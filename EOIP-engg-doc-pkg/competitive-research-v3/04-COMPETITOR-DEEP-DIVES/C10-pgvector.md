| Field | Value |
|---|---|
| Registry ID | T-C10-pgvector |
| Tier | A (vector search inside PostgreSQL; only candidate with native row-level security and ACID on the vector table) |
| Versions examined | pgvector v0.8.7 (tag commit 2026-10-01; master active 2026-10-25); PostgreSQL 18.6 current, 14 EOL 2026-11-12 |
| Verified on | 2026-10-26 |
| Worker | V06 |

## 1. Identity, current status, tier, sources

pgvector (github.com/pgvector/pgvector; maintainer Andrew Kane; open-source PostgreSQL extension) adds `vector`, `halfvec`, `bit`, `sparsevec` types, distance operators and HNSW/IVFFlat indexes to PostgreSQL. Licence: **PostgreSQL License** (LICENSE file header, copyright PGDG/UC Regents) [CLAIM-pgvector-01]. Supports Postgres 13+ (Linux/Mac source builds, Docker images pg13-pg18); PostgreSQL 14 final release is 2026-11-12, so new EOIP deployments target 16-18 [CLAIM-pgvector-02]. Latest tag v0.8.7 (tag commit "Version bump to 0.8.7" 2026-10-01); GitHub "Releases" API returned 404, so releases are tags only; commits continue daily (2026-10-25: hypothetical-index support, cost-function readability) [CLAIM-pgvector-02]. Pre-1.0 versioning: no API stability promise stated. Tier A because EOIP's multi-tenant ACL requirement (BL-18/BL-20) maps most directly onto SQL RLS and partitions.

## 2. Problem, workloads, workflows

Problem: avoid a second database for embeddings; combine vector search with relational filters, full-text, transactions and existing PG operations. EOIP workloads: chunk embeddings with per-document ACL rows; evidence tables; a small metadata store (EOIP currently has no relational DB in compose: HugeGraph, Neo4j, Ollama, Prometheus only [CLAIM-pgvector-09]) - so pgvector means **adding** PostgreSQL, not reusing one.
Workflow: `INSERT INTO chunk(id, tenant_id, doc_id, acl_hash, embedding halfvec(768), tsv)` -> `SET hnsw.iterative_scan = relaxed_order` -> `SELECT ... WHERE tenant_id=$1 ORDER BY embedding <=> $q LIMIT 50` under RLS policy `USING (acl_group = ANY(current_setting('eoip.groups')::text[]))` -> fuse with `ts_rank` list by RRF in SQL/app.

## 3. Feature inventory

| Feature | Status | Note |
|---|---|---|
| Types: `vector` (<=16,000 dims), `halfvec`, `bit`, `sparsevec` (<=16,000 non-zero) | present | **index limits**: vector 2,000, halfvec 4,000, bit 64,000, sparsevec 1,000 non-zero (HNSW) [CLAIM-pgvector-03] |
| Index: HNSW (build on empty table, slower build/more memory), IVFFlat (faster build, lower query perf) | present | params m=16, ef_construction=64, `hnsw.ef_search`=40, `ivfflat.lists`, `probes`=1 [CLAIM-pgvector-03] |
| Iterative index scans (0.8.0+): `strict_order` / `relaxed_order`, `hnsw.max_scan_tuples` default 20,000 | present | fixes filtered under-return but bounded [CLAIM-pgvector-03] |
| Filtering via B-tree, partial indexes, partitioning | present | filters apply **after** approximate index scan [CLAIM-pgvector-03] |
| Hybrid with Postgres full-text; RRF or cross-encoder | documented pattern | no built-in fusion operator [CLAIM-pgvector-03] |
| Row-level security, GRANT, roles, audit extensions | present via PostgreSQL | not pgvector-specific; README says nothing about RLS [CLAIM-pgvector-04] |
| WAL, streaming replication, PITR, pg_dump | present | vectors are WAL-logged [CLAIM-pgvector-03] |
| Parallel index build | present | `max_parallel_maintenance_workers` [CLAIM-pgvector-03] |
| Quantisation | partial | halfvec indexing and binary quantisation via `bit`; no PQ listed |
| Built-in embedding model call | absent | |
| Sharding / distributed ANN | absent (needs Citus or partitioning; not examined) | |

## 4. Architecture

```
 client --SQL--> PostgreSQL backend process (per connection)
   planner: chooses HNSW/IVFFlat index scan (ORDER BY <-> LIMIT) or seq scan; cost via index AM (hnswcostestimate)
   executor: index scan returns candidates -> heap fetch -> RLS quals + WHERE -> iterative re-scan if too few
   storage: heap table + HNSW graph pages in shared_buffers; WAL; autovacuum
```
Control plane = PostgreSQL (roles, pg_hba, TLS, extensions); no separate pgvector process.

## 5. Under-the-hood reconstruction

- **Data model**: ordinary table rows; vector column is a varlena; index is a PostgreSQL index access method written in C ("HNSW is a multilayer graph", IVFFlat divides vectors into lists) [CLAIM-pgvector-03]. Page-based graph storage; builds faster when graph fits in `maintenance_work_mem`; indexes should ideally fit in memory [CLAIM-pgvector-03].
- **Query pipeline**: `ORDER BY embedding <=> $1 LIMIT k` is required for the planner to use the ANN index; with `WHERE` the index returns up to `ef_search` (40) candidates, then the filter runs, so selective filters can return fewer than k rows - the documented fix is `hnsw.iterative_scan` which keeps scanning until enough rows or `max_scan_tuples` [CLAIM-pgvector-03]. This is post-filtering by construction; recall under restrictive ACLs depends on that cap (hypothesis for ACL group sizes; must be measured).
- **Security reconstruction**: with RLS enabled, policy expressions run per row before user-supplied predicates except `leakproof` functions; default-deny without policy; owners/superusers/BYPASSRLS skip RLS unless `FORCE ROW LEVEL SECURITY`; referential-integrity checks bypass RLS; policies reading other tables risk races under READ COMMITTED [CLAIM-pgvector-04]. Whether pgvector distance operators are marked leakproof, and whether RLS predicates are pushed into the index scan or applied post-scan, is **NOT PUBLICLY VERIFIED** here - test with EXPLAIN.
- **Concurrency**: PostgreSQL MVCC; inserts into HNSW are transactional; deletes leave dead tuples; "vacuuming can be slow for HNSW" - recommended `REINDEX INDEX CONCURRENTLY` first, then `VACUUM` [CLAIM-pgvector-03].
- **Partitioning/tenancy**: list partitioning or separate tables per tenant for isolation; partial indexes for few filter values [CLAIM-pgvector-03]; each partition has its own HNSW, giving per-tenant graphs (design inference, aligns with README).
- **Versioning**: extension versions via `ALTER EXTENSION UPDATE`; index format changes between minors not examined (UNVERIFIED).
- Caching: shared_buffers and OS cache; no vector-specific cache.

## 6. Inferred requirements for EOIP

FR: SQL schema owned by EOIP migrations; per-request `SET LOCAL eoip.tenant` / `eoip.groups` session settings consumed by RLS; `FORCE ROW LEVEL SECURITY` on chunk tables; app role without BYPASSRLS. NFR: derived index rebuildable from graph/raw capture; fit RAM budget per ADR-H15; connection pooling aware of session settings (transaction pooling requires `SET LOCAL`).

## 7. Performance and resource model

No independent benchmark used; the README gives parameters but no numbers I relied on. Expectations (documented): HNSW better speed-recall than IVFFlat but slower build and more memory; index should fit memory; use halfvec/binary quantisation to shrink [CLAIM-pgvector-03]. Single node: footprint = PostgreSQL (shared_buffers + per-backend memory) + index size; no JVM. CPU-only by nature (ADR-H15..H17 compatible). Failure modes: recall drop under filters (cap 20,000 tuples), slow HNSW vacuum, build memory spill, 2,000-dim index limit for float32 (needs halfvec for many embedding models), planner choosing seq scan.

## 8. Strengths and how to match/exceed

| Strength | Match/exceed |
|---|---|
| ACID + RLS + roles on vector rows | ACL and tenant policy enforced by the database, not just a convention: exceed Qdrant on enforcement locus |
| One system for text, vectors, relations, backups | integrate; reuse PG ops tooling |
| PostgreSQL License, no CLA/copyleft | redistribution-safe |
| WAL/PITR | cheap durable backup story |

## 9. Limitations with root causes

| Class | Item |
|---|---|
| Algorithmic | post-filtered ANN: restrictive filters starve results; iterative scan bounded by `max_scan_tuples` |
| Operational | HNSW build memory/time; slow vacuum; dimension caps for indexes; vertical scaling only; planner variance |
| Architectural | adds PostgreSQL to a stack that has none; RLS performance sensitive to policy shape ("keep policy based on current row", others costly) [CLAIM-pgvector-04] |
| Security | RLS bypass for owners/superusers/BYPASSRLS; RI side-channels; connection pooling can drop session context if misused |
| User friction | knobs (`ef_search`, probes, `iterative_scan`), no built-in fusion |
| Maintenance | pre-1.0, single-maintainer-led (governance not examined, UNVERIFIED) |

## 10. Deployment, licensing, redistribution

Self-hosted extension on PostgreSQL (docker images pg13-pg18); managed Postgres offerings support it (not examined). Air-gap: yes. Licence: PostgreSQL License (permissive, BSD/MIT-like); PostgreSQL itself under the same licence family. Legal-review trigger: no copyleft; record only. One-node-first fits: one PG container.

## 11. Competitive delta against EOIP baseline

| Item | EOIP | pgvector |
|---|---|---|
| Vector store | BL-14 Partial, in-process, non-persistent | persistent, transactional |
| Source-ACL | BL-18 Absent; BL-17 `PermissionMetadata`, `acl_hash` captured | RLS policy can express `acl_hash`/group membership |
| Tenancy | BL-20 contract only | partitions + RLS + roles |
| Deletes | BL-25 tombstones | `DELETE` is transactional; HNSW space reclaimed after vacuum |
| Backup | BL-50 scripts | WAL/PITR, pg_dump |
| Hybrid | BL-13/15 in-process BM25+RRF | tsvector + RRF in SQL, same transaction |

## 12. Cards

STR-pgvector-01 | pgvector | RLS + ACID on vector rows | [pgvector-03,04] | database-enforced tenant/ACL isolation | integrate | RLS policies keyed on session settings; FORCE RLS | cross-tenant/ACL leak suite returns 0 rows in EXPLAIN-verified plans.
STR-pgvector-02 | pgvector | one-binary-less ops: WAL/PITR/replication | [pgvector-03] | simple backup/DR | integrate | standard PG backup runbook | restore drill yields identical top-k within tolerance.

**INV-pgvector-01 (post-filtered ANN starves under restrictive ACLs).** Target v0.8.7, ACL group selectivity <1%. Root cause: algorithm, *proven* by README (filters apply after index scan) and bounded by `max_scan_tuples`. Options: (1) quick - `relaxed_order` iterative scan + raise cap; (2) native - partition by tenant (+ sub-partition by high-cardinality ACL bucket) so each ANN graph is within an access class; (3) long-term - hybrid router: dense ANN on tenant partition then exact scoring over ACL-qualified candidate set from B-tree when estimated selectivity is low. Selected: 2 with 1; 3 if measurements demand. Benchmark: 1M rows, 768-d halfvec, selectivity 0.1/1/10/50%; recall@10 vs exact; success >=0.95 with p95 < agreed budget; baseline = Qdrant filterable HNSW on same data. Failure cases: partition explosion; RLS pushed after scan. Defensibility: ACL-bucket partitioning derived from EOIP identity model. Decision: EXPERIMENT. Alternative worse above ~10^8 vectors per node.
**INV-pgvector-02 (new service vs ADR-005).** Root cause: deployment. Options: keep in-process for P1; optional PG profile; or reuse a customer's PG. Decision: EXPERIMENT. No 10.5 seed hypothesis targets pgvector.

## 13. Per-capability decisions

| Capability | Decision |
|---|---|
| CAP-53 vector search | INTEGRATE as one of the `VectorIndex` backends (preferred where Postgres already exists) |
| CAP-46 source-ACL enforcement | EXPERIMENT: RLS-backed enforcement; BUILD session-context middleware |
| CAP-47 tenant isolation | INTEGRATE partitioning + RLS |
| CAP-54/55 hybrid | REUSE EOIP RRF; EXPERIMENT SQL fusion |
| CAP-74 backup/PITR | REUSE PostgreSQL tooling |

## 14. Tests and acceptance

1. EXPLAIN audit: confirm RLS quals and ANN index usage for the exact ACL policy; record whether `<=>` is leakproof. 2. Recall vs exact at the four selectivities with/without iterative scan and with partitioning. 3. Leakage suite J5 including pooled connections and `SET LOCAL`. 4. Delete + vacuum test: bulk delete 20%, measure reclaim time and recall. 5. Single-node CPU/RAM footprint at 1M and 10M rows. 6. PITR restore drill. 7. 2,000-dim limit check against candidate embedding models (halfvec). 8. SBOM/licence.

## 15. Risks and open questions

RLS predicate pushdown vs index scan unknown; leakproofness of vector operators unknown; PG 14 EOL; pooling pitfalls; adding PG dependency to a stack without one; pgvector governance/long-term maintainers unverified; index-format upgrade behaviour unverified.

## Appendix A. Dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | PostgreSQL License, tag cadence |
| D2 | 2 | vectors in SQL |
| D3 | 4 | extension in backend process |
| D4 | 5 | HNSW/IVFFlat pages, types |
| D5 | 3 | SQL schema, RLS |
| D6 | 5 | planner, iterative scan |
| D7 | N/A | |
| D8 | 5,7 | MVCC, WAL, replication |
| D9 | 5,9 | transactional upsert/delete |
| D10 | 11 | ACL via RLS |
| D11 | N/A | |
| D12 | N/A | |
| D13 | 2,5 | core |
| D14 | N/A | |
| D15 | N/A | |
| D16 | N/A | |
| D17 | 3 | SQL, drivers (not examined) |
| D18 | 5,9 | RLS semantics and bypasses |
| D19 | 5,12 | partition/RLS tenancy |
| D20 | 7 | no numbers; measurement plan |
| D21 | 10 | permissive licence |
| D22 | 3 | pg_dump/COPY export |
| D23 | N/A | not examined |
| D24 | 7 | no benchmarks used |

## Appendix B. Capability mapping

| CAP | pgvector | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-53 | native | pgvector-03 | BL-14 Partial | INTEGRATE | P1 |
| CAP-46 | partial (via RLS) | pgvector-04 | BL-18 Absent | EXPERIMENT/BUILD | P0 |
| CAP-47 | partial (partition+RLS) | pgvector-03,04 | BL-20 Partial | INTEGRATE | P1 |
| CAP-54 | partial (FTS) | pgvector-03 | BL-13 Implemented | REUSE EOIP | P3 |
| CAP-74 | native (PG) | pgvector-03 | BL-50 | REUSE | P2 |
| CAP-04 | native | pgvector-03 | in-process | INTEGRATE | P1 |

## Appendix C. Evidence records (accessed 2026-10-26)

| CLAIM | product/version/date | claim | class | source | pub/access | conf | contradictory |
|---|---|---|---|---|---|---|---|
| pgvector-01 | master | PostgreSQL License | Officially documented | https://raw.githubusercontent.com/pgvector/pgvector/master/LICENSE | /2026-10-26 | 0.9 | none |
| pgvector-02 | v0.8.7; PG 18.6 | v0.8.7 tag commit 2026-10-01; tags only (no Releases); master commits 2026-10-25; PG supported versions and EOLs (14: 2026-11-12) | Officially documented | GitHub API https://api.github.com/repos/pgvector/pgvector/commits ; https://www.postgresql.org/support/versioning/ | /2026-10-26 | 0.85 | none |
| pgvector-03 | README master | Types, dimension and index limits, HNSW/IVFFlat params, iterative scans 0.8.0 and max_scan_tuples 20,000, filtering via partial indexes/partitioning post-filter, hybrid RRF pattern, WAL/PITR, vacuum slow for HNSW | Officially documented | https://github.com/pgvector/pgvector/blob/master/README.md | /2026-10-26 | 0.85 (summarised) | none |
| pgvector-04 | PostgreSQL 18 docs | RLS default-deny, USING/WITH CHECK, permissive/restrictive, bypass rules, leakproof ordering, RI bypass, race conditions | Officially documented | https://www.postgresql.org/docs/current/ddl-rowsecurity.html | /2026-10-26 | 0.9 | none |
| pgvector-09 | EOIP | compose has no PostgreSQL service | Observed in source code | `01-SYSTEM-BASELINE.md` §3 deployment list | /2026-10-26 | 0.8 (baseline doc, compose not re-read for all services) | none |

## Appendix D. Assumptions

RLS-plus-ANN planner behaviour is unverified and flagged for EXPLAIN testing. Governance of pgvector and index upgrade behaviour not examined. No numbers fabricated; no local run.
