"""Atlas-Pattern Lineage Classification Propagation and Reversal (CRA-029.7, INV-45).

Features:
- Tagging an upstream asset/column with a classification (e.g. PII, PCI, CONFIDENTIAL)
  automatically cascades along downstream lineage paths to all derived tables, views, and dashboards.
- Each cascaded classification retains exact provenance: root entity ID, path depth, and applied timestamp.
- Removal of the classification from the root cleanly and reversibly retracts the cascade
  from all downstream assets without affecting independent tags.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Optional

from eoip.graph.store import GraphStore


@dataclass
class PropagatedTag:
    tag_name: str
    root_asset_id: str
    hop_distance: int
    applied_at: str
    is_direct: bool = False


class ClassificationPropagationEngine:
    """Manages lineage-driven classification cascades and reversible retractions (CRA-029.7)."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store
        # asset_id -> tag_name -> PropagatedTag
        self._tags_by_asset: dict[str, dict[str, PropagatedTag]] = defaultdict(dict)

    def _get_downstream_lineage(self, root_cid: str, max_depth: int = 10) -> list[tuple[str, int]]:
        """BFS downstream traversal along dependency and derived edges."""
        edges = self._store.find_edges(limit=100_000)
        adj: dict[str, list[str]] = defaultdict(list)
        for e in edges:
            out_cid = e.get("out_cid")
            in_cid = e.get("in_cid")
            # Downstream propagation follows data flow: out_cid produces / feeds in_cid,
            # or in_cid DEPENDS_ON out_cid
            if e.get("label") in ("CALLS", "DEPLOYS", "PRODUCES", "CONTAINS"):
                adj[out_cid].append(in_cid)
            elif e.get("label") in ("DEPENDS_ON", "DERIVED_FROM", "REFERENCES"):
                adj[in_cid].append(out_cid)  # reversed data dependency: upstream -> downstream

        visited: set[str] = {root_cid}
        queue: deque[tuple[str, int]] = deque([(root_cid, 0)])
        downstream: list[tuple[str, int]] = []

        while queue:
            current, depth = queue.popleft()
            if current != root_cid:
                downstream.append((current, depth))
            if depth >= max_depth:
                continue
            for nbr in adj.get(current, []):
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append((nbr, depth + 1))

        return downstream

    def add_classification(self, asset_id: str, tag_name: str) -> dict[str, Any]:
        """Apply a classification tag to an asset and cascade downstream (CRA-029.7)."""
        ts = datetime.now(UTC).isoformat()
        # Direct tag on root
        self._tags_by_asset[asset_id][tag_name] = PropagatedTag(
            tag_name=tag_name,
            root_asset_id=asset_id,
            hop_distance=0,
            applied_at=ts,
            is_direct=True,
        )

        downstream = self._get_downstream_lineage(asset_id)
        cascaded_ids: list[str] = []

        for downstream_id, depth in downstream:
            self._tags_by_asset[downstream_id][tag_name] = PropagatedTag(
                tag_name=tag_name,
                root_asset_id=asset_id,
                hop_distance=depth,
                applied_at=ts,
                is_direct=False,
            )
            cascaded_ids.append(downstream_id)

        return {
            "root_asset_id": asset_id,
            "tag_name": tag_name,
            "cascaded_count": len(cascaded_ids),
            "cascaded_to": cascaded_ids,
        }

    def remove_classification(self, asset_id: str, tag_name: str) -> dict[str, Any]:
        """Remove a classification tag from an asset and reversibly retract downstream cascade (CRA-029.7)."""
        existing = self._tags_by_asset.get(asset_id, {}).get(tag_name)
        if not existing or not existing.is_direct:
            return {"removed": False, "reason": "Tag is not directly applied to this asset"}

        del self._tags_by_asset[asset_id][tag_name]

        # Retract cascade from all downstream assets whose tag was rooted at this asset
        retracted_ids: list[str] = []
        for a_id, tags in list(self._tags_by_asset.items()):
            if tag_name in tags and tags[tag_name].root_asset_id == asset_id and not tags[tag_name].is_direct:
                del tags[tag_name]
                retracted_ids.append(a_id)

        return {
            "root_asset_id": asset_id,
            "tag_name": tag_name,
            "removed": True,
            "retracted_count": len(retracted_ids),
            "retracted_from": retracted_ids,
        }

    def get_classifications(self, asset_id: str) -> list[dict[str, Any]]:
        """Get all direct and cascaded classifications with full provenance."""
        tags = self._tags_by_asset.get(asset_id, {})
        return [
            {
                "tag_name": t.tag_name,
                "is_direct": t.is_direct,
                "root_asset_id": t.root_asset_id,
                "hop_distance": t.hop_distance,
                "applied_at": t.applied_at,
            }
            for t in tags.values()
        ]
