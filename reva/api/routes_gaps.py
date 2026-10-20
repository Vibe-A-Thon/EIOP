"""REST router for knowledge-gap registry (T-304 / REVA-KG-001..007)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel

from reva.api.routes_warrants import get_kernel
from reva.kernel.gaps import record_gap, update_gap

router = APIRouter(prefix="/gaps", tags=["Knowledge Gaps"])


class CreateGapRequest(BaseModel):
    domain: str
    question: str
    scope: Dict[str, Any]
    severity: str = "medium"
    required_authority: Optional[str] = None
    required_depth: Optional[str] = None
    required_band: Optional[str] = None


class UpdateGapRequest(BaseModel):
    expected_revision: int
    status: Optional[str] = None
    severity: Optional[str] = None
    owner: Optional[str] = None
    due_at: Optional[str] = None
    supporting_warrant_ids: Optional[List[str]] = None
    contradicting_warrant_ids: Optional[List[str]] = None
    resolution: Optional[Dict[str, Any]] = None


@router.get("")
async def list_gaps(
    status: Optional[str] = None,
    domain: Optional[str] = None,
    x_tenant_id: str = Header(default="default"),
):
    """List knowledge gaps by status or domain."""
    kernel = get_kernel()
    cur = kernel.store.conn.cursor()
    query = "SELECT gap_id, revision, status, severity, impact_score_bp, owner, domain, record FROM reva_gap_heads WHERE tenant_id = ?"
    params = [x_tenant_id]
    if status:
        query += " AND status = ?"
        params.append(status)
    if domain:
        query += " AND domain = ?"
        params.append(domain)

    query += " ORDER BY impact_score_bp DESC, gap_id ASC"  # board order: highest impact first
    rows = cur.execute(query, params).fetchall()
    items = []
    for r in rows:
        items.append({
            "domain": r["domain"],
            "gap_id": r["gap_id"],
            "impact_score_bp": r["impact_score_bp"],
            "owner": r["owner"],
            "revision": r["revision"],
            "severity": r["severity"],
            "status": r["status"],
        })
    return {"items": items, "total": len(items)}


@router.get("/{gap_id}")
async def get_gap(
    gap_id: str,
    x_tenant_id: str = Header(default="default"),
):
    """Get latest revision head of a knowledge gap."""
    kernel = get_kernel()
    cur = kernel.store.conn.cursor()
    row = cur.execute(
        "SELECT record FROM reva_gap_heads WHERE tenant_id = ? AND gap_id = ?",
        (x_tenant_id, gap_id),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"Knowledge gap '{gap_id}' not found")
    import json
    return json.loads(row["record"])


@router.post("")
async def create_gap(
    body: CreateGapRequest,
    x_tenant_id: str = Header(default="default"),
    x_principal_id: str = Header(default="system"),
):
    """Record a new knowledge gap with deduplication and revision tracking."""
    kernel = get_kernel()
    gap = record_gap(
        store=kernel.store,
        tenant_id=x_tenant_id,
        domain=body.domain,
        question=body.question,
        scope=body.scope,
        severity=body.severity,
        actor=x_principal_id,
    )
    return gap


@router.patch("/{gap_id}")
async def patch_gap(
    gap_id: str,
    body: UpdateGapRequest,
    x_tenant_id: str = Header(default="default"),
    x_principal_id: str = Header(default="system"),
):
    """Update knowledge gap revision with state machine validation."""
    kernel = get_kernel()
    patch_dict = body.model_dump(exclude_unset=True)
    patch_dict.pop("expected_revision", None)

    updated = update_gap(
        store=kernel.store,
        tenant_id=x_tenant_id,
        gap_id=gap_id,
        expected_revision=body.expected_revision,
        patch=patch_dict,
        actor=x_principal_id,
    )
    return updated
