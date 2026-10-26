| Field | Value |
|---|---|
| Registry ID | T-C09-llama-cpp |
| Tier | B (CPU-first inference engine under Ollama; direct candidate for EOIP's CPU reference runtime) |
| Versions examined | llama.cpp build b11889 (tag created 2026-10-25); llama-cpp-python 0.3.36 (2026-10-01) |
| Verified on | 2026-10-26 |
| Worker | V22 |

## 1. Identity, current status, tier, sources

llama.cpp, repo `ggml-org/llama.cpp`, plain C/C++ inference with ggml; maintained by the ggml-org organisation (maintainers merge to `master`, collaborators invited by contribution) [CLAIM-llcpp-01]. Licence **MIT**, "Copyright (c) 2023-2026 The ggml authors" [CLAIM-llcpp-02]. Release model: rolling builds `bNNNN` (latest tag b11889 dated 2026-10-25), not semantic versions [CLAIM-llcpp-03]. Python bindings `llama-cpp-python` 0.3.36, MIT, separate project [CLAIM-llcpp-04]. Ollama (`C09-ollama.md`) embeds a llama.cpp-family engine; this file covers the engine used directly. Status: active, extremely fast cadence.

## 2. Problem, workloads, workflows

Problem: run quantised LLMs and embedding/reranker models on commodity CPUs and mixed hardware without Python or CUDA dependencies. EOIP workloads: embedding (BL-14 replacement), reranking, small-model extraction, NL-assist (BL-12), under ADR-H15 CPU-first. Workflow: build or fetch a pinned `llama-server` binary, supply GGUF files (provided by customer or converted), run with `--api-key`, point the EOIP provider at `/v1/embeddings`.

## 3. Feature inventory

| Feature | Status | Note |
|---|---|---|
| CPU backends: ARM NEON, AVX, AVX2, AVX512, AMX, RISC-V vector | present | no dependency C/C++ [CLAIM-llcpp-01] |
| GPU/other: CUDA, HIP, Metal, Vulkan, BLAS | optional | [CLAIM-llcpp-01] |
| Quantisation 1.5 to 8-bit integer | present | [CLAIM-llcpp-01] |
| `llama-server` OpenAI-compatible chat/completions/responses, streaming, tools (`--jinja`) | present | [CLAIM-llcpp-05] |
| `/v1/embeddings` (pooling required, normalised) | present | [CLAIM-llcpp-05] |
| `/v1/rerank` (Jina-style and TEI-style bodies, `top_n`) | present | [CLAIM-llcpp-05] |
| Grammar (GBNF) and JSON-schema constrained output | present | [CLAIM-llcpp-05] |
| Parallel slots, continuous batching, slot cache save/restore | present | [CLAIM-llcpp-05] |
| API keys (`--api-key`, file), public `/health` | present | [CLAIM-llcpp-05] |
| Prometheus `/metrics` | present | [CLAIM-llcpp-05] |
| Router mode (multiple models, `--models-max` default 4) | present | [CLAIM-llcpp-05] |
| Multi-tenant isolation, per-key quotas, audit | absent | keys are flat, no scopes verified |

## 4. Architecture

```
 client --HTTP--> llama-server (HTTP layer, slots scheduler, continuous batching)
                    |-- model(s): GGUF loaded via mmap; quantised weights
                    |-- ggml compute graph --> CPU kernels (AVX2/AVX512/AMX/NEON) or GPU backend
                    `-- KV cache per slot (save/restore), grammar sampler, /metrics
```

## 5. Under-the-hood reconstruction

Model format GGUF (single file with tensors plus metadata); tensors are memory-mapped; a ggml compute graph is built per architecture and executed by backend kernels; per-slot KV cache supports concurrent sessions; sampler chain applies grammar/JSON-schema masks [CLAIM-llcpp-05]. Quantisation kernels are architecture-specific SIMD (hypothesis from README's instruction-set list). Not source-read at a pinned tag this run: file-level citations UNVERIFIED.

## 6. Requirements inferred

FR: embedding and rerank endpoints with fixed model id and dimension; deterministic normalisation. NFR: pinned build per EOIP release with checksum; flags `--api-key-file`, `--metrics`, `--parallel` documented; CPU thread affinity tuned; model files validated by hash before load.

## 7. Performance and resource model

No independent benchmark gathered; throughput depends on quantisation, thread count, memory bandwidth. Memory roughly model size plus KV cache (general knowledge, not measured). Failure modes: rerankers must fit in `--ubatch-size`, pooling-less models rejected by embeddings endpoint [CLAIM-llcpp-05]; rolling builds can break flags between tags (inference).

## 8. Strengths

Zero-dependency CPU path matches ADR-H15/H16: no CUDA to redistribute. Single binary with embeddings, rerank, JSON-schema output and metrics covers the local-model needs of EOIP with one runtime. Exceed: add per-tenant key mapping and egress-gateway registration (BL-45) in front.

## 9. Limitations

Operational: build-numbered releases, no stability promise; GGUF conversion of arbitrary models is manual; throughput on CPU is far below GPU serving. Security: flat API keys, no TLS discussion in the page read (UNVERIFIED), `/slots` exposes state unless disabled. Friction: model-specific chat templates (`--jinja`). Licence: MIT engine, but model weights carry their own licences.

## 10. Deployment, licensing, viability

MIT, redistributable as a binary with notice. CPU-only builds fit offline bundles; GPU backends optional and customer-provisioned. One-node friendly. No legal trigger for the engine; model licences tracked in `C09-local-embeddings.md`.

## 11. Competitive delta vs EOIP baseline

EOIP currently has an Ollama provider and a sentence-transformers provider (`models/embeddings.py`) while the hashing embedder is default (BL-14, Partial). llama.cpp offers a smaller dependency alternative to torch for CPU embeddings, and a reranker endpoint EOIP lacks.

## 12. Cards

STR-llcpp-01 | llama.cpp | dependency-free CPU serving with embeddings, rerank, JSON-schema output, metrics | CLAIM-llcpp-01,05 | air-gapped installs with no CUDA or Python stack | integrate | `LlamaCppProvider` implementing `EmbeddingProvider`, health via `/health`, key from secret store | 10k-chunk embed run on CPU reference box meets the CRA-025 budget; no outbound packets (egress test).
INV-llcpp-01 | llama.cpp b11889 | rolling builds, flat keys (proven from docs) | root cause governance/maturity, proven | pinning plus a thin authenticating proxy; worse if customers need hot upgrades | options: (1) Ollama as-is; (2) pinned llama-server behind EOIP proxy; (3) embedded library binding | select 2 | POC: upgrade across 5 builds with golden embeddings cosine >= pre-set threshold | defensibility: conformance suite | decision ADOPT (integrate).

## 13. Per-capability decisions

| Capability | Decision |
|---|---|
| CAP-61 local model serving (CPU reference) | INTEGRATE (llama-server, alongside Ollama) |
| CAP-53 embeddings | INTEGRATE |
| Reranking (CAP-55) | EXPERIMENT |
| Python binding as dependency | DEFER (C extension build burden) |

## 14. Tests

Embedding parity vs sentence-transformers on a 500-pair set; rerank NDCG on EOIP gold set; flag audit (api-key required, `/slots` off); soak test of concurrent slots; checksum-verified model load offline.

## 15. Risks and open questions

Build-tag compatibility; GGUF availability and licence for chosen embedding models; TLS termination; security advisories not reviewed this run.

## Appendix A. Research-dimension coverage

| Dimension | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | MIT, ggml-org |
| D2 | 2 | CPU-first local inference |
| D3 | 4 | Server + ggml |
| D4 | 5 | GGUF mmap |
| D5-D7 | N/A | none |
| D8 | 3, 7 | Slots, no distribution |
| D9-D12 | N/A | none |
| D13 | 2, 3 | Embedding/rerank endpoints |
| D14 | N/A | structured output only |
| D15-D16 | N/A | none |
| D17 | 3 | OpenAI-compatible API |
| D18 | 9 | Flat keys |
| D19 | 3, 9 | Absent |
| D20 | 7 | No numbers |
| D21 | 10 | MIT |
| D22 | 8 | OpenAI-compatible, GGUF portable |
| D23 | N/A | none found |
| D24 | App. C | docs only, no benchmark |

## Appendix B. Capability mapping

| CAP-ID | This technology | CLAIM | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-61 | native | llcpp-01,05 | BL-57 Planned/Partial | INTEGRATE | P1 |
| CAP-53 | native (embeddings) | llcpp-05 | BL-14 Partial | INTEGRATE | P1 |
| CAP-50 | native | llcpp-01 | BL-45 default S0 | REUSE | P1 |
| CAP-75 | native (/metrics) | llcpp-05 | BL-49 | REUSE | P2 |

## Appendix C. Evidence records

| CLAIM-ID | product/version/date | claim | class | source | dates | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-llcpp-01 | llama.cpp README | CPU instruction sets, GPU backends, 1.5-8 bit quantisation, ggml-org governance | Officially documented | https://github.com/ggml-org/llama.cpp | undated / 2026-10-26 | 0.85 | none |
| CLAIM-llcpp-02 | LICENSE | MIT, 2023-2026 The ggml authors | Observed in source | https://raw.githubusercontent.com/ggml-org/llama.cpp/master/LICENSE | 2026-10-26 | 0.95 | none |
| CLAIM-llcpp-03 | tags page | latest tag b11889, 2026-10-25 | Officially documented | https://github.com/ggml-org/llama.cpp/tags | 2026-10-25 / 2026-10-26 | 0.9 | /releases/latest redirect showed v0.7.0 (a different tag stream) |
| CLAIM-llcpp-04 | llama-cpp-python 0.3.36 | MIT, 2026-10-01 | Officially documented | https://pypi.org/project/llama-cpp-python/ | 2026-10-01 / 2026-10-26 | 0.9 | none |
| CLAIM-llcpp-05 | server README (first 100k chars) | endpoints, rerank, grammar, slots, keys, metrics, router mode | Officially documented | https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md | undated / 2026-10-26 | 0.8 | final 26k chars unread |

## Appendix D. Assumptions

The "latest release" redirect resolved to an unrelated tag (v0.7.0); the `bNNNN` tags page was taken as authoritative.
