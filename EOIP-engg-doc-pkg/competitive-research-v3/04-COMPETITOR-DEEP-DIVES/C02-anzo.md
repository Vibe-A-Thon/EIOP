# C02 Altair Graph Studio / Anzo / AnzoGraph (now Siemens RapidMiner Graph Studio + Graph Lakehouse)

| Field | Value |
|---|---|
| Registry ID | T-C02-anzo |
| Tier | B (enterprise KG platform; ownership change verified) |
| Versions examined | Graph Studio 2026.0 / 2026.0.1 (engine version 6.2, no dates on page); Graph Lakehouse 2026.0, "Database Version 3.3"; legacy AnzoGraph DB v2.1-v3.1 docs; Graph Studio 5.4 (2024) architecture page |
| Verified on | 2026-10-26 (brief 2026-10-18) |
| Worker | V16 (registry W09) |

## 1. Identity, status, ownership, naming (trap resolved)
Chain of custody: Cambridge Semantics (Boston; products Anzo = platform, AnzoGraph DB = engine) was acquired by Altair, announced 2024-04-12, to be integrated with Altair RapidMiner [CLAIM-anzo-01]. Siemens completed its acquisition of Altair on 2025-03-26 (about USD 10B enterprise value) [CLAIM-anzo-02]. Naming now: Altair's docs call the platform **Altair Graph Studio** (formerly Anzo) and the engine **Altair Graph Lakehouse** (formerly AnzoGraph DB), also sold standalone [CLAIM-anzo-03,04]. Altair's product URL now redirects to a Siemens page titled "Rapidminer Graph Studio", part of Siemens Digital Industries Software and "Intelligence Center X", with no mention of Altair [CLAIM-anzo-05]. So the registry name has three live forms: Anzo/AnzoGraph (legacy), Altair Graph Studio/Lakehouse (docs), Siemens RapidMiner Graph Studio (marketing). Status: active, proprietary. Cross-ref: `C02-stardog.md`, `C02-ontotext-graphdb.md`, `C07` work-graph platforms (Siemens).

## 2. Problem and workloads
Data-fabric/knowledge-graph layer over enterprise sources: onboard structured data, model with ontologies, build "Graphmarts" (layered, activatable analytic graphs), virtualise or load into in-memory MPP engine for graph OLAP, serve dashboards, LLM/Copilot features [CLAIM-anzo-03,05,06].

## 3. Feature inventory
| Feature | Status | CLAIM |
|---|---|---|
| In-memory MPP graph engine (shards data, parallel load/query) | present | 05,07 |
| SPARQL 1.1 plus extensions (window aggregates, named queries, RDFS+ inferencing, RDF-star LPG) | present (legacy docs) | 08 |
| Cypher over Bolt | present in legacy AnzoGraph docs; not on Siemens page | 08 |
| OWL, SHACL listed as supported standards | marketing; depth NOT PUBLICLY VERIFIED | 05 |
| Virtualisation / in-memory / on-disk modes | present | 05 |
| Kubernetes-native Graphmarts on AWS/Azure/GCP; K8s 1.33 compat | present | 05,06 |
| RBAC, lineage, auditing; layer/graph-level security | present | 05 |
| ABAC (access, masking, row-level policies) | experimental in 2026.0; Immuta integration experimental | 06 |
| LLM connections with ACLs, Copilot, ontology-improvement service | present | 06 |
| Query explain-plan viewer | present (2026.0.1) | 06 |
| RDF 1.2 / SPARQL 1.2 | not found | UNKNOWN |
| Open-source edition | absent (legacy free edition up to 16 GB reported) | 08 |

## 4. Architecture
```
 sources --(GDI ingest/virtualise)--> Anzo / Graph Studio server (catalog, ontologies, Graphmart layers, Elasticsearch, LLM connections)
        |  dynamically provisioned pods (Kubernetes)
        v
 Graph Lakehouse cluster: leader (parse, plan, code-gen) -> stream to all nodes -> per-core slices -> results to leader
        data hashed on subject across slices; all in memory; disk persistence [details not published in page read]
```

## 5. Reconstruction
Verified (legacy architecture page): leader parses/plans each query; code generator packages the plan as a stream sent to all nodes; one data slice per core; subject-hash distribution avoids some network shuffles; homogeneous hardware required; all analytic operations run in memory [CLAIM-anzo-07]. Graphmarts as layered, activatable graph sets and the Graph Data Interface for transform are product concepts [CLAIM-anzo-03,06]. Storage encoding, index structure, join algorithms, transaction model, inference algorithm: NOT PUBLICLY VERIFIED. Hypothesis: columnar-style dictionary-encoded triples with MPP hash joins.

## 6. Requirements inferred
Homogeneous cluster sizing, memory proportional to active Graphmarts (the 2026.0 UI shows per-GraphMart memory use [CLAIM-anzo-06]), policy plane that spans graph, layer and masking. EOIP-relevant: ABAC with masking and row-level filters on a graph is arriving as "experimental" at a major vendor, validating priority of BL-18/BL-45-style policy work.

## 7. Performance and resource model
Vendor claims only: "tens of billions of triples in production", trillion-triple benchmark [CLAIM-anzo-05] (workload and hardware not stated here; Unverified, confidence 0.2). No independent benchmark found. Failure modes: RAM-bound; homogeneous cluster; cost of keeping Graphmarts active (hypothesis from per-Graphmart memory display).

## 8. Strengths
Graph OLAP on one cluster (analytics-heavy queries); layered Graphmart model; virtualise-or-materialise choice per source; explain-plan UI; ABAC/masking direction; Kubernetes-native provisioning. Match for EOIP: hybrid virtual/materialised design (seed hypothesis OBDA) and layer-based activation of analytic graphs.

## 9. Limitations
Licensing: proprietary, no OSS edition; OEM/white-label terms NOT PUBLICLY VERIFIED; Siemens now owns line, roadmap and air-gap policy unclear. Operational: in-memory MPP cost, homogeneous nodes. Friction: three product names, doc split between Altair and Siemens, experimental ABAC. Outdated risk: legacy docs describe Cypher and RDFS+; unclear whether still current in 2026.0.

## 10. Deployment, licensing
Kubernetes in customer cloud (AWS/Azure/GCP) per Siemens page; on-prem/air-gapped viability UNKNOWN (docs mention Elasticsearch and K8s; no statement). Licence: "single package, no feature tiers, per-user fees or add-ons" (vendor claim) [CLAIM-anzo-05]. Proprietary -> legal review trigger for any embedding.

## 11. Delta vs baseline
BL-06 has no Anzo adapter; BL-51 federation planner partial vs Graph Lakehouse virtualisation; BL-18/BL-20 absent vs layer/graph security and experimental ABAC; BL-12 optional LLM hook vs LLM connections with ACLs; BL-14 no external vector DB (this product also uses Elasticsearch, not a vector store as read).

## 12. Cards
STR-anzo-01 | Altair/Siemens Graph Studio | Graphmart: layered, activatable analytic graphs with per-layer memory accounting | 03,06 | cost control for live analytics | match | EOIP "analytic view" objects with activate/deactivate and resource quotas per tenant | test: activate/deactivate 5 views, memory returns to baseline, results equal.
STR-anzo-02 | same | ACLs on LLM connections and ABAC masking/row filters | 06 | prevents unauthorised model/data use | match | extend egress policy (BL-45) with per-connection ACL | test: user without grant cannot route prompt to external model.
INV-anzo-01 | Graph Lakehouse 2026.0 | RAM-bound homogeneous MPP; proprietary | root cause: storage/deployment/licensing (architecture proven for legacy engine [CLAIM-anzo-07]) | alternative: disk-based single node (QLever) for most EOIP sizes; worse for heavy interactive analytics across billions of edges | options: (a) integrate as customer-licensed backend (b) use QLever/Oxigraph read replicas (c) native analytics layer | select (b) EXPERIMENT | POC: same analytic query set on QLever vs Fuseki at 100M triples; metric p95 + RAM | decision DEFER (a).

## 13. Capability decisions
CAP-21 virtualise-or-materialise: EXPERIMENT. CAP-62 graph OLAP: REFERENCE. CAP-45 ABAC with masking: BUILD. CAP-61/51 model-connection ACLs: BUILD. CAP-05 MPP scale-out: DEFER. Anzo as backend: DEFER (no air-gap or OEM evidence).

## 14. Tests
PROPOSED: obtain trial docs only (no scraping); confirm air-gap deployment statement with vendor; check SPARQL 1.1 and RDFS+/OWL behaviour on a standard fixture if licensed; confirm Cypher/Bolt status; confirm naming and support contacts post-Siemens.

## 15. Risks, questions
Product lifecycle under Siemens; "Intelligence Center X" packaging; whether Graph Lakehouse standalone licence permits OEM; disk persistence and HA model; RDF 1.2.

## Appendix A. Dimensions
| Dim | Sec | Summary |
|---|---|---|
| D1 | 1,10 | acquisitions, proprietary |
| D2 | 2 | data fabric + graph OLAP |
| D3 | 4 | server + MPP cluster |
| D4 | 5 | in-memory slices; encoding unknown |
| D5 | 3 | OWL/SHACL claimed |
| D6 | 5 | leader code-gen |
| D7 | 3 | RDFS+ legacy |
| D8 | 5,7 | MPP; ACID unknown |
| D9 | 3 | virtualisation |
| D10 | N/A | not found |
| D11 | N/A | not found |
| D12 | 3 | analytics via SPARQL |
| D13 | 3 | Elasticsearch, LLM Copilot |
| D14 | 3 | Copilot (details unread) |
| D15 | 3 | ontologies, bulk delete |
| D16 | 3 | dashboards, explain UI |
| D17 | 3 | REST |
| D18 | 3 | RBAC, ABAC exp. |
| D19 | N/A | not documented |
| D20 | 7 | vendor claims |
| D21 | 10 | proprietary |
| D22 | 3 | RDF/TTL upload |
| D23 | N/A | not reviewed |
| D24 | App C | vendor docs |

## Appendix B. CAP mapping
| CAP | Anzo | CLAIM | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-02 | native | 05 | BL-06 | DEFER | P3 |
| CAP-05 | native MPP | 07 | BL-01 | DEFER | P3 |
| CAP-15 | native | 08 | BL-06 | DEFER | P3 |
| CAP-21 | native | 05 | BL-51 | EXPERIMENT | P2 |
| CAP-45 | partial (experimental ABAC) | 06 | BL-19 | BUILD | P1 |
| CAP-46 | partial | 05,06 | BL-18 absent | BUILD | P0 |
| CAP-51 | partial (LLM ACLs) | 06 | BL-45 | BUILD | P1 |

## Appendix C. Evidence
| CLAIM | version/date | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| anzo-01 | 2024-04-12 | Altair acquires Cambridge Semantics; Altair part of Siemens Digital Industries Software | Officially documented (press release) | https://news.siemens.com/en-us/altair-acquires-cambridge-semantics/ | 2024-04-12 / 2026-10-26 | 0.8 | none |
| anzo-02 | 2025-03-26 | Siemens completed acquisition of Altair (about USD 10B) | Third-party report | https://www.nafems.org/about-us/media/news/industrynews1003/siemens-completes-10-billion-acquisition-of-altair-engineering/ | 2025-03-26 / 2026-10-26 | 0.75 | none |
| anzo-03 | 2026.0 | Graph Studio 2026.0 includes Graph Lakehouse; Lakehouse also standalone; previously AnzoGraph DB | Officially documented | https://help.altair.com/graphstudio/userdoc/Home.htm ; https://help.altair.com/graphlakehouse/userdoc/Home.htm | 2026-10-26 | 0.8 | none |
| anzo-04 | 2025 | Graph Lakehouse formerly AnzoGraph DB | Officially documented | https://2025.help.altair.com/2025.0/graphlakehouse/userdoc/Home.htm | 2026-10-26 | 0.75 | none |
| anzo-05 | current | Siemens "Rapidminer Graph Studio"; in-memory MPP Lakehouse; SPARQL 1.1/RDF/OWL/SHACL; K8s-native; RBAC/lineage; scale claims; no tiers | Officially documented (vendor claims) | https://www.siemens.com/en-us/products/rapidminer/graph-studio/ (via redirect from https://altair.com/altair-graph-studio) | 2026-10-26 | 0.65 | claims unreproduced |
| anzo-06 | 2026.0/2026.0.1 | experimental ABAC, Immuta, LLM-connection ACLs, K8s 1.33, explain-plan viewer, per-Graphmart memory, engine 6.2 | Officially documented | https://2025.help.altair.com/2025.1/graphstudio/userdoc/relnotes/graph-studio-2026-releases.htm | 2026-10-26 | 0.8 | no dates on page |
| anzo-07 | Graph Studio 5.4 (2024) | leader/worker MPP, code-gen stream, per-core slices, subject hash, in-memory, homogeneous hardware | Officially documented | https://2024.help.altair.com/5.4/graphstudio/userdoc/anzograph-architecture.htm | 2026-10-26 | 0.8 | may be superseded |
| anzo-08 | AnzoGraph v2.x-3.1 docs | SPARQL 1.1 + extensions, RDFS+, RDF-star LPG, Cypher via Bolt, free edition 16 GB | Officially documented (archived) | https://docs.cambridgesemantics.com/anzograph/archive/v2.4/userdoc/sparql-rdf-standards.htm | archived / 2026-10-26 | 0.5 | Siemens page omits Cypher |

## Appendix D. Assumptions
Treated all three names as one product line. Legacy docs used for engine internals; may not match 2026.0.
