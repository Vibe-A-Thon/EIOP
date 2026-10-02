import json

import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.ontology.manifest import ONTOLOGY_VERSION
from eoip.ontology.rdf import export_jsonld


def _store_with_relationships():
    store = MemoryGraphStore()
    document = store.upsert_vertex(
        "Document",
        {"canonical_id": "urn:doc:1", "name": "Architecture", "path": "architecture.md"},
    )
    section = store.upsert_vertex(
        "DocumentSection",
        {"canonical_id": "urn:section:1", "name": "Overview", "section_index": 0},
    )
    store.upsert_edge(
        "CONTAINS",
        document["vid"],
        section["vid"],
        {"edge_key": "edge:doc-section", "source_ref": "fixture:1"},
    )
    return store


def test_jsonld_export_maps_ontology_vertices_and_reified_relationships():
    document = export_jsonld(_store_with_relationships())
    graph = document["@graph"]
    ontology = next(item for item in graph if item["@type"] == "owl:Ontology")
    document_node = next(item for item in graph if item.get("@id") == "urn:doc:1")
    relation = next(
        item for item in graph if item.get("@id") == "eoip:relation/CONTAINS"
    )
    assertion = next(
        item for item in graph if item.get("@type") == "eoip:RelationshipAssertion"
    )

    assert ontology["ontologyVersion"] == ONTOLOGY_VERSION
    assert document_node["@type"] == ["owl:NamedIndividual", "eoip:entity/Document"]
    assert document_node["property_name"] == "Architecture"
    assert relation["allowedEndpointPairs"][0] == ["Project", "WorkItem"]
    assert assertion["rdf:subject"] == "urn:doc:1"
    assert assertion["rdf:predicate"] == "eoip:relation/CONTAINS"
    assert assertion["rdf:object"] == "urn:section:1"
    assert assertion["property_source_ref"] == "fixture:1"
    assert document["export"]["mapping_losses"] == []
    assert document["export"]["partial"] is False
    json.dumps(document)


def test_jsonld_export_preserves_nested_properties_as_json_literals():
    store = MemoryGraphStore()
    store.upsert_vertex(
        "IngestionRun",
        {
            "canonical_id": "urn:run:1",
            "run_kind": "fixture",
            "run_status": "SUCCEEDED",
            "counts": {"created": 2, "updated": 1},
        },
    )

    document = export_jsonld(store)
    context = document["@context"]
    run = next(item for item in document["@graph"] if item.get("@id") == "urn:run:1")

    assert context["property_counts"]["@type"] == "@json"
    assert run["property_counts"] == {"created": 2, "updated": 1}


def test_jsonld_export_is_bounded_and_reports_truncation():
    store = MemoryGraphStore()
    vertices = []
    for index in range(3):
        vertices.append(
            store.upsert_vertex(
            "Document",
            {"canonical_id": f"urn:doc:{index}", "name": f"Document {index}", "path": "doc.md"},
            )
        )
    store.upsert_edge(
        "CONTAINS",
        vertices[0]["vid"],
        vertices[1]["vid"],
        {"edge_key": "edge:truncated"},
    )
    vertices[0]["properties"]["custom_unmapped"] = "retained"

    document = export_jsonld(store, limit=2)
    losses = document["export"]["mapping_losses"]

    assert document["export"]["vertices_included"] == 2
    assert document["export"]["truncated_vertices"] is True
    assert document["export"]["truncated_edges"] is False
    assert document["export"]["partial"] is True
    assert sum(
        1
        for item in document["@graph"]
        if item.get("@type") == ["owl:NamedIndividual", "eoip:entity/Document"]
    ) == 2
    assert {
        "kind": "unsupported_property",
        "label": "custom_unmapped",
        "count": 1,
    } in losses


def test_jsonld_export_reports_edges_with_missing_export_endpoints():
    store = MemoryGraphStore()
    source = store.upsert_vertex(
        "Document",
        {"canonical_id": "urn:doc:1", "name": "First", "path": "first.md"},
    )
    target = store.upsert_vertex(
        "Document",
        {"canonical_id": "urn:doc:2", "name": "Second", "path": "second.md"},
    )
    store.upsert_edge("CONTAINS", source["vid"], target["vid"], {"edge_key": "edge:1"})

    document = export_jsonld(store, limit=1)

    assert document["export"]["truncated_vertices"] is True
    assert document["export"]["mapping_losses"] == [
        {"kind": "edge_endpoint_not_in_export", "label": "CONTAINS", "count": 1}
    ]


def test_jsonld_export_rejects_unbounded_or_invalid_limits():
    store = MemoryGraphStore()

    with pytest.raises(ValueError, match="between 1 and 10000"):
        export_jsonld(store, limit=0)
    with pytest.raises(ValueError, match="between 1 and 10000"):
        export_jsonld(store, limit=10_001)
