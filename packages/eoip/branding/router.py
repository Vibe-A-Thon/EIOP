"""HTTP router for white-label branding (SR-WL-001/003/006/007, SR-ONT-007).

``build_router(...)`` constructs the FastAPI router with a LAZY fastapi
import, matching ``eoip.graph.bitemporal.build_router``. The API wiring
step (apps/api) includes this router under ``/api/v1/branding`` — no
apps/ changes are made here.
"""

from __future__ import annotations

from starlette.requests import Request

from eoip.branding.content import LegalContentKind, LegalContentRegistry
from eoip.branding.localization import LocalizationRegistry
from eoip.branding.terminology import TerminologyRegistry
from eoip.branding.theme import ThemeMode, ThemeRegistry
from pydantic import BaseModel


class RenameRequest(BaseModel):
    canonical_types: list[str]


class CanonicalizeRequest(BaseModel):
    labels: list[str]


def build_router(
    themes: ThemeRegistry,
    terminology: TerminologyRegistry | None = None,
    locales: LocalizationRegistry | None = None,
    legal: LegalContentRegistry | None = None,
):
    """Construct the FastAPI router for branding endpoints.

    Routes:
    * ``GET  /api/v1/branding/theme``                 — resolved theme tokens (?tenant_id, ?mode)
    * ``POST /api/v1/branding/terminology/rename``    — canonical -> tenant labels
    * ``POST /api/v1/branding/terminology/canonicalize`` — tenant label -> canonical
    * ``GET  /api/v1/branding/locales/{locale}/message`` — localized string lookup
    * ``GET  /api/v1/branding/legal``                 — published legal/onboarding content
    """
    from fastapi import APIRouter, Query

    def _tenant(request: Request, requested: str | None) -> str | None:
        """SEC-003: derive/validate tenant from the authenticated principal.

        A client-supplied tenant_id is only a selector; a tenant-bound principal
        may not read another tenant's branding. Falls back gracefully if no
        principal is attached (unauthenticated handling happens upstream).
        """
        principal = getattr(request.state, "principal", None)
        if principal is None:
            return requested
        from eoip.tenancy.context import authorized_tenant, TenantContextRequired
        try:
            return authorized_tenant(principal, requested)
        except TenantContextRequired:
            from fastapi import HTTPException
            raise HTTPException(status_code=403, detail="Cross-tenant branding access forbidden")

    router = APIRouter(prefix="/api/v1/branding", tags=["branding"])
    terminology = terminology or TerminologyRegistry()
    locales = locales or LocalizationRegistry()
    legal = legal or LegalContentRegistry()

    @router.get("/theme")
    def theme_view(request: Request, tenant_id: str | None = Query(default=None), mode: ThemeMode = Query(default=ThemeMode.LIGHT)):
        return themes.resolve_view(_tenant(request, tenant_id), mode)

    @router.post("/terminology/rename")
    def rename(body: RenameRequest, request: Request, tenant_id: str | None = Query(default=None)):
        t = _tenant(request, tenant_id)
        return {"renames": terminology.get(t or "").apply(body.canonical_types)}

    @router.post("/terminology/canonicalize")
    def canonicalize(body: CanonicalizeRequest, request: Request, tenant_id: str | None = Query(default=None)):
        t = _tenant(request, tenant_id)
        return {"canonical": {label: terminology.canonicalize(t, label) for label in body.labels}}

    @router.get("/locales/{locale}/message")
    def locale_message(locale: str, request: Request, key: str, tenant_id: str = Query(...), default: str | None = Query(default=None)):
        t = _tenant(request, tenant_id)
        return {"key": key, "text": locales.message(t, locale, key, default), "locale": locale}

    @router.get("/legal")
    def legal_content(request: Request, tenant_id: str = Query(...), kind: LegalContentKind | None = Query(default=None)):
        t = _tenant(request, tenant_id)
        return {"records": [r.model_dump() for r in legal.published(t, kind)]}

    return router
