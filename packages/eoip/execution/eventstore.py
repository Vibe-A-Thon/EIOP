"""Event-sourcing helpers — §7 Reasoning & Orchestration: durable execution.

Append-only per-stream event store with snapshots and reconciliation.
Persistence is JSONL-per-stream under a caller-supplied root (matching the
``eoip.jobs`` atomic-write convention). Optimistic concurrency is enforced via
``expected_seq``. This module owns no workflow semantics; see
:mod:`eoip.execution.workflows` for the workflow engine built on top.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from eoip.contracts.source_event import utc_now_iso


class Event(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stream_id: str
    seq: int  # 1-based per-stream sequence
    event_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    recorded_at: str = ""


class Snapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stream_id: str
    up_to_seq: int
    state: dict[str, Any]
    taken_at: str = ""


class ReconciliationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stream_id: str
    event_count: int
    gaps: list[int]  # missing seq numbers
    duplicates: list[int]
    expected_next_seq: int
    consistent: bool


class EventStore:
    """Append-only event store: one JSONL file per stream, plus snapshots."""

    def __init__(self, root: str | Path | None = None):
        self.root = Path(root) / "eventstore" if root else None
        if self.root:
            self.root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._memory: dict[str, list[Event]] = {}

    # -- streams ------------------------------------------------------------

    def _stream_path(self, stream_id: str) -> Path:
        safe = stream_id.replace("/", "_").replace(":", "_")
        return (self.root or Path()) / f"{safe}.jsonl"

    def append(self, stream_id: str, event_type: str,
               payload: dict[str, Any] | None = None, *, expected_seq: int | None = None) -> Event:
        with self._lock:
            events = self._memory.setdefault(stream_id, [])
            next_seq = (events[-1].seq + 1) if events else 1
            if expected_seq is not None and expected_seq != next_seq:
                raise RuntimeError(
                    f"concurrency conflict on {stream_id}: expected seq {expected_seq}, next is {next_seq}")
            event = Event(stream_id=stream_id, seq=next_seq, event_type=event_type,
                          payload=payload or {}, recorded_at=utc_now_iso())
            events.append(event)
            if self.root:
                with self._stream_path(stream_id).open("a", encoding="utf-8") as handle:
                    handle.write(event.model_dump_json() + "\n")
            return event

    def read(self, stream_id: str, *, after_seq: int = 0) -> list[Event]:
        with self._lock:
            return [e for e in self._memory.get(stream_id, []) if e.seq > after_seq]

    def load(self, stream_id: str) -> None:
        """Load a persisted stream from disk into memory (idempotent)."""
        if not self.root:
            return
        path = self._stream_path(stream_id)
        if not path.exists() or stream_id in self._memory:
            return
        with self._lock:
            events = self._memory.setdefault(stream_id, [])
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line:
                    events.append(Event.model_validate(json.loads(line)))

    # -- snapshots -----------------------------------------------------------

    def save_snapshot(self, stream_id: str, state: dict[str, Any], *, up_to_seq: int) -> Snapshot:
        snapshot = Snapshot(stream_id=stream_id, up_to_seq=up_to_seq, state=state,
                            taken_at=utc_now_iso())
        if self.root:
            safe = stream_id.replace("/", "_").replace(":", "_")
            (self.root / f"{safe}.snapshot.json").write_text(snapshot.model_dump_json(), encoding="utf-8")
        return snapshot

    def load_snapshot(self, stream_id: str) -> Snapshot | None:
        if not self.root:
            return None
        safe = stream_id.replace("/", "_").replace(":", "_")
        path = self.root / f"{safe}.snapshot.json"
        if not path.exists():
            return None
        return Snapshot.model_validate(json.loads(path.read_text(encoding="utf-8")))

    # -- reconciliation -------------------------------------------------------

    def reconcile(self, stream_id: str) -> ReconciliationReport:
        """Verify per-stream sequence continuity; report gaps/duplicates."""
        with self._lock:
            events = list(self._memory.get(stream_id, []))
        seen: dict[int, int] = {}
        for event in events:
            seen[event.seq] = seen.get(event.seq, 0) + 1
        if events:
            lo, hi = min(seen), max(seen)
            gaps = [seq for seq in range(lo, hi + 1) if seq not in seen]
        else:
            gaps = []
        duplicates = sorted(seq for seq, count in seen.items() if count > 1)
        return ReconciliationReport(
            stream_id=stream_id,
            event_count=len(events),
            gaps=gaps,
            duplicates=duplicates,
            expected_next_seq=(max(seen) + 1) if seen else 1,
            consistent=not gaps and not duplicates,
        )
