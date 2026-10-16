"""Identity Candidate review queue (GAP-ER-001..010 deterministic subset, FR-ID-002).

Deterministic signals can suggest that two source identities may be the same
person without reaching merge confidence. Rather than silently merging (never
allowed below threshold), the resolver records an ``IdentityCandidate`` for
human review. A reviewed candidate becomes a CONFIRMED/REJECTED audit record;
only explicit confirmation authorizes a later merge operation.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from uuid import uuid4

from eoip.contracts.source_event import utc_now_iso

PENDING = "PENDING"
CONFIRMED = "CONFIRMED"
REJECTED = "REJECTED"


@dataclass
class IdentityCandidate:
    candidate_id: str
    existing_cid: str
    incoming_source_system: str
    incoming_identity: str
    match_basis: str  # e.g. "display_name" | "email_domain" | "manual"
    confidence: float  # deterministic signal score in [0, 1]; never auto-merges
    status: str = PENDING
    reviewer: str | None = None
    created_at: str = field(default_factory=utc_now_iso)
    decided_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> IdentityCandidate:
        return cls(**payload)


def suggest_candidate(
    store,
    *,
    existing_cid: str,
    incoming_source_system: str,
    incoming_identity: str,
    match_basis: str,
    confidence: float,
) -> IdentityCandidate | None:
    """Create a PENDING review candidate. Returns None when evidence is absent
    (unknown existing person) — a candidate requires a real anchor entity."""
    if store.get_vertex_by_canonical_id(existing_cid) is None:
        return None
    return IdentityCandidate(
        candidate_id=str(uuid4()),
        existing_cid=existing_cid,
        incoming_source_system=incoming_source_system,
        incoming_identity=incoming_identity,
        match_basis=match_basis,
        confidence=max(0.0, min(1.0, float(confidence))),
    )


class IdentityCandidateStore:
    """JSON-persisted candidate queue with audit-preserving decisions."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._items: dict[str, IdentityCandidate] = {}
        self._load()

    def add(self, candidate: IdentityCandidate) -> IdentityCandidate:
        self._items[candidate.candidate_id] = candidate
        self._save()
        return candidate

    def get(self, candidate_id: str) -> IdentityCandidate | None:
        return self._items.get(candidate_id)

    def list(self, *, status: str | None = None) -> list[IdentityCandidate]:
        values = sorted(self._items.values(), key=lambda item: item.created_at, reverse=True)
        if status:
            values = [item for item in values if item.status == status]
        return values

    def decide(self, candidate_id: str, *, approve: bool, reviewer: str) -> IdentityCandidate:
        candidate = self._items[candidate_id]
        if candidate.status != PENDING:
            raise ValueError("Candidate has already been decided")
        candidate.status = CONFIRMED if approve else REJECTED
        candidate.reviewer = reviewer
        candidate.decided_at = utc_now_iso()
        self._save()
        return candidate

    def _load(self) -> None:
        if not self._path.is_file():
            return
        payload = json.loads(self._path.read_text(encoding="utf-8"))
        self._items = {
            item["candidate_id"]: IdentityCandidate.from_dict(item)
            for item in payload.get("candidates", [])
        }

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self._path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "candidates": [item.to_dict() for item in self._items.values()],
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        temporary.replace(self._path)
