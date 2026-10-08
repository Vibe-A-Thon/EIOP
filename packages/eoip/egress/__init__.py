"""Egress gateway — the only path to external models (SR-LLM-010..020, SR-CON-010/011).

Policy-gated, audited, observable single egress path: sharing-level
policy matrix (most-restrictive-wins, default deny S0), payload
transforms down to the permitted level, DLP + canary scanning,
reversible tokenization vault, immutable per-call EgressManifests with a
"what left the building" export, kill switch + budgets, consent/contract
records for endpoint enablement, and Service Provider plugin manifests
with Data-Flow declarations requiring admin approval.

No FastAPI imports at package import time — use ``eoip.egress.router.build_router``.
"""

from eoip.egress.dlp import CanaryRegistry, CanaryRecord, DlpScanner, DlpFinding, DlpReport
from eoip.egress.gateway import (
    BudgetExhausted,
    ConsentRecord,
    EgressDenied,
    EgressGateway,
    EndpointConfig,
    Transport,
)
from eoip.egress.manifest import (
    EgressManifest,
    hash_bytes,
    hash_payload,
    new_manifest,
    what_left_the_building,
)
from eoip.egress.policy import (
    KNOWN_TAGS,
    RESTRICTED_CLASSES,
    SENSITIVE_TAGS,
    ApprovalRequirement,
    DataClass,
    EgressTask,
    PolicyDecision,
    PolicyEngine,
    PolicyRule,
    SharingLevel,
)
from eoip.egress.provider import (
    KNOWN_PLUGIN_CAPABILITIES,
    DataFlowManifest,
    PluginCapability,
    PluginInstallRecord,
    PluginRegistry,
    ServiceProviderManifest,
)
from eoip.egress.transforms import (
    K_ANONYMITY_DEFAULT,
    TransformError,
    aggregate,
    redact,
    schema_strip,
    synthetic,
    tokenize,
    transform,
)
from eoip.egress.vault import TokenVault, VaultEntry

__all__ = [
    "ApprovalRequirement", "BudgetExhausted", "CanaryRecord", "CanaryRegistry",
    "ConsentRecord", "DataClass", "DataFlowManifest", "DlpFinding",
    "DlpReport", "DlpScanner", "EgressDenied", "EgressGateway",
    "EgressManifest", "EgressTask", "EndpointConfig", "KNOWN_PLUGIN_CAPABILITIES",
    "KNOWN_TAGS", "K_ANONYMITY_DEFAULT", "PluginCapability",
    "PluginInstallRecord", "PluginRegistry", "PolicyDecision", "PolicyEngine",
    "PolicyRule", "RESTRICTED_CLASSES", "SENSITIVE_TAGS", "ServiceProviderManifest",
    "SharingLevel", "TokenVault", "TransformError", "Transport", "VaultEntry",
    "aggregate", "build_router", "hash_bytes", "hash_payload", "new_manifest",
    "redact", "schema_strip", "synthetic", "tokenize", "transform",
    "what_left_the_building",
]


def build_router(gateway: EgressGateway):  # lazy re-export; fastapi imported inside
    from eoip.egress.router import build_router as _build

    return _build(gateway)
