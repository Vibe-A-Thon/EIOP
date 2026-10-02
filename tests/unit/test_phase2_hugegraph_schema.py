from threading import RLock
from time import monotonic

import httpx
import pytest
from eoip.graph.hugegraph import HugeGraphStore
from eoip.graph.store import GraphQueryTimeout, graph_query_deadline
from eoip.ontology.manifest import EDGE_LABELS, PROPERTY_KEYS, VERTEX_LABELS


def test_schema_bootstrap_appends_new_properties_to_existing_labels():
    store = HugeGraphStore.__new__(HugeGraphStore)
    store._lock = RLock()
    store.base = "/graphspaces/DEFAULT/graphs/hugegraph"
    requests = []

    vertex_labels = [
        {
            "name": name,
            "properties": [
                key for key in PROPERTY_KEYS if not (name == "Document" and key == "description")
            ],
        }
        for name in VERTEX_LABELS
        if name != "KnowledgeSpace"
    ]
    edge_labels = [
        {
            "name": f"{label}__{out_label}__{in_label}",
            "properties": list(PROPERTY_KEYS),
        }
        for label, (out_labels, in_labels, _) in EDGE_LABELS.items()
        for out_label in out_labels
        for in_label in in_labels
        if out_label != "KnowledgeSpace" and in_label != "KnowledgeSpace"
    ]
    schema = {
        "propertykeys": [{"name": key} for key in PROPERTY_KEYS],
        "vertexlabels": vertex_labels,
        "edgelabels": edge_labels,
        "indexlabels": [],
    }

    def request(method, path, **kwargs):
        requests.append((method, path, kwargs))
        kind = path.rsplit("/", 1)[-1]
        if method == "GET":
            return {kind: schema[kind]}
        return {}

    store._request = request

    result = store.ensure_schema()

    assert result == {"created": True, "initialized": True}
    append_document = next(
        request
        for request in requests
        if request[0] == "PUT" and request[1] == "/schema/vertexlabels/Document"
    )
    assert append_document[2] == {
        "params": {"action": "append"},
        "json": {
            "name": "Document",
            "properties": ["description"],
            "nullable_keys": ["description"],
        },
    }
    assert any(
        method == "POST"
        and path == "/schema/vertexlabels"
        and kwargs["json"]["name"] == "KnowledgeSpace"
        for method, path, kwargs in requests
    )


def test_hugegraph_request_timeout_uses_active_traversal_deadline():
    store = HugeGraphStore.__new__(HugeGraphStore)
    store.base = "/graph"

    class TimeoutClient:
        timeout = None

        def request(self, method, path, **kwargs):
            self.timeout = kwargs["timeout"]
            raise httpx.ReadTimeout("request timed out")

    store.client = TimeoutClient()

    with graph_query_deadline(monotonic() + 10.0), pytest.raises(
        GraphQueryTimeout, match="time budget"
    ):
        store._request("GET", "/vertices/1")

    assert 0 < store.client.timeout <= 10.0


@pytest.mark.req("FR-INGEST-003")
def test_hugegraph_edge_upsert_updates_matching_edge_key_instead_of_duplicating():
    store = HugeGraphStore.__new__(HugeGraphStore)
    store._lock = RLock()
    vertices = {
        "out": {"vid": "out", "canonical_id": "project-1", "label": "Project", "properties": {}},
        "in": {"vid": "in", "canonical_id": "item-1", "label": "WorkItem", "properties": {}},
    }
    store.get_vertex = vertices.get
    store.find_edges = lambda **kwargs: [
        {
            "eid": "edge-1",
            "label": "CONTAINS",
            "out_v": "out",
            "in_v": "in",
            "properties": {"edge_key": "stable-key"},
        }
    ]
    requests = []

    def request(method, path, **kwargs):
        requests.append((method, path, kwargs))
        return {
            "id": "edge-1",
            "label": "CONTAINS__Project__WorkItem",
            "outV": "out",
            "inV": "in",
            "properties": kwargs["json"]["properties"],
        }

    store._request = request

    edge = store.upsert_edge(
        "CONTAINS", "out", "in", {"edge_key": "stable-key", "fact_key": "contains-1"}
    )

    assert edge["eid"] == "edge-1"
    assert requests[0][0:2] == ("PUT", "/graph/edges/edge-1")
    assert requests[0][2]["params"] == {"action": "append"}
