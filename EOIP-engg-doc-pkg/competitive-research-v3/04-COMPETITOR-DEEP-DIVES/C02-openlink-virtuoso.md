# C02 OpenLink Virtuoso

| Field | Value |
|---|---|
| Registry ID | T-C02-openlink-virtuoso |
| Tier | B (long-lived RDF/SQL hybrid; scale reference) |
| Versions examined | Virtuoso Open Source (VOS) 7.2.17 (release notes posted 2026-05-07); VOS 7.2.16/16.1 (earlier); Commercial Edition 8.x (older announcement, current number UNVERIFIED) |
| Verified on | 2026-10-26 (brief 2026-10-18; actual access date recorded) |
| Worker | V16 (registry W09) |

## 1. Identity, status, sources
OpenLink Software's multi-model server: relational, RDF graph, documents, HTTP application server, ODBC/JDBC middleware [CLAIM-openlink-virtuoso-02,03]. Open-source 7.2.17 is a maintenance release (stability; HTTP/DAV/SOAP fixes; new `wikibase:mwapi` SERVICE handler; SPARQL optimiser and RDF Views fixes) [CLAIM-openlink-virtuoso-01]. Editions: GPL open source and a commercial edition [CLAIM-openlink-virtuoso-02]. Status: active, slow cadence (about 2 to 3 maintenance releases a year, release years per GitHub page not shown; 7.2.17 date from community post). Cross-reference: `C02-ontotext-graphdb.md`, `C02-apache-jena.md`.

## 2. Problem and workloads
Linked Data publishing (DBpedia-style endpoints), RDF Views over SQL, mixed SQL+SPARQL, large public endpoints. The Wikidata backend evaluation named Virtuoso as the other open-source candidate able to load 20B triples with real-time index updates, but flagged heavier operations, tuning complexity and the open/commercial feature gap [CLAIM-openlink-virtuoso-04]. 7.2.17 adding a Wikibase MWAPI service handler suggests Wikidata-alignment work (inference only).

## 3. Feature inventory
| Feature | Open source | Commercial | CLAIM |
|---|---|---|---|
| SPARQL, parallel SQL, GraphQL endpoint | present | present | 02 |
| RDF Views over native SQL | present | present | 02 |
| RDF Views over external sources | absent | present | 02 |
| HA cluster via replication | absent | present | 02 |
| Custom inference rules | absent | present | 02 |
| ABAC, encryption at rest | absent | present | 02 |
| Elastic Cluster Edition | n/a | present (details UNVERIFIED) | 02 |
| GeoSPARQL integration | optional | optional | 03 |
| Jena / RDF4J JDBC providers | present | present | 03 |
| RDF 1.2 / SPARQL 1.2 | not found | not found | UNKNOWN |
| SHACL | not found in sources read | UNKNOWN | |

## 4. Architecture
```
 clients: SPARQL/HTTP, ODBC/JDBC, GraphQL, WebDAV, Jena/RDF4J providers
            |
   Virtuoso server process (single engine)
     SQL compiler/executor  <-- SPARQL-to-SQL translation (hypothesis from the "RDF Views" design)
     quad store (RDF_QUAD table in the relational engine; hypothesis, NOT verified here)
     HTTP/DAV/SOAP server, RDF Views mapper, inference (rule sets)
   [commercial: replication cluster, Elastic Cluster]
```

## 5. Reconstruction
Official sources establish only the multi-model positioning and edition split [CLAIM-openlink-virtuoso-02,03]. Widely described design (UNVERIFIED in this run; public papers/docs not fetched): quads stored in relational tables with column-wise compression, SPARQL compiled to SQL and run by the same executor, sameAs/subclass inference applied via rule sets at query time. Treat all of this as hypothesis. Concurrency, ACID level, vector/text indexes: UNKNOWN. Source tree is public (GPL repo, develop/7 branch, ~15.9k commits) so Tier A-grade code inspection is possible later [CLAIM-openlink-virtuoso-03].

## 6. Requirements inferred
FR: SPARQL+SQL in one server, RDF views of relational data, WebDAV/HTTP publishing. NFR: single-node bulk load of ~20B triples with real-time updates (Wikidata criteria) [CLAIM-openlink-virtuoso-04]. EOIP takeaway: a virtual-graph tier over SQL is a documented product need (CAP-21), consistent with Ontop in `C04-ontop.md`.

## 7. Performance and resource model
No verified benchmark in this run. Wikimedia's evaluation states capability to load 20B triples but flagged tuning/operational complexity [CLAIM-openlink-virtuoso-04]. Failure modes: tuning-dependent memory/buffer configuration (hypothesis); feature cliff between editions.

## 8. Strengths
SQL+SPARQL in one engine; RDF Views; long operating history; large public endpoints; JDBC bridges for Jena/RDF4J. Match: EOIP already plans virtualisation (BL-51 partial); exceed by versioned mappings and per-tenant policy.

## 9. Limitations
Licensing: GPL open source with key enterprise features (cluster HA, inference, ABAC, encryption) commercial-only [CLAIM-openlink-virtuoso-02]. Operational: tuning and heavier ops (Wikimedia review) [CLAIM-openlink-virtuoso-04]. Friction: slow release cadence; user complaints not collected (UNKNOWN). Algorithmic: not analysed.

## 10. Deployment, licensing
Self-hosted, Docker image, native binaries; air-gap yes. GPLv2 (repo licence file; "3 other licenses" present, not enumerated) [CLAIM-openlink-virtuoso-03]: strong-copyleft; bundling or linking triggers legal review; commercial licence lifts GPL restrictions incl. OEM [CLAIM-openlink-virtuoso-02]. Safe use for EOIP: separate-process, customer-installed optional backend only (no redistribution).

## 11. Delta vs baseline
BL-06 SPARQL-over-HTTP adapters could target Virtuoso unchanged (conformance not run); BL-51 federation planner is partial vs RDF Views; BL-20 no tenancy in Virtuoso evidence; ABAC is commercial-only.

## 12. Cards
STR-openlink-virtuoso-01 | Virtuoso | RDF Views expose relational data as graphs without copying | 02 | freshness-sensitive sources | match | declarative versioned mappings feeding virtual tier, ACL-aware | test: change SQL row, graph answer changes within 1 query, ACLs preserved.
INV-openlink-virtuoso-01 | Virtuoso OSS 7.2.17 | enterprise-gated HA/inference/ABAC | root cause: licensing (proven) | alternative: EOIP native policy + any open store; worse if customers need Virtuoso-specific SQL join | options: (a) support Virtuoso as optional customer-installed backend (b) conformance-tested SPARQL subset (c) own virtual tier | select (a) | POC: run adapter conformance on VOS 7.2.17 in Docker | defensibility: policy portability | decision EXPERIMENT. Seed hypothesis §10.5 (Ontop/OBDA) partly relevant: validated direction (hybrid virtual+materialised) but no Virtuoso evidence for mapping versioning.

## 13. Capability decisions
CAP-21 federation/virtualisation: REFERENCE + EXPERIMENT. CAP-15 SPARQL endpoint backend: INTEGRATE (optional, not bundled). CAP-16 SQL bridge: DEFER. CAP-46/45 ABAC: BUILD natively. CAP-52 bundling: REJECT (GPL).

## 14. Tests
PROPOSED: Docker VOS 7.2.17 + adapter conformance (BL-07); SPARQL 1.1 W3C test subset; load 100M-triple LUBM and record memory/time (state hardware); confirm whether SHACL/RDF 1.2 exist.

## 15. Risks, questions
Exact release year of 7.2.17 (community post dated May 2026, consistent with Wikipedia 7 May 2026); commercial version number; GPL scope for network use; HA absence in OSS.

## Appendix A. Dimensions
| Dim | Sec | Summary |
|---|---|---|
| D1 | 1,10 | OpenLink; GPL+commercial |
| D2 | 2 | linked data, hybrid |
| D3 | 4 | single server, hypothesis |
| D4 | 5 | UNVERIFIED |
| D5 | 3 | SHACL unknown |
| D6 | 5 | SPARQL-to-SQL hypothesis |
| D7 | 3 | inference commercial |
| D8 | 3 | HA commercial |
| D9 | 3 | RDF Views, external commercial |
| D10-D12 | N/A | not covered |
| D13 | 3 | GraphQL; vector unknown |
| D14 | N/A | none |
| D15 | N/A | none |
| D16 | N/A | Conductor UI not examined |
| D17 | 3 | JDBC/ODBC |
| D18 | 3 | ABAC commercial |
| D19 | N/A | not found |
| D20 | 7 | no numbers |
| D21 | 10 | dual licence |
| D22 | 8 | wide |
| D23 | N/A | not reviewed |
| D24 | App C | mixed |

## Appendix B. CAP mapping
| CAP | Virtuoso | CLAIM | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-02 | native | 03 | BL-06 | INTEGRATE | P3 |
| CAP-15 | native | 02 | BL-06 | INTEGRATE | P3 |
| CAP-16 | native | 02 | BL-59 absent | DEFER | P3 |
| CAP-17 | native | 02 | BL-58 absent | REFERENCE | P3 |
| CAP-21 | native (commercial for external) | 02 | BL-51 partial | EXPERIMENT | P2 |
| CAP-23 | enterprise-only rules | 02 | BL-30 | DEFER | P3 |
| CAP-45 | enterprise-only ABAC | 02 | BL-19 | BUILD | P1 |

## Appendix C. Evidence
| CLAIM | version/date | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| openlink-virtuoso-01 | VOS 7.2.17, 2026-05-07 | maintenance release; wikibase:mwapi service; optimiser and RDF Views fixes | Officially documented | https://community.openlinksw.com/t/virtuoso-open-source-7-2-17-release-notes/6248 | 2026-05-07 / 2026-10-26 | 0.8 | GitHub page shows no year |
| openlink-virtuoso-02 | current | edition matrix: HA, custom inference, ABAC, encryption at rest, external RDF Views commercial-only; GPL vs commercial/OEM | Officially documented | https://virtuoso.openlinksw.com/ | undated / 2026-10-26 | 0.75 | pricing sample dated 2024 |
| openlink-virtuoso-03 | develop/7 | GPLv2 repo; multi-model; ODBC/JDBC; optional GeoSPARQL | Officially documented | https://github.com/openlink/virtuoso-opensource | 2026-10-26 | 0.8 | licence exceptions not enumerated |
| openlink-virtuoso-04 | Wikidata evaluation, edited 2026-08-31 | only other OSS able to load 20B triples; heavier ops, tuning, edition gap | Third-party report | https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/WDQS_backend_update/Backend_Replacement | 2026-08-31 / 2026-10-26 | 0.6 | proposal page |

## Appendix D. Assumptions
Internal storage description is hypothesis. No source code or paper opened. Commercial edition current version not verified.
