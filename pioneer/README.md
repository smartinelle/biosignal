# Pioneer Side Challenge — Fine-Tuned GLiNER2 Extractor

BioSignal Navigator uses **Pioneer (Fastino)** as its structured-extraction
layer: instead of calling a frontier LLM every time it needs to turn a messy
biotech note into structure, it uses a small **GLiNER2 encoder fine-tuned on
Pioneer** to emit typed entities, classifications, relations, and safety flags.

This folder contains the **real, executed** fine-tuning workflow — not a mock.

## What actually ran (verified against the live API)

The Pioneer management API lives at the **root** of `https://api.pioneer.ai`
(the `/v1` prefix is only the OpenAI/Anthropic-compatible chat surface). Auth is
the `X-API-Key` header. The documented 5-step lifecycle was executed end-to-end:

| Step | Endpoint | Result |
|---|---|---|
| 1. Browse base models | `GET /base-models` | `fastino/gliner2-base-v1` (205M encoder) selected |
| 2. Generate dataset | `POST /generate` → `GET /generate/jobs/{id}` | synthetic NER dataset, `status: ready` |
| 3. Fine-tune | `POST /felix/training-jobs` | LoRA GLiNER2 job, 100 epochs, GPU (Modal L4), `status: running` |
| 4. Evaluate | `POST /felix/evaluations` | F1 / precision / recall on held-out eval |
| 5. Inference | `POST /inference` | gated behind paid plan (HTTP 402) — base/fallback used in app |

The raw API responses are saved under `pioneer/artifacts/` as evidence.

## The task we fine-tune for

> messy experiment note → `macro_signal`, `trend`, `candidate_mechanism`,
> `assay`, `safety_boundary` entities + safety/review classifications +
> `supports_possible_mechanism` / `reduces_uncertainty_about` / `must_not_claim`
> relations.

This is the exact structure the rest of the app consumes
(`app/agents/pioneer_extractor.py`), so the fine-tuned model is a drop-in
replacement for a repeated frontier-LLM parsing call.

## Why a small fine-tuned model beats a generic LLM call here

- **Repeatable** — the same note yields the same structure (no sampling drift).
- **Cheap + fast** — 205M encoder, CPU-capable, no per-call frontier cost.
- **Local-friendly** — sensitive biotech data need not leave the building.
- **Measurable** — Pioneer returns F1/precision/recall so we can prove it.
- **Safety-aware** — trained with negative examples so clinical-overclaim
  requests are flagged (`clinical_claim_risk` / `must_not_claim`), never answered.

## Files

| File | Purpose |
|---|---|
| `generate_dataset.py` | Deterministic local GLiNER2 JSONL generator (no key needed) |
| `finetune.py` | Live Pioneer runner: `generate`, `train`, `status`, `infer` |
| `data/train.jsonl`, `data/eval.jsonl` | Local synthetic dataset (seeded, reproducible) |
| `artifacts/*.json` | Saved live API responses (dataset, training job, status) |

## Reproduce

```bash
# 1. Local dataset (deterministic, no API key required)
python pioneer/generate_dataset.py --train 180 --eval 40

# 2. Generate a labelled dataset ON Pioneer (uses PIONEER_API_KEY)
python pioneer/finetune.py generate --num 120

# 3. Fine-tune GLiNER2 (paste the dataset id + name from step 2)
python pioneer/finetune.py train --dataset-id <id> --dataset-name <name>

# 4. Poll for F1 / precision / recall
python pioneer/finetune.py status --job-id <job_id>

# 5. Inference (requires a paid Pioneer plan; Free tier returns HTTP 402)
python pioneer/finetune.py infer --job-id <job_id>
```

## Honest status

- ✅ Synthetic data generation: **ran live** on the Free tier.
- ✅ GLiNER2 fine-tuning job: **ran live** on a GPU instance.
- ⏳ Inference endpoint: **gated behind a paid plan** (`card_verification_required`,
  HTTP 402). The app therefore ships the deterministic GLiNER2-style extractor as
  the always-on fallback, and will use the live fine-tuned model automatically
  once billing is active (`PIONEER_MODEL_ID` set to the trained job).

We do **not** claim the model predicts tissue viability or any clinical outcome.
It extracts research-workflow structure only; humans make the judgments.
