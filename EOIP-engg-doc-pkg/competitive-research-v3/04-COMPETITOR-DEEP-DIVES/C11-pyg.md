# C11 — PyTorch Geometric (PyG)

| Field | Value |
|---|---|
| Registry ID | T-C11-pyg |
| Tier | A — the N1 tier of the Graph-Neurons programme (ADR-H15) names PyG as its GNN framework, and BL-44 is blocked on it. |
| Versions examined | `torch-geometric` **2.8.1** (PyPI upload 2026-10-12; GitHub release page labels it "06 Oct"); 2.8.0.post1 (2026-07-20); 2.8.0 (2026-06-05); 2.7.0 (2025-10-15); 2.6.1 (2024-09-26). PyTorch 2.12.0 and 2.14.1 CPU wheels for size. Source paths checked at tag `2.8.1`. |
| Verified on | 2026-10-18 (brief date); web sources actually fetched 2026-10-26 (session clock) |
| Worker | V08 (assigned as W24) |

## 1. Identity, current status, tier, and sources

| Item | Finding |
|---|---|
| What it is | A Python library of graph neural network (GNN) layers, data structures, mini-batch samplers, explainers and benchmarks on top of PyTorch. Not a database and not a service. [CLAIM-pyg-01] |
| Owner / governance | GitHub organisation `pyg-team`; repo `pyg-team/pytorch_geometric`. Corporate backing and governance model: **NOT PUBLICLY VERIFIED in this run** (GitHub API was rate-limited; no star or contributor counts captured). |
| Licence | **MIT** (PyPI `license_expression`) [CLAIM-pyg-01]. `pyg-lib` and `torch-scatter`/`torch-sparse` licences: UNVERIFIED. PyTorch itself is BSD-style upstream (not re-read this run; PyPI field was empty). |
| Python / dependencies | `>=3.10`; core deps: aiohttp, fsspec, jinja2, numpy, psutil, pyparsing, requests, tqdm, xxhash. **numpy is mandatory**; PyTorch is a separate requirement [CLAIM-pyg-01][CLAIM-pyg-04]. |
| Release cadence | 2.6.1 (2024-09-26) -> 2.7.0 (2025-10-15) is a 13-month gap; 2.8.0 followed 8 months later, then a post-release and 2.8.1 four months after that [CLAIM-pyg-01]. Active but irregular. |
| Torch coupling | 2.8.0 adds PyTorch 2.9-2.12 and Python 3.10-3.14, drops PyTorch 2.8 [CLAIM-pyg-02]. PyPI `torch` is already at **2.14.1**, i.e. newer than anything PyG declares support for (hypothesis: works but is untested; to be pinned) [CLAIM-pyg-08]. |
| Status | active. No archival signal. |
| Members | `torch_geometric` core; `pyg-lib` (native ops, heterogeneous operators, sampling); `torch-scatter`, `torch-sparse` (optional); `torch-cluster` and `torch-spline-conv` deprecated in favour of `pyg-lib` >= 0.6/0.7 [CLAIM-pyg-02][CLAIM-pyg-04]. PyG Temporal is a separate third-party package (Tier C, not examined here). |

Sources: PyPI JSON, CHANGELOG at tag 2.8.1, GitHub releases page, installation / explain / loader / data docs, PyTorch CPU wheel index, `pyproject.toml` at 2.8.1, the In-n-Out calibration paper. Internal: ADR-H15/H16/H17, Graph-Neurons-requirements.md section 0.6, baseline BL-44/BL-57.

## 2. Primary problem, target workloads, concrete example workflows

PyG solves **representation learning on graph-structured tensors**: node classification, link prediction, graph classification, KG completion, on homogeneous, heterogeneous and temporal graphs.

| Workflow | How PyG does it | EOIP relevance |
|---|---|---|
| Heterogeneous link prediction (e.g. predict missing `DEPENDS_ON` edges between services) | `HeteroData` + `to_hetero` / `RGCNConv` / `HGTConv`, trained with `LinkNeighborLoader` on positive and sampled negative edges | EOIP journey J8; GL0/GL2 learning |
| Temporal link prediction | `TemporalData` event stream, `TGNMemory`, `TemporalDataLoader`; or time-constrained neighbour sampling with `time_attr` / `edge_label_time` [CLAIM-pyg-06][CLAIM-pyg-07] | Seed hypothesis 12 (temporal graph learning with leakage controls) |
| KG embedding | `torch_geometric.nn.kge`: TransE, ComplEx, DistMult, RotatE [CLAIM-pyg-09] | CAP-63 |
| Explain a prediction | `Explainer` with GNNExplainer, PGExplainer, AttentionExplainer, CaptumExplainer, GraphMaskExplainer [CLAIM-pyg-05] | CAP-24 on the prediction plane |
| Mini-batch training beyond RAM | `NeighborLoader`, `HGTLoader`, `ClusterLoader`, GraphSAINT, plus `FeatureStore` / `GraphStore` abstractions for remote data [CLAIM-pyg-06][CLAIM-pyg-07] | A GraphStore bridge could read from HugeGraph/Neo4j without a full export (hypothesis) |
| Relational deep learning | `from_relbench` converts RelBench databases to `HeteroData` (added 2.8.0) [CLAIM-pyg-02] | Tier B RelBench cross-reference |

Not in scope for PyG: storage, serving, model registry, feature store, calibration, governance. EOIP must build the plane around it.

## 3. Feature inventory

| Area | Feature | Status | Evidence |
|---|---|---|---|
| Data | `Data`, `HeteroData`, `TemporalData`, `Batch`, on-disk datasets, DB backends | present | [CLAIM-pyg-07] |
| Data | `FeatureStore` / `GraphStore` abstract remote backends | present (abstract only) | [CLAIM-pyg-07] |
| Layers | Conv layers incl. `RGCNConv`, `HGTConv`, GAT/GATv2 (TorchScript dropped for GAT in 2.8.0) | present | [CLAIM-pyg-02]; files exist at 2.8.1 |
| Heterogeneous | `to_hetero`, `HGTLoader`, hetero-aware neighbour loaders, `HeteroExplanation` | present | [CLAIM-pyg-03][CLAIM-pyg-05][CLAIM-pyg-06] |
| Temporal | `TemporalData`, `TemporalDataLoader`, TGN model file, `time_attr` / `temporal_strategy` ("uniform" or "last") sampling, `edge_label_time` | present | [CLAIM-pyg-06][CLAIM-pyg-07] |
| Link prediction | `LinkNeighborLoader`, LPFormer (2.7.0), LinkPred metrics: MRR, recall, NDCG, weighted variants | present | [CLAIM-pyg-03] |
| Calibration | Temperature scaling, Platt/isotonic, ECE, edge-level calibration | **absent from docs/changelog; none found** | [CLAIM-pyg-10] (no PyG calibration module located; absence = not found, not proven) |
| Explainability | `Explainer`, 6 algorithms, model vs phenomenon explanations, node/edge/attribute masks, thresholds, fidelity / characterization / unfaithfulness metrics | present, **docs warn "active development and may not be stable"** | [CLAIM-pyg-05] |
| Explainability on hetero | GNNExplainer, PGExplainer, AttentionExplainer gain hetero support | present since 2.7.0 | [CLAIM-pyg-03] |
| Sampling / loaders | NeighborLoader, LinkNeighborLoader, HGTLoader, Cluster, GraphSAINT x3, ShaDow, RandomNode, Zip, Cached, Prefetch | present | [CLAIM-pyg-06] |
| KGE | TransE, ComplEx, DistMult, RotatE | present | [CLAIM-pyg-09] |
| GNN + LLM | `GRetriever`, `torch_geometric.nn.nlp` (2.6.0), GraphRAG QA generation example needing vLLM or NVIDIA NIM (2.8.0) | present as examples | [CLAIM-pyg-03][CLAIM-pyg-02] |
| Distributed / multi-GPU | examples; `cuGraph GNN` via NVIDIA container (GPU) | optional, GPU-oriented | [CLAIM-pyg-04] |
| UI / CLI / server | none | absent | n/a |
| Model governance, versioning, provenance | none | absent | n/a |
| Security-relevant | model artefacts are PyTorch checkpoints (pickle-based); loading untrusted `.pt` is unsafe by default in PyTorch | hypothesis, not verified in PyG source this run | n/a |

## 4. Text-based architecture diagram

```
        training-time                                  inference-time
  ┌────────────────────────┐                    ┌─────────────────────────┐
  │ Data / HeteroData /     │  FeatureStore /   │ trained nn.Module (CPU) │
  │ TemporalData (tensors)  │◄─GraphStore ABCs──│ + Explainer(algorithm)  │
  └──────────┬─────────────┘   (remote opt.)    └────────────┬────────────┘
             │ mini-batch                                     │ scores, masks
  ┌──────────▼─────────────┐   native ops                    ▼
  │ Loaders/Samplers        │◄── pyg-lib (C++/CPU or CUDA)   (no calibration, no provenance,
  │ Neighbor/LinkNeighbor/  │    torch-scatter/sparse (opt.)  no storage, no approval state)
  │ HGT/Cluster/GraphSAINT  │                                  ▲
  └──────────┬─────────────┘                                   │  EOIP must wrap this
             ▼                                                 │
  ┌────────────────────────┐        ┌──────────────────────────┴───────────────┐
  │ nn layers (MessagePassing)│      │ EOIP prediction plane (to be built)       │
  │ Conv/KGE/TGN/LPFormer    │      │ snapshot -> train -> calibrate -> propose │
  └────────────────────────┘        │ -> quarantine -> human approve -> fact    │
                                     └──────────────────────────────────────────┘
 PyTorch (CPU wheel ~0.12-0.20 GB download) + numpy underneath; no daemon, no network I/O.
```

## 5. Under-the-hood reconstruction

Only publicly documented behaviour is stated as fact; source-file existence at tag `2.8.1` was verified (`loader/link_neighbor_loader.py`, `explain/explainer.py`, `nn/models/tgn.py`, `nn/conv/rgcn_conv.py`, `nn/conv/hgt_conv.py`, `nn/kge/{transe,complex,distmult,rotate}.py`), but their bodies were **not read** in this run, so algorithm details below are labelled H.

| Aspect | Reconstruction |
|---|---|
| Data model | Graph as tensors: `x` node features, `edge_index` `[2, E]` COO (or `SparseTensor`/CSR), `edge_attr`, labels. `HeteroData` keeps one storage object per node type and per `(src, rel, dst)` edge type. `TemporalData` is parallel event arrays `src, dst, t, msg`. [CLAIM-pyg-07] |
| Compute | `MessagePassing`: gather source features -> message function -> scatter-aggregate by destination (sum/mean/max) -> update. The scatter step is where `torch-scatter` / `pyg-lib` accelerate CPU/GPU (H, standard design). |
| Sampling | Neighbour sampling expands seed nodes k hops with per-hop fan-out (`num_neighbors`, optionally per edge type). With `time_attr`, only neighbours with timestamp <= the seed's time are eligible; `temporal_strategy` "uniform" or "last"; temporal sampling forces `disjoint=True` so each seed gets its own subgraph [CLAIM-pyg-06]. Link variant seeds on `edge_label_index`, with `neg_sampling` generating negatives (H on exact API). |
| Hetero | `to_hetero` replicates a homogeneous GNN per edge type and sums across types (H); `HGTLoader` samples a fixed count per node type [CLAIM-pyg-06]. |
| Remote graphs | Loaders accept a `(FeatureStore, GraphStore)` tuple, so sampling can run against an external store implementing `get_tensor` / `get_edge_index`-style methods (H on method names; ABC existence verified) [CLAIM-pyg-07]. |
| Temporal memory | TGN keeps a per-node memory vector updated by a GRU from event messages (published TGN design; file exists at tag, body unread; H). |
| Explainability | `Explainer` wraps a model and an `ExplainerAlgorithm`; learns or computes node/edge/feature masks; `threshold_config` `hard`, `topk`, `topk_hard`; `Explanation` / `HeteroExplanation` objects carry masks and can export visualisations; metrics include fidelity [CLAIM-pyg-05]. |
| Transactions / concurrency / partitioning | N/A: in-process library. Parallelism comes from DataLoader workers and PyTorch threads. |
| Versioning | Library semver-ish; no model or data versioning. |
| Security | N/A at the library level; supply-chain surface is PyG + PyTorch + numpy + (aiohttp, requests, fsspec - note network-capable deps are mandatory) [CLAIM-pyg-01]. |

**Blueprint for an equivalent EOIP N1 stage** (mark H): exporter pulls an immutable, versioned subgraph snapshot from the `GraphStore` (BL-01) with permission filters applied (tenant isolation, BL-IDs for ACL), converts it to `HeteroData` with time cut-offs; trains an R-GCN (2 layers, 128 hidden, 30 bases per ADR-H15) with `LinkNeighborLoader`; scores hold-out pairs; calibrates; writes proposals to the prediction plane, never to the fact graph.

## 6. Functional and non-functional requirements inferred

| ID | Requirement for EOIP if PyG is adopted |
|---|---|
| FR-1 | Train on snapshots, never on the live authoritative graph; snapshot id recorded in every proposal. |
| FR-2 | Time-aware splits with leakage tests (sampling `time_attr` is necessary, not sufficient). |
| FR-3 | Calibrate scores on a held-out validation split; report ECE and reliability per relation type; store model version, snapshot id, seed, library versions. |
| FR-4 | Every proposed edge carries an explanation artefact (edge mask / subgraph) and is quarantined until human approval (J8). |
| NFR-1 | CPU-only; no `nvidia-*` anywhere in lock files or bundles (ADR-H16). |
| NFR-2 | N1 installed size budget <= 2.5 GB (CRA-043.1); must be **measured**, not assumed. |
| NFR-3 | Exact pinned versions of torch, torch-geometric, numpy, pyg-lib in a hash-locked file; re-evaluated each EOIP minor release (ADR-H15). |
| NFR-4 | Model files loaded only from the tenant's own signed store (checkpoint deserialisation risk, H). |

## 7. Performance and resource model

No performance numbers were measured or are claimed here.

| Resource | Verified fact | Unknown |
|---|---|---|
| Download size of CPU torch wheel | `torch 2.12.0+cpu` cp312 manylinux x86_64: **192,268,791 bytes** (~183 MiB); `torch 2.14.1+cpu` cp312 manylinux: **196,253,677 bytes** (~187 MiB); Windows cp312 win_amd64: **123,996,008 bytes** (~118 MiB) (HTTP Content-Length, 2026-10-26) [CLAIM-pyg-08] | **Installed** size (torch + numpy + PyG + deps + pyg-lib) was not measured; the 2.5 GB ADR budget remains a budget. |
| PyG wheel | `torch_geometric-2.8.1-py3-none-any.whl` 1,325,471 bytes; sdist 929,429 bytes [CLAIM-pyg-01] | Native extension wheel sizes (pyg-lib) UNVERIFIED. |
| Training/inference throughput | none claimed | Needs EOIP bake-off on CPU: nodes/s, epoch time for R-GCN on EOIP-shaped graph. |
| Scaling | Neighbour sampling bounds per-batch memory by fan-out, not graph size (design property); full-batch needs the whole graph in RAM | CPU sampling throughput is typically the bottleneck (H). |
| Failure modes | Native-extension wheel/torch ABI mismatch; unsupported torch (2.13+ vs declared 2.9-2.12); non-determinism across thread counts; silent leakage in temporal splits; score overconfidence | |

## 8. Strengths and use-case-specific advantages

| Strength | Why it matters | Match / exceed |
|---|---|---|
| MIT licence, pure-Python wheel, redistribution-friendly | Clears the GPL/AGPL gate; only transitive torch licences to review | Reuse as is |
| Broad, maintained model zoo (R-GCN, HGT, TGN, LPFormer, KGE) | Avoids writing GNNs; BL-44 stays heuristic otherwise | Reuse |
| First-class hetero and temporal sampling | EOIP graphs are heterogeneous and time-varying | Reuse; add leakage tests |
| Explainer API with fidelity metrics | Gives evidence for J8 proposals | Integrate; wrap in EOIP evidence schema |
| `FeatureStore` / `GraphStore` abstractions | Can stream from an external store; backend-neutral hook | Experiment |
| CPU wheels available on the official PyTorch index | Compatible with ADR-H16 CPU-only distribution | Reuse |

## 9. Limitations with root causes

| Class | Limitation | Type | Evidence |
|---|---|---|---|
| User/developer friction | No calibration, uncertainty or provenance tooling | intentional scope; verified absent in docs (not found) | [CLAIM-pyg-10] |
| User/developer friction | Explain module flagged unstable in its own docs | vendor-stated | [CLAIM-pyg-05] |
| Operational | Torch version coupling: PyG declares 2.9-2.12 while torch is at 2.14.1 | verified fact, consequence hypothesis | [CLAIM-pyg-02][CLAIM-pyg-08] |
| Operational | Native extensions (pyg-lib) need a wheel per torch/Python/OS; torch-cluster/spline-conv deprecated mid-stream | verified | [CLAIM-pyg-04][CLAIM-pyg-02] |
| Operational | Irregular release gaps (13 months 2024-09 -> 2025-10) | verified | [CLAIM-pyg-01] |
| Operational | numpy mandatory; EOIP lock has none (BL-57) | verified (EOIP side) | [CLAIM-pyg-01] |
| Algorithmic | GNN scores are not probabilities; GNN link predictors are over/under-confident (negatives overconfident, positives underconfident) | published research, not PyG-specific | [CLAIM-pyg-10] |
| Algorithmic | Temporal sampling prevents future neighbours but does not guard label or feature leakage | hypothesis | n/a |
| Licensing | MIT, but transitive network-capable deps (aiohttp, requests, fsspec) enlarge the air-gap review surface | verified deps; impact hypothesis | [CLAIM-pyg-01] |

## 10. Deployment, licensing, redistribution, and operational viability

| Item | Assessment |
|---|---|
| Deployment | In-process library inside an EOIP worker; offline wheel bundle from the PyTorch CPU index plus PyG PyPI wheel. No service, no egress at runtime. |
| Air-gap | **yes** once wheels are mirrored (`https://download.pytorch.org/whl/cpu/`, `https://data.pyg.org/whl/`). |
| Licence | MIT for PyG. **Legal-review trigger: yes (low)** only because of transitive PyTorch/torch-scatter/pyg-lib licences and model weights/datasets that PyG examples download (dataset licences vary). |
| H16 compliance | Install with the `+cpu` torch build only. The default `pip install torch` on Linux pulls `nvidia-*` packages; that would violate ADR-H16. Enforce with CI scan of the lock file. (Behaviour of default PyPI Linux wheels asserted from ADR-H16 context, not re-measured.) |
| One-node first | Feasible. CPU training on moderate graphs; large graphs require sampling and patience (H). |
| Multi-tenant | Train per tenant or with tenant-masked features; never share embeddings across tenants (cross-tenant leakage = P0). |

## 11. Competitive delta against the EOIP verified baseline

| EOIP item | PyG delta |
|---|---|
| BL-44 GNN/link prediction: pure-Python heuristics in `gnn/engine.py`; `LinkPredictor` / `NodeClassifier` call `require_qualified_model` and refuse unqualified models | PyG supplies real models, samplers and explainers; EOIP lacks the plane around them. |
| BL-57 numerical stack N0-N3 planned; numpy not in the lock | PyG needs numpy + torch: depends on N0/N1 extras being built first (ADR-H15). |
| BL-01 `GraphStore` protocol (CRUD + neighbourhood + bulk load) | No snapshot / tensor export; a `GraphSnapshotExporter` is needed to feed `HeteroData`. |
| Prediction plane (J8, seed hypotheses 11 and 12) | PyG offers none of: quarantine, calibration, approval, provenance. EOIP's differentiator is precisely this wrapper. |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

**STR-pyg-01** | PyG | Hetero + temporal sampling loaders | [CLAIM-pyg-06] | Learns on EOIP's typed, time-stamped graph without full-batch RAM | integrate | `SnapshotExporter` -> `HeteroData` -> `LinkNeighborLoader(time_attr, edge_label_time)` | Train on 10k-node synthetic hetero graph, CPU, peak RSS < agreed budget; no future-edge leakage in a planted-leak test.

**STR-pyg-02** | PyG | Explainer with fidelity metrics | [CLAIM-pyg-05] | Every proposed link ships with evidence an analyst can audit | integrate | Store `edge_mask` top-k subgraph as `explanation` on the proposal record | Fidelity+ and fidelity- reported for every released model; unfaithful explanation (> threshold) blocks promotion.

**STR-pyg-03** | PyG | MIT licence, CPU wheels | [CLAIM-pyg-01][CLAIM-pyg-08] | Redistributable in white-label bundles | reuse | N1 extra, hash-locked, `+cpu` | CI: zero `nvidia-*` in lock/bundle/image SBOM.

**INV-pyg-01 — Uncalibrated, unprovenanced scores**
- Target: PyG 2.8.1, link prediction on a hetero graph.
- Limitation: outputs are raw scores; no calibration module found; literature shows link-prediction GNNs are systematically miscalibrated [CLAIM-pyg-10].
- Root cause: *semantics / governance*; proven for absence in docs (not found), hypothesis for magnitude on EOIP data.
- Alternative design: calibrate in EOIP (temperature / Platt / isotonic per relation type on a time-ordered validation split; the In-n-Out edge-level approach as a later option). Worse when validation set is tiny or class balance is extreme.
- Options: (1) quick: scikit-learn isotonic/Platt in N0; (2) pragmatic: per-relation calibrators + ECE gate in the promotion pipeline; (3) long-term: learned edge-level temperature (In-n-Out style).
- Selected: option 2. Sketch: `score -> calibrator[relation, model_version] -> p_cal; store {p_raw, p_cal, ece_window, snapshot_id, model_ver}`; reject promotion if ECE > gate.
- Benchmark: hold-out time slice of an EOIP-shaped graph; success = ECE <= 0.05 and no relation with reliability slope outside 0.8-1.2; baseline = uncalibrated PyG scores.
- Dependencies: BL-57 numpy; security: calibrators are per-tenant artefacts; failure: calibrator trained on leaked data looks perfect.
- Defensibility: the calibrated, approved-edge workflow and its data are EOIP IP; PyG can't copy a governance workflow.
- Decision: **ADOPT**.

**INV-pyg-02 — Torch/native-extension version drift**
- Evidence: PyG 2.8.0 declares torch 2.9-2.12; PyPI torch is 2.14.1; wheel matrix per torch/Python/OS [CLAIM-pyg-02][CLAIM-pyg-04][CLAIM-pyg-08].
- Root cause: *maturity / deployment*; proven (versions), hypothesis (breakage).
- Alternative: pin one torch minor within the declared range (e.g. 2.12.x) in a hash-locked offline bundle; do not float. Worse: security patches in newer torch wait for PyG support.
- Options: (1) quick pin; (2) CI matrix job that tests pinned vs newest torch nightly; (3) avoid pyg-lib entirely (pure-PyG fallback).
- Selected 1 + 2. Benchmark: install the offline bundle on a clean air-gapped VM, run smoke + 3 model tests; success = green with no network; compare size against 2.5 GB budget.
- Defensibility: low (ops hygiene). Decision: **ADOPT**.

**INV-pyg-03 — Explainer instability**
- Evidence: docs warn "active development and may not be stable" [CLAIM-pyg-05].
- Alternative: treat explainers as advisory; persist the explanation plus fidelity score; fall back to deterministic evidence paths (metapath counts, shared neighbours) shown beside the GNN explanation.
- Options: (1) display only; (2) gate on fidelity; (3) in-house metapath explainer with provenance.
- Selected 2 with 3 as fallback. POC: compare GNNExplainer and AttentionExplainer masks across 5 seeds; success = top-k edge Jaccard >= 0.6 stability; otherwise explanations are labelled "unstable".
- Decision: **EXPERIMENT**.

Seed hypotheses validated: #11 (neuro-symbolic, predictions quarantined) - supported: PyG does not provide quarantine, EOIP must. #12 (temporal graph learning with leakage controls, CPU-first) - partly supported: time-constrained sampling exists, leakage controls and CPU benchmarks do not.

## 13. Per-capability decisions

| Capability | Decision | Rationale |
|---|---|---|
| CAP-64 GNN/link prediction with a prediction plane (model code) | REUSE PyG | MIT, hetero and temporal support. |
| CAP-64 prediction plane (quarantine, approval, provenance) | BUILD | No upstream equivalent. |
| CAP-63 KGE | REUSE `nn/kge` as baseline; INTEGRATE PyKEEN only if bake-off justifies (Tier B, not decided here) | |
| CAP-65 temporal graph analytics | EXPERIMENT (TGN/time sampling on CPU) | Leakage and CPU feasibility unproven. |
| CAP-24 explanation traces for predictions | INTEGRATE Explainer + EOIP evidence schema | |
| Calibration | BUILD on N0 (scikit-learn/numpy) | Absent upstream. |
| GPU path | DEFER (H-17) | |
| `GraphStore` remote sampling | EXPERIMENT | Avoids full export; unproven. |
| CAP-79 supply chain | BUILD CI gate (no `nvidia-*`, hashes) | ADR-H16. |

## 14. Concrete tests, proof-of-concept, and acceptance conditions

| ID | Test | Acceptance |
|---|---|---|
| T-PYG-01 | Offline install of `+cpu` torch + torch-geometric 2.8.1 + numpy on clean Linux and Windows without network | Imports succeed; `pip list` shows zero `nvidia-*`; installed size recorded and <= 2.5 GB |
| T-PYG-02 | R-GCN 2x128 link prediction on EOIP-shaped synthetic hetero graph (1k, 10k, 100k nodes) | Epoch time, RSS, AUC recorded (no gate until baseline set); results stored as H-17 CPU numbers |
| T-PYG-03 | Planted-leak temporal test: add a future edge feature that perfectly predicts labels | Pipeline leakage guard flags it; AUC drop after fix measured |
| T-PYG-04 | Calibration: ECE before/after per relation | ECE <= 0.05 after calibration on time-ordered split |
| T-PYG-05 | Explanation stability across 5 seeds | Jaccard >= 0.6 or label "unstable" |
| T-PYG-06 | Isolation: proposals never appear in fact-graph queries; promotion requires approval record | 0 leaks across 1,000 proposals; audit event for each approval |
| T-PYG-07 | Torch drift: nightly CI with newest torch | Pass/fail recorded; pin unchanged unless green |

## 15. Risks, trade-offs, and open research questions

| Risk / question | Note |
|---|---|
| Install weight vs air-gapped edge sites | CPU torch download is ~120-200 MB, installed size unmeasured. |
| GNN value vs heuristics | Unproven that GNN beats the existing heuristics or simple baselines (matrix factorisation, rules) on EOIP data: run baseline comparison before shipping (Master Prompt trap: do not assume ML superiority). |
| Maintenance gaps | Irregular releases; governance not verified. |
| Dataset/weights licences | Examples fetch public datasets with varied licences; keep out of distribution. |
| Open: does `GraphStore` bridge beat snapshot export? | Needs POC. |
| Open: tenant-isolation policy for shared pre-trained models | Policy decision (ADR). |
| Open: RelBench / ULTRA / PyKEEN comparison | Other registry entries. |

---

## Appendix A — Research-dimension coverage

| Dimension | Section(s) | Summary |
|---|---|---|
| D1 Identity and maturity | 1 | MIT, 2.8.1, irregular cadence, governance not verified |
| D2 Problem and workloads | 2 | Hetero/temporal link prediction, KGE |
| D3 Architecture | 4, 5 | Library; loaders, native ops, no service |
| D4 Storage and indexing | 5 | Tensor COO/CSR; no persistence beyond datasets |
| D5 Schema/semantics | 5 | Types via HeteroData keys; no ontology |
| D6 Query pipeline | N/A | Not a query engine; sampling pipeline in 5 |
| D7 Reasoning | N/A | Statistical, not logical; neuro-symbolic out of scope |
| D8 Transactions/scale | 5, 7 | In-process; sampling bounds memory |
| D9 Ingestion | 5, 11 | Needs snapshot exporter |
| D10 Identity/evidence | 9, 12 | None; EOIP must add |
| D11 Time | 3, 5 | Temporal sampling; no bitemporality |
| D12 Graph algorithms and ML | 2-5, 12 | Core strength |
| D13 Retrieval/agents | 3 | GRetriever/GraphRAG examples only |
| D14 NL querying | N/A | Not applicable |
| D15 Governance | 9, 12 | None |
| D16 Human experience | N/A | Library only |
| D17 Developer experience | 3, 9 | Strong API; unstable explain |
| D18 Trust/security | 3, 9, 10 | Checkpoint and supply-chain risks (hypothesis) |
| D19 Multi-tenancy | 10 | Per-tenant training required |
| D20 Empirical economics | 7 | Wheel sizes only; no benchmarks |
| D21 Commercial/licensing | 10 | MIT; transitive review |
| D22 Interoperability | 5 | `from_relbench`, no RDF/LPG bridge |
| D23 IP/prior art | 9 | No patents examined; NOT PUBLICLY VERIFIED |
| D24 Evaluation harness | 14 | Metrics module present; EOIP harness to build |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-62 graph algorithm library | partial (GNN, not classical) | [CLAIM-pyg-07] | BL-44 Partial | DEFER | P3 |
| CAP-63 embeddings and KGE | native (`nn/kge`) | [CLAIM-pyg-09] | BL-44 Partial | REUSE | P2 |
| CAP-64 GNN / link prediction with prediction plane | native model; plane absent | [CLAIM-pyg-03][CLAIM-pyg-10] | BL-44 Partial, BL-57 Planned | REUSE + BUILD | P2 |
| CAP-65 temporal graph analytics | native (TemporalData, sampling) | [CLAIM-pyg-06] | Absent | EXPERIMENT | P2 |
| CAP-24 explanation traces | native (Explainer) | [CLAIM-pyg-05] | Absent | INTEGRATE | P2 |
| CAP-04 single-node footprint | partial (CPU wheels) | [CLAIM-pyg-08] | BL-57 | EXPERIMENT (measure) | P2 |
| CAP-77 licensing and TCO | native (MIT) | [CLAIM-pyg-01] | n/a | REUSE | P2 |
| CAP-79 supply chain | absent upstream | [CLAIM-pyg-08] | ADR-H16 gate planned | BUILD | P1 |
| CAP-78 evaluation harness | partial (metrics) | [CLAIM-pyg-03] | Absent | BUILD | P2 |

## Appendix C — Evidence records

| CLAIM-ID | Product / version / date | Claim | Classification | Source + URL | Pub / access date | Confidence | Contradictory evidence |
|---|---|---|---|---|---|---|---|
| CLAIM-pyg-01 | torch-geometric 2.8.1, 2026-10-12 | MIT licence; Python >=3.10; deps incl. numpy, aiohttp, requests, fsspec; 2.8.1 wheel 1,325,471 B; release dates 2.6.1 2024-09-26, 2.7.0 2025-10-15, 2.8.0 2026-06-05, 2.8.0.post1 2026-07-20, 2.8.1 2026-10-12 | Officially documented (registry API) | PyPI JSON https://pypi.org/pypi/torch-geometric/json | 2026-10-12 / 2026-10-26 | 0.95 | GitHub page shows 2.8.1 as "06 Oct" (tag vs upload date) |
| CLAIM-pyg-02 | 2.8.0 / 2.8.0.post1 | Adds PyTorch 2.11-2.12 (docs: 2.9-2.12 supported), Python 3.10-3.14, `from_relbench`, GAT TorchScript dropped, GraphRAG QA example (vLLM or NIM); torch-cluster/spline-conv deprecated for pyg-lib 0.7.0 | Officially documented | CHANGELOG https://raw.githubusercontent.com/pyg-team/pytorch_geometric/2.8.1/CHANGELOG.md; releases https://github.com/pyg-team/pytorch_geometric/releases | 2026-06-05 / 2026-10-26 | 0.9 | none |
| CLAIM-pyg-03 | 2.6.0, 2.7.0 | 2.7.0: hetero support for Attention/PG/GNNExplainer, LPFormer, new link-pred metrics, BidirectionalSampler; 2.6.0: LinkPredMRR, HeteroJumpingKnowledge, GRetriever | Officially documented | GitHub releases page (above) | 2024-09 / 2025-10 / 2026-10-26 | 0.85 (page text summarised by a tool) | none |
| CLAIM-pyg-04 | docs latest | `pip install torch_geometric` needs only PyTorch; pyg-lib, torch-scatter, torch-sparse optional; wheels at data.pyg.org/whl with a `cpu` option for torch 2.4-2.12; no size statements; conda unavailable above torch 2.5.0 | Officially documented | https://pytorch-geometric.readthedocs.io/en/latest/install/installation.html | n/a / 2026-10-26 | 0.9 | PyPI lists numpy as mandatory, so "only PyTorch" is incomplete |
| CLAIM-pyg-05 | docs latest | Explainer, 6 algorithms, model vs phenomenon, mask/threshold types, HeteroExplanation, fidelity / unfaithfulness metrics; page warns module may not be stable | Officially documented | https://pytorch-geometric.readthedocs.io/en/latest/modules/explain.html | n/a / 2026-10-26 | 0.9 | warning text may be stale |
| CLAIM-pyg-06 | docs latest | NeighborLoader, LinkNeighborLoader, HGTLoader, Cluster, GraphSAINT, ShaDow, TemporalDataLoader; `time_attr`, `temporal_strategy`, `input_time`, `edge_label_time`; temporal sampling sets `disjoint=True`; hetero supported | Officially documented | https://pytorch-geometric.readthedocs.io/en/latest/modules/loader.html | n/a / 2026-10-26 | 0.85 (second half of page unread) | none |
| CLAIM-pyg-07 | docs latest | `Data`, `HeteroData`, `TemporalData`; `FeatureStore` / `GraphStore` ABCs; Database backends | Officially documented | https://pytorch-geometric.readthedocs.io/en/latest/modules/data.html | n/a / 2026-10-26 | 0.9 | none |
| CLAIM-pyg-08 | PyTorch CPU wheels | torch 2.12.0+cpu cp312 manylinux x86_64 = 192,268,791 B; torch 2.14.1+cpu cp312 manylinux = 196,253,677 B; win_amd64 = 123,996,008 B; PyPI torch latest 2.14.1 | Reproduced (HTTP HEAD Content-Length) | https://download.pytorch.org/whl/cpu/ ; https://pypi.org/pypi/torch/json | 2026-10-26 | 0.9 (download size, not install size) | none |
| CLAIM-pyg-09 | 2.8.1 source | `torch_geometric/nn/kge/__init__.py` exports KGEModel, TransE, ComplEx, DistMult, RotatE | Observed in source code | https://raw.githubusercontent.com/pyg-team/pytorch_geometric/2.8.1/torch_geometric/nn/kge/__init__.py | n/a / 2026-10-26 | 0.95 | none |
| CLAIM-pyg-10 | arXiv 2403.04605 | GNN link predictors are overconfident on negatives and underconfident on positives; standard temperature scaling is a poor fit; no PyG calibration module was found by search | Third-party report + absence-of-evidence | https://arxiv.org/pdf/2403.04605 | 2024 / 2026-10-26 | 0.6 (absence claim weak) | PyG may hold calibration code in a place not searched |

## Appendix D — Assumptions

- Brief date 2026-10-18 recorded as verification date; actual fetches used the session clock 2026-10-26.
- GitHub API unavailable (rate-limited), so repository activity, stars and governance are unverified; confidence capped accordingly.
- PyG internals (sampler, TGN, Explainer bodies) not read; reconstruction rows labelled H derive from public design and doc text.
- Installed-size and throughput were not measured; only download sizes are stated.
- PyG Temporal, DGL, PyKEEN, ULTRA, RelBench are separate registry entries and not assessed here.
