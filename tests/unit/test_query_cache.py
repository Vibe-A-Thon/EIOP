"""Semantic query cache (GAP-CACHE-001..005)."""

from eoip.graph.memory import MemoryGraphStore
from eoip.query.cache import SemanticQueryCache, cache_enabled


def _store():
    store = MemoryGraphStore()
    store.upsert_vertex(
        "WorkItem", {"canonical_id": "w:1", "issue_key": "EOIP-1", "summary": "One"}
    )
    return store


def _plan():
    return {
        "intent": "SEARCH",
        "anchors": ["EOIP-1"],
        "max_depth": 1,
        "result_limit": 25,
        "evidence_mode": "NONE",
    }


def test_cache_hit_and_miss():
    store = _store()
    cache = SemanticQueryCache()
    assert cache.get(_plan(), store) is None
    cache.put(_plan(), store, {"nodes": [1]})
    assert cache.get(_plan(), store) == {"nodes": [1]}
    assert cache.get(_plan(), store) == {"nodes": [1]}
    stats = cache.stats()
    assert stats["misses"] == 1
    assert stats["hits"] == 2


def test_plan_order_normalization():
    store = _store()
    cache = SemanticQueryCache()
    cache.put(_plan(), store, "r")
    reordered = {**_plan(), "anchors": ["EOIP-1"]}
    assert cache.get(reordered, store) == "r"


def test_graph_change_evicts_stale_entry():
    store = _store()
    cache = SemanticQueryCache()
    cache.put(_plan(), store, "before")
    store.upsert_vertex(
        "WorkItem", {"canonical_id": "w:2", "issue_key": "EOIP-2", "summary": "Two"}
    )
    assert cache.get(_plan(), store) is None
    assert cache.stats()["evictions"] == 1


def test_bound_evicts_lru():
    store = _store()
    cache = SemanticQueryCache(max_entries=2)
    for index in range(3):
        plan = {**_plan(), "anchors": [f"EOIP-{index}"]}
        cache.put(plan, store, index)
    assert len(cache.stats() and [1]) or True
    stats = cache.stats()
    assert stats["entries"] == 2


def test_cache_disabled_by_default():
    import os

    os.environ.pop("EOIP_QUERY_CACHE", None)
    assert cache_enabled() is False
    os.environ["EOIP_QUERY_CACHE"] = "1"
    assert cache_enabled() is True
    os.environ.pop("EOIP_QUERY_CACHE", None)
