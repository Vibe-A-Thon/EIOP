# C08 Text-to-query systems (Text2Cypher, text-to-Gremlin, text-to-SPARQL) and query suggestion

| Field | Value |
|---|---|
| Registry ID | T-C08-text-to-query |
| Tier | B (family of systems and benchmarks; central to journey J11, CAP-58) |
| Versions examined | Neo4j Text2Cypher dataset paper arXiv:2412.10064 (2024-12-13); `neo4j-labs/text2cypher` HEAD 2026-10-09; CypherBench arXiv:2412.18702 / ACL 2025, repo HEAD 2026-10-19; SPARQL-LLM arXiv:2512.14277 v2 (2026-09-23, TWEB 2026); `langchain-neo4j` 0.11.0 (2026-10-09); EICopilot arXiv:2501.13746 |
| Verified on | 2026-10-26 |
| Worker | V20 |

## 1. Identity, status, sources
Not one product: a family. (a) **Text2Cypher**: Neo4j Labs resources (experimental, "not part of Neo4j's supported product lineup"), 44,387-instance dataset, `Text2CypherRetriever` in neo4j-graphrag (see C08-neo4j-graphrag.md), `GraphCypherQAChain` in langchain-neo4j, CypherBench [CLAIM-t2q-01..03, -05]. (b) **text-to-Gremlin**: no dedicated public accuracy benchmark found; evidence is EICopilot (418 Gremlin pairs, fine-tuned Llama3-8B/ErnieBot), an AWS Bedrock blog (schema in prompt, execute-and-repair, LLM-judge scores), and an LDBC "Text2Graph" working-group charter v0.1.2 [CLAIM-t2q-06]. (c) **text-to-SPARQL**: TEXT2SPARQL challenge (DBpedia and Corporate KG tracks, 2025 and 2026), SPARQL-LLM (open source, github.com/sib-swiss/sparql-llm, deployed at expasy.org/chat) [CLAIM-t2q-07]. (d) **suggestion approaches**: ranked interpretations before execution; the EOIP engine is the in-scope reference. Licence note: repo CC0-1.0 vs dataset paper CC BY-SA 4.0 (inconsistent) [CLAIM-t2q-01].

## 2. Problem and workloads
Map a NL question to an executable graph query so non-technical users get answers; core to J11. Hard parts: schema size, opaque IDs, entity grounding, query dialect variance, safety.

## 3. Feature inventory
| Capability | Cypher | Gremlin | SPARQL |
|---|---|---|---|
| Public benchmark | CypherBench (>10k Qs, 11 graphs, 7.8M entities) [CLAIM-t2q-02]; Text2Cypher dataset 44,387 [CLAIM-t2q-01] | none found; LDBC effort starting, Gremlin secondary priority [CLAIM-t2q-06] | TEXT2SPARQL challenge: 2025 DBpedia 200 Qs, Corporate 50 Qs [CLAIM-t2q-07] |
| Schema grounding | schema text in prompt (apoc/db.schema), few-shot [CLAIM-t2q-03] | schema in prompt (AWS) | metadata index of classes/examples (SPARQL-LLM) [CLAIM-t2q-07] |
| Read-only guard | EXPLAIN query_type check (neo4j-graphrag); none in `GraphCypherQAChain` [CLAIM-t2q-03, -04] | none documented | none documented; SPARQL Update separable by parser |
| Execute-and-repair loop | yes (several libs) | yes (AWS) | yes (agents) |
| Fine-tuning | yes (dataset) | EICopilot | yes in challenge entries |

## 4. Architecture (generic pipeline and EOIP placement)
```
question -> mention detection -> schema/entity grounding (index of labels, props, examples)
  -> candidate generation (LLM or rules) x N -> static validation (parse, allow-list, EXPLAIN/algebra)
  -> rank (confidence, cost tier, permission) -> user picks -> execute with budgets -> answer + executed-query display
fallback: deterministic intents -> typed QueryPlan templates (EOIP BL-08/BL-11)
```

## 5. Under-the-hood reconstruction
**Accuracy evidence (vendor/author claims, workloads noted).** CypherBench reference result: gpt-4o-mini overall execution accuracy 0.3143, executable 87.39%, on the 7 test graphs [CLAIM-t2q-02]. Executable-but-wrong dominates; the paper's thesis is that raw RDF schemas are too large and opaque so it builds property-graph views. Text2Cypher paper: fine-tuned models improve Google-BLEU and exact-match over baselines (no numbers seen) [CLAIM-t2q-01]. SPARQL-LLM (authors): F1 0.7192 DBpedia-EN, 0.7810 DBpedia-ES, 0.8510 Corporate-EN, 0.8104 Corporate-DE in the 2026 challenge, up to 59% above second-best, at most $0.01/question; a secondary summary quotes different speedup figures (27x vs 36x), so treat as unreconciled [CLAIM-t2q-07]. Gremlin: no comparable number; AWS LLM-judge scores (70.36% Nova Pro vs 78.93% a stronger model) are judge-based, column labels unclear, not execution accuracy [CLAIM-t2q-06]. Cross-language comparison is invalid (different graphs, metrics, sizes).
**Safety pattern.** `Text2CypherRetriever` runs `EXPLAIN` and requires read-only query type (planner-based) [CLAIM-t2q-03]. `GraphCypherQAChain` has no read-only enforcement: it requires `allow_dangerous_requests=True` and advises narrowly scoped credentials; optional schema-based `validate_cypher` corrector; top_k=10 truncation [CLAIM-t2q-04]. EXPLAIN alone does not stop expensive reads or cross-tenant patterns; add allow-lists, tenant predicates, limits.
**Ranking.** Libraries return a single query. Multi-candidate ranking with plain-language paraphrase is rare; EOIP's engine (read: `suggest/engine.py` `suggest()` / `_confidence()`) scores up to 3 intents (0.35 + 0.45 x intent share + 0.15 x entity match, penalised for ambiguity), shows paraphrase, cost tier, latency estimate and a permission note per candidate, and only calls an optional `LLMAssistHook` when no intent or <2 candidates; hook output is labelled `llm_assist`, errors swallowed [CLAIM-t2q-08].

## 6. Requirements inferred
Per-tenant grounding index; N-best candidates; validation before display; read-only budgeted execution; executed-query display; deterministic fallback; per-dialect evaluation.

## 7. Performance and resource model
LLM latency per candidate dominates; local 7-14B models assumed weaker than gpt-4o-class (hypothesis, unmeasured). Main failure mode: executable but wrong queries [CLAIM-t2q-02].

## 8. Strengths
Planner-based read-only check; execute-and-repair; grounding indexes; open datasets (see cards).

## 9. Limitations
Algorithmic: benchmark accuracy on large schemas is modest even for strong models (0.31 EX reference). Friction: Gremlin lacks benchmarks; datasets have mixed licences; Labs project unsupported. Safety: LangChain chain lacks read-only enforcement; prompt injection through data values in schema/results (hypothesis).

## 10. Deployment and licensing
Mostly permissive/permissive-data: Apache-2.0 (CypherBench), MIT (langchain-neo4j), dataset licences CC0 / CC BY-SA 4.0 (**legal-review trigger for share-alike on bundled data**). All can run offline with local models. SPARQL-LLM software licence not verified.

## 11. Delta vs EOIP baseline
BL-08 typed QueryPlan + BL-11 deterministic engine are safer by construction (no generated query) and already give N-best with permission notes; BL-12 LLM path is only a hook. Absent: grounding index over ontology, per-language generation, EXPLAIN-style validators, evaluation suite (CAP-78), and ACL in candidate generation (BL-18 Absent; `_permission_note` checks API-action permissions, not source ACLs).

## 12. Cards
| ID | Card |
|---|---|
| STR-t2q-01 | Planner-based read-only validation of LLM queries (EXPLAIN); CLAIM-t2q-03; **integrate/match** for Cypher and extend to Gremlin/SPARQL; design: validator interface per dialect: parse -> AST allow-list (clauses, labels, props from ontology) -> engine EXPLAIN/algebra -> tenant predicate injection -> row/time/hop limits; acceptance: mutation-corpus (CREATE/DELETE/SET/CALL/SERVICE/UPDATE) 100% rejected; cross-tenant canary never returned |
| STR-t2q-02 | Metadata-indexed grounding and example retrieval (SPARQL-LLM); CLAIM-t2q-07; **match**; index ontology classes/properties/aliases and curated example queries per tenant; acceptance: grounding recall on EOIP question set |
| INV-t2q-01 | Executable-but-wrong queries and unsafe chains (proven by CLAIM-t2q-02, -04; root cause semantics/UX). Alternative: LLM proposes a *typed QueryPlan* (JSON against BL-08 schema), compiled by EOIP adapters; worse when the question needs an operator the plan language lacks. Options: (1) EXPLAIN guard around LLM Cypher, (2) LLM -> QueryPlan with N-best + paraphrase (selected), (3) differentiated: verified-example cache ranking candidates by past accepted queries. POC: 200 questions on EOIP ontology; success: top-3 contains correct plan >= deterministic baseline +15 points, 0 write attempts, p95 <= 5 s on local 14B; cost baseline: deterministic engine. Defensibility: ACL- and ontology-aware candidates. Decision **EXPERIMENT**. |
| INV-t2q-02 | No Gremlin/GQL evidence base (proven absence). Option: build EOIP's own benchmark across HugeGraph/Neo4j/Neptune dialects through the IR (BL-09). Decision **ADOPT** (build harness). Seed hypothesis "fixed vendor query languages via typed query plans plus adapters" (10.5 addendum): supported for read paths. |

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-58 NL-to-query | EXPERIMENT LLM->QueryPlan candidates behind hook; keep deterministic fallback as default |
| CAP-49 query safety | BUILD dialect validators; REUSE EXPLAIN pattern |
| CAP-14 Cypher gen | DEFER direct generation; INTEGRATE datasets for eval |
| CAP-13 Gremlin / CAP-15 SPARQL gen | DEFER; EXPERIMENT via IR (BL-09) |
| CAP-78 evaluation | BUILD per-dialect harness; REUSE CypherBench metrics (EX, PSJS, executable %) |

## 14. Tests
Question corpus per EOIP journey (J11); metrics: top-1/top-3 plan accuracy, execution accuracy, executable %, unsafe-attempt rejection, leakage canaries, latency on local models, fallback rate when LLM down (must return deterministic candidates).

## 15. Risks and questions
Share-alike data licence; model drift; Gremlin quality unverified; whether 3 candidates suffice (user study needed).

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1-D2 | 1,2 | family, mixed licences; J11 |
| D3 | 4 | generic pipeline |
| D4-D5,D7-D12 | N/A | not storage/ingest/ML systems |
| D6 | 5 | planner-based validation |
| D13-D14 | 3-5,7 | core: grounding, candidates, safety, fallback |
| D15-D17 | 3 | libraries only |
| D18-D19 | 5,9,11 | read-only, injection, tenant predicates |
| D20 | 7 | latency/cost |
| D21-D22 | 3,10 | licences; dialect portability |
| D23 | N/A | none verified |
| D24 | 5 | author benchmarks, incomparable |

## Appendix B. Capability mapping
| CAP | This tech | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-58 | native (Cypher/SPARQL), absent (Gremlin) | t2q-02,-06,-07 | BL-11 Impl, BL-12 Partial | EXPERIMENT | P1 |
| CAP-49 | partial | t2q-03,-04 | BL-08 Impl | BUILD | P0 |
| CAP-20 | absent | t2q-06 | BL-09 Partial | BUILD | P2 |
| CAP-78 | partial | t2q-02 | Unknown | BUILD | P1 |

## Appendix C. Evidence records
| CLAIM | Product/version/date | Claim | Class | Source | Dates/conf | Contradiction |
|---|---|---|---|---|---|---|
| t2q-01 | arXiv:2412.10064 | Text2Cypher dataset 44,387 instances; fine-tuned gains in Google-BLEU/EM; CC BY-SA 4.0 | Peer-reviewed preprint | arxiv.org/abs/2412.10064 | 2024-12-13; acc 2026-10-26; 0.8 | repo says CC0-1.0 |
| t2q-02 | CypherBench arXiv:2412.18702, ACL 2025 | 11 graphs, ~7.8M entities, >10k Qs; gpt-4o-mini EX 0.3143, PSJS 0.4591, executable 0.8739; Apache-2.0 | Independent benchmark | arxiv.org/abs/2412.18702; github.com/megagonlabs/cypherbench | acc 2026-10-26; 0.8 | single-model figure |
| t2q-03 | neo4j-graphrag (see C08-neo4j-graphrag.md CLAIM-07); neo4j-labs/text2cypher HEAD 2026-10-09 | EXPLAIN read-only guard; Labs "experimental, not supported"; CC0-1.0 | Observed in source / documented | github.com/neo4j-labs/text2cypher | acc 2026-10-26; 0.8 | none |
| t2q-04 | langchain-neo4j 0.11.0 (2026-10-09), `chains/graph_qa/cypher.py` | requires `allow_dangerous_requests`; narrow credentials advice; optional validate_cypher; top_k=10; no EXPLAIN/query_type | Observed in source | raw.githubusercontent.com/langchain-ai/langchain-neo4j | acc 2026-10-26; 0.75 (fetch-summarised) | none |
| t2q-06 | EICopilot 2501.13746; AWS blog; LDBC charter v0.1.2 | 418 Gremlin pairs; LLM-judge scores; Gremlin secondary after GQL, SQL/PGQ, Cypher | Third-party report | arxiv.org/abs/2501.13746; aws.amazon.com/blogs/machine-learning/generate-gremlin-queries-using-amazon-bedrock-models; ldbcouncil.org | acc 2026-10-26; 0.5 (search-snippet based; charter PDF unreadable) | none |
| t2q-07 | SPARQL-LLM 2512.14277 v2; TEXT2SPARQL 2025 | F1 .7192/.7810/.8510/.8104; up to 59% over runner-up; <= $0.01/Q; 2025 sets 200 + 50 Qs; open-source; speedup 27x (arXiv) vs 36x (review) | Author-reported | arxiv.org/abs/2512.14277; arxiv.org/pdf/2510.02200 | acc 2026-10-26; 0.65 | speedup discrepancy |
| t2q-08 | EOIP `suggest/engine.py` | scoring formula, LLM hook only if <2 candidates, `llm_assist` label | Observed in source | repo path | 2026-10-26; 0.95 | none |

## Appendix D. Assumptions
Local-model accuracy hypothesised from model-size trends, not measured. Gremlin conclusions rest on search snippets.
