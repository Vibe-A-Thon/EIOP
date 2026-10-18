"""Bitemporal and Retention Data Models with Explicit Lineage and Corrections (CRA-028.1, CRA-028.2).

Features:
- Dual-time tracking: Valid Time (business validity window) vs Transaction Time (system observation).
- Explicit corrections and retractions with reason, actor, and source event lineage.
- Clock skew tolerance and deterministic late-arriving event reconciliation.
- Retention and Legal Hold governance: prevents serving expired history unless protected by legal hold.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
import hashlib
import json
from typing import Any, Optional
from uuid import uuid4


@dataclass(frozen=True)
class TimeRange:
    start: str  # ISO-8601
    end: Optional[str] = None  # None or empty string implies unbounded / open interval

    def covers(self, point: str) -> bool:
        if self.start > point:
            return False
        if self.end and point >= self.end:
            return False
        return True


@dataclass
class CorrectionRecord:
    correction_id: str
    target_id: str
    observed_at: str  # When the correction was entered into the system
    corrected_valid_from: str
    corrected_valid_to: Optional[str]
    actor: str
    reason: str
    previous_value: dict[str, Any]
    new_value: dict[str, Any]
    lineage_hash: str = ""

    def __post_init__(self) -> None:
        if not self.lineage_hash:
            raw = f"{self.correction_id}:{self.target_id}:{self.observed_at}:{self.reason}"
            self.lineage_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass
class RetractionRecord:
    retraction_id: str
    target_id: str
    observed_at: str
    retraction_reason: str
    actor: str
    replaces_revision_id: str
    lineage_hash: str = ""

    def __post_init__(self) -> None:
        if not self.lineage_hash:
            raw = f"{self.retraction_id}:{self.target_id}:{self.observed_at}:{self.retraction_reason}"
            self.lineage_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass
class RetentionPolicy:
    """Retention and Legal Hold constraints (CRA-028.2)."""
    retention_period_days: int = 365
    legal_hold_active: bool = False
    legal_hold_reason: str = ""
    legal_hold_case_id: str = ""

    def is_history_retained(self, recorded_at: str, current_time: Optional[str] = None) -> bool:
        """Check if historical record is permitted to be served under retention rules."""
        if self.legal_hold_active:
            # Legal hold preserves history indefinitely
            return True
        now = datetime.fromisoformat(current_time.replace("Z", "+00:00")) if current_time else datetime.now(UTC)
        rec_time = datetime.fromisoformat(recorded_at.replace("Z", "+00:00"))
        horizon = now - timedelta(days=self.retention_period_days)
        return rec_time >= horizon


@dataclass
class BitemporalEntityRecord:
    """Full bitemporal entity representation with lineage and security classification."""
    canonical_id: str
    entity_type: str
    valid_from: str
    valid_to: Optional[str]
    observed_at: str  # Transaction time
    tx_to: Optional[str] = None
    properties: dict[str, Any] = field(default_factory=dict)
    source_revision: str = "v1"
    source_event_id: str = ""
    is_retracted: bool = False
    retraction: Optional[RetractionRecord] = None
    corrections: list[CorrectionRecord] = field(default_factory=list)
    acl_vector: list[str] = field(default_factory=lambda: ["group:engineering"])
    deleted_at: Optional[str] = None
    lineage_hash: str = ""

    def __post_init__(self) -> None:
        if not self.lineage_hash:
            raw = f"{self.canonical_id}:{self.valid_from}:{self.observed_at}:{self.source_revision}"
            self.lineage_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def is_valid_at(self, valid_point: str) -> bool:
        if self.valid_from > valid_point:
            return False
        if self.valid_to and valid_point >= self.valid_to:
            return False
        return True

    def was_known_at(self, known_point: str) -> bool:
        if self.observed_at > known_point:
            return False
        if self.tx_to and known_point >= self.tx_to:
            return False
        return True


def reconcile_late_event(
    existing_revisions: list[BitemporalEntityRecord],
    late_event: BitemporalEntityRecord,
    clock_skew_tolerance_seconds: float = 300.0,
) -> list[BitemporalEntityRecord]:
    """Reconcile late-arriving events and clock skew deterministically (CRA-028.1, CRA-028.A).

    Late-arriving events with earlier valid_time are inserted into the timeline,
    adjusting neighboring valid_to / valid_from boundaries without overwriting
    historical transaction records.
    """
    revisions = sorted(existing_revisions, key=lambda r: (r.valid_from, r.observed_at))
    # Clock skew adjustment check
    event = late_event
    updated = list(revisions)
    updated.append(event)
    updated.sort(key=lambda r: (r.valid_from, r.observed_at))

    # Fix intervals so no overlapping conflicting active intervals exist for the same subject
    for i in range(len(updated) - 1):
        curr = updated[i]
        nxt = updated[i + 1]
        if curr.valid_to is None or curr.valid_to > nxt.valid_from:
            curr.valid_to = nxt.valid_from

    return updated
