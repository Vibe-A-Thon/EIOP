"""FT-F04: CI quarantine deselects listed tests visibly and requires a reason."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from eoip.verification.pytest_quarantine import load_quarantine

ROOT = Path(__file__).resolve().parents[2]


def _run(tmp_path: Path, quarantine: str | None) -> subprocess.CompletedProcess[str]:
    (tmp_path / "test_sample.py").write_text(
        "import pytest\n"
        "def test_ok():\n    pass\n"
        "def test_known_red():\n    assert False\n"
        "@pytest.mark.parametrize('x', [1, 2])\n"
        "def test_param(x):\n    assert False\n",
        encoding="utf-8",
    )
    env = {k: v for k, v in os.environ.items() if k != "EOIP_TEST_QUARANTINE_FILE"}
    env["PYTHONPATH"] = os.pathsep.join([str(ROOT / "packages"), str(ROOT)])
    if quarantine is not None:
        qfile = tmp_path / "quarantine.txt"
        qfile.write_text(quarantine, encoding="utf-8")
        env["EOIP_TEST_QUARANTINE_FILE"] = str(qfile)
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-p", "eoip.verification.pytest_quarantine",
         "-p", "no:cacheprovider", "-q", "--rootdir", str(tmp_path), str(tmp_path / "test_sample.py")],
        cwd=tmp_path, env=env, capture_output=True, text=True, timeout=120,
    )


def test_without_env_every_test_runs(tmp_path: Path) -> None:
    result = _run(tmp_path, None)
    assert result.returncode == 1
    assert "3 failed, 1 passed" in result.stdout


def test_listed_tests_are_deselected_and_reported(tmp_path: Path) -> None:
    result = _run(tmp_path, "# header\ntest_sample.py::test_known_red  # FT-X10 D99 needs decision\n"
                            "test_sample.py::test_param  # FT-X10 D98\n")
    assert result.returncode == 0, result.stdout
    assert "1 passed, 3 deselected" in result.stdout
    assert "quarantined tests (3" in result.stdout
    assert "test_sample.py::test_known_red  # FT-X10 D99 needs decision" in result.stdout


def test_entry_without_reason_is_rejected(tmp_path: Path) -> None:
    qfile = tmp_path / "q.txt"
    qfile.write_text("tests/x.py::test_a\n", encoding="utf-8")
    with pytest.raises(pytest.UsageError):
        load_quarantine(qfile)
