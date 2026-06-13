# Submission Checklist

{Tech: Europe} Munich AI Hackathon — submission deadline **Sunday 14:00**.

## Hard requirements

- [ ] Public GitHub repository with setup instructions (`README.md`).
- [ ] At least **3 partner technologies** used and documented (`docs/partner_tech.md`):
      Gemini + Tavily + Pioneer (Aikido as security side challenge).
- [ ] **2-minute video demo** recorded (script: `docs/demo_script.md`).
- [ ] Technical docs for jury evaluation (`docs/architecture.md`, `docs/partner_tech.md`,
      `docs/research/`).
- [ ] API/tool documentation (`docs/credentials_setup.md`, `.env.example`).

## Demo robustness

- [ ] App launches from README instructions.
- [ ] Default preset works with **no API keys** (deterministic fallback).
- [ ] With keys in `.env`, the UI shows 🟢 LIVE vs ⚪ Fallback per partner.
- [ ] Final card contains: mechanisms, evidence + caveats, next measurements,
      uncertainty bottleneck, and a human-review question.
- [ ] Agent orchestration trace is visible (Atira fit).

## Verification

```bash
source .venv/bin/activate
python -m compileall -q app
python - <<'PY'
from app.agents.pipeline import run_pipeline
r = run_pipeline('48h cold preserved tissue, lactate rising, pH falling, resistance increasing')
assert 'uncertainty_bottleneck' in r and 'partner_trace' in r and 'pioneer_triples' in r and r['measurements']
print('pipeline smoke ok')
PY
streamlit run app/main.py --server.port 8501 --server.address 127.0.0.1 --server.headless true &
curl -fsS --retry-connrefused --retry 15 --retry-delay 1 http://127.0.0.1:8501/_stcore/health
```

## Partner-specific

### Gemini
- [ ] `GEMINI_API_KEY` (OpenRouter `sk-or...` or native `AIza...`) set in `.env`.
- [ ] UI memo shows "🟢 LIVE · Memo synthesized via …".

### Tavily
- [ ] `TAVILY_API_KEY` set; evidence cards show live sources.

### Pioneer (Fastino) — 500€ side challenge
- [ ] Deterministic GLiNER2-style extractor visible in the UI — **this is the shipped artifact** (works with no key).
- [ ] Submission narrative ready (`docs/pioneer_strategy.md`).
- [ ] (Optional, not pursued for this build) deploy a fine-tuned model and set
      `PIONEER_MODEL_ID` to route extraction through a live Pioneer model.

### Aikido — 1000€ side challenge
- [ ] Free Aikido account created.
- [ ] Public repo connected to Aikido.
- [ ] Scan run; **screenshot of the security report with issue categories**
      saved under `docs/assets/` and referenced in the submission.

## Do-not-claim guardrails (keep in the pitch)

- No viability score, no transplant/discard recommendation.
- No diagnosis or treatment.
- No macro-to-micro prediction without paired data.
- Frame everything as research workflow + human review.
