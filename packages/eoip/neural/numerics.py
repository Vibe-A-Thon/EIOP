"""Numerical substrate and determinism utilities (CRA-043.5 - 043.9)."""
from __future__ import annotations
import math, os, platform, random
from typing import Any, Optional

# CRA-043.7 BLAS Thread governance (must be set before any BLAS/numpy import)
def configure_blas_threads(n_threads: int = 1) -> None:
    s = str(max(1, n_threads))
    for var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        os.environ[var] = s

configure_blas_threads(1)

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


def seed_everything(seed: int = 42) -> None:
    """Deterministic seed control across Python, NumPy, and PyTorch (CRA-043.6)."""
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    if HAS_NUMPY:
        np.random.seed(seed)
    if HAS_TORCH:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)


def capture_environment() -> dict[str, Any]:
    """Capture runtime and hardware environment for receipt reproducibility (CRA-043.6)."""
    info: dict[str, Any] = {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "threads": {
            var: os.environ.get(var)
            for var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")
        },
        "has_numpy": HAS_NUMPY,
        "has_torch": HAS_TORCH,
    }
    if HAS_NUMPY:
        info["numpy_version"] = np.__version__
    if HAS_TORCH:
        info["torch_version"] = torch.__version__
        info["cuda_available"] = torch.cuda.is_available()
    return info


def assert_finite(arr: Any) -> None:
    """Verify all entries are finite (not NaN or Inf). Raises ValueError on violation."""
    if HAS_NUMPY and isinstance(arr, np.ndarray):
        if not np.all(np.isfinite(arr)):
            raise ValueError("CRA-043.8 violation: array contains non-finite values (NaN or Inf)")
    elif HAS_TORCH and isinstance(arr, torch.Tensor):
        if not torch.all(torch.isfinite(arr)):
            raise ValueError("CRA-043.8 violation: tensor contains non-finite values (NaN or Inf)")
    elif isinstance(arr, (list, tuple)):
        for x in arr:
            if math.isnan(x) or math.isinf(x):
                raise ValueError("CRA-043.8 violation: sequence contains non-finite values (NaN or Inf)")


def ensure_float32(arr: Any) -> Any:
    """Ensure array is stored with float32 precision policy (CRA-043.5)."""
    if HAS_NUMPY and isinstance(arr, np.ndarray):
        if arr.dtype != np.float32:
            return arr.astype(np.float32)
        return arr
    if HAS_TORCH and isinstance(arr, torch.Tensor):
        if arr.dtype != torch.float32:
            return arr.to(torch.float32)
        return arr
    if HAS_NUMPY:
        return np.array(arr, dtype=np.float32)
    return [float(x) for x in arr]


def cosine_similarity(a: Any, b: Any, eps: float = 1e-12) -> float:
    """Numerically stable vectorized cosine similarity handling zero-vectors safely."""
    if HAS_NUMPY:
        va = np.asarray(a, dtype=np.float32)
        vb = np.asarray(b, dtype=np.float32)
        assert_finite(va)
        assert_finite(vb)
        norm_a = float(np.linalg.norm(va))
        norm_b = float(np.linalg.norm(vb))
        if norm_a < eps or norm_b < eps:
            return 0.0
        dot = float(np.dot(va, vb))
        sim = dot / (norm_a * norm_b)
        return max(-1.0, min(1.0, sim))
    else:
        # Pure Python fallback
        assert_finite(a)
        assert_finite(b)
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        if na < eps or nb < eps:
            return 0.0
        return max(-1.0, min(1.0, dot / (na * nb)))


def stable_softmax(logits: Any, axis: int = -1) -> Any:
    """Numerically stable softmax subtracting max to prevent exp overflow."""
    if HAS_NUMPY:
        arr = np.asarray(logits, dtype=np.float32)
        assert_finite(arr)
        shifted = arr - np.max(arr, axis=axis, keepdims=True)
        exp_vals = np.exp(shifted)
        sum_exp = np.sum(exp_vals, axis=axis, keepdims=True)
        return exp_vals / np.maximum(sum_exp, 1e-12)
    else:
        assert_finite(logits)
        m = max(logits)
        exp_vals = [math.exp(x - m) for x in logits]
        s = sum(exp_vals)
        return [e / max(s, 1e-12) for e in exp_vals]


def stable_log(probs: Any, eps: float = 1e-12) -> Any:
    """Numerically stable logarithm clamping inputs to [eps, 1.0]."""
    if HAS_NUMPY:
        arr = np.asarray(probs, dtype=np.float32)
        assert_finite(arr)
        clamped = np.clip(arr, eps, 1.0)
        return np.log(clamped)
    else:
        assert_finite(probs)
        return [math.log(max(eps, min(1.0, float(p)))) for p in probs]


class MemoryGuard:
    """Estimates memory before tensor allocation, refusing at 80% budget (CRA-043.9)."""
    def __init__(self, max_bytes: int = 2 * 1024 * 1024 * 1024):  # 2 GiB default
        self.max_bytes = max_bytes

    def check_allocation(self, shape: tuple[int, ...], itemsize: int = 4) -> None:
        total_elements = 1
        for dim in shape:
            total_elements *= dim
        needed_bytes = total_elements * itemsize
        threshold = int(self.max_bytes * 0.80)
        if needed_bytes > threshold:
            raise MemoryError(
                f"MemoryGuard refusal: requested allocation of {needed_bytes} bytes "
                f"exceeds 80% safety budget ({threshold} bytes)"
            )
