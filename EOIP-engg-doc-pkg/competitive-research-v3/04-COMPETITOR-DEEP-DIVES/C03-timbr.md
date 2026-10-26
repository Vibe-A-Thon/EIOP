| Field | Value |
|---|---|
| Registry ID | T-C03-timbr |
| Tier | B (ontology-based semantic layer over SQL) |
| Versions examined | NOT PUBLICLY VERIFIED (no version/date found; docs have no versioning scheme page) |
| Verified on | 2026-10-26 (actual access date) |
| Worker | V13 |

## 1. Identity, current status, tier, and sources
Timbr (timbr.ai) is a commercial ontology-based semantic layer presenting data as a virtual SQL knowledge graph over warehouses/lakes without copying data [CLAIM-timbr-01]. Modelled with four primitives (concepts, properties, relationships, inheritance) in SQL-like DDL (third-party review). Access via SQL (JDBC/ODBC), REST, Python SDK, MCP server [CLAIM-timbr-01]. 40+ sources, 20+ BI tools (third-party analysis). Owner/legal entity, version and release cadence: NOT PUBLICLY VERIFIED. Licence: proprietary; pricing not published in detail (third-party listing shows a starting price of $499/month, unverified, may be stale) [CLAIM-timbr-02]. Tier B: closest commercial analogue for ontology-over-SQL with query rewriting.
Sources: `https://docs.timbr.ai/doc/docs/getting-started/faq`, `https://atlan.com/know/ai-agent/semantic-layer/timbr-semantic-layer/`, Gartner Peer Insights and AWS Marketplace listings.

## 2. Problem, workloads, workflows
Give BI, SQL users and AI agents shared business semantics: define concepts and relationships once, query the graph in SQL, translate to optimised SQL on the source. Workflows: generate a model from a data catalog; add relationships and measures; NL2SQL and GraphRAG agents query the ontology; materialise slow knowledge.

## 3. Feature inventory
| Feature | Status | Evidence |
|---|---|---|
| Virtual ontology over SQL sources, no data copy | present | [CLAIM-timbr-01] |
| SQL access (JDBC/ODBC), REST, Python SDK, MCP | present | [CLAIM-timbr-01] |
| Inference by query rewriting; OWL-DL and some OWL 2 inferences | present (partial) | [CLAIM-timbr-03] |
| Materialisation of slow knowledge | present | [CLAIM-timbr-03] |
| Immediate propagation of ontology changes | present | [CLAIM-timbr-03] |
| Git-like ontology deployment | planned (not shipped per docs) | [CLAIM-timbr-03] |
| NL2SQL, GraphRAG, agents | present as use cases; LLM provider and data flow not stated | [CLAIM-timbr-03] |
| Graph algorithms (networkX, cuGraph mentioned) | partial | [CLAIM-timbr-03] |
| SPARQL / RDF export | unknown | UNVERIFIED |
| Source-ACL pass-through | unknown | UNVERIFIED |
| Self-hosted | present (Docker/Kubernetes, on-prem, VPC) | [CLAIM-timbr-04] |

## 4. Architecture diagram
```
 BI / SQL client / Python / REST / MCP agent
        |  SQL over virtual graph (concept tables, relationship joins)
        v
 Timbr engine: ontology model (MySQL metadata DB) -> query rewriter/inference -> SQL generation
        |  (optional materialised/cached knowledge)
        v
 source engines: Snowflake, Databricks, BigQuery, Postgres, CSV, Web APIs ...
```

## 5. Under-the-hood reconstruction
Documented: runs as Docker/Kubernetes services; a mandatory Timbr MySQL metadata database stores the model; inference is "based on query-rewriting techniques"; selective materialisation for slow cases [CLAIM-timbr-03][CLAIM-timbr-04]. Hypothesis (not verified): the ontology compiles to views/joins; a query on a concept with inheritance expands to a UNION/JOIN over subconcept mappings (OBDA-style unfolding, as in Ontop; see C04-ontop.md). Transactions, partitioning, caching, security model beyond deployment: NOT PUBLICLY VERIFIED. Source code is proprietary.

## 6. Inferred requirements
SQL dialect translation per source; relationship join generation; inheritance expansion; metadata store; connector set; semantic model governance.

## 7. Performance and resource model
Sizing guidance only: 4 CPU/16 GB (small-medium), 8 CPU/32 GB (large) [CLAIM-timbr-04]. Query latency is that of the source engine plus rewrite overhead (hypothesis); no benchmarks found. Failure modes: pushdown mismatch, join explosions through inheritance expansion, stale materialisations.

## 8. Strengths
SQL-first adoption path (no new query language); virtualisation avoids data copy; MCP and NL2SQL surfaces; on-prem option. Match: EOIP federation planner (BL-51) plus mapping layer; exceed with evidence/provenance and tenant gates.

## 9. Limitations
Verified from docs: no formal versioning, Git-like deployment only planned [CLAIM-timbr-03]; LLM usage and data flow undocumented there; licensing terms not published [CLAIM-timbr-02]. Hypotheses: read-mostly virtual graph; reasoning limited to rewriting-friendly constructs; proprietary lock-in via DDL; relies on source-engine cost. Friction: pricing opacity.

## 10. Deployment, licensing, viability
Proprietary; SaaS tiers and self-hosted Enterprise (K8s/VPC/on-prem) [CLAIM-timbr-04]. Not redistributable/embeddable without a commercial agreement (terms NOT PUBLICLY VERIFIED); OEM/white-label unknown. Egress behaviour of LLM features unknown: conflicts with EOIP default-local policy until documented. Legal-review trigger: proprietary licence and unknown OEM terms. Air-gap: partial/unknown.

## 11. Competitive delta vs baseline
BL-51 federation/virtual planner is Partial (`federation/planner.py:35`); BL-33 CML mapping to IR is Implemented but not R2RML; BL-09 query IR transpiler is a regex subset. Timbr shows the SQL-surface target: BL-59 SQL/PGQ is Absent. BL-58 GraphQL absent. EOIP's advantage: connectors never mutate the graph, evidence and temporal layers (BL-37/41), which Timbr does not document.

## 12. Cards
**STR-timbr-01** | Timbr | semantic layer exposes ontology concepts as SQL tables so BI tools need no new language | [CLAIM-timbr-01] | analysts and BI adoption | match | SQL view facade over EOIP entity types (read-only, tenant-filtered) via a query-plan front end | acceptance: Postgres wire/JDBC client runs a SELECT on a concept; ACL filtering verified.
**INV-timbr-01** | Timbr (undated) | ontology change control not Git-native; Git deployment planned | [CLAIM-timbr-03] | root cause governance (*proven by docs statement*) | alternative: EOIP gitops-first definitions | options (a) export; (b) native gitops; (c) SQL-facade driven from versioned ontology | selected (b) with INV-edg-01 | POC: change an ontology concept, show release/rollback with zero downtime | decision EXPERIMENT.
**INV-timbr-02** | Timbr | opaque LLM data flow | [CLAIM-timbr-03] absence | root cause governance (*hypothesis*) | EOIP egress gateway (BL-45) with manifest | decision ADOPT (already in baseline).

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-21 virtualisation (SQL sources) | EXPERIMENT (via Ontop, see C04) |
| CAP-16 SQL facade | EXPERIMENT |
| CAP-58 NL2SQL | DEFER |
| Timbr product | REJECT as dependency (proprietary, undocumented egress); REFERENCE-ONLY |

## 14. Tests
(PROPOSED; no trial performed.) If a trial licence exists: model 5 concepts over Postgres; compare generated SQL to hand-written; test inheritance expansion cost; confirm no external calls with network disabled; check row-level security pass-through.

## 15. Risks and open questions
Everything beyond documentation is unverified: version, owner, pricing, ACL behaviour, LLM egress, OWL coverage. Marketing claims (analyst self-reports, "active semantic catalog") unaudited.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Proprietary; version unknown |
| D2 | 2 | BI and AI semantic layer |
| D3 | 4 | Engine + MySQL metadata + sources |
| D4 | N/A | Virtual; no graph storage |
| D5 | 1,3 | Four primitives, OWL-DL partial |
| D6 | 5 | Rewrite to SQL |
| D7 | 3,5 | Query rewriting; materialisation |
| D8 | N/A | Delegated to sources |
| D9 | 3 | Connectors, catalog import |
| D10 | N/A | Not documented |
| D11 | 3,9 | No versioning |
| D12 | 3 | networkX/cuGraph mentions |
| D13 | 3 | GraphRAG, MCP |
| D14 | 3 | NL2SQL |
| D15 | 9 | Weak governance |
| D16 | N/A | Not examined |
| D17 | 3 | SQL, REST, SDK, MCP |
| D18 | 10 | Unknown |
| D19 | N/A | Not documented |
| D20 | 7 | Sizing only |
| D21 | 10 | Subscription, opaque |
| D22 | 9 | SQL-centric; RDF unknown |
| D23 | N/A | Not examined |
| D24 | App. C | Vendor docs plus third parties |

## Appendix B. Capability mapping
| CAP-ID | Technology | CLAIM | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-21 | native | 01,03 | BL-51 Partial | EXPERIMENT | P2 |
| CAP-16 | native | 01 | BL-59 Absent | EXPERIMENT | P2 |
| CAP-58 | native (NL2SQL) | 03 | BL-12 Partial | DEFER | P3 |
| CAP-59 | native (MCP) | 01 | BL-47 Implemented | REFERENCE | P3 |
| CAP-77 | proprietary | 02 | n/a | REJECT | P3 |

## Appendix C. Evidence records
| CLAIM-ID | product/version/date | claim | class | source | dates | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-timbr-01 | Timbr (undated) | Virtual SQL knowledge graph; SQL translated to source SQL; JDBC/ODBC, REST, Python SDK, MCP; 40+ sources | Third-party report | https://atlan.com/know/ai-agent/semantic-layer/timbr-semantic-layer/ (via search) | undated / 2026-10-26 | 0.5 | vendor-derived |
| CLAIM-timbr-02 | Timbr | Pricing not published; third-party listing $499/month; subscription SaaS | Third-party report | FitGap/TrustRadius listings via search | undated / 2026-10-26 | 0.3 | stale risk |
| CLAIM-timbr-03 | Timbr docs | Query-rewriting inference; OWL-DL and some OWL 2; materialisation; no formal versioning; Git-like deployment planned; LLM details absent | Officially documented | https://docs.timbr.ai/doc/docs/getting-started/faq | undated / 2026-10-26 | 0.75 | docs undated, may be outdated |
| CLAIM-timbr-04 | Timbr docs | Docker/K8s, on-prem; 4 CPU/16 GB and 8 CPU/32 GB; MySQL metadata DB mandatory | Officially documented | same FAQ | undated / 2026-10-26 | 0.75 | none |

## Appendix D. Assumptions
Access date is the real date. Search-derived third-party statements are classed at low confidence. Section 5 reconstruction beyond the FAQ is hypothesis. No trial or paid access used.
