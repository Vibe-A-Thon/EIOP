"""Edge deployment runtime — offline-capable graph query and sync protocol.

Provides EdgeNode registration, delta-based sync protocol between edge
and cloud, offline query execution against a local snapshot, and
edge-to-cloud entity promotion for locally discovered knowledge.
"""

from __future__ import annotations

import hashlib
import threading
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EdgeNodeStatus(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    SYNCING = "SYNCING"
    DEGRADED = "DEGRADED"
    DECOMMISSIONED = "DECOMMISSIONED"


class SyncDirection(str, Enum):
    CLOUD_TO_EDGE = "CLOUD_TO_EDGE"
    EDGE_TO_CLOUD = "EDGE_TO_CLOUD"
    BIDIRECTIONAL = "BIDIRECTIONAL"


@dataclass
class SyncDelta:
    entity_id: str
    operation: str  # INSERT, UPDATE, DELETE
    payload: dict[str, Any]
    version: int
    timestamp: float = field(default_factory=time.time)
    checksum: str = ""

    def __post_init__(self) -> None:
        if not self.checksum:
            raw = f"{self.entity_id}:{self.operation}:{self.version}"
            self.checksum = hashlib.sha256(raw.encode()).hexdigest()[:16]


@dataclass
class SyncResult:
    sync_id: str
    node_id: str
    direction: SyncDirection
    deltas_sent: int = 0
    deltas_received: int = 0
    conflicts: int = 0
    resolved: int = 0
    duration_ms: float = 0.0
    timestamp: float = field(default_factory=time.time)
    success: bool = True
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "sync_id": self.sync_id,
            "node_id": self.node_id,
            "direction": self.direction.value,
            "deltas_sent": self.deltas_sent,
            "deltas_received": self.deltas_received,
            "conflicts": self.conflicts,
            "resolved": self.resolved,
            "duration_ms": round(self.duration_ms, 2),
            "success": self.success,
            "error": self.error,
        }


@dataclass
class EdgeNode:
    node_id: str
    name: str
    region: str
    status: EdgeNodeStatus = EdgeNodeStatus.OFFLINE
    sync_direction: SyncDirection = SyncDirection.BIDIRECTIONAL
    last_sync: float | None = None
    sync_interval_seconds: int = 300
    local_entity_count: int = 0
    version_vector: dict[str, int] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)

    def is_sync_due(self) -> bool:
        if self.status in (EdgeNodeStatus.DECOMMISSIONED, EdgeNodeStatus.SYNCING):
            return False
        if self.last_sync is None:
            return True
        return (time.time() - self.last_sync) >= self.sync_interval_seconds

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "name": self.name,
            "region": self.region,
            "status": self.status.value,
            "sync_direction": self.sync_direction.value,
            "last_sync": self.last_sync,
            "sync_interval_seconds": self.sync_interval_seconds,
            "local_entity_count": self.local_entity_count,
            "version_vector": dict(self.version_vector),
            "tags": list(self.tags),
        }


class OfflineQueryEngine:
    """Executes queries against a local entity snapshot when cloud is unavailable."""

    def __init__(self) -> None:
        self._snapshot: dict[str, dict[str, Any]] = {}
        self._snapshot_version: int = 0
        self._snapshot_time: float | None = None

    def load_snapshot(self, entities: dict[str, dict[str, Any]]) -> None:
        self._snapshot = dict(entities)
        self._snapshot_version += 1
        self._snapshot_time = time.time()

    def apply_deltas(self, deltas: list[SyncDelta]) -> int:
        applied = 0
        for d in sorted(deltas, key=lambda x: x.version):
            if d.operation == "DELETE":
                if d.entity_id in self._snapshot:
                    del self._snapshot[d.entity_id]
                    applied += 1
            elif d.operation in ("INSERT", "UPDATE"):
                self._snapshot[d.entity_id] = d.payload
                applied += 1
        if applied:
            self._snapshot_version += 1
        return applied

    def query(self, entity_type: str | None = None,
              filters: dict[str, Any] | None = None,
              limit: int = 100) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for eid, props in self._snapshot.items():
            if entity_type and props.get("type") != entity_type:
                continue
            if filters:
                match = True
                for k, v in filters.items():
                    if props.get(k) != v:
                        match = False
                        break
                if not match:
                    continue
            results.append({"entity_id": eid, **props})
            if len(results) >= limit:
                break
        return results

    def count(self, entity_type: str | None = None) -> int:
        if not entity_type:
            return len(self._snapshot)
        return sum(1 for p in self._snapshot.values() if p.get("type") == entity_type)

    @property
    def snapshot_version(self) -> int:
        return self._snapshot_version

    @property
    def snapshot_time(self) -> float | None:
        return self._snapshot_time

    def stats(self) -> dict[str, Any]:
        type_counts: dict[str, int] = {}
        for p in self._snapshot.values():
            t = p.get("type", "unknown")
            type_counts[t] = type_counts.get(t, 0) + 1
        return {
            "total_entities": len(self._snapshot),
            "snapshot_version": self._snapshot_version,
            "snapshot_time": self._snapshot_time,
            "type_counts": type_counts,
        }


class EdgeSyncProtocol:
    """Delta-based sync protocol between edge nodes and cloud."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._nodes: dict[str, EdgeNode] = {}
        self._pending_deltas: dict[str, deque[SyncDelta]] = {}
        self._sync_history: dict[str, list[SyncResult]] = {}
        self._global_version: int = 0
        self._max_history: int = 100
        self._offline_engines: dict[str, OfflineQueryEngine] = {}

    def register_node(self, node_id: str, name: str, region: str,
                      sync_direction: SyncDirection = SyncDirection.BIDIRECTIONAL,
                      sync_interval: int = 300,
                      tags: list[str] | None = None) -> EdgeNode:
        with self._lock:
            node = EdgeNode(
                node_id=node_id, name=name, region=region,
                sync_direction=sync_direction,
                sync_interval_seconds=sync_interval,
                tags=tags or [],
            )
            self._nodes[node_id] = node
            self._pending_deltas[node_id] = deque(maxlen=10000)
            self._offline_engines[node_id] = OfflineQueryEngine()
            return node

    def decommission_node(self, node_id: str) -> bool:
        with self._lock:
            node = self._nodes.get(node_id)
            if not node:
                return False
            node.status = EdgeNodeStatus.DECOMMISSIONED
            return True

    def set_node_status(self, node_id: str, status: EdgeNodeStatus) -> bool:
        with self._lock:
            node = self._nodes.get(node_id)
            if not node or node.status == EdgeNodeStatus.DECOMMISSIONED:
                return False
            node.status = status
            return True

    def enqueue_delta(self, node_id: str, delta: SyncDelta) -> bool:
        with self._lock:
            q = self._pending_deltas.get(node_id)
            if q is None:
                return False
            q.append(delta)
            return True

    def sync_node(self, node_id: str,
                  incoming_deltas: list[SyncDelta] | None = None) -> SyncResult:
        start = time.time()
        with self._lock:
            node = self._nodes.get(node_id)
            if not node:
                return SyncResult(
                    sync_id=uuid.uuid4().hex[:12], node_id=node_id,
                    direction=SyncDirection.BIDIRECTIONAL,
                    success=False, error="Node not registered",
                )
            if node.status == EdgeNodeStatus.DECOMMISSIONED:
                return SyncResult(
                    sync_id=uuid.uuid4().hex[:12], node_id=node_id,
                    direction=node.sync_direction,
                    success=False, error="Node decommissioned",
                )

            prev_status = node.status
            node.status = EdgeNodeStatus.SYNCING
            sync_id = uuid.uuid4().hex[:12]

            sent = 0
            received = 0
            conflicts = 0
            resolved = 0

            outbound = list(self._pending_deltas[node_id])
            self._pending_deltas[node_id].clear()
            sent = len(outbound)

            engine = self._offline_engines[node_id]

            if incoming_deltas:
                received = len(incoming_deltas)
                for d in incoming_deltas:
                    existing_ver = node.version_vector.get(d.entity_id, 0)
                    if d.version <= existing_ver:
                        conflicts += 1
                        if d.version == existing_ver:
                            resolved += 1
                    else:
                        node.version_vector[d.entity_id] = d.version
                        resolved += 1

                engine.apply_deltas(incoming_deltas)

            if outbound:
                engine.apply_deltas(outbound)
                for d in outbound:
                    node.version_vector[d.entity_id] = max(
                        node.version_vector.get(d.entity_id, 0), d.version
                    )

            node.local_entity_count = engine.count()
            node.last_sync = time.time()
            node.status = EdgeNodeStatus.ONLINE

            result = SyncResult(
                sync_id=sync_id, node_id=node_id,
                direction=node.sync_direction,
                deltas_sent=sent, deltas_received=received,
                conflicts=conflicts, resolved=resolved,
                duration_ms=(time.time() - start) * 1000,
            )

            hist = self._sync_history.setdefault(node_id, [])
            hist.append(result)
            if len(hist) > self._max_history:
                self._sync_history[node_id] = hist[-self._max_history:]

            return result

    def promote_to_cloud(self, node_id: str, entity_ids: list[str]) -> dict[str, Any]:
        """Promote edge-discovered entities to cloud-level knowledge."""
        with self._lock:
            engine = self._offline_engines.get(node_id)
            if not engine:
                return {"promoted": 0, "error": "Node not found"}
            promoted = []
            for eid in entity_ids:
                entity = engine._snapshot.get(eid)
                if entity:
                    self._global_version += 1
                    promoted.append({
                        "entity_id": eid,
                        "payload": entity,
                        "cloud_version": self._global_version,
                        "source_node": node_id,
                    })
            return {"promoted": len(promoted), "entities": promoted}

    def get_node(self, node_id: str) -> EdgeNode | None:
        return self._nodes.get(node_id)

    def list_nodes(self, region: str | None = None,
                   status: EdgeNodeStatus | None = None) -> list[EdgeNode]:
        nodes = list(self._nodes.values())
        if region:
            nodes = [n for n in nodes if n.region == region]
        if status:
            nodes = [n for n in nodes if n.status == status]
        return nodes

    def get_sync_history(self, node_id: str, limit: int = 20) -> list[SyncResult]:
        return (self._sync_history.get(node_id) or [])[-limit:]

    def offline_query(self, node_id: str, entity_type: str | None = None,
                      filters: dict[str, Any] | None = None,
                      limit: int = 100) -> list[dict[str, Any]]:
        engine = self._offline_engines.get(node_id)
        if not engine:
            return []
        return engine.query(entity_type=entity_type, filters=filters, limit=limit)

    def nodes_needing_sync(self) -> list[str]:
        return [nid for nid, n in self._nodes.items() if n.is_sync_due()]

    def stats(self) -> dict[str, Any]:
        by_status: dict[str, int] = {}
        by_region: dict[str, int] = {}
        total_entities = 0
        for n in self._nodes.values():
            by_status[n.status.value] = by_status.get(n.status.value, 0) + 1
            by_region[n.region] = by_region.get(n.region, 0) + 1
            total_entities += n.local_entity_count
        return {
            "total_nodes": len(self._nodes),
            "by_status": by_status,
            "by_region": by_region,
            "total_edge_entities": total_entities,
            "global_version": self._global_version,
            "nodes_needing_sync": len(self.nodes_needing_sync()),
        }


_instance: EdgeSyncProtocol | None = None
_lock = threading.Lock()


def get_edge_runtime() -> EdgeSyncProtocol:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = EdgeSyncProtocol()
    return _instance
