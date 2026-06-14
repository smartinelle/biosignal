def retrieve_evidence(structured: dict, hypotheses: list[dict]) -> list[dict]:
    """Curated evidence/caveat cards used when live Tavily is unavailable.

    These are intentionally conservative: they motivate troubleshooting checks but
    never claim biological truth from a single run.
    """
    domain = str(structured.get("domain", "")).lower()
    text = structured.get("raw_note", "").lower()

    if "molecular assay" in domain:
        return [
            {
                "source": "MIQE qPCR guidelines (Bustin et al., Clin Chem 2009)",
                "claim": "Control behavior, inhibition checks, melt/cluster shape, and replicate spread must be resolved before interpreting target abundance.",
                "caveat": "Reporting/QC standard; does not establish gene-expression truth from one compromised run.",
                "url": "https://doi.org/10.1373/clinchem.2008.112797",
            },
            {
                "source": "General molecular assay QC practice",
                "claim": "NTC, no-RT, positive-control, dilution, and alternate-primer checks separate contamination, inhibition, design, and setup failures.",
                "caveat": "The specific failure mode still requires direct controls in the same assay context.",
            },
        ]

    if "protein expression" in domain:
        return [
            {
                "source": "Protein purification troubleshooting heuristics",
                "claim": "Yield loss should be localized by fraction audit before changing expression or purification conditions.",
                "caveat": "SDS-PAGE, SEC, DLS, and activity data each observe different failure modes; none alone establishes functional adequacy.",
            },
            {
                "source": "Process development QC practice",
                "claim": "Aggregation, extra bands, and changed induction/buffer conditions can point to expression, proteolysis, recovery, or stability bottlenecks.",
                "caveat": "Requires stage-wise comparison to identify the loss point.",
            },
        ]

    if "cell culture" in domain:
        return [
            {
                "source": "Cell culture troubleshooting heuristics",
                "claim": "Growth and morphology drift can reflect media lot, environment, contamination, thaw stress, passage drift, or handling effects.",
                "caveat": "Do not infer contamination or biological drift without direct testing and reference comparison.",
            },
            {
                "source": "Cell line use guidelines (Geraghty et al., Br J Cancer 2014)",
                "claim": "Mycoplasma/contamination checks, media-lot comparison, incubator review, and reference-stock comparison are high-leverage first checks.",
                "caveat": "These checks narrow uncertainty; they do not establish line quality or suitability by themselves.",
                "url": "https://doi.org/10.1038/bjc.2014.166",
            },
        ]

    if "bioprocess" in domain:
        return [
            {
                "source": "Bioprocess troubleshooting heuristics",
                "claim": "Titer, DO, pH/base demand, off-gas, feed, and foam trends can reflect sensor, process-control, feed, contamination, or biology shifts.",
                "caveat": "Research guidance only; does not establish batch disposition, release readiness, or process acceptability.",
            },
            {
                "source": "Process monitoring QC practice",
                "claim": "Sensor calibration, event-timestamp overlays, pump/feed audits, and historical-batch comparison are useful first discriminators.",
                "caveat": "The run still needs domain-owner review before any process intervention.",
            },
        ]

    if any(token in text for token in ["potency assay", "positive control", "plate edge", "edge wells", "reagent lot"]):
        return [
            {
                "source": "Preclinical reproducibility standards (Begley & Ellis, Nature 2012)",
                "claim": "Conflicting controls, edge-well effects, and reagent-lot changes often indicate technical or procedural causes that must be resolved before interpreting a biological effect.",
                "caveat": "Supports the workflow; does not invalidate or accept this specific run — recommend discriminating checks instead.",
                "url": "https://doi.org/10.1038/483531a",
            },
            {
                "source": "Reproducibility survey (Baker, Nature 2016)",
                "claim": "Irreproducibility and failed replication in preclinical research are often driven by protocol, reagent, model, and analysis variability.",
                "caveat": "Motivates the workflow, but does not identify the cause in this specific assay.",
                "url": "https://doi.org/10.1038/533452a",
            },
        ]
    return [
        {
            "source": "Madissoon et al., Tissue Stability Cell Atlas (Genome Biology 2020) / PRJEB31843",
            "claim": "Cold-preserved human lung, spleen and esophagus scRNA-seq showed relative stability up to ~24h, with stronger degradation/quality signals by 72h in some tissues.",
            "caveat": "Indirect evidence: not necessarily the same organ, protocol, or decision context. Use as hypothesis support, not prediction.",
            "url": "https://doi.org/10.1186/s13059-019-1906-x",
        },
        {
            "source": "General preservation physiology",
            "claim": "Macro variables such as lactate, pH, oxygenation and resistance can indicate tissue stress but are underdetermined without context and trend data.",
            "caveat": "Cannot infer molecular state from one snapshot; trend and assay data matter.",
        },
    ]
