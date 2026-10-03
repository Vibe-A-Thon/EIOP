# KGR — Knowledge Graph Renderer & Explorer: Requirements Specification

**Version:** 2.0  
**Date:** 2026-10-03  
**Status:** Final Draft  
**Scope:** A knowledge graph visualization, exploration, and analysis platform integrated into EOIP that surpasses Graphify, Neo4j Bloom, Linkurious, Gephi, Graphistry, yFiles, Sourcetrail, CodeSee, Sourcegraph, and every other tool in the category.

---

## 1. Executive Summary

The Knowledge Graph Renderer (KGR) module transforms EOIP from a query-and-inspect tool into the **most capable open, local-first graph intelligence platform available**. It combines the best features of every competitor while fixing every one of their documented weaknesses. Where Graphify breaks at 5K nodes, KGR handles 50K+. Where Neo4j Bloom locks you to Neo4j, KGR works with any GraphStore backend. Where yFiles costs €9,200+/year, KGR ships bundled with EOIP at zero additional cost. Where Gephi is desktop-only, KGR runs in the browser. Where Sourcegraph went closed-source, KGR stays local-first and open.

### 1.1 Competitive Positioning — Full Landscape

| Capability | Graphify | Neo4j Bloom | Linkurious | Gephi | Graphistry | yFiles | Sourcetrail | CodeSee | Sourcegraph | code2flow | **KGR (EOIP)** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Data sources | Neo4j only | Neo4j only | Neo4j, JanusGraph | File import | CSV, Parquet, Neo4j | Any (SDK) | C/C++/Java/Python | GitHub only | Multi-host | Files | **Any GraphStore, file import, 6+ connectors** |
| Max nodes (interactive) | ~5K | ~10K | ~10K | ~50K (desktop) | 8M (GPU) | ~5K (no optimization) | ~1K | ~1K | N/A (search) | ~500 | **50K+ (WebGL), 5K (Canvas)** |
| Graph types | Property only | Property only | Property only | Network only | Tabular→graph | Any (SDK) | Call graph only | Dependency only | N/A | Call graph only | **8 specialized types** |
| Layouts | Force only | 4 layouts | Force + hierarchical | ForceAtlas2 + 6 | Force only | 20+ (best) | Custom Qt | Auto | N/A | Graphviz | **12 algorithms** |
| Impact/blast radius | None | None | None | None | None | None | None | None | None | None | **BFS blast radius + reverse impact** |
| Centrality metrics | None | GDS required | None | 6 metrics | None | Basic | None | None | None | None | **8 centrality algorithms** |
| Community detection | Leiden | GDS required | None | Modularity | Clustering | None | None | None | None | None | **Leiden + Louvain + Label Propagation** |
| Evidence/provenance | Extracted/Inferred | None | None | None | None | None | None | None | None | None | **First-class evidence chain + trust propagation** |
| Enterprise ontology | None | None | None | None | None | None | None | None | None | None | **OWL/RDFS-aligned ontology viewer** |
| Node inspection | Properties panel | Properties + NL | Properties | Attributes | Tooltip | Custom | 3-panel (graph+code+search) | Map view | Code intel | None | **8-tab inspector with impact, evidence, similarity** |
| Filtering | Label filter | Perspective filter | Faceted | Partition | Histogram + time | Custom | None | None | Repo scope | None | **10-dimensional filtering + saved presets** |
| Search | Subgraph query | NL + Cypher | Typeahead faceted | None | Filter | None | Fuzzy symbol | NL queries | Regex + structural | None | **Semantic + path + fuzzy + NL-ready** |
| Export | graph.html, JSON | PNG, CSV | PNG, CSV, XLSX | PNG, SVG, PDF, GEXF | CSV, JSON, Parquet | PNG-PDF-SVG-VSDX | PNG | None | None | DOT, PNG, SVG | **PNG, SVG, PDF, JSON-LD, GraphML, CSV, clipboard** |
| Real-time updates | Git hooks | None | Alerting | None | Streaming | WebSocket | None | PR sync | Webhooks | None | **WebSocket + polling fallback** |
| Collaboration | None | Shared scenes | Case management | None | Shared URLs | Real-time collab | Bookmarks | Code tours | Notebooks (removed) | None | **Annotations + bookmarks + context export** |
| Accessibility | None | Basic | Basic | None | None | Basic | None | None | None | None | **WCAG 2.1 AA, keyboard nav, color-blind modes** |
| Pricing | Free (OSS) | $$$$ (Enterprise) | $$$$ (Enterprise) | Free (OSS) | $$$$ (GPU) | €9,200+/yr | Free (discontinued) | Sunset | $49-59/user/mo | Free (OSS) | **Bundled with EOIP, zero cost** |
| Local-first | Yes | No (server) | No (server) | Yes (desktop) | No (GPU server) | Yes (SDK) | Yes (desktop) | No (SaaS) | No (server/SaaS) | Yes (CLI) | **Yes — fully local, no cloud** |
| Status | Active (buggy) | Active | Active | Stagnant | Active | Active | Discontinued | Sunset | Closed-source | Maintained | **Active, integrated** |

### 1.2 Competitor Weaknesses → KGR Strengths

Every documented competitor weakness becomes a KGR design requirement:

| Competitor Weakness | Affected Tools | KGR Requirement |
|---|---|---|
| Breaks at 5K nodes | Graphify, Sourcetrail, yFiles | Progressive WebGL rendering to 50K+ |
| Requires GPU/server infrastructure | Graphistry | CPU-only, browser-native, no server dependency |
| Single database vendor lock-in | Neo4j Bloom, Linkurious | Backend-agnostic GraphStore interface |
| Expensive commercial license | yFiles (€9.2K), Linkurious, Bloom, Sourcegraph ($49/mo) | Bundled free with EOIP |
| Desktop-only, not web | Gephi, Sourcetrail, Cytoscape | Browser-first SPA, no install |
| Cloud/SaaS dependency | CodeSee, Sourcegraph, Graphistry | Local-first, no external calls |
| Limited language support | Sourcetrail (4 langs), code2flow (4 langs) | Language-agnostic entity graph |
| No blast radius / impact analysis | ALL competitors | First-class BFS blast radius with risk classification |
| No enterprise ontology view | ALL competitors | OWL/RDFS-aligned ontology establishment graph |
| No evidence/provenance chain | All except Graphify (partial) | Full evidence chain with trust propagation |
| AI assistants bypass graph | Graphify | Tight MCP integration, graph-first context |
| Graph freshness/staleness | Graphify | WebSocket real-time + incremental ingestion |
| Product discontinued/sunset | Sourcetrail, CodeSee | Integrated into active EOIP platform |
| Closed-source pivot | Sourcegraph | Local-first, no external dependency |
| Steep API learning curve | yFiles | Declarative component architecture |
| No undo/redo exploration | Graphify, code2flow | Exploration history with breadcrumb trail |
| Limited export formats | Graphify (HTML only), Neo4j Bloom (PNG) | 7+ export formats |
| No keyboard navigation | Graphify, Gephi, Graphistry | Full keyboard navigation, WCAG 2.1 AA |
| Poor mobile/responsive design | ALL desktop/server tools | Responsive down to 320px |
| No annotation/collaboration | Graphify, Gephi, code2flow | Annotations on nodes/edges + bookmarks |
| Call-graph-only visualization | Sourcetrail, code2flow | 8 specialized graph types |
| Crashes on large indexing | Sourcetrail (SQLite locks) | Bounded queries, no full-index required |
| Non-deterministic output | code2flow | Deterministic graph traversal with policy bounds |

---

## 2. Functional Requirements

### FR-KGR-001: Multi-Graph Type Rendering

The system SHALL render 8 graph types from the same underlying data, each with a purpose-built visualization. This surpasses every competitor (Graphify: 1 type, Neo4j Bloom: 1, Gephi: 1, yFiles: configurable but no built-in types).

#### 2.1 Knowledge Graph (Primary)
- Entity-centric view: nodes represent canonical entities (WorkItem, Commit, File, CodeSymbol, Document, Person, etc.)
- Directed edges with type labels, evidence status, and trust indicators
- Domain coloring with automatic palette assignment per vertex label
- Evidence overlay: solid (deterministic) vs. dashed (inferred) edges
- Evidence thickness: edges backed by source references rendered thicker
- Semantic zoom: labels appear/hide at zoom thresholds
- This is the default view, extending the existing Graph lens

#### 2.2 Relationship Graph
- Edge-centric analysis: relationship types become nodes, connected by shared endpoint types
- Node size proportional to edge instance count
- Co-occurrence matrix heatmap view (toggle between graph and matrix)
- Click a relationship-type node to show all instances
- Frequency-encoded bar chart per relationship type
- **Unique to KGR** — no competitor offers edge-centric analysis

#### 2.3 Metadata Graph
- Schema topology: vertex labels as nodes, edge labels as connecting edges
- Property schema overlay: show required/optional properties per label on hover
- Index coverage map: checkmarks for indexed labels, highlights for unindexed
- Instance count badges on each label node
- Data from `/api/v1/graph/schema` endpoint
- Ingestion lineage: source system → connector → ingestion run → entity creation flow
- Validation topology: ValidationRun → Finding → affected entity connections

#### 2.4 Enterprise Ontology Establishment Graph
- Class hierarchy tree layout: GraphDomain → vertex labels with domain grouping
- Property list per type from ontology manifest with cardinality indicators
- Ontology version display with schema version
- Semantic alignment: map EOIP ontology to standard vocabularies (Dublin Core, SKOS, PROV-O)
- Index coverage per type
- Uses hierarchical (breadthfirst) layout by default
- **Unique to KGR** — no competitor has ontology establishment views

#### 2.5 Temporal Graph
- Time-windowed filtering by creation/modification timestamps
- Timeline scrubber with dual-handle range slider and histogram overlay
- Animated playback of graph evolution with configurable speed (1x, 2x, 5x, 10x)
- Entities outside time window fade to 10% opacity (not removed)
- Change velocity heatmap: color nodes by recency of modification
- X-axis temporal positioning when timeline layout active

#### 2.6 Provenance/Lineage Graph
- Evidence chain visualization: source → ingestion → canonicalization → entity chain
- Cross-system tracing: highlight entities spanning multiple source systems
- Trust propagation: visual flow showing confidence propagation through graph
- IngestionRun and ValidationRun nodes prominently displayed with temporal context
- Audit trail rendering: connect validation findings to affected entities

#### 2.7 Impact/Dependency Graph
- Blast radius concentric ring view centered on selected entity
- Ring depth 1-8 hops with entity type breakdown per ring
- Risk classification: HIGH (>20%), MEDIUM (5-20%), LOW (<5%) with color coding
- Animated propagation mode: wave effect showing impact spreading
- Reverse impact view: upstream dependencies ("who depends on me?")
- What-if simulation: preview effects of entity removal
- **Unique to KGR** — no competitor offers integrated impact visualization

#### 2.8 Similarity/Cluster Graph
- Community detection overlay (Leiden algorithm) with convex hull clusters
- Cluster coloring mode from toolbar
- Click community hull to filter to that cluster
- Similarity edges between structurally similar nodes (Jaccard, Adamic-Adar)
- k-core decomposition visualization
- Degree distribution histogram overlay
- **Unique to KGR** — goes beyond Graphify's basic Leiden by adding visual cluster intelligence

### FR-KGR-002: Node Intelligence (8-Tab Inspector)

When a node is selected, the system SHALL display an 8-tab inspector. This surpasses every competitor's node inspection (Graphify: properties only, Neo4j Bloom: properties + NL, Sourcetrail: 3-panel, yFiles: custom required).

#### Tab 1: Overview
- Canonical ID, display name, entity label/type, domain membership
- All stored properties with type-aware formatting (timestamps as locale dates, URLs as links, code refs as monospace)
- Creation metadata: source system, ingestion run, timestamp
- Quick actions: expand neighborhood, trace lineage, compute blast radius

#### Tab 2: Relationships
- Incoming edge count by type with expandable list
- Outgoing edge count by type with expandable list
- Bidirectional relationship detection
- Relationship type distribution bar chart
- Click any edge to navigate to it
- Total degree, in-degree, out-degree prominently displayed

#### Tab 3: Impact
- **Blast radius summary**: N entities at M depth, risk level badge
- **Blast radius depth breakdown**: by-depth and by-type bar charts
- **Centrality radar chart** (SVG): 5 axes — degree, betweenness, closeness, PageRank, blast radius
- **Change propagation score**: percentage of graph affected
- **Reverse impact** (upstream): who depends on this entity
- "Explore Blast Radius" button opens concentric ring view
- "Run What-If" button simulates removal
- **Unique to KGR** — no competitor has integrated impact analysis in the inspector

#### Tab 4: Evidence
- Direct evidence references (source_ref, evidence_key, method)
- Evidence chain depth: hops to nearest source-of-truth
- Trust score based on evidence completeness
- Source system diversity: entities backed by multiple independent sources
- Evidence provenance graph (mini inline view)
- **Unique to KGR** — only Graphify has partial evidence (EXTRACTED/INFERRED), KGR goes much deeper

#### Tab 5: Similarity
- Top 10 structurally similar nodes (by Jaccard neighbor similarity)
- Common neighbor count and list
- Shared relationship patterns
- Community/cluster membership
- Link prediction score: likelihood of missing connections
- **Unique to KGR** — no competitor offers node similarity analysis

#### Tab 6: History
- Temporal changes when available (property modifications over ingestion runs)
- Ingestion runs that touched this entity with timestamps
- Modification timeline (sparkline)
- Source system origin trail

#### Tab 7: Annotations
- Text annotations stored in localStorage keyed by canonical_id
- Annotation indicator icon on annotated nodes in graph
- Character limit: 500 per annotation
- Annotations included in export reports

#### Tab 8: Raw
- Full JSON representation of the entity
- Copy to clipboard button
- Linked canonical IDs clickable to navigate

### FR-KGR-003: Edge Intelligence

When an edge is selected, the system SHALL display:
- Source and target entity summaries with mini-preview cards
- Edge type with semantic meaning from ontology manifest
- All edge properties with type-aware formatting
- Evidence backing: source_ref, evidence_key, method, creation_status badge
- Temporal context: when was this relationship established
- Path context: which known paths use this edge
- Parallel edges: other relationships between the same two entities
- Trust badge: DETERMINISTIC (green), INFERRED (amber), MANUAL (blue)

### FR-KGR-004: Interactive Graph Exploration

#### 2.4.1 Navigation
- Click to select node/edge and populate inspector
- Double-click to expand neighborhood (configurable depth 1-3)
- Right-click context menu (node): expand (1/2/3 hop), blast radius, find paths, trace lineage, hide, pin/unpin position, copy canonical ID, add annotation
- Right-click context menu (edge): inspect, show evidence, find parallel edges, hide edge type, copy details
- Right-click context menu (canvas): fit all, reset filters, export view, toggle minimap
- Keyboard navigation: Tab through nodes, Enter to select, Arrow keys to traverse edges, `E` expand, `I` toggle inspector, `F` toggle filters, `1-8` switch graph types, `Esc` deselect
- Exploration history breadcrumb with undo/redo (fixes Graphify's lack of undo)
- Focus mode: isolate selected node + N-hop neighborhood, dim everything else

#### 2.4.2 Filtering (10-Dimensional)
This surpasses every competitor's filtering (Graphify: label only, Neo4j Bloom: perspective, Gephi: partition, Linkurious: faceted).

1. **Domain filter**: Multi-select dropdown of GraphDomains
2. **Entity type filter**: Checkbox list of vertex labels with live counts
3. **Relationship filter**: Checkbox list of edge types with live counts
4. **Trust filter**: Deterministic / Inferred / Manual / All (radio)
5. **Evidence filter**: Evidenced / Unevidenced / All (radio)
6. **Temporal filter**: Date range slider for entity/edge creation
7. **Property filter**: Key-value filter builder (property operator value)
8. **Centrality filter**: Min/max degree threshold slider
9. **Community filter**: Show/hide by detected cluster
10. **Search-within-view**: text filter on visible graph without new API call

- Active filter chips with click-to-remove
- Filter state persists across graph type switches
- Saved filter presets in localStorage with named configurations
- "Reset all filters" button

#### 2.4.3 Layout Algorithms (12)
This surpasses yFiles (20 but €9.2K), Gephi (7), and every free tool.

1. **Force-directed (COSE)**: Default organic layout
2. **Hierarchical (Dagre)**: Top-down or left-right for dependency trees
3. **Breadthfirst**: Tree-like expansion from root node
4. **Circle**: All nodes on a circle
5. **Grid**: Regular grid for comparing entities
6. **Concentric**: Selected node at center, neighbors in rings
7. **Radial**: Radial tree from selected root
8. **Cola (constraint-based)**: Constraint layout for aligned groupings
9. **Euler (force with edge-length preservation)**: Physics simulation
10. **Spread**: Even distribution across canvas
11. **Timeline**: Nodes on X-axis by timestamp
12. **Clustered**: Group by domain/type with force-directed within clusters

- Animated transitions between layouts (200ms)
- Layout computation in Web Worker for graphs > 500 nodes
- Pin individual node positions across layout changes

#### 2.4.4 Visual Intelligence
- **Semantic zoom** (3 levels): cluster (zoom <0.3), entity (0.3-0.8), detail (>0.8)
- **Fisheye distortion**: toggleable 2x magnification at cursor position
- **Minimap**: thumbnail overview (200×150px) with viewport indicator and click-to-navigate
- **Node sizing**: configurable by degree, centrality, property value, or uniform
- **Edge bundling**: force-directed bundling for nodes with >10 edges
- **Cluster hulls**: convex hull outlines around domain/type clusters
- **Heatmap overlay**: color nodes by any numeric metric
- **Path highlighting**: highlight shortest paths between entities
- **Focus + context**: selected entity and N-hop neighborhood at full opacity, rest dimmed

### FR-KGR-005: Data Feed Integration

#### 2.5.1 Live Graph Feed
- WebSocket subscription to graph change events (`WS /ws/graph/events`)
- Event types: vertex_upserted, edge_upserted, vertex_deleted, edge_deleted, ingestion_completed, validation_completed
- Real-time node/edge addition with fade-in animation
- Incremental layout adjustment (pin existing, only layout new nodes)
- Notification badge for off-screen changes
- Polling fallback: `GET /api/v1/graph/events?since=<timestamp>`
- Reconnect with exponential backoff (fixes Graphistry's WebSocket reliability issues)

#### 2.5.2 Search Feed
- Full-text search with typeahead suggestions from recent entities
- Faceted search results grouped by domain AND type
- Search history with re-execution
- "Search within current view" (filter existing graph, no API call)
- Quick filters from suggestions: "Show all WorkItems", "Show all Files"

#### 2.5.3 Query Feed
- Path finding between entities (all shortest paths, not just one — fixes code2flow's single-path limitation)
- Impact traversal with configurable depth/breadth
- Neighborhood expansion (1-3 hops)
- Traceability chain
- Custom QueryPlan execution

#### 2.5.4 Analytics Feed
- Graph-level statistics: node/edge counts, density, diameter, clustering coefficient, connected components
- Domain-level statistics: entities per domain, cross-domain edge counts
- Quality metrics: evidence coverage, provenance coverage, finding counts
- Temporal statistics: ingestion rate, graph growth over time
- Degree distribution histogram

#### 2.5.5 Event Feed Panel
- Collapsible panel showing real-time graph change events
- Clickable events navigate to affected entity
- Filter by event type
- Pause/resume event stream

### FR-KGR-006: Graph Comparison & Diff

- Snapshot comparison: compare graph state at two points in time
- Diff visualization: added (green), removed (red), modified (yellow), unchanged (gray)
- Side-by-side view with synchronized zoom/pan
- Overlay diff mode (toggle between side-by-side and overlay)
- Change list panel with sortable table
- Structural diff: changes in topology (new connections, broken paths)
- **Unique to KGR** — only yFiles has basic diff; KGR adds structural analysis

### FR-KGR-007: Export & Sharing (7+ Formats)

This surpasses every competitor's export (Graphify: HTML/JSON, Gephi: PNG/SVG/PDF/GEXF, yFiles: PNG-PDF-SVG-VSDX but €9.2K, Graphistry: CSV/JSON/Parquet).

- **PNG export**: current canvas at 2x resolution
- **SVG export**: vector graph via `cy.svg()`
- **PDF report**: graph image + node table + relationship summary + metrics
- **JSON-LD export**: graph data with EOIP ontology context
- **GraphML export**: standard graph interchange format
- **CSV export**: separate nodes.csv and edges.csv files
- **Clipboard**: copy selected node/edge as formatted Markdown
- **Context export**: current lens context as reusable JSON
- Export dialog with format selector, resolution options, scope (visible/all)

### FR-KGR-008: Annotation & Collaboration

- Node annotations: text notes stored in localStorage keyed by canonical_id
- Edge annotations: text notes keyed by edge_id
- Annotation indicator icon on annotated nodes/edges in graph
- Graph bookmarks: save named views (query + filters + graph type + layout + viewport)
- Quick-access bookmark bar below filter bar
- Export/import bookmarks as JSON
- Annotation export: include in PDF/JSON reports
- Character limit: 500 per annotation

### FR-KGR-009: AI-Assisted Exploration (Future-Ready)

- Natural language graph queries via MCP integration (query → QueryPlan conversion)
- "Explain this cluster" summarization via local LLM
- Auto-suggested interesting paths based on graph structure
- Anomaly highlighting: nodes with unusual degree patterns
- Recommended next expansions based on current exploration context
- **Surpasses** Neo4j Bloom's NL queries by using local-first LLM (no cloud)

---

## 3. Non-Functional Requirements

### NFR-KGR-001: Performance
- Graph rendering SHALL complete in < 2 seconds for up to 1,000 nodes and 5,000 edges (matches yFiles, beats Gephi)
- Progressive WebGL rendering SHALL support up to 50,000 nodes (beats Graphify 5K limit by 10x)
- Layout computation SHALL use Web Worker for graphs > 500 nodes (prevents UI blocking — fixes Sourcetrail's hang issue)
- Interaction response (click, hover, zoom) SHALL remain < 100ms at all sizes
- Memory usage SHALL not exceed 512 MB for 10,000 nodes (beats Graphistry's 537MB for 10M edges)
- Blast radius computation SHALL complete in < 2 seconds for 1,000 nodes
- Centrality computation SHALL complete in < 5 seconds for 5,000 nodes

### NFR-KGR-002: Responsiveness
- Full functionality at desktop (1280px+)
- Reduced but functional at tablet (768px-1279px): single-column, simplified inspector
- Read-only at mobile (< 768px): static graph image with tap-to-inspect

### NFR-KGR-003: Accessibility
- WCAG 2.1 AA for all interactive controls (no competitor achieves this)
- Keyboard-navigable graph: Tab/Enter/Arrow keys/shortcuts
- Screen reader descriptions for graph topology
- Color-blind safe palette (deuteranopia, protanopia, tritanopia)
- High contrast mode
- Focus ring styling on all interactive elements

### NFR-KGR-004: Browser Support
- Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- No external runtime dependencies (everything bundled — fixes Graphistry's server dependency)
- Offline-capable after initial load
- No eval() or inline scripts (CSP-compatible)

### NFR-KGR-005: Security
- No data leaves the browser except to the local API
- No external CDN dependencies in production
- Token-based API authentication for all data requests
- No telemetry (fixes Sourcegraph's data collection concerns)
- Annotations stored only in localStorage (never sent to API)

---

## 4. Graph Data Model

### 4.1 Node Data Contract
```typescript
interface GraphNode {
  id: string;              // canonical_id
  label: string;           // vertex label
  domain?: string;         // GraphDomain
  properties: Record<string, unknown>;
  metrics?: {
    degree: number;
    inDegree: number;
    outDegree: number;
    betweenness?: number;
    closeness?: number;
    pageRank?: number;
    blastRadius?: number;
    evidenceDepth?: number;
    clusterMembership?: number;
    kCoreNumber?: number;
  };
  visual?: {
    x?: number;  y?: number;
    pinned?: boolean;  hidden?: boolean;
    size?: number;  annotation?: string;
  };
}
```

### 4.2 Edge Data Contract
```typescript
interface GraphEdge {
  id: string;
  type: string;            // edge label
  from_id: string;
  to_id: string;
  properties: Record<string, unknown>;
  creation_status?: 'DETERMINISTIC' | 'INFERRED' | 'MANUAL';
  evidence?: {
    source_ref?: string;
    evidence_key?: string;
    method?: string;
  };
  temporal?: {
    created_at?: string;
    valid_from?: string;
    valid_to?: string;
  };
}
```

### 4.3 Blast Radius Result Contract
```typescript
interface BlastRadiusResult {
  target_id: string;
  total_affected: number;
  by_depth: Record<number, number>;   // {1: 5, 2: 12, 3: 8}
  by_type: Record<string, number>;     // {"File": 3, "Commit": 2}
  risk: 'HIGH' | 'MEDIUM' | 'LOW' | 'NONE';
  affected_ids: string[];
}
```

### 4.4 Centrality Metrics Contract
```typescript
interface CentralityMetrics {
  canonical_id: string;
  degree: number;
  in_degree: number;
  out_degree: number;
  betweenness: number;   // 0.0-1.0
  closeness: number;     // 0.0-1.0
  page_rank: number;     // 0.0-1.0
}
```

---

## 5. API Requirements

### 5.1 Endpoints (Implemented)

| Method | Path | Description | Status |
|---|---|---|---|
| POST | `/api/v1/graph/blast-radius` | BFS downstream impact with depth/type breakdown | **Done** |
| POST | `/api/v1/graph/reverse-impact` | BFS upstream dependencies | **Done** |
| POST | `/api/v1/graph/metrics` | Centrality metrics for node set | **Done** |
| GET | `/api/v1/graph/schema` | Full ontology meta-graph | **Done** |
| GET | `/api/v1/graph/statistics` | Aggregate graph statistics | **Done** |

### 5.2 Endpoints (Planned)

| Method | Path | Description | Phase |
|---|---|---|---|
| POST | `/api/v1/graph/cluster` | Leiden community detection | 4 |
| POST | `/api/v1/graph/diff` | Compare two graph snapshots | 8 |
| POST | `/api/v1/graph/what-if` | Simulate entity removal | 8 |
| POST | `/api/v1/graph/similarity` | Jaccard/Adamic-Adar similarity between nodes | 5 |
| POST | `/api/v1/graph/shortest-paths` | All shortest paths (not just one) | 4 |
| GET | `/api/v1/graph/events` | Polling fallback for real-time events | 7 |
| WS | `/ws/graph/events` | WebSocket for real-time graph changes | 7 |
| POST | `/api/v1/graph/k-core` | k-core decomposition | 6 |
| POST | `/api/v1/graph/link-prediction` | Predict missing edges | 6 |

### 5.3 Request/Response Contracts

```python
# Blast Radius
class BlastRadiusRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    max_depth: int = Field(default=4, ge=1, le=8)

# Response: BlastRadiusResult (see 4.3)

# Centrality Metrics
class MetricsRequest(BaseModel):
    canonical_ids: list[str] = Field(min_length=1, max_length=50)

# Response: dict[canonical_id, CentralityMetrics]

# Community Detection
class ClusterRequest(BaseModel):
    canonical_ids: list[str] | None = None  # None = entire graph
    resolution: float = Field(default=1.0, ge=0.1, le=10.0)
    algorithm: str = Field(default="leiden", pattern="^(leiden|louvain|label_propagation)$")

# Response: {communities: [{id, members: [canonical_id], size}], modularity: float}

# What-If Simulation
class WhatIfRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    action: str = Field(default="remove", pattern="^(remove|isolate)$")

# Response: {broken_paths: int, orphaned_entities: int, affected_centrality: dict}

# Similarity
class SimilarityRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    algorithm: str = Field(default="jaccard", pattern="^(jaccard|adamic_adar|common_neighbors)$")
    limit: int = Field(default=10, ge=1, le=50)

# Response: [{canonical_id, score, common_neighbors}]
```

---

## 6. UI/UX Layout

```
┌──────────────────────────────────────────────────────────────────┐
│ Sidebar │ Topbar (breadcrumb + service status + actions)         │
│         │────────────────────────────────────────────────────────│
│ Nav     │ Graph Type Selector (8 tabs)                           │
│         │ Filter Bar (10 dimensions + chips + presets)            │
│ Domains │────────────────────────────────────────────────────────│
│         │ ┌──────────────────────────┐ ┌──────────────────────┐  │
│ Graph   │ │  Graph Canvas            │ │  8-Tab Inspector     │  │
│ Types   │ │  (Cytoscape / Sigma)     │ │  Overview            │  │
│         │ │                          │ │  Relationships       │  │
│ Filters │ │  [Toolbar]  [Minimap]    │ │  Impact              │  │
│         │ │  [Legend]                │ │  Evidence            │  │
│ Book-   │ │                          │ │  Similarity          │  │
│ marks   │ │                          │ │  History             │  │
│         │ │                          │ │  Annotations         │  │
│ Status  │ └──────────────────────────┘ │  Raw                 │  │
│         │ Entity Strip / Timeline      └──────────────────────┘  │
│         │ Event Feed (collapsible)                               │
│         │────────────────────────────────────────────────────────│
│         │ Statistics Bar (graph-level metrics)                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## 7. Analysis & Intelligence Requirements

### 7.1 Blast Radius (Implemented)
- BFS from target along outgoing edges, collect at each depth
- Group by depth (1-hop through 8-hop) and by entity type
- Risk classification: HIGH (>20%), MEDIUM (5-20%), LOW (<5%)
- Concentric ring visualization with animated propagation

### 7.2 Reverse Impact (Implemented)
- BFS from target along incoming edges (upstream traversal)
- Same depth/type grouping and risk classification as blast radius

### 7.3 Centrality Analysis (Implemented — degree; planned — full suite)
- **Degree centrality**: in/out/total (implemented)
- **Betweenness centrality**: fraction of shortest paths (planned, Phase 3)
- **Closeness centrality**: inverse of avg shortest path (planned, Phase 3)
- **PageRank**: iterative, 20 iterations, damping=0.85 (planned, Phase 3)
- **Eigenvector centrality**: influence via neighbor importance (planned, Phase 6)
- **Katz centrality**: attenuated walk-based (planned, Phase 6)
- **HITS hub/authority**: bipartite influence (planned, Phase 6)
- **Harmonic centrality**: handles disconnected graphs (planned, Phase 6)
- Display as radar chart in Impact tab

### 7.4 Community Detection (Planned — Phase 4)
- **Leiden algorithm**: current gold standard, guarantees connected communities
- **Louvain**: modularity optimization, fast
- **Label Propagation**: near-linear time for very large graphs
- Visual: convex hull overlays on graph canvas with cluster coloring

### 7.5 Similarity Analysis (Planned — Phase 5)
- **Jaccard similarity**: neighbor overlap
- **Adamic-Adar**: weighted common neighbors biased toward low-degree bridges
- **Common neighbors**: simplest predictor
- **Link prediction**: predict likely missing edges based on structural similarity

### 7.6 Graph Statistics (Implemented)
- Vertex count, edge count, density
- Vertex/edge label counts
- Connected components (planned Phase 6)
- Clustering coefficient (planned Phase 6)
- Degree distribution (planned Phase 6)
- k-core decomposition (planned Phase 6)

### 7.7 What-If Analysis (Planned — Phase 8)
- Simulate entity removal: compute broken paths, orphaned entities
- New centrality scores for affected entities
- Before/after comparison view
- Risk summary text generation

### 7.8 Anomaly Detection (Planned — Phase 8)
- Outlier nodes by z-score on centrality distributions
- Sudden degree spikes (temporal anomaly)
- Missing expected edges (link prediction gap)
- Dense subgraph detection (unexpected clusters)

---

## 8. Acceptance Criteria

| ID | Criterion | Competitor Gap Addressed |
|---|---|---|
| AC-01 | User can switch between 8 graph types with appropriate visualization | Graphify: 1 type, Bloom: 1, Gephi: 1 |
| AC-02 | 8-tab inspector shows properties, relationships, impact, evidence, similarity, history, annotations, raw | Graphify: properties only |
| AC-03 | Blast radius renders concentric rings with depth/type breakdown and risk | No competitor has this |
| AC-04 | Centrality metrics computed and displayed as radar chart | Gephi: desktop only, Bloom: GDS required |
| AC-05 | 12 layout algorithms available and switchable without data loss | Graphify: 1, code2flow: 1 |
| AC-06 | Graph renders 1,000 nodes in < 2 seconds | Sourcetrail: crashes, code2flow: cluttered |
| AC-07 | Progressive WebGL rendering handles 50,000 nodes | Graphify: 5K limit |
| AC-08 | All existing EOIP lenses continue unchanged | N/A |
| AC-09 | Export produces valid PNG, SVG, PDF, JSON-LD, GraphML, CSV | Graphify: HTML only |
| AC-10 | 10-dimensional filter state persists across graph type switches | Graphify: label only |
| AC-11 | Minimap, fisheye, semantic zoom all function | No competitor bundles all three |
| AC-12 | Full keyboard navigation without mouse | No competitor achieves full keyboard nav |
| AC-13 | 166+ existing tests continue to pass | N/A |
| AC-14 | New components have > 80% test coverage | N/A |
| AC-15 | No external network requests in production | Fixes Sourcegraph, CodeSee, Graphistry |
| AC-16 | Community detection clusters visible as hull overlays | Gephi: desktop only |
| AC-17 | WebSocket real-time updates with fade-in animation | Graphify: git hooks only |
| AC-18 | Graph diff shows added/removed/modified entities | No free competitor has this |
| AC-19 | What-if simulation shows impact of entity removal | No competitor has this |
| AC-20 | Annotations on nodes/edges persist and export with reports | No free competitor has this |

---

## 9. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Large graph performance | Browser freeze, OOM | Progressive WebGL rendering, Web Worker layout, virtualization |
| Cytoscape.js limits at scale | Sluggish > 5K | Switch to Sigma.js (WebGL) for > 5K nodes |
| Centrality computation cost | Slow inspector | Server-side computation, cached in API response |
| Ontology graph complexity | Visual clutter | Collapsible hierarchy, semantic zoom, fisheye |
| WebSocket reliability | Stale graph | Reconnect with backoff, polling fallback |
| Community detection cost | Slow clustering | Precompute on server, cache results |
| Layout quality vs speed | Poor layouts | Multiple algorithms, user-selectable quality/speed |

---

## 10. Glossary

| Term | Definition |
|---|---|
| Blast radius | Count of entities transitively reachable from a change source via outgoing edges |
| Centrality | Graph-theoretic measure of a node's structural importance |
| Community | A group of densely connected nodes detected by algorithms like Leiden |
| Deterministic edge | Relationship established by parsing, not inference |
| Evidence chain | Sequence of provenance links from entity to source-of-truth |
| GraphDomain | High-level ontology grouping (META, WORK, CODE, CICD, KNOWLEDGE, IDENTITY, AGENT) |
| KGR | Knowledge Graph Renderer — this module |
| k-core | Maximal subgraph where every node has at least k neighbors within it |
| Leiden algorithm | State-of-the-art community detection guaranteeing connected communities |
| Lens | A purpose-specific view over the same underlying graph data |
| Meta-graph | The graph's own schema represented as a graph |
| Provenance | The recorded origin and transformation history of a data item |
| Semantic zoom | Adjusting visible detail based on zoom level |
| Trust propagation | How evidence confidence flows through the graph along edges |
| What-if analysis | Simulating the effect of adding/removing an entity on the graph structure |
