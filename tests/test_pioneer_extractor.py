import os
import unittest
from unittest.mock import Mock, patch

from app.agents import pioneer_extractor


class PioneerExtractorTests(unittest.TestCase):
    def setUp(self):
        self._old_env = os.environ.copy()

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self._old_env)

    def test_live_pioneer_call_uses_documented_inference_api(self):
        os.environ["PIONEER_API_KEY"] = "test-key"
        os.environ["PIONEER_MODEL_ID"] = "fastino/gliner2-base-v1"
        os.environ.pop("PIONEER_BASE_URL", None)

        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"entities": []}

        with patch("requests.post", return_value=response) as post:
            pioneer_extractor.extract_troubleshooting_structure("lactate rising, pH falling")

        post.assert_called_once()
        url = post.call_args.args[0]
        kwargs = post.call_args.kwargs
        self.assertEqual(url, "https://api.pioneer.ai/inference")
        self.assertEqual(kwargs["headers"]["X-API-Key"], "test-key")
        self.assertEqual(kwargs["headers"]["Content-Type"], "application/json")
        self.assertNotIn("Authorization", kwargs["headers"])
        self.assertEqual(kwargs["json"]["model_id"], "fastino/gliner2-base-v1")
        self.assertEqual(kwargs["json"]["text"], "lactate rising, pH falling")
        self.assertIn("schema", kwargs["json"])
        self.assertIn("entities", kwargs["json"]["schema"])
        self.assertIn("classifications", kwargs["json"]["schema"])
        self.assertIn("relations", kwargs["json"]["schema"])
        self.assertEqual(kwargs["json"]["threshold"], 0.35)

    def test_api_key_alone_enables_base_gliner2_live_mode(self):
        os.environ["PIONEER_API_KEY"] = "test-key"
        os.environ.pop("PIONEER_MODEL_ID", None)

        status = pioneer_extractor.pioneer_status()

        self.assertTrue(status["available"])
        self.assertEqual(status["mode"], "live")
        self.assertEqual(status["model_id"], "fastino/gliner2-base-v1")

    def test_live_pioneer_entities_are_normalized_into_app_schema(self):
        os.environ["PIONEER_API_KEY"] = "test-key"
        os.environ["PIONEER_MODEL_ID"] = "job_biosignal"

        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "entities": [
                {"text": "lactate", "label": "macro_signal", "score": 0.91},
                {"text": "rising", "label": "trend", "score": 0.88},
                {"text": "hypoxia", "label": "candidate_mechanism", "score": 0.77},
                {"text": "oxygen consumption", "label": "assay", "score": 0.73},
            ],
            "classifications": [
                {"task": "safety", "label": "research_workflow_only", "score": 0.97}
            ],
        }

        with patch("requests.post", return_value=response):
            result = pioneer_extractor.extract_troubleshooting_structure("lactate rising, test oxygen consumption")

        self.assertEqual(result["mode"], "live")
        self.assertIn({"label": "lactate", "trend": "rising", "confidence": 0.91}, result["observations"])
        self.assertIn({"label": "hypoxia", "confidence": 0.77}, result["candidate_mechanisms"])
        self.assertIn({"label": "oxygen_consumption", "confidence": 0.73}, result["suggested_measurements"])
        self.assertTrue(result["safety_flags"]["research_workflow_only"])


if __name__ == "__main__":
    unittest.main()
