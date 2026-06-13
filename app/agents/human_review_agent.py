def human_review_question(structured: dict, evidence: list[dict], measurements: list[dict]) -> str:
    return "Is this a research sample where molecular assay is feasible, or a time-critical decision where only macro trends are available? Approve next measurement plan or mark evidence as insufficient."
