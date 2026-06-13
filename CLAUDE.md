# BioSignal Navigator — Project Context

## Durable context first

This repo is for Sacha Martinelle's {Tech: Europe} Munich AI Hackathon build. The **hackathon facts, prize landscape, and Sacha's thesis goals are durable context**. The precise product idea may change during the hackathon; agents should preserve this upstream context and update the product-specific sections only when the chosen idea changes.

## Hackathon context

Event: **{Tech: Europe} Munich AI Hackathon** at Tacto Office, Sandstraße 33, 80335 München.

Key deadlines and deliverables:
- Project submission deadline: **Sunday 14:00**.
- Finalists announced: **Sunday 15:00**.
- Finalist pitches: **Sunday 15:15**.
- Award ceremony: **Sunday 16:30**.
- Team size: max **5** people.
- Must use at least **3 partner technologies** from the provided resources.
- Submission requires a **2-minute video demo** and a **public GitHub repository** with setup instructions, API/tool documentation, and enough technical docs for jury evaluation.

Competition mode:
- Stage 1: pre-selection, with 5 finalist teams total: **3 Open Track winners** and **2 Track winners**. Criteria: creativity, technical complexity, and bonus points for effective partner technology use.
- Stage 2: finalists give a **5-minute live presentation**; jury selects top 3 winners.

Prize landscape:
- Overall pool: **>10k€** distributed across cash, hardware, and credits.
- **Atira track — Orchestrating Agents and Humans:** AirPods per team member. Strong fit if the project visibly coordinates agents + humans + long-running context/uncertainty.
- **Kyrall track — Turning technical drawings into 3D parts:** AirPods per team member. Not thesis-aligned unless we pivot to manufacturing/engineering.
- **Open Innovation:** 3 finalist-stage qualification slots. Useful fallback if track fit becomes weak.
- **Fastino / Pioneer side challenge:** 500€ for best use of Pioneer. They want a model that replaces/outperforms a general-purpose LLM API call, thoughtful use of synthetic data/evals/adaptive inference, and bonus for GLiNER2/Gemma 4.
- **Aikido side challenge:** 1000€ for most secure build; requires free Aikido account, repo connection, and screenshot of security report with issue categories. High expected value; do it regardless of product.
- **fal side challenge:** $1000 fal credits for best use of fal. Only worth targeting if generative media becomes a core feature; LLM endpoints do not count.
- Finalist stage prizes: **1st: $5k Gemini credits + Pioneer Pro 1 month; 2nd: $2.5k Gemini credits + Pioneer Pro 1 month; 3rd: $1k Gemini credits + Pioneer Pro 1 month.**

Partner technology resources to plan around:
- Google DeepMind / Gemini frontier models.
- Pioneer by Fastino.
- fal generative media platform.
- Tavily real-time search, extraction, research, and crawling.

## Sacha context and thesis goals

Sacha's thesis direction: **autonomous life-support / ex-vivo organ monitoring**, with a focus on organ preservation, tissue engineering, perfusion workflows, and how to reason about hidden tissue state.

Core intellectual pull:
- Medicine and surgery often reason from **macro-scale variables**: lactate, pH, flow, vascular resistance, oxygenation, temperature, visual appearance, enzyme/injury markers, decision trees.
- Tissue failure/degradation often happens at **micro/molecular scale**: hypoxia, mitochondrial dysfunction, inflammation, endothelial injury, apoptosis/necrosis, cell-type shifts, RNA/tissue degradation, spatial/tissue architecture changes.
- The thesis opportunity is the bridge: **how can sensors, data analysis, omics, imaging, and agentic workflows help researchers or clinicians ask better questions about hidden biological state?**

Personal/build goal for the hackathon:
- Produce a **sendable artifact** that compounds the thesis, not just a generic hackathon toy.
- Show founder-track taste: ambitious, original, technically grounded, but honest about uncertainty and regulation.
- Use the hackathon to create proof of direction: a demo, repo, and narrative that can be sent to technically strong people / thesis contacts / poly friends.

Strategic product constraints:
- Avoid overclaiming. A 1-day hackathon cannot genuinely solve macro → micro biological inference or clinical viability prediction.
- Prefer **evidence routing, hypothesis generation, assay/measurement recommendation, and human-in-the-loop uncertainty escalation** over diagnosis or decision automation.
- The product can be broader than organ preservation, but the first demo should stay close to Sacha's thesis: tissue preservation, tissue engineering QC, ex vivo perfusion, organoid/organ-on-chip, or translational biology workflows.

## Current working product idea

Current candidate: **BioSignal Navigator** — an agent-human evidence routing tool that turns messy biomedical observations into molecular hypotheses, evidence, suggested measurements, and a human review question.

This is **not fixed**. If the product idea changes, keep the hackathon context and Sacha thesis context above intact, then update this section and downstream implementation tasks.

This is **not** a diagnostic, treatment, or clinical decision system. It is a research workflow / translational evidence-routing demo.

## Track framing

Primary current track fit: **Atira — Orchestrating Agents and Humans**.

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
