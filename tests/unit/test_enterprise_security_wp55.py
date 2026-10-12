"""Unit tests for Phase 5 WP 5.5: Enterprise Security (5 tasks).

Requirements:
- GAP-SEC-008: Fail-closed HMAC-SHA256 bearer token verification and tampering rejection
- GAP-SEC-009: Ephemeral random secret fallback & seamless key rotation
- GAP-SEC-010: Token Revocation Store (CRL) with instant revocation and TTL pruning
- GAP-SEC-011: Fine-grained token scopes (wildcard & exact) and ABAC tenant claims
- GAP-SEC-012: Enterprise security REST API (/api/v1/security) & Policy Matrix
"""

from __future__ import annotations

import time
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from apps.api.app import create_app
from eoip.authz import (
    TokenError,
    TokenRevocationStore,
    TokenSigner,
    global_revocation_store,
    has_scope,
)
from eoip.graph.memory import MemoryGraphStore

WEB_SRC = Path(__file__).resolve().parents[2] / "apps" / "web" / "src"


@pytest.fixture(scope="module")
def client() -> TestClient:
    app = create_app(MemoryGraphStore())
    return TestClient(app)


# --- 1. GAP-SEC-008: Fail-Closed Verification ---

@pytest.mark.req("GAP-SEC-008")
def test_gap_sec_008_fail_closed_verification():
    signer = TokenSigner("secret-key-1", ttl_seconds=60)
    token = signer.issue("alice", roles=["admin"])

    # Valid token passes
    payload = signer.verify(token)
    assert payload["sub"] == "alice"
    assert payload["roles"] == ["admin"]

    # Malformed token raises TokenError
    with pytest.raises(TokenError, match="malformed"):
        signer.verify("invalid.token.structure.extra")
    with pytest.raises(TokenError, match="malformed"):
        signer.verify("not-a-token")

    # Tampered signature raises TokenError
    parts = token.split(".")
    tampered_sig = parts[0] + ".AAAA"
    with pytest.raises(TokenError, match="invalid signature"):
        signer.verify(tampered_sig)

    # Expired token raises TokenError
    expired_token = signer.issue("bob", ttl_seconds=-10)
    with pytest.raises(TokenError, match="token expired"):
        signer.verify(expired_token)


# --- 2. GAP-SEC-009: Ephemeral Fallback & Key Rotation ---

@pytest.mark.req("GAP-SEC-009")
def test_gap_sec_009_ephemeral_fallback_and_key_rotation(monkeypatch):
    # Ephemeral random fallback when unset
    monkeypatch.delenv("EOIP_AUTHZ_TOKEN_SECRET", raising=False)
    s1 = TokenSigner()
    s2 = TokenSigner()
    token1 = s1.issue("charlie")
    # Different ephemeral keys cannot verify each other
    with pytest.raises(TokenError, match="invalid signature"):
        s2.verify(token1)

    # Key rotation: old secret retained in previous_secrets
    rotating_signer = TokenSigner("initial-secret")
    old_token = rotating_signer.issue("david")
    assert rotating_signer.verify(old_token)["sub"] == "david"

    # Rotate to new secret
    rotating_signer.rotate_secret("new-rotated-secret")
    new_token = rotating_signer.issue("eve")

    # Both old and new tokens verify seamlessly during rollover window
    assert rotating_signer.verify(new_token)["sub"] == "eve"
    assert rotating_signer.verify(old_token)["sub"] == "david"


# --- 3. GAP-SEC-010: Token Revocation Store (CRL) ---

@pytest.mark.req("GAP-SEC-010")
def test_gap_sec_010_token_revocation_store():
    rev_store = TokenRevocationStore()
    signer = TokenSigner("secret-crl", revocation_store=rev_store)

    token = signer.issue("frank", jti="jti-frank-100")
    assert signer.verify(token)["sub"] == "frank"

    # Revoke by JTI
    rev_store.revoke("jti-frank-100", reason="compromised_credential")
    assert rev_store.is_revoked("jti-frank-100") is True

    # Verification must now fail closed
    with pytest.raises(TokenError, match="token has been revoked"):
        signer.verify(token)

    # Check active revocation list
    revocations = rev_store.list_revocations()
    assert len(revocations) >= 1
    assert any(r["identifier"] == "jti-frank-100" for r in revocations)

    # Expired revocations are pruned
    rev_store.revoke("jti-temp", expires_at=int(time.time()) - 10)
    pruned = rev_store.prune_expired()
    assert pruned >= 1
    assert rev_store.is_revoked("jti-temp") is False


# --- 4. GAP-SEC-011: Scoped Bearer Tokens & ABAC Claims ---

@pytest.mark.req("GAP-SEC-011")
def test_gap_sec_011_fine_grained_scopes_and_claims():
    assert has_scope(["graph:read", "graph:mutate"], "graph:read") is True
    assert has_scope(["graph:*"], "graph:read") is True
    assert has_scope(["graph:*"], "graph:mutate") is True
    assert has_scope(["admin:*"], "graph:read") is True
    assert has_scope(["*"], "anything:really") is True
    assert has_scope(["graph:read"], "graph:mutate") is False

    signer = TokenSigner("secret-scope")
    token = signer.issue(
        "grace",
        roles=["analyst"],
        scopes=["graph:read", "catalog:read"],
        tenant_id="tenant-acme",
        attributes={"dept": "finance"},
    )
    payload = signer.verify(token, required_scopes=["graph:read"])
    assert payload["tenant_id"] == "tenant-acme"
    assert payload["attributes"]["dept"] == "finance"

    # Missing required scope raises TokenError
    with pytest.raises(TokenError, match="insufficient scope"):
        signer.verify(token, required_scopes=["graph:mutate"])


# --- 5. GAP-SEC-012: REST Security Router & Policy Matrix ---

@pytest.mark.req("GAP-SEC-012")
def test_gap_sec_012_security_rest_api_and_dashboard(client):
    # Verify dashboard UI component exists
    dashboard_file = WEB_SRC / "admin" / "SecurityGovernanceDashboard.jsx"
    assert dashboard_file.exists()
    content = dashboard_file.read_text(encoding="utf-8")
    assert "Enterprise Security & Token Governance" in content
    assert "GAP-SEC-008..012" in content

    # GET /api/v1/security/status
    res = client.get("/api/v1/security/status")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "OPERATIONAL"
    assert data["enforcement_mode"] == "FAIL_CLOSED"
    assert data["key_rotation_supported"] is True

    # GET /api/v1/security/policy-matrix
    matrix_res = client.get("/api/v1/security/policy-matrix")
    assert matrix_res.status_code == 200
    m_data = matrix_res.json()
    assert "roles_hierarchy" in m_data
    assert "admin" in m_data["roles_hierarchy"]
    assert "viewer" in m_data["roles_hierarchy"]

    # POST /api/v1/security/tokens/issue
    issue_res = client.post(
        "/api/v1/security/tokens/issue",
        json={
            "subject": "service-worker-01",
            "roles": ["steward"],
            "scopes": ["graph:read", "ontology:publish"],
            "tenant_id": "tenant-01",
            "ttl_seconds": 1800,
        },
    )
    assert issue_res.status_code == 200
    issued = issue_res.json()
    token = issued["token"]
    jti = issued["jti"]
    assert token and jti

    # POST /api/v1/security/tokens/verify - success
    v_res = client.post(
        "/api/v1/security/tokens/verify",
        json={"token": token, "required_scopes": ["graph:read"]},
    )
    assert v_res.status_code == 200
    assert v_res.json()["valid"] is True

    # POST /api/v1/security/tokens/verify - insufficient scope
    v_fail = client.post(
        "/api/v1/security/tokens/verify",
        json={"token": token, "required_scopes": ["admin:*"]},
    )
    assert v_fail.status_code == 401

    # POST /api/v1/security/tokens/revoke
    revoke_res = client.post(
        "/api/v1/security/tokens/revoke",
        json={"identifier": jti, "reason": "routine_rotation"},
    )
    assert revoke_res.status_code == 200
    assert revoke_res.json()["revoked"] is True

    # Verify after revocation must fail 401
    v_revoked = client.post(
        "/api/v1/security/tokens/verify",
        json={"token": token},
    )
    assert v_revoked.status_code == 401
