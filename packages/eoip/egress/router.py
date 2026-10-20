"""HTTP router for the egress gateway (wired later by apps/api).

FastAPI is imported lazily inside ``build_router`` so the rest of the
package stays framework-free.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from eoip.egress.gateway import ConsentRecord, EgressDenied, EgressGateway
from eoip.egress.policy import PolicyRule
from eoip.egress.provider import ServiceProviderManifest


try:  # FastAPI stays an optional import for the package; Request must be resolvable at module level
    from fastapi import Request
except ImportError:  # pragma: no cover
    Request = Any  # type: ignore[assignment,misc]

class EnableEndpointRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    endpoint_id: str
    admin: str
    signer: str
    dpa_ref: str = ""
    residency_region: str = ""
    scope: str = ""


class CallRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    endpoint_id: str
    task: str
    payload: dict[str, Any]
    user_id: str
    role: str
    data_classes: list[str]
    tags: list[str] = Field(default_factory=list)
    region: str | None = None
    approval_id: str | None = None
    dry_run: bool = False
    estimated_cost: float = 0.0


class AddRuleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule: PolicyRule


class KillRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    admin: str
    reason: str = ""
    endpoint_id: str | None = None


class SubmitPluginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    manifest: ServiceProviderManifest


class InstallPluginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    manifest_id: str
    approved_by: str
    acknowledged_fingerprint: str
    consent_ref: str = ""


class AmendConsentRequest(BaseModel):
    """Change of contract terms; any change requires re-approval (SR-LLM-017)."""

    model_config = ConfigDict(extra="forbid")

    admin: str = Field(min_length=1)
    dpa_ref: str | None = None
    residency_region: str | None = None
    scope: str | None = None


def build_router(gateway: EgressGateway):
    """Construct the FastAPI router bound to an ``EgressGateway``.

    The API wiring step (apps/api/app.py) calls ``build_router(gateway)`` —
    no apps/api changes required in this module. Routes:

    * ``POST /api/v1/egress/endpoints/{id}/enable``  — admin enable w/ consent (SR-LLM-010/017)
    * ``POST /api/v1/egress/endpoints/{id}/disable``
    * ``GET  /api/v1/egress/endpoints``               — list endpoints + enabled state
    * ``POST /api/v1/egress/call``                    — execute or dry-run a call (SR-LLM-012)
    * ``POST /api/v1/egress/policy/rules``            — add a matrix rule (SR-LLM-011)
    * ``GET  /api/v1/egress/policy/rules``
    * ``POST /api/v1/egress/kill``                    — global or per-endpoint kill switch (SR-LLM-016)
    * ``GET  /api/v1/egress/manifests``               — immutable per-call manifests (SR-LLM-013)
    * ``GET  /api/v1/egress/report``                  — 'what left the building' export (SR-LLM-013)
    * ``POST /api/v1/egress/plugins/submit``          — Service Provider manifest (SR-CON-010/011)
    * ``POST /api/v1/egress/plugins/install``         — admin-approved install (SR-CON-011)
    * ``GET  /api/v1/egress/plugins``
    """
    from fastapi import APIRouter, HTTPException

    router = APIRouter(prefix="/api/v1/egress", tags=["egress"])

    @router.post("/endpoints/{endpoint_id}/enable")
    def enable_endpoint(endpoint_id: str, body: EnableEndpointRequest) -> dict:
        import time
        import uuid

        try:
            gateway.enable_endpoint(
                endpoint_id, admin=body.admin,
                consent=ConsentRecord(
                    consent_id=f"urn:eoip:egress:consent:{uuid.uuid4().hex[:12]}",
                    endpoint_id=endpoint_id,
                    signer=body.signer,
                    signed_at=time.time(),
                    dpa_ref=body.dpa_ref,
                    residency_region=body.residency_region,
                    scope=body.scope,
                ),
            )
        except (KeyError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {"enabled": endpoint_id}

    @router.get("/endpoints/{endpoint_id}/consent")
    def get_consent(endpoint_id: str) -> dict:
        if endpoint_id not in gateway.endpoints:
            raise HTTPException(status_code=404, detail=f"unknown endpoint {endpoint_id}")
        current = gateway.consents.get(endpoint_id)
        return {
            "endpoint_id": endpoint_id,
            "current": current.model_dump() if current else None,
            "history": [c.model_dump() for c in gateway.consent_history.get(endpoint_id, [])],
            "reapproval_required": endpoint_id in gateway.reapproval_required,
        }

    @router.post("/endpoints/{endpoint_id}/consent/amend")
    def amend_consent(endpoint_id: str, body: AmendConsentRequest) -> dict:
        if endpoint_id not in gateway.endpoints:
            raise HTTPException(status_code=404, detail=f"unknown endpoint {endpoint_id}")
        try:
            required = gateway.amend_consent(endpoint_id, admin=body.admin, dpa_ref=body.dpa_ref,
                                             residency_region=body.residency_region, scope=body.scope)
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        return {"endpoint_id": endpoint_id, "reapproval_required": required}

    @router.post("/endpoints/{endpoint_id}/disable")
    def disable_endpoint(endpoint_id: str, body: KillRequest) -> dict:
        try:
            gateway.disable_endpoint(endpoint_id, admin=body.admin, reason=body.reason)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        return {"disabled": endpoint_id}

    @router.get("/endpoints")
    def list_endpoints() -> dict:
        return {
            "endpoints": [
                {
                    "id": e.id, "kind": e.kind, "region": e.region,
                    "enabled": e.enabled, "url_allowlist": e.url_allowlist,
                }
                for e in gateway.endpoints.values()
            ],
            "kill_switch_global": gateway.kill_switch_global,
            "killed_endpoints": sorted(gateway.killed_endpoints),
        }

    @router.post("/call")
    def call(body: CallRequest) -> dict:
        try:
            result = gateway.call(
                endpoint_id=body.endpoint_id, task=body.task,
                payload=body.payload, user_id=body.user_id, role=body.role,
                data_classes=body.data_classes, tags=body.tags,
                region=body.region, approval_id=body.approval_id,
                dry_run=body.dry_run, estimated_cost=body.estimated_cost,
            )
        except EgressDenied as exc:
            raise HTTPException(status_code=403, detail={
                "reason": exc.reason, "fallback_notice": exc.fallback_notice,
            }) from exc
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except Exception as exc:
            if exc.__class__.__name__ == "BudgetExhausted":
                raise HTTPException(status_code=429, detail=str(exc)) from exc
            raise
        return result

    @router.post("/policy/rules")
    def add_rule(body: AddRuleRequest) -> dict:
        gateway.policy.add_rule(body.rule)
        return {"rule_id": body.rule.rule_id}

    @router.get("/policy/rules")
    def list_rules() -> dict:
        return {"rules": [r.model_dump() for r in gateway.policy.rules],
                "default_level": int(gateway.policy.default_level)}

    @router.post("/kill")
    def kill(body: KillRequest) -> dict:
        if body.endpoint_id:
            gateway.kill_endpoint(body.endpoint_id, admin=body.admin, reason=body.reason)
            return {"killed_endpoint": body.endpoint_id}
        gateway.kill(admin=body.admin, reason=body.reason)
        return {"killed": "global"}

    @router.get("/manifests")
    def manifests() -> dict:
        return {"manifests": [m.model_dump() for m in gateway.manifests]}

    @router.get("/report")
    def report() -> dict:
        return gateway.report()

    @router.post("/plugins/submit")
    def submit_plugin(body: SubmitPluginRequest) -> dict:
        gateway.plugin_registry.submit(body.manifest)
        return {"submitted": body.manifest.id}

    @router.get("/plugins/{manifest_id:path}/install-preview")
    def plugin_install_preview(manifest_id: str) -> dict:
        try:
            return gateway.plugin_registry.install_preview(manifest_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @router.post("/plugins/install")
    def install_plugin(body: InstallPluginRequest, request: Request) -> dict:
        # The approver is the authenticated administrator when the API carries a principal
        # (the admin-prefix middleware has already required the admin role, SR-CON-011).
        principal = getattr(request.state, "principal", None)
        approver = getattr(principal, "username", None) or body.approved_by
        try:
            record = gateway.plugin_registry.install(
                body.manifest_id, approved_by=approver,
                acknowledged_fingerprint=body.acknowledged_fingerprint,
                consent_ref=body.consent_ref,
            )
        except (KeyError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return record.model_dump()

    @router.get("/plugins")
    def list_plugins() -> dict:
        return {
            "plugins": [
                {
                    "id": m.id, "name": m.name, "capability": m.capability,
                    "installed": gateway.plugin_registry.is_installed(m.id),
                    "data_flow": m.data_flow.model_dump(),
                }
                for m in gateway.plugin_registry._manifests.values()
            ]
        }

    return router
