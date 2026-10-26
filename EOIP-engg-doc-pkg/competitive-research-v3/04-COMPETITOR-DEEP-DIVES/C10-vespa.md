| Field | Value |
|---|---|
| Registry ID | T-C10-vespa |
| Tier | B (hybrid ranking engine; strongest ranking pipeline and streaming-search tenancy model) |
| Versions examined | Vespa v8.763.13 (2026-10-05, newest system tag found; no v9 tag), v8.754.14 (2026-09-21); Vespa CLI 8.763.13 |
| Verified on | 2026-10-26 |
| Worker | V23 |

## 1. Identity, status, sources
Vespa (github.com/vespa-engine/vespa; Vespa.ai, spun out of Yahoo; C++ content engine "proton" plus Java containers). Licence Apache-2.0 (LICENSE verified) [CLAIM-vespa-01]. Active, very frequent 8.x releases (several per month) [CLAIM-vespa-02]. Managed: Vespa Cloud. Community-vs-enterprise: no core feature gating found; Cloud-only security items (tokens, Private Endpoints, control-plane roles) are Cloud features, not OSS. Sources (6): LICENSE, tags, phased ranking, ANN, streaming search, multinode/security docs.

## 2. Problem and workloads
Real-time serving with hybrid retrieval (WAND/BM25, ANN, tensors) and multi-phase ML ranking. EOIP fit: ranking research and personal-data tenancy; heavy for P1. Workflow: schema with `tenant`, `acl` fields; rank profile with first phase BM25+closeness, global-phase `reciprocal_rank_fusion`; one request returns fused IDs.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Tensor fields, HNSW (int8/bfloat16/float/double), exact NN | present [CLAIM-vespa-04] |
| Phased ranking: first, second (content nodes), global (container; ONNX, GPU) | present [CLAIM-vespa-03] |
| `normalize_linear`, `reciprocal_rank`, `reciprocal_rank_fusion` (k default 60) | present [CLAIM-vespa-03] |
| Filtered ANN: pre-filter default, post-filter via thresholds, `exploreAdditionalHits`, parallel pre-filter since 8.78 | present [CLAIM-vespa-04] |
| Real-time vector add/update/remove | present [CLAIM-vespa-04] |
| Streaming search (per-group, no index, ~45 B/doc memory, exact NN only) | present [CLAIM-vespa-05] |
| mTLS data plane, read/write client authorisation (Cloud docs) | present (Cloud page); OSS self-managed mTLS page not retrieved |
| Document-level ACL | absent as a built-in; done via filter/group or custom searcher (page not found; UNVERIFIED) |
| Backup/restore tooling | NOT PUBLICLY VERIFIED in this pass (visit/feed export presumed) |

## 4. Architecture
```
client -> container cluster (stateless: query/feed, searchers, global-phase, ONNX)
       -> content cluster (stateful proton nodes: documents, attributes, HNSW, inverted index)
admin: config servers (ZooKeeper-backed, 1 or 3) + cluster controllers + slobrok
app package (services.xml, schemas, rank profiles, models) deployed to config server
```

## 5. Under-the-hood reconstruction
- **Data model:** document schema with typed fields; attributes in memory (tensors, HNSW), index fields on disk (inverted); redundancy via distribution over content groups.
- **Filtering:** boolean filter yields a candidate set; if pre-filtering, HNSW search is restricted; thresholds `approximate-threshold` and `post-filter-threshold` per rank profile choose exact vs graph vs post-filter; `geoLocation` and predicate operators run after neighbours are fetched so fewer hits than `totalTargetHits` may arrive [CLAIM-vespa-04]. One graph per tensor field per node; HNSW search itself single-threaded.
- **Ranking:** first-phase on every retrieved hit (must be cheap) -> second-phase top 100 per node -> container merges -> global-phase top 100 global hits, where normalisation covers only re-ranked hits so `rerank-count` changes results [CLAIM-vespa-03].
- **Streaming mode:** doc id carries group; query sets `streaming.groupname`; no HNSW so vector search exact within the group; no stemming at feed; no parent/child [CLAIM-vespa-05]. Mixing streaming and indexed in one cluster discouraged.
- **Scaling:** adding content nodes triggers redistribution taking hours; containers scale easily [CLAIM-vespa-06].
- **Security:** data-plane authorisation read/write per client mapped to HTTP verbs on Cloud; no row-level model found [CLAIM-vespa-07].

## 6. Inferred requirements
FR: ACL and tenant as group key or filter; global-phase fusion; rank profile versioning. NFR: JVM containers + proton processes; config server even on one node.

## 7. Performance and resource model
No benchmark run. Memory dominated by raw vectors and HNSW graph (docs: float to bfloat16 can halve cost, vendor claim) [CLAIM-vespa-04]; streaming mode ~45 bytes/doc [CLAIM-vespa-05]. Single-node: config server and services on one host; docs example minimum AWS t2.large (a doc example, not a requirement) [CLAIM-vespa-06]. Failure modes: long content-node rebalance, hit starvation under pre-filter + predicates, `rerank-count` coupling.

## 8. Strengths
Best-in-class multi-phase ranking with ML models; streaming-search tenancy cheap for millions of tiny tenants; real-time updates; Apache-2.0. Match: staged ranking pipeline in EOIP (candidate generation -> ACL -> rerank); exceed: ACL-before-rerank guarantees plus graph evidence in rank features.

## 9. Limitations
| Class | Item |
|---|---|
| Operational | multi-process JVM+C++ stack, config servers, application-package deployment model [vespa-06] |
| Friction | steep schema/rank-profile learning; no ACL primitive |
| Algorithmic | streaming mode has no ANN index and no stemming; pre-filter hit starvation [vespa-04,05] |
| Scaling | content redistribution hours [vespa-06] |
| Licensing | none (Apache-2.0) |

## 10. Deployment and licensing
Self-hosted Docker/K8s, air-gap viable (images mirror-able; no phone-home found, not exhaustively checked). Apache-2.0 redistributable. No legal trigger. Heavier than needed for one-node P1.

## 11. Competitive delta vs baseline
BL-15 RRF implemented in-process: Vespa offers RRF and normalised-linear fusion inside a multi-phase ranker, which EOIP lacks (BL-13/14/15 are single-stage). BL-18 absent; new `retrieval/hybrid_vector_service.py` applies role ACL in-memory plus a graph-centrality boost (0.05 x centrality) after fusion, no external backend. Vespa could host both but EOIP must still enforce ACL. BL-20 partial: streaming-mode groups are a model for EOIP's per-tenant isolation without per-tenant indexes.

## 12. Cards
| ID | Card |
|---|---|
| STR-vespa-01 | Phased ranking incl. global-phase fusion/normalisation [vespa-03]. Value: cheap candidate stage, costly rerank only on ACL-safe survivors. Match in EOIP retrieval pipeline stages. Test: nDCG@10 vs RRF baseline on EOIP benchmark. |
| STR-vespa-02 | Streaming search for many small tenants [vespa-05]. Value: tiny memory per doc. Match: tenant-scoped exact scan for tenants below N chunks (EOIP in-memory index is exactly this). Test: tenants under 50k chunks, latency of exact scan. |
| INV-vespa-01 | v8.763. Limitation: no ACL primitive, ACL by filter only; pre-filter hit starvation [vespa-04]. Root cause semantics (hypothesis). Options: (a) filter in query; (b) custom searcher doing ACL then fusion; (c) EOIP ACL-first candidate generator. Select (c) with Vespa as optional ranker. POC: adversarial ACLs at 0.1% selectivity, recall vs exact. Decision EXPERIMENT. |
| INV-vespa-02 | Operational weight [vespa-06]. Option: do not embed; document as customer-operated backend. Decision DEFER. |
Seed hypotheses: none targeting Vespa.

## 13. Per-capability decisions
CAP-55 REFERENCE and BUILD (phased pipeline); CAP-53 INTEGRATE optional; CAP-54 REFERENCE; CAP-47 REUSE streaming-group pattern; CAP-46 BUILD; CAP-04 REJECT for P1; CAP-74 DEFER (unverified).

## 14. Tests and acceptance
1. Stage-ordering test: no document outside caller ACL reaches rerank. 2. nDCG/recall vs current RRF. 3. Filtered ANN at several selectivities incl. predicates. 4. Small-tenant exact-scan latency. 5. Single-node idle RSS. 6. Backup route proof if adopted.

## 15. Risks and open questions
OSS security docs and ACL idioms unretrieved; backup procedure; resource minimums; whether global-phase ONNX is usable air-gapped (models local, believed yes).

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Apache-2.0, active |
| D2 | 2 | ranking engine |
| D3 | 4 | container/content/admin |
| D4 | 5 | attributes, HNSW, inverted |
| D5 | N/A | schema only |
| D6 | 5 | phased ranking, filters |
| D7 | N/A | |
| D8 | 5 | redistribution; consensus not examined |
| D9 | N/A | |
| D10 | N/A | |
| D11 | N/A | |
| D12 | 3 | ONNX/XGBoost ranking models |
| D13 | 2,5 | retrieval + rerank |
| D14 | N/A | |
| D15 | N/A | |
| D16 | N/A | |
| D17 | 3 | CLI, LSP |
| D18 | 5 | mTLS, authz (Cloud) |
| D19 | 5 | streaming groups |
| D20 | 7 | docs numbers only |
| D21 | 1,10 | Apache-2.0 |
| D22 | N/A | |
| D23 | N/A | |
| D24 | 15 | official docs only |

## Appendix B. Capability mapping
| CAP | Vespa | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-53 | native | vespa-04 | BL-14 partial | INTEGRATE | P3 |
| CAP-54 | native | vespa-03 | BL-13 | REFERENCE | P3 |
| CAP-55 | native | vespa-03 | BL-15 | BUILD | P2 |
| CAP-46 | absent | vespa-07 | BL-18 absent | BUILD | P0 |
| CAP-47 | partial | vespa-05 | BL-20 | REUSE pattern | P2 |
| CAP-04 | partial | vespa-06 | BL-14 | REJECT | P3 |

## Appendix C. Evidence
| ID | Product/date | Claim | Class | Source | Access | Conf. | Contra |
|---|---|---|---|---|---|---|---|
| CLAIM-vespa-01 | master | Apache License 2.0 | Observed | github.com/vespa-engine/vespa LICENSE | 2026-10-26 | 0.9 | none |
| CLAIM-vespa-02 | tags | v8.763.13 on 2026-10-05; v8.754.14 09-21; no v9 tag | Documented | github.com/vespa-engine/vespa/tags | 2026-10-26 | 0.8 | none |
| CLAIM-vespa-03 | docs | Phased ranking; normalize_linear, reciprocal_rank (k 60), fusion shorthand; global-phase top 100 | Documented | docs.vespa.ai/en/ranking/phased-ranking.html | 2026-10-26 | 0.85 | none |
| CLAIM-vespa-04 | docs | Pre-filter default, thresholds, exploreAdditionalHits, parallel pre-filter 8.78, real-time updates, memory/bfloat16 | Documented | docs.vespa.ai/en/querying/approximate-nn-hnsw.html; nearest-neighbor-search.html | 2026-10-26 | 0.8 | none |
| CLAIM-vespa-05 | docs | Streaming search: group names, 45 B/doc, no HNSW, limits | Documented | docs.vespa.ai/en/performance/streaming-search.html | 2026-10-26 | 0.85 | none |
| CLAIM-vespa-06 | docs | Multinode: config servers, content redistribution takes hours, single-node example t2.large | Documented | docs.vespa.ai/en/operations/self-managed/multinode-systems.html | 2026-10-26 | 0.75 | example only |
| CLAIM-vespa-07 | Cloud docs | mTLS or tokens; client read/write authorisation; no document-level security statement | Documented | docs.vespa.ai/en/security/guide.html | 2026-10-26 | 0.6 | Cloud page, not OSS |

## Appendix D. Assumptions
Vespa Cloud security pages assumed representative of OSS mTLS. Year of tags 2026.
