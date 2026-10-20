"""Ontology drift detection and evolution-proposal review (G2-OEVO-001..006)."""

from _principals import provision_api_token
from eoip.graph.memory import MemoryGraphStore

from apps.api import main

TOKEN = "test-token-with-at-least-24-characters"


def client(monkeypatch, tmp_path):
    store = MemoryGraphStore()
    monkeypatch.setenv("EOIP_API_TOKEN", TOKEN)
    provision_api_token(monkeypatch, TOKEN)
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path))
    monkeypatch.setattr(main, "create_store", lambda: store)
    from fastapi.testclient import TestClient

    return TestClient(main.create_app()), store


def _headers():
    return {"Authorization": f"Bearer {TOKEN}"}


def test_drift_report_is_clean_for_manifest_conformant_graph(monkeypatch, tmp_path):
    api, store = client(monkeypatch, tmp_path)
    store.upsert_vertex(
        "WorkItem", {"canonical_id": "w:1", "issue_key": "EOIP-1", "summary": "Ok"}
    )
    response = api.get("/api/v1/ontology/drift", headers=_headers())
    assert response.status_code == 200
    assert response.json() == {"has_drift": False, "findings": []}


def test_drift_detects_unmapped_vocabulary(monkeypatch, tmp_path):
    api, store = client(monkeypatch, tmp_path)
    store.upsert_vertex(
        "WorkItem", {"canonical_id": "w:1", "issue_key": "EOIP-1", "summary": "Ok"}
    )
    # Simulate a connector writing vocabulary the manifest does not declare.
    store._vertices["v:drift"] = {
        "vid": "v:drift",
        "canonical_id": "urn:custom:widget:1",
        "label": "CustomWidget",
        "properties": {"canonical_id": "urn:custom:widget:1", "custom_field": "x"},
    }
    response = api.get("/api/v1/ontology/drift", headers=_headers())
    assert response.status_code == 200
    body = response.json()
    assert body["has_drift"] is True
    kinds = {(finding["kind"], finding["value"]) for finding in body["findings"]}
    assert ("vertex_label", "CustomWidget") in kinds
    assert ("property_key", "custom_field") in kinds


def test_drift_proposals_enter_review_and_require_human_decision(monkeypatch, tmp_path):
    api, store = client(monkeypatch, tmp_path)
    store._vertices["v:drift"] = {
        "vid": "v:drift",
        "canonical_id": "urn:custom:widget:1",
        "label": "CustomWidget",
        "properties": {"canonical_id": "urn:custom:widget:1"},
    }

    generated = api.post("/api/v1/ontology/proposals", headers=_headers())
    assert generated.status_code == 201
    body = generated.json()
    assert body["created"] == 1
    proposal = body["proposals"][0]
    assert proposal["operation"] == "ONTOLOGY_VERTEX_LABEL"
    assert proposal["status"] == "PENDING"
    assert proposal["patch"]["occurrences"] == 1

    # Regenerating must not duplicate a pending proposal for the same finding.
    again = api.post("/api/v1/ontology/proposals", headers=_headers())
    assert again.json()["created"] == 0

    listed = api.get("/api/v1/agents/proposals?status=PENDING", headers=_headers())
    assert len(listed.json()["proposals"]) == 1

    # Human approval changes state only; nothing is auto-applied.
    decided = api.post(
        f"/api/v1/agents/proposals/{proposal['proposal_id']}/approve",
        headers=_headers(),
        json={"actor_id": "reviewer@example.invalid"},
    )
    assert decided.status_code == 200
    assert decided.json()["status"] == "APPROVED"
    drift = api.get("/api/v1/ontology/drift", headers=_headers()).json()
    assert ("vertex_label", "CustomWidget") in {
        (finding["kind"], finding["value"]) for finding in drift["findings"]
    }

    # A second decision is refused.
    repeat = api.post(
        f"/api/v1/agents/proposals/{proposal['proposal_id']}/reject",
        headers=_headers(),
        json={"actor_id": "reviewer@example.invalid"},
    )
    assert repeat.status_code == 409
