"""Federated Graph Engineering Engine (GRAPH-001).

Cross-database knowledge graph federation:
- Queries across Neo4j, Neptune, TigerGraph, Memgraph, and other backends as one virtual graph
- FederationPlanner decomposing queries with pushdown optimization
- ResultMerger combining records with deduplication and conflict resolution
- CatalogService maintaining cross-backend entity mappings and schema catalog
"""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from eoip.graph.database_adapters import DatabaseAdapterRegistry, DatabaseType
from eoip.graph.memory import MemoryGraphStore

logger = logging.getLogger("eoip.federation.engine")


@dataclass
class BackendMapping:
    """Mapping of an entity or relation label to a backend graph database."""

    label: str
    backend: DatabaseType
    pushdown_supported: bool = True
    priority: int = 10
    filters: dict[str, Any] = field(default_factory=dict)


class CatalogService:
    """Maintains cross-backend entity mappings and data source capabilities."""

    def __init__(self) -> None:
        self._mappings: dict[str, BackendMapping] = {}
        self._entity_id_routes: dict[str, DatabaseType] = {}
        self._lock = threading.Lock()
        self._bootstrap_default_catalog()

    def _bootstrap_default_catalog(self) -> None:
        self.register_mapping(BackendMapping("Person", DatabaseType.NEO4J, priority=1))
        self.register_mapping(BackendMapping("Organization", DatabaseType.NEO4J, priority=1))
        self.register_mapping(BackendMapping("Service", DatabaseType.AMAZON_NEPTUNE, priority=2))
        self.register_mapping(BackendMapping("Infrastructure", DatabaseType.AMAZON_NEPTUNE, priority=2))
        self.register_mapping(BackendMapping("FinancialTransaction", DatabaseType.TIGERGRAPH, priority=3))
        self.register_mapping(BackendMapping("HighVolumeEvent", DatabaseType.MEMGRAPH, priority=4))


    def register_mapping(self, mapping: BackendMapping) -> None:
        with self._lock:
            self._mappings[mapping.label.lower()] = mapping

    def get_mapping(self, label: str) -> BackendMapping | None:
        with self._lock:
            return self._mappings.get(label.lower())

    def record_entity_route(self, entity_id: str, backend: DatabaseType) -> None:
        with self._lock:
            self._entity_id_routes[entity_id] = backend

    def get_entity_backend(self, entity_id: str) -> DatabaseType | None:
        with self._lock:
            return self._entity_id_routes.get(entity_id)

    def list_catalog(self) -> list[dict[str, Any]]:
        with self._lock:
            return [asdict(m) for m in self._mappings.values()]


@dataclass
class SubQueryPlan:
    backend: DatabaseType
    query: str
    target_labels: list[str]
    pushed_filters: dict[str, Any] = field(default_factory=dict)


class FederationPlanner:
    """Decomposes a federated graph query across backends with pushdown optimization."""

    def __init__(self, catalog: CatalogService) -> None:
        self.catalog = catalog

    def plan_query(self, query: str, filters: dict[str, Any] | None = None) -> list[SubQueryPlan]:
        """Decompose query by detected entity types and push down filters."""
        plans: list[SubQueryPlan] = []
        q_lower = query.lower()
        applied_filters = filters or {}

        # Scan for known catalog labels in query
        matched_backends: dict[DatabaseType, list[str]] = {}
        for mapping in self.catalog.list_catalog():
            label = mapping["label"]
            backend = DatabaseType(mapping["backend"])
            if label.lower() in q_lower or not plans:
                matched_backends.setdefault(backend, []).append(label)

        if not matched_backends:
            # Default to Neo4j and Neptune
            matched_backends[DatabaseType.NEO4J] = ["DefaultEntity"]
            matched_backends[DatabaseType.AMAZON_NEPTUNE] = ["DefaultEdge"]


        for backend, labels in matched_backends.items():
            sub_query = f"MATCH (n) WHERE n.label IN {labels}"
            if applied_filters:
                filter_clauses = [f"n.{k} = '{v}'" for k, v in applied_filters.items()]
                sub_query += " AND " + " AND ".join(filter_clauses)
            sub_query += " RETURN n LIMIT 100"

            plans.append(SubQueryPlan(
                backend=backend,
                query=sub_query,
                target_labels=labels,
                pushed_filters=applied_filters,
            ))

        return plans


class ResultMerger:
    """Combines query results from multiple backends with deduplication and conflict resolution."""

    def merge_results(self, backend_results: dict[DatabaseType, list[dict[str, Any]]]) -> list[dict[str, Any]]:
        deduped: dict[str, dict[str, Any]] = {}

        for backend, records in backend_results.items():
            for rec in records:
                cid = rec.get("canonical_id") or rec.get("id") or str(rec.get("name", id(rec)))
                if cid not in deduped:
                    merged_rec = dict(rec)
                    merged_rec["_provenance_backend"] = backend.value
                    deduped[cid] = merged_rec
                else:
                    # Merge properties with latest write or non-empty preference
                    existing = deduped[cid]
                    for k, v in rec.items():
                        if k not in existing or not existing[k]:
                            existing[k] = v
                    existing["_provenance_backend"] = f"{existing['_provenance_backend']},{backend.value}"

        return list(deduped.values())


class FederatedGraph:
    """Virtual knowledge graph spanning multiple physical backend databases."""

    def __init__(
        self,
        db_registry: DatabaseAdapterRegistry | None = None,
        catalog: CatalogService | None = None,
    ) -> None:
        self.db_registry = db_registry or DatabaseAdapterRegistry()
        self.catalog = catalog or CatalogService()
        self.planner = FederationPlanner(self.catalog)
        self.merger = ResultMerger()
        self._local_cache = MemoryGraphStore()

    def query(self, query_text: str, filters: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute a cross-backend federated query."""
        plans = self.planner.plan_query(query_text, filters)
        backend_results: dict[DatabaseType, list[dict[str, Any]]] = {}

        for p in plans:
            try:
                adapter = self.db_registry.get_adapter(p.backend)
                res = adapter.execute_query(p.query)
                records = res.get("records", []) if isinstance(res, dict) else []
                backend_results[p.backend] = records
            except Exception as exc:
                logger.warning("Federation subquery failed on %s: %s", p.backend, exc)
                backend_results[p.backend] = []

        merged_records = self.merger.merge_results(backend_results)
        return {
            "query": query_text,
            "total_records": len(merged_records),
            "records": merged_records,
            "subquery_plans": [
                {
                    "backend": p.backend.value,
                    "query": p.query,
                    "target_labels": p.target_labels,
                    "pushed_filters": p.pushed_filters,
                }
                for p in plans
            ],
            "participating_backends": [p.backend.value for p in plans],
        }


class FederationEngine:
    """Singleton engine for federated graph management."""

    _instance: FederationEngine | None = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        self.catalog = CatalogService()
        self.federated_graph = FederatedGraph(catalog=self.catalog)

    @classmethod
    def get_instance(cls) -> FederationEngine:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def query(self, query: str, filters: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.federated_graph.query(query, filters)

    def stats(self) -> dict[str, Any]:
        return {
            "engine": "federated_graph_engineering",
            "catalog_mappings": self.catalog.list_catalog(),
            "participating_backends": [d.value for d in DatabaseType],
        }


def get_federation_engine() -> FederationEngine:
    return FederationEngine.get_instance()
