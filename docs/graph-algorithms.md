# EOIP Graph Algorithms

30+ algorithms distributed across four modules, operating on the `GraphStore` port.

---

## Module Map

| Module | Algorithms |
|--------|-----------|
| `packages/eoip/graph/metrics.py` | Centrality (8 types), blast radius, what-if |
| `packages/eoip/graph/paths.py` | BFS, Dijkstra, k-shortest, bi-directional search |
| `packages/eoip/graph/similarity.py` | Jaccard, Adamic-Adar, common neighbors, SimRank |
| `packages/eoip/graph/community.py` | Louvain, label propagation, k-core |
| `packages/eoip/graph/algorithms.py` | Cycle detection, weighted paths, co-neighbors, intersection, ray, what-if, process mining, recommendations |

---

## Centrality (`metrics.py`)

### `CentralityMetrics`

8 centrality scores computed per vertex:

| Metric | Description |
|--------|-------------|
| `degree` | Total edge count (in + out) |
| `in_degree` | Incoming edge count |
| `out_degree` | Outgoing edge count |
| `betweenness` | Fraction of shortest paths through this node |
| `closeness` | Inverse of average shortest path length to all nodes |
| `page_rank` | Iterative rank from incoming edge structure |
| `eigenvector` | Connectivity to other high-centrality nodes |
| `katz` | Counts paths of all lengths, damped by attenuation factor |
| `harmonic` | Sum of harmonic distances to all reachable nodes |
| `hits_hub` | HITS hub score (outgoing link authority) |
| `hits_authority` | HITS authority score (incoming link authority) |

API: `POST /api/v1/algorithms/run` with `"algorithm": "centrality"`

### `BlastRadiusResult`

Computes downstream impact from an anchor entity:
- `total_affected`: total entity count
- `by_depth`: entity count by hop distance
- `by_type`: entity count by vertex label
- `risk`: risk level string (LOW/MEDIUM/HIGH/CRITICAL)
- `affected_details`: `AffectedItem` list with canonical_id, label, path_depth, edge_classes

### What-If Analysis

`what_if_remove(canonical_id)` — simulates removing an entity and returns the blast radius change.

Computes a before/after delta showing which entities become unreachable.

---

## Path Algorithms (`paths.py`)

### BFS Path
`bfs_path(source, target, max_depth)` — shortest path by hop count.

### Dijkstra / Weighted Shortest Path
`dijkstra(source, target)` — minimum-cost path using edge `weight` or `confidence` property.

### K-Shortest Paths (Yen's algorithm)
`k_shortest_paths(source, target, k)` — top-k distinct paths by cost.

### Bi-Directional BFS
`bidirectional_bfs(source, target)` — faster shortest path for large graphs, meets in the middle.

### All Simple Paths
`all_simple_paths(source, target, max_depth)` — enumerate all non-cycling paths up to max_depth hops.

---

## Similarity Algorithms (`similarity.py`)

### Jaccard Similarity
`jaccard(node_a, node_b)` — `|N(a) ∩ N(b)| / |N(a) ∪ N(b)|`

### Adamic-Adar
`adamic_adar(node_a, node_b)` — Sum of `1/log(degree(common_neighbor))` over shared neighbors. Penalizes high-degree common neighbors.

### Common Neighbors
`common_neighbors(node_a, node_b)` — raw count of shared neighbors.

### SimRank
`simrank(node_a, node_b, iterations)` — recursive similarity based on structural equivalence.

---

## Community Detection (`community.py`)

### Louvain Modularity
`louvain(resolution)` — hierarchical greedy community detection. Maximizes modularity Q.

Returns: community assignments and `modularity_score`.

### Label Propagation
`label_propagation(iterations)` — each node adopts the most common label among neighbors.

### K-Core Decomposition
`k_core(k)` — largest subgraph where every node has ≥ k neighbors. Identifies tightly-connected clusters.

---

## Extended Algorithms (`algorithms.py`)

### Cycle / Ring Detection
`detect_rings(max_length)` — finds cycles (rings) in directed or undirected graph.

Returns list of `CycleResult(cycle, length)`.

### K-Step Neighborhood
`k_step_neighborhood(center, depth)` — returns `KStepResult` with neighbors grouped by hop distance.

### Co-Neighbor Analysis
`co_neighbors(source, target)` — returns `CoNeighborResult` with shared neighbors, overlap coefficient.

### Subgraph Intersection
`intersection(root_a, root_b, depth)` — finds entities reachable from both roots within `depth` hops.

Returns `IntersectionResult(intersection_nodes, intersection_count)`.

### Directional Ray Traversal
`ray(source, direction, edge_labels, depth)` — follows specific edge types in one direction.

Returns `RayResult(visited, depth_reached)`.

### Weighted Path (Dijkstra)
Returns `WeightedPath(path, total_weight, hop_count)`.

### Recommendations
`recommend(anchor, strategy)` — collaborative-filter-style recommendations based on co-neighbors and structural similarity.

### Temporal Degree Sequence
`temporal_degree_sequence(canonical_id, window_days)` — tracks degree changes over time.

---

## Process Mining Algorithms

`packages/eoip/graph/process_mining.py` (Phase C)

| Algorithm | Description |
|-----------|-------------|
| `alpha_miner` | Discover process model from event log sequences |
| `conformance_check` | Measure deviation between observed and designed process |
| `fitness_score` | Fraction of event traces that conform to the process model |
| `process_discovery` | Extract process graph from WorkItem state transitions |
| `bottleneck_detection` | Find steps with abnormally high wait or execution time |

---

## Phase C Extended Algorithms (12)

From `packages/eoip/agents/graph_analytics.py` ALGORITHM_REGISTRY:

| Algorithm | Module |
|-----------|--------|
| `triangle_count` | Community |
| `cross_domain_paths` | Paths |
| `temporal_anomaly` | Metrics |
| `orphan_detection` | Metrics |
| `twin_detection` | Algorithms |
| `risk_propagation` | Metrics |
| `dependency_rank` | Paths |
| `change_velocity` | Temporal |
| `knowledge_gap` | Algorithms |
| `trust_cluster` | Community |
| `semantic_drift` | Ontology |
| `compliance_coverage` | Algorithms |

---

## GraphAnalyticsAgent Swarm Mode

Running `{"goal": "swarm"}` in the `GraphAnalyticsAgent` executes these algorithms in parallel:

1. `ring_detection` — circular dependencies
2. `k_core` — dense cluster identification
3. `community_detection` — Louvain + label propagation
4. `anomaly_detection` — degree outliers, temporal gaps, orphans
5. `blast_radius` — impact hotspot map
6. Domain-specific algorithms based on present graph domains

Results are aggregated into a single swarm report with per-algorithm sections and an overall health summary.

API: `POST /api/v1/agents/analytics` with `{"goal": "swarm"}`

---

## API Usage

```json
POST /api/v1/algorithms/run
{
  "algorithm": "betweenness|pagerank|blast_radius|community_detection|louvain|jaccard|detect_rings|...",
  "parameters": {
    "start_vertex": "urn:service:auth",
    "max_depth": 3,
    "k": 5
  }
}
```

`GET /api/v1/algorithms` — list all algorithms with parameter schemas.

Tests: `tests/unit/test_graph_metrics.py`, `tests/unit/test_graph_algorithms.py`, `tests/unit/test_community_detection.py`
