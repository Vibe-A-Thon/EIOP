"""Unit tests for eoip.authn (GAP-SEC-001..004, §27, §48)."""

from __future__ import annotations

import base64
import json
import sys
import time

import pytest

from eoip.authn import (
    AuthenticationError,
    AuthenticationUnavailable,
    CryptographyVerifier,
    IdentityProvider,
    LdapIdentityProvider,
    LdapProtocolFacade,
    LocalIdentityProvider,
    OidcConfigurationError,
    OidcJwtValidator,
    Principal,
    TokenExpired,
    TokenService,
    TokenTampered,
    hash_password,
    verify_password,
)

_SECRET = b"\x01" * 32


def _b64u(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


# --------------------------------------------------------------------------
# Local provider


class TestLocalIdentityProvider:
    def test_authenticate_success(self):
        provider = LocalIdentityProvider()
        provider.add_user("alice", "s3cret!", roles=("admin", "reader"))
        principal = provider.authenticate(
            {"username": "alice", "password": "s3cret!"})
        assert principal.username == "alice"
        assert principal.roles == ("admin", "reader")
        assert principal.provider == "local"
        assert principal.id.startswith("urn:eoip:authn:principal:")
        assert isinstance(principal, Principal)

    def test_wrong_password_rejected(self):
        provider = LocalIdentityProvider()
        provider.add_user("alice", "s3cret!")
        with pytest.raises(AuthenticationError):
            provider.authenticate({"username": "alice", "password": "wrong"})

    def test_unknown_user_rejected(self):
        provider = LocalIdentityProvider()
        with pytest.raises(AuthenticationError):
            provider.authenticate({"username": "nobody", "password": "x"})

    def test_disabled_user_rejected(self):
        provider = LocalIdentityProvider()
        provider.add_user("alice", "s3cret!")
        provider._users["alice"] = provider._users["alice"].__class__(
            id=provider._users["alice"].id, username="alice",
            password_hash=provider._users["alice"].password_hash,
            roles=(), enabled=False,
        )
        with pytest.raises(AuthenticationError):
            provider.authenticate({"username": "alice", "password": "s3cret!"})

    def test_password_hash_roundtrip(self):
        stored = hash_password("pw", salt=b"0123456789abcdef")
        assert verify_password("pw", stored)
        assert not verify_password("nope", stored)

    def test_distinct_salts(self):
        assert hash_password("pw") != hash_password("pw")

    def test_hash_format(self):
        algo, iterations, salt, _ = hash_password("pw").split("$")
        assert algo == "pbkdf2-sha256"
        assert int(iterations) >= 200_000
        assert base64.b64decode(salt)

    def test_repr_redacts_password_hash(self):
        provider = LocalIdentityProvider()
        record = provider.add_user("alice", "s3cret!")
        assert "s3cret!" not in repr(record)
        assert "***REDACTED***" in repr(record)

    def test_set_password(self):
        provider = LocalIdentityProvider()
        provider.add_user("alice", "old")
        provider.set_password("alice", "new")
        with pytest.raises(AuthenticationError):
            provider.authenticate({"username": "alice", "password": "old"})
        assert provider.authenticate(
            {"username": "alice", "password": "new"}).username == "alice"

    def test_health(self):
        provider = LocalIdentityProvider()
        provider.add_user("alice", "x")
        health = provider.health()
        assert health["status"] == "ok"
        assert health["users"] == 1
        assert "password" not in json.dumps(health).lower()

    def test_satisfies_protocol(self):
        assert isinstance(LocalIdentityProvider(), IdentityProvider)


# --------------------------------------------------------------------------
# Token service


def _principal():
    return Principal(id="urn:eoip:authn:principal:local:alice",
                     username="alice", roles=("reader",))


class TestTokenService:
    def test_issue_and_validate(self):
        service = TokenService(secret=_SECRET)
        token = service.issue(_principal())
        claims = service.validate(token)
        assert claims["sub"] == "urn:eoip:authn:principal:local:alice"
        assert claims["username"] == "alice"
        assert claims["roles"] == ["reader"]
        assert claims["aud"] == "eoip-api"
        assert claims["exp"] > claims["iat"]

    def test_validate_custom_audience(self):
        service = TokenService(secret=_SECRET, audience="eoip-api")
        token = service.issue(_principal(), audience="other-aud")
        claims = service.validate(token, audience="other-aud")
        assert claims["aud"] == "other-aud"

    def test_expired_token(self):
        service = TokenService(secret=_SECRET)
        token = service.issue(_principal(), ttl_seconds=-1)
        with pytest.raises(TokenExpired):
            service.validate(token)

    def test_tampered_payload(self):
        service = TokenService(secret=_SECRET)
        token = service.issue(_principal())
        header_b64, payload_b64, sig_b64 = token.split(".")
        payload = json.loads(base64.urlsafe_b64decode(payload_b64 + "=="))
        payload["roles"] = ["admin"]  # escalate without re-signing
        forged = f"{header_b64}.{_b64u(json.dumps(payload).encode())}.{sig_b64}"
        with pytest.raises(TokenTampered):
            service.validate(forged)

    def test_wrong_secret_rejected(self):
        issuer = TokenService(secret=_SECRET)
        validator = TokenService(secret=b"\x02" * 32)
        token = issuer.issue(_principal())
        with pytest.raises(TokenTampered):
            validator.validate(token)

    def test_malformed_token(self):
        service = TokenService(secret=_SECRET)
        with pytest.raises(TokenTampered):
            service.validate("not-a-token")
        with pytest.raises(TokenTampered):
            service.validate("a.b")

    def test_audience_mismatch(self):
        service = TokenService(secret=_SECRET)
        token = service.issue(_principal())
        with pytest.raises(TokenTampered):
            service.validate(token, audience="elsewhere")

    def test_random_secret_per_instance(self):
        assert TokenService()._secret != TokenService()._secret


# --------------------------------------------------------------------------
# OIDC validator


class FakeRs256Verifier:
    algorithm = "RS256"

    def __init__(self, accept=True):
        self.accept = accept
        self.kids = []

    def verify(self, signing_input, signature, kid):
        self.kids.append(kid)
        return self.accept


def _make_oidc_token(payload, header=None):
    token_header = {"alg": "RS256", "typ": "JWT", "kid": "key-1"}
    token_header.update(header or {})
    return (f"{_b64u(json.dumps(token_header).encode())}."
            f"{_b64u(json.dumps(payload).encode())}.{_b64u(b'sig')}")


class TestOidcJwtValidator:
    def _payload(self, **overrides):
        payload = {
            "sub": "user-123",
            "iss": "https://idp.example.com",
            "aud": "eoip-api",
            "exp": time.time() + 300,
            "preferred_username": "alice@example.com",
            "groups": ["reader", "editor"],
            "email": "alice@example.com",
        }
        payload.update(overrides)
        return payload

    def test_valid_token_maps_to_principal(self):
        verifier = FakeRs256Verifier()
        validator = OidcJwtValidator(
            issuer="https://idp.example.com", audience="eoip-api",
            verifier=verifier)
        principal = validator.validate(_make_oidc_token(self._payload()))
        assert principal.username == "alice@example.com"
        assert principal.roles == ("reader", "editor")
        assert principal.provider == "oidc"
        assert principal.id == "urn:eoip:authn:principal:oidc:user-123"
        assert verifier.kids == ["key-1"]

    def test_requires_issuer_and_audience(self):
        with pytest.raises(OidcConfigurationError):
            OidcJwtValidator(issuer="", audience="x", verifier=FakeRs256Verifier())

    def test_requires_verifier_or_jwks(self):
        with pytest.raises(OidcConfigurationError):
            OidcJwtValidator(issuer="iss", audience="aud")

    def test_bad_signature_rejected(self):
        validator = OidcJwtValidator(
            issuer="https://idp.example.com", audience="eoip-api",
            verifier=FakeRs256Verifier(accept=False))
        with pytest.raises(TokenTampered, match="signature"):
            validator.validate(_make_oidc_token(self._payload()))

    def test_expired_id_token(self):
        validator = OidcJwtValidator(
            issuer="https://idp.example.com", audience="eoip-api",
            verifier=FakeRs256Verifier())
        token = _make_oidc_token(self._payload(exp=time.time() - 10))
        with pytest.raises(TokenExpired):
            validator.validate(token)

    def test_issuer_mismatch(self):
        validator = OidcJwtValidator(
            issuer="https://other.example.com", audience="eoip-api",
            verifier=FakeRs256Verifier())
        with pytest.raises(TokenTampered, match="issuer"):
            validator.validate(_make_oidc_token(self._payload()))

    def test_audience_mismatch(self):
        validator = OidcJwtValidator(
            issuer="https://idp.example.com", audience="other-app",
            verifier=FakeRs256Verifier())
        with pytest.raises(TokenTampered, match="audience"):
            validator.validate(_make_oidc_token(self._payload()))

    def test_nbf_enforced(self):
        validator = OidcJwtValidator(
            issuer="https://idp.example.com", audience="eoip-api",
            verifier=FakeRs256Verifier())
        token = _make_oidc_token(self._payload(nbf=time.time() + 600))
        with pytest.raises(TokenTampered, match="not yet valid"):
            validator.validate(token)

    def test_rejects_non_rs256(self):
        validator = OidcJwtValidator(
            issuer="https://idp.example.com", audience="eoip-api",
            verifier=FakeRs256Verifier())
        token = _make_oidc_token(self._payload(), header={"alg": "HS256"})
        with pytest.raises(TokenTampered, match="alg"):
            validator.validate(token)

    def test_missing_sub_rejected(self):
        validator = OidcJwtValidator(
            issuer="https://idp.example.com", audience="eoip-api",
            verifier=FakeRs256Verifier())
        token = _make_oidc_token(self._payload(sub=""))
        with pytest.raises(TokenTampered, match="sub"):
            validator.validate(token)

    def test_cryptography_verifier_not_available_path(self, monkeypatch):
        # A None entry in sys.modules forces ImportError on any
        # `from cryptography... import` inside CryptographyVerifier. Block every
        # cached cryptography.* submodule too, otherwise the test is order-dependent
        # (FT-D10): earlier tests leave cryptography.hazmat... importable.
        for name in [m for m in sys.modules if m == "cryptography" or m.startswith("cryptography.")]:
            monkeypatch.setitem(sys.modules, name, None)
        monkeypatch.setitem(sys.modules, "cryptography", None)
        with pytest.raises(AuthenticationUnavailable, match="not deployed"):
            CryptographyVerifier({"keys": []})


# --------------------------------------------------------------------------
# LDAP provider


class FakeLdapFacade(LdapProtocolFacade):
    """In-memory fake LDAP server stub for unit tests (GAP-SEC-003)."""

    def __init__(self, users=None, fail_connect=False):
        self.users = users or {}
        self.fail_connect = fail_connect
        self.connect_calls = []
        self.bound = []
        self.closed = False

    def connect(self, host, port, *, use_tls, timeout):
        if self.fail_connect:
            raise OSError("connection refused")
        self.connect_calls.append((host, port, use_tls, timeout))

    def bind(self, dn, password):
        self.bound.append((dn, "***" if password else ""))
        expected = self.users.get(dn)
        return expected is not None and expected[0] == password

    def search_roles(self, dn):
        entry = self.users.get(dn)
        return list(entry[1]) if entry else []

    def close(self):
        self.closed = True


class TestLdapIdentityProvider:
    def _provider(self, facade=None):
        return LdapIdentityProvider(
            host="ldap.example.com", port=636, use_tls=True,
            bind_dn_template="uid={username},ou=people,dc=example,dc=com",
            facade=facade or FakeLdapFacade())

    def test_authenticate_success(self):
        facade = FakeLdapFacade(
            {"uid=alice,ou=people,dc=example,dc=com": ("pw", ["reader"])})
        provider = self._provider(facade)
        principal = provider.authenticate(
            {"username": "alice", "password": "pw"})
        assert principal.username == "alice"
        assert principal.roles == ("reader",)
        assert principal.provider == "ldap"
        assert principal.id == "urn:eoip:authn:principal:ldap:alice"
        assert facade.closed

    def test_bad_password_rejected(self):
        facade = FakeLdapFacade(
            {"uid=alice,ou=people,dc=example,dc=com": ("pw", [])})
        provider = self._provider(facade)
        with pytest.raises(AuthenticationError):
            provider.authenticate({"username": "alice", "password": "bad"})

    def test_unknown_user_rejected(self):
        provider = self._provider(FakeLdapFacade())
        with pytest.raises(AuthenticationError):
            provider.authenticate({"username": "ghost", "password": "x"})

    def test_missing_credentials_rejected(self):
        provider = self._provider()
        with pytest.raises(AuthenticationError):
            provider.authenticate({"username": "", "password": "x"})
        with pytest.raises(AuthenticationError):
            provider.authenticate({"username": "a", "password": ""})

    def test_connection_failure_is_unavailable(self):
        facade = FakeLdapFacade(fail_connect=True)
        provider = self._provider(facade)
        with pytest.raises(AuthenticationUnavailable):
            provider.authenticate({"username": "alice", "password": "pw"})

    def test_facade_closed_after_bind(self):
        facade = FakeLdapFacade(
            {"uid=a,ou=people,dc=example,dc=com": ("pw", [])})
        provider = self._provider(facade)
        with pytest.raises(AuthenticationError):
            provider.authenticate({"username": "a", "password": "nope"})
        assert facade.closed

    def test_bind_dn_template_required_placeholder(self):
        with pytest.raises(ValueError):
            LdapIdentityProvider(host="h", bind_dn_template="uid=fixed")

    def test_password_never_recorded_by_facade(self):
        facade = FakeLdapFacade(
            {"uid=alice,ou=people,dc=example,dc=com": ("s3cret", [])})
        provider = self._provider(facade)
        provider.authenticate({"username": "alice", "password": "s3cret"})
        for _, logged in facade.bound:
            assert "s3cret" not in logged

    def test_health_no_secrets(self):
        provider = self._provider()
        health = provider.health()
        assert health["status"] == "ok"
        assert health["host"] == "ldap.example.com"
        assert "password" not in json.dumps(health).lower()

    def test_satisfies_protocol(self):
        assert isinstance(self._provider(), IdentityProvider)
