| Field | Value |
|---|---|
| Registry ID | T-C10-opensearch |
| Tier | A (only candidate combining full-text, ANN, hybrid and a built-in document-level security layer; BL-18 relevance) |
| Versions examined | OpenSearch 3.9.0 (2026-09-29), 3.8.0 (2026-08-05), 2.19.7 (2026-10-20); docs "latest" via documentation-website sources |
| Verified on | 2026-10-26 |
| Worker | V06 |

## 1. Identity, current status, tier, sources

OpenSearch (github.com/opensearch-project/OpenSearch) is a distributed search and analytics engine (Lucene-based, Java), forked from Elasticsearch 7.10; since September 2024 hosted by the **OpenSearch Software Foundation** under the Linux Foundation with a Governing Board and Technical Steering Committee [CLAIM-opensearch-02]. Licence: **Apache-2.0** (core LICENSE) [CLAIM-opensearch-01]. Components: core, k-NN plugin, neural-search, Security plugin, Dashboards, ML Commons, alerting and others; per-plugin licence not individually checked (assumed Apache-2.0, UNVERIFIED for each). Cadence: 3.x minors every ~8 weeks (3.6.0 2026-04-07, 3.7.0 06-09, 3.8.0 08-05, 3.9.0 09-29); 2.19 line patched (2.19.6 07-06, 2.19.7 10-20) [CLAIM-opensearch-03]. Status: active, production. Trap check: not Elasticsearch (SSPL/Elastic-licence/AGPL options), whose deep dive is separate (C10 Tier B).

## 2. Problem, workloads, workflows

Problem: distributed full-text + structured + vector search with RBAC and DLS. EOIP workloads: persistent BM25 (BL-13 is in-process and non-persistent), dense search (BL-14), hybrid (BL-15), and **source-ACL-filtered retrieval** (BL-18) where documents carry `acl_principals`.
Workflow: ingest chunk doc `{tenant, source_id, acl_hash, acl_principals[], text, embedding}` -> role per tenant/group with `dls: {"terms_set"/"terms": {"acl_principals": "${attr...}"}}` -> user queries via hybrid query + search pipeline -> hits already ACL-filtered by the engine -> EOIP graph re-check.

## 3. Feature inventory

| Feature | Status | Note |
|---|---|---|
| Document-level security (DLS) per index permission | present (Security plugin) | read-only restriction; **writes not restricted by DLS** [CLAIM-opensearch-04] |
| Field-level security, field masking | present | scripted `_update` blocked when FLS/DLS/masking active [CLAIM-opensearch-04] |
| Parameter substitution `${user.name}`, `${user.roles}`, `${attr.<TYPE>.<NAME>}`; fallback literals from 3.7.0 | present | missing variable errors otherwise [CLAIM-opensearch-04] |
| Evaluation modes `lucene-level` (fastest, no term-lookup queries), `filter-level`, `adaptive-level` (default) | present | [CLAIM-opensearch-04] |
| k-NN: Lucene HNSW (2.4+), Faiss HNSW (2.9+) / IVF (2.10+), JVector plugin (DiskANN-style), nmslib deprecated | present | [CLAIM-opensearch-05,06] |
| Filtering: efficient filter during search (approximate, hybrid of pre/post), Boolean post-filter, `post_filter`, scoring-script exact pre-filter; ACORN-style traversal for Faiss HNSW in 3.1+ with memory-optimized search | present | [CLAIM-opensearch-05] |
| Hybrid query (2.11), normalization processor (min_max, arithmetic_mean, weights), score ranker with RRF | present | [CLAIM-opensearch-07] |
| Full-text analyzers, BM25, aggregations | present (core Lucene) | not individually re-verified |
| Neural sparse, model serving via ML Commons | present (not examined in depth) | |
| Snapshots to repositories, snapshot management | present | details beyond intro UNVERIFIED [CLAIM-opensearch-09] |
| Multi-tenancy: index-per-tenant + DLS, Dashboards tenants | present (general knowledge; Dashboards tenants not examined) | |
| Docker/Helm/K8s Operator/tarball/RPM/DEB/Ansible | present | no offline guide [CLAIM-opensearch-08] |

## 4. Architecture

```
 client --HTTPS REST (basic/OIDC/SAML/mTLS)--> node (cluster-manager | data | ingest | coordinating roles)
   Security plugin: authc -> roles -> index permissions -> [DLS query | FLS | masking] injected into search
   Index = primary/replica shards (Lucene indices); segments: inverted index, doc values, vectors (HNSW graph per segment/engine)
   Search pipelines (request/response processors; hybrid normalization / RRF) ; ML Commons models (local or remote)
   snapshots -> repository (fs / object store)
```

## 5. Under-the-hood reconstruction

- **Data model**: JSON documents in indices with mappings (`keyword`, `text`, `knn_vector`, nested, etc.); `knn_vector` dimension fixed per field and engine/method (HNSW/IVF, space type) selected in mapping.
- **DLS mechanism (documented)**: role's `dls` is an OpenSearch query clause; a document is visible only if it matches; queries from several roles are OR-combined; a non-DLS role combined with DLS roles still yields DLS filtering unless `plugins.security.dfm_empty_overrides_all` is true; `lucene-level` mode applies the DLS query inside Lucene readers (efficient, no term-lookup queries), `filter-level` handles term-lookup queries for `get/search/mget/msearch` only [CLAIM-opensearch-04]. Pseudocode (inferred): `effective_query = AND(user_query, OR(dls_r for r in roles))` evaluated at reader level so aggregations and counts also respect it (aggregation behaviour not verified here). Text-field caveat: standard analyzer tokenises `User-1` into pieces, so DLS on analysed fields can over-match; use `keyword` [CLAIM-opensearch-04].
- **DLS x k-NN**: whether DLS is applied as a pre-filter inside ANN traversal (reader-level liveDocs-style filtering) or as a post-filter on ANN candidates, and whether `knn_vector` queries with `lucene-level` DLS return exactly `k` ACL-visible results, is **NOT PUBLICLY VERIFIED** (the docs fetched do not discuss it; search found nothing). Hypothesis: with `lucene-level` mode the DLS query behaves like a Lucene live-docs/filter on the segment reader, so Lucene/Faiss approximate filtering sees it; must be proven by test. This is the single most important POC item.
- **Filtered ANN**: efficient filtering on Lucene/Faiss/JVector engines; post-filter "may return significantly fewer than k results for a restrictive filter"; scoring-script pre-filter is exact but "does not scale when filtered subsets are large"; vendor recommends efficient filtering for 38%/80% selectivities and efficient filtering or scoring script at 2.5% (tables at 1M and 10M docs, k=100; numbers not extracted) [CLAIM-opensearch-05]. No exact-search-fallback threshold documented in the page read.
- **Hybrid**: `hybrid` query runs lexical and k-NN clauses; `normalization-processor` maps scores to a common scale (min_max) and combines (arithmetic_mean with weights); `score-ranker` applies RRF on positions [CLAIM-opensearch-07]. Pre-filter via top-level `filter` in hybrid; post-filter via `post_filter`.
- **Distribution**: shards/replicas, cluster-manager election (Raft-like in 2.x+/3.x not verified here), near-real-time refresh; deletes are tombstones in segments merged later (general Lucene behaviour, not source-verified); incremental indexing is native (`_bulk`, `_update`).
- **Memory/storage**: JVM heap (docs: set half of RAM via `OPENSEARCH_JAVA_OPTS`, default 1 GB), `vm.max_map_count>=262144` host setting; HNSW graphs live off-heap for native engines (general knowledge, UNVERIFIED); JVector provides disk-resident quantised index with incremental codebook refinement [CLAIM-opensearch-06,08].
- **Versioning/security**: demo security configuration uses known credentials; strong `OPENSEARCH_INITIAL_ADMIN_PASSWORD` required to start; replace before production [CLAIM-opensearch-08]. Supply chain: Java/Lucene dependencies; patch lines 2.19 and 3.x.

## 6. Inferred requirements for EOIP

FR: index template with `acl_principals` keyword (not analysed), `tenant`, `acl_hash`, `revision`; role generator mapping EOIP principals/groups to DLS; mandatory ACL recheck against graph; delete propagation by `_delete_by_query`/doc delete; hybrid pipeline definitions version-controlled. NFR: single-node profile (heap 1-2 GB for small corpora is an assumption; measure), `vm.max_map_count` preflight check in installer, TLS everywhere, no demo credentials, snapshot repository on local volume, Java process isolation, CPU-only.

## 7. Performance and resource model

No independent benchmarks used. Vendor tables exist for filtered k-NN recall (1M/10M docs, k=100) but their absolute values were not captured; do not quote. Single node cost = JVM heap + off-heap vector graphs + page cache + `max_map_count` host tuning; the heaviest of the three candidates to run on one node (inference from JVM + sharding architecture; EOIP must measure). DLS overhead: docs say complex DLS queries affect cluster performance, config max 1024 KB [CLAIM-opensearch-04]. Failure modes: DLS misconfiguration on analysed fields over-matches; `dfm_empty_overrides_all` footgun; DLS does not stop writes; post-filter under-return; circuit-breaker/heap pressure with large vector sets.

## 8. Strengths and how to match/exceed

| Strength | Match/exceed |
|---|---|
| Engine-enforced document-level security with attribute substitution | match semantics in EOIP's gateway; exceed by deriving DLS roles automatically from source ACL (BL-17) and graph identity |
| Lexical + ANN + filters + aggregations in one engine | INTEGRATE for deployments needing persistent BM25 and faceting |
| Apache-2.0, foundation governance | strongest licence/governance posture among the three |
| Mature ops: snapshots, RBAC, audit logs (audit not examined) | reuse |

## 9. Limitations with root causes

| Class | Item |
|---|---|
| Algorithmic | Filtered ANN recall depends on engine/mode; post-filter under-returns [CLAIM-opensearch-05]; DLS x ANN interaction undocumented |
| Operational | JVM, shards, heap tuning, `max_map_count`; heaviest single-node footprint; rolling upgrades across 2.19/3.x lines |
| Security design | DLS read-only: writers can modify hidden docs; scripted updates blocked; OR-combination across roles widens access; `dfm_empty_overrides_all`; analysed-field leakage |
| Licensing | core Apache-2.0; managed-service and plugin licences beyond core not verified |
| User friction | many processors/engines; nmslib deprecated; docs fragmented across versions |

## 10. Deployment, licensing, redistribution

Self-hosted (docker, K8s operator, tarball); managed services exist from several vendors (not examined). Air-gap: yes with mirrored images and plugins; docs lack an offline install guide [CLAIM-opensearch-08]. Apache-2.0 permits OEM redistribution including patent grant; trademark ("OpenSearch") rules for white-label need review (not examined). Legal-review trigger: low (Apache-2.0), note only.

## 11. Competitive delta against EOIP baseline

| Item | EOIP | OpenSearch |
|---|---|---|
| ACL | BL-18 Absent in `retrieval/service.py`, `query/policy.py`, `query/executor.py`; BL-17 stores `acl_hash` | DLS gives engine-level read filtering; EOIP must supply the principal mapping and keep ACLs fresh |
| Keyword | BL-13 in-process BM25 | persistent Lucene BM25, analyzers, facets |
| Vector | BL-14 Partial | Lucene/Faiss/JVector HNSW, filtering |
| Hybrid | BL-15 RRF | RRF score ranker + normalization pipelines |
| Tenancy | BL-20 contract | index-per-tenant/DLS; physical isolation is an EOIP choice |
| Backup | BL-50 | snapshots |
| Footprint | pure Python | JVM service |

## 12. Cards

STR-opensearch-01 | OpenSearch | DLS with attribute substitution | [opensearch-04] | engine-enforced ACL on search, aggregations (to verify) | integrate | generate roles from BL-17 permission metadata; `keyword` ACL fields; `lucene-level` mode | two principals with disjoint ACL see disjoint hits and counts in lexical, kNN and hybrid queries.
STR-opensearch-02 | OpenSearch | multi-mode filtered ANN | [opensearch-05] | recall control per filter selectivity | integrate | per-index engine choice by tenant size | recall@10 >= 0.95 vs exact at 1%, 10%, 50% ACL selectivity.
STR-opensearch-03 | OpenSearch | RRF/normalization hybrid pipelines | [opensearch-07] | server-side hybrid | match | EOIP RRF as reference oracle | rank parity with EOIP RRF on shared candidates.

**INV-opensearch-01 (ACL is read-only DLS; ingestion path unguarded).** Target 3.9.0 Security plugin. Evidence: DLS does not restrict writes [opensearch-04]. Root cause: *proven* semantics. Mitigation: EOIP is sole writer (connectors never write the graph; indexers are internal services with a distinct role); users never get index write permission. Options: (1) quick - read-only user roles; (2) native - dual-control: index writer role separate from query role, ACL fields immutable via ingest pipeline; (3) long-term - derive ACL fields only from graph snapshots with signed `acl_hash`. Test: attempt update by query-role user fails. Decision: ADOPT.
**INV-opensearch-02 (DLS x ANN recall unknown).** Root cause: *hypothesis*: DLS may behave as post-filter on k-NN candidates. Options: (1) quick - apply EOIP ACL filter as explicit `filter` inside k-NN clause in addition to DLS; (2) native - index-per-ACL-class for small classes; (3) long-term - hybrid router with exact scoring-script path for very selective principals. Benchmark: seed 1M chunks, 5 selectivity points, compare DLS-only vs explicit filter vs both; success: recall@10 >= 0.95 and zero ACL violations; baseline = Qdrant/pgvector arms. Failure: double filtering cost; stale ACL. Decision: EXPERIMENT (P0 because BL-18).
**INV-opensearch-03 (single-node weight).** Root cause: deployment (JVM + shards). Option: offer OpenSearch only in "enterprise search" profile; default pgvector/in-process. Decision: DEFER as default, ADOPT as optional. Seed hypotheses in 10.5 do not target OpenSearch.

## 13. Per-capability decisions

| Capability | Decision |
|---|---|
| CAP-46 ACL enforcement in retrieval | INTEGRATE DLS as a defence-in-depth layer; BUILD principal-to-role generator and recheck |
| CAP-54 full-text | INTEGRATE (optional backend) |
| CAP-53 vector | EXPERIMENT (filtered recall POC) |
| CAP-55 hybrid | INTEGRATE pipelines; REUSE EOIP RRF as oracle |
| CAP-47 tenancy | INTEGRATE index-per-tenant + DLS; BUILD isolation tests |
| CAP-74 backup | REUSE snapshots |
| CAP-04 single-node footprint | DEFER as default |

## 14. Tests and acceptance

1. DLS correctness matrix: lexical, kNN (Lucene, Faiss), hybrid, aggregations/count, `_mget`, scroll/PIT; roles OR-combined; `dfm_empty_overrides_all` off. 2. DLS x kNN recall per INV-opensearch-02, record `explain`/profile where available. 3. Write-bypass test (query-role user attempts update/delete). 4. Analysed-field leakage test (`User-1`/`User-2`). 5. Delete/ACL change propagation latency under refresh interval. 6. Single-node heap/RAM at 1M/10M chunks; startup preflight for `max_map_count`. 7. Snapshot/restore drill. 8. Offline install from mirrored images. 9. Licence/SBOM per plugin.

## 15. Risks and open questions

DLS x ANN semantics; aggregation/count leakage under DLS (not verified); DLS query size/complexity limits with many principals; refresh-interval ACL staleness; per-plugin licences; trademark; upgrade across 2.19 -> 3.x; JVM footprint on CPU-only edge nodes; Security plugin audit-log integrity (CAP-48) not examined.

## Appendix A. Dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Apache-2.0, foundation, cadence |
| D2 | 2 | ACL-aware enterprise search |
| D3 | 4 | node roles, plugins |
| D4 | 5 | Lucene segments, knn_vector engines |
| D5 | 5 | mappings, keyword vs text |
| D6 | 5 | hybrid pipelines, filter modes; EXPLAIN-like not examined |
| D7 | N/A | |
| D8 | 5,7 | shards/replicas; consistency details UNVERIFIED |
| D9 | 5 | bulk/incremental; delete behaviour general |
| D10 | 11 | ACL fields |
| D11 | N/A | |
| D12 | N/A | |
| D13 | 2,5 | core |
| D14 | N/A | |
| D15 | N/A | |
| D16 | 3 | Dashboards (not examined) |
| D17 | 3 | APIs, pipelines |
| D18 | 5,9 | DLS/FLS/masking, demo creds |
| D19 | 5,12 | index-per-tenant + DLS |
| D20 | 7 | no numbers; measure |
| D21 | 10 | Apache-2.0 |
| D22 | N/A | snapshots, _reindex |
| D23 | N/A | not examined |
| D24 | 7 | vendor tables not captured |

## Appendix B. Capability mapping

| CAP | OpenSearch | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-46 | native (DLS) / partial for ANN | opensearch-04 | BL-18 Absent | INTEGRATE+BUILD | P0 |
| CAP-54 | native | opensearch-05 | BL-13 Implemented | INTEGRATE | P2 |
| CAP-53 | native | opensearch-05,06 | BL-14 Partial | EXPERIMENT | P1 |
| CAP-55 | native | opensearch-07 | BL-15 Implemented | INTEGRATE | P2 |
| CAP-47 | partial | opensearch-04 | BL-20 Partial | INTEGRATE | P1 |
| CAP-74 | native | opensearch-09 | BL-50 | REUSE | P2 |
| CAP-45 | native RBAC | opensearch-04 | BL-19 | REUSE | P2 |

## Appendix C. Evidence records (accessed 2026-10-26)

| CLAIM | product/version/date | claim | class | source | pub/access | conf | contradictory |
|---|---|---|---|---|---|---|---|
| opensearch-01 | repo main | Apache License 2.0 | Officially documented | https://raw.githubusercontent.com/opensearch-project/OpenSearch/main/LICENSE.txt | /2026-10-26 | 0.95 | none |
| opensearch-02 | n/a, Sept 2024 | OpenSearch Software Foundation under Linux Foundation; Governing Board and TSC | Third-party report (LF/AWS blogs) | https://www.linuxfoundation.org/blog/how-the-opensearch-software-foundation-will-ensure-long-term-sustainability-of-the-opensearch-project | 2024-09 / 2026-10-26 | 0.85 | none |
| opensearch-03 | 3.6.0-3.9.0; 2.19.6-2.19.7 | Release dates (3.9.0 2026-09-29 etc.) | Officially documented | https://api.github.com/repos/opensearch-project/OpenSearch/releases | /2026-10-26 | 0.9 | none |
| opensearch-04 | docs main (3.7+ features) | DLS read-only semantics, substitution, modes, role OR-combination, dfm_empty_overrides_all, 1024 KB cap, scripted update blocked, text-analyzer caveat | Officially documented | https://github.com/opensearch-project/documentation-website/blob/main/_security/access-control/document-level-security.md | /2026-10-26 | 0.85 | no DLS x kNN statement found |
| opensearch-05 | docs main | k-NN filtering approaches and engines/versions; ACORN in 3.1+; post-filter under-return; scoring-script exact | Officially documented | https://github.com/opensearch-project/documentation-website/blob/main/_vector-search/filter-search-knn/index.md | /2026-10-26 | 0.85 | none |
| opensearch-06 | docs main | JVector engine: disk-based DiskANN-style, quantised, incremental codebook refinement | Officially documented | .../_vector-search/optimizing-storage/index.md | /2026-10-26 | 0.7 (partial page) | none |
| opensearch-07 | docs main | Hybrid search from 2.11; normalization min_max, arithmetic_mean weights; score ranker RRF; pre/post filter | Officially documented | .../_vector-search/ai-search/hybrid-search/index.md | /2026-10-26 | 0.8 | other techniques may exist |
| opensearch-08 | docs main | Heap = half RAM, default 1 GB; max_map_count 262144; strong initial admin password; no offline install doc | Officially documented | .../_install-and-configure/install-opensearch/index.md | /2026-10-26 | 0.8 | none |
| opensearch-09 | docs main | Snapshots back up indexes and cluster state; API and snapshot management | Officially documented | .../_tuning-your-cluster/availability-and-recovery/snapshots/index.md | /2026-10-26 | 0.5 (intro only) | none |
| opensearch-10 | EOIP | BL-18 absent in retrieval/policy/executor | Observed in source code | `01-SYSTEM-BASELINE.md` BL-18 | /2026-10-18 | 0.8 | U-04 residual uncertainty |

## Appendix D. Assumptions

The request path "docs.opensearch.org/latest" returned navigation only, so raw documentation-website sources on `main` were used; "main" may be ahead of 3.9.0 (e.g. 3.7.0 fallback feature noted). DLS x ANN not verified anywhere and treated as hypothesis. Plugin licences, audit logging and Dashboards tenancy not examined.
