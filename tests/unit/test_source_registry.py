from __future__ import annotations

import json

import pytest
from eoip.connectors.registry import SourceAlreadyExistsError, SourceNotFoundError, SourceRegistry
from eoip.contracts.source_registry import SourceRegistryEntry
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient
from pydantic import ValidationError


def _entry(**overrides) -> SourceRegistryEntry:
    values = {
        "source_id": "jira-prod",
        "source_type": "jira",
        "name": "Production Jira",
        "base_url": "https://jira.example.test",
        "secret_refs": {"token": "env://EOIP_JIRA_TOKEN"},
        "capabilities": {"polling": True, "webhooks": True, "deletion_events": True},
    }
    values.update(overrides)
    return SourceRegistryEntry(**values)


@pytest.mark.req("G2-T0004", "G2-T0101", "G2-T0102")
def test_registry_crud_is_durable_and_never_stores_inline_secrets(tmp_path) -> None:
    registry_path = tmp_path / "source-registry.json"
    registry = SourceRegistry(registry_path)
    created = registry.create(_entry())

    assert SourceRegistry(registry_path).get("jira-prod") == created
    updated = registry.update("jira-prod", {"enabled": False, "config": {"project": "EOIP"}})
    assert updated.enabled is False
    assert updated.created_at == created.created_at
    assert json.loads(registry_path.read_text(encoding="utf-8"))["sources"][0]["secret_refs"] == {
        "token": "env://EOIP_JIRA_TOKEN"
    }

    with pytest.raises(SourceAlreadyExistsError):
        registry.create(_entry())
    assert registry.delete("jira-prod").source_id == "jira-prod"
    with pytest.raises(SourceNotFoundError):
        registry.get("jira-prod")

    with pytest.raises(ValidationError):
        _entry(config={"api_token": "plain-text-secret"})
    with pytest.raises(ValidationError):
        _entry(secret_refs={"token": "plain-text-secret"})


@pytest.mark.req("G2-T0101")
def test_source_registry_api_crud_and_auth(monkeypatch, tmp_path) -> None:
    from apps.api import main as api_main

    monkeypatch.setattr(api_main, "api_token", lambda: "x" * 32)
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)
    client = TestClient(api_main.create_app())
    headers = {"Authorization": "Bearer " + "x" * 32}
    payload = _entry().model_dump(mode="json")

    assert client.get("/api/v1/sources").status_code == 401
    created = client.post("/api/v1/sources", json=payload, headers=headers)
    assert created.status_code == 201
    assert client.post("/api/v1/sources", json=payload, headers=headers).status_code == 409
    assert client.get("/api/v1/sources", headers=headers).json()[0]["source_id"] == "jira-prod"

    updated = client.patch(
        "/api/v1/sources/jira-prod", json={"enabled": False}, headers=headers
    )
    assert updated.status_code == 200
    assert updated.json()["enabled"] is False
    assert client.delete("/api/v1/sources/jira-prod", headers=headers).status_code == 204
    assert client.get("/api/v1/sources/jira-prod", headers=headers).status_code == 404
