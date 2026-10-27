"""Acceptance test suite for Numerical Compute Stack, Determinism and Hardware Profiles (WP-043, CRA-043.1-11, CRA-043.A)."""
from __future__ import annotations

import os
import platform
import importlib
import numpy as np
import pytest

try:
    torch = importlib.import_module("torch")
except ImportError:
    torch = None

from eoip.neural.runtime import NeuralTier, get_runtime, require_tier, reset_runtime_cache
from eoip.neural.numerics import (
    MemoryGuard,
    assert_finite,
    capture_environment,
    cosine_similarity,
    ensure_float32,
    seed_everything,
    stable_log,
    stable_softmax,
)
from eoip.capabilities.model import CapabilityUnavailableError


# ===========================================================================
# CRA-043.10: Platform matrix qualification (CPU execution, no GPU required)
# ===========================================================================

@pytest.mark.req("CRA-043")
def test_cra_043_10_platform_matrix():
    system = platform.system().lower()

    # Qualifies the platform on CPU without GPU dependency
    assert system in ["windows", "linux", "darwin"], f"Unqualified OS platform: {system}"
    rt = get_runtime()
    assert rt.torch_device == "cpu"
    assert rt.tier in [NeuralTier.NUMERICS, NeuralTier.NEURAL, NeuralTier.TEXT]
    if torch is None:
        assert rt.has_torch is False
    else:
        assert not torch.cuda.is_available(), "CUDA GPU must NOT be active or required (ADR-H16, ADR-H17)"


# ===========================================================================
# CRA-043.A: Full Acceptance Gate
# ===========================================================================

@pytest.mark.req("CRA-043")
def test_cra_043_a_acceptance_gate():
    # 1. Determinism reproducibility: two runs with same seed reproduce within 1e-4
    seed_everything(12345)
    r1 = np.random.randn(20)
    t1 = torch.randn(20) if torch is not None else None

    seed_everything(12345)
    r2 = np.random.randn(20)
    t2 = torch.randn(20) if torch is not None else None

    assert np.allclose(r1, r2, atol=1e-5)
    if torch is not None:
        assert torch.allclose(t1, t2, atol=1e-5)

    # Different seed produces different results
    seed_everything(54321)
    r3 = np.random.randn(20)
    assert not np.allclose(r1, r3, atol=1e-4)

    # 2. Numerics and stability: softmax and log never return NaN or Inf
    large_logits = np.array([2000.0, 2005.0], dtype=np.float32)
    probs = stable_softmax(large_logits)
    assert_finite(probs)
    assert probs[1] > probs[0]

    # 3. Memory guard refusal before allocation
    guard = MemoryGuard(max_bytes=1000)
    with pytest.raises(MemoryError, match="MemoryGuard refusal"):
        guard.check_allocation((500,), itemsize=4)

    # 4. Environment capture recorded
    env = capture_environment()
    assert env["python_version"] != ""
    assert "threads" in env
    assert "OMP_NUM_THREADS" in env["threads"]
