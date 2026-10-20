"""Ambient tenant scope for agent tool calls and plugin invocations (SR-TEN-001).

Dependency-free so low-level runtimes (tool registry, plugin runtime) can use it. The value is never
blank: unauthenticated platform work runs under ``_platform`` (same label as API logs/metrics).
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar

PLATFORM_SCOPE = "_platform"
_CURRENT_TENANT: ContextVar[str] = ContextVar("eoip_current_tenant", default=PLATFORM_SCOPE)


def current_tenant() -> str:
    """Tenant the current agent tool call or plugin invocation runs for."""
    return _CURRENT_TENANT.get()


@contextmanager
def tenant_scope(tenant_id: str) -> Iterator[str]:
    if not isinstance(tenant_id, str) or not tenant_id.strip():
        raise ValueError("tenant scope must be a non-blank tenant id (SR-TEN-001)")
    token = _CURRENT_TENANT.set(tenant_id)
    try:
        yield tenant_id
    finally:
        _CURRENT_TENANT.reset(token)
