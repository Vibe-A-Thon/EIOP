"""Background job queue, built-in worker, and lease manager (T-115 / D-05 / REVA-WK-015)."""

from __future__ import annotations

import json
import logging
import time
import uuid
from datetime import datetime, timedelta, timezone

from typing import Any, Dict, List, Optional
from collections.abc import Callable
from pydantic import BaseModel, Field

from reva.core.time import format_ts, parse_ts, utc_now_ms
from reva.kernel.events import dispatch_outbox
from reva.kernel.store import RevaStore

logger = logging.getLogger("reva.worker")


class Job(BaseModel):
    """Asynchronous background work item."""

    job_id: str
    tenant_id: str
    kind: str
    payload: Dict[str, Any]
    priority: int = 0
    status: str = "queued"
    lease_owner: Optional[str] = None
    lease_expires_at: Optional[str] = None
    attempts: int = 0
    progress: Optional[Dict[str, Any]] = None
    result_ref: Optional[str] = None
    error: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: str


JobHandler = Callable[[Job], Any]


def enqueue_job(
    store: RevaStore,
    tenant_id: str,
    kind: str,
    payload: Dict[str, Any],
    priority: int = 0,
) -> str:
    """Enqueue a job for asynchronous execution."""
    jid = f"job_{uuid.uuid4().hex}"
    now = format_ts(utc_now_ms())
    cur = store.conn.cursor()
    cur.execute(
        """
        INSERT INTO reva_jobs (
            job_id, tenant_id, kind, payload, priority, status, attempts, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, 'queued', 0, ?, ?)
        """,
        (jid, tenant_id, kind, json.dumps(payload), priority, now, now),
    )
    store.conn.commit()
    return jid


class JobWorker:
    """Built-in job runner leasing work with atomic status updates and retry backoff."""

    def __init__(self, store: RevaStore, worker_id: Optional[str] = None, lease_duration_s: int = 60) -> None:
        self.store = store
        self.worker_id = worker_id or f"worker_{uuid.uuid4().hex[:8]}"
        self.lease_duration_s = lease_duration_s
        self._handlers: Dict[str, JobHandler] = {}
        self._running = False

    def register(self, kind: str, handler: JobHandler) -> None:
        """Register a handler for a specific job kind."""
        self._handlers[kind] = handler

    def claim_job(self) -> Optional[Job]:
        """Claim the next highest priority queued or expired-lease job."""
        now = format_ts(utc_now_ms())
        cur = self.store.conn.cursor()

        # Find candidate
        cur.execute(
            """
            SELECT * FROM reva_jobs
            WHERE status = 'queued'
               OR (status = 'running' AND lease_expires_at IS NOT NULL AND lease_expires_at < ?)
            ORDER BY priority DESC, created_at ASC
            LIMIT 1
            """,
            (now,),
        )
        row = cur.fetchone()
        if not row:
            return None

        jid = row["job_id"]
        # Calculate new lease expiry
        lease_exp = format_ts(utc_now_ms() + timedelta(seconds=self.lease_duration_s))


        # Atomic claim
        cur.execute(
            """
            UPDATE reva_jobs
            SET status = 'running',
                lease_owner = ?,
                lease_expires_at = ?,
                attempts = attempts + 1,
                updated_at = ?
            WHERE job_id = ? AND (status = 'queued' OR lease_expires_at < ?)
            """,
            (self.worker_id, lease_exp, now, jid, now),
        )
        self.store.conn.commit()

        if cur.rowcount == 0:
            # Race condition lost to another worker
            return None

        # Fetch updated row
        updated = cur.execute("SELECT * FROM reva_jobs WHERE job_id = ?", (jid,)).fetchone()
        return Job(
            job_id=updated["job_id"],
            tenant_id=updated["tenant_id"],
            kind=updated["kind"],
            payload=json.loads(updated["payload"]),
            priority=updated["priority"],
            status=updated["status"],
            lease_owner=updated["lease_owner"],
            lease_expires_at=updated["lease_expires_at"],
            attempts=updated["attempts"],
            progress=json.loads(updated["progress"]) if updated["progress"] else None,
            result_ref=updated["result_ref"],
            error=json.loads(updated["error"]) if updated["error"] else None,
            created_at=updated["created_at"],
            updated_at=updated["updated_at"],
        )

    def execute_job(self, job: Job) -> bool:
        """Execute a claimed job and update terminal status."""
        handler = self._handlers.get(job.kind)
        cur = self.store.conn.cursor()
        now = format_ts(utc_now_ms())

        if not handler:
            cur.execute(
                """
                UPDATE reva_jobs
                SET status = 'failed',
                    error = ?,
                    updated_at = ?
                WHERE job_id = ?
                """,
                (json.dumps({"reason": f"No handler registered for kind {job.kind}"}), now, job.job_id),
            )
            self.store.conn.commit()
            return False

        try:
            result = handler(job)
            res_ref = result if isinstance(result, str) else None
            cur.execute(
                """
                UPDATE reva_jobs
                SET status = 'succeeded',
                    result_ref = ?,
                    updated_at = ?
                WHERE job_id = ?
                """,
                (res_ref, now, job.job_id),
            )
            self.store.conn.commit()
            return True
        except Exception as e:
            logger.exception("Job %s failed on attempt %d", job.job_id, job.attempts)
            is_terminal = job.attempts >= 5
            new_status = "failed" if is_terminal else "queued"
            cur.execute(
                """
                UPDATE reva_jobs
                SET status = ?,
                    error = ?,
                    updated_at = ?
                WHERE job_id = ?
                """,
                (new_status, json.dumps({"error": str(e), "attempts": job.attempts}), now, job.job_id),
            )
            self.store.conn.commit()
            return False

    def run_once(self) -> bool:
        """Process outbox events and claim and execute at most one job. Return True if work was done."""
        dispatched = dispatch_outbox(self.store)
        job = self.claim_job()
        if job:
            self.execute_job(job)
            return True
        return dispatched > 0

    def run_forever(self, poll_interval_s: float = 1.0) -> None:
        """Worker main loop."""
        self._running = True
        while self._running:
            did_work = self.run_once()
            if not did_work:
                time.sleep(poll_interval_s)

    def stop(self) -> None:
        self._running = False
