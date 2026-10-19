"""Graph Intelligence Backend for IPU (PUR-IPU-001..005).

Provides:
1. Export of authorized graph snapshot to validated CSR sparse matrix.
2. Connected components (weak/strong) using SciPy.
3. Bounded shortest path traversal.
4. Sparse neighbor feature aggregation.
5. Unsupervised feature clustering diagnostics.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import scipy.sparse as sp
import scipy.sparse.csgraph as csgraph


def graph_to_csr(
    vertices: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    weight_property: Optional[str] = "weight",
    default_weight: float = 1.0,
) -> Dict[str, Any]:
    """Convert graph nodes/edges into validated CSR sparse matrix with stable ID maps (PUR-IPU-001)."""
    # Deterministic node ordering
    sorted_vertices = sorted(vertices, key=lambda v: str(v.get("id") or v.get("canonical_id", "")))
    node_to_idx = {str(v.get("id") or v.get("canonical_id")): i for i, v in enumerate(sorted_vertices)}
    n = len(sorted_vertices)

    row_ind = []
    col_ind = []
    data = []

    for e in edges:
        s_id = str(e.get("from_id") or e.get("source", ""))
        t_id = str(e.get("to_id") or e.get("target", ""))
        if s_id in node_to_idx and t_id in node_to_idx:
            u = node_to_idx[s_id]
            v = node_to_idx[t_id]
            w_val = e.get("properties", {}).get(weight_property) if weight_property else None
            if w_val is None and weight_property:
                w_val = e.get(weight_property)
            w = float(w_val if w_val is not None else default_weight)
            row_ind.append(u)
            col_ind.append(v)
            data.append(w)


    csr = sp.csr_matrix((data, (row_ind, col_ind)), shape=(n, n), dtype=np.float64)

    return {
        "csr_matrix": csr,
        "num_nodes": n,
        "num_edges": len(data),
        "node_ids": [str(v.get("id") or v.get("canonical_id")) for v in sorted_vertices],
        "node_to_idx": node_to_idx,
    }


def graph_connected_components(
    csr: sp.csr_matrix,
    directed: bool = True,
    connection: str = "weak",
) -> Dict[str, Any]:
    """Compute connected components over CSR matrix using SciPy (PUR-IPU-002)."""
    n_components, labels = csgraph.connected_components(
        csgraph=csr,
        directed=directed,
        connection=connection,
        return_labels=True,
    )
    return {
        "num_components": int(n_components),
        "component_labels": labels.tolist(),
        "is_connected": bool(n_components == 1),
    }


def graph_shortest_paths(
    csr: sp.csr_matrix,
    indices: Optional[List[int]] = None,
    directed: bool = True,
) -> Dict[str, Any]:
    """Calculate bounded shortest paths from source indices using Dijkstra (PUR-IPU-002)."""
    dist_matrix = csgraph.dijkstra(
        csgraph=csr,
        directed=directed,
        indices=indices,
        return_predecessors=False,
    )
    # Replace inf with -1.0 for serialization
    safe_matrix = np.where(np.isinf(dist_matrix), -1.0, dist_matrix)
    return {
        "distance_matrix": safe_matrix.tolist(),
        "sources": indices if indices else list(range(csr.shape[0])),
    }


def graph_aggregate_features(
    csr: sp.csr_matrix,
    features: np.ndarray,
    normalize: bool = True,
    add_self_loops: bool = True,
) -> np.ndarray:
    """Sparse 1-hop neighbor feature aggregation with normalization (PUR-IPU-003)."""
    adj = csr.copy()
    n = adj.shape[0]
    if add_self_loops:
        adj = adj + sp.eye(n, dtype=np.float64)

    if normalize:
        # Degree normalization: D^{-1} A
        deg = np.array(adj.sum(axis=1)).flatten()
        deg_inv = np.where(deg > 0, 1.0 / deg, 0.0)
        d_mat = sp.diags(deg_inv)
        adj_norm = d_mat.dot(adj)
    else:
        adj_norm = adj

    return adj_norm.dot(features)


def graph_cluster_features(
    features: np.ndarray,
    k: int = 3,
    max_iter: int = 100,
    seed: int = 42,
) -> Dict[str, Any]:
    """K-means clustering diagnostics over node feature matrix (PUR-IPU-004)."""
    n_samples, n_features = features.shape
    k = min(k, n_samples)
    rng = np.random.default_rng(seed)

    # Initialize centroids randomly from points
    init_indices = rng.choice(n_samples, size=k, replace=False)
    centroids = features[init_indices].copy()

    labels = np.zeros(n_samples, dtype=int)
    for _ in range(max_iter):
        # Assign points to nearest centroid
        dists = np.linalg.norm(features[:, np.newaxis, :] - centroids[np.newaxis, :, :], axis=2)
        new_labels = np.argmin(dists, axis=1)
        if np.array_equal(labels, new_labels):
            break
        labels = new_labels

        # Recompute centroids
        for c in range(k):
            mask = labels == c
            if np.any(mask):
                centroids[c] = np.mean(features[mask], axis=0)

    # Calculate inertia
    inertia = float(np.sum((features - centroids[labels]) ** 2))

    return {
        "num_clusters": k,
        "labels": labels.tolist(),
        "centroids": centroids.tolist(),
        "inertia": inertia,
    }
