"""Comprehensive Unit Tests for EOIP Phase 4 — Phase 3 AI/ML Intelligence Enhancements.

Validates:
- AI-001: Advanced XAI Engine (Shapley attribution, trace graph, calibration, rendering)
- AI-002: Deep NLP Pipeline (NER, aspect sentiment, topic modeling, language detection, coreference)
- AI-004: Model A/B Testing & Canary Deployment (Traffic split, significance, auto-rollback)
- AI-005: MLOps Experiment Tracking (Runs, metrics, artifacts, comparison, best-run)
- AI-006: Embedding Management & Versioning (Registry, drift detector, fusion, dimension reduction)
- AI-007: Probabilistic Reasoning Integration (Bayesian belief updates, uncertainty propagation, query engine)
"""

import math
import pytest

from eoip.xai.engine import (
    AdvancedXAIEngine,
    ConfidenceCalibrator,
    DecisionTraceGraph,
    FeatureImportanceAnalyzer,
    get_xai_engine,
)
from eoip.nlp.pipeline import (
    DeepEntityExtractor,
    LanguageDetector,
    SentimentAnalyzer,
    TopicModeler,
    CoreferenceResolver,
)
from eoip.model_management.registry import (
    ABExperiment,
    CanaryDeployment,
    CanaryStatus,
    ExperimentStatus,
    get_model_registry,
)
from eoip.mlops.experiment_tracker import (
    ExperimentTracker,
    RunStatus,
    get_experiment_tracker,
)
from eoip.embeddings.engine import (
    DimensionReducer,
    EmbeddingDriftDetector,
    EmbeddingEngine,
    EmbeddingFusionStrategy,
    EmbeddingRegistry,
    FusionMethod,
    get_embedding_engine,
)
from eoip.reasoning.strategies import (
    BayesianGraphReasoner,
    ProbabilisticQueryEngine,
    ProbabilisticStrategy,
    ReasoningProblem,
    UncertaintyPropagator,
    default_registry,
)


@pytest.mark.req("AI-001")
class TestAI001AdvancedXAI:
    """AI-001: Advanced XAI Engine."""

    def test_feature_importance_shapley(self):
        analyzer = FeatureImportanceAnalyzer()

        # Simple linear function: f(x1, x2, x3) = 2*x1 - 3*x2 + 0.5*x3
        def predict(features):
            return 2.0 * features.get("x1", 0) - 3.0 * features.get("x2", 0) + 0.5 * features.get("x3", 0)

        inputs = {"x1": 5.0, "x2": 2.0, "x3": 4.0}
        baseline = {"x1": 0.0, "x2": 0.0, "x3": 0.0}

        attributions = analyzer.analyze(predict, inputs, baseline)
        assert len(attributions) == 3

        attr_map = {a.feature_name: a for a in attributions}
        # x1 marginal is +10.0
        assert attr_map["x1"].importance_score > 5.0
        assert attr_map["x1"].direction == "POSITIVE"

        # x2 marginal is -6.0
        assert attr_map["x2"].importance_score < 0.0
        assert attr_map["x2"].direction == "NEGATIVE"

        # x1 has highest absolute impact
        assert attributions[0].feature_name == "x1"

    def test_decision_trace_graph_and_critical_path(self):
        graph = DecisionTraceGraph()
        graph.add_step("s1", "PREMISE", "Service Latency high", confidence=0.95)
        graph.add_step("s2", "INFERENCE", "Downstream DB connection pool exhausted", confidence=0.60)
        graph.add_step("s3", "VERIFICATION", "Connection metrics verified via Prometheus", confidence=0.90)
        graph.add_step("s4", "CONCLUSION", "Root cause is DB connection starvation", confidence=0.88)

        graph.add_edge("s1", "s2", "DERIVES")
        graph.add_edge("s2", "s3", "SUPPORTS")
        graph.add_edge("s3", "s4", "PROVES")

        crit_path = graph.find_critical_path()
        assert len(crit_path) == 4
        assert "s2" in crit_path

        mermaid = graph.export_mermaid()
        assert "flowchart TD" in mermaid
        assert "s1 -->|DERIVES| s2" in mermaid

    def test_confidence_calibration(self):
        calibrator = ConfidenceCalibrator()

        # Well calibrated: predictions ~ 0.8 have ~80% positive rate
        preds = [0.8, 0.85, 0.78, 0.82, 0.2, 0.15, 0.22, 0.18, 0.81, 0.19]
        actuals = [1, 1, 1, 0, 0, 0, 0, 1, 1, 0]

        report = calibrator.evaluate(preds, actuals, num_bins=5)
        assert report.total_samples == 10
        assert report.expected_calibration_error < 0.35
        assert report.brier_score >= 0.0
        assert len(report.bins) > 0


@pytest.mark.req("AI-002")
class TestAI002DeepNLP:
    """AI-002: Deep NLP Pipeline."""

    def test_deep_entity_extractor(self):
        extractor = DeepEntityExtractor()
        text = "PaymentService experienced an Incident while connecting to Google and checking auth_latency."
        entities = extractor.extract(text)

        labels = {e.label: e.text for e in entities}
        assert "SYSTEM_COMPONENT" in labels
        assert labels["SYSTEM_COMPONENT"] == "PaymentService"
        assert "ORGANIZATION" in labels
        assert labels["ORGANIZATION"] == "Google"
        assert "EVENT" in labels
        assert labels["EVENT"] == "Incident"
        assert "METRIC" in labels
        assert labels["METRIC"] == "auth_latency"

    def test_aspect_sentiment_analyzer(self):
        analyzer = SentimentAnalyzer()
        text = "The system performance is fast and optimal. However, security is vulnerable and broken."
        result = analyzer.analyze(text, aspects=["performance", "security"])

        aspect_map = {a.aspect: a for a in result.aspects}
        assert "performance" in aspect_map
        assert aspect_map["performance"].label == "POSITIVE"
        assert aspect_map["performance"].score > 0.0

        assert "security" in aspect_map
        assert aspect_map["security"].label == "NEGATIVE"
        assert aspect_map["security"].score < 0.0

    def test_topic_modeler_and_language_detector(self):
        # 1. Topic modeling
        modeler = TopicModeler(num_topics=2)
        docs = [
            "database query optimization index table sql performance",
            "frontend user interface design component react button css",
            "database latency memory cluster postgres cache",
            "frontend visual layout typography theme widget style",
        ]
        modeler.fit(docs)
        assert len(modeler.topics) == 2

        dist = modeler.predict("database index performance table")
        assert len(dist) == 2
        assert sum(s for _, s in dist) == pytest.approx(1.0, rel=1e-2)

        # 2. Language detector
        detector = LanguageDetector()
        res_en = detector.detect("The service is running properly with low latency.")
        assert res_en.language == "en"
        assert res_en.confidence >= 0.5

        res_es = detector.detect("El servicio se ejecuta en la nube por los usuarios.")
        assert res_es.language == "es"

    def test_coreference_resolver(self):
        resolver = CoreferenceResolver()
        text = "AuthService was deployed yesterday. It processed over 10,000 requests. This service is healthy."
        clusters = resolver.resolve(text)
        assert len(clusters) >= 1
        assert clusters[0].representative_entity == "AuthService"
        assert len(clusters[0].mentions) >= 2


@pytest.mark.req("AI-004")
class TestAI004ModelABTestingAndCanary:
    """AI-004: Model A/B Testing & Canary Deployment."""

    def test_ab_experiment_lifecycle_and_significance(self):
        reg = get_model_registry()
        exp = reg.create_ab_experiment(
            name="LLM-Sonnet-vs-Haiku",
            control_model_id="model_sonnet",
            candidate_model_id="model_haiku",
            traffic_split=0.5,
        )

        assert exp.status == ExperimentStatus.RUNNING

        # Deterministic routing
        route_1 = exp.route_request("req_abc_123")
        route_2 = exp.route_request("req_abc_123")
        assert route_1 == route_2
        assert route_1 in ("model_sonnet", "model_haiku")

        # Simulate metrics with distinct performance distribution
        for _ in range(50):
            exp.record_metric("model_sonnet", latency_ms=120.0, quality_score=0.95, is_error=False)
            exp.record_metric("model_haiku", latency_ms=45.0, quality_score=0.45, is_error=False)

        res = exp.evaluate_significance()
        assert res["control_samples"] == 50
        assert res["candidate_samples"] == 50
        assert res["statistically_significant"] is True
        assert res["recommended_winner"] == "model_sonnet"

    def test_canary_deployment_promotion_and_auto_rollback(self):
        reg = get_model_registry()
        canary = reg.create_canary_deployment(
            stable_model_id="srv_stable_v1",
            canary_model_id="srv_canary_v2",
            initial_traffic_pct=10.0,
            max_error_rate=0.10,
        )

        assert canary.status == CanaryStatus.ACTIVE
        assert canary.canary_traffic_pct == 10.0

        # Promote traffic
        new_pct = canary.promote_traffic(increment_pct=25.0)
        assert new_pct == 35.0

        # Breach error rate threshold -> auto-rollback
        for _ in range(8):
            canary.record_canary_invocation(latency_ms=150.0, is_error=True)

        status_rep = canary.check_health_and_auto_rollback()
        assert status_rep["rolled_back"] is True
        assert canary.status == CanaryStatus.ROLLED_BACK
        assert canary.canary_traffic_pct == 0.0


@pytest.mark.req("AI-005")
class TestAI005MLOpsExperimentTracking:
    """AI-005: MLOps Experiment Tracking."""

    def test_experiment_runs_and_comparison(self):
        tracker = get_experiment_tracker()
        exp = tracker.create_experiment(name="Prompt-Tuning-Optimization", description="RAG prompt evaluations")

        # Run 1
        r1 = tracker.start_run(exp.experiment_id, run_name="temperature-0.2")
        tracker.log_param(exp.experiment_id, r1.run_id, "temperature", 0.2)
        tracker.log_metric(exp.experiment_id, r1.run_id, "accuracy", 0.85)
        tracker.log_metric(exp.experiment_id, r1.run_id, "latency", 120.0)
        tracker.end_run(exp.experiment_id, r1.run_id, status=RunStatus.COMPLETED)

        # Run 2
        r2 = tracker.start_run(exp.experiment_id, run_name="temperature-0.7")
        tracker.log_param(exp.experiment_id, r2.run_id, "temperature", 0.7)
        tracker.log_metric(exp.experiment_id, r2.run_id, "accuracy", 0.94)
        tracker.log_metric(exp.experiment_id, r2.run_id, "latency", 140.0)
        # Store artifact
        art_id = tracker.log_artifact(exp.experiment_id, r2.run_id, "model_config", {"temperature": 0.7, "max_tokens": 1024})
        tracker.end_run(exp.experiment_id, r2.run_id, status=RunStatus.COMPLETED)

        # Retrieve artifact
        art = tracker.artifact_store.get_artifact(art_id)
        assert art is not None
        assert art["content"]["temperature"] == 0.7

        # Compare runs
        comp = tracker.compare_experiment_runs(exp.experiment_id)
        assert comp["total_runs"] == 2
        assert "accuracy" in comp["metric_summary"]
        assert comp["metric_summary"]["accuracy"]["max"] == 0.94

        # Best run selection
        best_run = tracker.get_best_run(exp.experiment_id, target_metric="accuracy", higher_is_better=True)
        assert best_run is not None
        assert best_run.run_id == r2.run_id


@pytest.mark.req("AI-006")
class TestAI006EmbeddingManagement:
    """AI-006: Embedding Management & Versioning."""

    def test_embedding_registry_and_drift_detection(self):
        engine = get_embedding_engine()
        v1 = engine.registry.register_version(model_name="bge-large-en", dimensions=64, set_active=True)
        assert v1.is_active is True

        v2 = engine.registry.register_version(model_name="bge-large-en", dimensions=64, set_active=True)
        assert v2.is_active is True
        assert engine.registry.get_version(v1.version_id).is_active is False

        # Drift detector: identical distributions
        vecs_a = [[1.0, 0.0] * 32, [0.0, 1.0] * 32]
        vecs_b = [[1.0, 0.0] * 32, [0.0, 1.0] * 32]
        rep_no_drift = engine.drift_detector.detect_drift(vecs_a, vecs_b)
        assert rep_no_drift.drift_detected is False
        assert rep_no_drift.mean_cosine_shift == pytest.approx(0.0, abs=1e-3)

        # Drift detector: shifted orthogonal distributions
        vecs_c = [[0.0, 1.0] * 32, [1.0, 0.0] * 32]
        rep_drift = engine.drift_detector.detect_drift(vecs_a, vecs_c)
        assert rep_drift.mean_cosine_shift > 0.0

    def test_embedding_fusion_and_dimension_reduction(self):
        engine = get_embedding_engine()
        v_text = [1.0, 0.0, 0.5, 0.5]
        v_graph = [0.0, 1.0, 0.5, 0.5]

        # Fusion: Weighted Sum
        fused = engine.fusion.fuse([v_text, v_graph], weights=[0.5, 0.5], method=FusionMethod.WEIGHTED_SUM)
        assert len(fused) == 4
        # Norm should be approx 1.0
        norm = math.sqrt(sum(x * x for x in fused))
        assert norm == pytest.approx(1.0, rel=1e-2)

        # Dimension reduction: from 64 to 8
        large_vec = [float(i % 5) for i in range(64)]
        reduced = engine.reducer.reduce(large_vec, target_dimensions=8)
        assert len(reduced) == 8
        reduced_norm = math.sqrt(sum(x * x for x in reduced))
        assert reduced_norm == pytest.approx(1.0, rel=1e-2)


@pytest.mark.req("AI-007")
class TestAI007ProbabilisticReasoning:
    """AI-007: Probabilistic Reasoning Integration."""

    def test_uncertainty_propagation(self):
        prop = UncertaintyPropagator()
        # Conjunction: P(A & B) = 0.8 * 0.9 = 0.72
        assert prop.conjunction([0.8, 0.9]) == pytest.approx(0.72, abs=1e-3)

        # Disjunction: P(A or B) = 1 - (1-0.8)*(1-0.9) = 1 - 0.02 = 0.98
        assert prop.disjunction([0.8, 0.9]) == pytest.approx(0.98, abs=1e-3)

        # Link propagation: 0.8 * 0.75 = 0.60
        assert prop.propagate_link(0.8, 0.75) == pytest.approx(0.60, abs=1e-3)

    def test_bayesian_graph_reasoning_and_strategy(self):
        reasoner = BayesianGraphReasoner()
        # P(BugExists) prior = 0.20
        reasoner.set_prior("Bug", 0.20)
        # P(TestFails | Bug) = 0.90, P(TestFails | not Bug) = 0.05
        reasoner.add_conditional("TestFail", "Bug", p_child_given_parent=0.90, p_child_given_not_parent=0.05)

        # Evidence: TestFail = True
        # Posterior P(Bug | TestFail=True) = (0.90 * 0.20) / (0.90*0.20 + 0.05*0.80) = 0.18 / (0.18 + 0.04) = 0.18 / 0.22 = ~0.818
        posterior = reasoner.infer_posterior("Bug", evidence={"TestFail": True})
        assert posterior > 0.80
        assert posterior < 0.85

        # Query Engine with Wilson confidence interval
        engine = ProbabilisticQueryEngine(reasoner)
        q_res = engine.query("Bug", evidence={"TestFail": True})
        assert q_res["posterior_probability"] == posterior
        ci = q_res["confidence_interval_95"]
        assert ci[0] <= posterior <= ci[1]

        # Execute through StrategyRegistry
        reg = default_registry()
        assert "probabilistic" in reg.names()

        problem = ReasoningProblem(
            prompt="Infer probability of Bug given test failure",
            context={
                "target_variable": "Bug",
                "evidence": {"TestFail": True},
                "priors": {"Bug": 0.20},
                "conditionals": [
                    {"child": "TestFail", "parent": "Bug", "p_true": 0.90, "p_false": 0.05}
                ],
            },
        )
        res = reg.run("probabilistic", problem)
        assert res.strategy == "probabilistic"
        assert float(res.answer) == pytest.approx(posterior, abs=1e-3)
        assert len(res.steps) >= 3
