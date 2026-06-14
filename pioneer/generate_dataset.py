"""Synthetic GLiNER2 training-data generator for the Pioneer side challenge.

This produces a labelled dataset in GLiNER2 JSONL format
(`{"input": ..., "output": {entities, classifications, relations}}`) for the
narrow task BioSignal Navigator cares about:

    messy biotech experiment note
        -> macro_signal / trend / candidate_mechanism / assay entities
        -> safety + domain classifications
        -> observation -> mechanism -> measurement relations

It is deterministic (seeded) and needs no API key, so it documents the
data-engineering half of the Pioneer workflow even before a training job runs.
The same JSONL uploads directly to Pioneer `POST /v1/datasets` for the
NER / structured-extraction fine-tune.

Run:
    python pioneer/generate_dataset.py --train 180 --eval 40 --out pioneer/data
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

# Grounded in the app's own deterministic lexicon so the fine-tune target
# matches what the product actually consumes downstream.
SIGNAL_PHRASES = {
    "lactate": ("lactate", ["hypoxia", "mitochondrial_dysfunction"], "oxygen_consumption_assay"),
    "pH": ("pH", ["hypoxia", "metabolic_failure"], "lactate_pH_trend_timecourse"),
    "vascular resistance": ("vascular_resistance", ["endothelial_injury"], "endothelial_injury_marker"),
    "oxygenation": ("oxygenation", ["hypoxia"], "oxygen_consumption_assay"),
    "LDH": ("LDH", ["membrane_damage_necrosis"], "ldh_release_assay"),
    "caspase": ("caspase_activation", ["apoptosis"], "caspase_or_annexin_assay"),
    "TEER": ("barrier_integrity", ["model_instability", "drug_toxicity"], "orthogonal_structural_assay"),
    "cytokine": ("inflammatory_marker", ["inflammatory_activation"], "cytokine_panel"),
    "positive control": ("positive_control", ["reagent_or_protocol_drift"], "old_vs_new_reagent_lot_control"),
    "edge wells": ("plate_edge_effect", ["technical_artifact"], "control_and_layout_repeat"),
    "reagent lot": ("reagent_lot", ["reagent_or_protocol_drift"], "old_vs_new_reagent_lot_control"),
    "assay signal": ("assay_signal", ["technical_artifact", "reagent_or_protocol_drift"], "control_and_layout_repeat"),
    "creatinine": ("creatinine", ["tubuloepithelial_stress"], "tubular_injury_marker_panel"),
    "NGAL": ("NGAL", ["tubuloepithelial_stress"], "tubular_injury_marker_panel"),
}

TREND_PHRASES = {
    "rising": ["rising", "increasing", "elevated", "trending up"],
    "falling": ["falling", "dropping", "decreasing", "lower than expected"],
    "uncertain": ["uncertain", "borderline", "unclear"],
    "abnormal": ["anomalous", "unexpected", "shifted"],
}

SAMPLE_CONTEXTS = {
    "organoid": "organoid",
    "organ-on-chip": "organ_on_chip",
    "ex vivo perfused liver": "ex_vivo_perfusion",
    "48h cold-preserved kidney": "preservation",
    "bioreactor tissue construct": "tissue_engineering",
    "96-well potency assay plate": "assay_plate",
}

TIME_CONTEXTS = ["0h", "12h", "24h", "48h", "72h"]

# Unsafe overclaim requests the model must flag, never satisfy.
CLINICAL_OVERCLAIMS = [
    "tell me if this organ is viable for transplant",
    "decide whether to discard this graft",
    "give me a clinical diagnosis",
    "predict the viability score and clear it for the patient",
    "should we accept or reject this organ for surgery",
]


def _round(v: float) -> float:
    return round(min(v, 0.95), 2)


def _make_positive_example(rng: random.Random) -> dict:
    n_signals = rng.choice([2, 2, 3, 3, 4])
    chosen = rng.sample(list(SIGNAL_PHRASES.items()), n_signals)
    sample_phrase, sample_label = rng.choice(list(SAMPLE_CONTEXTS.items()))
    time_token = rng.choice(TIME_CONTEXTS)

    clauses = [f"{sample_phrase} at {time_token}"]
    signal_mentions: list[str] = []
    trend_mentions: list[str] = []
    mechanism_set: list[str] = []
    measurement_set: list[str] = []
    relations: list[dict] = []

    for phrase, (canon, mechanisms, measurement) in chosen:
        trend_key = rng.choice(list(TREND_PHRASES.keys()))
        trend_word = rng.choice(TREND_PHRASES[trend_key])
        clauses.append(f"{phrase} {trend_word}")
        signal_mentions.append(phrase)
        trend_mentions.append(trend_word)
        top_mech = mechanisms[0]
        if top_mech not in mechanism_set:
            mechanism_set.append(top_mech)
        if measurement not in measurement_set:
            measurement_set.append(measurement)
        relations.append({
            "subject": phrase,
            "relation": "supports_possible_mechanism",
            "object": top_mech,
        })
        relations.append({
            "subject": measurement,
            "relation": "reduces_uncertainty_about",
            "object": top_mech,
        })

    goal = rng.choice([
        "decide what to measure next",
        "separate technical artifact from real biology",
        "choose the next discriminating experiment",
    ])
    text = f"Context: {', '.join(clauses)}. Goal: {goal}. Research workflow only."

    entities: dict[str, list[str]] = {}
    if signal_mentions:
        entities["macro_signal"] = signal_mentions
    if trend_mentions:
        entities["trend"] = trend_mentions
    if mechanism_set:
        entities["candidate_mechanism"] = mechanism_set
    if measurement_set:
        entities["assay"] = measurement_set
    entities["sample_context"] = [sample_phrase]
    entities["time_context"] = [time_token]

    output = {
        "entities": entities,
        "classifications": [
            {
                "task": "safety",
                "labels": ["research_workflow_only", "clinical_claim_risk"],
                "true_label": ["research_workflow_only"],
            },
            {
                "task": "review",
                "labels": ["needs_human_review", "auto_safe"],
                "true_label": ["needs_human_review"],
            },
        ],
        "relations": relations,
    }
    return {"input": text, "output": output}


def _make_safety_example(rng: random.Random) -> dict:
    overclaim = rng.choice(CLINICAL_OVERCLAIMS)
    sample_phrase = rng.choice(list(SAMPLE_CONTEXTS.keys()))
    signal = rng.choice(list(SIGNAL_PHRASES.keys()))
    trend = rng.choice(TREND_PHRASES["rising"] + TREND_PHRASES["falling"])
    text = f"{sample_phrase}: {signal} {trend}. {overclaim}."
    output = {
        "entities": {
            "macro_signal": [signal],
            "trend": [trend],
            "safety_boundary": [overclaim],
        },
        "classifications": [
            {
                "task": "safety",
                "labels": ["research_workflow_only", "clinical_claim_risk"],
                "true_label": ["clinical_claim_risk"],
            },
            {
                "task": "review",
                "labels": ["needs_human_review", "auto_safe"],
                "true_label": ["needs_human_review"],
            },
        ],
        "relations": [
            {"subject": overclaim, "relation": "must_not_claim", "object": signal},
        ],
    }
    return {"input": text, "output": output}


def _make_sparse_example(rng: random.Random) -> dict:
    """Incomplete note: one signal, no trend — should yield insufficient_evidence."""
    signal = rng.choice(list(SIGNAL_PHRASES.keys()))
    sample_phrase = rng.choice(list(SAMPLE_CONTEXTS.keys()))
    text = f"{sample_phrase}. Something looked off with {signal} but no numbers recorded yet."
    output = {
        "entities": {"macro_signal": [signal], "sample_context": [sample_phrase]},
        "classifications": [
            {
                "task": "evidence",
                "labels": ["sufficient_evidence", "insufficient_evidence"],
                "true_label": ["insufficient_evidence"],
            },
        ],
    }
    return {"input": text, "output": output}


def generate(n: int, seed: int) -> list[dict]:
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        roll = rng.random()
        if roll < 0.70:
            rows.append(_make_positive_example(rng))
        elif roll < 0.88:
            rows.append(_make_safety_example(rng))
        else:
            rows.append(_make_sparse_example(rng))
    return rows


def write_jsonl(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate GLiNER2 synthetic dataset for Pioneer.")
    parser.add_argument("--train", type=int, default=180)
    parser.add_argument("--eval", type=int, default=40)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--out", type=str, default="pioneer/data")
    args = parser.parse_args()

    out = Path(args.out)
    train_rows = generate(args.train, args.seed)
    eval_rows = generate(args.eval, args.seed + 1000)
    write_jsonl(train_rows, out / "train.jsonl")
    write_jsonl(eval_rows, out / "eval.jsonl")

    print(f"train examples: {len(train_rows)} -> {out / 'train.jsonl'}")
    print(f"eval examples:  {len(eval_rows)} -> {out / 'eval.jsonl'}")

    # Quick label distribution for the README / submission narrative.
    from collections import Counter
    safety = Counter()
    for row in train_rows:
        for c in row["output"].get("classifications", []):
            if c["task"] == "safety":
                safety[c["true_label"][0]] += 1
    print("safety label distribution (train):", dict(safety))


if __name__ == "__main__":
    main()
