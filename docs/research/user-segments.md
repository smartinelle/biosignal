# User Segments

Status: v1 — segment comparison for the product-definition sprint (June 2026).

Goal: decide **who to build for and contact first**. Each segment is scored 1–5
(5 = best for BSN) on the dimensions the wedge decision actually turns on.
Scores are judgment calls grounded in the landscape scan and the research docs,
not survey data — they are hypotheses to validate, not facts.

---

## Scorecard summary

| Segment | Pain intensity | Budget/urgency | Data availability | Low regulatory risk | Reachability | BSN fit | **Total** |
|---|---|---|---|---|---|---|---|
| Perfusion / organ-preservation researchers | 4 | 4 | 2 | 1 | 2 | 3 | **16** |
| Tissue-engineering teams | 4 | 3 | 3 | 4 | 3 | 4 | **21** |
| Organoid / organ-on-chip teams | 5 | 4 | 4 | 4 | 4 | 5 | **26** |
| Translational biology / biomarker teams | 3 | 3 | 4 | 3 | 3 | 4 | **20** |
| Biotech R&D assay-troubleshooting teams | 4 | 4 | 4 | 4 | 4 | 4 | **24** |

**Read:** organoid / organ-on-chip teams and biotech R&D assay-troubleshooting
teams are the most attractive first wedges. Perfusion scores lowest on
**regulatory risk** and **reachability** despite the strongest thesis resonance.

---

## 1. Perfusion / organ-preservation researchers

- **User role:** transplant/perfusion scientists, surgical research teams, ex-vivo
  perfusion labs.
- **Current workflow:** run NMP/HMP on a device (OrganOx, TransMedics, XVIVO,
  Bridge to Life, LifePort); watch lactate, flow, resistance, bile/urine; decide
  extend/accept/escalate.
- **Pain:** no validated consensus thresholds; markers are inconclusive; assessment
  is subjective (Watson & Jochmans 2018; 2024 systematic review).
- **Budget/urgency proxy:** high per-organ stakes, but spend is locked into device
  vendors and hospital procurement; slow cycles.
- **Data availability:** rich time-series exists but is **device-locked and
  patient-adjacent**; public omics is small/underpowered (GSE293480).
- **Regulatory risk:** **highest.** Anything near accept/discard or viability is
  regulated; vendors already market "real-time viability assessment."
- **Reachability:** hard — clinical/academic gatekeeping, long trust cycles.
- **BSN fit:** strong thesis resonance, but the safe product here is narrow
  (evidence/uncertainty explainer) and collides with device viability framing.
- **Verdict:** **thesis-resonant demo, weak first commercial wedge.** Keep as the
  demo's emotional anchor, not the go-to-market.

---

## 2. Tissue-engineering teams

- **User role:** tissue engineers, bioreactor operators, QC managers in regenerative-
  medicine / engineered-tissue startups.
- **Current workflow:** culture → post-culture QC gate → pass/repeat/modify; failure
  investigation after an anomalous batch.
- **Pain:** batch variability, no standardized QC criteria, borderline viability +
  metabolic drift that bulk signals can't disambiguate.
- **Budget/urgency proxy:** medium-high; failed batches are expensive and gate
  downstream work.
- **Data availability:** in-house metabolic + imaging + sometimes omics; heterogeneous
  but accessible to a design partner.
- **Regulatory risk:** **low-medium** while pre-clinical / research-use.
- **Reachability:** medium — startup teams are reachable but smaller in number.
- **BSN fit:** strong — the troubleshooting loop maps directly onto QC failure
  investigation.

---

## 3. Organoid / organ-on-chip teams  ⭐ top wedge

- **User role:** R&D scientists and platform engineers at organoid/OoC companies,
  drug-discovery groups, and CROs running these models.
- **Current workflow:** routine monitoring + anomaly investigation after unexpected
  drug response or model instability; image-based QC (Incucyte/Harmony) + media
  metabolics + effluent markers.
- **Pain:** **highest and best-documented.** Batch-to-batch and organoid-to-organoid
  variability, no standardized QC, "3R" challenge (reproducibility, regulatory,
  real-time monitoring); barrier-leak + inflammatory signal is genuinely ambiguous
  (toxicity vs model failure vs artifact).
  [Organoid QC framework (Nature Sci Reports 2025)](https://www.nature.com/articles/s41598-025-14425-x),
  [Organoids review 2025](https://link.springer.com/article/10.1007/s00018-025-05692-y),
  [organoid-to-organoid variability](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9348635/)
- **Budget/urgency proxy:** high — a fast-growing OoC market with pharma/CRO buyers
  who already pay for platforms and imaging software.
- **Data availability:** good — imaging, media metabolics, sometimes transcriptomics,
  mostly in-house and shareable with a design partner.
- **Regulatory risk:** **low** in research/drug-discovery use (not patient care).
- **Reachability:** good — concentrated set of companies/labs, active publishing
  community, conference presence.
- **BSN fit:** **best.** Incumbents do imaging/feature extraction, not mechanism
  disambiguation + next-measurement. Directly inside the thesis (hidden biological
  state interpretation) without the transplant regulatory load.

---

## 4. Translational biology / biomarker teams

- **User role:** translational biologists, biomarker scientists, lab leads designing
  assay panels / study protocols.
- **Current workflow:** pre-study marker selection; literature + prior outcomes →
  prioritized panel.
- **Pain:** which markers are validated *in this context* vs only described elsewhere;
  contested markers mislead study design.
- **Budget/urgency proxy:** medium; study-design decisions are high-leverage but
  infrequent.
- **Data availability:** good (literature-centric), which suits the evidence-card +
  Tavily/Gemini layer well.
- **Regulatory risk:** medium (depends how close to clinical claims).
- **Reachability:** medium.
- **BSN fit:** strong for the **evidence/assay-planning** half of the product; weaker
  on the live-readout troubleshooting half. Good **secondary** segment / second feature.

---

## 5. Biotech R&D assay-troubleshooting teams (horizontal)

- **User role:** R&D scientists across modalities hitting ambiguous assay readouts;
  CRO scientists; process/assay-development teams.
- **Current workflow:** ad-hoc — senior scientist manually connects readouts,
  mechanisms, literature, protocols before choosing the next experiment.
- **Pain:** broad and real; the $28B/yr irreproducibility tax lands here (Freedman
  et al. 2015). Each failed replication = 3–24 months and \$0.5–2M.
- **Budget/urgency proxy:** high in aggregate; diffuse per-team.
- **Data availability:** good but heterogeneous.
- **Regulatory risk:** low (research use).
- **Reachability:** good but unfocused — "everyone" is hard to sell to.
- **BSN fit:** strong as the **platform vision**, but too broad to be the *first*
  wedge. Use organoid/OoC QC as the sharp entry, then generalize here.

---

## Implication for the wedge

Lead commercial validation with **organoid / organ-on-chip + tissue-engineering QC
troubleshooting** (segments 3 and 2), keep **perfusion/preservation** as the
thesis-resonant *demo* (segment 1, not the GTM), and treat **biomarker/assay
planning** (segment 4) as the natural second feature on the path to the broad
**R&D troubleshooting platform** (segment 5). See `decision-memo.md`.
