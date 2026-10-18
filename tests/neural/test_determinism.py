"""Tests for seeded determinism and environment capture (CRA-043.6)."""
from __future__ import annotations
import subprocess
import sys
import numpy as np
import pytest

from eoip.neural.numerics import seed_everything, capture_environment

def test_seeded_determinism():
    seed_everything(42)
    s1 = np.random.randn(10)

    seed_everything(42)
    s2 = np.random.randn(10)

    assert np.allclose(s1, s2, atol=1e-7)

    # Different seed produces different results
    seed_everything(99)
    s3 = np.random.randn(10)
    assert not np.allclose(s1, s3, atol=1e-4)

def test_capture_environment():
    seed_everything(4242)
    env = capture_environment()
    assert "python_version" in env
    assert "platform" in env
    assert "threads" in env
    assert env["threads"]["OMP_NUM_THREADS"] is not None
    assert env["seeds"]["python_seed"] == 4242
    assert env["numpy_version"] != ""
    assert env["scipy_version"] != ""
    assert env["scikit_learn_version"] != ""
    assert env["blas"]

def test_blas_threads_are_set_before_numpy_import():
    script = """
import builtins
import os

names = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")
observed = {}
original_import = builtins.__import__

def tracked_import(name, *args, **kwargs):
    if name == "numpy" or name.startswith("numpy."):
        observed.update({key: os.environ.get(key) for key in names})
    return original_import(name, *args, **kwargs)

builtins.__import__ = tracked_import
import eoip.neural.numerics
assert observed == {key: "1" for key in names}, observed
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stderr

def test_seed_reproduces_across_processes_and_changes_with_seed():
    script = """
import json
import eoip.neural.numerics as numerics
numerics.seed_everything(SEED)
import numpy as np
print(json.dumps(np.random.random(32).tolist()))
"""

    def sample(seed: int) -> list[float]:
        result = subprocess.run(
            [sys.executable, "-c", script.replace("SEED", str(seed))],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        return np.asarray(__import__("json").loads(result.stdout), dtype=np.float64).tolist()

    assert sample(12345) == sample(12345)
    assert sample(12345) != sample(54321)
