# C11 — DGL (Deep Graph Library)

| Field | Value |
|---|---|
| Registry ID | T-C11-dgl |
| Tier | B — GNN framework competing with PyG; activity must be verified before any reliance. |
| Versions examined | PyPI `dgl` 2.2.1 (2024-05-13, latest on PyPI); GitHub release v2.4.0 (2024-08-29); wheel index lists `dgl-2.5.0` under `torch-2.4` |
| Verified on | 2026-10-18 (brief date); web sources fetched 2026-10-26 (session clock) |
| Worker | V24 (assigned as W24) |

## 1. Identity, current status, tier, sources
| Item | Finding |
|---|---|
| What | Python GNN framework (message passing, heterogeneous graphs, samplers, distributed training) over PyTorch/MXNet/TensorFlow. Not a database. [CLAIM-dgl-01] |
| Owner | `dmlc` GitHub organisation (repo `dmlc/dgl`); corporate governance NOT PUBLICLY VERIFIED. |
| Licence | Apache-2.0 (README and PyPI) [CLAIM-dgl-01] |
| Releases | PyPI stops at 2.2.1 (2024-05-13). GitHub releases feed: v2.2.1, v2.3.0, v2.4.0 (2024-08-29) is newest. No tagged release in the ~26 months to 2026-10-26 [CLAIM-dgl-02] |
| Commit activity | Newest commit entries on `master` in the Atom feed dated 2025-07-31 (docs and bug-fix commits); nothing newer seen [CLAIM-dgl-02] |
| Wheels | `data.dgl.ai/wheels` has `torch-2.4/2.5/2.6` folders; `torch-2.7`+ returned HTTP 403 (absent or restricted: not proven). PyTorch is at 2.14.x per the sibling PyG file, so DGL lags by about eight minor versions [CLAIM-dgl-03] |
| Status | **maintenance / stagnating** (not archived; 143 open PRs on the repo page) [CLAIM-dgl-02] |
| Forks of note | AMD publishes a separate ROCm-maintained DGL fork; NVIDIA containers shipped DGL 2.1 (2024) [CLAIM-dgl-04] |

## 2. Problem, workloads, workflows
Node/link/graph prediction on homogeneous and heterogeneous graphs, billion-edge distributed training, KG embeddings (DGL-KE, see Tier C). EOIP workflow: heterogeneous link prediction over a service-dependency graph for journey J8. PyG already covers this ([C11-pyg.md](C11-pyg.md)), so DGL is a fallback only.

## 3. Feature inventory
| Feature | Status | Evidence |
|---|---|---|
| Heterographs, message passing, `dgl.nn` layers incl. RGCN/HGT | present | [CLAIM-dgl-01] |
| Neighbour/GraphBolt samplers, distributed training | present | [CLAIM-dgl-01] |
| Temporal graphs / leakage-safe sampling | partial (time-aware sampling not documented in what was read); UNVERIFIED | — |
| Calibration | absent (none found) | [CLAIM-dgl-01] |
| Explainability | partial (`dgl.nn.pytorch.explain`: GNNExplainer, PGExplainer; presence UNVERIFIED this run) | — |
| CLI/UI/server/registry | absent | — |
| CPU-only install | UNVERIFIED (CPU wheels exist historically; modern torch pairing not shown) | [CLAIM-dgl-03] |

## 4. Architecture
```
Python API (dgl, dgl.nn) -> DGLGraph (C++ core, tensoradapter per torch version)
   -> framework backend (PyTorch) -> kernels (CPU / CUDA)
Data: in-memory graph or distributed partitions (METIS) -> sampler -> trainer
```
No state, control plane or security layer beyond the process.

## 5. Under-the-hood reconstruction
A native C++ library with a per-PyTorch-version `tensoradapter` shim (CMake builds one adapter per torch release; seen in `CMakeLists.txt` and a build comment) [CLAIM-dgl-03]. Heterograph = one CSR/COO per relation type. This design explains the lag: every PyTorch release needs a new native build. Hypothesis: engineering capacity moved away; not evidenced.

## 6. Requirements inferred
FR: heterogeneous relational GNN training; sampling. NFR: pinned torch pairing; CPU wheels; no network at runtime. EOIP would need a version-matched native wheel it can build and hash-lock itself.

## 7. Performance and resource model
No benchmark run. Vendor/community claims about speed are not re-measured. Failure mode: ABI mismatch with current PyTorch.

## 8. Strengths
Mature heterograph abstraction; distributed partitioning; Apache-2.0 (better than nothing for redistribution). Match: PyG covers the same ground with an active release stream.

## 9. Limitations
| Class | Item |
|---|---|
| Operational | no release since 2024-08; wheels trail PyTorch by ~8 minors [CLAIM-dgl-02][CLAIM-dgl-03] |
| Friction | native build per torch version; PyPI wheel is 2.2.1 |
| Ecosystem | DGL-KE points to GraphStorm for TransE/DistMult/RotatE [CLAIM-dgl-05]; GraphStorm pins dgl 2.3.0 with torch 2.3.0 [CLAIM-dgl-05] |

## 10. Deployment, licensing, operations
Apache-2.0: redistributable; no legal trigger found. Air-gap: yes in principle (offline wheels). ADR-H15/H16: CPU build must be supplied by EOIP itself because no current-torch CPU wheel was shown; adds a native-build burden, so EOIP should not take DGL into the N1 tier.

## 11. Delta versus EOIP baseline
BL-44 is heuristic-only and BL-57 plans torch + PyG. DGL adds nothing PyG does not, and conflicts with the CPU-first torch pin (ADR-H15 item 5).

## 12. Cards
STR-dgl-01 | DGL | heterograph + distributed partitioning | [CLAIM-dgl-01] | scale beyond RAM | integrate (reference only) | study partition scheme | none now.
INV-dgl-01 | DGL 2.2.1 / 2.4.0 | stagnating release stream | [CLAIM-dgl-02][CLAIM-dgl-03] | root cause: maintenance (proven for releases; cause hypothesis) | choose PyG (maintained, MIT) over DGL; if a customer needs DGL, run it out-of-tree. Option 1: no DGL. Option 2: optional adapter. Option 3: framework-neutral model interface in the prediction plane. Selected: 3 over 1. Benchmark: same R-GCN on one dataset in both, compare CPU time. Defensibility: neutral model contract survives framework churn. Decision: REJECT as dependency. (Seed hypotheses 12/13 not targeted.)

## 13. Per-capability decisions
CAP-64 (GNN): REJECT DGL, REUSE PyG. CAP-63: DEFER. CAP-65: REJECT (use PyG temporal sampling).

## 14. Tests
Acceptance for any revisit: a current-torch CPU wheel installs offline, runs R-GCN 2-layer on the CPU reference, and has a release within 12 months.

## 15. Risks / open questions
Real maintainer activity (GitHub API rate-limited; commit dates come from Atom feeds). Whether 2.5.0 wheels are official.

## Appendix A — Dimension coverage
| Dimension | Sections | Summary |
|---|---|---|
| D1-D4 identity, model, storage, query | 1,3,5 | library only; no storage/query |
| D5-D8 reasoning, ingestion, identity, temporal | 3 | temporal UNVERIFIED; others N/A |
| D9-D12 governance, security, tenancy | 3,10 | none |
| D13-D16 retrieval, ML, GNN | 2,3,8 | GNN core capability |
| D17-D20 ops, perf, deployment | 7,9,10 | lag vs torch |
| D21-D24 licence, maturity, cost, risk | 1,10,15 | Apache-2.0; stagnating |

## Appendix B — Capability mapping
| CAP | This technology | Claim | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-64 | native | CLAIM-dgl-01 | BL-44 Partial | REJECT | P3 |
| CAP-63 | partial (DGL-KE) | CLAIM-dgl-05 | none | DEFER | P3 |
| CAP-50 | partial | CLAIM-dgl-03 | BL-57 | DEFER | P3 |

## Appendix C — Evidence
| CLAIM | product/date | claim | class | source | access | conf. | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-dgl-01 | DGL repo | Apache-2.0; GNN framework for PyTorch/MXNet/TF; 14.3k stars; not archived | vendor doc | github.com/dmlc/dgl | 2026-10-26 | 0.8 | none |
| CLAIM-dgl-02 | releases/commits feeds | newest release v2.4.0 2024-08-29; newest commits 2025-07-31 | primary feed | github.com/dmlc/dgl/releases.atom, /commits/master.atom | 2026-10-26 | 0.7 | feed shows only recent entries |
| CLAIM-dgl-03 | PyPI + wheel index | PyPI 2.2.1 2024-05-13; wheels for torch 2.4-2.6; torch-2.7+ HTTP 403; CMake builds a tensoradapter per torch | primary | pypi.org/pypi/dgl/json; data.dgl.ai/wheels/ | 2026-10-26 | 0.7 | 403 could be access policy |
| CLAIM-dgl-04 | AMD/NVIDIA docs | ROCm fork separate; NVIDIA 24.03 container has DGL 2.1 | secondary | rocm.docs.amd.com DGL compatibility; docs.nvidia.com rel-24-03 | 2026-10-26 | 0.6 | none |
| CLAIM-dgl-05 | dgl-ke README, graphstorm | DGL-KE redirects to GraphStorm; GraphStorm install pins dgl 2.3.0/torch 2.3.0 | vendor doc | github.com/awslabs/dgl-ke; github.com/awslabs/graphstorm | 2026-10-26 | 0.7 | none |

## Appendix D — Assumptions
GitHub API was rate-limited, so Atom feeds stand in for commit data. "Maintenance" is inferred from missing releases, not from maintainer statements. Access date follows the session clock.
