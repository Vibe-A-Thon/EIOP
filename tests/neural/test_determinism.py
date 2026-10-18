"""Tests for seeded determinism and environment capture (CRA-043.6)."""
from __future__ import annotations
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
    env = capture_environment()
    assert "python_version" in env
    assert "platform" in env
    assert "threads" in env
    assert env["threads"]["OMP_NUM_THREADS"] is not None
