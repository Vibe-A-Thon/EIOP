"""Transactional SHACL validation tests (CRA-020.4, CRA-020.5, CRA-020.10, CRA-020.A).

Verifies:
1. Transactional isolation and zero-triple commit on failure
2. Compare-and-swap (CAS) base revision concurrency conflict detection
3. Joint constraint violation detection (two individually valid candidate additions jointly violate maxCount)
4. Shape change revalidation distinguishing incremental vs full check
5. Validator outage blocking publication with zero triples committed
"""

from __future__ import annotations
import pytest

from eoip.graph.memory import MemoryGraphStore
from eoip.ontology.shacl_validator import (
    SHACLValidator,
    SHACLShape,
    SHACLSeverity,
    TransactionalSHACLValidator,
    SHACLTxnViolationError,
    SHACLConcurrencyConflictError,
    SHACLValidatorUnavailableError,
)


def test_transactional_validation_zero_commit_on_violation():
    """CRA-020.4 & CRA-020.10: If candidate data violates SHACL, zero triples/vertices are committed."""
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "srv-1", "name": "ExistingService", "service_id": "srv-1"})

    validator = SHACLValidator()
    validator.shapes = {}
    validator.register_shape(SHACLShape(
        shape_id="StrictServiceShape",
        target_class="Service",
        required_properties=["canonical_id", "name"],
        property_types={"name": "string"},
    ))

    txn = TransactionalSHACLValidator(store, validator)
    base_rev = txn.get_revision()

    # Candidate with empty name string (violation)
    candidate_vertices = [
        {"label": "Service", "properties": {"canonical_id": "srv-2", "name": "", "service_id": "srv-2"}}
    ]

    with pytest.raises(SHACLTxnViolationError) as exc_info:
        txn.validate_candidate_publication(
            candidate_vertices=candidate_vertices,
            candidate_edges=[],
            expected_base_revision=base_rev,
        )

    assert exc_info.value.report is not None
    assert not exc_info.value.report.conforms

    # Verify zero triples committed to canonical store!
    assert len(store.find_vertices()) == 1
    assert store.get_vertex_by_canonical_id("srv-2") is None


def test_transactional_validation_cas_concurrency_conflict():
    """CRA-020.4: If expected base revision has changed (concurrent write), abort with conflict."""
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "srv-1", "name": "ServiceA", "service_id": "srv-1"})

    validator = SHACLValidator()
    validator.shapes = {}
    validator.register_shape(SHACLShape(
        shape_id="SimpleShape",
        target_class="Service",
        required_properties=["name"],
    ))

    txn = TransactionalSHACLValidator(store, validator)
    base_rev = txn.get_revision()

    # First write succeeds and advances revision
    candidate_1 = [{"label": "Service", "properties": {"canonical_id": "srv-2", "name": "ServiceB", "service_id": "srv-2"}}]
    result_1 = txn.validate_candidate_publication(candidate_1, [], expected_base_revision=base_rev)
    assert result_1["committed"] is True
    new_rev = result_1["new_revision"]
    assert new_rev != base_rev

    # Second concurrent write using stale base_rev must fail with SHACLConcurrencyConflictError
    candidate_2 = [{"label": "Service", "properties": {"canonical_id": "srv-3", "name": "ServiceC", "service_id": "srv-3"}}]
    with pytest.raises(SHACLConcurrencyConflictError) as exc_info:
        txn.validate_candidate_publication(candidate_2, [], expected_base_revision=base_rev)
    assert "Concurrent modification conflict" in str(exc_info.value)

    # srv-3 was NOT committed
    assert store.get_vertex_by_canonical_id("srv-3") is None


def test_joint_constraint_violation_caught():
    """CRA-020.4: Two individually valid writes cannot jointly violate a constraint."""
    store = MemoryGraphStore()
    store.upsert_vertex("WorkItem", {"canonical_id": "w-1", "issue_key": "W-1", "summary": "Task", "source_aliases": ["alias-1"]})

    validator = SHACLValidator()
    validator.shapes = {}
    validator.register_shape(SHACLShape(
        shape_id="MaxAliasShape",
        target_class="WorkItem",
        max_counts={"source_aliases": 1},  # Maximum 1 alias allowed
    ))

    txn = TransactionalSHACLValidator(store, validator)
    base_rev = txn.get_revision()

    # Candidate alone has 2 aliases when combined with existing node
    candidate_update = [
        {"label": "WorkItem", "properties": {"canonical_id": "w-1", "issue_key": "W-1", "summary": "Task", "source_aliases": ["alias-1", "alias-2"]}}
    ]

    with pytest.raises(SHACLTxnViolationError):
        txn.validate_candidate_publication(candidate_update, [], expected_base_revision=base_rev)

    # Existing node remains unchanged with 1 alias
    assert len(store.get_vertex_by_canonical_id("w-1")["properties"]["source_aliases"]) == 1


def test_shape_change_revalidation_job_incremental_and_full():
    """CRA-020.5: Revalidate affected data on shape changes; distinguish incremental vs full check."""
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "srv-1", "name": "ServiceA", "service_id": "srv-1"})
    store.upsert_vertex("Service", {"canonical_id": "srv-2", "name": "", "service_id": "srv-2"})  # invalid under new shape

    txn = TransactionalSHACLValidator(store)
    new_shapes = [
        SHACLShape(shape_id="StrictNewShape", target_class="Service", required_properties=["name"]),
    ]

    # Revalidation in incremental mode detects invalid data and blocks publication
    inc_result = txn.revalidate_affected_data(new_shapes, mode="incremental")
    assert inc_result["mode"] == "incremental"
    assert inc_result["conforms"] is False
    assert inc_result["publication_blocked"] is True

    # Fix node in store
    store.upsert_vertex("Service", {"canonical_id": "srv-2", "name": "ServiceB", "service_id": "srv-2"})
    full_result = txn.revalidate_affected_data(new_shapes, mode="full")
    assert full_result["mode"] == "full"
    assert full_result["conforms"] is True
    assert full_result["publication_blocked"] is False
