import streamlit as st
from agents.pipeline import run_pipeline

st.set_page_config(page_title="BioSignal Navigator", page_icon="🧬", layout="wide")

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

if preset == "Living tissue preservation failure":
    default_obs = """Context: ex vivo preserved tissue sample in a biotech R&D workflow. Preservation duration: 48h cold storage. Macro signals: lactate rising, pH falling, vascular resistance increasing, oxygenation uncertain. Goal: debug the experiment and decide which measurement should be run next, without making a clinical viability claim."""
elif preset == "Organoid QC anomaly":
    default_obs = """Context: engineered organoid QC batch. Observations: abnormal morphology, borderline viability stain, media lactate rising, differentiation marker uncertain, possible hypoxic core. Goal: identify likely failure mechanisms and choose the next assays before repeating the batch."""
else:
    default_obs = """Context: organ-on-chip drug response experiment. Observations: unexpected barrier leak, oxygen consumption shift, inflammatory marker increase, morphology change after compound exposure. Goal: troubleshoot whether this is toxicity, protocol failure, or model instability and pick the next discriminating measurement."""

observation = st.text_area("Ambiguous experiment observation", value=default_obs, height=190)

if st.button("Run agent workflow", type="primary"):
    result = run_pipeline(observation)

    st.subheader("1. Agent trace")
    cols = st.columns(5)
    for col, step in zip(cols, result["trace"]):
        with col:
            st.markdown(f"**{step['agent']}**")
            st.write(step["summary"])

    st.subheader("2. Uncertainty bottleneck")
    bottleneck = result["uncertainty_bottleneck"]
    st.warning(f"**{bottleneck['headline']}**\n\n{bottleneck['why_it_matters']}", icon="⚠️")
    st.markdown(f"**Decision to unlock:** {bottleneck['decision_to_unlock']}")

    st.subheader("3. Experiment troubleshooting memo")
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

    st.markdown("### Evidence and caveats")
    for e in result["evidence"]:
        with st.expander(e["source"], expanded=True):
            st.markdown(f"**Claim:** {e['claim']}")
            st.caption(f"Caveat: {e['caveat']}")

    st.subheader("4. Pioneer-style structured triples")
    st.caption("Visible side-challenge artifact: extract signal → hypothesis → next-measurement triples rather than hiding partner tech in the backend.")
    st.json(result["pioneer_triples"])

    st.subheader("5. Business impact")
    for item in result["business_impact"]:
        st.markdown(f"- {item}")

    st.subheader("6. Partner technology trace")
    for item in result["partner_trace"]:
        st.markdown(f"- **{item['tool']}** — {item['role']}. _{item['status']}._")
