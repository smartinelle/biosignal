# Research Validation Loop Before Feature Build

> **For Hermes / Claude Code agents:** Do not build new product features until this loop produces a small evidence matrix and feature shortlist. The product idea may change; this document validates the problem, workflows, biomarkers, datasets, and demo claims before implementation.

## Goal

Validate what would make a credible hackathon product for Sacha's thesis direction: autonomous life-support / ex-vivo organ monitoring, organ preservation, perfusion, tissue engineering, and hidden tissue-state assessment.

The loop should answer:
1. What workflows actually exist in organ preservation / perfusion / tissue engineering quality assessment?
2. Which macro variables and biomarkers are accepted, contested, or emerging?
3. Which public datasets can ground the demo?
4. Which product features are credible in 1 day without overclaiming?
5. What should the demo explicitly *not* claim?

## Research thesis

The likely credible product is not "AI predicts viability." The credible product is:

> An evidence-routing and measurement-planning system that maps messy biomedical observations to plausible mechanisms, relevant evidence, candidate assays/biomarkers, uncertainty, and a human review question.

This should be validated against literature, public datasets, and real workflow constraints before building features.

## Evidence from quick initial scan

### 1. Viability assessment is real but not solved

Watson & Jochmans, *From Gut Feeling to Objectivity* (2018), argue that machine perfusion could move liver viability assessment away from subjective judgement, but validated criteria are still lacking and large multicenter datasets are needed.

Important implications:
- Product should emphasize uncertainty and evidence synthesis.
- Avoid claiming validated decision thresholds.
- A feature that explains which variables are promising vs unvalidated is credible.

Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC5843692/

### 2. Existing markers are useful but inconclusive

A 2024 systematic review of ex-vivo human-sized organ machine perfusion reports that conventional condition assessment often uses lactate, blood gas analysis, oxygen consumption, pressure/flow/resistance, and organ-specific outputs such as bile or urine production. It also states there is no consensus on standardized methods and existing markers can be inconclusive.

Important implications:
- Product should not output binary decisions.
- Product should support multi-modal evidence and caveat the limits of each marker.
- Imaging and metabolic readouts could be "next measurements".

Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC11408214/

### 3. Organ quality assessment may matter more than preservation duration alone

Eden & Dutkowski (2023) argue that prolonging storage alone will not necessarily improve organ utilization without reliable organ assessment and repair strategies. They highlight difficulty interpreting liver/kidney function during ex-situ preservation and point to mitochondria as central in ischemia-reperfusion injury.

Important implications:
- Product narrative should be about assessment/repair workflow, not just preservation time.
- Mechanism layer should include mitochondrial dysfunction and ischemia-reperfusion injury.

Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC10663298/

### 4. Molecular datasets exist but are small/specific

A 2025 human kidney NMP transcriptomics study reports GEO accession **GSE293480**. It links NMP biopsy transcriptomics to ischemia-reperfusion injury and delayed graft function, finding pro-inflammatory innate immune signatures including TNFα/NF-κB signaling, inflammatory response, allograft rejection-like pathways, macrophage/mononuclear phagocyte activation, and depleted tubuloepithelial signatures. The authors state the study was not powered to develop predictive biomarkers.

Important implications:
- Excellent anchor for molecular mechanism demo.
- Use as evidence for mechanism exploration, not prediction.
- Build feature: "retrieve molecular evidence + indicate power/limitations."

Source: https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2025.1679251/full
Dataset: GSE293480

### 5. Clinical registry datasets exist but are not perfect for real-time perfusion variables

SRTR/OPTN datasets cover transplant activity, donors, recipients, outcomes, survival, DGF, etc. They can validate outcomes and clinical risk factors, but likely lack granular ex-vivo perfusion time-series variables and omics.

Important implications:
- Public clinical datasets can ground outcome definitions and risk context.
- They probably cannot validate a macro-to-micro perfusion model alone.
- Use them for product framing, demo labels, and outcome definitions, not real-time viability inference.

Sources:
- SRTR: https://srtr.transplant.hrsa.gov/
- OPTN/SRTR annual data reports: delayed graft function defined as dialysis within first 7 days post-transplant in kidney reports.

## Candidate datasets to investigate

### Tier 1 — Best thesis fit

1. **GSE293480 — Human kidney NMP transcriptomics**
   - Domain: normothermic machine perfusion, kidney, ischemia-reperfusion injury, delayed graft function.
   - Data type: RNA-seq / transcriptomics.
   - Use: mechanism evidence card; compare IGF/DGF or ATI severity if metadata allows.
   - Risk: small sample; not powered for prediction.

2. **PRJEB31843 — Tissue Stability Cell Atlas**
   - Domain: human tissue cold preservation, lung/spleen/esophagus.
   - Data type: scRNA-seq.
   - Use: preservation-time molecular stability/degradation demo.
   - Risk: tissue slices / sample preservation rather than whole-organ transplant viability.

3. **Machine perfusion clinical trial papers / tables**
   - Domain: liver/kidney NMP/HMP.
   - Data type: paper-extracted variables and thresholds.
   - Use: marker dictionary and workflow validation.
   - Risk: not always machine-readable public patient-level data.

### Tier 2 — Clinical outcome grounding

4. **SRTR / OPTN public data and annual reports**
   - Domain: transplant outcomes, DGF, graft survival, donor/recipient factors.
   - Use: outcome definitions, incidence, risk factors, clinical context.
   - Risk: may require data request for granular analysis; lacks omics/perfusion time-series.

5. **Published kidney/liver transplant transcriptomics GEO datasets**
   - Examples from search: GSE21374, GSE48581, GSE36059, GSE50058, GSE72925, GSE25902 for kidney graft survival studies.
   - Use: demonstrate clinical+molecular integration concept.
   - Risk: post-transplant biopsy/graft survival rather than ex-vivo preservation workflow.

### Tier 3 — Broader translational medicine/product generalization

6. **Sepsis/inflammation public transcriptomics datasets**
   - Use only if pivoting broader.
   - Risk: generic medical AI feel; weaker thesis fit.

7. **Organoid / tissue engineering QC datasets**
   - Use if pivoting to tissue engineering quality control.
   - Risk: search/metadata time could exceed hackathon budget.

## Biomarker / feature dictionary to validate

### Macro / operational variables

- Preservation duration
- Cold ischemia time / warm ischemia time
- Perfusion temperature
- Perfusion pressure
- Flow
- Vascular/intrarenal resistance
- pH
- Oxygenation / oxygen consumption
- Lactate and lactate clearance
- Glucose metabolism
- Bicarbonate support / pH regulation

### Organ-specific functional outputs

Liver:
- Bile production
- Bile pH
- Bile glucose
- Bile bicarbonate
- Transaminases: AST/ALT
- LDH
- Urea production / ammonia clearance
- Coagulation factor production / factor V / INR where applicable

Kidney:
- Urine output
- Creatinine clearance / creatinine trends
- Renal blood flow
- Intrarenal resistance
- NGAL
- KIM-1
- L-FABP
- GSTs
- LDH
- FMN as mitochondrial injury / graft quality marker in HMP/HOPE literature

Cross-organ / molecular mechanisms:
- Ischemia-reperfusion injury
- Mitochondrial dysfunction
- TNFα/NF-κB signaling
- Innate immune activation
- Macrophage / mononuclear phagocyte activation
- Inflammasome / pattern recognition receptor pathways
- Endothelial injury
- Apoptosis / necrosis
- Cell-type depletion or composition shift
- Tubuloepithelial transport loss in kidney

Imaging / spatial readouts:
- Ultrasound / contrast-enhanced ultrasound
- MRI / functional MRI
- CT
- Laser speckle imaging
- Near-infrared spectroscopy
- 31P MRI / metabolic imaging

## Verification loop design

Run this loop before building each feature.

### Step 1 — Define workflow hypothesis

For each proposed feature, write:
- Target user: transplant researcher, perfusion scientist, tissue engineer, clinician-researcher, biotech R&D.
- Moment in workflow: before perfusion, during perfusion, after sampling, after assay, literature review.
- Input artifacts: case note, perfusion time series, biopsy result, paper, dataset metadata, assay panel.
- Decision or output: mechanism hypothesis, next measurement, evidence summary, uncertainty escalation.

Reject features that cannot name a real workflow moment.

### Step 2 — Evidence matrix

Create `docs/research/evidence-matrix.md` with rows:
- Claim
- Source / dataset
- Strength: strong / medium / weak
- User-facing implication
- Product feature supported
- Caveat / do-not-claim

Example:
- Claim: lactate clearance is widely used in liver NMP but incomplete.
- Source: Watson & Jochmans 2018.
- Strength: medium/high review evidence.
- Feature: evidence card should distinguish hepatocellular vs biliary compartments.
- Caveat: do not say lactate alone determines viability.

### Step 3 — Dataset feasibility card

For each candidate dataset, create a short card:
- accession / URL
- organism / organ / sample type
- data type
- sample count
- metadata available
- outcomes available
- what demo question it can answer
- what it cannot answer
- download/processing complexity
- go/no-go for hackathon

### Step 4 — Feature gating

Only build a feature if it has at least one of:
- a source supporting a real workflow/biomarker need;
- a public dataset that can demonstrate it;
- a demo value that is explicitly framed as speculative and human-reviewed.

Feature categories:
- **Green:** build now. Strong evidence + demoable.
- **Yellow:** build as mock/explainer with caveat.
- **Red:** do not build; too speculative or too regulated.

### Step 5 — Expert/customer proxy validation

If possible during the hackathon, ask 1–3 people:
- transplant/perfusion researcher
- tissue engineering person
- clinician-scientist / biotech friend

Three questions:
1. In your workflow, where do macro signals become ambiguous?
2. Which biomarkers/assays do you actually trust or distrust?
3. Would an evidence-routing + next-measurement tool be useful, or is the bottleneck elsewhere?

Record answers in `docs/research/expert-notes.md`.

### Step 6 — Build only the validated slice

After the above, choose a single demo wedge:
- **Kidney NMP IRI/DGF evidence router** if GSE293480 is usable.
- **Tissue preservation molecular stability navigator** if PRJEB31843 is easier to demo.
- **Liver NMP viability criteria explainer** if paper/table extraction is more demoable than omics.
- **General BioSignal Navigator** only if time remains and workflow breadth helps the pitch.

## Recommended research agent workstreams

### Research Agent A — Clinical workflow and biomarkers

Goal: identify real workflows and marker sets for liver/kidney machine perfusion.

Deliverable: `docs/research/workflows-and-biomarkers.md`

Questions:
- What variables are routinely monitored during liver/kidney NMP/HMP?
- Which are widely used vs disputed?
- Which are organ-specific vs cross-organ?
- What are the known limits of lactate, bile, urine, pH, resistance, oxygen consumption?

### Research Agent B — Dataset feasibility

Goal: find and rank public datasets.

Deliverable: `docs/research/dataset-feasibility.md`

Questions:
- Can GSE293480 be downloaded/parsed quickly?
- What metadata and outcomes does it include?
- Is PRJEB31843 accessible in a hackathon timeframe?
- Which SRTR/OPTN public data are readily usable without a lengthy data request?
- Are there machine-perfusion datasets with paired time-series + outcomes?

### Research Agent C — Product/workflow validation

Goal: convert evidence into feature gates.

Deliverables:
- `docs/research/evidence-matrix.md`
- `docs/research/feature-gates.md`

Questions:
- Which app features are supported by evidence?
- Which claims are unsafe?
- Which features will impress judges while staying honest?

### Research Agent D — Competitive / industry context

Goal: understand existing products and industry workflows.

Deliverable: `docs/research/industry-landscape.md`

Companies/areas:
- OrganOx
- XVIVO
- TransMedics
- Bridge to Life
- Organ Recovery Systems / LifePort
- Paragonix
- Northernmost
- Waters Medical Systems
- ex-vivo perfusion research platforms

Questions:
- What do devices currently measure/display?
- What claims do companies make publicly?
- Is there a gap around evidence interpretation / decision support / research workflow?

## Build implications after validation

Likely credible features:
1. **Observation structuring** — safe, general, useful.
2. **Mechanism hypotheses with caveats** — safe if evidence-linked.
3. **Biomarker dictionary** — high value, low risk.
4. **Evidence cards with source/caveat** — high value, judge-friendly.
5. **Next measurement recommender** — credible if framed as research suggestion.
6. **Human review question** — strongest Atira fit.
7. **Dataset browser / demo slice** — makes it less hand-wavy.

Likely risky features:
1. Viability score.
2. Transplant/discard recommendation.
3. Patient-specific clinical advice.
4. Macro-to-micro prediction without data.
5. Claims of validated thresholds across organs.

## First 2-hour validation sprint

1. 20 min — create `docs/research/` skeleton.
2. 35 min — Research Agent A: marker/workflow scan from review papers.
3. 35 min — Research Agent B: dataset feasibility scan for GSE293480, PRJEB31843, SRTR/OPTN.
4. 25 min — Research Agent C: evidence matrix + feature gate v0.
5. 5 min — decide the build wedge.

## Go/no-go decision rule

At the end of the sprint, choose the wedge with the highest score:

- Dataset accessibility: 0–3
- Thesis fit: 0–3
- Hackathon demo clarity: 0–3
- Regulatory safety: 0–3
- Partner-tech fit: 0–3
- Originality: 0–3

Build the highest-scoring wedge only.

## Current provisional recommendation

Do the verification loop, but bias toward:

> **Kidney NMP IRI/DGF Evidence Router**

Why:
- has a directly relevant public GEO accession: GSE293480;
- links ex-vivo NMP, transcriptomics, IRI, and delayed graft function;
- naturally supports the macro/micro bridge;
- stays honest if framed as mechanism/evidence routing, not prediction;
- gives a precise demo case rather than generic BioSignal Navigator.

Fallback if dataset processing is too slow:

> **Liver NMP Viability Criteria Navigator**

Why:
- literature has clearer marker discussions: lactate, pH, bile chemistry, transaminases, glucose, hemodynamics;
- easier to build as evidence cards without raw data.
