# C11 — Tier C records (V24)

Verified 2026-10-18 (brief date); web sources fetched 2026-10-26 (session clock). Worker V24 (assigned as W24). Commit dates come from GitHub Atom feeds because the GitHub API was rate-limited. Cross-references: [C11-pyg.md](C11-pyg.md), [C11-dgl.md](C11-dgl.md), [C11-pykeen.md](C11-pykeen.md).

### T-C11-graphstorm — GraphStorm
| Field | Value |
|---|---|
| URL | https://github.com/awslabs/graphstorm |
| Owner | AWS Labs |
| Latest | 0.5.1, 2025-12-31 (PyPI); commits to 2026-06-30 |
| Status | active |
| Licence | Apache-2.0 (permissive) |
| Deployment | CLI, Docker, SageMaker, self-hosted cluster |
| Air-gap | partial (pins `transformers==4.48.0`, `torchdata==0.9.0`, `ogb==1.3.6`) |
| Tier reason | Large-scale GNN; distributed link prediction and node classification |

Single-command GNN training and distributed inference, built on DGL (README pins dgl 2.3.0 with torch 2.3.0), so it inherits DGL's lag with PyTorch. README claims billion-edge scale (vendor claim, workload not read) and CPU or NVIDIA GPU. Temporal support not mentioned. No calibration or explainability found. Touches CAP-64, CAP-05. Useful as a scale reference; not for the N1 CPU stack.

**Decision:** REFERENCE-ONLY. DGL coupling conflicts with ADR-H15.

| CLAIM | product/date | claim | class | source | access | conf. | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-graphstorm-01 | 0.5.1, 2025-12-31 | Apache-2.0; deps above; DGL-based | primary | pypi.org/pypi/graphstorm/json; github.com/awslabs/graphstorm | 2026-10-26 | 0.8 | none |

### T-C11-ampligraph — AmpliGraph
| Field | Value |
|---|---|
| URL | https://github.com/Accenture/AmpliGraph |
| Owner | Accenture Labs |
| Latest | 2.2.0, 2026-07-06 |
| Status | active (release in 2026) |
| Licence | Apache-2.0 (permissive) |
| Deployment | pip library |
| Air-gap | yes (offline wheels) |
| Tier reason | KGE library with discovery API |

TensorFlow 2 (`tensorflow>=2.15,<2.16`), `numpy<2.0`, Python `>=3.9,<3.12` pinned, which collides with a torch-based EOIP stack (second ML framework, oversized install, old numpy). Models: TransE, DistMult, ComplEx, HolE, RotatE; discovery API for new facts. Calibration of predictions is mentioned in its older documentation but was not found on the current docs page: UNVERIFIED. No temporal or explainability support found. Touches CAP-63.

**Decision:** REJECT as dependency (framework mismatch); REFERENCE-ONLY for the discovery API shape.

| CLAIM | product/date | claim | class | source | access | conf. | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-ampligraph-01 | 2.2.0, 2026-07-06 | Apache-2.0; TF 2.15, Python <3.12, numpy<2 | primary | pypi.org/pypi/ampligraph/json; docs.ampligraph.org | 2026-10-26 | 0.85 | none |

### T-C11-dgl-ke — DGL-KE
| Field | Value |
|---|---|
| URL | https://github.com/awslabs/dgl-ke |
| Owner | AWS Labs |
| Latest | PyPI `dglke` 0.1.2, 2021-01-25; GitHub release feed shows 2020 tags only; commits to 2026-07-06 |
| Status | maintenance (README redirects to GraphStorm) |
| Licence | Apache-2.0 (permissive) |
| Deployment | pip, CLI (`dglke_train`) |
| Air-gap | partial |
| Tier reason | KGE (activity to verify) |

Activity verified: no release in about 5 years; README note sends users wanting TransE, DistMult or RotatE to GraphStorm; latest commit 2026-07-06 is not described. Claims of embedding 86M nodes/338M edges in 100 minutes on 8 GPUs are vendor claims on GPU hardware. Built on DGL, which is itself stagnant. Touches CAP-63.

**Decision:** REJECT. Superseded by GraphStorm and PyKEEN.

| CLAIM | product/date | claim | class | source | access | conf. | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-dgl-ke-01 | 0.1.2, 2021-01-25 | Apache-2.0; redirect note; vendor scale claim | vendor doc | github.com/awslabs/dgl-ke; pypi.org/pypi/dglke/json | 2026-10-26 | 0.8 | none |

### T-C11-pyg-temporal — PyTorch Geometric Temporal
| Field | Value |
|---|---|
| URL | https://github.com/benedekrozemberczki/pytorch_geometric_temporal |
| Owner | Benedek Rozemberczki (individual) and contributors |
| Latest | 0.56.2, 2025-07-16; commits to 2026-05-30 |
| Status | maintenance |
| Licence | MIT (permissive) |
| Deployment | pip library |
| Air-gap | partial (pins `decorator==4.4.2`, needs torch-scatter, torch-sparse) |
| Tier reason | Temporal GNN |

Recurrent and attention layers for spatio-temporal signals on a fixed or dynamic graph (traffic, epidemics); it is a third-party add-on to PyG, not the PyG event-stream `TemporalData`. Requires torch-scatter and torch-sparse, which PyG is moving off. Assumes snapshot sequences; no leakage-safe split utilities beyond temporal signal splitting, no calibration, no explainability (none found). Touches CAP-65.

**Decision:** DEFER. Snapshot models fit time-series forecasting on nodes, not EOIP's event-style graph.

| CLAIM | product/date | claim | class | source | access | conf. | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-pyg-temporal-01 | 0.56.2, 2025-07-16 | MIT; dependency list | primary | pypi.org/pypi/torch-geometric-temporal/json | 2026-10-26 | 0.85 | none |

### T-C11-graphgym — GraphGym
| Field | Value |
|---|---|
| URL | https://github.com/snap-stanford/GraphGym |
| Owner | Stanford SNAP (Jiaxuan You) |
| Latest | PyPI `graphgym` 0.4.0, 2022-03-24; last commit 2023-03-14 |
| Status | maintenance / effectively dormant (standalone repo) |
| Licence | MIT (licence file combines several copyright holders; MIT text not re-read in full: UNVERIFIED) |
| Deployment | pip library, YAML config CLI |
| Air-gap | yes |
| Tier reason | GNN design space |

Config-driven GNN design-space exploration (the NeurIPS 2020 "Design Space for GNNs" work). A GraphGym module also exists inside PyG (stated from PyG documentation memory, not re-verified this run). Value for EOIP: the idea of searching a small design space per task, not the code. Touches CAP-64, CAP-78.

**Decision:** REFERENCE-ONLY.

| CLAIM | product/date | claim | class | source | access | conf. | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-graphgym-01 | 0.4.0, 2022-03-24 | last release and commit dates | primary | pypi.org/pypi/graphgym/json; github.com/snap-stanford/GraphGym/commits.atom | 2026-10-26 | 0.8 | none |

### T-C11-graph-transformers — Graph transformers (Graphormer, GraphGPS)
| Field | Value |
|---|---|
| URL | https://github.com/microsoft/Graphormer ; https://github.com/rampasek/GraphGPS |
| Owner | Microsoft; Rampasek, Galkin, Dwivedi, Beaini et al. |
| Latest | Graphormer v2.0, 2021-12-22 (README), commits to 2026-09-24; GraphGPS release 2023-01-17, last commit 2023-02-17 |
| Status | Graphormer: maintenance (README only); GraphGPS: dormant |
| Licence | MIT both (permissive) |
| Deployment | research code |
| Air-gap | yes (code), awkward build |
| Tier reason | Architecture references |

Graphormer extends a pinned fairseq commit, Docker pins Python 3.9, PyTorch 1.9.1, CUDA 11.1, and the README explicitly disclaims compatibility with current Python or PyTorch; stronger pretrained versions are "exclusively on Azure Quantum Elements". It targets molecules. GraphGPS is built on PyG 2.2-era APIs. Both are CPU-hostile at scale (quadratic attention; hypothesis) and offer no calibration, explainability or temporal support. Maintained alternatives exist inside PyG (e.g. GPS layers; presence UNVERIFIED). Touches CAP-64.

**Decision:** REFERENCE-ONLY. Likely `DEFERRED (H-17)` under ADR-H15.

| CLAIM | product/date | claim | class | source | access | conf. | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-graph-transformers-01 | Graphormer README | MIT; fairseq pin; torch 1.9.1; no compatibility claim; Azure-only advanced models | vendor doc | github.com/microsoft/Graphormer | 2026-10-26 | 0.85 | none |
| CLAIM-graph-transformers-02 | GraphGPS | MIT; last commit 2023-02-17 | primary | github.com/rampasek/GraphGPS/commits.atom | 2026-10-26 | 0.75 | none |

### T-C11-tgn — Temporal GNNs (TGN and frameworks)
| Field | Value |
|---|---|
| URL | https://github.com/twitter-research/tgn |
| Owner | Twitter Research (reference code for Rossi et al.) |
| Latest | no releases; last commit 2023-06-21 |
| Status | dormant reference code |
| Licence | Apache-2.0 (permissive) |
| Deployment | research scripts |
| Air-gap | yes |
| Tier reason | Temporal link prediction |

Temporal Graph Networks keep a per-node memory updated by an event stream and predict future links. Maintained implementations: PyG `TGNMemory` and `TemporalDataLoader` (see C11-pyg.md), and TGB event streams inside RelBench (see C11-relbench.md). The temporal-split discipline (chronological train/val/test, no future edges) matters more than the model. Touches CAP-65.

**Decision:** EXPERIMENT via PyG's TGN, not this repo.

| CLAIM | product/date | claim | class | source | access | conf. | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-tgn-01 | repo | Apache-2.0; last commit 2023-06-21 | primary | github.com/twitter-research/tgn | 2026-10-26 | 0.75 | none |

### T-C11-torchkge-libkge — TorchKGE and LibKGE
| Field | Value |
|---|---|
| URL | https://github.com/torchkge-team/torchkge ; https://github.com/uma-pi1/kge |
| Owner | TorchKGE team; University of Mannheim (Gemulla group) |
| Latest | TorchKGE 0.17.7, 2023-04-05, last commit 2023-11-17; LibKGE no release or PyPI package found, commits to 2026-04-01 |
| Status | TorchKGE dormant; LibKGE maintenance |
| Licence | BSD (TorchKGE); MIT (LibKGE) (permissive) |
| Deployment | pip (TorchKGE); source install (LibKGE) |
| Air-gap | yes |
| Tier reason | KGE libraries |

TorchKGE is a lightweight PyTorch KGE library; LibKGE emphasises reproducible, config-driven experiments and hyperparameter search. PyKEEN is the more active superset. Neither offers calibration, explainability or temporal support (none found). Touches CAP-63, CAP-78.

**Decision:** REFERENCE-ONLY (LibKGE's reproducibility configs); REJECT TorchKGE.

| CLAIM | product/date | claim | class | source | access | conf. | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-torchkge-libkge-01 | 0.17.7 / master | dates and licences above | primary | pypi.org/pypi/torchkge/json; github.com/uma-pi1/kge | 2026-10-26 | 0.8 | none |

### T-C11-neuro-symbolic — Neuro-symbolic frameworks (Scallop, DeepProbLog, Logic Tensor Networks)
| Field | Value |
|---|---|
| URL | https://github.com/scallop-lang/scallop ; https://github.com/ML-KULeuven/deepproblog ; https://github.com/logictensornetworks/logictensornetworks |
| Owner | UPenn (Ziyang Li); KU Leuven; LTN community (Serafini, Garcez, Carraro) |
| Latest | Scallop 0.2.4 (2024-08-30), commits to 2026-06-26; DeepProbLog 2.1.0 (2026-09-07); LTN 2.1 (2023-03-31, TensorFlow) and LTNtorch 1.0.2 (PyTorch, separate package), last LTN commit 2024-11-13 |
| Status | Scallop active; DeepProbLog active; LTN maintenance |
| Licence | Scallop MIT; DeepProbLog Apache; LTN licence text appears to be MIT: UNVERIFIED |
| Deployment | Rust/Python (Scallop), Python (others) |
| Air-gap | yes (Scallop needs a Rust toolchain) |
| Tier reason | Research references |

All three combine learned predicates with logic: Scallop (Datalog with provenance semirings, differentiable), DeepProbLog (probabilistic logic with neural predicates, deps pysdd, problog), LTN (fuzzy first-order logic as a loss). They are relevant to rule-plus-learning in the prediction plane and to confidence propagation, not as production reasoners; Scallop's PyPI `scallopy` 0.1.0 dates from 2021 and is not the current distribution: UNVERIFIED install path. Touches CAP-22, CAP-64, CAP-24.

**Decision:** REFERENCE-ONLY; EXPERIMENT later with Scallop-style provenance semirings only if rules plus learned scores are needed.

| CLAIM | product/date | claim | class | source | access | conf. | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-neuro-symbolic-01 | releases | versions, dates, licences above | primary | pypi.org/pypi/deepproblog/json; pypi.org/pypi/ltntorch/json; github.com/scallop-lang/scallop | 2026-10-26 | 0.7 | LTN licence text unconfirmed |
