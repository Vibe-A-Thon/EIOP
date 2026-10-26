# C12 — igraph

| Field | Value |
|---|---|
| Registry ID | T-C12-igraph |
| Tier | B (fast C library; GPL flag) |
| Versions examined | python-igraph 1.0.0 (PyPI 2025-10-23); C core docs show igraph 1.0.1 |
| Verified on | 2026-10-26 |
| Worker | V25 |

## 1. Identity, status, sources
igraph: C library with Python, R, Mathematica and C bindings. PyPI `igraph` 1.0.0, uploaded 2025-10-23, requires Python >=3.9, classifier "GNU General Public License (GPL)" [CLAIM-igraph-01]; python-igraph repo sidebar GPL-2.0 [CLAIM-igraph-02]. The C reference manual shows version 1.0.1 [CLAIM-igraph-03]. The C core licence text (GPL-2.0-or-later) was NOT verified on this pass: UNVERIFIED, confidence 0.4. Active.

## 2. Problem and workloads
Fast single-machine analysis on graphs up to ~10^7 edges in RAM: community detection, centrality, motifs, layout. Workflow: `Graph.TupleList(edges)`, `g.community_leiden(...)`, `g.betweenness()`.

## 3. Feature inventory
| Area | Status |
|---|---|
| Centrality (betweenness, closeness, PageRank, eigenvector, hub/authority, strength) | present |
| Community: `igraph_community_leiden` (modularity or CPM), Louvain (`community_multilevel`), Infomap, walktrap, label propagation, spinglass, leading eigenvector, fastgreedy, edge-betweenness, optimal, fluid, Voronoi | present [CLAIM-igraph-03] |
| Subgraph matching (VF2, LAD, motifs counting, isomorphism BLISS) | present |
| k-hop (`neighborhood(order=k)`, BFS) | present |
| Shortest paths (Dijkstra, Bellman-Ford, Johnson, A*, k-shortest variants UNVERIFIED) | present |
| Anomaly detection | absent |
| Sampling / random walks | partial (random walks, subgraph sampling, graph generators) |
| GPU / distributed | absent |
| Persistence, auth, tenancy | absent |

## 4. Architecture
```
Python/R/C API -> vendored C core (igraph_t: indexed edge list, CSR-like incidence)
                -> optional BLAS/LAPACK/ARPACK/GLPK bundled; single process, mostly single-threaded
```

## 5. Reconstruction
Graph stored as vertex/edge integer-indexed arrays with sorted indices (`from`, `to`, `oi`, `ii`, `os`, `is`) — this is how the igraph C core is documented in its developer notes; not re-verified here (hypothesis, 0.5). Attributes live in the binding layer (Python dict/list per vertex/edge) rather than in the core. Algorithms are C implementations with ARPACK for eigen-problems. No transactions or security. Python wheels vendor the C core ("same version of the C core that is vendored") [CLAIM-igraph-02].

## 6. Requirements inferred
Integer vertex ids; in-RAM graph; deterministic algorithm outputs; bindings stable across languages.

## 7. Performance and resource model
Same graph-tool-author benchmark (i9-9980HK, 39,796 nodes / 301,498 edges, igraph 0.8.2 vs NetworkX 2.4): SSSP 0.0092 s, PageRank 0.072 s, global clustering 0.027 s, k-core 0.0098 s, MST 0.026 s, betweenness 198 s vertex + 439 s edge; igraph 1.1x-4x slower than single-thread graph-tool, 25x-300x faster than NetworkX [CLAIM-igraph-04] (competitor-authored, 2020, old version, confidence 0.5). Memory: C arrays; wheel 5.68 MB x86_64 manylinux_2_28, 3.22 MB win_amd64 (abi3 cp39) [CLAIM-igraph-01]. Failure modes: attribute-heavy graphs hit Python overhead; no out-of-core.

## 8. Strengths
Speed class of C with a 5.7 MB wheel; richest community-detection suite incl. Leiden and Infomap; abi3 wheel covers many Python versions.

## 9. Limitations
| Class | Item |
|---|---|
| Licensing | GPL (python-igraph GPL-2.0; C core to verify) — strong copyleft, redistribution trigger |
| Algorithmic | betweenness still hours at 3x10^5 edges; not parallel (hypothesis) |
| Friction | integer ids; attribute handling out of core |

## 10. Deployment, licensing, redistribution
GPL-2.0 = legal-review trigger. Bundling the wheel in an EOIP distribution, importing it in-process, and shipping offline bundles are exactly the cases to review; EOIP policy treats GPL/AGPL as a hard constraint (memory: ontology strategy). Record only: no conclusion. A process-isolated, customer-installed optional plugin is the typical mitigation to put before counsel, not a conclusion. Air-gap: wheel offline-installable. CPU only.

## 11. Delta vs baseline
BL-43 pure Python (no numpy in lock; `pyproject.toml` lists numpy>=1.26,<3.0 but 01-SYSTEM-BASELINE reports it not installed). igraph offers Leiden/Infomap/VF2/LAD that EOIP lacks, at C speed, but its licence blocks default inclusion. No igraph in lock.

## 12. Cards
`STR-igraph-01 | igraph | C-speed broad community and motif suite in 5.7 MB wheel | CLAIM-01,03,04 | benchmark yardstick for EOIP | integrate as external benchmark only | run igraph out-of-tree to compute reference timings | EOIP engine within 10x of igraph on 10^6-edge PageRank`
INV-igraph-01 — target igraph 1.0.0, any redistribution. Limitation: GPL. Root cause: licensing (proven, per classifier). Options: (a) exclude, (b) native Leiden/Louvain implementation in numpy/Rust, (c) optional customer-installed adapter in separate process. Selected: (b) with (c) as customer opt-in after legal review. POC: native Leiden within 5x of igraph runtime and modularity within 1% on 3 SNAP graphs. Failure: process boundary must carry tenant-filtered data only. Defensibility: permissive engine + tenant filtering. Decision: EXPERIMENT. No seed hypothesis targets igraph.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-62 runtime dependency | REJECT (GPL; legal review) |
| CAP-62 benchmark/oracle (off-product) | REUSE |
| Leiden/Infomap/VF2 algorithms | BUILD natively (clean-room from papers) |

## 14. Tests
Off-repo benchmark script; acceptance: results published with hardware; license scan in CI proving no igraph in distribution artefacts.

## 15. Risks
C core licence unverified; "GPL" ambiguity (2 vs 3, or-later); cleanroom boundary when reading igraph source.

## Appendix A
| Dim | Sec | Summary |
|---|---|---|
| D1 | 1,10 | GPL, active |
| D2 | 2 | in-RAM analytics |
| D3 | 4 | C core + bindings |
| D4 | 5 | indexed edge arrays (hypothesis) |
| D5 | N/A | attrs in bindings |
| D6 | N/A | no query engine |
| D7 | N/A | |
| D8 | 5 | none |
| D9 | N/A | |
| D10 | N/A | |
| D11 | N/A | |
| D12 | 3 | algos, no ML |
| D13 | N/A | |
| D14 | N/A | |
| D15 | N/A | |
| D16 | N/A | plotting minimal |
| D17 | 3 | multi-language |
| D18 | 10 | supply chain: vendored C |
| D19 | N/A | |
| D20 | 7 | see claims |
| D21 | 10 | GPL |
| D22 | 3 | GraphML/GML IO (UNVERIFIED) |
| D23 | N/A | none found |
| D24 | 7 | biased benchmark |

## Appendix B
| CAP | igraph | Claim | EOIP | Decision | Prio |
|---|---|---|---|---|---|
| CAP-62 | native | 03 | BL-43 | REJECT dep / BUILD | P1 |
| CAP-19 | native | 03 | BL-43 | BUILD | P2 |
| CAP-77 | GPL | 01,02 | — | REJECT | P1 |

## Appendix C
| ID | Product | Claim | Class | Source | Dates / conf | Contradiction |
|---|---|---|---|---|---|---|
| CLAIM-igraph-01 | igraph 1.0.0 2025-10-23 | GPL classifier; abi3 wheels 5.68 MB (linux x86_64), 3.22 MB (win) | Officially documented | https://pypi.org/pypi/igraph/json | acc 2026-10-26; 0.9 | none |
| CLAIM-igraph-02 | python-igraph | GPL-2.0 repo licence; vendors C core | Officially documented | https://github.com/igraph/python-igraph | acc 2026-10-26; 0.8 | C core licence not shown |
| CLAIM-igraph-03 | igraph C 1.0.1 | community functions list | Officially documented | https://igraph.org/c/doc/igraph-Community.html | acc 2026-10-26; 0.9 | none |
| CLAIM-igraph-04 | igraph 0.8.2 2020 | timings | Third-party (competitor) | https://graph-tool.skewed.de/performance.html | 2020-07-08/2026-10-26; 0.5 | old |

## Appendix D
C core licence not verified; no local benchmark; bundled-library licences (GLPK is GPL) not checked.
