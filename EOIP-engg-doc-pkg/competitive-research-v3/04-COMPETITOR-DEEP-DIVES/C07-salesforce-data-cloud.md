| Field | Value |
|---|---|
| Registry ID | T-C07-salesforce-data-cloud |
| Tier | B (customer data graph; renamed product) |
| Versions examined | "Data 360" (formerly Data Cloud), as named from Dreamforce 2025; SaaS, no version numbers published |
| Verified on | 2026-10-26 (brief date 2026-10-18; actual access date used) |
| Worker | V19 |

## 1. Identity, current status, tier, sources
**Rename trap resolved:** Salesforce Data Cloud is now **Salesforce Data 360**, renamed at Dreamforce 2025 under the Agentforce 360 umbrella; earlier names include Genie, Customer Data Platform, CDP (sources disagree on the full list); existing contracts carry over [CLAIM-sf-01,02]. Owner Salesforce, Inc.; proprietary SaaS; not a graph database in the strict sense: it is a customer-data lakehouse with identity resolution, a harmonised data model, and "data graphs" (precomputed JSON-like entity views) feeding Agentforce. The Salesforce help page for data graphs could not be rendered by the fetch tool, so data-graph internals are **UNVERIFIED** (see CLAIM-sf-03). Related existing deep dives: C07-servicenow-kg, C07-glean-enterprise (permission-aware enterprise search), C07-microsoft-graph-copilot-fabric.

## 2. Problem, workloads, workflows
Unify customer records across CRM, marketing, commerce, and warehouses; resolve identities into unified profiles; activate segments and ground agents. Workflow: ingest CRM + web events -> identity resolution -> unified profile -> data graph -> Agentforce grounding. Relevant to EOIP only for J15-style non-IT scenarios (customer/org data) and as an identity-resolution pattern.

## 3. Feature inventory (vendor-documented; not re-verified in this session unless cited)
| Feature | Status | Evidence |
|---|---|---|
| Data ingestion connectors, streaming | present | UNVERIFIED this session |
| Harmonised data model (DMOs), unified individual | present | UNVERIFIED |
| Identity resolution (rule-based, fuzzy) | present | UNVERIFIED; CAP-31 |
| Zero-copy federation to warehouses | present | UNVERIFIED; CAP-21 |
| Data graphs for agent grounding | present | CLAIM-sf-03 |
| Vector search / unstructured | present | UNVERIFIED |
| SPARQL/Cypher/Gremlin | absent (not a graph query product) | inference |
| Self-hosted / air-gap | absent | CLAIM-sf-01 (SaaS) |

## 4. Architecture diagram
```
Sources(CRM, web, ERP, warehouse zero-copy) -> Data 360 ingest -> DMO harmonisation
   -> Identity resolution -> Unified profile -> Data graphs / segments / calc insights
   -> Agentforce 360 (action layer) via trust layer
```
Hypothesis-level; derived from vendor positioning "Data 360 = data layer, Agentforce 360 = action layer" [CLAIM-sf-02].

## 5. Under-the-hood reconstruction
Not public at the level required. Observable pattern only: object-store lakehouse + semantic model + identity graph; materialised entity views for low-latency retrieval. Storage format, query engine, consistency: **NOT PUBLICLY VERIFIED** in this session. Security: Salesforce permission model and field-level controls reportedly honoured at activation (UNVERIFIED).

## 6. Inferred requirements
Unified entity identity with explainable matching; precomputed entity views for agent latency; source-system permission fidelity; consent and DSAR links to profiles (EOIP has privacy modules BL-46).

## 7. Performance and resource model
No benchmarks examined; vendor figures not retrieved. Consumption-credit pricing (UNVERIFIED) implies cost scales with rows processed. No numbers asserted.

## 8. Strengths
Mature identity resolution with business-user UX; zero-copy federation avoids duplication; direct agent activation. Match: EOIP BL-34/35 and a Splink/Zingg REUSE (BL-36 absent); exceed via explainable merge/split with provenance and revision (BL-37/41).

## 9. Limitations
Intentional trade-off: Salesforce-centric model and SaaS lock-in. Licensing: proprietary, credit-based. Friction: product rename churns docs and integrations. Hypothesis: opaque match logic limits auditability for regulated tenants. No user complaints retrieved.

## 10. Deployment/licensing/viability
SaaS only; fails air-gap, no-mandatory-cloud. OEM/white-label: not available. Legal trigger: proprietary terms; data-residency terms not reviewed.

## 11. Competitive delta
EOIP identity: deterministic person identity only (BL-34), no probabilistic ER (BL-36 Absent). Data 360 leads on ER and activation. EOIP leads on ontology governance (BL-32), bitemporal (BL-37), evidence (BL-41), on-prem (BL-45).

## 12. Cards
STR-sf-01 | Salesforce Data 360 | Business-user identity resolution with unified profile | sf-03 (partial) | value: customer-360 for J15 | match | Splink-based ER pipeline emitting merge candidates to BL-35 queue | test: 10k synthetic duplicate persons, F1 >= 0.9 with all merges reversible.
INV-sf-01 | Data 360 | Opaque, SaaS-bound identity merges | sf-01 | root cause: governance/deployment, hypothesis | EOIP alt: explainable merge with provenance, worse when users need turnkey UI | options: (1) Splink integration, (2) native blocking+scoring, (3) ER with epistemic labels | selected 1 then 2 | POC as above, resource baseline single node | defensibility: audit-grade lineage | decision EXPERIMENT. No §10.5 seed targets this entry.

## 13. Per-capability decisions
CAP-31 ER: INTEGRATE Splink/Zingg (see C04). CAP-21 federation: REFERENCE zero-copy pattern. CAP-46: EXPERIMENT permission mirroring. CAP-52 white-label: EOIP advantage. Data 360 itself: REJECT as dependency, REFERENCE-ONLY as pattern.

## 14. Tests/POC
Synthetic CRM duplicates ER test above; consent-withdrawal propagation test across unified profile.

## 15. Risks and open questions
Data-graph internals and pricing unverified; whether Data 360 exposes a graph query API; MCP/Agentforce interoperability.

## Appendix A — Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | renamed, proprietary |
| D2 | 2 | customer 360 |
| D3 | 4 | lakehouse+ER, hypothesis |
| D4 | 5 | not public |
| D5 | 3 | DMO model |
| D6 | N/A | no graph query language |
| D7 | N/A | none |
| D8 | N/A | SaaS-managed |
| D9 | 3 | connectors, zero-copy |
| D10 | 3,8 | identity resolution |
| D11 | N/A | not examined |
| D12 | N/A | not examined |
| D13 | 3 | agent grounding |
| D14 | N/A | not examined |
| D15 | N/A | not examined |
| D16 | N/A | not examined |
| D17 | N/A | not examined |
| D18 | 5 | permissions unverified |
| D19 | 10 | org-per-tenant SaaS, unverified |
| D20 | 7 | credits, unverified |
| D21 | 9,10 | proprietary |
| D22 | 9 | lock-in |
| D23 | N/A | not examined |
| D24 | 1 | secondary sources; low confidence |

## Appendix B — Capability mapping
| CAP | Technology | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-31 | native | sf-03 | BL-36 Absent | INTEGRATE | P1 |
| CAP-21 | native | sf-03 | BL-51 partial | REFERENCE | P3 |
| CAP-56 | partial | sf-03 | BL-16 | DEFER | P3 |
| CAP-52 | absent | sf-01 | BL-21 | EOIP advantage | P2 |

## Appendix C — Evidence records
| CLAIM | product/date | claim | class | source | pub/access | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| sf-01 | Data 360 / Dreamforce 2025 | Salesforce product page: Data 360 is new name for Data Cloud; contracts honoured | Officially documented (via search summary) | https://www.salesforce.com/ap/products/data/ | 2025 / 2026-10-26 | 0.8 | none |
| sf-02 | Agentforce 360 | rename removes "cloud"; Data 360 = data layer, Agentforce 360 = action layer | Third-party report | https://www.salesforceben.com/salesforce-data-cloud-renamed-to-data-360-as-part-of-agentforce-360/ | 2025 / 2026-10-26 | 0.7 | earlier-name lists differ across sources |
| sf-03 | Data 360 data graphs | Data graphs ground agents (help article not rendered) | UNVERIFIED | https://help.salesforce.com/s/articleView?id=data.c360_a_data_graphs.htm | n/d / 2026-10-26 | 0.25 | none found |

## Appendix D — Assumptions
Feature list beyond rename is from general product knowledge and treated UNVERIFIED (confidence <= 0.3). Official docs need a browser-capable re-check.
