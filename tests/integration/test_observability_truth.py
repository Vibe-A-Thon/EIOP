"""Acceptance test suite: Observability and Operational Truth (WP-032, CRA-032.1-8, CRA-032.A)."""
from __future__ import annotations

import time
import pytest

from eoip.contracts.canonical import PrincipalType, TrustedScope
from eoip.observability.truth import (
    AlertRule,
    ObservabilitySink,
    OperationalHealthStatus,
    TraceContext,
    redact_sensitive_telemetry,
    render_operational_metric,
)
from eoip.observability.metrics import Counter


@pytest.fixture
def scope():
    return TrustedScope(
        tenant_id="tenant_eng",
        workspace_id="ws_1",
        principal_id="engineer_bob",
        principal_type=PrincipalType.USER,
        roles=["developer"],
    )


# ===========================================================================
# CRA-032.1 & CRA-032.2: Context propagation and trace enrichment
# ===========================================================================

def test_cra_032_1_and_2_context_propagation_and_enrichment(scope):
    headers = {
        "x-correlation-id": "corr-test-9999",
        "traceparent": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
    }
    ctx = TraceContext.from_headers(headers, scope=scope)
    assert ctx.correlation_id == "corr-test-9999"
    assert ctx.trace_id == "4bf92f3577b34da6a3ce929d0e0e4736"
    assert ctx.tenant_id == "tenant_eng"
    assert ctx.principal_id == "engineer_bob"

    # W3C traceparent formatting
    tp = ctx.to_w3c_traceparent()
    assert tp.startswith("00-4bf92f3577b34da6a3ce929d0e0e4736-")
    assert tp.endswith("-01")

    # Child span propagation inherits trace_id and correlation_id but gets new span_id
    child = ctx.spawn_child_span()
    assert child.trace_id == ctx.trace_id
    assert child.correlation_id == ctx.correlation_id
    assert child.span_id != ctx.span_id
    assert child.tenant_id == "tenant_eng"


# ===========================================================================
# CRA-032.3 & CRA-032.8: Decoupled audit sink and collector resilience
# ===========================================================================

def test_cra_032_3_and_8_decoupled_audit_and_resilience(scope):
    sink = ObservabilitySink()
    ctx = TraceContext.from_headers({}, scope=scope)

    # Normal state: both audit and telemetry emitted
    rec1 = sink.emit_audit_event("user.login", "bob", ctx, {"ip": "127.0.0.1"})
    assert len(sink.durable_audit_log) == 1
    assert rec1.action == "user.login"

    tel_ok = sink.emit_telemetry_span("http_request", ctx, {"endpoint": "/search"})
    assert tel_ok is True
    assert len(sink.telemetry_spans) == 1

    # Collector fails (simulating network outage / backpressure)
    sink.collector_healthy = False

    # Telemetry gracefully degrades (returns False, never raises exception in critical path)
    tel_failed = sink.emit_telemetry_span("http_request_2", ctx, {"endpoint": "/query"})
    assert tel_failed is False
    assert len(sink.telemetry_spans) == 1  # No span appended

    # Audit log is STILL safely written (NEVER dropped)
    rec2 = sink.emit_audit_event("entity.mutate", "bob", ctx, {"entity_id": "svc_1"})
    assert len(sink.durable_audit_log) == 2
    assert rec2.action == "entity.mutate"


# ===========================================================================
# CRA-032.4: Sensitive telemetry redaction
# ===========================================================================

@pytest.mark.req("CRA-032")
def test_cra_032_4_sensitive_telemetry_redaction():
    raw_payload = {
        "auth_header": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.secret",
        "user_query": "SELECT * FROM users WHERE ssn = '123-45-6789' and password='superSecretPassword123'",
        "api_key": "api_key='abc123xyz'",
        "safe_label": "service_metrics",
    }
    redacted = redact_sensitive_telemetry(raw_payload)

    assert "secret" not in redacted["auth_header"]
    assert "[REDACTED_TOKEN]" in redacted["auth_header"]
    assert "123-45-6789" not in redacted["user_query"]
    assert "[REDACTED_SSN]" in redacted["user_query"]
    assert "superSecretPassword123" not in redacted["user_query"]
    assert "[REDACTED_PASSWORD]" in redacted["user_query"]
    assert "[REDACTED_KEY]" in redacted["api_key"]
    assert redacted["safe_label"] == "service_metrics"


# ===========================================================================
# CRA-032.5: Operational truth: UNKNOWN rendering
# ===========================================================================

@pytest.mark.req("CRA-032")
def test_cra_032_5_operational_truth_unknown():
    now = time.time()

    # Fresh metric renders exact float
    rendered_fresh = render_operational_metric(99.4, last_observed_epoch_s=now - 5.0, max_stale_s=30.0)
    assert rendered_fresh == "99.40"

    # Stale metric renders UNKNOWN (never 0 or green)
    rendered_stale = render_operational_metric(99.4, last_observed_epoch_s=now - 120.0, max_stale_s=30.0)
    assert rendered_stale == "UNKNOWN"

    # Unobserved metric renders UNKNOWN
    rendered_none = render_operational_metric(None, last_observed_epoch_s=None)
    assert rendered_none == "UNKNOWN"


# ===========================================================================
# CRA-032.6: Prometheus metrics suite with bounded labels
# ===========================================================================

@pytest.mark.req("CRA-032")
def test_cra_032_6_prometheus_metrics_suite():
    counter = Counter("eoip_http_requests_total", "Total incoming HTTP requests", label_names=("method", "status"))
    counter.inc(1.0, method="GET", status="200")
    counter.inc(2.0, method="POST", status="201")

    rendered = counter.render()
    assert "# TYPE eoip_http_requests_total counter" in rendered
    assert 'method="GET",status="200"' in rendered
    assert counter.get(method="GET", status="200") == 1.0


# ===========================================================================
# CRA-032.7: Alert rules linked to runbooks
# ===========================================================================

@pytest.mark.req("CRA-032")
def test_cra_032_7_alert_rules_linked_to_runbooks():
    rule = AlertRule(
        alert_name="GraphIngestionLagHigh",
        metric_name="ingestion_lag_seconds",
        threshold=300.0,
        comparison_op="gt",
        severity="critical",
        runbook_url="https://wiki.enterprise.internal/runbooks/ingestion-lag",
        description="Ingestion event stream lag exceeds 5 minutes",
    )
    # Under threshold -> No alert
    assert rule.evaluate(120.0) is False

    # Over threshold -> Alert fires
    assert rule.evaluate(350.0) is True
    assert rule.runbook_url == "https://wiki.enterprise.internal/runbooks/ingestion-lag"


# ===========================================================================
# CRA-032.A: Acceptance Gate
# ===========================================================================

@pytest.mark.req("CRA-032")
def test_cra_032_a_acceptance_gate(scope):
    sink = ObservabilitySink()
    ctx = TraceContext.from_headers(
        {"x-correlation-id": "corr-gate-32"},
        scope=scope,
    )

    # 1. Trace context enriched and formatted
    tp = ctx.to_w3c_traceparent()
    assert tp.startswith("00-")

    # 2. Audit record created with redactor
    audit = sink.emit_audit_event("query.execute", "bob", ctx, {"secret_token": "Bearer xyz123"})
    assert "[REDACTED_TOKEN]" in str(audit.details)

    # 3. Collector outage does not raise error
    sink.collector_healthy = False
    assert sink.emit_telemetry_span("test", ctx, {}) is False
    assert len(sink.durable_audit_log) == 1

    # 4. Stale metric renders UNKNOWN
    assert render_operational_metric(5.0, time.time() - 500.0, max_stale_s=10.0) == "UNKNOWN"
