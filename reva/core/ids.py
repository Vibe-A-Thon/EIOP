"""Prefixed identifier derivation and verification according to REVA §6.2 (T-102 / REVA-WK-002)."""

from __future__ import annotations

import re
import unicodedata
from typing import Any, Dict, List, Tuple
from collections.abc import Sequence

from reva.core.digest import sha256_canonical, sha256_hex
from reva.core.jcs import canonicalize

ID_PATTERN = re.compile(r"^([a-z]+)([0-9]+)_([0-9a-f]{64})$")


def normalize_question(q: str) -> str:
    """Normalize question text: NFKC, stripped, whitespace collapsed, lowercase."""
    text = unicodedata.normalize("NFKC", q)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def normalize_set(items: Sequence[Any]) -> List[Any]:
    """Sort and deduplicate a sequence by its canonical JSON bytes."""
    seen = set()
    unique_items = []
    for item in items:
        raw = item.model_dump(by_alias=True, mode="json") if hasattr(item, "model_dump") else item
        b = canonicalize(raw, allow_float=False)
        if b not in seen:
            seen.add(b)
            unique_items.append((b, item))
    unique_items.sort(key=lambda t: t[0])
    return [t[1] for t in unique_items]


def parse_id(id_str: str) -> Tuple[str, str, str]:
    """Parse an ID into (prefix, version, hex) or raise ValueError."""
    m = ID_PATTERN.match(id_str)
    if not m:
        raise ValueError(f"Malformed REVA identifier '{id_str}', expected <prefix><ver>_<64hex>")
    return m.group(1), m.group(2), m.group(3)


def is_valid_id(id_str: str, expected_prefix: str | None = None) -> bool:
    """Validate syntax of a REVA identifier."""
    m = ID_PATTERN.match(id_str)
    if not m:
        return False
    if expected_prefix and m.group(1) != expected_prefix:
        return False
    return True


def warrant_id(body: Dict[str, Any]) -> str:
    return "wr1_" + sha256_canonical(body)


def artifact_id(sha256_digest: str) -> str:
    return "art1_" + sha256_digest.lower()


def blob_id(sha256_digest: str) -> str:
    return "blb1_" + sha256_digest.lower()


def gap_id(tenant_id: str, domain: str, question: str, scope: Any) -> str:
    q_norm = normalize_question(question)
    payload = {
        "domain": domain,
        "question_normalized": q_norm,
        "scope": scope,
        "tenant_id": tenant_id,
    }
    return "gap1_" + sha256_canonical(payload)


def contradiction_id(tenant_id: str, conflict_key: Any, member_warrant_ids: Sequence[str]) -> str:
    payload = {
        "conflict_key": conflict_key,
        "member_warrant_ids": sorted(list(set(member_warrant_ids))),
        "tenant_id": tenant_id,
    }
    return "cx1_" + sha256_canonical(payload)


def obligation_digest(definition: Dict[str, Any]) -> str:
    return "obl1_" + sha256_canonical(definition)


def binding_digest(binding: Dict[str, Any]) -> str:
    return "bnd1_" + sha256_canonical(binding)


def verifier_run_id(run_record_unsigned: Dict[str, Any]) -> str:
    return "vr1_" + sha256_canonical(run_record_unsigned)


def attestation_id(dsse_payload_bytes: bytes) -> str:
    return "att1_" + sha256_hex(dsse_payload_bytes)


def closure_id(decision_body: Dict[str, Any]) -> str:
    return "cls1_" + sha256_canonical(decision_body)


def ledger_id(scope: str, closure_decision_ids: Sequence[str]) -> str:
    payload = {
        "closure_decision_ids": sorted(list(set(closure_decision_ids))),
        "scope": scope,
    }
    return "ldg1_" + sha256_canonical(payload)


def bundle_id(manifest: Dict[str, Any]) -> str:
    return "bun1_" + sha256_canonical(manifest)


def sth_id(sth_body: Dict[str, Any]) -> str:
    return "sth1_" + sha256_canonical(sth_body)


def entity_id(tenant_id: str, entity_type: str, logical_key: str) -> str:
    payload = {
        "entity_type": entity_type,
        "logical_key": logical_key,
        "tenant_id": tenant_id,
    }
    return "ent1_" + sha256_canonical(payload)


def entity_version_id(ent_id: str, version_basis: str, version_digest: str) -> str:
    payload = {
        "entity_id": ent_id,
        "version_basis": version_basis,
        "version_digest": version_digest,
    }
    return "ver1_" + sha256_canonical(payload)


def trace_id(trace_body: Dict[str, Any]) -> str:
    return "trc1_" + sha256_canonical(trace_body)


def diff_id(diff_body: Dict[str, Any]) -> str:
    return "dif1_" + sha256_canonical(diff_body)


def view_id(parent_id: str, view_request: Any, page: int) -> str:
    payload = {
        "page": page,
        "parent_id": parent_id,
        "view_request": view_request,
    }
    return "vw1_" + sha256_canonical(payload)


def producer_id(tenant_id: str, producer_type: str, name: str, version: str) -> str:
    payload = {
        "name": name,
        "producer_type": producer_type,
        "tenant_id": tenant_id,
        "version": version,
    }
    return "prd1_" + sha256_canonical(payload)


def key_id(raw_ed25519_public_key_bytes: bytes) -> str:
    return "key1_" + sha256_hex(raw_ed25519_public_key_bytes)


def schema_id(body: Dict[str, Any]) -> str:
    """Derive deterministic Neural Schema identifier sch1_[0-9a-f]{64}."""
    return "sch1_" + sha256_canonical(body)


def constitution_id(body: Dict[str, Any]) -> str:
    """Derive deterministic Living AI Agent Constitution identifier con1_[0-9a-f]{64}."""
    return "con1_" + sha256_canonical(body)


def budget_id(body: Dict[str, Any]) -> str:
    """Derive deterministic Autonomy Budget identifier bdg1_[0-9a-f]{64}."""
    return "bdg1_" + sha256_canonical(body)
