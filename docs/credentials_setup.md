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

Purpose: side-challenge-visible structured extraction/evaluation: observation → failure hypothesis → next measurement triples.

Environment variable:

```bash
PIONEER_API_KEY=...
```

Implementation expectation:
- App must show Pioneer-style triples even without credentials.
- With credentials, route extraction/evaluation through the provider if feasible.
- Document exactly what Pioneer replaces or improves vs a generic LLM call.

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
