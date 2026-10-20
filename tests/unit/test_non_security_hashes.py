"""FT-F11: MD5/SHA-1 are only used for non-security identifiers and say so.

usedforsecurity=False documents intent (bandit B324 / ruff S324) and keeps these
call sites working on FIPS-mode Python builds, without changing any digest.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def test_usedforsecurity_flag_does_not_change_digests() -> None:
    for algo in (hashlib.md5, hashlib.sha1):
        assert algo(b"proj_1_2").hexdigest() == algo(b"proj_1_2", usedforsecurity=False).hexdigest()


def test_no_unflagged_weak_hashes_or_unannotated_extractall() -> None:
    ruff = shutil.which("ruff")
    cmd = [ruff] if ruff else [sys.executable, "-m", "ruff"]
    try:
        result = subprocess.run(
            [*cmd, "check", "--select", "S324,S202", "--output-format", "concise",
             "packages", "apps", "reva", "backend", "scripts"],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        )
    except FileNotFoundError:
        pytest.skip("ruff not installed")
    if "No module named ruff" in result.stderr:
        pytest.skip("ruff not installed")
    assert result.returncode == 0, result.stdout


def test_hashing_embedder_buckets_are_unchanged() -> None:
    from eoip.retrieval.vectors import HashingEmbedder

    # Golden value computed from the pre-change implementation (plain hashlib.md5).
    digest = hashlib.md5(b"invoice").hexdigest()
    expected = (int(digest[:8], 16) % 256, 1.0 if int(digest[8:16], 16) % 2 == 0 else -1.0)
    assert HashingEmbedder(256)._bucket("invoice") == expected
