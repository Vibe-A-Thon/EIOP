| Field | Value |
|---|---|
| Registry ID | T-C03-vocbench |
| Tier | B (OSS collaborative SKOS/OWL editor) |
| Versions examined | VocBench 3 v15.1 (2026-05-07, listed as latest); v12.0 (2023-12-11); v10.0 (2021-09-30) |
| Verified on | 2026-10-26 (actual access date) |
| Worker | V13 |

## 1. Identity, current status, tier, and sources
VocBench 3 (VB3) is a web-based, multilingual, collaborative editor for OWL ontologies, SKOS/SKOS-XL thesauri, OntoLex-Lemon lexicons and generic RDF datasets, developed by the ART group at the University of Rome Tor Vergata, funded by the EC ISA² programme and used by the EU Publications Office and FAO [CLAIM-vocb-01]. The EU Interoperable Europe release list shows 15.1 on 07/05/2026 as latest, then 12.0 (11/12/2023), 11.0 (12/05/2022), 10.0 (30/09/2021) [CLAIM-vocb-02]. Licence: BSD-3-Clause for the standalone distribution (release page); public release in 2017 under BSD 3-clause (secondary) [CLAIM-vocb-03]. Active, but a slow cadence (about yearly). Tier B: the open counterpart to PoolParty for SKOS lifecycle; CAP-12.
Sources: `https://interoperable-europe.ec.europa.eu/collection/semic-support-centre/solution/vocbench/releases`, release/100 page, VocBench docs `https://vocbench.uniroma2.it/doc/`.

## 2. Problem, workloads, workflows
Teams curate multilingual controlled vocabularies and ontologies with roles and approval. Workflow: create project on a triple store; curators edit concepts/labels; edits recorded in history; validators approve changes; publish to SPARQL endpoint / linked data. Import spreadsheets with Sheet2RDF [CLAIM-vocb-04].

## 3. Feature inventory
| Feature | Status | Evidence |
|---|---|---|
| SKOS, SKOS-XL, OWL, OntoLex-Lemon editing | present | [CLAIM-vocb-05] |
| Collaborative multi-user with roles | present | [CLAIM-vocb-05] |
| History stored as triples (action metadata and changed triples); time-machine view | present | [CLAIM-vocb-04][CLAIM-vocb-05] |
| Validation workflow (approve/reject) | present; recommended with GraphDB for history/validation (v7.0 note) | [CLAIM-vocb-05] |
| Undo, including collaborative | present | [CLAIM-vocb-04] |
| OWL inconsistency detector | present (v10.0) | [CLAIM-vocb-04] |
| SHACL support | partial ("improved" in 10.0; scope unverified) | [CLAIM-vocb-04] |
| Sheet2RDF spreadsheet import, multiple named graphs | present | [CLAIM-vocb-04] |
| Multilingual UI | present | [CLAIM-vocb-04] |
| REST API | likely (Semantic Turkey backend) | UNVERIFIED |
| Property graph / Gremlin / Cypher | absent | inference |
| Real-time co-editing (CRDT) | absent / not verified | UNVERIFIED |
| Enterprise-only tier | none found | inference |

## 4. Architecture diagram
```
 Browser (Angular UI) --HTTP--> VocBench backend (Semantic Turkey RDF-management framework; v12 re-engineered, OSGi dropped)
                                  |-- project metadata + users/roles (store: UNVERIFIED)
                                  `-- RDF triple store per project (history + validation graphs inside the same store)
```

## 5. Under-the-hood reconstruction
Backend: Semantic Turkey, the ART group's RDF management framework; v12.0 re-engineered backend, dropping OSGi [CLAIM-vocb-02]. Data model: RDF; resource edits stored as triples. History: VB3 records action metadata and the changed triples in the triple store (unlike VB2's SQL history) [CLAIM-vocb-05]; hypothesis: add/delete triple sets in named graphs per operation, with validation state flags. Query: SPARQL against store; reasoning delegated to store; OWL inconsistency detector is a feature, mechanism NOT PUBLICLY VERIFIED here. Concurrency: optimistic multi-user with history and validation (mechanism unverified). Security: user/role admin in-app; fine-grained per-concept ACL not verified. Source not opened.

## 6. Inferred requirements
Role model (curator, validator, admin); per-project store; triple-level change audit; undo; import/export of SKOS/OWL; multilingual labels.

## 7. Performance and resource model
No benchmarks found. Cost is that of the underlying triple store; history-as-triples grows the store (hypothesis). Failure modes: history/validation features depend on specific stores (GraphDB recommendation); large vocabularies untested here.

## 8. Strengths
Free, BSD-3; SKOS-XL and OntoLex coverage; collaborative validation workflow and triple-level history out of the box; EU institutional adoption. Match: EOIP stewardship (`ontology/stewardship.py`) can adopt the propose-validate-publish states; exceed with Git-backed history and tenant scoping.

## 9. Limitations
Verified/documented: history and validation work best with GraphDB (v7.0 note) [CLAIM-vocb-05]. Hypotheses: RDF-only (no LPG); store-coupled; release cadence about yearly; Git integration absent in what I read; no semantic-diff-and-classify of breaking changes documented. Friction: Java/Angular server stack to run; admin model.

## 10. Deployment, licensing, viability
BSD-3 permissive; self-hostable (war/standalone distribution); air-gap viable once store is local (GraphDB Free licence/terms must be checked separately; Fuseki/RDF4J alternatives). Legal-review trigger: none for VB3; depends on chosen store. OEM: BSD allows embedding, but a Java web app beside a Python platform is an extra tier. UI white-labelling not verified.

## 11. Competitive delta vs baseline
CAP-12 SKOS management: EOIP has a fixed label manifest (`ontology/manifest.py`) and stewardship module (BL-32); no SKOS editor or SKOS-XL lifecycle in the baseline inventory (absent/unknown, not separately audited). BL-53 collaboration is annotations, not co-editing. BL-06: EOIP already has Fuseki/GraphDB adapters, so VB3 could sit beside them. BL-31 JSON-LD I/O supports hand-off.

## 12. Cards
**STR-vocb-01** | VocBench 3 | triple-based history with validation workflow for vocabularies | [CLAIM-vocb-05] | regulated vocabularies need approver sign-off and time-travel | match | implement proposal/validate states over EOIP revisions (BL-37) and claim states (BL-39) | acceptance: unapproved term invisible to retrieval, appears after approval, can be rolled back.
**INV-vocb-01** | VB3 v15.1 | editing state lives in the triple store, not in a diffable source repo (docs describe history in store) | [CLAIM-vocb-05] | root cause storage/governance coupling (*hypothesis*) | alternative: Git source of truth + web editor (same as INV-edg-01); worse for large SKOS volumes with high edit rates | options (a) integrate VB3 against Fuseki and export nightly to Git; (b) native stewardship UI on gitops; (c) editor writing commits | selected (a) for SKOS pilots, (b) long term | POC: 5k-concept vocabulary, 3 editors, measure approval latency and export fidelity | decision EXPERIMENT.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-12 taxonomy/SKOS editing UI | INTEGRATE (optional external tool) |
| CAP-41 approval workflow | BUILD (borrow states) |
| CAP-72 visual editing | DEFER |
| CAP-36 history | REFERENCE (already BL-37) |

## 14. Tests
(PROPOSED.) Deploy VB3 v15.1 offline against Fuseki; import a SKOS file; round-trip to Turtle and compare via pySHACL/rdflib isomorphism; verify role separation; license scan of the distribution.

## 15. Risks and open questions
Store lock-in/GraphDB dependence for history; SHACL scope; actual current repo location and activity (GitHub path 404 in this run); security model; accessibility; whether v15.1 changes licensing.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | BSD-3; Tor Vergata; yearly |
| D2 | 2 | Vocabulary curation |
| D3 | 4 | UI + ST backend + store |
| D4 | N/A | Delegates to RDF store |
| D5 | 3 | SKOS/XL/OWL/OntoLex |
| D6 | N/A | Store SPARQL |
| D7 | 5 | OWL inconsistency detector; store reasoning |
| D8 | N/A | Delegated |
| D9 | 3 | Sheet2RDF |
| D10 | 5 | Triple-level provenance of edits |
| D11 | 3,5 | History, time machine, undo |
| D12 | N/A | None |
| D13 | N/A | None |
| D14 | N/A | None |
| D15 | 3,8 | Core strength |
| D16 | 3 | Web, multilingual UI |
| D17 | 3 | API UNVERIFIED |
| D18 | 5,9 | Roles; fine ACL unverified |
| D19 | N/A | Per-project only |
| D20 | 7 | No data |
| D21 | 10 | Free |
| D22 | 9 | RDF standards-based |
| D23 | N/A | None identified |
| D24 | App. C | Release pages, docs; source not opened |

## Appendix B. Capability mapping
| CAP-ID | Technology | CLAIM | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-12 | native | 05 | absent/unknown (BL-32 partial) | INTEGRATE | P2 |
| CAP-41 | native | 05 | BL-32 Partial | BUILD | P1 |
| CAP-36 | native (history) | 05 | BL-37 Implemented | REFERENCE | P3 |
| CAP-72 | partial (web editing) | 05 | BL-53 | DEFER | P3 |

## Appendix C. Evidence records
| CLAIM-ID | product/version/date | claim | class | source | dates | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-vocb-01 | VB3 | Web-based collaborative platform for OWL, SKOS(XL), OntoLex, RDF; Tor Vergata team; ISA² funded; Publications Office managed | Third-party report | search summary of EU pages | n/a / 2026-10-26 | 0.6 | none |
| CLAIM-vocb-02 | 15.1 | Releases: 15.1 (07/05/2026), 12.0, 11.0, 10.0; 12.0 re-engineered backend dropping OSGi | Officially documented / third-party | https://interoperable-europe.ec.europa.eu/collection/semic-support-centre/solution/vocbench/releases | 2026-05-07 / 2026-10-26 | 0.75 | OSGi note from search summary |
| CLAIM-vocb-03 | standalone | BSD 3-Clause "New" or "Revised" | Officially documented | same release page | 2026-10-26 | 0.7 | EU page does not mention EUPL |
| CLAIM-vocb-04 | 10.0 | Time machine, named graph switching, OWL inconsistency detector, Sheet2RDF, undo, improved SHACL support | Officially documented | https://interoperable-europe.ec.europa.eu/collection/semic-support-centre/solution/vocbench/release/100 | 2021-09-30 / 2026-10-26 | 0.8 | 10.0 page marked outdated |
| CLAIM-vocb-05 | VB3 v7.0 era | History stored as triples with action metadata; Semantic Turkey backend; history and validation advised on latest GraphDB | Third-party report | https://vocbench.uniroma2.it/doc/vb2_vs_vb3.jsf ; https://lists.w3.org/Archives/Public/public-ontolex/2020Feb/0011.html | 2020-02 / 2026-10-26 | 0.55 | may have changed in 15.x |

## Appendix D. Assumptions
GitHub repo path not found; release data taken from EU Interoperable Europe pages. Features of 15.x beyond 10.0 notes not verified. Store compatibility list not verified.
