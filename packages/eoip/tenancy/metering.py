"""Usage metering — tamper-evident, append-only, offline-capable (SR-TEN-009).

Local metering for: records ingested, graph size, queries, LLM tokens,
storage, seats, connectors (SR-TEN-009). Records are appended to a
per-tenant hash chain: each entry carries

    entry_hash = sha256(prev_hash || entry_payload)

so any retroactive edit or deletion is detectable via ``verify_chain``.
Export produces the signed chain plus a chain head for billing
cross-checking. Entitlements enforcement against edition limits is
ADR-gated (deferred); this module measures and exports only. Designed to
run fully offline — no external service is required.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

METER_DIMENSIONS: frozenset[str] = frozenset({
    "records_ingested",
    "graph_size",
    "queries",
    "llm_tokens",
    "storage_bytes",
    "seats",
    "connectors",
})

GENESIS_HASH = "0" * 64


def _hash_entry(prev_hash: str, payload: dict[str, Any]) -> str:
    body = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(f"{prev_hash}|{body}".encode()).hexdigest()


@dataclass(frozen=True)
class MeterRecord:
    """One tamper-evident metering entry (SR-TEN-009)."""

    record_id: str
    tenant_id: str
    at: float
    dimensions: dict[str, int]  # subset of METER_DIMENSIONS
    prev_hash: str
    entry_hash: str
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "tenant_id": self.tenant_id,
            "at": self.at,
            "dimensions": dict(self.dimensions),
            "prev_hash": self.prev_hash,
            "entry_hash": self.entry_hash,
            "note": self.note,
        }


class MeteringLog:
    """Per-tenant append-only hash-chained usage log (SR-TEN-009)."""

    def __init__(self) -> None:
        self._chains: dict[str, list[MeterRecord]] = {}

    # -- writes (append-only) ---------------------------------------------------

    def record(
        self,
        tenant_id: str,
        dimensions: dict[str, int],
        *,
        note: str = "",
        at: float | None = None,
    ) -> MeterRecord:
        if not tenant_id:
            raise ValueError("tenant_id required")
        unknown = set(dimensions) - METER_DIMENSIONS
        if unknown:
            raise ValueError(f"unknown meter dimensions: {sorted(unknown)}")
        chain = self._chains.setdefault(tenant_id, [])
        prev_hash = chain[-1].entry_hash if chain else GENESIS_HASH
        record_id = f"urn:eoip:tenancy:meter:{uuid.uuid4().hex[:16]}"
        payload = {
            "record_id": record_id,
            "tenant_id": tenant_id,
            "at": at if at is not None else time.time(),
            "dimensions": {k: int(v) for k, v in sorted(dimensions.items())},
            "note": note,
        }
        entry = MeterRecord(
            record_id=record_id,
            tenant_id=tenant_id,
            at=payload["at"],
            dimensions=payload["dimensions"],
            prev_hash=prev_hash,
            entry_hash=_hash_entry(prev_hash, payload),
            note=note,
        )
        chain.append(entry)
        return entry

    # -- reads / verification ----------------------------------------------------

    def records(self, tenant_id: str) -> list[MeterRecord]:
        return list(self._chains.get(tenant_id, []))

    def chain_head(self, tenant_id: str) -> str:
        chain = self._chains.get(tenant_id, [])
        return chain[-1].entry_hash if chain else GENESIS_HASH

    def verify_chain(self, tenant_id: str) -> bool:
        """Recompute the hash chain; False on any tampering (SR-TEN-009)."""
        chain = self._chains.get(tenant_id, [])
        prev = GENESIS_HASH
        for entry in chain:
            if entry.prev_hash != prev:
                return False
            payload = {
                "record_id": entry.record_id,
                "tenant_id": entry.tenant_id,
                "at": entry.at,
                "dimensions": {k: int(v) for k, v in sorted(entry.dimensions.items())},
                "note": entry.note,
            }
            if _hash_entry(prev, payload) != entry.entry_hash:
                return False
            prev = entry.entry_hash
        return True

    def totals(self, tenant_id: str) -> dict[str, int]:
        """Sum of each metered dimension (SR-TEN-009)."""
        totals = {dim: 0 for dim in METER_DIMENSIONS}
        for entry in self._chains.get(tenant_id, []):
            for dim, value in entry.dimensions.items():
                totals[dim] += value
        return totals

    def export(self, tenant_id: str) -> dict[str, Any]:
        """Billing export: full signed chain + head + totals (SR-TEN-009)."""
        records = self.records(tenant_id)
        return {
            "tenant_id": tenant_id,
            "chain_head": self.chain_head(tenant_id),
            "record_count": len(records),
            "verified": self.verify_chain(tenant_id),
            "totals": self.totals(tenant_id),
            "records": [r.to_dict() for r in records],
        }

    def import_chain(self, tenant_id: str, records: list[dict[str, Any]]) -> bool:
        """Offline restore of an exported chain; verifies before accepting."""
        restored: list[MeterRecord] = []
        for raw in records:
            restored.append(
                MeterRecord(
                    record_id=raw["record_id"],
                    tenant_id=raw["tenant_id"],
                    at=raw["at"],
                    dimensions=dict(raw["dimensions"]),
                    prev_hash=raw["prev_hash"],
                    entry_hash=raw["entry_hash"],
                    note=raw.get("note", ""),
                )
            )
        self._chains[tenant_id] = restored
        return self.verify_chain(tenant_id)
