import unittest

from app.agents.evidence_quality import grade_evidence, build_evidence_ladder
from app.agents.outcome_loop import apply_run_outcome
from app.experiment_builder import build_custom_experiment_note, infer_dynamic_sections


class OutcomeEvidenceBuilderTests(unittest.TestCase):
    def test_outcome_loop_updates_branch_confidence_and_generates_pioneer_label(self):
        action_plan = {
            "ranked_actions": [
                {"title": "old-vs-new reagent lot control", "confidence": 0.7, "effort": "low"},
                {"title": "edge-vs-center plate-layout analysis", "confidence": 0.6, "effort": "low"},
            ]
        }
        uncertainty_map = {
            "branches": [
                {"hypothesis": "reagent_or_protocol_drift", "test": "old-vs-new reagent lot control"},
                {"hypothesis": "technical_artifact", "test": "edge-vs-center plate-layout analysis"},
            ]
        }
        pioneer = {
            "observations": [{"label": "reagent_lot", "trend": "changed"}],
            "relations": [
                {
                    "subject": "reagent_lot changed",
                    "predicate": "supports_possible_mechanism",
                    "object": "reagent_or_protocol_drift",
                    "confidence": 0.7,
                }
            ],
        }

        result = apply_run_outcome(action_plan, uncertainty_map, pioneer, "confirmed_branch")

        self.assertEqual(result["outcome"], "confirmed_branch")
        self.assertGreater(result["branch_updates"][0]["delta"], 0)
        self.assertLess(result["branch_updates"][1]["delta"], 0)
        self.assertIn("pioneer_training_row", result)
        self.assertEqual(result["pioneer_training_row"]["labels"]["outcome"], "confirmed_branch")
        self.assertIn("what_next", result)

    def test_evidence_quality_ladder_grades_directness_and_clinical_risk(self):
        evidence = [
            {
                "source": "Madissoon et al., Tissue Stability Cell Atlas / PRJEB31843",
                "claim": "Cold-preserved human tissue scRNA-seq showed stability patterns.",
                "caveat": "Indirect evidence: not the same organ.",
                "url": "https://example.org/paper",
            },
            {
                "source": "Vendor blog",
                "claim": "A vendor says edge effects happen.",
                "caveat": "Live web lead only.",
                "live": True,
            },
            {
                "source": "Assay troubleshooting heuristics",
                "claim": "Controls should be checked.",
                "caveat": "Heuristic support only.",
            },
        ]

        graded = grade_evidence(evidence, "ex-vivo tissue state / preservation R&D")
        ladder = build_evidence_ladder(graded)

        by_type = {item["evidence_type"]: item for item in graded}
        self.assertIn("paper/dataset", by_type)
        self.assertIn(by_type["paper/dataset"]["relevance"], {"direct", "adjacent"})
        self.assertIn("live web lead", by_type)
        self.assertIn("heuristic", by_type)
        self.assertGreaterEqual(len({item["evidence_type"] for item in graded}), 3)
        self.assertIn("safe_use", by_type["paper/dataset"])
        self.assertNotIn("clinical recommendation", by_type["paper/dataset"]["safe_use"].lower())

    def test_custom_experiment_builder_creates_general_purpose_notes_and_dynamic_sections(self):
        note = build_custom_experiment_note(
            workflow="ADC conjugation assay",
            sample="antibody-drug conjugate batch 17",
            observations=["DAR lower than expected", "aggregation increased", "HIC shoulder peak"],
            goal="choose the next discriminating analytical check",
            constraints="research workflow only",
        )
        sections = infer_dynamic_sections(note)

        self.assertIn("ADC conjugation assay", note)
        self.assertIn("DAR lower than expected", note)
        self.assertIn("research workflow only", note)
        self.assertIn("analytical chemistry", sections["likely_workflow_family"])
        self.assertIn("evidence_quality", sections["recommended_sections"])
        self.assertIn("outcome_loop", sections["recommended_sections"])


if __name__ == "__main__":
    unittest.main()
