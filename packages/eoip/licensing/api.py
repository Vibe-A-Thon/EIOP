"""FastAPI router fragment for licensing (SR-DEP-007, SR-TEN-009).

``build_router(checker, meter)`` mounts read-only status/verification and the
tamper-evident meter endpoints under ``/api/v1/licensing``. The fastapi import
is lazy so the rest of the package stays importable without the web
dependency (same pattern as ``eoip.graph.bitemporal.build_router``).

Wiring step (apps/api): build an :class:`EntitlementChecker` from the
deployed signed license file plus a :class:`UsageMeter`, then
``app.include_router(build_router(checker, meter))``. The vendor key must
never be committed; apps/api decides its source (env, key file — External
gate).
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from eoip.licensing.entitlements import EntitlementChecker, CheckOutcome
from eoip.licensing.license_file import LicenseVerification, verify_license
from eoip.licensing.meter import UsageMeter


class LicenseVerifyRequest(BaseModel):
    """Verify a signed license document against a vendor key.

    Sending the vendor key in the body is acceptable for offline admin
    verification on an air-gapped box; a proper key-handling integration is an
    External gate.
    """

    model_config = ConfigDict(extra="forbid")

    document: dict[str, Any]
    vendor_key: str = Field(min_length=1)


class MeterRecordRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metric: str = Field(min_length=1)
    value: int = Field(default=1, ge=0)
    tenant_id: str | None = None


class ModuleCheckRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    module: str = Field(min_length=1)


def build_router(checker: EntitlementChecker, meter: UsageMeter):
    """Construct the FastAPI router bound to an EntitlementChecker and UsageMeter.

    Routes:
    ``GET  /api/v1/licensing/status``           — entitlement summary + notice
    ``POST /api/v1/licensing/verify``           — offline-style signature verify
    ``POST /api/v1/licensing/check-module``     — module entitlement check
    ``POST /api/v1/licensing/meter/record``     — append a metered usage event
    ``GET  /api/v1/licensing/meter/verify``     — re-verify the meter hash chain
    ``GET  /api/v1/licensing/meter/export``     — billing usage export
    """
    from fastapi import APIRouter

    router = APIRouter(prefix="/api/v1/licensing", tags=["licensing"])

    @router.get("/status")
    def status() -> dict[str, Any]:
        return checker.summary()

    @router.post("/verify", response_model=LicenseVerification)
    def verify(body: LicenseVerifyRequest) -> LicenseVerification:
        return verify_license(body.document, body.vendor_key)

    @router.post("/check-module", response_model=CheckOutcome)
    def check_module(body: ModuleCheckRequest) -> CheckOutcome:
        return checker.degrade(checker.check_module(body.module))

    @router.post("/meter/record")
    def meter_record(body: MeterRecordRequest) -> dict[str, Any]:
        event = meter.record(body.metric, body.value, tenant_id=body.tenant_id)
        return event.model_dump(mode="json")

    @router.get("/meter/verify")
    def meter_verify() -> dict[str, Any]:
        return meter.verify().model_dump()

    @router.get("/meter/export")
    def meter_export() -> dict[str, Any]:
        return meter.export()

    return router
