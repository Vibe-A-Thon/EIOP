"""Tests for numerical substrate: float32, assert_finite, stable softmax/log, memory guard (CRA-043.5, 043.8, 043.9)."""
from __future__ import annotations
import math
import subprocess
import sys
import numpy as np
import pytest

from eoip.neural.numerics import (
    assert_finite,
    ensure_float32,
    cosine_similarity,
    cosine_matrix,
    l2_normalize,
    stable_softmax,
    stable_log,
    MemoryGuard,
    to_array,
    to_list,
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

def test_vector_conversion_and_batched_cosine():
    query = to_array([1.0, 0.0, 0.0])
    matrix = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], dtype=np.float32)

    assert query.dtype == np.float32
    assert to_list(query) == [1.0, 0.0, 0.0]
    assert np.array_equal(to_array(to_list(query)), query)
    assert np.allclose(cosine_matrix(query, matrix), [1.0, 0.0], atol=1e-6)
    assert cosine_matrix(query, np.empty((0, 3), dtype=np.float32)).shape == (0,)

def test_l2_normalize_zero_and_empty_inputs():
    matrix = np.array([[3.0, 4.0], [0.0, 0.0]], dtype=np.float32)
    normalized = l2_normalize(matrix)

    assert np.allclose(normalized[0], [0.6, 0.8], atol=1e-6)
    assert np.array_equal(normalized[1], [0.0, 0.0])
    assert l2_normalize(np.empty((0, 2), dtype=np.float32)).shape == (0, 2)
    assert stable_softmax(np.array([], dtype=np.float32)).shape == (0,)

def test_numerics_imports_without_optional_packages():
    script = """
import importlib.abc
import sys
sys.path.insert(0, 'packages')

class BlockOptionalNumerics(importlib.abc.MetaPathFinder):
    blocked = {'numpy', 'scipy', 'sklearn', 'torch', 'torch_geometric', 'transformers'}

    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in self.blocked:
            raise ModuleNotFoundError(f'Optional dependency blocked by test: {fullname}')
        return None

sys.meta_path.insert(0, BlockOptionalNumerics())
from eoip.neural import numerics
assert not numerics.HAS_NUMPY
assert not numerics.HAS_TORCH
assert numerics.cosine_matrix([1.0, 0.0], [[1.0, 0.0], [0.0, 1.0]]) == [1.0, 0.0]
assert numerics.l2_normalize([3.0, 4.0]) == [0.6, 0.8]
assert numerics.stable_softmax([]) == []
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stderr

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
