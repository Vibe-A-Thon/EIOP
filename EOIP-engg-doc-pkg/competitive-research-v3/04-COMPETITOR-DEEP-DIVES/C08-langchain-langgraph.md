# C08 LangChain and LangGraph (RAG/graph usage; agent framework comparison is in C09)

| Field | Value |
|---|---|
| Registry ID | T-C08-langchain-langgraph |
| Tier | B (ubiquitous orchestration; cross-ref C09) |
| Versions examined | `langchain` 1.4.7 (2026-10-21); `langgraph` 1.2.17 (2026-10-24); `langchain-core` 1.7.0 (2026-10-22); `langchain-neo4j` 0.11.0 (2026-10-09); `langchain-community` 0.4.2 (2026-05-22) |
| Verified on | 2026-10-26 |
| Worker | V20 |

## 1. Identity, status, sources
LangChain Inc. maintains LangChain (LLM application framework; 1.x line), LangGraph (stateful graph-based orchestration, 1.x), integration packages, and commercial LangSmith / LangGraph platform products (proprietary SaaS/self-host, not examined). All OSS packages are MIT, very active (patch releases weekly) except `langchain-community`, whose last release was 2026-05-22, suggesting integrations moved to partner packages [CLAIM-lc-01]. Legacy "LangChain 0.x" chains were reorganised; python.langchain.com redirects to docs.langchain.com [CLAIM-lc-02]. Name check: LangGraph (orchestration) is unrelated to graph databases.

## 2. Problem and workloads
Compose LLM calls, retrievers and tools into chains; LangGraph models workflows as state machines (nodes, conditional edges, loops) with persistence and human-in-the-loop. For RAG/graph work: GraphRAG recipes, `Neo4jGraph`, `GraphCypherQAChain`, `LLMGraphTransformer` (LLM extraction to graph documents), vector stores, retrievers.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Retriever/vectorstore abstractions, many stores | present [CLAIM-lc-01] |
| LangGraph state graph, conditional edges, cycles | present (from knowledge, 0.7) |
| Checkpointing / persistence (SQLite/Postgres savers), interrupts for human review | present (knowledge, 0.6) |
| Neo4j integration: graph, vector, Cypher chain, `validate_cypher` | present, `allow_dangerous_requests` opt-in; **no EXPLAIN read-only check** [CLAIM-lc-03] |
| LLM graph extraction (`LLMGraphTransformer`) | present in experimental/community lineage (UNVERIFIED current location) |
| Other graph stores (HugeGraph, Neptune, Gremlin, SPARQL, Memgraph) | community integrations, status UNVERIFIED |
| Tracing / evaluation | LangSmith (proprietary service); OTel export UNVERIFIED |
| Source ACL, tenancy | absent in core |
| MCP adapters | present via separate adapter package (UNVERIFIED version) |

## 4. Architecture
```
LangGraph StateGraph: state (typed dict) -> node fns (retrieve | generate | grade | tool) -> conditional edges (loop on grade)
  checkpointer (SQLite|Postgres) per thread_id ; interrupt() for human approval
LangChain layer: Runnable interface (invoke|stream|batch) ; retrievers ; chat models ; tools
Integrations: langchain-neo4j (Neo4jGraph, Neo4jVector, GraphCypherQAChain)
Optional SaaS: LangSmith tracing (opt-in)
```

## 5. Under-the-hood reconstruction
`GraphCypherQAChain._call` (source observed): LLM generates Cypher from schema text + question, optional `CypherQueryCorrector` (schema-relationship based, off by default), `graph.query(cypher)[:top_k]` with `top_k=10`, then a QA LLM answers; `return_direct` returns raw rows; constructor raises unless `allow_dangerous_requests=True` [CLAIM-lc-03]. No read-only enforcement, no EXPLAIN, no tenant predicate. LangGraph persistence: per-thread checkpoint of state after each superstep enabling resume and time-travel (knowledge, 0.6; not re-verified). Pattern value for EOIP: *agentic RAG loop* (retrieve -> grade -> rewrite -> retrieve) with human interrupt.

## 6. Requirements inferred
Typed workflow state; resumable runs; human-in-the-loop gates; tool calls as nodes; observability hooks.

## 7. Performance
Framework overhead is small against LLM latency (hypothesis, unmeasured). Agentic loops multiply LLM calls per question; no vendor benchmark relevant. No claim made.

## 8. Strengths
Largest ecosystem; LangGraph's explicit state machine and checkpoint/interrupt model suits governed workflows; MIT licence; native-tool-call helper `use_function_response`. EOIP could match with its own agent runtime (BL-48) using review gates.

## 9. Limitations
Verified: Cypher chain lacks read-only guard (contrast neo4j-graphrag) [CLAIM-lc-03]. Friction: API churn across 0.x -> 1.x, deprecated chains, sprawling integration quality (community package stale since May 2026, hypothesis on cause). Operational: LangSmith is SaaS; air-gap needs tracing disabled/self-hosted (UNVERIFIED terms). Security: no ACL/tenant model; prompt-injection handling left to app.

## 10. Deployment and licensing
MIT for all packages examined; embeddable and redistributable. LangSmith/Platform proprietary (community-vs-commercial split; **legal/commercial review** if white-labelled). Air-gap viable if tracing is off and models are local (0.6). One-node friendly.

## 11. Delta vs EOIP baseline
EOIP has its own agent runtime and governed tools (BL-48 Partial), MCP server (BL-47), read-only-by-default and review gates by design, egress gateway (BL-45). LangGraph offers a mature checkpoint/interrupt engine EOIP might lack in resumability (UNVERIFIED in `agents/`). LangChain's graph chains would bypass BL-08 typed plans and BL-18/BL-20 controls.

## 12. Cards
| ID | Card |
|---|---|
| STR-langgraph-01 | Explicit state-graph workflow with checkpoint, resume and human interrupt; CLAIM-lc-01 (version), knowledge-based mechanism; value: governed multi-step retrieval with approvals; **match** (reference), optionally **integrate** LangGraph as an executor behind EOIP's tool gateway; design: every tool node passes via governed-tool wrapper (ACL, tenant, audit), state checkpoints stored per tenant; acceptance: resume after crash, interrupt blocks destructive tool, no tool call bypasses the gateway |
| STR-langchain-01 | Runnable/retriever abstractions and wide integration reach; **reject** as hard dependency, **reference** for adapter shape |
| INV-langchain-01 | Unsafe default graph-query chain (proven in source; root cause governance/semantics). Alternative: EOIP validator pipeline (see C08-text-to-query.md STR-t2q-01). Options: (1) wrap chain with EXPLAIN guard + scoped DB role, (2) never expose generated query execution, use QueryPlan (selected), (3) differentiated: policy-compiled plans. POC: mutation corpus against wrapped chain; success: zero mutations pass. Decision **REJECT** chain, **ADOPT** guard pattern. Not a seed hypothesis target. |

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-59 agent tool orchestration | EXPERIMENT LangGraph as optional executor; keep EOIP gateway authoritative (C09 decides) |
| CAP-58 NL-to-query | REJECT `GraphCypherQAChain`; see text-to-query |
| CAP-32 LLM graph extraction | DEFER; compare against own extractor |
| CAP-53/55 retrievers | REUSE nothing; own stack |
| CAP-75 tracing | INTEGRATE via OTel only; no mandatory SaaS |

## 14. Tests
Spike a LangGraph agentic-RAG loop over EOIP retrieval in an air-gapped container with tracing disabled: assert zero outbound traffic, tool-gateway enforcement, resume/interrupt, tenant-scoped checkpoints.

## 15. Risks and questions
Dependency footprint and churn; telemetry defaults; platform licence terms; whether checkpoints store sensitive content outside tenant boundaries.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | MIT, active, community pkg slower |
| D2 | 2 | orchestration |
| D3 | 4 | layered |
| D4-D5,D7,D11,D12,D22 | N/A | no storage model of its own |
| D6 | 5 | chain flow |
| D8 | 3 | checkpoint savers (knowledge) |
| D9 | N/A | not ingestion |
| D10 | 9 | no provenance model |
| D13 | 2,5 | retrieval and agent loops |
| D14 | 5,9 | Cypher chain |
| D15 | N/A | not governance |
| D16 | 3 | LangSmith/Studio (not examined) |
| D17 | 8 | SDKs |
| D18 | 9 | no read-only guard |
| D19 | 9 | none |
| D20 | 7 | N/A |
| D21 | 10 | MIT + commercial platform |
| D23 | N/A | none |
| D24 | 1 | PyPI + source |

## Appendix B. Capability mapping
| CAP | This tech | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-59 | native (agents/tools) | lc-01 | BL-47/48 | EXPERIMENT | P2 |
| CAP-58 | partial | lc-03 | BL-11/12 | REJECT chain | P1 |
| CAP-49 | absent in chain | lc-03 | BL-08 | BUILD | P0 |
| CAP-32 | partial | lc-01 | Absent | DEFER | P3 |

## Appendix C. Evidence records
| CLAIM | Product/version/date | Claim | Class | Source | Dates/conf | Contradiction |
|---|---|---|---|---|---|---|
| lc-01 | PyPI: langchain 1.4.7, langgraph 1.2.17, core 1.7.0, community 0.4.2, langchain-neo4j 0.11.0 | MIT; release dates 2026-10-21/-24/-22, 2026-05-22, 2026-10-09 | Officially documented | pypi.org/project/langchain, /langgraph, /langchain-core, /langchain-community, /langchain-neo4j | acc 2026-10-26; 0.9 | none |
| lc-02 | docs | python.langchain.com redirects (308) to docs.langchain.com | Reproduced | python.langchain.com/docs/security | 2026-10-26; 0.9 | none |
| lc-03 | langchain-neo4j `chains/graph_qa/cypher.py` | `allow_dangerous_requests` required; narrow-credentials advice; `validate_cypher` default False; `top_k` 10; no EXPLAIN/read-only check | Observed in source | raw.githubusercontent.com/langchain-ai/langchain-neo4j/main/libs/neo4j/langchain_neo4j/chains/graph_qa/cypher.py | acc 2026-10-26; 0.75 (summarised by fetch tool) | neo4j-graphrag does check (C08-neo4j-graphrag.md) |

## Appendix D. Assumptions
LangGraph persistence and interrupt behaviour recalled from general knowledge (0.6), not re-verified. LangSmith terms not examined. Orchestration comparison deferred to C09.
