"""Contract tests for ontology validate and SHACL routes (CRA-020.9, CRA-020.10, CRA-020.A)."""

from __future__ import annotations
from _principals import provision_api_token
import json
import os
import pytest
from fastapi.testclient import TestClient

from eoip.graph.memory import MemoryGraphStore
from eoip.ontology.rdf import export_shacl_shapes, validate_shacl
from apps.api import main as api_main


def _make_client(tmp_path, monkeypatch):
    # monkeypatch restores env and create_store, so later tests do not inherit them.
    monkeypatch.setenv("EOIP_API_TOKEN", "test-token-minimum-24-characters!!")
    provision_api_token(monkeypatch, "test-token-minimum-24-characters!!")
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("EOIP_GRAPH_BACKEND", "memory")
    store = MemoryGraphStore()
    monkeypatch.setattr(api_main, "create_store", lambda: store)
    app = api_main.create_app()
    return TestClient(app), store


def test_ontology_validate_contract_unchanged(tmp_path, monkeypatch):
    """CRA-020.9: Keep existing /ontology/validate contract unchanged."""
    client, store = _make_client(tmp_path, monkeypatch)
    store.upsert_vertex("Service", {"canonical_id": "srv-1", "name": "PaymentService", "service_id": "srv-1"})
    headers = {"Authorization": "Bearer test-token-minimum-24-characters!!"}

    response = client.get("/api/v1/ontology/validate?limit=10", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "conforms" in data
    assert "checked" in data
    assert "results" in data
    assert data["conforms"] is True


def test_export_shacl_shapes_contract():
    """CRA-020.8: export_shacl_shapes contains W3C constraints and extension profile."""
    doc = export_shacl_shapes()
    assert "@context" in doc
    assert "@graph" in doc

    # Check that extension profile is present
    ext_entry = next((item for item in doc["@graph"] if item["@id"] == "urn:eoip:profile:extension"), None)
    assert ext_entry is not None
    assert "eoip:relationshipExtensions" in ext_entry


def test_post_ontology_validate_shacl_endpoint(tmp_path, monkeypatch):
    """CRA-020.9 & CRA-020.10: POST /ontology/validate/shacl semantics."""
    client, store = _make_client(tmp_path, monkeypatch)
    headers = {"Authorization": "Bearer test-token-minimum-24-characters!!"}

    # 1. Valid payload -> 200 OK
    valid_payload = {
        "data": [
            {"label": "Service", "canonical_id": "srv-10", "properties": {"name": "AuthService"}}
        ]
    }
    resp_valid = client.post("/api/v1/ontology/validate/shacl", json=valid_payload, headers=headers)
    assert resp_valid.status_code == 200
    assert resp_valid.json()["conforms"] is True

    # 2. Violation payload -> 422 with report
    invalid_payload = {
        "data": [
            {"label": "Service", "canonical_id": "srv-broken", "properties": {"name": ""}}
        ]
    }
    resp_invalid = client.post("/api/v1/ontology/validate/shacl", json=invalid_payload, headers=headers)
    assert resp_invalid.status_code == 422
    assert resp_invalid.json()["detail"] == "SHACL_VIOLATION"
    assert "report" in resp_invalid.json()
    assert resp_invalid.json()["report"]["conforms"] is False

    # 3. Unsupported constraint -> 422 UNSUPPORTED_CONSTRAINT
    unsupported_payload = {
        "shapes": [
            {
                "shape_id": "UnsupportedSPARQLShape",
                "target_class": "Service",
                "unsupported_components": ["sh:SPARQLConstraintComponent"],
            }
        ],
        "data": [{"label": "Service", "canonical_id": "srv-1"}]
    }
    resp_unsupported = client.post("/api/v1/ontology/validate/shacl", json=unsupported_payload, headers=headers)
    assert resp_unsupported.status_code == 422
    assert resp_unsupported.json()["detail"] == "UNSUPPORTED_CONSTRAINT"

    # 4. Validator unavailable -> 503
    resp_down = client.post(
        "/api/v1/ontology/validate/shacl",
        json={"mock_validator_down": True},
        headers=headers
    )
    assert resp_down.status_code == 503


def test_async_semantic_validations_endpoint(tmp_path, monkeypatch):
    """CRA-020.9: POST /api/v1/semantic/validations requires Idempotency-Key."""
    client, _ = _make_client(tmp_path, monkeypatch)
    headers = {"Authorization": "Bearer test-token-minimum-24-characters!!"}

    # Missing Idempotency-Key -> 400 Bad Request
    resp_no_key = client.post("/api/v1/semantic/validations", json={"data": []}, headers=headers)
    assert resp_no_key.status_code == 400
    assert "Idempotency-Key" in resp_no_key.json()["detail"]

    # With Idempotency-Key -> 202 Accepted
    headers_with_key = {**headers, "Idempotency-Key": "idemp-key-12345"}
    resp_ok = client.post("/api/v1/semantic/validations", json={"data": []}, headers=headers_with_key)
    assert resp_ok.status_code == 202
    data = resp_ok.json()
    assert data["status"] == "PENDING"
    assert data["idempotency_key"] == "idemp-key-12345"
    assert "job_id" in data
