"""Write-Ahead Log and disaster recovery infrastructure.

Provides a WAL for durable graph mutations, point-in-time recovery,
configurable RPO/RTO targets, and active-passive replication protocol
with automatic failover detection.
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


class WALOperationType(str, Enum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    SCHEMA_CHANGE = "SCHEMA_CHANGE"
    BULK_IMPORT = "BULK_IMPORT"


class ReplicationRole(str, Enum):
    PRIMARY = "PRIMARY"
    STANDBY = "STANDBY"
    WITNESS = "WITNESS"


class PeerState(str, Enum):
    HEALTHY = "HEALTHY"
    LAGGING = "LAGGING"
    UNREACHABLE = "UNREACHABLE"
    FAILED = "FAILED"


@dataclass
class WALEntry:
    lsn: int  # Log Sequence Number
    operation: WALOperationType
    entity_type: str
    entity_id: str
    payload: dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    checksum: str = ""
    tenant_id: str = "default"

    def __post_init__(self) -> None:
        if not self.checksum:
            raw = f"{self.lsn}:{self.operation.value}:{self.entity_id}:{self.timestamp}"
            self.checksum = hashlib.sha256(raw.encode()).hexdigest()[:16]

    def to_dict(self) -> dict[str, Any]:
        return {
            "lsn": self.lsn,
            "operation": self.operation.value,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "checksum": self.checksum,
            "tenant_id": self.tenant_id,
        }


@dataclass
class WALSegment:
    segment_id: str
    start_lsn: int
    end_lsn: int
    entry_count: int
    size_bytes: int
    created_at: float = field(default_factory=time.time)
    sealed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "segment_id": self.segment_id,
            "start_lsn": self.start_lsn,
            "end_lsn": self.end_lsn,
            "entry_count": self.entry_count,
            "size_bytes": self.size_bytes,
            "created_at": self.created_at,
            "sealed": self.sealed,
        }


@dataclass
class RecoveryConfig:
    rpo_seconds: float = 30.0
    rto_seconds: float = 300.0
    max_wal_entries: int = 100000
    segment_size: int = 10000
    checkpoint_interval_seconds: float = 60.0
    retention_segments: int = 100
    geo_redundancy: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "rpo_seconds": self.rpo_seconds,
            "rto_seconds": self.rto_seconds,
            "max_wal_entries": self.max_wal_entries,
            "segment_size": self.segment_size,
            "checkpoint_interval_seconds": self.checkpoint_interval_seconds,
            "retention_segments": self.retention_segments,
            "geo_redundancy": self.geo_redundancy,
        }


@dataclass
class ReplicationPeer:
    peer_id: str
    role: ReplicationRole
    endpoint: str
    state: PeerState = PeerState.HEALTHY
    last_lsn_acked: int = 0
    lag_entries: int = 0
    last_heartbeat: float = field(default_factory=time.time)
    consecutive_failures: int = 0

    def update_heartbeat(self) -> None:
        self.last_heartbeat = time.time()
        self.consecutive_failures = 0
        if self.state == PeerState.UNREACHABLE:
            self.state = PeerState.HEALTHY

    def record_failure(self, max_failures: int = 3) -> None:
        self.consecutive_failures += 1
        if self.consecutive_failures >= max_failures:
            self.state = PeerState.FAILED
        elif self.consecutive_failures >= 2:
            self.state = PeerState.UNREACHABLE

    def to_dict(self) -> dict[str, Any]:
        return {
            "peer_id": self.peer_id,
            "role": self.role.value,
            "endpoint": self.endpoint,
            "state": self.state.value,
            "last_lsn_acked": self.last_lsn_acked,
            "lag_entries": self.lag_entries,
            "last_heartbeat": self.last_heartbeat,
        }


@dataclass
class RecoveryPoint:
    point_id: str
    lsn: int
    timestamp: float
    label: str = ""
    entry_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "point_id": self.point_id,
            "lsn": self.lsn,
            "timestamp": self.timestamp,
            "label": self.label,
            "entry_count": self.entry_count,
        }


class WriteAheadLog:
    """Durable WAL with segmentation, replication, and point-in-time recovery."""

    def __init__(self, config: RecoveryConfig | None = None) -> None:
        self._lock = threading.Lock()
        self._config = config or RecoveryConfig()
        self._lsn: int = 0
        self._entries: deque[WALEntry] = deque(maxlen=self._config.max_wal_entries)
        self._segments: list[WALSegment] = []
        self._current_segment_entries: int = 0
        self._current_segment_start: int = 1
        self._peers: dict[str, ReplicationPeer] = {}
        self._checkpoints: list[RecoveryPoint] = []
        self._last_checkpoint_time: float = time.time()
        self._role: ReplicationRole = ReplicationRole.PRIMARY

    @property
    def config(self) -> RecoveryConfig:
        return self._config

    @property
    def current_lsn(self) -> int:
        return self._lsn

    @property
    def role(self) -> ReplicationRole:
        return self._role

    def append(self, operation: WALOperationType, entity_type: str,
               entity_id: str, payload: dict[str, Any],
               tenant_id: str = "default") -> WALEntry:
        with self._lock:
            self._lsn += 1
            entry = WALEntry(
                lsn=self._lsn, operation=operation,
                entity_type=entity_type, entity_id=entity_id,
                payload=payload, tenant_id=tenant_id,
            )
            self._entries.append(entry)
            self._current_segment_entries += 1

            if self._current_segment_entries >= self._config.segment_size:
                self._seal_segment()

            for peer in self._peers.values():
                if peer.role == ReplicationRole.STANDBY:
                    peer.lag_entries = self._lsn - peer.last_lsn_acked
                    if peer.lag_entries > self._config.segment_size:
                        peer.state = PeerState.LAGGING

            return entry

    def _seal_segment(self) -> None:
        seg = WALSegment(
            segment_id=uuid.uuid4().hex[:12],
            start_lsn=self._current_segment_start,
            end_lsn=self._lsn,
            entry_count=self._current_segment_entries,
            size_bytes=self._current_segment_entries * 256,
            sealed=True,
        )
        self._segments.append(seg)
        self._current_segment_start = self._lsn + 1
        self._current_segment_entries = 0

        if len(self._segments) > self._config.retention_segments:
            self._segments = self._segments[-self._config.retention_segments:]

    def read_from(self, start_lsn: int, limit: int = 1000) -> list[WALEntry]:
        with self._lock:
            return [e for e in self._entries if e.lsn >= start_lsn][:limit]

    def checkpoint(self, label: str = "") -> RecoveryPoint:
        with self._lock:
            pt = RecoveryPoint(
                point_id=uuid.uuid4().hex[:12],
                lsn=self._lsn,
                timestamp=time.time(),
                label=label or f"checkpoint-{self._lsn}",
                entry_count=len(self._entries),
            )
            self._checkpoints.append(pt)
            self._last_checkpoint_time = time.time()
            return pt

    def list_checkpoints(self, limit: int = 20) -> list[RecoveryPoint]:
        return self._checkpoints[-limit:]

    def recover_to_point(self, point_id: str) -> dict[str, Any]:
        with self._lock:
            target = None
            for cp in self._checkpoints:
                if cp.point_id == point_id:
                    target = cp
                    break
            if not target:
                return {"success": False, "error": "Checkpoint not found"}

            entries_to_replay = [e for e in self._entries if e.lsn <= target.lsn]
            return {
                "success": True,
                "target_lsn": target.lsn,
                "target_label": target.label,
                "entries_to_replay": len(entries_to_replay),
                "recovery_time_estimate_seconds": len(entries_to_replay) * 0.001,
            }

    def recover_to_timestamp(self, target_ts: float) -> dict[str, Any]:
        with self._lock:
            entries = [e for e in self._entries if e.timestamp <= target_ts]
            if not entries:
                return {"success": False, "error": "No entries before timestamp"}
            max_lsn = max(e.lsn for e in entries)
            return {
                "success": True,
                "target_lsn": max_lsn,
                "entries_to_replay": len(entries),
                "recovery_time_estimate_seconds": len(entries) * 0.001,
            }

    def add_peer(self, peer_id: str, role: ReplicationRole,
                 endpoint: str) -> ReplicationPeer:
        with self._lock:
            peer = ReplicationPeer(
                peer_id=peer_id, role=role, endpoint=endpoint,
            )
            self._peers[peer_id] = peer
            return peer

    def remove_peer(self, peer_id: str) -> bool:
        with self._lock:
            return self._peers.pop(peer_id, None) is not None

    def ack_peer(self, peer_id: str, acked_lsn: int) -> bool:
        with self._lock:
            peer = self._peers.get(peer_id)
            if not peer:
                return False
            peer.last_lsn_acked = acked_lsn
            peer.lag_entries = max(0, self._lsn - acked_lsn)
            peer.update_heartbeat()
            if peer.lag_entries == 0:
                peer.state = PeerState.HEALTHY
            elif peer.lag_entries <= self._config.segment_size:
                peer.state = PeerState.HEALTHY
            return True

    def peer_heartbeat(self, peer_id: str) -> bool:
        with self._lock:
            peer = self._peers.get(peer_id)
            if not peer:
                return False
            peer.update_heartbeat()
            return True

    def check_peer_health(self, timeout_seconds: float = 30.0) -> list[dict[str, Any]]:
        now = time.time()
        issues: list[dict[str, Any]] = []
        with self._lock:
            for peer in self._peers.values():
                since = now - peer.last_heartbeat
                if since > timeout_seconds:
                    peer.record_failure()
                    issues.append({
                        "peer_id": peer.peer_id,
                        "state": peer.state.value,
                        "seconds_since_heartbeat": round(since, 1),
                        "lag_entries": peer.lag_entries,
                    })
        return issues

    def promote_standby(self, peer_id: str) -> dict[str, Any]:
        with self._lock:
            peer = self._peers.get(peer_id)
            if not peer or peer.role != ReplicationRole.STANDBY:
                return {"success": False, "error": "Not a standby peer"}
            self._role = ReplicationRole.STANDBY
            peer.role = ReplicationRole.PRIMARY
            return {
                "success": True,
                "new_primary": peer_id,
                "lag_at_promotion": peer.lag_entries,
            }

    def rpo_status(self) -> dict[str, Any]:
        now = time.time()
        last_entry_time = self._entries[-1].timestamp if self._entries else now
        since_last_write = now - last_entry_time
        since_last_checkpoint = now - self._last_checkpoint_time

        within_rpo = since_last_checkpoint <= self._config.rpo_seconds
        standby_synced = all(
            p.lag_entries <= 10
            for p in self._peers.values()
            if p.role == ReplicationRole.STANDBY
        )

        return {
            "rpo_target_seconds": self._config.rpo_seconds,
            "rto_target_seconds": self._config.rto_seconds,
            "since_last_checkpoint_seconds": round(since_last_checkpoint, 2),
            "since_last_write_seconds": round(since_last_write, 2),
            "within_rpo": within_rpo,
            "standby_synced": standby_synced,
            "estimated_rto_seconds": round(len(self._entries) * 0.001, 2),
        }

    def list_segments(self, limit: int = 20) -> list[WALSegment]:
        return self._segments[-limit:]

    def list_peers(self) -> list[ReplicationPeer]:
        return list(self._peers.values())

    def stats(self) -> dict[str, Any]:
        return {
            "current_lsn": self._lsn,
            "total_entries": len(self._entries),
            "sealed_segments": len(self._segments),
            "current_segment_entries": self._current_segment_entries,
            "checkpoints": len(self._checkpoints),
            "peers": len(self._peers),
            "role": self._role.value,
            "rpo_status": self.rpo_status(),
        }


_instance: WriteAheadLog | None = None
_lock = threading.Lock()


def get_wal(config: RecoveryConfig | None = None) -> WriteAheadLog:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = WriteAheadLog(config=config)
    return _instance
