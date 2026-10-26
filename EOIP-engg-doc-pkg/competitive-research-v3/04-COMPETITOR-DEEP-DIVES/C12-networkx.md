# C12 — NetworkX

| Field | Value |
|---|---|
| Registry ID | T-C12-networkx |
| Tier | B (algorithm reference/reuse; BSD-3) |
| Versions examined | networkx 3.7 (PyPI upload 2026-09-21); graphblas-algorithms (backend, no release number verifiable) |
| Verified on | 2026-10-26 (brief says 2026-10-18; actual access date recorded) |
| Worker | V25 |

## 1. Identity, current status, tier, sources
NetworkX is the community reference pure-Python graph library (BSD-3-Clause, `!=3.14.1,>=3.12`, wheel 2.14 MB, sdist 1.87 MB, py3-none-any) [CLAIM-networkx-01]. Active: 3.7 released 2026-09-21. No archival risk. Sources: PyPI JSON, NetworkX 3.7 docs, graph-tool performance page, graphblas-algorithms README.

## 2. Problem, workloads, workflows
Algorithm prototyping, research, teaching, small-to-medium (up to ~10^5 edges interactive) analysis. Workflow: build `Graph`/`DiGraph`/`MultiDiGraph` of dicts-of-dicts, call algorithm, inspect. Not a store, not a server.

## 3. Feature inventory
| Area | Status |
|---|---|
| Centrality (degree, betweenness, closeness, eigenvector, Katz, PageRank, HITS) | present |
| Community: Louvain, **Leiden** (`leiden_communities`), label propagation (3 variants), greedy modularity, Girvan-Newman, k-clique, fluid | present in 3.7 [CLAIM-networkx-02] |
| Shortest paths (Dijkstra, Bellman-Ford, A*, Floyd-Warshall, all-pairs) | present |
| Subgraph matching (VF2 isomorphism / subgraph isomorphism, ISMAGS) | present, exponential worst-case |
| k-hop (`ego_graph`, `single_source_shortest_path_length` with cutoff) | present |
| Anomaly detection | absent (no dedicated module; only structural metrics) |
| Sampling / random walks | partial (generators, `random_walk` helpers; no GraphSAINT-style samplers) UNVERIFIED depth |
| Backend dispatch (`nx-cugraph`, `graphblas-algorithms`, `nx-parallel`) | present: NetworkX 3.0+ dispatches to installed plugins [CLAIM-networkx-03] |
| Persistence/server/auth/tenancy | absent |

## 4. Architecture
```
user code -> nx.Graph (dict[node]->dict[nbr]->attrdict, in RAM)
          -> algorithm fn (pure Python; optional dispatch decorator)
                -> [backend plugin: graphblas / cugraph / parallel] or native
```
Single process, GIL-bound, no control/data plane split.

## 5. Under-the-hood reconstruction
Data model: adjacency as nested dicts keyed by arbitrary hashable nodes; every edge carries a Python dict of attributes. Memory is therefore high per edge (hypothesis from the dict-of-dict design; no measured bytes/edge verified). Algorithms are straightforward Python (heap-based Dijkstra, Brandes betweenness). Dispatch layer converts the NetworkX graph to the backend type (conversion cost is paid per call unless the graph is kept backend-native) [CLAIM-networkx-03]. No transactions, no concurrency control, no security.

## 6. Requirements inferred
Deterministic, readable reference semantics; arbitrary node types; attribute-rich edges; algorithm results as dicts; pluggable backends.

## 7. Performance and resource model
Independent-ish evidence: graph-tool author's benchmark (Intel i9-9980HK, PGP web-of-trust SCC 39,796 nodes / 301,498 edges, NetworkX 2.4 vs igraph 0.8.2, 2020): single-source shortest path 0.25 s vs 0.0092 s igraph; PageRank 1.54 s vs 0.072 s; global clustering 7.94 s vs 0.027 s; betweenness ~10,297 s (vertex) vs 198 s igraph [CLAIM-networkx-04]. Caveats: author is a competitor, old versions (current is 3.7), single graph, numbers not reproduced by us. graphblas-algorithms README claims ~10x on k-truss, 5,000-node random graph, including conversion (vendor claim) [CLAIM-networkx-05]. Failure modes: memory exhaustion beyond ~10^7 edges (hypothesis), exponential VF2.

## 8. Strengths
- Widest pure-Python algorithm breadth; BSD-3; trivial install (no compiled code, air-gap friendly).
- Plugin dispatch gives an acceleration path without API change.
Match/exceed: EOIP can reuse NetworkX as the *correctness oracle* in tests rather than a runtime dependency.

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | VF2 exponential; betweenness O(VE) |
| Operational | dict-of-dict memory; single-threaded; conversion overhead for backends |
| Developer friction | none material; stable API. Python floor 3.12 (3.7) vs EOIP interpreter policy: check |

## 10. Deployment, licensing
BSD-3-Clause, permissive, redistribution-safe, no legal trigger. Pure Python wheel (2.14 MB) installs offline; depends on nothing mandatory (numpy/scipy optional but needed for many functions — UNVERIFIED which). CPU-only by default; `nx-cugraph` backend is GPU and excluded by ADR-H16.

## 11. Competitive delta vs baseline
BL-43: EOIP has ~1,587 lines of own pure-Python algorithms (`graph/algorithms.py` 685, `community.py` 380, `paths.py` 204, `anomaly.py` 318 lines). NetworkX has broader coverage (Leiden, VF2, many centralities) at the same performance class (pure Python). EOIP has anomaly detection and tenant/permission-aware execution, which NetworkX lacks. Baseline lock contains no `networkx` (01-SYSTEM-BASELINE). No EOIP-vs-NetworkX benchmark exists (BL-43 "scale untested").

## 12. Cards
`STR-networkx-01 | NetworkX | broadest reference algorithm set + dispatch plugin | CLAIM-02,03 | oracle for correctness tests; optional acceleration | integrate (test-only) | differential tests EOIP vs NetworkX on random graphs | results equal within tolerance on 1,000 seeded graphs`
`STR-networkx-02 | NetworkX | backend dispatch | CLAIM-03 | pluggable engine without API churn | match | EOIP algorithm port with engine registry (pure/rustworkx/GraphBLAS) | same result via all engines`

INV-networkx-01 — target NetworkX 3.7, analytics on >10^6-edge graphs. Limitation: ~100-1000x slower than C engines [CLAIM-04]. Root cause: interpreter + dict-of-dict (algorithm/storage; proven by benchmark for 2.4, hypothesis for 3.7). Options: (a) wrap igraph/rustworkx, (b) CSR snapshot + numpy, (c) GraphBLAS engine. Selected: (b)+(a-rustworkx) behind engine interface, adapter reads tenant-filtered CSR snapshot. POC: LDBC/SNAP graph 10^6 edges, PageRank+BFS+Louvain, success = ≥20x vs EOIP pure-Python at identical output, record RSS. Failure cases: snapshot must be permission-filtered before leaving the store. Defensibility: tenant-filtered snapshots. Decision: EXPERIMENT. Seed hypotheses 10.5: none targets this tech.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-62 reference semantics / test oracle | REUSE (dev/test only) |
| CAP-62 runtime engine | REJECT as runtime dep (pure Python adds no speed over BL-43) |
| Leiden/VF2 coverage ideas | REFERENCE-PORT (BUILD natively) |

## 14. Tests/POC
Differential suite (betweenness, PageRank, Louvain modularity, shortest paths) vs `graph/*`; acceptance: 100% agreement within 1e-6; document gaps (Leiden, VF2).

## 15. Risks / open questions
Python floor 3.12; numpy/scipy hidden requirements; whether EOIP community.py implements Louvain correctly (not audited here).

## Appendix A — Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | BSD-3, active, 3.7 |
| D2 | 2 | prototyping |
| D3 | 4 | single-process library |
| D4 | 5 | dict-of-dict |
| D5 | 5 | N/A schemaless attrs |
| D6 | N/A | not a query engine |
| D7 | N/A | no reasoning |
| D8 | 5 | none |
| D9 | N/A | no ingest |
| D10 | N/A | no |
| D11 | N/A | no |
| D12 | 3 | broad algos, no ML |
| D13 | N/A | no |
| D14 | N/A | no |
| D15 | N/A | no |
| D16 | N/A | drawing minimal |
| D17 | 3,8 | best docs/API |
| D18 | 5 | none; supply chain pure Python |
| D19 | N/A | no tenancy |
| D20 | 7 | see claims |
| D21 | 10 | permissive |
| D22 | 3 | conversion costs |
| D23 | N/A | no notable patents found |
| D24 | 7 | vendor/competitor benchmark flagged |

## Appendix B — Capability mapping
| CAP | NetworkX | Claim | EOIP baseline | Decision | Prio |
|---|---|---|---|---|---|
| CAP-62 | native | 01,02 | BL-43 Implemented, scale untested | REUSE(test oracle) | P2 |
| CAP-19 | native (cutoff BFS, VF2) | 02 | BL-43 | BUILD natively | P2 |
| CAP-04 | native (in-RAM) | 01 | BL-43 | REUSE | P3 |
| CAP-77 | native BSD | 01 | — | REUSE | P3 |

## Appendix C — Evidence
| ID | Product/version/date | Claim | Class | Source | Dates / confidence | Contradiction |
|---|---|---|---|---|---|---|
| CLAIM-networkx-01 | 3.7, 2026-09-21 | BSD-3-Clause, py>=3.12, wheel 2.14 MB | Officially documented | PyPI JSON https://pypi.org/pypi/networkx/json | pub 2026-09-21 / acc 2026-10-26; 0.95 | none |
| CLAIM-networkx-02 | 3.7 | Louvain, Leiden, LPA etc. listed | Officially documented | https://networkx.org/documentation/stable/reference/algorithms/community.html | acc 2026-10-26; 0.9 | none |
| CLAIM-networkx-03 | 3.x | dispatch to graphblas-algorithms plugin | Officially documented | https://github.com/python-graphblas/graphblas-algorithms | acc 2026-10-26; 0.8 | README says experimental |
| CLAIM-networkx-04 | NX 2.4/igraph 0.8.2, 2020-07 | timings above | Third-party report (competitor author) | https://graph-tool.skewed.de/performance.html | 2020-07-08 / 2026-10-26; 0.5 (old, biased) | newer versions faster, unmeasured |
| CLAIM-networkx-05 | graphblas-algorithms | ~10x k-truss vs NX | Vendor claim | https://github.com/python-graphblas/graphblas-algorithms | acc 2026-10-26; 0.4 | n/a |

## Appendix D — Assumptions
Access date recorded as 2026-10-26 (session date). NetworkX numpy/scipy hard requirements not checked. No local benchmark run.
