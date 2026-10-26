# C18-pg-schema — PG-Schema and LPG schema proposals

| Field | Value |
|---|---|
| Registry ID | T-C18-pg-schema |
| Tier | B (ADD-type entry: schema layer for LPG; BL-28, BL-29) |
| Versions examined | "PG-Schema: Schemas for Property Graphs", Proc. ACM Manag. Data 1(2), art. 198 (SIGMOD 2023), published 2023-06-20, arXiv 2211.10962 v4 (2023-07-08); GQL graph types in ISO/IEC 39075:2024; vendor constraint models (Neo4j, TigerGraph, etc.) |
| Verified on | 2026-10-26 |
| Worker | V32 |

## 1. Identity, current status, tier, and sources
**Peer-reviewed research proposal, not a standard.** Authors include members from academia, LDBC, Neo4j, AWS, Google, data.world and RelationalAI (21 listed on arXiv) [CLAIM-pgs-01]. It builds on PG-Keys (key/constraint formalism) and was positioned by its authors as input to the ISO GQL effort: the paper notes schema support is limited in existing systems and in GQL's first version and that a second version of GQL is "anticipated" to include a rich DDL [CLAIM-pgs-02]. I found **no verified PG-Schema adoption as an ISO or LDBC-published standard**, and no formal PG-Schema working group (UNVERIFIED negative). Other LPG schema approaches (examined by name only): GQL graph types (standard, limited), vendor constraints/indexes (Neo4j, vendor dialect), schema-optional engines, JSON Schema for property maps (de facto). Licence of the paper: publisher/arXiv; no software.

## 2. Primary problem, workloads, workflows
Declarative typing and constraints for nodes, edges, properties, with multi-inheritance and key constraints, in "strict" or "loose" graph types. Workflows: ontology-to-LPG schema compilation; reject ingest violating endpoint types; schema evolution review.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Node/edge types with labels and property specs | in proposal |
| Multi-inheritance among types | in proposal [CLAIM-pgs-01] |
| Key and cardinality constraints (PG-Keys basis) | in proposal |
| Strict vs loose graph type | in proposal (prior knowledge, conf 0.6) |
| Edge endpoint typing | in proposal |
| Reference implementation / validator | NOT PUBLICLY VERIFIED |
| Conformance test suite | absent (none found) |

## 4. Architecture (specification structure, conformance classes)
```
PG-Types (node/edge types, inheritance) + PG-Keys constraints
   -> Graph type (closed/open)  -> validation of a property graph
   (research artefact; no conformance classes; GQL graph type is the standard-track sibling)
```

## 5. Under-the-hood (formal semantics, complexity, what an implementation must do)
The paper gives a formal syntax and semantics for graph type conformance (graph satisfies type iff each element conforms and constraints hold). Closed-world over declared types in strict mode; loose mode allows extra elements. Complexity of conformance checking is bounded by constraint class (key checks polynomial; some inheritance/constraint combos harder — not independently verified). Implementer must: resolve type hierarchy (multi-inheritance diamond rules), evaluate endpoint typing per edge, enforce keys across the graph (uniqueness requires an index or global scan), and define evolution semantics (not specified in the proposal). **Contrast with RDF/OWL**: PG-Schema constrains and rejects; OWL infers; SHACL validates RDF but cannot natively address edge identity or parallel edges.

## 6. Functional and non-functional requirements inferred
FR: schema as versioned artefact diffed by gitops (CAP-37); typed errors; per-tenant graph types. NFR: incremental validation (only touched elements); compile target for each backend (constraints in Neo4j, VertexLabel/EdgeLabel in HugeGraph).

## 7. Performance and resource model
No benchmarks in scope; key checking requires index support. Failure modes: global uniqueness on sharded stores; inheritance explosion.

## 8. Strengths and use-case advantages
Gives LPG what SHACL gives RDF, with edge-first modelling and keys; aligned with GQL direction. Match with an in-house typed schema IR; exceed by compiling to SHACL for RDF export.

## 9. Limitations with root causes
| Class | Items |
|---|---|
| Algorithmic | uniqueness constraints distributed cost; evolution not formalised |
| Operational | no tooling, no suite, no standard; design may change |
| Friction | vendor schemas incompatible with each other; two schema notions (GQL graph type vs PG-Schema) may diverge |

## 10. Deployment, licensing, redistribution, viability
No code to license; patents: authors from Neo4j/AWS/Google — no patent claims verified (legal-review trigger for any implementation that follows it closely: record only). Air-gap: yes.

## 11. Competitive delta against EOIP baseline
BL-28: label/required-property gate only; BL-29: SHACL partial (RDF side); no LPG schema language, no edge endpoint typing declared, no type hierarchy. Closest EOIP asset is the ontology plus CML (BL-33) mapping into LPG/RDF; **semantic loss** when compiling an ontology to a PG-Schema: OWL existential/universal restrictions, `owl:equivalentClass`, disjointness inference, open-world typing have no constraint equivalent; `rdfs:domain/range` change from inference to rejection. Reverse (PG-Schema to SHACL): multi-inheritance maps to `sh:node`/`rdfs:subClassOf` but edge identity and parallel edges need reification. Not compatible by name similarity.

## 12. Strength-adoption and inversion cards
STR-pgs-01 | PG-Schema | typed LPG schema with keys and inheritance | CLAIM-pgs-01 | closes BL-28 gap with a principled design | exceed | EOIP-native "graph type" IR, ontology-compiled, emitting backend DDL + SHACL | for 20 ontologies, compile and reject a violating insert on 3 backends.
INV-pgs-01 | LPG schemas | no standard yet; backends enforce differently | CLAIM-pgs-02 | governance/semantics: proven | options: quick = enforce in gate only; native = IR + backend DDL + reporting; long-term = track GQL edition 2 | POC: same violating write on Neo4j/HugeGraph/rdf adapter; success = identical typed rejection | EXPERIMENT. Seed hypotheses: none targeted.

## 13. Per-capability decisions
CAP-08 BUILD (own graph-type IR, GQL/PG-Schema aligned); CAP-37 BUILD; CAP-10 REUSE (SHACL for RDF export); CAP-28 DEFER.

## 14. Concrete tests and acceptance
No third-party suite. Define EOIP conformance corpus: type, inheritance diamond, key violation, endpoint violation, loose-mode extras; run on each backend adapter and on SHACL export (differential vs pySHACL). **PROPOSED, not run.**

## 15. Risks and open questions
Divergence between PG-Schema and GQL edition 2 DDL; whether any engine implements PG-Schema; patents.

## Appendix A — Dimension coverage
| Dim | § | Summary |
|---|---|---|
| D1 | 1 | proposal |
| D2 | 2 | schema |
| D3 | 4 | formalism |
| D4 | N/A | storage unspecified |
| D5 | 3,5 | core topic |
| D6-D7 | N/A | none |
| D8-D9 | 7 | key checking cost |
| D10 | N/A | out of scope |
| D11 | 6 | evolution gap |
| D12-D14 | N/A | out of scope |
| D15 | 6,12 | gitops |
| D16-D17 | N/A | none |
| D18-D19 | 13 | per-tenant types |
| D20-D21 | N/A | no cost |
| D22 | 11 | loss |
| D23 | 10 | patent flag |
| D24 | App C | peer-reviewed |

## Appendix B — Capability mapping
| CAP | Tech | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-08 | proposal | pgs-01 | BL-28 partial | BUILD | P1 |
| CAP-37 | absent | pgs-02 | BL-32 partial | BUILD | P2 |
| CAP-10 | n/a | — | BL-29 | REUSE | P1 |

## Appendix C — Evidence records
| CLAIM | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| pgs-01 | PG-Schema, SIGMOD 2023 | PG-Types with multi-inheritance; constraints from PG-Keys; 21 authors | Officially documented (peer-reviewed) | https://arxiv.org/abs/2211.10962 ; https://www.research.ed.ac.uk/en/publications/pg-schemas-schemas-for-property-graphs/ | 2023-06-20 / 2026-10-26 | 0.8 | none |
| pgs-02 | same | schema support limited in GQL v1; v2 anticipated to include rich DDL | Officially documented | https://ar5iv.labs.arxiv.org/html/2211.10962 | 2023 / 2026-10-26 | 0.7 | no verified v2 plan |

## Appendix D — Assumptions
Strict/loose semantics and complexity remarks from prior knowledge of the paper. No code repo verified.
