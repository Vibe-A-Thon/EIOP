"""Per-user credentials: argon2id passwords, sessions, per-principal API tokens (FT-AUTH).

There is no default or bootstrap account and no implicit role. Every principal is
provisioned explicitly (``eoip-admin``, see :mod:`eoip.authn.provision`) and its roles
are stored with it. Authentication paths:

* **Login credentials (primary)** -- username + password verified against an argon2id
  hash; a successful login returns a signed, expiring session token. Each request with a
  session token re-reads the user record, so disabling a user or changing roles takes
  effect immediately (roles are never trusted from the token itself).
* **API tokens** -- opaque random tokens mapped to one principal with their own role
  set (a subset of the principal's roles). Only a sha256 digest is stored.

The store is a JSON file (mode 0600) under ``<EOIP_DATA_DIR>/state/credentials.json``
or ``EOIP_CREDENTIALS_FILE``. Passwords, hashes and token values are never logged.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import secrets
import tempfile
import threading
import time
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Any

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from eoip.authn import Principal, TokenError, TokenService

VALID_ROLES = frozenset({"superadmin", "admin", "system", "steward", "analyst", "viewer"})
MIN_PASSWORD_LENGTH = 12
MIN_SECRET_LENGTH = 32
API_TOKEN_PREFIX = "eoip_pat_"
CREDENTIALS_FILE_ENV = "EOIP_CREDENTIALS_FILE"
SESSION_SECRET_ENV = "EOIP_SESSION_SECRET"
SESSION_TTL_ENV = "EOIP_SESSION_TTL_SECONDS"
_USERNAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._@-]{0,127}$")
_HASHER = PasswordHasher()  # argon2id, RFC 9106 low-memory profile defaults
_DUMMY_HASH = _HASHER.hash(secrets.token_urlsafe(24))


class CredentialError(ValueError):
    """Invalid provisioning request (bad username, weak password, unknown role...)."""


def expand_roles(roles) -> tuple[str, ...]:
    """superadmin implies admin + system so existing role gates keep working."""
    out = {str(r).strip() for r in roles if r and str(r).strip()}
    if "superadmin" in out:
        out.update(("admin", "system"))
    return tuple(sorted(out))


def _check_roles(roles) -> tuple[str, ...]:
    expanded = expand_roles(roles)
    if not expanded:
        raise CredentialError("at least one role is required (there is no default role)")
    unknown = set(expanded) - VALID_ROLES
    if unknown:
        raise CredentialError(f"unknown role(s): {', '.join(sorted(unknown))}")
    return expanded


def token_sha256(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


@dataclass
class ApiTokenRecord:
    token_id: str
    sha256: str
    roles: list[str]
    label: str = ""
    created_at: float = field(default_factory=time.time)
    revoked: bool = False

    def __repr__(self) -> str:
        return f"ApiTokenRecord(token_id={self.token_id!r}, roles={self.roles!r}, revoked={self.revoked!r})"


@dataclass
class CredentialRecord:
    username: str
    principal_id: str
    roles: list[str]
    tenant_id: str | None
    password_hash: str | None = None  # None: service principal (API tokens only)
    enabled: bool = True
    created_at: float = field(default_factory=time.time)
    api_tokens: list[ApiTokenRecord] = field(default_factory=list)

    def __repr__(self) -> str:
        return (f"CredentialRecord(username={self.username!r}, roles={self.roles!r}, "
                f"tenant_id={self.tenant_id!r}, enabled={self.enabled!r})")

    def principal(self, provider: str, roles: tuple[str, ...] | None = None) -> Principal:
        return Principal(id=self.principal_id, username=self.username,
                         roles=tuple(roles if roles is not None else self.roles),
                         provider=provider, tenant_id=self.tenant_id)


def default_credentials_path() -> Path:
    explicit = os.environ.get(CREDENTIALS_FILE_ENV)
    if explicit:
        return Path(explicit)
    return Path(os.getenv("EOIP_DATA_DIR", "/data")) / "state" / "credentials.json"


def _write_private(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
        if os.name == "posix":
            os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


class CredentialStore:
    """File-backed user/credential registry. Thread-safe; re-reads the file on change."""

    def __init__(self, path: Path | str | None = None) -> None:
        self.path = Path(path) if path else default_credentials_path()
        self._lock = threading.RLock()
        self._users: dict[str, CredentialRecord] = {}
        self._mtime: tuple[int, int, int] | None = None
        self._reload(force=True)

    # -- persistence -----------------------------------------------------
    def _reload(self, force: bool = False) -> None:
        try:
            st = self.path.stat()
            # Saves replace the file atomically, so the inode changes even when two writes land in
            # the same coarse mtime tick (otherwise another process could keep stale roles).
            mtime = (st.st_mtime_ns, st.st_ino, st.st_size)
        except FileNotFoundError:
            if force or self._mtime is not None:
                self._users, self._mtime = {}, None
            return
        if not force and mtime == self._mtime:
            return
        data = json.loads(self.path.read_text(encoding="utf-8"))
        users = {}
        for raw in data.get("users", []):
            tokens = [ApiTokenRecord(**t) for t in raw.pop("api_tokens", [])]
            users[raw["username"]] = CredentialRecord(**raw, api_tokens=tokens)
        self._users, self._mtime = users, mtime

    def _save(self) -> None:
        payload = {"schema": "eoip-credentials/1", "users": [asdict(u) for u in self._users.values()]}
        _write_private(self.path, json.dumps(payload, indent=2, sort_keys=True))
        st = self.path.stat()
        self._mtime = (st.st_mtime_ns, st.st_ino, st.st_size)

    # -- queries ---------------------------------------------------------
    def is_empty(self) -> bool:
        with self._lock:
            self._reload()
            return not self._users

    def get(self, username: str) -> CredentialRecord | None:
        with self._lock:
            self._reload()
            return self._users.get(username)

    def summary(self) -> list[dict[str, Any]]:
        with self._lock:
            self._reload()
            return [{"username": u.username, "roles": list(u.roles), "tenant": u.tenant_id or "*",
                     "enabled": u.enabled, "login": u.password_hash is not None,
                     "api_tokens": sum(1 for t in u.api_tokens if not t.revoked)}
                    for u in self._users.values()]

    # -- provisioning ----------------------------------------------------
    def create_user(self, username: str, password: str | None, roles, *, tenant_id: str | None = None,
                    principal_id: str | None = None) -> CredentialRecord:
        if not _USERNAME.match(username or ""):
            raise CredentialError("username must be 1-128 characters: letters, digits, . _ @ -")
        expanded = _check_roles(roles)
        if password is not None and len(password) < MIN_PASSWORD_LENGTH:
            raise CredentialError(f"password must be at least {MIN_PASSWORD_LENGTH} characters")
        if "superadmin" in expanded:
            tenant_id = None  # cross-tenant by definition
        elif not tenant_id:
            raise CredentialError("non-superadmin principals must be bound to a tenant")
        with self._lock:
            self._reload()
            if username in self._users:
                raise CredentialError(f"user {username!r} already exists")
            record = CredentialRecord(
                username=username,
                principal_id=principal_id or f"urn:eoip:authn:principal:local:{username}",
                roles=list(expanded), tenant_id=tenant_id,
                password_hash=_HASHER.hash(password) if password is not None else None,
            )
            self._users[username] = record
            self._save()
            return record

    def _require(self, username: str) -> CredentialRecord:
        record = self._users.get(username)
        if record is None:
            raise CredentialError(f"unknown user {username!r}")
        return record

    def set_password(self, username: str, password: str) -> None:
        if len(password) < MIN_PASSWORD_LENGTH:
            raise CredentialError(f"password must be at least {MIN_PASSWORD_LENGTH} characters")
        with self._lock:
            self._reload()
            self._require(username).password_hash = _HASHER.hash(password)
            self._save()

    def set_roles(self, username: str, roles) -> None:
        expanded = _check_roles(roles)
        with self._lock:
            self._reload()
            record = self._require(username)
            record.roles = list(expanded)
            for token in record.api_tokens:  # a token can never exceed its principal
                token.roles = [r for r in token.roles if r in expanded]
            self._save()

    def set_enabled(self, username: str, enabled: bool) -> None:
        with self._lock:
            self._reload()
            self._require(username).enabled = bool(enabled)
            self._save()

    def issue_api_token(self, username: str, roles=None, *, label: str = "") -> tuple[str, str]:
        """Create an API token for ``username``; returns ``(token_id, token)``. Shown once."""
        token = API_TOKEN_PREFIX + secrets.token_urlsafe(32)
        token_id = self.register_api_token(username, token_sha256(token), roles, label=label)
        return token_id, token

    def register_api_token(self, username: str, sha256: str, roles=None, *, label: str = "") -> str:
        """Map an externally generated token (by digest) to ``username`` with its own roles."""
        if not re.fullmatch(r"[0-9a-f]{64}", sha256 or ""):
            raise CredentialError("expected a sha256 hex digest")
        with self._lock:
            self._reload()
            record = self._require(username)
            granted = _check_roles(roles) if roles else tuple(record.roles)
            if not set(granted) <= set(record.roles):
                raise CredentialError("API token roles must be a subset of the principal's roles")
            for user in self._users.values():
                for existing in user.api_tokens:
                    if hmac.compare_digest(existing.sha256, sha256):
                        if user.username != username:
                            raise CredentialError("token is already mapped to another principal")
                        existing.roles, existing.revoked, existing.label = list(granted), False, label
                        self._save()
                        return existing.token_id
            token_id = "tok_" + secrets.token_hex(8)
            record.api_tokens.append(ApiTokenRecord(token_id=token_id, sha256=sha256, roles=list(granted), label=label))
            self._save()
            return token_id

    def revoke_api_token(self, token_id: str) -> bool:
        with self._lock:
            self._reload()
            for user in self._users.values():
                for token in user.api_tokens:
                    if token.token_id == token_id and not token.revoked:
                        token.revoked = True
                        self._save()
                        return True
            return False

    # -- authentication --------------------------------------------------
    def verify_password(self, username: str, password: str) -> Principal | None:
        with self._lock:
            self._reload()
            record = self._users.get(username or "")
        stored = record.password_hash if record and record.password_hash else _DUMMY_HASH
        try:
            ok = isinstance(password, str) and _HASHER.verify(stored, password)
        except (VerifyMismatchError, VerificationError, InvalidHashError):
            ok = False
        if not ok or record is None or record.password_hash is None or not record.enabled:
            return None
        if _HASHER.check_needs_rehash(record.password_hash):
            with self._lock:
                record.password_hash = _HASHER.hash(password)
                self._save()
        return record.principal("local")

    def authenticate_api_token(self, token: str | None) -> Principal | None:
        if not token or len(token) > 16_384:
            return None
        presented = token_sha256(token)
        with self._lock:
            self._reload()
            hit: tuple[CredentialRecord, ApiTokenRecord] | None = None
            for user in self._users.values():  # walk every token (no early exit)
                for record in user.api_tokens:
                    if hmac.compare_digest(presented, record.sha256) and hit is None:
                        hit = (user, record)
        if hit is None:
            return None
        user, record = hit
        if record.revoked or not user.enabled:
            return None
        roles = tuple(r for r in expand_roles(record.roles) if r in user.roles)
        if not roles:
            return None
        return user.principal("api-token", roles)

    def principal_for_id(self, principal_id: str) -> Principal | None:
        with self._lock:
            self._reload()
            for user in self._users.values():
                if user.principal_id == principal_id:
                    return user.principal("session") if user.enabled and user.password_hash else None
        return None

    def principal_for_sso_session(self, principal_id: str, provider: str, selected_roles: Any) -> Principal | None:
        """Principal for an SSO session: the user must still exist and be enabled (a password is
        not required), and roles are the user's *current* stored roles intersected with the roles
        the IdP groups selected at login -- revocations apply at once, nothing is ever added."""
        selected = {str(r) for r in (selected_roles or [])}
        with self._lock:
            self._reload()
            for user in self._users.values():
                if user.principal_id == principal_id:
                    if not user.enabled:
                        return None
                    roles = tuple(r for r in user.roles if r in selected)
                    return user.principal(provider, roles) if roles else None
        return None


def session_secret(data_dir: Path | None = None) -> bytes:
    """``EOIP_SESSION_SECRET`` (>= 32 chars), else a random key persisted with mode 0600.

    Multi-replica deployments must inject the same ``EOIP_SESSION_SECRET`` everywhere.
    """
    value = os.environ.get(SESSION_SECRET_ENV, "")
    if value:
        if len(value) < MIN_SECRET_LENGTH:
            raise CredentialError(f"{SESSION_SECRET_ENV} must be at least {MIN_SECRET_LENGTH} characters")
        return value.encode("utf-8")
    base = data_dir or Path(os.getenv("EOIP_DATA_DIR", "/data"))
    path = base / "state" / "session.key"
    if not path.exists():
        _write_private(path, secrets.token_urlsafe(48))
    return path.read_text(encoding="utf-8").strip().encode("utf-8")


class SessionManager:
    """Signed, expiring session tokens for logged-in users; roles re-read per request."""

    def __init__(self, store: CredentialStore, secret: bytes, *, ttl_seconds: int | None = None) -> None:
        ttl = ttl_seconds if ttl_seconds is not None else int(os.environ.get(SESSION_TTL_ENV, "28800"))
        self._store = store
        self._tokens = TokenService(secret, issuer="eoip-authn", audience="eoip-api", default_ttl_seconds=ttl)
        self._revoked: dict[str, float] = {}
        self._lock = threading.Lock()
        self.ttl_seconds = ttl

    def issue(self, principal: Principal, **kwargs) -> str:
        return self._tokens.issue(principal, **kwargs)

    def revoke(self, token: str) -> None:
        try:
            exp = float(self._tokens.validate(token)["exp"])
        except TokenError:
            return
        with self._lock:
            now = time.time()
            self._revoked = {k: v for k, v in self._revoked.items() if v > now}
            self._revoked[token_sha256(token)] = exp

    def principal(self, token: str) -> Principal | None:
        try:
            payload = self._tokens.validate(token)
        except TokenError:
            return None
        with self._lock:
            if token_sha256(token) in self._revoked:
                return None
        if payload.get("provider") in ("oidc", "saml"):
            principal = self._store.principal_for_sso_session(
                payload["sub"], payload["provider"], payload.get("roles") or [])
        else:
            principal = self._store.principal_for_id(payload["sub"])
        if principal is None:
            return None
        return replace(principal, claims={k: payload[k] for k in ("sub", "iat", "exp", "aud", "iss") if k in payload})


class LoginThrottle:
    """Per-username failed-login limiter (in-process)."""

    def __init__(self, max_failures: int = 10, window_seconds: float = 300.0) -> None:
        self.max_failures, self.window = max_failures, window_seconds
        self._failures: dict[str, list[float]] = {}
        self._lock = threading.Lock()

    def blocked(self, username: str) -> bool:
        now = time.time()
        with self._lock:
            recent = [t for t in self._failures.get(username, []) if now - t < self.window]
            self._failures[username] = recent
            return len(recent) >= self.max_failures

    def failed(self, username: str) -> None:
        with self._lock:
            self._failures.setdefault(username, []).append(time.time())

    def succeeded(self, username: str) -> None:
        with self._lock:
            self._failures.pop(username, None)
