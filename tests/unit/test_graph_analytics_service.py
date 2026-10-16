import pytest
from eoip.analytics.service import (
    AlgorithmRegistry,
    GraphAnalyticsService,
    UnknownAlgorithm,
    connected_components,
    k_core,
    shortest_path,
    triangle_count,
)
from eoip.graph.memory import MemoryGraphStore


@pytest.fixture
def svc():
    store = MemoryGraphStore()
    ids = ["a", "b", "c", "d", "x", "y"]
    v = {
        i: store.upsert_vertex("Service", {"canonical_id": f"svc:{i}", "service_id": i, "name": i})
        for i in ids
    }
    # triangle a-b-c, tail c-d, separate pair x-y
    for s, t in [("a", "b"), ("b", "c"), ("c", "a"), ("c", "d"), ("x", "y")]:
        store.upsert_edge("CALLS", v[s]["vid"], v[t]["vid"], {})
    return GraphAnalyticsService(store)


@pytest.mark.req("GAP-GDS")
def test_catalog_lists_standard_algorithms(svc):
    names = {a["name"] for a in svc.catalog()}
    assert {
        "pagerank", "betweenness", "closeness", "degree", "leiden",
        "label_propagation", "connected_components", "k_core",
        "triangle_count", "clustering_coefficient", "shortest_path",
        "jaccard_similarity",
    } <= names


@pytest.mark.req("GAP-GDS")
def test_components_triangles_and_kcore(svc):
    comps = svc.run("connected_components").values
    assert comps["svc:a"] == comps["svc:d"] != comps["svc:x"] == comps["svc:y"]
    tri = svc.run("triangle_count").values
    assert tri["svc:a"] == tri["svc:b"] == tri["svc:c"] == 1 and tri["svc:d"] == 0
    cc = svc.run("clustering_coefficient").values
    assert cc["svc:a"] == 1.0 and cc["svc:c"] == pytest.approx(1 / 3)
    core = svc.run("k_core").values
    assert core["svc:a"] == 2 and core["svc:d"] == 1 and core["svc:x"] == 1


@pytest.mark.req("GAP-GDS")
def test_shortest_path_directed_and_weighted():
    adj = {"a": {"b": 1.0, "c": 5.0}, "b": {"c": 1.0}, "c": {}}
    r = shortest_path(adj, source="a", target="c")
    assert r["path"] == ["a", "b", "c"] and r["distance"] == 2.0
    assert shortest_path(adj, source="c", target="a")["found"] is False
    with pytest.raises(ValueError):
        shortest_path({"a": {"b": -1.0}, "b": {}}, source="a", target="b")


@pytest.mark.req("GAP-GDS")
def test_centrality_community_and_similarity(svc):
    pr = svc.run("pagerank").values
    assert sum(pr.values()) == pytest.approx(1.0, abs=1e-3)
    bt = svc.run("betweenness").values
    assert max(bt, key=bt.get) == "svc:c"
    lp = svc.run("label_propagation").values
    assert lp["svc:x"] == lp["svc:y"] != lp["svc:a"]
    sim = svc.run("jaccard_similarity", node="svc:a").values
    assert [r["node"] for r in sim[:2]] == ["svc:d", "svc:b"] and sim[0]["score"] == 0.5


@pytest.mark.req("GAP-GDS")
def test_plugin_registration_and_errors(svc):
    svc.registry.register_function("node_count", lambda adj: len(adj))
    res = svc.run("node_count")
    assert res.values == 6 and res.to_dict()["category"] == "custom"
    with pytest.raises(ValueError):
        svc.registry.register_function("node_count", lambda adj: 0)
    assert svc.registry.unregister("node_count") is True
    with pytest.raises(UnknownAlgorithm):
        svc.run("node_count")
    assert AlgorithmRegistry(with_builtins=False).catalog() == []


@pytest.mark.req("GAP-GDS")
def test_edge_label_filter_projects_subgraph(svc):
    res = svc.run("connected_components", edge_labels=["DEPENDS_ON"])
    assert len(set(res.values.values())) == res.node_count  # no DEPENDS_ON edges
