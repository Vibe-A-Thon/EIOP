| Field | Value |
|---|---|
| Registry ID | T-C16-cytoscape |
| Tier | B (incumbent in EOIP UI; ADR-KG3-10 proposes deprecating it) |
| Versions examined | Cytoscape.js 3.34.4 (2026-10-15; npm/GitHub); EOIP pins ^3.30.0 (2024-06-27). Cytoscape desktop 3.10.5 (2026-09-29). Cytoscape Web 1.0 (named on cytoscape.org) |
| Verified on | 2026-10-26 (brief says 2026-10-18; actual access date used) |
| Worker | V30 |

## 1. Identity, status, sources
Two distinct products share a name. **Cytoscape.js** is an MIT graph-theory and visualisation library (U. Toronto lineage; Max Franz, maintainer), releases roughly monthly/weekly patches, active (3.34.0 2026-06-02 ... 3.34.4 2026-10-15) [CLAIM-cytoscape-01]. **Cytoscape desktop** is a Java bioinformatics network-analysis platform, LGPL-2.1 per its download licence page [CLAIM-cytoscape-02], JDK 17, app store with "over a hundred" third-party apps, federally funded (NRNB/NHGRI), 3.10.5 on 2026-09-29 [CLAIM-cytoscape-03]. The registry row (library used in EOIP) means Cytoscape.js; desktop is covered as a product comparator. Library vs product: Cytoscape.js is a library; desktop is a complete analysis product.

## 2. Problem, workloads, workflows
Pathway/interaction networks, graph theory + styling with a declarative stylesheet; EOIP uses it for the main graph canvas (`apps/web/src/kgr/renderers/CytoscapeRenderer.jsx`). Workflows: load elements, apply layout (fcose, cola, dagre extensions), select/filter via selectors, export PNG/JSON.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Canvas 2D renderer (default) | present |
| WebGL renderer | partial: preview since 3.31 via `renderer:{name:'canvas',webgl:true}`; only straight/haystack/bezier edges, no dashed, triangle arrowheads only [CLAIM-cytoscape-04] |
| Selector query language, graph algorithms (BFS, PageRank, centrality, etc.) | present (library includes analysis) |
| Compound nodes, layouts (built-in + extensions fcose, cola, dagre, elk) | present / plugin |
| Accessibility (ARIA, keyboard) | absent in core; not mentioned in README (UNVERIFIED beyond README) [CLAIM-cytoscape-05] |
| TypeScript types | present (index.d.ts) |
| Time-machine / permission filtering | absent (application concern) |
| Desktop: CyREST, apps, Cytoscape Web | present |

## 4. Architecture
```
data -> Collection(cy.elements) -> style engine (selectors) -> layout (sync/async ext)
     -> renderer: Canvas2D layers | optional WebGL (sprite-sheet nodes, batched edges)
     -> events/gestures -> app state (React wrapper is app code)
```
## 5. Under-the-hood reconstruction
In-memory element collections with indexed selectors; stylesheet cascade evaluated per element; canvas renderer redraws layers with hit-testing; WebGL mode pre-renders nodes to texture sprite sheets (causes initial delay) and batches edges [CLAIM-cytoscape-04]. No tenant/permission model; no persistence. Hypothesis: label and style evaluation dominate cost on large graphs (not measured here).

## 6. Requirements inferred
Layouts and stylesheets must be portable; extension layouts must run in a worker or be bounded; renderer must degrade with a non-GPU fallback (Canvas works without WebGL).

## 7. Performance and resource model
Project-published preliminary figures (Chrome, M1 MacBook Pro): ~1,200 nodes/16,000 edges: ~20 FPS Canvas, >100 FPS WebGL; ~3,200 nodes/68,000 edges: ~3 FPS Canvas, ~10 FPS WebGL; results vary with styles [CLAIM-cytoscape-04]. These are vendor/project claims, small samples, no independent reproduction found. No independent 100k-node Cytoscape.js benchmark was found [CLAIM-cytoscape-06]. Local measure: EOIP `apps/web/dist/assets/cytoscape.esm-*.js` is 443,042 bytes (built, not gzip) [CLAIM-cytoscape-07]. Failure mode: label-heavy Canvas redraw; WebGL sprite warm-up.

## 8. Strengths
Mature selector/style/algorithm stack; compound nodes; large extension ecosystem; Canvas fallback needing no GPU; MIT; active. Match: keep as the "analysis canvas" with rich styling. See STR-cytoscape-01, 02.

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | Canvas CPU redraw limits (~thousands of nodes at interactive rates per project numbers) |
| Operational | WebGL preview feature-incomplete; provisional tuning options |
| Friction | No a11y; desktop Java/GPL-free but app-ecosystem licences vary; desktop version cadence slow (3.10.4 2025-09, 3.10.5 2026-09) |
| Licensing | Library MIT; desktop LGPL-2.1 (legal review if embedded) |

## 10. Deployment and licensing
Library: browser only, fully air-gap viable, MIT, redistribution-safe. Desktop: LGPL, JVM, offline viable, not embeddable as a white-label web component. Cytoscape Web is a separate browser product (not examined deeply).

## 11. Competitive delta vs baseline
BL-54: EOIP ships both Cytoscape ^3.30 and Sigma ^2.4 renderers; large-graph performance unmeasured. EOIP trails Cytoscape.js 3.34.4 by four minors (low risk, MIT). [CLAIM-cytoscape-01]

## 12. Strength / inversion cards
STR-cytoscape-01 | Cytoscape.js | rich selector+style+algorithm model | CLAIM-01 | analysts get filter-by-selector | integrate | keep behind a renderer interface | acceptance: same selector set drives both renderers.
STR-cytoscape-02 | Cytoscape.js | no-GPU Canvas fallback | CLAIM-04 | air-gapped thin clients without WebGL2 | integrate | auto-fallback | test on software-GL VM.
INV-cytoscape-01 | target: Cytoscape.js Canvas 3.30; limitation: interactive frame rate collapses beyond a few thousand elements (project figures); cause: CPU canvas redraw (proven by project numbers, hypothesis for exact thresholds); alternative: server-side aggregation + progressive disclosure so the client rarely exceeds ~5k elements; worse when analysts need raw-graph overview. Options: (a) enable `webgl:true` for large views; (b) native subgraph budgeting API; (c) permission-aware aggregate tiles. Selected: (b). Benchmark: LDBC-style 100k/1M edge graph, 30 FPS pan at <=5k visible elements, p95 aggregation <500 ms. Dependencies: tenant ACL on aggregates (no leak of hidden counts). Defensibility: permission-correct aggregation is not in any renderer. Decision EXPERIMENT.
**Seed §10.5 (Gephi/desktop visualisers):** see C16-gephi.

## 13. Per-capability decisions
CAP-70 EXPERIMENT (WebGL mode as optional path); CAP-71 REUSE (selector-driven exploration); CAP-72 REJECT for this library; CAP-73 BUILD (outside library).

## 14. Tests and acceptance
(1) Render 1k/5k/20k/100k synthetic nodes, edge ratios 1/3/10, Chrome stable, record FPS for Canvas vs WebGL. (2) axe/keyboard audit of the canvas wrapper. (3) Bundle-size diff with/without library using the current build. Accept: published numbers reproduced on EOIP's hardware class.

## 15. Risks and open questions
ADR-KG3-10's deprecation rationale (bundle size, "60 FPS on 100k+") is unmeasured; evaluate: Cytoscape adds a measured 443 KB chunk but Sigma's chunk was not in the dist (stale build) so no comparison exists [CLAIM-cytoscape-07]. Open: WebGL preview stability; a11y plan.

## Appendix A — Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 identity/status | 1 | active, MIT |
| D2 workloads | 2 | analysis canvas |
| D3 features | 3 | table |
| D4 architecture | 4,5 | canvas/WebGL |
| D5 query/language | 3 | selectors |
| D6 storage | N/A | in-memory library |
| D7 performance | 7 | project figures only |
| D8 scaling | 7,9 | client-bound |
| D9 reasoning | N/A | none |
| D10 security/tenancy | 9 | none in library; app-level |
| D11 deployment | 10 | browser, JVM desktop |
| D12 licensing | 10 | MIT / LGPL-2.1 |
| D13 ecosystem | 3 | extensions, app store |
| D14 UX | 3,9 | no a11y |
| D15 ops | N/A | client-side |
| D16 governance | N/A | none |
| D17 AI | N/A | none |
| D18 cost | 10 | free |
| D19 maturity | 1 | monthly releases |
| D20 community | 1 | 11.3k stars (GitHub page) |
| D21 integration | 3 | CyREST, extensions |
| D22 limits | 9 | see |
| D23 roadmap | 3 | WebGL preview |
| D24 risks | 15 | see |

## Appendix B — Capability mapping
| CAP | Tech | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-70 | partial (Canvas; WebGL preview) | 04 | BL-54 implemented, unmeasured | EXPERIMENT | P1 |
| CAP-71 | partial | 01 | BL-54 | REUSE | P2 |
| CAP-73 | absent | 05 | absent | BUILD | P2 |

## Appendix C — Evidence records
| CLAIM | product/version/date | claim | class | source | dates | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-cytoscape-01 | Cytoscape.js 3.34.4, 2026-10-15 | active monthly releases, MIT | verified | GitHub API releases; npm registry | 2026-10-15 / 2026-10-26 | 0.9 | none |
| CLAIM-cytoscape-02 | desktop | LGPL-2.1 licence agreement | verified | cytoscape.org/download (via search result) | n/d / 2026-10-26 | 0.7 (GitHub repo shows no licence field) | repo licence field null |
| CLAIM-cytoscape-03 | desktop 3.10.5, 2026-09-29 | release date; JDK17 | verified | GitHub releases; README | 2026-09-29 / 2026-10-26 | 0.85 | none |
| CLAIM-cytoscape-04 | 3.31 WebGL preview | project benchmark numbers and limitations | vendor claim | blog.js.cytoscape.org/2025/01/13/webgl-preview | 2025-01-13 / 2026-10-26 | 0.7 | no independent repro |
| CLAIM-cytoscape-05 | 3.34 | no accessibility mention in README | absence of evidence | github.com/cytoscape/cytoscape.js | / 2026-10-26 | 0.4 | none found |
| CLAIM-cytoscape-06 | library | no independent 100k-node benchmark found | search result | web search; PMC12061801 excludes Cytoscape.js | 2025-05-08 / 2026-10-26 | 0.6 | none |
| CLAIM-cytoscape-07 | EOIP build | cytoscape chunk 443,042 B; no sigma chunk | local measurement | apps/web/dist/assets | / 2026-10-26 | 0.9 | dist may be stale |

## Appendix D — Assumptions
Registry "Cytoscape and Cytoscape.js": library is primary. Access date is actual session date. Licence of desktop from download page, repo metadata is empty.
