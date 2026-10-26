| Field | Value |
|---|---|
| Registry ID | T-C07-writer-kg |
| Tier | B (graph-based RAG product) |
| Versions examined | Writer AI Studio Knowledge Graph, docs as of 2026-10-26; RobustQA report June 2024; RAG tool post Dec 2024 |
| Verified on | 2026-10-26 (brief date 2026-10-18; actual access date used) |
| Worker | V19 |

## 1. Identity, current status, tier, sources
Writer, Inc. (enterprise generative-AI platform; Palmyra LLMs). "Knowledge Graph" is a managed graph-based RAG feature: documents/connectors are processed into a searchable graph and queried by natural language. Proprietary SaaS. Not a general graph database. Sources: Writer product page, dev.writer.com concepts and API pages, Writer RobustQA post, ZenML case write-up [CLAIM-wri-01..05]. Existing relatives: C07-glean-enterprise, C07-onyx (enterprise RAG).

## 2. Problem and workloads
Ground enterprise chat/apps/agents on company content with citations. Workflow: upload files or connect Confluence/Notion/Google Drive/SharePoint or crawl a website -> graph built -> call `POST /v1/graphs/question` (graph IDs + question, optional subqueries) or use the KG tool inside chat completions [wri-01,02]. EOIP overlap: CAP-55/56/60.

## 3. Feature inventory
| Feature | Status | Evidence |
|---|---|---|
| File ingest (PDF, DOCX, PPTX, CSV, XLSX, EML, HTML, SRT, TXT) | present | wri-01 |
| Connectors: Confluence, Notion, Google Drive, SharePoint | present | wri-01 |
| Website crawl with auto refresh | present | wri-01 |
| Entity/concept/relationship graph built automatically | present (vendor description) | wri-01 |
| Multi-graph query, subqueries, streaming | present | wri-01, wri-02 |
| Inline citations; query config (search weight, grounding level, max snippets/tokens, thresholds) | present | wri-01, wri-02 |
| Graph query language / direct graph access | not documented | |
| Source-ACL enforcement | NOT PUBLICLY VERIFIED | |
| Self-hosted / VPC / air-gap | NOT PUBLICLY VERIFIED | |
| Explicit schema/ontology control | not documented | |

## 4. Architecture diagram
```
Files/Connectors/Web -> parse -> LLM extract (entities, relations) -> graph + index
Question -> (optional subquery decomposition) -> graph traversal + snippet retrieval
 -> Palmyra generation w/ grounding-level + citations -> answer + sources
```
Hypothesis per vendor text; ZenML account adds JSON graph data in Lucene-based search and fusion-in-decoder (secondary, vendor-origin) [wri-04].

## 5. Under-the-hood reconstruction
Verified from docs: graph is an index built by a model; retrieval traverses it; generation is grounded with tunable parameters [wri-01,02]. Vendor/secondary claims: no chunking, JSON graph in Lucene, FiD generator [wri-04, wri-05]. Not verified: node/edge schema, extraction prompts, update/invalidation, tenancy model, consistency. Reconstruction for EOIP: entity-relation extraction -> evidence span store -> hybrid index; EOIP BL-16/BL-15 already approximate retrieval; the missing part is LLM-built graph construction with extraction QA.

## 6. Inferred requirements
Doc-to-graph extraction with citation spans; connector refresh; configurable grounding strictness (maps to CAP-60 abstention); multi-graph scoping per tenant/app.

## 7. Performance and resource model
Vendor claim: 86.31% on RobustQA vs 32.74-75.89% for compared vector systems, avg response under 0.6 s [wri-03]. This is a vendor-run single 2024 report; hardware, dataset configuration, and baseline tuning are not independently verified; an independent paper (arXiv 2506.05690, "When to use Graphs in RAG") finds graph RAG benefits are task-dependent, not uniform [wri-06, confidence 0.5]. No cost model published in sources read.

## 8. Strengths
Zero-ops managed graph-RAG with connectors, citations and tunable grounding. Match: EOIP retrieval with citations (BL-16, cited-span checks in recent commits) plus a graph-build pipeline; exceed via ACL-aware retrieval and local models.

## 9. Limitations
Vendor claim, not independent: accuracy superiority. Intentional: opaque graph, no query access, no schema control. Licensing: proprietary SaaS. User complaints: none retrieved. Hypotheses: permission handling for connectors unclear; graph rebuild cost on change.

## 10. Deployment/licensing/viability
SaaS; self-host/air-gap NOT PUBLICLY VERIFIED so treated as no. Cannot be embedded or white-labelled by EOIP. Legal trigger: Writer terms for content processing and model use.

## 11. Competitive delta
Baseline: BL-16 GraphRAG deterministic (no benchmark vs plain RAG noted in baseline), BL-18 ACL absent, BL-14 hashing embedder default, BL-12 LLM hook partial. Writer's connectors-to-answer path is smoother; EOIP's potential edge (ACL, provenance, local) depends on closing BL-18 first.

## 12. Cards
STR-wri-01 | Writer | One-call graph RAG with citations and grounding-level tuning | wri-01,02 | value: low-ops Q&A | match | expose grounding-level and abstention config on retrieval API | test: unsupported-claim rate under strict level on 100-question set.
INV-wri-01 | Writer | Accuracy claim lacks reproducible methodology | wri-03,06 | root cause: maturity/semantics (hypothesis) | alt: publish EOIP's own reproducible harness (CAP-78); worse if harness bias | options: (1) adopt RobustQA-style eval, (2) native harness comparing plain vs graph RAG, (3) per-tenant continuous eval | selected 2 | POC: same corpus, three retrievers, metric = answer correctness + citation precision, baseline = BM25+vector | defensibility: tenant-specific eval | decision ADOPT. §10.5 seed hypotheses targeting Writer: none identified.

## 13. Per-capability decisions
CAP-56 GraphRAG: EXPERIMENT (benchmark first). CAP-60 grounded answers: BUILD tuning knobs. CAP-78 eval harness: BUILD. CAP-26 connectors: REFERENCE list. Writer product: REJECT as dependency.

## 14. Tests/POC
Build same-corpus A/B: plain hybrid vs graph-traversal retrieval; report on EOIP corpus; check citation precision; verify abstention.

## 15. Risks and open questions
Whether Writer offers VPC/self-host; ACL fidelity; benchmark replicability; pricing.

## Appendix A — Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | proprietary SaaS |
| D2 | 2 | enterprise Q&A |
| D3 | 4 | hypothesis |
| D4 | 5 | JSON in Lucene (secondary) |
| D5 | N/A | no schema control documented |
| D6 | 3 | NL only |
| D7 | N/A | none |
| D8 | N/A | SaaS |
| D9 | 3 | connectors, crawl |
| D10 | 3 | citations |
| D11 | 3 | auto refresh |
| D12 | N/A | |
| D13 | 3,5 | core |
| D14 | N/A | |
| D15 | N/A | |
| D16 | N/A | |
| D17 | 2 | REST/SDK, LangChain tool |
| D18 | 3,9 | ACL unverified |
| D19 | N/A | |
| D20 | 7 | vendor claim |
| D21 | 10 | proprietary |
| D22 | 9 | no export documented |
| D23 | N/A | |
| D24 | 7 | vendor claims flagged |

## Appendix B — Capability mapping
| CAP | Technology | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-56 | native (vendor) | wri-01 | BL-16 | EXPERIMENT | P2 |
| CAP-60 | native | wri-01,02 | BL-16 | BUILD knobs | P1 |
| CAP-26 | native | wri-01 | BL-23 | REFERENCE | P3 |
| CAP-78 | absent | - | BL-07 partial | BUILD | P1 |
| CAP-46 | unknown | - | BL-18 Absent | BUILD | P0 |

## Appendix C — Evidence records
| CLAIM | product/date | claim | class | source | pub/access | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| wri-01 | Writer KG | Ingest types, connectors, crawl, graph of entities/relationships, graph traversal retrieval, citations | Officially documented | https://dev.writer.com/home/knowledge-graph-concepts | n/d / 2026-10-26 | 0.8 | |
| wri-02 | Writer API | POST /v1/graphs/question, graph IDs, subqueries, answer + sources | Officially documented | https://dev.writer.com/home/kg-query.md | n/d / 2026-10-26 | 0.7 | |
| wri-03 | Writer RobustQA | 86.31% vs 32.74-75.89%; <0.6 s avg (vendor claim) | Third-party report of vendor claim | https://writer.com/blog/rag-benchmark/ ; https://thenewstack.io/writer-coms-graph-based-rag-alternative-to-vector-retrieval/ | 2024-06 / 2026-10-26 | 0.4 | independent paper wri-06 |
| wri-04 | Writer architecture | JSON graph in Lucene-based search, fusion-in-decoder | Third-party report | https://www.zenml.io/llmops-database/evolution-from-vector-search-to-graph-based-rag-for-enterprise-knowledge-systems | 2025 / 2026-10-26 | 0.35 | vendor-origin |
| wri-05 | Writer product page | graph-based RAG avoids chunking | Officially documented (vendor) | https://writer.com/product/graph-based-rag/ | n/d / 2026-10-26 | 0.4 | page returned 403 to fetch; search summary only |
| wri-06 | Independent study | Graph RAG benefits task-dependent | Independent paper | https://arxiv.org/pdf/2506.05690 | 2025 / 2026-10-26 | 0.5 | abstract-level only |

## Appendix D — Assumptions
Registry means Writer AI Studio Knowledge Graph. Deployment and ACL left unknown rather than assumed. Cross-ref C07-glean-enterprise for permission-aware retrieval.
