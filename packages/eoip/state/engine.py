"""State and persistence engineering engine with event-sourcing and time-travel."""

from __future__ import annotations

import copy
import hashlib
import json
import threading
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class StateEvent:
    event_id: str
    stream: str
    operation: str
    payload: dict[str, Any]
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "stream": self.stream,
            "operation": self.operation,
            "payload": self.payload,
            "timestamp": self.timestamp,
        }


@dataclass
class StateSnapshot:
    snapshot_id: str
    stream: str
    state: dict[str, Any]
    version: int
    checksum: str
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "stream": self.stream,
            "state": self.state,
            "version": self.version,
            "checksum": self.checksum,
            "created_at": self.created_at,
        }


class StateEngine:
    """Event-sourcing, snapshotting, and time-travel persistence engine."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._events: list[StateEvent] = []
        self._state: dict[str, dict[str, Any]] = {}
        self._snapshots: dict[str, StateSnapshot] = {}

    def record(self, stream: str, operation: str, payload: dict[str, Any]) -> StateEvent:
        with self._lock:
            event_id = f"state-event-{len(self._events) + 1:08d}"
            event = StateEvent(event_id=event_id, stream=stream, operation=operation, payload=dict(payload))
            self._events.append(event)
            current = self._state.setdefault(stream, {})
            if operation == "delete":
                for key in payload:
                    current.pop(key, None)
            else:
                current.update(payload)
            return event

    def snapshot(self, stream: str) -> StateSnapshot:
        with self._lock:
            state = copy.deepcopy(self._state.get(stream, {}))
            version = sum(1 for event in self._events if event.stream == stream)
            checksum = hashlib.sha256(json.dumps(state, sort_keys=True).encode()).hexdigest()[:16]
            snapshot = StateSnapshot(
                snapshot_id=f"state-snapshot-{stream}-{version}",
                stream=stream,
                state=state,
                version=version,
                checksum=checksum,
            )
            self._snapshots[snapshot.snapshot_id] = snapshot
            return snapshot

    def restore(self, snapshot_id: str) -> bool:
        with self._lock:
            snapshot = self._snapshots.get(snapshot_id)
            if snapshot is None:
                return False
            self._state[snapshot.stream] = copy.deepcopy(snapshot.state)
            return True

    def get_stream_state(self, stream: str) -> dict[str, Any]:
        with self._lock:
            return copy.deepcopy(self._state.get(stream, {}))

    def get_stream_events(self, stream: str, limit: int = 50) -> list[StateEvent]:
        with self._lock:
            stream_events = [e for e in self._events if e.stream == stream]
            return stream_events[-limit:]

    def list_snapshots(self, stream: str | None = None) -> list[StateSnapshot]:
        with self._lock:
            if stream:
                return [s for s in self._snapshots.values() if s.stream == stream]
            return list(self._snapshots.values())

    def time_travel_state(self, stream: str, target_timestamp: float) -> dict[str, Any]:
        """Reconstruct state of stream by playing events up to target_timestamp."""
        with self._lock:
            target_events = [e for e in self._events if e.stream == stream and e.timestamp <= target_timestamp]
        
        reconstructed: dict[str, Any] = {}
        for ev in target_events:
            if ev.operation == "delete":
                for key in ev.payload:
                    reconstructed.pop(key, None)
            else:
                reconstructed.update(ev.payload)
        return reconstructed

    def diff_snapshots(self, snapshot_id_a: str, snapshot_id_b: str) -> dict[str, Any]:
        """Compute delta between two snapshots."""
        with self._lock:
            snap_a = self._snapshots.get(snapshot_id_a)
            snap_b = self._snapshots.get(snapshot_id_b)
        if not snap_a or not snap_b:
            raise ValueError("Both snapshots must exist to compute diff.")
        
        state_a = snap_a.state
        state_b = snap_b.state
        added = {k: state_b[k] for k in state_b if k not in state_a}
        removed = {k: state_a[k] for k in state_a if k not in state_b}
        modified = {k: {"before": state_a[k], "after": state_b[k]} for k in state_a if k in state_b and state_a[k] != state_b[k]}
        
        return {
            "snapshot_a": snapshot_id_a,
            "snapshot_b": snapshot_id_b,
            "added": added,
            "removed": removed,
            "modified": modified,
        }

    def stats(self) -> dict[str, Any]:
        with self._lock:
            return {
                "engine": "state_persistence",
                "streams": len(self._state),
                "events": len(self._events),
                "snapshots": len(self._snapshots),
            }


_instance: StateEngine | None = None
_lock = threading.Lock()


def get_state_engine() -> StateEngine:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = StateEngine()
    return _instance

