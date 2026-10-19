# C01 — ArangoDB

| Field | Value |
|---|---|
| Registry ID | T-C01-arangodb |
| Tier | B — multi-model (document + graph + search + vector) reference; licence change from Apache 2.0 to BUSL-1.1 is directly relevant to EOIP redistribution |
| Versions examined | ArangoDB 3.12 series; latest patch listed in the official release notes: **3.12.12** (release date **UNVERIFIED**; Wikipedia lists 3.12.11 with conflicting August 2026 dates). 4.0 docs are labelled "under development, not released". Licence terms as of 3.12 (BUSL-1.1 source; ArangoDB Community License for binaries; 3.12.5+ Community Edition includes Enterprise features). |
| Verified on | 2026-10-18 |
| Worker | W06 |

## 1. Identity, current status, tier, and sources

**Identity.** ArangoDB, by ArangoDB Inc. (marketed under the "Arango" brand at arango.ai; documentation at docs.arango.ai), is a native multi-model database. It stores JSON documents in collections, keeps graphs as edge collections, has a search engine (ArangoSearch) and a vector index, and is queried with AQL. Repository: `github.com/arangodb/arangodb`. The repository is active, with its last push on 2026-10-17, and GitHub reports its licence as `NOASSERTION` because the text is BUSL, not a standard SPDX open-source licence [CLAIM-arangodb-07].

**Version status.** The official release-notes index lists 3.12 as the current series, with 3.12.12 as its latest patch, and says 4.0 is still in development [CLAIM-arangodb-05]. Versions 3.10 and 3.11 reached end of life on 30 May 2025 [CLAIM-arangodb-04]. A company product called "Arango Contextual Data Platform 4.0" was reportedly announced in March 2026 (third-party source). It is a platform/marketing release and is **not** the same as a released core database 4.0 [CLAIM-arangodb-06].

**Licence change (verified).** Starting with **3.12**, the source code licence changed from Apache 2.0 to the **Business Source License 1.1 (BUSL-1.1)**. Prepackaged Community Edition binaries come under a separate **ArangoDB Community License**, which limits production deployments to a **100 GiB dataset** and permits no commercial use beyond internal business purposes [CLAIM-arangodb-01]. The BUSL text names "ArangoDB Self Managed (Release Date: March 2024)" as the Licensed Work. Its Additional Use Grant allows internal production use but **not** "a commercial offering that allows one or more third parties" to access or manage databases. Each release converts to Apache 2.0 on its fourth anniversary [CLAIM-arangodb-02][CLAIM-arangodb-03]. From 3.12.5 the Community Edition includes all Enterprise features, but the download page says the edition gives no right "to distribute or embed within other products" [CLAIM-arangodb-04]. A "three clusters per organisation" limit appears in a secondary search summary only and is **UNVERIFIED** [CLAIM-arangodb-09].

## 2. Primary problem, target workloads, concrete example workflows

ArangoDB replaces a polyglot stack (document store + graph DB + search engine + vector DB) with one engine and one query language. Typical workloads are product and knowledge graphs with rich JSON entities, fraud and identity graphs, and hybrid search/vector/graph retrieval for GenAI. The vendor's current marketing centres on "contextual data" for AI agents [CLAIM-arangodb-06].

Example workflows mapped to EOIP:
- **J1 change impact as a single AQL query:** `FOR v, e, p IN 1..4 OUTBOUND 'stories/JIRA-1' GRAPH 'thread'` combined with filters on JSON properties of deployments.
- **Hybrid retrieval (J6):** ArangoSearch keyword match + `APPROX_NEAR_COSINE` vector lookup + graph expansion, all in one query plan [CLAIM-arangodb-10].

## 3. Feature inventory

| Area | Feature | Status (3.12) | Evidence |
|---|---|---|---|
| Data model | JSON documents, edge collections (`_from`/`_to`), named graphs | present | CLAIM-arangodb-11 |
| Query | AQL (document, graph traversal, search, vector functions) | present | CLAIM-arangodb-10 |
| Query | Gremlin / Cypher / GQL / SPARQL | absent natively (UNVERIFIED for third-party adapters) | — |
| Search | ArangoSearch (inverted index, ranking) | present; internals not re-verified | CLAIM-arangodb-08 |
| Vector | Faiss-based vector index (from 3.12.4); cosine, L2, inner product (3.12.6); approximate results via `nProbe`; enabling it is irreversible | present | CLAIM-arangodb-10 |
| Indexing | multi-dimensional indexes, wildcard search, transparent compression, external versioning | present (3.12) | CLAIM-arangodb-08 |
| Cluster | Agency (Raft), Coordinators, DB-Servers, hash sharding, synchronous per-shard replication, automatic failover | present | CLAIM-arangodb-12 |
| Enterprise graph features (SmartGraphs etc.) | sharding-aware graph placement | enterprise features, in Community Edition from 3.12.5 under Community License terms | CLAIM-arangodb-04 (feature names not re-verified) |
| Licensing | redistribution / embedding | **not granted** for Community binaries | CLAIM-arangodb-04 |
| Managed cloud | Arango managed platform | present (not examined) | — |
| Reasoning / ontology | — | absent | — |

## 4. Text-based architecture diagram

```
                 clients (HTTP/JSON, drivers, web UI)
                               |
                 +-------------v--------------+   stateless
                 |  Coordinators (AQL parse,  |   query plane
                 |  plan, distribute, Foxx)   |
                 +------+--------------+------+
           shard map    |              |   data-plane RPC
        +---------------v--+     +-----v-------------------+
        | Agency (odd # of |     | DB-Servers               |
        | Agents, Raft KV) |<--->|  shard leader / follower |
        | config, supervis.|     |  storage engine (RocksDB,|
        +------------------+     |  per 3.12 vector docs)   |
          control plane          |  docs | edges | search   |
                                 |  | vector (Faiss)        |
                                 +--------------------------+
   writes: Coordinator -> shard leader -> sync replicate to followers -> ack
   single-server mode: one process holds all roles except the Agency
```

[CLAIM-arangodb-12][CLAIM-arangodb-10]

## 5. Under-the-hood reconstruction

**Data model.** Documents are JSON with system attributes `_key`/`_id`/`_rev`. Edges are documents with `_from` and `_to` references, stored in edge collections. A named graph declares which edge collections connect which vertex collections [CLAIM-arangodb-11]. Graph and document data share one storage and query layer, which is the main architectural point.

**Storage and indexing.** The 3.12 vector-index docs say enabling the vector feature "permanently changes how the data is managed by the RocksDB storage engine", which confirms RocksDB as the storage engine [CLAIM-arangodb-10]. The vector index is built on Faiss. Searches probe a configurable number of neighbouring "Voronoi cells" (`nProbe`), which indicates an IVF-style (inverted-file, clustered) index rather than HNSW. `LIMIT k` therefore does not guarantee k results [CLAIM-arangodb-10]. Edge lookups by `_from`/`_to` use a dedicated edge index (*hypothesis* in this run; not re-verified).

**Query pipeline.** AQL is parsed on a Coordinator and optimised into an execution plan of nodes such as EnumerateCollection, IndexNode, TraversalNode and SortNode. Filters and parts of the plan are pushed to DB-Servers. The detailed optimiser rule set is NOT re-verified here.

**Reasoning.** None.

**Concurrency and transactions.** Single-server ACID transactions on RocksDB. In a cluster, writes go to the shard leader and are replicated synchronously to followers before acknowledgement [CLAIM-arangodb-12]. The cross-shard transaction isolation guarantees are NOT verified in this run and need checking before any claim is made.

**Partitioning and consistency.** Shards are placed by hashing, by default on `_key`. The Agency (Raft) holds the shard map and supervision state. Follower failure is detected after about 3 s and leader failover happens after about 15 s of missed heartbeats [CLAIM-arangodb-12]. A consequence (*hypothesis*): with default key hashing, multi-hop traversals cross shards and pay network round-trips per hop, which is why the vendor sells sharding-aware graph placement.

**Caching, versioning, security.** "External versioning" was added in 3.12 [CLAIM-arangodb-08]. There is no time-travel or branch model. Users, permissions per database and collection, and a web UI exist (not re-verified in this run).

## 6. Functional and non-functional requirements inferred

- FR: one query can combine document filters, graph traversal, keyword search and vector similarity.
- FR: automatic failover with synchronous replication.
- NFR: horizontal scale-out through hash sharding; operability through a central configuration store (Agency); vector search accepts approximate recall in exchange for speed.
- Licensing NFR imposed on adopters: dataset size and commercial-use limits in Community Edition [CLAIM-arangodb-01].

## 7. Performance and resource model

No benchmark was run. No independent, reproducible benchmark for 3.12 was found in the time budget. Qualitative model, derived from the documented design:
- Synchronous replication trades write latency for consistency [CLAIM-arangodb-12].
- IVF-style vector search trades recall for latency through `nProbe` [CLAIM-arangodb-10].
- Default key-hash sharding likely makes deep traversals network-bound (hypothesis).

Failure modes: losing Agency quorum stops the cluster; `replicationFactor: 1` risks data loss on permanent node loss [CLAIM-arangodb-12]; the vector feature flag cannot be turned off once enabled [CLAIM-arangodb-10].

## 8. Strengths — and how to match or exceed

1. **One plan across document, graph, search and vector** [CLAIM-arangodb-10][CLAIM-arangodb-11]. EOIP can match this at the application layer: QueryPlan templates (BL-08) that combine BM25/vector (BL-13, BL-14), RRF (BL-15) and graph expansion. EOIP can exceed it by applying source-ACL filtering inside the same plan (BL-18 must be built first).
2. **Clean control/data-plane split (Raft Agency + stateless Coordinators)** [CLAIM-arangodb-12]. This is a design reference for EOIP's eventual HA layer (CAP-76).
3. **Rich JSON entities next to edges.** EOIP's LPG adapters already hold properties. ArangoDB's model shows that keeping raw JSON alongside the canonical graph is useful for J12 (arbitrary JSON onboarding).

## 9. Limitations with root causes

| Type | Limitation | Root cause | Evidence |
|---|---|---|---|
| Licensing restriction | BUSL-1.1 source; Community binaries capped at 100 GiB, internal use only, no distribution/embedding | licensing — **proven** | CLAIM-arangodb-01, -02, -04 |
| Outdated claim | "ArangoDB is Apache-2.0" holds only for ≤ 3.11 (now EOL) or for releases past their 4-year change date | licensing history — proven | CLAIM-arangodb-02, -04 |
| Intentional trade-off | approximate vector results; `LIMIT` not guaranteed; feature irreversible | algorithm/storage — proven | CLAIM-arangodb-10 |
| Hypothesis | cross-shard traversal cost under default key hashing | partitioning — hypothesis | CLAIM-arangodb-12 (sharding rule) |
| Verified gap | no RDF/OWL/SHACL, no reasoning, no standard graph query language (Cypher/Gremlin/GQL) | semantics — proven by absence in docs examined | — |

Root causes by group:
- *Algorithmic:* traversal across hash shards.
- *Operational:* Agency quorum, replication latency.
- *User/developer friction:* the proprietary AQL language and the licence uncertainty that follows the change.

## 10. Deployment, licensing, redistribution, operational viability

Deployment modes: single server, cluster, Docker/Kubernetes operator, and a managed cloud. Air-gap: self-managed deployments are technically possible offline (operator and image mirroring not verified).

**Legal-review trigger: YES.**
- BUSL-1.1 forbids offering a commercial service that lets third parties access or manage databases [CLAIM-arangodb-02].
- The Community License forbids commercial use and redistribution/embedding [CLAIM-arangodb-04].

A white-label EOIP that bundled ArangoDB would need a negotiated Enterprise/OEM agreement. A customer-supplied ArangoDB licensed directly by the customer is a different scenario that also needs legal review. No legal conclusion is given here.

## 11. Competitive delta against the EOIP baseline

- EOIP composes the multi-model capabilities ArangoDB has in one engine: graph adapters (BL-01..BL-06), in-process BM25 (BL-13), hashing/HNSW vectors (BL-14), RRF (BL-15). EOIP's pieces are **not persistent or scalable** at the level ArangoDB's are, which is a competitive deficit in CAP-53/54/55.
- EOIP is ahead on governance and epistemics (BL-28, BL-37, BL-39, BL-40), egress (BL-45) and licence posture.
- ArangoDB is not among EOIP's required backends (HugeGraph, Neo4j, Neptune). Adding it is optional and blocked by licensing for OEM distribution.

## 12. Strength-adoption and inversion cards

**STR-arangodb-01** | ArangoDB | single query plan fusing keyword, vector and graph | CLAIM-arangodb-10, -11 | one-shot evidence retrieval for J1/J6 | match | `HybridGraphPlan` QueryPlan template: stage 1 BM25+vector candidates → RRF → stage 2 bounded graph expansion → ACL filter → citations | J6 benchmark: hybrid+graph plan versus BM25, dense, hybrid and reranked baselines on an EOIP test corpus; adopt only if nDCG@10 improves and p95 stays within budget (PROPOSED).

**STR-arangodb-02** | ArangoDB | Raft configuration store with stateless query nodes and automatic failover | CLAIM-arangodb-12 | HA reference for scale-out phase | match (design pattern) | for EOIP's own services: stateless API/worker replicas plus a consensus-backed config/lease store (etcd or the backend's own HA) | kill the leader in an HA compose; recovery under 30 s with no lost acknowledged mutation (PROPOSED).

**INV-arangodb-01 — licence change removes redistribution rights.**
- **Target:** ArangoDB 3.12+ Community and source.
- **Limitation:** BUSL-1.1 plus a Community License with no distribution/embedding right and a 100 GiB cap [CLAIM-arangodb-01][CLAIM-arangodb-04].
- **Root cause:** licensing (vendor monetisation strategy) — **proven**.
- **Alternative:** EOIP keeps every bundled component redistribution-safe (Apache-2.0/MIT/permissive) and treats any source-available engine as a *customer-supplied* backend reached through an adapter, never bundled. This is worse when a customer wants a single turnkey appliance with that engine inside.
- **Options:**
  1. Quick: document ArangoDB as "customer-licensed external backend only".
  2. Pragmatic: a licence-gate check in the build that fails the SBOM pipeline on BUSL/SSPL/Elastic/Commons-Clause dependencies unless an approved exception record exists (CAP-79).
  3. Long-term: an adapter certification programme where third-party engines plug in with the licence obligations recorded per tenant.
- **Selected:** option 2. Sketch: `sbom-licence-gate: deny [BUSL-1.1, SSPL-1.0, Elastic-2.0, Commons-Clause] unless exceptions/<component>.yaml{approved_by, scope, expiry}`.
- **POC:** inject a BUSL dependency into a test build; the gate must fail. Then add an exception file; it passes, and the decision is audited.
- **Defensibility:** buyers who need to redistribute or white-label get a clean licence chain; that is a sales asset competitors with source-available cores cannot easily copy.
- **Decision:** **ADOPT**.

**INV-arangodb-02 — key-hash sharding versus deep traversal.**
- **Limitation:** shards are placed by hashing `_key` by default [CLAIM-arangodb-12]. Multi-hop traversals that cross shards incur network hops — *hypothesis* (consequence not benchmarked).
- **Root cause:** partitioning — hypothesis.
- **EOIP inversion:** tenant-aligned placement. A tenant is the natural partition, and most EOIP queries are single-tenant, so one-node-per-tenant (SILO) or tenant-affine placement keeps traversals local. This is worse for one very large tenant that exceeds a node.
- **Options:**
  1. One-node first, scale vertically.
  2. Tenant-affine placement in the isolation registry (BL-20).
  3. Community-aware sub-tenant partitioning using graph clustering (BL-43 community detection).
- **Selected:** option 2.
- **POC:** 50 tenants on 3 nodes; measure the share of cross-node hops for J1 queries. Target 0% for SILO/BRIDGE tenants.
- **Decision:** **EXPERIMENT**.

Seed hypotheses (§10.5): none targets ArangoDB.

## 13. Per-capability decisions

| Capability | Decision | Note |
|---|---|---|
| CAP-03 multi-model document+graph storage | REJECT ArangoDB as bundled engine; DEFER as customer-licensed adapter | licensing |
| CAP-55 hybrid retrieval fused with traversal | BUILD | QueryPlan template, see STR-arangodb-01 |
| CAP-53 vector search (IVF via Faiss) | REJECT here | decided in C10 cohort |
| CAP-76 HA/DR control-plane pattern | BUILD (pattern) | Raft-style config store reference |
| CAP-77 / CAP-79 licence gate in supply chain | BUILD | INV-arangodb-01 |
| CAP-05 scale-out partitioning | EXPERIMENT | tenant-affine placement |

## 14. Concrete tests, POC, acceptance conditions (all PROPOSED)

1. **Licence-gate test:** SBOM pipeline rejects a BUSL component without an exception file (pass/fail).
2. **Hybrid-plan benchmark (BM-hybrid):** compare against strong non-graph baselines first (Master Prompt §5.3). Accept only on measured gain.
3. **Optional adapter spike:** an `ArangoGraphStore` adapter against a customer-licensed 3.12 instance. Accept if the BL-07 conformance suite passes, with the licence obligations recorded.

## 15. Risks, trade-offs, open questions

- Open questions:
  - Exact 3.12.12 release date.
  - Whether the three-cluster limit is in force.
  - Cross-shard transaction isolation level.
  - Whether the Arango "4.0" platform changes licensing for the core.
  - Exact current text of the Community License (page not fetched in full).
- Risk: licence terms have changed twice (3.12 and 3.12.5) and could change again. Any customer-supplied deployment needs per-version review.

## Appendix A — Research-dimension coverage

| Dimension | Covered in section(s) | Summary or N/A reason |
|---|---|---|
| D1 Identity and maturity | 1 | 3.12.12 latest; 4.0 unreleased; BUSL |
| D2 Problem and workloads | 2 | multi-model consolidation |
| D3 Architecture decomposition | 4 | Agency/Coordinators/DB-Servers |
| D4 Storage primitives and indexing | 5 | RocksDB; Faiss IVF-style vector index |
| D5 Schema and semantic expressivity | 3, 5 | schemaless JSON + edges; no ontology |
| D6 Query pipeline and optimisation | 5 | AQL on Coordinators; optimiser not re-verified |
| D7 Reasoning and inference | 5 | N/A — none |
| D8 Transactions, concurrency, scale | 5, 7 | sync replication, failover timings |
| D9 Ingestion and federation | 3 | not examined in depth (import tools exist; UNVERIFIED) |
| D10 Identity and evidence | 11 | N/A — no provenance model |
| D11 Time and evolution | 5 | external versioning only; no time travel |
| D12 Graph algorithms and ML | 3 | not examined (Pregel-style analytics history UNVERIFIED) |
| D13 Retrieval and agent integration | 2, 8 | search + vector + graph in AQL |
| D14 Natural-language querying | — | vendor AI suite not examined; UNVERIFIED |
| D15 Governance and authoring | — | N/A |
| D16 Human experience | 3 | web UI exists |
| D17 Developer experience | 3 | drivers, AQL |
| D18 Trust and security | 5 | DB/collection permissions (not re-verified) |
| D19 Multi-tenancy and white-label | 10, 12 | database-per-tenant possible; OEM blocked by licence |
| D20 Empirical economics | 7 | no numbers |
| D21 Commercial and licensing | 1, 10 | BUSL + Community License |
| D22 Interoperability and lock-in | 9 | AQL proprietary |
| D23 IP and prior art | — | no patent search; no relevant method claims |
| D24 Research quality | 15 | official docs; dates partly conflicting |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-03 | native | CLAIM-arangodb-11 | BL-01 (LPG only), Partial | REJECT (bundled) / DEFER (adapter) | P3 |
| CAP-05 | native | CLAIM-arangodb-12 | Planned | EXPERIMENT (tenant-affine) | P2 |
| CAP-53 | native (3.12.4+) | CLAIM-arangodb-10 | BL-14 Partial | REJECT here | P2 |
| CAP-54 | native | CLAIM-arangodb-08 | BL-13 Implemented (in-process) | REJECT here | P2 |
| CAP-55 | native (single AQL) | CLAIM-arangodb-10 | BL-15 Implemented | BUILD (plan template) | P1 |
| CAP-76 | native | CLAIM-arangodb-12 | BL-50 Partial | BUILD (pattern) | P2 |
| CAP-77 | source-available | CLAIM-arangodb-01, -02, -04 | BL-22 Implemented | BUILD licence gate | P1 |
| CAP-79 | n/a | — | Unknown | BUILD | P1 |

## Appendix C — Evidence records

| CLAIM-ID | product / version / date | exact claim | classification | source title + URL | publication / access date | confidence + rationale | contradictory evidence |
|---|---|---|---|---|---|---|---|
| CLAIM-arangodb-01 | ArangoDB 3.12 | "changes the licensing model for the ArangoDB source code and the Community Edition, starting with version 3.12"; Apache 2.0 replaced by BUSL-1.1; Community License "limits deployments to a 100 GiB on dataset size in production"; no commercial use, only internal business purposes | Officially documented | Incompatible changes in ArangoDB 3.12 — https://docs.arango.ai/arangodb/3.12/release-notes/version-3.12/incompatible-changes-in-3-12/ | — / 2026-10-18 | 0.85 | download page uses "100 GB" not GiB |
| CLAIM-arangodb-02 | ArangoDB source (devel) | BUSL Licensor ArangoDB Inc.; Licensed Work "ArangoDB Self Managed (Release Date: March 2024)"; Additional Use Grant: internal production use, not in a commercial offering letting third parties access/manage databases (except contractors); Change Date: 4-year anniversary; Change License: Apache 2.0 | Observed in source (licence file) | LICENSE — https://github.com/arangodb/arangodb/blob/devel/LICENSE | 2024 / 2026-10-18 | 0.85 | none |
| CLAIM-arangodb-03 | ArangoDB licensing blog | BSL 1.1 for future versions, reverting to Apache 2.0 after four years; Community License limits commercial use and imposes 100 GB per cluster; commercial use includes distributing to end users | Officially documented (vendor blog) | "Evolving ArangoDB's Licensing Model for a Sustainable Future" — https://arango.ai/?p=2755 | 2023-10-11 (edited 2023-10-12) / 2026-10-18 | 0.8 | none |
| CLAIM-arangodb-04 | ArangoDB downloads | from 3.12.5 Community Edition includes all Enterprise features, no time limit; free for non-commercial use and up to 100 GB; no rights to distribute or embed within other products; 3.10/3.11 EOL 2025-05-30 | Officially documented | Download ArangoDB — https://arango.ai/downloads/ | — / 2026-10-18 | 0.8 | none |
| CLAIM-arangodb-05 | ArangoDB release notes | 3.12 series latest patch 3.12.12; 4.0 in development, not released | Officially documented | Release notes — https://docs.arango.ai/arangodb/4.0/release-notes/ | — / 2026-10-18 | 0.75; no date given | Wikipedia lists 3.12.11 (27 Aug 2026 / 12 Aug 2026) |
| CLAIM-arangodb-06 | Arango platform | "Arango Contextual Data Platform 4.0" announced 2026-03-20 at NVIDIA GTC with an Agentic AI Suite | Third-party report | CB Insights company page — https://www.cbinsights.com/company/arangodb | 2026-03 / 2026-10-18 | 0.4 secondary | core 4.0 unreleased per CLAIM-arangodb-05 |
| CLAIM-arangodb-07 | arangodb/arangodb repo | not archived; licence NOASSERTION; last push 2026-10-17 | Officially documented | GitHub API — https://api.github.com/repos/arangodb/arangodb | — / 2026-10-18 | 0.85 | none |
| CLAIM-arangodb-08 | ArangoDB 3.12 | new: improved memory accounting, wildcard search, multi-dimensional indexes, external versioning, transparent compression | Officially documented | What's new in 3.12 — https://docs.arango.ai/arangodb/4.x/release-notes/version-3.12/whats-new-in-3-12/ | — / 2026-10-18 | 0.7 via search extract | none |
| CLAIM-arangodb-09 | Community License | max three clusters per organisation | Unverified (secondary summary) | search summary of arango.ai announcement | — / 2026-10-18 | 0.25 | not in docs or blog text fetched |
| CLAIM-arangodb-10 | ArangoDB 3.12.4+ | vector index built on Faiss, introduced 3.12.4; enabling `--vector-index` is permanent ("permanently changes how the data is managed by the RocksDB storage engine"); metrics cosine, L2, innerProduct (3.12.6); `APPROX_NEAR_COSINE`; results approximate, `nProbe` controls Voronoi cells searched; pre-filter from 3.12.6 | Officially documented | Vector indexes / AQL vector functions — https://docs.arango.ai/arangodb/3.12/indexes-and-search/indexing/working-with-indexes/vector-indexes/ ; https://docs.arango.ai/arangodb/3.12/aql/functions/vector/ | — / 2026-10-18 | 0.8 via search extract of official docs | none |
| CLAIM-arangodb-11 | ArangoDB | edges are documents in edge collections with `_from`/`_to`; named graphs | Reasoned inference (long-standing documented model, not re-fetched this run) | ArangoDB docs (graphs) — https://docs.arango.ai/arangodb/3.12/ | — / 2026-10-18 | 0.6 | none |
| CLAIM-arangodb-12 | ArangoDB 3.12 cluster | Agency = Raft KV of odd number of Agents; Coordinators stateless; DB-Servers host shards; hash sharding default on `_key`; per-shard leader/follower synchronous replication; follower out-of-sync after 3 s, leader failover after 15 s | Officially documented | Cluster deployment — https://docs.arango.ai/arangodb/3.12/deploy/cluster/ | — / 2026-10-18 | 0.85 | none |

## Appendix D — Assumptions

- A-arango-1: "ArangoDB" means the self-managed database (`arangodb/arangodb`), not the managed platform.
- A-arango-2: The licence terms read on 2026-10-18 apply to all 3.12.x releases. Terms for a future 4.0 are unknown.
- A-arango-3: Feature claims not re-fetched in this run (edge index, permissions, optimiser) are labelled hypothesis or reasoned inference and carry confidence ≤ 0.6.
