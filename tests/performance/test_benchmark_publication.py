"""NFR-PERF-001: Benchmark-defined objectives.

Validates that benchmark results are structured, machine-readable,
and include dataset/hardware/version metadata as required. Runs a
representative benchmark suite and verifies the output format.
"""

import platform
import sys
import time

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.traversal import GraphTraversal


def _build_benchmark_graph(n=200, branching=3):
    store = MemoryGraphStore()
    vertices = []
    for i in range(n):
        v = store.upsert_vertex("WorkItem", {
            "canonical_id": f"urn:bench:item:{i}",
            "issue_key": f"BENCH-{i}",
            "summary": f"Benchmark item {i}",
        })
        vertices.append(v)
    for i, v in enumerate(vertices):
        for j in range(1, branching + 1):
            target_idx = (i * branching + j) % n
            if target_idx != i:
                store.upsert_edge("REFERENCES", v["vid"], vertices[target_idx]["vid"], {
                    "fact_key": f"bench-ref-{i}-{target_idx}",
                    "creation_status": "DETERMINISTIC",
                })
    return store


def _run_benchmark(store, operation, iterations=50):
    """Run a benchmark and return structured results."""
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        operation()
        elapsed = time.perf_counter() - start
        times.append(elapsed * 1000)

    times.sort()
    n = len(times)
    return {
        "iterations": n,
        "p50_ms": times[n // 2],
        "p95_ms": times[int(n * 0.95)],
        "p99_ms": times[int(n * 0.99)],
        "min_ms": times[0],
        "max_ms": times[-1],
        "mean_ms": sum(times) / n,
    }


def _hardware_profile():
    return {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "python_version": sys.version,
        "cpu_count": platform.os.cpu_count(),
        "machine": platform.machine(),
    }


def test_benchmark_results_are_structured():
    """Benchmark results must include p50/p95/p99 and metadata."""
    store = _build_benchmark_graph(200)

    lookup_result = _run_benchmark(
        store,
        lambda: store.get_vertex_by_canonical_id("urn:bench:item:42"),
        iterations=50,
    )

    assert "p50_ms" in lookup_result
    assert "p95_ms" in lookup_result
    assert "p99_ms" in lookup_result
    assert "iterations" in lookup_result
    assert lookup_result["iterations"] == 50
    assert lookup_result["p50_ms"] <= lookup_result["p95_ms"] <= lookup_result["p99_ms"]


def test_benchmark_includes_hardware_profile():
    """Benchmark results must identify the hardware and environment."""
    profile = _hardware_profile()
    assert "platform" in profile
    assert "python_version" in profile
    assert "cpu_count" in profile
    assert profile["cpu_count"] is not None and profile["cpu_count"] > 0


def test_entity_lookup_benchmark_meets_target():
    """Entity lookup p95 must be under 500ms (NFR-PERF-001 target)."""
    store = _build_benchmark_graph(500)
    result = _run_benchmark(
        store,
        lambda: store.get_vertex_by_canonical_id("urn:bench:item:42"),
        iterations=100,
    )
    assert result["p95_ms"] < 500, (
        f"Entity lookup p95={result['p95_ms']:.1f}ms exceeds 500ms target"
    )


def test_path_query_benchmark_meets_target():
    """Path query p95 must be under 2000ms (NFR-PERF-001 target)."""
    store = _build_benchmark_graph(500, branching=3)
    traversal = GraphTraversal(store, max_depth=4, max_results=100)

    result = _run_benchmark(
        store,
        lambda: traversal.find_path(
            "urn:bench:item:0", "urn:bench:item:99", max_depth=4
        ),
        iterations=20,
    )
    assert result["p95_ms"] < 2000, (
        f"Path query p95={result['p95_ms']:.1f}ms exceeds 2000ms target"
    )


def test_full_benchmark_report_structure():
    """A complete benchmark report includes all required sections."""
    store = _build_benchmark_graph(200)
    traversal = GraphTraversal(store, max_depth=4, max_results=100)

    report = {
        "version": "0.1.0-architecture-baseline",
        "dataset": {
            "vertices": 200,
            "branching_factor": 3,
            "description": "Synthetic benchmark graph",
        },
        "hardware": _hardware_profile(),
        "results": {
            "entity_lookup": _run_benchmark(
                store,
                lambda: store.get_vertex_by_canonical_id("urn:bench:item:42"),
            ),
            "path_query": _run_benchmark(
                store,
                lambda: traversal.find_path(
                    "urn:bench:item:0", "urn:bench:item:50", max_depth=4
                ),
                iterations=10,
            ),
            "impact_query": _run_benchmark(
                store,
                lambda: traversal.impact("urn:bench:item:0", max_depth=3),
                iterations=10,
            ),
        },
    }

    assert "version" in report
    assert "dataset" in report
    assert "hardware" in report
    assert "results" in report
    for bench_name, bench in report["results"].items():
        assert "p50_ms" in bench, f"{bench_name} missing p50_ms"
        assert "p95_ms" in bench, f"{bench_name} missing p95_ms"
        assert "p99_ms" in bench, f"{bench_name} missing p99_ms"
