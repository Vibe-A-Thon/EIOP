"""Deterministic Graph Algorithms with Full Path Evidence and Cost Semantics (CRA-028.5, CRA-028.7).

Replaces heuristic random-walk summaries with deterministic algorithms:
- Breadth-First Search (BFS) for reachable sets and unweighted shortest paths.
- Dijkstra algorithm for cost/weight-accumulating shortest paths with full hop evidence.
- PageRank via power iteration with damping factor.
- Tarjan's algorithm for Strongly Connected Components (SCC) and dependency cycle isolation.
- Strict path preservation: Multi-hop results retain exact intermediate nodes, edge types, and weights (CRA-028.5).
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
import heapq
from typing import Any, Optional

from eoip.graph.store import GraphStore


@dataclass
class HopEvidence:
    from_node: str
    edge_label: str
    to_node: str
    weight: float = 1.0
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass
class PathResult:
    source: str
    target: str
    hops: list[str]  # [source, intermediate_1, ..., target]
    edge_labels: list[str]
    total_cost: float
    hop_count: int
    hop_evidence: list[HopEvidence] = field(default_factory=list)


class DeterministicGraphAlgorithms:
    """Qualified deterministic algorithms over GraphStore (CRA-028.5, CRA-028.7)."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    def _build_adj_list(self) -> tuple[dict[str, list[dict[str, Any]]], dict[str, str]]:
        """Construct adjacency list mapping canonical_ids to outgoing edges."""
        edges = self._store.find_edges(limit=100_000)
        adj: dict[str, list[dict[str, Any]]] = defaultdict(list)
        node_labels: dict[str, str] = {}

        for edge in edges:
            out_cid = edge.get("out_cid")
            in_cid = edge.get("in_cid")
            if out_cid and in_cid:
                weight = float(edge.get("properties", {}).get("coupling") or edge.get("properties", {}).get("weight") or 1.0)
                adj[out_cid].append({
                    "target": in_cid,
                    "label": edge.get("label", "DEPENDS_ON"),
                    "weight": weight,
                    "eid": edge.get("eid", ""),
                    "properties": edge.get("properties", {}),
                })

        for v in self._store.find_vertices(limit=100_000):
            cid = v.get("canonical_id")
            if cid:
                node_labels[cid] = v.get("label", "Entity")

        return adj, node_labels

    def bfs_reachable(self, start_id: str, max_depth: int = 10) -> list[str]:
        """Deterministic BFS returning all reachable canonical_ids within max_depth."""
        adj, _ = self._build_adj_list()
        visited: set[str] = {start_id}
        queue: deque[tuple[str, int]] = deque([(start_id, 0)])
        result: list[str] = []

        while queue:
            node, depth = queue.popleft()
            if node != start_id:
                result.append(node)
            if depth >= max_depth:
                continue
            for edge in adj.get(node, []):
                nbr = edge["target"]
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append((nbr, depth + 1))

        return result

    def dijkstra_shortest_path(self, source_id: str, target_id: str) -> Optional[PathResult]:
        """Dijkstra shortest path with explicit cost accumulation and full hop evidence (CRA-028.5, CRA-028.7)."""
        adj, _ = self._build_adj_list()
        if source_id == target_id:
            return PathResult(source=source_id, target=target_id, hops=[source_id], edge_labels=[], total_cost=0.0, hop_count=0)

        # Min-heap: (cost, current_node, path_nodes, edge_labels, hop_evidences)
        pq: list[tuple[float, str, list[str], list[str], list[HopEvidence]]] = [(0.0, source_id, [source_id], [], [])]
        min_costs: dict[str, float] = {source_id: 0.0}

        while pq:
            cost, current, path, labels, evidences = heapq.heappop(pq)

            if current == target_id:
                return PathResult(
                    source=source_id,
                    target=target_id,
                    hops=path,
                    edge_labels=labels,
                    total_cost=cost,
                    hop_count=len(path) - 1,
                    hop_evidence=evidences,
                )

            if cost > min_costs.get(current, float("inf")):
                continue

            for edge in adj.get(current, []):
                nbr = edge["target"]
                edge_weight = edge["weight"]
                new_cost = cost + edge_weight

                if new_cost < min_costs.get(nbr, float("inf")):
                    min_costs[nbr] = new_cost
                    hop_ev = HopEvidence(
                        from_node=current,
                        edge_label=edge["label"],
                        to_node=nbr,
                        weight=edge_weight,
                        properties=edge["properties"],
                    )
                    heapq.heappush(
                        pq,
                        (new_cost, nbr, path + [nbr], labels + [edge["label"]], evidences + [hop_ev]),
                    )

        return None

    def pagerank(self, damping_factor: float = 0.85, max_iterations: int = 50, tolerance: float = 1e-6) -> dict[str, float]:
        """PageRank via deterministic power iteration (CRA-028.7)."""
        adj, node_labels = self._build_adj_list()
        all_nodes = sorted(set(node_labels.keys()) | set(adj.keys()))
        N = len(all_nodes)
        if N == 0:
            return {}

        initial_score = 1.0 / N
        scores: dict[str, float] = {node: initial_score for node in all_nodes}

        # Out-degree table
        out_degrees = {node: len(adj.get(node, [])) for node in all_nodes}

        for _ in range(max_iterations):
            new_scores: dict[str, float] = {}
            # Teleportation base
            dangling_sum = sum(scores[node] for node in all_nodes if out_degrees[node] == 0)
            teleport = (1.0 - damping_factor) / N + (damping_factor * dangling_sum / N)

            for node in all_nodes:
                new_scores[node] = teleport

            for node in all_nodes:
                deg = out_degrees[node]
                if deg > 0:
                    share = (damping_factor * scores[node]) / deg
                    for edge in adj[node]:
                        nbr = edge["target"]
                        if nbr in new_scores:
                            new_scores[nbr] += share

            # Convergence check
            diff = sum(abs(new_scores[node] - scores[node]) for node in all_nodes)
            scores = new_scores
            if diff < tolerance:
                break

        return scores

    def tarjan_scc(self) -> list[list[str]]:
        """Tarjan's algorithm for Strongly Connected Components (CRA-028.7)."""
        adj, node_labels = self._build_adj_list()
        all_nodes = sorted(set(node_labels.keys()) | set(adj.keys()))

        idx = 0
        indices: dict[str, int] = {}
        lowlinks: dict[str, int] = {}
        on_stack: set[str] = set()
        stack: list[str] = []
        sccs: list[list[str]] = []

        def strongconnect(node: str) -> None:
            nonlocal idx
            indices[node] = idx
            lowlinks[node] = idx
            idx += 1
            stack.append(node)
            on_stack.add(node)

            for edge in adj.get(node, []):
                nbr = edge["target"]
                if nbr not in indices:
                    strongconnect(nbr)
                    lowlinks[node] = min(lowlinks[node], lowlinks[nbr])
                elif nbr in on_stack:
                    lowlinks[node] = min(lowlinks[node], indices[nbr])

            # If node is a root node, pop stack and emit an SCC
            if lowlinks[node] == indices[node]:
                current_scc: list[str] = []
                while True:
                    w = stack.pop()
                    on_stack.remove(w)
                    current_scc.append(w)
                    if w == node:
                        break
                sccs.append(sorted(current_scc))

        for node in all_nodes:
            if node not in indices:
                strongconnect(node)

        return sorted(sccs, key=lambda scc: (-len(scc), scc[0] if scc else ""))
