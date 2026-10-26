"""FT-AUTH: identity-derived roles, no default principal, fail-closed authentication paths."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest
from eoip.authn import Principal, TokenService
from eoip.authn.credentials import CredentialError, CredentialStore
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

import apps.api.main as api_main
from apps.api.asg import ASGConfigurationError

pytestmark = [pytest.mark.security]

SECRET = "s" * 48
PASSWORDS = {
    "root": "root-password-123456",
    "ada": "admin-password-123456",
    "stew": "steward-password-123456",
    "ana": "analyst-password-123456",
    "vic": "viewer-password-123456",
}
ROLES = {"root": ("superadmin",), "ada": ("admin",), "stew": ("steward",), "ana": ("analyst", "viewer"),
         "vic": ("viewer",)}


@pytest.fixture
def env(tmp_path, monkeypatch):
    for key in ("EOIP_ASG_FILE", "EOIP_API_TOKEN", "EOIP_CREDENTIALS_FILE", "EOIP_SSO_PROVIDER",
                "EOIP_REVOKED_TOKEN_SHA256_FILE"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("EOIP_SESSION_SECRET", SECRET)
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)
    return tmp_path


@pytest.fixture
def store(env) -> CredentialStore:
    s = CredentialStore(env / "state" / "credentials.json")
    for name, roles in ROLES.items():
        s.create_user(name, PASSWORDS[name], roles, tenant_id="default")
    return s


@pytest.fixture
def client(store):
    with TestClient(api_main.create_app()) as c:
        yield c


def _login(client, username, password):
    return client.post("/api/v1/auth/login", json={"username": username, "password": password})


def _bearer(token):
    return {"Authorization": f"Bearer {token}"}


def _whoami(client, token):
    return client.get("/api/v1/auth/whoami", headers=_bearer(token))


# -- fail closed: no default principal ------------------------------------------------

def test_app_refuses_to_start_without_any_principal(env, monkeypatch):
    monkeypatch.setenv("EOIP_API_TOKEN", "t" * 40)  # an injected token alone is not an identity
    with pytest.raises(ASGConfigurationError, match="no principals configured"):
        api_main.create_app()


def test_unmapped_api_token_and_anonymous_requests_are_rejected(store, monkeypatch):
    token = "u" * 40
    monkeypatch.setenv("EOIP_API_TOKEN", token)
    with TestClient(api_main.create_app()) as c:
        assert c.get("/api/v1/auth/whoami", headers=_bearer(token)).status_code == 401
        assert c.get("/api/v1/admin/jobs").status_code == 401
        assert c.get("/api/v1/admin/jobs", headers=_bearer("garbage")).status_code == 401


# -- login credentials (primary path) -------------------------------------------------

@pytest.mark.parametrize("username", sorted(ROLES))
def test_login_returns_session_with_roles_from_the_user_record(client, username):
    res = _login(client, username, PASSWORDS[username])
    assert res.status_code == 200
    me = _whoami(client, res.json()["token"]).json()
    expected = set(ROLES[username]) | ({"admin", "system"} if "superadmin" in ROLES[username] else set())
    assert set(me["roles"]) == expected
    assert me["provider"] == "session"
    assert me["tenant_id"] == (None if username == "root" else "default")


@pytest.mark.parametrize("username,password", [
    ("vic", "wrong-password-123456"), ("nobody", "whatever-password-1"), ("vic", ""), ("", ""),
])
def test_bad_credentials_get_the_same_401(client, username, password):
    res = _login(client, username, password)
    assert res.status_code in (401, 422)
    if res.status_code == 401:
        assert res.json()["detail"] == "invalid credentials"


def test_disabled_user_and_service_principal_cannot_log_in(client, store):
    store.set_enabled("vic", False)
    assert _login(client, "vic", PASSWORDS["vic"]).status_code == 401
    store.create_user("svc-mcp", None, ("viewer",), tenant_id="default")
    assert _login(client, "svc-mcp", "").status_code in (401, 422)


def test_repeated_failures_lock_the_username(client):
    for _ in range(10):
        assert _login(client, "ana", "wrong-password-123456").status_code == 401
    assert _login(client, "ana", PASSWORDS["ana"]).status_code == 401
    assert _login(client, "vic", PASSWORDS["vic"]).status_code == 200  # other users unaffected


def test_session_follows_role_changes_disable_and_logout(client, store):
    token = _login(client, "ana", PASSWORDS["ana"]).json()["token"]
    store.set_roles("ana", ("viewer",))
    assert _whoami(client, token).json()["roles"] == ["viewer"]  # never trusted from the token
    assert client.post("/api/v1/auth/logout", headers=_bearer(token)).status_code == 204
    assert _whoami(client, token).status_code == 401
    token = _login(client, "vic", PASSWORDS["vic"]).json()["token"]
    store.set_enabled("vic", False)
    assert _whoami(client, token).status_code == 401


def test_forged_tampered_and_expired_sessions_are_rejected(client):
    alice = Principal("urn:eoip:authn:principal:local:root", "root", ("superadmin",))
    other_secret = TokenService(b"x" * 48, issuer="eoip-authn", audience="eoip-api")
    assert _whoami(client, other_secret.issue(alice)).status_code == 401
    ours = TokenService(SECRET.encode(), issuer="eoip-authn", audience="eoip-api")
    assert _whoami(client, ours.issue(alice, ttl_seconds=-5)).status_code == 401
    valid = _login(client, "root", PASSWORDS["root"]).json()["token"]
    assert _whoami(client, valid[:-3] + "abc").status_code == 401
    ghost = Principal("urn:eoip:authn:principal:local:ghost", "ghost", ("superadmin",))
    assert _whoami(client, ours.issue(ghost)).status_code == 401  # signed but not provisioned


def test_viewer_is_forbidden_on_admin_surfaces_and_admin_is_not(client):
    viewer = _login(client, "vic", PASSWORDS["vic"]).json()["token"]
    admin = _login(client, "ada", PASSWORDS["ada"]).json()["token"]
    body = {"user_id": "u1", "roles": ["viewer"]}
    assert client.post("/api/v1/authz/users", json=body, headers=_bearer(viewer)).status_code == 403
    assert client.post("/api/v1/authz/users", json=body, headers=_bearer(admin)).status_code != 403


# -- API tokens: mapped to a principal with their own roles ---------------------------

def test_api_token_carries_its_own_subset_of_roles(client, store):
    token_id, token = store.issue_api_token("ada", label="ci")
    me = _whoami(client, token).json()
    assert me["roles"] == ["admin"] and me["provider"] == "api-token"
    with pytest.raises(CredentialError, match="subset"):
        store.issue_api_token("vic", ("admin",))
    _, narrow = store.issue_api_token("ana", ("viewer",))
    assert _whoami(client, narrow).json()["roles"] == ["viewer"]
    assert store.revoke_api_token(token_id)
    assert _whoami(client, token).status_code == 401


def test_api_token_never_exceeds_its_principal(client, store):
    _, token = store.issue_api_token("ana")
    store.set_roles("ana", ("viewer",))
    assert _whoami(client, token).json()["roles"] == ["viewer"]
    store.set_enabled("ana", False)
    assert _whoami(client, token).status_code == 401


def test_asg_file_token_role_comes_from_its_entry(env, store, monkeypatch):
    token = "asg-token-" + "z" * 40
    path = env / "asg"
    path.write_text(f"sha256:{hashlib.sha256(token.encode()).hexdigest()} | steward | acme | etl\n")
    os.chmod(path, 0o400)
    monkeypatch.setenv("EOIP_ASG_FILE", str(path))
    with TestClient(api_main.create_app()) as c:
        me = _whoami(c, token).json()
    assert me["roles"] == ["steward"] and me["tenant_id"] == "acme" and me["provider"] == "asg"


# -- SSO (disabled unless configured; see tests/security/test_sso_keycloak.py) --------

def test_sso_is_disabled_by_default_and_fails_closed_when_misconfigured(client, monkeypatch):
    providers = client.get("/api/v1/auth/providers").json()
    assert providers["local"]["enabled"] is True
    assert {p["name"]: p["enabled"] for p in providers["sso"]} == {"oidc": False, "saml": False}
    assert client.get("/api/v1/auth/sso/oidc/login").status_code == 501
    assert client.get("/api/v1/auth/sso/nope/login").status_code == 404
    assert client.get("/api/v1/auth/sso/oidc/callback", params={"state": "x" * 20, "code": "c"}).status_code == 404
    assert client.post("/api/v1/auth/sso/saml/acs", data={"SAMLResponse": "eA=="}).status_code == 404
    monkeypatch.setenv("EOIP_SSO_PROVIDER", "oidc")
    with pytest.raises(RuntimeError, match="EOIP_OIDC_ISSUER"):
        api_main.create_app()
    monkeypatch.setenv("EOIP_SSO_PROVIDER", "kerberos")
    with pytest.raises(RuntimeError, match="unknown SSO provider"):
        api_main.create_app()


# -- storage and provisioning ---------------------------------------------------------

def test_passwords_are_argon2id_and_store_is_private(store):
    raw = (store.path).read_text()
    data = json.loads(raw)
    assert all(u["password_hash"].startswith("$argon2id$") for u in data["users"])
    assert not any(p in raw for p in PASSWORDS.values())
    if os.name == "posix":
        assert stat.S_IMODE(store.path.stat().st_mode) == 0o600


def test_weak_passwords_unknown_roles_and_roleless_users_are_rejected(env):
    s = CredentialStore(env / "c.json")
    with pytest.raises(CredentialError, match="at least"):
        s.create_user("a", "short", ("viewer",), tenant_id="default")
    with pytest.raises(CredentialError, match="unknown role"):
        s.create_user("a", "long-enough-password", ("root",), tenant_id="default")
    with pytest.raises(CredentialError, match="no default role"):
        s.create_user("a", "long-enough-password", (), tenant_id="default")
    with pytest.raises(CredentialError, match="tenant"):
        s.create_user("a", "long-enough-password", ("viewer",))


def _cli(tmp_path, *args, **env):
    clean = {k: v for k, v in os.environ.items() if not k.startswith(("EOIP_ADMIN", "EOIP_USER_PASSWORD"))}
    clean.update(env)
    return subprocess.run([sys.executable, "-m", "eoip.authn.provision", "--store", str(tmp_path / "c.json"), *args],
                          env=clean, capture_output=True, text=True, input="", timeout=120)  # a pipe: NUL isatty() on Windows


def test_first_admin_requires_explicitly_supplied_credentials(tmp_path):
    proc = _cli(tmp_path, "create-admin", "--username", "boss")
    assert proc.returncode == 2 and "no password supplied" in proc.stderr
    assert not (tmp_path / "c.json").exists()
    secret = "a-very-long-admin-password"
    proc = _cli(tmp_path, "create-admin", "--username", "boss", EOIP_ADMIN_PASSWORD=secret)
    assert proc.returncode == 0, proc.stderr
    assert secret not in proc.stdout + proc.stderr
    assert CredentialStore(tmp_path / "c.json").verify_password("boss", secret).roles == ("admin", "superadmin", "system")


def test_issue_token_writes_a_private_file_and_never_prints_it(tmp_path):
    _cli(tmp_path, "add-user", "--username", "etl", "--roles", "steward", "--tenant", "default",
         EOIP_USER_PASSWORD="etl-password-123456")
    out = tmp_path / "token.txt"
    proc = _cli(tmp_path, "issue-token", "--username", "etl", "--output-file", str(out))
    assert proc.returncode == 0, proc.stderr
    token = out.read_text().strip()
    assert token not in proc.stdout + proc.stderr
    if os.name == "posix":
        assert stat.S_IMODE(out.stat().st_mode) == 0o600
    assert CredentialStore(tmp_path / "c.json").authenticate_api_token(token).roles == ("steward",)


def test_from_env_maps_service_token_only_with_explicit_roles(tmp_path):
    token = "m" * 40
    proc = _cli(tmp_path, "from-env", EOIP_API_TOKEN=token)
    assert proc.returncode == 0 and "NOT mapped" in proc.stdout
    assert CredentialStore(tmp_path / "c.json").authenticate_api_token(token) is None
    proc = _cli(tmp_path, "from-env", EOIP_API_TOKEN=token, EOIP_API_TOKEN_ROLES="analyst",
                EOIP_API_TOKEN_PRINCIPAL="svc-mcp")
    assert proc.returncode == 0, proc.stderr
    principal = CredentialStore(tmp_path / "c.json").authenticate_api_token(token)
    assert principal.username == "svc-mcp" and principal.roles == ("analyst",)
    assert token not in proc.stdout + proc.stderr


def test_no_default_credentials_in_source():
    root = Path(__file__).resolve().parents[2]
    for rel in ("apps/api/asg.py", "apps/api/main.py", "backend/server.py", "packages/eoip/authn/provision.py",
                "frontend/src/screens/SignIn.tsx", "frontend/src/lib/auth.tsx"):
        text = (root / rel).read_text(encoding="utf-8")
        assert "EOIP_BOOTSTRAP_SUPERADMIN" not in text, rel
        assert "bootstrap-superadmin" not in text and "bootstrap-admin" not in text, rel
