"""Adaptive RAG strategy plugin registry (FR-RAG-006).

Provides a plugin mechanism for registering custom RAG strategy variants
beyond the 17 built-in patterns. Strategies are registered by name and
can be selected at query time based on context signals.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol, runtime_checkable


class StrategyPhase(str, Enum):
    RETRIEVE = "retrieve"
    RERANK = "rerank"
    SYNTHESIZE = "synthesize"
    VALIDATE = "validate"


@runtime_checkable
class RAGStrategyPlugin(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def phases(self) -> list[StrategyPhase]: ...

    def should_activate(self, context: StrategyContext) -> bool: ...

    def execute(self, context: StrategyContext, prior_results: list[Any]) -> StrategyResult: ...


@dataclass
class StrategyContext:
    query: str
    canonical_ids: list[str] = field(default_factory=list)
    intent: str = ""
    domain: str = ""
    labels: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class StrategyResult:
    strategy_name: str
    phase: StrategyPhase
    contexts: list[dict[str, Any]] = field(default_factory=list)
    score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class StrategyRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, RAGStrategyPlugin] = {}

    def register(self, plugin: RAGStrategyPlugin) -> None:
        if not isinstance(plugin, RAGStrategyPlugin):
            raise TypeError(f"Plugin must implement RAGStrategyPlugin protocol, got {type(plugin).__name__}")
        if plugin.name in self._plugins:
            raise ValueError(f"Strategy '{plugin.name}' is already registered")
        self._plugins[plugin.name] = plugin

    def unregister(self, name: str) -> bool:
        return self._plugins.pop(name, None) is not None

    def get(self, name: str) -> RAGStrategyPlugin | None:
        return self._plugins.get(name)

    def list_strategies(self) -> list[dict[str, Any]]:
        return [
            {
                "name": plugin.name,
                "phases": [p.value for p in plugin.phases],
            }
            for plugin in self._plugins.values()
        ]

    def select_strategies(
        self, context: StrategyContext, *, phase: StrategyPhase | None = None,
    ) -> list[RAGStrategyPlugin]:
        candidates = []
        for plugin in self._plugins.values():
            if phase and phase not in plugin.phases:
                continue
            if plugin.should_activate(context):
                candidates.append(plugin)
        return candidates

    def execute_chain(
        self, context: StrategyContext, *, phases: list[StrategyPhase] | None = None,
    ) -> list[StrategyResult]:
        target_phases = phases or list(StrategyPhase)
        results: list[StrategyResult] = []
        prior: list[Any] = []

        for phase in target_phases:
            active = self.select_strategies(context, phase=phase)
            for plugin in active:
                result = plugin.execute(context, prior)
                result.phase = phase
                results.append(result)
                prior.append(result)

        return results

    @property
    def plugin_count(self) -> int:
        return len(self._plugins)


_GLOBAL_REGISTRY = StrategyRegistry()


def get_global_registry() -> StrategyRegistry:
    return _GLOBAL_REGISTRY


class GraphDepthStrategy:
    """Built-in strategy that adjusts retrieval depth based on query complexity."""

    @property
    def name(self) -> str:
        return "graph_depth_adaptive"

    @property
    def phases(self) -> list[StrategyPhase]:
        return [StrategyPhase.RETRIEVE]

    def should_activate(self, context: StrategyContext) -> bool:
        return len(context.query.split()) > 5 or "impact" in context.query.lower()

    def execute(self, context: StrategyContext, prior_results: list[Any]) -> StrategyResult:
        depth = 3 if len(context.query.split()) > 10 else 2
        return StrategyResult(
            strategy_name=self.name,
            phase=StrategyPhase.RETRIEVE,
            metadata={"recommended_depth": depth, "reason": "query_complexity"},
        )


class EvidenceWeightStrategy:
    """Built-in strategy that boosts results with stronger provenance evidence."""

    @property
    def name(self) -> str:
        return "evidence_weight"

    @property
    def phases(self) -> list[StrategyPhase]:
        return [StrategyPhase.RERANK]

    def should_activate(self, context: StrategyContext) -> bool:
        return any(kw in context.query.lower() for kw in ("why", "evidence", "proof", "source"))

    def execute(self, context: StrategyContext, prior_results: list[Any]) -> StrategyResult:
        return StrategyResult(
            strategy_name=self.name,
            phase=StrategyPhase.RERANK,
            metadata={"boost_factor": 1.5, "target_fields": ["evidence_key", "source_ref"]},
        )


class DomainFocusStrategy:
    """Built-in strategy that filters retrieval to a specific domain."""

    @property
    def name(self) -> str:
        return "domain_focus"

    @property
    def phases(self) -> list[StrategyPhase]:
        return [StrategyPhase.RETRIEVE, StrategyPhase.RERANK]

    def should_activate(self, context: StrategyContext) -> bool:
        return bool(context.domain)

    def execute(self, context: StrategyContext, prior_results: list[Any]) -> StrategyResult:
        return StrategyResult(
            strategy_name=self.name,
            phase=StrategyPhase.RETRIEVE,
            metadata={"domain_filter": context.domain, "strict": False},
        )


class FreshnessStrategy:
    """Built-in strategy that prioritizes recent results."""

    @property
    def name(self) -> str:
        return "freshness_boost"

    @property
    def phases(self) -> list[StrategyPhase]:
        return [StrategyPhase.RERANK]

    def should_activate(self, context: StrategyContext) -> bool:
        return any(kw in context.query.lower() for kw in ("recent", "latest", "new", "current", "today"))

    def execute(self, context: StrategyContext, prior_results: list[Any]) -> StrategyResult:
        return StrategyResult(
            strategy_name=self.name,
            phase=StrategyPhase.RERANK,
            metadata={"recency_weight": 2.0, "decay_days": 7},
        )


def register_builtin_strategies(registry: StrategyRegistry | None = None) -> StrategyRegistry:
    reg = registry or get_global_registry()
    builtins = [
        GraphDepthStrategy(),
        EvidenceWeightStrategy(),
        DomainFocusStrategy(),
        FreshnessStrategy(),
    ]
    for strategy in builtins:
        if reg.get(strategy.name) is None:
            reg.register(strategy)
    return reg
