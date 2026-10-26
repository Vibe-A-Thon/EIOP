| Field | Value |
|---|---|
| Registry ID | T-C06-collibra |
| Tier | B - governance leader; workflow/stewardship reference (CAP-42, CAP-41) |
| Versions examined | SaaS; docs set 2026.02 referenced; no semver |
| Verified on | 2026-10-26 |
| Worker | V18 |

# Collibra

## 1. Identity, current status, tier, and sources
Collibra is a proprietary data and AI governance platform (Collibra Data Intelligence Platform). Status: active. In June 2025 it announced the acquisition of Raito (data access governance) alongside a product release [CLAIM-collibra-02]; a third-party profile also reports Deasy Labs (unstructured data discovery) in July 2025 [CLAIM-collibra-03]. Tier B: the reference for governance workflow, but closed. Sources: Collibra docs and press release, CFTC privacy impact assessment, vendor blog (Appendix C).

## 2. Primary problem, workloads, workflows
| Concern | Position |
|---|---|
| Catalog search | Core: assets, business glossary, data sets |
| Operational lineage | Core: "supports comprehensive data lineage and relationship mapping" via Metadata Graph [CLAIM-collibra-01] |
| Semantic inference | Not documented; glossary relations only (NOT PUBLICLY VERIFIED) |
| Knowledge intelligence | AI governance, Copilot (third-party listing) [CLAIM-collibra-03] |

Workflows: a steward proposes a glossary term, it goes through an approval workflow, then is linked to columns; an Edge site harvests metadata from an on-prem database over JDBC [CLAIM-collibra-04].

## 3. Feature inventory
| Area | Feature | Status |
|---|---|---|
| Model | Metadata Graph as single metadata store | present [CLAIM-collibra-01] |
| API | GraphQL "Knowledge Graph" API | present [CLAIM-collibra-01] |
| Ingestion | Edge: on-prem metadata harvesting, Kubernetes-deployable | present [CLAIM-collibra-01][CLAIM-collibra-04] |
| Governance | Workflows, stewardship, policies | present (details not inspected) |
| Access governance | Raito integration | announced, merged-state UNVERIFIED [CLAIM-collibra-02] |
| AI governance | model/use-case registry | claimed [CLAIM-collibra-03] |
| Self-hosted core | | absent (SaaS on AWS/GCP) [CLAIM-collibra-01] |

## 4. Architecture diagram
```
on-prem sources --JDBC/API--> [Edge site (K8s)] --metadata only--> [Collibra Cloud SaaS (AWS/GCP)]
                                                   microservices -> Metadata Graph -> GraphQL API | UI | workflows
```

## 5. Under-the-hood reconstruction
Verified only at box level: microservice SaaS, Metadata Graph, Edge extracts metadata and sends it to cloud; source data sampled on Edge is purged after 24-48 h in one agency deployment [CLAIM-collibra-04]. Storage engine, indexing and query planner are NOT PUBLICLY VERIFIED. Blueprint to match behaviour: a typed asset/relation store with workflow state machine (draft, review, approved, retired), where state transitions are events; harvesters run at the edge and push only metadata.

## 6. Requirements inferred
Workflow-driven approvals, role-based stewardship, edge harvesting that keeps data in place, GraphQL read API, audit of changes.

## 7. Performance and resource model
No public numbers. Failure mode inferred from architecture: Edge outage stops ingestion while SaaS stays up (hypothesis).

## 8. Strengths
| Strength | Match/exceed |
|---|---|
| Approval workflow on terms and policies | match; EOIP has ontology stewardship (BL-32) but end-to-end flow is partial |
| Edge pattern: harvest in place, ship metadata only | exceed: EOIP connectors already emit SourceEvents (BL-23) |
| GraphQL API | EOIP has none (BL-58 absent) |

## 9. Limitations
Verified: no self-hosted core; cloud dependency. Intentional trade-off: SaaS operability. User-reported: not collected this run. Hypothesis: heavy configuration and services effort is typical for enterprise governance suites. Root causes: coupling to cloud control plane; workflow rigidity; proprietary model.

## 10. Deployment, licensing, viability
Proprietary subscription. Edge on customer K8s, control plane in vendor cloud. Air-gap: no for core (inferred from docs, confidence 0.6). Not embeddable. Legal trigger: none beyond proprietary terms.

## 11. Competitive delta
EOIP lacks a catalog UI and governed-term workflow end-to-end (BL-27, BL-32 partial); EOIP has source-ACL capture (BL-17) but not enforcement (BL-18); Collibra access governance (Raito) targets exactly that class of problem at the warehouse layer, not at graph-fact level.

## 12. Cards
STR-collibra-01 | Collibra | governed term lifecycle | CLAIM-collibra-01 | steward trust | match | states + approvers + semantic diff on ontology-as-code | draft->approved->retired replay test.
INV-collibra-01 | Collibra SaaS | no air-gap | root cause: deployment (proven for core per docs) | options: integrate export / native workflow / open governance contract | selected: native workflow on gitops.py | benchmark: steward task completion time vs spreadsheet | defensibility: offline + Git history | decision: EXPERIMENT.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-41 governance workflow | BUILD (extend gitops/stewardship) |
| CAP-42 catalog | BUILD thin; INTEGRATE Collibra as upstream source via export |
| GraphQL API | EXPERIMENT |
| Collibra core | REJECT as dependency |

## 14. Tests and acceptance
Approval workflow with two roles and rollback; export glossary to JSON-LD with loss accounting (BL-31); verify no tenant data leaves during run.

## 15. Risks and open questions
Public lineage depth, edge-to-cloud payload contents, and Raito merge status are unverified.

## Appendix A - Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | proprietary, active |
| D2 | 2 | governance |
| D3 | 4 | edge+cloud |
| D4 | 5 | N/A undisclosed |
| D5 | 3 | glossary/assets |
| D6 | 5 | N/A |
| D7 | 2 | none documented |
| D8 | 7 | N/A |
| D9 | 3,5 | Edge/JDBC |
| D10 | 11 | N/A |
| D11 | 5 | N/A |
| D12 | N/A | not in scope |
| D13 | 3 | Copilot claim |
| D14 | 3 | N/A unverified |
| D15 | 2,8 | core strength |
| D16 | 3 | not inspected |
| D17 | 3 | GraphQL |
| D18 | 3,11 | Raito access governance |
| D19 | 9 | SaaS multi-tenant, undisclosed |
| D20 | 7 | N/A |
| D21 | 10 | subscription |
| D22 | 10 | export UNVERIFIED |
| D23 | N/A | not assessed |
| D24 | 9 | vendor-heavy |

## Appendix B - Capability mapping
| CAP | Collibra | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-41 | native | 01 | BL-32 partial | BUILD | P1 |
| CAP-42 | native | 01 | none | BUILD thin | P1 |
| CAP-40 | native | 01 | BL-41 partial | EXPERIMENT | P2 |
| CAP-26 | native (Edge) | 04 | BL-23 | INTEGRATE | P3 |

## Appendix C - Evidence records
| CLAIM | product/date | claim | class | source | access | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-collibra-01 | Collibra docs 2026.02 | Metadata Graph, GraphQL Knowledge Graph API, Edge as on-prem component, SaaS on AWS/GCP, microservices | Officially documented (via search summary) | docs.collibra.com/Content/Cloud/Intro/co_cloud-introduction.htm | n/a / 2026-10-26 | 0.6 not fetched in full | none |
| CLAIM-collibra-02 | 2025-06 | Raito acquisition announced | Officially documented | collibra.com press release (raito) | 2025-06 / 2026-10-26 | 0.8 | none |
| CLAIM-collibra-03 | 2025-07 | Deasy Labs acquisition; Copilot | Third-party report | everydev.ai/developers/collibra | 2026-10-26 | 0.4 | none |
| CLAIM-collibra-04 | CFTC PIA | Edge pulls partial data via JDBC, sends metadata, purges in 24-48 h | Third-party report (government PIA) | cftc.gov/media/12636/piacollibra122024/download | 2024-12 / 2026-10-26 | 0.5 one deployment | other configs may differ |

## Appendix D - Assumptions
Pages were read via search summaries, not full fetches, for Collibra docs. Governance workflow detail assumed typical, unverified.
