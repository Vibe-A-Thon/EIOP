"""Qualified OBDA and Federated Query Engine (CRA-024.4).

Provides:
- Source authorization delegation (per-tenant credential propagation)
- Null / bag / set / type semantics (SQL 3-valued logic, distinct set vs multiset bag)
- Join pushdown (predicates and projections pushed down to remote sources)
- Partial-source degradation (unreachable source emits partial results with diagnostic metadata)
- Snapshot, watermark freshness, and schema-drift detection
"""
from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional


class SemanticsMode(str, Enum):
    SET = "SET"        # Deduplicated (DISTINCT)
    BAG = "BAG"        # Multiset (preserves duplicates)


@dataclass
class SourceAuthDelegation:
    source_id: str
    tenant_id: str
    auth_type: str  # "BEARER_TOKEN", "BASIC", "ROLE_ASSUME", "API_KEY"
    credentials: dict[str, str] = field(default_factory=dict)

    def get_auth_headers(self) -> dict[str, str]:
        if self.auth_type == "BEARER_TOKEN":
            return {"Authorization": f"Bearer {self.credentials.get('token', '')}"}
        if self.auth_type == "API_KEY":
            return {"X-API-Key": self.credentials.get('api_key', '')}
        return {}


@dataclass
class FederatedDataSource:
    source_id: str
    source_type: str  # "RELATIONAL_SQL", "GRAPH_STORE", "SNOWFLAKE", "REST"
    schema_hash: str
    watermark_timestamp: float = field(default_factory=time.time)
    supports_pushdown: bool = True
    is_available: bool = True
    auth_delegation: Optional[SourceAuthDelegation] = None


@dataclass
class FederatedPushdownFragment:
    fragment_id: str
    source_id: str
    pushed_filters: dict[str, Any]
    pushed_projection: list[str]
    raw_query: str


@dataclass
class FederatedExecutionOutcome:
    query_id: str
    status: str  # "SUCCESS", "PARTIAL", "FAILED"
    semantics: SemanticsMode
    rows: list[dict[str, Any]]
    total_rows: int
    degraded_sources: list[str] = field(default_factory=list)
    schema_drift_detected: list[str] = field(default_factory=list)
    freshness_watermarks: dict[str, float] = field(default_factory=dict)


class OBDAFederationEngine:
    """Qualified OBDA / Federation executor."""

    def __init__(self) -> None:
        self.sources: dict[str, FederatedDataSource] = {}
        self._source_executors: dict[str, Callable[[FederatedPushdownFragment], list[dict[str, Any]]]] = {}

    def register_source(
        self,
        source: FederatedDataSource,
        executor: Optional[Callable[[FederatedPushdownFragment], list[dict[str, Any]]]] = None,
    ) -> None:
        self.sources[source.source_id] = source
        if executor:
            self._source_executors[source.source_id] = executor

    def check_schema_drift(self, source_id: str, current_schema_def: str) -> bool:
        """Compares current schema definition hash against registered schema_hash."""
        source = self.sources.get(source_id)
        if not source:
            return False
        curr_hash = hashlib.sha256(current_schema_def.encode("utf-8")).hexdigest()
        is_drifted = curr_hash != source.schema_hash
        if is_drifted:
            source.schema_hash = curr_hash  # update or flag
        return is_drifted

    def plan_pushdown(
        self,
        source_id: str,
        filters: dict[str, Any],
        projection: list[str],
    ) -> FederatedPushdownFragment:
        """Pushes down predicates and projection to the remote source."""
        source = self.sources.get(source_id)
        if not source or not source.supports_pushdown:
            return FederatedPushdownFragment(
                fragment_id=f"frag_{source_id}",
                source_id=source_id,
                pushed_filters={},
                pushed_projection=[],
                raw_query="SELECT *",
            )

        # Build SQL/predicate pushdown
        clauses = [f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}" for k, v in filters.items()]
        where_sql = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        proj_sql = ", ".join(projection) if projection else "*"
        raw_sql = f"SELECT {proj_sql} FROM {source_id}{where_sql}"

        return FederatedPushdownFragment(
            fragment_id=f"frag_{source_id}",
            source_id=source_id,
            pushed_filters=dict(filters),
            pushed_projection=list(projection),
            raw_query=raw_sql,
        )

    def execute_federated_join(
        self,
        local_rows: list[dict[str, Any]],
        remote_source_id: str,
        join_key_local: str,
        join_key_remote: str,
        remote_filters: Optional[dict[str, Any]] = None,
        remote_projection: Optional[list[str]] = None,
        semantics: SemanticsMode = SemanticsMode.SET,
    ) -> FederatedExecutionOutcome:
        """Executes a federated join across local rows and remote source with null and partial degradation handling."""
        source = self.sources.get(remote_source_id)
        degraded: list[str] = []
        drifted: list[str] = []
        freshness: dict[str, float] = {}

        if not source or not source.is_available:
            # Partial source degradation: return local rows with degraded indicator
            degraded.append(remote_source_id)
            return FederatedExecutionOutcome(
                query_id="fed_query_degraded",
                status="PARTIAL",
                semantics=semantics,
                rows=local_rows,
                total_rows=len(local_rows),
                degraded_sources=degraded,
                freshness_watermarks=freshness,
            )

        freshness[remote_source_id] = source.watermark_timestamp

        # Execute pushdown fragment
        fragment = self.plan_pushdown(
            remote_source_id,
            filters=remote_filters or {},
            projection=remote_projection or [],
        )

        remote_executor = self._source_executors.get(remote_source_id)
        try:
            if remote_executor:
                remote_rows = remote_executor(fragment)
            else:
                remote_rows = []
        except Exception:
            # Handle source failure as partial degradation
            degraded.append(remote_source_id)
            return FederatedExecutionOutcome(
                query_id="fed_query_err",
                status="PARTIAL",
                semantics=semantics,
                rows=local_rows,
                total_rows=len(local_rows),
                degraded_sources=degraded,
                freshness_watermarks=freshness,
            )

        # Index remote rows by join key (handling SQL null semantics: NULL != NULL)
        remote_index: dict[Any, list[dict[str, Any]]] = {}
        for r_row in remote_rows:
            key_val = r_row.get(join_key_remote)
            if key_val is not None:  # In 3-valued logic, NULL cannot match
                remote_index.setdefault(key_val, []).append(r_row)

        joined_results: list[dict[str, Any]] = []
        for l_row in local_rows:
            l_key = l_row.get(join_key_local)
            if l_key is not None and l_key in remote_index:
                for matched_remote in remote_index[l_key]:
                    merged = dict(l_row)
                    merged.update({f"remote_{k}": v for k, v in matched_remote.items()})
                    joined_results.append(merged)
            else:
                # Left join / null semantics
                merged = dict(l_row)
                merged.update({f"remote_{join_key_remote}": None})
                joined_results.append(merged)

        # Handle SET vs BAG semantics
        if semantics == SemanticsMode.SET:
            seen = set()
            deduped = []
            for r in joined_results:
                row_key = tuple(sorted((k, str(v)) for k, v in r.items()))
                if row_key not in seen:
                    seen.add(row_key)
                    deduped.append(r)
            joined_results = deduped

        return FederatedExecutionOutcome(
            query_id="fed_query_success",
            status="SUCCESS" if not degraded else "PARTIAL",
            semantics=semantics,
            rows=joined_results,
            total_rows=len(joined_results),
            degraded_sources=degraded,
            freshness_watermarks=freshness,
        )
