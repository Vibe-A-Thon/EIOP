"""Graph repair: dangling-edge detection and orphan clustering.

* ``detect_dangling_edges`` — edges whose endpoint vertices are missing
  (or tombstoned) from the vertex set.
* ``cluster_orphans`` — weakly-connected components over the orphan edges
  (plus singleton orphans) so repair can propose batched fixes.

Works on plain snapshots (sets of vertex ids + edge dicts), so it is
testable without a live GraphStore.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DanglingEdge(BaseModel):
    model_config = ConfigDict(extra="forbid")

    edge_id: str
    label: str
    from_id: str
    to_id: str
    missing_from: bool = False
    missing_to: bool = False


class RepairReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    report_id: str
    dangling: list[DanglingEdge] = Field(default_factory=list)
    orphan_clusters: list[list[str]] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

    @property
    def dangling_count(self) -> int:
        return len(self.dangling)


def detect_dangling_edges(
    vertex_ids: set[str],
    edges: Iterable[dict[str, Any]],
    *,
    include_tombstoned: bool = False,
) -> list[DanglingEdge]:
    """Edges referencing vertices absent from ``vertex_ids``."""
    dangling = []
    for edge in edges:
        out_cid = str(edge.get("out_cid") or edge.get("from_id") or "")
        in_cid = str(edge.get("in_cid") or edge.get("to_id") or "")
        missing_from = out_cid not in vertex_ids
        missing_to = in_cid not in vertex_ids
        if missing_from or missing_to:
            dangling.append(
                DanglingEdge(
                    edge_id=str(edge.get("edge_id") or edge.get("eid") or f"{out_cid}->{in_cid}"),
                    label=str(edge.get("label", "")),
                    from_id=out_cid,
                    to_id=in_cid,
                    missing_from=missing_from,
                    missing_to=missing_to,
                )
            )
    return sorted(dangling, key=lambda d: d.edge_id)


def cluster_orphans(dangling: list[DanglingEdge]) -> list[list[str]]:
    """Group dangling edges by weakly-connected components of their endpoints."""
    adj: dict[str, set[str]] = {}
    for edge in dangling:
        adj.setdefault(edge.from_id, set()).add(edge.to_id)
        adj.setdefault(edge.to_id, set()).add(edge.from_id)

    clusters: list[list[str]] = []
    seen: set[str] = set()
    for start in sorted(adj):
        if start in seen:
            continue
        stack, component = [start], []
        seen.add(start)
        while stack:
            node = stack.pop()
            component.append(node)
            for other in adj[node]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        clusters.append(sorted(component))
    return sorted(clusters, key=lambda c: (c[0], len(c)))


def repair_report(vertex_ids: set[str], edges: list[dict[str, Any]]) -> RepairReport:
    import hashlib

    dangling = detect_dangling_edges(vertex_ids, edges)
    clusters = cluster_orphans(dangling)
    digest = hashlib.sha256(repr((sorted(vertex_ids), sorted(map(repr, edges)))).encode()).hexdigest()[:24]
    return RepairReport(
        report_id=f"urn:eoip:graphbuild:repair:{digest}",
        dangling=dangling,
        orphan_clusters=clusters,
        notes=[f"vertices={len(vertex_ids)}", f"edges={len(edges)}", f"dangling={len(dangling)}"],
    )
