| Field | Value |
|---|---|
| Registry ID | T-C16-yfiles |
| Tier | B (commercial diagramming/graph SDK; OEM terms) |
| Versions examined | yFiles for HTML 3.1.0.4 (release notes page; date not shown); 2.6 docs for WebGL history |
| Verified on | 2026-10-26 |
| Worker | V30 |

## 1. Identity, status, sources
yFiles by yWorks GmbH: commercial SDK family (HTML, .NET, Java, Avalonia ...); also powers the free yEd desktop editor [CLAIM-yfiles-01]. Current: yFiles for HTML 3.1 series, latest 3.1.0.4 [CLAIM-yfiles-02]. Active; vendor site shows 2026 copyright. A rendering/layout **library**, not an investigation product.

## 2. Problem and workflows
Diagram and network editing with automatic layout: BPMN, UML, network topology, process maps, knowledge-graph views with orthogonal/hierarchical routing. EOIP relevance: ontology/schema diagrams and lineage views (CAP-72), where layered layout quality beats force layout.

## 3. Features
| Feature | Status |
|---|---|
| Layout algorithms (hierarchical, orthogonal, organic, edge routing; vendor: "powerful and diverse") | present [CLAIM-yfiles-03] |
| Rendering: SVG default, WebGL/WebGL2 render mode | present; 3.1 adds WebGL zoom policies, port shapes, beacon/halo animation [CLAIM-yfiles-02] |
| Interactive editing (input modes, undo, grouping, folding) | present |
| Graph analysis | present (vendor) |
| GraphML serialisation incl. WebGL styles | present (3.1) |
| Accessibility | not addressed on pages read (UNVERIFIED) |
| Time/permission features | absent (app concern) |

## 4. Architecture
```
IGraph model (nodes/edges/ports/groups) -> layout engine (sync/async, may run in web worker)
  -> view: SVG/Canvas-like template rendering OR WebGL2 style layer -> input modes -> app
```
## 5. Reconstruction
Typed object model with styles per item and a visual-template pipeline; SVG for rich per-node HTML-like templates, WebGL path for large graphs where styles are restricted to a WebGL style set (3.1 API names above). Closed source; internals beyond API names are hypothesis.

## 6. Requirements inferred
Fixed layout determinism for diff views; item-count-aware render mode switching; licence key bound to domain.

## 7. Performance
Vendor: "efficient handling and rendering of large graphs"; no figures given [CLAIM-yfiles-03]. No independent benchmark located. SVG mode is DOM-bound (hypothesis: low thousands); WebGL mode is for larger graphs (vendor docs recommend WebGL2, 2.6 guide).

## 8. Strengths
Best-in-class automatic layout and edge routing for structured diagrams; editing; mature (decades); source licensable. STR-yfiles-01: layered/orthogonal layouts for ontologies. Match via ELK (EPL) + dagre; exceed not credible short term.

## 9. Limitations
Licensing: term (annual) licence, no perpetual option seen; Single Developer EUR 9,200/USD 11,000 per year, Project EUR 18,400/USD 22,000, Site EUR 55,200/USD 66,000 (vendor list, VAT excl.) [CLAIM-yfiles-04]. Operational: WebGL path limits styling. Friction: proprietary API; each EOIP white-label customer deployment may need OEM terms.

## 10. Deployment and redistribution
Client-side JS, no forced cloud, "data never leaves your environment" (vendor) [CLAIM-yfiles-04]; air-gap viable. Redistribution/OEM/SaaS specifics are **not on the public pricing page**; refers to the Software License Agreement and sales; domain keys (single-domain vs unrestricted) matter for multi-tenant white-label. Legal-review trigger: yes (OEM and SaaS terms, term-licence lapse behaviour). Source code licensable via sales.

## 11. Delta vs baseline
BL-54: EOIP has no layered/orthogonal diagram editor; ontology studio views rely on general force layouts (hypothesis, not audited).

## 12. Cards
STR-yfiles-01 above. INV-yfiles-01 | target yFiles for HTML 3.1; limitation: annual licence + unclear OEM; cause: licensing (proven); alternative: ELK/dagre layouts + Cytoscape/own editor, worse for orthogonal routing quality; options (a) buy Project licence for a studio module, (b) elkjs+Sigma/Cytoscape layouts, (c) own layered layout service; selected (b) with (a) as optional customer-supplied plugin; POC: layout of 500-class ontology, crossing count/time vs yFiles trial; decision EXPERIMENT.

## 13. Decisions
CAP-72 INTEGRATE (optional, customer-licensed plugin); CAP-70 REJECT as core; layouts REUSE ELK.

## 14. Tests
Trial: lay out 200/1,000/5,000-node hierarchical ontologies; measure time and crossings vs elkjs; confirm domain-key behaviour behind tenant subdomains; read the SLA text for OEM/SaaS.

## 15. Risks
Licence cost grows per project; vendor lock-in; unknown redistribution terms; WebGL feature gaps.

## Appendix A — Dimensions
| Dim | Sec | Summary |
|---|---|---|
| D1-D3 | 1-3 | commercial SDK, features |
| D4,D5 | 4,5 | model/render |
| D6,D9,D15-D17 | N/A | client library |
| D7,D8 | 7 | no figures |
| D10 | 9 | no tenancy features |
| D11,D12,D18 | 9,10 | term licence |
| D13,D21 | 3 | many platforms, GraphML |
| D14 | 3 | a11y unknown |
| D19,D20 | 1 | mature |
| D22-D24 | 9,15 | see |

## Appendix B — Capabilities
| CAP | Tech | CLAIM | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-72 | native | 03 | absent/partial | INTEGRATE | P3 |
| CAP-70 | partial | 02 | BL-54 | REJECT core | P3 |
| CAP-52 | enterprise licence | 04 | n/a | EXPERIMENT | P3 |

## Appendix C — Evidence
| CLAIM | prod/ver/date | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-yfiles-01 | yEd 3.25.1 | built on yFiles; free use | vendor | yworks.com/products/yed | n/d / 10-26 | 0.8 | none |
| CLAIM-yfiles-02 | 3.1.0.4 | WebGL features list | vendor docs | yfiles.com release-notes | n/d / 10-26 | 0.85 | none |
| CLAIM-yfiles-03 | site | performance/layout claims, no figures | vendor claim | yfiles.com/the-yfiles-sdk | / 10-26 | 0.6 | no benchmark |
| CLAIM-yfiles-04 | pricing | term licence tiers/prices, domain keys, no forced cloud | vendor | yfiles.com/pricing | / 10-26 | 0.8 | prices may be promotional |

## Appendix D — Assumptions
Release date of 3.1.0.4 unknown; OEM terms not read (SLA text not fetched). Confidence on OEM = 0.3.
