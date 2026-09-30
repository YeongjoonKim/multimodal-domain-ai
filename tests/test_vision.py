"""후보·모델 장애·근거 부재를 서로 다른 상태로 유지한다."""
import unittest
from src.vision_demo import Candidate, interpret


class VisionTests(unittest.TestCase):
    def test_support_requires_reference(self):
        result = interpret([Candidate("pattern-a", 0.9)])
        self.assertEqual(result["status"], "supported_candidate")
        self.assertEqual(result["claims"][0]["evidence_id"], result["evidence"][0])
        self.assertFalse(result["diagnosis"])

    def test_unknown_has_no_recommendation(self):
        result = interpret([Candidate("unknown", 0.99)])
        self.assertEqual(result["status"], "knowledge_missing")
        self.assertEqual(result["claims"], [])

    def test_low_confidence(self):
        self.assertEqual(interpret([Candidate("pattern-a", 0.2)])["status"], "low_confidence")

    def test_ambiguous(self):
        result = interpret([Candidate("pattern-a", 0.8), Candidate("pattern-b", 0.77)])
        self.assertEqual(result["status"], "ambiguous")

    def test_duplicate_not_ambiguity(self):
        self.assertEqual(interpret([Candidate("pattern-a", 0.8),
                                    Candidate("pattern-a", 0.81)])["status"], "supported_candidate")

    def test_empty_not_healthy(self):
        self.assertEqual(interpret([])["status"], "no_observation")
        self.assertFalse(interpret([])["diagnosis"])

    def test_failure_not_empty(self):
        self.assertEqual(interpret([], service_status="error")["status"], "service_error")

    def test_invalid_scores(self):
        for score in [True, float("nan"), float("inf"), -1, 2, "0.8"]:
            with self.subTest(score=score), self.assertRaises(ValueError):
                interpret([Candidate("pattern-a", score)])

    def test_private_origin_rejected(self):
        with self.assertRaises(ValueError):
            interpret([Candidate("pattern-a", 0.9, "unverified")])

    def test_invalid_policy(self):
        with self.assertRaises(ValueError):
            interpret([], threshold=True)


if __name__ == "__main__":
    unittest.main()
