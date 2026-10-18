"""Tests for NeuralTier detection and require_tier (CRA-043.1, CRA-043.4)."""
from __future__ import annotations
import pytest

from eoip.capabilities.model import CapabilityUnavailableError
from eoip.neural.runtime import (
    NeuralTier,
    get_runtime,
    require_tier,
    reset_runtime_cache,
)

def test_get_runtime_detects_system():
    reset_runtime_cache()
    rt = get_runtime()
    assert rt.python_version != ""
    assert rt.os_platform != ""
    assert rt.torch_device == "cpu"  # H-16: CPU-only distribution
    assert isinstance(rt.tier, NeuralTier)

def test_require_tier_enforcement():
    # Numerics tier requirement
    rt = require_tier(NeuralTier.NUMERICS)
    assert rt is not None

def test_require_unavailable_tier_raises_503():
    # Research tier is not installed in standard dev environment
    with pytest.raises(CapabilityUnavailableError) as exc_info:
        require_tier(NeuralTier.RESEARCH)
    assert exc_info.value.status_code == 503
    assert exc_info.value.code == "CAPABILITY_UNAVAILABLE"
    assert "neural-research" in exc_info.value.details["reason"]
