import importlib
from pathlib import Path

# Load partner keys from .env if present, before any os.getenv check runs.
# Safe no-op when python-dotenv or .env is absent; never required for the demo.
try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
except Exception:  # noqa: BLE001
    pass

from .observation_agent import structure_observation
from .mechanism_agent import infer_mechanisms
from .evidence_agent import retrieve_evidence
from .assay_agent import suggest_measurements
from .human_review_agent import human_review_question
from .pioneer_extractor import extract_troubleshooting_structure, pioneer_status
from .action_plan import build_action_plan
from .uncertainty_map import build_uncertainty_map
from .experiment_memory import build_experiment_memory, training_examples_from_memory
from .evidence_quality import grade_evidence, build_evidence_ladder


def _dual_import(package_name: str, flat_name: str):
    """Import a wrapper whether the app runs as a package or via ``streamlit``.

    Verification imports ``app.agents.pipeline`` (package context), while
    ``streamlit run app/main.py`` puts ``app/`` on the path (flat context). The
    Gemini/Tavily wrappers live in ``app/`` so we resolve both names.
    """
    for name in (package_name, flat_name):
        try:
            return importlib.import_module(name)
        except ModuleNotFoundError:
            continue
    return None


_llm = _dual_import("app.llm", "llm")
_search = _dual_import("app.search", "search")


def _humanize(label: str) -> str:
    return label.replace("_", " ")


def _uncertainty_bottleneck(structured: dict) -> dict:
    signals = ", ".join(structured.get("signals_detected", [])) or "the current readouts"
    return {
        "headline": "The data is underdetermined: do not jump from surface readouts to a biological state.",
        "why_it_matters": (
            f"{signals} can point to several failure modes. The product value is narrowing the next "
            "experiment, not pretending to know the answer."
        ),
        "decision_to_unlock": "Which mechanism is most worth testing next, and which measurement would discriminate it fastest?",
    }


def _workflow_context(structured: dict) -> dict:
    """Translate the research sprint into product-facing context for the demo.

    The research loop should improve the product immediately: every run now tells
    the viewer which biotech R&D workflow is being tested without narrowing the
    product category to that use case.
    """
    domain = str(structured.get("domain") or "").lower()
    if "tissue engineering" in domain:
        return {
            "role": "Use case: tissue-model QC / assay troubleshooting",
            "target_user": "Organoid / organ-on-chip / tissue-engineering R&D and QC teams",
            "workflow_moment": "A batch or model gives an ambiguous QC / assay readout before the team commits to the next experiment.",
            "product_gap": "Imaging and lab-data tools quantify features; they do not route ambiguous readouts to mechanisms, evidence, and the next discriminating measurement.",
            "next_validation": "Use this as one concrete test case for the broader biotech-research troubleshooting product.",
        }
    if "preservation" in domain or "ex-vivo" in domain:
        return {
            "role": "Hackathon proof / thesis anchor",
            "target_user": "Perfusion, preservation, and living-tissue R&D teams",
            "workflow_moment": "A preserved or perfused tissue sample shows underdetermined macro readouts and the team needs the next measurement, not a viability verdict.",
            "product_gap": "Perfusion devices show pressures, flows, lactate, gases, and resistance; the unowned layer is uncertainty-aware interpretation and next-measurement selection.",
            "next_validation": "Use this as the visceral demo case for the broader biotech-research troubleshooting product.",
        }
    if "assay" in domain:
        return {
            "role": "General biotech R&D workflow",
            "target_user": "R&D scientists, assay-development teams, and CRO scientists",
            "workflow_moment": "An assay produces a conflicting or low-confidence result and the team must decide whether to rerun, invalidate, or run an orthogonal check.",
            "product_gap": "ELN/LIMS systems record the run; BioSignal Navigator turns conflicting controls, artifacts, and biology into a next-action plan.",
            "next_validation": "Use this as the broadest demo of the general biotech-research troubleshooting category.",
        }
    return {
        "role": "General biotech R&D workflow",
        "target_user": "Biotech R&D assay-troubleshooting teams",
        "workflow_moment": "A living-system experiment produces ambiguous signals and a senior scientist must decide what to test next.",
        "product_gap": "ELN/LIMS tools capture data; BioSignal Navigator owns the mechanism/evidence/next-measurement loop.",
        "next_validation": "Narrow to a repeated workflow moment before adding more features.",
    }


def _triples_from_pioneer(pioneer: dict, hypotheses: list[dict], measurements: list[dict]) -> list[dict]:
    """Build signal → hypothesis → next-measurement triples from extracted relations.

    Falls back to zipping the deterministic agents if extraction was too sparse,
    so the side-challenge artifact is never empty.
    """
    relations = pioneer.get("relations", [])
    triples = []
    for mechanism in pioneer.get("candidate_mechanisms", [])[:3]:
        label = mechanism["label"]
        observation = next(
            (r["subject"] for r in relations
             if r["predicate"] == "supports_possible_mechanism" and r["object"] == label),
            "ambiguous experiment readout",
        )
        measurement = next(
            (r["subject"] for r in relations
             if r["predicate"] == "reduces_uncertainty_about" and r["object"] == label),
            None,
        )
        triples.append({
            "observation": _humanize(observation),
            "failure_hypothesis": _humanize(label),
            "next_measurement": _humanize(measurement) if measurement else "targeted discriminating assay",
            "confidence": mechanism.get("confidence"),
        })
    if triples:
        return triples
    # fallback: deterministic agents
    for hypothesis, measurement in zip(hypotheses[:3], measurements[:3]):
        triples.append({
            "observation": "ambiguous experiment readout",
            "failure_hypothesis": hypothesis["mechanism"],
            "next_measurement": measurement["measurement"],
            "confidence": None,
        })
    return triples


def _partner_trace(pioneer: dict, synthesis: dict, tavily: dict) -> list[dict]:
    """Build the partner trace from the integrations that actually ran."""
    pioneer_live = pioneer.get("mode") == "live"
    gemini_live = synthesis.get("mode") == "live"
    tavily_live = tavily.get("mode") == "live"
    return [
        {
            "tool": "Pioneer",
            "role": "Deterministic GLiNER2-style structured signal → hypothesis → measurement extraction",
            "live": pioneer_live,
            "badge": "live" if pioneer_live else "artifact",
            "status": pioneer.get("detail", ""),
        },
        {
            "tool": "Gemini",
            "role": "Mechanism synthesis and caveated troubleshooting memo",
            "live": gemini_live,
            "badge": "live" if gemini_live else "fallback",
            "status": synthesis.get("detail", ""),
        },
        {
            "tool": "Tavily",
            "role": "Live literature / source retrieval for evidence cards",
            "live": tavily_live,
            "badge": "live" if tavily_live else "fallback",
            "status": tavily.get("detail", ""),
        },
        {
            "tool": "Aikido",
            "role": "Repository security scan for the security side challenge",
            "live": False,
            "badge": "docs",
            "status": "Run via connected GitHub repo; report screenshot included in submission docs.",
        },
    ]


def run_pipeline(raw_observation: str) -> dict:
    structured = structure_observation(raw_observation)
    hypotheses = infer_mechanisms(structured)
    pioneer = extract_troubleshooting_structure(raw_observation)

    evidence = retrieve_evidence(structured, hypotheses)
    # Optionally augment curated evidence with live Tavily sources.
    tavily = {"results": [], "mode": "fallback", "detail": "Tavily wrapper unavailable; curated evidence used."}
    if _search is not None:
        tavily = _search.search_evidence(structured, hypotheses)
    evidence = list(evidence) + list(tavily.get("results", []))
    graded_evidence = grade_evidence(evidence, structured.get("domain", ""))
    evidence_ladder = build_evidence_ladder(graded_evidence)

    measurements = suggest_measurements(structured, hypotheses, graded_evidence)
    question = human_review_question(structured, evidence, measurements)
    bottleneck = _uncertainty_bottleneck(structured)
    workflow_context = _workflow_context(structured)

    # Optional Gemini synthesis; deterministic fallback otherwise.
    synthesis = {"text": "", "mode": "fallback", "detail": "Gemini wrapper unavailable; deterministic memo used."}
    if _llm is not None:
        synthesis = _llm.synthesize_memo(structured, hypotheses, evidence, measurements, question)

    triples = _triples_from_pioneer(pioneer, hypotheses, measurements)
    partner_trace = _partner_trace(pioneer, synthesis, tavily)
    action_plan = build_action_plan(
        structured,
        hypotheses,
        measurements,
        evidence,
        workflow_context,
        bottleneck,
        partner_trace,
    )
    uncertainty_map = build_uncertainty_map(structured, hypotheses, measurements, evidence, bottleneck)
    experiment_memory = build_experiment_memory(structured, action_plan, pioneer)
    pioneer_training_examples = training_examples_from_memory(experiment_memory)

    return {
        "structured_observations": structured,
        "hypotheses": hypotheses,
        "evidence": graded_evidence,
        "evidence_ladder": evidence_ladder,
        "measurements": measurements,
        "human_question": question,
        "uncertainty_bottleneck": bottleneck,
        "workflow_context": workflow_context,
        "pioneer_triples": triples,
        "pioneer_structured": pioneer,
        "synthesis": synthesis,
        "action_plan": action_plan,
        "uncertainty_map": uncertainty_map,
        "human_review_options": {
            "accept_next_action": "Accept next action",
            "ask_faster_alternative": "Ask for cheaper / faster alternative",
            "flag_top_hypothesis_implausible": "Flag top hypothesis as implausible",
            "add_missing_context": "Add missing context",
            "mark_overclaiming": "Mark as overclaiming / unsafe",
        },
        "experiment_memory": experiment_memory,
        "pioneer_training_examples": pioneer_training_examples,
        "integration_status": {
            "pioneer": pioneer_status(),
            "gemini": {"mode": synthesis.get("mode")},
            "tavily": {"mode": tavily.get("mode")},
        },
        "business_impact": [
            "Turns an ambiguous living-system failure into a structured troubleshooting memo.",
            "Narrows many plausible mechanisms into a few discriminating measurements.",
            "Positions BioSignal Navigator as the interpretation layer on top of instruments and ELN/LIMS data, not a system of record.",
            "Escalates only the unresolved scientific judgment to a senior human reviewer.",
        ],
        "partner_trace": partner_trace,
        "trace": [
            {"agent": "Observation Agent", "summary": "Converted messy experiment notes into signals, context, and the R&D job-to-be-done."},
            {"agent": "Mechanism Agent", "summary": "Mapped readouts to plausible biological failure mechanisms without claiming ground truth."},
            {"agent": "Evidence Agent", "summary": "Attached evidence and caveats so the memo is source-aware, not just plausible text."},
            {"agent": "Measurement Agent", "summary": "Ranked next measurements that reduce uncertainty and avoid wasted assay cycles."},
            {"agent": "Human Review Agent", "summary": "Escalated the irreducible scientific judgment to a senior human reviewer."},
        ],
    }
