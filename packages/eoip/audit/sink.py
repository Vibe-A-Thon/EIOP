"""Persistent audit event sink (NFR-OPS-001).

Audit events are emitted to structured logs and persisted to a local
JSON-lines file for compliance review. Hidden chain-of-thought is never stored.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from threading import Lock

from eoip.audit.redaction import redact_secrets
from eoip.contracts.audit import AuditEvent

log = logging.getLogger("eoip.audit")


class AuditSink:
    def __init__(self, audit_dir: str | Path | None = None) -> None:
        self._dir = Path(audit_dir) if audit_dir else Path(os.getenv("EOIP_DATA_DIR", "/data")) / "audit"
        self._dir.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()

    def emit(self, event: AuditEvent, **extra) -> None:
        record = event.model_dump(exclude_none=True)
        record.update({k: v for k, v in extra.items() if v is not None})
        record = redact_secrets(record)

        log.info(
            "audit.event",
            extra={"event": "audit.event", **record},
        )

        line = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
        path = self._dir / "audit.jsonl"
        with self._lock:
            with path.open("a", encoding="utf-8") as f:
                f.write(line)

    def read(self, *, limit: int = 100) -> list[dict]:
        path = self._dir / "audit.jsonl"
        if not path.exists():
            return []
        lines = path.read_text(encoding="utf-8").strip().splitlines()
        return [json.loads(line) for line in lines[-limit:]]
