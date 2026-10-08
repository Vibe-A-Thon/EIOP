"""Tenancy service facade — binds lifecycle, quotas, isolation, metering.

Single object the API wiring step constructs and passes to
``tenancy.router.build_router`` (SR-TEN-001/002/003/006/007/009). Also
wires lifecycle deletion certificates into the metering hash chain so
destruction events are tamper-evidently recorded (SR-TEN-007 + SR-TEN-009).
"""

from __future__ import annotations

from eoip.tenancy.isolation import IsolationPlacement, IsolationRegistry
from eoip.tenancy.lifecycle import TenantLifecycle
from eoip.tenancy.metering import MeteringLog
from eoip.tenancy.quotas import QuotaManager


class TenancyService:
    """Aggregates the tenancy subsystems for the HTTP boundary."""

    def __init__(self) -> None:
        self.isolation = IsolationRegistry()
        self.lifecycle = TenantLifecycle(self.isolation)
        self.quotas = QuotaManager()
        self.metering = MeteringLog()
        # Record certificates of destruction into the metering log (SR-TEN-009).
        self.lifecycle.on_destroy = lambda cert: self.metering.record(
            cert.tenant_id,
            {"connectors": 0},
            note=f"destruction:{cert.certificate_id}",
        )
