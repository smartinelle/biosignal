# BioSignal Navigator — Product Spec

Status: v1 — product package for the hackathon build and immediate post-hackathon validation.

## Product thesis

BioSignal Navigator is a **biotech R&D troubleshooting workspace** that turns messy experimental runs into evidence-backed hypotheses, next actions, and a shared decision artifact.

It is broad by design: useful across assay development, molecular biology, protein/process workflows, organoid / organ-on-chip workflows, tissue preservation research, translational biomarker planning, and adjacent wet-lab / computational troubleshooting.

The product is **not** a generic AI chat surface. It is a workflow-specific troubleshooting system:

```text
protocol + run data + notes + evidence
→ structured problem summary
→ likely failure modes
→ evidence with caveats
→ next discriminating experiments
→ human review / partner-ready memo
```

Safety boundary: research-use only. No clinical decision-making, viability prediction, transplant/discard recommendation, diagnosis, treatment, or patient claims.

## ICPs

### ICP A — Assay development / screening teams

- Users: assay developers, screening scientists, translational assay scientists.
- Pain: weak signal, noisy controls, plate effects, reagent-lot drift, inconsistent replicates.
- Buyer/user lead: head of assay development, R&D director, scientific founder.
- Best first proof: “why did signal collapse after a reagent/protocol change?”

### ICP B — CROs / assay service providers

- Users: scientists who repeatedly troubleshoot client studies and validation runs.
- Pain: repeated failures, scattered case memory, hard client handoffs.
- Buyer: scientific director, operations lead, founder.
- Best first proof: partner-ready troubleshooting memo with risk flags and next checks.

### ICP C — Molecular biology / omics teams

- Users: qPCR/ddPCR, sequencing, library-prep, bioinformatics/QC teams.
- Pain: QC anomalies, batch effects, contamination, low complexity, outliers.
- Buyer: platform lead, genomics lead, translational science lead.
- Best first proof: “is this biology or technical failure?”

### ICP D — Living model / tissue system teams

- Users: organoid, organ-on-chip, tissue engineering, preservation/perfusion R&D teams.
- Pain: hidden biological state, ambiguous multimodal readouts, uncertain next assay.
- Buyer: platform lead, CTO/scientific founder, lab head.
- Best first proof: organoid/OoC/preservation use cases, but not the category itself.

## Jobs-to-be-done

1. **Diagnose why an experiment failed or underperformed.**
   - Example: low assay signal, qPCR anomaly, protein yield collapse, tissue readout drift.

2. **Turn a messy experimental record into an actionable troubleshooting plan.**
   - “What changed, what matters, what should we test next?”

3. **Compare runs and surface patterns.**
   - Reagent sensitivity, operator variance, instrument drift, batch effects, environmental excursions.

4. **Create a shared, auditable explanation for scientific decisions.**
   - Evidence, assumptions, alternatives, uncertainty, and rationale.

5. **Shorten the path from problem to next experiment.**
   - Move from “something is off” to prioritized hypotheses and validation matrix.

## Use-case map

### 1. Assay troubleshooting copilot

- Inputs: protocol, controls, plate map, QC metrics, lot metadata, notes, prior runs.
- Outputs: failure-mode ranking, likely root causes, next controls/checks, rerun plan.
- Proof workflow: weak/noisy signal after reagent lot change.

### 2. Molecular assay anomaly navigator

- Inputs: qPCR/ddPCR curves, Ct tables, controls, primer/probe info, extraction batch, operator notes.
- Outputs: contamination/primer/template/inhibition hypotheses, next controls, trust decision.
- Proof workflow: Ct shift + weird NTC/melt curve.

### 3. Protein/process troubleshooting

- Inputs: expression/purification conditions, chromatogram, SDS-PAGE/SEC/DLS summaries, buffers, historical run.
- Outputs: expression vs recovery vs stability hypotheses, next screen/check.
- Proof workflow: yield drop + extra SEC peak.

### 4. Bioprocess / fermentation deviation

- Inputs: pH/DO/off-gas/feed/time-series, sensor calibration, inoculum QC, batch metadata.
- Outputs: sensor/process/biological shift hypotheses, next checks.
- Proof workflow: titer underperforms with DO/pH drift.

### 5. Organoid / OoC / tissue-model debugging

- Inputs: imaging summaries, media metabolics, TEER/barrier readouts, markers, culture conditions, notes.
- Outputs: model instability vs toxicity vs protocol/artifact hypotheses, next assay.
- Proof workflow: organoid QC anomaly or organ-on-chip drug-response ambiguity.

### 6. Tissue preservation / ex-vivo monitoring research

- Inputs: lactate, pH, flow, resistance, oxygenation, perfusion/preservation metadata, assay outputs.
- Outputs: possible mechanisms, caveats, next measurements, human review question.
- Proof workflow: 48h preserved tissue with underdetermined macro signals.

### 7. Cross-run troubleshooting memory

- Inputs: prior cases, validated fixes, protocols, case notes.
- Outputs: reusable playbooks and “have we seen this before?” retrieval.
- Proof workflow: recurring failure pattern across runs.

## Product surfaces

### Ingestion

- Paste/text problem note for hackathon demo.
- Later: CSV/XLSX run tables, protocol PDFs, ELN exports, instrument QC summaries, images as summaries, webhook/API connectors.

### Workspace

- Troubleshooting case page.
- Structured signals and context.
- Hypothesis ranking.
- Evidence/caveats.
- Ranked action plan.
- Partner-ready memo.
- Case memory.

### Integrations

- Pioneer: deterministic / fine-tuned structured extractor for notes → typed signals, mechanisms, measurements, safety flags.
- Gemini via OpenRouter: synthesis and memo generation.
- Tavily: live evidence retrieval.
- Aikido: security scan artifact.
- Future: ELN/LIMS, instrument exports, cloud storage, Slack/Teams, spreadsheets.

## Onboarding flow

1. Pick workflow type: assay troubleshooting, molecular assay anomaly, protein/process, bioprocess, living model, tissue preservation, or “other R&D issue.”
2. Paste or upload one real problem bundle: protocol/run summary/data export/note.
3. System summarizes: what changed, what failed, what evidence exists, what is missing.
4. User confirms constraints: available samples, time/budget, platform, what cannot change.
5. Navigator produces: hypotheses, evidence gaps, next checks, partner-ready summary.
6. User marks which recommendation was useful to build case memory.

## Activation moment

Activation happens when the user sees **one credible next step they would actually run**.

Definition:

- problem summarized correctly;
- at least one plausible non-obvious cause surfaced;
- next experiment/control is specific enough to act on;
- uncertainty is explicit rather than hidden.

## Pricing hypothesis

Early packaging:

- Starter: $99–$299/month for small teams, manual uploads, limited cases.
- Team: $499–$1,500/month for shared workspace, case history, templates, collaboration.
- Pro/platform: $2,500+/month for API/connectors, custom workflows, auditability, admin controls.

Pricing thesis: users pay for **time saved, fewer wasted cycles, and reusable troubleshooting memory**, not “AI.”

## ROI story

Direct value:

- fewer failed iterations;
- faster root-cause narrowing;
- less senior-scientist triage time;
- better reuse of prior learning;
- clearer handoff between bench, analysis, and partners.

Proof language:

- “Turn one week of troubleshooting into one afternoon of focused tests.”
- “Make prior runs usable as institutional memory.”
- “Reduce the gap between data and next experiment.”

## Differentiation

BioSignal Navigator is not:

- generic chat;
- generic literature search;
- static protocol repository;
- black-box score;
- ELN/LIMS replacement.

It is:

- a structured troubleshooting layer on top of biotech research workflows;
- evidence-aware and uncertainty-first;
- designed to produce next actions and shared decision artifacts.

## Validation questions

Buyer/value:

- What failed workflow already burns time or budget?
- What does one wasted iteration cost?
- Who owns the budget for reducing troubleshooting time?

Workflow:

- What data exists when a run goes wrong?
- What is fragmented or lost?
- What decision changes after diagnosis?

Product shape:

- Should v1 be chat workspace, structured case form, or run comparison dashboard?
- What output would get forwarded to a colleague or partner?
- What integrations are mandatory vs nice-to-have?

Go/no-go:

Proceed if users say:

- “This saved me time.”
- “This gave me a better troubleshooting plan.”
- “This captured knowledge we would otherwise lose.”

Narrow/kill if it becomes too generic, too dependent on perfect data ingestion, too close to clinical decision support, or too abstract to change what scientists do next.
