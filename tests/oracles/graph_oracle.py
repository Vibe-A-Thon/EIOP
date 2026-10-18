"""Independent reference oracles that never import production code (CRA-037.2)."""

from __future__ import annotations

from collections import deque
from typing import Any


class ReferenceGraphOracle:
    """Pure-Python reference graph model with zero production code dependencies."""

    def __init__(self) -> None:
        self.nodes: dict[str, dict[str, Any]] = {}
        self.adj: dict[str, list[str]] = {}

    def add_node(self, node_id: str, properties: dict[str, Any] | None = None) -> None:
        self.nodes[node_id] = properties or {}
        self.adj.setdefault(node_id, [])

    def add_edge(self, source_id: str, target_id: str) -> None:
        self.add_node(source_id)
        self.add_node(target_id)
        self.adj[source_id].append(target_id)

    def shortest_path(self, start_id: str, target_id: str, max_depth: int = 8) -> list[str] | None:
        if start_id not in self.nodes or target_id not in self.nodes:
            return None
        if start_id == target_id:
            return [start_id]

        queue = deque([(start_id, [start_id])])
        visited = {start_id}

        while queue:
            current, path = queue.popleft()
            if len(path) - 1 >= max_depth:
                continue
            for neighbor in self.adj.get(current, []):
                if neighbor == target_id:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    def neighborhood(self, node_id: str, max_depth: int = 1) -> set[str]:
        if node_id not in self.nodes:
            return set()
        visited = {node_id}
        frontier = {node_id}

        for _ in range(max_depth):
            next_frontier = set()
            for current in frontier:
                for nbr in self.adj.get(current, []):
                    if nbr not in visited:
                        visited.add(nbr)
                        next_frontier.add(nbr)
            frontier = next_frontier
        return visited - {node_id}
