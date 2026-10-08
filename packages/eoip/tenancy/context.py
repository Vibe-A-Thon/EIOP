"""Tenant context propagation (SR-TEN-001).

Every API request, query, job, event, cache key, log line, metric label,
agent call and plugin invocation must carry a tenant context. Code paths
that cannot resolve a tenant context fail closed (raise
``TenantContextRequired``) rather than fall back to a default tenant
(SR-TEN-001).

Headers used by the HTTP boundary:

- ``X-Tenant-Id``   — tenant URN or short id (``urn:eoip:tenancy:tenant:<id>``).
- ``X-Principal``   — authenticated principal (user or service account).

Helper ``tenant_context_dependency`` is a FastAPI dependency that resolves
the context from the request and fails closed; the wiring step attaches it
globally or per-route (lazy fastapi import — no fastapi import at module
load).

Real enforcement that a request *carries* context through every internal
hop (jobs, events, cache keys, metrics labels) is ADR-gated: this module
provides the canonical context object and the fail-closed resolution rule.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

TENANT_HEADER = "X-Tenant-Id"
PRINCIPAL_HEADER = "X-Principal"


class TenantContextRequired(RuntimeError):
    """Fail-closed error raised when tenant context is missing (SR-TEN-001)."""


@dataclass(frozen=True)
class TenantContext:
    """Immutable tenant + principal identity for one request (SR-TEN-001)."""

    tenant_id: str
    principal: str

    @property
    def urn(self) -> str:
        if self.tenant_id.startswith("urn:"):
            return self.tenant_id
        return f"urn:eoip:tenancy:tenant:{self.tenant_id}"

    def cache_key(self, key: str) -> str:
        """Namespace a cache key under this tenant (SR-TEN-001/SR-TEN-003)."""
        if not self.tenant_id:
            raise TenantContextRequired("cache key requested without tenant")
        return f"ten:{self.tenant_id}:{key}"

    def log_fields(self) -> dict[str, str]:
        """Fields that must accompany every log line for this tenant (SR-TEN-001)."""
        return {"tenant_id": self.tenant_id, "principal": self.principal}


def resolve_context(
    tenant_id: str | None,
    principal: str | None,
) -> TenantContext:
    """Build a TenantContext or fail closed (SR-TEN-001).

    Both fields are mandatory; empty/None values raise
    ``TenantContextRequired`` — there is no implicit/default tenant.
    """
    if not tenant_id or not tenant_id.strip():
        raise TenantContextRequired(f"missing tenant header {TENANT_HEADER}")
    if not principal or not principal.strip():
        raise TenantContextRequired(f"missing principal header {PRINCIPAL_HEADER}")
    return TenantContext(tenant_id=tenant_id.strip(), principal=principal.strip())


def require_tenant(ctx: TenantContext | None) -> TenantContext:
    """Return the context or fail closed when absent (SR-TEN-001)."""
    if ctx is None or not ctx.tenant_id:
        raise TenantContextRequired("tenant context is required on this code path")
    return ctx


def tenant_context_dependency() -> Any:
    """FastAPI dependency resolving TenantContext from request headers.

    Fail-closed: missing ``X-Tenant-Id`` / ``X-Principal`` produce HTTP 403
    (not 401 — the caller may be authenticated but lacks a tenant binding).
    """
    from fastapi import HTTPException, Request

    def _resolve(request: Request) -> TenantContext:
        try:
            return resolve_context(
                request.headers.get(TENANT_HEADER),
                request.headers.get(PRINCIPAL_HEADER),
            )
        except TenantContextRequired as exc:
            raise HTTPException(status_code=403, detail=str(exc)) from exc

    return _resolve
