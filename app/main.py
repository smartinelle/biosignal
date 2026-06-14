"""BioSignal Navigator — guided, multi-screen troubleshooting workflow.

The app is a progressive wizard, not a single scroll. The operator always knows
the next step:

    ① Describe  →  ② Diagnose & decide  →  ③ Enter results  →  ④ Next action  ↺

Each loop is input → human-mediated decision → input → human-mediated decision.
Evidence/literature and the agent/partner machinery are supporting screens reached
from the sidebar, never the main content.
"""

import os
from pathlib import Path

import streamlit as st

# Load .env before reading partner keys (safe no-op without python-dotenv/.env).
try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
except Exception:  # noqa: BLE001
    pass

from agents.pipeline import run_pipeline
from agents.outcome_loop import apply_run_outcome

try:
    from presets import PRESETS
except ModuleNotFoundError:  # package import during verification
    from app.presets import PRESETS


st.set_page_config(page_title="BioSignal Navigator", page_icon="🧬", layout="centered")

# Ordered workflow screens (the 4-step loop) and the always-available reference screens.
STEPS = [
    ("describe", "1 · Describe"),
    ("decide", "2 · Diagnose & decide"),
    ("results", "3 · Enter results"),
    ("next", "4 · Next action"),
]
REFS = [
    ("tree", "🌳 Decision tree"),
    ("evidence", "📚 Evidence & resources"),
    ("how", "🔧 How it worked"),
]
STEP_IDS = [s[0] for s in STEPS]
LABELS = {sid: lbl for sid, lbl in STEPS + REFS}

OUTCOME_LABELS = {
    "confirmed_branch": "✅ Confirmed this explanation",
    "weakened_branch": "❌ Weakened this explanation",
    "inconclusive": "➖ Inconclusive",
    "new_anomaly_found": "⚠️ Found a new anomaly",
}


# --------------------------------------------------------------------------- #
# State helpers
# --------------------------------------------------------------------------- #
def _init_state() -> None:
    st.session_state.setdefault("screen", "describe")
    st.session_state.setdefault("result", None)
    st.session_state.setdefault("outcome", None)
    st.session_state.setdefault("chosen_branch_idx", 0)
    st.session_state.setdefault("round", 1)
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("note", "")


def go(screen: str) -> None:
    st.session_state.screen = screen


def _load_example() -> None:
    label = st.session_state.get("example_pick")
    for preset in PRESETS:
        if preset["label"] == label:
            st.session_state.note = preset["note"]
            return


def _api_keys() -> dict:
    return {
        "Pioneer": bool(os.getenv("PIONEER_API_KEY")),
        "Tavily": bool(os.getenv("TAVILY_API_KEY")),
        "Gemini": bool(os.getenv("GEMINI_API_KEY") or os.getenv("OPENROUTER_API_KEY")),
    }


def _run_analysis(note: str) -> None:
    with st.spinner("Agents working: structure → hypotheses → evidence → next measurement…"):
        st.session_state.result = run_pipeline(note)
    st.session_state.outcome = None
    st.session_state.chosen_branch_idx = 0
    st.session_state.screen = "decide"


# --------------------------------------------------------------------------- #
# Decision tree (rendered as a real graph)
# --------------------------------------------------------------------------- #
def _esc(text: str) -> str:
    return str(text).replace('"', "'").replace("\n", " ")


def _decision_dot(result: dict, chosen_idx: int, outcome: dict | None) -> str:
    branches = result["uncertainty_map"]["branches"]
    updates = (outcome or {}).get("branch_updates", [])
    signals = ", ".join(result["structured_observations"].get("signals_detected", [])[:4]) or "ambiguous readout"
    lines = [
        "digraph G {",
        'rankdir=LR; bgcolor="transparent"; pad=0.2;',
        'node [shape=box style="rounded,filled" fontname="Helvetica" fontsize=10 color="#cbd5e1" fillcolor="#ffffff"];',
        'edge [color="#94a3b8"];',
        f'root [label="Observation\\n{_esc(signals)}" fillcolor="#e8eefc" color="#6b8afd"];',
    ]
    for i, b in enumerate(branches):
        upd = updates[i] if i < len(updates) else {}
        conf = upd.get("new_confidence")
        status = upd.get("status")
        fill, border = "#ffffff", "#cbd5e1"
        if i == chosen_idx:
            fill, border = "#e8eefc", "#6b8afd"
        if status == "reinforced":
            fill, border = "#e7f6ec", "#3fa95b"
        elif status == "weakened":
            fill, border = "#fdeaea", "#d64545"
        label = _esc(b["hypothesis"])
        if conf is not None:
            label += f"\\nconfidence {conf}"
        lines.append(f'b{i} [label="{label}" fillcolor="{fill}" color="{border}"];')
        lines.append(f'b{i}_t [label="Test\\n{_esc(b["test"])}" shape=note fillcolor="#fafafa"];')
        lines.append(f"root -> b{i};")
        lines.append(f"b{i} -> b{i}_t;")
    lines.append("}")
    return "\n".join(lines)


def _render_tree(result: dict) -> None:
    dot = _decision_dot(result, st.session_state.chosen_branch_idx, st.session_state.outcome)
    try:
        st.graphviz_chart(dot, use_container_width=True)
    except Exception:  # noqa: BLE001 - never break the page on a render issue
        for i, b in enumerate(result["uncertainty_map"]["branches"]):
            st.markdown(f"- **{b['hypothesis']}** → _test:_ {b['test']}")


# --------------------------------------------------------------------------- #
# Sidebar — navigation + status
# --------------------------------------------------------------------------- #
def _sidebar() -> None:
    has_result = st.session_state.result is not None
    cur = st.session_state.screen
    with st.sidebar:
        st.markdown("## 🧬 BioSignal")
        if has_result:
            step_n = (STEP_IDS.index(cur) + 1) if cur in STEP_IDS else "—"
            st.caption(f"Investigation round {st.session_state.round} · step {step_n} of 4")
        st.markdown("**Workflow**")
        for sid, label in STEPS:
            disabled = (sid != "describe") and not has_result
            st.button(
                label, key=f"nav_{sid}", on_click=go, args=(sid,),
                use_container_width=True,
                type="primary" if cur == sid else "secondary",
                disabled=disabled,
            )
        st.markdown("**Reference**")
        for sid, label in REFS:
            st.button(
                label, key=f"nav_{sid}", on_click=go, args=(sid,),
                use_container_width=True,
                type="primary" if cur == sid else "secondary",
                disabled=not has_result,
            )
        st.divider()
        keys = _api_keys()
        st.caption("Live integrations")
        st.caption(" · ".join(f"{'🟢' if v else '⚪'} {k}" for k, v in keys.items()))
        if not any(keys.values()):
            st.caption("Offline demo mode (curated data + real references).")
        st.divider()
        st.caption("Research troubleshooting only — not diagnosis, treatment, or clinical decision support. Human review required.")


def _breadcrumb() -> None:
    cur = st.session_state.screen
    parts = []
    for i, (sid, label) in enumerate(STEPS):
        name = label.split(" · ")[1]
        if sid == cur:
            parts.append(f"**{i + 1}·{name}**")
        else:
            parts.append(f"{i + 1}·{name}")
    st.caption("  ›  ".join(parts))


# --------------------------------------------------------------------------- #
# Screens
# --------------------------------------------------------------------------- #
def screen_describe() -> None:
    _breadcrumb()
    st.subheader("Describe your experiment")
    with st.container(border=True):
        st.caption("Plain lab language — what ran, what looked off, what changed recently, and the decision you're stuck on.")
        st.pills(
            "Load an example",
            options=[p["label"] for p in PRESETS],
            selection_mode="single",
            key="example_pick",
            on_change=_load_example,
            help="Click to load a ready-made case, then edit it or run as-is.",
        )
        st.text_area(
            "Experiment note", key="note", height=170, label_visibility="collapsed",
            placeholder=(
                "e.g. Potency assay signal dropped ~40% after a reagent-lot change. "
                "Positive control drifted, edge wells look worse, cell count is normal. "
                "Decide whether it's biology, protocol drift, reagent failure, or a plate artifact."
            ),
        )
        st.caption("💡 Tip: include anything that changed recently — reagent lot, operator, media, temperature, or timing.")
    if st.button("Analyze experiment  →", type="primary", use_container_width=True):
        if not st.session_state.note.strip():
            st.warning("Add a short experiment note first (or load an example).")
        else:
            st.session_state.round = 1
            st.session_state.history = []
            _run_analysis(st.session_state.note)
            st.rerun()


def screen_decide() -> None:
    result = st.session_state.result
    if result is None:
        st.info("Start by describing an experiment.")
        st.button("← Go to step 1", on_click=go, args=("describe",))
        return

    _breadcrumb()
    st.subheader("Diagnose & decide")

    actions = result["action_plan"]["ranked_actions"]
    branches = result["uncertainty_map"]["branches"]
    top = actions[0] if actions else {}
    if top:
        st.success(f"**Recommended next measurement:** {top['title']}\n\n{top.get('goal','')}", icon="🎯")

    st.markdown("**Decision tree** — which explanation is worth testing next?")
    _render_tree(result)

    st.markdown("**Your decision:** pick the explanation you'll test next.")
    idx = st.radio(
        "Explanation to test",
        options=list(range(len(branches))),
        index=min(st.session_state.chosen_branch_idx, max(0, len(branches) - 1)),
        format_func=lambda i: branches[i]["hypothesis"],
        label_visibility="collapsed",
    )
    st.session_state.chosen_branch_idx = idx
    b = branches[idx]
    with st.container(border=True):
        st.markdown(f"**Test:** {b['test']}")
        st.caption(f"Why plausible: {b['why_plausible']}")
        st.caption(f"What would change our mind: {b['what_would_change_our_mind']}")

    c1, c2 = st.columns(2)
    c1.button("← Back", on_click=go, args=("describe",), use_container_width=True)
    c2.button("I ran this measurement  →", type="primary", on_click=go, args=("results",), use_container_width=True)


def screen_results() -> None:
    result = st.session_state.result
    if result is None:
        st.info("Start by describing an experiment.")
        st.button("← Go to step 1", on_click=go, args=("describe",))
        return

    _breadcrumb()
    st.subheader("Enter the measurement result")
    branches = result["uncertainty_map"]["branches"]
    b = branches[st.session_state.chosen_branch_idx]
    st.info(f"You chose to test **{b['hypothesis']}** via **{b['test']}**.")

    outcome_key = st.radio(
        "What did the measurement show?",
        options=list(OUTCOME_LABELS.keys()),
        format_func=lambda k: OUTCOME_LABELS[k],
    )
    note = st.text_input("Notes (optional)", placeholder="e.g. old reagent lot rescued the signal")

    c1, c2 = st.columns(2)
    c1.button("← Back", on_click=go, args=("decide",), use_container_width=True)
    if c2.button("Record result  →", type="primary", use_container_width=True):
        st.session_state.outcome = apply_run_outcome(
            result["action_plan"], result["uncertainty_map"], result["pioneer_structured"],
            outcome_key, selected_branch_index=st.session_state.chosen_branch_idx, note=note,
        )
        st.session_state.outcome["note"] = note
        st.session_state.outcome["tested_branch"] = b["hypothesis"]
        st.session_state.screen = "next"
        st.rerun()


def screen_next() -> None:
    result = st.session_state.result
    outcome = st.session_state.outcome
    if result is None or outcome is None:
        st.info("Run an analysis and record a result first.")
        st.button("← Go to step 1", on_click=go, args=("describe",))
        return

    _breadcrumb()
    st.subheader("Next action")
    st.success(f"**What to do next:** {outcome['what_next']}", icon="➡️")
    st.caption(outcome["summary"])

    st.markdown("**Updated decision tree** (confidence shifted by your result)")
    _render_tree(result)

    with st.expander("Branch confidence updates"):
        st.dataframe(
            [
                {"Explanation": u["branch"], "Status": u["status"],
                 "Δ": u["delta"], "New confidence": u["new_confidence"]}
                for u in outcome["branch_updates"]
            ],
            hide_index=True, use_container_width=True,
        )

    st.divider()
    st.markdown("**Continue the investigation**")
    c1, c2 = st.columns(2)
    if c1.button("Plan next measurement  ↺", type="primary", use_container_width=True):
        # Record this round, then re-analyze with the new result folded in.
        st.session_state.history.append({
            "round": st.session_state.round,
            "tested": outcome.get("tested_branch"),
            "outcome": OUTCOME_LABELS.get(outcome["outcome"], outcome["outcome"]),
            "note": outcome.get("note", ""),
            "what_next": outcome["what_next"],
        })
        augmented = (
            f"{st.session_state.note}\n\n"
            f"Update (round {st.session_state.round}): ran '{outcome.get('tested_branch')}' check. "
            f"Outcome: {OUTCOME_LABELS.get(outcome['outcome'], outcome['outcome'])}. {outcome.get('note','')}"
        )
        st.session_state.note = augmented
        st.session_state.round += 1
        _run_analysis(augmented)
        st.rerun()
    if c2.button("Start new investigation", use_container_width=True):
        for k in ("result", "outcome", "history"):
            st.session_state[k] = None if k != "history" else []
        st.session_state.round = 1
        st.session_state.note = ""
        st.session_state.screen = "describe"
        st.rerun()


def screen_tree() -> None:
    result = st.session_state.result
    if result is None:
        st.info("Run an analysis first.")
        st.button("← Go to step 1", on_click=go, args=("describe",))
        return
    st.subheader("🌳 Decision tree")
    st.caption("BioSignal Navigator preserves uncertainty as a decision graph instead of collapsing it into one answer.")
    _render_tree(result)
    st.markdown("**Branches**")
    for b in result["uncertainty_map"]["branches"]:
        with st.container(border=True):
            st.markdown(f"**{b['hypothesis']}**")
            st.caption(f"Test: {b['test']} · {b['what_would_change_our_mind']}")
    if st.session_state.history:
        st.markdown("**Investigation log**")
        st.dataframe(
            [
                {"Round": h["round"], "Tested": h["tested"], "Outcome": h["outcome"], "Then": h["what_next"]}
                for h in st.session_state.history
            ],
            hide_index=True, use_container_width=True,
        )
    st.button("← Back to workflow", on_click=go, args=("decide",))


def screen_evidence() -> None:
    result = st.session_state.result
    if result is None:
        st.info("Run an analysis first.")
        st.button("← Go to step 1", on_click=go, args=("describe",))
        return
    st.subheader("📚 Evidence & resources")
    st.caption("Supporting literature for your decision — not the answer. Treat as leads to verify.")
    tavily_live = result["integration_status"]["tavily"].get("mode") == "live"
    st.caption(f"Source: {'🟢 live web search via Tavily + curated references' if tavily_live else 'curated reference library'}")
    for e in result.get("evidence", []):
        with st.container(border=True):
            head = e["source"] + ("  ·  🟢 live (Tavily)" if e.get("live") else "")
            st.markdown(f"**{head}**")
            st.write(e["claim"])
            meta = f"`{e.get('evidence_type', '—')}` · strength `{e.get('strength', '?')}/5`"
            if e.get("source_tier"):
                meta += f" · {e['source_tier']}"
            if e.get("relevance_score") is not None:
                meta += f" · Tavily score `{e['relevance_score']}`"
            st.caption(meta)
            if e.get("url"):
                st.markdown(f"[Open source ↗]({e['url']})")
            st.caption(f"⚠️ {e['caveat']}")

    st.markdown("### Troubleshooting memo")
    memo = result["synthesis"]
    gemini_live = memo.get("mode") == "live"
    st.caption(f"{'🟢 synthesized live by Gemini' if gemini_live else '⚪ deterministic memo (no Gemini key set)'} · {memo.get('detail','')}")
    if memo.get("text"):
        with st.container(border=True):
            st.markdown(memo["text"])
    st.button("← Back to workflow", on_click=go, args=("decide",))


def screen_how() -> None:
    result = st.session_state.result
    if result is None:
        st.info("Run an analysis first.")
        st.button("← Go to step 1", on_click=go, args=("describe",))
        return
    st.subheader("🔧 How it worked")
    st.markdown("**Agent pipeline**")
    for step in result.get("trace", []):
        st.markdown(f"- **{step['agent']}** — {step['summary']}")
    st.markdown("**Partner technologies**")
    badge_map = {"live": "🟢 LIVE", "artifact": "🧩 deterministic", "fallback": "⚪ fallback", "docs": "🔒 docs"}
    for item in result.get("partner_trace", []):
        badge = badge_map.get(item.get("badge", ""), "🟢 LIVE" if item.get("live") else "⚪ fallback")
        st.markdown(f"- {badge} · **{item['tool']}** — {item['role']}")
    st.markdown("**Pioneer — structured extraction**")
    triples = result.get("pioneer_triples", [])
    if triples:
        st.dataframe(
            [
                {"Observation": t["observation"], "Possible mechanism": t["failure_hypothesis"],
                 "Next measurement": t["next_measurement"], "Confidence": t.get("confidence")}
                for t in triples
            ],
            hide_index=True, use_container_width=True,
        )
    st.button("← Back to workflow", on_click=go, args=("decide",))


# --------------------------------------------------------------------------- #
# Router
# --------------------------------------------------------------------------- #
_init_state()
_sidebar()

st.title("BioSignal Navigator")

ROUTES = {
    "describe": screen_describe,
    "decide": screen_decide,
    "results": screen_results,
    "next": screen_next,
    "tree": screen_tree,
    "evidence": screen_evidence,
    "how": screen_how,
}
ROUTES.get(st.session_state.screen, screen_describe)()
