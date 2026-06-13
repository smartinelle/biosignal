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
            "role": "Fine-tuned-style structured signal → hypothesis → measurement extraction",
            "live": pioneer_live,
            "status": pioneer.get("detail", ""),
        },
        {
            "tool": "Gemini",
            "role": "Mechanism synthesis and caveated troubleshooting memo",
            "live": gemini_live,
            "status": synthesis.get("detail", ""),
        },
        {
            "tool": "Tavily",
            "role": "Live literature / source retrieval for evidence cards",
            "live": tavily_live,
            "status": tavily.get("detail", ""),
        },
        {
            "tool": "Aikido",
            "role": "Repository security scan for the security side challenge",
            "live": False,
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

    measurements = suggest_measurements(structured, hypotheses, evidence)
    question = human_review_question(structured, evidence, measurements)
    bottleneck = _uncertainty_bottleneck(structured)

    # Optional Gemini synthesis; deterministic fallback otherwise.
    synthesis = {"text": "", "mode": "fallback", "detail": "Gemini wrapper unavailable; deterministic memo used."}
    if _llm is not None:
        synthesis = _llm.synthesize_memo(structured, hypotheses, evidence, measurements, question)

    triples = _triples_from_pioneer(pioneer, hypotheses, measurements)

    return {
        "structured_observations": structured,
        "hypotheses": hypotheses,
        "evidence": evidence,
        "measurements": measurements,
        "human_question": question,
        "uncertainty_bottleneck": bottleneck,
        "pioneer_triples": triples,
        "pioneer_structured": pioneer,
        "synthesis": synthesis,
        "integration_status": {
            "pioneer": pioneer_status(),
            "gemini": {"mode": synthesis.get("mode")},
            "tavily": {"mode": tavily.get("mode")},
        },
        "business_impact": [
            "Turns an ambiguous experiment failure into a structured troubleshooting memo.",
            "Narrows many possible assays into a few discriminating measurements.",
            "Escalates only the unresolved scientific judgment to a senior human reviewer.",
        ],
        "partner_trace": _partner_trace(pioneer, synthesis, tavily),
        "trace": [
            {"agent": "Observation Agent", "summary": "Converted messy experiment notes into signals, context, and the R&D job-to-be-done."},
            {"agent": "Mechanism Agent", "summary": "Mapped readouts to plausible biological failure mechanisms without claiming ground truth."},
            {"agent": "Evidence Agent", "summary": "Attached evidence and caveats so the memo is source-aware, not just plausible text."},
            {"agent": "Measurement Agent", "summary": "Ranked next measurements that reduce uncertainty and avoid wasted assay cycles."},
            {"agent": "Human Review Agent", "summary": "Escalated the irreducible scientific judgment to a senior human reviewer."},
        ],
    }
