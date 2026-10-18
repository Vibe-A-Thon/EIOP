"""Acceptance Suite for WP-010: Durable Source Events and Incremental Synchronization.

Implements and validates:
- CRA-010.1: SourceEventV2 contract versioning across UPSERT, DELETE, PERMISSION_UPDATE
- CRA-010.2: Stable event ordering and deduplication preserving ACL and delete events
- CRA-010.3 & CRA-010.8: Durable checkpoints, idempotent publication, and crash recovery
- CRA-010.4: Reconciliation states and prevention of accidental deletion on partial absence
- CRA-010.5: Replay preserving deletion without data resurrection
- CRA-010.6: Cryptographic SHA-256 hash chaining and tamper detection
- CRA-010.7: Explicit independent bitemporal stamping (observed_at vs source_timestamp)
- CRA-010.A: Full crash-injection acceptance gate killing worker at ~50% baseline sync
"""
from __future__ import annotations

import time
from pathlib import Path
import pytest

from eoip.contracts.source_event import PermissionMetadata, SourceEventV2, utc_now_iso
from eoip.journal.event_journal import (
    CheckpointRecord,
    EventJournal,
    JournalEntry,
    ReconciliationState,
    ResumableCheckpointEngine,
)


def make_test_event(
    record_id: str,
    event_id: str,
    operation: str = "UPSERT",
    payload: dict | None = None,
    source_timestamp: str = "2026-10-18T10:00:00Z",
    permissions: PermissionMetadata | None = None,
) -> SourceEventV2:
    return SourceEventV2(
        event_id=event_id,
        source_id="src-prod-jira",
        source_system="jira",
        source_instance_id="inst-jira-01",
        source_record_id=record_id,
        source_record_type="WorkItem",
        operation=operation,
        event_time=source_timestamp,
        content_hash=f"hash-{event_id}",
        payload=payload or ({"summary": f"Task {record_id}"} if operation != "DELETE" else None),
        permissions=permissions or PermissionMetadata(visibility="INTERNAL"),
    )


def test_cra_010_1_source_event_contract_versioning():
    """CRA-010.1: SourceEventV2 contract versioning for UPSERT, DELETE, PERMISSION_UPDATE."""
    # 1. UPSERT event
    evt_upsert = make_test_event("item-1", "evt-1", operation="UPSERT")
    assert evt_upsert.schema_version == "2.0"
    assert evt_upsert.operation == "UPSERT"
    assert evt_upsert.content_hash == "hash-evt-1"

    # 2. DELETE event
    evt_delete = make_test_event("item-1", "evt-2", operation="DELETE")
    assert evt_delete.operation == "DELETE"
    assert evt_delete.payload is None

    # 3. PERMISSION_UPDATE event
    perms = PermissionMetadata(visibility="RESTRICTED", principal_refs=["user:admin"])
    evt_acl = make_test_event("item-1", "evt-3", operation="PERMISSION_UPDATE", permissions=perms)
    assert evt_acl.operation == "PERMISSION_UPDATE"
    assert evt_acl.permissions.visibility == "RESTRICTED"


def test_cra_010_2_event_order_and_deduplication_preserving_acl_and_deletes():
    """CRA-010.2: Preserve event order and deduplication without hiding ACL or delete events."""
    journal = EventJournal()
    engine = ResumableCheckpointEngine(journal)

    # Sequence of operations on same record: Create -> ACL change -> Delete
    evt1 = make_test_event("rec-1", "e-1", operation="UPSERT", payload={"title": "V1"})
    evt2 = make_test_event("rec-1", "e-2", operation="PERMISSION_UPDATE", permissions=PermissionMetadata(visibility="RESTRICTED"))
    evt3 = make_test_event("rec-1", "e-3", operation="DELETE")

    engine.process_and_publish("inst-jira-01", [evt1, evt2, evt3], next_cursor="c-3")

    state = engine.canonical_graph_state["rec-1"]
    assert state["deleted"] is True
    assert state["permissions"]["visibility"] == "RESTRICTED"


def test_cra_010_3_and_8_durable_checkpoints_idempotent_publication_and_crash_resumption():
    """CRA-010.3 & CRA-010.8: Durable checkpoints, idempotent effects, and crash recovery."""
    journal = EventJournal()
    engine = ResumableCheckpointEngine(journal)

    batch1 = [
        make_test_event(f"rec-{i}", f"evt-{i}", operation="UPSERT")
        for i in range(1, 6)
    ]
    # Process batch 1
    engine.process_and_publish("inst-jira-01", batch1, next_cursor="cur-5")
    ckpt = engine.get_checkpoint("inst-jira-01")
    assert ckpt.cursor == "cur-5"
    assert ckpt.watermark_sequence == 5

    # Replay same batch 1 (simulating crash retry) -> zero duplicate published assertions
    replayed = engine.resume_after_crash("inst-jira-01", batch1, next_cursor="cur-5")
    assert replayed == 0, "Duplicate events must be ignored idempotently"
    assert len(engine.canonical_graph_state) == 5


def test_cra_010_4_reconciliation_states_and_no_accidental_deletion_on_partial_absence():
    """CRA-010.4: Reconciliation states; partial baseline absence is NOT treated as deletion."""
    journal = EventJournal()
    engine = ResumableCheckpointEngine(journal)

    initial_batch = [make_test_event("rec-A", "e-A"), make_test_event("rec-B", "e-B")]
    engine.process_and_publish("inst-jira-01", initial_batch, next_cursor="c-1")

    # Partial page containing only rec-A in BACKFILLING/RECONCILING state
    partial_batch = [make_test_event("rec-A", "e-A2", payload={"title": "Updated A"})]
    engine.process_and_publish("inst-jira-01", partial_batch, next_cursor="c-2")

    # rec-B must NOT be marked as deleted due to partial absence
    assert engine.canonical_graph_state["rec-B"]["deleted"] is False
    assert engine.canonical_graph_state["rec-A"]["payload"]["title"] == "Updated A"


def test_cra_010_5_bound_revisions_and_replay_without_resurrecting_deleted_data():
    """CRA-010.5: Replay preserves deletion without data resurrection."""
    journal = EventJournal()
    engine = ResumableCheckpointEngine(journal)

    # Insert then delete rec-Z
    e_create = make_test_event("rec-Z", "e-z1", operation="UPSERT")
    e_delete = make_test_event("rec-Z", "e-z2", operation="DELETE")
    engine.process_and_publish("inst-jira-01", [e_create, e_delete], next_cursor="c-z")

    assert engine.canonical_graph_state["rec-Z"]["deleted"] is True

    # Replay entire stream into a fresh engine instance
    fresh_engine = ResumableCheckpointEngine(EventJournal())
    entries = journal.get_entries("inst-jira-01")
    events = [entry.event for entry in entries]
    fresh_engine.process_and_publish("inst-jira-01", events, next_cursor="c-z")

    # rec-Z must still be deleted in fresh engine
    assert fresh_engine.canonical_graph_state["rec-Z"]["deleted"] is True


def test_cra_010_6_cryptographic_hash_chain_tamper_detection():
    """CRA-010.6: Immutable append-only event journal with SHA-256 hash chaining and tamper detection."""
    journal = EventJournal()
    inst_id = "inst-audit-01"

    # Append 5 events
    for i in range(1, 6):
        evt = make_test_event(f"rec-{i}", f"evt-{i}")
        journal.append(inst_id, evt)

    # Valid chain passes verification
    assert journal.verify_chain(inst_id) is True

    # Tampering with entry 2 hash breaks the chain
    chain = journal._journals[inst_id]
    chain[1].entry_hash = "bad0000000000000000000000000000000000000000000000000000000000000"
    assert journal.verify_chain(inst_id) is False


def test_cra_010_7_bitemporal_stamping_independence():
    """CRA-010.7: Storing source_timestamp and observed_at independently without inference."""
    journal = EventJournal()
    inst_id = "inst-bitemporal-01"

    source_recorded_time = "2026-10-18T04:15:00Z"
    platform_observed_time = "2026-10-18T10:30:00Z"

    evt = make_test_event("item-1", "e-bt-1", source_timestamp=source_recorded_time)
    entry = journal.append(inst_id, evt, observed_at=platform_observed_time)

    assert entry.source_timestamp == source_recorded_time
    assert entry.observed_at == platform_observed_time
    assert entry.source_timestamp != entry.observed_at


def test_cra_010_a_acceptance_gate():
    """CRA-010.A: Acceptance gate killing worker at ~50% baseline sync, restarting, and verifying 0 loss and 0 duplicates."""
    journal = EventJournal()
    engine = ResumableCheckpointEngine(journal)
    inst_id = "inst-gate-sync-01"

    # Expected baseline dataset of 10 items
    baseline_events = [
        make_test_event(f"task-{i}", f"e-gate-{i}", operation="UPSERT", payload={"num": i})
        for i in range(1, 11)
    ]

    # 1. Kill ingestion worker at ~50% (after 5th item)
    with pytest.raises(RuntimeError, match="Simulated worker crash"):
        engine.process_and_publish(
            source_instance_id=inst_id,
            events=baseline_events,
            next_cursor="cur-gate-10",
            simulate_crash_after_index=5,
        )

    # Verify state at crash: 5 items processed in journal
    ckpt = engine.get_checkpoint(inst_id)
    assert ckpt is None or ckpt.watermark_sequence <= 5
    assert len(engine.canonical_graph_state) == 5

    # 2. Worker restart: resubmit full batch (replaying items 1..10)
    engine.resume_after_crash(inst_id, baseline_events, next_cursor="cur-gate-10")

    # 3. Verify canonical graph matches expected state: exactly 10 records, 0 duplicates, 0 gaps
    assert len(engine.canonical_graph_state) == 10
    for i in range(1, 11):
        rec_id = f"task-{i}"
        assert rec_id in engine.canonical_graph_state
        assert engine.canonical_graph_state[rec_id]["deleted"] is False
        assert engine.canonical_graph_state[rec_id]["payload"]["num"] == i

    # 4. Checkpoint is at watermark 10
    final_ckpt = engine.get_checkpoint(inst_id)
    assert final_ckpt.watermark_sequence == 10
    assert final_ckpt.published_count == 10
