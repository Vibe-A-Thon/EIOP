"""Tests for adaptive RAG strategy plugin registry (FR-RAG-006)."""

from eoip.retrieval.strategy_registry import (
    DomainFocusStrategy,
    EvidenceWeightStrategy,
    FreshnessStrategy,
    GraphDepthStrategy,
    RAGStrategyPlugin,
    StrategyContext,
    StrategyPhase,
    StrategyRegistry,
    StrategyResult,
    register_builtin_strategies,
)
import pytest


def test_registry_register_and_list():
    reg = StrategyRegistry()
    reg.register(GraphDepthStrategy())
    strategies = reg.list_strategies()
    assert len(strategies) == 1
    assert strategies[0]["name"] == "graph_depth_adaptive"
    assert "retrieve" in strategies[0]["phases"]


def test_registry_duplicate_raises():
    reg = StrategyRegistry()
    reg.register(GraphDepthStrategy())
    with pytest.raises(ValueError, match="already registered"):
        reg.register(GraphDepthStrategy())


def test_registry_unregister():
    reg = StrategyRegistry()
    reg.register(GraphDepthStrategy())
    assert reg.plugin_count == 1
    assert reg.unregister("graph_depth_adaptive")
    assert reg.plugin_count == 0
    assert not reg.unregister("nonexistent")


def test_registry_get():
    reg = StrategyRegistry()
    reg.register(GraphDepthStrategy())
    assert reg.get("graph_depth_adaptive") is not None
    assert reg.get("nonexistent") is None


def test_graph_depth_activates_on_long_query():
    strategy = GraphDepthStrategy()
    short_ctx = StrategyContext(query="find item")
    long_ctx = StrategyContext(query="what is the full impact of changing the payment processing module on downstream services")
    assert not strategy.should_activate(short_ctx)
    assert strategy.should_activate(long_ctx)


def test_graph_depth_activates_on_impact():
    strategy = GraphDepthStrategy()
    ctx = StrategyContext(query="impact analysis")
    assert strategy.should_activate(ctx)


def test_evidence_weight_activates_on_keywords():
    strategy = EvidenceWeightStrategy()
    ctx_yes = StrategyContext(query="why did this change?")
    ctx_no = StrategyContext(query="show me the list")
    assert strategy.should_activate(ctx_yes)
    assert not strategy.should_activate(ctx_no)


def test_domain_focus_activates_with_domain():
    strategy = DomainFocusStrategy()
    ctx_yes = StrategyContext(query="find items", domain="WORK")
    ctx_no = StrategyContext(query="find items")
    assert strategy.should_activate(ctx_yes)
    assert not strategy.should_activate(ctx_no)


def test_freshness_activates_on_recency():
    strategy = FreshnessStrategy()
    ctx_yes = StrategyContext(query="show recent changes")
    ctx_no = StrategyContext(query="show all changes")
    assert strategy.should_activate(ctx_yes)
    assert not strategy.should_activate(ctx_no)


def test_select_strategies_filters_by_phase():
    reg = StrategyRegistry()
    reg.register(GraphDepthStrategy())
    reg.register(EvidenceWeightStrategy())
    ctx = StrategyContext(query="why did this impact analysis fail")
    retrieve = reg.select_strategies(ctx, phase=StrategyPhase.RETRIEVE)
    rerank = reg.select_strategies(ctx, phase=StrategyPhase.RERANK)
    assert any(s.name == "graph_depth_adaptive" for s in retrieve)
    assert any(s.name == "evidence_weight" for s in rerank)


def test_execute_chain():
    reg = StrategyRegistry()
    reg.register(GraphDepthStrategy())
    reg.register(EvidenceWeightStrategy())
    ctx = StrategyContext(query="why does this impact the payment module and what evidence exists")
    results = reg.execute_chain(ctx)
    assert len(results) >= 2
    phases_seen = {r.phase for r in results}
    assert StrategyPhase.RETRIEVE in phases_seen
    assert StrategyPhase.RERANK in phases_seen


def test_execute_chain_specific_phases():
    reg = StrategyRegistry()
    reg.register(GraphDepthStrategy())
    reg.register(EvidenceWeightStrategy())
    ctx = StrategyContext(query="why does this impact analysis work")
    results = reg.execute_chain(ctx, phases=[StrategyPhase.RETRIEVE])
    for r in results:
        assert r.phase == StrategyPhase.RETRIEVE


def test_register_builtin_strategies():
    reg = StrategyRegistry()
    result = register_builtin_strategies(reg)
    assert result is reg
    assert reg.plugin_count == 4
    names = {s["name"] for s in reg.list_strategies()}
    assert names == {"graph_depth_adaptive", "evidence_weight", "domain_focus", "freshness_boost"}


def test_register_builtin_idempotent():
    reg = StrategyRegistry()
    register_builtin_strategies(reg)
    register_builtin_strategies(reg)
    assert reg.plugin_count == 4


def test_custom_plugin():
    class MyPlugin:
        @property
        def name(self) -> str:
            return "custom_test"

        @property
        def phases(self):
            return [StrategyPhase.SYNTHESIZE]

        def should_activate(self, context):
            return True

        def execute(self, context, prior_results):
            return StrategyResult(strategy_name=self.name, phase=StrategyPhase.SYNTHESIZE, score=0.9)

    reg = StrategyRegistry()
    reg.register(MyPlugin())
    ctx = StrategyContext(query="test")
    selected = reg.select_strategies(ctx, phase=StrategyPhase.SYNTHESIZE)
    assert len(selected) == 1
    result = selected[0].execute(ctx, [])
    assert result.score == 0.9


def test_strategy_result_fields():
    result = StrategyResult(
        strategy_name="test",
        phase=StrategyPhase.VALIDATE,
        contexts=[{"id": "1"}],
        score=0.75,
        metadata={"key": "value"},
    )
    assert result.strategy_name == "test"
    assert result.phase == StrategyPhase.VALIDATE
    assert len(result.contexts) == 1
    assert result.score == 0.75
