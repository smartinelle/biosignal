"""Pioneer fine-tuning runner — verified against the live Pioneer API.

Implements the documented 5-step workflow from https://docs.pioneer.ai. The
endpoint paths and payload shapes below were verified against the live API
(base URL https://api.pioneer.ai, `X-API-Key` auth) — note the management
routes live at the ROOT, not under `/v1` (which is only the OpenAI/Anthropic
compatible chat surface).

Verified routes:
    GET  /base-models                          browse base models
    POST /generate                             start synthetic data generation
    GET  /generate/jobs/{job_id}               poll a generation job
    GET  /felix/datasets                       list datasets
    GET  /felix/datasets/{id}                  dataset version info
    POST /felix/training-jobs                  start a fine-tune
    GET  /felix/training-jobs/{id}             poll a training job (status, metrics)
    GET  /felix/training-jobs                  list training jobs
    POST /felix/evaluations                    run an evaluation
    POST /inference                            run a prediction (Pro plan / billing)

Auth: X-API-Key header. Reads PIONEER_API_KEY from env / .env. Never prints it.

Usage:
    python pioneer/finetune.py generate          # synthetic dataset on Pioneer
    python pioneer/finetune.py train  --dataset-id <id> --dataset-name <name>
    python pioneer/finetune.py status --job-id <id>
    python pioneer/finetune.py infer  --job-id <id>      # needs paid plan
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
except Exception:
    pass

import requests

BASE_URL = os.getenv("PIONEER_BASE_URL", "https://api.pioneer.ai")
API_KEY = os.getenv("PIONEER_API_KEY", "")
ARTIFACTS = Path(__file__).resolve().parent / "artifacts"


def _h() -> dict:
    return {"X-API-Key": API_KEY, "Content-Type": "application/json"}


def _require_key() -> None:
    if not API_KEY:
        print("ERROR: PIONEER_API_KEY not set (check .env).")
        sys.exit(1)


def _save(name: str, payload: dict) -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / name).write_text(json.dumps(payload, indent=2))
    print(f"  saved -> pioneer/artifacts/{name}")


def cmd_generate(args: argparse.Namespace) -> None:
    """Step 1+2: generate a labelled NER dataset on Pioneer."""
    _require_key()
    body = {
        "dataset_name": args.dataset_name,
        "task_type": "ner",
        "domain": (
            "messy biotech experiment troubleshooting notes; extract macro signals, "
            "their trends, candidate failure mechanisms, and discriminating assays; "
            "flag clinical-overclaim requests as out of scope"
        ),
        "labels": ["macro_signal", "trend", "candidate_mechanism", "assay", "safety_boundary"],
        "num_examples": args.num,
    }
    print(f"[POST] {BASE_URL}/generate  ({args.num} examples)")
    r = requests.post(f"{BASE_URL}/generate", headers=_h(), json=body, timeout=90)
    print(f"  -> HTTP {r.status_code}")
    data = r.json()
    print(f"  job_id={data.get('job_id')} status={data.get('status')}")
    if not r.ok:
        return
    job_id = data["job_id"]
    for i in range(30):
        time.sleep(8)
        p = requests.get(f"{BASE_URL}/generate/jobs/{job_id}", headers=_h(), timeout=30).json()
        st = p.get("status")
        print(f"  poll {i}: {st} count={p.get('count')}")
        if st in {"ready", "completed", "succeeded"}:
            ds = p.get("dataset") or {}
            print(f"  dataset ready: id={ds.get('id', job_id)} examples={p.get('count')}")
            _save("generate_job.json", p)
            return
        if st in {"failed", "error"}:
            _save("generate_job.json", p)
            return
    print("  generation still running; check later with /generate/jobs/{id}")


def cmd_train(args: argparse.Namespace) -> None:
    """Step 3: start a GLiNER2 fine-tune from a generated/uploaded dataset."""
    _require_key()
    body = {
        "model_name": args.model_name,
        "base_model": args.base_model,
        "datasets": [{"id": args.dataset_id, "name": args.dataset_name}],
        "task_type": "ner",
    }
    print(f"[POST] {BASE_URL}/felix/training-jobs  base={args.base_model}")
    r = requests.post(f"{BASE_URL}/felix/training-jobs", headers=_h(), json=body, timeout=120)
    print(f"  -> HTTP {r.status_code}")
    data = r.json()
    if not r.ok:
        print(f"  body: {json.dumps(data)[:400]}")
        return
    print(f"  job_id={data.get('id')} status={data.get('status')} instance={data.get('instance_type')} epochs={data.get('nr_epochs')}")
    _save("training_job.json", data)


def cmd_status(args: argparse.Namespace) -> None:
    """Step 4: poll a training job for status + F1/precision/recall metrics."""
    _require_key()
    r = requests.get(f"{BASE_URL}/felix/training-jobs/{args.job_id}", headers=_h(), timeout=30)
    data = r.json()
    print(f"  status: {data.get('status')} / {data.get('normalized_status')}")
    print(f"  base_model: {data.get('base_model')}  instance: {data.get('instance_type')}")
    metrics = data.get("metrics") or {}
    if metrics:
        print(f"  metrics: F1={metrics.get('f1')} P={metrics.get('precision')} R={metrics.get('recall')}")
    if data.get("error_message"):
        print(f"  error: {data['error_message']}")
    _save("training_status.json", data)


def cmd_infer(args: argparse.Namespace) -> None:
    """Step 5: run inference against the base or fine-tuned model.

    Requires a Pro plan / active billing; on Free tier this returns HTTP 402.
    """
    _require_key()
    sample = args.text or (
        "48h cold-preserved kidney at 48h, lactate rising, vascular resistance increasing, "
        "creatinine elevated. Goal: decide what to measure next. Research workflow only."
    )
    body = {
        "model_id": args.job_id or args.base_model,
        "text": sample,
        "schema": {
            "entities": ["macro_signal", "trend", "candidate_mechanism", "assay", "safety_boundary"],
            "classifications": [{"task": "safety", "labels": ["research_workflow_only", "clinical_claim_risk"]}],
        },
        "threshold": 0.35,
    }
    print(f"[POST] {BASE_URL}/inference  model={body['model_id']}")
    r = requests.post(f"{BASE_URL}/inference", headers=_h(), json=body, timeout=60)
    print(f"  -> HTTP {r.status_code}")
    if r.status_code == 402:
        print("  PAYMENT REQUIRED: activate a paid plan at https://agent.pioneer.ai/billing")
        return
    data = r.json()
    print(json.dumps(data, indent=2)[:800])
    _save("inference_result.json", data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Pioneer fine-tuning workflow runner.")
    sub = parser.add_subparsers(dest="command", required=True)

    g = sub.add_parser("generate", help="Generate a synthetic NER dataset on Pioneer.")
    g.add_argument("--dataset-name", default="biosignal-troubleshooting-extraction")
    g.add_argument("--num", type=int, default=120)
    g.set_defaults(func=cmd_generate)

    t = sub.add_parser("train", help="Start a GLiNER2 fine-tune.")
    t.add_argument("--dataset-id", required=True)
    t.add_argument("--dataset-name", required=True)
    t.add_argument("--model-name", default="biosignal-gliner2-troubleshooting")
    t.add_argument("--base-model", default="fastino/gliner2-base-v1")
    t.set_defaults(func=cmd_train)

    s = sub.add_parser("status", help="Poll a training job.")
    s.add_argument("--job-id", required=True)
    s.set_defaults(func=cmd_status)

    i = sub.add_parser("infer", help="Run inference (needs paid plan).")
    i.add_argument("--job-id", default=None)
    i.add_argument("--base-model", default="fastino/gliner2-base-v1")
    i.add_argument("--text", default=None)
    i.set_defaults(func=cmd_infer)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
