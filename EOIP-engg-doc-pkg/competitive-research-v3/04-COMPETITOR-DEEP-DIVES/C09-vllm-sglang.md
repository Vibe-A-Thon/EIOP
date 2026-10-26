| Field | Value |
|---|---|
| Registry ID | T-C09-vllm-sglang |
| Tier | B (GPU serving references; optional customer-provisioned components under ADR-H15/H16/H17) |
| Versions examined | vLLM 0.32.0 (2026-10-18); SGLang 0.5.22 (2026-10-16) |
| Verified on | 2026-10-26 |
| Worker | V22 |

## 1. Identity, current status, tier, sources

| Item | vLLM | SGLang |
|---|---|---|
| Repo | `vllm-project/vllm` | `sgl-project/sglang` |
| Origin / governance | UC Berkeley Sky Computing Lab origin; now community of academic and company contributors, 2000+ contributors [CLAIM-vsg-01]. PyTorch Foundation hosting: UNVERIFIED | Hosted by LMSYS, "a non-profit open-source organization"; Linux Foundation affiliation not stated [CLAIM-vsg-03] |
| Licence | **Apache-2.0** (LICENSE file header read) [CLAIM-vsg-02] | **Apache-2.0** (README badge; PyPI) [CLAIM-vsg-03] |
| Latest | 0.32.0, 2026-10-18 [CLAIM-vsg-02] | 0.5.22, 2026-10-16 [CLAIM-vsg-04] |
| Status | active, 0.x | active, 0.x |

Both are open-source LLM serving engines focused on throughput under concurrency. Neither is registry-ambiguous; do not confuse "SGLang" (LMSYS) with the unrelated SGL kernels subproject name.

## 2. Problem, workloads, workflows

Problem: serve many concurrent LLM requests efficiently on GPU clusters. EOIP relevance: a large customer with GPUs may want to host a bigger model for extraction/summarisation (CRA-026) and point EOIP at it. Workflow: customer deploys vLLM/SGLang on their own GPU hosts, exposes an OpenAI-compatible endpoint inside the perimeter, registers it as an egress-gateway endpoint of class "customer-local" (BL-45), EOIP calls it like any provider.

## 3. Feature inventory

| Feature | vLLM | SGLang |
|---|---|---|
| OpenAI-compatible server, streaming | present [CLAIM-vsg-01] | likely present; not verified |
| PagedAttention, continuous batching, chunked prefill, prefix caching | present [CLAIM-vsg-01] | prefix-cache design (RadixAttention) widely described; README read did not name it: UNVERIFIED |
| Quantisation (FP8, INT8, INT4, GPTQ/AWQ) | present [CLAIM-vsg-01] | unknown |
| Speculative decoding, multi-LoRA, parallelism | present [CLAIM-vsg-01] | unknown |
| Structured output | xgrammar or guidance [CLAIM-vsg-01] | credits Guidance, Outlines, LMQL as influences [CLAIM-vsg-03] |
| Embedding/pooling models (E5-Mistral, GTE, ColBERT listed) | present [CLAIM-vsg-01] | unknown |
| CPU | x86/ARM/PowerPC listed [CLAIM-vsg-01] | Intel Xeon CPUs listed [CLAIM-vsg-03] |
| Hardware breadth | NVIDIA, AMD, plugins (Apple) | NVIDIA, AMD MI3xx, Google TPU, Intel Arc/Xeon, Apple Metal/MLX, Huawei Ascend, Moore Threads [CLAIM-vsg-03] |
| Tenancy, per-tenant quota, ACL | absent (auth/key features not verified) | absent |

## 4. Architecture

```
 client --OpenAI API--> API server --> scheduler (continuous batching, prefix/KV cache blocks)
                                          --> model runner(s) (tensor/pipeline parallel) --> GPU kernels
 metrics/logging; optional LoRA adapters; structured-output grammar backend
```

## 5. Under-the-hood reconstruction

vLLM: paged KV-cache blocks allocated like virtual memory pages, scheduler admits requests each step (continuous batching), prefix caching reuses KV blocks for shared prompts [CLAIM-vsg-01]. SGLang: scheduler plus a radix-tree prefix cache is the publicly described design (general knowledge, not confirmed in sources read this run: hypothesis). Source-level citations at pinned tags were not collected: UNVERIFIED.

## 6. Requirements inferred

For an EOIP-facing integration: a provider adapter that sends only egress-approved payloads; health and model-list probe; timeouts; per-tenant concurrency caps imposed by EOIP, because the engines have none verified; capability flags (embeddings, structured output) discovered, not assumed.

## 7. Performance and resource model

No benchmarks gathered; vendor claims of throughput gains are workload and hardware specific and are not quoted. Failure modes: GPU out-of-memory at large context, cold start loading weights, tight coupling to CUDA/driver versions (inference). Single-node CPU use is possible but not the design centre.

## 8. Strengths

Highest-throughput open serving for concurrent agent workloads; broad hardware support (SGLang); embeddings and structured output in the same server. Match: nothing to build, integrate. Exceed: EOIP adds tenant-fair admission control and egress manifests in front.

## 9. Limitations

Operational: GPU drivers, large images, fast-moving 0.x APIs. Licensing: engines are Apache-2.0, but the Docker/wheel distributions bundle NVIDIA CUDA/PyTorch components (not verified here) whose redistribution EOIP has already declined (ADR-H16), so EOIP must not package them. Model weights have own licences. User friction: GPU sizing. Security: no verified multi-tenant isolation.

## 10. Deployment, licensing, viability

Apache-2.0 with patent grant: redistribution-safe in principle, but per ADR-H15/H16 EOIP distributes CPU-only builds; vLLM/SGLang are therefore documented as optional customer-provisioned endpoints, never shipped, never required. Air-gap viable if customer mirrors images and weights. Not one-node-first.

## 11. Competitive delta vs EOIP baseline

EOIP has no GPU serving and by policy will not (BL-57 CPU-first). Delta is a deployment pattern, not a feature gap. Cross-ref `C09-ollama.md` (default runtime), `C09-llama-cpp.md` (CPU engine).

## 12. Cards

STR-vsg-01 | vLLM/SGLang | high-concurrency GPU serving with OpenAI API | CLAIM-vsg-01,03 | large tenants run bigger local models without egress | integrate | "OpenAI-compatible local endpoint" provider class in the egress gateway; no vendor code in repo | integration test with a mock OpenAI server plus one live run on customer GPU; manifest records every call.
INV-vsg-01 | vLLM 0.32.0 / SGLang 0.5.22 | CUDA-coupled distribution vs CPU-only distribution policy (hypothesis on bundle contents) | root cause deployment/licensing, hypothesis | documenting a customer-provisioned pattern avoids redistribution; worse if customers want one-click | options: (1) docs only; (2) example compose profile that pulls upstream image at customer site; (3) managed installer | select 2 | POC: profile starts upstream image from customer registry, EOIP health passes | defensibility: policy plus governance integration | decision ADOPT (docs + profile), EXPERIMENT for installer.

## 13. Per-capability decisions

| Capability | Decision |
|---|---|
| CAP-61 GPU serving | INTEGRATE as optional endpoint |
| Bundle vLLM/SGLang in EOIP images | REJECT (ADR-H16) |
| Embedding serving on GPU | DEFER (TEI or vLLM, customer choice) |

## 14. Tests

Provider contract test against both engines' OpenAI endpoints; confirm EOIP never sends data when kill switch on; concurrency fairness test with two tenants; version-matrix smoke test of pinned image digests supplied by customer.

## 15. Risks and open questions

CUDA bundle licensing (legal review); governance of vLLM (foundation hosting unverified); SGLang feature claims unverified; security advisories not reviewed.

## Appendix A. Research-dimension coverage

| Dimension | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | Apache-2.0, versions |
| D2 | 2 | GPU serving |
| D3 | 4 | Scheduler + runner |
| D4 | 5 | KV cache paging |
| D5-D7 | N/A | none |
| D8 | 5, 7 | Parallelism only |
| D9-D12 | N/A | none |
| D13 | 2, 3 | Endpoint provider |
| D14 | 3 | Structured output |
| D15-D16 | N/A | none |
| D17 | 3 | API |
| D18 | 9 | No tenancy |
| D19 | 3, 9 | Absent |
| D20 | 7 | No numbers |
| D21 | 10 | Apache-2.0 |
| D22 | 8 | OpenAI API portability |
| D23 | N/A | none found |
| D24 | App. C | Docs only |

## Appendix B. Capability mapping

| CAP-ID | This technology | CLAIM | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-61 | native | vsg-01,03 | BL-57 Planned | INTEGRATE | P2 |
| CAP-51 | absent | vsg-01 | BL-45 Implemented | REUSE | P1 |
| CAP-79 | partial | vsg-02 | none | DEFER | P3 |

## Appendix C. Evidence records

| CLAIM-ID | product/version/date | claim | class | source | dates | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-vsg-01 | vLLM docs | PagedAttention, continuous batching, quantisation, structured output (xgrammar/guidance), embedding models, CPUs, Berkeley origin | Officially documented | https://docs.vllm.ai/en/latest/ | undated / 2026-10-26 | 0.8 | none |
| CLAIM-vsg-02 | vLLM 0.32.0 | Apache-2.0 LICENSE; release 2026-10-18 | Observed + documented | https://raw.githubusercontent.com/vllm-project/vllm/main/LICENSE ; https://github.com/vllm-project/vllm/releases/latest | 2026-10-18 / 2026-10-26 | 0.9 | none |
| CLAIM-vsg-03 | SGLang README | LMSYS-hosted, Apache-2.0 badge, hardware list, Guidance/Outlines/LMQL credits | Officially documented | https://github.com/sgl-project/sglang | undated / 2026-10-26 | 0.8 | RadixAttention not in README |
| CLAIM-vsg-04 | SGLang 0.5.22 | released 2026-10-16, Apache | Officially documented | https://pypi.org/project/sglang/ ; https://github.com/sgl-project/sglang/releases/latest | 2026-10-16 / 2026-10-26 | 0.9 | none |

## Appendix D. Assumptions

CUDA bundling in upstream artefacts is assumed from general practice, not verified; flagged for legal review.
