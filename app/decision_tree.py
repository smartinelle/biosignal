"""Decision-tree investigations for BioSignal Navigator.

Two sources of trees, same schema and engine:

1. A curated demo tree for ex-vivo tissue preservation — a coherent, branching
   investigation generated upfront (4 decision nodes -> 5 resolutions). This is a
   *demo dataset*, not the only possible query.
2. ``build_dynamic_tree`` turns any pipeline result (from any note) into a
   branching tree, so an arbitrary query is always supported.

Node schema
-----------
Decision node:
  id, question, test, rationale (why this measurement discriminates),
  evidence: [{source, url, tier, why}], options: [{key, edge, label, desc, next}]
Terminal node:
  id, resolution: {headline, leading_mechanism, confirmatory_assay,
                   molecular_targets, human_review}
"""

from __future__ import annotations

# Real, verifiable references; ``why`` is attached per node (it differs by step).
_MADISSOON = {"source": "Madissoon et al., Tissue Stability Cell Atlas (Genome Biology 2020)",
              "url": "https://doi.org/10.1186/s13059-019-1906-x", "tier": "peer-reviewed"}
_ELTZSCHIG = {"source": "Eltzschig & Eckle, Ischemia and reperfusion (Nature Medicine 2011)",
              "url": "https://doi.org/10.1038/nm.2507", "tier": "peer-reviewed"}
_NASRALLA = {"source": "Nasralla et al., Normothermic preservation trial (Nature 2018)",
             "url": "https://doi.org/10.1038/s41586-018-0047-9", "tier": "peer-reviewed"}


def _ref(base: dict, why: str) -> dict:
    return {**base, "why": why}


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
            "rationale": "A calibrated re-measure against a control separates a true metabolic signal from a sensor/sampling artifact before you spend further experiments.",
            "evidence": [_ref(_NASRALLA,
                              "Nasralla et al. used lactate clearance as a viability readout in machine perfusion — so confirming the lactate/pH signal is real is the right first step.")],
            "options": [
                {"key": "real", "edge": "Signals real", "label": "Signals are REAL (calibrated re-measure agrees)",
                 "desc": "Re-measured lactate/pH match the originals with calibrated sensors → the metabolic decline is real.", "next": "n2"},
                {"key": "artifact", "edge": "Artifact", "label": "ARTIFACT (calibrated re-measure disagrees)",
                 "desc": "Calibrated re-measurement disagrees with the originals → it was sensor drift or a sampling error.", "next": "r_artifact"},
            ],
        },
        "n2": {
            "id": "n2",
            "question": "Is the metabolic stress driven by oxygen-delivery limitation or intrinsic mitochondrial dysfunction?",
            "test": "Run a perfusion flow challenge; compare oxygen extraction, vascular resistance, and the lactate/pyruvate ratio.",
            "rationale": "A flow challenge plus lactate/pyruvate tells supply-limitation apart from intrinsic mitochondrial failure — they need different follow-ups.",
            "evidence": [_ref(_ELTZSCHIG,
                              "This ischemia–reperfusion review distinguishes oxygen-supply limitation from intrinsic mitochondrial injury, motivating the flow challenge.")],
            "options": [
                {"key": "o2", "edge": "O₂-delivery limited", "label": "OXYGEN-DELIVERY limited (responds to flow)",
                 "desc": "Resistance is high and improves when you raise flow, with a near-normal lactate/pyruvate ratio → oxygen delivery is the limit.", "next": "n3"},
                {"key": "mito", "edge": "Mitochondrial", "label": "MITOCHONDRIAL dysfunction (no flow response)",
                 "desc": "No improvement with flow and a high lactate/pyruvate ratio → intrinsic mitochondrial dysfunction.", "next": "n4"},
            ],
        },
        "n3": {
            "id": "n3",
            "question": "Is the oxygen-delivery limit from endothelial/vascular injury, or a mechanical perfusion-setup issue?",
            "test": "Compare vascular resistance vs perfusion pressure trend; assay endothelial injury markers (e.g. syndecan-1) and review histology.",
            "rationale": "Comparing resistance vs pressure and assaying endothelial markers separates biological injury from a mechanical perfusion problem.",
            "evidence": [
                _ref(_ELTZSCHIG, "Endothelial dysfunction is central to ischemia–reperfusion injury, motivating endothelial markers + histology."),
                _ref(_MADISSOON, "Shows cold-storage degradation accrues by ~72h — relevant when judging vascular/tissue injury at 48h."),
            ],
            "options": [
                {"key": "endothelial", "edge": "Endothelial injury", "label": "ENDOTHELIAL injury indicated",
                 "desc": "Resistance rises out of proportion to pressure and endothelial markers/histology show injury.", "next": "r_vascular"},
                {"key": "mechanical", "edge": "Setup issue", "label": "MECHANICAL / setup issue",
                 "desc": "Resistance tracks the circuit/cannulation and injury markers are clean → a setup issue, not biology.", "next": "r_mechanical"},
            ],
        },
        "n4": {
            "id": "n4",
            "question": "Confirm intrinsic mitochondrial dysfunction vs time-driven tissue/RNA degradation?",
            "test": "Measure mitochondrial membrane potential / respiration (high-resolution respirometry); pair with scRNA-seq QC for degradation signatures.",
            "rationale": "Respirometry vs scRNA-seq QC distinguishes active mitochondrial dysfunction from passive time-driven degradation.",
            "evidence": [_ref(_MADISSOON,
                              "Documents time-dependent transcriptomic degradation in cold-stored tissue — the comparator for telling degradation apart from mitochondrial dysfunction.")],
            "options": [
                {"key": "mito_confirmed", "edge": "Mito dysfunction", "label": "MITOCHONDRIAL dysfunction confirmed",
                 "desc": "Respirometry shows reduced membrane potential/respiration → mitochondrial dysfunction confirmed.", "next": "r_mito"},
                {"key": "degradation", "edge": "Tissue degradation", "label": "Time-driven DEGRADATION",
                 "desc": "Respiration is preserved but scRNA-seq QC shows degradation signatures → time-driven tissue/RNA degradation.", "next": "r_degradation"},
            ],
        },
        "r_artifact": {"id": "r_artifact", "resolution": {
            "headline": "Resolved: measurement artifact",
            "leading_mechanism": "No real metabolic decline — sensor drift / sampling error.",
            "confirmatory_assay": "Recalibrate sensors, re-baseline, and repeat the readout before any further interpretation.",
            "molecular_targets": [],
            "human_review": "Confirm the recalibration with a senior scientist; no molecular escalation needed."}},
        "r_vascular": {"id": "r_vascular", "resolution": {
            "headline": "Resolved: endothelial / vascular injury",
            "leading_mechanism": "Endothelial and vascular injury during cold preservation raising resistance and limiting O₂ delivery.",
            "confirmatory_assay": "Endothelial injury panel + histology; optimize perfusion and re-test resistance.",
            "molecular_targets": ["syndecan-1 (glycocalyx)", "VCAM-1 / ICAM-1", "endothelial apoptosis markers"],
            "human_review": "A senior scientist must confirm the injury interpretation before any protocol change."}},
        "r_mechanical": {"id": "r_mechanical", "resolution": {
            "headline": "Resolved: mechanical / perfusion-setup limitation",
            "leading_mechanism": "Cannulation / pressure / circuit issue limiting delivery — not primarily biology.",
            "confirmatory_assay": "Optimize cannulation and pressure; re-run the flow challenge before molecular escalation.",
            "molecular_targets": [],
            "human_review": "Confirm the setup fix resolves resistance before drawing biological conclusions."}},
        "r_mito": {"id": "r_mito", "resolution": {
            "headline": "Resolved: mitochondrial dysfunction / cold-ischemic injury",
            "leading_mechanism": "Intrinsic mitochondrial dysfunction from cold ischemia, driving anaerobic metabolism.",
            "confirmatory_assay": "High-resolution respirometry + ATP/ADP ratio; consider a mito-protective intervention study.",
            "molecular_targets": ["membrane potential", "complex I / IV activity", "ROS / oxidative-stress markers"],
            "human_review": "A senior scientist must confirm before treating this as the operative mechanism."}},
        "r_degradation": {"id": "r_degradation", "resolution": {
            "headline": "Resolved: time-driven tissue / RNA degradation",
            "leading_mechanism": "Cumulative cold-storage degradation (consistent with stronger signals beyond ~24–72h).",
            "confirmatory_assay": "scRNA-seq QC (RNA integrity, ambient RNA) and cell-type composition shift vs a fresh control.",
            "molecular_targets": ["RNA integrity (RIN)", "stress / apoptosis programs", "cell-type-specific dropout"],
            "human_review": "Confirm degradation signatures with a senior scientist before concluding."}},
    },
}

WORKFLOWS = {"tissue_preservation": TISSUE_PRESERVATION}


def get_workflow(workflow_id: str = "tissue_preservation") -> dict:
    return WORKFLOWS.get(workflow_id, TISSUE_PRESERVATION)


def is_terminal(node: dict) -> bool:
    return "resolution" in node


def build_dynamic_tree(result: dict) -> dict:
    """Turn any pipeline result into a branching decision tree (rule-of-elimination).

    Each ranked hypothesis becomes a decision node: run its discriminating test and
    report whether the result supports or weakens it. 'Supports' resolves to that
    mechanism; 'weakens' falls through to the next hypothesis, ending in an
    'inconclusive / escalate' resolution.
    """
    branches = result.get("uncertainty_map", {}).get("branches", [])[:3]
    measurements = result.get("measurements", [])
    structured = result.get("structured_observations", {})
    ev_src = result.get("evidence", [])[:2]
    evidence = [
        _ref(
            {"source": e.get("source", "evidence"), "url": e.get("url", ""),
             "tier": e.get("source_tier") or e.get("evidence_type", "")},
            "Retrieved for this workflow — use it to judge whether the measurement supports this mechanism.",
        )
        for e in ev_src
    ]

    nodes: dict[str, dict] = {}
    n = len(branches)
    for i, b in enumerate(branches):
        nid = f"n{i + 1}"
        res_id = f"r{i + 1}"
        weak_next = f"n{i + 2}" if (i + 1) < n else "r_inconclusive"
        confirm_assay = measurements[i]["measurement"] if i < len(measurements) else b.get("test", "an orthogonal check")
        nodes[nid] = {
            "id": nid,
            "question": f"Does the measurement support this explanation: {b['hypothesis']}?",
            "test": b.get("test", "Run the discriminating control for this hypothesis."),
            "rationale": b.get("what_would_change_our_mind", "This test separates the leading explanation from the alternatives."),
            "evidence": evidence,
            "options": [
                {"key": "supports", "edge": "Supports", "label": f"SUPPORTS — consistent with {b['hypothesis']}",
                 "desc": f"The measurement is consistent with {b['hypothesis'].lower()}.", "next": res_id},
                {"key": "weakens", "edge": "Weakens", "label": "WEAKENS — argues against this",
                 "desc": "The result argues against this explanation; move on to the next hypothesis.", "next": weak_next},
            ],
        }
        nodes[res_id] = {"id": res_id, "resolution": {
            "headline": f"Resolved: {b['hypothesis']}",
            "leading_mechanism": b.get("why_plausible", b["hypothesis"]),
            "confirmatory_assay": confirm_assay,
            "molecular_targets": [],
            "human_review": "A senior scientist must confirm before treating this as the operative mechanism.",
        }}

    if not nodes:
        nodes["n1"] = {"id": "n1",
                       "question": "Collect a minimal control/baseline to make the run interpretable?",
                       "test": "Gather the missing controls and baseline context, then re-investigate.",
                       "rationale": "The note lacks enough structured observations for a stronger plan.",
                       "evidence": evidence,
                       "options": [{"key": "collected", "edge": "Collected", "label": "Controls/baseline collected",
                                    "desc": "You now have enough context to re-run the investigation.", "next": "r_inconclusive"}]}

    nodes["r_inconclusive"] = {"id": "r_inconclusive", "resolution": {
        "headline": "Resolved: inconclusive — escalate",
        "leading_mechanism": "No single explanation was supported by the measurements.",
        "confirmatory_assay": "Collect missing controls/baseline or run an orthogonal check, then re-investigate.",
        "molecular_targets": [],
        "human_review": "Escalate to a senior scientist to choose the next orthogonal measurement.",
    }}

    return {
        "id": "custom",
        "title": f"Investigation — {structured.get('domain', 'custom experiment')}",
        "context": structured.get("raw_note", ""),
        "root": "n1",
        "nodes": nodes,
    }
