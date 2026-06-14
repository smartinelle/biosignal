import unittest

from app.agents.action_plan import build_action_plan
from app.agents.uncertainty_map import build_uncertainty_map
from app.agents.human_review import apply_human_feedback
from app.agents.experiment_memory import build_experiment_memory, training_examples_from_memory


class DecisionWorkflowTests(unittest.TestCase):
    def _sample_inputs(self):
        structured = {
            "domain": "biotech R&D assay troubleshooting",
            "signals_detected": ["positive control", "plate edge", "reagent"],
        }
        hypotheses = [
            {"mechanism": "reagent_or_protocol_drift", "rationale": "control drift and lot change"},
            {"mechanism": "technical_artifact", "rationale": "edge wells look worse"},
            {"mechanism": "true_biology", "rationale": "signal collapse could be biological"},
        ]
        measurements = [
            {"measurement": "old-vs-new reagent lot control", "why": "Separates reagent drift from biology."},
            {"measurement": "edge-vs-center plate layout repeat", "why": "Tests for plate artifact."},
            {"measurement": "orthogonal readout", "why": "Checks whether biology reproduces."},
        ]
        evidence = [{"source": "curated", "claim": "controls matter", "caveat": "demo"}]
        workflow_context = {"role": "General biotech R&D workflow", "workflow_moment": "ambiguous assay run"}
        bottleneck = {
            "headline": "The data is underdetermined",
            "why_it_matters": "Multiple explanations fit.",
            "decision_to_unlock": "Which branch should be tested first?",
        }
        partner_trace = [{"tool": "Pioneer", "live": False}]
        action_plan = build_action_plan(
            structured, hypotheses, measurements, evidence, workflow_context, bottleneck, partner_trace
        )
        pioneer = {
            "observations": [{"label": "positive_control", "trend": "drifted", "confidence": 0.91}],
            "candidate_mechanisms": [{"label": "reagent_or_protocol_drift", "confidence": 0.8}],
            "suggested_measurements": [{"label": "old_vs_new_reagent_lot_control", "confidence": 0.7}],
            "relations": [
                {
                    "subject": "positive_control drifted",
                    "predicate": "supports_possible_mechanism",
                    "object": "reagent_or_protocol_drift",
                    "confidence": 0.78,
                }
            ],
            "safety_flags": {"research_workflow_only": True, "needs_human_review": True},
            "mode": "fallback",
        }
        return structured, hypotheses, measurements, evidence, bottleneck, action_plan, pioneer

    def test_uncertainty_map_has_branch_tests_and_change_my_mind_copy(self):
        structured, hypotheses, measurements, evidence, bottleneck, action_plan, pioneer = self._sample_inputs()

        result = build_uncertainty_map(structured, hypotheses, measurements, evidence, bottleneck)

        self.assertEqual(result["headline"], "What would change our mind?")
        self.assertGreaterEqual(len(result["branches"]), 3)
        first = result["branches"][0]
        self.assertIn("hypothesis", first)
        self.assertIn("test", first)
        self.assertIn("what_would_change_our_mind", first)
        self.assertIn("mermaid", result)
        self.assertIn("graph TD", result["mermaid"])
        self.assertNotIn("diagnosis", str(result).lower())

    def test_human_feedback_can_rerank_annotate_and_mark_training_signal(self):
        structured, hypotheses, measurements, evidence, bottleneck, action_plan, pioneer = self._sample_inputs()

        faster = apply_human_feedback(action_plan, "ask_faster_alternative")
        self.assertIn("human_feedback", faster)
        self.assertLessEqual(faster["ranked_actions"][0]["effort_score"], faster["ranked_actions"][-1]["effort_score"])
        self.assertIn("cheapest discriminating", faster["human_feedback"]["annotation"].lower())

        flagged = apply_human_feedback(action_plan, "flag_top_hypothesis_implausible")
        self.assertIn("implausible", flagged["ranked_actions"][0]["human_note"].lower())
        self.assertTrue(flagged["human_feedback"]["pioneer_training_event"])

    def test_experiment_memory_turns_reviewed_runs_into_pioneer_training_examples(self):
        structured, hypotheses, measurements, evidence, bottleneck, action_plan, pioneer = self._sample_inputs()
        reviewed_plan = apply_human_feedback(action_plan, "accept_next_action")

        memory = build_experiment_memory(structured, reviewed_plan, pioneer)
        examples = training_examples_from_memory(memory)

        self.assertGreaterEqual(len(memory["runs"]), 3)
        self.assertEqual(memory["runs"][0]["source"], "current_run")
        self.assertIn("Pioneer", memory["learning_loop"])
        self.assertGreaterEqual(len(examples), 1)
        self.assertIn("input", examples[0])
        self.assertIn("labels", examples[0])
        self.assertIn("relations", examples[0]["labels"])


if __name__ == "__main__":
    unittest.main()
