"""Tenant tenancy package (SR-TEN-001..010).

Submodules:

- ``context``    — TenantContext + fail-closed resolution (SR-TEN-001).
- ``isolation``  — Silo/Bridge/Pool models + per-layer placement (SR-TEN-002/003).
- ``quotas``     — quota check/consume/refund + fair lanes (SR-TEN-006).
- ``lifecycle``  — tenant lifecycle state machine + destruction cert (SR-TEN-007).
- ``metering``   — tamper-evident append-only usage meter (SR-TEN-009).
- ``service``    — TenancyService facade binding the above.
- ``router``     — FastAPI fragment via ``build_router(service)``.

Deferred: SR-TEN-004 (live pen-test suite), SR-TEN-005 (BYOK
crypto-shredding), SR-TEN-008 (per-tenant configuration catalog),
SR-TEN-010 (cross-tenant sharing) — marked External gate / ADR-gated in
their respective modules.
"""

from eoip.tenancy.context import (
    PRINCIPAL_HEADER,
    TENANT_HEADER,
    TenantContext,
    TenantContextRequired,
    require_tenant,
    resolve_context,
    tenant_context_dependency,
)
from eoip.tenancy.isolation import (
    IsolationModel,
    IsolationPlacement,
    IsolationRegistry,
    PlacementValidationError,
    REQUIRED_LAYERS,
    model_catalog,
    validate_placement,
)
from eoip.tenancy.lifecycle import (
    CertificateOfDestruction,
    LifecycleError,
    LifecycleEvent,
    TenantLifecycle,
    TenantState,
)
from eoip.tenancy.metering import (
    GENESIS_HASH,
    METER_DIMENSIONS,
    MeterRecord,
    MeteringLog,
)
from eoip.tenancy.quotas import (
    QUOTA_DIMENSIONS,
    Lane,
    QuotaDecision,
    QuotaExceeded,
    QuotaManager,
    QuotaSpec,
)
from eoip.tenancy.service import TenancyService

__all__ = [
    "PRINCIPAL_HEADER",
    "TENANT_HEADER",
    "TenantContext",
    "TenantContextRequired",
    "require_tenant",
    "resolve_context",
    "tenant_context_dependency",
    "IsolationModel",
    "IsolationPlacement",
    "IsolationRegistry",
    "PlacementValidationError",
    "REQUIRED_LAYERS",
    "model_catalog",
    "validate_placement",
    "CertificateOfDestruction",
    "LifecycleError",
    "LifecycleEvent",
    "TenantLifecycle",
    "TenantState",
    "GENESIS_HASH",
    "METER_DIMENSIONS",
    "MeterRecord",
    "MeteringLog",
    "QUOTA_DIMENSIONS",
    "Lane",
    "QuotaDecision",
    "QuotaExceeded",
    "QuotaManager",
    "QuotaSpec",
    "TenancyService",
]
