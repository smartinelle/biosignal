# Product Research Sprint

Status: v1 — product-definition sprint for BioSignal Navigator (June 2026).

This is the synthesis doc. It evaluates which product BSN should become, grounded
in the industry scan (`industry-landscape.md`), the segment scorecard
(`user-segments.md`), and the prior research/evidence docs. The recommendation is
opinionated; the formal decision is in `decision-memo.md`.

---

## TL;DR

- **Product category (company):** an **agent–human troubleshooting workspace for
  ambiguous living-tissue R&D experiments** — the *interpretation layer* between raw
  readouts and the next experiment. (Scope ladder Level 2–3.)
- **First wedge (GTM):** **organoid / organ-on-chip / tissue-engineering QC failure
  investigation** — high pain, low regulation, reachable buyers, thesis-aligned.
- **Demo proof (hackathon):** the **ex-vivo tissue-preservation failure** case — most
  visceral, thesis-resonant, and anchored by a real dataset (PRJEB31843).
- **Hard boundary:** never claim viability, transplant/discard, diagnosis, treatment,
  or macro→micro prediction. The differentiator is *uncertainty-first*, the opposite
  of the device vendors now marketing "real-time viability assessment."

---

## Strongest product-category candidates

| # | Candidate | Strength | Weakness | Call |
|---|---|---|---|---|
| 1 | Ex-vivo biological state monitoring | Thesis core; visceral macro/micro gap | Collides with device viability framing; transplant-regulated | **Demo, not GTM** |
| 2 | Translational biomarker / assay-planning copilot | Broad; literature-grounded; safe | Risks generic feel without a sharp readout demo | **Second feature** |
| 3 | Machine-perfusion evidence router | Sharpest thesis demo | Narrow buyer; regulated; device-adjacent | **Demo vertical only** |
| 4 | **Tissue-engineering / organoid / OoC QC troubleshooting** | Best pain × reachability × low regulation × thesis fit | Smaller logos than pharma | **First wedge ✅** |
| 5 | Horizontal biotech R&D troubleshooting platform | Largest TAM; the eventual vision | Too broad to enter cold | **Platform vision** |

The winner is a **Level-2/3 platform** (living-tissue state interpretation /
troubleshooting) entered through the **organoid/OoC QC wedge** (Level-0/1 proof),
exactly the altitude the validation loop recommended.

---

## Target users

- **Primary (build for):** R&D scientists and platform engineers on organoid /
  organ-on-chip / engineered-tissue teams and the CROs running these models.
- **Secondary:** translational-biology / biomarker scientists doing assay/panel design.
- **Demo persona (resonates, don't sell first):** perfusion / preservation researchers.

---

## Workflow moment

The product fires at one specific, repeated moment:

> A living-tissue experiment produced an **ambiguous multimodal readout** and the team
> must decide **what to run next** before burning another batch/cycle.

Concretely: a borderline viability stain + rising media lactate + uncertain
differentiation marker (organoid), or barrier leak + inflammatory marker + O₂ shift
after compound exposure (OoC), or rising lactate / falling pH / rising resistance
in a preserved tissue (preservation demo). Today this is resolved by a senior
scientist manually connecting readouts → mechanisms → literature → protocols → next
assay. That manual loop is the thing BSN compresses.

---

## The painful ambiguity / bottleneck

All target workflows share one structure:

```
macro / aggregate signal
  → multiple plausible mechanisms
  → no single bulk signal can discriminate them
  → senior-scientist judgment on an ambiguous readout
  → another expensive experiment cycle
```

The bottleneck is **not missing data — it is missing interpretation**. Devices and
imaging tools produce more numbers; nobody routes those numbers to *mechanisms +
evidence + the single next discriminating measurement*. BSN's core claim is that it
**narrows** the ambiguity and **names the measurement that resolves it fastest**,
rather than pretending to resolve it.

---

## Why now

- **The pain is large and expensive.** ~50%+ of preclinical research is
  irreproducible, ~**\$28B/yr in the US** (~\$90B globally); industry replication of an
  academic result costs **\$0.5–2M and 3–24 months**; Amgen reproduced only **11%** of
  53 landmark cancer papers.
  [Freedman et al., PLOS Biology 2015](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1002165),
  [Science News summary](https://www.sciencenews.org/article/irreproducible-life-sciences-research-us-costs-28-billion)
- **The wedge pain is acute and documented.** Organoid/OoC variability and the lack
  of standardized QC are named as primary blockers to translation ("3R": reproducibility,
  regulatory frameworks, real-time monitoring).
  [Organoid QC framework (Nature Sci Reports 2025)](https://www.nature.com/articles/s41598-025-14425-x),
  [Organoids review 2025](https://link.springer.com/article/10.1007/s00018-025-05692-y)
- **Agentic AI in R&D is crossing the adoption line.** Benchling's 2026 report says
  **89% of scientists** use copilots/reasoning tools as a first stop; the field is
  shifting toward agentic "research & prediction."
  [Benchling 2026 Biotech AI Report](https://www.benchling.com/biotech-ai-report-2026),
  [Agentic AI in R&D (pharmaphorum)](https://pharmaphorum.com/digital/agentic-ai-shift-rd-rp-will-deliver-first-predictive-drug-pipeline-2026)
- **Why AI agents specifically:** the task is multi-step reasoning over heterogeneous
  evidence (signals → mechanisms → literature → assays) with explicit uncertainty and
  a human handoff — a coordination problem, which is precisely the agent-orchestration
  shape (and the Atira track thesis).

---

## Why Sacha / thesis fit

- Sacha's thesis is the **macro→micro bridge**: how sensors, omics, imaging, and
  agentic workflows help reason about **hidden biological state**. BSN *is* that
  bridge, productized as an interpretation layer.
- The organoid/OoC wedge keeps the thesis intact (hidden tissue-state interpretation)
  while **shedding the transplant regulatory load** — a more fundable, faster-iterating
  surface for a founder to learn on.
- Founder credibility: Sacha can speak the biology, which is exactly the moat the
  horizontal copilots (Benchling/Scispot) lack in this vertical.
- The ex-vivo perfusion story remains the **emotional/intellectual anchor** of the
  pitch and demo — it makes the macro/micro gap unforgettable.

---

## What the demo proves

- A real agent–human loop: observations → ranked mechanisms → evidence with caveats →
  next discriminating measurements → uncertainty bottleneck → human-review question.
- That the loop is **honest about uncertainty** and **source-aware** (curated evidence
  + live Tavily; Gemini synthesis; Pioneer-style structured extraction with safety flags).
- **Generality**: the same loop runs across preservation, organoid QC, and OoC presets.
- Partner-tech orchestration is **visible**, with honest live-vs-fallback status.

## What the demo does NOT prove

- Any **viability, accept/discard, diagnostic, or prognostic** capability (out of scope
  by design).
- **Macro→micro prediction** — there is no paired validation dataset; mechanisms are
  *possible*, not inferred truth (GSE293480 and PRJEB31843 are underpowered/indirect).
- **Willingness to pay or buyer validation** — that requires the segment interviews in
  `outreach-list.md`.
- **Real-world time/cost savings** — the reproducibility figures motivate the problem;
  they are not a measured product outcome.

---

## Recommended product wedge (opinionated)

> Build the **agent–human troubleshooting workspace for ambiguous living-tissue
> experiments**, and validate it first with **organoid / organ-on-chip / tissue-
> engineering QC teams** at the "why did this batch behave ambiguously and what do I
> measure next?" moment. Demo it with the **tissue-preservation failure** case for
> thesis resonance, position the company as the **interpretation layer** the device,
> imaging, and ELN vendors don't own, and hold the line on the no-clinical-claims
> boundary as a *feature*, not a limitation.

Feature gating is unchanged and reaffirmed in `feature-gates.md`:
**Green** = observation structuring, uncertainty bottleneck, evidence cards,
next-measurement suggestions, human-review question, partner trace.
**Yellow** = mechanism ranking, live enrichment, cost/time-saved estimates.
**Red** = viability score, transplant/discard, diagnosis/treatment, macro→micro
prediction without paired validation.
