def suggest_measurements(structured: dict, hypotheses: list[dict], evidence: list[dict]) -> list[dict]:
    text = structured.get("raw_note", "").lower()
    if any(token in text for token in ["potency assay", "positive control", "plate edge", "edge wells", "reagent lot"]):
        return [
            {"measurement": "Old-vs-new reagent lot control run", "why": "Tests whether the signal drop follows the reagent change rather than the biology."},
            {"measurement": "Edge-vs-center plate-layout analysis", "why": "Checks whether spatial artifacts explain the worse wells."},
            {"measurement": "Positive and negative control repeat", "why": "Determines whether the assay system is stable enough to interpret the sample signal."},
            {"measurement": "Orthogonal potency/readout assay", "why": "Separates true biological effect from assay-specific chemistry or protocol drift."},
            {"measurement": "Protocol timing and incubation audit", "why": "Targets a common source of drift before repeating the full study."},
        ]
    return [
        {"measurement": "Lactate and pH trend", "why": "Separates transient metabolic shift from worsening anaerobic metabolism."},
        {"measurement": "Oxygen consumption / perfusate oxygen delta", "why": "Closer to metabolic function than static oxygenation."},
        {"measurement": "Mitochondrial stress or apoptosis marker", "why": "Tests cold ischemic / cell stress hypothesis."},
        {"measurement": "Endothelial injury marker", "why": "Tests whether rising resistance is vascular/endothelial rather than purely mechanical."},
        {"measurement": "Targeted RNA panel or scRNA-seq if research context", "why": "Checks cell-type-specific degradation hidden by macro variables."},
    ]
