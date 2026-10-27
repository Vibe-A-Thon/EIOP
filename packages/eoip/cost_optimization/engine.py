"""Cost & Latency Optimization engine — budget tracking, latency profiling,
compute optimization, and cost-aware model routing."""

from __future__ import annotations

import statistics
import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from collections.abc import Callable


@dataclass
class CostEvent:
    operation: str
    model: str
    tokens_in: int
    tokens_out: int
    cost_usd: float
    latency_ms: float
    timestamp: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class BudgetAlert:
    policy_name: str
    threshold_pct: float
    current_pct: float
    message: str
    triggered_at: float = field(default_factory=time.time)


class BudgetPolicy:
    def __init__(self, name: str, daily_limit_usd: float = 100.0,
                 hourly_limit_usd: float = 20.0,
                 alert_thresholds: list[float] | None = None) -> None:
        self.name = name
        self.daily_limit_usd = daily_limit_usd
        self.hourly_limit_usd = hourly_limit_usd
        self.alert_thresholds = alert_thresholds or [0.5, 0.75, 0.9, 1.0]

    def check(self, spent_daily: float, spent_hourly: float) -> list[BudgetAlert]:
        alerts: list[BudgetAlert] = []
        daily_pct = spent_daily / self.daily_limit_usd if self.daily_limit_usd > 0 else 0
        hourly_pct = spent_hourly / self.hourly_limit_usd if self.hourly_limit_usd > 0 else 0
        for threshold in self.alert_thresholds:
            if daily_pct >= threshold:
                alerts.append(BudgetAlert(
                    self.name, threshold, daily_pct,
                    f"Daily budget at {daily_pct:.0%} (${spent_daily:.2f}/${self.daily_limit_usd:.2f})",
                ))
                break
        for threshold in self.alert_thresholds:
            if hourly_pct >= threshold:
                alerts.append(BudgetAlert(
                    self.name, threshold, hourly_pct,
                    f"Hourly budget at {hourly_pct:.0%} (${spent_hourly:.2f}/${self.hourly_limit_usd:.2f})",
                ))
                break
        return alerts


class CostTracker:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._events: list[CostEvent] = []
        self._by_model: dict[str, list[CostEvent]] = defaultdict(list)
        self._by_operation: dict[str, list[CostEvent]] = defaultdict(list)
        self._policies: list[BudgetPolicy] = []

    def record(self, event: CostEvent) -> list[BudgetAlert]:
        with self._lock:
            self._events.append(event)
            self._by_model[event.model].append(event)
            self._by_operation[event.operation].append(event)
        return self._check_budgets()

    def add_policy(self, policy: BudgetPolicy) -> None:
        self._policies.append(policy)

    def _check_budgets(self) -> list[BudgetAlert]:
        now = time.time()
        day_start = now - 86400
        hour_start = now - 3600
        with self._lock:
            daily_spend = sum(e.cost_usd for e in self._events if e.timestamp >= day_start)
            hourly_spend = sum(e.cost_usd for e in self._events if e.timestamp >= hour_start)
        all_alerts: list[BudgetAlert] = []
        for policy in self._policies:
            all_alerts.extend(policy.check(daily_spend, hourly_spend))
        return all_alerts

    def total_cost(self, since: float | None = None) -> float:
        with self._lock:
            events = self._events if since is None else [e for e in self._events if e.timestamp >= since]
            return sum(e.cost_usd for e in events)

    def cost_by_model(self) -> dict[str, float]:
        with self._lock:
            return {m: sum(e.cost_usd for e in evts) for m, evts in self._by_model.items()}

    def cost_by_operation(self) -> dict[str, float]:
        with self._lock:
            return {op: sum(e.cost_usd for e in evts) for op, evts in self._by_operation.items()}

    def stats(self) -> dict[str, Any]:
        with self._lock:
            total = sum(e.cost_usd for e in self._events)
            total_tokens = sum(e.tokens_in + e.tokens_out for e in self._events)
            return {
                "total_events": len(self._events),
                "total_cost_usd": total,
                "total_tokens": total_tokens,
                "models_tracked": len(self._by_model),
            }


@dataclass
class LatencyProfile:
    operation: str
    p50_ms: float
    p90_ms: float
    p99_ms: float
    mean_ms: float
    count: int


class LatencyProfiler:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._latencies: dict[str, list[float]] = defaultdict(list)

    def record(self, operation: str, latency_ms: float) -> None:
        with self._lock:
            self._latencies[operation].append(latency_ms)

    def profile(self, operation: str) -> LatencyProfile | None:
        with self._lock:
            data = self._latencies.get(operation, [])
            if not data:
                return None
            sorted_data = sorted(data)
            n = len(sorted_data)
            return LatencyProfile(
                operation=operation,
                p50_ms=sorted_data[n // 2],
                p90_ms=sorted_data[int(n * 0.9)],
                p99_ms=sorted_data[int(n * 0.99)],
                mean_ms=statistics.mean(sorted_data),
                count=n,
            )

    def all_profiles(self) -> list[LatencyProfile]:
        profiles: list[LatencyProfile] = []
        for op in list(self._latencies.keys()):
            p = self.profile(op)
            if p:
                profiles.append(p)
        return profiles

    def slow_operations(self, threshold_ms: float = 1000.0) -> list[LatencyProfile]:
        return [p for p in self.all_profiles() if p.p90_ms > threshold_ms]


@dataclass
class OptimizationRecommendation:
    category: str
    description: str
    estimated_savings_pct: float
    priority: str = "medium"


class ComputeOptimizer:
    def __init__(self, cost_tracker: CostTracker, latency_profiler: LatencyProfiler) -> None:
        self._cost = cost_tracker
        self._latency = latency_profiler
        self._model_capabilities: dict[str, dict[str, Any]] = {
            "gpt-4": {"quality": 0.95, "cost_per_1k": 0.03, "speed": 0.3},
            "gpt-3.5-turbo": {"quality": 0.80, "cost_per_1k": 0.001, "speed": 0.9},
            "claude-sonnet": {"quality": 0.92, "cost_per_1k": 0.003, "speed": 0.7},
            "claude-haiku": {"quality": 0.85, "cost_per_1k": 0.00025, "speed": 0.95},
        }

    def recommend_model(self, operation: str, min_quality: float = 0.8) -> str:
        candidates = [(n, c) for n, c in self._model_capabilities.items() if c["quality"] >= min_quality]
        if not candidates:
            return "gpt-4"
        candidates.sort(key=lambda x: x[1]["cost_per_1k"])
        return candidates[0][0]

    def analyze(self) -> list[OptimizationRecommendation]:
        recs: list[OptimizationRecommendation] = []
        cost_by_model = self._cost.cost_by_model()
        total = sum(cost_by_model.values()) or 1.0
        for model, cost in cost_by_model.items():
            pct = cost / total
            if pct > 0.5 and model in ("gpt-4",):
                recs.append(OptimizationRecommendation(
                    "model_downgrade",
                    f"{model} accounts for {pct:.0%} of costs",
                    estimated_savings_pct=pct * 0.6, priority="high",
                ))
        for profile in self._latency.slow_operations():
            recs.append(OptimizationRecommendation(
                "latency_optimization",
                f"{profile.operation} p90={profile.p90_ms:.0f}ms",
                estimated_savings_pct=0.0,
                priority="high" if profile.p90_ms > 5000 else "medium",
            ))
        return recs

    def stats(self) -> dict[str, Any]:
        return {"registered_models": len(self._model_capabilities)}


class CostLatencyEngine:
    def __init__(self) -> None:
        self._cost_tracker = CostTracker()
        self._latency_profiler = LatencyProfiler()
        self._optimizer = ComputeOptimizer(self._cost_tracker, self._latency_profiler)

    @property
    def cost_tracker(self) -> CostTracker:
        return self._cost_tracker

    @property
    def latency_profiler(self) -> LatencyProfiler:
        return self._latency_profiler

    @property
    def optimizer(self) -> ComputeOptimizer:
        return self._optimizer

    def record_operation(self, operation: str, model: str,
                         tokens_in: int, tokens_out: int,
                         cost_usd: float, latency_ms: float,
                         **metadata: Any) -> list[BudgetAlert]:
        event = CostEvent(operation=operation, model=model,
                          tokens_in=tokens_in, tokens_out=tokens_out,
                          cost_usd=cost_usd, latency_ms=latency_ms, metadata=metadata)
        alerts = self._cost_tracker.record(event)
        self._latency_profiler.record(operation, latency_ms)
        return alerts

    def set_budget(self, name: str, daily_limit: float = 100.0,
                   hourly_limit: float = 20.0) -> None:
        self._cost_tracker.add_policy(BudgetPolicy(name, daily_limit, hourly_limit))

    def recommend_model(self, operation: str, min_quality: float = 0.8) -> str:
        return self._optimizer.recommend_model(operation, min_quality)

    def get_recommendations(self) -> list[OptimizationRecommendation]:
        return self._optimizer.analyze()

    def stats(self) -> dict[str, Any]:
        return {
            "engine": "cost_latency_optimization",
            "cost": self._cost_tracker.stats(),
            "latency_profiles": len(self._latency_profiler.all_profiles()),
            "optimizer": self._optimizer.stats(),
        }


_instance: CostLatencyEngine | None = None
_lock = threading.Lock()


def get_cost_engine() -> CostLatencyEngine:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = CostLatencyEngine()
    return _instance
