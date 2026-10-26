# C16 Tier C records (batch V30) — verified 2026-10-26

Access date is the actual session date. Entries marked UNVERIFIED were not confirmed this session.

### T-C16-graphviz — Graphviz
| Field | Value |
|---|---|
| Official URL | https://graphviz.org |
| Owner | Graphviz community (gitlab.com/graphviz/graphviz) |
| Latest version | 16.1.0-1 accepted into Debian experimental 2026-09-08 (distro upload; upstream tag UNVERIFIED) |
| Status | active |
| Licence | Eclipse Public License (from prior knowledge; not re-fetched) — weak-copyleft |
| Deployment / air-gap | CLI/library; yes |
| Tier reason | Static layout/rendering (DOT) |

Relevance: batch DOT/SVG layout (dot, sfdp) for reports, lineage and ontology diagrams; no interactivity. CAP-72, CAP-70 (static). **Decision:** REUSE as optional server-side exporter for static diagrams.
[CLAIM-gv-01] Graphviz | Debian tracker shows 16.0.0-1 (2026-08-23) and 16.1.0-1 (2026-09-08), Fedora 15.1.0 (2026-06-22) | secondary | Debian/Fedora package trackers | 0.5 | upstream not checked.

### T-C16-constellation — Constellation
| Field | Value |
|---|---|
| Official URL | https://github.com/constellation-app/constellation |
| Owner | Australian Signals Directorate (open-sourced 2019) |
| Latest version | UNVERIFIED (GitHub API blocked) |
| Status | UNVERIFIED (likely maintained) |
| Licence | Apache-2.0 (Computerworld/AlternativeTo) — permissive |
| Deployment / air-gap | Java/NetBeans desktop; yes |
| Tier reason | Analysis desktop app |

Relevance: government-grade link-analysis desktop with claimed scale to "billions of inputs" (vendor claim, unqualified); reference for analyst workflows, not an embeddable web UI. CAP-71. **Decision:** REFERENCE-ONLY.
[CLAIM-cn-01] Constellation | open-sourced under Apache 2.0, August 2019, NetBeans Java | secondary | computerworld.com; technologydecisions.com.au | 0.6 | none.

### T-C16-yed — yEd
| Field | Value |
|---|---|
| Official URL | https://www.yworks.com/products/yed |
| Owner | yWorks GmbH |
| Latest version | 3.25.1 (date not shown) |
| Status | active |
| Licence | Free to use incl. commercial under yEd SLA; may not be distributed or used in automated processes — proprietary |
| Deployment / air-gap | Java desktop; yes |
| Tier reason | Desktop diagram editor |

Relevance: free layout/diagram editor on the yFiles engine; useful for manual ontology sketches; cannot be bundled. CAP-72. **Decision:** REFERENCE-ONLY.
[CLAIM-yed-01] yEd 3.25.1 | free incl. commercial; no redistribution or automated use | vendor | yworks.com/products/yed | 0.8 | SLA not read.

### T-C16-citespace-vosviewer — CiteSpace and VOSviewer
| Field | Value |
|---|---|
| Official URL | https://www.vosviewer.com ; CiteSpace UNVERIFIED |
| Owner | CWTS Leiden University (VOSviewer); Chaomei Chen (CiteSpace) |
| Latest version | VOSviewer 1.6.21 (2026-06-12); CiteSpace UNVERIFIED |
| Status | VOSviewer active; CiteSpace UNVERIFIED |
| Licence | VOSviewer "free to use for any purpose" (terms not detailed); CiteSpace UNVERIFIED |
| Deployment / air-gap | Java desktop (VOSviewer needs Java 8+); yes |
| Tier reason | Bibliometric viz |

Relevance: domain-specific co-citation/term maps; shows density/cluster map idioms. Not a platform component. CAP-70 (idiom only). **Decision:** REFERENCE-ONLY.
[CLAIM-vv-01] VOSviewer 1.6.21 | released 2026-06-12, free for any purpose | vendor | vosviewer.com/download | 0.8 | none. CiteSpace: NOT PUBLICLY VERIFIED this session, 0.2.

### T-C16-cosmograph — Cosmograph / cosmos.gl
| Field | Value |
|---|---|
| Official URL | https://github.com/cosmosgl/graph |
| Owner | cosmos.gl, OpenJS Foundation incubating project; Cosmograph app by Cosmograph team |
| Latest version | @cosmos.gl/graph 3.5.1 (2026-10-08); v3 announced 2026-06-25 |
| Status | active |
| Licence | cosmos.gl MIT (package.json, repo). **Older @cosmograph/cosmos 3.4.1 and @cosmograph/react 2.5.1 are CC-BY-NC-4.0 (non-commercial)** — legal-review trigger |
| Deployment / air-gap | browser WebGL2 via luma.gl; yes |
| Tier reason | GPU force layout |

Relevance: layout and rendering both on the GPU; vendor claims "over one million nodes and links" (OpenJS) vs "hundreds of thousands" (README), without hardware. Strong candidate for million-node overview layer or layout; no a11y/analysis. CAP-70. **Decision:** EXPERIMENT (benchmark vs Sigma); REJECT the NC-licensed packages.
[CLAIM-cg-01] cosmos.gl 3.5.1 | MIT; @cosmograph/* CC-BY-NC-4.0 | verified | npm registry; github.com/cosmosgl/graph | 2026-10-08 | 0.9 | none.
[CLAIM-cg-02] scale claims differ (1M vs hundreds of thousands), no hardware | vendor | openjsf.org/blog/cosmos-gl-v3; README | 0.5.

### T-C16-d3 — D3.js
| Field | Value |
|---|---|
| Official URL | https://d3js.org |
| Owner | Observable / Mike Bostock community |
| Latest version | 7.9.0 (2024-03-12) |
| Status | maintenance (no release in 19 months) |
| Licence | ISC — permissive |
| Deployment / air-gap | browser; yes |
| Tier reason | Viz toolkit |

Relevance: primitives (d3-force, scales); SVG/Canvas only. Independent study (PMC12061801, Chrome 106, i7-12700/RTX 3060): D3-SVG 30 fps up to ~2k nodes (ratio 1), D3-Canvas 5k, D3-WebGL (NetV) 7k; at ratio 10: 600 / 2k / 5k [CLAIM-d3-01]. Use for charts/time axes, not as the graph renderer. CAP-70. **Decision:** REUSE (d3-force/scale utilities), REJECT as renderer.
[CLAIM-d3-01] above | independent | PMC12061801 (2025-05-08) | 0.8 | D3 v5.16 tested, old.
[CLAIM-d3-02] d3 7.9.0, ISC, 2024-03-12 | npm | 0.9.

### T-C16-vis-network — vis-network
| Field | Value |
|---|---|
| Official URL | https://github.com/visjs/vis-network |
| Owner | visjs community |
| Latest version | 10.1.3 (2026-10-25) |
| Status | active |
| Licence | Apache-2.0 OR MIT — permissive |
| Deployment / air-gap | browser Canvas; yes |
| Tier reason | Network viz |

Relevance: easy Canvas network with physics; modest scale (Memgraph blog: slower than Sigma up to 10k nodes, tested range only). CAP-70/71. **Decision:** REFERENCE-ONLY.
[CLAIM-vn-01] vis-network 10.1.3 | dual-licence | npm | 2026-10-25 | 0.9. [CLAIM-vn-02] slower than WebGL Sigma to 10k | memgraph.com blog | 0.5.

### T-C16-antv-g6 — AntV G6
| Field | Value |
|---|---|
| Official URL | https://g6.antv.antgroup.com |
| Owner | AntV / Ant Group |
| Latest version | 5.1.1 (2026-05-08) |
| Status | active |
| Licence | MIT |
| Deployment / air-gap | browser Canvas/SVG/WebGL renderers; yes (docs primarily Chinese/English) |
| Tier reason | Graph viz framework |

Relevance: richest open-source feature set after Cytoscape (combos, plugins, GPU layouts via G6 5). Independent: G6 v4.8.7 Canvas hit 30 fps only at ~1k nodes (ratio 1) and 200 (ratio 10), the weakest of those tested; version old (v5 not tested) [CLAIM-g6-01]. CAP-70/71. **Decision:** REFERENCE-ONLY; EXPERIMENT only if Cytoscape+Sigma bake-off fails.
[CLAIM-g6-01] PMC12061801 table 4 | independent | 0.7 | v4 vs v5.

### T-C16-neo4j-nvl — Neo4j NVL
| Field | Value |
|---|---|
| Official URL | https://neo4j.com/docs/nvl/current/ |
| Owner | Neo4j, Inc. |
| Latest version | @neo4j-nvl/base 2.0.0 (2026-09-15) |
| Status | active |
| Licence | **Proprietary**: "may only be used with" Aura or Neo4j's commercial products under their agreements — proprietary, restrictive |
| Deployment / air-gap | browser library; yes technically, contractually limited to Neo4j |
| Tier reason | Vendor viz library |

Relevance: Bloom/Browser rendering components; licence forbids use with other backends, so it conflicts with backend neutrality. CAP-70. **Decision:** REJECT as dependency; legal trigger.
[CLAIM-nvl-01] NVL licence text first paragraph | verified | unpkg.com/@neo4j-nvl/base@2.0.0/LICENSE.txt | 2026-09-15 | 0.9.

### T-C16-react-force-graph-reagraph — react-force-graph and Reagraph
| Field | Value |
|---|---|
| Official URL | github.com/vasturiano/react-force-graph ; github.com/reaviz/reagraph |
| Owner | Vasco Asturiano ; Reaviz |
| Latest version | react-force-graph 1.48.3 (2026-09-29); Reagraph 4.32.0 (2026-06-25) |
| Status | active |
| Licence | MIT ; Apache-2.0 |
| Deployment / air-gap | browser (Canvas/three.js WebGL); yes |
| Tier reason | React graph viz |

Relevance: React 19 wrappers around force-graph/three.js and a WebGL React lib; handy for 3D demos but no a11y, tenancy or aggregation. CAP-70. **Decision:** REFERENCE-ONLY.
[CLAIM-rfg-01] versions/licences | verified | npm | 0.9.

### T-C16-layout-engines — Layout engines (ELK/elkjs, Dagre, WebCola, ForceAtlas2)
| Field | Value |
|---|---|
| Official URL | github.com/kieler/elkjs ; github.com/dagrejs/dagre ; github.com/tgdwyer/WebCola ; graphology-layout-forceatlas2 |
| Owner | Kiel/Eclipse ELK ; dagrejs ; Dwyer ; Sciences Po medialab |
| Latest version | elkjs 0.12.0 (2026-07-17); @dagrejs/dagre 3.1.3 (2026-10-24; old `dagre` 0.8.5 is 2019); webcola 3.4.0 (2019-05-10); graphology-layout-forceatlas2 0.10.1 (2022-10-17) |
| Status | elkjs/dagrejs active; webcola and old dagre stale; FA2 stable, slow cadence |
| Licence | elkjs EPL-2.0 OR GPL-3.0-or-later (npm field; weak-copyleft dual — legal review); dagre/webcola/FA2 MIT |
| Deployment / air-gap | browser/worker; yes |
| Tier reason | Layouts |

Relevance: layered/orthogonal (ELK, dagre) for ontology and lineage; force (FA2, cola) for exploration; keep layouts separate from renderers so Cytoscape/Sigma/Cosmos are swappable (ties to ADR-KG3-10 neutral question). CAP-70/72. **Decision:** REUSE (ELK for layered, FA2 for force, drop WebCola).
[CLAIM-le-01] versions and licences | verified | npm registry | 2026-10-26 | 0.9.

### T-C16-kumu-thebrain — Kumu and TheBrain
| Field | Value |
|---|---|
| Official URL | https://kumu.io ; https://www.thebrain.com |
| Owner | Kumu Inc. ; TheBrain Technologies |
| Latest version | Kumu SaaS (continuous); TheBrain 14 (current store snapshot) |
| Status | active |
| Licence | Proprietary SaaS; Kumu Enterprise self-hosted or air-gapped on request; TheBrain perpetual desktop USD 219, cloud subscription |
| Deployment / air-gap | Kumu Enterprise yes (vendor); TheBrain desktop yes |
| Tier reason | Systems mapping |

Relevance: stakeholder/systems maps with lightweight collaboration; benchmark for non-technical UX (CAP-71). Kumu pricing: free public, USD 9-20 per private project per month, Enterprise by quote with 99.95% SLA (vendor). **Decision:** REFERENCE-ONLY.
[CLAIM-kt-01] Kumu pricing/enterprise | vendor | kumu.io/pricing | 0.8. [CLAIM-kt-02] TheBrain 14 pricing | vendor via search | thebrain.com/store | 0.5.
