"""Untrusted token strings must never create an authenticated identity."""

import base64
import hashlib
import hmac
import json
import time

import pytest
from eoip.authn import Principal, TokenService
from eoip.authn.oauth_sso import TokenValidator

pytestmark = [pytest.mark.security, pytest.mark.req("GAP-SEC-004", "INFRA-002")]
SECRET = "test-secret-that-is-never-a-production-default"


def _signed(payload, header=None):
    def encode(value):
        return base64.urlsafe_b64encode(json.dumps(value).encode()).decode().rstrip("=")
    signing = f"{encode(header or {'alg': 'HS256'})}.{encode(payload)}"
    signature = hmac.new(SECRET.encode(), signing.encode(), hashlib.sha256).digest()
    return signing + "." + base64.urlsafe_b64encode(signature).decode().rstrip("=")


def test_valid_canonical_token_is_accepted():
    token = TokenService(SECRET.encode()).issue(Principal("user-1", "alice", ("viewer",)))
    assert TokenValidator(SECRET).validate_token(token)["sub"] == "user-1"


@pytest.mark.parametrize("token", ["", "arbitrary-long-token-that-used-to-authenticate", "a.b.c", "x" * 20000, None])
def test_arbitrary_malformed_or_unbounded_tokens_are_rejected(token):
    with pytest.raises(ValueError, match="Invalid token"):
        TokenValidator(SECRET).validate_token(token)


@pytest.mark.parametrize("claim,value", [
    ("iss", "another-issuer"), ("aud", "another-api"), ("exp", None), ("exp", True),
    ("exp", float("nan")), ("exp", float("inf")), ("exp", 1),
    # Stable id: a time-derived node id differs per process (breaks quarantine, receipts, CI shards).
    ("nbf", float("nan")), pytest.param("nbf", time.time() + 3600, id="nbf-future"), ("sub", ""), ("sub", []),
    ("exp", 10 ** 400), ("nbf", 10 ** 400), ("roles", "admin"), ("roles", [None]),
    ("tenant_id", []), ("tenant", ""), ("username", {}),
])
def test_even_correctly_signed_invalid_claims_are_rejected(claim, value):
    payload = {"sub": "alice", "iss": "eoip-authn", "aud": "eoip-api", "exp": time.time() + 60}
    payload[claim] = value
    with pytest.raises(ValueError):
        TokenValidator(SECRET).validate_token(_signed(payload))


def test_unsigned_algorithm_and_non_object_claims_are_rejected():
    payload = {"sub": "alice", "iss": "eoip-authn", "aud": "eoip-api", "exp": time.time() + 60}
    with pytest.raises(ValueError):
        TokenValidator(SECRET).validate_token(_signed(payload, {"alg": "none"}))
    with pytest.raises(ValueError):
        TokenValidator(SECRET).validate_token(_signed([]))


def test_conflicting_tenant_claims_are_rejected():
    payload = {"sub": "alice", "iss": "eoip-authn", "aud": "eoip-api", "exp": time.time() + 60,
               "tenant": "alpha", "tenant_id": "beta"}
    with pytest.raises(ValueError, match="conflicting tenant"):
        TokenValidator(SECRET).validate_token(_signed(payload))


def test_no_implicit_signing_secret_and_wrong_signature_rejected():
    with pytest.raises(ValueError, match="explicit"):
        TokenValidator()
    token = TokenService(b"different-secret").issue(Principal("user-1", "alice"))
    with pytest.raises(ValueError):
        TokenValidator(SECRET).validate_token(token)
