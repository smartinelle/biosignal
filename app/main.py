"""BioSignal Navigator — clean operator UI.

A single, linear flow: describe an ambiguous experiment → get the next measurement
to run, the likely explanations, evidence with references, and a caveated memo. The
agent pipeline and partner-API machinery are tucked into one "How it worked" panel so
a first-time scientist sees the answer, not the plumbing.
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

try:
    from presets import PRESETS
except ModuleNotFoundError:  # package import during verification
    from app.presets import PRESETS


st.set_page_config(page_title="BioSignal Navigator", page_icon="🧬", layout="centered")


def _api_keys() -> dict:
    return {
        "gemini": bool(os.getenv("GEMINI_API_KEY") or os.getenv("OPENROUTER_API_KEY")),
        "tavily": bool(os.getenv("TAVILY_API_KEY")),
        "pioneer": bool(os.getenv("PIONEER_API_KEY")),
    }


def _load_example() -> None:
    label = st.session_state.get("example_pick")
    for preset in PRESETS:
        if preset["label"] == label:
            st.session_state.note = preset["note"]
            return


# --------------------------------------------------------------------------- #
# Sidebar — live API status (the "where are the APIs used" answer at a glance)
# --------------------------------------------------------------------------- #
keys = _api_keys()
with st.sidebar:
    st.markdown("### Live integrations")
    st.markdown(f"{'🟢' if keys['pioneer'] else '⚪'} **Pioneer** — structured extraction")
    st.markdown(f"{'🟢' if keys['tavily'] else '⚪'} **Tavily** — evidence & references")
    st.markdown(f"{'🟢' if keys['gemini'] else '⚪'} **Gemini** — memo synthesis")
    st.markdown("🔒 **Aikido** — repo security scan")
    if not any(keys.values()):
        st.info("No API keys set — running in offline demo mode with curated data and real references. Add keys to `.env` for live mode.")
    else:
        st.caption("🟢 = a live API runs on Analyze. ⚪ = curated fallback.")
    st.divider()
    st.caption(
        "Research troubleshooting only — not diagnosis, treatment, viability prediction, "
        "or clinical decision support. A senior scientist reviews every result."
    )


# --------------------------------------------------------------------------- #
# Header
# --------------------------------------------------------------------------- #
st.title("🧬 BioSignal Navigator")
st.markdown("#### Turn an ambiguous experiment into the next measurement worth running.")
st.caption(
    "Paste a messy lab note. The agents structure it, propose possible mechanisms, "
    "pull evidence, and name the single measurement that best reduces uncertainty — "
    "then hand the judgment call to you."
)


# --------------------------------------------------------------------------- #
# 1 · Input
# --------------------------------------------------------------------------- #
with st.container(border=True):
    st.markdown("##### 1 · Describe your experiment")
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
        "Experiment note",
        key="note",
        height=170,
        label_visibility="collapsed",
        placeholder=(
            "e.g. Potency assay signal dropped ~40% after a reagent-lot change. "
            "Positive control drifted, edge wells look worse, cell count is normal. "
            "Decide whether it's biology, protocol drift, reagent failure, or a plate "
            "artifact before repeating the study."
        ),
    )
    st.caption("💡 Tip: include anything that changed recently — reagent lot, operator, media, temperature, or timing.")
    analyze = st.button("Analyze experiment  →", type="primary", use_container_width=True)

if analyze and st.session_state.note.strip():
    with st.spinner("Agents working: structure → hypotheses → evidence → next measurement…"):
        st.session_state.result = run_pipeline(st.session_state.note)
elif analyze:
    st.warning("Add a short experiment note first (or load an example above).")


# --------------------------------------------------------------------------- #
# 2 · Result
# --------------------------------------------------------------------------- #
result = st.session_state.get("result")
if result:
    gemini_live = result["synthesis"].get("mode") == "live"
    tavily_live = result["integration_status"]["tavily"].get("mode") == "live"
    pioneer_live = result["pioneer_structured"].get("mode") == "live"

    st.divider()

    # --- The answer: next best measurement ---
    st.markdown("##### 2 · Run this next")
    measurements = result.get("measurements", [])
    if measurements:
        top = measurements[0]
        st.success(f"**{top['measurement']}**\n\n{top['why']}", icon="🎯")
        if len(measurements) > 1:
            with st.container(border=True):
                st.markdown("**Other discriminating measurements**")
                for m in measurements[1:4]:
                    st.markdown(f"- **{m['measurement']}** — {m['why']}")

    # --- Why: likely explanations ---
    st.markdown("##### 3 · Why — the likely explanations")
    st.caption("Possible mechanisms consistent with your readouts. Ranked by plausibility, not confirmed.")
    for i, h in enumerate(result.get("hypotheses", [])[:3], 1):
        with st.container(border=True):
            st.markdown(f"**{i}. {h['mechanism']}**")
            st.write(h["rationale"])

    # --- What needs a human ---
    st.markdown("##### 4 · What needs a human")
    st.warning(result["human_question"], icon="⚠️")

    # --- Evidence with references ---
    st.markdown("##### 5 · Evidence & references")
    ev_src = "🟢 live web search via **Tavily** + curated references" if tavily_live else "curated reference library"
    st.caption(f"Source: {ev_src}. Treat as leads to verify, not proof.")
    for e in result.get("evidence", []):
        with st.container(border=True):
            head = e["source"] + ("  ·  🟢 live (Tavily)" if e.get("live") else "")
            st.markdown(f"**{head}**")
            st.write(e["claim"])
            meta = (
                f"`{e.get('evidence_type', '—')}` · relevance `{e.get('relevance', '—')}` "
                f"· strength `{e.get('strength', '?')}/5`"
            )
            if e.get("source_tier"):
                meta += f" · {e['source_tier']}"
            if e.get("relevance_score") is not None:
                meta += f" · Tavily score `{e['relevance_score']}`"
            st.caption(meta)
            if e.get("url"):
                st.markdown(f"[Open source ↗]({e['url']})")
            st.caption(f"⚠️ {e['caveat']}")

    # --- Memo (Gemini) ---
    st.markdown("##### 6 · Troubleshooting memo")
    memo = result["synthesis"]
    memo_src = "🟢 synthesized live by **Gemini**" if gemini_live else "⚪ deterministic memo (no Gemini key set)"
    st.caption(f"{memo_src} · {memo.get('detail', '')}")
    if memo.get("text"):
        with st.container(border=True):
            st.markdown(memo["text"])

    # --- How it worked (agents + partner APIs + Pioneer extraction) ---
    st.divider()
    with st.expander("🔧 How it worked — agents, partner APIs & structured extraction"):
        st.markdown("**Agent pipeline**")
        for step in result.get("trace", []):
            st.markdown(f"- **{step['agent']}** — {step['summary']}")

        st.markdown("---")
        st.markdown("**Partner technologies** (live vs fallback, shown honestly)")
        badge_map = {"live": "🟢 LIVE", "artifact": "🧩 deterministic", "fallback": "⚪ fallback", "docs": "🔒 docs"}
        for item in result.get("partner_trace", []):
            badge = badge_map.get(item.get("badge", ""), "🟢 LIVE" if item.get("live") else "⚪ fallback")
            st.markdown(f"- {badge} · **{item['tool']}** — {item['role']}")
            if item.get("status"):
                st.caption(item["status"])

        st.markdown("---")
        st.markdown("**Pioneer — structured extraction** (signal → possible mechanism → next measurement)")
        triples = result.get("pioneer_triples", [])
        if triples:
            st.dataframe(
                [
                    {
                        "Observation": t["observation"],
                        "Possible mechanism": t["failure_hypothesis"],
                        "Next measurement": t["next_measurement"],
                        "Confidence": t.get("confidence"),
                    }
                    for t in triples
                ],
                hide_index=True,
                use_container_width=True,
            )
        flags = result["pioneer_structured"].get("safety_flags", {})
        if flags:
            st.caption(
                f"Safety flags — research-only: `{flags.get('research_workflow_only')}` · "
                f"needs human review: `{flags.get('needs_human_review')}` · "
                f"clinical-claim risk: `{flags.get('clinical_claim_risk')}`"
            )
else:
    st.caption("Load an example or paste a note, then press **Analyze** to see the result.")
