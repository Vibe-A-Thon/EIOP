"""EOIP Processing Runtime package.

Normative implementation of the 10 logical processing units (CPU, GPU, TPU, NPU,
DPU, QPU, APU, LPU, IPU, VPU) with local-first, air-gapped, policy-governed execution.
"""

from eoip.processing.contracts import (
    LogicalUnit,
    JobStatus,
    ExecutionPreference,
    OperatorBudget,
    ExecutionContext,
    ArtifactRef,
    OperatorSpec,
    ProcessingRequest,
    PlanNode,
    ExecutionPlan,
    DeviceDescriptor,
    ProviderQualification,
    JobRecord,
    ExecutionReceipt,
    ModelManifest,
    canonical_digest,
)
from eoip.processing.catalog import (
    OPERATOR_CATALOG,
    get_operator_spec,
    list_operator_specs,
    get_unit_capabilities,
)
from eoip.processing.devices import (
    enumerate_devices,
    get_thread_budget,
)
from eoip.processing.planner import (
    compile_plan,
)
from eoip.processing.service import (
    ProcessingService,
    get_processing_service,
)

__all__ = [
    "LogicalUnit",
    "JobStatus",
    "ExecutionPreference",
    "OperatorBudget",
    "ExecutionContext",
    "ArtifactRef",
    "OperatorSpec",
    "ProcessingRequest",
    "PlanNode",
    "ExecutionPlan",
    "DeviceDescriptor",
    "ProviderQualification",
    "JobRecord",
    "ExecutionReceipt",
    "ModelManifest",
    "canonical_digest",
    "OPERATOR_CATALOG",
    "get_operator_spec",
    "list_operator_specs",
    "get_unit_capabilities",
    "enumerate_devices",
    "get_thread_budget",
    "compile_plan",
    "ProcessingService",
    "get_processing_service",
]
