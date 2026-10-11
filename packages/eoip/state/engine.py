"""State and persistence engineering engine."""

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


@dataclass
class StateSnapshot:
    snapshot_id: str
    stream: str
    state: dict[str, Any]
    version: int
    checksum: str
    created_at: float = field(default_factory=time.time)


class StateEngine:
    """Small event/snapshot facade used by platform engineering routes."""

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
