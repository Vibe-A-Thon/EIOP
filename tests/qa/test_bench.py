import json

import httpx
import pytest

from qa.bench import api_surface, exit_code, live_checks, validated_base_url, write_evidence
from qa.postman.build_collection import collection, environment
from qa.postman.build_workflow import collection as workflow_collection


@pytest.mark.parametrize("url", [
    "https://example.com", "http://192.0.2.1:8000", "http://user:pass@localhost:8000",
    "http://localhost:8000/api", "http://localhost:8000?x=1", "file:///etc/passwd",
])
def test_remote_or_ambiguous_targets_are_rejected(url):
    with pytest.raises(ValueError):
        validated_base_url(url)


def test_local_target_is_allowed():
    assert validated_base_url("http://127.0.0.1:8000/") == "http://127.0.0.1:8000"


def test_postman_collection_is_get_only_and_has_no_embedded_token():
    generated = collection()
    items = [item for group in generated["item"] for item in group["item"]]
    assert len(items) >= 8
    assert {item["request"]["method"] for item in items} == {"GET"}
    assert next(v["value"] for v in environment()["values"] if v["key"] == "qaToken") == ""


def test_mutating_collection_is_disposable_and_source_scoped():
    workflow = workflow_collection()
    items = workflow["item"]
    assert [item["request"]["method"] for item in items] == ["POST", "GET", "POST", "PATCH", "GET", "DELETE", "GET"]
    assert all(item["request"]["url"]["raw"].startswith("{{baseUrl}}/api/v1/sources") for item in items)
    assert next(v["value"] for v in workflow["variable"] if v["key"] == "qaDisposableTarget") == "false"
    assert "qaDisposableTarget" in " ".join(workflow["event"][0]["script"]["exec"])


def test_surface_sorting_ignores_non_operations():
    surface = api_surface({"openapi": "3.1.0", "paths": {"/z": {"post": {}, "parameters": []}, "/a": {"get": {}}}})
    assert surface["operations"] == [{"method": "GET", "path": "/a"}, {"method": "POST", "path": "/z"}]


def test_evidence_status_and_exit_codes(tmp_path):
    path = write_evidence("offline", [{"name": "dependency", "status": "blocked", "detail": "missing"}], {}, tmp_path)
    assert json.loads(path.read_text())["status"] == "blocked"
    assert exit_code([{"status": "blocked"}]) == 2
    assert exit_code([{"status": "fail"}]) == 1
    assert exit_code([{"status": "pass"}]) == 0


def test_live_probes_are_get_only_and_missing_token_blocks_authorized_checks(monkeypatch):
    seen = []

    def respond(request):
        seen.append(request)
        protected = request.url.path.startswith("/api/v1/")
        return httpx.Response(401 if protected else 200, json={"ok": True})

    transport = httpx.MockTransport(respond)
    original_client = httpx.Client
    monkeypatch.setattr("qa.bench.httpx.Client", lambda **kwargs: original_client(transport=transport, **kwargs))
    checks = live_checks("http://127.0.0.1:8000", None, 2.0)
    assert len(seen) == 9
    assert {request.method for request in seen} == {"GET"}
    assert [request.headers.get("authorization") for request in seen if "authorization" in request.headers] == ["Bearer invalid-qa-token", "Basic Zm9vOmJhcg=="]
    assert sum(item["status"] == "blocked" for item in checks) == 8
