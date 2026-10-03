"""What-if simulation engine: simulate entity removal/isolation without mutation."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any

from eoip.graph.store import GraphStore


@dataclass
class WhatIfResult:
    canonical_id: str
    action: str
    broken_edges: int = 0
    affected_neighbors: int = 0
    orphaned_entities: int = 0
    broken_paths: int = 0
    centrality_changes: list[dict[str, Any]] = field(default_factory=list)
    component_split: bool = False
    new_components: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "canonical_id": self.canonical_id,
            "action": self.action,
            "broken_edges": self.broken_edges,
            "affected_neighbors": self.affected_neighbors,
            "orphaned_entities": self.orphaned_entities,
            "broken_paths": self.broken_paths,
            "centrality_changes": self.centrality_changes,
            "component_split": self.component_split,
            "new_components": self.new_components,
        }


class WhatIfEngine:
    def __init__(self, store: GraphStore) -> None:
        self._store = store

    def simulate_removal(self, canonical_id: str) -> WhatIfResult:
        root = self._store.get_vertex_by_canonical_id(canonical_id)
        if root is None:
            return WhatIfResult(canonical_id=canonical_id, action="remove")

        out_edges = self._store.edges_from(root["vid"])
        in_edges = self._store.edges_to(root["vid"])
        broken_edges = len(out_edges) + len(in_edges)

        neighbors: set[str] = set()
        neighbor_vids: set[str] = set()
        for edge in out_edges:
            v = self._store.get_vertex(edge["in_v"])
            if v:
                neighbors.add(v["properties"]["canonical_id"])
                neighbor_vids.add(edge["in_v"])
        for edge in in_edges:
            v = self._store.get_vertex(edge["out_v"])
            if v:
                neighbors.add(v["properties"]["canonical_id"])
                neighbor_vids.add(edge["out_v"])

        orphaned = 0
        for vid in neighbor_vids:
            other_out = [e for e in self._store.edges_from(vid) if e["in_v"] != root["vid"]]
            other_in = [e for e in self._store.edges_to(vid) if e["out_v"] != root["vid"]]
            if not other_out and not other_in:
                orphaned += 1

        broken_paths = self._count_broken_paths(root["vid"], neighbor_vids)
        component_split, new_components = self._check_component_split(
            root["vid"], neighbor_vids
        )

        centrality_changes = self._compute_centrality_changes(
            canonical_id, neighbors
        )

        return WhatIfResult(
            canonical_id=canonical_id,
            action="remove",
            broken_edges=broken_edges,
            affected_neighbors=len(neighbors),
            orphaned_entities=orphaned,
            broken_paths=broken_paths,
            centrality_changes=centrality_changes,
            component_split=component_split,
            new_components=new_components,
        )

    def simulate_isolation(self, canonical_id: str) -> WhatIfResult:
        root = self._store.get_vertex_by_canonical_id(canonical_id)
        if root is None:
            return WhatIfResult(canonical_id=canonical_id, action="isolate")

        out_edges = self._store.edges_from(root["vid"])
        in_edges = self._store.edges_to(root["vid"])

        neighbors: set[str] = set()
        for edge in out_edges:
            v = self._store.get_vertex(edge["in_v"])
            if v:
                neighbors.add(v["properties"]["canonical_id"])
        for edge in in_edges:
            v = self._store.get_vertex(edge["out_v"])
            if v:
                neighbors.add(v["properties"]["canonical_id"])

        return WhatIfResult(
            canonical_id=canonical_id,
            action="isolate",
            broken_edges=len(out_edges) + len(in_edges),
            affected_neighbors=len(neighbors),
            orphaned_entities=0,
            broken_paths=0,
            component_split=False,
            new_components=0,
        )

    def _count_broken_paths(self, removed_vid: str, neighbor_vids: set[str]) -> int:
        count = 0
        vid_list = list(neighbor_vids)
        for i in range(len(vid_list)):
            for j in range(i + 1, len(vid_list)):
                a, b = vid_list[i], vid_list[j]
                if self._path_through(a, b, removed_vid):
                    count += 1
        return count

    def _path_through(self, src_vid: str, tgt_vid: str, through_vid: str) -> bool:
        visited: set[str] = {through_vid}
        queue = deque([src_vid])
        visited.add(src_vid)
        while queue:
            vid = queue.popleft()
            if vid == tgt_vid:
                return False
            for edge in self._store.edges_from(vid):
                next_vid = edge["in_v"]
                if next_vid not in visited:
                    visited.add(next_vid)
                    queue.append(next_vid)
            for edge in self._store.edges_to(vid):
                next_vid = edge["out_v"]
                if next_vid not in visited:
                    visited.add(next_vid)
                    queue.append(next_vid)
        return True

    def _check_component_split(
        self, removed_vid: str, neighbor_vids: set[str]
    ) -> tuple[bool, int]:
        if len(neighbor_vids) < 2:
            return False, 0
        start = next(iter(neighbor_vids))
        visited: set[str] = {removed_vid, start}
        queue = deque([start])
        while queue:
            vid = queue.popleft()
            for edge in self._store.edges_from(vid):
                nxt = edge["in_v"]
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
            for edge in self._store.edges_to(vid):
                nxt = edge["out_v"]
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
        unreachable = neighbor_vids - visited
        if unreachable:
            return True, 2
        return False, 0

    def _compute_centrality_changes(
        self, removed_cid: str, neighbors: set[str]
    ) -> list[dict[str, Any]]:
        if not neighbors:
            return []
        from eoip.graph.metrics import GraphMetricsEngine
        engine = GraphMetricsEngine(self._store)
        before = engine.centrality(list(neighbors))
        changes = []
        for cid, metrics in before.items():
            changes.append({
                "canonical_id": cid,
                "degree_before": metrics.degree,
                "degree_after": max(0, metrics.degree - 1),
            })
        return changes
