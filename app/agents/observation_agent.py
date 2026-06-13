def structure_observation(text: str) -> dict:
    lower = text.lower()
    signals = []
    signal_tokens = [
        "lactate",
        "ph",
        "resistance",
        "oxygen",
        "morphology",
        "viability",
        "cold",
        "48h",
        "72h",
        "organoid",
        "tissue",
        "perfusion",
        "bioreactor",
        "marker",
        "assay",
    ]
    for token in signal_tokens:
        if token in lower:
            signals.append(token)

    if any(t in lower for t in ["organoid", "organ-on-chip", "tissue engineering", "bioreactor"]):
        domain = "living tissue R&D / tissue engineering QC"
    elif any(t in lower for t in ["tissue", "preservation", "cold", "perfusion"]):
        domain = "ex-vivo tissue state / preservation R&D"
    else:
        domain = "biotech experiment troubleshooting"

    return {
        "domain": domain,
        "raw_note": text,
        "signals_detected": signals,
        "workflow_goal": "Troubleshoot an ambiguous biotech experiment and choose the next best measurement.",
        "commercial_job": "Reduce wasted experimental cycles by narrowing uncertainty before the team runs the next assay.",
        "uncertainty": "high",
        "safety_scope": "Research workflow only — not diagnosis, treatment, viability prediction, or clinical decision support.",
    }
