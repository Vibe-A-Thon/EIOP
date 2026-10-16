"""Extended graph algorithms: cycle detection, weighted paths, recommendations.

Pure-Python implementations operating on the GraphStore port.
Covers HugeGraph-compatible algorithm set requested for agent-driven analysis.
"""

from __future__ import annotations

import heapq
import math
import random
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any

from eoip.graph.store import GraphStore


@dataclass
class CycleResult:
    """A detected cycle (ring) in the graph."""

    cycle: list[str]
    length: int

    def to_dict(self) -> dict[str, Any]:
        return {"cycle": self.cycle, "length": self.length}


@dataclass
class WeightedPath:
    """A path with accumulated weight/cost."""

    path: list[str]
    total_weight: float
    hop_count: int

    def to_dict(self) -> dict[str, Any]:
        return {"path": self.path, "total_weight": self.total_weight, "hop_count": self.hop_count}


@dataclass
class KStepResult:
    """K-step neighborhood result."""

    center: str
    depth: int
    neighbors: dict[int, list[str]]
    total_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "center": self.center,
            "depth": self.depth,
            "neighbors": {str(k): v for k, v in self.neighbors.items()},
            "total_count": self.total_count,
        }


@dataclass
class CoNeighborResult:
    """Co-neighbor (shared neighbor) analysis between two nodes."""

    source: str
    target: str
    shared_neighbors: list[str]
    shared_count: int
    source_degree: int
    target_degree: int
    overlap_coefficient: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "shared_neighbors": self.shared_neighbors,
            "shared_count": self.shared_count,
            "source_degree": self.source_degree,
            "target_degree": self.target_degree,
            "overlap_coefficient": self.overlap_coefficient,
        }


@dataclass
class IntersectionResult:
    """Intersection nodes between two subgraphs."""

    subgraph_a_root: str
    subgraph_b_root: str
    intersection_nodes: list[str]
    intersection_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "subgraph_a_root": self.subgraph_a_root,
            "subgraph_b_root": self.subgraph_b_root,
            "intersection_nodes": self.intersection_nodes,
            "intersection_count": self.intersection_count,
        }


@dataclass
class RayResult:
    """Directional ray traversal from a source node."""

    source: str
    direction: str
    edge_labels: list[str]
    visited: list[str]
    depth_reached: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "direction": self.direction,
            "edge_labels": self.edge_labels,
            "visited": self.visited,
            "depth_reached": self.depth_reached,
        }


class GraphAlgorithms:
    """Extended graph algorithms for analysis and recommendation."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    def _build_undirected_adj(self, limit: int = 50_000) -> tuple[dict[str, set[str]], dict[str, str]]:
        vertices = self._store.find_vertices(limit=limit)
        vid_to_cid: dict[str, str] = {}
        for v in vertices:
            vid_to_cid[v["vid"]] = v["properties"]["canonical_id"]

        adj: dict[str, set[str]] = defaultdict(set)
        for v in vertices:
            src_cid = vid_to_cid[v["vid"]]
            for edge in self._store.edges_from(v["vid"]):
                tgt_cid = vid_to_cid.get(edge["in_v"])
                if tgt_cid and tgt_cid != src_cid:
                    adj[src_cid].add(tgt_cid)
                    adj[tgt_cid].add(src_cid)
        return dict(adj), vid_to_cid

    def _build_directed_adj(self, limit: int = 50_000) -> tuple[dict[str, set[str]], dict[str, set[str]], dict[str, str]]:
        vertices = self._store.find_vertices(limit=limit)
        vid_to_cid: dict[str, str] = {}
        for v in vertices:
            vid_to_cid[v["vid"]] = v["properties"]["canonical_id"]

        out_adj: dict[str, set[str]] = defaultdict(set)
        in_adj: dict[str, set[str]] = defaultdict(set)
        for v in vertices:
            src_cid = vid_to_cid[v["vid"]]
            for edge in self._store.edges_from(v["vid"]):
                tgt_cid = vid_to_cid.get(edge["in_v"])
                if tgt_cid and tgt_cid != src_cid:
                    out_adj[src_cid].add(tgt_cid)
                    in_adj[tgt_cid].add(src_cid)
        return dict(out_adj), dict(in_adj), vid_to_cid

    def _edge_weight(self, from_vid: str, to_vid: str) -> float:
        for edge in self._store.edges_from(from_vid):
            if edge["in_v"] == to_vid:
                props = edge.get("properties", {})
                return float(props.get("weight", props.get("confidence", 1.0)))
        return 1.0

    def _build_weighted_adj(self, limit: int = 50_000) -> tuple[dict[str, list[tuple[str, float]]], dict[str, str]]:
        vertices = self._store.find_vertices(limit=limit)
        vid_to_cid: dict[str, str] = {}
        cid_to_vid: dict[str, str] = {}
        for v in vertices:
            cid = v["properties"]["canonical_id"]
            vid_to_cid[v["vid"]] = cid
            cid_to_vid[cid] = v["vid"]

        adj: dict[str, list[tuple[str, float]]] = defaultdict(list)
        for v in vertices:
            src_cid = vid_to_cid[v["vid"]]
            for edge in self._store.edges_from(v["vid"]):
                tgt_cid = vid_to_cid.get(edge["in_v"])
                if tgt_cid and tgt_cid != src_cid:
                    w = float(edge.get("properties", {}).get("weight", 1.0))
                    adj[src_cid].append((tgt_cid, w))
                    adj[tgt_cid].append((src_cid, w))
        return dict(adj), vid_to_cid

    # ------------------------------------------------------------------
    # Ring (cycle) detection
    # ------------------------------------------------------------------

    def detect_rings(self, max_length: int = 10, limit: int = 20) -> list[CycleResult]:
        """Detect cycles/rings in the directed graph using DFS."""
        out_adj, _, _ = self._build_directed_adj()
        all_nodes = set(out_adj.keys())
        cycles: list[list[str]] = []
        visited_global: set[str] = set()

        for start in all_nodes:
            if len(cycles) >= limit:
                break
            stack: list[tuple[str, list[str], set[str]]] = [(start, [start], {start})]
            while stack and len(cycles) < limit:
                node, path, on_stack = stack.pop()
                for nbr in out_adj.get(node, set()):
                    if nbr == start and len(path) >= 2:
                        cycle = path + [start]
                        if len(cycle) - 1 <= max_length:
                            normalized = self._normalize_cycle(cycle[:-1])
                            if normalized not in visited_global:
                                visited_global.add(normalized)
                                cycles.append(cycle)
                    elif nbr not in on_stack and len(path) < max_length:
                        stack.append((nbr, path + [nbr], on_stack | {nbr}))

        return [CycleResult(cycle=c, length=len(c) - 1) for c in cycles[:limit]]

    @staticmethod
    def _normalize_cycle(cycle: list[str]) -> str:
        if not cycle:
            return ""
        min_idx = cycle.index(min(cycle))
        rotated = cycle[min_idx:] + cycle[:min_idx]
        return "|".join(rotated)

    # ------------------------------------------------------------------
    # Intersection detection
    # ------------------------------------------------------------------

    def detect_intersection(
        self, root_a: str, root_b: str, max_depth: int = 4
    ) -> IntersectionResult:
        """Find nodes reachable from both root_a and root_b within max_depth."""
        adj, _ = self._build_undirected_adj()

        def _bfs_reachable(start: str) -> set[str]:
            visited: set[str] = {start}
            queue: deque[tuple[str, int]] = deque([(start, 0)])
            while queue:
                node, depth = queue.popleft()
                if depth >= max_depth:
                    continue
                for nbr in adj.get(node, set()):
                    if nbr not in visited:
                        visited.add(nbr)
                        queue.append((nbr, depth + 1))
            return visited

        reachable_a = _bfs_reachable(root_a)
        reachable_b = _bfs_reachable(root_b)
        intersection = sorted(reachable_a & reachable_b - {root_a, root_b})

        return IntersectionResult(
            subgraph_a_root=root_a,
            subgraph_b_root=root_b,
            intersection_nodes=intersection,
            intersection_count=len(intersection),
        )

    # ------------------------------------------------------------------
    # Weighted shortest path (Dijkstra)
    # ------------------------------------------------------------------

    def weighted_shortest_path(
        self, source_id: str, target_id: str
    ) -> WeightedPath | None:
        """Dijkstra's algorithm for single-pair weighted shortest path."""
        wadj, _ = self._build_weighted_adj()
        if source_id not in wadj and source_id != target_id:
            return None

        dist: dict[str, float] = {source_id: 0.0}
        prev: dict[str, str | None] = {source_id: None}
        heap: list[tuple[float, str]] = [(0.0, source_id)]

        while heap:
            d, node = heapq.heappop(heap)
            if node == target_id:
                path: list[str] = []
                cur: str | None = target_id
                while cur is not None:
                    path.append(cur)
                    cur = prev.get(cur)
                path.reverse()
                return WeightedPath(path=path, total_weight=d, hop_count=len(path) - 1)
            if d > dist.get(node, math.inf):
                continue
            for nbr, w in wadj.get(node, []):
                nd = d + w
                if nd < dist.get(nbr, math.inf):
                    dist[nbr] = nd
                    prev[nbr] = node
                    heapq.heappush(heap, (nd, nbr))

        return None

    # ------------------------------------------------------------------
    # Single-source weighted shortest paths
    # ------------------------------------------------------------------

    def single_source_weighted_paths(
        self, source_id: str, limit: int = 100
    ) -> dict[str, WeightedPath]:
        """Dijkstra from a single source to all reachable nodes."""
        wadj, _ = self._build_weighted_adj()
        dist: dict[str, float] = {source_id: 0.0}
        prev: dict[str, str | None] = {source_id: None}
        heap: list[tuple[float, str]] = [(0.0, source_id)]
        settled: set[str] = set()

        while heap and len(settled) < limit:
            d, node = heapq.heappop(heap)
            if node in settled:
                continue
            settled.add(node)
            if d > dist.get(node, math.inf):
                continue
            for nbr, w in wadj.get(node, []):
                nd = d + w
                if nd < dist.get(nbr, math.inf):
                    dist[nbr] = nd
                    prev[nbr] = node
                    heapq.heappush(heap, (nd, nbr))

        results: dict[str, WeightedPath] = {}
        for target, d in sorted(dist.items(), key=lambda x: x[1]):
            if target == source_id:
                continue
            path: list[str] = []
            cur: str | None = target
            while cur is not None:
                path.append(cur)
                cur = prev.get(cur)
            path.reverse()
            results[target] = WeightedPath(path=path, total_weight=d, hop_count=len(path) - 1)
        return results

    # ------------------------------------------------------------------
    # K-step neighbor
    # ------------------------------------------------------------------

    def k_step_neighbors(
        self, canonical_id: str, k: int = 3, limit: int = 500
    ) -> KStepResult:
        """Extract the K-hop neighborhood of a node."""
        adj, _ = self._build_undirected_adj()
        neighbors: dict[int, list[str]] = {}
        visited: set[str] = {canonical_id}
        current_layer: set[str] = {canonical_id}
        total = 0

        for depth in range(1, k + 1):
            next_layer: set[str] = set()
            for node in current_layer:
                for nbr in adj.get(node, set()):
                    if nbr not in visited and total < limit:
                        next_layer.add(nbr)
                        visited.add(nbr)
                        total += 1
            if next_layer:
                neighbors[depth] = sorted(next_layer)
            current_layer = next_layer
            if not current_layer:
                break

        return KStepResult(
            center=canonical_id, depth=k, neighbors=neighbors, total_count=total
        )

    # ------------------------------------------------------------------
    # K-jump (random walk)
    # ------------------------------------------------------------------

    def k_jump(
        self, start_id: str, k: int = 5, walks: int = 10, seed: int | None = None
    ) -> dict[str, float]:
        """K-jump random walk: visit probability after k hops from start.

        Returns {canonical_id: visit_probability} for nodes visited across
        *walks* independent random walks of length *k*.
        """
        adj, _ = self._build_undirected_adj()
        rng = random.Random(seed)
        visit_count: dict[str, int] = defaultdict(int)

        for _ in range(walks):
            current = start_id
            for _ in range(k):
                neighbors = list(adj.get(current, set()))
                if not neighbors:
                    break
                current = rng.choice(neighbors)
            visit_count[current] += 1

        return {cid: count / walks for cid, count in sorted(visit_count.items(), key=lambda x: -x[1])}

    # ------------------------------------------------------------------
    # Custom path (constrained path finding)
    # ------------------------------------------------------------------

    def custom_path(
        self,
        source_id: str,
        target_id: str,
        allowed_labels: list[str] | None = None,
        blocked_labels: list[str] | None = None,
        max_depth: int = 6,
        max_paths: int = 5,
    ) -> list[list[str]]:
        """Find paths between two nodes with edge label constraints."""
        source = self._store.get_vertex_by_canonical_id(source_id)
        target = self._store.get_vertex_by_canonical_id(target_id)
        if source is None or target is None:
            return []

        src_vid = source["vid"]
        tgt_vid = target["vid"]
        allowed = set(allowed_labels) if allowed_labels else None
        blocked = set(blocked_labels) if blocked_labels else set()

        vertices = self._store.find_vertices(limit=50_000)
        vid_to_cid: dict[str, str] = {v["vid"]: v["properties"]["canonical_id"] for v in vertices}

        paths: list[list[str]] = []
        stack: list[tuple[str, list[str], set[str]]] = [(src_vid, [src_vid], {src_vid})]

        while stack and len(paths) < max_paths:
            node, path, visited = stack.pop()
            if len(path) - 1 >= max_depth:
                continue
            for edge in self._store.edges_from(node):
                label = edge.get("label", "")
                if allowed is not None and label not in allowed:
                    continue
                if label in blocked:
                    continue
                nbr = edge["in_v"]
                if nbr == tgt_vid:
                    cid_path = [vid_to_cid.get(v, v) for v in path + [nbr]]
                    paths.append(cid_path)
                elif nbr not in visited:
                    stack.append((nbr, path + [nbr], visited | {nbr}))
            for edge in self._store.edges_to(node):
                label = edge.get("label", "")
                if allowed is not None and label not in allowed:
                    continue
                if label in blocked:
                    continue
                nbr = edge["out_v"]
                if nbr == tgt_vid:
                    cid_path = [vid_to_cid.get(v, v) for v in path + [nbr]]
                    paths.append(cid_path)
                elif nbr not in visited:
                    stack.append((nbr, path + [nbr], visited | {nbr}))

        return paths

    # ------------------------------------------------------------------
    # Ray detection (directional traversal)
    # ------------------------------------------------------------------

    def ray_detection(
        self,
        source_id: str,
        direction: str = "outgoing",
        edge_labels: list[str] | None = None,
        max_depth: int = 10,
    ) -> RayResult:
        """Follow a directed ray from source along specified edge types.

        direction: 'outgoing' follows edges_from, 'incoming' follows edges_to.
        """
        source = self._store.get_vertex_by_canonical_id(source_id)
        if source is None:
            return RayResult(source=source_id, direction=direction,
                             edge_labels=edge_labels or [], visited=[], depth_reached=0)

        label_filter = set(edge_labels) if edge_labels else None
        visited: list[str] = []
        seen: set[str] = {source["vid"]}
        current_vids: list[str] = [source["vid"]]
        depth = 0

        vertices_cache: dict[str, str] = {}

        for _ in range(max_depth):
            next_vids: list[str] = []
            for vid in current_vids:
                edges = (self._store.edges_from(vid) if direction == "outgoing"
                         else self._store.edges_to(vid))
                for edge in edges:
                    if label_filter and edge.get("label", "") not in label_filter:
                        continue
                    nbr = edge["in_v"] if direction == "outgoing" else edge["out_v"]
                    if nbr not in seen:
                        seen.add(nbr)
                        next_vids.append(nbr)
                        if nbr not in vertices_cache:
                            v = self._store.get_vertex(nbr)
                            if v:
                                vertices_cache[nbr] = v["properties"]["canonical_id"]
                        if nbr in vertices_cache:
                            visited.append(vertices_cache[nbr])
            if not next_vids:
                break
            current_vids = next_vids
            depth += 1

        return RayResult(
            source=source_id,
            direction=direction,
            edge_labels=edge_labels or [],
            visited=visited,
            depth_reached=depth,
        )

    # ------------------------------------------------------------------
    # Co-neighbor analysis
    # ------------------------------------------------------------------

    def co_neighbors(
        self, source_id: str, target_id: str
    ) -> CoNeighborResult:
        """Analyze shared neighbors between two nodes."""
        adj, _ = self._build_undirected_adj()
        src_nbrs = adj.get(source_id, set())
        tgt_nbrs = adj.get(target_id, set())
        shared = src_nbrs & tgt_nbrs
        min_deg = min(len(src_nbrs), len(tgt_nbrs)) if src_nbrs and tgt_nbrs else 1

        return CoNeighborResult(
            source=source_id,
            target=target_id,
            shared_neighbors=sorted(shared),
            shared_count=len(shared),
            source_degree=len(src_nbrs),
            target_degree=len(tgt_nbrs),
            overlap_coefficient=len(shared) / max(min_deg, 1),
        )

    # ------------------------------------------------------------------
    # Personal Rank (Personalized PageRank)
    # ------------------------------------------------------------------

    def personal_rank(
        self,
        source_id: str,
        alpha: float = 0.85,
        iterations: int = 40,
        limit: int = 20,
    ) -> list[tuple[str, float]]:
        """Personalized PageRank for recommendation.

        Computes PageRank with teleportation bias toward source_id.
        Returns [(canonical_id, score)] sorted by descending score.
        """
        adj, _ = self._build_undirected_adj()
        all_nodes = set(adj.keys())
        if source_id not in all_nodes:
            return []

        n = len(all_nodes)
        pr: dict[str, float] = {node: 1.0 / n for node in all_nodes}

        for _ in range(iterations):
            new_pr: dict[str, float] = {}
            dangling = sum(pr[node] for node in all_nodes if not adj.get(node))
            for node in all_nodes:
                teleport = (1 - alpha) * (1.0 if node == source_id else 0.0)
                rank = teleport + alpha * dangling / n
                for nbr in adj.get(node, set()):
                    rank += alpha * pr[nbr] / len(adj.get(nbr, {nbr}))
                new_pr[node] = rank
            pr = new_pr

        results = [(cid, score) for cid, score in pr.items() if cid != source_id]
        results.sort(key=lambda x: -x[1])
        return results[:limit]

    # ------------------------------------------------------------------
    # Neighbor Rank recommendation
    # ------------------------------------------------------------------

    def neighbor_rank(
        self,
        source_id: str,
        alpha: float = 0.5,
        limit: int = 20,
    ) -> list[tuple[str, float]]:
        """Neighbor Rank: rank nodes by weighted neighborhood contribution.

        alpha controls decay per hop. Score = sum over paths of
        alpha^depth * (1/degree_at_each_hop).
        """
        adj, _ = self._build_undirected_adj()
        if source_id not in adj:
            return []

        scores: dict[str, float] = defaultdict(float)
        visited: set[str] = {source_id}
        current: dict[str, float] = {source_id: 1.0}
        max_depth = 4

        for depth in range(1, max_depth + 1):
            next_layer: dict[str, float] = defaultdict(float)
            decay = alpha ** depth
            for node, incoming_score in current.items():
                neighbors = adj.get(node, set())
                if not neighbors:
                    continue
                share = incoming_score / len(neighbors)
                for nbr in neighbors:
                    contribution = decay * share
                    next_layer[nbr] += contribution
                    if nbr not in visited:
                        scores[nbr] += contribution

            visited.update(next_layer.keys())
            current = dict(next_layer)
            if not current:
                break

        results = sorted(scores.items(), key=lambda x: -x[1])
        return results[:limit]

    # ------------------------------------------------------------------
    # Model similarity (graph-level structural comparison)
    # ------------------------------------------------------------------

    def model_similarity(
        self,
        nodes_a: list[str],
        nodes_b: list[str],
    ) -> dict[str, Any]:
        """Compare structural similarity between two sets of nodes (subgraph models).

        Returns Jaccard on node sets, edge overlap, degree distribution similarity.
        """
        adj, _ = self._build_undirected_adj()

        set_a = set(nodes_a)
        set_b = set(nodes_b)
        node_jaccard = len(set_a & set_b) / max(len(set_a | set_b), 1)

        def _edges_in(nodes: set[str]) -> set[tuple[str, str]]:
            edges: set[tuple[str, str]] = set()
            for n in nodes:
                for nbr in adj.get(n, set()):
                    if nbr in nodes:
                        edge = (min(n, nbr), max(n, nbr))
                        edges.add(edge)
            return edges

        edges_a = _edges_in(set_a)
        edges_b = _edges_in(set_b)
        edge_jaccard = len(edges_a & edges_b) / max(len(edges_a | edges_b), 1)

        def _degree_dist(nodes: set[str]) -> dict[int, int]:
            dist: dict[int, int] = defaultdict(int)
            for n in nodes:
                deg = len(adj.get(n, set()) & nodes)
                dist[deg] += 1
            return dict(dist)

        dd_a = _degree_dist(set_a)
        dd_b = _degree_dist(set_b)
        all_degrees = set(dd_a.keys()) | set(dd_b.keys())
        if all_degrees:
            norm_a = max(sum(dd_a.values()), 1)
            norm_b = max(sum(dd_b.values()), 1)
            cosine_num = sum((dd_a.get(d, 0) / norm_a) * (dd_b.get(d, 0) / norm_b) for d in all_degrees)
            mag_a = math.sqrt(sum((dd_a.get(d, 0) / norm_a) ** 2 for d in all_degrees))
            mag_b = math.sqrt(sum((dd_b.get(d, 0) / norm_b) ** 2 for d in all_degrees))
            degree_similarity = cosine_num / max(mag_a * mag_b, 1e-12)
        else:
            degree_similarity = 0.0

        return {
            "node_jaccard": round(node_jaccard, 6),
            "edge_jaccard": round(edge_jaccard, 6),
            "degree_distribution_cosine": round(degree_similarity, 6),
            "combined_score": round((node_jaccard + edge_jaccard + degree_similarity) / 3, 6),
            "subgraph_a_size": len(set_a),
            "subgraph_b_size": len(set_b),
        }
