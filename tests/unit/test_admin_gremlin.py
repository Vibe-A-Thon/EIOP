"""Tests for the admin Gremlin endpoint (FR-QUERY-008)."""

import os

import pytest
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

from apps.api import main

_TOKEN = "test-token-with-at-least-24-characters"


@pytest.fixture
def client(monkeypatch, tmp_path):
    store = MemoryGraphStore()
    store.close = lambda: None
    monkeypatch.setenv("EOIP_API_TOKEN", _TOKEN)
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path))
    monkeypatch.setattr(main, "create_store", lambda: store)
    return TestClient(main.create_app())


def test_gremlin_disabled_by_default(client):
    response = client.post(
        "/api/v1/admin/gremlin",
        json={"gremlin": "g.V().count()"},
        headers={"Authorization": f"Bearer {_TOKEN}"},
    )
    assert response.status_code == 403
    assert "disabled by policy" in response.json()["detail"]


def test_gremlin_enabled_but_memory_store_unsupported(client, monkeypatch):
    monkeypatch.setenv("EOIP_ADMIN_GREMLIN_ENABLED", "true")
    response = client.post(
        "/api/v1/admin/gremlin",
        json={"gremlin": "g.V().count()"},
        headers={"Authorization": f"Bearer {_TOKEN}"},
    )
    assert response.status_code == 501
    assert "does not support" in response.json()["detail"]


def test_gremlin_empty_query(client, monkeypatch):
    monkeypatch.setenv("EOIP_ADMIN_GREMLIN_ENABLED", "true")
    response = client.post(
        "/api/v1/admin/gremlin",
        json={"gremlin": ""},
        headers={"Authorization": f"Bearer {_TOKEN}"},
    )
    assert response.status_code == 422


def test_gremlin_requires_auth(client):
    response = client.post(
        "/api/v1/admin/gremlin",
        json={"gremlin": "g.V().count()"},
    )
    assert response.status_code == 401
