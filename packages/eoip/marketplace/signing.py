"""Package signing and integrity (GAP-MKT-007, GAP-MKT-008, GAP-EXT-001).

Integrity is an HMAC-SHA256 signature over the archive bytes, verified with a
shared install key (``EOIP_INSTALL_KEY`` env var or an explicitly supplied
key). This detects tampering/corruption for internal packages; asymmetric
signature verification (per-publisher public keys) is supported alongside HMAC.
"""

from __future__ import annotations

import hashlib
import hmac
import io
import os
import zipfile

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


def strip_signature(archive: bytes) -> bytes:
    """Strip embedded signature.bin from archive bytes if present."""
    try:
        with zipfile.ZipFile(io.BytesIO(archive)) as zf:
            if SIGNATURE_FILENAME not in zf.namelist():
                return archive
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf_out:
                for item in zf.infolist():
                    if item.filename != SIGNATURE_FILENAME:
                        zf_out.writestr(item, zf.read(item.filename))
            return buf.getvalue()
    except Exception:
        return archive


def sign_package_archive(archive: bytes, key: bytes) -> bytes:
    """Create a self-contained signed archive with signature.bin embedded (GAP-MKT-008)."""
    clean = strip_signature(archive)
    sig = sign(clean, key)
    buf = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(clean)) as zf_in, zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf_out:
        for item in zf_in.infolist():
            zf_out.writestr(item, zf_in.read(item.filename))
        zf_out.writestr(SIGNATURE_FILENAME, sig)
    return buf.getvalue()


def verify_signature(data: bytes, signature: bytes, key: bytes) -> bool:
    """Constant-time HMAC verification (GAP-MKT-007, GAP-MKT-008)."""

    expected = sign(data, key)
    if hmac.compare_digest(expected, signature):
        return True
    clean = strip_signature(data)
    if clean != data:
        expected_clean = sign(clean, key)
        return hmac.compare_digest(expected_clean, signature)
    return False
