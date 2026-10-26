# C05 LLM schema-guided extraction (Neo4j LLM Graph Builder; LlamaIndex property-graph extractors)

| Field | Value |
|---|---|
| Registry ID | T-C05-llm-schema-extraction |
| Tier | B (competitor extraction pattern) |
| Versions examined | neo4j-labs/llm-graph-builder (no release tag shown); llama-index-core 0.14.25; langchain-experimental 0.4.2 |
| Verified on | 2026-10-18 (re-read 2026-10-26) |
| Worker | V17 |

## 1. Identity, current status, tier, and sources
Two named members plus the shared LangChain transformer.
| Member | Owner | Licence | Status |
|---|---|---|---|
| Neo4j LLM Graph Builder | Neo4j Labs | Apache-2.0 | "experimental Neo4j Labs project, not part of the supported product lineup" [CLAIM-llmx-01] |
| LlamaIndex property-graph extractors (`SimpleLLMPathExtractor`, `DynamicLLMPathExtractor`, `SchemaLLMPathExtractor`, `ImplicitPathExtractor`) | LlamaIndex | MIT (llama-index-core 0.14.25) | active [CLAIM-llmx-02] |
| LangChain `LLMGraphTransformer` (used by the Graph Builder per its docs) | LangChain | MIT, package `langchain-experimental` 0.4.2 | package says "being sunset" [CLAIM-llmx-03] |
Retrieval side is covered in `C08-llamaindex-pgi.md` and `C08-neo4j-graphrag.md`; this record covers extraction only.

## 2. Primary problem, workloads, workflows
Turn text chunks into entity/relation triples with an LLM, optionally constrained by a node/relationship schema, and write them to a graph with a link back to the source chunk.

## 3. Feature inventory
| Feature | Graph Builder | LlamaIndex |
|---|---|---|
| Schema (node/rel types) | UI-configurable, improves quality [CLAIM-llmx-04] | `SchemaLLMPathExtractor` with Pydantic validation; `strict=True` rejects out-of-schema triples [CLAIM-llmx-05] |
| Loose typing hints | n/a | `DynamicLLMPathExtractor` suggests, does not enforce |
| Chunk provenance | Document->Chunk->Entity links [CLAIM-llmx-04] | `include_text`, `HAS_SOURCE` pattern [CLAIM-llmx-05] |
| Local LLM | Ollama via env config [CLAIM-llmx-01] | any `llm` object |
| Char offsets / evidence spans | absent (chunk-level only) | absent |
| Backends | Neo4j 5.23+ with APOC only | Neo4j, TiDB, FalkorDB, Nebula, in-memory [CLAIM-llmx-05] |
| UI | React front-end | none |
| Inputs | PDF, docs, web, YouTube, S3/GCS | via loaders |

## 4. Architecture
```
file/url -> loader -> chunks (Chunk nodes, SIMILAR kNN edges, embeddings)
chunk -> LLM prompt (+schema) -> JSON/tool-call triples -> [validate vs schema]
 -> MERGE nodes/edges -> (Chunk)-[:HAS_ENTITY]-(Entity)  [name from docs unverified]
chat: vector + graph retrieval over the same store
```

## 5. Under-the-hood reconstruction
Data model: Document, Chunk, Entity nodes with chunk-to-entity edges [CLAIM-llmx-04]. Chunk defaults: `MAX_TOKEN_CHUNK_SIZE` 10000, overlap 20 [CLAIM-llmx-01]. Extraction = one LLM call per chunk (cost therefore linear in chunks, hypothesis); entity identity is by name string, so duplicates and conflation are expected (error pattern reported in a social-network KG study) [CLAIM-llmx-06]. Strict schema mode is post-hoc filtering by Pydantic validation, not constrained decoding (reading of docs; hypothesis). No review state: triples are written as facts, unlike EOIP's PROPOSED-until-promoted contract (BL-40).

## 6. Requirements inferred
FR: schema from ontology; every triple carries chunk id and span; confidence; reject out-of-schema. NFR: bounded tokens per doc; deterministic re-run via cached prompts; local model default; egress policy.

## 7. Performance and resource model
No vendor throughput or accuracy numbers found. Independent: CEUR (ISWC 2025) compares `LLMGraphTransformer`, KGGen and GT2KG on three abstracts: precision/recall trade-off, predicate vocabulary differs from gold [CLAIM-llmx-07]; Springer 2025 reports precision lower than recall, spelling errors, node conflation [CLAIM-llmx-06]. Tiny samples; neither tests local models or hallucination rate. Cost and latency: NOT PUBLICLY VERIFIED for local models.

## 8. Strengths
Fast path from text to explorable graph; schema-constrained mode; chunk-level provenance; pluggable models; UI for demos. Exceed by adding spans, review state and ACL.

## 9. Limitations
Verified: best on long English text, weak on tables/images [CLAIM-llmx-04]; Graph Builder is Neo4j-only with APOC, Labs-grade support [CLAIM-llmx-01]. Package risk: LangChain transformer sunset [CLAIM-llmx-03]. Hypotheses: unconstrained local models violate schema often; cost grows with corpus; no ACL propagation to extracted entities (BL-18 gap would be repeated).

## 10. Deployment, licensing, viability
Apache-2.0/MIT, no copyleft. Air-gap viable only with local LLM and local embeddings (sentence-transformers default) [CLAIM-llmx-01]; default compose enables only OpenAI and Diffbot [CLAIM-llmx-01], so default-egress must be disabled. Graph Builder cannot serve HugeGraph/Neptune; LlamaIndex stores can.

## 11. Competitive delta
EOIP baseline: ontology proposals from JSON with review (BL-27), claims and boundary (BL-39/40), evidence manifests (BL-41), egress gateway (BL-45), LLM only via optional hook (BL-12). Missing: text-to-triple extraction. EOIP's design is stricter than both products (PROPOSED state, egress) but has no extractor.

## 12. Cards
STR-llmx-01 | LlamaIndex | Pydantic-validated schema-constrained triples | CLAIM-llmx-05 | ontology-bound extraction | match | validate against EOIP ontology manifest | out-of-schema rate <1% after validation.
STR-llmx-02 | Graph Builder | Document->Chunk->Entity provenance chain | CLAIM-llmx-04 | citation path | match, exceed with spans | add `SpanAnchor` | 100% triples have chunk id and span.
INV-llmx-01 | LLM triples written as facts, name-keyed entities, no spans (proven for provenance; conflation per CLAIM-llmx-06) | root: semantics/governance | options: quick (adopt extractor, route output to PROPOSED), native (rules -> GLiNER -> LLM cascade with evidence verifier), long-term (learned verifier trained on reviews). Select native cascade. Benchmark: triple P/R vs gold on 100 docs, LLM calls per doc, % triples with verified span. Defensible: review-queue labels. Validates seed hypothesis "deterministic first, local models second, LLM under policy" in direction; cost claim untested. Decision EXPERIMENT.
INV-llmx-02 | single-backend/Labs support (proven) | root: coupling | keep extraction backend-neutral via SourceEvent. ADOPT.

## 13. Per-capability decisions
CAP-32 RE/NER by LLM: EXPERIMENT (policy-gated, local default). CAP-28 schema-guided: REUSE pattern. CAP-38 spans/CAP-60 citations: BUILD. Graph Builder as product: REJECT (Neo4j-only); LlamaIndex extractors as library: EXPERIMENT; LLMGraphTransformer: REJECT as dependency (sunset).

## 14. Tests / PoC
100 docs with gold triples; 7-8B local model via Ollama, 4 vCPU or consumer GPU: strict vs loose schema, triples P/R, schema violations, duplicate-entity rate, calls and wall-clock per doc, verbatim-span verification rate; no external egress. Accept: >=95% accepted triples have verifiable span; out-of-schema <1%.

## 15. Risks / open questions
Local-model quality; prompt injection from ingested text steering extraction (CAP-49); extraction non-determinism vs replay (BL-24); ACL inheritance; upstream churn.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Labs/experimental; MIT/Apache |
| D2 | 2 | text to triples |
| D3 | 4 | LLM per chunk |
| D4 | 5 | Neo4j schema only |
| D5 | 3,5 | schema modes |
| D6-D8 | N/A | not engines |
| D9 | 2,11 | ingest stage |
| D10 | 5,9,12 | name-keyed, no spans |
| D11 | N/A | none |
| D12 | 7 | LLM extraction |
| D13 | 1 | see C08 files |
| D14 | N/A | none |
| D15 | 5,11 | no review |
| D16 | 3 | Graph Builder UI |
| D17 | 3 | extractors API |
| D18 | 15 | prompt injection |
| D19 | N/A | none |
| D20 | 7 | no numbers |
| D21 | 10 | permissive |
| D22 | 9 | Neo4j lock-in |
| D23 | N/A | none |
| D24 | 7 | small studies |

## Appendix B. Capability mapping
| CAP | This tech | CLAIM | EOIP baseline | Decision | P |
|---|---|---|---|---|---|
| CAP-32 | native | 04,05 | absent for text | EXPERIMENT | P2 |
| CAP-28 | partial | 05 | BL-26/27 | REUSE pattern | P2 |
| CAP-38 | partial (chunk) | 04 | BL-41 | BUILD | P1 |
| CAP-51 | partial | 01 | BL-45 | INTEGRATE policy | P1 |

## Appendix C. Evidence records
| CLAIM | Product/version/date | Claim | Class | Source | Dates | Confidence | Contra |
|---|---|---|---|---|---|---|---|
| llmx-01 | Graph Builder | Apache-2.0; Labs; Ollama; Neo4j 5.23+; defaults; chunk config | Officially documented | https://github.com/neo4j-labs/llm-graph-builder | 2026-10-26 | 0.85 | none |
| llmx-02 | llama-index-core 0.14.25 | MIT | Officially documented | https://pypi.org/pypi/llama-index-core/json | 10-26 | 0.9 | none |
| llmx-03 | langchain-experimental 0.4.2 | MIT; sunsetting | Officially documented | https://pypi.org/pypi/langchain-experimental/json | 10-26 | 0.8 | none |
| llmx-04 | Neo4j docs | Document/Chunk/Entity model, schema, limits | Officially documented | https://neo4j.com/labs/genai-ecosystem/llm-graph-builder/ | 10-26 | 0.85 | none |
| llmx-05 | LlamaIndex | extractor behaviours, stores | Officially documented | https://developers.llamaindex.ai/python/framework/module_guides/indexing/lpg_index_guide/ | 10-26 | 0.85 | none |
| llmx-06 | 2025 study | precision<recall, conflation | Independent paper | https://link.springer.com/article/10.1007/s41109-025-00749-0 (via search) | 10-26 | 0.4 | not re-read |
| llmx-07 | ISWC 2025 | LLMGraphTransformer vs KGGen vs GT2KG | Independent paper | https://ceur-ws.org/Vol-4085/paper49.pdf (via search) | 10-26 | 0.4 | not re-read; 3 abstracts |

## Appendix D. Assumptions
HAS_ENTITY name taken from convention, flagged unverified. Hypotheses on cost and strict-mode mechanism labelled as such.
