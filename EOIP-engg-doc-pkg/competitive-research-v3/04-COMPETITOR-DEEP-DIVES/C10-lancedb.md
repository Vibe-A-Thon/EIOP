| Field | Value |
|---|---|
| Registry ID | T-C10-lancedb |
| Tier | B (embedded vector DB; best match to EOIP one-node, library-in-process model) |
| Versions examined | lancedb PyPI 0.40.0 (date UNVERIFIED); GitHub pre-release v0.41.0-beta.14 (2026-10-25) |
| Verified on | 2026-10-26 |
| Worker | V23 |

## 1. Identity, status, sources
LanceDB (github.com/lancedb/lancedb; LanceDB Inc.; Rust core, Python/TypeScript/Rust/Java SDKs) is an embedded multimodal retrieval database on the open Lance columnar format. OSS licence Apache-2.0 (LICENSE and PyPI classifier) [CLAIM-lancedb-01]. Very frequent beta releases (beta.10 to beta.14 between 10-20 and 10-25) [CLAIM-lancedb-02]. Commercial: LanceDB Enterprise (distributed, `db://`, sales-led, private deployment) sharing format and table model [CLAIM-lancedb-03]. Which features are Enterprise-only (e.g. scale-out indexing, access controls): NOT PUBLICLY VERIFIED. Sources (5): LICENSE, releases, docs.lancedb.com home, filtering/versioning/hybrid pages via search, PyPI.

## 2. Problem and workloads
In-process vector, FTS and hybrid search over local disk or object storage, plus versioned multimodal tables. EOIP workflow: per-tenant table (or one table with `tenant_id`); `where("tenant_id = 't1' AND acl_hash IN (...)")` pre-filter + vector + FTS -> RRF -> IDs -> graph ACL re-check.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Vector index (IVF-based and HNSW variants; exact specifics UNVERIFIED) | present |
| Scalar indexes BTREE (default), BITMAP, LABEL_LIST | present [CLAIM-lancedb-04] |
| Pre-filter default in current docs; post-filter selectable; older docs said post-filter default | present, doc conflict [CLAIM-lancedb-04] |
| FTS index (`create_fts_index`), hybrid with `RRFReranker` default, Cohere/CrossEncoder rerankers | present [CLAIM-lancedb-05] |
| Table versioning, checkout/restore, branching, compaction | present [CLAIM-lancedb-06] |
| Auth, RBAC, document-level ACL in OSS | absent (embedded library; no server) - hypothesis from architecture, 0.6 |
| Backup/restore | file/object copy of dataset plus versions; no dedicated tool found |
| Server mode, multi-tenant namespace service | Enterprise (per docs home); details UNVERIFIED |

## 4. Architecture
```
app process (Python/TS/Rust) -> lancedb lib -> Lance dataset on local FS | S3/GCS/Azure
  dataset: manifest versions -> fragments (columnar data files) + deletion files + index files
  no daemon, no network port (OSS); Enterprise: db:// remote service
```

## 5. Under-the-hood reconstruction
- **Data model:** table = Lance dataset with schema; vector columns, scalar, blob. Each write produces a new immutable version (manifest); readers pin a version [CLAIM-lancedb-06].
- **Deletes:** rows marked in fragment deletion files; data recoverable while a referencing version exists; compaction rewrites fragments and removes deleted rows but raises disk use until old versions are cleaned [CLAIM-lancedb-06]. Implication for right-to-erasure: physical erasure needs compaction + version cleanup (verified behaviour; process is EOIP's burden).
- **Filtering:** pre-filter applies `where` before ANN; too-selective filter can miss neighbours, docs suggest raising `nprobes` or bypassing the vector index when highly selective; without scalar index the predicate is evaluated on every row [CLAIM-lancedb-04].
- **Hybrid:** vector and FTS result sets merged by reranker, RRF default; `normalize` "score" or "rank" [CLAIM-lancedb-05].
- **Concurrency:** snapshot reads, optimistic commits; behaviour of concurrent writers and object-store commits NOT VERIFIED in this pass.
- **Security:** none in library; isolation = separate table/dataset path per tenant plus OS/file permissions (design inference).

## 6. Inferred requirements
FR: one dataset per tenant; scalar indexes on `tenant_id`, `acl_hash`; scheduled compaction and version cleanup bound to erasure SLA. NFR: no extra service; run inside EOIP worker process.

## 7. Performance and resource model
No benchmark run or verified. Embedded: memory is process-local; disk-resident indices suit low RAM (vendor positioning, UNVERIFIED numbers). Failure modes: unbounded version growth, writer conflicts, pre-filter recall loss at extreme selectivity.

## 8. Strengths
Zero-ops one-node fit; dataset versioning gives time-travel and rollback of an index; Apache-2.0; file-copy tenant export/delete. Match: STR-lancedb-01 in `VectorIndexPort`; exceed: bind index versions to EOIP revisions (BL-37).

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | selective pre-filter can lose recall [lancedb-04] |
| Operational | version/compaction hygiene; erasure not immediate [lancedb-06] |
| Friction | pre/post default conflict across doc versions; fast-moving 0.x API with betas [lancedb-02,04] |
| Security | no ACL layer; Enterprise gating unclear |
| Licensing | Apache-2.0; no restriction found |

## 10. Deployment and licensing
Embedded, air-gap trivial (pip wheel, no network); object-store backends optional. Apache-2.0 redistributable; Enterprise terms are sales-led (not evaluated). No legal trigger beyond verifying the Lance format and any bundled dependencies.

## 11. Competitive delta vs baseline
BL-14 partial (hashing embedder, pure-Python HNSW, in-process): LanceDB provides a persistent embedded ANN+FTS engine with the same deployment shape, directly upgrading BL-13/14/15. BL-18 absent: no help; new `retrieval/hybrid_vector_service.py` already filters `acl_allow_roles` over in-memory documents with brute-force cosine and supports no external backend. BL-25 tombstones map to LanceDB deletion files. BL-37 revisions map to dataset versions. Lock: `requirements.lock` has no numpy or vector client today (baseline).

## 12. Cards
| ID | Card |
|---|---|
| STR-lancedb-01 | Embedded persistent ANN+FTS+hybrid, no service [lancedb-01,05]. Value: fits one-node, air-gap. Integrate as default persistent backend candidate behind `VectorIndexPort`. Test: replace in-memory index, same conformance suite, RSS and restart time. |
| STR-lancedb-02 | Versioned tables [lancedb-06]. Exceed: pin index version to EOIP policy epoch; roll back after bad re-embed. Test: shadow index cutover/rollback (matches existing shadow-index design). |
| INV-lancedb-01 | v0.40.0. Limitation: no ACL layer, tenant isolation is path-based. Root cause architecture (proven: embedded). Options: (a) per-tenant dataset dirs + EOIP filter; (b) encrypted per-tenant datasets; (c) ACL-aware index service. Select (a). POC: 1,000 tenants, open-handle and latency cost. Decision ADOPT. |
| INV-lancedb-02 | Erasure latency via soft delete [lancedb-06]. Option (b) scheduled compaction + cleanup tied to DSAR SLA. POC: delete then forensic scan of data files. Decision EXPERIMENT. |
Seed hypotheses: none targeting LanceDB.

## 13. Per-capability decisions
CAP-53 EXPERIMENT (first persistent backend); CAP-54 EXPERIMENT (FTS engine unverified); CAP-55 REUSE reranker design, BUILD fusion in EOIP; CAP-04 INTEGRATE; CAP-46 BUILD; CAP-47 REUSE dataset-per-tenant; CAP-74 REUSE (copy dataset) with EXPERIMENT drill; CAP-35 REFERENCE versions.

## 14. Tests and acceptance
1. Conformance suite shared with other backends. 2. Selectivity sweep recall@10 vs exact with/without scalar index. 3. Delete + compact + cleanup: data bytes gone from files. 4. Concurrent writer test (two processes). 5. Cold start and RSS at 1M x 768 on 4 GB container. 6. Air-gap pip install from mirror.

## 15. Risks and open questions
Default prefilter by version; FTS engine (native vs Tantivy) unverified; Enterprise-only features; 0.x API stability; release date of 0.40.0.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Apache-2.0, beta cadence |
| D2 | 2 | embedded retrieval |
| D3 | 4 | library, no daemon |
| D4 | 5 | Lance fragments/versions |
| D5 | N/A | schema only |
| D6 | 5 | pre/post filter, rerank |
| D7 | N/A | |
| D8 | 5 | MVCC-like versions; writers UNVERIFIED |
| D9 | N/A | |
| D10 | N/A | |
| D11 | 5 | dataset versions |
| D12 | N/A | |
| D13 | 2,5 | retrieval |
| D14 | N/A | |
| D15 | N/A | |
| D16 | N/A | |
| D17 | 3 | four SDKs |
| D18 | 3,9 | no ACL |
| D19 | 5,12 | path-based |
| D20 | 7 | none verified |
| D21 | 1,10 | OSS vs Enterprise |
| D22 | N/A | open Lance format |
| D23 | N/A | |
| D24 | 15 | thin official evidence |

## Appendix B. Capability mapping
| CAP | LanceDB | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-53 | native | lancedb-04 | BL-14 partial | EXPERIMENT | P1 |
| CAP-54 | native (engine UNVERIFIED) | lancedb-05 | BL-13 | EXPERIMENT | P2 |
| CAP-55 | native | lancedb-05 | BL-15 | BUILD | P2 |
| CAP-04 | native | lancedb-01 | BL-14 | INTEGRATE | P1 |
| CAP-46 | absent | lancedb-03 | BL-18 absent | BUILD | P0 |
| CAP-47 | partial | lancedb-06 | BL-20 | REUSE | P1 |
| CAP-74 | partial | lancedb-06 | none | REUSE | P2 |

## Appendix C. Evidence
| ID | Product/date | Claim | Class | Source | Access | Conf. | Contra |
|---|---|---|---|---|---|---|---|
| CLAIM-lancedb-01 | main | Apache License 2.0; PyPI classifier Apache | Observed | github.com/lancedb/lancedb LICENSE; pypi.org/project/lancedb | 2026-10-26 | 0.9 | PyPI licence field null |
| CLAIM-lancedb-02 | releases | v0.41.0-beta.10..14 between 10-20 and 10-25 (year inferred); PyPI latest 0.40.0 | Documented | github.com/lancedb/lancedb/releases | 2026-10-26 | 0.75 | page omits year |
| CLAIM-lancedb-03 | docs | OSS embedded; Enterprise distributed, sales-led, same format | Documented | docs.lancedb.com | 2026-10-26 | 0.8 | none |
| CLAIM-lancedb-04 | docs | Pre-filter default in newer docs, older docs post-filter; BTREE/BITMAP/LABEL_LIST; nprobes advice | Documented | docs.lancedb.com/search/filtering, /performance | 2026-10-26 | 0.6 | doc versions conflict |
| CLAIM-lancedb-05 | docs | Hybrid search with RRFReranker default; requires FTS index; default limit 10 | Documented | docs.lancedb.com/search/hybrid-search | 2026-10-26 | 0.8 | none |
| CLAIM-lancedb-06 | docs | Immutable versions, checkout/restore, deletions marked, compaction disk caveat | Documented | docs.lancedb.com/tables/versioning | 2026-10-26 | 0.7 | search summary only |

## Appendix D. Assumptions
Release years inferred. Enterprise gating unknown. Tenant-per-dataset design is an EOIP inference.
