# C11 — ULTRA (knowledge graph foundation model)

| Field | Value |
|---|---|
| Registry ID | T-C11-ultra |
| Tier | B — research artefact for zero-shot inductive link prediction; no package, no releases. |
| Versions examined | repo `DeepGraphLearning/ULTRA` `main` (18 commits; newest commit entry 2025-02-03); checkpoints `ultra_3g`, `ultra_4g`, `ultraquery` |
| Verified on | 2026-10-18 (brief date); web sources fetched 2026-10-26 (session clock) |
| Worker | V24 (assigned as W24) |

## 1. Identity, current status, tier, sources
| Item | Finding |
|---|---|
| What | A single pre-trained model for link prediction on any multi-relational graph; it learns relation representations from a graph of relations, not per-graph embeddings. UltraQuery extends it to complex logical queries [CLAIM-ultra-01] |
| Owner | Authors Galkin, Yuan, Mostafa, Tang, Zhu (DeepGraphLearning group); ICLR 2024 (arXiv:2310.04562); NeurIPS 2024 (arXiv:2404.07198) [CLAIM-ultra-01] |
| Licence | MIT for code [CLAIM-ultra-01]. Checkpoint licence not separately stated: UNVERIFIED |
| Release | No tagged release, not on PyPI (lookup returned nothing). Last commit 2025-02-03 [CLAIM-ultra-02] |
| Size | 6-layer GNN, 64 dims, about 168k parameters, checkpoints about 2 MB; 4g trained on FB15k237, WN18RR, CoDExMedium, NELL995 [CLAIM-ultra-01] |
| Requirements | README: Python 3.9, PyTorch 2.1, PyG 2.4 (older than ADR-H15 stack); CPU run supported (`--gpus null`) with a custom `rspmm` kernel compiled on CPU [CLAIM-ultra-01] |
| Status | research / quiescent (about 20 months since last commit) |

## 2. Problem, workloads, workflows
Predict missing edges in a KG whose entities and relations were never seen in training (zero-shot), or after short fine-tuning. EOIP workflow: new tenant graph with no training history proposes candidate links into the prediction plane (J8); cold-start for GL0.

## 3. Feature inventory
| Feature | Status | Evidence |
|---|---|---|
| Zero-shot link prediction on 57 graphs (16 transductive, 18 inductive entity, 23 inductive entity+relation) | present | [CLAIM-ultra-01] |
| UltraQuery logical queries (23 datasets) | present | [CLAIM-ultra-01] |
| Fine-tuning | present | [CLAIM-ultra-03] |
| Heterogeneous types / node features | partial: relation-structure only, no node attribute encoder (hypothesis from method description) | [CLAIM-ultra-03] |
| Temporal graphs | absent (none found) | [CLAIM-ultra-01] |
| Calibration | absent | [CLAIM-ultra-01] |
| Explainability | absent (per-path explanations of the underlying NBFNet-style model are not offered) | [CLAIM-ultra-01] |
| Packaging, API, CLI | scripts only | [CLAIM-ultra-01] |

## 4. Architecture
```
Query (h, r, ?) -> relation graph (4 fundamental interaction types)
   -> GNN_1 builds relation representations conditioned on r
   -> GNN_2 runs over entity graph with those as edge features, h initialised
   -> score each candidate tail -> rank
```
No state beyond checkpoint; stateless inference per query.

## 5. Under-the-hood reconstruction
Per the paper: relation identity is replaced by relation-to-relation interaction patterns (head-to-head, head-to-tail, tail-to-head, tail-to-tail), so any vocabulary maps onto the same learned parameters. Inference is conditional message passing from the query head, so cost per query scales with graph size (hypothesis: no precomputed index). A custom generalised sparse matrix multiplication (`rspmm`) kernel is compiled at first run, which needs a C++ toolchain on the host: relevant for air-gapped images [CLAIM-ultra-01]. Code paths were not opened.

## 6. Requirements inferred
FR: score candidates for unseen vocabularies; fine-tune. NFR: pinned torch/PyG; pre-built kernel in image; deterministic evaluation split protocol; filtered ranking.

## 7. Performance and resource model
Authors' numbers, single RTX 3090, PyG port: ULTRA(4g) zero-shot averages inductive(e) MRR 0.444 / Hits@10 0.588; inductive(e,r) MRR 0.344 / Hits@10 0.513 (paper: 0.439/0.580 and 0.352/0.518). UltraQuery 23-dataset average EPFO MRR 0.309 [CLAIM-ultra-01]. Paper headline: beats tailored baselines on 50+ graphs of 1k-120k nodes by about 15% on average, zero-shot [CLAIM-ultra-03]. CPU timing: NOT PUBLICLY VERIFIED. Uncertainty: benchmark graphs are small; the authors state parameter scaling beyond about 200k did not help [CLAIM-ultra-03].

## 8. Strengths
Zero-shot across vocabularies, tiny model (2 MB), MIT code. Exceed: wrap behind calibration and evidence.

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | tested on 1k-120k node graphs; large-graph scalability unverified; per-query message passing |
| Evidence | authors' own limitations section: no gain from more pre-training graphs or parameters [CLAIM-ultra-03] |
| Independent | no dedicated reproduction found; a different-author paper (arXiv:2410.12609) reports its own method SCR beating ULTRA on most metrics under identical conditions, which weakens "state of the art" but does not refute zero-shot transfer [CLAIM-ultra-04] |
| Friction | stale pins (Python 3.9, torch 2.1, PyG 2.4); kernel compile; not a package |

## 10. Deployment, licensing, operations
MIT; redistribution straightforward for code. Datasets used for pre-training (FB15k237, WN18RR, CoDEx, NELL995) have their own terms: legal review of weight redistribution trigger (derived from data) is advisable. CPU path exists, so no CUDA need (ADR-H16). Air-gap viable if kernel pre-built.

## 11. Delta versus baseline
BL-44 has no learned link predictor; BL-57 gives PyG tier. ULTRA could run on N1 as a cold-start scorer. It also fits the prediction-plane contract (BL-40 epistemic separation: PROPOSED) but needs calibration it lacks.

## 12. Cards
STR-ultra-01 | ULTRA | vocabulary-agnostic scoring | [CLAIM-ultra-01] | cold-start tenants | integrate | optional scorer behind a model-interface | on 3 held-out tenant graphs, zero-shot Hits@10 beats a degree/path heuristic by a pre-set margin.
INV-ultra-01 | ULTRA main / 4g | unproven scale and unverified independent results | [CLAIM-ultra-03][CLAIM-ultra-04] | root cause: maturity (hypothesis for scale) | Option 1: use as offline scorer only; 2: ULTRA plus path-evidence re-ranker; 3: tenant-fine-tuned model with calibration and provenance. Selected 1 then 2. Benchmark: CPU latency and MRR on 10k, 100k, 1M-edge synthetic KGs vs PyKEEN RotatE; kill if 100k-edge latency exceeds budget. Falls apart on filtered-evaluation errors. Defensibility: governance layer, not the model. Decision: EXPERIMENT. (Seed hypothesis 12, temporal graph learning only with explainability, leakage controls and CPU-first viability: ULTRA fails its temporal and explainability preconditions, so it supports the hypothesis only as a static scorer.)

## 13. Per-capability decisions
CAP-64: EXPERIMENT. CAP-63: DEFER (use PyKEEN for transductive). CAP-65: REJECT (no time).

## 14. Tests
(1) Reproduce 3 inductive datasets on CPU from a clean offline image. (2) Run on an EOIP tenant fixture with held-out edges split by timestamp. (3) Check ranks are filtered. (4) Measure ECE after isotonic calibration. (5) Confirm scores land only in the prediction plane.

## 15. Risks
Result inflation from benchmark overlap with pre-training data; weight provenance; stale deps; no maintainers.

## Appendix A — Dimension coverage
| Dimension | Sections | Summary |
|---|---|---|
| D1-D8 | 1,3,5 | research code; temporal absent |
| D9-D12 | 3,10 | none provided |
| D13-D16 | 2,7,8 | zero-shot KG completion |
| D17-D20 | 7,9,10 | CPU unmeasured |
| D21-D24 | 1,10,15 | MIT code; data terms unclear |

## Appendix B — Capability mapping
| CAP | Technology | Claim | Baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-64 | native (scoring only) | CLAIM-ultra-01 | BL-44 Partial | EXPERIMENT | P2 |
| CAP-43 | absent | CLAIM-ultra-01 | BL-40 Partial | BUILD | P1 |
| CAP-24 | absent | CLAIM-ultra-01 | BL-48 Partial | BUILD | P2 |
| CAP-50 | partial | CLAIM-ultra-01 | BL-57 | EXPERIMENT | P2 |

## Appendix C — Evidence
| CLAIM | product/date | claim | class | source | access | conf. | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-ultra-01 | ULTRA repo | MIT; 57 datasets; ckpts; 168k params; PyG numbers above; Python 3.9/torch 2.1/PyG 2.4; CPU via `--gpus null`; no releases | vendor doc | github.com/DeepGraphLearning/ULTRA | 2026-10-26 | 0.8 | none |
| CLAIM-ultra-02 | commits feed | newest commit 2025-02-03 | primary | github.com/DeepGraphLearning/ULTRA/commits.atom | 2026-10-26 | 0.7 | none |
| CLAIM-ultra-03 | ICLR 2024 paper | 57 KGs; zero-shot beats supervised baselines ~15% avg; scaling beyond ~200k params gave no significant gain | peer-reviewed | arxiv.org/abs/2310.04562 (via search summary) | 2026-10-26 | 0.6 | full paper not read |
| CLAIM-ultra-04 | arXiv 2410.12609 | different-author method SCR outperforms ULTRA on most metrics under identical PyG setup | peer-reviewed/preprint | arxiv.org/pdf/2410.12609 (via search summary) | 2026-10-26 | 0.5 | numbers not extracted |

## Appendix D — Assumptions
No independent reproduction exists in what was found; absence is not proof. Method details (relation graph, kernel) come from the README and search summary of the paper.
