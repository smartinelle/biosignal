# Demo Workflows

Status: v1 — concrete product workflows to demo now.

BioSignal Navigator should be marketed as a **general biotech R&D troubleshooting workspace**. The workflows below are use cases that prove the core loop, not separate product categories.

Core loop:

```text
messy research observation
→ structured signals and context
→ possible mechanisms
→ evidence with caveats
→ next discriminating measurement
→ human review question
→ action plan
```

Hard boundary: these workflows do **not** output diagnosis, treatment, viability scores, transplant/discard recommendations, or biological ground truth. They output research hypotheses and next measurements.

---

## Recommended demo set

### 1. Failed / ambiguous assay result — broadest biotech workflow

**Why demo it:** This is the most general product story. Every biotech R&D team has assay results that are noisy, contradictory, or hard to interpret.

**Input note:**

> Cell-based potency assay repeated twice. Signal is 40% lower than expected, but cell count is normal. Positive control drifted slightly. Plate edge wells look worse. Reagent lot changed last week. Need to decide whether this is biology, protocol drift, reagent failure, or plate artifact before repeating the study.

**Signals:** low assay signal, normal cell count, positive-control drift, edge effect, reagent-lot change.

**Possible mechanisms:** plate artifact, reagent degradation/lot effect, protocol timing drift, real biological potency change.

**Next measurements:** repeat controls with old/new reagent lot, edge-vs-center plate analysis, orthogonal potency assay, timepoint check.

**Human review question:** Should the team invalidate the run as technical artifact, or run an orthogonal assay before repeating the full experiment?

**Why it helps positioning:** Shows BioSignal Navigator as a general biotech research tool, not a tissue-specific app.

---

### 2. Organoid / tissue-model QC anomaly — living-system use case

**Why demo it:** Concrete, visual, and close to the current presets. It is a use case, not the product category.

**Input note:**

> Organoid QC batch shows abnormal morphology, borderline viability stain, rising media lactate, and uncertain differentiation marker expression. Some wells show possible hypoxic cores. Need to decide which assay resolves whether this is batch stress, differentiation failure, imaging artifact, or media/protocol drift.

**Signals:** morphology shift, borderline viability stain, lactate rise, uncertain marker expression, possible hypoxic core.

**Possible mechanisms:** hypoxic/metabolic stress, differentiation failure, media/protocol drift, imaging/segmentation artifact.

**Next measurements:** hypoxia stain, marker panel repeat, media metabolite profile, imaging QC review, single-cell/spatial assay only if needed.

**Human review question:** Which mechanism would change the next batch protocol, and which minimal assay discriminates it fastest?

**Why it helps positioning:** Demonstrates hidden-state interpretation in living systems without making clinical claims.

---

### 3. Organ-on-chip drug-response ambiguity — translational R&D use case

**Why demo it:** Shows the product can handle causality ambiguity in experimental models, not only QC.

**Input note:**

> Organ-on-chip drug response experiment shows unexpected barrier leak, oxygen-consumption shift, inflammatory marker increase, and morphology change after compound exposure. Need to troubleshoot whether this is compound toxicity, model instability, dosing artifact, or protocol failure.

**Signals:** barrier leak, oxygen shift, inflammatory marker increase, morphology change, compound exposure.

**Possible mechanisms:** true compound toxicity, barrier model instability, dosing/exposure artifact, culture/protocol failure.

**Next measurements:** vehicle/control comparison, dose-response repeat, TEER/barrier orthogonal assay, inflammatory panel, medium/osmolality check.

**Human review question:** Is the signal strong enough to justify mechanistic follow-up, or should the model/run be rejected as unstable?

**Why it helps positioning:** Makes the product feel useful for pharma / translational biology workflows.

---

### 4. Ex-vivo tissue preservation ambiguity — visceral thesis anchor

**Why demo it:** Strongest emotional and thesis-resonant story. Use as the hackathon hero case, but avoid making the product sound transplant-specific.

**Input note:**

> Ex-vivo preserved tissue sample after 48h cold storage. Lactate rising, pH falling, vascular resistance increasing, oxygenation uncertain. Need to debug the experiment and decide which measurement should be run next, without making a clinical viability claim.

**Signals:** lactate rise, pH fall, resistance rise, uncertain oxygenation, preservation duration.

**Possible mechanisms:** metabolic stress, perfusion/oxygenation failure, endothelial/vascular injury, sampling artifact.

**Next measurements:** oxygen extraction / perfusate gas check, endothelial injury marker, histology/viability stain as research readout, lactate clearance trend under controlled perfusion.

**Human review question:** What evidence would distinguish reversible perfusion stress from deeper tissue injury in a research setting?

**Why it helps positioning:** Makes the macro→micro hidden-state problem intuitive, while preserving the research-only boundary.

---

## Best 2-minute demo order

1. Open with general category: “debugger for biotech research experiments.”
2. Show the broad assay troubleshooting workflow first or mention it explicitly.
3. Run the ex-vivo preservation hero case because it is visceral.
4. Flash organoid/OoC presets to prove generality.
5. End with the invariant workflow: evidence-backed mechanisms, next measurement, human review.

## Product implication

Do not market BioSignal Navigator as a tissue-engineering or perfusion platform. Market it as a general **biotech research troubleshooting workspace**, then prove it through concrete workflows where the same loop repeats.
