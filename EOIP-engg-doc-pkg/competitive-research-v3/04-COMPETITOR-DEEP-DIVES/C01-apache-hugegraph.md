| Field | Value |
|---|---|
| Registry ID | T-C01-apache-hugegraph |
| Tier | A (current reference backend; deep baseline study required by Master Prompt §6 and §5.4) |
| Versions examined | apache/hugegraph 1.7.0 (tag commit b12425c, GitHub release 2025-11-16); hugegraph-toolchain 1.7.0 (1643f2b); hugegraph-computer 1.7.0 (6dae7d2, includes Vermeer); hugegraph-ai 1.7.0 (101f10f). master HEADs checked for drift: hugegraph 90790e8 (2026-10-18, revision 1.8.0, unreleased), toolchain 09f9aa1, ai 84ee9c4, computer 413f95f |
| Verified on | 2026-10-18 |
| Worker | W01 |

Source paths below are relative to the repo named, at tag `1.7.0`, unless they say master. `core/` = `hugegraph-server/hugegraph-core/src/main/java/org/apache/hugegraph/`, `api/` = `hugegraph-server/hugegraph-api/src/main/java/org/apache/hugegraph/`.

## 1. Identity, current status, tier, and sources

| Item | Verified value |
|---|---|
| Project | Apache HugeGraph, https://hugegraph.apache.org, repos `apache/hugegraph`, `apache/hugegraph-toolchain`, `apache/hugegraph-computer`, `apache/hugegraph-ai`, `apache/hugegraph-doc` |
| Governance | **ASF top-level project.** Entered the Incubator 2022-01-23 and graduated 2026-01-21; the ASF announced it 2026-02-12 [CLAIM-apache-hugegraph-02]. The 1.7.0 source tree still has the incubating `DISCLAIMER`, because it was released before graduation [CLAIM-apache-hugegraph-04]. |
| Latest release | **1.7.0** for all four component repos, GitHub releases dated 2025-11-16. The Incubator news page dates the announcement 2025-11-28 [CLAIM-apache-hugegraph-01]. There is no 1.8.0 tag. master declares `<revision>1.8.0</revision>` and is very active (commits on 2026-10-18) [CLAIM-apache-hugegraph-03]. |
| EOIP pin | `hugegraph/hugegraph:1.7.0` and `hugegraph/hubble:1.7.0` (`deploy/docker-compose.yml:32`, `deploy/hubble/Dockerfile:1`). **This is the current release.** Watch for 1.8.0. |
| Licence | Apache-2.0 in all repos [CLAIM-apache-hugegraph-04]. Docker Hub images are "convenience releases, not official distribution artifacts" [CLAIM-apache-hugegraph-33]. |
| Cadence | 1.0.0 (2023-02), 1.2.0 (2023-12), 1.3.0 (2024-03), 1.5.0 (2024-12), 1.7.0 (2025-11). Roughly one release every 9–12 months, with even minor numbers skipped [CLAIM-apache-hugegraph-01]. |
| Runtime | Java 11 only for 1.7.0. Built on TinkerPop 3.5.1. RocksDB went from 7.2.2 to 8.10.2 in 1.7.0 [CLAIM-apache-hugegraph-06][CLAIM-apache-hugegraph-35]. |
| Components (members) | Server (REST, Gremlin, Cypher); PD (placement driver); Store (HStore); Toolchain (client Java/Go, Loader, Hubble, Tools, Spark connector); Computer (Java, K8s/YARN) and Vermeer (Go, in-memory); HugeGraph-AI (HugeGraph-LLM, HugeGraph-ML, python client, vermeer-python-client) [CLAIM-apache-hugegraph-36][CLAIM-apache-hugegraph-27][CLAIM-apache-hugegraph-28] |
| Tier reason | EOIP's configured primary backend (`config/graph-store.yaml:11`). It is the reference column for every C01/C10/C12 cohort. |

Sources: GitHub releases and tags (git ls-remote), source code at the 1.7.0 tags, the 1.7.0 release notes, the Incubator status page, the ASF announcement, the cypher-for-gremlin README, and the HugeGraph-LLM/Store/Vermeer READMEs. All are listed in Appendix C.

## 2. Primary problem, target workloads, concrete example workflows

HugeGraph is a TinkerPop-compliant OLTP property-graph database. It has an optional distributed storage tier, a separate OLAP compute tier and a Python AI tier. Its strongest documented use is large, schema-first graphs in Chinese enterprise and Internet settings. The ASF names security and social-networking domains [CLAIM-apache-hugegraph-02].

| Workflow | Upstream path |
|---|---|
| Schema-first bulk build | Define PropertyKey, VertexLabel, EdgeLabel and IndexLabel over REST, then load CSV/JSON/JDBC/HDFS with `hugegraph-loader`, or use the Spark connector |
| Interactive investigation | Hubble UI with a Gremlin/Cypher console, or REST traversers (`kout`, `kneighbor`, `shortest path`, `paths`, `rings`) [CLAIM-apache-hugegraph-22] |
| Analytics write-back | Submit PageRank/LPA/… to Computer or Vermeer; results land in OLAP property tables [CLAIM-apache-hugegraph-25][CLAIM-apache-hugegraph-27] |
| GraphRAG / text-to-Gremlin | HugeGraph-LLM: extract KG from text into a HugeGraph schema, retrieve with vector and graph search, generate Gremlin [CLAIM-apache-hugegraph-28] |
| EOIP reference question (service-account blast radius, J9) | Upstream can serve `kout`/`kneighbor` from the service-account vertex with label filters. EOIP instead expands neighbours in Python through `edges_from` (§11). |

## 3. Feature inventory

| Area | Capability | Status upstream (1.7.0) | Evidence |
|---|---|---|---|
| API | REST CRUD for vertices and edges, batch endpoints | present | `api/api/graph/BatchAPI.java` |
| API | Gremlin (REST `/gremlin` + Gremlin Server WebSocket) | present | [CLAIM-apache-hugegraph-06] |
| API | Cypher endpoint `/graphspaces/{gs}/graphs/{g}/cypher` | partial (translated to Gremlin by an unmaintained library) | [CLAIM-apache-hugegraph-11][CLAIM-apache-hugegraph-12] |
| API | REST traverser library (about 25 algorithms) | present | [CLAIM-apache-hugegraph-22] |
| API | Async tasks and jobs (rebuild index, Gremlin job, algorithm job, computer job) | present | `api/api/job/*`, `core/task/*` [CLAIM-apache-hugegraph-23] |
| Schema | Property keys, vertex/edge labels, index labels, nullable keys, sort keys, user_data | present | `api/api/schema/*` |
| Schema | Multi-link edge labels (`links`) and PARENT/SUB edge labels | present | [CLAIM-apache-hugegraph-13] |
| Schema | TTL on vertex and edge labels | present | [CLAIM-apache-hugegraph-24] |
| Index | SECONDARY, RANGE_{INT,LONG,FLOAT,DOUBLE}, SHARD, UNIQUE, SEARCH (tokenised) | present | [CLAIM-apache-hugegraph-09][CLAIM-apache-hugegraph-10] |
| Index | Vector index in server | **absent** (also absent on master 90790e8) | [CLAIM-apache-hugegraph-09] |
| Storage | RocksDB (standalone, embedded) | present, default | [CLAIM-apache-hugegraph-05] |
| Storage | HStore (PD + Store, Raft, hash partitions) | present (distributed, production target) | [CLAIM-apache-hugegraph-17] |
| Storage | HBase | present (per README) | [CLAIM-apache-hugegraph-05] |
| Storage | MySQL, PostgreSQL, Cassandra, ScyllaDB, Palo | **disabled in 1.7.0** (legacy; use 1.5.0 or earlier) | [CLAIM-apache-hugegraph-05] |
| Security | Auth (users, groups, targets, belongs, accesses, projects, roles), token login | optional (off unless configured; Docker `PASSWORD` enables it) | [CLAIM-apache-hugegraph-14][CLAIM-apache-hugegraph-32] |
| Security | Element-level read filtering by label regex and property predicate | present (post-filter) | [CLAIM-apache-hugegraph-15] |
| Tenancy | Graph spaces with CPU/memory/storage/graph-count/role quotas | partial: full management needs PD mode; standalone runs DEFAULT plus local graphs | [CLAIM-apache-hugegraph-16] |
| Ops | RocksDB snapshot/resume, `hugegraph-tools` backup/restore/dump/migrate/graph-clone/schedule-backup | present | [CLAIM-apache-hugegraph-26] |
| Ops | Metrics API, Arthas API, whitelist IP API, Raft API | present | `api/api/metrics`, `api/api/arthas`, `api/api/profile/WhiteIpListAPI.java` |
| OLAP | Computer (Java; K8s operator, YARN) and Vermeer (Go, in-memory, 15+ algorithms) | present (separate deployables) | [CLAIM-apache-hugegraph-27] |
| AI | HugeGraph-LLM: KG construction, text2gremlin, GraphRAG, Graph Agent, Gradio UI; Faiss/Milvus/Qdrant vector stores; LiteLLM providers | present (Python; separate service) | [CLAIM-apache-hugegraph-28] |
| AI | HugeGraph-ML: 21 DGL/PyTorch GNN models | present (library) | [CLAIM-apache-hugegraph-29] |
| AI | MCP server/toolsets | unreleased (master only) | [CLAIM-apache-hugegraph-30] |
| UI | Hubble (schema management, loading, Gremlin console, graph spaces in 1.7.0) | present | [CLAIM-apache-hugegraph-36] |
| SDK | Java client, Go client, Python client | present | [CLAIM-apache-hugegraph-36] |
| Standards | SPARQL, RDF, SHACL, OWL, GQL, SQL/PGQ, GraphQL | absent | no module found in the 1.7.0 tree (reasoned inference, 0.7) |
| Edition split | Community vs enterprise | none for code (single Apache-2.0 tree, distributed tier included) | [CLAIM-apache-hugegraph-04] |

## 4. Text-based architecture diagram

```
                  CONTROL PLANE                                     DATA PLANE
 Clients: REST / Gremlin(WS,HTTP) / Cypher / Hubble / Loader / Tools / HugeGraph-LLM (Python)
                                   │
 ┌─────────────────────────────── hugegraph-server (Java 11, Jetty/Jersey + Gremlin Server) ─────────────┐
 │ filters: Authentication, Path, LoadDetect, AccessLog, WhiteIP   (api/api/filter/*)                    │
 │ APIs: graph, schema, gremlin, cypher→(opencypher-gremlin 1.0.4)→gremlin, traversers, job, auth, space │
 │ HugeGraphAuthProxy (per-call permission + element FilterIterator)                                     │
 │ GraphManager: graph spaces / graphs (local conf  | PD meta when usePD=true)                            │
 │ StandardHugeGraph ─ thread-local TinkerPop tx ─ GraphTransaction / SchemaTransaction / IndexTx        │
 │   traversal strategies (HugeGraphStep, HugeVertexStep, HugeCount, HugePrimaryKey)                      │
 │   caches: CachedGraphTransaction / CachedSchemaTransaction (Ram/Offheap/Level) + CacheNotifier        │
 │   TaskScheduler (Standard | Distributed) for async schema/index/algorithm jobs                        │
 │ BinarySerializer → BackendMutation ─────────────► BackendStore SPI                                    │
 └───────────────────────────────────────────────────────┬──────────────────────────────────────────────┘
               ┌─────────────────────────────────────────┴───────────────────────────────┐
     STANDALONE (EOIP today)                                       DISTRIBUTED (HStore)
     RocksDBStore: one DB, column families per HugeType              hugegraph-pd (gRPC, Raft): partitions,
     (vertex, o/i edges, *_index, olap_*), optional                    store registry, graph-space meta, ids
     per-table data disks; WAL; snapshot/resume                      hugegraph-store × N (gRPC): partition
                                                                      engines = one JRaft group each, RocksDB,
                                                                      filter/agg/index pushdown
     OLAP tier (separate): Computer (K8s operator / YARN) │ Vermeer (Go master+workers, in-memory)
       reads graph → computes → writes OLAP properties back
     AI tier (separate): HugeGraph-LLM (Gradio + REST, LiteLLM, Faiss/Milvus/Qdrant) │ HugeGraph-ML (DGL)
```

## 5. Under-the-hood reconstruction

**5.1 Data model.** HugeGraph uses a strict-schema labelled property graph. You define a PropertyKey (data type, cardinality SINGLE/LIST/SET, aggregate type), then a VertexLabel, whose `id_strategy` is AUTOMATIC, PRIMARY_KEY, CUSTOMIZE_STRING, CUSTOMIZE_NUMBER or CUSTOMIZE_UUID, with `nullable_keys`, `ttl` and `enable_label_index`. Then an EdgeLabel (frequency SINGLE/MULTIPLE, `sort_keys`, `links` as a set of (source, target) label pairs, `edgelabel_type` NORMAL/PARENT/SUB, `ttl`), and then IndexLabels (`core/schema/*`, `api/api/schema/EdgeLabelAPI.java:194-224`) [CLAIM-apache-hugegraph-13][CLAIM-apache-hugegraph-24]. MULTIPLE edges between the same pair are told apart by `sort_keys`. A PRIMARY_KEY vertex id is derived from the label plus the primary-key values. Internal type codes are listed in `core/type/HugeType.java` (V, O, I, SI, II/FI/LI/DI range indexes, AI search, HI shard, UI unique, AP olap, T task) [CLAIM-apache-hugegraph-07]. OLAP property keys get their own tables so analytics write-back does not rewrite OLTP rows [CLAIM-apache-hugegraph-25].

**5.2 Storage layout (RocksDB, standalone).** `hugegraph-rocksdb/.../RocksDBTables.java` gives each HugeType its own column family. These are Meta, Counters, the schema tables (VL/EL/PK/IL), Vertex, Edge out (`o…`) and Edge in (`i…`), SecondaryIndex, VertexLabelIndex, EdgeLabelIndex, SearchIndex, UniqueIndex, RangeInt/Float/Long/DoubleIndex, ShardIndex, and one OlapTable per OLAP property (`:392`) [CLAIM-apache-hugegraph-07]. `RocksDBStore.java:213-243,827-859` can map individual tables to separate disks (`rocksdb.data_disks`, format `graph/vertex:/path`). The edge key layout is observed in `core/backend/serializer/BytesBuffer.java:733-743` [CLAIM-apache-hugegraph-08]:

```
vertex row : key = varlen(vertex_id)              value = label_id + properties (+ expire time)
edge row   : key = owner_vertex | dir(O|I) | edge_label_id | sub_label_id | sort_values\0 | other_vertex
             (stored twice: in the OUT table and the IN table → adjacency is a prefix scan on owner_vertex[|dir|label])
index row  : key = index_label_id | field_values (range: sortable numeric encoding) | element_id
             SECONDARY → prefix scan; RANGE → range scan; UNIQUE → point get + conflict check; SEARCH → token rows
```

What follows from this layout (reasoned inference, 0.6). An edge write costs two primary rows plus N index rows. An unindexed property filter falls back to a label-index scan plus filtering. A supernode's adjacency is one contiguous key range, so it is cheap to stream but expensive to filter without sort keys or indexes. SEARCH indexes tokenise with Chinese-oriented analyzers: Ansj, HanLP, IK, Jcseg, Jieba, MMSeg4J and SmartCN (`core/analyzer/*`). The enum comment still says "full-text query (not supported now)" [CLAIM-apache-hugegraph-10][CLAIM-apache-hugegraph-37]. There is **no vector index type** at 1.7.0 or on master [CLAIM-apache-hugegraph-09].

**5.3 Storage layout (HStore, distributed).** PD keeps partition metadata, store registration, graph-space metadata and id allocation, and is itself Raft-replicated. Store nodes host partition engines. **Each partition is one JRaft group** over RocksDB, data is hash-partitioned, and the store pushes down filters, aggregations and index work and runs multi-partition scans in parallel (`hugegraph-store/README.md:10-71`) [CLAIM-apache-hugegraph-17]. The servers become stateless query nodes. The repo ships `docker/docker-compose-3pd-3store-3server.yml` [CLAIM-apache-hugegraph-18]. A legacy "raft mode" for replicating RocksDB still exists in `core/backend/store/raft/`. Its supported status in 1.7.0 is UNVERIFIED [CLAIM-apache-hugegraph-38].

**5.4 Query pipeline.** There are three entry paths. (a) REST CRUD and the traverser APIs call `GraphTransaction` directly. (b) Gremlin is TinkerPop bytecode or a Groovy script. HugeGraph strategies in `core/traversal/optimize/` (HugeGraphStepStrategy, HugeVertexStepStrategy, HugeCountStepStrategy, HugePrimaryKeyStrategy) fold `has()` filters, `count()` and adjacency expansion into backend `ConditionQuery` objects [CLAIM-apache-hugegraph-21]. (c) Cypher is parsed by `org.opencypher.gremlin:translation:1.0.4` into a Gremlin traversal (`api/opencypher/CypherOpProcessor.java`, `hugegraph-api/pom.xml:154`) [CLAIM-apache-hugegraph-11]. That translator's README says it is "not maintained anymore" and that about 75 % of openCypher TCK M13 scenarios work on TinkerGraph [CLAIM-apache-hugegraph-12]. Planning chooses indexes per condition: `GraphIndexTransaction` matches conditions against the available index labels and prefers an exact or unique match, then secondary, range, label index, and finally a scan. This order is a *hypothesis* from code structure; there is no documented cost model and no statistics-based CBO [CLAIM-apache-hugegraph-21]. Pagination uses opaque `page` tokens, which EOIP already uses (`hugegraph.py:363`).

Index-selection sketch (hypothesis, reconstructed from class roles):
```
plan(ConditionQuery q):
  if q has id(s): return point-get
  cands = index_labels_covering(q.label, q.fields)        # unique > secondary(all fields) > range > shard > search
  if cands: ids = intersect(scan(idx) for idx in best_cover(cands)); return fetch(ids) then filter(q.residual)
  if label_index_enabled(q.label): return scan(label_index) then filter(q)
  return full_table_scan then filter(q)                   # may be refused or capped by config limits
```

**5.5 Reasoning.** None. There is no RDFS/OWL or rule engine. Schema constraints (label membership, nullable keys, data types, edge link pairs) are enforced at write time. Computer/Vermeer algorithms are analytics, not inference (reasoned inference from the module inventory, 0.7).

**5.6 Concurrency and transactions.** Transactions are thread-local TinkerPop transactions (`core/StandardHugeGraph.java:1636-1652`). Mutations are buffered in `GraphTransaction` up to `VERTEX_TX_CAPACITY`/`EDGE_TX_CAPACITY` (`GraphTransaction.java:141-176,2105-2116`), then serialized into one `BackendMutation` per commit. On RocksDB that commit is applied as one write batch (hypothesis, 0.5). Schema deletion takes read locks through `LockUtil.LocksTable` (`:629-631,885-887`) [CLAIM-apache-hugegraph-19]. There is no documented MVCC and no snapshot isolation for multi-statement reads. Unique-index conflicts are detected at commit, which EOIP worked around (`hugegraph.py:571`: "batch PUT conflicts with UNIQUE vertex indexes"). Schema DDL that touches data (index rebuild, label removal) runs as **asynchronous tasks** returning `task_id`, and EOIP polls `/tasks/{id}` (`hugegraph.py:63-78`).

**5.7 Partitioning and consistency.** Standalone has a single RocksDB per server and no replication. HStore gives Raft-consistent replicas per partition (strong per partition). Cross-partition multi-element commits have no documented distributed-transaction protocol: NOT PUBLICLY VERIFIED, so treat them as non-atomic across partitions until tested [CLAIM-apache-hugegraph-17].

**5.8 Caching.** Vertex, edge and schema caches (`core/backend/cache/`: RamCache, OffheapCache, LevelCache, CachedGraphTransaction, CachedSchemaTransaction) are invalidated cluster-wide through `CacheNotifier` events. A notifier bug was fixed in 1.7.0 [CLAIM-apache-hugegraph-20]. The caches are per graph, not per user. Permission filtering happens *after* cache reads in the auth proxy (§5.10), so a cache hit cannot bypass the proxy (reasoned inference, 0.6).

**5.9 Versioning and time.** HugeGraph has **no history, MVCC time-travel or bitemporality**. It offers per-label TTL expiry [CLAIM-apache-hugegraph-24] and RocksDB snapshots (`BackendStore.createSnapshot/resumeSnapshot`, implemented in `RocksDBStore`) [CLAIM-apache-hugegraph-26]. EOIP's revision vertices and bitemporal layer (BL-37) stay application-level on every backend.

**5.10 Security.** The authenticators are ConfigAuthenticator (a single admin token/password) and StandardAuthenticator, which keeps users in a graph store (`api/auth/*`). The model has User, Group, Belong (user→group), Target, Access (group→target with permission), Project and Role. The permissions are NONE, READ, WRITE, DELETE, EXECUTE, SPACE, SPACE_MEMBER and ADMIN, with default roles space, space_member, analyst and observer [CLAIM-apache-hugegraph-14]. A Target holds resources typed VERTEX, EDGE, SCHEMA, GREMLIN, TASK, VAR, … with a **label regex and property predicates** (`core/auth/HugeResource.java:189-219`). `HugeGraphAuthProxy` wraps every read iterator in a `FilterIterator` that drops elements the user cannot READ (`:1063-1084`) [CLAIM-apache-hugegraph-15]. This is post-filtering: it is correct but not index-assisted, and `limit`/`count` results may reflect pre-filter work (hypothesis). The GREMLIN resource is a single coarse permission for arbitrary scripts. Graph spaces carry CPU/memory/compute limits, olap/storage namespaces, max graphs/roles and an auth flag (`core/space/GraphSpace.java:43-67`). Space creation, quotas and service registration go through PD (`api/core/GraphManager.java:279,834,894`). In non-PD mode graphs are created locally and scoped by the `space-graph` name [CLAIM-apache-hugegraph-16].

**Equivalent-behaviour blueprint for EOIP (re-implementation, not copying).** (1) Keep EOIP's backend-neutral `GraphStore`, but add *pushdown hooks*: `neighbourhood(k, labels, filters)` maps to `kout`/`kneighbor` on HugeGraph, to Cypher variable-length patterns on Neo4j, and to Gremlin `repeat()` on Neptune. (2) Make permission predicates explicit and indexable, so an `acl_principal_hash` SECONDARY index can be pushed down on every backend instead of relying on HugeGraph's post-filter. (3) Map tenant to graph (standalone) or graph space (PD) behind one `TenantPlacement` interface.

## 6. Functional and non-functional requirements inferred from verified behaviour

| ID | Inferred requirement (what an equivalent engine must do) | Evidence |
|---|---|---|
| FR-1 | Schema-first DDL with typed keys, nullable keys, sort keys, link pairs and TTL; DDL that touches data runs as an async task with status polling | §5.1, §5.6 |
| FR-2 | Five index families (secondary, range, shard, unique, search) declared per label | [CLAIM-apache-hugegraph-09] |
| FR-3 | Server-side traversal primitives (k-out, k-neighbour, paths, rings, similarity) with depth, degree and limit caps | [CLAIM-apache-hugegraph-22] |
| FR-4 | Element-level permission filtering by label and property predicate | [CLAIM-apache-hugegraph-15] |
| FR-5 | Analytics run outside the OLTP process, with write-back to isolated property storage | [CLAIM-apache-hugegraph-25] |
| NFR-1 | One-node embedded mode with no external dependencies (RocksDB) | [CLAIM-apache-hugegraph-05] |
| NFR-2 | Scale-out by partition plus Raft replication with a separate metadata service | [CLAIM-apache-hugegraph-17] |
| NFR-3 | Bounded transaction size (capacity limits), so bulk paths must batch | [CLAIM-apache-hugegraph-19] |
| NFR-4 | Auth must be enabled explicitly for production | [CLAIM-apache-hugegraph-32] |

## 7. Performance and resource model

- **Vendor claims only.** The README says it "supports more than 10 billion vertices & edges". The ASF announcement says it "processes hundreds of billions of graph elements with millisecond-level latency". Neither states workload or hardware, so both are classed **Unverified** [CLAIM-apache-hugegraph-31]. No independent LDBC SNB or Graphalytics result for HugeGraph 1.7 was found in this run (NOT PUBLICLY VERIFIED).
- **Cost model (reasoned inference, 0.5).** Writes cost about 2 primary rows per edge plus one row per index field per element. Reads by id are point gets. Adjacency is a prefix scan. A property filter without an index scans the label index and filters in memory. JVM heap holds the caches; RocksDB block cache and memtables use native memory. EOIP sets `HG_SERVER_MIN_FREE_MEMORY: "0"`, which disables the server's low-memory guard (`deploy/docker-compose.yml:35`); this matters on small single nodes.
- **EOIP-specific amplification (observed in EOIP code).** The adapter creates 75 vertex labels, each carrying all 250 property keys, **677 physical edge labels** (68 logical labels expanded per source/target pair) and **1,005 index labels**. This was computed from `HugeGraphStore._schema_definitions()` [CLAIM-apache-hugegraph-40]. The `idx_edge_key` index is replicated across all 677 edge labels, and `find_vertices`/`count_vertices`/`count_edges` page through whole label sets in Python (`hugegraph.py:390-410,504-510`). Expect O(N) counts and slow schema bootstrap. This is a self-inflicted cost (INV-SELF-HG-01).
- **Failure modes.** Unique-index conflicts in batch PUT (EOIP comment). Async schema tasks failing or timing out. A large Gremlin result set exhausting heap. Standalone RocksDB is a single point of failure with no HA. Cache-notifier lag across servers (fixed issue in 1.7.0).
- **Uncertainty.** EOIP never ran a live HugeGraph in the baseline run (U-01), so all latency numbers are unknown. See §14 BM-HG-01..04.

## 8. Strengths and use-case-specific advantages

| # | Strength | Evidence | How EOIP matches or exceeds it |
|---|---|---|---|
| S1 | Whole stack, distributed tier included, under Apache-2.0 with no community/enterprise split | [CLAIM-apache-hugegraph-04][CLAIM-apache-hugegraph-17] | Keep HugeGraph as the redistribution-safe default backend; ship HStore as the scale-out option |
| S2 | Server-side traverser library (about 25 algorithms) | [CLAIM-apache-hugegraph-22] | Push `kout`/`kneighbor`/`shortest path` down from QueryPlan templates (STR-02) |
| S3 | Fine-grained auth (label + property predicates) and graph spaces with quotas | [CLAIM-apache-hugegraph-14..16] | Use as defence in depth under EOIP's own ACL enforcement (STR-03) |
| S4 | Rich schema: unique/secondary/range indexes, multi-link and parent/sub edge labels, TTL, OLAP write-back | [CLAIM-apache-hugegraph-13][CLAIM-apache-hugegraph-24][CLAIM-apache-hugegraph-25] | Collapse the adapter's schema explosion; use TTL for agent-memory expiry |
| S5 | Separate OLAP engines (Computer, Vermeer) | [CLAIM-apache-hugegraph-27] | Integrate as an optional analytics module for graphs too big for in-process `graph/algorithms.py` |
| S6 | HugeGraph-AI: text2gremlin, KG extraction, GraphRAG, 21 GNN models | [CLAIM-apache-hugegraph-28][CLAIM-apache-hugegraph-29] | Reuse as a benchmark baseline and pattern source, not as a runtime dependency |

## 9. Limitations with root causes

| Limitation | Type | Root-cause class | Evidence |
|---|---|---|---|
| Cypher depends on an **unmaintained** translator (cypher-for-gremlin 1.0.4), covers only a subset, and only through Gremlin | Verified trade-off / maturity | Algorithmic dead-end (translation layer); developer friction | [CLAIM-apache-hugegraph-11][CLAIM-apache-hugegraph-12] |
| No vector index in the server; vectors live in Faiss/Milvus/Qdrant via HugeGraph-LLM | Verified absence | Operational overhead (extra store, consistency) | [CLAIM-apache-hugegraph-09][CLAIM-apache-hugegraph-28] |
| Full-text analyzers are Chinese-oriented, and the enum calls SEARCH "not supported now" | Verified, with contradictory signals | User friction for non-CJK text | [CLAIM-apache-hugegraph-10][CLAIM-apache-hugegraph-37] |
| Permission filtering is a post-filter over iterators; GREMLIN permission is all-or-nothing | Verified design | Algorithmic (no index-assisted ACL); security friction | [CLAIM-apache-hugegraph-15] |
| Full graph-space management (quotas, service registration) needs PD | Verified (code branches) | Operational overhead (3+ PD, 3+ Store for the documented topology) | [CLAIM-apache-hugegraph-16][CLAIM-apache-hugegraph-18] |
| No history, MVCC time travel or bitemporal model | Verified absence | Data-model limit; EOIP must stay app-level | §5.9 |
| No cost-based optimiser or EXPLAIN-style plan output found | Hypothesis (no doc found) | Algorithmic | §5.4 |
| Legacy backends (MySQL/PG/Cassandra/ScyllaDB) disabled in 1.7.0 | Verified breaking change | Maturity / scope narrowing | [CLAIM-apache-hugegraph-05] |
| Java 11 only, TinkerPop 3.5.1 (older line) | Verified | Operational / upgrade risk | [CLAIM-apache-hugegraph-06] |
| Release cadence of about 1 per year; docs page marked "WIP … BETA" | Verified | Maturity | [CLAIM-apache-hugegraph-01] |
| Distributed cross-partition atomicity undocumented | Unknown | NOT PUBLICLY VERIFIED | §5.7 |

## 10. Deployment, licensing, redistribution, and operational viability under EOIP constraints

| Constraint | Assessment |
|---|---|
| Air-gap | **Yes.** Server, PD, Store, Hubble, Computer and Vermeer are self-hosted with no cloud dependency. HugeGraph-LLM is air-gap capable only with local LLM endpoints via LiteLLM and local vector stores (Faiss), and its README defaults point at hosted model providers (reasoned inference, 0.6). |
| Licence | Apache-2.0 across repos. **Legal-review trigger: low.** Three items still need checking: transitive dependencies (Chinese NLP analyzers, cypher-for-gremlin, RocksDB under Apache-2.0/GPLv2 dual licence, LiteLLM, whose repo has a separately licensed `enterprise/` directory — UNVERIFIED for the pinned version), ASF trademark rules when white-labelling ("Apache HugeGraph" naming in UI or docs), and the fact that Docker images are convenience binaries, not ASF releases [CLAIM-apache-hugegraph-33]. |
| One node | RocksDB standalone, 1 container (EOIP compose). Viable. |
| Scale-out | HStore: PD + Store + Server, each normally 3 or more. EOIP's `deploy/docker-compose.ha.yml:128-170` labels PD/Store as needing "enterprise/infra images" and pins `hugegraph/pd:latest` and `hugegraph/store:latest`. **Both are wrong or risky:** PD and Store are Apache OSS images from the same release [CLAIM-apache-hugegraph-17][CLAIM-apache-hugegraph-18][CLAIM-apache-hugegraph-41]. Pin `:1.7.0`. |
| Tenant isolation | Upstream gives: separate graphs (separate RocksDB tables per graph), graph spaces (PD), and per-space auth. EOIP uses none of these: the adapter is hard-wired to `/graphspaces/DEFAULT/graphs/{graph}` and logs in as the `admin` superuser (`hugegraph.py:31-38`, `config/graph-store.yaml:18`) [CLAIM-apache-hugegraph-39]. |
| Backup | Upstream offers RocksDB snapshot API and `hugegraph-tools backup/restore/schedule-backup`. EOIP uses its own paging export (`native_export`, `hugegraph.py:693`), which is not point-in-time consistent under concurrent writes (reasoned inference, 0.6). |

**Upstream capabilities the EOIP adapter does not use (available upstream / not integrated):** Cypher endpoint; REST traversers; `count` pushdown (`g.V().hasLabel().count()` via HugeCountStepStrategy) instead of Python paging; multi-link/parent-sub edge labels; TTL; OLAP properties; Computer/Vermeer; HugeGraph-AI (text2gremlin, GraphRAG, ML); the auth model (users, groups, targets, property-predicate resources); graph spaces and per-tenant graphs; RocksDB snapshot and hugegraph-tools backup; SEARCH/RANGE/SHARD index types (the adapter uses only UNIQUE and SECONDARY, per `ontology/manifest.py:455-476`); Gremlin bytecode (the adapter sends Groovy scripts with closures, `hugegraph.py:525-528`); metrics API; HStore [CLAIM-apache-hugegraph-39][CLAIM-apache-hugegraph-42].

## 11. Competitive delta against the EOIP verified baseline

| Area | HugeGraph upstream | EOIP baseline | Delta |
|---|---|---|---|
| Storage and adapter | Native LPG, indexes, batch | BL-02 adapter Implemented / live-unverified; BL-01 protocol has no pushdown | EOIP gives up native traversal and counting (Performance gap) |
| Multi-hop | REST traversers [CLAIM-apache-hugegraph-22] | BL-08 templates executed via protocol in Python | Available upstream / not integrated |
| Cypher | Partial (translator) | BL-03/BL-04 Cypher only on Neo4j and Neptune; BL-09 regex transpiler | Do not rely on HG Cypher; portable IR remains EOIP work |
| Permissions | Label/property-predicate post-filter [CLAIM-apache-hugegraph-15] | BL-18 **Absent** (P0); BL-19 API RBAC | Upstream offers defence in depth; EOIP must still BUILD backend-neutral ACL enforcement |
| Tenancy | Graphs, graph spaces (PD) [CLAIM-apache-hugegraph-16] | BL-20 Partial: adapters not tenant-aware [CLAIM-apache-hugegraph-39] | Available upstream / not integrated; P0 |
| Temporal | TTL only | BL-37/BL-38 Implemented (app-level) | EOIP ahead; keep app-level |
| Reasoning, SHACL, ontology | None | BL-28..BL-32 Partial | EOIP ahead (in-house) |
| Vector and full-text | No vector; CJK search index | BL-13..BL-15 in-process | Neither has a production vector tier; HugeGraph-LLM uses external stores |
| Analytics and ML | Computer, Vermeer, HugeGraph-ML | BL-43 in-process; BL-44 Partial; numpy missing | Available upstream / not integrated (optional module) |
| NL→query | text2gremlin (LLM) | BL-11 deterministic Implemented; BL-12 Partial | EOIP deterministic-first is a differentiator; HG-LLM is a useful baseline |
| Backup | Snapshot + tools | BL-50 scripts / live-unverified | Integrate the upstream snapshot |
| UI | Hubble (EOIP already ships a customised Hubble) | BL-54 | EOIP reuses Hubble; white-label review needed |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

### Strength-adoption cards

| STR-ID | Strength | Evidence | Value to EOIP customers | Decision | Design approach | Acceptance test |
|---|---|---|---|---|---|---|
| STR-apache-hugegraph-01 | Apache-2.0 full stack incl. distributed HStore, no edition split | CLAIM-01, -04, -17 | Redistribution-safe default backend for white-label OEM | integrate | Keep HugeGraph primary; add an HStore deployment profile pinned to the same release | Licence/NOTICE audit of the bundled images passes; J16 install on HStore 3×3×3 |
| STR-apache-hugegraph-02 | Server-side traverser library | CLAIM-22 | Fast J1/J9 impact queries | integrate | Optional `GraphStore.neighbourhood()` pushdown; HugeGraph uses `kout`/`kneighbor` with label filters, max_degree and limit | BM-HG-02: kout depth 3 matches Python expansion results and is at least 5× faster on 1M edges (target, PROPOSED) |
| STR-apache-hugegraph-03 | Property-predicate element auth and graph spaces | CLAIM-14, -15, -16 | Defence in depth for J5/J13 | integrate (secondary layer) | Per-tenant HugeGraph user with Access to that tenant's graph only; EOIP stays the primary enforcer | Cross-tenant read with tenant-A credentials returns 0 rows on tenant-B graph (J13) |
| STR-apache-hugegraph-04 | Multi-link and parent/sub edge labels, TTL | CLAIM-13, -24 | Simpler schema; memory expiry | match | Collapse 677 physical edge labels to 68 using `links` (INV-SELF-HG-01); TTL for ephemeral agent memory | Schema bootstrap time and index-label count drop; conformance suite green |
| STR-apache-hugegraph-05 | Separate OLAP engines (Vermeer in-memory, Computer on K8s) | CLAIM-27 | Analytics at scale without loading OLTP | experiment | Optional module: export a snapshot to Vermeer, write results to a prediction plane, never to facts (J8) | PageRank/LPA on 10M edges completes within the resource budget; results land in the prediction plane |
| STR-apache-hugegraph-06 | HugeGraph-LLM text2gremlin and GraphRAG | CLAIM-28 | Benchmark baseline for J6/J11 | integrate as baseline only | Run under the egress gateway with local LiteLLM to Ollama | J6 harness reports EOIP deterministic vs HG-LLM vs BM25/dense baselines |

### Con-to-Pro inversion cards

No seed hypothesis in Master Prompt §10.5 targets HugeGraph directly. The additional direction "fixed vendor query languages → typed query plans plus adapters" is **validated** by INV-01. The Neo4j seed ("weak formal semantics, no native reasoning") **also holds for HugeGraph**: no reasoning or validation layer (§5.5). It is handled by EOIP's mutation gateway (BL-28) and is not duplicated here.

**INV-apache-hugegraph-01 — Cypher via an unmaintained translator**
- Target: HugeGraph 1.7.0 `/cypher`, any Cypher workload. Limitation: Cypher is translated to Gremlin by cypher-for-gremlin 1.0.4, which upstream marks unmaintained, and about 75 % of TCK M13 passes on TinkerGraph [CLAIM-apache-hugegraph-11][CLAIM-apache-hugegraph-12].
- Root cause: coupling plus maturity (*proven*: dependency and README); no native Cypher planner.
- Why an alternative helps: EOIP's QueryPlan / portable IR compiles straight to each backend's native language (Gremlin bytecode for HugeGraph, Cypher for Neo4j), so there is no double translation. It would be worse if users demand ad-hoc Cypher on HugeGraph.
- Options: (1) quick: expose HG `/cypher` read-only for power users, with a warning; (2) pragmatic: compile a typed IR subset (match, k-hop, filter, aggregate) to Gremlin bytecode with a parity test suite; (3) long-term: GQL-shaped IR with per-backend capability descriptors and emulation.
- Selected: option 2. Pattern: compiler with capability negotiation.
  ```
  plan = QueryPlan(match=[V("Service",id=$s)], expand=Out(["DEPENDS_ON"],1..3), filter=acl(principal), limit=500)
  compile(plan, backend="hugegraph") -> g.V($s).repeat(out('DEPENDS_ON__*')).times(3).emit().has('acl_h',within($p)).limit(500)
  compile(plan, backend="neo4j")     -> MATCH (s:Service {id:$s})-[:DEPENDS_ON*1..3]->(x) WHERE x.acl_h IN $p RETURN x LIMIT 500
  ```
- POC: BM-HG-03, 40 J1/J9 queries, results compared across HugeGraph, Neo4j and Memory. Success means 100 % result parity, p95 ≤ the Python path, and zero injection (parameters only). Budget: 1 dev-week, one node.
- Failure cases: an IR feature unsupported on a backend must fail closed with a parity-gap error, never silently fall back to an unfiltered query. ACL predicates are mandatory nodes in the IR.
- Defensibility: one governed IR across HugeGraph, Neo4j and Neptune, with policy nodes, cannot be copied by a single engine.
- Decision: **ADOPT**.

**INV-apache-hugegraph-02 — Permission filtering is a post-filter, and tenancy primitives are PD-gated**
- Target: 1.7.0 auth proxy and graph spaces. Limitation: element reads are filtered after retrieval (`FilterIterator`). The GREMLIN permission is coarse. Full graph-space quotas need PD [CLAIM-apache-hugegraph-15][CLAIM-apache-hugegraph-16].
- Root cause: security design (*proven*, code) plus deployment (*proven*, `usePD` branches).
- Alternative: EOIP stores an `acl_principal_hash` set (from BL-17 `acl_hash`) on each element with a SECONDARY index and injects it as a mandatory predicate in the compiled query, so filtering happens before limits and counts and works the same on Neo4j and Neptune. Tenants map to separate HugeGraph graphs in standalone mode and to graph spaces in PD mode. It would be worse when ACL sets churn heavily (re-index cost) or principals are very numerous; then use group-level hashes.
- Options: (1) quick: one HugeGraph graph per tenant plus a per-tenant HugeGraph user; (2) pragmatic: option 1 plus the ACL predicate pushdown above; (3) long-term: ReBAC (OpenFGA/SpiceDB-style) resolving principals to group hashes at query time, with revocation invalidating caches.
- Selected: option 2. Pattern: policy-enforcement point in the compiler, plus physical tenant separation.
- POC: J5 + J13 harness. Two tenants and two users with disjoint ACLs; 1,000 randomised queries. Success means 0 leaked rows, and `limit 10` returns 10 authorised rows whenever 10 or more exist.
- Failure cases: ACL hash staleness after revocation (must invalidate caches and indexes, J5); admin superuser credentials in the adapter defeat upstream auth (fix: per-tenant least-privilege users).
- Defensibility: source-ACL propagation from connectors to answers is cross-backend, which a single engine does not provide.
- Decision: **ADOPT** (P0).

**INV-apache-hugegraph-03 — No native vector index; CJK-centric full-text**
- Target: 1.7.0 server plus HugeGraph-LLM. Limitation: no vector index type. HugeGraph-LLM keeps vectors in Faiss/Milvus/Qdrant, outside graph transactions, with no graph ACL [CLAIM-apache-hugegraph-09][CLAIM-apache-hugegraph-28].
- Root cause: storage scope (*proven*).
- Alternative: an EOIP-owned retrieval index (BM25 + dense, optionally a REUSE vector DB per C10) keyed by canonical_id and carrying tenant and ACL payload filters, rebuilt from the SourceEvent log. It would be worse if a backend later ships native vector indexes with ACL-aware filtering (Neo4j already has vector indexes; see the W02 deep dive).
- Options: (1) use HugeGraph-LLM's Faiss store; (2) EOIP sidecar index with payload filters and an outbox-driven freshness pipeline; (3) a backend capability flag that uses a native vector index where it exists and the sidecar otherwise.
- Selected: option 3, built on option 2.
- POC: BM-HG-04, hybrid retrieval on the J6 dataset against BM25 and dense baselines. Success means nDCG@10 ≥ the best non-graph baseline + 0.03 and zero ACL leaks.
- Failure cases: index-graph divergence after deletes or tombstones (BL-25), so a reconciliation job is required.
- Defensibility: ACL-aware hybrid retrieval that works the same on any backend.
- Decision: **ADOPT** (option 2 now, option 3 later).

**INV-SELF-HG-01 (EOIP self-inversion) — Adapter schema explosion and Python-side scans**
- Target: EOIP `graph/hugegraph.py` on HugeGraph 1.7.0. Limitation: 677 physical edge labels, 1,005 index labels, every vertex label carrying all 250 keys, and O(N) counts and filters done by paging in Python [CLAIM-apache-hugegraph-40][CLAIM-apache-hugegraph-42].
- Root cause: coupling (*proven*). The docstring assumes "edge labels have one source/target label pair" (`hugegraph.py:3-4`), but 1.7.0 supports `links` [CLAIM-apache-hugegraph-13].
- Alternative: one edge label per logical relationship with `links`, per-label property sets from the manifest, count and filter via Gremlin `count()` and index-backed `has()`. It would be worse if `links` labels behave badly with `sort_keys`/indexes in practice (to be tested), or if migrating existing data is costly.
- Options: (1) only push counts and filters to Gremlin; (2) option 1 plus a new schema version with `links` and per-label properties, migrated through `native_export`/`bulk_load`; (3) generate the backend schema from the ontology-as-code (BL-32) with a per-backend schema compiler.
- Selected: option 2, then option 3.
- POC: BM-HG-01, bootstrap time, index count, `count_vertices` latency at 1M vertices, and conformance parity before and after. Success means index labels ≤ 150, counts ≥ 10× faster (target), conformance green, and rollback by restoring the old schema snapshot.
- Failure cases: logical edge names stay stable for callers (already abstracted); migration needs an empty graph (`native_import` precondition), so offline migration needs an ADR (Master Prompt §4.3-13).
- Defensibility: N/A (internal hygiene). Decision: **ADOPT**.

**INV-apache-hugegraph-04 — Single-node RocksDB has no HA; HStore is heavy**
- Limitation: standalone RocksDB has no replication. HA means a 3 PD + 3 Store + N Server topology [CLAIM-apache-hugegraph-17][CLAIM-apache-hugegraph-18].
- Root cause: deployment (*proven*).
- Alternative: one-node first with consistent snapshots (upstream snapshot API or hugegraph-tools) plus the SourceEvent replay log (BL-24) as the recovery source; HStore only for customers who need HA. It would be worse for RPO=0 requirements.
- Options: (1) scheduled `hugegraph-tools backup`; (2) snapshot plus replay from a checkpoint, with restore drills; (3) HStore profile with documented sizing.
- Selected: option 2 now, option 3 deferred. POC: kill -9 during ingest, then restore the snapshot and replay; success means zero lost events and no duplicate identities (J7).
- Decision: **EXPERIMENT**.

## 13. Per-capability decisions

| Capability | Backend-native on HugeGraph? | Decision | Note |
|---|---|---|---|
| CAP-01 LPG storage/indexing | native | INTEGRATE | Keep as primary backend; fix the schema shape (INV-SELF-HG-01) |
| CAP-05 scale-out | native (HStore) | DEFER | Profile pinned to 1.7.0; correct the HA compose |
| CAP-06 bulk load | native (batch API, Loader) | REUSE | Loader for initial backfills of very large exports, still behind the governed path |
| CAP-13 Gremlin | native | INTEGRATE | Move from Groovy scripts with closures to bytecode or parameterised scripts |
| CAP-14 Cypher | partial (translator) | REJECT as dependency | Use the IR compiler instead (INV-01) |
| CAP-19 multi-hop | native traversers | INTEGRATE | Pushdown hook (STR-02) |
| CAP-20 portable IR | absent | BUILD | INV-01 |
| CAP-45/46 RBAC/ACL | partial (post-filter) | BUILD (EOIP) + INTEGRATE (HG auth as defence in depth) | INV-02 |
| CAP-47 tenant isolation | partial (graphs, spaces with PD) | INTEGRATE | Graph per tenant (standalone), graph space (PD) |
| CAP-53 vector | absent | BUILD/REUSE (sidecar, C10) | INV-03 |
| CAP-54 full-text | partial (CJK analyzers) | EXPERIMENT | Test SEARCH index with English text before relying on it |
| CAP-56 GraphRAG | HugeGraph-LLM | EXPERIMENT (baseline only) | Under the egress gateway |
| CAP-58 NL→query | text2gremlin | EXPERIMENT (baseline) | Compare against BL-11 |
| CAP-62 algorithms | native (traversers, Computer, Vermeer) | INTEGRATE (optional module) | Predictions go to the prediction plane |
| CAP-64 GNN | HugeGraph-ML (DGL) | DEFER | Needs N1 stack; DGL maintenance check (W24) |
| CAP-34/36 temporal/history | absent (TTL only) | BUILD (keep app-level BL-37) | — |
| CAP-57 agent memory expiry | TTL native | EXPERIMENT | TTL plus EOIP invalidation |
| CAP-74 backup/PITR | snapshot + tools | INTEGRATE | Replace paging export for consistent backups |
| CAP-59 MCP | master only | DEFER | Re-check at 1.8.0 |
| CAP-70/71 UI | Hubble | REUSE (already) | White-label/trademark review |

## 14. Concrete tests, proof-of-concept, and acceptance conditions (all PROPOSED)

| ID | Test | Dataset | Pass condition |
|---|---|---|---|
| BM-HG-01 | Schema v2 (`links`, per-label properties) vs current | Synthetic EOIP digital thread, 1M V / 5M E | Index labels ≤ 150; bootstrap ≤ 25 % of current; conformance (`graph/conformance.py`) green |
| BM-HG-02 | `kout`/`kneighbor` pushdown vs Python expansion (J1, J9) | Same | Identical result sets; p95 ≥ 5× faster at depth 3 |
| BM-HG-03 | IR→Gremlin/Cypher parity | 40 template queries × HugeGraph/Neo4j/Memory | 100 % parity or an explicit parity-gap error; 0 string-concatenated queries |
| BM-HG-04 | Hybrid retrieval with ACL payload | J6 corpus | ≥ best non-graph baseline + 0.03 nDCG@10; 0 leaks |
| SEC-HG-01 | Tenant per graph plus per-tenant HG user (J13) | 2 tenants | 0 cross-tenant rows via REST, Gremlin and Hubble |
| SEC-HG-02 | HG Target property-predicate filter correctness and `limit` semantics | 10k elements, 2 users | Filtered counts are exact; behaviour of limit-before-filter documented |
| OPS-HG-01 | Snapshot + replay recovery (J7) | Ingest under kill -9 | 0 lost events, 0 duplicate identities |
| OPS-HG-02 | Air-gapped install of server, Hubble and HG-LLM with Ollama (J16) | Offline host | All features work with egress blocked |
| LIC-HG-01 | NOTICE/transitive licence audit of the images EOIP ships | hugegraph/hugegraph:1.7.0, hubble:1.7.0 | No unflagged copyleft; trademark use reviewed |

## 15. Risks, trade-offs, and open research questions

- **1.8.0 drift.** master is moving fast (auth clear and truncate fixes, MCP in AI). API paths changed in 1.7.0 (auth path, graph spaces). Pin versions and run the conformance suite on every bump.
- **Translator dependency.** Upstream Cypher may change or be replaced. Do not build features on it.
- **Groovy script execution.** The adapter sends Groovy closures. If HugeGraph's Gremlin sandboxing is weak, a compromised EOIP process could run arbitrary scripts. Use bytecode and least-privilege HG users. Sandbox status is UNVERIFIED.
- **Admin credentials.** EOIP's single admin login concentrates risk. Per-tenant users are required for defence in depth.
- **Open questions.** (1) Does `links` work correctly with `sort_keys` and edge indexes under load? (2) Exact behaviour of graph spaces without PD in 1.7.0 (create and auth per space)? (3) Is cross-partition commit atomic in HStore? (4) Is SEARCH index quality acceptable for English? (5) Legacy RocksDB raft mode support status? (6) Is there any independent LDBC result for 1.7?

## Appendix A — Research-dimension coverage

| Dim | Section(s) | Summary or N/A reason |
|---|---|---|
| D1 Identity/maturity | 1 | ASF TLP 2026-01-21; 1.7.0 latest; Apache-2.0 |
| D2 Problem/workloads | 2 | Schema-first OLTP LPG plus OLAP and AI tiers |
| D3 Architecture | 4, 5.3 | Server / PD / Store / Computer / Vermeer / AI |
| D4 Storage/indexing | 5.2, 5.3 | RocksDB column families per type; edge key layout; 5 index families; no vector |
| D5 Schema/semantics | 5.1 | Strict schema, links, parent/sub, TTL; no ontology |
| D6 Query pipeline | 5.4 | Strategies, translator Cypher, index selection (hypothesis), no CBO found |
| D7 Reasoning | 5.5 | None |
| D8 Transactions/scale | 5.6, 5.7 | Thread-local tx, capacity caps, Raft per partition |
| D9 Ingestion/federation | 2, 3 | Loader, Spark/Flink connectors; no OBDA |
| D10 Identity/evidence | 5.1 | Id strategies only; no ER or provenance |
| D11 Time/evolution | 5.9 | TTL, snapshots; no history |
| D12 Algorithms/ML | 3, 8 | Traversers, Computer, Vermeer, HugeGraph-ML |
| D13 Retrieval/agents | 3, INV-03 | HG-LLM GraphRAG; MCP unreleased |
| D14 NL query | 3, 11 | text2gremlin (LLM) |
| D15 Governance | 5.6 | Async schema tasks; no review workflow |
| D16 Human experience | 3 | Hubble |
| D17 DevEx | 3 | Java, Go and Python clients; REST; Swagger annotations |
| D18 Trust/security | 5.10, 15 | Auth model, post-filter, Groovy risk |
| D19 Multi-tenancy | 5.10, 10, INV-02 | Graphs, graph spaces (PD), quotas |
| D20 Economics | 7 | Vendor claims only; EOIP amplification measured statically |
| D21 Commercial/licensing | 10 | Apache-2.0, no edition split; trademark note |
| D22 Interop/lock-in | 3, 11 | Gremlin standard; no RDF; export via tools |
| D23 IP/prior art | — | No HugeGraph patents identified in this run; NOT PUBLICLY VERIFIED |
| D24 Research quality | App. C | Source code at tags (high); performance unverified |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-01 | native | CLAIM-07, -08 | BL-02 Implemented/live-unverified | INTEGRATE | P0 |
| CAP-04 | native (RocksDB) | CLAIM-05 | compose single node | INTEGRATE | P1 |
| CAP-05 | native (HStore) | CLAIM-17 | HA compose placeholder | DEFER | P2 |
| CAP-06 | native | CLAIM-36 | BL-01 bulk_load | REUSE | P2 |
| CAP-07 | partial (sort keys, degree caps) | CLAIM-22 | Unknown | EXPERIMENT | P2 |
| CAP-08 | native (strict schema) | CLAIM-13 | BL-28 | INTEGRATE | P1 |
| CAP-13 | native | CLAIM-06, -21 | BL-02 | INTEGRATE | P1 |
| CAP-14 | partial | CLAIM-11, -12 | BL-03/04 | REJECT (dependency) | P2 |
| CAP-18 | absent (no CBO found) | §5.4 | — | DEFER | P3 |
| CAP-19 | native | CLAIM-22 | BL-08 | INTEGRATE | P1 |
| CAP-20 | absent | — | BL-09 Partial | BUILD | P1 |
| CAP-34 | absent | §5.9 | BL-37 Implemented | BUILD (keep) | P1 |
| CAP-45 | native (RBAC + targets) | CLAIM-14 | BL-19 | INTEGRATE | P1 |
| CAP-46 | partial (post-filter) | CLAIM-15 | BL-18 Absent | BUILD | P0 |
| CAP-47 | partial (PD-gated) | CLAIM-16, -39 | BL-20 Partial | INTEGRATE | P0 |
| CAP-50 | native | §10 | BL-45 | INTEGRATE | P0 |
| CAP-53 | absent (server) / plugin (HG-LLM) | CLAIM-09, -28 | BL-14 Partial | BUILD/REUSE | P1 |
| CAP-54 | partial (CJK) | CLAIM-10, -37 | BL-13 | EXPERIMENT | P2 |
| CAP-56 | plugin (HG-LLM) | CLAIM-28 | BL-16 | EXPERIMENT | P2 |
| CAP-57 | partial (TTL) | CLAIM-24 | Unknown | EXPERIMENT | P2 |
| CAP-58 | plugin | CLAIM-28 | BL-11/12 | EXPERIMENT | P2 |
| CAP-59 | unreleased | CLAIM-30 | BL-47 | DEFER | P3 |
| CAP-62 | native | CLAIM-22, -23, -27 | BL-43 | INTEGRATE | P2 |
| CAP-64 | plugin (HG-ML) | CLAIM-29 | BL-44 Partial | DEFER | P3 |
| CAP-70/71 | native (Hubble) | CLAIM-36 | BL-54 | REUSE | P2 |
| CAP-74 | native | CLAIM-26 | BL-50 | INTEGRATE | P1 |
| CAP-76 | native (HStore Raft) | CLAIM-17 | HA placeholder | DEFER | P2 |
| CAP-77 | Apache-2.0 | CLAIM-04 | — | INTEGRATE | P1 |

## Appendix C — Evidence records

All access dates are 2026-10-18. Abbreviations: OSC = Observed in source code, OD = Officially documented, RI = Reasoned inference, UV = Unverified. Repo URLs are `https://github.com/apache/<repo>/tree/1.7.0/<path>`.

| CLAIM-ID | Product / version | Exact claim | Class | Source | Pub / access | Conf | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-apache-hugegraph-01 | all repos 1.7.0 | Latest release 1.7.0, GitHub releases 2025-11-16; prior 1.5.0 (2024-12-10), 1.3.0, 1.2.0 | OD | GitHub releases API `api.github.com/repos/apache/hugegraph/releases` and `git ls-remote --tags` | 2025-11-16 / 2026-10-18 | 0.95 | Incubator page dates release news 2025-11-28 (announcement) |
| -02 | project | Graduated to TLP 2026-01-21; ASF announced 2026-02-12 | OD | https://incubator.apache.org/projects/hugegraph.html ; https://news.apache.org/foundation/entry/the-apache-software-foundation-announces-new-top-level-project-3 | 2026-02-12 | 0.95 | none |
| -03 | master | master revision 1.8.0, HEAD 90790e8 dated 2026-10-18; no 1.8.0 tag | OSC | `git ls-remote`, `pom.xml` on master | 2026-10-18 | 0.9 | none |
| -04 | 1.7.0 | Apache-2.0 LICENSE; DISCLAIMER (incubating) still in tag | OSC | `LICENSE`, `DISCLAIMER` at tag | 2025-11 | 0.95 | none |
| -05 | 1.7.0 | Legacy backends MySQL/PG/Cassandra etc. disabled; README: "mainly support RocksDB/HStore + HBase", others in ≤1.5.0 | OD | https://hugegraph.apache.org/docs/changelog/hugegraph-1.7.0-release-notes/ ; `README.md` | 2025/2026 | 0.85 | modules still present in source tree |
| -06 | 1.7.0 | Java 11 only; TinkerPop 3.5.1 | OD+OSC | release notes; `hugegraph-server/pom.xml:45` | — | 0.9 | none |
| -07 | 1.7.0 | RocksDB column family per HugeType incl. o/i edges, index tables, OLAP tables | OSC | `hugegraph-server/hugegraph-rocksdb/.../RocksDBTables.java` | — | 0.9 | none |
| -08 | 1.7.0 | Edge key = owner + dir + label + sublabel + sort-values + other vertex | OSC | `core/backend/serializer/BytesBuffer.java:733-743` | — | 0.9 | none |
| -09 | 1.7.0 + master | IndexType = SECONDARY, RANGE_*, SEARCH, SHARD, UNIQUE; no VECTOR | OSC | `core/type/define/IndexType.java`; master `hugegraph-struct/.../IndexType.java` | — | 0.9 | master IndexLabelAPI doc string mentions "VECTOR" |
| -10 | 1.7.0 | SEARCH analyzers: Ansj, HanLP, IK, Jcseg, Jieba, MMSeg4J, SmartCN | OSC | `core/analyzer/*` | — | 0.9 | none |
| -11 | 1.7.0 | Cypher endpoint translates via org.opencypher.gremlin translation 1.0.4 | OSC | `api/api/cypher/CypherAPI.java:49`; `api/opencypher/CypherOpProcessor.java`; `hugegraph-api/pom.xml:154` | — | 0.9 | none |
| -12 | cypher-for-gremlin | "not maintained anymore"; ~75 % TCK M13 on TinkerGraph | OD (3rd-party project) | https://github.com/opencypher/cypher-for-gremlin | — | 0.85 | repo not archived |
| -13 | 1.7.0 | EdgeLabel `links` (multiple source/target pairs), PARENT/SUB types in REST API | OSC | `api/api/schema/EdgeLabelAPI.java:194-262`; `core/schema/EdgeLabel.java:48-186` | — | 0.8 | live behaviour untested |
| -14 | 1.7.0 | Permissions NONE/READ/WRITE/DELETE/EXECUTE/SPACE/SPACE_MEMBER/ADMIN; roles space/space_member/analyst/observer; User/Group/Target/Belong/Access/Project/Role | OSC | `core/auth/HugePermission.java`, `HugeDefaultRole.java`, `api/api/auth/*` | — | 0.9 | none |
| -15 | 1.7.0 | Resources filter by label regex + property predicates; reads post-filtered by FilterIterator | OSC | `core/auth/HugeResource.java:189-219`; `api/auth/HugeGraphAuthProxy.java:1063-1084` | — | 0.85 | none |
| -16 | 1.7.0 | GraphSpace quotas fields; management branches on usePD; PD sets storage limit | OSC | `core/space/GraphSpace.java:43-67`; `api/core/GraphManager.java:279,834,1230,1984` | — | 0.75 | non-PD semantics not fully traced |
| -17 | 1.7.0 | HStore: RocksDB + JRaft, hash partitions, partition = Raft group, pushdown | OD | `hugegraph-store/README.md:10-71` | — | 0.85 | none |
| -18 | 1.7.0 | Compose for 3 PD + 3 Store + 3 Server shipped | OSC | `docker/docker-compose-3pd-3store-3server.yml` | — | 0.9 | none |
| -19 | 1.7.0 | Thread-local tx; tx capacity limits; LocksTable for schema delete | OSC | `core/StandardHugeGraph.java:1636`; `core/backend/tx/GraphTransaction.java:141-176,629,2105` | — | 0.85 | isolation level undocumented |
| -20 | 1.7.0 | Ram/Offheap/Level caches with CacheNotifier; notifier fix in 1.7.0 | OSC+OD | `core/backend/cache/*`; release notes #2729 | — | 0.85 | none |
| -21 | 1.7.0 | Optimisation strategies HugeGraphStep/VertexStep/Count/PrimaryKey | OSC | `core/traversal/optimize/*` | — | 0.85 | index-selection order is hypothesis |
| -22 | 1.7.0 | ~25 REST traversers (kout, kneighbor, shortest/weighted/all paths, rings, rays, personal rank, jaccard…) | OSC | `api/api/traversers/*` | — | 0.9 | none |
| -23 | 1.7.0 | Algorithm and computer job APIs, server-side algorithms | OSC | `api/api/job/AlgorithmAPI.java`, `ComputerAPI.java`, `core/job/algorithm/*` | — | 0.85 | none |
| -24 | 1.7.0 | TTL and ttl_start_time on vertex and edge labels | OSC | `EdgeLabelAPI.java:216-218`; `core/schema/VertexLabel.java:130-153` | — | 0.85 | none |
| -25 | 1.7.0 | OLAP tables per OLAP property key | OSC | `RocksDBTables.java:392-411`; `HugeType.OLAP` | — | 0.8 | none |
| -26 | 1.7.0 | Snapshot SPI; tools commands backup/restore/dump/migrate/graph-clone/schedule-backup | OSC | `core/backend/store/BackendStore.java:180-185`; `hugegraph-toolchain/hugegraph-tools/.../cmd/SubCommands.java` | — | 0.85 | none |
| -27 | computer 1.7.0 | Computer (k8s, k8s-operator, yarn modules) and Vermeer (Go, in-memory, 15+ algorithms) migrated into repo | OSC+OD | `hugegraph-computer/computer/*`, `vermeer/README.md`; release notes #316 | — | 0.85 | none |
| -28 | ai 1.7.0 | HugeGraph-LLM: KG build, NL→Gremlin/Cypher, GraphRAG/Agent; LiteLLM; Faiss/Milvus/Qdrant stores; Gradio | OSC+OD | `hugegraph-llm/README.md`; `src/hugegraph_llm/indices/vector_index/*` | — | 0.85 | none |
| -29 | ai 1.7.0 | HugeGraph-ML: 21 models on DGL + torch | OSC | `hugegraph-ml/src/hugegraph_ml/models/*`, `pyproject.toml` | — | 0.9 | none |
| -30 | ai master | MCP toolsets on master (commit 84ee9c4, 2026-10-13) | OSC (commit message only) | `git log` FETCH_HEAD of apache/hugegraph-ai | 2026-10-13 | 0.5 | not in any release |
| -31 | vendor | ">10 billion vertices & edges"; "hundreds of billions … millisecond-level latency" | UV (vendor claim) | `README.md`; ASF announcement | — | 0.2 | no workload/hardware |
| -32 | 1.7.0 | Production must enable AuthSystem; auth commented out in default rest-server.properties | OD+OSC | `README.md`; `hugegraph-dist/.../conf/rest-server.properties:23-33` | — | 0.9 | Docker `PASSWORD` enables auth |
| -33 | 1.7.0 | Docker images are convenience releases, not official ASF artifacts | OD | `README.md` | — | 0.9 | none |
| -34 | 1.7.0 | Login token expiry added; graph removed from auth API path | OD | release notes #2754, #2899 | — | 0.8 | none |
| -35 | 1.7.0 | RocksDB 7.2.2 → 8.10.2 | OD | release notes #2896 | — | 0.85 | none |
| -36 | toolchain 1.7.0 | Modules: client, client-go, hubble, loader, spark-connector, tools; graphspace support | OSC+OD | repo tree at tag; release notes #633 | — | 0.9 | none |
| -37 | 1.7.0 | Enum comment says SEARCH "not supported now" | OSC | `IndexType.java` | — | 0.8 | analyzers exist (CLAIM-10) |
| -38 | 1.7.0 | Legacy raft store mode in core | OSC | `core/backend/store/raft/` | — | 0.5 | support status unknown |
| -39 | EOIP HEAD | Adapter fixed to `/graphspaces/DEFAULT`, admin basic auth, Gremlin alias `__g_DEFAULT-{g}`, no cypher/traversers/auth/TTL calls | OSC (EOIP) | `packages/eoip/graph/hugegraph.py:31-38,545-555`; `config/graph-store.yaml:14-19` | 2026-10-18 | 0.9 | none |
| -40 | EOIP HEAD | Generated schema: 250 property keys, 75 vertex labels, 677 edge labels, 1,005 index labels | OSC (computed) | `HugeGraphStore._schema_definitions()` run locally | 2026-10-18 | 0.95 | none |
| -41 | EOIP HEAD | HA compose calls PD/Store "enterprise/infra images", uses `:latest` | OSC (EOIP) | `deploy/docker-compose.ha.yml:11,128-170` | 2026-10-18 | 0.95 | CLAIM-17/-18 show OSS |
| -42 | EOIP HEAD | find/count page all vertices/edges in Python; Groovy closure filter; indexes only UNIQUE/SECONDARY | OSC (EOIP) | `hugegraph.py:363-410,504-528`; `ontology/manifest.py:455-476` | 2026-10-18 | 0.9 | none |

## Appendix D — Assumptions

1. "Latest" means the latest Apache release tag (1.7.0). master 1.8.0 work is reported only as drift.
2. Release notes on the docs site are authoritative despite the "WIP/BETA" banner, because they match the tags and commit history.
3. Lines cited for reasoning about index selection and RocksDB write-batch atomicity are hypotheses from class roles. They were not traced line by line.
4. EOIP's customised Hubble image counts as reuse of the upstream Hubble; its white-label compliance is out of scope here.
5. The slug in IDs is `apache-hugegraph`. The self-inversion is named `INV-SELF-HG-01` to avoid colliding with other workers' `INV-SELF-NN`.
6. The GitHub REST API was rate-limited during this run; tags and code were read via `git ls-remote` and shallow clones at the tags.
