# Dataset Feasibility

Status: scored v1 — sufficient for demo anchoring and evidence card content.

---

## Scoring rubric

- **Demo support:** what the dataset enables in the product demo.
- **Demo limits:** what it cannot support; what to avoid claiming.
- **Effort / risk:** download complexity, sample size, analysis required.
- **Recommended use:** primary demo / evidence card / background only / skip.

---

## Dataset 1 — PRJEB31843 (Tissue Stability Cell Atlas)

| Field | Detail |
|---|---|
| Accession | PRJEB31843 (ENA/EMBL-EBI); published as Madissoon et al., Cell 2020 |
| Organism / organ | Human lung, spleen, esophagus |
| Data type | scRNA-seq |
| Sample count | Multiple donors; multiple cold-preservation timepoints |
| Timepoints | 0h, 12h, 24h, 72h at 4°C HypoThermosol FRS |
| Metadata | Preservation duration, tissue type, donor |
| Outcomes | Relative transcriptomic stability / degradation quality scores |
| Demo support | Anchors the claim that tissue-level molecular signatures shift with cold preservation time; supports the evidence card narrative "molecular stability up to ~24h with tissue-specific degradation by 72h" |
| Demo limits | Tissue slices, not whole-organ transplant viability; lung/spleen/esophagus, not kidney/liver NMP; no viability outcome labels for transplant decision |
| Effort / risk | Medium: scRNA-seq data on EMBL-EBI; bioinformatics pipeline needed for reanalysis; curated summary is sufficient for hackathon evidence card |
| Recommended use | **Primary demo evidence anchor** — use the published qualitative finding as the curated evidence card. Do not attempt full download/reanalysis in hackathon timeframe. |
| Caveat | Do not extrapolate findings to transplant viability or other organ types. State explicitly: "tissue slices, not whole organ; different organs may differ." |

---

## Dataset 2 — GSE293480 (Human kidney NMP transcriptomics)

| Field | Detail |
|---|---|
| Accession | GSE293480 (GEO); published Frontiers in Immunology 2025 |
| Organism / organ | Human kidney |
| Data type | RNA-seq (bulk transcriptomics from NMP biopsies) |
| Sample count | Small (study authors state not powered for predictive biomarker development) |
| Metadata | NMP condition, IRI severity, DGF outcome |
| Outcomes | IRI severity (ATI grading), delayed graft function (DGF) |
| Demo support | Provides molecular mechanism evidence: pro-inflammatory innate immune signatures (TNFα/NF-κB, macrophage activation, allograft rejection-like pathways, tubuloepithelial depletion) linked to IRI/DGF in kidney NMP |
| Demo limits | Underpowered; authors explicitly state not for predictive biomarker development; post-NMP biopsy, not real-time perfusion time series |
| Effort / risk | Low-medium: GEO download is straightforward; count matrix processing requires bioinformatics setup; published findings can be cited without reanalysis |
| Recommended use | **Evidence card / background** — cite published pathway findings (TNFα/NF-κB, innate immune activation) as molecular mechanism evidence for kidney IRI demo. Do not claim predictive power. |
| Caveat | Authors explicitly state underpowered for predictive biomarker development. Do not imply GSE293480 validates any threshold or viability score. |

---

## Dataset 3 — SRTR / OPTN public reports and data

| Field | Detail |
|---|---|
| Source | Scientific Registry of Transplant Recipients (SRTR), OPTN annual data reports |
| Data type | Aggregate transplant outcome statistics, annual reports (PDF/Excel) |
| Coverage | Deceased/living donor transplants, graft survival, DGF rates, donor/recipient factors; US-based |
| Outcomes | Graft survival, DGF (defined: dialysis within first 7 days post-transplant for kidney), rejection rates |
| Demo support | Grounds outcome definitions (DGF), demonstrates clinical scale of the problem (thousands of kidneys/livers transplanted annually, % DGF rates), provides clinical risk factor context |
| Demo limits | No granular ex-vivo perfusion time-series data; no omics; no NMP/HMP real-time variables; aggregate statistics, not individual patient-level data without data request |
| Effort / risk | Low: public annual reports are PDF/Excel downloads without data request; patient-level data requires DUA and review process |
| Recommended use | **Background only / framing context** — use aggregate DGF statistics for demo narrative framing ("DGF affects X% of kidney transplants"). Do not attempt individual-level analysis in hackathon. |
| Caveat | Aggregate data only without a DUA. Cannot validate perfusion or molecular model claims. |

---

## Dataset 4 — Organoid / tissue engineering QC (literature survey)

| Field | Detail |
|---|---|
| Source | Published organoid QC papers, tissue engineering validation studies (no single canonical public dataset) |
| Data type | Published assay results, protocol descriptions, validation benchmarks |
| Coverage | Variable by organoid type (intestinal, liver, kidney, lung); cell viability, differentiation markers, metabolic markers |
| Demo support | Demonstrates that QC bottleneck exists across organoid and tissue engineering workflows; grounds the organoid QC demo preset |
| Demo limits | No single canonical public dataset; heterogeneous methods and QC criteria across organoid types; no standardized outcome labels |
| Effort / risk | High for a systematic review; low for a literature description |
| Recommended use | **Background only** — reference the domain in the demo preset without claiming a specific dataset. The organoid QC demo preset is demonstrative, not dataset-backed. |
| Caveat | Do not imply the organoid QC preset is validated against a specific published dataset unless explicitly cited. |

---

## Recommended demo strategy

Based on this scoring:

| Demo element | Dataset anchor | Use |
|---|---|---|
| Default demo preset (tissue preservation failure) | PRJEB31843 qualitative finding | Curated evidence card in fallback |
| Molecular mechanism evidence | GSE293480 pathway summary | Evidence card bullet, with caveat |
| Clinical outcome framing | SRTR/OPTN aggregate | Narrative context only |
| Organoid QC preset | Literature description | Demo shape, not dataset-backed |

**Do not** claim any dataset validates a threshold, prediction, or viability score.
