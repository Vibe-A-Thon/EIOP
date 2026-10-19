"""in-toto Statement v1 and DSSE envelope generation and verification (T-207 / REVA-VS-008 / §7.6.6)."""

from __future__ import annotations

import base64
import hashlib
import json
from typing import Any, Dict, List, Optional
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from reva.core.errors import RevaIntegrityError, RevaSignatureError
from reva.core.ids import attestation_id as compute_attestation_id
from reva.core.jcs import canonicalize

DSSE_PAYLOAD_TYPE = "application/vnd.in-toto+json"
PREDICATE_TYPE_VERIFICATION = "https://reva.kgf/verification/v1"


def compute_dsse_pae(payload_type: str, payload_bytes: bytes) -> bytes:
    """Compute Pre-Authentication Encoding (PAE) per DSSE specification."""
    type_bytes = payload_type.encode("utf-8")
    return (
        b"DSSEv1 "
        + str(len(type_bytes)).encode("ascii")
        + b" "
        + type_bytes
        + b" "
        + str(len(payload_bytes)).encode("ascii")
        + b" "
        + payload_bytes
    )


def create_in_toto_statement(
    repo_id: str,
    commit: str,
    owner_files: List[Dict[str, str]],  # [{path, sha256}]
    run_record: Dict[str, Any],
    binding_digest: str,
    obligation_keys: List[str],
) -> Dict[str, Any]:
    """Create in-toto Statement v1 dictionary."""
    subjects = [
        {"name": f"git:{repo_id}", "digest": {"gitCommit": commit}}
    ]
    for of in owner_files:
        subjects.append({"name": of["path"], "digest": {"sha256": of["sha256"]}})

    # Strip raw bytes or large output buffers if present in run_record
    sanitized_record = dict(run_record)
    sanitized_record.pop("stdout", None)
    sanitized_record.pop("stderr", None)

    predicate = {
        "binding_digest": binding_digest,
        "obligation_keys": sorted(list(set(obligation_keys))),
        "run_record": sanitized_record,
    }

    return {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": subjects,
        "predicateType": PREDICATE_TYPE_VERIFICATION,
        "predicate": predicate,
    }


def create_dsse_attestation(
    statement: Dict[str, Any],
    private_key: Ed25519PrivateKey,
    key_id: str,
) -> Dict[str, Any]:
    """Sign an in-toto statement and produce a DSSE envelope with att1_ identifier."""
    payload_bytes = canonicalize(statement)
    pae = compute_dsse_pae(DSSE_PAYLOAD_TYPE, payload_bytes)
    sig_raw = private_key.sign(pae)
    sig_b64 = base64.urlsafe_b64encode(sig_raw).decode("ascii").rstrip("=")
    payload_b64 = base64.b64encode(payload_bytes).decode("ascii")

    att_id = compute_attestation_id(payload_bytes)

    envelope = {
        "attestation_id": att_id,
        "payloadType": DSSE_PAYLOAD_TYPE,
        "payload": payload_b64,
        "signatures": [{"keyid": key_id, "sig": sig_b64}],
    }
    return envelope


def verify_dsse_attestation(
    envelope: Dict[str, Any],
    public_key: Union[Ed25519PublicKey, bytes],
) -> Dict[str, Any]:
    """Verify DSSE envelope signature and return decoded statement."""
    if isinstance(public_key, bytes):
        public_key = Ed25519PublicKey.from_public_bytes(public_key)
    payload_b64 = envelope.get("payload")
    if not payload_b64:
        raise RevaIntegrityError("Missing payload in DSSE envelope")

    try:
        payload_bytes = base64.b64decode(payload_b64)
    except Exception as e:
        raise RevaIntegrityError(f"Malformed base64 payload in DSSE envelope: {e}") from e

    # Verify attestation_id if provided
    expected_id = compute_attestation_id(payload_bytes)
    claimed_id = envelope.get("attestation_id")
    if claimed_id and claimed_id != expected_id:
        raise RevaIntegrityError(f"Attestation ID mismatch: claimed {claimed_id}, computed {expected_id}")

    signatures = envelope.get("signatures", [])
    if not signatures:
        raise RevaSignatureError("No signatures present in DSSE envelope")

    sig_b64 = signatures[0].get("sig", "")
    # Pad urlsafe base64
    padded_sig = sig_b64 + "=" * (-len(sig_b64) % 4)
    try:
        sig_raw = base64.urlsafe_b64decode(padded_sig)
    except Exception as e:
        raise RevaSignatureError(f"Malformed signature encoding: {e}") from e

    pae = compute_dsse_pae(envelope.get("payloadType", DSSE_PAYLOAD_TYPE), payload_bytes)
    try:
        public_key.verify(sig_raw, pae)
    except Exception as e:
        raise RevaSignatureError(f"DSSE attestation signature verification failed: {e}") from e

    return json.loads(payload_bytes.decode("utf-8"))
