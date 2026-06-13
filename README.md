# BioSignal Navigator

**Agent-human troubleshooting for ambiguous biotech R&D experiments.**

When a living-system experiment fails ambiguously, BioSignal Navigator turns messy readouts into failure hypotheses, evidence, next measurements, and a human review question.

## Hackathon framing

AI agents are entering healthcare through concrete workflows: documentation, coding, intake, monitoring, and workflow automation. BioSignal Navigator applies the same agentic-workflow pattern to **biotech R&D**:

> experimental observations → failure hypotheses → evidence → next best measurements → human expert review

The first demo vertical is **living tissue systems**: tissue preservation, organoids, organ-on-chip, and tissue engineering QC. This keeps the product venture-shaped while preserving a sharp thesis demo.

BioSignal Navigator is **not** a diagnostic, treatment, transplant, or clinical decision system. It is a research workflow tool for experiment troubleshooting.

## Why this can be a product

Biotech teams lose time and budget when experiments produce ambiguous signals. Senior scientists manually connect readouts, mechanisms, papers, protocols, and assay options before deciding what to run next.

BioSignal Navigator helps teams:

- structure messy experimental observations
- generate plausible biological failure mechanisms
- retrieve supporting and contradictory evidence
- suggest discriminating assays / biomarkers
- surface the uncertainty bottleneck
- escalate only the real judgment call to a human expert

## Demo scenario

A 48h cold-preserved ex-vivo tissue sample shows:

- rising lactate
- falling pH
- increasing vascular resistance
- uncertain oxygenation

The app produces a troubleshooting memo with possible mechanisms such as hypoxia, mitochondrial stress, endothelial dysfunction, inflammatory activation, and cell-type-specific degradation, then recommends measurements that would reduce uncertainty.

## Partner technologies

Required minimum: 3 partner technologies. This repo makes partner use visible in the product and docs.

- **Google Gemini:** caveated troubleshooting-memo synthesis. Works with a native Gemini key (`AIza...`) or via **OpenRouter** (`sk-or...`, auto-detected) — see `docs/partner_tech.md`.
- **Tavily:** live literature / source retrieval for evidence cards when `TAVILY_API_KEY` is configured.
- **Pioneer:** deterministic GLiNER2-style structured extractor (signal → hypothesis → measurement triples + safety flags). Runs with no key; goes live with `PIONEER_API_KEY` **and** a deployed `PIONEER_MODEL_ID`.
- **Aikido:** security scan path for side challenge submission.

The demo remains fully usable without API keys via deterministic fallbacks. When keys are present, the UI shows a 🟢 LIVE vs ⚪ Fallback badge per partner and an honest partner trace. See `docs/architecture.md`, `docs/partner_tech.md`, and `docs/submission_checklist.md`.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app/main.py --server.port 8501 --server.address 0.0.0.0
```

## Verification

```bash
source .venv/bin/activate
python -m compileall -q app
streamlit run app/main.py --server.port 8501 --server.address 127.0.0.1 --server.headless true
curl -fsS http://127.0.0.1:8501/_stcore/health
```

## Safety scope

Use language:

- possible mechanisms
- experiment troubleshooting
- evidence and caveats
- suggested measurements
- uncertainty bottleneck
- human review required

Avoid language:

- diagnosis
- treatment
- viability prediction
- clinical decision support
- transplant/discard recommendation
