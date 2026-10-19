"""REST router for warrants and bundles (T-303 / REVA-IF-001..008)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Header, HTTPException, Query, Request
from pydantic import BaseModel

from reva.core.errors import RevaNotFoundError, RevaValidationError
from reva.kernel.builder import ObservationDraft
from reva.kernel.kernel import WarrantKernel

router = APIRouter(prefix="/warrants", tags=["Warrants"])

_KERNEL: Optional[WarrantKernel] = None


def set_api_kernel(kernel: WarrantKernel) -> None:
    global _KERNEL
    _KERNEL = kernel


def get_kernel() -> WarrantKernel:
    if _KERNEL is None:
        raise HTTPException(status_code=503, detail="Warrant kernel not initialized")
    return _KERNEL


class QueryRequest(BaseModel):
    subject_key: Optional[str] = None
    predicate: Optional[str] = None
    as_of_valid: Optional[str] = None
    as_of_recorded: Optional[str] = None
    limit: int = 100
    offset: int = 0


class RetractRequest(BaseModel):
    reason: str


class BundleExportRequest(BaseModel):
    warrant_ids: List[str]
    depth: int = 1
    include_restricted: bool = False


@router.get("/{warrant_id}")
async def get_warrant(
    warrant_id: str,
    x_tenant_id: str = Header(default="default"),
    x_principal_id: str = Header(default="system"),
):
    """Retrieve sealed warrant with cryptographic and ACL verification."""
    kernel = get_kernel()
    w = kernel.get(tenant_id=x_tenant_id, principal_id=x_principal_id, warrant_id=warrant_id)
    return {
        "body": w.body.canonical_dict(),
        "envelope": w.envelope.model_dump(mode="json"),
        "warrant_id": w.warrant_id,
    }


@router.post("/query")
async def query_warrants(
    body: QueryRequest,
    x_tenant_id: str = Header(default="default"),
    x_principal_id: str = Header(default="system"),
):
    """Query active or bitemporal warrants filtered by ACL."""
    kernel = get_kernel()
    warrants = kernel.query(
        tenant_id=x_tenant_id,
        principal_id=x_principal_id,
        subject_key=body.subject_key,
        predicate=body.predicate,
        as_of_valid=body.as_of_valid,
        as_of_recorded=body.as_of_recorded,
        limit=body.limit,
        offset=body.offset,
    )
    return {
        "items": [
            {
                "body": w.body.canonical_dict(),
                "envelope": w.envelope.model_dump(mode="json"),
                "warrant_id": w.warrant_id,
            }
            for w in warrants
        ],
        "total": len(warrants),
    }


@router.post("")
async def issue_warrant(
    draft: ObservationDraft,
    x_tenant_id: str = Header(default="default"),
    x_principal_id: str = Header(default="system"),
):
    """Issue a new observation warrant through validation and transparency log."""
    kernel = get_kernel()
    sealed = kernel.issue(tenant_id=x_tenant_id, draft=draft)
    return {
        "body": sealed.body.canonical_dict(),
        "envelope": sealed.envelope.model_dump(mode="json"),
        "warrant_id": sealed.warrant_id,
    }


@router.post("/{warrant_id}/supersede")
async def supersede_warrant(
    warrant_id: str,
    new_draft: ObservationDraft,
    reason: str = Query(...),
    x_tenant_id: str = Header(default="default"),
    x_principal_id: str = Header(default="system"),
):
    """Supersede existing warrant with new version."""
    kernel = get_kernel()
    sealed = kernel.supersede(tenant_id=x_tenant_id, old_warrant_id=warrant_id, new_draft=new_draft, reason=reason)
    return {
        "body": sealed.body.canonical_dict(),
        "envelope": sealed.envelope.model_dump(mode="json"),
        "warrant_id": sealed.warrant_id,
    }


@router.post("/{warrant_id}/retract")
async def retract_warrant(
    warrant_id: str,
    body: RetractRequest,
    x_tenant_id: str = Header(default="default"),
    x_principal_id: str = Header(default="system"),
):
    """Retract warrant with immutable audit link."""
    kernel = get_kernel()
    sealed = kernel.retract(tenant_id=x_tenant_id, warrant_id=warrant_id, reason=body.reason)
    return {"status": "retracted", "warrant_id": sealed.warrant_id}
