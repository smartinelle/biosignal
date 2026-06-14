# Pioneer Strategy — Fine-Tuned Structured Biology Extractor

## Why Pioneer matters for this project

Pioneer should not be treated as just another generic LLM endpoint. For the hackathon side challenge, the strongest use is:

> Fine-tune a small structured model that replaces a frontier LLM call for a narrow, high-value task in the BioSignal Navigator workflow.

The demo task should be narrow enough to evaluate and useful enough to justify the product:

> Extract structured troubleshooting signals from messy biotech experiment notes: observations, biological entities, failure mechanisms, assays/biomarkers, and relation triples linking them.

This fits Pioneer's strengths:

- fine-tuning open-source small/large models
- synthetic data generation
- custom evals against frontier models / benchmarks
- deployed inference
- downloadable weights
- GLiNER2 for deterministic structured extraction, NER, relation extraction, JSON extraction, and classification

## Recommended side-challenge path

Use **GLiNER2** as the Pioneer artifact if feasible.

Preferred base model candidates:

- `fastino/gliner2-base-v1`
- `fastino/gliner2-large-v1`
- `fastino/gliner2-multi-v1`
- `fastino/gliner2-multi-large-v1`

The pitch:

> Instead of calling a large general-purpose LLM every time we need structured observations, BioSignal Navigator uses Pioneer as the structured extraction layer: a fine-tuned small model that produces stable entities, classifications, relations, and safety flags that downstream agents can reason over.

## Concrete model task

### Input

Messy note from a scientist / operator, e.g.

```text
48h cold preserved tissue. Lactate rising, pH falling, vascular resistance increasing, oxygenation uncertain. Need to know whether this is hypoxia, endothelial injury, or metabolic failure and what to measure next.
```

### Output

Structured records such as:

```json
{
  "domain": "living_tissue_systems",
  "observations": [
    {"label": "lactate", "trend": "rising", "confidence": 0.92},
    {"label": "pH", "trend": "falling", "confidence": 0.90},
    {"label": "vascular_resistance", "trend": "increasing", "confidence": 0.88}
  ],
  "candidate_mechanisms": [
    {"label": "hypoxia", "confidence": 0.76},
    {"label": "endothelial_injury", "confidence": 0.67},
    {"label": "mitochondrial_dysfunction", "confidence": 0.61}
  ],
  "suggested_measurements": [
    {"label": "oxygen_consumption", "confidence": 0.73},
    {"label": "LDH", "confidence": 0.69},
    {"label": "histology", "confidence": 0.64}
  ],
  "relations": [
    {
      "subject": "lactate rising",
      "predicate": "supports_possible_mechanism",
      "object": "hypoxia",
      "confidence": 0.71
    },
    {
      "subject": "vascular resistance increasing",
      "predicate": "supports_possible_mechanism",
      "object": "endothelial injury",
      "confidence": 0.66
    },
    {
      "subject": "oxygen consumption",
      "predicate": "reduces_uncertainty_about",
      "object": "hypoxia",
      "confidence": 0.72
    }
  ]
}
```

## Label schema

Use a compact label schema so a small model can plausibly learn it quickly.

### Entity labels

- `macro_signal`
- `trend`
- `sample_context`
- `time_context`
- `candidate_mechanism`
- `biomarker`
- `assay`
- `uncertainty`
- `safety_boundary`

### Classification labels

- `domain_living_tissue_systems`
- `needs_human_review`
- `insufficient_evidence`
- `clinical_claim_risk`
- `research_workflow_only`

### Relation labels

- `supports_possible_mechanism`
- `contradicts_possible_mechanism`
- `reduces_uncertainty_about`
- `requires_human_review_for`
- `must_not_claim`

## Synthetic training data plan

Create a small dataset, not a huge one.

Minimum viable dataset:

- 100–200 synthetic examples for hackathon demonstration
- 20–40 held-out eval examples
- mix of clean and messy notes
- include negative/safety examples that mention diagnosis, treatment, transplant/discard decisions, or viability prediction and label them as `clinical_claim_risk` / `must_not_claim`

Training examples should cover:

1. cold preservation / perfusion
2. organoids
3. organ-on-chip
4. tissue engineering QC
5. ex-vivo drug testing
6. ambiguous or incomplete notes
7. unsafe clinical overclaim requests

## Evaluation plan

The eval should prove that the fine-tuned model replaces or improves a generic LLM call for a specific subtask.

### Benchmark fields

| Field | What it checks |
|---|---|
| `valid_schema` | Output parses to the expected JSON / label schema |
| `relation_extraction` | Correctness of observation→mechanism→measurement links |
| `repeatability` | Same input yields the same structured result across runs |
| `safety_flags` | Detection of clinical-claim risk and human-review requirements |

Suggested metrics:

- valid structured output rate
- entity F1 or approximate match rate
- relation extraction match rate
- safety-boundary detection recall
- latency / cost comparison vs frontier LLM call
- deterministic repeatability on same input

Comparison baseline:

- deterministic fallback extractor currently in the app
- optional generic frontier LLM extraction, if API keys are available
- Pioneer fine-tuned GLiNER2 model

## App integration expectation

Add `app/agents/pioneer_extractor.py` if missing.

The wrapper should expose one stable function, for example:

```python
def extract_troubleshooting_structure(note: str) -> dict:
    """Return observations, mechanisms, measurements, relations, and safety flags."""
```

Behavior:

- if `PIONEER_API_KEY` is present, call Pioneer's documented native inference endpoint (`POST /inference`) with `X-API-Key`
- if `PIONEER_MODEL_ID` is present, use it; otherwise default to the inference-ready base GLiNER2 model `fastino/gliner2-base-v1`
- if credentials are missing or the live call fails, use deterministic local fallback
- never fail the demo because Pioneer is unavailable
- surface status in the UI: `Pioneer: live fine-tuned model` vs `Pioneer: fallback structured extractor`

Do not hard-code undocumented endpoint shapes. Check the official Pioneer docs before implementing live API calls:

- https://docs.pioneer.ai/introduction

## Environment variables

```bash
PIONEER_API_KEY=...
# Optional; defaults to fastino/gliner2-base-v1 when omitted.
PIONEER_MODEL_ID=...
```

Optional only if the docs require it:

```bash
PIONEER_BASE_URL=...
```

## Submission narrative

Short version:

> We use Pioneer to fine-tune GLiNER2 into a deterministic biology troubleshooting extractor. It turns messy experiment notes into structured observations, mechanisms, measurements, and safety-boundary flags. This replaces a repeated frontier-LLM extraction call with a small model that is faster, cheaper, stable, and potentially runnable locally for sensitive biotech data.

Long version:

> BioSignal Navigator coordinates agents around ambiguous biotech experiments. The first step is turning noisy lab notes into reliable structure. Pioneer owns the structured-extraction layer: a fine-tuned GLiNER2 model extracts macro signals, candidate mechanisms, assays, uncertainty flags, safety flags, and relations. Gemini can still synthesize the final memo, Tavily can retrieve evidence, and humans still make judgments — but Pioneer makes the downstream workflow robust and measurable.

## What not to do

- Do not use Pioneer only as a generic chat model provider if there is time to build the GLiNER2 path.
- Do not claim the model predicts viability or hidden tissue state.
- Do not claim clinical correctness.
- Do not make the app dependent on Pioneer credentials.
- Do not commit training secrets, API keys, or downloaded private weights.
