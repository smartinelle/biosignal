def human_review_question(structured: dict, evidence: list[dict], measurements: list[dict]) -> str:
    return (
        "Before spending the next experiment cycle: which single measurement would best distinguish "
        "metabolic stress from structural/tissue damage, and does the team have enough context to run it now? "
        "If not, route to a senior scientist with this memo rather than making an automated decision."
    )
