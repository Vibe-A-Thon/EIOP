"""Integration tests for Data Privacy, 8-Plane Erasure Cascade, Anti-Resurrection, and Strict No-Egress (CRA-040.1 - CRA-040.7, CRA-040.A).

Covers:
1. Handling policy classification, license distinction (code/model/dataset/content), residency, retention, and legal holds (CRA-040.1).
2. Socket monitor recording zero external bytes at network boundary in no-egress mode (CRA-040.2, CRA-040.7).
3. 8-plane erasure cascade across raw, canonical, schema, provenance, lineage, policy, temporal, vector + caches, exports, backups (CRA-040.3, CRA-040.6).
4. Legal hold exceptions and explicit audit reporting (CRA-040.5).
5. Anti-resurrection registry preventing replay/restore from resurrecting purged subjects (CRA-040.4).
6. Post-GDPR deep sweep verifying zero remaining records except documented held material (CRA-040.A).
"""

from __future__ import annotations

import pytest

from eoip.privacy import (
    AntiResurrectionRegistry,
    ClassificationEngine,
    EgressViolationError,
    ErasureCascadeEngine,
    GraphPlane,
    HandlingPolicy,
    LawfulBasis,
    LicenseKind,
    NetworkSocketMonitor,
)


def test_handling_policy_and_license_differentiation():
    """CRA-040.1: Distinct licenses (code/model/dataset/content), residence, retention, lawful basis, legal hold."""
    policy_dataset = HandlingPolicy(
        subject_id="sub-101",
        lawful_basis=LawfulBasis.CONTRACTUAL,
        residence_region="EU",
        retention_days=365,
        license_kind=LicenseKind.DATASET,
        license_identifier="CDLA-Permissive-2.0",
        legal_hold=False,
    )
    policy_model = HandlingPolicy(
        subject_id="model-bge-m3",
        lawful_basis=LawfulBasis.LEGITIMATE_INTEREST,
        residence_region="GLOBAL",
        retention_days=730,
        license_kind=LicenseKind.MODEL,
        license_identifier="MIT",
        legal_hold=False,
    )
    policy_code = HandlingPolicy(
        subject_id="plugin-jira",
        lawful_basis=LawfulBasis.LEGAL_OBLIGATION,
        residence_region="EU",
        retention_days=1095,
        license_kind=LicenseKind.CODE,
        license_identifier="Apache-2.0",
        legal_hold=True,
        legal_hold_ref="LH-2026-ENG-42",
    )

    assert policy_dataset.license_kind != policy_model.license_kind
    assert policy_code.legal_hold is True
    assert policy_code.legal_hold_ref == "LH-2026-ENG-42"
    assert policy_dataset.residence_region == "EU"


def test_no_egress_network_boundary_measurement():
    """CRA-040.2, CRA-040.7: Socket monitor blocks external bytes and records 0 external bytes sent."""
    monitor = NetworkSocketMonitor(
        allowed_hosts={"127.0.0.1", "enterprise-vault.internal", "db-cluster.internal"},
        no_egress_mode=True,
    )

    # 1. Internal enterprise system connection allowed
    monitor.check_and_record_outbound("enterprise-vault.internal", 8200, 1024)
    monitor.check_and_record_outbound("127.0.0.1", 5432, 2048)
    assert monitor.internal_bytes_sent == 3072
    assert monitor.external_bytes_sent == 0

    # 2. External destination connection blocked at network boundary
    with pytest.raises(EgressViolationError) as exc:
        monitor.check_and_record_outbound("api.openai.com", 443, 512)
    assert "No-egress policy violation" in str(exc.value)

    with pytest.raises(EgressViolationError):
        monitor.check_and_record_outbound("8.8.8.8", 53, 64)

    # External bytes strictly remain ZERO
    assert monitor.external_bytes_sent == 0


def test_eight_plane_erasure_cascade_and_scoped_report():
    """CRA-040.3, CRA-040.6: Deletion request locates and processes every derivative across 8 graph planes."""
    engine = ErasureCascadeEngine()

    subject_id = "user-alice-99"
    tenant_id = "tenant-alpha"

    # Set handling policy without legal hold
    engine.set_handling_policy(
        HandlingPolicy(
            subject_id=subject_id,
            lawful_basis=LawfulBasis.CONSENT,
            residence_region="EU",
            retention_days=90,
            license_kind=LicenseKind.CONTENT,
            license_identifier="Proprietary",
            legal_hold=False,
        )
    )

    # Populate 8 graph planes with subject data and bystander data
    storage_planes = {
        GraphPlane.RAW.value: [
            {"id": "raw-1", "subject_id": subject_id, "payload": "user form submission"},
            {"id": "raw-2", "subject_id": "other-user", "payload": "other data"},
        ],
        GraphPlane.CANONICAL.value: [
            {"id": "can-1", "subject_id": subject_id, "entity_type": "Person"},
        ],
        GraphPlane.SCHEMA.value: [
            {"id": "sch-1", "subject_id": subject_id, "class": "Employee"},
        ],
        GraphPlane.PROVENANCE.value: [
            {"id": "prv-1", "subject_id": subject_id, "activity": "ingest_v1"},
        ],
        GraphPlane.LINEAGE.value: [
            {"id": "lin-1", "subject_id": subject_id, "pipeline": "crm_sync"},
        ],
        GraphPlane.POLICY.value: [
            {"id": "pol-1", "subject_id": subject_id, "acl": "read_only"},
        ],
        GraphPlane.TEMPORAL.value: [
            {"id": "tmp-1", "subject_id": subject_id, "valid_from": "2026-01-01"},
        ],
        GraphPlane.VECTOR.value: [
            {"id": "vec-1", "subject_id": subject_id, "embedding": [0.1, 0.2]},
        ],
    }

    caches = {
        "query:user-alice-99:profile": {"name": "Alice"},
        "query:other-user:profile": {"name": "Bob"},
    }
    exports = [
        {"export_id": "exp-1", "subject_id": subject_id},
        {"export_id": "exp-2", "subject_id": "other-user"},
    ]
    backups = [
        {"backup_id": "bak-1", "subject_id": subject_id, "tombstoned": False},
        {"backup_id": "bak-2", "subject_id": "other-user", "tombstoned": False},
    ]

    report = engine.execute_erasure_cascade(
        subject_id=subject_id,
        tenant_id=tenant_id,
        storage_planes=storage_planes,
        caches=caches,
        exports=exports,
        backups=backups,
    )

    assert report.subject_id == subject_id
    assert report.total_erased == 8  # 1 from each of the 8 planes
    assert report.caches_cleared == 1
    assert "query:user-alice-99:profile" not in caches
    assert "query:other-user:profile" in caches
    assert report.exports_purged == 1
    assert report.backups_marked == 1
    assert backups[0]["tombstoned"] is True

    # Check that each plane no longer contains subject_id
    for plane_name, items in storage_planes.items():
        assert not any(it.get("subject_id") == subject_id for it in items)
    # Bystander records remain intact
    assert len(storage_planes[GraphPlane.RAW.value]) == 1
    assert storage_planes[GraphPlane.RAW.value][0]["subject_id"] == "other-user"


def test_legal_hold_conflict_and_retention_escalation():
    """CRA-040.5: Subject under active Legal Hold retains held records with explicit audit exception report."""
    engine = ErasureCascadeEngine()
    subject_id = "exec-charlie-88"
    tenant_id = "tenant-corp"

    # Set policy with ACTIVE LEGAL HOLD
    engine.set_handling_policy(
        HandlingPolicy(
            subject_id=subject_id,
            lawful_basis=LawfulBasis.LEGAL_OBLIGATION,
            residence_region="US",
            retention_days=2555,
            license_kind=LicenseKind.CONTENT,
            license_identifier="Proprietary",
            legal_hold=True,
            legal_hold_ref="LH-SEC-LITIGATION-2026-09",
        )
    )

    storage_planes = {
        GraphPlane.RAW.value: [{"id": "r1", "subject_id": subject_id}],
        GraphPlane.CANONICAL.value: [{"id": "c1", "subject_id": subject_id}],
    }

    report = engine.execute_erasure_cascade(
        subject_id=subject_id,
        tenant_id=tenant_id,
        storage_planes=storage_planes,
    )

    # Total erased is 0 because records are legally held
    assert report.total_erased == 0
    assert len(report.legal_hold_exceptions) > 0
    assert "LH-SEC-LITIGATION-2026-09" in report.legal_hold_exceptions[0]

    # Records were preserved under hold
    assert len(storage_planes[GraphPlane.RAW.value]) == 1
    assert len(storage_planes[GraphPlane.CANONICAL.value]) == 1


def test_anti_resurrection_tombstone_blocks_replay():
    """CRA-040.4: Prevent replay, restore, or resync from resurrecting deleted content."""
    registry = AntiResurrectionRegistry()
    subject_id = "user-deleted-42"
    tenant_id = "tenant-gamma"

    # Register tombstone on purge
    registry.register_tombstone(subject_id, tenant_id, reason="GDPR_ARTICLE_17")
    assert registry.is_tombstoned(subject_id) is True

    # Replay event containing deleted subject must be rejected at ingestion admission
    replayed_payload = {"id": subject_id, "name": "Resurrected Alice", "email": "alice@corp.internal"}
    with pytest.raises(PermissionError) as exc:
        registry.verify_admission(replayed_payload, subject_id_key="id")
    assert "Resurrection blocked" in str(exc.value)

    # Bystander payload is admitted cleanly
    allowed_payload = {"id": "user-active-99", "name": "Active Bob"}
    registry.verify_admission(allowed_payload, subject_id_key="id")  # Does not raise


def test_gdpr_purge_deep_sweep_acceptance():
    """CRA-040.A: After GDPR purge, deep sweep across graph, vector, cache, and object store finds 0 remaining records."""
    tombstones = AntiResurrectionRegistry()
    engine = ErasureCascadeEngine(tombstone_registry=tombstones)

    subject_id = "gdpr-target-user"
    tenant_id = "t-eu"

    engine.set_handling_policy(
        HandlingPolicy(
            subject_id=subject_id,
            lawful_basis=LawfulBasis.CONSENT,
            residence_region="EU",
            retention_days=30,
            license_kind=LicenseKind.CONTENT,
            license_identifier="Proprietary",
            legal_hold=False,
        )
    )

    planes = {p.value: [{"id": f"{p.value}-1", "subject_id": subject_id}] for p in GraphPlane}
    caches = {"cache-key-1": subject_id}
    exports = [{"subject_id": subject_id}]
    backups = [{"subject_id": subject_id, "tombstoned": False}]

    report = engine.execute_erasure_cascade(
        subject_id=subject_id,
        tenant_id=tenant_id,
        storage_planes=planes,
        caches=caches,
        exports=exports,
        backups=backups,
    )

    assert report.total_erased == 8

    # Deep sweep: inspect all surfaces for any trace of subject_id
    remaining_graph_records = [
        it for plane_items in planes.values() for it in plane_items if it.get("subject_id") == subject_id
    ]
    remaining_cache_records = [v for v in caches.values() if subject_id in str(v)]
    remaining_exports = [e for e in exports if e.get("subject_id") == subject_id]

    assert len(remaining_graph_records) == 0
    assert len(remaining_cache_records) == 0
    assert len(remaining_exports) == 0

    # Backups marked tombstoned/shredded
    assert backups[0]["tombstoned"] is True
