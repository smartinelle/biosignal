def suggest_measurements(structured: dict, hypotheses: list[dict], evidence: list[dict]) -> list[dict]:
    return [
        {"measurement": "Lactate and pH trend", "why": "Separates transient metabolic shift from worsening anaerobic metabolism."},
        {"measurement": "Oxygen consumption / perfusate oxygen delta", "why": "Closer to metabolic function than static oxygenation."},
        {"measurement": "Mitochondrial stress or apoptosis marker", "why": "Tests cold ischemic / cell stress hypothesis."},
        {"measurement": "Endothelial injury marker", "why": "Tests whether rising resistance is vascular/endothelial rather than purely mechanical."},
        {"measurement": "Targeted RNA panel or scRNA-seq if research context", "why": "Checks cell-type-specific degradation hidden by macro variables."},
    ]
