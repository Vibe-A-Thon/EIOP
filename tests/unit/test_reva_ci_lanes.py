"""FT-F04: every REVA CI lane runs real checks on push and pull_request."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("check_ci_lanes", ROOT / "scripts/reva/check_ci_lanes.py")
lanes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lanes)
spec2 = importlib.util.spec_from_file_location("run_lane", ROOT / "scripts/reva/run_lane.py")
run_lane = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(run_lane)

PLACEHOLDER = """name: reva-x (NOT IMPLEMENTED)
on:
  workflow_dispatch:
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - run: echo "::error::reva-x NOT IMPLEMENTED" && exit 1
"""
ECHO_ONLY = """name: reva-x
on:
  push:
  pull_request:
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Running reva-x"
"""
REAL = """name: reva-x
# (was a NOT IMPLEMENTED placeholder)
on:
  push:
  pull_request:
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - run: python -m pytest tests/reva/x
"""


def test_placeholder_detection():
    assert lanes.placeholder_reason(PLACEHOLDER) == "marked NOT IMPLEMENTED"
    assert lanes.placeholder_reason(ECHO_ONLY) == "no step runs python/pytest (echo-only)"
    assert lanes.placeholder_reason(REAL.replace("  pull_request:\n", "")) == "does not run on push and pull_request"
    assert lanes.placeholder_reason(REAL) == ""


def test_all_ten_repository_lanes_are_real():
    result = subprocess.run([sys.executable, str(ROOT / "scripts/reva/check_ci_lanes.py")], capture_output=True,
                            text=True, cwd=ROOT, timeout=60)
    assert result.returncode == 0, result.stderr


def test_lane_runner_refuses_zero_test_success_and_failures():
    empty = {"passed": [], "failed": [], "skipped": [{"test": "t", "reason": "r"}]}
    assert any("zero tests passed" in p for p in run_lane.evaluate(empty, 0, 1))
    assert any("zero tests passed" in p for p in run_lane.evaluate(empty, 5, 1))
    ok = {"passed": ["a", "b"], "failed": [], "skipped": []}
    assert run_lane.evaluate(ok, 0, 2) == []
    assert any("requires 3" in p for p in run_lane.evaluate(ok, 0, 3))
    assert any("exited with 1" in p for p in run_lane.evaluate(ok, 1, 1))
    assert any("failed" in p for p in run_lane.evaluate({**ok, "failed": ["c"]}, 0, 1))
