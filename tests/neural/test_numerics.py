"""Tests for numerical substrate: float32, assert_finite, stable softmax/log, memory guard (CRA-043.5, 043.8, 043.9)."""
from __future__ import annotations
import math
import numpy as np
import pytest

from eoip.neural.numerics import (
    assert_finite,
    ensure_float32,
    cosine_similarity,
    stable_softmax,
    stable_log,
    MemoryGuard,
)

def test_assert_finite():
    # Valid finite array
    arr = np.array([1.0, 2.0, 3.5], dtype=np.float32)
    assert_finite(arr)

    # Array containing NaN
    arr_nan = np.array([1.0, float("nan"), 3.0], dtype=np.float32)
    with pytest.raises(ValueError, match="non-finite"):
        assert_finite(arr_nan)

    # Array containing Inf
    arr_inf = np.array([1.0, float("inf"), 3.0], dtype=np.float32)
    with pytest.raises(ValueError, match="non-finite"):
        assert_finite(arr_inf)

def test_ensure_float32():
    arr_f64 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    out = ensure_float32(arr_f64)
    assert out.dtype == np.float32

def test_cosine_similarity():
    v1 = [1.0, 0.0, 0.0]
    v2 = [1.0, 0.0, 0.0]
    assert math.isclose(cosine_similarity(v1, v2), 1.0, abs_tol=1e-5)

    v3 = [0.0, 1.0, 0.0]
    assert math.isclose(cosine_similarity(v1, v3), 0.0, abs_tol=1e-5)

    # Zero vector safety: returns 0.0 without divide by zero
    v_zero = [0.0, 0.0, 0.0]
    assert cosine_similarity(v1, v_zero) == 0.0

def test_stable_softmax_overflow_prevention():
    # Large logits that would overflow standard exp([1000, 1001])
    large_logits = np.array([1000.0, 1001.0], dtype=np.float32)
    probs = stable_softmax(large_logits)
    assert_finite(probs)
    assert math.isclose(np.sum(probs), 1.0, abs_tol=1e-5)
    assert probs[1] > probs[0]

def test_stable_log():
    # Near-zero probabilities
    probs = np.array([0.0, 0.5, 1.0], dtype=np.float32)
    logs = stable_log(probs)
    assert_finite(logs)
    assert logs[0] < -20.0
    assert math.isclose(logs[2], 0.0, abs_tol=1e-5)

def test_memory_guard():
    guard = MemoryGuard(max_bytes=1000)  # 1000 bytes max
    # 200 elements * 4 bytes = 800 bytes (exactly 80% threshold -> allowed)
    guard.check_allocation((200,), itemsize=4)

    # 300 elements * 4 bytes = 1200 bytes (> 800 bytes -> refused)
    with pytest.raises(MemoryError, match="MemoryGuard refusal"):
        guard.check_allocation((300,), itemsize=4)
