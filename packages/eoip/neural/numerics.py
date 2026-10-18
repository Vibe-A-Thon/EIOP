"""Numerical substrate and determinism utilities (CRA-043.5 - 043.9)."""
from __future__ import annotations
import math, os, platform, random
import importlib
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from typing import Any, Optional

# CRA-043.7 BLAS Thread governance (must be set before any BLAS/numpy import)
def configure_blas_threads(n_threads: int = 1) -> None:
    s = str(max(1, n_threads))
    for var in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
    ):
        os.environ[var] = s

configure_blas_threads(1)
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

if HAS_NUMPY:
    from numpy.typing import NDArray

    Vector = NDArray[np.float32]
    Matrix = NDArray[np.float32]
else:
    Vector = Any
    Matrix = Any

torch: Any = None
try:
    torch = importlib.import_module("torch")
    HAS_TORCH = True
except ImportError:
    torch = None
    HAS_TORCH = False


@dataclass(frozen=True)
class SeedBundle:
    python_seed: int
    numpy_seed: int | None
    torch_seed: int | None
    cuda_seed: int | None
    deterministic: bool


_LAST_SEED_BUNDLE: SeedBundle | None = None


def seed_everything(seed: int = 42, deterministic: bool = True) -> SeedBundle:
    """Deterministic seed control across Python, NumPy, and PyTorch (CRA-043.6)."""
    global _LAST_SEED_BUNDLE
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    numpy_seed: int | None = None
    torch_seed: int | None = None
    cuda_seed: int | None = None
    if HAS_NUMPY:
        numpy_seed = seed % (2**32)
        np.random.seed(numpy_seed)
    if HAS_TORCH:
        if deterministic:
            os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
        torch.manual_seed(seed)
        torch_seed = seed
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
            cuda_seed = seed
        if deterministic:
            torch.use_deterministic_algorithms(True)
    _LAST_SEED_BUNDLE = SeedBundle(seed, numpy_seed, torch_seed, cuda_seed, deterministic)
    return _LAST_SEED_BUNDLE


def capture_environment() -> dict[str, Any]:
    """Capture runtime and hardware environment for receipt reproducibility (CRA-043.6)."""
    info: dict[str, Any] = {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "threads": {
            var: os.environ.get(var)
            for var in (
                "OMP_NUM_THREADS",
                "OPENBLAS_NUM_THREADS",
                "MKL_NUM_THREADS",
                "NUMEXPR_NUM_THREADS",
                "VECLIB_MAXIMUM_THREADS",
            )
        },
        "has_numpy": HAS_NUMPY,
        "has_torch": HAS_TORCH,
        "seeds": asdict(_LAST_SEED_BUNDLE) if _LAST_SEED_BUNDLE is not None else None,
    }
    if HAS_NUMPY:
        info["numpy_version"] = np.__version__
    for module_name, version_key in (("scipy", "scipy_version"), ("sklearn", "scikit_learn_version")):
        try:
            info[version_key] = importlib.import_module(module_name).__version__
        except ImportError:
            info[version_key] = None
    try:
        from threadpoolctl import threadpool_info

        info["blas"] = [
            {key: pool.get(key) for key in ("internal_api", "version", "num_threads", "threading_layer")}
            for pool in threadpool_info()
        ]
    except ImportError:
        info["blas"] = None
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


def to_array(values: Sequence[float]) -> Any:
    """Convert a numeric sequence to a finite float32 vector."""
    if HAS_NUMPY:
        result = np.asarray(values, dtype=np.float32)
        if result.ndim != 1:
            raise ValueError("to_array expects a one-dimensional sequence")
        assert_finite(result)
        return result
    result = [float(value) for value in values]
    assert_finite(result)
    return result


def to_list(values: Any) -> list[float]:
    """Convert a finite vector to JSON-compatible Python floats."""
    assert_finite(values)
    if HAS_NUMPY and isinstance(values, np.ndarray):
        if values.ndim != 1:
            raise ValueError("to_list expects a one-dimensional vector")
        return [float(value) for value in values.tolist()]
    return [float(value) for value in values]


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


def cosine_matrix(query: Any, matrix: Any, eps: float = 1e-12) -> Any:
    """Return cosine similarities between one vector and each matrix row."""
    if HAS_NUMPY:
        vector = np.asarray(query, dtype=np.float32)
        rows = np.asarray(matrix, dtype=np.float32)
        if vector.ndim != 1 or rows.ndim != 2 or rows.shape[1] != vector.shape[0]:
            raise ValueError("cosine_matrix expects a vector and a matrix with matching feature width")
        assert_finite(vector)
        assert_finite(rows)
        if rows.shape[0] == 0:
            return np.empty((0,), dtype=np.float32)
        vector_norm = float(np.linalg.norm(vector))
        row_norms = np.sqrt(np.einsum("ij,ij->i", rows, rows, optimize=False))
        denominators = np.maximum(row_norms * vector_norm, eps)
        similarities = np.einsum("ij,j->i", rows, vector, optimize=False) / denominators
        similarities[(row_norms < eps) | (vector_norm < eps)] = 0.0
        return np.clip(similarities, -1.0, 1.0).astype(np.float32, copy=False)

    rows = list(matrix)
    return [cosine_similarity(query, row, eps=eps) for row in rows]


def l2_normalize(values: Any, axis: int = -1, eps: float = 1e-12) -> Any:
    """Normalize vectors along an axis; zero vectors remain zero and empty arrays remain empty."""
    if HAS_NUMPY:
        array = np.asarray(values, dtype=np.float32)
        assert_finite(array)
        if array.size == 0:
            return array.copy()
        norms = np.linalg.norm(array, axis=axis, keepdims=True)
        return array / np.maximum(norms, eps)

    if not isinstance(values, (list, tuple)):
        raise TypeError("l2_normalize requires an array or a numeric sequence")
    if not values:
        return []
    if isinstance(values[0], (list, tuple)):
        if axis not in (-1, 1):
            raise ValueError("Pure-Python matrix normalization supports only the last axis")
        return [l2_normalize(row, eps=eps) for row in values]
    assert_finite(values)
    norm = math.sqrt(sum(float(value) ** 2 for value in values))
    if norm < eps:
        return [0.0 for _ in values]
    return [float(value) / norm for value in values]


def stable_softmax(logits: Any, axis: int = -1) -> Any:
    """Numerically stable softmax subtracting max to prevent exp overflow."""
    if HAS_NUMPY:
        arr = np.asarray(logits, dtype=np.float32)
        assert_finite(arr)
        if arr.size == 0:
            return np.zeros_like(arr)
        shifted = arr - np.max(arr, axis=axis, keepdims=True)
        exp_vals = np.exp(shifted)
        sum_exp = np.sum(exp_vals, axis=axis, keepdims=True)
        return exp_vals / np.maximum(sum_exp, 1e-12)
    else:
        assert_finite(logits)
        if not logits:
            return []
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
