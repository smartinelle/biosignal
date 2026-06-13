# Industry Landscape

Status: v1 — competitive scan for the product-definition sprint (June 2026).

Purpose: locate the layer BioSignal Navigator (BSN) should occupy. The thesis of
this scan is that the market is well served at the **sensor/display layer** and
the **data-plumbing layer**, but the **interpretation / troubleshooting layer**
— messy multimodal readouts → ranked mechanisms → literature-grounded evidence →
next discriminating measurement → human review — is largely unowned for
living-tissue R&D.

---

## Layer map (where value is captured today)

| Layer | Who owns it | What they do | Do they interpret / recommend next experiment? |
|---|---|---|---|
| Sensor / perfusion hardware | OrganOx, TransMedics, XVIVO, Bridge to Life, Organ Recovery Systems, Paragonix | Measure & control perfusion variables; some embed simple viability criteria | No — they display numbers; viability rules are fixed thresholds, not literature-aware reasoning |
| Image-based QC | Sartorius Incucyte, PerkinElmer Harmony, OrganoID, CellProfiler, Organoid Profiler | Quantify organoid morphology, size, count, live/dead | No — per-image metrics, not mechanism/evidence reasoning |
| Organ-on-chip platforms | Emulate, MIMETAS, TissUse, InSphero, CN Bio | Run tissue models + data management + imaging | No — platform + data, not troubleshooting of ambiguous readouts |
| Lab data / ELN / copilots | Benchling (+ Benchling AI), Scispot (Scibot), TetraScience, Sapio | Structure R&D data; generic NL Q&A, anomaly/trend flags | Partially — generic copilots over *your own* data; not biology-mechanism-specialized or literature-grounded |
| **Interpretation / troubleshooting** | **largely unowned** | messy readouts → mechanisms → evidence → next measurement → human review | **This is the BSN wedge** |

---

## Organ preservation / perfusion devices

These define the regulated transplant space. They are **adjacent, not competitors** —
BSN is a research-workflow tool and must not enter their viability-claim territory.
But they show what "measurement" looks like today and where interpretation is missing.

### OrganOx (metra) — liver NMP
- Continuously perfuses the liver with oxygenated blood at physiological temperature;
  **onboard blood-gas analysis** auto-controls perfusate gases. Tracks **lactate
  clearance, bile production, flow/pressure**. Lactate clearance + bile + stable
  flow is the de-facto viability heuristic. [OrganOx](https://www.organox.com/metra-how-it-works/index),
  [Jeddou 2025 NMP viability review](https://onlinelibrary.wiley.com/doi/10.1111/liv.16244)
- Gap: viability criteria are fixed heuristics with **no validated consensus
  thresholds**; the device does not reason across literature or recommend the next
  discriminating assay.

### TransMedics (OCS — heart/lung/liver)
- Monitors **aortic pressure, coronary flow, SvO₂, hematocrit, blood temperature,
  and arterial/venous lactate dynamics**; lactate trend is the headline metabolic
  readout. [OCS Heart User Guide (FDA)](https://www.accessdata.fda.gov/cdrh_docs/pdf18/P180051S001D.pdf),
  [OCS DCD heart review](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9229932/)
- Gap: again a display + threshold device; no mechanism hypothesis layer.

### XVIVO — multi-organ (lung/heart/liver/kidney)
- Temperature-controlled perfusion (12–37 °C), pressure-controlled pulsatile flow,
  hollow-fiber oxygenator; markets **DGF reduction** vs static cold storage for
  kidney. [XVIVO organ perfusion](https://www.xvivogroup.com/organ-perfusion/)

### Bridge to Life (VitaSmart — HOPE) — liver/kidney
- Hypothermic **oxygenated** perfusion; markets **FMN / mitochondrial function as a
  real-time viability biomarker**; first U.S. FDA De Novo clearance for HOPE of donor
  livers. [Bridge to Life ILTS 2026 / FMN](https://www.prnewswire.com/news-releases/bridge-to-life-presents-new-ilts-2026-data-showing-vitasmart-hypothermic-oxygenated-perfusion-hope-expands-use-of-marginal-donor-livers-and-preserves-mitochondrial-function-for-real-time-viability-assessment-302767518.html)
- **Important boundary signal:** vendors are now explicitly marketing "real-time
  viability assessment." BSN must **not** compete on viability claims — that is the
  regulated red line. BSN's defensible angle is the opposite: uncertainty-first,
  research-only, "we tell you what you *cannot* yet conclude and what to measure next."

### Organ Recovery Systems (LifePort Kidney Transporter) — kidney HMP
- Records **pressure, temperature, flow rate, and renal vascular resistance every
  ~10 s**; adjusts pressure wave to protect microvasculature. [LifePort](https://www.organ-recovery.com/lifeport-kidney-transporter/)

### Paragonix (SherpaPak / *guard family) — heart/lung/liver/kidney/pancreas
- Non-perfusing cold storage with a **Bluetooth temperature data logger**; real-time
  preservation-temperature reporting, downloaded post-transport. [Paragonix SherpaPak](https://www.paragonixtechnologies.com/sherpapak)

### Signal of the gap: academia is building the missing analytics layer
- **EXAM** — an ex-vivo allograft monitoring *dashboard* for analyzing hypothermic
  machine-perfusion data in deceased-donor kidney transplantation — was built in
  academia, not by a device vendor. [EXAM dashboard](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11654979/)
- Read: even in the most instrumented corner of the field, the **interpretation
  layer is a research afterthought**, not a product.

---

## Organoid / tissue-engineering QC tooling

### Image-based QC (incumbents)
- **Sartorius Incucyte Organoid Analysis** — automated label-free morphology, size,
  count, growth/death over time. [Sartorius Incucyte](https://www.sartorius.com/en/products/live-cell-imaging-analysis/live-cell-analysis-software/incucyte-organoid-analysis-software)
- **OrganoID, CellProfiler, Organoid Profiler, PerkinElmer Harmony** — segmentation,
  morphology, live/dead, drug-effect quantification. [Organoid QC framework (Nature Sci Reports 2025)](https://www.nature.com/articles/s41598-025-14425-x)
- Gap: these answer *"what does this image look like?"* not *"why did this batch
  fail and what should I measure next?"* They produce features; they do not route
  features → mechanisms → evidence → next assay.

### Organ-on-chip platforms
- **Emulate** (Human Emulation System), **MIMETAS** (OrganoPlate, high-throughput,
  imaging-optimized), **TissUse** (HUMIMIC multi-organ), **InSphero**, **CN Bio**.
  [Top OoC companies](https://www.marketsandmarkets.com/ResearchInsight/organs-on-chips-market.asp),
  [MIMETAS technology](https://www.mimetas.com/technology)
- Gap: platform + data management + imaging. When a chip gives an ambiguous result
  (barrier leak + inflammatory marker after a compound — toxicity vs model failure
  vs artifact), the **mechanism-disambiguation and next-measurement decision is left
  entirely to the scientist**.

---

## Lab data / ELN / AI copilots (closest in *shape*)

- **Benchling** — dominant ELN/LIMS in biotech/academia; **Benchling AI** connects
  agents to structured R&D data; its **2026 Biotech AI Report** states 89% of
  scientists use copilots/reasoning tools as a first stop. [Benchling AI](https://www.benchling.com/ai),
  [2026 Biotech AI Report](https://www.benchling.com/biotech-ai-report-2026)
- **Scispot (Scibot Omega)** — "lab copilot that knows your ELN, data, and freezer";
  anomaly detection, trend insight, predictive quality. [Scibot](https://www.scispot.com/blog/scibot-omega-intelligent-lab-copilot)
- **TetraScience** — harmonizes instrument data into a scientific-data cloud feeding
  ELNs/AI. [TetraScience + Benchling](https://www.tetrascience.com/videos/benchling)

**Why these are not the same product:**
- They are **horizontal copilots over your own structured data**. Their reasoning is
  general-purpose Q&A + anomaly/trend flags.
- BSN is **vertical and biology-specific**: it reasons about *mechanisms of living-
  tissue failure*, grounds them in *external literature/datasets with caveats*, and
  outputs a *next discriminating measurement* and a *human-review question* — an
  uncertainty-first troubleshooting loop, not a data chatbot.
- Realistic future: BSN is the *interpretation layer* that could sit **on top of**
  a Benchling/Scispot data substrate, not a replacement for it.

---

## The visible gap BSN can occupy

> Between the **numbers** (devices, imaging) and the **data plumbing** (ELN/copilots)
> sits the **interpretation/troubleshooting decision**: "these ambiguous readouts are
> consistent with several mechanisms; here is the evidence and its caveats; here is
> the single next measurement that best discriminates them; here is the judgment a
> human must still make."

No incumbent owns this for living-tissue R&D. Devices won't (regulated, hardware-
locked, viability-threshold framing). Image tools won't (feature extraction, not
reasoning). Horizontal copilots could drift into it, but lack the biology-specific,
literature-grounded, uncertainty-first framing — and they are not thesis-defensible
for a founder who can speak the biology.

**Caveat:** this is a workflow/decision-support gap, not a proven willingness-to-pay.
The reproducibility-cost evidence (see `product-research-sprint.md`) suggests the
pain is real and expensive, but pricing/buyer validation is the explicit next step.
