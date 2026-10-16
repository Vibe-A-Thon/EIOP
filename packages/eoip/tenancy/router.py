"""FastAPI router fragment for tenancy (SR-TEN-001/002/003/006/007/009).

``build_router(service)`` constructs the router bound to a
``TenancyService``. Lazy fastapi import — no framework import at module
load. All routes are namespaced under ``/api/v1/tenancy`` and require the
fail-closed tenant-context dependency (SR-TEN-001); admin/lifecycle
mutations additionally require the ``X-Principal`` header via the same
dependency.

Routes:

- ``GET  /api/v1/tenancy/context`` — echo the resolved tenant context.
- ``GET  /api/v1/tenancy/isolation/models`` — isolation model catalog.
- ``GET  /api/v1/tenancy/isolation/placement`` — this tenant's placement.
- ``POST /api/v1/tenancy/isolation/placement`` — register/validate placement.
- ``GET  /api/v1/tenancy/quotas`` — quota spec + usage for this tenant.
- ``POST /api/v1/tenancy/quotas/check`` / ``consume`` / ``refund``.
- ``POST /api/v1/tenancy/lifecycle/provision`` / ``configure`` / ``suspend``
  / ``resume`` / ``clone`` / ``export`` / ``delete``.
- ``GET  /api/v1/tenancy/metering/export`` — billing export with chain head.
- ``GET  /api/v1/tenancy/metering/verify`` — re-verify the hash chain.
- ``POST /api/v1/tenancy/metering/record`` — append a meter record.
"""

from typing import Any

from eoip.tenancy.context import tenant_context_dependency
from eoip.tenancy.isolation import (
    IsolationModel,
    IsolationPlacement,
    PlacementValidationError,
    model_catalog,
)
from eoip.tenancy.quotas import QUOTA_DIMENSIONS
from eoip.tenancy.service import TenancyService


def build_router(service: TenancyService):
    """Construct the FastAPI router bound to a TenancyService (lazy import)."""
    from fastapi import APIRouter, HTTPException, Request

    router = APIRouter(prefix="/api/v1/tenancy", tags=["tenancy"])
    dep = tenant_context_dependency()

    def _err(exc: Exception, status: int = 400) -> HTTPException:
        return HTTPException(status_code=status, detail=str(exc))

    # -- context (SR-TEN-001) ---------------------------------------------------

    @router.get("/context")
    def get_context(request: Request) -> dict[str, Any]:
        ctx = dep(request)
        return {"tenant_id": ctx.tenant_id, "urn": ctx.urn, "principal": ctx.principal}

    # -- isolation (SR-TEN-002/003) ----------------------------------------------

    @router.get("/isolation/models")
    def isolation_models(request: Request) -> dict[str, Any]:
        dep(request)
        return {"models": model_catalog()}

    @router.get("/isolation/placement")
    def get_placement(request: Request) -> dict[str, Any]:
        ctx = dep(request)
        try:
            return service.isolation.get(ctx.tenant_id).to_dict()
        except PlacementValidationError as exc:
            raise _err(exc, 404) from exc

    @router.post("/isolation/placement")
    def set_placement(request: Request, body: dict[str, Any]) -> dict[str, Any]:
        ctx = dep(request)
        try:
            placement = IsolationPlacement(
                model=IsolationModel(body["model"]),
                layers=dict(body["layers"]),
                tenant_id=ctx.tenant_id,
            )
            service.isolation.register(placement)
        except (KeyError, ValueError, PlacementValidationError) as exc:
            raise _err(exc) from exc
        return placement.to_dict()

    # -- quotas (SR-TEN-006) -------------------------------------------------------

    @router.get("/quotas")
    def get_quotas(request: Request) -> dict[str, Any]:
        ctx = dep(request)
        spec = service.quotas._specs.get(ctx.tenant_id)
        usage = {
            dim: service.quotas.usage(ctx.tenant_id, dim)
            for dim in sorted(QUOTA_DIMENSIONS)
        }
        return {
            "tenant_id": ctx.tenant_id,
            "lane": service.quotas.lane(ctx.tenant_id).value,
            "spec": spec.to_dict() if spec else None,
            "usage": usage,
        }

    @router.post("/quotas/check")
    def quota_check(request: Request, body: dict[str, Any]) -> dict[str, Any]:
        ctx = dep(request)
        try:
            return service.quotas.check(
                ctx.tenant_id, body["dimension"], int(body.get("amount", 1))
            ).to_dict()
        except ValueError as exc:
            raise _err(exc) from exc

    @router.post("/quotas/consume")
    def quota_consume(request: Request, body: dict[str, Any]) -> dict[str, Any]:
        ctx = dep(request)
        try:
            decision = service.quotas.consume(
                ctx.tenant_id,
                body["dimension"],
                int(body.get("amount", 1)),
                idempotency_key=body.get("idempotency_key"),
            )
        except ValueError as exc:
            raise _err(exc) from exc
        if not decision.allowed:
            raise HTTPException(status_code=429, detail=decision.to_dict())
        return decision.to_dict()

    @router.post("/quotas/refund")
    def quota_refund(request: Request, body: dict[str, Any]) -> dict[str, Any]:
        ctx = dep(request)
        try:
            return service.quotas.refund(
                ctx.tenant_id,
                body["dimension"],
                int(body.get("amount", 1)),
                idempotency_key=body.get("idempotency_key"),
            ).to_dict()
        except ValueError as exc:
            raise _err(exc) from exc

    # -- lifecycle (SR-TEN-007) ------------------------------------------------------

    @router.post("/lifecycle/provision")
    def provision(request: Request, body: dict[str, Any]) -> dict[str, Any]:
        ctx = dep(request)
        try:
            placement = IsolationPlacement(
                model=IsolationModel(body["model"]),
                layers=dict(body["layers"]),
                tenant_id=ctx.tenant_id,
            )
            event = service.lifecycle.provision(ctx.tenant_id, placement, ctx.principal)
        except (KeyError, ValueError, PlacementValidationError) as exc:
            raise _err(exc) from exc
        return event.to_dict()

    def _lifecycle_action(action: str):
        def handler(request: Request) -> Any:
            ctx = dep(request)
            try:
                if action == "delete":
                    return service.lifecycle.delete(ctx.tenant_id, ctx.principal).to_dict()
                method = getattr(service.lifecycle, action)
                return method(ctx.tenant_id, ctx.principal).to_dict()
            except Exception as exc:
                raise _err(exc) from exc

        return handler

    for _action in ("configure", "suspend", "resume", "clone", "export"):
        router.add_api_route(
            f"/lifecycle/{_action}",
            _lifecycle_action(_action),
            methods=["POST"],
            name=f"tenancy_lifecycle_{_action}",
        )
    router.add_api_route(
        "/lifecycle/delete",
        _lifecycle_action("delete"),
        methods=["POST"],
        name="tenancy_lifecycle_delete",
    )

    # -- metering (SR-TEN-009) --------------------------------------------------------

    @router.post("/metering/record")
    def meter_record(request: Request, body: dict[str, Any]) -> dict[str, Any]:
        ctx = dep(request)
        try:
            entry = service.metering.record(
                ctx.tenant_id, dict(body["dimensions"]), note=body.get("note", "")
            )
        except ValueError as exc:
            raise _err(exc) from exc
        return entry.to_dict()

    @router.get("/metering/verify")
    def meter_verify(request: Request) -> dict[str, Any]:
        ctx = dep(request)
        return {
            "tenant_id": ctx.tenant_id,
            "verified": service.metering.verify_chain(ctx.tenant_id),
            "chain_head": service.metering.chain_head(ctx.tenant_id),
        }

    @router.get("/metering/export")
    def meter_export(request: Request) -> dict[str, Any]:
        ctx = dep(request)
        return service.metering.export(ctx.tenant_id)

    return router
