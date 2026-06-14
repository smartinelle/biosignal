"""Curated multi-node decision tree for the ex-vivo tissue preservation workflow.

This is the "investigation plan" the agents generate upfront: a branching tree of
decision nodes that ends in a concrete resolution. As the operator records each
measurement outcome, the workflow advances along an edge to the next decision
node and the tree updates live — until it reaches a terminal resolution.

Each non-terminal node has: a question, the discriminating measurement to run,
supporting literature, and the possible outcomes (edges to the next node).
Terminal nodes carry a resolution: leading mechanism, confirmatory assay,
molecular targets to verify, and the human-review boundary.
"""

from __future__ import annotations

# Real, verifiable references used as inline support at the relevant nodes.
_MADISSOON = {"source": "Madissoon et al., Tissue Stability Cell Atlas (Genome Biology 2020)",
              "url": "https://doi.org/10.1186/s13059-019-1906-x", "tier": "peer-reviewed"}
_ELTZSCHIG = {"source": "Eltzschig & Eckle, Ischemia and reperfusion (Nature Medicine 2011)",
              "url": "https://doi.org/10.1038/nm.2507", "tier": "peer-reviewed"}
_NASRALLA = {"source": "Nasralla et al., Normothermic preservation trial (Nature 2018)",
             "url": "https://doi.org/10.1038/s41586-018-0047-9", "tier": "peer-reviewed"}

TISSUE_PRESERVATION = {
    "id": "tissue_preservation",
    "title": "Ex-vivo tissue preservation — ambiguous decline at 48h cold storage",
    "context": (
        "Ex vivo preserved tissue, 48h cold (4°C) storage. Macro signals: lactate rising, "
        "pH falling, vascular resistance increasing, oxygenation uncertain. Goal: find the "
        "leading molecular/physiological mechanism and the next discriminating measurement — "
        "without making a clinical viability claim."
    ),
    "root": "n1",
    "nodes": {
        "n1": {
            "id": "n1",
            "question": "Are the rising lactate and falling pH real metabolic signals, or measurement artifact?",
            "test": "Re-measure perfusate lactate and pH with freshly calibrated sensors against a paired reference sample; review sensor-drift logs.",
            "evidence": [_NASRALLA],
            "options": [
                {"key": "real", "edge": "Signals are real", "label": "Confirmed — signals are real (metabolic stress)", "next": "n2"},
                {"key": "artifact", "edge": "Artifact", "label": "Artifact — sensor drift / sampling error", "next": "r_artifact"},
            ],
        },
        "n2": {
            "id": "n2",
            "question": "Is the metabolic stress driven by oxygen-delivery limitation or intrinsic mitochondrial dysfunction?",
            "test": "Run a perfusion flow challenge; compare oxygen extraction, vascular resistance, and the lactate/pyruvate ratio.",
            "evidence": [_ELTZSCHIG],
            "options": [
                {"key": "o2", "edge": "O₂-delivery limited", "label": "Oxygen-delivery limited (high resistance, responds to flow)", "next": "n3"},
                {"key": "mito", "edge": "Mitochondrial", "label": "Mitochondrial dysfunction (no flow response, high L/P ratio)", "next": "n4"},
            ],
        },
        "n3": {
            "id": "n3",
            "question": "Is the oxygen-delivery limit from endothelial/vascular injury, or a mechanical perfusion-setup issue?",
            "test": "Compare vascular resistance vs perfusion pressure trend; assay endothelial injury markers (e.g. syndecan-1) and review histology.",
            "evidence": [_ELTZSCHIG, _MADISSOON],
            "options": [
                {"key": "endothelial", "edge": "Endothelial injury", "label": "Endothelial injury indicated", "next": "r_vascular"},
                {"key": "mechanical", "edge": "Setup issue", "label": "Mechanical / perfusion-setup issue", "next": "r_mechanical"},
            ],
        },
        "n4": {
            "id": "n4",
            "question": "Confirm intrinsic mitochondrial dysfunction vs time-driven tissue/RNA degradation?",
            "test": "Measure mitochondrial membrane potential / respiration (high-resolution respirometry); pair with scRNA-seq QC for degradation signatures.",
            "evidence": [_MADISSOON],
            "options": [
                {"key": "mito_confirmed", "edge": "Mito dysfunction", "label": "Mitochondrial dysfunction confirmed", "next": "r_mito"},
                {"key": "degradation", "edge": "Tissue degradation", "label": "Predominantly time-driven tissue/RNA degradation", "next": "r_degradation"},
            ],
        },
        # ---- Terminal resolutions ----
        "r_artifact": {
            "id": "r_artifact",
            "resolution": {
                "headline": "Resolved: measurement artifact",
                "leading_mechanism": "No real metabolic decline — sensor drift / sampling error.",
                "confirmatory_assay": "Recalibrate sensors, re-baseline, and repeat the readout before any further interpretation.",
                "molecular_targets": [],
                "human_review": "Confirm the recalibration with a senior scientist; no molecular escalation needed.",
            },
        },
        "r_vascular": {
            "id": "r_vascular",
            "resolution": {
                "headline": "Resolved: endothelial / vascular injury",
                "leading_mechanism": "Endothelial and vascular injury during cold preservation raising resistance and limiting O₂ delivery.",
                "confirmatory_assay": "Endothelial injury panel + histology; optimize perfusion and re-test resistance.",
                "molecular_targets": ["syndecan-1 (glycocalyx)", "VCAM-1 / ICAM-1", "endothelial apoptosis markers"],
                "human_review": "A senior scientist must confirm the injury interpretation before any protocol change.",
            },
        },
        "r_mechanical": {
            "id": "r_mechanical",
            "resolution": {
                "headline": "Resolved: mechanical / perfusion-setup limitation",
                "leading_mechanism": "Cannulation / pressure / circuit issue limiting delivery — not primarily biology.",
                "confirmatory_assay": "Optimize cannulation and pressure; re-run the flow challenge before molecular escalation.",
                "molecular_targets": [],
                "human_review": "Confirm the setup fix resolves resistance before drawing biological conclusions.",
            },
        },
        "r_mito": {
            "id": "r_mito",
            "resolution": {
                "headline": "Resolved: mitochondrial dysfunction / cold-ischemic injury",
                "leading_mechanism": "Intrinsic mitochondrial dysfunction from cold ischemia, driving anaerobic metabolism.",
                "confirmatory_assay": "High-resolution respirometry + ATP/ADP ratio; consider a mito-protective intervention study.",
                "molecular_targets": ["membrane potential", "complex I / IV activity", "ROS / oxidative-stress markers"],
                "human_review": "A senior scientist must confirm before treating this as the operative mechanism.",
            },
        },
        "r_degradation": {
            "id": "r_degradation",
            "resolution": {
                "headline": "Resolved: time-driven tissue / RNA degradation",
                "leading_mechanism": "Cumulative cold-storage degradation (consistent with stronger signals beyond ~24–72h).",
                "confirmatory_assay": "scRNA-seq QC (RNA integrity, ambient RNA) and cell-type composition shift vs a fresh control.",
                "molecular_targets": ["RNA integrity (RIN)", "stress / apoptosis programs", "cell-type-specific dropout"],
                "human_review": "Confirm degradation signatures with a senior scientist before concluding.",
            },
        },
    },
}

WORKFLOWS = {"tissue_preservation": TISSUE_PRESERVATION}


def get_workflow(workflow_id: str = "tissue_preservation") -> dict:
    return WORKFLOWS.get(workflow_id, TISSUE_PRESERVATION)


def is_terminal(node: dict) -> bool:
    return "resolution" in node
