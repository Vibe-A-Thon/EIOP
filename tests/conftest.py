"""Shared test bootstrap for subprocess-based CLI tests."""

from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPO_ROOT / "packages"

for path in (REPO_ROOT, PACKAGE_ROOT):
    value = str(path)
    if value not in sys.path:
        sys.path.insert(0, value)

existing = [part for part in os.environ.get("PYTHONPATH", "").split(os.pathsep) if part]
desired = [str(REPO_ROOT), str(PACKAGE_ROOT)]
os.environ["PYTHONPATH"] = os.pathsep.join(desired + [part for part in existing if part not in desired])

pytest_plugins = [
    "eoip.verification.pytest_evidence",
    "eoip.verification.pytest_quarantine",
    "eoip.verification.pytest_shard",
]

