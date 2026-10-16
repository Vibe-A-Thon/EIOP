"""Tests for audit sink and secret redaction."""

import tempfile

from eoip.audit.redaction import redact_secrets
from eoip.audit.sink import AuditSink
from eoip.contracts.audit import AuditEvent


def test_audit_sink_persists_events():
    with tempfile.TemporaryDirectory() as tmpdir:
        sink = AuditSink(tmpdir)
        event = AuditEvent(
            audit_id="aud-1",
            event_type="query",
            actor="test-user",
            correlation_id="corr-1",
            outcome="success",
            safe_summary="Test query completed",
        )
        sink.emit(event, operation="query")
        records = sink.read()
        assert len(records) == 1
        assert records[0]["audit_id"] == "aud-1"
        assert records[0]["operation"] == "query"


def test_audit_sink_redacts_secrets():
    with tempfile.TemporaryDirectory() as tmpdir:
        sink = AuditSink(tmpdir)
        event = AuditEvent(
            audit_id="aud-2",
            event_type="auth",
            actor="admin",
            correlation_id="corr-2",
            outcome="success",
        )
        sink.emit(event, token="secret-value")
        records = sink.read()
        assert records[0].get("token") is None or "secret-value" not in str(records[0])


def test_redaction_preserves_safe_fields():
    record = {"actor": "user", "outcome": "success", "password": "p@ssw0rd"}
    result = redact_secrets(record)
    assert result["actor"] == "user"
    assert result["outcome"] == "success"
    assert result["password"] == "***REDACTED***"
