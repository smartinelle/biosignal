"""Deterministic action-plan builder for BioSignal Navigator.

This layer turns the existing pipeline output into an operational product surface:
ranked next actions, remaining unknowns, and a partner-ready summary. It is fully
local and rule-based so the demo works without API keys.
"""

from __future__ import annotations

_FORBIDDEN = [
    "diagnosis",
    "treatment",
    "transplant",
    "discard",
    "viability prediction",
    "batch release",
    "release readiness",
    "disposition",
]


def _clean(text: str) -> str:
    """Keep action-plan copy inside the research-only safety boundary."""
    cleaned = text
    replacements = {
        "discard": "set aside for research review",
        "batch release": "workflow decision",
        "release readiness": "workflow readiness",
        "disposition": "workflow decision",
        "diagnosis": "research interpretation",
        "treatment": "research follow-up",
        "transplant": "clinical-use",
        "viability prediction": "viability-related claim",
    }
    for bad, replacement in replacements.items():
        cleaned = cleaned.replace(bad, replacement).replace(bad.title(), replacement)
    return cleaned


def _effort_for(measurement: str) -> str:
    lower = measurement.lower()
    if any(token in lower for token in ["audit", "analysis", "review", "log", "layout", "control repeat"]):
        return "low"
    if any(token in lower for token in ["orthogonal", "assay", "panel", "screen", "matrix", "side-by-side"]):
        return "medium"
    if any(token in lower for token in ["scrna", "sequencing", "omics", "multi-condition"]):
        return "high"
    return "medium"


def _impact_for(rank: int, measurement: str) -> str:
    lower = measurement.lower()
    if rank == 1 or any(token in lower for token in ["control", "calibration", "old-vs-new", "contamination"]):
        return "high"
    if rank <= 3:
        return "medium"
    return "low"


def _confidence(rank: int, evidence_count: int, measurement: str) -> float:
    lower = measurement.lower()
    score = 0.72 - (rank - 1) * 0.07
    if evidence_count >= 2:
        score += 0.05
    if any(token in lower for token in ["control", "calibration", "audit", "side-by-side"]):
        score += 0.06
    if any(token in lower for token in ["scrna", "sequencing", "omics"]):
        score -= 0.08
    return round(max(0.35, min(0.92, score)), 2)


def _expected_readout(measurement: dict, hypothesis: dict | None) -> str:
    name = measurement.get("measurement", "follow-up check")
    if hypothesis:
        return f"Shows whether {name.lower()} supports or weakens: {hypothesis.get('mechanism', 'the leading hypothesis')}."
    return f"Shows whether {name.lower()} reduces the main uncertainty enough to choose the next experiment."


def _success_criteria(measurement: dict, hypothesis: dict | None) -> list[str]:
    name = measurement.get("measurement", "follow-up check")
    criteria = [f"The team can interpret {name.lower()} without relying on a single ambiguous signal."]
    if hypothesis:
        criteria.append(f"The result separates {hypothesis.get('mechanism', 'the leading hypothesis')} from at least one alternative explanation.")
    else:
        criteria.append("The result separates technical artifact from possible biological change.")
    return [_clean(c) for c in criteria]


def _unknowns(structured: dict, bottleneck: dict) -> list[str]:
    domain = str(structured.get("domain", "biotech experiment troubleshooting"))
    signals = structured.get("signals_detected", [])
    unknowns = [
        bottleneck.get("decision_to_unlock", "Which explanation should be tested first?"),
        f"Whether the observed pattern in {domain} is technical artifact, process drift, or a real biological change.",
    ]
    if signals:
        unknowns.append(f"Which of these signals is actually causal rather than correlated: {', '.join(signals[:5])}.")
    unknowns.append("Whether an orthogonal check would reproduce the same interpretation.")
    return [_clean(u) for u in unknowns[:4]]


def _partner_summary(structured: dict, actions: list[dict], workflow_context: dict, bottleneck: dict, partner_trace: list[dict]) -> list[str]:
    live_tools = [item["tool"] for item in partner_trace if item.get("live")]
    artifact_tools = [item["tool"] for item in partner_trace if not item.get("live")]
    top = actions[0] if actions else {"title": "Run the smallest discriminating check"}
    bullets = [
        f"Problem: ambiguous {structured.get('domain', 'biotech R&D')} run needs a next experiment, not a black-box answer.",
        f"Bottleneck: {bottleneck.get('headline', 'the current evidence is underdetermined')}",
        f"Recommended next step: {top['title']}.",
        f"Use-case framing: {workflow_context.get('role', 'General biotech R&D workflow')}.",
        "Safety: research workflow only; no clinical, viability, release, or discard recommendation.",
    ]
    if live_tools or artifact_tools:
        bullets.append(f"Partner trace: live={', '.join(live_tools) or 'none'}; artifact/fallback={', '.join(artifact_tools) or 'none'}.")
    return [_clean(b) for b in bullets]


def build_action_plan(
    structured: dict,
    hypotheses: list[dict],
    measurements: list[dict],
    evidence: list[dict],
    workflow_context: dict,
    bottleneck: dict,
    partner_trace: list[dict],
) -> dict:
    """Build a deterministic product-facing action plan from pipeline outputs."""
    evidence_count = len(evidence)
    actions = []
    for idx, measurement in enumerate(measurements[:5], 1):
        hypothesis = hypotheses[idx - 1] if idx - 1 < len(hypotheses) else (hypotheses[0] if hypotheses else None)
        name = measurement.get("measurement", f"Follow-up check {idx}")
        why = measurement.get("why", "Reduces uncertainty before the next experimental cycle.")
        effort = _effort_for(name)
        impact = _impact_for(idx, name)
        confidence = _confidence(idx, evidence_count, name)
        actions.append({
            "rank": idx,
            "title": _clean(name),
            "goal": _clean(why),
            "why_now": _clean(
                "This is the fastest way to turn the current ambiguity into an interpretable next experimental decision."
                if idx == 1 else
                "This provides a secondary check if the top action does not resolve the uncertainty."
            ),
            "effort": effort,
            "impact": impact,
            "confidence": confidence,
            "evidence_count": evidence_count,
            "expected_readout": _clean(_expected_readout(measurement, hypothesis)),
            "success_criteria": _success_criteria(measurement, hypothesis),
            "risk": _clean("Can still be misleading if controls, sample handling, or baseline context are incomplete."),
        })

    if not actions:
        actions.append({
            "rank": 1,
            "title": "Collect a minimal control and baseline comparison",
            "goal": "Create enough context to separate technical artifact from possible biology.",
            "why_now": "The current note does not contain enough structured evidence for a stronger recommendation.",
            "effort": "low",
            "impact": "medium",
            "confidence": 0.5,
            "evidence_count": evidence_count,
            "expected_readout": "A clearer baseline for the next troubleshooting pass.",
            "success_criteria": ["At least one control or baseline comparison is available."],
            "risk": "Still underdetermined if the underlying run metadata is missing.",
        })

    return {
        "problem_summary": _clean(
            f"{workflow_context.get('role', 'General biotech R&D workflow')}: {workflow_context.get('workflow_moment', structured.get('workflow_goal', 'choose the next best measurement'))}"
        ),
        "bottleneck": {
            "title": _clean(bottleneck.get("headline", "The current evidence is underdetermined.")),
            "why_it_matters": _clean(bottleneck.get("why_it_matters", "The next experiment should reduce uncertainty rather than amplify it.")),
            "confidence": 0.74,
        },
        "ranked_actions": actions[:3],
        "what_we_do_not_know": _unknowns(structured, bottleneck),
        "human_decision": _clean(
            "Human review is needed to decide whether to repeat, run an orthogonal check, or treat the current evidence as inconclusive."
        ),
        "partner_summary": _partner_summary(structured, actions, workflow_context, bottleneck, partner_trace),
    }


def contains_forbidden_language(action_plan: dict) -> list[str]:
    """Return forbidden terms found in the rendered action-plan text."""
    text = str(action_plan).lower()
    return [term for term in _FORBIDDEN if term in text]
