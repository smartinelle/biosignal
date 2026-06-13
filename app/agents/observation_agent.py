def structure_observation(text: str) -> dict:
    lower = text.lower()
    signals = []
    for token in ["lactate", "ph", "resistance", "oxygen", "morphology", "crp", "viability", "cold", "48h", "72h"]:
        if token in lower:
            signals.append(token)
    domain = "tissue preservation / tissue engineering" if any(t in lower for t in ["tissue", "preservation", "cold", "perfusion"]) else "translational biomedical research"
    return {
        "domain": domain,
        "raw_note": text,
        "signals_detected": signals,
        "goal": "Generate molecular hypotheses and next measurements; do not make a clinical decision.",
        "uncertainty": "high",
    }
