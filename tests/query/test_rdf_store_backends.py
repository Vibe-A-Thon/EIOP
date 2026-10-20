"""CRA-024.11 / CRA-002.10 / ONT-003: the GraphStore port runs on real RDF stores over SPARQL 1.1.

Live cases run on Apache Jena Fuseki (EOIP_LIVE_FUSEKI_URL) and Ontotext GraphDB Free
(EOIP_LIVE_GRAPHDB_URL) - CI job rdf-stores. Every operation round-trips through the server: a second
client instance (no shared process state) reads what the first wrote. Without a reachable store, operations
fail loudly; nothing is cached locally.
"""
from __future__ import annotations

import os

import pytest
from eoip.graph.rdf_backend import FusekiGraphStore, GraphDBGraphStore, RDFStoreError, create_rdf_store_from_config

pytestmark = pytest.mark.req("CRA-024", "CRA-002", "ONT-003")


def _fuseki():
    url = os.getenv("EOIP_LIVE_FUSEKI_URL")
    if not url:
        pytest.skip("no live Fuseki (set EOIP_LIVE_FUSEKI_URL)")
    kw = dict(endpoint_url=url, username=os.getenv("EOIP_LIVE_FUSEKI_USER", "admin"),
              password=os.getenv("EOIP_LIVE_FUSEKI_PASSWORD", ""))
    return lambda: FusekiGraphStore(**kw)


def _graphdb():
    url = os.getenv("EOIP_LIVE_GRAPHDB_URL")
    if not url:
        pytest.skip("no live GraphDB (set EOIP_LIVE_GRAPHDB_URL)")
    return lambda: GraphDBGraphStore(endpoint_url=url, repository=os.getenv("EOIP_LIVE_GRAPHDB_REPO", "eoip"))


@pytest.fixture(params=["fuseki", "graphdb"])
def stores(request):
    factory = _fuseki() if request.param == "fuseki" else _graphdb()
    writer = factory()
    writer.clear()
    yield writer, factory()  # (writer, independent reader)
    writer.clear()


def test_vertex_round_trip_merge_and_typed_lookup(stores):
    w, r = stores
    w.upsert_vertex("Service", {"canonical_id": "svc:pay", "name": "Payments", "tier": 1, "quote": 'a "b" \\ c'})
    w.upsert_vertex("Service", {"canonical_id": "svc:pay", "owner": "team-red"})  # merge, like the memory store
    got = r.get_vertex_by_canonical_id("svc:pay")
    assert got["label"] == "Service"
    assert got["properties"] == {"canonical_id": "svc:pay", "name": "Payments", "tier": 1,
                                 "quote": 'a "b" \\ c', "owner": "team-red"}
    assert [v["canonical_id"] for v in r.find_vertex_by_property("Service", "tier", 1)] == ["svc:pay"]
    assert r.find_vertex_by_property("Service", "tier", "1") == []  # typed literals, no string coercion
    assert r.count_vertices("Service") == 1 and r.count_vertices("Person") == 0


def test_injection_shaped_values_are_data(stores):
    w, r = stores
    evil = 'x" } ; DROP ALL ; INSERT DATA { <urn:a> <urn:b> "c'
    w.upsert_vertex("Person", {"canonical_id": "p:1", "name": evil})
    w.upsert_vertex("Person", {"canonical_id": "p:2> <urn:x", "name": "n"})
    assert r.get_vertex_by_canonical_id("p:1")["properties"]["name"] == evil
    assert r.get_vertex_by_canonical_id("p:2> <urn:x")["properties"]["name"] == "n"
    assert r.count_vertices() == 2


def test_edges_traversal_and_tombstone(stores):
    w, r = stores
    for cid in ("svc:a", "svc:b", "svc:c"):
        w.upsert_vertex("Service", {"canonical_id": cid, "name": cid})
    w.upsert_edge("DEPENDS_ON", "svc:a", "svc:b", {"weight": 0.5})
    w.upsert_edge("DEPENDS_ON", "svc:a", "svc:c", {})
    w.upsert_edge("DEPENDS_ON", "svc:a", "svc:b", {"weight": 0.9})  # upsert replaces
    assert r.count_edges("DEPENDS_ON") == 2
    assert sorted(e["in_v"] for e in r.edges_from("svc:a")) == ["svc:b", "svc:c"]
    assert r.get_edge("svc:a->DEPENDS_ON->svc:b")["properties"] == {"weight": 0.9}
    assert [e["out_v"] for e in r.edges_to("svc:c", labels=["DEPENDS_ON"])] == ["svc:a"]
    # the navigable triple is queryable with plain SPARQL on the server
    rows = r._rows("SELECT ?o WHERE { <urn:eoip:v:svc%3Aa> <urn:eoip:rel#DEPENDS_ON> ?o } ORDER BY ?o")
    assert [x["o"] for x in rows] == ["urn:eoip:v:svc%3Ab", "urn:eoip:v:svc%3Ac"]
    assert w.tombstone_vertex("svc:c") and r.get_vertex_by_canonical_id("svc:c") is None
    assert len(r.find_vertices("Service", include_deleted=True)) == 3 and r.count_vertices("Service") == 2
    assert w.tombstone_vertex("svc:c") is False


def test_bulk_load_and_health(stores):
    w, r = stores
    vs = [{"label": "Service", "properties": {"canonical_id": f"svc:{i}", "name": f"s{i}"}} for i in range(1200)]
    out = w.bulk_load(vs, [], batch_size=500)
    assert out["vertices_in_store"] == 1200 and r.count_vertices("Service") == 1200
    assert r.ping()["healthy"] and r.schema_status()["status"] == "READY"


def test_unreachable_store_fails_loudly_and_config_targets_both():
    dead = FusekiGraphStore(endpoint_url="http://127.0.0.1:9/ds", timeout=2)
    with pytest.raises(RDFStoreError):
        dead.upsert_vertex("Service", {"canonical_id": "svc:x"})
    with pytest.raises(RDFStoreError):
        dead.get_vertex("svc:x")
    assert dead.health() is False and dead.schema_status()["status"] == "UNAVAILABLE"
    with pytest.raises(RDFStoreError):
        dead.ensure_schema({})
    g = create_rdf_store_from_config({"backend": "graphdb", "endpoint_url": "http://gdb:7200", "repository": "r"})
    assert isinstance(g, GraphDBGraphStore)
    assert (g.query_url, g.update_url) == ("http://gdb:7200/repositories/r", "http://gdb:7200/repositories/r/statements")
    f = create_rdf_store_from_config({"backend": "fuseki", "endpoint_url": "http://f:3030/ds"})
    assert (f.query_url, f.update_url) == ("http://f:3030/ds/sparql", "http://f:3030/ds/update")
    with pytest.raises(ValueError):
        create_rdf_store_from_config({"backend": "blazegraph"})
