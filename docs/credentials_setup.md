# Hackathon Partner Credentials Setup

Do **not** commit real credentials. Copy `.env.example` to `.env` locally and fill values there.

```bash
cp .env.example .env
```

## Required / high-value

### Google Gemini

Purpose: mechanism synthesis, caveated memo generation, and final troubleshooting summary.

Environment variable:

```bash
GEMINI_API_KEY=...
```

Implementation expectation:
- App must work without the key via deterministic fallback.
- When present, Gemini should enrich mechanism generation and/or final memo synthesis.

### Tavily

Purpose: retrieve current literature/web evidence and source snippets for evidence cards.

Environment variable:

```bash
TAVILY_API_KEY=...
```

Implementation expectation:
- App must work without the key via curated evidence fallback.
- When present, Tavily augments evidence cards with sources and caveats.

### Pioneer / Fastino

Purpose: side-challenge-visible fine-tuned structured extraction/evaluation. Pioneer should ideally replace a repeated generic LLM extraction call, not merely act as another chat provider.

Recommended artifact:
- fine-tune GLiNER2 on a narrow BioSignal Navigator task
- extract observations, candidate mechanisms, assays/biomarkers, relations, uncertainty, and safety-boundary flags from messy experiment notes
- compare against deterministic fallback and/or generic LLM extraction
- show why a small deterministic model is faster, cheaper, stabler, and potentially local/private for sensitive biotech data

Environment variables:

```bash
PIONEER_API_KEY=...
# Optional; defaults to fastino/gliner2-base-v1 when omitted.
PIONEER_MODEL_ID=...
```

Optional, only if Pioneer docs require it:

```bash
PIONEER_BASE_URL=...
```

Implementation expectation:
- App must show Pioneer-style triples even without credentials.
- With `PIONEER_API_KEY`, route extraction/evaluation through Pioneer's documented `POST /inference` endpoint if feasible; use `PIONEER_MODEL_ID` when set, otherwise the base GLiNER2 model.
- Document exactly what Pioneer replaces or improves vs a generic LLM call.
- See `docs/pioneer_strategy.md` for the model task, label schema, synthetic data plan, eval plan, and submission narrative.

Onboarding resources:
- Platform: https://pioneer.ai/
- Docs: https://docs.pioneer.ai/introduction
- Discord support: https://discord.gg/yCG3FjXvfp
- Hackathon promo code for Pro: `Munich2026HackPioneer`

## Side-prize / optional

### Aikido

Purpose: security side challenge.

No app runtime key is expected unless the hackathon account flow requires one. The likely deliverable is:

- connect public GitHub repo to Aikido
- run scan
- include screenshot / report summary in submission docs

Add screenshot path under `docs/assets/` if available, but do not commit secrets.

### fal

Purpose: optional visualization / generative media side challenge. Only use if it becomes central to the demo.

Environment variable:

```bash
FAL_KEY=...
```

Current default: do not make fal central; partner stack is Gemini + Tavily + Pioneer + Aikido.

## Verification after adding keys

```bash
source .venv/bin/activate
python -m compileall -q app
streamlit run app/main.py --server.port 8501 --server.address 127.0.0.1 --server.headless true
curl -fsS http://127.0.0.1:8501/_stcore/health
```

If keys are configured, run one demo case and confirm the UI clearly shows which integrations were used and which fallbacks were used.
