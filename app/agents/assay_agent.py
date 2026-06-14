# Curated next measurements for broad biotech R&D troubleshooting workflows.
# These are research follow-up checks, not decisions or claims of ground truth.
_DOMAIN_MEASUREMENTS = {
    "molecular assay (qPCR/ddPCR)": [
        {"measurement": "Dilution series plus inhibition control", "why": "Checks whether delayed Ct or droplet ambiguity improves when inhibitors are diluted."},
        {"measurement": "NTC / no-RT / positive-control repeat", "why": "Separates contamination, RT issues, and setup variability before interpreting samples."},
        {"measurement": "Alternate primer/probe or orthogonal assay", "why": "Tests whether the target signal survives a different assay design."},
        {"measurement": "Template quality and input audit", "why": "Determines whether degraded or low input template explains the shift."},
        {"measurement": "Threshold / droplet-gating review", "why": "Checks whether analysis settings are creating the apparent anomaly."},
    ],
    "protein expression / purification": [
        {"measurement": "Fraction audit across input, soluble, pellet, flow-through, wash, and elution", "why": "Locates where the protein is lost before optimizing the wrong step."},
        {"measurement": "SDS-PAGE / Western / activity comparison across stages", "why": "Separates expression, degradation, recovery, and functional-loss explanations."},
        {"measurement": "Buffer pH / salt / concentration mini-screen", "why": "Tests whether aggregation or instability is condition-driven."},
        {"measurement": "Induction-temperature pilot matrix", "why": "Checks whether the changed expression condition caused yield or folding loss."},
        {"measurement": "Protease inhibitor or mass-spec confirmation", "why": "Tests whether extra bands are degradation products or co-purifying contaminants."},
    ],
    "cell culture / media & environment": [
        {"measurement": "Mycoplasma / contamination and identity check", "why": "Rules out hidden contamination or line mismatch before interpreting phenotype."},
        {"measurement": "Fresh-vs-current media lot side-by-side", "why": "Tests whether growth and morphology track the recent lot change."},
        {"measurement": "Incubator CO2 / temperature calibration review", "why": "Checks whether environmental drift explains media color and growth changes."},
        {"measurement": "Reference-stock or early-passage comparison", "why": "Separates passage drift from transient handling or thaw stress."},
        {"measurement": "Seeding-density and passage-history audit", "why": "Targets handling variables that often masquerade as biological drift."},
    ],
    "bioprocess / fermentation": [
        {"measurement": "Sensor calibration and secondary-reading cross-check", "why": "Determines whether DO/pH behavior is real or probe-derived."},
        {"measurement": "Feed, pump, and line audit against event timestamps", "why": "Separates feed-delivery issues from culture-state changes."},
        {"measurement": "Off-gas and historical-batch overlay", "why": "Shows whether the run diverged before or after the suspected process change."},
        {"measurement": "Inoculum QC and contamination screen", "why": "Tests biological and contamination explanations for productivity loss."},
        {"measurement": "Agitation / aeration sensitivity check", "why": "Evaluates whether oxygen-transfer limitation is driving the deviation."},
    ],
}


def suggest_measurements(structured: dict, hypotheses: list[dict], evidence: list[dict]) -> list[dict]:
    domain = str(structured.get("domain", "")).lower()
    for key, measurements in _DOMAIN_MEASUREMENTS.items():
        if key.lower() in domain:
            return measurements[:5]

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
