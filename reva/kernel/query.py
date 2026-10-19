"""Retrieval, ACL filtering, tamper quarantine, and bitemporal queries (T-113 / REVA-WK-006 / REVA-WK-009 / REVA-SEC-002)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from reva.core.errors import RevaIntegrityError, RevaNotFoundError
from reva.core.ids import warrant_id as compute_warrant_id
from reva.core.time import format_ts, parse_ts, utc_now_ms
from reva.kernel.acl import Principal, is_authorized
from reva.kernel.signing import verify_warrant_signature
from reva.kernel.store import RevaStore
from reva.kernel.warrant import SealedWarrant, WarrantBody, WarrantEnvelope


def get_warrant(
    store: RevaStore,
    tenant_id: str,
    principal: Principal,
    warrant_id: str,
) -> SealedWarrant:
    """Fetch warrant, verify integrity and signature, enforce ACL, quarantine on corruption."""
    if store.is_quarantined(tenant_id, "warrant", warrant_id):
        raise RevaNotFoundError(
            f"Warrant not found: {warrant_id}",
            details={"warrant_id": warrant_id, "tenant_id": tenant_id},
        )

    row = store.get_warrant(tenant_id, warrant_id)
    if not row:
        raise RevaNotFoundError(
            f"Warrant not found: {warrant_id}",
            details={"warrant_id": warrant_id, "tenant_id": tenant_id},
        )

    body_dict, env_dict = row

    # 1. Integrity check: recompute warrant ID
    expected_wid = compute_warrant_id(body_dict)
    if expected_wid != warrant_id:
        store.quarantine_object(
            tenant_id,
            "warrant",
            warrant_id,
            "ID_BODY_DIGEST_MISMATCH",
            {"expected": expected_wid, "claimed": warrant_id},
        )
        raise RevaIntegrityError(
            f"Warrant {warrant_id} integrity mismatch with body digest",
            details={"warrant_id": warrant_id, "expected": expected_wid},
        )

    # 2. Cryptographic signature check
    sig_obj = env_dict.get("signature")
    if isinstance(sig_obj, dict):
        sig = sig_obj.get("sig")
        key_id = sig_obj.get("key_id")
    else:
        sig = env_dict.get("sig")
        key_id = env_dict.get("key_id")

    if not sig or not key_id:
        store.quarantine_object(
            tenant_id,
            "warrant",
            warrant_id,
            "MISSING_SIGNATURE_OR_KEY",
            {"key_id": key_id},
        )
        raise RevaIntegrityError(f"Warrant {warrant_id} missing signature or key")


    key_record = store.get_key(key_id)
    if not key_record:
        store.quarantine_object(
            tenant_id,
            "warrant",
            warrant_id,
            "UNKNOWN_KEY",
            {"key_id": key_id},
        )
        raise RevaIntegrityError(f"Warrant {warrant_id} signed by unknown key {key_id}")

    # Check key revocation at warrant recorded_at time
    recorded_at = env_dict.get("recorded_at")
    revoked_at = key_record.get("revoked_at")
    if key_record.get("status") == "revoked" and revoked_at and recorded_at:
        if parse_ts(recorded_at) >= parse_ts(revoked_at):
            store.quarantine_object(
                tenant_id,
                "warrant",
                warrant_id,
                "KEY_REVOKED_PRIOR_TO_RECORDING",
                {"key_id": key_id, "revoked_at": revoked_at, "recorded_at": recorded_at},
            )
            raise RevaIntegrityError(f"Key {key_id} was revoked prior to warrant issuance")

    public_key = key_record["public_key"]
    if not verify_warrant_signature(warrant_id, sig, public_key):
        store.quarantine_object(
            tenant_id,
            "warrant",
            warrant_id,
            "SIGNATURE_INVALID",
            {"key_id": key_id},
        )
        raise RevaIntegrityError(f"Warrant {warrant_id} signature invalid")

    # 3. Access control list authorization
    if not is_authorized(env_dict, principal):
        # Do not leak existence of unauthorized warrants
        raise RevaNotFoundError(
            f"Warrant not found: {warrant_id}",
            details={"warrant_id": warrant_id, "tenant_id": tenant_id},
        )

    return SealedWarrant(
        warrant_id=warrant_id,
        body=WarrantBody.model_validate(body_dict),
        envelope=WarrantEnvelope.model_validate(env_dict),
    )


def query_warrants(
    store: RevaStore,
    tenant_id: str,
    principal: Principal,
    subject_key: Optional[str] = None,
    predicate: Optional[str] = None,
    producer_id: Optional[str] = None,
    authority: Optional[str] = None,
    epistemic: Optional[str] = None,
    status: Optional[str] = None,
    min_confidence_bp: Optional[int] = None,
    classification: Optional[str] = None,
    as_of_valid: Optional[str] = None,
    as_of_recorded: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[SealedWarrant]:
    """Bitemporal search with full ACL filtering and verification."""
    raw_results = store.search_warrants(
        tenant_id=tenant_id,
        subject_key=subject_key,
        predicate=predicate,
        producer_id=producer_id,
        authority=authority,
        epistemic=epistemic,
        status=status,
        min_confidence_bp=min_confidence_bp,
        classification=classification,
        as_of_valid=as_of_valid,
        as_of_recorded=as_of_recorded,
        limit=limit,
        offset=offset,
    )

    verified: List[SealedWarrant] = []
    for body_dict, env_dict in raw_results:
        wid = env_dict.get("warrant_id") or body_dict.get("warrant_id")
        if not wid:
            continue
        if store.is_quarantined(tenant_id, "warrant", wid):
            continue
        if not is_authorized(env_dict, principal):
            continue

        # Verify integrity and signature
        if compute_warrant_id(body_dict) != wid:
            store.quarantine_object(tenant_id, "warrant", wid, "ID_MISMATCH")
            continue

        sig_obj = env_dict.get("signature")
        if isinstance(sig_obj, dict):
            sig = sig_obj.get("sig")
            key_id = sig_obj.get("key_id")
        else:
            sig = env_dict.get("sig")
            key_id = env_dict.get("key_id")

        if not key_id or not sig:
            store.quarantine_object(tenant_id, "warrant", wid, "MISSING_KEY_OR_SIG")
            continue

        key_record = store.get_key(key_id)
        if not key_record:
            store.quarantine_object(tenant_id, "warrant", wid, "UNKNOWN_KEY")
            continue

        if not verify_warrant_signature(wid, sig, key_record["public_key"]):
            store.quarantine_object(tenant_id, "warrant", wid, "SIGNATURE_INVALID")
            continue


        verified.append(
            SealedWarrant(
                warrant_id=wid,
                body=WarrantBody.model_validate(body_dict),
                envelope=WarrantEnvelope.model_validate(env_dict),
            )
        )

    return verified
