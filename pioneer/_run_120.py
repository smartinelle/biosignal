"""Wait for the 120-example generation job, then fine-tune GLiNER2 on it."""
import os, json, time, requests
from pathlib import Path
from dotenv import load_dotenv
load_dotenv("/root/projects/biosignal-navigator/.env")

key = os.getenv("PIONEER_API_KEY")
H = {"X-API-Key": key, "Content-Type": "application/json"}
B = "https://api.pioneer.ai"
art = Path("/root/projects/biosignal-navigator/pioneer/artifacts"); art.mkdir(parents=True, exist_ok=True)

GEN_JOB = "1eec3184-03a9-477a-bf3e-d6acea636028"
DS_NAME = "biosignal-troubleshooting-120"

def redact(d):
    return json.loads(json.dumps(d).replace(os.getenv("PIONEER_API_KEY",""), "<key>")
                      .replace("e3e7bd1b-8c82-4db1-a73a-9305495cbda4", "<redacted-user-id>"))

# 1. wait for generation ready
ds_id = None
for i in range(40):
    p = requests.get(f"{B}/generate/jobs/{GEN_JOB}", headers=H, timeout=30).json()
    st = p.get("status")
    print(f"gen poll {i}: {st} count={p.get('count')}", flush=True)
    if st in ("ready","completed","succeeded"):
        ds_id = (p.get("dataset") or {}).get("id", GEN_JOB)
        (art/"generate_120_job.json").write_text(json.dumps(redact(p), indent=2))
        break
    if st in ("failed","error"):
        print("GENERATION FAILED", flush=True); raise SystemExit(1)
    time.sleep(10)

if not ds_id:
    print("generation not ready in time", flush=True); raise SystemExit(1)

print(f"dataset ready: id={ds_id} name={DS_NAME}", flush=True)

# 2. start fine-tune against the 120-example dataset
body = {
    "model_name": "biosignal-gliner2-120",
    "base_model": "fastino/gliner2-base-v1",
    "datasets": [{"id": ds_id, "name": DS_NAME}],
    "task_type": "ner",
}
r = requests.post(f"{B}/felix/training-jobs", headers=H, json=body, timeout=120)
print("train POST ->", r.status_code, flush=True)
job = r.json()
if not r.ok:
    print(json.dumps(job)[:400], flush=True); raise SystemExit(1)
jid = job.get("id")
(art/"training_120_job.json").write_text(json.dumps(redact(job), indent=2))
print(f"TRAINING JOB: {jid} status={job.get('status')} epochs={job.get('nr_epochs')}", flush=True)

# 3. poll to terminal (up to ~40 min)
for i in range(160):
    d = requests.get(f"{B}/felix/training-jobs/{jid}", headers=H, timeout=30).json()
    stt = d.get("normalized_status")
    m = d.get("metrics") or {}
    print(f"train poll {i}: {stt} F1={m.get('f1')}", flush=True)
    if d.get("is_terminal_status") or stt in ("completed","succeeded","failed","stopped","error"):
        (art/"training_120_final.json").write_text(json.dumps(redact(d), indent=2))
        print("TERMINAL:", stt, "metrics:", m, flush=True)
        break
    time.sleep(15)
