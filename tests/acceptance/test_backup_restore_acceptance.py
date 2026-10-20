"""Acceptance test suite for Backup, Restore, and Disaster Recovery (WP-033, CRA-033.1-033.7, CRA-033.A)."""

from __future__ import annotations

import copy
import time
import pytest

from eoip.graph.memory import MemoryGraphStore
from eoip.recovery.enterprise_recovery import (
    AuthoritativeStateInventory,
    CleanRoomRestoreEngine,
    DisasterRecoveryEvaluator,
    EnterpriseBackupEngine,
    FencedWriterGuard,
    PointInTimeRecoveryEngine,
    RPORTOReport,
)
from eoip.recovery.wal import WALEntry, WALOperationType


@pytest.fixture
def populated_store():
    store = MemoryGraphStore()
    v1 = store.upsert_vertex("Project", {"canonical_id": "proj:1", "name": "Enterprise Core"})
    v2 = store.upsert_vertex("WorkItem", {"canonical_id": "item:101", "issue_key": "CORE-101", "summary": "Implement backup engine"})
    v3 = store.upsert_vertex("WorkItem", {"canonical_id": "item:102", "issue_key": "CORE-102", "summary": "Implement clean restore"})
    store.upsert_edge("CONTAINS", v1["vid"], v2["vid"], {})
    store.upsert_edge("PARENT_OF", v2["vid"], v3["vid"], {})
    return store


# ===========================================================================
# CRA-033.1: Authoritative state inventory
# ===========================================================================

@pytest.mark.req("CRA-033")
def test_cra_033_1_authoritative_state_inventory(populated_store):
    inv = AuthoritativeStateInventory.capture(
        populated_store,
        control_jobs=["job-extract-01", "job-transform-02"],
        ontology_pkgs=["pkg-eoip-core-1.0.0", "pkg-financial-2.1.0"],
        raw_refs=["sha256:112233445566778899aabbccddeeff00"],
        principals=["user:auditor_sindhu", "role:compliance_officer"],
        watermarks={"snowflake": "2026-10-18T10:00:00Z"},
        kms_refs=["arn:aws:kms:us-east-1:123456789012:key/dr-key-01"],
    )

    # All 8 authoritative components captured
    assert inv.vertex_count == 3
    assert inv.edge_count == 2
    assert len(inv.canonical_graph_checksum) == 64
    assert "job-extract-01" in inv.control_db_jobs
    assert "pkg-eoip-core-1.0.0" in inv.ontology_packages
    assert len(inv.raw_reference_hashes) == 1
    assert "user:auditor_sindhu" in inv.identity_principals
    assert inv.outbox_watermarks["snowflake"] == "2026-10-18T10:00:00Z"
    assert "arn:aws:kms" in inv.kms_key_references[0]

    # Secret references only, never plaintext credentials
    inv_str = str(inv.to_dict())
    assert "password" not in inv_str.lower()
    assert "secret" not in inv_str.lower() or "secret_key" not in inv_str.lower()


# ===========================================================================
# CRA-033.2: Consistent encrypted backups & immutability
# ===========================================================================

@pytest.mark.req("CRA-033")
def test_cra_033_2_consistent_encrypted_backups_and_immutability(populated_store):
    engine = EnterpriseBackupEngine(kms_key="test-key-2026")
    snap = engine.create_snapshot(populated_store, encrypt=True, immutable=True, retention_days=45)

    assert snap.is_encrypted is True
    assert snap.is_immutable is True
    assert snap.retention_days == 45
    assert len(snap.checksum) == 64
    assert len(snap.payload_bytes) > 0
    assert snap.inventory.vertex_count == 3
    assert snap.inventory.edge_count == 2


# ===========================================================================
# CRA-033.3: Clean environment restore & projection rebuild
# ===========================================================================

@pytest.mark.req("CRA-033")
def test_cra_033_3_clean_environment_restore_and_projection_rebuild(populated_store):
    backup_engine = EnterpriseBackupEngine(kms_key="test-key-2026")
    snap = backup_engine.create_snapshot(populated_store, encrypt=True)

    restore_engine = CleanRoomRestoreEngine(kms_key="test-key-2026")

    # 1. Non-clean environment must be rejected
    dirty_store = MemoryGraphStore()
    dirty_store.upsert_vertex("Project", {"canonical_id": "dirty:1", "name": "residual"})
    dirty_res = restore_engine.restore_to_clean_store(snap, dirty_store)
    assert dirty_res.success is False
    assert "not clean" in dirty_res.error

    # 2. Pristine clean environment succeeds
    clean_store = MemoryGraphStore()
    res = restore_engine.restore_to_clean_store(snap, clean_store)
    assert res.success is True
    assert res.restored_vertices == 3
    assert res.restored_edges == 2
    assert res.revision_consistent is True
    assert res.checksum_verified is True
    assert res.acl_verified is True
    assert res.projections_rebuilt is True


# ===========================================================================
# CRA-033.4: Measured P1 RPO & RTO bounds
# ===========================================================================

@pytest.mark.req("CRA-033")
def test_cra_033_4_measured_rpo_and_rto_bounds():
    now = time.time()
    # 15 seconds transaction lag before simulated crash
    last_tx = now - 15.0
    failure = now
    # Recovery takes 2.5 seconds
    rec_start = now + 1.0
    rec_complete = rec_start + 2.5

    report = DisasterRecoveryEvaluator.evaluate(
        last_durable_tx_time=last_tx,
        failure_time=failure,
        recovery_start_time=rec_start,
        recovery_complete_time=rec_complete,
    )

    # P1 binding: RPO <= 15 min (900s), RTO <= 4 h (14400s)
    assert report.rpo_conforms is True
    assert report.rto_conforms is True
    assert report.measured_rpo_seconds <= 900.0
    assert report.measured_rto_seconds <= 14400.0
    assert report.exact_data_loss_records == 0


# ===========================================================================
# CRA-033.5: Failure rehearsals: corrupt snapshot, lost key, writer fencing, tombstones
# ===========================================================================

@pytest.mark.req("CRA-033")
def test_cra_033_5_failure_rehearsals_corrupt_key_fencing_tombstones(populated_store):
    backup_engine = EnterpriseBackupEngine(kms_key="correct-key")
    snap = backup_engine.create_snapshot(populated_store, encrypt=True)

    # 1. Corrupt snapshot fails checksum verification
    corrupt_snap = copy.deepcopy(snap)
    corrupt_snap.payload_bytes = corrupt_snap.payload_bytes[:-4] + b"XXXX"
    restore_engine = CleanRoomRestoreEngine(kms_key="correct-key")
    res_corrupt = restore_engine.restore_to_clean_store(corrupt_snap, MemoryGraphStore())
    assert res_corrupt.success is False
    assert "Corrupt snapshot" in res_corrupt.error

    # 2. Lost or invalid key fails decryption
    wrong_key_restore = CleanRoomRestoreEngine(kms_key="wrong-unauthorized-key")
    res_wrong_key = restore_engine.restore_to_clean_store(snap, MemoryGraphStore())
    assert res_wrong_key.success is True  # with correct key
    res_bad = wrong_key_restore.restore_to_clean_store(snap, MemoryGraphStore())
    assert res_bad.success is False
    assert "Decryption / decode failure" in res_bad.error

    # 3. Fencing token fences obsolete writers
    guard = FencedWriterGuard(current_token=100)
    assert guard.write("rec-1", {"val": 1}, fencing_token=100) is True

    # Advance generation token
    guard.bump_token()  # now 101

    # Old writer with token 100 is rejected
    with pytest.raises(PermissionError, match="Fenced writer rejected"):
        guard.write("rec-2", {"val": 2}, fencing_token=100)

    # 4. Deletion tombstone prevents replay resurrection
    guard.delete("rec-1", fencing_token=101)
    with pytest.raises(ValueError, match="deletion tombstone"):
        guard.write("rec-1", {"val": 99}, fencing_token=101)


# ===========================================================================
# CRA-033.6: Point-in-time recovery (PITR) with WAL journal replay
# ===========================================================================

@pytest.mark.req("CRA-033")
def test_cra_033_6_point_in_time_recovery_with_wal_replay(populated_store):
    now = time.time()
    backup_engine = EnterpriseBackupEngine(kms_key="pitr-key")
    base_snap = backup_engine.create_snapshot(populated_store, encrypt=True)
    base_snap.created_at = now - 100.0

    # WAL transactions after snapshot
    wal = [
        WALEntry(lsn=1, operation=WALOperationType.INSERT, entity_type="WorkItem", entity_id="item:103", payload={"canonical_id": "item:103", "issue_key": "CORE-103", "summary": "Item 3"}, timestamp=now - 50.0),
        WALEntry(lsn=2, operation=WALOperationType.INSERT, entity_type="WorkItem", entity_id="item:104", payload={"canonical_id": "item:104", "issue_key": "CORE-104", "summary": "Item 4"}, timestamp=now - 20.0),
        WALEntry(lsn=3, operation=WALOperationType.INSERT, entity_type="WorkItem", entity_id="item:105", payload={"canonical_id": "item:105", "issue_key": "CORE-105", "summary": "Item 5"}, timestamp=now - 5.0),
    ]

    pitr = PointInTimeRecoveryEngine(base_snapshot=base_snap, wal_entries=wal, max_pitr_window_days=30, kms_key="pitr-key")
    target_store = MemoryGraphStore()

    # Replay up to timestamp (now - 15.0): should include item:103 and item:104, but NOT item:105
    res = pitr.recover_to_timestamp(target_timestamp=now - 15.0, target_store=target_store)
    assert res["success"] is True
    assert res["replayed_transactions"] == 2
    assert target_store.count_vertices() == 5  # 3 base + 2 replayed


# ===========================================================================
# CRA-033.7: P1 RPO/RTO vs P2 500M-triple qualification target (Decision X-09)
# ===========================================================================

@pytest.mark.req("CRA-033")
def test_cra_033_7_p1_rpo_rto_vs_p2_500m_triple_qualification():
    report = DisasterRecoveryEvaluator.evaluate(
        last_durable_tx_time=100.0,
        failure_time=105.0,
        recovery_start_time=106.0,
        recovery_complete_time=108.0,
    )
    # P1 objectives
    assert report.target_rpo_seconds == 900.0  # 15 min
    assert report.target_rto_seconds == 14400.0  # 4 hours
    assert report.rpo_conforms is True
    assert report.rto_conforms is True
    # Explicit distinction from P2 500M target
    assert "Decision X-09" in report.p2_qualification_note
    assert "P1 objective RTO <= 4h is binding" in report.p2_qualification_note


# ===========================================================================
# CRA-033.A: Timed independent restore and adversarial authorization check
# ===========================================================================

@pytest.mark.req("CRA-033")
def test_cra_033_a_timed_independent_restore_and_adversarial_auth_check(populated_store):
    start_time = time.perf_counter()

    # 1. Independent snapshot with full inventory
    backup_engine = EnterpriseBackupEngine(kms_key="master-prod-key")
    snapshot = backup_engine.create_snapshot(
        populated_store,
        encrypt=True,
        immutable=True,
        retention_days=30,
    )

    # 2. Timed restore into clean target
    target_store = MemoryGraphStore()
    restore_engine = CleanRoomRestoreEngine(kms_key="master-prod-key")
    result = restore_engine.restore_to_clean_store(snapshot, target_store)
    assert result.success is True
    assert result.duration_ms < 5000.0  # well under RTO bounds

    # 3. Business queries execute correctly over restored state
    proj_vertices = [v for v in target_store.find_vertices() if v["label"] == "Project"]
    assert len(proj_vertices) == 1
    assert proj_vertices[0]["properties"]["name"] == "Enterprise Core"

    # 4. Source cursors and watermarks preserved
    assert "github" in snapshot.inventory.outbox_watermarks
    assert snapshot.inventory.rebuild_watermark == "wm-epoch-9942"

    # 5. Adversarial authorization check: tampered or revoked access cannot read store
    adversary_engine = CleanRoomRestoreEngine(kms_key="adversary-unauthorized-key")
    adversary_store = MemoryGraphStore()
    adversary_res = adversary_engine.restore_to_clean_store(snapshot, adversary_store)
    assert adversary_res.success is False
    assert adversary_store.count_vertices() == 0  # 0 records leaked
