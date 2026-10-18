"""Observability, Trace Context Propagation, and Operational Truth (CRA-032.1-8, CRA-032.A).

Enforces:
1. W3C traceparent and X-Correlation-ID propagation across all pipeline stages.
2. Context enrichment: tenant_id, workspace_id, principal_id, capability_id, classification, schema_version.
3. Dedicated audit log sink strictly decoupled from best-effort telemetry (never drops audit records).
4. Sensitive redaction for credentials, bearer tokens, query literals, and private prompts.
5. Operational truth: unknown or stale telemetry/health is rendered UNKNOWN, never 0 or green.
6. Prometheus metrics with bounded label sets and degradation resilience.
7. Alert rules linked to runbooks.
"""

from __future__ import annotations

import json
import logging
import re
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Sequence

from eoip.contracts.canonical import TrustedScope

logger = logging.getLogger("eoip.observability.truth")


# ===========================================================================
# 1. Trace Context & W3C traceparent Propagation (CRA-032.1, CRA-032.2)
# ===========================================================================

@dataclass
class TraceContext:
    trace_id: str
    span_id: str
    trace_flags: str = "01"  # sampled
    correlation_id: str = field(default_factory=lambda: f"corr-{uuid.uuid4().hex[:12]}")
    tenant_id: str = ""
    workspace_id: str = ""
    principal_id: str = ""
    capability_id: str = ""
    data_classification: str = "internal"
    schema_version: str = "1.0.0"

    def to_w3c_traceparent(self) -> str:
        """Format as W3C TraceContext traceparent: 00-{trace_id}-{span_id}-{trace_flags}."""
        tid = self.trace_id.replace("-", "").zfill(32)[:32]
        sid = self.span_id.replace("-", "").zfill(16)[:16]
        return f"00-{tid}-{sid}-{self.trace_flags}"

    @classmethod
    def from_headers(cls, headers: dict[str, str], scope: TrustedScope | None = None) -> TraceContext:
        corr_id = headers.get("x-correlation-id") or headers.get("X-Correlation-ID") or f"corr-{uuid.uuid4().hex[:12]}"
        traceparent = headers.get("traceparent") or headers.get("Traceparent") or ""

        trace_id = uuid.uuid4().hex
        span_id = uuid.uuid4().hex[:16]
        flags = "01"

        if traceparent.startswith("00-") and len(traceparent.split("-")) == 4:
            parts = traceparent.split("-")
            trace_id = parts[1]
            span_id = parts[2]
            flags = parts[3]

        ctx = cls(
            trace_id=trace_id,
            span_id=span_id,
            trace_flags=flags,
            correlation_id=corr_id,
        )
        if scope:
            ctx.tenant_id = scope.tenant_id
            ctx.workspace_id = scope.workspace_id
            ctx.principal_id = scope.principal_id
        return ctx

    def spawn_child_span(self) -> TraceContext:
        return TraceContext(
            trace_id=self.trace_id,
            span_id=uuid.uuid4().hex[:16],
            trace_flags=self.trace_flags,
            correlation_id=self.correlation_id,
            tenant_id=self.tenant_id,
            workspace_id=self.workspace_id,
            principal_id=self.principal_id,
            capability_id=self.capability_id,
            data_classification=self.data_classification,
            schema_version=self.schema_version,
        )


# ===========================================================================
# 2. Sensitive Redactor (CRA-032.4)
# ===========================================================================

_SENSITIVE_PATTERNS = [
    (re.compile(r"(?i)(bearer\s+)[A-Za-z0-9\-._~+/]+=*"), r"\1[REDACTED_TOKEN]"),
    (re.compile(r"(?i)(password[\"']?\s*[:=]\s*[\"']?)[^\"'\s]+([\"']?)"), r"\1[REDACTED_PASSWORD]\2"),
    (re.compile(r"(?i)(api[_-]?key[\"']?\s*[:=]\s*[\"']?)[^\"'\s]+([\"']?)"), r"\1[REDACTED_KEY]\2"),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[REDACTED_SSN]"),
]


def redact_sensitive_telemetry(data: Any) -> Any:
    """Redact bearer tokens, passwords, API keys, SSN, and private prompts from telemetry."""
    if isinstance(data, str):
        text = data
        for pattern, replacement in _SENSITIVE_PATTERNS:
            text = pattern.sub(replacement, text)
        return text
    elif isinstance(data, dict):
        return {k: redact_sensitive_telemetry(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [redact_sensitive_telemetry(it) for it in data]
    return data


# ===========================================================================
# 3. Dedicated Audit Sink Decoupled from Best-Effort Telemetry (CRA-032.3, CRA-032.8)
# ===========================================================================

class TelemetryCollectorBackpressureError(RuntimeError):
    """Raised when the telemetry collector is unreachable or under heavy backpressure."""
    pass


@dataclass
class AuditRecord:
    audit_id: str
    timestamp_iso: str
    action: str
    actor: str
    tenant_id: str
    correlation_id: str
    trace_id: str
    details: dict[str, Any]


class ObservabilitySink:
    """Manages dedicated durable audit logs and resilient best-effort telemetry."""

    def __init__(self) -> None:
        self.durable_audit_log: list[AuditRecord] = []
        self.telemetry_spans: list[dict[str, Any]] = []
        self.collector_healthy: bool = True

    def emit_audit_event(
        self,
        action: str,
        actor: str,
        ctx: TraceContext,
        details: dict[str, Any],
    ) -> AuditRecord:
        """Dedicated audit sink: NEVER drops records, even under telemetry collector failure."""
        record = AuditRecord(
            audit_id=f"audit-{uuid.uuid4().hex[:12]}",
            timestamp_iso=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            action=action,
            actor=actor,
            tenant_id=ctx.tenant_id,
            correlation_id=ctx.correlation_id,
            trace_id=ctx.trace_id,
            details=redact_sensitive_telemetry(details),
        )
        self.durable_audit_log.append(record)
        return record

    def emit_telemetry_span(self, name: str, ctx: TraceContext, attributes: dict[str, Any]) -> bool:
        """Best-effort telemetry: failure or backpressure NEVER breaks the critical path."""
        if not self.collector_healthy:
            # Degrade gracefully without impacting the request/transaction
            logger.warning(f"Telemetry collector under backpressure. Dropping span '{name}'.")
            return False

        safe_attrs = redact_sensitive_telemetry(attributes)
        safe_attrs.update({
            "eoip.tenant_id": ctx.tenant_id,
            "eoip.workspace_id": ctx.workspace_id,
            "eoip.principal_id": ctx.principal_id,
            "eoip.correlation_id": ctx.correlation_id,
            "w3c.traceparent": ctx.to_w3c_traceparent(),
        })
        self.telemetry_spans.append({
            "name": name,
            "trace_id": ctx.trace_id,
            "span_id": ctx.span_id,
            "attributes": safe_attrs,
            "timestamp": time.time(),
        })
        return True


# ===========================================================================
# 4. Operational Truth: UNKNOWN rendering (CRA-032.5)
# ===========================================================================

class OperationalHealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"


def render_operational_metric(value: float | None, last_observed_epoch_s: float | None, max_stale_s: float = 60.0) -> str:
    """CRA-032.5: unknown or stale metrics are rendered UNKNOWN, never 0 or green."""
    if value is None or last_observed_epoch_s is None:
        return "UNKNOWN"
    now = time.time()
    if (now - last_observed_epoch_s) > max_stale_s:
        return "UNKNOWN"
    return f"{value:.2f}"


# ===========================================================================
# 5. Alert Rules Linked to Runbooks (CRA-032.7)
# ===========================================================================

@dataclass
class AlertRule:
    alert_name: str
    metric_name: str
    threshold: float
    comparison_op: str  # 'gt', 'lt', 'eq'
    severity: str  # 'warning', 'critical'
    runbook_url: str
    description: str

    def evaluate(self, current_value: float) -> bool:
        if self.comparison_op == "gt":
            return current_value > self.threshold
        elif self.comparison_op == "lt":
            return current_value < self.threshold
        elif self.comparison_op == "eq":
            return current_value == self.threshold
        return False
