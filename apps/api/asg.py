"""Application Security Group (ASG) — file-backed token RBAC, fail closed.

Maps API tokens to roles + tenant and plugs into ``authenticated_principal`` in
``apps.api.main``. Security properties (FT-F01 / FT-F02, audit findings F-01/F-02):

* No default credentials file. The registry is read only from ``EOIP_ASG_FILE``;
  there is no repository-root fallback any more.
* Tokens are stored as ``sha256:<hex>`` digests, never in plaintext. Plaintext
  entries are accepted only in an explicit development profile
  (``EOIP_ENV=dev`` **and** ``EOIP_ASG_ALLOW_PLAINTEXT=true``).
* A configured file that is missing, unreadable, malformed, group/world
  accessible (POSIX), or that contains a revoked digest is FATAL at startup.
* ``EOIP_REVOKED_TOKEN_SHA256_FILE`` (newline-separated sha256 hex) is a
  revocation denylist checked for every entry.
* There is no bootstrap or default principal (FT-AUTH): ``EOIP_API_TOKEN`` is not
  registered here. Every token maps to the explicit roles written on its line;
  login users and their API tokens live in :mod:`eoip.authn.credentials`.
* Comparison is constant time over every entry (no early exit); token values are
  never logged or echoed — ``summary()`` exposes usernames and roles only.

File format (pipe-delimited; ``#`` comments and blank lines ignored):

    sha256:<64 hex> | <role,role> | <tenant|*> | <username>

Create a digest without echoing the token, e.g.::

    python -c "import getpass,hashlib;print('sha256:'+hashlib.sha256(getpass.getpass().encode()).hexdigest())"
"""

from __future__ import annotations

import hashlib
import hmac
import os
import re
import stat
from dataclasses import dataclass, field
from pathlib import Path

from eoip.authn.credentials import VALID_ROLES, expand_roles  # noqa: E402,F401
ASG_FILE_ENV = "EOIP_ASG_FILE"
REVOKED_SHA256_FILE_ENV = "EOIP_REVOKED_TOKEN_SHA256_FILE"
MIN_TOKEN_LENGTH = 32
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class ASGConfigurationError(RuntimeError):
    """Raised when the ASG configuration is insecure or invalid (fail closed)."""


def token_digest(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _dev_profile() -> bool:
    return os.environ.get("EOIP_ENV", "").strip().lower() == "dev"


def _plaintext_allowed() -> bool:
    return _dev_profile() and os.environ.get("EOIP_ASG_ALLOW_PLAINTEXT", "").strip().lower() == "true"


@dataclass(frozen=True)
class ASGEntry:
    token_sha256: str
    roles: tuple[str, ...]
    tenant_id: str | None
    username: str
    principal_id: str

    def __repr__(self) -> str:  # never include the digest in logs/tracebacks
        return f"ASGEntry(username={self.username!r}, roles={self.roles!r}, tenant_id={self.tenant_id!r})"


@dataclass
class ASG:
    entries: list[ASGEntry] = field(default_factory=list)

    def authenticate(self, supplied: str | None) -> ASGEntry | None:
        if not supplied or len(supplied) > 16_384:
            return None
        presented = token_digest(supplied).encode("ascii")
        hit: ASGEntry | None = None
        for e in self.entries:  # constant time: always walk every entry
            if hmac.compare_digest(presented, e.token_sha256.encode("ascii")) and hit is None:
                hit = e
        return hit

    def summary(self) -> list[dict]:
        return [
            {"username": e.username, "roles": list(e.roles), "tenant": e.tenant_id or "*"}
            for e in self.entries
        ]


def load_revoked_digests(path: str | None = None) -> set[str]:
    path = path if path is not None else os.environ.get(REVOKED_SHA256_FILE_ENV)
    if not path:
        return set()
    p = Path(path)
    try:
        text = p.read_text(encoding="utf-8")
    except OSError as exc:
        raise ASGConfigurationError(f"{REVOKED_SHA256_FILE_ENV} is set but unreadable: {p}") from exc
    out: set[str] = set()
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip().lower().removeprefix("sha256:")
        if not line or line.startswith("#"):
            continue
        if not _HEX64.match(line):
            raise ASGConfigurationError(f"{p}:{n}: expected a sha256 hex digest")
        out.add(line)
    return out


def _check_permissions(p: Path) -> None:
    if os.name != "posix":
        return
    mode = p.stat().st_mode
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        raise ASGConfigurationError(
            f"{p} must not be group/world accessible (chmod 400; Kubernetes: defaultMode 0400)"
        )


def _parse_line(line: str, where: str) -> ASGEntry:
    parts = [p.strip() for p in line.split("|")]
    if len(parts) < 4:
        raise ASGConfigurationError(f"{where}: expected '<sha256:hex> | <roles> | <tenant|*> | <username>'")
    token, role_text, tenant, username = parts[0], parts[1], parts[2], parts[3]
    if token.lower().startswith("sha256:"):
        digest = token[len("sha256:"):].strip().lower()
        if not _HEX64.match(digest):
            raise ASGConfigurationError(f"{where}: malformed sha256 digest")
    elif _plaintext_allowed():
        plain = token.removeprefix("plain:")
        if len(plain) < MIN_TOKEN_LENGTH:
            raise ASGConfigurationError(f"{where}: token shorter than {MIN_TOKEN_LENGTH} characters")
        digest = token_digest(plain)
    else:
        raise ASGConfigurationError(
            f"{where}: plaintext ASG token rejected; store 'sha256:<hex>' "
            "(plaintext is allowed only with EOIP_ENV=dev and EOIP_ASG_ALLOW_PLAINTEXT=true)"
        )
    roles = expand_roles(role_text.split(","))
    if not roles or not set(roles).issubset(VALID_ROLES):
        raise ASGConfigurationError(f"{where}: unknown role in {role_text!r}")
    tenant_id = None if tenant in ("*", "", "global", "system") else tenant
    if "superadmin" not in roles and tenant_id is None:
        # Non-superadmins must be tenant-bound; default to 'default' tenant.
        tenant_id = "default"
    username = username or "user"
    return ASGEntry(
        token_sha256=digest,
        roles=roles,
        tenant_id=tenant_id,
        username=username,
        principal_id=f"urn:eoip:authn:principal:asg:{username}",
    )


def load_asg(path: str | None, *, revoked: set[str] | None = None, allow_empty: bool = False) -> ASG:
    """Build the ASG registry. Fail closed: any configuration problem raises.

    ``allow_empty`` lets the API start with principals from the credential store only;
    the caller must still refuse to start when no principal exists anywhere.
    """
    revoked = load_revoked_digests() if revoked is None else revoked
    entries: list[ASGEntry] = []
    seen: set[str] = set()
    if path:
        p = Path(path)
        if not p.is_file():
            raise ASGConfigurationError(f"{ASG_FILE_ENV} points to a missing file: {p}")
        _check_permissions(p)
        try:
            text = p.read_text(encoding="utf-8")
        except OSError as exc:
            raise ASGConfigurationError(f"{ASG_FILE_ENV} is unreadable: {p}") from exc
        for n, raw in enumerate(text.splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            entry = _parse_line(line, f"{p.name}:{n}")
            if entry.token_sha256 in revoked:
                raise ASGConfigurationError(f"{p.name}:{n}: entry for {entry.username!r} uses a revoked token")
            if entry.token_sha256 in seen:
                raise ASGConfigurationError(f"{p.name}:{n}: duplicate token")
            entries.append(entry)
            seen.add(entry.token_sha256)

    if not entries and not allow_empty:
        raise ASGConfigurationError("no principals configured; refusing to start")
    return ASG(entries=entries)


def default_keys_path() -> str | None:
    """Path of the ASG file, or None. There is deliberately no repository fallback."""
    return os.environ.get(ASG_FILE_ENV) or None
