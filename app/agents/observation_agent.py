def structure_observation(text: str) -> dict:
    lower = text.lower()
    signals = []
    signal_tokens = [
        # generic / living-system signals
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
        "marker",
        "assay",
        "potency",
        "cell count",
        "positive control",
        "control",
        "plate edge",
        "edge wells",
        "reagent",
        "lot",
        "protocol",
        # molecular-assay (qPCR/ddPCR) signals
        "ct value",
        "melt curve",
        "amplification",
        "no-template",
        "primer",
        "template",
        "rna integrity",
        # protein / process signals
        "yield",
        "sds-page",
        "sec",
        "aggregation",
        "induction",
        # cell-culture signals
        "confluency",
        "confluence",
        "incubator",
        "co2",
        "passage",
        "thaw",
        "mycoplasma",
        # bioprocess signals
        "titer",
        "off-gas",
        "dissolved oxygen",
        "feed",
        "foam",
        "inoculum",
        "operator",
    ]
    for token in signal_tokens:
        if token in lower:
            signals.append(token)

    domain = _classify_domain(lower)

    return {
        "domain": domain,
        "raw_note": text,
        "signals_detected": signals,
        "workflow_goal": "Troubleshoot an ambiguous biotech experiment and choose the next best measurement.",
        "commercial_job": "Reduce wasted experimental cycles by narrowing uncertainty before the team runs the next assay.",
        "uncertainty": "high",
        "safety_scope": "Research workflow only — not diagnosis, treatment, viability prediction, or clinical decision support.",
    }


def _classify_domain(lower: str) -> str:
    """Single source of truth for the workflow domain.

    Ordered most-specific first so the broad new R&D workflows are recognised
    before the original assay/living-system branches. Downstream agents read
    ``structured['domain']`` so every agent agrees on the workflow.
    """
    if _any(lower, ["qpcr", "ddpcr", "ct value", "melt curve", "amplification",
                    "no-template", "ntc", "primer", "rt inhibition"]):
        return "molecular assay (qPCR/ddPCR) troubleshooting"
    if _any(lower, ["recombinant", "protein yield", "sds-page", "sec ", "chromatogram",
                    "purification", "induction", "aggregation", "inclusion bod"]):
        return "protein expression / purification R&D"
    if _any(lower, ["bioreactor", "fermentation", "titer", "off-gas", "dissolved oxygen",
                    "inoculum"]):
        return "bioprocess / fermentation deviation"
    if _any(lower, ["cell culture", "passage", "confluency", "confluence", "incubator",
                    "co2", "thaw", "media lot", "mycoplasma"]):
        return "cell culture / media & environment troubleshooting"
    if _any(lower, ["potency assay", "cell-based", "plate edge", "edge wells",
                    "positive control", "reagent lot"]):
        return "biotech R&D assay troubleshooting"
    if _any(lower, ["organoid", "organ-on-chip", "tissue engineering"]):
        return "living tissue R&D / tissue engineering QC"
    if _any(lower, ["tissue", "preservation", "cold", "perfusion"]):
        return "ex-vivo tissue state / preservation R&D"
    return "biotech experiment troubleshooting"


def _any(text: str, tokens: list[str]) -> bool:
    return any(token in text for token in tokens)
