"""Retention policies and automated expiry (SR-PRV-003).

A retention policy pins how long records of a given data class may live,
scoped by tenant and source. The ``RetentionEngine`` evaluates policies
against caller-supplied record metadata and returns expiry actions for
the job runner; legal-hold suspension is ADR-gated (hold workflows need a
compliance-store decision) — policies under an active hold are skipped by
default. Crypto-shredding of expired material at rest is External gate
(key-management integration in storage tooling).
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DataClass(str, Enum):
    RAW_CAPTURE = "raw_capture"
    GRAPH_ENTITY = "graph_entity"
    DERIVED = "derived"
    AUDIT = "audit"
    CONSENT = "consent"


class ExpiryAction(str, Enum):
    DELETE = "delete"
    ANONYMIZE = "anonymize"
    REVIEW = "review"


class RetentionPolicy(BaseModel):
    """Retention rule per data class, optionally per tenant/source (SR-PRV-003)."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="URN, e.g. urn:eoip:privacy:retention:<slug>")
    data_class: DataClass
    tenant_id: str | None = Field(default=None, description="None = platform-wide default")
    source: str | None = Field(default=None, description="None = all sources")
    retain_days: int = Field(ge=1)
    action: ExpiryAction = ExpiryAction.DELETE
    legal_hold: bool = Field(default=False, description="ADR-gated: when True, expiry is suspended")

    @field_validator("id")
    @classmethod
    def _urn(cls, value: str) -> str:
        if not value.startswith("urn:eoip:privacy:retention:"):
            raise ValueError("retention policy id must be urn:eoip:privacy:retention:<slug>")
        return value


class RetainableRecord(BaseModel):
    """Record metadata handed to the retention engine by the job runner."""

    model_config = ConfigDict(extra="forbid")

    ref: str
    data_class: DataClass
    tenant_id: str | None = None
    source: str | None = None
    ingested_at: str  # ISO-8601
    legal_hold: bool = False


class ExpiryDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    record_ref: str
    policy_id: str
    action: ExpiryAction
    expired: bool
    reason: str = ""


def _parse_ts(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.replace(tzinfo=UTC)


class RetentionEngine:
    """Matches records to policies and decides expiry (SR-PRV-003)."""

    def __init__(self, policies: list[RetentionPolicy] | None = None, now: datetime | None = None):
        self._policies: list[RetentionPolicy] = list(policies or [])
        self._now = now

    def register(self, policy: RetentionPolicy) -> None:
        self._policies.append(policy)

    def _select(self, record: RetainableRecord) -> RetentionPolicy | None:
        """Most specific matching policy: tenant+source > tenant/source > default."""
        best: RetentionPolicy | None = None
        best_score = -1
        for p in self._policies:
            if p.data_class != record.data_class:
                continue
            if p.tenant_id not in (None, record.tenant_id) or p.source not in (None, record.source):
                continue
            score = (p.tenant_id is not None) + (p.source is not None)
            if score > best_score:
                best, best_score = p, score
        return best

    def decide(self, record: RetainableRecord, now: datetime | None = None) -> ExpiryDecision:
        policy = self._select(record)
        if policy is None:
            return ExpiryDecision(record_ref=record.ref, policy_id="", action=ExpiryAction.REVIEW, expired=False, reason="no matching policy")
        if policy.legal_hold or record.legal_hold:
            return ExpiryDecision(
                record_ref=record.ref,
                policy_id=policy.id,
                action=ExpiryAction.REVIEW,
                expired=False,
                reason="legal hold active (hold workflow itself is ADR-gated)",
            )
        now = now or self._now or datetime.now(UTC)
        age = now - _parse_ts(record.ingested_at)
        expired = age > timedelta(days=policy.retain_days)
        return ExpiryDecision(
            record_ref=record.ref,
            policy_id=policy.id,
            action=policy.action if expired else ExpiryAction.REVIEW,
            expired=expired,
            reason="expired" if expired else "within retention window",
        )

    def run_expiry(
        self,
        records: list[RetainableRecord],
        now: datetime | None = None,
        executor: dict[str, object] | None = None,
    ) -> list[ExpiryDecision]:
        """Evaluate a batch; optionally execute via ``executor[action](record)``."""
        decisions = [self.decide(record, now) for record in records]
        for record, decision in zip(records, decisions):
            if decision.expired and executor:
                fn = executor.get(decision.action.value)
                if callable(fn):
                    fn(record)
        return decisions
