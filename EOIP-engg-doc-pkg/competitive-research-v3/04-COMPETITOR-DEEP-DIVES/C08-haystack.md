# C08 Haystack (deepset)

| Field | Value |
|---|---|
| Registry ID | T-C08-haystack |
| Tier | B (OSS RAG/agent pipeline framework; relevant for pipeline patterns) |
| Versions examined | PyPI `haystack-ai` 3.4.1 (2026-10-21); tag v3.5.0-rc0; HEAD commit 2026-10-24 |
| Verified on | 2026-10-26 |
| Worker | V20 |

## 1. Identity, status, sources
Haystack, by deepset (deepset-ai/haystack), Apache-2.0, active (3.4.1 released five days before check; 3.5.0 RC tagged) [CLAIM-hay-01]. A modular Python framework of components wired into typed pipelines (retrieval, ranking, generation, agents), with a hosted/enterprise offering from deepset (details not verified). Major version 3.x: migration cost from 2.x not assessed.

## 2. Problem and workloads
Production RAG and agentic search: pipelines of Retrievers, Rankers, Generators, Routers, Converters; document stores via integrations. Workloads: semantic/hybrid search, QA, agents with tools.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Component/pipeline model with typed sockets, serialisation to YAML | present (from knowledge, 0.6) |
| Document stores: Elasticsearch, OpenSearch, Qdrant, pgvector, Weaviate, Neo4j, FalkorDB | present as integrations [CLAIM-hay-02] |
| Graph-memory: Cognee memory store (deepset-maintained) | present as integration [CLAIM-hay-02] |
| Text-to-Cypher / text-to-SPARQL components | **none listed** [CLAIM-hay-02] |
| Hybrid retrieval + rerank, evaluation components | present (from knowledge, 0.6) |
| Tracing (OpenTelemetry, Langfuse etc.) | present via integrations (0.5) |
| Source ACL / tenancy | absent in core (metadata filters only, hypothesis) |
| Local models (Ollama, llama.cpp, HF) | present via integrations (0.6) |

## 4. Architecture
```
Pipeline (directed graph of components, may loop for agents)
 [Converter] -> [Splitter] -> [Embedder] -> [DocumentWriter] -> DocumentStore (ES|OS|Qdrant|pgvector|Neo4j|FalkorDB)
 query: [Embedder] -> [Retriever(s)] -> [Joiner/RRF] -> [Ranker] -> [PromptBuilder] -> [Generator]
```
Library only; no server (Hayhooks / deepset Cloud are separate, UNVERIFIED here).

## 5. Under-the-hood reconstruction
Typed component interface (`run()` with declared inputs/outputs), pipeline validation of socket connections, async execution, serialisation of the DAG. Reciprocal rank fusion joiner is a stock component (from knowledge, 0.6). Pattern for EOIP: the same typed-component idea can express EOIP's retrieval pipeline stages with explicit permission filter components; no new storage concept.

## 6. Requirements inferred
Typed, inspectable, serialisable pipelines; swappable stores; evaluation components next to pipeline.

## 7. Performance
No framework-level benchmark relevant; throughput is that of the stores and models. Not claimed.

## 8. Strengths
Clean pipeline abstraction, broad store support, Apache-2.0, enterprise-oriented maintenance. Match by keeping EOIP retrieval stages as typed components with serialisable definitions (config-as-code per tenant).

## 9. Limitations
No graph reasoning of its own; graph is storage-adjacent only. No ACL propagation; no text-to-query; major-version churn (3.x). Friction: Python-only runtime, dependency weight (hypothesis).

## 10. Deployment and licensing
Apache-2.0 library; embeddable in FastAPI; air-gap viable with local models and stores. No legal trigger noted for the core; store integrations carry the stores' own licences (FalkorDB SSPL: see C01-falkordb.md).

## 11. Delta vs EOIP baseline
EOIP already has hybrid RRF (BL-15), deterministic retrieval (BL-16), observability (BL-49). Haystack adds a component ecosystem and evaluation tooling EOIP lacks as a benchmark harness (CAP-78); no capability EOIP needs that it cannot match.

## 12. Cards
| ID | Card |
|---|---|
| STR-haystack-01 | Typed, serialisable component pipelines with swappable stores; CLAIM-hay-01/02; value: per-tenant retrieval configuration; **match**; design: stage interface for EOIP retrieval with mandatory ACL-filter stage that cannot be omitted by config; acceptance: pipeline definition validates only if ACL stage present |
| INV-haystack-01 | No ACL/tenant awareness in framework (proven by absence in listing, hypothesis for core). Options: (1) use Haystack plus custom filters, (2) EOIP-native stage runner (selected), (3) differentiated: policy-compiled pipelines. POC: leakage canary suite on the pipeline. Decision **DEFER** adopting; **REFERENCE** pattern. No seed hypothesis targets it. |

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-55 hybrid/rank fusion | REUSE own RRF (BL-15) |
| CAP-78 evaluation | EXPERIMENT using Haystack eval components or similar as harness |
| Pipeline abstraction | BUILD thin typed stage runner (REFERENCE) |
| CAP-58 NL-to-query | absent upstream; see C08-text-to-query.md |

## 14. Tests
Spike: express BL-16 retrieval as Haystack pipeline offline with Ollama; compare overhead and ACL-stage enforceability.

## 15. Risks and questions
3.x migration stability; deepset commercial direction; whether graph integrations are maintained.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Apache-2.0 active |
| D2 | 2 | RAG pipelines |
| D3 | 4 | library |
| D4-D8,D11,D12,D15,D22 | N/A | storage via integrations; no semantic layer |
| D9 | 4 | converters/writers |
| D10 | 9 | no ACL |
| D13 | 3,5 | retrieval pipelines |
| D14 | 3 | none |
| D16 | N/A | no UI in core |
| D17 | 5,8 | typed components |
| D18-D19 | 9 | none |
| D20 | 7 | N/A |
| D21 | 10 | Apache |
| D23 | N/A | none |
| D24 | 1 | PyPI/GitHub/integrations page |

## Appendix B. Capability mapping
| CAP | This tech | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-55 | native | hay-01 | BL-15 | REUSE own | P3 |
| CAP-53 | plugin | hay-02 | BL-14 | DEFER | P3 |
| CAP-78 | partial | hay-01 | Unknown | EXPERIMENT | P2 |
| CAP-58 | absent | hay-02 | BL-11/12 | n/a | P3 |

## Appendix C. Evidence records
| CLAIM | Product/version/date | Claim | Class | Source | Dates/conf | Contradiction |
|---|---|---|---|---|---|---|
| hay-01 | haystack-ai 3.4.1, 2026-10-21 | Apache-2.0; v3.5.0-rc0 tag; commit 2026-10-24 | Officially documented | pypi.org/project/haystack-ai; github.com/deepset-ai/haystack | acc 2026-10-26; 0.9 | none |
| hay-02 | integrations page | Document stores listed (ES, OpenSearch, Qdrant, pgvector, Weaviate, Neo4j, FalkorDB); Cognee memory store; no text-to-Cypher/SPARQL components listed | Officially documented | haystack.deepset.ai/integrations | acc 2026-10-26; 0.7 (page may be partial) | none |

## Appendix D. Assumptions
Pipeline internals recalled from general knowledge (0.5-0.6) because docs pages were not fetched in detail.
