# KGR — Knowledge Graph Renderer: Phase-by-Phase Implementation Plan

**Version:** 1.0  
**Date:** 2026-10-02  
**Baseline:** EOIP current state (123+ tests passing, full App.jsx with 5 lenses, GraphCanvas with Cytoscape.js)  
**Target:** Graphify-class+ knowledge graph exploration platform

---

## Architecture Overview

### Rendering Strategy
- **Primary renderer**: Cytoscape.js (existing, extend) for graphs up to 5K nodes
- **Large-graph renderer**: Sigma.js (WebGL) for 5K-50K+ nodes, progressive fallback
- **Layout engine**: Web Worker-based layout computation for graphs > 500 nodes
- **Data layer**: graphology library for in-memory graph algorithms (centrality, community detection, shortest path)

### Component Architecture
```
apps/web/src/
├── App.jsx                          (existing — extend with KGR lens routing)
├── GraphCanvas.jsx                  (existing — enhance with advanced features)
├── kgr/
│   ├── KGRExplorer.jsx              (main KGR container, graph type switching)
│   ├── GraphTypeSelector.jsx        (tab bar for 6 graph types)
│   ├── FilterBar.jsx                (multi-dimensional filtering)
│   ├── NodeInspector.jsx            (extended inspector with 6 tabs)
│   ├── EdgeInspector.jsx            (relationship intelligence panel)
│   ├── BlastRadius.jsx              (concentric ring blast radius view)
│   ├── CentralityRadar.jsx          (radar chart for centrality metrics)
│   ├── Minimap.jsx                  (thumbnail overview navigator)
│   ├── TimelineScrubber.jsx         (temporal graph navigation)
│   ├── GraphToolbar.jsx             (extended toolbar controls)
│   ├── ExportMenu.jsx               (PNG/SVG/JSON/CSV export)
│   ├── AnnotationPanel.jsx          (node/edge annotations)
│   ├── GraphBookmarks.jsx           (saved view management)
│   ├── renderers/
│   │   ├── CytoscapeRenderer.jsx    (Cytoscape.js wrapper, extends existing)
│   │   ├── SigmaRenderer.jsx        (Sigma.js/WebGL for large graphs)
│   │   └── LayoutWorker.js          (Web Worker for layout computation)
│   ├── graphs/
│   │   ├── KnowledgeGraph.jsx       (primary entity-relationship view)
│   │   ├── RelationshipGraph.jsx    (edge-centric analysis view)
│   │   ├── MetadataGraph.jsx        (schema topology view)
│   │   ├── OntologyGraph.jsx        (class hierarchy view)
│   │   ├── TemporalGraph.jsx        (time-windowed view)
│   │   └── ProvenanceGraph.jsx      (lineage/evidence chain view)
│   └── analysis/
│       ├── centrality.js            (client-side centrality computation)
│       ├── community.js             (Leiden/Louvain community detection)
│       ├── blast-radius.js          (BFS-based blast radius computation)
│       └── graph-metrics.js         (density, diameter, components)

packages/eoip/
├── graph/
│   ├── metrics.py                   (centrality, PageRank, blast radius)
│   └── community.py                 (Leiden community detection)
├── query/
│   └── executor.py                  (existing — extend with metrics intents)

apps/api/
├── app.py                           (existing — extend with KGR endpoints)
└── main.py                          (existing — add graph metrics routes)
```

### Backend API Additions
```python
# New endpoints in apps/api/app.py
POST /api/v1/graph/metrics          # centrality, PageRank, blast radius
POST /api/v1/graph/blast-radius     # downstream impact count + list
POST /api/v1/graph/reverse-impact   # upstream dependency count
POST /api/v1/graph/cluster          # community detection
POST /api/v1/graph/diff             # compare two graph snapshots
GET  /api/v1/graph/schema           # meta-graph (labels, edge types, properties)
GET  /api/v1/graph/statistics       # aggregate graph-level stats
POST /api/v1/graph/what-if          # simulate entity removal
```

---

## Phase 1: Foundation — Enhanced Graph Canvas & Node Intelligence
**Duration:** 2 weeks  
**Goal:** Transform the existing GraphCanvas into a professional-grade graph exploration component with deep node inspection.

### 1.1 Enhanced Node Inspector (3 days)
**Files:** `apps/web/src/kgr/NodeInspector.jsx` (new), modify `apps/web/src/App.jsx`

- Create a 6-tab inspector replacing the current EntityInspector:
  - **Overview**: Properties, identity, domain, creation metadata
  - **Relationships**: In/out edges grouped by type with counts, expandable lists
  - **Impact**: Blast radius preview, centrality scores, risk classification
  - **Evidence**: Source references, trust score, provenance chain depth
  - **History**: Temporal changes (when available), ingestion runs
  - **Annotations**: User notes stored in localStorage
- Responsive side panel (collapsible, resizable via drag handle)
- Keyboard navigation within inspector (Tab between tabs, Enter to expand)

### 1.2 Enhanced Edge Inspector (2 days)
**Files:** `apps/web/src/kgr/EdgeInspector.jsx` (new)

- Source/target entity summaries with mini-preview
- Edge type with semantic meaning from ontology manifest
- All edge properties with type-aware formatting
- Evidence backing display (source_ref, evidence_key, method)
- Creation status badge (DETERMINISTIC, INFERRED, MANUAL)
- Parallel edge indicator (other relationships between same endpoints)
- Path context (which known paths use this edge)

### 1.3 Graph Toolbar Extension (2 days)
**Files:** `apps/web/src/kgr/GraphToolbar.jsx` (new), modify `apps/web/src/GraphCanvas.jsx`

- Add 4 new layout algorithms (dagre, concentric, radial, clustered) to existing 4
- Fullscreen toggle for graph canvas
- Node sizing control (uniform, by degree, by centrality)
- Edge label toggle (separate from node labels)
- Settings gear with: animation speed, edge bundling threshold, label truncation length
- Filter summary chips showing active filters

### 1.4 Minimap Component (2 days)
**Files:** `apps/web/src/kgr/Minimap.jsx` (new)

- Thumbnail overview (200x150px) in bottom-right corner
- Viewport rectangle showing current visible area
- Click-to-navigate: click anywhere on minimap to recenter
- Auto-hide when graph has fewer than 20 nodes
- Toggle on/off from toolbar

### 1.5 Backend: Graph Schema Endpoint (1 day)
**Files:** modify `apps/api/app.py`, `packages/eoip/ontology/manifest.py`

- `GET /api/v1/graph/schema` returns meta-graph:
  - All vertex labels with property schemas (required/optional)
  - All edge labels with allowed source/target types
  - Index coverage per label
  - Instance counts per label and edge type
- Used by Metadata Graph and Ontology Graph views

### Tests
- 15+ unit tests for inspector tab rendering
- 8+ tests for toolbar state management
- 5+ tests for minimap viewport calculations
- 3+ API tests for schema endpoint
- All 123+ existing tests continue to pass

---

## Phase 2: Multi-Graph Type System
**Duration:** 2 weeks  
**Goal:** Implement 6 graph type views, each transforming the same underlying data into a purpose-specific visualization.

### 2.1 KGR Explorer Container (2 days)
**Files:** `apps/web/src/kgr/KGRExplorer.jsx` (new), `apps/web/src/kgr/GraphTypeSelector.jsx` (new)

- Main container component managing:
  - Active graph type state
  - Shared filter state across graph types
  - Graph data transformations per type
  - Inspector panel routing
- Tab bar with 6 graph types: Knowledge, Relationship, Metadata, Ontology, Temporal, Provenance
- Smooth CSS transitions when switching types
- Each type retains independent layout and viewport state

### 2.2 Knowledge Graph View (2 days)
**Files:** `apps/web/src/kgr/graphs/KnowledgeGraph.jsx` (new)

- Primary view (reuses enhanced GraphCanvas)
- Full entity-centric exploration with all new inspector features
- Domain coloring, evidence overlay, trust indicators
- This is the "default" view and most closely matches current graph lens behavior
- Seamless migration from existing Graph lens

### 2.3 Relationship Graph View (2 days)
**Files:** `apps/web/src/kgr/graphs/RelationshipGraph.jsx` (new)

- Transform: edge types become nodes, connected by shared endpoint types
- Node size proportional to edge instance count
- Co-occurrence matrix heatmap view (toggle from graph view)
- Clicking a relationship-type node shows all instances of that relationship
- Useful for understanding the relationship model at a glance

### 2.4 Metadata Graph View (2 days)
**Files:** `apps/web/src/kgr/graphs/MetadataGraph.jsx` (new)

- Transform: vertex labels become nodes, edge labels become connecting edges
- Property schema overlay (hover to see required/optional properties per label)
- Index coverage indicators (green checkmark for indexed, gray for unindexed)
- Instance count badges on each label node
- Uses data from `/api/v1/graph/schema` endpoint

### 2.5 Ontology Graph View (2 days)
**Files:** `apps/web/src/kgr/graphs/OntologyGraph.jsx` (new)

- Class hierarchy tree layout (EOIP's GraphDomain → vertex labels)
- Domain decomposition: GraphDomain nodes at top, member types below
- Property list per type (from ontology manifest)
- Cardinality indicators (required properties marked)
- Ontology version display with schema version
- Uses hierarchical (breadthfirst) layout by default

### 2.6 Temporal Graph View (1 day)
**Files:** `apps/web/src/kgr/graphs/TemporalGraph.jsx` (new)

- Time-windowed filtering of entities by creation/ingestion timestamp
- Basic timeline bar at bottom (range slider)
- Nodes positioned along X-axis by timestamp when timeline layout active
- Color encoding: recent entities brighter, older entities faded
- Placeholder for full timeline scrubber (Phase 5)

### 2.7 Provenance Graph View (1 day)
**Files:** `apps/web/src/kgr/graphs/ProvenanceGraph.jsx` (new)

- Evidence chain visualization: source → ingestion → entity
- IngestionRun and Evidence nodes prominently displayed
- Cross-system highlighting (entities from multiple source systems)
- Trust propagation visual (evidence-backed edges vs. inferred)
- Uses existing lineage API data

### 2.8 Integration with Existing App (1 day)
**Files:** modify `apps/web/src/App.jsx`

- Add "KGR" as a new primary lens in the lens bar
- KGR lens renders KGRExplorer container
- Existing lenses (Search, Graph, Impact, Evidence, Architecture) continue unchanged
- Context sharing: selecting an entity in KGR populates the shared lens context
- Graph data from search/impact results available in KGR

### Tests
- 6 component tests (one per graph type view)
- 8 transformation tests (data transform for each graph type)
- 5 integration tests (lens switching, context sharing)
- 3 API tests for extended schema endpoint

---

## Phase 3: Blast Radius & Impact Analysis Intelligence
**Duration:** 2 weeks  
**Goal:** Implement the full impact analysis stack — blast radius computation, centrality metrics, and visual intelligence.

### 3.1 Backend: Graph Metrics Engine (3 days)
**Files:** `packages/eoip/graph/metrics.py` (new), modify `apps/api/app.py`

```python
# packages/eoip/graph/metrics.py
class GraphMetricsEngine:
    def blast_radius(self, canonical_id: str, max_depth: int = 4) -> BlastRadiusResult
    def reverse_impact(self, canonical_id: str, max_depth: int = 4) -> ReverseImpactResult
    def centrality(self, node_ids: list[str]) -> dict[str, CentralityMetrics]
    def what_if_remove(self, canonical_id: str) -> WhatIfResult
```

- **Blast radius**: BFS from target node along outgoing edges, collect at each depth
  - Group by depth (1-hop, 2-hop, 3-hop, 4-hop)
  - Group by entity type at each depth
  - Compute affected path count
  - Risk classification: HIGH (>20% reachable), MEDIUM (5-20%), LOW (<5%)
- **Centrality metrics**: Compute for requested node set
  - Degree centrality (in/out/total normalized)
  - Betweenness centrality (fraction of shortest paths)
  - Closeness centrality (inverse avg shortest path)
  - PageRank (iterative, 20 iterations, damping=0.85)
- **What-if simulation**: Remove entity, compute broken paths, orphaned nodes, new centrality

API endpoints:
```
POST /api/v1/graph/blast-radius    → BlastRadiusResult
POST /api/v1/graph/reverse-impact  → ReverseImpactResult
POST /api/v1/graph/metrics         → dict[node_id, CentralityMetrics]
POST /api/v1/graph/what-if         → WhatIfResult
```

### 3.2 Client-Side Graph Algorithms (2 days)
**Files:** `apps/web/src/kgr/analysis/centrality.js`, `blast-radius.js`, `graph-metrics.js` (new)

- Client-side computation using graphology library for immediate feedback:
  - Degree centrality (instant)
  - Graph density, component count
  - BFS blast radius preview (for small graphs < 500 nodes)
- Falls back to server API for large graphs or PageRank/betweenness
- Web Worker wrapper for computation > 200ms

### 3.3 Blast Radius Visualization (3 days)
**Files:** `apps/web/src/kgr/BlastRadius.jsx` (new)

- Concentric ring layout centered on selected entity
- Ring 1: direct dependencies (1-hop)
- Ring 2: transitive dependencies (2-hop)
- Ring 3-4: further transitive reach
- Color intensity fades with distance (deep red → orange → yellow → gray)
- Each ring labeled with hop count and entity count
- Entity type breakdown per ring as legend
- Risk badge: HIGH/MEDIUM/LOW with percentage
- Animated propagation mode: wave effect showing impact spreading
- Clickable nodes in rings to drill into their own blast radius

### 3.4 Centrality Radar Chart (2 days)
**Files:** `apps/web/src/kgr/CentralityRadar.jsx` (new)

- SVG-based radar/spider chart in inspector Impact tab
- 5 axes: Degree, Betweenness, Closeness, PageRank, Blast Radius
- Normalized 0-1 scale with percentile ranking
- Comparison mode: overlay two entities' radar charts
- Tooltip on each axis explaining the metric

### 3.5 Inspector Impact Tab Integration (2 days)
**Files:** modify `apps/web/src/kgr/NodeInspector.jsx`

- Impact tab shows:
  - Blast radius summary (N entities at M depth, risk level)
  - "Explore Blast Radius" button → opens BlastRadius view
  - Centrality radar chart
  - Change propagation score (% of graph affected)
  - Critical path membership count
  - "Run What-If" button → simulated removal analysis
- Reverse impact section (upstream dependencies)

### Tests
- 12+ unit tests for metrics engine (blast radius, centrality, what-if)
- 6+ API endpoint tests
- 8+ component tests (blast radius view, radar chart, inspector tab)
- Performance tests (blast radius computation < 2s for 1K nodes)

---

## Phase 4: Advanced Filtering & Community Detection
**Duration:** 2 weeks  
**Goal:** Multi-dimensional filtering, community detection, and search intelligence.

### 4.1 Multi-Dimensional Filter Bar (3 days)
**Files:** `apps/web/src/kgr/FilterBar.jsx` (new)

- **Domain filter**: Multi-select dropdown of GraphDomains
- **Entity type filter**: Checkbox list of vertex labels with counts
- **Relationship filter**: Checkbox list of edge types with counts
- **Trust filter**: Deterministic / Inferred / All (radio)
- **Evidence filter**: Evidenced / Unevidenced / All (radio)
- **Property filter**: Key-value filter builder (property = value)
- Active filter chips with click-to-remove
- Filter state persists across graph type switches
- "Save preset" button to store named filter configurations
- Filter presets stored in localStorage

### 4.2 Community Detection (3 days)
**Files:** `packages/eoip/graph/community.py` (new), `apps/web/src/kgr/analysis/community.js` (new)

Backend:
- Leiden algorithm implementation for community detection
- `POST /api/v1/graph/cluster` → CommunityResult with community memberships
- Configurable resolution parameter

Frontend:
- Cluster hull overlays on graph canvas (convex hulls around community members)
- Community coloring mode (toggle from toolbar)
- Community legend showing detected communities with member counts
- Click community hull to filter to that community's members

### 4.3 Enhanced Search (2 days)
**Files:** modify `apps/web/src/App.jsx` search form area

- Typeahead suggestions from recent entities and common queries
- Faceted search results in KGR (grouped by domain AND type)
- Search history with re-execution
- "Search within current view" option (filter existing graph without new API call)
- Quick filters from search suggestions ("Show all WorkItems", "Show all Files")

### 4.4 Keyboard Navigation (2 days)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`, `NodeInspector.jsx`

- Tab through nodes in the entity strip
- Enter to select, Escape to deselect
- Arrow keys to traverse edges (left/right for siblings, up/down for in/out edges)
- `E` to expand selected node's neighborhood
- `I` to toggle inspector panel
- `F` to toggle filter bar
- `1-6` to switch graph types
- Focus ring styling for accessibility

### 4.5 Context Menu (2 days)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`

- Right-click context menu for nodes:
  - Expand neighborhood (1-hop, 2-hop, 3-hop)
  - Explore blast radius
  - Find paths from/to this entity
  - Trace lineage
  - Hide node
  - Pin/unpin position
  - Copy canonical ID
  - Add annotation
- Right-click context menu for edges:
  - Inspect relationship
  - Show evidence
  - Find parallel edges
  - Hide edge type
  - Copy edge details
- Right-click on canvas background:
  - Fit all
  - Reset filters
  - Export view

### 4.6 Saved Filter Presets & Bookmarks (1 day)
**Files:** `apps/web/src/kgr/GraphBookmarks.jsx` (new)

- Save current view state: query + filters + graph type + layout + viewport position
- Named bookmarks stored in localStorage
- Quick-access bookmark bar below filter bar
- Export/import bookmarks as JSON

### Tests
- 10+ filter state management tests
- 6+ community detection tests (backend + frontend)
- 5+ keyboard navigation tests
- 4+ context menu tests
- 3+ bookmark persistence tests

---

## Phase 5: Temporal Views, Export & Visual Polish
**Duration:** 2 weeks  
**Goal:** Timeline scrubber, full export suite, annotations, and visual refinements.

### 5.1 Timeline Scrubber (3 days)
**Files:** `apps/web/src/kgr/TimelineScrubber.jsx` (new)

- Horizontal bar at bottom of temporal graph view
- Dual-handle range slider for selecting time window
- Histogram overlay showing entity/edge creation density over time
- Play/pause button for animated playback through time
- Speed control (1x, 2x, 5x, 10x)
- Entities outside the selected window fade to 10% opacity (not removed)
- Works with Temporal Graph type; available as overlay in other types

### 5.2 Export Suite (3 days)
**Files:** `apps/web/src/kgr/ExportMenu.jsx` (new)

- **PNG export**: Current graph canvas at 2x resolution
- **SVG export**: Vector export of graph (Cytoscape.js `cy.svg()`)
- **JSON-LD export**: Graph data in JSON-LD format with EOIP context
- **CSV export**: Separate nodes.csv and edges.csv files
- **Clipboard**: Copy selected node/edge as formatted Markdown
- **Context export**: Current lens context as reusable JSON (existing, move to menu)
- Export dialog with format selector, resolution options, scope (visible/all)

### 5.3 Annotation System (2 days)
**Files:** `apps/web/src/kgr/AnnotationPanel.jsx` (new)

- Text annotations on nodes (stored in localStorage keyed by canonical_id)
- Text annotations on edges (stored in localStorage keyed by edge_id)
- Annotation indicator icon on annotated nodes/edges
- Annotations tab in inspector for viewing/editing
- Annotations included in export reports
- Character limit: 500 per annotation

### 5.4 Semantic Zoom Enhancement (2 days)
**Files:** modify `apps/web/src/GraphCanvas.jsx`

- 3-level semantic zoom:
  - **Cluster level** (zoom < 0.3): Only cluster hulls and high-degree nodes visible
  - **Entity level** (zoom 0.3-0.8): All nodes visible, abbreviated labels
  - **Detail level** (zoom > 0.8): Full labels, edge labels, evidence indicators
- Smooth transitions between levels
- Node hover always shows full label tooltip regardless of zoom

### 5.5 Fisheye Distortion (1 day)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`

- Toggle-able fisheye mode from toolbar
- Magnifies area around cursor (2x magnification in center)
- Context preserved at edges (gradual distortion falloff)
- Implemented via CSS transform on cursor move

### 5.6 Edge Bundling (1 day)
**Files:** modify `apps/web/src/GraphCanvas.jsx`

- Force-directed edge bundling for highly connected nodes
- Toggle from toolbar settings
- Threshold: activate when any node has > 10 edges
- Bundled edges fan out at endpoints for readability

### 5.7 Color-Blind Safe Palette (1 day)
**Files:** modify `apps/web/src/GraphCanvas.jsx`, `apps/web/src/style.css`

- Alternative palette option for deuteranopia/protanopia
- Uses shape variations alongside color for double encoding
- Toggle in toolbar settings
- High contrast mode option

### Tests
- 6+ timeline scrubber interaction tests
- 8+ export format validation tests
- 4+ annotation CRUD tests
- 3+ semantic zoom level tests
- 2+ accessibility tests (color-blind, keyboard)

---

## Phase 6: Large-Graph Rendering & Performance
**Duration:** 1.5 weeks  
**Goal:** Scale visualization to 50K+ nodes using WebGL rendering and progressive loading.

### 6.1 Sigma.js Integration (3 days)
**Files:** `apps/web/src/kgr/renderers/SigmaRenderer.jsx` (new)

- Sigma.js v3 + graphology as the large-graph renderer
- Automatic switch: Cytoscape for < 5K nodes, Sigma for >= 5K nodes
- Shared interaction API (click, hover, select work identically)
- ForceAtlas2 layout running in Web Worker
- Level-of-detail rendering (labels at zoom thresholds)
- Node/edge program: custom WebGL shaders for EOIP entity types

### 6.2 Web Worker Layout Engine (2 days)
**Files:** `apps/web/src/kgr/renderers/LayoutWorker.js` (new)

- Offload layout computation for graphs > 500 nodes
- Support algorithms: ForceAtlas2, dagre, concentric, radial
- Message protocol: `{type: 'layout', nodes, edges, algorithm, options}` → `{type: 'positions', positions}`
- Progress reporting: `{type: 'progress', iteration, total}`
- Cancel support for layout interruption

### 6.3 Progressive Rendering (2 days)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`

- For results > 1K nodes:
  - Render first 200 nodes immediately (highest degree)
  - Add remaining nodes in batches of 100 with 50ms delay
  - Incremental layout adjustment (don't re-layout entire graph)
- Loading progress indicator
- "Show all" / "Show top N" toggle

### 6.4 Virtual Scrolling Entity Strip (1 day)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`

- Virtualized list for entity strip (only render visible rows)
- Smooth scroll with 10K+ items
- Fixed header with count and filter controls

### Tests
- Performance benchmarks: 1K, 5K, 10K, 50K node rendering times
- Memory usage tests (< 512MB for 10K nodes)
- Layout worker message protocol tests
- Progressive rendering correctness tests
- Renderer switching tests (Cytoscape ↔ Sigma)

---

## Phase 7: Real-Time Updates & WebSocket Integration
**Duration:** 1 week  
**Goal:** Live graph updates as ingestion events occur.

### 7.1 WebSocket Event Service (2 days)
**Files:** modify `apps/api/main.py`, `packages/eoip/events/` (new)

- `WS /ws/graph/events` endpoint
- Event types:
  - `vertex_upserted`: new/updated entity
  - `edge_upserted`: new/updated relationship
  - `vertex_deleted`: entity removed
  - `edge_deleted`: relationship removed
  - `ingestion_completed`: batch ingestion finished
  - `validation_completed`: validation run finished
- Event payload includes full entity/edge data
- Client-side reconnect with exponential backoff
- Polling fallback: `GET /api/v1/graph/events?since=<timestamp>` for environments without WebSocket

### 7.2 Incremental Graph Updates (2 days)
**Files:** modify `apps/web/src/kgr/KGRExplorer.jsx`

- WebSocket subscription on KGR lens activation
- New entities appear with animated fade-in
- Removed entities disappear with fade-out
- Incremental layout adjustment (only reposition affected neighborhood)
- Notification badge for off-screen changes
- "Jump to new" button to navigate to newly added entities

### 7.3 Event Feed Panel (1 day)
**Files:** `apps/web/src/kgr/EventFeed.jsx` (new)

- Collapsible panel showing real-time graph change events
- Clickable events navigate to the affected entity
- Filter by event type
- Pause/resume event stream

### Tests
- WebSocket connection/reconnection tests
- Incremental update correctness tests
- Event feed rendering tests

---

## Phase 8: Graph Comparison & Advanced Analytics
**Duration:** 1.5 weeks  
**Goal:** Diff visualization, what-if analysis, and graph health scoring.

### 8.1 Graph Diff View (3 days)
**Files:** `apps/web/src/kgr/GraphDiff.jsx` (new), modify `apps/api/app.py`

Backend:
- `POST /api/v1/graph/diff` accepts two snapshots (by timestamp or save ID)
- Returns added/removed/modified nodes and edges

Frontend:
- Side-by-side view with synchronized zoom/pan
- Overlay diff mode: green (added), red (removed), yellow (modified), gray (unchanged)
- Change list panel with sortable table
- Toggle between side-by-side and overlay modes

### 8.2 What-If Analysis View (2 days)
**Files:** modify `apps/web/src/kgr/BlastRadius.jsx`

- "Simulate removal" button in inspector
- Shows before/after comparison:
  - Broken paths count
  - Orphaned entities
  - New centrality scores for affected entities
- Risk summary: "Removing this entity would break N paths and orphan M entities"
- Undo/cancel simulation

### 8.3 Graph Health Dashboard (2 days)
**Files:** `apps/web/src/kgr/GraphHealth.jsx` (new)

- Aggregate quality scores displayed as dashboard widgets:
  - **Completeness**: % entities with all required properties
  - **Connectivity**: avg degree vs. expected per type
  - **Evidence coverage**: % edges backed by evidence
  - **Provenance depth**: avg hops to source-of-truth
  - **Freshness**: time since last ingestion per type
- Trend sparklines (comparing current to previous ingestion cycle)
- Accessible from both KGR and Admin sections

### 8.4 Statistics Endpoint (1 day)
**Files:** modify `apps/api/app.py`

- `GET /api/v1/graph/statistics` returns:
  - Node count, edge count, density
  - Connected components count
  - Average degree, max degree
  - Average path length (sampled for large graphs)
  - Graph diameter (sampled)

### Tests
- Graph diff correctness tests
- What-if simulation tests
- Health score computation tests
- Statistics endpoint tests

---

## Cross-Cutting Concerns (Applied Across All Phases)

### CSS Design System Extension
**File:** `apps/web/src/style.css`

New CSS classes for KGR components following the existing design system:
- `.kgr-explorer`, `.kgr-filter-bar`, `.kgr-inspector`
- `.blast-ring`, `.centrality-radar`
- `.graph-type-tab`, `.graph-type-tab.active`
- `.filter-chip`, `.filter-preset`
- `.minimap`, `.timeline-scrubber`
- `.context-menu`, `.context-menu-item`
- Dark mode support via existing `@media (prefers-color-scheme: dark)` pattern
- All existing CSS classes remain untouched

### Testing Strategy
- **Unit tests**: Every new component and utility function
- **Integration tests**: Lens switching, context sharing, API roundtrips
- **Performance tests**: Rendering benchmarks at 1K, 5K, 10K, 50K nodes
- **Accessibility tests**: Keyboard navigation, screen reader, color-blind modes
- **Regression**: All 123+ existing tests must pass after each phase
- **Target**: > 80% coverage on new code

### Documentation
- Each phase delivers a brief section in the demo playbook
- API endpoint documentation via FastAPI's built-in OpenAPI
- No separate doc files unless explicitly requested

---

## Phase Summary

| Phase | Duration | Key Deliverables | New Tests |
|-------|----------|-----------------|-----------|
| 1 | 2 weeks | Enhanced inspector, toolbar, minimap, schema API | ~31 |
| 2 | 2 weeks | 6 graph type views, KGR Explorer container | ~22 |
| 3 | 2 weeks | Blast radius, centrality, metrics engine | ~26 |
| 4 | 2 weeks | Filtering, community detection, keyboard nav, bookmarks | ~28 |
| 5 | 2 weeks | Timeline, export, annotations, visual polish | ~23 |
| 6 | 1.5 weeks | Sigma.js, Web Worker layouts, progressive rendering | ~12 |
| 7 | 1 week | WebSocket events, incremental updates | ~8 |
| 8 | 1.5 weeks | Graph diff, what-if, health dashboard | ~10 |
| **Total** | **~14 weeks** | **Complete KGR platform** | **~160** |

### Definition of Done (per phase)
1. All new components render correctly
2. All new API endpoints return valid responses
3. All new tests pass
4. All existing 123+ tests continue to pass
5. No new lint warnings
6. CSS follows existing design system tokens
7. No external network requests
8. Keyboard-accessible

### Dependencies Between Phases
- Phase 1 is the foundation; all subsequent phases depend on it
- Phases 2-4 can be partially parallelized
- Phase 5 depends on Phases 1-4 for visual polish context
- Phase 6 is independent (can start after Phase 1)
- Phase 7 depends on Phase 1 (graph canvas features)
- Phase 8 depends on Phase 3 (metrics engine)

---

## Research Sources Informing This Plan

This implementation plan is informed by comprehensive research across 7 deep-dive research streams:

1. **Graphify Competitive Analysis**: 85K+ stars, AST extraction via Tree-sitter, Leiden community detection, static graph.html visualization breaks at 5K nodes, no blast radius, no real-time updates — 10 exploitable gaps identified
2. **Knowledge Graph Types & Patterns**: 10 KG types researched (entity-relationship, code, infrastructure, document, ontology, provenance, impact, metadata, temporal, social) with entity/relationship models from Diffbot, Google KG, Kythe, Grafana, GraphRAG, OpenLineage, W3C PROV
3. **Graph Visualization Libraries**: 12 libraries compared (Cytoscape.js, D3, Sigma.js, vis-network, G6/Graphin, react-force-graph, Neo4j Bloom, Gephi, KeyLines, Graphistry, Ogma, yFiles) with performance limits, layout algorithms, and licensing
4. **Enterprise Ontology Patterns**: OWL/RDFS/SKOS standards, TOVE, ArchiMEO, TOGAF metamodel, ontology versioning, OOPS! pitfall validation
5. **Data Feed & Ingestion Patterns**: ETL/ELT/CDC/streaming, Lambda/Kappa architectures, entity resolution pipelines, confidence scoring, Netflix/Atlassian/Grafana production examples
6. **Graph Analysis Algorithms**: BFS/DFS blast radius, Leiden/Louvain community detection, PageRank/betweenness/closeness centrality, temporal KG reasoning, anomaly detection, cognitive load research
7. **Graph Exploration UX Patterns**: Neo4j Bloom expand/collapse, Linkurious search-to-explore, Gephi real-time layout tuning, Cambridge Intelligence graph UX design, IEEE TVCG 2024 KG practitioner study (3 personas: Builder, Analyst, Consumer)
