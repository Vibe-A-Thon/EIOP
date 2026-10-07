"""Graph store port (NFR-MAINT-001: typed ports).

Implementations:
- HugeGraphStore: client over HugeGraph REST/Gremlin.
- NeptuneGraphStore: client over Amazon Neptune HTTPS endpoints.
- Neo4jGraphStore: client over Neo4j transactional Cypher HTTP.
- MemoryGraphStore: in-process store used by automated tests and explicit
  local developer harnesses.
"""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from time import monotonic
from typing import Any, Protocol

_query_deadline: ContextVar[float | None] = ContextVar("eoip_graph_query_deadline", default=None)


class GraphQueryTimeout(ValueError):
    """A graph operation exceeded the caller's cooperative deadline."""


class BulkLoadError(RuntimeError):
    """A bounded native bulk-load batch failed after earlier batches committed."""

    def __init__(self, message: str, *, vertices_committed: int, edges_committed: int):
        self.vertices_committed = vertices_committed
        self.edges_committed = edges_committed
        super().__init__(message)


@contextmanager
def graph_query_deadline(deadline: float):
    token = _query_deadline.set(deadline)
    try:
        yield
    finally:
        _query_deadline.reset(token)


def remaining_query_seconds() -> float | None:
    deadline = _query_deadline.get()
    return None if deadline is None else max(0.0, deadline - monotonic())


class Vertex(dict):
    """A vertex record: {vid, canonical_id, label, properties}"""


class Edge(dict):
    """An edge record: {eid, label, out_v, in_v, out_cid, in_cid, properties}"""


class GraphStore(Protocol):
    def health(self) -> bool: ...

    def ping(self) -> dict: ...

    # -- schema ------------------------------------------------------------
    def ensure_schema(self, manifest: dict) -> dict: ...

    def schema_status(self) -> dict: ...

    # -- vertices ------------------------------------------------------------
    def upsert_vertex(self, label: str, properties: dict) -> Vertex: ...

    def get_vertex(self, vid: str) -> Vertex | None: ...

    def get_vertex_by_canonical_id(self, canonical_id: str) -> Vertex | None: ...

    def find_vertex_by_property(
        self,
        label: str,
        key: str,
        value: Any,
        limit: int = 10,
        include_deleted: bool = False,
    ) -> list[Vertex]: ...

    def find_vertices(
        self,
        label: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> list[Vertex]: ...

    def count_vertices(self, label: str | None = None) -> int: ...

    # -- edges ---------------------------------------------------------------
    def upsert_edge(self, label: str, out_v: str, in_v: str, properties: dict) -> Edge: ...

    def get_edge(self, eid: str) -> Edge | None: ...

    def find_edge_by_key(self, edge_key: str) -> Edge | None: ...

    def find_edges(
        self,
        label: str | None = None,
        out_v: str | None = None,
        in_v: str | None = None,
        limit: int = 500,
        include_historical: bool = False,
    ) -> list[Edge]: ...

    def edges_from(self, vid: str, labels: list[str] | None = None, limit: int = 500, include_historical: bool = False) -> list[Edge]: ...

    def edges_to(self, vid: str, labels: list[str] | None = None, limit: int = 500, include_historical: bool = False) -> list[Edge]: ...

    def count_edges(self, label: str | None = None) -> int: ...

    def bulk_load(
        self,
        vertices: list[Vertex],
        edges: list[Edge],
        *,
        batch_size: int = 500,
    ) -> dict: ...

    # -- maintenance ---------------------------------------------------------
    def tombstone_vertex(self, canonical_id: str) -> bool: ...

    def clear(self) -> None: ...
