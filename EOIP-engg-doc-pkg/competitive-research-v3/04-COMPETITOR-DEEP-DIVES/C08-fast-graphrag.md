# C08 fast-graphrag (Circlemind)

| Field | Value |
|---|---|
| Registry ID | T-C08-fast-graphrag |
| Tier | B (PPR GraphRAG variant; no unique architecture beyond HippoRAG-style PPR, see C08-hipporag.md) |
| Versions examined | PyPI `fast-graphrag` 0.0.5 (2025-04-04); `main` HEAD commit 2025-11-01 |
| Verified on | 2026-10-26 (brief says 2026-10-18; actual access date used) |
| Worker | V20 |

## 1. Identity, current status, tier, sources
Open-source (MIT) Python GraphRAG library by Circlemind (circlemind-ai/fast-graphrag), with a separate managed Circlemind service [CLAIM-fgr-01, -04]. Status: **low-activity / maintenance-leaning**. Last commit on `main` is 2025-11-01, nearly a year before the check date; the latest PyPI release (0.0.5) is 2025-04-04; GitHub shows no releases; ~4.0k stars, 249 commits [CLAIM-fgr-02]. The last commit message is "remove cost-saving details" from the README [CLAIM-fgr-03]. Treat as a reference design, not a dependency. Sources: GitHub repo, PyPI, git history.

## 2. Problem, workloads, example workflows
Cheap GraphRAG over a document set: insert text with a `domain`, `example_queries` and `entity_types`; query returns an LLM answer plus context. Fits small-to-mid corpora and prototyping. Not designed for multi-tenant, ACL-aware or governed ingestion.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Entity/relation extraction with configured domain + entity types | present (README) |
| Personalized PageRank graph exploration (cites HippoRAG) | present [CLAIM-fgr-03] |
| Incremental insertion, checkpoint of `working_dir` | present (README) |
| Pluggable graph/vector backends, Neo4j etc. | UNKNOWN (README silent) |
| ACL, tenancy, provenance spans, deletion | absent / not documented |
| REST API / UI | absent in OSS; managed service only |
| MCP | not documented |

## 4. Architecture
```
docs -> chunk -> LLM extract (entities typed by config) -> graph + chunk/entity embeddings in working_dir
query -> LLM entity extraction -> embed/match seeds -> PPR over graph -> rank entities/chunks -> LLM answer
```

## 5. Under-the-hood reconstruction
Public evidence: PPR-based exploration derived from HippoRAG [CLAIM-fgr-03]. Hypotheses (from library structure, not re-verified this session, confidence 0.4): file-based local storage under `working_dir`, igraph-style in-memory graph, local vector index; node merging at insert time by name similarity / LLM; no transactions or concurrency model. Practical consequence: single-process, single-writer, whole graph in memory.

## 6. Requirements inferred
Typed entity schema supplied up front; incremental upsert; seed-then-PPR retrieval; cost-sensitive extraction (fewer LLM calls than community-summary pipelines).

## 7. Performance and resource model
Only vendor claim found: README (as fetched) stated a single example, Wizard of Oz text, $0.08 vs $0.48 for Microsoft GraphRAG ("6x") with no methodology; the latest commit removes the cost-saving details [CLAIM-fgr-03]. Treated as unverified vendor claim; no independent benchmark found. Memory grows with whole graph (hypothesis). Failure modes: extraction errors compound into PPR seeds; no retrieval-quality benchmark vs BM25/dense/hybrid (Master Prompt 5.3).

## 8. Strengths
PPR avoids global community summarisation cost (match with LightRAG/HippoRAG patterns in existing deep dives); config-driven entity types align with ontology-guided extraction. STR cards below.

## 9. Limitations
Algorithmic: single-pass extraction, no temporal or claim model. Operational: in-memory graph; stale maintenance. Friction: pre-1.0 version, sparse docs, no governance. Licensing: MIT (permissive); managed service is separate commercial. Outdated claims: cost comparison against an earlier GraphRAG.

## 10. Deployment and licensing
Self-hosted library, MIT, air-gap viable if local LLM/embeddings are configured (OpenAI-compatible endpoints; confidence 0.5). No legal trigger beyond normal MIT notice. One-node friendly; not multi-tenant.

## 11. Delta vs EOIP baseline
EOIP BL-16 is deterministic graph-first retrieval without LLM extraction or PPR; BL-14 weak vectors. In-process graph algorithms exist (BL-43; whether PPR specifically is implemented was not checked), so a PPR retriever is a thin composition. ACL gap BL-18 and tenancy BL-20 apply equally to this library: it provides nothing.

## 12. Cards
| ID | Card |
|---|---|
| STR-fast-graphrag-01 | Typed-entity-config + PPR seeds retrieval; evidence CLAIM-fgr-03; value: low-LLM-cost multi-hop; **match** via BL-43 PPR over tenant-scoped subgraph with ACL filter before scoring; test: multi-hop QA beats hybrid BM25+dense baseline on EOIP corpus or is dropped |
| INV-fast-graphrag-01 | Maintenance/maturity risk (proven by dates, maturity). Alternative: own PPR in EOIP, reuse algorithm only. Options: (1) wrap library [rejected: no ACL], (2) native PPR retriever on `GraphStore` neighbourhood, (3) differentiated: PPR with permission-pruned graph. Select 2. POC: compare vs hybrid RAG, success = statistically significant gain on multi-hop subset. Defensibility: ACL-aware retrieval. Decision **EXPERIMENT**. No seed hypothesis in 10.5 targets this entry. |

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-56 GraphRAG (PPR) | BUILD native PPR retriever (EXPERIMENT); do not depend on library |
| CAP-32 extraction | REFERENCE only; DEFER |
| CAP-55 hybrid | REUSE existing RRF (BL-15) as baseline |

## 14. Tests
Reproduce on EOIP sample corpus: PPR vs BM25/dense/hybrid, recall@k and answer faithfulness; run with a local 7-14B model; cost in LLM calls per 1k chunks.

## 15. Risks and open questions
Unknown storage internals; unknown real-world quality; whether Circlemind continues OSS.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | status, MIT |
| D2 | 2 | cheap GraphRAG |
| D3 | 4 | library |
| D4-D8 | 5 | UNVERIFIED internals |
| D9 | 3 | insert only |
| D10-D12 | N/A | not covered by project |
| D13 | 3,5 | PPR retrieval |
| D14 | N/A | no NL-to-query |
| D15-D17 | 3 | minimal |
| D18-D19 | 9,11 | no ACL/tenancy |
| D20 | 7 | vendor claim only |
| D21 | 10 | MIT + managed service |
| D22 | 3 | unknown |
| D23 | N/A | PPR/HippoRAG prior art |
| D24 | 7 | low-quality evidence |

## Appendix B. Capability mapping
| CAP | This tech | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-56 | native (PPR) | fgr-03 | BL-16 Implemented (deterministic) | EXPERIMENT | P2 |
| CAP-32 | native (LLM) | fgr-03 | Absent | DEFER | P3 |
| CAP-46 | absent | fgr-01 | BL-18 Absent | BUILD (EOIP) | P0 |

## Appendix C. Evidence records
| CLAIM | Product/version/date | Claim | Class | Source | Dates/conf | Contradiction |
|---|---|---|---|---|---|---|
| fgr-01 | repo main 2025-11-01 | MIT licence; Circlemind owner | Officially documented | github.com/circlemind-ai/fast-graphrag | acc 2026-10-26; 0.9 | none |
| fgr-02 | PyPI 0.0.5 | Latest release 2025-04-04; no GitHub releases | Officially documented | pypi.org/project/fast-graphrag | acc 2026-10-26; 0.9 | none |
| fgr-03 | README | Uses PPR citing HippoRAG; "6x" cost example $0.08 vs $0.48 (vendor claim); last commit removes cost details | Officially documented + git log | repo README, git log | acc 2026-10-26; 0.8 | claim withdrawn in HEAD |
| fgr-04 | README | Managed service, 100 free requests/month | Officially documented | repo README | acc 2026-10-26; 0.7 | pricing may change |

## Appendix D. Assumptions
Local-model operation assumed possible via OpenAI-compatible endpoint; storage internals not verified.
