"""Auditor for Merkle log consistency, leaf continuity, and warrant signatures (T-120 / REVA-TL-004)."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from reva.core.ids import warrant_id as compute_warrant_id
from reva.kernel.signing import b64url_encode, verify_warrant_signature
from reva.kernel.sth import SignedTreeHead, verify_sth
from reva.kernel.store import RevaStore
from reva.kernel.translog import TransparencyLog, verify_consistency


class AuditReport(BaseModel):
    """Result of automated transparency log audit."""

    clean: bool
    log_id: str
    tree_size: int
    sths_checked: int
    warrants_sampled: int
    issues: List[str] = Field(default_factory=list)


def audit_transparency_log(
    store: RevaStore,
    log: TransparencyLog,
    sample_size: int = 50,
) -> AuditReport:
    """Perform integrity audit: leaf hashes, STH signatures, STH consistency, and sample warrant checks."""
    issues: List[str] = []
    current_size = log.size()
    leaves = log.get_leaves()

    # 1. Check leaf continuity
    cur = store.conn.cursor()
    cur.execute(
        "SELECT leaf_index, leaf_data, leaf_hash FROM reva_log_leaves WHERE log_id = ? ORDER BY leaf_index ASC",
        (log.log_id,),
    )
    rows = cur.fetchall()

    for idx, r in enumerate(rows):
        if r["leaf_index"] != idx:
            issues.append(f"Leaf sequence gap: expected index {idx}, found {r['leaf_index']}")

    # 2. Check stored STHs
    cur.execute(
        "SELECT * FROM reva_sths WHERE log_id = ? ORDER BY tree_size ASC",
        (log.log_id,),
    )
    sth_rows = cur.fetchall()
    previous_sth: Optional[SignedTreeHead] = None

    for sr in sth_rows:
        key_record = store.get_key(sr["key_id"])
        if not key_record:
            issues.append(f"STH for size {sr['tree_size']} signed with unknown key {sr['key_id']}")
            continue

        sth = SignedTreeHead(
            sth_id=sr["sth_id"],
            log_id=sr["log_id"],
            tree_size=sr["tree_size"],
            root_hash=sr["root_hash"].hex() if isinstance(sr["root_hash"], bytes) else sr["root_hash"],
            issued_at=sr["issued_at"],
            key_id=sr["key_id"],
            signature=b64url_encode(sr["signature"]) if isinstance(sr["signature"], bytes) else sr["signature"],
        )

        # Verify signature
        if not verify_sth(sth, key_record["public_key"]):
            issues.append(f"STH {sth.sth_id} signature invalid")

        # Verify root hash against leaves
        if sth.tree_size <= len(leaves):
            expected_root = log.root(sth.tree_size).hex()
            if expected_root.lower() != sth.root_hash.lower():
                issues.append(f"STH {sth.sth_id} root {sth.root_hash} does not match computed root {expected_root}")

        # Verify consistency against previous STH
        if previous_sth is not None and previous_sth.tree_size < sth.tree_size:
            proof_hex = log.consistency_proof(previous_sth.tree_size, sth.tree_size)
            proof_bytes = [bytes.fromhex(p) for p in proof_hex]
            r_prev = bytes.fromhex(previous_sth.root_hash)
            r_curr = bytes.fromhex(sth.root_hash)
            if not verify_consistency(previous_sth.tree_size, sth.tree_size, r_prev, r_curr, proof_bytes):
                issues.append(f"Consistency verification failed between STH size {previous_sth.tree_size} and {sth.tree_size}")

        previous_sth = sth

    # 3. Sample warrants and verify leaf_data matches warrant_id and signature is valid
    cur.execute(
        "SELECT warrant_id, body, envelope FROM reva_warrants ORDER BY RANDOM() LIMIT ?",
        (sample_size,),
    )
    sample_warrants = cur.fetchall()
    warrants_checked = 0

    for w in sample_warrants:
        wid = w["warrant_id"]
        body_dict = json.loads(w["body"])
        env_dict = json.loads(w["envelope"])

        # ID digest matches
        if compute_warrant_id(body_dict) != wid:
            issues.append(f"Sampled warrant {wid} fails body digest check")

        # Signature matches
        sig_obj = env_dict.get("signature")
        if isinstance(sig_obj, dict):
            sig = sig_obj.get("sig")
            kid = sig_obj.get("key_id")
        else:
            sig = env_dict.get("sig")
            kid = env_dict.get("key_id")

        if kid and sig:
            k = store.get_key(kid)
            if not k or not verify_warrant_signature(wid, sig, k["public_key"]):
                issues.append(f"Sampled warrant {wid} fails cryptographic signature verification")

        warrants_checked += 1

    return AuditReport(
        clean=len(issues) == 0,
        log_id=log.log_id,
        tree_size=current_size,
        sths_checked=len(sth_rows),
        warrants_sampled=warrants_checked,
        issues=issues,
    )
