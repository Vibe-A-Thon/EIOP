# C02 QLever

| Field | Value |
|---|---|
| Registry ID | T-C02-qlever |
| Tier | B (high-performance SPARQL engine for very large KGs; promoted by the Wikidata decision) |
| Versions examined | v0.6.0 (marked Latest on GitHub, "13 Aug", year not shown, 2026 inferred); v0.5.50 (17 Jul); master pre-release dated 2026-10-25 |
| Verified on | 2026-10-26 (brief 2026-10-18) |
| Worker | V16 (registry W09) |

## 1. Identity, status, sources
Open-source C++ SPARQL engine from the University of Freiburg (Chair for Algorithms and Data Structures; Hannah Bast, Johannes Kalmbach et al.), first described in a 2017 paper [CLAIM-qlever-02]. Licence: Apache-2.0 per README and Wikipedia; a third-party catalogue says MIT, which conflicts and is treated as wrong pending LICENSE-file check [CLAIM-qlever-01,02]. Status: very active (about monthly releases, 3,340 commits, 203 open issues on the page read) [CLAIM-qlever-01]. Adoption: public instances for Wikidata, OSM, UniProt (UniProt endpoint moved from Virtuoso in 2025), DBLP [CLAIM-qlever-02]. In 2026 the Wikimedia Wikidata Platform team decided to replace Blazegraph with QLever [CLAIM-qlever-03]. Cross-ref: `C02-tier-c-records-V16.md` (Blazegraph), `C02-openlink-virtuoso.md`.

## 2. Problem and workloads
Read-heavy SPARQL over very large static or slowly changing graphs on one commodity server: Wikidata (17B triples) and UniProt (94B) are cited by the project [CLAIM-qlever-04]; geospatial (OSM), full-text-in-SPARQL, autocompletion UI. Workflows: build index from dump (`qlever` CLI + Qleverfile), serve, optionally SPARQL Update.

## 3. Feature inventory
| Feature | Status | CLAIM |
|---|---|---|
| SPARQL 1.1 full compliance incl. Update + Graph Store Protocol (reported reached June 2025) | present | 01,02 |
| Update persistence flag, access token for updates | present | 05 |
| Text search in SPARQL | present | 01 |
| GeoSPARQL / spatial joins | present (extent not verified) | 01,04 |
| Materialized views, named subqueries, path search | present | 04 |
| Embedded C++ library, WASM (QLever.js) | present | 01 |
| Native packages Debian/Ubuntu/macOS, containers | present | 01 |
| RDF 1.2 / SPARQL 1.2, RDF-star | not found | UNKNOWN |
| OWL/RDFS reasoning, SHACL, vector search, multi-tenancy, RBAC, clustering | absent / not found | none |
| Blazegraph-specific services (e.g. label/mwapi) | absent (migration cost) | 03 |

## 4. Architecture
```
 qlever CLI + Qleverfile  --index build-->  on-disk index (sorted permutations, vocabulary)  [details: hypothesis]
 HTTP server: SPARQL query | Update (token) | Graph Store | UI (autocomplete)
   parser -> optimizer (cost model) -> operators (joins, text, spatial) -> cache -> result streaming
   delta layer for updates (hypothesis), optional persistence
```

## 5. Reconstruction
Verified: single-machine design for hundreds of billions to >1T triples [CLAIM-qlever-01,02]; a 2025 extension encodes common identifiers directly in numeric IDs to avoid string lookups, including at export [CLAIM-qlever-02]; update requires an access token and optional persistence [CLAIM-qlever-05]. Everything else is *reasoned inference* from the literature (not read in this run): index = several sorted triple permutations stored as compressed blocks, a vocabulary mapping strings to IDs, joins as merge/hash over sorted streams, query result caching. Delta-triples and consolidation semantics for Update are NOT PUBLICLY VERIFIED in what was read; transaction isolation unknown. Source code not opened; recommended for a Tier A style follow-up (C++ repo at a pinned tag).

## 6. Requirements inferred
Index build is an offline step (hours at scale; UNVERIFIED), memory/disk planning; updates need token control; Wikidata needs real-time index updates (hard requirement of the Wikimedia evaluation) [CLAIM-qlever-03]. EOIP implication: QLever suits an analytical read replica of RDF data, not the system of record for permissioned, tenant-isolated writes.

## 7. Performance and resource model
All numbers are claims: "hundreds of billions" on a commodity PC/server; "more than a trillion triples" demo; outperforms others "by a large margin on most queries" (README, evaluation linked, not reproduced) [CLAIM-qlever-01]; 1.4B OSM geometries spatial relations in under 3 h vs PostGIS (2025 paper, per Wikipedia) [CLAIM-qlever-02]; a 2023 evaluation found it very fast on successful queries but limited on complex constructs (Wikipedia citing it; since then SPARQL 1.1 compliance reported) [CLAIM-qlever-02]. Wikimedia reports decision based on AWS and on-prem tests, benchmarks and production replay (details on wiki, not reproduced) [CLAIM-qlever-03]. Failure modes: Blazegraph-only functions, update/consolidation cost (unknown), memory pressure.

## 8. Strengths
Scale on one node; permissive licence; strong public adoption (Wikidata, UniProt); SPARQL+text+geo in one engine; embeddable; fast release cadence. Exceed: wrap with tenant/ACL/lineage which QLever lacks.

## 9. Limitations
Algorithmic/semantic: no reasoning, SHACL or RDF-star found. Operational: offline index builds; update model less mature than a transactional store (hypothesis). Friction: "wiki potentially outdated" per README; docs landing pages thin on internals. Security: only an update access token documented [CLAIM-qlever-05]; no read ACLs found. Outdated/contradictory: licence listed as MIT by one catalogue.

## 10. Deployment, licensing
Self-hosted binary, Docker/Podman, Debian/Ubuntu/macOS packages [CLAIM-qlever-01]; air-gap yes after install. Apache-2.0: permissive with patent grant; no legal flag. Hardware sizing unverified.

## 11. Delta vs baseline
BL-06: only Fuseki/GraphDB adapters; a QLever adapter would be read-optimised only; BL-01 protocol assumes CRUD+tombstone, matching only the Update path; BL-18/BL-20: QLever gives no per-fact ACL or tenant isolation, so EOIP must filter before and after.

## 12. Cards
STR-qlever-01 | QLever | single-node trillion-triple SPARQL with text and spatial | 01,02,03 | one-node-first big-graph analytics tier | integrate | optional read replica fed from the EOIP graph/event log; queries pass through EOIP policy rewriter | test: build index from 100M-triple export, run 20-query corpus, compare result sets with Fuseki/rdflib, record p50/p95 and RAM.
STR-qlever-02 | QLever | public-scale adoption (Wikidata migration) | 03 | de-risks SPARQL-engine bet | reference | track migration outcome | test: re-read Wikimedia status Q1 2027.
INV-qlever-01 | QLever v0.6.0 | no read ACLs/tenancy; update model for volatile data unverified | root cause: semantics/governance (proven absence in docs read) | alternative: EOIP policy layer in front; worse when each tenant needs separate indexes (many small indexes) | options: (a) per-tenant index (b) shared index + query rewrite to allowed graphs (c) own store | select (b) EXPERIMENT with (a) fallback | POC: adversarial SPARQL (`GRAPH ?g`, property paths, SERVICE) against rewriter; success: zero cross-tenant rows | defensibility: policy proof | decision EXPERIMENT.

## 13. Capability decisions
CAP-02/05 very large RDF read tier: EXPERIMENT (INTEGRATE optional). CAP-54 text in SPARQL: REFERENCE. CAP-19 path search: REFERENCE. CAP-06 bulk index build: REFERENCE. CAP-20 query translation to SPARQL 1.1 only: REUSE (subset target for EOIP portability). Embedded C++: REJECT for Python core.

## 14. Tests
PROPOSED: SPARQL 1.1 compliance run; RDF 1.2 probe; update/delete + restart persistence test; cross-tenant leak test; 100M and 1B triple build time/RAM on stated hardware; compare against Oxigraph and Fuseki.

## 15. Risks, questions
Licence-file confirmation; version dates; Update consolidation behaviour; Wikimedia end-state (endpoints due by 2026-11-01; Blazegraph degradation from Feb 2027; shutdown targeted 2027-06-30) [CLAIM-qlever-03]; RDF 1.2 plans.

## Appendix A. Dimensions
| Dim | Sec | Summary |
|---|---|---|
| D1 | 1 | Freiburg, Apache-2.0, active |
| D2 | 2 | big read-heavy KGs |
| D3 | 4 | CLI + server |
| D4 | 5 | permutations (inference) |
| D5 | 3 | no reasoning/SHACL |
| D6 | 5 | cost-based; text, spatial |
| D7 | N/A | none |
| D8 | 5,7 | single node; update details unknown |
| D9 | 3 | federation per SPARQL 1.1 |
| D10-D12 | N/A | none |
| D13 | 3 | text search; no vector |
| D14 | N/A | UI autocomplete only |
| D15 | N/A | none |
| D16 | 3 | UI, autocomplete |
| D17 | 3 | CLI, C++ API, JS |
| D18 | 9 | token only |
| D19 | N/A | none |
| D20 | 7 | claims only |
| D21 | 10 | permissive |
| D22 | 11 | SPARQL 1.1 standards |
| D23 | N/A | not reviewed |
| D24 | App C | docs+secondary |

## Appendix B. CAP mapping
| CAP | QLever | CLAIM | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-02 | native | 01 | BL-06 | EXPERIMENT | P2 |
| CAP-05 | single-node scale-up | 01,02 | BL-01 | REFERENCE | P3 |
| CAP-06 | native index build | 01 | BL-06 | REFERENCE | P3 |
| CAP-15 | native | 01 | BL-06 | INTEGRATE | P2 |
| CAP-19 | partial (path search) | 04 | BL-43 | REFERENCE | P3 |
| CAP-54 | native in SPARQL | 01 | BL-13 | REFERENCE | P3 |
| CAP-47 | absent | 05 | BL-20 | BUILD | P0 |

## Appendix C. Evidence
| CLAIM | version/date | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| qlever-01 | README | Apache 2.0; full SPARQL 1.1; text, spatial, materialised views; hundreds of billions/>1T triples; packages | Officially documented (vendor-style claim for scale) | https://github.com/ad-freiburg/qlever | 2026-10-26 | 0.75 | scale/benchmark claims unreproduced |
| qlever-02 | encyclopedia | Freiburg history; SPARQL 1.1 compliance June 2025; users; 2025 ID-encoding extension; UniProt switch; Wikimedia 2026 choice; licence Apache | Third-party report | https://en.wikipedia.org/wiki/QLever | 2026-10-26 | 0.55 | DBDB lists MIT (https://dbdb.io/db/qlever) |
| qlever-03 | Wikidata proposal + newsletter | QLever replaces Blazegraph for WDQS; endpoints 2026-11-01; degradation Feb 2027; shutdown 2027-06-30; Blazegraph services unsupported | Third-party report (operator pages) | https://www.wikidata.org/wiki/Wikidata:Wikidata_Platform_team/Newsletter_June_2026 ; https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/WDQS_backend_update/Backend_Replacement | 2026-06 / 2026-10-26 | 0.7 | Newsletter says Blazegraph decommission 2027-06-30; hub says Feb 2027 degradation |
| qlever-04 | docs | Wikidata 17B, UniProt 94B triples cited; reference pages for GeoSPARQL, update, materialised views, text search, path search | Officially documented | https://docs.qlever.dev/ ; https://github.com/ad-freiburg/qlever/wiki | 2026-10-26 | 0.7 | none |
| qlever-05 | docs | updates need access token; persistence flag; Graph Store `TSOP` extension | Officially documented | https://docs.qlever.dev/update/ | 2026-10-26 | 0.8 | none |

## Appendix D. Assumptions
Release years inferred. Internal index design is inference, not read from papers or code.
