| Field | Value |
|---|---|
| Registry ID | T-C09-local-embeddings |
| Tier | B (model families that replace the hashing embedder, BL-14; licence is the decisive axis) |
| Versions examined | models listed in section 1 (Hugging Face model cards); sentence-transformers 6.2.0 (2026-10-21); PyLate 1.6.0 (2026-06-11); RAGatouille 0.0.9.post2 (2025-05-19); FlagEmbedding 1.4.2 (2026-08-24) |
| Verified on | 2026-10-26 |
| Worker | V22 |

## 1. Identity, current status, tier, sources

Licence per model, as read from the model cards on the access date (cards can change; re-verify at pin time):

| Family / model | Params / dim / context | Licence | Redistribution verdict (record, not legal advice) |
|---|---|---|---|
| BGE-M3 (BAAI) | dim 1024, 8192 tokens, 100+ languages; dense + sparse + multi-vector | **MIT** [CLAIM-emb-01] | permissive |
| bge-reranker-v2-m3 | 0.6B, multilingual, built on bge-m3 | **Apache-2.0** [CLAIM-emb-02] | permissive |
| multilingual-e5-large-instruct (E5, intfloat) | dim 1024, 24 layers | **MIT** [CLAIM-emb-03] | permissive |
| gte-modernbert-base (GTE, Alibaba-NLP) | ~149M, dim 768, 8192 | **Apache-2.0** [CLAIM-emb-04] | permissive |
| nomic-embed-text-v2-moe (Nomic) | 475M total / 305M active, dim 768 (Matryoshka to 256), 512 ctx; weights, code and training data stated open | **Apache-2.0** [CLAIM-emb-05] | permissive |
| jina-embeddings-v2-base-en | ~137M, 8192 ctx | **Apache-2.0** [CLAIM-emb-06] | permissive |
| jina-embeddings-v3 | n/a | **CC-BY-NC-4.0** (page also says deprecated) [CLAIM-emb-07] | non-commercial: legal-review trigger, do not bundle |
| jina-embeddings-v5-text-small (0.6B) / nano (239M) | Qwen3-0.6B / EuroBERT-210M backbones | **CC-BY-NC-4.0** [CLAIM-emb-07] | non-commercial: do not bundle |
| jina-embeddings-v4 | Qwen2.5-VL-3B derived | card: initially cc-by-nc-4.0 "due to an error"; correct licence is **Qwen Research License** [CLAIM-emb-08] | terms not read: legal-review trigger |
| jina-colbert-v2 | ~0.6B, dim 128 (96/64 variants), 94 languages | **CC-BY-NC-4.0** [CLAIM-emb-09] | non-commercial: do not bundle |
| ColBERTv2 (colbert-ir/colbertv2.0) | ~110M | **MIT** [CLAIM-emb-10] | permissive |

Tooling: sentence-transformers 6.2.0 Apache-2.0 [CLAIM-emb-11]; PyLate 1.6.0 MIT (late-interaction training/serving library, Jun 2026) [CLAIM-emb-11]; RAGatouille 0.0.9.post2 Apache-2.0, last release 2025-05-19, i.e. stale [CLAIM-emb-11]; FlagEmbedding 1.4.2 (2026-08-24, licence not captured: UNVERIFIED). Trap resolved: Jina has both permissive (v2) and non-commercial (v3, v5, colbert-v2) models; "Jina" cannot be treated as one licence. Qwen3-Embedding and Gemma-based embedding models appear in TEI's supported list [CLAIM-emb-12] but their licences were not examined.

## 2. Problem, workloads, workflows

Problem: BL-14 default is a deterministic hashing embedder with no semantic generalisation. Workloads: chunk embedding for GraphRAG retrieval (BL-16), entity-name matching for identity candidates (BL-35), reranking evidence, ColBERT-style token-level matching for citation-span selection. Workflow: pick a model per deployment profile (small English vs multilingual), serve via TEI, llama.cpp, Ollama or ONNX, record model id and hash on every vector.

## 3. Feature inventory

| Capability | Models | Status |
|---|---|---|
| Dense embeddings | all above | present |
| Sparse lexical weights | BGE-M3 | present [CLAIM-emb-01] |
| Multi-vector (late interaction) | BGE-M3, ColBERTv2, jina-colbert-v2 | present; EOIP index support absent |
| Long context 8192 | BGE-M3, GTE-modernbert, jina-v2 | present |
| Matryoshka truncation | Nomic v2, jina-colbert-v2 | present |
| Cross-encoder rerank | bge-reranker-v2-m3 | present |
| Instruction prefixes | E5-instruct | present (usage detail UNVERIFIED) |
| Quantised/ONNX/GGUF builds | varies | not verified per model |

## 4. Architecture

```
 text --> tokenizer --> encoder (BERT/ModernBERT/XLM-R/MoE) --> pooling (CLS/mean) --> L2 norm --> dense vector
 BGE-M3: same encoder -> dense + sparse head + per-token vectors (ColBERT-style)
 late interaction: score(q,d) = sum over q tokens of max over d tokens (dot)  [general description]
```

## 5. Under-the-hood reconstruction

Encoder transformers with pooling heads; MoE variant (Nomic v2) activates 305M of 475M parameters [CLAIM-emb-05]. Late-interaction stores one vector per token (storage 10-100x dense, hypothesis) and requires either a multi-vector index (PLAID-style, not examined) or reranking top-k candidates only. EOIP storage: `retrieval/vectors.py` and `graph/vector_graph.py` (pure-Python HNSW, BL-14) hold single vectors; multi-vector needs a new index or MaxSim rerank over fetched token vectors.

## 6. Requirements inferred

Embedding provider must expose `model_id`, `dim`, `max_tokens`, licence tag; vectors carry model id/hash for invalidation; permissive-licence allowlist in the build; non-commercial models blocked by policy unless tenant supplies them; language coverage matched to tenant data; unit tests for dimension mismatch.

## 7. Performance and resource model

No benchmark was run. Benchmark claims (MTEB etc.) were not collected; EOIP must run its own retrieval evaluation on tenant-like corpora (CAP-78). CPU cost scales with parameters and sequence length: 8192-context models are costly on CPU (inference). Failure modes: embedding drift on model swap (full re-index), truncation at 512 tokens (Nomic v2), prefix misuse for E5.

## 8. Strengths

Several strong permissively licensed options exist (BGE-M3 MIT covers dense, sparse, multi-vector in one model; GTE-modernbert Apache-2.0 with 8192 context; Nomic v2 with open data). Match: ship none, support all via provider; recommend defaults. Exceed: model-pinned lineage and automatic re-embedding plans.

## 9. Limitations

Licensing: Jina v3/v5/colbert-v2 non-commercial, v4 under Qwen Research License (verified from cards). Operational: re-embedding cost, multi-vector storage blow-up. Friction: prefix conventions, per-model tokenisers. Outdated: RAGatouille stale since 2025-05. Weights' redistribution inside EOIP bundles must respect ADR-H15 ("weights ship only where licence permits; otherwise customer-provided").

## 10. Deployment, licensing, viability

MIT/Apache-2.0 models are bundle-eligible subject to notice files; non-commercial ones are not. All run offline once weights are staged. Legal triggers: Jina v3/v4/v5/colbert-v2; any gated model; training-data licence questions for any model (not assessed).

## 11. Competitive delta vs EOIP baseline

BL-14 hashing default Partial; `models/embeddings.py` already defines `EmbeddingProvider` with Ollama and sentence-transformers implementations (not default). No multi-vector or sparse-neural retrieval (absent), RRF fusion exists (BL-15), so BGE-M3 sparse + dense maps well onto it.

## 12. Cards

STR-emb-01 | BGE-M3 | one MIT model for dense+sparse+multi-vector, 8192 ctx, 100+ languages | CLAIM-emb-01 | multilingual enterprise corpora, hybrid fusion with existing RRF | integrate | default `bge-m3` profile via TEI/llama.cpp; store dense + sparse; MaxSim rerank on top 50 | on EOIP gold queries recall@10 beats hashing baseline by pre-set margin, same ACL filters.
INV-emb-01 | Jina family | mixed licences (proven) | root cause licensing, proven | per-model licence allowlist enforced in CI and provider registry; worse if a customer insists on a Jina model (then customer-supplied weights) | options: (1) avoid Jina; (2) allowlist + customer-supplied; (3) negotiated commercial licence | select 2 | POC: CI fails when a non-allowlisted model id appears in a profile | defensibility: policy automation | decision ADOPT.
INV-emb-02 | BL-14 hashing embedder | no semantics (proven by design) | root cause algorithm | replace default with a real model while keeping hashing as zero-dependency fallback; worse on 1-core devices | options: (1) Ollama embed; (2) TEI/llama.cpp profile; (3) built-in ONNX | select 2 | POC: retrieval eval hashing vs BGE-M3 vs gte-modernbert on CPU | defensibility: evaluation data | decision ADOPT.

## 13. Per-capability decisions

| Capability | Decision |
|---|---|
| CAP-53 default embedding model | INTEGRATE (BGE-M3 or gte-modernbert; choose by eval) |
| Reranker | INTEGRATE bge-reranker-v2-m3 (EXPERIMENT quality) |
| Late-interaction index | EXPERIMENT (rerank-only first); DEFER full multi-vector index |
| Jina v3/v5/colbert-v2 | REJECT for bundling |
| Hashing embedder | REUSE as fallback |

## 14. Tests

Licence allowlist test in CI against model card metadata; retrieval evaluation (recall@k, nDCG) on EOIP gold corpora with tenant ACL filters; CPU latency per 1k chunks per model; re-embedding migration test with dual-write; truncation behaviour test.

## 15. Risks and open questions

Model-card licences change; training-data provenance not assessed; Qwen Research License terms unread; Qwen3-Embedding, Gemma-based and newer 2026 models unexamined; MTEB-type scores not collected.

## Appendix A. Research-dimension coverage

| Dimension | Sections | Summary |
|---|---|---|
| D1 | 1 | Licence table |
| D2 | 2 | Retrieval workloads |
| D3 | 4 | Encoder pipeline |
| D4 | 5 | Multi-vector storage cost |
| D5-D7 | N/A | none |
| D8 | N/A | none |
| D9-D12 | N/A | none |
| D13 | 2, 8 | Core |
| D14 | N/A | none |
| D15-D16 | N/A | none |
| D17 | 3 | sentence-transformers etc. |
| D18 | 6 | Weights supply chain |
| D19 | 6 | Per-tenant model choice |
| D20 | 7 | No numbers |
| D21 | 1, 10 | Licences |
| D22 | 8, 9 | Re-embedding lock-in |
| D23 | 10 | Training-data/IP not assessed |
| D24 | App. C | Model cards only; no benchmarks |

## Appendix B. Capability mapping

| CAP-ID | This technology | CLAIM | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-53 | native | emb-01,04,05 | BL-14 Partial | INTEGRATE | P1 |
| CAP-55 | native (sparse+dense) | emb-01 | BL-15 Implemented | INTEGRATE | P1 |
| CAP-77 | n/a | emb-07,08 | none | BUILD (allowlist) | P1 |
| CAP-78 | n/a | emb-01 | none verified | BUILD | P1 |
| CAP-31 | partial | emb-01 | BL-34/36 | EXPERIMENT | P3 |

## Appendix C. Evidence records

| CLAIM-ID | product/version/date | claim | class | source | dates | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-emb-01 | BAAI/bge-m3 | MIT; dim 1024; 8192; dense+sparse+multi-vector | Officially documented | https://huggingface.co/BAAI/bge-m3 | undated / 2026-10-26 | 0.85 | none |
| CLAIM-emb-02 | bge-reranker-v2-m3 | Apache-2.0; 0.6B | Officially documented | https://huggingface.co/BAAI/bge-reranker-v2-m3 | undated / 2026-10-26 | 0.85 | none |
| CLAIM-emb-03 | multilingual-e5-large-instruct | MIT; dim 1024 | Officially documented | https://huggingface.co/intfloat/multilingual-e5-large-instruct | undated / 2026-10-26 | 0.85 | none |
| CLAIM-emb-04 | gte-modernbert-base | Apache-2.0; ~149M; 768; 8192 | Officially documented | https://huggingface.co/Alibaba-NLP/gte-modernbert-base | undated / 2026-10-26 | 0.85 | none |
| CLAIM-emb-05 | nomic-embed-text-v2-moe | Apache-2.0; 475M/305M active; 768; 512 ctx; open data/code | Officially documented | https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe | undated / 2026-10-26 | 0.85 | none |
| CLAIM-emb-06 | jina-embeddings-v2-base-en | Apache-2.0; ~137M; 8192 | Officially documented | https://huggingface.co/jinaai/jina-embeddings-v2-base-en | undated / 2026-10-26 | 0.85 | none |
| CLAIM-emb-07 | jina v3, v5-text small/nano | CC-BY-NC-4.0 | Officially documented | https://jina.ai/models/jina-embeddings-v3/ ; https://jina.ai/models/jina-embeddings-v5-text-small/ | undated / 2026-10-26 | 0.8 (via search result snippets) | none |
| CLAIM-emb-08 | jina-embeddings-v4 | card says cc-by-nc was an error; correct licence Qwen Research License | Officially documented | https://huggingface.co/jinaai/jina-embeddings-v4 | undated / 2026-10-26 | 0.8 | earlier cc-by-nc tag |
| CLAIM-emb-09 | jina-colbert-v2 | cc-by-nc-4.0; ~0.6B; 128-dim | Officially documented | https://huggingface.co/jinaai/jina-colbert-v2 | undated / 2026-10-26 | 0.85 | none |
| CLAIM-emb-10 | colbertv2.0 | MIT; ~0.1B | Officially documented | https://huggingface.co/colbert-ir/colbertv2.0 | undated / 2026-10-26 | 0.8 | none |
| CLAIM-emb-11 | PyPI: sentence-transformers 6.2.0, pylate 1.6.0, ragatouille 0.0.9.post2 | licences and dates as stated | Officially documented | https://pypi.org/pypi/<pkg>/json | per package / 2026-10-26 | 0.85 | none |
| CLAIM-emb-12 | TEI README | supports Qwen3-Embedding, Gemma3, Nomic, GTE, E5, BGE rerankers | Officially documented | https://github.com/huggingface/text-embeddings-inference | undated / 2026-10-26 | 0.8 | none |

## Appendix D. Assumptions

Model-card licence fields are authoritative for this record; no weights were downloaded. Benchmark rankings deliberately omitted (no verified source gathered). ColBERT-style indexing (PLAID) not examined.
