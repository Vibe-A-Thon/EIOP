"""Identity candidate review queue (GAP-ER-005/007/010, FR-ID-002)."""

from _principals import provision_api_token
import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.identity.candidates import IdentityCandidateStore, suggest_candidate

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


def test_candidate_requires_real_anchor():
    store = MemoryGraphStore()
    assert (
        suggest_candidate(
            store,
            existing_cid="urn:missing",
            incoming_source_system="gitlab",
            incoming_identity="murthy.r",
            match_basis="display_name",
            confidence=0.6,
        )
        is None
    )


def test_candidate_lifecycle_and_audit_preservation(tmp_path):
    store = MemoryGraphStore()
    store.upsert_vertex(
        "Person", {"canonical_id": "urn:person:1", "display_name": "Murthy Reddy"}
    )
    candidate = suggest_candidate(
        store,
        existing_cid="urn:person:1",
        incoming_source_system="gitlab",
        incoming_identity="R. Murthy",
        match_basis="display_name",
        confidence=0.55,
    )
    queue = IdentityCandidateStore(tmp_path / "candidates.json")
    queue.add(candidate)
    assert queue.list(status="PENDING")[0].candidate_id == candidate.candidate_id

    decided = queue.decide(candidate.candidate_id, approve=True, reviewer="reviewer@example.invalid")
    assert decided.status == "CONFIRMED"
    assert decided.reviewer == "reviewer@example.invalid"
    with pytest.raises(ValueError, match="already been decided"):
        queue.decide(candidate.candidate_id, approve=False, reviewer="reviewer@example.invalid")

    # Persistence round-trip preserves the decision history.
    reloaded = IdentityCandidateStore(tmp_path / "candidates.json")
    assert reloaded.get(candidate.candidate_id).status == "CONFIRMED"


def test_candidate_api_review_flow(monkeypatch, tmp_path):
    api, store = client(monkeypatch, tmp_path)
    store.upsert_vertex("Person", {"canonical_id": "urn:person:1", "display_name": "Murthy"})

    from eoip.identity.candidates import IdentityCandidateStore, suggest_candidate

    queue = IdentityCandidateStore(tmp_path / "state" / "identity-candidates.json")
    queue.add(suggest_candidate(
        store,
        existing_cid="urn:person:1",
        incoming_source_system="servicenow",
        incoming_identity="murthy_reddy",
        match_basis="email_domain",
        confidence=0.4,
    ))

    listed = api.get("/api/v1/identity/candidates?status=PENDING", headers=_headers())
    assert listed.status_code == 200
    candidate_id = listed.json()["candidates"][0]["candidate_id"]

    decided = api.post(
        f"/api/v1/identity/candidates/{candidate_id}/decide",
        headers=_headers(),
        json={"actor_id": "reviewer@example.invalid"},
    )
    assert decided.status_code == 200
    assert decided.json()["status"] == "CONFIRMED"

    repeat = api.post(
        f"/api/v1/identity/candidates/{candidate_id}/reject",
        headers=_headers(),
        json={"actor_id": "reviewer@example.invalid"},
    )
    assert repeat.status_code == 409
    assert api.get(
        "/api/v1/identity/candidates?status=MAYBE", headers=_headers()
    ).status_code == 422
