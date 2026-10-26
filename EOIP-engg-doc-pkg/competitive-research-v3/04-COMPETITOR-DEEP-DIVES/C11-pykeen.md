# C11 — PyKEEN

| Field | Value |
|---|---|
| Registry ID | T-C11-pykeen |
| Tier | B — the reference KG-embedding (KGE) library; supplies the evaluation discipline for CAP-63. |
| Versions examined | `pykeen` 1.11.1 (PyPI and GitHub release, 2025-04-24); repository activity to 2026-10-23 |
| Verified on | 2026-10-18 (brief date); web sources fetched 2026-10-26 (session clock) |
| Worker | V24 (assigned as W24) |

## 1. Identity, current status, tier, sources
| Item | Finding |
|---|---|
| What | PyTorch library to train and evaluate knowledge graph embedding models [CLAIM-pykeen-01] |
| Owner | `pykeen` GitHub organisation; academic team (Ali et al.); funders listed on README include DFG, DARPA, BMBF [CLAIM-pykeen-01] |
| Licence | MIT, copyright "2019-2024 PyKEEN Project Team" [CLAIM-pykeen-02] |
| Release | 1.11.1 on 2025-04-24; last commit entry 2026-10-23. Releases are 18 months old while `master` is alive [CLAIM-pykeen-02] |
| Python / torch | PyPI `>=3.10`, `torch>=2.0`, numpy, scipy, scikit-learn, optuna, pandas, class_resolver, pystow [CLAIM-pykeen-02]. README says latest stable needs 3.11+ (conflicts with PyPI; unresolved) |
| Status | active, low release cadence |
| Scale | README counts: 40 models, 37 datasets, 5 inductive datasets, 15 losses, 40 metrics [CLAIM-pykeen-01] |

## 2. Problem, workloads, workflows
Link prediction in a fixed-vocabulary KG: train TransE/ComplEx/RotatE/R-GCN/CompGCN; rank candidate tails with filtered rank metrics. EOIP workflow: score candidate missing edges in the prediction plane (J8) and compare architectures in a bake-off.

## 3. Feature inventory
| Feature | Status | Evidence |
|---|---|---|
| 40 models incl. R-GCN, CompGCN (typed relations) | present | [CLAIM-pykeen-01] |
| Rank-based, sampled rank, classification, OGB evaluators; filtered evaluation | present | [CLAIM-pykeen-03] |
| Inductive link prediction (NodePiece variants) | present, 2 models | [CLAIM-pykeen-01] |
| HPO via Optuna; ablation and `experiments reproduce` CLI | present | [CLAIM-pykeen-01] |
| Trackers: MLflow, TensorBoard, W&B, CSV, JSON | present | [CLAIM-pykeen-01] |
| Triple leakage tooling (`Sealant`, `pykeen.triples.leakage`) | present | [CLAIM-pykeen-03] |
| Calibration | absent (only an "Uncertainty" reference page; no calibrators named) | [CLAIM-pykeen-03] |
| Explainability | absent | [CLAIM-pykeen-03] |
| Temporal KGs | absent | [CLAIM-pykeen-03] |
| Automatic memory optimisation | present | [CLAIM-pykeen-03] |
| Server / UI / registry | absent (CLI only) | — |

## 4. Architecture
```
TriplesFactory (id-mapped triples, splits) -> Model(Representations + Interaction)
  -> TrainingLoop (sLCWA/LCWA) <- NegativeSampler, Loss, Regularizer
  -> Evaluator (filtered ranks) -> Tracker; HPO pipeline wraps all
```
All state lives in the process and local files.

## 5. Under-the-hood reconstruction
Composition pattern: a model is `Representation` modules plus an `Interaction` function scoring (h,r,t); `class_resolver` registries make each part swappable by name (documented; code paths not opened this run). Training uses sLCWA (sampled negatives) or LCWA (score all tails). Evaluation ranks the true entity among all candidates, optionally filtering other known true triples (`pykeen.sampling.filtering`). Fixed entity/relation vocabularies mean a new entity cannot be scored without retraining, except in NodePiece inductive models (hypothesis: anchor-based tokenisation).

## 6. Requirements inferred
FR: per-entity vocabulary, filtered evaluation, reproducible configs. NFR: deterministic seeds, batch-size autotuning to avoid OOM, export of config with every score.

## 7. Performance and resource model
No benchmark run here. The authors' large-scale study (TPAMI 2021) is the public evidence; its results were not re-extracted [CLAIM-pykeen-04]. CPU suitability is plausible (pure PyTorch) but not measured; memory scales with entities x embedding dimension.

## 8. Strengths
Wide model zoo under one API; evaluation discipline; reproducibility CLI; MIT. Match: wrap evaluator and leakage checks as EOIP's KGE bake-off harness.

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | transductive by default; temporal and heterogeneous-attribute data ignored |
| Governance gap | no calibration, no explanations, no provenance |
| Friction | Python-version statement inconsistent between README and PyPI; torch-geometric not used |
| Cadence | one release in 18 months |

## 10. Deployment, licensing, operations
MIT, library-only, offline-capable, CPU torch works under ADR-H16 (no nvidia packages needed by its declared dependencies). Adds optuna, pandas, pystow (pystow downloads data on demand: must be disabled air-gapped). No legal trigger.

## 11. Delta versus baseline
BL-44 is heuristic-only; BL-57 plans N1 with PyG, which has its own `kge` module (TransE, ComplEx, DistMult, RotatE, see C11-pyg). PyKEEN adds more models, filtered and sampled evaluators, and ablation tooling that PyG lacks. Neither gives calibration or provenance; EOIP must build both.

## 12. Cards
STR-pykeen-01 | PyKEEN | filtered rank metrics + leakage tooling | [CLAIM-pykeen-03] | prevents inflated link-prediction claims | match | build EOIP evaluator with filtered ranks and a leakage gate | accepted when inverse-relation leakage injected in a test set is detected.
INV-pykeen-01 | PyKEEN 1.11.1 | scores uncalibrated and unexplained | [CLAIM-pykeen-03] | root cause: scope (proven absent) | Option 1: post-hoc isotonic/Platt on held-out ranks; 2: native calibrator in prediction plane; 3: calibrated, evidence-attached suggestions. Selected 2. Benchmark: ECE on FB15k-237-like split <= agreed threshold vs raw scores. Falls apart if calibration set leaks. Defensibility: calibrated scores tied to provenance. Decision: EXPERIMENT. (Seed hypotheses not targeted.)

## 13. Per-capability decisions
CAP-63 embeddings: EXPERIMENT as offline bake-off tool, not a runtime dependency. CAP-64: REUSE evaluator design. CAP-78: REUSE protocols.

## 14. Tests
Train TransE and RotatE on an EOIP tenant sample on the CPU reference; compare filtered MRR/Hits@10; confirm no network calls; confirm model file loads under hash-locked deps.

## 15. Risks
Release stagnation; Python-version inconsistency; unverified CPU throughput; model files are pickle-based torch artefacts (hypothesis).

## Appendix A — Dimension coverage
| Dimension | Sections | Summary |
|---|---|---|
| D1-D8 identity to temporal | 1,3,5 | library; temporal absent |
| D9-D12 governance, security | 3,10 | none provided |
| D13-D16 retrieval, ML | 2,3,8 | KGE core |
| D17-D20 ops, perf | 7,10 | unmeasured |
| D21-D24 licence, maturity | 1,10,15 | MIT, active |

## Appendix B — Capability mapping
| CAP | Technology | Claim | Baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-63 | native | CLAIM-pykeen-01 | none | EXPERIMENT | P2 |
| CAP-64 | partial | CLAIM-pykeen-03 | BL-44 Partial | REUSE evaluator design | P2 |
| CAP-78 | partial | CLAIM-pykeen-04 | none | REUSE | P2 |
| CAP-43 | absent | CLAIM-pykeen-03 | BL-40 Partial | BUILD | P1 |

## Appendix C — Evidence
| CLAIM | product/date | claim | class | source | access | conf. | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-pykeen-01 | repo README | 40 models, 37 datasets, 5 inductive, 15 losses, 40 metrics, Optuna, trackers, funders | vendor doc | github.com/pykeen/pykeen | 2026-10-26 | 0.8 | none |
| CLAIM-pykeen-02 | PyPI + releases feed | 1.11.1 on 2025-04-24; MIT; `>=3.10`; torch>=2.0; commits to 2026-10-23 | primary | pypi.org/pypi/pykeen/json; github.com/pykeen/pykeen/releases.atom, commits.atom | 2026-10-26 | 0.85 | README says Python 3.11+ |
| CLAIM-pykeen-03 | docs | filtered evaluation, `Sealant`/leakage module, "Uncertainty" page, no calibration/explainability/temporal | vendor doc | pykeen.readthedocs.io/en/stable | 2026-10-26 | 0.6 | docs index only; subpages unread |
| CLAIM-pykeen-04 | paper | Ali et al., "Bringing Light Into the Dark", TPAMI 2021, benchmark code at github.com/pykeen/benchmarking | peer-reviewed | cited by README | 2026-10-26 | 0.7 | paper itself not read |

## Appendix D — Assumptions
Docs subpages were not opened; absence claims mean "not found on the index page". Access date follows the session clock.
