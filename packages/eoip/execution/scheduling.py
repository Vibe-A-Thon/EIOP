"""Distributed scheduling primitives — §7 Reasoning & Orchestration.

Lease-based work claiming and priority queues, reusing ``eoip.ha.LeaderLease``
for scheduler election and per-item lease records for at-most-once claiming.
Items are persisted as JSON files under a caller-supplied root (matching the
``eoip.jobs`` convention) so claimed work survives process restarts; a claim
expires after its TTL and may be re-claimed by another worker.

External gate: cross-host lease safety relies on the shared filesystem +
TTL discipline documented in ``eoip.ha``; a consensus-backed lease (etcd/
ZooKeeper) is out of scope for the offline primitives.
"""

from __future__ import annotations

import heapq
import itertools
import threading
import uuid
from datetime import UTC
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from eoip.contracts.source_event import utc_now_iso
from eoip.ha import LeaderLease
from eoip.jobs import write_json


class WorkItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_id: str
    kind: str
    payload: dict[str, Any] = Field(default_factory=dict)
    priority: int = 0  # higher = more urgent
    created_at: str = ""
    seq: int = 0  # heap ordering sequence
    status: str = "PENDING"  # PENDING|LEASED|DONE
    lease_owner: str | None = None
    lease_expires_at: str | None = None  # ISO; lease TTL discipline
    attempts: int = 0


class PriorityWorkQueue:
    """Priority queue with lease-based claiming.

    ``enqueue`` accepts items with a numeric priority; ``claim`` atomically
    leases the highest-priority available item to a caller-supplied owner for
    ``lease_ttl_seconds``. Expired leases are reclaimable. A :class:`LeaderLease`
    may be passed for scheduler-election before claiming (single dispatcher).
    """

    def __init__(self, root: str | Path | None = None, *, lease_ttl_seconds: float = 30.0):
        if lease_ttl_seconds <= 0:
            raise ValueError("lease_ttl_seconds must be positive")
        self.root = Path(root) / "workqueue" if root else None
        if self.root:
            self.root.mkdir(parents=True, exist_ok=True)
        self.lease_ttl_seconds = lease_ttl_seconds
        self._lock = threading.RLock()
        self._heap: list[tuple[int, int, str]] = []  # (-priority, seq, item_id)
        self._items: dict[str, WorkItem] = {}
        self._seq = itertools.count()

    # -- enqueue ---------------------------------------------------------------

    def enqueue(self, kind: str, payload: dict[str, Any] | None = None, *,
                priority: int = 0, item_id: str | None = None) -> WorkItem:
        with self._lock:
            seq = next(self._seq)
            item = WorkItem(item_id=item_id or str(uuid.uuid4()), kind=kind,
                            payload=payload or {}, priority=priority,
                            created_at=utc_now_iso(), seq=seq)
            self._items[item.item_id] = item
            heapq.heappush(self._heap, (-priority, seq, item.item_id))
            self._persist(item)
            return item

    # -- claiming ----------------------------------------------------------------

    def claim(self, owner: str, *, lease_ttl_seconds: float | None = None) -> WorkItem | None:
        """Lease the highest-priority available item. Expired leases are
        reclaimed; returns None when no work is available."""
        from datetime import datetime, timedelta

        ttl = lease_ttl_seconds or self.lease_ttl_seconds
        expires = (datetime.now(UTC) + timedelta(seconds=ttl)) \
            .strftime("%Y-%m-%dT%H:%M:%S.%f")[:23] + "Z"
        with self._lock:
            now = utc_now_iso()
            best_entry: tuple[int, int, str] | None = None
            for entry in self._heap:
                item_id = entry[2]
                item = self._items[item_id]
                if item.status == "DONE":
                    continue
                if item.status == "LEASED" and item.lease_expires_at \
                        and item.lease_expires_at > now:
                    continue  # live lease held by another worker
                if best_entry is None or entry < best_entry:
                    best_entry = entry
            if best_entry is None:
                return None
            self._heap.remove(best_entry)
            heapq.heapify(self._heap)
            _, _, item_id = best_entry
            item = self._items[item_id]
            if item.status == "LEASED":
                item.attempts += 1  # expired lease reclaimed
            item.status = "LEASED"
            item.lease_owner = owner
            item.lease_expires_at = expires
            heapq.heappush(self._heap, best_entry)  # stays visible for reclaim
            self._persist(item)
            return item

    def _remove_from_heap(self, item: WorkItem) -> None:
        entry = (-item.priority, item.seq, item.item_id)
        if entry in self._heap:
            self._heap.remove(entry)
            heapq.heapify(self._heap)

    def complete(self, item_id: str, *, owner: str) -> WorkItem:
        """Mark a leased item done; only the lease owner may complete it."""
        with self._lock:
            item = self._items[item_id]
            if item.status != "LEASED" or item.lease_owner != owner:
                raise RuntimeError(f"item {item_id} is not leased by {owner}")
            item.status = "DONE"
            item.lease_owner = None
            item.lease_expires_at = None
            self._remove_from_heap(item)
            self._persist(item)
            return item

    def release(self, item_id: str, *, owner: str) -> WorkItem:
        """Return a leased item to the pending queue (worker fault path)."""
        with self._lock:
            item = self._items[item_id]
            if item.status != "LEASED" or item.lease_owner != owner:
                raise RuntimeError(f"item {item_id} is not leased by {owner}")
            item.status = "PENDING"
            item.lease_owner = None
            item.lease_expires_at = None
            self._remove_from_heap(item)
            item.seq = next(self._seq)
            heapq.heappush(self._heap, (-item.priority, item.seq, item.item_id))
            self._persist(item)
            return item

    # -- queries ---------------------------------------------------------------

    def list(self, *, status: str | None = None) -> list[WorkItem]:
        with self._lock:
            items = [i for i in self._items.values() if status is None or i.status == status]
        return sorted(items, key=lambda i: (-i.priority, i.created_at, i.item_id))

    def _persist(self, item: WorkItem) -> None:
        if self.root:
            write_json(self.root / f"{item.item_id}.json", item.model_dump())


class SchedulerElection:
    """Thin wrapper pairing a :class:`LeaderLease` with a work queue: only the
    lease-holding dispatcher may claim and dispatch work (GAP-HA-001 reuse)."""

    def __init__(self, lease: LeaderLease, queue: PriorityWorkQueue):
        self.lease = lease
        self.queue = queue

    def dispatch_once(self, owner: str) -> WorkItem | None:
        """Claim one item iff this process can hold the leader lease.

        Uses the expiry-aware ``acquire`` path so a standby dispatcher takes
        over after the previous holder's lease TTL elapses (GAP-HA-001)."""
        if not self.lease.acquire():
            return None
        self.lease.renew()
        return self.queue.claim(owner)
