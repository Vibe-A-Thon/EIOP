| Field | Value |
|---|---|
| Registry ID | T-C08-hipporag |
| Tier | A (PPR-based memory retrieval; candidate pattern for the inverted design in seed hypothesis §10.5) |
| Versions examined | OSU-NLP-Group/HippoRAG: tag v1.0.0 (2025-02-27, HippoRAG v1 code, commit b144c46); `main` at commit d5c8329 (2026-10-06), package version `2.0.0a5` (HippoRAG 2, alpha, no release tag). Papers: HippoRAG arXiv 2405.14831 (v3 2025-01-14), HippoRAG 2 arXiv 2502.14802 (v2 2025-06-19). |
| Verified on | 2026-10-18 (brief date; source and APIs read in this run) |
| Worker | V05 (registry worker W19) |

## 1. Identity, current status, tier, and sources

| Item | Verified value |
|---|---|
| Owner / licence | OSU NLP Group (Ohio State University; lead author B. J. Gutierrez, Y. Su); MIT (`LICENSE`, "Copyright (c) 2025 OSU Natural Language Processing"). [CLAIM-hipporag-01] |
| Status | Research code, active but pre-release: GitHub's only release is v1.0.0 (2025-02-27); `main` is `2.0.0a5` (alpha) with commits through 2026-10-06 (OpenAI-compatible endpoints, MCP server, Claude Code plugin). ~4.1k stars; branches `main`, `develop`, `legacy`, `backup-main`. Not archived. [CLAIM-hipporag-01, -15] |
| Version trap | The v1.0.0 tag contains **HippoRAG v1** code (`src/hipporag.py`, ColBERTv2, Elasticsearch helpers); HippoRAG 2 lives only on `main` (`src/hipporag/HippoRAG.py`). Pin by commit, not tag, for v2. |
| Members | HippoRAG v1 (NeurIPS 2024 per arXiv comments), HippoRAG 2 (ICML 2025 per arXiv comments), `hipporag-mcp` server, StandardRAG baseline class. |
| Sources | Repo, README, both arXiv papers, GraphRAG-Bench 2506.05690, Han et al. 2502.11371. |

## 2. Primary problem, target workloads, example workflows

- Problem: associative multi-hop and "memory" retrieval over a corpus without iterative LLM retrieval loops; one retrieval step that propagates relevance across entities. [CLAIM-hipporag-02]
- Targets: multi-hop QA (MuSiQue, 2Wiki, HotpotQA), factual QA (NQ, PopQA), long narrative (NarrativeQA). Positioned by authors as non-parametric continual learning for LLMs.
- EOIP workflows: "Which incident, change and ticket together explain X" (associative multi-hop across documents); agent long-term memory that adds documents continuously and answers with passages. Not for global thematic summaries or permissioned retrieval.

## 3. Feature inventory

| Feature | Status | Note |
|---|---|---|
| OpenIE: NER then entity-conditioned triple extraction (LLM) | present | prompts in `prompts/templates/{ner,triple_extraction}.py` |
| Passage + entity + fact embedding stores | present | parquet default; Qdrant, Chroma, Milvus options |
| Synonymy edges by embedding kNN | present | threshold 0.8 default |
| Personalised PageRank retrieval | present | python-igraph `prpack` |
| Fact-to-graph linking with LLM triple filter ("recognition memory") | present (v2) | DSPy-derived prompt |
| Incremental `index()` | present | OpenIE cached per chunk; synonymy only for new nodes |
| `delete()` | present | source-aware edges; refuses legacy graphs |
| QA generation, IRCoT multi-step | present | `rag_qa`, `retrieve_ircot` |
| Local LLM / embeddings | partial | vLLM or any OpenAI-compatible endpoint; transformers offline modes |
| MCP server | present (alpha) | stdio or streamable HTTP; `--read_only` flag [CLAIM-hipporag-09] |
| Server / UI / admin | absent | library only |
| ACL / tenancy | absent | [CLAIM-hipporag-09] |
| Community summaries / global search | absent | |
| Temporal / provenance beyond chunk id | partial | `source_id` and chunk metadata only |
| Graph DB backend | absent | in-memory igraph pickled to disk |

## 4. Architecture diagram

```
 docs -> chunks (hash id = md5 of text)
   -> OpenIE (LLM): NER -> triples(conditioned on entities)   [cached per chunk: openie_results json]
   -> stores: chunk_emb | entity_emb | fact_emb          (parquet | qdrant | chroma | milvus)
   -> graph (igraph, undirected PPR projection): nodes = entities + passages
        edges: fact (entity-entity, weight=#supporting facts) | passage (passage-entity) | synonym (kNN cos>=0.8)
   -> pickle graph + source-aware edge metadata
 retrieve(q): embed q -> score all facts (cos) -> top linking_top_k=5 -> LLM triple filter (recognition memory)
        -> seeds: entities of surviving facts (weighted by fact score / #chunks of entity)
                  + ALL passage nodes weighted dense_score * 0.05
        -> PPR(damping 0.5) -> rank passages (top 200 default) ; if no facts survive -> dense retrieval fallback
 qa: top-k passages -> reader LLM
```

## 5. Under-the-hood reconstruction

**5.1 Data model** (`HippoRAG.py` at d5c8329). Nodes: `entity-<md5(phrase)>` and `chunk-<md5(text)>`. Facts are (subject, predicate, object) triples stored as strings in a fact embedding store; they are **not** graph edges with predicate labels: only subject-object adjacency with weight survives in the graph (predicate text lives in the fact store). Chunk metadata (`source_id`, user metadata) persisted separately. [CLAIM-hipporag-03]

**5.2 Indexing** (`index()`, ~line 499). (1) Insert chunks into the chunk store; (2) `load_existing_openie` finds chunks lacking cached OpenIE and runs `batch_openie` only for those (NER, then triple extraction conditioned on the entity list; online, vLLM-offline, or transformers-offline variants); (3) normalise triples (`text_processing`), derive entity nodes, flatten facts; (4) embed new entities and facts; (5) `add_fact_edges` (weight += 1 per supporting fact, counts tracked per source chunk), `add_passage_edges` (passage node to each entity from that chunk), `add_synonymy_edges`; (6) `augment_graph`, `save_igraph`. State checks raise `StateConsistencyError` on mismatched counts or legacy graphs. [CLAIM-hipporag-03]

**5.3 Synonymy edges** (`add_synonymy_edges`, ~line 1278). kNN over entity embeddings (`synonymy_edge_topk=2047`, `sim_threshold=0.8`), skipping entities with <=2 alphanumerics, up to 100 neighbours kept per node; incremental updates query only newly inserted entities against all stored ones (comment: "to reduce cost for incremental graph updates"). Edge weight = max similarity. This is soft entity resolution done by vector similarity rather than merging nodes. Threshold sensitivity unmeasured by us. [CLAIM-hipporag-05]

**5.4 Retrieval** (`retrieve()` ~line 704; `graph_search_with_fact_entities` ~line 2008; `run_ppr` ~line 2177). Steps: query embedding; `get_fact_scores` (cosine to all fact embeddings); candidate facts = top `linking_top_k=5`; `rerank_facts` calls the LLM through a DSPy-style prompt (`rerank.py::DSPyFilter`) to keep only relevant triples (recognition memory) - an LLM call per query; seed weights: for each surviving fact's subject and object, add fact score divided by the number of chunks containing the entity (down-weights hub entities, an IDF-like step), averaged over occurrences; passage seeds: all passages get min-max-normalised dense score times `passage_node_weight=0.05`; PPR with `damping=0.5`, `weights='weight'`, undirected, `implementation='prpack'`; passages ranked by PPR mass; default `retrieval_top_k=200`. If no fact survives filtering, falls back to dense passage retrieval. [CLAIM-hipporag-04, -06]

**5.5 v1 vs v2 differences** (README, paper, v1 tag). v1: NER on query, entity linking by embedding, PPR damping 0.1 in `src/hipporag.py`, passages scored through an entity-to-passage matrix, ColBERTv2 retriever. v2: queries matched to whole triples ("deeper contextualisation"), passage nodes inside the graph with dense-score seeding ("dense-sparse integration"), LLM triple filter ("recognition memory"), NV-Embed-v2 default in paper. Paper ablation (recall@5, avg of MuSiQue/2Wiki/HotpotQA): full 87.1; NER-to-node linking 74.6; query-to-node linking 59.6; without passage nodes 81.0; without triple filter 86.4. [CLAIM-hipporag-10]

**5.6 Incremental update and deletion.** `index()` is additive: cached OpenIE is reused, synonymy is computed for new entities only, and the graph is rebuilt in memory from counters (`add_new_nodes/edges`, `merge_metadata`). `delete()` (~line 595) removes chunks, subtracts their facts using persisted per-chunk OpenIE provenance and source-aware edge counts, and raises if provenance is missing; the docstring notes entities/triples from retained chunks stay. Verified by reading, not by running. [CLAIM-hipporag-07]

**5.7 Storage, concurrency, consistency.** Graph is a python-igraph object held in RAM and pickled (`graph_pickle_filename`); embedding stores are parquet files by default (atomic temp-file writes) or Qdrant/Chroma/Milvus. No transactions; single-process library; `__enter__/__exit__` close handles. PPR over the whole graph per query (prpack) - cost grows with node+edge count; the paper reports QA time ~1.2 s per query and ~9.9 GB QA GPU memory on its setup. [CLAIM-hipporag-08, -10]

**5.8 Security.** Grep for acl/permission/tenant/principal over `src/hipporag` finds nothing. MCP server README: HTTP transport "has no authentication", keep on loopback or behind an authenticating proxy; `--read_only` disables `index` and `delete` tools. All users of an index see all passages. [CLAIM-hipporag-09]

**5.9 Citations.** Returns ranked passages with scores and `doc_metadata`; the QA step is a plain reader prompt; no claim-to-span mapping. Passage-level provenance is exact (retrieved text is the source), which is stronger than LLM-written citation tags.

## 6. Functional and non-functional requirements inferred

FR: continually add documents; retrieve passages by associative multi-hop in one step; delete documents; use any OpenAI-compatible LLM. NFR: needs an instruct LLM for OpenIE and per-query triple filtering; embedding model matters (paper uses NV-Embed-v2, GPU); graph must fit in RAM; Python 3.10; alpha API stability not promised. [CLAIM-hipporag-14]

## 7. Performance and resource model

| Evidence | Workload / setup | Result | Class |
|---|---|---|---|
| HippoRAG 2 paper | 7 datasets, Llama-3.3-70B reader, NV-Embed-v2 | Avg QA F1: HippoRAG 2 59.8 vs NV-Embed-v2 dense 57.0 vs HippoRAG 53.1 vs GraphRAG 49.6 vs RAPTOR 48.8; passage recall@5 78.2 vs 73.4 dense. Indexing MuSiQue ~11.7k passages: 99.5 min, ~9.2M input tokens (v1 57.5 min, similar tokens); GraphRAG ~115.5M. [CLAIM-hipporag-10] | author claim |
| GraphRAG-Bench | novel/medical, GPT-4o-mini, vs vanilla RAG with rerank | Tokens per query: HippoRAG 2 1,008 (novel) vs vanilla 879; HippoRAG v1 7,208; Complex reasoning ACC 53.38 vs 42.93; fact retrieval 60.14 vs 60.92 (novel) but 66.28 vs 64.73 (medical); summarisation 64.10 (MS-GraphRAG 64.40, vanilla 51.30). [CLAIM-hipporag-11] | independent |
| Han et al. | Llama-3.1-8B | HotpotQA F1 63.01 vs RAG 60.04; MultiHop-RAG 70.27 vs 67.02; NQ 61.03 vs 64.78 (RAG better); NovelQA 56.54 vs 57.12. [CLAIM-hipporag-12] | independent |
| HippoRAG v1 paper | MuSiQue, 2Wiki, HotpotQA | Claims up to 20% over prior RAG; 10-30x cheaper and 6-13x faster than iterative retrieval (IRCoT) with comparable or better accuracy. [CLAIM-hipporag-13] | author claim |

Hardware for our target (CPU-only one-node): NOT PUBLICLY VERIFIED. Indexing minutes figure relies on the authors' GPU/API setup. Failure modes: bad OpenIE JSON (a 2026-09 PR title mentions OpenIE JSON-parsing fixes), synonymy threshold errors creating false merges via soft edges, hub entities, whole-graph PPR per query at large scale (hypothesis: sub-second only up to some graph size; not measured).

## 8. Strengths

| Strength | Evidence | Match or exceed in EOIP |
|---|---|---|
| Near-vanilla query cost with graph benefit (about 1k tokens vs 0.9k) | [CLAIM-hipporag-11] | Same retrieval step can run with no LLM if triple filter replaced by a local reranker |
| Best-measured multi-hop gain among graph methods in two independent benchmarks (reasoning ACC +10.45 points; HotpotQA/MultiHop-RAG +3 points) | [CLAIM-hipporag-11, -12] | PPR is a standard algorithm EOIP can run on its own graph (BL-43) or a backend |
| Indexing about 12x fewer tokens than GraphRAG on the same corpus (author-run) | [CLAIM-hipporag-10] | EOIP deterministic extraction removes most remaining cost |
| Passage-level exact provenance; graph is a derived index | source | Matches EOIP evidence model (BL-41) |
| Soft entity resolution via synonym edges (no destructive merge) | source 5.3 | Compatible with EOIP review-queue merges (BL-35): propose, don't merge |
| Incremental index + delete with provenance | source 5.6 | Same design goals as EOIP replay/tombstone |

## 9. Limitations and root causes

| Class | Limitation | Basis | Root cause |
|---|---|---|---|
| Algorithmic | No hierarchical/global summarisation capability (it matched MS-GraphRAG on summarisation ACC in one benchmark, but cannot produce theme reports) | [CLAIM-hipporag-11]; inference | PPR returns passages only |
| Algorithmic | Underperforms dense on simple fact retrieval in some sets (NQ F1 61.03 vs 64.78; novel fact ACC 60.14 vs 60.92) | [CLAIM-hipporag-11, -12] | Graph seeds add noise on single-hop |
| Algorithmic | Predicate semantics dropped from graph edges; weights are co-occurrence counts | source 5.1 | Graph built for propagation, not reasoning |
| Algorithmic | Soft synonymy via cosine threshold: false positives merge distinct entities in propagation | hypothesis | Embedding similarity not identity |
| Operational | In-memory igraph + pickle; whole-graph PPR; one process | source 5.7 | Library design |
| Operational | Indexing tokens still ~9M per 11.7k passages and 99.5 min author-run | [CLAIM-hipporag-10] | LLM OpenIE per chunk |
| Operational | LLM call per query for triple filtering; GPU-heavy reference setup (NV-Embed-v2, 70B) | source, [CLAIM-hipporag-10] | Recognition memory step |
| Friction | Alpha version 2.0.0a5, no v2 release tag, tag v1.0.0 holds old code | [CLAIM-hipporag-15] | Research cadence |
| Friction | No ACL, no tenancy, unauthenticated HTTP MCP | [CLAIM-hipporag-09] | Out of scope |
| Friction | Python 3.10, heavy ML dependency set (torch, transformers, vLLM optional) | README, requirements | Research stack |
| Licensing | None (MIT); model weights (NV-Embed-v2 etc.) carry separate licences, not checked (UNVERIFIED) | | |

## 10. Deployment, licensing, redistribution, viability

MIT, library only; pip install from source (`hipporag` extras for vLLM, MCP). Air-gap: **partial-to-yes**: works with vLLM or any OpenAI-compatible local endpoint and local embedding models (README local vLLM example uses Llama-3.3-70B on 2 GPUs, which exceeds one-node CPU-only constraints; smaller models untested by us). One-node: yes at small corpus; RAM scales with graph. Redistribution: MIT; third-party model licences need review. Multi-tenant: one index directory per tenant; no isolation inside. Not a service; EOIP would reimplement the pattern (small: igraph PPR + fact index) rather than embed alpha research code.

## 11. Competitive delta against EOIP baseline

| EOIP | Delta |
|---|---|
| BL-16 graph-first retrieval | BL-16 is deterministic entity/graph expansion with evidence; HippoRAG seeds a PPR from query-matched facts plus dense passage scores. No evidence BL-16 matches HippoRAG's multi-hop gains; no benchmark exists |
| BL-14 hashing embedder; BL-13 BM25; BL-15 RRF | HippoRAG's gains are measured against strong dense retrievers (NV-Embed-v2); EOIP's dense leg is far weaker, so the same experiment on EOIP would conflate embedder quality with graph benefit |
| BL-43 graph algorithms (pure Python) | EOIP has centrality/community; PPR is a small extension. Scale of pure-Python PPR untested (U-06) |
| BL-26/34 schema profiling, identity | Deterministic keys give exact entity nodes without LLM OpenIE for structured sources; HippoRAG helps for unstructured text only |
| BL-18 ACL absent | Same absence; HippoRAG additionally has passage nodes that could carry `acl_hash`, enabling seed/propagation masking (hypothesis: mask before PPR so mass cannot flow through forbidden nodes) |
| BL-24/25 replay, tombstones | EOIP ahead on lifecycle |
| BL-47 MCP read tools | HippoRAG MCP is alpha with write tools; EOIP read-only by design (ADR-007) is stronger |

## 12. Strength-adoption and inversion cards

| ID | Competitor | Strength | Evidence | Value | Decision | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-hipporag-01 | HippoRAG 2 | PPR over entity+passage graph seeded by query facts and dense scores | [CLAIM-hipporag-04, -11, -12] | Multi-hop recall at near-vanilla token cost | match | `ppr_retrieve()` in `retrieval/` using `graph/algorithms.py`; seeds = BL-16 entity hits + dense scores x 0.05 | On MuSiQue/HotpotQA subset (>=500 q): recall@5 >= dense + 3 points with identical embedder; tokens/query within 20% of dense |
| STR-hipporag-02 | HippoRAG 2 | Soft synonym edges instead of destructive merge | [CLAIM-hipporag-05] | Alias tolerance with reversible decisions | match | Synonym candidates written as PROPOSED edges (BL-40) feeding the review queue (BL-35) | False-merge rate in propagation < 1% on labelled alias set |
| STR-hipporag-03 | HippoRAG 2 | Hub down-weighting (fact score / chunks-per-entity) | source 5.4 | Avoids supernode domination | match | Same weighting in seed construction | Ablation shows no regression on hub-heavy corpora |

**INV-hipporag-01 (tests the §10.5 candidate design: dual-level indexing with HippoRAG patterns).** Target: HippoRAG 2 (main d5c8329) vs MS GraphRAG v3.3.0 on MuSiQue-size corpora. Evidence: indexing ~9.2M vs ~115.5M tokens, per-query ~1.0k vs 38.7k (local) / 331k (global) tokens, and equal or better accuracy on multi-hop QA. [CLAIM-hipporag-10, -11, -12] Root cause of GraphRAG cost: *proven* by those measurements plus the project's own docs; HippoRAG avoids community summarisation and per-description LLM merging. Limit: HippoRAG cannot answer "what are the main themes" in prose form; its summarisation ACC parity is a single benchmark with one metric. Alternative worse when: workload is dominated by explicit global questions. Options: (1) integrate: run HippoRAG as a sidecar via its MCP on a prose subset; (2) pragmatic native: PPR retrieval in BL-16 plus optional on-demand summary of the retrieved subgraph; (3) long: learned seed selector. Select 2. Benchmark: MuSiQue + HotpotQA + MultiHop-RAG subsets plus 50 global questions on EOIP-shaped corpus; baselines BM25, dense (bge-m3), RRF, +reranker, HippoRAG 2 reference run, GraphRAG fast; metrics F1/recall@k/tokens; success = beats the best non-graph baseline on multi-hop by >=3 points absolute at <= 1.3x tokens. Failure cases: ACL leakage through propagation (see INV-02), synonym false merges. Defensibility: ACL-masked, provenance-exact PPR on a governed graph. **Seed hypothesis §10.5 verdict: partially validated** (token-cost claim supported for HippoRAG; "dual-level" is LightRAG's, and global-answer parity is unproven). Decision: **EXPERIMENT**.

**INV-hipporag-02.** Limitation: no ACL and propagation crosses all nodes. Root cause *proven* (grep) for absence, *hypothesis* for the leak path (PPR mass reaching passages whose entities connect through forbidden documents; relevance ranking can reveal existence). Alternative: build the PPR subgraph per caller from permitted passages only (ACL-filtered node/edge set; cache per ACL class). Worse when: ACL classes numerous, so no cache hits. Options: (1) per-role index; (2) on-the-fly induced subgraph with permitted-source filter; (3) ACL-aware sparse PPR with node masks. Select 2/3. POC: 20 principals, canary documents; 0 canary appearances in ranks or scores in 10k queries; p95 overhead < 40%. Decision: **ADOPT** (hard requirement).

**INV-hipporag-03.** Limitation: alpha maturity, unauthenticated MCP HTTP, in-memory pickled graph. Root cause: maturity/governance. Alternative: reimplement pattern on EOIP `GraphStore` (backend-neutral) with persisted indexes. Decision: **ADOPT** reimplementation, **REJECT** embedding upstream code.

## 13. Per-capability decisions

| Capability | Decision | Note |
|---|---|---|
| CAP-56 PPR associative retrieval | EXPERIMENT | native reimplementation |
| CAP-19 multi-hop retrieval | EXPERIMENT | benchmarked against RRF+rerank |
| CAP-62 PPR algorithm | REUSE | backend GDS where present, igraph/pure Python fallback; check licences |
| CAP-31 soft entity linking via embeddings | EXPERIMENT | proposal-only |
| CAP-32 LLM OpenIE | DEFER | deterministic first; local model optional |
| CAP-57 agent memory (index/delete/retrieve) | EXPERIMENT | compare with Graphiti/Mem0 in other batch |
| CAP-59 MCP | REJECT upstream server | EOIP MCP read-only stays |
| CAP-46 ACL-masked propagation | BUILD | INV-02 |
| CAP-78 benchmark harness | BUILD | shared with other C08 dives |

## 14. Tests, POC, acceptance

1. Check out main d5c8329 in an isolated env, run the README local vLLM example with an 8B model on 500 EOIP-shaped passages; record OpenIE failure rate, minutes, tokens.
2. Controlled retrieval comparison with a fixed embedder: BM25, dense, RRF, +reranker, HippoRAG 2, BL-16, BL-16 + PPR; report recall@5/10 and tokens; seeds fixed.
3. Synonym threshold sweep 0.7/0.8/0.9 with false-merge audit.
4. ACL canary test (INV-02) and delete test (provenance-driven; 0 residual facts).
5. Acceptance: adopt PPR step only if it improves recall on multi-hop sets by >=3 points without hurting single-hop by >1 point (router or fusion allowed) and zero canary leaks.

## 15. Risks and open questions

Author-run indexing figures on GPU/API setups do not transfer to one-node CPU; independent benchmarks use different readers and metrics so cross-table comparison is unsafe; alpha code may change; recognition-memory LLM call adds latency and egress surface at query time (route through BL-45); PPR scale in pure Python unknown (U-06); synonym threshold sensitivity; benefits on enterprise ticket/log text (short, templated, non-encyclopaedic) unproven since all benchmarks are Wikipedia, novel or medical text.

## Appendix A. Research-dimension coverage

| Dimension | Sections | Summary |
|---|---|---|
| D1 Identity | 1 | OSU NLP, MIT, v2 alpha |
| D2 Problem | 2 | Associative multi-hop memory |
| D3 Architecture | 4, 5 | Library; igraph + stores |
| D4 Storage | 5.7 | parquet/vector DB + pickle |
| D5 Schema | 5.1 | Entity/passage nodes; predicate in fact store |
| D6 Query pipeline | 5.4 | Fact linking, filter, PPR |
| D7 Reasoning | 5.4 | Propagation only, no inference |
| D8 Transactions/scale | 5.7 | None; RAM bound |
| D9 Ingestion | 5.2 | Text chunks, cached OpenIE |
| D10 Identity/evidence | 5.3, 5.9 | Soft synonyms; passage provenance |
| D11 Time | N/A | None |
| D12 Graph ML | 5.4 | PPR only |
| D13 Retrieval/agents | 5.4, 3 | MCP alpha |
| D14 NL query | N/A | Not text-to-query |
| D15 Governance | N/A | None |
| D16 UX | N/A | Library |
| D17 DevEx | 1, 3 | Python API, examples |
| D18 Security | 5.8 | None |
| D19 Multi-tenancy | 10 | Directory per index |
| D20 Economics | 7 | Token/time evidence |
| D21 Commercial | 10 | MIT |
| D22 Interop | 3 | Qdrant/Chroma/Milvus |
| D23 IP | N/A | Not verified |
| D24 Research quality | 7, 15 | Author + independent |

## Appendix B. Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-56 | native (PPR variant) | 04, 11, 12 | BL-16 Implemented | EXPERIMENT | P1 |
| CAP-19 | native | 11, 12 | BL-16/43 | EXPERIMENT | P1 |
| CAP-62 | native | 06 | BL-43 Implemented | REUSE | P2 |
| CAP-31 | partial (soft) | 05 | BL-36 Absent | EXPERIMENT | P2 |
| CAP-32 | native | 03 | BL-26 | DEFER | P3 |
| CAP-57 | native | 07 | none | EXPERIMENT | P2 |
| CAP-53 | plugin | 03 | BL-14 Partial | INTEGRATE | P1 |
| CAP-59 | partial | 09 | BL-47 Implemented | REJECT upstream | P3 |
| CAP-46 | absent | 09 | BL-18 Absent | BUILD | P0 |
| CAP-67 | native | 07 | BL-24 | BUILD | P1 |
| CAP-78 | absent | n/a | none | BUILD | P1 |

## Appendix C. Evidence records

| CLAIM-ID | product/version/date | claim | class | source | pub / access | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-hipporag-01 | repo, main d5c8329 | MIT; not archived; ~4.1k stars; last push 2026-10-06; only release v1.0.0 (2025-02-27) | Officially documented | github.com/OSU-NLP-Group/HippoRAG (API, LICENSE) | 2026-10-18 | 0.95 | none |
| CLAIM-hipporag-02 | HippoRAG v1 / v2 | positioning: neurobiologically inspired retrieval; v2 as non-parametric continual learning | Peer-reviewed/preprint | arXiv 2405.14831; 2502.14802 | 2024-05-23; 2025-02-20 | 0.85 | none |
| CLAIM-hipporag-03 | main d5c8329 | OpenIE NER+triples; entity/chunk node ids by md5; fact/passage/synonym edges; per-chunk OpenIE cache | Observed in source | `src/hipporag/HippoRAG.py` (index, add_*_edges) | 2026-10-18 | 0.9 | none |
| CLAIM-hipporag-04 | main d5c8329 | retrieval: fact scoring, top-5 linking, LLM triple filter, seeds, PPR, dense fallback | Observed in source | `HippoRAG.py` retrieve, graph_search_with_fact_entities, `rerank.py` | 2026-10-18 | 0.9 | none |
| CLAIM-hipporag-05 | main d5c8329 | synonymy edges: topk 2047, threshold 0.8, new-node-only incremental kNN | Observed in source | `HippoRAG.py` add_synonymy_edges; `utils/config_utils.py` | 2026-10-18 | 0.9 | none |
| CLAIM-hipporag-06 | main d5c8329 | PPR damping 0.5 default, passage_node_weight 0.05, retrieval_top_k 200, prpack, undirected | Observed in source | `HippoRAG.py` run_ppr; `config_utils.py` | 2026-10-18 | 0.9 | v1 code default damping 0.1 |
| CLAIM-hipporag-07 | main d5c8329 | incremental index and delete with persisted OpenIE provenance; refuses legacy graphs | Observed in source | `HippoRAG.py` delete, index | 2026-10-18 | 0.8 | not executed |
| CLAIM-hipporag-08 | main d5c8329 | igraph pickle; parquet or Qdrant/Chroma/Milvus stores | Observed in source | `embedding_store.py`, `vector_stores/` | 2026-10-18 | 0.9 | none |
| CLAIM-hipporag-09 | main d5c8329 | no ACL/tenancy code (grep); MCP HTTP has no authentication; `--read_only` option | Observed in source / documented | README "MCP Server"; `src/hipporag` | 2026-10-18 | 0.85 | absence by grep |
| CLAIM-hipporag-10 | HippoRAG 2 paper | avg F1 59.8 vs 57.0 dense vs 49.6 GraphRAG; recall@5 78.2; indexing 99.5 min / 9.2M tokens vs GraphRAG ~115.5M; ablations; QA 1.2 s/query, 9.9 GB | Vendor (author) claim | arXiv 2502.14802 https://arxiv.org/html/2502.14802 | 2025-02-20 / 2026-10-18 | 0.65 | independent tables CLAIM-11, -12 are less favourable on some sets |
| CLAIM-hipporag-11 | GraphRAG-Bench | HippoRAG2 tokens/query 1,008/1,020 vs vanilla 879/954; v1 7,208; reasoning ACC 53.38 vs 42.93; fact ACC 60.14 vs 60.92 (novel), 66.28 vs 64.73 (medical); summarisation 64.10 vs MS-GraphRAG 64.40 | Independent benchmark | arXiv 2506.05690 https://arxiv.org/abs/2506.05690 | 2025-06-06 / 2026-10-18 | 0.8 | none |
| CLAIM-hipporag-12 | Han et al. | F1 HotpotQA 63.01 vs RAG 60.04; MultiHop-RAG 70.27 vs 67.02; NQ 61.03 vs 64.78; NovelQA 56.54 vs 57.12 | Independent benchmark | arXiv 2502.11371 https://arxiv.org/abs/2502.11371 | 2025-02-17 / 2026-10-18 | 0.8 | none |
| CLAIM-hipporag-13 | HippoRAG v1 paper | up to 20% over prior RAG; 10-30x cheaper, 6-13x faster than IRCoT | Vendor (author) claim | arXiv 2405.14831 https://arxiv.org/abs/2405.14831 | 2024-05-23 | 0.6 | none |
| CLAIM-hipporag-14 | main d5c8329 | local deployment via vLLM / OpenAI-compatible endpoints; example uses Llama-3.3-70B on 2 GPUs | Officially documented | README "Local Deployment (vLLM)" | 2026-10-18 | 0.9 | none |
| CLAIM-hipporag-15 | main | package version 2.0.0a5 (alpha); tag v1.0.0 holds v1 code | Observed in source | `setup.py`, `pyproject.toml`, tag listing | 2026-10-18 | 0.95 | none |

## Appendix D. Assumptions

- Brief access date 2026-10-18 recorded; fetches ran 2026-10-26.
- HippoRAG 2 is pinned to commit d5c8329 (main) because no v2 tag exists.
- Query-time latency, RAM per million nodes and CPU-only behaviour not measured (NOT PUBLICLY VERIFIED beyond the authors' GPU numbers).
- Venue statements (NeurIPS 2024, ICML 2025) come from arXiv comment fields only.
- Dependency and model licences, security advisories not checked (UNVERIFIED).
