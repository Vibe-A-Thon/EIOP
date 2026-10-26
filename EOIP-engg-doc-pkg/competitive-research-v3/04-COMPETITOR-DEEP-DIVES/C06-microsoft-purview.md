| Field | Value |
|---|---|
| Registry ID | T-C06-microsoft-purview |
| Tier | B - enterprise governance; Azure-native catalog and lineage (CAP-42, CAP-40) |
| Versions examined | Azure service (no semver). Learn pages: classic lineage doc (updated 2025-11-18); "what's new" 2026 |
| Verified on | 2026-10-26 |
| Worker | V18 |

# Microsoft Purview

## 1. Identity, current status, tier, and sources
Microsoft Purview is Microsoft's cloud data governance, compliance and security suite. Relevant here: the **Data Map** (metadata store, Atlas-compatible APIs), the **classic Data Catalog**, and the newer **Unified Catalog** (data products, governance domains, data quality) [CLAIM-pv-01][CLAIM-pv-02]. Proprietary, Azure-only SaaS; active. Tier B because it is the default catalog for Microsoft estates. Sources: Microsoft Learn, Azure pricing pages, one third-party analysis (Appendix C).

## 2. Primary problem, workloads, workflows
| Concern | Position |
|---|---|
| Catalog search | Core: Data Map + Unified Catalog |
| Operational lineage | Core: Sources > Process > Targets, column level where source supports, execution status [CLAIM-pv-02] |
| Semantic inference | Absent; classifications and glossary only |
| Knowledge intelligence | Data quality GA features 2026 (scans, rules); no first-party MCP server for Unified Catalog documented as of 2026-09-16 (third-party claim) [CLAIM-pv-03] |

Workflows: scan Azure SQL, label PII, see lineage from Data Factory copy to Power BI dashboard [CLAIM-pv-02]; use Atlas API to build apps on Data Map [CLAIM-pv-01].

## 3. Feature inventory
| Area | Feature | Status |
|---|---|---|
| Metadata store | Data Map with Atlas-compatible API | present [CLAIM-pv-01] |
| Scale model | capacity units: 25 ops/s and 10 GB each; auto-scale 1 to 10; more by support request | present [CLAIM-pv-01] |
| Lineage | ADF, Synapse, Databricks notebooks (Unity Catalog lineage limited to notebooks per Oct 2025 Q&A), Power BI | partial [CLAIM-pv-02][CLAIM-pv-03] |
| Quality | scans, SQL-expression rules | GA 2026 per Learn summary; REST API preview [CLAIM-pv-03] |
| MCP | | absent per third party [CLAIM-pv-03] |
| Self-hosted core | | absent |
| Self-hosted integration runtime for on-prem scans | | present (background; not re-verified) |

## 4. Architecture diagram
```
sources (Azure, on-prem via IR, M365, Fabric) -> scan engine -> [Data Map: Atlas-style store, capacity units]
   -> classic Catalog | Unified Catalog (domains, data products, quality) -> UI | Atlas API | REST
```

## 5. Under-the-hood reconstruction
Public facts: Atlas-compatible API surface, capacity-unit billing, entity-level lineage with process nodes and column mapping [CLAIM-pv-01][CLAIM-pv-02]. The actual storage engine and indexing are NOT PUBLICLY VERIFIED. Hypothesis (0.4): Atlas-like typedef model re-implemented on proprietary storage. Blueprint to match: typed entity store with GUIDs, Process nodes, scanner framework with classification rules (regex/dictionary), collection-scoped permissions (background, unverified). Reuse of Atlas model knowledge is licence-clean (Apache-2.0).

## 6. Requirements inferred
Scheduled scanning, classification, lineage from orchestrators, capacity elasticity, enterprise identity (Entra).

## 7. Performance and resource model
Only the billing unit is public: 25 ops/s and 10 GB per capacity unit; older material said 2 GB (outdated) [CLAIM-pv-01]. No latency numbers. Failure mode: storage growth forces next unit even at low throughput [CLAIM-pv-01].

## 8. Strengths
| Strength | Match/exceed |
|---|---|
| Native lineage for Microsoft stack | integrate through OpenLineage/Atlas API |
| Atlas-compatible API | build a reader once, reuse for Atlas |
| Capacity-based elasticity | N/A on one node |

## 9. Limitations
Verified: lineage coverage gaps for Databricks Unity Catalog beyond notebooks (Oct 2025) [CLAIM-pv-03]; cloud-only. Hypothesis: capacity-unit pricing penalises large metadata. Root causes: deployment/coupling to Azure; proprietary model; docs flux (classic vs new).

## 10. Deployment, licensing, viability
Proprietary, pay-as-you-go; not embeddable; air-gap: no (core is Azure). Legal trigger: none beyond service terms. Use only as an upstream source.

## 11. Competitive delta
EOIP has no data-estate scanner or catalog (no BL); has PII detection (BL-46) and ingest-side permission capture (BL-17). Purview's collection-scoped permissions vs EOIP per-fact ACL gap (BL-18).

## 12. Cards
STR-pv-01 | Purview | Atlas-compatible API as lingua franca | CLAIM-pv-01 | one reader for two catalogs | integrate | `AtlasEntityConnector` emitting SourceEvents | recorded JSON fixtures map without loss.
INV-pv-01 | Purview | cloud-only, capacity-metered | root cause: deployment/licensing (proven) | options: integrate as source / native local scanner / OpenLineage-first model | selected: integrate + native thin | benchmark: import 100k entities, loss report | defensibility: air-gap | decision: EXPERIMENT.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-42 | INTEGRATE Purview as source |
| CAP-40 | INTEGRATE via Atlas API/OpenLineage |
| CAP-33 PII detection | REUSE own (BL-46) |
| Purview runtime | REJECT |

## 14. Tests and acceptance
Replay an Atlas-format export from Data Map into SourceEvents; verify connector never writes graph directly (BL-23); lineage edges preserved; ACL metadata carried.

## 15. Risks and open questions
Unified Catalog vs classic divergence; MCP status; lineage coverage by source; export rights.

## Appendix A - Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Microsoft, proprietary |
| D2 | 2 | catalog+compliance |
| D3 | 4 | Data Map + catalogs |
| D4 | 5 | N/A undisclosed |
| D5 | 5 | Atlas-style |
| D6 | N/A | REST/Atlas API |
| D7 | 2 | none |
| D8 | 7 | capacity units |
| D9 | 3 | scans, IR |
| D10 | N/A | not inspected |
| D11 | N/A | not inspected |
| D12 | N/A | out of scope |
| D13 | 3 | no MCP (3rd party) |
| D14 | N/A | not inspected |
| D15 | 3 | domains, data products |
| D16 | N/A | not inspected |
| D17 | 3 | REST, Atlas API |
| D18 | 5 | collections; unverified |
| D19 | N/A | Azure tenants |
| D20 | 7 | pricing unit |
| D21 | 10 | PAYG |
| D22 | 8,11 | Atlas API |
| D23 | N/A | not assessed |
| D24 | 9 | mixed source quality |

## Appendix B - Capability mapping
| CAP | Purview | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-40 | partial (source dependent) | 02,03 | BL-41 partial | INTEGRATE | P2 |
| CAP-42 | native | 01 | none | INTEGRATE | P2 |
| CAP-33 | native (classification) | - | BL-46 | REUSE own | P3 |

## Appendix C - Evidence records
| CLAIM | product/date | claim | class | source | access | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-pv-01 | Data Map | Atlas-compatible APIs; capacity unit 25 ops/s + 10 GB; auto-scale 1-10 CU | Officially documented | learn.microsoft.com/purview/data-map; docs.azure.cn/en-us/purview/data-gov-classic-pricing-data-map | n/a / 2026-10-26 | 0.7 via search summary | older docs say 2 GB |
| CLAIM-pv-02 | classic lineage doc 2025-11-18 | Lineage is a graph of Sources > Process > Targets; column-level; execution status | Officially documented | learn.microsoft.com/en-us/purview/data-gov-classic-lineage | 2025-11-18 / 2026-10-26 | 0.9 | Unified Catalog may differ |
| CLAIM-pv-03 | 2025-10 to 2026-09 | Unity Catalog lineage limited to notebooks (Q&A Oct 2025); DQ GA features; no first-party MCP for Unified Catalog (3rd party, 2026-09-16) | Third-party report | learn.microsoft.com/answers/a/12313138; atlan.com/know/ai-agent/microsoft/purview-unified-catalog/ | 2026-10-26 | 0.4 competitor-authored | not confirmed by Microsoft |

## Appendix D - Assumptions
Scanner, IR and collection permission details are prior knowledge and unverified. "What's new" content read only via search summary.
