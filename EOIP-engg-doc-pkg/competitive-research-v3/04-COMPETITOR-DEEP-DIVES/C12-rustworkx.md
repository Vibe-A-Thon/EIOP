# C12 — Rustworkx

| Field | Value |
|---|---|
| Registry ID | T-C12-rustworkx |
| Tier | B (Apache-2.0 fast algorithms) |
| Versions examined | rustworkx 0.18.1 (PyPI 2026-07-30) |
| Verified on | 2026-10-26 |
| Worker | V25 |

## 1. Identity, status, sources
Rust-core graph library for Python, API modelled on NetworkX; arXiv:2110.15221 (Treinish, Carvalho, Tsilimigkounakis, Sá; v4 2022-11-02) [CLAIM-rustworkx-02]. PyPI 0.18.1, Apache-2.0, `>=3.10`, released 2026-07-30 [CLAIM-rustworkx-01]. Maintaining organisation: Qiskit-associated (stated from general knowledge; GitHub page not retrieved: UNVERIFIED, 0.4). Sub-1.0 version number: API may still break.

## 2. Problem and workloads
Performance-sensitive graph algorithms inside Python apps (originally quantum-circuit DAG processing). Workflow: `PyDiGraph.add_edges_from`, `rx.dijkstra_shortest_paths`, `rx.vf2_mapping`.

## 3. Feature inventory (0.18.1 API index) [CLAIM-rustworkx-03]
| Area | Status |
|---|---|
| Centrality: betweenness, closeness, degree, eigenvector, Katz, group variants | present |
| Shortest paths: Dijkstra, Bellman-Ford, Floyd-Warshall, A*, k-shortest lengths | present |
| Subgraph matching: `is_subgraph_isomorphic`, `vf2_mapping` | present |
| k-hop | partial (`bfs_layers`, descendants/ancestors; no k-hop neighbourhood function seen) |
| PageRank, HITS | present |
| Community detection (Louvain/Leiden/LPA) | **absent** (not in API index) |
| Connectivity, cycles, articulation, bridges, core number, MST, Steiner, matching, colouring, dominators, planarity | present |
| Anomaly detection, sampling, embeddings | absent (random paths only) |
| Parallelism | partial (rayon in some functions: UNVERIFIED which) |
| Persistence/server/tenancy | absent |

## 4. Architecture
```
Python API (PyGraph/PyDiGraph, integer node indices, payload = Python object)
   -> PyO3 -> Rust core (petgraph-derived StableGraph, rayon in places)
```

## 5. Reconstruction
Rust petgraph-style adjacency (hypothesis: derived from petgraph, noted in project descriptions, unverified here, 0.5). Nodes/edges are integer indices; arbitrary Python payloads attach to nodes/edges, so algorithms with weight callbacks (`weight_fn`) re-enter Python and lose speed (hypothesis). abi3 wheels (cp310-abi3) avoid per-Python-version builds. No transactions, no security.

## 6. Requirements inferred
Index-based IDs; payloads opaque to core; NetworkX-like names for migration; stable-index removal semantics.

## 7. Performance and resource model
No independent benchmark found in this pass. The paper abstract claims only that it addresses NetworkX performance concerns and gives no figures; no igraph comparison [CLAIM-rustworkx-02]. Treat speed as UNVERIFIED (0.3). Footprint: wheel 2.37 MB x86_64 manylinux2014, 2.28 MB win_amd64; free-threaded cp314t wheel exists (2.34 MB) [CLAIM-rustworkx-01]. Failure modes: Python-callback weights, missing algorithms.

## 8. Strengths
Smallest wheel of the compiled options (2.4 MB), Apache-2.0, abi3 wheels incl. aarch64, s390x, ppc64le (useful for on-prem enterprise hardware); VF2 and Dijkstra/A* in Rust; NetworkX-like API eases a drop-in engine.

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | no community detection, no k-hop helper, no anomaly/sampling |
| Friction | pre-1.0; integer index semantics differ from NetworkX; Python weight callbacks |
| Maturity | speed claims unverified |

## 10. Deployment, licensing
Apache-2.0, permissive, patent grant; no legal trigger. Offline wheel 2.4 MB; CPU only; no cloud. Qualifies as cleanest redistributable accelerator.

## 11. Delta vs baseline
BL-43 pure-Python shortest paths/centrality (`graph/paths.py`, `algorithms.py`) vs compiled equivalents; EOIP additionally has community.py (380 lines) and anomaly.py (318 lines), which rustworkx lacks. numpy not in lock; rustworkx needs numpy? UNVERIFIED (depends on `numpy>=1.16` in the project metadata, not checked).

## 12. Cards
`STR-rustworkx-01 | rustworkx | 2.4 MB Apache-2.0 compiled path/centrality/VF2 with multi-arch wheels | CLAIM-01,03 | cheap permissive acceleration for BL-43 | integrate | optional engine behind `GraphAlgorithms` interface fed by a tenant-filtered index snapshot | same results as pure-Python on 1,000 random graphs; >=10x speedup on 10^6 edges (to be measured)`
INV-rustworkx-01 — target 0.18.1, community detection absent. Root cause: scope/maturity (proven by API index). Options: (a) keep EOIP community.py, (b) native Leiden in numpy/Rust, (c) GraphBLAS Louvain. Selected: (a) now, (b) after benchmark. POC: Louvain on 10^6 edges within 30 min budget. Decision: DEFER. No seed hypothesis targets rustworkx.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-62 shortest-path/centrality/VF2 engine | EXPERIMENT (INTEGRATE if POC passes) |
| CAP-62 community detection | BUILD/keep EOIP |
| CAP-19 k-hop | BUILD (BFS on CSR) |

## 14. Tests
Differential vs EOIP `paths.py`; benchmark SNAP road graph and LDBC-size graph; acceptance: >=10x on Dijkstra and betweenness-sampled; wheel hash recorded in offline bundle; confirm numpy dependency.

## 15. Risks
Pre-1.0 API; speed unverified; maintaining-org dependency; index-vs-ID mapping bugs could cross tenant data if snapshots are shared across tenants (one snapshot per tenant).

## Appendix A
| Dim | Sec | Summary |
|---|---|---|
| D1 | 1,10 | Apache-2.0, 0.18.1 |
| D2 | 2 | embedded algos |
| D3 | 4 | PyO3 + Rust |
| D4 | 5 | index graph |
| D5 | N/A | payloads |
| D6 | N/A | |
| D7 | N/A | |
| D8 | N/A | in-process |
| D9 | N/A | |
| D10 | N/A | |
| D11 | N/A | |
| D12 | 3 | algos only |
| D13 | N/A | |
| D14 | N/A | |
| D15 | N/A | |
| D16 | N/A | |
| D17 | 3 | NetworkX-like API |
| D18 | 10 | Rust supply chain, unaudited |
| D19 | N/A | |
| D20 | 7 | no verified numbers |
| D21 | 10 | permissive |
| D22 | 3 | from_networkx UNVERIFIED |
| D23 | N/A | |
| D24 | 7 | low evidence |

## Appendix B
| CAP | rustworkx | Claim | EOIP | Decision | Prio |
|---|---|---|---|---|---|
| CAP-62 | partial | 03 | BL-43 | EXPERIMENT | P1 |
| CAP-19 | partial | 03 | BL-43 | BUILD | P2 |
| CAP-04 | native | 01 | BL-43 | REUSE | P3 |

## Appendix C
| ID | Product | Claim | Class | Source | Dates / conf | Contradiction |
|---|---|---|---|---|---|---|
| CLAIM-rustworkx-01 | 0.18.1, 2026-07-30 | Apache-2.0; wheels 2.37 MB x86_64, 2.28 MB win, cp314t 2.34 MB; sdist 0.9 MB | Officially documented | https://pypi.org/pypi/rustworkx/json | acc 2026-10-26; 0.95 | none |
| CLAIM-rustworkx-02 | paper v4 2022-11-02 | designed for NetworkX-level perf gaps; no figures | Officially documented | https://arxiv.org/abs/2110.15221 | acc 2026-10-26; 0.9 | none |
| CLAIM-rustworkx-03 | 0.18.1 | API categories, no community/k-hop | Officially documented | https://www.rustworkx.org/api/index.html | acc 2026-10-26; 0.8 (index page only) | functions may exist elsewhere |

## Appendix D
No local benchmark. Maintainer org not verified. Numpy dependency unchecked.
