# Cohort 01: Property-graph and multi-model engines (candidate EOIP backends)

| Field | Value |
|---|---|
| Cohort ID | COH-01-LPG |
| Workload class | System-of-record storage and traversal for the KnowGridFlow instance graph (CAP-01..08, 13..20, 45..47, 50, 53..54, 62, 74..77) |
| Date | 2026-10-26 (deep dives verified 2026-10-18 and 2026-10-26) |
| EOIP reference | BL-IDs at `ad9937b` ([01-SYSTEM-BASELINE.md](../01-SYSTEM-BASELINE.md)) and status at HEAD `896e06d` ([01a-BASELINE-DELTA-HEAD.md](../01a-BASELINE-DELTA-HEAD.md)); HEAD wins where they differ |
| Reference columns | HugeGraph, Neo4j, Neptune (the three required backends) and EOIP @HEAD |
| Supported backends (adapter exists, BL-02..05) | [Apache HugeGraph](../04-COMPETITOR-DEEP-DIVES/C01-apache-hugegraph.md), [Neo4j](../04-COMPETITOR-DEEP-DIVES/C01-neo4j.md), [Amazon Neptune](../04-COMPETITOR-DEEP-DIVES/C01-amazon-neptune.md), [JanusGraph](../04-COMPETITOR-DEEP-DIVES/C01-janusgraph.md) |
| Candidate engines (no adapter) | [Memgraph](../04-COMPETITOR-DEEP-DIVES/C01-memgraph.md), [FalkorDB](../04-COMPETITOR-DEEP-DIVES/C01-falkordb.md), [TigerGraph](../04-COMPETITOR-DEEP-DIVES/C01-tigergraph.md), [ArangoDB](../04-COMPETITOR-DEEP-DIVES/C01-arangodb.md), [ArcadeDB](../04-COMPETITOR-DEEP-DIVES/C01-arcadedb.md), [Kuzu](../04-COMPETITOR-DEEP-DIVES/C01-kuzu.md), [NebulaGraph](../04-COMPETITOR-DEEP-DIVES/C01-nebulagraph.md), [Apache AGE](../04-COMPETITOR-DEEP-DIVES/C01-apache-age.md), [TypeDB](../04-COMPETITOR-DEEP-DIVES/C01-typedb.md), [TerminusDB](../04-COMPETITOR-DEEP-DIVES/C01-terminusdb.md), [Dgraph](../04-COMPETITOR-DEEP-DIVES/C01-dgraph.md), [GraphScope](../04-COMPETITOR-DEEP-DIVES/C01-graphscope.md), [Oracle Graph](../04-COMPETITOR-DEEP-DIVES/C01-oracle-graph.md), [Spanner Graph](../04-COMPETITOR-DEEP-DIVES/C01-spanner-graph.md), [PuppyGraph](../04-COMPETITOR-DEEP-DIVES/C01-puppygraph.md), [Azure Cosmos DB Gremlin](../04-COMPETITOR-DEEP-DIVES/C01-azure-cosmos-db-gremlin.md) |
| Query-language conformance | [C12 TinkerPop](../04-COMPETITOR-DEEP-DIVES/C12-tinkerpop.md) |
| Tier C context | [C01-tier-c-records](../04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md) (placeholder, no CLAIMs), [V01](../04-COMPETITOR-DEEP-DIVES/C01-tier-c-records-V01.md), [V15](../04-COMPETITOR-DEEP-DIVES/C01-tier-c-records-V15.md) |
| Members | 20 deep dives with CLAIM records (4 supported, 16 candidate), 1 conformance reference, 11 Tier C records |

CLAIM shorthand in table cells: only the numeric suffix is given and the prefix comes from the column header (for example HugeGraph `-07` means CLAIM-apache-hugegraph-07). Prefixes: HG `CLAIM-apache-hugegraph-`, N4 `CLAIM-neo4j-`, NP `CLAIM-amazon-neptune-`, JG `CLAIM-janusgraph-`, MG `CLAIM-memgraph-`, FK `CLAIM-falkordb-`, TG `CLAIM-tigergraph-`, AR `CLAIM-arangodb-`, AC `CLAIM-arcade-`, KZ `CLAIM-kuzu-`, NB `CLAIM-nebula-`, AGE `CLAIM-age-`, TY `CLAIM-typedb-`, TM `CLAIM-terminus-`, DG `CLAIM-dgraph-`, GS `CLAIM-graphscope-`, OR `CLAIM-oracle-`, SP `CLAIM-spanner-`, PG `CLAIM-puppygraph-`, CZ `CLAIM-azure-cosmos-db-gremlin-`, TP `CLAIM-tp-`. "§n" means a section of that deep dive without a CLAIM row.

## 1. Workload class and comparison basis

**Workloads served.** The EOIP instance graph holds typed entities and relationships produced by the governed ingest pipeline (§4.3 item 4). The backend must support ID-keyed upserts and tombstones (BL-01, BL-25), neighbourhood and multi-hop reads for retrieval and impact analysis (BL-08, BL-16, BL-43), bulk load, and operation on one node first (§4.3 item 10). Tenant and source-ACL enforcement must survive the backend (§4.3 items 8 and 9).

**Why comparable.** Every member stores labelled property graphs (or maps them onto relational tables, Oracle, Spanner, AGE, PuppyGraph), is reachable over a network or embedded API, and could sit behind the `GraphStore` protocol (BL-01).

**Excluded and why.**
- RDF stores and reasoners: cohort 02. Ontology tools: cohort 03.
- Vector engines (C10), graph ML (C11) and in-memory algorithm libraries (C12 except TinkerPop): different workload class.
- Tier C records are context only, none gets a table column: RedisGraph is EOL (CLAIM-redisgraph-01); TuGraph, Ultipa, SAP HANA Graph, Aerospike Graph, Galaxybase are reference-only (CLAIM-tugraph-01, CLAIM-ultipa-01, CLAIM-sap-hana-graph-01, CLAIM-aerospike-graph-01, CLAIM-galaxybase-01); SurrealDB is BSL (CLAIM-surrealdb-01); CozoDB is dormant (CLAIM-cozodb-01); HelixDB is young (CLAIM-helixdb-01); OrientDB is maintained but low momentum (CLAIM-orientdb-01). DuckPGQ is the one Tier C item worth an experiment (CLAIM-duckpgq-01).
- Managed-only services (Neptune, Cosmos, Spanner) are compared as optional customer-requested backends or references, never as defaults (§4.3 item 1).

## 2. Capability comparison

### 2.1 Supported backends vs EOIP @HEAD

| CAP | HugeGraph (HG) | Neo4j (N4) | Neptune (NP) | JanusGraph (JG) | EOIP @HEAD |
|---|---|---|---|---|---|
| CAP-01 property-graph storage | native, RocksDB or HStore -05, -17 | native, aligned format; block format is enterprise-only -18 | native; 3 fixed quad indexes, no user indexes -11, -12 | native over Cassandra/HBase/Scylla -04, -06 | `GraphStore` + 4 adapters, live-unverified (BL-01..05) |
| CAP-04 one-node footprint | native, 1 container -05 | native, CE or EE single instance -05 | absent, managed only -08 | partial: BerkeleyJE/in-memory on one JVM, distributed store is heavy -04 | compose runs HugeGraph 1.7.0 + Neo4j 5 CE (BL-01) |
| CAP-05 scale-out | native HStore (PD + Store) -17 | enterprise-only Raft cluster; Infinigraph sharding -16, -06 | partial: 1 writer + 15 replicas, no sharding -14 | native via storage backend -04 | not applicable; HA compose files exist, pins `:latest` (HG §10) |
| CAP-06 bulk load | native batch API, Loader -36 | native `neo4j-admin import`; EOIP uses one request per entity -38 | native S3 loader, not ACID -15 | partial; adapter loads per item -09 | `bulk_load` exists; per-item on Neo4j/Neptune (BL-01) |
| CAP-07 supernodes | partial: sort keys, degree caps -22 | partial: dense-node trees -18 | partial: optional OSGP index, gap-lock contention -11, -10 | native vertex-centric indexes -06 | unknown |
| CAP-08 schema/constraints | native strict schema -13 | CE uniqueness only; existence/type/key and GRAPH TYPE enterprise-only -22, -23 | absent, ID uniqueness only -12 | native schema management -06 | gateway label/required-property check (BL-28) |
| CAP-13 Gremlin | native, TinkerPop 3.5.1 -06 | unknown (not in feature inventory) | native with deviations, no bindings -03 | native, TinkerPop 3.7.3 -02 | adapters HugeGraph/Neptune/Janus (BL-02/04/05) |
| CAP-14 Cypher/GQL | partial: unmaintained translator to Gremlin -11, -12 | native Cypher 5/25; GQL partial -07, -08 | native openCypher with deviations, no `CALL`/`shortestPath` -04 | unknown -04 | Neo4j/Neptune adapters (BL-03/04); AST compiler emits text, library-only (BL-09) |
| CAP-15 SPARQL | absent (reasoned, §3) | absent natively; n10s is Labs -31 | native SPARQL 1.1, isolated RDF mode -06, -26 | absent (§3) | Fuseki/GraphDB adapters Implemented (BL-06); SPARQL backends library-only, not mounted (BL-06a) |
| CAP-16 SQL/PGQ, GQL | absent (§3) | partial GQL -08 | absent -12 | absent (§3) | Partial, library-only (BL-59) |
| CAP-18 optimiser/EXPLAIN | absent, no CBO found (hypothesis, §5.4) | native CBO, EXPLAIN/PROFILE -05, -07 | partial: explain, hints -04, -34 | partial -06 | none in protocol; templates only (BL-08) |
| CAP-19 multi-hop | native REST traversers -22 | native -05 | native | native -06 | emulated in Python via protocol (BL-08, BL-43) |
| CAP-34 bitemporal | absent (§5.9) | absent -17 | absent -14 | absent (§3) | Implemented, application layer (BL-37) |
| CAP-45 RBAC | native, optional auth -14 | enterprise-only -14 | partial: per-action IAM -09 | partial: authentication only -07 | Implemented at API layer (BL-19) |
| CAP-46 source-ACL | partial: post-filter -15 | enterprise-only, one property per rule, fails open -15 | absent -12 | absent -07 | Partial: evaluator exists, not applied on deployed retrieval paths (BL-18) |
| CAP-47 tenant isolation | partial: graphs; spaces need PD -16, -39 | enterprise-only DB-per-tenant -13 | partial: one graph per cluster -12 | absent -07 | Partial: embedded layers isolated, adapters contain zero tenant code (BL-20) |
| CAP-50 air-gap | native | native, usage report must be disabled -30 | absent -08 | native -04 | local model default (BL-45) |
| CAP-53 vector | absent in server; Faiss/Milvus/Qdrant via HG-LLM -09, -28 | native HNSW (CE: list properties) -09 | Neptune Analytics only -19 | absent -04 | Partial: hashing embedder, pure-Python HNSW (BL-14) |
| CAP-54 full-text | partial, CJK analyzers -10, -37 | native Lucene, `SEARCH` -10 | plugin, OpenSearch -16 | plugin, Elasticsearch/Solr/Lucene -04 | in-process BM25 (BL-13) |
| CAP-62 algorithms | native traversers, Computer, Vermeer -22, -27 | plugin GDS; CE capped at 4 cores -24 | Neptune Analytics only -18 | partial OLAP via Hadoop/Spark (§3) | Implemented in-process (BL-43, NB-01) |
| CAP-74 backup/PITR | native snapshot + tools -26 | online/PITR enterprise-only -17 | native snapshots, PITR -14, -26 | backend-level (§3) | scripts, live-unverified (BL-50) |
| CAP-76 HA/DR | native HStore Raft -17 | enterprise-only -16 | native -26 | via backend | HA compose, unverified (BL-50) |

### 2.2 Candidate engines (selected CAPs)

| CAP | Memgraph (MG) | FalkorDB (FK) | TigerGraph (TG) | ArangoDB (AR) | ArcadeDB (AC) | Kuzu (KZ) | NebulaGraph (NB) |
|---|---|---|---|---|---|---|---|
| CAP-01/03 model | native in-memory LPG -13 | native, sparse-matrix on Redis -08 | native MPP, schema-first -07, -02 | native multi-model, AQL -11 | native multi-model -01 | native columnar CSR -06 | native over RocksDB -03 |
| CAP-04 one node | native, RAM-bound -12 | partial: RAM, single process -13 | partial: CE single server -03 | unknown (single-server mode listed, §10) | native, embedded JVM -01 | native, embedded -05 | partial: 3 services, oversized (§9) |
| CAP-05 scale-out | partial: replicas; HA enterprise-only; no sharding -17, -18 | partial: graph per shard -12 | enterprise-only -08 | native sharding -12 | partial: Raft HA, detail unverified -01 | absent -05 | native Raft -03 |
| CAP-08 constraints | partial -23 | partial: unique -17 | native -02 | unknown | unknown | native typed tables -06 | native tags/edge types (§3) |
| CAP-13/14/16 languages | Cypher native dialect; no GQL/Gremlin -23 | openCypher + extensions; no Gremlin -14 | GSQL; Cypher/GQL patterns partial; Gremlin unverified -06, -07 | AQL only; no Cypher/Gremlin (§3) | SQL, Cypher, Gremlin, GraphQL; Cypher completeness unverified -01 | Cypher dialect; no TCK result -05 | nGQL + openCypher subset -01 |
| CAP-18 optimiser | partial -24 | partial -08 | native profiler -12 | unknown | unknown | native WCO joins -07 | unknown |
| CAP-45/46 RBAC, ACL | enterprise-only RBAC/LBAC/PBAC; vector results silently truncated -07, -29, -21 | unknown: only `requirepass` found -13 | enterprise-only RBAC, row policy -08 | unknown | users/groups/tokens; no source-ACL -01 | absent (inference) | native RBAC; no row ACL -03 |
| CAP-47 tenancy | enterprise-only DB-per-tenant, memory caps -19, -20 | partial: graph-per-key, claimed >10,000 graphs -12, -15 | unknown -08 | unknown | absent -01 | absent (inference) | absent beyond RBAC -03 |
| CAP-53/54 vector, FTS | native / native -21, -22 | native HNSW (no property filter combine) / native -09, -04 | native from 4.2 / unknown -05 | native Faiss / native ArangoSearch -10, -08 | native / present -01 | extension / extension -05 | unknown / ES listener, unverified (§3) |
| CAP-62 algorithms | native MAGE, BSL since 3.8 -30, -06 | partial; Leiden/Louvain not ported to v6 -04 | native -07 | unknown | unknown | partial -06 | unknown |

### 2.3 Other candidates (summary)

| Member | Distinct angle | Query | Tenancy/ACL | Vector/FTS | Air-gap |
|---|---|---|---|---|---|
| Apache AGE | graph in PostgreSQL | openCypher partial, hybrid SQL (AGE-03) | RLS since 1.7.0, traversal semantics unproven (AGE-04, conf 0.6) | via pgvector/tsvector, not AGE-native (§3) | yes (§10) |
| TypeDB | strong typing, n-ary relations | TypeQL only (TY-03) | unknown | unknown | yes, CE |
| TerminusDB | git-like branch/diff/merge | WOQL, GraphQL (TM-02) | unknown | vector preview in 12.1-rc (§3) | yes |
| Dgraph | GraphQL-native | GraphQL, DQL (DG-03) | namespaces; ACL "upcoming" (DG-03) | unverified | yes; licence unresolved (DG-03) |
| GraphScope | analytics + LDBC-audited Interactive | Cypher, Gremlin (GS-02) | not found (§3) | not found (§3) | yes |
| Oracle Graph | SQL/PGQ in RDBMS | SQL/PGQ, PGQL (OR-01) | inherited DB security (OR-01) | not examined | customer-installed |
| Spanner Graph | GQL + SQL in managed DB | GQL (SP-01, SP-02) | Spanner IAM (not examined) | vector + FTS (SP-01) | no, managed only |
| PuppyGraph | zero-ETL virtual graph over SQL/lake | Gremlin, openCypher (PG-01) | source-side RLS guidance; SSO enterprise-only (PG-02) | unverified | partial (PG-02) |
| Cosmos DB Gremlin | managed, document-backed | Gremlin text, GraphSON v2 only (CZ-03) | keys, resource tokens (CZ-06) | not offered | no (CZ-04) |

## 3. Operational and licensing comparison

| Member | Licence class | Redistribution / OEM trigger | Air-gap | Maintenance (as read) |
|---|---|---|---|---|
| HugeGraph | Apache-2.0, no edition split (HG-04) | Low; ASF trademark and Docker images are convenience builds (HG-33) | yes | 1.7.0 (2025-11-16), ASF TLP, ~1 release a year (HG-01, -02) |
| Neo4j | CE GPLv3; EE commercial; GDS CE GPLv3 plus closed parts (N4-04, -24) | **Trigger**: bundling CE; EE OEM terms not public; NVL needs review (N4-33) | yes, set `usage_report.enabled=false` (N4-30) | monthly CalVer; 5.26 LTS to 2028-06-06 (N4-02) |
| Neptune | proprietary managed (NP §9) | Commercial review if reselling | **no** (NP-08) | engine 1.5.0.0 (2026-10-13) (NP-01) |
| JanusGraph | Apache-2.0 (JG-04) | Low; storage/index dependencies drive risk (§10) | yes | stable 1.1.0 (2024-11); 1.2.0 pre-release; 507 open issues (JG-01, -08) |
| Memgraph | BSL 1.1 + MEL; 2026 grant forbids embedding/distribution (MG-04) | **High trigger**; MAGE moved from Apache-2.0 to BSL (MG-06) | yes (key offline-capable unverified) | monthly (MG-02) |
| FalkorDB | SSPLv1 core (FK-01) | **Trigger**; "as a service" rules (FK §10) | yes | two lines v6.0.3 and v4.22.2 (FK-03, -04) |
| TigerGraph | proprietary; CE internal-use only, 300 GB, no third-party use (TG-03, -04) | **Likely blocker** | partial, offline licence unverified (TG-09) | 4.2.5 LTS; 4.3 preview (TG-01) |
| ArangoDB | BUSL-1.1 source; Community binaries 100 GiB, internal use (AR-02, -04) | **Trigger: yes** | technically yes | 3.12.12 (AR-05) |
| ArcadeDB | Apache-2.0 (AC-01) | Low | yes | 26.10.2 (2026-10-15), ~1.2k stars (AC-02) |
| Kuzu | MIT (KZ-03) | Operational: archived 2025-10-10 (KZ-01); LadybugDB is the live fork (KZ-12) | core yes; extensions need self-hosted server (KZ-04) | **archived** |
| NebulaGraph | Apache-2.0 core (NB-01) | Low; enterprise modules unverified | yes (unverified) | last release 2024-05-17 (NB-02) |
| Apache AGE | Apache-2.0 (AGE-02) | Low | yes | 1.8.0-rc0 tags; GA unverified (AGE-02) |
| TypeDB | MPL-2.0 CE (TY-01) | file-level copyleft review | yes | 3.14.1 (2026-10-22) |
| TerminusDB | Apache-2.0 (TM-01) | Low | yes | 12.0.8 (2026-10-12); maintainer transition (TM-02) |
| Dgraph | Apache-2.0 vs Community License conflict (DG-03) | **Trigger** until resolved | yes | v25.5.1; 2 ownership changes (DG-01, -02) |
| GraphScope | Apache-2.0 (GS-01) | Low | yes | no GitHub release since 2025-01-27 (GS-04) |
| Oracle / Spanner / Cosmos / PuppyGraph | proprietary (OR-04, SP-01, CZ-01, PG-03) | cannot be bundled | Oracle customer-installed; PuppyGraph partial; Spanner and Cosmos no | Cosmos de-emphasised (CZ-01) |

## 4. Performance evidence

No row below supports a ranking: no two figures share workload, dataset and hardware.

| Source | Workload and hardware | Class | Use |
|---|---|---|---|
| GraphScope Flex 0.31.3 (GS-03) | LDBC SNB Interactive, SF30/100/300, single instance, Cypher, FDR 2025-04-21 | independent audit | Only audited figure in the cohort. Blog says >80,000 QPS, docs say 33,180.87 ops/s; unreconciled, no number adopted |
| Galaxybase (CLAIM-galaxybase-01) | LDBC SNB Interactive SF30/100/300, 2022-05 | independent audit, Tier C | Context only; later report not opened |
| TigerGraph vs Neo4j (TG-11) | arXiv:1907.07405, LDBC SNB, 2019, vendor-tuned; Neo4j finished 12 of 25 BI queries in 5 h | academic, vendor-involved | 2019 code; not current |
| FalkorDB (FK-16) | 496x lower P99 vs Neo4j (820K nodes/9.8M edges, setup unpublished); Dec-2024 blog 136.2 ms vs 46,923.8 ms on SNAP Pokec, 16 CPU/32 GB | vendor | Two multipliers disagree; predates the Rust engine |
| Memgraph (MG-28, MG-32) | benchgraph (Memgraph 2.4 vs Neo4j 5.1), later 3.16x single-hop; AIMultiple 2026 synthetic test favours FalkorDB at 8 threads (confidence 0.4) | vendor, third-party | "120x" claim superseded |
| Neo4j (N4-10) | rescored binary quantisation "about 5X" latency | vendor | No dataset or hardware |
| HugeGraph (HG-31) | ">10 billion elements", "millisecond latency" | vendor | No workload; no LDBC result found |
| Neptune (NP-36) | "100,000 queries per second" | vendor | No workload; no audited LDBC result found |
| PuppyGraph (PG-04) | "10 hops in 2 seconds" on MotherDuck/DuckDB | vendor | Hardware not stated |
| Kuzu (KZ-07) | CIDR 2023 paper, WCO joins | academic | Applies to 2023 code; fork claim "374x" unverified (KZ-16) |

**No comparable evidence exists** for HugeGraph, Neo4j (2026.x), Neptune or JanusGraph under the §12 protocol. BM-01..BM-06 remain PROPOSED.

**EOIP-side cost models (reasoned from code, not measured).** Neo4j adapter: 3 HTTP calls per edge (N4-37, -38). Neptune: N + 3M sequential requests, about 2.8 h for 1M vertices and 3M edges at 1 ms (NP §7). HugeGraph adapter: 75 vertex labels, 677 edge labels, 1,005 index labels (HG-40). These adapter files are unchanged at HEAD (BL-02..05).

## 5. Findings

1. **No audited benchmark exists for any supported backend.** HugeGraph, Neo4j, Neptune and JanusGraph deep dives found only vendor claims (HG-31, N4-10, NP-36, JG §7). Falsified by an audited LDBC SNB report for any of the four. Only GraphScope (GS-03) and Galaxybase (CLAIM-galaxybase-01) have one.
2. **Tenancy and source-ACL primitives are missing, gated or coarse on every engine.** DB-per-tenant is enterprise-only on Neo4j (N4-13) and Memgraph (MG-19); HugeGraph needs PD (HG-16); Neptune is one graph per cluster (NP-12); JanusGraph has none (JG-07). The only storage-level row policy found is AGE's RLS, with unproven traversal semantics (AGE-04). EOIP adapters still hold zero tenant code (BL-20 at HEAD). Falsified by any engine whose native policy filters traversal results by source ACL in a test.
3. **Redistribution splits the field.** Of the 20 deep-dive members: 7 are Apache-2.0 (HugeGraph, JanusGraph, ArcadeDB, AGE, NebulaGraph, TerminusDB, GraphScope); Kuzu is MIT and TypeDB MPL-2.0; Dgraph is unresolved (DG-03); 5 are copyleft, source-available or restricted (Neo4j CE, Memgraph, FalkorDB, ArangoDB, TigerGraph CE); 5 are proprietary or managed (Neptune, Cosmos, Oracle, Spanner, PuppyGraph). Only the first group can be bundled without a legal-review trigger. Falsified by a licence change or a negotiated OEM grant.
4. **One query text cannot run unmodified on all supported backends.** Neptune has no Gremlin bindings and no `CALL` (NP-03, -04); HugeGraph's Cypher is a Gremlin translation over an unmaintained library (HG-11, -12); JanusGraph 1.2.0 moves to TinkerPop 3.8 with breaking semantics (JG-02); TinkerPop 4.0 beta removes bytecode (TP-05); provider conformance is uneven (TP-11). Falsified by one conformance suite passing byte-identical on all four.
5. **Vector support is native in most candidates but absent in two supported backends.** Native: Neo4j, Memgraph, FalkorDB, TigerGraph, ArangoDB, ArcadeDB. Absent from the HugeGraph server (HG-09), JanusGraph (JG-04) and Neptune Database (NP-19). FalkorDB filters vectors after the search (FK-09); Memgraph truncates results silently under ACL (MG-21). So vector search stays a backend-neutral sidecar with ACL pre-filtering. Falsified by a native vector index with pre-filtering by an ACL predicate.
6. **Three managed engines fail the air-gap constraint.** Neptune (NP-08), Cosmos (CZ-04) and Spanner (SP-01) are cloud-only. Neo4j reports usage by default (N4-30) and Kuzu extensions need a self-hosted server since the archive (KZ-04).
7. **The biggest defects on supported backends are in EOIP's adapters, not the engines.** Neo4j's HTTP transactional API is deprecated in 5.26 (N4-11); Neptune IAM SigV4 has no code path (BL-04, U-03 resolved negatively); HugeGraph adapter label explosion (HG-40); JanusGraph property prefix mismatch and no-op schema creation (JG-09). Falsified by a live conformance run (BL-07, U-01) that passes without these changes.
8. **Maintenance risk is concentrated in the permissive candidates.** Kuzu archived 2025-10-10 (KZ-01), NebulaGraph no release since 2024-05 (NB-02), GraphScope none since 2025-01 (GS-04), JanusGraph 23 months between stable releases (JG-01), AGE only rc tags (AGE-02), Cosmos de-emphasised (CZ-01). ArcadeDB (AC-02), TerminusDB (TM-01) and HugeGraph (HG-03) are active. Falsified by new stable releases.
9. **Standards-based graph query is thin in the cohort.** SQL/PGQ or GQL is native only in Oracle (OR-01) and Spanner (SP-02), partial in Neo4j (N4-08) and TigerGraph patterns (TG-06), research-only in DuckPGQ (CLAIM-duckpgq-01). EOIP has a typed AST compiler that is library-only and a regex-based plan engine with mock rows when no executor is passed (BL-09, BL-09a, BL-59).
10. **Several differentiators are cheap to adopt as patterns, not engines.** Path-mode vocabulary from Spanner (SP-03), vertex-centric index policy from JanusGraph (JG-06), typed constraints from TypeDB (TY-03), branch/merge semantics from TerminusDB (TM-02).

## 6. Implications for EOIP

Backend neutrality (§4.3 item 3): "available upstream / not integrated" means the supported engine already offers it.

| CAP | Parity needed (STR) | Exploitable weakness (INV) | Decision | Candidate gap statement |
|---|---|---|---|---|
| CAP-20 portable IR | STR-tigergraph-04 (standard patterns into typed plans) | INV-apache-hugegraph-01, INV-amazon-neptune-04, INV-tinkerpop-02 | BUILD | Interoperability: `ASTCompiler` (BL-09) is not on the production path and no dialect profile exists per backend |
| CAP-08 constraints | STR-neo4j-03 (GRAPH TYPE) | INV-neo4j-01, INV-amazon-neptune-03 | BUILD gateway contract; INTEGRATE GRAPH TYPE where present | Partial: BL-28 lacks cardinality, value-range, role constraints; Neo4j GRAPH TYPE and HugeGraph schema are available upstream / not integrated |
| CAP-47 tenancy | STR-neo4j-07, STR-memgraph-03, STR-falkordb-02, STR-apache-hugegraph-03 | INV-neo4j-02, INV-amazon-neptune-02 | BUILD placement modes in the adapter; INTEGRATE native tenancy per backend | Security (P0): adapters carry no tenant code (BL-20); HugeGraph graph spaces and Neo4j databases are available upstream / not integrated |
| CAP-46 source-ACL | STR-neo4j-05 (as defence in depth) | INV-neo4j-03, INV-apache-hugegraph-02, INV-memgraph-02 | BUILD | Security (P0): ACL evaluator not applied on keyword/vector/hybrid retrieval (BL-18) |
| CAP-06 bulk load | STR-amazon-neptune-06 | none | BUILD batching; INTEGRATE S3 loader (opt-in) | Performance: per-item requests on Neo4j/Neptune/Janus (BL-01) |
| CAP-19 multi-hop pushdown | STR-neo4j-01, STR-apache-hugegraph-02, STR-memgraph-01 | INV-azure-cosmos-db-gremlin-01 | INTEGRATE (pushdown hook) | Performance: traversal runs in Python (BL-08); REST traversers and Cypher paths are available upstream / not integrated |
| CAP-53 vector | STR-neo4j-02, STR-falkordb-03, STR-tigergraph-02 | INV-falkordb-02, INV-memgraph-02, INV-apache-hugegraph-03 | INTEGRATE optional per backend; keep sidecar default | Partial: no external vector DB (BL-14); needs ACL pre-filter |
| CAP-18 optimiser | STR-tigergraph-03 | none | DEFER | Pass EXPLAIN through; no gap until pushdown exists |
| CAP-35/37 versioning | n/a | TerminusDB branch/merge (TM-02) | EXPERIMENT | Research gap for instance-graph branches |
| CAP-50 air-gap | STR-neo4j-* config only | INV-amazon-neptune-01 | INTEGRATE (config); REJECT Neptune/Cosmos/Spanner as defaults | Operability: document the matrix |
| CAP-77 licence | n/a | INV-memgraph-01, INV-arangodb-01, INV-falkordb-03, INV-tigergraph-01 | BUILD licence gate (SBOM CI) | Operability: `compliance/sbom.py` is library-only (NB-14) |
| Candidate backends | n/a | INV-kuzu-01, INV-kuzu-02 | ArcadeDB, AGE: EXPERIMENT; Nebula: DEFER; Kuzu/LadybugDB: EXPERIMENT (embedded only); TigerGraph, Memgraph, FalkorDB, ArangoDB, Dgraph: REJECT bundling, optional customer-supplied only | Competitive deficit: no engine passes conformance (BL-07) |

## 7. Open questions

1. Does the EOIP conformance suite (BL-07) pass on a live HugeGraph 1.7.0, Neo4j 5.26 and Neptune? (U-01)
2. Which supported backends can use native tenant primitives (HugeGraph graph per tenant, Neo4j EE database per tenant) without breaking the `GraphStore` contract?
3. Is Neo4j CE GPLv3 acceptable as a customer-supplied, network-accessed dependency? Legal review (N4-04).
4. Does AGE's RLS filter multi-hop traversal and `MERGE` results (AGE-04)?
5. Can the EOIP Neo4j adapter run unmodified against ArcadeDB over Bolt, and what is ArcadeDB's openCypher coverage (AC-01, completeness unverified)?
6. When does the next LTS (Neo4j 2026.LTS) land, and does it still serve the HTTP transactional API (N4-11)?
7. Is Dgraph's licence Apache-2.0 or Community-License (DG-03)?
8. Which library-only modules (BL-09 AST compiler, BL-06a SPARQL handler) are intended to be mounted? (U-14)
