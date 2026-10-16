"""Bounded, allowlisted graph path and impact traversal."""

from __future__ import annotations

from collections import deque
from math import isfinite
from time import monotonic
from typing import Literal

from eoip.graph.store import Edge, GraphQueryTimeout, GraphStore, graph_query_deadline

Direction = Literal["outgoing", "incoming", "both"]


def _path_evidence_count(edges: list[Edge]) -> int:
    return sum(
        1
        for edge in edges
        if edge["properties"].get("source_ref") or edge["properties"].get("evidence_key")
    )


def impact_rationale(item: dict) -> str:
    """Deterministic 'why included' summary for one impacted item."""
    edges = item["path"]["edges"]
    labels = sorted({edge["label"] for edge in edges})
    evidence = _path_evidence_count(edges)
    return f"{len(edges)} hop(s) via {', '.join(labels)}; evidence: {evidence} source ref(s)"


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
        timeout_seconds: float = 20.0,
    ) -> None:
        if max_depth < 1 or max_results < 1:
            raise ValueError("max_depth and max_results must be positive")
        if not isfinite(timeout_seconds) or timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be a positive finite number")
        self._store = store
        self._allowed_edges = allowed_edges
        self._max_depth = max_depth
        self._max_results = max_results
        self._max_visited = 1000
        self._timeout = timeout_seconds

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
        deadline = monotonic() + self._timeout
        with graph_query_deadline(deadline):
            source = self._store.get_vertex_by_canonical_id(source_id)
        self._check_deadline(deadline)
        with graph_query_deadline(deadline):
            target = self._store.get_vertex_by_canonical_id(target_id)
        self._check_deadline(deadline)
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
        while queue:
            self._check_deadline(deadline)
            if len(visited) >= self._max_visited:
                raise ValueError("Path query exceeded the traversal budget; narrow the endpoints or depth")
            current_id, vertices, edges = queue.popleft()
            if len(edges) >= depth_limit:
                continue
            for edge, neighbor_id in self._neighbors(current_id, direction, deadline):
                self._check_deadline(deadline)
                if neighbor_id in visited:
                    continue
                with graph_query_deadline(deadline):
                    neighbor = self._store.get_vertex(neighbor_id)
                self._check_deadline(deadline)
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
        deadline = monotonic() + self._timeout
        try:
            with graph_query_deadline(deadline):
                source = self._store.get_vertex_by_canonical_id(canonical_id)
            self._check_deadline(deadline)
        except GraphQueryTimeout:
            return {"source": None, "impacted": [], "truncated": True}
        if source is None or source["properties"].get("deleted_at"):
            return {"source": None, "impacted": [], "truncated": False}

        queue = deque([(source["vid"], [source], [])])
        visited = {source["vid"]}
        impacted = []
        truncated = False
        while queue:
            try:
                self._check_deadline(deadline)
            except GraphQueryTimeout:
                return self._finalize_impact(source, impacted, True)
            if len(visited) >= self._max_visited:
                return self._finalize_impact(source, impacted, True)
            current_id, vertices, edges = queue.popleft()
            if len(edges) >= depth_limit:
                try:
                    neighbors = self._neighbors(current_id, direction, deadline)
                except GraphQueryTimeout:
                    return self._finalize_impact(source, impacted, True)
                if any(neighbor_id not in visited for _, neighbor_id in neighbors):
                    truncated = True
                continue
            try:
                neighbors = self._neighbors(current_id, direction, deadline)
            except GraphQueryTimeout:
                return self._finalize_impact(source, impacted, True)
            for edge, neighbor_id in neighbors:
                try:
                    self._check_deadline(deadline)
                except GraphQueryTimeout:
                    return self._finalize_impact(source, impacted, True)
                if neighbor_id in visited:
                    continue
                try:
                    with graph_query_deadline(deadline):
                        neighbor = self._store.get_vertex(neighbor_id)
                    self._check_deadline(deadline)
                except GraphQueryTimeout:
                    return self._finalize_impact(source, impacted, True)
                if neighbor is None or neighbor["properties"].get("deleted_at"):
                    continue
                visited.add(neighbor_id)
                next_vertices = [*vertices, neighbor]
                next_edges = [*edges, edge]
                impacted.append(
                    {"vertex": neighbor, "path": {"vertices": next_vertices, "edges": next_edges}}
                )
                queue.append((neighbor_id, next_vertices, next_edges))
        return self._finalize_impact(source, impacted, truncated)

    def _finalize_impact(self, source: dict, impacted: list[dict], truncated: bool) -> dict:
        """Annotate rationale, then keep the most relevant items under the cap."""
        for item in impacted:
            item["rationale"] = impact_rationale(item)
        impacted.sort(
            key=lambda item: (
                len(item["path"]["edges"]),
                -_path_evidence_count(item["path"]["edges"]),
            )
        )
        if len(impacted) > self._max_results:
            truncated = True
            impacted = impacted[: self._max_results]
        return {"source": source, "impacted": impacted, "truncated": truncated}

    def _depth_limit(self, requested: int | None) -> int:
        if requested is None:
            return self._max_depth
        if requested < 1 or requested > self._max_depth:
            raise ValueError(f"max_depth must be between 1 and {self._max_depth}")
        return requested

    def _check_deadline(self, deadline: float) -> None:
        if monotonic() >= deadline:
            raise GraphQueryTimeout("Traversal query exceeded the traversal budget")

    def _neighbors(
        self,
        vid: str,
        direction: Direction,
        deadline: float,
    ) -> list[tuple[Edge, str]]:
        neighbors: list[tuple[Edge, str]] = []
        labels = list(self._allowed_edges)
        if direction in {"outgoing", "both"}:
            self._check_deadline(deadline)
            with graph_query_deadline(deadline):
                outgoing = self._store.edges_from(vid, labels=labels)
            self._check_deadline(deadline)
            neighbors.extend((edge, edge["in_v"]) for edge in outgoing)
        if direction in {"incoming", "both"}:
            self._check_deadline(deadline)
            with graph_query_deadline(deadline):
                incoming = self._store.edges_to(vid, labels=labels)
            self._check_deadline(deadline)
            neighbors.extend((edge, edge["out_v"]) for edge in incoming)
        return neighbors
