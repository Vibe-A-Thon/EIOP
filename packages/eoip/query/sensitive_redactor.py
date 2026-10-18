"""Scoped templates, history, results, and sensitive literal redaction (CRA-024.5).

Ensures sensitive literals (passwords, api keys, tokens, secrets) are redacted in query logs,
history, and explain outputs. Enforces strict tenant scoping for query templates and cache.
Prevents unauthorized cross-tenant leakage or export of intermediate facts.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


def redact_sensitive_literals(text: str) -> str:
    """Replaces sensitive literals and credentials with [REDACTED]."""
    redacted = re.sub(
        r"(?i)\b(password|passwd|secret|api_key|token|auth)\s*([:=])\s*['\"]?[^'\"]+['\"]?",
        r"\1\2 [REDACTED]",
        text,
    )
    redacted = re.sub(r"(?i)Bearer\s+[a-zA-Z0-9_\-\.]+", "Bearer [REDACTED]", redacted)
    redacted = re.sub(r"\b[A-Za-z0-9+/]{40,}\b", "[REDACTED]", redacted)
    redacted = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED]", redacted)
    redacted = re.sub(r"\b(?:\d{4}-){3}\d{4}\b", "[REDACTED]", redacted)
    return redacted


@dataclass
class ScopedQueryRecord:
    record_id: str
    tenant_id: str
    principal_id: str
    query_text_redacted: str
    dialect: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    execution_time_ms: float = 0.0
    status: str = "COMPLETED"


class ScopedQueryManager:
    """Manages tenant-isolated query templates, history, and result caching."""

    def __init__(self) -> None:
        self._templates: dict[str, dict[str, str]] = {}       # tenant_id -> {template_id: text}
        self._history: dict[str, list[ScopedQueryRecord]] = {} # tenant_id -> list[ScopedQueryRecord]
        self._cache: dict[str, dict[str, Any]] = {}            # tenant_id -> {query_hash: result}

    def save_template(self, tenant_id: str, template_name: str, query_text: str) -> None:
        clean_text = redact_sensitive_literals(query_text)
        self._templates.setdefault(tenant_id, {})[template_name] = clean_text

    def get_template(self, tenant_id: str, template_name: str) -> Optional[str]:
        return self._templates.get(tenant_id, {}).get(template_name)

    def record_history(
        self,
        tenant_id: str,
        principal_id: str,
        query_text: str,
        dialect: str,
        execution_time_ms: float,
        status: str = "COMPLETED",
    ) -> ScopedQueryRecord:
        clean_text = redact_sensitive_literals(query_text)
        rec_id = hashlib.sha256(f"{tenant_id}:{query_text}:{datetime.now(timezone.utc)}".encode("utf-8")).hexdigest()[:16]
        rec = ScopedQueryRecord(
            record_id=rec_id,
            tenant_id=tenant_id,
            principal_id=principal_id,
            query_text_redacted=clean_text,
            dialect=dialect,
            execution_time_ms=execution_time_ms,
            status=status,
        )
        self._history.setdefault(tenant_id, []).append(rec)
        return rec

    def get_history(self, tenant_id: str) -> list[ScopedQueryRecord]:
        return list(self._history.get(tenant_id, []))

    def cache_result(self, tenant_id: str, query_text: str, result: dict[str, Any]) -> None:
        h = hashlib.sha256(query_text.encode("utf-8")).hexdigest()
        # Sanitize result to strip internal/intermediate facts before caching
        safe_result = {k: v for k, v in result.items() if not k.startswith("_intermediate")}
        self._cache.setdefault(tenant_id, {})[h] = safe_result

    def get_cached_result(self, tenant_id: str, query_text: str) -> Optional[dict[str, Any]]:
        h = hashlib.sha256(query_text.encode("utf-8")).hexdigest()
        return self._cache.get(tenant_id, {}).get(h)

    def clear_cache(self, tenant_id: Optional[str] = None) -> None:
        if tenant_id:
            self._cache.pop(tenant_id, None)
        else:
            self._cache.clear()
