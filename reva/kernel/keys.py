"""Ed25519 key management, key derivation, and AES-256-GCM encryption at rest (T-107 / REVA-WK-010 / REVA-SEC-007)."""

from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Tuple

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from reva.core.ids import key_id
from reva.core.time import format_ts, utc_now_ms


@dataclass
class KeyRecord:
    key_id: str
    tenant_id: str
    owner_kind: str  # producer | log | verifier | pd | continuation | pii
    owner_id: str
    public_key_bytes: bytes
    private_key_enc: bytes  # nonce (12) + ciphertext + tag (16)
    status: str             # active | verify_only | revoked
    activated_at: str
    revoked_at: Optional[str] = None


def generate_keypair() -> Tuple[ed25519.Ed25519PrivateKey, bytes, str]:
    """Generate fresh Ed25519 private key, raw public bytes, and key1_ ID."""
    priv = ed25519.Ed25519PrivateKey.generate()
    pub = priv.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    kid = key_id(pub)
    return priv, pub, kid


def encrypt_private_key(priv: ed25519.Ed25519PrivateKey, kek_b64: str) -> bytes:
    """Encrypt raw private key bytes with AES-256-GCM using base64 KEK."""
    raw_kek = base64.b64decode(kek_b64)
    if len(raw_kek) != 32:
        raise ValueError(f"KEK must be 32 bytes, got {len(raw_kek)}")

    priv_raw = priv.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    nonce = os.urandom(12)
    aesgcm = AESGCM(raw_kek)
    ct = aesgcm.encrypt(nonce, priv_raw, None)
    return nonce + ct


from reva.config import get_settings


def generate_key(store: Any, tenant_id: str, owner_kind: str, owner_id: str) -> KeyRecord:
    """Generate and store an Ed25519 key wrapped with REVA_KEK."""
    settings = get_settings()
    priv, pub, kid = generate_keypair()
    enc_priv = encrypt_private_key(priv, settings.kek)
    now = format_ts(utc_now_ms())
    store.save_key(
        key_id=kid,
        tenant_id=tenant_id,
        owner_kind=owner_kind,
        owner_id=owner_id,
        public_key=pub,
        private_key_enc=enc_priv,
        status="active",
        activated_at=now,
    )
    return KeyRecord(
        key_id=kid,
        tenant_id=tenant_id,
        owner_kind=owner_kind,
        owner_id=owner_id,
        public_key_bytes=pub,
        private_key_enc=enc_priv,
        status="active",
        activated_at=now,
    )


def decrypt_private_key(enc_bytes: bytes, kek_b64: Optional[str] = None) -> ed25519.Ed25519PrivateKey:
    """Decrypt encrypted private key bytes with AES-256-GCM using base64 KEK."""
    actual_kek = kek_b64 or get_settings().kek
    raw_kek = base64.b64decode(actual_kek)
    if len(raw_kek) != 32:
        raise ValueError(f"KEK must be 32 bytes, got {len(raw_kek)}")

    nonce = enc_bytes[:12]
    ct = enc_bytes[12:]
    aesgcm = AESGCM(raw_kek)
    priv_raw = aesgcm.decrypt(nonce, ct, None)
    return ed25519.Ed25519PrivateKey.from_private_bytes(priv_raw)

