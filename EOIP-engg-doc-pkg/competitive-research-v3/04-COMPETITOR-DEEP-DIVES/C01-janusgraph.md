# C01 — JanusGraph

| Field | Value |
|---|---|
| Registry ID | T-C01-janusgraph |
| Tier | A (EOIP already ships an adapter, `packages/eoip/adapters/janusgraph.py`; permissive-licence distributed OLTP reference) |
| Versions examined | 1.1.0 (notes 2024-11-07, GitHub published 2024-11-09, latest stable); 1.0.0 (2023-10-21/22); 1.2.0 (GitHub **pre-release**, published 2026-10-25, notes dated 2026-10-28); EOIP adapter at working tree HEAD (dev_local) |
| Verified on | 2026-10-26 (brief says 2026-10-18; actual access date used) |
| Worker | V01 |

## 1. Identity, current status, tier, and sources

JanusGraph is an Apache-2.0 distributed property-graph database that implements Apache TinkerPop/Gremlin on top of pluggable storage and index backends; community-driven under the Linux Foundation since 2017, now listed under LF AI & Data [CLAIM-janusgraph-04]. Repo `github.com/JanusGraph/janusgraph`: ~5.9k stars, 1.2k forks, 507 open issues, 71 open PRs, DCO and security policy present [CLAIM-janusgraph-08].

Release state: v1.0.0 2023-10-21/22 (TinkerPop 3.7.0); v1.0.1 2024-11-08; **v1.1.0 2024-11-07/09 (TinkerPop 3.7.3)** latest stable; **v1.2.0 is a GitHub pre-release** (published 2026-10-25, notes headed "October 28, 2026", date mismatch noted) [CLAIM-janusgraph-01][CLAIM-janusgraph-02][CLAIM-janusgraph-03]. Cadence: roughly one stable release per year, with a ~23-month gap between 1.1.0 and the 1.2.0 pre-release. Status: **maintenance with active development** (large PR/issue queue, release after a long gap). Maturity: production (long-running deployments); not a product with vendor SLAs.

Sources (9): see Appendix C. Master Prompt traps: none specific; "Titan" is the predecessor project (general knowledge, Appendix D A5), not a separate candidate.

## 2. Primary problem, target workloads, concrete example workflows

Large OLTP property graphs where storage scalability and Apache licensing matter more than latency: relationship lookup and shallow-to-medium traversals with indexed entry points, supernode-aware traversals via vertex-centric indexes, OLAP through TinkerPop Hadoop/Spark integration [CLAIM-janusgraph-06]. It is a graph layer, not a database engine: durability, replication and sharding come from Cassandra/ScyllaDB/HBase/Bigtable.

EOIP workflows: (1) "who changed class X" as indexed entry then 3-hop traversal over `canonical_id`; (2) ingest-heavy graph on an existing Cassandra/ScyllaDB estate; (3) mixed-index full-text/geo over entity names via Elasticsearch/OpenSearch. HugeGraph is the same class of system (Gremlin over pluggable storage); see `C01-apache-hugegraph.md` for the reference baseline.

## 3. Feature inventory

| Feature | Status | Notes |
|---|---|---|
| Property graph, schema auto-create or explicit | present | Schema management API; JSON schema initialiser from 1.1.0 [CLAIM-janusgraph-03] |
| Gremlin / TinkerPop | native | 3.7.3 (1.1.0), 3.8.2 (1.2.0 pre-release, breaking semantics) [CLAIM-janusgraph-02] |
| openCypher | unknown | A community Cypher-for-Gremlin translation exists outside core: UNVERIFIED here |
| SPARQL / GQL / SQL-PGQ | absent | |
| Storage: Cassandra, HBase, Bigtable, BerkeleyJE (test), ScyllaDB; community Aerospike, DynamoDB, FoundationDB | present | [CLAIM-janusgraph-04] |
| Index: Elasticsearch, Solr, Lucene; OpenSearch in 1.2.0 | present | [CLAIM-janusgraph-02][CLAIM-janusgraph-04] |
| Composite, mixed, vertex-centric indexes | present | [CLAIM-janusgraph-06] |
| Index lifecycle (REGISTERED/INSTALLED/ENABLED; reindex); `force-index` | present | 1.2.0 adds `WRITE_ONLY_ENABLED` and opt-in CDC-based mixed-index sync |
| Transactions | partial | Depend on backend; locking opt-in [CLAIM-janusgraph-05] |
| Multi-tenant / per-graph ACL / source ACL | absent in docs read | Authentication only via Gremlin Server [CLAIM-janusgraph-07] |
| Vector search | absent in core | not found in sources read |
| OLAP | present | Hadoop-Gremlin/Spark; Spark limited to Java 11/17 in 1.2.0 |
| Authentication | present | HTTP Basic, SASL, HMAC tokens; no authorization model found [CLAIM-janusgraph-07] |
| UI | absent in core | third-party tools |
| Bitemporal/versioning | absent | |
| Backup | backend-level | e.g. Cassandra snapshots |

## 4. Architecture diagram

```
 clients: Gremlin Console | gremlin drivers (WS/HTTP) | EOIP httpx adapter (HTTP script POST)
        |
 Gremlin Server (channelizer: WS and/or HTTP; auth: Basic/SASL/HMAC; script engines)
        |
 JanusGraph core (embedded in server JVM or app)
   schema/type manager -> transaction (in-memory buffer, tx cache)
   query optimiser: index selection (composite/mixed), vertex-centric index use
   StandardJanusGraph -> KeyColumnValueStore SPI  \
                      -> IndexProvider SPI         /  pluggable
        |                                   |
 Storage backend (edgestore, graphindex,    Mixed index backend
 system_properties, txlog...) :             Elasticsearch/Solr/Lucene/OpenSearch
 Cassandra/Scylla/HBase/Bigtable/BerkeleyJE
 control plane: management API (schema, reindex), locks via backend, cluster = backend cluster
```

## 5. Under-the-hood reconstruction

Evidence is documentation level only; the JanusGraph source was not read, so source paths at pinned tags are not cited (limitation, Appendix D). (H) = hypothesis.

**Data model.** Property graph with typed property keys (cardinality SINGLE/LIST/SET), edge labels with multiplicity, vertex labels, meta-properties on properties. Schema is auto-created on first use unless disabled (`schema.default`, H from general knowledge); explicit schema recommended for production.

**Storage layout.** A vertex is a row in the backend `edgestore` keyed by vertex id; properties and edges are columns sorted by a type-id + sort-key encoding (H), so adjacency for a vertex-label-direction would be a contiguous column slice. Documented: vertex-centric indexes are "local to each vertex and stored with edges and properties in `edgeStore`", built per edge label and direction, prefix indexes whose key order matters [CLAIM-janusgraph-06]. Global composite indexes are stored in the primary backend (atomic with the graph mutation); mixed indexes live in the external index backend and are not atomic with it [CLAIM-janusgraph-06]. 1.1.0 can inline vertex properties into a composite index (irreversible: no downgrade after adoption) [CLAIM-janusgraph-03].

**Query pipeline.** Gremlin traversal -> TinkerPop strategies -> JanusGraph-specific strategies (index selection, vertex-step batching, `has()` folding; H) -> backend slice queries. Composite index needs equality on every indexed key; mixed index supports range/text/geo; unindexed `has()` falls back to a **full graph scan** (correct but very slow); `force-index` turns that into an error [CLAIM-janusgraph-06]. Ordered traversals with limit can use vertex-centric indexes. No documented cost-based optimiser or EXPLAIN equivalent was read (H: `profile()` only).

**Reasoning.** None.

**Concurrency and transactions.** On eventually consistent backends (Cassandra, HBase) JanusGraph itself needs explicit locking: `setConsistency(element, ConsistencyModifier.LOCK)` per schema element, default lock provider relies on synchronised clocks; locking adds commit steps, can deadlock under conflicting concurrent writes and fails to guarantee consistency if Cassandra drops below quorum. Edge labels can use `FORK` to keep conflicting modifications as separate edges resolved at read; LIST-cardinality with FORK keeps multiple values. Temporary stale index entries and half-edges are expected; ghost vertices (deleted during concurrent modification) can reappear permanently; transactions larger than `buffer-size` split into batches and can leave permanent inconsistencies on failure [CLAIM-janusgraph-05].

**Partitioning.** Delegated to the backend (token ring / region / tablet). Vertex-cut partitioning for supernodes: UNVERIFIED (not read).

**Caching.** Transaction-level and database-level caches exist (general knowledge); staleness trade-offs not read: UNVERIFIED.

**Versioning.** None; compatibility rules between versions documented (1.0 TinkerPop 3.5 -> 3.7 breaking; string vertex IDs; 1.1 inline index is one-way) [CLAIM-janusgraph-03]. **Security.** Gremlin Server authenticator with credentials graph; HTTP Basic and SASL; HMAC token sessions (default 1 h); credentials store should be a separate keyspace [CLAIM-janusgraph-07]. No row/property-level authorization and no tenant concept found.

### 5.1 Reading EOIP's adapter against this model (observed, `packages/eoip/adapters/janusgraph.py`)

What it uses: Gremlin Server HTTP script endpoint `POST {url}/gremlin` with `{"gremlin", "bindings"}`; property **values** passed as bindings (`cid`, `val`, `f0..`, `outV`, `inV`, `key`, `p_<k>`), so values are not string-built; `elementMap()` for reads; `coalesce(unfold(), addV(...))` upsert idiom; `canonical_id` as business key; `limit` forced through `int()`; injectable transport; query-budget timeout; Basic auth when a password is set [CLAIM-janusgraph-09].

What it misses or gets wrong (static reading; live-unverified like BL-05), severity-ordered:

| # | Finding | Lines | Confidence |
|---|---|---|---|
| 1 | Property **keys** are written with a `p_` prefix (`.property("p_<k>", p_<k>)`) but read, filtered and indexed by the unprefixed key. Upserted properties other than `canonical_id` therefore land under `p_name`, `p_out_cid`, etc. `find_vertex_by_property`, `find_vertices(filters)` and `_find_edges(out_v/in_v)` query `has(key)` / `has('out_cid')` and will not match them; `_to_edge` returns empty `out_cid`/`in_cid` | 191-193, 227, 249, 276, 316-318, 157-158 | high (0.85), unverified live |
| 2 | `ensure_schema` is a no-op ("managed externally"): no unique composite index on `canonical_id`/`edge_key`, so every `V().has('canonical_id', cid)` is a full graph scan, and no `LOCK` consistency, so the `coalesce` upsert is not safe under concurrent writers (duplicates possible) on Cassandra/HBase [CLAIM-janusgraph-05][CLAIM-janusgraph-06] | 163-166, 194-199 | high on mechanism; impact live-unverified |
| 3 | Label and key names are inlined with `json.dumps` into a double-quoted Groovy script. `json.dumps` does not escape `$`, so a label/key containing `${...}` could be evaluated as a Groovy GString by a groovy script engine. EOIP labels come from an ontology manifest, but keys come from ingested JSON (BL-26). Fix: bind label/key too (`hasLabel(lbl)`, `has(k, v)`, `property(k, v)` accept bound values) | 195-197, 227, 249, 193 | medium (0.6), hypothesis |
| 4 | Edge `elementMap()` returns `IN`/`OUT` sub-maps (TinkerPop semantics, H), but `_to_edge` reads `outV`/`inV`/`out_v`; endpoints likely empty | 150-151 | medium (0.6), hypothesis |
| 5 | `bulk_load` issues one HTTP request per vertex/edge; `batch_size` only chunks a Python loop, so no batching, no transaction grouping; partial failure is reported but not resumable | 368-391 | high |
| 6 | `tombstone_vertex` returns `count_vertices() <= before`, which is true whenever the soft-delete does not delete; the return value does not report whether any vertex matched; two full `count()` scans per call | 393-402 | high |
| 7 | `vertex_id()` hash is never used: JanusGraph assigns its own ids, contradicting the module docstring "deterministic eoip vid" | 94-96 | high |
| 8 | No tenant handling anywhere; `clear()` drops all vertices; no source-ACL | 404-405 | high (BL-20) |
| 9 | Server-side timeout not set: a client timeout abandons the HTTP call but the script keeps running until the server-side evaluation timeout (H) | 69-78 | medium |
| 10 | TinkerPop 3.8 (JanusGraph 1.2.0) "changes Gremlin semantics"; adapter assumptions about `property()` default cardinality, `elementMap` shape and the HTTP request format must be re-tested before pinning 1.2.x [CLAIM-janusgraph-02] | n/a | medium |

## 6. Functional and non-functional requirements inferred

FR: Gremlin with explicit schema and index management; composite unique constraints plus locking; mixed index for text/geo; vertex-centric indexes for supernodes. NFR: needs a separately operated distributed store (Cassandra/Scylla/HBase) and optional ES/Solr; Java 11+ (1.2.0), Java 8 dropped; index provisioning is an operational step with reindex; consistency tuning is the operator's job.

## 7. Performance and resource model

No benchmark was retrieved for 1.1.0 or 1.2.0, so there are **no performance numbers** in this file. Qualitative, from docs: indexed equality lookups are backend point reads; unindexed predicates are full scans; supernode traversals depend on vertex-centric indexes; lock-based consistency costs extra commit round trips and risks deadlock under write conflicts [CLAIM-janusgraph-05][CLAIM-janusgraph-06]. Resource model: JVM heap on server nodes plus the backend cluster (Cassandra replicas, ES nodes); BerkeleyJE is explicitly non-distributed and typically for testing. Failure modes: ghost vertices, stale index entries, clock skew under locking, reindex stalls.

## 8. Strengths and use-case-specific advantages

| ID | Strength | Match or exceed |
|---|---|---|
| STR-janusgraph-01 | Apache-2.0 with no edition split; redistribution-safe | Reference for an EOIP default-bundled backend alongside HugeGraph (Apache-2.0) |
| STR-janusgraph-02 | Pluggable storage/index SPI: reuse existing Cassandra/Scylla/HBase estates | Pattern for EOIP `GraphStore` plus index SPI |
| STR-janusgraph-03 | Vertex-centric indexes for supernodes (CAP-07) | Adopt as an explicit "supernode policy" in EOIP traversal plans |
| STR-janusgraph-04 | Index lifecycle with reindex and `force-index` guard against silent scans | Adopt as a conformance rule: EOIP refuses to run template queries lacking an index |

Strength cards: STR-janusgraph-04 | JanusGraph | `force-index` | [CLAIM-janusgraph-06] | prevents accidental full scans in multi-tenant production | match | adapter `ensure_schema` creates indexes and deployment config sets `force-index` | a query without an index fails fast in the conformance suite. STR-janusgraph-03 | JanusGraph | vertex-centric | [CLAIM-janusgraph-06] | impact queries through hub nodes | match | per-label/direction sort-key indexes and degree-capped traversal | 100k-degree hub 2-hop under time budget.

## 9. Limitations with root causes

| Class | Item | Type | Evidence |
|---|---|---|---|
| Algorithmic | Consistency inherited from backend; locking opt-in, clock dependent, deadlock-prone; ghost vertices permanent | intentional trade-off / verified | [CLAIM-janusgraph-05] |
| Algorithmic | Unindexed queries fall back to full scan; composite needs all keys with equality | verified | [CLAIM-janusgraph-06] |
| Operational | Two to three systems to operate (server, store, index); reindex procedures; one-way index inlining | verified | [CLAIM-janusgraph-03][CLAIM-janusgraph-06] |
| Maturity | 23 months between stable releases; 1.2.0 still pre-release; 507 open issues | verified | [CLAIM-janusgraph-01][CLAIM-janusgraph-08] |
| Friction | TinkerPop 3.8 breaks semantics; Java 8 dropped; Elasticsearch 6.0 dropped | verified | [CLAIM-janusgraph-02] |
| Security | Authentication only; no tenant/row authorization | docs gap (NOT PUBLICLY VERIFIED beyond docs read) | [CLAIM-janusgraph-07] |
| Adapter | See section 5.1 findings | observed | [CLAIM-janusgraph-09] |

## 10. Deployment, licensing, redistribution, operational viability

Licence: Apache-2.0 for code (repo carries `APACHE-2.0.txt`, `LICENSE.txt`, docs CC-BY-4.0), no commercial edition, "all functionality free" [CLAIM-janusgraph-04][CLAIM-janusgraph-08]. Redistribution-safe in principle; **dependencies drive the risk**: Cassandra and HBase are Apache projects (general knowledge); ScyllaDB edition terms, Elasticsearch licence history (SSPL/Elastic/AGPL options) and Oracle BerkeleyDB JE (used for tests; Sleepycat/AGPL-class) are UNVERIFIED and need legal check if bundled. A redistribution-safer stack would pair Cassandra with OpenSearch (1.2.0 supports OpenSearch 2/3) [CLAIM-janusgraph-02].

Air-gap: fully self-hosted, no cloud dependency: viable. One-node first: BerkeleyJE or inmemory on one JVM works, but a distributed-store deployment is heavy; HugeGraph with RocksDB is lighter on one node. Backend neutrality: it is one of the declared adapter targets (BL-05). Tenancy: none native; would need label/property partitioning or separate graphs (`graph` names in Gremlin Server config) plus an authorization layer [CLAIM-janusgraph-07].

## 11. Competitive delta against the EOIP verified baseline

| Area | JanusGraph | EOIP baseline | Delta |
|---|---|---|---|
| Adapter | Gremlin HTTP server | BL-05 Implemented/live-unverified; BL-07 conformance Partial | adapter has findings 1-10 above; none live-tested |
| Schema/index | explicit management API, index lifecycle | adapter schema-flexible, no-op | gap: index provisioning (CAP-08, CAP-18) |
| Supernodes | vertex-centric index | BL-43 Python algorithms, U-06 unmeasured | EOIP lacks supernode policy |
| Consistency | explicit locking/FORK | BL-24/BL-25 idempotent events | EOIP upsert idempotent only if unique index + lock |
| Security | authentication only | BL-19, BL-18 Absent, BL-20 Partial | neither enforces source ACL |
| Licence | Apache-2.0 | BL-22 licensing | strong match for redistribution |
| Query | Gremlin only | BL-08/BL-09 | covered by typed plans |

## 12. Strength-adoption and inversion cards

**INV-janusgraph-01** — Target: EOIP JanusGraph adapter against JanusGraph 1.1.0. Limitation: property-key prefix mismatch and no index provisioning (section 5.1 #1, #2) mean the adapter is functionally partial and slow beyond tiny graphs. Root cause: coupling/maturity of the EOIP adapter (hypothesis until live run; mechanism proven from source). Option 1 (quick integration): fix key naming, bind labels/keys, add a composite unique index creation script; Option 2 (native enhancement): `ensure_schema` using the management API over a Gremlin script, `LOCK` consistency on `canonical_id`/`edge_key`, batch loads using `inject()`/`unfold()` for chunked upserts, set server-side timeout; Option 3 (long-term): backend-capability descriptor (`requires_index`, `consistency`) in the `GraphStore` protocol so conformance checks it for every backend. Selected: 2. Sketch: `g.inject(batch).unfold().as('r')...coalesce(V().has('canonical_id', select('r').select('cid')), addV(select('r').select('label')))`. POC: JanusGraph 1.1.0 + Cassandra 4.0.6 + OpenSearch, 1M vertices/5M edges via adapter before/after; success: `find_vertices(filters)` returns expected sets, 1,000 canonical lookups with p95 under 20 ms on one node, zero duplicates under 16 concurrent upsert writers; dataset: synthetic enterprise dependency graph. Dependencies: BL-07 conformance; migration: existing graphs with `p_`-prefixed keys need a copy-property migration; rollback: keep both key styles on read. Failure case: LOCK deadlocks under hub writes. Defensibility: conformance plus capability descriptor benefits every backend. Decision: ADOPT.

**INV-janusgraph-02** — Target: JanusGraph consistency. Limitation: backend-dependent consistency, ghost vertices [CLAIM-janusgraph-05]. Root cause: storage/coupling (proven). Alternative: EOIP applies idempotent SourceEvents and tombstones (BL-24/25) and treats the backend as an eventually consistent projection with reconciliation scans; worse when strict uniqueness is required. Options: (1) LOCK on unique keys; (2) reconciliation job comparing revision log with graph; (3) event-sourced rebuild per backend. Selected 2 plus 1. POC: kill a Cassandra node during bulk load; success: reconciliation restores expected counts. Decision: EXPERIMENT. Seed hypotheses (Master Prompt §10.5): none targets JanusGraph; "fixed vendor query languages via typed query plans plus adapters" is consistent with BL-08.

**INV-janusgraph-03** — Target: adapter query construction. Limitation: string-built labels/keys (5.1 #3). Root cause: coupling (hypothesis). Fix: bind everything; for TinkerPop 3.8 evaluate the typed driver over HTTP or `gremlin-python`. Decision: ADOPT for binding; DEFER driver change.

## 13. Per-capability decisions

| Capability | Decision | Note |
|---|---|---|
| CAP-01 as backend | INTEGRATE (existing adapter) after fixes | INV-01 |
| CAP-05 distributed scale-out | REUSE (delegated to Cassandra/Scylla/HBase) | |
| CAP-07 supernode handling | BUILD policy in EOIP plans, use vertex-centric indexes | |
| CAP-08 schema/index | BUILD `ensure_schema` | |
| CAP-13 Gremlin | REUSE | pin TinkerPop 3.7.x until 3.8 retested |
| CAP-18 index/force-index guard | BUILD conformance rule | |
| CAP-46/CAP-47 ACL/tenancy | BUILD in EOIP layer | not native |
| CAP-53 vector | REJECT as JanusGraph role | use C10 engines |
| CAP-62 algorithms | REUSE TinkerPop OLAP only if Spark exists; else EOIP | |
| CAP-74/76 backup/HA | REUSE backend features | |
| CAP-77 licence | REUSE (Apache-2.0) with dependency review | |

## 14. Tests, POC, acceptance

1. Live stand-up: JanusGraph 1.1.0 (TinkerPop 3.7.3) + Cassandra 4.0.6 + OpenSearch/ES 8.15.3 via compose; run `tests/runtime_*` plus `graph/conformance.py`; acceptance: all GraphStore operations pass; record outcomes for findings 1, 4, 6.
2. Property round-trip test: upsert `{canonical_id, name}`; `find_vertices(filters={name})` returns it.
3. Concurrency: 16 writers upserting the same 1,000 ids with and without LOCK; count duplicates.
4. Injection test: label/key with `${1+1}` and quotes; assert no evaluation.
5. Version gate: repeat on 1.2.0 when GA; compare Gremlin semantics.
6. Index guard: `force-index` on; assert template queries all use indexes.

## 15. Risks, trade-offs, open research questions

Risks: stagnant release cadence; TinkerPop 3.8 migration; operating three systems; dependency licences (BerkeleyDB, Elasticsearch, Scylla); adapter correctness unproven live. Open: is 1.2.0 GA imminent; HTTP request format under TinkerPop 3.8; db-cache semantics under multi-writer; vertex partitioning for supernodes; whether `property(k, v)` cardinality defaults changed in 3.8; community Cypher support; vector via mixed index.

---

## Appendix A — Research-dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Apache-2.0, LF, cadence, pre-release 1.2.0 |
| D2 | 2 | Distributed OLTP graph |
| D3 | 4 | Server, core, storage/index SPI |
| D4 | 5 | edgestore columns, composite/mixed/vertex-centric |
| D5 | 3,5 | Schema API, cardinality, no ontology |
| D6 | 5 | Gremlin strategies, index selection, full-scan fallback |
| D7 | N/A | None |
| D8 | 5,7 | Backend-dependent consistency, locking, FORK |
| D9 | 5.1 | Per-item HTTP in adapter; OLAP via Hadoop/Spark |
| D10 | N/A | No ER/evidence features |
| D11 | N/A | No native temporal |
| D12 | 3 | OLAP via TinkerPop |
| D13 | 3 | No vector/RAG |
| D14 | N/A | Not examined |
| D15 | N/A | No governance features |
| D16 | N/A | No UI |
| D17 | 3,5.1 | Drivers, management API |
| D18 | 5,9 | Auth only; script injection hypothesis |
| D19 | 10 | No tenancy |
| D20 | 7 | No numbers |
| D21 | 10 | Free Apache-2.0; dependency licences |
| D22 | 3 | Gremlin only; GraphSON |
| D23 | N/A | Not examined |
| D24 | App. C | Official docs; adapter observed |

## Appendix B — Capability mapping

| CAP-ID | JanusGraph | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-01 | native | CLAIM-janusgraph-06 | BL-05 Implemented/unverified | INTEGRATE | P1 |
| CAP-05 | native via backend | CLAIM-janusgraph-04 | BL-02 | REUSE | P2 |
| CAP-06 | partial | CLAIM-janusgraph-09 | BL-05 per-item | BUILD batching | P2 |
| CAP-07 | native | CLAIM-janusgraph-06 | BL-43 | BUILD policy | P2 |
| CAP-08 | native | CLAIM-janusgraph-06 | adapter no-op | BUILD | P1 |
| CAP-13 | native | CLAIM-janusgraph-02 | BL-05 | REUSE | P1 |
| CAP-14 | unknown | CLAIM-janusgraph-04 | BL-03 | n/a | P3 |
| CAP-18 | partial | CLAIM-janusgraph-06 | BL-07 | BUILD conformance rule | P2 |
| CAP-19 | native | CLAIM-janusgraph-06 | BL-43 | REUSE | P2 |
| CAP-44 | partial | CLAIM-janusgraph-07 | BL-19 | REUSE | P2 |
| CAP-46 | absent | CLAIM-janusgraph-07 | BL-18 Absent | BUILD | P0 |
| CAP-47 | absent | CLAIM-janusgraph-07 | BL-20 Partial | BUILD | P0 |
| CAP-50 | native | CLAIM-janusgraph-04 | BL-45 | INTEGRATE | P2 |
| CAP-53 | absent | CLAIM-janusgraph-04 | BL-14 | REJECT | P3 |
| CAP-77 | Apache-2.0 | CLAIM-janusgraph-04 | BL-22 | REUSE | P2 |

## Appendix C — Evidence records (access 2026-10-26)

| CLAIM-ID | Product/version/date | Claim | Class | Source | Pub/access | Conf | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-janusgraph-01 | releases | v1.2.0 pre-release 2026-10-25; v1.1.0 published 2024-11-09; v1.0.1 2024-11-08; v1.0.0 2023-10-22 | Officially documented | api.github.com/repos/JanusGraph/janusgraph/releases | 10-26 | 0.9 | 1.1.0 notes date 2024-11-07 |
| CLAIM-janusgraph-02 | 1.2.0 | TinkerPop 3.8.2 (changes semantics), Java 11+, Java 8 dropped, Cassandra 5.0, ES 9, OpenSearch 2/3, Solr 9, CDC mixed-index sync, WRITE_ONLY_ENABLED; notes dated 2026-10-28 vs published 10-25 | Officially documented | github.com/JanusGraph/janusgraph/releases/tag/v1.2.0 | 2026-10-25 / 10-26 | 0.85 | date mismatch; pre-release |
| CLAIM-janusgraph-03 | 1.0.0 / 1.1.0 | 1.1.0 (2024-11-07): TinkerPop 3.7.3, irreversible inline composite index, JSON schema; 1.0.0 (2023-10-21): TinkerPop 3.7.0, string vertex IDs, Java 11 | Officially documented | JanusGraph Changelog, docs.janusgraph.org/changelog/ | 10-26 | 0.9 | none |
| CLAIM-janusgraph-04 | project | Apache-2.0; LF since 2017, LF AI & Data; storage Cassandra/HBase/Bigtable/BerkeleyJE/ScyllaDB (+community Aerospike, DynamoDB, FoundationDB); index ES/Solr/Lucene | Officially documented | janusgraph.org | 10-26 | 0.9 | licence name stated on site; repo files consistent |
| CLAIM-janusgraph-05 | docs | Locking opt-in, clock-dependent, deadlock risk, quorum caveat, FORK, stale index entries, permanent ghost vertices, buffer-size batching | Officially documented | Eventually-consistent storage backends, docs.janusgraph.org/advanced-topics/eventual-consistency/ | 10-26 | 0.9 | none |
| CLAIM-janusgraph-06 | docs | Composite vs mixed index; vertex-centric indexes in edgeStore; reindex lifecycle; full-scan fallback; force-index | Officially documented | Index performance, docs.janusgraph.org/schema/index-management/index-performance/ | 10-26 | 0.9 | none |
| CLAIM-janusgraph-07 | docs | HTTP/WS channelizers; Basic, SASL, HMAC auth; separate credentials store | Officially documented | Server operations, docs.janusgraph.org/operations/server/ | 10-26 | 0.85 | authorization/sandboxing not covered by page |
| CLAIM-janusgraph-08 | repo | ~5.9k stars, 1.2k forks, 507 issues, 71 PRs, DCO, security policy | Officially documented | github.com/JanusGraph/janusgraph | 10-26 | 0.8 | counts change daily |
| CLAIM-janusgraph-09 | EOIP adapter | Bindings for values, inline json.dumps labels/keys, `p_` key prefix, no-op ensure_schema, per-item bulk load, unused vertex_id, tombstone return | Observed in source code | `packages/eoip/adapters/janusgraph.py` lines cited in 5.1 | working tree / 10-26 | 0.85 (static; not run live) | BL-05 says Implemented/live-unverified |

## Appendix D — Assumptions

A1: JanusGraph source code was not read; storage layout is described from documentation and flagged where inferred. A2: Dependency licences (Scylla, Elasticsearch, BerkeleyDB) are noted as UNVERIFIED legal-check items, not conclusions. A3: Adapter findings 1, 3, 4, 9, 10 are static-reading hypotheses until a live run (U-01). A4: Access date 2026-10-26. A5: "Titan lineage" and schema.default/cache behaviour are general knowledge, not separately sourced.
