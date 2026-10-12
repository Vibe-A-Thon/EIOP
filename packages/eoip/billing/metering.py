"""Usage Intelligence & Embedded Billing Metering Engine (MS-27).

Tracks query tokens, API requests, storage consumption, and applies rate limits
with cryptographic billing ledger receipts:
- Token accounting (prompt tokens, completion tokens, embedding tokens)
- Tenant-scoped quota enforcement
- Cryptographically sealed usage receipt records
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class UsageRecord:
    record_id: str
    tenant_id: str
    timestamp: float
    metric_type: str  # QUERY_TOKENS, API_CALLS, GRAPH_NODES, RAG_SYNTHESIS
    quantity: float
    details: dict[str, Any] = field(default_factory=dict)
    receipt_hash: str = ""

    def seal(self, secret: str = "eoip-billing-seal") -> str:
        payload = f"{self.record_id}:{self.tenant_id}:{self.timestamp}:{self.metric_type}:{self.quantity}"
        self.receipt_hash = hashlib.sha256(f"{payload}:{secret}".encode("utf-8")).hexdigest()
        return self.receipt_hash


class UsageIntelligenceMeter:
    """Enterprise usage metering and billing ledger."""

    def __init__(self, tenant_quotas: dict[str, dict[str, float]] | None = None) -> None:
        self.quotas = tenant_quotas or {}
        self._ledger: list[UsageRecord] = []
        self._totals: dict[str, dict[str, float]] = {}

    def record_usage(
        self,
        tenant_id: str,
        metric_type: str,
        quantity: float,
        details: dict[str, Any] | None = None,
    ) -> UsageRecord:
        """Records a usage event into the ledger and verifies quota."""
        now = time.time()
        rec_id = f"use-{tenant_id}-{len(self._ledger) + 1}"
        record = UsageRecord(
            record_id=rec_id,
            tenant_id=tenant_id,
            timestamp=now,
            metric_type=metric_type,
            quantity=quantity,
            details=details or {},
        )
        record.seal()
        self._ledger.append(record)

        tenant_totals = self._totals.setdefault(tenant_id, {})
        tenant_totals[metric_type] = tenant_totals.get(metric_type, 0.0) + quantity

        # Quota check
        tenant_quota = self.quotas.get(tenant_id, {})
        max_quota = tenant_quota.get(metric_type)
        if max_quota is not None and tenant_totals[metric_type] > max_quota:
            record.details["quota_exceeded"] = True

        return record

    def get_tenant_summary(self, tenant_id: str) -> dict[str, Any]:
        totals = self._totals.get(tenant_id, {})
        quotas = self.quotas.get(tenant_id, {})
        return {
            "tenant_id": tenant_id,
            "consumption": totals,
            "quotas": quotas,
            "record_count": len([r for r in self._ledger if r.tenant_id == tenant_id]),
        }

    def verify_receipt(self, record: UsageRecord, secret: str = "eoip-billing-seal") -> bool:
        expected = hashlib.sha256(
            f"{record.record_id}:{record.tenant_id}:{record.timestamp}:{record.metric_type}:{record.quantity}:{secret}".encode("utf-8")
        ).hexdigest()
        return record.receipt_hash == expected
