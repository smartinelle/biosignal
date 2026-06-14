"""Evidence quality grading for scientific/clinical credibility.

The app should not treat every source as equal. This module makes evidence
quality visible while keeping all outputs in a research-only safety boundary.
"""

from __future__ import annotations


def _lower(item: dict, key: str) -> str:
    return str(item.get(key, "")).lower()


def _evidence_type(item: dict) -> str:
    source = _lower(item, "source")
    claim = _lower(item, "claim")
    if item.get("live"):
        return "live web lead"
    if any(token in source + claim for token in ("atlas", "prjeb", "paper", "scRNA".lower(), "dataset", "et al")):
        return "paper/dataset"
    if any(token in source for token in ("vendor", "protocol", "guide", "docs")):
        return "vendor/protocol docs"
    if "heuristic" in source or "practice" in source:
        return "heuristic"
    return "unverified hypothesis"


def _relevance(item: dict, domain: str) -> str:
    text = f"{item.get('source', '')} {item.get('claim', '')} {item.get('caveat', '')}".lower()
    domain_lower = domain.lower()
    if "indirect" in text or "not necessarily" in text or "not the same" in text:
        return "adjacent"
    if any(token in text for token in domain_lower.split("/")[0].split()[:3]):
        return "direct"
    if item.get("live") or "heuristic" in text:
        return "adjacent"
    return "weak"


def _risk(item: dict) -> str:
    text = f"{item.get('claim', '')} {item.get('caveat', '')}".lower()
    if any(token in text for token in ("clinical", "viability", "transplant", "release", "disposition")):
        return "clinical leap risk"
    if item.get("live"):
        return "unverified live-source risk"
    if "indirect" in text or "not the same" in text:
        return "overgeneralization risk"
    if "heuristic" in text:
        return "heuristic-only risk"
    return "normal caveat risk"


def _strength(evidence_type: str, relevance: str) -> int:
    base = {
        "paper/dataset": 4,
        "vendor/protocol docs": 3,
        "heuristic": 2,
        "live web lead": 2,
        "unverified hypothesis": 1,
    }.get(evidence_type, 1)
    if relevance == "direct":
        base += 1
    elif relevance == "weak":
        base -= 1
    return max(1, min(5, base))


def grade_evidence(evidence: list[dict], domain: str) -> list[dict]:
    """Add type/relevance/risk/safe-use labels to evidence cards."""
    graded = []
    for item in evidence:
        evidence_type = _evidence_type(item)
        relevance = _relevance(item, domain)
        risk = _risk(item)
        graded_item = dict(item)
        graded_item.update({
            "evidence_type": evidence_type,
            "relevance": relevance,
            "risk": risk,
            "strength": _strength(evidence_type, relevance),
            "safe_use": "Use for hypothesis generation and next-measurement selection only; require human scientific review.",
            "action_implication": "Can inform which branch to test next, not a final biological or clinical conclusion.",
        })
        graded.append(graded_item)
    return sorted(graded, key=lambda x: (-x["strength"], x.get("source", "")))


def build_evidence_ladder(graded_evidence: list[dict]) -> list[dict]:
    """Summarize evidence by strength tier for a compact UI ladder."""
    buckets: dict[int, list[dict]] = {}
    for item in graded_evidence:
        buckets.setdefault(int(item.get("strength", 1)), []).append(item)
    ladder = []
    for strength in sorted(buckets.keys(), reverse=True):
        items = buckets[strength]
        ladder.append({
            "strength": strength,
            "label": {
                5: "Strong / direct",
                4: "Useful / adjacent",
                3: "Operational support",
                2: "Weak lead",
                1: "Hypothesis only",
            }.get(strength, "Evidence"),
            "count": len(items),
            "sources": [item.get("source", "unknown") for item in items[:3]],
            "safe_use": "Use to prioritize experiments, not to automate scientific or clinical decisions.",
        })
    return ladder
