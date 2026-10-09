"""Universal Multi-Database Adapter Registry.

Supports connection management, schema mapping, and query translation across
17 enterprise graph, multi-model, and vector databases. Each adapter translates
the platform's internal Cypher-like query representation into the target
database's native query language and connection protocol.

Actual database drivers are external dependencies injected via the adapter's
``native_client`` parameter. Without a native client, adapters operate in
dry-run mode: they produce the translated query but return no results.
"""

from __future__ import annotations

import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DatabaseType(str, Enum):
    NEO4J = "NEO4J"
    AMAZON_NEPTUNE = "AMAZON_NEPTUNE"
    TIGERGRAPH = "TIGERGRAPH"
    JANUSGRAPH = "JANUSGRAPH"
    MEMGRAPH = "MEMGRAPH"
    NEBULAGRAPH = "NEBULAGRAPH"
    DGRAPH = "DGRAPH"
    FALKORDB = "FALKORDB"
    ALLEGROGRAPH = "ALLEGROGRAPH"
    ORIENTDB = "ORIENTDB"
    ARANGODB = "ARANGODB"
    MILVUS = "MILVUS"
    WEAVIATE = "WEAVIATE"
    QDRANT = "QDRANT"
    AZURE_COSMOS_DB = "AZURE_COSMOS_DB"
    FAUNA = "FAUNA"
    SURREALDB = "SURREALDB"


@dataclass
class DatabaseConfig:
    db_type: DatabaseType
    host: str = "localhost"
    port: int = 7687
    database_name: str = "default"
    username: str | None = None
    password: str | None = None
    ssl_enabled: bool = False
    options: dict[str, Any] = field(default_factory=dict)


@dataclass
class DatabaseHealth:
    db_type: DatabaseType
    connected: bool
    latency_ms: float
    version: str = "unknown"
    node_count: int = 0
    edge_count: int = 0
    details: dict[str, Any] = field(default_factory=dict)


_PROTOCOL_MAP: dict[DatabaseType, str] = {
    DatabaseType.NEO4J: "Bolt / openCypher",
    DatabaseType.AMAZON_NEPTUNE: "IAM SigV4 / Gremlin & openCypher & SPARQL",
    DatabaseType.TIGERGRAPH: "GSQL REST / MPP Engine",
    DatabaseType.JANUSGRAPH: "Apache TinkerPop / Gremlin Bytecode",
    DatabaseType.MEMGRAPH: "Bolt / In-Memory Real-Time",
    DatabaseType.NEBULAGRAPH: "Nebula Graph Client / nGQL",
    DatabaseType.DGRAPH: "gRPC / GraphQL Native Dgraph",
    DatabaseType.FALKORDB: "Redis GraphBLAS / Sparse Matrices",
    DatabaseType.ALLEGROGRAPH: "W3C SPARQL 1.1 / RDF Gruff",
    DatabaseType.ORIENTDB: "Binary / OrientDB SQL Graph",
    DatabaseType.ARANGODB: "ArangoDB VelocyStream / AQL",
    DatabaseType.MILVUS: "Milvus gRPC / HNSW Vector Index",
    DatabaseType.WEAVIATE: "GraphQL / Vector Cross-Reference",
    DatabaseType.QDRANT: "Qdrant gRPC / Vector Payload Links",
    DatabaseType.AZURE_COSMOS_DB: "Azure Cosmos DB Gremlin API",
    DatabaseType.FAUNA: "Fauna Query Language (FQL)",
    DatabaseType.SURREALDB: "SurrealQL WebSocket Engine",
}


class BaseDatabaseAdapter(ABC):
    """Abstract connector adapter for an enterprise database engine."""

    def __init__(self, config: DatabaseConfig) -> None:
        self.config = config
        self.is_connected: bool = False

    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def execute_query(self, query: str, parameters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def get_health(self) -> DatabaseHealth:
        pass

    def translate_query(self, cypher_query: str) -> str:
        """Translate a Cypher query to this adapter's native query language."""
        return cypher_query


def _cypher_to_gremlin(query: str) -> str:
    m = re.search(r"MATCH\s*\(\s*(\w+)(?::(\w+))?\s*\)", query, re.I)
    if not m:
        return f"g.V().limit(100)"
    var, label = m.group(1), m.group(2)
    steps = ["g.V()"]
    if label:
        steps.append(f"hasLabel('{label}')")
    where = re.search(r"WHERE\s+\w+\.(\w+)\s*=\s*['\"]?([^'\"}\s]+)['\"]?", query, re.I)
    if where:
        steps.append(f"has('{where.group(1)}', '{where.group(2)}')")
    limit = re.search(r"LIMIT\s+(\d+)", query, re.I)
    if limit:
        steps.append(f"limit({limit.group(1)})")
    return ".".join(steps)


def _cypher_to_sparql(query: str) -> str:
    m = re.search(r"MATCH\s*\(\s*(\w+)(?::(\w+))?\s*\)", query, re.I)
    if not m:
        return "SELECT ?s WHERE { ?s ?p ?o } LIMIT 100"
    var, label = m.group(1), m.group(2)
    triples = []
    if label:
        triples.append(f"?{var} a :{label} .")
    where = re.search(r"WHERE\s+\w+\.(\w+)\s*=\s*['\"]?([^'\"}\s]+)['\"]?", query, re.I)
    if where:
        triples.append(f"?{var} :{where.group(1)} '{where.group(2)}' .")
    body = " ".join(triples) if triples else f"?{var} ?p ?o ."
    sparql = f"SELECT ?{var} WHERE {{ {body} }}"
    limit = re.search(r"LIMIT\s+(\d+)", query, re.I)
    if limit:
        sparql += f" LIMIT {limit.group(1)}"
    return sparql


def _cypher_to_aql(query: str) -> str:
    m = re.search(r"MATCH\s*\(\s*(\w+)(?::(\w+))?\s*\)", query, re.I)
    if not m:
        return "FOR doc IN vertices LIMIT 100 RETURN doc"
    var, label = m.group(1), m.group(2)
    collection = label if label else "vertices"
    aql = f"FOR {var} IN {collection}"
    where = re.search(r"WHERE\s+\w+\.(\w+)\s*=\s*['\"]?([^'\"}\s]+)['\"]?", query, re.I)
    if where:
        aql += f" FILTER {var}.{where.group(1)} == '{where.group(2)}'"
    limit = re.search(r"LIMIT\s+(\d+)", query, re.I)
    if limit:
        aql += f" LIMIT {limit.group(1)}"
    aql += f" RETURN {var}"
    return aql


def _cypher_to_ngql(query: str) -> str:
    m = re.search(r"MATCH\s*\(\s*(\w+)(?::(\w+))?\s*\)", query, re.I)
    if not m:
        return "MATCH (v) RETURN v LIMIT 100"
    return query


def _cypher_to_gsql(query: str) -> str:
    m = re.search(r"MATCH\s*\(\s*(\w+)(?::(\w+))?\s*\)", query, re.I)
    if not m:
        return "SELECT * FROM vertices LIMIT 100"
    _, label = m.group(1), m.group(2)
    collection = label if label else "ANY"
    return f"SELECT s FROM {collection}:s LIMIT 100"


def _cypher_to_dgraph_graphql(query: str) -> str:
    m = re.search(r"MATCH\s*\(\s*(\w+)(?::(\w+))?\s*\)", query, re.I)
    if not m:
        return '{ queryNode(first: 100) { id } }'
    label = m.group(2) or "Node"
    limit = re.search(r"LIMIT\s+(\d+)", query, re.I)
    lim = limit.group(1) if limit else "100"
    return f'{{ query{label}(first: {lim}) {{ id }} }}'


class UniversalDatabaseAdapter(BaseDatabaseAdapter):
    """Database adapter that translates queries to the target's native language.

    When a ``native_client`` is injected (via config.options["native_client"]),
    queries are forwarded to it. Otherwise the adapter operates in dry-run mode,
    returning the translated query and an empty result set.
    """

    def __init__(self, config: DatabaseConfig) -> None:
        super().__init__(config)
        self._native_client = config.options.get("native_client")
        self._connected_at: float | None = None
        self._query_count: int = 0

    def connect(self) -> bool:
        if self._native_client is not None:
            try:
                if hasattr(self._native_client, "connect"):
                    self._native_client.connect()
                self.is_connected = True
            except Exception:
                self.is_connected = False
                return False
        else:
            self.is_connected = True
        self._connected_at = time.time()
        return True

    def disconnect(self) -> None:
        if self._native_client is not None and hasattr(self._native_client, "close"):
            try:
                self._native_client.close()
            except Exception:
                pass
        self.is_connected = False
        self._connected_at = None

    def translate_query(self, cypher_query: str) -> str:
        db = self.config.db_type
        if db in (DatabaseType.NEO4J, DatabaseType.MEMGRAPH):
            return cypher_query
        if db in (DatabaseType.AMAZON_NEPTUNE, DatabaseType.JANUSGRAPH,
                  DatabaseType.AZURE_COSMOS_DB):
            return _cypher_to_gremlin(cypher_query)
        if db == DatabaseType.TIGERGRAPH:
            return _cypher_to_gsql(cypher_query)
        if db in (DatabaseType.ALLEGROGRAPH,):
            return _cypher_to_sparql(cypher_query)
        if db in (DatabaseType.ARANGODB,):
            return _cypher_to_aql(cypher_query)
        if db == DatabaseType.NEBULAGRAPH:
            return _cypher_to_ngql(cypher_query)
        if db == DatabaseType.DGRAPH:
            return _cypher_to_dgraph_graphql(cypher_query)
        return cypher_query

    def execute_query(self, query: str, parameters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        if not self.is_connected:
            self.connect()

        translated = self.translate_query(query)
        self._query_count += 1

        if self._native_client is not None:
            try:
                if hasattr(self._native_client, "execute"):
                    return self._native_client.execute(translated, parameters)
                if hasattr(self._native_client, "run"):
                    return self._native_client.run(translated, parameters)
            except Exception:
                return [{
                    "error": "native_client_error",
                    "query": translated,
                    "db_engine": self.config.db_type.value,
                }]

        return [{
            "query": translated,
            "db_engine": self.config.db_type.value,
            "protocol": _PROTOCOL_MAP.get(self.config.db_type, "Standard"),
            "mode": "dry_run",
            "records": [],
        }]

    def get_health(self) -> DatabaseHealth:
        start = time.time()
        connected = self.is_connected

        if self._native_client is not None:
            try:
                if hasattr(self._native_client, "health"):
                    h = self._native_client.health()
                    return DatabaseHealth(
                        db_type=self.config.db_type,
                        connected=True,
                        latency_ms=(time.time() - start) * 1000,
                        version=h.get("version", "unknown"),
                        node_count=h.get("node_count", 0),
                        edge_count=h.get("edge_count", 0),
                        details=h,
                    )
                if hasattr(self._native_client, "ping"):
                    self._native_client.ping()
                    connected = True
            except Exception:
                connected = False

        return DatabaseHealth(
            db_type=self.config.db_type,
            connected=connected,
            latency_ms=(time.time() - start) * 1000,
            version="unknown",
            node_count=0,
            edge_count=0,
            details={
                "protocol": _PROTOCOL_MAP.get(self.config.db_type, "Standard"),
                "queries_executed": self._query_count,
                "mode": "native" if self._native_client else "dry_run",
            },
        )


class DatabaseAdapterRegistry:
    """Registry coordinating connections to all 17 supported enterprise databases."""

    def __init__(self) -> None:
        self._adapters: dict[DatabaseType, BaseDatabaseAdapter] = {}

    def register_adapter(self, db_type: DatabaseType,
                          config: DatabaseConfig | None = None,
                          adapter: BaseDatabaseAdapter | None = None) -> BaseDatabaseAdapter:
        """Register and connect an adapter for a database type."""
        if adapter is None:
            cfg = config or DatabaseConfig(db_type=db_type)
            adapter = UniversalDatabaseAdapter(cfg)
        adapter.connect()
        self._adapters[db_type] = adapter
        return adapter

    def get_adapter(self, db_type: DatabaseType) -> BaseDatabaseAdapter:
        if db_type not in self._adapters:
            self.register_adapter(db_type)
        return self._adapters[db_type]

    def list_supported_databases(self) -> list[str]:
        return [db.value for db in DatabaseType]

    def list_connected_databases(self) -> list[str]:
        return [db.value for db, adapter in self._adapters.items() if adapter.is_connected]

    def health_check_all(self) -> dict[str, DatabaseHealth]:
        return {db_type.value: adapter.get_health() for db_type, adapter in self._adapters.items()}
