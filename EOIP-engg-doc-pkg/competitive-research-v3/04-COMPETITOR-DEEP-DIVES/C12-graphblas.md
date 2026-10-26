# C12 — GraphBLAS (SuiteSparse:GraphBLAS, python-graphblas)

| Field | Value |
|---|---|
| Registry ID | T-C12-graphblas |
| Tier | B (linear-algebra graph engine) |
| Versions examined | SuiteSparse:GraphBLAS 10.5.2 (README, 2026-10-20); `suitesparse-graphblas` wheel 10.5.1.1 (PyPI 2026-10-17); `python-graphblas` 2025.2.0 (2025-02-17); `graphblas-algorithms` (no release number shown) |
| Verified on | 2026-10-26 |
| Worker | V25 |

## 1. Identity, status, sources
GraphBLAS = C API standard for graph algorithms in the language of sparse linear algebra over semirings. SuiteSparse:GraphBLAS (Timothy A. Davis) is the reference implementation; Apache-2.0 for all sources needed to build `libgraphblas` [CLAIM-graphblas-01]. Python layers: `suitesparse-graphblas` (CFFI binding, Apache-2.0, wheel 21-24 MB) [CLAIM-graphblas-02], `python-graphblas` (Apache-2.0, py3-none-any 0.35 MB, requires numpy>=1.23, donfig, pyyaml, suitesparse-graphblas, numba optional/py<3.14) [CLAIM-graphblas-03], `graphblas-algorithms` (Apache-2.0, NetworkX backend) [CLAIM-graphblas-04]. LAGraph (algorithm library) is separate and not verified here. Python wrapper lags the C library; python-graphblas last release is 8 months old (check cadence).

## 2. Problem and workloads
Whole-graph analytics (BFS, PageRank, triangle counting, connected components, k-truss, centrality) expressed as sparse matrix ops; large static graphs on multicore CPUs.

## 3. Feature inventory
| Area | Status |
|---|---|
| Sparse matrix/vector formats (CSR/CSC, hypersparse, bitmap, full) | present |
| Semirings, masks, accumulators, user-defined types/ops | present |
| JIT kernel compiler, runtime-compiled kernels cached in `~/.SuiteSparse`; `GRAPHBLAS_COMPACT` mode | present [CLAIM-graphblas-01] |
| Centrality (degree, eigenvector, Katz, PageRank, HITS) via graphblas-algorithms | present [CLAIM-graphblas-04]; betweenness in LAGraph UNVERIFIED |
| Community detection (Louvain/Leiden) | not listed in graphblas-algorithms (modularity matrix only); LAGraph community: UNVERIFIED |
| Shortest paths (BFS levels, SSSP Bellman-Ford, Floyd-Warshall dense) | present |
| Subgraph matching | absent (isomorphism checks only, not enumeration) |
| k-hop | native (BFS with level masks) |
| Anomaly detection, sampling | absent |
| GPU | draft only, "not ready to use" [CLAIM-graphblas-01] |
| Persistence/server/tenancy | absent |

## 4. Architecture
```
python-graphblas (Matrix/Vector/Scalar, lazy exprs, numba UDFs)
  -> suitesparse-graphblas (CFFI) -> libgraphblas (C, OpenMP, JIT via system C compiler)
  graphblas-algorithms -> NetworkX plugin entry point "networkx.plugin"
```

## 5. Reconstruction
Graph = adjacency Matrix; traversal step = `vxm` over a boolean/`any_pair` semiring with complement mask for visited set; PageRank = iterated `mxv` on plus_times. SuiteSparse chooses sparse/hypersparse/bitmap/full per matrix. Kernels: precompiled "FactoryKernels" plus JIT; JIT needs a C compiler at runtime and a writable cache dir, which is an air-gap/hardening consideration (compiler required on target) [CLAIM-graphblas-01]. Parallelism via OpenMP. Node identity requires external mapping string id <-> integer index (hypothesis: standard practice). No concurrency control beyond library-thread safety; no security.

## 6. Requirements inferred
Integer-indexed adjacency snapshot; semiring algebra; mask discipline; C compiler for JIT (or PreJIT); OpenMP runtime.

## 7. Performance and resource model
Vendor-style claim: graphblas-algorithms README: ~10x faster than native NetworkX for k-truss on a 5,000-node random graph including conversion; gains "grow with size"; "faster than scipy.sparse" [CLAIM-graphblas-04] (vendor, small graph, 0.4). Independent evidence: the GAP Benchmark Suite (Beamer, Asanovic, Patterson, arXiv:1508.03619) defines BFS, SSSP, PR, CC, BC, TC kernels and is the standard yardstick [CLAIM-graphblas-05]; LAGraph/GraphBLAS GAP results exist in the literature but were NOT retrieved: UNVERIFIED. Footprint: wheel 23.57 MB x86_64 cp312; JIT compile latency on first use (hypothesis). Failure modes: first-call JIT cost, compiler absent, memory for dense semiring ops.

## 8. Strengths
Highest ceiling on single-node CPU for whole-graph kernels; Apache-2.0 (patent grant); k-hop/BFS natural; NetworkX plugin gives a drop-in acceleration route; hypersparse handles huge ID spaces.

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | no subgraph enumeration, no anomaly, community gap; per-vertex path queries are awkward in matrix form |
| Operational | JIT needs compiler; 24 MB binary; OpenMP tuning; GPU not ready |
| Friction | integer ids, algebraic thinking, wrapper lag (python-graphblas 2025.2.0 pins `suitesparse-graphblas<10` while wheel is 10.5.1.1 — compatibility conflict, verify) [CLAIM-graphblas-03] |

## 10. Deployment, licensing
Apache-2.0 library; bundled LZ4/xxHash/ZSTD BSD, cpu_features Apache-2.0; logo CC BY 4.0 (do not ship) [CLAIM-graphblas-01]. No GPL. Air-gap: wheels offline, but JIT cache/compiler decision needed (PreJIT can bake kernels). CPU only; GPU code excluded by ADR-H16. No legal trigger noted. Note: `python-graphblas` requires numpy, adding numpy to the runtime lock (baseline: numpy not in the lock).

## 11. Delta vs baseline
BL-43 is pure-Python adjacency; GraphBLAS provides parallel sparse-matrix kernels (not measured by us). BL-43 has anomaly.py and community.py which GraphBLAS lacks. BL-57 numerical stack: numpy tier planned; GraphBLAS fits N1/N2 CPU tier subject to ADR-H15 review.

## 12. Cards
`STR-graphblas-01 | SuiteSparse:GraphBLAS | semiring sparse kernels, Apache-2.0, CPU OpenMP | CLAIM-01,02 | speed for PageRank, BFS, k-hop, triangle on large tenant snapshots | integrate | optional engine; tenant-filtered CSR -> Matrix; pre-JIT bundle | GAP-kron/urand-scale or smaller dataset runs 20x faster than BL-43 at identical output`
`STR-graphblas-02 | graphblas-algorithms | NetworkX dispatch | CLAIM-04 | compatibility oracle | integrate | differential tests | outputs match NetworkX within tolerance`
INV-graphblas-01 — target python-graphblas 2025.2.0 / suitesparse 10.5.1.1, JIT. Limitation: runtime C compiler and cache dir needed [CLAIM-01]. Root cause: deployment (proven by README). Options: (a) use FactoryKernels only, (b) PreJIT bake at build, (c) own Rust kernels. Selected (b). POC: air-gapped container without compiler runs PageRank/BFS; success = identical output, cold-start <5 s. Failure case: cache dir shared across tenants leaks nothing but must be read-only. Decision: EXPERIMENT. No seed hypothesis targets this tech.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-62 whole-graph kernels (PageRank, CC, triangles, BFS) | EXPERIMENT -> INTEGRATE as optional engine |
| CAP-19 k-hop/BFS | EXPERIMENT |
| Community/anomaly | BUILD (EOIP) |
| GPU path | REJECT (ADR-H16) |

## 14. Tests
Differential vs NetworkX and BL-43; GAP-kernel subset on a laptop-size graph; no-compiler container test; wheel size/hash recorded; numpy added to lock review.

## 15. Risks
Version skew between wrappers and C library; numpy lock impact; JIT in hardened images; wrapper release cadence slow (2025-02-17).

## Appendix A
| Dim | Sec | Summary |
|---|---|---|
| D1 | 1,10 | Apache-2.0, active C lib |
| D2 | 2 | whole-graph analytics |
| D3 | 4 | 3-layer stack |
| D4 | 5 | sparse formats |
| D5 | N/A | |
| D6 | N/A | not a query engine |
| D7 | N/A | |
| D8 | 5 | OpenMP only |
| D9 | N/A | |
| D10 | N/A | |
| D11 | N/A | |
| D12 | 3,7 | algos |
| D13 | N/A | |
| D14 | N/A | |
| D15 | N/A | |
| D16 | N/A | |
| D17 | 3,8 | Python API |
| D18 | 10 | JIT compiler surface |
| D19 | N/A | |
| D20 | 7 | few verified numbers |
| D21 | 10 | permissive |
| D22 | N/A | |
| D23 | N/A | not examined |
| D24 | 7 | evidence thin |

## Appendix B
| CAP | GraphBLAS | Claim | EOIP | Decision | Prio |
|---|---|---|---|---|---|
| CAP-62 | native | 01,04 | BL-43 | EXPERIMENT | P1 |
| CAP-19 | native (BFS) | 01 | BL-43 | EXPERIMENT | P2 |
| CAP-04 | native | 02 | BL-43 | REUSE | P3 |
| CAP-50 | partial (JIT) | 01 | — | EXPERIMENT | P2 |

## Appendix C
| ID | Product | Claim | Class | Source | Dates / conf | Contradiction |
|---|---|---|---|---|---|---|
| CLAIM-graphblas-01 | SuiteSparse:GraphBLAS 10.5.2 (README date 2026-10-20) | Apache-2.0; JIT; GPU draft | Officially documented | https://github.com/DrTimothyAldenDavis/GraphBLAS | acc 2026-10-26; 0.8 (page summarised) | none |
| CLAIM-graphblas-02 | suitesparse-graphblas 10.5.1.1, 2026-10-17 | Apache-2.0; wheels 21-24 MB | Officially documented | https://pypi.org/pypi/suitesparse-graphblas/json | acc 2026-10-26; 0.95 | none |
| CLAIM-graphblas-03 | python-graphblas 2025.2.0, 2025-02-17 | wheel 353 KB; deps; Apache | Officially documented | https://pypi.org/pypi/python-graphblas/json | acc 2026-10-26; 0.9 | pins suitesparse <10 vs wheel 10.5 |
| CLAIM-graphblas-04 | graphblas-algorithms | algorithm list; NX plugin; ~10x k-truss | Vendor claim | https://github.com/python-graphblas/graphblas-algorithms | acc 2026-10-26; 0.5 | |
| CLAIM-graphblas-05 | GAP v4 2017-05-16 | benchmark suite spec | Officially documented | https://arxiv.org/abs/1508.03619 | acc 2026-10-26; 0.9 | |

## Appendix D
LAGraph and published GraphBLAS performance papers not retrieved. No local run.
