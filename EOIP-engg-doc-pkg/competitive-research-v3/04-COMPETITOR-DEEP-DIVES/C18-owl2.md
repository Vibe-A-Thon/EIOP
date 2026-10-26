# C18-owl2 — RDFS and OWL 2 profiles (EL, QL, RL, DL)

| Field | Value |
|---|---|
| Registry ID | T-C18-owl2 |
| Tier | B (semantics reference; BL-30) |
| Versions examined | RDF 1.1 Schema (Rec 2014-02-25); OWL 2 Web Ontology Language Second Edition (Rec 2012-12-11); OWL 2 Profiles Second Edition (Rec 2012-12-11); RDF 1.2 Schema WD 2026-10-23 |
| Verified on | 2026-10-26 |
| Worker | V32 |

## 1. Identity, current status, tier, and sources
W3C Recommendations, unchanged since 2012: OWL 2 Structural Spec, Direct Semantics, RDF-Based Semantics, Profiles [CLAIM-owl2-01]. RDFS = Rec (RDF 1.1 Schema); **RDF 1.2 Schema is a Working Draft** [CLAIM-owl2-02]. No OWL 3 Recommendation-track work found (UNVERIFIED by negative search). Governance: W3C; no active OWL WG verified.

## 2. Primary problem, workloads, workflows
Declarative class/property axioms with entailment. Workflows: classify a 100k-class taxonomy (EL); rewrite ontology-mediated queries over relational data (QL, Ontop-style); rule-materialise on triple stores (RL); consistency-check a governed ontology before promotion (DL).

## 3. Feature inventory
| Feature | RDFS | EL | QL | RL | DL |
|---|---|---|---|---|---|
| subClassOf / subPropertyOf / domain / range | yes | yes | yes | yes | yes |
| Existential restriction | no | yes | limited | no | yes |
| Universal / cardinality | no | no | no | limited (max 0/1) | yes |
| Property chains | no | yes | no | yes | yes |
| disjointness / negation | no | yes (disjoint) | yes | yes | yes |
| Nominals, inverse, transitive | no | partial | inverse | partial | yes |
| Datatype reasoning | minimal | restricted | restricted | restricted | full (D) |

## 4. Architecture (specification structure, conformance classes)
```
Structural spec (functional syntax) -> Mapping to RDF graphs (RDF syntaxes)
  Direct Semantics (OWL 2 DL, SROIQ(D))   |  RDF-Based Semantics (OWL 2 Full)
  Profiles: EL | QL | RL (syntactic subsets)  ->  Conformance doc (test cases)
```
Conformance classes: OWL 2 DL / Full ontology checkers, entailment checkers, query-answering (profile-specific) [CLAIM-owl2-01].

## 5. Under-the-hood (formal semantics, complexity, what an implementation must do)
Open-world, monotonic, no unique name assumption: absence of a fact is not falsity; two IRIs may denote one individual unless `differentFrom`. This is the **opposite default** of LPG constraints and of closed-world validation (SHACL). Complexity (Rec text): EL — PTIME-complete (data and taxonomic); QL — NLogSpace-complete taxonomic, AC0 data (first-order rewritable to SQL/UCQ); RL — PTIME-complete consistency, co-NP combined [CLAIM-owl2-03]. OWL 2 DL = SROIQ(D): combined N2EXPTIME-complete, data complexity NP-hard (from literature, not re-fetched, conf 0.7). OWL 2 Full: undecidable. Implementer must: (EL) saturate with completion rules; (QL) perfect-reformulate queries; (RL) forward-chain the rule set (semi-naive); (DL) tableau/hypertableau with blocking and explanation support. RDFS entailment is polynomial but simple-model, with known quirks (axiomatic triples, `rdfs:Resource` everywhere).

## 6. Functional and non-functional requirements inferred
FR: explain every inferred triple (CAP-24), mark inferred vs asserted (CAP-43), retract on source delete (truth maintenance). NFR: bounded reasoning time per tenant; profile validation before load to prevent undecidable fragments; deterministic.

## 7. Performance and resource model
Per profile above; no benchmark numbers claimed. Failure modes: DL explosion on cardinality/nominal-heavy ontologies; RL materialisation blow-up (property chains, transitive closure); inconsistency makes everything entail (explosion) — needs repair/quarantine.

## 8. Strengths and use-case advantages
Formal guarantees and ready-made decision procedures; QL enables virtual query over legacy SQL (CAP-21). Match: enforce a declared profile (EL/RL) as a reasoning contract.

## 9. Limitations with root causes
| Class | Items |
|---|---|
| Algorithmic | DL worst case N2EXPTIME; RL/EL cannot express negation/universals fully; no non-monotonic reasoning, no defaults |
| Operational | OWA surprises business users who expect constraint failures; reasoner licences (HermiT LGPL, Openllet/Pellet-family AGPL or commercial; ELK Apache-2.0 — from prior knowledge, conf 0.6, verify) |
| Friction | modelling pitfalls (domain/range as inference not constraint); Rec frozen since 2012 |

## 10. Deployment, licensing, redistribution, viability
Specification is royalty-free (W3C patent policy, UNVERIFIED). Implementations are separate: GPL/AGPL-class reasoners are legal-review triggers. Air-gap: yes (in-process libraries).

## 11. Competitive delta against EOIP baseline
BL-30 partial: subclass, disjoint, property-chain only (`ontology/rdf.py:598`); no declared profile, no explanation, no OWL 2 conformance run. **RDF/OWL vs LPG**: OWL axioms create entailments, LPG labels/constraints reject writes; BL-28 gate is closed-world label checks — mixing them without stating which fragment governs is incorrect. Bridging loss: `rdfs:domain` to LPG becomes either a constraint (semantics changed from inference to rejection) or nothing; existential restrictions have no LPG form; `owl:sameAs` merge vs LPG node merge (BL-34) differ in identity semantics. Syntactic similarity (class = label) implies **no equivalence**.

## 12. Strength-adoption and inversion cards
STR-owl2-01 | OWL 2 profiles | tractable fragments with proofs | CLAIM-owl2-03 | predictable reasoning cost | match | declare "EOIP-RL" rule set in `ontology/rdf.py` with justification trace | owlrl/RL conformance subset passes; every inferred triple has a rule id.
INV-owl2-01 | OWL 2 | open-world surprises and explosion on inconsistency | CLAIM-owl2-03 | semantics: proven | option: native pragmatic = reason in RL, validate closed-world with SHACL, quarantine inconsistent source graph | POC: seed 5 contradictory claims; success = scope-limited quarantine, no global explosion | EXPERIMENT. Seed hypotheses: none targeted.

## 13. Per-capability decisions
CAP-09 INTEGRATE (Ontology authoring in Protégé; stay standard); CAP-22 BUILD (RL-style incremental materialisation, native); CAP-23 INTEGRATE (ELK/HermiT optional, licence gated); CAP-24 BUILD; CAP-25 EXPERIMENT.

## 14. Concrete tests and acceptance
OWL 2 conformance test cases (W3C OWL 2 Test Cases/Conformance docs, accessed via the OWL 2 Conformance Rec; direct entailment tests) filtered to RL; Jena/owlrl as oracle; profile-checker negative tests (inputs outside EL/QL/RL rejected). **PROPOSED, not run.**

## 15. Risks and open questions
Reasoner licences; whether customers need DL at all; RDF 1.2 Schema WD churn; how to surface "unknown" (OWA) in UX.

## Appendix A — Dimension coverage
| Dim | § | Summary |
|---|---|---|
| D1 | 1,10 | Rec 2012 |
| D2 | 2 | workflows |
| D3 | 4 | spec parts |
| D4 | N/A | storage unspecified |
| D5 | 3,5 | expressivity |
| D6 | 5 | QL rewriting |
| D7 | 5,7 | core of this entry |
| D8-D9 | N/A | none |
| D10 | 6 | explanation |
| D11 | N/A | no temporal axioms (OWL-Time separate) |
| D12-D14 | N/A | out of scope |
| D15 | 12,13 | governance via Protégé |
| D16-D19 | N/A | spec only |
| D20 | 7 | no numbers |
| D21 | 10 | reasoner licences |
| D22 | 11 | RDF/LPG loss |
| D23 | N/A | not assessed |
| D24 | App C | W3C primary |

## Appendix B — Capability mapping
| CAP | Tech | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-09 | native | owl2-01 | BL-30 partial | INTEGRATE | P1 |
| CAP-22/23 | native (RL/EL) | owl2-03 | BL-30 partial | BUILD/INTEGRATE | P1 |
| CAP-24/25 | absent in spec | — | absent | BUILD/EXPERIMENT | P2 |

## Appendix C — Evidence records
| CLAIM | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| owl2-01 | OWL 2 Profiles 2nd ed, 2012-12-11 | W3C Recommendation, EL/QL/RL profiles | Officially documented | https://www.w3.org/TR/owl2-profiles/ | 2012-12-11 / 2026-10-26 | 0.9 | none |
| owl2-02 | RDF 1.2 Schema 2026-10-23 | Working Draft | Officially documented | https://www.w3.org/groups/wg/rdf-star/publications/ | 2026-10-26 | 0.85 | none |
| owl2-03 | Profiles Rec | EL PTIME-complete; QL NLogSpace taxonomic, AC0 data; RL PTIME consistency, co-NP combined | Officially documented | https://www.w3.org/TR/owl2-profiles/ | 2026-10-26 | 0.9 | none |

## Appendix D — Assumptions
DL/Full complexity and reasoner licences from prior knowledge, not re-fetched. Absence of OWL 3 work not verified positively.
