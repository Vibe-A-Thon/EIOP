"""Token Budget Engineering Engine (CORE-006).

Dynamic token allocation across cognitive pipeline stages:
- Total token budget distribution across plan stages
- 4 allocation strategies: EQUAL_SPLIT, PROPORTIONAL, PRIORITY_WEIGHTED, ADAPTIVE
- Real-time consumption tracking and reallocation
- Automatic context compression triggers on budget overflow
"""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from eoip.token_formats.engine import get_token_format_engine

logger = logging.getLogger("eoip.token_budget.engine")


class BudgetPolicy(str, Enum):
    EQUAL_SPLIT = "EQUAL_SPLIT"
    PROPORTIONAL = "PROPORTIONAL"
    PRIORITY_WEIGHTED = "PRIORITY_WEIGHTED"
    ADAPTIVE = "ADAPTIVE"


@dataclass
class StageBudget:
    """Budget and consumption state for a single pipeline stage."""

    stage_name: str
    allocated_tokens: int
    consumed_tokens: int = 0
    priority_weight: float = 1.0
    status: str = "within_budget"  # "within_budget", "warning", "exceeded", "compressed"
    compression_triggered: bool = False
    alerts: list[str] = field(default_factory=list)

    @property
    def remaining_tokens(self) -> int:
        return max(0, self.allocated_tokens - self.consumed_tokens)

    @property
    def utilization_ratio(self) -> float:
        if self.allocated_tokens <= 0:
            return 1.0 if self.consumed_tokens > 0 else 0.0
        return self.consumed_tokens / self.allocated_tokens

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage_name": self.stage_name,
            "allocated_tokens": self.allocated_tokens,
            "consumed_tokens": self.consumed_tokens,
            "remaining_tokens": self.remaining_tokens,
            "utilization_ratio": round(self.utilization_ratio, 3),
            "priority_weight": self.priority_weight,
            "status": self.status,
            "compression_triggered": self.compression_triggered,
            "alerts": self.alerts,
        }


@dataclass
class TokenBudget:
    """Total and stage-level token budget for a cognitive plan or request."""

    budget_id: str
    total_budget: int
    policy: BudgetPolicy
    stages: dict[str, StageBudget] = field(default_factory=dict)
    reserve_tokens: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

    @property
    def total_consumed(self) -> int:
        return sum(s.consumed_tokens for s in self.stages.values())

    @property
    def total_remaining(self) -> int:
        return max(0, self.total_budget - self.total_consumed)

    def to_dict(self) -> dict[str, Any]:
        return {
            "budget_id": self.budget_id,
            "total_budget": self.total_budget,
            "total_consumed": self.total_consumed,
            "total_remaining": self.total_remaining,
            "policy": self.policy.value,
            "reserve_tokens": self.reserve_tokens,
            "stages": {name: stage.to_dict() for name, stage in self.stages.items()},
            "metadata": self.metadata,
        }


class BudgetTracker:
    """Manages allocation, tracking, reallocation, and compression triggers."""

    def __init__(self, warning_threshold: float = 0.85, reserve_percent: float = 0.1) -> None:
        self.warning_threshold = warning_threshold
        self.reserve_percent = reserve_percent
        self._format_engine = get_token_format_engine()

    def allocate(
        self,
        budget_id: str,
        stage_names: list[str],
        total_budget: int,
        policy: BudgetPolicy = BudgetPolicy.PRIORITY_WEIGHTED,
        weights: dict[str, float] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> TokenBudget:
        if not stage_names:
            stage_names = ["default"]

        reserve = int(total_budget * self.reserve_percent) if total_budget > 100 else 0
        distributable = max(0, total_budget - reserve)
        stage_weights = weights or {}

        # Default weights if not specified (reasoning gets more, simple lookups get less)
        default_stage_weights: dict[str, float] = {
            "reasoning": 3.0,
            "agentic_reasoning": 3.0,
            "synthesis": 2.5,
            "multi_step_rag": 2.0,
            "rag": 1.5,
            "graph_lookup": 1.0,
            "verification": 1.0,
            "template_fill": 0.5,
        }

        stages: dict[str, StageBudget] = {}
        n = len(stage_names)

        if policy == BudgetPolicy.EQUAL_SPLIT:
            per_stage = distributable // n if n > 0 else distributable
            for name in stage_names:
                stages[name] = StageBudget(stage_name=name, allocated_tokens=per_stage)

        elif policy in (BudgetPolicy.PRIORITY_WEIGHTED, BudgetPolicy.PROPORTIONAL):
            total_w = sum(stage_weights.get(s, default_stage_weights.get(s, 1.0)) for s in stage_names)
            total_w = total_w if total_w > 0 else float(n)
            for name in stage_names:
                w = stage_weights.get(name, default_stage_weights.get(name, 1.0))
                alloc = int((w / total_w) * distributable)
                stages[name] = StageBudget(stage_name=name, allocated_tokens=alloc, priority_weight=w)

        elif policy == BudgetPolicy.ADAPTIVE:
            # Adaptive reserves 20% in reserve buffer, weights rest dynamically
            adaptive_reserve = int(total_budget * 0.20)
            distributable = max(0, total_budget - adaptive_reserve)
            reserve = adaptive_reserve
            total_w = sum(stage_weights.get(s, default_stage_weights.get(s, 1.0)) for s in stage_names)
            total_w = total_w if total_w > 0 else float(n)
            for name in stage_names:
                w = stage_weights.get(name, default_stage_weights.get(name, 1.0))
                alloc = int((w / total_w) * distributable)
                stages[name] = StageBudget(stage_name=name, allocated_tokens=alloc, priority_weight=w)

        return TokenBudget(
            budget_id=budget_id,
            total_budget=total_budget,
            policy=policy,
            stages=stages,
            reserve_tokens=reserve,
            metadata=metadata or {},
        )

    def record_consumption(
        self,
        budget: TokenBudget,
        stage_name: str,
        consumed_tokens: int,
        context_payload: Any = None,
    ) -> dict[str, Any]:
        """Record token usage for a stage, triggering warnings or compression if exceeded."""
        if stage_name not in budget.stages:
            budget.stages[stage_name] = StageBudget(
                stage_name=stage_name,
                allocated_tokens=budget.reserve_tokens // 2 or 500,
            )

        stage = budget.stages[stage_name]
        stage.consumed_tokens += consumed_tokens
        res: dict[str, Any] = {
            "stage_name": stage_name,
            "consumed": stage.consumed_tokens,
            "allocated": stage.allocated_tokens,
            "status": "within_budget",
            "action_taken": None,
            "compressed_payload": None,
        }

        # Check budget thresholds
        if stage.consumed_tokens > stage.allocated_tokens:
            excess = stage.consumed_tokens - stage.allocated_tokens
            stage.status = "exceeded"
            stage.alerts.append(f"Exceeded by {excess} tokens")
            res["status"] = "exceeded"
            res["excess_tokens"] = excess

            # Attempt context compression if payload provided
            if context_payload is not None:
                compressed_res = self.trigger_compression(context_payload, excess)
                stage.compression_triggered = True
                stage.status = "compressed"
                stage.alerts.append(f"Triggered context compression: saved {compressed_res.get('tokens_saved', 0)} tokens")
                res["action_taken"] = "context_compressed"
                res["compressed_payload"] = compressed_res.get("compressed_payload")
                res["tokens_saved"] = compressed_res.get("tokens_saved", 0)
            else:
                # Borrow from reserve if available
                if budget.reserve_tokens >= excess:
                    budget.reserve_tokens -= excess
                    stage.allocated_tokens += excess
                    stage.status = "within_budget"
                    res["action_taken"] = f"borrowed_{excess}_from_reserve"
                    stage.alerts.append(f"Allocated {excess} tokens from reserve buffer")
        elif stage.utilization_ratio >= self.warning_threshold:
            stage.status = "warning"
            stage.alerts.append(f"Approaching limit: {stage.utilization_ratio:.1%} utilized")
            res["status"] = "warning"

        return res

    def reallocate(self, budget: TokenBudget) -> TokenBudget:
        """Reclaim unused tokens from completed stages and reallocate to active/exceeded stages."""
        surplus = 0
        active_stages: list[StageBudget] = []

        for stage in budget.stages.values():
            if stage.status in ("within_budget", "warning") and stage.consumed_tokens > 0:
                # Stage finished under budget
                surplus += stage.remaining_tokens
                stage.allocated_tokens = stage.consumed_tokens
            elif stage.status in ("exceeded", "compressed"):
                active_stages.append(stage)
            elif stage.consumed_tokens == 0:
                active_stages.append(stage)

        total_pool = surplus + budget.reserve_tokens
        if active_stages and total_pool > 0:
            total_weight = sum(s.priority_weight for s in active_stages) or len(active_stages)
            for s in active_stages:
                share = int((s.priority_weight / total_weight) * total_pool)
                s.allocated_tokens += share
                if s.consumed_tokens <= s.allocated_tokens:
                    s.status = "within_budget"
            budget.reserve_tokens = 0

        return budget

    def trigger_compression(self, payload: Any, excess_tokens: int) -> dict[str, Any]:
        """Compress payload using token-efficient serialization engine."""
        try:
            chosen_format, serialized_str, ratio = self._format_engine.auto_serialize(payload)
            est_tokens = self._format_engine.estimate_tokens(serialized_str)
            return {
                "format": chosen_format,
                "compressed_payload": serialized_str,
                "tokens_saved": excess_tokens,
                "compression_ratio": ratio,
                "estimated_tokens": est_tokens,
            }
        except Exception as exc:
            logger.warning("Token compression failed: %s", exc)
            return {
                "format": "RAW",
                "compressed_payload": str(payload),
                "tokens_saved": 0,
                "error": str(exc),
            }


class TokenBudgetEngine:
    """Thread-safe centralized token budget engine."""

    def __init__(self) -> None:
        self._tracker = BudgetTracker()
        self._budgets: dict[str, TokenBudget] = {}
        self._lock = threading.Lock()

    def create_budget(
        self,
        budget_id: str,
        stage_names: list[str],
        total_budget: int,
        policy: BudgetPolicy = BudgetPolicy.PRIORITY_WEIGHTED,
        weights: dict[str, float] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> TokenBudget:
        with self._lock:
            budget = self._tracker.allocate(
                budget_id=budget_id,
                stage_names=stage_names,
                total_budget=total_budget,
                policy=policy,
                weights=weights,
                metadata=metadata,
            )
            self._budgets[budget_id] = budget
            return budget

    def get_budget(self, budget_id: str) -> TokenBudget | None:
        with self._lock:
            return self._budgets.get(budget_id)

    def consume(
        self,
        budget_id: str,
        stage_name: str,
        tokens: int,
        context_payload: Any = None,
    ) -> dict[str, Any]:
        with self._lock:
            budget = self._budgets.get(budget_id)
            if not budget:
                # Auto-create if not present
                budget = self._tracker.allocate(budget_id, [stage_name], 4000)
                self._budgets[budget_id] = budget
            return self._tracker.record_consumption(budget, stage_name, tokens, context_payload)

    def reallocate(self, budget_id: str) -> TokenBudget | None:
        with self._lock:
            budget = self._budgets.get(budget_id)
            if budget:
                return self._tracker.reallocate(budget)
            return None

    def stats(self) -> dict[str, Any]:
        with self._lock:
            total_b = len(self._budgets)
            total_consumed = sum(b.total_consumed for b in self._budgets.values())
            return {
                "total_budgets": total_b,
                "total_tokens_tracked": total_consumed,
                "active_budgets": [b.to_dict() for b in self._budgets.values()],
            }


_instance: TokenBudgetEngine | None = None
_lock = threading.Lock()


def get_token_budget_engine() -> TokenBudgetEngine:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = TokenBudgetEngine()
    return _instance
