"""Pioneer-style structured extractor for biotech troubleshooting notes.

This module owns the deterministic "structured extraction" layer described in
``docs/pioneer_strategy.md``. The intent is to mirror what a fine-tuned GLiNER2
model deployed on Pioneer would return: macro signals, candidate mechanisms,
suggested measurements, relation triples, and safety-boundary flags.

Design rules (hackathon-safe):
- The deterministic fallback always works with no API key and no network call.
- A live Pioneer model is used only when both ``PIONEER_API_KEY`` and
  ``PIONEER_MODEL_ID`` are set; any failure falls back transparently.
- Output is repeatable for the same input (no randomness).
- The function never raises; the demo must not depend on Pioneer being reachable.

The live request shape is intentionally conservative and guarded because the
Pioneer endpoint contract is not hard-coded here. See:
https://docs.pioneer.ai/introduction
"""

from __future__ import annotations

import os
import re

# --- Deterministic lexicons -------------------------------------------------

# macro_signal keyword -> canonical label
_SIGNAL_LEXICON = {
    "lactate": "lactate",
    "ph": "pH",
    "vascular resistance": "vascular_resistance",
    "resistance": "vascular_resistance",
    "oxygen consumption": "oxygen_consumption",
    "oxygenation": "oxygenation",
    "oxygen": "oxygenation",
    "glucose": "glucose",
    "flow": "perfusion_flow",
    "pressure": "perfusion_pressure",
    "temperature": "temperature",
    "viability stain": "viability_stain",
    "viability": "viability_stain",
    "morphology": "morphology",
    "barrier": "barrier_integrity",
    "teer": "barrier_integrity",
    "differentiation": "differentiation_marker",
    "inflammatory": "inflammatory_marker",
    "cytokine": "inflammatory_marker",
    "ldh": "LDH",
    "atp": "ATP",
    "caspase": "caspase_activation",
    "ngal": "NGAL",
    "kim-1": "KIM-1",
    "ast": "AST_ALT",
    "alt": "AST_ALT",
    "transaminase": "AST_ALT",
    "bile": "bile_output",
    "urine": "urine_output",
    "creatinine": "creatinine",
    "potency": "assay_potency_signal",
    "signal": "assay_signal",
    "cell count": "cell_count",
    "positive control": "positive_control",
    "control": "assay_control",
    "plate edge": "plate_edge_effect",
    "edge wells": "plate_edge_effect",
    "reagent": "reagent_lot",
    "lot": "reagent_lot",
}

# words that signal a trend, mapped to a canonical trend label
_TREND_WORDS = {
    "rising": "rising",
    "rise": "rising",
    "increasing": "rising",
    "increase": "rising",
    "elevated": "rising",
    "high": "rising",
    "up": "rising",
    "falling": "falling",
    "fall": "falling",
    "decreasing": "falling",
    "decrease": "falling",
    "dropping": "falling",
    "low": "falling",
    "down": "falling",
    "uncertain": "uncertain",
    "unclear": "uncertain",
    "unknown": "uncertain",
    "borderline": "uncertain",
    "abnormal": "abnormal",
    "anomalous": "abnormal",
    "unexpected": "abnormal",
    "leak": "abnormal",
    "shift": "shifting",
    "change": "shifting",
}

# time / sample context tokens
_TIME_TOKENS = ["0h", "12h", "24h", "48h", "72h", "cold", "warm ischemia", "cold ischemia"]
_CONTEXT_TOKENS = {
    "organoid": "organoid",
    "organ-on-chip": "organ_on_chip",
    "tissue engineering": "tissue_engineering",
    "bioreactor": "tissue_engineering",
    "perfusion": "ex_vivo_perfusion",
    "preserv": "preservation",
    "tissue": "tissue",
}

# signal -> list of (mechanism_label, base_confidence)
_MECHANISM_RULES = {
    "lactate": [("hypoxia", 0.74), ("mitochondrial_dysfunction", 0.58)],
    "pH": [("hypoxia", 0.66), ("metabolic_failure", 0.55)],
    "vascular_resistance": [("endothelial_injury", 0.68), ("edema_or_microthrombi", 0.55)],
    "oxygenation": [("hypoxia", 0.70)],
    "oxygen_consumption": [("mitochondrial_dysfunction", 0.64)],
    "viability_stain": [("cell_type_specific_degradation", 0.6)],
    "morphology": [("structural_degradation", 0.58)],
    "barrier_integrity": [("model_instability", 0.6), ("drug_toxicity", 0.55)],
    "inflammatory_marker": [("inflammatory_activation", 0.66)],
    "LDH": [("membrane_damage_necrosis", 0.64)],
    "caspase_activation": [("apoptosis", 0.7)],
    "differentiation_marker": [("protocol_drift", 0.55)],
    "creatinine": [("tubuloepithelial_stress", 0.6)],
    "NGAL": [("tubuloepithelial_stress", 0.62)],
    "KIM-1": [("tubuloepithelial_stress", 0.62)],
    "assay_potency_signal": [("technical_artifact", 0.55), ("reagent_or_protocol_drift", 0.62)],
    "assay_signal": [("technical_artifact", 0.55), ("reagent_or_protocol_drift", 0.6)],
    "positive_control": [("reagent_or_protocol_drift", 0.68)],
    "assay_control": [("reagent_or_protocol_drift", 0.62)],
    "plate_edge_effect": [("technical_artifact", 0.72)],
    "reagent_lot": [("reagent_or_protocol_drift", 0.7)],
}

# mechanism -> discriminating measurement (label, base_confidence)
_MEASUREMENT_RULES = {
    "hypoxia": ("oxygen_consumption_assay", 0.72),
    "mitochondrial_dysfunction": ("mitochondrial_membrane_potential", 0.7),
    "endothelial_injury": ("endothelial_injury_marker", 0.68),
    "edema_or_microthrombi": ("perfusate_flow_pressure_trend", 0.6),
    "metabolic_failure": ("lactate_pH_trend_timecourse", 0.66),
    "cell_type_specific_degradation": ("targeted_rna_or_scrna_panel", 0.64),
    "structural_degradation": ("histology_imaging", 0.62),
    "model_instability": ("orthogonal_structural_assay", 0.6),
    "drug_toxicity": ("ldh_release_and_cytokine_panel", 0.64),
    "inflammatory_activation": ("cytokine_panel", 0.65),
    "membrane_damage_necrosis": ("ldh_release_assay", 0.66),
    "apoptosis": ("caspase_or_annexin_assay", 0.68),
    "protocol_drift": ("repeat_with_control_batch", 0.58),
    "tubuloepithelial_stress": ("tubular_injury_marker_panel", 0.63),
    "technical_artifact": ("control_and_layout_repeat", 0.7),
    "reagent_or_protocol_drift": ("old_vs_new_reagent_lot_control", 0.68),
}

# tokens that indicate a request for a clinical claim we must not make
_CLINICAL_RISK_TOKENS = [
    "diagnos",
    "treat",
    "transplant",
    "discard",
    "viability prediction",
    "predict viability",
    "prognos",
    "clinical decision",
    "accept or reject",
]


def _clause_trend(clause: str, signal_start: int, signal_end: int) -> str:
    """Pick the trend word in a clause nearest to the signal span."""
    best_label = "reported"
    best_distance = None
    for word, label in _TREND_WORDS.items():
        for match in re.finditer(rf"\b{re.escape(word)}\b", clause):
            position = (match.start() + match.end()) / 2
            distance = min(abs(position - signal_start), abs(position - signal_end))
            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_label = label
    return best_label


def _is_negated_signal(clause: str, label: str, start: int, end: int) -> bool:
    """Skip signals that appear inside a safety disclaimer, not as a readout.

    The notes deliberately contain phrases like "no clinical viability claim";
    matching "viability" there would create a phantom observation.
    """
    if label != "viability_stain":
        return False
    before = clause[max(0, start - 14):start]
    after = clause[end:min(len(clause), end + 16)]
    if any(token in before for token in ("no ", "not ", "without", "clinical")):
        return True
    if any(token in after for token in ("claim", "predict")):
        return True
    return False


def _extract_observations(text: str) -> list[dict]:
    """Clause-aware extraction so a trend attaches only within its own clause.

    Notes are typically comma-delimited ("lactate rising, pH falling"); splitting
    on clause boundaries prevents a neighbouring clause's trend from bleeding in.
    """
    lower = text.lower()
    seen = set()
    observations = []
    for clause in re.split(r"[.,;:\n]", lower):
        matched_spans: list[tuple[int, int]] = []
        for keyword, label in _SIGNAL_LEXICON.items():
            if label in seen:
                continue
            match = re.search(rf"\b{re.escape(keyword)}\b", clause)
            if not match:
                continue
            # skip sub-matches inside an already-claimed span, e.g. "oxygen"
            # inside "oxygen consumption" (multi-word keywords are ordered first)
            if any(s < match.end() and match.start() < e for s, e in matched_spans):
                continue
            if _is_negated_signal(clause, label, match.start(), match.end()):
                continue
            seen.add(label)
            matched_spans.append((match.start(), match.end()))
            trend = _clause_trend(clause, match.start(), match.end())
            observations.append({"label": label, "trend": trend})
    return observations


def _round(value: float) -> float:
    return round(min(value, 0.95), 2)


def _extract_mechanisms(observations: list[dict]) -> list[dict]:
    scores: dict[str, float] = {}
    for obs in observations:
        for mechanism, conf in _MECHANISM_RULES.get(obs["label"], []):
            # reinforce a mechanism deterministically when multiple signals point to it
            scores[mechanism] = scores.get(mechanism, 0.0)
            scores[mechanism] = max(scores[mechanism], conf) + (0.04 if scores[mechanism] else 0.0)
    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    return [{"label": label, "confidence": _round(conf)} for label, conf in ranked[:5]]


def _extract_measurements(mechanisms: list[dict]) -> list[dict]:
    seen = set()
    measurements = []
    for mech in mechanisms:
        rule = _MEASUREMENT_RULES.get(mech["label"])
        if not rule:
            continue
        label, conf = rule
        if label in seen:
            continue
        seen.add(label)
        measurements.append({"label": label, "confidence": _round(conf)})
    return measurements


def _extract_relations(observations: list[dict], mechanisms: list[dict], measurements: list[dict]) -> list[dict]:
    relations = []
    mech_labels = {m["label"] for m in mechanisms}
    for obs in observations:
        for mechanism, conf in _MECHANISM_RULES.get(obs["label"], []):
            if mechanism in mech_labels:
                relations.append({
                    "subject": f"{obs['label']} {obs['trend']}",
                    "predicate": "supports_possible_mechanism",
                    "object": mechanism,
                    "confidence": _round(conf),
                })
    for mech in mechanisms:
        rule = _MEASUREMENT_RULES.get(mech["label"])
        if rule:
            relations.append({
                "subject": rule[0],
                "predicate": "reduces_uncertainty_about",
                "object": mech["label"],
                "confidence": _round(rule[1]),
            })
    return relations


def _extract_context(text: str) -> dict:
    lower = text.lower()
    time_context = [t for t in _TIME_TOKENS if t in lower]
    sample_context = sorted({label for token, label in _CONTEXT_TOKENS.items() if token in lower})
    return {"time_context": time_context, "sample_context": sample_context}


def _safety_flags(text: str, observations: list[dict]) -> dict:
    lower = text.lower()
    clinical_risk = any(token in lower for token in _CLINICAL_RISK_TOKENS)
    return {
        "research_workflow_only": True,
        "needs_human_review": True,
        "clinical_claim_risk": clinical_risk,
        "insufficient_evidence": len(observations) < 2,
    }


def _fallback_extract(note: str) -> dict:
    observations = _extract_observations(note)
    mechanisms = _extract_mechanisms(observations)
    measurements = _extract_measurements(mechanisms)
    relations = _extract_relations(observations, mechanisms, measurements)
    context = _extract_context(note)
    return {
        "domain": "living_tissue_systems",
        "observations": observations,
        "candidate_mechanisms": mechanisms,
        "suggested_measurements": measurements,
        "relations": relations,
        "context": context,
        "safety_flags": _safety_flags(note, observations),
        "mode": "fallback",
        "detail": "Deterministic GLiNER2-style structured extractor — the Pioneer side-challenge artifact.",
    }


def pioneer_status() -> dict:
    """Report Pioneer availability without making a network call."""
    has_key = bool(os.getenv("PIONEER_API_KEY"))
    has_model = bool(os.getenv("PIONEER_MODEL_ID"))
    if has_key and has_model:
        return {"available": True, "mode": "live", "model_id": os.getenv("PIONEER_MODEL_ID")}
    missing = [name for name in ("PIONEER_API_KEY", "PIONEER_MODEL_ID")
               if not os.getenv(name)]
    return {"available": False, "mode": "fallback", "missing": missing}


def _live_extract(note: str) -> dict | None:
    """Best-effort call to a deployed Pioneer model.

    Returns ``None`` on any problem so the caller can fall back. The request
    shape is intentionally conservative; confirm the exact contract against the
    Pioneer docs before relying on this in production.
    """
    base_url = os.getenv("PIONEER_BASE_URL", "https://api.pioneer.ai")
    model_id = os.getenv("PIONEER_MODEL_ID")
    api_key = os.getenv("PIONEER_API_KEY")
    try:
        import requests

        response = requests.post(
            f"{base_url.rstrip('/')}/v1/extract",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"model": model_id, "input": note},
            timeout=12,
        )
        response.raise_for_status()
        payload = response.json()
    except Exception:
        return None

    # Merge live payload onto the deterministic skeleton so downstream code
    # always sees the full schema even if the model omits a field.
    structured = _fallback_extract(note)
    if isinstance(payload, dict):
        for key in ("observations", "candidate_mechanisms", "suggested_measurements", "relations"):
            if isinstance(payload.get(key), list):
                structured[key] = payload[key]
    structured["mode"] = "live"
    structured["detail"] = f"Pioneer model '{model_id}' returned structured extraction."
    return structured


def extract_troubleshooting_structure(note: str) -> dict:
    """Return observations, mechanisms, measurements, relations, and safety flags.

    Uses a deployed Pioneer model when credentials are present, otherwise the
    deterministic fallback. Never raises.
    """
    # The deterministic extractor is the shipped Pioneer artifact. A deployed
    # model (PIONEER_MODEL_ID) is an optional route, not a required step.
    if pioneer_status()["available"]:
        live = _live_extract(note)
        if live is not None:
            return live
        fallback = _fallback_extract(note)
        fallback["detail"] = "Optional live Pioneer call failed; deterministic extractor used."
        return fallback
    return _fallback_extract(note)
