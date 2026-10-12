import pytest

from eoip.graph.memory import MemoryGraphStore
from eoip.query.cache import AIResponseCache, SemanticQueryCache


@pytest.fixture
def store():
    s = MemoryGraphStore()
    s.upsert_vertex("WorkItem", {"canonical_id": "w:1", "issue_key": "EOIP-1", "summary": "One"})
    return s


def _plan(intent="SEARCH"):
    return {
        "intent": intent,
        "anchors": ["EOIP-1"],
        "max_depth": 1,
        "result_limit": 25,
        "evidence_mode": "NONE",
    }


@pytest.mark.req("GAP-CACHE-002")
def test_cache_dependencies_reference_graph_version_and_source_freshness(store):
    cache = SemanticQueryCache()
    plan = _plan()

    # Cache with graph_version v1 and git freshness seq 100
    cache.put(
        plan,
        store,
        {"data": "fresh"},
        graph_version="v1.0.0",
        source_freshness={"git": 100, "jira": 50},
    )

    # Hits when version and freshness match
    assert cache.get(plan, store, current_graph_version="v1.0.0", current_source_freshness={"git": 100, "jira": 50}) == {"data": "fresh"}

    # Invalidated when graph version advances
    assert cache.get(plan, store, current_graph_version="v2.0.0", current_source_freshness={"git": 100, "jira": 50}) is None
    assert cache.stats()["evictions"] == 1

    # Reput and test source freshness advance
    cache.put(
        plan,
        store,
        {"data": "fresh2"},
        graph_version="v2.0.0",
        source_freshness={"git": 100, "jira": 50},
    )
    # git source freshness advanced to 105 -> invalidates entry
    assert cache.get(plan, store, current_graph_version="v2.0.0", current_source_freshness={"git": 105, "jira": 50}) is None


@pytest.mark.req("GAP-CACHE-003")
def test_invalidate_using_graph_cdc(store):
    cache = SemanticQueryCache()
    plan1 = _plan("SEARCH")
    plan2 = _plan("NEIGHBORS")

    # plan1 depends on entity w:1; plan2 depends on entity w:99
    cache.put(plan1, store, {"res": 1}, touched_entities=["w:1"])
    cache.put(plan2, store, {"res": 2}, touched_entities=["w:99"])

    assert cache.stats()["entries"] == 2

    # CDC event touching w:1
    cdc_events = [{"sequence": 1, "entity_id": "w:1", "domain": "WORK", "change_type": "UPDATE"}]
    evicted_count = cache.invalidate_cdc(cdc_events)
    assert evicted_count == 1

    # plan1 evicted, plan2 remains
    assert cache.get(plan1, store) is None
    assert cache.get(plan2, store) == {"res": 2}


@pytest.mark.req("GAP-CACHE-004")
def test_separate_deterministic_query_cache_from_ai_response_cache(store):
    det_cache = SemanticQueryCache()
    ai_cache = AIResponseCache()

    # Deterministic cache stores structured query result
    det_plan = _plan()
    det_cache.put(det_plan, store, {"nodes": ["w:1"]})

    # AI cache stores synthesized text from LLM with temperature & model parameters
    prompt = "Summarize issue EOIP-1"
    ai_cache.put(prompt, "Issue EOIP-1 describes item One.", model="claude-3-5", temperature=0.2)

    # Independent boundaries and lookup keys
    assert det_cache.get(det_plan, store) == {"nodes": ["w:1"]}
    assert ai_cache.get(prompt, model="claude-3-5", temperature=0.2) == "Issue EOIP-1 describes item One."

    # Varying model or temperature misses AI cache without affecting deterministic cache
    assert ai_cache.get(prompt, model="claude-3-5", temperature=0.7) is None
    assert ai_cache.get(prompt, model="gpt-4o", temperature=0.2) is None

    # Clearing AI cache does not touch deterministic query cache
    ai_cache.clear()
    assert ai_cache.stats()["entries"] == 0
    assert det_cache.get(det_plan, store) == {"nodes": ["w:1"]}


@pytest.mark.req("GAP-CACHE-005")
def test_do_not_serve_stale_results_beyond_policy(store):
    cache = SemanticQueryCache()
    plan = _plan()

    # Cache with max_staleness of 60 seconds at t=1000
    cache.put(plan, store, {"computed": True}, max_staleness_seconds=60.0, created_at=1000.0)

    # Within staleness window (t=1030)
    assert cache.get(plan, store, now=1030.0) == {"computed": True}

    # Beyond staleness window (t=1065) -> must not serve, evicts
    assert cache.get(plan, store, now=1065.0) is None
    assert cache.stats()["evictions"] == 1
