"""HTTP router for white-label branding (SR-WL-001/003/006/007, SR-ONT-007).

``build_router(...)`` constructs the FastAPI router with a LAZY fastapi
import, matching ``eoip.graph.bitemporal.build_router``. The API wiring
step (apps/api) includes this router under ``/api/v1/branding`` — no
apps/ changes are made here.
"""

from __future__ import annotations

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

    router = APIRouter(prefix="/api/v1/branding", tags=["branding"])
    terminology = terminology or TerminologyRegistry()
    locales = locales or LocalizationRegistry()
    legal = legal or LegalContentRegistry()

    @router.get("/theme")
    def theme_view(tenant_id: str | None = Query(default=None), mode: ThemeMode = Query(default=ThemeMode.LIGHT)):
        return themes.resolve_view(tenant_id, mode)

    @router.post("/terminology/rename")
    def rename(body: RenameRequest, tenant_id: str | None = Query(default=None)):
        return {"renames": terminology.get(tenant_id or "").apply(body.canonical_types)}

    @router.post("/terminology/canonicalize")
    def canonicalize(body: CanonicalizeRequest, tenant_id: str | None = Query(default=None)):
        return {"canonical": {label: terminology.canonicalize(tenant_id, label) for label in body.labels}}

    @router.get("/locales/{locale}/message")
    def locale_message(locale: str, key: str, tenant_id: str = Query(...), default: str | None = Query(default=None)):
        return {"key": key, "text": locales.message(tenant_id, locale, key, default), "locale": locale}

    @router.get("/legal")
    def legal_content(tenant_id: str = Query(...), kind: LegalContentKind | None = Query(default=None)):
        return {"records": [r.model_dump() for r in legal.published(tenant_id, kind)]}

    return router
