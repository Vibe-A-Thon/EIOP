"""REVA FastAPI API Router package (T-004 / T-301)."""

from __future__ import annotations

from fastapi import APIRouter

from reva.api.middleware import register_reva_error_handlers
from reva.api.routes_contradictions import router as contradictions_router
from reva.api.routes_gaps import router as gaps_router
from reva.api.routes_logs import router as logs_router
from reva.api.routes_pd import router as pd_router
from reva.api.routes_warrants import router as warrants_router, set_api_kernel

reva_router = APIRouter()


@reva_router.get("/health")
async def reva_health():
    """Health check endpoint for REVA subsystem."""
    return {"status": "ok", "version": "1.0.0"}


reva_router.include_router(warrants_router)
reva_router.include_router(logs_router)
reva_router.include_router(gaps_router)
reva_router.include_router(contradictions_router)
reva_router.include_router(pd_router)

__all__ = ["reva_router", "register_reva_error_handlers", "set_api_kernel"]
