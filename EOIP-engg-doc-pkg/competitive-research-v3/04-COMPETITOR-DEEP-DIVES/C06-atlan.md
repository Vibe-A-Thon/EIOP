| Field | Value |
|---|---|
| Registry ID | T-C06-atlan |
| Tier | B - active-metadata / "context layer" competitor (CAP-42, CAP-40) |
| Versions examined | SaaS, no public product version. pyatlan SDK (version/date UNVERIFIED; README shows 7.1.3 only as an install example) |
| Verified on | 2026-10-26 (brief says 2026-10-18; today's date used) |
| Worker | V18 |

# Atlan

## 1. Identity, current status, tier, and sources
Atlan is a proprietary SaaS data catalog and governance product. It now markets itself as a "context layer for AI" with a "Context Lakehouse" [CLAIM-atlan-01]. Public SDKs are Apache-2.0 [CLAIM-atlan-03]. Core platform: proprietary, no source. Status: active. A third-party profile reports 400+ customers (Aug 2026); this is not independently verified [CLAIM-atlan-01]. Tier B because it is the market's loudest "active metadata / context graph" voice, but it is closed and cloud-first. Sources: atlan.com pages, docs.atlan.com, GitHub atlan-python (Appendix C).

## 2. Primary problem, workloads, example workflows
| Concern | Atlan position (vendor-described) |
|---|---|
| Catalog search | Core. 100+ connectors; asset search, glossary, certificates [CLAIM-atlan-01] |
| Operational lineage | Core. Column-level lineage from metadata and query history; "Process" assets are the basis of lineage [CLAIM-atlan-02] |
| Semantic inference | NOT PUBLICLY VERIFIED. No OWL/SHACL reasoner documented. |
| Knowledge intelligence | Vendor claim: Iceberg-based context store queryable by agents over MCP, A2A, SQL, APIs [CLAIM-atlan-01] |

Workflows: an analyst finds a certified table; a steward propagates a PII tag downstream via lineage [CLAIM-atlan-02]; an agent pulls context through MCP before writing SQL.

## 3. Feature inventory
| Area | Feature | Status |
|---|---|---|
| Model | Typedefs inheriting `Asset`; custom metadata sets; badges | present [CLAIM-atlan-02] |
| Lineage | Process-based lineage; tag propagation along lineage, parent/child, glossary | present [CLAIM-atlan-02] |
| SDK | Python sync/async, 400+ asset types, Py3.9-3.13 | present [CLAIM-atlan-03] |
| Agents | MCP / A2A access | vendor claim [CLAIM-atlan-01] |
| Storage | Iceberg "Metadata/Context Lakehouse" | vendor claim, internals unknown |
| Access | RBAC/ABAC, "purposes" | present; semantics partly documented |
| Deploy | Single-tenant, cloud-agnostic SaaS; on-prem/air-gap | on-prem NOT PUBLICLY VERIFIED |

## 4. Architecture diagram
```
sources(100+ connectors, query logs) -> crawlers -> [Atlan control plane, SaaS]
   -> typedef store (Atlas-derived model, UNVERIFIED) + search index
   -> Context Lakehouse (Iceberg, vendor claim)
   -> UI | REST/SDK | MCP | A2A | SQL
```
Control/data plane split and datastores are NOT PUBLICLY VERIFIED.

## 5. Under-the-hood reconstruction
Verified: typed asset model with inheritance, Processes as lineage edges, tag propagation rules [CLAIM-atlan-02]. The SDK credits Apache Atlas for portions of its code, so the metastore model is Atlas-derived (hypothesis for server side, confidence 0.4) [CLAIM-atlan-03]. Everything else (storage layout, indexing, query planning, concurrency, versioning) is NOT PUBLICLY VERIFIED. Blueprint to match: typed entities + `Process` nodes (input[] -> output[]) + propagation rule engine over the lineage DAG; this is a straightforward graph traversal and needs no private knowledge.

## 6. Requirements inferred
FR: typed assets, custom metadata, lineage traversal with tag propagation, certification, glossary linking, agent-facing API. NFR: tenant isolation (single-tenant claim), audit trail (vendor claim), hundreds of connectors.

## 7. Performance and resource model
No public benchmarks. The "5x agent accuracy" figure is an internal Atlan AI Labs claim with unstated workload and hardware; do not use [CLAIM-atlan-04]. Footprint unknown (SaaS).

## 8. Strengths
| Strength | Match/exceed |
|---|---|
| Tag/classification propagation along lineage | match: deterministic graph rule, local |
| Agent-facing governed context API | exceed: EOIP has MCP (BL-47) plus evidence spans |
| Wide connector catalogue | integrate via SourceEvent, never replicate |

## 9. Limitations
Verified: closed core; SaaS orientation. User-reported: one Gartner Peer Insights review (3.0) cites weak Microsoft integration [CLAIM-atlan-05]. Intentional trade-off: managed service. Hypothesis: "context graph" is catalog metadata plus lineage, not a reasoning layer. Root causes: coupling to vendor cloud (operational), no open spec (friction).

## 10. Deployment, licensing, viability
Proprietary SaaS; SDK Apache-2.0. Air-gap: NOT PUBLICLY VERIFIED, assume no. Not embeddable or white-label. Legal review trigger: any reuse of docs or typedef layouts. Only SDK code is lawfully reusable.

## 11. Competitive delta (EOIP baseline)
| Topic | EOIP | Atlan |
|---|---|---|
| Source ACL in answers | BL-17 captured, BL-18 absent | RBAC/ABAC on assets (vendor) |
| Lineage | BL-41 evidence lineage, not OpenLineage-style data lineage (not confirmed) | operational lineage core |
| Agents | BL-47 MCP read-only | MCP + A2A |
| Tenancy | BL-20 partial | single-tenant SaaS |

## 12. Cards
STR-atlan-01 | Atlan | tag propagation via lineage | CLAIM-atlan-02 | cuts steward toil | match | rule engine over lineage DAG, emits PROPOSED tags | propagation test on 3-hop DAG with tombstones.
INV-atlan-01 | target: Atlan SaaS context layer | limitation: no self-host/air-gap evidence | root cause: deployment (hypothesis) | options: (a) integrate via export, (b) native local context API, (c) open context contract | selected (b): local-first MCP with governed spans | benchmark: agent QA on fixed schema, local vs plain metadata | defensibility: air-gap + ACL-aware spans | decision: EXPERIMENT. Seed hypothesis check: "catalogs lack evidence spans" - supported only for what is documented; UNVERIFIED for Atlan internals.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-40 lineage | EXPERIMENT: OpenLineage ingestion, Process-style edges |
| CAP-42 catalog | BUILD thin catalog view over graph; INTEGRATE external catalogs as sources |
| Tag propagation | BUILD |
| Atlan service | REJECT as dependency (cloud, closed) |

## 14. Tests and acceptance
Import an OpenLineage fixture; verify 3-hop propagation with PROPOSED status; verify no egress during run; MCP call returns ACL-filtered spans.

## 15. Risks and open questions
Is on-prem offered? What is the Context Lakehouse schema? How does Atlan enforce source ACLs for agents? All open.

## Appendix A - Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | proprietary SaaS, active |
| D2 | 2 | catalog + lineage + agents |
| D3 | 4 | partial, undisclosed |
| D4 | 5 | N/A not public |
| D5 | 3,5 | typedefs, custom metadata |
| D6 | 5 | N/A |
| D7 | 2 | no reasoning documented |
| D8 | 7 | N/A |
| D9 | 3 | 100+ connectors |
| D10 | 11 | N/A tag/ACL only |
| D11 | 5 | N/A |
| D12 | 7 | N/A |
| D13 | 3,8 | MCP/A2A claim |
| D14 | 3 | NL access claimed, unmeasured |
| D15 | 3 | certificates, glossary |
| D16 | 3 | UI, not inspected |
| D17 | 3 | SDKs |
| D18 | 3,9 | RBAC/ABAC claim |
| D19 | 11 | single-tenant claim |
| D20 | 7 | N/A |
| D21 | 10 | proprietary |
| D22 | 10 | Iceberg claim |
| D23 | 10 | not assessed |
| D24 | 9 | vendor sources dominate |

## Appendix B - Capability mapping
| CAP | Atlan | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-40 | native | 02 | BL-41 partial | EXPERIMENT | P1 |
| CAP-42 | native | 01 | none verified | BUILD thin | P1 |
| CAP-59 MCP | vendor claim | 01 | BL-47 | REUSE own | P2 |
| CAP-26 | native | 01 | BL-23 | INTEGRATE | P2 |

## Appendix C - Evidence records
| CLAIM | product/date | claim | class | source | access | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-atlan-01 | Atlan / 2026 | Positions as context layer; Iceberg Context Lakehouse; queryable via MCP, A2A, SQL, APIs; 100+ connectors; 400+ customers (third party) | Third-party report / vendor claim | atlan.com/context-lakehouse/, atlan.com/atlan-for-snowflake/, atlan.com/p/context-layer/ | n/a / 2026-10-26 | 0.6 vendor | none |
| CLAIM-atlan-02 | Atlan docs | Typedefs inherit Asset; Processes basis of lineage; tags propagate via lineage, parent-child, glossary | Officially documented | docs.atlan.com/product/capabilities/build-apps/sdks/python/concepts | n/a / 2026-10-26 | 0.85 | none |
| CLAIM-atlan-03 | atlan-python | Apache-2.0; 400+ asset types; credits Apache Atlas | Officially documented | github.com/atlanhq/atlan-python | n/a / 2026-10-26 | 0.85 | server licence proprietary, unverified |
| CLAIM-atlan-04 | Atlan | "5x" agent accuracy claim | Unverified vendor claim | atlan.com search summary | 2026-10-26 | 0.2 | no method |
| CLAIM-atlan-05 | Gartner Peer Insights | 3.0 review citing missing Microsoft integration | Third-party report | gartner.com/reviews/product/atlan | 2026-10-26 | 0.3 single review | other reviews unseen |

## Appendix D - Assumptions
Access date 2026-10-26. "Context graph" treated as marketing for catalog+lineage+retrieval. Server internals not assumed beyond Atlas heritage hypothesis.
