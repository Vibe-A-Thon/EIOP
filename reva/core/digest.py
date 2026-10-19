"""Digest helpers for REVA (T-102 / REVA-WK-002)."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from reva.core.jcs import canonicalize


def sha256_hex(data: bytes) -> str:
    """Return SHA-256 hex string for given bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path | str, chunk_size: int = 1024 * 1024) -> str:
    """Stream file and compute its SHA-256 hex digest."""
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def sha256_canonical(obj: Any, *, allow_float: bool = False) -> str:
    """Compute SHA-256 digest of object serialized with RFC 8785 canonical JSON."""
    return sha256_hex(canonicalize(obj, allow_float=allow_float))
