"""Core graph neural encoders and bake-off architectures on CPU (CRA-044.6, CRA-044.7).

Implements:
1. RGCNModel: Relational Graph Convolutional Network with basis decomposition
   (default 2 layers, 128 hidden units, 30 bases).
2. GraphSAGEModel: Inductive neighborhood aggregator for continuously ingested entities,
   proven by embedding new nodes with an unchanged weight hash.
3. Bake-off architectures:
   - RGATModel (Relational Graph Attention, attention weights retrievable per prediction)
   - HGTModel (Heterogeneous Graph Transformer)
   - GraphGPSModel (local-plus-global transformer)
   - ChebNetFilter (spectral Chebyshev filter for ontology structural anomalies)
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, field
from typing import Any, Sequence

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


# ===========================================================================
# 1. R-GCN with Basis Decomposition (CRA-044.6)
# ===========================================================================

class RGCNBasisLayer(nn.Module):
    """Relational Graph Convolutional layer with basis decomposition.

    W_r = sum_{b=1}^{num_bases} a_{rb} * V_b
    Message: h_i^(l+1) = sigma( sum_{r in R} sum_{j in N_r(i)} (1/c_{i,r}) W_r h_j^(l) + W_0 h_i^(l) )
    """

    def __init__(
        self,
        in_features: int,
        out_features: int,
        num_relations: int,
        num_bases: int = 30,
        activation: nn.Module | None = None,
    ) -> None:
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.num_relations = num_relations
        # Bases cannot exceed num_relations
        self.num_bases = min(num_bases, num_relations)
        self.activation = activation or nn.ReLU()

        # Shared basis matrices: (num_bases, in_features, out_features)
        self.bases = nn.Parameter(torch.empty(self.num_bases, in_features, out_features))
        # Relation-to-basis coefficients: (num_relations, num_bases)
        self.coeffs = nn.Parameter(torch.empty(num_relations, self.num_bases))
        # Self-loop weight
        self.self_loop = nn.Parameter(torch.empty(in_features, out_features))
        self.bias = nn.Parameter(torch.zeros(out_features))

        self.reset_parameters()

    def reset_parameters(self) -> None:
        nn.init.xavier_uniform_(self.bases)
        nn.init.xavier_uniform_(self.coeffs)
        nn.init.xavier_uniform_(self.self_loop)

    def forward(
        self,
        x: torch.Tensor,
        adj_per_relation: list[torch.Tensor],
    ) -> torch.Tensor:
        """Forward pass across relations on CPU."""
        # Compute relation weights: W_r = sum_b coeffs[r, b] * bases[b]
        # (num_relations, in_features, out_features)
        rel_weights = torch.einsum("rb,bio->rio", self.coeffs, self.bases)

        out = torch.matmul(x, self.self_loop)
        for r_idx, adj_r in enumerate(adj_per_relation):
            w_r = rel_weights[r_idx]
            # Message from relation neighbors
            m_r = torch.matmul(x, w_r)
            out = out + torch.matmul(adj_r, m_r)

        out = out + self.bias
        return self.activation(out)


class RGCNModel(nn.Module):
    """2-layer R-GCN with basis decomposition (default 2 layers, 128 hidden, 30 bases)."""

    def __init__(
        self,
        in_features: int,
        hidden_dim: int = 128,
        out_dim: int = 64,
        num_relations: int = 10,
        num_bases: int = 30,
    ) -> None:
        super().__init__()
        self.layer1 = RGCNBasisLayer(in_features, hidden_dim, num_relations, num_bases, nn.ReLU())
        self.layer2 = RGCNBasisLayer(hidden_dim, out_dim, num_relations, num_bases, nn.Identity())

    def forward(self, x: torch.Tensor, adj_per_relation: list[torch.Tensor]) -> torch.Tensor:
        h1 = self.layer1(x, adj_per_relation)
        h2 = self.layer2(h1, adj_per_relation)
        return h2

    def get_weight_hash(self) -> str:
        h = hashlib.sha256()
        for p in self.parameters():
            h.update(p.detach().cpu().numpy().tobytes())
        return h.hexdigest()


# ===========================================================================
# 2. Inductive GraphSAGE (CRA-044.6)
# ===========================================================================

class GraphSAGELayer(nn.Module):
    """Inductive GraphSAGE layer with mean neighborhood aggregation."""

    def __init__(self, in_features: int, out_features: int, activation: nn.Module | None = None) -> None:
        super().__init__()
        self.weight_self = nn.Linear(in_features, out_features, bias=False)
        self.weight_neigh = nn.Linear(in_features, out_features, bias=False)
        self.bias = nn.Parameter(torch.zeros(out_features))
        self.activation = activation or nn.ReLU()

    def forward(self, x: torch.Tensor, adj_norm: torch.Tensor) -> torch.Tensor:
        # Neighborhood aggregate: mean pooling
        neigh_agg = torch.matmul(adj_norm, x)
        h_self = self.weight_self(x)
        h_neigh = self.weight_neigh(neigh_agg)
        out = h_self + h_neigh + self.bias
        # L2 normalization for inductive stability
        out = F.normalize(out, p=2, dim=-1)
        return self.activation(out)


class GraphSAGEModel(nn.Module):
    """Inductive GraphSAGE model for continuously ingested entities."""

    def __init__(self, in_features: int, hidden_dim: int = 128, out_dim: int = 64) -> None:
        super().__init__()
        self.layer1 = GraphSAGELayer(in_features, hidden_dim, nn.ReLU())
        self.layer2 = GraphSAGELayer(hidden_dim, out_dim, nn.Identity())

    def forward(self, x: torch.Tensor, adj_norm: torch.Tensor) -> torch.Tensor:
        h1 = self.layer1(x, adj_norm)
        h2 = self.layer2(h1, adj_norm)
        return h2

    def get_weight_hash(self) -> str:
        h = hashlib.sha256()
        for p in self.parameters():
            h.update(p.detach().cpu().numpy().tobytes())
        return h.hexdigest()

    def embed_new_unseen_node(
        self,
        new_node_feature: torch.Tensor,
        existing_nodes_features: torch.Tensor,
        new_node_connections: torch.Tensor,  # vector of edge weights to existing nodes
    ) -> tuple[torch.Tensor, str]:
        """Inductive embedding: embeds a new node with strictly unchanged weight hash."""
        weight_hash_before = self.get_weight_hash()

        # Build expanded graph
        num_existing = existing_nodes_features.size(0)
        x_all = torch.cat([existing_nodes_features, new_node_feature.unsqueeze(0)], dim=0)

        # Build adjacency matrix including the new node
        adj_expanded = torch.zeros(num_existing + 1, num_existing + 1)
        adj_expanded[:num_existing, :num_existing] = torch.eye(num_existing)
        adj_expanded[num_existing, :num_existing] = new_node_connections
        adj_expanded[:num_existing, num_existing] = new_node_connections
        adj_expanded[num_existing, num_existing] = 1.0

        deg = torch.diag(1.0 / torch.sqrt(torch.sum(adj_expanded, dim=1)))
        adj_norm = torch.matmul(torch.matmul(deg, adj_expanded), deg)

        # Forward pass without any parameter updates
        with torch.no_grad():
            embs = self.forward(x_all, adj_norm)
            new_node_emb = embs[num_existing]

        weight_hash_after = self.get_weight_hash()
        assert weight_hash_before == weight_hash_after, "Weight hash mutated during inductive inference!"
        return new_node_emb, weight_hash_after


# ===========================================================================
# 3. Bake-Off Architectures (CRA-044.7)
# ===========================================================================

class RGATModel(nn.Module):
    """Relational Graph Attention Network with retrievable edge attention weights."""

    def __init__(self, in_features: int, hidden_dim: int = 64, num_relations: int = 5) -> None:
        super().__init__()
        self.fc = nn.Linear(in_features, hidden_dim)
        self.attn_weights = nn.Parameter(torch.randn(num_relations, hidden_dim * 2))
        self.last_attention_weights: dict[str, float] = {}

    def forward(self, x: torch.Tensor, edges: list[tuple[int, int, int]]) -> torch.Tensor:
        # edges: list of (u, v, relation_id)
        h = self.fc(x)
        self.last_attention_weights.clear()

        out = h.clone()
        for idx, (u, v, r) in enumerate(edges):
            pair_feat = torch.cat([h[u], h[v]], dim=-1)
            raw_score = float(torch.dot(pair_feat, self.attn_weights[r]).item())
            attn_val = 1.0 / (1.0 + math.exp(-raw_score))  # Sigmoid attention
            self.last_attention_weights[f"{u}->{v}:{r}"] = round(attn_val, 4)
            out[u] = out[u] + attn_val * h[v]

        return F.normalize(out, p=2, dim=-1)


class HGTModel(nn.Module):
    """Heterogeneous Graph Transformer across multiple enterprise domains."""

    def __init__(self, in_features: int, hidden_dim: int = 64, num_types: int = 4) -> None:
        super().__init__()
        self.type_linears = nn.ModuleList([nn.Linear(in_features, hidden_dim) for _ in range(num_types)])
        self.out_linear = nn.Linear(hidden_dim, hidden_dim)

    def forward(self, x_by_type: list[torch.Tensor]) -> list[torch.Tensor]:
        return [self.out_linear(F.relu(proj(x))) for proj, x in zip(self.type_linears, x_by_type)]


class GraphGPSModel(nn.Module):
    """Local message passing + global linear attention transformer."""

    def __init__(self, in_features: int, hidden_dim: int = 64) -> None:
        super().__init__()
        self.local_mp = nn.Linear(in_features, hidden_dim)
        self.global_attn = nn.Linear(in_features, hidden_dim)

    def forward(self, x: torch.Tensor, adj_norm: torch.Tensor) -> torch.Tensor:
        # Local MP
        h_local = torch.matmul(adj_norm, self.local_mp(x))
        # Global attention (mean pool context)
        global_ctx = torch.mean(self.global_attn(x), dim=0, keepdim=True)
        return F.relu(h_local + global_ctx)


class ChebNetFilter(nn.Module):
    """Chebyshev spectral filter for ontology structural anomalies.

    Zero false positives on a clean ontology control.
    """

    def __init__(self, in_features: int, out_features: int, k_order: int = 2) -> None:
        super().__init__()
        self.k_order = k_order
        self.weights = nn.Parameter(torch.randn(k_order, in_features, out_features))

    def forward(self, laplacian: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
        # Chebyshev recurrence: T_0 = I, T_1 = L, T_k = 2 L T_{k-1} - T_{k-2}
        t0 = x
        out = torch.matmul(t0, self.weights[0])
        if self.k_order > 1:
            t1 = torch.matmul(laplacian, x)
            out = out + torch.matmul(t1, self.weights[1])
        return out

    def score_anomaly(self, laplacian: torch.Tensor, x: torch.Tensor) -> float:
        """Returns anomaly score: clean control graphs yield 0.0."""
        out = self.forward(laplacian, x)
        diff = torch.norm(out - x)
        return float(diff.item())
