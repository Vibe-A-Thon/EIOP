"""Persistent audit event sink (NFR-OPS-001, NFR-SEC-007).

Audit events are emitted to structured logs and persisted to a local
JSON-lines file for compliance review. Each record carries a SHA-256
hash chain linking it to the previous record, making the log
tamper-evident. Hidden chain-of-thought is never stored.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
from pathlib import Path
from threading import Lock

from eoip.audit.redaction import redact_secrets
from eoip.contracts.audit import AuditEvent

log = logging.getLogger("eoip.audit")

_TOKEN_PATTERN = re.compile(
    r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}"
    r"|sk-[A-Za-z0-9]{16,}|xox[baprs]-[A-Za-z0-9-]{10,})\b"
)

_GENESIS_HASH = hashlib.sha256(b"eoip:audit:genesis").hexdigest()


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
        self._prev_hash: str = self._load_chain_head()

    def _load_chain_head(self) -> str:
        """Load the hash of the last record to continue the chain."""
        path = self._dir / "audit.jsonl"
        if not path.exists():
            return _GENESIS_HASH
        try:
            lines = path.read_text(encoding="utf-8").strip().splitlines()
            if not lines:
                return _GENESIS_HASH
            last = json.loads(lines[-1])
            return last.get("_chain_hash", _GENESIS_HASH)
        except (json.JSONDecodeError, OSError):
            return _GENESIS_HASH

    def _compute_chain_hash(self, record_json: str, prev_hash: str) -> str:
        """SHA-256( prev_hash || canonical_record ) — tamper-evident link."""
        return hashlib.sha256(
            f"{prev_hash}:{record_json}".encode("utf-8")
        ).hexdigest()

    def emit(self, event: AuditEvent, **extra) -> None:
        record = event.model_dump(exclude_none=True)
        record.update({k: v for k, v in extra.items() if v is not None})
        record = _redact_tokens(redact_secrets(record))

        log.info(
            "audit.event",
            extra={"event": "audit.event", **record},
        )

        with self._lock:
            record_json = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            chain_hash = self._compute_chain_hash(record_json, self._prev_hash)
            record["_prev_hash"] = self._prev_hash
            record["_chain_hash"] = chain_hash
            self._prev_hash = chain_hash

            line = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
            path = self._dir / "audit.jsonl"
            with path.open("a", encoding="utf-8") as f:
                f.write(line)

    def read(self, *, limit: int = 100) -> list[dict]:
        path = self._dir / "audit.jsonl"
        if not path.exists():
            return []
        lines = path.read_text(encoding="utf-8").strip().splitlines()
        return [json.loads(line) for line in lines[-limit:]]

    def verify_chain_integrity(self) -> tuple[bool, int, str]:
        """Verify the full hash chain. Returns (valid, record_count, error_detail)."""
        path = self._dir / "audit.jsonl"
        if not path.exists():
            return True, 0, ""

        lines = path.read_text(encoding="utf-8").strip().splitlines()
        if not lines:
            return True, 0, ""

        prev_hash = _GENESIS_HASH
        for i, line in enumerate(lines):
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                return False, i, f"Record {i}: malformed JSON"

            stored_prev = record.get("_prev_hash", "")
            stored_chain = record.get("_chain_hash", "")

            if stored_prev != prev_hash:
                return False, i, f"Record {i}: prev_hash mismatch (expected {prev_hash[:16]}..., got {stored_prev[:16]}...)"

            payload = {k: v for k, v in record.items() if k not in ("_prev_hash", "_chain_hash")}
            payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            expected_hash = self._compute_chain_hash(payload_json, prev_hash)

            if stored_chain != expected_hash:
                return False, i, f"Record {i}: chain_hash mismatch — record has been tampered"

            prev_hash = stored_chain

        return True, len(lines), ""
