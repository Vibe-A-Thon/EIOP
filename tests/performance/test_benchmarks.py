"""Performance benchmark tests (MVP benchmark definition).

These run against the in-memory store to validate algorithmic bounds.
Docker-level benchmarks run separately via the smoke test suite.
"""

import time

from eoip.contracts.query_plan import QueryPlan
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.traversal import GraphTraversal
from eoip.query.executor import QueryExecutor


def _build_graph(n_vertices=200, branching=3):
    store = MemoryGraphStore()
    vertices = []
    for i in range(n_vertices):
        v = store.upsert_vertex("WorkItem", {
            "canonical_id": f"urn:bench:item:{i}",
            "issue_key": f"BENCH-{i}",
            "summary": f"Benchmark item {i}",
        })
        vertices.append(v)
    for i, v in enumerate(vertices):
        for j in range(1, branching + 1):
            target_idx = (i * branching + j) % n_vertices
            if target_idx != i:
                store.upsert_edge("REFERENCES", v["vid"], vertices[target_idx]["vid"], {
                    "fact_key": f"bench-ref-{i}-{target_idx}",
                    "creation_status": "DETERMINISTIC",
                })
    return store


def test_entity_lookup_under_500ms():
    store = _build_graph(500)
    start = time.perf_counter()
    for i in range(100):
        store.get_vertex_by_canonical_id(f"urn:bench:item:{i}")
    elapsed = (time.perf_counter() - start) * 1000
    per_lookup = elapsed / 100
    assert per_lookup < 500, f"p95 entity lookup: {per_lookup:.1f}ms exceeds 500ms target"


def test_bounded_path_query_under_2s():
    store = _build_graph(500, branching=3)
    traversal = GraphTraversal(store, max_depth=4, max_results=100)
    start = time.perf_counter()
    traversal.find_path("urn:bench:item:0", "urn:bench:item:99", max_depth=4)
    elapsed = time.perf_counter() - start
    assert elapsed < 2.0, f"Path query took {elapsed:.2f}s, exceeds 2s target"


def test_bounded_impact_query_under_2s():
    store = _build_graph(500, branching=3)
    traversal = GraphTraversal(store, max_depth=4, max_results=100)
    start = time.perf_counter()
    result = traversal.impact("urn:bench:item:0", max_depth=4)
    elapsed = time.perf_counter() - start
    assert elapsed < 2.0, f"Impact query took {elapsed:.2f}s, exceeds 2s target"
    assert result["source"] is not None


def test_query_executor_search_under_1s():
    store = _build_graph(500)
    executor = QueryExecutor(store)
    start = time.perf_counter()
    plan = QueryPlan(intent="SEARCH", anchors=["BENCH-42"], max_depth=1, result_limit=25, evidence_mode="NONE")
    executor.execute(plan)
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, f"Search took {elapsed:.2f}s, exceeds 1s target"


def test_benchmark_dataset_scale_s_executor_bounds():
    """NFR-PERF-001 (CI scale): benchmark dataset scale 's' (seed 42) — 200 work
    items, 2 repos, 30 commits, 500 files/symbols; ~2.3k edges, ~950 vertices.

    The versioned harness emits actual nearest-rank p50/p95/p99 values. The
    full baseline profile runs manually against an isolated HugeGraph stack.
    """
    from scripts.benchmark import load_manifest, run_benchmark

    report = run_benchmark(load_manifest(), samples=5, warmups=1)

    assert report["status"] == "passed"
    assert report["dataset"]["vertices"] > 0
    assert report["dataset"]["edges"] > 0
    measured = [item for item in report["workloads"] if item["status"] != "skipped"]
    assert measured
    assert all(set(item["latency_ms"]) >= {"p50", "p95", "p99"} for item in measured)


def test_benchmark_manifest_declares_normative_full_dataset():
    from scripts.benchmark import load_manifest
    from scripts.benchmark_data import SCALES

    manifest = load_manifest()
    baseline = SCALES[manifest["dataset"]["profiles"]["full"]]

    assert baseline["work_items"] == 2_000
    assert baseline["repos"] == 10
    assert baseline["commits"] == 15_000
    assert baseline["files_symbols"] == 25_000
    assert baseline["document_sections"] == 5_000
    assert manifest["bulk_batch_size"] == 500


def test_benchmark_percentile_uses_nearest_rank():
    from scripts.benchmark import percentile

    values = list(range(1, 101))
    assert percentile(values, 50) == 50
    assert percentile(values, 95) == 95
    assert percentile(values, 99) == 99
