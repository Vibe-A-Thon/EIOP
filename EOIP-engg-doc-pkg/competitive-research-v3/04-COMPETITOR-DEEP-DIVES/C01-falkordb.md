# C01 — FalkorDB

| Field | Value |
|---|---|
| Registry ID | T-C01-falkordb |
| Tier | A (RedisGraph successor lineage; GraphRAG-oriented candidate backend; SSPL licence is a legal-review trigger) |
| Versions examined | v6.0.3 (2026-10-22, Rust-engine line); v6.0.0 (2026-09-29); v4.22.2 (2026-10-20, C-engine line); RedisGraph 2.x (EOL). Docs at docs.falkordb.com as of access date |
| Verified on | 2026-10-26 (brief says 2026-10-18; actual access date used) |
| Worker | V01 |

Cross-reference: Memgraph (the other in-memory Cypher/GraphRAG candidate) is in `C01-memgraph.md`; this file does not repeat its analysis. RedisGraph is in `C01-tier-c-records-V01.md`.

## 1. Identity, current status, tier, and sources

FalkorDB (FalkorDB Ltd; repo `github.com/FalkorDB/FalkorDB`, ~10.5k stars, 630 open issues) is an in-memory property-graph database delivered as a Redis module, queried with openCypher plus proprietary extensions over the Redis protocol (`GRAPH.QUERY`, `GRAPH.RO_QUERY`) [CLAIM-falkordb-01]. It is the declared direct successor of RedisGraph: same `GRAPH.*` command API, reads RedisGraph RDB files, built by "the engineers behind the original project" [CLAIM-falkordb-07]. The vendor docs do not use the word "fork"; the lineage is codebase continuation (the third-party components page lists RedisGraph itself as a bundled component) [CLAIM-falkordb-05].

Status: **active, two release lines in parallel.** v6.0.x (first release 2026-09-29) replaces the C engine with a new Rust query engine and is built on Redis 8.10.2; v4.22.x (C engine) is still released (2026-10-15, 2026-10-20) [CLAIM-falkordb-03][CLAIM-falkordb-04]. v6.0.1/6.0.2/6.0.3 shipped within 22 days; v6.0.3 is a bug-fix release including several crash/corruption fixes on restore, RDB decoding and bulk import [CLAIM-falkordb-17]. Maturity of the Rust line is therefore **early-production**.

Resolution of Master Prompt §5.6: RedisGraph reached end of sale 2023-07-05 and end of support 2025-01-31; its repo went to maintenance mode and was to be tagged deprecated on 2025-02-01 [CLAIM-falkordb-06]. FalkorDB is the successor lineage. No material name collision found.

Sources (14): see Appendix C.

## 2. Primary problem, target workloads, concrete example workflows

Vendor positioning: low-latency graph store for GraphRAG and agent memory, plus multi-tenant SaaS with many small graphs [CLAIM-falkordb-15]. Workloads that fit: (a) per-tenant knowledge graphs of modest size held in RAM; (b) GraphRAG retrieval combining vector, full-text and Cypher; (c) fraud/identity/relationship lookups with shallow multi-hop traversal.

Example EOIP workflows: (1) per-tenant "personal brain" graph for agent memory with one FalkorDB graph key per tenant; (2) impact queries (service account -> dependent systems) as 2-4 hop Cypher over a RAM-resident dependency graph; (3) GraphRAG SDK building a document graph from local models via LiteLLM/Ollama [CLAIM-falkordb-10].

Unsuited: graphs larger than RAM, long-running OLAP over billions of edges, workloads needing multi-statement ACID transactions (not documented; see section 5).

## 3. Feature inventory

| Feature | Status | Notes |
|---|---|---|
| Property graph, openCypher | present | Proprietary extensions; four documented Cypher limitations [CLAIM-falkordb-14] |
| Gremlin / SPARQL / GQL / SQL-PGQ | absent | No evidence in docs read |
| RESP (Redis) protocol | present | Docs index lists Bolt support; another docs note says Bolt is not used: UNVERIFIED [CLAIM-falkordb-07] |
| Vector index (HNSW) | present | Node and edge properties, cosine/euclidean, 1-4096 dims [CLAIM-falkordb-09] |
| Full-text index | present | RediSearch-based; scoring defaults to TFIDF in v6 [CLAIM-falkordb-04] |
| Multi-graph per instance | present | One graph per Redis key; vendor claims >10,000 graphs/instance [CLAIM-falkordb-15] |
| Graph copy | present | `GRAPH.COPY` includes indexes and constraints |
| Constraints (unique) | present | UNIQUE constraints backed by index lookups [CLAIM-falkordb-17] |
| Algorithms (centrality, community, flow, paths) | partial | Some (A*, CCH, Leiden/Louvain) not yet ported to Rust engine [CLAIM-falkordb-04] |
| Clustering | present | Redis Cluster hash slots; each graph on one shard [CLAIM-falkordb-12] |
| Replication | present | v6: replicas apply effects; no automatic failover standalone [CLAIM-falkordb-12] |
| Persistence | present | RDB + AOF [CLAIM-falkordb-12] |
| Browser UI | present (bundled) | FalkorDB Browser; not examined |
| GraphRAG SDK (Python) | present, separate | LiteLLM; licence not stated on docs page [CLAIM-falkordb-10] |
| MCP server | present, separate | MIT per third-party listing; read-only mode [CLAIM-falkordb-11] |
| Per-graph ACL / authz | unknown | Only global `requirepass` example found [CLAIM-falkordb-13] |
| Bitemporal / versioning | absent | |
| Source-ACL, tenant policy | absent | Application must implement |
| Managed cloud (FalkorDB Cloud) | present | Out of scope for EOIP |

## 4. Architecture diagram

```
 client (RESP: GRAPH.QUERY / RO_QUERY / BULK / COPY, FT.*, vector procs)
        |
 +------v---------------- Redis 8.x process (v6) ----------------------+
 | Redis event loop (network, RDB/AOF, replication, cluster bus)       |
 |   +-- FalkorDB module                                               |
 |        thread pool (THREAD_COUNT)  <- read/write query workers      |
 |        parser -> AST -> algebraic expressions -> plan (ops) -> run  |
 |        graph key = {node store, per-label & per-reltype sparse      |
 |        matrices (GraphBLAS), property attr sets, indexes}           |
 |        RediSearch 8.x (full-text + HNSW vector)                     |
 +--------------------------------------------------------------------+
   RAM-resident state  --RDB/AOF-->  disk       primary --effects--> replicas
 cluster: key slot -> shard (one graph never spans shards)
 side services: GraphRAG SDK (python, LiteLLM) ; MCP server (node/http) ; Browser
```

## 5. Under-the-hood reconstruction

Evidence note: the design page describes the C-engine era (4.x); the v6 Rust engine is documented only through release notes [CLAIM-falkordb-04]. Items marked (H) are hypotheses.

**Data model.** Labeled property graph. Per graph: one "THE adjacency matrix" (any relationship), one matrix per relationship type (rows source, columns destination, entry = relationship id), one diagonal matrix per label [CLAIM-falkordb-08]. Matrices live in RAM in GraphBLAS CSC sparse format (vendor says format may change). Node insertion extends matrices; relationship insertion sets one entry (vendor: O(1); vendor throughput numbers, hardware unspecified).

**Storage and indexing.** Entire graph in memory; persistence by Redis RDB/AOF; RDB decoding bugs were still being fixed in v6.0.3 [CLAIM-falkordb-17]. Secondary indexes: range, full-text, vector (HNSW, M=16, efConstruction=200, efRuntime=10 default; about 3 GB per 1M x 768-d float32 vectors per vendor) [CLAIM-falkordb-09]. Indexes do not serve `<>` filters [CLAIM-falkordb-14].

**Query pipeline.** Lex/Lemon-built openCypher parser -> AST -> pattern turned into linear-algebra expression (`(a)-[A]->(b)-[B]->(c)` becomes `A * B`), reordered using associativity to favour sparse intermediates -> filter trees -> operation plan (filtered traverse, conditional traverse, filter, project) -> result set [CLAIM-falkordb-08]. Traversal as sparse matrix multiply means a k-hop frontier expansion is a batched operation, not pointer chasing; cost is driven by frontier nnz, which would explain good shallow multi-hop behaviour and weaker behaviour for property-selective point lookups (H). Plan cache holds 25 query shapes by default, not results [CLAIM-falkordb-13].

**Reasoning.** None (no RDFS/OWL/Datalog). Cypher only.

**Concurrency and transactions.** A thread pool (default = logical cores) bounds concurrent queries; OpenMP threads cap GraphBLAS parallelism per query; writes buffer in pending-change deltas (`DELTA_MAX_PENDING_CHANGES` default 10,000) [CLAIM-falkordb-13]. Timed-out writes are rolled back. The docs read do not state write serialisation, isolation level, or multi-statement transactions: **NOT PUBLICLY VERIFIED**. Known semantic quirks: relationship uniqueness not enforced for unreferenced pattern edges; LIMIT does not bound eager CREATE/SET/MERGE [CLAIM-falkordb-14].

**Partitioning and consistency.** Redis Cluster slots; an entire graph resides on one shard, so a single graph cannot scale out horizontally; scale-out is across graphs (tenants) [CLAIM-falkordb-12]. v6 replication ships effects (v3 format) instead of re-executing queries; 4.x and 6.0 nodes cannot share a replica set [CLAIM-falkordb-04]. Failover needs Sentinel/cluster manager.

**Caching.** Query-plan cache only. **Versioning.** None native. **Security.** Global password (`requirepass`) shown; Redis ACL users are a Redis feature but per-graph key-pattern ACL for FalkorDB is not documented in the pages read: UNVERIFIED. Result cap 10,000 rows is the only default resource control; query memory and queue limits are unlimited by default [CLAIM-falkordb-13].

## 6. Functional and non-functional requirements inferred

FR: openCypher read/write; named multiple graphs; vector+full-text+range indexes; bulk load; graph copy; RDB-compatible migration. NFR: whole working set in RAM (plan raw vector payload plus about 20% HNSW overhead plus graph); write concurrency model not confirmed; restart time = RDB load time; version lockstep across replica sets; operational need for Sentinel or cluster for HA.

## 7. Performance and resource model

No independent benchmark of v6 found. Vendor claims: 496x lower P99 than Neo4j (homepage, 820K nodes/9.8M edges, setup not published) versus a Dec-2024 blog showing 136.2 ms vs 46,923.8 ms P99 (about 344x by our arithmetic) on SNAP Pokec, 11 templated queries, 82/18 read/write, 16 CPU/32 GB [CLAIM-falkordb-16]. Different runs, not reconciled, vendor-run, and predating the Rust engine (a maintainer reportedly says C and Rust now benchmark at parity). Scaling claim: 20k to 120k QPS from 1 to 6 nodes (marketing, undocumented). Resource model: memory-bound; index builds slow on large data. Failure modes: OOM kills (no default query memory cap), queue growth (unlimited `MAX_QUEUED_QUERIES`), corruption-on-restore fixes still landing in v6.0.3.

## 8. Strengths and use-case-specific advantages

| ID | Strength | How to match or exceed |
|---|---|---|
| STR-falkordb-01 | Algebraic (GraphBLAS) multi-hop expansion; strong for shallow-hop RAM graphs | Integrate as optional accelerator; study matrix-frontier technique (GraphBLAS is Apache-2.0) |
| STR-falkordb-02 | Many isolated small graphs per instance (graph-per-key) | Native-per-tenant graph placement pattern; EOIP tenancy POOL/SILO map onto it |
| STR-falkordb-03 | One engine for graph + HNSW vector + full-text, with GraphRAG SDK and MCP | Match with backend-neutral hybrid retrieval over any backend |
| STR-falkordb-04 | RedisGraph RDB migration path | Pattern: documented import from predecessor formats |

Strength cards (STR-ID | competitor | strength | evidence | value | decision | design | test):
- STR-falkordb-02 | FalkorDB | graph-per-tenant key | [CLAIM-falkordb-12][CLAIM-falkordb-15] | cheap hard isolation unit for small tenants (BL-20 gap) | integrate pattern | EOIP `GraphStore` receives tenant->graph-key mapping; refuse queries outside it | cross-tenant read attempt returns zero rows in a 1,000-tenant test
- STR-falkordb-03 | FalkorDB | single engine hybrid retrieval | [CLAIM-falkordb-09][CLAIM-falkordb-10] | fewer moving parts on one node | match (optional) | optional backend module only | hybrid-vs-BM25+dense baseline per Master Prompt §5.3

## 9. Limitations with root causes

| Class | Item | Type | Evidence |
|---|---|---|---|
| Licensing | SSPLv1 on core; Redis/RediSearch tri-licensed RSALv2/SSPLv1/AGPLv3 | licensing restriction | [CLAIM-falkordb-01][CLAIM-falkordb-05] |
| Algorithmic | Graph cannot span shards; RAM-bound | intentional trade-off | [CLAIM-falkordb-12][CLAIM-falkordb-08] |
| Algorithmic | Cypher quirks: edge uniqueness, LIMIT vs eager ops, no `<>` index, no aggregates in pattern comprehensions | verified limits | [CLAIM-falkordb-14] |
| Algorithmic | Vector search does not combine with property filters; post-filter only | verified limit | [CLAIM-falkordb-09] |
| Operational | Version lockstep (4.x vs 6.0); two engines in market; restore corruption fixes ongoing | verified | [CLAIM-falkordb-04][CLAIM-falkordb-17] |
| Operational | Unlimited default memory/queue; 10k default result cap | verified config | [CLAIM-falkordb-13] |
| Friction | Per-graph authz, audit, transactions not documented | NOT PUBLICLY VERIFIED | n/a |
| Outdated claim | Benchmarks pre-date Rust engine; two inconsistent multipliers | vendor marketing | [CLAIM-falkordb-16] |

Root causes: coupling to the Redis process (single process memory, key = graph, Redis licence inherited); sparse-matrix model optimised for traversal rather than selective property predicates (H).

## 10. Deployment, licensing, redistribution, operational viability

**Licence (legal-review trigger, not a legal conclusion).** FalkorDB core is SSPLv1 (MongoDB text, 2018-10-16) [CLAIM-falkordb-01]. Vendor FAQ: internal use, closed-source apps not exposing FalkorDB as a service, evaluation, and redistribution inside an application that is not offered as a service do not require source disclosure; offering FalkorDB "as a service" to external users requires open-sourcing the associated codebase or a commercial licence; OEM/embedding terms are **not defined** and need a conversation with FalkorDB Ltd [CLAIM-falkordb-02]. Triggers for EOIP: (1) white-label SaaS or managed hosting of EOIP with FalkorDB inside; (2) bundling the binary or image in a distributed appliance (scope of the SSPL service clause is the open question); (3) the bundled Redis 8 component is itself RSALv2/SSPLv1/AGPLv3 (choose-one) [CLAIM-falkordb-05]; (4) SDK/GraphRAG SDK/MCP licences differ per repo (MCP listed MIT, SDK unstated). Not OSI open source; do not describe it as such.

**Air-gap.** Self-hosted container/binary, no mandatory cloud: viable. GraphRAG SDK supports local models via LiteLLM [CLAIM-falkordb-10]; egress policy must still wrap it. **One-node first:** yes; HA needs replicas plus Sentinel. **Tenancy:** graph-per-key is a usable isolation unit but not enforced by EOIP adapters today (BL-20).

## 11. Competitive delta against the EOIP baseline

| Area | FalkorDB | EOIP baseline | Delta |
|---|---|---|---|
| Backends | one engine | BL-01..07: HugeGraph, Neo4j, Neptune, Janus, Fuseki, GraphDB, memory; no FalkorDB adapter | gap: no adapter; Cypher adapter pattern (BL-03) reusable over Redis protocol |
| Vector | HNSW inside graph | BL-14 pure-Python HNSW, hashing default | FalkorDB offers native index (not filter-aware) |
| Tenancy | graph-per-key | BL-20 contract only | pattern to adopt |
| Query | openCypher | BL-08 typed bounded plans, BL-59 no GQL | EOIP plans compile to templates, which suit a Cypher backend |
| Reasoning/temporal | none | BL-30, BL-37 app-layer | no delta; EOIP keeps app-layer |
| GraphRAG | SDK + MCP | BL-16, BL-47 | EOIP lacks benchmark vs plain RAG; FalkorDB publishes GraphRAG-Bench pages (not evaluated) |
| ACL | none documented | BL-18 absent | neither solves it |

## 12. Strength-adoption and inversion cards

**INV-falkordb-01** — Target FalkorDB v6.0.3, single large graph. Limitation: a graph cannot span shards; RAM-bound [CLAIM-falkordb-12]. Root cause: storage/coupling (proven for sharding; RAM from design doc). Alternative: EOIP keeps backend neutrality and partitions by tenant/domain across backends; worse when a single tenant exceeds one node's RAM and the chosen backend is FalkorDB. Options: (1) quick: cap FalkorDB use to tenants below an entity budget; (2) native: router that places each tenant graph on a backend by size/profile; (3) long-term: placement-aware federated query over HugeGraph (large) and FalkorDB (hot subgraph cache). Selected: (2). Sketch: `placement(tenant)->backend,graph_key`; hot-subgraph cache refilled from authoritative HugeGraph with permission filtering. POC: 100 tenants x 1M edges, measure p95 2-hop and RAM per tenant against Neo4j Community; success p95 under 50 ms and RAM within budget. Dependencies: BL-20 fix first; privacy failure case: cache holds data after source ACL revocation, so cache must key on ACL hash (BL-17). Defensibility: placement policy plus ACL-aware cache is EOIP-specific. Decision: EXPERIMENT.

**INV-falkordb-02** — Target FalkorDB vector+graph retrieval. Limitation: vector queries do not combine with property filters, post-filter only [CLAIM-falkordb-09]; for ACL-filtered retrieval this wastes ranking budget and, if filtering happens after retrieval of foreign-tenant vectors, violates least privilege. Root cause: algorithm (HNSW without filtered traversal; proven by docs). Alternative: EOIP applies tenant/ACL pre-filter by partitioning (graph per tenant) plus post-filter inside the same trust boundary. Options: (1) quick: oversample k and post-filter; (2) native: per-tenant index; (3) long-term: filter-aware ANN. Selected: (2) via graph-per-tenant. POC: 10 tenants, plant canary vectors, assert zero cross-tenant results and recall at 10 of at least 0.95 versus filtered brute force. Decision: EXPERIMENT. Seed hypotheses in Master Prompt §10.5: none targets FalkorDB; the "typed query plans plus adapters" direction applies and is consistent with BL-08.

**INV-falkordb-03** — Target licensing. SSPLv1 blocks silent bundling in a white-label SaaS (section 10). Options: (1) quick: customer-supplied/optional install, never bundled; (2) native: commercial licence negotiation if FalkorDB becomes default; (3) long-term: ship an Apache-2.0 GraphBLAS-based traversal accelerator inside EOIP, independent of FalkorDB. Decision: ADOPT option (1) now; DEFER (3). Falsifier: legal review concludes bundling on-prem for customer self-hosting is outside the service clause, which would lift the restriction.

## 13. Per-capability decisions

| Capability | Decision | Note |
|---|---|---|
| CAP-01 property-graph storage (as backend) | EXPERIMENT | optional adapter, customer-supplied install, not bundled |
| CAP-14 openCypher | REUSE Neo4j adapter patterns | verify FalkorDB Cypher subset via conformance suite (BL-07) |
| CAP-47 tenant isolation via graph-per-key | EXPERIMENT | pattern, not dependency |
| CAP-53 vector search | DEFER native FalkorDB; keep EOIP pluggable | filter limitation |
| CAP-56 GraphRAG SDK | REJECT as dependency, EXPERIMENT as comparison baseline | licence unstated, FalkorDB-only |
| CAP-59 MCP | REFERENCE-ONLY for tool design; EOIP has its own (BL-47) | |
| CAP-19 / CAP-62 algebraic traversal | EXPERIMENT (study GraphBLAS) | |
| CAP-05 scale-out | REJECT as FalkorDB role | graph on one shard |

## 14. Tests, POC, acceptance

1. Stand up FalkorDB v6.0.3 and v4.22.2 in compose; run EOIP `graph/conformance.py` over a new Cypher-over-RESP adapter; acceptance: all required GraphStore operations pass or documented gaps.
2. Tenant-isolation canary test (INV-02) with 1,000 graph keys; acceptance zero leakage, p95 latency recorded.
3. Crash-restore test: kill -9 during bulk load, restart, verify counts; v6.0.3 corruption fixes make this mandatory.
4. Cypher quirks regression: the four documented limitations; acceptance that EOIP templates never rely on them.
5. Licence gate: written legal opinion before any bundling.
6. Reproduce vendor benchmark code on EOIP hardware; accept claims only with our own numbers.

## 15. Risks, trade-offs, open research questions

Risks: SSPL scope for white-label (legal); two engine lines; Rust engine maturity; RAM sizing; vendor dependency (small company). Open: per-graph ACL and audit; write isolation level; OEM terms; GraphRAG SDK licence; whether Bolt is supported; v6 benchmark parity; whether FalkorDB Ltd offers an OEM licence.

---

## Appendix A — Research-dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Identity, SSPLv1, active, two lines |
| D2 | 2 | GraphRAG, small multi-tenant graphs |
| D3 | 4 | Redis-module architecture |
| D4 | 5 | GraphBLAS CSC matrices, RAM, HNSW |
| D5 | 3,5 | Optional schema, constraints; no ontology |
| D6 | 5 | Algebraic plan; EXPLAIN exists (unexamined); no CBO detail |
| D7 | 5 | None |
| D8 | 5,7 | Thread pool, one shard per graph; isolation NOT PUBLICLY VERIFIED |
| D9 | 3 | Bulk loader; no connectors/CDC |
| D10 | N/A | No identity/evidence features |
| D11 | N/A | No temporal features |
| D12 | 3 | Basic algorithms; no ML |
| D13 | 3,8 | Vector, FT, GraphRAG SDK, MCP |
| D14 | 3 | SDK generates Cypher; accuracy not evaluated |
| D15 | N/A | No governance features |
| D16 | 3 | Browser UI not examined |
| D17 | 3 | Clients, SDKs; docs have llms.txt |
| D18 | 5,9 | Global password only found; UNVERIFIED ACL |
| D19 | 5,10 | Graph-per-key; no branding |
| D20 | 7 | Vendor numbers only |
| D21 | 10 | SSPL + commercial licence; cloud |
| D22 | 3,10 | RDB migration; Cypher export not examined |
| D23 | N/A | Not examined; no patents located |
| D24 | App. C | Mostly official docs; benchmarks vendor |

## Appendix B — Capability mapping

| CAP-ID | FalkorDB | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-01 | native | CLAIM-falkordb-08 | BL-01 Implemented | EXPERIMENT | P2 |
| CAP-04 | partial (RAM, single process) | CLAIM-falkordb-13 | BL-01 | DEFER | P3 |
| CAP-05 | partial (graph per shard) | CLAIM-falkordb-12 | BL-02 live-unverified | REJECT | P3 |
| CAP-08 | partial (constraints) | CLAIM-falkordb-17 | BL-28 | REUSE EOIP | P2 |
| CAP-14 | native (openCypher+ext) | CLAIM-falkordb-14 | BL-03/BL-59 | INTEGRATE | P2 |
| CAP-18 | partial | CLAIM-falkordb-08 | BL-08 | DEFER | P3 |
| CAP-47 | partial (graph-per-key) | CLAIM-falkordb-12 | BL-20 Partial | EXPERIMENT | P1 |
| CAP-50 | native self-hosted | CLAIM-falkordb-10 | BL-45 | INTEGRATE | P2 |
| CAP-52 | commercial licence needed | CLAIM-falkordb-02 | BL-21 | legal review | P1 |
| CAP-53 | native | CLAIM-falkordb-09 | BL-14 Partial | EXPERIMENT | P2 |
| CAP-54 | native | CLAIM-falkordb-04 | BL-13 | DEFER | P3 |
| CAP-56 | plugin (SDK) | CLAIM-falkordb-10 | BL-16 | EXPERIMENT | P2 |
| CAP-59 | plugin | CLAIM-falkordb-11 | BL-47 | REFERENCE-ONLY | P3 |
| CAP-62 | partial | CLAIM-falkordb-04 | BL-43 | DEFER | P3 |
| CAP-77 | SSPL | CLAIM-falkordb-01 | n/a | legal | P1 |

## Appendix C — Evidence records (access 2026-10-26 unless noted)

| CLAIM-ID | Product/version/date | Claim | Class | Source | Pub/access | Conf | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-falkordb-01 | repo, master | Core licensed SSPLv1; Redis module; openCypher+extensions; 10.5k stars | Officially documented | FalkorDB GitHub README/LICENSE.txt, github.com/FalkorDB/FalkorDB | n/a / 10-26 | 0.9 | none; Atlan says OSS status disputed |
| CLAIM-falkordb-02 | docs | FAQ: internal/closed-app/redistribution-not-as-service need no disclosure; service offering needs source or commercial licence; OEM undefined | Officially documented | FalkorDB License, docs.falkordb.com/References/license.html | n/a / 10-26 | 0.8 (summary of FAQ, not licence text) | none |
| CLAIM-falkordb-03 | GitHub releases | v6.0.3 2026-10-22; v4.22.2 2026-10-20; v4.22.1 10-15; v6.0.2 10-08; v6.0.1 10-01 | Officially documented | api.github.com/repos/FalkorDB/FalkorDB/releases | 10-26 | 0.95 | none |
| CLAIM-falkordb-04 | v6.0.0 2026-09-29 | Rust engine replaces C; Redis 8.10.2; RediSearch 8.6.1; effects replication; no 4.x/6.0 mixing; algorithms being ported | Officially documented | github.com/FalkorDB/FalkorDB/releases/tag/v6.0.0 | 10-26 | 0.85 (year inferred from sequence) | none |
| CLAIM-falkordb-05 | docs | GraphBLAS Apache-2.0; Redis, RediSearch, RedisGraph RSALv2/SSPLv1/AGPLv3 | Officially documented | Third-Party Components, docs.falkordb.com/design/third-party.html | 10-26 | 0.8 | page may lag v6 Redis 8 |
| CLAIM-falkordb-06 | RedisGraph | EOL announced 2023-07-05; end of support 2025-01-31; maintenance mode, deprecated tag 2025-02-01; RSALv2 or SSPLv1 | Officially documented | Redis blog "RedisGraph EOL", redis.io/blog/redisgraph-eol/ | 2023-07-05 (upd 2026-06-01) / 10-26 | 0.95 | none |
| CLAIM-falkordb-07 | docs | Direct successor, same GRAPH.* API, reads RDB; differences table | Officially documented | RedisGraph to FalkorDB migration, docs.falkordb.com/operations/migration/redisgraph-to-falkordb.md | 10-26 | 0.85 | docs index mentions Bolt, another note says no |
| CLAIM-falkordb-08 | docs (C-engine era) | Matrices per reltype/label, GraphBLAS CSC, algebraic traversal, Lex/Lemon parser | Officially documented | Design, docs.falkordb.com/design/ | 10-26 | 0.8 | v6 Rust engine may differ |
| CLAIM-falkordb-09 | docs | HNSW, cosine/euclidean, 1-4096 dims, M/ef defaults, about 3 GB per 1M x 768, weak filter combination | Officially documented | Vector index, docs.falkordb.com/cypher/indexing/vector-index.md | 10-26 | 0.85 | none |
| CLAIM-falkordb-10 | GraphRAG SDK | LiteLLM providers incl. local; incremental re-sync; licence not stated on page | Officially documented | docs.falkordb.com/genai-tools/graphrag-sdk.md | 10-26 | 0.8 | none |
| CLAIM-falkordb-11 | MCP server | Official, MIT, read-only mode, HTTP | Third-party report | Glama/mcpservers listings of FalkorDB/FalkorDB-MCPServer | 10-26 | 0.6 | READMEs disagree on details |
| CLAIM-falkordb-12 | docs | Redis Cluster slots, each graph one shard; replication no auto failover; RDB/AOF | Officially documented | Operations, docs.falkordb.com/operations/ | 10-26 | 0.8 | none |
| CLAIM-falkordb-13 | docs | THREAD_COUNT, timeouts, QUERY_MEM_CAPACITY unlimited, RESULTSET_SIZE 10000, CACHE_SIZE 25, global password | Officially documented | Configuration, docs.falkordb.com/getting-started/configuration | 10-26 | 0.85 | none |
| CLAIM-falkordb-14 | docs | Four Cypher limitations | Officially documented | Known limitations, docs.falkordb.com/cypher/known-limitations.html | 10-26 | 0.9 | none |
| CLAIM-falkordb-15 | vendor | >10,000 graphs per instance; multi-tenant in all plans | Third-party report (vendor FAQ via search) | falkordb.com FAQ pages | 10-26 | 0.5 | no methodology |
| CLAIM-falkordb-16 | vendor | 496x P99 homepage vs 136.2 ms/46,923.8 ms blog; Pokec; 16 CPU/32 GB | Third-party report | FalkorDB blog, falkordb.com/blog/graph-database-performance-benchmarks-falkordb-vs-neo4j/ ; Atlan review | 2024-12 / 10-26 | 0.6 | claims inconsistent; engine since changed |
| CLAIM-falkordb-17 | v6.0.3 | Bug-fix release: restore/RDB/bulk-import crash and corruption fixes; UNIQUE via index lookups | Officially documented | github.com/FalkorDB/FalkorDB/releases/tag/v6.0.3 | 2026-10-22 / 10-26 | 0.9 | none |

## Appendix D — Assumptions

A1: v6 release year 2026 inferred from release sequence. A2: Docs features (cluster, ACL) not deep-read; unread items marked UNVERIFIED. A3: "Verified on" uses actual access date 2026-10-26. A4: No code from the repo was read; reconstruction rests on docs and release notes, so source paths at pinned tags are not cited. A5: SSPL interpretation is out of scope (record only).
