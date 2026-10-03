"""Native bounded bulk loading (GAP-HG-004, G2-EVOL-010)."""

from threading import RLock

import pytest
from eoip.graph.hugegraph import HugeGraphStore
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.store import BulkLoadError


def _snapshot():
    vertices = [
        {
            "vid": "old-project",
            "canonical_id": "urn:bulk:project",
            "label": "Project",
            "properties": {"canonical_id": "urn:bulk:project", "name": "Bulk project"},
        },
        {
            "vid": "old-item",
            "canonical_id": "urn:bulk:item",
            "label": "WorkItem",
            "properties": {
                "canonical_id": "urn:bulk:item",
                "issue_key": "BULK-1",
                "summary": "Bulk item",
            },
        },
    ]
    edges = [
        {
            "eid": "old-edge",
            "label": "CONTAINS",
            "out_v": "old-project",
            "in_v": "old-item",
            "out_cid": "urn:bulk:project",
            "in_cid": "urn:bulk:item",
            "properties": {"fact_key": "contains-1"},
        }
    ]
    return vertices, edges


@pytest.mark.req("GAP-HG-004", "G2-EVOL-010")
def test_memory_bulk_load_validates_then_commits_atomically():
    vertices, edges = _snapshot()
    store = MemoryGraphStore()

    result = store.bulk_load(vertices, edges, batch_size=1)

    assert result == {
        "vertices": 2,
        "edges": 1,
        "vertex_batches": 2,
        "edge_batches": 1,
        "batch_size": 1,
        "mode": "atomic-memory",
    }
    assert store.count_vertices() == 2
    assert store.count_edges() == 1


def test_memory_bulk_load_invalid_edge_leaves_target_empty():
    vertices, edges = _snapshot()
    edges[0]["in_v"] = "missing"
    store = MemoryGraphStore()

    with pytest.raises(ValueError, match="missing vertex"):
        store.bulk_load(vertices, edges)

    assert store.count_vertices() == 0
    assert store.count_edges() == 0


def _hugegraph_stub():
    store = HugeGraphStore.__new__(HugeGraphStore)
    store._lock = RLock()
    store._identity_cache = {}
    store.count_vertices = lambda: 0
    store.count_edges = lambda: 0
    schema_calls = []
    store.ensure_schema = lambda manifest: schema_calls.append(manifest) or {"initialized": True}
    requests = []

    def request(method, path, **kwargs):
        requests.append((method, path, kwargs))
        if path.endswith("vertices/batch"):
            return [item["id"] for item in kwargs["json"]]
        return [f"edge-{index}" for index, _item in enumerate(kwargs["json"])]

    store._request = request
    return store, schema_calls, requests


@pytest.mark.req("GAP-HG-004", "G2-EVOL-010")
def test_hugegraph_bulk_load_uses_bounded_native_batches():
    vertices, edges = _snapshot()
    store, schema_calls, requests = _hugegraph_stub()

    result = store.bulk_load(vertices, edges, batch_size=1)

    assert result["mode"] == "hugegraph-native-post"
    assert result["vertex_batches"] == 2
    assert result["edge_batches"] == 1
    assert schema_calls == [{}]
    assert [item[1] for item in requests] == [
        "/graph/vertices/batch",
        "/graph/vertices/batch",
        "/graph/edges/batch",
    ]
    edge_request = requests[-1][2]
    assert edge_request["params"] == {"check_vertex": True}
    assert edge_request["json"][0]["label"] == "CONTAINS__Project__WorkItem"
    assert edge_request["json"][0]["properties"]["edge_key"]


def test_hugegraph_bulk_load_prevalidates_before_schema_or_writes():
    vertices, edges = _snapshot()
    edges[0]["in_v"] = "missing"
    store, schema_calls, requests = _hugegraph_stub()

    with pytest.raises(ValueError, match="missing vertex"):
        store.bulk_load(vertices, edges)

    assert schema_calls == []
    assert requests == []


def test_hugegraph_bulk_load_reports_committed_batches_on_failure():
    vertices, edges = _snapshot()
    store, _schema_calls, requests = _hugegraph_stub()

    def request(method, path, **kwargs):
        requests.append((method, path, kwargs))
        if path.endswith("vertices/batch"):
            return [item["id"] for item in kwargs["json"]]
        raise RuntimeError("backend rejected edge batch")

    store._request = request

    with pytest.raises(BulkLoadError) as captured:
        store.bulk_load(vertices, edges, batch_size=2)

    assert captured.value.vertices_committed == 2
    assert captured.value.edges_committed == 0
    assert "discard the isolated graph" in str(captured.value)


def test_bulk_load_refuses_a_nonempty_hugegraph():
    vertices, edges = _snapshot()
    store, schema_calls, requests = _hugegraph_stub()
    store.count_vertices = lambda: 1

    with pytest.raises(RuntimeError, match="empty graph"):
        store.bulk_load(vertices, edges)

    assert schema_calls == []
    assert requests == []
