"""Federated query planner (GAP-FABRIC-001..008, GAP-FED-001..004).

Provides a source capability registry, a fragment planner that splits a
semantic query into per-source fragments with filter/projection pushdown
(GAP-FABRIC-004), local result merging with per-row provenance
(GAP-FABRIC-005), cost-aware routing that prefers materialized/local sources
(GAP-FABRIC-003), offline degradation that marks unavailable sources and
continues with the rest (GAP-FABRIC-006), and an explainable routing plan
(GAP-FABRIC-007) recording which fragments ran where, why, and at what cost.

Built-in adapters are independent of HugeGraph: in-memory rows for tests,
local graph-store reads, local files, REST endpoints and SQLite-backed JDBC-like
tables. All external access is explicit; registering the planner never makes a
network call by itself.
"""

from __future__ import annotations

import csv
import json
import re
import sqlite3
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from threading import RLock
from typing import Any, Protocol
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

from pydantic import BaseModel, Field


class SourceMode(str, Enum):
    """How a source serves data (GAP-FED-002).

    Legacy names remain aliases so older callers keep working while the public
    contract exposes VIRTUAL/CACHE/MATERIALIZE/HYBRID.
    """

    VIRTUAL = "VIRTUAL"
    CACHE = "CACHE"
    MATERIALIZE = "MATERIALIZE"
    HYBRID = "HYBRID"
    LIVE = "LIVE"
    CACHE_TTL = "CACHE_TTL"
    MATERIALIZED = "MATERIALIZED"


class SourcePolicy(BaseModel):
    """Source-level data policy enforced before routing and after fetch."""

    allowed_roles: list[str] = Field(default_factory=list)
    required_purpose: str | None = None
    required_filters: dict[str, Any] = Field(default_factory=dict)
    denied_fields: list[str] = Field(default_factory=list)
    max_rows: int | None = Field(default=None, ge=1)


class SourceCapability(BaseModel):
    """Registered capability of a federated data source (GAP-FABRIC-001)."""

    source_id: str = Field(..., description="Stable source id, e.g. urn:eoip:federation:source:<name>")
    adapter_kind: str = "generic"
    entity_types: list[str] = Field(default_factory=list)
    entity_modes: dict[str, SourceMode] = Field(default_factory=dict)
    pushdown_filters: bool = False
    pushdown_projection: bool = False
    mode: SourceMode = SourceMode.VIRTUAL
    freshness_seconds: float | None = None
    authority: float = 1.0
    locality: float = 1.0  # 1.0 = local process, lower = remote/networked
    policy: SourcePolicy = Field(default_factory=SourcePolicy)

    def urn(self) -> str:
        if self.source_id.startswith("urn:"):
            return self.source_id
        return f"urn:eoip:federation:source:{self.source_id}"

    def mode_for(self, entity_type: str) -> SourceMode:
        return self.entity_modes.get(entity_type, self.mode)


@dataclass
class QueryFragment:
    """One per-source slice of a federated query (GAP-FABRIC-002)."""

    fragment_id: str
    source_id: str
    entity_types: list[str]
    filters: dict[str, Any] = field(default_factory=dict)
    projection: list[str] = field(default_factory=list)
    access_mode: SourceMode = SourceMode.VIRTUAL
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "fragment_id": self.fragment_id,
            "source_id": self.source_id,
            "entity_types": list(self.entity_types),
            "filters": dict(self.filters),
            "projection": list(self.projection),
            "access_mode": self.access_mode.value,
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
    adapter_kind: str = "generic"
    cache_hit: bool = False
    freshness_seconds: float | None = None

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
            "adapter_kind": self.adapter_kind,
            "cache_hit": self.cache_hit,
            "freshness_seconds": self.freshness_seconds,
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
            "policy_denied_sources": sorted(
                {d.source_id for d in self.decisions if d.status == "policy_denied"}
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


class InMemoryRowAdapter:
    """Deterministic in-memory row source for tests and local fixtures."""

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


class LocalGraphStoreAdapter:
    """Adapter over a local GraphStore, filtered by vertex label.

    Uses ``find_vertices`` so it works against any configured GraphStore
    implementation without a backend-specific query language.
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
        except (AttributeError, KeyError, RuntimeError, ValueError):
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


HugeGraphLocalAdapter = LocalGraphStoreAdapter
InMemoryDemoAdapter = InMemoryRowAdapter


class FileSourceAdapter:
    """HugeGraph-independent adapter over JSON, JSONL or CSV files."""

    def __init__(
        self,
        capability: SourceCapability,
        path: str | Path,
        *,
        file_format: str | None = None,
    ) -> None:
        self._capability = capability.model_copy(update={"adapter_kind": "file"})
        self._path = Path(path)
        self._format = (file_format or self._path.suffix.lstrip(".") or "json").lower()

    def capability(self) -> SourceCapability:
        return self._capability

    def health(self) -> bool:
        return self._path.is_file()

    def _load_rows(self) -> list[dict[str, Any]]:
        if self._format == "csv":
            with self._path.open("r", encoding="utf-8", newline="") as handle:
                return [dict(row) for row in csv.DictReader(handle)]
        if self._format in {"jsonl", "ndjson"}:
            rows = []
            with self._path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    if line.strip():
                        item = json.loads(line)
                        if isinstance(item, dict):
                            rows.append(item)
            return rows
        payload = json.loads(self._path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            payload = payload.get("rows", [])
        if not isinstance(payload, list):
            raise TypeError("file source must contain a JSON array or {'rows': [...]}")
        return [dict(row) for row in payload if isinstance(row, dict)]

    def fetch(
        self,
        entity_types: list[str],
        filters: dict[str, Any],
        projection: list[str],
    ) -> list[dict[str, Any]]:
        return _filter_project_rows(self._load_rows(), entity_types, filters, projection)


class RestSourceAdapter:
    """HugeGraph-independent REST adapter for JSON row endpoints."""

    def __init__(
        self,
        capability: SourceCapability,
        url: str,
        *,
        method: str = "GET",
        headers: dict[str, str] | None = None,
        rows_path: list[str] | None = None,
        timeout_seconds: float = 5.0,
        health_url: str | None = None,
    ) -> None:
        self._capability = capability.model_copy(update={"adapter_kind": "rest"})
        for endpoint in (url, health_url):
            if endpoint is not None and urlsplit(endpoint).scheme not in ("http", "https"):
                raise ValueError(f"REST source URL scheme must be http or https: {endpoint!r}")
        self._url = url
        self._method = method.upper()
        self._headers = dict(headers or {})
        self._rows_path = rows_path or ["rows"]
        self._timeout_seconds = timeout_seconds
        self._health_url = health_url

    def capability(self) -> SourceCapability:
        return self._capability

    def health(self) -> bool:
        if self._health_url is None:
            return True
        try:
            with urlopen(Request(self._health_url, method="GET"), timeout=self._timeout_seconds) as response:  # nosec B310 - scheme restricted to http/https in __init__
                return 200 <= response.status < 500
        except (OSError, ValueError):
            return False

    def fetch(
        self,
        entity_types: list[str],
        filters: dict[str, Any],
        projection: list[str],
    ) -> list[dict[str, Any]]:
        payload = {"entity_types": entity_types, "filters": filters, "projection": projection}
        url = self._url
        data = None
        headers = {"Accept": "application/json", **self._headers}
        if self._method == "GET":
            query = urlencode({k: json.dumps(v) if isinstance(v, (dict, list)) else v for k, v in payload.items()})
            url = f"{url}?{query}" if "?" not in url else f"{url}&{query}"
        else:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        with urlopen(Request(url, data=data, headers=headers, method=self._method), timeout=self._timeout_seconds) as response:  # nosec B310 - scheme restricted to http/https in __init__
            body = response.read().decode("utf-8")
        parsed = json.loads(body) if body else []
        for part in self._rows_path:
            if isinstance(parsed, dict):
                parsed = parsed.get(part, [])
        if isinstance(parsed, dict):
            parsed = [parsed]
        if not isinstance(parsed, list):
            raise TypeError("REST source response does not contain a row array")
        return _filter_project_rows([dict(row) for row in parsed if isinstance(row, dict)], entity_types, filters, projection)


class JdbcSourceAdapter:
    """SQLite-backed JDBC-style adapter using DB-API parameter binding."""

    _IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

    def __init__(
        self,
        capability: SourceCapability,
        database_path: str | Path,
        table: str,
    ) -> None:
        if not self._IDENT.fullmatch(table):
            raise ValueError("table must be a safe SQL identifier")
        self._capability = capability.model_copy(update={"adapter_kind": "jdbc"})
        self._database_path = Path(database_path)
        self._table = table

    def capability(self) -> SourceCapability:
        return self._capability

    def health(self) -> bool:
        return self._database_path.is_file()

    def fetch(
        self,
        entity_types: list[str],
        filters: dict[str, Any],
        projection: list[str],
    ) -> list[dict[str, Any]]:
        columns = [col for col in projection if self._IDENT.fullmatch(col)]
        select = ", ".join(columns) if columns else "*"
        clauses = []
        values = []
        for key, value in filters.items():
            if self._IDENT.fullmatch(key):
                clauses.append(f"{key} = ?")
                values.append(value)
        if entity_types:
            clauses.append(f"entity_type IN ({','.join('?' for _ in entity_types)})")
            values.extend(entity_types)
        where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
        with sqlite3.connect(self._database_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(f"SELECT {select} FROM {self._table}{where}", values).fetchall()  # nosec B608 - table/column/key identifiers _IDENT-validated, values bound via ? params
        return [dict(row) for row in rows]


def _matches(row: dict[str, Any], filters: dict[str, Any]) -> bool:
    return all(row.get(k) == v for k, v in filters.items())


def _row_entity_type(row: dict[str, Any]) -> str | None:
    return row.get("entity_type") or row.get("label")


def _filter_project_rows(
    rows: list[dict[str, Any]],
    entity_types: list[str],
    filters: dict[str, Any],
    projection: list[str],
) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        if entity_types and _row_entity_type(row) not in entity_types:
            continue
        if not _matches(row, filters):
            continue
        if projection:
            out.append({key: row.get(key) for key in projection})
        else:
            out.append(dict(row))
    return out


@dataclass
class _CachedRows:
    rows: list[dict[str, Any]]
    cached_at: float
    ttl_seconds: float

    def is_fresh(self, now: float) -> bool:
        return now - self.cached_at <= self.ttl_seconds


class FederatedQueryPlanner:
    """Plans and executes federated semantic queries (GAP-FABRIC-001..008)."""

    def __init__(self) -> None:
        self._adapters: dict[str, DataSourceAdapter] = {}
        self._result_cache: dict[tuple[Any, ...], _CachedRows] = {}
        self._lock = RLock()

    # -- Source Capability Registry (GAP-FABRIC-001) -----------------------

    def register(self, adapter: DataSourceAdapter) -> None:
        cap = adapter.capability()
        with self._lock:
            self._adapters[cap.source_id] = adapter

    def unregister(self, source_id: str) -> None:
        with self._lock:
            self._adapters.pop(source_id, None)

    def sources(self) -> list[SourceCapability]:
        with self._lock:
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
        for adapter in self._cost_ordered_adapters(entity_types):
            cap = adapter.capability()
            supported = [t for t in entity_types if t in cap.entity_types]
            if not supported:
                continue
            by_mode: dict[SourceMode, list[str]] = {}
            for entity_type in supported:
                by_mode.setdefault(cap.mode_for(entity_type), []).append(entity_type)
            for access_mode, mode_supported in by_mode.items():
                residual = [t for t in mode_supported if t not in covered]
                target = residual or mode_supported
                idx += 1
                pushed_filters = dict(filters) if cap.pushdown_filters else {}
                pushed_projection = list(projection) if cap.pushdown_projection else []
                reason_bits = [f"{access_mode.value.lower()} access"]
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
                        access_mode=access_mode,
                        reason="; ".join(reason_bits),
                    )
                )
                covered.update(target)
        return fragments

    # -- Cost-aware routing (GAP-FABRIC-003) --------------------------------

    def _source_cost(self, cap: SourceCapability, access_mode: SourceMode | None = None) -> float:
        mode = access_mode or cap.mode
        mode_penalty = {
            SourceMode.VIRTUAL: 10.0,
            SourceMode.LIVE: 10.0,
            SourceMode.CACHE: 4.0,
            SourceMode.CACHE_TTL: 4.0,
            SourceMode.HYBRID: 2.0,
            SourceMode.MATERIALIZE: 0.5,
            SourceMode.MATERIALIZED: 0.5,
        }[mode]
        freshness_penalty = (cap.freshness_seconds or 0.0) / 60.0
        return mode_penalty + freshness_penalty + (1.0 - cap.locality) * 5.0 - cap.authority

    def _cost_ordered_adapters(self, entity_types: list[str] | None = None) -> list[DataSourceAdapter]:
        def cost(adapter: DataSourceAdapter) -> float:
            cap = adapter.capability()
            modes = [
                cap.mode_for(t)
                for t in entity_types or cap.entity_types
                if t in cap.entity_types
            ]
            return min(
                (self._source_cost(cap, mode) for mode in modes),
                default=self._source_cost(cap),
            )

        with self._lock:
            return sorted(self._adapters.values(), key=cost)

    def _cache_key(self, fragment: QueryFragment) -> tuple[Any, ...]:
        return (
            fragment.source_id,
            tuple(fragment.entity_types),
            tuple(sorted(fragment.filters.items())),
            tuple(fragment.projection),
            fragment.access_mode.value,
        )

    def _cache_ttl(self, cap: SourceCapability) -> float:
        return cap.freshness_seconds if cap.freshness_seconds is not None else 60.0

    def _policy_denial(
        self,
        cap: SourceCapability,
        filters: dict[str, Any],
        context: dict[str, Any],
    ) -> str | None:
        policy = cap.policy
        roles = set(context.get("roles") or [])
        if policy.allowed_roles and roles.isdisjoint(policy.allowed_roles):
            return "source policy denied caller role"
        purpose = context.get("purpose")
        if policy.required_purpose and purpose != policy.required_purpose:
            return "source policy denied caller purpose"
        for key, value in policy.required_filters.items():
            if filters.get(key) != value:
                return f"source policy requires filter {key}"
        return None

    def _apply_policy(
        self,
        cap: SourceCapability,
        rows: list[dict[str, Any]],
        projection: list[str],
    ) -> list[dict[str, Any]]:
        denied = set(cap.policy.denied_fields)
        max_rows = cap.policy.max_rows or len(rows)
        out = []
        for row in rows[:max_rows]:
            clean = {k: v for k, v in row.items() if k not in denied}
            if projection:
                clean = {k: clean.get(k) for k in projection if k not in denied}
            out.append(clean)
        return out

    # -- Execution with offline degradation (GAP-FABRIC-005/006) ------------

    def _execute_legacy(
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
            except Exception:  # noqa: BLE001 - adapter failures degrade this fragment
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

    def execute(
        self,
        entity_types: list[str],
        filters: dict[str, Any] | None = None,
        projection: list[str] | None = None,
        merge_key: str = "canonical_id",
        policy_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        filters = filters or {}
        projection = list(projection or [])
        policy_context = policy_context or {}
        fragments = self.plan_fragments(entity_types, filters, projection)
        plan = RoutingPlan()
        merged: dict[Any, dict[str, Any]] = {}
        seen_sources: dict[Any, set[str]] = {}
        source_details: dict[Any, dict[str, dict[str, Any]]] = {}
        local_filter_keys: dict[Any, bool] = {}

        for fragment in fragments:
            adapter = self._adapters[fragment.source_id]
            cap = adapter.capability()
            cost = self._source_cost(cap, fragment.access_mode)
            cache_key = self._cache_key(fragment)
            cache_allowed = fragment.access_mode in {
                SourceMode.CACHE,
                SourceMode.CACHE_TTL,
                SourceMode.HYBRID,
            }
            now = time.time()
            cached = self._result_cache.get(cache_key)

            denial = self._policy_denial(cap, filters, policy_context)
            if denial:
                plan.decisions.append(
                    RoutingDecision(
                        fragment_id=fragment.fragment_id,
                        source_id=fragment.source_id,
                        mode=fragment.access_mode,
                        cost=cost,
                        reason=f"{fragment.reason}; {denial}",
                        status="policy_denied",
                        pushed_filters=bool(fragment.filters),
                        pushed_projection=bool(fragment.projection),
                        adapter_kind=cap.adapter_kind,
                    )
                )
                continue

            if cache_allowed and cached is not None and cached.is_fresh(now):
                rows = [dict(row) for row in cached.rows]
                self._stamp_freshness(rows, cached, now)
                self._merge_rows(
                    rows,
                    merged,
                    seen_sources,
                    source_details,
                    local_filter_keys,
                    fragment,
                    cap,
                    merge_key,
                )
                plan.decisions.append(
                    RoutingDecision(
                        fragment_id=fragment.fragment_id,
                        source_id=fragment.source_id,
                        mode=fragment.access_mode,
                        cost=cost,
                        reason=f"{fragment.reason}; cache hit",
                        status="executed",
                        pushed_filters=bool(fragment.filters),
                        pushed_projection=bool(fragment.projection),
                        row_count=len(rows),
                        adapter_kind=cap.adapter_kind,
                        cache_hit=True,
                        freshness_seconds=self._cache_ttl(cap),
                    )
                )
                continue

            if not adapter.health():
                row_count = 0
                cache_hit = False
                if cache_allowed and cached is not None:
                    rows = [dict(row) for row in cached.rows]
                    self._stamp_freshness(rows, cached, now)
                    self._merge_rows(
                        rows,
                        merged,
                        seen_sources,
                        source_details,
                        local_filter_keys,
                        fragment,
                        cap,
                        merge_key,
                    )
                    row_count = len(rows)
                    cache_hit = True
                plan.decisions.append(
                    RoutingDecision(
                        fragment_id=fragment.fragment_id,
                        source_id=fragment.source_id,
                        mode=fragment.access_mode,
                        cost=cost,
                        reason=f"{fragment.reason}; source unavailable - fragment degraded",
                        status="degraded",
                        pushed_filters=bool(fragment.filters),
                        pushed_projection=bool(fragment.projection),
                        row_count=row_count,
                        adapter_kind=cap.adapter_kind,
                        cache_hit=cache_hit,
                        freshness_seconds=self._cache_ttl(cap) if cache_hit else None,
                    )
                )
                continue

            start = time.perf_counter()
            try:
                rows = adapter.fetch(
                    fragment.entity_types,
                    fragment.filters,
                    fragment.projection,
                )
            except Exception:  # noqa: BLE001 - adapter failures degrade this fragment
                plan.decisions.append(
                    RoutingDecision(
                        fragment_id=fragment.fragment_id,
                        source_id=fragment.source_id,
                        mode=fragment.access_mode,
                        cost=cost,
                        reason=f"{fragment.reason}; fetch failed - fragment degraded",
                        status="degraded",
                        pushed_filters=bool(fragment.filters),
                        pushed_projection=bool(fragment.projection),
                        adapter_kind=cap.adapter_kind,
                    )
                )
                continue
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            rows = self._apply_policy(cap, rows, projection if cap.pushdown_projection else [])
            if cache_allowed:
                self._result_cache[cache_key] = _CachedRows(
                    rows=[dict(row) for row in rows],
                    cached_at=now,
                    ttl_seconds=self._cache_ttl(cap),
                )

            self._merge_rows(
                rows,
                merged,
                seen_sources,
                source_details,
                local_filter_keys,
                fragment,
                cap,
                merge_key,
            )
            plan.decisions.append(
                RoutingDecision(
                    fragment_id=fragment.fragment_id,
                    source_id=fragment.source_id,
                    mode=fragment.access_mode,
                    cost=cost,
                    reason=fragment.reason,
                    status="executed",
                    pushed_filters=bool(fragment.filters),
                    pushed_projection=bool(fragment.projection),
                    row_count=len(rows),
                    elapsed_ms=elapsed_ms,
                    adapter_kind=cap.adapter_kind,
                    freshness_seconds=self._cache_ttl(cap) if cache_allowed else cap.freshness_seconds,
                )
            )

        rows_out = []
        for row in merged.values():
            key = row.get(merge_key)
            if local_filter_keys.get(key, True) and not _matches(row, filters):
                continue
            if projection:
                keep = {k: row.get(k) for k in projection}
                keep["_provenance"] = row["_provenance"]
                if "_freshness" in row:
                    keep["_freshness"] = row["_freshness"]
                row = keep
            rows_out.append(row)

        plan_dict = plan.to_dict()
        return {
            "rows": rows_out,
            "plan": plan_dict,
            "row_count": len(rows_out),
            "degraded": bool(plan_dict["degraded_sources"]),
        }

    def _stamp_freshness(
        self,
        rows: list[dict[str, Any]],
        cached: _CachedRows,
        now: float,
    ) -> None:
        for row in rows:
            row["_freshness"] = {
                "cached_at": cached.cached_at,
                "age_seconds": round(now - cached.cached_at, 3),
                "ttl_seconds": cached.ttl_seconds,
            }

    def _merge_rows(
        self,
        rows: list[dict[str, Any]],
        merged: dict[Any, dict[str, Any]],
        seen_sources: dict[Any, set[str]],
        source_details: dict[Any, dict[str, dict[str, Any]]],
        local_filter_keys: dict[Any, bool],
        fragment: QueryFragment,
        cap: SourceCapability,
        merge_key: str,
    ) -> None:
        for row in rows:
            key = row.get(merge_key)
            if key is None:
                key = f"row:{len(merged)}"
            existing = merged.get(key)
            if existing is None:
                merged[key] = dict(row)
                seen_sources[key] = {fragment.source_id}
                source_details[key] = {}
                local_filter_keys[key] = not fragment.filters
            else:
                seen_sources[key].add(fragment.source_id)
                for row_key, value in row.items():
                    if row_key not in existing or existing[row_key] in (None, ""):
                        existing[row_key] = value
                local_filter_keys[key] = local_filter_keys[key] or not fragment.filters
            source_details[key][fragment.source_id] = {
                "urn": cap.urn(),
                "adapter_kind": cap.adapter_kind,
                "mode": fragment.access_mode.value,
                "freshness_seconds": cap.freshness_seconds,
            }
            merged[key]["_provenance"] = {
                "sources": sorted(seen_sources[key]),
                "source_urns": [
                    source_details[key][source_id]["urn"]
                    for source_id in sorted(seen_sources[key])
                ],
                "source_details": [
                    source_details[key][source_id]
                    for source_id in sorted(seen_sources[key])
                ],
            }
