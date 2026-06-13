# BioSignal Navigator Implementation Plan

> **For Hermes / Claude Code agents:** Use this as the coordination contract. Pick one workstream, stay inside the owned files, verify locally, and report exact files changed plus commands run.

## Goal

Build a credible 1-day hackathon MVP for **BioSignal Navigator**: an agent-human biomedical evidence-routing demo that maps messy observations to possible mechanisms, evidence, next measurements, and a human review question.

## Architecture

A Streamlit app calls a modular Python pipeline:

```text
Observation Agent
  → Mechanism Agent
  → Evidence Agent
  → Assay / Measurement Agent
  → Human Review Agent
  → Evidence Card UI
```

The app must work in two modes:

1. **Fallback/offline demo mode:** curated evidence and heuristic agents; no API keys required.
2. **Partner-tech mode:** Gemini + Tavily + Pioneer wrappers enrich the same pipeline.

## Safety / positioning invariant

This project must never present itself as a clinical decision tool. It is for research workflow and evidence routing.

User-visible language should say:
- possible mechanisms
- supporting / contradictory evidence
- suggested measurements
- uncertainty
- human review required

Avoid:
- diagnosis
- treatment
- prediction of viability
- transplant/discard recommendation

---

## Workstream A — UI and demo polish

**Owner surface:**
- `app/main.py`
- `docs/demo_script.md`

**Objective:** Make the app demoable and legible in 2 minutes.

**Tasks:**
1. Add a top-level value proposition block: "From biomedical observations to molecular hypotheses and next measurements."
2. Make the multi-agent trace visually obvious.
3. Add a safety banner: "Research workflow only — not diagnosis or treatment."
4. Improve the evidence card layout:
   - observations
   - mechanisms
   - evidence/caveats
   - measurements
   - human review question
5. Add 3 demo presets:
   - tissue preservation
   - sepsis/inflammation research
   - organoid QC
6. Update `docs/demo_script.md` to match the final UI.

**Verification:**
```bash
source .venv/bin/activate
python -m compileall -q app
streamlit run app/main.py --server.port 8501 --server.address 127.0.0.1 --server.headless true
curl -fsS http://127.0.0.1:8501/_stcore/health
```

---

## Workstream B — Gemini structured reasoning

**Owner surface:**
- `app/llm.py`
- `app/agents/mechanism_agent.py`
- `app/agents/pipeline.py` only if needed

**Objective:** Add Gemini-backed mechanism generation with deterministic fallback.

**Tasks:**
1. Create `app/llm.py` with:
   - environment loading from `.env`
   - `has_gemini()`
   - `generate_json(prompt, fallback)` or similar
2. Update `mechanism_agent.py` so it:
   - uses Gemini when `GEMINI_API_KEY` exists
   - returns the current heuristic fallback otherwise
3. Output schema:
```json
{
  "mechanisms": [
    {
      "mechanism": "Hypoxia / anaerobic metabolism",
      "rationale": "...",
      "confidence": "low|medium|high",
      "caveat": "..."
    }
  ]
}
```
4. Keep all caveats explicit.

**Verification:**
```bash
source .venv/bin/activate
python -m compileall -q app
python - <<'PY'
from app.agents.observation_agent import structure_observation
from app.agents.mechanism_agent import infer_mechanisms
s = structure_observation('48h cold preserved tissue, lactate rising, pH falling')
print(infer_mechanisms(s))
PY
```

---

## Workstream C — Tavily evidence retrieval

**Owner surface:**
- `app/search.py`
- `app/agents/evidence_agent.py`
- `app/data/`

**Objective:** Add Tavily search/extraction for literature evidence while preserving curated fallback.

**Tasks:**
1. Create `app/search.py` with:
   - `has_tavily()`
   - `tavily_search(query, max_results=3)`
   - safe fallback returning empty list if no key/error
2. Update `evidence_agent.py` to:
   - formulate a query from structured observation + hypotheses
   - call Tavily if configured
   - merge top results with curated Tissue Stability Cell Atlas evidence
   - always include caveats
3. Keep source objects shaped like:
```json
{
  "source": "title or citation",
  "url": "optional",
  "claim": "short claim",
  "caveat": "why this is indirect / uncertain"
}
```

**Verification:**
```bash
source .venv/bin/activate
python -m compileall -q app
python - <<'PY'
from app.agents.pipeline import run_pipeline
r = run_pipeline('48h cold preserved tissue, lactate rising, pH falling, resistance increasing')
print(r['evidence'])
PY
```

---

## Workstream D — Pioneer structured extractor story

**Owner surface:**
- `app/agents/pioneer_extractor.py`
- `app/data/observation_mechanism_biomarker_triples.jsonl`
- `docs/partner_tech.md`
- `README.md` only partner-tech section

**Objective:** Make the Pioneer use credible and visible.

**Tasks:**
1. Create a small synthetic/curated JSONL dataset of triples:
```json
{"observation":"rising lactate during perfusion","mechanism":"anaerobic metabolism / hypoxia","biomarker":"lactate trend, oxygen consumption"}
```
2. Create `pioneer_extractor.py` with a fallback local extractor interface.
3. Document intended Pioneer use:
   - generate/evaluate observation → mechanism → biomarker triples
   - replace one general LLM extraction call with smaller structured extraction
   - use adaptive inference/evals if available during hackathon
4. Add a small UI/trace mention if time permits.

**Verification:**
```bash
source .venv/bin/activate
python -m compileall -q app
python - <<'PY'
from pathlib import Path
p = Path('app/data/observation_mechanism_biomarker_triples.jsonl')
print(p.exists(), sum(1 for _ in p.open()) if p.exists() else 0)
PY
```

---

## Workstream E — Docs, submission, and security

**Owner surface:**
- `README.md`
- `docs/architecture.md`
- `docs/partner_tech.md`
- `docs/submission_checklist.md`

**Objective:** Make the repo judge-ready.

**Tasks:**
1. Improve README:
   - one-liner
   - safety framing
   - quick start
   - architecture diagram
   - partner technologies
   - demo scenario
2. Add `docs/architecture.md` with pipeline diagram and file map.
3. Add `docs/partner_tech.md` mapping Gemini/Tavily/Pioneer/Aikido to features.
4. Add `docs/submission_checklist.md`:
   - public GitHub repo
   - README complete
   - 2-min Loom
   - Aikido screenshot
   - at least 3 partner techs named
   - submission form URL
5. Add explicit "not clinical decision support" disclaimer.

**Verification:**
```bash
git status --short
python -m compileall -q app
```

---

## Workstream F — Review / integration agent

**Owner surface:** read-only by default; edits only after reporting issues.

**Objective:** Catch overclaiming, broken setup, and demo risks.

**Tasks:**
1. Review all user-visible text for overclaiming.
2. Run the app and basic smoke checks.
3. Check README setup instructions against actual files.
4. Check that fallback mode works without API keys.
5. Check `.gitignore` prevents `.env`, `.venv`, and caches.
6. Report critical issues first.

**Verification:**
```bash
git status --short
source .venv/bin/activate
python -m compileall -q app
```

---

## Recommended agent launch commands

### Hermes subagent pattern

Use `delegate_task` for short independent tasks, passing this plan and limiting files.

### Claude Code print-mode pattern

Prefer print mode for one-shot tasks:

```bash
cd /root/projects/biosignal-navigator
claude -p "Read CLAUDE.md and docs/plans/hackathon-build-plan.md. Execute Workstream A only. Stay within app/main.py and docs/demo_script.md. Verify with python -m compileall -q app. Report files changed." --allowedTools "Read,Edit,Write,Bash" --max-turns 12 --max-budget-usd 3
```

Use separate commands for B/C/D/E. Do not run multiple agents editing the same files.

### Claude Code worktree pattern for parallelism

Use a separate git worktree per workstream when running in parallel:

```bash
cd /root/projects/biosignal-navigator
git worktree add ../biosignal-ui -b workstream-ui
git worktree add ../biosignal-evidence -b workstream-evidence
git worktree add ../biosignal-docs -b workstream-docs
```

Then run Claude in each worktree with the corresponding workstream prompt.

---

## Final integration checklist

Before submission:

- [ ] `python -m compileall -q app` passes
- [ ] Streamlit health endpoint returns `ok`
- [ ] README quick start works
- [ ] Demo works without API keys
- [ ] Partner tech docs mention Gemini, Tavily, Pioneer, Aikido
- [ ] No secrets committed
- [ ] Aikido screenshot captured
- [ ] 2-minute demo script recorded
- [ ] Submission form filled before Sunday 14:00
