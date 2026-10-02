"""Tests for the provenance evidence and lineage services."""

from eoip.graph.memory import MemoryGraphStore
from eoip.provenance.lineage import LineageService


def _store_with_lineage():
    store = MemoryGraphStore()
    wi = store.upsert_vertex("WorkItem", {
        "canonical_id": "urn:test:item:1", "issue_key": "TEST-1", "summary": "Test",
        "ingestion_run_id": "run-1",
    })
    evidence = store.upsert_vertex("Evidence", {
        "canonical_id": "urn:test:evidence:1",
        "source_system": "jira", "source_ref": "jira://TEST-1", "method": "SOURCE_EVENT",
    })
    run = store.upsert_vertex("IngestionRun", {
        "canonical_id": "urn:test:run:1",
        "run_status": "SUCCEEDED", "run_kind": "JIRA_JSON",
    })
    store.upsert_edge("EVIDENCED_BY", wi["vid"], evidence["vid"], {
        "fact_key": "ev-link", "creation_status": "DETERMINISTIC",
    })
    store.upsert_edge("INGESTED_IN", wi["vid"], run["vid"], {
        "fact_key": "run-link", "creation_status": "DETERMINISTIC",
    })
    return store


def test_lineage_traces_to_source():
    store = _store_with_lineage()
    service = LineageService(store)
    result = service.trace("urn:test:item:1")
    assert result["entity"] is not None
    assert result["sources"]
    assert result["ingestion_runs"]


def test_lineage_missing_entity():
    store = MemoryGraphStore()
    service = LineageService(store)
    result = service.trace("urn:missing")
    assert result["entity"] is None
    assert not result["lineage"]
