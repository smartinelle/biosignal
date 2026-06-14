# Preset Output Spec

Status: v1 — deterministic preset/output contract for broad biotech R&D troubleshooting.

## Purpose

BioSignal Navigator should not feel like a tissue-engineering niche tool. Each preset proves the same general product loop:

```text
ambiguous research run → detected signals → plausible mechanisms → discriminating measurements → ranked actions → human review
```

Hard boundary: research-use only. The system must not output diagnosis, treatment, viability prediction, transplant/discard guidance, batch disposition, release readiness, or biological ground truth.

## Global output contract

Every preset should emit:

1. Input note
2. Detected signals
3. Likely hypotheses
4. Next measurements
5. Action-plan top 3
6. What we do not know
7. Human decision
8. Safety phrasing

Formatting rules:

- Use “could indicate”, “may reflect”, “consistent with”, not definitive language.
- Separate technical artifact from biological change when both are plausible.
- Prioritize controls, orthogonal checks, and time-course comparison before interventions.
- Keep action items research-facing.
- If evidence is weak, say so explicitly.

## Preset IDs

- `bio.assay_signal_collapse`
- `bio.qpcr_ddpcr`
- `bio.protein_yield_purification`
- `bio.cell_culture_drift`
- `bio.bioreactor_deviation`
- `bio.organoid_ooc`
- `bio.preservation`

---

## 1. Assay signal collapse

Input note:

> Cell-based potency assay signal is 40% lower than expected. Cell count is normal. Positive control drifted, plate edge wells look worse, and reagent lot changed last week.

Detected signals:

- low signal with normal cell count;
- positive-control drift;
- edge-well / plate-position effect;
- reagent-lot change;
- uncertainty between true biology and technical artifact.

Likely hypotheses:

1. Plate artifact / edge effect.
2. Reagent lot or stability issue.
3. Protocol timing / handling drift.
4. Assay signal decoupled from cell number.
5. Real biological potency change, lower priority until controls are resolved.

Next measurements:

- old-vs-new reagent lot control run;
- edge-vs-center plate-layout analysis;
- positive/negative control repeat;
- orthogonal potency/readout assay;
- protocol timing and incubation audit.

Action-plan top 3:

1. Validate controls and reagent lot before interpreting sample biology.
2. Test whether the signal drop is spatially localized to plate edge effects.
3. Run an orthogonal readout only after the assay system is stable enough to interpret.

What we do not know:

- whether the signal drop is assay chemistry or sample biology;
- whether the effect is plate-localized or global;
- whether instrument settings or read timing changed;
- whether normalization hides the real trend.

Human decision:

> Decide whether the run should be treated as invalid, partially interpretable, or worth repeating with tighter controls.

Safety phrasing:

> Research-only troubleshooting guidance; this does not establish assay validity, biological absence, clinical relevance, or any release/discard decision.

---

## 2. qPCR / ddPCR amplification anomaly

Input note:

> qPCR Ct values are 3 cycles later than expected. Melt curve has a shoulder, NTC shows weak amplification, and positive control failed intermittently. RNA integrity is borderline.

Detected signals:

- Ct/Cq shift;
- abnormal melt curve;
- no-template-control amplification;
- intermittent positive-control failure;
- borderline template quality.

Likely hypotheses:

1. PCR inhibition or extraction carryover.
2. Template degradation or low input.
3. Primer-dimer / poor specificity.
4. Contamination or amplicon carryover.
5. Reverse-transcription or setup variability.

Next measurements:

- dilution series plus inhibition control;
- no-RT / NTC / positive-control repeat;
- alternate primer/probe set;
- re-extract sample;
- spike-in control or orthogonal assay.

Action-plan top 3:

1. Verify control behavior before interpreting sample-level expression.
2. Run dilution/inhibition and no-RT controls to localize the failure mode.
3. Confirm with an alternate primer/probe or orthogonal method.

What we do not know:

- whether the issue is extraction, RT, amplification, or analysis;
- exact nucleic-acid integrity and input amount;
- primer/probe specificity in this sample context;
- whether contamination or thresholding artifact drives the result.

Human decision:

> Decide whether to rerun, redesign the assay, or treat the result as inconclusive.

Safety phrasing:

> Research-only troubleshooting guidance; this does not establish biological truth, diagnostic meaning, viability, clinical relevance, or any release/discard decision.

---

## 3. Protein yield / purification drop

Input note:

> Recombinant protein run produced 60% lower yield than baseline. SDS-PAGE shows extra bands, SEC has a shoulder peak, DLS indicates aggregation, induction temperature changed, and buffer pH was lower than usual.

Detected signals:

- yield loss;
- extra bands / degradation or contamination;
- SEC shoulder;
- aggregation;
- induction and buffer changes.

Likely hypotheses:

1. Expression bottleneck or fold-state shift.
2. Proteolysis during harvest/purification.
3. Resin overload / weak binding / poor recovery.
4. Buffer pH or salt-driven aggregation.
5. Storage or concentration instability.

Next measurements:

- mass-balance fraction audit: input, soluble, insoluble, flow-through, wash, elution;
- SDS-PAGE / Western / activity across stages;
- buffer pH/salt screen;
- induction temperature mini-matrix;
- protease inhibitor check or mass spec confirmation.

Action-plan top 3:

1. Map where the protein is lost before optimizing the wrong step.
2. Determine whether the main bottleneck is expression, recovery, or stability.
3. Test small buffer/induction variants before repeating a full run.

What we do not know:

- construct/tag/host context;
- whether extra bands are degradation or co-purification;
- whether activity loss tracks purity, folding, or assay mismatch;
- whether the yield drop is stage-specific.

Human decision:

> Decide whether to optimize expression, redesign purification, or prioritize functional confirmation.

Safety phrasing:

> Research-only troubleshooting guidance; this does not establish purity suitability, functional adequacy, clinical relevance, or any disposition decision.

---

## 4. Cell culture drift

Input note:

> Cells grew slower after thaw. Morphology shifted, confluency stalled, media color changed earlier than usual, media lot changed, and incubator CO2 had a short excursion.

Detected signals:

- growth-rate decline;
- morphology shift;
- stalled confluency;
- media pH/color change;
- media lot and incubator changes;
- passage-to-passage variability.

Likely hypotheses:

1. Media/serum/reagent lot shift.
2. Incubator drift or environmental excursion.
3. Seeding/split/thaw handling issue.
4. Low-grade contamination, including mycoplasma.
5. Passage-related biological drift or selection.

Next measurements:

- contamination and mycoplasma check;
- media-lot side-by-side;
- incubator log/calibration review;
- seeding-density titration;
- compare with early-passage or reference stock.

Action-plan top 3:

1. Rule out contamination and identity/environment failures before interpreting phenotype.
2. Compare current cells to a known-good reference passage or stock.
3. Isolate media lot and incubator variables with a small side-by-side test.

What we do not know:

- exact passage/thaw history;
- whether drift is reversible;
- whether media, environment, handling, or biology caused it;
- whether a hidden confounder changed at the same time.

Human decision:

> Decide whether to continue the current line, reset from stock, or treat the current state as a separate experimental condition.

Safety phrasing:

> Research-only troubleshooting guidance; this does not establish viability, quality, identity, or any release/discard decision.

---

## 5. Bioreactor deviation

Input note:

> Bioreactor titer underperformed. DO drifted lower mid-run, pH control required more base, off-gas diverged from historical batch, and foam spiked after feed change.

Detected signals:

- low titer;
- DO and pH/base-demand drift;
- off-gas divergence;
- foam spike;
- feed-change temporal association.

Likely hypotheses:

1. Oxygen-transfer limitation.
2. Feed strategy or pump delivery mismatch.
3. Probe/sensor calibration drift.
4. Foam/shear/process disturbance.
5. Contamination or biological state shift.

Next measurements:

- sensor calibration / secondary reading;
- off-gas and event timestamp overlay;
- pump/line/feed audit;
- inoculum QC and contamination screen;
- small agitation/aeration sensitivity test.

Action-plan top 3:

1. Confirm whether the deviation is real or sensor-derived.
2. Separate control-loop/process issues from biological response.
3. Compare current trends against historical baselines before changing conditions.

What we do not know:

- whether the deviation is instrumentation, process, or biology;
- exact calibration state;
- onset timing relative to feeds/alarms;
- whether adjacent vessels/runs show the same pattern.

Human decision:

> Decide whether to intervene in process settings, hold for more data, or classify the event as a sensor/process anomaly.

Safety phrasing:

> Research-only troubleshooting guidance; this does not establish process acceptability, batch disposition, release readiness, or any discard decision.

---

## 6. Organoid / organ-on-chip ambiguity

Use this as a living-system proof workflow, not as product category.

Likely outputs should separate:

- matrix/ECM changes;
- seeding or cell-composition mismatch;
- perfusion/shear/oxygen/nutrient gradient;
- bubble/clog/device issue;
- differentiation drift;
- imaging/segmentation artifact.

Next measurements:

- time-lapse morphology against baseline;
- barrier/permeability or functional readout;
- flow/oxygenation/ECM/seeding comparison;
- reference device/batch comparison.

Safety phrase must avoid viability or physiological-validity claims.

---

## 7. Preservation / ex-vivo tissue ambiguity

Use this as thesis anchor and visceral demo, not product category.

Likely outputs should separate:

- metabolic stress;
- oxygenation/perfusion issue;
- endothelial/vascular injury;
- mitochondrial/cold ischemic stress;
- sampling artifact.

Next measurements:

- lactate/pH trend;
- oxygen extraction / perfusate gas delta;
- endothelial injury marker;
- histology/viability stain as research readout only;
- targeted RNA panel only if justified.

Safety phrase must explicitly avoid clinical viability, transplant/discard, or tissue-suitability language.

## Implementation note

If output needs to be serialized, use:

```json
{
  "preset_id": "bio.assay_signal_collapse",
  "input_note": "...",
  "detected_signals": ["..."],
  "likely_hypotheses": ["..."],
  "next_measurements": ["..."],
  "action_plan_top_3": ["..."],
  "what_we_do_not_know": ["..."],
  "human_decision": "...",
  "safety_phrasing": "..."
}
```
