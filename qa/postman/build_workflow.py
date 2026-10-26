"""Build a guarded Postman source-registry CRUD workflow collection."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_PATH = ROOT / "qa" / "postman" / "EOIP-disposable-source-workflow.postman_collection.json"


def workflow_item(name: str, method: str, path: str, expected: int, body: dict | None = None, assertion: str | None = None) -> dict:
    script = [
        f"pm.test('HTTP {expected}', function () {{ pm.response.to.have.status({expected}); }});",
        "pm.test('Bounded response', function () { pm.expect(pm.response.text().length).to.be.below(1000000); });",
        "pm.test('Token not echoed', function () { pm.expect(pm.response.text()).not.to.include(pm.variables.get('qaToken')); });",
    ]
    if assertion:
        script.append(assertion)
    headers = [{"key": "Authorization", "value": "Bearer {{qaToken}}"}, {"key": "Accept", "value": "application/json"}]
    request = {
        "method": method,
        "header": headers,
        "url": {"raw": "{{baseUrl}}" + path, "host": ["{{baseUrl}}"], "path": path.lstrip("/").split("/")},
        "description": "Mutates only a unique qa-* source in the bench-owned disposable in-memory API.",
    }
    if body is not None:
        headers.append({"key": "Content-Type", "value": "application/json"})
        request["body"] = {"mode": "raw", "raw": json.dumps(body), "options": {"raw": {"language": "json"}}}
    return {"name": name, "request": request, "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": script}}]}


def collection() -> dict:
    source = {"source_id": "{{qaSourceId}}", "source_type": "local_files", "name": "QA disposable source"}
    items = [
        workflow_item("Create source", "POST", "/api/v1/sources", 201, source,
                      "pm.test('Created ID', function () { pm.expect(pm.response.json().source_id).to.equal(pm.collectionVariables.get('qaSourceId')); });"),
        workflow_item("Read source", "GET", "/api/v1/sources/{{qaSourceId}}", 200, assertion=
                      "pm.test('Read ID', function () { pm.expect(pm.response.json().source_id).to.equal(pm.collectionVariables.get('qaSourceId')); });"),
        workflow_item("Reject duplicate", "POST", "/api/v1/sources", 409, source),
        workflow_item("Rename source", "PATCH", "/api/v1/sources/{{qaSourceId}}", 200, {"name": "QA renamed source"},
                      "pm.test('Updated name', function () { pm.expect(pm.response.json().name).to.equal('QA renamed source'); });"),
        workflow_item("List source", "GET", "/api/v1/sources", 200, assertion=
                      "pm.test('Listed ID', function () { pm.expect(pm.response.json().some(item => item.source_id === pm.collectionVariables.get('qaSourceId'))).to.equal(true); });"),
        workflow_item("Delete source", "DELETE", "/api/v1/sources/{{qaSourceId}}", 204),
        workflow_item("Deleted source is absent", "GET", "/api/v1/sources/{{qaSourceId}}", 404),
    ]
    guard = [
        "const base = pm.variables.get('baseUrl') || '';",
        r"const local = /^http:\/\/(127\.0\.0\.1|localhost)(:\d+)?\/?$/.test(base);",
        "if (!local || pm.variables.get('qaDisposableTarget') !== 'true') throw new Error('Disposable workflow requires loopback and qaDisposableTarget=true');",
        "if (!pm.variables.get('qaToken')) throw new Error('QA token is required');",
        "if (!pm.collectionVariables.get('qaSourceId')) { const id = 'qa-' + pm.variables.replaceIn('{{$guid}}').replace(/-/g, '').slice(0, 20); pm.collectionVariables.set('qaSourceId', id); }",
    ]
    return {
        "info": {
            "_postman_id": str(uuid5(NAMESPACE_URL, "eoip-disposable-source-workflow-v1")),
            "name": "EOIP Disposable Source Workflow QA",
            "description": "Mutating functional QA. Execute only through python -m qa.bench workflow against its bench-owned disposable API.",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "event": [{"listen": "prerequest", "script": {"type": "text/javascript", "exec": guard}}],
        "item": items,
        "variable": [
            {"key": "baseUrl", "value": "http://127.0.0.1:8000", "type": "string"},
            {"key": "qaToken", "value": "", "type": "string"},
            {"key": "qaDisposableTarget", "value": "false", "type": "string"},
            {"key": "qaSourceId", "value": "", "type": "string"},
        ],
    }


def main() -> None:
    WORKFLOW_PATH.write_text(json.dumps(collection(), indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {WORKFLOW_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
