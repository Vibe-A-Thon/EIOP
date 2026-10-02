from threading import RLock

from eoip.graph.hugegraph import HugeGraphStore
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
