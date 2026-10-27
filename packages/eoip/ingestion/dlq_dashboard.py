"""Dead Letter Queue Dashboard & Replay — inspect, filter, and replay failed ingestion records."""

from __future__ import annotations

import threading
import time
import uuid
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any
from collections.abc import Callable

from eoip.enterprise.logging import get_logger

_log = get_logger("ingestion.dlq")


class DLQEntryStatus(str, Enum):
    PENDING = "PENDING"
    REPLAYING = "REPLAYING"
    REPLAYED = "REPLAYED"
    DISCARDED = "DISCARDED"
    EXPIRED = "EXPIRED"


@dataclass
class DLQEntry:
    entry_id: str
    source_system: str
    pipeline_id: str
    original_record: dict[str, Any]
    error_message: str
    error_type: str = "unknown"
    status: DLQEntryStatus = DLQEntryStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    created_at: str = ""
    last_retry_at: str | None = None
    tags: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


@dataclass
class DLQStats:
    total_entries: int = 0
    pending: int = 0
    replayed: int = 0
    discarded: int = 0
    by_source: dict[str, int] = field(default_factory=dict)
    by_error_type: dict[str, int] = field(default_factory=dict)
    oldest_entry_age_seconds: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class DLQDashboard:
    """Manages dead letter queue entries with filtering, replay, and analytics."""

    def __init__(self, replay_fn: Callable[[dict], bool] | None = None,
                 max_entries: int = 10000) -> None:
        self._replay_fn = replay_fn or (lambda rec: True)
        self._max_entries = max_entries
        self._entries: dict[str, DLQEntry] = {}
        self._lock = threading.Lock()

    def add_entry(self, source_system: str, pipeline_id: str,
                  record: dict[str, Any], error_message: str,
                  error_type: str = "unknown",
                  tags: dict[str, str] | None = None) -> DLQEntry:
        with self._lock:
            self._enforce_capacity()
            entry_id = uuid.uuid4().hex[:12]
            entry = DLQEntry(
                entry_id=entry_id, source_system=source_system,
                pipeline_id=pipeline_id, original_record=record,
                error_message=error_message, error_type=error_type,
                created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                tags=tags or {},
            )
            self._entries[entry_id] = entry
            return entry

    def get_entry(self, entry_id: str) -> DLQEntry | None:
        return self._entries.get(entry_id)

    def list_entries(self, source: str | None = None,
                     error_type: str | None = None,
                     status: DLQEntryStatus | None = None,
                     limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        entries = list(self._entries.values())
        if source:
            entries = [e for e in entries if e.source_system == source]
        if error_type:
            entries = [e for e in entries if e.error_type == error_type]
        if status:
            entries = [e for e in entries if e.status == status]
        entries.sort(key=lambda e: e.created_at, reverse=True)
        return [e.to_dict() for e in entries[offset : offset + limit]]

    def replay_entry(self, entry_id: str) -> bool:
        entry = self._entries.get(entry_id)
        if not entry or entry.status not in (DLQEntryStatus.PENDING,):
            return False

        entry.status = DLQEntryStatus.REPLAYING
        entry.retry_count += 1
        entry.last_retry_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        try:
            success = self._replay_fn(entry.original_record)
            entry.status = DLQEntryStatus.REPLAYED if success else DLQEntryStatus.PENDING
            return success
        except Exception:
            entry.status = DLQEntryStatus.PENDING
            return False

    def replay_batch(self, entry_ids: list[str] | None = None,
                     source: str | None = None) -> dict[str, Any]:
        targets: list[DLQEntry] = []
        if entry_ids:
            targets = [self._entries[eid] for eid in entry_ids if eid in self._entries]
        elif source:
            targets = [e for e in self._entries.values()
                       if e.source_system == source and e.status == DLQEntryStatus.PENDING]
        else:
            targets = [e for e in self._entries.values()
                       if e.status == DLQEntryStatus.PENDING]

        succeeded = 0
        failed = 0
        for entry in targets:
            if self.replay_entry(entry.entry_id):
                succeeded += 1
            else:
                failed += 1
        return {"total": len(targets), "succeeded": succeeded, "failed": failed}

    def discard_entry(self, entry_id: str) -> bool:
        entry = self._entries.get(entry_id)
        if entry:
            entry.status = DLQEntryStatus.DISCARDED
            return True
        return False

    def purge(self, status: DLQEntryStatus | None = None,
              older_than_seconds: float | None = None) -> int:
        now = time.time()
        to_remove: list[str] = []
        for eid, entry in self._entries.items():
            if status and entry.status != status:
                continue
            if older_than_seconds:
                try:
                    ts = time.strptime(entry.created_at, "%Y-%m-%dT%H:%M:%SZ")
                    age = now - time.mktime(ts)
                    if age < older_than_seconds:
                        continue
                except (ValueError, OverflowError):
                    pass
            to_remove.append(eid)

        for eid in to_remove:
            del self._entries[eid]
        return len(to_remove)

    def get_stats(self) -> DLQStats:
        by_source: dict[str, int] = defaultdict(int)
        by_error: dict[str, int] = defaultdict(int)
        pending = replayed = discarded = 0
        oldest_age = 0.0
        now = time.time()

        for entry in self._entries.values():
            by_source[entry.source_system] += 1
            by_error[entry.error_type] += 1
            if entry.status == DLQEntryStatus.PENDING:
                pending += 1
            elif entry.status == DLQEntryStatus.REPLAYED:
                replayed += 1
            elif entry.status == DLQEntryStatus.DISCARDED:
                discarded += 1
            try:
                ts = time.strptime(entry.created_at, "%Y-%m-%dT%H:%M:%SZ")
                age = now - time.mktime(ts)
                oldest_age = max(oldest_age, age)
            except (ValueError, OverflowError):
                pass

        return DLQStats(
            total_entries=len(self._entries), pending=pending,
            replayed=replayed, discarded=discarded,
            by_source=dict(by_source), by_error_type=dict(by_error),
            oldest_entry_age_seconds=round(oldest_age, 1),
        )

    def _enforce_capacity(self) -> None:
        if len(self._entries) >= self._max_entries:
            replayed = [e for e in self._entries.values()
                        if e.status == DLQEntryStatus.REPLAYED]
            replayed.sort(key=lambda e: e.created_at)
            for entry in replayed[: len(self._entries) - self._max_entries + 1]:
                del self._entries[entry.entry_id]
