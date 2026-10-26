| Field | Value |
|---|---|
| Registry ID | T-C10-weaviate |
| Tier | B (vector DB with built-in hybrid search and shard-per-tenant tenancy) |
| Versions examined | v1.40.2 (marked latest, 2026-10-22); patch lines v1.39.13, v1.38.22, v1.37.18 (2026-10-25), v1.36.24 (2026-10-23) |
| Verified on | 2026-10-26 |
| Worker | V23 |

## 1. Identity, status, sources
Weaviate (github.com/weaviate/weaviate; Weaviate B.V.; Go). Licence: repository LICENSE says files are BSD-3-Clause except the `wl` directory, which needs a separate Weaviate (enterprise) licence [CLAIM-weaviate-01]. Active: several maintained minor lines receive patch releases in the same week, so cadence is high and the support window is long [CLAIM-weaviate-02]. Managed: Weaviate Cloud. Sources: LICENSE, releases, tenancy, filtering, hybrid, backup, RBAC, vector-index docs (8).

## 2. Problem and workloads
Object store plus vector index plus BM25 in one engine. EOIP workflow: class per source/tenant; tenant = shard; objects carry `acl_principals`, `revision`; hybrid query with filter on ACL; return IDs to graph for ACL re-check.

## 3. Feature inventory
| Feature | Status |
|---|---|
| HNSW (default), flat, dynamic (experimental), HFresh cluster index | present [CLAIM-weaviate-06] |
| Compression RQ (HFresh), PQ/BQ/SQ | present (PQ/BQ/SQ detail UNVERIFIED) |
| Hybrid: BM25 + vector, `relativeScoreFusion` (default since 1.24), `rankedFusion`, `alpha` | present [CLAIM-weaviate-04] |
| Filter strategies ACORN (default since 1.34), sweeping, PathSeer (1.40); flat-search cutoff ~15% | present [CLAIM-weaviate-03] |
| Multi-tenancy: tenant = shard; states ACTIVE/INACTIVE/OFFLOADED(S3) | present [CLAIM-weaviate-05] |
| RBAC by collection and tenant; roles root/viewer; API key + OIDC | present; no per-object ACL [CLAIM-weaviate-07] |
| Backups: S3/GCS/Azure/filesystem; incremental since 1.37 | present [CLAIM-weaviate-08] |
| Enterprise-only (`wl` dir) features | exist; contents NOT PUBLICLY VERIFIED |

## 4. Architecture
```
client (gRPC/GraphQL/REST) -> node -> collection -> shard (one per tenant if MT)
  shard: LSM object store + inverted index (BM25) + vector index (HNSW | flat | HFresh)
  async-indexing queue (on disk) -> vector index | tombstone cleanup (async)
  cluster: Raft for schema, replicas per shard; backup module -> S3/GCS/Azure/fs; offload -> S3
```

## 5. Under-the-hood reconstruction
- **Filtering:** inverted index builds an allow-list of IDs; HNSW traverses the full graph but only admits allowed IDs (ACORN: multi-hop neighbour checks plus extra filtered entry points). If the filter is very selective (cutoff ~15% of objects, configurable) it switches to brute-force over the matching set [CLAIM-weaviate-03]. Vendor states filtered recall is typically no worse than unfiltered (vendor claim, vendor test, k = 10/15/20).
- **Hybrid:** BM25 and vector searches run in parallel; relativeScoreFusion min-max normalises each list to [0,1] then sums with alpha (server default 0.75; clients may leave it unset) [CLAIM-weaviate-04].
- **Deletes/updates:** HNSW delete marks a tombstone; node remains connected until async cleanup reassigns edges [CLAIM-weaviate-06]. Async indexing means a new object may not yet appear in vector search [CLAIM-weaviate-06].
- **Tenancy:** each tenant has a dedicated vector index and shard; tenant delete drops the shard; adding nodes does not rebalance existing tenants; ~170k active tenants tested on 9 nodes, limited by open-file limit [CLAIM-weaviate-05].
- **Security:** permissions filter on collection name and tenant name; not per object; a permission set false means "not set", so any role granting access still applies [CLAIM-weaviate-07].

## 6. Inferred requirements
FR: ACL as a filter property on every object; ACL change = object update; tombstone-aware delete verification. NFR: per-tenant index for strong isolation; bounded memory via flat/HFresh for small tenants.

## 7. Performance and resource model
HNSW is fully in memory: docs estimate about 2-12 GB per 1M vectors for nodes plus ~200 MB per 1M for edges (vendor estimate, dimension-dependent) [CLAIM-weaviate-06]. Flat is disk-backed and suits small per-tenant sets. No benchmark run. Failure modes: eventual consistency of tenant state changes; async index lag; cache dropped wholesale when full; downgrade below 1.40 needs filter strategy switch.

## 8. Strengths
Shard-per-tenant isolation; strong filtered-ANN strategy menu; built-in BM25 and fusion; BSD-3 core. Match: tenant-scoped index family in EOIP (already tenant-partitioned in `hybrid_vector_service.py`); exceed: ACL re-check against graph.

## 9. Limitations
| Class | Item |
|---|---|
| Operational | HNSW memory; per-tenant file handles cap active tenants [weaviate-05] |
| Friction | restore fails if collection exists; same node count/names required; tenants not a restore unit; RBAC not restored by default [weaviate-08] |
| Algorithmic | no per-object ACL; fusion needs alpha tuning |
| Licensing | split BSD-3 plus `wl` enterprise code [weaviate-01]; legal review trigger |

## 10. Deployment and licensing
Single binary or container, air-gap viable; module system can call external vectorisers (must be disabled under egress policy). Redistribution: BSD-3 core fine, `wl` files require separate licence; verify no EOIP-needed feature lives there. Legal-review trigger: community/enterprise split.

## 11. Competitive delta vs baseline
BL-14 partial/in-process: Weaviate adds persistent filtered ANN. BL-15: server-side fusion. BL-18 absent in `retrieval/service.py`; `retrieval/hybrid_vector_service.py` (new) filters `acl_allow_roles` in-memory with brute-force cosine and no external backend: Weaviate offers a persistent filter-based path, not ACL semantics. BL-20 partial: shard-per-tenant stronger than EOIP contract. BL-25: tombstones align with EOIP tombstones.

## 12. Cards
| ID | Card |
|---|---|
| STR-weaviate-01 | Shard-per-tenant with dedicated index and ACTIVE/INACTIVE/OFFLOADED lifecycle [weaviate-05]. Value: cheap cold tenants. Match in EOIP index lifecycle (unload idle tenants). Test: 10k tenants, 1% active, RSS bounded. |
| STR-weaviate-02 | Selectable filter strategy plus flat-cutoff [weaviate-03]. Exceed: EOIP planner picks exact scan vs graph by ACL selectivity. Test: recall@10 at 0.1%/1%/10% selectivity. |
| INV-weaviate-01 | v1.40.2. Limitation: tenant not a restore unit; whole-collection restore only [weaviate-08]. Root cause storage coupling (proven). Options: (a) collection per tenant; (b) rebuild per-tenant index from graph; (c) per-tenant snapshot manifests. Select (b): vector index is derived. POC: rebuild one tenant from 100k chunks, time vs restore. Decision ADOPT as design rule. |
| INV-weaviate-02 | Split licence [weaviate-01]. Mitigation: depend only on BSD-3 paths behind `VectorIndexPort`. Decision ADOPT. |
Seed hypotheses: none targeting Weaviate.

## 13. Per-capability decisions
CAP-53 INTEGRATE (optional adapter, P2); CAP-55 REFERENCE fusion normalisation, BUILD RRF + normalised-score option; CAP-47 REUSE pattern; CAP-46 BUILD; CAP-74 REJECT dependence (rebuild from graph); CAP-77 licence gate DEFER until `wl` contents are mapped.

## 14. Tests and acceptance
1. Adapter conformance: cross-tenant query returns nothing, ACL-filtered query never returns a document outside caller principals. 2. Filtered recall vs exact at several selectivities. 3. Delete visibility: after tombstone, absent from hybrid results in <= SLA incl. async queue lag. 4. Memory at 1M x 768 with and without RQ. 5. Restore drill. 6. Scan `wl` imports in any redistributed build.

## 15. Risks and open questions
Contents of `wl`; PQ/BQ/SQ parameters; whether async-indexing lag breaks "delete means gone"; GraphQL deprecation status (not examined).

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | BSD-3 + wl split, active |
| D2 | 2 | object+vector+BM25 |
| D3 | 4 | shard, LSM, HNSW |
| D4 | 5,7 | HNSW/flat/HFresh |
| D5 | N/A | no ontology; schema classes only |
| D6 | 5 | filter strategies, fusion |
| D7 | N/A | |
| D8 | 4,5 | Raft schema, replicas; tenant state eventual |
| D9 | N/A | not examined |
| D10 | 11 | no evidence spans |
| D11 | N/A | |
| D12 | N/A | |
| D13 | 2,5 | retrieval engine |
| D14 | N/A | |
| D15 | N/A | |
| D16 | N/A | |
| D17 | 3 | clients not examined |
| D18 | 5 | RBAC, OIDC |
| D19 | 5 | shard per tenant |
| D20 | 7 | vendor memory estimate |
| D21 | 1,10 | BSD-3 + enterprise |
| D22 | N/A | |
| D23 | N/A | |
| D24 | 15 | vendor docs only |

## Appendix B. Capability mapping
| CAP | Weaviate | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-53 | native | weaviate-03 | BL-14 partial | INTEGRATE | P2 |
| CAP-54 | native BM25 | weaviate-04 | BL-13 | REFERENCE | P3 |
| CAP-55 | native | weaviate-04 | BL-15 | BUILD | P2 |
| CAP-46 | absent per-object | weaviate-07 | BL-18 absent | BUILD | P0 |
| CAP-47 | native | weaviate-05 | BL-20 partial | REUSE pattern | P1 |
| CAP-74 | native | weaviate-08 | none | REJECT reliance | P3 |
| CAP-77 | split | weaviate-01 | BL-22 | DEFER | P2 |

## Appendix C. Evidence
| ID | Product/date | Claim | Class | Source | Access | Conf. | Contra |
|---|---|---|---|---|---|---|---|
| CLAIM-weaviate-01 | main | BSD-3-Clause except `wl` directory needing separate licence | Observed | raw.githubusercontent.com/weaviate/weaviate/main/LICENSE | 2026-10-26 | 0.9 | none |
| CLAIM-weaviate-02 | v1.40.2 | v1.40.2 latest 10-22; v1.37.18 10-25; v1.36.24 10-23 (years inferred from page) | Documented | github.com/weaviate/weaviate/releases | 2026-10-26 | 0.75 | page omits years |
| CLAIM-weaviate-03 | 1.40 | ACORN default since 1.34; PathSeer 1.40; flat cutoff ~15% | Documented | docs.weaviate.io/weaviate/concepts/filtering | 2026-10-26 | 0.85 | vendor-run recall tests |
| CLAIM-weaviate-04 | docs | relativeScoreFusion default since 1.24; rankedFusion; alpha default 0.75 | Documented | docs.weaviate.io/weaviate/concepts/search/hybrid-search | 2026-10-26 | 0.85 | none |
| CLAIM-weaviate-05 | docs | Tenant=shard, states, ~170k tenants on 9 nodes, no rebalance | Documented | docs.weaviate.io/weaviate/concepts/data | 2026-10-26 | 0.85 | none |
| CLAIM-weaviate-06 | docs | HNSW memory estimate, tombstones, async indexing persistent queue since 1.28, dynamic/HFresh | Documented | docs.weaviate.io/weaviate/concepts/vector-index | 2026-10-26 | 0.8 | none |
| CLAIM-weaviate-07 | docs | RBAC by collection/tenant, no per-object ACL, OIDC groups | Documented | docs.weaviate.io/weaviate/configuration/rbac | 2026-10-26 | 0.8 | absence of mention |
| CLAIM-weaviate-08 | docs | Backups to S3/GCS/Azure/fs; incremental 1.37; restore constraints | Documented | docs.weaviate.io/deploy/configuration/backups | 2026-10-26 | 0.85 | none |

## Appendix D. Assumptions
Release years inferred from 2026 context. `wl` assumed to hold enterprise features.
