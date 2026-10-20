"""Quota manager — noisy-neighbor control (SR-TEN-006).

Per-tenant quotas covering graph size, ingestion rate, concurrent queries,
LLM token budget and storage (SR-TEN-006). Three operations per dimension:

- ``check(tenant, dimension, amount)`` — dry-run, returns allow/deny.
- ``consume(tenant, dimension, amount)`` — reserve against the quota;
  denied when the limit would be exceeded. (Idempotency keys accepted —
  consuming twice with the same key is a no-op returning the first result.)
- ``refund(tenant, dimension, amount, key)`` — return previously consumed
  capacity (e.g. a query finished and released its concurrency slot).

Two dimensions are time-windowed: ingestion rate (per minute, sliding
token bucket) and LLM tokens (per hour, sliding window). The others
(graph size, storage, concurrent queries) are counters.

Fair-scheduling priority lanes (SR-TEN-006): each tenant belongs to a lane
(``interactive`` > ``batch`` > ``background``). ``fair_order`` sorts
waiting tenants by lane priority then by deficit (most under-quota first)
so background tenants cannot starve interactive ones.

Per-tenant rate limits and circuit breakers are ADR-gated (deferred); the
quota primitives here are the substrate they would wrap.
"""

from __future__ import annotations

import threading
import time
from collections import deque
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

QUOTA_DIMENSIONS: frozenset[str] = frozenset({
    "graph_size",        # entities/edges count
    "ingestion_rate",    # records ingested per minute
    "concurrent_queries",
    "llm_tokens",        # tokens per hour
    "storage_bytes",
})

# Sliding window for the two time-based dimensions.
WINDOW_SECONDS = {
    "ingestion_rate": 60.0,
    "llm_tokens": 3600.0,
}


class QuotaExceeded(RuntimeError):
    """Raised (or returned) when a consume would exceed a tenant quota (SR-TEN-006)."""


@dataclass
class QuotaSpec:
    """Per-tenant quota limits; None = unlimited (SR-TEN-006)."""

    graph_size: int | None = None
    ingestion_rate: int | None = None
    concurrent_queries: int | None = None
    llm_tokens: int | None = None
    storage_bytes: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "graph_size": self.graph_size,
            "ingestion_rate": self.ingestion_rate,
            "concurrent_queries": self.concurrent_queries,
            "llm_tokens": self.llm_tokens,
            "storage_bytes": self.storage_bytes,
        }


class Lane(StrEnum):
    INTERACTIVE = "interactive"
    BATCH = "batch"
    BACKGROUND = "background"


_LANE_ORDER = {Lane.INTERACTIVE: 0, Lane.BATCH: 1, Lane.BACKGROUND: 2}


@dataclass
class QuotaDecision:
    tenant_id: str
    dimension: str
    allowed: bool
    requested: int
    limit: int | None
    used: int
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "tenant_id": self.tenant_id,
            "dimension": self.dimension,
            "allowed": self.allowed,
            "requested": self.requested,
            "limit": self.limit,
            "used": self.used,
            "reason": self.reason,
        }


@dataclass
class _Usage:
    """Windowed or counter usage for one tenant/dimension."""

    counter: int = 0
    events: deque[tuple[float, int]] = field(default_factory=deque)


class CircuitOpen(RuntimeError):
    """Raised when a tenant's circuit for a dependency is open (SR-TEN-006)."""

    def __init__(self, tenant_id: str, dependency: str, retry_after: float) -> None:
        super().__init__(f"circuit open for tenant {tenant_id} on {dependency}; retry after {retry_after:.1f}s")
        self.tenant_id, self.dependency, self.retry_after = tenant_id, dependency, retry_after


class TenantCircuitBreaker:
    """Per-tenant, per-dependency circuit breakers (SR-TEN-006 noisy-neighbor control).

    closed -> open after ``failure_threshold`` consecutive failures; open rejects immediately
    for ``cooldown_s``; then half_open admits exactly one probe: success closes, failure re-opens.
    One tenant tripping a breaker never affects another tenant's circuit for the same dependency.
    """

    def __init__(self, *, failure_threshold: int = 5, cooldown_s: float = 30.0,
                 clock: Any = time.monotonic) -> None:
        if failure_threshold < 1 or cooldown_s <= 0:
            raise ValueError("failure_threshold >= 1 and cooldown_s > 0 required")
        self.failure_threshold, self.cooldown_s, self._clock = failure_threshold, cooldown_s, clock
        self._state: dict[tuple[str, str], dict[str, Any]] = {}
        self._lock = threading.Lock()

    def _get(self, tenant_id: str, dependency: str) -> dict[str, Any]:
        if not tenant_id:
            raise ValueError("tenant context is required (fail closed)")
        return self._state.setdefault((tenant_id, dependency),
                                      {"state": "closed", "failures": 0, "opened_at": 0.0, "probe": False})

    def state(self, tenant_id: str, dependency: str) -> str:
        with self._lock:
            st = self._get(tenant_id, dependency)
            if st["state"] == "open" and self._clock() - st["opened_at"] >= self.cooldown_s:
                return "half_open"
            return st["state"]

    def before_call(self, tenant_id: str, dependency: str) -> None:
        with self._lock:
            st = self._get(tenant_id, dependency)
            if st["state"] == "open":
                elapsed = self._clock() - st["opened_at"]
                if elapsed < self.cooldown_s:
                    raise CircuitOpen(tenant_id, dependency, self.cooldown_s - elapsed)
                st["state"] = "half_open"
            if st["state"] == "half_open":
                if st["probe"]:
                    raise CircuitOpen(tenant_id, dependency, 0.0)
                st["probe"] = True

    def record_success(self, tenant_id: str, dependency: str) -> None:
        with self._lock:
            st = self._get(tenant_id, dependency)
            st.update(state="closed", failures=0, probe=False)

    def record_failure(self, tenant_id: str, dependency: str) -> None:
        with self._lock:
            st = self._get(tenant_id, dependency)
            st["failures"] += 1
            if st["state"] == "half_open" or st["failures"] >= self.failure_threshold:
                st.update(state="open", opened_at=self._clock(), probe=False)

    def call(self, tenant_id: str, dependency: str, fn: Any, *args: Any, **kwargs: Any) -> Any:
        self.before_call(tenant_id, dependency)
        try:
            result = fn(*args, **kwargs)
        except Exception:
            self.record_failure(tenant_id, dependency)
            raise
        self.record_success(tenant_id, dependency)
        return result


class QuotaManager:
    """Thread-safe per-tenant quota checks/consumption (SR-TEN-006)."""

    def __init__(self) -> None:
        self.breakers = TenantCircuitBreaker()
        self._specs: dict[str, QuotaSpec] = {}
        self._lanes: dict[str, Lane] = {}
        self._usage: dict[tuple[str, str], _Usage] = {}
        self._idempotency: dict[str, QuotaDecision] = {}
        self._lock = threading.Lock()

    # -- administration ---------------------------------------------------

    def set_quota(self, tenant_id: str, spec: QuotaSpec, lane: Lane = Lane.BATCH) -> None:
        if not tenant_id:
            raise ValueError("tenant_id required")
        with self._lock:
            self._specs[tenant_id] = spec
            self._lanes[tenant_id] = Lane(lane)

    def lane(self, tenant_id: str) -> Lane:
        return self._lanes.get(tenant_id, Lane.BATCH)

    # -- core operations ---------------------------------------------------

    def check(self, tenant_id: str, dimension: str, amount: int = 1) -> QuotaDecision:
        if dimension not in QUOTA_DIMENSIONS:
            raise ValueError(f"unknown quota dimension: {dimension}")
        with self._lock:
            return self._decision(tenant_id, dimension, amount)

    def consume(
        self, tenant_id: str, dimension: str, amount: int = 1, *, idempotency_key: str | None = None
    ) -> QuotaDecision:
        if amount <= 0:
            raise ValueError("amount must be positive")
        with self._lock:
            if idempotency_key and idempotency_key in self._idempotency:
                return self._idempotency[idempotency_key]
            decision = self._decision(tenant_id, dimension, amount)
            if decision.allowed:
                usage = self._usage_for(tenant_id, dimension)
                if dimension in WINDOW_SECONDS:
                    usage.events.append((time.monotonic(), amount))
                else:
                    usage.counter += amount
                if idempotency_key:
                    self._idempotency[idempotency_key] = decision
            return decision

    def refund(
        self, tenant_id: str, dimension: str, amount: int = 1, *, idempotency_key: str | None = None
    ) -> QuotaDecision:
        """Release previously consumed capacity (SR-TEN-006)."""
        if amount <= 0:
            raise ValueError("amount must be positive")
        with self._lock:
            usage = self._usage_for(tenant_id, dimension)
            if dimension in WINDOW_SECONDS:
                # Remove the most recent matching events (sliding window credit).
                remaining = amount
                while remaining and usage.events:
                    ts, amt = usage.events.pop()
                    remaining -= amt
            else:
                usage.counter = max(0, usage.counter - amount)
            spec = self._specs.get(tenant_id, QuotaSpec())
            limit = getattr(spec, dimension)
            used = self._used_locked(tenant_id, dimension)
            decision = QuotaDecision(tenant_id, dimension, True, amount, limit, used, "refunded")
            if idempotency_key:
                self._idempotency.pop(idempotency_key, None)
            return decision

    def usage(self, tenant_id: str, dimension: str) -> int:
        with self._lock:
            return self._used_locked(tenant_id, dimension)

    # -- fair scheduling (SR-TEN-006) ---------------------------------------

    def fair_order(self, waiting: list[str]) -> list[str]:
        """Order waiting tenants: lane priority, then most-unused-quota first."""
        with self._lock:
            def sort_key(tid: str) -> tuple[int, float]:
                lane_rank = _LANE_ORDER.get(self._lanes.get(tid, Lane.BATCH), 1)
                spec = self._specs.get(tid, QuotaSpec())
                used_frac = self._dominant_usage_fraction(tid, spec)
                return (lane_rank, used_frac)

            return sorted(waiting, key=sort_key)

    def _dominant_usage_fraction(self, tid: str, spec: QuotaSpec) -> float:
        worst = 0.0
        for dim in QUOTA_DIMENSIONS:
            limit = getattr(spec, dim)
            if limit:
                worst = max(worst, self._used_locked(tid, dim) / limit)
        return worst

    # -- internals -----------------------------------------------------------

    def _usage_for(self, tenant_id: str, dimension: str) -> _Usage:
        key = (tenant_id, dimension)
        if key not in self._usage:
            self._usage[key] = _Usage()
        return self._usage[key]

    def _used_locked(self, tenant_id: str, dimension: str) -> int:
        usage = self._usage_for(tenant_id, dimension)
        window = WINDOW_SECONDS.get(dimension)
        if window is None:
            return usage.counter
        now = time.monotonic()
        while usage.events and now - usage.events[0][0] > window:
            usage.events.popleft()
        return sum(amt for _, amt in usage.events)

    def _decision(self, tenant_id: str, dimension: str, amount: int) -> QuotaDecision:
        spec = self._specs.get(tenant_id)
        limit = getattr(spec, dimension) if spec else None
        used = self._used_locked(tenant_id, dimension)
        if limit is None:
            return QuotaDecision(tenant_id, dimension, True, amount, None, used)
        if used + amount > limit:
            return QuotaDecision(
                tenant_id, dimension, False, amount, limit, used,
                f"quota exceeded: {dimension} used={used} limit={limit}",
            )
        return QuotaDecision(tenant_id, dimension, True, amount, limit, used)
