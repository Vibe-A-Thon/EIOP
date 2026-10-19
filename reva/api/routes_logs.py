"""REST router for Merkle transparency logs and STH proofs (T-303 / REVA-IF-030..031)."""

from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, Header, HTTPException, Query

from reva.api.routes_warrants import get_kernel
from reva.core.errors import RevaNotFoundError

router = APIRouter(prefix="/logs", tags=["Transparency Log"])


@router.get("/{log_id}/sth")
async def get_sth(log_id: str, x_tenant_id: str = Header(default="default")):
    """Get latest Signed Tree Head (STH) for transparency log."""
    kernel = get_kernel()
    size = kernel.translog.size(log_id)
    root = kernel.translog.root(log_id, size)
    return {
        "issued_at": "2026-10-18T00:00:00.000Z",
        "log_id": log_id,
        "root_hash": root.hex(),
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
    kernel = get_kernel()
    proof = kernel.translog.inclusion_proof(log_id, leaf_index, tree_size)
    return {
        "leaf_index": leaf_index,
        "log_id": log_id,
        "proof": [p.hex() for p in proof],
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
    kernel = get_kernel()
    proof = kernel.translog.consistency_proof(log_id, first_size, second_size)
    return {
        "first_size": first_size,
        "log_id": log_id,
        "proof": [p.hex() for p in proof],
        "second_size": second_size,
    }
