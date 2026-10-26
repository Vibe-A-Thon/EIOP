| Field | Value |
|---|---|
| Registry ID | T-C07-sap-knowledge-graph |
| Tier | B (shipped-vs-announced check; ERP-semantics competitor) |
| Versions examined | SAP HANA Cloud Q2 2026 release (per SAP Developer News 2026-07-03, secondary); Business Data Cloud (BDC) as described by BARC 2026 |
| Verified on | 2026-10-26 (brief says 2026-10-18; actual access date used) |
| Worker | V19 |

## 1. Identity, current status, tier, sources
"SAP knowledge graph" is three things; the registry means (a) **SAP HANA Cloud Knowledge Graph Engine** (RDF/OWL/SPARQL engine inside HANA Cloud), as consumed by (b) **SAP Business Data Cloud** (data products + semantics) and (c) **Joule/Joule Studio agents**. Ownership: SAP SE, proprietary, managed cloud only. [CLAIM-sap-01..05]

**Shipped vs announced (trap resolved):** Engine exists and is documented as a HANA Cloud component (shipped; documentation exists). A Q2 2026 release note says it gained property-graph transformation and automatic KG generation from metadata (secondary source, video transcript). An Early Adopter Care programme for the engine is advertised, and BARC states the end-to-end graph-BDC-BTP vision is "still under development" and gives no GA date. **GA status of the KG engine: NOT PUBLICLY VERIFIED.** Joule agents "intended to draw on" the graph: announced, not confirmed live. Confidence 0.45.

## 2. Problem, workloads, example workflows
Give SAP business objects (orders, materials, suppliers) shared semantics so agents/NL queries ground on business meaning. Examples: NL question over S/4 + non-SAP data in BDC resolved through a KG of data-product metadata; GraphRAG over HANA vectors + triples. Fit for EOIP: customers that run SAP; not a general KG.

## 3. Feature inventory
| Feature | Status | Note |
|---|---|---|
| RDF triple store, OWL modelling | present (docs) | CLAIM-sap-02 |
| SPARQL query + Update endpoint | present | CLAIM-sap-02 |
| Load Turtle/RDF-XML/N-Triples/JSON-LD via REST | present | |
| Graph algorithms (path, community, centrality) | present (page); relation to RDF store unclear | |
| Cypher/PGQL listed | listed, unexplained | UNVERIFIED |
| Property-graph transform | announced/Q2 2026 release (secondary) | CLAIM-sap-03 |
| Auto KG from metadata | announced/Q2 2026 (secondary) | CLAIM-sap-03 |
| Vector + KG GraphRAG | marketed; page silent | UNVERIFIED |
| Inference/reasoning, named graphs | not documented on page read | UNVERIFIED |
| Self-hosted/air-gap | absent (managed service) | |

## 4. Architecture diagram
```
S/4, SuccessFactors, non-SAP -> BDC data products (Datasphere/Databricks) -> HANA Cloud
   HANA Cloud: relational | vector | text | spatial | PG graph | KG engine (RDF/SPARQL, in-memory)
   Joule / Joule Studio agents -> NL -> (SQL | SPARQL | vector) -> grounded answer
Control plane: SAP BTP / HANA Cloud Central (managed only)
```
(Hypothesis from product pages; internal layout not public.)

## 5. Under-the-hood reconstruction
Public evidence only: in-memory engine, RDF/OWL data model, SPARQL 1.1 endpoint, REST bulk loader, SQL extensions/JS client/OData for integration [CLAIM-sap-02]. Storage layout, join strategy, inference engine, transaction semantics, partitioning: **NOT PUBLICLY VERIFIED**. Hypothesis: triple tables in HANA column store with dictionary encoding (typical for HANA multi-model) — unverified. Security inherits HANA roles; source-ACL propagation from SAP apps into KG answers is not documented.

## 6. Inferred requirements
FR: ingest metadata/semantics from business-data products; SPARQL + SQL joint queries; NL grounding. NFR: managed-service SLA; HANA licence. For EOIP: an ERP-metadata connector emitting SourceEvents (BL-23) and mapping SAP semantics via CML (BL-33).

## 7. Performance and resource model
No benchmarks found. HANA is in-memory so memory cost is the dominant resource (inference). Scaling/failure modes NOT PUBLICLY VERIFIED. No numbers given.

## 8. Strengths
SAP semantic depth (CDS views, data products) and customer base; one database for vector+graph+relational joins. Match: EOIP federation (BL-51) + mapping; exceed via backend neutrality and air-gap.

## 9. Limitations
Intentional trade-off: SAP-cloud lock-in, no self-host. Licensing: proprietary, consumption-priced (not verified). Maturity: GA unverified; early-adopter programme. Friction: needs HANA Cloud instance with triple store enabled [CLAIM-sap-02]. Hypothesis: knowledge value depends on customers adopting BDC.

## 10. Deployment/licensing/viability
SaaS only; fails EOIP air-gap and no-mandatory-cloud constraints. Legal-review trigger: proprietary SaaS terms; OEM not offered. Air-gap: no.

## 11. Competitive delta (baseline)
EOIP has Fuseki/GraphDB RDF adapters (BL-06, partial), SHACL subset (BL-29), OWL subset (BL-30), mapping (BL-33). SAP gap in EOIP: no SAP semantic catalogue connector. EOIP advantage: ACL-aware governance is still **Absent** (BL-18), so no claim to win on permissions yet.

## 12. Strength and inversion cards
STR-sap-01 | SAP | Business-semantics KG over enterprise data products | CLAIM-sap-01,04 | value: ERP-grounded NL answers | integrate | SAP metadata connector -> SourceEvent -> CML | test: 100 SAP data-product definitions mapped with zero direct graph writes.
INV-sap-01 | HANA Cloud KG | Managed-only; no air-gap | CLAIM-sap-02 | root cause: deployment (proven for managed-service framing) | alt: local multi-backend store; worse when customer is all-SAP and cloud-ready | options: (1) export SAP metadata as RDF to Fuseki, (2) native SAP-metadata CML pack, (3) bidirectional BDC sync | selected: 2 | POC: map 200 CDS-view definitions, success = >95% field mapping round trip; defensibility: air-gap + ACL; decision EXPERIMENT. No seed hypothesis from §10.5 targets this entry.

## 13. Per-capability decisions
CAP-02/15 RDF/SPARQL: REUSE existing adapters. CAP-26 connectors: BUILD SAP metadata connector (DEFER until customer demand). CAP-56 GraphRAG: REFERENCE only. CAP-50 air-gap: EOIP advantage. CAP-42 catalog: INTEGRATE BDC catalog export.

## 14. Tests and POC
(1) Ingest a public SAP CDS/OData metadata sample, map to ontology; (2) check SourceEvent-only writes; (3) verify trial instance GA status before positioning claims.

## 15. Risks and open questions
GA date, inference support, pricing, SAP API terms for metadata export; whether SAP ships a KG outside BDC.

## Appendix A — Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | SAP SE, proprietary, GA unverified |
| D2 | 2 | ERP-grounded agents |
| D3 | 4 | managed, HANA multi-model |
| D4 | 5 | not public |
| D5 | 3,5 | RDF/OWL; SHACL not documented |
| D6 | 3 | SPARQL; planner not public |
| D7 | 5 | inference not documented |
| D8 | 7 | not public |
| D9 | 3,6 | REST/streaming load |
| D10 | 5 | not public |
| D11 | N/A | no evidence |
| D12 | 3 | built-in algorithms |
| D13 | 3 | GraphRAG marketed only |
| D14 | 3 | NL over data announced |
| D15 | N/A | not public |
| D16 | N/A | not examined |
| D17 | 3 | SQL, OData, JS API |
| D18 | 5 | HANA roles; ACL propagation unknown |
| D19 | N/A | managed by BTP; not examined |
| D20 | 7 | no figures |
| D21 | 9,10 | proprietary consumption |
| D22 | 9,13 | RDF export formats |
| D23 | N/A | not examined |
| D24 | 1 | secondary sources, low confidence |

## Appendix B — Capability mapping
| CAP | Technology | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-02 | native | sap-02 | BL-06 partial | REUSE | P2 |
| CAP-15 | native | sap-02 | BL-06 partial | REUSE | P2 |
| CAP-28 | partial (auto KG, announced) | sap-03 | BL-26 | EXPERIMENT | P3 |
| CAP-42 | native via BDC | sap-04 | none | INTEGRATE | P3 |
| CAP-56 | unknown | sap-05 | BL-16 | DEFER | P3 |
| CAP-50 | absent | sap-02 | yes | EOIP advantage | P1 |

## Appendix C — Evidence records
| CLAIM | product/version/date | claim | class | source | pub/access | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| sap-01 | BDC, 2026 | KG adds a technical base component to BDC architecture | Third-party report | BARC, SAP Data & Analytics 2026, https://barc.com/sap-data-analytics-2026/ | 2026 / 2026-10-26 | 0.6 | none |
| sap-02 | HANA Cloud KG | RDF/OWL, SPARQL+Update, REST load, requires triple-store-enabled instance | Officially documented | SAP Learning, https://learning.sap.com/courses/data-engineer-sap-hana/sap-hana-cloud-knowledge-graph-engine-1 ; LangChain SAP HANA RDF docs https://docs.langchain.com/oss/python/integrations/graphs/sap_hana_rdf_graph.md | n/d / 2026-10-26 | 0.7 | Cypher/PGQL listing unexplained |
| sap-03 | HANA Cloud Q2 2026 | KG to property-graph, auto-generation from metadata | Third-party report (transcript) | SAP Developer News 3 Jul 2026, https://community.sap.com/t5/developer-news/sap-developer-new-july-3rd-2026/ba-p/14432288 | 2026-07-03 / 2026-10-26 | 0.4 | not in release notes (unchecked) |
| sap-04 | SAP Datasphere preview | KG was preview in 2024 | Officially documented | https://news.sap.com/2024/03/latest-sap-data-and-analytics-innovations-sap-data-unleashed/ | 2024-03 / 2026-10-26 | 0.5 | |
| sap-05 | Joule 2025-26 | Joule agents intended to use KG; end-to-end vision under development | Third-party report | BARC (as sap-01) | 2026 / 2026-10-26 | 0.5 | |

## Appendix D — Assumptions
"SAP knowledge graph" = HANA Cloud KG engine + BDC usage. Q2 2026 claims treated as unconfirmed. No cross-duplication with C07-servicenow-kg, C07-microsoft-graph-copilot-fabric (similar managed-enterprise-graph pattern).
