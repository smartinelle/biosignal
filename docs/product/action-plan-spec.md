# Action Plan Spec

Status: v1 — deterministic action-planning layer for BioSignal Navigator.

## Goal

Convert existing pipeline outputs into an operational `action_plan` that makes the product feel useful, not merely descriptive.

Inputs already available:

- `structured_observations`
- `hypotheses`
- `measurements`
- `evidence`
- `workflow_context`
- `uncertainty_bottleneck`
- `pioneer_triples`
- `pioneer_structured`
- `synthesis`
- `partner_trace`

No new network calls or dependencies should be required.

## Design principles

1. Deterministic: same inputs produce same plan.
2. Grounded: every action should map to upstream observations/hypotheses/measurements/evidence.
3. Operational: action items should be things an R&D team could actually do.
4. Uncertainty-first: plan should say what remains unknown.
5. Safe: no clinical, viability, transplant/discard, release, batch-disposition, or biological-ground-truth claims.

## Output schema

Recommended shape:

```python
{
    "problem_summary": str,
    "bottleneck": {
        "title": str,
        "why_it_matters": str,
        "confidence": float,
    },
    "ranked_actions": [
        {
            "rank": int,
            "title": str,
            "goal": str,
            "why_now": str,
            "effort": "low" | "medium" | "high",
            "impact": "low" | "medium" | "high",
            "confidence": float,
            "evidence_count": int,
            "expected_readout": str,
            "success_criteria": list[str],
            "risk": str,
        }
    ],
    "what_we_do_not_know": list[str],
    "human_decision": str,
    "partner_summary": list[str],
}
```

## Candidate action types

Use a controlled vocabulary:

- `validate`: test whether a hypothesis holds.
- `measure`: collect a discriminating metric.
- `compare`: compare controls, lots, runs, or baseline.
- `audit`: inspect metadata, process, timing, or handling.
- `repeat`: rerun with tighter controls.
- `escalate`: ask a human expert to decide the unresolved judgment.
- `document`: preserve a conclusion or caveat.

## Deterministic generation rules

### 1. Start from measurements

For each item in `measurements`, create one candidate action:

- title = measurement name;
- goal = the measurement’s `why` text;
- evidence_count = number of evidence items + supporting hypotheses if available;
- expected_readout = what the measurement should distinguish;
- success criteria = 1–2 bullets derived from measurement/hypothesis text.

### 2. Enrich with hypotheses

Map action to the most related hypothesis by keyword overlap:

- if measurement mentions reagent/control/plate → technical artifact hypotheses;
- if measurement mentions oxygen/lactate/pH → metabolic/perfusion hypotheses;
- if measurement mentions marker/panel/RNA → cell-state/degradation hypotheses;
- if measurement mentions media/incubator/contamination → cell-culture environment hypotheses.

### 3. Use the uncertainty bottleneck

Always include bottleneck text in:

- `bottleneck.title`
- `bottleneck.why_it_matters`
- at least one `what_we_do_not_know` item.

If no bottleneck exists, default:

> “The current evidence is underdetermined; run the smallest control that separates technical artifact from biological change.”

### 4. Add safety and human decision

Human decision should be a single sentence:

> “Human review is needed to decide whether to repeat, run an orthogonal check, or treat the current evidence as inconclusive.”

Preset-specific variants are allowed, but must not recommend clinical or disposition decisions.

## Ranking heuristic

Compute a simple priority score internally:

```text
priority = impact_weight + confidence_weight + uncertainty_reduction - effort_penalty
```

Suggested deterministic scoring:

### Impact

- high: action directly distinguishes top hypotheses or controls interpretation.
- medium: action adds useful context but does not resolve primary bottleneck.
- low: action mostly documents or monitors.

### Confidence

Base confidence:

- 0.75 if action is a direct control/orthogonal check;
- 0.65 if supported by multiple observations;
- 0.55 if supported by one weak observation;
- cap at 0.50 if evidence is contradictory;
- cap at 0.45 if action is speculative or Pioneer-only.

### Effort

- low: one focused control/check/metadata audit.
- medium: side-by-side rerun or orthogonal assay.
- high: sequencing, omics, multi-condition matrix, new experimental campaign.

### Uncertainty reduction

- +0.20 if action directly addresses the bottleneck;
- +0.15 if action separates technical artifact from biological change;
- +0.10 if action can reuse existing samples/data;
- +0.05 if action improves partner-facing explanation.

Tie-break rules:

1. higher impact;
2. lower effort;
3. higher confidence;
4. earlier measurement order;
5. alphabetical title.

## Recommended default action templates

### Assay signal collapse

1. Old-vs-new reagent lot control run.
2. Edge-vs-center plate-layout analysis.
3. Positive/negative control repeat or orthogonal readout.

### qPCR / ddPCR

1. Dilution/inhibition control.
2. NTC/no-RT/positive-control repeat.
3. Alternate primer/probe or orthogonal assay.

### Protein purification

1. Fraction audit across purification stages.
2. Soluble/insoluble and degradation check.
3. Buffer or induction mini-screen.

### Cell culture drift

1. Contamination/mycoplasma and identity check.
2. Media-lot/incubator side-by-side.
3. Compare to reference passage or thaw stock.

### Bioreactor deviation

1. Sensor/probe calibration cross-check.
2. Feed/pump/event timestamp audit.
3. Historical-batch overlay and inoculum QC.

### Organoid / OoC

1. Time-lapse morphology vs matched baseline.
2. Functional barrier/permeability or marker readout.
3. Flow/ECM/seeding/bubble audit.

### Preservation

1. Lactate/pH/oxygen trend check.
2. Perfusate gas/oxygen-extraction measurement.
3. Endothelial/stress marker or histology as research readout.

## UI rendering rules

Action-plan section:

- Header: “Recommended next actions”
- Helper: “Ranked by likely impact, evidence strength, and speed to validation.”
- Show top 3 cards by default.
- Each card should show:
  - rank;
  - title;
  - effort chip;
  - impact chip;
  - confidence badge;
  - why now;
  - expected readout;
  - success criteria.

Partner-ready summary:

- 4–6 bullets maximum.
- Must include: problem, bottleneck, top action, uncertainty, safety boundary, partner tech used.

What-we-do-not-know:

- Always visible.
- Keep 3–5 bullets.
- This is a product differentiator, not a weakness.

## Smoke tests

Run a pipeline smoke test for at least:

1. assay signal collapse;
2. qPCR anomaly;
3. protein yield drop;
4. cell culture drift;
5. bioreactor deviation;
6. preservation;
7. organoid/OoC.

For each, assert:

- `action_plan` exists;
- `ranked_actions` length >= 3;
- each action has title, effort, impact, confidence, expected_readout;
- `what_we_do_not_know` non-empty;
- `human_decision` non-empty;
- no forbidden language appears in titles or summary:
  - diagnosis;
  - treatment;
  - transplant;
  - discard;
  - viability prediction;
  - batch release;
  - disposition.

## Acceptance criteria

The feature is ready when:

- every preset yields a deterministic `action_plan`;
- top action is concrete enough to run;
- plan separates technical artifact from biological interpretation;
- UI makes action plan more prominent than raw JSON;
- safety boundary remains explicit;
- verification passes without running Streamlit.
