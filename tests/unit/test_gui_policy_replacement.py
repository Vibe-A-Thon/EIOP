"""Policy editor replacement must remove obsolete grants and retain ABAC semantics."""

import json

import pytest
from fastapi.testclient import TestClient

from apps.api.app import create_app
from eoip.authz.core import PolicyEnforcer, User
from eoip.graph.memory import MemoryGraphStore


def policy_doc(permission="graph:read"):
    return {"policies": [{"policy_id": "gui-policy", "role": "analyst", "permission": permission,
                          "description": "",
                          "conditions": [{"attribute": "classification", "op": "eq", "value": "internal"}]}]}


def test_replacement_retains_conditions_and_removes_obsolete_grants():
    enforcer = PolicyEnforcer()
    enforcer.load_yaml(json.dumps(policy_doc("graph:mutate")))
    assert enforcer.replace_yaml(json.dumps(policy_doc())) == 1
    user = User("alice", ["analyst"])
    assert enforcer.enforce(user, "graph:read", {"classification": "internal"}).allow
    assert not enforcer.enforce(user, "graph:read", {"classification": "restricted"}).allow
    assert not enforcer.enforce(user, "graph:mutate", {"classification": "internal"}).allow
    enforcer.replace_yaml(json.dumps(policy_doc()))
    assert len(enforcer.statements) == 1


@pytest.mark.parametrize("invalid", [
    {"policies": [{"role": "analyst"}]},
    {"policies": policy_doc()["policies"] * 2},
    {"policies": "invalid"},
    {"policies": ["invalid"]},
    "invalid",
])
def test_invalid_replacement_leaves_active_set_intact(invalid):
    enforcer = PolicyEnforcer()
    enforcer.load_yaml(json.dumps(policy_doc()))
    before = enforcer.statements
    with pytest.raises((KeyError, ValueError)):
        enforcer.replace_yaml(json.dumps(invalid))
    assert enforcer.statements == before


def test_real_api_replacement_round_trip_and_failed_validation(tmp_path, monkeypatch):
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path))
    with TestClient(create_app(MemoryGraphStore())) as client:
        response = client.post("/api/v1/authz/policies/reload?replace_existing=true",
                               content=json.dumps(policy_doc()), headers={"Content-Type": "application/yaml"})
        assert response.status_code == 200
        assert response.json() == {"loaded": 1}
        assert client.get("/api/v1/authz/policies").json() == policy_doc()
        failure = client.post("/api/v1/authz/policies/reload?replace_existing=true",
                              content='{"policies":[{"role":"analyst"}]}',
                              headers={"Content-Type": "application/yaml"})
        assert failure.status_code == 422
        assert client.get("/api/v1/authz/policies").json() == policy_doc()
