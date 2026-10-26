| Field | Value |
|---|---|
| Registry ID | T-C16-sigma |
| Tier | B (used in EOIP UI, WebGL; subject of ADR-KG3-10) |
| Versions examined | sigma 4.0.3 (2026-10-15), 4.0.0 (2026-10-08), 3.0.0 (2024-12-12), 3.0.1 (2025-01-16), 2.4.0 (2022-11-04, EOIP pin); graphology 0.26.0 (2025-01-26) vs EOIP 0.25.4 |
| Verified on | 2026-10-26 (actual session date) |
| Worker | V30 |

## 1. Identity, status, sources
Sigma.js: MIT WebGL graph-rendering library on graphology; maintainers Alexis Jacomy, Benoit Simard (OuestWare), Guillaume Plique (Sciences Po medialab); repo created 2012, pushed 2026-10-16, not archived [CLAIM-sigma-01]. **The registry brief's "3.x" is stale: 3.0.0 shipped 2024-12-12 and 4.0.0 on 2026-10-08; npm `latest` is 4.0.3** [CLAIM-sigma-02]. A rendering library, not a product. Placeholder `C16-sigma-graphology-visualization.md` untouched.

## 2. Problem, workloads, workflows
Interactive display of large node-link graphs with GPU draw; layouts and metrics come from graphology's standard library (ForceAtlas2, Louvain, etc.). EOIP: `apps/web/src/kgr/renderers/SigmaRenderer.jsx` (180 lines; labels "WebGL · N nodes · M edges"; no aria attributes found in the file).

## 3. Feature inventory
| Feature | Status |
|---|---|
| WebGL node/edge/label rendering | present; v4 WebGL2 only, labels via SDF [CLAIM-sigma-03] |
| Declarative styles API (replaces node/edgeReducer mostly) | v4 present |
| Node dragging, parallel edges, self-loops, curved/step edges | v4 built-in (were plugins `@sigma/edge-curve`, `node-square`) |
| Canvas fallback | absent (WebGL1 dropped in v4) |
| Layouts / algorithms | via graphology (separate) |
| Compound/group nodes | absent |
| Accessibility | not documented (UNVERIFIED) [CLAIM-sigma-04] |
| Time-machine, permission filtering | absent (application concern) |
| Map layers (leaflet/maplibre), heatmap layer | v4 present |

## 4. Architecture
```
graphology Graph (state, attrs) -> sigma (reducers/styles) -> single WebGL2 program
   (node/edge primitives + SDF labels + depth layers) -> picking buffer -> events
layouts/metrics: graphology-* packages (CPU, web workers optional)
```
## 5. Reconstruction
Data model: graphology multigraph held in browser memory (the real scale ceiling beyond GPU); sigma uploads typed arrays of per-item attributes; v4 merges layers and compiles shapes/paths into one program [CLAIM-sigma-03]; picking by colour-ID or geometry (hypothesis, not read from source). No server tier, no auth, no persistence: all multi-tenant and ACL concerns live in EOIP's API.

## 6. Requirements inferred
Browser must expose WebGL2 (a hard gate for locked-down VDI/air-gapped thin clients); an accessible non-canvas alternative is the application's job.

## 7. Performance model
Project states "thousands of nodes and edges" in the README and gives no numeric limit on sigmajs.org [CLAIM-sigma-05]. The v4.0.0 release makes no performance claims [CLAIM-sigma-03]. Independent: Memgraph blog found Sigma notably faster than D3/vis up to 10k nodes (tested range only); NetV.js paper compared Sigma with others on a ~50k-node axis; the 2025 PMC benchmark of D3/ECharts/G6/NetV did **not** include Sigma or Cytoscape [CLAIM-sigma-06]. Therefore "60 FPS on 100,000+ nodes" (ADR-KG3-10) is unsupported by any source located. Memory: graphology in-heap objects dominate beyond ~10^5 items (hypothesis).

## 8. Strengths
GPU-native; small, focused, MIT; graphology ecosystem; v4 styles/primitives reduce custom shader code; maintained by researchers with a mapping (Gephi-style) heritage. Match: keep. STR-sigma-01..02.

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | none on large static graphs; label collision is visual-only |
| Operational | WebGL2 only (v4); GPU/driver variance; context loss |
| Friction | v2->v4 are two breaking majors; no compound nodes, no analysis API, no a11y |
| Maturity | v4.0.0 only 18 days old at verification, three patches in a week; maintainers say LLMs helped v4 work [CLAIM-sigma-01] |

## 10. Deployment and licensing
MIT; fully air-gap viable; redistribution-safe; no cloud. `@sigma/*` plugins MIT presumed (UNVERIFIED).

## 11. Delta vs baseline
BL-54: EOIP is on 2.4.0 (2022), i.e. two majors behind, and graphology 0.25.4 vs 0.26.0. Both renderers exist in `apps/web/src/kgr/renderers/`. **Sigma 2.4->4.x migration:** v4 breaking changes: `hidden`/`forceLabel` replaced by `visibility`/`labelVisibility`; `itemSizesReference` default `screen`->`positions`; removed packages; WebGL1 dropped; reducers superseded by styles (migration guide exists but was not fetched) [CLAIM-sigma-03]. Recommendation: do 2.4->3.0.1 first, defer 4.x to ~4.1.

## 12. Cards
STR-sigma-01 | Sigma | GPU rendering with graphology ecosystem | CLAIM-03 | large exploration views | integrate | renderer interface, one Sigma impl | acceptance: 50k nodes/150k edges >=30 FPS pan on reference GPU.
STR-sigma-02 | Sigma | v4 declarative styles | CLAIM-03 | policy-driven styling (classification colours) | integrate | style = f(attr, ACL state) | test: hidden nodes never emitted to the graphology instance.
INV-sigma-01 | target Sigma 4.0.x; limitation: no non-WebGL fallback or accessible representation; cause: rendering architecture (proven for WebGL2-only); alternative: dual path (accessible table/tree + WebGL) is correct but needs synchronised selection state, worse when two views diverge; options: (a) ship ADR's table/tree view; (b) generic `GraphView` contract with parity tests; (c) server-side summarised outline. Selected (b). POC: axe + keyboard-only task on 5k-node graph, parity test of selection. Decision ADOPT.
INV-sigma-02 | permission leakage via client graph: any node loaded to graphology is inspectable. Cause: client holds data (proven). Alternative: send only ACL-filtered, aggregated tiles; decision EXPERIMENT.

## 13. Decisions
CAP-70 REUSE (primary candidate, pending benchmark); CAP-71 EXPERIMENT; CAP-73 BUILD; CAP-52 REUSE (MIT).

## 14. Tests
Reproduce on EOIP's data: synthetic 10k/50k/100k/250k nodes, ratios 1/3/10; measure FPS, JS heap, GPU memory on three GPU classes (integrated, mid discrete, VDI software GL); WebGL2-less browser behaviour; sigma 2.4->3.0.1 diff of SigmaRenderer.

## 15. Risks / ADR evaluation (neutral)
ADR-KG3-10 (file marked APPROVED, dated 2026-10-18, no cited evidence) claims: (1) Cytoscape+Sigma duplication inflates bundles — plausible, Cytoscape chunk measured 443 KB, Sigma chunk unmeasured (stale dist); (2) "60 FPS on 100,000+" — **unsupported**; no located source measures Sigma at that scale, and Cytoscape's own WebGL preview is also unbenchmarked independently; (3) deprecating Cytoscape loses selectors, compound nodes, algorithms, Canvas fallback — not addressed. Evidence-based position: a single renderer is reasonable engineering, but choose after a measured bake-off; Sigma is the leading GPU candidate, not a proven 100k solution. Risk: ADR also drops Canvas fallback while Sigma 4 needs WebGL2.

## Appendix A — Dimensions
| Dim | Sec | Summary |
|---|---|---|
| D1,D19,D20 | 1,9 | MIT, active, 12.2k stars |
| D2 | 2 | large-graph display |
| D3,D4,D5 | 3-5 | table, diagram |
| D6 | N/A | in-memory |
| D7,D8 | 7 | no numbers published |
| D9 | N/A | none |
| D10 | 9,12 | client-held data |
| D11,D12,D18 | 10 | MIT |
| D13,D21 | 3 | graphology, plugins |
| D14 | 9 | no a11y |
| D15,D16,D17 | N/A | client lib |
| D22 | 9 | WebGL2 |
| D23 | 11 | v4 |
| D24 | 15 | ADR |

## Appendix B — Capabilities
| CAP | Tech | CLAIM | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-70 | native | 03,05 | BL-54 | REUSE | P1 |
| CAP-71 | partial | 03 | BL-54 | EXPERIMENT | P2 |
| CAP-73 | absent | 04 | absent | BUILD | P2 |

## Appendix C — Evidence
| CLAIM | product/version/date | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-sigma-01 | repo | MIT, created 2012, pushed 2026-10-16, maintainers, LLM-assisted v4 | verified | GitHub API/page | 2026-10-16/10-26 | 0.9 | none |
| CLAIM-sigma-02 | npm | 3.0.0 2024-12-12; 4.0.0 2026-10-08; latest 4.0.3 | verified | registry.npmjs.org/sigma | / 10-26 | 0.95 | none |
| CLAIM-sigma-03 | 4.0.0 | WebGL2-only, styles API, breaking changes, no perf claims | verified | github.com/jacomyal/sigma.js release sigma@4.0.0 | 2026-10-08 / 10-26 | 0.9 | none |
| CLAIM-sigma-04 | docs | no accessibility mention | absence | sigmajs.org, README | / 10-26 | 0.4 | not exhaustively searched |
| CLAIM-sigma-05 | docs | "thousands of nodes and edges", no numeric limit | vendor claim | sigmajs.org; README | / 10-26 | 0.8 | tagline "Render large graphs" |
| CLAIM-sigma-06 | benchmarks | PMC 2025 excludes Sigma/Cytoscape; Memgraph test up to 10k | independent, partial | PMC12061801; memgraph.com blog | 2025-05-08 / 10-26 | 0.7 | none |

## Appendix D — Assumptions
Reducer-to-styles migration effort not measured; "3.x" in brief treated as outdated. Sigma 3 release notes not read.
