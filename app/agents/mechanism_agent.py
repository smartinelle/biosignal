# Curated candidate mechanisms for the broad biotech R&D workflows. Keyed by the
# domain string from observation_agent so every agent reasons about the same case.
# These are POSSIBLE mechanisms, never claims of ground truth.
_DOMAIN_MECHANISMS = {
    "molecular assay (qPCR/ddPCR)": [
        {"mechanism": "Contamination / carryover", "rationale": "No-template control amplification points to template or environmental contamination rather than true signal."},
        {"mechanism": "Primer-dimer / non-specific amplification", "rationale": "A melt-curve shoulder suggests off-target or primer-dimer products inflating or distorting signal."},
        {"mechanism": "Degraded template / low RNA integrity", "rationale": "Late Ct with borderline RNA integrity is consistent with degraded or low-quality template."},
        {"mechanism": "RT inhibition / inhibitors in extract", "rationale": "Inhibitors carried through extraction can delay Ct without reflecting real abundance."},
        {"mechanism": "Pipetting / setup error", "rationale": "Intermittent control failure with a new operator points to handling or setup variability."},
    ],
    "protein expression / purification": [
        {"mechanism": "Low or burdened expression", "rationale": "An induction change can reduce expression independently of downstream recovery."},
        {"mechanism": "Proteolysis / degradation", "rationale": "Extra SDS-PAGE bands are consistent with proteolytic clipping during expression or purification."},
        {"mechanism": "Aggregation / misfolding", "rationale": "A new SEC shoulder with rising DLS aggregation suggests misfolding or instability, not just yield loss."},
        {"mechanism": "Purification recovery loss", "rationale": "Resin saturation, binding, or wash conditions can lose product without an expression problem."},
        {"mechanism": "pH-driven instability / storage", "rationale": "Lower buffer pH can shift solubility and aggregation between purification and analysis."},
    ],
    "cell culture / media & environment": [
        {"mechanism": "Media lot / formulation shift", "rationale": "A recent media-lot change can alter growth and morphology independent of the cells."},
        {"mechanism": "Incubator drift / CO2-pH excursion", "rationale": "A logged CO2 excursion can shift media pH and stress the culture transiently or persistently."},
        {"mechanism": "Low-grade contamination", "rationale": "Slow growth and morphology change after a media/handling change can reflect mycoplasma or bacterial contamination."},
        {"mechanism": "Freeze/thaw recovery stress", "rationale": "Post-thaw cultures often lag; inconsistent passages can reflect incomplete recovery."},
        {"mechanism": "Passage-related drift", "rationale": "Accumulated passage changes or senescence can shift behavior across passages."},
    ],
    "bioprocess / fermentation": [
        {"mechanism": "Oxygen-transfer limitation", "rationale": "A mid-run DO drop suggests aeration/agitation or oxygen-demand mismatch limiting the culture."},
        {"mechanism": "Feed strategy / nutrient limitation", "rationale": "Off-gas divergence after a feed change is consistent with a feeding or nutrient limitation."},
        {"mechanism": "Sensor calibration drift", "rationale": "Extra base demand and pH/DO behavior can reflect probe drift rather than true biology."},
        {"mechanism": "Contamination", "rationale": "Atypical off-gas and base demand can indicate a contaminating organism."},
        {"mechanism": "Strain instability / metabolic overflow", "rationale": "Productivity loss can reflect strain instability or overflow metabolism under the run conditions."},
    ],
}


def infer_mechanisms(structured: dict) -> list[dict]:
    domain = str(structured.get("domain", "")).lower()
    for key, mechanisms in _DOMAIN_MECHANISMS.items():
        if key.lower() in domain:
            return mechanisms[:5]

    # Original keyword-driven logic for the assay and living-system workflows.
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
