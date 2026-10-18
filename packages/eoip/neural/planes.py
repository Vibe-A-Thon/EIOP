"""Graph Planes and Graph Levels mapping (CRA-044.2).

Maps the four graph levels (GL0-GL3 + GLT) of the neural fabric onto the
canonical graph planes (planes 1, 2, 3, 7, 8):
- GL0 (instance graph) -> Plane 1 (Raw/Extracted) and Plane 2 (Entity/Resolved)
- GL1 (meta-graph) -> Plane 3 (Schema/Ontology)
- GL2 (living brain) -> Plane 2 across sources (cross-source unified graph)
- GL3 (enterprise ontology) -> Plane 3 axioms and SHACL shapes
- GLT (temporal axis) -> Plane 7 (Bitemporal/Intervals)
- Learned Embeddings -> Plane 8 (Tenant-partitioned rebuildable projections)

Enforces policy-epoch-bound snapshots and strictly prohibits a parallel
temporal store duplicating plane 2.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from eoip.contracts.canonical import TrustedScope


class GraphPlane(str, Enum):
    PLANE_1_RAW = "plane_1_raw"
    PLANE_2_ENTITY = "plane_2_entity"
    PLANE_3_ONTOLOGY = "plane_3_ontology"
    PLANE_7_TEMPORAL = "plane_7_temporal"
    PLANE_8_EMBEDDING = "plane_8_embedding"


class GraphLevel(str, Enum):
    GL0_INSTANCE = "GL0"
    GL1_METAGRAPH = "GL1"
    GL2_LIVING_BRAIN = "GL2"
    GL3_ONTOLOGY = "GL3"
    GLT_TEMPORAL = "GLT"


GRAPH_LEVEL_TO_PLANES: dict[GraphLevel, list[GraphPlane]] = {
    GraphLevel.GL0_INSTANCE: [GraphPlane.PLANE_1_RAW, GraphPlane.PLANE_2_ENTITY],
    GraphLevel.GL1_METAGRAPH: [GraphPlane.PLANE_3_ONTOLOGY],
    GraphLevel.GL2_LIVING_BRAIN: [GraphPlane.PLANE_2_ENTITY],
    GraphLevel.GL3_ONTOLOGY: [GraphPlane.PLANE_3_ONTOLOGY],
    GraphLevel.GLT_TEMPORAL: [GraphPlane.PLANE_7_TEMPORAL],
}


class ParallelTemporalStoreProhibitedError(RuntimeError):
    """Raised when an attempt is made to instantiate a parallel temporal store duplicating plane 2."""
    pass


@dataclass
class EpochBoundSnapshot:
    """Content-addressed snapshot bound to a specific policy epoch and tenant scope."""
    snapshot_id: str
    policy_epoch: str
    scope: TrustedScope
    graph_level: GraphLevel
    assigned_planes: list[GraphPlane]
    created_at_epoch_s: float
    triples_or_edges: list[dict[str, Any]] = field(default_factory=list)

    @property
    def digest(self) -> str:
        h = hashlib.sha256(self.snapshot_id.encode())
        h.update(self.policy_epoch.encode())
        h.update(self.graph_level.value.encode())
        return h.hexdigest()


class GraphPlaneCoordinator:
    """Coordinates neural model access across graph levels and planes."""

    def __init__(self) -> None:
        self._registered_temporal_stores: set[str] = set()

    def map_level_to_planes(self, level: GraphLevel) -> list[GraphPlane]:
        return list(GRAPH_LEVEL_TO_PLANES[level])

    def register_temporal_backend(self, backend_id: str, duplicates_plane_2: bool = False) -> None:
        """Register a temporal backend. Strictly prohibits parallel stores duplicating plane 2."""
        if duplicates_plane_2:
            raise ParallelTemporalStoreProhibitedError(
                f"Temporal backend '{backend_id}' duplicates Plane 2 entity graph. "
                "Per CRA-044.2, parallel temporal stores duplicating plane 2 are strictly prohibited; "
                "temporal axis GLT must map directly to Plane 7."
            )
        self._registered_temporal_stores.add(backend_id)

    def create_epoch_bound_snapshot(
        self,
        snapshot_id: str,
        level: GraphLevel,
        policy_epoch: str,
        scope: TrustedScope,
        data: list[dict[str, Any]],
    ) -> EpochBoundSnapshot:
        planes = self.map_level_to_planes(level)
        return EpochBoundSnapshot(
            snapshot_id=snapshot_id,
            policy_epoch=policy_epoch,
            scope=scope,
            graph_level=level,
            assigned_planes=planes,
            created_at_epoch_s=time.time(),
            triples_or_edges=data,
        )
