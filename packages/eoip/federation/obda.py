"""Qualified OBDA and Federated Query Engine (CRA-024.4).

Provides:
- Source authorization delegation (per-tenant credential propagation)
- Null / bag / set / type semantics (SQL 3-valued logic, distinct set vs multiset bag)
- Join pushdown (predicates and projections pushed down to remote sources)
- Partial-source degradation (unreachable source emits partial results with diagnostic metadata)
- Snapshot, watermark freshness, and schema-drift detection

Remote sources are executed by real executors (``eoip.federation.executors``: Snowflake SQL via the Snowflake
connector, Jira Cloud REST). A registered source without an executor is an error (``SourceExecutorMissing``),
never an empty result. Pushed-down SQL is parameterised and identifiers are validated (no value interpolation).
"""
from __future__ import annotations

import base64
import hashlib
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from collections.abc import Callable


class SourceExecutorMissing(RuntimeError):
    """A federated source was queried but has no executor bound (CRA-024.4: never answer with empty rows)."""


_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_$]*$")


def safe_identifier(name: str) -> str:
    """Validate a SQL identifier (optionally dotted: db.schema.table). Raises ValueError on anything else."""
    parts = str(name).split(".")
    if not parts or not all(_IDENT.match(p) for p in parts):
        raise ValueError(f"unsafe SQL identifier: {name!r}")
    return ".".join(parts)


def build_select(table: str, filters: dict[str, Any], projection: list[str]) -> tuple[str, dict[str, Any]]:
    """Parameterised SELECT (pyformat) for pushdown. ``None`` filter values become IS NULL."""
    cols = ", ".join(safe_identifier(c) for c in projection) if projection else "*"
    clauses: list[str] = []
    params: dict[str, Any] = {}
    for i, (col, value) in enumerate(filters.items()):
        ident = safe_identifier(col)
        if value is None:
            clauses.append(f"{ident} IS NULL")
        else:
            clauses.append(f"{ident} = %(p{i})s")
            params[f"p{i}"] = value
    where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
    return f"SELECT {cols} FROM {safe_identifier(table)}{where}", params  # nosec B608 - all identifiers pass safe_identifier, values bound via pyformat params


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
        """HTTP auth headers for REST sources. Missing credentials raise instead of sending an empty header."""
        if self.auth_type == "BEARER_TOKEN":
            return {"Authorization": f"Bearer {self._need('token')}"}
        if self.auth_type == "API_KEY":
            return {"X-API-Key": self._need("api_key")}
        if self.auth_type == "BASIC":
            raw = f"{self._need('username')}:{self._need('password')}".encode("utf-8")
            return {"Authorization": "Basic " + base64.b64encode(raw).decode("ascii")}
        raise ValueError(f"auth type {self.auth_type!r} has no HTTP header form (use connector_kwargs)")

    def connector_kwargs(self) -> dict[str, str]:
        """Credential keyword arguments for database connectors (Snowflake: password, OAuth token or key pair)."""
        if self.auth_type == "BASIC":
            return {"user": self._need("username"), "password": self._need("password")}
        if self.auth_type == "BEARER_TOKEN":
            out = {"authenticator": "oauth", "token": self._need("token")}
            if self.credentials.get("username"):
                out["user"] = self.credentials["username"]
            return out
        if self.auth_type == "ROLE_ASSUME":
            return {"user": self._need("username"), "role": self._need("role"),
                    **({"password": self.credentials["password"]} if self.credentials.get("password") else {})}
        raise ValueError(f"auth type {self.auth_type!r} is not supported for database connectors")

    def _need(self, key: str) -> str:
        value = self.credentials.get(key)
        if not value:
            raise ValueError(f"source {self.source_id!r}: credential {key!r} missing for {self.auth_type}")
        return value


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
    parameters: dict[str, Any] = field(default_factory=dict)


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
    errors: dict[str, str] = field(default_factory=dict)


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

        # Parameterised SQL/predicate pushdown (values are bound, identifiers validated)
        raw_sql, params = build_select(source_id, filters, projection)

        return FederatedPushdownFragment(
            fragment_id=f"frag_{source_id}",
            source_id=source_id,
            pushed_filters=dict(filters),
            pushed_projection=list(projection),
            raw_query=raw_sql,
            parameters=params,
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
        if remote_executor is None:
            raise SourceExecutorMissing(
                f"source {remote_source_id!r} is registered without an executor; refusing to report empty remote rows"
            )
        try:
            remote_rows = list(remote_executor(fragment))
        except Exception as exc:  # noqa: BLE001 - any source failure degrades to PARTIAL with a diagnostic
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
                errors={remote_source_id: f"{type(exc).__name__}: {exc}"[:500]},
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
