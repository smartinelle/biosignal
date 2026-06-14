import unittest

from app.presets import PRESETS
from app.agents.pipeline import run_pipeline
from app.agents.action_plan import contains_forbidden_language


class PipelineProductSurfaceTests(unittest.TestCase):
    def test_pipeline_returns_uncertainty_review_and_memory_surfaces(self):
        result = run_pipeline(PRESETS[0]["note"])

        self.assertIn("uncertainty_map", result)
        self.assertIn("human_review_options", result)
        self.assertIn("experiment_memory", result)
        self.assertIn("pioneer_training_examples", result)
        self.assertGreaterEqual(len(result["uncertainty_map"]["branches"]), 3)
        self.assertIn("accept_next_action", result["human_review_options"])
        self.assertGreaterEqual(len(result["experiment_memory"]["runs"]), 3)
        self.assertGreaterEqual(len(result["pioneer_training_examples"]), 1)
        self.assertFalse(contains_forbidden_language(result["action_plan"]))


if __name__ == "__main__":
    unittest.main()
