# C04 — JedAI (JedAI Toolkit, Java) and pyJedAI

| Field | Value |
|---|---|
| Registry ID | T-C04-jedai |
| Tier | B — ER toolkit, blocking-research reference for BL-36 |
| Versions examined | JedAI Toolkit (Java) release **3.2.1** (2021-08-27), last commit 2025-07-12 (dependabot); **pyJedAI 0.3.6** (PyPI and GitHub release 2025-11-03), last commit 2026-03-22 |
| Verified on | 2026-10-18 |
| Worker | V12 |

## 1. Identity, current status, tier, and sources
Two code bases from the University of Athens / NCSR Demokritos / SciFY group: the original Java **JedAIToolkit** (`github.com/scify/JedAIToolkit`; core library + GUI) and the Python re-implementation **pyJedAI** (`github.com/AI-team-UoA/pyJedAI`) [CLAIM-jedai-01][CLAIM-jedai-02]. Both Apache-2.0 [CLAIM-jedai-01][CLAIM-jedai-02]. Name collision: `scify/JedAI-core` and `ad-freiburg/jedai-core` are not valid repos (404). The registry means the toolkit family. Status: Java line is **maintenance-only** (last release 2021, dependency bumps in 2025); pyJedAI is **active** (0.3.6 in 2025-11, commits in 2026-03) [CLAIM-jedai-03]. Cross-reference: `C04-splink.md`, `C04-zingg.md`, `C04-senzing.md`.
Sources (5): both GitHub repos, Atom feeds, PyPI JSON, EDBT 2020 JedAI3 paper and PVLDB 2018 JedAI paper (found via search; content not opened, so paper claims are UNVERIFIED beyond title).

## 2. Primary problem, target workloads, concrete example workflows
Problem: end-to-end entity resolution with emphasis on scalable **blocking** and **meta-blocking** for noisy, heterogeneous (schema-agnostic) and RDF-like data. Workflow (JedAI model, recalled; conf 0.6): data reading -> block building -> block cleaning -> comparison cleaning (meta-blocking) -> entity matching -> entity clustering -> evaluation. pyJedAI states it handles structured and semi-structured data and uses supervised and unsupervised techniques including deep-learning/NLP for blocking and matching without labelled instances [CLAIM-jedai-02].

## 3. Feature inventory
| Feature | Status |
|---|---|
| Schema-agnostic blocking (token, n-gram, suffix variants) | present (Java; recalled, conf 0.6) |
| Block/comparison cleaning, meta-blocking | present (Java; recalled) |
| Entity matching + clustering library of algorithms | present |
| Desktop GUI (workflow wizard) | present (Java GUI) |
| Progressive / budget-aware ER (JedAI3) | present per EDBT 2020 title; details UNVERIFIED |
| Embeddings/DL-based blocking and matching | present in pyJedAI [CLAIM-jedai-02] |
| Server/API, multi-tenant, provenance | absent |
| Graph write-back | absent |

## 4. Architecture
```
sources -> data reader -> block building -> block cleaning -> comparison cleaning(meta-blocking)
        -> similarity/matching -> clustering -> clusters + evaluation (given ground truth)
(library / GUI; state = in-memory block collections; no service tier)
```

## 5. Under-the-hood reconstruction
Hypotheses (conf 0.5, from the published architecture): blocks keyed on tokens/n-grams inverted into entity-id lists; block purging/filtering drops oversized and low-value blocks; meta-blocking builds a weighted blocking graph (nodes = entities, edges = co-occurrence weighted by e.g. common-block count) and prunes low-weight edges before pairwise comparison; matching computes attribute-agnostic similarity; connected-components or related clustering. No storage, transactions or security. Pseudocode: `for token t: B[t].add(e)`; `edge(a,b).w = |blocks(a) ∩ blocks(b)|`; `keep edges with w >= mean`. This is a re-implementation sketch, not a source reading (source not opened in this pass).

## 6. Requirements inferred
Blocking must be schema-agnostic and tunable for recall vs candidate count; evaluation harness (precision, recall, pair completeness, reduction ratio) built in. EOIP lesson: any BL-36 solution needs blocking diagnostics, not only a matcher.

## 7. Performance and resource model
No numbers verified. Cost is dominated by candidate comparisons after blocking; meta-blocking exists precisely to reduce them. Failure mode: huge blocks from frequent tokens (supernode analogue). pyJedAI neural components may need PyTorch and, optionally, GPU (not stated) [CLAIM-jedai-02].

## 8. Strengths
| ID | Strength | Match/exceed |
|---|---|---|
| STR-jedai-01 | Schema-agnostic blocking + meta-blocking suited to heterogeneous JSON/RDF | BUILD blocking diagnostics (pair completeness, reduction ratio) around Splink/Zingg blocking |
| STR-jedai-02 | Evaluation metrics for blocking quality | Adopt in 15-VALIDATION plan |
| STR-jedai-03 | Progressive ER (budget-aware) for first answers fast | EXPERIMENT for review-queue prioritisation |

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | Meta-blocking quality depends on weighting scheme; no calibrated probabilities (hypothesis) |
| Operational | Java line stale releases (2021); pyJedAI is 0.x |
| Developer friction | Not a service; no provenance or merge/split semantics |
| Licensing | Apache-2.0, none |
INV-jedai-01: *Target* pyJedAI 0.3.6. *Limitation:* produces clusters, not auditable merge/split events. *Root cause* semantics/governance (hypothesis). *Options:* (a) use as offline blocking evaluator; (b) emit candidate pairs into BL-35 queue with score+method tags; (c) own blocking service. *Selected:* (b). *POC:* DBLP-ACM and a synthetic JSON export; success = pair completeness ≥ 0.98 with reduction ratio ≥ 0.95 versus Splink default rules. *Decision:* EXPERIMENT. No master-prompt seed hypothesis targets JedAI.

## 10. Deployment, licensing, viability
Library/GUI, Apache-2.0, offline, JVM or Python. Embeddable via subprocess or Python import. No legal trigger (patents not checked; UNVERIFIED).

## 11. Competitive delta vs EOIP baseline
EOIP has no blocking (BL-34 states "no blocking, no probabilistic ER"; BL-36 absent). JedAI shows the missing blocking layer; adopting Splink/Zingg covers matching, JedAI contributes diagnostic methodology.

## 12. Cards
STR-jedai-01..03 (§8); INV-jedai-01 (§9).

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| Blocking (CAP-31) | REUSE Splink/Zingg blocking; EXPERIMENT pyJedAI meta-blocking as evaluator |
| Blocking diagnostics | BUILD |
| Progressive ER | DEFER |
| GUI | REJECT |

## 14. Tests and acceptance
Run pyJedAI and Splink blocking on the same 3 datasets; record pair completeness, reduction ratio, wall clock and RAM; accept if diagnostics can be implemented as a library-agnostic report.

## 15. Risks and open questions
Java toolkit abandonment risk; does meta-blocking help over Splink's deterministic rules on JSON-derived entities; paper claims unverified.

## Appendix A — Research-dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Apache-2.0; Java maintenance, Python active |
| D2 | 2 | ER blocking/matching |
| D3 | 4 | library pipeline |
| D4–D8 | N/A | no storage/query/reasoning/transactions |
| D9 | 2 | batch readers |
| D10 | 2,5 | ER core; no source authority |
| D11 | N/A | |
| D12 | 3 | embeddings in pyJedAI |
| D13–D14 | N/A | |
| D15 | N/A | |
| D16 | 3 | Java GUI |
| D17 | 3 | Java/Python APIs |
| D18–D19 | N/A | |
| D20 | 7 | no numbers |
| D21 | 10 | Apache-2.0 |
| D22 | 10 | file formats unverified |
| D23 | 10 | patents UNVERIFIED |
| D24 | 1,5 | paper content unopened; conf 0.5 |

## Appendix B — Capability mapping
| CAP | Tech | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-31 | native (blocking, matching, clustering) | jedai-02 | BL-36 absent | EXPERIMENT | P2 |
| CAP-78 | partial (ER metrics) | jedai-02 | none | BUILD | P2 |

## Appendix C — Evidence records
| CLAIM | product/version/date | claim | class | source | dates | conf | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-jedai-01 | JedAIToolkit 3.2.1 | Apache-2.0 licence; release 2021-08-27; last commit 2025-07-12 | Officially documented | https://github.com/scify/JedAIToolkit (LICENSE, releases.atom, commits.atom) | 2026-10-18 | 0.9 | none |
| CLAIM-jedai-02 | pyJedAI 0.3.6 | Apache-2.0; structured and semi-structured data; supervised/unsupervised; DL/NLP for blocking and matching without labels; Python 3.8+ | Officially documented | https://github.com/AI-team-UoA/pyJedAI | 2026-10-18 | 0.85 | none |
| CLAIM-jedai-03 | pyJedAI 0.3.6 | PyPI 0.3.6 uploaded 2025-11-03; commit 2026-03-22 | Officially documented | https://pypi.org/project/pyjedai/ ; releases.atom | 2026-10-18 | 0.9 | none |
| CLAIM-jedai-04 | JedAI 2018/2020 | Papers exist: PVLDB 2018 "JedAI", EDBT 2020 "JedAI3" (budget-agnostic and budget-aware workflows) | Third-party report (search snippet) | https://helios2.mi.parisdescartes.fr/~themisp/publications/edbt20-jedai3.pdf | 2026-10-18 | 0.6 | content not opened |

## Appendix D — Assumptions
Pipeline stages and meta-blocking mechanics are from general knowledge of the JedAI papers, not source inspection; flagged hypothesis.
