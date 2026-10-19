"""Signed Tree Head (STH) generation, signing, and verification (T-120 / REVA-TL-002 / REVA-TL-004 / REVA-TL-005)."""

from __future__ import annotations

import base64
from typing import Any, Dict, Optional
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ed25519
from pydantic import BaseModel, Field

from reva.core.ids import sth_id as compute_sth_id
from reva.core.jcs import canonicalize
from reva.core.time import format_ts, utc_now_ms
from reva.kernel.signing import b64url_decode, b64url_encode
from reva.kernel.store import RevaStore
from reva.kernel.translog import TransparencyLog


STH_DOMAIN_PREFIX = b"REVA-STH-V1\n"


class SignedTreeHead(BaseModel):
    """Normative signed commitment to log state at a specific size."""

    sth_id: str
    log_id: str
    tree_size: int
    root_hash: str  # Hex string
    issued_at: str
    key_id: str
    signature: str  # Base64url signature


def issue_sth_now(
    store: RevaStore,
    log: TransparencyLog,
    key_id: str,
    priv_key: ed25519.Ed25519PrivateKey,
) -> SignedTreeHead:
    """Compute current Merkle Tree Head, sign it with log key, and store STH record."""
    tree_size = log.size()
    root_bytes = log.root(tree_size)
    root_hex = root_bytes.hex()
    now = format_ts(utc_now_ms())

    payload = {
        "issued_at": now,
        "key_id": key_id,
        "log_id": log.log_id,
        "root_hash": root_hex,
        "tree_size": tree_size,
    }
    canonical_bytes = canonicalize(payload)
    sid = compute_sth_id(payload)

    msg = STH_DOMAIN_PREFIX + canonical_bytes
    sig = priv_key.sign(msg)
    sig_b64url = b64url_encode(sig)

    cur = store.conn.cursor()
    cur.execute(
        """
        INSERT OR REPLACE INTO reva_sths (
            log_id, tree_size, root_hash, issued_at, key_id, signature, sth_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (log.log_id, tree_size, root_bytes, now, key_id, sig, sid),
    )
    store.conn.commit()

    return SignedTreeHead(
        sth_id=sid,
        log_id=log.log_id,
        tree_size=tree_size,
        root_hash=root_hex,
        issued_at=now,
        key_id=key_id,
        signature=sig_b64url,
    )


def verify_sth(sth: SignedTreeHead, pub_key_bytes: bytes) -> bool:
    """Verify cryptographic signature on an STH."""
    payload = {
        "issued_at": sth.issued_at,
        "key_id": sth.key_id,
        "log_id": sth.log_id,
        "root_hash": sth.root_hash.lower(),
        "tree_size": sth.tree_size,
    }
    canonical_bytes = canonicalize(payload)
    msg = STH_DOMAIN_PREFIX + canonical_bytes

    try:
        sig = b64url_decode(sth.signature)
        pub = ed25519.Ed25519PublicKey.from_public_bytes(pub_key_bytes)
        pub.verify(sig, msg)
        return True
    except (InvalidSignature, ValueError, Exception):
        return False
