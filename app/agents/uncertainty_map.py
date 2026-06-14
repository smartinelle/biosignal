"""Uncertainty decision graph for BioSignal Navigator.

The product should preserve scientific ambiguity as a decision graph instead of
collapsing it into a fake answer. This module converts hypotheses + next
measurements into branches a human can inspect in the app.
"""

from __future__ import annotations

_FORBIDDEN = ("diagnosis", "treatment", "transplant", "discard", "viability prediction")


def _clean(text: str) -> str:
    cleaned = text
    replacements = {
        "diagnosis": "research interpretation",
        "treatment": "research follow-up",
        "transplant": "clinical-use",
        "discard": "set aside for review",
        "viability prediction": "viability-related claim",
    }
    for bad, repl in replacements.items():
        cleaned = cleaned.replace(bad, repl).replace(bad.title(), repl)
    return cleaned


def _effort_score(measurement: str) -> int:
    lower = measurement.lower()
    if any(token in lower for token in ("control", "layout", "audit", "log", "repeat")):
        return 1
    if any(token in lower for token in ("orthogonal", "assay", "panel", "screen")):
        return 2
    return 3


def build_uncertainty_map(
    structured: dict,
    hypotheses: list[dict],
    measurements: list[dict],
    evidence: list[dict],
    bottleneck: dict,
) -> dict:
    """Return a decision graph for 'what would change our mind?'."""
    branches = []
    for idx, hypothesis in enumerate(hypotheses[:3], 1):
        measurement = measurements[idx - 1] if idx - 1 < len(measurements) else (measurements[0] if measurements else {})
        mechanism = hypothesis.get("mechanism", f"hypothesis_{idx}")
        test = measurement.get("measurement", "minimal discriminating control")
        branches.append({
            "id": f"branch_{idx}",
            "hypothesis": _clean(mechanism),
            "why_plausible": _clean(hypothesis.get("rationale", "Fits at least one observed signal.")),
            "test": _clean(test),
            "effort_score": _effort_score(test),
            "what_would_change_our_mind": _clean(
                f"If {test.lower()} weakens {mechanism}, deprioritize this branch and test the next explanation."
            ),
            "human_question": _clean(
                f"Is {mechanism} scientifically plausible enough to spend the next experiment on?"
            ),
        })

    if not branches:
        branches.append({
            "id": "branch_1",
            "hypothesis": "insufficient structured evidence",
            "why_plausible": "The note lacks enough controlled observations.",
            "test": "collect baseline and control context",
            "effort_score": 1,
            "what_would_change_our_mind": "If controls are normal, revisit possible biology; if controls fail, fix the workflow first.",
            "human_question": "What missing context would make this interpretable?",
        })

    mermaid_lines = ["graph TD", "A[Ambiguous experiment readout]"]
    for branch in branches:
        node_id = branch["id"].replace("branch_", "B")
        test_id = f"T{node_id[1:]}"
        mermaid_lines.append(f"A --> {node_id}[{branch['hypothesis']}]")
        mermaid_lines.append(f"{node_id} --> {test_id}[Test: {branch['test']}]")

    result = {
        "headline": "What would change our mind?",
        "bottleneck": _clean(bottleneck.get("headline", "The current evidence is underdetermined.")),
        "domain": structured.get("domain", "biotech experiment troubleshooting"),
        "evidence_count": len(evidence),
        "branches": branches,
        "mermaid": "\n".join(mermaid_lines),
        "copy": "Most AI tools collapse uncertainty into an answer. BioSignal Navigator preserves it as a decision graph.",
    }
    rendered = str(result).lower()
    for term in _FORBIDDEN:
        if term in rendered:
            # Raise (not assert) so the safety check still runs under PYTHONOPTIMIZE.
            raise ValueError(f"Forbidden clinical term '{term}' in uncertainty-map output")
    return result
