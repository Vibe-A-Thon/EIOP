# C18-sparql — SPARQL 1.1 and 1.2

| Field | Value |
|---|---|
| Registry ID | T-C18-sparql |
| Tier | B (query standard; BL-06, BL-06a, BL-09) |
| Versions examined | SPARQL 1.1 Query/Update/Protocol/Graph Store/Federated/Service Description/Entailment (Rec 2013-03-21); SPARQL 1.2 Query WD 2026-10-25; Update WD 2026-10-25; Protocol WD 2026-07-23; Graph Store Protocol WD 2026-09-24; Results JSON WD 2026-08-13; CSV/TSV WD 2026-10-22; Federated Query and Service Description WD 2026-04-23; Entailment Regimes WD 2026-04-09 |
| Verified on | 2026-10-26 |
| Worker | V32 |

## 1. Identity, current status, tier, and sources
**SPARQL 1.1 = W3C Recommendation (2013).** **SPARQL 1.2 = Working Draft (all parts)**; the Query WD of 2026-10-25 states the latest Rec is SPARQL 1.1 [CLAIM-sparql-01, -02]. This confirms the other batch's finding (SPARQL 1.2 at WD); RDF 1.2 Concepts is at CR [CLAIM-sparql-03]. Owner: W3C RDF & SPARQL WG. Licence: W3C document licence (text UNVERIFIED).

## 2. Primary problem, workloads, workflows
Declarative pattern matching, aggregation and update over RDF datasets, plus an HTTP protocol. Workflows: BL-06a endpoint to Fuseki/GraphDB; federated joins across sources (SERVICE) — disabled in EOIP; CONSTRUCT to export subgraphs.

## 3. Feature inventory
| Feature | Status |
|---|---|
| SELECT/CONSTRUCT/ASK/DESCRIBE, OPTIONAL, UNION, MINUS, FILTER, aggregates, subqueries, VALUES, BIND | Rec 1.1 |
| Property paths (incl. `*`, `+`) | Rec 1.1 |
| SPARQL Update, Graph Store Protocol, SERVICE federation | Rec 1.1 |
| Entailment regimes (RDF, RDFS, OWL Direct/RDF-Based, RIF) | Rec 1.1 (optional) |
| Triple terms `<<( )>>`, reifier shorthand, annotation `{| |}` | WD 1.2 |
| Base direction functions LANGDIR, hasLANG, hasLANGDIR, STRLANGDIR | WD 1.2 |
| TRIPLE, SUBJECT, PREDICATE, OBJECT, isTRIPLE | WD 1.2 |
| `VERSION` directive "1.2"/"1.2-basic" | WD 1.2 |
| Temporal, ordering of path results, shortest path | absent in spec |

## 4. Architecture (specification structure, conformance classes)
```
Query ---> algebra ---> Results formats (XML/JSON/CSV/TSV)
Update, Protocol (HTTP), Graph Store Protocol, Service Description
Federated Query (SERVICE)    Entailment Regimes (optional)
```
Conformance: query processors, update processors, protocol servers, results parsers; entailment regimes a separate conformance claim.

## 5. Under-the-hood (formal semantics, complexity, what an implementation must do)
Defined by an algebra over multisets of solution mappings (bag semantics); OPTIONAL = left join with compatibility; MINUS vs FILTER NOT EXISTS differ on unshared variables. Complexity (literature, conf 0.7): evaluation PSPACE-complete combined, LOGSPACE data complexity for patterns; property paths with counting under bag semantics were a known blow-up (1.1 mandates distinct-endpoint semantics for `*`/`+`). Implementation must: parse to algebra, optimise (join ordering, filter pushdown), evaluate with open-world matching (no negation-as-failure beyond NOT EXISTS), honour dataset clauses, and under 1.2 treat triple terms as terms. Query evaluation never infers unless an entailment regime or materialisation is enabled. SPARQL ≠ Cypher/GQL: result is a table of RDF terms, no path objects, no graph-valued results except CONSTRUCT [CLAIM-sparql-04].

## 6. Functional and non-functional requirements inferred
FR: read-only default endpoint; parameter binding rather than string splice; result-size and time budgets (CRA-024.9 in BL-06a). NFR: deadline cancellation backend-side; SERVICE/updates blocked unless tenant policy allows.

## 7. Performance and resource model
Engine-dependent; spec gives none. Failure modes: cartesian products, unbounded property paths, `ORDER BY` on huge results, `SERVICE` SSRF. No numbers claimed.

## 8. Strengths and use-case advantages
Mature, multi-vendor, standardised protocol and formats; large conformance corpus; federation. Match via existing rdflib/Fuseki back ends; exceed through tenant-scoped, policy-validated execution.

## 9. Limitations with root causes
| Class | Items |
|---|---|
| Algorithmic | no native path binding/shortest-path; joins exponential in worst case; bag vs set confusion |
| Operational | 1.2 still WD (grammar may change); engines differ on property-path performance and extension functions |
| Friction | verbose for graph traversal compared with openCypher/GQL; edge-property patterns need reification or 1.2 annotations |

## 10. Deployment, licensing, redistribution, viability
Spec royalty-free per W3C policy (UNVERIFIED). Engines: Jena/Fuseki Apache-2.0, RDF4J EDL, rdflib BSD-3, Oxigraph Apache/MIT (prior knowledge, conf 0.6; separate deep dives). Air-gap: yes.

## 11. Competitive delta against EOIP baseline
BL-06a: library-level execution on Fuseki (HTTP) and embedded rdflib with algebra-walk rejection of updates/SERVICE/unbounded paths, typed parameter binding, deadlines — **stronger than raw endpoint exposure**; not mounted on a route (01a). BL-09: `ast_compiler` emits SPARQL text; **no semantic guarantee that a Cypher and a SPARQL translation of one plan return equal answers** (bag vs set, null vs unbound, edge identity). BL-06 semantic loss unmeasured. Open-world absence vs LPG null: a SPARQL OPTIONAL unbound variable is not an LPG null property. No SPARQL 1.2 support is claimed or required today.

## 12. Strength-adoption and inversion cards
STR-sparql-01 | SPARQL 1.1 | standard protocol + algebra enabling safe validation before execution | CLAIM-sparql-01,04 | tenant-safe RDF query | match (done in BL-06a) | extend validator to reject 1.2 triple-term constructs until supported | test corpus passes on rdflib and Fuseki.
INV-sparql-01 | SPARQL | translation to/from LPG queries is not semantics-preserving | CLAIM-sparql-04 | semantics: proven | options: quick = per-backend native plans; native = typed IR with documented unsupported set; long-term = differential test harness | POC: 200 plans, compare result multisets across rdflib, Neo4j, HugeGraph; success = divergences all classified | ADOPT. Seed hypotheses: none targeted.

## 13. Per-capability decisions
CAP-15 REUSE (rdflib/Fuseki) ; CAP-20 BUILD (typed IR, documented loss); CAP-21 DEFER (SERVICE federation off); CAP-19 EXPERIMENT (path constructs); 1.2 features EXPERIMENT behind flag.

## 14. Concrete tests and acceptance
W3C SPARQL 1.1 test suite (manifests under `w3c/rdf-tests/sparql`), SPARQL 1.2 tests in the same repo (UNVERIFIED contents). Acceptance: query evaluation, update (disabled path), results-format and protocol tests pass for enabled features; negative tests for SERVICE/updates/unbounded paths. **PROPOSED, not run** by this batch.

## 15. Risks and open questions
Grammar churn before CR; extension-function portability; whether to adopt SPARQL 1.2 annotations for edge properties; GeoSPARQL dependency.

## Appendix A — Dimension coverage
| Dim | § | Summary |
|---|---|---|
| D1 | 1 | Rec/WD |
| D2 | 2 | workflows |
| D3 | 4 | parts |
| D4 | N/A | engine-defined |
| D5 | 3 | triple terms |
| D6 | 5,7 | algebra, complexity |
| D7 | 5 | entailment regimes optional |
| D8-D9 | 6 | protocol; federation |
| D10-D12 | N/A | out of scope |
| D13-D14 | 11 | NL-to-query risk via IR |
| D15-D17 | N/A | spec only |
| D18 | 6,14 | injection, SERVICE |
| D19 | N/A | none |
| D20-D21 | 7,10 | no numbers |
| D22 | 11 | translation limits |
| D23 | N/A | not assessed |
| D24 | App C | W3C primary |

## Appendix B — Capability mapping
| CAP | Tech | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-15 | native | sparql-01 | BL-06a lib | REUSE | P1 |
| CAP-20 | absent | sparql-04 | BL-09 partial | BUILD | P1 |
| CAP-21 | native (SERVICE) | sparql-01 | BL-51 partial | DEFER | P3 |

## Appendix C — Evidence records
| CLAIM | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| sparql-01 | SPARQL 1.2 Query WD 2026-10-25 | Working Draft; latest Rec is SPARQL 1.1 (2013) | Officially documented | https://www.w3.org/TR/sparql12-query/ | 2026-10-26 | 0.9 | none |
| sparql-02 | SPARQL 1.2 parts | all listed parts WD; dates as in header | Officially documented | https://www.w3.org/groups/wg/rdf-star/publications/ | 2026-10-26 | 0.85 | none |
| sparql-03 | RDF 1.2 Concepts | CR Snapshot 2026-04-07 | Officially documented | https://www.w3.org/TR/rdf12-concepts/ | 2026-10-26 | 0.9 | none |
| sparql-04 | SPARQL 1.2 WD | triple terms, LANGDIR etc.; solution mappings table | Officially documented | https://www.w3.org/TR/sparql12-query/ | 2026-10-26 | 0.75 (page truncated) | LATEST not found in visible text |

## Appendix D — Assumptions
SPARQL 1.1 Rec date and complexity from prior knowledge. Engine licences unverified.
