"""Authorized Bitemporal As-Of Query Engine with Dual-Time ACL and Retention Governance (CRA-028.2, CRA-028.6, CRA-028.A).

Features:
- Dual-time authorization (CRA-028.A): Access to historical records of deleted nodes requires authorization at BOTH the historical point-in-time AND the current query time.
- Retention / Legal Hold enforcement (CRA-028.2): Historical states older than the retention period are redacted unless protected by an active Legal Hold.
- Explicit query API `as_of` parameters (CRA-028.6) and SPARQL `eoip:asOf` service parameter parsing.
- Bounded historical snapshots and first-class bitemporal version diffs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
import json
import re
from typing import Any, Optional

from eoip.graph.bitemporal import (
    BitemporalCoordinate,
    BitemporalDiff,
    BitemporalQueryEngine,
    BitemporalSlice,
    BitemporalTopology,
)
from eoip.graph.store import GraphStore
from eoip.temporal.models import BitemporalEntityRecord, RetentionPolicy


class HistoricalAccessDeniedError(PermissionError):
    """Raised when principal lacks dual-time authorization or retention period expired (CRA-028.2, CRA-028.A)."""


@dataclass
class AuthorizedHistoricalSnapshot:
    coordinate: BitemporalCoordinate
    entities: list[dict[str, Any]]
    edges: list[dict[str, Any]]
    authorized_principal: str
    redacted_count: int = 0
    retention_pruned_count: int = 0


class AuthorizedAsOfEngine:
    """Orchestrates secure point-in-time bitemporal graph navigation."""

    def __init__(
        self,
        store: GraphStore,
        default_retention_policy: Optional[RetentionPolicy] = None,
    ) -> None:
        self._store = store
        self._bitemporal_engine = BitemporalQueryEngine(store)
        self.default_retention_policy = default_retention_policy or RetentionPolicy()

    def query_as_of(
        self,
        valid_at: str,
        known_at: str,
        principal_id: str,
        historical_acls: set[str],
        current_acls: set[str],
        retention_policy: Optional[RetentionPolicy] = None,
        current_time: Optional[str] = None,
    ) -> AuthorizedHistoricalSnapshot:
        """Execute an authorized as-of query with dual-time ACL and retention checks (CRA-028.2, CRA-028.A)."""
        policy = retention_policy or self.default_retention_policy
        slice_result = self._bitemporal_engine.slice(valid_at=valid_at, known_at=known_at)
        topology = self._bitemporal_engine.topology(valid_at=valid_at, known_at=known_at)

        authorized_entities: list[dict[str, Any]] = []
        authorized_entity_ids: set[str] = set()
        redacted_count = 0
        retention_pruned_count = 0

        # Query active store to check if entity was since deleted
        active_entities = {
            v.get("canonical_id"): v for v in self._store.find_vertices(limit=100_000, include_deleted=True)
        }

        for record in slice_result.entities:
            if record.is_delete:
                continue

            cid = record.subject_id
            payload = record.payload or {}
            acl_vector = set(payload.get("acl_vector") or ["group:engineering", "public"])

            # 1. Retention check (CRA-028.2)
            if not policy.is_history_retained(record.observed_at, current_time=current_time):
                retention_pruned_count += 1
                continue

            # 2. Dual-time authorization check (CRA-028.A)
            # Was principal authorized at historical time?
            has_historical_auth = bool(historical_acls & acl_vector)
            if not has_historical_auth:
                redacted_count += 1
                continue

            # Check if entity is deleted in current active graph state
            active_vertex = active_entities.get(cid)
            is_currently_deleted = False
            if active_vertex is None or active_vertex.get("properties", {}).get("deleted_at"):
                is_currently_deleted = True

            # If node was since deleted, principal MUST also be authorized at current time (CRA-028.A)
            if is_currently_deleted:
                has_current_auth = bool(current_acls & acl_vector)
                if not has_current_auth:
                    # Access denied to deleted historical node without current auth!
                    redacted_count += 1
                    continue

            authorized_entities.append({
                "canonical_id": cid,
                "revision_id": record.revision_id,
                "entity_type": record.entity_type,
                "observed_at": record.observed_at,
                "valid_from": record.valid_from,
                "valid_to": record.valid_to,
                "properties": payload.get("properties", {}),
            })
            authorized_entity_ids.add(cid)

        # Filter edges to only include authorized endpoints
        authorized_edges: list[dict[str, Any]] = []
        for edge in topology.edges:
            if edge.from_id in authorized_entity_ids and edge.to_id in authorized_entity_ids:
                authorized_edges.append({
                    "relationship_id": edge.relationship_id,
                    "relationship_type": edge.relationship_type,
                    "from_id": edge.from_id,
                    "to_id": edge.to_id,
                    "revision_id": edge.revision_id,
                })

        return AuthorizedHistoricalSnapshot(
            coordinate=BitemporalCoordinate(valid_at=valid_at, known_at=known_at),
            entities=authorized_entities,
            edges=authorized_edges,
            authorized_principal=principal_id,
            redacted_count=redacted_count,
            retention_pruned_count=retention_pruned_count,
        )

    def diff(
        self,
        from_coord: BitemporalCoordinate,
        to_coord: BitemporalCoordinate,
    ) -> BitemporalDiff:
        """First-class bitemporal diff between two coordinates (CRA-028.2)."""
        return self._bitemporal_engine.diff(from_coord, to_coord)

    @staticmethod
    def parse_sparql_as_of(sparql_query: str) -> tuple[str, Optional[dict[str, str]]]:
        """Extract eoip:asOf service parameter from SPARQL queries (CRA-028.6).

        Standard SPARQL 1.1 has no native AS OF syntax. EOIP provides
        PREFIX eoip: <urn:eoip:query:> and SERVICE eoip:asOf { ... }
        or query comments/parameters.
        """
        match = re.search(r"eoip:asOf\s*\(\s*valid_at\s*=\s*['\"]([^'\"]+)['\"]\s*,\s*known_at\s*=\s*['\"]([^'\"]+)['\"]\s*\)", sparql_query)
        if match:
            clean_query = sparql_query[:match.start()] + sparql_query[match.end():]
            return clean_query.strip(), {"valid_at": match.group(1), "known_at": match.group(2)}
        return sparql_query, None
