# Evidence Matrix

Status: v1 — grounded in published sources; sufficient for demo claims and feature gating.

---

## Columns

- **Claim** — what the product can assert
- **Source / dataset** — citation or accession
- **Strength** — strong / medium / weak
- **User-facing implication** — how this shapes the demo output
- **Product feature supported** — which UI element or agent output this grounds
- **Caveat / do-not-claim** — what must NOT be implied

---

## Matrix rows

| Claim | Source / dataset | Strength | User-facing implication | Product feature | Caveat / do-not-claim |
|---|---|---|---|---|---|
| Lactate clearance is the most widely used hepatic perfusion quality indicator but validated thresholds are absent | Watson & Jochmans 2018, PMC5843692 | Medium-high (peer-reviewed review) | Evidence card should note lactate clearance is useful but cannot determine viability alone | Evidence card with source/caveat; uncertainty bottleneck | Do not claim lactate clearance determines transplant outcome |
| Existing markers in ex-vivo organ perfusion can be inconclusive; no consensus on standardized assessment methods exists | 2024 systematic review, PMC11408214 | Strong (systematic review) | Product should never output a binary accept/discard decision based on standard markers alone | Uncertainty bottleneck; human review escalation | Do not claim the product resolves what the literature cannot |
| Organ quality assessment and repair strategy matter more than preservation duration alone; mitochondria are central to ischemia-reperfusion injury | Eden & Dutkowski 2023, PMC10663298 | Medium (expert review) | Mechanism layer should include mitochondrial dysfunction and IRI; narrative should frame assessment as active, not passive | Mechanism hypotheses (mitochondrial stress); next-measurement suggestions | Do not claim the product assesses organ quality or recommends repair interventions |
| Cold-preserved human lung, spleen, and esophagus tissue showed relative transcriptomic stability up to ~24h; stronger degradation signals by 72h in some tissues | Madissoon et al. / PRJEB31843, Cell 2020 | Medium (single study, tissue slices) | Default demo evidence card: "tissue stability can differ by timepoint; 48h is within a window where molecular changes may be detectable" | Default demo preset evidence card | Do not extrapolate to whole organs, transplant viability, or other tissue types |
| Human kidney NMP biopsies linked to IRI/DGF show pro-inflammatory innate immune signatures: TNFα/NF-κB, macrophage/MNP activation, allograft rejection-like pathways, tubuloepithelial depletion | GSE293480, Frontiers in Immunology 2025 | Medium (single study, small n, authors state not powered for prediction) | Mechanism layer can cite "innate immune activation and tubuloepithelial stress" as plausible molecular mechanisms; evidence card must include underpowered caveat | Mechanism hypotheses; evidence card with caveat | Do not claim this study predicts DGF or validates any threshold; authors explicitly state underpowered |
| Delayed graft function (DGF) is clinically defined as the need for dialysis within the first 7 days post-transplant (kidney) | SRTR/OPTN kidney annual data reports | Strong (regulatory/administrative definition) | Demo can reference DGF as an outcome concept for clinical framing | Demo narrative context | Do not claim the product predicts DGF |
| Machine perfusion imaging and spectroscopy are emerging as complementary assessment readouts | 2024 systematic review, PMC11408214 | Medium (systematic review, methods not yet standardized) | "Imaging and spectroscopy" can appear as next-measurement suggestions alongside metabolic markers | Next-measurement suggestion list | Do not claim any imaging modality is validated for viability assessment |
| Macro variables (lactate, pH, oxygenation, resistance) are underdetermined without context and trend data | General preservation physiology; supported by all above sources | Strong (corroborated by multiple reviews) | Core product claim: single-timepoint macro signals cannot resolve mechanism; trend + assay context is needed | Uncertainty bottleneck; observation structuring output | Do not claim the product infers biological truth from one snapshot |

---

## Product-level claim summary

Safe to assert:
- "Macro signals are underdetermined without context and targeted assays."
- "Several molecular mechanisms are consistent with these readouts; assay data is needed to discriminate."
- "These markers are used in the literature but thresholds are not validated."
- "The next measurement that would discriminate fastest is X."
- "Human expert review is required before any protocol change."

Unsafe to assert:
- "The tissue has a viability score of X."
- "This organ should be accepted / discarded."
- "The lactate level predicts transplant outcome."
- "This product diagnoses IRI, DGF, or any clinical condition."
