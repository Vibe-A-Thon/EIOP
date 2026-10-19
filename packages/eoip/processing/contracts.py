"""Typed Pydantic contracts and schemas for EOIP Processing Runtime (PUR-CON-001..010).

All models enforce extra="forbid" and conform strictly to Section 5.1 of
processing-units-requirements.md.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from pydantic import BaseModel, ConfigDict, Field


class LogicalUnit(str, Enum):
    """The 10 normative logical processing units."""
    CPU = "CPU"  # General processing
    GPU = "GPU"  # Vector and parallel analytics
    TPU = "TPU"  # Tensor processing
    NPU = "NPU"  # Neural inference
    DPU = "DPU"  # Data preparation
    QPU = "QPU"  # Quantum simulation
    APU = "APU"  # Heterogeneous scheduling
    LPU = "LPU"  # Local language processing
    IPU = "IPU"  # Graph intelligence
    VPU = "VPU"  # Vision and document processing


class JobStatus(str, Enum):
    """Normative public job lifecycle states."""
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    CANCEL_REQUESTED = "CANCEL_REQUESTED"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    TIMED_OUT = "TIMED_OUT"
    REJECTED = "REJECTED"
    HELD_FOR_REVIEW = "HELD_FOR_REVIEW"


class ExecutionPreference(str, Enum):
    """Device execution preference."""
    CPU_ONLY = "cpu_only"
    PREFER_ACCELERATOR = "prefer_accelerator"
    REQUIRE_GPU = "require_gpu"
    REQUIRE_NPU = "require_npu"


def canonical_json_bytes(obj: Any) -> bytes:
    """Canonical RFC-8785 JSON serialization for deterministic hashing."""
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def canonical_digest(obj: Any) -> str:
    """Compute SHA-256 hex digest of canonical JSON bytes."""
    return hashlib.sha256(canonical_json_bytes(obj)).hexdigest()


class ExecutionContext(BaseModel):
    """Server-issued execution context; never accepted on trust from request JSON."""
    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(min_length=1, max_length=128)
    workspace_id: str = Field(default="default", max_length=128)
    principal_id: str = Field(min_length=1, max_length=128)
    roles: List[str] = Field(default_factory=list)
    effective_acls: List[str] = Field(default_factory=list)
    policy_epoch: int = Field(default=1, ge=1)
    correlation_id: str = Field(default="", max_length=128)
    causation_id: Optional[str] = Field(default=None, max_length=128)
    issued_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: Optional[str] = None
    permitted_operators: List[str] = Field(default_factory=list)
    output_scopes: List[str] = Field(default_factory=list)


class ArtifactRef(BaseModel):
    """Opaque tenant-scoped immutable artifact reference."""
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(min_length=1, max_length=256)
    tenant_id: str = Field(min_length=1, max_length=128)
    version: str = Field(default="v1", max_length=64)
    media_type: str = Field(default="application/octet-stream", max_length=128)
    byte_length: int = Field(ge=0)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    classification: str = Field(default="internal")
    labels: List[str] = Field(default_factory=list)
    producer_job_id: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class OperatorBudget(BaseModel):
    """Resource limits and deadlines for operator execution."""
    model_config = ConfigDict(extra="forbid")

    deadline_seconds: float = Field(default=60.0, ge=1.0, le=300.0)
    memory_mib: int = Field(default=512, ge=32, le=8192)
    threads: int = Field(default=2, ge=1, le=16)


class OperatorSpec(BaseModel):
    """Normative operator metadata declaration."""
    model_config = ConfigDict(extra="forbid")

    operator_id: str = Field(min_length=1, max_length=128)
    operator_version: str = Field(default="1.0", max_length=32)
    logical_unit: LogicalUnit
    description: str = ""
    accepted_profiles: List[str] = Field(default_factory=lambda: ["cpu"])
    parameter_schema: Dict[str, Any] = Field(default_factory=dict)
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)
    is_deterministic: bool = True
    default_budgets: OperatorBudget = Field(default_factory=OperatorBudget)
    supported_precisions: List[str] = Field(default_factory=lambda: ["float32", "float64"])


class ProcessingRequest(BaseModel):
    """Public execution submission schema."""
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0"] = "1.0"
    logical_unit: LogicalUnit
    operator_id: str = Field(min_length=1, max_length=128)
    operator_version: str = Field(default="1.0", max_length=32)
    inputs: Dict[str, Any] = Field(default_factory=dict)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    model_reference: Optional[str] = None
    execution_preference: ExecutionPreference = ExecutionPreference.CPU_ONLY
    fallback_policy: Literal["forbid", "allow_cpu"] = "allow_cpu"
    budgets: OperatorBudget = Field(default_factory=OperatorBudget)
    client_correlation_id: str = Field(default="", max_length=128)

    def canonical_digest(self) -> str:
        return canonical_digest(self.model_dump(exclude={"client_correlation_id"}))


class PlanNode(BaseModel):
    """A node in an execution plan DAG."""
    model_config = ConfigDict(extra="forbid")

    node_id: str = Field(min_length=1, max_length=64)
    operator_id: str
    operator_version: str = "1.0"
    logical_unit: LogicalUnit
    inputs: Dict[str, str] = Field(default_factory=dict)  # port_name -> source_node_id or artifact_id
    parameters: Dict[str, Any] = Field(default_factory=dict)
    budgets: OperatorBudget = Field(default_factory=OperatorBudget)


class ExecutionPlan(BaseModel):
    """Validated operator DAG with immutable bindings and resource estimates."""
    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(min_length=1, max_length=128)
    schema_version: Literal["1.0"] = "1.0"
    nodes: List[PlanNode] = Field(default_factory=list)
    topological_order: List[str] = Field(default_factory=list)
    estimated_memory_mib: int = 512
    estimated_duration_seconds: float = 1.0
    required_permissions: List[str] = Field(default_factory=list)
    device_candidates: List[str] = Field(default_factory=lambda: ["cpu"])
    plan_digest: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: str = Field(default="")

    def compute_digest(self) -> str:
        dump = self.model_dump(exclude={"plan_digest", "created_at", "expires_at"})
        return canonical_digest(dump)


class DeviceDescriptor(BaseModel):
    """Physical hardware resource descriptor (redacted for safe multi-tenant display)."""
    model_config = ConfigDict(extra="forbid")

    device_id: str = Field(min_length=1, max_length=128)
    device_type: Literal["cpu", "gpu", "npu", "accelerator"] = "cpu"
    vendor: str = "Generic"
    model: str = "Standard CPU Reference"
    usable_cores: int = Field(ge=1)
    usable_memory_mib: int = Field(ge=64)
    supported_profiles: List[str] = Field(default_factory=lambda: ["cpu"])
    driver_version: Optional[str] = None
    runtime_version: Optional[str] = None
    is_qualified: bool = True
    last_probed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ProviderQualification(BaseModel):
    """Attestation record binding operator/model/profile/platform."""
    model_config = ConfigDict(extra="forbid")

    qualification_id: str
    operator_id: str
    profile: str
    platform: str
    runtime_version: str
    evidence_receipt_path: str
    evidence_sha256: str
    verified_at: str
    is_valid: bool = True


class JobRecord(BaseModel):
    """Durable job record in the queue."""
    model_config = ConfigDict(extra="forbid")

    job_id: str
    tenant_id: str
    principal_id: str
    logical_unit: LogicalUnit
    operator_id: str
    status: JobStatus = JobStatus.QUEUED
    plan_digest: str = ""
    request_digest: str = ""
    fencing_token: int = 0
    attempts: int = 0
    max_retries: int = 2
    lease_holder: Optional[str] = None
    lease_expires_at: Optional[float] = None
    created_at: str
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    deadline_at: Optional[str] = None
    cancel_requested: bool = False
    result_artifact_id: Optional[str] = None
    receipt_artifact_id: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None


class ExecutionReceipt(BaseModel):
    """Signed, verifiable execution receipt for a completed processing job."""
    model_config = ConfigDict(extra="forbid")

    receipt_id: str
    job_id: str
    tenant_id: str
    logical_unit: LogicalUnit
    operator_id: str
    operator_version: str
    actual_provider: str  # e.g. "cpu_numpy", "qiskit_aer", "onnx_cpu"
    device_id: str
    input_digests: Dict[str, str] = Field(default_factory=dict)
    output_digests: Dict[str, str] = Field(default_factory=dict)
    was_fallback: bool = False
    fallback_reason: Optional[str] = None
    is_simulation: bool = False
    is_physical_qpu: bool = False
    queue_duration_ms: float = 0.0
    compute_duration_ms: float = 0.0
    total_duration_ms: float = 0.0
    peak_memory_mib: float = 0.0
    outcome: Literal["SUCCEEDED", "FAILED", "CANCELLED", "TIMED_OUT"] = "SUCCEEDED"
    completed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    receipt_digest: str = ""

    def compute_digest(self) -> str:
        dump = self.model_dump(exclude={"receipt_digest"})
        return canonical_digest(dump)


class ModelManifest(BaseModel):
    """Immutable model metadata declaration."""
    model_config = ConfigDict(extra="forbid")

    model_id: str
    name: str
    version: str
    format: Literal["onnx", "gguf", "safetensors"]
    weights_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    tokenizer_version: Optional[str] = None
    license: str
    permitted_tasks: List[str]
    input_shapes: Dict[str, List[int]] = Field(default_factory=dict)
    output_shapes: Dict[str, List[int]] = Field(default_factory=dict)
    estimated_memory_mib: int = 512
    is_promoted: bool = True
