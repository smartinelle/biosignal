import streamlit as st
from agents.pipeline import run_pipeline

st.set_page_config(page_title="BioSignal Navigator", page_icon="🧬", layout="wide")

st.title("🧬 BioSignal Navigator")
st.caption("Agent-human evidence routing from biomedical observations to molecular hypotheses and next measurements.")

with st.sidebar:
    st.header("Demo presets")
    preset = st.selectbox("Case", ["Tissue preservation", "Sepsis/inflammation", "Organoid QC"])
    st.markdown("**Safety framing:** research workflow, not diagnosis or treatment.")

if preset == "Tissue preservation":
    default_obs = """Context: ex vivo preserved tissue sample. Preservation duration: 48h cold storage. Macro signals: lactate rising, pH falling, vascular resistance increasing, oxygenation uncertain. Goal: understand possible molecular degradation processes and what measurements would reduce uncertainty."""
elif preset == "Sepsis/inflammation":
    default_obs = """Context: inflammatory patient cohort research note. Observations: lactate elevated, CRP high, hypotension, neutrophil activation suspected. Goal: map observations to plausible mechanisms and biomarker panel for research triage."""
else:
    default_obs = """Context: engineered organoid QC. Observations: morphology abnormal, viability stain borderline, media lactate rising, differentiation marker uncertain. Goal: identify likely mechanisms and next assays."""

observation = st.text_area("Biomedical observation", value=default_obs, height=180)

if st.button("Run agent workflow", type="primary"):
    result = run_pipeline(observation)
    st.subheader("Agent trace")
    cols = st.columns(5)
    for col, step in zip(cols, result["trace"]):
        with col:
            st.markdown(f"**{step['agent']}**")
            st.write(step["summary"])

    st.subheader("Evidence card")
    left, right = st.columns([1,1])
    with left:
        st.markdown("### Structured observations")
        st.json(result["structured_observations"])
        st.markdown("### Top hypotheses")
        for h in result["hypotheses"]:
            st.markdown(f"- **{h['mechanism']}** — {h['rationale']}")
    with right:
        st.markdown("### Suggested measurements")
        for m in result["measurements"]:
            st.markdown(f"- **{m['measurement']}** — {m['why']}")
        st.markdown("### Human review question")
        st.info(result["human_question"])

    st.markdown("### Evidence and caveats")
    for e in result["evidence"]:
        st.markdown(f"- **{e['source']}**: {e['claim']}  
  Caveat: {e['caveat']}")
