"""Unit tests for the RBAC/ABAC authorization framework (GAP-SEC-001..012)."""

from __future__ import annotations

import json
import time

import pytest

from eoip.authz import (
    KNOWN_PERMISSIONS,
    PolicyEnforcer,
    PolicyStatement,
    RoleRegistry,
    TokenError,
    TokenSigner,
    UserStore,
    load_policy_yaml,
    role_inherited_roles,
    role_rank,
)


@pytest.fixture
def enforcer() -> PolicyEnforcer:
    enc = PolicyEnforcer()
    enc.add_policy(PolicyStatement(policy_id="p-viewer-read", role="viewer", permission="graph:read"))
    enc.add_policy(PolicyStatement(policy_id="p-analyst-mutate", role="analyst", permission="graph:mutate"))
    enc.add_policy(
        PolicyStatement(
            policy_id="p-steward-publish",
            role="steward",
            permission="ontology:publish",
            conditions=(
                {"attribute": "classification", "op": "in", "value": ["internal", "public"]},
            ),
        )
    )
    return enc


@pytest.fixture
def store() -> UserStore:
    s = UserStore()
    s.create_user("alice", ["admin"])
    s.create_user("bob", ["viewer"])
    s.create_user("carol", ["analyst"], attributes={"department": "eng"})
    s.create_user("dave", ["steward"])
    return s


# ---------------------------------------------------------------------------
# Role hierarchy (GAP-SEC-002)
# ---------------------------------------------------------------------------

@pytest.mark.req("H-04")
def test_builtin_roles_have_stable_urn_ids():
    reg = RoleRegistry()
    admin = reg.get_role("admin")
    assert admin["role_id"] == "urn:eoip:authz:role:admin"


def test_role_hierarchy_inheritance():
    assert role_rank("admin") > role_rank("steward") > role_rank("analyst") > role_rank("viewer")
    assert role_inherited_roles("steward") == ["viewer", "analyst", "steward"]
    assert role_inherited_roles("unknown-role") == []


def test_permission_catalog_contains_core_permissions():
    for perm in ("graph:read", "graph:mutate", "ontology:publish", "agents:approve", "admin:*"):
        assert perm in KNOWN_PERMISSIONS


def test_role_registry_crud_and_builtin_protection():
    reg = RoleRegistry()
    reg.create_role("auditor", description="read-only audit", permissions=["audit:read"])
    assert reg.get_role("auditor")["description"] == "read-only audit"
    reg.update_role("auditor", description="updated")
    assert reg.get_role("auditor")["description"] == "updated"
    with pytest.raises(ValueError):
        reg.create_role("auditor")
    with pytest.raises(ValueError):
        reg.create_role("badperm", permissions=["nope:read"])
    with pytest.raises(ValueError):
        reg.delete_role("admin")  # built-in protected
    reg.delete_role("auditor")
    assert reg.get_role("auditor") is None


# ---------------------------------------------------------------------------
# Default-deny enforcement (GAP-SEC-004)
# ---------------------------------------------------------------------------

def test_default_deny_no_matching_policy(enforcer, store):
    dec = enforcer.enforce(store.get_user("bob"), "ontology:publish", {"classification": "internal"})
    assert not dec.allow
    assert any("no policy grants" in r for r in dec.reasons)


def test_default_deny_unknown_action(enforcer, store):
    dec = enforcer.enforce(store.get_user("alice"), "unknown:thing", {})
    assert not dec.allow


def test_viewer_can_read_graph(enforcer, store):
    dec = enforcer.enforce(store.get_user("bob"), "graph:read", {})
    assert dec.allow
    assert dec.policy_id == "p-viewer-read"


def test_hierarchy_admin_inherits_viewer_grant(enforcer, store):
    dec = enforcer.enforce(store.get_user("alice"), "graph:read", {})
    assert dec.allow


def test_viewer_cannot_mutate(enforcer, store):
    assert not enforcer.enforce(store.get_user("bob"), "graph:mutate", {}).allow
    assert enforcer.enforce(store.get_user("carol"), "graph:mutate", {}).allow


def test_fail_closed_on_evaluation_error(enforcer, store):
    class Exploding:
        roles = ["viewer"]
        user_id = "eve"
    dec = enforcer.enforce(Exploding(), "graph:read", None)  # fine
    assert dec.allow
    # A statement whose conditions raise (non-dict attrs) must deny, not crash.
    bad = PolicyEnforcer([PolicyStatement(policy_id="bad", role="viewer", permission="graph:read")])
    dec = bad.enforce(store.get_user("bob"), "graph:read", {"domain": {"unhashable": {}}})
    # dict attrs are fine; force an error instead with malformed action bytes
    dec = bad.enforce(store.get_user("bob"), b"\xff".decode("utf-8", "surrogateescape"), {})
    assert not dec.allow
    assert any("fail-closed" in r or "malformed" in r for r in dec.reasons)


# ---------------------------------------------------------------------------
# ABAC conditions (GAP-SEC-003)
# ---------------------------------------------------------------------------

def test_abac_condition_eq():
    cond = load_policy_yaml(
        "policies:\n"
        "  - id: p1\n"
        "    role: analyst\n"
        "    permission: graph:read\n"
        "    conditions:\n"
        "      - {attribute: domain, op: eq, value: finance}\n"
    )[0]
    assert cond.conditions[0].matches({"domain": "finance"})
    assert not cond.conditions[0].matches({"domain": "hr"})


def test_abac_policy_requires_classification(enforcer, store):
    dave = store.get_user("dave")
    assert enforcer.enforce(dave, "ontology:publish", {"classification": "internal"}).allow
    assert enforcer.enforce(dave, "ontology:publish", {"classification": "public"}).allow
    denied = enforcer.enforce(dave, "ontology:publish", {"classification": "restricted"})
    assert not denied.allow
    # Missing attribute also denies (condition not met).
    assert not enforcer.enforce(dave, "ontology:publish", {}).allow


def test_abac_source_system_condition():
    stmts = load_policy_yaml(
        "policies:\n"
        "  - id: p-src\n"
        "    role: analyst\n"
        "    permission: graph:read\n"
        "    conditions:\n"
        "      - {attribute: source_system, op: in, value: [jira, gitlab]}\n"
    )
    enc = PolicyEnforcer(stmts)
    user = UserStore()
    user.create_user("u1", ["analyst"])
    assert enc.enforce(user.get_user("u1"), "graph:read", {"source_system": "jira"}).allow
    assert not enc.enforce(user.get_user("u1"), "graph:read", {"source_system": "confluence"}).allow


def test_policy_yaml_load_roundtrip():
    text = (
        "policies:\n"
        "  - id: p1\n"
        "    role: steward\n"
        "    permission: ontology:publish\n"
        "    conditions:\n"
        "      - {attribute: classification, op: in, value: [internal, public]}\n"
    )
    stmts = load_policy_yaml(text)
    assert len(stmts) == 1
    assert stmts[0].to_dict()["conditions"][0]["attribute"] == "classification"


def test_admin_wildcard_permission():
    enc = PolicyEnforcer([
        PolicyStatement(policy_id="p-admin", role="admin", permission="admin:*"),
    ])
    enc.add_policy(PolicyStatement(policy_id="p-admin-read", role="admin", permission="graph:read"))
    user = UserStore()
    user.create_user("root", ["admin"])
    assert enc.enforce(user.get_user("root"), "admin:anything", {}).allow


# ---------------------------------------------------------------------------
# Audit records of decisions (GAP-SEC-004, §48)
# ---------------------------------------------------------------------------

def test_decision_audit_record_is_redacted_and_serializable(enforcer, store):
    dec = enforcer.enforce(store.get_user("alice"), "graph:read", {"token": "secret-value"})
    record = dec.to_audit_record()
    assert record["event"] == "authz.decision"
    assert record["allow"] is True
    assert record["decision_id"].startswith("urn:eoip:authz:decision:")
    # resource attrs aren't dumped raw; reasons are present
    assert "secret-value" not in json.dumps(record)
    json.dumps(record)  # must be JSON-serializable


def test_deny_decision_has_reasons(enforcer, store):
    dec = enforcer.enforce(store.get_user("bob"), "graph:mutate", {})
    assert not dec.allow
    assert len(dec.reasons) >= 1
    record = dec.to_audit_record()
    assert record["allow"] is False


# ---------------------------------------------------------------------------
# Export round-trips (GAP-SEC-005, GAP-SEC-006)
# ---------------------------------------------------------------------------

def test_role_registry_export_roundtrip():
    reg = RoleRegistry()
    reg.create_role("auditor", permissions=["audit:read"])
    reg.update_role("steward", description="data steward")
    restored = RoleRegistry.from_json(reg.export_json())
    assert restored.get_role("auditor") == reg.get_role("auditor")
    assert restored.get_role("steward") == reg.get_role("steward")
    assert restored.get_role("admin") == reg.get_role("admin")


def test_user_store_export_roundtrip(store):
    restored = UserStore.from_json(store.export_json())
    for uid in ("alice", "bob", "carol", "dave"):
        original, copy = store.get_user(uid), restored.get_user(uid)
        assert copy is not None
        assert copy.to_dict() == original.to_dict()


def test_user_store_crud(store):
    store.update_user("bob", roles=["analyst"])
    assert store.get_user("bob").roles == ["analyst"]
    store.delete_user("bob")
    assert store.get_user("bob") is None
    assert store.get_user("nobody") is None
    with pytest.raises(KeyError):
        store.update_user("nobody", roles=["viewer"])
    with pytest.raises(ValueError):
        store.create_user("alice", ["viewer"])  # duplicate


# ---------------------------------------------------------------------------
# HMAC-SHA256 tokens (GAP-SEC-007..009)
# ---------------------------------------------------------------------------

def test_token_issue_verify_roundtrip():
    signer = TokenSigner("test-secret")
    token = signer.issue("alice", roles=["admin"])
    payload = signer.verify(token)
    assert payload["sub"] == "alice"
    assert payload["roles"] == ["admin"]


def test_token_tampering_rejected():
    signer = TokenSigner("test-secret")
    token = signer.issue("alice")
    payload_b64, sig = token.split(".")
    forged = payload_b64[:-2] + ("AA" if not payload_b64.endswith("AA") else "AB") + "." + sig
    with pytest.raises(TokenError):
        signer.verify(forged)


def test_token_wrong_secret_rejected():
    signer = TokenSigner("secret-a")
    token = signer.issue("alice")
    with pytest.raises(TokenError):
        TokenSigner("secret-b").verify(token)


def test_token_expiry():
    signer = TokenSigner("test-secret", ttl_seconds=1)
    token = signer.issue("alice", ttl_seconds=-1)
    with pytest.raises(TokenError):
        signer.verify(token)
    live = signer.issue("bob", ttl_seconds=60)
    assert signer.verify(live)["sub"] == "bob"


def test_token_malformed_rejected():
    signer = TokenSigner("test-secret")
    with pytest.raises(TokenError):
        signer.verify("not-a-token")
    with pytest.raises(TokenError):
        signer.verify("abc.def.ghi")


def test_token_signer_random_secret_when_unconfigured(monkeypatch):
    monkeypatch.delenv("EOIP_AUTHZ_TOKEN_SECRET", raising=False)
    s1, s2 = TokenSigner(), TokenSigner()
    token = s1.issue("alice")
    with pytest.raises(TokenError):
        s2.verify(token)
