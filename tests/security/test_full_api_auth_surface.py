"""Verify auth rejection for every registered API operation, without any credentials."""

import logging
import re

import httpx
import pytest

from apps.api.main import create_app
from _principals import provision_api_token

PUBLIC = {
    "/health/live", "/health/ready", "/metrics", "/api/reva/v1/health",
    "/ontology/docs", "/api/v1/ontology/docs",
    # Pre-authentication endpoints (apps/api/main.py middleware, route_policy.OPEN).
    "/api/v1/auth/login", "/api/v1/auth/health", "/api/v1/auth/providers",
    "/api/v1/auth/sso/{provider}/login",
}
METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}


@pytest.mark.asyncio
async def test_every_protected_api_operation_rejects_missing_and_invalid_bearer(monkeypatch, tmp_path, caplog):
    monkeypatch.setenv("EOIP_GRAPH_BACKEND", "memory")
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path))
    provision_api_token(monkeypatch, "api-auth-surface-test-token-with-at-least-24-chars")
    monkeypatch.setenv("REVA_ENABLED", "false")
    app = create_app()
    document = app.openapi()
    operations = sorted(
        (method.upper(), path)
        for path, routes in document["paths"].items()
        for method in routes
        if method in METHODS
    )
    assert len(operations) >= 700, "An unexpectedly small API inventory must be reviewed"
    failures = []
    checked = 0
    with caplog.at_level(logging.CRITICAL, logger="eoip.api"), caplog.at_level(logging.CRITICAL, logger="eoip.audit"):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://localhost", trust_env=False,
        ) as client:
            for method, path in operations:
                concrete = re.sub(r"\{[^{}]+\}", "qa-example", path)
                if path in PUBLIC or re.fullmatch(r"/api/v1/sources/[A-Za-z0-9][A-Za-z0-9._-]*/webhooks", concrete):
                    continue
                for authorization in (None, "Bearer invalid-qa-token"):
                    headers = {"Authorization": authorization} if authorization else {}
                    response = await client.request(method, concrete, headers=headers)
                    checked += 1
                    if response.status_code != 401:
                        failures.append((method, path, "missing" if authorization is None else "invalid", response.status_code))
    assert checked >= 1400
    assert not failures, f"Auth boundary failures: {failures[:25]} ({len(failures)} total)"
