# C04 — Ontology alignment (LogMap, AgreementMakerLight/Matcha, OAEI systems)

| Field | Value |
|---|---|
| Registry ID | T-C04-ontology-alignment |
| Tier | B — alignment reference for ontology governance and cross-source vocabulary mapping (BL-27, BL-32) |
| Versions examined | LogMap repo (release "Version July 2021"; commits to 2026-10-19; README updated 2026-09); AML **v3.2** (2021-02-24; last commit 2024-07-08); OAEI **2025** campaign (12 tracks, 20 participants) |
| Verified on | 2026-10-18 |
| Worker | V12 |

## 1. Identity, current status, tier, and sources
| Member | Owner | Licence | Status |
|---|---|---|---|
| LogMap (`ernestojimenezruiz/logmap-matcher`) | Ernesto Jiménez-Ruiz (City, Univ. of London; Oxford origins) | Apache-2.0 repo licence [CLAIM-oa-01] | **active** (commits 2026-10-19; latest tagged release 2021) |
| AgreementMakerLight (`AgreementMakerLight/AML-Project`) | Daniel Faria et al. (Lisbon) | Apache-2.0 [CLAIM-oa-02] | **maintenance/stale** (v3.2 2021; last commit 2024-07) |
| Matcha (AML successor, new architecture) | same group | UNVERIFIED (repo not located) [CLAIM-oa-03] | active in OAEI 2025 (Anatomy F-measure 0.941 reported on preliminary page) [CLAIM-oa-04] |
| OAEI (evaluation campaign) | community | n/a | annual; 2025 results presented 2025-11-02 [CLAIM-oa-04] |
Systems listed on 2025 pages include LogMap, LogMapLt, LogMapKG, LSMatch, Matcha, Agent-OM (new) [CLAIM-oa-04]. AML was not found in 2025 results (search only). Dependency licences (OWL API, reasoners) were not inspected: **legal-review flag** because LogMap bundles reasoning libraries (hypothesis). Sources (6).

## 2. Problem, workloads, workflows
Find correspondences (equivalence/subsumption, classes, properties, instances) between ontologies, with repair of logically inconsistent mappings. Workflow: load two OWL files -> lexical indexing and anchor mappings -> iterative structural/reasoning-based expansion -> inconsistency repair -> alignment (RDF Alignment/SSSOM-like) -> human review. LogMap offers user intervention and LLM validation and an LLM extension (LogMapLLM, arXiv 2508.08500) [CLAIM-oa-01].

## 3. Feature inventory
| Feature | LogMap | AML/Matcha |
|---|---|---|
| Large biomedical-scale matching (10^4-10^5 classes) | present [CLAIM-oa-01] | present (AML; recalled, conf 0.6) |
| Built-in reasoning and repair | present [CLAIM-oa-01] | partial (AML repair; recalled) |
| Interactive user intervention | present | GUI mode present [CLAIM-oa-02] |
| LLM validation / embeddings (OWL2Vec*, OntoAlign) | present as extensions [CLAIM-oa-01] | Matcha-DL ranking [CLAIM-oa-03] |
| MELT platform interface | present [CLAIM-oa-01] | unknown |
| Alignment governance (versioned, reviewed) | absent | absent |
| Service API | proof-of-concept only (KGAS) | absent |

## 4. Architecture
```
O1,O2 -> lexical indexer -> anchors -> [structural expansion + OWL reasoning] -> candidate mappings
      -> inconsistency repair (diagnosis, remove minimal mapping subset) -> alignment output
(optional: LLM validation / embedding ranker / user oracle)
```

## 5. Under-the-hood reconstruction
LogMap (hypotheses from the published design, conf 0.5; source not opened): inverted index of lexical labels yields high-confidence anchors; mappings are propagated through the class hierarchy in iterated "expand and repair" rounds; a lightweight propositional encoding (Horn) of the combined ontologies+mappings detects unsatisfiable classes and a repair heuristic drops a small set of mappings. AML: element-level lexical matchers with a combination of matchers, selection under cardinality constraints, optional repair. Division of the alignment task (modules) is documented for scale [CLAIM-oa-01]. No transactions/tenancy; library/CLI.

## 6. Requirements inferred
Reasoned alignment with consistency repair; evaluation against reference alignments (OAEI tracks); mapping provenance (confidence, method); human validation.

## 7. Performance and resource model
OAEI Anatomy 2025: LogMap, LogMapLite, LogMapKG, LSMatch, Matcha aligned in under 100 s [CLAIM-oa-04] (campaign hardware per OAEI, not stated here; preliminary). LogMap and LogMapLt results unchanged between 2023-2025 [CLAIM-oa-04]. No other numbers.

## 8. Strengths
| ID | Strength | Match/exceed |
|---|---|---|
| STR-oa-01 | Repair-aware alignment (consistency) | EXPERIMENT: run LogMap as an offline proposal generator; EOIP records mappings as reviewed `skos:exactMatch`/SSSOM-like claims |
| STR-oa-02 | OAEI as shared benchmark and reference alignments | REUSE for acceptance tests |
| STR-oa-03 | Apache-2.0 JVM tools, offline | INTEGRATE as optional worker |
| STR-oa-04 | LLM-validated mapping candidates | EXPERIMENT via local LLM |

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | Designed for OWL ontologies with lexical overlap; weak on enterprise JSON-derived ontologies (hypothesis) |
| Operational | AML stale; Matcha repo/licence unverified; releases of LogMap old (2021) while commits continue |
| Developer friction | JVM batch tools, no governed workflow |
| Licensing | transitive licences to check |
INV-oa-01: *Target* LogMap/AML. *Limitation:* alignments are files, not governed artefacts; no review/approve/release. *Root cause* governance (proven by feature list). *Options:* (a) run offline and import SSSOM; (b) alignment proposals as PR into `ontology/gitops.py` workflow with semantic diff; (c) native matcher. *Selected:* (b) using BL-32 stewardship. *POC:* two public OAEI Conference-track ontologies + one internal; success = precision/recall vs reference measured, every accepted mapping carries method, confidence, reviewer. *Decision:* EXPERIMENT. Seed hypotheses: none target this.

## 10. Deployment, licensing, viability
JVM, offline, Apache-2.0 repos; dependency licences unverified; run as sidecar process, not linked.

## 11. Competitive delta vs EOIP baseline
EOIP has ontology-as-code and stewardship (BL-32, partial), SHACL subset (BL-29), reasoning subset (BL-30), ontology induction (BL-27). No alignment/mapping between ontologies or vocabularies is in the baseline. Alignment fills the "bridge to W3C at boundary" need for imported standards.

## 12. Cards
STR-oa-01..04; INV-oa-01.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| Ontology matching proposals (CAP-41, CAP-37) | EXPERIMENT (LogMap sidecar) |
| Alignment benchmark | REUSE OAEI |
| Own matcher | DEFER |
| AML | REJECT (stale) |

## 14. Tests and acceptance
OAEI Conference and Anatomy subsets reproduced; evaluate time/RAM on one-node; verify output import into gitops review.

## 15. Risks and open questions
Matcha licence; transitive licences; transfer to non-biomedical domains; LLM variants need local models.

## Appendix A — Research-dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | status and licences |
| D2 | 2 | ontology matching |
| D3 | 4 | pipeline |
| D4 | N/A | |
| D5 | 2,5 | OWL, repair |
| D6 | N/A | |
| D7 | 5 | reasoning-based repair |
| D8 | N/A | |
| D9 | N/A | |
| D10 | 2 | mapping confidence |
| D11 | N/A | |
| D12 | 3 | embeddings |
| D13–D14 | N/A | |
| D15 | 3,9 | no governance |
| D16–D17 | 3 | CLI/GUI |
| D18–D19 | N/A | |
| D20 | 7 | OAEI timing only |
| D21 | 10 | Apache-2.0 |
| D22 | 11 | OWL boundary |
| D23 | N/A | |
| D24 | 5,7 | source not opened |

## Appendix B — Capability mapping
| CAP | Tech | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-41 | plugin | oa-01 | BL-32 partial | EXPERIMENT | P2 |
| CAP-23 | partial | oa-01 | BL-30 partial | REUSE (repair idea) | P3 |
| CAP-78 | native (OAEI) | oa-04 | none | REUSE | P2 |

## Appendix C — Evidence records
| CLAIM | product/version/date | claim | class | source | dates | conf | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-oa-01 | LogMap repo | scalable matching, reasoning/repair, user and LLM validation; LogMapLLM; MELT; division of task; Apache-2.0; commits 2026-10-19 | Officially documented | https://github.com/ernestojimenezruiz/logmap-matcher | README 2026-09 / 2026-10-18 | 0.85 | latest release 2021 |
| CLAIM-oa-02 | AML v3.2 | Apache-2.0; ready-to-run jar; Java 1.7-1.9 tested; v3.2 2021-02-24; last commit 2024-07-08 | Officially documented | https://github.com/AgreementMakerLight/AML-Project | 2026-10-18 | 0.9 | none |
| CLAIM-oa-03 | Matcha | successor to AML, new architecture; Matcha-DL ranker; repo/licence not found | Third-party report | https://www.ceur-ws.org/Vol-1272/paper_151.pdf ; oaei22 paper11 | 2026-10-18 | 0.5 | UNVERIFIED licence |
| CLAIM-oa-04 | OAEI 2025 | 12 tracks, 20 participants; Anatomy times; Matcha 0.941; Agent-OM new | Independent benchmark (preliminary) | https://oaei.ontologymatching.org/2025/results ; https://ceur-ws.org/Vol-4144/om2025-oaei-paper0.pdf | 2025-11-02 / 2026-10-18 | 0.7 | pages say preliminary |

## Appendix D — Assumptions
Algorithm descriptions are recalled from papers, flagged hypothesis; dependency licences not inspected.
