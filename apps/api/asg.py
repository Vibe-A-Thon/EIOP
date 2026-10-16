"""Application Security Group (ASG) — file-backed token RBAC.

Loads an editable credentials file (``Logins_credentials.keys``) that maps API
tokens to roles + tenant. Integrates with the existing ``authenticated_principal``
path in ``apps.api.main``. Design goals (see security audit SEC-001/002/003):

* Multiple roles incl. a ``superadmin`` that implies ``admin`` + ``system`` and is
  cross-tenant; plus ``admin``, ``steward``, ``analyst``, ``viewer`` bound to a tenant.
* A working superadmin ALWAYS exists (fail-safe): the ``EOIP_API_TOKEN`` bootstrap
  credential is registered as superadmin even if the file is missing/empty/broken.
* Tokens are operator-editable in the file (plaintext demo tokens are supported for
  this preview; production should inject a strong bootstrap token via env).
* Constant-time comparison; tokens are never logged or echoed.

File format (pipe-delimited; ``#`` comments and blank lines ignored):

    <token> | <role,role> | <tenant|*> | <username>
"""

from __future__ import annotations

import hmac
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

VALID_ROLES = {"superadmin", "admin", "system", "steward", "analyst", "viewer"}


def expand_roles(roles) -> tuple[str, ...]:
    """superadmin implies admin + system so existing role gates keep working."""
    out = {r.strip() for r in roles if r and r.strip()}
    if "superadmin" in out:
        out.update(("admin", "system"))
    return tuple(sorted(out))


@dataclass(frozen=True)
class ASGEntry:
    token: str
    roles: tuple[str, ...]
    tenant_id: str | None
    username: str
    principal_id: str


@dataclass
class ASG:
    entries: list[ASGEntry] = field(default_factory=list)

    def authenticate(self, supplied: str | None) -> ASGEntry | None:
        if not supplied or len(supplied) > 16_384:
            return None
        presented = supplied.encode("utf-8")
        for e in self.entries:
            if hmac.compare_digest(presented, e.token.encode("utf-8")):
                return e
        return None

    def summary(self) -> list[dict]:
        return [
            {"username": e.username, "roles": list(e.roles), "tenant": e.tenant_id or "*"}
            for e in self.entries
        ]


def _parse_line(line: str) -> ASGEntry | None:
    parts = [p.strip() for p in line.split("|")]
    if len(parts) < 4:
        return None
    token, role_text, tenant, username = parts[0], parts[1], parts[2], parts[3]
    if token.startswith("plain:"):
        token = token[len("plain:"):]
    if not token:
        return None
    roles = expand_roles(role_text.split(","))
    if not roles or not set(roles).issubset(VALID_ROLES):
        return None
    tenant_id = None if tenant in ("*", "", "global", "system") else tenant
    if "superadmin" not in roles and tenant_id is None:
        # Non-superadmins must be tenant-bound; default to 'default' tenant.
        tenant_id = "default"
    return ASGEntry(
        token=token,
        roles=roles,
        tenant_id=tenant_id,
        username=username or "user",
        principal_id=f"urn:eoip:authn:principal:asg:{username or 'user'}",
    )


def load_asg(path: str | None, bootstrap_token: str | None) -> ASG:
    """Build the ASG registry. Never raises — a broken file must not lock out ops."""
    entries: list[ASGEntry] = []
    seen: set[str] = set()
    p = Path(path) if path else None
    if p and p.exists():
        try:
            for raw in p.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if "|" not in line:
                    continue
                entry = _parse_line(line)
                if entry and entry.token not in seen:
                    entries.append(entry)
                    seen.add(entry.token)
        except Exception as exc:  # pragma: no cover - never fatal
            print(f"[asg] failed to parse {p}: {exc}", file=sys.stderr)

    # Fail-safe: the env bootstrap token is ALWAYS a working superadmin.
    if bootstrap_token and bootstrap_token not in seen:
        entries.append(
            ASGEntry(
                token=bootstrap_token,
                roles=expand_roles(("superadmin",)),
                tenant_id=None,
                username="bootstrap-superadmin",
                principal_id="urn:eoip:authn:principal:bootstrap",
            )
        )
        seen.add(bootstrap_token)

    # Guarantee at least one superadmin exists even if someone removed them all.
    if not any("superadmin" in e.roles for e in entries) and bootstrap_token:
        entries.append(
            ASGEntry(
                token=bootstrap_token,
                roles=expand_roles(("superadmin",)),
                tenant_id=None,
                username="bootstrap-superadmin",
                principal_id="urn:eoip:authn:principal:bootstrap",
            )
        )
    return ASG(entries=entries)


def default_keys_path() -> str:
    return os.environ.get(
        "EOIP_ASG_FILE",
        str(Path(__file__).resolve().parent.parent.parent / "Logins_credentials.keys"),
    )
