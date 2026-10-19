| Field | Value |
|---|---|
| Registry ID | T-C01-memgraph |
| Tier | A (candidate backend; in-memory Cypher engine with GraphRAG / agent-memory positioning; Neo4j-protocol-compatible alternative) |
| Versions examined | Memgraph v3.13.2 (2026-10-09; source read at tag `v3.13.2`), v3.13.0 (2026-09-09), v3.8.0 (2026-02-11, licence and repo-merge boundary), v3.7.2 (2025-12-23, last pre-amendment BSL); archived `memgraph/mage` v3.7.2 (2025-12-23); `memgraph/ai-toolkit` (mcp-memgraph, langchain-memgraph) at `main`, latest tag `actions-graph-v0.5.0` 2026-10-13 |
| Verified on | 2026-10-18 |
| Worker | W04 |

## 1. Identity, current status, tier, and sources

- **What it is.** Memgraph is a C++ in-memory labelled-property-graph database that speaks Bolt (Neo4j wire protocol) and an openCypher dialect, owned by Memgraph Ltd (London/Zagreb). Repository `github.com/memgraph/memgraph`, default branch `master`, active (last push 2026-10-16), repository description "High-performance open-source in-memory graph database for GraphRAG, AI memory, agentic AI, and real-time graph analytics" [CLAIM-memgraph-01].
- **Current version.** v3.13.2, 2026-10-09 (bug-fix: SSO login on coordinators). Cadence is roughly monthly minors with patch releases: v3.8.0 2026-02-11, v3.8.1 2026-02-17, v3.10.0 2026-05-13, v3.11.0 2026-06-17, v3.12.0 2026-07-15, v3.13.0 2026-09-09, v3.13.1 2026-09-14 [CLAIM-memgraph-02].
- **MAGE (Memgraph Advanced Graph Extensions).** Until v3.7.2 MAGE lived in `github.com/memgraph/mage` under Apache-2.0. Announced 2025-11-07 and executed in v3.8.0, MAGE and `mgcxx` were merged into the main repository (`src/mage`), the old repository was archived, and **the merged code is released under the Memgraph BSL**, not Apache-2.0 [CLAIM-memgraph-06]. The registry entry "Memgraph (with MAGE)" therefore now means one product under one licence; the Apache-2.0 MAGE exists only as the frozen archive (≤ v3.7.2).
- **Members of this entry.** Memgraph Community Edition (MCE, BSL), Memgraph Enterprise (MEL; licence-key unlocked in the same binary), MAGE (query-module library, BSL from v3.8.0), Memgraph Lab (desktop/web IDE, proprietary Lab User Licence Agreement), Memgraph Cloud (managed service on AWS), `memgraph/ai-toolkit` (MIT: `mcp-memgraph`, `langchain-memgraph`, `memgraph-toolbox`) [CLAIM-memgraph-09][CLAIM-memgraph-10][CLAIM-memgraph-25].
- **Licence status — the single most important finding.** The repository `LICENSE` states code is "variously licensed under the Business Source License 1.1 (BSL), the Memgraph Enterprise License (MEL)" [CLAIM-memgraph-03]. From v3.8.0 the BSL carries a new Additional Use Grant dated 2026-01-01 that limits production use to "internal business purposes" and forbids (a) embedding or distributing to third parties, (b) DBaaS hosting, (c) competing works [CLAIM-memgraph-04]. The pre-2026 grant had allowed an "Integrated Solution" hosted as SaaS [CLAIM-memgraph-05]. Embedding and distribution to end customers requires the separate **Memgraph OEM License** [CLAIM-memgraph-09]. Section 10 covers the effect on EOIP.
- **Tier reason.** Tier A. Memgraph is a credible extra backend: it speaks Cypher and Bolt, so EOIP's Neo4j adapter path is close to reusable. It is also a direct competitor in "graph database for GraphRAG / agent memory" positioning, and its tenancy, vector and MCP designs set buyer expectations.
- **Traps resolved.** (1) The pricing page calls Community "open source", but the licence text says BSL "is not an 'open source' license"; we follow the licence text [CLAIM-memgraph-10]. (2) The MAGE licence changed with the repository merge, and Apache-2.0 should not be assumed for current MAGE [CLAIM-memgraph-06]. (3) The `cross_database` module became Enterprise-only in v3.13.0 [CLAIM-memgraph-33].
- **Sources used (15).** GitHub repository metadata and releases; `LICENSE` and `licenses/BSL.txt` at tags v3.7.2, v3.8.0 to v3.13.2 and `master`; archived `mage` README; release notes; docs pages on enabling Enterprise, multi-tenancy, tenant profiles, storage memory usage, data durability, transactions, replication, HA, vector search, text search, Cypher differences, query plan, MCP, integrations and GraphRAG; memgraph.com/pricing and /legal; source files at v3.13.2; benchgraph pages (vendor). Full list in Appendix C.

## 2. Primary problem, target workloads, concrete example workflows

**Problem.** Memgraph targets low-latency OLTP traversal plus in-database analytics on graphs that fit in RAM, with streaming ingest. The vendor positions it for "GraphRAG, AI memory, agentic AI, and real-time graph analytics" [CLAIM-memgraph-01][CLAIM-memgraph-27].

**Workloads.** Fraud and risk rings, network/IT topology and impact analysis, supply chain, real-time recommendation, cybersecurity graphs, and, since 2024–2026, GraphRAG and agent memory backends (integrations with LlamaIndex, LangChain/LangGraph, Cognee, Mem0, LightRAG) [CLAIM-memgraph-26].

**Example workflows (EOIP-relevant).**
1. *Service-account blast radius (J9).* Kafka/Redpanda/Pulsar stream → Python transformation module → Cypher `MERGE` → `MATCH (sa:ServiceAccount {id:$id})-[*BFS ..6]-(x)` with built-in BFS → PageRank/betweenness from MAGE to rank impacted assets [CLAIM-memgraph-23][CLAIM-memgraph-30][CLAIM-memgraph-34].
2. *GraphRAG retrieval.* Vector index on `:Chunk(embedding)` → `CALL vector_search.search('idx', 10, $q)` → expand to entities → text search via Tantivy `text_search.search` → context for an LLM. Memgraph Lab's chat or an MCP client drives it [CLAIM-memgraph-21][CLAIM-memgraph-22][CLAIM-memgraph-25].
3. *Per-tenant knowledge graphs (Enterprise).* `CREATE DATABASE tenant_a; CREATE TENANT PROFILE gold LIMIT memory_limit 4096 MB; SET TENANT PROFILE ...; GRANT DATABASE tenant_a TO role_a` [CLAIM-memgraph-19][CLAIM-memgraph-20].

**Suitability for on-prem local-first.** The software is technically strong: a single binary or Docker image, no cloud dependency, Linux packages, Helm charts. Commercially it is constrained, because the Community grant forbids distribution to third parties (Section 10).

## 3. Feature inventory

| Area | Feature | Status | Evidence |
|---|---|---|---|
| Storage | In-memory transactional (default), in-memory analytical, on-disk transactional (RocksDB) | Present / ON_DISK **experimental** | [CLAIM-memgraph-11] |
| Storage | Light edges, property compression (zlib), float resolution reduction | Present (opt-in flags) | [CLAIM-memgraph-12] |
| Transactions | SI (default), READ_COMMITTED, READ_UNCOMMITTED; optimistic commit-time conflicts | Present | [CLAIM-memgraph-15] |
| Durability | WAL + periodic snapshots, snapshot on exit, CRC32 WAL checksums (v3.12), S3 snapshot recovery | Present | [CLAIM-memgraph-16][CLAIM-memgraph-34] |
| Durability | CRON snapshot schedules | Enterprise-only | [CLAIM-memgraph-16] |
| Replication | MAIN/REPLICA, SYNC / ASYNC / STRICT_SYNC (2PC), manual failover | Present (Community) | [CLAIM-memgraph-17] |
| HA | Raft coordinators (NuRaft), automatic failover, routing, ISSU on Helm | Enterprise-only | [CLAIM-memgraph-18] |
| Scale-out | Sharding / partitioned graph | **Absent** (single-writer MAIN; replicas for reads) | [CLAIM-memgraph-17][CLAIM-memgraph-18] (reasoned) |
| Tenancy | Multiple databases per instance | Enterprise-only for non-default DBs | [CLAIM-memgraph-19] |
| Tenancy | Tenant profiles (per-DB memory cap), SUSPEND/RESUME DATABASE | Enterprise-only | [CLAIM-memgraph-20][CLAIM-memgraph-02] |
| Security | Users and passwords, TLS | Present | [CLAIM-memgraph-07] (inference: not on Enterprise list) |
| Security | RBAC, label-based (LBAC), property-based (PBAC, v3.12) access control, LDAP/SAML/OIDC, impersonation, audit log | Enterprise-only | [CLAIM-memgraph-07][CLAIM-memgraph-29] |
| Security | FIPS 140-3 mode | Enterprise-only, experimental (v3.13.1) | [CLAIM-memgraph-31] |
| Query | openCypher dialect, EXPLAIN/PROFILE, index hints, `ANALYZE GRAPH` | Present (dialect gaps, §5.3) | [CLAIM-memgraph-23][CLAIM-memgraph-24] |
| Query | Parallel Cypher execution (`USING PARALLEL EXECUTION`) | Enterprise-only (v3.8) | [CLAIM-memgraph-24] |
| Query | Built-in deep paths: BFS, DFS, weighted SP, all SP, K-shortest | Present | [CLAIM-memgraph-23] |
| Query | GQL / SQL/PGQ / Gremlin / SPARQL | Absent | [CLAIM-memgraph-23] (none documented) |
| Search | Vector index (USearch) on nodes and edges, multi-label / wildcard | Present (Community) | [CLAIM-memgraph-21] |
| Search | Full-text (Tantivy) on nodes and edges, fuzzy, regex | Present (GA since 3.6) | [CLAIM-memgraph-22] |
| Analytics | MAGE query modules (C++/Python/Rust), PageRank, community detection, centralities, etc. | Present (BSL from v3.8) | [CLAIM-memgraph-30][CLAIM-memgraph-06] |
| Analytics | Dynamic (incremental) graph algorithms | Enterprise-only | [CLAIM-memgraph-07][CLAIM-memgraph-30] |
| Analytics | `cross_database` module | Enterprise-only (v3.13.0) | [CLAIM-memgraph-33] |
| Ingest | Kafka / Redpanda / Pulsar streams with transformation modules; triggers (BEFORE/AFTER COMMIT) | Present | [CLAIM-memgraph-34] |
| Lifecycle | TTL | Enterprise-only | [CLAIM-memgraph-07] |
| Ops | Prometheus/OpenMetrics HTTP metrics | Enterprise-only | [CLAIM-memgraph-07] |
| AI | MCP server (mcp-memgraph, MIT), read-only default, optional OIDC/JWT per-tenant routing | Present (separate repo) | [CLAIM-memgraph-25] |
| AI | LangChain/LangGraph toolkit, LlamaIndex graph store, Cognee/Mem0/LightRAG integrations | Present (third-party or MIT) | [CLAIM-memgraph-26] |
| UI | Memgraph Lab (visual queries, GSS styling, chat); Lab SSO, monitoring, sharing | Present (proprietary) / Enterprise for SSO, sharing | [CLAIM-memgraph-07][CLAIM-memgraph-09] |
| Reasoning | RDFS/OWL/SHACL/Datalog | Absent | none documented |
| Temporal | Bitemporal / as-of queries | Absent (temporal data types only) | none documented |
| Deploy | Docker, DEB/RPM, Helm, Memgraph Cloud (AWS) | Present | [CLAIM-memgraph-10][CLAIM-memgraph-18] |

## 4. Text-based architecture diagram

```
 Clients: Neo4j Bolt drivers / Memgraph Lab / mgconsole / mcp-memgraph (MIT, HTTP or stdio) / LangChain, LlamaIndex
        │ Bolt (TCP 7687, optional TLS; bolt+routing in HA)
        ▼
 ┌──────────────────────────── memgraph process (C++) ────────────────────────────┐
 │ Session / auth (users; Enterprise: RBAC, LBAC, PBAC, SSO, audit)               │
 │   │                                                                            │
 │ DBMS handler (src/dbms) ── database "memgraph" (default) ── tenant DBs (Ent.)  │
 │   │      shared: CPU, config, auth store      per-DB: storage, indexes, data dir│
 │   ▼                                                                            │
 │ Query engine: ANTLR openCypher parser (Cypher.g4) → AST → semantic analysis    │
 │   → rule-based planner + cardinality cost estimator → operator tree            │
 │   (ScanAll*, Expand, ExpandVariable[BFS/DFS/WSP/KSP], HashJoin, Filter, ...)   │
 │   → pull-based execution; Enterprise: parallel execution                       │
 │   │             ▲ query modules: MAGE C++ / Python / Rust (CALL proc)          │
 │   ▼                                                                            │
 │ Storage v2 (per DB)                                                            │
 │   SkipList<Vertex>, SkipList<Edge> (light edges: no edge SkipList)            │
 │   Vertex{gid, labels, in_edges, out_edges, PropertyStore, RWSpinLock, Delta*} │
 │   Delta undo chains + CommitInfo timestamps → snapshot isolation, GC           │
 │   Indexes: label, label+property, edge-type, point, global property (3.13),    │
 │            text (Tantivy, Rust), vector (USearch)                              │
 │   Durability: WAL (CRC32) + snapshots → data_dir/databases/<db>/               │
 │   ON_DISK mode: RocksDB key-value serialization (experimental, no HA)          │
 │   Streams: Kafka/Pulsar consumers → transformation modules → Cypher            │
 └────────────────────────────────────────────────────────────────────────────────┘
        │ replication: deltas / WAL / snapshots (SYNC, ASYNC, STRICT_SYNC=2PC)
        ▼
 REPLICA instances (read-only)  ◄── control plane (Enterprise HA): 3+ COORDINATORS
                                    (NuRaft Raft log; leader promotes MAIN, routing table)
```

## 5. Under-the-hood reconstruction

The blueprint below comes from documentation and source files at tag `v3.13.2`. Statements not backed by a cited file are marked *hypothesis*.

### 5.1 Data model
Labelled property graph. Vertices carry a 64-bit `Gid`, a small vector of `LabelId`s and a `PropertyStore`. Edges carry a `Gid`, an `EdgeTypeId` (stored in the adjacency triple) and an optional `PropertyStore` (`--storage-properties-on-edges`). Labels, edge types and property keys are interned to integer IDs through a name-ID mapper. Constraints cover existence, uniqueness and type on node labels only; relationship constraints raise `SemanticException` [CLAIM-memgraph-23]. The schema is optional. Enums and `SHOW SCHEMA INFO` are used by the MCP tools [CLAIM-memgraph-25]. There are no hyperedges, no edge-on-edge and no named graphs beyond whole databases.

### 5.2 Storage layout and indexing
- **Object store.** `src/storage/v2/vertex.hpp` defines `struct Vertex { const Gid gid; small_vector<LabelId> labels; Edges in_edges; Edges out_edges; PropertyStore properties; RWSpinLock lock; PointerPack<Delta,2> delta_; }` with `static_assert(sizeof(Vertex) == 80)`. `Edges` is a `small_vector<tuple<EdgeTypeId, Vertex*, EdgeRef>>` [CLAIM-memgraph-13]. This is **index-free adjacency with direct pointers**: expanding a vertex walks an inline vector, with no index lookup. Vertices and edges live in a lock-free `utils::SkipList` (`src/utils/skip_list.hpp`) keyed by Gid. Each node adds 8 B plus 8 B per level pointer [CLAIM-memgraph-12].
- **Memory model.** The documented minimum is 136 B per vertex (80 B object plus a 56 B Delta) and 88 B per edge (32 B plus 56 B), plus about 24 B of SkipList overhead per edge. The summary formula is "V×204 B + E×154 B". The worked example uses 252 B/172 B, an internal inconsistency we record rather than resolve [CLAIM-memgraph-12]. Light edges (`--storage-light-edge`) drop the edge SkipList (about 24 B per edge saved) at the cost of slower edge-by-ID lookup [CLAIM-memgraph-12].
- **Properties.** `src/storage/v2/property_store.cpp` uses a packed variable-length encoding (BOOL 2 B, INT 3–10 B, DOUBLE 4/6/10 B, STRING ≥ 4 B), with optional zlib compression (off by default) [CLAIM-memgraph-12].
- **Secondary indexes.** Label, label+property (composite in 3.x), edge-type, edge-type+property, point (geo), global vertex-property (3.13) [CLAIM-memgraph-02]. Text indexes are implemented in Rust on Tantivy (`src/storage/v2/indices/text_index.cpp` bridges to Rust; Tantivy 0.25 in v3.10) [CLAIM-memgraph-22]. Vector indexes use USearch (`src/storage/v2/indices/vector_index.cpp`). From v3.8 the vector is stored only in the index, with the property store holding a reference [CLAIM-memgraph-21].
- **Constraints do not create indexes**, and indexes are not auto-created [CLAIM-memgraph-23].
- **On-disk mode.** RocksDB key-value serialization of nodes and edges. Objects touched by a transaction must still fit in RAM. Only snapshot isolation is supported, with no replication or HA, and the mode is "still in the experimental phase" [CLAIM-memgraph-11].

### 5.3 Query pipeline and planning
- **Parser.** ANTLR grammar `src/query/frontend/opencypher/grammar/Cypher.g4` → AST → semantic analysis (symbol table) → planner. The planner is rule-based (`src/query/plan/rule_based_planner.hpp`) and generates candidate plans that a **cardinality-based cost estimator** (`cost_estimator.hpp`: `cardinality_ *= VerticesCount(label)`, `IncrementCost(kScanAll)`) compares. `ANALYZE GRAPH` collects label/property statistics [CLAIM-memgraph-24].
- **Operators.** `ScanAll`, `ScanAllByLabel`, `ScanAllByLabelProperties`, `ScanAllByPointDistance`, `Expand`, `ExpandVariable`, `HashJoin`, `Filter`, `Aggregate`, `CreateExpand` and others. Execution is pull-based (Volcano-style; *hypothesis* for the exact cursor model, consistent with `operator.cpp` cursor classes) [CLAIM-memgraph-24].
- **Deep paths.** Built-in `-[*BFS]-`, `-[*WSHORTEST (r,n|r.w)]-`, `*ALLSHORTEST`, `*KSHORTEST|k`. These are in-engine operators rather than procedures, which is why Memgraph replaces Neo4j's `shortestPath()` and quantified path patterns [CLAIM-memgraph-23].
- **Vector indexes are not used by the planner.** They are reached only through `vector_search.search()` procedures, which return results under READ_UNCOMMITTED semantics for the index [CLAIM-memgraph-21].
- **Parallel execution** of Cypher has been an Enterprise feature since v3.8 [CLAIM-memgraph-24].
- **Cypher dialect gaps against Neo4j 5 / openCypher (documented)** [CLAIM-memgraph-23]:
  - no quantified path patterns (`--{1,4}`) and no `SHORTEST k` syntax;
  - no `!` label negation;
  - no patterns inside arbitrary functions such as `size((n)-->())`;
  - no multi-value `CASE WHEN a, b`, no `IS ::` type predicates;
  - missing functions: `exists(n.prop)`, `isEmpty`, `nullIf`, `percentileCont/Disc`, `stDev/stDevP`, `isNaN`, `cot`, `degrees`, `radians`, `haversin`, `normalize`, `time()`;
  - no named indexes/constraints (names are parsed then ignored), so `DROP CONSTRAINT <name>` fails;
  - `COUNT{}` and `COLLECT{}` subqueries only from v3.13.0;
  - APOC is not native; MAGE ships partial equivalents (*hypothesis* on coverage depth — not measured).
- **Consequence for EOIP.** The Neo4j adapter (`graph/neo4j.py`, HTTP transactional endpoint, BL-03) **cannot be pointed at Memgraph unchanged**: Memgraph exposes Bolt and no Neo4j HTTP `/db/{db}/tx/commit` endpoint (*hypothesis*: no HTTP Cypher endpoint is documented in the pages read). A Bolt-based adapter variant plus a dialect profile is needed.

### 5.4 Reasoning
None. There are no RDFS/OWL/SHACL/Datalog facilities. Triggers (`BEFORE COMMIT` / `AFTER COMMIT`) and query modules are the only rule hooks [CLAIM-memgraph-34], so ontology reasoning stays in EOIP's layer.

### 5.5 Concurrency and transactions
- MVCC by **undo-delta chains**. Each object holds a pointer to its newest `Delta`. Deltas (`src/storage/v2/delta.hpp`) record inverse actions (`DELETE_OBJECT`, `RECREATE_OBJECT`, `ADD_LABEL`/`REMOVE_LABEL`, `SET_PROPERTY`, `ADD_IN_EDGE`/`ADD_OUT_EDGE`/`REMOVE_*`) with a shared `CommitInfo{atomic<uint64_t> timestamp}` and `command_id` [CLAIM-memgraph-14]. A reader at start-timestamp *t* reconstructs its view by applying deltas newer than *t* in reverse.
- Pseudocode (reconstruction, consistent with the cited structures):

```
read(obj, tx):
  lock_shared(obj.lock); view = copy(obj.current); d = obj.delta; unlock
  while d and not visible(d.commit_info.timestamp, tx):   # committed after tx.start or uncommitted by others
      view = undo(view, d); d = d.next
  return view
write(obj, tx):
  lock(obj.lock)
  if obj.delta and obj.delta.commit_info not committed by tx and not visible-to-tx: abort(SerializationError)  # optimistic
  push Delta(inverse_of(change), tx.commit_info, tx.command_id); apply change in place; unlock
commit(tx): ts = next_ts(); tx.commit_info.timestamp = ts; append WAL(deltas); replicate(deltas, mode)
gc(): unlink deltas older than oldest active start-ts; purge index entries; free
```

- Isolation is SI by default, with RC and RU available. Conflicts are detected at write/commit and the transaction rolls back [CLAIM-memgraph-15]. Analytical mode removes deltas, giving "no isolation levels and no ACID guarantees" and up to about 6× faster import (vendor statement) [CLAIM-memgraph-11][CLAIM-memgraph-15].
- Text-index snapshots are per search and do not see uncommitted changes in the same transaction [CLAIM-memgraph-22]. The vector index is READ_UNCOMMITTED [CLAIM-memgraph-21]. Indexes therefore have **weaker isolation than the graph**, which matters for permission-aware retrieval (J5).

### 5.6 Partitioning and consistency
No partitioning. One MAIN accepts writes and REPLICAs serve reads. Replication ships deltas, WAL segments or snapshots depending on how far a replica lags [CLAIM-memgraph-17].
- **SYNC**: the MAIN commits, then waits for replica acknowledgement. Since v3.13, a SYNC failure no longer rolls back everywhere and surfaces `SyncReplicationFailure` instead.
- **STRICT_SYNC**: two-phase commit; the vendor describes it as CP.
- **ASYNC**: available, but can lose data on failover.

HA (Enterprise) adds an odd number of coordinators running Raft through eBay **NuRaft** (`src/coordination/raft_state.cpp`); the leader coordinator promotes a replica on MAIN failure [CLAIM-memgraph-18]. Multi-tenant replication is Enterprise [CLAIM-memgraph-17].

### 5.7 Caching
The whole graph is resident, so there is no buffer pool in in-memory modes. Query-plan caching exists (*hypothesis*; not verified in the pages read). Vector memory is reported separately and is not freed on vertex delete until the index is dropped [CLAIM-memgraph-21].

### 5.8 Versioning
There is no user-visible history, no time travel and no branching. Deltas are garbage-collected after the oldest active transaction. Snapshots and WAL support recovery only [CLAIM-memgraph-16]. EOIP's application-layer revisions (BL-37/BL-38) stay necessary.

### 5.9 Security
- **Community.** Users/passwords and TLS. The default `memgraph` database is the admin database. Fine-grained controls, SSO, audit and metrics are Enterprise [CLAIM-memgraph-07].
- **Access-control model.** Authentication data is global across databases, with **no per-database privileges**: a user holds the same privileges in every database they can reach [CLAIM-memgraph-19]. Renaming or dropping a database does not update grants [CLAIM-memgraph-19].
- **Search under fine-grained access.** Vector-search hits that fail access checks are "silently dropped", so top-k can be short. In Community "all matches" are visible [CLAIM-memgraph-21]. Text search honours fine-grained permissions from v3.13 [CLAIM-memgraph-29].
- **MCP server.** The read-only mode **blocks writes by keyword detection** (CREATE, MERGE, DELETE, SET, DROP, REMOVE) and does not run a database-enforced read-only transaction [CLAIM-memgraph-25].

## 6. Functional and non-functional requirements inferred from verified behaviour

- FR-1: Accept Bolt connections from Neo4j drivers and execute an openCypher dialect with built-in weighted/K-shortest path operators [CLAIM-memgraph-23].
- FR-2: Maintain vector (USearch) and full-text (Tantivy) indexes on nodes and edges inside the same transactional store [CLAIM-memgraph-21][CLAIM-memgraph-22].
- FR-3: Host several isolated databases per process with per-database memory caps and suspend/resume to cold storage (Enterprise) [CLAIM-memgraph-19][CLAIM-memgraph-20].
- FR-4: Ingest from Kafka, Redpanda and Pulsar through user transformation modules, and fire triggers before or after commit [CLAIM-memgraph-34].
- FR-5: Expose tools to LLM agents over MCP with schema discovery and read-only default [CLAIM-memgraph-25].
- NFR-1: The whole working set lives in RAM, sized at about 136–252 B per vertex and 88–172 B per edge before properties [CLAIM-memgraph-12].
- NFR-2: Durability through WAL plus snapshots, with checksummed WAL (v3.12+) and fail-closed recovery (v3.13) [CLAIM-memgraph-16].
- NFR-3: RPO and RTO depend on the replication mode (STRICT_SYNC 2PC → zero acknowledged-loss; ASYNC → possible loss) [CLAIM-memgraph-17].
- NFR-4: Write throughput is bounded by a single MAIN; read scale comes from replicas [CLAIM-memgraph-17] (reasoned).

## 7. Performance and resource model

- **Vendor benchmarks.** Memgraph's "benchgraph" compared Memgraph 2.4 against Neo4j 5.1 Community and claimed "up to 120× faster … one quarter of the memory". The post is now marked outdated and was superseded by a revised methodology with identical query counts, for example a single-hop query reported as 3.16× faster with 5.42× lower p99. The current landing page claims "41× lower latency" and "2–5× throughput" [CLAIM-memgraph-28]. All of these are **vendor claims, Unverified**. Methodology changed between versions, and the comparison is against Neo4j Community, which lacks Enterprise's parallel runtime.
- **Third-party report.** A 2026 AIMultiple synthetic test (Neo4j, FalkorDB, Memgraph) reported FalkorDB with higher throughput than Memgraph at 8 threads. It is a third-party report with an undisclosed full configuration in what we read, confidence 0.4 [CLAIM-memgraph-32].
- **Resource model (documented).** RAM ≈ V·(136–252 B) + E·(88–172 B) + properties + indexes, plus vector-index memory (dimension × scalar size × capacity × resize coefficient 2 by default) [CLAIM-memgraph-12][CLAIM-memgraph-21]. *Worked example (reasoned):* 50 M vertices and 200 M edges is about 50e6·204 + 200e6·154 ≈ 41 GB before properties and indexes, so a single 64–128 GB node is the practical ceiling for EOIP-scale tenant pools in one instance.
- **Scaling behaviour.** Reads scale with replicas. Writes do not scale horizontally. Recovery time grows with snapshot size; parallel snapshot creation and recovery exist [CLAIM-memgraph-16].
- **Failure modes.**
  - Out-of-memory: queries are rejected beyond `--memory-limit` or a tenant-profile cap [CLAIM-memgraph-20].
  - Analytical mode loses all un-snapshotted writes on crash [CLAIM-memgraph-11].
  - Snapshots are not checksummed [CLAIM-memgraph-16].
  - Vector memory is not reclaimed on delete [CLAIM-memgraph-21].
  - Renamed databases keep stale grants [CLAIM-memgraph-19].
- **Uncertainty.** We have no independent LDBC SNB audit for Memgraph 3.x (NOT PUBLICLY VERIFIED in this run).

## 8. Strengths and use-case-specific advantages

1. **Pointer-based in-memory adjacency with built-in deep-path operators.** Low-latency k-hop and weighted shortest paths are useful for impact analysis (J1, J9, J10). *Match:* push down bounded traversals to backends that have this; *exceed* by combining with EOIP evidence and ACL filtering [CLAIM-memgraph-13][CLAIM-memgraph-23].
2. **One process holds the graph, vector and full-text indexes, and algorithms.** Hybrid GraphRAG retrieval needs no separate vector database. *Integrate* as an optional backend; EOIP keeps an engine-neutral retrieval contract [CLAIM-memgraph-21][CLAIM-memgraph-22][CLAIM-memgraph-30].
3. **Database-per-tenant with memory caps and cold suspend.** A pragmatic SILO model for multi-tenant SaaS (Enterprise). *Match* in EOIP's isolation registry (BL-20) as a backend-native placement [CLAIM-memgraph-19][CLAIM-memgraph-20].
4. **Tenant-aware MCP server.** OIDC/JWT `tenants` claim intersected with a tenant catalogue routes each session to a database. *Match/exceed* in EOIP MCP (BL-47) with per-fact ACL as well as per-tenant routing [CLAIM-memgraph-25].
5. **Streaming ingest inside the database** (Kafka/Pulsar plus transformation modules, triggers). *Reject* for EOIP's authoritative path, because connectors must never mutate the graph directly. Adopt the checkpoint/offset ideas only [CLAIM-memgraph-34].
6. **Bolt/Cypher compatibility** lowers migration friction from Neo4j. *Integrate* through a Bolt adapter with a dialect profile [CLAIM-memgraph-23].

## 9. Limitations with root causes

**Verified defects or documented limitations**
- The planner ignores vector indexes [CLAIM-memgraph-21].
- Index isolation is weaker than graph isolation (vector READ_UNCOMMITTED, text per-search snapshots) [CLAIM-memgraph-21][CLAIM-memgraph-22].
- On-disk mode is experimental and cannot replicate [CLAIM-memgraph-11].
- Snapshots are not checksummed [CLAIM-memgraph-16].
- The memory-sizing documentation is internally inconsistent [CLAIM-memgraph-12].

**Intentional trade-offs**
- RAM-resident working set.
- Single-writer replication instead of sharding.
- Analytical mode trades ACID for load speed [CLAIM-memgraph-11][CLAIM-memgraph-17].

**Licensing restrictions**
- The BSL Additional Use Grant (2026) limits production use to internal purposes and forbids distribution and DBaaS.
- MAGE moved from Apache-2.0 to BSL.
- Enterprise gates every isolation and security feature a multi-tenant OEM needs: multi-tenancy, RBAC/LBAC/PBAC, SSO, audit, HA, metrics, TTL [CLAIM-memgraph-04][CLAIM-memgraph-06][CLAIM-memgraph-07].
- Features have moved behind Enterprise over time (parallel execution v3.8, `cross_database` v3.13) [CLAIM-memgraph-24][CLAIM-memgraph-33].

**User-reported complaints** — not systematically collected in this run (UNVERIFIED). Cypher dialect gaps are documented by the vendor rather than reported by users [CLAIM-memgraph-23].

**Outdated claims** — "120× faster than Neo4j" is superseded [CLAIM-memgraph-28].

**Root-cause organisation**
- *Algorithmic dead-ends:*
  - No cost model for vector-plus-graph co-planning, so hybrid queries are procedure-ordered by hand (proven: planner does not use vector indices).
  - Supernodes: the inline `small_vector` adjacency means a supernode expansion scans the whole list, with no per-type sub-index (*hypothesis* from `vertex.hpp`; per-type filtering happens during iteration).
- *Operational and hardware overhead:*
  - RAM cost per element, with vector memory not reclaimed.
  - Write throughput capped at one MAIN.
  - Recovery replays snapshot plus WAL at start-up (proven by docs).
- *User and developer friction:*
  - Dialect gaps against Neo4j 5.
  - No per-database privileges.
  - Grants drift on rename.
  - Keyword-based MCP read-only guard.
  - Licence complexity across BSL, MEL, OEM, Lab ULA and Cloud ULA (proven).

## 10. Deployment, licensing, redistribution, and operational viability under EOIP constraints

| Constraint | Memgraph position |
|---|---|
| Air-gap | **Yes technically.** A Docker image or DEB/RPM runs offline. The Enterprise licence is a key string set via `SET DATABASE SETTING` (offline-capable — *hypothesis* that no phone-home is required; not verified) [CLAIM-memgraph-07] |
| No mandatory cloud | Met; Memgraph Cloud is optional [CLAIM-memgraph-10] |
| Backend neutrality | Can be added as one more `GraphStore` backend; Bolt adapter required |
| One-node first | Strong fit: single process, RAM-bound |
| Tenant isolation | Native database-per-tenant **only with Enterprise**. Community gives one usable database for production (v3.11: "only non-default databases still require Memgraph Enterprise") [CLAIM-memgraph-19] |
| Permissions survive everything | Graph-level RBAC/LBAC/PBAC is Enterprise. Vector results under ACLs are silently truncated [CLAIM-memgraph-21]. EOIP must keep its own ACL enforcement (BL-18 gap) regardless |
| **Redistribution / white-label** | **LEGAL-REVIEW TRIGGER (high).** Shipping Memgraph Community inside a white-label product sold to customers is "embed or otherwise distribute the Licensed Work to third parties", which the 2026 grant excludes. It also arguably gives third parties operational access [CLAIM-memgraph-04]. Hosting EOIP as multi-tenant SaaS on Memgraph Community is likewise outside "internal business purposes"; the 2026 text dropped the old "Integrated Solution … software-as-a-service" permission [CLAIM-memgraph-05]. The vendor's own route is the **OEM License** (PDF; terms not reviewed) and the OEM / OEM_COMMUNITY key tiers [CLAIM-memgraph-08][CLAIM-memgraph-09]. Customer-procured Memgraph (the customer licenses Memgraph directly and EOIP connects to it) is a different fact pattern that needs legal confirmation. The "competing work" clause is a further trigger, because EOIP includes graph-store functionality. We record this and give no legal conclusion. |
| Licence change cadence | Each version converts to Apache-2.0 at its Change Date (about 4 years; v3.13.0 → "2030-15-07", a malformed date string in the file, interpreted as 15 July 2030; master shows 2030-09-10) [CLAIM-memgraph-04] |
| MAGE reuse | Archived Apache-2.0 MAGE ≤ v3.7.2 can be studied and reused under Apache-2.0. Current MAGE is BSL [CLAIM-memgraph-06] |
| MCP / toolkit reuse | `memgraph/ai-toolkit` is MIT and safe to study and reuse with attribution [CLAIM-memgraph-25] |
| Lab | Proprietary ULA; not redistributable without agreement [CLAIM-memgraph-09] |

**Operational viability.** Good for a single node. HA requires Enterprise plus 3 coordinators and 2 or more data instances. Multi-tenant backup and suspend/resume are Enterprise [CLAIM-memgraph-18][CLAIM-memgraph-34].

## 11. Competitive delta against the EOIP verified baseline

| Area | Memgraph | EOIP baseline | Delta |
|---|---|---|---|
| Backend abstraction | Single engine | `GraphStore` protocol, 6 adapters (BL-01..BL-06) | EOIP ahead on neutrality; no Memgraph adapter exists. The Neo4j adapter uses HTTP Cypher (BL-03), which Memgraph does not expose (hypothesis) |
| Multi-hop pushdown | Native BFS/WSP/KSP operators [CLAIM-memgraph-23] | Traversal in Python over the protocol (baseline §6.1); bounded templates (BL-08) | Memgraph far ahead on deep-path latency; EOIP needs pushdown profiles |
| Vector / full-text | In-engine USearch and Tantivy [CLAIM-memgraph-21][CLAIM-memgraph-22] | In-process BM25, hashing embedder, pure-Python HNSW, RRF (BL-13..BL-15) | Memgraph ahead on persistence and scale; EOIP ahead on fusion contract and engine neutrality |
| Tenancy | DB-per-tenant + memory caps (Enterprise) [CLAIM-memgraph-19][CLAIM-memgraph-20] | Isolation contract, adapters tenant-unaware (BL-20) | Memgraph ahead in physical isolation, behind a licence gate. EOIP P0 gap |
| Source-ACL in retrieval | LBAC/PBAC (Enterprise), silent truncation | **Absent** (BL-18) | Memgraph partially ahead; neither offers source-ACL-aware ranking with re-fill |
| Temporal / versioning | None user-visible | Bitemporal revisions, diff, playback (BL-37, BL-38) | EOIP ahead |
| Evidence / claims / epistemics | None | BL-39..BL-41 | EOIP ahead |
| Reasoning / SHACL | None | In-house subsets (BL-29, BL-30) | EOIP ahead (subset) |
| Algorithms | MAGE C++ library, dynamic algorithms (Ent.) [CLAIM-memgraph-30] | Pure-Python algorithms (BL-43) | Memgraph far ahead on scale |
| MCP | 7 tools, read-only by keyword, JWT tenant routing [CLAIM-memgraph-25] | 18 read-oriented tools incl. `query(plan)` (BL-47) | EOIP ahead on typed plans; Memgraph ahead on OIDC tenant routing |
| Streaming ingest | In-DB Kafka/Pulsar [CLAIM-memgraph-34] | SourceEvent log, replay, DLQ (BL-23, BL-24); no external bus (BL-60) | Different philosophies; EOIP's governed path is a requirement |
| Licensing for OEM | BSL restricts distribution [CLAIM-memgraph-04] | Offline signed licences (BL-22) | EOIP must not depend on Memgraph Community in shipped bundles |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

### Strength-adoption cards

| STR-ID | Competitor | Strength | Evidence | Value to EOIP customers | Match / exceed / integrate / reject | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-memgraph-01 | Memgraph | Built-in deep-path operators (BFS, weighted SP, K-shortest) executed in-engine | CLAIM-memgraph-23, -13 | Fast blast-radius and change-impact answers (J1, J9, J10) | Match (pushdown) / exceed (evidence + ACL) | Add a `PathQuery` IR node to QueryPlan v1 with per-backend compilers (Memgraph `*WSHORTEST`, Neo4j `SHORTEST`, Gremlin `repeat().until()`, emulated fallback) | On a 10 M-edge synthetic digital thread, 6-hop impact query p95 is at least 5× lower with pushdown than with Python traversal, with identical result sets |
| STR-memgraph-02 | Memgraph | Graph + vector + full-text in one transactional engine | CLAIM-memgraph-21, -22 | Simpler one-node GraphRAG deployments | Integrate (optional backend) | `RetrievalBackend` capability flags: if `native_vector` then push kNN, else use EOIP's vector store; fusion stays in EOIP (BL-15) | Hybrid retrieval nDCG@10 is within 2 points of EOIP's external-index path on the same corpus, with fewer containers |
| STR-memgraph-03 | Memgraph | Database-per-tenant with per-DB memory caps and cold suspend | CLAIM-memgraph-19, -20 | Noisy-neighbour control and cheap idle tenants | Match (backend-native placement in isolation registry) | Extend `tenancy/isolation.py` placement with `SILO_DB` per backend (Memgraph DB, Neo4j DB, HugeGraph graph space) + quota adapters | J13 leakage suite passes; a tenant over its quota is rejected without affecting the p95 of another tenant |
| STR-memgraph-04 | Memgraph | MCP server with OIDC/JWT tenant-claim routing | CLAIM-memgraph-25 | Agents can be safely exposed per tenant | Match / exceed | EOIP MCP validates the JWT, derives tenant plus principal, and enforces per-fact source ACLs (BL-18) as well as per-tenant routing | A token for tenant A cannot list or query tenant B. An agent with a revoked ACL gets no hit from a previously visible document |
| STR-memgraph-05 | Memgraph | `SHOW SCHEMA INFO` / enum schema tools that ground LLM text-to-Cypher | CLAIM-memgraph-25 | Better NL→query accuracy (J11) | Match | Expose an ontology-derived schema digest to the suggestion engine (BL-11/BL-12) per backend dialect | Text-to-query exact-match accuracy improves on a 200-question set when the schema digest is included |

### Inversion cards

**INV-memgraph-01 — Licence gate on redistribution and tenancy**
- *Target / version / workload:* Memgraph v3.8.0+ Community (BSL as amended 2026-01-01); white-label on-prem and SaaS distribution.
- *Limitation:* production use is limited to internal purposes, with no distribution, no DBaaS and no competing work. Multi-tenancy, RBAC/LBAC/PBAC, SSO, audit and HA are Enterprise-only [CLAIM-memgraph-04][CLAIM-memgraph-07].
- *Root cause:* licensing (proven).
- *Why an alternative mitigates it:* an engine-neutral platform can ship with a permissively licensed default backend (HugeGraph, Apache-2.0 — verify in W01) and treat Memgraph as customer-licensed. This would be worse if a customer needs Memgraph-class in-memory latency and refuses to buy a Memgraph licence.
- *Options:* (1) Quick: document Memgraph as a "bring-your-own-licence" backend, never bundled. (2) Pragmatic: a Bolt adapter plus a licence-aware deployment manifest that refuses to bundle BSL components in white-label builds (SBOM gate). (3) Long-term: negotiate an OEM agreement only if customer demand is proven.
- *Selected:* (1) and (2). Pattern: a licence-policy gate in the build.

```
deploy/profiles/*.yaml:  backends: [hugegraph(bundled), neo4j(customer|bundled-community?), memgraph(customer-only)]
ci/licence_gate.py: fail if image contains component with licence_class in {BSL, SSPL} and profile.distribution == "white-label"
```

- *Falsifiable POC:* build all white-label profiles. The SBOM (Syft) shows no BSL or SSPL artefacts, and the Memgraph adapter passes conformance against a customer-supplied instance. Success means 0 violations and a green conformance run. Cost is about 3 engineer-days.
- *Dependencies / failure cases:* the risk is a licence misclassification in the SBOM. The mitigation is a manual legal list for engines.
- *Defensibility:* the customer value (a freely redistributable, air-gapped white-label bundle) persists because competitors that rely on BSL engines cannot copy it without OEM fees.
- *Decision:* **ADOPT**.

**INV-memgraph-02 — Indexes weaker than the graph: silent ACL truncation and READ_UNCOMMITTED vectors**
- *Target:* Memgraph v3.13 vector and text search with fine-grained access control; workload is permission-aware GraphRAG (J5).
- *Limitation:* vector results the user cannot see are "silently dropped", so top-k can be short. The vector index is READ_UNCOMMITTED. Text search uses per-search snapshots and misses same-transaction changes [CLAIM-memgraph-21][CLAIM-memgraph-22].
- *Root cause:* storage/coupling. The index is outside MVCC and the ACL is a post-filter (proven by docs).
- *Alternative:* ACL-aware retrieval in EOIP that over-fetches and re-fills, or partitions indexes by ACL group. It would be worse when the ACL cardinality is huge (one index per principal is infeasible).
- *Options:* (1) Quick: over-fetch k·f and post-filter in EOIP with a loop until k hits or a budget is reached. (2) Pragmatic: an `acl_hash` filter pushed into backends that support filtered kNN, with an EOIP fallback. (3) Long-term: an ACL-bucketed index layout plus revocation-driven invalidation (J5).
- *Selected:* (1) now, then (2). Pseudocode:

```
def acl_knn(q, k, principal, f=4, budget=5):
    got, offset = [], 0
    for _ in range(budget):
        cand = backend.knn(q, k*f, offset); offset += k*f
        got += [c for c in cand if acl.allows(principal, c.acl_hash)]
        if len(got) >= k: return got[:k]
    return got  # flagged INCOMPLETE with evidence-gap reason
```

- *POC:* on a 1 M-chunk corpus with 50 ACL groups, recall@10 against brute-force ACL-filtered ground truth is at least 0.95, and p95 is at most 2× unfiltered.
- *Security failure cases:* leakage through counts or timing; stale `acl_hash` after revocation.
- *Defensibility:* correctness under revocation is hard to retrofit into engines.
- *Decision:* **ADOPT** (option 1), **EXPERIMENT** (option 2).

**INV-memgraph-03 — No sharding; RAM-bound single writer**
- *Target:* Memgraph 3.x; workload is graphs larger than RAM or with heavy concurrent writes.
- *Limitation:* one MAIN, replicas for reads, on-disk mode experimental without HA [CLAIM-memgraph-11][CLAIM-memgraph-17].
- *Root cause:* storage and deployment design (proven by docs).
- *Alternative:* EOIP's one-node-first stance accepts this. For scale-out it prefers tenant-level partitioning (tenant per instance) over graph sharding. That is worse for a single huge tenant graph.
- *Options:* (1) Tenant-to-instance placement map. (2) Hot/cold tiering: hot subgraph in an in-memory engine, full history in HugeGraph/RocksDB. (3) Federated query over shards in EOIP (CAP-21).
- *Selected:* (1). (2) is EXPERIMENT.
- *POC:* place 20 tenants across 3 instances and rebalance one tenant with no cross-tenant downtime. Measure RTO.
- *Decision:* **EXPERIMENT**.

**INV-memgraph-04 — MCP read-only by keyword blocking**
- *Target:* mcp-memgraph (`MCP_READ_ONLY=true`).
- *Limitation:* writes are blocked by detecting CREATE/MERGE/DELETE/SET/DROP/REMOVE keywords [CLAIM-memgraph-25]. Write-capable procedures (`CALL` modules) and obfuscation are not covered by the documented rule.
- *Root cause:* governance/UX. The guard sits outside the database (proven by README; bypass is a *hypothesis*, not tested).
- *Alternative:* EOIP's typed `QueryPlan` (BL-08) with named bounded templates, plus database-side read-only roles where the backend supports them. It would be worse for exploratory power users.
- *Options:* (1) Keep typed plans only. (2) Add a "raw read" tool that opens a backend read-only transaction or user. (3) A static analyser on the parsed AST that allow-lists read operators and procedures.
- *Selected:* (1) + (3).
- *POC:* a red-team set of 100 write-attempt prompts (including `CALL` write procedures, case and comment tricks) gives 0 mutations.
- *Decision:* **ADOPT**.

**Seed hypotheses (Master Prompt §10.5).** No seed targets Memgraph directly. The Neo4j seed ("weak formal semantics, no native reasoning, schema-optional decay") is **validated as applicable to Memgraph**: there is no reasoning or SHACL layer, and only node-label constraints [CLAIM-memgraph-23]. The proposed inverted design (constraints enforced in EOIP's mutation gateway, portable across backends) applies unchanged. The "fixed vendor query languages → typed plans + adapters" direction is validated by the documented dialect gaps.

## 13. Per-capability decisions

| Capability | Decision | Rationale |
|---|---|---|
| Memgraph as an optional customer-licensed backend (CAP-01, CAP-14) | INTEGRATE (P2) | Bolt adapter + dialect profile; never bundled (INV-memgraph-01) |
| Deep-path pushdown IR (CAP-19, CAP-20) | BUILD (P1) | STR-memgraph-01; benefits every backend |
| In-engine vector/text as an optional retrieval backend (CAP-53, CAP-54, CAP-55) | EXPERIMENT (P2) | STR-memgraph-02; keep fusion and ACL in EOIP |
| DB-per-tenant placement (CAP-47) | BUILD (P0 contract, backend-specific realisation) | STR-memgraph-03; tenant isolation is P0 |
| ACL-aware retrieval with re-fill (CAP-46) | BUILD (P0) | INV-memgraph-02, BL-18 |
| MCP OIDC tenant routing (CAP-59, CAP-44) | BUILD (P1) | STR-memgraph-04 |
| MAGE algorithms (CAP-62) | REUSE patterns only from archived Apache-2.0 MAGE ≤ v3.7.2; REJECT bundling current BSL MAGE | Licence |
| In-DB streaming ingest (CAP-26) | REJECT for authoritative path | Connectors must not mutate the graph |
| Licence gate in build (CAP-77, CAP-79) | BUILD (P1) | INV-memgraph-01 |
| Memgraph Lab (CAP-71) | REJECT (reference only) | Proprietary ULA |
| Dynamic/incremental algorithms (CAP-62, CAP-65) | DEFER | Enterprise-only; revisit with W33 findings |

## 14. Concrete tests, proof-of-concept, and acceptance conditions (all PROPOSED)

1. **POC-MG-1 Bolt adapter conformance.** Run `graph/conformance.py` against Memgraph v3.13.2 Community in Docker (single default DB). Accept when all protocol operations pass, and log dialect gaps such as named constraints and `DROP CONSTRAINT`.
2. **POC-MG-2 Path pushdown.** Generate a synthetic digital-thread graph (1 M vertices, 10 M edges, power-law degree). Run 6-hop and weighted shortest-path impact queries. Accept when results equal the Python baseline and p95 is at least 5× faster. Record RAM against the documented formula (±25%).
3. **POC-MG-3 ACL-filtered kNN.** Use 1 M chunks with 384-d f32 vectors and 50 ACL groups. Accept when recall@10 ≥ 0.95 against brute force and nothing leaks after revocation within 1 index-refresh cycle.
4. **POC-MG-4 Tenancy (Enterprise trial, licence permitting).** Use 10 databases with tenant profiles. Accept when the J13 suite gives 0 leaks and over-quota rejection is isolated.
5. **POC-MG-5 MCP red team.** Run 100 write-attempt prompts against mcp-memgraph (read-only) and against the EOIP MCP. Accept when EOIP shows 0 mutations, and record mcp-memgraph results as evidence.
6. **LIC-MG-1 Licence gate.** Accept when the white-label SBOM contains 0 BSL/SSPL items.

## 15. Risks, trade-offs, and open research questions

- **R1 Licence drift.** Memgraph tightened its grant in 2026 and moved features to Enterprise. Further change is plausible, so re-verify at each upgrade [CLAIM-memgraph-04][CLAIM-memgraph-33].
- **R2 Dialect drift.** Cypher gaps narrow with each release (`COUNT{}` in 3.13). Dialect profiles must be versioned.
- **R3 Index isolation.** Retrieval correctness under concurrent writes is weaker than graph correctness.
- **Open questions.**
  - Q1: OEM licence terms and pricing (PDF not reviewed).
  - Q2: Does the Enterprise key validate offline? (UNVERIFIED)
  - Q3: Is an HTTP Cypher endpoint available? (none documented in the pages read)
  - Q4: APOC-equivalence coverage of MAGE.
  - Q5: Independent LDBC results for 3.x.
  - Q6: Does a customer-procured Memgraph licence plus an EOIP connector avoid the "competing work" clause? (legal)

## Appendix A. Research-dimension coverage

| Dimension | Covered in section(s) | Summary or N/A reason |
|---|---|---|
| D1 Identity and maturity | 1, 10 | Active, monthly cadence, BSL+MEL, MAGE merged into the repo under BSL |
| D2 Problem and workloads | 2 | Real-time graph, GraphRAG, agent memory |
| D3 Architecture decomposition | 4 | Single process, DBMS handler, Raft coordinators |
| D4 Storage primitives and indexing | 5.2 | SkipList objects, inline pointer adjacency, deltas, Tantivy, USearch, RocksDB on-disk |
| D5 Schema and semantic expressivity | 5.1 | Optional schema, node-only constraints, no hyperedges |
| D6 Query pipeline and optimisation | 5.3 | ANTLR → rule-based + cardinality cost; dialect gaps |
| D7 Reasoning and inference | 5.4 | None; triggers only |
| D8 Transactions, concurrency, scale | 5.5, 5.6, 7 | Delta MVCC, SI default, single MAIN, NuRaft HA |
| D9 Ingestion and federation | 3, 8 | Kafka/Pulsar streams, triggers; no federation |
| D10 Identity and evidence | 11 | N/A natively, no ER or provenance features; EOIP ahead |
| D11 Time and evolution | 5.8 | No user-visible history |
| D12 Graph algorithms and ML | 3, 8 | MAGE, dynamic algorithms (Ent.) |
| D13 Retrieval and agent integration | 3, 8, 12 | Vector, text, MCP, LangChain/LlamaIndex |
| D14 NL querying | 12 (STR-05) | Schema-info tools; text-to-Cypher via LangChain toolkit; no accuracy data |
| D15 Governance and authoring | 11 | N/A natively, no ontology governance |
| D16 Human experience | 3 | Memgraph Lab (proprietary) |
| D17 Developer experience | 3, 5.3 | Bolt drivers, query modules in C++/Python/Rust |
| D18 Trust and security | 5.9, 12 | Enterprise RBAC/LBAC/PBAC, keyword MCP guard |
| D19 Multi-tenancy and white-label | 3, 10, 12 | DB-per-tenant (Ent.), tenant profiles, shared auth, OEM licence |
| D20 Empirical economics | 7 | RAM formula, vendor benchmarks only |
| D21 Commercial and licensing | 1, 10 | Memory-based pricing, OEM licence, BSL 2026 grant |
| D22 Interoperability and lock-in | 5.3, 11 | Bolt/Cypher; dialect gaps; no RDF |
| D23 IP and prior art | 15 | No patents searched (NOT PUBLICLY VERIFIED). BSL "competing work" clause is a FTO-style trigger |
| D24 Research quality | 7, App. C | Strong docs and source; benchmarks vendor-run |

## Appendix B. Capability mapping

| CAP-ID | This technology | Evidence CLAIM-ID | EOIP baseline (BL-ID + status) | Decision for EOIP | Priority |
|---|---|---|---|---|---|
| CAP-01 | native | CLAIM-memgraph-13 | BL-01 Implemented | INTEGRATE (optional backend) | P2 |
| CAP-04 | native | CLAIM-memgraph-12 | BL-01 Implemented | INTEGRATE | P2 |
| CAP-05 | partial (replication, no sharding; HA Ent.) | CLAIM-memgraph-17, -18 | Absent | DEFER | P3 |
| CAP-07 | unknown / hypothesis weak | CLAIM-memgraph-13 | Unknown | EXPERIMENT | P3 |
| CAP-08 | partial (node constraints) | CLAIM-memgraph-23 | BL-28 Implemented | BUILD in gateway | P1 |
| CAP-14 | native (dialect) | CLAIM-memgraph-23 | BL-03 Implemented | INTEGRATE via profile | P2 |
| CAP-18 | partial (cardinality cost, EXPLAIN/PROFILE) | CLAIM-memgraph-24 | BL-08 Implemented | REUSE upstream | P3 |
| CAP-19 | native | CLAIM-memgraph-23 | BL-08 Implemented (emulated) | BUILD pushdown IR | P1 |
| CAP-20 | absent | CLAIM-memgraph-23 | BL-09 Partial | BUILD | P1 |
| CAP-26 | native (streams) | CLAIM-memgraph-34 | BL-23 Implemented | REJECT for authoritative path | — |
| CAP-34 / CAP-36 | absent | CLAIM-memgraph-16 | BL-37 Implemented | keep EOIP | — |
| CAP-45 | enterprise-only | CLAIM-memgraph-07 | BL-19 Implemented | keep EOIP | P1 |
| CAP-46 | enterprise-only, truncating | CLAIM-memgraph-21 | BL-18 Absent | BUILD | P0 |
| CAP-47 | enterprise-only | CLAIM-memgraph-19, -20 | BL-20 Partial | BUILD | P0 |
| CAP-48 | enterprise-only (audit log) | CLAIM-memgraph-07 | Partial | keep EOIP | P1 |
| CAP-52 | absent (BSL forbids distribution) | CLAIM-memgraph-04 | BL-21 Implemented | REJECT bundling | P1 |
| CAP-53 | native | CLAIM-memgraph-21 | BL-14 Partial | EXPERIMENT | P2 |
| CAP-54 | native | CLAIM-memgraph-22 | BL-13 Implemented | EXPERIMENT | P2 |
| CAP-56 | partial (positioning + integrations) | CLAIM-memgraph-27, -26 | BL-16 Implemented | reference | P3 |
| CAP-59 | native (MIT server) | CLAIM-memgraph-25 | BL-47 Implemented | BUILD tenant routing | P1 |
| CAP-62 | native (MAGE, BSL) | CLAIM-memgraph-30, -06 | BL-43 Implemented | REUSE archived Apache-2.0 patterns | P2 |
| CAP-74 | native (snapshots, S3) | CLAIM-memgraph-16, -34 | BL-50 Implemented | INTEGRATE in adapter ops | P3 |
| CAP-76 | enterprise-only | CLAIM-memgraph-18 | Partial | DEFER | P3 |
| CAP-77 | BSL/MEL/OEM | CLAIM-memgraph-04, -10 | BL-22 Implemented | BUILD licence gate | P1 |

## Appendix C. Evidence records

All access dates are 2026-10-18.

| CLAIM-ID | Product / version / date | Exact claim | Classification | Source title + URL | Publication / access | Confidence + rationale | Contradictory evidence |
|---|---|---|---|---|---|---|---|
| CLAIM-memgraph-01 | Memgraph repo, 2026-10-16 | Repo active, not archived; description "High-performance open-source in-memory graph database for GraphRAG, AI memory, agentic AI…" | Officially documented | GitHub API repos/memgraph/memgraph — https://github.com/memgraph/memgraph | live / 2026-10-18 | 0.9 primary metadata | "open-source" wording conflicts with BSL text (CLAIM-04) |
| CLAIM-memgraph-02 | v3.8.0–v3.13.2 | Release dates (v3.13.2 2026-10-09; v3.13.0 2026-09-09; v3.12.0 2026-07-15; v3.11.0 2026-06-17; v3.10.0 2026-05-13; v3.8.0 2026-02-11); v3.12 SUSPEND/RESUME, PBAC; v3.13 global property indexes, COUNT{}/COLLECT{} | Officially documented | Memgraph release notes — https://memgraph.com/docs/release-notes ; GitHub releases | 2026 / 2026-10-18 | 0.9 | v3.9.0 heading lacked date (Lab v3.9.0 2026-03-18) |
| CLAIM-memgraph-03 | master | "variously licensed under the Business Source License 1.1 (BSL), the Memgraph Enterprise License (MEL)" | Observed in source code | LICENSE — https://github.com/memgraph/memgraph/blob/master/LICENSE | / 2026-10-18 | 0.95 | none |
| CLAIM-memgraph-04 | v3.8.0–v3.13.2, master | BSL "as amended by the Additional Use Grant", 2026-01-01: production use solely for internal business purposes; no embedding/distribution to third parties; no DBaaS; no competing work; Change Licence Apache-2.0; per-version Change Date (v3.13.0 "2030-15-07", master "2030-09-10") | Observed in source code | licenses/BSL.txt at tags — https://github.com/memgraph/memgraph/blob/v3.13.2/licenses/BSL.txt | 2026-01-01 / 2026-10-18 | 0.95 verbatim text; malformed date strings noted | pricing page calls Community "open source" |
| CLAIM-memgraph-05 | ≤ v3.7.2 | Previous grant permitted internal use, "Integrated Solution" adding primary functionality, and hosting the Integrated Solution as SaaS; still no embedding/distribution | Observed in source code | licenses/BSL.txt @ v3.7.2 — https://github.com/memgraph/memgraph/blob/v3.7.2/licenses/BSL.txt | 2025 / 2026-10-18 | 0.95 | none |
| CLAIM-memgraph-06 | MAGE, 2025-11-07 / v3.8.0 | MAGE and mgcxx merged into memgraph repo; old repos archived under existing licence (Apache-2.0); "merged code will be released under the existing Memgraph Community BSL license" | Officially documented | memgraph/mage README — https://github.com/memgraph/mage ; release notes v3.8.0 | 2025-11-07 / 2026-10-18 | 0.9 | none |
| CLAIM-memgraph-07 | docs, current | Enterprise-only: RBAC, LBAC, PBAC, multi-role/multi-tenant roles, LDAP/SAML/OIDC, impersonation, audit log, Prometheus metrics, HA auto failover, multi-tenancy, tenant profiles, CRON snapshots, dynamic algorithms, TTL, parallel execution, user profiles, Lab SSO/monitoring/sharing | Officially documented | Enabling Memgraph Enterprise — https://memgraph.com/docs/database-management/enabling-memgraph-enterprise | / 2026-10-18 | 0.85 | — |
| CLAIM-memgraph-08 | v3.10–v3.11 | Licence types enterprise, ai_platform (memory limit on graph only), oem; v3.11 splits OEM into OEM and OEM_COMMUNITY | Officially documented | Release notes; Enabling Enterprise page | 2026 / 2026-10-18 | 0.8 | OEM_COMMUNITY not on Enterprise page |
| CLAIM-memgraph-09 | legal, current | Embedding Memgraph in a product distributed to end customers requires the Memgraph OEM License; separate Lab ULA and Cloud ULA | Officially documented | Memgraph Legal — https://memgraph.com/legal | / 2026-10-18 | 0.8 (OEM PDF not read) | — |
| CLAIM-memgraph-10 | pricing, current | Pricing scales with memory capacity; Community "open source and free"; Enterprise AI Platform vs Graph Analytics; OEM/SaaS by contract; Memgraph Cloud on AWS | Officially documented | Memgraph Pricing — https://memgraph.com/pricing | / 2026-10-18 | 0.75 (marketing page) | BSL says "not an open source license" |
| CLAIM-memgraph-11 | docs, current | Three storage modes; ANALYTICAL no WAL, "up to 6 times faster import"; ON_DISK uses RocksDB, "still in the experimental phase", SI only, no replication/HA | Officially documented | Storage memory usage — https://memgraph.com/docs/fundamentals/storage-memory-usage | / 2026-10-18 | 0.85; 6× is vendor figure | — |
| CLAIM-memgraph-12 | docs, current | Vertex min 136 B, edge min 88 B; formula V×204 B + E×154 B; worked example 252 B/172 B; light edges save ~24 B; zlib property compression default off | Officially documented | same page | / 2026-10-18 | 0.75 internal inconsistency | formula vs example mismatch |
| CLAIM-memgraph-13 | v3.13.2 | `struct Vertex` with labels, in/out edge small_vectors of (EdgeTypeId, Vertex*, EdgeRef), PropertyStore, RWSpinLock, Delta pointer; sizeof 80 | Observed in source code | src/storage/v2/vertex.hpp @ v3.13.2 — https://github.com/memgraph/memgraph/blob/v3.13.2/src/storage/v2/vertex.hpp | / 2026-10-18 | 0.95 | — |
| CLAIM-memgraph-14 | v3.13.2 | Delta actions (DELETE_OBJECT, RECREATE_OBJECT, ADD/REMOVE_LABEL, edge add/remove), CommitInfo atomic timestamp, command_id | Observed in source code | src/storage/v2/delta.hpp @ v3.13.2 | / 2026-10-18 | 0.85 (partial read) | — |
| CLAIM-memgraph-15 | docs, current | SNAPSHOT_ISOLATION default, READ_COMMITTED, READ_UNCOMMITTED; commit-time conflict → rollback; ANALYTICAL "no isolation levels and no ACID guarantees" | Officially documented | Transactions — https://memgraph.com/docs/fundamentals/transactions | / 2026-10-18 | 0.85 | — |
| CLAIM-memgraph-16 | docs, current | WAL + snapshots; CRC32 WAL (v3.12); fail-closed corrupted WAL (v3.13); snapshots not checksummed; CRON intervals Enterprise; retention 3 | Officially documented | Data durability — https://memgraph.com/docs/fundamentals/data-durability | / 2026-10-18 | 0.85 | — |
| CLAIM-memgraph-17 | docs, current | Replication in Community with manual failover; SYNC, ASYNC, STRICT_SYNC (2PC); deltas/WAL/snapshots; multi-tenant replication Enterprise; SYNC failure semantics changed in 3.13 | Officially documented | Replication; How replication works — https://memgraph.com/docs/clustering/replication | / 2026-10-18 | 0.85 | — |
| CLAIM-memgraph-18 | docs, current | HA Enterprise; coordinators use Raft via NuRaft; odd number, 3 typical; automatic failover; Helm ISSU | Officially documented | How high availability works — https://memgraph.com/docs/clustering/high-availability | / 2026-10-18 | 0.85 | — |
| CLAIM-memgraph-19 | docs, current | Multi-tenancy Enterprise; per-DB data directory; shared CPU and config; no cross-DB queries; auth shared, no per-database privileges; rename/drop doesn't update grants; v3.11 "only non-default databases still require Memgraph Enterprise" | Officially documented | Multi-tenancy — https://memgraph.com/docs/database-management/multi-tenancy ; release notes v3.11 | / 2026-10-18 | 0.85 | — |
| CLAIM-memgraph-20 | docs, current | Tenant profiles (Enterprise) cap total memory per DB; `memory_limit` only key; queries over cap rejected | Officially documented | Tenant profiles — https://memgraph.com/docs/database-management/tenant-profiles | / 2026-10-18 | 0.9 | — |
| CLAIM-memgraph-21 | docs, current | Vector index backend USearch; metrics and scalar kinds; node + edge indexes; READ_UNCOMMITTED for vector indices; planner does not use vector indices; ACL-failing results "silently dropped"; Community sees all matches; vector memory not freed until drop | Officially documented | Vector search — https://memgraph.com/docs/querying/vector-search | / 2026-10-18 | 0.85 | — |
| CLAIM-memgraph-22 | docs, current | Text search on Tantivy, GA since 3.6; node/edge indexes; fuzzy, regex; uncommitted changes invisible; per-search snapshot | Officially documented | Text search — https://memgraph.com/docs/querying/text-search | / 2026-10-18 | 0.85 | — |
| CLAIM-memgraph-23 | docs, current | Documented Cypher differences (list in §5.3), built-in BFS/DFS/WSP/ASP/KSP, node-only constraints, no named constraints | Officially documented | Differences in Cypher implementations — https://memgraph.com/docs/querying/differences-in-cypher-implementations | / 2026-10-18 | 0.85 | — |
| CLAIM-memgraph-24 | docs + v3.13.2 + v3.8 notes | Plan operators incl. HashJoin, ScanAllByPointDistance; cardinality-based cost estimator; parallel execution Enterprise (v3.8) | Officially documented / Observed in source code | Query plan — https://memgraph.com/docs/querying/query-plan ; src/query/plan/cost_estimator.hpp @ v3.13.2 | / 2026-10-18 | 0.8 | — |
| CLAIM-memgraph-25 | ai-toolkit main | mcp-memgraph (MIT, 2026): 7 tools (run_cypher_query, search_schema, get_node_schema, get_relationship_schema, get_enum_schema, list_databases, use_database); read-only default blocks CREATE/MERGE/DELETE/SET/DROP/REMOVE; optional OIDC/JWT tenants-claim routing; streamable HTTP or stdio | Officially documented | MCP docs — https://memgraph.com/docs/ai-ecosystem/mcp ; README — https://github.com/memgraph/ai-toolkit/tree/main/integrations/mcp-memgraph | 2026 / 2026-10-18 | 0.85 | — |
| CLAIM-memgraph-26 | docs, current | Integrations: LlamaIndex, LangChain (langchain-memgraph, toolkit), Cognee, Mem0, LightRAG | Officially documented | Integrations — https://memgraph.com/docs/ai-ecosystem/integrations | / 2026-10-18 | 0.85 | — |
| CLAIM-memgraph-27 | docs, current | GraphRAG positioning: in-memory performance, algorithms (deep path, community detection, PageRank), vector search | Officially documented | GraphRAG with Memgraph — https://memgraph.com/docs/ai-ecosystem/graph-rag | / 2026-10-18 | 0.7 marketing | — |
| CLAIM-memgraph-28 | benchgraph 2022–2026 | "up to 120× faster than Neo4j … quarter of the memory" (Memgraph 2.4 vs Neo4j 5.1 Community, outdated); revised: 3.16× faster single-hop, 5.42× lower p99; landing page "41×" latency, "2–5×" throughput | Unverified (vendor claim) | Memgraph blog — https://memgraph.com/blog/memgraph-vs-neo4j-performance-benchmark-comparison ; https://memgraph.com/benchmark | 2022–2026 / 2026-10-18 | 0.25 vendor-run, methodology changed | AIMultiple (CLAIM-32) |
| CLAIM-memgraph-29 | v3.12–v3.13 | Property-based access control (v3.12); text search respects fine-grained permissions (v3.13) | Officially documented | Release notes | 2026 / 2026-10-18 | 0.85 | — |
| CLAIM-memgraph-30 | docs, current | MAGE query modules in repo `src/mage`; built-in deep path algorithms; dynamic graph algorithms Enterprise | Officially documented | Advanced algorithms — https://memgraph.com/docs/advanced-algorithms | / 2026-10-18 | 0.85 | — |
| CLAIM-memgraph-31 | v3.13.1, 2026-09-14 | Experimental Enterprise-only FIPS 140-3 support | Officially documented | Release notes | 2026-09-14 / 2026-10-18 | 0.85 | — |
| CLAIM-memgraph-32 | 2026 | Third-party synthetic benchmark: FalkorDB higher throughput than Neo4j and Memgraph at 8 threads | Third-party report | AIMultiple graph databases — https://aimultiple.com/graph-databases | 2026 / 2026-10-18 | 0.4 config not fully reviewed | vendor benchgraph |
| CLAIM-memgraph-33 | v3.13.0 | `cross_database` module now requires Enterprise (breaking change); metrics default OpenMetrics | Officially documented | Release notes v3.13.0 | 2026-09-09 / 2026-10-18 | 0.85 | Enterprise page did not mark it |
| CLAIM-memgraph-34 | docs, current | Kafka/Redpanda/Pulsar streams with transformation modules; triggers BEFORE/AFTER COMMIT; S3 snapshot recovery; multi-tenant backup Enterprise | Officially documented | Data streams — https://memgraph.com/docs/data-streams ; Triggers — https://memgraph.com/docs/fundamentals/triggers ; Backup and restore — https://memgraph.com/docs/database-management/backup-and-restore | / 2026-10-18 | 0.85 | — |

## Appendix D. Assumptions

- A1. "Memgraph (with MAGE)" means the current single-repository product (v3.13.x) including MAGE. The archived Apache-2.0 MAGE is treated as a separate, frozen artefact.
- A2. The Community features absent from the Enterprise list are assumed to be Community (users, TLS, replication, vector, text). This matches the pricing page.
- A3. We assumed Memgraph exposes no Neo4j-compatible HTTP transactional endpoint, because none appears in the documentation pages read. To be verified in POC-MG-1.
- A4. The malformed Change Date strings ("2030-15-07") are read as day-month (15 July 2030). The licence text, not our reading, governs.
- A5. The licensing analysis is fact-recording only. No legal conclusion is given, and every redistribution path is a legal-review trigger.
- A6. Performance numbers are vendor or third-party figures. No benchmark was executed in this programme.
