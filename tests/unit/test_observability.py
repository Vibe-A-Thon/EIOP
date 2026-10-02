import json
import logging
from io import StringIO

from eoip.contracts.audit import AuditEvent
from eoip.observability import JsonLogFormatter, log_audit_event


def test_json_log_formatter_emits_correlation_and_operation_fields():
    record = logging.makeLogRecord(
        {
            "name": "eoip.api",
            "levelno": logging.INFO,
            "levelname": "INFO",
            "msg": "http.request.completed",
            "args": (),
            "created": 1_800_000_000.0,
            "event": "http.request.completed",
            "event_type": "query",
            "actor": "local-user",
            "outcome": "success",
            "safe_summary": "query operation completed with status 200",
            "correlation_id": "correlation-123",
            "audit_id": "audit-456",
            "operation": "query",
            "method": "GET",
            "path": "/api/v1/search",
            "status_code": 200,
            "duration_seconds": 0.012,
        }
    )

    payload = json.loads(JsonLogFormatter().format(record))

    assert payload["event"] == "http.request.completed"
    assert payload["event_type"] == "query"
    assert payload["actor"] == "local-user"
    assert payload["outcome"] == "success"
    assert payload["safe_summary"] == "query operation completed with status 200"
    assert payload["correlation_id"] == "correlation-123"
    assert payload["audit_id"] == "audit-456"
    assert payload["operation"] == "query"
    assert payload["status_code"] == 200
    assert "authorization" not in payload


def test_audit_events_are_emitted_as_structured_json():
    stream = StringIO()
    logger = logging.getLogger("eoip.test.audit")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonLogFormatter())
    logger.addHandler(handler)
    try:
        log_audit_event(
            logger,
            AuditEvent(
                audit_id="audit-123",
                event_type="backup",
                actor="local-operator",
                correlation_id="correlation-123",
                outcome="success",
                safe_summary="Graph backup created",
            ),
            operation="backup",
        )
    finally:
        logger.removeHandler(handler)

    payload = json.loads(stream.getvalue())
    assert payload["event"] == "audit.event"
    assert payload["audit_id"] == "audit-123"
    assert payload["event_type"] == "backup"
    assert payload["actor"] == "local-operator"
    assert payload["correlation_id"] == "correlation-123"
    assert payload["outcome"] == "success"
    assert payload["safe_summary"] == "Graph backup created"
