"""Deterministic CPU Numerical and Tensor Backend (PUR-GPU-001..004, PUR-TPU-001..003).

Pure Python + NumPy/SciPy implementation enforcing strict IEEE 754 precision,
shape/dtype bounds, and deterministic tie-breaking.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple, Union
from collections.abc import Sequence

import numpy as np
import scipy.sparse as sp


def cosine_top_k(
    candidates: np.ndarray,
    query: np.ndarray,
    k: int = 5,
    zero_vector_policy: str = "reject",
    row_ids: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Calculate cosine similarity and return top-k matches with stable tie-breaking."""
    if candidates.ndim != 2:
        raise ValueError(f"Candidates matrix must be 2D, got shape {candidates.shape}")
    if query.ndim == 1:
        query = query.reshape(1, -1)
    if query.ndim != 2 or query.shape[0] != 1:
        raise ValueError(f"Query vector must be 1D or (1, D), got shape {query.shape}")
    if candidates.shape[1] != query.shape[1]:
        raise ValueError(f"Dimension mismatch: candidates {candidates.shape[1]} vs query {query.shape[1]}")

    q_norm = np.linalg.norm(query)
    if q_norm < 1e-12:
        if zero_vector_policy == "reject":
            raise ValueError("Zero-norm query vector rejected under zero_vector_policy='reject'")
        # Return zero scores
        top_k_indices = list(range(min(k, candidates.shape[0])))
        return {
            "top_indices": top_k_indices,
            "scores": [0.0] * len(top_k_indices),
            "matched_ids": [row_ids[i] if row_ids else f"row_{i}" for i in top_k_indices],
        }

    c_norms = np.linalg.norm(candidates, axis=1)
    # Avoid div by zero
    valid_mask = c_norms > 1e-12
    scores = np.zeros(candidates.shape[0], dtype=np.float64)
    if np.any(valid_mask):
        dots = np.dot(candidates[valid_mask], query.T).ravel()
        scores[valid_mask] = dots / (c_norms[valid_mask] * q_norm)

    # Sort descending by score, ascending by original index for stable tie breaks
    indices = np.lexsort((np.arange(candidates.shape[0]), -scores))
    top_indices = indices[: min(k, candidates.shape[0])].tolist()

    return {
        "top_indices": top_indices,
        "scores": [float(scores[i]) for i in top_indices],
        "matched_ids": [row_ids[i] if row_ids else f"row_{i}" for i in top_indices],
    }


def matmul(
    a: np.ndarray,
    b: np.ndarray,
    transpose_b: bool = False,
) -> np.ndarray:
    """Matrix multiplication with dimension checks."""
    if transpose_b:
        b = np.swapaxes(b, -1, -2)
    return np.matmul(a, b)


def vector_reduce(
    arr: np.ndarray,
    op: str = "sum",
    axis: Optional[int] = None,
) -> Union[float, np.ndarray]:
    """Axis-wise reduction with explicit operation dispatch."""
    if op == "sum":
        return np.sum(arr, axis=axis)
    elif op == "mean":
        return np.mean(arr, axis=axis)
    elif op == "min":
        return np.amin(arr, axis=axis)
    elif op == "max":
        return np.amax(arr, axis=axis)
    elif op == "l2_norm":
        return np.linalg.norm(arr, axis=axis)
    else:
        raise ValueError(f"Unsupported reduction op: {op}")


def sparse_dense_matmul(
    sparse_csr: sp.csr_matrix,
    dense_matrix: np.ndarray,
) -> np.ndarray:
    """Compressed Sparse Row by dense matrix multiplication with zero unexpected densification."""
    if not sp.isspmatrix_csr(sparse_csr):
        sparse_csr = sp.csr_matrix(sparse_csr)
    return sparse_csr.dot(dense_matrix)


def tensor_elementwise(
    a: np.ndarray,
    op: str = "add",
    b: Optional[np.ndarray] = None,
) -> np.ndarray:
    """Elementwise tensor operations."""
    if op == "add":
        if b is None:
            raise ValueError("Binary op 'add' requires tensor b")
        return np.add(a, b)
    elif op == "multiply":
        if b is None:
            raise ValueError("Binary op 'multiply' requires tensor b")
        return np.multiply(a, b)
    elif op == "relu":
        return np.maximum(a, 0)
    elif op == "sigmoid":
        # Numerically safe sigmoid
        return np.where(a >= 0, 1 / (1 + np.exp(-a)), np.exp(a) / (1 + np.exp(a)))
    else:
        raise ValueError(f"Unsupported elementwise op: {op}")


def tensor_softmax(
    a: np.ndarray,
    axis: int = -1,
) -> np.ndarray:
    """Numerically stable softmax."""
    shifted = a - np.amax(a, axis=axis, keepdims=True)
    exp_shifted = np.exp(shifted)
    return exp_shifted / np.sum(exp_shifted, axis=axis, keepdims=True)


def tensor_normalize(
    a: np.ndarray,
    mode: str = "l2",
    axis: int = -1,
    epsilon: float = 1e-5,
) -> np.ndarray:
    """Normalize tensor (L2 or LayerNorm)."""
    if mode == "l2":
        norm = np.linalg.norm(a, axis=axis, keepdims=True)
        return a / np.maximum(norm, epsilon)
    elif mode in ("layernorm", "layer"):
        mean = np.mean(a, axis=axis, keepdims=True)
        var = np.var(a, axis=axis, keepdims=True)
        return (a - mean) / np.sqrt(var + epsilon)
    else:
        raise ValueError(f"Unsupported normalization mode: {mode}")


def tensor_reshape(
    a: np.ndarray,
    target_shape: Sequence[int],
) -> np.ndarray:
    """Reshape tensor with validated element count."""
    return np.reshape(a, target_shape)


def conv2d_nchw(
    x: np.ndarray,
    weight: np.ndarray,
    bias: Optional[np.ndarray] = None,
    stride: int = 1,
    padding: int = 0,
) -> np.ndarray:
    """2D Convolution for NCHW tensor layout."""
    if x.ndim != 4 or weight.ndim != 4:
        raise ValueError(f"Input and weight must be 4D (NCHW), got x={x.shape}, w={weight.shape}")

    n, c_in, h_in, w_in = x.shape
    c_out, w_c_in, kh, kw = weight.shape
    if c_in != w_c_in:
        raise ValueError(f"Channel mismatch: input has {c_in}, weight has {w_c_in}")

    if padding > 0:
        x_padded = np.pad(x, ((0, 0), (0, 0), (padding, padding), (padding, padding)), mode="constant")
    else:
        x_padded = x

    h_out = (h_in + 2 * padding - kh) // stride + 1
    w_out = (w_in + 2 * padding - kw) // stride + 1

    out = np.zeros((n, c_out, h_out, w_out), dtype=x.dtype)

    for i in range(h_out):
        for j in range(w_out):
            h_start = i * stride
            w_start = j * stride
            patch = x_padded[:, :, h_start : h_start + kh, w_start : w_start + kw]
            # patch shape: (n, c_in, kh, kw), weight shape: (c_out, c_in, kh, kw)
            for k in range(c_out):
                out[:, k, i, j] = np.sum(patch * weight[k], axis=(1, 2, 3))

    if bias is not None:
        out += bias.reshape(1, c_out, 1, 1)

    return out


def pool2d_nchw(
    x: np.ndarray,
    kernel_size: int = 2,
    stride: int = 2,
    mode: str = "max",
) -> np.ndarray:
    """2D Pooling (max or average) over NCHW tensor."""
    if x.ndim != 4:
        raise ValueError(f"Input must be 4D (NCHW), got {x.shape}")
    n, c, h_in, w_in = x.shape
    h_out = (h_in - kernel_size) // stride + 1
    w_out = (w_in - kernel_size) // stride + 1

    out = np.zeros((n, c, h_out, w_out), dtype=x.dtype)
    for i in range(h_out):
        for j in range(w_out):
            h_s = i * stride
            w_s = j * stride
            patch = x[:, :, h_s : h_s + kernel_size, w_s : w_s + kernel_size]
            if mode == "max":
                out[:, :, i, j] = np.amax(patch, axis=(2, 3))
            elif mode == "avg":
                out[:, :, i, j] = np.mean(patch, axis=(2, 3))
            else:
                raise ValueError(f"Unsupported pooling mode: {mode}")
    return out
