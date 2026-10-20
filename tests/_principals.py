"""Explicit principal provisioning for tests (FT-AUTH).

The API has no default/bootstrap principal, so every test that calls it provisions the
identity it uses: an ASG token entry with explicit roles, or a login user in the
credential store.
"""

from __future__ import annotations

import hashlib
import os
import secrets
import tempfile
from pathlib import Path


def _set(monkeypatch, name: str, value: str) -> None:
    if monkeypatch is None:
        os.environ[name] = value
    else:
        monkeypatch.setenv(name, value)


def provision_api_token(monkeypatch, token: str, *, roles=("superadmin",), tenant: str = "*",
                        username: str = "test-principal") -> Path:
    """Map ``token`` to a principal with explicit ``roles`` through an ASG file."""
    folder = Path(tempfile.mkdtemp(prefix="eoip-asg-test-"))
    path = folder / "asg.txt"
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
    path.write_text(f"sha256:{digest} | {','.join(roles)} | {tenant} | {username}\n", encoding="utf-8")
    os.chmod(path, 0o400)
    _set(monkeypatch, "EOIP_ASG_FILE", str(path))
    return path


def provision_login_user(monkeypatch, data_dir: Path, username: str, *, roles, tenant: str | None = None,
                         principal_id: str | None = None, password: str | None = None,
                         session_secret: str | None = None) -> str:
    """Create a login user in the credential store under ``data_dir``; returns the password."""
    from eoip.authn.credentials import CredentialStore

    password = password or secrets.token_urlsafe(18)
    store = CredentialStore(Path(data_dir) / "state" / "credentials.json")
    store.create_user(username, password, roles, tenant_id=tenant, principal_id=principal_id)
    if session_secret is not None:
        _set(monkeypatch, "EOIP_SESSION_SECRET", session_secret)
    return password


class ProvisioningTokenService:
    """Wrap a TokenService so every principal it signs for exists in the credential store.

    Session tokens only authenticate provisioned, enabled users (roles are read from the
    store, not from the token), so tests that mint tokens provision the user first.
    """

    def __init__(self, service, data_dir: Path) -> None:
        self._service = service
        self._path = Path(data_dir) / "state" / "credentials.json"

    def issue(self, principal, **kwargs) -> str:
        from eoip.authn.credentials import VALID_ROLES, CredentialStore

        store = CredentialStore(self._path)
        roles = [r for r in principal.roles if r in VALID_ROLES] or ["viewer"]
        tenant = principal.tenant_id or (None if "superadmin" in roles else "default")
        record = store.get(principal.username)
        if record is None:
            store.create_user(principal.username, secrets.token_urlsafe(18), roles,
                              tenant_id=tenant, principal_id=principal.id)
        elif record.principal_id != principal.id or record.tenant_id != tenant:
            raise AssertionError("test reuses a username with a different identity")
        else:
            store.set_roles(principal.username, roles)
        return self._service.issue(principal, **kwargs)

    def __getattr__(self, name):
        return getattr(self._service, name)
