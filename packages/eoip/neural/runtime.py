"""Numerical and Neural Compute Runtime tiers (CRA-043, ADR-H15, ADR-H16)."""
from __future__ import annotations
import importlib, os, platform, sys
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel

from eoip.capabilities.model import CapabilityState, CapabilityUnavailableError
from eoip.capabilities.registry import get_capability_registry

class NeuralTier(str, Enum):
    NONE = "none"
    NUMERICS = "numerics"          # N0: numpy, scipy
    NEURAL = "neural"              # N1: torch (CPU-only), torch_geometric, scikit-learn
    TEXT = "neural-text"          # N2: transformers, tokenizers, sentence-transformers
    RESEARCH = "neural-research"  # N3: experimental graph research packages

class NeuralRuntime(BaseModel):
    tier: NeuralTier
    has_numpy: bool
    has_scipy: bool
    has_sklearn: bool
    has_torch: bool
    has_torch_geometric: bool
    has_transformers: bool
    torch_device: str = "cpu"
    python_version: str
    os_platform: str

_CACHED_RUNTIME: Optional[NeuralRuntime] = None

def _probe_import(module_name: str) -> bool:
    try:
        importlib.import_module(module_name)
        return True
    except Exception:
        return False

def get_runtime() -> NeuralRuntime:
    """Inspect installed libraries and return current active NeuralTier (never raises)."""
    global _CACHED_RUNTIME
    if _CACHED_RUNTIME is not None:
        return _CACHED_RUNTIME

    has_np = _probe_import("numpy")
    has_sp = _probe_import("scipy")
    has_sk = _probe_import("sklearn")
    has_torch = _probe_import("torch")
    has_pyg = _probe_import("torch_geometric")
    has_tf = _probe_import("transformers")

    # Determine highest available tier
    tier = NeuralTier.NONE
    if has_np and has_sp:
        tier = NeuralTier.NUMERICS
        if has_torch and has_sk:
            tier = NeuralTier.NEURAL
            if has_tf:
                tier = NeuralTier.TEXT

    device = "cpu"
    if has_torch:
        try:
            import torch
            # H-16: EOIP distributes CPU-only builds
            device = "cpu"
        except Exception:
            pass

    _CACHED_RUNTIME = NeuralRuntime(
        tier=tier,
        has_numpy=has_np,
        has_scipy=has_sp,
        has_sklearn=has_sk,
        has_torch=has_torch,
        has_torch_geometric=has_pyg,
        has_transformers=has_tf,
        torch_device=device,
        python_version=platform.python_version(),
        os_platform=platform.platform(),
    )
    return _CACHED_RUNTIME

def reset_runtime_cache() -> None:
    global _CACHED_RUNTIME
    _CACHED_RUNTIME = None

def require_tier(required: NeuralTier) -> NeuralRuntime:
    """Check that current runtime satisfies the required tier.
    Raises CapabilityUnavailableError (HTTP 503) if tier is missing.
    """
    rt = get_runtime()
    tier_order = [NeuralTier.NONE, NeuralTier.NUMERICS, NeuralTier.NEURAL, NeuralTier.TEXT, NeuralTier.RESEARCH]
    curr_idx = tier_order.index(rt.tier)
    req_idx = tier_order.index(required)
    if curr_idx < req_idx:
        raise CapabilityUnavailableError(
            capability_id=f"tier.{required.value}",
            reason=f"Numerical tier '{required.value}' is missing. Install with pip install -e '.[{required.value}]'",
        )
    return rt

def register_neural_capabilities() -> None:
    """Register numerical tiers into CapabilityRegistry."""
    reg = get_capability_registry()
    rt = get_runtime()
    
    tiers = [
        (NeuralTier.NUMERICS, "CRA-043.1", lambda: get_runtime().has_numpy),
        (NeuralTier.NEURAL, "CRA-043.1", lambda: get_runtime().has_torch),
        (NeuralTier.TEXT, "CRA-043.1", lambda: get_runtime().has_transformers),
    ]
    for tier, clause, probe in tiers:
        reg.register(
            capability_id=f"tier.{tier.value}",
            provider_id="eoip-neural",
            provider_version="1.0.0",
            probe=probe,
            qualifying_clauses=[clause],
            details={"tier": tier.value},
        )
