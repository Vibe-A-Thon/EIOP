"""Bounded, allowlisted graph path and impact traversal."""

from __future__ import annotations

from collections import deque
from time import monotonic
from typing import Literal

from eoip.graph.store import Edge, GraphStore

Direction = Literal["outgoing", "incoming", "both"]

DEFAULT_TRAVERSAL_EDGES = frozenset(
    {
        "CONTAINS",
        "HAS_BRANCH",
        "HAS_COMMIT",
        "HAS_MERGE_REQUEST",
        "MODIFIES",
        "DECLARES",
        "CALLS",
        "IMPORTS",
        "DEPENDS_ON",
        "IMPLEMENTS",
        "REFERENCES",
        "DOCUMENTS",
        "PRODUCED_BY",
    }
)


class GraphTraversal:
    def __init__(
        self,
        store: GraphStore,
        allowed_edges: frozenset[str] = DEFAULT_TRAVERSAL_EDGES,
        max_depth: int = 8,
        max_results: int = 100,
    ) -> None:
        if max_depth < 1 or max_results < 1:
            raise ValueError("max_depth and max_results must be positive")
        self._store = store
        self._allowed_edges = allowed_edges
        self._max_depth = max_depth
        self._max_results = max_results
        self._max_visited = 1000
        self._timeout = 20

    def find_path(
        self,
        source_id: str,
        target_id: str,
        *,
        max_depth: int | None = None,
        direction: Direction = "both",
    ) -> dict | None:
        """Return the shortest path, including ordered vertices and edges."""
        if direction not in {"outgoing", "incoming", "both"}:
            raise ValueError("direction must be outgoing, incoming, or both")
        depth_limit = self._depth_limit(max_depth)
        source = self._store.get_vertex_by_canonical_id(source_id)
        target = self._store.get_vertex_by_canonical_id(target_id)
        if (
            source is None
            or target is None
            or source["properties"].get("deleted_at")
            or target["properties"].get("deleted_at")
        ):
            return None
        if source["vid"] == target["vid"]:
            return {"vertices": [source], "edges": []}

        queue = deque([(source["vid"], [source], [])])
        visited = {source["vid"]}
        deadline = monotonic() + self._timeout
        while queue:
            if len(visited) >= self._max_visited or monotonic() > deadline:
                raise ValueError("Path query exceeded the traversal budget; narrow the endpoints or depth")
            current_id, vertices, edges = queue.popleft()
            if len(edges) >= depth_limit:
                continue
            for edge, neighbor_id in self._neighbors(current_id, direction):
                if neighbor_id in visited:
                    continue
                neighbor = self._store.get_vertex(neighbor_id)
                if neighbor is None or neighbor["properties"].get("deleted_at"):
                    continue
                next_vertices = [*vertices, neighbor]
                next_edges = [*edges, edge]
                if neighbor_id == target["vid"]:
                    return {"vertices": next_vertices, "edges": next_edges}
                visited.add(neighbor_id)
                queue.append((neighbor_id, next_vertices, next_edges))
        return None

    def impact(
        self,
        canonical_id: str,
        *,
        max_depth: int | None = None,
        direction: Direction = "both",
    ) -> dict:
        """Return bounded reachable entities and their shortest paths."""
        if direction not in {"outgoing", "incoming", "both"}:
            raise ValueError("direction must be outgoing, incoming, or both")
        depth_limit = self._depth_limit(max_depth)
        source = self._store.get_vertex_by_canonical_id(canonical_id)
        if source is None or source["properties"].get("deleted_at"):
            return {"source": None, "impacted": [], "truncated": False}

        queue = deque([(source["vid"], [source], [])])
        visited = {source["vid"]}
        impacted = []
        truncated = False
        deadline = monotonic() + self._timeout
        while queue:
            if len(visited) >= self._max_visited or monotonic() > deadline:
                return {"source": source, "impacted": impacted, "truncated": True}
            current_id, vertices, edges = queue.popleft()
            if len(edges) >= depth_limit:
                if any(
                    neighbor_id not in visited for _, neighbor_id in self._neighbors(current_id, direction)
                ):
                    truncated = True
                continue
            for edge, neighbor_id in self._neighbors(current_id, direction):
                if neighbor_id in visited:
                    continue
                neighbor = self._store.get_vertex(neighbor_id)
                if neighbor is None or neighbor["properties"].get("deleted_at"):
                    continue
                if len(impacted) >= self._max_results:
                    truncated = True
                    return {"source": source, "impacted": impacted, "truncated": truncated}
                visited.add(neighbor_id)
                next_vertices = [*vertices, neighbor]
                next_edges = [*edges, edge]
                impacted.append(
                    {"vertex": neighbor, "path": {"vertices": next_vertices, "edges": next_edges}}
                )
                queue.append((neighbor_id, next_vertices, next_edges))
        return {"source": source, "impacted": impacted, "truncated": truncated}

    def _depth_limit(self, requested: int | None) -> int:
        if requested is None:
            return self._max_depth
        if requested < 1 or requested > self._max_depth:
            raise ValueError(f"max_depth must be between 1 and {self._max_depth}")
        return requested

    def _neighbors(self, vid: str, direction: Direction) -> list[tuple[Edge, str]]:
        neighbors: list[tuple[Edge, str]] = []
        labels = list(self._allowed_edges)
        if direction in {"outgoing", "both"}:
            neighbors.extend((edge, edge["in_v"]) for edge in self._store.edges_from(vid, labels=labels))
        if direction in {"incoming", "both"}:
            neighbors.extend((edge, edge["out_v"]) for edge in self._store.edges_to(vid, labels=labels))
        return neighbors
