"""Paging, token and byte budgets, and continuation tokens (T-302 / REVA-VW-001..004)."""

from __future__ import annotations

import base64
import hmac
import hashlib
import json
import math
from typing import Any, Dict, List, Optional, Protocol, Tuple

from reva.core.errors import ContinuationInvalidError
from reva.core.jcs import canonicalize
from reva.core.time import format_ts, parse_ts, utc_now_ms


class ViewableResult(Protocol):
    """Protocol for query results rendering under resource budgets."""

    def summary(self) -> Dict[str, Any]:
        ...

    def facets(self) -> List[str]:
        ...

    def facet(self, name: str) -> Dict[str, Any]:
        ...

    def collections(self) -> List[str]:
        ...

    def page(self, collection: str, offset: int, limit: int) -> Tuple[List[Any], int]:
        ...

    def item(self, collection: str, key: str) -> Optional[Any]:
        ...


def estimate_tokens(payload_bytes: bytes) -> int:
    """Estimate token count: ceil(len(utf-8) / 4)."""
    return math.ceil(len(payload_bytes) / 4)


def create_continuation_token(
    hmac_key: bytes,
    tenant_id: str,
    principal_id: str,
    parent_id: str,
    view: str,
    collection: str,
    offset: int,
    limit: int = 50,
    expires_in_s: int = 3600,
) -> str:
    """Generate signed, tamper-evident continuation token."""
    now = utc_now_ms()
    exp_dt = now.timestamp() + expires_in_s
    payload = {
        "collection": collection,
        "exp": int(exp_dt),
        "limit": limit,
        "offset": offset,
        "parent_id": parent_id,
        "principal_id": principal_id,
        "tenant_id": tenant_id,
        "view": view,
    }
    payload_bytes = canonicalize(payload)
    sig = hmac.new(hmac_key, payload_bytes, hashlib.sha256).digest()

    p_b64 = base64.urlsafe_b64encode(payload_bytes).decode("ascii").rstrip("=")
    s_b64 = base64.urlsafe_b64encode(sig).decode("ascii").rstrip("=")
    return f"{p_b64}.{s_b64}"


def verify_continuation_token(
    hmac_key: bytes,
    token: str,
    expected_tenant: str,
    expected_principal: str,
) -> Dict[str, Any]:
    """Verify continuation token signature, principal/tenant binding, and expiry."""
    parts = token.split(".")
    if len(parts) != 2:
        raise ContinuationInvalidError("Malformed continuation token format")

    p_b64, s_b64 = parts
    # Pad base64
    p_pad = p_b64 + "=" * (-len(p_b64) % 4)
    s_pad = s_b64 + "=" * (-len(s_b64) % 4)

    try:
        payload_bytes = base64.urlsafe_b64decode(p_pad)
        claimed_sig = base64.urlsafe_b64decode(s_pad)
    except Exception as e:
        raise ContinuationInvalidError(f"Malformed base64 in continuation token: {e}") from e

    expected_sig = hmac.new(hmac_key, payload_bytes, hashlib.sha256).digest()
    if not hmac.compare_digest(claimed_sig, expected_sig):
        raise ContinuationInvalidError("Invalid continuation token signature")

    try:
        payload = json.loads(payload_bytes.decode("utf-8"))
    except Exception as e:
        raise ContinuationInvalidError(f"Invalid JSON payload in token: {e}") from e

    if payload.get("tenant_id") != expected_tenant:
        raise ContinuationInvalidError("Continuation token tenant mismatch")
    if payload.get("principal_id") != expected_principal:
        raise ContinuationInvalidError("Continuation token principal mismatch")

    now_ts = utc_now_ms().timestamp()
    if payload.get("exp", 0) < now_ts:
        raise ContinuationInvalidError("Continuation token has expired")

    return payload


def render_view(
    result: ViewableResult,
    parent_id: str,
    tenant_id: str,
    principal_id: str,
    hmac_key: bytes,
    byte_budget: int = 65536,
    token_budget: int = 16384,
) -> Dict[str, Any]:
    """Render result within byte and token budget, returning continuations when exceeded."""
    full_collections: Dict[str, Any] = {}
    total_items = 0

    for col in result.collections():
        items, count = result.page(col, offset=0, limit=1000)
        full_collections[col] = items
        total_items += count

    candidate = {
        "collections": full_collections,
        "facets": {f: result.facet(f) for f in result.facets()},
        "parent_id": parent_id,
        "summary": result.summary(),
    }

    cand_bytes = canonicalize(candidate)
    cand_tokens = estimate_tokens(cand_bytes)

    # If within both budgets, return full result
    if len(cand_bytes) <= byte_budget and cand_tokens <= token_budget:
        return candidate

    # Exceeded budget: return summary + ready-to-call continuation tokens
    continuations: List[Dict[str, Any]] = []
    for col in result.collections():
        _, count = result.page(col, offset=0, limit=1)
        if count > 0:
            token = create_continuation_token(
                hmac_key=hmac_key,
                tenant_id=tenant_id,
                principal_id=principal_id,
                parent_id=parent_id,
                view="collection",
                collection=col,
                offset=0,
                limit=50,
            )
            continuations.append({
                "collection": col,
                "continuation_token": token,
                "endpoint": f"/api/reva/v1/views/{parent_id}?token={token}",
                "total_items": count,
            })

    return {
        "continuations": continuations,
        "facets": {f: result.facet(f) for f in result.facets()},
        "parent_id": parent_id,
        "summary": result.summary(),
        "truncated": True,
    }
