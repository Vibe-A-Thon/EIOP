"""REST router for Proof-of-Done engine, obligations, closure, and ledger (T-216 / REVA-IF-020..026)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional
from fastapi import APIRouter, Header, HTTPException, Query, Response
from pydantic import BaseModel

from reva.api.routes_warrants import get_kernel
from reva.pd.bindings import Binding, sync_bindings
from reva.pd.closure import ClosureContext, evaluate_closure
from reva.pd.export_html import render_ledger_html
from reva.pd.ledger import LedgerRecord, build_ledger
from reva.pd.obligations import Obligation, sync_obligations

router = APIRouter(prefix="/pd", tags=["Proof of Done"])


class SyncObligationsRequest(BaseModel):
    obligations: List[Obligation]


class SyncBindingsRequest(BaseModel):
    bindings: List[Binding]


class EvaluateClosureRequest(BaseModel):
    commit: str = "HEAD"
    scope: str = "all"


@router.get("/obligations")
async def list_obligations(
    disposition: Optional[str] = None,
    x_tenant_id: str = Header(default="default"),
):
    """List obligations for tenant."""
    kernel = get_kernel()
    cur = kernel.store.conn.cursor()
    query = "SELECT key, version, digest, definition, reviewed_warrant_id, disposition FROM reva_obligations WHERE tenant_id = ?"
    params = [x_tenant_id]
    if disposition:
        query += " AND disposition = ?"
        params.append(disposition)

    rows = cur.execute(query, params).fetchall()
    items = [json.loads(r["definition"]) for r in rows]
    return {"items": items, "total": len(items)}


@router.post("/obligations/sync")
async def sync_ob(
    body: SyncObligationsRequest,
    x_tenant_id: str = Header(default="default"),
):
    """Sync obligations into repository with version checks."""
    kernel = get_kernel()
    count = sync_obligations(kernel.store, x_tenant_id, body.obligations)
    return {"synced_count": count}


@router.get("/bindings")
async def list_bindings(
    x_tenant_id: str = Header(default="default"),
):
    """List bindings for tenant."""
    kernel = get_kernel()
    cur = kernel.store.conn.cursor()
    rows = cur.execute(
        "SELECT binding FROM reva_bindings WHERE tenant_id = ?",
        (x_tenant_id,),
    ).fetchall()
    items = [json.loads(r["binding"]) for r in rows]
    return {"items": items, "total": len(items)}


@router.post("/bindings/sync")
async def sync_bnd(
    body: SyncBindingsRequest,
    x_tenant_id: str = Header(default="default"),
):
    """Sync bindings into repository."""
    kernel = get_kernel()
    count = sync_bindings(kernel.store, x_tenant_id, body.bindings)
    return {"synced_count": count}


@router.post("/closure/evaluate")
async def evaluate_closure_endpoint(
    body: EvaluateClosureRequest,
    x_tenant_id: str = Header(default="default"),
):
    """Evaluate pure closure for obligations and build canonical ledger."""
    kernel = get_kernel()
    cur = kernel.store.conn.cursor()

    # Load obligations and bindings
    ob_rows = cur.execute(
        "SELECT definition FROM reva_obligations WHERE tenant_id = ?",
        (x_tenant_id,),
    ).fetchall()
    obligations = [Obligation.model_validate(json.loads(r["definition"])) for r in ob_rows]

    b_rows = cur.execute(
        "SELECT binding FROM reva_bindings WHERE tenant_id = ?",
        (x_tenant_id,),
    ).fetchall()
    bindings = {b.obligation_key: b for b in [Binding.model_validate(json.loads(r["binding"])) for r in b_rows]}

    decisions = []
    for ob in obligations:
        ctx = ClosureContext(
            obligation=ob,
            binding=bindings.get(ob.key),
            commit=body.commit,
        )
        dec = evaluate_closure(ctx)
        decisions.append(dec)

    ledger = build_ledger(
        tenant_id=x_tenant_id,
        scope=body.scope,
        commit=body.commit,
        decisions=decisions,
        store=kernel.store,
    )
    return ledger.canonical_dict()


@router.get("/ledger")
async def get_latest_ledger(
    scope: str = "all",
    x_tenant_id: str = Header(default="default"),
):
    """Get latest canonical Proof-of-Done ledger."""
    kernel = get_kernel()
    cur = kernel.store.conn.cursor()
    row = cur.execute(
        "SELECT record FROM reva_ledgers WHERE tenant_id = ? AND scope = ? ORDER BY created_at DESC LIMIT 1",
        (x_tenant_id, scope),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"No ledger found for scope '{scope}'")
    return json.loads(row["record"])


@router.get("/ledger/export")
async def export_ledger(
    scope: str = "all",
    format: Literal["json", "md", "html"] = "json",
    x_tenant_id: str = Header(default="default"),
):
    """Export canonical ledger in JSON, Markdown, or self-contained HTML."""
    kernel = get_kernel()
    cur = kernel.store.conn.cursor()
    row = cur.execute(
        "SELECT record FROM reva_ledgers WHERE tenant_id = ? AND scope = ? ORDER BY created_at DESC LIMIT 1",
        (x_tenant_id, scope),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"No ledger found for scope '{scope}'")

    raw_data = json.loads(row["record"])
    closures_data = raw_data.get("closures", [])
    # Reconstruct LedgerRecord
    from reva.pd.closure import ClosureDecision
    decisions = [
        ClosureDecision(
            closure_id=c.get("closure_id", ""),
            obligation_key=c.get("obligation_key", ""),
            obligation_version=c.get("obligation_version", 1),
            commit=c.get("commit", ""),
            outcome=c.get("outcome", "open"),
            reasons=c.get("reasons", []),
            checks=[],
            inputs={},
        )
        for c in closures_data
    ]
    ledger = LedgerRecord(
        ledger_id=raw_data.get("ledger_id", ""),
        tenant_id=x_tenant_id,
        scope=scope,
        commit=raw_data.get("commit", ""),
        complete=raw_data.get("complete", False),
        summary=raw_data.get("summary", {}),
        closures=decisions,
        created_at=raw_data.get("created_at", ""),
    )

    if format == "json":
        return Response(content=json.dumps(raw_data, indent=2), media_type="application/json")
    elif format == "md":
        return Response(content=ledger.to_markdown(), media_type="text/markdown")
    elif format == "html":
        return Response(content=render_ledger_html(ledger), media_type="text/html")
