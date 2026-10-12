"""Semantic stewardship workflow and ontology branching (GAP-GOV, GAP-GITOPS-002, GAP-GITOPS-007).

Implements the governance lifecycle:
DRAFT -> IN_REVIEW -> APPROVED -> PUBLISHED -> DEPRECATED
with ontology branching, semantic diffs, semantic merge, and audit trails.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from eoip.ontology.gitops import (
    SemanticChange,
    SemanticDiff,
    diff_manifests,
    snapshot_manifest,
)
from eoip.ontology.manifest import EDGE_LABELS, PROPERTY_KEYS, VERTEX_LABELS


class GovernanceState(str, Enum):
    DRAFT = "DRAFT"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    DEPRECATED = "DEPRECATED"


ALLOWED_GOVERNANCE_TRANSITIONS: dict[GovernanceState, set[GovernanceState]] = {
    GovernanceState.DRAFT: {GovernanceState.IN_REVIEW, GovernanceState.DEPRECATED},
    GovernanceState.IN_REVIEW: {GovernanceState.APPROVED, GovernanceState.DRAFT, GovernanceState.DEPRECATED},
    GovernanceState.APPROVED: {GovernanceState.PUBLISHED, GovernanceState.IN_REVIEW, GovernanceState.DEPRECATED},
    GovernanceState.PUBLISHED: {GovernanceState.DEPRECATED},
    GovernanceState.DEPRECATED: set(),
}


@dataclass
class OntologyBranch:
    name: str
    base_version: str
    manifest: dict[str, Any]
    state: GovernanceState = GovernanceState.DRAFT
    author: str = ""
    reviewers: list[str] = field(default_factory=list)
    approvers: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    audit_trail: list[dict[str, Any]] = field(default_factory=list)


class SemanticStewardshipManager:
    """Manages ontology governance branches, lifecycle states, and semantic merges (GAP-GOV)."""

    def __init__(self, main_manifest: dict[str, Any] | None = None) -> None:
        self._canonical_manifest = main_manifest or snapshot_manifest(
            VERTEX_LABELS, EDGE_LABELS, PROPERTY_KEYS
        )
        self._branches: dict[str, OntologyBranch] = {}
        # Main branch
        self._branches["main"] = OntologyBranch(
            name="main",
            base_version="1.0.0",
            manifest=self._canonical_manifest,
            state=GovernanceState.PUBLISHED,
            author="system",
        )

    def create_branch(self, branch_name: str, author: str = "steward", base_branch: str = "main") -> OntologyBranch:
        if branch_name in self._branches:
            raise ValueError(f"Branch '{branch_name}' already exists")
        base = self._branches.get(base_branch)
        if not base:
            raise ValueError(f"Base branch '{base_branch}' not found")

        # Deep copy manifest for the new branch
        import copy
        branch = OntologyBranch(
            name=branch_name,
            base_version=base.base_version,
            manifest=copy.deepcopy(base.manifest),
            state=GovernanceState.DRAFT,
            author=author,
        )
        branch.audit_trail.append({
            "action": "BRANCH_CREATED",
            "author": author,
            "base": base_branch,
            "timestamp": datetime.now(UTC).isoformat(),
        })
        self._branches[branch_name] = branch
        return branch

    def get_branch(self, branch_name: str) -> OntologyBranch:
        if branch_name not in self._branches:
            raise KeyError(f"Branch '{branch_name}' not found")
        return self._branches[branch_name]

    def transition_state(self, branch_name: str, new_state: GovernanceState, actor: str, comment: str = "") -> OntologyBranch:
        branch = self.get_branch(branch_name)
        if new_state not in ALLOWED_GOVERNANCE_TRANSITIONS.get(branch.state, set()):
            raise ValueError(f"Illegal governance transition from {branch.state} to {new_state}")

        old_state = branch.state
        branch.state = new_state
        branch.updated_at = datetime.now(UTC).isoformat()
        if new_state == GovernanceState.IN_REVIEW and actor not in branch.reviewers:
            branch.reviewers.append(actor)
        if new_state == GovernanceState.APPROVED and actor not in branch.approvers:
            branch.approvers.append(actor)

        branch.audit_trail.append({
            "action": "STATE_TRANSITION",
            "from_state": old_state.value,
            "to_state": new_state.value,
            "actor": actor,
            "comment": comment,
            "timestamp": branch.updated_at,
        })
        return branch

    def diff_with_main(self, branch_name: str) -> SemanticDiff:
        branch = self.get_branch(branch_name)
        return diff_manifests(self._branches["main"].manifest, branch.manifest)

    def merge_to_main(self, branch_name: str, approver: str) -> dict[str, Any]:
        """Semantically merges an approved branch into main."""
        branch = self.get_branch(branch_name)
        if branch.state != GovernanceState.APPROVED:
            raise ValueError(f"Branch '{branch_name}' cannot be merged because state is {branch.state}, not APPROVED")

        diff = self.diff_with_main(branch_name)
        if diff.breaking:
            raise ValueError(f"Cannot automatically merge branch '{branch_name}' with {len(diff.breaking)} breaking changes")

        # Update main manifest with changes
        import copy
        self._branches["main"].manifest = copy.deepcopy(branch.manifest)
        self._branches["main"].updated_at = datetime.now(UTC).isoformat()
        self.transition_state(branch_name, GovernanceState.PUBLISHED, actor=approver, comment="Merged into main")

        return {
            "status": "MERGED",
            "branch": branch_name,
            "approver": approver,
            "changes_merged": len(diff.changes),
            "breaking_count": len(diff.breaking),
        }
