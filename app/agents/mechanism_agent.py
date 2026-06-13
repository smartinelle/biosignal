def infer_mechanisms(structured: dict) -> list[dict]:
    text = structured["raw_note"].lower()
    hypotheses = []
    if "lactate" in text or "ph" in text:
        hypotheses.append({"mechanism": "Hypoxia / anaerobic metabolism", "rationale": "Rising lactate or falling pH can reflect metabolic stress, but is not specific."})
    if "resistance" in text or "perfusion" in text:
        hypotheses.append({"mechanism": "Endothelial or vascular dysfunction", "rationale": "Increased resistance can indicate vascular tone, edema, microthrombi, or endothelial injury."})
    if "cold" in text or "48h" in text or "72h" in text:
        hypotheses.append({"mechanism": "Mitochondrial stress / cold ischemic injury", "rationale": "Long preservation can create cell-type-specific stress and quality degradation."})
    if "plate edge" in text or "edge wells" in text:
        hypotheses.append({"mechanism": "Plate artifact / edge effect", "rationale": "Spatially worse edge wells often indicate evaporation, temperature gradients, handling, or plate-layout artifacts rather than true biology."})
    if "reagent" in text or "lot" in text:
        hypotheses.append({"mechanism": "Reagent lot or stability issue", "rationale": "A recent reagent or lot change can shift signal independently of the biological sample."})
    if "positive control" in text or "control drift" in text:
        hypotheses.append({"mechanism": "Protocol or control drift", "rationale": "Control drift suggests the assay system changed, so the test result should not be interpreted as biology until controls are resolved."})
    if "cell count" in text and ("signal" in text or "potency" in text):
        hypotheses.append({"mechanism": "Assay signal decoupled from cell number", "rationale": "Normal cell count with lower signal points toward potency/readout chemistry, protocol timing, or pathway-specific effects rather than simple cell loss."})
    hypotheses.append({"mechanism": "Inflammatory activation", "rationale": "Tissue stress often induces immune and cytokine programs; needs assay confirmation."})
    hypotheses.append({"mechanism": "Cell-type-specific degradation", "rationale": "Bulk macro signals can hide loss or stress in vulnerable cell populations."})
    return hypotheses[:5]
