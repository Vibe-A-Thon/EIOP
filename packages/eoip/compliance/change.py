"""Change-governance proposal workflow (SR-GOV-003).

State machine for ontology, mapping, policy, model and agent changes:
``proposed -> review -> approved -> rolled_out`` with ``rolled_back``
reachable from ``approved`` or ``rolled_out``. Every transition appends a
tamper-evident entry to the change's audit trail; rollback is a first-class
state, not a delete. Applying the underlying mutation after approval remains
a separate, explicitly authorised platform operation (same separation as
``eoip.agents.proposals.ProposalStore``).

Persistence is a JSON-file store so the workflow survives restarts.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from threading import RLock
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from eoip.compliance.pack import new_id

ChangeKind = Literal["ontology", "mapping", "policy", "model", "agent"]
ChangeState = Literal["proposed", "review", "approved", "rolled_out", "rolled_back", "rejected"]

_TRANSITIONS: dict[ChangeState, set[ChangeState]] = {
    "proposed": {"review", "rejected"},
    "review": {"approved", "rejected", "proposed"},
    "approved": {"rolled_out", "rolled_back"},
    "rolled_out": {"rolled_back"},
    "rolled_back": set(),
    "rejected": set(),
}


class ChangeTransition(BaseModel):
    """One audited state transition."""

    model_config = ConfigDict(extra="forbid")

    from_state: ChangeState
    to_state: ChangeState
    actor: str
    at: str
    reason: str = ""


class ChangeProposal(BaseModel):
    """A governed change proposal (SR-GOV-003)."""

    model_config = ConfigDict(extra="forbid")

    proposal_id: str
    kind: ChangeKind
    title: str
    description: str = ""
    requested_by: str = ""
    state: ChangeState = "proposed"
    audit_trail: list[ChangeTransition] = Field(default_factory=list)
    created_at: str = ""
    applied_mutation_ref: str | None = None


class ChangeGovernanceStore:
    """JSON-file store + state machine for change proposals (SR-GOV-003)."""

    def __init__(self, path: str | Path | None = None) -> None:
        self._lock = RLock()
        self._path = Path(path) if path else Path(
            os.getenv("EOIP_DATA_DIR", ".data")
        ) / "state" / "change-governance.json"
        self._items: dict[str, ChangeProposal] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            return
        data = json.loads(self._path.read_text(encoding="utf-8"))
        for item in data.get("proposals", []):
            proposal = ChangeProposal(**item)
            self._items[proposal.proposal_id] = proposal

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"proposals": [p.model_dump() for p in self._items.values()]}
        self._path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def create(
        self,
        kind: ChangeKind,
        title: str,
        *,
        description: str = "",
        requested_by: str = "",
        created_at: str = "",
    ) -> ChangeProposal:
        proposal = ChangeProposal(
            proposal_id=new_id("compliance", "change-proposal"),
            kind=kind,
            title=title,
            description=description,
            requested_by=requested_by,
            created_at=created_at,
        )
        with self._lock:
            self._items[proposal.proposal_id] = proposal
            self._save()
        return proposal

    def get(self, proposal_id: str) -> ChangeProposal | None:
        return self._items.get(proposal_id)

    def list(self, *, state: ChangeState | None = None, kind: ChangeKind | None = None) -> list[ChangeProposal]:
        items = list(self._items.values())
        if state:
            items = [p for p in items if p.state == state]
        if kind:
            items = [p for p in items if p.kind == kind]
        return items

    def transition(
        self,
        proposal_id: str,
        to_state: ChangeState,
        *,
        actor: str,
        at: str,
        reason: str = "",
        applied_mutation_ref: str | None = None,
    ) -> ChangeProposal:
        """Move a proposal through the workflow, recording an audited transition."""
        with self._lock:
            proposal = self._items.get(proposal_id)
            if proposal is None:
                raise KeyError(f"Unknown proposal: {proposal_id}")
            allowed = _TRANSITIONS.get(proposal.state, set())
            if to_state not in allowed:
                raise ValueError(
                    f"Invalid transition: {proposal.state} -> {to_state} "
                    f"(allowed: {sorted(allowed) or 'none'})"
                )
            proposal.audit_trail.append(ChangeTransition(
                from_state=proposal.state,
                to_state=to_state,
                actor=actor,
                at=at,
                reason=reason,
            ))
            proposal.state = to_state
            if applied_mutation_ref is not None:
                proposal.applied_mutation_ref = applied_mutation_ref
            self._save()
            return proposal
