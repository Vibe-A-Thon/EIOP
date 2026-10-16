import pytest

from eoip.federation.planner import (
    FederatedQueryPlanner,
    InMemoryRowAdapter,
    SourceCapability,
)
from eoip.graph.memory import MemoryGraphStore
from eoip.query.unified import (
    QueryError,
    UnifiedQueryAPI,
    UnifiedQueryRequest,
    detect_mode,
)


@pytest.fixture
def api():
    store = MemoryGraphStore()
    v = {
        i: store.upsert_vertex(
            "Service",
            {"canonical_id": f"svc:{i}", "service_id": i, "name": f"{i} payment gateway"
             if i == "a" else f"{i} service"},
        )
        for i in ["a", "b", "c"]
    }
    store.upsert_edge("CALLS", v["a"]["vid"], v["b"]["vid"], {})
    store.upsert_edge("CALLS", v["b"]["vid"], v["c"]["vid"], {})
    planner = FederatedQueryPlanner()
    planner.register(InMemoryRowAdapter(
        SourceCapability(source_id="crm", entity_types=["Customer"], pushdown_filters=True),
        [{"canonical_id": "urn:crm:1", "entity_type": "Customer", "name": "Acme", "region": "EMEA"},
         {"canonical_id": "urn:crm:2", "entity_type": "Customer", "name": "Globex", "region": "APAC"}],
    ))
    return UnifiedQueryAPI(store, federation=planner)


@pytest.mark.req("GAP-QUERY")
def test_gremlin_traversal_is_really_executed(api):
    r = api.query("g.V().hasLabel('Service').has('service_id','a').out('CALLS').values('service_id')")
    assert r["mode"] == "gremlin" and r["auto_routed"] is True
    assert r["results"] == ["b"]
    two = api.query("g.V('svc:a').out('CALLS').out('CALLS').id()")
    assert two["results"] == ["svc:c"]
    assert api.query("g.V().hasLabel('Service').count()")["results"] == [3]
    assert api.query("g.V('svc:c').in('CALLS').id()")["results"] == ["svc:b"]


@pytest.mark.req("GAP-QUERY")
def test_gremlin_rejects_unsupported_and_invalid(api):
    with pytest.raises(QueryError):
        api.query("g.V().repeat(out())")
    with pytest.raises(QueryError):
        api.query("g.V(", mode="gremlin")


@pytest.mark.req("GAP-QUERY")
def test_sparql_pattern_matching_and_joins(api):
    q = ("SELECT ?s ?t WHERE { ?s eoip:relation/CALLS ?t . "
         "?s eoip:property/service_id \"a\" }")
    r = api.query(q)
    assert r["mode"] == "sparql"
    assert r["results"] == [{"s": "svc:a", "t": "svc:b"}]
    types = api.query("SELECT DISTINCT ?x WHERE { ?s a ?x } LIMIT 5")
    assert types["results"] == [{"x": "eoip:entity/Service"}]
    with pytest.raises(QueryError):
        api.query("SELECT ?z WHERE { ?s a ?x }", mode="sparql")


@pytest.mark.req("GAP-QUERY")
def test_search_and_vector_routes(api):
    s = api.query("payment gateway")
    assert s["mode"] == "search" and s["results"]
    assert s["results"][0]["canonical_id"] == "svc:a"
    v = api.query("a payment gateway", mode="vector")
    assert v["mode"] == "vector" and v["results"][0]["canonical_id"] == "svc:a"

    assert v["plan"]["backend"] == "semantic_vector_index"


@pytest.mark.req("GAP-QUERY")
def test_federated_route_with_filters(api):
    r = api.query(UnifiedQueryRequest(
        mode="federated", params={"entity_types": ["Customer"], "filters": {"region": "EMEA"}}))
    assert r["mode"] == "federated"
    assert [row["name"] for row in r["results"]] == ["Acme"]
    assert "federation" in r["plan"]


@pytest.mark.req("GAP-QUERY")
def test_eoql_route_and_uniform_envelope(api):
    r = api.query("SELECT service_id FROM Service LIMIT 2")
    assert r["mode"] == "eoql" and r["count"] == 2
    for res in (r, api.query("g.V().count()"), api.query("payment")):
        assert {"mode", "dialect", "results", "count", "plan", "elapsed_ms", "warnings"} <= set(res)


@pytest.mark.req("GAP-QUERY")
def test_limit_truncation_and_mode_validation(api):
    r = api.query("g.V().hasLabel('Service')", limit=2)
    assert r["count"] == 2 and r["truncated"] is True and r["warnings"]
    with pytest.raises(QueryError):
        api.query("x", mode="cypher")
    assert detect_mode("g.V()") == "gremlin"
    assert detect_mode("hello") == "search"
    assert UnifiedQueryAPI(MemoryGraphStore()).query("g.V().count()")["results"] == [0]
    with pytest.raises(QueryError):
        UnifiedQueryAPI(MemoryGraphStore()).query("x", mode="federated")
