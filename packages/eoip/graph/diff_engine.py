"""Knowledge Graph Diff & Change Intelligence — track, compare, and explain graph changes."""

from __future__ import annotations

import time
import uuid
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class ChangeType(str, Enum):
    ENTITY_ADDED = "ENTITY_ADDED"
    ENTITY_REMOVED = "ENTITY_REMOVED"
    ENTITY_MODIFIED = "ENTITY_MODIFIED"
    EDGE_ADDED = "EDGE_ADDED"
    EDGE_REMOVED = "EDGE_REMOVED"
    PROPERTY_CHANGED = "PROPERTY_CHANGED"
    LABEL_CHANGED = "LABEL_CHANGED"


class ChangeImpact(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class Change:
    change_id: str
    change_type: ChangeType
    entity_id: str
    entity_label: str = ""
    old_value: Any = None
    new_value: Any = None
    property_name: str = ""
    timestamp: str = ""
    source: str = ""
    impact: ChangeImpact = ChangeImpact.LOW

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["change_type"] = self.change_type.value
        d["impact"] = self.impact.value
        return d


@dataclass
class DiffResult:
    diff_id: str
    snapshot_a: str
    snapshot_b: str
    changes: list[Change] = field(default_factory=list)
    summary: dict[str, int] = field(default_factory=dict)
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "diff_id": self.diff_id,
            "snapshot_a": self.snapshot_a,
            "snapshot_b": self.snapshot_b,
            "total_changes": len(self.changes),
            "summary": self.summary,
            "changes": [c.to_dict() for c in self.changes],
            "created_at": self.created_at,
        }


@dataclass
class ChangeTimeline:
    entity_id: str
    changes: list[Change] = field(default_factory=list)
    first_seen: str = ""
    last_modified: str = ""
    total_modifications: int = 0


class GraphDiffEngine:
    """Computes diffs between graph states and tracks change history."""

    def __init__(self) -> None:
        self._change_log: list[Change] = []
        self._diffs: dict[str, DiffResult] = {}
        self._entity_timeline: dict[str, list[Change]] = defaultdict(list)
        self._max_log_size = 50000

    def record_change(self, change_type: ChangeType, entity_id: str,
                      entity_label: str = "", old_value: Any = None,
                      new_value: Any = None, property_name: str = "",
                      source: str = "", impact: ChangeImpact = ChangeImpact.LOW) -> Change:
        cid = uuid.uuid4().hex[:10]
        change = Change(
            change_id=cid, change_type=change_type, entity_id=entity_id,
            entity_label=entity_label, old_value=old_value, new_value=new_value,
            property_name=property_name, source=source, impact=impact,
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        )
        self._change_log.append(change)
        self._entity_timeline[entity_id].append(change)
        if len(self._change_log) > self._max_log_size:
            self._change_log = self._change_log[-self._max_log_size:]
        return change

    def diff(self, state_a: dict[str, Any], state_b: dict[str, Any],
             label_a: str = "before", label_b: str = "after") -> DiffResult:
        did = uuid.uuid4().hex[:10]
        changes: list[Change] = []
        entities_a = state_a.get("entities", {})
        entities_b = state_b.get("entities", {})
        keys_a = set(entities_a.keys())
        keys_b = set(entities_b.keys())

        for eid in keys_b - keys_a:
            changes.append(Change(
                change_id=uuid.uuid4().hex[:10],
                change_type=ChangeType.ENTITY_ADDED,
                entity_id=eid,
                entity_label=entities_b[eid].get("label", ""),
                new_value=entities_b[eid],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            ))

        for eid in keys_a - keys_b:
            changes.append(Change(
                change_id=uuid.uuid4().hex[:10],
                change_type=ChangeType.ENTITY_REMOVED,
                entity_id=eid,
                entity_label=entities_a[eid].get("label", ""),
                old_value=entities_a[eid],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            ))

        for eid in keys_a & keys_b:
            ea = entities_a[eid]
            eb = entities_b[eid]
            props_a = ea.get("properties", ea)
            props_b = eb.get("properties", eb)
            if props_a != props_b:
                for key in set(list(props_a.keys()) + list(props_b.keys())):
                    va = props_a.get(key)
                    vb = props_b.get(key)
                    if va != vb:
                        changes.append(Change(
                            change_id=uuid.uuid4().hex[:10],
                            change_type=ChangeType.PROPERTY_CHANGED,
                            entity_id=eid, property_name=key,
                            old_value=va, new_value=vb,
                            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        ))

        edges_a = set(tuple(sorted(e.items())) for e in state_a.get("edges", []) if isinstance(e, dict))
        edges_b = set(tuple(sorted(e.items())) for e in state_b.get("edges", []) if isinstance(e, dict))
        for edge in edges_b - edges_a:
            ed = dict(edge)
            changes.append(Change(
                change_id=uuid.uuid4().hex[:10],
                change_type=ChangeType.EDGE_ADDED,
                entity_id=ed.get("source", ""),
                new_value=ed,
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            ))
        for edge in edges_a - edges_b:
            ed = dict(edge)
            changes.append(Change(
                change_id=uuid.uuid4().hex[:10],
                change_type=ChangeType.EDGE_REMOVED,
                entity_id=ed.get("source", ""),
                old_value=ed,
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            ))

        summary: dict[str, int] = defaultdict(int)
        for c in changes:
            summary[c.change_type.value] += 1

        result = DiffResult(
            diff_id=did, snapshot_a=label_a, snapshot_b=label_b,
            changes=changes, summary=dict(summary),
            created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        )
        self._diffs[did] = result
        return result

    def get_entity_timeline(self, entity_id: str) -> ChangeTimeline:
        changes = self._entity_timeline.get(entity_id, [])
        return ChangeTimeline(
            entity_id=entity_id, changes=changes,
            first_seen=changes[0].timestamp if changes else "",
            last_modified=changes[-1].timestamp if changes else "",
            total_modifications=len(changes),
        )

    def get_recent_changes(self, limit: int = 50,
                           change_type: ChangeType | None = None) -> list[dict[str, Any]]:
        filtered = self._change_log
        if change_type:
            filtered = [c for c in filtered if c.change_type == change_type]
        return [c.to_dict() for c in filtered[-limit:]]

    def get_change_stats(self) -> dict[str, Any]:
        by_type: dict[str, int] = defaultdict(int)
        by_impact: dict[str, int] = defaultdict(int)
        for c in self._change_log:
            by_type[c.change_type.value] += 1
            by_impact[c.impact.value] += 1
        return {
            "total_changes": len(self._change_log),
            "by_type": dict(by_type),
            "by_impact": dict(by_impact),
            "entities_tracked": len(self._entity_timeline),
        }
