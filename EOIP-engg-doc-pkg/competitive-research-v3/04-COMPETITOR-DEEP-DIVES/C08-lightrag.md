| Field | Value |
|---|---|
| Registry ID | T-C08-lightrag |
| Tier | A (dual-level graph retrieval; incremental-update pattern named in seed hypothesis §10.5) |
| Versions examined | HKUDS/LightRAG v1.5.7 (tag, released 2026-09-02, commit 28ff1b0; `__api_version__` 0344); predecessors v1.5.7rc1/rc2 (2026-08-17/19), v1.5.6 (2026-08-06). Paper arXiv 2410.05779 (v3 2025-04-28). |
| Verified on | 2026-10-18 (brief date; source and API read in this run) |
| Worker | V05 (registry worker W19) |

## 1. Identity, current status, tier, and sources

| Item | Verified value |
|---|---|
| Owner / licence | HKUDS GitHub organisation (paper authors Guo, Xia, Yu, Ao, Huang; institutional affiliation not verified); MIT (GitHub API + `pyproject.toml`). [CLAIM-lightrag-01] |
| Status | Very active: last push 2026-10-22, ~40.3k stars, roughly weekly-to-monthly releases. `SECURITY.md` supported-versions table lists only 1.3.x as supported (stale relative to 1.5.7). [CLAIM-lightrag-01] |
| Members | `lightrag-hku` core library (`lightrag/lightrag.py`, `operate.py`); LightRAG Server (FastAPI + React WebUI, Ollama-compatible API); document pipeline with parsers (native, MinerU, Docling), multimodal (VLM) support; storage adapters; maintenance tools. |
| Name collision | Forks and similarly named repositories exist (search results listed LLTrs/LightRAG, fpdb/LightRAG); the registry means HKUDS/LightRAG (paper Guo et al.). MiniRAG is a separate Tier C registry row; VideoRAG is a separate project (not verified as same maintainers). |
| Sources | Repo at tag, README, `docs/`, arXiv 2410.05779, GraphRAG-Bench 2506.05690, Zeng et al. 2506.06331, HippoRAG 2 paper 2502.14802. |

## 2. Primary problem, target workloads, example workflows

- Problem: give RAG entity/relationship awareness (multi-hop and thematic questions) with lower cost than GraphRAG and the ability to add documents without a rebuild. [CLAIM-lightrag-09]
- Target: small-to-mid document sets through a self-hostable server with WebUI; developer SDK; users who want "GraphRAG-like" behaviour with off-the-shelf storage (PostgreSQL, Neo4j, Milvus, Qdrant, ...).
- Workflows relevant to EOIP: (a) ingest runbooks and post-mortems, ask "which services share this failure pattern" (global-mode relation keys); (b) ask "what do we know about service X" (local-mode entity keys); (c) add one new document daily and expect cheap incremental update; (d) delete a withdrawn document and have derived facts disappear.

## 3. Feature inventory

| Feature | Status | Note |
|---|---|---|
| LLM entity/relation extraction with gleaning | present | default `max_gleaning=1`; JSON-output mode optional (`ENTITY_EXTRACTION_USE_JSON`) |
| Entity/relation description merging and LLM summary | present | forced LLM summary at 8 descriptions, capped source ids 200 per entity/relation |
| Query modes naive / local / global / hybrid / mix / bypass | present | default `mix` [CLAIM-lightrag-04] |
| Reranker | optional | recommended `bge-reranker-v2-m3`, adds 1-2 s [CLAIM-lightrag-04] |
| Incremental insert | present | upsert into existing graph; document status tracking |
| Delete document with graph repair | present | rebuild affected nodes/edges from LLM cache [CLAIM-lightrag-05] |
| Entity edit / merge / create API | present | `aedit_entity`, `amerge_entities`, `acreate_entity` |
| Graph storage options | present | NetworkX (dev), Neo4j, Memgraph, PostgreSQL (graph and table variants), MongoDB, OpenSearch [CLAIM-lightrag-02] |
| Vector storage options | present | NanoVectorDB (dev), Milvus, PGVector, Faiss, Qdrant, Mongo, OpenSearch |
| Server auth | partial | API key and JWT accounts; no per-document authorisation [CLAIM-lightrag-06] |
| Workspaces | present | logical data partition per instance/namespace |
| Per-role LLMs (extract/query/keyword/VLM) | present | [CLAIM-lightrag-07] |
| Citations | partial | returns references to source files/chunks; see 5.6 |
| WebUI incl. graph viewer, query-only `/workspace` entry | present | not a security boundary [CLAIM-lightrag-06] |
| MCP | absent in tree | none found |
| Re-embedding tool | absent | [CLAIM-lightrag-08] |
| Temporal / bitemporal graph | absent | |
| Ontology / schema enforcement | partial | configurable entity-type guidance only |

## 4. Architecture diagram

```
 files/text -> parser (native | MinerU | Docling | legacy) -> chunker (token 1200 or paragraph-semantic)
   -> pipeline queue (doc_status) -> extract_entities [LLM per chunk, gleaning, cache in KV]
   -> merge_nodes_and_edges [dedupe by normalised name; LLM summary when many descriptions]
   -> upsert: GRAPH_STORAGE (nodes+edges with source_ids) | VECTOR_STORAGE (entities, relations, chunks)
              KV_STORAGE (chunks, LLM cache, extraction results) | DOC_STATUS_STORAGE
 query -> keyword LLM -> {low-level keywords, high-level keywords}
       local : ll_keywords -> entities_vdb top_k -> graph neighbours/edges -> source chunks
       global: hl_keywords -> relationships_vdb top_k -> endpoint entities -> source chunks
       mix   : local + global + naive chunk vector search -> token-budget truncation -> optional rerank
       -> answer LLM (separate role) -> response + reference list
 isolation: workspace string prefix on all four stores; auth: API key / JWT at the FastAPI layer
```

## 5. Under-the-hood reconstruction (v1.5.7, `lightrag/...`)

**5.1 Data model.** Entity node: name (normalised key), type, description (concatenated or LLM-summarised), `source_id` list of chunk ids and `file_path` list. Relation edge: src, tgt, `keywords` (high-level theme tokens), description, weight, source ids. Three vector indices: entity names/descriptions, relation descriptions with keywords, and chunks. [CLAIM-lightrag-03]

**5.2 Extraction.** `operate.py::extract_entities` (~line 3941): per chunk, prompt `entity_extraction_system_prompt` (`prompt.py`), delimiter format `entity<|#|>name<|#|>type<|#|>description` and `relation<|#|>src<|#|>tgt<|#|>relationship_keywords<|#|>description`, completion marker `<|COMPLETE|>`; gleaning continuation prompt up to `DEFAULT_MAX_GLEANING=1`; JSON variant (`_process_json_extraction_result`) trades tokens for stability. Extraction results are cached (KV), which makes delete-and-rebuild and re-runs cheaper. Chunk-level concurrency set by `MAX_ASYNC_LLM`. README documents timeouts/loops with slower local models and bibliography chunks producing floods of low-value entities. [CLAIM-lightrag-03, -07]

**5.3 Merge.** `merge_nodes_and_edges` -> `_merge_nodes_then_upsert` / `_merge_edges_then_upsert`: new descriptions are unioned into existing nodes; when description count crosses `FORCE_LLM_SUMMARY_ON_MERGE=8` an LLM summary (`summarize_entity_descriptions`, `DEFAULT_SUMMARY_MAX_TOKENS=1200`) is produced; source-id lists are capped at 200 with a configurable limit method (default: stop updating once capped, which README says speeds construction). Entity identity = exact normalised string; no embedding-based resolution at write time (explicit merge API exists for manual curation). [CLAIM-lightrag-03, -05]

**5.4 Query (dual-level).** `kg_query` (~line 4588): `get_keywords_from_query` runs one keyword-extraction LLM call returning `high_level_keywords` and `low_level_keywords`. `_build_query_context` (~line 5895) is a four-stage pipeline: (1) `_perform_kg_search`: local mode embeds low-level keywords against the entity vector index (`top_k=40`), pulls adjacent edges (`_find_most_related_edges_from_entities`) and related chunks (`_find_related_text_unit_from_entities`); global mode embeds high-level keywords against the relation index, pulls endpoint entities and chunks; mix adds plain chunk vector search (`chunk_top_k=20`); (2) `_apply_token_truncation` with budgets `MAX_ENTITY_TOKENS=6000`, `MAX_RELATION_TOKENS=8000`, `MAX_TOTAL_TOKENS=30000`; (3) `_merge_all_chunks` (optional reranker); (4) `_build_context_str` prompting `kg_query_context`. Chunk picking from graph items by `KG_CHUNK_PICK_METHOD=VECTOR` (cosine to query, threshold 0.2) or weight. Per query: 1 keyword LLM call + 1 answer LLM call + embedding calls, independent of graph size. [CLAIM-lightrag-04]

**5.5 Incremental update and deletion.** Insert path = same pipeline; graph merge makes it additive (no corpus-level artefacts such as community reports exist, which is the structural reason updates are cheap). `adelete_by_doc_id` (`lightrag.py` ~line 5718) removes chunks and doc status, subtracts the document's source ids from nodes/edges, deletes entities left with no sources, and **rebuilds** partially affected entities/relations from cached extraction results of the remaining chunks (`rebuild_knowledge_from_chunks`, `_rebuild_single_entity`); a pipeline-level lock serialises deletions. Verified from source and docstring; not executed. [CLAIM-lightrag-05]

**5.6 Citations.** Context items carry file paths and chunk ids; the response API returns references; the answer prompt instructs reference formatting. The LLM writes the in-text references; span-level anchoring is absent (source reading, moderate confidence). [CLAIM-lightrag-04]

**5.7 Storage layout, concurrency, consistency.** Four pluggable stores selected by env; default JSON/NetworkX/NanoVectorDB files "for development and debugging, not production". Multi-worker deployment uses shared-storage locks (`kg/shared_storage.py`); docs insist all old writers stop before upgrades against a shared workspace. No cross-store transaction: graph, vector and KV writes are separate upserts (inference from the architecture; failure-recovery behaviour not tested). Changing embedding model, dimension, or asymmetric settings requires clearing and re-indexing; no re-embed tool. [CLAIM-lightrag-08, -14]

**5.8 Security.** FastAPI layer: `LIGHTRAG_API_KEY`, JWT accounts (refuses default token secret), login rate limiting, body-size and admission middleware. Data layer: `workspace` string isolates stores logically. Grep for acl/permission/tenant/principal/owner across the package finds only OS-level permission handling. There is no per-document or per-user authorisation: every authenticated caller of a workspace sees all facts, and entity descriptions merge text from all documents in it. [CLAIM-lightrag-06]

## 6. Functional and non-functional requirements inferred

FR: add/delete documents without rebuild; retrieve by entity (local) and theme (global) with one keyword LLM call; pluggable storage including Neo4j; per-role models. NFR: extraction needs a strong instruct model (README minimum for local deployment is Qwen3-30B-A3B-Instruct class) and non-thinking mode; reranker and embedding model should be local; embedding model is immutable after indexing. [CLAIM-lightrag-07, -08]

## 7. Performance and resource model

| Evidence | Workload / setup | Result | Class |
|---|---|---|---|
| LightRAG paper | UltraDomain Agriculture/CS/Legal/Mix, GPT-4o-mini, LLM judge | Overall win rate vs NaiveRAG ~57-85%; vs GraphRAG near even (52.8% Legal, 49.6% Mix); retrieval on Legal: GraphRAG ~610k tokens vs LightRAG under 100 tokens and one API call; incremental update claimed cheaper than regenerating GraphRAG reports. [CLAIM-lightrag-09] | author claim |
| GraphRAG-Bench | novel + medical, GPT-4o-mini | LightRAG tokens per query 100,832 (novel), 100,310 (medical) vs vanilla RAG 879-954; best creative-generation faithfulness on medical (78.76 vs 36.74 vanilla); not best on fact retrieval or reasoning. [CLAIM-lightrag-10] | independent |
| HippoRAG 2 paper | MuSiQue ~11.7k passages | LightRAG indexing ~68.5M input tokens (vs HippoRAG 2 ~9.2M, GraphRAG ~115.5M); reported average QA F1 6.6, which is implausibly low and probably reflects configuration or output-format mismatch; treat as unreliable. [CLAIM-lightrag-12] | competitor-authored |
| Zeng et al. | unbiased re-evaluation | Same LightRAG system run twice: win rate 90% vs 10% under LLM-judge protocol; true gains "much more moderate". [CLAIM-lightrag-11] | independent |

Reconciling the 100-token paper claim with the 100k-token benchmark: the paper's figure plausibly counts the keyword-generation call only, the benchmark counts the full answer prompt, which the defaults permit up to ~30k tokens (`MAX_TOTAL_TOKENS`); the benchmark's setting is not fully known. Unresolved. No independent p95 latency, memory-per-million-entities or disk numbers found. Failure modes: extraction loops/timeouts on slow local models, bibliography entity floods, silent description staleness once source-id cap reached (by design), duplicate entities from string identity.

## 8. Strengths

| Strength | Evidence | Match or exceed in EOIP |
|---|---|---|
| Per-query cost independent of graph size: 1 keyword + 1 answer call | source 5.4 | Replace keyword LLM with deterministic/lexical keyword split under policy; LLM optional |
| Additive incremental insert with no corpus-level summaries | source 5.5 | EOIP source events already versioned (BL-23/24) |
| Delete with graph repair via cached extractions | source 5.5 | EOIP tombstones (BL-25) plus provenance (BL-41) can do this exactly and without LLM |
| Backend-pluggable stores incl. Neo4j and Memgraph | source 5.7 | Shows a mapping of "entity/relation/chunk" stores onto graph DB + vector DB; supports feasibility of backend neutrality |
| Reranker + mix mode as default; per-role LLMs | README | Adopt role split in model abstraction |
| Usable server/WebUI and graph editor APIs | repo | Reference for review UX |

## 9. Limitations and root causes

| Class | Limitation | Basis | Root cause |
|---|---|---|---|
| Algorithmic | Gains over strong RAG not established; judge bias | verified, independent [CLAIM-lightrag-11] | Evaluation via LLM win-rate; no ground-truth metrics in the paper |
| Algorithmic | Entity identity by string; duplicates and drift | source | No resolution at write time |
| Algorithmic | Relation keys are free text: global mode retrieval quality depends on LLM keyword wording | source (hypothesis on effect) | Dual-level design relies on LLM-written themes |
| Operational | Extraction LLM per chunk dominates indexing; heavy token use (68.5M on 11.7k passages, third-party) | [CLAIM-lightrag-12] | Per-chunk LLM extraction |
| Operational | Large answer prompts (up to 30k tokens by default) | [CLAIM-lightrag-04, -10] | Context stuffing of entities+relations+chunks |
| Operational | Default stores not for production; no cross-store transactions; embedding model change forces full re-index | docs [CLAIM-lightrag-08, -14] | Pluggable, loosely coupled stores |
| Friction | No ACL / tenant model; workspace only | [CLAIM-lightrag-06] | Out of scope |
| Friction | Local-model fragility (loops, timeouts, thinking models slow) | README [CLAIM-lightrag-07] | Long structured generations |
| Friction | Rapid release churn (api version, storage migrations, upgrade requires stopping all writers) | docs | Fast-moving project |
| Licensing | None known (MIT); dependency licences not audited (UNVERIFIED) | | |

## 10. Deployment, licensing, redistribution, viability

MIT. Docker, Docker Compose (including full stack with Postgres), Kubernetes and Podman manifests, offline deployment guide (`docs/OfflineDeployment.md`) and offline requirement files exist; local LLM via Ollama or any OpenAI-compatible endpoint; local embedding (`bge-m3`) and reranker recommended. Air-gap: **yes in principle** (offline requirements files provided; parsers like MinerU can run locally); quality gated by local model strength. One-node: yes with default file stores, PostgreSQL single-instance recommended for production. Redistribution: MIT permits embedding or OEM; third-party parser/model licences (MinerU, Docling, model weights) need separate review, no conclusion given. Multi-tenant white-label: one workspace per tenant gives logical separation only; physical isolation needs separate databases.

## 11. Competitive delta against EOIP baseline

| EOIP | Delta |
|---|---|
| BL-16 deterministic graph-first retrieval | LightRAG is LLM-built-graph + vector retrieval; EOIP's retrieval is deterministic, so no LLM at ingest, but also no theme-level (relation-keyword) index. No benchmark of BL-16 vs plain RAG exists; LightRAG has one only from authors |
| BL-14 dense (hashing embedder) | LightRAG assumes strong embeddings (bge-m3) and notes retrieval quality is only weakly dependent on them; EOIP's hashing default is a real gap for any vector leg |
| BL-15 RRF hybrid | EOIP has RRF; LightRAG `mix` is concatenation with token truncation and optional rerank. EOIP could match with a reranker |
| BL-24/25 replay, tombstones, BL-41 provenance | EOIP ahead structurally on deletion correctness (exact provenance vs LLM-cache rebuild) |
| BL-18 ACL enforcement absent | Both lack ACL in retrieval; EOIP captures ACL metadata (BL-17), LightRAG does not |
| BL-01..05 backends | LightRAG proves graph+vector stores can sit on Neo4j/Memgraph/PG; EOIP's `GraphStore` has no vector or KV roles |

## 12. Strength-adoption and inversion cards

| ID | Competitor | Strength | Evidence | Value | Decision | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-lightrag-01 | LightRAG | Dual-level keys: entity index for specifics, relation-theme index for concepts | [CLAIM-lightrag-04] | Better recall on thematic questions without community reports | match (experiment) | Add relation-description embedding index to BL-16; deterministic keyword split first | On 100 mixed questions, recall@10 and answer accuracy >= best of BM25/dense/RRF; ground-truth metrics |
| STR-lightrag-02 | LightRAG | Additive update + exact delete repair | [CLAIM-lightrag-05] | Living-graph correctness | exceed | Tombstone events trigger removal of derived index entries by provenance (no LLM) | Delete 5% of docs: 0 residual facts, no re-extraction calls |
| STR-lightrag-03 | LightRAG | Per-role model routing | [CLAIM-lightrag-07] | Cost control, egress policy per role | match | Role-keyed model registry in egress gateway (BL-45) | Policy test: extraction role local-only, answer role configurable |

**INV-lightrag-01 (relates to seed hypothesis §10.5).** Target: LightRAG v1.5.7 on a MuSiQue-sized corpus. Limitation: LLM extraction per chunk keeps indexing at tens of millions of tokens, and query prompts reach tens of thousands. [CLAIM-lightrag-10, -12] Root cause: *proven* (source: per-chunk extraction; default 30k-token context). Hypothesis check: "dual-level indexing" as cost fix for GraphRAG is **only partly validated**: it removes community summarisation and gives cheap updates, but extraction cost stays (same order as GraphRAG, ~0.6x on one third-party measurement) and answer-prompt cost can exceed vanilla RAG by ~100x. Alternative: deterministic extraction first (structured sources need no LLM), LLM extraction only for unstructured text under policy, smaller query budget with reranking. Worse when: corpora are mostly free prose where deterministic extraction yields little. Options: (1) quick: run LightRAG against local Ollama on a prose subset; (2) native: relation-theme index over EOIP graph edges plus reranker; (3) long: learned extractor distilled from LLM outputs on tenant data. Select 2. Benchmark: 5k-doc mixed corpus (tickets, runbooks, wiki); metrics answer accuracy (exact/F1 plus judged both orders), tokens/query, index tokens; baseline BM25+dense+rerank and LightRAG `mix`; success = >= baseline accuracy at <= 50% of LightRAG tokens/query. Failure cases: prompt injection through chunks into extraction. Defensibility: tied to EOIP provenance and ACL. Decision: **EXPERIMENT**.

**INV-lightrag-02.** Limitation: no ACL; descriptions merge text across all documents. Root cause *proven*. Alternative: store atomic per-source facts with `acl_hash` (BL-17) and compose descriptions at read time from permitted sources. Worse when: huge ACL cardinality causes read-time cost. Options: (1) workspace per role; (2) lazy composition; (3) ACL-aware index. Select 2. POC: 20 principals, canary facts, 0 leaks in 10k queries; latency overhead < 30%. Decision: **ADOPT** as constraint.

**INV-lightrag-03.** Limitation: string entity identity and no cross-store transaction. Root cause: *proven* (source) for identity, *hypothesis* for transaction failures. Alternative: route through EOIP identity (BL-34, CAP-31) and mutation gateway so indexes are derived views rebuilt idempotently from the graph. POC: kill the process mid-ingest 100 times; success = indexes converge with 0 orphans after replay (BL-24). Decision: **ADOPT** (architecture principle).

## 13. Per-capability decisions

| Capability | Decision | Note |
|---|---|---|
| CAP-56 dual-level retrieval | EXPERIMENT | pattern, not dependency |
| CAP-55 hybrid retrieval | BUILD | RRF + local reranker beats `mix` concatenation (to be proven) |
| CAP-53 vector search | INTEGRATE | strong local embedder (bge-m3 class) replacing hashing default |
| CAP-67 incremental re-index | BUILD | provenance-driven delete repair |
| CAP-32 LLM extraction | EXPERIMENT | optional, policy-gated, local model |
| CAP-46 ACL | BUILD | INV-02 |
| CAP-61 role-based local model serving | INTEGRATE | Ollama/vLLM via existing abstraction |
| LightRAG as embedded dependency | REJECT | no ACL, loose transactions, churn; use as comparison harness only |
| CAP-71 graph editor/review UX | REFERENCE-ONLY | WebUI patterns |

## 14. Tests, POC, acceptance

1. Install v1.5.7 offline with Ollama (Qwen3-30B-A3B class and a 7-8B model), index 500 EOIP-shaped docs; log extraction failures, loops, tokens, wall time.
2. Controlled comparison on the same questions: BM25, dense, RRF, +reranker, LightRAG naive/local/global/hybrid/mix, EOIP BL-16; ground-truth metrics and two-order LLM judge; fixed answer length budget.
3. Delete/update test (STR-02) and ACL canary (INV-02).
4. Crash-recovery test (INV-03).
5. Accept pattern adoption only if it beats the strongest non-graph baseline on a defined question class without exceeding token budget.

## 15. Risks and open questions

Self-reported results; judge bias; LightRAG's own paper and the third-party measurement disagree by orders of magnitude on tokens; HippoRAG 2 paper's F1 for LightRAG looks like a failed reproduction; fast release cadence (storage migrations) raises upgrade risk; security posture of server for hostile networks not audited; relation-keyword quality on non-English content unknown; effect of string-identity duplicates on multi-hop recall unmeasured.

## Appendix A. Research-dimension coverage

| Dimension | Sections | Summary |
|---|---|---|
| D1 Identity | 1 | HKUDS, MIT, v1.5.7 |
| D2 Problem | 2 | Cheap graph-RAG with updates |
| D3 Architecture | 4, 5 | Pipeline + 4 stores |
| D4 Storage | 5.7 | Pluggable KV/graph/vector/doc-status |
| D5 Schema | 5.1 | Typed entities, free-text relations |
| D6 Query pipeline | 5.4 | keyword LLM, 4-stage context |
| D7 Reasoning | N/A | None beyond LLM |
| D8 Transactions/scale | 5.7 | No cross-store tx; locks |
| D9 Ingestion | 5.2, 5.5 | Parsers, queue, status |
| D10 Identity/evidence | 5.3, 5.6 | String identity; file/chunk refs |
| D11 Time | N/A | No temporal model |
| D12 Graph ML | N/A | None |
| D13 Retrieval/agents | 5.4, 5.6 | Modes, rerank; no MCP found |
| D14 NL query | N/A | Not text-to-query |
| D15 Governance | 3 | Entity edit/merge API only |
| D16 UX | 3 | WebUI, graph viewer |
| D17 DevEx | 3, 10 | SDK + REST + Docker/K8s |
| D18 Security | 5.8 | Key/JWT; no ACL |
| D19 Multi-tenancy | 5.8, 10 | Workspace only |
| D20 Economics | 7 | Conflicting token evidence |
| D21 Commercial | 10 | MIT |
| D22 Interop | 3 | Neo4j/Memgraph/PG |
| D23 IP | N/A | No patent info verified |
| D24 Research quality | 7, 15 | Author claims vs independent |

## Appendix B. Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-56 | native | 04 | BL-16 Implemented | EXPERIMENT | P1 |
| CAP-55 | partial (mix) | 04 | BL-15 Implemented | BUILD | P1 |
| CAP-53 | plugin | 02 | BL-14 Partial | INTEGRATE | P1 |
| CAP-32 | native | 03 | BL-26 (JSON only) | EXPERIMENT | P2 |
| CAP-67 | native | 05 | BL-42/24 partial | BUILD | P1 |
| CAP-46 | absent | 06 | BL-18 Absent | BUILD | P0 |
| CAP-47 | partial (workspace) | 06 | BL-20 Partial | BUILD | P0 |
| CAP-60 | partial | 04 | BL-41 | BUILD | P1 |
| CAP-61 | native roles | 07 | BL-45 | INTEGRATE | P2 |
| CAP-50 | partial | 14 | BL-45 | EXPERIMENT | P2 |
| CAP-78 | absent in project | 11 | none | BUILD | P1 |

## Appendix C. Evidence records

| CLAIM-ID | product/version/date | claim | class | source | pub / access | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-lightrag-01 | v1.5.7, 2026-09-02 | MIT; active; ~40.3k stars; last push 2026-10-22; SECURITY.md lists 1.3.x as supported | Officially documented | github.com/HKUDS/LightRAG (API, `pyproject.toml`, `SECURITY.md`) | 2026-10-18 | 0.95 | none |
| CLAIM-lightrag-02 | v1.5.7 | storage implementations: KV (JSON, Redis, PG, Mongo, OpenSearch), graph (NetworkX, Neo4j, PG, PGTable, Mongo, Memgraph, OpenSearch), vector (Nano, Milvus, PGVector, Faiss, Qdrant, Mongo, OpenSearch), doc-status | Observed in source | `lightrag/kg/__init__.py` | 2026-10-18 | 0.95 | none |
| CLAIM-lightrag-03 | v1.5.7 | extraction prompt and delimiter format; gleaning default 1; JSON mode; forced LLM summary at 8; source-id caps 200 | Observed in source | `lightrag/prompt.py`, `constants.py`, `operate.py` | 2026-10-18 | 0.9 | none |
| CLAIM-lightrag-04 | v1.5.7 | query modes (default mix); keyword LLM -> ll/hl; four-stage context; defaults top_k 40, chunk_top_k 20, tokens 6000/8000/30000; rerank adds 1-2 s | Observed in source / documented | `base.py` QueryParam, `operate.py` kg_query/_build_query_context, README | 2026-10-18 | 0.9 | none |
| CLAIM-lightrag-05 | v1.5.7 | delete by doc id rebuilds affected entities/relations from cached extractions; entity edit/merge/create APIs | Observed in source (docstring) | `lightrag/lightrag.py` `adelete_by_doc_id` | 2026-10-18 | 0.8 | not executed |
| CLAIM-lightrag-06 | v1.5.7 | API key + JWT auth; workspace isolation; no per-user/per-document ACL (grep); `/workspace` UI not a security boundary | Observed in source / documented | `lightrag/api/config.py`, README, docs | 2026-10-18 | 0.85 | absence by grep |
| CLAIM-lightrag-07 | v1.5.7 | four LLM roles; local minimum Qwen3-30B-A3B-Instruct; non-thinking extraction; timeout/loop guidance | Officially documented | README "Key Configuration Guide" | 2026-10-18 | 0.9 | none |
| CLAIM-lightrag-08 | v1.5.7 | embedding model must be fixed before indexing; no re-embedding tool | Officially documented | README | 2026-10-18 | 0.95 | none |
| CLAIM-lightrag-09 | paper v3, 2025-04-28 | UltraDomain/GPT-4o-mini; win rates 57-85% vs NaiveRAG, ~even vs GraphRAG; Legal retrieval 610k tokens vs <100 tokens; incremental update without rebuild | Vendor (author) claim | arXiv 2410.05779 https://arxiv.org/html/2410.05779 | 2024-10 / 2026-10-18 | 0.7 | CLAIM-lightrag-10, -11 |
| CLAIM-lightrag-10 | GraphRAG-Bench | LightRAG ~100.8k tokens/query (novel), 100.3k (medical) vs vanilla 879/954; medical creative FS 78.76 vs 36.74 | Independent benchmark | arXiv 2506.05690 https://arxiv.org/abs/2506.05690 | 2025-06-06 / 2026-10-18 | 0.8 | CLAIM-lightrag-09 |
| CLAIM-lightrag-11 | Zeng et al. | Two LightRAG instances: win rate 90% vs 10% under LLM judge; gains "much more moderate" | Independent benchmark | arXiv 2506.06331 https://arxiv.org/abs/2506.06331 | 2025-05-31 / 2026-10-18 | 0.7 (abstract + search snippet) | none |
| CLAIM-lightrag-12 | HippoRAG 2 paper | LightRAG ~68.5M indexing input tokens on MuSiQue 11.7k passages; average F1 6.6 | Third-party report (competitor) | arXiv 2502.14802 https://arxiv.org/html/2502.14802 | 2025-02-20 / 2026-10-18 | 0.4 | F1 anomaly suggests poor reproduction |
| CLAIM-lightrag-14 | v1.5.7 | default storages dev-only; production on PG/Mongo/OpenSearch; stop all writers before upgrade | Officially documented | README, `docs/` upgrade notes | 2026-10-18 | 0.9 | none |

## Appendix D. Assumptions

- Brief access date 2026-10-18 recorded; fetches ran 2026-10-26.
- Paper's exact venue not verified (arXiv comments not seen); omitted.
- Cross-store consistency behaviour inferred from design, not tested.
- GraphRAG-Bench configuration behind the 100k tokens/query figure is not fully known.
- Dependency and model licences, security advisories not checked (UNVERIFIED).
