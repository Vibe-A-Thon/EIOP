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

    SEARCH / IMPACT / PATH executed via the QueryExecutor must each stay under
    a 2s bound (max over repeated runs as a p95 proxy). Generation + queries
    complete in well under 5s, so this test runs in the default suite.

    TODO(NFR-PERF-001): full-scale benchmarking against HugeGraph requires the
    Docker Compose profile; scale 'm' (~19k edges) and production profiles run
    there, not in unit tests.
    """
    from scripts.benchmark_data import build_store, store_stats

    store = build_store("s")
    stats = store_stats(store, "s", 42)
    assert stats["vertices"] > 0 and stats["edges"] > 0

    executor = QueryExecutor(store)
    plans = [
        QueryPlan(intent="SEARCH", anchors=["BENCH-42"], max_depth=1, result_limit=25, evidence_mode="NONE"),
        QueryPlan(
            intent="IMPACT",
            anchors=["urn:bench:item:0"],
            max_depth=4,
            result_limit=100,
            evidence_mode="SUMMARY",
        ),
        QueryPlan(
            intent="PATH",
            anchors=["urn:bench:item:0", "urn:bench:item:5"],
            max_depth=8,
            result_limit=100,
            evidence_mode="NONE",
        ),
    ]
    for plan in plans:
        latencies = []
        for _ in range(5):
            start = time.perf_counter()
            result = executor.execute(plan)
            latencies.append(time.perf_counter() - start)
        p95 = max(latencies)
        assert p95 < 2.0, (
            f"{plan.intent} on scale s ({stats['vertices']} vertices, "
            f"{stats['edges']} edges) took {p95:.2f}s, exceeds 2s bound"
        )
        assert result is not None
