"""Tests for Processing Runtime Typed Contracts and Schemas (PUR-CON-001..010).

Validates Pydantic extra='forbid' constraint, RFC-8785 canonical JSON hashing,
and schema invariants across all ten logical units.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from eoip.processing.contracts import (
    ArtifactRef,
    DeviceDescriptor,
    ExecutionContext,
    ExecutionPlan,
    ExecutionPreference,
    ExecutionReceipt,
    JobRecord,
    JobStatus,
    LogicalUnit,
    ModelManifest,
    OperatorBudget,
    OperatorSpec,
    PlanNode,
    ProcessingRequest,
    canonical_digest,
)


@pytest.mark.req("PUR-CON-001")
def test_all_ten_logical_units_defined():
    """PUR-CON-001, PUR-FND-001: Ensure exactly ten logical processing units are enumerated."""
    expected_units = {"CPU", "GPU", "TPU", "NPU", "DPU", "QPU", "APU", "LPU", "IPU", "VPU"}
    actual_units = {u.value for u in LogicalUnit}
    assert actual_units == expected_units


@pytest.mark.req("PUR-CON-004")
def test_canonical_json_hashing_invariance():
    """PUR-CON-004: Key-order permutation must produce identical canonical SHA-256 digest."""
    obj1 = {"b": 2, "a": 1, "nested": {"z": "final", "y": "middle"}}
    obj2 = {"a": 1, "nested": {"y": "middle", "z": "final"}, "b": 2}
    digest1 = canonical_digest(obj1)
    digest2 = canonical_digest(obj2)
    assert digest1 == digest2
    assert len(digest1) == 64

    # Altering nested data changes digest
    obj3 = {"a": 1, "nested": {"y": "middle", "z": "changed"}, "b": 2}
    assert canonical_digest(obj3) != digest1


@pytest.mark.req("PUR-CON-001")
def test_pydantic_extra_forbidden():
    """PUR-CON-001: Pydantic models must reject unexpected/injected fields (extra='forbid')."""
    valid_data = {
        "tenant_id": "tenant-corp",
        "principal_id": "user-123",
        "workspace_id": "ws-1",
        "roles": ["analyst"],
    }
    ctx = ExecutionContext(**valid_data)
    assert ctx.tenant_id == "tenant-corp"

    # Injected rogue parameter should raise ValidationError
    with pytest.raises(ValidationError):
        ExecutionContext(**{**valid_data, "unauthorized_injection": True})


@pytest.mark.req("PUR-CON-002")
def test_processing_request_validation():
    """PUR-CON-002: ProcessingRequest strictly validates logical unit and operator parameters."""
    req = ProcessingRequest(
        logical_unit=LogicalUnit.GPU,
        operator_id="vector.cosine_top_k",
        inputs={"candidates": [[1.0, 0.0], [0.0, 1.0]], "query": [1.0, 0.0]},
        parameters={"k": 5, "zero_vector_policy": "reject"},
        execution_preference=ExecutionPreference.CPU_ONLY,
    )
    assert req.logical_unit == LogicalUnit.GPU
    assert req.operator_id == "vector.cosine_top_k"
    digest = req.canonical_digest()
    assert len(digest) == 64

    # Invalid logical unit should fail
    with pytest.raises(ValidationError):
        ProcessingRequest(
            logical_unit="SUPERCOMPUTER",  # Invalid
            operator_id="vector.cosine_top_k",
        )


@pytest.mark.req("PUR-CON-003")
def test_artifact_ref_validation():
    """PUR-CON-003: ArtifactRef validates SHA-256 pattern, byte length, and tenant scope."""
    valid_sha = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    ref = ArtifactRef(
        artifact_id="art:dataset:102",
        tenant_id="tenant-alpha",
        byte_length=1024,
        sha256=valid_sha,
        classification="confidential",
    )
    assert ref.byte_length == 1024
    assert ref.sha256 == valid_sha

    # Malformed SHA-256 should fail
    with pytest.raises(ValidationError):
        ArtifactRef(
            artifact_id="art:bad",
            tenant_id="tenant-alpha",
            byte_length=10,
            sha256="not-a-valid-sha256",
        )


@pytest.mark.req("PUR-CON-005")
def test_execution_preference_matrix():
    """PUR-CON-005: Verify all four execution preference modes are strictly defined."""
    assert ExecutionPreference.CPU_ONLY.value == "cpu_only"
    assert ExecutionPreference.PREFER_ACCELERATOR.value == "prefer_accelerator"
    assert ExecutionPreference.REQUIRE_GPU.value == "require_gpu"
    assert ExecutionPreference.REQUIRE_NPU.value == "require_npu"


@pytest.mark.req("PUR-CON-008")
def test_execution_receipt_digest_integrity():
    """PUR-CON-008: ExecutionReceipt includes cryptographic digest and simulation labeling."""
    receipt = ExecutionReceipt(
        receipt_id="rcpt-001",
        job_id="job-001",
        tenant_id="tenant-01",
        logical_unit=LogicalUnit.QPU,
        operator_id="quantum.simulate",
        operator_version="1.0",
        actual_provider="qiskit_aer",
        device_id="dev:cpu:0",
        is_simulation=True,
        is_physical_qpu=False,
        compute_duration_ms=12.5,
        total_duration_ms=15.0,
        peak_memory_mib=64.0,
        outcome="SUCCEEDED",
    )
    digest = receipt.compute_digest()
    assert len(digest) == 64
    assert receipt.is_simulation is True
    assert receipt.is_physical_qpu is False


@pytest.mark.req("PUR-CON-010")
def test_job_record_lifecycle_states():
    """PUR-CON-010: JobRecord tracks public states including HELD_FOR_REVIEW and REJECTED."""
    assert JobStatus.QUEUED.value == "QUEUED"
    assert JobStatus.RUNNING.value == "RUNNING"
    assert JobStatus.SUCCEEDED.value == "SUCCEEDED"
    assert JobStatus.FAILED.value == "FAILED"
    assert JobStatus.CANCELLED.value == "CANCELLED"
    assert JobStatus.HELD_FOR_REVIEW.value == "HELD_FOR_REVIEW"
    assert JobStatus.REJECTED.value == "REJECTED"

    record = JobRecord(
        job_id="job-101",
        tenant_id="t-1",
        principal_id="p-1",
        logical_unit=LogicalUnit.CPU,
        operator_id="records.transform",
        status=JobStatus.QUEUED,
        created_at="2026-10-19T12:00:00Z",
    )
    assert record.status == JobStatus.QUEUED
    assert record.cancel_requested is False
