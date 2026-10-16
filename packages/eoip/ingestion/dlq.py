"""Unified dead-letter envelope (FR-INGEST-005).

Every ingestion service writes rejected source records through
:func:`write_dlq_record` so the DLQ has one schema regardless of source:

- ``event_id`` / ``source_record_id`` / ``payload_hash`` — source identity
- ``source_system`` — source system name
- ``stage`` — pipeline stage that rejected the record (mapping/parsing/...)
- ``error_category`` — stable machine-readable category (mapping_error,
  parse_error, schema_drift, invalid_fact, ...)
- ``error`` / ``errors`` — safe human-readable message(s); never secrets
- ``run_id`` / ``correlation_id`` — ingestion run + request correlation
- ``replay_ref`` — captured raw event path when capture-first replay applies

Replay support is keyed off ``source_system`` + ``error_category``; the
admin replay endpoint validates the captured event before resubmitting.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path


def write_dlq_record(
    dlq_root: str | Path,
    event,
    error: str | Iterable[str],
    *,
    stage: str,
    error_category: str = "mapping_error",
    run_id: str | None = None,
    correlation_id: str | None = None,
    replay_ref: str | None = None,
    mapping_version: str | None = None,
    retry_state: str | None = "UNPROCESSED",
    remediation_note: str | None = None,
    stack_trace: str | None = None,
    extra: dict | None = None,
) -> Path:
    """Write one DLQ record idempotently; returns the record path."""
    root = Path(dlq_root)
    root.mkdir(parents=True, exist_ok=True)
    destination = root / f"{event.event_id}.json"
    if isinstance(error, str):
        record: dict = {"error": error}
    else:
        record = {"errors": list(error)}
    record.update(
        {
            "event_id": event.event_id,
            "source_system": event.source_system,
            "source_record_id": event.source_record_id,
            "payload_hash": event.payload_hash,
            "stage": stage,
            "error_category": error_category,
        }
    )
    if run_id:
        record["run_id"] = run_id
    if correlation_id:
        record["correlation_id"] = correlation_id
    if replay_ref:
        record["replay_ref"] = replay_ref
    if mapping_version:
        record["mapping_version"] = mapping_version
    if retry_state:
        record["retry_state"] = retry_state
    if remediation_note:
        record["remediation_note"] = remediation_note
    if stack_trace:
        record["stack_trace"] = stack_trace
    if hasattr(event, "model_dump"):
        record["source_event"] = event.model_dump(mode="json")
    elif isinstance(event, dict):
        record["source_event"] = event
    if extra:
        record.update(extra)
    if not destination.exists():
        destination.write_text(
            json.dumps(record, sort_keys=True, indent=2), encoding="utf-8"
        )
    return destination
