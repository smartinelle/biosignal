def infer_mechanisms(structured: dict) -> list[dict]:
    text = structured["raw_note"].lower()
    hypotheses = []
    if "lactate" in text or "ph" in text:
        hypotheses.append({"mechanism": "Hypoxia / anaerobic metabolism", "rationale": "Rising lactate or falling pH can reflect metabolic stress, but is not specific."})
    if "resistance" in text or "perfusion" in text:
        hypotheses.append({"mechanism": "Endothelial or vascular dysfunction", "rationale": "Increased resistance can indicate vascular tone, edema, microthrombi, or endothelial injury."})
    if "cold" in text or "48h" in text or "72h" in text:
        hypotheses.append({"mechanism": "Mitochondrial stress / cold ischemic injury", "rationale": "Long preservation can create cell-type-specific stress and quality degradation."})
    hypotheses.append({"mechanism": "Inflammatory activation", "rationale": "Tissue stress often induces immune and cytokine programs; needs assay confirmation."})
    hypotheses.append({"mechanism": "Cell-type-specific degradation", "rationale": "Bulk macro signals can hide loss or stress in vulnerable cell populations."})
    return hypotheses[:5]
