"""HTTP router for the layered configuration framework (SR-CFG-001..006).

``build_router(store, flag_store=None)`` returns a FastAPI router mounted
under ``/api/v1/config``. FastAPI is imported lazily inside the factory so
the package stays importable without the web stack (same pattern as
``eoip.graph.bitemporal.build_router``).

Routes:

* ``GET  /api/v1/config/definitions``           — registered setting defs
* ``GET  /api/v1/config/effective``             — effective value for a key
* ``GET  /api/v1/config/explain``               — layer-chain trace (SR-CFG-003)
* ``POST /api/v1/config/set``                   — write a setting at a layer
* ``POST /api/v1/config/bounds``                — set floor/ceiling (SR-CFG-002)
* ``GET  /api/v1/config/audit``                 — audit trail for a key
* ``POST /api/v1/config/rollback``              — rollback to a version (SR-CFG-004)
* ``POST /api/v1/config/import``                — import archive, dry-run ok (SR-CFG-004)
* ``POST /api/v1/config/export``                — export a layer (SR-CFG-004)
* ``POST /api/v1/config/diff``                  — diff two archives (SR-CFG-004)
* ``GET/POST /api/v1/config/flags``             — feature flags (SR-CFG-005)
* ``POST /api/v1/config/reload-subscribe``      — hot-reload probe (SR-CFG-006)

Tenant context (SR-TEN-001) is taken from the query/body ``tenant`` field;
enforcement of mandatory tenant context at the gateway is an external
gate (wired in apps/api).
"""

from __future__ import annotations

from typing import Any

from eoip.config.ascode import ConfigArchive, diff_configs, export_config, import_config, rollback
from eoip.config.layered import (
    ConfigChangeRecord,
    ConfigStore,
    ExplainResult,
    FeatureFlag,
    FeatureFlagStore,
    LayerRef,
    SettingDef,
    SettingScope,
)


def build_router(store: ConfigStore, flag_store: FeatureFlagStore | None = None):
    """Construct the FastAPI router bound to a ConfigStore."""
    from fastapi import APIRouter, HTTPException, Query

    router = APIRouter(prefix="/api/v1/config", tags=["config"])
    flags = flag_store or FeatureFlagStore(store)

    def _not_found(exc: Exception) -> HTTPException:
        return HTTPException(status_code=404, detail=str(exc))

    def _bad_request(exc: Exception) -> HTTPException:
        return HTTPException(status_code=422, detail=str(exc))

    @router.get("/definitions", response_model=list[SettingDef])
    def definitions() -> list[SettingDef]:
        return store.definitions()

    @router.get("/effective")
    def effective(
        key: str,
        tenant: str | None = Query(default=None),
        business_unit: str | None = Query(default=None),
        workspace: str | None = Query(default=None),
        user_id: str | None = Query(default=None),
    ) -> dict[str, Any]:
        scope = SettingScope(tenant=tenant, business_unit=business_unit, workspace=workspace)
        try:
            return store.get(key, scope, user_id=user_id).model_dump()
        except KeyError as exc:
            raise _not_found(exc) from exc

    @router.get("/explain", response_model=ExplainResult)
    def explain(
        key: str,
        tenant: str | None = Query(default=None),
        business_unit: str | None = Query(default=None),
        workspace: str | None = Query(default=None),
        user_id: str | None = Query(default=None),
    ) -> ExplainResult:
        scope = SettingScope(tenant=tenant, business_unit=business_unit, workspace=workspace)
        try:
            return store.explain(key, scope, user_id=user_id)
        except KeyError as exc:
            raise _not_found(exc) from exc

    @router.post("/set", response_model=ConfigChangeRecord)
    def set_(body: dict[str, Any]) -> ConfigChangeRecord:
        try:
            return store.set(
                body["key"],
                LayerRef.model_validate(body["layer"]),
                body["value"],
                actor=body.get("actor", "api"),
                reason=body.get("reason", ""),
            )
        except KeyError as exc:
            raise _not_found(exc) from exc
        except ValueError as exc:
            raise _bad_request(exc) from exc

    @router.post("/bounds", response_model=ConfigChangeRecord)
    def bounds(body: dict[str, Any]) -> ConfigChangeRecord:
        try:
            return store.set_bound(
                body["key"],
                LayerRef.model_validate(body["layer"]),
                floor=body.get("floor"),
                ceiling=body.get("ceiling"),
                actor=body.get("actor", "api"),
            )
        except KeyError as exc:
            raise _not_found(exc) from exc

    @router.get("/audit", response_model=list[ConfigChangeRecord])
    def audit(key: str) -> list[ConfigChangeRecord]:
        try:
            return store.audit_trail(key)
        except KeyError as exc:
            raise _not_found(exc) from exc

    @router.post("/rollback", response_model=ConfigChangeRecord)
    def rollback_(body: dict[str, Any]) -> ConfigChangeRecord:
        try:
            return rollback(
                store,
                body["key"],
                LayerRef.model_validate(body["layer"]),
                int(body["to_version"]),
                actor=body.get("actor", "api"),
            )
        except KeyError as exc:
            raise _not_found(exc) from exc
        except ValueError as exc:
            raise _bad_request(exc) from exc

    @router.post("/export", response_model=ConfigArchive)
    def export_(body: dict[str, Any]) -> ConfigArchive:
        try:
            return export_config(store, LayerRef.model_validate(body["layer"]))
        except KeyError as exc:
            raise _not_found(exc) from exc

    @router.post("/import")
    def import_(body: dict[str, Any]) -> dict[str, Any]:
        payload = body["payload"]
        fmt = body.get("format", "json")
        if isinstance(payload, dict):
            payload = ConfigArchive.model_validate(payload).model_dump()
        result = import_config(
            store,
            payload,
            fmt=fmt,
            dry_run=body.get("dry_run", False),
            actor=body.get("actor", "api"),
            approved_by=body.get("approved_by"),
        )
        return {
            "ok": result["ok"],
            "dry_run": result["dry_run"],
            "errors": result["errors"],
            "applied": [c.model_dump() for c in result["applied"]],
        }

    @router.post("/diff")
    def diff(body: dict[str, Any]) -> dict[str, Any]:
        a = ConfigArchive.model_validate(body["from"])
        b = ConfigArchive.model_validate(body["to"])
        result = diff_configs(a, b)
        payload = result.model_dump()
        payload["changed_count"] = result.changed_count
        return payload

    @router.get("/flags", response_model=list[FeatureFlag])
    def list_flags() -> list[FeatureFlag]:
        return flags.list()

    @router.post("/flags", response_model=FeatureFlag)
    def set_flag(body: dict[str, Any]) -> FeatureFlag:
        try:
            return flags.set(body["key"], bool(body["enabled"]), actor=body.get("actor", "api"))
        except KeyError as exc:
            raise _not_found(exc) from exc

    @router.post("/reload-subscribe")
    def reload_subscribe(body: dict[str, Any]) -> dict[str, Any]:
        """Validate a key is hot-reloadable (SR-CFG-006).

        Actual streaming subscription (SSE) is external gate; this endpoint
        verifies the key is non-structural and reports reloadability.
        """
        key = body["key"]
        try:
            definition = next(d for d in store.definitions() if d.key == key)
        except StopIteration as exc:
            raise _not_found(KeyError(f"unknown setting: {key}")) from exc
        return {"key": key, "reloadable": not definition.structural}

    return router
