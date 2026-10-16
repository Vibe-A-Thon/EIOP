"""Tests for AI/ML ops — RLHF, hallucination detection, attention, temperature tuning, token budgets."""

from __future__ import annotations

import unittest


class TestRLHFRewardModel(unittest.TestCase):
    def setUp(self):
        from eoip.model_management.ai_ml_ops import RLHFRewardModel, PreferenceLabel
        self.rlhf = RLHFRewardModel()
        self.PreferenceLabel = PreferenceLabel

    def test_add_preference_pair(self):
        pair = self.rlhf.add_preference(
            prompt="Explain X", response_a="Answer A", response_b="Answer B",
            label=self.PreferenceLabel.PREFERRED, annotator="alice",
        )
        self.assertEqual(pair.label, self.PreferenceLabel.PREFERRED)
        self.assertEqual(pair.annotator, "alice")

    def test_compute_reward_with_reference(self):
        score = self.rlhf.compute_reward(
            response="The database stores user data and sessions",
            reference="The database stores user data sessions and tokens",
        )
        self.assertGreater(score.score, 0)
        self.assertIn("relevance", score.components)
        self.assertIn("safety", score.components)

    def test_compute_reward_with_sources(self):
        score = self.rlhf.compute_reward(
            response="The auth service handles user login and password verification",
            source_texts=["auth service manages login and password checks"],
        )
        self.assertGreater(score.components["accuracy"], 0.3)

    def test_safety_penalty(self):
        safe = self.rlhf.compute_reward(response="The system provides helpful answers")
        unsafe = self.rlhf.compute_reward(response="Use this exploit to hack and attack the system bypass security")
        self.assertGreater(safe.components["safety"], unsafe.components["safety"])

    def test_agreement_rate(self):
        self.rlhf.add_preference("Q1", "A", "B", self.PreferenceLabel.PREFERRED, "a")
        self.rlhf.add_preference("Q1", "A", "B", self.PreferenceLabel.PREFERRED, "b")
        rate = self.rlhf.agreement_rate()
        self.assertEqual(rate, 1.0)

    def test_update_weights(self):
        self.rlhf.update_weights({"relevance": 0.5, "safety": 0.5})
        self.assertEqual(self.rlhf._reward_weights["relevance"], 0.5)

    def test_stats(self):
        self.rlhf.add_preference("Q", "A", "B", self.PreferenceLabel.TIE, "x")
        stats = self.rlhf.stats()
        self.assertEqual(stats["total_pairs"], 1)
        self.assertIn("TIE", stats["by_label"])


class TestHallucinationDetector(unittest.TestCase):
    def setUp(self):
        from eoip.model_management.ai_ml_ops import HallucinationDetector
        self.detector = HallucinationDetector()

    def test_grounded_response(self):
        report = self.detector.check(
            response="The auth service handles login. It uses JWT tokens.",
            source_texts=["The auth service handles user login via JWT tokens"],
        )
        self.assertGreater(report.grounding_ratio, 0.5)
        self.assertIn(report.severity.value, ("NONE", "LOW"))

    def test_ungrounded_response(self):
        report = self.detector.check(
            response="The quantum flux capacitor enables time travel. Aliens built it.",
            source_texts=["The database stores user records"],
        )
        self.assertGreater(len(report.ungrounded_claims), 0)
        self.assertIn(report.severity.value, ("HIGH", "CRITICAL", "MODERATE"))

    def test_empty_response(self):
        report = self.detector.check(response="", source_texts=["source"])
        self.assertEqual(report.severity.value, "NONE")

    def test_overall_grounding_rate(self):
        self.detector.check("The database stores data", ["database stores data"])
        self.detector.check("Unicorns fly in space", ["database stores data"])
        rate = self.detector.overall_grounding_rate()
        self.assertGreater(rate, 0)
        self.assertLess(rate, 1.0)

    def test_stats(self):
        self.detector.check("test response", ["test source"])
        stats = self.detector.stats()
        self.assertEqual(stats["total_checks"], 1)


class TestAttentionAnalyzer(unittest.TestCase):
    def setUp(self):
        from eoip.model_management.ai_ml_ops import AttentionAnalyzer
        self.analyzer = AttentionAnalyzer()

    def test_compute_attention(self):
        query = [1.0, 0.0, 0.5]
        keys = [[1.0, 0.0, 0.5], [0.0, 1.0, 0.0], [0.5, 0.5, 0.5]]
        weights = self.analyzer.compute_attention(query, keys)
        self.assertEqual(len(weights), 3)
        self.assertAlmostEqual(sum(weights), 1.0, places=5)
        self.assertEqual(weights.index(max(weights)), 0)

    def test_attention_entropy(self):
        uniform = [0.25, 0.25, 0.25, 0.25]
        focused = [0.97, 0.01, 0.01, 0.01]
        self.assertGreater(
            self.analyzer.attention_entropy(uniform),
            self.analyzer.attention_entropy(focused),
        )

    def test_record_pattern(self):
        pattern = self.analyzer.record_pattern(
            layer=0, head=0,
            source_tokens=["the", "cat"],
            target_tokens=["sat"],
            attention_weights=[[0.9, 0.1]],
        )
        self.assertEqual(pattern.layer, 0)
        self.assertIn(pattern.pattern_type, ("focused", "moderate", "diffuse"))

    def test_find_salient_tokens(self):
        weights = [[0.8, 0.1, 0.05, 0.05]]
        tokens = ["important", "filler1", "filler2", "filler3"]
        salient = self.analyzer.find_salient_tokens(weights, tokens, top_k=2)
        self.assertEqual(salient[0][0], "important")

    def test_stats(self):
        self.analyzer.record_pattern(0, 0, ["a"], ["b"], [[1.0]])
        stats = self.analyzer.stats()
        self.assertEqual(stats["total_patterns"], 1)


class TestTemperatureTuner(unittest.TestCase):
    def setUp(self):
        from eoip.model_management.ai_ml_ops import TemperatureTuner
        self.tuner = TemperatureTuner()

    def test_create_experiment(self):
        exp = self.tuner.create_experiment("low-temp", temperature=0.3)
        self.assertEqual(exp.temperature, 0.3)
        self.assertEqual(exp.trial_count, 0)

    def test_record_trial(self):
        exp = self.tuner.create_experiment("test")
        self.tuner.record_trial(exp.experiment_id, 0.8, 0.6, 0.9)
        self.assertEqual(exp.trial_count, 1)
        self.assertAlmostEqual(exp.avg_quality, 0.8)

    def test_best_config(self):
        e1 = self.tuner.create_experiment("low", temperature=0.3)
        e2 = self.tuner.create_experiment("high", temperature=1.2)
        self.tuner.record_trial(e1.experiment_id, 0.9, 0.5, 0.9)
        self.tuner.record_trial(e2.experiment_id, 0.4, 0.9, 0.3)
        best = self.tuner.best_config()
        self.assertEqual(best.experiment_id, e1.experiment_id)

    def test_compare(self):
        e1 = self.tuner.create_experiment("a")
        e2 = self.tuner.create_experiment("b")
        self.tuner.record_trial(e1.experiment_id, 0.7, 0.7, 0.7)
        self.tuner.record_trial(e2.experiment_id, 0.5, 0.5, 0.5)
        comparison = self.tuner.compare([e1.experiment_id, e2.experiment_id])
        self.assertEqual(comparison[0]["experiment_id"], e1.experiment_id)

    def test_stats(self):
        self.tuner.create_experiment("x")
        stats = self.tuner.stats()
        self.assertEqual(stats["total_experiments"], 1)


class TestTokenBudgetManager(unittest.TestCase):
    def setUp(self):
        from eoip.model_management.ai_ml_ops import TokenBudgetManager
        self.mgr = TokenBudgetManager()

    def test_create_and_consume(self):
        budget = self.mgr.create_budget("test", max_total=1000)
        ok = self.mgr.consume(budget.budget_id, 200, 100)
        self.assertTrue(ok)
        self.assertEqual(budget.used_prompt_tokens, 200)
        self.assertEqual(budget.used_completion_tokens, 100)

    def test_budget_exceeded(self):
        budget = self.mgr.create_budget("small", max_total=100,
                                        max_prompt=50, max_completion=50)
        ok = self.mgr.consume(budget.budget_id, 60, 10)
        self.assertFalse(ok)

    def test_utilization(self):
        budget = self.mgr.create_budget("test", max_total=1000)
        self.mgr.consume(budget.budget_id, 250, 250)
        self.assertAlmostEqual(budget.utilization, 0.5)

    def test_auto_reset(self):
        budget = self.mgr.create_budget("test", max_total=100,
                                        reset_interval=0.0)
        self.mgr.consume(budget.budget_id, 50, 40)
        budget.last_reset = 0.0
        ok = self.mgr.consume(budget.budget_id, 50, 40)
        self.assertTrue(ok)

    def test_stats(self):
        self.mgr.create_budget("a")
        self.mgr.create_budget("b")
        stats = self.mgr.stats()
        self.assertEqual(stats["total_budgets"], 2)


class TestAIMLOpsManager(unittest.TestCase):
    def test_unified_stats(self):
        from eoip.model_management.ai_ml_ops import AIMLOpsManager
        mgr = AIMLOpsManager()
        stats = mgr.stats()
        self.assertIn("rlhf", stats)
        self.assertIn("hallucination", stats)
        self.assertIn("attention", stats)
        self.assertIn("temperature", stats)
        self.assertIn("token_budgets", stats)


if __name__ == "__main__":
    unittest.main()
