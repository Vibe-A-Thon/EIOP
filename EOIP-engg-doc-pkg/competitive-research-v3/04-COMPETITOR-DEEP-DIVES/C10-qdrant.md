| Field | Value |
|---|---|
| Registry ID | T-C10-qdrant |
| Tier | A (leading dedicated vector engine; candidate for the "multiple vector stores" requirement, BL-14/ADR-005) |
| Versions examined | Qdrant v1.20.0 (2026-10-22), v1.19.x (2026-08-05..10-05), docs as of 2026-10-26 |
| Verified on | 2026-10-26 |
| Worker | V06 |

Note: file `C10-qdrant-vector-engines.md` is a separate committed placeholder and was not touched.

## 1. Identity, current status, tier, sources

Qdrant (github.com/qdrant/qdrant; Qdrant Solutions GmbH; Rust) is an open-source vector database / search engine with REST+gRPC APIs, HNSW indexing, payload (metadata) filtering, sparse and multi-vectors, hybrid Query API, quantization, distributed mode (Raft for topology), and a managed Qdrant Cloud. Licence of the core repository: **Apache-2.0** [CLAIM-qdrant-01]. Cadence: roughly monthly minors (1.18.3 on 2026-07-17, 1.19.0 08-05, 1.19.1 09-04, 1.19.2 10-05, 1.20.0 10-22) [CLAIM-qdrant-02]. Status: active, production. Community-vs-enterprise: managed Cloud and Hybrid/Private Cloud offerings exist; whether any core feature is enterprise-only is NOT PUBLICLY VERIFIED in this pass (the security pages examined describe API key and JWT RBAC as in the open server config).

## 2. Problem, workloads, workflows

Problem: low-latency approximate nearest-neighbour search with rich filtering at scale. EOIP workloads: chunk/entity embeddings for GraphRAG candidates (BL-16), semantic dedupe of candidates (BL-35), multi-tenant semantic search where **each hit must be filtered by source ACL** (BL-18).
Workflow: ingest -> chunk -> embed (Ollama) -> upsert point `{id, vector(s), payload{tenant, source_id, acl_principals[], acl_hash, revision, tombstone}}` -> query: `prefetch` dense + sparse (BM25) with filter `tenant==T AND acl_principals any-of caller_groups` -> fuse (RRF) -> top-k IDs -> EOIP graph re-check of ACL/tombstone -> evidence.

## 3. Feature inventory

| Feature | Status | Note |
|---|---|---|
| Dense, sparse, multi-vector points | present | multivector not supported with inline storage [CLAIM-qdrant-07] |
| Query API: prefetch (1.10), RRF, DBSF (1.11), formula rescoring (1.14), RRF k (1.16), weighted RRF (1.17) | present | BM25 text queries need full-text index; BM25 scoring in index 1.20.0+ [CLAIM-qdrant-04,06] |
| Payload indexes: keyword, integer, float, bool, geo, datetime, text, uuid; `nested` (1.20) | present | create before ingest or rebuild HNSW [CLAIM-qdrant-06] |
| Filterable HNSW (extra edges), per-request ACORN (`acorn.enable`, applied below `max_selectivity` 0.4) | present | ACORN off by default [CLAIM-qdrant-05] |
| Multitenancy: payload partition with `is_tenant` (1.11), custom shards (1.7), tiered shards (1.16) | present | [CLAIM-qdrant-03] |
| Auth: static API key, read-only key (1.7), JWT RBAC (HS256), TLS | present | claims `exp`, `access` (global r/m or per-collection r/rw), `value_exists`; changing the key invalidates tokens [CLAIM-qdrant-08] |
| Row/document-level ACL natively | **partial** | achieved by payload filter, not by a security layer: a caller who can query can supply any filter unless the JWT is scoped; no payload-filter claim seen in the docs page summarised (UNVERIFIED) |
| Quantization (scalar, binary, product, TurboQuant `bits1`, `turbo4/8`), `memory` tiers pinned/cached/cold (1.19+), inline storage (1.16+) | present | [CLAIM-qdrant-07] |
| Snapshots (collection, full, shard), S3 | **UNVERIFIED** | the page text could not be fetched; confidence in existence from prior knowledge only |
| Incremental upsert/delete, WAL | present (general knowledge) | specific delete/compaction behaviour UNVERIFIED here |
| Web UI dashboard, Python/JS/Go/Rust/Java/.NET clients | present (not examined) | |

## 4. Architecture

```
 client --REST/gRPC (api-key | JWT)--> Qdrant node
   collection -> shards (auto / custom shard keys) -> segments (immutable HNSW + mutable appendable)
   per segment: vectors (RAM | mmap | cold on disk, optional quantized copy) + payload store + payload indexes
   WAL + segment optimizer (build index, vacuum deletes)   |  cluster: Raft metadata, peers gRPC :6335
```

## 5. Under-the-hood reconstruction

- **Data model**: point = id + named vectors (dense/sparse/multivector) + JSON payload. Collections fix vector size/distance; names/vectors above 65,536 dims rejected from 1.19.1 [CLAIM-qdrant-02].
- **Indexing/filtering**: HNSW per segment; payload indexes (keyword, range, geo, full-text, nested) used (a) to estimate filter cardinality, (b) to choose a plan - payload-index scan for selective filters vs graph traversal with in-line filtering for permissive ones [CLAIM-qdrant-06]; "filterable HNSW" adds per-payload-value edges at build time (design proposal from the 2019 article: extra edges per category, at most ~2x edges; the article states it does not fully describe current behaviour) [CLAIM-qdrant-05]. ACORN-1 expands through neighbours-of-neighbours when a neighbour fails the filter; measured by Qdrant on v1.18.2: recall 39.7% -> 100% on a 4% intersection but 5.4x-6.7x slower when the planner stays on the graph; at 1% filter and ef=512 filterable HNSW reached 91.2% at 4.9 ms vs ACORN 90.3% at 20.1 ms (vendor figures, vendor datasets) [CLAIM-qdrant-05]. Pseudocode for plan choice (hypothesis consistent with docs): `c = estimate(filter); if c < full_scan_threshold: exact over payload-index hits else: hnsw_search(filter, ef)`.
- **Hybrid**: server-side `prefetch` branches (dense/sparse/BM25) fused by RRF/DBSF/formula; tenant-scoped IDF via `idf` corpus filter (1.19.0+) because BM25/IDF statistics are shared across tenants by default - **a cross-tenant statistical side-channel to consider** [CLAIM-qdrant-03].
- **Tenant isolation models**: (1) one collection per tenant - discouraged, Qdrant Cloud caps 1000 collections by default; (2) payload partition with `is_tenant` index co-locating tenant data; (3) `payload_m`/`m=0` per-tenant graphs; (4) custom shards per tenant (~<=1000 per cluster); (5) tiered (small tenants on shared `default` shard, large promoted around 20,000 points) [CLAIM-qdrant-03]. Queries without a tenant filter scan all tenants.
- **Storage/memory**: mmap/cold tiers, 4-bit and 1-bit quantized copies with optional rescoring against original vectors; inline storage keeps vectors in the HNSW file (index 3-6x float32 size), in 1.20.0 the HNSW file holds the only copy of originals [CLAIM-qdrant-07].
- **Concurrency/consistency**: WAL, per-shard replication, Raft only for cluster metadata (general knowledge; UNVERIFIED here). Segment count tunes latency (= cores) vs throughput (few big segments) [CLAIM-qdrant-07].
- **Security**: key checked per request; internal gRPC now enforces auth by default when a key is set (1.20.0) [CLAIM-qdrant-02,08].

## 6. Inferred requirements for EOIP

FR: a `VectorIndex` protocol (upsert/delete/query with mandatory `tenant` and `principal_filter` arguments that cannot be omitted); payload carries `acl_hash`, `revision`, `tombstone`; deterministic re-embed on model-digest change. NFR: single-node CPU container, mmap/quantized to bound RAM; vector store is a **derived index** rebuildable from graph + raw capture (ADR-004), never authoritative; delete propagation within an SLA; ACL change propagation within an SLA; backup optional because rebuildable.

## 7. Performance and resource model

No independent benchmark used. Vendor figures above are workload-specific (their filters, v1.18.2, hardware not captured in the summary). Resource rules from docs: RAM drives latency; quantization trades recall for memory without published recall numbers on the optimisation page; disk-resident modes depend on IOPS (measure with fio) [CLAIM-qdrant-07]. Qdrant is CPU-capable (no GPU requirement stated in the pages examined), consistent with ADR-H15..H17; GPU indexing is an optional feature NOT examined. Failure modes: unindexed filter fields run slowly (strict mode can reject); recall collapse when filter is restrictive and edges missing (ACORN mitigation); tenant-less queries scan everything; BM25 stats shared across tenants.

## 8. Strengths and how to match/exceed

| Strength | Match/exceed |
|---|---|
| Filter-aware ANN (payload index + filterable HNSW + ACORN) | EOIP's pure-Python HNSW (`graph/vector_graph.py:78`) cannot match; INTEGRATE rather than rebuild |
| Rich hybrid fusion server-side | keep EOIP RRF (`search/hybrid_engine.py:150`) as the portable fallback; use Qdrant fusion when present |
| Mature multitenancy toolkit | exceed by tying `tenant` + ACL to EOIP identity and a mandatory filter wrapper |
| Apache-2.0 Rust single binary | easy redistribution |

## 9. Limitations with root causes

| Class | Item |
|---|---|
| Algorithmic | Filter + HNSW recall cliff at low selectivity; ACORN costs latency (vendor-measured) |
| Operational | Extra service to run, back up and version; collection/shard count limits for tenancy; new defaults change behaviour between minors (internal auth enforcement 1.20.0, update queue 1M->200 in 1.19.0) [CLAIM-qdrant-02] |
| Security design | ACL is a filter convention: a bug or missing filter leaks; JWT `value_exists` ties revocation to stored data, not to a policy engine |
| Licensing | core Apache-2.0; Cloud features/enterprise gating not verified |
| User friction | many tuning knobs (`m`, `ef_construct`, `payload_m`, memory tiers); docs for older concepts (2019 article) lag current behaviour |

## 10. Deployment, licensing, redistribution

Self-hosted binary/docker/Helm (general knowledge), managed cloud optional. Air-gap: yes (no mandatory phone-home verified; telemetry setting exists in general knowledge, UNVERIFIED - confirm and disable). Apache-2.0 permits OEM redistribution; patent grant included; trademark use for white-label needs review. Legal-review trigger: low (Apache-2.0), but confirm no enterprise-only security features required for ACL (JWT RBAC appears in OSS docs).

## 11. Competitive delta against EOIP baseline

| Capability | EOIP | Qdrant |
|---|---|---|
| Dense search | BL-14 Partial: hashing embedder + pure-Python HNSW, no persistence, no external DB (ADR-005) | persistent filtered ANN, quantization, mmap |
| Hybrid | BL-15 Implemented RRF over in-process BM25 (BL-13) | server-side RRF/DBSF/BM25 |
| ACL | BL-18 Absent; BL-17 captures `acl_hash` | filterable payload; enforcement still EOIP's job |
| Tenancy | BL-20 Partial, adapters tenant-blind | explicit patterns (payload / shard / tiered) |
| Deletes | BL-25 tombstones in graph | delete-by-filter needed to propagate; no existing code |
| Backup | BL-50 scripts | derived index; rebuild path preferable |

## 12. Cards

STR-qdrant-01 | Qdrant | filtered ANN with planner + ACORN | [qdrant-05,06] | ACL-filtered semantic search without recall collapse | integrate | `VectorIndex` adapter; per-request ACORN for compound filters | recall@10 >= 0.95 vs exact on ACL filters at 1%/10%/50% selectivity.
STR-qdrant-02 | Qdrant | tenant toolkit (`is_tenant`, tiered shards) | [qdrant-03] | many small tenants on one node | integrate | payload-partition default; promote large tenants | 1,000 synthetic tenants, tenant-filter p95 within 2x of single-tenant.
STR-qdrant-03 | Qdrant | server-side hybrid | [qdrant-04] | fewer round trips | match | use only behind adapter | RRF result parity with EOIP RRF on same candidates within agreed tolerance.

**INV-qdrant-01 (ACL-as-filter leak risk).** Target Qdrant 1.20; workload ACL-filtered search. Limitation: authorisation depends on caller-supplied filter [qdrant-08]. Root cause: *proven* design (filter semantics) / enforcement location. Options: (1) quick - EOIP gateway builds the filter, vector DB reachable only from the gateway on backend network; (2) native - per-tenant JWT scoped to collection + EOIP post-check against graph/ACL (defence in depth, drop hits failing recheck); (3) long-term - ACL epoch tokens: payload stores `acl_epoch`, gateway rejects hits whose epoch is stale. Selected 1+2. Benchmark: leakage suite J5 with 100 principals, 10 ACL changes/s, success = 0 leaked hits after propagation SLA (target to be set), baseline = no recheck. Dependencies: BL-17 `acl_hash`; failure case: stale ACL window; deleted user remains. Defensibility: ACL propagation/recheck tied to EOIP identity+graph. Decision: ADOPT. Alternative worse when ACL volume is so high that recheck costs dominate.
**INV-qdrant-02 (extra service vs ADR-005).** Root cause: deployment. Options: quick - keep in-process index for P1; native - optional `VectorIndex` backends (in-process, pgvector, Qdrant, OpenSearch); long-term - derived-index framework with rebuild from graph. Decision: EXPERIMENT (ADR-005 revisit trigger met if hashing-embedder recall gap is shown in P3 evaluation).
No seed hypothesis in 10.5 targets Qdrant.

## 13. Per-capability decisions

| Capability | Decision |
|---|---|
| CAP-53 vector search | INTEGRATE Qdrant as the optional dedicated backend behind `VectorIndex`; keep in-process fallback |
| CAP-55 hybrid fusion | REUSE EOIP RRF; EXPERIMENT server-side fusion |
| CAP-46 ACL in retrieval | BUILD (wrapper + recheck); do not rely on Qdrant alone |
| CAP-47 tenancy | INTEGRATE payload-partition pattern |
| CAP-74 backup | DEFER (derived index; rebuild-first; verify snapshots) |
| GPU indexing | REJECT under ADR-H15..H17 until H-17 resolved |

## 14. Tests and acceptance

1. Recall: 1M-chunk synthetic corpus, 768-d, ACL labels with Zipf group sizes; recall@10 vs `exact:true` at selectivities 0.1%, 1%, 10%, 50%, with/without ACORN. 2. J5 leakage test through the gateway. 3. Delete propagation: tombstone in graph -> point gone within SLA, tested under ingest load. 4. Single-node CPU footprint: RAM and p95 latency with float32, scalar, binary quantization; record hardware. 5. 1,000-tenant isolation test. 6. Restart/rebuild from raw capture equals prior results. 7. Licence/SBOM check; telemetry disabled.

## 15. Risks and open questions

Snapshot/restore semantics unverified; whether any JWT payload-filter claim exists; enterprise gating; telemetry defaults; version churn; cross-tenant BM25/IDF statistics leakage; interaction with embeddings drift (Ollama CLAIM-ollama hypothesis).

## Appendix A. Dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Apache-2.0, cadence |
| D2 | 2 | ACL-filtered retrieval |
| D3 | 4 | shards/segments |
| D4 | 5 | HNSW, payload indexes, quantization |
| D5 | 5 | payload typing |
| D6 | 5 | planner, hybrid; no EXPLAIN verified |
| D7 | N/A | not a reasoner |
| D8 | 5,7 | WAL, Raft metadata (partly UNVERIFIED) |
| D9 | 2,9 | upsert/delete; freshness not benchmarked |
| D10 | 11 | ACL via payload |
| D11 | N/A | no bitemporal; `revision` payload convention |
| D12 | N/A | |
| D13 | 2,5 | core |
| D14 | N/A | |
| D15 | N/A | |
| D16 | 3 | dashboard (not examined) |
| D17 | 3 | clients |
| D18 | 5,9 | keys, JWT, TLS |
| D19 | 5 | tenancy patterns |
| D20 | 7 | vendor numbers flagged |
| D21 | 1,10 | Apache-2.0; cloud |
| D22 | N/A | export via scroll/snapshots UNVERIFIED |
| D23 | N/A | not examined |
| D24 | 7 | vendor-only benchmarks |

## Appendix B. Capability mapping

| CAP | Qdrant | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-53 | native | qdrant-05,07 | BL-14 Partial | INTEGRATE | P1 |
| CAP-55 | native | qdrant-04 | BL-15 Implemented | REUSE/EXPERIMENT | P2 |
| CAP-46 | partial (filter) | qdrant-08 | BL-18 Absent | BUILD | P0 |
| CAP-47 | partial (patterns) | qdrant-03 | BL-20 Partial | INTEGRATE | P1 |
| CAP-54 | partial (BM25 1.20) | qdrant-06 | BL-13 Implemented | EXPERIMENT | P3 |
| CAP-04 | native (single node) | qdrant-07 | in-process | INTEGRATE | P1 |

## Appendix C. Evidence records (accessed 2026-10-26)

| CLAIM | product/version/date | claim | class | source | pub/access | conf | contradictory |
|---|---|---|---|---|---|---|---|
| qdrant-01 | repo main | Licence Apache-2.0 | Officially documented | GitHub licence API https://api.github.com/repos/qdrant/qdrant/license | /2026-10-26 | 0.95 | none |
| qdrant-02 | v1.18.3-1.20.0 | Release dates; 1.20.0 enforce_internal_auth default true with API key; 1.19.2 internal gRPC rw keys only; 1.19.1 rejects vector size >65536; 1.19.0 update queue 1M->200, mmap single-file default | Officially documented | GitHub releases https://github.com/qdrant/qdrant/releases | /2026-10-26 | 0.85 (list truncated at 100k chars) | none |
| qdrant-03 | docs | Multitenancy patterns, `is_tenant` 1.11, custom sharding 1.7, tiered 1.16, 1000 collection cap on Cloud, IDF stats shared (idf param 1.19) | Officially documented | https://qdrant.tech/documentation/guides/multiple-partitions/ | /2026-10-26 | 0.85 | none |
| qdrant-04 | docs | Query API prefetch 1.10, RRF, DBSF 1.11, formula 1.14, RRF k 1.16, weighted RRF 1.17; BM25 needs full-text index | Officially documented | https://qdrant.tech/documentation/concepts/hybrid-queries/ | /2026-10-26 | 0.85 | none |
| qdrant-05 | v1.18.2 benchmark; 2019 article | ACORN-1 per-request; recall 39.7->100% on 4% intersection; 5.4x/6.7x slower; max_selectivity 0.4; filterable HNSW article is 2019 design proposal | Officially documented (vendor benchmark) | https://qdrant.tech/articles/filtered-vector-search-acorn/ ; https://qdrant.tech/articles/filterable-hnsw/ | /2026-10-26 | 0.7 vendor-only | no independent benchmark |
| qdrant-06 | docs | Payload index types, cardinality estimation used for planning, strict mode, `nested` 1.20, BM25 index 1.20 | Officially documented | https://qdrant.tech/documentation/concepts/indexing/ | /2026-10-26 | 0.8 (page truncated) | none |
| qdrant-07 | docs | Memory tiers 1.19+, quantization variants, inline storage 1.16+, segment tuning, hnsw_ef, exact:true | Officially documented | https://qdrant.tech/documentation/ops-optimization/optimize/ | /2026-10-26 | 0.8 | none |
| qdrant-08 | docs | Static API key, read-only key 1.7, JWT RBAC HS256 with exp/access/value_exists, TLS off by default | Officially documented | https://qdrant.tech/documentation/security/ | /2026-10-26 | 0.85 | none |
| qdrant-09 | EOIP repo | in-process HNSW/BM25, ADR-005 no mandatory vector DB | Observed in source code | `retrieval/vectors.py:29,87`, `graph/vector_graph.py:78`, `64-decisions-and-adrs.md` | /2026-10-26 | 0.9 | none |

## Appendix D. Assumptions

Snapshot, delete/compaction, Raft, telemetry statements flagged UNVERIFIED because fetched pages were unavailable or summaries lacked text. Dates are GitHub API UTC. No local benchmark run.
