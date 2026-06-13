# Partner Technologies

Required minimum: 3 partner technologies. BioSignal Navigator makes partner use
**visible in the product** (live-vs-fallback badges in the UI and an explicit
partner trace) rather than hiding it in the backend.

| Partner | Role in product | Live trigger | Fallback when absent |
|---|---|---|---|
| **Google Gemini** | Synthesizes the caveated troubleshooting memo | `GEMINI_API_KEY` / `OPENROUTER_API_KEY` | Deterministic memo from pipeline outputs |
| **Tavily** | Live literature/source retrieval for evidence cards | `TAVILY_API_KEY` | Curated evidence cards (PRJEB31843 etc.) |
| **Pioneer (Fastino)** | Structured signal → hypothesis → measurement extraction | _(optional)_ `PIONEER_API_KEY` + `PIONEER_MODEL_ID` | Deterministic GLiNER2-style extractor (**the shipped artifact**) |
| **Aikido** | Repository security scan (security side challenge) | Connected GitHub repo | Documented in submission checklist |

The demo runs fully on the fallbacks — keys only upgrade the experience.

## Gemini (`app/llm.py`)

Two live routes plus a deterministic fallback:

- **OpenRouter (OpenAI-compatible):** auto-detected when the key looks like an
  OpenRouter key (`sk-or...`), or when `OPENROUTER_API_KEY` / `GEMINI_BASE_URL`
  is set. Calls `{base}/chat/completions` with `requests`. Default model
  `google/gemini-2.5-flash` (override via `GEMINI_MODEL` / `OPENROUTER_MODEL`).
- **Native Gemini:** uses `google-generativeai` when `GEMINI_API_KEY` is a
  Google key (`AIza...`). Default model `gemini-2.5-flash`.

The prompt forbids diagnosis, viability prediction, and transplant/discard or
treatment recommendations, and requires a human-review close. The status line in
the UI shows the resolved provider and model.

## Tavily (`app/search.py`)

When `TAVILY_API_KEY` is set, the evidence step adds live sources (title, snippet,
URL) labelled "🟢 live (Tavily)" with a verify-this-lead caveat. Curated evidence
remains the reliable backbone; Tavily augments, never replaces it.

## Pioneer (`app/agents/pioneer_extractor.py`)

The side-challenge thesis: replace a repeated generic-LLM extraction call with a
small deterministic structured extractor. `extract_troubleshooting_structure()`
returns typed entities, candidate mechanisms, suggested measurements, relation
triples, and safety-boundary flags — repeatable for the same input.

- **Shipped artifact:** the deterministic extractor *is* the Pioneer artifact —
  the demo's Pioneer-style triples come from its relations. No credentials needed.
- **Optional live route (not pursued for this build):** set both `PIONEER_API_KEY`
  and a deployed `PIONEER_MODEL_ID`. The live request shape is conservative and
  guarded; confirm the contract against https://docs.pioneer.ai/introduction
  before relying on it.

See `docs/pioneer_strategy.md` for the GLiNER2 fine-tune plan, label schema,
synthetic-data plan, and eval plan.

## Aikido

No app runtime key. Deliverable: connect the public GitHub repo to Aikido, run
the scan, and include the report screenshot in the submission (see
`docs/submission_checklist.md`).

## fal (optional, not central)

`FAL_KEY` reserved for optional generative-media visualization. Not used in the
core demo; LLM endpoints do not count toward the fal side challenge.
