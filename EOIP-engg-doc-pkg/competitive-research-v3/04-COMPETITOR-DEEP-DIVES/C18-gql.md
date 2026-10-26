# C18-gql — ISO/IEC 39075 GQL (Graph Query Language)

| Field | Value |
|---|---|
| Registry ID | T-C18-gql |
| Tier | B (ISO LPG query standard; BL-59) |
| Versions examined | ISO/IEC 39075:2024 (1st ed., published April 2024; sources give 2024-04-11 and 2024-04-12); ISO/IEC 39075:2024/Cor 1:2026 (listed by UNE) |
| Verified on | 2026-10-26 |
| Worker | V32 |

## 1. Identity, current status, tier, and sources
**Published ISO/IEC international standard**, first edition 2024 (JTC 1/SC 32, 610 pages), confirmed by multiple national-body catalogues; the ISO page itself returned HTTP 403 so ISO was not read directly [CLAIM-gql-01]. A 2026 corrigendum (Cor 1:2026) is listed by UNE (single catalogue, conf 0.6) [CLAIM-gql-02]. One third-party article says the standard sits at ISO stage 90.92 (systematic review), unverified. The standard is **paid** (national-body sale); the openCypher grammar artefact is ISO WG3 BNF-format and freely available. Next edition: anticipated schema/DDL expansion per PG-Schema authors (paper statement, not a published plan) [CLAIM-gql-03].

## 2. Primary problem, workloads, workflows
A single standard query-and-DDL language for property graphs. Workflows: portable multi-hop pattern queries; graph-type (schema) declaration; vendor-neutral application code, if engines implement it.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Graph pattern matching (nodes, edges, quantified paths, path modes e.g. WALK/TRAIL/ACYCLIC/SIMPLE, ANY/ALL SHORTEST) | in standard (prior knowledge, conf 0.7; spec paywalled) |
| Data modification (INSERT, SET, REMOVE, DELETE) | in standard |
| Graph types / catalog DDL | in 1st edition (limited; richer DDL anticipated later) |
| Composable subqueries, NEXT chaining | in standard |
| Mandatory/optional feature list; implementation-defined elements | yes |
| Free test suite or conformance programme | NOT PUBLICLY VERIFIED |

## 4. Architecture (specification structure, conformance classes)
```
Parts: Foundation/ Definitions -> Catalog & Session -> Graph types
 -> Pattern matching (shared with SQL/PGQ GPML) -> Query & Data statements
Conformance = mandatory features + chosen optional features (Annex lists)
```
Because pattern-matching language is shared with SQL/PGQ, the two standards align on pattern semantics but differ in host (GQL standalone vs SQL embedding).

## 5. Under-the-hood (formal semantics, complexity, what an implementation must do)
Semantics are specified in ISO prose/BNF, not a published machine-checkable model; research formalisations exist (conf 0.6). Data model: property graph with labels (sets), property maps, directed and undirected edges, parallel edges, edge identity. Path modes are decisive: trail/simple/acyclic semantics make existence checks NP-hard in the general case, hence engines bound or restrict; shortest modes polynomial. Implementers must: parse the BNF, define graph-type conformance on INSERT, apply null/3VL, implement path-mode filtering, selector semantics (ANY SHORTEST etc.), and report features claimed. Nothing in GQL says how to store or index. **No entailment, no open-world**: a graph type either is declared (closed schema) or open; absence is not inference.

## 6. Functional and non-functional requirements inferred
FR: express policy-scoped queries; deterministic result ordering clause; graph types as declarative governance (CAP-08). NFR: bound path expansion; capability matrix per backend so "GQL" claims are testable.

## 7. Performance and resource model
Not specified. Failure modes: unbounded quantified paths, selector semantics blow-up. No numbers.

## 8. Strengths and use-case advantages
Vendor-neutral, standards-body backing, shared pattern core with SQL; reduces long-term lock-in vs proprietary dialects (INV-ocy-01). Match: GQL as canonical compile target of the IR where backends support it.

## 9. Limitations with root causes
| Class | Items |
|---|---|
| Algorithmic | path-mode complexity; no standard cost model |
| Operational | paywalled text; few complete implementations; no public conformance suite found; Cor 1:2026 existence unclear |
| Friction | schema/DDL minimal in 1st ed.; vendors market "GQL support" with differing coverage |

## 10. Deployment, licensing, redistribution, viability
Spec paywalled (ISO/national bodies). Implementations vary: Neo4j converges via Cypher 25 (partial), Google Spanner Graph reported GQL-based (prior knowledge, conf 0.5, verify). Patents: ISO/IEC patent declarations not checked — legal-review trigger. Air-gap: standard itself n/a.

## 11. Competitive delta against EOIP baseline
BL-59 Partial (library-only): `sql_adapter.py`, `cypher_adapter.py` exist; `ast_compiler` emits Cypher/Gremlin/SPARQL, **not GQL**. No GQL execution or parser. **GQL vs RDF**: closed-schema LPG with edge identity vs open-world IRI triples; GQL graph type != SHACL shape != OWL class. Bridging GQL to RDF mints IRIs for nodes/edges and maps labels to `rdf:type` (multi-label = multiple types, no hierarchy); GQL path modes/match modes have **no SPARQL equivalent** (SPARQL property paths return endpoints, not paths). Do not infer compatibility from the shared `-[]->` visual.

## 12. Strength-adoption and inversion cards
STR-gql-01 | ISO GQL | standard LPG language with defined path modes | CLAIM-gql-01 | exit from dialect lock-in | integrate | add GQL emitter target to the IR for backends that advertise support; keep Cypher as fallback | for each feature, equal result multiset vs Cypher on Neo4j.
INV-gql-01 | GQL | paywalled spec + no public conformance suite | CLAIM-gql-01,03 | governance/maturity: proven (absence not found, search-limited) | option: build own capability-matrix tests per backend, publish | POC: 50 GQL-subset queries on each supported backend; success = matrix of pass/fail with reasons | EXPERIMENT. Seed hypothesis on IR lock-in: partly validated (GQL emitter reduces dialect lock-in).

## 13. Per-capability decisions
CAP-14 INTEGRATE (as emitter target, DEFER until two backends support); CAP-20 BUILD; CAP-08 EXPERIMENT (graph types vs PG-Schema); CAP-16 DEFER.

## 14. Concrete tests and acceptance
No public ISO conformance suite found. Use: openCypher TCK for the shared core; vendor test corpora (licence permitting); LDBC workloads for semantic differential. Acceptance: documented subset with version stamp and per-backend pass matrix. **PROPOSED, not run.**

## 15. Risks and open questions
Who tests "GQL conformant"? Spec cost for contributors; edition 2 timing; patent declarations; legal reading of use of the BNF.

## Appendix A — Dimension coverage
| Dim | § | Summary |
|---|---|---|
| D1 | 1,10 | ISO, paid |
| D2 | 2 | portability |
| D3 | 4 | parts |
| D4 | N/A | storage unspecified |
| D5 | 3,5 | graph types |
| D6 | 5 | path modes |
| D7 | N/A | none |
| D8-D9 | N/A | engine-defined |
| D10-D12 | N/A | out of scope |
| D13-D14 | 13 | NL-to-GQL later |
| D15-D17 | 3 | none |
| D18 | N/A | spec only |
| D19 | N/A | none |
| D20-D21 | 7,10 | paywall |
| D22 | 11 | RDF/LPG |
| D23 | 10 | patent declarations unchecked |
| D24 | App C | catalogue sources, ISO 403 |

## Appendix B — Capability mapping
| CAP | Tech | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-14 | native | gql-01 | BL-59 partial | INTEGRATE/DEFER | P2 |
| CAP-08 | partial | gql-03 | BL-28 | EXPERIMENT | P2 |
| CAP-20 | absent | — | BL-09 | BUILD | P1 |

## Appendix C — Evidence records
| CLAIM | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| gql-01 | ISO/IEC 39075:2024 | first edition, April 2024, JTC 1/SC 32, 610 pages | Officially documented (national-body catalogues) | https://webstore.iec.ch/publication/94107 ; https://scc-ccn.ca/standardsdb/standards/8186711 | 2024-04-11/12 / 2026-10-26 | 0.85 | one-day date difference; ISO page 403 |
| gql-02 | ISO/IEC 39075:2024/Cor 1:2026 | corrigendum listed | Officially documented (UNE) | https://www.en.une.org/encuentra-tu-norma/busca-tu-norma/iso?c=076120 | 2026-10-26 | 0.6 | single source |
| gql-03 | PG-Schema paper (SIGMOD 2023) | anticipates richer DDL in second GQL version | Third-party report | https://arxiv.org/abs/2211.10962 | 2023 / 2026-10-26 | 0.6 | paper predates publication |

## Appendix D — Assumptions
Path-mode and feature lists from prior knowledge of public GQL summaries; text is paywalled and was not read.
