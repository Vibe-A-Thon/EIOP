| Field | Value |
|---|---|
| Registry ID | T-C16-gephi |
| Tier | B (seed inversion target, Master Prompt §10.5) |
| Versions examined | Gephi 0.11.3 (2026-09-06), 0.11.2 (2026-05-09), 0.11.1 (2026-05-03), 0.10.1 (2023-01-17); Gephi Lite 1.1 (announced 2026-10-07); Gephi Toolkit |
| Verified on | 2026-10-26 |
| Worker | V30 |

## 1. Identity and status
Gephi: open desktop graph exploration/analysis platform, Java on NetBeans Platform, OpenGL visualisation; community project (Open Collective backers, Weblate translations) [CLAIM-gephi-01]. Active: repo pushed 2026-10-25, 6.7k stars, not archived. Licence: GitHub shows **GPL-3.0**; Gephi's wiki states dual CDDL 1.0 + GPL v3; gephi.org states GPL only [CLAIM-gephi-02]. Gephi's website still described 0.11 as in beta in April/May 2026 posts while GitHub has 0.11.1-0.11.3 released: website is stale [CLAIM-gephi-03]. Product (desktop) plus Toolkit library plus Gephi Lite (browser).

## 2. Problem and workflows
Network science and journalism: import GEXF/CSV/GraphML, run ForceAtlas2/OpenOrd layouts, statistics (modularity, centrality), filter, partition/rank styling, export PNG/PDF/SVG. Single analyst, static data.

## 3. Features
| Feature | Status |
|---|---|
| OpenGL engine rewritten from scratch (0.11.1) | present [CLAIM-gephi-01] |
| ForceAtlas2, Fruchterman-Reingold, OpenOrd, community detection, centrality | present |
| Dynamic (time-slider) networks | present (GEXF dynamic; depth UNVERIFIED) |
| Plugin ecosystem | present (count not on page) |
| Toolkit (Graph, Layout, Filters, IO) for server/CLI | present (Java library) |
| Gephi Lite browser version | present, scope UNVERIFIED |
| Live DB connection, multi-user, permissions | absent |
| Accessibility | UNVERIFIED |

## 4. Architecture
```
file import -> in-memory graph store (Graph API, Java heap) -> layout/filters/statistics
 -> OpenGL canvas  | Preview (SVG/PDF export) ;  Toolkit = same modules headless
```
## 5. Reconstruction
Single-process modular NetBeans app; graph held in JVM heap with attribute tables; parallel-stream iterators added in 0.11.1 [CLAIM-gephi-01]. No persistence beyond project files, no server, no auth. Internals public (GPL); detailed code not read here.

## 6. Requirements inferred
Layout algorithms must be reusable headless; static snapshots exported with provenance.

## 7. Performance
Gephi site: "ten to ten million nodes" (vendor/project claim); wiki: "up to a million elements" (does not say nodes vs edges); release notes give no benchmarks [CLAIM-gephi-02]. Heap-bound; no independent number retrieved. Contradiction between the two claims noted, confidence low (0.4).

## 8. Strengths
Gold-standard exploratory analytics UX for static networks; ForceAtlas2 origin; free; Toolkit lets servers batch-render. STR-gephi-01: ForceAtlas2/modularity pipeline as reusable layout/community service. STR-gephi-02: rich statistics panel.

## 9. Limitations
| Class | Item |
|---|---|
| Operational | requires JDK 17 to run; desktop-only; GPU/OpenGL support issues addressed with a 0.11.2 error dialog |
| Friction | single-user, no live data, no tenancy |
| Licensing | GPL-3 (CDDL option per wiki): copyleft, cannot be linked into a proprietary distributed product without legal review |
| Maturity | slow major cadence (0.10.1 2023 -> 0.11.1 2026) |

## 10. Deployment and licensing
Desktop and Toolkit; air-gap viable; **GPL/CDDL legal-review trigger**. Toolkit licensing not independently checked.

## 11. Delta vs baseline
BL-54: EOIP's UI is multi-tenant web with live API; lacks Gephi-grade built-in statistics/partition styling in the canvas (not audited).

## 12. Cards and seed hypothesis
**Seed §10.5 verdict: PARTIALLY VALIDATED.** The seed says "client-side, static, single-user". Evidence: client-side yes, single-user yes, no tenancy/permissions yes; "static" is too strong: dynamic networks exist and the Toolkit runs server-side; no live permissioned data is verified. "Poor at very large" is unproven: the project claims up to a million elements (or ten million nodes), no independent test. The EOIP remedy (server-side aggregation, progressive disclosure, GPU, permission-filtered views, time-machine) is a sound differentiator, but Gephi is not a competitor to a platform UI; treat as capability reference.
INV-gephi-01 | target Gephi 0.11.3 desktop; limitation: no live permission-filtered views; cause: single-process desktop data model (proven); alternative: server-side permission-correct subgraph + export to Gephi (GEXF) for power users; worse when export leaks data; options (a) GEXF/GraphML export endpoint with ACL filter + audit, (b) hosted ForceAtlas2 layout service, (c) Gephi Lite embed; selected (a); POC: export 50k-node subgraph for 3 roles, zero unauthorised nodes; decision ADOPT. STR-gephi-01, 02 as above.

## 13. Decisions
CAP-70 REFERENCE for analytics UX; CAP-62 REUSE ForceAtlas2 via graphology (MIT); export INTEGRATE; Gephi code REJECT as dependency (GPL).

## 14. Tests
Export a synthetic 100k/1M-edge graph to GEXF and open in 0.11.3 on 16 GB; record load time, FPS, heap. Verify licence text of Toolkit and files in each module.

## 15. Risks
GPL contamination if code copied; licence statement inconsistency; website staleness.

## Appendix A
| Dim | Sec | Summary |
|---|---|---|
| D1-D3 | 1-3 | desktop |
| D4,D5 | 4,5 | JVM heap |
| D6,D9,D16,D17 | N/A | none |
| D7,D8 | 7 | vendor claims conflict |
| D10 | 3,9 | none |
| D11,D12,D18 | 10 | GPL |
| D13 | 3 | plugins |
| D14 | 3 | a11y unknown |
| D19,D20 | 1 | active |
| D21-D24 | 9,12,15 | seed verdict |

## Appendix B
| CAP | Tech | CLAIM | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-70 | native desktop | 02 | BL-54 | REFERENCE | P3 |
| CAP-62 | native | 02 | analytics (BL graph algos) | REUSE (graphology port) | P2 |
| CAP-73 | partial | 02 | absent | BUILD | P2 |

## Appendix C
| CLAIM | prod/ver/date | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-gephi-01 | 0.11.1-0.11.3, 2026-05..09 | rewritten OpenGL engine; releases | verified | github.com/gephi/gephi releases | 2026-09-06 / 10-26 | 0.9 | none |
| CLAIM-gephi-02 | site/wiki | scale claims; licences | vendor | gephi.org; github wiki; LICENSE.md (GPLv3) | / 10-26 | 0.6 | conflicting claims |
| CLAIM-gephi-03 | site | 0.11 described as beta | stale claim | gephi.org | 2026 / 10-26 | 0.7 | GitHub shows release |

## Appendix D
CDDL half taken from the wiki page only. Gephi Lite scope not examined.
