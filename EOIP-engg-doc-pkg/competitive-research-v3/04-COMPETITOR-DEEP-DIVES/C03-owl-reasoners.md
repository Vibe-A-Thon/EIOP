| Field | Value |
|---|---|
| Registry ID | T-C03-owl-reasoners |
| Tier | B (grouped record; profile-bounded reasoning reference for BL-30) |
| Versions examined | ELK 0.6.0 (Maven 2024-05-24); HermiT 1.3.8 (official, OWL API 3.4.3) and 1.4.5.519 (OWL API 4/5 line, Maven 2020-02-18); Openllet 2.6.5 (Maven 2019-09-27); Konclude changelog top entry v0.7.0-1138 (no date); FaCT++ UNVERIFIED current version |
| Verified on | 2026-10-26 |
| Worker | V13 |

## 1. Identity, current status, tier, and sources
| Member | Identity | Profile / logic | Licence | Status |
|---|---|---|---|---|
| ELK | Java consequence-based reasoner, `liveontologies/elk-reasoner` [CLAIM-owlr-01] | OWL 2 EL fragment, polynomial time; incremental, concurrent, explanations | Apache-2.0 | Latest artefact 0.6.0 (2024-05-24); repo not archived; slow cadence |
| HermiT | Oxford hypertableau reasoner [CLAIM-owlr-02] | OWL 2 DL (SROIQ), DL-safe rules since 1.1; passes OWL 2 direct-semantics conformance tests (vendor/self-claim) | LGPL (older 1.1 readme said GPL: UNVERIFIED which applies to which release) | Official 1.3.8 on OWL API 3.4.3, no date on page; Maven line `org.semanticweb.hermit` to 1.4.5.519 (2020-02-18) [CLAIM-owlr-03]; maintenance NOT PUBLICLY VERIFIED |
| Openllet | Fork/continuation of Pellet by Galigator [CLAIM-owlr-04] | OWL 2 DL, explanations, SPARQL via Jena/OWL API | AGPL-3.0 (dual with commercial) per repo LICENSE.txt [CLAIM-owlr-05] | Maven latest 2.6.5 (2019-09-27); repo not archived but latest commit date unverified; Pellet 1.x-2.3 also AGPL/commercial |
| Konclude | Parallel tableau reasoner, SROIQV(D) plus nominal schemas [CLAIM-owlr-06] | OWL 2 DL; OWLlink subset; basic SPARQL server | LGPLv3 (bundled Qt container modifications GPLv3) | changelog v0.7.0-1138; "still under active development", may contain bugs; release date NOT PUBLICLY VERIFIED |
| FaCT++ | C++ DL tableau reasoner (Tsarkov); JFact is Java port | OWL 2 DL | LGPL per secondary sources; older text said GPL: UNVERIFIED [CLAIM-owlr-07] | Dev home Bitbucket `dtsarkov/factplusplus`; GitHub `ethz-asl/libfactplusplus` mirror archived at 1.6.3 (2014); pyfactxx bindings track 1.8.2 [CLAIM-owlr-07] |
Also noted by ROBOT: Whelk, JFact, EMR, Structural reasoners [CLAIM-owlr-08]. Sources: GitHub repos above; Maven metadata; `https://www.cs.ox.ac.uk/isg/tools/HermiT/`.

## 2. Problem, workloads, workflows
Classification (subsumption), consistency/satisfiability, realisation, explanation. Workflows: CI "reason" step in ontology releases (ROBOT runs ELK by default [CLAIM-owlr-08]); Protégé classification; SPARQL entailment in Jena/OWL API apps.

## 3. Feature inventory
| Feature | ELK | HermiT | Openllet | Konclude | FaCT++ |
|---|---|---|---|---|---|
| OWL 2 EL | present | present | present | present | present |
| OWL 2 QL/RL profile engines | absent (not a rule/rewriting engine) | absent | absent | absent | absent |
| Full DL | absent | present | present | present | present |
| Incremental update | present [CLAIM-owlr-01] | unknown | not documented | unknown | unknown |
| Explanations | present | via OWL API tooling | present | unknown | unknown |
| SWRL/rules | absent | DL-safe | unknown | nominal schemas | unknown |
| API | OWL API, Protégé | OWL API, CLI, Protégé | OWL API, Jena | OWLlink, SPARQL server, CLI | OWL API JNI, C++ |
QL (query rewriting) and RL (rule materialisation) are served by other components (Ontop, OWL-RL/owlrl, RDFox), outside this group.

## 4. Architecture
```
 ontology (OWL API object / Jena model / OWLlink request)
   -> [normalisation + axiom indexing] -> [calculus: ELK saturation | HermiT hypertableau | Pellet/Konclude/FaCT++ tableau]
   -> class taxonomy + realisation -> inferred axioms / explanations -> (ROBOT or app writes inferred ontology)
```

## 5. Under-the-hood reconstruction
ELK: consequence-based saturation; polynomial-time, goal-directed; incremental reasoning recomputes only consequences depending on changed axioms [CLAIM-owlr-01]. HermiT: hypertableau calculus with clausification and blocking; ontology-specific optimisation (hypothesis from Oxford papers; not opened). Konclude/FaCT++/Pellet: tableau with optimisations (parallel Konclude; internals NOT verified here). Code not opened at pinned tags. For EOIP a re-implementation blueprint for the EL fragment is feasible: normalise axioms to NF1-NF4, saturate with completion rules over a queue (the algorithm class ELK documents), add tombstone-aware incremental retraction (hard; ELK supports additions and deletions incrementally, mechanism unverified).

## 6. Inferred requirements
Soundness and completeness per profile; termination guards; explanation; OWL API/Jena interface; JVM runtime (all but FaCT++/Konclude native).

## 7. Performance and resource model
No numbers verified. Complexity (standard theory): EL classification PTIME; OWL 2 DL 2NExpTime-complete worst case; QL in AC0 data complexity; RL PTIME. ELK is positioned for large biomedical EL ontologies; DL reasoners can blow up on heavy nominal/cardinality use. JVM heap and GC dominate for Java members. Failure modes: non-termination/time-outs, unsupported-datatype errors, silent profile violations.

## 8. Strengths
Mature formal semantics; ELK incremental + polynomial; explanations; ROBOT/Protégé integration. Matchable: tractable EL fragment in-house, or integrate ELK sidecar.

## 9. Limitations
Algorithmic: DL worst-case complexity; ELK ignores constructs outside EL (profile bound, not an error in some modes: UNVERIFIED). Operational: JVM footprint; stale OWL API versions (HermiT official on 3.4.3). Friction: dependency on OWL API; open-world semantics surprise users (no closed-world constraints; use SHACL). Licensing: AGPL (Openllet), LGPL (HermiT, Konclude, FaCT++) restrict embedding/linking; Python (EOIP) calling a separate JVM/CLI process is a different link model: legal review trigger.

## 10. Deployment, licensing, viability
Only ELK (Apache-2.0) is permissive. Others are copyleft: record as legal-review triggers; avoid linking into a redistributed product; run as external process only if counsel agrees. Air-gap: all run offline. One-node: yes. Self-hosting a JVM sidecar adds a runtime to a Python product.

## 11. Delta vs baseline
BL-30: in-house `OWLReasoner` at `ontology/rdf.py:598` does subclass, disjointness, property chains only; no profile engine, no explanations from a standard reasoner, no incremental saturation. BL-31 JSON-LD export exists, so OWL/RDF handoff to a sidecar is possible. BL-40 epistemic separation: inferred axioms must be tagged inferred.

## 12. Cards
**STR-owlr-01** | ELK | polynomial, incremental EL classification with Apache-2.0 | [CLAIM-owlr-01] | fast taxonomy checks in release gates | integrate | optional ELK sidecar behind a `Reasoner` interface; results stored with `inferred` plane | acceptance: classify a 100k-class EL ontology and match HermiT subsumptions on shared fragment.
**STR-owlr-02** | ROBOT+ELK | reason step fails build on unsatisfiable classes | [CLAIM-owlr-08] | ontology CI | match | add equivalent check to gitops validation | acceptance: injected unsatisfiable class refused.
**INV-owlr-01** | HermiT/Openllet/Konclude/FaCT++ | copyleft licences and stale APIs block embedding | [CLAIM-owlr-03][CLAIM-owlr-05] | root cause licensing/maturity (*proven* for licence, hypothesis for staleness impact) | alternative: native incremental EL/RL materialiser in Python with explanation traces (seed hypothesis "tiered hybrid materialisation" supported for EL/RL, not for full DL); worse when customers need DL | options (a) ELK sidecar; (b) native EL saturation with provenance; (c) tiered engine with query-time rewriting | selected (a) then (b) | POC: replicate ELK classification on Gene-Ontology-scale EL file; success = identical taxonomy, <5x ELK time | decision EXPERIMENT.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-23 EL profile | INTEGRATE ELK (Apache) / EXPERIMENT native |
| CAP-23 full DL | DEFER; REJECT embedding copyleft reasoners |
| CAP-24 explanations | EXPERIMENT (ELK proofs) |
| CAP-25 inconsistency handling | BUILD (policy), reasoner supplies detection |
| CAP-22 incremental materialisation | BUILD (native, BL-30) |

## 14. Tests
(PROPOSED.) Differential: in-house OWLReasoner vs ELK on subclass/property-chain cases; incremental add/delete equivalence vs full recompute; unsupported-construct detection; time-outs; licence/SBOM scan; inconsistent ontology produces quarantine not crash.

## 15. Risks and open questions
Latest ELK commit date and Konclude/HermiT/FaCT++ maintenance unverified; legal reading of LGPL/AGPL for process boundaries; profile violations silently ignored; JVM sidecar ops cost.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Per-member identity and licence |
| D2 | 2 | Classification workloads |
| D3 | 4 | Library/CLI pipeline |
| D4 | N/A | In-memory; no storage layer |
| D5 | 1,3 | EL/DL profiles |
| D6 | N/A | Not query engines (Konclude SPARQL basic) |
| D7 | 5,7 | Core subject |
| D8 | N/A | No transactions |
| D9 | N/A | None |
| D10 | N/A | None |
| D11 | 5 | ELK incremental only |
| D12 | N/A | None |
| D13 | N/A | None |
| D14 | N/A | None |
| D15 | 2 | CI use via ROBOT |
| D16 | 3 | Protégé plug-ins |
| D17 | 3 | OWL API |
| D18 | N/A | None |
| D19 | N/A | None |
| D20 | 7 | No verified numbers |
| D21 | 10 | OSS, copyleft split |
| D22 | 9 | OWL API coupling |
| D23 | N/A | None identified |
| D24 | App. C | Repos/Maven; papers not read |

## Appendix B. Capability mapping
| CAP-ID | Technology | CLAIM | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-23 | native (EL=ELK; DL=others) | 01,02,06 | BL-30 Partial | INTEGRATE/EXPERIMENT | P2 |
| CAP-24 | partial | 01,04 | BL-30 | EXPERIMENT | P2 |
| CAP-25 | native detection | 08 | BL-30 | BUILD | P1 |
| CAP-22 | partial (ELK incr.) | 01 | BL-30 | BUILD | P2 |

## Appendix C. Evidence records
| CLAIM-ID | product/version/date | claim | class | source | dates | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-owlr-01 | ELK 0.6.0 | OWL 2 EL fragment, polynomial goal-directed, concurrent, incremental, explanations; Apache-2.0; Maven latest 0.6.0 updated 2024-05-24 | Officially documented | https://github.com/liveontologies/elk-reasoner ; https://repo1.maven.org/maven2/io/github/liveontologies/elk-owlapi/maven-metadata.xml | 2024-05-24 / 2026-10-26 | 0.8 | newer builds outside Maven unseen |
| CLAIM-owlr-02 | HermiT 1.3.8 | LGPL; hypertableau; OWL 2 conformance for direct-semantics reasoners; DL-safe rules; OWL API 3.4.3 | Officially documented | https://www.cs.ox.ac.uk/isg/tools/HermiT/ | n/a / 2026-10-26 | 0.7 | 1.1 readme says GPL |
| CLAIM-owlr-03 | HermiT 1.4.5.519 | Maven `org.semanticweb.hermit` latest 1.4.5.519, 2020-02-18 | Officially documented | https://repo1.maven.org/maven2/net/sourceforge/owlapi/org.semanticweb.hermit/maven-metadata.xml | 2020-02-18 / 2026-10-26 | 0.8 | OWL API wiki describes fork for OWL API 5 |
| CLAIM-owlr-04 | Openllet 2.6.x | OWL 2 reasoner in Java built on Pellet; Java 11 since 2.6.5 | Officially documented | https://github.com/Galigator/openllet | n/a / 2026-10-26 | 0.7 | none |
| CLAIM-owlr-05 | Openllet | LICENSE.txt is AGPL-3.0 (dual licensing); Maven latest 2.6.5 on 2019-09-27 | Officially documented | https://raw.githubusercontent.com/Galigator/openllet/integration/LICENSE.txt ; Maven metadata | 2019-09-27 / 2026-10-26 | 0.7 | Maven coordinate may not be the active line |
| CLAIM-owlr-06 | Konclude v0.7.0-1138 | SROIQV(D) parallel tableau; LGPLv3; basic SPARQL, OWLlink subset; under active development | Officially documented | https://github.com/konclude/Konclude | undated / 2026-10-26 | 0.7 | none |
| CLAIM-owlr-07 | FaCT++ | Dev on Bitbucket; ethz-asl mirror archived at 1.6.3 (2014); licence LGPL per JFact page, older GPL text | Third-party report | search results via https://github.com/ethz-asl/libfactplusplus ; https://jfact.sourceforge.net/ | 2014 / 2026-10-26 | 0.35 | licence unconfirmed |
| CLAIM-owlr-08 | ROBOT reason | Supports ELK (default), HermiT, JFact, Whelk, EMR, Structural; fails on unsatisfiable/inconsistent | Officially documented | https://robot.obolibrary.org/reason | n/a / 2026-10-26 | 0.85 | none |

## Appendix D. Assumptions
Maven timestamps used as release dates where GitHub releases pages were empty. Copyleft implications are recorded, not concluded. Internals not opened in source; section 5 for non-ELK members is hypothesis.
