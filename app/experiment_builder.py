"""Custom experiment builder for general-purpose biotech troubleshooting.

This keeps BioSignal Navigator from feeling hard-coded to presets. Biotech teams
can describe their own workflow, observations, goals, and constraints; the app
turns that into the same pipeline input and decides which UI sections matter.
"""

from __future__ import annotations


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


def infer_dynamic_sections(note: str) -> dict:
    lower = note.lower()
    if any(token in lower for token in ("adc", "hic", "dar", "lc-ms", "mass spec", "chromatography")):
        family = "analytical chemistry / bioconjugation troubleshooting"
        extras = ["evidence_quality", "outcome_loop", "experiment_memory", "analytical_controls"]
    elif any(token in lower for token in ("qpcr", "ddpcr", "primer", "ct", "ntc")):
        family = "molecular assay troubleshooting"
        extras = ["evidence_quality", "outcome_loop", "experiment_memory", "control_matrix"]
    elif any(token in lower for token in ("bioreactor", "fermentation", "titer", "off-gas")):
        family = "bioprocess troubleshooting"
        extras = ["evidence_quality", "outcome_loop", "experiment_memory", "process_timeline"]
    elif any(token in lower for token in ("organoid", "organ-on-chip", "tissue", "perfusion")):
        family = "living tissue system troubleshooting"
        extras = ["evidence_quality", "outcome_loop", "experiment_memory", "safety_boundary"]
    else:
        family = "custom biotech R&D troubleshooting"
        extras = ["evidence_quality", "outcome_loop", "experiment_memory"]
    return {
        "likely_workflow_family": family,
        "recommended_sections": ["action_plan", "uncertainty_map", "scientist_review", *extras],
        "dynamic_prompt": (
            "This is a user-defined workflow. Avoid preset assumptions; extract signals, controls, "
            "candidate mechanisms, and next measurements from the user's note."
        ),
    }
