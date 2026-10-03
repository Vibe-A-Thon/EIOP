"""Edge dedup (FR-INGEST-003): re-ingesting must not duplicate edges.

MemoryGraphStore has always deduped by edge_key; these tests pin the same
idempotency contract on the HugeGraph adapter.
"""

from threading import RLock

from eoip.graph.hugegraph import HugeGraphStore
from eoip.graph.memory import MemoryGraphStore


def _seeded_store():
    store = MemoryGraphStore()
    project = store.upsert_vertex("Project", {"canonical_id": "urn:test:project:1", "name": "P"})
    item = store.upsert_vertex(
        "WorkItem", {"canonical_id": "urn:test:item:1", "issue_key": "T-1", "summary": "S"}
    )
    return store, project, item


def test_memory_store_upsert_same_edge_key_twice_returns_same_edge():
    store, project, item = _seeded_store()

    first = store.upsert_edge("CONTAINS", project["vid"], item["vid"], {"edge_key": "k-1"})
    second = store.upsert_edge("CONTAINS", project["vid"], item["vid"], {"edge_key": "k-1"})

    assert first["eid"] == second["eid"]
    assert store.count_edges("CONTAINS") == 1
    assert store.find_edge_by_key("k-1") is not None


def test_memory_store_upsert_without_edge_key_still_creates():
    store, project, item = _seeded_store()

    edge = store.upsert_edge("CONTAINS", project["vid"], item["vid"], {"fact_key": "f-1"})

    assert edge["properties"]["edge_key"]
    assert store.count_edges("CONTAINS") == 1
    assert store.find_edge_by_key(edge["properties"]["edge_key"])["eid"] == edge["eid"]


def _hugegraph_stub():
    store = HugeGraphStore.__new__(HugeGraphStore)
    store._lock = RLock()
    vertices = {
        "out": {"vid": "out", "canonical_id": "urn:test:project:1", "label": "Project", "properties": {}},
        "in": {
            "vid": "in",
            "canonical_id": "urn:test:item:1",
            "label": "WorkItem",
            "properties": {},
        },
    }
    store.get_vertex = vertices.get
    found = []
    store.find_edges = lambda **kwargs: list(found)
    requests = []

    def request(method, path, **kwargs):
        requests.append((method, path, kwargs))
        return {
            "id": "edge-1",
            "label": "CONTAINS__Project__WorkItem",
            "outV": "out",
            "inV": "in",
            "properties": kwargs["json"].get("properties") or {"edge_key": "k-1"},
        }

    store._request = request
    return store, found, requests


def test_hugegraph_second_upsert_with_same_edge_key_does_not_post():
    store, found, requests = _hugegraph_stub()

    first = store.upsert_edge("CONTAINS", "out", "in", {"edge_key": "k-1", "fact_key": "f-1"})
    assert ("POST", "/graph/edges") in [(method, path) for method, path, _ in requests]
    assert first["eid"] == "edge-1"

    found.append(
        {
            "eid": "edge-1",
            "label": "CONTAINS",
            "out_v": "out",
            "in_v": "in",
            "out_cid": "urn:test:project:1",
            "in_cid": "urn:test:item:1",
            "properties": {"edge_key": "k-1"},
        }
    )
    requests.clear()

    second = store.upsert_edge("CONTAINS", "out", "in", {"edge_key": "k-1", "fact_key": "f-1"})

    assert second["eid"] == "edge-1"
    posted = [entry for entry in requests if entry[0:2] == ("POST", "/graph/edges")]
    assert not posted, f"duplicate edge POSTed: {posted}"
    assert requests[0][0:2] == ("PUT", "/graph/edges/edge-1")


def test_hugegraph_upsert_without_edge_key_still_creates():
    store, _found, requests = _hugegraph_stub()

    edge = store.upsert_edge("CONTAINS", "out", "in", {"fact_key": "f-2"})

    assert edge["eid"] == "edge-1"
    assert ("POST", "/graph/edges") in [(method, path) for method, path, _ in requests]
