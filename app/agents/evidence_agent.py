def retrieve_evidence(structured: dict, hypotheses: list[dict]) -> list[dict]:
    # MVP uses curated evidence; Tavily integration should replace/augment this.
    return [
        {
            "source": "Madissoon et al., Tissue Stability Cell Atlas / PRJEB31843",
            "claim": "Cold-preserved human lung, spleen and esophagus scRNA-seq showed relative stability up to ~24h, with stronger degradation/quality signals by 72h in some tissues.",
            "caveat": "Indirect evidence: not necessarily the same organ, protocol, or decision context. Use as hypothesis support, not prediction.",
        },
        {
            "source": "General preservation physiology",
            "claim": "Macro variables such as lactate, pH, oxygenation and resistance can indicate tissue stress but are underdetermined without context and trend data.",
            "caveat": "Cannot infer molecular state from one snapshot; trend and assay data matter.",
        },
    ]
