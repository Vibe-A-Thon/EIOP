# C04 — Dedupe (dedupeio/dedupe, DataMade)

| Field | Value |
|---|---|
| Registry ID | T-C04-dedupe |
| Tier | B — Python active-learning dedupe; reference for human-in-the-loop labelling and learned blocking (BL-36 absent, BL-35 partial) |
| Versions examined | Dedupe **3.0.3** (GitHub release and PyPI 2024-08-15); latest commit seen on `master` 2025-07-29 (CI bot workflow only) |
| Verified on | 2026-10-18 |
| Worker | V12 |

## 1. Identity, current status, tier, and sources
Python library for fuzzy matching, deduplication and record linkage using supervised ML with human labels [CLAIM-dedupe-01]. Authors Forest Gregg and Derek Eder (DataMade); a separate commercial Dedupe.io service exists [CLAIM-dedupe-01]. Licence MIT [CLAIM-dedupe-02]. Status: **low activity**. The last release is 3.0.3 (2024-08-15); the only 2025 commit is a CI workflow edit; 78 open issues [CLAIM-dedupe-01][CLAIM-dedupe-03]. Not archived. Sibling ER deep dives: `C04-splink.md` (unsupervised Fellegi-Sunter, SQL backends), `C04-zingg.md` (Spark ML), `C04-senzing.md` (embeddable engine). Not duplicated here.
Sources (4): GitHub repo page, releases/commits Atom feeds, PyPI JSON, LICENSE file. The docs page `docs.dedupe.io/.../How-it-works.html` returned 404, so algorithm details below are marked as recalled from the project's published design and carry confidence 0.5.

## 2. Primary problem, target workloads, concrete example workflows
Problem: dedupe or link tabular records without a shared key when you can label a few dozen pairs. Workloads: single-machine, in-memory, tens of thousands to low millions of records (scale limit is a hypothesis from the in-memory design, not measured here).
Workflow: define fields and comparator types; `prepare_training`; interactive `console_label` of uncertain pairs (active learning); `train`; `partition` with a threshold to get clusters; persist settings/training files.

## 3. Feature inventory
| Feature | Status | Note |
|---|---|---|
| Active learning labelling (CLI console) | present | human-in-the-loop [CLAIM-dedupe-01] |
| Learned blocking predicates | present (hypothesis: from design papers, conf 0.5) | |
| Field comparators (string, text, price, datetime via add-on) | present | |
| Clustering of pair scores | present | |
| Linking two datasets (gazetteer/record link) | present | |
| Web UI | absent in OSS | DataMade/Dedupe.io service is separate [CLAIM-dedupe-01] |
| Distributed/Spark/SQL execution | absent | single-process |
| Explainable per-field scores | partial | model weights inspectable; no Splink-style waterfall |
| Incremental/streaming match | partial/unknown | NOT PUBLICLY VERIFIED in this pass |

## 4. Architecture
```
records(dict) -> [prepare_training: sample pairs] -> [active learner <-> human labels]
   -> logistic-regression-style classifier + learned blocking predicates (settings file)
   -> block -> compare candidate pairs -> score -> hierarchical clustering -> (cluster_id, confidence)
state: in-process memory; settings + training JSON on disk
```

## 5. Under-the-hood reconstruction
Data model: list/dict of records keyed by id; per-field variable definitions. Pipeline (design hypothesis, conf 0.5): (1) generate candidate pairs from sampled data; (2) active learner picks uncertain pairs to label; (3) learn a classifier over field-distance features; (4) learn a covering set of blocking predicates (e.g., first-N chars, token, n-gram) that keeps recall on labelled duplicates while minimising candidate pairs; (5) score blocked pairs; (6) cluster. No transactions, partitioning or caching; state is a settings file. Security: none (library).

## 6. Requirements inferred
FR: label-efficient training; learned blocking; threshold-tuned clustering. NFR: reproducible settings artefact; pure Python deployable offline. Lesson for EOIP: label store with provenance, uncertain-pair queue (maps to BL-35 review queue).

## 7. Performance and resource model
No benchmark verified. Complexity driven by blocking selectivity and in-memory pair scoring. Failure mode: poor predicates produce quadratic candidate pairs; memory exhaustion at scale (hypothesis). No numbers asserted.

## 8. Strengths
| ID | Strength | How to match/exceed |
|---|---|---|
| STR-dedupe-01 | Active learning needs few labels (design claim) | Reviewer queue ranked by model uncertainty feeding BL-35 |
| STR-dedupe-02 | Learned blocking rather than hand-written rules | Splink/Zingg REUSE for blocking; keep learner pluggable |
| STR-dedupe-03 | MIT, tiny dependency footprint | Embed as optional extra |

## 9. Limitations with root causes
| Class | Item |
|---|---|
| Algorithmic | Single-machine in-memory design limits scale (hypothesis); no probabilistic m/u interpretability |
| Operational | Low maintenance cadence since 2024-08 (verified); no server/UI in OSS |
| Developer friction | Interactive console labelling is not an API workflow; label governance absent |
| Licensing | None (MIT) |

INV-dedupe-01: *Target* dedupe 3.0.3 on enterprise records. *Limitation:* console-only labelling, no governance of labels. *Root cause* UX/governance (hypothesis). *Options:* (a) wrap `dedupe` behind a job API; (b) native label service with tenant-scoped, audited labels feeding any matcher; (c) active-learning layer over Splink/Zingg scores. *Selected:* (b) pattern: `UncertainPairQueue -> reviewer decision (CuratedEdge) -> training set version`. *POC:* 3 public ER benchmarks, labels-to-F1 curve vs Splink with random labels; success = ≥ equal F1 with ≤ 50% labels. *Security:* labels inherit source ACLs; PII in pairs shown only to authorised reviewers. *Defensibility:* label provenance and reviewer workflow integrated with graph governance. *Decision:* EXPERIMENT. Master-prompt seed hypotheses do not target Dedupe; none validated or rejected.

## 10. Deployment, licensing, viability
pip-installable, MIT, air-gap viable (no network). Not a service. Redistribution-safe. No legal trigger.

## 11. Competitive delta vs EOIP baseline
BL-36 absent (probabilistic ER), BL-34 deterministic person-only, BL-35 partial review queue. Dedupe adds learned blocking and active learning, none present in EOIP. Prefer Splink/Zingg as the matcher; take Dedupe's active-learning pattern only.

## 12. Strength-adoption and inversion cards
See §8 (STR-dedupe-01..03) and INV-dedupe-01 (§9).

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| Probabilistic matcher (CAP-31) | REJECT Dedupe as the engine; REUSE Splink/Zingg |
| Active-learning label loop (CAP-31) | BUILD (pattern) |
| Learned blocking (CAP-31) | EXPERIMENT |

## 14. Tests and acceptance
Reproduce on a public benchmark (e.g., Magellan/DBLP-ACM datasets) with 20/50/100 labels; compare F1 and wall clock; acceptance: documented label-efficiency curve and a go/no-go for the active-learning loop.

## 15. Risks and open questions
Maintenance stall; unverified scale ceiling; whether active-learning ordering transfers to Fellegi-Sunter scores.

## Appendix A — Research-dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | MIT, DataMade, low activity |
| D2 | 2 | tabular dedupe |
| D3 | 4 | library, single process |
| D4 | N/A | no storage layer |
| D5 | N/A | no schema/ontology |
| D6 | 5 | blocking+scoring pipeline |
| D7 | N/A | no reasoning |
| D8 | 7 | single process; no transactions |
| D9 | 2,3 | batch ingest from dict records |
| D10 | 2,5,8 | core: ER, clustering; no source authority |
| D11 | N/A | no time model |
| D12 | 5 | classical ML only |
| D13 | N/A | |
| D14 | N/A | |
| D15 | 8,9 | labelling workflow |
| D16 | 3 | CLI only |
| D17 | 3 | Python API |
| D18 | N/A | library |
| D19 | N/A | |
| D20 | 7 | no verified numbers |
| D21 | 1,10 | MIT + separate paid service |
| D22 | 10 | JSON settings |
| D23 | N/A | no patents identified (not searched) |
| D24 | 1 | docs 404; 0.5 confidence on internals |

## Appendix B — Capability mapping
| CAP | This technology | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-31 | native | dedupe-01 | BL-36 absent, BL-35 partial | EXPERIMENT (pattern) | P2 |
| CAP-30 | absent | dedupe-01 | BL-34 implemented | REJECT | P3 |

## Appendix C — Evidence records
| CLAIM | product/version/date | claim | class | source | dates | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-dedupe-01 | dedupe/3.0.3 | ML fuzzy matching/dedupe/ER from human training data; DataMade authors; Dedupe.io separate service; 78 open issues | Officially documented | GitHub dedupeio/dedupe https://github.com/dedupeio/dedupe | n/a / 2026-10-18 | 0.9 | none |
| CLAIM-dedupe-02 | master | MIT licence, Copyright 2014 Gregg, Eder, DataMade | Officially documented | LICENSE https://github.com/dedupeio/dedupe/blob/master/LICENSE | 2026-10-18 | 0.95 | none |
| CLAIM-dedupe-03 | 3.0.3 | latest release 2024-08-15; latest commit 2025-07-29 | Officially documented | releases.atom / commits.atom https://github.com/dedupeio/dedupe/releases.atom | 2026-10-18 | 0.9 | PyPI agrees (3.0.3, 2024-08-15) |
| CLAIM-dedupe-04 | 3.0.3 | internals (learned predicates, regularised classifier, clustering) | Reasoned inference | project design; docs page 404 | 2026-10-18 | 0.5 | none |

## Appendix D — Assumptions
Active learning and blocking internals taken from the project's published design (not re-verified); "low activity" judged from release/commit dates only.
