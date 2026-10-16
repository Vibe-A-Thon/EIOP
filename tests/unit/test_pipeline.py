"""Tests for canonical-contract-validated ingestion pipeline (P1-19)."""

import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.pipeline import validate_and_write_entity, validate_and_write_relationship
from eoip.validation.gate import MutationBlocked


def test_validated_entity_writes_to_store():
    store = MemoryGraphStore()
    result = validate_and_write_entity(
        store,
        label="WorkItem",
        canonical_id="urn:test:item:1",
        properties={"issue_key": "TEST-1", "summary": "Test"},
        source_refs=["jira://issue/TEST-1"],
        ingestion_run_id="run-001",
    )
    assert result["canonical_id"] == "urn:test:item:1"
    assert store.get_vertex_by_canonical_id("urn:test:item:1") is not None


def test_validated_relationship_writes_to_store():
    store = MemoryGraphStore()
    store.upsert_vertex("WorkItem", {"canonical_id": "urn:w1", "issue_key": "W-1"})
    store.upsert_vertex("Evidence", {"canonical_id": "urn:e1", "source_system": "test", "method": "TEST", "evidence_key": "ek1"})
    result = validate_and_write_relationship(
        store,
        label="EVIDENCED_BY",
        from_id="urn:w1",
        to_id="urn:e1",
        properties={"fact_key": "test:1"},
        evidence_refs=["test://1"],
        ingestion_run_id="run-001",
    )
    assert result["label"] == "EVIDENCED_BY"


def test_validated_entity_rejects_unknown_label():
    store = MemoryGraphStore()
    with pytest.raises(MutationBlocked, match="unknown vertex label"):
        validate_and_write_entity(
            store,
            label="BogusLabel",
            canonical_id="urn:bogus:1",
            properties={"name": "bogus"},
            ingestion_run_id="run-1",
        )


def test_entity_identity_cannot_be_overridden_by_properties():
    store = MemoryGraphStore()
    with pytest.raises(MutationBlocked, match="canonical_id"):
        validate_and_write_entity(
            store, "WorkItem", "urn:expected",
            {"canonical_id": "urn:override"}, ingestion_run_id="run-1",
        )
    assert store.count_vertices() == 0


@pytest.mark.parametrize("confidence", [-0.1, 1.1, "not-a-number", True])
def test_property_confidence_is_validated_before_write(confidence):
    store = MemoryGraphStore()
    with pytest.raises(ValueError):
        validate_and_write_entity(
            store, "WorkItem", "urn:item", {"confidence": confidence},
            ingestion_run_id="run-1",
        )
    assert store.count_vertices() == 0


def test_mutation_requires_a_real_run_id():
    store = MemoryGraphStore()
    with pytest.raises(ValueError, match="ingestion_run_id"):
        validate_and_write_entity(store, "WorkItem", "urn:item", {})
    assert store.count_vertices() == 0


def test_relationship_accepts_physical_ids_without_changing_fact_identity():
    store = MemoryGraphStore()
    source = store.upsert_vertex("WorkItem", {"canonical_id": "urn:item"})
    target = store.upsert_vertex("Evidence", {"canonical_id": "urn:evidence"})
    first = validate_and_write_relationship(
        store, "EVIDENCED_BY", source["vid"], target["vid"],
        {"fact_key": "fact-1"}, ingestion_run_id="run-1",
    )
    repeated = validate_and_write_relationship(
        store, "EVIDENCED_BY", "urn:item", "urn:evidence",
        {"fact_key": "fact-1"}, ingestion_run_id="run-2",
    )
    second = validate_and_write_relationship(
        store, "EVIDENCED_BY", "urn:item", "urn:evidence",
        {"fact_key": "fact-2"}, ingestion_run_id="run-2",
    )
    assert first["eid"] == repeated["eid"]
    assert first["eid"] != second["eid"]
    assert first["out_cid"] == "urn:item"


@pytest.mark.parametrize("properties", [
    {"graph_domain": "CODE"}, {"creation_status": "INVENTED"},
])
def test_entity_rejects_contradictory_or_unsupported_properties(properties):
    store = MemoryGraphStore()
    with pytest.raises(ValueError):
        validate_and_write_entity(
            store, "WorkItem", "urn:item", properties, ingestion_run_id="run-1",
        )
    assert store.count_vertices() == 0


def test_revision_preserves_subject_type_without_changing_envelope_type():
    store = MemoryGraphStore()
    revision = validate_and_write_entity(
        store, "EntityRevision", "urn:revision",
        {"entity_type": "WorkItem"}, ingestion_run_id="run-1",
    )
    assert revision["label"] == "EntityRevision"
    assert revision["properties"]["entity_type"] == "WorkItem"


def test_relationship_contract_failure_does_not_create_edge():
    store = MemoryGraphStore()
    store.upsert_vertex("WorkItem", {"canonical_id": "urn:item"})
    store.upsert_vertex("Evidence", {"canonical_id": "urn:evidence"})
    with pytest.raises(ValueError, match="confidence"):
        validate_and_write_relationship(
            store, "EVIDENCED_BY", "urn:item", "urn:evidence",
            {"fact_key": "fact", "confidence": 2.0}, ingestion_run_id="run-1",
        )
    assert store.count_edges() == 0
