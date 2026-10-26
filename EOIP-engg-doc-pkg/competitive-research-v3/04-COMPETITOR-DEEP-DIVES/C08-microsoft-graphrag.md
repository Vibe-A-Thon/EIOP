| Field | Value |
|---|---|
| Registry ID | T-C08-microsoft-graphrag |
| Tier | A (GraphRAG reference implementation; target of seed inversion hypothesis §10.5) |
| Versions examined | microsoft/graphrag v3.3.0 (tag, released 2026-10-08, commit 5faaaf4); release history v3.1.1 (2026-07-18), v3.1.2 (2026-08-21), v3.2.0 (2026-09-24). Papers: arXiv 2404.16130 (v2 2025-02-19). LazyGraphRAG: Microsoft Research blog 2024-11-25 (not in the examined source tree). |
| Verified on | 2026-10-18 (brief date; source read at tag; tag/licence via GitHub API unauthenticated) |
| Worker | V05 (registry worker W19) |

## 1. Identity, current status, tier, and sources

| Item | Verified value |
|---|---|
| Owner / licence | Microsoft; MIT, `LICENSE` in repo. [CLAIM-msgraphrag-01] |
| Status | Active, not archived; last push 2026-10-20; ~36.4k GitHub stars; 4 releases in ~3 months. [CLAIM-msgraphrag-01] |
| Packaging | v3 monorepo `packages/{graphrag, graphrag-cache, graphrag-chunking, graphrag-common, graphrag-input, graphrag-llm, graphrag-storage, graphrag-vectors}`; v3 removed fnllm, umap/graspologic embedding, multi-search, document grouping. [CLAIM-msgraphrag-02] |
| Members | GraphRAG (standard indexing; local, global, DRIFT, basic search); "fast" indexing (NLP graph); incremental `*-update` methods; prompt tuning; **LazyGraphRAG** (research technique, see below). |
| LazyGraphRAG trap | Blog (2024-11-25) describes it; the GraphRAG 1.0 post said it would be added to the library "in the near future". No LazyGraphRAG code exists in the v3.3.0 tree (case-insensitive grep: only unrelated hits); Microsoft states it is available through Microsoft Discovery / Azure Local preview. Treat as **announced / hosted, not shipped as OSS** at v3.3.0. [CLAIM-msgraphrag-15] |
| Project posture | Repo states it is "a platform for our research into RAG indexing methods"; internals may change without semver; only CLI, API layer, settings and data model carry compatibility promises. [CLAIM-msgraphrag-02] |

Sources: GitHub repo/tags, `docs/index/methods.md`, `breaking-changes.md`, paper 2404.16130, LazyGraphRAG blog, GraphRAG-Bench (2506.05690), Han et al. (2502.11371), Zeng et al. (2506.06331), HippoRAG 2 paper (2502.14802).

## 2. Primary problem, target workloads, example workflows

- Problem: "global sensemaking" questions ("what are the main themes across this corpus?") that top-k chunk retrieval cannot answer because no single chunk contains the answer. [CLAIM-msgraphrag-16]
- Workloads: narrative or report corpora around 1M tokens (paper scale), private-data discovery, query-focused summarisation. Not designed for fact lookup, per-user permissions, or frequently changing corpora.
- EOIP-style workflows: (a) "Summarise the main risk themes across all post-incident reviews for service X"; (b) "What are the recurring change-failure patterns in this repository's Jira history?" Both are global questions; the EOIP reference questions (impact of deleting a service account, who changed class X) are graph-traversal questions that GraphRAG does not target.

## 3. Feature inventory

| Feature | Status | Note |
|---|---|---|
| LLM entity/relationship extraction with gleaning | present | default 1 glean, types org/person/geo/event |
| Entity/relationship description summarisation | present | LLM merge of duplicate descriptions |
| Claims/covariate extraction | optional | `extract_claims.enabled=false` default |
| Hierarchical Leiden communities + LLM reports | present | `max_cluster_size=10`, largest connected component only by default |
| Global search (map-reduce), dynamic community selection | present | |
| Local search (entity-centred) | present | |
| DRIFT search | present | |
| Basic (vector chunk) search | present | the in-tool plain-RAG baseline |
| Fast indexing (NLP noun-phrase graph) | present | spaCy/NLTK/regex |
| Incremental update | partial | additive only (see 5.7) |
| Bring-your-own-graph | present | `docs/index/byog.md` |
| Prompt tuning | present | CLI |
| Vector stores | present | LanceDB default; Azure AI Search, Cosmos DB modules |
| Graph database backend | absent | graph lives in parquet tables, not a graph DB |
| ACL / tenant filtering | absent | none in source; see 5.8 [CLAIM-msgraphrag-12] |
| Entity resolution beyond exact-name merge | absent | |
| UI | partial | `unified-search-app` demo; no admin UI |
| Local-LLM first-class support | partial | works via LiteLLM/Ollama proxy, malformed-JSON warnings |
| LazyGraphRAG | absent (OSS) | see section 1 |
| MCP | absent | none in tree |

## 4. Architecture diagram

```
 input files (txt/csv/json) -> load_input_documents
   -> create_base_text_units (1200 tok chunks, 100 overlap)
   -> extract_graph [LLM per chunk + gleaning]  --or-->  extract_graph_nlp [noun phrases + co-occurrence]
   -> (summarize descriptions) -> finalize_graph (+prune in fast mode)
   -> extract_covariates (optional) -> create_communities [hierarchical Leiden, LCC]
   -> create_community_reports [LLM per community, bottom-up context]
   -> generate_text_embeddings [text_unit_text, entity_description, community_full_content] -> LanceDB
 state:  parquet tables (documents, text_units, entities, relationships, communities, community_reports, covariates)
         + JSON LLM cache + vector store            (no graph DB, no transactions)
 query:  CLI/API -> {local | global | drift | basic}
   global: reports(level) -> shuffle+batch -> N parallel map LLM calls (points+score 0-100) -> reduce LLM
   local : embed query -> top-k entities -> relationships/text units/reports within token budget -> 1 LLM call
   drift : primer over report folds -> follow-up questions -> local-search actions (depth n) -> reduce
 update: delta by document title -> run pipeline on delta -> merge tables -> re-report changed communities
```

## 5. Under-the-hood reconstruction (v3.3.0, `packages/graphrag/graphrag/...`)

**5.1 Data model.** `data_model/{document,text_unit,entity,relationship,community,community_report,covariate}.py`. Entities carry `description`, `text_unit_ids`, degree; relationships carry weight (co-mention count) and `text_unit_ids`; communities carry `level`, `parent`, `children`, entity ids; reports carry title, summary, rating, findings, `full_content`. Provenance granularity is the chunk (text unit), not a character span. [CLAIM-msgraphrag-03]

**5.2 Extraction (standard).** `index/operations/extract_graph/graph_extractor.py`: one prompt per chunk (`prompts/index/extract_graph.py`), model replies with delimiter-separated records (`<|>` tuple, `##` record, `<|COMPLETE|>`); a gleaning loop (`CONTINUE_PROMPT`, then `LOOP_PROMPT` expecting "Y") runs up to `max_gleanings=1`; results parsed by string splitting, errors yield empty frames (silent loss on malformed output). Entities merge across chunks by normalised name+type string (no embedding/alias resolution); descriptions are then LLM-summarised (`summarize_descriptions`). Docs estimate graph extraction at "roughly 75%" of indexing cost. [CLAIM-msgraphrag-04, -07]

**5.3 Fast mode.** `extract_graph_nlp` + `prune_graph`: entities are noun phrases (regex/NLTK default, spaCy options), relationships are chunk co-occurrence, no descriptions; pruning defaults `min_node_freq=2`, `min_edge_weight_pct=40`; reports built from raw text units (`create_community_reports_text`); docs recommend 50-100-token chunks and warn of noisier graphs, English-centric. [CLAIM-msgraphrag-04]

**5.4 Communities.** `index/operations/cluster_graph.py` normalises edges to undirected, optionally keeps the largest connected component (`use_lcc=True` default), then `graspologic_native.hierarchical_leiden(max_cluster_size=10, resolution=1.0, use_modularity=True, seed=0xDEADBEEF)` (`graphs/hierarchical_leiden.py`). Every hierarchy level becomes a community row. Consequences (inferred from code): entities outside the largest component are dropped from community reports by default; the fixed seed makes clustering deterministic given identical input order. [CLAIM-msgraphrag-05, -06]

**5.5 Community reports.** `summarize_communities/*`: for each community (leaf level first) the context builder packs entities, relationships and claims sorted by degree up to `max_input_length=8000` tokens; if too large, sub-community reports substitute for raw members; LLM emits a structured report (title, summary, rating, findings) capped at `max_length=2000`. Cost scales with number of communities across all levels. [CLAIM-msgraphrag-05]

**5.6 Query.**
- *Global* (`query/structured_search/global_search/search.py`): reports at a chosen level are shuffled (`random_state=86`) and batched to `data_max_tokens=12000`; `asyncio.gather` runs one map call per batch returning JSON points with `score` 0-100; reduce call ranks points and writes the answer (`map_max_length=1000`, `reduce_max_length=2000`). Optional dynamic community selection (`context_builder/dynamic_community_selection.py`) rates reports top-down with an LLM `rate_relevancy` call, descending only into children of relevant communities. [CLAIM-msgraphrag-08]
- *Local* (`local_search/mixed_context.py`): embed query, top-10 entities by description embedding, then budget split `text_unit_prop=0.5`, `community_prop=0.15`, remainder to entities/relationships, `max_context_tokens=12000`; single LLM call. [CLAIM-msgraphrag-09]
- *DRIFT* (`drift_search/{primer,search,state,action}.py`): HyDE-style query expansion; primer runs over `primer_folds=5` folds of top community reports to produce an intermediate answer plus follow-up questions; a priority queue of incomplete actions (`rank_incomplete_actions`) is executed through local search for `n_depth=3` epochs, `drift_k_followups=20` per epoch, `concurrency=32`; final reduce merges the action tree. LLM calls per query are therefore on the order of tens (hypothesis: up to ~1 primer + 5 + 3x20 + 1; not measured). [CLAIM-msgraphrag-10]
- *Basic*: vector top-`k=10` chunks, `max_context_tokens=12000`; this is the in-tool plain-RAG control.

**5.7 Incremental update.** `index/update/incremental_index.py::get_delta_docs` diffs input titles against the stored `documents` table; the update pipeline (`update_final_documents … update_clean_state`) indexes the delta in a side directory (`update_output`), then merges entities, relationships, text units, communities (`_update_and_merge_communities`, producing a community-id mapping) and regenerates reports for changed communities. `deleted_inputs` is computed but a repository grep finds no consumer: **deletions are not propagated** (source-observed; behaviour not run). Document identity is the title string. [CLAIM-msgraphrag-11]

**5.8 Security / tenancy / ACL.** Grep for acl/permission/tenant/principal/access-control across `packages/graphrag/graphrag` returns nothing. A community report mixes content from many documents, so one unauthorised source can leak through a summary; per-user filtering after generation is not possible without re-generating. Isolation today means "one index directory per corpus". [CLAIM-msgraphrag-12]

**5.9 Citations.** Prompts instruct the LLM to emit `[Data: Reports (1); Entities (5, 7); Relationships (23)]` record ids (`prompts/query/*`). These are model-written, not validated against returned context in the code read; granularity is table row, not source span. [CLAIM-msgraphrag-13]

**5.10 Caching / concurrency / consistency.** JSON file cache keyed by prompt+model params (`graphrag-cache`) makes re-index of unchanged chunks cheap; LLM concurrency via config tpm/rpm; no transactions; a failed run leaves parquet outputs per workflow. Single-process pandas: memory-bound at corpus scale (hypothesis).

## 6. Functional and non-functional requirements inferred

FR: hierarchical thematic summaries with row-level pointers; map-reduce global answers; LLM-vs-NLP indexing trade-off. NFR: needs a model that reliably emits delimiter/JSON formats [CLAIM-msgraphrag-14]; index time and tokens scale with corpus and community count [CLAIM-msgraphrag-21]; no built-in security model.

## 7. Performance and resource model

| Evidence | Workload / setup | Result | Class |
|---|---|---|---|
| Han et al. 2502.11371 | MultiHop-RAG corpus, Llama-3.1-8B (build), their unified harness | Build time: RAG 135 s vs Community-GraphRAG 5,560 s (~41x); retrieval-phase 1,249 s vs 1,724 s; storage 165 MB vs 127 MB. [CLAIM-msgraphrag-18] | independent academic |
| HippoRAG 2 paper | MuSiQue ~11.7k passages | GraphRAG ~115.5M input tokens to index vs HippoRAG 2 ~9.2M; QA F1 49.6 vs dense NV-Embed-v2 57.0 (7-dataset average). [CLAIM-msgraphrag-20] | competitor-authored, direction consistent with others |
| GraphRAG-Bench 2506.05690 | Novel and medical corpora, GPT-4o-mini | Tokens per query: vanilla RAG 879; MS-GraphRAG local 38,707; global 331,375 (~380x). [CLAIM-msgraphrag-17] | independent academic |
| LazyGraphRAG blog | 5,590 AP news articles, 100 synthetic queries (50 local, 50 global), LLM judge | Vendor claim: index cost equals vector RAG (~0.1% of full GraphRAG); global quality comparable to GraphRAG global at >700x lower query cost. Win rates only in a figure. [CLAIM-msgraphrag-15] | vendor claim |

Failure modes: malformed LLM output silently drops chunks; LCC filtering silently drops disconnected entities; unstable quality across corpora (MS-GraphRAG medical summarisation accuracy 41.87 vs vanilla 65.75, novel 64.40 vs 51.30 [CLAIM-msgraphrag-17]). No p95 latency data found. Hardware figures for v3.3.0 indexing: NOT PUBLICLY VERIFIED.

## 8. Strengths

| Strength | Evidence | How matched or exceeded in EOIP |
|---|---|---|
| Global/thematic questions: only first-class map-reduce answer path | paper claims comprehensiveness/diversity gains; GraphRAG-Bench summarisation 64.40 vs 51.30 (novel) | Hierarchical community summaries computed on EOIP's own graph (BL-43 community code) on demand, permission-scoped |
| Hierarchical Leiden with hierarchy persisted | source 5.4 | Reuse algorithm via `graspologic-native` (MIT) or backend GDS |
| Cheap/rich indexing switch and prompt tuning | docs methods.md | Mirror: deterministic extraction first, LLM optional |
| Reproducible, well-documented data model | `docs/index/outputs.md` | Adopt table shapes as export format only |
| Active maintenance, MIT | CLAIM-01 | n/a |
| Dynamic community selection reduces map calls | source 5.6 | Cheap relevance rating with local reranker instead of LLM |

## 9. Limitations and root causes

| Class | Limitation | Basis | Root cause |
|---|---|---|---|
| Algorithmic dead-end | Not better than plain RAG on single-hop facts; Community-Global weak on detail QA (NQ F1 54.48 vs 64.78) | verified, independent [CLAIM-msgraphrag-18] | Summaries lose detail; global map-reduce answers a different question |
| Algorithmic | Graph quality bounded by extraction LLM (MultiHop-RAG accuracy 71.17 -> 75.08 gpt-4o-mini -> gpt-4o) | verified [CLAIM-msgraphrag-18] | Name-string entity merge, no resolution |
| Algorithmic | Evaluation inflated by LLM-judge bias (same system won ~90% vs ~10% in two instances; order effects) | independent [CLAIM-msgraphrag-19] | Win-rate on comprehensiveness favours long answers |
| Operational | Indexing token/time cost 40x+ over RAG; per-query tokens 40-380x | verified [CLAIM-msgraphrag-17, -18] | LLM calls per chunk, per description, per community |
| Operational | Re-summarisation on update; deletions not propagated | source [CLAIM-msgraphrag-11] | Corpus-level artefacts (communities) are not incrementally maintainable |
| Operational | Parquet/pandas, file cache, no DB | source | Research-platform design |
| Friction | No ACL, no tenants, no span-level citation | source [CLAIM-msgraphrag-12, -13] | Out of scope for the project |
| Friction | Local models: malformed JSON issues | docs [CLAIM-msgraphrag-14] | Format-brittle prompts |
| Friction | Breaking changes between majors (v2, v3) with migration notebooks | docs [CLAIM-msgraphrag-02] | Research cadence |
| Licensing | None (MIT); dependency licences not audited here (graspologic-native, LiteLLM, spaCy models) | UNVERIFIED | |

## 10. Deployment, licensing, redistribution, viability

MIT, pure Python, pip-installable (Python version range UNVERIFIED), runs offline if LLM and embeddings are local (LiteLLM → Ollama/vLLM). Air-gap viability: **partial** (works; quality depends on local model JSON discipline; spaCy model auto-download on first use must be pre-seeded). No cloud dependency by default (LanceDB local). Redistribution: MIT permits embedding; legal review of transitive dependencies still required (no conclusion). Single-node feasible but indexing is hours-to-days at corpus scale with local GPUs (hypothesis). Operating it for multi-tenant white-label requires one index per tenant and per permission scope.

## 11. Competitive delta against EOIP baseline

| EOIP | Delta |
|---|---|
| BL-16 deterministic graph-first retrieval (no LLM at index time; no benchmark vs plain RAG) | GraphRAG adds LLM-built thematic layer EOIP lacks; EOIP has deterministic traceable retrieval GraphRAG lacks. No evidence EOIP's retrieval beats BM25+dense; GraphRAG's own `basic` mode shows the control EOIP lacks. |
| BL-13/14/15 BM25, hashing-embedder dense, RRF | Hashing embedder is far weaker than the embeddings used in every benchmark above; any EOIP-vs-GraphRAG comparison must first upgrade the dense leg |
| BL-43 community detection (in-process Python) | Partial parity on clustering; absent: LLM reports, map-reduce answer path |
| BL-18 source-ACL enforcement absent in retrieval | Same gap as GraphRAG; neither is ahead. EOIP captured ACL metadata (BL-17), GraphRAG does not |
| BL-45 egress gateway | EOIP ahead: GraphRAG sends raw chunks to whichever endpoint is configured |
| BL-38/37 snapshots, bitemporal | EOIP ahead on versioning; GraphRAG stores update directories only |
| BL-39 claims/contradictions, BL-40 epistemic separation | EOIP ahead; GraphRAG `claims` are optional extractions with no truth maintenance |

## 12. Strength-adoption and inversion cards

| ID | Competitor | Strength | Evidence | Value | Decision | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-msgraphrag-01 | GraphRAG | Hierarchical community reports enable global questions | [CLAIM-msgraphrag-08, -16, -17] | Executive/trend questions across tickets, incidents | match, on demand | Reports computed from EOIP graph per permission scope; cache invalidated by graph version | On a held-out set of 50 global questions, answer win-rate vs hybrid-reranked RAG >= 60% under length-controlled, order-swapped judging |
| STR-msgraphrag-02 | GraphRAG | In-tool plain-RAG control (`basic`) | source | Honest benchmarking | match | `eoip-bench` harness: graph-first vs BM25/dense/RRF/rerank | Runs offline in CI |
| STR-msgraphrag-03 | GraphRAG | Fast (NLP) vs standard indexing switch | [CLAIM-msgraphrag-04] | Cost control | exceed | Deterministic extraction (BL-26) first | Index cost per 1k docs reported |

**INV-msgraphrag-01 (validates, with correction, seed hypothesis §10.5).**
- Target/workload: GraphRAG v3.3.0 standard indexing; MuSiQue 11.7k passages and MultiHop-RAG.
- Limitation: indexing 40x+ time and ~12x tokens of the cheapest graph method. [CLAIM-msgraphrag-18, -20]
- Root cause: *proven* that extraction dominates (docs: ~75%) and that community-report generation is a further per-community cost; *hypothesis* that "community summarisation at ingest" is the main cost driver is **partly refuted**: per the project's own estimate it is entity/relationship extraction. Verdict: **VALIDATED for "costly indexing", REFUTED as to "offline community summarisation" being the primary cost; CONDITIONAL for the candidate design** (LightRAG/HippoRAG patterns reduce tokens but do not equal GraphRAG's global-answer capability; see C08-lightrag, C08-hipporag).
- Alternative mitigates: deterministic/NLP extraction + lazily generated reports only for communities touched by queries (a LazyGraphRAG-like deferral, vendor claims only). Worse when: global questions dominate and latency budgets are tight (on-demand reports add query-time LLM calls).
- Options: (1) quick: GraphRAG `--method fast` through BYOG on an exported EOIP graph; (2) pragmatic: native `CommunitySummaryService` over BL-43 with report cache keyed by (community hash, graph version, ACL scope); (3) long-term: incremental Leiden with report invalidation by member-set delta.
- Selected: option 2. Sketch: `report = cache.get(hash(sorted(member_ids)), acl_scope, model_id) or llm_summarise(top_k_edges_by_degree(community, 8000 tokens))`.
- Benchmark/POC: dataset = 2k EOIP-shaped incident/ticket docs plus GraphRAG-Bench novel corpus; metric = global-question win rate (length-controlled, both orderings) and tokens/index; baseline = GraphRAG fast and BM25+dense+rerank; success = within 5 points of GraphRAG standard at <= 20% of its index tokens.
- Dependencies/failure cases: reports must be built per ACL scope or leak (INV-02); cache poisoning by prompt-injected documents.
- Defensibility: permission-scoped, versioned, evidence-linked reports are tied to EOIP's graph/ACL moat, not to an algorithm.
- Decision: **EXPERIMENT**.

**INV-msgraphrag-02.** Limitation: no ACL; summaries aggregate across sources. Root cause: *proven* (no ACL code; reports mix documents), design. Alternative: compute communities and reports per ACL-equivalence class (set of principals), merge only at answer time among classes the caller may see. Worse when: ACL cardinality is high (reports fragment; hypothesis). Options: (1) one index per role group; (2) ACL-class partitioning with cached reports; (3) report generation with per-claim provenance and answer-time redaction. Select 2. POC: synthetic corpus with 20 principals, seeded canary facts; success = 0 canary leaks in 10k queries and report count growth < 3x. Decision: **ADOPT** as a requirement for any summary layer (P0, consistent with BL-18).

**INV-msgraphrag-03.** Limitation: deletions not propagated, update only appends. Root cause: *proven* from source; communities are global artefacts. Select: native tombstone-driven invalidation via EOIP source events (BL-24/25): mark reports whose member set intersects deleted entities stale. POC: delete 5% of documents, measure stale-fact rate in answers = 0 after refresh. Decision: **ADOPT**.

## 13. Per-capability decisions

| Capability | Decision | Note |
|---|---|---|
| CAP-56 global/community GraphRAG | EXPERIMENT | native service over BL-43 first; BYOG integration as fallback |
| CAP-56 local/DRIFT search | DEFER | no evidence DRIFT beats hybrid; BL-16 covers entity-centred retrieval |
| CAP-62 hierarchical Leiden | REUSE | `graspologic-native` or backend algorithms; licence check |
| CAP-32 LLM extraction pipeline | REJECT as core | name-string merge; use BL-26 + CAP-31 resolver |
| CAP-67 incremental update | BUILD | tombstone aware, not title-diff |
| CAP-46 ACL in summaries | BUILD | INV-02 |
| CAP-60 citations | BUILD | verify cited ids against returned context; span-level |
| CAP-78 benchmark harness | BUILD | STR-02 |
| LazyGraphRAG | DEFER | no OSS implementation; vendor-only evidence |

## 14. Tests, POC, acceptance

1. Install v3.3.0 offline, index 200 EOIP-shaped docs with a local 8B model and with fast mode; record tokens, wall time, malformed-record rate (target < 2% chunks dropped).
2. Run the benchmark triple on GraphRAG-Bench novel subset: BM25+dense+RRF+reranker vs GraphRAG local/global vs EOIP BL-16; metrics: ACC, evidence recall, tokens/query; two judge orderings.
3. ACL canary test (INV-02) against any report layer built.
4. Deletion test (INV-03).
5. Acceptance to adopt a summary layer: beats best non-graph baseline on global questions by >= 10 points absolute, loses < 3 points on fact questions via router, zero canary leaks.

## 15. Risks and open questions

LLM-judge bias can reverse conclusions [CLAIM-msgraphrag-19]; vendor LazyGraphRAG numbers unverified and not reproducible without code; v3 breaking changes show API churn; local-model quality unknown for EOIP content; whether LCC filtering drops important disconnected systems (e.g., isolated services); DRIFT's cost/benefit never independently measured (not found). Open: can ACL-class partitioning keep community quality?

## Appendix A. Research-dimension coverage

| Dimension | Sections | Summary |
|---|---|---|
| D1 Identity | 1 | MIT, active, v3.3.0 |
| D2 Problem | 2 | Global sensemaking |
| D3 Architecture | 4, 5 | Pipeline of workflows, parquet |
| D4 Storage | 5.1, 5.10 | Parquet + LanceDB; no graph DB |
| D5 Schema | 5.1 | Fixed table schema, 4 entity types default |
| D6 Query pipeline | 5.6 | local/global/drift/basic |
| D7 Reasoning | N/A | No inference engine; LLM synthesis only |
| D8 Transactions/scale | 5.10, 7 | None; single-process |
| D9 Ingestion | 5.2, 5.7 | Files, title-diff update |
| D10 Identity/evidence | 5.2, 5.9 | String merge; row-level cites |
| D11 Time | 5.7 | Update dirs only; no valid time |
| D12 Graph ML | 5.4 | Leiden only |
| D13 Retrieval/agents | 5.6, 5.9 | No MCP; cites unvalidated |
| D14 NL query | N/A | Not a text-to-query system |
| D15 Governance | N/A | None |
| D16 UX | 3 | Demo app only |
| D17 DevEx | 1, 9 | CLI/API, breaking changes |
| D18 Security | 5.8 | Absent; prompt-injection not addressed (UNVERIFIED) |
| D19 Multi-tenancy | 5.8, 10 | Index per corpus |
| D20 Economics | 7 | Cost evidence table |
| D21 Commercial | 10 | MIT |
| D22 Interop | 3 | BYOG, parquet |
| D23 IP | N/A | No patent info verified; flag for legal (Microsoft research output) |
| D24 Research quality | 7, 15 | Independent + vendor mixed |

## Appendix B. Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-56 | native | 03,08,09,10 | BL-16 Implemented (deterministic); BL-43 partial | EXPERIMENT | P1 |
| CAP-62 | native (Leiden) | 06 | BL-43 Implemented | REUSE | P2 |
| CAP-32 | native (LLM) | 07 | BL-26 Implemented (JSON only) | REJECT as core | P3 |
| CAP-67 | partial | 11 | BL-42/24 partial | BUILD | P1 |
| CAP-46 | absent | 12 | BL-18 Absent | BUILD | P0 |
| CAP-47 | absent | 12 | BL-20 Partial | BUILD | P0 |
| CAP-60 | partial | 13 | BL-41 Implemented | BUILD | P1 |
| CAP-61 | partial | 14 | BL-45 Implemented | INTEGRATE | P2 |
| CAP-78 | partial (basic mode) | 17,18 | none | BUILD | P1 |
| CAP-55 | absent | 18 | BL-15 Implemented | n/a (baseline to beat) | P1 |
| CAP-50 | partial | 14 | BL-45 | EXPERIMENT | P2 |

## Appendix C. Evidence records

All accessed 2026-10-18 (brief date) unless noted.

| CLAIM-ID | product/version/date | claim | class | source | pub / access | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-msgraphrag-01 | graphrag v3.3.0, 2026-10-08 | MIT, not archived, 36.4k stars, releases v3.1.1..v3.3.0 | Officially documented (GitHub API) | github.com/microsoft/graphrag (API repos, releases) | 2026-10-18 | 0.95 | none |
| CLAIM-msgraphrag-02 | v3.3.0 | v3 monorepo; removed fnllm/UMAP/multi-search/grouping; internals not semver-bound | Observed in source | `breaking-changes.md`, `packages/` | 2026-10-18 | 0.9 | none |
| CLAIM-msgraphrag-03 | v3.3.0 | table data model incl. text_unit_ids | Observed in source | `graphrag/data_model/*.py` | 2026-10-18 | 0.9 | none |
| CLAIM-msgraphrag-04 | v3.3.0 | standard vs fast methods; extraction ~75% of cost (project estimate); fast = NLP co-occurrence | Officially documented | `docs/index/methods.md`; `index/workflows/factory.py` | 2026-10-18 | 0.9 | none |
| CLAIM-msgraphrag-05 | v3.3.0 | defaults: chunk 1200/100, gleanings 1, max_cluster_size 10, use_lcc true, report 2000/8000 | Observed in source | `config/defaults.py` | 2026-10-18 | 0.95 | none |
| CLAIM-msgraphrag-06 | v3.3.0 | hierarchical Leiden via graspologic_native, seed 0xDEADBEEF | Observed in source | `graphs/hierarchical_leiden.py`, `index/operations/cluster_graph.py` | 2026-10-18 | 0.95 | none |
| CLAIM-msgraphrag-07 | v3.3.0 | delimiter-based extraction with gleaning loop; exceptions return empty frames | Observed in source | `index/operations/extract_graph/graph_extractor.py` | 2026-10-18 | 0.9 | none |
| CLAIM-msgraphrag-08 | v3.3.0 | global search: shuffled report batches, parallel map with 0-100 scores, reduce; dynamic community selection | Observed in source | `query/structured_search/global_search/search.py`, `context_builder/dynamic_community_selection.py` | 2026-10-18 | 0.9 | none |
| CLAIM-msgraphrag-09 | v3.3.0 | local search proportions 0.5/0.15, top-k 10, 12k tokens | Observed in source | `config/defaults.py` LocalSearchDefaults | 2026-10-18 | 0.95 | none |
| CLAIM-msgraphrag-10 | v3.3.0 | DRIFT: primer_folds 5, n_depth 3, k_followups 20, concurrency 32; priority queue of actions via local search | Observed in source | `drift_search/search.py`, `defaults.py` | 2026-10-18 | 0.9 | LLM call count is inference |
| CLAIM-msgraphrag-11 | v3.3.0 | incremental update diffs titles; deleted_inputs has no consumer (grep) | Observed in source | `index/update/incremental_index.py`, `workflows/load_update_documents.py` | 2026-10-18 | 0.8 (absence by grep) | behaviour not executed |
| CLAIM-msgraphrag-12 | v3.3.0 | no ACL/tenant/permission code in package | Observed in source (grep) | `packages/graphrag/graphrag` | 2026-10-18 | 0.85 | other packages (storage/cache) not exhaustively read |
| CLAIM-msgraphrag-13 | v3.3.0 | citations are LLM-emitted `[Data: ...]` ids | Observed in source | `prompts/query/local_search_system_prompt.py`, `global_search_map_system_prompt.py` | 2026-10-18 | 0.85 | validation elsewhere not found |
| CLAIM-msgraphrag-14 | v3.3.0 | proxied models (ollama/LiteLLM) often give malformed responses esp. JSON | Officially documented | `docs/config/models.md` | 2026-10-18 | 0.9 | none |
| CLAIM-msgraphrag-15 | LazyGraphRAG, 2024-11-25 | vendor claims: index cost ≈ vector RAG (~0.1% of GraphRAG); >700x cheaper global queries; AP news 5,590 docs, 100 queries; integrated in Microsoft Discovery; not OSS-confirmed; no code in v3.3.0 | Vendor claim | Microsoft Research blog "LazyGraphRAG: Setting a new standard for quality and cost" https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ ; GraphRAG 1.0 blog | 2024-11-25 / 2026-10-18 | 0.8 (existence), 0.3 (numbers) | independent reproduction not found |
| CLAIM-msgraphrag-16 | GraphRAG paper v2 | designed for global sensemaking; claims comprehensiveness/diversity gains vs conventional RAG at ~1M tokens | Peer-reviewed/preprint | arXiv 2404.16130 https://arxiv.org/abs/2404.16130 | 2024-04-24 (v2 2025-02-19) | 0.85 | CLAIM-18, -19 show gains narrower |
| CLAIM-msgraphrag-17 | GraphRAG-Bench (Xiang et al.) | GPT-4o-mini: MS-GraphRAG summarisation ACC 64.40 vs 51.30 vanilla+rerank (novel) but 41.87 vs 65.75 (medical); vanilla fact retrieval 60.92 vs best graph 60.14; tokens/query 879 vs 38,707 (local) vs 331,375 (global) | Independent benchmark | arXiv 2506.05690 https://arxiv.org/abs/2506.05690 (HTML read) | 2025-06-06 (v3 2026-02-22) | 0.8 | retriever and some appendix not read |
| CLAIM-msgraphrag-18 | Han et al. | Llama-3.1-8B: NQ F1 RAG 64.78 vs Comm-Global 54.48; HotpotQA RAG 60.04 vs Comm-Local 61.66 vs HippoRAG2 63.01; build 135 s vs 5,560 s; hybrid integration +6.4% | Independent benchmark | arXiv 2502.11371 https://arxiv.org/abs/2502.11371 (HTML v3) | 2025-02-17 (v3 2026-03-04) | 0.8 | paper notes BERTScore vs ROUGE tension |
| CLAIM-msgraphrag-19 | Zeng et al. | LLM-judge win-rate bias; gains of GraphRAG methods "much more moderate" after unbiased eval | Independent benchmark | arXiv 2506.06331 https://arxiv.org/abs/2506.06331 | 2025-05-31 (v2 2026-08-13) | 0.7 (abstract and search snippet only) | methods named not verified |
| CLAIM-msgraphrag-20 | HippoRAG 2 paper | MuSiQue 11.7k passages: GraphRAG ~115.5M indexing input tokens vs HippoRAG 2 ~9.2M; avg F1 49.6 vs 57.0 dense | Third-party report (competitor authors) | arXiv 2502.14802 https://arxiv.org/abs/2502.14802 | 2025-02-20 | 0.6 | authors favour own method; LightRAG F1 6.6 there looks anomalous |
| CLAIM-msgraphrag-21 | v3.3.0 | README/get-started warn indexing is expensive and consumes many LLM resources | Officially documented | `README.md`, `docs/get_started.md` | 2026-10-18 | 0.95 | none |

## Appendix D. Assumptions

- Source access date recorded as 2026-10-18 per brief; actual fetch occurred during the 2026-10-26 run.
- Hardware/latency for v3.3.0 not measured; cost numbers come from third-party papers using older versions (pre-v3), flagged per claim.
- Python version range, dependency licences, and security advisories not checked (UNVERIFIED).
- "Largest connected component drop" is inferred from code reading, not executed.
