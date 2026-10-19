"""FastAPI exception handlers and middleware for REVA error responses (T-301 / §10.1)."""

from __future__ import annotations

import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from reva.core.errors import RevaError

CATEGORY_TO_STATUS = {
    "invalid_input": 400,
    "not_found": 404,
    "conflict": 409,
    "unauthorized": 401,
    "forbidden": 403,
    "integrity": 409,
    "resource_limit": 413,
    "unavailable": 503,
    "timeout": 504,
    "cancelled": 499,
    "internal": 500,
}


async def reva_exception_handler(request: Request, exc: RevaError) -> JSONResponse:
    """Serialize RevaError into canonical §10.1 JSON response."""
    status_code = CATEGORY_TO_STATUS.get(exc.category, 500)
    correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    payload = exc.to_dict(correlation_id=correlation_id)

    response = JSONResponse(status_code=status_code, content=payload)
    response.headers["X-Correlation-ID"] = correlation_id
    return response


def register_reva_error_handlers(app: FastAPI) -> None:
    """Register REVA domain error handlers on FastAPI application."""
    app.add_exception_handler(RevaError, reva_exception_handler)
