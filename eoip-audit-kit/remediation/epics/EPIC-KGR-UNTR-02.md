# EPIC-KGR-UNTR-02: EOIP-engg-doc-pkg/KGR-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 22 tasks, ~138.0 h, priorities {'P2': 22}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-FR-KGR-010 [P2] FR-KGR-010: Node Group Collapsing & Combo Declutter

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:393-408` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Node Group Collapsing & Combo Declutter Addresses a gap present in Graphify, Gephi, and code2flow. Matches Linkurious, yFiles, and KeyLines. - Group by domain: Collapse all entities in a GraphDomain into a single combo node - Group by type: Collapse all entities of the same vertex label into a combo node - Group by community: Collapse detected community clusters into combo node
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-011 [P2] FR-KGR-011: Geographic Mode (Geo-Mode)

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:409-422` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Geographic Mode (Geo-Mode) Addresses a gap present in Graphify, Gephi, Sourcetrail, and code2flow. Matches Linkurious and Ogma. - Position entities on a geographic map when they have location metadata (latitude/longitude properties, or region/datacenter tags) - Map tile provider: OpenStreetMap (local tile cache, no external CDN in production) - Entities without location data cl
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-012 [P2] FR-KGR-012: Code + Graph Side-by-Side View

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:423-437` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Code + Graph Side-by-Side View Inspired by Sourcetrail's defining feature (graph + code + search synchronized). No free tool currently offers this in the browser. - Split-pane view: graph canvas (left) + code viewer (right) - Click a CodeSymbol node → code viewer scrolls to its definition (start_line/end_line) - Click a File node → code viewer shows that file with syntax highli
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-013 [P2] FR-KGR-013: Visual Query Builder (No-Code)

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:438-452` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Visual Query Builder (No-Code) Addresses Linkurious's no-code Query Builder capability. No other free tool offers this. - Drag-and-drop visual query construction on a canvas - Palette of entity types (from ontology manifest) as draggable node templates - Palette of relationship types as connectable edge templates - Property filter widgets on each node/edge template: operator (=
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-014 [P2] FR-KGR-014: Dead Code & Orphaned Entity Detection

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:453-466` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-014' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-014') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Dead Code & Orphaned Entity Detection Inspired by code2flow's orphaned function detection. Extended to cover all entity types. - Orphaned entities: identify graph nodes with zero incoming edges (unreferenced) - Dead code symbols: CodeSymbol nodes with no CALLED_BY, REFERENCES, or IMPORTS edges - Disconnected components: entities in components not connected to any domain hub - S
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-017 [P2] FR-KGR-017: Self-Contained Interactive HTML Export

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:492-503` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-017: Self-Contained Interactive HTML Export

Inspired by Graphify's `graph.html` but significantly more capable. No competitor bundles search, filtering, and inspection into a single portable HTML file.

- Single HTML file containing: graph data (compressed JSON), rendering engine (Sigma.js inline), interaction logic
- Interactive features in exported HTML: zoom/pan, click-to-inspect, search bar, filter by entity type, community hull overlays, domain coloring, node sizing by degree
- Responsive: works on mobile browsers
- Dark/light theme auto-detect from OS
- Target file size: < 2MB for 5K-node graph, < 10MB for 20K-node graph
- Export option in ExportMenu alongside existing formats
- **Surpasses Graphify**: KGR's graph.html includes search, filtering, community hulls, and full inspector — Graphify's only has zoom/pan
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-017' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-017') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Self-Contained Interactive HTML Export Inspired by Graphify's graph.html but significantly more capable. No competitor bundles search, filtering, and inspection into a single portable HTML file. - Single HTML file containing: graph data (compressed JSON), rendering engine (Sigma.js inline), interaction logic - Interactive features in exported HTML: zoom/pan, click-to-inspect, s
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-018 [P2] FR-KGR-018: Automated Graph Intelligence Report

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:504-518` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-018' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-018') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Automated Graph Intelligence Report Inspired by Graphify's GRAPH_REPORT.md but with far deeper analysis. - Auto-generated Markdown report with 7 sections: 1. Executive summary (node/edge counts, density, components) 2. Topology statistics (degree distribution, clustering coefficient, diameter) 3. Centrality analysis (top-10 by each of 8 centrality algorithms) 4. Community break
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-019 [P2] FR-KGR-019: Hub Exclusion Filter

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:519-529` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-019: Hub Exclusion Filter

Inspired by Graphify's `--exclude-hubs` flag. Hub nodes dominate visuals and obscure substructures.

- New filter dimension (#12): max degree threshold slider
- Quick presets: "Remove top-1%", "Remove top-5%", "Remove top-10%"
- Visual indicator: dimmed hub silhouette showing excluded node position
- "Show hubs" toggle to re-enable
- Hub exclusion reveals hidden community structures
- **Surpasses Graphify**: visual indicator of excluded hubs (Graphify just hides them)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-019' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-019') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Hub Exclusion Filter Inspired by Graphify's --exclude-hubs flag. Hub nodes dominate visuals and obscure substructures. - New filter dimension (#12): max degree threshold slider - Quick presets: "Remove top-1%", "Remove top-5%", "Remove top-10%" - Visual indicator: dimmed hub silhouette showing excluded node position - "Show hubs" toggle to re-enable - Hub exclusion reveals hidd
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-020 [P2] FR-KGR-020: Surprising/Unexpected Connection Detection

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:530-541` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-020: Surprising/Unexpected Connection Detection

Inspired by Graphify's unexpected connection ranking. Extended with cross-domain analysis and absence detection.

- **Surprising edges**: edges connecting structurally distant entities (low Jaccard similarity of neighborhoods × long alternate path × cross-domain bonus)
- **Surprising communities**: communities bridging 3+ different GraphDomains
- **Unexpected absence**: entity pairs with high link prediction scores but no actual edge — connections that probably should exist
- API endpoint: `GET /api/v1/graph/surprises`
- UI: "Surprise" sidebar tab with ranked list, click to highlight on graph
- Sparkle icon overlay on surprising edges in graph view
- **Surpasses Graphify**: adds cross-domain analysis and unexpected absence detection
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-020' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-020') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Surprising/Unexpected Connection Detection Inspired by Graphify's unexpected connection ranking. Extended with cross-domain analysis and absence detection. - Surprising edges: edges connecting structurally distant entities (low Jaccard similarity of neighborhoods × long alternate path × cross-domain bonus) - Surprising communities: communities bridging 3+ different GraphDomains
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-021 [P2] FR-KGR-021: Rule-Based Conditional Visual Styling

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:542-552` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-021: Rule-Based Conditional Visual Styling

Inspired by Neo4j Bloom's "Perspective" system and Linkurious's conditional styling.

- Rule builder: IF [entity type] [property] [operator] [value] THEN [set color/size/shape/border/icon/label]
- Rule priority: top-to-bottom, first match wins
- Live preview: rules apply immediately as edited
- Template rules: pre-built rule sets for common patterns (test files green, deprecated entities red, high-risk entities large)
- Persist rules in localStorage, import/export as JSON
- **Surpasses Neo4j Bloom**: rules are composable, exportable, and apply to all 10 graph types
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-021' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-021') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Rule builder: IF [entity type] [property] [operator] [value] THEN [set color/size/shape/border/icon/label] - Rule priority: top-to-bottom, first match wins - Live preview: rules apply immediately as edited - Template rules: pre-built rule sets for common patterns (test files green, deprecated entities red, high-risk entities large) - Persist rules in localStorage, import/export as JSON - Surpasses
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-022 [P2] FR-KGR-022: Lasso/Rectangle Multi-Selection

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:553-563` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-022: Lasso/Rectangle Multi-Selection

Inspired by KeyLines and yFiles. Essential for large graph interaction.

- Shift+drag: freeform lasso (polygon) selection — all nodes inside the polygon selected
- Ctrl+Shift+drag: rectangle selection
- Selection count badge in toolbar
- "Select all in community" context menu option
- Group selection actions: hide all, expand all, blast radius union, export selection
- **Unique among free tools** — KeyLines (€5K+) and yFiles (€9.2K) both charge for this
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-022' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-022') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Lasso/Rectangle Multi-Selection Inspired by KeyLines and yFiles. Essential for large graph interaction. - Shift+drag: freeform lasso (polygon) selection — all nodes inside the polygon selected - Ctrl+Shift+drag: rectangle selection - Selection count badge in toolbar - "Select all in community" context menu option - Group selection actions: hide all, expand all, blast radius uni
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-023 [P2] FR-KGR-023: URL Deep Linking / Graph State Sharing

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:564-574` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-023: URL Deep Linking / Graph State Sharing

Inspired by Neo4j Bloom's shareable scene URLs.

- Encode graph state in URL hash: graph type, active filters, selected node, zoom/pan, layout algorithm
- "Copy link to this view" button in toolbar
- Opening shared URL restores exact graph state
- Browser bookmark compatible
- State update debounced (500ms) to avoid excessive URL changes
- **Surpasses Neo4j Bloom**: includes filter state, layout, and zoom (Bloom only encodes selection)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-023' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-023') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): URL Deep Linking / Graph State Sharing Inspired by Neo4j Bloom's shareable scene URLs. - Encode graph state in URL hash: graph type, active filters, selected node, zoom/pan, layout algorithm - "Copy link to this view" button in toolbar - Opening shared URL restores exact graph state - Browser bookmark compatible - State update debounced (500ms) to avoid excessive URL changes - 
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-024 [P2] FR-KGR-024: Alternative Table/List View (Accessibility)

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:575-588` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-024' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-024') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] WCAG requirement: provide non-visual alternative to graph visualization.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-025 [P2] FR-KGR-025: Investigation Playbooks

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:589-599` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-025: Investigation Playbooks

Inspired by Graphistry's investigation workflows. Guided exploration for common analysis patterns.

- Built-in playbooks: Impact Assessment, Root Cause Analysis, Community Health Check, Dependency Audit
- Playbook runner: step-by-step guided mode with progress indicator
- Each step auto-executes analysis and waits for user input where needed
- User-created custom playbooks saved in localStorage
- Export/import playbooks as JSON for team sharing
- **Surpasses Graphistry**: includes what-if simulation and anomaly detection steps (Graphistry is GPU-only commercial)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-025' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-025') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Investigation Playbooks Inspired by Graphistry's investigation workflows. Guided exploration for common analysis patterns. - Built-in playbooks: Impact Assessment, Root Cause Analysis, Community Health Check, Dependency Audit - Playbook runner: step-by-step guided mode with progress indicator - Each step auto-executes analysis and waits for user input where needed - User-create
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-026 [P2] FR-KGR-026: Cross-Project Graph Merge

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:600-610` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-026: Cross-Project Graph Merge

Inspired by Graphify's multi-repo graph merging.

- Merge strategies: union (add all), intersection (keep common), diff (keep unique)
- Conflict resolution: primary wins on property conflicts with audit trail
- Accept EOIP snapshot files or GraphML/GEXF imports
- Preview merge: show counts of added/merged/skipped/conflicted entities before applying
- Undo merge via exploration history
- API endpoint: `POST /api/v1/graph/merge`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-026' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-026') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Cross-Project Graph Merge Inspired by Graphify's multi-repo graph merging. - Merge strategies: union (add all), intersection (keep common), diff (keep unique) - Conflict resolution: primary wins on property conflicts with audit trail - Accept EOIP snapshot files or GraphML/GEXF imports - Preview merge: show counts of added/merged/skipped/conflicted entities before applying - Un
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-027 [P2] FR-KGR-027: RAG-Powered Graph Intelligence (17 Patterns)

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:611-641` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 9.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-027' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-027') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Auto-routing: RAGRouter classifies queries and selects best pattern
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-028 [P2] FR-KGR-028: Agentic AI Graph Intelligence (40+ Agent Types)

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:642-665` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 9.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-028' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-028') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] The system SHALL support 40+ agent types organized into 9 categories, each operating over the EOIP knowledge graph.
- [ ] #### 28.1 Agent Categories - Agent registry with factory pattern for dynamic instantiation - Perceive-decide-act lifecycle with memory persistence - Tool integration: all graph analysis tools available to agents - API: POST /api/v1/agents/query (auto-routed), POST /api/v1/agents/query/{type} (specific) - Unique to KGR — no graph visualization tool has an agent framework
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-030 [P2] FR-KGR-030: AI Explorer Panel

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:685-701` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-030' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-030') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): AI Explorer Panel Integrated chat-style interface for AI-powered graph exploration. - Natural language questions about the graph - Structured responses with: text explanation, graph highlights, action buttons, source references - RAG pattern indicator showing which pattern was used - Agent type indicator showing which agent processed the query - Confidence score for each respon
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-NFR-KGR-001 [P2] NFR-KGR-001: Performance

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:704-712` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-KGR-001: Performance
- Graph rendering SHALL complete in < 2 seconds for up to 1,000 nodes and 5,000 edges (matches yFiles, beats Gephi)
- Progressive WebGL rendering SHALL support up to 50,000 nodes (beats Graphify 5K limit by 10x)
- Layout computation SHALL use Web Worker for graphs > 500 nodes (prevents UI blocking — fixes Sourcetrail's hang issue)
- Interaction response (click, hover, zoom) SHALL remain < 100ms at all sizes
- Memory usage SHALL not exceed 512 MB for 10,000 nodes (beats Graphistry's 537MB for 10M edges)
- Blast radius computation SHALL complete in < 2 seconds for 1,000 nodes
- Centrality computation SHALL complete in < 5 seconds for 5,000 nodes
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NFR-KGR-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NFR-KGR-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Performance - Graph rendering SHALL complete in < 2 seconds for up to 1,000 nodes and 5,000 edges (matches yFiles, beats Gephi) - Progressive WebGL rendering SHALL support up to 50,000 nodes (beats Graphify 5K limit by 10x) - Layout computation SHALL use Web Worker for graphs > 500 nodes (prevents UI blocking — fixes Sourcetrail's hang issue) - Interaction response (click, hove
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-NFR-KGR-002 [P2] NFR-KGR-002: Responsiveness

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:713-717` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-KGR-002: Responsiveness
- Full functionality at desktop (1280px+)
- Reduced but functional at tablet (768px-1279px): single-column, simplified inspector
- Read-only at mobile (< 768px): static graph image with tap-to-inspect
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NFR-KGR-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NFR-KGR-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Responsiveness - Full functionality at desktop (1280px+) - Reduced but functional at tablet (768px-1279px): single-column, simplified inspector - Read-only at mobile (< 768px): static graph image with tap-to-inspect
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-NFR-KGR-003 [P2] NFR-KGR-003: Accessibility

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:718-725` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-KGR-003: Accessibility
- WCAG 2.1 AA for all interactive controls (no competitor achieves this)
- Keyboard-navigable graph: Tab/Enter/Arrow keys/shortcuts
- Screen reader descriptions for graph topology
- Color-blind safe palette (deuteranopia, protanopia, tritanopia)
- High contrast mode
- Focus ring styling on all interactive elements
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NFR-KGR-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NFR-KGR-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Accessibility - WCAG 2.1 AA for all interactive controls (no competitor achieves this) - Keyboard-navigable graph: Tab/Enter/Arrow keys/shortcuts - Screen reader descriptions for graph topology - Color-blind safe palette (deuteranopia, protanopia, tritanopia) - High contrast mode - Focus ring styling on all interactive elements
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-NFR-KGR-004 [P2] NFR-KGR-004: Browser Support

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:726-731` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-KGR-004: Browser Support
- Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- No external runtime dependencies (everything bundled — fixes Graphistry's server dependency)
- Offline-capable after initial load
- No eval() or inline scripts (CSP-compatible)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NFR-KGR-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NFR-KGR-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Browser Support - Chrome 90+, Firefox 88+, Safari 14+, Edge 90+ - No external runtime dependencies (everything bundled — fixes Graphistry's server dependency) - Offline-capable after initial load - No eval() or inline scripts (CSP-compatible)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

