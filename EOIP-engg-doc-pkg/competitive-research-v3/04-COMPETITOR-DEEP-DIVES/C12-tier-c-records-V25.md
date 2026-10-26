# C12 Tier C records — V25

Access date 2026-10-26. Cross-references: TinkerPop (C12-tinkerpop.md), Neo4j GDS (C01-neo4j.md), Memgraph MAGE (C01-memgraph.md), TigerGraph (C01-tigergraph.md), GraphScope (C01-graphscope.md), HugeGraph Computer/Vermeer (C01-apache-hugegraph.md).

### T-C12-graphx-graphframes — GraphX and GraphFrames (Spark)
| Field | Value |
|---|---|
| Official URL | https://spark.apache.org/graphx/ ; https://github.com/graphframes/graphframes |
| Owner | GraphX: Apache Spark (ASF); GraphFrames: community contributors (originated UC Berkeley, MIT, Databricks) |
| Latest version + date | GraphX ships inside Spark (Spark 4.2.0 listed 2026-07-14); `graphframes-py` 0.12.3 (PyPI 2026-10-05) |
| Status | GraphX "alpha stage" per project page; GraphFrames active, "maintained by a group of individual contributors" |
| Licence + class | Apache-2.0 (both), permissive |
| Deployment | Spark cluster (JVM), also local mode |
| Air-gap viable | yes (JARs/wheels offline) but requires Spark runtime |
| Tier reason | distributed analytics, out of one-node-first scope |

Relevance: Spark-based batch graph analytics (PageRank, connected components, label propagation, SCC, triangle count in GraphX; plus K-Core, shortest paths, motif finding, Pregel/AggregateMessages, random-walk embeddings in GraphFrames). Relevant only as an optional customer-side offload target for graphs beyond one node; a Spark+JVM dependency conflicts with one-node-first and BL-43's in-process model. Touches CAP-62, CAP-05, CAP-06.
**Decision:** REFERENCE-ONLY. Offer an export-to-Parquet path for customers who already run Spark; no embedded dependency.

| CLAIM | Claim | Class | Source | Dates / confidence |
|---|---|---|---|---|
| CLAIM-graphx-01 | GraphX alpha stage, Apache-2.0, algorithms PageRank, CC, LPA, SVD++, SCC, triangle count | Officially documented | https://spark.apache.org/graphx/ | acc 2026-10-26; 0.85 |
| CLAIM-graphx-02 | GraphFrames Apache-2.0, algorithm list, community-maintained; release notes not read | Officially documented | https://github.com/graphframes/graphframes | acc 2026-10-26; 0.7 |
| CLAIM-graphx-03 | graphframes-py 0.12.3 uploaded 2026-10-05, Python>=3.10 | Officially documented | https://pypi.org/pypi/graphframes-py/json | 2026-10-05; 0.9 |

### T-C12-cugraph — RAPIDS cuGraph
| Field | Value |
|---|---|
| Official URL | https://docs.nvidia.com/cugraph/latest/ (docs.rapids.ai redirects) |
| Owner | NVIDIA / RAPIDS |
| Latest version + date | 26.10.0 (PyPI `cugraph-cu12`, `cugraph-cu13`, 2026-10-08) |
| Status | active |
| Licence + class | Apache-2.0 (PyPI metadata) for cuGraph; its runtime stack (CUDA, cuDF, CuPy, NVIDIA libraries) is under NVIDIA terms — not assessed; legal-review trigger |
| Deployment | NVIDIA GPU, Linux (manylinux x86_64/aarch64); single and multi-GPU (Dask) |
| Air-gap viable | partial (wheels offline, but CUDA stack required) |
| Tier reason | GPU analytics, excluded by CPU-only policy |

Relevance: GPU graph analytics and `nx-cugraph`, a NetworkX backend accelerating supported algorithms on NVIDIA GPUs without code changes. The cugraph-cu12 wheel itself is ~1.7 MB but depends on `cudf-cu12`, `cupy-cuda12x[ctk]`, `dask-cuda`, `pylibcugraph`, `libcugraph` etc. (pinned 26.10.*) [CLAIM-cugraph-02]. ADR-H16 forbids redistributing `nvidia-*`/CUDA packages in any EOIP artefact; ADR-H17 (GPU availability) is open. So cuGraph can only be a customer-provisioned, unqualified optional path, never required.
**Decision:** REJECT as bundled dependency; REFERENCE-ONLY for algorithm coverage; revisit under ADR-H17. Touches CAP-62, CAP-50, CAP-77.

| CLAIM | Claim | Class | Source | Dates / confidence |
|---|---|---|---|---|
| CLAIM-cugraph-01 | cugraph-cu12/cu13 26.10.0, Apache-2.0, requires Python>=3.11, uploaded 2026-10-08 | Officially documented | https://pypi.org/pypi/cugraph-cu12/json | 2026-10-08; 0.95 |
| CLAIM-cugraph-02 | Dependencies on cudf, cupy, cuda-bindings, dask-cuda | Officially documented | same | 0.95 |
| CLAIM-cugraph-03 | nx-cugraph is a NetworkX GPU backend; docs list single/multi-GPU algorithms; GPU/CUDA requirements not on the page | Officially documented | https://docs.nvidia.com/cugraph/latest/ | acc 2026-10-26; 0.6 |
| CLAIM-cugraph-04 | EOIP policy: no CUDA redistribution | Internal decision | docs/decisions/ADR-H16-no-cuda-redistribution.md | accepted 2026-10-18; 1.0 |

### T-C12-graphology — Graphology
| Field | Value |
|---|---|
| Official URL | https://graphology.github.io ; https://github.com/graphology/graphology |
| Owner | graphology community (Sigma.js ecosystem; maintainer not verified) |
| Latest version + date | `graphology` 0.26.0 (npm, 2025-01-26); `graphology-metrics` 2.4.2 (2026-09-02); `graphology-communities-louvain` 2.0.2 (2024-12-17); `graphology-shortest-path` 2.1.0 (2024-03-27); `graphology-library` 0.8.0 (2023-03-03) |
| Status | active but uneven; README warns the standard-library bundle "often lags behind" |
| Licence + class | MIT, permissive |
| Deployment | browser / Node library, embedded |
| Air-gap viable | yes |
| Tier reason | JS graph library already in EOIP's web UI |

Relevance: `apps/web/package.json` already depends on `graphology ^0.25.4` alongside `sigma ^2.4.0`, so it is the client-side graph structure for rendering. Standard-library packages give Louvain, metrics, shortest paths, layouts in-browser. Use limited to presentation-side subgraph layout and small client analytics; authoritative analytics and permission filtering must remain server-side (view must receive only permitted nodes). Observation: the declared range `^0.25.4` is behind the 0.26.0 latest (not a defect finding; upgrade check). Touches CAP-70, CAP-71, CAP-62.
**Decision:** REUSE (already in use) for UI; REFERENCE-ONLY for algorithms.

| CLAIM | Claim | Class | Source | Dates / confidence |
|---|---|---|---|---|
| CLAIM-graphology-01 | MIT; standard library bundle lags | Officially documented | https://github.com/graphology/graphology | acc 2026-10-26; 0.8 |
| CLAIM-graphology-02 | npm versions and dates above, MIT | Officially documented | https://registry.npmjs.org/graphology (and package pages) | acc 2026-10-26; 0.9 |
| CLAIM-graphology-03 | EOIP web depends on graphology ^0.25.4 and sigma ^2.4.0 | Observed in source | apps/web/package.json lines 17, 21 | acc 2026-10-26; 1.0 |

### T-C12-ligra-gap — Ligra and GAP benchmark suite
| Field | Value |
|---|---|
| Official URL | https://github.com/jshun/ligra ; https://github.com/sbeamer/gapbs ; https://arxiv.org/abs/1508.03619 |
| Owner | Ligra: Julian Shun and Guy Blelloch (CMU/MIT); GAP: Scott Beamer, Krste Asanović, David Patterson (UC Berkeley) |
| Latest version + date | no releases listed for either repo; GAP paper v4 2017-05-16; Ligra PPoPP 2013 |
| Status | reference/academic; commit recency UNVERIFIED |
| Licence + class | Ligra MIT; gapbs UC Regents BSD-style header (exact variant UNVERIFIED); permissive |
| Deployment | C++ (OpenMP/Cilk) source build; benchmark harness |
| Air-gap viable | yes |
| Tier reason | algorithmic references |

Relevance: GAP defines six kernels (BFS direction-optimizing, SSSP delta-stepping, PageRank, Connected Components Afforest/Shiloach-Vishkin, Betweenness Brandes, Triangle Counting) and standard input graphs: the agreed yardstick for answering BL-43's "scale untested" using a subset on EOIP engines. Ligra (shared-memory framework; also Ligra+ compressed graphs, Hygra hypergraphs) is the algorithmic reference for frontier-based traversal (edgeMap/vertexMap) and direction-optimising BFS, useful for a native k-hop/BFS implementation. Neither is a product.
**Decision:** REFERENCE-ONLY; adopt the GAP kernel set and methodology into the CAP-78 benchmark harness (EXPERIMENT).

| CLAIM | Claim | Class | Source | Dates / confidence |
|---|---|---|---|---|
| CLAIM-gap-01 | GAP suite spec: kernels and graph sets for shared-memory | Officially documented | https://arxiv.org/abs/1508.03619 | v4 2017-05-16 / acc 2026-10-26; 0.9 |
| CLAIM-gap-02 | gapbs reference implementation, six kernels, C++11+OpenMP | Officially documented | https://github.com/sbeamer/gapbs | acc 2026-10-26; 0.85 |
| CLAIM-ligra-01 | Ligra MIT, PPoPP 2013, Ligra+/Hygra | Officially documented | https://github.com/jshun/ligra | acc 2026-10-26; 0.8 |
