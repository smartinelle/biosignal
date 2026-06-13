# Feature Gates

Status: v1 — classified against research validation v1 and evidence matrix v1.

---

## Green — Build now

These features are evidence-backed, demoable, and safe within the research workflow framing.

| Feature | Evidence support | Demo value | Notes |
|---|---|---|---|
| **Observation structuring** | All workflow domains share ambiguous multi-signal readouts; structuring is the entry point | High — shows agent-first design | Observation Agent: detect signals, domain, uncertainty level |
| **Uncertainty bottleneck** | Core finding from all literature: markers are underdetermined, thresholds lack consensus | High — Atira fit; differentiates product from generic chatbot | Must be impossible to miss in UI; is the product's core philosophical claim |
| **Evidence cards with caveats** | Every source reviewed carries explicit limitations; source-aware output is safe | High — builds credibility with scientific audience | Must include strength level and caveat per card; do not assert validated thresholds |
| **Next-measurement suggestions** | All workflow domains have a natural "next assay" question; evidence supports gap between macro signals and molecular truth | High — concrete actionable output | Frame as "research suggestion"; not a protocol mandate |
| **Human review question** | No workflow validated for autonomous decision; escalation is the correct output | High — Atira track fit; shows agent-human coordination | Must be specific to the case; not a generic disclaimer |
| **Partner tech trace** | Jury-visible; Atira and Pioneer side challenge both reward visible orchestration | High — judging criterion | Show live vs fallback status per integration; do not hide fallback |
| **Multiple demo presets** | Three workflow domains are covered by evidence: tissue preservation, organoid QC, organ-on-chip | High — shows generality of platform claim | Keep presets grounded; organoid/organ-on-chip presets are demo-shaped, not dataset-backed |

---

## Yellow — Build as mock/explainer with explicit caveat

These features add demo value but require explicit uncertainty framing. Show them as explainers, not validated outputs.

| Feature | Evidence support | Demo value | Required caveat |
|---|---|---|---|
| **Mechanism ranking** | Literature supports plausible mechanisms but no validated ranking model exists | Medium — shows agent reasoning | "Ranked by plausibility based on reported literature; requires assay confirmation." |
| **Cost / time saved estimate** | Reasonable claim: structured troubleshooting reduces wasted cycles, but no RCT evidence | Medium — business narrative | "Estimated; not based on controlled study." |
| **Gemini live mechanism synthesis** | Gemini can produce plausible text; quality depends on prompt | Medium — shows real partner tech | Show "live" vs "fallback" clearly; fallback must remain demoable |
| **Tavily live evidence retrieval** | Tavily can retrieve web/literature content; quality and relevance varies | Medium — shows evidence routing | Show "live" vs "fallback"; curated fallback is more reliable for demo |
| **Pioneer live extraction/evaluation** | Pioneer can replace generic LLM call for structured extraction; requires API key and prompt engineering | Medium — side challenge visibility | Show "live" vs "fallback"; triples must be recognizable as structured artifact, not just JSON |

---

## Red — Do not build

These features are unsafe, too speculative, regulated, or unsupported by available evidence.

| Feature | Why not |
|---|---|
| **Viability score** | No validated thresholds in any literature source; binary or numeric output implies unwarranted precision; overclaims in regulated context |
| **Transplant / discard recommendation** | Clinical decision; regulated; no available evidence base supports autonomous recommendation; would invalidate Atira fit claim |
| **Diagnosis or treatment recommendation** | Outside research workflow scope; clinically regulated; not appropriate for a hackathon demo |
| **Macro-to-micro prediction without paired data** | No paired dataset available; all sources (GSE293480, PRJEB31843) are study-specific and underpowered for prediction; would be demonstrably false claim |
| **Validated threshold alerts** | No validated thresholds exist (Watson & Jochmans 2018; 2024 systematic review); displaying a threshold would mislead users |
| **Patient-level clinical advice** | Not a clinical product; no IRB; not within scope |
| **fal generative media as core feature** | Only relevant if visualization is central; LLM endpoints do not count for fal side challenge; adds complexity without demo value |

---

## Gate logic for new features

Before building any new feature, answer:

1. Does at least one source support the underlying biomarker, workflow step, or biological claim?
2. Does the output include an explicit caveat if the claim is not validated?
3. Is the feature framed as a research suggestion, not a clinical recommendation?
4. Can the fallback (no API keys) still demonstrate the feature?

If all four are yes → Green / proceed.
If 1–2 fail but demo value is high → Yellow / add explicit caveat.
If any of the Red categories applies → do not build.
