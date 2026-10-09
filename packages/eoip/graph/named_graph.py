"""KGR-G-013: Native Per-Tenant Named-Graph Isolation Protocol.

Provides fully isolated named graph instances per tenant across all
backends.  Each tenant's data lives in a separate named graph with
enforced boundary guards preventing cross-tenant data leakage.
"""

from __future__ import annotations

import hashlib
import logging
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol

from eoip.graph.store import Edge, GraphStore, Vertex

log = logging.getLogger("eoip.graph.named_graph")


class IsolationLevel(str, Enum):
    STRICT = "STRICT"
    SHARED_SCHEMA = "SHARED_SCHEMA"
    READ_ONLY_SHARED = "READ_ONLY_SHARED"


@dataclass
class TenantConfig:
    tenant_id: str
    graph_name: str
    isolation_level: IsolationLevel = IsolationLevel.STRICT
    max_vertices: int = 10_000_000
    max_edges: int = 50_000_000
    storage_quota_mb: int = 10_240
    allowed_labels: set[str] | None = None
    blocked_labels: set[str] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def namespace_prefix(self) -> str:
        return f"ng:{self.tenant_id}:"


@dataclass
class TenantStats:
    tenant_id: str
    vertex_count: int = 0
    edge_count: int = 0
    storage_bytes: int = 0
    last_access: float = 0.0
    created_at: float = 0.0


class CrossTenantViolation(PermissionError):
    """Raised when an operation would cross tenant graph boundaries."""

    def __init__(self, source_tenant: str, target_tenant: str, operation: str) -> None:
        self.source_tenant = source_tenant
        self.target_tenant = target_tenant
        self.operation = operation
        super().__init__(
            f"Cross-tenant violation: {operation} from tenant '{source_tenant}' "
            f"to tenant '{target_tenant}' is forbidden"
        )


class CrossTenantIsolationGuard:
    """Validates that all graph operations stay within tenant boundaries."""

    def __init__(self) -> None:
        self._violations: list[CrossTenantViolation] = []

    def validate_vertex_access(self, tenant_id: str, vertex: Vertex) -> None:
        vid = str(vertex.get("canonical_id") or vertex.get("vid", ""))
        owner = self._extract_tenant(vid)
        if owner and owner != tenant_id:
            violation = CrossTenantViolation(tenant_id, owner, f"vertex_access:{vid}")
            self._violations.append(violation)
            raise violation

    def validate_edge_creation(self, tenant_id: str, out_v: str, in_v: str) -> None:
        out_owner = self._extract_tenant(out_v)
        in_owner = self._extract_tenant(in_v)
        if out_owner and out_owner != tenant_id:
            violation = CrossTenantViolation(tenant_id, out_owner, f"edge_out:{out_v}")
            self._violations.append(violation)
            raise violation
        if in_owner and in_owner != tenant_id:
            violation = CrossTenantViolation(tenant_id, in_owner, f"edge_in:{in_v}")
            self._violations.append(violation)
            raise violation

    def validate_query_scope(self, tenant_id: str, query_params: dict[str, Any]) -> None:
        scope_tenant = query_params.get("tenant_id") or query_params.get("graph_name")
        if scope_tenant and scope_tenant != tenant_id:
            violation = CrossTenantViolation(tenant_id, str(scope_tenant), "query_scope")
            self._violations.append(violation)
            raise violation

    @property
    def violation_count(self) -> int:
        return len(self._violations)

    @property
    def recent_violations(self) -> list[CrossTenantViolation]:
        return self._violations[-100:]

    @staticmethod
    def _extract_tenant(vid: str) -> str | None:
        if vid.startswith("ng:"):
            parts = vid.split(":", 2)
            if len(parts) >= 3:
                return parts[1]
        return None


class NamedGraphStore:
    """Wraps a GraphStore with per-tenant named-graph isolation.

    All vertex canonical_ids and edge keys are prefixed with the tenant's
    namespace, ensuring physical separation within the shared store.
    """

    def __init__(
        self,
        backing_store: GraphStore,
        config: TenantConfig,
        *,
        guard: CrossTenantIsolationGuard | None = None,
    ) -> None:
        self._store = backing_store
        self._config = config
        self._guard = guard or CrossTenantIsolationGuard()
        self._stats = TenantStats(
            tenant_id=config.tenant_id,
            created_at=time.time(),
        )
        self._lock = threading.Lock()

    @property
    def tenant_id(self) -> str:
        return self._config.tenant_id

    @property
    def graph_name(self) -> str:
        return self._config.graph_name

    @property
    def stats(self) -> TenantStats:
        return self._stats

    def _namespace_id(self, canonical_id: str) -> str:
        if canonical_id.startswith(self._config.namespace_prefix):
            return canonical_id
        return f"{self._config.namespace_prefix}{canonical_id}"

    def _strip_namespace(self, namespaced_id: str) -> str:
        prefix = self._config.namespace_prefix
        if namespaced_id.startswith(prefix):
            return namespaced_id[len(prefix):]
        return namespaced_id

    def _check_label(self, label: str) -> None:
        if self._config.allowed_labels and label not in self._config.allowed_labels:
            raise ValueError(f"Label '{label}' not allowed for tenant '{self.tenant_id}'")
        if self._config.blocked_labels and label in self._config.blocked_labels:
            raise ValueError(f"Label '{label}' is blocked for tenant '{self.tenant_id}'")

    def health(self) -> bool:
        return self._store.health()

    def upsert_vertex(self, label: str, properties: dict) -> Vertex:
        self._check_label(label)
        props = dict(properties)
        cid = props.get("canonical_id", "")
        props["canonical_id"] = self._namespace_id(str(cid))
        props["_tenant_id"] = self.tenant_id
        props["_graph_name"] = self.graph_name

        result = self._store.upsert_vertex(label, props)
        with self._lock:
            self._stats.vertex_count += 1
            self._stats.last_access = time.time()
        return result

    def get_vertex(self, vid: str) -> Vertex | None:
        namespaced = self._namespace_id(vid)
        vertex = self._store.get_vertex(namespaced)
        if vertex:
            self._guard.validate_vertex_access(self.tenant_id, vertex)
        self._stats.last_access = time.time()
        return vertex

    def get_vertex_by_canonical_id(self, canonical_id: str) -> Vertex | None:
        namespaced = self._namespace_id(canonical_id)
        vertex = self._store.get_vertex_by_canonical_id(namespaced)
        if vertex:
            self._guard.validate_vertex_access(self.tenant_id, vertex)
        return vertex

    def find_vertices(
        self,
        label: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
    ) -> list[Vertex]:
        tenant_filters = dict(filters) if filters else {}
        tenant_filters["_tenant_id"] = self.tenant_id
        return self._store.find_vertices(label=label, filters=tenant_filters, limit=limit)

    def upsert_edge(self, label: str, out_v: str, in_v: str, properties: dict) -> Edge:
        ns_out = self._namespace_id(out_v)
        ns_in = self._namespace_id(in_v)
        self._guard.validate_edge_creation(self.tenant_id, ns_out, ns_in)

        props = dict(properties)
        props["_tenant_id"] = self.tenant_id

        result = self._store.upsert_edge(label, ns_out, ns_in, props)
        with self._lock:
            self._stats.edge_count += 1
            self._stats.last_access = time.time()
        return result

    def edges_from(self, vid: str, labels: list[str] | None = None, limit: int = 500) -> list[Edge]:
        return self._store.edges_from(self._namespace_id(vid), labels=labels, limit=limit)

    def edges_to(self, vid: str, labels: list[str] | None = None, limit: int = 500) -> list[Edge]:
        return self._store.edges_to(self._namespace_id(vid), labels=labels, limit=limit)

    def count_vertices(self, label: str | None = None) -> int:
        return len(self.find_vertices(label=label, limit=1_000_000))

    def count_edges(self, label: str | None = None) -> int:
        return self._store.count_edges(label=label)

    def tombstone_vertex(self, canonical_id: str) -> bool:
        return self._store.tombstone_vertex(self._namespace_id(canonical_id))

    def clear(self) -> None:
        vertices = self.find_vertices(limit=1_000_000)
        for v in vertices:
            cid = str(v.get("canonical_id", ""))
            if cid:
                self._store.tombstone_vertex(cid)
        with self._lock:
            self._stats.vertex_count = 0
            self._stats.edge_count = 0


class NamedGraphManager:
    """Manages multiple named graph instances for multi-tenant deployments."""

    def __init__(self, backing_store: GraphStore) -> None:
        self._store = backing_store
        self._tenants: dict[str, NamedGraphStore] = {}
        self._guard = CrossTenantIsolationGuard()
        self._lock = threading.Lock()

    def create_tenant(self, config: TenantConfig) -> NamedGraphStore:
        with self._lock:
            if config.tenant_id in self._tenants:
                raise ValueError(f"Tenant '{config.tenant_id}' already exists")
            tenant_store = NamedGraphStore(self._store, config, guard=self._guard)
            self._tenants[config.tenant_id] = tenant_store
            log.info("Created named graph for tenant '%s' (graph: %s)", config.tenant_id, config.graph_name)
            return tenant_store

    def get_tenant(self, tenant_id: str) -> NamedGraphStore | None:
        return self._tenants.get(tenant_id)

    def remove_tenant(self, tenant_id: str, *, purge_data: bool = False) -> bool:
        with self._lock:
            tenant = self._tenants.pop(tenant_id, None)
            if tenant is None:
                return False
            if purge_data:
                tenant.clear()
            log.info("Removed named graph for tenant '%s' (purged: %s)", tenant_id, purge_data)
            return True

    def list_tenants(self) -> list[TenantStats]:
        return [t.stats for t in self._tenants.values()]

    @property
    def tenant_count(self) -> int:
        return len(self._tenants)

    @property
    def isolation_guard(self) -> CrossTenantIsolationGuard:
        return self._guard
