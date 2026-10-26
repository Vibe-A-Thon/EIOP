# C08 RAPTOR

| Field | Value |
|---|---|
| Registry ID | T-C08-raptor |
| Tier | B (tree-summarisation retrieval; a method, not a product) |
| Versions examined | arXiv:2401.18059 v1 (2024-01-31); `parthsarthi03/raptor` HEAD (2024-09-03) |
| Verified on | 2026-10-26 |
| Worker | V20 |

## 1. Identity, status, sources
RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval), Sarthi, Abdullah, Tuli, Khanna, Goldie, Manning; arXiv preprint cs.CL, v1 only [CLAIM-rap-01]. Reference implementation `parthsarthi03/raptor`, MIT licence (LICENSE.txt), last commit 2024-09-03 (research code, **dormant**) [CLAIM-rap-02]. The method is re-implemented inside other stacks (not verified here; LlamaIndex and Haystack community packs are believed to exist, UNVERIFIED). Not a graph: a hierarchy of cluster summaries.

## 2. Problem and workloads
Standard chunk retrieval misses questions needing whole-document themes. RAPTOR clusters chunks, summarises clusters with an LLM, and repeats upward to build a tree; retrieval searches across levels. Targets long single documents, narrative QA, multi-step reasoning [CLAIM-rap-01].

## 3. Feature inventory
| Feature | Status |
|---|---|
| Recursive embed-cluster-summarise tree | present (paper, repo) |
| Retrieval modes: tree traversal, collapsed tree | present (paper; from memory, confidence 0.6) |
| Pluggable embedder/summariser/QA model | present in repo (from memory, 0.5) |
| Incremental update, deletion, ACL, tenancy, provenance to span | absent / not addressed |
| Server, API, persistence | absent (pickled tree, demo notebook) |

## 4. Architecture
```
chunks(100 tok) -> embed -> cluster (UMAP + GMM, soft) -> LLM summary per cluster -> new layer
repeat until single cluster/limit -> tree; index all nodes
query -> embed -> (collapsed: top-k over all nodes by cosine | traversal: top-k per layer descending) -> LLM answer
```

## 5. Under-the-hood reconstruction
Clustering: dimensionality reduction (UMAP) then Gaussian mixture with soft assignment so a chunk can sit in several clusters; cluster count by BIC; very large clusters re-clustered (paper description, recalled; not re-verified this session, 0.6). Summaries are abstractive LLM outputs, themselves embedded as nodes. Collapsed-tree retrieval flattens all layers into one vector index and takes top-k under a token budget. Cost: one summarisation call per cluster per layer, roughly geometric in chunk count (hypothesis), so indexing cost is linear-ish in corpus size plus a re-run on any change.

## 6. Requirements inferred
Layered summary nodes with parent links; chunk-to-summary lineage; rebuild strategy on corpus change; token-budgeted multi-level retrieval.

## 7. Performance
Paper claims (authors' benchmarks): improves over traditional retrieval-augmented LMs; with GPT-4, "20% in absolute accuracy" gain on QuALITY [CLAIM-rap-01]. Single venue (preprint), long-document QA tasks, no enterprise heterogeneous data, no cost/latency table in the abstract. Independent reports of GraphRAG-style hierarchical methods underperforming vanilla RAG on many real tasks exist [CLAIM-rap-03]; applicability to EOIP unproven (Master Prompt 5.3).

## 8. Strengths
Cheap-ish thematic abstraction layer that needs no entity extraction; usable beside hybrid retrieval; summaries can answer broad questions. Matched by EOIP derived "summary nodes" with lineage.

## 9. Limitations
Algorithmic: summaries are lossy and can hallucinate; stale after edits; clustering is embedding-quality-bound. Operational: LLM cost at index time; full rebuild on change (no incremental algorithm in repo). Friction: research code, dormant. Permissions: a summary mixes content from sources with different ACLs, so it leaks by construction unless clusters are formed per ACL group (hypothesis; critical for BL-18).

## 10. Deployment and licensing
MIT; library-level; air-gap viable with local embedder and LLM (0.6). No legal trigger. One-node friendly (CPU clustering).

## 11. Delta vs EOIP baseline
EOIP has hybrid RRF (BL-15) and deterministic graph-first retrieval (BL-16), no hierarchical summaries and no evaluation harness against strong baselines. ACL-aware summarisation is missing everywhere (BL-18 Absent).

## 12. Cards
| ID | Card |
|---|---|
| STR-raptor-01 | Multi-level summary nodes searched together with leaves; CLAIM-rap-01; value: broad "what is this about" questions at low graph cost; **match** as optional derived layer; design: summary node per (ACL-group, cluster) with `derived_from` lineage and invalidation on source change; acceptance: gain over hybrid baseline on thematic questions, zero cross-ACL leakage test |
| INV-raptor-01 | Rebuild cost and ACL-mixing summaries (hypothesis for ACL; proven for no-incremental in repo). Options: (1) use library as-is [rejected], (2) per-ACL-group incremental re-summarisation of dirty clusters (selected), (3) differentiated: summary nodes carrying evidence spans and expiry. POC: 10k-chunk corpus, edit 1%, measure LLM calls vs full rebuild; success: <10% calls. Falsifier: no gain vs hybrid. Decision **EXPERIMENT**. No seed hypothesis in 10.5 names RAPTOR (the GraphRAG-cost one is partly related and supported). |

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-56 hierarchical/global summaries | EXPERIMENT (derived layer, ACL-grouped) |
| CAP-55 hybrid baseline | REUSE BL-15 as control |
| Reference implementation | REJECT as dependency (dormant) |

## 14. Tests
Benchmark on EOIP-like corpus: BM25, dense, hybrid, hybrid+RAPTOR; metrics faithfulness, recall, indexing LLM calls, leakage canary documents per ACL.

## 15. Risks and questions
Do gains survive modern long-context local models? Summary drift over time; how to expire summaries.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | method, MIT repo dormant |
| D2 | 2 | thematic retrieval |
| D3 | 4 | pipeline |
| D4-D5 | 5 | tree, no schema |
| D6 | 5 | cosine over nodes |
| D7-D8,D11-D12 | N/A | not applicable |
| D9 | 9 | batch only |
| D10 | 9 | no lineage |
| D13 | 3,5,7 | multi-level retrieval |
| D14 | N/A | none |
| D15-D17 | N/A | research code |
| D18-D19 | 9 | ACL leakage |
| D20 | 7 | index LLM cost |
| D21 | 10 | MIT |
| D22 | 10 | portable summaries |
| D23 | N/A | none verified |
| D24 | 7 | preprint, author benchmarks |

## Appendix B. Capability mapping
| CAP | This tech | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-56 | partial (hierarchical, non-graph) | rap-01 | BL-16 | EXPERIMENT | P2 |
| CAP-53 | plugin | rap-02 | BL-14 Partial | REUSE own | P2 |
| CAP-46 | absent | rap-02 | BL-18 Absent | BUILD | P0 |

## Appendix C. Evidence records
| CLAIM | Product/version/date | Claim | Class | Source | Dates/conf | Contradiction |
|---|---|---|---|---|---|---|
| rap-01 | arXiv:2401.18059 v1, 2024-01-31 | recursive embed-cluster-summarise tree; with GPT-4 +20% absolute on QuALITY (authors' claim) | Peer-reviewed-preprint | arxiv.org/abs/2401.18059 | acc 2026-10-26; 0.85 | rap-03 |
| rap-02 | repo HEAD 2024-09-03 | MIT, last commit 2024-09-03 | Officially documented / git log | github.com/parthsarthi03/raptor | acc 2026-10-26; 0.9 | none |
| rap-03 | arXiv:2506.05690 v3 | GraphRAG "frequently underperforms vanilla RAG on many real-world tasks"; GraphRAG-Bench | Independent benchmark (abstract) | arxiv.org/abs/2506.05690 | 2025-06-06 rev 2026-02-22; 0.7 | rap-01 |

## Appendix D. Assumptions
Algorithm details recalled from the paper and marked 0.5-0.6; PDF not re-read this session.
