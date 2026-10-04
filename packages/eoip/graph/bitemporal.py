"""Bitemporal query layer over the revision model (GAP-TEMP-001..005).

Pure read layer: reconstructs historical graph states from ``EntityRevision``
and ``RelationshipRevision`` vertices (see G2-P2 evolution engine and
``eoip.ontology.manifest`` VERTEX_LABELS) without mutating any data.

Two independent time axes are queried:

* **transaction time** (``known_at`` / system time) — the revision record
  timeline: which revisions had been *recorded* at system time ``S``
  (``observed_at <= S``). This answers "what did we know at S".
* **valid time** (``valid_at`` / business time) — the asserted fact timeline:
  which revisions were *actually valid* at time ``V``
  (``valid_from <= V < valid_to``, open interval when ``valid_to`` is unset).
  This answers "what was true at V".

A bitemporal coordinate ``(valid_at, known_at)`` combines both axes, and the
topology/diff operations expose graph states and graph diffs as first-class
contracts. Suggested API routes (wired in apps/api, not here):

* ``POST /api/v1/graph/bitemporal/known-at``   — body ``{"known_at": S}``
* ``POST /api/v1/graph/bitemporal/valid-at``   — body ``{"valid_at": V}``
* ``POST /api/v1/graph/bitemporal/slice``      — body ``{"valid_at": V, "known_at": S}``
* ``POST /api/v1/graph/bitemporal/topology``   — body ``{"valid_at": V, "known_at": S}``
* ``POST /api/v1/graph/bitemporal/diff``       — body ``{"from": {...}, "to": {...}}``
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from eoip.graph.store import GraphStore

ENTITY_REVISION_LABEL = "EntityRevision"
RELATIONSHIP_REVISION_LABEL = "RelationshipRevision"


class BitemporalCoordinate(BaseModel):
    """A point in bitemporal space (GAP-TEMP-003)."""

    model_config = ConfigDict(extra="forbid")

    valid_at: str | None = Field(default=None, description="Valid-time coordinate; None = current valid time")
    known_at: str | None = Field(default=None, description="Transaction-time coordinate; None = latest knowledge")


class RevisionRecord(BaseModel):
    """A single revision selected by a bitemporal query."""

    model_config = ConfigDict(extra="forbid")

    revision_id: str
    subject_id: str
    kind: Literal["ENTITY", "RELATIONSHIP"]
    entity_type: str | None = None
    relationship_type: str | None = None
    from_id: str | None = None
    to_id: str | None = None
    observed_at: str
    valid_from: str | None = None
    valid_to: str | None = None
    graph_version: str | None = None
    is_delete: bool = False
    payload: dict[str, Any] = Field(default_factory=dict)


class BitemporalSlice(BaseModel):
    """Revision set selected at one bitemporal coordinate (GAP-TEMP-001..003)."""

    model_config = ConfigDict(extra="forbid")

    coordinate: BitemporalCoordinate
    entities: list[RevisionRecord] = Field(default_factory=list)
    relationships: list[RevisionRecord] = Field(default_factory=list)


class HistoricalEdge(BaseModel):
    model_config = ConfigDict(extra="forbid")

    relationship_id: str
    relationship_type: str
    from_id: str
    to_id: str
    revision_id: str


class BitemporalTopology(BaseModel):
    """Entity + edge set reconstructed at a bitemporal coordinate (GAP-TEMP-004)."""

    model_config = ConfigDict(extra="forbid")

    coordinate: BitemporalCoordinate
    entity_ids: list[str] = Field(default_factory=list)
    edges: list[HistoricalEdge] = Field(default_factory=list)
    entity_count: int = 0
    edge_count: int = 0


class ItemDiff(BaseModel):
    model_config = ConfigDict(extra="forbid")

    added: list[str] = Field(default_factory=list)
    removed: list[str] = Field(default_factory=list)
    changed: list[str] = Field(default_factory=list)


class BitemporalDiff(BaseModel):
    """First-class diff between two bitemporal coordinates (GAP-TEMP-005)."""

    model_config = ConfigDict(extra="forbid")

    diff_id: str
    from_coordinate: BitemporalCoordinate
    to_coordinate: BitemporalCoordinate
    entities: ItemDiff
    relationships: ItemDiff
    edges: ItemDiff
    summary: dict[str, int] = Field(default_factory=dict)


class BitemporalDiffRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    from_coordinate: BitemporalCoordinate
    to_coordinate: BitemporalCoordinate


def _window_open(valid_to: Any) -> bool:
    return valid_to is None or valid_to == ""


def _valid_at(properties: dict[str, Any], at: str) -> bool:
    valid_from = properties.get("valid_from") or ""
    if valid_from > at:
        return False
    valid_to = properties.get("valid_to")
    return _window_open(valid_to) or at < valid_to


def _parse_revision(item: dict[str, Any], kind: Literal["ENTITY", "RELATIONSHIP"]) -> RevisionRecord:
    props = item["properties"]
    payload = json.loads(props.get("payload_json") or "{}")
    return RevisionRecord(
        revision_id=props.get("revision_id", ""),
        subject_id=props.get("subject_id") or props.get("relationship_id", ""),
        kind=kind,
        entity_type=props.get("entity_type"),
        relationship_type=props.get("relationship_type"),
        from_id=props.get("from_id"),
        to_id=props.get("to_id"),
        observed_at=props.get("observed_at", ""),
        valid_from=props.get("valid_from"),
        valid_to=props.get("valid_to") or None,
        graph_version=props.get("graph_version"),
        is_delete=payload.get("operation") == "DELETE",
        payload=payload,
    )


class BitemporalQueryEngine:
    """Dual-time reads over the EntityRevision / RelationshipRevision journal."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    # -- revision selection -------------------------------------------------

    def _select(
        self,
        label: str,
        kind: Literal["ENTITY", "RELATIONSHIP"],
        *,
        known_at: str | None,
        valid_at: str | None,
    ) -> list[RevisionRecord]:
        items = self._store.find_vertices(label=label, limit=100_000)
        selected: list[RevisionRecord] = []
        for item in items:
            props = item["properties"]
            if known_at is not None and props.get("observed_at", "") > known_at:
                continue
            if valid_at is not None and not _valid_at(props, valid_at):
                continue
            selected.append(_parse_revision(item, kind))
        return selected

    @staticmethod
    def _latest_per_subject(records: list[RevisionRecord]) -> list[RevisionRecord]:
        best: dict[str, RevisionRecord] = {}
        for record in records:
            current = best.get(record.subject_id)
            if current is None or (record.observed_at, record.revision_id) > (
                current.observed_at,
                current.revision_id,
            ):
                best[record.subject_id] = record
        return [best[key] for key in sorted(best)]

    # -- public queries ------------------------------------------------------

    def known_at(self, system_time: str) -> BitemporalSlice:
        """GAP-TEMP-001: latest revision per subject known at system time T."""
        return BitemporalSlice(
            coordinate=BitemporalCoordinate(known_at=system_time),
            entities=self._latest_per_subject(
                self._select(ENTITY_REVISION_LABEL, "ENTITY", known_at=system_time, valid_at=None)
            ),
            relationships=self._latest_per_subject(
                self._select(RELATIONSHIP_REVISION_LABEL, "RELATIONSHIP", known_at=system_time, valid_at=None)
            ),
        )

    def valid_at(self, valid_time: str) -> BitemporalSlice:
        """GAP-TEMP-002: revisions whose valid window covers valid time T."""
        return BitemporalSlice(
            coordinate=BitemporalCoordinate(valid_at=valid_time),
            entities=sorted(
                self._select(ENTITY_REVISION_LABEL, "ENTITY", known_at=None, valid_at=valid_time),
                key=lambda record: record.subject_id,
            ),
            relationships=sorted(
                self._select(RELATIONSHIP_REVISION_LABEL, "RELATIONSHIP", known_at=None, valid_at=valid_time),
                key=lambda record: record.subject_id,
            ),
        )

    def slice(self, valid_at: str, known_at: str) -> BitemporalSlice:
        """GAP-TEMP-003: valid at V as known at S (latest revision per subject)."""
        return BitemporalSlice(
            coordinate=BitemporalCoordinate(valid_at=valid_at, known_at=known_at),
            entities=self._latest_per_subject(
                self._select(ENTITY_REVISION_LABEL, "ENTITY", known_at=known_at, valid_at=valid_at)
            ),
            relationships=self._latest_per_subject(
                self._select(RELATIONSHIP_REVISION_LABEL, "RELATIONSHIP", known_at=known_at, valid_at=valid_at)
            ),
        )

    def topology(self, valid_at: str, known_at: str) -> BitemporalTopology:
        """GAP-TEMP-004: reconstruct entity + edge set at a bitemporal coordinate."""
        state = self.slice(valid_at, known_at)
        entities = {record.subject_id for record in state.entities if not record.is_delete}
        edges: list[HistoricalEdge] = []
        for record in state.relationships:
            if record.is_delete:
                continue
            if record.from_id not in entities or record.to_id not in entities:
                continue
            edges.append(
                HistoricalEdge(
                    relationship_id=record.subject_id,
                    relationship_type=record.relationship_type or "",
                    from_id=record.from_id or "",
                    to_id=record.to_id or "",
                    revision_id=record.revision_id,
                )
            )
        edges.sort(key=lambda edge: edge.relationship_id)
        return BitemporalTopology(
            coordinate=state.coordinate,
            entity_ids=sorted(entities),
            edges=edges,
            entity_count=len(entities),
            edge_count=len(edges),
        )

    def diff(self, from_coordinate: BitemporalCoordinate, to_coordinate: BitemporalCoordinate) -> BitemporalDiff:
        """GAP-TEMP-005: graph diff between two bitemporal coordinates."""
        before = self._topology_for(from_coordinate)
        after = self._topology_for(to_coordinate)
        entity_diff = _diff_sets(set(before.entity_ids), set(after.entity_ids))
        edge_before = {(edge.relationship_id, edge.relationship_type, edge.from_id, edge.to_id) for edge in before.edges}
        edge_after = {(edge.relationship_id, edge.relationship_type, edge.from_id, edge.to_id) for edge in after.edges}
        edge_keys_before = {item[0] for item in edge_before}
        edge_keys_after = {item[0] for item in edge_after}
        rel_diff = _diff_sets(edge_keys_before, edge_keys_after)
        changed_edges = sorted(
            key for key in edge_keys_before & edge_keys_after
            if {item for item in edge_before if item[0] == key} != {item for item in edge_after if item[0] == key}
        )
        fingerprint = json.dumps(
            {
                "from": from_coordinate.model_dump(),
                "to": to_coordinate.model_dump(),
                "entities": entity_diff.model_dump(),
                "relationships": rel_diff.model_dump(),
            },
            sort_keys=True,
        )
        diff_id = "urn:eoip:bitemporal:diff:" + hashlib.sha256(fingerprint.encode()).hexdigest()[:24]
        return BitemporalDiff(
            diff_id=diff_id,
            from_coordinate=from_coordinate,
            to_coordinate=to_coordinate,
            entities=entity_diff,
            relationships=rel_diff,
            edges=ItemDiff(added=rel_diff.added, removed=rel_diff.removed, changed=changed_edges),
            summary={
                "entities_added": len(entity_diff.added),
                "entities_removed": len(entity_diff.removed),
                "entities_changed": len(entity_diff.changed),
                "edges_added": len(rel_diff.added),
                "edges_removed": len(rel_diff.removed),
                "edges_changed": len(changed_edges),
            },
        )

    def _topology_for(self, coordinate: BitemporalCoordinate) -> BitemporalTopology:
        if coordinate.valid_at is not None and coordinate.known_at is not None:
            return self.topology(coordinate.valid_at, coordinate.known_at)
        if coordinate.known_at is not None:
            state = self.known_at(coordinate.known_at)
        elif coordinate.valid_at is not None:
            state = self.valid_at(coordinate.valid_at)
        else:
            state = self.known_at("\uffff")
        entities = {record.subject_id for record in state.entities if not record.is_delete}
        edges = [
            HistoricalEdge(
                relationship_id=record.subject_id,
                relationship_type=record.relationship_type or "",
                from_id=record.from_id or "",
                to_id=record.to_id or "",
                revision_id=record.revision_id,
            )
            for record in state.relationships
            if not record.is_delete and record.from_id in entities and record.to_id in entities
        ]
        edges.sort(key=lambda edge: edge.relationship_id)
        return BitemporalTopology(
            coordinate=coordinate,
            entity_ids=sorted(entities),
            edges=edges,
            entity_count=len(entities),
            edge_count=len(edges),
        )


def _diff_sets(before: set[str], after: set[str]) -> ItemDiff:
    return ItemDiff(
        added=sorted(after - before),
        removed=sorted(before - after),
        changed=[],
    )


# ---------------------------------------------------------------------------
# HTTP surface (wired by apps/api; not registered here)
# ---------------------------------------------------------------------------

def build_router(store: GraphStore):
    """Construct the FastAPI router bound to a GraphStore.

    The API wiring step (apps/api/app.py) calls ``build_router(store)`` —
    no apps/api changes required in this module. Routes (all POST):
    ``/api/v1/graph/bitemporal/known-at``, ``/valid-at``, ``/slice``,
    ``/topology``, ``/diff``.
    """
    from fastapi import APIRouter, Body

    router = APIRouter(prefix="/api/v1/graph/bitemporal", tags=["bitemporal"])
    engine = BitemporalQueryEngine(store)

    @router.post("/known-at", response_model=BitemporalSlice)
    def known_at(coordinate: BitemporalCoordinate) -> BitemporalSlice:
        return engine.known_at(coordinate.known_at or "")

    @router.post("/valid-at", response_model=BitemporalSlice)
    def valid_at(coordinate: BitemporalCoordinate) -> BitemporalSlice:
        return engine.valid_at(coordinate.valid_at or "")

    @router.post("/slice", response_model=BitemporalSlice)
    def slice_(coordinate: BitemporalCoordinate) -> BitemporalSlice:
        return engine.slice(coordinate.valid_at or "", coordinate.known_at or "")

    @router.post("/topology", response_model=BitemporalTopology)
    def topology(coordinate: BitemporalCoordinate) -> BitemporalTopology:
        return engine.topology(coordinate.valid_at or "", coordinate.known_at or "")

    @router.post("/diff", response_model=BitemporalDiff)
    def diff_(body: BitemporalDiffRequest = Body(...)) -> BitemporalDiff:
        return engine.diff(body.from_coordinate, body.to_coordinate)

    return router
