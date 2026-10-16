"""Structured JSON Log Aggregation Engine (INFRA-004).

Produces Loki/ELK-compatible structured JSON logs with correlation IDs,
module-level log control, and sampling for high-frequency events.
"""

from __future__ import annotations

import contextvars
import io
import json
import logging
import random
import sys
import threading
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

# Context variables for distributed request tracing
_CORRELATION_ID = contextvars.ContextVar("correlation_id", default="")
_REQUEST_ID = contextvars.ContextVar("request_id", default="")
_TRACE_ID = contextvars.ContextVar("trace_id", default="")
_ACTOR_ID = contextvars.ContextVar("actor_id", default="")


def set_trace_context(
    correlation_id: str = "",
    request_id: str = "",
    trace_id: str = "",
    actor_id: str = "",
) -> None:
    if correlation_id:
        _CORRELATION_ID.set(correlation_id)
    if request_id:
        _REQUEST_ID.set(request_id)
    if trace_id:
        _TRACE_ID.set(trace_id)
    if actor_id:
        _ACTOR_ID.set(actor_id)


def get_trace_context() -> dict[str, str]:
    return {
        "correlation_id": _CORRELATION_ID.get(),
        "request_id": _REQUEST_ID.get(),
        "trace_id": _TRACE_ID.get(),
        "actor_id": _ACTOR_ID.get(),
    }


class LogFormat(str, Enum):
    JSON = "JSON"
    LOKI = "LOKI"


class StructuredLogFormatter(logging.Formatter):
    """Formats log records as one-line JSON documents with correlation context."""

    def __init__(self, service_name: str = "eoip-platform", log_format: LogFormat = LogFormat.JSON) -> None:
        super().__init__()
        self.service_name = service_name
        self.log_format = log_format

    def format(self, record: logging.LogRecord) -> str:
        ctx = get_trace_context()
        log_payload = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(record.created)),
            "level": record.levelname,
            "service": self.service_name,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": ctx["correlation_id"] or getattr(record, "correlation_id", ""),
            "request_id": ctx["request_id"] or getattr(record, "request_id", ""),
            "trace_id": ctx["trace_id"] or getattr(record, "trace_id", ""),
            "actor_id": ctx["actor_id"] or getattr(record, "actor_id", ""),
            "module": record.module,
            "line": record.lineno,
        }

        # Include extra dictionary properties
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            log_payload.update(record.extra)

        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)

        if self.log_format == LogFormat.LOKI:
            # Format compatible with Grafana Loki JSON ingestion
            return json.dumps({
                "streams": [
                    {
                        "stream": {"level": record.levelname, "service": self.service_name},
                        "values": [[str(int(record.created * 1e9)), json.dumps(log_payload)]],
                    }
                ]
            })

        return json.dumps(log_payload)


class SamplingFilter(logging.Filter):
    """Probabilistically samples high-volume debug/info logs."""

    def __init__(self, sample_rate: float = 1.0) -> None:
        super().__init__()
        self.sample_rate = sample_rate

    def filter(self, record: logging.LogRecord) -> bool:
        # Never sample WARNING, ERROR, CRITICAL
        if record.levelno >= logging.WARNING:
            return True
        if self.sample_rate >= 1.0:
            return True
        return random.random() < self.sample_rate


class StructuredLogger:
    """Manages structured log configuration and module levels."""

    _instance: StructuredLogger | None = None

    def __init__(self, default_level: int = logging.INFO) -> None:
        self.default_level = default_level
        self.module_levels: dict[str, int] = {}
        self.formatter = StructuredLogFormatter()
        self._lock = threading.Lock()

    @classmethod
    def get_instance(cls) -> StructuredLogger:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def set_module_level(self, module_name: str, level: int | str) -> None:
        lvl = getattr(logging, level.upper()) if isinstance(level, str) else level
        with self._lock:
            self.module_levels[module_name] = lvl
            logging.getLogger(module_name).setLevel(lvl)

    def format_log(self, level: str, message: str, logger_name: str = "eoip", extra: dict[str, Any] | None = None) -> str:
        record = logging.LogRecord(
            name=logger_name,
            level=getattr(logging, level.upper(), logging.INFO),
            pathname="",
            lineno=0,
            msg=message,
            args=(),
            exc_info=None,
        )
        if extra:
            record.extra = extra
        return self.formatter.format(record)


def get_structured_logger() -> StructuredLogger:
    return StructuredLogger.get_instance()
