"""Snapshot & Point-in-Time Recovery — versioned graph snapshots with rollback."""

from __future__ import annotations

import copy
import hashlib
import json
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from eoip.enterprise.logging import get_logger

_log = get_logger("graph.snapshots")


class SnapshotType(str, Enum):
    FULL = "FULL"
    INCREMENTAL = "INCREMENTAL"
    SCHEMA_ONLY = "SCHEMA_ONLY"


class SnapshotStatus(str, Enum):
    CREATING = "CREATING"
    READY = "READY"
    RESTORING = "RESTORING"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"


@dataclass
class SnapshotConfig:
    auto_snapshot: bool = True
    auto_interval_seconds: int = 3600
    max_snapshots: int = 50
    retention_days: int = 30
    compress: bool = True
    include_metadata: bool = True


@dataclass
class Snapshot:
    snapshot_id: str
    name: str
    snapshot_type: SnapshotType
    status: SnapshotStatus = SnapshotStatus.CREATING
    created_at: str = ""
    entity_count: int = 0
    edge_count: int = 0
    size_bytes: int = 0
    checksum: str = ""
    parent_snapshot_id: str | None = None
    tags: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["snapshot_type"] = self.snapshot_type.value
        d["status"] = self.status.value
        return d


@dataclass
class RestorePoint:
    restore_id: str
    snapshot_id: str
    started_at: str
    completed_at: str | None = None
    entities_restored: int = 0
    edges_restored: int = 0
    success: bool = False


class SnapshotManager:
    """Manages versioned graph snapshots with point-in-time restore."""

    def __init__(self, config: SnapshotConfig | None = None) -> None:
        self._config = config or SnapshotConfig()
        self._snapshots: dict[str, Snapshot] = {}
        self._snapshot_data: dict[str, dict[str, Any]] = {}
        self._restore_log: list[RestorePoint] = []
        self._current_data: dict[str, Any] = {"entities": {}, "edges": [], "schema": {}}
        self._lock = threading.RLock()

    def create_snapshot(self, name: str,
                        snapshot_type: SnapshotType = SnapshotType.FULL,
                        tags: dict[str, str] | None = None) -> Snapshot:
        with self._lock:
            self._enforce_retention()
            sid = uuid.uuid4().hex[:12]
            now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

            data = self._capture_data(snapshot_type)
            raw = json.dumps(data, sort_keys=True, default=str)
            checksum = hashlib.sha256(raw.encode()).hexdigest()[:16]

            snapshot = Snapshot(
                snapshot_id=sid, name=name, snapshot_type=snapshot_type,
                created_at=now,
                entity_count=len(data.get("entities", {})),
                edge_count=len(data.get("edges", [])),
                size_bytes=len(raw),
                checksum=checksum,
                tags=tags or {},
            )

            last = self._latest_snapshot()
            if last and snapshot_type == SnapshotType.INCREMENTAL:
                snapshot.parent_snapshot_id = last.snapshot_id

            self._snapshots[sid] = snapshot
            self._snapshot_data[sid] = data
            snapshot.status = SnapshotStatus.READY
            return snapshot

    def restore_snapshot(self, snapshot_id: str) -> RestorePoint:
        with self._lock:
            snapshot = self._snapshots.get(snapshot_id)
            if not snapshot or snapshot.status != SnapshotStatus.READY:
                raise ValueError(f"Snapshot {snapshot_id} not available for restore")

            data = self._snapshot_data.get(snapshot_id)
            if not data:
                raise ValueError(f"No data for snapshot {snapshot_id}")

            rid = uuid.uuid4().hex[:8]
            now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            rp = RestorePoint(restore_id=rid, snapshot_id=snapshot_id, started_at=now)

            snapshot.status = SnapshotStatus.RESTORING
            self._current_data = copy.deepcopy(data)
            rp.entities_restored = len(data.get("entities", {}))
            rp.edges_restored = len(data.get("edges", []))
            rp.completed_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            rp.success = True
            snapshot.status = SnapshotStatus.READY

            self._restore_log.append(rp)
            return rp

    def delete_snapshot(self, snapshot_id: str) -> bool:
        with self._lock:
            if snapshot_id in self._snapshots:
                del self._snapshots[snapshot_id]
                self._snapshot_data.pop(snapshot_id, None)
                return True
            return False

    def get_snapshot(self, snapshot_id: str) -> Snapshot | None:
        return self._snapshots.get(snapshot_id)

    def list_snapshots(self) -> list[dict[str, Any]]:
        return sorted(
            [s.to_dict() for s in self._snapshots.values()],
            key=lambda x: x["created_at"], reverse=True,
        )

    def compare_snapshots(self, id_a: str, id_b: str) -> dict[str, Any]:
        data_a = self._snapshot_data.get(id_a, {})
        data_b = self._snapshot_data.get(id_b, {})
        ents_a = set(data_a.get("entities", {}).keys())
        ents_b = set(data_b.get("entities", {}).keys())
        return {
            "added": list(ents_b - ents_a),
            "removed": list(ents_a - ents_b),
            "common": len(ents_a & ents_b),
            "a_total": len(ents_a),
            "b_total": len(ents_b),
        }

    def get_restore_log(self) -> list[dict[str, Any]]:
        return [asdict(rp) for rp in self._restore_log]

    def set_current_data(self, entities: dict[str, Any] | None = None,
                         edges: list[dict] | None = None,
                         schema: dict[str, Any] | None = None) -> None:
        with self._lock:
            if entities is not None:
                self._current_data["entities"] = entities
            if edges is not None:
                self._current_data["edges"] = edges
            if schema is not None:
                self._current_data["schema"] = schema

    def _capture_data(self, snapshot_type: SnapshotType) -> dict[str, Any]:
        if snapshot_type == SnapshotType.SCHEMA_ONLY:
            return {"schema": copy.deepcopy(self._current_data.get("schema", {}))}
        return copy.deepcopy(self._current_data)

    def _latest_snapshot(self) -> Snapshot | None:
        ready = [s for s in self._snapshots.values() if s.status == SnapshotStatus.READY]
        if not ready:
            return None
        return max(ready, key=lambda s: s.created_at)

    def _enforce_retention(self) -> None:
        ready = sorted(
            [s for s in self._snapshots.values() if s.status == SnapshotStatus.READY],
            key=lambda s: s.created_at,
        )
        while len(ready) >= self._config.max_snapshots:
            oldest = ready.pop(0)
            self.delete_snapshot(oldest.snapshot_id)
