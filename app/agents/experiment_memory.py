"""Experiment memory and Pioneer training-loop surface.

This is product-shaped memory for the demo, not a clinical knowledge base. It
shows how reviewed troubleshooting runs become labeled traces for Pioneer.
"""

from __future__ import annotations


def _top_action(action_plan: dict) -> dict:
    actions = action_plan.get("ranked_actions", [])
    return actions[0] if actions else {"title": "collect baseline controls", "confidence": 0.5}


def _historical_runs() -> list[dict]:
    return [
        {
            "source": "example_memory",
            "workflow": "qPCR / ddPCR anomaly",
            "ambiguous_signal": "late Ct + weak no-template amplification",
            "chosen_branch": "primer-dimer / contamination check",
            "next_action": "repeat NTC + melt-curve review",
            "status": "resolved_by_control",
            "pioneer_value": "positive label for contamination/primer artifact extraction",
        },
        {
            "source": "example_memory",
            "workflow": "assay signal collapse",
            "ambiguous_signal": "signal down + edge wells worse + reagent lot change",
            "chosen_branch": "plate artifact vs reagent drift",
            "next_action": "edge-vs-center layout repeat and old-vs-new lot control",
            "status": "pending_repeat",
            "pioneer_value": "relation labels: plate_edge_effect supports technical_artifact",
        },
        {
            "source": "example_memory",
            "workflow": "ex-vivo tissue preservation",
            "ambiguous_signal": "lactate rising + pH falling + resistance increasing",
            "chosen_branch": "hypoxia vs endothelial injury",
            "next_action": "oxygen consumption + endothelial injury marker",
            "status": "needs_human_review",
            "pioneer_value": "safety label: do not infer clinical viability",
        },
    ]


def build_experiment_memory(structured: dict, action_plan: dict, pioneer_structured: dict) -> dict:
    """Build a product-facing learning loop from the current and past runs."""
    top = _top_action(action_plan)
    current = {
        "source": "current_run",
        "workflow": structured.get("domain", "biotech experiment troubleshooting"),
        "ambiguous_signal": ", ".join(structured.get("signals_detected", [])[:5]) or "messy experiment note",
        "chosen_branch": top.get("title", "next discriminating check"),
        "next_action": top.get("title", "next discriminating check"),
        "status": "reviewed" if action_plan.get("human_feedback") else "awaiting_human_review",
        "pioneer_value": "new labeled trace: note → entities → branch → human correction → next action",
    }
    runs = [current] + _historical_runs()
    accepted = sum(1 for run in runs if run["status"] in {"reviewed", "resolved_by_control"})
    pending = sum(1 for run in runs if "pending" in run["status"] or "review" in run["status"])
    return {
        "headline": "Experiment memory → Pioneer improvement loop",
        "runs": runs,
        "stats": {
            "stored_runs": len(runs),
            "accepted_or_resolved": accepted,
            "pending_or_review_needed": pending,
            "extracted_relations_this_run": len(pioneer_structured.get("relations", [])),
        },
        "learning_loop": (
            "Pioneer extracts structured entities/relations from each run; the human accepts, rejects, "
            "or edits the branch; those corrections become synthetic/eval examples for the next GLiNER2 fine-tune."
        ),
    }


def training_examples_from_memory(memory: dict) -> list[dict]:
    """Convert visible experiment memory into compact Pioneer-style examples."""
    examples = []
    for run in memory.get("runs", []):
        examples.append({
            "input": f"Workflow: {run['workflow']}. Signals: {run['ambiguous_signal']}. Human chose: {run['chosen_branch']}.",
            "labels": {
                "entities": ["macro_signal", "candidate_mechanism", "assay", "safety_boundary"],
                "relations": ["supports_possible_mechanism", "reduces_uncertainty_about", "requires_human_review_for"],
                "classification": run["status"],
            },
            "pioneer_value": run["pioneer_value"],
        })
    return examples
