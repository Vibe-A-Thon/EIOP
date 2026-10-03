"""Persistent audit event sink (NFR-OPS-001).

Audit events are emitted to structured logs and persisted to a local
JSON-lines file for compliance review. Hidden chain-of-thought is never stored.
"""

from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path
from threading import Lock

from eoip.audit.redaction import redact_secrets
from eoip.contracts.audit import AuditEvent

log = logging.getLogger("eoip.audit")

# Token-shaped secrets that key-based redaction cannot catch inside free text
# (GitHub/GitLab PATs, fine-grained PATs, OpenAI-style keys, Slack tokens).
_TOKEN_PATTERN = re.compile(
    r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}"
    r"|sk-[A-Za-z0-9]{16,}|xox[baprs]-[A-Za-z0-9-]{10,})\b"
)


def _redact_tokens(value):
    if isinstance(value, str):
        return _TOKEN_PATTERN.sub("***REDACTED***", value)
    if isinstance(value, dict):
        return {key: _redact_tokens(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_redact_tokens(item) for item in value]
    return value


class AuditSink:
    def __init__(self, audit_dir: str | Path | None = None) -> None:
        self._dir = Path(audit_dir) if audit_dir else Path(os.getenv("EOIP_DATA_DIR", "/data")) / "audit"
        self._dir.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()

    def emit(self, event: AuditEvent, **extra) -> None:
        record = event.model_dump(exclude_none=True)
        record.update({k: v for k, v in extra.items() if v is not None})
        record = _redact_tokens(redact_secrets(record))

        log.info(
            "audit.event",
            extra={"event": "audit.event", **record},
        )

        line = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
        path = self._dir / "audit.jsonl"
        with self._lock, path.open("a", encoding="utf-8") as f:
            f.write(line)

    def read(self, *, limit: int = 100) -> list[dict]:
        path = self._dir / "audit.jsonl"
        if not path.exists():
            return []
        lines = path.read_text(encoding="utf-8").strip().splitlines()
        return [json.loads(line) for line in lines[-limit:]]
