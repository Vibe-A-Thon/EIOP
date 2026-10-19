"""REST router for contradiction detection and resolution (T-305 / REVA-CX-001..005)."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from reva.api.routes_warrants import get_kernel
from reva.kernel.contradictions import resolve_contradiction

router = APIRouter(prefix="/contradictions", tags=["Contradictions"])


class ResolveContradictionRequest(BaseModel):
    rule: str  # authority_precedence | recency | valid_time_split | human_decision
    winner_warrant_id: Optional[str] = None
    rationale: str = ""


@router.get("")
async def list_contradictions(
    status: Optional[str] = None,
    x_tenant_id: str = Header(default="default"),
):
    """List open or resolved contradictions for tenant."""
    kernel = get_kernel()
    cur = kernel.store.conn.cursor()
    query = "SELECT contradiction_id, record, status, conflict_kind, subject_key, predicate, opened_at FROM reva_contradictions WHERE tenant_id = ?"
    params = [x_tenant_id]
    if status:
        query += " AND status = ?"
        params.append(status)

    rows = cur.execute(query, params).fetchall()
    items = []
    for r in rows:
        items.append({
            "conflict_kind": r["conflict_kind"],
            "contradiction_id": r["contradiction_id"],
            "opened_at": r["opened_at"],
            "predicate": r["predicate"],
            "status": r["status"],
            "subject_key": r["subject_key"],
        })
    return {"items": items, "total": len(items)}


@router.get("/{contradiction_id}")
async def get_contradiction(
    contradiction_id: str,
    x_tenant_id: str = Header(default="default"),
):
    """Get contradiction details and member warrant links."""
    kernel = get_kernel()
    cur = kernel.store.conn.cursor()
    row = cur.execute(
        "SELECT record FROM reva_contradictions WHERE tenant_id = ? AND contradiction_id = ?",
        (x_tenant_id, contradiction_id),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"Contradiction '{contradiction_id}' not found")
    return json.loads(row["record"])


@router.post("/{contradiction_id}/resolve")
async def resolve(
    contradiction_id: str,
    body: ResolveContradictionRequest,
    x_tenant_id: str = Header(default="default"),
    x_principal_id: str = Header(default="system"),
):
    """Resolve contradiction according to normative resolution rule."""
    kernel = get_kernel()
    result = resolve_contradiction(
        store=kernel.store,
        tenant_id=x_tenant_id,
        contradiction_id=contradiction_id,
        rule=body.rule,
        winner_warrant_id=body.winner_warrant_id,
        decided_by=x_principal_id,
    )
    return result
