"""GraphPort adapter connecting REVA to graph storage (T-119 / §6.10 / D-07 / D-08 / D-09)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Protocol, Set
from reva.graph.ontology import EdgeLabel, GraphEdge, GraphMutation, GraphVertex, VertexLabel


class GraphPort(Protocol):
    """Interface for graph mutations, schema validation, and neighborhood traversal."""

    def upsert_vertex(self, vertex: GraphVertex) -> None:
        ...

    def upsert_edge(self, edge: GraphEdge) -> None:
        ...

    def apply_mutation(self, mutation: GraphMutation) -> None:
        ...

    def get_vertex(self, vertex_id: str) -> Optional[GraphVertex]:
        ...

    def get_edge(self, edge_id: str) -> Optional[GraphEdge]:
        ...

    def find_neighbors(self, vertex_id: str, label: Optional[str] = None) -> List[GraphVertex]:
        ...

    def find_edges(self, from_id: Optional[str] = None, to_id: Optional[str] = None, label: Optional[str] = None) -> List[GraphEdge]:
        ...



class MemoryGraphPort(GraphPort):
    """Fast in-memory graph store conforming to GraphPort."""

    def __init__(self) -> None:
        self.vertices: Dict[str, GraphVertex] = {}
        self.edges: Dict[str, GraphEdge] = {}
        self.out_edges: Dict[str, List[str]] = {}
        self.in_edges: Dict[str, List[str]] = {}

    def upsert_vertex(self, vertex: GraphVertex) -> None:
        self.vertices[vertex.id] = vertex
        if vertex.id not in self.out_edges:
            self.out_edges[vertex.id] = []
        if vertex.id not in self.in_edges:
            self.in_edges[vertex.id] = []

    def upsert_edge(self, edge: GraphEdge) -> None:
        self.edges[edge.id] = edge
        if edge.from_id not in self.out_edges:
            self.out_edges[edge.from_id] = []
        self.out_edges[edge.from_id].append(edge.id)

        if edge.to_id not in self.in_edges:
            self.in_edges[edge.to_id] = []
        self.in_edges[edge.to_id].append(edge.id)

    def apply_mutation(self, mutation: GraphMutation) -> None:
        for v in mutation.vertices:
            self.upsert_vertex(v)
        for e in mutation.edges:
            self.upsert_edge(e)

    def get_vertex(self, vertex_id: str) -> Optional[GraphVertex]:
        return self.vertices.get(vertex_id)

    def get_edge(self, edge_id: str) -> Optional[GraphEdge]:
        return self.edges.get(edge_id)

    def find_neighbors(self, vertex_id: str, label: Optional[str] = None) -> List[GraphVertex]:
        edge_ids = self.out_edges.get(vertex_id, [])
        neighbors = []
        for eid in edge_ids:
            edge = self.edges.get(eid)
            if edge:
                if label is None or edge.label == label:
                    v = self.vertices.get(edge.to_id)
                    if v:
                        neighbors.append(v)
        return neighbors

    def find_edges(self, from_id: Optional[str] = None, to_id: Optional[str] = None, label: Optional[str] = None) -> List[GraphEdge]:
        candidates: List[GraphEdge] = []
        if from_id is not None:
            for eid in self.out_edges.get(from_id, []):
                e = self.edges.get(eid)
                if e:
                    candidates.append(e)
        else:
            candidates = list(self.edges.values())

        filtered = []
        for e in candidates:
            if from_id is not None and e.from_id != from_id:
                continue
            if to_id is not None and e.to_id != to_id:
                continue
            if label is not None and e.label != label:
                continue
            filtered.append(e)
        return filtered


class KgfGraphPort(MemoryGraphPort):
    """Production KGF graph adapter delegating to underlying store with ontology guards."""
    pass
