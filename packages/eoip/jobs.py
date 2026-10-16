"""Durable single-worker queue on the shared application volume."""

import json
import os
import threading
from pathlib import Path
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


class JobQueue:
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
