# Final Submission Runbook

Use this at the venue. Goal: submit a clean public GitHub repo, a short demo video, and side-prize proof without adding risky new features.

## 0. Current product story

**One-liner**

> BioSignal Navigator is a general biotech R&D troubleshooting workspace that turns messy experimental runs into evidence-backed hypotheses, next discriminating measurements, and a human review decision.

**Do say**

- general biotech R&D troubleshooting workspace;
- research workflow only;
- possible mechanisms;
- evidence-backed hypotheses;
- next discriminating measurement;
- human review required;
- Pioneer structured extraction layer;
- outcome loop produces training/eval rows.

**Do not say**

- diagnosis;
- treatment;
- viability prediction;
- clinical decision support;
- transplant/discard recommendation;
- batch release or disposition decision.

## 1. Run the app

```bash
cd /root/projects/biosignal-navigator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # optional, then add keys if available
streamlit run app/main.py --server.port 8501 --server.address 0.0.0.0
```

Health check:

```bash
curl -fsS http://127.0.0.1:8501/_stcore/health
# expected: ok
```

If port 8501 is busy:

```bash
streamlit run app/main.py --server.port 8502 --server.address 0.0.0.0
```

## 2. Connect to GitHub

Create a public GitHub repo named `biosignal-navigator`, without initializing it with README/gitignore/license.

Then:

```bash
cd /root/projects/biosignal-navigator
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/biosignal-navigator.git
git push -u origin main
```

If `origin` already exists:

```bash
git remote set-url origin https://github.com/YOUR_USERNAME/biosignal-navigator.git
git push -u origin main
```

Sanity check:

```bash
git status --short --branch
git remote -v
```

## 3. Aikido side-prize proof

Do not claim Aikido is complete until this artifact exists.

1. Connect the public GitHub repo to Aikido.
2. Run the scan.
3. Screenshot the report with issue categories visible.
4. Save it as:

```text
docs/assets/aikido-security-report.png
```

5. Commit and push:

```bash
mkdir -p docs/assets
git add docs/assets/aikido-security-report.png
git commit -m "docs: add Aikido security report"
git push
```

## 4. Demo video sequence — 2 minutes

### 0:00–0:10 Problem

> Biotech R&D teams lose days when an experiment fails and nobody knows whether the issue is biology, protocol drift, reagent failure, instrument drift, or environment.

### 0:10–0:25 Product

> BioSignal Navigator is a general biotech R&D troubleshooting workspace. It turns messy run notes into possible mechanisms, evidence with caveats, ranked next actions, and a human review decision. It is research workflow software, not clinical decision support.

### 0:25–0:55 General-purpose proof

Use **Custom workflow** if stable, otherwise **Assay signal collapse** preset.

Custom workflow example:

```text
Workflow / assay: ADC conjugation assay
Sample / system: antibody-drug conjugate batch 17
Observed anomalies:
- DAR lower than expected
- aggregation increased
- HIC shoulder peak
Goal: choose the next discriminating analytical check
Constraints: research workflow only; no release or clinical recommendation
```

Show that the UI infers the workflow family and adapts the workspace.

### 0:55–1:20 Decision workflow

Show:

1. recommended next actions;
2. uncertainty map;
3. evidence quality ladder;
4. scientist review mode.

Line:

> The app does not pretend to know the answer. It asks what measurement would change the team’s mind fastest.

### 1:20–1:40 Outcome + Pioneer loop

Show Run Outcome and the generated Pioneer training row.

Line:

> Pioneer is the structured extraction layer. Human-reviewed outcomes become training and eval rows for observations, mechanisms, measurements, relations, and safety flags.

### 1:40–1:55 Partner stack

Show partner trace.

Line:

> Gemini supports synthesis, Tavily retrieves sources, Pioneer structures extraction, and Aikido gives public-repo security hygiene.

### 1:55–2:00 Close

> BioSignal Navigator turns experimental ambiguity into a defensible next step — evidence first, uncertainty visible, human judgment preserved.

## 5. Prize checklist

| Prize / criterion | Proof to show |
|---|---|
| Main hackathon | running app, clean repo, 2-minute video, clear product story |
| Partner tech | UI partner trace + `docs/partner_tech.md` |
| Atira | agent-human orchestration + scientist review + outcome loop |
| Pioneer / Fastino | structured extractor, triples/relations, training row, `docs/pioneer_strategy.md` |
| Aikido | `docs/assets/aikido-security-report.png` screenshot after scan |
| Trust/safety | evidence quality ladder + research-only wording |
| Generality | custom workflow builder + multiple presets |

## 6. Last verification before submit

```bash
cd /root/projects/biosignal-navigator
source .venv/bin/activate
python -m compileall -q app tests
python -m unittest discover -s tests -p 'test_*.py' -v
git status --short --branch
```

Expected:

- tests pass;
- repo clean except intentional Aikido screenshot before commit;
- GitHub repo public and accessible;
- README renders setup instructions;
- demo video link works.

## 7. If something breaks

Prioritize in this order:

1. Public GitHub repo with README.
2. App runs locally with deterministic fallback.
3. 2-minute video shows the app working.
4. Partner trace visible.
5. Aikido screenshot if available.

Do not add new product features in the final hour unless the demo cannot be understood without them.
