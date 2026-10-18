"""EOIP Neural and Numerical Stack."""
from eoip.neural.runtime import NeuralTier, NeuralRuntime, get_runtime, require_tier
from eoip.neural.numerics import (
    seed_everything,
    assert_finite,
    ensure_float32,
    cosine_similarity,
    stable_softmax,
    stable_log,
    MemoryGuard,
    capture_environment,
)

from eoip.neural.antistub import (
    AntiStubHarness,
    AntiStubReport,
    HashBaseline,
    SimpleLearnedGNN,
)

__all__ = [
    "NeuralTier",
    "NeuralRuntime",
    "get_runtime",
    "require_tier",
    "seed_everything",
    "assert_finite",
    "ensure_float32",
    "cosine_similarity",
    "stable_softmax",
    "stable_log",
    "MemoryGuard",
    "capture_environment",
    "AntiStubHarness",
    "AntiStubReport",
    "HashBaseline",
    "SimpleLearnedGNN",
]

