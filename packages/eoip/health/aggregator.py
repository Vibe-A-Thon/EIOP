"""Health Check Aggregator & SLA Monitor — unified health checks across all systems with SLA tracking."""

from __future__ import annotations

import threading
import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable

from eoip.enterprise.logging import get_logger

_log = get_logger("health.aggregator")


class HealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"


class SLAMetric(str, Enum):
    UPTIME = "UPTIME"
    LATENCY_P50 = "LATENCY_P50"
    LATENCY_P99 = "LATENCY_P99"
    ERROR_RATE = "ERROR_RATE"
    THROUGHPUT = "THROUGHPUT"


@dataclass
class HealthCheck:
    name: str
    target: str
    check_fn: Callable[[], dict[str, Any]] | None = None
    interval_seconds: float = 30.0
    timeout_seconds: float = 10.0
    failure_threshold: int = 3
    enabled: bool = True


@dataclass
class HealthResult:
    target: str
    status: HealthStatus
    latency_ms: float = 0.0
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)
    checked_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


@dataclass
class SLATarget:
    name: str
    metric: SLAMetric
    target_value: float
    warning_threshold: float
    current_value: float = 0.0
    violations: int = 0
    measurement_window_seconds: int = 3600

    def is_met(self) -> bool:
        if self.metric in (SLAMetric.UPTIME, SLAMetric.THROUGHPUT):
            return self.current_value >= self.target_value
        return self.current_value <= self.target_value

    def is_warning(self) -> bool:
        if self.metric in (SLAMetric.UPTIME, SLAMetric.THROUGHPUT):
            return self.current_value < self.warning_threshold
        return self.current_value > self.warning_threshold


class HealthAggregator:
    """Aggregates health checks across all registered systems and tracks SLAs."""

    def __init__(self) -> None:
        self._checks: dict[str, HealthCheck] = {}
        self._results: dict[str, list[HealthResult]] = defaultdict(list)
        self._consecutive_failures: dict[str, int] = defaultdict(int)
        self._sla_targets: dict[str, SLATarget] = {}
        self._listeners: list[Callable[[str, HealthResult], None]] = []
        self._lock = threading.Lock()
        self._max_history = 100

    def register_check(self, check: HealthCheck) -> None:
        with self._lock:
            self._checks[check.target] = check

    def unregister_check(self, target: str) -> bool:
        with self._lock:
            return self._checks.pop(target, None) is not None

    def run_check(self, target: str) -> HealthResult:
        check = self._checks.get(target)
        if not check:
            return HealthResult(
                target=target, status=HealthStatus.UNKNOWN,
                message="No check registered",
                checked_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            )

        t0 = time.time()
        try:
            if check.check_fn:
                details = check.check_fn()
                latency = (time.time() - t0) * 1000
                status = HealthStatus(details.get("status", "HEALTHY"))
                msg = details.get("message", "OK")
            else:
                latency = 0.0
                status = HealthStatus.UNKNOWN
                msg = "No check function"
                details = {}
        except Exception as e:
            latency = (time.time() - t0) * 1000
            status = HealthStatus.UNHEALTHY
            msg = str(e)
            details = {}

        result = HealthResult(
            target=target, status=status, latency_ms=round(latency, 2),
            message=msg, details=details,
            checked_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        )

        with self._lock:
            self._results[target].append(result)
            if len(self._results[target]) > self._max_history:
                self._results[target] = self._results[target][-self._max_history:]

            if status == HealthStatus.UNHEALTHY:
                self._consecutive_failures[target] += 1
            else:
                self._consecutive_failures[target] = 0

        for listener in self._listeners:
            try:
                listener(target, result)
            except Exception:
                pass

        return result

    def run_all_checks(self) -> dict[str, HealthResult]:
        results: dict[str, HealthResult] = {}
        for target in list(self._checks.keys()):
            check = self._checks[target]
            if check.enabled:
                results[target] = self.run_check(target)
        return results

    def get_status(self, target: str) -> HealthResult | None:
        history = self._results.get(target)
        if history:
            return history[-1]
        return None

    def get_aggregate_status(self) -> dict[str, Any]:
        statuses: dict[str, int] = defaultdict(int)
        all_results: dict[str, dict] = {}

        for target in self._checks:
            last = self.get_status(target)
            if last:
                statuses[last.status.value] += 1
                all_results[target] = last.to_dict()
            else:
                statuses["UNKNOWN"] += 1

        unhealthy = statuses.get("UNHEALTHY", 0)
        degraded = statuses.get("DEGRADED", 0)
        total = len(self._checks)

        if unhealthy > 0:
            overall = HealthStatus.UNHEALTHY
        elif degraded > 0:
            overall = HealthStatus.DEGRADED
        elif total == 0:
            overall = HealthStatus.UNKNOWN
        else:
            overall = HealthStatus.HEALTHY

        return {
            "overall_status": overall.value,
            "total_checks": total,
            "status_counts": dict(statuses),
            "checks": all_results,
        }

    def get_history(self, target: str, limit: int = 20) -> list[dict[str, Any]]:
        history = self._results.get(target, [])
        return [r.to_dict() for r in history[-limit:]]

    def add_sla_target(self, sla: SLATarget) -> None:
        self._sla_targets[sla.name] = sla

    def update_sla_metric(self, name: str, value: float) -> None:
        sla = self._sla_targets.get(name)
        if sla:
            sla.current_value = value
            if not sla.is_met():
                sla.violations += 1

    def get_sla_report(self) -> list[dict[str, Any]]:
        return [
            {
                "name": sla.name,
                "metric": sla.metric.value,
                "target": sla.target_value,
                "current": sla.current_value,
                "met": sla.is_met(),
                "warning": sla.is_warning(),
                "violations": sla.violations,
            }
            for sla in self._sla_targets.values()
        ]

    def on_status_change(self, listener: Callable[[str, HealthResult], None]) -> None:
        self._listeners.append(listener)

    def compute_uptime(self, target: str) -> float:
        history = self._results.get(target, [])
        if not history:
            return 0.0
        healthy = sum(1 for r in history if r.status == HealthStatus.HEALTHY)
        return round(healthy / len(history), 4)
