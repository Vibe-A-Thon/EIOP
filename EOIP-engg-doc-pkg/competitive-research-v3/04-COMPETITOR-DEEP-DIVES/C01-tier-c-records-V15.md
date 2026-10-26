# C01 — Tier C records (batch V15)

Verified on 2026-10-26. Worker V15. Related deep dives: `C01-graphscope.md`, `C01-oracle-graph.md`, `C01-spanner-graph.md`, `C01-puppygraph.md`, `C01-dgraph.md`, `C01-kuzu.md`. GitHub fields below come from the GitHub REST API (unauthenticated) read 2026-10-26 before it rate-limited.

### T-C01-tugraph — TuGraph

| Field | Value |
|---|---|
| Official URL | https://github.com/TuGraph-family/tugraph-db |
| Owner | TuGraph-family org (Ant Group affiliation not stated on the page; widely reported, UNVERIFIED here) |
| Latest version + date | v4.5.2, 2025-03-13; last push 2026-05-11 |
| Status | Slow: no release in about 19 months, activity continues sporadically |
| Licence + class | Apache-2.0, permissive |
| Deployment | self-hosted, Docker, embedded library |
| Air-gap viable | yes |
| Tier reason | Narrow relevance outside CN market |

**Relevance.** ACID labeled property graph with openCypher; LDBC SNB record claimed (2022, vendor). No GQL claim found. Touches CAP-01, CAP-14, CAP-62. Not needed given Neo4j/HugeGraph adapters; minor C++ engine reference.
**Decision.** REFERENCE-ONLY. Cypher conformance candidate if a customer asks.

| CLAIM-ID | Product/version/date | Claim | Class | Source | Pub/access | Conf | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-tugraph-01 | v4.5.2 | Apache-2.0; LPG, ACID, openCypher API; latest release 2025-03-13; push 2026-05-11 | Officially documented | github.com/TuGraph-family/tugraph-db (+API) | 2026-10-26 | 0.8 | owner not stated |

### T-C01-ultipa — Ultipa

| Field | Value |
|---|---|
| Official URL | https://www.ultipa.com |
| Owner | Ultipa (commercial vendor) |
| Latest version + date | "Ultipa Graph v6" / GQLDB per third-party text; exact version and date NOT PUBLICLY VERIFIED |
| Status | Active (inferred from current product pages) |
| Licence + class | Proprietary; free Community edition for personal/noncommercial use (third-party report) |
| Deployment | self-hosted, cloud |
| Air-gap viable | partial (self-hosted binary; licence checks UNVERIFIED) |
| Tier reason | Commercial HTAP graph; narrow relevance |

**Relevance.** HTAP graph with ISO GQL claimed (older UQL language), vector and algorithms. Noncommercial free tier blocks bundling. Touches CAP-14, CAP-53, CAP-62, CAP-77.
**Decision.** REFERENCE-ONLY. Watch for ISO GQL conformance claims.

| CLAIM-ID | Product/version/date | Claim | Class | Source | Pub/access | Conf | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-ultipa-01 | undated | HTAP positioning; free single-binary ISO GQL database listed; Community free for noncommercial use | Third-party report/vendor | ultipa.com/llms.txt ; ultipa.com product pages | 2026-10-26 | 0.35 | official licence text not read |

### T-C01-surrealdb — SurrealDB

| Field | Value |
|---|---|
| Official URL | https://github.com/surrealdb/surrealdb |
| Owner | SurrealDB Ltd |
| Latest version + date | v3.3.4, 2026-10-19 |
| Status | Active (33.2k stars, releases within days) |
| Licence + class | Business Source License 1.1 for core (SPDX NOASSERTION); SDKs Apache-2.0/MIT; source-available. Change date and additional-use grant not read |
| Deployment | embedded, single node, cluster, WASM, cloud |
| Air-gap viable | yes |
| Tier reason | Multi-model DB with graph relations; adjacent |

**Relevance.** Document/relational/graph store with `RELATE` typed edges and record links, SurrealQL. BSL is a legal-review trigger for white-label hosting. Touches CAP-03, CAP-04, CAP-47. Weak graph semantics for ontology work.
**Decision.** REFERENCE-ONLY (multi-model embedding pattern). Do not bundle.

| CLAIM-ID | Product/version/date | Claim | Class | Source | Pub/access | Conf | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-surrealdb-01 | v3.3.4, 2026-10-19 | Core under BSL 1.1; SDKs Apache-2.0/MIT; RELATE graph edges; embedded/server/WASM | Officially documented | github.com/surrealdb/surrealdb (+API) | 2026-10-26 | 0.8 | none |

### T-C01-sap-hana-graph — SAP HANA Graph

| Field | Value |
|---|---|
| Official URL | https://help.sap.com (HANA Cloud Graph) |
| Owner | SAP SE |
| Latest version + date | NOT PUBLICLY VERIFIED (docs read were HANA 2.0 SPS05 and tutorials) |
| Status | Active product component |
| Licence + class | Proprietary |
| Deployment | SAP HANA on-prem and HANA Cloud |
| Air-gap viable | partial (on-prem HANA) |
| Tier reason | ERP-embedded graph; adjacent |

**Relevance.** `GRAPH WORKSPACE` defined over existing tables/views; openCypher subset via `OPENCYPHER_TABLE`, algorithms (shortest path, neighbors, BFS, SCC). Same table-mapped model as Oracle. Touches CAP-14, CAP-16, CAP-21. Relevant to SAP-centric customers as a source.
**Decision.** REFERENCE-ONLY; treat HANA as a customer source via SQL connector.

| CLAIM-ID | Product/version/date | Claim | Class | Source | Pub/access | Conf | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-sap-hana-graph-01 | HANA 2.0 SPS05 / Cloud tutorials | Graph workspaces over tables/views; openCypher subset in SQL; built-in algorithms | Officially documented (tutorials, reference PDF) | developers.sap.com/tutorials/hana-graph-overview-pattern-matching-sql.html ; SAP HANA Graph Reference | 2026-10-26 | 0.6 | current clause coverage unknown |

### T-C01-aerospike-graph — Aerospike Graph

| Field | Value |
|---|---|
| Official URL | https://github.com/aerospike/aerospike-graph-service |
| Owner | Aerospike, Inc. |
| Latest version + date | v3.3.3, 2026-10-21 |
| Status | Active |
| Licence + class | Graph service Apache-2.0; underlying Aerospike Database edition terms (Community vs Enterprise feature key) separate, not read |
| Deployment | Docker, JVM service over an Aerospike cluster |
| Air-gap viable | yes |
| Tier reason | Gremlin over Aerospike; adjacent |

**Relevance.** TinkerPop-compliant Gremlin server (3.7.x only; 3.8 unsupported) storing graph in Aerospike. Fits the existing Gremlin/JanusGraph adapter path (BL-05) for customers already on Aerospike. Touches CAP-13, CAP-05.
**Decision.** REFERENCE-ONLY; adapter is possible via BL-05 pattern if requested.

| CLAIM-ID | Product/version/date | Claim | Class | Source | Pub/access | Conf | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-aerospike-graph-01 | v3.3.3, 2026-10-21 | Apache-2.0 service; Gremlin on TinkerPop 3.7.x; needs Aerospike with feature key for Enterprise/Standard editions | Officially documented | github.com/aerospike/aerospike-graph-service | 2026-10-26 | 0.8 | none |

### T-C01-duckpgq — DuckPGQ

| Field | Value |
|---|---|
| Official URL | https://github.com/cwida/duckpgq-extension ; duckpgq.org |
| Owner | cwida GitHub org (CWI affiliation not stated on page) |
| Latest version + date | No GitHub releases; distributed as DuckDB community extension; last push 2026-10-23 |
| Status | Active research project |
| Licence + class | MIT, permissive |
| Deployment | embedded (DuckDB in-process) |
| Air-gap viable | yes |
| Tier reason | SQL/PGQ research extension |

**Relevance.** Adds `CREATE PROPERTY GRAPH`, `GRAPH_TABLE`/`MATCH` to DuckDB via the grammar-extension API, with factorized-aggregate optimizer; "research project, work in progress". Only open, embeddable SQL/PGQ engine found, so a candidate test target for BL-59 and for IR-to-SQL/PGQ conformance. Touches CAP-04, CAP-16, CAP-19.
**Decision.** EXPERIMENT as a local SQL/PGQ conformance and analytics target.

| CLAIM-ID | Product/version/date | Claim | Class | Source | Pub/access | Conf | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-duckpgq-01 | main, 2026-10-23 | MIT; SQL/PGQ via DuckDB grammar extension; community-extension install; research/WIP | Officially documented | github.com/cwida/duckpgq-extension | 2026-10-26 | 0.75 | DuckDB version pin not read |

### T-C01-cozodb — CozoDB

| Field | Value |
|---|---|
| Official URL | https://github.com/cozodb/cozo |
| Owner | Individual maintainer org (cozodb) |
| Latest version + date | v0.7.6, 2023-12-11; last push 2024-12-04 |
| Status | Dormant: no release in about 34 months, no push in about 22 months |
| Licence + class | MPL-2.0 (weak copyleft, file-level) |
| Deployment | embedded, HTTP server; backends in-memory/SQLite/RocksDB/Sled/TiKV |
| Air-gap viable | yes |
| Tier reason | Embedded Datalog+graph+vector; activity to verify (verified: dormant) |

**Relevance.** Transactional relational-graph-vector DB queried in Datalog, with recursion, HNSW and time travel; README: pre-1.0 with no API/storage compatibility promise. Valuable design reference for CAP-22 (Datalog), CAP-34, CAP-04, but unmaintained.
**Decision.** REFERENCE-ONLY. Do not depend on it.

| CLAIM-ID | Product/version/date | Claim | Class | Source | Pub/access | Conf | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-cozodb-01 | v0.7.6 | MPL-2.0; latest release 2023-12-11; last push 2024-12-04; Datalog, HNSW, time travel, MVCC; pre-1.0 | Officially documented (README + API) | github.com/cozodb/cozo | 2026-10-26 | 0.85 | none |

### T-C01-helixdb — HelixDB

| Field | Value |
|---|---|
| Official URL | https://github.com/HelixDB/helix-db |
| Owner | HelixDB (vendor with managed Helix Cloud) |
| Latest version + date | v3.5.1, 2026-10-08 (README text cites Rust 3.0.0, so README lags) |
| Status | Active (6.2k stars, last push 2026-10-25) |
| Licence + class | Apache-2.0 per current README/API; earlier licence history NOT checked |
| Deployment | local (Docker/Podman), embedded in-process, managed cloud |
| Air-gap viable | yes (local/embedded) |
| Tier reason | Young graph-vector DB |

**Relevance.** Rust OLTP graph with vector (ANN prefiltered by traversal) and BM25 in one transactional engine, JSON query endpoint and Cypher reads from source builds. Young; single ACID writer in cloud. Touches CAP-01, CAP-04, CAP-53, CAP-54. Interesting for embedded agent memory (CAP-57).
**Decision.** EXPERIMENT as an optional embedded local backend candidate; check licence history and maturity first.

| CLAIM-ID | Product/version/date | Claim | Class | Source | Pub/access | Conf | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-helixdb-01 | v3.5.1, 2026-10-08 | Apache-2.0; Rust graph+vector+BM25; local/embedded/cloud | Officially documented | github.com/HelixDB/helix-db (+API) | 2026-10-26 | 0.7 | README version (3.0.0) older than release tag |

### T-C01-galaxybase — Galaxybase

| Field | Value |
|---|---|
| Official URL | NOT PUBLICLY VERIFIED (vendor CreateLink / 创邻科技) |
| Owner | CreateLink (Zhejiang) Technology Co., Ltd |
| Latest version + date | NOT PUBLICLY VERIFIED |
| Status | Commercial; LDBC SNB Interactive audits 2022-05 and a later record report |
| Licence + class | Proprietary (LDBC FDR) |
| Deployment | self-hosted distributed |
| Air-gap viable | unknown |
| Tier reason | Commercial CN graph DB |

**Relevance.** Native distributed HTAP graph DB with audited LDBC results (vendor press and FDR). No open source, no Community terms found. Touches CAP-05 only.
**Decision.** REFERENCE-ONLY.

| CLAIM-ID | Product/version/date | Claim | Class | Source | Pub/access | Conf | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-galaxybase-01 | 2022-05 | LDBC audited SNB Interactive SF30/100/300; described as proprietary product | Independent benchmark (audit) | ldbcouncil.org LDBC_SNB_I_20220516_SF30-100-300_galaxybase.pdf | 2026-10-26 | 0.6 | later report not opened |

### T-C01-orientdb — OrientDB (historical lessons)

| Field | Value |
|---|---|
| Official URL | https://github.com/orientechnologies/orientdb |
| Owner | OrientDB LTD (licensor per README) |
| Latest version + date | 3.2.57, 2026-10-05 (API); last push 2026-10-23 |
| Status | Active maintenance. The registry label "historical" is partly wrong: the project still ships frequent 3.2.x releases |
| Licence + class | Apache-2.0, permissive |
| Deployment | embedded, server, distributed multi-master |
| Air-gap viable | yes |
| Tier reason | Historical lessons |

**Relevance.** Multi-model (graph, document, full-text, geospatial) with SQL dialect and ACID; 5k stars, 366 open issues. Lessons: multi-model breadth versus graph-specialist traction. Touches CAP-03, CAP-05, CAP-01.
**Decision.** REFERENCE-ONLY. Registry note: relabel as "maintained, low momentum" (ADD-style correction, not exclusion).

| CLAIM-ID | Product/version/date | Claim | Class | Source | Pub/access | Conf | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-orientdb-01 | 3.2.57 | Apache-2.0; release 2026-10-05; push 2026-10-23; multi-model | Officially documented | github.com/orientechnologies/orientdb (+API) | 2026-10-26 | 0.85 | README lists no owner history |
