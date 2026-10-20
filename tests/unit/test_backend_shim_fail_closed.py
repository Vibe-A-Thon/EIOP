"""FT-F02: backend/server.py has no committed default token and fails closed."""

from __future__ import annotations

import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SERVER = REPO_ROOT / "backend" / "server.py"


def _env(tmp_path, **extra):
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("EOIP_API_TOKEN", "EOIP_ENV", "EOIP_ASG", "EOIP_REVOKED", "EOIP_LOAD_DEMO"))}
    env.update({"EOIP_DATA_DIR": str(tmp_path / "data"), "EOIP_GRAPH_BACKEND": "memory",
                "PYTHONPATH": os.pathsep.join([str(REPO_ROOT), str(REPO_ROOT / "packages")])})
    env.update(extra)
    return env


def test_server_source_has_no_token_default():
    text = SERVER.read_text(encoding="utf-8")
    assert 'setdefault("EOIP_API_TOKEN"' not in text
    assert "EOIP_LOAD_DEMO\", \"true\")" not in text


def test_import_without_token_outside_dev_exits_nonzero(tmp_path):
    proc = subprocess.run(
        [sys.executable, "-c", "import runpy; runpy.run_path(r'%s')" % SERVER],
        env=_env(tmp_path), capture_output=True, text=True, timeout=120,
    )
    assert proc.returncode != 0
    assert "EOIP_API_TOKEN is required" in proc.stderr


@pytest.mark.skipif(os.name != "posix", reason="POSIX permission bits")
def test_dev_profile_generates_private_ephemeral_token(tmp_path):
    code = (
        "import os, runpy, sys\n"
        "sys.modules['apps.api.main'] = type(sys)('apps.api.main')\n"
        "sys.modules['apps.api.main'].create_app = lambda: type('A', (), {'state': type('S', (), {})()})()\n"
        f"runpy.run_path(r'{SERVER}')\n"
        "print(len(os.environ['EOIP_API_TOKEN']), os.environ['EOIP_LOAD_DEMO'])\n"
    )
    proc = subprocess.run([sys.executable, "-c", code], env=_env(tmp_path, EOIP_ENV="dev"),
                          capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stderr
    length, demo = proc.stdout.split()[-2:]
    assert int(length) >= 32 and demo == "true"
    token_file = tmp_path / "data" / "dev-token"
    assert stat.S_IMODE(token_file.stat().st_mode) == 0o600
    assert token_file.read_text(encoding="utf-8") not in proc.stdout + proc.stderr
