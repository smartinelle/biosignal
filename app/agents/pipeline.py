from .observation_agent import structure_observation
from .mechanism_agent import infer_mechanisms
from .evidence_agent import retrieve_evidence
from .assay_agent import suggest_measurements
from .human_review_agent import human_review_question


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


def _pioneer_like_triples(hypotheses: list[dict], measurements: list[dict]) -> list[dict]:
    triples = []
    for hypothesis, measurement in zip(hypotheses[:3], measurements[:3]):
        triples.append(
            {
                "observation": "ambiguous experiment readout",
                "failure_hypothesis": hypothesis["mechanism"],
                "next_measurement": measurement["measurement"],
            }
        )
    return triples


def run_pipeline(raw_observation: str) -> dict:
    structured = structure_observation(raw_observation)
    hypotheses = infer_mechanisms(structured)
    evidence = retrieve_evidence(structured, hypotheses)
    measurements = suggest_measurements(structured, hypotheses, evidence)
    question = human_review_question(structured, evidence, measurements)
    bottleneck = _uncertainty_bottleneck(structured)
    triples = _pioneer_like_triples(hypotheses, measurements)
    return {
        "structured_observations": structured,
        "hypotheses": hypotheses,
        "evidence": evidence,
        "measurements": measurements,
        "human_question": question,
        "uncertainty_bottleneck": bottleneck,
        "pioneer_triples": triples,
        "business_impact": [
            "Turns an ambiguous experiment failure into a structured troubleshooting memo.",
            "Narrows many possible assays into a few discriminating measurements.",
            "Escalates only the unresolved scientific judgment to a senior human reviewer.",
        ],
        "partner_trace": [
            {"tool": "Pioneer", "role": "Structured signal → hypothesis → measurement extraction", "status": "MVP fallback shown as transparent triples"},
            {"tool": "Gemini", "role": "Mechanism synthesis and caveated memo generation", "status": "Used when GEMINI_API_KEY is configured; fallback remains demoable"},
            {"tool": "Tavily", "role": "Evidence retrieval and source extraction", "status": "Used when TAVILY_API_KEY is configured; curated evidence fallback included"},
            {"tool": "Aikido", "role": "Repository security scan for side challenge", "status": "Documented for submission"},
        ],
        "trace": [
            {"agent": "Observation Agent", "summary": "Converted messy experiment notes into signals, context, and the R&D job-to-be-done."},
            {"agent": "Mechanism Agent", "summary": "Mapped readouts to plausible biological failure mechanisms without claiming ground truth."},
            {"agent": "Evidence Agent", "summary": "Attached evidence and caveats so the memo is source-aware, not just plausible text."},
            {"agent": "Measurement Agent", "summary": "Ranked next measurements that reduce uncertainty and avoid wasted assay cycles."},
            {"agent": "Human Review Agent", "summary": "Escalated the irreducible scientific judgment to a senior human reviewer."},
        ],
    }
