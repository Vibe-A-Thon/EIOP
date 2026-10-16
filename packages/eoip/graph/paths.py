"""Graph path-finding algorithms: all-shortest and k-shortest paths.

Pure-Python implementations operating on the GraphStore port.
Returns paths as lists of canonical_ids.
"""

from __future__ import annotations

import heapq
from collections import defaultdict, deque

from eoip.graph.store import GraphStore


class GraphPathFinder:
    """Find shortest paths between nodes in an EOIP GraphStore."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _vid_to_cid(self, vid: str) -> str | None:
        v = self._store.get_vertex(vid)
        if v is None:
            return None
        return v["properties"]["canonical_id"]

    def _neighbor_vids(self, vid: str) -> list[str]:
        """Return adjacent vertex ids (both directions)."""
        neighbors: list[str] = []
        for edge in self._store.edges_from(vid):
            neighbors.append(edge["in_v"])
        for edge in self._store.edges_to(vid):
            neighbors.append(edge["out_v"])
        return neighbors

    # ------------------------------------------------------------------
    # Algorithms
    # ------------------------------------------------------------------

    def all_shortest_paths(
        self, source_id: str, target_id: str, max_paths: int = 5
    ) -> list[list[str]]:
        """Find all shortest paths between two canonical_ids using modified BFS.

        Returns up to *max_paths* paths, each a list of canonical_ids from
        source to target inclusive.
        """
        source = self._store.get_vertex_by_canonical_id(source_id)
        target = self._store.get_vertex_by_canonical_id(target_id)
        if source is None or target is None:
            return []

        src_vid = source["vid"]
        tgt_vid = target["vid"]

        if src_vid == tgt_vid:
            return [[source_id]]

        # BFS keeping all shortest predecessors
        dist: dict[str, int] = {src_vid: 0}
        predecessors: dict[str, list[str]] = defaultdict(list)
        queue: deque[str] = deque([src_vid])
        found_depth: int | None = None

        while queue:
            current = queue.popleft()
            d = dist[current]

            if found_depth is not None and d >= found_depth:
                continue

            for nbr_vid in self._neighbor_vids(current):
                if nbr_vid not in dist:
                    dist[nbr_vid] = d + 1
                    predecessors[nbr_vid].append(current)
                    queue.append(nbr_vid)
                    if nbr_vid == tgt_vid:
                        found_depth = d + 1
                elif dist[nbr_vid] == d + 1:
                    predecessors[nbr_vid].append(current)

        if tgt_vid not in dist:
            return []

        # Reconstruct paths via backtracking from target
        paths: list[list[str]] = []

        def _backtrack(node: str, path: list[str]) -> None:
            if len(paths) >= max_paths:
                return
            if node == src_vid:
                cid_path = []
                for vid in reversed(path):
                    cid = self._vid_to_cid(vid)
                    if cid is not None:
                        cid_path.append(cid)
                if cid_path:
                    paths.append(cid_path)
                return
            for pred in predecessors[node]:
                if len(paths) >= max_paths:
                    return
                _backtrack(pred, path + [pred])

        _backtrack(tgt_vid, [tgt_vid])
        return paths

    def k_shortest_paths(
        self, source_id: str, target_id: str, k: int = 5
    ) -> list[list[str]]:
        """Find k shortest paths using Yen's algorithm variant.

        Returns up to *k* simple paths (no repeated vertices) ordered
        by length, each a list of canonical_ids.
        """
        source = self._store.get_vertex_by_canonical_id(source_id)
        target = self._store.get_vertex_by_canonical_id(target_id)
        if source is None or target is None:
            return []

        src_vid = source["vid"]
        tgt_vid = target["vid"]

        if src_vid == tgt_vid:
            return [[source_id]]

        # Find the first shortest path with BFS
        first_path = self._bfs_path(src_vid, tgt_vid, excluded_edges=set(), excluded_nodes=set())
        if first_path is None:
            return []

        A: list[list[str]] = [first_path]  # confirmed shortest paths (vid lists)
        B: list[tuple[int, int, list[str]]] = []  # candidate pool (length, tiebreak, vid_path)
        tiebreak = 0

        for ki in range(1, k):
            prev_path = A[ki - 1]
            for i in range(len(prev_path) - 1):
                spur_node = prev_path[i]
                root_path = prev_path[: i + 1]

                excluded_edges: set[tuple[str, str]] = set()
                for path in A:
                    if path[: i + 1] == root_path and len(path) > i + 1:
                        excluded_edges.add((path[i], path[i + 1]))

                excluded_nodes = set(root_path[:-1])

                spur_path = self._bfs_path(spur_node, tgt_vid, excluded_edges, excluded_nodes)
                if spur_path is not None:
                    total_path = root_path[:-1] + spur_path
                    if total_path not in A:
                        tiebreak += 1
                        heapq.heappush(B, (len(total_path), tiebreak, total_path))

            if not B:
                break
            _, _, best = heapq.heappop(B)
            A.append(best)

        # Convert vid paths to canonical_id paths
        result: list[list[str]] = []
        for vid_path in A:
            cid_path = []
            for vid in vid_path:
                cid = self._vid_to_cid(vid)
                if cid is not None:
                    cid_path.append(cid)
            if cid_path:
                result.append(cid_path)

        return result

    def _bfs_path(
        self,
        src_vid: str,
        tgt_vid: str,
        excluded_edges: set[tuple[str, str]],
        excluded_nodes: set[str],
    ) -> list[str] | None:
        """BFS shortest path avoiding excluded edges and nodes."""
        if src_vid in excluded_nodes:
            return None
        visited: set[str] = {src_vid} | excluded_nodes
        queue: deque[tuple[str, list[str]]] = deque([(src_vid, [src_vid])])

        while queue:
            current, path = queue.popleft()
            for nbr_vid in self._neighbor_vids(current):
                if nbr_vid in visited:
                    continue
                if (current, nbr_vid) in excluded_edges:
                    continue
                new_path = path + [nbr_vid]
                if nbr_vid == tgt_vid:
                    return new_path
                visited.add(nbr_vid)
                queue.append((nbr_vid, new_path))

        return None
