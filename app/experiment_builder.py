"""Custom experiment builder for general-purpose biotech troubleshooting.

This keeps BioSignal Navigator from feeling hard-coded to presets. Biotech teams
can describe their own workflow, observations, goals, and constraints; the app
turns that into the same pipeline input and decides which UI sections matter.
"""

from __future__ import annotations

from typing import Any


_FAMILY_RULES: list[dict[str, Any]] = [
    {
        "family_key": "analytical_chemistry_bioconjugation",
        "family_label": "analytical chemistry / bioconjugation troubleshooting",
        "match_tokens": ("adc", "hic", "dar", "lc-ms", "mass spec", "chromatography", "conjugation"),
        "surface_copy": "Focused on analytical chemistry / bioconjugation workflow controls, orthogonal readouts, and chemistry-vs-artifact separation.",
        "ui_labels": {
            "action_plan": "1. Ranked analytical checks",
            "uncertainty_map": "1b. Analytical uncertainty map",
            "review_mode": "1c. Analyst Review Mode",
            "memory": "4b. Analytical memory / learning loop",
            "pioneer": "4. Pioneer structured extraction layer",
        },
        "recommended_sections": [
            "analytical_controls",
            "orthogonal_readouts",
            "chemistry_artifact_split",
        ],
        "section_cards": [
            {
                "title": "Analytical controls",
                "body": "Check lot changes, calibration drift, separation quality, and method carryover before reading biology into the signal.",
            },
            {
                "title": "Orthogonal readouts",
                "body": "Pair chromatography with MS, peptide maps, or alternate purity metrics to separate conjugation chemistry from instrument artifact.",
            },
            {
                "title": "Safety boundary",
                "body": "Research workflow only; treat the output as evidence-backed hypothesis generation, not a release or disposition decision.",
            },
        ],
    },
    {
        "family_key": "molecular_assay",
        "family_label": "molecular assay troubleshooting",
        "match_tokens": ("qpcr", "ddpcr", "primer", "ct", "ntc", "pcr", "assay", "amplification"),
        "surface_copy": "Focused on assay controls, workflow contamination checks, normalization, and signal-quality recovery.",
        "ui_labels": {
            "action_plan": "1. Ranked assay controls",
            "uncertainty_map": "1b. Assay uncertainty map",
            "review_mode": "1c. Assay Review Mode",
            "memory": "4b. Assay memory / learning loop",
            "pioneer": "4. Pioneer structured extraction layer",
        },
        "recommended_sections": [
            "control_matrix",
            "normalization_checks",
            "contamination_and_replication",
        ],
        "section_cards": [
            {
                "title": "Control matrix",
                "body": "Check positive controls, NTCs, and reference targets before inferring a biological shift.",
            },
            {
                "title": "Normalization checks",
                "body": "Inspect Ct shifts, thresholding, and replicate spread to distinguish true change from assay instability.",
            },
            {
                "title": "Safety boundary",
                "body": "Keep the output in research troubleshooting terms and escalate uncertain calls to a human reviewer.",
            },
        ],
    },
    {
        "family_key": "bioprocess",
        "family_label": "bioprocess troubleshooting",
        "match_tokens": ("bioreactor", "fermentation", "titer", "off-gas", "feed", "harvest", "scale-up", "process"),
        "surface_copy": "Focused on bioprocess workflow drift, feed strategy, scale-up effects, and orthogonal process checks.",
        "ui_labels": {
            "action_plan": "1. Ranked process checks",
            "uncertainty_map": "1b. Process uncertainty map",
            "review_mode": "1c. Process Review Mode",
            "memory": "4b. Process memory / learning loop",
            "pioneer": "4. Pioneer structured extraction layer",
        },
        "recommended_sections": [
            "process_timeline",
            "feed_and_offgas",
            "scale_up_drift",
        ],
        "section_cards": [
            {
                "title": "Process timeline",
                "body": "Look for step changes in feed, pH, DO, agitation, or temperature that line up with the anomaly.",
            },
            {
                "title": "Scale-up drift",
                "body": "Compare vessel-to-vessel differences and orthogonal process signals before attributing the issue to biology.",
            },
            {
                "title": "Safety boundary",
                "body": "Frame recommendations as process troubleshooting and human review, not final batch disposition.",
            },
        ],
    },
    {
        "family_key": "living_tissue_systems",
        "family_label": "living tissue system troubleshooting",
        "match_tokens": ("organoid", "organ-on-chip", "tissue", "perfusion", "ex-vivo", "ex vivo", "preservation"),
        "surface_copy": "Focused on living tissue system workflow perfusion, tissue-state readouts, paired controls, and the next discriminating measurement.",
        "ui_labels": {
            "action_plan": "1. Ranked tissue-state measurements",
            "uncertainty_map": "1b. Tissue uncertainty map",
            "review_mode": "1c. Scientist Review Mode",
            "memory": "4b. Tissue memory / learning loop",
            "pioneer": "4. Pioneer structured extraction layer",
        },
        "recommended_sections": [
            "perfusion_and_viability_controls",
            "tissue_state_readouts",
            "paired_controls_and_human_review",
        ],
        "section_cards": [
            {
                "title": "Perfusion and viability controls",
                "body": "Treat oxygenation, temperature, flow, and preservation duration as the first control panel, not the conclusion.",
            },
            {
                "title": "Tissue-state readouts",
                "body": "Pair macro readouts with histology, transcriptomics, or metabolite evidence to decide which mechanism deserves attention next.",
            },
            {
                "title": "Safety boundary",
                "body": "Research use only — the app suggests hypotheses and measurements, while human review keeps the final judgment.",
            },
        ],
    },
    {
        "family_key": "custom",
        "family_label": "custom biotech R&D troubleshooting",
        "match_tokens": (),
        "surface_copy": "Custom workflow detected. Keep the problem statement broad, the controls explicit, and the next measurement discriminating.",
        "ui_labels": {
            "action_plan": "1. Recommended next actions",
            "uncertainty_map": "1b. Uncertainty map",
            "review_mode": "1c. Scientist Review Mode",
            "memory": "4b. Experiment memory / learning loop",
            "pioneer": "4. Pioneer structured extraction layer",
        },
        "recommended_sections": ["evidence_quality", "uncertainty_map", "scientist_review"],
        "section_cards": [
            {
                "title": "Workflow framing",
                "body": "Describe the experiment family and the problem in plain research language before narrowing to one instrument or assay.",
            },
            {
                "title": "Controls and discriminators",
                "body": "Surface the control, the failure mode, and the measurement that would best separate the top explanations.",
            },
            {
                "title": "Safety boundary",
                "body": "Use evidence-backed hypotheses and human review — not diagnosis, treatment, or any clinical claim.",
            },
        ],
    },
]


def build_custom_experiment_note(
    workflow: str,
    sample: str,
    observations: list[str],
    goal: str,
    constraints: str = "research workflow only",
) -> str:
    obs = "; ".join(o.strip() for o in observations if o.strip()) or "ambiguous readout"
    return (
        f"Context: {workflow}. Sample/system: {sample}. "
        f"Observations: {obs}. Goal: {goal}. Constraints: {constraints}. "
        "Use as research workflow troubleshooting only; choose the next discriminating check."
    )


def infer_dynamic_sections(note: str) -> dict[str, Any]:
    lower = note.lower()
    selected = _FAMILY_RULES[-1]
    for family in _FAMILY_RULES[:-1]:
        if any(token in lower for token in family["match_tokens"]):
            selected = family
            break

    return {
        "family_key": selected["family_key"],
        "likely_workflow_family": selected["family_label"],
        "surface_copy": selected["surface_copy"],
        "recommended_sections": ["action_plan", "evidence_quality", *selected["recommended_sections"], "outcome_loop", "experiment_memory"],
        "section_cards": selected["section_cards"],
        "ui_labels": selected["ui_labels"],
        "dynamic_prompt": (
            "This is a user-defined workflow. Avoid preset assumptions; extract signals, controls, "
            "candidate mechanisms, and next measurements from the user's note."
        ),
    }
