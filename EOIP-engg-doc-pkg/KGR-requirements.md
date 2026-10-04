# KGR — Knowledge Graph Renderer & Explorer: Requirements Specification

**Version:** 4.0  
**Date:** 2026-10-04  
**Status:** Final Draft (Revised — competitive gap audit + RAG/Agent/Engineering patterns)  
**Scope:** A knowledge graph visualization, exploration, and analysis platform integrated into EOIP that surpasses Graphify, Neo4j Bloom, Linkurious, Gephi, Graphistry, yFiles, Sourcetrail, CodeSee, Sourcegraph, and every other tool in the category.

---

## 1. Executive Summary

The Knowledge Graph Renderer (KGR) module transforms EOIP from a query-and-inspect tool into the **most capable open, local-first graph intelligence platform available**. It combines the best features of every competitor while fixing every one of their documented weaknesses. Where Graphify breaks at 5K nodes, KGR handles 50K+. Where Neo4j Bloom locks you to Neo4j, KGR works with any GraphStore backend. Where yFiles costs €9,200+/year, KGR ships bundled with EOIP at zero additional cost. Where Gephi is desktop-only, KGR runs in the browser. Where Sourcegraph went closed-source, KGR stays local-first and open.

### 1.1 Competitive Positioning — Full Landscape

| Capability | Graphify | Neo4j Bloom | Linkurious | Gephi | Graphistry | yFiles | Sourcetrail | CodeSee | Sourcegraph | code2flow | **KGR (EOIP)** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Data sources | Self-contained (NetworkX + tree-sitter AST, 37+ langs) | Neo4j only | Neo4j, Cosmos DB, Neptune, Memgraph, Spanner | File import | CSV, Parquet, Neo4j | Any (SDK) | C/C++/Java/Python | GitHub only | Multi-host | Files | **Any GraphStore, file import, 6+ connectors** |
| Max nodes (interactive) | ~5K | ~10K | ~10K | ~50K (desktop) | 8M (GPU) | ~5K (no optimization) | ~1K | ~1K | N/A (search) | ~500 | **50K+ (WebGL), 5K (Canvas)** |
| Graph types | Property only | Property only | Property only | Network only | Tabular→graph | Any (SDK) | Call graph only | Dependency only | N/A | Call graph only | **10 specialized types** |
| Layouts | Force only | 4 layouts | Force + hierarchical | ForceAtlas2 + 6 | Force only | 20+ (best) | Custom Qt | Auto | N/A | Graphviz | **12 algorithms** |
| Impact/blast radius | None | None | None | None | None | None | None | None | None | None | **BFS blast radius + reverse impact** |
| Centrality metrics | None | GDS required | None | 6 metrics | None | Basic | None | None | None | None | **8 centrality algorithms** |
| Community detection | Leiden | GDS required | None | Modularity | Clustering | None | None | None | None | None | **Leiden + Louvain + Label Propagation** |
| Evidence/provenance | Extracted/Inferred/Ambiguous | None | None | None | None | None | None | None | None | None | **First-class evidence chain + trust propagation + AMBIGUOUS status** |
| Enterprise ontology | None | None | None | None | None | None | None | None | None | None | **OWL/RDFS-aligned ontology viewer** |
| Node inspection | Properties panel | Properties + NL | Properties | Attributes | Tooltip | Custom | 3-panel (graph+code+search) | Map view | Code intel | None | **8-tab inspector with impact, evidence, similarity** |
| Filtering | Label filter | Perspective filter | Faceted | Partition | Histogram + time | Custom | None | None | Repo scope | None | **10-dimensional filtering + saved presets** |
| Search | Subgraph query | NL + Cypher | Typeahead faceted | None | Filter | None | Fuzzy symbol | NL queries | Regex + structural | None | **Semantic + path + fuzzy + NL-ready** |
| Export | graph.html, JSON, GraphML, SVG, Obsidian vault, Mermaid, Cypher | PNG, CSV | PNG, CSV, XLSX | PNG, SVG, PDF, GEXF | CSV, JSON, Parquet | PNG-PDF-SVG-VSDX | PNG | None | None | DOT, PNG, SVG | **PNG, SVG, PDF, JSON-LD, GraphML, CSV, GEXF, Obsidian, Mermaid, Cypher, clipboard** |
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
| No node group collapsing / declutter | Graphify, Gephi, code2flow | Node group collapsing with combo nodes |
| No geo-mode / geographic positioning | Graphify, Gephi, Sourcetrail, code2flow | Geo-mode when entities have location metadata |
| No code + graph side-by-side view | Graphify, Gephi, Graphistry, code2flow | Synchronized code viewer + graph panel (Sourcetrail-inspired) |
| No visual query builder | Graphify, Gephi, code2flow, Sourcetrail | No-code visual query builder for non-technical users |
| No dead code / orphaned entity detection | Graphify, Neo4j Bloom, Gephi | Orphaned entity detection + dead code highlighting |
| No community auto-labeling | Neo4j Bloom, Gephi, Graphistry | Automated community naming from dominant entity types |
| No PR/change conflict detection | Neo4j Bloom, Gephi, Sourcetrail | PR dashboard with community-based conflict detection |
| Ollama backend drops 96% of edges | Graphify | No LLM dependency for graph construction — deterministic AST + API extraction |
| Watch mode has unbounded O(n) state | Graphify | Bounded event buffer with ring-buffer eviction |
| 10K node display limit | Neo4j Bloom | Progressive WebGL rendering to 50K+ |
| Performance collapses at 384K nodes | Gephi | Progressive rendering with virtualization |
| Edge types immutable after creation | Linkurious | Schema-driven mutable edge types via ontology manifest |
| No subgraph extraction with depth | Graphify, Neo4j Bloom | Configurable neighborhood expansion (1-8 hops) with depth control |
| No self-contained interactive export | Neo4j Bloom, Gephi, Linkurious | Self-contained graph.html with search, filter, inspect |
| No automated graph report | Neo4j Bloom, Gephi, Linkurious, yFiles | 7-section Markdown report with centrality + health + recommendations |
| No hub exclusion with visual indicator | Neo4j Bloom, Gephi | Degree-based hub exclusion with dimmed silhouette |
| No surprising connection detection | Neo4j Bloom, Gephi, Linkurious | Structural surprise scoring + unexpected absence detection |
| No rule-based conditional styling (free) | Graphify, Gephi, code2flow | Composable IF/THEN visual rules, exportable JSON |
| No lasso/rectangle selection (free) | Graphify, Gephi, Sourcetrail | Shift+drag lasso, Ctrl+Shift+drag rectangle |
| No URL deep linking for graph state | Graphify, Gephi, code2flow | Full state encoded in URL hash |
| No accessible table view alternative | ALL competitors | WCAG-compliant sortable/filterable table view |
| No investigation playbooks (free) | Graphify, Neo4j Bloom, Gephi | Built-in + custom playbooks with what-if integration |
| No cross-project graph merge | Neo4j Bloom, Gephi, Linkurious | Union/intersection/diff merge with preview |
| No RAG-powered graph queries | ALL competitors | 17 RAG patterns with auto-routing |
| No agentic AI graph exploration | ALL competitors | 40+ agent types with tool integration |
| No engineering discipline patterns | ALL competitors | 8 composable meta-patterns |
| AI queries require cloud/GPU | Neo4j Bloom (cloud), Graphistry (GPU) | Local-first, LLM-optional, structured fallback |

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
- Trust badge: DETERMINISTIC (green), INFERRED (amber), AMBIGUOUS (orange), MANUAL (blue)

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

### FR-KGR-007: Export & Sharing (11+ Formats)

This surpasses every competitor's export (Graphify: HTML/JSON/GraphML/SVG/Obsidian/Mermaid/Cypher, Gephi: PNG/SVG/PDF/GEXF, yFiles: PNG-PDF-SVG-VSDX but €9.2K, Graphistry: CSV/JSON/Parquet).

- **PNG export**: current canvas at 2x resolution
- **SVG export**: vector graph via `cy.svg()`
- **PDF report**: graph image + node table + relationship summary + metrics
- **JSON-LD export**: graph data with EOIP ontology context
- **GraphML export**: standard graph interchange format
- **GEXF export**: Gephi-compatible graph exchange format (matches Gephi's native format)
- **CSV export**: separate nodes.csv and edges.csv files
- **Obsidian vault export**: entity-per-note structure with `[[wikilinks]]` for graph relationships, preserving domain hierarchy as folder structure (matches Graphify's Obsidian export)
- **Mermaid diagram export**: entity relationships as Mermaid flowchart/graph syntax for embedding in Markdown documentation (matches Graphify's Mermaid callflow)
- **Cypher script export**: graph as Neo4j-compatible Cypher CREATE/MERGE statements for pushing to Neo4j or FalkorDB (matches Graphify's Cypher export)
- **Clipboard**: copy selected node/edge as formatted Markdown
- **Context export**: current lens context as reusable JSON
- Export dialog with format selector, resolution options, scope (visible/all)
- Annotations included in PDF/JSON-LD/context exports when "Include annotations" is checked

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

### FR-KGR-010: Node Group Collapsing & Combo Declutter

Addresses a gap present in Graphify, Gephi, and code2flow. Matches Linkurious, yFiles, and KeyLines.

- **Group by domain**: Collapse all entities in a GraphDomain into a single combo node
- **Group by type**: Collapse all entities of the same vertex label into a combo node
- **Group by community**: Collapse detected community clusters into combo nodes
- **Custom grouping**: Select multiple nodes and collapse into a named group
- Combo node displays: group name, member count badge, aggregate edge count
- Double-click combo node to expand back to individual members
- Nested grouping: groups within groups (max 3 levels)
- Edges between groups become bundled super-edges with count labels
- Collapse/expand state persists across layout changes
- Keyboard shortcut: `G` to group selected, `Shift+G` to ungroup
- **Unique to KGR among free tools** — yFiles has this but costs €9,200+/yr, KeyLines is commercial

### FR-KGR-011: Geographic Mode (Geo-Mode)

Addresses a gap present in Graphify, Gephi, Sourcetrail, and code2flow. Matches Linkurious and Ogma.

- Position entities on a geographic map when they have location metadata (latitude/longitude properties, or region/datacenter tags)
- Map tile provider: OpenStreetMap (local tile cache, no external CDN in production)
- Entities without location data clustered in a sidebar or positioned at configurable default coordinates
- Edge rendering: curved lines between geographic positions with arrow markers
- Zoom levels: continent → country → city → site with progressive entity display
- Toggle between geo-mode and standard graph layout without losing selection state
- Use case: visualize service deployments, team locations, infrastructure topology
- Available as layout option in GraphToolbar (layout algorithm #13)
- Graceful degradation: if no entities have location data, show informative message

### FR-KGR-012: Code + Graph Side-by-Side View

Inspired by Sourcetrail's defining feature (graph + code + search synchronized). No free tool currently offers this in the browser.

- Split-pane view: graph canvas (left) + code viewer (right)
- Click a CodeSymbol node → code viewer scrolls to its definition (start_line/end_line)
- Click a File node → code viewer shows that file with syntax highlighting
- Highlight a function in code → corresponding graph node selected and centered
- Breadcrumb trail showing: File → Class → Method navigation
- Code viewer: read-only Monaco editor (already bundled in VS Code extension context) or lightweight syntax highlighter
- Source file retrieval: fetch from local filesystem via API endpoint `GET /api/v1/files/{path}`
- Diff view: when a Commit node is selected, show the commit's diff in the code panel
- Available as a toggle in the KGR toolbar ("Code Panel" button)
- **Surpasses Sourcetrail** by being browser-based (Sourcetrail was desktop Qt only) and supporting all languages (Sourcetrail supported only 4)

### FR-KGR-013: Visual Query Builder (No-Code)

Addresses Linkurious's no-code Query Builder capability. No other free tool offers this.

- Drag-and-drop visual query construction on a canvas
- Palette of entity types (from ontology manifest) as draggable node templates
- Palette of relationship types as connectable edge templates
- Property filter widgets on each node/edge template: operator (=, !=, >, <, contains, regex) + value
- Result limit and depth controls
- "Run Query" button converts visual pattern to QueryPlan and executes
- Results rendered on the main graph canvas with query pattern highlighted
- Save/load query patterns in localStorage with named configurations
- Share queries as exportable JSON
- **Surpasses Linkurious** by being integrated with the full KGR explorer, not a standalone mode

### FR-KGR-014: Dead Code & Orphaned Entity Detection

Inspired by code2flow's orphaned function detection. Extended to cover all entity types.

- **Orphaned entities**: identify graph nodes with zero incoming edges (unreferenced)
- **Dead code symbols**: CodeSymbol nodes with no CALLED_BY, REFERENCES, or IMPORTS edges
- **Disconnected components**: entities in components not connected to any domain hub
- **Stale entities**: entities whose last ingestion_run is older than a configurable threshold
- Visual indicator: orphaned nodes get a distinct style (dashed border, dimmed opacity)
- Filter dimension: toggle to show only orphaned/stale entities
- Available in the Health dashboard as a dedicated "Dead Code" widget with count and drill-down
- API endpoint: `GET /api/v1/graph/orphaned` returns orphaned entity list
- **Surpasses code2flow** (only functions in 4 languages) by covering all entity types in a language-agnostic graph

### FR-KGR-015: Community Auto-Labeling

Addresses a gap in all competitors except Graphify (which has basic community labeling).

- Automatically name detected communities based on the most prevalent entity types and shared properties within the cluster
- Labeling algorithm: extract top-3 most common vertex labels + top-3 most common property values (e.g., "Code: auth-service, API, security")
- Community labels displayed on convex hull overlays in the graph
- Community labels shown in the community filter dropdown
- Override: user can rename a community label (persisted in localStorage)
- Community summary card: click a hull to see member count, dominant types, key hub nodes, intra-community density
- **Surpasses Graphify** which labels communities but doesn't allow user overrides or show summary cards

### FR-KGR-016: PR / Change Impact Dashboard

Inspired by Graphify's PR dashboard (`graphify prs`) with community-based conflict detection.

- **PR list**: display open pull requests/merge requests with title, branch, author, status
- **Community overlap detection**: for each PR, identify which graph communities are touched by its changes
- **Conflict risk indicator**: when two or more PRs touch the same community, flag as potential conflict (HIGH: >50% overlap, MEDIUM: 20-50%, LOW: <20%)
- **Change heatmap**: overlay on the graph showing which nodes/edges are affected by each PR
- **PR comparison view**: select two PRs to see their blast radius overlap
- Data source: GitLab MR API / GitHub PR API via existing connectors
- Available as a dedicated dashboard accessible from the KGR lens toolbar
- **Surpasses Graphify** by providing visual overlap analysis (Graphify only lists PRs with community labels)

### FR-KGR-017: Self-Contained Interactive HTML Export

Inspired by Graphify's `graph.html` but significantly more capable. No competitor bundles search, filtering, and inspection into a single portable HTML file.

- Single HTML file containing: graph data (compressed JSON), rendering engine (Sigma.js inline), interaction logic
- Interactive features in exported HTML: zoom/pan, click-to-inspect, search bar, filter by entity type, community hull overlays, domain coloring, node sizing by degree
- Responsive: works on mobile browsers
- Dark/light theme auto-detect from OS
- Target file size: < 2MB for 5K-node graph, < 10MB for 20K-node graph
- Export option in ExportMenu alongside existing formats
- **Surpasses Graphify**: KGR's graph.html includes search, filtering, community hulls, and full inspector — Graphify's only has zoom/pan

### FR-KGR-018: Automated Graph Intelligence Report

Inspired by Graphify's GRAPH_REPORT.md but with far deeper analysis.

- Auto-generated Markdown report with 7 sections:
  1. Executive summary (node/edge counts, density, components)
  2. Topology statistics (degree distribution, clustering coefficient, diameter)
  3. Centrality analysis (top-10 by each of 8 centrality algorithms)
  4. Community breakdown (auto-labels, inter/intra density, bridge nodes)
  5. Evidence coverage (trust distribution, provenance depth, unevidenced entities)
  6. Health assessment (completeness, freshness, anomalies, stale entities)
  7. Actionable recommendations (orphaned entities, missing edges, risk hotspots)
- Export option: "Graph Report" button in ExportMenu
- **Surpasses Graphify**: adds centrality analysis, evidence coverage, health scores, actionable recommendations

### FR-KGR-019: Hub Exclusion Filter

Inspired by Graphify's `--exclude-hubs` flag. Hub nodes dominate visuals and obscure substructures.

- New filter dimension (#12): max degree threshold slider
- Quick presets: "Remove top-1%", "Remove top-5%", "Remove top-10%"
- Visual indicator: dimmed hub silhouette showing excluded node position
- "Show hubs" toggle to re-enable
- Hub exclusion reveals hidden community structures
- **Surpasses Graphify**: visual indicator of excluded hubs (Graphify just hides them)

### FR-KGR-020: Surprising/Unexpected Connection Detection

Inspired by Graphify's unexpected connection ranking. Extended with cross-domain analysis and absence detection.

- **Surprising edges**: edges connecting structurally distant entities (low Jaccard similarity of neighborhoods × long alternate path × cross-domain bonus)
- **Surprising communities**: communities bridging 3+ different GraphDomains
- **Unexpected absence**: entity pairs with high link prediction scores but no actual edge — connections that probably should exist
- API endpoint: `GET /api/v1/graph/surprises`
- UI: "Surprise" sidebar tab with ranked list, click to highlight on graph
- Sparkle icon overlay on surprising edges in graph view
- **Surpasses Graphify**: adds cross-domain analysis and unexpected absence detection

### FR-KGR-021: Rule-Based Conditional Visual Styling

Inspired by Neo4j Bloom's "Perspective" system and Linkurious's conditional styling.

- Rule builder: IF [entity type] [property] [operator] [value] THEN [set color/size/shape/border/icon/label]
- Rule priority: top-to-bottom, first match wins
- Live preview: rules apply immediately as edited
- Template rules: pre-built rule sets for common patterns (test files green, deprecated entities red, high-risk entities large)
- Persist rules in localStorage, import/export as JSON
- **Surpasses Neo4j Bloom**: rules are composable, exportable, and apply to all 10 graph types

### FR-KGR-022: Lasso/Rectangle Multi-Selection

Inspired by KeyLines and yFiles. Essential for large graph interaction.

- Shift+drag: freeform lasso (polygon) selection — all nodes inside the polygon selected
- Ctrl+Shift+drag: rectangle selection
- Selection count badge in toolbar
- "Select all in community" context menu option
- Group selection actions: hide all, expand all, blast radius union, export selection
- **Unique among free tools** — KeyLines (€5K+) and yFiles (€9.2K) both charge for this

### FR-KGR-023: URL Deep Linking / Graph State Sharing

Inspired by Neo4j Bloom's shareable scene URLs.

- Encode graph state in URL hash: graph type, active filters, selected node, zoom/pan, layout algorithm
- "Copy link to this view" button in toolbar
- Opening shared URL restores exact graph state
- Browser bookmark compatible
- State update debounced (500ms) to avoid excessive URL changes
- **Surpasses Neo4j Bloom**: includes filter state, layout, and zoom (Bloom only encodes selection)

### FR-KGR-024: Alternative Table/List View (Accessibility)

WCAG requirement: provide non-visual alternative to graph visualization.

- Sortable, filterable data table showing graph entities
- Columns: Name, Type, Domain, Degree, In-Degree, Out-Degree, Evidence, Status
- Expandable rows: show relationships for each entity
- Virtual scrolling for large datasets (50K+ rows)
- Toggle via toolbar button or keyboard shortcut (`T`)
- Split view option: table (left) + graph (right) with synchronized selection
- Full keyboard navigation with ARIA table roles
- Screen reader compatible
- **Unique to KGR** — no competitor offers a true accessible table alternative

### FR-KGR-025: Investigation Playbooks

Inspired by Graphistry's investigation workflows. Guided exploration for common analysis patterns.

- Built-in playbooks: Impact Assessment, Root Cause Analysis, Community Health Check, Dependency Audit
- Playbook runner: step-by-step guided mode with progress indicator
- Each step auto-executes analysis and waits for user input where needed
- User-created custom playbooks saved in localStorage
- Export/import playbooks as JSON for team sharing
- **Surpasses Graphistry**: includes what-if simulation and anomaly detection steps (Graphistry is GPU-only commercial)

### FR-KGR-026: Cross-Project Graph Merge

Inspired by Graphify's multi-repo graph merging.

- Merge strategies: union (add all), intersection (keep common), diff (keep unique)
- Conflict resolution: primary wins on property conflicts with audit trail
- Accept EOIP snapshot files or GraphML/GEXF imports
- Preview merge: show counts of added/merged/skipped/conflicted entities before applying
- Undo merge via exploration history
- API endpoint: `POST /api/v1/graph/merge`

### FR-KGR-027: RAG-Powered Graph Intelligence (17 Patterns)

The system SHALL support 17 Retrieval-Augmented Generation patterns over the knowledge graph, making KGR the first graph platform with native RAG capabilities.

#### 27.1 RAG Patterns

| # | Pattern | Retrieval Strategy | When to Use |
|---|---|---|---|
| 1 | Simple RAG | Keyword match + 1-hop BFS | Simple factual queries |
| 2 | Advanced RAG | Query expansion → retrieval → re-ranking → filtering | Complex queries needing precision |
| 3 | Graph RAG | Community-based: summarize per-community → merge | Questions spanning the entire graph |
| 4 | Hybrid RAG | Vector similarity + graph traversal + keyword BM25 | Multi-modality queries |
| 5 | Corrective RAG (CRAG) | Retrieve → evaluate → corrective re-retrieval if poor | When initial retrieval insufficient |
| 6 | Self-RAG | Retrieve → generate → self-evaluate → regenerate if poor | Response quality verification |
| 7 | Adaptive RAG | Query classifier → route to simplest sufficient RAG | Cost/latency optimization |
| 8 | Agentic RAG | Agent loop: plan → execute → evaluate → adjust → iterate | Open-ended exploration |
| 9 | Modular RAG | Composable pipeline: search → retrieve → rerank → compress → generate | Custom retrieval pipelines |
| 10 | HyDE | Generate hypothetical document → use as retrieval query | Abstract queries, concrete answers |
| 11 | Conversational RAG | Session memory + context carry-forward | Multi-turn exploration sessions |
| 12 | Multi-step RAG | Decompose complex query → sequential sub-queries → aggregate | Compound questions |
| 13 | Multi-hop RAG | Graph path traversal through N hops for transitive context | Causal chains, lineage traces |
| 14 | Branched RAG | Parallel retrieval branches → merge best results | Multiple valid retrieval paths |
| 15 | Multimodal RAG | Across modalities: graph + code + documentation + diagrams | Cross-domain queries |
| 16 | Speculative RAG | Multiple drafts in parallel → verify against facts → select best | High-confidence answers |
| 17 | RAG of RAGs | Meta-RAG: routes to sub-RAGs, aggregates, resolves conflicts | Complex multi-pattern queries |

- Auto-routing: RAGRouter classifies queries and selects best pattern
- LLM-optional: structured graph analysis fallback when no LLM configured
- API: `POST /api/v1/rag/query` (auto-routed), `POST /api/v1/rag/query/{pattern}` (specific)
- **Unique to KGR** — no graph visualization tool has native RAG capabilities

### FR-KGR-028: Agentic AI Graph Intelligence (40+ Agent Types)

The system SHALL support 40+ agent types organized into 9 categories, each operating over the EOIP knowledge graph.

#### 28.1 Agent Categories

| Category | Agents | Capabilities |
|---|---|---|
| Reactive | Simple Reflex, Model-Based Reflex | Condition-action rules, internal state tracking |
| Deliberative | Goal-Based, Utility-Based, Planner, Executor | Goal decomposition, utility maximization, plan generation |
| Tool-Using | Tool-Calling, Function-Calling, RAG Agent | Invoke graph APIs, execute queries, RAG-enhanced responses |
| Orchestration | Orchestrator, Router, Hierarchical, Task Agent | Multi-agent coordination, query routing, task decomposition |
| Collaboration | Choreography, Peer-to-Peer, Consensus, Collaboration, Swarm | Decentralized coordination, voting, emergent behavior |
| Meta-Cognitive | Critic, Reflection, Self-Reflection, Reviewer, Validator, XAI Agent | Self-evaluation, explanation generation, quality assurance |
| Autonomous | Self-Learning, Self-Evolving, Self-Writing, Deep AI Agents | Online learning, strategy evolution, code generation |
| Enterprise | Enterprise Agent, Just-In-Time Agent | Compliance-aware analysis, on-demand provisioning |
| Multi-Agent | Multi-Agent System, Agentic Swarm | Agent composition, swarm intelligence for parallel exploration |

- Agent registry with factory pattern for dynamic instantiation
- Perceive-decide-act lifecycle with memory persistence
- Tool integration: all graph analysis tools available to agents
- API: `POST /api/v1/agents/query` (auto-routed), `POST /api/v1/agents/query/{type}` (specific)
- **Unique to KGR** — no graph visualization tool has an agent framework

### FR-KGR-029: Engineering Disciplines (8 Patterns)

The system SHALL implement 8 engineering discipline patterns that compose RAG, agents, and graph analysis into higher-order intelligence systems.

| # | Discipline | Purpose | Use Case |
|---|---|---|---|
| 1 | Loop Engineering | Iterative refinement cycles with convergence detection | Refining community detection thresholds, sensitivity tuning |
| 2 | Graph Engineering | Structured graph construction, optimization, and maintenance | Schema optimization, index recommendations, migration planning |
| 3 | Harness Engineering | Controlled execution environments with safety bounds | Sandboxed what-if simulations, rate limiting, circuit breakers |
| 4 | Memory Engineering | 5-tier memory system (short-term, working, long-term, episodic, semantic) | Agents that learn from prior analysis sessions |
| 5 | Context Engineering | Optimal context assembly within token budgets | Assembling relevant graph context for LLM queries |
| 6 | Prompt Engineering | Structured prompt construction with template library | Effective prompts for graph analysis, chain-of-thought reasoning |
| 7 | Graph-over-Loop Engineering | Graph traversal drives iteration control flow | Automated dependency chain analysis, root cause search |
| 8 | Loop-over-Graph Engineering | Iterative loops progressively refine graph understanding | Progressive intelligence that improves each pass |

- API: `POST /api/v1/engineering/{discipline}` for each pattern
- Composable: disciplines can be combined (e.g., Loop + Graph-over-Loop for multi-pass traversal)
- **Unique to KGR** — no competitor has formalized engineering discipline patterns

### FR-KGR-030: AI Explorer Panel

Integrated chat-style interface for AI-powered graph exploration.

- Natural language questions about the graph
- Structured responses with: text explanation, graph highlights, action buttons, source references
- RAG pattern indicator showing which pattern was used
- Agent type indicator showing which agent processed the query
- Confidence score for each response
- Pre-built quick actions: "Explain this cluster", "What would break?", "Find surprising connections"
- Session memory: conversation history persisted
- LLM-optional: structured graph analysis fallback without LLM
- Keyboard shortcut: `A` to toggle AI Explorer
- **Unique to KGR** — no competitor has integrated AI graph exploration

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
  creation_status?: 'DETERMINISTIC' | 'INFERRED' | 'AMBIGUOUS' | 'MANUAL';
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

### 5.2 Endpoints (Implemented — Phases 3-10)

| Method | Path | Description | Phase |
|---|---|---|---|
| POST | `/api/v1/graph/centrality/full` | Full centrality (8 algorithms) | 3 |
| POST | `/api/v1/graph/shortest-paths` | All shortest paths (Yen's k-shortest) | 3 |
| POST | `/api/v1/graph/cluster` | Leiden/Louvain/Label Propagation community detection | 4 |
| POST | `/api/v1/graph/similarity` | Jaccard/Adamic-Adar/Common neighbors | 5 |
| POST | `/api/v1/graph/link-prediction` | Predict missing edges | 5 |
| POST | `/api/v1/graph/k-core` | k-core decomposition | 6 |
| POST | `/api/v1/graph/components` | Connected component analysis | 6 |
| POST | `/api/v1/graph/degree-distribution` | Degree histogram data | 6 |
| WS | `/ws/graph/events` | WebSocket for real-time graph changes | 7 |
| GET | `/api/v1/graph/events` | Polling fallback with since_id | 7 |
| POST | `/api/v1/graph/diff` | Compare two graph snapshots | 8 |
| POST | `/api/v1/graph/what-if` | Simulate entity removal/isolation | 8 |
| POST | `/api/v1/graph/anomalies` | Detect outlier nodes (3 algorithms) | 8 |
| GET | `/api/v1/graph/orphaned` | Orphaned entity detection | 10 |
| GET | `/api/v1/graph/stale` | Stale entity detection | 10 |
| GET | `/api/v1/graph/pr-impact` | PR/MR community overlap analysis | 10 |
| GET | `/api/v1/files/{path}` | File content retrieval for code panel | 10 |

### 5.3 Endpoints (Planned — Phases 12-13)

| Method | Path | Description | Phase |
|---|---|---|---|
| GET | `/api/v1/graph/surprises` | Surprising/unexpected connection detection | 12 |
| POST | `/api/v1/graph/merge` | Cross-project graph merge | 12 |
| POST | `/api/v1/rag/query` | Auto-routed RAG query over knowledge graph | 13 |
| POST | `/api/v1/rag/query/{pattern}` | Specific RAG pattern (17 available) | 13 |
| GET | `/api/v1/rag/patterns` | List available RAG patterns | 13 |
| POST | `/api/v1/rag/evaluate` | Evaluate retrieval quality for a query | 13 |
| POST | `/api/v1/agents/query` | Auto-routed agent query | 13 |
| POST | `/api/v1/agents/query/{type}` | Specific agent type (40+ available) | 13 |
| GET | `/api/v1/agents/types` | List available agent types | 13 |
| POST | `/api/v1/agents/orchestrate` | Multi-agent orchestration | 13 |
| GET | `/api/v1/agents/memory` | Agent memory state | 13 |
| POST | `/api/v1/engineering/loop` | Run a loop engineering cycle | 13 |
| POST | `/api/v1/engineering/context` | Assemble optimal context | 13 |
| POST | `/api/v1/engineering/prompt` | Build a structured prompt | 13 |
| POST | `/api/v1/engineering/harness/sandbox` | Create sandboxed environment | 13 |
| GET | `/api/v1/engineering/memory` | Query agent memory | 13 |
| POST | `/api/v1/engineering/traverse` | Graph-over-loop traversal | 13 |

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

### 7.3 Centrality Analysis (Implemented — Phase 3)
- **Degree centrality**: in/out/total
- **Betweenness centrality**: Brandes' algorithm, normalized by (n-1)(n-2)
- **Closeness centrality**: inverse of average shortest path length
- **PageRank**: iterative, 20 iterations, damping=0.85
- **Eigenvector centrality**: power iteration, 50 iterations
- **Katz centrality**: alpha=0.1, 50 iterations
- **HITS hub/authority**: 20 iterations, normalized
- **Harmonic centrality**: handles disconnected graphs
- Display as radar chart in Impact tab
- Client-side: centrality.js with 8 matching functions

### 7.4 Community Detection (Implemented — Phase 4)
- **Leiden algorithm**: 3-phase (local moving → refinement via BFS → aggregation), max 10 iterations, guarantees connected communities
- **Louvain**: single-pass modularity optimization with resolution parameter
- **Label Propagation**: async, max 20 iterations, random tie-breaking
- **Auto-labeling**: top-3 vertex labels + top-2 name tokens per community (Phase 10)
- Visual: convex hull overlays on graph canvas with cluster coloring

### 7.5 Similarity Analysis (Implemented — Phase 5)
- **Jaccard similarity**: |N(u) ∩ N(v)| / |N(u) ∪ N(v)|
- **Adamic-Adar**: sum(1/log(|N(w)|)) for w in common neighbors
- **Common neighbors**: simple count
- **Link prediction**: predict missing edges for non-adjacent pairs only

### 7.6 Graph Statistics (Implemented — Phases 1+6)
- Vertex count, edge count, density
- Vertex/edge label counts
- Connected components (BFS/DFS)
- Clustering coefficient
- Degree distribution histogram
- k-core decomposition (iterative peeling)

### 7.7 What-If Analysis (Implemented — Phase 8)
- **simulate_removal**: compute broken paths, orphaned entities, centrality changes
- **simulate_isolation**: keep entity but remove all edges
- MutationPlan with NL intent parsing (6 intent types)
- Confirm/execute scenario via SimulationWorkspace
- Before/after comparison view

### 7.8 Anomaly Detection (Implemented — Phase 8)
- **degree_zscore_outliers**: nodes with degree > mean + threshold*std
- **dense_subgraph_detection**: unexpectedly dense clusters
- **missing_expected_edges**: gaps detected via link prediction
- **orphaned_entities**: zero incoming edges (excludes meta-labels) (Phase 10)
- **stale_entities**: last modification > threshold (default 168 hours) (Phase 10)

### 7.9 Surprising Connection Analysis (Planned — Phase 12)
- Structural surprise scoring: 1/jaccard × path_length × cross_domain_bonus
- Community bridge detection: communities spanning 3+ domains
- Unexpected absence: high link prediction score but no actual edge

### 7.10 RAG Intelligence (Planned — Phase 13)
- 17 RAG patterns from Simple RAG to RAG of RAGs
- Graph-native retrieval: community-based, path-based, similarity-based
- Auto-routing: RAGRouter classifies queries to optimal pattern
- LLM-optional: structured fallback without LLM configured

### 7.11 Agentic Intelligence (Planned — Phase 13)
- 40+ agent types in 9 categories (reactive, deliberative, tool-using, orchestration, collaboration, meta-cognitive, autonomous, enterprise, multi-agent)
- Perceive-decide-act lifecycle with memory persistence
- Agent registry with factory pattern for dynamic instantiation
- All graph analysis tools available to agents as callable tools

### 7.12 Engineering Disciplines (Planned — Phase 13)
- 8 meta-patterns composing RAG + agents + graph analysis
- Loop, Graph, Harness, Memory, Context, Prompt, Graph-over-Loop, Loop-over-Graph
- Composable: disciplines can be combined for multi-pass intelligent analysis

---

## 8. Acceptance Criteria

| ID | Criterion | Competitor Gap Addressed |
|---|---|---|
| AC-01 | User can switch between 10 graph types with appropriate visualization | Graphify: 1 type, Bloom: 1, Gephi: 1 |
| AC-02 | 8-tab inspector shows properties, relationships, impact, evidence, similarity, history, annotations, raw | Graphify: properties only |
| AC-03 | Blast radius renders concentric rings with depth/type breakdown and risk | No competitor has this |
| AC-04 | Centrality metrics computed and displayed as radar chart | Gephi: desktop only, Bloom: GDS required |
| AC-05 | 12 layout algorithms available and switchable without data loss | Graphify: 1, code2flow: 1 |
| AC-06 | Graph renders 1,000 nodes in < 2 seconds | Sourcetrail: crashes, code2flow: cluttered |
| AC-07 | Progressive WebGL rendering handles 50,000 nodes | Graphify: 5K limit |
| AC-08 | All existing EOIP lenses continue unchanged | N/A |
| AC-09 | Export produces valid PNG, SVG, PDF, JSON-LD, GraphML, CSV, GEXF, Obsidian, Mermaid, Cypher | Graphify: HTML/JSON/GraphML/SVG/Obsidian/Mermaid/Cypher — KGR matches all + adds PDF/JSON-LD/GEXF |
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
| AC-21 | Node group collapsing works with domain/type/community/custom grouping | yFiles (€9.2K), KeyLines (commercial), Linkurious (commercial) — KGR does it free |
| AC-22 | Code + graph side-by-side view with synchronized navigation | Sourcetrail (discontinued, desktop, 4 langs) — KGR is browser-based, all languages |
| AC-23 | Visual query builder produces valid QueryPlans without writing code | Linkurious (commercial) — KGR does it free |
| AC-24 | Dead code / orphaned entity detection with visual indicators | code2flow (4 langs, CLI only) — KGR covers all entity types |
| AC-25 | Community auto-labeling with user override and summary cards | Graphify (basic labeling only, no override) |
| AC-26 | PR/change impact dashboard with community overlap detection | Graphify (list only, no visual overlap) |
| AC-27 | 11+ export formats covering every competitor's export capability | Surpasses all: matches Graphify's 7 + adds PDF/JSON-LD/GEXF/clipboard |
| AC-28 | AMBIGUOUS evidence status supported alongside DETERMINISTIC/INFERRED/MANUAL | Matches Graphify's 3-tier evidence (EXTRACTED/INFERRED/AMBIGUOUS) |
| AC-29 | Geo-mode positions entities on map when location metadata available | Linkurious, Ogma (commercial) — KGR does it free |
| AC-30 | Semantic zoom shows 3 levels (cluster/entity/detail) with smooth transitions | No free competitor has this |
| AC-31 | Fisheye distortion provides 2x magnification at cursor with gradual falloff | yFiles (€9.2K) — KGR does it free |
| AC-32 | Force-directed edge bundling declutters high-degree nodes | yFiles (€9.2K) — KGR does it free |
| AC-33 | Color-blind safe palette with 3 modes (deuteranopia/tritanopia/high-contrast) | No competitor has 3 palette modes |
| AC-34 | Self-contained interactive HTML export with search/filter/inspect | Graphify (basic zoom only) — KGR adds full interaction |
| AC-35 | Automated graph report with 7 analysis sections | Graphify (basic topology) — KGR adds centrality, health, recommendations |
| AC-36 | Hub exclusion filter with visual indicator of excluded nodes | Graphify (flag only, no visual) |
| AC-37 | Surprising connection detection with cross-domain and absence analysis | Graphify (basic ranking only) |
| AC-38 | Rule-based conditional styling with composable IF/THEN rules | Neo4j Bloom, Linkurious (both commercial) — KGR does it free |
| AC-39 | Lasso and rectangle multi-selection for large graphs | KeyLines, yFiles (commercial) — KGR does it free |
| AC-40 | URL deep linking encodes full graph state (filters, zoom, selection, layout) | Neo4j Bloom (selection only) — KGR encodes full state |
| AC-41 | Alternative table view provides WCAG-accessible data browsing | No competitor has this |
| AC-42 | Investigation playbooks guide multi-step analysis workflows | Graphistry (GPU-only, commercial) — KGR does it free |
| AC-43 | Cross-project graph merge with preview and undo | Graphify (multi-repo, no preview) |
| AC-44 | 17 RAG patterns route queries to optimal retrieval strategy | No graph viz tool has RAG |
| AC-45 | 40+ agent types with perceive-decide-act lifecycle | No graph viz tool has agents |
| AC-46 | 8 engineering disciplines compose RAG + agents into higher-order intelligence | Unique to KGR |
| AC-47 | AI Explorer panel provides chat-based graph exploration with LLM-optional fallback | Neo4j Bloom (NL, cloud-only) — KGR is local-first + multi-RAG |
| AC-48 | MCP tools expose RAG/agent/engineering capabilities to external clients | Graphify (basic MCP) — KGR has full RAG+agent MCP |

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
| Ambiguous edge | Relationship that couldn't be fully resolved — e.g., dynamic dispatch, reflection, string-built imports |
| Combo node | A collapsed group of nodes represented as a single visual element |
| Geo-mode | Positioning graph nodes on a geographic map using location metadata |
| Orphaned entity | A graph node with zero incoming edges — unreferenced by any other entity |
| Visual query builder | Drag-and-drop interface for constructing graph queries without writing code |
| Community labeling | Automated naming of detected clusters based on member entity characteristics |
| Semantic zoom | Adjusting visible detail level (labels, edges, hulls) based on zoom factor |
| Fisheye distortion | Magnification effect centered at cursor position with gradual falloff |
| Edge bundling | Force-directed algorithm that groups nearby parallel edges for visual clarity |
| Hub exclusion | Filtering out high-degree nodes to reveal hidden substructures |
| Surprising connection | An edge between structurally distant entities — low neighborhood overlap, long alternate path |
| Lasso selection | Freeform polygon drawn by dragging; all nodes inside the polygon are selected |
| Deep linking | Encoding graph state (filters, zoom, selection) in the URL for sharing or bookmarking |
| Investigation playbook | A guided multi-step analysis workflow with pre-defined actions and user checkpoints |
| RAG | Retrieval-Augmented Generation — a pattern that retrieves relevant context before generating a response |
| Graph RAG | A RAG variant using community detection to summarize graph neighborhoods as retrieval context |
| Self-RAG | A RAG variant that evaluates its own output for groundedness and regenerates if quality is low |
| CRAG | Corrective RAG — triggers corrective re-retrieval when initial results are insufficient |
| Agentic RAG | A RAG variant using an agent loop to iteratively plan, retrieve, and evaluate |
| HyDE | Hypothetical Document Embedding — generates a hypothetical answer to use as a retrieval query |
| RAG of RAGs | A meta-RAG that routes to multiple sub-RAG patterns and aggregates their results |
| Agent registry | A factory-pattern registry that instantiates agent types by name |
| Loop Engineering | Iterative refinement cycles over graph analysis with convergence detection |
| Graph Engineering | Structured graph construction, schema optimization, and health monitoring |
| Harness Engineering | Controlled execution environments with sandboxing, rate limiting, and circuit breakers |
| Memory Engineering | 5-tier memory system for agent state (short-term, working, long-term, episodic, semantic) |
| Context Engineering | Optimal context assembly for LLM interactions within token budgets |
| Prompt Engineering | Structured prompt construction with templates, chain-of-thought, and few-shot examples |
| Graph-over-Loop | Pattern where graph traversal drives the iteration loop's control flow |
| Loop-over-Graph | Pattern where iterative loops progressively refine graph understanding |
