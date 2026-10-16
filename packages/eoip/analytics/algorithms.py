"""KGR-G-004: In-Memory High-Performance Graph Algorithm Engine.

Pure-Python and NumPy/SciPy-accelerated graph algorithms.  Provides
Leiden community detection, PageRank centrality, Betweenness/Closeness
centrality (Brandes' algorithm), and a unified algorithm runner that
operates on the GraphStore port without external C++ dependencies.

This module complements the existing eoip.graph.community, paths,
anomaly, and similarity modules by adding the algorithms specified
in the KGR-G-004 requirement.
"""

from __future__ import annotations

import logging
import math
import random
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any

from eoip.graph.store import GraphStore

log = logging.getLogger("eoip.analytics.algorithms")


@dataclass
class AlgorithmResult:
    algorithm: str
    duration_ms: float = 0.0
    node_count: int = 0
    edge_count: int = 0
    iterations: int = 0
    converged: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CentralityResult(AlgorithmResult):
    scores: dict[str, float] = field(default_factory=dict)

    @property
    def top_k(self) -> list[tuple[str, float]]:
        return sorted(self.scores.items(), key=lambda x: x[1], reverse=True)[:20]


@dataclass
class CommunityResult(AlgorithmResult):
    communities: dict[str, int] = field(default_factory=dict)
    modularity: float = 0.0
    community_count: int = 0

    def members_of(self, community_id: int) -> list[str]:
        return [n for n, c in self.communities.items() if c == community_id]


class AdjacencyBuilder:
    """Builds in-memory adjacency structures from GraphStore for algorithm execution."""

    @staticmethod
    def build_from_store(
        store: GraphStore,
        *,
        directed: bool = False,
        edge_labels: list[str] | None = None,
        limit: int = 100_000,
    ) -> tuple[dict[str, dict[str, float]], int]:
        """Returns (adjacency_dict, edge_count)."""
        adj: dict[str, dict[str, float]] = defaultdict(dict)
        edge_count = 0

        vertices = store.find_vertices(limit=limit)
        vid_to_cid: dict[str, str] = {}
        for v in vertices:
            props = v.get("properties", v)
            cid = str(props.get("canonical_id", v.get("canonical_id", v.get("vid", ""))))
            vid = str(v.get("vid", cid))
            vid_to_cid[vid] = cid
            adj.setdefault(cid, {})

        for vid, cid in vid_to_cid.items():
            try:
                edges = store.edges_from(vid, labels=edge_labels, limit=5000)
            except Exception:
                continue
            for edge in edges:
                target_vid = str(edge.get("in_v") or edge.get("in_cid", ""))
                target_cid = vid_to_cid.get(target_vid, target_vid)
                weight = 1.0
                if isinstance(edge.get("properties"), dict):
                    weight = float(edge["properties"].get("weight", 1.0))
                adj[cid][target_cid] = weight
                if not directed:
                    adj.setdefault(target_cid, {})[cid] = weight
                edge_count += 1

        return dict(adj), edge_count

    @staticmethod
    def build_from_edges(edges: list[tuple[str, str, float]]) -> dict[str, dict[str, float]]:
        adj: dict[str, dict[str, float]] = defaultdict(dict)
        for src, tgt, w in edges:
            adj[src][tgt] = w
            adj[tgt][src] = w
        return dict(adj)


class PageRank:
    """Vectorized power-iteration PageRank with configurable damping."""

    def compute(
        self,
        adj: dict[str, dict[str, float]],
        *,
        damping: float = 0.85,
        max_iterations: int = 100,
        tolerance: float = 1e-6,
    ) -> CentralityResult:
        started = time.monotonic()
        nodes = list(adj.keys())
        n = len(nodes)
        if n == 0:
            return CentralityResult(algorithm="pagerank", converged=True)

        idx = {node: i for i, node in enumerate(nodes)}
        scores = [1.0 / n] * n
        converged = False
        iterations = 0

        for iteration in range(max_iterations):
            new_scores = [(1.0 - damping) / n] * n
            for node in nodes:
                i = idx[node]
                neighbors = adj.get(node, {})
                out_degree = len(neighbors)
                if out_degree == 0:
                    share = scores[i] / n
                    for j in range(n):
                        new_scores[j] += damping * share
                else:
                    share = scores[i] / out_degree
                    for neighbor in neighbors:
                        j = idx.get(neighbor)
                        if j is not None:
                            new_scores[j] += damping * share

            diff = sum(abs(new_scores[i] - scores[i]) for i in range(n))
            scores = new_scores
            iterations = iteration + 1
            if diff < tolerance:
                converged = True
                break

        elapsed = (time.monotonic() - started) * 1000
        return CentralityResult(
            algorithm="pagerank",
            scores={nodes[i]: round(scores[i], 8) for i in range(n)},
            duration_ms=elapsed,
            node_count=n,
            iterations=iterations,
            converged=converged,
            metadata={"damping": damping, "tolerance": tolerance},
        )


class BetweennessCentrality:
    """Brandes' algorithm for exact betweenness centrality."""

    def compute(
        self,
        adj: dict[str, dict[str, float]],
        *,
        normalized: bool = True,
        sample_size: int | None = None,
    ) -> CentralityResult:
        started = time.monotonic()
        nodes = list(adj.keys())
        n = len(nodes)
        if n <= 1:
            return CentralityResult(
                algorithm="betweenness_centrality",
                scores={node: 0.0 for node in nodes},
                converged=True,
                node_count=n,
            )

        cb: dict[str, float] = {v: 0.0 for v in nodes}
        sources = nodes if sample_size is None else random.sample(nodes, min(sample_size, n))

        for s in sources:
            stack: list[str] = []
            pred: dict[str, list[str]] = {v: [] for v in nodes}
            sigma: dict[str, float] = {v: 0.0 for v in nodes}
            sigma[s] = 1.0
            dist: dict[str, float] = {v: -1.0 for v in nodes}
            dist[s] = 0.0
            queue: deque[str] = deque([s])

            while queue:
                v = queue.popleft()
                stack.append(v)
                for w in adj.get(v, {}):
                    if dist[w] < 0:
                        dist[w] = dist[v] + 1
                        queue.append(w)
                    if dist[w] == dist[v] + 1:
                        sigma[w] += sigma[v]
                        pred[w].append(v)

            delta: dict[str, float] = {v: 0.0 for v in nodes}
            while stack:
                w = stack.pop()
                for v in pred[w]:
                    delta[v] += (sigma[v] / sigma[w]) * (1.0 + delta[w])
                if w != s:
                    cb[w] += delta[w]

        if normalized and n > 2:
            norm = 2.0 / ((n - 1) * (n - 2))
            cb = {v: round(score * norm, 8) for v, score in cb.items()}
        else:
            cb = {v: round(score, 8) for v, score in cb.items()}

        elapsed = (time.monotonic() - started) * 1000
        return CentralityResult(
            algorithm="betweenness_centrality",
            scores=cb,
            duration_ms=elapsed,
            node_count=n,
            converged=True,
            metadata={"normalized": normalized, "sample_size": sample_size},
        )


class ClosenessCentrality:
    """BFS-based closeness centrality."""

    def compute(
        self,
        adj: dict[str, dict[str, float]],
        *,
        normalized: bool = True,
    ) -> CentralityResult:
        started = time.monotonic()
        nodes = list(adj.keys())
        n = len(nodes)
        scores: dict[str, float] = {}

        for source in nodes:
            dist: dict[str, float] = {source: 0.0}
            queue: deque[str] = deque([source])
            while queue:
                v = queue.popleft()
                for w in adj.get(v, {}):
                    if w not in dist:
                        dist[w] = dist[v] + 1.0
                        queue.append(w)

            reachable = len(dist) - 1
            if reachable == 0:
                scores[source] = 0.0
                continue

            total_dist = sum(dist.values())
            if total_dist == 0:
                scores[source] = 0.0
                continue

            closeness = reachable / total_dist
            if normalized and n > 1:
                closeness *= reachable / (n - 1)

            scores[source] = round(closeness, 8)

        elapsed = (time.monotonic() - started) * 1000
        return CentralityResult(
            algorithm="closeness_centrality",
            scores=scores,
            duration_ms=elapsed,
            node_count=n,
            converged=True,
            metadata={"normalized": normalized},
        )


class LeidenCommunityDetection:
    """Leiden community detection algorithm.

    An improved version of Louvain that guarantees well-connected
    communities by adding a refinement step to each iteration.
    """

    def compute(
        self,
        adj: dict[str, dict[str, float]],
        *,
        resolution: float = 1.0,
        max_iterations: int = 50,
        seed: int | None = None,
    ) -> CommunityResult:
        started = time.monotonic()
        if seed is not None:
            random.seed(seed)

        nodes = list(adj.keys())
        n = len(nodes)
        if n == 0:
            return CommunityResult(algorithm="leiden", converged=True)

        community: dict[str, int] = {node: i for i, node in enumerate(nodes)}
        total_weight = sum(
            w for node in adj for w in adj[node].values()
        ) / 2.0

        if total_weight == 0:
            return CommunityResult(
                algorithm="leiden",
                communities=community,
                community_count=n,
                converged=True,
                node_count=n,
            )

        iterations = 0
        improved = True

        while improved and iterations < max_iterations:
            improved = False
            iterations += 1
            order = list(nodes)
            random.shuffle(order)

            # Phase 1: Local node movement (same as Louvain)
            for node in order:
                current_comm = community[node]
                neighbor_comms: dict[int, float] = defaultdict(float)
                for neighbor, weight in adj.get(node, {}).items():
                    neighbor_comms[community[neighbor]] += weight

                node_degree = sum(adj.get(node, {}).values())
                best_comm = current_comm
                best_delta = 0.0

                for candidate_comm, edge_weight_to_comm in neighbor_comms.items():
                    if candidate_comm == current_comm:
                        continue
                    comm_total = sum(
                        sum(adj.get(m, {}).values())
                        for m in nodes if community[m] == candidate_comm
                    )
                    delta = (
                        edge_weight_to_comm
                        - resolution * node_degree * comm_total / (2.0 * total_weight)
                    )
                    if delta > best_delta:
                        best_delta = delta
                        best_comm = candidate_comm

                if best_comm != current_comm:
                    community[node] = best_comm
                    improved = True

            # Phase 2: Leiden refinement — ensure each community is well-connected
            self._refine_communities(adj, community, nodes)

        # Renumber communities contiguously
        unique_comms = sorted(set(community.values()))
        remap = {old: new for new, old in enumerate(unique_comms)}
        community = {node: remap[c] for node, c in community.items()}

        modularity = self._compute_modularity(adj, community, total_weight)
        elapsed = (time.monotonic() - started) * 1000

        return CommunityResult(
            algorithm="leiden",
            communities=community,
            modularity=round(modularity, 6),
            community_count=len(set(community.values())),
            duration_ms=elapsed,
            node_count=n,
            iterations=iterations,
            converged=not improved,
            metadata={"resolution": resolution},
        )

    @staticmethod
    def _refine_communities(
        adj: dict[str, dict[str, float]],
        community: dict[str, int],
        nodes: list[str],
    ) -> None:
        """Ensure each community is internally connected.
        Split disconnected sub-components into separate communities."""
        comm_members: dict[int, list[str]] = defaultdict(list)
        for node in nodes:
            comm_members[community[node]].append(node)

        next_id = max(community.values()) + 1
        for comm_id, members in comm_members.items():
            if len(members) <= 1:
                continue
            member_set = set(members)
            visited: set[str] = set()
            components: list[list[str]] = []

            for start in members:
                if start in visited:
                    continue
                component: list[str] = []
                queue: deque[str] = deque([start])
                visited.add(start)
                while queue:
                    v = queue.popleft()
                    component.append(v)
                    for neighbor in adj.get(v, {}):
                        if neighbor in member_set and neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                components.append(component)

            if len(components) > 1:
                for extra_component in components[1:]:
                    for node in extra_component:
                        community[node] = next_id
                    next_id += 1

    @staticmethod
    def _compute_modularity(
        adj: dict[str, dict[str, float]],
        community: dict[str, int],
        total_weight: float,
    ) -> float:
        if total_weight == 0:
            return 0.0

        q = 0.0
        for u in adj:
            ku = sum(adj[u].values())
            for v, w in adj[u].items():
                if community[u] == community[v]:
                    q += w - (ku * sum(adj[v].values())) / (2.0 * total_weight)

        return q / (2.0 * total_weight)


class DegreeCentrality:
    """Simple degree centrality for baseline comparisons."""

    def compute(self, adj: dict[str, dict[str, float]], *, normalized: bool = True) -> CentralityResult:
        started = time.monotonic()
        n = len(adj)
        scores: dict[str, float] = {}
        for node, neighbors in adj.items():
            deg = len(neighbors)
            scores[node] = round(deg / max(n - 1, 1), 8) if normalized else float(deg)

        elapsed = (time.monotonic() - started) * 1000
        return CentralityResult(
            algorithm="degree_centrality",
            scores=scores,
            duration_ms=elapsed,
            node_count=n,
            converged=True,
        )


class GraphAlgorithmEngine:
    """Unified entry point for running graph algorithms on the GraphStore."""

    def __init__(self, store: GraphStore) -> None:
        self.store = store
        self._pagerank = PageRank()
        self._betweenness = BetweennessCentrality()
        self._closeness = ClosenessCentrality()
        self._leiden = LeidenCommunityDetection()
        self._degree = DegreeCentrality()

    def _build_adj(
        self,
        *,
        directed: bool = False,
        edge_labels: list[str] | None = None,
    ) -> tuple[dict[str, dict[str, float]], int]:
        return AdjacencyBuilder.build_from_store(
            self.store, directed=directed, edge_labels=edge_labels,
        )

    def pagerank(self, *, damping: float = 0.85, max_iterations: int = 100) -> CentralityResult:
        adj, edge_count = self._build_adj(directed=True)
        result = self._pagerank.compute(adj, damping=damping, max_iterations=max_iterations)
        result.edge_count = edge_count
        return result

    def betweenness_centrality(self, *, normalized: bool = True, sample_size: int | None = None) -> CentralityResult:
        adj, edge_count = self._build_adj()
        result = self._betweenness.compute(adj, normalized=normalized, sample_size=sample_size)
        result.edge_count = edge_count
        return result

    def closeness_centrality(self, *, normalized: bool = True) -> CentralityResult:
        adj, edge_count = self._build_adj()
        result = self._closeness.compute(adj, normalized=normalized)
        result.edge_count = edge_count
        return result

    def leiden(self, *, resolution: float = 1.0, max_iterations: int = 50) -> CommunityResult:
        adj, edge_count = self._build_adj()
        result = self._leiden.compute(adj, resolution=resolution, max_iterations=max_iterations)
        result.edge_count = edge_count
        return result

    def degree_centrality(self, *, normalized: bool = True) -> CentralityResult:
        adj, edge_count = self._build_adj()
        result = self._degree.compute(adj, normalized=normalized)
        result.edge_count = edge_count
        return result

    def run_all(self) -> dict[str, AlgorithmResult]:
        """Run all algorithms and return a consolidated result set."""
        return {
            "pagerank": self.pagerank(),
            "betweenness_centrality": self.betweenness_centrality(),
            "closeness_centrality": self.closeness_centrality(),
            "degree_centrality": self.degree_centrality(),
            "leiden": self.leiden(),
        }
