"""CapabilityManifest models and the full §6 backend manifest set (SR-GDB-002/003).

Each adapter/backend MUST publish a CapabilityManifest so the planner can
choose pushdown vs in-engine execution and refuse/degrade unsupported plans
explicitly (never silently). Backend-specific behavior is recorded here, not
scattered in code (SR-GDB-003). Certification tiers per SR-GDB-004:
A = Certified, B = Compatible, C = Community/Experimental, P2 = roadmap.

Corrections from gap analysis §6.5 applied throughout:

* **OrientDB dedup** — OrientDB is classified only as a native multimodel
  graph (HTTP Gremlin); it is NOT an operational/document store entry and
  appears exactly once in the catalog.
* **Vector DBs reclassified** — Pinecone, Chroma, LanceDB, Vespa, pgvector,
  OpenSearch, Elasticsearch, Redis Search, ClickHouse, Typesense,
  Milvus/Weaviate/Qdrant are vector/retrieval engines, NOT graph databases.
  Their role is ``vector_index``; they do not claim GraphStore conformance.
* **FalkorDB note** — RedisGraph successor (GraphBLAS), SSPL-licensed; Cypher
  via Bolt/RESP. Transport is an External gate.
* **Kùzu archived-warning** — Kùzu's upstream lineage shows an archived/
  maintenance-risk status; manifests carry an ``archived_warning`` note and
  Tier C until maintenance is verified (SR-GDB-004 marketing constraint).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

AdapterStatus = Literal["real", "manifest-only"]
CertificationTier = Literal["A", "B", "C", "P2"]
Deployment = Literal["local", "cloud", "both"]
Role = Literal[
    "graph_store",
    "rdf_store",
    "vector_index",
    "operational",
    "multimodel",
    "query_builder",
]


class CapabilityManifest(BaseModel):
    """SR-GDB-002 capability manifest for one database backend."""

    model_config = ConfigDict(extra="forbid")

    backend: str
    """Canonical backend key (lowercase, e.g. ``janusgraph``)."""
    display_name: str
    category: Literal["native_graph", "rdf_store", "multimodel", "vector", "operational"]
    native_surface: list[str] = Field(default_factory=list)
    """Native protocol(s)/language(s) the database actually speaks."""
    deployment: Deployment = "both"
    tier: CertificationTier = "C"
    role: Role = "graph_store"
    notes: list[str] = Field(default_factory=list)
    adapter_status: AdapterStatus = "manifest-only"
    """``real`` = in-repo protocol-compatible adapter exists; ``manifest-only``
    = capability record only, catalog refuses instantiation."""
    conformance: list[str] = Field(default_factory=list)
    """SR-GDB-003: recorded backend-specific conformance notes / golden-query
    deviations."""
    external_gate: bool = False
    """True when live transport requires a protocol EOIP does not implement
    in-repo (Bolt/RESP, vendor SDK); a protocol interface is provided but no
    client is faked."""
    connection_config: dict[str, Any] = Field(default_factory=dict)
    """Default connection config merged under deployment config."""


MANIFESTS: list[CapabilityManifest] = [
    # ------------------------------------------------------------------ §6.1
    CapabilityManifest(
        backend="neo4j",
        display_name="Neo4j",
        category="native_graph",
        native_surface=["Cypher (Bolt + transactional HTTP)"],
        deployment="both",
        tier="A",
        role="graph_store",
        adapter_status="real",
        notes=["GraphStore adapter in eoip.graph.neo4j (transactional Cypher HTTP)."],
        conformance=["Verified in-repo: eoip.graph.neo4j.Neo4jGraphStore."],
    ),
    CapabilityManifest(
        backend="neptune",
        display_name="Amazon Neptune",
        category="native_graph",
        native_surface=["openCypher HTTPS", "Gremlin", "SPARQL"],
        deployment="cloud",
        tier="A",
        role="graph_store",
        adapter_status="real",
        notes=["GraphStore adapter in eoip.graph.neptune (openCypher HTTPS)."],
    ),
    CapabilityManifest(
        backend="hugegraph",
        display_name="Apache HugeGraph",
        category="native_graph",
        native_surface=["Gremlin (REST)", "REST schema API"],
        deployment="both",
        tier="A",
        role="graph_store",
        adapter_status="real",
        notes=["Default deployment backend; adapter in eoip.graph.hugegraph."],
        conformance=["HugeGraph 1.7 does not honor UNIQUE edge indexes; adapter uses SECONDARY + sort-key emulation."],
    ),
    CapabilityManifest(
        backend="memory",
        display_name="EOIP MemoryGraphStore",
        category="native_graph",
        native_surface=["EOIP GraphStore API"],
        deployment="local",
        tier="A",
        role="graph_store",
        adapter_status="real",
        notes=["In-process store for tests and local harnesses."],
    ),
    CapabilityManifest(
        backend="janusgraph",
        display_name="JanusGraph",
        category="native_graph",
        native_surface=["Gremlin (TinkerPop, script HTTP)"],
        deployment="both",
        tier="B",
        role="graph_store",
        adapter_status="real",
        notes=[
            ("Gremlin dialect adapter reusing the HugeGraph Gremlin client "
            "shape with JanusGraph connection config (eoip.adapters.janusgraph)."),
            ("Schema management is declarative/transactional; adapter relies on "
            "schema-flexible vertices with deterministic eoip vid properties."),
        ],
    ),
    CapabilityManifest(
        backend="memgraph",
        display_name="Memgraph",
        category="native_graph",
        native_surface=["Cypher (Bolt)"],
        deployment="both",
        tier="C",
        role="graph_store",
        adapter_status="manifest-only",
        external_gate=True,
        notes=[
            ("Bolt transport is an External gate: eoip.adapters.cypher_bolt "
            "defines the BoltLikeTransport protocol interface; no in-repo client."),
            "Memgraph 3.8+; BSL 1.1 license note from §6 source research.",
        ],
        connection_config={"protocol": "bolt", "host": "localhost", "port": 7687, "database": ""},
    ),
    CapabilityManifest(
        backend="falkordb",
        display_name="FalkorDB",
        category="native_graph",
        native_surface=["Cypher (RESP)"],
        deployment="both",
        tier="C",
        role="graph_store",
        adapter_status="manifest-only",
        external_gate=True,
        notes=[
            ("§6.5 correction: RedisGraph successor (GraphBLAS sparse-matrix "
            "engine), SSPL license; not Redis 'Graph' any more."),
            ("RESP transport is an External gate: eoip.adapters.cypher_bolt "
            "defines the RespLikeTransport protocol interface; no in-repo client."),
            ("HNSW vector co-location and per-tenant named graphs are roadmap "
            "gaps (KGR-G-013/016), not adapter claims."),
        ],
        connection_config={"protocol": "resp", "host": "localhost", "port": 6379},
    ),
    CapabilityManifest(
        backend="tigergraph",
        display_name="TigerGraph",
        category="native_graph",
        native_surface=["GSQL", "GSQL REST++"],
        deployment="both",
        tier="C",
        role="graph_store",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="nebulagraph",
        display_name="NebulaGraph",
        category="native_graph",
        native_surface=["nGQL"],
        deployment="both",
        tier="C",
        role="graph_store",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="dgraph",
        display_name="Dgraph",
        category="native_graph",
        native_surface=["GraphQL+- / DQL"],
        deployment="both",
        tier="C",
        role="graph_store",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="allegrograph",
        display_name="AllegroGraph",
        category="native_graph",
        native_surface=["SPARQL", "SPARQL 1.1"],
        deployment="both",
        tier="C",
        role="rdf_store",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="arangodb",
        display_name="ArangoDB",
        category="multimodel",
        native_surface=["AQL"],
        deployment="both",
        tier="C",
        role="multimodel",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="typedb",
        display_name="TypeDB",
        category="native_graph",
        native_surface=["TypeQL"],
        deployment="both",
        tier="C",
        role="graph_store",
        adapter_status="manifest-only",
        notes=["Schema-first strongly-typed knowledge graph."],
    ),
    CapabilityManifest(
        backend="arcadedb",
        display_name="ArcadeDB",
        category="multimodel",
        native_surface=["SQL", "OpenCypher subset", "Gremlin subset", "HTTP"],
        deployment="both",
        tier="C",
        role="multimodel",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="cayley",
        display_name="Cayley",
        category="native_graph",
        native_surface=["GraphQL", "Gremlin-ish HTTP"],
        deployment="local",
        tier="C",
        role="graph_store",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="cozodb",
        display_name="CozoDB",
        category="native_graph",
        native_surface=["Datalog (CozoScript)"],
        deployment="local",
        tier="C",
        role="graph_store",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="kuzu",
        display_name="Kùzu",
        category="native_graph",
        native_surface=["Cypher"],
        deployment="local",
        tier="C",
        role="graph_store",
        adapter_status="manifest-only",
        notes=[
            ("§6.5 archived-warning: upstream repository shows archived/"
            "maintenance-risk status; candidate for embedded DP-0/edge use "
            "only after maintenance verification (SR-GDB-004)."),
        ],
    ),
    CapabilityManifest(
        backend="terminusdb",
        display_name="TerminusDB",
        category="native_graph",
        native_surface=["WOQL", "JSON-LD"],
        deployment="both",
        tier="C",
        role="graph_store",
        adapter_status="manifest-only",
        notes=["Version-controlled document/graph store; WOQL query surface."],
    ),
    # ------------------------------------------------------------------ §6.2
    CapabilityManifest(
        backend="apache_age",
        display_name="Apache AGE",
        category="multimodel",
        native_surface=["openCypher wrapped in SQL (PostgreSQL extension)"],
        deployment="both",
        tier="B",
        role="query_builder",
        adapter_status="real",
        notes=[
            ("SQL-wrapped openCypher query builder in eoip.adapters.apache_age "
            "builds deterministic AGE SQL over any existing PostgreSQL port; "
            "no new dependency."),
        ],
        connection_config={"host": "localhost", "port": 5432, "database": "postgres", "graph": "eoip"},
    ),
    CapabilityManifest(
        backend="orientdb",
        display_name="OrientDB",
        category="multimodel",
        native_surface=["HTTP Gremlin-ish", "SQL"],
        deployment="both",
        tier="C",
        role="multimodel",
        adapter_status="manifest-only",
        external_gate=True,
        notes=[
            ("§6.5 correction (dedup): OrientDB is a multimodel (document+graph) "
            "database listed once here; it is not an operational-store entry."),
            "HTTP Gremlin-ish transport is an External gate: manifest-only.",
        ],
    ),
    # ------------------------------------------------------------------ §6.3 RDF stores
    CapabilityManifest(
        backend="graphdb",
        display_name="Ontotext GraphDB",
        category="rdf_store",
        native_surface=["SPARQL 1.1", "RDF4J"],
        deployment="both",
        tier="C",
        role="rdf_store",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="stardog",
        display_name="Stardog",
        category="rdf_store",
        native_surface=["SPARQL 1.1", "GraphQL"],
        deployment="both",
        tier="C",
        role="rdf_store",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="rdfox",
        display_name="RDFox",
        category="rdf_store",
        native_surface=["SPARQL 1.1", "Datalog"],
        deployment="both",
        tier="C",
        role="rdf_store",
        adapter_status="manifest-only",
        notes=["In-memory RDF rule engine; Datalog reasoning surface."],
    ),
    CapabilityManifest(
        backend="virtuoso",
        display_name="OpenLink Virtuoso",
        category="rdf_store",
        native_surface=["SPARQL", "SQL"],
        deployment="both",
        tier="C",
        role="rdf_store",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="jena_tdb2",
        display_name="Apache Jena TDB2",
        category="rdf_store",
        native_surface=["SPARQL 1.1"],
        deployment="local",
        tier="C",
        role="rdf_store",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="oxigraph",
        display_name="Oxigraph",
        category="rdf_store",
        native_surface=["SPARQL 1.1"],
        deployment="local",
        tier="C",
        role="rdf_store",
        adapter_status="manifest-only",
    ),
    # ------------------------------------------------------- §6.4 multimodel / relational-graph
    CapabilityManifest(
        backend="oracle_pg",
        display_name="Oracle Property Graph",
        category="multimodel",
        native_surface=["PGQL", "SQL/PGQ"],
        deployment="both",
        tier="P2",
        role="graph_store",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="spanner_graph",
        display_name="Google Cloud Spanner Graph",
        category="multimodel",
        native_surface=["Graph extension to GoogleSQL (GQL)"],
        deployment="cloud",
        tier="P2",
        role="graph_store",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="sqlserver_graph",
        display_name="Microsoft SQL Server Graph",
        category="multimodel",
        native_surface=["T-SQL graph extensions (NODE/EDGE tables)"],
        deployment="both",
        tier="P2",
        role="graph_store",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="mongodb_atlas",
        display_name="MongoDB Atlas",
        category="multimodel",
        native_surface=["MQL", "Atlas $graphLookup"],
        deployment="cloud",
        tier="C",
        role="multimodel",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="neptune_analytics",
        display_name="Amazon Neptune Analytics",
        category="multimodel",
        native_surface=["openCypher", "Gremlin (serverless analytics)"],
        deployment="cloud",
        tier="P2",
        role="graph_store",
        adapter_status="manifest-only",
    ),
    # ------------------------------------------------------------------ §6.5 vector (reclassified)
    CapabilityManifest(
        backend="pinecone",
        display_name="Pinecone",
        category="vector",
        native_surface=["REST/JSON vector API"],
        deployment="cloud",
        tier="C",
        role="vector_index",
        adapter_status="manifest-only",
        notes=["§6.5 reclassification: vector engine, not a graph database."],
    ),
    CapabilityManifest(
        backend="chroma",
        display_name="Chroma",
        category="vector",
        native_surface=["Embedded/HTTP vector API"],
        deployment="local",
        tier="C",
        role="vector_index",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="lancedb",
        display_name="LanceDB",
        category="vector",
        native_surface=["Embedded columnar vector API"],
        deployment="local",
        tier="C",
        role="vector_index",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="vespa",
        display_name="Vespa",
        category="vector",
        native_surface=["Vespa Query Language (YQL)"],
        deployment="both",
        tier="C",
        role="vector_index",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="pgvector",
        display_name="pgvector",
        category="vector",
        native_surface=["PostgreSQL <->> operators", "ivfflat/HNSW"],
        deployment="both",
        tier="B",
        role="vector_index",
        adapter_status="manifest-only",
        notes=["Vector lives inside PostgreSQL; pairs naturally with Apache AGE for graph+vector."],
    ),
    CapabilityManifest(
        backend="opensearch",
        display_name="OpenSearch",
        category="vector",
        native_surface=["k-NN REST", "Lucene"],
        deployment="both",
        tier="C",
        role="vector_index",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="elasticsearch",
        display_name="Elasticsearch",
        category="vector",
        native_surface=["kNN dense-vector REST", "Lucene"],
        deployment="both",
        tier="C",
        role="vector_index",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="redis_search",
        display_name="Redis Search",
        category="vector",
        native_surface=["FT.SEARCH", "RediSearch"],
        deployment="both",
        tier="C",
        role="vector_index",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="clickhouse",
        display_name="ClickHouse",
        category="vector",
        native_surface=["SQL + vector functions"],
        deployment="both",
        tier="C",
        role="vector_index",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="typesense",
        display_name="Typesense",
        category="vector",
        native_surface=["REST search API"],
        deployment="both",
        tier="C",
        role="vector_index",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="milvus",
        display_name="Milvus",
        category="vector",
        native_surface=["Milvus SDK/REST"],
        deployment="both",
        tier="C",
        role="vector_index",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="weaviate",
        display_name="Weaviate",
        category="vector",
        native_surface=["GraphQL/REST vector API"],
        deployment="both",
        tier="C",
        role="vector_index",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="qdrant",
        display_name="Qdrant",
        category="vector",
        native_surface=["REST/gRPC vector API"],
        deployment="both",
        tier="C",
        role="vector_index",
        adapter_status="manifest-only",
    ),
    # ------------------------------------------------------------------ §6.6 operational
    CapabilityManifest(
        backend="postgresql",
        display_name="PostgreSQL",
        category="operational",
        native_surface=["SQL"],
        deployment="both",
        tier="B",
        role="operational",
        adapter_status="manifest-only",
        notes=["System-of-record for relational data; Apache AGE adds graph surface."],
    ),
    CapabilityManifest(
        backend="sqlite",
        display_name="SQLite",
        category="operational",
        native_surface=["SQL"],
        deployment="local",
        tier="B",
        role="operational",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="redis",
        display_name="Redis",
        category="operational",
        native_surface=["RESP"],
        deployment="both",
        tier="B",
        role="operational",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="foundationdb",
        display_name="FoundationDB",
        category="operational",
        native_surface=["Tuple/byte KV API"],
        deployment="both",
        tier="C",
        role="operational",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="dynamodb",
        display_name="Amazon DynamoDB",
        category="operational",
        native_surface=["PartiQL", "KV API"],
        deployment="cloud",
        tier="C",
        role="operational",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="cassandra",
        display_name="Apache Cassandra",
        category="operational",
        native_surface=["CQL"],
        deployment="both",
        tier="C",
        role="operational",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="duckdb",
        display_name="DuckDB",
        category="operational",
        native_surface=["SQL (OLAP)"],
        deployment="local",
        tier="B",
        role="operational",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="pinot",
        display_name="Apache Pinot",
        category="operational",
        native_surface=["PQL/Pinot SQL"],
        deployment="both",
        tier="C",
        role="operational",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="druid",
        display_name="Apache Druid",
        category="operational",
        native_surface=["Druid SQL", "native JSON query"],
        deployment="both",
        tier="C",
        role="operational",
        adapter_status="manifest-only",
    ),
    CapabilityManifest(
        backend="timescaledb",
        display_name="TimescaleDB",
        category="operational",
        native_surface=["SQL (hypertables)"],
        deployment="both",
        tier="C",
        role="operational",
        adapter_status="manifest-only",
    ),
]


def load_manifests() -> dict[str, CapabilityManifest]:
    """Return the §6 manifest set keyed by backend (deterministic order)."""
    return {m.backend: m for m in MANIFESTS}
