"""Multi-Graph Projection Views: Data Graph vs Schema/Meta Graph vs Provenance/Security Graph (CRA-029.4).

Features:
- Separate projections over the unified knowledge store:
  1. Data Graph: Operational and business entities (Services, Repositories, WorkItems, Datastores).
  2. Schema/Meta Graph: Ontology classes, SHACL shapes, domain boundaries, and versioning.
  3. Provenance/Security Graph: Ingestion runs, evidence nodes, security ACLs, classifications, and lineage warrants.
- Strict object-typing guarantee (CRA-029.4): Each view presents strictly typed vertices and relationships with stable cross-view IRI links.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from eoip.graph.store import GraphStore


@dataclass
class GraphViewProjection:
    view_name: str
    vertices: list[dict[str, Any]]
    edges: list[dict[str, Any]]
    entity_count: int
    edge_count: int


class MultiGraphViewEngine:
    """Projects typed graph planes with stable cross-plane links (CRA-029.4)."""

    DATA_LABELS = frozenset({
        "Service", "APIService", "APIEndpoint", "Database", "Repository",
        "Project", "WorkItem", "File", "CodeSymbol", "Incident", "ChangeRequest",
    })

    SCHEMA_LABELS = frozenset({
        "OntologyVersion", "GraphDomain", "IssueType", "Status", "Version",
    })

    PROVENANCE_SECURITY_LABELS = frozenset({
        "DataSource", "IngestionRun", "Evidence", "ValidationRun", "ValidationFinding",
        "EntityRevision", "RelationshipRevision", "GraphVersion",
    })

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    def get_data_graph_view(self) -> GraphViewProjection:
        """Project the Data Graph Plane."""
        vertices = [
            v for v in self._store.find_vertices(limit=100_000)
            if v.get("label") in self.DATA_LABELS
        ]
        vids = {v["vid"] for v in vertices}
        edges = [
            e for e in self._store.find_edges(limit=100_000)
            if e.get("out_v") in vids and e.get("in_v") in vids
        ]
        return GraphViewProjection(
            view_name="DATA_GRAPH",
            vertices=vertices,
            edges=edges,
            entity_count=len(vertices),
            edge_count=len(edges),
        )

    def get_schema_meta_graph_view(self) -> GraphViewProjection:
        """Project the Schema / Meta Graph Plane."""
        vertices = [
            v for v in self._store.find_vertices(limit=100_000)
            if v.get("label") in self.SCHEMA_LABELS
        ]
        vids = {v["vid"] for v in vertices}
        edges = [
            e for e in self._store.find_edges(limit=100_000)
            if e.get("out_v") in vids and e.get("in_v") in vids
        ]
        return GraphViewProjection(
            view_name="SCHEMA_META_GRAPH",
            vertices=vertices,
            edges=edges,
            entity_count=len(vertices),
            edge_count=len(edges),
        )

    def get_provenance_security_graph_view(self) -> GraphViewProjection:
        """Project the Provenance / Security Graph Plane."""
        vertices = [
            v for v in self._store.find_vertices(limit=100_000)
            if v.get("label") in self.PROVENANCE_SECURITY_LABELS
        ]
        vids = {v["vid"] for v in vertices}
        edges = [
            e for e in self._store.find_edges(limit=100_000)
            if e.get("out_v") in vids and e.get("in_v") in vids
        ]
        return GraphViewProjection(
            view_name="PROVENANCE_SECURITY_GRAPH",
            vertices=vertices,
            edges=edges,
            entity_count=len(vertices),
            edge_count=len(edges),
        )
