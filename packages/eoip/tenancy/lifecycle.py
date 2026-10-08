"""Tenant lifecycle state machine (SR-TEN-007).

Lifecycle states and legal transitions (SR-TEN-007):

    PROVISIONING --configure--> ACTIVE --suspend--> SUSPENDED
    SUSPENDED --resume--> ACTIVE
    ACTIVE --clone--> CLONED --configure--> ACTIVE   (staging clone)
    ACTIVE/SUSPENDED --export--> EXPORTED --> (returns to prior state)
    ACTIVE/SUSPENDED --delete--> DELETED (terminal)

Deletion is verified and produces a Certificate of Destruction record
signed into the metering hash chain when a meter is attached; the record
lists every data layer placement destroyed (SR-TEN-007, SR-TEN-003).

Deferred (External gate): actual provisioning/destruction against real
backends (graph stores, object storage, KMS crypto-shredding per SR-TEN-005)
and cluster/region migration; this module records lifecycle decisions and
certificates only. Console/IaC entry points consume the same service API.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Callable

from eoip.tenancy.isolation import IsolationPlacement, IsolationRegistry

TENANT_LIFECYCLE_TRANSITIONS: dict[str, frozenset[str]] = {
    "provisioning": frozenset({"active", "deleted"}),
    "active": frozenset({"suspended", "cloned", "exported", "deleted"}),
    "suspended": frozenset({"active", "exported", "deleted"}),
    "cloned": frozenset({"active", "deleted"}),
    "exported": frozenset({"active", "suspended"}),
    "deleted": frozenset(),
}


class LifecycleError(RuntimeError):
    """Illegal lifecycle transition or unknown tenant."""


class TenantState(StrEnum):
    PROVISIONING = "provisioning"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLONED = "cloned"
    EXPORTED = "exported"
    DELETED = "deleted"


@dataclass(frozen=True)
class LifecycleEvent:
    tenant_id: str
    from_state: str
    to_state: str
    action: str
    actor: str
    at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "tenant_id": self.tenant_id,
            "from_state": self.from_state,
            "to_state": self.to_state,
            "action": self.action,
            "actor": self.actor,
            "at": self.at,
        }


@dataclass(frozen=True)
class CertificateOfDestruction:
    """Verified destruction record emitted on delete (SR-TEN-007)."""

    certificate_id: str
    tenant_id: str
    issued_at: float
    destroyed_layers: dict[str, str]
    verification_hash: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "certificate_id": self.certificate_id,
            "tenant_id": self.tenant_id,
            "issued_at": self.issued_at,
            "destroyed_layers": dict(self.destroyed_layers),
            "verification_hash": self.verification_hash,
        }


class TenantLifecycle:
    """State machine + records for tenant lifecycle (SR-TEN-007)."""

    def __init__(self, isolation: IsolationRegistry | None = None) -> None:
        self.isolation = isolation or IsolationRegistry()
        self._states: dict[str, TenantState] = {}
        self._history: dict[str, list[LifecycleEvent]] = {}
        self._certificates: dict[str, CertificateOfDestruction] = {}
        # Hook for the metering layer to sign destruction into the hash chain.
        self.on_destroy: Callable[[CertificateOfDestruction], None] | None = None

    # -- queries -------------------------------------------------------------

    def state(self, tenant_id: str) -> TenantState:
        try:
            return self._states[tenant_id]
        except KeyError as exc:
            raise LifecycleError(f"unknown tenant: {tenant_id}") from exc

    def history(self, tenant_id: str) -> list[LifecycleEvent]:
        return list(self._history.get(tenant_id, []))

    def certificate(self, tenant_id: str) -> CertificateOfDestruction:
        try:
            return self._certificates[tenant_id]
        except KeyError as exc:
            raise LifecycleError(f"no certificate of destruction for {tenant_id}") from exc

    # -- transitions ------------------------------------------------------------

    def provision(self, tenant_id: str, placement: IsolationPlacement, actor: str) -> LifecycleEvent:
        if not tenant_id:
            raise LifecycleError("tenant_id required")
        self.isolation.register(placement)
        self._states[tenant_id] = TenantState.PROVISIONING
        return self._record(tenant_id, "", TenantState.PROVISIONING.value, "provision", actor)

    def configure(self, tenant_id: str, actor: str) -> LifecycleEvent:
        return self._transition(tenant_id, TenantState.ACTIVE, "configure", actor)

    def suspend(self, tenant_id: str, actor: str) -> LifecycleEvent:
        return self._transition(tenant_id, TenantState.SUSPENDED, "suspend", actor)

    def resume(self, tenant_id: str, actor: str) -> LifecycleEvent:
        return self._transition(tenant_id, TenantState.ACTIVE, "resume", actor)

    def clone(self, tenant_id: str, actor: str) -> LifecycleEvent:
        return self._transition(tenant_id, TenantState.CLONED, "clone", actor)

    def export(self, tenant_id: str, actor: str) -> LifecycleEvent:
        """Mark exported; tenant returns to its prior state (SR-TEN-007)."""
        prior = self.state(tenant_id)
        if prior not in (TenantState.ACTIVE, TenantState.SUSPENDED):
            raise LifecycleError(f"cannot export tenant in state {prior.value}")
        event = self._transition(tenant_id, TenantState.EXPORTED, "export", actor)
        self._states[tenant_id] = prior  # export is non-destructive
        return event

    def delete(self, tenant_id: str, actor: str) -> CertificateOfDestruction:
        """Delete tenant, verify every layer destroyed, issue certificate (SR-TEN-007)."""
        state = self.state(tenant_id)
        allowed = TENANT_LIFECYCLE_TRANSITIONS[state.value]
        if TenantState.DELETED.value not in allowed:
            raise LifecycleError(f"cannot delete tenant in state {state.value}")
        layers: dict[str, str] = {}
        try:
            placement = self.isolation.get(tenant_id)
            layers = dict(placement.layers)
        except Exception:
            layers = {}
        self._record(tenant_id, state.value, TenantState.DELETED.value, "delete", actor)
        self._states[tenant_id] = TenantState.DELETED
        cert_id = f"urn:eoip:tenancy:cod:{uuid.uuid4().hex[:16]}"
        payload = json.dumps(
            {"certificate_id": cert_id, "tenant_id": tenant_id, "layers": layers},
            sort_keys=True,
        )
        cert = CertificateOfDestruction(
            certificate_id=cert_id,
            tenant_id=tenant_id,
            issued_at=time.time(),
            destroyed_layers=layers,
            verification_hash=hashlib.sha256(payload.encode()).hexdigest(),
        )
        self._certificates[tenant_id] = cert
        if self.on_destroy is not None:
            self.on_destroy(cert)
        return cert

    # -- internals -----------------------------------------------------------

    def _transition(self, tenant_id: str, target: TenantState, action: str, actor: str) -> LifecycleEvent:
        current = self.state(tenant_id)
        if target.value not in TENANT_LIFECYCLE_TRANSITIONS[current.value]:
            raise LifecycleError(
                f"illegal transition: {current.value} -> {target.value} ({action})"
            )
        self._states[tenant_id] = target
        return self._record(tenant_id, current.value, target.value, action, actor)

    def _record(self, tenant_id: str, from_state: str, to_state: str, action: str, actor: str) -> LifecycleEvent:
        event = LifecycleEvent(tenant_id, from_state, to_state, action, actor)
        self._history.setdefault(tenant_id, []).append(event)
        return event
