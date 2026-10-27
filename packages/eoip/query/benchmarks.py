"""Warmed endpoint benchmarks and semantic equivalence comparison (CRA-024.6).

Separates warmed server/endpoint benchmarks from cold CLI/module startup time.
Compares materialized and virtual query results on declared semantic equivalence.
"""
from __future__ import annotations

import statistics
import time
from dataclasses import dataclass, field
from typing import Any, Optional
from collections.abc import Callable


@dataclass
class LatencyMetrics:
    iterations: int
    cold_startup_ms: float
    min_ms: float
    max_ms: float
    mean_ms: float
    p50_ms: float
    p95_ms: float
    p99_ms: float


@dataclass
class BenchmarkReport:
    name: str
    warmed: bool
    metrics: LatencyMetrics
    details: dict[str, Any] = field(default_factory=dict)


class WarmedEndpointBenchmark:
    """Benchmark runner isolating cold startup from warmed execution."""

    def __init__(self, warmup_runs: int = 5, measured_runs: int = 25) -> None:
        self.warmup_runs = warmup_runs
        self.measured_runs = measured_runs

    def run_benchmark(
        self,
        name: str,
        query_fn: Callable[[], Any],
        cold_setup_fn: Optional[Callable[[], None]] = None,
    ) -> BenchmarkReport:
        # 1. Measure cold startup if provided
        cold_startup_ms = 0.0
        if cold_setup_fn:
            t0 = time.perf_counter()
            cold_setup_fn()
            cold_startup_ms = (time.perf_counter() - t0) * 1000.0

        # 2. Warmup iterations
        for _ in range(self.warmup_runs):
            query_fn()

        # 3. Measured runs
        latencies: list[float] = []
        for _ in range(self.measured_runs):
            t0 = time.perf_counter()
            query_fn()
            latencies.append((time.perf_counter() - t0) * 1000.0)

        latencies.sort()
        n = len(latencies)
        p50 = latencies[int(n * 0.50)]
        p95 = latencies[min(int(n * 0.95), n - 1)]
        p99 = latencies[min(int(n * 0.99), n - 1)]

        metrics = LatencyMetrics(
            iterations=n,
            cold_startup_ms=cold_startup_ms,
            min_ms=latencies[0],
            max_ms=latencies[-1],
            mean_ms=statistics.mean(latencies),
            p50_ms=p50,
            p95_ms=p95,
            p99_ms=p99,
        )

        return BenchmarkReport(
            name=name,
            warmed=True,
            metrics=metrics,
            details={"samples_count": n},
        )


class SemanticEquivalenceComparator:
    """Compares materialized and virtualized results based on declared semantics."""

    def compare(
        self,
        materialized_rows: list[dict[str, Any]],
        virtual_rows: list[dict[str, Any]],
        id_field: str = "canonical_id",
        fields_to_compare: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """Validates that materialized and virtual datasets represent the same logical facts."""
        mat_map = {r.get(id_field): r for r in materialized_rows if r.get(id_field)}
        virt_map = {r.get(id_field): r for r in virtual_rows if r.get(id_field)}

        missing_in_virt = set(mat_map.keys()) - set(virt_map.keys())
        missing_in_mat = set(virt_map.keys()) - set(mat_map.keys())

        discrepancies: list[dict[str, Any]] = []
        common_ids = set(mat_map.keys()) & set(virt_map.keys())

        for cid in common_ids:
            r_mat = mat_map[cid]
            r_virt = virt_map[cid]
            check_fields = fields_to_compare or list(set(r_mat.keys()) & set(r_virt.keys()))

            for f in check_fields:
                val_m = r_mat.get(f)
                val_v = r_virt.get(f)
                if val_m != val_v:
                    discrepancies.append({
                        "id": cid,
                        "field": f,
                        "materialized_value": val_m,
                        "virtual_value": val_v,
                    })

        is_equivalent = (
            len(missing_in_virt) == 0
            and len(missing_in_mat) == 0
            and len(discrepancies) == 0
        )

        return {
            "equivalent": is_equivalent,
            "materialized_count": len(materialized_rows),
            "virtual_count": len(virtual_rows),
            "missing_in_virtual": list(missing_in_virt),
            "missing_in_materialized": list(missing_in_mat),
            "discrepancies_count": len(discrepancies),
            "discrepancies": discrepancies[:10],
        }
