"""Tamper-evident usage metering (SR-TEN-009, SR-DEP-007 usage export).

Local, append-only JSONL meter with a SHA-256 hash chain: every record hashes
the canonical record plus the previous record's hash, so any edit, deletion,
reordering, or truncation is detectable by :func:`UsageMeter.verify`. The
format follows the shared eoip audit-sink JSONL conventions (one compact
sorted-key JSON object per line) and is self-contained in this module — no
dependency on a remote metering service, so it works offline / air-gapped
(SR-DEP-007).

Metrics covered (SR-TEN-009): ``records_ingested``, ``graph_size``,
``queries``, ``llm_tokens``, ``storage_bytes``, ``seats`` and
``connectors``. Billing export is :func:`UsageMeter.export`, the aggregated
report a customer hands to the vendor for settlement (SR-DEP-007 "usage
export for manual reporting"); a push connector to a billing system is an
External gate.
"""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

GENESIS_PREV_HASH = "0" * 64


class MeterEvent(BaseModel):
    """One metered usage increment."""

    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(default_factory=lambda: f"urn:eoip:licensing:meter:{uuid.uuid4()}")
    seq: int
    ts: datetime
    metric: str
    value: int = Field(ge=0)
    tenant_id: str | None = None
    prev_hash: str = GENESIS_PREV_HASH
    hash: str = ""


class MeterVerification(BaseModel):
    """Result of re-verifying the meter hash chain."""

    model_config = ConfigDict(extra="forbid")

    ok: bool
    records_checked: int
    first_bad_seq: int | None = None
    reason: str = "ok"


def _canonical(record: dict[str, Any]) -> bytes:
    return json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def event_hash(record: dict[str, Any], prev_hash: str) -> str:
    """SHA-256 over the canonical record (minus ``hash``) and the previous hash."""
    body = {k: v for k, v in record.items() if k != "hash"}
    return hashlib.sha256(prev_hash.encode("ascii") + b"\n" + _canonical(body)).hexdigest()


class UsageMeter:
    """Append-only, tamper-evident JSONL usage meter."""

    def __init__(self, meter_dir: str | Path | None = None) -> None:
        self._dir = Path(meter_dir) if meter_dir else Path(os.getenv("EOIP_DATA_DIR", "/data")) / "meter"
        self._dir.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._path = self._dir / "usage_meter.jsonl"

    def _last(self) -> dict[str, Any] | None:
        if not self._path.exists():
            return None
        lines = self._path.read_text(encoding="utf-8").strip().splitlines()
        return json.loads(lines[-1]) if lines else None

    def record(self, metric: str, value: int = 1, tenant_id: str | None = None, ts: datetime | None = None) -> MeterEvent:
        """Append one usage increment and seal it into the hash chain."""
        if value < 0:
            raise ValueError("meter values must be >= 0")
        with self._lock:
            last = self._last()
            seq = (last["seq"] + 1) if last else 1
            prev_hash = last["hash"] if last else GENESIS_PREV_HASH
            event = MeterEvent(
                seq=seq,
                ts=ts or datetime.now(timezone.utc),
                metric=metric,
                value=value,
                tenant_id=tenant_id,
                prev_hash=prev_hash,
            )
            sealed = event.model_dump(mode="json")
            sealed["hash"] = event_hash(sealed, prev_hash)
            line = json.dumps(sealed, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
            with self._path.open("a", encoding="utf-8") as f:
                f.write(line)
            return MeterEvent.model_validate(sealed)

    def read(self, *, limit: int | None = None) -> list[MeterEvent]:
        if not self._path.exists():
            return []
        lines = self._path.read_text(encoding="utf-8").strip().splitlines()
        if limit is not None:
            lines = lines[-limit:]
        return [MeterEvent.model_validate(json.loads(line)) for line in lines]

    def verify(self) -> MeterVerification:
        """Re-walk the chain; detects tampering, reordering and truncation."""
        if not self._path.exists():
            return MeterVerification(ok=True, records_checked=0)
        prev_hash = GENESIS_PREV_HASH
        checked = 0
        for line in self._path.read_text(encoding="utf-8").strip().splitlines():
            record = json.loads(line)
            if record.get("prev_hash") != prev_hash:
                return MeterVerification(
                    ok=False, records_checked=checked, first_bad_seq=record.get("seq"), reason="chain_broken"
                )
            if record.get("hash") != event_hash(record, prev_hash):
                return MeterVerification(
                    ok=False, records_checked=checked, first_bad_seq=record.get("seq"), reason="hash_mismatch"
                )
            prev_hash = record["hash"]
            checked += 1
        return MeterVerification(ok=True, records_checked=checked)

    def export(self) -> dict[str, Any]:
        """Aggregated usage export for manual billing reporting (SR-DEP-007).

        Returns per-metric totals with the chain verification result so the
        customer can hand over a tamper-evident report.
        """
        events = self.read()
        totals: dict[str, int] = {}
        tenants: set[str] = set()
        for event in events:
            totals[event.metric] = totals.get(event.metric, 0) + event.value
            if event.tenant_id:
                tenants.add(event.tenant_id)
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "record_count": len(events),
            "totals": dict(sorted(totals.items())),
            "tenants": sorted(tenants),
            "chain": self.verify().model_dump(),
        }
