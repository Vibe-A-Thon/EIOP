"""PLAN-N01: every tracked Python source must compile (no NUL bytes, no syntax errors)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def _tracked_python() -> list[str]:
    try:
        out = subprocess.run(["git", "ls-files", "-z", "--", "packages/*.py", "apps/*.py", "reva/*.py"],
                             cwd=REPO_ROOT, capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("not a git checkout")
    return [p for p in out.decode().split("\0") if p]


def test_product_python_sources_have_no_nul_bytes_and_compile():
    failures = []
    for rel in _tracked_python():
        data = (REPO_ROOT / rel).read_bytes()
        if b"\x00" in data:
            line = data[: data.index(b"\x00")].count(b"\n") + 1
            failures.append(f"{rel}: NUL byte at line {line}")
            continue
        try:
            compile(data, rel, "exec", dont_inherit=True)
        except SyntaxError as exc:
            failures.append(f"{rel}:{exc.lineno}: {exc.msg}")
    assert not failures, "\n".join(failures)


def test_temporal_rag_prop_valid_keeps_missing_observed_at():
    from eoip.ragx.architectures import TemporalRAG

    assert TemporalRAG._prop_valid({}, None, "2026-01-01T00:00:00Z") is True
    assert TemporalRAG._prop_valid({"observed_at": "2027-01-01"}, None, "2026-01-01") is False
    assert TemporalRAG._prop_valid({"observed_at": "2025-01-01"}, None, "2026-01-01") is True
