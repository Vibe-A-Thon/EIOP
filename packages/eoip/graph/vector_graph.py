"""KGR-G-016: Co-Located HNSW VectorGraph Adapter.

Co-locates an HNSW vector index within the graph engine for combined
vector similarity + multi-hop graph traversal queries.  Target: < 5ms
for combined vector + 2-hop queries.
"""

from __future__ import annotations

import hashlib
import heapq
import logging
import math
import random
import threading
import time
from dataclasses import dataclass, field
from typing import Any

from eoip.graph.store import GraphStore, Vertex

log = logging.getLogger("eoip.graph.vector_graph")


@dataclass(frozen=True)
class VectorEntry:
    canonical_id: str
    vector: tuple[float, ...]
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def dimension(self) -> int:
        return len(self.vector)


@dataclass
class VectorSearchResult:
    canonical_id: str
    score: float
    vector: tuple[float, ...]
    metadata: dict[str, Any] = field(default_factory=dict)
    graph_context: dict[str, Any] | None = None


@dataclass
class HNSWConfig:
    max_connections: int = 16  # M parameter
    ef_construction: int = 200
    ef_search: int = 50
    max_elements: int = 1_000_000
    distance_metric: str = "cosine"  # cosine, euclidean, dot_product


def _cosine_distance(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 1.0
    return 1.0 - (dot / (norm_a * norm_b))


def _euclidean_distance(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def _dot_product_distance(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return -sum(x * y for x, y in zip(a, b))


DISTANCE_FUNCTIONS = {
    "cosine": _cosine_distance,
    "euclidean": _euclidean_distance,
    "dot_product": _dot_product_distance,
}


class HNSWIndex:
    """Hierarchical Navigable Small World graph index for approximate nearest neighbor search."""

    def __init__(self, config: HNSWConfig | None = None) -> None:
        self.config = config or HNSWConfig()
        self._entries: dict[str, VectorEntry] = {}
        self._graph: dict[int, dict[str, list[str]]] = {}  # level -> {node_id -> [neighbors]}
        self._entry_point: str | None = None
        self._max_level: int = 0
        self._node_levels: dict[str, int] = {}
        self._lock = threading.Lock()
        self._dist_fn = DISTANCE_FUNCTIONS[self.config.distance_metric]

    def _random_level(self) -> int:
        ml = 1.0 / math.log(self.config.max_connections)
        level = int(-math.log(random.random()) * ml)
        return min(level, 16)

    def insert(self, entry: VectorEntry) -> None:
        with self._lock:
            self._entries[entry.canonical_id] = entry
            node_level = self._random_level()
            self._node_levels[entry.canonical_id] = node_level

            if self._entry_point is None:
                self._entry_point = entry.canonical_id
                self._max_level = node_level
                for level in range(node_level + 1):
                    self._graph.setdefault(level, {})[entry.canonical_id] = []
                return

            current = self._entry_point
            for level in range(self._max_level, node_level, -1):
                current = self._greedy_search_layer(entry.vector, current, level)

            for level in range(min(node_level, self._max_level), -1, -1):
                self._graph.setdefault(level, {}).setdefault(entry.canonical_id, [])
                neighbors = self._search_layer(entry.vector, current, self.config.ef_construction, level)
                selected = self._select_neighbors(entry.vector, neighbors, self.config.max_connections)

                self._graph[level][entry.canonical_id] = selected
                for neighbor_id in selected:
                    self._graph[level].setdefault(neighbor_id, [])
                    self._graph[level][neighbor_id].append(entry.canonical_id)
                    if len(self._graph[level][neighbor_id]) > self.config.max_connections:
                        n_vec = self._entries[neighbor_id].vector
                        self._graph[level][neighbor_id] = self._select_neighbors(
                            n_vec, self._graph[level][neighbor_id], self.config.max_connections
                        )

                if neighbors:
                    current = neighbors[0]

            if node_level > self._max_level:
                self._max_level = node_level
                self._entry_point = entry.canonical_id

    def search(self, query: tuple[float, ...], k: int = 10) -> list[tuple[str, float]]:
        if self._entry_point is None:
            return []

        current = self._entry_point
        for level in range(self._max_level, 0, -1):
            current = self._greedy_search_layer(query, current, level)

        candidates = self._search_layer(query, current, max(self.config.ef_search, k), 0)
        results: list[tuple[str, float]] = []
        for cid in candidates[:k]:
            entry = self._entries.get(cid)
            if entry:
                dist = self._dist_fn(query, entry.vector)
                results.append((cid, 1.0 - dist if self.config.distance_metric == "cosine" else -dist))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]

    def _greedy_search_layer(self, query: tuple[float, ...], entry: str, level: int) -> str:
        current = entry
        current_dist = self._distance(query, current)
        changed = True
        while changed:
            changed = False
            neighbors = self._graph.get(level, {}).get(current, [])
            for neighbor in neighbors:
                d = self._distance(query, neighbor)
                if d < current_dist:
                    current = neighbor
                    current_dist = d
                    changed = True
        return current

    def _search_layer(self, query: tuple[float, ...], entry: str, ef: int, level: int) -> list[str]:
        visited: set[str] = {entry}
        candidates: list[tuple[float, str]] = [(self._distance(query, entry), entry)]
        results: list[tuple[float, str]] = [(self._distance(query, entry), entry)]
        heapq.heapify(candidates)

        while candidates:
            dist_c, current = heapq.heappop(candidates)
            if results and dist_c > max(r[0] for r in results) and len(results) >= ef:
                break

            neighbors = self._graph.get(level, {}).get(current, [])
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                d = self._distance(query, neighbor)
                if len(results) < ef or d < max(r[0] for r in results):
                    heapq.heappush(candidates, (d, neighbor))
                    results.append((d, neighbor))
                    if len(results) > ef:
                        results.sort()
                        results = results[:ef]

        results.sort()
        return [cid for _, cid in results]

    def _select_neighbors(self, query: tuple[float, ...], candidates: list[str], max_neighbors: int) -> list[str]:
        if len(candidates) <= max_neighbors:
            return candidates
        scored = [(self._distance(query, cid), cid) for cid in candidates]
        scored.sort()
        return [cid for _, cid in scored[:max_neighbors]]

    def _distance(self, query: tuple[float, ...], node_id: str) -> float:
        entry = self._entries.get(node_id)
        if entry is None:
            return float("inf")
        return self._dist_fn(query, entry.vector)

    def remove(self, canonical_id: str) -> bool:
        with self._lock:
            if canonical_id not in self._entries:
                return False
            del self._entries[canonical_id]
            level = self._node_levels.pop(canonical_id, 0)
            for lv in range(level + 1):
                if lv in self._graph and canonical_id in self._graph[lv]:
                    neighbors = self._graph[lv].pop(canonical_id)
                    for n in neighbors:
                        if n in self._graph[lv]:
                            self._graph[lv][n] = [x for x in self._graph[lv][n] if x != canonical_id]
            return True

    @property
    def size(self) -> int:
        return len(self._entries)

    def get(self, canonical_id: str) -> VectorEntry | None:
        return self._entries.get(canonical_id)


class UnifiedVectorGraphPlanner:
    """Plans and executes unified vector similarity + graph traversal queries."""

    def __init__(self, store: GraphStore, vector_index: HNSWIndex) -> None:
        self.store = store
        self.index = vector_index

    def vector_then_traverse(
        self,
        query_vector: tuple[float, ...],
        *,
        top_k: int = 10,
        hop_labels: list[str] | None = None,
        max_hops: int = 2,
        limit: int = 50,
    ) -> list[VectorSearchResult]:
        """Find nearest vectors, then expand graph context via multi-hop traversal."""
        started = time.monotonic()
        nn_results = self.index.search(query_vector, k=top_k)

        results: list[VectorSearchResult] = []
        for cid, score in nn_results:
            entry = self.index.get(cid)
            if entry is None:
                continue

            graph_ctx = self._traverse_hops(cid, hop_labels, max_hops)
            results.append(VectorSearchResult(
                canonical_id=cid,
                score=score,
                vector=entry.vector,
                metadata=dict(entry.metadata),
                graph_context=graph_ctx,
            ))

        elapsed_ms = (time.monotonic() - started) * 1000
        log.debug("vector_then_traverse: %d results in %.1fms", len(results), elapsed_ms)
        return results[:limit]

    def graph_then_vector(
        self,
        root_vid: str,
        query_vector: tuple[float, ...],
        *,
        hop_labels: list[str] | None = None,
        max_hops: int = 2,
        top_k: int = 10,
    ) -> list[VectorSearchResult]:
        """Start from a graph node, traverse hops, then rank neighbors by vector similarity."""
        neighbor_ids = self._collect_neighbor_ids(root_vid, hop_labels, max_hops)

        scored: list[tuple[float, str]] = []
        for nid in neighbor_ids:
            entry = self.index.get(nid)
            if entry is None:
                continue
            dist = _cosine_distance(query_vector, entry.vector)
            scored.append((1.0 - dist, nid))

        scored.sort(key=lambda x: x[0], reverse=True)
        results: list[VectorSearchResult] = []
        for score, cid in scored[:top_k]:
            entry = self.index.get(cid)
            if entry:
                results.append(VectorSearchResult(
                    canonical_id=cid,
                    score=score,
                    vector=entry.vector,
                    metadata=dict(entry.metadata),
                ))
        return results

    def hybrid_search(
        self,
        query_vector: tuple[float, ...],
        *,
        top_k: int = 10,
        max_hops: int = 2,
        vector_weight: float = 0.7,
        graph_weight: float = 0.3,
    ) -> list[VectorSearchResult]:
        """Reciprocal rank fusion of vector similarity and graph centrality."""
        nn_results = self.index.search(query_vector, k=top_k * 3)

        candidates: dict[str, dict[str, float]] = {}
        for rank, (cid, score) in enumerate(nn_results):
            candidates.setdefault(cid, {})["vector_rrf"] = 1.0 / (rank + 60)

        for cid in list(candidates):
            neighbors = self._collect_neighbor_ids(cid, None, max_hops)
            degree = len(neighbors)
            candidates[cid]["graph_rrf"] = degree / (degree + 10)

        final: list[tuple[float, str]] = []
        for cid, scores in candidates.items():
            combined = (
                vector_weight * scores.get("vector_rrf", 0)
                + graph_weight * scores.get("graph_rrf", 0)
            )
            final.append((combined, cid))

        final.sort(key=lambda x: x[0], reverse=True)
        results: list[VectorSearchResult] = []
        for score, cid in final[:top_k]:
            entry = self.index.get(cid)
            if entry:
                results.append(VectorSearchResult(
                    canonical_id=cid,
                    score=score,
                    vector=entry.vector,
                    metadata=dict(entry.metadata),
                ))
        return results

    def _traverse_hops(self, vid: str, labels: list[str] | None, max_hops: int) -> dict[str, Any]:
        neighbors: list[dict[str, str]] = []
        visited: set[str] = {vid}
        queue: list[tuple[str, int]] = [(vid, 0)]
        while queue:
            current, depth = queue.pop(0)
            if depth >= max_hops:
                continue
            try:
                edges = self.store.edges_from(current, labels=labels, limit=50)
            except Exception:
                continue
            for edge in edges:
                target = str(edge.get("in_v") or edge.get("in_cid", ""))
                if target and target not in visited:
                    visited.add(target)
                    neighbors.append({
                        "id": target,
                        "edge": str(edge.get("label", "")),
                        "depth": depth + 1,
                    })
                    queue.append((target, depth + 1))
        return {"neighbor_count": len(neighbors), "neighbors": neighbors[:20]}

    def _collect_neighbor_ids(self, vid: str, labels: list[str] | None, max_hops: int) -> set[str]:
        visited: set[str] = {vid}
        queue: list[tuple[str, int]] = [(vid, 0)]
        while queue:
            current, depth = queue.pop(0)
            if depth >= max_hops:
                continue
            try:
                edges = self.store.edges_from(current, labels=labels, limit=100)
            except Exception:
                continue
            for edge in edges:
                target = str(edge.get("in_v") or edge.get("in_cid", ""))
                if target and target not in visited:
                    visited.add(target)
                    queue.append((target, depth + 1))
        return visited


class VectorGraphAdapter:
    """Top-level adapter that manages the co-located vector index alongside a graph store."""

    def __init__(self, store: GraphStore, config: HNSWConfig | None = None) -> None:
        self.store = store
        self.index = HNSWIndex(config)
        self.planner = UnifiedVectorGraphPlanner(store, self.index)

    def index_vertex(self, canonical_id: str, vector: list[float], metadata: dict[str, Any] | None = None) -> None:
        entry = VectorEntry(
            canonical_id=canonical_id,
            vector=tuple(vector),
            metadata=metadata or {},
        )
        self.index.insert(entry)

    def search(self, query_vector: list[float], *, top_k: int = 10, max_hops: int = 2) -> list[VectorSearchResult]:
        return self.planner.vector_then_traverse(
            tuple(query_vector), top_k=top_k, max_hops=max_hops,
        )

    def hybrid_search(self, query_vector: list[float], *, top_k: int = 10) -> list[VectorSearchResult]:
        return self.planner.hybrid_search(tuple(query_vector), top_k=top_k)

    @property
    def vector_count(self) -> int:
        return self.index.size
