"""Demo presets — the single source of truth for the BioSignal Navigator demo.

Each preset is one troubleshooting case the demo can load. The product is a
**general biotech R&D troubleshooting workspace**; these presets are concrete
use cases that prove the same loop, not separate products.

Order is intentional: broadest / most general workflows first so a first-time
viewer sees the category before the thesis-flavoured living-system cases.

Schema per preset:
- ``key``      stable identifier
- ``label``    short menu/card title
- ``category`` one-line use-case framing
- ``note``     the default experiment note loaded into the workspace

Notes are research-only by construction: they ask for the next measurement, never
for a diagnosis, viability score, or transplant/discard/batch-release decision.
"""

from __future__ import annotations

PRESETS: list[dict] = [
    {
        "key": "assay_signal_collapse",
        "label": "Assay signal collapse",
        "category": "Assay development — broadest biotech workflow",
        "note": (
            "Context: biotech R&D cell-based potency assay. Observations: signal is 40% lower "
            "than expected, cell count is normal, positive control drifted slightly, plate edge "
            "wells look worse, reagent lot changed last week. Goal: decide whether this is "
            "biology, protocol drift, reagent failure, or plate artifact before repeating the study."
        ),
    },
    {
        "key": "qpcr_amplification_anomaly",
        "label": "qPCR / ddPCR anomaly",
        "category": "Molecular biology — ubiquitous assay troubleshooting",
        "note": (
            "Context: biotech R&D molecular assay. A qPCR/ddPCR run shows Ct values about 3 cycles "
            "later than expected, the melt curve has a shoulder, no-template controls show weak "
            "amplification, and the positive control failed intermittently. RNA integrity is "
            "borderline and this extraction batch was handled by a new operator. Goal: decide "
            "whether this is contamination, primer-dimer, degraded template, RT inhibition, or "
            "pipetting error before trusting the quantification — without inferring gene-expression "
            "truth from one compromised run."
        ),
    },
    {
        "key": "protein_yield_drop",
        "label": "Protein yield / purity drop",
        "category": "Protein & process R&D",
        "note": (
            "Context: biotech R&D protein production run. Recombinant protein yield is 60% lower "
            "than baseline, SDS-PAGE shows extra bands, SEC has a new shoulder peak, and DLS "
            "indicates more aggregation. Induction temperature changed and buffer pH was slightly "
            "lower than usual. Goal: decide whether the bottleneck is expression, proteolysis, "
            "purification, or storage stability and pick the next discriminating check — without "
            "claiming protein function or usability."
        ),
    },
    {
        "key": "cell_culture_drift",
        "label": "Cell culture drift",
        "category": "Everyday wet-lab operations",
        "note": (
            "Context: biotech R&D cell culture line. After thaw, cells grew slower, morphology "
            "shifted, confluency stalled, media color changed earlier than usual, and "
            "passage-to-passage behavior is inconsistent. The media lot changed two weeks ago and "
            "incubator CO2 logs show a short excursion. Goal: decide whether this is media, "
            "environment, handling, contamination, or biology drift and choose the next check — "
            "without recommending discard or claiming contamination before direct testing."
        ),
    },
    {
        "key": "bioreactor_deviation",
        "label": "Bioreactor deviation",
        "category": "Bioprocess / fermentation R&D",
        "note": (
            "Context: biotech R&D bioprocess run. A bioreactor underperformed on titer: dissolved "
            "oxygen drifted lower mid-run, pH control required more base than usual, off-gas trends "
            "diverged from the historical batch, and foam spiked after a feed change. Goal: decide "
            "whether this is sensor drift, feed limitation, oxygen-transfer bottleneck, "
            "contamination, or strain instability and choose the next check — without claiming batch "
            "disposition or release-readiness."
        ),
    },
    {
        "key": "organoid_qc_anomaly",
        "label": "Organoid QC anomaly",
        "category": "Living-system use case",
        "note": (
            "Context: engineered organoid QC batch. Observations: abnormal morphology, borderline "
            "viability stain, media lactate rising, differentiation marker uncertain, possible "
            "hypoxic core. Goal: identify likely failure mechanisms and choose the next assays "
            "before repeating the batch."
        ),
    },
    {
        "key": "organ_on_chip_ambiguity",
        "label": "Organ-on-chip ambiguity",
        "category": "Translational R&D use case",
        "note": (
            "Context: organ-on-chip drug response experiment. Observations: unexpected barrier "
            "leak, oxygen consumption shift, inflammatory marker increase, morphology change after "
            "compound exposure. Goal: troubleshoot whether this is toxicity, protocol failure, or "
            "model instability and pick the next discriminating measurement."
        ),
    },
    {
        "key": "tissue_preservation_failure",
        "label": "Ex-vivo tissue preservation",
        "category": "Thesis anchor — living-tissue use case",
        "note": (
            "Context: ex vivo preserved tissue sample in a biotech R&D workflow. Preservation "
            "duration: 48h cold storage. Macro signals: lactate rising, pH falling, vascular "
            "resistance increasing, oxygenation uncertain. Goal: debug the experiment and decide "
            "which measurement should be run next, without making a clinical viability claim."
        ),
    },
]

# Convenience lookups for the UI.
PRESETS_BY_LABEL: dict[str, dict] = {p["label"]: p for p in PRESETS}
PRESET_LABELS: list[str] = [p["label"] for p in PRESETS]


def get_note(label: str) -> str:
    """Return the default note for a preset label (empty string if unknown)."""
    preset = PRESETS_BY_LABEL.get(label)
    return preset["note"] if preset else ""
