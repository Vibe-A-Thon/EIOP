"""Local EKAF scheduling controls for baseline, poll, reconcile and replay jobs."""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path
from typing import Literal

from eoip.connectors.registry import SourceRegistry
from eoip.contracts.source_event import utc_now_iso
from eoip.jobs import JobQueue, write_json
from pydantic import BaseModel, ConfigDict, Field

AcquisitionOperation = Literal["BASELINE", "POLL", "RECONCILE", "REPLAY"]
BaselineStage = Literal[
    "CREATED",
    "DISCOVERING",
    "FETCHING",
    "MAPPING",
    "VALIDATING",
    "MUTATING",
    "VERIFYING",
    "COMPLETE",
    "FAILED",
]


class AcquisitionPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    max_concurrency: int = Field(default=1, ge=1, le=16)
    rate_limit_per_minute: int = Field(default=60, ge=1, le=60_000)
    paused: bool = False


class AcquisitionScheduler:
    """Admission controller over the durable job queue; execution remains worker-owned."""

    def __init__(self, root: str | Path, registry: SourceRegistry, queue: JobQueue) -> None:
        self.root = Path(root)
        self.registry = registry
        self.queue = queue
        self.policy_path = self.root / "state" / "acquisition-policies.json"
        self._lock = threading.RLock()

    def policy(self, source_id: str) -> AcquisitionPolicy:
        self.registry.get(source_id)
        return self._policies().get(source_id, AcquisitionPolicy())

    def set_policy(self, source_id: str, policy: AcquisitionPolicy) -> AcquisitionPolicy:
        self.registry.get(source_id)
        with self._lock:
            policies = self._policies()
            policies[source_id] = policy
            write_json(
                self.policy_path,
                {"schema_version": "1.0", "sources": {key: value.model_dump() for key, value in policies.items()}},
            )
        return policy

    def pause(self, source_id: str) -> AcquisitionPolicy:
        return self.set_policy(source_id, self.policy(source_id).model_copy(update={"paused": True}))

    def resume(self, source_id: str) -> AcquisitionPolicy:
        return self.set_policy(source_id, self.policy(source_id).model_copy(update={"paused": False}))

    def submit(
        self,
        source_id: str,
        operation: AcquisitionOperation,
        *,
        checkpoint: str | None = None,
        event_ids: list[str] | None = None,
        dry_run: bool = False,
        correlation_id: str | None = None,
    ) -> dict:
        with self._lock:
            self._check_admission(source_id, operation, event_ids)
            return self.queue.submit(
                "SOURCE_OPERATION",
                {
                    "source_id": source_id,
                    "operation": operation,
                    "checkpoint": checkpoint,
                    "event_ids": event_ids or [],
                    "dry_run": dry_run,
                },
                correlation_id=correlation_id,
            )

    def readmit(self, job_id: str, *, correlation_id: str | None = None) -> dict:
        with self._lock:
            job = self.queue.get(job_id)
            if job["status"] != "HELD" or job["kind"] != "SOURCE_OPERATION":
                raise RuntimeError("Only held source operation jobs can be re-admitted")
            payload = job["payload"]
            if not isinstance(payload, dict) or not isinstance(payload.get("source_id"), str):
                raise TypeError("source_id is required for source operation recovery")
            self._check_admission(
                payload["source_id"], payload.get("operation"), payload.get("event_ids")
            )
            return self.queue.readmit(job_id, correlation_id=correlation_id)

    def _check_admission(self, source_id, operation, event_ids):
        if operation not in {"BASELINE", "POLL", "RECONCILE", "REPLAY"}:
            raise ValueError("unsupported source acquisition operation")
        source = self.registry.get(source_id)
        if not source.enabled:
            raise RuntimeError("source is disabled")
        policy = self.policy(source_id)
        if policy.paused:
            raise RuntimeError("source is paused")
        if operation == "POLL" and not source.capabilities.polling:
            raise ValueError("source does not declare polling capability")
        if operation == "RECONCILE" and not source.capabilities.reconciliation:
            raise ValueError("source does not declare reconciliation capability")
        if operation == "REPLAY" and not source.capabilities.replay:
            raise ValueError("source does not declare replay capability")
        if operation == "REPLAY" and not event_ids:
            raise ValueError("event_ids are required for replay")

        jobs = self._source_jobs(source_id)
        active = [job for job in jobs if job.get("status") in {"PENDING", "RUNNING"}]
        if len(active) >= policy.max_concurrency:
            raise RuntimeError("source concurrency limit reached")
        cutoff = time.time() - 60
        recent = [job for job in jobs if job.get("status") != "HELD" and self._created_epoch(job) >= cutoff]
        if len(recent) >= policy.rate_limit_per_minute:
            raise RuntimeError("source rate limit reached")

    def _policies(self) -> dict[str, AcquisitionPolicy]:
        if not self.policy_path.exists():
            return {}
        document = json.loads(self.policy_path.read_text(encoding="utf-8"))
        if document.get("schema_version") != "1.0" or not isinstance(document.get("sources"), dict):
            raise ValueError("invalid acquisition policy document")
        return {key: AcquisitionPolicy.model_validate(value) for key, value in document["sources"].items()}

    def _source_jobs(self, source_id: str) -> list[dict]:
        jobs = []
        for path in self.queue.root.glob("*.json"):
            job = json.loads(path.read_text(encoding="utf-8"))
            payload = job.get("payload") or {}
            if job.get("kind") == "SOURCE_OPERATION" and payload.get("source_id") == source_id:
                jobs.append(job)
        return jobs

    @staticmethod
    def _created_epoch(job: dict) -> float:
        from datetime import datetime

        try:
            admitted_at = (job.get("recovery") or {}).get("readmitted_at", job["created_at"])
            return datetime.fromisoformat(admitted_at).timestamp()
        except (KeyError, TypeError, ValueError):
            return 0.0


class BaselineController:
    """Durable baseline state machine and restart manifest (G2-T0201..0203)."""

    _ORDER = (
        "CREATED",
        "DISCOVERING",
        "FETCHING",
        "MAPPING",
        "VALIDATING",
        "MUTATING",
        "VERIFYING",
        "COMPLETE",
    )

    def __init__(self, path: str | Path, source_id: str, metadata: dict | None = None) -> None:
        self.path = Path(path)
        self.source_id = source_id
        if not self.path.exists():
            self._write(
                {
                    "schema_version": "1.0",
                    "source_id": source_id,
                    "stage": "CREATED",
                    "history": [{"stage": "CREATED", "at": utc_now_iso()}],
                    "metadata": metadata or {},
                    "checkpoint": None,
                    "counts": {},
                    "failures": [],
                }
            )

    def transition(self, stage: BaselineStage, **updates) -> dict:
        state = self.read()
        current = state["stage"]
        if stage != "FAILED":
            expected = self._ORDER[min(self._ORDER.index(current) + 1, len(self._ORDER) - 1)]
            if stage != expected and not (current == stage == "COMPLETE"):
                raise ValueError(f"invalid baseline transition: {current} -> {stage}")
        state.update(updates, stage=stage)
        state["history"].append({"stage": stage, "at": utc_now_iso()})
        self._write(state)
        return state

    def read(self) -> dict:
        state = json.loads(self.path.read_text(encoding="utf-8"))
        if state.get("source_id") != self.source_id:
            raise ValueError("baseline manifest source mismatch")
        return state

    def _write(self, state: dict) -> None:
        write_json(self.path, state)
