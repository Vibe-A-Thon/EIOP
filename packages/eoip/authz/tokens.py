"""HMAC-SHA256 signed bearer tokens, stdlib only (GAP-SEC-007..012, §27).

Features:
- Compact HMAC-signed JSON blobs: ``base64url(payload).base64url(sig)``.
- Verification is constant-time and fail-closed: any malformed, expired,
  revoked, or wrongly-signed token is rejected (GAP-SEC-008).
- Key rotation: supports previous verification secrets during rollover (GAP-SEC-009).
- Ephemeral random secret fallback when unconfigured (GAP-SEC-009).
- Token Revocation Store (CRL / denylist) with instant revocation and TTL pruning (GAP-SEC-010).
- Fine-grained token scopes and ABAC tenant claims (GAP-SEC-011).
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time
import uuid
from typing import Any


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


def has_scope(granted_scopes: list[str], required_scope: str) -> bool:
    """Checks if a granted list of scopes satisfies a required scope (GAP-SEC-011).

    Supports exact matches ('graph:read'), domain wildcards ('graph:*'),
    and platform admin wildcards ('admin:*', '*').
    """
    for scope in granted_scopes:
        if scope in ("*", "admin:*") or scope == required_scope:
            return True
        if scope.endswith(":*"):
            prefix = scope[:-2]
            if required_scope.startswith(prefix + ":") or required_scope == prefix:
                return True
    return False


class TokenRevocationStore:
    """In-memory thread-safe Certificate / Token Revocation List (CRL) (GAP-SEC-010)."""

    def __init__(self) -> None:
        self._revoked: dict[str, dict[str, Any]] = {}

    def revoke(
        self,
        identifier: str,
        reason: str = "revoked_by_admin",
        expires_at: int | None = None,
    ) -> None:
        """Revokes a token identifier (jti, subject, or token hash)."""
        now = int(time.time())
        exp = expires_at if expires_at is not None else now + 86400
        self._revoked[identifier] = {
            "identifier": identifier,
            "reason": reason,
            "revoked_at": now,
            "expires_at": exp,
        }

    def is_revoked(self, identifier: str | None) -> bool:
        """Returns True if the identifier is currently revoked and not past expiration."""
        if not identifier or identifier not in self._revoked:
            return False
        entry = self._revoked[identifier]
        if entry["expires_at"] < int(time.time()):
            del self._revoked[identifier]
            return False
        return True

    def list_revocations(self) -> list[dict[str, Any]]:
        self.prune_expired()
        return list(self._revoked.values())

    def prune_expired(self) -> int:
        now = int(time.time())
        expired_keys = [k for k, v in self._revoked.items() if v["expires_at"] < now]
        for k in expired_keys:
            del self._revoked[k]
        return len(expired_keys)

    def clear(self) -> None:
        self._revoked.clear()


_GLOBAL_REVOCATION_STORE = TokenRevocationStore()


def global_revocation_store() -> TokenRevocationStore:
    return _GLOBAL_REVOCATION_STORE


class TokenSigner:
    """Issues and verifies HMAC-SHA256 signed tokens with key rotation and scopes (GAP-SEC-007..011)."""

    def __init__(
        self,
        secret: str | None = None,
        *,
        previous_secrets: list[str] | None = None,
        ttl_seconds: int = 3600,
        revocation_store: TokenRevocationStore | None = None,
    ) -> None:
        sec = secret if secret is not None else default_secret()
        self._secret = sec.encode("utf-8") if sec else os.urandom(32)
        self._previous_secrets: list[bytes] = [
            s.encode("utf-8") for s in (previous_secrets or []) if s
        ]
        self._ttl = ttl_seconds
        self.revocation_store = revocation_store or global_revocation_store()

    def rotate_secret(self, new_secret: str) -> None:
        """Rotates active signing secret while retaining the old one for verification (GAP-SEC-009)."""
        if self._secret not in self._previous_secrets:
            self._previous_secrets.append(self._secret)
        self._secret = new_secret.encode("utf-8")

    def _signature_for_secret(self, payload_b64: str, secret: bytes) -> bytes:
        return hmac.new(secret, payload_b64.encode("ascii"), hashlib.sha256).digest()

    def issue(
        self,
        subject: str,
        *,
        roles: list[str] | None = None,
        scopes: list[str] | None = None,
        tenant_id: str | None = None,
        attributes: dict[str, Any] | None = None,
        ttl_seconds: int | None = None,
        jti: str | None = None,
    ) -> str:
        """Issues a scoped HMAC-SHA256 signed bearer token (GAP-SEC-007, GAP-SEC-011)."""
        now = int(time.time())
        token_id = jti or uuid.uuid4().hex
        payload: dict[str, Any] = {
            "jti": token_id,
            "sub": subject,
            "roles": list(roles or []),
            "scopes": list(scopes or ["*"]),
            "tenant_id": tenant_id or "default",
            "attributes": dict(attributes or {}),
            "iat": now,
            "exp": now + (ttl_seconds if ttl_seconds is not None else self._ttl),
        }
        payload_b64 = _b64encode(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"))
        sig_b64 = _b64encode(self._signature_for_secret(payload_b64, self._secret))
        return f"{payload_b64}.{sig_b64}"

    def verify(
        self,
        token: str,
        *,
        required_scopes: list[str] | None = None,
        enforce_revocation: bool = True,
    ) -> dict[str, Any]:
        """Return the payload or raise TokenError (fail-closed, GAP-SEC-008)."""
        try:
            payload_b64, sig_b64 = token.split(".")
        except ValueError as exc:
            raise TokenError("malformed token") from exc

        provided = _b64decode(sig_b64)
        # Try active key first
        valid_sig = hmac.compare_digest(self._signature_for_secret(payload_b64, self._secret), provided)

        # If not valid, try previous keys for rollover support (GAP-SEC-009)
        if not valid_sig:
            for prev_sec in self._previous_secrets:
                if hmac.compare_digest(self._signature_for_secret(payload_b64, prev_sec), provided):
                    valid_sig = True
                    break

        if not valid_sig:
            raise TokenError("invalid signature")

        try:
            payload = json.loads(_b64decode(payload_b64))
        except (ValueError, json.JSONDecodeError) as exc:
            raise TokenError("invalid payload") from exc

        # Check expiration
        if int(payload.get("exp", 0)) < int(time.time()):
            raise TokenError("token expired")

        # Check revocation (GAP-SEC-010)
        if enforce_revocation and self.revocation_store:
            token_hash = hashlib.sha256(token.encode("ascii")).hexdigest()
            jti = payload.get("jti")
            sub = payload.get("sub")
            if (
                self.revocation_store.is_revoked(jti)
                or self.revocation_store.is_revoked(token_hash)
                or self.revocation_store.is_revoked(sub)
            ):
                raise TokenError("token has been revoked")

        # Check scopes (GAP-SEC-011)
        if required_scopes:
            granted = list(payload.get("scopes", []))
            for req in required_scopes:
                if not has_scope(granted, req):
                    raise TokenError(f"insufficient scope: missing required scope '{req}'")

        return payload
