# Outreach List

Status: v1 — post-hackathon validation outreach (June 2026).

Goal: get **5–10 design-partner / feedback conversations** with the wedge segments
in `user-segments.md`. These are **target archetypes and where to find them**, not
scraped personal contacts — fill in real names/emails yourself (LinkedIn, paper
corresponding-author addresses, lab pages, the hackathon network). Prioritize
organoid/OoC and tissue-engineering first; perfusion contacts are for credibility,
not design-partnering.

## How to use

- Aim for the **workflow moment**, not a product pitch: "show me the last ambiguous
  result you had to troubleshoot." Validate before selling.
- Lead with the three validation questions (bottom of this doc).
- Keep it research/feedback framed — no clinical claims.

---

## Tier 1 — Organoid / organ-on-chip (contact first)

1. **Corresponding authors of recent organoid-QC / reproducibility papers** — e.g. the
   2025 organoid QC-framework and variability papers cited in `industry-landscape.md`.
   They have named the exact pain; ask if a troubleshooting copilot would help.
2. **R&D scientists at organoid/OoC companies** — Emulate, MIMETAS, TissUse, InSphero,
   CN Bio (and similar). Target bench scientists/platform engineers, not execs.
3. **Drug-discovery / safety-tox teams using OoC models** at pharma or CROs — the
   "toxicity vs model failure vs artifact" ambiguity is their daily problem.
4. **Academic organoid core-facility managers** — they see failure modes across many
   groups and feel QC variability acutely.

## Tier 2 — Tissue engineering / regenerative medicine

5. **QC leads / bioreactor operators at engineered-tissue startups** — post-culture
   QC-gate and batch-failure investigation owners.
6. **Regenerative-medicine PIs / translational tissue-engineering labs** — bridge
   academia↔startup; good for both feedback and intros.
7. **Cell-therapy process/assay-development scientists** — batch-release ambiguity is
   high-stakes and expensive.

## Tier 3 — Translational biology / biomarker (second feature)

8. **Biomarker scientists / lab leads designing assay panels** — validate the
   evidence-card + assay-planning half of the product.
9. **Translational-omics researchers** (e.g. tissue-stability / preservation omics
   authors behind PRJEB31843-type work) — relevance of evidence routing + caveats.

## Tier 4 — Broader biotech R&D troubleshooting (platform signal)

10. **R&D scientists who publicly complain about irreproducibility / failed assays**
    (LinkedIn, X, lab blogs) — warm, opinionated, fast to respond.
11. **CRO assay-development scientists** — see many clients' ambiguous readouts.
12. **Lab-data / ELN power users** (Benchling/Scispot communities) — test the
    "interpretation layer on top of our data" hypothesis.

## Tier 5 — Thesis-relevant / credibility (advisory, not design-partner)

13. **Perfusion / ex-vivo organ-preservation researchers** (NMP/HMP labs; authors of
    machine-perfusion viability reviews) — credibility, thesis anchor, demo feedback.
14. **Sacha's EPFL/ETH/Polytechnique ("poly") bioengineering contacts** — fast, honest
    technical feedback and warm intros into Tiers 1–2.
15. **Hackathon network** — Atira/{Tech: Europe} judges, mentors, and fellow finalists
    in bio/health; immediate, contextual feedback on the demo.

---

## Message template (feedback-first)

> **Subject:** 15 min on troubleshooting ambiguous [organoid / OoC / tissue] experiments?
>
> Hi [Name],
>
> I'm [Sacha], working on a research-workflow tool for biotech R&D teams. It helps you
> debug an **ambiguous experiment readout** — turning messy signals into possible
> mechanisms, evidence (with caveats), and the **single next measurement** that would
> reduce the uncertainty, with a human expert making the call. It is explicitly **not**
> diagnosis, viability prediction, or any clinical decision — just faster
> troubleshooting.
>
> I saw your work on [paper / platform / topic] and would value 15 minutes of brutal
> feedback. I'm not selling anything — I want to know whether this bottleneck is real
> for you and whether the tool would actually help.
>
> Three questions I'd love your take on:
> 1. Where do your **aggregate signals become ambiguous** (and you can't tell which
>    mechanism it is)?
> 2. Which **biomarkers/assays** do you actually trust vs distrust for that call?
> 3. Would an **evidence-routing + next-measurement** copilot help, or is the real
>    bottleneck somewhere else?
>
> Happy to share a 2-minute demo first if useful. Thank you!
>
> — [Sacha] · [link to repo/demo]

---

## Logging

Record answers in `docs/research/expert-notes.md` (one block per conversation:
segment, role, the ambiguity moment they named, trusted/distrusted markers, would-
use yes/no/why, and any feature request). Three "yes, this moment is real" from
Tier 1–2 is the gate to build wedge-specific features (see `decision-memo.md`).
