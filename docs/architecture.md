# Architecture

BioSignal Navigator is an agent-human troubleshooting workspace for ambiguous
biotech R&D experiments. The first demo vertical is **living tissue systems**
(tissue preservation, organoids, organ-on-chip, tissue engineering QC).

It is a **research workflow tool**, not diagnosis, treatment, viability
prediction, or clinical decision support.

## Pipeline

```text
raw experiment note
  → Observation Agent      (structure signals, domain, job-to-be-done)
  → Mechanism Agent        (plausible failure mechanisms, no ground-truth claim)
  → Pioneer extractor      (typed entities, relations, safety-boundary flags)
  → Evidence Agent         (curated cards + optional live Tavily sources, w/ caveats)
  → Measurement Agent      (next discriminating measurements)
  → Human Review Agent     (escalate the irreducible scientific judgment)
  → Uncertainty Bottleneck (name what cannot be known yet)
  → Gemini synthesis       (caveated troubleshooting memo)
```

`app/agents/pipeline.py:run_pipeline()` orchestrates these and returns one
JSON-like dict consumed by the Streamlit UI.

## Modules

| File | Responsibility |
|---|---|
| `app/main.py` | Streamlit UI; presets; live-vs-fallback badges; demo layout |
| `app/agents/pipeline.py` | Orchestration; builds `partner_trace` from real run modes |
| `app/agents/observation_agent.py` | Structure messy note into signals + context |
| `app/agents/mechanism_agent.py` | Map readouts to candidate mechanisms |
| `app/agents/evidence_agent.py` | Curated evidence cards with caveats |
| `app/agents/assay_agent.py` | Next-measurement suggestions |
| `app/agents/human_review_agent.py` | Human escalation question |
| `app/agents/pioneer_extractor.py` | Deterministic GLiNER2-style structured extraction (+ guarded live Pioneer path) |
| `app/llm.py` | Gemini memo synthesis (OpenRouter or native), deterministic fallback |
| `app/search.py` | Tavily live retrieval, curated fallback |
| `app/data/` | Curated dataset summaries (e.g. PRJEB31843) |

## Fallback-first design

Every integration has a deterministic fallback and the demo runs with **no API
keys**:

- **Pioneer** → deterministic extractor (the side-challenge artifact itself).
- **Gemini** → deterministic memo composed from pipeline outputs.
- **Tavily** → curated evidence cards.

Wrappers never make a network call without a key and never raise; any partner
failure falls back transparently and the UI reports `live` vs `fallback`.

## Run modes & imports

The app must import correctly in two contexts:

- `streamlit run app/main.py` — `app/` is on `sys.path`; `agents.pipeline` and
  the flat `llm` / `search` modules resolve directly.
- `from app.agents.pipeline import run_pipeline` (verification) — package
  context.

`pipeline.py` uses a small `_dual_import` helper so the Gemini/Tavily wrappers
resolve under both names. `.env` is loaded (via `python-dotenv`) at the top of
both `pipeline.py` and `main.py`.

## Safety boundary

The Pioneer extractor emits explicit `safety_flags`
(`research_workflow_only`, `needs_human_review`, `clinical_claim_risk`,
`insufficient_evidence`), and the Gemini prompt forbids diagnosis, viability
prediction, and transplant/discard or treatment recommendations. Every memo ends
with a human-review requirement.
