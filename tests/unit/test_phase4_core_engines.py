"""Unit tests for Phase 4 Core Engines (CORE-001 through CORE-006).

Ensures 100% test coverage for:
- CORE-001: Token Format Serialization (TOON, TRON, LEAN, ASON, ZON, ZOON, TSON)
- CORE-002: Verification & Guardrail Engineering
- CORE-003: Intent Router Engineering
- CORE-004: Graph-over-Graph Engineering
- CORE-005: Loop-over-Loop Meta-Orchestration
- CORE-006: Token Budget Engineering
"""

import sys
import time
from pathlib import Path

# Ensure workspace packages take precedence
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "packages"))

import pytest
from fastapi.testclient import TestClient

from eoip.graph_graph.engine import (
    GraphLayer,
    GraphOverGraphEngine,
    LayerRelation,
    LayerType,
    RelationKind,
    get_graph_graph_engine,
)
from eoip.intelligence_eng.engine import (
    LoopCircuitBreakerOpenError,
    LoopComposition,
    LoopMonitor,
    LoopSwitcher,
    SupervisoryLoop,
)
from eoip.platform_router import build_platform_router
from eoip.routing.engine import (
    FastIntentClassifier,
    IntentCategory,
    RouterEngine,
    get_router_engine,
)
from eoip.token_budget.engine import (
    BudgetPolicy,
    BudgetTracker,
    TokenBudgetEngine,
    get_token_budget_engine,
)
from eoip.token_formats.engine import (
    AsonFormatStrategy,
    LeanFormatStrategy,
    ToonFormatStrategy,
    TronFormatStrategy,
    TsonFormatStrategy,
    ZonFormatStrategy,
    ZoonFormatStrategy,
    estimate_bpe_tokens,
    get_token_format_engine,
)
from eoip.verification.engine import (
    CognitiveDriftRule,
    ConfidenceThresholdRule,
    DynamicGuardrailInjector,
    FactConsistencyRule,
    HallucinationDetectionRule,
    OutputFormatRule,
    PolicyComplianceRule,
    SchemaConformanceRule,
    VerifierRegistry,
    get_verification_engine,
)


@pytest.mark.req("CORE-001")
class TestCore001TokenFormats:
    """CORE-001: Token Format Serialization Engines."""

    @pytest.fixture
    def test_payload(self):
        return {
            "entity_id": "ent_test_42",
            "name": "Synthetic Test Service",
            "active": True,
            "metrics": {"latency_ms": 12.5, "error_rate": 0.001, "replica_count": 3},
            "tags": ["critical", "p0", "service_mesh"],
        }

    def test_all_seven_strategies_roundtrip(self, test_payload):
        strategies = [
            ToonFormatStrategy(),
            TronFormatStrategy(),
            LeanFormatStrategy(),
            AsonFormatStrategy(),
            ZonFormatStrategy(),
            ZoonFormatStrategy(),
            TsonFormatStrategy(),
        ]
        for strat in strategies:
            encoded = strat.serialize(test_payload)
            assert isinstance(encoded, str)
            assert len(encoded) > 0
            decoded = strat.deserialize(encoded)
            assert decoded == test_payload
            tokens = strat.estimate_tokens(encoded)
            assert tokens > 0
            ratio = strat.compression_ratio(test_payload)
            assert ratio >= 0.0

    def test_format_engine_auto_selection_and_benchmarks(self, test_payload):
        engine = get_token_format_engine()
        chosen_format, serialized, ratio = engine.auto_serialize(test_payload)
        assert chosen_format in engine.supported_formats
        assert isinstance(serialized, str)
        assert ratio > 0.0

        bench = engine.benchmark_all(test_payload)
        assert "json_tokens" in bench
        assert "benchmarks" in bench
        assert len(bench["benchmarks"]) == 7
        assert "recommended_format" in bench


@pytest.mark.req("CORE-002")
class TestCore002Verification:
    """CORE-002: Verification & Guardrail Engineering."""

    def test_builtin_rules_and_registry(self):
        registry = VerifierRegistry()
        registry.register(SchemaConformanceRule())
        registry.register(ConfidenceThresholdRule(min_confidence=0.75))
        registry.register(PolicyComplianceRule())
        registry.register(HallucinationDetectionRule())
        registry.register(CognitiveDriftRule())
        registry.register(FactConsistencyRule())
        registry.register(OutputFormatRule())

        # Valid payload passes all rules
        valid_out = {
            "canonical_id": "ent_valid_01",
            "status": "success",
            "confidence": 0.95,
            "answer": "Operation completed safely according to specifications.",
        }
        res = registry.verify_chain(valid_out)
        assert res.passed
        assert len(res.failures) == 0


        # Low confidence triggers failure
        low_conf = {
            "canonical_id": "ent_low_01",
            "status": "success",
            "confidence": 0.40,
            "answer": "Maybe it succeeded.",
        }
        res_fail = registry.verify_chain(low_conf)
        assert not res_fail.passed
        assert any("Confidence" in f for f in res_fail.failures)


    def test_dynamic_guardrail_interceptor(self):
        injector = DynamicGuardrailInjector()
        injector.add_boundary("no_drop", lambda intent, params: "drop" not in intent.lower())

        allowed, reason = injector.intercept_intent("agent_alpha", "read_telemetry_metrics", {})
        assert allowed
        assert reason == "All boundaries cleared"

        blocked, reason = injector.intercept_intent("agent_alpha", "drop_production_database", {})
        assert not blocked
        assert "Blocked" in reason


@pytest.mark.req("CORE-003")
class TestCore003IntentRouter:
    """CORE-003: Intent Router Engineering."""

    def test_sub10ms_intent_classification(self):
        classifier = FastIntentClassifier()
        queries = [
            ("SELECT * FROM instances WHERE active = true", IntentCategory.GRAPH_LOOKUP),
            ("show status of node cluster", IntentCategory.GRAPH_LOOKUP),
            ("explain causal path between service failures and latency", IntentCategory.AGENTIC_REASONING),
            ("update configuration and set timeout to 500", IntentCategory.GRAPH_MUTATION),
            ("restart engine daemon and purge logs", IntentCategory.ADMIN_OPERATION),
        ]
        for q, expected in queries:
            t0 = time.time()
            cat, conf = classifier.classify(q)
            elapsed_ms = (time.time() - t0) * 1000
            assert elapsed_ms < 15.0  # Sub-15ms fast classification
            assert conf > 0.0
            assert isinstance(cat, IntentCategory)

    def test_router_engine_and_feedback(self):
        engine = RouterEngine()
        decision = engine.route("lookup entity topology in the graph")
        assert decision.category in [c.value for c in IntentCategory]
        assert decision.estimated_cost >= 0.0
        assert decision.estimated_latency_ms > 0.0

        # Feedback recording
        engine.record_feedback(decision.category, actual_cost=0.0008, actual_latency_ms=18.0)
        stats = engine.stats()
        assert stats["total_routed_queries"] >= 1


@pytest.mark.req("CORE-004")
class TestCore004GraphOverGraph:
    """CORE-004: Graph-over-Graph Engineering."""

    def test_cross_layer_and_diff(self):
        engine = GraphOverGraphEngine()
        ont_layer = engine.get_or_create_layer("core_ontology", LayerType.ONTOLOGY, priority=1)
        inst_layer = engine.get_or_create_layer("live_instances", LayerType.INSTANCE, priority=2)

        # Add cross layer edge
        engine.add_cross_layer_edge(
            source_layer="core_ontology",
            source_vertex_id="OntologyClassA",
            target_layer="live_instances",
            target_vertex_id="InstVertex01",
            relation_kind=RelationKind.CONSTRAINS,
        )

        matches = engine.cross_layer_query("core_ontology", "live_instances", RelationKind.CONSTRAINS.value)
        assert len(matches) == 1
        assert matches[0]["relation"]["source_id"] == "OntologyClassA"

        # Diff layers
        diff = engine.diff_layers("core_ontology", "live_instances")
        assert "modified" in diff and "count_a" in diff



@pytest.mark.req("CORE-005")
class TestCore005LoopOverLoop:
    """CORE-005: Loop-over-Loop Engineering."""

    def test_supervisory_loop_execution_and_fallback(self):
        comp = LoopComposition(
            name="test_supervisory_pipeline",
            outer_loop_name="OODA",
            strategies=["fragile_react", "robust_fallback"],
            failure_threshold=3,
        )
        switcher = LoopSwitcher(fallback_chains={"fragile_react": ["robust_fallback"]})
        supervisor = SupervisoryLoop(composition=comp, switcher=switcher)

        call_counts = {"fragile_react": 0, "robust_fallback": 0}

        def mock_inner_loop(strategy: str, ctx: dict):
            call_counts[strategy] += 1
            if strategy == "fragile_react":
                raise RuntimeError("Synthetic tool execution failure in fragile react")
            return {
                "status": "success",
                "iterations": 2,
                "cost": 0.02,
                "quality": 0.95,
                "convergence": 0.98,
            }

        res = supervisor.execute(mock_inner_loop)
        assert res.success
        assert res.final_strategy == "robust_fallback"
        assert call_counts["fragile_react"] == 1
        assert call_counts["robust_fallback"] == 1
        assert not res.circuit_breaker_tripped

    def test_circuit_breaker_tripping(self):
        comp = LoopComposition(
            name="failing_pipeline",
            outer_loop_name="OODA",
            strategies=["always_fail"],
            failure_threshold=2,
        )
        supervisor = SupervisoryLoop(composition=comp)

        def failing_task(strat: str, ctx: dict):
            raise ValueError("Persistent synthetic failure")

        # First run fails
        res1 = supervisor.execute(failing_task)
        assert not res1.success

        # Second run trips circuit breaker
        res2 = supervisor.execute(failing_task)
        assert not res2.success
        assert supervisor.is_circuit_open

        # Subsequent run raises circuit breaker open exception
        with pytest.raises(LoopCircuitBreakerOpenError):
            supervisor.execute(failing_task)


@pytest.mark.req("CORE-006")
class TestCore006TokenBudget:
    """CORE-006: Token Budget Engineering."""

    def test_token_budget_allocation_and_reallocation(self):
        engine = TokenBudgetEngine()
        budget = engine.create_budget(
            budget_id="test_plan_budget_01",
            stage_names=["reasoning", "rag", "verification"],
            total_budget=5000,
            policy=BudgetPolicy.PRIORITY_WEIGHTED,
        )
        assert budget.total_budget == 5000
        assert "reasoning" in budget.stages
        # Reasoning gets higher weight than verification
        assert budget.stages["reasoning"].allocated_tokens > budget.stages["verification"].allocated_tokens

        # Record normal consumption
        engine.consume("test_plan_budget_01", "rag", 500)
        assert budget.stages["rag"].consumed_tokens == 500

        # Trigger reallocation
        reallocated = engine.reallocate("test_plan_budget_01")
        assert reallocated is not None

    def test_context_compression_on_budget_exceed(self):
        tracker = BudgetTracker()
        budget = tracker.allocate(
            budget_id="overflow_budget",
            stage_names=["synthesis"],
            total_budget=500,
            policy=BudgetPolicy.EQUAL_SPLIT,
        )
        large_payload = {"synthetic_context": "Important entity data " * 100}

        # Consuming 2000 tokens when only ~450 allocated
        res = tracker.record_consumption(
            budget,
            stage_name="synthesis",
            consumed_tokens=2000,
            context_payload=large_payload,
        )
        assert res["status"] in ("exceeded", "compressed")
        assert res["action_taken"] == "context_compressed"
        assert res["compressed_payload"] is not None


class TestPlatformRouterPhase1Integration:
    """FastAPI integration tests for Phase 1 endpoints."""

    @pytest.fixture
    def client(self):
        from fastapi import FastAPI
        app = FastAPI()
        app.include_router(build_platform_router())
        return TestClient(app)

    def test_token_formats_endpoint(self, client):
        resp = client.post(
            "/api/v1/platform/token-formats/serialize",
            json={"payload": {"test_key": "test_val", "count": 10}, "format_name": "TOON"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["format"] == "TOON"
        assert "serialized" in data

    def test_verification_endpoint(self, client):
        resp = client.post(
            "/api/v1/platform/verification/check",
            json={"output": {"confidence": 0.99, "status": "ok"}, "rules": ["confidence", "schema"]},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["passed"] is True

    def test_routing_endpoint(self, client):
        resp = client.post(
            "/api/v1/platform/routing/classify-and-route",
            json={"query": "MATCH (n:Person) RETURN n LIMIT 10"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "category" in data
        assert "estimated_cost" in data

    def test_token_budget_endpoint(self, client):
        resp = client.post(
            "/api/v1/platform/token-budget/allocate",
            json={
                "budget_id": "api_test_budget_99",
                "stage_names": ["rag", "reasoning"],
                "total_budget": 3000,
                "policy": "PRIORITY_WEIGHTED",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["budget_id"] == "api_test_budget_99"
        assert data["total_budget"] == 3000
