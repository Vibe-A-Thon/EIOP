"""KGR-G-018: Massively Parallel Deep Multi-Hop Analytics (5+ Hops).

SciPy CSR sparse matrix-based 5+ hop traversal engine for deep graph
analytics.  Provides fraud ring detection, supply chain risk
propagation, and arbitrary depth influence analysis — as an alternative
to TigerGraph's proprietary GSQL for deep-link analytics.
"""

from __future__ import annotations

import logging
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

log = logging.getLogger("eoip.analytics.parallel_multihop")


class AnalyticsMode(str, Enum):
    BFS = "BFS"
    DFS = "DFS"
    BIDIRECTIONAL = "BIDIRECTIONAL"
    WEIGHTED = "WEIGHTED"


@dataclass
class HopResult:
    hop: int
    nodes_reached: int
    edges_traversed: int
    nodes: list[str] = field(default_factory=list)
    duration_ms: float = 0.0


@dataclass
class MultiHopResult:
    root_node: str
    total_hops: int
    total_nodes_reached: int
    total_edges_traversed: int
    per_hop: list[HopResult]
    duration_ms: float = 0.0
    paths: list[list[str]] | None = None
    scores: dict[str, float] | None = None


@dataclass
class FraudRingResult:
    ring_id: str
    nodes: list[str]
    edges: list[tuple[str, str, str]]
    risk_score: float
    ring_size: int
    max_depth: int


@dataclass
class SparseGraphMatrix:
    """CSR-format sparse adjacency matrix for high-performance traversal."""
    node_ids: list[str]
    node_index: dict[str, int]
    row_ptr: list[int]
    col_idx: list[int]
    edge_weights: list[float]

    @property
    def num_nodes(self) -> int:
        return len(self.node_ids)

    @property
    def num_edges(self) -> int:
        return len(self.col_idx)

    def neighbors(self, node_idx: int) -> list[tuple[int, float]]:
        start = self.row_ptr[node_idx]
        end = self.row_ptr[node_idx + 1]
        return [(self.col_idx[i], self.edge_weights[i]) for i in range(start, end)]


class SparseGraphBuilder:
    """Builds a CSR sparse matrix from graph store data."""

    def __init__(self) -> None:
        self._adjacency: dict[str, list[tuple[str, float]]] = defaultdict(list)
        self._nodes: set[str] = set()

    def add_edge(self, source: str, target: str, weight: float = 1.0) -> None:
        self._adjacency[source].append((target, weight))
        self._nodes.add(source)
        self._nodes.add(target)

    def build(self) -> SparseGraphMatrix:
        node_ids = sorted(self._nodes)
        node_index = {nid: idx for idx, nid in enumerate(node_ids)}

        row_ptr = [0]
        col_idx: list[int] = []
        edge_weights: list[float] = []

        for i, nid in enumerate(node_ids):
            neighbors = self._adjacency.get(nid, [])
            neighbors.sort(key=lambda x: node_index.get(x[0], 0))
            for target, weight in neighbors:
                tidx = node_index.get(target)
                if tidx is not None:
                    col_idx.append(tidx)
                    edge_weights.append(weight)
            row_ptr.append(len(col_idx))

        return SparseGraphMatrix(
            node_ids=node_ids,
            node_index=node_index,
            row_ptr=row_ptr,
            col_idx=col_idx,
            edge_weights=edge_weights,
        )

    def from_graph_store(self, store: Any, label_filter: list[str] | None = None, limit: int = 100_000) -> SparseGraphMatrix:
        """Build sparse matrix from a GraphStore by reading all edges."""
        from eoip.graph.store import GraphStore
        edges = store.find_edges(limit=limit)
        for edge in edges:
            elabel = str(edge.get("label", ""))
            if label_filter and elabel not in label_filter:
                continue
            src = str(edge.get("out_v") or edge.get("out_cid", ""))
            tgt = str(edge.get("in_v") or edge.get("in_cid", ""))
            if src and tgt:
                weight = float(edge.get("properties", {}).get("weight", 1.0)) if isinstance(edge.get("properties"), dict) else 1.0
                self.add_edge(src, tgt, weight)
        return self.build()


class SubgraphPartitioner:
    """Partitions a graph into subgraphs for parallel processing."""

    @staticmethod
    def partition_by_component(matrix: SparseGraphMatrix) -> list[list[int]]:
        """Find connected components using union-find."""
        n = matrix.num_nodes
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        for i in range(n):
            for j, _ in matrix.neighbors(i):
                union(i, j)

        components: dict[int, list[int]] = defaultdict(list)
        for i in range(n):
            components[find(i)].append(i)
        return list(components.values())

    @staticmethod
    def partition_by_degree(matrix: SparseGraphMatrix, num_partitions: int = 4) -> list[list[int]]:
        """Partition nodes by degree for load balancing."""
        degrees: list[tuple[int, int]] = []
        for i in range(matrix.num_nodes):
            deg = matrix.row_ptr[i + 1] - matrix.row_ptr[i]
            degrees.append((deg, i))
        degrees.sort(reverse=True)

        partitions: list[list[int]] = [[] for _ in range(num_partitions)]
        partition_loads = [0] * num_partitions
        for deg, node in degrees:
            min_idx = partition_loads.index(min(partition_loads))
            partitions[min_idx].append(node)
            partition_loads[min_idx] += deg

        return [p for p in partitions if p]


class ParallelMultiHopEngine:
    """Executes deep multi-hop traversals (5+ hops) using parallel processing."""

    def __init__(
        self,
        matrix: SparseGraphMatrix,
        *,
        max_workers: int = 4,
        max_hops: int = 10,
    ) -> None:
        self.matrix = matrix
        self.max_workers = max_workers
        self.max_hops = max_hops

    def multi_hop_bfs(self, root_id: str, *, hops: int = 5, max_nodes_per_hop: int = 10000) -> MultiHopResult:
        started = time.monotonic()
        root_idx = self.matrix.node_index.get(root_id)
        if root_idx is None:
            return MultiHopResult(
                root_node=root_id, total_hops=0, total_nodes_reached=0,
                total_edges_traversed=0, per_hop=[], duration_ms=0,
            )

        actual_hops = min(hops, self.max_hops)
        visited: set[int] = {root_idx}
        frontier: set[int] = {root_idx}
        per_hop: list[HopResult] = []
        total_edges = 0

        for hop in range(1, actual_hops + 1):
            hop_start = time.monotonic()
            next_frontier: set[int] = set()

            frontier_list = list(frontier)
            if len(frontier_list) > 1000 and self.max_workers > 1:
                next_frontier, hop_edges = self._parallel_expand(frontier_list, visited)
            else:
                hop_edges = 0
                for node in frontier_list:
                    for neighbor, _ in self.matrix.neighbors(node):
                        hop_edges += 1
                        if neighbor not in visited:
                            next_frontier.add(neighbor)

            if len(next_frontier) > max_nodes_per_hop:
                next_frontier = set(list(next_frontier)[:max_nodes_per_hop])

            visited.update(next_frontier)
            total_edges += hop_edges
            hop_ms = (time.monotonic() - hop_start) * 1000

            per_hop.append(HopResult(
                hop=hop,
                nodes_reached=len(next_frontier),
                edges_traversed=hop_edges,
                nodes=[self.matrix.node_ids[i] for i in list(next_frontier)[:100]],
                duration_ms=hop_ms,
            ))

            frontier = next_frontier
            if not frontier:
                break

        elapsed = (time.monotonic() - started) * 1000
        return MultiHopResult(
            root_node=root_id,
            total_hops=len(per_hop),
            total_nodes_reached=len(visited) - 1,
            total_edges_traversed=total_edges,
            per_hop=per_hop,
            duration_ms=elapsed,
        )

    def influence_propagation(
        self,
        source_ids: list[str],
        *,
        hops: int = 5,
        decay_factor: float = 0.5,
    ) -> dict[str, float]:
        """Propagate influence scores from source nodes through the graph."""
        scores: dict[int, float] = {}
        for sid in source_ids:
            idx = self.matrix.node_index.get(sid)
            if idx is not None:
                scores[idx] = 1.0

        for hop in range(hops):
            new_scores: dict[int, float] = dict(scores)
            for node_idx, score in list(scores.items()):
                propagated = score * decay_factor
                if propagated < 0.001:
                    continue
                for neighbor, weight in self.matrix.neighbors(node_idx):
                    contribution = propagated * weight
                    new_scores[neighbor] = max(new_scores.get(neighbor, 0), contribution)
            scores = new_scores

        return {
            self.matrix.node_ids[idx]: round(score, 6)
            for idx, score in scores.items()
        }

    def _parallel_expand(self, frontier: list[int], visited: set[int]) -> tuple[set[int], int]:
        chunk_size = max(1, len(frontier) // self.max_workers)
        chunks = [frontier[i:i + chunk_size] for i in range(0, len(frontier), chunk_size)]
        all_new: set[int] = set()
        total_edges = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._expand_chunk, chunk, visited): chunk
                for chunk in chunks
            }
            for future in as_completed(futures):
                new_nodes, edges = future.result()
                all_new.update(new_nodes)
                total_edges += edges

        return all_new, total_edges

    def _expand_chunk(self, chunk: list[int], visited: set[int]) -> tuple[set[int], int]:
        new_nodes: set[int] = set()
        edges = 0
        for node in chunk:
            for neighbor, _ in self.matrix.neighbors(node):
                edges += 1
                if neighbor not in visited:
                    new_nodes.add(neighbor)
        return new_nodes, edges


class FraudRingDetector:
    """Detects cyclic fraud rings using deep multi-hop traversal."""

    def __init__(self, engine: ParallelMultiHopEngine) -> None:
        self.engine = engine

    def detect_rings(
        self,
        *,
        min_ring_size: int = 3,
        max_ring_size: int = 20,
        max_depth: int = 6,
        suspicious_labels: list[str] | None = None,
    ) -> list[FraudRingResult]:
        matrix = self.engine.matrix
        partitioner = SubgraphPartitioner()
        components = partitioner.partition_by_component(matrix)

        rings: list[FraudRingResult] = []
        ring_counter = 0

        for component in components:
            if len(component) < min_ring_size or len(component) > max_ring_size:
                continue

            cycles = self._find_cycles(matrix, component, max_depth)
            for cycle in cycles:
                if len(cycle) < min_ring_size:
                    continue
                ring_counter += 1
                node_names = [matrix.node_ids[i] for i in cycle]
                edges: list[tuple[str, str, str]] = []
                for k in range(len(cycle)):
                    src = matrix.node_ids[cycle[k]]
                    tgt = matrix.node_ids[cycle[(k + 1) % len(cycle)]]
                    edges.append((src, "TRANSACTS_WITH", tgt))

                risk = min(1.0, len(cycle) / 10.0 * 0.5 + 0.3)
                rings.append(FraudRingResult(
                    ring_id=f"ring_{ring_counter}",
                    nodes=node_names,
                    edges=edges,
                    risk_score=round(risk, 3),
                    ring_size=len(cycle),
                    max_depth=max_depth,
                ))

        return rings

    @staticmethod
    def _find_cycles(matrix: SparseGraphMatrix, component: list[int], max_depth: int) -> list[list[int]]:
        cycles: list[list[int]] = []
        comp_set = set(component)

        for start in component[:10]:
            visited: set[int] = set()
            path: list[int] = []

            def dfs(node: int, depth: int) -> None:
                if depth > max_depth:
                    return
                path.append(node)
                visited.add(node)
                for neighbor, _ in matrix.neighbors(node):
                    if neighbor not in comp_set:
                        continue
                    if neighbor == start and len(path) >= 3:
                        cycles.append(list(path))
                    elif neighbor not in visited:
                        dfs(neighbor, depth + 1)
                path.pop()
                visited.discard(node)

            dfs(start, 0)

        return cycles
