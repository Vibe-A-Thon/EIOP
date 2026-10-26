"""Cypher-over-Bolt/RESP protocol interfaces for Memgraph and FalkorDB.

**External gate**: EOIP does not implement the Bolt (Memgraph) or RESP
(FalkorDB) wire protocols in-repo, and adding a driver dependency is out of
scope for this package. This module therefore provides:

* ``BoltLikeTransport`` / ``RespLikeTransport`` — protocol interfaces an
  external transport implementation must satisfy,
* ``CypherConnectionConfig`` — validated connection config for both backends,
* ``CypherAdapterManifest`` helpers — what a conforming adapter must support
  (SR-GDB-002/003 records).

No client is faked. The BackendCatalog marks both backends ``manifest-only``
with ``external_gate=True``; instantiation is refused explicitly.
"""

from __future__ import annotations

from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field


class CypherConnectionConfig(BaseModel):
    """Connection config for a Cypher-over-wire graph database (§6)."""

    model_config = ConfigDict(extra="forbid")

    protocol: str = Field(description="'bolt' (Memgraph/Neo4j) or 'resp' (FalkorDB).")
    host: str = "localhost"
    port: int = 7687
    database: str = ""
    username: str = ""
    password: str = ""
    use_tls: bool = False
    max_connection_lifetime: float = 3600.0
    fetch_size: int = 1000


class BoltLikeTransport(Protocol):
    """External gate: a Bolt-protocol transport for Memgraph (or Neo4j).

    An external implementation (e.g. the official Bolt driver) provides this
    surface; EOIP code depends only on the protocol, never on the driver.
    """

    def run(self, cypher: str, parameters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Run one Cypher statement and return result records as dicts."""
        ...

    def close(self) -> None: ...


class RespLikeTransport(Protocol):
    """External gate: a RESP-protocol transport for FalkorDB's Cypher surface."""

    def graph_query(self, graph: str, cypher: str) -> list[list[Any]]:
        """Run a GRAPH.QUERY on the named graph; returns result rows."""
        ...

    def close(self) -> None: ...


class CypherAdapterCapability(BaseModel):
    """SR-GDB-002 record of what a conforming Memgraph/FalkorDB adapter must
    implement before its manifest can move from manifest-only to real."""

    model_config = ConfigDict(extra="forbid")

    backend: str
    required_transport: str
    supports: list[str] = Field(
        default_factory=lambda: [
            "idempotent vertex upsert by canonical_id",
            "idempotent edge upsert by deterministic edge_key",
            "parameter-bound Cypher (no string interpolation)",
            "tombstone via deleted_at property",
            "health/ping via guaranteed query",
        ]
    )
    recorded_deviations: list[str] = Field(default_factory=list)


MEMGRAPH_CAPABILITY = CypherAdapterCapability(
    backend="memgraph", required_transport="bolt",
    recorded_deviations=["Memgraph community has no multi-database; use one instance per domain."],
)

FALKORDB_CAPABILITY = CypherAdapterCapability(
    backend="falkordb", required_transport="resp",
    recorded_deviations=[
        "FalkorDB is the GraphBLAS successor to RedisGraph (§6.5); SSPL license.",
        "Named graphs isolate tenants (KGR-G-013 gap until formalized).",
    ],
)
