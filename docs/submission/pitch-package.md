# Submission Pitch Package

Status: v1 — hackathon video and finalist pitch package.

## Positioning

BioSignal Navigator is a **general biotech R&D troubleshooting workspace** that turns messy experimental runs into evidence-backed hypotheses, ranked next steps, and partner-ready summaries.

It is not a tissue-engineering niche. Tissue preservation, organoids, and organ-on-chip are proof workflows inside a broader category.

Safety boundary: research-use only. No clinical decision support, diagnosis, treatment, viability prediction, transplant/discard guidance, batch disposition, or release-readiness claims.

## Core one-liner

> BioSignal Navigator is a biotech R&D troubleshooting workspace that turns messy runs into evidence-backed hypotheses and next actions.

Alternates:

- “The troubleshooting layer for biotech R&D teams.”
- “From failed runs to ranked next steps, with evidence and uncertainty built in.”
- “A decision workspace for diagnosing why biotech experiments underperform — research-use only.”
- “Evidence first, answers second.”

## 2-minute video script

Goal: make a judge understand the product in one watch.

### 0:00–0:10 — Problem

Visual: landing screen / title.

Voiceover:

> “Biotech R&D teams lose days when an experiment fails and nobody knows whether the issue is biology, protocol drift, reagent failure, or instrumentation.”

### 0:10–0:25 — Product category

Visual: preset selector with broad workflows.

Voiceover:

> “BioSignal Navigator is a troubleshooting workspace for biotech research. It starts from real workflows: weak assay signal, qPCR anomalies, protein yield drops, cell culture drift, or living-system readouts.”

### 0:25–0:45 — Run broad workflow

Visual: assay signal collapse preset.

Voiceover:

> “Here the assay signal dropped after a reagent-lot change. The app structures the problem, detects controls and edge effects, and separates technical artifact from possible biology.”

### 0:45–1:05 — Evidence and uncertainty

Visual: bottleneck + evidence/caveats.

Voiceover:

> “It is uncertainty-first. It shows what the evidence supports, what remains unresolved, and why the team should not over-interpret the result yet.”

### 1:05–1:25 — Action plan

Visual: top 3 action cards.

Voiceover:

> “The output is a ranked action plan: old-vs-new reagent control, edge-vs-center plate analysis, and an orthogonal readout if needed. Each action has rationale, effort, confidence, and expected readout.”

### 1:25–1:40 — Use-case generality

Visual: flash qPCR/protein/cell culture/preservation/organoid presets.

Voiceover:

> “The same loop works across biotech R&D: molecular assays, protein workflows, cell culture, bioprocessing, and thesis-flavored living-system cases like tissue preservation.”

### 1:40–1:55 — Partner stack

Visual: partner trace.

Voiceover:

> “Gemini via OpenRouter supports synthesis, Tavily retrieves evidence, Pioneer/Fastino makes extraction deterministic, and Aikido supports secure public-repo hygiene.”

### 1:55–2:00 — Close

Visual: partner-ready summary / export.

Voiceover:

> “The result is not a chat transcript. It is a defensible next step the team can act on.”

## 5-minute finalist pitch outline

### 0:00–0:30 — Hook

Biotech teams do not fail because they lack data. They fail because experimental data becomes ambiguous:

- assay signal drops;
- qPCR controls drift;
- protein yield collapses;
- culture behavior changes;
- tissue readouts conflict.

Message:

> “The bottleneck is turning a messy run into a defensible next experiment.”

### 0:30–1:15 — Product definition

BioSignal Navigator is the troubleshooting layer for biotech R&D.

It ingests notes/run context, structures signals, proposes mechanisms, retrieves evidence, ranks next actions, and produces a partner-ready summary.

### 1:15–2:15 — Demo

Use assay signal collapse as the broad demo:

1. weak signal + normal cell count;
2. positive-control drift;
3. plate-edge effect;
4. reagent lot change;
5. ranked action plan.

Then flash preservation/organoid/OoC to show thesis resonance and generality.

### 2:15–3:15 — Technical architecture

- Pioneer/Fastino: deterministic structured extraction from messy notes.
- Gemini via OpenRouter: synthesis and memo generation.
- Tavily: evidence retrieval.
- Aikido: security scan for public repo hygiene.
- Human review: final unresolved scientific judgment.

### 3:15–4:15 — Why now / impact

- Biotech teams already use AI tools, but generic chat does not fit troubleshooting workflows.
- R&D data is fragmented across protocols, spreadsheets, ELNs, instruments, and people.
- A single wasted cycle can cost days to weeks.

Value line:

> “Turn one week of troubleshooting into one afternoon of focused tests.”

### 4:15–5:00 — Close

Reinforce:

- general biotech R&D troubleshooting;
- research-only safety;
- uncertainty-first outputs;
- partner-ready action plan;
- extensible product category.

Close line:

> “BioSignal Navigator helps biotech teams move from ambiguity to action with evidence, structure, and human judgment.”

## Partner-tech talking points

### Gemini via OpenRouter

Role: synthesis layer for evidence, hypotheses, caveats, and memo text.

Talking point:

> “Gemini helps produce a coherent troubleshooting narrative from structured signals and retrieved evidence.”

### Tavily

Role: live evidence/source retrieval.

Talking point:

> “Tavily keeps the workflow grounded in current sources instead of free-form guessing.”

### Pioneer / Fastino

Role: deterministic structured extraction from experiment notes.

Talking point:

> “Pioneer is the small-model path: consistent extraction of signals, mechanisms, measurements, relations, and safety flags — replacing a repeated frontier-LLM parsing call.”

### Aikido

Role: public repo/security hygiene.

Talking point:

> “Aikido gives us a security scan artifact for a repo that handles partner integrations and research workflow data.”

### Atira track

Role: agent-human orchestration.

Talking point:

> “This is not one chatbot. It is an orchestrated workflow: extraction, evidence, synthesis, action planning, and human review.”

## Judging criteria map

- Creativity: biotech R&D debugger, not generic healthcare chat.
- Technical complexity: multi-agent pipeline, deterministic extractor, live/fallback partner trace, action-plan schema.
- Partner tech: Gemini/OpenRouter, Tavily, Pioneer/Fastino, Aikido.
- Atira fit: specialized agents plus human review around uncertainty.
- Utility: turns ambiguous run into ranked next actions.
- Trust: evidence/caveats and explicit research-only guardrails.
- Generality: assay/qPCR/protein/cell culture/process/living-system workflows.

## Demo choreography

1. Open on product category, not tissue engineering.
2. Select broad assay troubleshooting preset.
3. Show bottleneck and structured signals.
4. Show hypotheses and evidence with caveats.
5. Show action-plan cards.
6. Show partner-ready summary.
7. Flash living-system use cases.
8. Close on partner trace and exportable memo.

## Lines to avoid

Avoid:

- “predicts viability”;
- “clinical decision support”;
- “decides whether to discard”;
- “diagnoses the issue” in a medical sense;
- “knows the true biological state.”

Use instead:

- “possible mechanisms”;
- “evidence-backed hypotheses”;
- “next discriminating measurement”;
- “human review”;
- “research-use troubleshooting.”

## Very short judge-facing summary

> BioSignal Navigator is a general biotech R&D troubleshooting workspace. It ingests messy experiment context, extracts structured signals, retrieves supporting evidence, and produces a ranked, uncertainty-aware next-step plan. It is research-use only and designed to turn ambiguous failed runs into defensible action plans.
