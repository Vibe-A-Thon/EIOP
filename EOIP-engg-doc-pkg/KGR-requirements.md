# KGR — Knowledge Graph Renderer & Explorer: Requirements Specification

**Version:** 1.0  
**Date:** 2026-10-02  
**Status:** Draft  
**Scope:** A "Graphify-class" (and beyond) knowledge graph visualization, exploration, and analysis application integrated into the EOIP platform.

---

## 1. Executive Summary

The Knowledge Graph Renderer (KGR) module elevates EOIP from a query-and-inspect tool into a **full-featured, interactive graph intelligence experience**. Inspired by—but designed to significantly surpass—applications like [Graphify](https://github.com/Graphify-Labs/graphify), KGR provides multi-graph visualization, deep node/edge inspection, impact & blast radius analysis, metadata graph rendering, enterprise ontology establishment views, and relationship intelligence.

### 1.1 Competitive Positioning vs. Graphify

| Capability | Graphify | KGR (EOIP) |
|---|---|---|
| Data sources | Neo4j only | HugeGraph, any GraphStore backend, file import, connectors |
| Graph types | Property graph only | Knowledge, relationship, metadata, ontology, temporal, provenance |
| Visualization | Basic node-link | Multi-layout, semantic zoom, lens-based, fisheye, minimap, timeline |
| Node inspection | Properties panel | Full entity inspector with evidence chain, provenance, impact analysis |
| Impact analysis | None | Blast radius, centrality metrics, dependency cascading, what-if |
| Metadata graphs | None | Schema meta-graph, ingestion lineage, validation topology |
| Enterprise ontology | None | OWL/RDFS-aligned ontology viewer, domain establishment, class hierarchy |
| Filtering | Basic label filter | Multi-dimensional: domain, relationship, trust, temporal, evidence |
| Layouts | Force-directed only | 8+ algorithms: force, hierarchy, radial, dagre, concentric, grid, circle, timeline |
| Export | PNG only | PNG, SVG, PDF, JSON-LD, GraphML, CSV, clipboard |
| Evidence | None | First-class evidence chain, provenance, source reference linking |
| Search | Text match | Semantic search, path finding, fuzzy match, faceted results |
| Collaboration | None | Context export, shared graph snapshots, annotation support |
| Scalability | <500 nodes | Progressive rendering, virtualization, up to 50K nodes |
| Local-first | Cloud-dependent | Fully local, no external dependencies |

---

## 2. Functional Requirements

### FR-KGR-001: Multi-Graph Type Rendering

The system SHALL render the following graph types from the same underlying data:

#### 2.1 Knowledge Graph (Primary)
- **Entity-centric view**: Nodes represent canonical entities (WorkItem, Commit, File, CodeSymbol, Document, Person, etc.)
- **Relationship rendering**: Directed edges with type labels, evidence status, and trust indicators
- **Domain coloring**: Automatic palette assignment per vertex label with legend
- **Evidence overlay**: Visual distinction between deterministic and inferred edges (solid vs. dashed)
- **Evidence thickness**: Edges backed by source references rendered thicker

#### 2.2 Relationship Graph
- **Edge-centric analysis**: Nodes are relationship types, edges connect types that share endpoints
- **Frequency encoding**: Node/edge size proportional to instance count
- **Relationship pattern discovery**: Highlight common traversal patterns
- **Co-occurrence matrix**: Heatmap view showing which entity types connect via which relationship types

#### 2.3 Metadata Graph
- **Schema topology**: Vertex labels as nodes, edge labels as connecting edges
- **Property schema overlay**: Show required/optional properties per label
- **Index coverage map**: Highlight which labels have search/range/secondary indexes
- **Ingestion lineage**: Source system → connector → ingestion run → entity creation flow
- **Validation topology**: ValidationRun → Finding → affected entity connections

#### 2.4 Enterprise Ontology Establishment Graph
- **Class hierarchy**: OWL/RDFS-style class tree with subclass relationships
- **Domain decomposition**: GraphDomain nodes connected to their member entity types
- **Property inheritance**: Show which properties are inherited vs. local
- **Ontology versioning**: Side-by-side diff view between ontology versions
- **Cardinality constraints**: Visual indicators for required/optional, single/multi-valued properties
- **Semantic alignment**: Map EOIP ontology to standard vocabularies (Dublin Core, SKOS, PROV-O)

#### 2.5 Temporal Graph
- **Time-windowed views**: Filter graph by creation/modification timestamps
- **Timeline scrubber**: Animated playback of graph evolution over time
- **Temporal edges**: Show when relationships were established and by what evidence
- **Change velocity**: Heat encoding showing which areas of the graph change most

#### 2.6 Provenance/Lineage Graph
- **Evidence chain visualization**: Full source → ingestion → canonicalization → entity chain
- **Cross-system tracing**: Highlight entities that span multiple source systems
- **Trust propagation**: Visual flow showing how evidence confidence propagates through the graph
- **Audit trail rendering**: IngestionRun and ValidationRun nodes with temporal context

### FR-KGR-002: Node & Vertex Intelligence

When a node is selected, the system SHALL display:

#### 2.2.1 Core Properties
- Canonical ID, display name, entity label/type
- All stored properties with type-aware formatting (timestamps, URLs, code references)
- Domain membership and ontology context
- Creation metadata (source system, ingestion run, timestamp)

#### 2.2.2 Relationship Summary
- Incoming edge count by type with expandable list
- Outgoing edge count by type with expandable list
- Bidirectional relationship detection
- Relationship strength/frequency indicators

#### 2.2.3 Impact Analysis
- **Blast radius**: N-hop downstream dependency count with depth breakdown
- **Reverse blast radius**: N-hop upstream dependency count (who depends on me?)
- **Centrality metrics**:
  - Degree centrality (direct connections)
  - Betweenness centrality (bridge nodes)
  - Closeness centrality (average distance to all others)
  - PageRank (importance in the graph)
- **Change propagation score**: Estimated percentage of graph affected if this entity changes
- **Risk classification**: High/Medium/Low based on centrality + blast radius

#### 2.2.4 Evidence Intelligence
- Direct evidence references (source_ref, evidence_key)
- Evidence chain depth (how many hops to nearest source-of-truth)
- Trust score based on evidence completeness
- Source system diversity (entities backed by multiple independent sources)

#### 2.2.5 Spread Analysis
- **Dependency cascade**: Animated visualization showing how changes propagate
- **Failure domain**: What breaks if this entity is removed
- **Similarity cluster**: Other entities with similar relationship patterns
- **Critical path membership**: Which requirement-to-delivery paths include this entity

### FR-KGR-003: Edge/Vertex Intelligence

When an edge is selected, the system SHALL display:

- Source and target entity summaries
- Edge type and semantic meaning from ontology
- All edge properties with formatting
- Evidence backing (source_ref, evidence_key, method)
- Creation status (DETERMINISTIC, INFERRED, MANUAL)
- Temporal context (when was this relationship established)
- Path context (which requirement-to-implementation paths use this edge)
- Parallel edges (other relationships between the same two entities)

### FR-KGR-004: Interactive Graph Exploration

#### 2.4.1 Navigation
- Click to select node/edge and populate inspector
- Double-click to expand neighborhood (bounded, configurable depth 1-3)
- Right-click context menu with actions: expand, collapse, hide, pin, trace impact, find paths
- Keyboard navigation: Tab through nodes, Enter to select, arrow keys to traverse edges
- Breadcrumb trail of exploration history with undo/redo

#### 2.4.2 Filtering & Faceting
- **Domain filter**: Show/hide by GraphDomain
- **Entity type filter**: Show/hide by vertex label (multi-select)
- **Relationship filter**: Show/hide by edge type (multi-select)
- **Trust filter**: Deterministic only / Inferred only / All
- **Evidence filter**: Evidenced only / Unevidenced only / All
- **Temporal filter**: Date range slider for entity/edge creation
- **Property filter**: Filter by property value (e.g., status = "SUCCEEDED")
- **Saved filter presets**: Store and recall named filter configurations

#### 2.4.3 Layout Algorithms
- **Force-directed (COSE)**: Default organic layout for general exploration
- **Hierarchical (Dagre)**: Top-down or left-right for dependency trees
- **Radial/Concentric**: Selected node at center, neighbors in concentric rings
- **Breadthfirst**: Tree-like expansion from a root node
- **Circle**: All nodes on a circle, good for small graphs
- **Grid**: Regular grid, useful for comparing similar entities
- **Timeline**: Nodes positioned on X-axis by timestamp
- **Clustered**: Group nodes by domain/type with force-directed within clusters

#### 2.4.4 Visual Intelligence
- **Semantic zoom**: Labels appear/disappear based on zoom level, detail on hover
- **Fisheye distortion**: Magnify area around cursor while maintaining context
- **Minimap**: Thumbnail overview of full graph with viewport indicator
- **Node sizing**: Configurable by degree, centrality, property value, or uniform
- **Edge bundling**: Reduce visual clutter for highly connected nodes
- **Cluster hulls**: Convex hull outlines around domain/type clusters
- **Heatmap overlay**: Color nodes by any numeric metric (centrality, age, evidence count)

### FR-KGR-005: Data Feed Integration

The KGR SHALL display data from the following feeds, with real-time update capability:

#### 2.5.1 Live Graph Feed
- WebSocket subscription to graph change events
- Real-time node/edge addition with animation
- Incremental layout adjustment (don't re-layout entire graph)

#### 2.5.2 Search Feed
- Full-text search with typeahead suggestions
- Faceted search results grouped by domain/type
- Search history with re-execution

#### 2.5.3 Query Feed
- Path finding between entities
- Impact traversal with configurable depth/breadth
- Neighborhood expansion
- Traceability chain
- Custom query plan execution

#### 2.5.4 Analytics Feed
- Graph-level statistics (node/edge counts, density, diameter, components)
- Domain-level statistics (entities per domain, cross-domain edges)
- Quality metrics (evidence coverage, provenance coverage, finding counts)
- Temporal statistics (ingestion rate, graph growth over time)

#### 2.5.5 Event Feed
- Ingestion job status changes
- Validation run results
- Agent execution results
- DLQ events

### FR-KGR-006: Graph Comparison & Diff

- **Snapshot comparison**: Compare graph state at two points in time
- **Diff visualization**: Added/removed/modified nodes and edges highlighted
- **Structural diff**: Changes in graph topology (new connections, broken paths)
- **Merge view**: Overlay two graph states with conflict highlighting

### FR-KGR-007: Export & Sharing

- **Image export**: PNG (raster) and SVG (vector) at configurable resolution
- **PDF report**: Graph image + node table + relationship summary + metrics
- **Data export**: JSON-LD, GraphML, CSV (nodes/edges separately), Gremlin script
- **Clipboard**: Copy selected node/edge details as formatted text
- **Context export**: Export current lens context as reusable JSON
- **Embeddable widget**: Standalone graph component for embedding in other tools
- **Print-optimized view**: Black-and-white layout suitable for documentation

### FR-KGR-008: Annotation & Collaboration

- **Node annotations**: Attach text notes to nodes (stored in localStorage initially)
- **Edge annotations**: Attach text notes to edges
- **Graph bookmarks**: Save named graph views (query + filters + layout + viewport)
- **Annotation export**: Include annotations in exported reports

---

## 3. Non-Functional Requirements

### NFR-KGR-001: Performance
- Graph rendering SHALL complete in < 2 seconds for up to 1,000 nodes and 5,000 edges
- Progressive rendering SHALL support up to 50,000 nodes with virtualization
- Layout computation SHALL be offloaded to a Web Worker for graphs > 500 nodes
- Interaction response (click, hover, zoom) SHALL remain < 100ms at all graph sizes
- Memory usage SHALL not exceed 512 MB for a 10,000-node graph

### NFR-KGR-002: Responsiveness
- Full functionality at desktop resolution (1280px+)
- Reduced but functional at tablet resolution (768px-1279px): single-column layout, simplified inspector
- Read-only at mobile resolution (< 768px): static graph image with tap-to-inspect

### NFR-KGR-003: Accessibility
- WCAG 2.1 AA compliance for all interactive controls
- Keyboard-navigable graph (Tab/Enter/Arrow keys)
- Screen reader descriptions for graph topology
- Color-blind safe palette option (deuteranopia, protanopia, tritanopia)
- High contrast mode

### NFR-KGR-004: Browser Support
- Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- No external runtime dependencies (everything bundled)
- Offline-capable after initial load

### NFR-KGR-005: Security
- No data leaves the browser except to the local API
- No external CDN dependencies in production (all libraries bundled)
- CSP-compatible (no inline eval, no external scripts)
- Token-based API authentication maintained for all data requests

---

## 4. Graph Data Model Requirements

### 4.1 Node Data Contract
```typescript
interface GraphNode {
  id: string;              // canonical_id
  label: string;           // vertex label (WorkItem, Commit, etc.)
  domain?: string;         // GraphDomain membership
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
  };
  visual?: {
    x?: number;
    y?: number;
    pinned?: boolean;
    hidden?: boolean;
    size?: number;
    annotation?: string;
  };
}
```

### 4.2 Edge Data Contract
```typescript
interface GraphEdge {
  id: string;
  type: string;            // edge label (IMPLEMENTS, MODIFIES, etc.)
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

### 4.3 Graph Result Contract (Extended)
```typescript
interface KGRGraphResult {
  nodes: GraphNode[];
  edges: GraphEdge[];
  paths: GraphPath[];
  evidence: EvidenceRef[];
  warnings: string[];
  partial: boolean;
  metrics?: {
    nodeCount: number;
    edgeCount: number;
    density: number;
    components: number;
    diameter: number;
    avgDegree: number;
    avgPathLength: number;
  };
  query?: {
    intent: string;
    anchors: string[];
    executionMs: number;
    bounded: boolean;
  };
}
```

---

## 5. API Requirements

### 5.1 New Endpoints Required

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/graph/metrics` | Compute centrality, PageRank, blast radius for a node set |
| POST | `/api/v1/graph/cluster` | Detect communities/clusters in a subgraph |
| POST | `/api/v1/graph/diff` | Compare two graph snapshots |
| GET | `/api/v1/graph/schema` | Return the meta-graph (labels, edge types, property schemas) |
| POST | `/api/v1/graph/shortest-paths` | All shortest paths between two nodes (not just one) |
| GET | `/api/v1/graph/statistics` | Graph-level aggregate statistics |
| POST | `/api/v1/graph/blast-radius` | Compute downstream impact count + affected entity list |
| POST | `/api/v1/graph/reverse-impact` | Compute upstream dependency count |
| POST | `/api/v1/graph/what-if` | Simulate entity removal and report broken paths |
| WS | `/ws/graph/events` | WebSocket for real-time graph change notifications |

### 5.2 Extended Existing Endpoints

| Endpoint | Extension |
|---|---|
| `/api/v1/search` | Add `include_metrics=true` to return centrality with results |
| `/api/v1/impact` | Add `include_blast_radius=true` to return blast radius counts |
| `/api/v1/neighborhood` | Add `depth` parameter support (1-3 hops) |
| `/api/v1/lineage` | Add `direction=upstream|downstream|both` parameter |

---

## 6. UI/UX Requirements

### 6.1 Layout Architecture

```
┌─────────────────────────────────────────────────────────┐
│ Sidebar │ Topbar with graph type selector + search      │
│         │───────────────────────────────────────────────│
│ Nav     │ Filter Bar (domain, type, relationship, time) │
│         │───────────────────────────────────────────────│
│ Domains │ ┌─────────────────────┐ ┌──────────────────┐ │
│         │ │                     │ │  Node Inspector   │ │
│ Graph   │ │  Graph Canvas       │ │  - Properties     │ │
│ Types   │ │  (Cytoscape.js)     │ │  - Relationships  │ │
│         │ │  + Minimap          │ │  - Impact         │ │
│ Filters │ │  + Toolbar          │ │  - Evidence       │ │
│         │ │  + Legend            │ │  - Metrics        │ │
│ Book-   │ │                     │ │  - Annotations    │ │
│ marks   │ └─────────────────────┘ └──────────────────┘ │
│         │ Entity Strip / Timeline                       │
│         │───────────────────────────────────────────────│
│ Status  │ Statistics Bar                                │
└─────────────────────────────────────────────────────────┘
```

### 6.2 Graph Type Selector
- Tab bar above the graph canvas allowing switching between:
  - Knowledge Graph (default)
  - Relationship Graph
  - Metadata Graph
  - Ontology Graph
  - Temporal Graph
  - Provenance Graph
- Smooth transition animation when switching graph types
- Each type retains its own filter and layout state

### 6.3 Inspector Tabs (Extended)
1. **Overview**: Properties, identity, domain
2. **Relationships**: In/out edges grouped by type
3. **Impact**: Blast radius, centrality, change propagation
4. **Evidence**: Source references, trust score, provenance chain
5. **History**: Temporal changes, ingestion runs that touched this entity
6. **Annotations**: User notes, bookmarks

### 6.4 Toolbar Controls
- Zoom in / Zoom out / Fit all / Reset view
- Layout selector dropdown
- Toggle labels / Toggle edge labels
- Toggle minimap / Toggle legend
- Filter summary chips (clickable to edit)
- Export menu (PNG, SVG, PDF, JSON)
- Fullscreen toggle
- Settings gear (node sizing, edge bundling, animation speed)

---

## 7. Analysis & Intelligence Requirements

### 7.1 Blast Radius Analysis
Given a selected entity:
1. Compute all entities reachable within N hops via outgoing edges
2. Group by depth (1-hop, 2-hop, 3-hop, ...)
3. Group by entity type at each depth
4. Compute affected path count (how many requirement-to-delivery paths pass through this entity)
5. Classify risk: HIGH (>20% of graph affected), MEDIUM (5-20%), LOW (<5%)
6. Visualize as concentric rings from the selected entity

### 7.2 Centrality Analysis
Compute and display:
- **Degree centrality**: Normalize by max possible degree
- **Betweenness centrality**: Fraction of shortest paths passing through this node
- **Closeness centrality**: Inverse of average shortest path to all reachable nodes
- **PageRank**: Iterative importance based on incoming link quality
- **Hub/Authority score**: HITS algorithm for identifying connectors vs. destinations
- Display as radar chart in the inspector's Impact tab

### 7.3 Community Detection
- **Louvain method**: Detect modular communities for cluster visualization
- **Label propagation**: Fast community detection for large graphs
- **Connected components**: Identify disconnected subgraphs
- Display cluster membership as hull overlays on the graph canvas

### 7.4 What-If Analysis
Given a hypothetical entity removal or modification:
1. Compute which paths break
2. Identify orphaned entities (no remaining connections)
3. Calculate new centrality scores for affected entities
4. Show before/after comparison

### 7.5 Graph Health Scoring
Compute aggregate quality scores:
- **Completeness**: Percentage of entities with all required properties
- **Connectivity**: Average degree vs. expected degree per type
- **Evidence coverage**: Percentage of edges backed by evidence
- **Provenance depth**: Average hops to a source-of-truth
- **Freshness**: Time since last ingestion update per entity type
- Display as dashboard widgets with trend indicators

---

## 8. Data Feed Requirements

### 8.1 Supported Data Sources (Graph Population)
The KGR module renders data that enters the graph through EOIP's existing ingestion pipeline:

| Source | Feed Type | Entities Created |
|---|---|---|
| Jira | JSON import / REST connector | WorkItem, Project, Person |
| GitLab | JSON import / REST connector | MergeRequest, PipelineRun, Repository, Branch |
| Git repositories | File system scan | Commit, File, CodeSymbol, Dependency |
| Confluence | REST connector | Document, DocumentSection |
| ServiceNow | REST connector | Document (knowledge articles) |
| Demo dataset | Built-in synthetic | All entity types |

### 8.2 Real-Time Updates
- Ingestion events pushed via WebSocket
- Graph canvas updates incrementally (add/remove nodes without full re-render)
- Animation for new entities appearing
- Notification badge for off-screen changes

---

## 9. Integration Requirements

### 9.1 EOIP Platform Integration
- Seamlessly embedded within the existing EOIP web application
- Shares authentication and API infrastructure
- Reuses existing GraphCanvas component as foundation
- Extends existing lens-based navigation
- Compatible with existing sidebar, topbar, and inspector components

### 9.2 MCP Tool Integration
- Graph views can be triggered from MCP tool results
- Entity IDs from MCP responses are clickable to open in KGR
- MCP `navigate_graph` tool opens KGR with specified context

### 9.3 VS Code Extension Integration
- Graph views embeddable in VS Code webview panels
- Code symbol selection in editor → highlight in graph
- Graph node click → open corresponding file in editor

---

## 10. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-01 | User can switch between 6 graph types and see appropriate visualization for each |
| AC-02 | Selecting a node shows properties, relationships, impact metrics, and evidence chain |
| AC-03 | Blast radius analysis renders concentric ring visualization with depth breakdown |
| AC-04 | Centrality metrics computed and displayed in radar chart format |
| AC-05 | 8+ layout algorithms available and switchable without data loss |
| AC-06 | Graph renders 1,000 nodes in under 2 seconds |
| AC-07 | Progressive rendering handles 50,000 nodes without browser crash |
| AC-08 | All existing EOIP lenses continue to function unchanged |
| AC-09 | Export produces valid PNG, SVG, and JSON-LD output |
| AC-10 | Filter state persists across graph type switches |
| AC-11 | Minimap, fisheye, and semantic zoom function correctly |
| AC-12 | Keyboard navigation allows full graph traversal without mouse |
| AC-13 | 123+ existing tests continue to pass |
| AC-14 | New components have > 80% test coverage |
| AC-15 | No external network requests in production mode |

---

## 11. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Large graph performance | Browser freeze, OOM | Progressive rendering, Web Worker layout, virtualization |
| Cytoscape.js limitations at scale | Sluggish interaction | Switch to WebGL renderer (Sigma.js) for >5K nodes |
| Centrality computation cost | Slow inspector | Precompute on server, cache in API response |
| Ontology graph complexity | Visual clutter | Collapsible hierarchy, semantic zoom, fisheye |
| WebSocket reliability | Stale graph views | Reconnect with full-state resync, polling fallback |

---

## 12. Glossary

| Term | Definition |
|---|---|
| Blast radius | Count of entities transitively reachable from a change source |
| Centrality | Graph-theoretic measure of a node's structural importance |
| Deterministic edge | Relationship established by parsing, not inference |
| Evidence chain | Sequence of provenance links from entity to source-of-truth |
| GraphDomain | High-level ontology grouping (DELIVERY, CODE, OPERATIONS, etc.) |
| KGR | Knowledge Graph Renderer — this module |
| Lens | A purpose-specific view over the same underlying graph data |
| Meta-graph | The graph's own schema represented as a graph |
| Provenance | The recorded origin and transformation history of a data item |
| Semantic zoom | Adjusting visible detail based on zoom level |
