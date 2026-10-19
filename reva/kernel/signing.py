"""Ed25519 signing and verification utilities for warrants and attestations (T-107 / REVA-WK-010)."""

from __future__ import annotations

import base64
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

WARRANT_SIGN_PREFIX = b"REVA-WARRANT-V1\n"
ATTESTATION_SIGN_PREFIX = b"REVA-ATTESTATION-V1\n"


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def b64url_decode(s: str) -> bytes:
    padding = 4 - (len(s) % 4)
    if padding < 4:
        s += "=" * padding
    return base64.urlsafe_b64decode(s)


def sign_warrant_id(w_id: str, priv_key: ed25519.Ed25519PrivateKey) -> str:
    """Sign 'REVA-WARRANT-V1\\n' + warrant_id and return base64url signature."""
    msg = WARRANT_SIGN_PREFIX + w_id.encode("ascii")
    sig = priv_key.sign(msg)
    return b64url_encode(sig)


def verify_warrant_signature(w_id: str, sig_b64url: str, pub_key_bytes: bytes) -> bool:
    """Verify base64url signature over 'REVA-WARRANT-V1\\n' + warrant_id."""
    try:
        sig = b64url_decode(sig_b64url)
        pub = ed25519.Ed25519PublicKey.from_public_bytes(pub_key_bytes)
        msg = WARRANT_SIGN_PREFIX + w_id.encode("ascii")
        pub.verify(sig, msg)
        return True
    except (InvalidSignature, ValueError, Exception):
        return False


def sign_attestation_payload(payload_bytes: bytes, priv_key: ed25519.Ed25519PrivateKey) -> str:
    """Sign DSSE attestation payload."""
    msg = ATTESTATION_SIGN_PREFIX + payload_bytes
    sig = priv_key.sign(msg)
    return b64url_encode(sig)


def verify_attestation_payload(payload_bytes: bytes, sig_b64url: str, pub_key_bytes: bytes) -> bool:
    """Verify DSSE attestation signature."""
    try:
        sig = b64url_decode(sig_b64url)
        pub = ed25519.Ed25519PublicKey.from_public_bytes(pub_key_bytes)
        msg = ATTESTATION_SIGN_PREFIX + payload_bytes
        pub.verify(sig, msg)
        return True
    except (InvalidSignature, ValueError, Exception):
        return False
