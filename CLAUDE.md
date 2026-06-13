# BioSignal Navigator — Project Context

## Mission

Build a hackathon demo for **BioSignal Navigator**: an agent-human evidence routing tool that turns messy biomedical observations into molecular hypotheses, evidence, suggested measurements, and a human review question.

This is **not** a diagnostic, treatment, or clinical decision system. It is a research workflow / translational evidence-routing demo.

## Hackathon framing

Primary track fit: **Atira — Orchestrating Agents and Humans**.

Core claim:
> We help biomedical teams ask the right biological question faster by coordinating agents and humans around uncertainty.

Do not claim:
- viability prediction
- diagnosis
- treatment recommendation
- transplant/discard decision
- macro variables directly infer molecular truth

Use language:
- possible mechanisms
- evidence routing
- suggested measurements
- uncertainty and caveats
- human review required
- research workflow

## MVP demo case

Default demo vertical: **tissue preservation / tissue engineering viability**.

Input example:
> Context: ex vivo preserved tissue sample. Preservation duration: 48h cold storage. Macro signals: lactate rising, pH falling, vascular resistance increasing, oxygenation uncertain. Goal: understand possible molecular degradation processes and what measurements would reduce uncertainty.

Expected output:
- structured observations
- top molecular/physiological hypotheses
- relevant literature/dataset evidence with caveats
- suggested assays/biomarkers
- explicit human review question

Anchor evidence:
- Madissoon et al., Tissue Stability Cell Atlas / PRJEB31843
- Human lung, spleen, esophagus tissue stability after cold preservation
- 4°C HypoThermosol FRS
- timepoints: 0h, 12h, 24h, 72h
- key qualitative claim: relative transcriptomic stability up to ~24h; more tissue/cell-type-specific degradation signals at 72h in some tissues

## Partner technologies to show in README/demo

Required minimum: 3 partner technologies.

Core:
1. **Google Gemini** — synthesis, mechanism mapping, final evidence card.
2. **Tavily** — literature/dataset search and source extraction.
3. **Pioneer** — structured extractor/evaluator for observation → mechanism → biomarker triples.

Side prize:
4. **Aikido** — security scan screenshot and clean repo.

Optional:
5. **fal** — only if we add visualization; do not make it central unless genmedia is the main feature.

## Current stack

- Python 3.11
- Streamlit UI
- small modular agent files under `app/agents/`
- curated fallback data in `app/data/`

Run locally:
```bash
cd /root/projects/biosignal-navigator
source .venv/bin/activate
streamlit run app/main.py --server.port 8501 --server.address 0.0.0.0
```

Verify:
```bash
python -m compileall -q app
curl -fsS http://127.0.0.1:8501/_stcore/health
```

## File ownership for parallel agents

Avoid merge conflicts. Each coding agent should own a narrow surface.

- UI agent: `app/main.py`, `docs/demo_script.md`
- Gemini/LLM agent: `app/llm.py`, `app/agents/mechanism_agent.py`, `app/agents/pipeline.py`
- Tavily/evidence agent: `app/search.py`, `app/agents/evidence_agent.py`, `app/data/`
- Pioneer agent: `app/agents/pioneer_extractor.py`, `data/triples_*`, `docs/partner_tech.md`
- Docs/submission agent: `README.md`, `docs/architecture.md`, `docs/partner_tech.md`, `docs/submission_checklist.md`
- Review agent: read-only review first; edit only after explicit handoff

If two agents need the same file, one should produce a patch plan or notes, not edit directly.

## Code standards

- Keep the demo robust without API keys: every integration must have a fallback.
- Do not read or commit `.env` or secrets.
- Keep generated local artifacts out of git: `.venv/`, `__pycache__/`, `.env`.
- Prefer small functions and simple JSON-like dict outputs.
- Preserve the safety framing in user-visible outputs.
- Add clear caveats to evidence claims.

## Definition of done for hackathon MVP

- App launches from README instructions.
- Demo preset works without any API key.
- If Gemini/Tavily keys exist, app uses them; if not, fallback still works.
- The agent trace visibly shows multi-agent orchestration.
- Final card contains mechanisms, evidence, measurements, uncertainty, and human review question.
- README explicitly documents partner technologies.
- 2-minute demo script exists.
- Aikido scan screenshot or placeholder instructions exist.
