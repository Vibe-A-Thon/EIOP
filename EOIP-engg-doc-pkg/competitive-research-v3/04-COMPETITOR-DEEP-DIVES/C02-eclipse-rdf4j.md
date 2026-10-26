# C02 Eclipse RDF4J

| Field | Value |
|---|---|
| Registry ID | T-C02-eclipse-rdf4j |
| Tier | B (Java RDF framework; reuse reference) |
| Versions examined | 6.0.0 (released 2026-07-02); 5.1.x/5.2/5.3 line referenced only through news pages |
| Verified on | 2026-10-26 (brief date 2026-10-18; actual access date recorded) |
| Worker | V16 (registry W09) |

## 1. Identity, status, sources
Eclipse Foundation project: "modular Java framework for working with RDF data" covering parsing, storage, inferencing, querying; full SPARQL 1.1 query/update [CLAIM-eclipse-rdf4j-01]. Current: 6.0.0 on 2026-07-02, requires Java 25 [CLAIM-eclipse-rdf4j-02]. Licence: Eclipse Distribution License 1.0 (BSD-3-Clause) [CLAIM-eclipse-rdf4j-03]. Status: active. Many third-party stores (GraphDB, Stardog, Neptune, Virtuoso, Blazegraph, metaphactory) implement the RDF4J API [CLAIM-eclipse-rdf4j-01]. Cross-reference: `C02-ontotext-graphdb.md` (RDF4J-based), `C02-apache-jena.md` (competing Java framework).

## 2. Problem and workloads
A library and server for embedding RDF in Java applications and for a common API across stores. Workflows: Rio parse/serialise; embedded MemoryStore/NativeStore/LMDBStore; HTTP server + Workbench; FedX federation; SHACL Sail validation; remote repository proxies. EOIP relevance: the closest REUSE candidate for a JVM-side RDF sidecar and for SHACL/RDFS reasoning, but EOIP is Python (BL).

## 3. Feature inventory
| Feature | Status | CLAIM |
|---|---|---|
| RDF model, Rio parsers (Turtle, TriG, N-Triples/Quads, JSON-LD, RDF/XML, TriX) | present | 01 |
| SPARQL 1.1 query/update; SPARQL 1.2 + RDF 1.2 triple terms, base-direction literals | present in 6.0.0 | 02 |
| LATERAL (non-standard) | present | 02 |
| MemoryStore, NativeStore (~100M triples guidance), LMDBStore | present | 01,02 |
| RDFS inferencer, rule-based reasoning, SHACL/SPIN validation | present as extensions | 01 |
| FedX federation | present | 02 |
| Full-text (Lucene), geospatial | extension | 01 |
| Elasticsearch store | experimental | 01 |
| Solr Sail | removed in 6.0 | 02 |
| Query circuit breakers, slow-query log | present (6.0) | 02 |
| OWL DL reasoning, Datalog materialisation, clustering | absent / not found | |
| Auth / multi-tenancy | not found in sources read | UNKNOWN |

## 4. Architecture
```
 app code --> Repository API (local | HTTP proxy) --> SAIL stack
                                   |   [SHACL Sail] -> [RDFS inferencer] -> [Lucene Sail] -> base Sail
                                   |   base: Memory | Native (B-tree) | LMDB | Elasticsearch(exp.) | 3rd-party
 SPARQL parser -> algebra -> optimizers (cardinality estimates) -> evaluation (FedX for federation)
 RDF4J Server (Jakarta servlet) + Workbench
```
Stackable Sail layers is the key pattern (documented in project docs; layering detail from docs is hypothesis-level here).

## 5. Reconstruction
Data model: statements with contexts (named graphs); 6.0 adds first-class `TripleTerm` replacing RDF-star `Triple` [CLAIM-eclipse-rdf4j-02]. Storage: NativeStore persists with write-ahead log and triple-term/base-direction support; LMDBStore uses an extensible identifier layout inlining some values and a new cardinality estimator, with sketch-based planning off by default [CLAIM-eclipse-rdf4j-02]. Query: parse to algebra, optimise, evaluate; RDF 1.2/SPARQL 1.2 via updated parser, algebra, evaluator, renderer [CLAIM-eclipse-rdf4j-02]. Reasoning: RDFS inferencer as a Sail layer (forward materialisation is the common design, hypothesis—not verified in this run). Concurrency, isolation levels, caching: not read; UNVERIFIED. Source paths not opened.

## 6. Requirements inferred
FR: pluggable store SPI, RDF 1.2 round-trip, SHACL gate on write, federation. NFR: modern JVM baseline (Java 25 is a deployment constraint), Jakarta migration for embedders. EOIP: contract-test any RDF store against this API surface.

## 7. Performance and resource model
No benchmark executed; none cited. NativeStore guidance (about 100M triples) is project advice, not a measurement [CLAIM-eclipse-rdf4j-01]. LMDB loading speedups are release-note claims without workload/hardware. Failure modes: Java 25 baseline, incompatibilities for custom HttpClient 4 code.

## 8. Strengths
Permissive licence; wide ecosystem; API adopted by commercial stores; SHACL and RDFS layers; RDF 1.2 ahead of most stores (verified only for RDF4J itself). Match: EOIP's `FusekiGraphStore/GraphDBGraphStore` already speak SPARQL, so RDF4J compliance gives portability for free.

## 9. Limitations
Algorithmic: no Datalog/OWL RL incremental engine; NativeStore sized for medium data. Operational: JVM footprint and Java 25 floor; breaking changes in 6.0 (Jakarta, HTTP API, RDF-star types, Solr Sail removed) [CLAIM-eclipse-rdf4j-02]. Friction: major-version churn for embedders. Licensing: Elasticsearch optional features carry Elastic licensing questions per the project page [CLAIM-eclipse-rdf4j-01].

## 10. Deployment, licensing
Embedded, Docker, servlet container; air-gap yes (library). EDL/BSD-3 is permissive; redistribution fine subject to notices and the no-endorsement clause. Legal trigger: only optional third-party extras (Elasticsearch).

## 11. Delta vs baseline
BL-06 RDF adapters are HTTP-only and lose property-graph semantics; BL-29 SHACL is in-house subset (RDF4J SHACL Sail is a W3C-conformance-candidate reference, conformance not verified here); BL-30 reasoner tiny; BL-31 JSON-LD exists in-house.

## 12. Cards
STR-eclipse-rdf4j-01 | RDF4J | stackable Sail layers (validation, inference, search around a base store) | 01,02 | clean separation of storage and policy | match | EOIP store wrapper chain: validation gate -> ACL filter -> inference -> store | test: wrapper order swap changes no results except where policy says so.
STR-eclipse-rdf4j-02 | RDF4J | RDF 1.2 triple terms across parsers/stores | 02 | reification without LPG loss | integrate | use as oracle for RDF 1.2 round-trip | test: W3C RDF 1.2 syntax tests via RDF4J vs EOIP JSON-LD export.
INV-eclipse-rdf4j-01 | RDF4J 6.0.0 embedding churn | breaking changes each major | root cause: maturity/coupling (proven by release notes) | alternative: talk only SPARQL/HTTP | worse when in-process speed needed | options: HTTP-only integration; thin Python rdflib/oxigraph embed; own store | select HTTP-only | POC: run EOIP rdf_backend conformance against RDF4J Server 5.x and 6.x | decision ADOPT (integration only). Seed hypothesis (Stardog latency) not targeted.

## 13. Capability decisions
CAP-02 RDF storage: INTEGRATE via SPARQL. CAP-10 SHACL: REUSE (RDF4J SHACL as oracle, EXPERIMENT). CAP-23 OWL: DEFER. CAP-21 federation (FedX): REFERENCE. CAP-11 RDF 1.2 triple terms: EXPERIMENT. CAP-52 embedding as OEM: REJECT for Python core, JVM sidecar optional.

## 14. Tests
PROPOSED: run BL-07 conformance suite against RDF4J Server; run SHACL test-suite comparison (BL-29, U-07) on RDF4J SHACL vs in-house; RDF 1.2 round-trip; measure sidecar memory on 10M triples.

## 15. Risks, questions
Java 25 availability in customer estates; SHACL conformance level; isolation semantics of NativeStore/LMDB under concurrent writers (UNVERIFIED); tenant/graph-level ACL (not provided).

## Appendix A. Dimensions
| Dim | Sec | Summary |
|---|---|---|
| D1 | 1,10 | Eclipse, EDL/BSD-3, active |
| D2 | 2 | embeddable RDF framework |
| D3 | 4 | Sail stack, server, workbench |
| D4 | 5 | native/LMDB/memory |
| D5 | 3 | RDF 1.2, SHACL |
| D6 | 5 | algebra, FedX, estimators |
| D7 | 3,5 | RDFS, rules only |
| D8 | 5,7 | not verified |
| D9 | 3 | federation only |
| D10-D12 | N/A | not an RDF4J concern |
| D13 | 3 | Lucene/ES; no vector |
| D14 | N/A | none |
| D15 | N/A | none |
| D16 | 3 | Workbench |
| D17 | 3 | Java API, HTTP |
| D18 | 6,15 | security UNKNOWN |
| D19 | N/A | none found |
| D20 | 7 | no numbers |
| D21 | 10 | permissive OSS |
| D22 | 8 | RDF formats |
| D23 | N/A | not reviewed |
| D24 | App C | docs-level |

## Appendix B. CAP mapping
| CAP | RDF4J | CLAIM | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-02 | native | 01 | BL-06 partial | INTEGRATE | P2 |
| CAP-04 | native (embedded JVM) | 01 | BL-01 | DEFER | P3 |
| CAP-10 | plugin | 01 | BL-29 partial | EXPERIMENT | P1 |
| CAP-11 | native (6.0) | 02 | absent | EXPERIMENT | P2 |
| CAP-15 | native 1.1 + 1.2 | 02 | BL-06 | INTEGRATE | P1 |
| CAP-21 | native FedX | 02 | BL-51 partial | REFERENCE | P3 |
| CAP-23 | partial RDFS | 01 | BL-30 partial | DEFER | P3 |

## Appendix C. Evidence
| CLAIM | version/date | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| eclipse-rdf4j-01 | current | modular Java framework; SPARQL 1.1; Memory/Native/ES stores; Native ~100M triples; extensions; third-party stores | Officially documented | https://rdf4j.org/about/ | undated / 2026-10-26 | 0.8 | none |
| eclipse-rdf4j-02 | 6.0.0, 2026-07-02 | RDF 1.2, SPARQL 1.2, LATERAL, LMDB/Native persistence of triple terms, Java 25, Jakarta, breaking changes, Solr Sail removed | Officially documented | https://rdf4j.org/release-notes/6.0.0/ ; https://rdf4j.org/news/2026/07/02/rdf4j-6.0.0-released/ | 2026-07-02 / 2026-10-26 | 0.85 | none |
| eclipse-rdf4j-03 | current | licence EDL 1.0 = BSD-3-Clause | Officially documented (secondary pages) | https://projects.eclipse.org/node/8588 ; https://www.eclipse.org/org/documents/edl-v10 | 2026-10-26 | 0.8 | repo LICENSE file not opened |

## Appendix D. Assumptions
5.x features not re-verified. Internals described as hypotheses where marked. No source code opened.
