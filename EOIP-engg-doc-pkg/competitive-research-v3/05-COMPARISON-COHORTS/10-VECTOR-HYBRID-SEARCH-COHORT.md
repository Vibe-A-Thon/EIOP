# Cohort 10 - Vector and hybrid search engines, with local embeddings

| Field | Value |
|---|---|
| Cohort ID | COH-10 |
| Workload class | Persistent dense, sparse and full-text retrieval with metadata filtering, tenant partitioning and rank fusion; the substrate under GraphRAG (cohort 06) and ACL-filtered search (cohort 12) |
| Members | [qdrant](../04-COMPETITOR-DEEP-DIVES/C10-qdrant.md), [pgvector](../04-COMPETITOR-DEEP-DIVES/C10-pgvector.md), [opensearch](../04-COMPETITOR-DEEP-DIVES/C10-opensearch.md), [milvus](../04-COMPETITOR-DEEP-DIVES/C10-milvus.md), [weaviate](../04-COMPETITOR-DEEP-DIVES/C10-weaviate.md), [lancedb](../04-COMPETITOR-DEEP-DIVES/C10-lancedb.md), [elasticsearch](../04-COMPETITOR-DEEP-DIVES/C10-elasticsearch.md), [vespa](../04-COMPETITOR-DEEP-DIVES/C10-vespa.md) |
| Tier C | [C10-tier-c-records-V23](../04-COMPETITOR-DEEP-DIVES/C10-tier-c-records-V23.md): Chroma, Tantivy/Lucene, native vector indexes inside graph engines (Neo4j, Memgraph, FalkorDB, Neptune Analytics, HugeGraph) |
| Embedding models | [C09-local-embeddings](../04-COMPETITOR-DEEP-DIVES/C09-local-embeddings.md) (bge-m3, bge-reranker-v2-m3, multilingual-e5, gte-modernbert, nomic-embed-v2, Jina family, ColBERT variants, sentence-transformers, TEI) |
| Reference columns | HugeGraph, Neo4j, Neptune, EOIP @HEAD 896e06d (BL-IDs from `01-SYSTEM-BASELINE.md`, status from `01a-BASELINE-DELTA-HEAD.md`) |
| Date | 2026-10-26 |

## 1. Workload class and comparison basis

**Customer workloads.** Keyword, semantic and hybrid search over tenant-owned documents and graph-entity text; retrieval for RAG that must respect source permissions; embeddings that survive model change; deployment on one CPU node in an air-gapped site.

**Why comparable.** All members store vectors (and, except pgvector and LanceDB without extra indexes, text) behind a query API with payload filters. The decisive differences for EOIP are not raw speed but (a) what happens to recall when a restrictive filter such as an ACL or tenant predicate is applied, (b) how tenants are isolated, (c) whether deletes are real, and (d) licence and footprint on one node.

**Excluded.** Chroma is prototype-grade and its tenancy and auth were not verified (CLAIM-chroma-01/02); Lucene and Tantivy are libraries (Tier C). Native vector indexes in graph engines are compared as a column group, not as search engines. Managed-only offerings (Neptune Analytics vectors, Zilliz Cloud) appear only as references.

**Evidence quality.** No dive ran a benchmark. Every performance statement in the cohort is either a vendor figure or a design statement from documentation. Claim IDs below are written as in the dives (for example `qdrant-05` means CLAIM-qdrant-05).

## 2. Capability comparison

Values: native / partial / enterprise-only / absent / unknown, with claim IDs.

### 2.1 Search engines

| CAP | Qdrant | pgvector | OpenSearch | Milvus | Weaviate | LanceDB | Elasticsearch | Vespa | EOIP @HEAD |
|---|---|---|---|---|---|---|---|---|---|
| CAP-53 dense vector | native HNSW, quantisation, memory tiers (qdrant-07) | native HNSW, IVFFlat; index dimension caps (pgvector-03) | native k-NN; JVector disk engine (opensearch-05, -06) | native (milvus-04) | native HNSW, flat, dynamic (weaviate-06) | native, embedded (lancedb-01, -04) | native kNN exact and approximate (elasticsearch-05) | native HNSW (vespa-04) | **Partial**: pure-Python HNSW `graph/vector_graph.py:78`; hashing embedder default; no external vector DB (BL-14) |
| CAP-54 full text | partial: BM25 index in 1.20.0 (qdrant-04, -06) | partial: PostgreSQL FTS (pgvector-03) | native (opensearch-05) | native BM25 function, sparse index (milvus-04) | native BM25 (weaviate-04) | native, needs FTS index (lancedb-05) | native | native (vespa-03) | Implemented BM25 in-process, not persistent (BL-13); tenant postings in `retrieval/tenant_index.py` |
| CAP-55 hybrid fusion | native: RRF, DBSF, formula, weighted RRF (qdrant-04) | partial: RRF as SQL pattern in README, no built-in (pgvector-03) | native: min_max normalisation, RRF ranker (opensearch-07) | native: RRF, weighted (milvus-04) | native: relativeScoreFusion default, rankedFusion, alpha 0.75 (weaviate-04) | native: RRF reranker, needs FTS (lancedb-05) | native retrievers rrf, linear; rrf reportedly licence-gated (third party, elasticsearch-06) | native phased ranking, reciprocal_rank (vespa-03) | Implemented twice: weighted 0.45/0.35/0.20 on API path; RRF library-only (BL-15, 01a) |
| Filtered ANN recall | filterable HNSW; ACORN per request, off by default; vendor: recall 39.7% to 100% at 4% selectivity, 5.4x to 6.7x slower (qdrant-05) | **post-filter**: restrictive filters starve results; iterative scan 0.8.0, `max_scan_tuples` 20,000; partial indexes or partitioning as workaround (pgvector-03) | engine-dependent; ACORN 3.1+; post-filter under-returns (opensearch-05) | partition key; isolation needs HNSW and single key (milvus-03) | ACORN default since 1.34, PathSeer 1.40, flat cutoff about 15% (weaviate-03) | pre-filter default in newer docs, post-filter in older: docs conflict (lancedb-04) | filter semantics not retrieved (elasticsearch-05) | pre-filter default, real-time (vespa-04); hit starvation noted in dive | **Unmeasured**; candidates filtered by tenant ownership only (BL-14, BL-18) |
| CAP-46 source-ACL | partial: API key, JWT RBAC per collection, `value_exists` ties token to stored data; ACL is a filter convention (qdrant-08) | partial: row-level security default-deny; bypass for owners, superusers (pgvector-04) | native document-level security; read-only semantics, OR across roles; no statement on DLS with kNN (opensearch-04) | absent: RBAC to collection level, no row level mentioned (milvus-05) | absent per object: RBAC by collection and tenant (weaviate-07) | absent (lancedb-03) | enterprise-only DLS, tier officially unstated (elasticsearch-04, -08) | absent: Cloud docs state client authorisation only (vespa-07) | **Partial**: `authz/pdp.py` evaluator applied only in graph branch when `scope` passed; keyword/vector/hybrid filter by tenant only (BL-18) |
| CAP-47 tenancy | payload partition `is_tenant`, custom shards, tiered shards; Cloud cap 1,000 collections; IDF statistics shared across tenants unless `idf` filter (qdrant-03) | partition plus RLS (pgvector-03, -04) | DLS roles with attribute substitution (opensearch-04); index-per-tenant is an option, not documented as a pattern | partition key, 16 default (milvus-03) | tenant = shard; about 170k tenants on 9 nodes; states ACTIVE/INACTIVE/OFFLOADED (weaviate-05) | no tenant model; isolation is path-based, i.e. one dataset directory per tenant (INV-lancedb-01) | unknown | streaming mode groups, 45 B/doc, no HNSW (vespa-05) | **Partial improved**: `TenantLayers` gives each tenant its own embedded vector and search index (BL-20, NB-11) |
| Incremental delete | unknown | vacuum slow for HNSW (pgvector-03) | deferred physical delete (dive) | unknown | tombstones; async indexing queue since 1.28 (weaviate-06) | deletions marked, compaction needs disk (lancedb-06) | deferred physical delete (dive) | real-time updates (vespa-04) | Tombstones in graph (BL-25); DSAR erases index docs and vectors (BL-46) |
| CAP-04 one-node footprint | Rust binary; RAM drives latency (qdrant-07) | one PostgreSQL container; compose has none today (pgvector-09) | **heaviest**: JVM heap half of RAM, `max_map_count` tuning (opensearch-08) | needs WAL, object store, metadata store; Lite is limited (milvus-06, -03) | single binary; HNSW 2 to 12 GB per 1M vectors (vendor, weaviate-06) | embedded wheel, no server (lancedb-03) | JVM node (dive) | multi-service; docs example t2.large (vespa-06) | In-process; no extra service |
| Licence | Apache-2.0 (qdrant-01) | PostgreSQL License (pgvector-01) | Apache-2.0 (opensearch-01) | Apache-2.0 (milvus-01) | BSD-3 except `wl` directory (weaviate-01) | Apache-2.0; Enterprise sales-led (lancedb-01, -03) | AGPLv3 / SSPL / ELv2 choice (elasticsearch-02, -03) | Apache-2.0 (vespa-01) | n/a |

### 2.2 Reference columns: vector in graph engines

| CAP | Neo4j | HugeGraph | Neptune | Others (Tier C) | EOIP @HEAD |
|---|---|---|---|---|---|
| CAP-53 | Lucene HNSW, up to 4,096 dims, filter properties from 2026.01; changes not visible inside the transaction (neo4j-09) | **absent** in server (hugegraph-09); HugeGraph-LLM uses Faiss, Milvus or Qdrant (hugegraph-28) | Neptune Analytics only: one HNSW index per graph, updates neither atomic nor isolated, cannot be loaded from Neptune Database (neptune-19) | Memgraph USearch, ACL-failing results silently dropped, planner ignores vector indexes; FalkorDB HNSW with weak filter combination (native-graph-vector-01) | Partial (BL-14) |
| CAP-54 | Lucene full text (neo4j-10, 2026.09 `SEARCH`) | unknown | via OpenSearch integration (neptune-16) | Memgraph Tantivy text index | Implemented, in-process (BL-13) |
| CAP-46 | RBAC and property privileges are EE (neo4j-14); defence in depth only | auth optional (hugegraph-14, -32) | IAM actions (neptune-09) | n/a | Partial |
| Backend neutrality | Neo4j-specific; availability depends on edition | gap is "available upstream: external store" | managed only | per engine | Adapter-level capability flags proposed (tier C decision) |

### 2.3 Embedding models and serving (C09-local-embeddings)

| Model | Licence | Key facts | Bundle-eligible |
|---|---|---|---|
| bge-m3 | MIT (emb-01) | 1,024-dim, 8,192 context, dense plus sparse plus multi-vector | Yes |
| bge-reranker-v2-m3 | Apache-2.0 (emb-02) | 0.6B reranker | Yes |
| multilingual-e5-large-instruct | MIT (emb-03) | 1,024-dim; prefix conventions | Yes |
| gte-modernbert-base | Apache-2.0 (emb-04) | about 149M, 768-dim, 8,192 context | Yes |
| nomic-embed-text-v2-moe | Apache-2.0 (emb-05) | 475M total, 305M active, 512 context | Yes |
| jina-embeddings-v2-base-en | Apache-2.0 (emb-06) | about 137M, 8,192 context | Yes |
| jina v3, v5-text, colbert-v2 | CC-BY-NC-4.0 (emb-07, -09) | non-commercial | **No** |
| jina v4 | Qwen Research License (emb-08) | card says its earlier cc-by-nc label was an error | Legal review |
| ColBERTv2 | MIT (emb-10) | multi-vector, storage blow-up | Yes |
| TEI | per README (emb-12) | serves Qwen3-Embedding, Gemma3, Nomic, GTE, E5, BGE rerankers | Server (see cohort 14) |

EOIP @HEAD: `HashingEmbedder` default; optional Ollama and sentence-transformers providers (BL-14); versioned embedding service with re-embed jobs (NB-10, `models/embedding_service.py`); `RealSemanticProvider` in `retrieval/hybrid_vector_service.py:129` is a SHA-256 simulation, not a model (01a). `sentence-transformers` is not installed.

## 3. Operational and licensing comparison

| Engine | Deployment | Air-gap | OEM / redistribution trigger | Maintenance |
|---|---|---|---|---|
| Qdrant | Binary, Docker, Helm; Raft for topology | Yes; telemetry setting to confirm and disable (dive, unverified) | Apache-2.0; confirm no enterprise-only feature is needed for ACL | Monthly minors, 1.20.0 on 2026-10-22; default changes between minors (qdrant-02) |
| pgvector | Extension on PostgreSQL 13 to 18 | Yes | Permissive; no copyleft | v0.8.7, tag 2026-10-01 (pgvector-02) |
| OpenSearch | Docker, K8s operator, tarball | Yes, but no offline install guide (opensearch-08) | Apache-2.0; trademark for white-label to review | 3.9.0 on 2026-09-29; foundation-governed (opensearch-02, -03) |
| Milvus | Lite, Standalone, Distributed (milvus-06) | Viable but heavy | Apache-2.0 | 3.0.3 on 2026-10-14; Storage V3 has no rollback (milvus-02) |
| Weaviate | Single binary, container | Yes; vectoriser modules must be disabled under egress policy (dive) | BSD-3; `wl` features are a community/enterprise split | 1.40.2 on 2026-10-22 (weaviate-02) |
| LanceDB | Embedded | Trivial | Apache-2.0; verify Lance format dependencies | Betas of 0.41 in late October; PyPI 0.40.0 (lancedb-02) |
| Elasticsearch | Self-managed | Yes | **AGPL, SSPL and ELv2 are all legal-review triggers**; x-pack ELv2-only (elasticsearch-02) | 9.5.5 (elasticsearch-01) |
| Vespa | Docker, K8s | Yes (no phone-home found, not exhaustive) | Apache-2.0 | v8.763.13 on 2026-10-05 (vespa-02) |

## 4. Performance evidence

| Figure | Source | Class | Comparable? |
|---|---|---|---|
| Qdrant ACORN: recall 39.7% to 100% at 4% selectivity, 5.4x and 6.7x slower, v1.18.2 | qdrant-05 | Vendor benchmark | Only within Qdrant |
| Weaviate HNSW memory about 2 to 12 GB per 1M vectors plus about 200 MB edges; about 170k tenants on 9 nodes | weaviate-05, -06 | Vendor documentation | No |
| OpenSearch filtered k-NN recall tables at 1M and 10M documents | opensearch dive, values not captured | Vendor | Not quoted |
| FalkorDB about 3 GB per 1M x 768 vectors | native-graph-vector-01 | Vendor | No |
| Vespa 45 bytes per document in streaming mode | vespa-05 | Documentation | Different mode (no HNSW) |

No independent benchmark, no p95 latency on one CPU node, no filtered-ANN recall under ACL-shaped predicates, and no measurement of EOIP's own pure-Python HNSW exists in the package (U-06). Embedding-model quality claims (MTEB) were not collected (C09-local-embeddings section 7). No winner can be named.

## 5. Findings

1. **Restrictive-filter recall is the main technical risk for ACL-filtered search, and engines handle it differently.** pgvector post-filters and can return too few rows (pgvector-03); OpenSearch post-filter under-returns (opensearch-05); Qdrant and Weaviate offer in-graph strategies (ACORN) with measured latency cost (qdrant-05, weaviate-03). Falsifier: a recall measurement at 1%, 4% and 40% selectivity showing parity.
2. **Only OpenSearch (native DLS) and pgvector (row-level security) provide a row-level permission primitive; Elasticsearch's equivalent is paid and tier-ambiguous.** Qdrant, Weaviate and Milvus stop at collection or tenant level; LanceDB and Vespa document nothing (opensearch-04, pgvector-04, elasticsearch-04, qdrant-08, weaviate-07, milvus-05). Source ACL therefore stays EOIP's job in every case; the engine can at most enforce tenant partitions as defence in depth.
3. **No engine documents how DLS or RLS interacts with approximate nearest-neighbour search.** The OpenSearch dive found no statement on DLS with kNN (opensearch-04 contradiction column). That behaviour must be tested, not assumed.
4. **Tenant isolation models split into three kinds: shard per tenant (Weaviate), payload partition (Qdrant, Milvus), and separate collections or directories (Qdrant's discouraged collection-per-tenant option, LanceDB's path-based isolation, INV-lancedb-01).** Qdrant shares IDF statistics across tenants by default, which is a statistical side channel unless the `idf` filter is set (qdrant-03). EOIP's current `TenantLayers` uses the third kind with embedded stores (BL-20, NB-11).
5. **One-node footprint ranks LanceDB, pgvector and Qdrant as light; OpenSearch, Elasticsearch, Milvus and Vespa as heavy.** Evidence: embedded wheel (lancedb-03), one PostgreSQL container (pgvector-03), JVM heap and `max_map_count` (opensearch-08), three mandatory services (milvus-06), multi-service config servers (vespa-06). The OpenSearch dive notes this is inference.
6. **Elasticsearch is not redistributable in the white-label product without legal review.** Its licence is a three-way AGPL/SSPL/ELv2 choice and x-pack is ELv2-only (elasticsearch-02). OpenSearch is the Apache-2.0 alternative.
7. **EOIP has no persistent vector or hybrid index in a deployed path.** The default API path uses `TenantRetrievalIndex` with a hashing embedder; `hybrid_vector_service.py` (shadow index, cutover, dimension-mismatch errors, RRF) is library-only and its "semantic" provider hashes text (BL-14, 01a). Semantic search quality is therefore currently lexical-class.
8. **Two fusion implementations exist in EOIP and disagree** (weighted on the API path, RRF in the library), so retrieval results differ by entry point (BL-15 at HEAD).
9. **Graph-engine vector indexes are convenient but should not carry ACL semantics.** Neo4j changes are not visible within the transaction (neo4j-09), Memgraph drops ACL-failing results silently and its planner ignores the index, Neptune Analytics updates are not atomic (neptune-19), and HugeGraph has none (hugegraph-09).
10. **Embedding licences are a deployment constraint.** Four of the Jina family models are non-commercial or under a research licence (emb-07..09); bge-m3, gte-modernbert, nomic v2 and e5 are MIT or Apache-2.0 and bundle-eligible, subject to ADR-H15 (weights ship only where the licence permits).

## 6. Implications for EOIP

ADR-005 states there is no mandatory vector database in P1; this cohort supports keeping the vector port backend-neutral and treating external engines as optional.

| CAP | Parity needed (STR-IDs) | Exploitable weakness (INV-IDs) | Decision | Candidate gap statement |
|---|---|---|---|---|
| CAP-46 over search | STR-opensearch-01 (DLS with attribute substitution), STR-pgvector-01 (RLS), STR-elasticsearch-01 (templated role queries), STR-vespa-01 (cheap candidate stage, costly rerank on ACL-safe survivors) | INV-qdrant-01 (ACL as caller-supplied filter), INV-opensearch-01 (DLS read-only), INV-opensearch-02 (DLS x ANN recall unknown), INV-vespa-01, INV-elasticsearch-02 (DLS leaks through aggregations) | **BUILD, P0** | Apply `authz/pdp.py` `can_read` as a pre-filter in keyword, vector and hybrid stages on every deployed path; test filtered recall and leakage (J5). |
| CAP-53 persistent vector | STR-qdrant-01 (planner plus ACORN), STR-lancedb-01 (embedded persistent ANN+FTS), STR-lancedb-02 (versioned tables, pin to policy epoch) | INV-qdrant-02, INV-pgvector-02, INV-milvus-01 (extra services vs ADR-005); INV-emb-02 (hashing embedder has no semantics) | **EXPERIMENT, P1**: run LanceDB (embedded), Qdrant and pgvector behind one port against BL-14 on a tenant corpus | EOIP has no persistent semantic index; choose by measured filtered recall, RAM and ops cost. |
| CAP-55 fusion | STR-qdrant-03, STR-opensearch-03, STR-milvus-02, STR-elasticsearch-02 (server-side fusion; use EOIP RRF as oracle) | Two EOIP implementations disagree (01a BL-15) | **BUILD, P1** | One fusion path, configurable, with a regression test against a fixed corpus. |
| CAP-54 persistent BM25 | Tantivy behind index port (tier C) | In-process, non-persistent BM25 | **EXPERIMENT, P2** | Native-extension policy needed first. |
| CAP-47 tenancy | STR-weaviate-01 (shard per tenant with lifecycle), STR-qdrant-02 (`is_tenant` plus `idf`), STR-milvus-01, STR-vespa-02 | Shared IDF statistics (qdrant-03); INV-weaviate-01 (tenant not a restore unit); INV-lancedb-01 (path-based isolation) | **INTEGRATE** patterns; keep `TenantLayers` as the isolation boundary | Embedding, index and cache isolation per tenant is already runtime-enforced for embedded layers; external engines must be wrapped, not trusted. |
| CAP-04 footprint | STR-lancedb-01, STR-pgvector-02 | INV-opensearch-03, INV-milvus-01, INV-vespa-02, INV-elasticsearch-01 (licence) | **REJECT** Elasticsearch bundling; **DEFER** OpenSearch, Milvus, Vespa | Offer OpenSearch as a customer-operated adapter only. |
| CAP-61 embeddings | STR-emb-01 (bge-m3 as one MIT model for dense, sparse and multi-vector) | INV-emb-01 (mixed Jina licences), INV-emb-02 | **BUILD**: licence allow-list in the model catalog, **INTEGRATE** TEI/sentence-transformers | Replace the SHA-256 `RealSemanticProvider` with a real model on CPU; measure recall on a local corpus. |
| CAP-78 evaluation | STR-weaviate-02 (planner picks exact scan or graph by ACL selectivity) | No independent data exists; INV-pgvector-01 (post-filter starves under restrictive ACLs) | **BUILD, P1** | Cohort-level benchmark on EOIP corpora; mark as PROPOSED until run. |
| Graph-native vectors | Per-adapter capability flags `in_tx_visibility`, `filter_props` (tier C decision) | Engine-specific ACL semantics (native-graph-vector-01) | **INTEGRATE** as optional, never as ACL boundary | "Available upstream / not integrated" for Neo4j and Neptune Analytics. |

## 7. Open questions

1. What is filtered recall of each light engine (LanceDB, Qdrant, pgvector) at 1%, 4% and 40% selectivity with realistic ACL predicates?
2. Does OpenSearch DLS apply before or after ANN candidate generation, and does it change recall?
3. Which Elasticsearch features, if any, require a paid tier (DLS, rrf)? Official sources are silent (elasticsearch-04, -06, -08).
4. Which Weaviate features live in the `wl` directory (weaviate-01)?
5. Qdrant telemetry default and the enterprise-only gating of security features need confirmation (qdrant dive section 10).
6. Can a CPU-only node embed and re-embed a representative tenant corpus within an acceptable window with bge-m3 versus gte-modernbert? No benchmark exists (C09-local-embeddings section 7).
7. Is a PostgreSQL service acceptable in the one-node reference deployment (compose has none, pgvector-09)?
