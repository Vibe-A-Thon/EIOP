"""Incremental Materialized Views — pre-computed graph views with incremental updates.

Maintains cached graph projections (impact subgraphs, dependency trees,
hot-path caches) that update incrementally on mutations rather than
full recomputation.
"""

from __future__ import annotations

import hashlib
import threading
import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any
from collections.abc import Callable


class ViewType(str, Enum):
    SUBGRAPH = "SUBGRAPH"
    AGGREGATION = "AGGREGATION"
    PROJECTION = "PROJECTION"
    DEPENDENCY_TREE = "DEPENDENCY_TREE"
    IMPACT_GRAPH = "IMPACT_GRAPH"
    METRIC_ROLLUP = "METRIC_ROLLUP"
    TRAVERSAL_CACHE = "TRAVERSAL_CACHE"


class ViewStatus(str, Enum):
    FRESH = "FRESH"
    STALE = "STALE"
    REFRESHING = "REFRESHING"
    ERROR = "ERROR"
    DISABLED = "DISABLED"


@dataclass
class ViewDefinition:
    view_id: str
    name: str
    view_type: ViewType
    source_query: str
    entity_labels: list[str] = field(default_factory=list)
    edge_labels: list[str] = field(default_factory=list)
    refresh_policy: str = "on_mutation"  # on_mutation, periodic, manual
    refresh_interval_seconds: int = 300
    ttl_seconds: int = 3600
    max_cache_size: int = 10000
    enabled: bool = True

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["view_type"] = self.view_type.value
        return d


@dataclass
class MaterializedView:
    view_id: str
    definition: ViewDefinition
    data: dict[str, Any] = field(default_factory=dict)
    status: ViewStatus = ViewStatus.STALE
    entity_count: int = 0
    edge_count: int = 0
    last_refresh: str | None = None
    last_mutation: str | None = None
    refresh_count: int = 0
    refresh_duration_ms: int = 0
    version: int = 0
    checksum: str = ""

    def is_expired(self) -> bool:
        if not self.last_refresh:
            return True
        try:
            ts = time.strptime(self.last_refresh, "%Y-%m-%dT%H:%M:%SZ")
            age = time.time() - time.mktime(ts)
            return age > self.definition.ttl_seconds
        except (ValueError, OverflowError):
            return True


@dataclass
class MutationEvent:
    event_type: str  # vertex_added, vertex_updated, vertex_deleted, edge_added, edge_deleted
    entity_id: str
    entity_label: str
    properties: dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""


class MaterializedViewManager:
    """Manages materialized views with incremental refresh on graph mutations."""

    def __init__(self) -> None:
        self._definitions: dict[str, ViewDefinition] = {}
        self._views: dict[str, MaterializedView] = {}
        self._label_subscriptions: dict[str, set[str]] = defaultdict(set)
        self._refresh_functions: dict[str, Callable] = {}
        self._lock = threading.RLock()

    def register_view(self, definition: ViewDefinition,
                      refresh_fn: Callable | None = None) -> MaterializedView:
        with self._lock:
            self._definitions[definition.view_id] = definition
            view = MaterializedView(view_id=definition.view_id, definition=definition)
            self._views[definition.view_id] = view

            for label in definition.entity_labels:
                self._label_subscriptions[label].add(definition.view_id)
            for label in definition.edge_labels:
                self._label_subscriptions[label].add(definition.view_id)

            if refresh_fn:
                self._refresh_functions[definition.view_id] = refresh_fn

            return view

    def unregister_view(self, view_id: str) -> bool:
        with self._lock:
            defn = self._definitions.pop(view_id, None)
            self._views.pop(view_id, None)
            self._refresh_functions.pop(view_id, None)
            if defn:
                for label in defn.entity_labels + defn.edge_labels:
                    self._label_subscriptions[label].discard(view_id)
                return True
            return False

    def get_view(self, view_id: str) -> MaterializedView | None:
        view = self._views.get(view_id)
        if view and view.is_expired():
            view.status = ViewStatus.STALE
        return view

    def query_view(self, view_id: str) -> dict[str, Any]:
        view = self._views.get(view_id)
        if not view:
            raise ValueError(f"View {view_id} not found")

        if view.status == ViewStatus.STALE or view.is_expired():
            self.refresh_view(view_id)

        return {
            "view_id": view_id,
            "status": view.status.value,
            "data": view.data,
            "entity_count": view.entity_count,
            "edge_count": view.edge_count,
            "version": view.version,
            "last_refresh": view.last_refresh,
            "checksum": view.checksum,
        }

    def on_mutation(self, event: MutationEvent) -> list[str]:
        affected = self._label_subscriptions.get(event.entity_label, set())
        refreshed: list[str] = []

        for view_id in affected:
            view = self._views.get(view_id)
            if not view or not view.definition.enabled:
                continue

            view.last_mutation = event.timestamp or time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

            if view.definition.refresh_policy == "on_mutation":
                self._incremental_update(view, event)
                refreshed.append(view_id)
            else:
                view.status = ViewStatus.STALE

        return refreshed

    def refresh_view(self, view_id: str) -> bool:
        with self._lock:
            view = self._views.get(view_id)
            if not view:
                return False

            view.status = ViewStatus.REFRESHING
            t0 = time.time()

            refresh_fn = self._refresh_functions.get(view_id)
            if refresh_fn:
                try:
                    result = refresh_fn(view.definition)
                    view.data = result.get("data", {})
                    view.entity_count = result.get("entity_count", 0)
                    view.edge_count = result.get("edge_count", 0)
                except Exception:
                    view.status = ViewStatus.ERROR
                    return False
            else:
                self._default_refresh(view)

            ms = int((time.time() - t0) * 1000)
            view.status = ViewStatus.FRESH
            view.last_refresh = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            view.refresh_count += 1
            view.refresh_duration_ms = ms
            view.version += 1
            view.checksum = hashlib.sha256(
                str(view.data).encode()
            ).hexdigest()[:16]
            return True

    def refresh_stale(self) -> list[str]:
        refreshed: list[str] = []
        for view_id, view in self._views.items():
            if view.status == ViewStatus.STALE or view.is_expired():
                if self.refresh_view(view_id):
                    refreshed.append(view_id)
        return refreshed

    def list_views(self) -> list[dict[str, Any]]:
        return [
            {
                "view_id": v.view_id,
                "name": v.definition.name,
                "type": v.definition.view_type.value,
                "status": v.status.value,
                "entity_count": v.entity_count,
                "version": v.version,
                "last_refresh": v.last_refresh,
            }
            for v in self._views.values()
        ]

    def get_metrics(self) -> dict[str, Any]:
        total = len(self._views)
        fresh = sum(1 for v in self._views.values() if v.status == ViewStatus.FRESH)
        stale = sum(1 for v in self._views.values() if v.status == ViewStatus.STALE)
        total_entities = sum(v.entity_count for v in self._views.values())
        return {
            "total_views": total,
            "fresh": fresh,
            "stale": stale,
            "total_cached_entities": total_entities,
            "subscribed_labels": len(self._label_subscriptions),
        }

    def _incremental_update(self, view: MaterializedView, event: MutationEvent) -> None:
        entities = view.data.setdefault("entities", {})
        if event.event_type in ("vertex_added", "vertex_updated"):
            entities[event.entity_id] = {
                "label": event.entity_label,
                "properties": event.properties,
                "updated_at": event.timestamp,
            }
            view.entity_count = len(entities)
        elif event.event_type == "vertex_deleted":
            if event.entity_id in entities:
                del entities[event.entity_id]
                view.entity_count = len(entities)
        elif event.event_type in ("edge_added",):
            edges = view.data.setdefault("edges", [])
            edges.append({
                "source": event.properties.get("source"),
                "target": event.properties.get("target"),
                "label": event.entity_label,
            })
            view.edge_count = len(edges)

        view.version += 1
        view.status = ViewStatus.FRESH
        view.last_refresh = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def _default_refresh(self, view: MaterializedView) -> None:
        view.data = {"entities": {}, "edges": [], "query": view.definition.source_query}
        view.entity_count = 0
        view.edge_count = 0
