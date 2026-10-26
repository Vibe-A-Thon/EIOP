# C01 — Oracle Graph (PGX / Property Graph, SQL/PGQ)

| Field | Value |
|---|---|
| Registry ID | T-C01-oracle-graph |
| Tier | B — enterprise RDBMS graph incl. ISO SQL/PGQ; proprietary; reference for SQL-bridge strategy |
| Versions examined | Oracle AI Database 26ai (Oracle's rename of 23ai line); Oracle Graph Server and Client 25.4 (release date not on page); 24.1 (earlier); property-graph docs 25.3/25.4 |
| Verified on | 2026-10-26 (actual access date) |
| Worker | V15 (W07 scope) |

## 1. Identity, current status, tier, and sources
Oracle's property graph has three parts: (1) SQL property graphs, `CREATE PROPERTY GRAPH` plus `GRAPH_TABLE` with `MATCH` (ISO SQL/PGQ) inside Oracle AI Database 26ai; (2) Graph Server (PGX, in-memory analytics engine) with PGQL, Java and Python (pypgx) clients, loadable from SQL property graphs; (3) legacy PG views/PGQL-on-RDBMS and RDF Graph [CLAIM-oracle-01, -02]. Graph Server and Client 25.4 "works with Oracle AI Database or earlier Oracle Database versions"; the page lists Oracle Linux 9 support and visualization/APEX plug-in updates [CLAIM-oracle-02]. Oracle describes itself as "among the first commercial products" to support SQL/PGQ [CLAIM-oracle-01]. Owner: Oracle Corporation. Sources: Oracle 26ai New Features Graph page, SPGDG 25.4, Oracle blog posts (one blog returned HTTP 403, so its licensing statement is secondhand), oracle-base.

## 2. Primary problem and workloads
Run graph pattern queries and algorithms on data already in Oracle (fraud, supply chain, ownership, identity) without moving it; avoid a second database [CLAIM-oracle-01]. EOIP-relevant: customer-supplied Oracle estates (ERP/CMDB) queried as a graph; SQL/PGQ as an EOIP query target.

## 3. Feature inventory
| Feature | Status |
|---|---|
| SQL/PGQ DDL and GRAPH_TABLE | Present (26ai) |
| Property graph views over multiple tables, views, aggregates, DB links | Present [CLAIM-oracle-01] |
| JSON collections as graph source (schema-less) | Present |
| In-database algorithms `DBMS_OGA` (e.g. PageRank) | Present |
| `DBMS_AI_GRAPHRAG` graph-augmented RAG | Present (26ai) |
| PGQL via Graph Server and directly on SQL property graphs | Present |
| PGX in-memory algorithms | Present; separate download (Graph Server) |
| Visualization (APEX plug-in, VS Code extension, Graph Studio) | Present |
| RDF graph analytics on Graph Server | Present |
| openCypher / Gremlin / GQL | Not found |
| Edition limits, PGX on Free edition | UNVERIFIED |

## 4. Architecture diagram
```
SQL app --> Oracle AI Database 26ai: optimizer rewrites GRAPH_TABLE -> joins over base tables/views (hypothesis)
Graph Server (PGX): load SQL property graph snapshot -> in-memory CSR-like engine -> algorithms/PGQL
Clients: SQL*Plus/JDBC, pypgx, Java, APEX, VS Code
```

## 5. Under-the-hood reconstruction
Verified: the property graph is a schema-level definition over existing tables/views; graphs inherit database security and manageability; PGX loads a full graph or subgraph into memory [CLAIM-oracle-01, -03]. Hypotheses (0.5): GRAPH_TABLE is expanded by the SQL optimizer into relational joins using existing indexes and cost model; PGX uses compressed adjacency storage with snapshot refresh (no incremental sync verified). Security uses standard grants; row/column policies apply because queries run as SQL (hypothesis, test needed).

## 6. Requirements inferred
FR: graph defined declaratively over relational data; SQL composability with graph results; algorithms reachable from SQL. NFR: transactional consistency with source data, inherited RBAC/VPD, no ETL.

## 7. Performance and resource model
No audited benchmark read; none quoted. In-DB queries share resources with OLTP (noisy-neighbour risk, inference); PGX requires RAM for the loaded snapshot and refresh strategy. Failure modes: stale PGX snapshots, join explosion on deep multi-hop.

## 8. Strengths
Standards-based SQL/PGQ over live data; inherits mature security and backup; graph views over aggregates and DB links. Match: EOIP can emit SQL/PGQ for SQL-based backends (CAP-16).

## 9. Limitations
Licensing: proprietary; PGX Graph Server is a separate product; whether graph features are included in database licence rests on an Oracle blog not directly read [CLAIM-oracle-04, conf 0.4]. Operational: depends on Oracle DB. Semantics: no openCypher/Gremlin found, no ontology reasoning in LPG. Naming churn (23ai -> 26ai, PGQL vs SQL/PGQ) causes docs ambiguity.

## 10. Deployment, licensing, redistribution, operational viability
Self-hosted on customer Oracle; proprietary; cannot be bundled; Oracle Database Free (earlier 23c Developer Release carried SQL property graphs per Oracle) for tests — current Free edition status UNVERIFIED. Legal-review trigger: proprietary database, Graph Server licence terms (OTN vs included). Air-gap: yes (customer-installed).

## 11. Competitive delta vs baseline
BL-59 (SQL/PGQ absent): Oracle is a reference implementation for GRAPH_TABLE. BL-09 transpiler covers Gremlin/Cypher/SPARQL only. BL-01 has no SQL-backed store; BL-51 federation planner could treat Oracle as a virtual source. BL-33 (CML) is not R2RML, unlike Oracle's declarative mapping.

## 12. Strength and inversion cards
STR-oracle-graph-01 | Oracle | SQL/PGQ over existing tables, no ETL | CLAIM-oracle-01 | graph view of ERP/CMDB estates | integrate | emit GRAPH_TABLE from the IR for SQL targets | same 10 queries return identical rows via IR->PGQ and IR->Cypher on a test dataset.
STR-oracle-graph-02 | Oracle | graph inherits DB security | CLAIM-oracle-01 | permission fidelity (BL-18 gap) | match | push source-ACL filters into generated SQL | no row visible that SQL grants deny.
INV-oracle-graph-01 | Oracle 26ai | vendor lock-in: SQL/PGQ portability is claimed, features beyond standard (PGQL, PGX, DBMS_OGA) are proprietary | licensing/semantics, proven by doc naming | alternative: standard SQL/PGQ subset only (worse: loses algorithms) | options: skip / SQL/PGQ-subset target / engine-neutral IR | select subset target | POC: run conformance corpus on Oracle Free vs DuckPGQ vs Spanner, success = identical rows | defensibility: neutrality | decision EXPERIMENT. Seed hypotheses: none apply.

## 13. Per-capability decisions
CAP-16 SQL/PGQ: INTEGRATE (target dialect, EXPERIMENT). CAP-21 virtualisation: INTEGRATE as source. CAP-62: REJECT dependence on DBMS_OGA. CAP-01 store: REJECT as bundled backend. CAP-77: flag.

## 14. Tests and acceptance
Install Oracle Database Free; create property graph over test tables; compare rows to Cypher on a backend; verify VPD/row-level policy applies to GRAPH_TABLE; test PGX load/refresh latency.

## 15. Risks and open questions
Licence of Graph Server; Free-edition scope; SQL/PGQ ISO version supported (ISO/IEC 9075-16:2023 assumed, unverified); performance of deep traversals.

## Appendix A — Research-dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | Oracle, proprietary |
| D2 | 2 | Graph on RDBMS |
| D3 | 4 | DB + Graph Server |
| D4 | 5 | Hypothesis |
| D5 | 3 | View-based schema |
| D6 | 5 | GRAPH_TABLE expansion hypothesis |
| D7 | 3 | RDF graph only; no LPG reasoning |
| D8 | 5 | Inherits DB |
| D9 | 3 | DB links, no ETL |
| D10 | N/A | Not found |
| D11 | N/A | Not found |
| D12 | 3 | Algorithms |
| D13 | 3 | DBMS_AI_GRAPHRAG |
| D14 | N/A | Not found |
| D15 | 3 | APEX, VS Code |
| D16 | 3 | Visualization |
| D17 | 3 | pypgx, JDBC |
| D18 | 5 | Inherited grants |
| D19 | N/A | DB-level only |
| D20 | 7 | No numbers |
| D21 | 10 | Licence unclear |
| D22 | 9, 11 | Standard SQL/PGQ |
| D23 | N/A | Not researched |
| D24 | App. C | Conf per claim |

## Appendix B — Capability mapping
| CAP | Oracle | Claim | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-16 | native | -01 | BL-59 absent | INTEGRATE/EXPERIMENT | P1 |
| CAP-21 | native | -01 | BL-51 partial | INTEGRATE | P2 |
| CAP-62 | native | -01 | BL-43 | REJECT | P3 |
| CAP-56 | native | -01 | BL-16 | DEFER | P3 |
| CAP-45 | inherited | -01 | BL-19 | REFERENCE | P3 |

## Appendix C — Evidence records
| CLAIM-ID | Product/date | Claim | Class | Source | Access | Conf | Contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-oracle-01 | 26ai | SQL/PGQ ISO; property graph views; JSON sources; DBMS_OGA; DBMS_AI_GRAPHRAG; "among the first commercial products" | Officially documented | docs.oracle.com/en/database/oracle/oracle-database/26/nfcoa/graph.html | 2026-10-26 | 0.8 | none |
| CLAIM-oracle-02 | Graph Server 25.4 | Works with 26ai and earlier; OL9 support; viz updates; release date not given | Officially documented | docs.oracle.com/en/database/oracle/property-graph/25.4/spgdg/changes-in-this-release.html | 2026-10-26 | 0.8 | none |
| CLAIM-oracle-03 | SPGDG 25.4 | SQL property graphs created/queried with GRAPH_TABLE; loadable into PGX; PGQL runs on them | Officially documented | .../spgdg/sql-property-graphs.html | 2026-10-26 | 0.8 | none |
| CLAIM-oracle-04 | undated blog | Oracle blog states graph features included with Database licences | Third-party report (search snippet; page 403) | blogs.oracle.com/database/graph-database-and-analytics-for-everyone | 2026-10-26 | 0.4 | no official price list read |

## Appendix D — Assumptions
26ai treated as the current release; ISO standard edition and Free-edition scope unverified; PGX internals are hypotheses.
