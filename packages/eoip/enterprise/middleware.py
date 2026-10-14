"""Enterprise API middleware for structured error handling, timing, and correlation.

Provides a global exception handler that translates EnterpriseError subclasses
into consistent JSON responses, injects correlation IDs, and records request
latency metrics.
"""

from __future__ import annotations

import time
import uuid
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from eoip.enterprise.exceptions import EnterpriseError, ErrorSeverity
from eoip.enterprise.logging import get_logger, set_correlation_id, set_tenant_id
from eoip.tenancy.context import TenantContextRequired, authorized_tenant

logger = get_logger("middleware")


def build_error_response(error: EnterpriseError,
                         correlation_id: str = "") -> JSONResponse:
    """Build a structured JSON error response from an EnterpriseError."""
    body: dict[str, Any] = {
        "error": {
            "code": error.error_code,
            "message": error.message,
            "category": error.category.value,
            "severity": error.severity.value,
        },
    }
    if correlation_id:
        body["correlation_id"] = correlation_id

    return JSONResponse(status_code=error.http_status, content=body)


def install_enterprise_middleware(app: FastAPI) -> None:
    """Install all enterprise middleware on a FastAPI application."""

    @app.exception_handler(EnterpriseError)
    async def enterprise_error_handler(request: Request,
                                       exc: EnterpriseError) -> JSONResponse:
        cid = getattr(request.state, "correlation_id", "")
        if exc.severity in (ErrorSeverity.HIGH, ErrorSeverity.CRITICAL):
            logger.error("enterprise_error code=%s msg=%s correlation_id=%s",
                         exc.error_code, exc.message, cid)
        else:
            logger.warning("enterprise_error code=%s msg=%s correlation_id=%s",
                           exc.error_code, exc.message, cid)
        return build_error_response(exc, correlation_id=cid)

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request,
                                  exc: ValueError) -> JSONResponse:
        return JSONResponse(status_code=422, content={
            "error": {
                "code": "EOIP-VAL-001",
                "message": str(exc),
                "category": "VALIDATION",
                "severity": "LOW",
            }
        })

    @app.middleware("http")
    async def enterprise_request_middleware(request: Request,
                                           call_next) -> Response:
        supplied = request.headers.get("X-Correlation-ID", "")
        correlation_id = supplied if 0 < len(supplied) <= 128 else uuid.uuid4().hex
        request.state.correlation_id = correlation_id
        set_correlation_id(correlation_id)

        import os

        supplied_tenant = request.headers.get("X-Tenant-ID") or request.headers.get("X-Tenant-Id")
        principal = getattr(request.state, "principal", None)
        if principal:
            try:
                tenant_id = authorized_tenant(principal, supplied_tenant) or ""
            except TenantContextRequired as exc:
                return JSONResponse(
                    status_code=403,
                    content={
                        "error": {
                            "code": "EOIP-AUTHZ-003",
                            "message": str(exc),
                            "category": "AUTHORIZATION",
                            "severity": "HIGH",
                        },
                        "correlation_id": correlation_id,
                    },
                )
        elif supplied_tenant:
            tenant_id = supplied_tenant
        else:
            env = os.getenv("EOIP_ENV", os.getenv("APP_ENV", "")).lower()
            if env == "production":
                tenant_id = ""
            else:
                tenant_id = getattr(request.state, "tenant_id", "default") or "default"

        request.state.tenant_id = tenant_id
        set_tenant_id(tenant_id)

        t0 = time.monotonic()
        response = await call_next(request)
        elapsed_ms = (time.monotonic() - t0) * 1000

        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Response-Time-Ms"] = f"{elapsed_ms:.1f}"
        response.headers["X-Powered-By"] = "EOIP Enterprise"

        logger.info(
            "request method=%s path=%s status=%d duration_ms=%.1f correlation_id=%s tenant=%s",
            request.method, request.url.path, response.status_code,
            elapsed_ms, correlation_id, tenant_id,
        )
        return response
