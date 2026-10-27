"""Deep health probe system for readiness, liveness, and startup checks.

Provides Kubernetes-compatible health endpoints with subsystem-level
granularity. Each probe aggregates results from registered health
contributors (graph store, learning engine, RAG suite, etc.) and
reports overall health only when all critical dependencies pass.
"""

from __future__ import annotations

import enum
import threading
import time
from dataclasses import dataclass, field
from typing import Any
from collections.abc import Callable


class HealthStatus(str, enum.Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"


class ProbeType(str, enum.Enum):
    LIVENESS = "LIVENESS"
    READINESS = "READINESS"
    STARTUP = "STARTUP"


@dataclass
class ComponentHealth:
    name: str
    status: HealthStatus
    latency_ms: float
    details: dict[str, Any] = field(default_factory=dict)
    last_checked: float = 0.0


@dataclass
class SystemHealth:
    status: HealthStatus
    probe_type: ProbeType
    timestamp: float
    components: list[ComponentHealth]
    version: str
    uptime_seconds: float


class HealthProbe:
    """Aggregates health checks from registered subsystem contributors."""

    def __init__(self, version: str = "1.0.0") -> None:
        self._contributors: dict[str, tuple[Callable[[], ComponentHealth], bool]] = {}
        self._lock = threading.Lock()
        self._start_time = time.monotonic()
        self._version = version
        self._startup_complete = False

    def register(
        self,
        name: str,
        check_fn: Callable[[], ComponentHealth],
        critical: bool = True,
    ) -> None:
        with self._lock:
            self._contributors[name] = (check_fn, critical)

    def mark_startup_complete(self) -> None:
        self._startup_complete = True

    def check_liveness(self) -> SystemHealth:
        return self._run_probe(ProbeType.LIVENESS)

    def check_readiness(self) -> SystemHealth:
        return self._run_probe(ProbeType.READINESS)

    def check_startup(self) -> SystemHealth:
        if not self._startup_complete:
            return SystemHealth(
                status=HealthStatus.UNHEALTHY,
                probe_type=ProbeType.STARTUP,
                timestamp=time.time(),
                components=[],
                version=self._version,
                uptime_seconds=time.monotonic() - self._start_time,
            )
        return self._run_probe(ProbeType.STARTUP)

    def _run_probe(self, probe_type: ProbeType) -> SystemHealth:
        components: list[ComponentHealth] = []
        overall = HealthStatus.HEALTHY

        with self._lock:
            contributors = dict(self._contributors)

        for name, (check_fn, critical) in contributors.items():
            start = time.perf_counter()
            try:
                result = check_fn()
                result.latency_ms = (time.perf_counter() - start) * 1000.0
                result.last_checked = time.time()
            except Exception as exc:
                result = ComponentHealth(
                    name=name,
                    status=HealthStatus.UNHEALTHY,
                    latency_ms=(time.perf_counter() - start) * 1000.0,
                    details={"error": str(exc)},
                    last_checked=time.time(),
                )

            components.append(result)
            if result.status == HealthStatus.UNHEALTHY and critical:
                overall = HealthStatus.UNHEALTHY
            elif result.status == HealthStatus.DEGRADED and overall == HealthStatus.HEALTHY:
                overall = HealthStatus.DEGRADED

        return SystemHealth(
            status=overall,
            probe_type=probe_type,
            timestamp=time.time(),
            components=components,
            version=self._version,
            uptime_seconds=time.monotonic() - self._start_time,
        )

    def to_dict(self, health: SystemHealth) -> dict[str, Any]:
        return {
            "status": health.status.value,
            "probe": health.probe_type.value,
            "timestamp": health.timestamp,
            "version": health.version,
            "uptime_seconds": round(health.uptime_seconds, 2),
            "components": [
                {
                    "name": c.name,
                    "status": c.status.value,
                    "latency_ms": round(c.latency_ms, 2),
                    "details": c.details,
                }
                for c in health.components
            ],
        }


def graph_store_health_check(store: Any) -> ComponentHealth:
    if store is None:
        return ComponentHealth(
            name="graph_store",
            status=HealthStatus.DEGRADED,
            latency_ms=0.0,
            details={"message": "No graph store configured"},
        )
    try:
        if hasattr(store, "ping"):
            store.ping()
        elif hasattr(store, "count_vertices"):
            store.count_vertices(None)
        return ComponentHealth(
            name="graph_store",
            status=HealthStatus.HEALTHY,
            latency_ms=0.0,
            details={"type": type(store).__name__},
        )
    except Exception as exc:
        return ComponentHealth(
            name="graph_store",
            status=HealthStatus.UNHEALTHY,
            latency_ms=0.0,
            details={"error": str(exc)},
        )


def learning_engine_health_check(engine: Any) -> ComponentHealth:
    try:
        telemetry = engine.get_learning_telemetry()
        return ComponentHealth(
            name="learning_engine",
            status=HealthStatus.HEALTHY,
            latency_ms=0.0,
            details={
                "paradigms_active": telemetry.get("paradigms_active", 0),
                "q_learning_updates": telemetry.get("q_learning", {}).get("total_updates", 0),
            },
        )
    except Exception as exc:
        return ComponentHealth(
            name="learning_engine",
            status=HealthStatus.DEGRADED,
            latency_ms=0.0,
            details={"error": str(exc)},
        )


def self_llm_health_check(engine: Any) -> ComponentHealth:
    try:
        tokens = engine.tokenize("health check")
        return ComponentHealth(
            name="self_llm",
            status=HealthStatus.HEALTHY,
            latency_ms=0.0,
            details={"tokenizer_ok": len(tokens) > 0},
        )
    except Exception as exc:
        return ComponentHealth(
            name="self_llm",
            status=HealthStatus.DEGRADED,
            latency_ms=0.0,
            details={"error": str(exc)},
        )
