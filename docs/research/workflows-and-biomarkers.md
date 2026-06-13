# Workflows and Biomarkers

Status: validated v1 — sufficient for hackathon feature gating.

Sources: Watson & Jochmans 2018 (PMC5843692), ex-vivo perfusion imaging review 2024 (PMC11408214), Eden & Dutkowski 2023 (PMC10663298), GSE293480 (frontiersin 2025 kidney NMP), PRJEB31843 (Madissoon et al. Tissue Stability Cell Atlas).

---

## Workflow domain comparison

### 1. Organ preservation / perfusion

| Field | Detail |
|---|---|
| User / team | Transplant researcher, perfusion scientist, surgical team |
| Workflow moment | During ex-vivo normothermic (NMP) or hypothermic (HMP) machine perfusion, before transplant decision |
| Common readouts | Lactate, lactate clearance, pH, O₂ consumption, bile pH/glucose/bicarbonate (liver), urine output/creatinine (kidney), perfusion flow, vascular/intrarenal resistance, transaminases (AST/ALT), LDH, NGAL, KIM-1, FMN (mitochondrial marker in HOPE) |
| Decision / output | Extend perfusion, accept organ, escalate to expert assessment — not transplant/discard by algorithm |
| Uncertainty bottleneck | No validated consensus on assessment thresholds; markers like lactate clearance are widely used but inconclusive (Watson & Jochmans 2018); existing markers can mask organ-quality failure |
| Why BSN can help | Routes macro signals to plausible molecular mechanisms (IRI, mitochondrial stress, endothelial injury), surfaces which markers are strong vs contested, suggests next discriminating assay, and escalates the residual judgment to a human expert |

**Key literature support:**
- Watson & Jochmans 2018: lactate clearance is the most common hepatic indicator but validated thresholds are lacking; product should not set binary thresholds.
- Eden & Dutkowski 2023: organ assessment + repair strategy matters more than extended storage time alone; mitochondria are central to ischemia-reperfusion injury.
- GSE293480 (2025 kidney NMP): pro-inflammatory innate immune signatures (TNFα/NF-κB, macrophage activation, tubuloepithelial depletion) in IRI/DGF; not powered for predictive biomarker development.

---

### 2. Tissue engineering QC

| Field | Detail |
|---|---|
| User / team | Tissue engineer, bioreactor operator, quality manager |
| Workflow moment | Post-culture quality gate before batch use or downstream processing; failure investigation after anomalous batch |
| Common readouts | Metabolic markers (lactate, glucose), cell viability stain, morphology imaging, differentiation markers (transcription factors, surface antigens), secretion profiles, O₂ consumption, pH |
| Decision / output | Pass batch / repeat batch / modify protocol / escalate to lead scientist |
| Uncertainty bottleneck | Borderline viability stain combined with rising lactate can reflect culture stress, hypoxic core, or contamination — bulk signals cannot discriminate without targeted assays |
| Why BSN can help | Generates ranked failure hypotheses (hypoxic core vs contamination vs protocol drift), maps each to a discriminating assay, and surfaces the earliest measurement that would differentiate the most likely causes |

---

### 3. Organoids / organ-on-chip

| Field | Detail |
|---|---|
| User / team | R&D scientist, platform engineer, drug discovery team |
| Workflow moment | Routine monitoring or after unexpected drug response or model anomaly |
| Common readouts | Barrier integrity (TEER), lactate/pH in media, oxygen consumption, fluorescent reporter signals, morphology imaging, inflammatory markers in effluent |
| Decision / output | Troubleshoot model instability vs genuine drug signal; decide whether to repeat with modified protocol or proceed with compound |
| Uncertainty bottleneck | Barrier leak + inflammatory marker increase could be drug toxicity, model failure, or protocol artifact; compound exposure confounds baseline |
| Why BSN can help | Separates model-failure hypotheses from drug-response hypotheses, recommends orthogonal measurements (e.g. cell viability stain + cytokine panel vs structural assay), escalates ambiguous signals to a domain expert |

---

### 4. Ex-vivo drug testing

| Field | Detail |
|---|---|
| User / team | Pharmacology researcher, safety assessment team, CRO scientist |
| Workflow moment | After compound exposure to ex-vivo tissue/perfused organ slice; reading out toxicity vs off-target effect |
| Common readouts | LDH release, ATP/ADP ratio, caspase activation, cytokine panel, metabolic shift (lactate/pH), membrane integrity, mitochondrial membrane potential |
| Decision / output | Flag compound for further safety tox work, or confirm safety in this assay format |
| Uncertainty bottleneck | Multi-target compound effects are hard to attribute; ex-vivo model may not recapitulate in-vivo distribution |
| Why BSN can help | Routes readout patterns to mechanism hypotheses (mitochondrial toxicant vs inflammatory vs reactive metabolite), suggests panel of mechanistic follow-up assays, and attaches literature caveats on assay limitations |

---

### 5. Biomarker / assay planning

| Field | Detail |
|---|---|
| User / team | Translational biologist, biomarker scientist, lab lead |
| Workflow moment | Pre-study design: choosing which markers to include in a new assay panel or study protocol |
| Common readouts | Literature markers, validated thresholds, regulatory guidance documents, prior study outcomes |
| Decision / output | Prioritized assay panel with rationale; flag contested vs established markers |
| Uncertainty bottleneck | Which markers are validated in the organism/context of interest vs only described in other settings; contested markers risk misleading study design |
| Why BSN can help | Queries evidence with source/caveat, surfaces marker validation status, warns about overclaiming, and surfaces the irreducible judgment call for a domain expert |

---

## Cross-domain uncertainty pattern

All five domains share the same core uncertainty structure:

```
macro/aggregate signal
    → multiple possible mechanisms
    → need targeted discriminating assay
    → senior judgment on ambiguous readout
```

This is the structural problem BioSignal Navigator addresses. The product does not resolve the ambiguity — it narrows it and names the measurement that would resolve it fastest.

---

## Key biomarker validity notes

| Marker | Domain | Validation status | Notes |
|---|---|---|---|
| Lactate / lactate clearance | Liver NMP, organ preservation | Widely used, no validated threshold | Do not set binary thresholds (Watson & Jochmans 2018) |
| pH | Cross-organ | Contextually useful | Must be interpreted with trend data |
| O₂ consumption | Cross-organ | Useful metabolic proxy | Needs normalization to mass/flow |
| Bile pH/glucose | Liver NMP | Organ-specific; clinically used | Not applicable to kidney or other organs |
| NGAL, KIM-1 | Kidney | Injury markers with published studies | Context-dependent; not viability thresholds |
| FMN | Kidney HMP/HOPE | Emerging mitochondrial marker | Promising but not consensus-validated |
| TNFα/NF-κB signaling | Molecular (IRI) | Pathway-level (GSE293480) | Transcriptomics level; not measurable at bedside without assay |
| Viability stain | Tissue engineering, organoids | Lab standard | Bulk signal; misses cell-type-specific failure |
| Barrier integrity (TEER) | Organ-on-chip | Platform-specific | Model-dependent; not transferable across chip designs |
