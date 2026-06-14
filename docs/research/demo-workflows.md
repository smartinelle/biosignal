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

Top 4 for the hackathon demo:

1. **Assay signal collapse after protocol/reagent-lot change** — broadest biotech category proof.
2. **qPCR / ddPCR amplification anomaly** — ubiquitous molecular-biology troubleshooting.
3. **Protein expression / purification yield drop** — process/protein R&D proof.
4. **Cell culture growth / media/incubator issue** — everyday wet-lab operations proof.

If the demo needs more bioprocess flavor, swap workflow 4 for **bioreactor / fermentation productivity deviation**.

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

### 5. qPCR / ddPCR amplification anomaly — molecular biology workflow

**Why demo it:** qPCR/ddPCR troubleshooting is ubiquitous across biotech R&D and makes the product feel general immediately.

**Input note:**

> qPCR assay shows Ct values 3 cycles later than expected. Melt curve has a shoulder, no-template controls show weak amplification, and the positive control failed intermittently. RNA integrity is borderline and this extraction batch was handled by a new operator. Need to decide whether the result is contamination, primer-dimer, degraded template, RT inhibition, or pipetting error.

**Signals:** late Ct shift, melt-curve shoulder, NTC amplification, intermittent positive-control failure, borderline RNA quality, new operator.

**Possible mechanisms:** contamination/carryover, primer-dimer, degraded template, RT inhibition, pipetting/setup error, poor primer specificity.

**Next measurements:** no-RT control, alternate primer set, dilution/inhibition test, re-extract sample, spike-in control, orthogonal assay confirmation.

**Human review question:** Do we trust the quantification enough to interpret biology, or must the assay design/run be fixed first?

**What not to claim:** Do not infer gene-expression truth from one compromised run.

---

### 6. Protein expression / purification yield drop — protein/process R&D workflow

**Why demo it:** Protein production failures are common, expensive, and clearly outside tissue engineering.

**Input note:**

> Recombinant protein run produced 60% lower yield than baseline. SDS-PAGE shows extra bands, SEC has a new shoulder peak, and DLS indicates more aggregation. Induction temperature changed and buffer pH was slightly lower than usual. Need to decide whether the bottleneck is expression, proteolysis, purification, or storage stability.

**Signals:** yield drop, extra bands, SEC shoulder, aggregation, induction change, pH change.

**Possible mechanisms:** expression burden, proteolysis, inclusion bodies, resin saturation, pH-driven aggregation, oxidation/storage instability.

**Next measurements:** soluble/insoluble split, small induction-temperature matrix, protease inhibitor check, buffer screen, fresh resin/control purification, mass spec confirmation.

**Human review question:** Is the main bottleneck expression, recovery, or stability?

**What not to claim:** Do not claim protein function or usability without functional/orthogonal assays.

---

### 7. Cell culture growth / media / incubator issue — everyday wet-lab workflow

**Why demo it:** This is a universal lab-operations failure mode and reinforces the general biotech category.

**Input note:**

> Cell culture grew slower after thaw. Morphology shifted, confluency stalled, media color changed earlier than usual, and passage-to-passage behavior is inconsistent. Media lot changed two weeks ago and incubator CO2 logs show a short excursion. Need to decide whether this is media, environment, handling, contamination, or biology drift.

**Signals:** slow growth, morphology shift, stalled confluency, media color/pH shift, media lot change, incubator excursion, passage variability.

**Possible mechanisms:** media lot shift, incubator drift, seeding error, passage-related drift, freeze/thaw stress, low-grade contamination.

**Next measurements:** fresh-media lot comparison, incubator log review/calibration, mycoplasma test, seeding-density titration, side-by-side historical baseline.

**Human review question:** Is this environment/handling, or has the biological model drifted enough to reset the line/batch?

**What not to claim:** Do not recommend discard or claim contamination without direct testing.

---

### 8. Bioreactor / fermentation productivity deviation — bioprocess workflow

**Why demo it:** Shows the same product loop applies to process development and manufacturing-adjacent R&D.

**Input note:**

> Bioreactor run underperformed on titer. DO drifted lower during mid-run, pH control required more base than usual, off-gas trends diverged from the historical batch, and foam spiked after feed change. Need to decide whether this is sensor drift, feed limitation, oxygen-transfer bottleneck, contamination, or strain instability.

**Signals:** low titer, DO drift, pH/base demand, off-gas divergence, foam spike, feed change.

**Possible mechanisms:** oxygen-transfer limitation, feed strategy issue, sensor calibration drift, contamination, strain instability, metabolic overflow.

**Next measurements:** sensor calibration check, off-gas comparison, feed titration, inoculum QC, contamination screen, agitation/aeration sensitivity run.

**Human review question:** Is the failure process-control, instrumentation, or biological strain state?

**What not to claim:** Do not claim batch disposition, release-readiness, or scale-up success.

---

## Best 2-minute demo order

1. Open with general category: “debugger for biotech research experiments.”
2. Show the broad assay troubleshooting workflow first or mention it explicitly.
3. Run the ex-vivo preservation hero case because it is visceral.
4. Flash organoid/OoC presets to prove generality.
5. End with the invariant workflow: evidence-backed mechanisms, next measurement, human review.

## Product implication

Do not market BioSignal Navigator as a tissue-engineering or perfusion platform. Market it as a general **biotech research troubleshooting workspace**, then prove it through concrete workflows where the same loop repeats.
