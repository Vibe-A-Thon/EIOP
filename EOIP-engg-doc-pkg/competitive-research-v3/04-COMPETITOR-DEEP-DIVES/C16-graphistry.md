| Field | Value |
|---|---|
| Registry ID | T-C16-graphistry |
| Tier | B (GPU visual analytics) |
| Versions examined | PyGraphistry 0.61.2 (PyPI latest, BSD licence field; upload date UNVERIFIED); Graphistry server version UNVERIFIED |
| Verified on | 2026-10-26 |
| Worker | V30 |

## 1. Identity and status
Graphistry, Inc.: GPU-accelerated visual graph analytics platform. Components: Graphistry server (Hub SaaS or self-hosted; proprietary, EULA), open-source **PyGraphistry** (Python client, BSD classifier), graphistry-js, graph-app-kit (Streamlit), and Louie.ai (genAI analytics product) [CLAIM-gph-01, 02]. Active.

## 2. Problem and workflows
Security, fraud and operations teams load events/edges from Pandas, RAPIDS cuDF, Spark or notebooks and explore millions of edges interactively; typical flow: notebook -> `g.plot()` -> shareable server-rendered view with filters, clustering, GPU layout.

## 3. Features
| Feature | Status |
|---|---|
| GPU client/cloud rendering ("100X" vendor claim) | present |
| RAPIDS/cuGraph GPU analytics mode (optional; CPU Pandas/Arrow works) | present [CLAIM-gph-02] |
| Self-host via Docker/Kubernetes; "air-gapping" claimed on homepage | claimed; docs page lacks air-gap detail |
| Python, JavaScript, Streamlit integrations | present |
| Auth / multi-user | present (details UNVERIFIED) |
| Time-machine, permission filtered views | UNVERIFIED |
| Accessibility | UNVERIFIED |

## 4. Architecture
```
Python/JS client --upload (Arrow)--> Graphistry server (GPU node: layout, clustering, filtering)
   --streamed/rendered state--> browser (thin WebGL client)
optional: RAPIDS cuDF/cuGraph for ETL and algorithms
```
## 5. Reconstruction
Server-side GPU does layout and heavy computation, the browser receives compact state: this is the architecture EOIP's seed ("server-side aggregation, GPU") points toward; details beyond marketing/doc pages not verifiable (hypothesis). Data leaves the browser to the Graphistry server: tenancy depends on the server's workspace model (UNVERIFIED).

## 6. Requirements inferred
GPU node optional but required for headline scale; Arrow transport; workspace-level sharing.

## 7. Performance
Vendor: "millions of edges" interactive; "100X+ speedups" with RAPIDS; demo of 80,000+ Facebook friendships; no hardware or datasets stated [CLAIM-gph-02]. No independent benchmark located.

## 8. Strengths
Server-side GPU keeps the client thin and limits data shipped; strong notebook workflow; open client. STR-gph-01: server-side layout/aggregation delivering a thin client for million-edge graphs (CAP-70). STR-gph-02: notebook-to-share workflow for analysts.

## 9. Limitations
| Class | Item |
|---|---|
| Operational | GPU hardware for headline scale; one-node-first conflict |
| Friction | server is proprietary EULA; Hub is SaaS (egress) |
| Licensing | server redistribution/OEM NOT PUBLICLY VERIFIED |
| Evidence | claims lack methodology |

## 10. Deployment and licensing
Self-hosted Docker/Kubernetes possible; air-gap claimed (homepage), not confirmed in docs page. PyGraphistry licence "BSD" in PyPI metadata (variant UNVERIFIED). Server EULA: legal review trigger. Embedding in a white-label product: not a documented option.

## 11. Delta vs baseline
BL-54: browser-only rendering; EOIP has no GPU server tier and no server-side layout service; large-graph performance unmeasured.

## 12. Cards
STR-gph-01/02 above. INV-gph-01 | target Graphistry server; limitation: GPU-mandatory and proprietary for scale; cause: architecture/licensing (proven by stated GPU optionality only partly); alternatives: CPU server-side layout (graphology ForceAtlas2 in worker), cosmos.gl client GPU layout (MIT), optional RAPIDS plugin; worse when graph > client memory; options (a) interop export to Graphistry, (b) server-side CPU aggregation + tile API, (c) optional GPU worker; selected (b) then (c); POC: 1M-edge graph, 500 ms to first meaningful view at 5k visible nodes on CPU-only node; decision EXPERIMENT.

## 13. Decisions
CAP-70 EXPERIMENT (server-side tier); PyGraphistry INTEGRATE (optional export); server REJECT as dependency.

## 14. Tests
Trial Graphistry Hub-equivalent self-hosted image: 1M edges, measure load/FPS; capture network egress; verify air-gap start with no outbound DNS.

## 15. Risks
Claims unverified; GPU cost; data leaving app boundary.

## Appendix A
| Dim | Sec | Summary |
|---|---|---|
| D1-D3 | 1-3 | platform |
| D4,D5 | 4,5 | server GPU |
| D6,D9 | N/A | no store of record |
| D7,D8 | 7 | vendor |
| D10 | 5 | unverified |
| D11,D12,D18 | 9,10 | EULA |
| D13,D21 | 3 | RAPIDS |
| D14 | 3 | unknown |
| D15-D17 | 3 | Louie.ai |
| D19-D24 | 1,9,15 | see |

## Appendix B
| CAP | Tech | CLAIM | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-70 | native (server GPU) | 02 | BL-54 | EXPERIMENT | P1 |
| CAP-62 | plugin (RAPIDS) | 02 | partial | DEFER | P3 |
| CAP-52 | n/a | 01 | n/a | REJECT | P3 |

## Appendix C
| CLAIM | prod/ver/date | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-gph-01 | site | GPU platform, Docker/AWS/Azure/air-gap, EULA | vendor | graphistry.com | / 10-26 | 0.6 | docs page silent on air-gap |
| CLAIM-gph-02 | PyGraphistry 0.61.2 | components, scale claims, self-host links, BSD (PyPI) | vendor + registry | github.com/graphistry/pygraphistry README; pypi.org/project/graphistry | / 10-26 | 0.6 | no benchmarks |

## Appendix D
Release date of 0.61.2 not retrieved. Server version unknown.
