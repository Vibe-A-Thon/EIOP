| Field | Value |
|---|---|
| Registry ID | T-C01-apache-age |
| Tier | B (graph on PostgreSQL; candidate backend for Postgres shops) |
| Versions examined | v1.8.0-rc0 (PG15 build 2026-09-19; PG18 build 2026-07-09); v1.7.0-rc0 (2026-01-21 PG18, 2026-02-11 PG17) |
| Verified on | 2026-10-26 (brief says 2026-10-18; actual access date used) |
| Worker | V14 |

## 1. Identity, current status, tier, and sources
Apache AGE ("A Graph Extension") adds openCypher graph storage and queries to PostgreSQL. It began in 2019 inside Bitnine's AgensGraph, entered the Apache Incubator in April 2020 and graduated to a Top-Level Project on 2022-05-17 (announced 2022-06-08) [CLAIM-age-01]. Repo `apache/age`, Apache-2.0, ~4.9k stars, pushed 2026-10-13 [CLAIM-age-02]. Releases are per-PostgreSQL-major tags; the newest are v1.8.0-rc0 builds for PG15 and PG18 (the `-rc0` suffix on the latest tags means they are release-candidate-labelled; GA status of 1.8.0 UNVERIFIED), after 1.7.0 and 1.6.0 [CLAIM-age-02]. Peers: [C01-neo4j](C01-neo4j.md), [C01-kuzu](C01-kuzu.md).

## 2. Primary problem, target workloads, example workflows
Graph queries inside the existing PostgreSQL estate, with relational and graph in one transaction. Example: SQL join of a `customers` table with a Cypher traversal via `SELECT * FROM cypher('g', $$ MATCH ... $$) AS (a agtype)`. For EOIP: Postgres-only customers, no new datastore.

## 3. Feature inventory
| Feature | Status | Note |
|---|---|---|
| openCypher queries | present, coverage partial | README does not list supported subset [CLAIM-age-03] |
| Hybrid SQL + Cypher | present | [CLAIM-age-03] |
| Multiple graphs, label hierarchy, property indexes | present | [CLAIM-age-03] |
| Supported PostgreSQL | 11-18 | [CLAIM-age-03] |
| Row-level security support | present since 1.7.0 | "Add RLS support and fix permission checks (#2309)" [CLAIM-age-04] |
| Gremlin / SPARQL / GQL | absent | |
| Vector / FTS | via PostgreSQL extensions (pgvector, tsvector) | not AGE-native |
| Distributed scale-out | absent natively | Postgres replication/Citus not verified for AGE |
| Branching, bitemporal | absent | |

## 4. Architecture
```
 client (psycopg/JDBC) -> PostgreSQL backend: LOAD 'age'; search_path=ag_catalog
   cypher() function -> AGE parser/transformer -> SQL plan -> PG executor
   storage: per-graph schema; vertex/edge label tables (heap) + agtype columns
 shared with PG: WAL, MVCC, roles, RLS, replication, pg_dump
```

## 5. Under-the-hood reconstruction
Cypher is parsed by an AGE grammar and transformed into PostgreSQL query trees; each label is a table in a graph schema holding `agtype` (JSONB-like) properties, so planning, indexes (B-tree/GIN), MVCC, WAL and backup are PostgreSQL's (HYPOTHESIS from project design; verify in `src/backend/parser`). Operational caveats: each connection must `LOAD 'age'` and set `search_path`; in non-autocommit clients graph and label changes are invisible to other sessions until commit; `CREATE EXTENSION age` fails if `ag_catalog` exists owned by another role [CLAIM-age-03]. Security: PostgreSQL roles, GRANTs and, since 1.7.0, RLS on graph label tables; how policies interact with traversal joins (policy applied per label table, so a multi-hop pattern is filtered at each hop) is HYPOTHESIS; no source describes semantics [CLAIM-age-04].

## 6. Requirements inferred
PostgreSQL superuser to install extension; per-PG-major build; connection-pool pinning of `LOAD`/search_path.

## 7. Performance and resource model
No verified benchmark. Expected: multi-hop traversal executes as repeated joins, so deep traversals degrade vs native adjacency (hypothesis, common to relational-over-graph designs). Scaling is PostgreSQL vertical plus read replicas. Failure modes: pooler (PgBouncer transaction mode) breaking session `LOAD`.

## 8. Strengths
Apache TLP governance; permissive licence; inherits PostgreSQL durability, PITR, replication and RLS; hybrid SQL/graph; lets EOIP serve customers who mandate Postgres. Match by an `AgeGraphStore` over SQL with pooled pinned sessions.

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | multi-hop as joins; no native graph algorithms library (UNVERIFIED) |
| Operational | per-PG-major extension builds; RC-labelled latest tags; session setup per connection |
| Friction | openCypher gaps and agtype quirks; incomplete documented subset |
| Semantics | no RDF/OWL/reasoning; no versioning |
| Licensing | none (Apache-2.0); extension must be installable by customer DBAs |

## 10. Deployment, licensing, redistribution
Apache-2.0, ASF-governed; redistribution-safe. Runs wherever PostgreSQL does (self-hosted, container, many managed Postgres services only if AGE is allowed: UNVERIFIED per provider). Air-gap: yes. No community/enterprise split (Bitnine sells support: UNVERIFIED).

## 11. Competitive delta vs EOIP baseline
No Postgres/AGE adapter in BL-01..05. RLS is the one security primitive that could back BL-20 tenancy and BL-18 source-ACL pushdown (both weak in baseline): physical row filtering in the store rather than in `query/policy.py`.

## 12. Strength cards and inversion cards
- STR-age-01 | Apache AGE | PostgreSQL RLS plus graph in one transaction | CLAIM-age-04 | tenant isolation and ACL enforced in storage | integrate | per-tenant `app.tenant_id` RLS policy on every label table, set via `SET LOCAL` by the adapter | acceptance: cross-tenant traversal returns zero rows in a 3-tenant test, including 3-hop patterns and `MERGE`.
- STR-age-02 | Apache AGE | Postgres operations (PITR, replication) reused | CLAIM-age-03 | BL-50 gap | reuse | defer to `pg_basebackup` | acceptance: restore drill.
- INV-age-01 | v1.8.0-rc0, deep traversal | join-based traversal | root cause algorithm (hypothesis) | alternative: EOIP query plans bound depth (BL-08) and push heavy analytics to CSR snapshots (BL-43); worse for ad hoc deep paths | options: (a) depth caps (b) materialised neighbour tables (c) hybrid with native engine | selected (a) | POC: LDBC-style 1-5 hop on 10^7 edges vs Neo4j CE; success = p95 within agreed multiple | defensibility: bounded plans exist anyway | decision: EXPERIMENT.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-01 property-graph storage | INTEGRATE (optional Postgres backend) |
| CAP-14 openCypher | EXPERIMENT |
| CAP-47 / CAP-46 RLS-backed isolation | EXPERIMENT (high value) |
| CAP-74 backup/PITR | REUSE (Postgres) |
| CAP-53 vector | DEFER (pgvector, separate) |

## 14. Tests / PoC
Conformance run; RLS cross-tenant matrix; pooler behaviour; upgrade 1.7 to 1.8; PG16 vs PG18 build availability check; crash recovery.

## 15. Risks and open questions
GA vs `-rc0` tag labelling; RLS-on-traversal semantics unproven; openCypher subset; managed-Postgres availability; Bitnine dependence on contributions.

## Appendix A. Research-dimension coverage
| Dimension | Sections | Summary |
|---|---|---|
| D1-D4 | 1-4 | covered |
| D5 storage | 5 | label tables + agtype (hypothesis) |
| D6 query | 3 | openCypher in SQL |
| D7 reasoning | 9 | absent |
| D8 concurrency | 5 | PG MVCC |
| D9 performance | 7 | no numbers |
| D10 versioning | 3 | absent |
| D11 security/tenancy | 5,12 | RBAC + RLS (1.7.0) |
| D12 ingestion | N/A | not examined |
| D13-D16 AI | 3 | via pgvector |
| D17 ops | 8 | PG tooling |
| D18 UX | N/A | none native |
| D19-D20 | 10 | Apache-2.0 |
| D21 ecosystem | 1 | ASF TLP |
| D22-D24 | 12,15 | covered |

## Appendix B. Capability mapping
| CAP-ID | This tech | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-01 | native | 03 | BL-01 | INTEGRATE | P2 |
| CAP-14 | partial | 03 | BL-59 absent | EXPERIMENT | P2 |
| CAP-16 | native (SQL) | 03 | BL-59 absent | EXPERIMENT | P3 |
| CAP-45/46/47 | native RLS | 04 | BL-18 absent, BL-20 partial | EXPERIMENT | P1 |
| CAP-74 | native (PG) | 03 | BL-50 | REUSE | P2 |

## Appendix C. Evidence records
| CLAIM-ID | Product/version/date | Claim | Class | Source | Dates | Confidence | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-age-01 | Apache AGE 2022 | Top-Level Project; graduated 2022-05-17; incubated since April 2020 | primary (ASF) | https://blogsarchive.apache.org/foundation/entry/the-apache-software-foundation-announces83 ; https://incubator.apache.org/projects/age.html | 2022-06-08 / 2026-10-26 | 0.85 | GitHub README does not state status |
| CLAIM-age-02 | tags | Apache-2.0; 4.9k stars; releases PG15/v1.8.0-rc0 2026-09-19, PG18 v1.8.0-rc0 2026-07-09, PG17 v1.7.0-rc0 2026-02-11 | primary (API) | https://api.github.com/repos/apache/age/releases | 2026-10-26 | 0.85 | README badge says v1.8.0 |
| CLAIM-age-03 | README | PG 11-18; openCypher; hybrid SQL/Cypher; session and visibility caveats | vendor docs | https://github.com/apache/age | 2026-10-26 | 0.85 | none |
| CLAIM-age-04 | 1.7.0 notes | "Add RLS support and fix permission checks (#2309)" | release notes (via search) | https://age.apache.org/release-notes | 2026-10-26 | 0.6 | label-level semantics not found |

## Appendix D. Assumptions
Internals are design-level hypotheses; RLS traversal semantics untested.
