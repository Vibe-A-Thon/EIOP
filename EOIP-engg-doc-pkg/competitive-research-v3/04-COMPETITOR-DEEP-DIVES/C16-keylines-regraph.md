| Field | Value |
|---|---|
| Registry ID | T-C16-keylines-regraph |
| Tier | B (commercial graph-viz SDK) |
| Versions examined | KeyLines 8.13.0 and ReGraph 5.13.0 (both 2026-09-16, developers.cambridge-intelligence.com/downloads); notes for 8.9-8.10.2 (2026-02..05) |
| Verified on | 2026-10-26 |
| Worker | V30 |

## 1. Identity and status
Cambridge Intelligence: KeyLines (vanilla JS) and ReGraph (React) share a numbering line (8.x / 5.x), plus sibling SDKs KronoGraph (timeline) and MapWeave (geo) [CLAIM-kl-01]. Active, ISO 27001-certified company (vendor). Libraries, not full products.

## 2. Problem and workflows
Embed investigation-grade link analysis in a customer application: fraud, cyber, intelligence. Workflows: load subgraph from Neo4j/Neptune/TigerGraph, apply combos (group, drill down), run centrality/traversal highlight, filter with Time Bar, view on map, annotate.

## 3. Features
| Feature | Status |
|---|---|
| GPU-based rendering (vendor wording; WebGL/Canvas not named on pages; 8.10.1 notes mention a "Canvas mode") | present [CLAIM-kl-02] |
| Combos with open/close, 10x faster nested arrangements (8.10) | present [CLAIM-kl-03] |
| Time Bar filter (React component), KronoGraph integration | present |
| Graph engine (centrality, traversal) | present |
| Map mode (Leaflet / MapWeave) | present |
| Annotations (standalone since 5.9/8.9) | present |
| MCP server support (8.9 notes) | present, scope UNVERIFIED |
| Accessibility | not stated on pages read (UNVERIFIED) |
| Data backend | none; backend-agnostic |

## 4. Architecture
```
app data (any DB) -> KeyLines/ReGraph chart (items, combos, layouts, engine)
  -> GPU/canvas renderer -> events -> app (React state for ReGraph)
Time Bar / KronoGraph / MapWeave as separate components synchronised by the app
```
## 5. Reconstruction
Immutable props-driven model in ReGraph (React reconciliation to a retained scene), mutable API in KeyLines; layouts run incrementally; combos aggregate items client-side. Closed source: everything below the API is hypothesis.

## 6. Requirements inferred
Props-driven state suits server-side permission filtering (data never enters the chart unless allowed); investigators need combos, time filter, map, annotations.

## 7. Performance
Vendor: smooth large-graph performance via GPU rendering, incremental updates and tuned layouts; **no limits or benchmarks published** [CLAIM-kl-02]. Local estimate none. Independent evidence: none located.

## 8. Strengths
Mature investigation UX building blocks (combos, time bar, annotations, map); dedicated large-graph tuning; React-native API. STR-kl-01: combos as client-side progressive disclosure. STR-kl-02: Time Bar for CAP-73. Match with own components on Sigma/Cytoscape; exceed by tying combos to server aggregation and ACL.

## 9. Limitations
Licensing: commercial, licensed per application, tailored quotes, free trial only [CLAIM-kl-04]. Friction: closed internals, vendor roadmap. Hypothesis: client holds all loaded items so ACL must be applied before load. No pricing public.

## 10. Deployment and licensing
Client-side JS libraries, usable offline once bundled (air-gap viable; licence-key check mechanism UNVERIFIED). OEM/white-label/redistribution terms NOT PUBLICLY VERIFIED: licensing is "per application" and quote-based. Legal-review trigger: yes (embedding in a multi-tenant product redistributed to many customers; per-application vs per-deployment counting).

## 11. Delta vs baseline
BL-54 has no combos, time bar, annotation layer or map mode in the canvas (not audited in depth); collaboration annotations exist as BL-53.

## 12. Cards
STR-kl-01, STR-kl-02 above. INV-kl-01 | target ReGraph 5.13; limitation: closed, per-application licence incompatible with a free redistributable platform; cause: licensing (proven for commercial, per-app terms unverified); alternatives: (a) optional customer-licensed adapter, (b) native combos on Sigma/Cytoscape, (c) server-aggregated "combo tiles" with ACL; selected (b)+(c); POC: 10k-node graph, combo open/close <200 ms, hidden-node count not disclosed to unauthorised users; defensibility: permission-aware aggregation; decision EXPERIMENT.

## 13. Decisions
CAP-71 EXPERIMENT (build combos), INTEGRATE optional adapter; CAP-73 BUILD; CAP-70 REJECT as dependency.

## 14. Tests
Trial both SDKs: 1k/10k/50k node import, combo operations, Time Bar with 1M events; confirm offline licence; read OEM terms before any bundling.

## 15. Risks
Unknown OEM terms; vendor lock-in; feature creep if copying UX; cannot verify rendering tech.

## Appendix A
| Dim | Sec | Summary |
|---|---|---|
| D1-D3 | 1-3 | SDK, features |
| D4,D5 | 4,5 | hypothesis |
| D6,D9,D16,D17 | N/A | client lib |
| D7,D8 | 7 | no figures |
| D10 | 6,9 | filter before load |
| D11,D12,D18 | 10 | per-app licence |
| D13,D21 | 3 | Neo4j/Neptune/TigerGraph |
| D14 | 3 | a11y unknown |
| D19,D20 | 1 | active |
| D22-D24 | 9,15 | see |

## Appendix B
| CAP | Tech | CLAIM | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-70 | native | 02 | BL-54 | REJECT dependency | P3 |
| CAP-71 | native | 03 | BL-54/BL-53 | EXPERIMENT | P1 |
| CAP-73 | native Time Bar | 01 | absent | BUILD | P2 |

## Appendix C
| CLAIM | prod/ver/date | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-kl-01 | 8.13.0/5.13.0 2026-09-16 | latest versions | verified | developers.cambridge-intelligence.com/downloads | 2026-09-16 / 10-26 | 0.85 | none |
| CLAIM-kl-02 | pages | GPU-based rendering, no limits stated | vendor claim | cambridge-intelligence.com/keylines, /regraph | / 10-26 | 0.7 | none |
| CLAIM-kl-03 | 8.10 2026-03-30 | combo speedups, patches | vendor release notes (via search summary) | cambridge-intelligence.com release notes | 2026-03-30 / 10-26 | 0.6 | secondary summary |
| CLAIM-kl-04 | pages | per-application licensing, trial | vendor | cambridge-intelligence.com/keylines | / 10-26 | 0.7 | OEM terms absent |

## Appendix D
Rendering technology unnamed on public pages: not assumed WebGL. Time Bar mention taken from ReGraph page, not KeyLines page.
