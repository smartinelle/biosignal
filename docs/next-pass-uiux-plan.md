# Next Product Build Pass — UI/UX + Demo Plan

Status: build-ready plan for Claude Code. Do **not** run Streamlit during this pass; verify with compile/smoke tests only unless Sacha explicitly asks to run the server.

## North star

> Input an experiment problem → see the bottleneck → inspect evidence → get ranked next actions → export a partner-ready summary.

The app should communicate value in under 10 seconds:

1. it understands the research problem;
2. it names the bottleneck;
3. it grounds hypotheses in evidence;
4. it produces concrete next actions;
5. it exposes partner-tech proof without looking like a notebook.

## Current shape to preserve

Keep the existing app logic:

- product shape;
- presets;
- product context;
- agent trace;
- uncertainty bottleneck;
- memo;
- structured observations;
- hypotheses;
- measurements;
- evidence/caveats;
- Pioneer extraction;
- partner trace;
- business impact.

The next pass should improve **product workflow and UI organization**, not rewrite the reasoning engine.

## Desired screens / sections

### 1. Landing / preset chooser

Purpose: make it feel like a product, not a Streamlit notebook.

Sections:

- hero headline: “Turn messy biotech runs into clear next steps.”
- subtitle: “BioSignal Navigator helps R&D teams find the bottleneck, compare evidence, and produce a ranked action plan.”
- preset cards grid:
  - Assay signal collapse
  - qPCR / ddPCR anomaly
  - Protein yield / purity drop
  - Cell culture drift
  - Bioreactor deviation
  - Organoid/OoC ambiguity
  - Ex-vivo tissue preservation
- “What this does / what this does not do” block.
- partner-tech badges: Pioneer, Gemini/OpenRouter, Tavily, Aikido.

### 2. Investigation workspace

Use a 3-column product layout when results exist:

- Left: problem context, selected workflow, input note.
- Center: bottleneck, hypotheses, evidence, measurements.
- Right: action plan, partner-ready summary, business impact, partner trace.

### 3. Action-plan section

This is the most important new product surface.

Render top 3 actions as cards:

- rank;
- action title;
- goal;
- why now;
- effort: low/medium/high;
- impact: low/medium/high;
- confidence;
- evidence count;
- expected readout;
- success criterion;
- remaining human decision.

### 4. Partner-ready summary

A concise export/handoff block:

- problem summary;
- current bottleneck;
- top recommended next action;
- what we know;
- what we do not know;
- why this is research-only;
- partner tech used.

### 5. Memo / export view

Add copy/download affordances if easy:

- copy partner summary;
- copy action plan JSON;
- copy troubleshooting memo.

## Action-plan schema

Add an `action_plan` object to `run_pipeline()` output:

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

Implementation shortcut: derive this deterministically from existing `measurements`, `hypotheses`, `evidence`, `workflow_context`, and `uncertainty_bottleneck`. Do not introduce new network dependencies.

## Microcopy

Hero:

- “Turn messy biotech runs into clear next steps.”
- “Find the bottleneck, compare evidence, and produce a partner-ready action plan in minutes.”

Input:

- Label: “Describe the experiment problem”
- Placeholder: “e.g. signal dropped after reagent-lot change; qPCR controls drifted; protein yield collapsed; QC failed across batches”

Action plan:

- Header: “Recommended next actions”
- Helper: “Ranked by likely impact, evidence strength, and speed to validation.”

Evidence:

- Header: “Evidence that matters”
- Helper: “Supporting and contradictory signals, with caveats.”

Uncertainty:

- Header: “What we still do not know”
- Helper: “The product is useful because it narrows uncertainty, not because it pretends to eliminate it.”

Partner:

- Header: “Partner-ready summary”
- Helper: “A concise handoff for collaborators, reviewers, or technical partners.”

## 2-minute demo sequence

0:00–0:10 — Product frame:

> “BioSignal Navigator is a debugger for biotech R&D workflows.”

0:10–0:25 — Select broad workflow:

> Load “Assay signal collapse after reagent-lot change.”

0:25–0:45 — Show bottleneck:

> controls drifted, edge wells worse, reagent lot changed; ambiguous biology vs artifact.

0:45–1:05 — Show evidence/caveats:

> the system names plausible mechanisms but refuses to claim ground truth.

1:05–1:25 — Show action plan:

> old-vs-new reagent control, edge-vs-center analysis, control repeat, orthogonal assay.

1:25–1:40 — Flash thesis/living-system proof:

> same loop works for ex-vivo tissue preservation and organoid/OoC ambiguity.

1:40–2:00 — Show partner trace/export:

> Pioneer extraction, Gemini synthesis, Tavily evidence, Aikido security; export partner-ready summary.

## Acceptance criteria

Product/UI:

- landing screen has clear hero and preset cards;
- first-time reviewer can explain product after 10 seconds;
- main result view reads as product workflow, not notebook output;
- action plan is visible and ranked;
- partner-ready summary is separate from internal trace.

Content:

- product marketed as general biotech R&D troubleshooting;
- tissue engineering/preservation are use cases;
- no clinical/viability/transplant/discard claims;
- “what we do not know” remains visible.

Verification:

- `python -m compileall -q app`
- pipeline smoke tests for all presets;
- no Streamlit server run unless explicitly requested.

## Exact Claude Code implementation tasks

1. Move presets into a single config module/file.
2. Add 3 new broad presets: qPCR/ddPCR anomaly, protein yield/purity drop, cell culture drift or bioreactor deviation.
3. Add deterministic `action_plan` generation in the pipeline.
4. Refactor `app/main.py` into a more product-like layout: preset cards/selector, action plan cards, partner-ready summary.
5. Add export/copy blocks for memo and action plan JSON if easy.
6. Update `docs/demo_script.md` to match the general biotech R&D positioning and 2-minute flow.
7. Run compile + pipeline smoke tests only.
8. Commit with `feat: polish product demo workflow`.
