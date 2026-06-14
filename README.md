# BioSignal Navigator

**An agent–human investigation workspace for ambiguous biotech R&D experiments. It generates a live decision tree, routes the scientist to the next measurement, and learns from every decision.**

When an experiment gives ambiguous signals — a perfused tissue declining at 48h, a qPCR run drifting — BioSignal Navigator doesn't guess an answer. It generates a **branching decision tree upfront**, walks the scientist **node by node** to the measurement that best reduces uncertainty (backed by real papers), and resolves to a leading mechanism plus the confirmatory assay and molecular targets. **Every human decision becomes labeled training data** that fine-tunes the extractor over time.

> raw observations → structured extraction → hypotheses → evidence → next measurement → **human decision** → resolution → training data ↺

## What makes it different

- **It preserves uncertainty instead of faking an answer.** Most AI tools collapse ambiguity into one confident output. This one keeps it as a decision graph, makes the human decide at each node, and escalates the irreducible judgment — built for a domain where being honest about what you don't know is the point.
- **It's a real small-model system, not a wrapper.** A **GLiNER2 model fine-tuned on Pioneer (val loss 1.83)** replaces a generic LLM call for structured extraction — small, fast, private, and domain-specialized.
- **It improves itself.** Each recorded decision is written as a labeled training row (JSONL, in the exact fine-tune format) → re-fine-tune Pioneer → sharper extraction and routing. A data flywheel from real lab decisions.
- **Any query works.** Run the curated ex-vivo preservation workflow, or paste *any* experiment note and the decision tree is generated dynamically from the agent pipeline.

## Technical highlights

- **Live multi-agent pipeline** (5 agents) orchestrating **3 partner APIs**, with deterministic fallbacks so it never crashes without keys.
- **Decision-tree engine** — curated *and* dynamically generated trees, rendered live (graphviz) with the chosen path and resolution.
- **Tiered evidence retrieval** — ranks sources by trust (peer-reviewed > vendor/protocol > general web), drops junk (forums/social/blogs), blends relevance + trust, guarantees ≥1 peer-reviewed source.
- **Self-improving data flywheel** — SQLite store of every decision, exportable as fine-tune-ready JSONL.
- **Fine-tuned GLiNER2 on Pioneer** — synthetic dataset + eval (`pioneer/`), live `/inference` with deterministic fallback.
- **Secure build** — passes Aikido (SCA/secrets/SAST): dependency CVE floors, SSRF guard on outbound calls, no committed secrets. See [`SECURITY.md`](SECURITY.md).

## Partner technologies (live, each with a deterministic fallback)

| Partner | Where in code | Where in UI | What it does |
|---|---|---|---|
| **Pioneer** | `app/agents/pioneer_extractor.py` (+ `pioneer/` fine-tune) | 🔧 How it worked | Fine-tuned GLiNER2 extracts typed **signals, mechanisms, measurements + relations + safety flags** — replacing a generic LLM extraction call. |
| **Tavily** | `app/search.py` | 📚 Evidence & resources + inline node papers | Trust-tiered, score-ranked **literature retrieval** (real DOIs). |
| **Google Gemini** | `app/llm.py` (native `AIza…` or OpenRouter `sk-or…`, auto-detected) | 📚 Evidence & resources | Synthesizes the **caveated troubleshooting memo**. |
| **Aikido** | repo security scan | — | Most-secure-build side challenge; findings fixed. |

The app runs fully without keys (deterministic fallbacks); with keys, the sidebar shows live 🟢 badges per partner. See `docs/partner_tech.md` and `docs/architecture.md`.

## How to use

1. **Setup** — pick the curated ex-vivo tissue preservation demo, or **Custom query** to paste any experiment note.
2. **Investigate** — at each node, run the suggested measurement (with the paper that justifies it) and record what you observed; the tree advances and narrows.
3. **Resolution** — leading mechanism, confirmatory assay, molecular targets, mandatory human review.
4. **Reference tabs** — 🌳 Decision tree, 📚 Evidence & resources (live Tavily + Gemini memo), 🗄️ Training data (the flywheel + JSONL export), 🔧 How it worked (agents + partner trace + Pioneer triples).

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
integration has a no-network fallback, all outbound calls use fixed/validated endpoints
with timeouts and an SSRF guard, and the app binds to loopback by default. See
[`SECURITY.md`](SECURITY.md) for the full posture. The repo is scanned with
[Aikido](https://www.aikido.dev/) (SCA, secrets, SAST) for the security side challenge.

## Safety scope

This is a **research workflow / experiment-troubleshooting** tool. It speaks in possible
mechanisms, suggested measurements, evidence with caveats, and explicit uncertainty —
and it requires human review. It is **not** diagnosis, treatment, viability prediction,
clinical decision support, or any transplant/discard recommendation.
