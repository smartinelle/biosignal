# BioSignal Navigator

Agent-human evidence routing from biomedical observations to molecular hypotheses and next measurements.

## Hackathon framing

BioSignal Navigator is **not** a diagnostic or treatment system. It is a research workflow tool for biomedical evidence routing:

- structure messy observations
- generate plausible biological mechanisms
- retrieve supporting / contradictory evidence
- suggest assays and biomarkers that reduce uncertainty
- escalate unresolved decisions to a human expert

First demo vertical: tissue preservation / tissue engineering viability.

## Partner technologies

- Google Gemini: synthesis, mechanism mapping, final evidence card
- Tavily: literature/dataset search and extraction
- Pioneer: small structured extractor/evaluator for observation → mechanism → biomarker triples
- Aikido: repository security scan screenshot for side challenge

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app/main.py --server.port 8501 --server.address 0.0.0.0
```

## Demo scenario

Cold-preserved tissue sample, 48h, rising lactate, falling pH, increasing vascular resistance. The app routes this to hypotheses such as hypoxia, mitochondrial stress, endothelial dysfunction, inflammatory activation, and cell-type-specific degradation, then recommends measurements and asks a human review question.
