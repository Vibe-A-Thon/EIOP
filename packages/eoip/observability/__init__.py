"""Structured logging helpers shared by the API and worker."""

import json
import logging as stdlib_logging
from datetime import UTC, datetime

from eoip.contracts.audit import AuditEvent


class JsonLogFormatter(stdlib_logging.Formatter):
    _fields = (
        "event",
        "correlation_id",
        "audit_id",
        "event_type",
        "actor",
        "outcome",
        "reason_code",
        "safe_summary",
        "operation",
        "job_id",
        "method",
        "path",
        "status_code",
        "duration_seconds",
        "attempt",
        "error_type",
    )

    def format(self, record: stdlib_logging.LogRecord) -> str:
        payload = {
            "timestamp": getattr(
                record,
                "timestamp",
                datetime.fromtimestamp(record.created, UTC).isoformat(timespec="milliseconds"),
            ),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for field in self._fields:
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def configure_json_logging() -> None:
    logger = stdlib_logging.getLogger("eoip")
    logger.setLevel(stdlib_logging.INFO)
    if any(isinstance(handler.formatter, JsonLogFormatter) for handler in logger.handlers):
        return
    handler = stdlib_logging.StreamHandler()
    handler.setFormatter(JsonLogFormatter())
    logger.addHandler(handler)
    logger.propagate = False


def log_audit_event(logger: stdlib_logging.Logger, event: AuditEvent, **fields) -> None:
    logger.info(
        "audit.event",
        extra={
            "event": "audit.event",
            **event.model_dump(exclude_none=True),
            **fields,
        },
    )
