"""Shared environment configuration for Docker processes."""

import hashlib
import os
from pathlib import Path

from eoip.graph.backends import create_graph_store


def create_store():
    return create_graph_store()


def data_root():
    return Path(os.getenv("EOIP_DATA_DIR", "/data"))


MIN_API_TOKEN_LENGTH = 32


def _revoked_token_digests():
    path = os.getenv("EOIP_REVOKED_TOKEN_SHA256_FILE")
    if not path:
        return set()
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise RuntimeError("EOIP_REVOKED_TOKEN_SHA256_FILE is set but unreadable") from exc
    return {line.strip().lower().removeprefix("sha256:") for line in lines if line.strip() and not line.startswith("#")}


def api_token():
    """Return the injected bootstrap token or refuse to start (fail closed, FT-F02)."""
    value = os.getenv("EOIP_API_TOKEN", "")
    if len(value) < MIN_API_TOKEN_LENGTH:
        raise RuntimeError(
            f"EOIP_API_TOKEN must contain at least {MIN_API_TOKEN_LENGTH} characters; "
            "inject it from the secret store (scripts/container.ps1 generates one for local Docker)"
        )
    if hashlib.sha256(value.encode("utf-8")).hexdigest() in _revoked_token_digests():
        raise RuntimeError("EOIP_API_TOKEN is revoked; inject a new value from the secret store")
    return value
