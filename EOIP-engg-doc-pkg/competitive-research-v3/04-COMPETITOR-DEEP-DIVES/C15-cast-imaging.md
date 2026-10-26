# C15 - CAST Imaging

| Field | Value |
|---|---|
| Registry ID | T-C15-cast-imaging |
| Tier | B - enterprise architecture / dependency graph over legacy and polyglot estates; closest commercial analogue to the digital-thread code layer |
| Versions examined | CAST Imaging V3 documentation (undated landing page); Docker install guide mentions `3.6.4-funcrel`; exact current release NOT PUBLICLY VERIFIED |
| Verified on | 2026-10-26 (brief date 2026-10-18) |
| Worker | V29 |

## 1. Identity, status, tier, sources

| Item | Finding | Claim |
|---|---|---|
| What | CAST Software's application intelligence product: reverse-engineers source and DB code into a navigable architecture/dependency model ("MRI for software") | [CLAIM-cast-01] |
| Owner | CAST (CAST Software), proprietary | [CLAIM-cast-01] |
| Activity | Docs live with Kubernetes, multi-machine Docker, viewer-only layouts; MCP Server and API reference sections exist | [CLAIM-cast-02] |
| Licence | Commercial, per application per year; one third-party listing: from $10,200 per application per year, on-premises with MCP server (G2, unverified) | [CLAIM-cast-03] |
| Related | CAST Highlight (portfolio SaaS) and "Imaging Express" (managed SaaS on AWS Marketplace, analysis stays in customer environment) are different offerings | [CLAIM-cast-03] |
| Name collision | none; keep separate from Highlight | |

## 2. Problem and workloads

Modernisation and risk: understand unknown legacy (COBOL, JCL, CICS, Java/JEE, .NET, ABAP, RDBMS), find transactions end to end (UI to DB), impact before change, quality/security/cloud-readiness metrics. Workflow: register application, deliver source, analyse, explore in Viewer, produce reports/dashboards, query via API/MCP [CLAIM-cast-02]. Technology list (third-party): Java/JEE, .NET, COBOL, JCL, CICS, ABAP, Oracle Forms, PeopleSoft, Go, Python, C/C++, NoSQL [CLAIM-cast-03]; CAST's site cites "450+ languages, frameworks & DBs" for its dataset, not specifically Imaging [CLAIM-cast-01].

## 3. Feature inventory

| Feature | Status |
|---|---|
| Application / transaction / data-call-graph views | present (names from docs structure; detail UNVERIFIED) |
| Cross-technology links (code to SQL objects, messaging, UI) | present (vendor) |
| Impact analysis upstream/downstream | present (reviews, news) |
| Architecture checks, quality/security/modernisation assessment | present |
| AI assistance / GraphRAG service | present (viewer component list) |
| MCP server, REST API | present |
| Dashboards (management, engineering, security) | present |
| Git-history lineage, Jira/incident link | NOT PUBLICLY VERIFIED |
| Source ACLs on results | NOT PUBLICLY VERIFIED |

## 4. Architecture

```
source delivery -> analysis-node (static analysers, extensions)
   -> imaging-viewer: ETL -> Neo4j (graph) + API + AI/GraphRAG service
imaging-services: gateway, console, auth/SSO, control panel, embedded PostgreSQL
dashboards: management/engineering/security
```
Component groups per Docker multi-machine guide; Neo4j can sit on a dedicated host [CLAIM-cast-04].

## 5. Under-the-hood reconstruction

Data model: property graph of objects (programs, classes, tables, files), links (call, read/write, inherit), and transactions as ordered paths; stored in Neo4j after ETL from the analysis result database (PostgreSQL) [CLAIM-cast-04]. Analysis pipeline: delivery -> per-technology analysers produce an object/link model -> cross-technology link resolution -> ETL to Neo4j -> viewer queries (Cypher inferred). Concurrency: multiple analysis nodes, one viewer graph. Neo4j heap and transaction memory default 12 GB each [CLAIM-cast-04]. Security: SSO/auth service, user and licence management documented; per-object ACL NOT PUBLICLY VERIFIED. Analysis algorithms are proprietary: NOT PUBLICLY VERIFIED; everything above on resolution is hypothesis.

## 6. Inferred requirements

Batch whole-application analysis with explicit delivery; cross-technology link resolution; transaction-path abstraction; separate analysis and viewer scaling; air-gap image export/import.

## 7. Performance and resource model

Single-machine Docker is positioned for POC/small production, multi-machine for production [CLAIM-cast-04]. Neo4j defaults 12 GB heap plus 12 GB transaction memory (documented). No latency/throughput benchmark found. Failure modes: Neo4j sizing, re-analysis cost for each delivery (batch, not incremental - hypothesis).

## 8. Strengths

STR-cast-01 transaction (UI to DB) paths as first-class objects. STR-cast-02 breadth incl. mainframe/COBOL/SQL objects. STR-cast-03 on-prem/air-gap packaging with documented image export/import and Kubernetes Helm. STR-cast-04 MCP server exposing architecture to agents.

## 9. Limitations

| Class | Finding |
|---|---|
| Algorithmic | batch analysis per delivery; freshness lags (hypothesis) |
| Operational | Neo4j dependence, 12 GB defaults, multi-container install |
| Friction | per-application pricing, onboarding steps (profile, register, deliver) |
| Licensing | proprietary, not redistributable or embeddable under white-label (OEM terms NOT PUBLICLY VERIFIED) |
| Evidence | most feature claims from vendor/reseller pages |

## 10. Deployment, licensing, viability

On-prem Docker/Kubernetes, air-gap image procedure documented [CLAIM-cast-04]. Proprietary: legal review before any bundling; realistic role is customer-owned side system whose export is ingested, not an OEM dependency.

## 11. Delta vs EOIP

| Area | CAST Imaging | EOIP |
|---|---|---|
| Technologies | legacy+modern, DB objects | BL-42 Python/TS only |
| Transaction paths | first-class | `polyglot_linker.py` Partial |
| Graph store | Neo4j fixed | BL-01 backend-neutral |
| Cross-source thread | code-centric | BL-41 lineage, Jira/ITSM connectors (BL-23) |
| Permissions | NOT PUBLICLY VERIFIED | BL-18 Partial |
| Incrementality | batch | BL-42 incremental indexer |

## 12. Cards

| ID | Card |
|---|---|
| STR-cast-01 | [CLAIM-cast-02] transaction path object; value: "which class caused an incident" starting point; **match**: derive transaction paths from route-to-DB edges; test: fixture with controller->service->SQL yields one named path |
| STR-cast-04 | [CLAIM-cast-02] MCP over architecture graph; **match** via BL-47 with ACL filter |
| INV-cast-01 | Target CAST Imaging V3, whole-app batch analysis, Neo4j-bound. Limitation: freshness and backend lock [CLAIM-cast-04]; cause deployment/storage (hypothesis for batch). Options: (a) ingest CAST exports as a SourceEvent connector; (b) native incremental graph; (c) both with provenance-tagged confidence. Selected (a) when customer owns CAST, (b) otherwise. Benchmark: edit one file, graph delta reflects within minutes vs full re-analysis. Defensibility: live cross-source thread. Decision EXPERIMENT. |
| INV-cast-02 | Proprietary + per-app pricing blocks OEM [CLAIM-cast-03]; cause licensing. Decision ADOPT (no dependency). No 10.5 seed applies. |

## 13. Decisions

CAP-66: REFERENCE (INTEGRATE as optional connector when customer licensed - EXPERIMENT). CAP-69 impact digital thread: BUILD. CAP-59: REFERENCE. Mainframe breadth: DEFER. Product dependency: REJECT.

## 14. Tests/POC

If a CAST export (API/CSV) is available from a customer: map objects/links into SourceEvents, verify idempotent replay and ACL propagation. Acceptance: re-ingest same export yields zero graph delta.

## 15. Risks

Reverse-engineering temptation: only public docs and customer-authorised exports allowed. Open: export schema stability, MCP tool list, ACL model, Imaging version numbering.

## Appendix A - Dimensions

| Dim | Sec | Summary |
|---|---|---|
| D1 | 1,10 | proprietary, active |
| D2 | 2 | modernisation, impact |
| D3 | 4 | four component groups |
| D4 | 5 | Neo4j + PostgreSQL |
| D5 | 5 | object/link/transaction |
| D6 | 5 | Cypher inferred |
| D7 | N/A | none |
| D8 | 5,7 | multi-node analysis |
| D9 | 5 | batch delivery |
| D10 | 5 | NOT PUBLICLY VERIFIED |
| D11 | 9 | per-delivery snapshots, hypothesis |
| D12 | N/A | quality metrics only |
| D13 | 3 | GraphRAG, MCP |
| D14 | 3 | AI assist |
| D15 | N/A | none |
| D16 | 3 | Viewer |
| D17 | 3 | API |
| D18 | 5 | SSO documented |
| D19 | NOT PUBLICLY VERIFIED | domains documented |
| D20 | 7 | sizing only |
| D21 | 1,10 | per-application pricing |
| D22 | 11 | NOT PUBLICLY VERIFIED |
| D23 | N/A | not researched |
| D24 | 5 | doc landing pages + reseller |

## Appendix B - Capabilities

| CAP | Tech | Claim | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-66 | native | 02 | BL-42 | REFERENCE | P2 |
| CAP-69 | native | 02 | BL-41/42 | BUILD | P1 |
| CAP-59 | native | 02 | BL-47 | REFERENCE | P3 |
| CAP-50 | native | 04 | BL-45 | REFERENCE | P3 |

## Appendix C - Evidence

| ID | Product/date | Claim | Class | Source | Dates/conf | Contra |
|---|---|---|---|---|---|---|
| CLAIM-cast-01 | site | product framing, 450+ dataset | Vendor claim | https://www.castsoftware.com/ | 2026-10-26, 0.5 | dataset not Imaging-specific |
| CLAIM-cast-02 | docs landing | sections incl. API, MCP, Viewer, install | Officially documented | https://doc.castsoftware.com/imaging/ | 0.7 | detail pages not read |
| CLAIM-cast-03 | G2/AWS listings | price, technologies, SaaS variant | Third-party report | https://www.g2.com/products/codified/pricing ; AWS Marketplace listing | 0.35 | search-summary only |
| CLAIM-cast-04 | Docker/K8s guides | components, Neo4j, 12 GB, air-gap | Officially documented | https://doc.castsoftware.com/imaging/install/global/docker/multi-machine/all-multi/ | 0.7 | via search summary |

## Appendix D - Assumptions

Neo4j-backed Cypher viewer is inferred from component list. Pricing is third-party and unverified.
