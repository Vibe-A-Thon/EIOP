"""Package signing and integrity (GAP-MKT-007, GAP-EXT-001).

Integrity is an HMAC-SHA256 signature over the archive bytes, verified with a
shared install key (``EOIP_INSTALL_KEY`` env var or an explicitly supplied
key). This detects tampering/corruption for internal packages; asymmetric
signature verification (per-publisher public keys) is a later phase and noted
in §45.
"""

from __future__ import annotations

import hashlib
import hmac
import os

SIGNATURE_FILENAME = "signature.bin"
ENV_INSTALL_KEY = "EOIP_INSTALL_KEY"


def default_install_key() -> bytes:
    """Resolve the shared install key from the environment (GAP-MKT-007)."""

    key = os.environ.get(ENV_INSTALL_KEY)
    if not key:
        raise RuntimeError(
            f"no install key configured; set {ENV_INSTALL_KEY} or pass key= explicitly"
        )
    return key.encode("utf-8")


def sign(data: bytes, key: bytes) -> bytes:
    """HMAC-SHA256 signature over raw archive bytes."""

    return hmac.new(key, data, hashlib.sha256).digest()


def verify_signature(data: bytes, signature: bytes, key: bytes) -> bool:
    """Constant-time HMAC verification (GAP-MKT-007)."""

    expected = sign(data, key)
    return hmac.compare_digest(expected, signature)
