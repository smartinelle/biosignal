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
from agents.human_review import apply_human_feedback
from agents.experiment_memory import build_experiment_memory, training_examples_from_memory
from agents.outcome_loop import apply_run_outcome
try:
    from experiment_builder import build_custom_experiment_note, infer_dynamic_sections
except ModuleNotFoundError:
    from app.experiment_builder import build_custom_experiment_note, infer_dynamic_sections
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
    st.header("Experiment setup")
    mode = st.radio("Input mode", ["Preset demo", "Custom workflow"], horizontal=True)
    preset = st.selectbox(
        "Preset case",
        PRESET_LABELS,
        disabled=mode == "Custom workflow",
    )
    st.markdown("**Product:** general biotech R&D troubleshooting.")
    st.markdown("**Use cases:** assay, qPCR/ddPCR, protein, cell culture, bioprocess, preservation, organoid/OoC — or your own workflow.")
    st.markdown("**Atira fit:** specialized agents coordinate with a human expert around uncertainty.")

    st.divider()
    st.subheader("Partner integrations")
    st.caption("The demo runs fully on deterministic fallbacks. Keys enable live partner tech.")
    st.markdown(f"- **Pioneer** — {_badge(_key_present('PIONEER_API_KEY'))} structured extractor")
    st.markdown(f"- **Gemini** — {_badge(_key_present('GEMINI_API_KEY') or _key_present('OPENROUTER_API_KEY'))}")
    st.markdown(f"- **Tavily** — {_badge(_key_present('TAVILY_API_KEY'))}")
    st.markdown("- **Aikido** — 🔒 security scan (submission docs)")

selected_preset = PRESETS_BY_LABEL.get(preset, PRESETS[0])
if mode == "Custom workflow":
    with st.container(border=True):
        st.markdown("### Design your own experiment workflow")
        c1, c2 = st.columns(2)
        workflow = c1.text_input("Workflow / assay", value="ADC conjugation assay")
        sample = c2.text_input("Sample / system", value="antibody-drug conjugate batch 17")
        observations_raw = st.text_area(
            "Observed anomaly / readouts, one per line",
            value="DAR lower than expected\naggregation increased\nHIC shoulder peak",
            height=110,
        )
        goal = st.text_input("Goal", value="choose the next discriminating analytical check")
        constraints = st.text_input("Constraints", value="research workflow only; no release or clinical recommendation")
        observation = build_custom_experiment_note(
            workflow=workflow,
            sample=sample,
            observations=observations_raw.splitlines(),
            goal=goal,
            constraints=constraints,
        )
        dynamic_sections = infer_dynamic_sections(observation)
        st.caption(f"Dynamic workflow family: {dynamic_sections['likely_workflow_family']}")
        st.caption("Recommended UI sections: " + ", ".join(dynamic_sections["recommended_sections"]))
else:
    default_obs = get_note(preset)
    observation = st.text_area("Ambiguous experiment observation", value=default_obs, height=190)
    st.caption(f"Selected workflow: {selected_preset['category']}")

if "last_result" not in st.session_state:
    st.session_state["last_result"] = None

if st.button("Run agent workflow", type="primary"):
    st.session_state["last_result"] = run_pipeline(observation)

result = st.session_state.get("last_result")
if result:

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

    # 1b. Uncertainty map — turn ambiguity into a decision graph instead of an answer.
    uncertainty_map = result["uncertainty_map"]
    with st.container(border=True):
        st.markdown("## 1b. Uncertainty map")
        st.caption(uncertainty_map["copy"])
        branch_cols = st.columns(min(3, len(uncertainty_map["branches"])))
        for col, branch in zip(branch_cols, uncertainty_map["branches"]):
            with col:
                st.markdown(f"### {branch['hypothesis']}")
                st.markdown(f"**Test:** {branch['test']}")
                st.markdown(f"**Change-my-mind rule:** {branch['what_would_change_our_mind']}")
                st.caption(branch["human_question"])
        with st.expander("Decision graph source", expanded=False):
            st.code(uncertainty_map["mermaid"], language="mermaid")

    # 1c. Scientist Review Mode — visible human-in-the-loop controls.
    with st.container(border=True):
        st.markdown("## 1c. Scientist Review Mode")
        st.caption("The human does not just receive an answer — they correct the agent trace. Those corrections become Pioneer training/eval signal.")
        feedback_label_by_key = result["human_review_options"]
        feedback_key = st.radio(
            "Human feedback",
            list(feedback_label_by_key.keys()),
            format_func=lambda key: feedback_label_by_key[key],
            horizontal=True,
        )
        feedback_note = st.text_input("Optional missing context / correction", placeholder="e.g. this cell line often shows edge sensitivity after thaw")
        reviewed_plan = apply_human_feedback(action_plan, feedback_key, feedback_note)
        st.session_state["reviewed_action_plan"] = reviewed_plan
        st.info(reviewed_plan["human_decision"])
        if reviewed_plan.get("human_feedback", {}).get("pioneer_training_event"):
            st.success(reviewed_plan["human_feedback"]["why_pioneer_cares"])
        reviewed_top = reviewed_plan["ranked_actions"][0]
        st.markdown(f"**Reviewed top action:** {reviewed_top['title']} · confidence `{reviewed_top['confidence']}`")
        if reviewed_top.get("human_note"):
            st.caption(reviewed_top["human_note"])

    # 1d. Run Outcome — close the loop after the recommended experiment.
    with st.container(border=True):
        st.markdown("## 1d. Run Outcome")
        st.caption("After the scientist runs the next measurement, the result updates branch confidence and creates a labeled Pioneer training row.")
        outcome = st.selectbox(
            "Measurement outcome",
            ["confirmed_branch", "weakened_branch", "inconclusive", "new_anomaly_found"],
            format_func=lambda x: {
                "confirmed_branch": "Confirmed selected branch",
                "weakened_branch": "Weakened selected branch",
                "inconclusive": "Inconclusive",
                "new_anomaly_found": "New anomaly found",
            }[x],
        )
        outcome_note = st.text_input("Outcome note", placeholder="e.g. old reagent lot rescued the signal")
        outcome_result = apply_run_outcome(reviewed_plan, uncertainty_map, result["pioneer_structured"], outcome, note=outcome_note)
        st.markdown(f"**What next:** {outcome_result['what_next']}")
        st.dataframe(
            [
                {
                    "Branch": update["branch"],
                    "Status": update["status"],
                    "Δ confidence": update["delta"],
                    "New confidence": update["new_confidence"],
                }
                for update in outcome_result["branch_updates"]
            ],
            hide_index=True,
        )
        with st.expander("Pioneer training row from outcome", expanded=False):
            st.json(outcome_result["pioneer_training_row"])

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

    # 5. Evidence quality ladder, evidence and caveats
    st.markdown("### Evidence Quality Ladder")
    st.caption("Evidence is graded for directness and safe use before it influences the next experiment.")
    ladder_cols = st.columns(min(4, max(1, len(result["evidence_ladder"]))))
    for col, tier in zip(ladder_cols, result["evidence_ladder"]):
        with col:
            st.metric(tier["label"], tier["count"])
            st.caption(tier["safe_use"])
    st.markdown("### Evidence and caveats")
    for e in result["evidence"]:
        title = e["source"] + ("  ·  🟢 live (Tavily)" if e.get("live") else "")
        with st.expander(title, expanded=not e.get("live")):
            st.markdown(f"**Claim:** {e['claim']}")
            st.markdown(
                f"**Quality:** `{e.get('evidence_type', 'unknown')}` · `{e.get('relevance', 'unknown')}` · strength `{e.get('strength', '?')}/5"
            )
            st.markdown(f"**Safe use:** {e.get('safe_use', 'Hypothesis generation only.')}")
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

    # 6b. Experiment memory / Pioneer learning loop
    reviewed_plan_for_memory = st.session_state.get("reviewed_action_plan", result["action_plan"])
    memory = build_experiment_memory(result["structured_observations"], reviewed_plan_for_memory, pioneer)
    training_examples = training_examples_from_memory(memory)
    st.subheader("4b. Experiment memory / Pioneer learning loop")
    st.caption(memory["learning_loop"])
    m1, m2, m3, m4 = st.columns(4)
    stats = memory["stats"]
    m1.metric("Stored runs", stats["stored_runs"])
    m2.metric("Accepted/resolved", stats["accepted_or_resolved"])
    m3.metric("Pending/review", stats["pending_or_review_needed"])
    m4.metric("Relations this run", stats["extracted_relations_this_run"])
    st.dataframe(
        [
            {
                "Source": run["source"],
                "Workflow": run["workflow"],
                "Ambiguous signal": run["ambiguous_signal"],
                "Human branch": run["chosen_branch"],
                "Status": run["status"],
                "Pioneer value": run["pioneer_value"],
            }
            for run in memory["runs"]
        ],
        hide_index=True,
    )
    with st.expander("Example training rows produced from memory", expanded=False):
        st.json(training_examples[:3])

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
