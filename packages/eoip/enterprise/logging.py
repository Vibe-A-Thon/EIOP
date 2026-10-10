"""Enterprise structured logging with correlation IDs and operational context.

Provides a consistent logging facade for all enterprise modules with
JSON-structured output, correlation tracking, and performance instrumentation.
"""

from __future__ import annotations

import functools
import logging
import time
import uuid
from contextvars import ContextVar
from typing import Any

_correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")
_tenant_id: ContextVar[str] = ContextVar("tenant_id", default="")

ENTERPRISE_LOGGER_NAME = "eoip.enterprise"


def get_correlation_id() -> str:
    return _correlation_id.get() or ""


def set_correlation_id(cid: str) -> None:
    _correlation_id.set(cid)


def set_tenant_id(tid: str) -> None:
    _tenant_id.set(tid)


class EnterpriseLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = _correlation_id.get()  # type: ignore[attr-defined]
        record.tenant_id = _tenant_id.get()  # type: ignore[attr-defined]
        return True


def get_logger(module_name: str) -> logging.Logger:
    """Get a child logger under the enterprise namespace."""
    name = f"{ENTERPRISE_LOGGER_NAME}.{module_name}"
    logger = logging.getLogger(name)
    if not logger.filters:
        logger.addFilter(EnterpriseLogFilter())
    return logger


def log_operation(logger: logging.Logger, operation: str, **extra: Any):
    """Context manager-style decorator that logs operation start/end with timing."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            op_id = uuid.uuid4().hex[:8]
            logger.info("op.start operation=%s op_id=%s %s",
                        operation, op_id,
                        " ".join(f"{k}={v}" for k, v in extra.items()))
            t0 = time.monotonic()
            try:
                result = fn(*args, **kwargs)
                elapsed_ms = (time.monotonic() - t0) * 1000
                logger.info("op.end operation=%s op_id=%s duration_ms=%.1f status=ok",
                            operation, op_id, elapsed_ms)
                return result
            except Exception as exc:
                elapsed_ms = (time.monotonic() - t0) * 1000
                logger.error("op.end operation=%s op_id=%s duration_ms=%.1f status=error error=%s",
                             operation, op_id, elapsed_ms, type(exc).__name__)
                raise
        return wrapper
    return decorator
