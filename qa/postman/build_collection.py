"""Build a deterministic, read-only Postman v2.1 collection."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

ROOT = Path(__file__).resolve().parents[2]
COLLECTION_PATH = ROOT / "qa" / "postman" / "EOIP-readonly-QA.postman_collection.json"
ENVIRONMENT_PATH = ROOT / "qa" / "postman" / "local.postman_environment.json"

REQUESTS = [
    ("Public", "Readiness", "/health/ready", 200, False),
    ("Public", "OpenAPI", "/openapi.json", 200, False),
    ("Public", "Metrics", "/metrics", 200, False),
    ("Authentication", "Whoami without token", "/api/v1/auth/whoami", 401, False),
    ("Authentication", "Whoami with invalid token", "/api/v1/auth/whoami", 401, "invalid"),
    ("Authentication", "Whoami with Basic auth", "/api/v1/auth/whoami", 401, "basic"),
    ("Authentication", "Whoami with valid token", "/api/v1/auth/whoami", 200, True),
    ("Administration", "Stats without token", "/api/v1/admin/stats", 401, False),
    ("Administration", "System without token", "/api/v1/admin/system", 401, False),
    ("Administration", "Stats with valid token", "/api/v1/admin/stats", 200, True),
    ("Administration", "System with valid token", "/api/v1/admin/system", 200, True),
    ("Graph", "Backends without token", "/api/v1/graph/backends", 401, False),
    ("Graph", "Backends with valid token", "/api/v1/graph/backends", 200, True),
    ("Query", "Templates with valid token", "/api/v1/query/templates", 200, True),
    ("Reporting", "Templates with valid token", "/api/v1/reports/templates", 200, True),
    ("Product", "Capabilities with valid token", "/api/v1/product/capabilities", 200, True),
    ("Routing", "Unknown path with valid token", "/api/v1/qa-nonexistent-route", 404, True),
]


def request_item(name: str, path: str, expected: int, auth: bool | str) -> dict:
    headers = [{"key": "Accept", "value": "application/json"}]
    if auth is True:
        headers.append({"key": "Authorization", "value": "Bearer {{qaToken}}"})
    elif auth == "invalid":
        headers.append({"key": "Authorization", "value": "Bearer invalid-qa-token"})
    elif auth == "basic":
        headers.append({"key": "Authorization", "value": "Basic Zm9vOmJhcg=="})
    script = [
        f"pm.test('HTTP {expected}', function () {{ pm.response.to.have.status({expected}); }});",
        "pm.test('Response is bounded', function () { pm.expect(pm.response.text().length).to.be.below(1000000); });",
        "pm.test('Access token is not echoed', function () { const token = pm.variables.get('qaToken'); if (token) pm.expect(pm.response.text()).not.to.include(token); });",
    ]
    if expected == 200:
        script.append("pm.test('Correlation header is present', function () { pm.expect(pm.response.headers.has('X-Correlation-ID')).to.equal(true); });")
    if path != "/metrics":
        script.append("pm.test('JSON media type', function () { pm.expect(pm.response.headers.get('Content-Type') || '').to.include('application/json'); });")
    if auth is True:
        script.insert(0, "pm.test('QA token was configured', function () { pm.expect(pm.variables.get('qaToken')).to.be.a('string').and.not.empty; });")
    return {
        "name": name,
        "request": {
            "method": "GET",
            "header": headers,
            "url": {"raw": "{{baseUrl}}" + path, "host": ["{{baseUrl}}"], "path": path.lstrip("/").split("/")},
            "description": "Read-only non-functional probe. No business-data assertion or mutation.",
        },
        "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": script}}],
    }


def collection() -> dict:
    groups: dict[str, list[dict]] = {}
    for group, name, path, expected, auth in REQUESTS:
        groups.setdefault(group, []).append(request_item(name, path, expected, auth))
    guard = [
        "const base = pm.variables.get('baseUrl') || '';",
        "const local = /^http:\\/\\/(127\\.0\\.0\\.1|localhost)(:\\d+)?\\/?$/.test(base);",
        "if (!local && pm.variables.get('qaAllowRemote') !== 'true') { throw new Error('Remote QA target requires explicit qaAllowRemote=true'); }",
    ]
    return {
        "info": {
            "_postman_id": str(uuid5(NAMESPACE_URL, "eoip-readonly-qa-v1")),
            "name": "EOIP Read-only Non-functional QA",
            "description": "Safe GET-only probes for readiness, API metadata and authorization. Use only against an isolated QA environment. A passing run is not functional or production acceptance.",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "event": [{"listen": "prerequest", "script": {"type": "text/javascript", "exec": guard}}],
        "item": [{"name": name, "item": items} for name, items in groups.items()],
        "variable": [
            {"key": "baseUrl", "value": "http://127.0.0.1:8000", "type": "string"},
            {"key": "qaToken", "value": "", "type": "string"},
            {"key": "qaAllowRemote", "value": "false", "type": "string"},
        ],
    }


def environment() -> dict:
    return {
        "id": str(uuid5(NAMESPACE_URL, "eoip-readonly-qa-environment-v1")),
        "name": "EOIP local QA template",
        "values": [
            {"key": "baseUrl", "value": "http://127.0.0.1:8000", "enabled": True},
            {"key": "qaToken", "value": "", "enabled": True, "type": "secret"},
            {"key": "qaAllowRemote", "value": "false", "enabled": True},
        ],
        "_postman_variable_scope": "environment",
        "_postman_exported_using": "EOIP QA bench",
    }


def main() -> None:
    COLLECTION_PATH.write_text(json.dumps(collection(), indent=2) + "\n", encoding="utf-8")
    ENVIRONMENT_PATH.write_text(json.dumps(environment(), indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {COLLECTION_PATH.relative_to(ROOT)} and {ENVIRONMENT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
