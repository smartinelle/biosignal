"""BioSignal Navigator — guided decision-tree investigation.

The agents generate a full multi-node decision tree upfront for the chosen
workflow (ex-vivo tissue preservation). The operator advances it by recording the
outcome of each discriminating measurement; the tree updates live and narrows —
through multiple branching decision nodes — until it reaches a concrete resolution.

    Setup  →  Investigate (decision node → record outcome → next node …)  →  Resolution

Evidence/literature is shown inline at each decision and aggregated on a reference
screen; the agent/partner machinery lives on the "How it worked" screen.
"""

import os
from pathlib import Path

import streamlit as st

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
except Exception:  # noqa: BLE001
    pass

from agents.pipeline import run_pipeline

try:
    import store
    from presets import PRESETS
    from decision_tree import get_workflow, is_terminal, build_dynamic_tree
except ModuleNotFoundError:  # package import during verification
    from app import store
    from app.presets import PRESETS
    from app.decision_tree import get_workflow, is_terminal, build_dynamic_tree


st.set_page_config(page_title="BioSignal Navigator", page_icon="🧬", layout="centered")

STEPS = [("describe", "1 · Setup"), ("investigate", "2 · Investigate")]
REFS = [
    ("tree", "🌳 Decision tree"),
    ("evidence", "📚 Evidence & resources"),
    ("dataset", "🗄️ Training data"),
    ("how", "🔧 How it worked"),
]


# --------------------------------------------------------------------------- #
# State
# --------------------------------------------------------------------------- #
def _init_state() -> None:
    st.session_state.setdefault("screen", "describe")
    st.session_state.setdefault("result", None)   # pipeline output (live partner evidence/memo)
    st.session_state.setdefault("tree", None)
    st.session_state.setdefault("current_node", None)
    st.session_state.setdefault("path", [])        # [{node, key, edge, question, label}]
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


def _begin(tree: dict, result: dict) -> None:
    st.session_state.result = result
    st.session_state.tree = tree
    st.session_state.current_node = tree["root"]
    st.session_state.path = []
    st.session_state.screen = "investigate"


def _decide(tree: dict, current: str, node: dict, opt: dict) -> None:
    nxt = tree["nodes"][opt["next"]]
    what_next = nxt["resolution"]["headline"] if is_terminal(nxt) else nxt["question"]
    training_row = {
        "input": {"workflow": tree["title"], "node": node["question"], "measurement": node["test"]},
        "labels": {"decision": opt["key"], "outcome": opt["label"], "next": what_next, "human_review_required": True},
    }
    store.record_event(
        round=len(st.session_state.path) + 1,
        domain=tree["id"],
        tested_branch=node["question"],
        outcome=opt["key"],
        outcome_note=opt["label"],
        what_next=what_next,
        training_row=training_row,
    )
    st.session_state.path.append({
        "node": current, "key": opt["key"], "edge": opt["edge"],
        "question": node["question"], "label": opt["label"],
    })
    st.session_state.current_node = opt["next"]


# --------------------------------------------------------------------------- #
# Decision tree rendering
# --------------------------------------------------------------------------- #
def _short(text: str, n: int) -> str:
    text = str(text)
    return text if len(text) <= n else text[: n - 1] + "…"


def _wrap(text: str, width: int = 22) -> str:
    """Word-wrap into graphviz \\n-joined lines so labels are never clipped."""
    words = str(text).replace('"', "'").split()
    lines, cur = [], ""
    for w in words:
        if cur and len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return "\\n".join(lines)


def _tree_dot(tree: dict, current: str, chosen: dict) -> str:
    nodes = tree["nodes"]
    visited = set(chosen.keys())
    lines = [
        "digraph G {",
        'rankdir=LR; bgcolor="transparent"; pad=0.25; nodesep=0.35; ranksep=0.6;',
        'node [shape=box style="rounded,filled" fontname="Helvetica" fontsize=10 width=2 color="#cbd5e1" fillcolor="#ffffff"];',
        'edge [color="#cbd5e1" fontname="Helvetica" fontsize=9 fontcolor="#475569"];',
    ]
    for nid, node in nodes.items():
        terminal = is_terminal(node)
        label = node["resolution"]["headline"] if terminal else node["question"]
        fill, border = "#ffffff", "#cbd5e1"
        if nid in visited:
            fill, border = "#e7f6ec", "#3fa95b"
        if nid == current:
            fill, border = (("#e7f6ec", "#3fa95b") if terminal else ("#e8eefc", "#6b8afd"))
        shape = "note" if terminal else "box"
        lines.append(f'{nid} [label="{_wrap(label, 26)}" shape={shape} fillcolor="{fill}" color="{border}"];')
    for nid, node in nodes.items():
        for opt in node.get("options", []):
            on_path = chosen.get(nid) == opt["key"]
            color = "#3fa95b" if on_path else "#cbd5e1"
            penwidth = "2" if on_path else "1"
            lines.append(
                f'{nid} -> {opt["next"]} [label="{_wrap(opt["edge"], 16)}" color="{color}" penwidth={penwidth}];'
            )
    lines.append("}")
    return "\n".join(lines)


def _render_tree() -> None:
    tree = st.session_state.tree
    chosen = {p["node"]: p["key"] for p in st.session_state.path}
    dot = _tree_dot(tree, st.session_state.current_node, chosen)
    try:
        st.graphviz_chart(dot, use_container_width=True)
    except Exception:  # noqa: BLE001
        st.markdown("\n".join(f"- {n.get('question', n.get('resolution', {}).get('headline',''))}"
                              for n in tree["nodes"].values()))


# --------------------------------------------------------------------------- #
# Sidebar
# --------------------------------------------------------------------------- #
def _sidebar() -> None:
    started = st.session_state.tree is not None
    cur = st.session_state.screen
    with st.sidebar:
        st.markdown("## 🧬 BioSignal")
        if started:
            done = len(st.session_state.path)
            node = st.session_state.tree["nodes"][st.session_state.current_node]
            status = "resolved ✅" if is_terminal(node) else "in progress"
            st.caption(f"Decisions recorded: {done} · {status}")
        st.markdown("**Workflow**")
        for sid, label in STEPS:
            disabled = (sid == "investigate") and not started
            st.button(label, key=f"nav_{sid}", on_click=go, args=(sid,), use_container_width=True,
                      type="primary" if cur == sid else "secondary", disabled=disabled)
        st.markdown("**Reference**")
        for sid, label in REFS:
            st.button(label, key=f"nav_{sid}", on_click=go, args=(sid,), use_container_width=True,
                      type="primary" if cur == sid else "secondary", disabled=not started)
        st.divider()
        keys = _api_keys()
        st.caption("Live integrations")
        st.caption(" · ".join(f"{'🟢' if v else '⚪'} {k}" for k, v in keys.items()))
        st.divider()
        st.caption("Research troubleshooting only — not diagnosis, treatment, or clinical decision support. Human review required.")


def _papers(evidence: list[dict]) -> None:
    if not evidence:
        return
    st.markdown("📚 **Why this measurement — supporting papers**")
    for e in evidence:
        link = f" — [open ↗]({e['url']})" if e.get("url") else ""
        st.markdown(f"- 📄 **{e['source']}**{link}")
        if e.get("why"):
            st.caption(f"↳ {e['why']}")


# --------------------------------------------------------------------------- #
# Screens
# --------------------------------------------------------------------------- #
def screen_describe() -> None:
    st.subheader("Start an investigation")
    st.caption(
        "The agents generate a decision tree upfront, then you advance it by recording the outcome "
        "of each measurement until it reaches a resolution."
    )
    mode = st.radio("Input", ["Demo workflow", "Custom query"], horizontal=True, label_visibility="collapsed")

    if mode == "Demo workflow":
        wf = get_workflow("tissue_preservation")
        with st.container(border=True):
            st.markdown(f"### {wf['title']}")
            st.write(wf["context"])
            st.caption("Curated demo workflow — a hand-built investigation to show the full flow end to end.")
        if st.button("▶ Generate investigation plan & start", type="primary", use_container_width=True):
            with st.spinner("Agents generating the decision tree and pulling supporting evidence…"):
                result = run_pipeline(wf["context"])
            _begin(wf, result)
            st.rerun()
    else:
        with st.container(border=True):
            st.caption("Describe any experiment — the tree is generated from the agent pipeline. Plain lab language; load an example or write your own.")
            st.pills(
                "Load an example", options=[p["label"] for p in PRESETS], selection_mode="single",
                key="example_pick", on_change=_load_example,
            )
            st.text_area(
                "Experiment note", key="note", height=150, label_visibility="collapsed",
                placeholder="e.g. qPCR run: Ct ~3 cycles late, melt-curve shoulder, NTC weak amplification, borderline RNA integrity, new operator.",
            )
        if st.button("▶ Generate investigation from this note", type="primary", use_container_width=True):
            if not st.session_state.note.strip():
                st.warning("Add a note or load an example first.")
            else:
                with st.spinner("Agents structuring the note and generating the decision tree…"):
                    result = run_pipeline(st.session_state.note)
                    tree = build_dynamic_tree(result)
                _begin(tree, result)
                st.rerun()


def screen_investigate() -> None:
    tree = st.session_state.tree
    if tree is None:
        st.info("Start an investigation first.")
        st.button("← Go to Setup", on_click=go, args=("describe",))
        return

    current = st.session_state.current_node
    node = tree["nodes"][current]
    st.subheader(tree["title"])
    done = len(st.session_state.path)
    st.caption(f"Decision {done + (0 if is_terminal(node) else 1)} · {done} recorded · "
               f"{'resolved ✅' if is_terminal(node) else 'in progress'}")

    _render_tree()

    if is_terminal(node):
        res = node["resolution"]
        st.success(f"🏁 **{res['headline']}**")
        with st.container(border=True):
            st.markdown(f"**Leading mechanism:** {res['leading_mechanism']}")
            st.markdown(f"**Confirmatory assay:** {res['confirmatory_assay']}")
            if res.get("molecular_targets"):
                st.markdown("**Molecular targets to verify:** " + ", ".join(res["molecular_targets"]))
            st.warning(f"🧑‍🔬 Human review: {res['human_review']}", icon="⚠️")
        c1, c2 = st.columns(2)
        if st.session_state.path:
            if c1.button("↩ Revise last decision", use_container_width=True):
                last = st.session_state.path.pop()
                st.session_state.current_node = last["node"]
                st.rerun()
        if c2.button("Start new investigation", use_container_width=True):
            st.session_state.path = []
            st.session_state.current_node = tree["root"]
            st.rerun()
        return

    # Active decision node
    st.markdown(f"### ❓ {node['question']}")
    with st.container(border=True):
        st.markdown("**① Run this measurement**")
        st.markdown(node["test"])
        if node.get("rationale"):
            st.caption(f"Why this discriminates: {node['rationale']}")
        _papers(node.get("evidence", []))

    st.markdown("**② Report what the measurement showed** — click the result you observed; the tree advances accordingly:")
    for opt in node["options"]:
        if st.button(opt["label"], key=f"opt_{current}_{opt['key']}", type="secondary", use_container_width=True):
            _decide(tree, current, node, opt)
            st.rerun()
        if opt.get("desc"):
            st.caption(opt["desc"])
    if st.session_state.path:
        st.divider()
        if st.button("↩ Revise last decision"):
            last = st.session_state.path.pop()
            st.session_state.current_node = last["node"]
            st.rerun()


def screen_tree() -> None:
    if st.session_state.tree is None:
        st.info("Start an investigation first.")
        st.button("← Go to Setup", on_click=go, args=("describe",))
        return
    st.subheader("🌳 Decision tree")
    st.caption("Generated upfront, updated live. BioSignal Navigator preserves uncertainty as a branching decision graph instead of collapsing it into one answer.")
    _render_tree()
    if st.session_state.path:
        st.markdown("**Investigation log**")
        st.dataframe(
            [
                {"#": i + 1, "Decision": p["question"], "Outcome recorded": p["label"]}
                for i, p in enumerate(st.session_state.path)
            ],
            hide_index=True, use_container_width=True,
        )
    st.button("← Back to investigation", on_click=go, args=("investigate",))


def screen_evidence() -> None:
    result = st.session_state.result
    st.subheader("📚 Evidence & resources")
    st.caption("Supporting literature for the workflow — leads to verify, not the answer.")
    if result is None:
        st.info("Start an investigation first.")
        return
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
    memo = result["synthesis"]
    st.markdown("### Troubleshooting memo")
    st.caption(f"{'🟢 synthesized live by Gemini' if memo.get('mode') == 'live' else '⚪ deterministic memo'} · {memo.get('detail','')}")
    if memo.get("text"):
        with st.container(border=True):
            st.markdown(memo["text"])


def screen_dataset() -> None:
    st.subheader("🗄️ Training data")
    st.caption(
        "Every recorded decision is persisted as a labeled Pioneer training row — the workflow "
        "accumulates a real dataset that can fine-tune the extractor/router over time."
    )
    events = store.fetch_events()
    st.metric("Recorded training examples", store.count())
    if not events:
        st.info("No recorded decisions yet. Record an outcome in the investigation to add the first example.")
        return
    st.dataframe(
        [
            {"When": e["ts"], "#": e["round"], "Workflow": e["domain"],
             "Decision": _short(e["tested_branch"], 60), "Outcome": e["outcome_note"]}
            for e in events
        ],
        hide_index=True, use_container_width=True,
    )
    st.download_button(
        "⬇️ Export dataset (JSONL for fine-tuning)",
        data=store.export_jsonl(), file_name="biosignal_training.jsonl",
        mime="application/jsonl", use_container_width=True,
    )
    with st.expander("Preview a training row"):
        import json as _json
        st.json(_json.loads(events[0]["training_row"]) if events[0].get("training_row") else {})


def screen_how() -> None:
    result = st.session_state.result
    st.subheader("🔧 How it worked")
    st.caption("The decision tree is generated upfront and updated live; partner technologies power extraction, evidence, and synthesis.")
    if result is None:
        st.info("Start an investigation first.")
        return
    st.markdown("**Agent pipeline**")
    for step in result.get("trace", []):
        st.markdown(f"- **{step['agent']}** — {step['summary']}")
    st.markdown("**Partner technologies**")
    badge_map = {"live": "🟢 LIVE", "artifact": "🧩 deterministic", "fallback": "⚪ fallback", "docs": "🔒 docs"}
    for item in result.get("partner_trace", []):
        badge = badge_map.get(item.get("badge", ""), "🟢 LIVE" if item.get("live") else "⚪ fallback")
        st.markdown(f"- {badge} · **{item['tool']}** — {item['role']}")
    triples = result.get("pioneer_triples", [])
    if triples:
        st.markdown("**Pioneer — structured extraction**")
        st.dataframe(
            [
                {"Observation": t["observation"], "Possible mechanism": t["failure_hypothesis"],
                 "Next measurement": t["next_measurement"], "Confidence": t.get("confidence")}
                for t in triples
            ],
            hide_index=True, use_container_width=True,
        )


# --------------------------------------------------------------------------- #
# Router
# --------------------------------------------------------------------------- #
_init_state()
_sidebar()
st.title("BioSignal Navigator")

ROUTES = {
    "describe": screen_describe,
    "investigate": screen_investigate,
    "tree": screen_tree,
    "evidence": screen_evidence,
    "dataset": screen_dataset,
    "how": screen_how,
}
ROUTES.get(st.session_state.screen, screen_describe)()
