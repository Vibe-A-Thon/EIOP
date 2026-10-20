"""Performance & Throughput Benchmarking: Concurrency and Latency Profiling."""

from __future__ import annotations

import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
import pytest


@pytest.mark.performance
class TestQueryThroughput:
    """Load and throughput benchmarking for KnowGridFlow API endpoints."""

    def test_concurrent_schema_retrieval_latency(self, admin_client):
        """Simulate concurrent users requesting graph schema and calculate P50, P95, P99."""
        total_requests = 40
        concurrency = 8
        latencies: list[float] = []

        def _make_req():
            t0 = time.perf_counter()
            res = admin_client.get("/graph/schema")
            elapsed = time.perf_counter() - t0
            assert res.status_code == 200
            return elapsed

        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(_make_req) for _ in range(total_requests)]
            for f in as_completed(futures):
                latencies.append(f.result())

        assert len(latencies) == total_requests
        latencies_ms = [l * 1000.0 for l in sorted(latencies)]

        p50 = statistics.median(latencies_ms)
        p95 = latencies_ms[int(total_requests * 0.95)]
        p99 = latencies_ms[-1]

        print(f"\n[Performance Benchmark] Requests: {total_requests}, Concurrency: {concurrency}")
        print(f"  P50 Latency: {p50:.2f} ms")
        print(f"  P95 Latency: {p95:.2f} ms")
        print(f"  P99 Latency: {p99:.2f} ms")

        # Enterprise SLO check: In-memory schema query should resolve P95 under 600ms in-process
        assert p95 < 600.0, f"P95 latency {p95:.2f}ms exceeded SLO threshold of 600ms"
