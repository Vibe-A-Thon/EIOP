# C18-rdf — RDF 1.1 / 1.2, RDF-star lineage, Turtle / TriG / N-Triples / N-Quads / JSON-LD

| Field | Value |
|---|---|
| Registry ID | T-C18-rdf |
| Tier | B (important interchange reference; BL-06, BL-31) |
| Versions examined | RDF 1.1 Concepts (W3C Rec, 2014-02-25); RDF 1.2 Concepts CR Snapshot 2026-04-07; RDF 1.2 Semantics CR Snapshot 2026-04-07, CR Draft 2026-09-24; RDF 1.2 Turtle/TriG/N-Triples/N-Quads WD 2026-10-23; JSON-LD 1.1 Rec 2020-07-16; RDF-star CG Final Report 2021-12 |
| Verified on | 2026-10-26 (brief said 2026-10-18; actual access date used) |
| Worker | V32 |

## 1. Identity, current status, tier, and sources
Abstract data model of triples/quads of IRIs, blank nodes, literals. Owner: W3C (RDF & SPARQL WG; JSON-LD WG). Status, precisely: **RDF 1.1 and its syntaxes = W3C Recommendations**. **RDF 1.2 Concepts and Semantics = Candidate Recommendation** (Snapshot 2026-04-07; CRD of Semantics 2026-09-24) [CLAIM-rdf-01]; confirmed still not a Recommendation on 2026-10-26. **RDF 1.2 Turtle, TriG, N-Triples, N-Quads, XML Syntax = Working Draft** (2026-10-23/25) [CLAIM-rdf-02]. **JSON-LD 1.1 = Rec**; JSON-LD 1.2 chartered (WG Jan 2026 to Jan 2028) but no draft verified [CLAIM-rdf-03]. **RDF-star = Community Group Final Report (2021-12), not a standard**; its lineage is superseded by 1.2 triple terms [CLAIM-rdf-04]. Licence: W3C Software/Document licences (permissive; terms not re-read, UNVERIFIED).

## 2. Primary problem, workloads, example workflows
Syntax-neutral global-identifier data exchange and merge. Workflows: export a tenant ontology as Turtle for Protégé; load N-Quads into Fuseki/GraphDB (BL-06); publish JSON-LD to web consumers (BL-31); annotate a statement with provenance (RDF 1.2 reifier vs named graph).

## 3. Feature inventory
| Feature | Status |
|---|---|
| IRIs, blank nodes, typed literals, language tags | present (1.1) |
| Named graphs / datasets | present (1.1; no normative graph semantics) |
| Base direction (`rdf:dirLangString`, ltr/rtl) | present in 1.2 CR |
| Triple terms (triple as object only) + `rdf:reifies` reifier | present in 1.2 CR; Turtle `<<( )>>`, `<< >>`, `{| |}` shorthand in WD |
| Edge properties without reification | absent natively; via reifier/annotation (1.2) |
| Property-graph typing/labels | absent |

## 4. Architecture (specification structure, conformance classes)
```
Concepts (abstract syntax) -> Semantics (model theory, simple/RDF/RDFS entailment)
   -> concrete syntaxes: Turtle | TriG | N-Triples | N-Quads | RDF/XML | JSON-LD (separate WG)
   -> consumers: SPARQL 1.x, SHACL, OWL 2 (RDF-Based Semantics)
```
Conformance classes per syntax: document conformance and processor conformance; 1.2 adds a `VERSION` directive ("1.2", "1.2-basic") [CLAIM-rdf-05].

## 5. Under-the-hood (formal semantics, complexity, what an implementation must do)
Graph = set of triples (set semantics, no duplicates, no ordering). Entailment is monotonic; open world; no unique-name assumption. Blank nodes are existentials: graph isomorphism for equality is GI-hard in general (practically canonicalisation via RDFC-1.0). Literals are value-mapped via datatype maps; `xsd:integer` `"01"` and `"1"` are term-distinct, value-equal. An implementation must: parse Unicode/IRI normalisation per spec, skolemise or scope blank nodes per document, preserve literal lexical forms, and treat triple terms as opaque terms that do not assert the inner triple (1.2 semantics: `rdf:reifies` does not assert) [CLAIM-rdf-01]. Quads: datasets have no model-theoretic meaning in 1.1; each engine chooses merge/union default-graph behaviour. JSON-LD is a JSON syntax over an extended model (generalised RDF in the API, lists, `@json` literals, graph containers) — not every JSON-LD document maps to RDF without loss.

## 6. Functional and non-functional requirements inferred
FR: round-trip IRIs, datatypes, language/direction, named graphs; deterministic canonical form for hashing (BL-37/48 audit). NFR: streaming N-Triples/N-Quads for bulk load; no network on parse (JSON-LD remote `@context` must be pinned/offline for air-gap).

## 7. Performance and resource model
Not specified by the standard. N-Triples/N-Quads are line-oriented, parallel-parsable; Turtle/JSON-LD are not. No numbers claimed. Failure modes: remote context fetch (SSRF, air-gap break), blank-node explosion, huge literals.

## 8. Strengths and use-case advantages
Global identifiers and merge-by-union make multi-source integration well-defined; mature tooling; normative test suites. Match/exceed: EOIP already emits JSON-LD with loss accounting (BL-31) and uses rdflib as oracle.

## 9. Limitations with root causes
| Class | Items |
|---|---|
| Algorithmic | blank-node isomorphism; no ordering; edge properties need reification (cost: 3-4x triples) |
| Operational | 1.2 syntaxes are WD; parsers diverge until CR/Rec; RDF-star vs 1.2 syntax differences (triple terms object-only, `rdf:reifies`) |
| Friction | named graph semantics left to implementations; JSON-LD context handling |

## 10. Deployment, licensing, redistribution, viability
Pure specification; royalty-free via W3C Patent Policy (UNVERIFIED for 1.2 CR exclusion period). Libraries (rdflib BSD-3, Jena Apache-2.0, RDF4J EDL BSD-3) per their own deep dives. Air-gap viable: yes, if JSON-LD contexts are bundled.

## 11. Competitive delta against EOIP baseline
BL-06: Fuseki/GraphDB adapters serialise via rdflib; the LPG-shaped API cannot express RDF-only constructs (blank-node scope, language/direction, named graphs as first-class) — **semantic loss unmeasured**. BL-31: JSON-LD export/import has loss accounting. BL-33: CML maps to LPG/RDF; no RDF 1.2 triple-term support. **Semantic differences vs LPG**: RDF identifies by IRI, open-world, set semantics, edges are not objects; LPG edges have identity, multi-edges between same pair, local property maps, closed schema when declared. Bridging losses: LPG parallel edges collapse unless edge IRIs minted; edge properties require reifiers; RDF literals language/datatypes need property typing; named-graph provenance has no LPG analogue. Syntax resemblance (`<<..>>` vs edge properties) implies **no compatibility**.

## 12. Strength-adoption and inversion cards
STR-rdf-01 | W3C | canonical, test-suite-backed interchange | CLAIM-rdf-01,06 | portable ontology/data exit | match | rdflib oracle in CI + w3c/rdf-tests | all RDF 1.1 syntax tests pass.
INV-rdf-01 | RDF 1.2 | syntaxes still WD | CLAIM-rdf-02 | semantics: proven (status) | option: emit 1.1-reified form by default, 1.2 behind flag | POC: round-trip 10k edge-annotated claims through rdflib and Jena, loss = 0 or reported | ADOPT (flagged). Seed hypotheses in §10.5 on RDF: none targeted.

## 13. Per-capability decisions
CAP-02 INTEGRATE (via rdflib/Jena, never own a triplestore); CAP-11 EXPERIMENT (1.2 triple terms, behind flag); CAP-20 REFERENCE; CAP-29 DEFER.

## 14. Concrete tests and acceptance
Run w3c/rdf-tests (`rdf/`, `shapes/`; N-Triples/N-Quads/Turtle/TriG manifests) against EOIP parse/serialise paths; JSON-LD API tests from w3c/json-ld-api. Acceptance: 100% of applicable positive/negative syntax tests; documented loss list for LPG round trip. **PROPOSED, not run.**

## 15. Risks and open questions
1.2 CR exit may change syntax; JSON-LD 1.2 draft absence UNVERIFIED; does RDFC-1.0 canonicalisation suit tenant audit hashes?

## Appendix A — Dimension coverage
| Dim | § | Summary |
|---|---|---|
| D1 | 1 | status/licence |
| D2 | 2 | interchange |
| D3 | 4 | spec structure |
| D4 | 5 | N/A storage unspecified |
| D5 | 3,5 | open-world, reification |
| D6 | N/A | see sparql |
| D7 | 5 | entailment only |
| D8-D9 | N/A | not applicable to a data model; bulk load 7 |
| D10 | 11 | provenance via graphs/reifiers |
| D11 | N/A | no temporal model |
| D12-D14 | N/A | out of scope |
| D15 | 12 | none |
| D16-D19 | N/A | no UX/tenancy; JSON-LD context SSRF 7 |
| D20-D21 | 7,10 | no numbers; royalty-free |
| D22 | 11 | RDF/LPG loss |
| D23 | 10 | patent policy UNVERIFIED |
| D24 | App C | W3C primary sources |

## Appendix B — Capability mapping
| CAP | Tech | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-02 | native | rdf-01 | BL-06 partial | INTEGRATE | P1 |
| CAP-11 | partial (1.2 CR) | rdf-01,05 | none | EXPERIMENT | P2 |
| CAP-29 | n/a | — | BL-33 | DEFER | P3 |

## Appendix C — Evidence records
| CLAIM | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| rdf-01 | RDF 1.2 Concepts/Semantics, 2026-04-07 | CR Snapshot; triple as object; latest Rec is 1.1 | Officially documented | W3C https://www.w3.org/TR/rdf12-concepts/ | 2026-04-07 / 2026-10-26 | 0.9 primary | none |
| rdf-02 | 1.2 syntaxes, 2026-10-23 | Turtle, TriG, N-Triples, N-Quads, XML are WD | Officially documented | https://www.w3.org/groups/wg/rdf-star/publications/ | 2026-10-26 | 0.85 | none |
| rdf-03 | JSON-LD, 2020-07-16 / charter 2026 | 1.1 Rec; WG chartered Jan 2026–Jan 2028 for 1.2 | Officially documented | https://www.w3.org/groups/wg/json-ld/publications/ | 2026-10-26 | 0.8 | draft existence unchecked |
| rdf-04 | RDF-star CG 2021-12 | Final CG report, not a standard | Officially documented | https://www.w3.org/2021/12/rdf-star.html | 2021-12 / 2026-10-26 | 0.85 | none |
| rdf-05 | SPARQL 1.2 WD 2026-10-25 | VERSION directive "1.2"/"1.2-basic", `<<( )>>`, `{| |}` | Officially documented | https://www.w3.org/TR/sparql12-query/ | 2026-10-26 | 0.8 | syntax in WD may change |
| rdf-06 | w3c/rdf-tests | RDF and SPARQL test suites jointly managed by CG and WG | Officially documented | https://github.com/w3c/rdf-tests | 2026-10-26 | 0.8 | licence not read |

## Appendix D — Assumptions
Access date 2026-10-26. W3C Patent Policy royalty-free assumed, not verified for 1.2. RDF 1.1 Rec dates from prior knowledge (confidence 0.8).
