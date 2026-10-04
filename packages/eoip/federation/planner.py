"""Federated query planner (GAP-FABRIC-001..008).

Provides a source capability registry, a fragment planner that splits a
semantic query into per-source fragments with filter/projection pushdown
(GAP-FABRIC-004), local result merging with per-row provenance
(GAP-FABRIC-005), cost-aware routing that prefers materialized/local sources
(GAP-FABRIC-003), offline degradation that marks unavailable sources and
continues with the rest (GAP-FABRIC-006), and an explainable routing plan
(GAP-FABRIC-007) recording which fragments ran where, why, and at what cost.

Two built-in adapters keep the layer runnable without external systems:
``InMemoryDemoAdapter`` (deterministic in-memory rows) and
``HugeGraphLocalAdapter`` (reads through a local ``GraphStore``).
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol

from pydantic import BaseModel, Field


class SourceMode(str, Enum):
    """How a source serves data (GAP-FABRIC-001)."""

    LIVE = "LIVE"
    CACHE_TTL = "CACHE_TTL"
    MATERIALIZED = "MATERIALIZED"
    HYBRID = "HYBRID"


class SourceCapability(BaseModel):
    """Registered capability of a federated data source (GAP-FABRIC-001)."""

    source_id: str = Field(..., description="Stable source id, e.g. urn:eoip:federation:source:<name>")
    entity_types: list[str] = Field(default_factory=list)
    pushdown_filters: bool = False
    pushdown_projection: bool = False
    mode: SourceMode = SourceMode.LIVE
    freshness_seconds: float | None = None
    authority: float = 1.0
    locality: float = 1.0  # 1.0 = local process, lower = remote/networked

    def urn(self) -> str:
        if self.source_id.startswith("urn:"):
            return self.source_id
        return f"urn:eoip:federation:source:{self.source_id}"


@dataclass
class QueryFragment:
    """One per-source slice of a federated query (GAP-FABRIC-002)."""

    fragment_id: str
    source_id: str
    entity_types: list[str]
    filters: dict[str, Any] = field(default_factory=dict)
    projection: list[str] = field(default_factory=list)
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "fragment_id": self.fragment_id,
            "source_id": self.source_id,
            "entity_types": list(self.entity_types),
            "filters": dict(self.filters),
            "projection": list(self.projection),
            "reason": self.reason,
        }


@dataclass
class FragmentResult:
    rows: list[dict[str, Any]]
    provenance: dict[str, Any]
    degraded: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "rows": self.rows,
            "provenance": self.provenance,
            "degraded": self.degraded,
        }


@dataclass
class RoutingDecision:
    fragment_id: str
    source_id: str
    mode: SourceMode
    cost: float
    reason: str
    status: str  # "planned" | "executed" | "degraded"
    pushed_filters: bool = False
    pushed_projection: bool = False
    row_count: int = 0
    elapsed_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "fragment_id": self.fragment_id,
            "source_id": self.source_id,
            "mode": self.mode.value,
            "cost": round(self.cost, 4),
            "reason": self.reason,
            "status": self.status,
            "pushed_filters": self.pushed_filters,
            "pushed_projection": self.pushed_projection,
            "row_count": self.row_count,
            "elapsed_ms": round(self.elapsed_ms, 3),
        }


@dataclass
class RoutingPlan:
    """Explainable plan output (GAP-FABRIC-007)."""

    decisions: list[RoutingDecision] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "fragments": [d.to_dict() for d in self.decisions],
            "total_cost": round(sum(d.cost for d in self.decisions), 4),
            "degraded_sources": sorted(
                {d.source_id for d in self.decisions if d.status == "degraded"}
            ),
        }


class DataSourceAdapter(Protocol):
    """Adapter interface between the planner and a concrete source."""

    def capability(self) -> SourceCapability: ...
    def health(self) -> bool: ...
    def fetch(
        self,
        entity_types: list[str],
        filters: dict[str, Any],
        projection: list[str],
    ) -> list[dict[str, Any]]: ...


class InMemoryDemoAdapter:
    """Deterministic in-memory demo source; no external systems needed."""

    def __init__(
        self,
        capability: SourceCapability,
        rows: list[dict[str, Any]],
        healthy: bool = True,
    ) -> None:
        self._capability = capability
        self._rows = rows
        self._healthy = healthy

    def capability(self) -> SourceCapability:
        return self._capability

    def set_healthy(self, healthy: bool) -> None:
        self._healthy = healthy

    def health(self) -> bool:
        return self._healthy

    def fetch(
        self,
        entity_types: list[str],
        filters: dict[str, Any],
        projection: list[str],
    ) -> list[dict[str, Any]]:
        out = []
        for row in self._rows:
            if entity_types and row.get("entity_type") not in entity_types:
                continue
            if any(row.get(k) != v for k, v in filters.items()):
                continue
            if projection:
                out.append({k: row.get(k) for k in projection})
            else:
                out.append(dict(row))
        return out


class HugeGraphLocalAdapter:
    """Adapter over a local GraphStore, filtered by vertex label.

    Uses ``find_vertices`` so it works against the in-memory HugeGraph-local
    store implementation without a running server.
    """

    def __init__(self, capability: SourceCapability, store: Any) -> None:
        self._capability = capability
        self._store = store

    def capability(self) -> SourceCapability:
        return self._capability

    def health(self) -> bool:
        try:
            self._store.count_vertices()
            return True
        except Exception:
            return False

    def fetch(
        self,
        entity_types: list[str],
        filters: dict[str, Any],
        projection: list[str],
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for label in entity_types:
            vertices = self._store.find_vertices(label=label, limit=5000)
            for vertex in vertices:
                props = dict(vertex.get("properties", {}))
                if any(props.get(k) != v for k, v in filters.items()):
                    continue
                row = {
                    "canonical_id": props.get("canonical_id"),
                    "label": vertex.get("label", label),
                    "entity_type": label,
                }
                row.update(props)
                if projection:
                    row = {k: row.get(k) for k in projection}
                rows.append(row)
        return rows


def _matches(row: dict[str, Any], filters: dict[str, Any]) -> bool:
    return all(row.get(k) == v for k, v in filters.items())


def _row_entity_type(row: dict[str, Any]) -> str | None:
    return row.get("entity_type") or row.get("label")


class FederatedQueryPlanner:
    """Plans and executes federated semantic queries (GAP-FABRIC-001..008)."""

    def __init__(self) -> None:
        self._adapters: dict[str, DataSourceAdapter] = {}

    # -- Source Capability Registry (GAP-FABRIC-001) -----------------------

    def register(self, adapter: DataSourceAdapter) -> None:
        cap = adapter.capability()
        self._adapters[cap.source_id] = adapter

    def unregister(self, source_id: str) -> None:
        self._adapters.pop(source_id, None)

    def sources(self) -> list[SourceCapability]:
        return [a.capability() for a in self._adapters.values()]

    # -- Fragment planning (GAP-FABRIC-002/004) -----------------------------

    def plan_fragments(
        self,
        entity_types: list[str],
        filters: dict[str, Any] | None = None,
        projection: list[str] | None = None,
    ) -> list[QueryFragment]:
        """Split a semantic query into per-source fragments, pushing
        filters/projections only where the source supports them
        (GAP-FABRIC-004)."""
        filters = filters or {}
        projection = list(projection or [])
        fragments: list[QueryFragment] = []
        covered: set[str] = set()
        idx = 0
        # Cost-aware order: materialized/local sources first (GAP-FABRIC-003).
        for adapter in self._cost_ordered_adapters():
            cap = adapter.capability()
            supported = [t for t in entity_types if t in cap.entity_types]
            if not supported:
                continue
            residual = [t for t in supported if t not in covered]
            target = residual or supported
            idx += 1
            pushed_filters = dict(filters) if cap.pushdown_filters else {}
            pushed_projection = list(projection) if cap.pushdown_projection else []
            reason_bits = []
            if residual:
                reason_bits.append("authoritative for uncovered entity types")
            else:
                reason_bits.append("secondary/duplicate coverage")
            if pushed_filters:
                reason_bits.append("filters pushed down")
            if pushed_projection:
                reason_bits.append("projection pushed down")
            fragments.append(
                QueryFragment(
                    fragment_id=f"frag-{idx:03d}",
                    source_id=cap.source_id,
                    entity_types=target,
                    filters=pushed_filters,
                    projection=pushed_projection,
                    reason="; ".join(reason_bits),
                )
            )
            covered.update(target)
        return fragments

    # -- Cost-aware routing (GAP-FABRIC-003) --------------------------------

    def _source_cost(self, cap: SourceCapability) -> float:
        mode_penalty = {
            SourceMode.LIVE: 10.0,
            SourceMode.CACHE_TTL: 4.0,
            SourceMode.HYBRID: 2.0,
            SourceMode.MATERIALIZED: 0.5,
        }[cap.mode]
        freshness_penalty = (cap.freshness_seconds or 0.0) / 60.0
        return mode_penalty + freshness_penalty + (1.0 - cap.locality) * 5.0 - cap.authority

    def _cost_ordered_adapters(self) -> list[DataSourceAdapter]:
        return sorted(
            self._adapters.values(),
            key=lambda a: self._source_cost(a.capability()),
        )

    # -- Execution with offline degradation (GAP-FABRIC-005/006) ------------

    def execute(
        self,
        entity_types: list[str],
        filters: dict[str, Any] | None = None,
        projection: list[str] | None = None,
        merge_key: str = "canonical_id",
    ) -> dict[str, Any]:
        filters = filters or {}
        projection = list(projection or [])
        fragments = self.plan_fragments(entity_types, filters, projection)
        plan = RoutingPlan()
        merged: dict[Any, dict[str, Any]] = {}
        seen_sources: dict[Any, set[str]] = {}
        local_filter_keys: dict[Any, bool] = {}

        for fragment in fragments:
            adapter = self._adapters[fragment.source_id]
            cap = adapter.capability()
            cost = self._source_cost(cap)

            if not adapter.health():
                # GAP-FABRIC-006: mark degraded, continue with remaining sources.
                plan.decisions.append(
                    RoutingDecision(
                        fragment_id=fragment.fragment_id,
                        source_id=fragment.source_id,
                        mode=cap.mode,
                        cost=cost,
                        reason=f"{fragment.reason}; source unavailable — fragment degraded",
                        status="degraded",
                        pushed_filters=bool(fragment.filters),
                        pushed_projection=bool(fragment.projection),
                    )
                )
                continue

            start = time.perf_counter()
            try:
                rows = adapter.fetch(
                    fragment.entity_types, fragment.filters, fragment.projection
                )
            except Exception:
                plan.decisions.append(
                    RoutingDecision(
                        fragment_id=fragment.fragment_id,
                        source_id=fragment.source_id,
                        mode=cap.mode,
                        cost=cost,
                        reason=f"{fragment.reason}; fetch failed — fragment degraded",
                        status="degraded",
                        pushed_filters=bool(fragment.filters),
                        pushed_projection=bool(fragment.projection),
                    )
                )
                continue
            elapsed_ms = (time.perf_counter() - start) * 1000.0

            # GAP-FABRIC-005: merge locally with per-row provenance.
            for row in rows:
                key = row.get(merge_key)
                if key is None:
                    key = f"row:{len(merged)}"
                existing = merged.get(key)
                if existing is None:
                    merged[key] = dict(row)
                    seen_sources[key] = {fragment.source_id}
                    local_filter_keys[key] = not fragment.filters
                else:
                    seen_sources[key].add(fragment.source_id)
                    # Fill missing fields from this source (authority-resolved).
                    for k, v in row.items():
                        if k not in existing or existing[k] in (None, ""):
                            existing[k] = v
                    local_filter_keys[key] = (
                        local_filter_keys[key] or not fragment.filters
                    )
            for row_key, sources in seen_sources.items():
                merged[row_key]["_provenance"] = {
                    "sources": sorted(sources),
                    "source_urns": [
                        self._adapters[s].capability().urn() for s in sorted(sources)
                    ],
                }

            plan.decisions.append(
                RoutingDecision(
                    fragment_id=fragment.fragment_id,
                    source_id=fragment.source_id,
                    mode=cap.mode,
                    cost=cost,
                    reason=fragment.reason,
                    status="executed",
                    pushed_filters=bool(fragment.filters),
                    pushed_projection=bool(fragment.projection),
                    row_count=len(rows),
                    elapsed_ms=elapsed_ms,
                )
            )

        # Post-merge filter/projection for rows whose source lacked pushdown.
        rows_out = []
        for row in merged.values():
            key = row.get(merge_key)
            # Only re-apply filters that a contributing source did not push down.
            if local_filter_keys.get(key, True) and not _matches(row, filters):
                continue
            if projection:
                keep = {k: row.get(k) for k in projection}
                keep["_provenance"] = row["_provenance"]
                row = keep
            rows_out.append(row)

        return {
            "rows": rows_out,
            "plan": plan.to_dict(),
            "row_count": len(rows_out),
            "degraded": bool(plan.to_dict()["degraded_sources"]),
        }
