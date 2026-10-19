"""
Neural Schema Multi-Plane Graph Projection (NS-P5, T-NS-009).
Connects Neural Schemas across Graph Planes:
- Plane GL0: Observation Blobs & Raw Records
- Plane GL1: Knowledge Graph Entities & Boundaries
- Plane GL2: Meta-Graph Templates & Cognitive Schemas
- Plane GW:  Wisdom Graph Architectural Archetypes
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from packages.eoip.neural.schemas.models import NeuralSchema
from reva.core.ids import entity_id


@dataclass
class ProjectedPlaneVertex:
    id: str
    plane: str  # "GL0", "GL1", "GL2", "GL3", "GW"
    kind: str
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProjectedPlaneEdge:
    source_id: str
    target_id: str
    relation: str
    source_plane: str
    target_plane: str


class GraphPlanesProjector:
    """
    Projects schemas and instances across KnowGridFlow (KGF) multi-plane graph architecture.
    """

    def __init__(self, tenant_id: str = "default") -> None:
        self.tenant_id = tenant_id

    def project_schema_to_gl2(self, schema: NeuralSchema) -> ProjectedPlaneVertex:
        """Projects schema definition into Meta-Graph Plane GL2."""
        return ProjectedPlaneVertex(
            id=schema.schema_id,
            plane="GL2",
            kind="meta_SchemaTemplate",
            properties={
                "name": schema.name,
                "domain": schema.domain,
                "slots_count": len(schema.slots),
                "warrant_ref": schema.warrant_ref,
            },
        )

    def project_instance(
        self,
        schema: NeuralSchema,
        instance_data: Dict[str, Any],
        logical_key: str,
        blob_hash: Optional[str] = None,
        governing_decision_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Projects an entity instance across planes GL0, GL1, GL2, and GW.
        """
        vertices: List[ProjectedPlaneVertex] = []
        edges: List[ProjectedPlaneEdge] = []

        ent_id = entity_id(self.tenant_id, schema.name, logical_key)

        # 1. Plane GL1 Entity Vertex
        vertices.append(ProjectedPlaneVertex(
            id=ent_id,
            plane="GL1",
            kind=f"kg_{schema.name}",
            properties={
                **instance_data,
                "epistemic_state": "inferred",
            },
        ))

        # 2. Link GL1 Entity to GL2 Schema via INSTANTIATES_SCHEMA
        edges.append(ProjectedPlaneEdge(
            source_id=ent_id,
            target_id=schema.schema_id,
            relation="INSTANTIATES_SCHEMA",
            source_plane="GL1",
            target_plane="GL2",
        ))

        # 3. Optional Plane GL0 Blob link
        if blob_hash:
            gl0_id = f"blb1_{blob_hash}"
            vertices.append(ProjectedPlaneVertex(
                id=gl0_id,
                plane="GL0",
                kind="raw_Blob",
                properties={"sha256": blob_hash},
            ))
            edges.append(ProjectedPlaneEdge(
                source_id=ent_id,
                target_id=gl0_id,
                relation="DERIVED_FROM_BLOB",
                source_plane="GL1",
                target_plane="GL0",
            ))

        # 4. Optional Plane GW Wisdom Graph link
        if governing_decision_id:
            edges.append(ProjectedPlaneEdge(
                source_id=schema.schema_id,
                target_id=governing_decision_id,
                relation="GOVERNED_BY_DECISION",
                source_plane="GL2",
                target_plane="GW",
            ))

        return {
            "entity_id": ent_id,
            "vertices": [v.__dict__ for v in vertices],
            "edges": [e.__dict__ for e in edges],
        }
