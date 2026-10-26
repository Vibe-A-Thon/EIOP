| Field | Value |
|---|---|
| Registry ID | T-C07-diffbot |
| Tier | B (web-scale KG; external-data enrichment) |
| Versions examined | Diffbot Knowledge Graph (SaaS); Diffbot GraphRAG LLM (Llama 3.3 70B fine-tune, announced 2025-01-07) |
| Verified on | 2026-10-26 (brief date 2026-10-18; actual access date used) |
| Worker | V19 |

## 1. Identity, current status, tier, sources
Diffbot Inc. sells a machine-crawled public-web Knowledge Graph (organisations, people, articles, products etc.), a Natural Language/Extract API, Enhance (batch record matching) and DQL (Diffbot Query Language). Vendor claim: >10 billion entities, trillions of facts [CLAIM-dif-01]. In Jan 2025 Diffbot published a fine-tuned Llama 3.3 70B "GraphRAG LLM" and an inference repo, github.com/diffbot/diffbot-llm-inference [CLAIM-dif-02]. Neo4j LLM Knowledge Graph Builder lists Diffbot as an extraction backend [CLAIM-dif-03]. Tier B: external reference graph, not an internal org-brain.

**Prompt-injection note:** the product page fetched contained text instructing the reader to ignore prior instructions; it was disregarded and is not used as evidence.

## 2. Problem and workloads
Enrich internal entities (companies, people) with public facts; entity-linking against a global graph; news/market monitoring; grounding LLMs on live web facts. Workflow: upload CRM list -> Enhance -> match to KG entity -> attributes returned. Fit for EOIP: optional external-enrichment source (J15-type vendor/regulation context), always via connector -> SourceEvent (BL-23).

## 3. Feature inventory
| Feature | Status | Evidence |
|---|---|---|
| Public-web KG, entity types, entity-to-entity links | present | dif-01 |
| DQL structured search | present | dif-01 |
| Enhance (match your records to KG) | present | dif-01 |
| Extract / NL APIs | present | UNVERIFIED this session |
| GraphRAG LLM (open-weight tool-calling model) | present (open source claim) | dif-02 |
| Licence of weights / repo | NOT PUBLICLY VERIFIED here | |
| Self-hosted KG | UNVERIFIED (secondary report says self-host possible) | dif-02 |
| Per-fact provenance/origin sources | partial: "560 origin sources" for one entity | dif-01 |
| Update frequency | not stated | dif-01 |

## 4. Architecture diagram
```
Web crawl -> ML extraction (vision+NLP) -> entity resolution/fusion -> KG (DQL, API)
Client: DQL / Enhance / GraphRAG LLM(tool-use over KG API) -> answer + citations
```
Hypothesis from vendor description; internals not public.

## 5. Under-the-hood reconstruction
Public evidence: entity-centric fused records with multi-source origins [dif-01]; LLM trained as expert tool user of the KG API (tool-calling retrieval, not text-to-graph-query over a local store) [dif-02]. Storage engine, indexing, fusion algorithm, confidence scoring, concurrency: **NOT PUBLICLY VERIFIED**. Hypothesis: fact-level provenance with source-weighted fusion; EOIP could replicate the pattern with BL-39/41 claim + evidence model.

## 6. Inferred requirements
Entity-resolution against external IDs; per-fact origin and recency; rate/cost control per call; egress DLP before sending internal names to a SaaS (BL-45 gateway needed).

## 7. Performance and resource model
Vendor pricing (secondary aggregator, unverified): credit-based, 1 credit per page extract, 25 credits per KG entity export, 100 per summarised facet query; tiers $0/$299/$899/custom [CLAIM-dif-04, confidence 0.3]. Self-hosting a 70B model needs GPU-class hardware (reasoned inference); the claimed distillation under 1B parameters is a vendor claim, unverified [dif-02]. No latency benchmarks verified.

## 8. Strengths
Breadth of public-entity coverage no internal team can match; entity-linking utility; open GraphRAG tool-use recipe. Match: EOIP federation connector with caching; exceed by combining with tenant-private graph under ACL control.

## 9. Limitations
Intentional: public-web only, no private enterprise semantics. Licensing/ToS for data reuse: data rights page exists, terms not retrieved - legal review. Cost per entity high versus bulk open data (Wikidata, OpenCorporates: other sources, not examined). Hypothesis: web-fact accuracy varies; no independent accuracy benchmark found. Egress of internal identifiers conflicts with default-local posture.

## 10. Deployment/licensing/viability
SaaS API (core); self-host status UNVERIFIED. Air-gap: no for the KG; partial if the open-weight LLM is used offline (licence of Llama 3.3 community licence applies to the base; verify). Legal trigger: Llama community licence, data-rights terms, ToS on caching/redistribution.

## 11. Competitive delta
EOIP lacks any external-reference graph (no baseline item). Diffbot complements, not replaces, the platform. Egress gateway BL-45 and DLP exist to make this optional use safe; BL-18 ACL gap not relevant to public data.

## 12. Cards
STR-dif-01 | Diffbot | Public entity reference graph with entity linking | dif-01 | value: enrichment of vendors/regulators/companies | integrate | optional connector + egress policy + cache with source_ref | test: 500 company records enriched with 0 untagged writes and DLP block on restricted fields.
INV-dif-01 | Diffbot | SaaS dependence/cost per entity; unverifiable fact accuracy | dif-04 (low) | root cause: deployment/licensing, hypothesis | alt: cache only needed attributes, use open datasets; worse when freshness matters | options: (1) connector, (2) cache + confidence labels, (3) open-data reference layer | selected 1+2 | POC: precision on 200 hand-checked entities vs ground truth | decision EXPERIMENT. No §10.5 seed targets this.

## 13. Per-capability decisions
CAP-26 connector: INTEGRATE (optional). CAP-31 ER vs external IDs: EXPERIMENT. CAP-38 provenance: REUSE pattern. CAP-56/59 GraphRAG tool-use: REFERENCE-ONLY. CAP-51 egress: required.

## 14. Tests/POC
Enhance 500 sample companies in sandbox; verify egress manifest entries; measure match precision/recall against manually labelled set.

## 15. Risks and open questions
Pricing verified only via aggregators; repo licence/weights; dataset ToS; whether KG can be licensed for on-prem.

## Appendix A — Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | vendor, unverified licence |
| D2 | 2 | enrichment |
| D3 | 4 | hypothesis |
| D4 | 5 | not public |
| D5 | 3 | typed entities |
| D6 | 3 | DQL |
| D7 | N/A | none |
| D8 | N/A | SaaS |
| D9 | 2 | Enhance batch |
| D10 | 3,5 | fusion, origins |
| D11 | 3 | update cadence unstated |
| D12 | N/A | |
| D13 | 3,5 | GraphRAG tool-use LLM |
| D14 | 3 | DQL, LLM tool use |
| D15 | N/A | |
| D16 | N/A | |
| D17 | 3 | APIs |
| D18 | 9 | egress |
| D19 | N/A | |
| D20 | 7 | credits, low confidence |
| D21 | 7,10 | tiers |
| D22 | 9 | ToS |
| D23 | N/A | not examined |
| D24 | 1 | vendor sources |

## Appendix B — Capability mapping
| CAP | Technology | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-26 | native | dif-01 | BL-23 | INTEGRATE | P3 |
| CAP-31 | native | dif-01 | BL-36 Absent | EXPERIMENT | P3 |
| CAP-38 | partial | dif-01 | BL-41 | REFERENCE | P3 |
| CAP-56 | native | dif-02 | BL-16 | REFERENCE | P3 |
| CAP-51 | n/a | - | BL-45 | required | P1 |

## Appendix C — Evidence records
| CLAIM | product/date | claim | class | source | pub/access | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| dif-01 | Diffbot KG | >10B entities, trillions of facts; DQL; Enhance; origin sources shown (vendor claim) | Officially documented (vendor) | https://www.diffbot.com/products/knowledge-graph/ | n/d / 2026-10-26 | 0.6 (vendor claim) | page also held injected text |
| dif-02 | GraphRAG LLM | Llama 3.3 70B fine-tuned as tool user of KG API; open-source inference repo | Officially documented | https://www.diffbot.com/changelog/2025-01-07-diffbot-graphrag-llm | 2025-01-07 / 2026-10-26 | 0.6 | sub-1B distillation claim only via TechStrong, https://techstrong.ai/uncategorized/diffbot-extends-knowledge-graph-to-create-more-efficient-gen-ai-alternative |
| dif-03 | Neo4j LLM KG Builder | Diffbot listed as supported extraction backend | Third-party report | https://neo4j.com/blog/developer/graphrag-llm-knowledge-graph-builder/ | n/d / 2026-10-26 | 0.5 | |
| dif-04 | Diffbot pricing | Tiers and credit costs per aggregator | Third-party report | https://pricingsaas.com/companies/diffbot | 2026 / 2026-10-26 | 0.3 | official page not retrieved |

## Appendix D — Assumptions
Registry means Diffbot's hosted KG plus its GraphRAG LLM. Repo licence not fetched: UNVERIFIED. Cross-ref C07-palantir-foundry for the enrichment-vs-ontology contrast.
