"""Tests for canonical-contract-validated ingestion pipeline (P1-19)."""

import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.pipeline import validate_and_write_entity, validate_and_write_relationship


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
    with pytest.raises(Exception):
        validate_and_write_entity(
            store,
            label="BogusLabel",
            canonical_id="urn:bogus:1",
            properties={"name": "bogus"},
        )
