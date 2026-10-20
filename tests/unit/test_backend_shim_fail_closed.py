"""FT-F02 / FT-AUTH: backend/server.py has no default token or account and fails closed."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SERVER = REPO_ROOT / "backend" / "server.py"
_STUB_APP = (
    "import os, runpy, sys\n"
    "sys.modules['apps.api.main'] = type(sys)('apps.api.main')\n"
    "sys.modules['apps.api.main'].create_app = lambda: type('A', (), {'state': type('S', (), {})()})()\n"
    f"runpy.run_path(r'{SERVER}')\n"
)


def _env(tmp_path, **extra):
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("EOIP_API_TOKEN", "EOIP_ENV", "EOIP_ASG", "EOIP_REVOKED", "EOIP_LOAD_DEMO",
                                "EOIP_ADMIN", "EOIP_CREDENTIALS", "EOIP_SESSION"))}
    env.update({"EOIP_DATA_DIR": str(tmp_path / "data"), "EOIP_GRAPH_BACKEND": "memory",
                "PYTHONPATH": os.pathsep.join([str(REPO_ROOT), str(REPO_ROOT / "packages")])})
    env.update(extra)
    return env


def test_server_source_has_no_token_or_account_default():
    text = SERVER.read_text(encoding="utf-8")
    assert 'setdefault("EOIP_API_TOKEN"' not in text
    assert "EOIP_LOAD_DEMO\", \"true\")" not in text
    assert "dev-token" not in text and "token_urlsafe" not in text


def test_without_any_principal_the_app_refuses_to_start(tmp_path):
    proc = subprocess.run(
        [sys.executable, "-c", "import runpy; runpy.run_path(r'%s')" % SERVER],
        env=_env(tmp_path, EOIP_ENV="dev"), capture_output=True, text=True, timeout=120,
    )
    assert proc.returncode != 0
    assert "no principals configured" in proc.stderr


def test_unmapped_api_token_grants_nothing(tmp_path):
    proc = subprocess.run([sys.executable, "-c", _STUB_APP], capture_output=True, text=True, timeout=120,
                          env=_env(tmp_path, EOIP_API_TOKEN="t" * 40))
    assert proc.returncode == 0, proc.stderr
    assert "NOT mapped" in proc.stderr
    assert not (tmp_path / "data" / "state" / "credentials.json").exists()


def test_first_admin_is_provisioned_only_from_explicit_env(tmp_path):
    password = "correct horse battery staple"
    env = _env(tmp_path, EOIP_ADMIN_USERNAME="ops-admin", EOIP_ADMIN_PASSWORD=password)
    proc = subprocess.run([sys.executable, "-c", _STUB_APP], env=env, capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stderr
    assert password not in proc.stdout + proc.stderr
    store = json.loads((tmp_path / "data" / "state" / "credentials.json").read_text(encoding="utf-8"))
    (user,) = store["users"]
    assert user["username"] == "ops-admin" and "superadmin" in user["roles"]
    assert user["password_hash"].startswith("$argon2id$") and password not in json.dumps(store)
    if os.name == "posix":
        assert (tmp_path / "data" / "state" / "credentials.json").stat().st_mode & 0o077 == 0
