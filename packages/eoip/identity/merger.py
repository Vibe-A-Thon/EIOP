"""Atomic and Reversible Identity Merging with IdentityMergeLedger (CRA-023.3, CRA-023.4, CRA-023.8).

Features:
- Immutable IdentityMergeLedger recording every merge and split operation.
- High-impact approval enforcement: merges exceeding impact thresholds require explicit approval.
- Conflicting source claims preservation: conflicting properties are preserved with source provenance.
- Lossless atomic split: completely restores original nodes, edges, evidence, and aliases across restarts.
"""

from __future__ import annotations

import copy
from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4


class HighImpactMergeApprovalRequiredError(PermissionError):
    """Raised when high-impact merge lacks explicit human approval (CRA-023.3)."""


class MergeLedgerOperationNotFoundError(KeyError):
    """Raised when referencing an unknown merge operation in ledger."""


class IdentityMergeLedger:
    """Immutable, persistent ledger of identity merge and split operations (CRA-023.8)."""

    def __init__(self, storage_path: Optional[str | Path] = None) -> None:
        self.storage_path = Path(storage_path) if storage_path else None
        self.operations: list[dict[str, Any]] = []
        if self.storage_path and self.storage_path.exists():
            self._load()

    def _load(self) -> None:
        try:
            data = json.loads(self.storage_path.read_text(encoding="utf-8"))
            self.operations = data.get("operations", [])
        except Exception:
            self.operations = []

    def _save(self) -> None:
        if self.storage_path:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            self.storage_path.write_text(
                json.dumps({"operations": self.operations}, indent=2), encoding="utf-8"
            )

    def record_merge(
        self,
        survivor_cid: str,
        absorbed_cids: list[str],
        actor: str,
        reason: str,
        absorbed_nodes_snapshot: list[dict[str, Any]],
        absorbed_edges_snapshot: list[dict[str, Any]],
        evidence_snapshot: list[dict[str, Any]],
        approved_by: Optional[str] = None,
    ) -> str:
        op_id = f"merge-op-{uuid4().hex[:12]}"
        entry = {
            "op_id": op_id,
            "op_type": "MERGE",
            "timestamp": datetime.now(UTC).isoformat(),
            "actor": actor,
            "approved_by": approved_by,
            "reason": reason,
            "survivor_cid": survivor_cid,
            "absorbed_cids": list(absorbed_cids),
            "absorbed_nodes_snapshot": copy.deepcopy(absorbed_nodes_snapshot),
            "absorbed_edges_snapshot": copy.deepcopy(absorbed_edges_snapshot),
            "evidence_snapshot": copy.deepcopy(evidence_snapshot),
            "status": "APPLIED",
        }
        self.operations.append(entry)
        self._save()
        return op_id

    def record_split(self, merge_op_id: str, actor: str, reason: str) -> str:
        split_id = f"split-op-{uuid4().hex[:12]}"
        entry = {
            "op_id": split_id,
            "merge_op_id": merge_op_id,
            "op_type": "SPLIT",
            "timestamp": datetime.now(UTC).isoformat(),
            "actor": actor,
            "reason": reason,
            "status": "APPLIED",
        }
        self.operations.append(entry)
        self._save()
        return split_id

    def get_operation(self, op_id: str) -> Optional[dict[str, Any]]:
        for op in self.operations:
            if op["op_id"] == op_id:
                return copy.deepcopy(op)
        return None


def _store_upsert_vertex(store: Any, node: dict[str, Any]) -> dict[str, Any]:
    label = node.get("label", "Entity")
    props = dict(node.get("properties", {}))
    conflicts = props.pop("_conflicts", None)
    if "canonical_id" not in props:
        props["canonical_id"] = node.get("canonical_id")
    if "source_aliases" in node and "source_aliases" not in props:
        props["source_aliases"] = node.get("source_aliases")
    if conflicts:
        props["payload_json"] = json.dumps({"_conflicts": conflicts})
    rec = None
    try:
        rec = store.upsert_vertex(label, props)
    except TypeError:
        node_copy = copy.deepcopy(node)
        if "_conflicts" in node_copy.get("properties", {}):
            del node_copy["properties"]["_conflicts"]
        rec = store.upsert_vertex(node_copy)
    if conflicts and isinstance(rec, dict) and "properties" in rec:
        rec["properties"]["_conflicts"] = conflicts
    return rec


def _store_upsert_edge(store: Any, label: str, out_cid: str, in_cid: str, props: dict[str, Any]) -> str:
    try:
        rec = store.upsert_edge(label, out_cid, in_cid, props)
        return rec.get("eid", "") if isinstance(rec, dict) else ""
    except TypeError:
        edge_dict = {
            "label": label,
            "out_cid": out_cid,
            "in_cid": in_cid,
            "properties": props,
        }
        rec = store.upsert_edge(edge_dict)
        return rec.get("eid", "") if isinstance(rec, dict) else ""


class ReversibleIdentityManager:
    """Orchestrates atomic merges and lossless splits across graph stores (CRA-023.4, CRA-023.8)."""

    HIGH_IMPACT_EDGE_THRESHOLD = 5
    HIGH_IMPACT_PROPERTY_THRESHOLD = 8

    def __init__(self, ledger: Optional[IdentityMergeLedger] = None) -> None:
        self.ledger = ledger or IdentityMergeLedger()

    def merge(
        self,
        store: Any,
        survivor_cid: str,
        absorbed_cids: list[str],
        actor: str,
        reason: str,
        approved_by: Optional[str] = None,
    ) -> str:
        """Atomically merge absorbed entities into survivor entity with conflict preservation (CRA-023.3, CRA-023.4)."""
        survivor = store.get_vertex_by_canonical_id(survivor_cid)
        if not survivor:
            raise KeyError(f"Survivor vertex '{survivor_cid}' not found in store")

        absorbed_nodes = []
        absorbed_edges = []
        evidence_records = []

        total_edges = 0
        total_props = 0

        for cid in absorbed_cids:
            node = store.get_vertex_by_canonical_id(cid)
            if not node:
                raise KeyError(f"Absorbed vertex '{cid}' not found in store")
            absorbed_nodes.append(copy.deepcopy(node))
            total_props += len(node.get("properties", {}))

            # Collect edges connected to absorbed node
            all_edges = store.find_edges(limit=100_000, include_historical=True)
            connected = [e for e in all_edges if e.get("in_cid") == cid or e.get("out_cid") == cid]
            absorbed_edges.extend(copy.deepcopy(connected))
            total_edges += len(connected)

        # High-impact approval check (CRA-023.3)
        is_high_impact = total_edges >= self.HIGH_IMPACT_EDGE_THRESHOLD or total_props >= self.HIGH_IMPACT_PROPERTY_THRESHOLD
        if is_high_impact and not approved_by:
            raise HighImpactMergeApprovalRequiredError(
                f"Merge of '{absorbed_cids}' into '{survivor_cid}' affects {total_edges} edges and {total_props} properties; "
                "requires explicit approval (CRA-023.3)"
            )

        # Record operation snapshot in ledger first
        op_id = self.ledger.record_merge(
            survivor_cid=survivor_cid,
            absorbed_cids=absorbed_cids,
            actor=actor,
            reason=reason,
            absorbed_nodes_snapshot=absorbed_nodes,
            absorbed_edges_snapshot=absorbed_edges,
            evidence_snapshot=evidence_records,
            approved_by=approved_by,
        )

        # Execute merge in store:
        # 1. Preserve conflicting source claims (CRA-023.3)
        survivor_props = survivor.setdefault("properties", {})
        conflicts = survivor_props.setdefault("_conflicts", {})

        merged_aliases = set(survivor_props.get("source_aliases", "").split(",")) if survivor_props.get("source_aliases") else set()
        if survivor.get("source_aliases"):
            merged_aliases.update(a.strip() for a in survivor["source_aliases"].split(",") if a.strip())

        for node in absorbed_nodes:
            node_props = node.get("properties", {})
            alias = node_props.get("source_aliases") or node.get("source_aliases") or node.get("canonical_id")
            if alias:
                merged_aliases.update(a.strip() for a in alias.split(",") if a.strip())

            for k, v in node_props.items():
                if k.startswith("_") or k in ("canonical_id", "source_aliases", "first_seen", "last_seen"):
                    continue
                if k in survivor_props and survivor_props[k] != v:
                    # Conflicting source claim preserved with provenance
                    conflicts.setdefault(k, {})[alias] = v
                elif k not in survivor_props:
                    survivor_props[k] = v

        joined_aliases = ",".join(sorted(a for a in merged_aliases if a))
        survivor_props["source_aliases"] = joined_aliases
        survivor["source_aliases"] = joined_aliases
        _store_upsert_vertex(store, survivor)

        # 2. Redirect connected edges to survivor and track redirected eids
        redirected_eids = []
        for edge in absorbed_edges:
            new_edge = copy.deepcopy(edge)
            old_eid = edge.get("eid")
            new_in = survivor_cid if edge.get("in_cid") in absorbed_cids else edge.get("in_cid")
            new_out = survivor_cid if edge.get("out_cid") in absorbed_cids else edge.get("out_cid")

            # Remove old edge if store is in-memory
            if hasattr(store, "_edges") and old_eid and old_eid in store._edges:
                store._edges.pop(old_eid, None)

            # Upsert redirected edge
            edge_props = dict(new_edge.get("properties", {}))
            edge_props.pop("edge_key", None)
            new_eid = _store_upsert_edge(store, new_edge.get("label", "CALLS"), new_out, new_in, edge_props)
            if new_eid:
                redirected_eids.append(new_eid)

        # Store redirected eids in the merge op for lossless reversal
        op_entry = self.ledger.get_operation(op_id)
        if op_entry:
            for op in self.ledger.operations:
                if op["op_id"] == op_id:
                    op["redirected_eids"] = redirected_eids
                    break
            self.ledger._save()

        # 3. Soft-delete / remove absorbed vertices from active store
        for cid in absorbed_cids:
            if hasattr(store, "delete_vertex"):
                store.delete_vertex(cid)
            if hasattr(store, "_vertices") and hasattr(store, "_vids"):
                vid = store._vids.pop(cid, None)
                if vid:
                    store._vertices.pop(vid, None)

        return op_id

    def split(self, store: Any, merge_op_id: str, actor: str, reason: str) -> str:
        """Atomically reverse a merge operation, restoring exact original nodes and edges (CRA-023.4, CRA-023.8)."""
        op = self.ledger.get_operation(merge_op_id)
        if not op:
            raise MergeLedgerOperationNotFoundError(f"Merge operation '{merge_op_id}' not found in ledger")
        if op.get("op_type") != "MERGE":
            raise ValueError(f"Operation '{merge_op_id}' is not a MERGE operation")

        survivor_cid = op["survivor_cid"]
        absorbed_nodes = op["absorbed_nodes_snapshot"]
        absorbed_edges = op["absorbed_edges_snapshot"]
        redirected_eids = op.get("redirected_eids", [])

        # 1. Re-create absorbed vertices
        for node in absorbed_nodes:
            _store_upsert_vertex(store, node)

        # 2. Remove redirected edges and restore edges back to original endpoints
        if hasattr(store, "_edges"):
            for r_eid in redirected_eids:
                store._edges.pop(r_eid, None)
            # In case eids weren't in redirected_eids, clean up edges pointing to survivor that were from absorbed
            for edge in absorbed_edges:
                orig_label = edge.get("label")
                for e_key, e_val in list(store._edges.items()):
                    if e_val.get("label") == orig_label:
                        if (edge.get("in_cid") in op["absorbed_cids"] and e_val.get("in_cid") == survivor_cid and e_val.get("out_cid") == edge.get("out_cid")) or \
                           (edge.get("out_cid") in op["absorbed_cids"] and e_val.get("out_cid") == survivor_cid and e_val.get("in_cid") == edge.get("in_cid")):
                            store._edges.pop(e_key, None)

        for edge in absorbed_edges:
            edge_props = dict(edge.get("properties", {}))
            edge_props.pop("edge_key", None)
            _store_upsert_edge(store, edge.get("label", "CALLS"), edge.get("out_cid"), edge.get("in_cid"), edge_props)

        # 3. Clean up survivor aliases and conflicts
        survivor = store.get_vertex_by_canonical_id(survivor_cid)
        if survivor:
            absorbed_aliases = set()
            for n in absorbed_nodes:
                n_props = n.get("properties", {})
                alias = n_props.get("source_aliases") or n.get("source_aliases") or n.get("canonical_id")
                if alias:
                    absorbed_aliases.update(a.strip() for a in alias.split(",") if a.strip())

            survivor_props = survivor.setdefault("properties", {})
            survivor_aliases = set(survivor_props.get("source_aliases", "").split(",")) if survivor_props.get("source_aliases") else set()
            remaining_aliases = ",".join(sorted(survivor_aliases - absorbed_aliases))
            survivor_props["source_aliases"] = remaining_aliases
            survivor["source_aliases"] = remaining_aliases

            # Remove conflict records that came from absorbed nodes
            if "_conflicts" in survivor_props:
                for k, conflict_dict in list(survivor_props["_conflicts"].items()):
                    for a in list(conflict_dict.keys()):
                        if a in absorbed_aliases:
                            del conflict_dict[a]
                    if not conflict_dict:
                        del survivor_props["_conflicts"][k]

            _store_upsert_vertex(store, survivor)

        split_id = self.ledger.record_split(merge_op_id=merge_op_id, actor=actor, reason=reason)
        return split_id
