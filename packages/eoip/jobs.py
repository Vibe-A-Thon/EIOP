"""Durable queue and distributed jobs engine with leases, fencing, transactional outbox, and governed DLQ (CRA-031)."""

from __future__ import annotations

import json
import os
import re
import sqlite3
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from uuid import UUID, uuid4

from eoip.contracts.source_event import utc_now_iso


def write_json(path: Path, value, *, indent: int | None = None):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(f".{uuid4().hex}.tmp")
    with temporary.open("w", encoding="utf-8") as output:
        json.dump(value, output, ensure_ascii=False, indent=indent)
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, path)


class FencedWorkerError(RuntimeError):
    """Raised when an expired or revoked worker attempts to heartbeat, checkpoint or commit."""


# Secret redaction patterns for diagnostics (CRA-031.7, CRA-031.3)
_SECRET_PATTERNS = [
    re.compile(r"(Bearer\s+)[A-Za-z0-9_\-\.]+", re.IGNORECASE),
    re.compile(r"(password['\"]?\s*[:=]\s*['\"]?)[^,\s'\"]+", re.IGNORECASE),
    re.compile(r"((api_key|secret|token|client_secret|auth_token)['\"]?\s*[:=]\s*['\"]?)[^,\s'\"]+", re.IGNORECASE),
    re.compile(r"(Authorization:\s*)[^\r\n]+", re.IGNORECASE),
    re.compile(r"(https?://[^\s?]+[?&][^=]*?(?:token|key|password|auth)=)[^&\s]+", re.IGNORECASE),
    re.compile(r"(://[^:/@\s]+:)[^@\s]+@", re.IGNORECASE),
]


def redact_diagnostics(text: str) -> str:
    """Strip bearer credentials, passwords, tokens and secrets from diagnostic outputs."""
    redacted = text
    for pat in _SECRET_PATTERNS:
        redacted = pat.sub(r"\1[REDACTED]", redacted)
    return redacted


class DurableJobStore:
    """ACID transactional durable job queue with heartbeats, fencing, outbox, and governed DLQ."""

    def __init__(self, db_path: Path | str) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=10.0, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA busy_timeout = 5000;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    tenant_id TEXT,
                    kind TEXT,
                    status TEXT,
                    payload TEXT,
                    created_at TEXT,
                    started_at TEXT,
                    finished_at TEXT,
                    deadline_at TEXT,
                    attempts INTEGER DEFAULT 0,
                    max_retries INTEGER DEFAULT 3,
                    is_idempotent INTEGER DEFAULT 0,
                    checkpoint TEXT,
                    lease_holder TEXT,
                    lease_expires_at REAL,
                    fencing_token INTEGER DEFAULT 0,
                    error TEXT
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status_lease ON jobs (status, lease_expires_at);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_tenant ON jobs (tenant_id);")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS job_outbox (
                    outbox_id TEXT PRIMARY KEY,
                    job_id TEXT,
                    tenant_id TEXT,
                    event_type TEXT,
                    payload TEXT,
                    created_at TEXT,
                    published_at TEXT,
                    status TEXT DEFAULT 'PENDING'
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_outbox_status ON job_outbox (status);")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS governed_dlq (
                    dlq_id TEXT PRIMARY KEY,
                    job_id TEXT UNIQUE,
                    tenant_id TEXT,
                    reason TEXT,
                    attempt_count INTEGER,
                    error_diagnostics TEXT,
                    original_payload TEXT,
                    moved_at TEXT,
                    replayed_at TEXT,
                    replay_authority TEXT
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_dlq_tenant ON governed_dlq (tenant_id);")

    def submit(
        self,
        kind: str,
        payload: Optional[dict[str, Any]] = None,
        *,
        tenant_id: Optional[str] = None,
        is_idempotent: bool = False,
        max_retries: int = 3,
        deadline_seconds: Optional[float] = None,
    ) -> dict[str, Any]:
        """Submit a new durable job."""
        job_id = str(uuid4())
        now_iso = utc_now_iso()
        deadline_at = (
            datetime.fromtimestamp(time.time() + deadline_seconds, tz=timezone.utc).isoformat()
            if deadline_seconds
            else None
        )
        payload_json = json.dumps(payload or {})

        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO jobs (
                    job_id, tenant_id, kind, status, payload, created_at,
                    max_retries, is_idempotent, deadline_at, fencing_token
                ) VALUES (?, ?, ?, 'PENDING', ?, ?, ?, ?, ?, 0)
                """,
                (job_id, tenant_id, kind, payload_json, now_iso, max_retries, 1 if is_idempotent else 0, deadline_at),
            )

        return {
            "job_id": job_id,
            "tenant_id": tenant_id,
            "kind": kind,
            "status": "PENDING",
            "created_at": now_iso,
            "is_idempotent": is_idempotent,
            "max_retries": max_retries,
        }

    def claim_job(
        self,
        worker_id: str,
        lease_ttl_s: float = 30.0,
        tenant_id: Optional[str] = None,
    ) -> Optional[dict[str, Any]]:
        """Atomically claim a pending job or reclaim an expired lease with incremented fencing token."""
        now = time.time()
        conn = self._get_connection()
        try:
            conn.execute("BEGIN IMMEDIATE;")
            # Select candidate: either PENDING or RUNNING with expired lease
            query = """
                SELECT * FROM jobs
                WHERE (status = 'PENDING')
                   OR (status = 'RUNNING' AND lease_expires_at < ?)
            """
            params: list[Any] = [now]
            if tenant_id:
                query += " AND tenant_id = ?"
                params.append(tenant_id)

            query += " ORDER BY created_at ASC LIMIT 1;"
            cur = conn.execute(query, params)
            row = cur.fetchone()
            if not row:
                conn.execute("COMMIT;")
                return None

            job_id = row["job_id"]
            old_fence = row["fencing_token"]
            new_fence = old_fence + 1
            lease_expires = now + lease_ttl_s
            now_iso = utc_now_iso()

            update_cur = conn.execute(
                """
                UPDATE jobs
                SET status = 'RUNNING',
                    lease_holder = ?,
                    lease_expires_at = ?,
                    fencing_token = ?,
                    started_at = COALESCE(started_at, ?),
                    attempts = attempts + 1
                WHERE job_id = ? AND fencing_token = ?
                """,
                (worker_id, lease_expires, new_fence, now_iso, job_id, old_fence),
            )

            if update_cur.rowcount == 0:
                conn.execute("ROLLBACK;")
                return None

            conn.execute("COMMIT;")
            # Fetch updated row
            cur = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
            res = dict(cur.fetchone())
            res["payload"] = json.loads(res["payload"]) if res["payload"] else {}
            res["checkpoint"] = json.loads(res["checkpoint"]) if res["checkpoint"] else None
            return res
        except Exception:
            conn.execute("ROLLBACK;")
            raise
        finally:
            conn.close()

    def heartbeat(
        self,
        job_id: str,
        worker_id: str,
        fencing_token: int,
        lease_ttl_s: float = 30.0,
    ) -> None:
        """Send heartbeat extending lease TTL. Fences worker if token or lease holder changed."""
        now = time.time()
        new_expires = now + lease_ttl_s

        with self._get_connection() as conn:
            cur = conn.execute(
                """
                UPDATE jobs
                SET lease_expires_at = ?
                WHERE job_id = ? AND lease_holder = ? AND fencing_token = ? AND status = 'RUNNING'
                """,
                (new_expires, job_id, worker_id, fencing_token),
            )
            if cur.rowcount == 0:
                raise FencedWorkerError(
                    f"Heartbeat rejected: Worker '{worker_id}' is fenced on job '{job_id}' (token {fencing_token})"
                )

    def checkpoint(
        self,
        job_id: str,
        worker_id: str,
        fencing_token: int,
        state_data: dict[str, Any],
    ) -> None:
        """Persist intermediate checkpoint for resumed execution on lease reclamation."""
        state_json = json.dumps(state_data)
        with self._get_connection() as conn:
            cur = conn.execute(
                """
                UPDATE jobs
                SET checkpoint = ?
                WHERE job_id = ? AND lease_holder = ? AND fencing_token = ? AND status = 'RUNNING'
                """,
                (state_json, job_id, worker_id, fencing_token),
            )
            if cur.rowcount == 0:
                raise FencedWorkerError(
                    f"Checkpoint rejected: Worker '{worker_id}' is fenced on job '{job_id}' (token {fencing_token})"
                )

    def commit_job(
        self,
        job_id: str,
        worker_id: str,
        fencing_token: int,
        result: Optional[dict[str, Any]] = None,
        outbox_events: Optional[list[dict[str, Any]]] = None,
    ) -> None:
        """Commit job completion and transactionally persist outbox publication events (CRA-031.2, CRA-031.5)."""
        now_iso = utc_now_iso()
        conn = self._get_connection()
        try:
            conn.execute("BEGIN IMMEDIATE;")
            # Verify fence
            cur = conn.execute(
                """
                UPDATE jobs
                SET status = 'COMPLETED',
                    finished_at = ?,
                    lease_holder = NULL
                WHERE job_id = ? AND lease_holder = ? AND fencing_token = ? AND status = 'RUNNING'
                """,
                (now_iso, job_id, worker_id, fencing_token),
            )
            if cur.rowcount == 0:
                raise FencedWorkerError(
                    f"Commit rejected: Worker '{worker_id}' is fenced on job '{job_id}' (token {fencing_token})"
                )

            # Insert outbox events atomically
            if outbox_events:
                # Fetch tenant_id
                t_row = conn.execute("SELECT tenant_id FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
                tenant_id = t_row["tenant_id"] if t_row else None

                for evt in outbox_events:
                    outbox_id = str(uuid4())
                    conn.execute(
                        """
                        INSERT INTO job_outbox (outbox_id, job_id, tenant_id, event_type, payload, created_at, status)
                        VALUES (?, ?, ?, ?, ?, ?, 'PENDING')
                        """,
                        (outbox_id, job_id, tenant_id, evt.get("event_type", "JOB_COMPLETED"), json.dumps(evt.get("payload", {})), now_iso),
                    )

            conn.execute("COMMIT;")
        except Exception:
            try:
                conn.execute("ROLLBACK;")
            except Exception:
                pass
            raise
        finally:
            conn.close()

    def fail_job(
        self,
        job_id: str,
        worker_id: str,
        fencing_token: int,
        error_message: str,
        stack_trace: str,
        is_poison: bool = False,
    ) -> None:
        """Handle job failure. Moves poison or repeatedly failing non-idempotent jobs to governed DLQ."""
        redacted_trace = redact_diagnostics(stack_trace)
        redacted_err = redact_diagnostics(error_message)
        now_iso = utc_now_iso()

        conn = self._get_connection()
        try:
            conn.execute("BEGIN IMMEDIATE;")
            cur = conn.execute(
                "SELECT attempts, max_retries, is_idempotent, payload, tenant_id FROM jobs WHERE job_id = ? AND fencing_token = ?",
                (job_id, fencing_token),
            )
            row = cur.fetchone()
            if not row:
                raise FencedWorkerError(f"Fail rejected: Worker '{worker_id}' is fenced on job '{job_id}'")

            attempts = row["attempts"]
            max_retries = row["max_retries"]
            is_idempotent = bool(row["is_idempotent"])
            tenant_id = row["tenant_id"]
            payload = row["payload"]

            # Safe retry policy: Mutations are not blindly retried (CRA-031.4)
            should_dlq = is_poison or (not is_idempotent) or (attempts >= max_retries)

            if should_dlq:
                # Move to governed DLQ
                dlq_id = str(uuid4())
                reason = "POISON_PAYLOAD" if is_poison else ("NON_IDEMPOTENT_MUTATION_FAILURE" if not is_idempotent else "MAX_RETRIES_EXCEEDED")

                conn.execute(
                    """
                    INSERT OR REPLACE INTO governed_dlq (
                        dlq_id, job_id, tenant_id, reason, attempt_count,
                        error_diagnostics, original_payload, moved_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (dlq_id, job_id, tenant_id, reason, attempts, f"{redacted_err}\n{redacted_trace}", payload, now_iso),
                )
                conn.execute(
                    """
                    UPDATE jobs
                    SET status = 'DEAD_LETTER',
                        finished_at = ?,
                        error = ?,
                        lease_holder = NULL
                    WHERE job_id = ? AND fencing_token = ?
                    """,
                    (now_iso, redacted_err, job_id, fencing_token),
                )
            else:
                # Safe to retry: release lease and return to PENDING
                conn.execute(
                    """
                    UPDATE jobs
                    SET status = 'PENDING',
                        error = ?,
                        lease_holder = NULL
                    WHERE job_id = ? AND fencing_token = ?
                    """,
                    (redacted_err, job_id, fencing_token),
                )

            conn.execute("COMMIT;")
        except Exception:
            try:
                conn.execute("ROLLBACK;")
            except Exception:
                pass
            raise
        finally:
            conn.close()

    def cancel(self, job_id: str, cancelled_by: str, tenant_id: Optional[str] = None) -> dict[str, Any]:
        """Cancel a job, incrementing fencing token to fence any executing workers (CRA-031.5)."""
        now_iso = utc_now_iso()
        with self._get_connection() as conn:
            query = "SELECT * FROM jobs WHERE job_id = ?"
            params: list[Any] = [job_id]
            if tenant_id:
                query += " AND tenant_id = ?"
                params.append(tenant_id)

            row = conn.execute(query, params).fetchone()
            if not row:
                raise PermissionError("Job not found or cross-tenant access forbidden")

            conn.execute(
                """
                UPDATE jobs
                SET status = 'CANCELLED',
                    finished_at = ?,
                    fencing_token = fencing_token + 1,
                    lease_holder = NULL
                WHERE job_id = ?
                """,
                (now_iso, job_id),
            )
            return {"job_id": job_id, "status": "CANCELLED", "cancelled_by": cancelled_by}

    def replay_dlq(
        self,
        dlq_id: str,
        replay_authority: str,
        tenant_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Replay a governed DLQ item with audit authority (CRA-031.7, CRA-031.A)."""
        if not replay_authority:
            raise PermissionError("Replay authority required to requeue DLQ items")

        now_iso = utc_now_iso()
        conn = self._get_connection()
        try:
            conn.execute("BEGIN IMMEDIATE;")
            query = "SELECT * FROM governed_dlq WHERE dlq_id = ?"
            params: list[Any] = [dlq_id]
            if tenant_id:
                query += " AND tenant_id = ?"
                params.append(tenant_id)

            row = conn.execute(query, params).fetchone()
            if not row:
                raise PermissionError("DLQ item not found or cross-tenant access forbidden")

            job_id = row["job_id"]

            # Record replay audit
            conn.execute(
                """
                UPDATE governed_dlq
                SET replayed_at = ?,
                    replay_authority = ?
                WHERE dlq_id = ?
                """,
                (now_iso, replay_authority, dlq_id),
            )

            # Reset job to PENDING
            conn.execute(
                """
                UPDATE jobs
                SET status = 'PENDING',
                    attempts = 0,
                    lease_holder = NULL,
                    fencing_token = fencing_token + 1
                WHERE job_id = ?
                """,
                (job_id,),
            )
            conn.execute("COMMIT;")
            return {"dlq_id": dlq_id, "job_id": job_id, "status": "REQUEUED", "replayed_by": replay_authority}
        except Exception:
            try:
                conn.execute("ROLLBACK;")
            except Exception:
                pass
            raise
        finally:
            conn.close()

    def get_job(self, job_id: str, tenant_id: Optional[str] = None) -> dict[str, Any]:
        """Retrieve job record enforcing tenant isolation."""
        with self._get_connection() as conn:
            cur = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
            row = cur.fetchone()
            if not row:
                raise KeyError(f"Job '{job_id}' not found")
            res = dict(row)
            if tenant_id and res.get("tenant_id") and res["tenant_id"] != tenant_id:
                raise PermissionError("Cross-tenant job access forbidden")
            res["payload"] = json.loads(res["payload"]) if res["payload"] else {}
            res["checkpoint"] = json.loads(res["checkpoint"]) if res["checkpoint"] else None
            return res

    def list_dlq(self, tenant_id: Optional[str] = None) -> list[dict[str, Any]]:
        """List governed DLQ entries."""
        with self._get_connection() as conn:
            query = "SELECT * FROM governed_dlq"
            params: list[Any] = []
            if tenant_id:
                query += " WHERE tenant_id = ?"
                params.append(tenant_id)
            query += " ORDER BY moved_at DESC"
            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]

    def list_outbox(self, status: str = "PENDING") -> list[dict[str, Any]]:
        """List pending outbox events."""
        with self._get_connection() as conn:
            rows = conn.execute("SELECT * FROM job_outbox WHERE status = ? ORDER BY created_at ASC", (status,)).fetchall()
            return [dict(r) for r in rows]


class JobQueue:
    """Original file-based job queue for backward compatibility."""

    def __init__(self, root):
        self.root = Path(root) / "jobs"
        self.root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()

    def submit(self, kind, payload=None, *, correlation_id=None, tenant_id=None, created_by=None):
        job_id = str(uuid4())
        job = {
            "job_id": job_id,
            "kind": kind,
            "status": "PENDING",
            "created_at": utc_now_iso(),
            "correlation_id": correlation_id or str(uuid4()),
            "tenant_id": tenant_id,
            "created_by": created_by,
            "payload": payload,
        }
        write_json(self.root / f"{job_id}.json", job)
        return {key: value for key, value in job.items() if key != "payload"}

    def get(self, job_id, *, tenant_id=None):
        UUID(job_id)
        job = json.loads((self.root / f"{job_id}.json").read_text(encoding="utf-8"))
        if tenant_id and job.get("tenant_id") and job["tenant_id"] != tenant_id:
            raise PermissionError("Cross-tenant job access forbidden")
        return job

    def cancel(self, job_id, *, tenant_id=None):
        with self._lock:
            job = self.get(job_id, tenant_id=tenant_id)
            if job["status"] == "RUNNING":
                raise RuntimeError("Running jobs cannot be cancelled safely")
            if job["status"] in {"PENDING", "HELD"}:
                job.update(status="CANCELLED", finished_at=utc_now_iso())
                write_json(self.root / f"{job_id}.json", job)
            return {key: value for key, value in job.items() if key != "payload"}

    def readmit(self, job_id, *, correlation_id=None, tenant_id=None):
        with self._lock:
            job = self.get(job_id, tenant_id=tenant_id)
            if job["status"] != "HELD":
                raise RuntimeError("Only held recovery jobs can be re-admitted")
            if not isinstance(job.get("recovery"), dict):
                raise TypeError("Held job lacks recovery metadata")
            now = utc_now_iso()
            job.update(status="PENDING", attempts=0, correlation_id=correlation_id or str(uuid4()))
            job["recovery"] = {**job["recovery"], "readmitted_at": now}
            for key in ("started_at", "finished_at", "next_attempt", "error", "result"):
                job.pop(key, None)
            write_json(self.root / f"{job_id}.json", job)
            return {key: value for key, value in job.items() if key != "payload"}

    def list(self, *, tenant_id=None):
        jobs = [json.loads(p.read_text(encoding="utf-8")) for p in self.root.glob("*.json")]
        if tenant_id:
            jobs = [j for j in jobs if not j.get("tenant_id") or j.get("tenant_id") == tenant_id]
        return [
            {k: v for k, v in job.items() if k != "payload"}
            for job in sorted(jobs, key=lambda j: j["created_at"], reverse=True)[:100]
        ]
