import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.ontology.rdf import (
    export_jsonld,
    export_shacl_shapes,
    import_jsonld,
    validate_jsonld_round_trip,
    validate_shacl,
)


def _semantic_store() -> MemoryGraphStore:
    store = MemoryGraphStore()
    work_item = store.upsert_vertex(
        "WorkItem",
        {
            "canonical_id": "jira://PROJ-42",
            "issue_key": "PROJ-42",
            "summary": "Implement payment gateway trace",
            "status": "In Progress",
        },
    )
    commit = store.upsert_vertex(
        "Commit",
        {
            "canonical_id": "git://payments/commit/abc123",
            "commit_sha": "abc123",
            "message": "Add trace propagation",
            "author_email": "engineer@example.com",
        },
    )
    store.upsert_edge(
        "IMPLEMENTS",
        commit["vid"],
        work_item["vid"],
        {"edge_key": "edge:implements:abc123:PROJ-42", "source_ref": "git://payments/commit/abc123"},
    )
    return store


@pytest.mark.req("GAP-DUAL")
@pytest.mark.req("GAP-DUAL-001")
@pytest.mark.req("GAP-DUAL-002")
@pytest.mark.req("FR-GRAPH-010")
def test_jsonld_import_reconstructs_supported_property_graph_records():
    source = _semantic_store()
    document = export_jsonld(source)
    restored = MemoryGraphStore()

    report = import_jsonld(document, restored)
    work_item = restored.get_vertex_by_canonical_id("jira://PROJ-42")
    commit = restored.get_vertex_by_canonical_id("git://payments/commit/abc123")
    edges = restored.find_edges(label="IMPLEMENTS")

    assert report == {"vertices": 2, "edges": 1, "skipped_edges": 0, "mapping_losses": []}
    assert work_item["label"] == "WorkItem"
    assert work_item["properties"]["issue_key"] == "PROJ-42"
    assert commit["properties"]["commit_sha"] == "abc123"
    assert edges[0]["out_cid"] == "git://payments/commit/abc123"
    assert edges[0]["in_cid"] == "jira://PROJ-42"
    assert edges[0]["properties"]["source_ref"] == "git://payments/commit/abc123"


@pytest.mark.req("GAP-DUAL")
@pytest.mark.req("GAP-DUAL-001")
@pytest.mark.req("GAP-DUAL-002")
def test_round_trip_validator_confirms_lossless_supported_constructs():
    result = validate_jsonld_round_trip(_semantic_store())

    assert result["conforms"] is True
    assert result["original"] == {"vertices": 2, "edges": 1}
    assert result["restored"] == {"vertices": 2, "edges": 1}
    assert result["issues"] == []


@pytest.mark.req("GAP-DUAL")
@pytest.mark.req("GAP-DUAL-001")
def test_shacl_shapes_expose_required_properties_and_relationship_ranges():
    shapes = export_shacl_shapes()
    work_item_shape = next(item for item in shapes["@graph"] if item["@id"] == "eoip:shape/WorkItem")
    implements_shape = next(
        item for item in shapes["@graph"] if item["@id"] == "eoip:shape/relation/IMPLEMENTS"
    )

    required_paths = {constraint["sh:path"] for constraint in work_item_shape["sh:property"]}
    assert "eoip:property/issue_key" in required_paths
    assert "eoip:property/summary" in required_paths
    assert ["Commit", "WorkItem"] in implements_shape["allowedEndpointPairs"]
    assert ["MergeRequest", "WorkItem"] in implements_shape["allowedEndpointPairs"]


@pytest.mark.req("GAP-DUAL")
@pytest.mark.req("GAP-DUAL-001")
def test_shacl_validator_reports_missing_required_properties():
    store = MemoryGraphStore()
    store.upsert_vertex(
        "WorkItem",
        {"canonical_id": "jira://PROJ-99", "issue_key": "PROJ-99"},
    )

    result = validate_shacl(store)

    assert result["conforms"] is False
    assert result["checked"] == {
        "vertices": 1,
        "edges": 0,
        "partial": False,
        "truncated_vertices": False,
        "truncated_edges": False,
    }
    assert result["results"] == [
        {
            "focusNode": "jira://PROJ-99",
            "sourceShape": "eoip:shape/WorkItem",
            "resultPath": "eoip:property/summary",
            "severity": "Violation",
            "message": "WorkItem requires property summary",
        }
    ]
