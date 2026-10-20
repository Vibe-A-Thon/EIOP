"""REST router for Merkle transparency logs and STH proofs (T-303 / REVA-IF-030..031)."""

from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, Query

from reva.api.routes_warrants import get_kernel
from reva.core.time import format_ts, utc_now_ms
from reva.kernel.signing import b64url_encode

router = APIRouter(prefix="/logs", tags=["Transparency Log"])


def _log_for(log_id: str):
    """Return the kernel's transparency log when log_id names it; 404 otherwise."""
    kernel = get_kernel()
    log = kernel.translog
    if log.log_id != log_id:
        raise HTTPException(status_code=404, detail=f"Transparency log '{log_id}' not found")
    return kernel, log


@router.get("/{log_id}/sth")
async def get_sth(log_id: str, x_tenant_id: str = Header(default="default")):
    """Latest Signed Tree Head for the log, or the unsigned current head when none is stored yet."""
    kernel, log = _log_for(log_id)
    row = kernel.store.conn.execute(
        "SELECT * FROM reva_sths WHERE log_id = ? ORDER BY tree_size DESC LIMIT 1", (log_id,)
    ).fetchone()
    size = log.size()
    if row is not None:
        root_hash = row["root_hash"]
        signature = row["signature"]
        return {
            "issued_at": row["issued_at"],
            "key_id": row["key_id"],
            "log_id": log_id,
            "root_hash": root_hash.hex() if isinstance(root_hash, bytes) else root_hash,
            "signature": b64url_encode(signature) if isinstance(signature, bytes) else signature,
            "signed": True,
            "tree_size": row["tree_size"],
        }
    return {
        "issued_at": format_ts(utc_now_ms()),
        "log_id": log_id,
        "root_hash": log.root(size).hex(),
        "signed": False,
        "tree_size": size,
    }


@router.get("/{log_id}/inclusion")
async def get_inclusion_proof(
    log_id: str,
    leaf_index: int = Query(..., ge=0),
    tree_size: int = Query(..., gt=0),
    x_tenant_id: str = Header(default="default"),
):
    """Serve RFC 6962 inclusion proof for leaf at leaf_index against tree_size."""
    _, log = _log_for(log_id)
    if tree_size > log.size() or leaf_index >= tree_size:
        raise HTTPException(status_code=400, detail="leaf_index/tree_size out of range")
    return {
        "leaf_index": leaf_index,
        "log_id": log_id,
        "proof": log.inclusion_proof(leaf_index, tree_size),
        "tree_size": tree_size,
    }


@router.get("/{log_id}/consistency")
async def get_consistency_proof(
    log_id: str,
    first_size: int = Query(..., ge=0),
    second_size: int = Query(..., gt=0),
    x_tenant_id: str = Header(default="default"),
):
    """Serve RFC 6962 / RFC 9162 consistency proof between two log tree sizes."""
    _, log = _log_for(log_id)
    if second_size > log.size() or first_size > second_size:
        raise HTTPException(status_code=400, detail="first_size/second_size out of range")
    return {
        "first_size": first_size,
        "log_id": log_id,
        "proof": log.consistency_proof(first_size, second_size),
        "second_size": second_size,
    }
