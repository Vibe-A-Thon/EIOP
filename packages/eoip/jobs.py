"""Durable single-worker queue on the shared application volume."""

import json
import os
from pathlib import Path
from uuid import UUID, uuid4

from eoip.contracts.source_event import utc_now_iso


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(f".{uuid4().hex}.tmp")
    with temporary.open("w", encoding="utf-8") as output:
        json.dump(value, output, ensure_ascii=False)
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, path)


class JobQueue:
    def __init__(self, root):
        self.root = Path(root) / "jobs"
        self.root.mkdir(parents=True, exist_ok=True)

    def submit(self, kind, payload=None):
        job_id = str(uuid4())
        job = {
            "job_id": job_id,
            "kind": kind,
            "status": "PENDING",
            "created_at": utc_now_iso(),
            "payload": payload,
        }
        write_json(self.root / f"{job_id}.json", job)
        return {key: value for key, value in job.items() if key != "payload"}

    def get(self, job_id):
        UUID(job_id)
        return json.loads((self.root / f"{job_id}.json").read_text(encoding="utf-8"))

    def list(self):
        jobs = [json.loads(p.read_text(encoding="utf-8")) for p in self.root.glob("*.json")]
        return [
            {k: v for k, v in job.items() if k != "payload"}
            for job in sorted(jobs, key=lambda j: j["created_at"], reverse=True)[:100]
        ]
