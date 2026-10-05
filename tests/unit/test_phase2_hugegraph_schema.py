import json
from threading import RLock
from time import monotonic

import httpx
import pytest
from eoip.graph.hugegraph import HugeGraphStore
from eoip.graph.store import GraphQueryTimeout, graph_query_deadline
from eoip.ontology.manifest import DOCUMENT_TARGET_LABELS, EDGE_LABELS, PROPERTY_KEYS, VERTEX_LABELS


@pytest.mark.req("G2-SRC-CONF-004")
def test_document_reference_lookups_have_single_property_secondary_indexes():
    indexes = HugeGraphStore._schema_definitions()["indexlabels"]
    for label in DOCUMENT_TARGET_LABELS:
        for key in ("url", "path", "source_uri"):
            assert any(
                index["base_type"] == "VERTEX_LABEL"
                and index["base_value"] == label
                and index["index_type"] == "SECONDARY"
                and index["fields"] == [key]
                for index in indexes
            ), (label, key)


def test_schema_bootstrap_appends_new_properties_to_existing_labels():
    store = HugeGraphStore.__new__(HugeGraphStore)
    store._lock = RLock()
    store.base = "/graphspaces/DEFAULT/graphs/hugegraph"
    requests = []

    vertex_labels = [
        {
            "name": name,
            "id_strategy": "CUSTOMIZE_STRING",
            "primary_keys": [],
            "enable_label_index": True,
            "nullable_keys": [key for key in PROPERTY_KEYS if key != "canonical_id"],
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
            "source_label": out_label,
            "target_label": in_label,
            "frequency": "MULTIPLE",
            "sort_keys": ["edge_key"],
            "enable_label_index": True,
            "nullable_keys": [key for key in PROPERTY_KEYS if key != "edge_key"],
            "properties": list(PROPERTY_KEYS),
        }
        for label, (out_labels, in_labels, _) in EDGE_LABELS.items()
        for out_label in out_labels
        for in_label in in_labels
        if out_label != "KnowledgeSpace" and in_label != "KnowledgeSpace"
    ]
    schema = {
        "propertykeys": [
            {"name": key, "data_type": "TEXT" if kind == "DATE" else kind, "cardinality": "SINGLE"}
            for key, kind in PROPERTY_KEYS.items()
        ],
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


@pytest.mark.req("FR-GRAPH-003")
@pytest.mark.parametrize(
    ("kind", "field", "value"),
    [
        ("propertykeys", "data_type", "INT"),
        ("propertykeys", "cardinality", "LIST"),
        ("vertexlabels", "id_strategy", "AUTOMATIC"),
        ("vertexlabels", "primary_keys", ["name"]),
        ("vertexlabels", "enable_label_index", False),
        ("vertexlabels", "nullable_keys", ["canonical_id"]),
        ("edgelabels", "source_label", "UnexpectedLabel"),
        ("edgelabels", "target_label", "UnexpectedLabel"),
        ("edgelabels", "frequency", "SINGLE"),
        ("edgelabels", "sort_keys", ["fact_key"]),
        ("edgelabels", "enable_label_index", False),
        ("indexlabels", "index_type", "RANGE"),
        ("indexlabels", "fields", ["name"]),
        ("indexlabels", "base_value", "UnexpectedLabel"),
        ("indexlabels", "base_type", "EDGE_LABEL"),
    ],
)
def test_schema_incompatibility_blocks_all_mutations(kind, field, value):
    from copy import deepcopy

    store = HugeGraphStore.__new__(HugeGraphStore)
    store._lock = RLock()
    schema = deepcopy(store._schema_definitions())
    schema[kind][0][field] = value
    # An otherwise safe early addition must not precede a later incompatible definition.
    schema["propertykeys"] = [item for item in schema["propertykeys"] if item["name"] != "source_uri"]
    calls = []

    def request(method, path, **kwargs):
        calls.append((method, path))
        assert method == "GET", "Incompatible schema must remain untouched"
        return {path.rsplit("/", 1)[-1]: schema[path.rsplit("/", 1)[-1]]}

    store._request = request
    with pytest.raises(ValueError, match=f"Incompatible HugeGraph schema.*{field}"):
        store.ensure_schema()
    assert len(calls) == 4


@pytest.mark.req("FR-GRAPH-003")
def test_schema_bootstrap_is_read_only_when_compatible():
    store = HugeGraphStore.__new__(HugeGraphStore)
    store._lock = RLock()
    schema = store._schema_definitions()
    calls = []

    def request(method, path, **kwargs):
        calls.append((method, path))
        assert method == "GET"
        kind = path.rsplit("/", 1)[-1]
        return {kind: schema[kind]}

    store._request = request
    assert store.ensure_schema() == {"created": False, "initialized": True}
    assert len(calls) == 4


@pytest.mark.req("FR-GRAPH-003")
def test_schema_bootstrap_rejects_new_required_property_on_existing_label():
    store = HugeGraphStore.__new__(HugeGraphStore)
    store._lock = RLock()
    schema = store._schema_definitions()
    schema["vertexlabels"][0]["properties"] = [
        key for key in schema["vertexlabels"][0]["properties"] if key != "canonical_id"
    ]

    def request(method, path, **kwargs):
        assert method == "GET"
        kind = path.rsplit("/", 1)[-1]
        return {kind: schema[kind]}

    store._request = request
    with pytest.raises(ValueError, match="required properties"):
        store.ensure_schema()


@pytest.mark.req("FR-GRAPH-003")
@pytest.mark.parametrize(
    ("kind", "field"),
    [("propertykeys", "data_type"), ("vertexlabels", "properties"), ("edgelabels", "nullable_keys")],
)
def test_schema_bootstrap_refuses_missing_compatibility_metadata(kind, field):
    store = HugeGraphStore.__new__(HugeGraphStore)
    store._lock = RLock()
    schema = store._schema_definitions()
    del schema[kind][0][field]

    def request(method, path, **kwargs):
        assert method == "GET"
        requested_kind = path.rsplit("/", 1)[-1]
        return {requested_kind: schema[requested_kind]}

    store._request = request
    with pytest.raises(ValueError, match=field):
        store.ensure_schema()


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


def test_hugegraph_schema_task_waits_until_success():
    store = HugeGraphStore.__new__(HugeGraphStore)
    statuses = iter(["running", "success"])
    calls = []

    def request(method, path, **kwargs):
        calls.append((method, path))
        return {"task_status": next(statuses)}

    store._request = request

    store._wait_schema_task({"task_id": 17}, timeout_seconds=1)

    assert calls == [("GET", "/tasks/17"), ("GET", "/tasks/17")]


def test_hugegraph_exact_property_lookup_serializes_json_filter():
    store = HugeGraphStore.__new__(HugeGraphStore)
    vertex = {
        "id": "eoip-work-item",
        "label": "WorkItem",
        "properties": {"canonical_id": "urn:eoip:work:item:jira:EOIP-1", "issue_key": "EOIP-1"},
    }
    requests = []

    def pages(kind, params=None):
        requests.append((kind, params))
        yield vertex

    store._pages = pages

    result = store.find_vertex_by_property("WorkItem", "issue_key", "EOIP-1")

    assert result == [store._vertex(vertex)]
    assert requests == [
        ("vertices", {"label": "WorkItem", "properties": '{"issue_key":"EOIP-1"}'})
    ]


def test_hugegraph_search_projection_binds_inputs_and_decodes_single_properties():
    store = HugeGraphStore.__new__(HugeGraphStore)
    requests = []

    def execute(gremlin, bindings):
        requests.append((gremlin, bindings))
        return [{"id": "one", "label": "WorkItem", "properties": {
            "canonical_id": ["urn:test:one"], "name": ["Search result"],
        }}]

    store.execute_gremlin = execute
    result = store.find_search_candidates(
        properties={"name"}, label="WorkItem", filters={"summary": "'); g.V().drop(); //"},
        include_deleted=True,
    )
    assert result[0]["properties"] == {
        "canonical_id": "urn:test:one", "name": "Search result",
    }
    gremlin, bindings = requests[0]
    assert "g.V().drop()" not in gremlin
    assert bindings == {
        "search_label": "WorkItem", "include_deleted": True,
        "filter_values": {"summary": "'); g.V().drop(); //"},
        "candidate_limit": 5000, "search_properties": ["canonical_id", "name"],
    }


def test_hugegraph_gremlin_uses_graph_space_alias_and_remaining_budget():
    requests = []

    def request(req):
        requests.append(req)
        return httpx.Response(200, json={"status": {"code": 200}, "result": {"data": [1]}})

    store = HugeGraphStore("http://graph.invalid", graph="enterprise")
    store.client.close()
    store.client = httpx.Client(
        base_url="http://graph.invalid", transport=httpx.MockTransport(request)
    )
    try:
        with graph_query_deadline(monotonic() + 2):
            assert store.execute_gremlin("g.V().limit(1).count()") == [1]
        assert requests[0].url.path == "/gremlin"
        assert json.loads(requests[0].content)["aliases"] == {"g": "__g_DEFAULT-enterprise"}
        assert 0 < requests[0].extensions["timeout"]["read"] <= 2
    finally:
        store.close()


def test_hugegraph_edge_decoding_caches_only_immutable_vertex_identity():
    store = HugeGraphStore.__new__(HugeGraphStore)
    store._identity_cache = {}
    vertices = {
        "out": {
            "vid": "out",
            "canonical_id": "urn:test:project",
            "label": "Project",
            "properties": {"canonical_id": "urn:test:project", "name": "old"},
        },
        "in": {
            "vid": "in",
            "canonical_id": "urn:test:item",
            "label": "WorkItem",
            "properties": {"canonical_id": "urn:test:item", "status": "old"},
        },
    }
    calls = []

    def get_vertex(vid):
        calls.append(vid)
        vertex = vertices[vid]
        store._remember_identity(vertex)
        return vertex

    store.get_vertex = get_vertex
    raw = {
        "id": "edge-1",
        "label": "CONTAINS__Project__WorkItem",
        "outV": "out",
        "inV": "in",
        "properties": {},
    }

    first = store._edge(raw)
    vertices["out"]["properties"]["name"] = "new"
    second = store._edge(raw)

    assert first["out_cid"] == second["out_cid"] == "urn:test:project"
    assert calls == ["out", "in"]
    assert all(len(identity) == 2 for identity in store._identity_cache.values())


@pytest.mark.req("FR-INGEST-003")
def test_hugegraph_edge_upsert_updates_matching_edge_key_instead_of_duplicating():
    store = HugeGraphStore.__new__(HugeGraphStore)
    store._lock = RLock()
    vertices = {
        "out": {"vid": "out", "canonical_id": "project-1", "label": "Project", "properties": {}},
        "in": {"vid": "in", "canonical_id": "item-1", "label": "WorkItem", "properties": {}},
    }
    store.get_vertex = vertices.get
    store.find_edge_by_key = lambda key, **kwargs: {
        "eid": "edge-1",
        "label": "CONTAINS",
        "out_v": "out",
        "in_v": "in",
        "properties": {"edge_key": key},
    }
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

    edge = store.upsert_edge("CONTAINS", "out", "in", {"edge_key": "stable-key", "fact_key": "contains-1"})

    assert edge["eid"] == "edge-1"
    assert requests[0][0:2] == ("PUT", "/graph/edges/edge-1")
    assert requests[0][2]["params"] == {"action": "append"}
