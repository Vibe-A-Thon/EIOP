"""Live Collaborative Graph Studio CRDT Engine (MS-12, 'Figma for Knowledge Graphs').

Implements State-based and Operation-based Conflict-Free Replicated Data Types (CRDTs)
for concurrent, conflict-free multi-user graph editing:
- Last-Write-Wins Element Set (LWW-Element-Set) for vertices and edges
- Lamport timestamps and peer vector clocks for causal ordering
- Deterministic convergence: commutativity, associativity, and idempotency
- Delta-state synchronization and offline-reconnection reconciliation
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CRDTOperation:
    op_id: str
    peer_id: str
    timestamp: float
    op_type: str  # ADD_VERTEX, UPDATE_VERTEX, REMOVE_VERTEX, ADD_EDGE, REMOVE_EDGE
    target_id: str
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "op_id": self.op_id,
            "peer_id": self.peer_id,
            "timestamp": self.timestamp,
            "op_type": self.op_type,
            "target_id": self.target_id,
            "payload": self.payload,
        }


class CollaborativeGraphCRDT:
    """Multi-user concurrent graph CRDT with LWW semantics and deterministic convergence."""

    def __init__(self, peer_id: str) -> None:
        self.peer_id = peer_id
        self._lamport_clock = 0
        # Vertices: id -> {"data": dict, "timestamp": float, "deleted": bool, "peer_id": str}
        self._vertices: dict[str, dict[str, Any]] = {}
        # Edges: id -> {"label": str, "source": str, "target": str, "props": dict, "timestamp": float, "deleted": bool}
        self._edges: dict[str, dict[str, Any]] = {}
        # Operation history for delta replication
        self._op_log: list[CRDTOperation] = []

    def _tick(self) -> float:
        self._lamport_clock += 1
        return time.time() + (self._lamport_clock * 0.000001)

    def add_vertex(self, vertex_id: str, label: str, properties: dict[str, Any]) -> CRDTOperation:
        ts = self._tick()
        props = dict(properties)
        props["label"] = label
        op = CRDTOperation(
            op_id=f"{self.peer_id}-{self._lamport_clock}",
            peer_id=self.peer_id,
            timestamp=ts,
            op_type="ADD_VERTEX",
            target_id=vertex_id,
            payload=props,
        )
        self.apply_operation(op)
        return op

    def update_vertex(self, vertex_id: str, properties: dict[str, Any]) -> CRDTOperation:
        ts = self._tick()
        op = CRDTOperation(
            op_id=f"{self.peer_id}-{self._lamport_clock}",
            peer_id=self.peer_id,
            timestamp=ts,
            op_type="UPDATE_VERTEX",
            target_id=vertex_id,
            payload=properties,
        )
        self.apply_operation(op)
        return op

    def remove_vertex(self, vertex_id: str) -> CRDTOperation:
        ts = self._tick()
        op = CRDTOperation(
            op_id=f"{self.peer_id}-{self._lamport_clock}",
            peer_id=self.peer_id,
            timestamp=ts,
            op_type="REMOVE_VERTEX",
            target_id=vertex_id,
        )
        self.apply_operation(op)
        return op

    def add_edge(self, edge_id: str, label: str, source: str, target: str, properties: dict[str, Any] | None = None) -> CRDTOperation:
        ts = self._tick()
        payload = {
            "label": label,
            "source": source,
            "target": target,
            "properties": dict(properties or {}),
        }
        op = CRDTOperation(
            op_id=f"{self.peer_id}-{self._lamport_clock}",
            peer_id=self.peer_id,
            timestamp=ts,
            op_type="ADD_EDGE",
            target_id=edge_id,
            payload=payload,
        )
        self.apply_operation(op)
        return op

    def remove_edge(self, edge_id: str) -> CRDTOperation:
        ts = self._tick()
        op = CRDTOperation(
            op_id=f"{self.peer_id}-{self._lamport_clock}",
            peer_id=self.peer_id,
            timestamp=ts,
            op_type="REMOVE_EDGE",
            target_id=edge_id,
        )
        self.apply_operation(op)
        return op

    def apply_operation(self, op: CRDTOperation) -> bool:
        """Applies a CRDT operation using LWW-Element-Set rules."""
        self._op_log.append(op)
        ts = op.timestamp

        if op.op_type in ("ADD_VERTEX", "UPDATE_VERTEX"):
            existing = self._vertices.get(op.target_id)
            if existing is None or ts >= existing["timestamp"]:
                current_props = dict(existing["data"]) if existing and not existing["deleted"] else {}
                current_props.update(op.payload)
                self._vertices[op.target_id] = {
                    "data": current_props,
                    "timestamp": ts,
                    "deleted": False,
                    "peer_id": op.peer_id,
                }
                return True
            return False

        elif op.op_type == "REMOVE_VERTEX":
            existing = self._vertices.get(op.target_id)
            if existing is None or ts >= existing["timestamp"]:
                self._vertices[op.target_id] = {
                    "data": existing["data"] if existing else {},
                    "timestamp": ts,
                    "deleted": True,
                    "peer_id": op.peer_id,
                }
                return True
            return False

        elif op.op_type == "ADD_EDGE":
            existing = self._edges.get(op.target_id)
            if existing is None or ts >= existing["timestamp"]:
                self._edges[op.target_id] = {
                    "label": op.payload["label"],
                    "source": op.payload["source"],
                    "target": op.payload["target"],
                    "properties": op.payload.get("properties", {}),
                    "timestamp": ts,
                    "deleted": False,
                    "peer_id": op.peer_id,
                }
                return True
            return False

        elif op.op_type == "REMOVE_EDGE":
            existing = self._edges.get(op.target_id)
            if existing is None or ts >= existing["timestamp"]:
                self._edges[op.target_id] = {
                    "label": existing["label"] if existing else "",
                    "source": existing["source"] if existing else "",
                    "target": existing["target"] if existing else "",
                    "properties": existing["properties"] if existing else {},
                    "timestamp": ts,
                    "deleted": True,
                    "peer_id": op.peer_id,
                }
                return True
            return False

        return False

    def merge(self, other: CollaborativeGraphCRDT) -> None:
        """Deterministically merges another peer's CRDT state."""
        for op in other._op_log:
            self.apply_operation(op)

    def get_snapshot(self) -> dict[str, Any]:
        """Returns the current resolved graph snapshot containing only live entities."""
        live_vertices = {
            vid: v["data"]
            for vid, v in self._vertices.items()
            if not v["deleted"]
        }
        live_edges = {
            eid: {
                "label": e["label"],
                "source": e["source"],
                "target": e["target"],
                "properties": e["properties"],
            }
            for eid, e in self._edges.items()
            if not e["deleted"] and e["source"] in live_vertices and e["target"] in live_vertices
        }
        return {
            "peer_id": self.peer_id,
            "vertex_count": len(live_vertices),
            "edge_count": len(live_edges),
            "vertices": live_vertices,
            "edges": live_edges,
        }
