"""Tests for ASPEII governed action lifecycle and verification."""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import pytest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from eoip.contracts.aspeii import (
    ActionReference,
    ASPEIIActionCertificate,
    ASPEIIActionCertificatePayload,
    ASPEIIActionIntent,
    ASPEIIApprovalDecision,
    ASPEIIObligationResult,
    canonical_action_digest,
)
from eoip.aspeii.receipts import ASPEIIReceiptSigner
from eoip.aspeii.admission import ASPEIIAdmissionController
from eoip.aspeii.dispatcher import ASPEIIDispatcher
from eoip.aspeii.verifier import ASPEIIVerifier


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
        "tenant_id": "acme-demo",
        "workspace_id": "workspace-a",
        "principal_id": "principal-a",
        "intent_ref": _ref("intent", "intent-1"),
        "task_ref": _ref("task", "task-1"),
        "grant_ref": _ref("grant", "grant-1"),
        "tool_ref": _ref("tool", "tool-1"),
        "adapter_ref": _ref("adapter", "adapter-1"),
        "resource_ref": _ref("resource", "resource-1"),
        "destination": "eoip://graph/acme-demo",
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


def test_aspeii_action_intent_and_digest():
    intent = _action()
    digest = canonical_action_digest(intent)
    assert len(digest) == 64
    assert intent.effect_class == "INTERNAL_WRITE"


def test_aspeii_admission_separation_of_duties():
    controller = ASPEIIAdmissionController(allowed_tenants={"acme-demo"})
    intent = _action(
        effect_class="IRREVERSIBLE",
        principal_id="user:operator@example.com",
        created_by="user:operator@example.com",
        logical_idempotency_key="idempotency-key-reboot-1",
    )
    digest = canonical_action_digest(intent)

    # 1. Missing approval for IRREVERSIBLE action fails
    dec = controller.evaluate_admission(intent)
    assert not dec.admitted
    assert dec.status_code == "APPROVAL_REQUIRED"

    # 2. Self-approval is rejected by model validation (enforcing separation of duties)
    with pytest.raises(Exception) as exc_info:
        ASPEIIApprovalDecision(
            approval_id="app-1",
            tenant_id="acme-demo",
            action_ref=ActionReference(kind="action", id=intent.action_id, revision=1, digest=digest),
            action_digest=digest,
            requester_principal_id="user:operator@example.com",
            reviewer_principal_id="user:operator@example.com",
            decision="APPROVE",
            rationale="Approved by myself",
            policy_ref=ActionReference(kind="policy", id="pol-reboot", revision=1, digest="b" * 64),
            separation_of_duties_passed=False,
            decided_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )
    assert "cannot approve their own action" in str(exc_info.value)

    # 3. Valid independent approval succeeds
    valid_app = ASPEIIApprovalDecision(
        approval_id="app-2",
        tenant_id="acme-demo",
        action_ref=ActionReference(kind="action", id=intent.action_id, revision="1", digest=digest),
        action_digest=digest,
        requester_principal_id="user:operator@example.com",
        reviewer_principal_id="user:security_officer@example.com",
        decision="APPROVE",
        rationale="Approved by security officer after review",
        policy_ref=ActionReference(kind="policy", id="pol-reboot", revision="1", digest="b" * 64),
        separation_of_duties_passed=True,
        decided_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    dec_ok = controller.evaluate_admission(intent, approvals=[valid_app])
    assert dec_ok.admitted
    assert dec_ok.status_code == "ADMITTED"


def test_aspeii_dispatcher_and_rollback():
    controller = ASPEIIAdmissionController(allowed_tenants={"acme-demo"})
    dispatcher = ASPEIIDispatcher(controller)

    # Register custom reversible handler
    def sample_write_handler(intent: ASPEIIActionIntent):
        return True, {"created_id": "TICKET-42"}, {"delete_id": "TICKET-42"}

    dispatcher.register_handler("tool-1", sample_write_handler)

    intent = _action(
        logical_idempotency_key="idempotency-key-ticket-42",
    )

    res = dispatcher.dispatch(intent)
    assert res.success
    assert res.status_code == "EXECUTED"
    assert res.rollback is not None
    assert res.rollback.undo_command == {"delete_id": "TICKET-42"}
    assert len(res.rollback.receipt_sha256) == 64


def test_aspeii_verifier_bundle_pass(tmp_path: Path):
    bundle_dir = tmp_path / "aspeii_run"
    bundle_dir.mkdir()

    manifest = {
        "run_id": "run-test-01",
        "profile": "local-sqlite-windows",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    (bundle_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    # Generate 5 sample passing cases covering 5 clauses
    cases = []
    for i in range(1, 6):
        cases.append({
            "case_id": f"case-test-{i}",
            "clause_ids": [f"ASPEII-RQ-{i:03d}.C01"],
            "status": "PASSED",
            "expected": {"result": True},
            "observed": {"result": True},
        })

    cases_file = bundle_dir / "cases.jsonl"
    cases_file.write_text("\n".join(json.dumps(c) for c in cases) + "\n", encoding="utf-8")

    verifier = ASPEIIVerifier(expected_total_clauses=5)
    res = verifier.verify_bundle(bundle_dir)
    assert res.verdict == "PASS"
    assert res.verified_clauses == 5
    assert (bundle_dir / "verifier-result.json").exists()
