| Field | Value |
|---|---|
| Registry ID | T-C09-hf-tei |
| Tier | B (purpose-built embedding/reranker server; candidate for EOIP's embedding service) |
| Versions examined | TEI v1.9.4 (2026-09-15); LICENSE history: v0.1.0 (2023-10-13) and commit 3c385a4 (2024-04-08) |
| Verified on | 2026-10-26 |
| Worker | V22 |

## 1. Identity, current status, tier, sources

Hugging Face Text Embeddings Inference (repo `huggingface/text-embeddings-inference`), a Rust server for embedding, sequence-classification and reranker models. Latest release v1.9.4, 2026-09-15 [CLAIM-tei-01]. **Licence history (verified from the repository):** the LICENSE at v0.1.0 (commit b26fd46, 2023-10-13) was the *Hugging Face Optimized Inference License 1.0 (HFOILv1.0)*; commit 3c385a4 "Change license to Apache 2.0 (#231)" on 2024-04-08 replaced it; the current file is Apache-2.0 [CLAIM-tei-02]. The text of HFOILv1.0 was not read beyond its preamble, so its exact restrictions (commonly described as limiting offering the software as a hosted service) are UNVERIFIED. Trap: third-party directories still list "HFOIL" and Homebrew lists 1.7.2, both stale [CLAIM-tei-03]. Releases between 2023-10 and 2024-04 are the only HFOIL-licensed ones; anything pinned at or after that commit is Apache-2.0 (reasoned from the commit history, with the exact first Apache tag not identified). Status: active, 1.x.

## 2. Problem, workloads, workflows

Problem: efficient production serving of embedding and reranking models without the overhead of general LLM runtimes. EOIP workflow: ingestion pipeline posts batches of chunks to `/embed`, retrieval posts queries and candidate texts to `/rerank`, all inside the perimeter; weights are loaded from a local directory (offline mode must be verified, see tests).

## 3. Feature inventory

| Feature | Status | Note |
|---|---|---|
| Embedding models: Nomic (v1, v1.5, v2-moe), BERT, XLM-RoBERTa, JinaBERT, GTE, Qwen2/Qwen3, MPNet, ModernBERT, Gemma3, Mistral | present | [CLAIM-tei-01] |
| Rerankers/classification: BGE rerankers, gte-multilingual-reranker, gte-reranker-modernbert, XLM-R | present | [CLAIM-tei-01] |
| Token-based dynamic batching, Flash Attention, Candle, cuBLASLt | present | [CLAIM-tei-01] |
| CPU images x86_64 and aarch64 (`cpu-1.9`, `cpu-arm64-1.9`) | present | [CLAIM-tei-01]; tags quoted from README for 1.9 line |
| ONNX backend for x86 CPU (build `-F ort`), safetensors + ONNX loading | present | [CLAIM-tei-01] |
| GPU images (Turing experimental, Ampere, Ada, Hopper, Blackwell experimental), ROCm MI200/MI300, Metal | optional | [CLAIM-tei-01] |
| Prometheus metrics, OpenTelemetry tracing, gRPC (`-grpc` tag) | present | [CLAIM-tei-01] |
| No graph compilation step, small images | present | [CLAIM-tei-01] |
| ColBERT multi-vector / sparse outputs | unknown | BGE-M3 sparse/multi-vector support not verified |
| Authentication, tenancy | unknown / absent | API key option not verified |

## 4. Architecture

```
 client --HTTP/gRPC--> router (Rust: tokenization, queue, token-budget dynamic batching)
                         --> backend: Candle | ONNX Runtime (ort) | (GPU: flash attn, cuBLASLt)
                         --> pooling/normalisation --> vectors or rerank scores
 model dir/hub download; /metrics, OTel
```

## 5. Under-the-hood reconstruction

Router tokenizes requests, queues them and forms batches under a token budget; a backend executes the model graph (hand-written Candle models, or ONNX through `ort` for CPU) and returns pooled outputs [CLAIM-tei-01]. Source paths at a pinned tag (`router/`, `backends/`) were not read: UNVERIFIED. Stateless: no storage, no index.

## 6. Requirements inferred

FR: batch embedding with stable dimension per model id; rerank endpoint; truncate policy explicit. NFR: pinned image digest; offline weight directory; health and readiness; `/metrics` scraped into EOIP observability (BL-49); request size limits; model hash recorded in embedding lineage so vectors can be invalidated on model change.

## 7. Performance and resource model

No independent benchmark gathered; Hugging Face's own performance statements were not collected. Scaling: CPU throughput bounded by cores and ONNX/Candle kernels; GPU much faster but optional. Failure modes: experimental GPU tags (Turing, Blackwell) with precision caveats (Flash Attention off by default on Turing) [CLAIM-tei-01]; unsupported architecture errors at startup.

## 8. Strengths

Smallest purpose-built path to production-grade embedding+rerank serving with both CPU and GPU images, metrics and tracing out of the box; Apache-2.0 since April 2024. Match by integrating, not rebuilding.

## 9. Limitations

Licensing history (HFOIL era) is a diligence item for anyone pinned to old tags; GPU images likely bundle NVIDIA runtime components (hypothesis) which EOIP does not redistribute (ADR-H16); model support is a fixed list per release; auth and multi-tenancy not documented in sources read; Hugging Face hub dependence by default (offline path must be proven). Homebrew and directory staleness causes confusion.

## 10. Deployment, licensing, viability

Apache-2.0 (current): redistributable with notice; CPU image ARM and x86 fits CPU-only policy. Air-gap: viable if weights are pre-staged (to verify). One-node: yes, small image. Legal triggers: confirm no residual HFOIL files in any pinned tag; confirm licences of model weights loaded (see `C09-local-embeddings.md`).

## 11. Competitive delta vs EOIP baseline

EOIP has Ollama and sentence-transformers providers (`models/embeddings.py`) but default hashing embedder (BL-14); no reranker (no BL; absent). TEI would supply batched CPU embeddings and reranking behind one HTTP contract; Ollama remains default runtime (`C09-ollama.md`). llama.cpp (`C09-llama-cpp.md`) is the dependency-free alternative.

## 12. Cards

STR-tei-01 | TEI | embedding+rerank server with CPU ONNX path, metrics, tracing | CLAIM-tei-01 | upgrade from BL-14 with a single sidecar | integrate | `TeiEmbeddingProvider`/`TeiReranker` implementing `EmbeddingProvider`, optional compose profile | 10k-chunk batch on CPU image; vectors match sentence-transformers reference within tolerance; no outbound traffic.
INV-tei-01 | TEI pre-2024-04 tags | HFOIL licence era (proven) vs Apache-2.0 now | root cause licensing, proven | pin >= post-April-2024 tag and verify LICENSE in image | options: (1) pin tag; (2) mirror source + SBOM; (3) alternative llama.cpp | select 1 with SBOM | POC: scan pinned image for LICENSE content | defensibility: low | decision ADOPT.

## 13. Per-capability decisions

| Capability | Decision |
|---|---|
| CAP-53 embeddings serving | INTEGRATE (optional profile) |
| Reranking (CAP-55) | INTEGRATE / EXPERIMENT |
| CAP-79 SBOM/licence scan of image | BUILD |
| Replace Ollama default | REJECT (keep Ollama default; TEI optional) |

## 14. Tests

Offline start with local weights and no hub access; embedding parity; rerank quality on EOIP gold set; image licence scan; load test at 1/8/32 concurrent; metrics scrape; confirm egress S0 respected.

## 15. Risks and open questions

Exact HFOIL terms; first Apache-2.0 tag; auth options; whether BGE-M3 sparse/multi-vector is served; bundled third-party licences in images.

## Appendix A. Research-dimension coverage

| Dimension | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | Licence history verified |
| D2 | 2 | Embedding/rerank serving |
| D3 | 4 | Router + backend |
| D4 | N/A | Stateless |
| D5-D7 | N/A | none |
| D8 | 5, 7 | Batching only |
| D9-D12 | N/A | none |
| D13 | 2, 3 | Retrieval components |
| D14-D16 | N/A | none |
| D17 | 3 | HTTP/gRPC |
| D18 | 9 | Auth unknown |
| D19 | 3 | Absent |
| D20 | 7 | No numbers |
| D21 | 1, 10 | Apache-2.0 |
| D22 | 8 | Model portability |
| D23 | N/A | none found |
| D24 | App. C | README + repo history only |

## Appendix B. Capability mapping

| CAP-ID | This technology | CLAIM | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-53 | native | tei-01 | BL-14 Partial | INTEGRATE | P1 |
| CAP-55 | partial (rerank) | tei-01 | BL-15 Implemented | EXPERIMENT | P2 |
| CAP-61 | native | tei-01 | BL-57 | INTEGRATE | P2 |
| CAP-75 | native | tei-01 | BL-49 | REUSE | P3 |
| CAP-79 | n/a | tei-02 | none | BUILD | P2 |

## Appendix C. Evidence records

| CLAIM-ID | product/version/date | claim | class | source | dates | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-tei-01 | TEI README (1.9 line), release v1.9.4 | model list, CPU/GPU tags, ONNX backend, batching, metrics, gRPC; v1.9.4 on 2026-09-15 | Officially documented | https://github.com/huggingface/text-embeddings-inference ; /releases/tag/v1.9.4 | 2026-09-15 / 2026-10-26 | 0.8 | none |
| CLAIM-tei-02 | LICENSE history | HFOILv1.0 at v0.1.0 (2023-10-13, b26fd46); Apache-2.0 from 3c385a4 (2024-04-08) | Observed in source (raw LICENSE at commit; commit list) | https://raw.githubusercontent.com/huggingface/text-embeddings-inference/b26fd46/LICENSE ; https://github.com/huggingface/text-embeddings-inference/commits/main/LICENSE | 2023-10-13, 2024-04-08 / 2026-10-26 | 0.9 | third-party listings say HFOIL |
| CLAIM-tei-03 | third-party listings | stale: HFOIL tag; Homebrew 1.7.2 | Third-party report | https://formulae.brew.sh/formula/text-embeddings-inference | undated / 2026-10-26 | 0.6 | superseded by CLAIM-tei-01/02 |

## Appendix D. Assumptions

Registry "HF TEI" = Hugging Face Text Embeddings Inference, not Text Generation Inference. HFOIL restrictions not analysed; legal review needed only for old tags.
