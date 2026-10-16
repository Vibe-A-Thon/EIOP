"""Tenancy service facade — binds lifecycle, quotas, isolation, metering.

Single object the API wiring step constructs and passes to
``tenancy.router.build_router`` (SR-TEN-001/002/003/006/007/009). Also
wires lifecycle deletion certificates into the metering hash chain so
destruction events are tamper-evidently recorded (SR-TEN-007 + SR-TEN-009).
"""

from __future__ import annotations

from eoip.graph.named_graph import NamedGraphManager, NamedGraphStore, TenantConfig
from eoip.graph.store import GraphStore
from eoip.tenancy.isolation import IsolationRegistry
from eoip.tenancy.lifecycle import TenantLifecycle
from eoip.tenancy.metering import MeteringLog
from eoip.tenancy.quotas import QuotaManager


class TenancyService:
    """Aggregates the tenancy subsystems for the HTTP boundary."""

    def __init__(self, graph_store: GraphStore | None = None) -> None:
        self.isolation = IsolationRegistry()
        self.lifecycle = TenantLifecycle(self.isolation)
        self.quotas = QuotaManager()
        self.metering = MeteringLog()
        self.named_graphs = NamedGraphManager(graph_store) if graph_store is not None else None
        # Record certificates of destruction into the metering log (SR-TEN-009).
        self.lifecycle.on_destroy = lambda cert: self.metering.record(
            cert.tenant_id,
            {"connectors": 0},
            note=f"destruction:{cert.certificate_id}",
        )

    def named_graph_for(self, tenant_id: str) -> NamedGraphStore:
        if self.named_graphs is None:
            raise RuntimeError("tenancy service was created without a graph store")
        tenant = self.named_graphs.get_tenant(tenant_id)
        if tenant is None:
            tenant = self.named_graphs.create_tenant(TenantConfig(tenant_id=tenant_id, graph_name=f"g:{tenant_id}"))
        return tenant
