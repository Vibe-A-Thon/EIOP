"""Tenant-namespace enforcement at the GraphStore port boundary (SR-TEN-003, CC3-011).

The managed backends (``hugegraph.py``, ``neo4j.py``, ``neptune.py``) carry no
tenant concept: every query they issue sees the whole graph. ``tenancy/layers.py``
enforces per-layer isolation for the *embedded* backends but does not wrap the
``GraphStore`` port. ``TenantScopedGraphStore`` closes that gap: it wraps any
``GraphStore`` and

* namespaces every written ``canonical_id`` as ``urn:eoip:{tenant_id}:{raw}``
  via ``TenantNamespace`` (a foreign-prefixed id raises ``ScopeViolationError``);
* stamps ``tenant_id`` on every written vertex/edge record;
* fails closed on reads: explicit foreign canonical ids raise
  ``ScopeViolationError``; foreign records reached by opaque ids are invisible
  (indistinguishable not-found), and scans only ever return owned records;
* refuses ``clear()`` — a tenant handle cannot wipe a shared store.
"""

from __future__ import annotations

from typing import Any

from eoip.authz.pdp import ScopeViolationError
from eoip.tenancy.isolation_hardened import (
    TENANT_ID_REGEX,
    InvalidTenantNamespaceError,
    TenantNamespace,
)


class TenantScopedGraphStore:
    def __init__(self, inner: Any, tenant_id: str) -> None:
        if not tenant_id or not TENANT_ID_REGEX.match(tenant_id):
            raise InvalidTenantNamespaceError(f"invalid tenant_id: {tenant_id!r}")
        self._inner = inner
        self.tenant_id = tenant_id
        self._prefix = f"urn:eoip:{tenant_id}:"

    # -- scoping helpers -----------------------------------------------------
    def _scope_id(self, canonical_id: str) -> str:
        """Namespace a raw id; a foreign tenant prefix raises ScopeViolationError."""
        return TenantNamespace.format_canonical_id(self.tenant_id, str(canonical_id))

    def _owns(self, record: dict | None) -> bool:
        if not record:
            return False
        cid = str(record.get("canonical_id") or "")
        if cid:
            return cid.startswith(self._prefix)
        return record.get("properties", {}).get("tenant_id") == self.tenant_id

    def _owned(self, records: list[dict], limit: int) -> list[dict]:
        return [rec for rec in records if self._owns(rec)][:limit]

    # -- metadata ------------------------------------------------------------
    def health(self) -> bool:
        return bool(self._inner.health())

    def ping(self) -> dict:
        return {**self._inner.ping(), "tenant_scope": self.tenant_id}

    def ensure_schema(self, manifest: dict) -> dict:
        return self._inner.ensure_schema(manifest)

    def schema_status(self) -> dict:
        return self._inner.schema_status()

    # -- vertices --------------------------------------------------------------
    def upsert_vertex(self, label: str, properties: dict) -> dict:
        scoped = dict(properties)
        scoped["canonical_id"] = self._scope_id(scoped.get("canonical_id", ""))
        scoped["tenant_id"] = self.tenant_id
        return self._inner.upsert_vertex(label, scoped)

    def get_vertex(self, vid: str) -> dict | None:
        record = self._inner.get_vertex(vid)
        return record if self._owns(record) else None

    def get_vertex_by_canonical_id(self, canonical_id: str) -> dict | None:
        return self._inner.get_vertex_by_canonical_id(self._scope_id(canonical_id))

    def find_vertex_by_property(
        self,
        label: str,
        key: str,
        value: Any,
        limit: int = 10,
        include_deleted: bool = False,
    ) -> list[dict]:
        records = self._inner.find_vertex_by_property(
            label, key, value, limit=limit, include_deleted=include_deleted
        )
        return self._owned(records, limit)

    def find_vertices(
        self,
        label: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> list[dict]:
        records = self._inner.find_vertices(
            label=label, filters=filters, limit=limit, include_deleted=include_deleted
        )
        return self._owned(records, limit)

    def count_vertices(self, label: str | None = None) -> int:
        return len(self.find_vertices(label=label, limit=1_000_000))

    # -- edges ---------------------------------------------------------------
    def _assert_owned_endpoint(self, vid: str) -> None:
        if self._inner.get_vertex(vid) is None:
            raise ScopeViolationError(f"edge endpoint {vid!r} does not exist")
        if not self._owns(self._inner.get_vertex(vid)):
            raise ScopeViolationError(
                f"edge endpoint {vid!r} belongs to another tenant"
            )

    def upsert_edge(self, label: str, out_v: str, in_v: str, properties: dict) -> dict:
        self._assert_owned_endpoint(out_v)
        self._assert_owned_endpoint(in_v)
        scoped = dict(properties)
        scoped["tenant_id"] = self.tenant_id
        return self._inner.upsert_edge(label, out_v, in_v, scoped)

    def get_edge(self, eid: str) -> dict | None:
        record = self._inner.get_edge(eid)
        return record if self._owns(record) else None

    def find_edge_by_key(self, edge_key: str) -> dict | None:
        record = self._inner.find_edge_by_key(edge_key)
        return record if self._owns(record) else None

    def find_edges(
        self,
        label: str | None = None,
        out_v: str | None = None,
        in_v: str | None = None,
        limit: int = 500,
        include_historical: bool = False,
    ) -> list[dict]:
        records = self._inner.find_edges(
            label=label, out_v=out_v, in_v=in_v, limit=limit,
            include_historical=include_historical,
        )
        return self._owned(records, limit)

    def edges_from(self, vid: str, labels: list[str] | None = None, limit: int = 500, include_historical: bool = False) -> list[dict]:
        self._assert_owned_endpoint(vid)
        records = self._inner.edges_from(vid, labels=labels, limit=limit, include_historical=include_historical)
        return self._owned(records, limit)

    def edges_to(self, vid: str, labels: list[str] | None = None, limit: int = 500, include_historical: bool = False) -> list[dict]:
        self._assert_owned_endpoint(vid)
        records = self._inner.edges_to(vid, labels=labels, limit=limit, include_historical=include_historical)
        return self._owned(records, limit)

    def count_edges(self, label: str | None = None) -> int:
        return len(self.find_edges(label=label, limit=1_000_000, include_historical=True))

    def bulk_load(self, vertices: list[dict], edges: list[dict], *, batch_size: int = 500) -> dict:
        scoped_vertices = []
        for vertex in vertices:
            props = dict(vertex["properties"])
            props["canonical_id"] = self._scope_id(props.get("canonical_id", ""))
            props["tenant_id"] = self.tenant_id
            scoped_vertices.append({**vertex, "properties": props})
        scoped_edges = []
        for edge in edges:
            props = dict(edge.get("properties", {}))
            props["tenant_id"] = self.tenant_id
            scoped_edges.append({**edge, "properties": props})
        return self._inner.bulk_load(scoped_vertices, scoped_edges, batch_size=batch_size)

    # -- maintenance -----------------------------------------------------------
    def tombstone_vertex(self, canonical_id: str) -> bool:
        return bool(self._inner.tombstone_vertex(self._scope_id(canonical_id)))

    def clear(self) -> None:
        raise ScopeViolationError(
            "a tenant-scoped handle cannot clear the shared graph store"
        )
