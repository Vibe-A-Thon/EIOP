from __future__ import annotations

import base64
from datetime import datetime, timezone
from typing import Any

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from eoip.aspeii.receipts import ASPEIIReceiptSigner, verify_action_certificate
from eoip.contracts.aspeii import (
    ActionReference,
    ASPEIIActionCertificatePayload,
    ASPEIIActionIntent,
    ASPEIIObligationResult,
    canonical_action_digest,
)


def _ref(kind: str, identifier: str, digest: str = "a" * 64) -> ActionReference:
    return ActionReference(kind=kind, id=identifier, revision=1, digest=digest)


def _action(**changes) -> ASPEIIActionIntent:
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
        "policy_ref": _ref("policy", "policy-1"),
        "destination": "eoip://graph/tenant-a",
        "account_id": "account-a",
        "effect_class": "INTERNAL_WRITE",
        "arguments": {"target": "resource-1"},
        "obligation_refs": [_ref("obligation", "obligation-1")],
        "scope": ["graph:mutate:resource-1"],
        "deadline": datetime(2030, 1, 1, tzinfo=timezone.utc),
        "created_at": datetime(2029, 12, 31, tzinfo=timezone.utc),
        "created_by": "principal-a",
        "logical_idempotency_key": "idempotency-key-0001",
    }
    return ASPEIIActionIntent(**(values | changes))


def _payload(action: ASPEIIActionIntent, key_id: str = "key-1") -> ASPEIIActionCertificatePayload:
    digest = canonical_action_digest(action)
    return ASPEIIActionCertificatePayload(
        certificate_id="certificate-1",
        action_ref=ActionReference(
            kind="action", id=action.action_id, revision=action.revision, digest=digest
        ),
        action_digest=digest,
        canonicalization_version=action.canonicalization_version,
        verifier_ref=_ref("checker", "checker-1"),
        required_obligation_refs=action.obligation_refs,
        obligation_results=[ASPEIIObligationResult(
            obligation_ref=action.obligation_refs[0],
            verifier_ref=_ref("verifier", "verifier-1"),
            decision="PASS",
            reason_code="CHECKED",
            evaluated_at=datetime(2029, 12, 31, tzinfo=timezone.utc),
        )],
        authorization_decision="ALLOW",
        enforceability_mode="PRE_EXECUTION_GATE",
        issued_at=datetime(2029, 12, 31, tzinfo=timezone.utc),
        expires_at=datetime(2030, 1, 1, tzinfo=timezone.utc),
        key_id=key_id,
    )


@pytest.mark.req("ASPEII-RQ-022.C01", "ASPEII-RQ-022.C03")
def test_ed25519_receipt_verifies_with_explicit_trusted_public_key():
    private_key = Ed25519PrivateKey.generate()
    signer = ASPEIIReceiptSigner.from_private_key(key_id="key-1", private_key=private_key)
    action = _action()
    certificate = signer.sign(_payload(action), action=action)

    result = verify_action_certificate(
        certificate,
        action=action,
        trusted_public_keys={"key-1": signer.public_key_bytes},
        now=datetime(2029, 12, 31, 12, tzinfo=timezone.utc),
    )

    assert result.valid is True
    assert result.reason_code == "SIGNATURE_VALID"


@pytest.mark.req("ASPEII-RQ-022.C01", "ASPEII-RQ-022.C04")
def test_ed25519_receipt_rejects_tampered_signature_unknown_key_and_changed_action():
    private_key = Ed25519PrivateKey.generate()
    signer = ASPEIIReceiptSigner.from_private_key(key_id="key-1", private_key=private_key)
    action = _action()
    certificate = signer.sign(_payload(action), action=action)
    now = datetime(2029, 12, 31, 12, tzinfo=timezone.utc)

    tampered = certificate.model_copy(update={"signature": base64.b64encode(b"x" * 64).decode()})
    assert not verify_action_certificate(
        tampered, action=action, trusted_public_keys={"key-1": signer.public_key_bytes}, now=now
    ).valid
    assert verify_action_certificate(
        certificate, action=action, trusted_public_keys={}, now=now
    ).reason_code == "UNTRUSTED_KEY_ID"
    changed_action = _action(account_id="different-account")
    assert verify_action_certificate(
        certificate,
        action=changed_action,
        trusted_public_keys={"key-1": signer.public_key_bytes},
        now=now,
    ).reason_code == "ACTION_DIGEST_MISMATCH"


@pytest.mark.req("ASPEII-RQ-022.C01", "ASPEII-RQ-022.C02")
def test_receipt_signer_requires_explicit_valid_private_key_and_key_id():
    signer_factory: Any = ASPEIIReceiptSigner
    with pytest.raises(TypeError):
        signer_factory()
    with pytest.raises(ValueError, match="exactly 32 bytes"):
        ASPEIIReceiptSigner(key_id="key-1", private_key_bytes=b"short")
    with pytest.raises(ValueError, match="key id"):
        ASPEIIReceiptSigner(key_id="", private_key_bytes=b"x" * 32)


@pytest.mark.req("ASPEII-RQ-022.C01")
def test_receipt_verification_rejects_expired_and_not_yet_valid_certificates():
    private_key = Ed25519PrivateKey.generate()
    signer = ASPEIIReceiptSigner.from_private_key(key_id="key-1", private_key=private_key)
    action = _action()
    certificate = signer.sign(_payload(action), action=action)
    keys = {"key-1": signer.public_key_bytes}

    expired = verify_action_certificate(
        certificate, action=action, trusted_public_keys=keys,
        now=datetime(2030, 1, 1, tzinfo=timezone.utc),
    )
    early = verify_action_certificate(
        certificate, action=action, trusted_public_keys=keys,
        now=datetime(2029, 12, 30, tzinfo=timezone.utc),
    )

    assert expired.reason_code == "CERTIFICATE_EXPIRED_OR_NOT_YET_VALID"
    assert early.reason_code == "CERTIFICATE_EXPIRED_OR_NOT_YET_VALID"


@pytest.mark.req("ASPEII-RQ-022.C01", "ASPEII-RQ-022.C04")
def test_receipt_binds_noninitial_action_revision_and_rejects_mismatched_reference():
    private_key = Ed25519PrivateKey.generate()
    signer = ASPEIIReceiptSigner.from_private_key(key_id="key-1", private_key=private_key)
    action = _action(revision=2)
    certificate = signer.sign(_payload(action), action=action)

    verified = verify_action_certificate(
        certificate,
        action=action,
        trusted_public_keys={"key-1": signer.public_key_bytes},
        now=datetime(2029, 12, 31, 12, tzinfo=timezone.utc),
    )
    mismatched_reference = certificate.model_copy(update={
        "action_ref": certificate.action_ref.model_copy(update={"revision": 1})
    })
    rejected = verify_action_certificate(
        mismatched_reference,
        action=action,
        trusted_public_keys={"key-1": signer.public_key_bytes},
        now=datetime(2029, 12, 31, 12, tzinfo=timezone.utc),
    )

    assert verified.valid is True
    assert rejected.reason_code == "ACTION_REFERENCE_MISMATCH"