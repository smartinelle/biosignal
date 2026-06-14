"""Lightweight SQLite store for recorded troubleshooting outcomes.

Every human-recorded result is persisted as a labeled Pioneer training row, so the
workflow accumulates a real dataset across sessions that can later fine-tune the
extractor/router. Pure standard-library (sqlite3) — no extra dependencies, and it
never raises into the UI (failures degrade to a no-op / empty list).
"""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

_DB = Path(__file__).resolve().parents[1] / "data" / "biosignal_runs.db"
_COLS = ["ts", "round", "domain", "tested_branch", "outcome", "outcome_note", "what_next", "training_row"]


def _conn() -> sqlite3.Connection:
    _DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(_DB)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT, round INTEGER, domain TEXT, tested_branch TEXT,
            outcome TEXT, outcome_note TEXT, what_next TEXT, training_row TEXT
        )"""
    )
    return conn


def record_event(round: int, domain: str, tested_branch: str, outcome: str,
                 outcome_note: str, what_next: str, training_row: dict) -> bool:
    """Persist one recorded outcome. Returns True on success, False on any error."""
    try:
        conn = _conn()
        conn.execute(
            "INSERT INTO events (ts,round,domain,tested_branch,outcome,outcome_note,what_next,training_row)"
            " VALUES (?,?,?,?,?,?,?,?)",
            (time.strftime("%Y-%m-%d %H:%M:%S"), int(round), domain, tested_branch,
             outcome, outcome_note, what_next, json.dumps(training_row)),
        )
        conn.commit()
        conn.close()
        return True
    except Exception:  # noqa: BLE001 - never break the demo on a store failure
        return False


def fetch_events(limit: int = 200) -> list[dict]:
    """Most-recent-first list of recorded events (empty list on any error)."""
    try:
        conn = _conn()
        rows = conn.execute(
            f"SELECT {','.join(_COLS)} FROM events ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        conn.close()
        return [dict(zip(_COLS, row)) for row in rows]
    except Exception:  # noqa: BLE001
        return []


def count() -> int:
    try:
        conn = _conn()
        n = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        conn.close()
        return int(n)
    except Exception:  # noqa: BLE001
        return 0


def export_jsonl(limit: int = 10000) -> str:
    """Training rows as JSONL — the format the Pioneer fine-tune pipeline consumes."""
    lines = []
    for event in fetch_events(limit):
        raw = event.get("training_row")
        if raw:
            try:
                lines.append(json.dumps(json.loads(raw)))
            except Exception:  # noqa: BLE001
                continue
    return "\n".join(lines)
