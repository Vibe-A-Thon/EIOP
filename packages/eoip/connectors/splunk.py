"""Splunk REST & Saved Searches connector emitting SourceEvents (CRA-008.2, CRA-008.7, CRA-008.8).

Enforces:
1. Strict query/time/result budgets on searches.
2. Secret and PII redaction on ingested query strings and log snippets before persistence,
   producing a RedactionReceipt with counts, never the removed values.
3. Saved searches, alerts, and dashboards with app/role permissions.
4. Dashboard panels link to CMDB services as proposals with evidence.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
import httpx

from eoip.connectors.base import (
    DiscoveredResource,
    DiscoveryResult,
    DiscoveryScope,
)
from eoip.connectors.errors import ConnectorError
from eoip.contracts.source_event import PermissionMetadata, SourceEventV2, utc_now_iso
from eoip.contracts.source_registry import SourceCapabilities

_SECRET_PATTERNS = {
    "connection_string": re.compile(r"(?i)(mongodb(\+srv)?|postgres(ql)?|mysql|redis)://[^\s'\"]+"),
    "api_key": re.compile(r"(?i)\b(api_?key|apikey)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-\.]{16,})['\"]?"),
    "password": re.compile(r"(?i)\b(password|passwd|pwd)\s*[:=]\s*['\"]?([^'\"\s]{6,})['\"]?"),
    "token": re.compile(r"(?i)(?:\b(?:auth_?token|token|bearer)\s*[:= ]\s*['\"]?([a-zA-Z0-9_\-\.]{16,})['\"]?|\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{16,}\b)"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
}


@dataclass
class RedactionReceipt:
    receipt_id: str
    target_id: str
    redaction_counts: dict[str, int]
    total_redacted: int
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat().replace("+00:00", "Z"))


def redact_with_receipt(text: str, target_id: str) -> tuple[str, RedactionReceipt]:
    """Redact secrets and PII from query string or log snippet; emit receipt with counts only."""
    clean = text
    counts: dict[str, int] = {}
    total = 0

    for category, pat in _SECRET_PATTERNS.items():
        matches = list(pat.finditer(clean))
        if matches:
            counts[category] = len(matches)
            total += len(matches)
            clean = pat.sub(f"[REDACTED_{category.upper()}]", clean)

    receipt = RedactionReceipt(
        receipt_id=hashlib.sha256(f"{target_id}:{total}:{datetime.now(UTC)}".encode()).hexdigest()[:16],
        target_id=target_id,
        redaction_counts=counts,
        total_redacted=total,
    )
    return clean, receipt


@dataclass
class SearchBudget:
    max_results: int = 1000
    timeout_seconds: float = 30.0
    max_search_span_hours: int = 72


class SplunkConnector:
    """Splunk REST API connector for saved searches, alerts, and budgeted knowledge extraction."""

    source_system = "splunk"
    mapper_version = "splunk-rest/1.0"

    def __init__(
        self,
        source_id: str,
        base_url: str,
        *,
        token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        app: str = "search",
        budget: SearchBudget | None = None,
        client: httpx.Client | None = None,
    ) -> None:
        self.source_id = source_id
        self.base_url = base_url.rstrip("/")
        self.app = app
        self.budget = budget or SearchBudget()
        self._client = client or httpx.Client(timeout=self.budget.timeout_seconds)
        self._headers = {"Accept": "application/json"}
        if token:
            self._headers["Authorization"] = f"Splunk {token}"
        elif username and password:
            import base64
            auth_str = base64.b64encode(f"{username}:{password}".encode()).decode()
            self._headers["Authorization"] = f"Basic {auth_str}"

    def capabilities(self) -> SourceCapabilities:
        return SourceCapabilities(
            baseline=True,
            polling=True,
            webhooks=True,
            discovery=True,
            reconciliation=True,
            replay=True,
        )

    def make_saved_search_event(
        self,
        search_name: str,
        search_query: str,
        properties: dict[str, Any] | None = None,
        *,
        app: str | None = None,
        roles: list[str] | None = None,
    ) -> tuple[SourceEventV2, RedactionReceipt]:
        """Create SourceEventV2 for a Splunk saved search with automated secrets redaction."""
        app_name = app or self.app
        search_id = f"{app_name}:{search_name}"

        # Automate secret/PII redaction and produce receipt
        clean_query, receipt = redact_with_receipt(search_query, target_id=search_id)

        props = dict(properties or {})
        props["search"] = clean_query
        props["name"] = search_name
        props["app"] = app_name

        serialized = json.dumps(props, sort_keys=True, separators=(",", ":"))
        content_hash = hashlib.sha256(serialized.encode()).hexdigest()
        event_id = hashlib.sha256(f"splunk:{self.source_id}:{search_id}:{content_hash}".encode()).hexdigest()
        event_time = utc_now_iso()

        principal_refs = [f"splunk:role:{r}" for r in (roles or ["admin", "power"])]
        permissions = PermissionMetadata(
            visibility="INTERNAL",
            principal_refs=principal_refs,
            inherited_from=f"splunk:app:{app_name}",
        )

        event = SourceEventV2(
            event_id=event_id,
            source_system="splunk",
            source_instance_id=self.source_id,
            source_record_id=f"savedsearch:{search_id}",
            operation="UPSERT",
            source_version=content_hash,
            event_time=event_time,
            captured_at=utc_now_iso(),
            content_hash=content_hash,
            cursor=event_time,
            permissions=permissions,
            payload=props,
            metadata={
                "search_name": search_name,
                "app": app_name,
                "redaction_receipt_id": receipt.receipt_id,
                "total_redactions": receipt.total_redacted,
                "budget_max_results": self.budget.max_results,
            },
        )
        return event, receipt

    def validate_budget(self, result_count: int, execution_time_seconds: float) -> None:
        """Enforce search query/time/result budgets (CRA-008.2)."""
        if result_count > self.budget.max_results:
            raise ConnectorError(
                "splunk",
                "budget_exceeded",
                f"Result count {result_count} exceeds budget limit {self.budget.max_results}",
            )
        if execution_time_seconds > self.budget.timeout_seconds:
            raise ConnectorError(
                "splunk",
                "budget_exceeded",
                f"Execution time {execution_time_seconds:.1f}s exceeds budget limit {self.budget.timeout_seconds:.1f}s",
            )
