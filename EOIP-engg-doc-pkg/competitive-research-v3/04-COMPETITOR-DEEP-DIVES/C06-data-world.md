| Field | Value |
|---|---|
| Registry ID | T-C06-data-world |
| Tier | B - knowledge-graph-based catalog; ownership resolved (ServiceNow) |
| Versions examined | SaaS; no semver |
| Verified on | 2026-10-26 |
| Worker | V18 |

# data.world

## 1. Identity, current status, tier, and sources
**Ownership resolved:** ServiceNow announced the acquisition on 2025-05-07 [CLAIM-dw-01]; ServiceNow's FY2025 Form 10-K states it completed the acquisition of data.world, Inc. in July 2025 and that it is not material financially [CLAIM-dw-02]. data.world is therefore a ServiceNow-owned product (status: acquired). One aggregator says it is now called "Declan"; no second source, UNVERIFIED and likely wrong [CLAIM-dw-03]. Current product packaging inside ServiceNow (standalone SKU vs Workflow Data Fabric) is NOT PUBLICLY VERIFIED. Tier B because it is the one catalog that names RDF/OWL/SPARQL as its foundation. Proprietary SaaS.

## 2. Primary problem, workloads, workflows
| Concern | Position |
|---|---|
| Catalog search | Core |
| Semantic inference | Semantic technologies used; reasoning depth NOT PUBLICLY VERIFIED [CLAIM-dw-04] |
| Operational lineage | present, details not inspected |
| Knowledge intelligence | AI Context Engine: enterprise agents answering over structured data with traceable evidence (vendor claim) [CLAIM-dw-04] |

Workflows: a steward runs a templated SPARQL script to bulk-enrich glossary and relationships; a business user asks a question of Snowflake data via the AI Context Engine and gets an answer with evidence links [CLAIM-dw-04].

## 3. Feature inventory
| Area | Feature | Status |
|---|---|---|
| Model | Catalog as knowledge graph; RDF, OWL, SPARQL named | present (vendor) [CLAIM-dw-04] |
| Automation | Eureka Automations with templated SPARQL scripts | present [CLAIM-dw-04] |
| Eureka | Action Center, Answers, Explorer | present (vendor) [CLAIM-dw-04] |
| AI | AI Context Engine (SaaS agents) | present, SaaS only [CLAIM-dw-04] |
| Self-hosted | | not documented; assume absent |
| SHACL, OWL reasoning | | UNVERIFIED |

## 4. Architecture diagram
```
connectors/collectors -> [RDF catalog graph (store UNVERIFIED)] <- SPARQL automations
        -> Eureka UI/search -> AI Context Engine (agents) -> BI/GenAI interfaces
```
Hosted by ServiceNow after 2025 (deployment topology UNVERIFIED).

## 5. Under-the-hood reconstruction
Verified: vendor states catalog is a knowledge graph on RDF/OWL/SPARQL [CLAIM-dw-04]. Not verified: triple store engine, indexing, inference regime, tenancy. Hypothesis (confidence 0.4): metadata stored as RDF named graphs per organisation, enrichment via SPARQL UPDATE templates. Blueprint to match behaviour: catalog entities as RDF (DCAT/PROV style), SPARQL CONSTRUCT/INSERT templates as versioned "automations", answer generation that returns the evidence IRIs. EOIP already has an RDF adapter path (BL-06) and PROV-O mapping (BL-33).

## 6. Requirements inferred
Standards-based catalog model, template-driven bulk enrichment, evidence-linked NL answers, glossary generation.

## 7. Performance and resource model
No public numbers. Failure mode: SPARQL automations over large graphs without budgets (hypothesis); EOIP has budgets (CRA-024.9 in recent commits).

## 8. Strengths
| Strength | Match/exceed |
|---|---|
| Semantic-web foundation lowers lock-in in principle | match: EOIP bridges to W3C at the boundary |
| Templated SPARQL enrichment | exceed: reviewable, Git-tracked automations |
| Evidence-linked answers | match; EOIP citation checks already exist |

## 9. Limitations
Verified: now inside ServiceNow (roadmap risk) [CLAIM-dw-02]. Vendor claims: unmeasured accuracy. Unknown: whether export of the RDF graph is supported. Root causes: ownership change (governance), SaaS-only agents (deployment).

## 10. Deployment, licensing, viability
Proprietary SaaS; no OSS. Air-gap: no evidence. Not embeddable. Legal trigger: none identified.

## 11. Competitive delta
EOIP baseline: RDF adapters partial (BL-06), SHACL partial (BL-29), JSON-LD loss accounting (BL-31), mapping to LPG/RDF (BL-33). data.world shows a market for catalog-on-RDF; EOIP differs by backend neutrality and ACL work (BL-17/18 gap).

## 12. Cards
STR-dw-01 | data.world | SPARQL-template enrichment | CLAIM-dw-04 | bulk steward ops | exceed | versioned templates via mapping IR + review queue | rerun idempotency test.
INV-dw-01 | data.world | acquisition risk and SaaS-only agents | root cause: governance/deployment (proven ownership change) | options: integrate by export / native evidence answers / open interchange | selected native | benchmark: answer citation validity on fixed catalog | defensibility: local-first | decision: EXPERIMENT.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-42 catalog on RDF model | EXPERIMENT |
| CAP-29 template mappings | REUSE own CML |
| data.world service | REFERENCE-ONLY; REJECT as dependency |

## 14. Tests and acceptance
Express three enrichment automations in CML, run twice, diff = zero; produce answers whose cited IRIs resolve.

## 15. Risks and open questions
Post-acquisition product continuity; "Declan" rename; export formats; store engine.

## Appendix A - Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | ServiceNow-owned |
| D2 | 2 | catalog/KG |
| D3 | 4 | UNVERIFIED |
| D4 | 5 | RDF claimed |
| D5 | 3 | RDF/OWL claimed |
| D6 | 3 | SPARQL |
| D7 | 2 | UNVERIFIED |
| D8 | 7 | N/A |
| D9 | 4 | collectors |
| D10 | 2 | evidence in answers |
| D11 | N/A | not documented |
| D12 | N/A | out of scope |
| D13 | 2 | AI Context Engine |
| D14 | 3 | NL over Snowflake (vendor) |
| D15 | 3 | glossary automation |
| D16 | 3 | Eureka UI |
| D17 | 3 | SPARQL templates |
| D18 | N/A | not inspected |
| D19 | N/A | not public |
| D20 | 7 | N/A |
| D21 | 10 | proprietary |
| D22 | 8,15 | export unknown |
| D23 | N/A | not assessed |
| D24 | 9 | vendor sources |

## Appendix B - Capability mapping
| CAP | data.world | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-42 | native | 04 | none verified | EXPERIMENT | P2 |
| CAP-29 | partial (SPARQL templates) | 04 | BL-33 | REUSE own | P3 |
| CAP-40 | unknown | - | BL-41 | DEFER | P3 |

## Appendix C - Evidence records
| CLAIM | product/date | claim | class | source | access | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-dw-01 | 2025-05-07 | ServiceNow signed agreement to acquire data.world | Third-party report | techcrunch.com/2025/05/07/servicenow-acquires-data-world-two-months-after-acquiring-moveworks | 2025-05-07 / 2026-10-26 | 0.9 | none |
| CLAIM-dw-02 | FY2025 10-K | Acquisition completed July 2025 | Officially documented | sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm | 2026 / 2026-10-26 | 0.85 via search summary | none |
| CLAIM-dw-03 | aggregator | Company "now called Declan" | Unverified | finder.techleap.nl feed | 2026-10-26 | 0.1 | uncorroborated |
| CLAIM-dw-04 | data.world | KG-based catalog using RDF/OWL/SPARQL; Eureka; AI Context Engine SaaS agents | Vendor claim | data.world/ai/ai-context-engine-faq; data.world/product/eureka/ | 2026-10-26 | 0.5 | none |

## Appendix D - Assumptions
Pre-acquisition data.world used an RDF store (prior knowledge, not re-verified). Current packaging inside ServiceNow assumed unchanged in function.
