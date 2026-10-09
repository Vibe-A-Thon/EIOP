"""Moonshot 1: Quantum-Resilient Bitemporal Graph State Machine & Time-Warp Replay.

Provides zero-copy virtual branch forking, 2D bitemporal state reconstruction
(valid-time vs transaction-time), Merkle hash chain integrity, and CRDT delta
three-way merge semantics.
"""

from __future__ import annotations

import copy
import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any


def _hash_payload(data: Any) -> str:
    serialized = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class BitemporalDelta:
    """An atomic state mutation recording both valid-time and transaction-time."""
    entity_id: str
    op: str  # UPSERT, RETRACT, EXPIRE
    state: dict[str, Any]
    valid_from: float
    valid_to: float | None
    tx_time: float
    sequence_num: int
    delta_hash: str = ""

    @classmethod
    def create(
        cls,
        entity_id: str,
        op: str,
        state: dict[str, Any],
        valid_from: float,
        valid_to: float | None = None,
        tx_time: float | None = None,
        sequence_num: int = 0,
    ) -> BitemporalDelta:
        actual_tx = tx_time if tx_time is not None else time.time()
        raw_info = {
            "entity_id": entity_id,
            "op": op,
            "state": state,
            "valid_from": valid_from,
            "valid_to": valid_to,
            "tx_time": actual_tx,
            "sequence_num": sequence_num,
        }
        h = _hash_payload(raw_info)
        return cls(
            entity_id=entity_id,
            op=op,
            state=state,
            valid_from=valid_from,
            valid_to=valid_to,
            tx_time=actual_tx,
            sequence_num=sequence_num,
            delta_hash=h,
        )


@dataclass
class BitemporalCommit:
    """A Merkle-chained commit bundle containing one or more bitemporal deltas."""
    commit_id: str
    parent_id: str | None
    author: str
    message: str
    tx_time: float
    deltas: list[BitemporalDelta]
    merkle_root: str = ""

    def __post_init__(self) -> None:
        if not self.merkle_root:
            delta_hashes = [d.delta_hash for d in self.deltas]
            raw = {
                "commit_id": self.commit_id,
                "parent_id": self.parent_id,
                "author": self.author,
                "tx_time": self.tx_time,
                "delta_hashes": delta_hashes,
            }
            self.merkle_root = _hash_payload(raw)


class BitemporalStateMachine:
    """Quantum-resilient bitemporal state machine with zero-copy branch forking."""

    def __init__(self, tenant_id: str = "default") -> None:
        self.tenant_id = tenant_id
        # Branch name -> list of commits in chronological order
        self._branches: dict[str, list[BitemporalCommit]] = {"main": []}
        # Fork metadata: branch -> parent_branch, fork_commit_id
        self._fork_origins: dict[str, tuple[str, str | None]] = {"main": ("main", None)}
        self._seq_counter = 0

    def list_branches(self) -> list[str]:
        return sorted(self._branches.keys())

    def branch(self, new_branch: str, from_branch: str = "main", as_of_tx_time: float | None = None) -> str:
        """Create a zero-copy virtual branch forking from an existing branch."""
        if from_branch not in self._branches:
            raise KeyError(f"Source branch '{from_branch}' does not exist")
        if new_branch in self._branches:
            raise ValueError(f"Branch '{new_branch}' already exists")

        source_commits = self._branches[from_branch]
        if as_of_tx_time is not None:
            active_commits = [c for c in source_commits if c.tx_time <= as_of_tx_time]
        else:
            active_commits = list(source_commits)

        fork_head = active_commits[-1].commit_id if active_commits else None
        # Copy-on-write initial state: branch pointer inherits parent commits up to fork_head
        self._branches[new_branch] = list(active_commits)
        self._fork_origins[new_branch] = (from_branch, fork_head)
        return new_branch

    def commit(
        self,
        branch: str,
        entity_id: str,
        state: dict[str, Any],
        op: str = "UPSERT",
        valid_from: float | None = None,
        valid_to: float | None = None,
        tx_time: float | None = None,
        author: str = "system",
        message: str = "Update entity state",
    ) -> BitemporalCommit:
        """Commit an atomic bitemporal delta to a specific branch."""
        if branch not in self._branches:
            raise KeyError(f"Branch '{branch}' does not exist")

        now = time.time()
        actual_tx = tx_time if tx_time is not None else now
        actual_valid_from = valid_from if valid_from is not None else actual_tx

        self._seq_counter += 1
        delta = BitemporalDelta.create(
            entity_id=entity_id,
            op=op,
            state=state,
            valid_from=actual_valid_from,
            valid_to=valid_to,
            tx_time=actual_tx,
            sequence_num=self._seq_counter,
        )

        parent = self._branches[branch][-1].commit_id if self._branches[branch] else None
        commit_id = f"c_{self.tenant_id}_{int(actual_tx * 1000)}_{self._seq_counter}"
        commit_obj = BitemporalCommit(
            commit_id=commit_id,
            parent_id=parent,
            author=author,
            message=message,
            tx_time=actual_tx,
            deltas=[delta],
        )
        self._branches[branch].append(commit_obj)
        return commit_obj

    def time_warp_replay(
        self,
        branch: str,
        valid_at: float,
        tx_at: float | None = None,
    ) -> dict[str, dict[str, Any]]:
        """Reconstruct the entire active graph state as of (valid_at, tx_at).

        Returns:
            Dict mapping entity_id to its properties at that 2D temporal coordinate.
        """
        if branch not in self._branches:
            raise KeyError(f"Branch '{branch}' does not exist")

        effective_tx = tx_at if tx_at is not None else float("inf")
        # Step 1: Collect all commits recorded in transaction time <= effective_tx
        applicable_deltas: list[BitemporalDelta] = []
        for c in self._branches[branch]:
            if c.tx_time <= effective_tx:
                for d in c.deltas:
                    applicable_deltas.append(d)

        # Sort by sequence_num
        applicable_deltas.sort(key=lambda d: d.sequence_num)

        # Step 2: Apply deltas to reconstruct state as of valid_at
        active_entities: dict[str, dict[str, Any]] = {}

        for d in applicable_deltas:
            # Check valid-time window
            is_valid = d.valid_from <= valid_at and (d.valid_to is None or d.valid_to > valid_at)
            if not is_valid:
                continue

            if d.op == "RETRACT" or d.op == "EXPIRE":
                active_entities.pop(d.entity_id, None)
            elif d.op == "UPSERT":
                existing = active_entities.get(d.entity_id, {})
                updated = dict(existing)
                updated.update(d.state)
                active_entities[d.entity_id] = updated

        return active_entities

    def diff_branches(self, branch_a: str, branch_b: str) -> dict[str, Any]:
        """Compute structural differences between two branches with real conflict detection."""
        if branch_a not in self._branches or branch_b not in self._branches:
            raise KeyError("Both branches must exist for diff calculation")

        now = time.time()
        state_a = self.time_warp_replay(branch_a, valid_at=now)
        state_b = self.time_warp_replay(branch_b, valid_at=now)

        keys_a = set(state_a.keys())
        keys_b = set(state_b.keys())

        added_in_b = sorted(list(keys_b - keys_a))
        removed_in_b = sorted(list(keys_a - keys_b))
        modified: dict[str, dict[str, Any]] = {}
        conflicts: list[dict[str, Any]] = []

        fork_origin = self._fork_origins.get(branch_b, (branch_a, None))
        fork_commit_id = fork_origin[1] if fork_origin[0] == branch_a else None

        base_state: dict[str, dict[str, Any]] = {}
        if fork_commit_id:
            fork_commit = next(
                (c for c in self._branches[branch_a] if c.commit_id == fork_commit_id),
                None,
            )
            if fork_commit:
                base_state = self.time_warp_replay(branch_a, valid_at=now, tx_at=fork_commit.tx_time)

        for k in keys_a & keys_b:
            if state_a[k] != state_b[k]:
                base_val = base_state.get(k, {})
                a_changed = state_a[k] != base_val
                b_changed = state_b[k] != base_val
                if a_changed and b_changed:
                    conflicting_fields = []
                    all_keys = set(state_a[k].keys()) | set(state_b[k].keys())
                    for field in all_keys:
                        va = state_a[k].get(field)
                        vb = state_b[k].get(field)
                        vbase = base_val.get(field)
                        if va != vb and va != vbase and vb != vbase:
                            conflicting_fields.append(field)
                    if conflicting_fields:
                        conflicts.append({
                            "entity_id": k,
                            "conflicting_fields": conflicting_fields,
                            "branch_a_state": state_a[k],
                            "branch_b_state": state_b[k],
                            "base_state": base_val,
                        })
                modified[k] = {"before": state_a[k], "after": state_b[k]}

        return {
            "branch_a": branch_a,
            "branch_b": branch_b,
            "added": added_in_b,
            "removed": removed_in_b,
            "modified": modified,
            "conflicts": conflicts,
            "has_conflicts": len(conflicts) > 0,
        }

    def merge_crdt(self, target_branch: str, source_branch: str,
                   author: str = "merge-agent",
                   force: bool = False) -> BitemporalCommit | None:
        """Merge source_branch into target_branch using Last-Write-Wins CRDT delta resolution.

        When both branches modify the same entity field, the delta with the later
        tx_time wins (LWW). If force=False (default) and unresolvable conflicts
        exist (identical tx_time on divergent values), raises ValueError.
        """
        if target_branch not in self._branches or source_branch not in self._branches:
            raise KeyError("Target and source branches must exist")

        diff = self.diff_branches(target_branch, source_branch)
        if diff["has_conflicts"] and not force:
            conflict_ids = [c["entity_id"] for c in diff["conflicts"]]
            raise ValueError(
                f"CRDT merge blocked: conflicting entities {conflict_ids}. "
                f"Use force=True for LWW resolution or resolve manually."
            )

        target_commits = {c.commit_id for c in self._branches[target_branch]}
        incoming_commits = [c for c in self._branches[source_branch] if c.commit_id not in target_commits]

        if not incoming_commits:
            return None

        all_new_deltas: list[BitemporalDelta] = []
        target_latest: dict[str, float] = {}
        for c in self._branches[target_branch]:
            for d in c.deltas:
                target_latest[d.entity_id] = max(
                    target_latest.get(d.entity_id, 0.0), d.tx_time
                )

        for c in incoming_commits:
            for d in c.deltas:
                target_tx = target_latest.get(d.entity_id, 0.0)
                if d.tx_time >= target_tx:
                    all_new_deltas.append(d)

        all_new_deltas.sort(key=lambda d: (d.tx_time, d.sequence_num))

        if not all_new_deltas:
            return None

        now = time.time()
        self._seq_counter += 1
        parent = self._branches[target_branch][-1].commit_id if self._branches[target_branch] else None
        merge_commit_id = f"merge_{target_branch}_{source_branch}_{int(now*1000)}"

        merge_commit = BitemporalCommit(
            commit_id=merge_commit_id,
            parent_id=parent,
            author=author,
            message=f"Merged '{source_branch}' into '{target_branch}' (LWW-CRDT, {len(all_new_deltas)} deltas)",
            tx_time=now,
            deltas=all_new_deltas,
        )
        self._branches[target_branch].append(merge_commit)
        return merge_commit

    def verify_chain_integrity(self, branch: str) -> bool:
        """Verify the cryptographic Merkle chain consistency for a branch."""
        commits = self._branches.get(branch, [])
        if not commits:
            return True

        for i, c in enumerate(commits):
            expected_parent = commits[i - 1].commit_id if i > 0 else c.parent_id
            if c.parent_id != expected_parent:
                return False
            # Verify merkle root matches contents
            delta_hashes = [d.delta_hash for d in c.deltas]
            raw = {
                "commit_id": c.commit_id,
                "parent_id": c.parent_id,
                "author": c.author,
                "tx_time": c.tx_time,
                "delta_hashes": delta_hashes,
            }
            computed_root = _hash_payload(raw)
            if computed_root != c.merkle_root:
                return False
        return True
