# Decision Memo

Status: v1 — opinionated recommendation from the product-definition sprint (June 2026).

Audience: Sacha. Inputs: `product-research-sprint.md`, `user-segments.md`,
`industry-landscape.md`, `evidence-matrix.md`, `feature-gates.md`.

---

## Recommendation in one line

> Ship BioSignal Navigator as the **agent–human interpretation/troubleshooting layer
> for biotech research workflows**, and use living-tissue experiments as concrete demo
> cases rather than the product category.

---

## 1. Best product framing for the hackathon submission

Keep the current framing — it survived the research — and sharpen it with the gap
thesis:

> **BioSignal Navigator** coordinates agents and a human expert to debug ambiguous
> biotech experiments and choose the next best measurement. It is the **interpretation
> layer** that sits between the instruments (which produce numbers) and the scientist
> (who must decide what to run next) — a layer no device, imaging tool, or ELN copilot
> owns for living-tissue R&D.

Lean into three things judges can see:
- **Uncertainty-first** (the bottleneck section) — the honest opposite of "real-time
  viability assessment" device marketing.
- **Agent–human orchestration** (Atira fit) — visible multi-agent trace + human-review
  handoff.
- **Honest partner orchestration** — live-vs-fallback badges; Pioneer-style structured
  extraction as a deliberate artifact.

## 2. Best post-hackathon use cases for Sacha to explore

**Organoid / organ-on-chip / tissue-engineering QC troubleshooting** remains a strong
test use case. It wins the scorecard (`user-segments.md`) on pain × reachability ×
low-regulation × thesis fit:
- Documented, acute pain (batch variability, no standardized QC).
- Research-use (not patient care) → low regulatory load.
- Reachable, concentrated buyer community already paying for platforms/imaging.
- Keeps the thesis (hidden tissue-state interpretation) without transplant baggage.

Treat **machine perfusion / preservation** as the thesis-resonant demo and long-term
"hero" story, **not** the product category — it is the most regulated, least
reachable segment, and sits closest to the viability red line.

## 3. Which user segment to contact first

1. **Organoid / OoC R&D scientists and platform engineers** (incl. CRO teams) — primary.
2. **Tissue-engineering / regenerative-medicine QC leads** — close second.
3. **Translational-biology / biomarker scientists** — for the assay-planning feature.

Defer transplant/perfusion clinicians to "advisory/credibility" conversations, not
design-partner conversations. See `outreach-list.md`.

## 4. What to demo in the 2-minute video

Use the **tissue-preservation failure** preset (visceral + thesis-anchored + dataset-
backed by PRJEB31843), and narrate the loop:

1. Observation Agent structures a messy note.
2. Mechanism Agent proposes *possible* failure modes (no ground-truth claim).
3. Evidence Agent attaches curated + live (Tavily) sources **with caveats**.
4. Measurement Agent recommends the **next discriminating measurement**.
5. **Uncertainty Bottleneck** — the differentiator: "we name what cannot be known yet."
6. Human-Review Agent escalates the irreducible judgment.
7. Show **live Gemini synthesis** + **Pioneer-style triples** + honest partner trace.

Close with one sentence of generality: *"the same loop runs for organoid and organ-
on-chip QC — preservation is just the most visceral example."* Optionally flash the
organoid/OoC presets to prove breadth without diluting the story.

## 5. What to avoid claiming

- ❌ Viability score / quality grade.
- ❌ Transplant / discard / accept-reject recommendation.
- ❌ Diagnosis, prognosis, or treatment.
- ❌ Macro→micro molecular prediction from surface signals (no paired validation data).
- ❌ "Validated thresholds" — none exist in the perfusion literature.
- ❌ Competing on "real-time viability assessment" with device vendors — deliberately
  cede that framing; uncertainty-first is the wedge.
- ❌ "Generic healthcare AI" / "research assistant" positioning — stay vertical.

## 6. What to build next — only after validation

Gate every new feature on a real workflow moment named by an interviewed user.

- **After ≥3 organoid/OoC interviews confirm the QC-failure moment:**
  - Organoid/OoC-specific presets and biomarker dictionary (Green).
  - Evidence cards tuned to imaging + media-metabolic + effluent readouts (Green).
- **If users ask for it (Yellow, with caveats):**
  - Mechanism ranking with confidence + "requires assay confirmation."
  - Cost/time-saved estimate framed as *illustrative, not measured*.
  - Deeper live enrichment (Tavily/Gemini) and a real Pioneer GLiNER2 fine-tune
    (deterministic extractor stays the default artifact).
- **Integration bet (only if a design partner pulls):** position BSN as the
  interpretation layer **on top of** a Benchling/Scispot data substrate rather than a
  competing system of record.
- **Never (Red):** viability/discard/diagnosis/macro→micro prediction features.

---

## Risks & honest caveats

- **Willingness-to-pay is unproven.** The reproducibility-cost evidence motivates the
  problem; it does not prove a budget line. The outreach interviews are the gate.
- **Horizontal-copilot encroachment.** Benchling AI / Scispot could move into
  interpretation; BSN's defense is biology depth, literature-grounding, uncertainty-
  first framing, and founder credibility.
- **Demo ≠ product.** The demo proves the loop and the orchestration, not clinical or
  predictive validity — keep that explicit in every external conversation.

---

## What changed vs prior positioning

- **No pivot.** The "agent–human troubleshooting for living-tissue R&D" thesis is
  confirmed, not replaced.
- **Sharper use-case map:** tissue engineering / organoid / OoC QC is a strong test
  case, while perfusion remains the demo/credibility anchor. The product itself is
  marketed as general biotech R&D troubleshooting, not a niche tissue-engineering
  platform.
- **Sharper differentiator:** the **interpretation layer nobody owns** + **uncertainty-
  first** as a deliberate counter-position to device "viability assessment" marketing.
- **Boundary reaffirmed:** no-clinical-claims is now framed as a *competitive feature*,
  not just a safety constraint.
