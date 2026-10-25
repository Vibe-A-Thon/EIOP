"""Universal Multi-Database Adapter Registry.

Supports connection management, schema mapping, and query translation across
39+ enterprise graph, semantic, multi-model, vector, and operational databases:

1. Native Graph & Semantic Knowledge Graph Databases:
   - Neo4j, Amazon Neptune, TigerGraph, JanusGraph, Memgraph, NebulaGraph, Dgraph,
     FalkorDB, AllegroGraph, OrientDB, ArangoDB, TypeDB, Apache AGE, Apache HugeGraph,
     ArcadeDB, Ontotext GraphDB, Stardog, RDFox, OpenLink Virtuoso, Apache Jena TDB2,
     Oxigraph, TerminusDB, CozoDB, Cayley.
2. Multimodel & Relational Graph Engines:
   - Oracle Property Graph, Google Cloud Spanner Graph, Microsoft SQL Server Graph,
     MongoDB Atlas, Amazon Neptune Analytics, Azure Cosmos DB, Fauna, SurrealDB.
3. Vector Databases & Hybrid Retrieval Engines:
   - Milvus, Weaviate, Qdrant, Pinecone, Chroma, LanceDB, Vespa, pgvector,
     OpenSearch, Elasticsearch, Redis Search, ClickHouse, Typesense.
4. Operational State, Memory & Analytical Databases:
   - PostgreSQL, SQLite, Redis, FoundationDB, DynamoDB, Apache Cassandra,
     DuckDB, Apache Pinot, Apache Druid, TimescaleDB.

Adapters operate in native mode when a ``native_client`` is supplied,
or in deterministic dry-run / contract validation mode when operating in
air-gapped or test environments.
"""

from __future__ import annotations

import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DatabaseType(str, Enum):
    # 1. Native Graph & Semantic KGs
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
    TYPEDB = "TYPEDB"
    APACHE_AGE = "APACHE_AGE"
    APACHE_HUGEGRAPH = "APACHE_HUGEGRAPH"
    ARCADEDB = "ARCADEDB"
    ONTOTEXT_GRAPHDB = "ONTOTEXT_GRAPHDB"
    STARDOG = "STARDOG"
    RDFOX = "RDFOX"
    OPENLINK_VIRTUOSO = "OPENLINK_VIRTUOSO"
    APACHE_JENA_TDB2 = "APACHE_JENA_TDB2"
    OXIGRAPH = "OXIGRAPH"
    TERMINUSDB = "TERMINUSDB"
    COZODB = "COZODB"
    CAYLEY = "CAYLEY"

    # 2. Multimodel & Relational Graph Engines
    ORACLE_PROPERTY_GRAPH = "ORACLE_PROPERTY_GRAPH"
    GOOGLE_SPANNER_GRAPH = "GOOGLE_SPANNER_GRAPH"
    MSSQL_GRAPH = "MSSQL_GRAPH"
    MONGODB_ATLAS = "MONGODB_ATLAS"
    NEPTUNE_ANALYTICS = "NEPTUNE_ANALYTICS"
    AZURE_COSMOS_DB = "AZURE_COSMOS_DB"
    FAUNA = "FAUNA"
    SURREALDB = "SURREALDB"

    # 3. Vector Databases & Search Engines
    MILVUS = "MILVUS"
    WEAVIATE = "WEAVIATE"
    QDRANT = "QDRANT"
    PINECONE = "PINECONE"
    CHROMA = "CHROMA"
    LANCEDB = "LANCEDB"
    VESPA = "VESPA"
    PGVECTOR = "PGVECTOR"
    OPENSEARCH = "OPENSEARCH"
    ELASTICSEARCH = "ELASTICSEARCH"
    REDIS_SEARCH = "REDIS_SEARCH"
    CLICKHOUSE = "CLICKHOUSE"
    TYPESENSE = "TYPESENSE"

    # 4. Operational State, Memory & Analytics
    POSTGRESQL = "POSTGRESQL"
    SQLITE = "SQLITE"
    REDIS = "REDIS"
    FOUNDATIONDB = "FOUNDATIONDB"
    DYNAMODB = "DYNAMODB"
    APACHE_CASSANDRA = "APACHE_CASSANDRA"
    DUCKDB = "DUCKDB"
    APACHE_PINOT = "APACHE_PINOT"
    APACHE_DRUID = "APACHE_DRUID"
    TIMESCALEDB = "TIMESCALEDB"


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
    DatabaseType.TYPEDB: "TypeDB Client / TypeQL Polymorphic",
    DatabaseType.APACHE_AGE: "PostgreSQL libpq / Cypher in SQL (agtype)",
    DatabaseType.APACHE_HUGEGRAPH: "HugeGraph REST Client / Gremlin",
    DatabaseType.ARCADEDB: "ArcadeDB HTTP/Binary Multimodel Engine",
    DatabaseType.ONTOTEXT_GRAPHDB: "RDF4J / SPARQL Semantic Engine",
    DatabaseType.STARDOG: "Stardog Protocol / SPARQL Reasoning",
    DatabaseType.RDFOX: "RDFox High-Performance In-Memory Datalog",
    DatabaseType.OPENLINK_VIRTUOSO: "Virtuoso JDBC / Linked Data SPARQL",
    DatabaseType.APACHE_JENA_TDB2: "Apache Jena ARQ / SPARQL 1.1",
    DatabaseType.OXIGRAPH: "Rust / PyOxigraph Embedded SPARQL",
    DatabaseType.TERMINUSDB: "TerminusDB WOQL / Git-for-Data Engine",
    DatabaseType.COZODB: "CozoDB Datalog Engine",
    DatabaseType.CAYLEY: "Cayley Gizmo / Graph Engine",
    DatabaseType.ORACLE_PROPERTY_GRAPH: "Oracle Net Services / SQL:2023 PGQ",
    DatabaseType.GOOGLE_SPANNER_GRAPH: "Google Cloud Spanner gRPC / Graph Query",
    DatabaseType.MSSQL_GRAPH: "T-SQL Graph Match / Node-Edge Tables",
    DatabaseType.MONGODB_ATLAS: "MongoDB Wire Protocol / Aggregation Pipeline",
    DatabaseType.NEPTUNE_ANALYTICS: "AWS SigV4 / Neptune Graph Analytics",
    DatabaseType.AZURE_COSMOS_DB: "Azure Cosmos DB Gremlin API",
    DatabaseType.FAUNA: "Fauna Query Language (FQL)",
    DatabaseType.SURREALDB: "SurrealQL WebSocket Engine",
    DatabaseType.MILVUS: "Milvus gRPC / HNSW Vector Index",
    DatabaseType.WEAVIATE: "GraphQL / Vector Cross-Reference",
    DatabaseType.QDRANT: "Qdrant gRPC / Vector Payload Links",
    DatabaseType.PINECONE: "Pinecone gRPC API / Managed Vector Index",
    DatabaseType.CHROMA: "Chroma Embedded / REST Vector Store",
    DatabaseType.LANCEDB: "Apache Arrow / Serverless Vector DB",
    DatabaseType.VESPA: "Vespa HTTP API / Neural Search Engine",
    DatabaseType.PGVECTOR: "PostgreSQL pgvector / HNSW Extension",
    DatabaseType.OPENSEARCH: "OpenSearch REST / Lucene k-NN",
    DatabaseType.ELASTICSEARCH: "Elasticsearch REST / Dense Vector",
    DatabaseType.REDIS_SEARCH: "Redis RESP / RediSearch HNSW Index",
    DatabaseType.CLICKHOUSE: "ClickHouse TCP / Columnar Vector Similarity",
    DatabaseType.TYPESENSE: "Typesense REST / Fast Typo-Tolerant Search",
    DatabaseType.POSTGRESQL: "PostgreSQL libpq / ACID Relational & Audit",
    DatabaseType.SQLITE: "SQLite3 Embedded Local Transaction Store",
    DatabaseType.REDIS: "Redis RESP / In-Memory Coordination & Queues",
    DatabaseType.FOUNDATIONDB: "FoundationDB Client / Distributed KV Engine",
    DatabaseType.DYNAMODB: "AWS DynamoDB SDK / Managed Distributed KV",
    DatabaseType.APACHE_CASSANDRA: "CQL Binary Protocol / High-Write Event Store",
    DatabaseType.DUCKDB: "DuckDB Embedded OLAP Analytics Engine",
    DatabaseType.APACHE_PINOT: "Pinot Broker REST / Real-time Distributed OLAP",
    DatabaseType.APACHE_DRUID: "Druid SQL / Streaming Time-Series Analytics",
    DatabaseType.TIMESCALEDB: "PostgreSQL TimescaleDB / Hypertables",
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
        return "g.V().limit(100)"
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


# FT-F08: SQL/AQL translations never interpolate values. Identifiers must be plain
# ASCII names (allow-list) and are quoted; values travel as bound parameters.
_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]{0,62}")
_WHERE = re.compile(r"WHERE\s+\w+\.(\w+)\s*=\s*(?:'([^']*)'|\"([^\"]*)\"|([^'\"}\s]+))", re.I)
_MATCH = re.compile(r"MATCH\s*\(\s*(\w+)(?::(\w+))?\s*\)", re.I)
_LIMIT = re.compile(r"LIMIT\s+(\d{1,9})\b", re.I)


class UnsafeIdentifierError(ValueError):
    """A label/property name in a translated query is not a plain identifier."""


def _identifier(name: str) -> str:
    if not _IDENTIFIER.fullmatch(name):
        raise UnsafeIdentifierError(f"unsupported identifier: {name!r}")
    return name


def _where_clause(query: str) -> tuple[str, str] | None:
    where = _WHERE.search(query)
    if not where:
        return None
    value = next(group for group in where.groups()[1:] if group is not None)
    return _identifier(where.group(1)), value


def _cypher_to_aql_bound(query: str) -> tuple[str, dict[str, Any]]:
    m = _MATCH.search(query)
    if not m:
        return "FOR doc IN vertices LIMIT 100 RETURN doc", {}
    var = _identifier(m.group(1))
    params: dict[str, Any] = {"@collection": _identifier(m.group(2)) if m.group(2) else "vertices"}
    parts = [f"FOR {var} IN @@collection"]
    where = _where_clause(query)
    if where:
        params["attr"], params["value"] = where
        parts.append(f"FILTER {var}.@attr == @value")
    limit = _LIMIT.search(query)
    if limit:
        params["limit"] = int(limit.group(1))
        parts.append("LIMIT @limit")
    parts.append(f"RETURN {var}")
    return " ".join(parts), params


def _cypher_to_sql_bound(query: str) -> tuple[str, dict[str, Any]]:
    m = _MATCH.search(query)
    table = _identifier(m.group(2)) if (m and m.group(2)) else "entities"
    parts = ["SELECT * FROM", f'"{table}"']
    params: dict[str, Any] = {}
    where = _where_clause(query)
    if where:
        column, params["p0"] = where
        parts.append(f'WHERE "{column}" = :p0')
    limit = _LIMIT.search(query)
    if limit:
        params["limit"] = int(limit.group(1))
        parts.append("LIMIT :limit")
    return " ".join(parts), params


def _cypher_to_aql(query: str) -> str:
    return _cypher_to_aql_bound(query)[0]


def _cypher_to_sql(query: str) -> str:
    return _cypher_to_sql_bound(query)[0]


_SQL_ENGINES = frozenset({
    DatabaseType.POSTGRESQL, DatabaseType.PGVECTOR, DatabaseType.SQLITE,
    DatabaseType.DUCKDB, DatabaseType.CLICKHOUSE, DatabaseType.TIMESCALEDB,
})


class UniversalDatabaseAdapter(BaseDatabaseAdapter):
    """Universal multi-model database adapter translating queries to native protocols."""

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

        # Native Cypher / openCypher engines
        if db in (DatabaseType.NEO4J, DatabaseType.MEMGRAPH, DatabaseType.FALKORDB, DatabaseType.NEBULAGRAPH):
            return cypher_query

        # Apache AGE (Cypher wrapped in SQL cypher() function)
        if db == DatabaseType.APACHE_AGE:
            # AGE executes the Cypher itself; the only SQL-level risk is closing the
            # $$ dollar-quote early, so such queries are refused.
            if "$$" in cypher_query:
                raise UnsafeIdentifierError("Cypher for Apache AGE must not contain '$$'")
            return f"SELECT * FROM cypher('graph_name', $$ {cypher_query} $$) as (v agtype);"  # noqa: S608

        # Gremlin-based engines
        if db in (DatabaseType.AMAZON_NEPTUNE, DatabaseType.JANUSGRAPH,
                  DatabaseType.AZURE_COSMOS_DB, DatabaseType.APACHE_HUGEGRAPH):
            return _cypher_to_gremlin(cypher_query)

        # SPARQL & RDF engines
        if db in (DatabaseType.ALLEGROGRAPH, DatabaseType.ONTOTEXT_GRAPHDB,
                  DatabaseType.STARDOG, DatabaseType.RDFOX, DatabaseType.OPENLINK_VIRTUOSO,
                  DatabaseType.APACHE_JENA_TDB2, DatabaseType.OXIGRAPH):
            return _cypher_to_sparql(cypher_query)

        # ArangoDB
        if db == DatabaseType.ARANGODB:
            return _cypher_to_aql(cypher_query)

        # Relational SQL & Vector SQL engines
        if db in _SQL_ENGINES:
            return _cypher_to_sql(cypher_query)

        # TypeDB TypeQL
        if db == DatabaseType.TYPEDB:
            m = re.search(r"MATCH\s*\(\s*(\w+)(?::(\w+))?\s*\)", cypher_query, re.I)
            t = _identifier(m.group(2)) if (m and m.group(2)) else "entity"
            return f"match $x isa {t}; get $x;"

        # Dgraph GraphQL
        if db == DatabaseType.DGRAPH:
            m = re.search(r"MATCH\s*\(\s*(\w+)(?::(\w+))?\s*\)", cypher_query, re.I)
            lbl = _identifier(m.group(2)) if (m and m.group(2)) else "Node"
            return f"{{ query{lbl}(first: 100) {{ id }} }}"

        # TigerGraph GSQL
        if db == DatabaseType.TIGERGRAPH:
            m = re.search(r"MATCH\s*\(\s*(\w+)(?::(\w+))?\s*\)", cypher_query, re.I)
            collection = _identifier(m.group(2)) if (m and m.group(2)) else "ANY"
            return f"SELECT s FROM {collection}:s LIMIT 100"  # noqa: S608 (allow-listed identifier)

        # CozoDB Datalog
        if db == DatabaseType.COZODB:
            return "?[id, label] := *entities[id, label]"

        return cypher_query

    def translate_query_bound(self, cypher_query: str) -> tuple[str, dict[str, Any]]:
        """Translate and return (query text, bound parameters).

        For SQL and AQL engines the text holds placeholders only (FT-F08); values
        are in the returned parameters. Other engines return no extra parameters.
        """
        db = self.config.db_type
        if db == DatabaseType.ARANGODB:
            return _cypher_to_aql_bound(cypher_query)
        if db in _SQL_ENGINES:
            return _cypher_to_sql_bound(cypher_query)
        return self.translate_query(cypher_query), {}

    def execute_query(self, query: str, parameters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        if not self.is_connected:
            self.connect()

        translated, bound = self.translate_query_bound(query)
        parameters = {**(parameters or {}), **bound} if (parameters or bound) else parameters
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
            "protocol": _PROTOCOL_MAP.get(self.config.db_type, "Standard Protocol"),
            "parameters": parameters or {},
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
                "protocol": _PROTOCOL_MAP.get(self.config.db_type, "Standard Protocol"),
                "queries_executed": self._query_count,
                "mode": "native" if self._native_client else "dry_run",
            },
        )


class DatabaseAdapterRegistry:
    """Registry coordinating connections across all 39+ supported enterprise databases."""

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
