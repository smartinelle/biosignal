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

st.set_page_config(page_title="BioSignal Navigator", page_icon="🧬", layout="wide")


def _badge(is_live: bool) -> str:
    return "🟢 **LIVE**" if is_live else "⚪ Fallback"


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

st.info(
    "Research workflow only — not diagnosis, treatment, viability prediction, or clinical decision support.",
    icon="🛡️",
)

with st.sidebar:
    st.header("Demo presets")
    preset = st.selectbox(
        "Case",
        [
            "Living tissue preservation failure",
            "Organoid QC anomaly",
            "Organ-on-chip drug response anomaly",
        ],
    )
    st.markdown("**Wedge:** biotech experiment troubleshooting, demonstrated on living tissue systems.")
    st.markdown("**Atira fit:** specialized agents coordinate with a human expert around uncertainty.")

    st.divider()
    st.subheader("Partner integrations")
    st.caption("The demo runs fully on deterministic fallbacks. Keys enable live partner tech.")
    st.markdown(f"- **Pioneer** — {_badge(_key_present('PIONEER_API_KEY') and _key_present('PIONEER_MODEL_ID'))}")
    st.markdown(f"- **Gemini** — {_badge(_key_present('GEMINI_API_KEY'))}")
    st.markdown(f"- **Tavily** — {_badge(_key_present('TAVILY_API_KEY'))}")
    st.markdown("- **Aikido** — 🔒 security scan (submission docs)")

if preset == "Living tissue preservation failure":
    default_obs = """Context: ex vivo preserved tissue sample in a biotech R&D workflow. Preservation duration: 48h cold storage. Macro signals: lactate rising, pH falling, vascular resistance increasing, oxygenation uncertain. Goal: debug the experiment and decide which measurement should be run next, without making a clinical viability claim."""
elif preset == "Organoid QC anomaly":
    default_obs = """Context: engineered organoid QC batch. Observations: abnormal morphology, borderline viability stain, media lactate rising, differentiation marker uncertain, possible hypoxic core. Goal: identify likely failure mechanisms and choose the next assays before repeating the batch."""
else:
    default_obs = """Context: organ-on-chip drug response experiment. Observations: unexpected barrier leak, oxygen consumption shift, inflammatory marker increase, morphology change after compound exposure. Goal: troubleshoot whether this is toxicity, protocol failure, or model instability and pick the next discriminating measurement."""

observation = st.text_area("Ambiguous experiment observation", value=default_obs, height=190)

if st.button("Run agent workflow", type="primary"):
    result = run_pipeline(observation)

    # 1. Agent orchestration trace
    st.subheader("1. Agent orchestration trace")
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
    st.subheader("2. Troubleshooting memo")
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
    st.subheader("3. Pioneer structured extraction")
    st.caption(
        f"Side-challenge artifact — {_badge(pioneer['mode'] == 'live')} · {pioneer['detail']}  "
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
    st.subheader("4. Partner technology trace")
    st.caption("Live vs fallback is shown honestly — the demo never hides which integrations ran.")
    for item in result["partner_trace"]:
        st.markdown(f"- {_badge(item['live'])} **{item['tool']}** — {item['role']}.")
        st.caption(f"    {item['status']}")

    # 8. Business impact
    st.subheader("5. Business impact")
    for item in result["business_impact"]:
        st.markdown(f"- {item}")
