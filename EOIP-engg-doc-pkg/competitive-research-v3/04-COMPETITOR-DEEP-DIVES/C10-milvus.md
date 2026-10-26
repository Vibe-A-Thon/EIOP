| Field | Value |
|---|---|
| Registry ID | T-C10-milvus |
| Tier | B (distributed vector DB; scale-out reference, not a one-node fit) |
| Versions examined | Milvus 3.0.3 (2026-10-14), 3.0.0 (2026-07-29), 2.6.25 (2026-09-29); pymilvus 3.0.2 (PyPI; date UNVERIFIED) |
| Verified on | 2026-10-26 (brief says 10-18; later date used, consistent with other V-batches) |
| Worker | V23 |

## 1. Identity, status, sources
Milvus (github.com/milvus-io/milvus; Zilliz; LF AI & Data project; Go/C++) is a vector database. Licence Apache-2.0 [CLAIM-milvus-01]. Active: 3.0.x line (3.0.0 2026-07-29, 3.0.3 2026-10-14) plus 2.6.x maintenance (2.6.25 on 2026-09-29) [CLAIM-milvus-02]. Managed offering: Zilliz Cloud. Enterprise-only features in the OSS repo: NOT PUBLICLY VERIFIED. Sources: repo releases/LICENSE, release notes, RBAC, partition-key, hybrid-search, install, backup docs (6).

## 2. Problem and workloads
Billion-scale ANN with scalar filtering, sparse/BM25 and multi-vector hybrid. EOIP fit: only at a scale EOIP does not target in P1 (one-node first). Workflow: chunk -> embed -> insert with `tenant_id` partition key -> hybrid search (dense + BM25 sparse, RRF) filtered by tenant and ACL scalar field -> candidate IDs -> graph ACL re-check.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Dense, sparse, BM25 function (`SPARSE_INVERTED_INDEX`, MaxScore/WAND) | present [CLAIM-milvus-04] |
| Hybrid search, RRFRanker (k param), WeightedRanker | present [CLAIM-milvus-04] |
| Partition key (default 16 partitions, `num_partitions`), partition-key isolation (per-key HNSW index; single key only) | present [CLAIM-milvus-03] |
| RBAC at instance/database/collection, privilege groups | present; no row/filter-level security documented [CLAIM-milvus-05] |
| Milvus Lite (pip, local file), Standalone, Distributed (K8s) | present [CLAIM-milvus-06] |
| Snapshots (3.0, point-in-time read-only), online schema change, entity TTL, External Collections over lake data | present in 3.0 [CLAIM-milvus-02] |
| Milvus Backup (CLI/API; collection metadata + segments) | present, separate tool [CLAIM-milvus-07] |
| Iterative filtered ANN / filtered-HNSW recall guarantees | UNVERIFIED (official page not retrieved) |

## 4. Architecture
```
clients (pymilvus/REST/gRPC) -> proxy -> coordinators (root/data/query) [control]
 WAL: Woodpecker (embedded in Standalone, own service in Distributed) -> object storage (MinIO/S3)
 metadata: etcd | stream/query/data nodes load segments from object storage; index nodes build indexes
```

## 5. Under-the-hood reconstruction
- **Storage:** log-structured; WAL -> sealed segments on object storage; compaction; 3.0 adds manifest-based columnar "Storage V3 (Loon)", opt-in, one-way (no rollback to 2.6 once used) [CLAIM-milvus-02].
- **Filtering:** scalar filter evaluated to a bitset then ANN; third-party analysis (arXiv 2602.11443) says restrictive filters use a deterministic fallback rather than a cost-based optimiser (hypothesis for current version, confidence 0.4).
- **Tenancy:** partition key hashes value mod partition count; with isolation property, each key value gets its own HNSW index but queries must pin exactly one key [CLAIM-milvus-03].
- **Hybrid:** one ANN request per vector field, merged by ranker [CLAIM-milvus-04].
- **Security:** users/roles/privileges on three resource levels; bcrypt cost raised in 3.0.1 forcing credential rotation [CLAIM-milvus-02].

## 6. Inferred requirements
FR: tenant + ACL fields mandatory on every insert and query; deletes by filter. NFR: do not require etcd + object store + WAL for the one-node tier; derived index rebuildable from graph.

## 7. Performance and resource model
No benchmark was run or verified. Three mandatory dependencies (WAL, object store, metadata store) [CLAIM-milvus-06]; docs give no CPU/RAM figures (sizing tool only). Standalone is said to reach ~100M vectors (vendor claim). Failure modes: partition-key tenants beyond partition count share partitions; isolation requires HNSW and single-key filter.

## 8. Strengths
Scale-out and lake-native storage; native BM25+dense+rerank in one engine; partition-key tenancy with optional per-tenant index; Apache-2.0. Match: EOIP `VectorIndexPort` with tenant-scoped partitions; exceed: ACL enforced in EOIP, re-checked against graph.

## 9. Limitations
| Class | Item |
|---|---|
| Operational overhead | etcd + MinIO + WAL even in Standalone; Distributed needs Kubernetes [CLAIM-milvus-06] |
| Friction | breaking upgrades in 3.0 (no rollback, hash rotation, new `ImportBinlog` privilege, Pulsar >= 2.8) [CLAIM-milvus-02]; backup compatibility matrix restores 2.6 only to 2.6 [CLAIM-milvus-07] |
| Algorithmic/semantic | no document-level ACL beyond filter expressions (a caller-supplied filter is the only control; hypothesis, 0.5) |
| Licensing | none found; Apache-2.0 |

## 10. Deployment and licensing under EOIP constraints
Self-hosted, air-gap viable (images mirror-able; no mandatory cloud) but heavy. Apache-2.0 redistributable; Zilliz Cloud irrelevant. No legal trigger. One-node: Milvus Lite (local file) is closest but is for "a few million vectors" and lacks partition keys per third-party docs (LangChain note; confidence 0.5) [CLAIM-milvus-03].

## 11. Competitive delta vs baseline
BL-14 (partial, in-process HNSW): Milvus offers scalable ANN, BM25 and sparse. BL-15 (RRF implemented in-process): Milvus RRFRanker server-side. BL-18 (source-ACL absent in retrieval; note `hybrid_vector_service.py` now filters on `acl_allow_roles` in-memory only, brute-force cosine, no external backend, no persistence): Milvus gives no ACL semantics beyond scalar filters. BL-20: partition-key tenancy exceeds EOIP's contract. CLAIM refs: none from baseline.

## 12. Cards
| ID | Card |
|---|---|
| STR-milvus-01 | Per-tenant HNSW via partition-key isolation. Evidence milvus-03. Value: noisy-neighbour and recall isolation. Approach: match in `VectorIndexPort` (per-tenant index option). Test: tenant A queries cannot change tenant B recall. |
| STR-milvus-02 | Server-side BM25 sparse + dense + ranker. Evidence milvus-04. Integrate pattern, not engine. |
| INV-milvus-01 | Target Milvus 3.0.3 standalone, EOIP one-node. Limitation: three infrastructure dependencies [milvus-06]. Root cause deployment (proven). Options: (a) skip; (b) native in-process index with persistence (EOIP `hybrid_vector_service` + disk); (c) pluggable port with Qdrant/pgvector default. Selected (c). POC: p95 and RSS of a 1M x 768 index on 8 GB container vs Qdrant/pgvector. Defensibility: ACL-aware port. Decision DEFER Milvus. |
| INV-milvus-02 | Irreversible storage-format upgrades [milvus-02]; mitigated by treating the vector store as a rebuildable derived index (ADR-004 style). Decision ADOPT as design rule. |
Seed hypotheses targeting Milvus: none identified.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-53 vector search | INTEGRATE (optional adapter, scale tier) |
| CAP-54/55 BM25 + fusion | REFERENCE (pattern); BUILD in EOIP |
| CAP-47 tenant isolation | REUSE pattern (partition + per-tenant index) |
| CAP-46 source ACL | BUILD (EOIP-side filter + graph re-check) |
| CAP-74 backup | REJECT reliance; rebuild from graph |
| CAP-04 one-node | REJECT Milvus for P1; EXPERIMENT Lite only |

## 14. Tests and acceptance
1. Adapter conformance suite: insert with tenant+ACL, cross-tenant query returns 0. 2. Delete propagation: tombstone in graph -> vector absent within SLA. 3. Filtered recall at 1%, 10%, 50% selectivity vs exact search (recall@10 >= 0.95). 4. Footprint of Standalone idle and at 1M vectors. 5. Backup/restore round trip across a minor upgrade.

## 15. Risks and open questions
Official filtered-ANN behaviour unverified; `gh` rate-limited so repo-level facts rely on release pages; Lite capabilities; whether privilege model can be scoped by field value (no evidence found).

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Apache-2.0, active |
| D2 | 2 | scale vector search |
| D3 | 4 | proxy/coords/WAL/object store |
| D4 | 5 | segments, Storage V3 |
| D5 | N/A | no ontology |
| D6 | 5 | scalar bitset + ANN; hybrid rankers |
| D7 | N/A | none |
| D8 | 5,7 | distributed; consistency UNVERIFIED |
| D9 | 3 | import, binlog import; external collections |
| D10 | 11 | no evidence spans |
| D11 | 3 | snapshots, TTL |
| D12 | N/A | no graph ML |
| D13 | 2,3 | retrieval engine |
| D14 | N/A | |
| D15 | N/A | |
| D16 | 3 | Attu UI not examined |
| D17 | 3 | SDKs (Python, Node, Java, Go) |
| D18 | 5,9 | RBAC; no row ACL |
| D19 | 5 | partition key |
| D20 | 7 | no verified numbers |
| D21 | 1,10 | Apache-2.0; Zilliz Cloud |
| D22 | 3 | Lance/Parquet interchange |
| D23 | N/A | none examined |
| D24 | 15 | vendor docs; limited independent evidence |

## Appendix B. Capability mapping
| CAP | Milvus | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-53 | native | milvus-04 | BL-14 partial | INTEGRATE | P2 |
| CAP-54 | native (BM25) | milvus-04 | BL-13 impl. | REFERENCE | P3 |
| CAP-55 | native | milvus-04 | BL-15 impl. | BUILD | P2 |
| CAP-46 | absent | milvus-05 | BL-18 absent | BUILD | P0 |
| CAP-47 | native | milvus-03 | BL-20 partial | REUSE pattern | P1 |
| CAP-74 | partial | milvus-07 | not in baseline | REJECT | P3 |
| CAP-04 | partial (Lite) | milvus-06 | BL-14 | EXPERIMENT | P3 |

## Appendix C. Evidence
| ID | Product/date | Claim | Class | Source | Access | Conf. | Contra |
|---|---|---|---|---|---|---|---|
| CLAIM-milvus-01 | master, 2026-10-26 | LICENSE is Apache 2.0 | Observed | github.com/milvus-io/milvus LICENSE | 2026-10-26 | 0.9 | none |
| CLAIM-milvus-02 | 3.0.3 / 2026-10-14 | 3.0.0 on 2026-07-29, 3.0.3 on 2026-10-14; Storage V3 opt-in, no rollback; Woodpecker WAL; snapshots; bcrypt rotation; ImportBinlog privilege; 2.6.25 on 2026-09-29 | Documented | milvus.io/docs/release_notes.md; github releases | 2026-10-26 | 0.85 | none |
| CLAIM-milvus-03 | docs | Partition key: 16 partitions default, isolation needs HNSW and single key; Lite lacks partition key (third party) | Documented / third-party | milvus.io/docs/use-partition-key.md; LangChain Milvus docs | 2026-10-26 | 0.8 / 0.5 | none |
| CLAIM-milvus-04 | docs | Hybrid search with RRFRanker/WeightedRanker; BM25 function with sparse index | Documented | milvus.io/docs/multi-vector-search.md | 2026-10-26 | 0.85 | none |
| CLAIM-milvus-05 | docs | RBAC at instance/database/collection; no row-level security mentioned | Documented | milvus.io/docs/rbac.md | 2026-10-26 | 0.7 | absence of mention only |
| CLAIM-milvus-06 | docs | Modes Lite/Standalone/Distributed; requires WAL, object store, metadata store (Woodpecker, MinIO, etcd defaults) | Documented | milvus.io/docs/install-overview.md | 2026-10-26 | 0.85 | none |
| CLAIM-milvus-07 | docs | Backup tool copies metadata+segments; 2.6.x restores only to 2.6.x | Documented | milvus.io/docs/milvus_backup_overview.md | 2026-10-26 | 0.8 | none |

## Appendix D. Assumptions
Date 2026-10-26 used. Milvus Lite assumed unsuitable for partition-key tenancy (third-party). EOIP target scale is one node (ADR-005).
