# KGR — Knowledge Graph Renderer: Phase-by-Phase Implementation Plan

**Version:** 3.0  
**Date:** 2026-10-03  
**Baseline:** EOIP current state (166 tests passing, full App.jsx with 6 lenses including KGR, GraphCanvas with Cytoscape.js, Phase 1 backend+frontend complete)  
**Target:** The most capable open, local-first graph intelligence platform — surpassing Graphify, Neo4j Bloom, Linkurious, Gephi, Graphistry, yFiles, Sourcetrail, CodeSee, Sourcegraph, code2flow, KeyLines, Ogma, G6/Graphin, and Cytoscape desktop.

---

## Architecture Overview

### Rendering Strategy
- **Primary renderer**: Cytoscape.js (existing, extend) for graphs up to 5K nodes
- **Large-graph renderer**: Sigma.js v3 (WebGL) for 5K-50K+ nodes, progressive fallback
- **Layout engine**: Web Worker-based layout computation for graphs > 500 nodes (ForceAtlas2, dagre, Cola, Euler)
- **Data layer**: graphology library for in-memory graph algorithms (centrality, community detection, shortest path, similarity)
- **Visualization extras**: SVG-based radar charts, timeline scrubber, heatmap overlay — all inline, no external charting library

### Why This Stack Beats Every Competitor

| Decision | Rationale | Competitor It Beats |
|---|---|---|
| Cytoscape.js + Sigma.js dual renderer | Canvas for interaction quality (<5K), WebGL for raw throughput (50K+) | Graphify (5K limit), Gephi (desktop), Graphistry (GPU required) |
| graphology for algorithms | Pure JS, runs in browser, no server dependency for basic analytics | Neo4j Bloom (requires GDS), Linkurious (server-side only) |
| Web Worker layouts | Non-blocking UI during heavy computation | Sourcetrail (hangs on large indexing), yFiles (main-thread layouts) |
| Zero external runtime | No cloud, no GPU, no license server | Sourcegraph ($49/mo), yFiles (€9.2K/yr), Graphistry ($1.47/hr GPU) |
| 8 graph types from one data model | Purpose-built views vs. one-size-fits-all | ALL competitors (max 1-2 view types) |
| Evidence-first data model | Trust propagation, provenance chains native | Only Graphify has partial evidence; KGR goes deeper |

### Component Architecture
```
apps/web/src/
├── App.jsx                            (existing — KGR lens already integrated)
├── GraphCanvas.jsx                    (existing — enhance with advanced features)
├── kgr/
│   ├── KGRExplorer.jsx                (DONE — main container, 6 graph types, inspector)
│   ├── components/
│   │   ├── GraphTypeSelector.jsx      (8 graph type tabs — extract from KGRExplorer)
│   │   ├── FilterBar.jsx             (10-dimensional filtering with presets)
│   │   ├── NodeInspector.jsx          (8-tab inspector — extract from KGRExplorer)
│   │   ├── EdgeInspector.jsx          (relationship intelligence panel)
│   │   ├── BlastRadiusView.jsx        (concentric ring blast radius visualization)
│   │   ├── CentralityRadar.jsx        (SVG radar chart for centrality metrics)
│   │   ├── Minimap.jsx                (thumbnail overview navigator)
│   │   ├── TimelineScrubber.jsx       (temporal graph navigation with playback)
│   │   ├── GraphToolbar.jsx           (extended toolbar: layouts, sizing, settings)
│   │   ├── ExportMenu.jsx             (PNG/SVG/PDF/JSON-LD/GraphML/CSV export)
│   │   ├── AnnotationPanel.jsx        (node/edge annotations with persistence)
│   │   ├── GraphBookmarks.jsx         (saved view management)
│   │   ├── ContextMenu.jsx            (right-click menu for nodes/edges/canvas)
│   │   ├── ExplorationHistory.jsx     (undo/redo breadcrumb trail)
│   │   ├── EventFeed.jsx              (real-time graph change events)
│   │   ├── GraphDiff.jsx              (snapshot comparison view)
│   │   ├── GraphHealth.jsx            (quality dashboard widgets)
│   │   └── SimilarityPanel.jsx        (structural similarity analysis)
│   ├── renderers/
│   │   ├── CytoscapeRenderer.jsx      (Cytoscape.js wrapper, extends existing)
│   │   ├── SigmaRenderer.jsx          (Sigma.js/WebGL for large graphs)
│   │   └── LayoutWorker.js            (Web Worker for layout computation)
│   ├── graphs/
│   │   ├── KnowledgeGraph.jsx         (primary entity-relationship view)
│   │   ├── RelationshipGraph.jsx      (edge-centric analysis view)
│   │   ├── MetadataGraph.jsx          (schema topology view — DONE inline)
│   │   ├── OntologyGraph.jsx          (class hierarchy view — DONE inline)
│   │   ├── TemporalGraph.jsx          (time-windowed view with playback)
│   │   ├── ProvenanceGraph.jsx        (lineage/evidence chain view — DONE inline)
│   │   ├── ImpactGraph.jsx            (blast radius + dependency view)
│   │   └── SimilarityGraph.jsx        (community clusters + similarity edges)
│   └── analysis/
│       ├── centrality.js              (client-side centrality: degree, betweenness, closeness, PageRank)
│       ├── community.js               (Leiden/Louvain community detection via graphology)
│       ├── similarity.js              (Jaccard, Adamic-Adar, common neighbors)
│       ├── blast-radius.js            (client-side BFS blast radius for small graphs)
│       ├── graph-metrics.js           (density, diameter, components, k-core)
│       └── link-prediction.js         (common neighbors, Jaccard, Adamic-Adar prediction)

packages/eoip/
├── graph/
│   ├── metrics.py                     (DONE — blast radius, reverse impact, centrality, statistics, schema)
│   ├── community.py                   (Leiden/Louvain/Label Propagation community detection)
│   ├── similarity.py                  (Jaccard, Adamic-Adar, common neighbors)
│   ├── paths.py                       (all shortest paths, Yen's k-shortest, widest path)
│   ├── anomaly.py                     (outlier detection, degree spike, dense subgraph)
│   └── whatif.py                      (entity removal simulation, broken path count)
├── query/
│   └── executor.py                    (existing — extend with metrics intents)

apps/api/
├── app.py                             (DONE — KGR endpoints: blast-radius, reverse-impact, metrics, schema, statistics)
└── main.py                            (existing — operation classifier updated)
```

### Backend API — Full Endpoint Inventory

```python
# DONE (Phase 1)
POST /api/v1/graph/blast-radius     # BFS downstream impact
POST /api/v1/graph/reverse-impact   # BFS upstream dependencies
POST /api/v1/graph/metrics          # Centrality metrics for node set
GET  /api/v1/graph/schema           # Full ontology meta-graph
GET  /api/v1/graph/statistics       # Aggregate graph-level stats

# Phase 3 — Advanced Centrality
POST /api/v1/graph/centrality/full  # Betweenness, closeness, PageRank, eigenvector

# Phase 4 — Community & Paths
POST /api/v1/graph/cluster          # Leiden/Louvain/Label Propagation community detection
POST /api/v1/graph/shortest-paths   # All shortest paths between two entities

# Phase 5 — Similarity & Prediction
POST /api/v1/graph/similarity       # Jaccard/Adamic-Adar/Common neighbors
POST /api/v1/graph/link-prediction  # Predict missing edges

# Phase 6 — Structure Analysis
POST /api/v1/graph/k-core           # k-core decomposition
POST /api/v1/graph/components       # Connected component analysis
POST /api/v1/graph/degree-distribution # Degree histogram data

# Phase 7 — Real-Time
WS   /ws/graph/events               # WebSocket for real-time graph changes
GET  /api/v1/graph/events           # Polling fallback

# Phase 8 — Advanced Analytics
POST /api/v1/graph/diff             # Compare two graph snapshots
POST /api/v1/graph/what-if          # Simulate entity removal
POST /api/v1/graph/anomalies        # Detect outlier nodes
```

### Request/Response Contracts for All Endpoints

```python
# --- DONE ---

class BlastRadiusRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    max_depth: int = Field(default=4, ge=1, le=8)
# Response: {target_id, total_affected, by_depth: {1: N, 2: M}, by_type: {"File": N}, risk: "HIGH"|"MEDIUM"|"LOW", affected_ids: [...]}

class MetricsRequest(BaseModel):
    canonical_ids: list[str] = Field(min_length=1, max_length=50)
# Response: {canonical_id: {canonical_id, degree, in_degree, out_degree, betweenness, closeness, page_rank}}

# --- PLANNED ---

class FullCentralityRequest(BaseModel):
    canonical_ids: list[str] = Field(min_length=1, max_length=50)
    algorithms: list[str] = Field(default=["degree", "betweenness", "closeness", "pagerank"])
# Response: {canonical_id: {degree, in_degree, out_degree, betweenness, closeness, page_rank, eigenvector, katz, hits_hub, hits_authority}}

class ClusterRequest(BaseModel):
    canonical_ids: list[str] | None = None  # None = entire graph
    resolution: float = Field(default=1.0, ge=0.1, le=10.0)
    algorithm: str = Field(default="leiden", pattern="^(leiden|louvain|label_propagation)$")
# Response: {communities: [{id: int, members: [canonical_id], size: int, label_distribution: {}}], modularity: float, algorithm: str}

class ShortestPathsRequest(BaseModel):
    source_id: str = Field(min_length=1, max_length=512)
    target_id: str = Field(min_length=1, max_length=512)
    max_paths: int = Field(default=5, ge=1, le=20)
    max_length: int = Field(default=10, ge=2, le=20)
# Response: {paths: [[canonical_id, ...]], count: int}

class SimilarityRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    algorithm: str = Field(default="jaccard", pattern="^(jaccard|adamic_adar|common_neighbors)$")
    limit: int = Field(default=10, ge=1, le=50)
# Response: [{canonical_id, score: float, common_neighbors: [canonical_id]}]

class LinkPredictionRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    algorithm: str = Field(default="common_neighbors", pattern="^(common_neighbors|jaccard|adamic_adar)$")
    limit: int = Field(default=10, ge=1, le=50)
# Response: [{source_id, target_id, score: float, algorithm: str}]

class KCoreRequest(BaseModel):
    min_k: int = Field(default=2, ge=1, le=100)
# Response: {cores: [{k: int, members: [canonical_id], size: int}], max_k: int}

class WhatIfRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    action: str = Field(default="remove", pattern="^(remove|isolate)$")
# Response: {broken_paths: int, orphaned_entities: int, affected_components: int, centrality_changes: {canonical_id: {before, after}}}

class DiffRequest(BaseModel):
    snapshot_a: str  # timestamp ISO or snapshot ID
    snapshot_b: str
# Response: {added_nodes: [...], removed_nodes: [...], modified_nodes: [...], added_edges: [...], removed_edges: [...], structural_changes: {broken_paths: int, new_components: int}}

class AnomalyRequest(BaseModel):
    algorithms: list[str] = Field(default=["degree_zscore", "dense_subgraph"])
    threshold: float = Field(default=2.0, ge=1.0, le=5.0)
# Response: [{canonical_id, anomaly_type: str, score: float, explanation: str}]
```

---

## Implementation Status

| Phase | Status | Tests Added | Key Deliverables |
|---|---|---|---|
| Phase 1 | **COMPLETE** | 19 | Metrics engine, 5 API endpoints, KGR Explorer, 6 graph types, 5-tab inspector, CSS |
| Phase 2 | **COMPLETE** | 14 | 10 graph types, 8-tab inspector, edge inspector, standalone graph components |
| Phase 3 | **COMPLETE** | 28 | Full centrality (8 algos), client-side algorithms, radar chart, path finding |
| Phase 4 | **COMPLETE** | 12 | 11-dim filtering, community detection (3 algos), keyboard nav, context menu, bookmarks, exploration history |
| Phase 5 | **COMPLETE** | 10 | Timeline scrubber, 7-format export, annotations, similarity (3 algos), link prediction |
| Phase 6 | **COMPLETE** | 10 | Sigma.js WebGL, Web Worker layouts, progressive rendering, k-core, components, degree distribution |
| Phase 7 | **COMPLETE** | 8 | WebSocket event emitter, polling fallback, event feed UI, useGraphEvents hook |
| Phase 8 | **COMPLETE** | 20 | Graph diff, what-if (2 modes), anomaly detection (3 algos), health dashboard |
| Phase 9 | **TODO** | — | Component wiring & integration (connect disconnected components into KGRExplorer) |
| Phase 10 | **TODO** | — | Advanced competitor features (node grouping, geo-mode, code+graph, visual query builder, dead code, community labeling, PR dashboard, 4 new export formats) |

---

## Phase 1: Foundation — COMPLETE

**Duration:** 2 weeks (done)  
**Tests:** 166 total (19 new KGR tests)

### What Was Built
- `packages/eoip/graph/metrics.py` — GraphMetricsEngine with blast_radius, reverse_impact, centrality, graph_statistics, graph_schema
- 5 API endpoints in `apps/api/app.py` — blast-radius, reverse-impact, metrics, schema, statistics
- `apps/web/src/kgr/KGRExplorer.jsx` — main container with 6 graph types (Knowledge, Relationship, Metadata, Ontology, Temporal, Provenance), 5-tab inspector, blast radius overlay
- KGR lens integrated into App.jsx
- ~150 lines of KGR CSS in style.css
- 9 unit tests for metrics engine, 10 API endpoint tests

### Key Implementation Details
- Edge traversal uses `edge["in_v"]` (outgoing target) and `edge["out_v"]` (incoming source) — matches MemoryGraphStore and HugeGraphStore
- Pydantic request models MUST be at module level (not inside create_app) for FastAPI body parameter binding
- GraphMetricsEngine instantiated inside create_app with the store instance
- BlastRadiusResult and CentralityMetrics use `__slots__` for memory efficiency

---

## Phase 2: Component Extraction & New Graph Types
**Duration:** 2 weeks  
**Goal:** Extract inline components from KGRExplorer.jsx into standalone files, add Impact and Similarity graph types, extend inspector to 8 tabs.

### 2.1 Extract Components from KGRExplorer.jsx (3 days)
**Files to create (extract from KGRExplorer.jsx):**

```
apps/web/src/kgr/components/GraphTypeSelector.jsx
```
- Extract the GraphTypeSelector component
- Add 2 new types: Impact, Similarity (total: 8 graph types)
- Each tab has icon, label, tooltip description
- Active tab state managed by parent KGRExplorer

```
apps/web/src/kgr/components/FilterBar.jsx
```
- Extract the FilterBar component
- Extend from 4 filters (domain, label, edgeType, trust) to 10 dimensions
- Add: evidence filter, temporal filter, property filter, centrality filter, community filter, search-within-view
- Active filter chips with click-to-remove
- "Save preset" and "Reset all" buttons
- Presets stored in localStorage

```
apps/web/src/kgr/components/NodeInspector.jsx
```
- Extract the NodeInspector with current 5 tabs
- Add 3 new tabs: Similarity, History, Raw (total: 8 tabs)
- Tab 5 (Similarity): top 10 structurally similar nodes, common neighbor count, community membership
- Tab 6 (History): ingestion runs that touched entity, modification timeline sparkline
- Tab 7 (Annotations): text annotations with 500 char limit, persist in localStorage
- Tab 8 (Raw): full JSON with copy-to-clipboard button

### 2.2 Impact/Dependency Graph View (2 days)
**Files:** `apps/web/src/kgr/graphs/ImpactGraph.jsx`

- Blast radius concentric ring view centered on selected entity
- Ring depth 1-8 hops with entity type breakdown per ring
- Risk classification color coding: HIGH (red), MEDIUM (amber), LOW (green)
- Animated propagation mode: wave effect showing impact spreading
- Reverse impact toggle (flip to upstream view)
- Click any ring entity to recenter blast radius on it
- Uses data from `/api/v1/graph/blast-radius` and `/api/v1/graph/reverse-impact`
- **No competitor has this** — KGR's unique differentiator

### 2.3 Similarity/Cluster Graph View (2 days)
**Files:** `apps/web/src/kgr/graphs/SimilarityGraph.jsx`

- Community detection overlay with convex hull clusters
- Cluster coloring mode (domain colors replaced by cluster colors)
- Click community hull to filter to that cluster
- Similarity edges between structurally similar nodes (dashed lines)
- k-core decomposition highlighting
- Degree distribution histogram overlay (toggleable)
- Initially uses client-side graphology algorithms; server fallback for large graphs
- **Goes beyond Graphify's basic Leiden** by adding visual cluster intelligence

### 2.4 Edge Inspector Component (1 day)
**Files:** `apps/web/src/kgr/components/EdgeInspector.jsx`

- Source and target entity summaries with mini-preview cards
- Edge type with semantic meaning from ontology manifest
- All edge properties with type-aware formatting
- Evidence backing: source_ref, evidence_key, method
- Creation status badge: DETERMINISTIC (green), INFERRED (amber), MANUAL (blue)
- Parallel edges indicator (other relationships between same endpoints)
- Path context: which known paths use this edge
- Activates when user clicks an edge in any graph type

### 2.5 Update KGRExplorer.jsx (1 day)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`

- Import extracted components
- Add routing for 2 new graph types (Impact, Similarity)
- Wire edge selection to EdgeInspector
- Add CSS for new components

### Tests (Phase 2)
```
tests/unit/test_kgr_phase2.py  — 15 tests
tests/unit/test_kgr_components.jsx — 10 tests (if using vitest/jest)
```
- 4 tests for 8-tab inspector (each new tab renders correctly)
- 3 tests for 10-dimensional filter state management
- 2 tests for Impact graph data transformation
- 2 tests for Similarity graph data transformation
- 2 tests for edge inspector rendering
- 2 tests for graph type switching with 8 types
- All 166 existing tests continue to pass

---

## Phase 3: Full Centrality Suite & Client-Side Algorithms
**Duration:** 2 weeks  
**Goal:** Implement the complete centrality analysis stack with 8 algorithms, client-side graph algorithms, and visual intelligence.

### 3.1 Backend: Full Centrality Engine (3 days)
**Files:** modify `packages/eoip/graph/metrics.py`

Extend GraphMetricsEngine with new methods:

```python
def full_centrality(self, canonical_ids: list[str], algorithms: list[str]) -> dict[str, FullCentralityMetrics]:
    """Compute requested centrality algorithms for given nodes."""
    # Build adjacency lists once, compute all requested algorithms

def _betweenness_centrality(self, adj, nodes) -> dict[str, float]:
    """Brandes' algorithm for betweenness centrality. O(V*E)."""
    # For each node s: BFS from s, accumulate pair dependencies

def _closeness_centrality(self, adj, nodes) -> dict[str, float]:
    """Inverse of average shortest path length. O(V*(V+E))."""
    # BFS from each node, sum distances, invert

def _pagerank(self, adj, nodes, damping=0.85, iterations=20) -> dict[str, float]:
    """Iterative PageRank with damping factor."""
    # Initialize uniform, iterate: PR(v) = (1-d)/N + d * sum(PR(u)/out(u))

def _eigenvector_centrality(self, adj, nodes, iterations=50) -> dict[str, float]:
    """Power iteration for eigenvector centrality."""
    # Initialize uniform, iterate: x_new = A * x_old, normalize

def _katz_centrality(self, adj, nodes, alpha=0.1, beta=1.0) -> dict[str, float]:
    """Katz centrality with attenuation factor."""
    # x = beta * (I - alpha*A)^-1 * 1 — approximated via power iteration

def _hits(self, adj, nodes, iterations=20) -> dict[str, tuple[float, float]]:
    """HITS hub and authority scores."""
    # Initialize uniform, iterate: auth = A^T * hub, hub = A * auth, normalize
```

New API endpoint:
```
POST /api/v1/graph/centrality/full
```

Update CentralityMetrics to include: eigenvector, katz, hits_hub, hits_authority, harmonic

### 3.2 Client-Side Graph Algorithms (3 days)
**Files:** `apps/web/src/kgr/analysis/centrality.js`, `blast-radius.js`, `graph-metrics.js`

Using graphology library for immediate client-side feedback:

```javascript
// centrality.js
export function degreeCentrality(graph) { /* graphology-metrics/centrality/degree */ }
export function betweennessCentrality(graph) { /* graphology-metrics/centrality/betweenness */ }
export function closenessCentrality(graph) { /* BFS-based */ }
export function pageRank(graph, {damping: 0.85, iterations: 20}) { /* power iteration */ }

// blast-radius.js
export function clientBlastRadius(graph, nodeId, maxDepth = 4) {
    // BFS from nodeId along outgoing edges, collect by depth/type
    // Use for small graphs (<500 nodes) for instant feedback
}

// graph-metrics.js
export function graphDensity(graph) { /* edges / (nodes * (nodes-1)) */ }
export function connectedComponents(graph) { /* BFS/DFS component detection */ }
export function degreeDistribution(graph) { /* histogram of degree values */ }
export function clusteringCoefficient(graph) { /* local clustering per node */ }
```

Decision logic:
- Graph < 500 nodes → compute client-side for instant feedback
- Graph >= 500 nodes → call server API, show loading state
- All computations wrapped in requestIdleCallback or Web Worker

### 3.3 Centrality Radar Chart (2 days)
**Files:** `apps/web/src/kgr/components/CentralityRadar.jsx`

- Pure SVG radar/spider chart (no external charting library)
- 5 axes: Degree, Betweenness, Closeness, PageRank, Blast Radius
- Normalized 0-1 scale with percentile ranking against all visible nodes
- Comparison mode: overlay two entities' radar charts (select via shift-click)
- Tooltip on each axis explaining the metric in plain language
- Renders in inspector Impact tab
- Responsive: scales to inspector panel width
- Color: primary entity in palette blue, comparison entity in palette amber

### 3.4 Inspector Impact Tab Enhancement (2 days)
**Files:** modify `apps/web/src/kgr/components/NodeInspector.jsx`

Impact tab now shows:
1. **Blast radius summary**: "N entities affected across M depth levels" + risk badge
2. **Depth breakdown**: horizontal bar chart (depth 1, 2, 3, 4...)
3. **Type breakdown**: horizontal bar chart by entity type
4. **Centrality radar chart** (from 3.3)
5. **Change propagation score**: "This entity affects X% of the graph"
6. **Reverse impact section**: "Y upstream entities depend on this"
7. **"Explore Blast Radius" button** → switches to Impact graph type centered on this entity
8. **"Run What-If" button** → opens what-if simulation (Phase 8, greyed out until then)

### 3.5 Path Finding (2 days)
**Files:** `packages/eoip/graph/paths.py`, modify `apps/api/app.py`

```python
class GraphPathFinder:
    def all_shortest_paths(self, source_id: str, target_id: str, max_paths: int = 5) -> list[list[str]]:
        """BFS-based all shortest paths. Returns up to max_paths paths."""
    
    def k_shortest_paths(self, source_id: str, target_id: str, k: int = 5) -> list[list[str]]:
        """Yen's k-shortest paths algorithm."""
```

API endpoint: `POST /api/v1/graph/shortest-paths`

Frontend: path highlighting on graph canvas — selected path edges turn bold blue, intermediate nodes get highlight rings.

### Tests (Phase 3)
```
tests/unit/test_kgr_centrality.py — 20 tests
tests/unit/test_kgr_paths.py — 8 tests
```
- 4 tests per centrality algorithm (betweenness, closeness, PageRank, eigenvector)
- 2 tests for Katz centrality
- 2 tests for HITS hub/authority
- 4 tests for all shortest paths
- 2 tests for k-shortest paths
- 2 API endpoint tests for centrality/full
- 2 API endpoint tests for shortest-paths
- All 166+ existing tests continue to pass

---

## Phase 4: Community Detection, Filtering & Keyboard Navigation
**Duration:** 2 weeks  
**Goal:** Leiden/Louvain community detection, 10-dimensional filtering, keyboard navigation, context menus, exploration history, bookmarks.

### 4.1 Backend: Community Detection Engine (3 days)
**Files:** `packages/eoip/graph/community.py`, modify `apps/api/app.py`

```python
class CommunityDetectionEngine:
    def __init__(self, store: GraphStore):
        self._store = store
    
    def leiden(self, node_ids: list[str] | None = None, resolution: float = 1.0) -> CommunityResult:
        """Leiden algorithm — guarantees connected communities.
        Steps: 1) local moving (greedy modularity), 2) refinement, 3) aggregate, repeat."""
    
    def louvain(self, node_ids: list[str] | None = None, resolution: float = 1.0) -> CommunityResult:
        """Louvain modularity optimization — fast but may produce disconnected communities."""
    
    def label_propagation(self, node_ids: list[str] | None = None) -> CommunityResult:
        """Near-linear time label propagation. Good for very large graphs."""

class CommunityResult:
    communities: list[Community]  # [{id, members: [canonical_id], size, label_distribution}]
    modularity: float
    algorithm: str
```

Implementation notes:
- Leiden: implement the 3-phase approach (local moving → refinement → aggregation → repeat)
- For graphs > 10K nodes, use Label Propagation (near-linear) as default
- Cache community results with TTL (communities don't change without new ingestion)
- API endpoint: `POST /api/v1/graph/cluster`

### 4.2 Client-Side Community Detection (2 days)
**Files:** `apps/web/src/kgr/analysis/community.js`

```javascript
import louvain from 'graphology-communities-louvain';

export function detectCommunities(graph, algorithm = 'louvain', resolution = 1.0) {
    // Use graphology-communities-louvain for client-side
    // Returns: {nodeId: communityId}
}

export function computeConvexHulls(graph, communities) {
    // Compute convex hull points for each community
    // Returns: {communityId: [{x, y}, ...]}
}
```

- Graph < 1K nodes → compute client-side with graphology-communities-louvain
- Graph >= 1K nodes → call server API

### 4.3 10-Dimensional Filter Bar (3 days)
**Files:** `apps/web/src/kgr/components/FilterBar.jsx` (from Phase 2 extraction)

Filter dimensions with UI controls:

| # | Dimension | Control | Default |
|---|---|---|---|
| 1 | Domain | Multi-select dropdown | ALL |
| 2 | Entity type | Checkbox list with live counts | ALL |
| 3 | Relationship type | Checkbox list with live counts | ALL |
| 4 | Trust level | Radio: Deterministic / Inferred / Manual / All | All |
| 5 | Evidence | Radio: Evidenced / Unevidenced / All | All |
| 6 | Temporal | Dual-handle range slider (date) | Full range |
| 7 | Property | Key-value builder: property [=, >, <, contains] value | None |
| 8 | Centrality | Min/max degree threshold slider | 0-max |
| 9 | Community | Multi-select of detected cluster IDs | ALL |
| 10 | Search-within | Text input filtering visible nodes (no API call) | Empty |

State management:
```javascript
const [filters, setFilters] = useState({
    domain: [],        // empty = all
    label: [],         // empty = all
    edgeType: [],      // empty = all
    trust: 'ALL',      // 'DETERMINISTIC' | 'INFERRED' | 'MANUAL' | 'ALL'
    evidence: 'ALL',   // 'EVIDENCED' | 'UNEVIDENCED' | 'ALL'
    temporal: { from: null, to: null },
    property: [],      // [{key, operator, value}]
    centrality: { min: 0, max: Infinity },
    community: [],     // empty = all
    searchText: '',
});
```

Features:
- Active filter chips below filter bar with click-to-remove
- Saved filter presets in localStorage with named configurations
- "Reset all filters" button
- Filter state persists across graph type switches
- Collapsible sections (only show expanded dimensions with active filters)

### 4.4 Keyboard Navigation (2 days)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`

| Key | Action |
|---|---|
| Tab | Cycle through nodes in entity strip |
| Enter | Select focused node, open inspector |
| Escape | Deselect, close inspector |
| Arrow Left/Right | Traverse to sibling nodes (same depth/type) |
| Arrow Up/Down | Traverse along edges (up=incoming, down=outgoing) |
| E | Expand selected node's neighborhood (1-hop) |
| Shift+E | Expand 2-hop |
| I | Toggle inspector panel |
| F | Toggle filter bar |
| 1-8 | Switch graph types |
| / | Focus search-within-view |
| Ctrl+Z | Undo last exploration action |
| Ctrl+Shift+Z | Redo |
| M | Toggle minimap |
| Space | Fit all visible nodes |

- Focus ring styling on all interactive elements
- Screen reader announcements for graph topology changes
- ARIA roles on graph elements

### 4.5 Context Menu (2 days)
**Files:** `apps/web/src/kgr/components/ContextMenu.jsx`

Right-click on node:
- Expand neighborhood (1-hop / 2-hop / 3-hop submenu)
- Explore blast radius
- Find paths from/to this entity
- Trace lineage
- Pin/unpin position
- Hide node
- Copy canonical ID
- Add annotation

Right-click on edge:
- Inspect relationship
- Show evidence
- Find parallel edges
- Hide this edge type
- Copy edge details

Right-click on canvas:
- Fit all
- Reset filters
- Export view
- Toggle minimap
- Select layout (submenu with 12 options)

Implementation: absolute-positioned div with click-outside-to-close, keyboard-navigable (arrow keys + Enter).

### 4.6 Exploration History (1 day)
**Files:** `apps/web/src/kgr/components/ExplorationHistory.jsx`

- Stack of exploration actions: expand, filter, select, navigate
- Breadcrumb trail below graph type selector
- Undo (Ctrl+Z) pops last action, restores previous graph state
- Redo (Ctrl+Shift+Z) re-applies
- Max history depth: 50 actions
- Action types: `{type: 'expand', nodeId, depth}`, `{type: 'filter', filters}`, `{type: 'navigate', nodeId}`, `{type: 'layout', algorithm}`
- **Fixes Graphify's lack of undo** — a key user complaint

### 4.7 Bookmarks (1 day)
**Files:** `apps/web/src/kgr/components/GraphBookmarks.jsx`

- Save current view state: `{name, query, filters, graphType, layout, viewport: {zoom, pan}, selectedNodes}`
- Stored in localStorage under key `kgr-bookmarks`
- Quick-access bar below filter bar (icon + name chips)
- Click bookmark to restore view
- Export/import bookmarks as JSON
- Max 20 bookmarks

### Tests (Phase 4)
```
tests/unit/test_kgr_community.py — 12 tests
tests/unit/test_kgr_filters.py — 10 tests (if backend filter endpoints added)
```
- 4 tests for Leiden algorithm correctness
- 4 tests for Louvain algorithm correctness
- 2 tests for Label Propagation
- 2 tests for community API endpoint
- 10 filter state management tests (component-level)
- 5 keyboard navigation tests
- 4 context menu rendering tests
- 3 exploration history undo/redo tests
- 3 bookmark persistence tests
- All 166+ existing tests continue to pass

---

## Phase 5: Timeline, Export Suite, Annotations & Visual Polish
**Duration:** 2 weeks  
**Goal:** Timeline scrubber with animated playback, 7-format export suite, annotation system, semantic zoom, fisheye distortion, edge bundling, color-blind palette.

### 5.1 Timeline Scrubber (3 days)
**Files:** `apps/web/src/kgr/components/TimelineScrubber.jsx`

- Horizontal bar at bottom of temporal graph view (height: 60px)
- Dual-handle range slider for selecting time window
- Histogram overlay showing entity creation density over time (bucketed by day/week/month auto)
- Playback controls: play, pause, step forward, step backward
- Speed control: 1x, 2x, 5x, 10x
- Entities outside selected window fade to 10% opacity (not removed, avoids layout jump)
- Current time indicator with date label
- Available as overlay in all graph types (collapsible)
- Responds to temporal filter dimension in FilterBar

### 5.2 Export Suite (3 days)
**Files:** `apps/web/src/kgr/components/ExportMenu.jsx`

| Format | Method | Details |
|---|---|---|
| PNG | `cy.png({output: 'blob', scale: 2, full: true})` | 2x resolution, full graph or viewport |
| SVG | `cy.svg({full: true})` | Vector, scalable |
| PDF | PNG + jsPDF | Graph image + node table + relationship summary + metrics |
| JSON-LD | Custom serializer | Graph data with EOIP ontology @context |
| GraphML | Custom XML builder | Standard graph interchange format |
| CSV | Custom | Separate nodes.csv and edges.csv, zipped |
| Clipboard | `navigator.clipboard.writeText()` | Selected node/edge as formatted Markdown |

Export dialog:
- Format selector (radio buttons with format icons)
- Scope: visible graph / entire graph / selected nodes
- Resolution: 1x / 2x / 3x (PNG only)
- Include: annotations / metrics / legend (checkboxes)
- "Export" button triggers download

**Surpasses**: Graphify (HTML/JSON only), Neo4j Bloom (PNG/CSV), Gephi (no web export)

### 5.3 Annotation System (2 days)
**Files:** `apps/web/src/kgr/components/AnnotationPanel.jsx`

- Text annotations stored in localStorage:
  - Key format: `kgr-annotation-node-${canonical_id}` or `kgr-annotation-edge-${edge_id}`
  - Value: `{text: string, created: ISO, updated: ISO}`
- Annotation indicator: small blue dot overlay on annotated nodes/edges
- Inspector Annotations tab: textarea for viewing/editing
- Character limit: 500 per annotation
- Annotations included in PDF/JSON exports when "Include annotations" checked
- Batch clear option: "Remove all annotations"

### 5.4 Semantic Zoom Enhancement (2 days)
**Files:** modify `apps/web/src/GraphCanvas.jsx`

Three zoom levels with smooth transitions:

| Zoom Level | Range | Visible Elements |
|---|---|---|
| Cluster | < 0.3 | Cluster hulls, high-degree nodes only (degree > mean+1σ), no labels |
| Entity | 0.3 - 0.8 | All nodes, abbreviated labels (first 15 chars), no edge labels |
| Detail | > 0.8 | All nodes with full labels, edge labels, evidence indicators, property badges |

- Transitions: CSS opacity/transform animations (200ms)
- Node hover always shows full label tooltip regardless of zoom level
- Configurable thresholds in toolbar settings

### 5.5 Fisheye Distortion (1 day)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`

- Toggle from toolbar ("magnifier" icon)
- 2x magnification at cursor center, gradual falloff to edges
- Implementation: on mousemove, compute distortion for each visible node position
- Use `cy.nodes().positions()` with distortion function
- Debounce: compute every 50ms during drag
- Disable during layout animation

### 5.6 Edge Bundling (1 day)
**Files:** modify `apps/web/src/GraphCanvas.jsx`

- Force-directed edge bundling (FDEB) for visual declutter
- Activate when any node has > 10 edges (configurable threshold)
- Toggle from toolbar settings
- Implementation: Cytoscape.js `haystack` edge style with control points
- Bundled edges fan out at endpoints for readability
- Performance: skip bundling for > 2K edges (too expensive)

### 5.7 Color-Blind Safe Palette (1 day)
**Files:** modify `apps/web/src/GraphCanvas.jsx`, `apps/web/src/style.css`

Two alternative palettes:
1. **Deuteranopia/Protanopia**: blue-orange-yellow scheme (no red-green)
2. **High Contrast**: black-white-blue-yellow for maximum contrast

Additional accessibility:
- Shape variations alongside color: circles (default), diamonds (selected), triangles (high-degree), squares (annotated)
- Pattern fills for cluster hulls
- Toggle in toolbar settings gear

### 5.8 Similarity Analysis (2 days)
**Files:** `packages/eoip/graph/similarity.py`, `apps/web/src/kgr/analysis/similarity.js`, modify `apps/api/app.py`

Backend:
```python
class SimilarityEngine:
    def jaccard(self, canonical_id: str, limit: int = 10) -> list[SimilarityResult]:
        """Jaccard neighbor similarity: |N(u) ∩ N(v)| / |N(u) ∪ N(v)|"""
    
    def adamic_adar(self, canonical_id: str, limit: int = 10) -> list[SimilarityResult]:
        """Adamic-Adar: sum(1/log(|N(w)|)) for w in N(u) ∩ N(v). Biased toward low-degree bridges."""
    
    def common_neighbors(self, canonical_id: str, limit: int = 10) -> list[SimilarityResult]:
        """Simple common neighbor count."""
```

API endpoints: `POST /api/v1/graph/similarity`, `POST /api/v1/graph/link-prediction`

Frontend: SimilarityPanel in inspector Similarity tab showing ranked similar nodes.

### Tests (Phase 5)
```
tests/unit/test_kgr_similarity.py — 10 tests
tests/unit/test_kgr_export.py — 8 tests (if backend export endpoints added)
```
- 3 tests for Jaccard similarity
- 3 tests for Adamic-Adar similarity
- 2 tests for common neighbors
- 2 similarity API endpoint tests
- 6 timeline scrubber interaction tests (component-level)
- 8 export format validation tests (component-level)
- 4 annotation CRUD tests (component-level)
- 3 semantic zoom level tests (component-level)
- 2 accessibility tests (color-blind palette, keyboard)
- All 166+ existing tests continue to pass

---

## Phase 6: Large-Graph Rendering & Performance
**Duration:** 1.5 weeks  
**Goal:** Scale visualization to 50K+ nodes using WebGL rendering and progressive loading. This phase directly addresses the #1 complaint against Graphify (5K node limit) and Sourcetrail (crashes on large codebases).

### 6.1 Sigma.js Integration (3 days)
**Files:** `apps/web/src/kgr/renderers/SigmaRenderer.jsx`

```javascript
import Sigma from 'sigma';
import Graph from 'graphology';
import forceAtlas2 from 'graphology-layout-forceatlas2';

export default function SigmaRenderer({ elements, layout, onSelect, onHover, style }) {
    // Create graphology graph from EOIP elements
    // Initialize Sigma with WebGL renderer
    // Apply ForceAtlas2 layout in Web Worker
    // Wire click/hover/select events to match CytoscapeRenderer API
}
```

Auto-switch logic:
```javascript
const Renderer = elements.nodes.length > 5000 ? SigmaRenderer : CytoscapeRenderer;
```

Feature parity with CytoscapeRenderer:
- Click to select node/edge
- Hover to highlight neighbors
- Zoom/pan with mouse wheel/drag
- Domain coloring
- Node sizing by degree/centrality
- Edge styling by evidence status

WebGL node programs:
- Circle (default), diamond (selected), triangle (high-degree)
- Label rendering with collision avoidance
- Edge rendering with arrow markers

### 6.2 Web Worker Layout Engine (2 days)
**Files:** `apps/web/src/kgr/renderers/LayoutWorker.js`

```javascript
// LayoutWorker.js — runs in Web Worker context
import forceAtlas2 from 'graphology-layout-forceatlas2/worker';

self.onmessage = function(event) {
    const { type, nodes, edges, algorithm, options } = event.data;
    
    switch (algorithm) {
        case 'forceAtlas2':
            // Run ForceAtlas2 with progress reporting
            // Post: {type: 'progress', iteration, total}
            // Post: {type: 'positions', positions: {nodeId: {x, y}}}
            break;
        case 'dagre':
            // Dagre hierarchical layout
            break;
        case 'cola':
            // Cola constraint-based layout
            break;
    }
};
```

Message protocol:
- `{type: 'start', nodes, edges, algorithm, options}` → start computation
- `{type: 'progress', iteration, total}` ← progress update
- `{type: 'positions', positions}` ← final result
- `{type: 'cancel'}` → abort computation

### 6.3 Progressive Rendering (2 days)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`

For results > 1K nodes:
1. Sort nodes by degree (descending)
2. Render first 200 nodes immediately (highest degree = most connected = most important)
3. Add remaining nodes in batches of 100 with requestAnimationFrame scheduling
4. Incremental layout: pin existing positions, only layout new nodes
5. Progress indicator: "Rendering 200/5,234 nodes..."
6. "Show all" / "Show top N" toggle in toolbar

Performance targets:
| Node Count | Initial Render | Full Render | Memory |
|---|---|---|---|
| 1,000 | < 500ms | < 2s | < 50MB |
| 5,000 | < 1s | < 5s | < 150MB |
| 10,000 | < 2s | < 10s | < 300MB |
| 50,000 | < 5s | < 30s | < 512MB |

### 6.4 Virtual Scrolling Entity Strip (1 day)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`

- Virtualized list rendering only visible rows (window of ~20 items)
- Smooth scroll with 50K+ items
- Fixed header with count + filter controls
- Implementation: calculate visible range from scroll position, render only those items with absolute positioning

### 6.5 Backend: Structure Analysis Endpoints (2 days)
**Files:** modify `packages/eoip/graph/metrics.py`, `apps/api/app.py`

```python
def k_core_decomposition(self) -> dict:
    """Find k-core subgraphs. Returns {k: [canonical_ids]}."""
    # Iteratively remove nodes with degree < k

def connected_components(self) -> list[list[str]]:
    """BFS/DFS component detection. Returns list of components."""

def degree_distribution(self) -> dict[int, int]:
    """Histogram of degree values. Returns {degree: count}."""
```

API endpoints: `POST /api/v1/graph/k-core`, `POST /api/v1/graph/components`, `POST /api/v1/graph/degree-distribution`

### Tests (Phase 6)
```
tests/unit/test_kgr_structure.py — 10 tests
```
- 3 tests for k-core decomposition
- 3 tests for connected components
- 2 tests for degree distribution
- 2 API endpoint tests
- Performance benchmarks: 1K, 5K, 10K rendering times (manual verification)
- Memory usage tests (manual verification)
- Renderer switching tests (Cytoscape ↔ Sigma)
- All 166+ existing tests continue to pass

---

## Phase 7: Real-Time Updates & WebSocket Integration
**Duration:** 1 week  
**Goal:** Live graph updates as ingestion events occur. Fixes Graphify's staleness problem and matches Graphistry's streaming (without GPU dependency).

### 7.1 WebSocket Event Service (2 days)
**Files:** modify `apps/api/main.py`, `packages/eoip/events/emitter.py` (new)

```python
# packages/eoip/events/emitter.py
class GraphEventEmitter:
    def __init__(self):
        self._subscribers: list[asyncio.Queue] = []
    
    def subscribe(self) -> asyncio.Queue:
        q = asyncio.Queue(maxsize=1000)
        self._subscribers.append(q)
        return q
    
    def unsubscribe(self, q: asyncio.Queue):
        self._subscribers.remove(q)
    
    async def emit(self, event: GraphEvent):
        for q in self._subscribers:
            try:
                q.put_nowait(event)
            except asyncio.QueueFull:
                pass  # drop oldest events for slow consumers
```

WebSocket endpoint:
```python
@app.websocket("/ws/graph/events")
async def graph_events(websocket: WebSocket):
    await websocket.accept()
    queue = emitter.subscribe()
    try:
        while True:
            event = await queue.get()
            await websocket.send_json(event.to_dict())
    except WebSocketDisconnect:
        emitter.unsubscribe(queue)
```

Event types:
```python
class GraphEvent:
    type: str  # vertex_upserted, edge_upserted, vertex_deleted, edge_deleted, ingestion_completed, validation_completed
    data: dict  # full entity/edge data
    timestamp: str  # ISO 8601
```

Polling fallback:
```python
@app.get("/api/v1/graph/events")
async def poll_events(since: str = Query(...)):
    # Return events since timestamp from in-memory ring buffer (last 1000 events)
```

### 7.2 Client-Side WebSocket Manager (2 days)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`

```javascript
function useGraphEvents(apiBase) {
    const [events, setEvents] = useState([]);
    const wsRef = useRef(null);
    
    useEffect(() => {
        const ws = new WebSocket(`${apiBase.replace('http', 'ws')}/ws/graph/events`);
        ws.onmessage = (e) => {
            const event = JSON.parse(e.data);
            setEvents(prev => [...prev.slice(-999), event]);
            // Apply to graph state
        };
        ws.onclose = () => reconnectWithBackoff();
        wsRef.current = ws;
        return () => ws.close();
    }, [apiBase]);
    
    return events;
}
```

Incremental graph updates:
- New entities: fade-in animation (opacity 0→1 over 300ms)
- Removed entities: fade-out animation (opacity 1→0 over 300ms)
- Modified entities: flash highlight (yellow pulse)
- Incremental layout: only reposition affected neighborhood (1-hop from changed entity)
- Off-screen change notification badge: "3 new entities added"

Reconnection:
- Exponential backoff: 1s, 2s, 4s, 8s, 16s, max 30s
- On reconnect: poll `/api/v1/graph/events?since=lastEventTimestamp` to catch missed events
- Connection status indicator in KGR toolbar

### 7.3 Event Feed Panel (1 day)
**Files:** `apps/web/src/kgr/components/EventFeed.jsx`

- Collapsible panel (bottom of KGR Explorer, height: 150px)
- Real-time scrolling list of graph change events
- Each event: icon + type + entity summary + timestamp
- Click event to navigate to affected entity
- Filter by event type (checkboxes)
- Pause/resume toggle
- Clear history button
- Max display: 100 events (virtualized)

### Tests (Phase 7)
```
tests/unit/test_kgr_events.py — 8 tests
```
- 2 tests for event emitter subscribe/unsubscribe
- 2 tests for event serialization
- 2 tests for polling fallback endpoint
- 2 tests for event type filtering
- WebSocket integration tests (manual verification with test client)
- All 166+ existing tests continue to pass

---

## Phase 8: Graph Comparison, What-If & Advanced Analytics
**Duration:** 1.5 weeks  
**Goal:** Diff visualization, what-if simulation, anomaly detection, and graph health dashboard. These features have **no equivalent in any competitor** — they make KGR definitively the most analytical graph tool available.

### 8.1 Backend: What-If Engine (2 days)
**Files:** `packages/eoip/graph/whatif.py`, modify `apps/api/app.py`

```python
class WhatIfEngine:
    def __init__(self, store: GraphStore):
        self._store = store
        self._metrics = GraphMetricsEngine(store)
    
    def simulate_removal(self, canonical_id: str) -> WhatIfResult:
        """Simulate removing an entity without actually modifying the graph.
        Computes: broken paths, orphaned entities, centrality changes."""
        
        # 1. Find all edges connected to this entity
        # 2. For each neighbor: check if removing these edges disconnects it
        # 3. Count broken shortest paths through this entity
        # 4. Recompute centrality for affected neighbors
        # 5. Return impact summary
    
    def simulate_isolation(self, canonical_id: str) -> WhatIfResult:
        """Simulate disconnecting an entity (keeping it but removing all edges)."""
```

API endpoint: `POST /api/v1/graph/what-if`

### 8.2 Backend: Anomaly Detection (2 days)
**Files:** `packages/eoip/graph/anomaly.py`, modify `apps/api/app.py`

```python
class AnomalyDetector:
    def degree_zscore_outliers(self, threshold: float = 2.0) -> list[AnomalyResult]:
        """Nodes with degree > mean + threshold*std."""
    
    def dense_subgraph_detection(self) -> list[AnomalyResult]:
        """Find unexpectedly dense subgraphs (potential hub-and-spoke anomalies)."""
    
    def missing_expected_edges(self) -> list[AnomalyResult]:
        """Entities that should be connected based on type patterns but aren't."""
```

API endpoint: `POST /api/v1/graph/anomalies`

### 8.3 Graph Diff View (3 days)
**Files:** `apps/web/src/kgr/components/GraphDiff.jsx`, modify `apps/api/app.py`

Backend:
```python
def graph_diff(self, snapshot_a: str, snapshot_b: str) -> DiffResult:
    """Compare graph state at two points.
    Returns added/removed/modified nodes and edges with structural analysis."""
```

API endpoint: `POST /api/v1/graph/diff`

Frontend — two modes:

**Overlay mode** (default):
- Single graph canvas
- Added nodes: green border + "+" badge
- Removed nodes: red border + "−" badge, dashed outline
- Modified nodes: yellow border + "~" badge
- Unchanged: gray (dimmed)
- Same color scheme for edges

**Side-by-side mode**:
- Two graph canvases with synchronized zoom/pan
- Left: snapshot A, Right: snapshot B
- Changes highlighted in both views
- Change list panel below: sortable table of all changes

### 8.4 What-If Simulation UI (2 days)
**Files:** modify `apps/web/src/kgr/components/NodeInspector.jsx`, `apps/web/src/kgr/KGRExplorer.jsx`

- "Run What-If Simulation" button in inspector Impact tab
- Opens modal with simulation results:
  - "Removing [Entity Name] would:"
  - "Break N shortest paths"
  - "Orphan M entities (no remaining connections)"
  - "Change centrality for K neighbors"
  - Centrality change table: entity | before | after | delta
- "Preview on graph" button: shows affected entities highlighted with dotted borders
- "Cancel" returns to normal view
- No actual data modification — purely read-only simulation

### 8.5 Graph Health Dashboard (2 days)
**Files:** `apps/web/src/kgr/components/GraphHealth.jsx`

Dashboard widgets:

| Widget | Metric | Visualization |
|---|---|---|
| Completeness | % entities with all required properties filled | Progress bar (green > 80%, amber > 50%, red < 50%) |
| Connectivity | Average degree vs. expected per entity type | Gauge chart |
| Evidence Coverage | % edges backed by evidence references | Progress bar |
| Provenance Depth | Average hops to source-of-truth entity | Number + sparkline |
| Freshness | Time since last ingestion per source system | Status pills (green < 1h, amber < 24h, red > 24h) |
| Density | Graph density vs. theoretical maximum | Number with context |
| Components | Number of disconnected components | Number (1 = fully connected = good) |
| Anomalies | Count of detected anomalous entities | Badge (click to list) |

Accessible from both KGR lens and as a standalone dashboard.

### Tests (Phase 8)
```
tests/unit/test_kgr_whatif.py — 8 tests
tests/unit/test_kgr_anomaly.py — 6 tests
tests/unit/test_kgr_diff.py — 6 tests
```
- 4 tests for what-if removal simulation
- 2 tests for what-if isolation simulation
- 2 tests for what-if API endpoint
- 3 tests for degree z-score outlier detection
- 3 tests for dense subgraph detection
- 2 tests for anomaly API endpoint
- 4 tests for graph diff computation
- 2 tests for diff API endpoint
- All 166+ existing tests continue to pass

---

## Phase 9: Component Wiring & Integration
**Duration:** 1 week  
**Goal:** Connect all existing but disconnected components into KGRExplorer.jsx. The codebase audit revealed that multiple fully-implemented components exist as standalone modules but are not imported or wired into the main KGR orchestrator. This phase resolves that by making every component functional end-to-end.

### 9.1 Wire useGraphEvents Hook into KGRExplorer (0.5 day)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`

The `useGraphEvents` hook (`apps/web/src/kgr/hooks/useGraphEvents.js`) is fully implemented with WebSocket auto-reconnect, event buffering, and gap-fill via HTTP polling. Currently, KGRExplorer manages its own empty events array instead of calling this hook.

- Import and call `useGraphEvents(apiBase)` in KGRExplorer
- Pass returned `events`, `status`, `pause`, `resume`, `clear` to `EventFeed` component
- Remove the placeholder `events` state variable
- Wire connection status indicator into KGR toolbar

### 9.2 Wire LayoutWorker.js into Renderers (0.5 day)
**Files:** modify `apps/web/src/kgr/renderers/SigmaRenderer.jsx`, `apps/web/src/GraphCanvas.jsx`

The `LayoutWorker.js` (`apps/web/src/kgr/renderers/LayoutWorker.js`) implements ForceAtlas2, Dagre, and Cola in a Web Worker context. Currently unused — SigmaRenderer uses its own inline layout and GraphCanvas uses Cytoscape's built-in layouts.

- In SigmaRenderer: use LayoutWorker for graphs > 500 nodes (delegate ForceAtlas2)
- In GraphCanvas: use LayoutWorker for Dagre and Cola layouts (Cytoscape's built-in layouts stay for COSE, circle, grid, etc.)
- Show progress indicator during Web Worker layout computation
- Handle cancellation when user switches layout mid-computation

### 9.3 Wire GraphToolbar into KGRExplorer (0.5 day)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`

The `GraphToolbar.jsx` (`apps/web/src/kgr/components/GraphToolbar.jsx`) provides 12 layout options and node sizing modes. Currently not imported — KGRExplorer has its own inline toolbar controls.

- Import `GraphToolbar` and replace inline toolbar controls in KGRExplorer
- Wire layout change callback to update the active layout in Cytoscape/Sigma
- Wire node sizing mode to update node style computations
- Wire minimap/filter/entity-list toggles to existing state variables

### 9.4 Wire ExportMenu into KGRExplorer (0.5 day)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`, `apps/web/src/kgr/components/ExportMenu.jsx`

The `ExportMenu.jsx` (`apps/web/src/kgr/components/ExportMenu.jsx`) implements 7 export formats. Currently not imported.

- Import `ExportMenu` into KGRExplorer
- Pass Cytoscape ref to enable PNG/SVG export (`cy.png()`, `cy.svg()`)
- Pass current graph elements to enable JSON-LD, GraphML, CSV, Clipboard exports
- Wire "Include annotations" checkbox to read annotations from localStorage
- Add export button to KGR toolbar that toggles the ExportMenu dialog

### 9.5 Wire TimelineScrubber into Temporal View (0.5 day)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`

The `TimelineScrubber.jsx` (`apps/web/src/kgr/components/TimelineScrubber.jsx`) implements play/pause animation, histogram, and dual range handles. Currently not used in KGRExplorer's temporal view.

- Import `TimelineScrubber` and render it below the graph canvas when temporal graph type is active
- Wire `onRangeChange` callback to update temporal filter in filter bar state
- Wire play/pause to animate through time windows
- Pass entity timestamps to compute histogram buckets

### 9.6 Populate Community Filter Dropdown (0.5 day)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`

The community filter dropdown in the filter bar only shows "All communities" and never populates with detected community IDs.

- After community detection API call, extract community IDs and labels
- Populate the community filter dropdown with detected communities
- Allow multi-select filtering by community
- Show member count next to each community option

### 9.7 Connect Minimap Viewport Rectangle (0.5 day)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`, `apps/web/src/kgr/components/Minimap.jsx`

The minimap viewport rectangle is always null because Cytoscape/Sigma renderers don't expose viewport bounds.

- In GraphCanvas: expose viewport bounds via callback or ref (`cy.extent()`)
- In SigmaRenderer: expose camera state (x, y, ratio) as viewport bounds
- Pass viewport bounds to Minimap component
- Update viewport rectangle on zoom/pan events

### 9.8 Implement Side-by-Side Diff View (0.5 day)
**Files:** modify `apps/web/src/kgr/components/GraphDiff.jsx`

The toggle button for side-by-side vs overlay mode exists but both modes render the same change list.

- Overlay mode (existing): single list with +/-/~ badges — already works
- Side-by-side mode: render two graph canvases with synchronized zoom/pan
  - Left canvas: snapshot A entities only, with removed entities highlighted in red
  - Right canvas: snapshot B entities only, with added entities highlighted in green
  - Synchronized zoom/pan: scroll/zoom events mirrored between canvases
- Change list below both views remains the same

### 9.9 Wire Annotation Inclusion in Exports (0.5 day)
**Files:** modify `apps/web/src/kgr/components/ExportMenu.jsx`

The AnnotationPanel mentions annotations are "included in export reports" but ExportMenu doesn't read localStorage annotations.

- In PDF export: append annotation text below each annotated node in the node table
- In JSON-LD export: include `annotation` field on nodes that have one
- In Context export: include annotations object keyed by canonical_id
- Read all `kgr-annotation-node-*` keys from localStorage

### 9.10 Deduplicate Inline vs Standalone Components (1 day)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`

KGRExplorer has inline versions of views that also exist as standalone components in `apps/web/src/kgr/graphs/`. The standalone components should replace the inline code.

- Import and use standalone graph view components:
  - `KnowledgeGraph.jsx` → replace inline knowledge graph rendering
  - `RelationshipGraph.jsx` → replace inline relationship bar chart
  - `MetadataGraph.jsx` → replace inline MetadataGraphView
  - `OntologyGraph.jsx` → replace inline OntologyGraphView
  - `TemporalGraph.jsx` → replace inline temporal view (includes TimelineScrubber)
  - `ProvenanceGraph.jsx` → replace inline ProvenanceGraphView
  - `ImpactGraph.jsx` → replace inline ImpactGraphView
  - `SimilarityGraph.jsx` → replace inline SimilarityGraphView
- Remove duplicated inline code from KGRExplorer
- Pass required props (elements, filters, onSelect, apiBase) to each standalone component
- Target: reduce KGRExplorer.jsx from ~1075 lines to ~500 lines

### Tests (Phase 9)
```
apps/web/tests/kgr-wiring.spec.js — 12 tests
```
- 2 tests: WebSocket events appear in EventFeed
- 2 tests: Layout worker produces positions for ForceAtlas2 and Dagre
- 2 tests: Export menu generates valid PNG, JSON-LD output
- 2 tests: Timeline scrubber updates temporal filter
- 2 tests: Community filter populates from detection results
- 1 test: Minimap viewport rectangle updates on zoom
- 1 test: Side-by-side diff renders two canvases
- All existing tests continue to pass

---

## Phase 10: Advanced Competitor Features
**Duration:** 3 weeks  
**Goal:** Implement the remaining features identified in the comprehensive competitor audit that make KGR definitively superior to every tool in the category. These are features that no single free tool currently offers together.

### 10.1 Node Group Collapsing & Combo Declutter (3 days)
**Files:** `apps/web/src/kgr/components/ComboNode.jsx` (new), modify `apps/web/src/kgr/KGRExplorer.jsx`, modify `apps/web/src/GraphCanvas.jsx`

Implements FR-KGR-010. Addresses a gap in Graphify, Gephi, and code2flow. Matches yFiles (€9.2K), KeyLines (commercial), Linkurious (commercial) — all of which charge for this feature.

Frontend:
```javascript
// ComboNode.jsx
function useComboNodes(elements, groups) {
    // groups: [{id, name, memberIds: [canonical_id]}]
    // Returns: modified elements where grouped nodes are replaced by a single combo node
    // Combo node: {id: group.id, label: group.name, data: {isCombo: true, memberCount, memberIds}}
    // Edges between group members become internal (hidden)
    // Edges between group and external become super-edges with count
}

export function groupByDomain(elements) { /* group nodes by GraphDomain */ }
export function groupByType(elements) { /* group nodes by vertex label */ }
export function groupByCommunity(elements, communities) { /* group by detected community */ }
export function createCustomGroup(selectedIds, name) { /* user-selected grouping */ }
```

Cytoscape.js integration:
- Use Cytoscape.js compound nodes (`parent` field) for visual grouping
- Collapsed state: single node with badge showing member count
- Expanded state: compound node container with members visible inside
- Double-click to toggle collapse/expand
- Keyboard: `G` to group selected nodes, `Shift+G` to ungroup

CSS classes: `.combo-node`, `.combo-badge`, `.combo-expanded`, `.super-edge`

### 10.2 Code + Graph Side-by-Side View (3 days)
**Files:** `apps/web/src/kgr/components/CodePanel.jsx` (new), modify `apps/web/src/kgr/KGRExplorer.jsx`, modify `apps/api/app.py`

Implements FR-KGR-012. Inspired by Sourcetrail's defining feature. No free browser-based tool offers this.

Backend — new API endpoint:
```python
@app.get("/api/v1/files/{path:path}")
async def get_file_content(path: str):
    """Return file content with syntax highlighting hints."""
    # Read file from configured repository path
    # Return: {content: str, language: str, line_count: int}
```

Frontend:
```javascript
// CodePanel.jsx
function CodePanel({ filePath, highlightLines, language, onSymbolClick }) {
    // Split-pane right panel (resizable, 40% default width)
    // Syntax highlighting via highlight.js (already available via CDN)
    // Line numbers with click-to-select
    // Scroll-to-line when highlightLines changes
    // Diff mode: show unified diff when a Commit node is selected
}
```

Integration:
- Click CodeSymbol node → CodePanel shows file at `start_line..end_line`
- Click File node → CodePanel shows entire file
- Click Commit node → CodePanel shows commit diff
- Highlight in code → corresponding graph node selected (bidirectional sync)
- Toggle via toolbar button ("Code Panel")
- Keyboard: `C` to toggle code panel

CSS classes: `.code-panel`, `.code-line`, `.code-highlight`, `.code-gutter`

### 10.3 Four New Export Formats (2 days)
**Files:** modify `apps/web/src/kgr/components/ExportMenu.jsx`

Implements the export gap vs Graphify. Adds GEXF, Obsidian vault, Mermaid, and Cypher.

```javascript
// GEXF export (Gephi-compatible)
function exportGEXF(elements) {
    // XML format: <gexf><graph><nodes><node id="..." label="..."/></nodes>
    //             <edges><edge source="..." target="..." label="..."/></edges></graph></gexf>
    // Include attributes as <attvalue> elements
}

// Obsidian vault export
function exportObsidian(elements) {
    // Create zip with one .md file per entity
    // Folder structure: domain/entity_type/entity_name.md
    // File content: properties as YAML frontmatter, relationships as [[wikilinks]]
    // Example: "## Relationships\n- IMPLEMENTS [[Commit/abc123]]\n- MODIFIES [[File/app.py]]"
}

// Mermaid diagram export
function exportMermaid(elements) {
    // Generate Mermaid graph syntax: "graph TD\n  A[Entity] --> B[Entity]\n  ..."
    // Group by domain with subgraph blocks
    // Limit to visible entities to keep diagrams readable
    // Output as .md file with ```mermaid code block
}

// Cypher script export (Neo4j/FalkorDB compatible)
function exportCypher(elements) {
    // Generate CREATE/MERGE statements
    // Nodes: "MERGE (n:Label {canonical_id: 'id'}) SET n.prop1 = 'val1', ..."
    // Edges: "MATCH (a {canonical_id: 'src'}), (b {canonical_id: 'tgt'}) MERGE (a)-[:TYPE]->(b)"
    // Output as .cypher file
}
```

### 10.4 Visual Query Builder (3 days)
**Files:** `apps/web/src/kgr/components/QueryBuilder.jsx` (new), modify `apps/web/src/kgr/KGRExplorer.jsx`

Implements FR-KGR-013. Matches Linkurious's no-code Query Builder (commercial).

```javascript
// QueryBuilder.jsx
function QueryBuilder({ ontologyManifest, onExecute }) {
    // Canvas area (400x300) for visual query construction
    // Left palette: entity type chips (from ontology manifest vertex labels)
    // Drag entity type to canvas → creates query node
    // Draw edge between query nodes → select edge type from dropdown
    // Click query node → add property filters (key, operator, value)
    // Controls: result limit slider, depth slider
    // "Run" button → converts visual pattern to QueryPlan JSON
    // "Save" button → persist to localStorage
    // "Load" button → restore saved queries
    // "Clear" button → reset canvas
}

function visualPatternToQueryPlan(pattern) {
    // Convert visual node+edge pattern to EOIP QueryPlan
    // {intent: "SEARCH", anchors: [...], filters: [...], max_depth, result_limit}
}
```

Accessible from KGR toolbar as "Query Builder" button. Opens as a modal overlay.
Keyboard shortcut: `Q` to toggle query builder.

CSS classes: `.query-builder`, `.qb-canvas`, `.qb-palette`, `.qb-node`, `.qb-edge`, `.qb-filter`

### 10.5 Dead Code & Orphaned Entity Detection (2 days)
**Files:** modify `packages/eoip/graph/anomaly.py`, modify `apps/api/app.py`, modify `apps/web/src/kgr/components/GraphHealth.jsx`

Implements FR-KGR-014. Matches code2flow's orphaned function detection. Extended to cover all entity types.

Backend:
```python
# Add to AnomalyDetector
def orphaned_entities(self, entity_types: list[str] | None = None) -> list[AnomalyResult]:
    """Find entities with zero incoming edges (unreferenced).
    Excludes meta-graph entities (GraphDomain, OntologyVersion, DataSource).
    Optionally filter to specific entity types (e.g., ['CodeSymbol', 'File'])."""

def stale_entities(self, threshold_hours: int = 168) -> list[AnomalyResult]:
    """Find entities whose last ingestion_run is older than threshold."""
```

New API endpoint:
```python
@app.get("/api/v1/graph/orphaned")
async def orphaned_entities(types: str = Query(default=None)):
    # Returns: [{canonical_id, label, name, in_degree: 0, last_ingestion_run}]
```

Frontend — add to GraphHealth.jsx:
- "Dead Code" widget: count of CodeSymbol entities with zero CALLED_BY/REFERENCES/IMPORTS edges
- "Orphaned Entities" widget: count of entities with zero incoming edges
- "Stale Entities" widget: count of entities not updated in >7 days
- Click any count to filter the main graph to show only those entities

### 10.6 Community Auto-Labeling (1 day)
**Files:** modify `packages/eoip/graph/community.py`, modify `apps/web/src/kgr/KGRExplorer.jsx`

Implements FR-KGR-015.

Backend:
```python
# Add to CommunityDetectionEngine
def label_community(self, member_ids: list[str]) -> str:
    """Generate a human-readable label for a community.
    Algorithm: extract top-3 most common vertex labels + top-2 most common
    property values (e.g., 'Code: auth-service, API, security').
    Format: '{dominant_label}: {key_terms}'."""
```

Update `CommunityResult` to include labels:
```python
class Community:
    id: int
    members: list[str]
    size: int
    label_distribution: dict[str, int]
    auto_label: str  # NEW: generated label
```

Frontend:
- Show community labels on convex hull overlays
- Use labels in community filter dropdown instead of numeric IDs
- Allow user to rename a community label (override stored in localStorage)
- Community summary card on hull click: member count, dominant types, hub nodes, density

### 10.7 Geo-Mode (2 days)
**Files:** `apps/web/src/kgr/components/GeoMap.jsx` (new), modify `apps/web/src/kgr/KGRExplorer.jsx`

Implements FR-KGR-011. Matches Linkurious and Ogma (both commercial).

```javascript
// GeoMap.jsx
function GeoMap({ elements, onSelect }) {
    // Leaflet.js map (via CDN) with OpenStreetMap tiles
    // Place nodes at [latitude, longitude] from entity properties
    // Nodes without location: sidebar list or default position
    // Curved edge rendering between geo-positioned nodes
    // Zoom levels with progressive entity display
    // Click node → select in inspector
    // Toggle between geo-mode and standard layout
}
```

- Map tile caching: service worker caches tiles for offline use after initial load
- Available as layout option #13 in GraphToolbar
- Entities require `latitude`/`longitude` properties or `region`/`datacenter` tags
- Graceful degradation: if <3 entities have location data, show message with instructions

CSS classes: `.geo-map`, `.geo-node`, `.geo-edge`, `.geo-sidebar`

### 10.8 PR / Change Impact Dashboard (2 days)
**Files:** `apps/web/src/kgr/components/PRDashboard.jsx` (new), modify `apps/web/src/kgr/KGRExplorer.jsx`, modify `apps/api/app.py`

Implements FR-KGR-016. Inspired by Graphify's `graphify prs` with community-based conflict detection.

Backend:
```python
@app.get("/api/v1/graph/pr-impact")
async def pr_impact():
    """Analyze open PRs/MRs for community overlap and conflict risk."""
    # 1. Fetch open MRs from GitLab connector (or PRs from GitHub)
    # 2. For each MR: find Commit vertices, trace to modified entities
    # 3. Map modified entities to communities (from last community detection run)
    # 4. Compute pairwise overlap between MRs
    # 5. Return: [{mr_id, title, author, communities_touched: [], entities_modified: int}]
    # 6. conflicts: [{mr_a, mr_b, overlap_communities: [], overlap_pct: float, risk: "HIGH"|"MEDIUM"|"LOW"}]
```

Frontend:
```javascript
// PRDashboard.jsx
function PRDashboard({ apiBase }) {
    // Table of open PRs/MRs with columns: title, author, status, communities touched, entities modified
    // Conflict matrix: heatmap showing pairwise overlap between PRs
    // Click a PR → highlight its affected entities on the graph
    // Click a conflict → show both PRs' blast radius overlap
    // Risk indicators: HIGH (red), MEDIUM (amber), LOW (green)
}
```

Accessible from KGR toolbar as "PR Impact" button. Opens as a side panel.

CSS classes: `.pr-dashboard`, `.pr-row`, `.conflict-matrix`, `.conflict-cell`, `.risk-badge`

### 10.9 AMBIGUOUS Evidence Status Support (0.5 day)
**Files:** modify `packages/eoip/ontology/manifest.py`, modify `apps/web/src/kgr/KGRExplorer.jsx`, modify `apps/web/src/kgr/components/EdgeInspector.jsx`

Adds AMBIGUOUS as a fourth evidence status alongside DETERMINISTIC, INFERRED, and MANUAL. This matches Graphify's three-tier evidence system (EXTRACTED/INFERRED/AMBIGUOUS) and extends it.

Backend:
- Add `"AMBIGUOUS"` to the allowed `creation_status` values in the validation gate
- AMBIGUOUS = evidence that couldn't be fully resolved (dynamic dispatch, reflection, string-built imports)

Frontend:
- Trust badge: AMBIGUOUS gets orange color (between INFERRED amber and DETERMINISTIC green)
- Edge style: AMBIGUOUS edges rendered with dotted-dash pattern (distinct from INFERRED dashed)
- Filter bar trust filter: add AMBIGUOUS option to the radio group (Deterministic / Inferred / Ambiguous / Manual / All)

### Tests (Phase 10)
```
tests/unit/test_kgr_combo.py — 6 tests
tests/unit/test_kgr_orphaned.py — 6 tests
tests/unit/test_kgr_community_labels.py — 4 tests
tests/unit/test_kgr_pr_impact.py — 4 tests
apps/web/tests/kgr-advanced.spec.js — 10 tests
```
- 3 tests for combo node creation (by domain, type, community)
- 3 tests for combo edge aggregation
- 3 tests for orphaned entity detection
- 3 tests for stale entity detection
- 4 tests for community auto-labeling
- 2 tests for PR impact endpoint
- 2 tests for conflict detection
- 2 tests for GEXF export validation
- 2 tests for Obsidian export structure
- 2 tests for Mermaid export syntax
- 2 tests for Cypher export syntax
- 2 tests for AMBIGUOUS evidence filtering
- 2 tests for visual query builder → QueryPlan conversion
- All existing tests continue to pass

---

## Cross-Cutting Concerns (Applied Across All Phases)

### CSS Design System Extension
**File:** `apps/web/src/style.css`

Existing KGR classes (Phase 1 — done):
```css
.kgr-explorer, .kgr-type-bar, .kgr-filter-bar, .filter-chip,
.kgr-inspector, .impact-summary, .relationship-summary, .edge-list,
.depth-breakdown, .type-breakdown, .annotation-panel,
.kgr-metadata-view, .schema-grid, .schema-card, .ontology-domain-grid,
.kgr-provenance-view, .provenance-list, .kgr-blast-overlay,
.blast-header, .blast-rings, .blast-types
```

New classes to add per phase:
- Phase 2: `.edge-inspector`, `.similarity-graph`, `.impact-graph`, `.raw-tab`, `.history-tab`
- Phase 3: `.centrality-radar`, `.radar-axis`, `.radar-polygon`, `.path-highlight`
- Phase 4: `.context-menu`, `.context-menu-item`, `.filter-preset`, `.exploration-breadcrumb`, `.bookmark-bar`, `.community-hull`
- Phase 5: `.timeline-scrubber`, `.timeline-handle`, `.export-dialog`, `.semantic-zoom-*`, `.fisheye-lens`, `.annotation-dot`
- Phase 6: `.sigma-container`, `.progressive-loader`, `.virtual-list`
- Phase 7: `.event-feed`, `.event-item`, `.ws-status`, `.change-badge`
- Phase 8: `.graph-diff`, `.diff-overlay`, `.whatif-modal`, `.health-dashboard`, `.health-widget`
- Phase 9: (no new classes — wiring phase uses existing component CSS)
- Phase 10: `.combo-node`, `.combo-badge`, `.combo-expanded`, `.super-edge`, `.code-panel`, `.code-line`, `.code-highlight`, `.code-gutter`, `.query-builder`, `.qb-canvas`, `.qb-palette`, `.qb-node`, `.qb-edge`, `.qb-filter`, `.geo-map`, `.geo-node`, `.geo-edge`, `.geo-sidebar`, `.pr-dashboard`, `.pr-row`, `.conflict-matrix`, `.conflict-cell`, `.risk-badge`, `.ambiguous-edge`, `.orphan-indicator`

All classes follow existing design system tokens (CSS variables for colors, spacing, radii).
Dark mode support via existing `@media (prefers-color-scheme: dark)` pattern.

### Testing Strategy
- **Unit tests**: Every new Python module and utility function
- **Component tests**: React component rendering (vitest or manual verification)
- **Integration tests**: Lens switching, context sharing, API roundtrips
- **Performance tests**: Rendering benchmarks at 1K, 5K, 10K, 50K nodes
- **Accessibility tests**: Keyboard navigation, screen reader, color-blind modes
- **Regression**: All 166+ existing tests must pass after each phase
- **Target**: > 80% coverage on new Python code, reasonable coverage on JS

### Dependencies

```
# Python (already in requirements or to add)
# No new Python dependencies — all algorithms implemented from scratch
# This avoids the dependency bloat that plagues Graphistry, yFiles, Neo4j

# JavaScript (via CDN or bundled)
sigma@3.x          # WebGL renderer (Phase 6)
graphology@0.25+   # Graph data structure for algorithms
graphology-communities-louvain  # Community detection
graphology-layout-forceatlas2   # ForceAtlas2 layout
graphology-metrics  # Centrality metrics
jspdf@2.x          # PDF export (Phase 5)
leaflet@1.9+       # Geo-mode map rendering (Phase 10)
highlight.js@11.x  # Code panel syntax highlighting (Phase 10)
```

---

## Phase Summary

| Phase | Duration | Key Deliverables | New Tests | Competitor Gaps Closed |
|---|---|---|---|---|
| 1 | 2 weeks | **DONE** — Metrics engine, 5 API endpoints, KGR Explorer, 6 graph types | 19 | Blast radius (none had it), evidence chains |
| 2 | 2 weeks | Component extraction, 8 graph types, 8-tab inspector, edge inspector | ~15 | 8 graph types (max 1-2 elsewhere) |
| 3 | 2 weeks | Full centrality (8 algos), client-side algorithms, radar chart, path finding | ~28 | Full centrality (Gephi desktop-only, Bloom needs GDS) |
| 4 | 2 weeks | Community detection, 10-dim filtering, keyboard nav, context menu, undo/redo | ~35 | Leiden (free, in-browser), undo/redo, full keyboard nav |
| 5 | 2 weeks | Timeline, 7-format export, annotations, semantic zoom, fisheye, similarity | ~25 | 7 export formats, annotations, visual intelligence |
| 6 | 1.5 weeks | Sigma.js WebGL, Web Worker layouts, progressive rendering, k-core | ~10 | 50K+ nodes (Graphify: 5K, Sourcetrail: crashes) |
| 7 | 1 week | WebSocket events, incremental updates, event feed | ~8 | Real-time (Graphify: stale, CodeSee: sunset) |
| 8 | 1.5 weeks | Graph diff, what-if simulation, anomaly detection, health dashboard | ~20 | What-if (none), anomaly (none), diff (yFiles only) |
| 9 | 1 week | Wire all disconnected components into KGRExplorer, deduplicate inline code | ~12 | End-to-end integration of all Phase 2-8 features |
| 10 | 3 weeks | Node grouping, code+graph, 4 new exports, visual query builder, dead code, geo-mode, PR dashboard, community labeling, AMBIGUOUS evidence | ~30 | Node grouping (yFiles €9.2K), code+graph (Sourcetrail dead), all Graphify exports, no-code queries (Linkurious $$), PR conflicts (Graphify basic) |
| **Total** | **~18 weeks** | **Complete KGR platform — surpasses every competitor** | **~190+** | **Every competitor gap closed, every Graphify feature matched or exceeded** |

### Definition of Done (per phase)
1. All new components render correctly in browser
2. All new API endpoints return valid responses with proper error handling
3. All new tests pass (`python -m pytest tests/`)
4. All existing 166+ tests continue to pass
5. No new lint warnings
6. CSS follows existing design system tokens
7. No external network requests in production
8. Keyboard-accessible (WCAG 2.1 AA)
9. Dark mode supported
10. Responsive down to 768px

### Dependencies Between Phases
```
Phase 1 ──────┐
  (DONE)      ├── Phase 2 ──── Phase 3 ──── Phase 5
              │                   │
              ├── Phase 4 ────────┤
              │                   │
              ├── Phase 6 ────────┤
              │                   │
              ├── Phase 7         │
              │                   │
              └── Phase 8 ───────(depends on Phase 3 metrics)
                                  │
              Phase 9 ────────────┤ (depends on all of Phases 2-8 being built)
                                  │
              Phase 10 ───────────┘ (depends on Phase 9 wiring being complete)
```

- Phase 1 is the foundation; all subsequent phases depend on it
- Phases 2, 4, 6, 7 can start in parallel after Phase 1
- Phase 3 depends on Phase 2 (inspector enhancements)
- Phase 5 depends on Phases 2-4 (needs all UI components in place)
- Phase 8 depends on Phase 3 (metrics engine for what-if)
- **Phase 9** depends on all of Phases 2-8 (wires disconnected components together)
- **Phase 10** depends on Phase 9 (builds advanced features on a fully integrated KGRExplorer)

---

## Competitive Advantage Summary

After all 10 phases, KGR will have:

| Capability | KGR | Best Competitor | Gap |
|---|---|---|---|
| Graph types | 10 purpose-built | 1-2 (yFiles configurable) | 5-10x more |
| Max interactive nodes | 50K+ (WebGL) | 8M (Graphistry, needs GPU) | CPU-only, no GPU needed |
| Centrality algorithms | 8 | 6 (Gephi, desktop only) | In-browser, not desktop |
| Community detection | 3 algorithms + auto-labeling | 1 (Graphify: Leiden, basic labeling) | 3x algorithms, visual hulls, smart labels |
| Impact analysis | Blast radius + reverse + what-if | None | Unique to KGR |
| Evidence/provenance | 4-tier (DETERMINISTIC/INFERRED/AMBIGUOUS/MANUAL) | 3-tier (Graphify: EXTRACTED/INFERRED/AMBIGUOUS) | Matches + extends |
| Inspector tabs | 8 | 3 (Sourcetrail) | 2.7x richer |
| Filter dimensions | 11 | 5 (Linkurious faceted) | 2.2x |
| Export formats | 11 (PNG, SVG, PDF, JSON-LD, GraphML, GEXF, CSV, Obsidian, Mermaid, Cypher, clipboard) | 7 (Graphify: HTML/JSON/GraphML/SVG/Obsidian/Mermaid/Cypher) | Matches all Graphify exports + adds PDF/JSON-LD/GEXF |
| Layout algorithms | 13 (incl. geo-mode) | 20 (yFiles, €9.2K/yr) | Free, 65% coverage |
| Node group collapsing | Domain/type/community/custom | yFiles (€9.2K), KeyLines (commercial) | Free, built-in |
| Code + graph view | Browser-based, all languages | Sourcetrail (discontinued, 4 langs, desktop) | Alive, browser, all languages |
| Visual query builder | No-code drag-and-drop | Linkurious (commercial) | Free, integrated |
| Dead code detection | All entity types, visual indicators | code2flow (4 langs, CLI only) | All types, interactive |
| PR conflict detection | Community-based overlap analysis | Graphify (list only, no visual) | Visual overlap + risk scoring |
| Keyboard navigation | Full | None complete | WCAG 2.1 AA |
| Real-time updates | WebSocket + polling | Streaming (Graphistry, GPU) | No GPU needed |
| Graph diff | Overlay + side-by-side | Basic (yFiles only) | Visual + structural |
| What-if simulation | Full simulation | None | Unique to KGR |
| Anomaly detection | 3 algorithms + orphan detection | None (in viz tool) | Unique to KGR |
| Geo-mode | Map-based layout | Linkurious, Ogma (commercial) | Free |
| Price | $0 (bundled) | $0-$11K/year | Free |
| Local-first | Yes | Varies | No cloud dependency |
| Open/extensible | Yes | Varies | No vendor lock-in |

---

## Research Sources Informing This Plan

This implementation plan is informed by comprehensive competitive analysis of 16+ tools and deep-dive research across 10 streams:

1. **Graphify** (123K stars): Tree-sitter AST for ~40 languages, Leiden community detection, graph.html breaks at 5K nodes, AI assistants bypass graph, graph freshness problem, Ollama drops 96% of edges, multiple parser bugs
2. **Sourcetrail** (discontinued Sep 2021): Three-panel UI (graph+code+search), 4 languages only, slow indexing, desktop-only, crashes on large projects
3. **Sourcegraph** ($49-59/user/month): Universal code search (Zoekt), SCIP code intel, Cody AI, batch changes; went closed source, complex self-hosted
4. **CodeSee** (sunset by GitKraken May 2024): Codebase maps, review maps, code tours; GitHub-only, cloud-only
5. **code2flow**: Call graph via AST for Python/JS/Ruby/PHP; CLI only, 4 languages, no interactive navigation
6. **Graphistry**: GPU-accelerated (8M nodes), GFQL query language; hard GPU dependency, expensive ($1.47-10/hr), vendor lock-in
7. **yFiles**: Best layout algorithms (20+), multi-platform SDKs, real-time collaboration; €9,200+/year, steep learning curve, closed source
8. **Neo4j Bloom**: NL queries, scenes, perspectives; Neo4j lock-in, expensive, limited analytics without GDS
9. **Linkurious**: Search-to-explore, case management, alerting; expensive commercial, limited backends
10. **Gephi**: Rich analytics, ForceAtlas2, modularity statistics; desktop-only, Java, stagnant development
11. **KeyLines**: Time bar, geospatial, compound graphs; expensive SDK-only, no open source
12. **Ogma**: Force + hierarchical + radial layouts, WebGL; commercial, limited community
13. **G6/Graphin**: Rich interactions, plugins, React integration; Chinese documentation, limited enterprise adoption
14. **Cytoscape desktop**: 90+ plugins, biological network analysis; desktop-only, academic focus
15. **Graph algorithm research**: 60+ algorithms across centrality, community detection, similarity, paths, anomaly detection, structure analysis
16. **Visualization technique research**: ForceAtlas2, Sugiyama hierarchical, compound graphs, FDEB edge bundling, semantic zoom, LOD rendering, fisheye distortion, WebGL/WebGPU capabilities
17. **UX pattern research**: Search-to-explore (Linkurious), progressive disclosure, undo/redo exploration, collaborative annotations, NL graph queries, AI-assisted exploration, dashboard integration
