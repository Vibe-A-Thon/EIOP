"""Source-to-graph reconciliation and repair reports (G2-T0250..0253)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal
from uuid import uuid4

from eoip.contracts.source_event import SourceEvent, SourceEventV2, utc_now_iso
from pydantic import BaseModel, ConfigDict, Field


class ReconciliationRun(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0"] = "1.0"
    reconciliation_id: str
    source_id: str
    started_at: str
    finished_at: str
    checkpoint: str | None = None
    source_records: int = Field(ge=0)
    graph_records: int = Field(ge=0)
    unchanged: list[str] = Field(default_factory=list)
    missing: list[str] = Field(default_factory=list)
    stale: list[str] = Field(default_factory=list)
    orphaned: list[str] = Field(default_factory=list)
    repaired: list[str] = Field(default_factory=list)
    status: Literal["MATCHED", "DRIFT_FOUND", "REPAIRED", "PARTIAL"]


class SourceReconciler:
    def reconcile(
        self,
        *,
        source_id: str,
        events: list[SourceEvent | SourceEventV2],
        current_vertices: list[dict[str, Any]],
        canonical_id: Callable[[SourceEvent | SourceEventV2], str],
        repair: Callable[[list[SourceEvent | SourceEventV2]], list[str]] | None = None,
        checkpoint: str | None = None,
    ) -> ReconciliationRun:
        started_at = utc_now_iso()
        source = {canonical_id(event): event for event in events}
        graph = {vertex["canonical_id"]: vertex for vertex in current_vertices}
        missing = sorted(source.keys() - graph.keys())
        orphaned = sorted(graph.keys() - source.keys())
        stale, unchanged = [], []
        for cid in sorted(source.keys() & graph.keys()):
            graph_hash = graph[cid]["properties"].get("content_hash")
            if graph_hash == source[cid].payload_hash:
                unchanged.append(cid)
            else:
                stale.append(cid)
        repaired: list[str] = []
        if repair and (missing or stale):
            repaired = repair([source[cid] for cid in missing + stale])
        drift = bool(missing or stale or orphaned)
        status = "REPAIRED" if drift and set(repaired) == set(missing + stale) else "DRIFT_FOUND" if drift else "MATCHED"
        if repair and (missing or stale) and set(repaired) != set(missing + stale):
            status = "PARTIAL"
        return ReconciliationRun(
            reconciliation_id=str(uuid4()),
            source_id=source_id,
            started_at=started_at,
            finished_at=utc_now_iso(),
            checkpoint=checkpoint,
            source_records=len(source),
            graph_records=len(graph),
            unchanged=unchanged,
            missing=missing,
            stale=stale,
            orphaned=orphaned,
            repaired=sorted(repaired),
            status=status,
        )
