"""Local minimized task memory; durable traces and audit are separate stores."""

from __future__ import annotations

import json
import logging
import os
from collections import OrderedDict
from collections.abc import Callable, Generator
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path
from tempfile import NamedTemporaryFile
from threading import RLock
from typing import Literal, Protocol

from eoip.contracts.agent import AgentResult
from eoip.contracts.memory import MemoryRecord
from pydantic import BaseModel, ConfigDict, Field

log = logging.getLogger("eoip.agents.memory")
MAX_TTL_SECONDS = 30 * 86400


class MemoryPolicyError(ValueError):
    """The proposed record is forbidden by the local memory policy."""


class MemoryCapacityError(MemoryPolicyError):
    """Unexpired records exhaust the configured capacity."""


class MemoryStorageError(RuntimeError):
    """Storage is unavailable or corrupt; no successful persistence is implied."""


class MemoryPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    schema_version: Literal["1.0"] = "1.0"
    ttl_seconds: int = Field(default=MAX_TTL_SECONDS, ge=1, le=MAX_TTL_SECONDS)
    max_records: int = Field(default=1000, ge=1, le=100_000)
    max_bytes: int = Field(default=8 * 1024 * 1024, ge=512, le=64 * 1024 * 1024)


class TaskMemoryContent(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    status: Literal["SUCCEEDED", "PARTIAL", "FAILED", "DENIED", "CANCELLED"]
    evidence_count: int = Field(ge=0, le=100_000)


class MemoryStore(Protocol):
    policy: MemoryPolicy

    def put(self, record: MemoryRecord, *, correlation_id: str | None = None) -> None: ...

    def get(self, memory_id: str, *, scope: str, owner: str) -> MemoryRecord | None: ...

    def delete(self, memory_id: str, *, scope: str, owner: str) -> bool: ...

    def prune(self) -> int: ...


class FileMemoryStore:
    """One bounded atomic JSON document, serialized across processes by an OS lock."""

    def __init__(
        self,
        root: Path | None = None,
        *,
        policy: MemoryPolicy | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self.policy = policy or MemoryPolicy()
        self._clock = clock or (lambda: datetime.now(UTC))
        self._lock = RLock()
        root = root if root is not None else Path(os.getenv("EOIP_DATA_DIR", ".data"))
        self.path = root / "agent-memory" / "records.json"
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise MemoryStorageError("Memory directory is unavailable") from exc
        self.prune()

    @contextmanager
    def _locked(self) -> Generator[None, None, None]:
        with self._lock:
            try:
                with (self.path.parent / "records.lock").open("a+b") as handle:
                    if os.name == "nt":
                        import msvcrt

                        if handle.seek(0, os.SEEK_END) == 0:
                            handle.write(b"\0")
                            handle.flush()
                        handle.seek(0)
                        msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
                    else:
                        import fcntl

                        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
                    try:
                        yield
                    finally:
                        if os.name == "nt":
                            handle.seek(0)
                            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                        else:
                            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            except OSError as exc:
                log.error("memory.storage_failed", extra={
                    "event": "memory.storage_failed", "error_type": type(exc).__name__,
                })
                raise MemoryStorageError("Memory storage operation failed") from exc

    def _validate(self, record: MemoryRecord, now: datetime) -> datetime:
        try:
            created = datetime.fromisoformat(record.created_at)
            if created.tzinfo is None or created > now:
                raise ValueError("Memory timestamp must be timezone-aware and not in the future")
            for value in (record.memory_id, record.scope, record.owner, record.source):
                if not value.strip() or len(value) > 256:
                    raise ValueError("Memory identity, scope, owner and source must be bounded and nonblank")
            if record.kind != "TASK" or record.classification not in {"PUBLIC", "INTERNAL"}:
                raise ValueError("Only PUBLIC/INTERNAL task memory is approved")
            if record.deletion_policy != "DELETE_AT_EXPIRY":
                raise ValueError("Memory must be deleted at expiry")
            if record.ttl_seconds is None or not 1 <= record.ttl_seconds <= self.policy.ttl_seconds:
                raise ValueError("Memory TTL must be positive and within the configured maximum")
            if not record.provenance_refs or len(record.provenance_refs) > 100:
                raise ValueError("Memory requires bounded provenance references")
            if any(not isinstance(ref, str) or not ref.strip() or len(ref) > 512
                   for ref in record.provenance_refs):
                raise ValueError("Provenance references must be bounded nonblank strings")
            if record.confidence is not None and not 0 <= record.confidence <= 1:
                raise ValueError("Memory confidence must be between zero and one")
            TaskMemoryContent.model_validate(record.content)
            return created + timedelta(seconds=record.ttl_seconds)
        except (ValueError, TypeError, OverflowError) as exc:
            raise MemoryPolicyError("Memory record violates task-memory policy") from exc

    def _read(self, now: datetime) -> list[MemoryRecord]:
        if not self.path.exists():
            return []
        try:
            with self.path.open("rb") as handle:
                raw = handle.read(self.policy.max_bytes + 1)
            if len(raw) > self.policy.max_bytes:
                raise ValueError("Memory file exceeds configured byte bound")
            payload = json.loads(raw)
            if (
                not isinstance(payload, dict) or payload.get("schema_version") != "1.0"
                or set(payload) != {"schema_version", "records"}
                or not isinstance(payload["records"], list)
                or len(payload["records"]) > self.policy.max_records
            ):
                raise ValueError("Invalid memory storage envelope")
            if any(not isinstance(item, dict) or set(item) != set(MemoryRecord.model_fields)
                   for item in payload["records"]):
                raise ValueError("Unexpected memory record fields")
            records = [MemoryRecord.model_validate(item) for item in payload["records"]]
            if len({item.memory_id for item in records}) != len(records):
                raise ValueError("Duplicate memory identity")
            for record in records:
                self._validate(record, now)
            return records
        except (ValueError, TypeError, KeyError) as exc:
            log.error("memory.storage_corrupt", extra={
                "event": "memory.storage_corrupt", "error_type": type(exc).__name__,
            })
            raise MemoryStorageError("Memory storage failed validation") from exc

    def _write(self, records: list[MemoryRecord]) -> None:
        encoded = json.dumps({
            "schema_version": "1.0",
            "records": [record.model_dump() for record in records],
        }, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")
        if len(records) > self.policy.max_records or len(encoded) > self.policy.max_bytes:
            raise MemoryCapacityError("Task memory capacity exhausted; delete or expire records first")
        temp_path: Path | None = None
        try:
            with NamedTemporaryFile(dir=self.path.parent, suffix=".tmp", delete=False) as handle:
                temp_path = Path(handle.name)
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_path, self.path)
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)

    def _active(self, now: datetime) -> list[MemoryRecord]:
        records = self._read(now)
        active = [record for record in records if self._validate(record, now) > now]
        if len(active) != len(records):
            self._write(active)
            log.info("memory.expired", extra={
                "event": "memory.expired", "record_count": len(records) - len(active),
            })
        return active

    def put(self, record: MemoryRecord, *, correlation_id: str | None = None) -> None:
        with self._locked():
            now = self._clock()
            try:
                if self._validate(record, now) <= now:
                    raise MemoryPolicyError("Expired task memory cannot be admitted")
                records = self._active(now)
                existing = next((item for item in records if item.memory_id == record.memory_id), None)
                if existing is not None:
                    if existing != record:
                        raise MemoryPolicyError("Task memory is immutable until deletion or expiry")
                    return
                self._write([*records, record])
            except MemoryPolicyError as exc:
                log.warning("memory.refused", extra={
                    "event": "memory.refused", "correlation_id": correlation_id,
                    "error_type": type(exc).__name__,
                })
                raise
            log.info("memory.saved", extra={
                "event": "memory.saved", "correlation_id": correlation_id,
                "classification": record.classification, "record_count": len(records) + 1,
            })

    def get(self, memory_id: str, *, scope: str, owner: str) -> MemoryRecord | None:
        with self._locked():
            return next((record for record in self._active(self._clock())
                         if (record.memory_id, record.scope, record.owner) == (memory_id, scope, owner)), None)

    def delete(self, memory_id: str, *, scope: str, owner: str) -> bool:
        with self._locked():
            records = self._active(self._clock())
            remaining = [record for record in records
                         if (record.memory_id, record.scope, record.owner) != (memory_id, scope, owner)]
            if len(remaining) == len(records):
                return False
            self._write(remaining)
            log.info("memory.deleted", extra={"event": "memory.deleted"})
            return True

    def prune(self) -> int:
        with self._locked():
            now = self._clock()
            count = len(self._read(now))
            return count - len(self._active(now))


class AgentResultCache:
    """Bounded transient result cache; eviction never deletes durable evidence."""

    def __init__(
        self, *, policy: MemoryPolicy | None = None, clock: Callable[[], datetime] | None = None,
    ) -> None:
        self.policy = policy or MemoryPolicy()
        self._clock = clock or (lambda: datetime.now(UTC))
        self._lock = RLock()
        self._records: OrderedDict[str, tuple[datetime, AgentResult, int]] = OrderedDict()
        self._bytes = 0

    def _remove(self, run_id: str) -> None:
        self._bytes -= self._records.pop(run_id)[2]

    def _expire(self) -> None:
        now = self._clock()
        for run_id, (expires, _, _) in list(self._records.items()):
            if expires <= now:
                self._remove(run_id)

    def put(self, run_id: str, result: AgentResult) -> None:
        with self._lock:
            self._expire()
            if run_id in self._records:
                self._remove(run_id)
            size = len(result.model_dump_json().encode("utf-8")) + len(run_id.encode("utf-8"))
            if size > self.policy.max_bytes:
                log.warning("agent.result.not_cached", extra={
                    "event": "agent.result.not_cached", "reason": "byte_capacity",
                })
                return
            while self._records and (
                len(self._records) >= self.policy.max_records or self._bytes + size > self.policy.max_bytes
            ):
                self._remove(next(iter(self._records)))
            self._records[run_id] = (
                self._clock() + timedelta(seconds=self.policy.ttl_seconds), result.model_copy(deep=True), size,
            )
            self._bytes += size

    def get(self, run_id: str) -> AgentResult | None:
        with self._lock:
            self._expire()
            item = self._records.get(run_id)
            return item[1].model_copy(deep=True) if item else None


from eoip.moonshot.streaming_agent_memory import (  # noqa: E402
    DualTimelineIndex,
    MemoryEventType,
    StreamingMemoryIngester,
    TemporalMemoryEvent,
)


class StreamingAgentMemory:
    """KGR-G-014: Streaming dual-timeline agent memory integrated with local memory policy."""

    def __init__(
        self,
        *,
        max_buffer_size: int = 10000,
        policy: MemoryPolicy | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self.policy = policy or MemoryPolicy()
        self._clock = clock or (lambda: datetime.now(UTC))
        self.ingester = StreamingMemoryIngester(max_buffer_size=max_buffer_size)

    def record_memory(
        self,
        agent_id: str,
        content: dict[str, Any],
        *,
        event_id: str | None = None,
        event_type: MemoryEventType = MemoryEventType.OBSERVATION,
        event_time: float | None = None,
        salience: float = 1.0,
        ttl_seconds: int | None = None,
    ) -> TemporalMemoryEvent:
        now_ts = self._clock().timestamp()
        event = TemporalMemoryEvent(
            event_id=event_id or f"mem-{agent_id}-{now_ts}-{len(self.ingester.index._by_id)}",
            agent_id=agent_id,
            event_type=event_type,
            content=content,
            event_time=event_time if event_time is not None else now_ts,
            ingestion_time=now_ts,
            salience=salience,
            ttl_seconds=ttl_seconds or self.policy.ttl_seconds,
        )
        return self.ingester.ingest(event)

    def query_dual_timeline(
        self,
        *,
        event_time_range: tuple[float, float] | None = None,
        ingestion_time_range: tuple[float, float] | None = None,
    ) -> list[TemporalMemoryEvent]:
        events = list(self.ingester.index._by_id.values())
        if event_time_range is not None:
            start, end = event_time_range
            events = [e for e in events if start <= e.event_time <= end]
        if ingestion_time_range is not None:
            start, end = ingestion_time_range
            events = [e for e in events if start <= e.ingestion_time <= end]
        return events

    def get_agent_context(
        self,
        agent_id: str,
        *,
        max_events: int = 50,
        min_salience: float = 0.1,
    ) -> list[TemporalMemoryEvent]:
        return self.ingester.query_context(agent_id, max_events=max_events, min_salience=min_salience)

