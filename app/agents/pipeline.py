from .observation_agent import structure_observation
from .mechanism_agent import infer_mechanisms
from .evidence_agent import retrieve_evidence
from .assay_agent import suggest_measurements
from .human_review_agent import human_review_question


def run_pipeline(raw_observation: str) -> dict:
    structured = structure_observation(raw_observation)
    hypotheses = infer_mechanisms(structured)
    evidence = retrieve_evidence(structured, hypotheses)
    measurements = suggest_measurements(structured, hypotheses, evidence)
    question = human_review_question(structured, evidence, measurements)
    return {
        "structured_observations": structured,
        "hypotheses": hypotheses,
        "evidence": evidence,
        "measurements": measurements,
        "human_question": question,
        "trace": [
            {"agent": "Observation Agent", "summary": "Converted messy note into context, signals, goal and uncertainty."},
            {"agent": "Mechanism Agent", "summary": "Mapped signals to plausible biological mechanisms, without claiming diagnosis."},
            {"agent": "Evidence Agent", "summary": "Retrieved/attached relevant preservation evidence and caveats."},
            {"agent": "Assay Agent", "summary": "Prioritized measurements that reduce uncertainty."},
            {"agent": "Human Review Agent", "summary": "Escalated the unresolved decision to a human expert."},
        ],
    }
