# BioSignal Navigator

**Agent-human troubleshooting for ambiguous biotech R&D experiments.**

When a biotech R&D experiment fails ambiguously, BioSignal Navigator turns messy run context into evidence-backed hypotheses, next discriminating measurements, and a human review decision.

## Hackathon framing

AI agents are entering healthcare through concrete workflows: documentation, coding, intake, monitoring, and workflow automation. BioSignal Navigator applies the same agentic-workflow pattern to **biotech R&D**:

> experimental observations → failure hypotheses → evidence → next best measurements → human expert review

The main demo path is **general biotech R&D troubleshooting**: start with a broad assay or custom workflow, then optionally show tissue preservation, organoids, and organ-on-chip as proof workflows inside the broader category.

BioSignal Navigator is **not** a diagnostic, treatment, transplant, or clinical decision system. It is a general biotech R&D troubleshooting workspace for experiment debugging.

The first demo vertical is living tissue systems, but it is only one use case inside a broader product category.

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

Start with a broad assay or custom workflow:

- signal dropped after a reagent-lot change;
- positive-control drift;
- worse edge wells;
- normal cell count;
- goal: choose the next discriminating measurement before rerunning the study.

Then optionally flash living-system cases such as cold-preserved tissue, organoids, or organ-on-chip to show category expansion. The app produces possible mechanisms, evidence grading, uncertainty branches, ranked next actions, human review, and an outcome loop that creates Pioneer training/eval rows.

## Partner technologies

Required minimum: 3 partner technologies. This repo makes partner use visible in the product and docs.

- **Google Gemini:** caveated troubleshooting-memo synthesis. Works with a native Gemini key (`AIza...`) or via **OpenRouter** (`sk-or...`, auto-detected) — see `docs/partner_tech.md`.
- **Tavily:** live literature / source retrieval for evidence cards when `TAVILY_API_KEY` is configured.
- **Pioneer:** deterministic GLiNER2-style structured extractor (signal → hypothesis → measurement triples + safety flags). Runs with no key; goes live with `PIONEER_API_KEY` **and** a deployed `PIONEER_MODEL_ID`.
- **Aikido:** security scan path for side challenge submission. The required screenshot should be attached as `docs/assets/aikido-security-report.png` before submission; do not fabricate it.

The demo remains fully usable without API keys via deterministic fallbacks. When keys are present, the UI shows a 🟢 LIVE vs ⚪ Fallback badge per partner and an honest partner trace. See `docs/architecture.md`, `docs/partner_tech.md`, and `docs/submission_checklist.md`.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m streamlit run app/main.py --server.port 8501
```

Use `python -m streamlit` (not the bare `streamlit` command) so it always runs from this
virtualenv rather than a different Streamlit that may be on your PATH.

The app binds to `127.0.0.1` (loopback) by default. Only expose it on the network when
you intentionally need remote access: `python -m streamlit run app/main.py --server.address 0.0.0.0`.

## Verification

```bash
source .venv/bin/activate
python -m compileall -q app
python -m streamlit run app/main.py --server.port 8501 --server.address 127.0.0.1 --server.headless true
curl -fsS http://127.0.0.1:8501/_stcore/health
```

## Security

No secrets are committed; all credentials load from `.env` (gitignored). Every partner
integration has a no-network fallback, all outbound calls use fixed endpoints with
timeouts, and the app binds to loopback by default. See [`SECURITY.md`](SECURITY.md) for
the full posture and disclosure policy. The repo is scanned with
[Aikido](https://www.aikido.dev/) (SCA, secrets, SAST) for the security side challenge.

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
