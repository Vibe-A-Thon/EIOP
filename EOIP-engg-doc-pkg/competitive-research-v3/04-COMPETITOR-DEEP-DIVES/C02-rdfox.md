# C02 RDFox (Oxford Semantic Technologies, Samsung)

| Field | Value |
|---|---|
| Registry ID | T-C02-rdfox |
| Tier | B (incremental Datalog materialisation reference for the tiered-reasoning inversion) |
| Versions examined | RDFox 7.7 (release notes dated 2026-09-29); 7.4-7.6 notes; papers AAAI 2015 (B/F), ISWC 2015 |
| Verified on | 2026-10-26 (brief 2026-10-18; actual access date recorded) |
| Worker | V16 (registry W09) |

## 1. Identity, status, sources
In-memory RDF/Datalog engine from Oxford Semantic Technologies (University of Oxford spin-out). Samsung Electronics agreed to acquire Oxford Semantic Technologies; press coverage dated 2024-07-18, aimed at personal knowledge graphs across Samsung products; whether RDFox stays on sale to third parties was not stated [CLAIM-rdfox-01]. The vendor site still offers RDFox (free start, evaluation licence) and release notes show 7.7 on 2026-09-29 [CLAIM-rdfox-02,05]. Licence: proprietary, object-code only; evaluation licence terms in CLAIM-rdfox-04; production licence terms NOT PUBLICLY VERIFIED. Cross-ref: `C02-stardog.md`, `C02-tier-c-records-V16.md` (Nemo, VLog, Soufflé).

## 2. Problem and workloads
Low-latency reasoning over changing knowledge graphs: Datalog with negation and aggregation, OWL 2 RL, SHACL, SPARQL 1.1; cloud, on-prem or edge [CLAIM-rdfox-02]. Workflow: load, import rules, materialise, query, update incrementally, request a shortest-proof explanation [CLAIM-rdfox-03].

## 3. Feature inventory
| Feature | Status | CLAIM |
|---|---|---|
| SPARQL 1.1, federated SPARQL (7.5) | present | 02,05 |
| Datalog rules, stratified negation + aggregation, SWRL, OWL 2 RL (best-effort axiom to rule translation, warnings on disjunction) | present | 02,03 |
| Incremental add/delete maintenance of data and rules | present | 03 |
| Proof/explanation (shortest proof, JSON) | present | 03 |
| SHACL validation | present | 02 |
| Persistence (snapshots + deltas, compaction) | present | 06 |
| HA replication | present (edition UNKNOWN) | 02 |
| Lucene, SQLite data sources, geospatial search/GEODIST, semantic similarity (SEMSIM), index tuple tables | present (7.4-7.7) | 05 |
| REST + Java + C/C++ APIs, web Console, OpenMetrics | present | 02,05 |
| RDF 1.2 / SPARQL 1.2 | not found | UNKNOWN |
| Per-graph access control (roles) | present (details not read) | 06 |
| Property-graph query (Cypher/GQL) | absent | none |

## 4. Architecture
```
 REST / Java / C++ / Console
        |
 Data store (parallel-nn|nw|ww)  max-threads-used
   in-memory tuple tables: DefaultTriples, Quads  + dictionary (prefix sharing)
   Reasoner: Mat (initial) | Addition | Deletion | BwdChain | RuleAdd/RuleDel (incremental)
   SPARQL engine (stats; selectivity-reordering planner in 7.7)  | SHACL | explanation
   persistence: snapshot + delta log, compaction (exclusive)
```

## 5. Under-the-hood reconstruction: incremental materialisation
**Documented behaviour.** RDFox materialises all Datalog consequences, then maintains them "under addition/deletion updates that may affect both the data and the rules"; only explicit triples can be deleted, and deleting one removes dependent consequences [CLAIM-rdfox-03]. Profiler phases of incremental reasoning are Addition, Deletion, BwdChain ("reproving of deleted facts"), RuleAdd and rule deletion; initial load is a single Mat phase; adding facts can trigger deletion plus backward chaining when rules use negation or aggregation [CLAIM-rdfox-03]. Docs attribute the algorithms to published literature without naming them.
**Algorithms in the literature** (AAAI-15 and ISWC-15 papers [CLAIM-rdfox-07,08]; the PDF text was not machine-readable in this run, so the mechanics below are standard background, marked *reasoned inference*, to be checked against the paper):
- *Semi-naive evaluation*: new facts from each round are joined only against the delta, parallelised across threads (ISWC-15 reports parallel computation and incremental update on a 128-core server).
- *Additions*: run semi-naive from the added facts only.
- *DRed (delete/rederive)*: (1) over-delete every fact derivable using any deleted fact, transitively; (2) re-derive over-deleted facts that still have a proof from surviving facts; (3) propagate re-derived and added facts. Weakness: step 1 can remove a large part of the materialisation when facts have many alternative derivations, and step 2 re-pays it.
- *Backward/Forward (B/F)*: avoids blanket over-deletion. For each candidate deletion it searches backwards for a proof from facts that survive, and only propagates forwards from facts that truly lose all proofs. Authors report orders-of-magnitude gains over DRed on some inputs and "never significantly slower" [CLAIM-rdfox-07]. RDFox's BwdChain phase name fits B/F (inference, not stated in the docs). Hypothesis: B/F is the default maintenance method; confirm with the vendor or an experiment.
**Storage**: dictionary-encoded in-memory tuple tables, IRI prefix sharing; deleted facts marked dead, reclaimed on exclusive compaction [CLAIM-rdfox-06]; ISWC-15 reports as low as 36.9 bytes/triple (2015, its datasets) [CLAIM-rdfox-08].
**ACID/isolation**: UNVERIFIED (Transactions section not read).

## 6. Requirements inferred
FR: rule add/delete as first-class updates, explicit/derived separation, stratification check, explanation API. NFR: RAM-bound; exclusive compaction. For EOIP tiering: (a) explicit vs derived provenance (BL-40), (b) B/F-style re-proving on deletes, (c) per-tenant rule sets.

## 7. Performance and resource model
Claims only: ISWC-15 (128 cores, 4 TB RAM): up to 87x speed-up, 9.2B triples, 6.1M triples/s [CLAIM-rdfox-08]; vendor site 2-3M inferred facts/s, no workload stated, Unverified [CLAIM-rdfox-02]. Failure modes: working set above RAM; compaction pauses; densely connected derivations on delete. Publishing benchmarks needs prior approval under the evaluation licence [CLAIM-rdfox-04].

## 8. Strengths
Incremental maintenance of data and rules; parallel materialisation; proof explanations; negation/aggregation in rules; edge footprint. Exceed: ACL-aware explanation and claim status (BL-39/40).

## 9. Limitations
Algorithmic: RAM-resident; stratification limits; sameAs rules exclude NOT/aggregation [CLAIM-rdfox-03]; OWL 2 RL by best-effort translation. Operational: exclusive compaction. Licensing: closed source; evaluation licence forbids commercial use [CLAIM-rdfox-04]. Friction: Samsung ownership clouds roadmap/OEM availability (inference).

## 10. Deployment, licensing
Cloud, on-prem, on-device [CLAIM-rdfox-02]; air-gap plausible (licence key; offline renewal UNVERIFIED). Proprietary; OEM terms NOT PUBLICLY VERIFIED -> legal review trigger; evaluation licence bars distribution and reverse engineering [CLAIM-rdfox-04].

## 11. Delta vs baseline
BL-30 reasoner: subclass/disjoint/property-chain only, no incremental materialisation, no Datalog, no proofs; BL-39/40 claim states are not linked to rule proofs; BL-37/38 revisions could drive delta feeds.

## 12. Cards
STR-rdfox-01 | RDFox | incremental maintenance on data and rule changes | 03,07 | reasoning stays fresh without full recompute | match (pattern) | EOIP tier-1 Datalog subset: semi-naive add, B/F-style delete using revision deltas; explicit/derived flag stored in graph | test: 1% random deletions on 1M-triple LUBM-like graph; incremental result equals full re-materialisation (oracle), time <= 10% of full.
STR-rdfox-02 | RDFox | shortest-proof explanations | 03 | auditability (CAP-24) | match | store rule id + premise ids per derived fact, ACL-check premises before display | test: every derived fact shown to user cites only premises the user may read.
INV-rdfox-01 | RDFox 7.7 | closed-source, RAM-bound materialisation, restrictive evaluation licence | root cause: licensing + storage (proven) | alternative: open implementations (Nemo, Soufflé, VLog; see Tier C) or own Datalog; worse when sub-second multi-million rule firings needed | options: (a) RDFox via REST as customer-licensed backend (b) native semi-naive + B/F (c) Nemo (Apache-2.0/MIT) as reasoning worker | select (b)+(c) | POC: Nemo vs prototype vs RDFox (if licensed) on one rule set; success: equivalence + update latency; RAM per million facts | defensibility: tenant/ACL-aware provenance | decision EXPERIMENT. Seed hypothesis (Stardog latency from query rewriting, tiered materialisation): *partially validated* - RDFox demonstrates materialise-then-maintain; EL/RL coverage and mixed rewriting not evidenced here.

## 13. Capability decisions
CAP-22: EXPERIMENT (BUILD subset; Nemo candidate). CAP-23: EXPERIMENT via rule translation. CAP-24: BUILD. CAP-25: DEFER. CAP-02: INTEGRATE optional. RDFox bundled: REJECT (licence).

## 14. Tests
PROPOSED: (1) incremental vs full materialisation equivalence after random add/delete batches; (2) many-alternative-proof test exposing DRed over-deletion; (3) rule add/remove correctness; (4) ACL-filtered explanation; (5) internal-only use of an evaluation licence, no publication.

## 15. Risks, questions
Is B/F RDFox's actual algorithm? Third-party roadmap under Samsung? Production/OEM terms? RDF 1.2? Isolation semantics?

## Appendix A. Dimensions
| Dim | Sec | Summary |
|---|---|---|
| D1 | 1,10 | Samsung-owned, proprietary |
| D2 | 2 | reasoning KG, edge |
| D3 | 4 | in-memory store |
| D4 | 5 | tuple tables |
| D5 | 3 | SHACL, OWL RL |
| D6 | 3 | SPARQL 1.1 |
| D7 | 5 | core topic |
| D8 | 5,7 | ACID unread |
| D9 | 3 | data sources |
| D10-D12 | N/A | not covered |
| D13 | 3 | semantic index |
| D14 | N/A | none |
| D15 | 6 | rule versioning |
| D16-D17 | 3 | Console, APIs |
| D18-D19 | 3 | roles unread |
| D20 | 7 | paper/vendor figures |
| D21 | 10 | evaluation licence |
| D22 | 3 | RDF formats |
| D23 | 5 | B/F published; patents unreviewed |
| D24 | App C | papers+docs |

## Appendix B. CAP mapping
| CAP | RDFox | CLAIM | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-02 | native | 03 | BL-06 | INTEGRATE | P3 |
| CAP-15 | native | 02 | BL-06 | INTEGRATE | P3 |
| CAP-22 | native | 03,07 | none (BL-30 partial) | EXPERIMENT | P1 |
| CAP-23 | partial (RL) | 03 | BL-30 | EXPERIMENT | P1 |
| CAP-24 | native | 03 | BL-39 partial | BUILD | P1 |

## Appendix C. Evidence
| CLAIM | version/date | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| rdfox-01 | 2024 | Samsung to acquire Oxford Semantic Technologies for personal knowledge graphs | Third-party report | https://www.thestack.technology/samsung-acquires-oxford-semantics/ | 2024-07-18 / 2026-10-26 | 0.7 | closing/continuity not stated |
| rdfox-02 | product page | Datalog/SWRL/OWL 2 RL/SHACL/SPARQL 1.1, incremental reasoning, HA, vendor rate claim, deployment modes | Officially documented (vendor claim for rate) | https://www.oxfordsemantic.tech/product | undated / 2026-10-26 | 0.6 | rate unverified |
| rdfox-03 | docs 7.x | incremental maintenance, explicit-only deletion, phases Mat/Addition/Deletion/BwdChain/RuleAdd, stratification, shortest proof | Officially documented | https://docs.oxfordsemantic.tech/reasoning.html | 2026-10-26 | 0.85 | algorithm not named |
| rdfox-04 | evaluation licence | evaluation only; no commercial use/distribution; benchmark publication needs approval | Officially documented | https://oxfordsemantic.tech/rdfox-evaluation-license | 2026-10-26 | 0.85 | production licence unseen |
| rdfox-05 | 7.7, 2026-09-29 (7.4-7.6) | release notes: selectivity-reordering planner, semantic index, federated SPARQL, Lucene/SQLite sources | Officially documented | https://docs.oxfordsemantic.tech/release-notes.html | 2026-09-29 / 2026-10-26 | 0.85 | none |
| rdfox-06 | docs 7.x | parallel store types, snapshot+delta persistence, dead-fact marking, exclusive compaction | Officially documented | https://docs.oxfordsemantic.tech/data-stores.html | 2026-10-26 | 0.8 | ACID unread |
| rdfox-07 | AAAI 2015 | B/F combines backward and forward chaining; far faster than DRed on some inputs, never significantly slower | Officially documented (peer-reviewed abstract) | https://ojs.aaai.org/index.php/AAAI/article/view/9409 | 2015 / 2026-10-26 | 0.85 | RDFox use of B/F not confirmed |
| rdfox-08 | ISWC 2015 | main-memory parallel store; 87x speed-up, 9.2B triples, 6.1M triples/s, 36.9 bytes/triple | Peer-reviewed (abstract via index) | https://www.cs.ox.ac.uk/people/boris.motik/pubs/npmhwb15RDFox-scalable.pdf | 2015 / 2026-10-26 | 0.7 | hardware atypical |

## Appendix D. Assumptions
Algorithm mechanics are background, not extracted from the PDF; B/F use is hypothesis.
