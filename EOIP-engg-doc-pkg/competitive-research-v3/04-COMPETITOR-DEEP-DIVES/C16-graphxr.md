| Field | Value |
|---|---|
| Registry ID | T-C16-graphxr |
| Tier | B (visual analytics product) |
| Versions examined | Kineviz GraphXR (marketing page; help docs referenced as "v3"); exact version and release date UNVERIFIED |
| Verified on | 2026-10-26 |
| Worker | V30 |

## 1. Identity and status
Kineviz (company site now brands the product line "Kineviz"; GraphXR is its browser-based graph analytics platform; SeekerXR listed as a separate product) [CLAIM-gxr-01]. Status: commercial, apparently active; no public version/date located (confidence 0.3). Complete product, not a library.

## 2. Problem and workflows
Analysts load graph DB / relational / CSV / JSON / API data, extract entities with AI assistance, build graphs with Graph Composer transforms (extract, shortcut, link, merge), then explore in 3D/2D with geospatial, time-series and social-network views; path finding, centrality, community detection.

## 3. Features
| Feature | Status |
|---|---|
| Browser-based, no install | present |
| 3D immersive scatter/graph views | present; VR NOT confirmed |
| Graph Composer (visual transforms) | present |
| AI-assisted entity/relationship extraction | present (model/egress policy UNVERIFIED) |
| Geospatial, time-series views | present |
| Algorithms: path, centrality, community | present |
| Data sources: Neo4j, relational, CSV/JSON, APIs; BigQuery and Spanner solution pages | present |
| Deployment: on-prem, private cloud, air-gapped | claimed [CLAIM-gxr-01] |
| Public pricing/licence/scale | NOT PUBLICLY VERIFIED |

## 4. Architecture
```
sources -> import/ETL (Graph Composer, AI extraction) -> project graph store (UNVERIFIED)
  -> browser WebGL 3D/2D views -> analytics (path/centrality/community) -> dashboards
```
## 5. Reconstruction
Not verifiable from public pages. Hypotheses: WebGL client over a server-side workspace store; extraction via LLM service; connectors read-only for imports. Do not rely.

## 6. Requirements inferred
Visual data-prep step that produces an explicit graph from tables (aligns with EOIP's rule that connectors never mutate the graph directly: transforms should yield proposals).

## 7. Performance
No scale claims published [CLAIM-gxr-01]; no independent evidence. Unknown.

## 8. Strengths
Table-to-graph visual composer; 3D and multi-view (geo/time) exploration in one tool; air-gap option claimed. STR-gxr-01: visual transforms (extract/shortcut/link/merge) as an ingestion-mapping UX (CAP-28/29). STR-gxr-02: coordinated geo/time views.

## 9. Limitations
| Class | Item |
|---|---|
| Licensing | terms/pricing not public; redistribution unknown |
| Friction | proprietary; 3D navigation learnability (hypothesis) |
| Evidence gap | no scale numbers, no version |

## 10. Deployment and licensing
Vendor claims on-prem/private cloud/air-gapped. Closed product; no OEM terms found. Legal-review: yes if integration or bundling considered; integration only as an external tool.

## 11. Delta vs baseline
BL-54 lacks coordinated geo/time/3D views and a visual graph-composer; BL-52 streaming and BL-37 bitemporal give EOIP data for time views.

## 12. Cards
STR-gxr-01/02 above. INV-gxr-01 | target GraphXR (unversioned); limitation: transforms act on a project copy, not governed graph; cause: governance (hypothesis); alternative: visual composer producing reviewable change proposals into EOIP ontology/gitops; options (a) none, (b) mapping UI over R2RML-like mapping, (c) AI-suggested transforms with proof; selected (b); POC: 3 CSVs to graph in <15 min with diffable mapping; decision EXPERIMENT.

## 13. Decisions
CAP-28/29 EXPERIMENT (UX); CAP-70 DEFER; product INTEGRATE not recommended; time/geo views BUILD.

## 14. Tests
Request evaluation licence; test import of 3 CSVs, air-gapped install, 100k-node scene, egress traffic capture of AI extraction.

## 15. Risks
Closed evidence base; claims not verifiable; naming change risk (Kineviz vs GraphXR).

## Appendix A
| Dim | Sec | Summary |
|---|---|---|
| D1-D3 | 1-3 | product |
| D4,D5 | 4,5 | hypothesis only |
| D6-D9 | 7 | unknown |
| D10 | 3 | unknown |
| D11,D12,D18 | 9,10 | not public |
| D13,D21 | 3 | connectors |
| D14 | 3 | 3D |
| D15-D17 | N/A / 3 | AI extraction unverified |
| D19-D24 | 1,9,15 | thin evidence |

## Appendix B
| CAP | Tech | CLAIM | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-28 | partial | 01 | BL ingestion (see baseline) | EXPERIMENT | P2 |
| CAP-71 | native | 01 | BL-54 | EXPERIMENT | P2 |
| CAP-73 | partial | 01 | absent | BUILD | P2 |

## Appendix C
| CLAIM | prod/ver/date | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-gxr-01 | GraphXR, version n/d | features, deployment options, no scale/pricing stated | vendor | kineviz.com/graphxr | / 10-26 | 0.5 | none |

## Appendix D
Only one source page read (Tier B budget 3-6 not met): verification gap. Confidence capped at 0.5.
