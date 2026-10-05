"""Authentication & identity federation (GAP-SEC-001..GAP-SEC-004, §27, §48).

Pluggable identity layer for EOIP:

- :class:`IdentityProvider` — protocol implemented by local, LDAP, and future
  SSO/OIDC/SAML providers (GAP-SEC roadmap, §27).
- :class:`LocalIdentityProvider` — username/password with salted
  PBKDF2-HMAC-SHA256 hashing and a user store whose role assignments are
  consumed by ``eoip.authz`` authorization checks.
- :class:`TokenService` — stdlib-only HMAC-SHA256 bearer token issue/validate.
- :class:`OidcJwtValidator` — offline RS256 OIDC ID-token validation against a
  JWKS document and issuer/audience configuration (GAP-SEC-002, §48).
- :class:`LdapIdentityProvider` — adapter over a generic socket-based LDAP
  protocol facade; unit-testable with a fake server stub. Real LDAP requires
  the deployment's LDAP server (GAP-SEC-003, §27).

Secrets discipline: passwords and tokens are never logged or included in
``repr()`` output (NFR-OPS-001, see ``eoip.audit.redaction``).
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import socket
import ssl
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

__all__ = [
    "AuthenticationError",
    "AuthenticationUnavailable",
    "CryptographyVerifier",
    "IdentityProvider",
    "LdapIdentityProvider",
    "LocalIdentityProvider",
    "LdapProtocolFacade",
    "OidcConfigurationError",
    "OidcJwtValidator",
    "Principal",
    "SignatureVerifier",
    "TokenError",
    "TokenExpired",
    "TokenService",
    "TokenTampered",
    "UserRecord",
]

# ---------------------------------------------------------------------------
# Errors (GAP-SEC-001)


class AuthenticationError(Exception):
    """Credentials rejected or malformed (GAP-SEC-001)."""


class AuthenticationUnavailable(Exception):
    """Identity backend unreachable or not configured."""


class TokenError(Exception):
    """Base class for bearer token validation failures (GAP-SEC-004)."""


class TokenExpired(TokenError):
    """Token past its expiry."""


class TokenTampered(TokenError):
    """Signature mismatch or malformed token."""


class OidcConfigurationError(Exception):
    """OIDC validator missing required issuer/audience/JWKS configuration."""


# ---------------------------------------------------------------------------
# Principal (GAP-SEC-001, §27)


@dataclass(frozen=True)
class Principal:
    """Authenticated identity. Roles are consumed by ``eoip.authz``.

    GAP-SEC-001; identity federation via SSO/OIDC/SAML/LDAP per §27/§48.
    """

    id: str  # urn:eoip:authn:principal:<id>
    username: str
    roles: tuple[str, ...] = ()
    provider: str = "local"
    claims: dict[str, Any] = field(default_factory=dict, compare=False)

    def __repr__(self) -> str:  # never leak claims that may hold tokens
        return (
            f"Principal(id={self.id!r}, username={self.username!r}, "
            f"roles={self.roles!r}, provider={self.provider!r})"
        )


# ---------------------------------------------------------------------------
# IdentityProvider protocol (GAP-SEC-001, §27)


@runtime_checkable
class IdentityProvider(Protocol):
    """Pluggable identity backend protocol.

    Implemented by :class:`LocalIdentityProvider`, :class:`LdapIdentityProvider`,
    and future OIDC/SAML federation providers (GAP-SEC-002/GAP-SEC-003, §48).
    """

    def authenticate(self, credentials: dict[str, Any]) -> Principal:
        """Validate credentials and return a Principal (GAP-SEC-001)."""
        ...

    def health(self) -> dict[str, Any]:
        """Backend liveness/readiness without exposing secrets."""
        ...


# ---------------------------------------------------------------------------
# Local identity provider (GAP-SEC-001)

_PBKDF2_ITERATIONS = 210_000
_ALGORITHM = "pbkdf2-sha256"


def hash_password(password: str, *, salt: bytes | None = None,
                  iterations: int = _PBKDF2_ITERATIONS) -> str:
    """Salted PBKDF2-HMAC-SHA256 password hash, ``algo$iterations$salt$hash``.

    GAP-SEC-001. Never log the password or this value's preimage.
    """
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                 salt, iterations)
    return "$".join([
        _ALGORITHM,
        str(iterations),
        base64.b64encode(salt).decode("ascii"),
        base64.b64encode(digest).decode("ascii"),
    ])


def verify_password(password: str, stored: str) -> bool:
    """Constant-time verification of a stored PBKDF2 hash (GAP-SEC-001)."""
    try:
        algo, iterations, salt_b64, digest_b64 = stored.split("$")
        if algo != _ALGORITHM:
            return False
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(digest_b64)
    except (ValueError, TypeError):
        return False
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                 salt, int(iterations))
    return hmac.compare_digest(digest, expected)


@dataclass(frozen=True)
class UserRecord:
    """Local user store entry; ``roles`` are consumed by ``eoip.authz``.

    GAP-SEC-001, §27.
    """

    id: str
    username: str
    password_hash: str
    roles: tuple[str, ...] = ()
    enabled: bool = True

    def __repr__(self) -> str:
        return (
            f"UserRecord(id={self.id!r}, username={self.username!r}, "
            f"password_hash=***REDACTED***, roles={self.roles!r}, "
            f"enabled={self.enabled!r})"
        )


class LocalIdentityProvider:
    """Username/password provider with PBKDF2-HMAC-SHA256 hashing.

    GAP-SEC-001. Deterministic; no external calls. The user store maps
    usernames to :class:`UserRecord` whose role assignments feed ``eoip.authz``.
    """

    name = "local"

    def __init__(self, users: dict[str, UserRecord] | None = None) -> None:
        self._users: dict[str, UserRecord] = dict(users or {})
        self._lock = threading.Lock()

    def add_user(self, username: str, password: str,
                 roles: tuple[str, ...] = (),
                 user_id: str | None = None) -> UserRecord:
        """Create a user with a freshly salted hash (GAP-SEC-001)."""
        record = UserRecord(
            id=user_id or f"urn:eoip:authn:principal:local:{username}",
            username=username,
            password_hash=hash_password(password),
            roles=tuple(roles),
        )
        with self._lock:
            self._users[username] = record
        return record

    def set_password(self, username: str, password: str) -> None:
        with self._lock:
            if username not in self._users:
                raise AuthenticationError("unknown user")
            current = self._users[username]
            self._users[username] = UserRecord(
                id=current.id, username=current.username,
                password_hash=hash_password(password), roles=current.roles,
                enabled=current.enabled,
            )

    def authenticate(self, credentials: dict[str, Any]) -> Principal:
        """Verify ``{"username": ..., "password": ...}`` (GAP-SEC-001)."""
        username = str(credentials.get("username") or "")
        password = credentials.get("password")
        with self._lock:
            record = self._users.get(username)
        # Compare against a dummy hash when the user is unknown so timing
        # does not reveal which usernames exist (GAP-SEC-001).
        stored = (record.password_hash if record
                  else "$".join([_ALGORITHM, str(_PBKDF2_ITERATIONS),
                                 base64.b64encode(b"\x00" * 16).decode(),
                                 base64.b64encode(b"\x00" * 32).decode()]))
        if not isinstance(password, str) or not verify_password(password, stored):
            raise AuthenticationError("invalid credentials")
        if record is None or not record.enabled:
            raise AuthenticationError("invalid credentials")
        return Principal(
            id=record.id, username=record.username, roles=record.roles,
            provider=self.name,
        )

    def health(self) -> dict[str, Any]:
        with self._lock:
            count = len(self._users)
        return {"status": "ok", "provider": self.name, "users": count}


# ---------------------------------------------------------------------------
# HMAC bearer tokens (GAP-SEC-004, §48)

_B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
_B64_ALT = f"{_B64}+/".encode()
_B64_MAP = bytes.maketrans(_B64_ALT,
                           (_B64 + "-_").encode())


def _b64u_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64u_decode(data: str) -> bytes:
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)


def _canonical(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"),
                      ).encode("utf-8")


class TokenService:
    """Issue and validate HMAC-SHA256 bearer tokens. Stdlib-only.

    Token format: ``b64u(header).b64u(payload).b64u(hmac_sha256_sig)``.
    Payload carries ``sub`` (principal id), ``username``, ``roles``, ``exp``
    (epoch seconds), ``iat``, and ``aud``. GAP-SEC-004, §48.

    Never log tokens; only their ``sub``/``exp`` are safe to record.
    """

    def __init__(self, secret: bytes | None = None,
                 *, audience: str = "eoip-api",
                 issuer: str = "eoip-authn",
                 default_ttl_seconds: int = 3600,
                 sign_algorithm: str = "HS256") -> None:
        if sign_algorithm != "HS256":
            raise ValueError("only HS256 (HMAC-SHA256) is supported")
        self._secret = secret or os.urandom(32)
        self._audience = audience
        self._issuer = issuer
        self._ttl = default_ttl_seconds

    @property
    def audience(self) -> str:
        return self._audience

    def _signature(self, signing_input: bytes) -> bytes:
        return hmac.new(self._secret, signing_input, hashlib.sha256).digest()

    def issue(self, principal: Principal,
              *, ttl_seconds: int | None = None,
              audience: str | None = None) -> str:
        """Mint a bearer token for a Principal (GAP-SEC-004)."""
        now = int(time.time())
        ttl = self._ttl if ttl_seconds is None else ttl_seconds
        payload = {
            "sub": principal.id,
            "username": principal.username,
            "roles": list(principal.roles),
            "iat": now,
            "exp": now + ttl,
            "aud": audience or self._audience,
            "iss": self._issuer,
        }
        header = {"alg": "HS256", "typ": "EOIP"}
        signing_input = (
            _b64u_encode(_canonical(header)) + "." +
            _b64u_encode(_canonical(payload))
        ).encode("ascii")
        sig = _b64u_encode(self._signature(signing_input))
        return signing_input.decode("ascii") + "." + sig

    def validate(self, token: str,
                 *, audience: str | None = None) -> dict[str, Any]:
        """Validate signature, expiry, issuer, and audience (GAP-SEC-004)."""
        try:
            header_b64, payload_b64, sig_b64 = token.split(".")
            payload = json.loads(_b64u_decode(payload_b64))
        except (ValueError, json.JSONDecodeError) as exc:
            raise TokenTampered("malformed token") from exc

        signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
        expected = self._signature(signing_input)
        try:
            supplied = _b64u_decode(sig_b64)
        except (ValueError, TypeError) as exc:
            raise TokenTampered("malformed signature") from exc
        if not hmac.compare_digest(expected, supplied):
            raise TokenTampered("signature mismatch")

        if payload.get("iss") != self._issuer:
            raise TokenTampered("unexpected issuer")
        aud = audience or self._audience
        if payload.get("aud") != aud:
            raise TokenTampered("unexpected audience")
        exp = payload.get("exp")
        if not isinstance(exp, (int, float)):
            raise TokenTampered("missing expiry")
        if time.time() >= exp:
            raise TokenExpired("token expired")
        return payload


# ---------------------------------------------------------------------------
# OIDC JWT validation (GAP-SEC-002, §48)


class SignatureVerifier(Protocol):
    """Pluggable RS256 signature verifier for OIDC ID tokens.

    The stdlib has no RSA. If the optional ``cryptography`` package is
    deployed (not declared in pyproject.toml), :class:`CryptographyVerifier`
    performs real RS256 verification against a JWKS document. Otherwise the
    validator raises :class:`AuthenticationUnavailable` — a documented
    NotAvailable path; production OIDC requires the deployment to provide
    ``cryptography`` (GAP-SEC-002, §48).
    """

    algorithm: str

    def verify(self, signing_input: bytes, signature: bytes,
               kid: str | None) -> bool:
        ...


class CryptographyVerifier:
    """RS256 verifier using an optional JWKS document.

    NotAvailable path: raises :class:`AuthenticationUnavailable` when the
    ``cryptography`` package is not importable (GAP-SEC-002).
    """

    algorithm = "RS256"

    def __init__(self, jwks: dict[str, Any]) -> None:
        try:
            from cryptography.hazmat.primitives.asymmetric import rsa
            from cryptography.hazmat.primitives.asymmetric import padding
            from cryptography.hazmat.primitives import hashes
        except ImportError as exc:  # documented NotAvailable path
            raise AuthenticationUnavailable(
                "cryptography package not deployed; RS256 OIDC validation "
                "unavailable (provide `cryptography` to enable GAP-SEC-002)"
            ) from exc
        self._padding = padding
        self._hashes = hashes
        self._keys: dict[str, Any] = {}
        for jwk in jwks.get("keys", []):
            if jwk.get("kty") == "RSA" and jwk.get("kid"):
                n = int.from_bytes(_b64u_decode(jwk["n"]), "big")
                e = int.from_bytes(_b64u_decode(jwk["e"]), "big")
                self._keys[jwk["kid"]] = rsa.RSAPublicNumbers(e, n).public_key()

    def verify(self, signing_input: bytes, signature: bytes,
               kid: str | None) -> bool:
        key = self._keys.get(kid or "")
        if key is None:
            return False
        try:
            key.verify(signature, signing_input,
                       self._padding.PKCS1v15(), self._hashes.SHA256())
            return True
        except Exception:
            return False


class OidcJwtValidator:
    """Offline OIDC ID-token validation against issuer/audience config.

    Validates ``iss``, ``aud``, ``exp``, ``nbf`` (if present), and the RS256
    signature via a pluggable :class:`SignatureVerifier` keyed by JWKS ``kid``
    (GAP-SEC-002, §48). Deterministic — no network calls at validation time;
    JWKS must be supplied as configuration.
    """

    def __init__(self, *, issuer: str, audience: str,
                 verifier: SignatureVerifier | None = None,
                 jwks: dict[str, Any] | None = None,
                 leeway_seconds: int = 0,
                 now: Any | None = None) -> None:
        if not issuer or not audience:
            raise OidcConfigurationError("issuer and audience are required")
        self._issuer = issuer
        self._audience = audience
        self._leeway = leeway_seconds
        self._now = now or time.time
        if verifier is not None:
            self._verifier = verifier
        elif jwks is not None:
            self._verifier = CryptographyVerifier(jwks)
        else:
            raise OidcConfigurationError(
                "a signature verifier or JWKS document is required")

    @property
    def issuer(self) -> str:
        return self._issuer

    def validate(self, id_token: str) -> Principal:
        """Validate an OIDC ID token and map claims to a Principal."""
        try:
            header_b64, payload_b64, sig_b64 = id_token.split(".")
            header = json.loads(_b64u_decode(header_b64))
            payload = json.loads(_b64u_decode(payload_b64))
            signature = _b64u_decode(sig_b64)
        except (ValueError, json.JSONDecodeError) as exc:
            raise TokenTampered("malformed id token") from exc

        if header.get("alg") != "RS256":
            raise TokenTampered(f"unsupported alg: {header.get('alg')!r}")
        if payload.get("iss") != self._issuer:
            raise TokenTampered("issuer mismatch")
        aud = payload.get("aud")
        if aud != self._audience and self._audience not in (
                aud if isinstance(aud, list) else []):
            raise TokenTampered("audience mismatch")

        now = float(self._now())
        exp = payload.get("exp")
        if not isinstance(exp, (int, float)) or now > exp + self._leeway:
            raise TokenExpired("id token expired")
        nbf = payload.get("nbf")
        if isinstance(nbf, (int, float)) and now + self._leeway < nbf:
            raise TokenTampered("id token not yet valid")

        signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
        if not self._verifier.verify(signing_input, signature,
                                     header.get("kid")):
            raise TokenTampered("signature verification failed")

        sub = str(payload.get("sub") or "")
        if not sub:
            raise TokenTampered("missing sub claim")
        roles = payload.get("roles") or payload.get("groups") or []
        if isinstance(roles, str):
            roles = [roles]
        return Principal(
            id=f"urn:eoip:authn:principal:oidc:{sub}",
            username=str(payload.get("preferred_username") or sub),
            roles=tuple(str(r) for r in roles),
            provider="oidc",
            claims={"email": payload.get("email"), "iss": self._issuer},
        )


# ---------------------------------------------------------------------------
# LDAP adapter (GAP-SEC-003, §27)


class LdapProtocolFacade:
    """Generic socket-based LDAP protocol facade.

    Minimal synchronous interface the adapter speaks. Unit tests provide a
    fake implementation; production wiring supplies a facade bound to the
    deployment's LDAP server over TLS when ``use_tls`` is set (GAP-SEC-003).

    .. note::
        Real LDAP connectivity requires the deployment's LDAP server; EOIP
        ships no LDAP server. This facade keeps the adapter fully
        unit-testable without network access (§27 roadmap).
    """

    def connect(self, host: str, port: int, *, use_tls: bool,
                timeout: float) -> None:
        raise NotImplementedError

    def bind(self, dn: str, password: str) -> bool:
        """Attempt a bind with ``dn``/``password``; True on success."""
        raise NotImplementedError

    def search_roles(self, dn: str) -> list[str]:
        """Return role/group names for a bound DN (consumed by eoip.authz)."""
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError


class SocketLdapProtocolFacade(LdapProtocolFacade):
    """Placeholder TLS-socket facade.

    NotAvailable path: real BER/DER LDAP wire-encoding is deployment-specific
    and intentionally not shipped (GAP-SEC-003). Use this only with a
    deployment-provided LDAP codec, or inject a custom facade in tests.
    """

    def connect(self, host: str, port: int, *, use_tls: bool,
                timeout: float) -> None:
        raw = socket.create_connection((host, port), timeout=timeout)
        if use_tls:
            context = ssl.create_default_context()
            self._sock = context.wrap_socket(raw, server_hostname=host)
        else:
            self._sock = raw

    def bind(self, dn: str, password: str) -> bool:
        raise AuthenticationUnavailable(
            "SocketLdapProtocolFacade requires the deployment's LDAP wire "
            "codec; inject a custom LdapProtocolFacade (GAP-SEC-003)")

    def search_roles(self, dn: str) -> list[str]:
        raise AuthenticationUnavailable(
            "SocketLdapProtocolFacade requires the deployment's LDAP wire "
            "codec; inject a custom LdapProtocolFacade (GAP-SEC-003)")

    def close(self) -> None:
        sock = getattr(self, "_sock", None)
        if sock is not None:
            sock.close()
            self._sock = None


class LdapIdentityProvider:
    """LDAP bind/authenticate adapter (GAP-SEC-003, §27).

    Interface: ``host``, ``port``, ``bind_dn_template`` (``{username}``
    placeholder), ``use_tls``. Passwords are used only for the bind and are
    never stored or logged. Role lookup via the facade feeds ``eoip.authz``.
    """

    name = "ldap"

    def __init__(self, *, host: str, port: int = 389,
                 bind_dn_template: str,
                 use_tls: bool = True,
                 facade: LdapProtocolFacade | None = None,
                 timeout: float = 5.0) -> None:
        if "{username}" not in bind_dn_template:
            raise ValueError("bind_dn_template must contain {username}")
        self._host = host
        self._port = port
        self._template = bind_dn_template
        self._use_tls = use_tls
        self._facade = facade or SocketLdapProtocolFacade()
        self._timeout = timeout

    def authenticate(self, credentials: dict[str, Any]) -> Principal:
        """Bind with ``{"username": ..., "password": ...}`` (GAP-SEC-003)."""
        username = str(credentials.get("username") or "")
        password = credentials.get("password")
        if not username or not isinstance(password, str) or not password:
            raise AuthenticationError("invalid credentials")
        dn = self._template.format(username=username)
        try:
            self._facade.connect(self._host, self._port, use_tls=self._use_tls,
                                 timeout=self._timeout)
        except OSError as exc:
            raise AuthenticationUnavailable(
                f"ldap unreachable: {exc.__class__.__name__}") from exc
        try:
            if not self._facade.bind(dn, password):
                raise AuthenticationError("invalid credentials")
            roles = tuple(str(r) for r in self._facade.search_roles(dn))
        finally:
            self._facade.close()
        return Principal(
            id=f"urn:eoip:authn:principal:ldap:{username}",
            username=username, roles=roles, provider=self.name,
        )

    def health(self) -> dict[str, Any]:
        return {
            "status": "ok",
            "provider": self.name,
            "host": self._host,
            "port": self._port,
            "tls": self._use_tls,
        }
