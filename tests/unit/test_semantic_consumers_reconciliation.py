from __future__ import annotations

import hashlib
import json

import pytest
from eoip.connectors.reconciliation import SourceReconciler
from eoip.contracts.source_event import SourceEventV2
from eoip.graph.consumers import run_default_consumers
from eoip.graph.evolution import ChangeJournal
from eoip.graph.memory import MemoryGraphStore


def _event(record_id: str, content: str) -> SourceEventV2:
    digest = hashlib.sha256(content.encode()).hexdigest()
    return SourceEventV2(
        event_id=hashlib.sha256(f"{record_id}:{digest}".encode()).hexdigest(),
        source_system="test",
        source_instance_id="test-prod",
        source_record_id=record_id,
        event_time="2026-10-03T00:00:00Z",
        content_hash=digest,
        payload={"id": record_id, "content": content},
    )


@pytest.mark.req(
    "G2-T0241", "G2-T0242", "G2-T0243",
    "G2-EVENT-002", "G2-EVENT-003", "G2-EVENT-004", "G2-EVENT-005", "G2-EVENT-007", "G2-SYNC-008"
)
def test_default_semantic_consumers_process_each_cursor_once(tmp_path) -> None:
    store = MemoryGraphStore()
    store.upsert_vertex(
        "WorkItem", {"canonical_id": "item-1", "issue_key": "EOIP-1", "summary": "Consumer"}
    )
    journal = ChangeJournal(tmp_path / "journal" / "semantic-changes.ndjson")
    journal.append(
        {
            "graph_version": "v1",
            "change_kind": "CREATE",
            "target_kind": "ENTITY",
            "target_id": "item-1",
            "source_event_id": "event-1",
            "observed_at": "2026-10-03T00:00:00Z",
            "details": {},
        }
    )

    first = run_default_consumers(store, tmp_path)
    second = run_default_consumers(store, tmp_path)

    assert set(first) == {
        "quality-recalculation",
        "semantic-cache-invalidation",
        "admin-timeline",
    }
    assert all(state["cursor"] == 1 and state["processed"] == 1 for state in first.values())
    assert all(state["processed"] == 1 for state in second.values())
    assert json.loads((tmp_path / "state" / "semantic-cache.json").read_text())["targets"] == [
        "item-1"
    ]
    timeline = json.loads((tmp_path / "state" / "admin-timeline.json").read_text())
    assert len(timeline["events"]) == 1
    assert (tmp_path / "state" / "validation.json").exists()


@pytest.mark.req("G2-EVENT-006")
def test_consumer_failure_does_not_corrupt_graph_state(tmp_path) -> None:
    from eoip.graph.consumers import SemanticConsumerRunner

    store = MemoryGraphStore()
    store.upsert_vertex(
        "WorkItem", {"canonical_id": "item-auth", "issue_key": "AUTH-1", "summary": "Authoritative"}
    )
    journal = ChangeJournal(tmp_path / "journal" / "semantic-changes.ndjson")
    journal.append(
        {
            "graph_version": "v1",
            "change_kind": "CREATE",
            "target_kind": "ENTITY",
            "target_id": "item-auth",
            "source_event_id": "event-1",
            "observed_at": "2026-10-03T00:00:00Z",
            "details": {},
        }
    )

    class FailingConsumer:
        name = "failing-consumer"

        def consume(self, events):
            raise RuntimeError("Consumer crash simulation")

    runner = SemanticConsumerRunner(journal, tmp_path / "state" / "event-consumers")
    runner.register(FailingConsumer())
    results = runner.run_once()

    assert results["failing-consumer"]["status"] == "FAILED"
    assert "Consumer crash simulation" in results["failing-consumer"]["error"]
    # Authoritative graph state remains completely uncorrupted
    assert store.get_vertex_by_canonical_id("item-auth")["properties"]["summary"] == "Authoritative"


@pytest.mark.req("G2-T0250", "G2-T0251", "G2-T0252", "G2-T0253", "G2-SYNC-003", "G2-SYNC-005")
def test_reconciler_detects_and_repairs_missing_stale_and_orphaned_records() -> None:
    unchanged = _event("unchanged", "same")
    stale = _event("stale", "new")
    missing = _event("missing", "new")
    current = [
        {
            "canonical_id": "urn:test:unchanged",
            "properties": {"content_hash": unchanged.content_hash},
        },
        {
            "canonical_id": "urn:test:stale",
            "properties": {"content_hash": hashlib.sha256(b"old").hexdigest()},
        },
        {"canonical_id": "urn:test:orphan", "properties": {"content_hash": "orphan"}},
    ]
    repaired_batches = []

    def repair(events):
        repaired_batches.append([event.source_record_id for event in events])
        return [f"urn:test:{event.source_record_id}" for event in events]

    report = SourceReconciler().reconcile(
        source_id="test-prod",
        events=[unchanged, stale, missing],
        current_vertices=current,
        canonical_id=lambda event: f"urn:test:{event.source_record_id}",
        repair=repair,
        checkpoint="cursor-3",
    )

    assert report.status == "REPAIRED"
    assert report.unchanged == ["urn:test:unchanged"]
    assert report.stale == ["urn:test:stale"]
    assert report.missing == ["urn:test:missing"]
    assert report.orphaned == ["urn:test:orphan"]
    assert report.repaired == ["urn:test:missing", "urn:test:stale"]
    assert repaired_batches == [["missing", "stale"]]
