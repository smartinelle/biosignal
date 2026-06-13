def retrieve_evidence(structured: dict, hypotheses: list[dict]) -> list[dict]:
    # MVP uses curated evidence; Tavily integration should replace/augment this.
    text = structured.get("raw_note", "").lower()
    if any(token in text for token in ["potency assay", "positive control", "plate edge", "edge wells", "reagent lot"]):
        return [
            {
                "source": "Assay troubleshooting heuristics",
                "claim": "Conflicting controls, edge-well effects, and reagent-lot changes often indicate technical or procedural causes that must be resolved before interpreting a biological effect.",
                "caveat": "Heuristic support only; the system should recommend discriminating checks rather than invalidate or accept the run automatically.",
            },
            {
                "source": "General biotech R&D reproducibility literature",
                "claim": "Irreproducibility and failed replication in preclinical research are often driven by protocol, reagent, model, and analysis variability.",
                "caveat": "Motivates the workflow, but does not identify the cause in this specific assay.",
            },
        ]
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
