from datetime import datetime, timedelta, timezone
from typing import Literal

import pytest
from eoip.contracts.aspeii import (
    ActionReference,
    ASPEIIActionCertificate,
    ASPEIIActionIntent,
    ASPEIIApprovalDecision,
    ASPEIIObligationResult,
    canonical_action_bytes,
    canonical_action_digest,
)
from pydantic import ValidationError


def _ref(kind: str, identifier: str) -> ActionReference:
    return ActionReference(
        kind=kind,
        id=identifier,
        revision=1,
        digest="a" * 64,
    )


def _action(**overrides) -> ASPEIIActionIntent:
    values = {
        "action_id": "action-1",
        "revision": 1,
        "tenant_id": "tenant-a",
        "workspace_id": "workspace-a",
        "principal_id": "principal-a",
        "intent_ref": _ref("intent", "intent-1"),
        "task_ref": _ref("task", "task-1"),
        "grant_ref": _ref("grant", "grant-1"),
        "tool_ref": _ref("tool", "tool-1"),
        "adapter_ref": _ref("adapter", "adapter-1"),
        "resource_ref": _ref("resource", "resource-1"),
        "destination": "eoip://graph/tenant-a",
        "account_id": "account-a",
        "effect_class": "INTERNAL_WRITE",
        "arguments": {"z": 2, "a": 1},
        "expected_state": {"revision": "r1"},
        "policy_ref": _ref("policy", "policy-1"),
        "obligation_refs": [_ref("obligation", "obligation-1")],
        "evidence_refs": [_ref("evidence", "evidence-1")],
        "scope": ["graph:mutate:resource-1"],
        "deadline": datetime(2030, 1, 1, tzinfo=timezone.utc),
        "created_at": datetime(2029, 12, 31, tzinfo=timezone.utc),
        "created_by": "principal-a",
        "logical_idempotency_key": "idempotency-key-0001",
    }
    return ASPEIIActionIntent(**(values | overrides))


def _obligation_result(decision: Literal["PASS", "FAIL", "UNKNOWN"] = "PASS") -> ASPEIIObligationResult:
    return ASPEIIObligationResult(
        obligation_ref=_ref("obligation", "obligation-1"),
        verifier_ref=_ref("verifier", "verifier-1"),
        decision=decision,
        reason_code="CHECKED",
        evaluated_at=datetime(2029, 12, 31, tzinfo=timezone.utc),
    )


@pytest.mark.req("ASPEII-RQ-018.C01", "ASPEII-RQ-018.C02")
def test_action_digest_is_independent_of_object_key_order():
    first = _action(arguments={"z": 2, "a": 1})
    second = _action(arguments={"a": 1, "z": 2})

    assert canonical_action_digest(first) == canonical_action_digest(second)
    assert canonical_action_bytes(first).startswith(b"EOIP-ASPEII-ACTION-v1\n")


@pytest.mark.req("ASPEII-RQ-018.C02")
def test_action_scope_set_order_is_normalized_but_argument_array_order_is_significant():
    first = _action(scope=["graph:mutate:resource-1", "graph:read:resource-1"], arguments={"steps": [1, 2]})
    reordered_scope = _action(scope=["graph:read:resource-1", "graph:mutate:resource-1"], arguments={"steps": [1, 2]})
    reordered_array = _action(scope=["graph:mutate:resource-1", "graph:read:resource-1"], arguments={"steps": [2, 1]})

    assert canonical_action_digest(first) == canonical_action_digest(reordered_scope)
    assert canonical_action_digest(first) != canonical_action_digest(reordered_array)


@pytest.mark.req("ASPEII-RQ-018.C02", "ASPEII-RQ-018.C03")
@pytest.mark.parametrize("field,value", [
    ("tenant_id", "tenant-b"),
    ("revision", 2),
    ("destination", "https://other.example.invalid/write"),
    ("account_id", "account-b"),
    ("arguments", {"z": 2, "a": 2}),
    ("deadline", datetime(2030, 1, 2, tzinfo=timezone.utc)),
    ("policy_ref", _ref("policy", "policy-2")),
])
def test_security_bearing_action_changes_change_digest(field, value):
    assert canonical_action_digest(_action()) != canonical_action_digest(_action(**{field: value}))


@pytest.mark.req("ASPEII-RQ-018.C03")
def test_action_timestamps_are_normalized_to_utc_before_digest():
    utc_action = _action(deadline=datetime(2030, 1, 1, 0, 0, tzinfo=timezone.utc))
    offset_action = _action(deadline=datetime(2030, 1, 1, 5, 30, tzinfo=timezone(timedelta(hours=5, minutes=30))))

    assert canonical_action_digest(utc_action) == canonical_action_digest(offset_action)


@pytest.mark.req("ASPEII-RQ-018.C02")
def test_action_security_projection_is_deeply_immutable():
    action = _action(arguments={"nested": {"items": ["original"]}})

    with pytest.raises(TypeError):
        action.arguments["nested"]["items"][0] = "mutated"
    with pytest.raises(TypeError):
        action.scope.append("graph:export:*")


@pytest.mark.req("ASPEII-RQ-018.C03", "ASPEII-RQ-018.C06")
@pytest.mark.parametrize("arguments", [
    {1: "non-string key"},
    {"nested": {1: "non-string key"}},
    {"not-finite": float("nan")},
    {"not-finite": float("inf")},
    {"outside-safe-integer": 2**53},
    {"unsupported": object()},
])
def test_action_rejects_values_outside_json_canonicalization_domain(arguments):
    with pytest.raises(ValidationError):
        _action(arguments=arguments)


@pytest.mark.req("ASPEII-RQ-018.C03", "ASPEII-RQ-018.C06")
def test_action_rejects_naive_timestamps():
    with pytest.raises(ValidationError):
        _action(deadline=datetime(2030, 1, 1))


@pytest.mark.req("ASPEII-RQ-019.C03", "ASPEII-RQ-022.C01")
def test_action_certificate_requires_allow_and_all_obligations_pass():
    action = _action()
    action_digest = canonical_action_digest(action)
    values = {
        "certificate_id": "certificate-1",
        "action_ref": ActionReference(
            kind="action", id=action.action_id, revision=1, digest=action_digest
        ),
        "action_digest": action_digest,
        "canonicalization_version": action.canonicalization_version,
        "verifier_ref": _ref("checker", "checker-1"),
        "required_obligation_refs": [_ref("obligation", "obligation-1")],
        "obligation_results": [_obligation_result()],
        "authorization_decision": "ALLOW",
        "enforceability_mode": "PRE_EXECUTION_GATE",
        "issued_at": datetime(2029, 12, 31, tzinfo=timezone.utc),
        "expires_at": datetime(2030, 1, 1, tzinfo=timezone.utc),
        "key_id": "test-key-1",
        "signature": "test-signature",
    }

    certificate = ASPEIIActionCertificate.model_validate(values)
    assert certificate.action_digest == canonical_action_digest(action)
    with pytest.raises(ValidationError, match="failed or unknown obligations"):
        ASPEIIActionCertificate.model_validate(
            values | {"obligation_results": [_obligation_result("UNKNOWN")]}
        )
    with pytest.raises(ValidationError, match="every required obligation"):
        ASPEIIActionCertificate.model_validate(values | {
            "required_obligation_refs": [
                _ref("obligation", "obligation-1"),
                _ref("obligation", "obligation-2"),
            ],
        })


@pytest.mark.req("ASPEII-RQ-020.C01", "ASPEII-RQ-020.C02")
def test_approval_decision_requires_distinct_reviewer_and_consistent_state():
    values = {
        "approval_id": "approval-1",
        "tenant_id": "tenant-a",
        "action_ref": ActionReference(
            kind="action", id="action-1", revision=1, digest="b" * 64
        ),
        "action_digest": "b" * 64,
        "requester_principal_id": "principal-a",
        "reviewer_principal_id": "principal-b",
        "decision": "APPROVE",
        "rationale": "Reviewed exact action effects",
        "policy_ref": _ref("policy", "policy-1"),
        "separation_of_duties_passed": True,
        "decided_at": datetime(2029, 12, 31, tzinfo=timezone.utc),
        "expires_at": datetime(2030, 1, 1, tzinfo=timezone.utc),
    }

    approval = ASPEIIApprovalDecision.model_validate(values)
    assert approval.state == "AVAILABLE"
    with pytest.raises(ValidationError, match="cannot approve their own action"):
        ASPEIIApprovalDecision.model_validate(values | {"reviewer_principal_id": "principal-a"})
    with pytest.raises(ValidationError, match="requires consumed_at"):
        ASPEIIApprovalDecision.model_validate(values | {"state": "CONSUMED"})