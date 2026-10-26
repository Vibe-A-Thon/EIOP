# C18-shacl — SHACL Core, SHACL-SPARQL, SHACL 1.2

| Field | Value |
|---|---|
| Registry ID | T-C18-shacl |
| Tier | B (validation standard; BL-28, BL-29) |
| Versions examined | SHACL (1.0) Rec 2017-07-20; SHACL 1.2 Core WD 2026-10-25; Node Expressions WD 2026-10-22; SPARQL-Related Features WD 2026-10-22; Inference Rules FPWD 2026-09-17; Profiling FPWD 2026-07-02; User Interfaces FPWD 2026-05-26; pySHACL 0.40.1 (as installed in EOIP venv, per 01a) |
| Verified on | 2026-10-26 |
| Worker | V32 |

## 1. Identity, current status, tier, and sources
SHACL 1.0 (Core + SHACL-SPARQL) is a **W3C Recommendation (2017)**. **SHACL 1.2 is a family of Working Drafts / First Public Working Drafts from the Data Shapes WG, not a Recommendation** [CLAIM-shacl-01]. Core WD states the latest Rec remains SHACL 1.0 [CLAIM-shacl-02]. SHACL 1.2 SPARQL-Related Features splits SPARQL out of Core. A sibling "SPARQL 1.2 RL" WD is listed but belongs to the SPARQL track. Licence: W3C document/software licences (UNVERIFIED text).

## 2. Primary problem, workloads, workflows
Validate RDF graphs against shapes and produce a machine-readable report. Workflows: gate ingest/promotion of tenant ontology data; derive UI forms and GraphQL types from shapes (BL-58 library); closed-world constraint checking over an open-world store.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Core constraint components (class, datatype, cardinality, pattern, logical, `sh:closed`) | Rec 1.0, WD 1.2 |
| Targets (node, class, subjectsOf, objectsOf) | Rec; 1.2 adds `sh:targetWhere`, `sh:shape` |
| SHACL-SPARQL (`sh:sparql`, SPARQL-based constraint components) | Rec 1.0; WD 1.2 relocated |
| SHACL-JS, advanced features, rules (`sh:TripleRule`) | Working Group Note (not Rec) |
| Node expressions, `sh:values`, `sh:defaultValue` | WD 1.2 |
| `sh:ShapeClass`, reifier-annotated severity/messages | WD 1.2 |
| Inference rules, profiling, UI | FPWD |

## 4. Architecture (specification structure, conformance classes)
```
SHACL Core (shapes graph + data graph -> validation report)
   + SPARQL-Related Features (sh:sparql, SPARQL constraint components)
   + Node Expressions -> Inference Rules (FPWD) ; Profiling ; User Interfaces
```
Conformance: SHACL processor must implement Core; SPARQL support is a separate optional conformance class [CLAIM-shacl-02].

## 5. Under-the-hood (formal semantics, complexity, what an implementation must do)
Validation is a function: (data graph, shapes graph) -> report; closed-world interpretation of the constraints over the given graph, **no entailment unless a prior step materialises** (1.2 adds `sh:entailment`). Core recursion is undefined in 1.0 (recursive shapes implementation-defined); published research shows full recursive validation is NP-hard with negation (literature, conf 0.7). Implementation must: select focus nodes by targets, evaluate each component on value nodes (SPARQL path evaluation for property paths), apply severity, handle `sh:deactivated`, emit `sh:ValidationReport` with source constraint component and shape; SHACL-SPARQL needs a SPARQL engine with pre-binding (`$this`, `$PATH`) and restrictions to avoid unsafe queries. 1.2 reifier annotations require RDF 1.2 triple terms [CLAIM-shacl-03].

## 6. Functional and non-functional requirements inferred
FR: report per violation with focus node, path, value, shape IRI; transactional validate-before-commit (BL-29 CAS-revision). NFR: query timeouts, no `sh:js`/arbitrary SPARQL from untrusted tenants (query-injection surface).

## 7. Performance and resource model
Depends on path-evaluation and SPARQL engines; no standard benchmark verified. Failure modes: unbounded `sh:sparql` cost, recursion, huge `sh:in` lists.

## 8. Strengths and use-case advantages
Shapes are RDF (versionable, reviewable via gitops); closed-world checking complements OWL; reports are structured; shapes can drive UI/API artefacts. Match with adoption of full Core; exceed with provenance-aware reports.

## 9. Limitations with root causes
| Class | Items |
|---|---|
| Algorithmic | recursion undefined/hard; no inference semantics in Core; cross-node aggregates only via SPARQL |
| Operational | 1.2 not final; implementers split between 1.0 and drafts; SPARQL constraints can be costly |
| Friction | not an LPG schema language — no edge-type endpoints/labels/multiplicity of parallel edges; closed-world meaning differs from OWL |

## 10. Deployment, licensing, redistribution, viability
Spec royalty-free (patent policy, UNVERIFIED). pySHACL (Apache-2.0 per its repo, from prior knowledge conf 0.6), TopBraid SHACL (Apache-2.0, conf 0.6), Jena SHACL (Apache-2.0). Air-gap: yes.

## 11. Competitive delta against EOIP baseline
BL-29 partial: in-house subset now rejects unsupported components (`UnsupportedConstraintError`) and a PySHACLAdapter handles `sh:sparql`/`sh:js` explicitly (01a); **W3C SHACL test suite not run** (U-07). BL-28 gate is label/required-property checks — not SHACL. BL-58 GraphQL types are generated from shapes — a lossy projection: SHACL's `sh:or`, `sh:xone`, SPARQL constraints have no GraphQL equivalent. **RDF/LPG**: validating an LPG-over-RDF projection with SHACL checks the projection, not LPG-native semantics (edge identity, parallel edges); PG-Schema is the LPG analogue — no compatibility implied by shared "shape" vocabulary.

## 12. Strength-adoption and inversion cards
STR-shacl-01 | SHACL Core | standard shapes + structured reports | CLAIM-shacl-01,02 | portable validation, UI/API generation | match | pass W3C data-shapes core tests with pySHACL as differential oracle | 100% core tests or listed gaps.
INV-shacl-01 | SHACL 1.2 | draft churn, undefined recursion | CLAIM-shacl-01 | semantics: proven | native option: pin 1.0 + versioned EOIP profile, adapter for 1.2 drafts | POC: compare in-house, pySHACL, Jena on test suite; success = zero silent-conform on unsupported components | ADOPT. Seed hypotheses: none targeted.

## 13. Per-capability decisions
CAP-10 INTEGRATE (pySHACL/Jena as oracle) + BUILD (tenant-safe in-house core); CAP-08 BUILD (own LPG schema layer, see pg-schema); CAP-17 REUSE (shape-to-GraphQL generator, documented loss); CAP-37 EXPERIMENT.

## 14. Concrete tests and acceptance
W3C data-shapes-test-suite (Core and SPARQL manifests; implementation report) in `w3c/data-shapes`; a `shacl12-test-suite` folder exists but contents unverified. Differential run in CI; negative: tenant-supplied `sh:sparql` with SERVICE or unbounded paths must be refused. **PROPOSED, not run.**

## 15. Risks and open questions
Final 1.2 shape of node expressions/inference; recursion; adopting `sh:sparql` safely; test-suite licence not read.

## Appendix A — Dimension coverage
| Dim | § | Summary |
|---|---|---|
| D1 | 1,10 | Rec + WD |
| D2 | 2 | validation |
| D3 | 4 | family |
| D4 | N/A | storage unspecified |
| D5 | 3,5 | expressivity |
| D6 | 5 | SPARQL pre-binding |
| D7 | 5,9 | no entailment |
| D8-D9 | 6 | CAS gate |
| D10-D12 | N/A | out of scope |
| D13-D14 | N/A | none |
| D15 | 8,12 | gitops of shapes |
| D16-D17 | 8 | forms, test suite |
| D18 | 6,14 | query injection |
| D19 | N/A | none |
| D20-D21 | 7,10 | no numbers |
| D22 | 11 | RDF/LPG, GraphQL loss |
| D23 | N/A | not assessed |
| D24 | App C | W3C primary |

## Appendix B — Capability mapping
| CAP | Tech | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-10 | native | shacl-01 | BL-29 partial | INTEGRATE+BUILD | P0/P1 |
| CAP-08 | partial (RDF only) | shacl-02 | BL-28 | BUILD | P1 |
| CAP-17 | absent | — | BL-58 partial | REUSE | P2 |

## Appendix C — Evidence records
| CLAIM | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| shacl-01 | SHACL 1.2 family | Core and Node Expressions and SPARQL-Related Features are WD; Inference Rules, Profiling, UI are FPWD | Officially documented | https://www.w3.org/groups/wg/data-shapes/publications/ | 2026-10-26 | 0.9 | none |
| shacl-02 | SHACL 1.2 Core WD 2026-10-25 | latest Recommendation is SHACL 1.0 (2017) | Officially documented | https://www.w3.org/TR/shacl12-core/ | 2026-10-26 | 0.85 | none |
| shacl-03 | SHACL 1.2 Core WD | adds sh:targetWhere, sh:shape, sh:values, sh:defaultValue, sh:entailment, reifier annotations | Officially documented | https://www.w3.org/TR/shacl12-core/ | 2026-10-26 | 0.75 (page truncated at 100k chars) | possible additional features |

## Appendix D — Assumptions
SHACL 1.0 date and recursion complexity from prior knowledge. Licence classes of implementations unverified.
