# C04 — JSON/CSV schema inference and automatic entity/relationship detection tools

| Field | Value |
|---|---|
| Registry ID | T-C04-schema-inference |
| Tier | B — directly relevant to journey J12 (arbitrary JSON onboarding), BL-26, BL-27 |
| Versions examined | GenSON **1.4.0** (2026-07-06); quicktype **26.0.0** (2026-07-20); datamodel-code-generator **0.86.0** (2026-10-18); Frictionless (Python) **5.21.0** (2026-10-15); ydata-profiling **4.18.4** (2026-04-22); DuckDB **2.0.0** (2026-10-21; CSV sniffer); csvkit **2.2.0** (2025-12-15); Pandera **0.35.0** (2026-10-25); Sherlock (MIT, KDD 2019); Auto-BI (VLDB 2023); Baazizi et al. (VLDB J. 2019) |
| Verified on | 2026-10-18 |
| Worker | V12 |

## 1. Identity, current status, tier, and sources
Grouped category record. Members (all verified 2026-10-18 unless stated):
| Function | Tool | Licence | Status |
|---|---|---|---|
| JSON to JSON Schema | GenSON | MIT | 1.4.0, 2026-07 [CLAIM-si-01] |
| JSON/Schema to typed code | quicktype; datamodel-code-generator | Apache-2.0; MIT | 26.0.0 2026-07; 0.86.0 2026-10 [CLAIM-si-02][CLAIM-si-03] |
| Table descriptors, validation, profiling | Frictionless, Pandera, ydata-profiling | MIT, MIT, UNVERIFIED (blank metadata) | active [CLAIM-si-03] |
| CSV sniffing | DuckDB `sniff_csv`, csvkit | MIT | active [CLAIM-si-03] |
| Semantic column typing | Sherlock (78 DBpedia types, F1 0.89 reported) | repo licence UNVERIFIED | research [CLAIM-si-04] |
| Massive-JSON inference | Baazizi et al., VLDB J. 2019 | n/a | research [CLAIM-si-05] |
| Join discovery | Auto-BI (VLDB 2023); Metanome (last release 2016) | n/a; UNVERIFIED | research [CLAIM-si-06][CLAIM-si-07] |
Cross-refs: `C04-rml-tools.md`, `C04-ontology-alignment.md`, `C04-openrefine.md`.

## 2. Primary problem, workloads, workflows
Given unknown records, infer types, nullability, keys, enums, nesting, formats, and likely relationships; then propose an ontology. Journey J12: unknown JSON export -> auto-detect entities/relationships -> propose ontology extension -> review -> ingest with provenance.

## 3. Feature inventory (category vs EOIP)
| Capability | Best in category | EOIP `ingest/profile.py` |
|---|---|---|
| Union/optional types, JSON Schema output | GenSON, quicktype | partial: observed_types, no Schema emission |
| Formats, cardinality, enums | ydata-profiling, Frictionless | yes (11 formats; cap 10,000 distinct) |
| Streaming, bounded memory, determinism | Baazizi (Spark) | yes |
| Drift, key candidates with stability | Metanome-style | yes (`diff_profiles`, `detect_key_candidates`) |
| Explicit FK-like relationships | heuristics | yes (5 signals, edge-class tagging) |
| Statistical inclusion discovery | Auto-BI, Metanome | partial: MinHash bands in `graphbuild/dependencies.py` (64 hashes, 16 bands, containment >= 0.8); profile.py defers SR-ING-014 |
| Semantic column typing | Sherlock | absent |
| Ontology proposal from structure | none mature | partial: `graphbuild/schema.py::induce_schema` |

## 4. Architecture
```
records -> profiler (types, nullability, cardinality, formats, nesting) -> key candidates
        -> relationship candidates (explicit rules -> statistical joins -> learned ranker)
        -> schema/ontology proposal (entity types, properties, relations, SHACL) -> HUMAN REVIEW -> gated promotion -> ingest w/ provenance
```

## 5. Under-the-hood reconstruction
GenSON: per-record schemas merged by a commutative union (type sets, `required` intersection, `anyOf` on conflicts; hypothesis conf 0.6). Baazizi: values map to types fused under a parameterised equivalence, commutative and associative so it parallelises [CLAIM-si-05]. Sherlock: 1,588 column features into a multi-input network [CLAIM-si-04]. Auto-BI: local join classifier then global k-MCA selection [CLAIM-si-06]. EOIP: single-pass accumulators, SHA-256 value hashes, sorted deterministic output, `urn:eoip:ingest:profile:<slug>` IDs. Risk: PII in sample values (EOIP keeps up to 5; masking not checked).

## 6. Requirements inferred (for J12)
Deterministic, streaming, bounded-memory profile; schema merge semantics (commutative); precision knob; statistical join discovery with calibrated confidence and explanation; human-reviewed proposals; PII-safe samples; drift between loads; edge provenance classes.

## 7. Performance and resource model
No benchmarks verified by us. Reported: Auto-BI sub-second for ~100 tables [CLAIM-si-06]; Baazizi scale via Spark [CLAIM-si-05]. EOIP's profiler is single-process Python (Pydantic) with an exact-set cardinality cap, so huge inputs trade exactness for lower bounds (documented in code). Failure modes: heterogeneous arrays, polymorphic fields, sampled profiles missing rare types.

## 8. Strengths
| ID | Strength | Match/exceed |
|---|---|---|
| STR-si-01 | Commutative schema fusion with a precision knob (Baazizi, GenSON) | BUILD: emit JSON Schema 2020-12 from `ProfileReport` with mergeable partial profiles |
| STR-si-02 | Global optimisation of joins (Auto-BI) reduces false relationships | EXPERIMENT for SR-ING-014 |
| STR-si-03 | Learned semantic column types (Sherlock) | DEFER; rules-first, optional local model |
| STR-si-04 | Code/pydantic generation from schema (quicktype, datamodel-code-generator) | INTEGRATE for SDK stubs |
| STR-si-05 | Validation-as-contract (Frictionless/Pandera) | REUSE ideas for data contracts |

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | open tools stop at types; relationship discovery is research-grade |
| Operational | Metanome stale [CLAIM-si-07]; ydata licence unclear |
| Friction | outputs are schemas or reports, not governed ontology deltas |
INV-si-01: *Limitation:* no governed entity/relationship proposals with evidence. *Root cause:* governance/semantics (proven by tool scope). *Options:* (a) wrap GenSON; (b) wire existing `induce_schema` and `discover_inclusion_dependencies` into review and promotion via `ontology/gitops.py`, adding global join selection; (c) learned ranker. *Selected:* (b), later (c). *POC:* 5 public multi-table datasets; key/FK precision-recall, reviewer acceptance, 100% determinism. *Decision:* ADOPT (b). No seed hypothesis targets this category.

## 10. Deployment, licensing, viability
All Python/Node libraries, permissive where verified, offline, one-node friendly. Check ydata-profiling and Metanome licences before any embedding (UNVERIFIED). No copyleft found among verified members.

## 11. Competitive delta vs EOIP baseline (BL-26, BL-27)
BL-26 (`profile.py`, 1,023 lines, plus `graphbuild`) exceeds every open tool here on the J12 spec: deterministic, streaming, formats, key stability, drift, five explicit relationship signals, ASSERTED/INFERRED tagging. Gaps: no JSON Schema emission or mergeable partial profiles; no global join optimisation or learned ranker; no learned column typing; `object_fields` one level; cardinality is a lower bound past 10,000. BL-27: the baseline cites `moonshot/ontology_induction.py`, which is the text/LLM path (`CorpusOntologyInducer.induce(texts)`, `LocalOllamaProvider`) and has no inbound references in `packages/eoip` (grep). The structured path is `graphbuild/schema.py::induce_schema(ProfileReport)` (ProposedClass/ProposedProperty, `required` from null counts, profile evidence) plus `graphbuild/enrichment.py` review items; the baseline under-describes it. Unverified: end-to-end review, approval and promotion from `InducedSchema` through `gitops.py`.

## 12. Cards
STR-si-01..05; INV-si-01.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| Profiling and keys (CAP-28) | BUILD (keep native) |
| JSON Schema emission (CAP-08) | BUILD; GenSON as differential oracle |
| Statistical relationships (CAP-28) | EXPERIMENT (Auto-BI style) |
| Proposal governance wiring (CAP-41) | BUILD |
| Learned column typing | DEFER |
| SDK code generation | INTEGRATE |
| Metanome | REJECT |

## 14. Tests and acceptance
Differential test: GenSON schema vs EOIP-emitted schema on a corpus (no accepted value rejected); FK discovery P/R on 5 datasets; fusion associativity property test (shuffled chunks yield identical report); PII masking test on samples; J12 end-to-end test with reviewer approval.

## 15. Risks and open questions
Heuristic false relationships; polymorphic arrays; privacy of profile samples; whether statistical joins stay deterministic; licence of ydata-profiling and Sherlock repo.

## Appendix A — Research-dimension coverage
| Dimension | Covered in | Summary or N/A reason |
|---|---|---|
| D1, D21 | 1,10 | mostly permissive, some licences unverified |
| D2-D3 | 2,4 | J12 pipeline |
| D4,D6,D7,D8,D13,D14,D16,D19,D23 | N/A | profiling libraries: no storage, query, reasoning, retrieval or UI; patents not searched |
| D5,D22 | 3,8 | JSON Schema typing and interop |
| D9,D10 | 3,5 | core: schema, key and relationship inference |
| D11 | 3 | drift diff |
| D12 | 5 | Sherlock |
| D15 | 4,9 | proposal review gap |
| D17 | 8 | code generation |
| D18 | 5 | PII in samples |
| D20,D24 | 7 | reported only; papers at abstract level |

## Appendix B — Capability mapping
| CAP | Tech | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-28 | partial across tools; EOIP native | si-01..06 | BL-26 implemented, BL-27 partial | BUILD/EXPERIMENT | P1 |
| CAP-08 | partial (JSON Schema) | si-01 | BL-28 | BUILD | P2 |
| CAP-41 | absent | si-02 | BL-32 partial | BUILD | P1 |

## Appendix C — Evidence records
| CLAIM | product/version/date | claim | class | source | dates | conf | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-si-01 | GenSON 1.4.0 | MIT; JSON Schema generator; 2026-07-06 | Officially documented | https://pypi.org/project/genson/ | 2026-10-18 | 0.9 | none |
| CLAIM-si-02 | quicktype 26.0.0 | Apache-2.0; 2026-07-20 | Officially documented | https://github.com/quicktype/quicktype | 2026-10-18 | 0.9 | none |
| CLAIM-si-03 | package set | versions and licences from metadata | Officially documented | https://pypi.org/pypi/PKG/json | 2026-10-18 | 0.85 | ydata blank |
| CLAIM-si-04 | Sherlock KDD 2019 | 686,765 columns, 78 types, F1 0.89 | Third-party report | https://sherlock.media.mit.edu | 2026-10-18 | 0.8 | author-reported |
| CLAIM-si-05 | VLDB J. 28(4) | parametric parallel JSON inference | Third-party report | https://researchportal.ip-paris.fr/en/publications/parametric-schema-inference-for-massive-json-datasets/ | 2026-10-18 | 0.85 | none |
| CLAIM-si-06 | PVLDB 16(10) | Auto-BI k-MCA, F1 > 0.9 | Third-party report | https://www.vldb.org/pvldb/vol16/p2578-he.pdf | 2026-10-18 | 0.8 | author benchmark |
| CLAIM-si-07 | Metanome 1.0.0 | release 2016-01-20, commit 2025-06-05 | Officially documented | https://github.com/HPI-Information-Systems/Metanome | 2026-10-18 | 0.7 | licence unchecked |
| CLAIM-si-08 | EOIP HEAD | profile.py, graphbuild/schema.py, dependencies.py, ontology_induction.py as described | Observed in source code | packages/eoip/ingest, graphbuild, moonshot | 2026-10-18 | 0.9 | review wiring not traced |

## Appendix D — Assumptions
GenSON merge mechanics and Metanome algorithms are general knowledge (hypotheses); governance wiring from InducedSchema to gitops was not traced.
