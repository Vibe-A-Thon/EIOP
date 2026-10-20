"""``eoip-admin``: explicit provisioning of principals (FT-AUTH).

There is no default account. The first administrator is created explicitly, with the
password supplied through the environment or a file (never a command-line argument, so
it does not land in shell history or ``ps``)::

    EOIP_ADMIN_PASSWORD=... eoip-admin create-admin --username alice
    eoip-admin create-admin --username alice --password-file /run/secrets/admin_password

Container entrypoints run ``eoip-admin from-env``, which provisions only what the
operator configured: EOIP_ADMIN_USERNAME + EOIP_ADMIN_PASSWORD(_FILE) for the first
admin, and EOIP_API_TOKEN + EOIP_API_TOKEN_ROLES to map a service token to its own
principal. It never prints secrets.
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
from pathlib import Path

from eoip.authn.credentials import (
    CredentialError,
    CredentialStore,
    default_credentials_path,
    token_sha256,
)


def _password(args, env_default: str) -> str:
    if getattr(args, "password_file", None):
        return Path(args.password_file).read_text(encoding="utf-8").rstrip("\r\n")
    value = os.environ.get(getattr(args, "password_env", None) or env_default, "")
    if value:
        return value
    if sys.stdin.isatty():
        first = getpass.getpass("Password: ")
        if first != getpass.getpass("Repeat password: "):
            raise CredentialError("passwords do not match")
        return first
    raise CredentialError(f"no password supplied (set {getattr(args, 'password_env', None) or env_default} "
                          "or pass --password-file)")


def _env_password(prefix: str) -> str | None:
    file_value = os.environ.get(f"{prefix}_FILE")
    if file_value:
        return Path(file_value).read_text(encoding="utf-8").rstrip("\r\n")
    return os.environ.get(prefix) or None


def provision_from_env(store: CredentialStore, log=print) -> dict[str, str]:
    """Idempotent provisioning from operator-supplied environment variables."""
    done: dict[str, str] = {}
    admin = os.environ.get("EOIP_ADMIN_USERNAME", "").strip()
    if admin:
        if store.get(admin) is None:
            password = _env_password("EOIP_ADMIN_PASSWORD")
            if not password:
                raise CredentialError("EOIP_ADMIN_USERNAME is set but EOIP_ADMIN_PASSWORD(_FILE) is not")
            store.create_user(admin, password, ("superadmin",))
            done["admin"] = "created"
            log(f"[eoip-admin] created first administrator {admin!r}")
        else:
            done["admin"] = "exists"
            log(f"[eoip-admin] administrator {admin!r} already provisioned; unchanged")
    token = os.environ.get("EOIP_API_TOKEN", "")
    roles = [r for r in os.environ.get("EOIP_API_TOKEN_ROLES", "").split(",") if r.strip()]
    if token and roles:
        if len(token) < 32:
            raise CredentialError("EOIP_API_TOKEN must be at least 32 characters")
        principal = os.environ.get("EOIP_API_TOKEN_PRINCIPAL", "svc-api-token").strip()
        tenant = os.environ.get("EOIP_API_TOKEN_TENANT", "default").strip() or "default"
        if store.get(principal) is None:
            store.create_user(principal, None, roles, tenant_id=tenant)
        else:
            store.set_roles(principal, roles)
        store.register_api_token(principal, token_sha256(token), roles, label="EOIP_API_TOKEN")
        done["api_token"] = principal
        log(f"[eoip-admin] EOIP_API_TOKEN mapped to principal {principal!r} with roles {sorted(roles)}")
    elif token:
        done["api_token"] = "unmapped"
        log("[eoip-admin] EOIP_API_TOKEN is set without EOIP_API_TOKEN_ROLES: it is NOT mapped "
            "to any principal and grants nothing (there is no default role)")
    return done


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="eoip-admin", description=__doc__.splitlines()[0])
    parser.add_argument("--store", type=Path, default=None, help="credential store (default: %(default)s)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("create-admin", help="create the first (or another) superadmin")
    p.add_argument("--username", required=True)
    p.add_argument("--password-env", default="EOIP_ADMIN_PASSWORD")
    p.add_argument("--password-file")

    p = sub.add_parser("add-user", help="create a login user with explicit roles")
    p.add_argument("--username", required=True)
    p.add_argument("--roles", required=True, help="comma separated, e.g. analyst,steward")
    p.add_argument("--tenant", required=True)
    p.add_argument("--password-env", default="EOIP_USER_PASSWORD")
    p.add_argument("--password-file")

    p = sub.add_parser("set-password")
    p.add_argument("--username", required=True)
    p.add_argument("--password-env", default="EOIP_USER_PASSWORD")
    p.add_argument("--password-file")

    p = sub.add_parser("set-roles")
    p.add_argument("--username", required=True)
    p.add_argument("--roles", required=True)

    p = sub.add_parser("disable")
    p.add_argument("--username", required=True)

    p = sub.add_parser("issue-token", help="issue an API token for a principal (written to a 0600 file)")
    p.add_argument("--username", required=True)
    p.add_argument("--roles", default="", help="subset of the principal's roles (default: all)")
    p.add_argument("--label", default="")
    p.add_argument("--output-file", required=True, type=Path)

    p = sub.add_parser("revoke-token")
    p.add_argument("--token-id", required=True)

    sub.add_parser("from-env", help="provision from EOIP_ADMIN_* / EOIP_API_TOKEN_* variables")
    sub.add_parser("list", help="list principals (no secrets)")

    args = parser.parse_args(argv)
    store = CredentialStore(args.store or default_credentials_path())
    split = lambda text: [r.strip() for r in text.split(",") if r.strip()]  # noqa: E731
    try:
        if args.command == "create-admin":
            store.create_user(args.username, _password(args, "EOIP_ADMIN_PASSWORD"), ("superadmin",))
            print(f"created superadmin {args.username!r}")
        elif args.command == "add-user":
            store.create_user(args.username, _password(args, "EOIP_USER_PASSWORD"), split(args.roles),
                              tenant_id=args.tenant)
            print(f"created user {args.username!r}")
        elif args.command == "set-password":
            store.set_password(args.username, _password(args, "EOIP_USER_PASSWORD"))
            print("password updated")
        elif args.command == "set-roles":
            store.set_roles(args.username, split(args.roles))
            print("roles updated")
        elif args.command == "disable":
            store.set_enabled(args.username, False)
            print("user disabled")
        elif args.command == "issue-token":
            token_id, token = store.issue_api_token(args.username, split(args.roles) or None, label=args.label)
            fd = os.open(args.output_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(token + "\n")
            print(f"issued {token_id}; token written to {args.output_file} (mode 0600)")
        elif args.command == "revoke-token":
            print("revoked" if store.revoke_api_token(args.token_id) else "no such active token")
        elif args.command == "from-env":
            provision_from_env(store)
        elif args.command == "list":
            print(json.dumps(store.summary(), indent=2))
    except (CredentialError, OSError) as exc:
        print(f"eoip-admin: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
