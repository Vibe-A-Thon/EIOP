# Cohort 13 - Graph ML frameworks and classical graph algorithm libraries

| Field | Value |
|---|---|
| Cohort ID | COH-13 |
| Workload class | GNN and knowledge-graph-embedding training/inference (CPU-only), and classical graph algorithms (paths, centrality, community, similarity) used for features, analytics and as GNN baselines |
| Members, graph ML | [pyg](../04-COMPETITOR-DEEP-DIVES/C11-pyg.md), [dgl](../04-COMPETITOR-DEEP-DIVES/C11-dgl.md), [pykeen](../04-COMPETITOR-DEEP-DIVES/C11-pykeen.md), [ultra](../04-COMPETITOR-DEEP-DIVES/C11-ultra.md), [relbench](../04-COMPETITOR-DEEP-DIVES/C11-relbench.md) |
| Tier C, graph ML | [C11-tier-c-records-V24](../04-COMPETITOR-DEEP-DIVES/C11-tier-c-records-V24.md): GraphStorm, AmpliGraph, DGL-KE, PyTorch Geometric Temporal, GraphGym, Graphormer/GraphGPS, TGN, TorchKGE/LibKGE, neuro-symbolic frameworks (Scallop, DeepProbLog, LTN) |
| Members, classical algorithms | [networkx](../04-COMPETITOR-DEEP-DIVES/C12-networkx.md), [igraph](../04-COMPETITOR-DEEP-DIVES/C12-igraph.md), [rustworkx](../04-COMPETITOR-DEEP-DIVES/C12-rustworkx.md), [graphblas](../04-COMPETITOR-DEEP-DIVES/C12-graphblas.md), [raphtory](../04-COMPETITOR-DEEP-DIVES/C12-raphtory.md) |
| Tier C, classical algorithms | [C12-tier-c-records-V25](../04-COMPETITOR-DEEP-DIVES/C12-tier-c-records-V25.md): GraphX/GraphFrames (Spark), RAPIDS cuGraph, Graphology, Ligra and the GAP benchmark suite |
| Reference columns | HugeGraph, Neo4j, Neptune, EOIP @HEAD 896e06d (BL-IDs from `01-SYSTEM-BASELINE.md`, status from `01a-BASELINE-DELTA-HEAD.md`) |
| Date | 2026-10-26 |

## 1. Workload class and comparison basis

**Customer workloads.** (a) Classical graph analytics (shortest paths, centrality, community detection, similarity, anomaly) over the knowledge graph for features and investigation; (b) learned link prediction, node classification and knowledge-graph embedding as a prediction plane; (c) temporal graph analytics; (d) all of the above on a single CPU-only node, air-gapped, under the constraints in `docs/decisions/ADR-H15-numerical-stack-tiers.md` (CPU-only numerical tiers N0-N3), `ADR-H16-no-cuda-redistribution.md` (no CUDA package or NVIDIA-licensed artifact is ever distributed) and `ADR-H17-gpu-availability.md` (open; every gate is qualified CPU-only in the interim, and a learned architecture that needs a GPU to pass is recorded `DEFERRED (H-17)`, not promoted).

**Why comparable.** Every member is a library EOIP would embed in a worker process, not a managed service, so the comparison is about CPU feasibility, licence, maintenance and algorithm coverage, not about a hosted product. Classical libraries are the test oracles and fast paths beneath BL-43; graph-ML libraries are candidates for the BL-44/BL-57 prediction plane that the current `neural/*` code cannot execute because `torch` is absent from every lock (01a BL-44).

**Excluded.** GPU-only or CUDA-coupled items (RAPIDS cuGraph, Graphormer's implicit GPU assumption) are kept as REFERENCE-ONLY per ADR-H16/H17 and are not candidates for BUILD/INTEGRATE. Spark GraphX/GraphFrames are reference-only because they imply a cluster, not a one-node deployment.

**Evidence quality.** No dive in C11 or C12 ran its own benchmark; all performance figures are vendor claims or a single third-party benchmark from 2020 (networkx/igraph) that both dives flag as old and competitor-authored. CPU timing for every learned model (ULTRA, RelBench's GNN examples, PyKEEN) is explicitly "NOT PUBLICLY VERIFIED" in its dive.

## 2. Capability comparison

Values: native / partial / absent / unknown, with claim IDs as written in the dives.

### 2.1 Graph ML (knowledge-graph embedding, GNN, link prediction)

| CAP | PyG | DGL | PyKEEN | ULTRA | RelBench | HugeGraph | Neo4j | Neptune | EOIP @HEAD |
|---|---|---|---|---|---|---|---|---|---|
| CAP-63 embeddings/KGE | native: `KGEModel`, TransE, ComplEx, DistMult, RotatE (pyg-09) | partial via DGL-KE, redirected to GraphStorm (dgl-05) | native: 40 models, 37 datasets, 5 inductive, 15 losses, 40 metrics, Optuna (pykeen-01) | native scoring only (ultra-01) | n/a | HugeGraph-ML: 21 DGL/PyTorch GNN models (hugegraph-29, cohort 06 cross-ref) | n/a | n/a | Absent in BL list; candidate for BUILD per pykeen evaluator design |
| CAP-64 GNN / link prediction with a prediction plane | native: NeighborLoader, LinkNeighborLoader, HGTLoader, GraphSAINT (pyg-06) | native framework (dgl-01) | partial: no calibration/explainability (pykeen-03) | native, scoring only, zero-shot (ultra-01) | partial: relational deep learning examples (relbench-04) | library (hugegraph-29) | n/a | n/a | **Partial**: `gnn/engine.py` pure-Python node2vec/TransE-style heuristics; `neural/encoders.py` (R-GCN, GraphSAGE, R-GAT, HGT, GraphGPS, ChebNet) imports `torch` at module top and **fails to import**, not in any lock (BL-44, 01a) |
| CAP-24 explanation/calibration | partial, explicitly unstable (pyg-05); GNN link predictors overconfident on negatives, underconfident on positives, no calibration module found (pyg-10) | absent | absent: "Uncertainty" docs page exists but no calibration/explainability (pykeen-03) | absent (ultra-01) | absent | unknown | n/a | n/a | **Absent** (CAP-43/24 both flagged absent across every member in the Appendix B rows) |
| CAP-43 epistemic separation on predictions | absent | absent | absent (pykeen-03) | absent (ultra-01) | absent (relbench-01) | unknown | n/a | n/a | BL-40 contract exists (PROPOSED-until-validated) but is not wired to any learned-model output |
| CAP-65 temporal graph ML | native: `TemporalData`, `time_attr`, `temporal_strategy`, disjoint sampling (pyg-06) | absent (dgl dive) | absent (transductive by default; temporal ignored, pykeen dive) | absent (tested 1k-120k node static graphs, ultra-03) | native: temporal split API (relbench-01) | unknown | n/a | n/a | In-process heuristics only (BL-43/44); no temporal GNN |
| CAP-78 leakage-safe evaluation | filtered evaluation not inherent to PyG itself | unknown | native: filtered evaluation, `Sealant` leakage module (pykeen-03) | zero-shot transfer protocol across 57 datasets (ultra-03) | native: temporal split API is the headline feature (relbench-01) | unknown | n/a | n/a | **Absent**; no leakage-safe harness exists |
| Torch/CPU installability | Declared torch 2.9-2.12 while PyPI torch is 2.14.1: version-range mismatch (pyg-02, -08); CPU wheel ~183-196 MiB verified by HTTP HEAD | No current CPU wheel: PyPI pinned at 2.2.1 (2024-05-13), wheels only for torch 2.4-2.6, torch 2.7+ returns HTTP 403 (dgl-02, -03) | `torch>=2.0`, no nvidia packages in declared deps (pykeen dive) | Python 3.9/torch 2.1/PyG 2.4 pins, stale (ultra-01) | PyG-based examples inherit PyG's torch coupling (relbench-04) | n/a | n/a | n/a | `torch` absent from every lock including `requirements-neural.lock`, which is mislabelled (01a BL-57, U-13) |
| Licence | MIT (pyg-01) | Apache-2.0 (dgl-01) | MIT (pykeen-02) | MIT, pre-training datasets have separate terms (ultra-01) | Apache-2.0 (relbench-01) | Apache-2.0 | n/a | n/a | n/a |

### 2.2 Tier C graph ML (reference-only unless noted)

| Item | Status | Licence | Decision | Reason |
|---|---|---|---|---|
| GraphStorm (AWS) | Active, 0.5.1 (graphstorm-01) | Apache-2.0 | REFERENCE-ONLY | DGL coupling conflicts with ADR-H15 |
| AmpliGraph (Accenture) | Active, 2.2.0 (ampligraph-01) | Apache-2.0 | REJECT as dependency, REFERENCE for API shape | TensorFlow framework mismatch |
| DGL-KE | Maintenance, redirects to GraphStorm (dgl-ke-01) | Apache-2.0 | REJECT | Superseded by GraphStorm and PyKEEN |
| PyTorch Geometric Temporal | Maintenance, 0.56.2 (pyg-temporal-01) | MIT | DEFER | Snapshot models fit node time-series, not EOIP's event-style graph |
| GraphGym | Dormant since 2023-03-14 (graphgym-01) | MIT (licence text not fully re-read) | REFERENCE-ONLY | — |
| Graphormer / GraphGPS | Maintenance (README only) / dormant (graph-transformers-01, -02) | MIT | REFERENCE-ONLY, likely `DEFERRED (H-17)` | Azure-only advanced Graphormer models; GPU-oriented |
| TGN (Twitter Research) | Dormant since 2023-06-21 (tgn-01) | Apache-2.0 | EXPERIMENT via PyG's TGN, not this repo | — |
| TorchKGE / LibKGE | Dormant / maintenance (torchkge-libkge-01) | BSD / MIT | REFERENCE-ONLY (LibKGE configs); REJECT TorchKGE | — |
| Scallop, DeepProbLog, LTN | Active / active / maintenance (neuro-symbolic-01) | MIT / Apache / MIT (LTN unconfirmed) | REFERENCE-ONLY; EXPERIMENT later | Provenance-semiring idea only if rules plus learned scores are needed |

### 2.3 Classical graph algorithms

| CAP | NetworkX | igraph | rustworkx | python-graphblas | Raphtory | EOIP @HEAD |
|---|---|---|---|---|---|---|
| CAP-62 algorithm library | native: Louvain, Leiden, LPA and more, dispatches to graphblas-algorithms plugin (networkx-02, -03) | native: full community function list (igraph-03) | partial: no community detection, no k-hop helper, no anomaly/sampling (rustworkx-03) | native: k-truss and more via graphblas-algorithms, about 10x faster than native NetworkX on a 5,000-node graph including conversion, vendor claim (graphblas-04) | native but no classical-algorithm focus (temporal is the point) | Implemented in-process: `graph/algorithms.py`, `graph/community.py`, `graph/paths.py`, `graph/anomaly.py`; pure Python, scale untested (BL-43) |
| CAP-19 multi-hop/path queries | native: cutoff BFS, VF2 (networkx-02) | native (igraph-03) | partial (rustworkx-03) | native BFS (graphblas-01) | unknown | BL-43 in-process |
| CAP-65 temporal analytics | absent | absent | absent | absent | native: the library's reason for existing (raphtory-01, -03) | Absent as a dedicated capability |
| CAP-34 bitemporal | n/a | n/a | n/a | n/a | partial: single valid-time model, not bitemporal (hypothesis, raphtory dive) | Implemented application-layer bitemporal (BL-37), independent of this cohort |
| CAP-04 footprint | Pure-Python wheel, 2.14 MB (networkx-01) | C core; wheel 5.68 MB linux, 3.22 MB windows (igraph-01) | Rust; wheel 2.37 MB x86_64, 2.28 MB windows, free-threaded cp314t wheel exists (rustworkx-01) | SuiteSparse C library; wheels 21-24 MB, JIT needs a compiler, 24 MB binary (graphblas-02, dive) | Rust; wheel grew 3x to about 93 MB by 0.17.0, and 0.18.5 lists no Linux/Windows wheel files, source build or fallback to 0.17.0 needed (raphtory-02) | In-process, no extra binary |
| Licence | BSD-3-Clause (networkx-01) | **GPL-2.0** (python-igraph); C core licence to verify (igraph-01, -02) | Apache-2.0, patent grant (rustworkx-01) | Apache-2.0; bundled LZ4/xxHash/ZSTD BSD; logo CC BY 4.0, do not ship (graphblas-01) | **GPL-3.0** core; commercial split for out-of-memory scale (raphtory-01) | n/a |

### 2.4 Tier C classical algorithms

| Item | Status | Licence | Decision |
|---|---|---|---|
| GraphX / GraphFrames (Spark) | GraphX alpha stage; GraphFrames active (graphx-01, -02) | Apache-2.0 | REFERENCE-ONLY; export-to-Parquet path for Spark customers, no embedded dependency |
| RAPIDS cuGraph | Active, 26.10.0 (cugraph-01) | Apache-2.0 code; CUDA/cuDF/CuPy stack under NVIDIA terms, not assessed (cugraph-02) | **REJECT** as bundled dependency per ADR-H16 (cugraph-04); REFERENCE-ONLY for algorithm coverage; revisit under ADR-H17 |
| Graphology | Active but uneven, standard bundle "often lags behind" per its own README (graphology-01, -02) | MIT | **REUSE (already in use)**: EOIP web depends on `graphology ^0.25.4` and `sigma ^2.4.0` (graphology-03, `apps/web/package.json`) |
| Ligra and the GAP benchmark suite | Reference/academic (gap-01, -02, ligra-01) | MIT / BSD-style (gapbs licence variant unverified) | REFERENCE-ONLY; adopt the GAP kernel set and methodology into the CAP-78 benchmark harness |

## 3. Operational and licensing comparison

| Member | Licence class | Redistribution / OEM trigger | One-node footprint | Air-gap | Maintenance |
|---|---|---|---|---|---|
| PyG | MIT | Low: transitive torch/torch-scatter/pyg-lib licences and example dataset licences vary (pyg dive) | Needs CPU-only torch wheel (~183-196 MiB) plus PyG wheel; no service | Yes once wheels are mirrored from `download.pytorch.org/whl/cpu/` and `data.pyg.org/whl/` | Declared torch range (2.9-2.12) trails installed torch (2.14.1); irregular release gaps, 13 months between 2024-09 and 2025-10 (pyg-01, -02) |
| DGL | Apache-2.0 | None found | Native build per torch version | Yes in principle, offline wheels | **No release since 2024-08**; PyPI wheel pinned to 2.2.1, wheels for torch 2.4-2.6 only, torch 2.7+ returns HTTP 403 (dgl-02, -03) |
| PyKEEN | MIT | None | Pure PyTorch, library-only | Needs `pystow` disabled (it downloads data on demand) | One release in 18 months (pykeen dive) |
| ULTRA | MIT | Pre-training datasets (FB15k237, WN18RR, CoDEx, NELL995) carry their own terms; legal review advisable for weight redistribution (ultra-01) | CPU path exists via `--gpus null` | Viable if the kernel is pre-built | Newest commit 2025-02-03; not a package (ultra-02) |
| RelBench | Apache-2.0 | Dataset licences, especially third-party ones, not stated (relbench-03) | GNN examples need PyG, inheriting its coupling | Viable if Hub datasets are mirrored | v3 breaking changes; label regeneration changed counts between versions (relbench-03) |
| NetworkX | BSD-3-Clause | None | Pure Python, 2.14 MB wheel | Trivial | Active, 3.7; `nx-cugraph` GPU backend excluded by ADR-H16 (networkx-01) |
| **igraph** | **GPL-2.0** (python-igraph) | **Legal-review trigger**; EOIP policy treats GPL/AGPL as a hard constraint (project memory: ontology strategy) | C core, 5.68 MB wheel | Yes | Active, 1.0.0 (igraph-01, -02) |
| rustworkx | Apache-2.0, patent grant | None | Rust, 2.37 MB wheel | Trivial | Pre-1.0; speed claims unverified (rustworkx-01, -02) |
| python-graphblas | Apache-2.0 | None; do not ship the CC BY 4.0 logo (graphblas-01) | SuiteSparse C, 21-24 MB wheel, JIT needs a compiler | Needs a JIT cache or compiler decision for air-gap | Wrapper pin conflict: `python-graphblas 2025.2.0` pins `suitesparse-graphblas<10` while the available wheel is 10.5.1.1 (graphblas-03) |
| **Raphtory** | **GPL-3.0** core; commercial split for out-of-memory scale | **Legal-review trigger** for embedding or redistribution in wheels or containers | Wheel grew 3x to about 93 MB; 0.18.5 has no Linux/Windows wheel listed (raphtory-02) | Wheels install offline when available | Pre-1.0; docs URL for v0.16 algorithms returns 404 (raphtory dive) |

## 4. Performance evidence

| Figure | Source | Class | Comparable? |
|---|---|---|---|
| NetworkX 2.4 vs igraph 0.8.2 (2020, Intel i9-9980HK, PGP web-of-trust graph, 39,796 nodes / 301,498 edges): SSSP 0.25s vs 0.0092s; PageRank 1.54s vs 0.072s; global clustering 7.94s vs 0.027s; betweenness about 10,297s vs 198s | networkx-04, igraph-04 | Third-party, competitor-authored (graph-tool's author), old versions, single machine | Internally consistent between the two dives but not to current NetworkX 3.7 or to EOIP's pure-Python implementation |
| igraph vs graph-tool: 1.1x to 4x slower single-threaded; 25x to 300x faster than NetworkX | igraph-04 | Same source | Same caveats |
| graphblas-algorithms: about 10x faster than native NetworkX for k-truss on a 5,000-node random graph, including conversion | graphblas-04 | Vendor claim, small graph | Not comparable to EOIP graphs |
| ULTRA: zero-shot averages MRR 0.444/Hits@10 0.588 (inductive-e); beats tailored baselines by about 15% on 50+ graphs of 1k-120k nodes, single RTX 3090 | ultra-01, -03 | Authors' own, GPU | Not CPU-comparable; a different-author paper (arXiv:2410.12609) reports its own method beating ULTRA on most metrics under identical conditions (ultra-04) |
| RelBench: RDL beats manual feature engineering per a one-data-scientist user study | relbench-05 | Authors' own, small sample | Weak evidence; a 2026-08 preprint says the manual baseline is a reference, not a ceiling, and a flattened single-table approach is competitive (relbench-06) |

**No CPU timing exists for any learned model in this cohort** (PyG, DGL, PyKEEN, ULTRA, RelBench's GNN examples all say "NOT PUBLICLY VERIFIED" or "no benchmark run"). No benchmark of EOIP's own `gnn/engine.py` or `graph/algorithms.py` at scale exists either (01a, BL-43 "scale untested"). No winner can be named.

## 5. Findings

1. **EOIP's prediction plane is currently unqualifiable, not merely weak.** `neural/encoders.py` imports `torch` at module top and fails to import in every shipped environment; `torch` is absent from `requirements.lock`, `requirements-numerics.lock` and the misleadingly-named `requirements-neural.lock` (01a BL-44, BL-57, U-13). Under ADR-H15/H17 this means N1/N2 are `UNQUALIFIED`, not `DEFERRED (H-17)`, because no CPU build has even been attempted.
2. **Every CPU-capable graph-ML candidate has a currency problem.** PyG declares support for torch 2.9-2.12 while PyPI's current torch is 2.14.1 (pyg-02, -08); DGL has had no release since 2024-08 and its wheels stop at torch 2.6, returning HTTP 403 for 2.7+ (dgl-02, -03); PyKEEN has shipped one release in 18 months (pykeen dive). None of these is a drop-in CPU-safe dependency today without a version-pin decision.
3. **GPL/AGPL is a hard blocker for two of the five classical-algorithm candidates.** python-igraph is GPL-2.0 (igraph-01, -02) and Raphtory's core is GPL-3.0 with a commercial split for scale (raphtory-01). Per project memory ("GPL/AGPL is a hard constraint"), both need legal review before any embedding, and the EOIP-authored `graph/algorithms.py` already covers their common ground, untested at scale.
4. **No member provides calibration, explainability, or epistemic separation on predictions.** CAP-24 and CAP-43 are marked absent across PyG, DGL, PyKEEN, ULTRA and RelBench (section 2.1); the one independent fact found is that GNN link predictors are systematically overconfident on negative edges and underconfident on positive ones, and standard temperature scaling is a poor fit (pyg-10). EOIP's BL-40 epistemic contract exists but is not connected to any learned-model output.
5. **Leakage-safe temporal evaluation exists in exactly two members, and neither is a drop-in harness.** PyKEEN's `Sealant` module and RelBench's temporal split API are the only CAP-78-relevant designs found (pykeen-03, relbench-01); RelBench's own benchmark v3 changed label-regeneration counts between versions (relbench-03), which is itself a leakage/reproducibility risk to watch when adopting its protocol.
6. **The classical-algorithm speed gap between pure Python and compiled libraries is large on the one benchmark found, but it is twelve-year-old data from a competitor.** 25x to 300x (igraph vs NetworkX 2.4, igraph-04) should not be treated as current or as representative of EOIP's graph shapes; it only motivates measuring EOIP's own `graph/algorithms.py`, which is untested at scale (BL-43 note).
7. **Licence-clean, CPU-friendly classical options exist and avoid the GPL/AGPL issue: NetworkX (BSD-3), rustworkx (Apache-2.0) and python-graphblas (Apache-2.0, logo excluded).** rustworkx explicitly lacks community detection and k-hop helpers (rustworkx-03), so it is a partial accelerator, not a NetworkX replacement; graphblas-algorithms needs numpy, which is not in the runtime lock today (graphblas dive note; numpy is in `requirements-numerics.lock` per 01a).
8. **Dataset and weight licensing is a second, separate legal-review surface from the library licence.** ULTRA's pre-training datasets and RelBench's Hub datasets carry their own terms, not reviewed here (ultra-01, relbench-03); this is distinct from the Apache-2.0/MIT code licences and must be checked before redistributing any pre-trained weights.
9. **Tier C confirms there is no missing "ready" graph-ML framework being overlooked.** GraphStorm, AmpliGraph, DGL-KE, PyTorch Geometric Temporal, GraphGym, Graphormer/GraphGPS, TGN, TorchKGE/LibKGE are each REFERENCE-ONLY, REJECT or DEFER, mostly for the same reasons as PyG/DGL (framework coupling, dormancy, or GPU orientation) (section 2.2).
10. **EOIP's web stack already reuses one Tier C classical item (Graphology) and should continue to.** `apps/web/package.json` depends on `graphology ^0.25.4` and `sigma ^2.4.0` (graphology-03); this is unrelated to the server-side algorithm question and should not be conflated with BL-43.

## 6. Implications for EOIP

Respecting backend neutrality and ADR-H15/H16/H17: a prediction plane must run CPU-only in every distributed artifact, and any GPU use is customer-provisioned and non-binding until H-17 is decided.

| CAP | Parity needed | Exploitable weakness | Decision | Candidate gap statement |
|---|---|---|---|---|
| CAP-44 GNN/link prediction (BL-44) | PyG's `KGEModel` family (pyg-09) and PyKEEN's filtered evaluation (pykeen-03) as design references | `neural/encoders.py` cannot import; `gnn/engine.py` is a pure-Python heuristic | **BUILD, P0**: pin and vendor a CPU-only torch wheel (per ADR-H15/H16), smoke-test `neural/encoders.py` import, then re-qualify | No learned model has ever executed in a shipped EOIP environment; this is a qualification gap, not an algorithm gap. |
| CAP-63 embeddings/KGE | PyKEEN's 40-model, 37-dataset evaluator design (pykeen-01) | No calibration or explainability anywhere in the cohort (CAP-24 absent row) | **EXPERIMENT, P1**: adopt PyKEEN's evaluator design, not the dependency, inside EOIP's own training loop | Build calibration on top of BL-40's epistemic contract before promoting any learned score. |
| CAP-78 leakage-safe evaluation | PyKEEN `Sealant`; RelBench temporal split API; GAP benchmark kernels (gap-01, -02) | No EOIP harness exists; RelBench's own label counts changed between versions (relbench-03) | **BUILD, P0** | A leakage-safe, versioned evaluation harness is a precondition for promoting any CAP-44/63/65 capability past `DEFERRED`. |
| CAP-62 algorithm library | rustworkx (Apache-2.0, fast, incomplete) and python-graphblas (Apache-2.0, k-truss about 10x) as optional accelerators behind the existing `GraphStore`-neutral interface | igraph and Raphtory are GPL/AGPL-class; EOIP's own `graph/algorithms.py` is untested at scale | **EXPERIMENT, P1**: benchmark `graph/algorithms.py` against rustworkx/graphblas on EOIP-shaped graphs using the GAP kernel methodology; **REJECT** igraph and Raphtory as embedded dependencies pending legal review | "Available upstream / not integrated": NetworkX-class algorithms are not missing from EOIP, they are implemented in-house and simply unmeasured. |
| CAP-65 temporal graph analytics | Raphtory's design (not its GPL code); PyG's `TemporalData` API shape (pyg-06) | No temporal GNN or temporal classical-algorithm layer exists in EOIP | **DEFER, P2** | Bitemporal facts already exist at the data layer (BL-37); temporal graph analytics on top of them is unbuilt. |
| CAP-77 licence/TCO | — | igraph GPL-2.0, Raphtory GPL-3.0 (legal-review trigger, hard constraint per project memory) | **REJECT** both as embedded dependencies | Record only; no conclusion without counsel. |
| CAP-50 air-gap | PyG/DGL wheel-mirroring pattern (`download.pytorch.org/whl/cpu/`, `data.pyg.org/whl/`) | DGL's wheels trail current torch and 403 on 2.7+ | **DEFER** DGL; **EXPERIMENT** PyG with a pinned, mirrored CPU wheel set | DGL's install path is currently broken for any torch newer than 2.6; do not adopt until this is resolved upstream. |

## 7. Open questions

1. Can a CPU-only torch wheel be installed and `neural/encoders.py` imported successfully in a clean environment matching EOIP's deployment lock, and what does that change for BL-44/BL-57 status? (No evidence either way; 01a records only the import failure.)
2. What is EOIP's own `graph/algorithms.py` throughput at 1M+ nodes, and how does it compare to rustworkx and python-graphblas using the GAP kernel set? (U-06, open.)
3. Is a legal review of igraph (GPL-2.0) and Raphtory (GPL-3.0) already scheduled, and what alternative closes the temporal-analytics gap if Raphtory is rejected?
4. Which pre-trained weights or datasets (ULTRA's FB15k237/WN18RR/CoDEx/NELL995, RelBench's Hub datasets) would EOIP ever redistribute, and have their individual licences been reviewed? (ultra-01, relbench-03, both open.)
5. Does PyKEEN's `Sealant` leakage module or RelBench's temporal split API transfer cleanly to EOIP's own bitemporal fact model (BL-37), or does a native evaluator need to be built from scratch?
6. Should DEFERRED (H-17) status be recorded now for any CAP-64 row, or does the "never attempted" state (finding 1) mean no gate has been evaluated at all, so `UNQUALIFIED` is the only honest label?
