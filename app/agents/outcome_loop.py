"""Run outcome loop for closing the troubleshooting product cycle."""

from __future__ import annotations

_OUTCOME_COPY = {
    "confirmed_branch": "Outcome confirmed the selected branch; use this as a positive label.",
    "weakened_branch": "Outcome weakened the selected branch; use this as a correction label.",
    "inconclusive": "Outcome was inconclusive; request missing context or a cheaper orthogonal check.",
    "new_anomaly_found": "Outcome surfaced a new anomaly; create a new branch before recommending another action.",
}


def _delta_for(index: int, outcome: str) -> float:
    if outcome == "confirmed_branch":
        return 0.18 if index == 0 else -0.08
    if outcome == "weakened_branch":
        return -0.18 if index == 0 else 0.06
    if outcome == "new_anomaly_found":
        return -0.05
    return 0.0


def apply_run_outcome(
    action_plan: dict,
    uncertainty_map: dict,
    pioneer_structured: dict,
    outcome: str,
    selected_branch_index: int = 0,
    note: str = "",
) -> dict:
    """Update branch confidence after the next measurement returns an outcome."""
    branches = uncertainty_map.get("branches", [])
    actions = action_plan.get("ranked_actions", [])
    selected_action = actions[0] if actions else {"title": "next discriminating check", "confidence": 0.5}
    updates = []
    for idx, branch in enumerate(branches):
        old_conf = float(selected_action.get("confidence", 0.5)) if idx == selected_branch_index else 0.5
        delta = _delta_for(idx - selected_branch_index, outcome)
        new_conf = round(max(0.05, min(0.95, old_conf + delta)), 2)
        updates.append({
            "branch": branch.get("hypothesis", f"branch_{idx + 1}"),
            "test": branch.get("test", selected_action.get("title", "next check")),
            "old_confidence": round(old_conf, 2),
            "new_confidence": new_conf,
            "delta": round(delta, 2),
            "status": "reinforced" if delta > 0 else "weakened" if delta < 0 else "unchanged",
        })

    top_relation = (pioneer_structured.get("relations") or [{}])[0]
    training_row = {
        "input": {
            "selected_action": selected_action.get("title"),
            "outcome_note": note or _OUTCOME_COPY.get(outcome, "Human recorded outcome."),
            "pioneer_observations": pioneer_structured.get("observations", []),
        },
        "labels": {
            "outcome": outcome,
            "relation": top_relation,
            "branch_update": updates[0] if updates else {},
            "human_review_required": True,
        },
    }

    if outcome == "confirmed_branch":
        what_next = "Promote the confirmed branch into experiment memory and run the smallest confirmatory/replicate check."
    elif outcome == "weakened_branch":
        what_next = "Demote the selected branch and test the next highest-uncertainty explanation."
    elif outcome == "new_anomaly_found":
        what_next = "Create a new uncertainty branch before spending another assay cycle."
    else:
        what_next = "Ask for missing context or run a cheaper orthogonal control."

    return {
        "outcome": outcome,
        "summary": _OUTCOME_COPY.get(outcome, "Human recorded an outcome."),
        "selected_action": selected_action.get("title"),
        "branch_updates": updates,
        "pioneer_training_row": training_row,
        "what_next": what_next,
    }
