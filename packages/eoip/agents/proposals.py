"""Approval-gated storage for agent-authored change proposals.

Approval changes proposal state only; applying a mutation remains a separate,
explicitly authorised platform operation.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from threading import RLock

from eoip.contracts.agent import ChangeProposal
from eoip.contracts.source_event import utc_now_iso


class ProposalStore:
    def __init__(self, path: str | Path | None = None) -> None:
        self._items: dict[str, ChangeProposal] = {}
        self._lock = RLock()
        self._path = Path(path) if path else Path(
            os.getenv("EOIP_DATA_DIR", ".data")
        ) / "state" / "agent-proposals.json"
        self._load()

    def create(self, proposal: ChangeProposal) -> ChangeProposal:
        if proposal.status != "PENDING":
            raise ValueError("New proposals must be pending")
        with self._lock:
            if proposal.proposal_id in self._items:
                raise ValueError(f"Duplicate proposal: {proposal.proposal_id}")
            self._items[proposal.proposal_id] = proposal
            self._save()
        return proposal

    def get(self, proposal_id: str) -> ChangeProposal | None:
        return self._items.get(proposal_id)

    def list(self, *, status: str | None = None) -> list[ChangeProposal]:
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        return sorted(values, key=lambda item: item.created_at, reverse=True)

    def decide(self, proposal_id: str, *, actor_id: str, approve: bool) -> ChangeProposal:
        with self._lock:
            proposal = self._items.get(proposal_id)
            if proposal is None:
                raise KeyError(proposal_id)
            if proposal.status != "PENDING":
                raise ValueError("Proposal has already been decided")
            updated = proposal.model_copy(update={
                "status": "APPROVED" if approve else "REJECTED",
                "approved_by": actor_id,
                "decided_at": utc_now_iso(),
            })
            self._items[proposal_id] = updated
            self._save()
            return updated

    def _load(self) -> None:
        if not self._path.is_file():
            return
        payload = json.loads(self._path.read_text(encoding="utf-8"))
        proposals = [ChangeProposal.model_validate(item) for item in payload.get("proposals", [])]
        self._items = {item.proposal_id: item for item in proposals}

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self._path.with_suffix(".tmp")
        payload = {"schema_version": "1.0", "proposals": [
            item.model_dump(mode="json") for item in self._items.values()
        ]}
        temporary.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        temporary.replace(self._path)
