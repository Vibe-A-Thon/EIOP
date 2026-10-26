| Field | Value |
|---|---|
| Registry ID | T-C10-elasticsearch |
| Tier | B (search reference; licence verification is the main finding; OpenSearch is the Tier A comparator) |
| Versions examined | 9.5.5, 9.4.8, 8.19.23 (all 2026-10-06); 8.19.22 (2026-09-23) |
| Verified on | 2026-10-26 |
| Worker | V23 |

## 1. Identity, status, sources
Elasticsearch (github.com/elastic/elasticsearch; Elastic N.V.; Java, Lucene-based). Active; patch releases across 9.5, 9.4 and 8.19 lines on the same day [CLAIM-elasticsearch-01]. **Licence (verified from repo LICENSE.txt):** source is by default offered under a choice of AGPL v3.0-only, SSPL v1 and Elastic License 2.0; some files carry Apache-2.0-compatible headers; code in `x-pack` is ELv2-only [CLAIM-elasticsearch-02]. AGPL was added as a third option in 2024 ahead of 8.16; Elastic states existing users are unaffected, binary distributions unchanged, clients Apache-2.0 [CLAIM-elasticsearch-03]. Sources (7): releases, LICENSE.txt, licensing news, subscriptions page, DLS, retrievers, snapshot docs.

## 2. Problem and workloads
Distributed full-text, kNN vector, hybrid and analytics. EOIP use: reference for DLS-style security and hybrid retrievers; candidate adapter where an enterprise customer already runs it. Workflow: index per tenant or shared index with `tenant_id`; role-query DLS from user metadata; `knn` + `match` combined via `rrf` retriever; IDs back to graph.

## 3. Feature inventory
| Feature | Status |
|---|---|
| BM25, kNN (approximate and exact), `dense_vector`, query vector builders | present [CLAIM-elasticsearch-05] |
| Retrievers: standard, knn, rrf, linear, text_similarity_reranker | present; `rrf` licence tier per third party: Enterprise [CLAIM-elasticsearch-06] |
| Document- and field-level security with templated role queries from `_user` | present, paid tier (Platinum or Enterprise per third party; official page silent) [CLAIM-elasticsearch-04] |
| Snapshot/restore: incremental, segment-deduplicated, index/data-stream/feature-state/cluster scope | present [CLAIM-elasticsearch-07] |
| Searchable snapshots, cross-cluster replication | paid (subscriptions listing; tier mapping unreadable in fetch) |
| Quantisation int8/int4/BBQ, filter inside kNN | UNVERIFIED this pass (docs pages not retrieved) |
| Free "Basic" tier | exists; Platinum closed to new customers [CLAIM-elasticsearch-08] |

## 4. Architecture
```
client (REST) -> coordinating node -> shards (primary+replica) on data nodes; master nodes hold cluster state
  shard = Lucene index: segments (inverted index, doc values, HNSW per segment) + translog
  security layer (x-pack): authN realms -> roles -> index privileges (+ DLS role query, FLS)
  snapshot repository (off-cluster) <- incremental segment copy
```

## 5. Under-the-hood reconstruction
- **Storage:** immutable Lucene segments merged in background; deletes are bitsets until merge, so erasure is deferred to segment merge (general Lucene behaviour, 0.8).
- **DLS:** role `query` (Query DSL, templated with `{{_user.metadata...}}`) is injected as a filter on every search; multiple roles OR together; omitting `query` disables DLS for that entry [CLAIM-elasticsearch-04]. Caveats: scoring ignores the role query; request cache disabled for stored-script templates; terms enum returns nothing; aggregations may still leak counts and field names; unsupported queries include `has_child`, `percolate`, remote-lookup terms; DLS does not apply to writes, so ownership must be stamped at ingest (set-security-user processor) [CLAIM-elasticsearch-04].
- **Hybrid:** `rrf` retriever fuses ranked lists; `linear` retriever combines scores, normaliser matters or lexical dominates; multi-field format GA since 9.1 [CLAIM-elasticsearch-06].
- **Tenant models:** index per tenant, filtered aliases, or shared index plus DLS (patterns known; tenant-count limits UNVERIFIED here).
- **Snapshots:** immutable segments mean only new segments copied; restore at index granularity, not tenant granularity unless one index per tenant [CLAIM-elasticsearch-07].

## 6. Inferred requirements
FR: ACL expressed as a filter field, enforced server-side by role query; user-metadata templating; stamp owner/ACL at ingest. NFR: JVM heap sizing; at least one master-eligible plus data node; snapshot repository on local/NFS storage in air gap.

## 7. Performance and resource model
No benchmark run. JVM node with heap plus OS cache; single-node possible but heavier than Qdrant/LanceDB (general knowledge, 0.7, not quantified here). Failure modes: DLS cost on large role queries, deferred physical delete, split-brain avoided by master election (not examined).

## 8. Strengths
Mature DLS/FLS model; deep text analysis; rich retriever composition; snapshots. Match: express EOIP principal filter as a templated role query analogue; exceed: ACL derived from source ACL hash with revocation epoch (already in `hybrid_vector_service.py`).

## 9. Limitations
| Class | Item |
|---|---|
| Licensing | triple/ELv2 licence; x-pack ELv2-only; DLS and RRF paid [CLAIM-elasticsearch-02,04,06]; legal-review trigger |
| Operational | JVM footprint, multi-node defaults |
| Semantic | aggregation and terms leaks under DLS; scoring ignores role query [elasticsearch-04] |
| Friction | licence tier mapping not readable on subscriptions page extraction |

## 10. Deployment and licensing
Self-managed, container, air-gap viable. **Redistribution:** AGPL-3.0 (network copyleft) option, SSPL v1 (source-available; SaaS clause) and ELv2 (no managed-service offering, no circumvention of licence-key features, no removal of notices) are all legal-review triggers for bundling or reselling inside a white-label product; clients are Apache-2.0. Recommendation: do not bundle; support as a customer-operated adapter; OpenSearch (Apache-2.0, see C10-opensearch.md) is the redistributable alternative. Not a legal conclusion.

## 11. Competitive delta vs baseline
BL-13/14/15: Elasticsearch gives persistent BM25 + ANN + retrievers. BL-18 absent: DLS is the closest server-enforced model but paid. `retrieval/hybrid_vector_service.py` (new) enforces role ACL in-memory (pre-filter and final delivery check, policy-epoch cache revocation); no external backend. BL-20: index-per-tenant plausible. BL-22 offline licensing is unrelated. Cross-reference C10-opensearch.md (DLS in Apache-2.0) and C10-qdrant.md.

## 12. Cards
| ID | Card |
|---|---|
| STR-elasticsearch-01 | Server-side DLS via templated role queries [elasticsearch-04]. Value: ACL enforced in the engine, not callers. Match: EOIP adapter attaches principal filter server-side where backend supports it; otherwise two-stage check. Test: forged filter from caller cannot widen results. |
| STR-elasticsearch-02 | Composable retrievers (rrf/linear/rerank) [elasticsearch-06]. Match with pluggable fusion in EOIP. |
| INV-elasticsearch-01 | 9.5.5. Limitation: licence choice and paid DLS/RRF block redistribution [elasticsearch-02,04,06]. Root cause licensing (proven). Options: (a) customer-supplied adapter; (b) OpenSearch adapter; (c) native ACL-aware index. Select (a)+(b). POC: same conformance suite against both. Decision ADOPT. |
| INV-elasticsearch-02 | DLS leaks via aggregations/terms [elasticsearch-04]. EOIP retrieval API exposes no aggregations on protected fields. Decision ADOPT. |
Seed hypotheses: none targeting Elasticsearch.

## 13. Per-capability decisions
CAP-54 REFERENCE (BM25 via own index; INTEGRATE as customer adapter); CAP-53 INTEGRATE adapter only; CAP-55 REFERENCE retriever composition; CAP-46 BUILD, REFERENCE DLS pattern; CAP-77 REJECT bundling; CAP-74 REFERENCE.

## 14. Tests and acceptance
1. Same adapter conformance suite as other backends. 2. DLS leak probe: aggregations, terms enum, suggesters. 3. Delete visibility and physical deletion after merge. 4. Licence scan of any shipped artefact. 5. Single-node RSS at idle and 1M x 768.

## 15. Risks and open questions
Tier of DLS/RRF (official page unreadable); kNN filter semantics and quantisation unverified; whether AGPL option applies to x-pack paid features (ELv2-only per file); legal review needed.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | triple licence, active |
| D2 | 2 | search + vectors |
| D3 | 4 | shards, Lucene, security layer |
| D4 | 5 | segments |
| D5 | N/A | mappings only |
| D6 | 5 | retrievers |
| D7 | N/A | |
| D8 | 5 | snapshots; consensus not examined |
| D9 | N/A | |
| D10 | N/A | |
| D11 | N/A | |
| D12 | N/A | |
| D13 | 2,5 | hybrid retrieval |
| D14 | N/A | |
| D15 | N/A | |
| D16 | N/A | Kibana not examined |
| D17 | N/A | |
| D18 | 5 | DLS/FLS, caveats |
| D19 | 5 | index/alias/DLS |
| D20 | 7 | none verified |
| D21 | 1,10 | tiers, licences |
| D22 | N/A | |
| D23 | N/A | |
| D24 | 15 | official docs + two third-party |

## Appendix B. Capability mapping
| CAP | Elasticsearch | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-54 | native | elasticsearch-05 | BL-13 | INTEGRATE adapter | P3 |
| CAP-53 | native | elasticsearch-05 | BL-14 | INTEGRATE adapter | P3 |
| CAP-55 | native (paid rrf) | elasticsearch-06 | BL-15 | REFERENCE | P3 |
| CAP-46 | enterprise-only (DLS) | elasticsearch-04 | BL-18 absent | BUILD | P0 |
| CAP-77 | n/a | elasticsearch-02 | BL-22 | REJECT bundling | P1 |
| CAP-74 | native | elasticsearch-07 | none | REFERENCE | P3 |

## Appendix C. Evidence
| ID | Product/date | Claim | Class | Source | Access | Conf. | Contra |
|---|---|---|---|---|---|---|---|
| CLAIM-elasticsearch-01 | releases | 9.5.5, 9.4.8, 8.19.23 on 10-06; 8.19.22 on 09-23 (year inferred) | Documented | github.com/elastic/elasticsearch/releases | 2026-10-26 | 0.75 | page omits year |
| CLAIM-elasticsearch-02 | main | LICENSE.txt: default triple choice AGPLv3-only / SSPL v1 / ELv2; Apache-compatible headers; x-pack ELv2-only | Observed | raw.githubusercontent.com/elastic/elasticsearch/main/LICENSE.txt | 2026-10-26 | 0.9 | none |
| CLAIM-elasticsearch-03 | 2024 | AGPL added as option before 8.16; existing users unaffected; clients Apache-2.0 | Third-party/vendor | elastic.co licensing FAQ; Elastic DevRel newsletter (Sep 2024) via search | 2026-10-26 | 0.8 | none |
| CLAIM-elasticsearch-04 | docs current | DLS role queries, templating, caveats; subscription not stated; Platinum/Enterprise per third party | Documented / third-party | elastic.co/docs ... controlling-access-at-document-field-level; elastic.sios.jp | 2026-10-26 | 0.8 / 0.5 | official silent on tier |
| CLAIM-elasticsearch-05 | docs | kNN exact/approximate, query vector builders | Documented | elastic.co/docs/solutions/search/vector/knn | 2026-10-26 | 0.7 | filter semantics not retrieved |
| CLAIM-elasticsearch-06 | docs | rrf, linear, knn, text_similarity_reranker retrievers; multi-field GA 9.1; rrf gated to Enterprise (third party) | Documented / third-party | elastic.co/docs retrievers; dev.to/u11d RRF article | 2026-10-26 | 0.8 / 0.5 | tier unverified officially |
| CLAIM-elasticsearch-07 | docs | Incremental segment-based snapshots; index/feature/cluster scope | Documented | elastic.co/docs ... snapshot-and-restore | 2026-10-26 | 0.8 | none |
| CLAIM-elasticsearch-08 | 2026-08 | Subscriptions page: Free/Basic, Platinum (not new customers), Enterprise; DLS/FLS listed under security | Documented | elastic.co/subscriptions | 2026-10-26 | 0.6 | check marks lost in extraction |

## Appendix D. Assumptions
Year 2026 for release dates. Tier of DLS and rrf taken as paid on third-party evidence pending legal/commercial confirmation.
