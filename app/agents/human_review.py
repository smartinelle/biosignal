"""Human review controls for the agent-human troubleshooting loop."""

from __future__ import annotations

from copy import deepcopy

_EFFORT_SCORE = {"low": 1, "medium": 2, "high": 3}

_FEEDBACK_COPY = {
    "accept_next_action": "Scientist accepted the next action; capture this as positive workflow feedback.",
    "ask_faster_alternative": "Scientist asked for the cheapest discriminating alternative before spending another assay cycle.",
    "flag_top_hypothesis_implausible": "Scientist flagged the leading hypothesis as implausible; this is valuable correction data.",
    "add_missing_context": "Scientist added missing context; rerun extraction before committing to the next action.",
    "mark_overclaiming": "Scientist marked the output as overclaiming; strengthen safety-boundary extraction.",
}


def _with_effort_scores(actions: list[dict]) -> list[dict]:
    scored = []
    for action in actions:
        item = dict(action)
        item["effort_score"] = _EFFORT_SCORE.get(str(item.get("effort", "medium")).lower(), 2)
        scored.append(item)
    return scored


def apply_human_feedback(action_plan: dict, feedback: str, note: str = "") -> dict:
    """Return an annotated/reranked copy of an action plan after human review."""
    updated = deepcopy(action_plan)
    actions = _with_effort_scores(updated.get("ranked_actions", []))
    annotation = _FEEDBACK_COPY.get(feedback, "Scientist reviewed the plan; preserve the correction as feedback.")
    pioneer_training_event = feedback in {
        "accept_next_action",
        "flag_top_hypothesis_implausible",
        "add_missing_context",
        "mark_overclaiming",
    }

    if feedback == "ask_faster_alternative":
        actions = sorted(actions, key=lambda a: (a["effort_score"], -float(a.get("confidence", 0))))
        for idx, action in enumerate(actions, 1):
            action["rank"] = idx
        if actions:
            actions[0]["human_note"] = "Human requested the cheapest discriminating next step."
    elif feedback == "flag_top_hypothesis_implausible" and actions:
        actions[0]["human_note"] = "Human flagged the leading hypothesis as implausible; use as correction data."
        actions[0]["confidence"] = round(float(actions[0].get("confidence", 0.5)) * 0.6, 2)
    elif feedback == "add_missing_context" and actions:
        actions[0]["human_note"] = f"Missing context to add before rerun: {note or 'sample metadata / controls / baseline.'}"
    elif feedback == "mark_overclaiming" and actions:
        actions[0]["human_note"] = "Human marked the output as too strong; keep only research-workflow language."
    elif feedback == "accept_next_action" and actions:
        actions[0]["human_note"] = "Human accepted this as the next experiment to run."

    updated["ranked_actions"] = actions
    updated["human_feedback"] = {
        "choice": feedback,
        "annotation": annotation,
        "note": note,
        "pioneer_training_event": pioneer_training_event,
        "why_pioneer_cares": (
            "Accepted/rejected branches become labeled traces for fine-tuning the Pioneer extractor/router."
        ),
    }
    updated["human_decision"] = annotation
    return updated
