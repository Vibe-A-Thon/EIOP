"""Governed proposal review flow (human control over agent-authored changes)."""

from _principals import provision_api_token, session_token, use_test_session_secret
from uuid import uuid4

from eoip.authn import Principal
from eoip.contracts.agent import ChangeProposal
from eoip.contracts.source_event import utc_now_iso
from eoip.graph.memory import MemoryGraphStore

from apps.api import main

TOKEN = "test-token-with-at-least-24-characters"


def client(monkeypatch, tmp_path):
    store = MemoryGraphStore()
    monkeypatch.setenv("EOIP_API_TOKEN", TOKEN)
    provision_api_token(monkeypatch, TOKEN)
    use_test_session_secret(monkeypatch)
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path))
    monkeypatch.setattr(main, "create_store", lambda: store)
    from fastapi.testclient import TestClient

    return TestClient(main.create_app())


def _headers():
    return {"Authorization": f"Bearer {TOKEN}"}


def _signed_headers(username, roles):
    principal = Principal(
        id=f"urn:eoip:authn:principal:{username}",
        username=username,
        roles=roles,
        provider="local",
    )
    return {"Authorization": f"Bearer {session_token(principal)}"}


def _proposal(proposal_id="p-1"):
    return ChangeProposal(
        proposal_id=proposal_id,
        run_id="run-1",
        proposed_by="KnowledgeCuratorAgent",
        operation="REVIEW_PROVENANCE",
        target_ref="urn:eoip:work:item:jira:EOIP-1",
        patch={"note": "attach missing source evidence"},
        rationale="Provenance coverage gap on a trusted work item",
        evidence_refs=["urn:eoip:evidence:demo"],
        risk_level="R2",
        created_at=utc_now_iso(),
    )


def test_proposals_list_and_review_roundtrip(monkeypatch, tmp_path):
    api = client(monkeypatch, tmp_path)
    response = api.get("/api/v1/agents/proposals", headers=_headers())
    assert response.status_code == 200
    assert response.json() == {"proposals": []}


def _seed_drift(monkeypatch, tmp_path):
    """Create an app instance whose store carries one unmapped label."""
    store = MemoryGraphStore()
    monkeypatch.setenv("EOIP_API_TOKEN", TOKEN)
    provision_api_token(monkeypatch, TOKEN)
    use_test_session_secret(monkeypatch)
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path))
    monkeypatch.setattr(main, "create_store", lambda: store)
    store._vertices["v:drift"] = {
        "vid": "v:drift",
        "canonical_id": "urn:custom:widget:1",
        "label": "CustomWidget",
        "properties": {"canonical_id": "urn:custom:widget:1"},
    }
    from fastapi.testclient import TestClient

    return TestClient(main.create_app())


def test_pending_proposal_can_be_approved_and_is_inert(monkeypatch, tmp_path):
    api = _seed_drift(monkeypatch, tmp_path)
    created = api.post("/api/v1/ontology/proposals", headers=_headers())
    assert created.status_code == 201

    listed = api.get("/api/v1/agents/proposals?status=PENDING", headers=_headers())
    proposals = listed.json()["proposals"]
    assert proposals

    approve = api.post(
        f"/api/v1/agents/proposals/{proposals[0]['proposal_id']}/approve",
        headers=_signed_headers("reviewer", ("admin",)),
        json={"actor_id": "forged-reviewer"},
    )
    assert approve.status_code == 200
    body = approve.json()
    assert body["status"] == "APPROVED"
    assert body["approved_by"] == "reviewer"
    assert body["decided_at"]

    # Approval is a state change only: the patch is never executed by the API.
    assert body["patch"] == proposals[0]["patch"]


def test_rejection_and_unknown_and_double_decision_paths(monkeypatch, tmp_path):
    api = _seed_drift(monkeypatch, tmp_path)
    api.post("/api/v1/ontology/proposals", headers=_headers())
    proposals = api.get("/api/v1/agents/proposals?status=PENDING", headers=_headers()).json()[
        "proposals"
    ]
    proposal_id = proposals[0]["proposal_id"]

    reject = api.post(
        f"/api/v1/agents/proposals/{proposal_id}/reject",
        headers=_signed_headers("reviewer", ("admin",)),
        json={"actor_id": "forged-reviewer"},
    )
    assert reject.status_code == 200
    assert reject.json()["status"] == "REJECTED"

    double = api.post(
        f"/api/v1/agents/proposals/{proposal_id}/approve",
        headers=_signed_headers("reviewer", ("admin",)),
        json={"actor_id": "forged-reviewer"},
    )
    assert double.status_code == 409

    missing = api.post(
        f"/api/v1/agents/proposals/{uuid4()}/approve",
        headers=_signed_headers("reviewer", ("admin",)),
        json={"actor_id": "forged-reviewer"},
    )
    assert missing.status_code == 404

    invalid_status = api.get("/api/v1/agents/proposals?status=MAYBE", headers=_headers())
    assert invalid_status.status_code == 422


def test_non_admin_cannot_decide_proposal(monkeypatch, tmp_path):
    api = _seed_drift(monkeypatch, tmp_path)
    api.post("/api/v1/ontology/proposals", headers=_headers())
    proposals = api.get("/api/v1/agents/proposals?status=PENDING", headers=_headers()).json()[
        "proposals"
    ]
    proposal_id = proposals[0]["proposal_id"]

    response = api.post(
        f"/api/v1/agents/proposals/{proposal_id}/approve",
        headers=_signed_headers("analyst", ("analyst",)),
        json={"actor_id": "forged-admin"},
    )

    assert response.status_code == 403
    assert api.get(
        f"/api/v1/agents/proposals?status=PENDING", headers=_headers()
    ).json()["proposals"]
