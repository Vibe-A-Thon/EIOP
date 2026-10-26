# C08 RAGFlow

| Field | Value |
|---|---|
| Registry ID | T-C08-ragflow |
| Tier | B (OSS RAG engine with graph mode; large adoption) |
| Versions examined | `infiniflow/ragflow` tag v1.0.0-rc2 (pre-release; rc1 announced 2026-09-29); PyPI `ragflow-sdk` 0.27.3 (2026-10-23); HEAD commit 2026-10-26 |
| Verified on | 2026-10-26 |
| Worker | V20 |

## 1. Identity, status, sources
RAGFlow by InfiniFlow: open-source RAG engine with deep document parsing (DeepDoc), chunk templates, agent workflows and knowledge-graph construction. Apache-2.0, ~92.9k stars, very active (commit on the check date) [CLAIM-rf-01]. Release line is moving from 0.27.x to **1.0.0 release candidates** (rc1 2026-09-29, rc2 tagged) [CLAIM-rf-01, -02]. The current README describes a "Knowledge Compilation" capability producing wikis, graphs, trees, PageIndex, mind maps, timelines and skills [CLAIM-rf-01]. Not related to Flowise or the RAGFlow-named forks (name check only).

## 2. Problem and workloads
Turn heterogeneous documents (PDF layout, tables, OCR) into retrievable chunks with citations, then chat/agent over them. Graph mode is an optional enrichment step between chunking and indexing. Target: team knowledge bases, enterprise search, agentic retrieval ("Low/Medium/High/Ultra thinking modes") [CLAIM-rf-01].

## 3. Feature inventory
| Feature | Status |
|---|---|
| Document parsing (layout, OCR, tables; CPU inference) | present [CLAIM-rf-01] |
| Hybrid retrieval, rerank, citations | present (docs; details not re-verified) |
| KG construction: method General (GraphRAG prompts) or Light (LightRAG prompts, default) | present [CLAIM-rf-03] |
| Entity resolution (LLM merge) | optional, off by default [CLAIM-rf-03] |
| Community reports | optional, off by default [CLAIM-rf-03] |
| Doc stores: Elasticsearch, Infinity | present [CLAIM-rf-01] |
| Agent canvas, templates, Browser component | present |
| Source-ACL propagation | absent / UNVERIFIED (workspace/team level only) |
| MCP | not mentioned on README (a separate MCP server may exist, UNVERIFIED) |
| Air-gap guide | not documented; setup downloads models/libs (inference) |

## 4. Architecture
```
upload -> DeepDoc parse -> chunk (template) -> [optional KG step: LLM extract (General|Light) -> entity resolution -> community reports]
       -> embed -> Elasticsearch | Infinity (text + vector + graph artefacts as documents)
query  -> hybrid retrieve (+ KG retrieval of entities/relations/community) -> rerank -> LLM with citations
agents -> canvas workflow engine over the same retrieval
```
Services: web/API server, task executor workers, MySQL, MinIO, Redis, doc engine (Docker Compose).

## 5. Under-the-hood reconstruction
Graph artefacts are stored inside the document engine rather than a graph database (inference from docs describing KG as an indexing step, 0.6); graph is rebuilt per knowledge base. The blog notes a deduplication step added to the original GraphRAG, which used extracted names directly [CLAIM-rf-03]. Concurrency via task-executor queue (Redis). Tenancy = user/team + knowledge-base objects. Docs warn that KG construction needs significant memory, compute and tokens [CLAIM-rf-03].

## 6. Requirements inferred
Layout-aware parsing; pluggable doc engine; token-cheap default graph method; opt-in costly steps; citation-bearing chunks.

## 7. Performance and resource model
Recommended deployment: 4 CPU cores, 16 GB RAM, 50 GB disk, Docker 24+, Compose v2.26.1+ [CLAIM-rf-01]. No independent benchmark of graph-mode benefit found; vendor does not claim one in the sources read. Cost driver: LLM calls at KG build; entity resolution and reports multiply tokens [CLAIM-rf-03]. GraphRAG-style gain over plain RAG is unproven here [CLAIM-rf-04].

## 8. Strengths
Best-in-class open-source document parsing for messy enterprise files; opinionated, deployable stack; Light default avoids community-summary cost; large community. Adoptable as an *ingestion front-end* producing SourceEvents.

## 9. Limitations
Operational: heavy five-service stack, high RAM; macOS unsupported; 1.0 only at RC. Algorithmic: graph is a retrieval aid, not a governed model (no ontology, no claim/evidence separation). Friction: fast-moving config between versions (Method option absent in v0.27.0 docs excerpt). Licensing: RAGFlow Apache-2.0, but defaults pull Elasticsearch (licence set includes SSPL/ELv2/AGPL options per Elastic; legal-review trigger if bundled) and MySQL/MinIO (MinIO is AGPL-3.0; **legal-review trigger**, from memory, not re-verified).

## 10. Deployment and licensing
Self-hosted Docker; air-gap needs pre-seeded images/models (partial). Apache-2.0 code permits embedding; bundled infrastructure licences need review. No tenant isolation beyond app-level.

## 11. Delta vs EOIP baseline
EOIP has JSON profiling and governed pipeline (BL-26, BL-23) but no unstructured/layout parsing (CAP-32 Absent) and weak vectors (BL-14). RAGFlow's parsing could feed EOIP; its graph and retrieval would bypass the governance chain (connectors must not mutate graph; BL-23) and ACL (BL-18).

## 12. Cards
| ID | Card |
|---|---|
| STR-ragflow-01 | Layout-aware document parsing with chunk templates and citations; CLAIM-rf-01; value: enterprise PDFs/tables ingestion; **integrate** as optional parser worker; design: run DeepDoc as a connector-side parser emitting versioned SourceEvents with chunk spans and source ACL; never write graph; acceptance: parsing outputs round-trip to evidence manifests, ACL preserved, runs offline |
| STR-ragflow-02 | Cheap-by-default graph method with opt-in costly steps; CLAIM-rf-03; **match** (cost tiers in EOIP extraction policy) |
| INV-ragflow-01 | Graph is an unmanaged index artefact (coupling/governance, proven by architecture description at 0.6). Options: (1) use RAGFlow end-to-end [bypasses governance, rejected]; (2) parser-only integration (selected); (3) differentiated: governed graph with claims. POC: parse 500 mixed PDFs, compare extraction quality vs current ingest, success: table fidelity and span provenance. Decision **EXPERIMENT**. No seed hypothesis targets it. |

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-32 parsing | INTEGRATE (optional worker) |
| CAP-56 graph mode | REJECT as retrieval layer; reuse the idea of tiered cost |
| CAP-54/55 retrieval | REUSE existing; DEFER |

## 14. Tests
Offline install with pre-pulled images; parse corpus with scanned/table-heavy PDFs; compare against plain text extraction; verify no network egress during parse (egress gateway BL-45).

## 15. Risks and questions
RC stability; infra licence stack; GPU needs for OCR/layout at scale; data egress when an LLM is configured.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Apache-2.0, RC |
| D2 | 2 | RAG engine |
| D3 | 4 | multi-service |
| D4 | 5 | doc engine, no graph DB |
| D5,D7,D11,D12 | N/A | no semantic layer |
| D6 | 5 | hybrid + KG retrieval |
| D8 | 7,9 | Redis task queue, resources |
| D9 | 3 | file upload; sync connectors UNVERIFIED |
| D10 | 9 | citations; no ACL |
| D13 | 3,4 | agentic retrieval |
| D14 | N/A | no text-to-query |
| D15-D17 | 3 | UI/SDK |
| D18-D19 | 9 | app-level |
| D20 | 7 | sizing |
| D21 | 10 | OSS + infra licences |
| D22 | 5 | data in doc engine |
| D23 | N/A | none |
| D24 | 7 | vendor docs only |

## Appendix B. Capability mapping
| CAP | This tech | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-32 | native | rf-01 | Absent | INTEGRATE | P1 |
| CAP-56 | partial | rf-03 | BL-16 | REJECT | P3 |
| CAP-53/55 | native | rf-01 | BL-14/15 | DEFER | P2 |
| CAP-46 | absent | rf-01 | BL-18 Absent | BUILD | P0 |

## Appendix C. Evidence records
| CLAIM | Product/version/date | Claim | Class | Source | Dates/conf | Contradiction |
|---|---|---|---|---|---|---|
| rf-01 | README, 1.0.0-rc | Apache-2.0; 92.9k stars; Knowledge Compilation outputs; ES and Infinity; 4 CPU/16 GB/50 GB; macOS unsupported; agentic retrieval modes | Officially documented | github.com/infiniflow/ragflow | acc 2026-10-26; 0.85 | none |
| rf-02 | tags/PyPI | v1.0.0-rc1/rc2 tags; ragflow-sdk 0.27.3 on 2026-10-23, Apache-2.0 | Officially documented | github.com tags (git ls-remote), pypi.org/project/ragflow-sdk | acc 2026-10-26; 0.9 | none |
| rf-03 | dev docs | KG method General vs Light (default); entity resolution and community reports off by default and token-costly; high memory/compute; blog: dedup added to GraphRAG | Officially documented | ragflow.io/docs/dev/construct_knowledge_graph (via search snippet), ragflow.io/blog/ragflow-support-graphrag | acc 2026-10-26; 0.7 (direct page fetch returned 404; snippet-based) | v0.27.0 docs omit Method |
| rf-04 | arXiv:2506.05690 | GraphRAG frequently underperforms vanilla RAG on real tasks | Independent benchmark (abstract) | arxiv.org/abs/2506.05690 | 2025-06 rev 2026-02; 0.7 | vendor positioning |

## Appendix D. Assumptions
Infra licence statements (Elasticsearch, MinIO) are from general knowledge and flagged for legal review, not verified this session.
