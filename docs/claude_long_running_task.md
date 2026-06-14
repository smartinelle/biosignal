# Claude Long-Running Task — Hackathon Build

## Mission

Turn BioSignal Navigator into a stronger hackathon artifact while preserving the venture-shaped pivot:

> AI agents for biotech R&D experiment troubleshooting, demonstrated on living tissue systems.

Do **not** pivot back to generic healthcare AI, generic research assistant, or narrow organ-preservation-only tooling.

## Current positioning

BioSignal Navigator is an agent-human workspace for biotech R&D teams when experiments produce ambiguous readouts.

Core workflow:

```text
experimental observations
→ failure hypotheses
→ evidence
→ next best measurements
→ human expert review
```

The first demo vertical is living tissue systems: tissue preservation, organoids, organ-on-chip, tissue engineering QC.

## Critical constraints

- Do not read, print, or commit `.env` or secrets.
- App must work without any API keys via deterministic fallbacks.
- If partner API keys exist, use them opportunistically, but never make them required for the demo.
- Keep safety framing: research workflow only; not diagnosis, treatment, viability prediction, clinical decision support, or transplant/discard recommendation.
- Preserve the research/verification pipeline. Do not delete or bypass `docs/plans/research-validation-loop.md` or the `docs/research/` files.
- Favor concrete demo polish and credible workflow outputs over broad feature sprawl.

## Read first

1. `CLAUDE.md`
2. `README.md`
3. `docs/demo_script.md`
4. `docs/venture_positioning.md`
5. `docs/credentials_setup.md`
6. `docs/pioneer_strategy.md`
7. `docs/plans/research-validation-loop.md`
8. `docs/research/workflows-and-biomarkers.md`
9. `docs/research/dataset-feasibility.md`
10. `docs/research/evidence-matrix.md`
11. `docs/research/feature-gates.md`

## Priority A — Maintain and advance research/verification pipeline

Fill the placeholder research docs with concise, cited, product-relevant evidence. The goal is not a full literature review; it is to support demo claims and feature gates.

Update:

- `docs/research/workflows-and-biomarkers.md`
- `docs/research/dataset-feasibility.md`
- `docs/research/evidence-matrix.md`
- `docs/research/feature-gates.md`

Minimum expected content:

### Workflows and biomarkers

Compare these workflow domains:

1. organ preservation / perfusion
2. tissue engineering QC
3. organoids / organ-on-chip
4. ex-vivo drug testing
5. biomarker / assay planning workflows

For each, document:

- user/team
- workflow moment
- common readouts/signals
- decision/output
- uncertainty bottleneck
- why BioSignal Navigator could help

### Dataset feasibility

Score at least:

- PRJEB31843 — Tissue Stability Cell Atlas
- GSE293480 — human kidney NMP transcriptomics
- SRTR/OPTN public reports/data
- at least one organoid/tissue-engineering QC dataset or paper source if found quickly

For each, include:

- what it can support in the demo
- what it cannot support
- effort/risk
- recommended use: primary demo / evidence card / background only / skip

### Evidence matrix

Add concrete rows with:

- Claim
- Source / dataset
- Strength
- User-facing implication
- Product feature supported
- Caveat / do-not-claim

### Feature gates

Classify features:

Green:
- observation structuring
- uncertainty bottleneck
- evidence cards with caveats
- next-measurement suggestions
- human review question
- partner tech trace

Yellow:
- mechanism ranking
- cost/time saved estimate
- Pioneer/Gemini/Tavily live enrichment if credentials are available

Red:
- viability score
- transplant/discard recommendation
- diagnosis/treatment
- macro-to-micro prediction without paired data

## Priority B — Improve demo product without breaking fallback

Inspect current app and improve only if safe:

- Better visual hierarchy for the 2-minute demo.
- Make the `Uncertainty Bottleneck` section impossible to miss.
- Make `Partner Technology Trace` clear about live-vs-fallback status.
- Ensure `Pioneer-style triples` look like a deliberate side-challenge artifact, not a hack.
- Add or improve `docs/architecture.md`, `docs/partner_tech.md`, and `docs/submission_checklist.md` if missing.

## Priority C — Pioneer side-challenge implementation

Do **not** treat Pioneer as just another generic LLM provider if there is time to do better. The intended Pioneer use is a fine-tuned structured extractor that replaces a repeated frontier-LLM extraction call.

Read `docs/pioneer_strategy.md`, then implement the safest subset.

Preferred path:

- Use Pioneer / Fastino GLiNER2 for structured extraction from messy experiment notes.
- Target labels: macro signals, trends, sample context, candidate mechanisms, biomarkers/assays, uncertainty, safety-boundary flags.
- Target relations: observation supports possible mechanism, measurement reduces uncertainty about mechanism, and must-not-claim safety boundaries.
- If feasible, create a small synthetic dataset plan and eval harness for the fine-tuned model.
- If no live fine-tune can be completed, still make the app and docs show the intended Pioneer artifact clearly with a deterministic fallback extractor.

Success criterion for the side challenge:

> Pioneer owns the deterministic structured-extraction layer. Gemini can synthesize, Tavily can retrieve evidence, humans review; Pioneer turns messy notes into stable observations/mechanisms/measurements/relations/safety flags.

Implementation expectations:

- Add or improve `app/agents/pioneer_extractor.py`.
- Use `PIONEER_API_KEY` only if present; use `PIONEER_MODEL_ID` when available, otherwise default to the base GLiNER2 model.
- Never require credentials for the demo path.
- Surface status in the UI: `Pioneer: live fine-tuned model` or `Pioneer: fallback structured extractor`.
- Use the documented native inference shape: `POST https://api.pioneer.ai/inference` with `X-API-Key`, `model_id`, `text`, `schema`, and `threshold`.

## Priority D — Partner integration scaffolding

If time allows, add clean wrappers with fallbacks:

- `app/llm.py` for Gemini
- `app/search.py` for Tavily
- `app/agents/pioneer_extractor.py` for Pioneer GLiNER2-style extraction/evaluation

Important:

- Do not require real credentials.
- Do not fail if keys are missing.
- Do not make network calls in tests unless keys exist.
- Surface integration status in UI.

## Verification commands

Run before finishing:

```bash
source .venv/bin/activate
python -m compileall -q app
python - <<'PY'
from app.agents.pipeline import run_pipeline
r = run_pipeline('48h cold preserved tissue, lactate rising, pH falling, resistance increasing')
assert 'uncertainty_bottleneck' in r
assert 'partner_trace' in r
assert 'pioneer_triples' in r
assert r['measurements']
print('pipeline smoke ok')
PY
streamlit run app/main.py --server.port 8501 --server.address 127.0.0.1 --server.headless true &
sleep 5
curl -fsS http://127.0.0.1:8501/_stcore/health
```

If starting Streamlit in the background, clean it up after the health check.

## Git expectations

- Inspect `git diff` before committing.
- Commit only intentional files.
- Suggested commit message if successful:

```text
feat: strengthen hackathon research and partner scaffolding
```

## Final report format

When done, report:

1. Files changed
2. Research conclusions that affect the demo
3. Features added / improved
4. Partner integrations status
5. Verification commands run and results
6. Remaining manual tasks for Sacha, especially credentials / Aikido / video submission
