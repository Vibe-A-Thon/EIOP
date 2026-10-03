"""Temporal graph evolution, semantic journal and local event bus (G2-P2)."""

from __future__ import annotations

import hashlib
import json
import os
import threading
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from eoip.contracts.source_event import SourceEventV2
from eoip.graph.store import GraphStore
from pydantic import BaseModel, ConfigDict, Field


class SemanticChangeEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0"] = "1.0"
    cursor: int = Field(ge=1)
    graph_version: str
    change_kind: Literal["CREATE", "UPDATE", "DELETE", "LATE_EVENT"]
    target_kind: Literal["ENTITY", "RELATIONSHIP"]
    target_id: str
    source_event_id: str
    observed_at: str
    details: dict[str, Any] = Field(default_factory=dict)
    previous_hash: str | None = None
    entry_hash: str


class ChangeJournal:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._lock = threading.RLock()

    def append(self, event: dict[str, Any]) -> SemanticChangeEvent:
        with self._lock:
            entries = self.read(limit=None)
            cursor = entries[-1].cursor + 1 if entries else 1
            previous_hash = entries[-1].entry_hash if entries else None
            body = {**event, "schema_version": "1.0", "cursor": cursor, "previous_hash": previous_hash}
            digest = hashlib.sha256(
                json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ).hexdigest()
            record = SemanticChangeEvent(**body, entry_hash=digest)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as output:
                output.write(record.model_dump_json() + "\n")
                output.flush()
                os.fsync(output.fileno())
            return record

    def read(self, *, after: int = 0, limit: int | None = 100) -> list[SemanticChangeEvent]:
        if not self.path.exists():
            return []
        records = [
            SemanticChangeEvent.model_validate_json(line)
            for line in self.path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        previous = None
        for record in records:
            body = record.model_dump(exclude={"entry_hash"})
            expected = hashlib.sha256(
                json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ).hexdigest()
            if record.previous_hash != previous or record.entry_hash != expected:
                raise ValueError("semantic change journal integrity check failed")
            previous = record.entry_hash
        selected = [record for record in records if record.cursor > after]
        return selected if limit is None else selected[:limit]


class SemanticEventBus:
    def __init__(self) -> None:
        self._subscribers: list[Callable[[SemanticChangeEvent], None]] = []

    def subscribe(self, consumer: Callable[[SemanticChangeEvent], None]) -> None:
        self._subscribers.append(consumer)

    def publish(self, event: SemanticChangeEvent) -> None:
        for consumer in tuple(self._subscribers):
            consumer(event)


class GraphEvolutionEngine:
    def __init__(self, store: GraphStore, journal: ChangeJournal, bus: SemanticEventBus | None = None) -> None:
        self.store = store
        self.journal = journal
        self.bus = bus or SemanticEventBus()
        self._lock = threading.RLock()

    def evolve_entity(
        self,
        label: str,
        canonical_id: str,
        properties: dict[str, Any],
        event: SourceEventV2,
    ) -> dict[str, Any]:
        with self._lock:
            current_revision = self._current("EntityRevision", "subject_id", canonical_id)
            if current_revision and self._is_late(event.event_time, current_revision["properties"]["observed_at"]):
                return self._record("LATE_EVENT", "ENTITY", canonical_id, event, {}, mutate=False)
            state = {"label": label, "properties": {**properties, "canonical_id": canonical_id}}
            if event.operation == "DELETE":
                state["operation"] = "DELETE"
            revision_id, unchanged = self._revision_for_state(
                "ENTITY", canonical_id, state, event, current_revision
            )
            if unchanged:
                return {"status": "UNCHANGED", "revision_id": revision_id}
            observed_at = event.event_time
            change = "CREATE" if self.store.get_vertex_by_canonical_id(canonical_id) is None else "UPDATE"
            if event.operation == "DELETE":
                change = "DELETE"
            version = self._graph_version(event, canonical_id, revision_id)
            if current_revision:
                self._close_revision(current_revision, observed_at)
            if change == "DELETE":
                self.store.tombstone_vertex(canonical_id)
            else:
                self.store.upsert_vertex(
                    label,
                    {
                        **properties,
                        "canonical_id": canonical_id,
                        "content_hash": event.content_hash,
                        "source_version": event.source_version,
                        "modified_at": observed_at,
                        "valid_from": observed_at,
                        "deleted_at": "",
                    },
                )
            self._create_entity_revision(
                canonical_id, label, state, revision_id, current_revision, version, event
            )
            return self._record(change, "ENTITY", canonical_id, event, {"revision_id": revision_id}, version)

    def evolve_relationship(
        self,
        relationship_id: str,
        relationship_type: str,
        from_id: str,
        to_id: str,
        properties: dict[str, Any],
        event: SourceEventV2,
    ) -> dict[str, Any]:
        with self._lock:
            current = self._current("RelationshipRevision", "relationship_id", relationship_id)
            if current and self._is_late(event.event_time, current["properties"]["observed_at"]):
                return self._record("LATE_EVENT", "RELATIONSHIP", relationship_id, event, {}, mutate=False)
            state = {
                "relationship_type": relationship_type,
                "from_id": from_id,
                "to_id": to_id,
                "properties": properties,
            }
            if event.operation == "DELETE":
                state["operation"] = "DELETE"
            revision_id, unchanged = self._revision_for_state(
                "RELATIONSHIP", relationship_id, state, event, current
            )
            if unchanged:
                return {"status": "UNCHANGED", "revision_id": revision_id}
            observed_at = event.event_time
            change = "CREATE" if current is None else "UPDATE"
            if event.operation == "DELETE":
                change = "DELETE"
            version = self._graph_version(event, relationship_id, revision_id)
            if change != "DELETE":
                source = self.store.get_vertex_by_canonical_id(from_id)
                target = self.store.get_vertex_by_canonical_id(to_id)
                if source is None or target is None:
                    raise ValueError("relationship endpoints must exist before evolution")
                edge_properties = {
                    **properties,
                    "fact_key": relationship_id,
                    # Per-revision edge identity: each revision is its own
                    # physical edge so history is preserved on the graph and
                    # the new current edge can be created BEFORE the old one
                    # is expired — concurrent readers always observe a
                    # consistent current state (no visibility gap).
                    "edge_key": f"{relationship_id}:{revision_id}",
                    "is_current": True,
                    "valid_from": observed_at,
                    "valid_to": "",
                    "source_event_id": event.event_id,
                    "source_version": event.source_version,
                    "graph_version": version,
                }
                self.store.upsert_edge(
                    relationship_type, source["vid"], target["vid"], edge_properties
                )
            if current:
                self._close_revision(current, observed_at)
                self._expire_relationship(current, observed_at)
            self._create_relationship_revision(
                relationship_id, state, revision_id, current, version, event
            )
            return self._record(
                change,
                "RELATIONSHIP",
                relationship_id,
                event,
                {"revision_id": revision_id},
                version,
            )

    def as_of(self, at: str, *, limit: int = 500) -> dict[str, list[dict[str, Any]]]:
        entities = self._active_revisions("EntityRevision", at, limit)
        relationships = self._active_revisions("RelationshipRevision", at, limit)
        return {
            "at": at,
            "entities": [json.loads(item["properties"]["payload_json"]) for item in entities],
            "relationships": [json.loads(item["properties"]["payload_json"]) for item in relationships],
        }

    def diff(self, from_at: str, to_at: str, *, limit: int = 500) -> dict[str, Any]:
        before, after = self.as_of(from_at, limit=limit), self.as_of(to_at, limit=limit)
        return {
            "from": from_at,
            "to": to_at,
            "entities": self._diff_items(before["entities"], after["entities"], "canonical_id"),
            "relationships": self._diff_items(
                before["relationships"], after["relationships"], "relationship_id"
            ),
        }

    def versions(self, limit: int = 100) -> list[dict[str, Any]]:
        return [item["properties"] for item in self.store.find_vertices(label="GraphVersion", limit=limit)]

    def _create_entity_revision(self, cid, label, state, rid, previous, version, event) -> None:
        self.store.upsert_vertex(
            "EntityRevision",
            {
                "canonical_id": f"urn:eoip:revision:entity:{rid}",
                "revision_id": rid,
                "subject_id": cid,
                "entity_type": label,
                "observed_at": event.event_time,
                "valid_from": event.event_time,
                "valid_to": "",
                "is_current": True,
                "previous_revision": previous["properties"]["revision_id"] if previous else None,
                "source_version": event.source_version,
                "graph_version": version,
                "source_event_id": event.event_id,
                "content_hash": event.content_hash,
                "payload_json": json.dumps({**state, "canonical_id": cid}, sort_keys=True),
            },
        )

    def _create_relationship_revision(self, rel_id, state, rid, previous, version, event) -> None:
        self.store.upsert_vertex(
            "RelationshipRevision",
            {
                "canonical_id": f"urn:eoip:revision:relationship:{rid}",
                "revision_id": rid,
                "relationship_id": rel_id,
                "relationship_type": state["relationship_type"],
                "from_id": state["from_id"],
                "to_id": state["to_id"],
                "observed_at": event.event_time,
                "valid_from": event.event_time,
                "valid_to": "",
                "is_current": True,
                "previous_revision": previous["properties"]["revision_id"] if previous else None,
                "source_version": event.source_version,
                "graph_version": version,
                "source_event_id": event.event_id,
                "content_hash": event.content_hash,
                "payload_json": json.dumps({**state, "relationship_id": rel_id}, sort_keys=True),
            },
        )

    def _close_revision(self, revision: dict, at: str) -> None:
        self.store.upsert_vertex(
            revision["label"], {**revision["properties"], "is_current": False, "valid_to": at}
        )

    def _expire_relationship(self, revision: dict, at: str) -> None:
        props = revision["properties"]
        state = json.loads(props["payload_json"])
        source = self.store.get_vertex_by_canonical_id(state["from_id"])
        target = self.store.get_vertex_by_canonical_id(state["to_id"])
        if source and target:
            self.store.upsert_edge(
                state["relationship_type"],
                source["vid"],
                target["vid"],
                {
                    **state.get("properties", {}),
                    "fact_key": props["relationship_id"],
                    # Target the exact physical edge created for this revision
                    # (see evolve_relationship) so expiry cannot create a
                    # parallel edge or miss the current one.
                    "edge_key": f"{props['relationship_id']}:{props['revision_id']}",
                    "is_current": False,
                    "valid_to": at,
                },
            )

    def _record(self, change, kind, target, event, details, version=None, mutate=True):
        version = version or self._graph_version(event, target, change)
        if mutate:
            self.store.upsert_vertex(
                "GraphVersion",
                {
                    "canonical_id": f"urn:eoip:graph-version:{version}",
                    "graph_version": version,
                    "created_at": event.event_time,
                    "source_event_id": event.event_id,
                    "change_kind": change,
                },
            )
        recorded = self.journal.append(
            {
                "graph_version": version,
                "change_kind": change,
                "target_kind": kind,
                "target_id": target,
                "source_event_id": event.event_id,
                "observed_at": event.event_time,
                "details": details,
            }
        )
        self.bus.publish(recorded)
        return {"status": "LATE_IGNORED" if change == "LATE_EVENT" else change, "graph_version": version, "cursor": recorded.cursor, **details}

    def _current(self, label: str, field: str, value: str):
        matches = self.store.find_vertices(label=label, filters={field: value, "is_current": True}, limit=2)
        if len(matches) > 1:
            raise RuntimeError(f"multiple current revisions for {value}")
        return matches[0] if matches else None

    def _active_revisions(self, label: str, at: str, limit: int):
        items = self.store.find_vertices(label=label, limit=100_000)
        active = [
            item
            for item in items
            if item["properties"].get("valid_from", "") <= at
            and (not item["properties"].get("valid_to") or at < item["properties"]["valid_to"])
            and json.loads(item["properties"]["payload_json"]).get("operation") != "DELETE"
        ]
        return active[:limit]

    def _revision_for_state(self, kind, target, state, event, current) -> tuple[str, bool]:
        revision_id = self._revision_id(kind, target, state, event)
        identity_key = "canonical_id" if kind == "ENTITY" else "relationship_id"
        if current:
            props = current["properties"]
            if props["revision_id"] == revision_id or (
                props.get("content_hash") == event.content_hash
                and json.loads(props["payload_json"]) == {**state, identity_key: target}
            ):
                return props["revision_id"], True
        if self.store.get_vertex_by_canonical_id(f"urn:eoip:revision:{kind.lower()}:{revision_id}"):
            # Equal content in a later interval must not overwrite its earlier revision.
            revision_id = hashlib.sha256(
                f"{revision_id}|{event.event_time}|{event.event_id}".encode()
            ).hexdigest()
        return revision_id, False

    @staticmethod
    def _revision_id(kind, target, state, event):
        body = json.dumps(state, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(f"{kind}|{target}|{event.content_hash}|{body}".encode()).hexdigest()

    @staticmethod
    def _graph_version(event, target, revision):
        return hashlib.sha256(f"{event.event_time}|{event.event_id}|{target}|{revision}".encode()).hexdigest()[:24]

    @staticmethod
    def _is_late(candidate: str, current: str) -> bool:
        return datetime.fromisoformat(candidate) < datetime.fromisoformat(current)

    @staticmethod
    def _diff_items(before, after, key):
        left, right = {item[key]: item for item in before}, {item[key]: item for item in after}
        return {
            "added": [right[item] for item in sorted(right.keys() - left.keys())],
            "removed": [left[item] for item in sorted(left.keys() - right.keys())],
            "changed": [
                {"before": left[item], "after": right[item]}
                for item in sorted(left.keys() & right.keys())
                if left[item] != right[item]
            ],
        }
