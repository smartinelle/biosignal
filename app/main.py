import os
from pathlib import Path

import streamlit as st

# Load .env before reading partner keys for the sidebar status / pipeline.
try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
except Exception:  # noqa: BLE001
    pass

from agents.pipeline import run_pipeline
try:
    from presets import PRESETS, PRESET_LABELS, PRESETS_BY_LABEL, get_note
except ModuleNotFoundError:  # package import during verification
    from app.presets import PRESETS, PRESET_LABELS, PRESETS_BY_LABEL, get_note

st.set_page_config(page_title="BioSignal Navigator", page_icon="🧬", layout="wide")


def _badge(is_live: bool) -> str:
    return "🟢 **LIVE**" if is_live else "⚪ Fallback"


_BADGE_TOKENS = {
    "live": "🟢 **LIVE**",
    "fallback": "⚪ Fallback",
    "artifact": "🧩 Deterministic artifact",
    "docs": "🔒 Submission docs",
}


def _key_present(name: str) -> bool:
    return bool(os.getenv(name))


st.title("🧬 BioSignal Navigator")
st.caption("Agent-human troubleshooting for ambiguous biotech R&D experiments.")

st.markdown(
    """
    ### From messy readouts to the next best experiment
    Biotech teams lose days when living-system experiments fail ambiguously. BioSignal Navigator turns
    observations into failure hypotheses, evidence, next measurements, and a human review question.
    """
)

with st.container(border=True):
    st.markdown("### Product shape")
    c1, c2, c3 = st.columns(3)
    c1.markdown("**Product category**  \nbiotech R&D troubleshooting")
    c2.markdown("**Demo use cases**  \npreservation, organoids, organ-on-chip")
    c3.markdown("**Core workflow**  \ninterpretation + next-measurement selection")

st.info(
    "Research workflow only — not diagnosis, treatment, viability prediction, or clinical decision support.",
    icon="🛡️",
)

with st.sidebar:
    st.header("Demo presets")
    preset = st.selectbox(
        "Case",
        PRESET_LABELS,
    )
    st.markdown("**Product:** general biotech R&D troubleshooting.")
    st.markdown("**Use cases:** assay, qPCR/ddPCR, protein, cell culture, bioprocess, preservation, organoid/OoC.")
    st.markdown("**Atira fit:** specialized agents coordinate with a human expert around uncertainty.")

    st.divider()
    st.subheader("Partner integrations")
    st.caption("The demo runs fully on deterministic fallbacks. Keys enable live partner tech.")
    st.markdown(f"- **Pioneer** — {_badge(_key_present('PIONEER_API_KEY'))} structured extractor")
    st.markdown(f"- **Gemini** — {_badge(_key_present('GEMINI_API_KEY') or _key_present('OPENROUTER_API_KEY'))}")
    st.markdown(f"- **Tavily** — {_badge(_key_present('TAVILY_API_KEY'))}")
    st.markdown("- **Aikido** — 🔒 security scan (submission docs)")

default_obs = get_note(preset)
selected_preset = PRESETS_BY_LABEL.get(preset, PRESETS[0])

observation = st.text_area("Ambiguous experiment observation", value=default_obs, height=190)
st.caption(f"Selected workflow: {selected_preset['category']}")

if st.button("Run agent workflow", type="primary"):
    result = run_pipeline(observation)

    # 0. Product context — the research loop translated into the product now.
    context = result["workflow_context"]
    with st.container(border=True):
        st.markdown("## 0. Product context")
        st.markdown(f"**Role of this case:** {context['role']}")
        st.markdown(f"**Target user:** {context['target_user']}")
        st.markdown(f"**Workflow moment:** {context['workflow_moment']}")
        st.markdown(f"**Gap:** {context['product_gap']}")
        st.caption(f"Next validation: {context['next_validation']}")

    # 1. Action plan — the product surface judges and scientists should remember.
    action_plan = result["action_plan"]
    st.subheader("1. Recommended next actions")
    st.caption("Ranked by likely impact, evidence strength, and speed to validation.")
    plan_cols = st.columns(3)
    for col, action in zip(plan_cols, action_plan["ranked_actions"]):
        with col:
            with st.container(border=True):
                st.markdown(f"### #{action['rank']} {action['title']}")
                st.markdown(f"**Impact:** `{action['impact']}` · **Effort:** `{action['effort']}` · **Confidence:** `{action['confidence']}`")
                st.markdown(f"**Goal:** {action['goal']}")
                st.markdown(f"**Expected readout:** {action['expected_readout']}")
                st.caption(f"Risk: {action['risk']}")

    with st.container(border=True):
        st.markdown("### Partner-ready summary")
        for bullet in action_plan["partner_summary"]:
            st.markdown(f"- {bullet}")
        st.markdown("### What we still do not know")
        for unknown in action_plan["what_we_do_not_know"]:
            st.markdown(f"- {unknown}")
        st.info(action_plan["human_decision"])

    # 2. Agent orchestration trace
    st.subheader("2. Agent orchestration trace")
    cols = st.columns(5)
    for col, step in zip(cols, result["trace"]):
        with col:
            st.markdown(f"**{step['agent']}**")
            st.write(step["summary"])

    # 2. Uncertainty bottleneck — the core differentiator; make it impossible to miss
    bottleneck = result["uncertainty_bottleneck"]
    with st.container(border=True):
        st.markdown("## ⚠️ The Uncertainty Bottleneck")
        st.markdown(f"### {bottleneck['headline']}")
        st.warning(bottleneck["why_it_matters"], icon="🧭")
        st.markdown(f"**Decision to unlock:** {bottleneck['decision_to_unlock']}")
        st.caption(
            "This is the product's core claim: it does not infer biological truth from surface signals — "
            "it names what cannot be known yet and the measurement that would resolve it fastest."
        )

    # 3. Synthesized troubleshooting memo (Gemini live or deterministic fallback)
    st.subheader("3. Troubleshooting memo")
    synthesis = result["synthesis"]
    st.caption(f"Memo synthesis — {_badge(synthesis['mode'] == 'live')} · {synthesis['detail']}")
    if synthesis.get("text"):
        st.markdown(synthesis["text"])

    # 4. Structured memo detail
    left, right = st.columns([1, 1])
    with left:
        st.markdown("### Structured observations")
        st.json(result["structured_observations"])
        st.markdown("### Ranked failure hypotheses")
        for idx, h in enumerate(result["hypotheses"], 1):
            st.markdown(f"{idx}. **{h['mechanism']}** — {h['rationale']}")
    with right:
        st.markdown("### Next best measurements")
        for idx, m in enumerate(result["measurements"], 1):
            st.markdown(f"{idx}. **{m['measurement']}** — {m['why']}")
        st.markdown("### Human review question")
        st.info(result["human_question"])

    # 5. Evidence and caveats
    st.markdown("### Evidence and caveats")
    for e in result["evidence"]:
        title = e["source"] + ("  ·  🟢 live (Tavily)" if e.get("live") else "")
        with st.expander(title, expanded=not e.get("live")):
            st.markdown(f"**Claim:** {e['claim']}")
            if e.get("url"):
                st.markdown(f"[source]({e['url']})")
            st.caption(f"Caveat: {e['caveat']}")

    # 6. Pioneer structured extraction artifact
    pioneer = result["pioneer_structured"]
    st.subheader("4. Pioneer structured extraction")
    pioneer_badge = _BADGE_TOKENS["live"] if pioneer["mode"] == "live" else _BADGE_TOKENS["artifact"]
    st.caption(
        f"Side-challenge artifact — {pioneer_badge} · {pioneer['detail']}  "
        "A deterministic GLiNER2-style extractor turns a messy note into typed entities, relations, and "
        "safety-boundary flags instead of an opaque LLM call."
    )

    st.markdown("**Signal → hypothesis → next-measurement triples**")
    st.dataframe(
        [
            {
                "Observation": t["observation"],
                "Possible mechanism": t["failure_hypothesis"],
                "Next measurement": t["next_measurement"],
                "Confidence": t.get("confidence"),
            }
            for t in result["pioneer_triples"]
        ],
        hide_index=True,
    )

    tri_left, tri_right = st.columns([1, 1])
    with tri_left:
        st.markdown("**Extracted observations**")
        for o in pioneer["observations"]:
            st.markdown(f"- `{o['label']}` — {o['trend']}")
        flags = pioneer["safety_flags"]
        st.markdown("**Safety-boundary flags**")
        st.markdown(f"- research workflow only: `{flags['research_workflow_only']}`")
        st.markdown(f"- needs human review: `{flags['needs_human_review']}`")
        clinical_icon = "🚫" if flags["clinical_claim_risk"] else "✅"
        st.markdown(f"- clinical-claim risk: `{flags['clinical_claim_risk']}` {clinical_icon}")
        st.markdown(f"- insufficient evidence: `{flags['insufficient_evidence']}`")
    with tri_right:
        st.markdown("**Relations (raw extractor output)**")
        st.json(pioneer["relations"])

    # 7. Partner technology trace with live/fallback status
    st.subheader("5. Partner technology trace")
    st.caption("Live vs fallback is shown honestly — the demo never hides which integrations ran.")
    for item in result["partner_trace"]:
        badge = _BADGE_TOKENS.get(item.get("badge", ""), _badge(item["live"]))
        st.markdown(f"- {badge} **{item['tool']}** — {item['role']}.")
        st.caption(f"    {item['status']}")

    # 8. Business impact
    st.subheader("6. Business impact")
    for item in result["business_impact"]:
        st.markdown(f"- {item}")
