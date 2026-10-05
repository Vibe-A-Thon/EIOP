"""HMAC-SHA256 signed bearer tokens, stdlib only (GAP-SEC-007..009, §27).

No PyJWT/cryptography dependency is declared in pyproject.toml, so tokens
are compact HMAC-signed JSON blobs: ``base64url(payload).base64url(sig)``.
Verification is constant-time and fail-closed: any malformed, expired,
or wrongly-signed token is rejected (GAP-SEC-008).
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time


class TokenError(Exception):
    """Raised when a token cannot be verified (fail-closed, GAP-SEC-008)."""


def _b64encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64decode(data: str) -> bytes:
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)


def default_secret() -> str:
    """Env-provided signing secret; ephemeral random fallback (GAP-SEC-009)."""
    return os.getenv("EOIP_AUTHZ_TOKEN_SECRET", "")


class TokenSigner:
    """Issues and verifies HMAC-SHA256 signed tokens (GAP-SEC-007)."""

    def __init__(self, secret: str | None = None, *, ttl_seconds: int = 3600) -> None:
        self._secret = (secret if secret is not None else default_secret()).encode("utf-8")
        if not self._secret:
            self._secret = os.urandom(32)
        self._ttl = ttl_seconds

    def _signature(self, payload_b64: str) -> bytes:
        return hmac.new(self._secret, payload_b64.encode("ascii"), hashlib.sha256).digest()

    def issue(self, subject: str, *, roles: list[str] | None = None, ttl_seconds: int | None = None) -> str:
        now = int(time.time())
        payload = {
            "sub": subject,
            "roles": list(roles or []),
            "iat": now,
            "exp": now + (ttl_seconds if ttl_seconds is not None else self._ttl),
        }
        payload_b64 = _b64encode(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"))
        sig_b64 = _b64encode(self._signature(payload_b64))
        return f"{payload_b64}.{sig_b64}"

    def verify(self, token: str) -> dict:
        """Return the payload or raise TokenError (fail-closed, GAP-SEC-008)."""
        try:
            payload_b64, sig_b64 = token.split(".")
        except ValueError as exc:
            raise TokenError("malformed token") from exc
        expected = self._signature(payload_b64)
        provided = _b64decode(sig_b64)
        if not hmac.compare_digest(expected, provided):
            raise TokenError("invalid signature")
        try:
            payload = json.loads(_b64decode(payload_b64))
        except (ValueError, json.JSONDecodeError) as exc:
            raise TokenError("invalid payload") from exc
        if int(payload.get("exp", 0)) < int(time.time()):
            raise TokenError("token expired")
        return payload
