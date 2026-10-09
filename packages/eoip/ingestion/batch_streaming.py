"""Async Batch Processing & Streaming Ingestion — chunked batch ingest with backpressure-aware streaming."""

from __future__ import annotations

import queue
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable, Iterator


class BatchStatus(str, Enum):
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"
    CANCELLED = "CANCELLED"


class StreamMode(str, Enum):
    MICRO_BATCH = "MICRO_BATCH"
    RECORD_AT_A_TIME = "RECORD_AT_A_TIME"
    WINDOWED = "WINDOWED"


@dataclass
class BatchConfig:
    chunk_size: int = 500
    max_concurrent_chunks: int = 4
    retry_failed_chunks: bool = True
    max_retries: int = 3
    timeout_seconds: float = 300.0
    checkpoint_interval: int = 1000


@dataclass
class StreamConfig:
    mode: StreamMode = StreamMode.MICRO_BATCH
    micro_batch_size: int = 100
    micro_batch_interval_seconds: float = 5.0
    window_size_seconds: float = 60.0
    max_buffer_size: int = 10000
    backpressure_threshold: float = 0.8


@dataclass
class BatchJob:
    job_id: str
    source: str
    status: BatchStatus = BatchStatus.QUEUED
    total_records: int = 0
    processed_records: int = 0
    failed_records: int = 0
    chunks_total: int = 0
    chunks_completed: int = 0
    chunks_failed: int = 0
    started_at: str | None = None
    completed_at: str | None = None
    errors: list[dict[str, Any]] = field(default_factory=list)
    checkpoint: int = 0

    @property
    def progress(self) -> float:
        if self.total_records == 0:
            return 0.0
        return self.processed_records / self.total_records

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        d["progress"] = round(self.progress, 4)
        return d


@dataclass
class StreamState:
    stream_id: str
    source: str
    active: bool = False
    records_ingested: int = 0
    records_buffered: int = 0
    records_dropped: int = 0
    batches_flushed: int = 0
    backpressure_active: bool = False
    started_at: str | None = None
    last_flush: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return d


class BatchProcessor:
    """Processes large datasets in configurable chunks with checkpointing."""

    def __init__(self, config: BatchConfig | None = None,
                 process_fn: Callable[[list[dict]], list[dict]] | None = None) -> None:
        self._config = config or BatchConfig()
        self._process_fn = process_fn or self._default_process
        self._jobs: dict[str, BatchJob] = {}
        self._lock = threading.Lock()

    def submit(self, source: str, records: list[dict[str, Any]]) -> BatchJob:
        job_id = uuid.uuid4().hex[:12]
        chunks_total = max(1, (len(records) + self._config.chunk_size - 1) // self._config.chunk_size)
        job = BatchJob(
            job_id=job_id, source=source,
            total_records=len(records), chunks_total=chunks_total,
        )
        with self._lock:
            self._jobs[job_id] = job

        threading.Thread(target=self._run_batch, args=(job, records), daemon=True).start()
        return job

    def get_job(self, job_id: str) -> BatchJob | None:
        return self._jobs.get(job_id)

    def cancel(self, job_id: str) -> bool:
        job = self._jobs.get(job_id)
        if job and job.status in (BatchStatus.QUEUED, BatchStatus.PROCESSING):
            job.status = BatchStatus.CANCELLED
            return True
        return False

    def list_jobs(self) -> list[dict[str, Any]]:
        return [j.to_dict() for j in self._jobs.values()]

    def _run_batch(self, job: BatchJob, records: list[dict[str, Any]]) -> None:
        job.status = BatchStatus.PROCESSING
        job.started_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        for i in range(0, len(records), self._config.chunk_size):
            if job.status == BatchStatus.CANCELLED:
                return

            chunk = records[i : i + self._config.chunk_size]
            retries = 0
            while retries <= self._config.max_retries:
                try:
                    results = self._process_fn(chunk)
                    job.processed_records += len(results)
                    job.chunks_completed += 1
                    job.checkpoint = job.processed_records
                    break
                except Exception as e:
                    retries += 1
                    if retries > self._config.max_retries:
                        job.failed_records += len(chunk)
                        job.chunks_failed += 1
                        job.errors.append({
                            "chunk_index": i // self._config.chunk_size,
                            "error": str(e), "records": len(chunk),
                        })

        job.completed_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        if job.chunks_failed == 0:
            job.status = BatchStatus.COMPLETED
        elif job.chunks_completed > 0:
            job.status = BatchStatus.PARTIAL
        else:
            job.status = BatchStatus.FAILED

    @staticmethod
    def _default_process(chunk: list[dict]) -> list[dict]:
        return chunk


class StreamIngester:
    """Streaming ingestion with micro-batching, windowing, and backpressure."""

    def __init__(self, config: StreamConfig | None = None,
                 flush_fn: Callable[[list[dict]], None] | None = None) -> None:
        self._config = config or StreamConfig()
        self._flush_fn = flush_fn or (lambda batch: None)
        self._streams: dict[str, StreamState] = {}
        self._buffers: dict[str, list[dict[str, Any]]] = {}
        self._lock = threading.Lock()
        self._timers: dict[str, threading.Timer] = {}

    def create_stream(self, source: str) -> StreamState:
        stream_id = uuid.uuid4().hex[:12]
        state = StreamState(stream_id=stream_id, source=source)
        with self._lock:
            self._streams[stream_id] = state
            self._buffers[stream_id] = []
        return state

    def start_stream(self, stream_id: str) -> bool:
        state = self._streams.get(stream_id)
        if not state:
            return False
        state.active = True
        state.started_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        if self._config.mode == StreamMode.MICRO_BATCH:
            self._schedule_flush(stream_id)
        return True

    def stop_stream(self, stream_id: str) -> bool:
        state = self._streams.get(stream_id)
        if not state:
            return False
        state.active = False
        timer = self._timers.pop(stream_id, None)
        if timer:
            timer.cancel()
        self._flush(stream_id)
        return True

    def ingest(self, stream_id: str, record: dict[str, Any]) -> bool:
        state = self._streams.get(stream_id)
        if not state or not state.active:
            return False

        with self._lock:
            buf = self._buffers.get(stream_id, [])
            if len(buf) >= self._config.max_buffer_size:
                if self._check_backpressure(stream_id):
                    state.records_dropped += 1
                    return False
            buf.append(record)
            self._buffers[stream_id] = buf
            state.records_buffered = len(buf)

        if self._config.mode == StreamMode.RECORD_AT_A_TIME:
            self._flush(stream_id)
        elif (self._config.mode == StreamMode.MICRO_BATCH
              and len(buf) >= self._config.micro_batch_size):
            self._flush(stream_id)

        return True

    def ingest_batch(self, stream_id: str, records: list[dict[str, Any]]) -> int:
        ingested = 0
        for rec in records:
            if self.ingest(stream_id, rec):
                ingested += 1
        return ingested

    def get_stream(self, stream_id: str) -> StreamState | None:
        return self._streams.get(stream_id)

    def list_streams(self) -> list[dict[str, Any]]:
        return [s.to_dict() for s in self._streams.values()]

    def _flush(self, stream_id: str) -> None:
        with self._lock:
            buf = self._buffers.get(stream_id, [])
            if not buf:
                return
            batch = list(buf)
            buf.clear()

        state = self._streams.get(stream_id)
        if state:
            try:
                self._flush_fn(batch)
                state.records_ingested += len(batch)
                state.batches_flushed += 1
                state.records_buffered = 0
                state.last_flush = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            except Exception:
                with self._lock:
                    self._buffers.setdefault(stream_id, []).extend(batch)

    def _check_backpressure(self, stream_id: str) -> bool:
        buf = self._buffers.get(stream_id, [])
        ratio = len(buf) / max(1, self._config.max_buffer_size)
        state = self._streams.get(stream_id)
        if state:
            state.backpressure_active = ratio >= self._config.backpressure_threshold
        return ratio >= 1.0

    def _schedule_flush(self, stream_id: str) -> None:
        def _timer_flush():
            state = self._streams.get(stream_id)
            if state and state.active:
                self._flush(stream_id)
                self._schedule_flush(stream_id)

        timer = threading.Timer(self._config.micro_batch_interval_seconds, _timer_flush)
        timer.daemon = True
        self._timers[stream_id] = timer
        timer.start()
