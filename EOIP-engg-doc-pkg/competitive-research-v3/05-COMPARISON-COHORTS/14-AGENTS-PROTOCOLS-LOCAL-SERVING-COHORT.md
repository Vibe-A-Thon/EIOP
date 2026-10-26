# Cohort 14 - Agent protocols, frameworks and local CPU model serving

| Field | Value |
|---|---|
| Cohort ID | COH-14 |
| Workload class | Agent-to-tool and agent-to-agent protocols, agent orchestration frameworks, and self-hosted local inference (LLM, embedding, reranker) on a CPU-only, air-gapped node |
| Members | [mcp](../04-COMPETITOR-DEEP-DIVES/C09-mcp.md), [ollama](../04-COMPETITOR-DEEP-DIVES/C09-ollama.md), [a2a](../04-COMPETITOR-DEEP-DIVES/C09-a2a.md), [agent-frameworks](../04-COMPETITOR-DEEP-DIVES/C09-agent-frameworks.md) (AutoGen, Microsoft Agent Framework, PydanticAI, CrewAI, Claude Agent SDK), [dspy](../04-COMPETITOR-DEEP-DIVES/C09-dspy.md), [llama-cpp](../04-COMPETITOR-DEEP-DIVES/C09-llama-cpp.md), [vllm-sglang](../04-COMPETITOR-DEEP-DIVES/C09-vllm-sglang.md), [hf-tei](../04-COMPETITOR-DEEP-DIVES/C09-hf-tei.md), [onnx-runtime](../04-COMPETITOR-DEEP-DIVES/C09-onnx-runtime.md), [local-embeddings](../04-COMPETITOR-DEEP-DIVES/C09-local-embeddings.md), [guardrails](../04-COMPETITOR-DEEP-DIVES/C09-guardrails.md) (NeMo Guardrails, Llama Guard 4, Llama Prompt Guard 2) |
| Reference columns | HugeGraph, Neo4j, Neptune, EOIP @HEAD 896e06d (BL-IDs from `01-SYSTEM-BASELINE.md`, status from `01a-BASELINE-DELTA-HEAD.md`) |
| Date | 2026-10-26 |

## 1. Workload class and comparison basis

**Customer workloads.** (a) An agent or IDE client calling EOIP's tools over a standard protocol with a real per-user principal; (b) one EOIP agent calling another agent or a customer's agent estate; (c) orchestrating multi-step agent runs with approval gates; (d) serving LLMs, embeddings and rerankers locally on one CPU node, air-gapped, with model licences tracked; (e) defending the agent surface against prompt injection and tool abuse.

**Why comparable.** Every member is something EOIP would either expose (MCP server), consume (A2A, agent frameworks, DSPy) or run in-process (llama.cpp, vLLM/SGLang, TEI, ONNX Runtime, Ollama, embedding models, guardrails). None is a workload substitute for another; together they define the protocol security and local-serving boundary that cohort 06 (GraphRAG) and cohort 12 (security) depend on.

**Excluded.** vLLM and SGLang are GPU-centred by design (vsg-01) and, per ADR-H15/H16, are documented as optional customer-provisioned endpoints only, never bundled; they stay in the comparison as a reference row, not a candidate. Managed-only services are out of scope; none appear in this cohort's dives.

**Evidence quality.** Every C09 performance section says no benchmark was gathered or run. The one quantitative fact with a real CVSS score is the Ollama CVE (ollama-07). Everything else is a design or licence statement.

## 2. Capability comparison

### 2.1 Agent and tool protocols (CAP-59)

| Aspect | MCP (spec 2026-07-28) | A2A | Agent frameworks (AutoGen/MAF/PydanticAI/CrewAI/Claude Agent SDK) | DSPy | EOIP @HEAD |
|---|---|---|---|---|---|
| Purpose | Agent/IDE-to-tool interface (mcp-01) | Agent-to-agent task protocol, JSON-RPC 2.0/HTTP, SSE, push notifications (a2a-01) | In-process orchestration patterns: sequential, concurrent, handoff, group (agfw-02) | Metric-driven prompt/weight compilation (dspy-01) | `apps/mcp/main.py`, FastMCP stateless_http, 18 tools (BL-47, mcp-17) |
| Authorization | Optional; PRM (RFC 9728) and resource indicators (RFC 8707) MUST when used; servers MUST validate audience, MUST NOT accept tokens for other audiences; token passthrough forbidden (mcp-06, -08) | **Not specified at the protocol level**; "authorisation schemes listed as future work" (a2a-01) | None of the frameworks ship tenant isolation or egress control (agfw dive) | n/a | **One shared static bootstrap token**, `hmac.compare_digest`; every caller is the same principal; no per-user identity or tenant propagates (mcp-17, BL-47) |
| Tool trust signalling | Annotations (`readOnlyHint` default false, `destructiveHint` true) are advisory, untrusted unless from a trusted server; human-in-the-loop only SHOULD (mcp-03) | n/a | Typed outputs, checkpointed human-in-the-loop in MAF/PydanticAI (agfw-02) | n/a | 18 tools, **no annotations at all** (mcp-17) |
| Reference server quality | Graph-DB servers are Labs/community grade; mcp-neo4j runs read/write Cypher (mcp-09); Neptune server is not read-only, runs any query, scope via IAM (mcp-12); FalkorDB server read-only by default but overridable (mcp-10); TigerGraph licence unclear (mcp-13) | n/a | AutoGen **archived**, no fixes, migrate to MAF (agfw-01) | n/a | `tools_contract/mcp_server.py` (identity-spoof checks, ontology/graph/action tools) exists but is **not mounted**; separately instantiates `ActionEngine(write_back_enabled=True)` (01a NB-03, U-14) |
| Known attacks | Tool poisoning / rug pull disclosed 2025-04-01; attack-success figures conflict between sources (36.5% MCPTox vs over 60% in a CSA note), not reconciled (mcp-16) | Prompt injection across agents not solved by the protocol (a2a dive) | Unbounded tool loops, context growth, non-deterministic handoffs (agfw dive) | Metric gaming, overfitting to a small dev set (dspy dive) | `agents/governed.py:250` calls `retrieve` without `scope` or `allow` (01a BL-48) |
| Governance | Spec breaking change 2026-07-28 removed the handshake, sessions, SSE resumability; SDK 2.x breaks 1.x; licence of the spec text and Python SDK **not examined** (mcp-04, -10, dive section 10) | Apache-2.0 spec and SDK, patent grant; TSC has nine company seats, startup-phase governance, 18-month steady state undecided (a2a-02, -04) | MIT/Apache-2.0 per metadata; each pulls a large, unmeasured transitive tree against the nine-package core (ADR-H15); Claude Agent SDK terms need verification against service terms (agfw dive) | MIT (dspy-02) | n/a |

### 2.2 Local model serving (CAP-61, CAP-53/55 where relevant)

| Aspect | Ollama | llama.cpp | vLLM / SGLang | HF TEI | ONNX Runtime | EOIP @HEAD |
|---|---|---|---|---|---|---|
| Role | Trivial local LLM and embedding serving (ollama-04, -05) | Dependency-free CPU serving: chat, embeddings, rerank, JSON-schema output, metrics (llcpp-01, -05) | High-concurrency GPU serving, OpenAI-compatible API, PagedAttention, continuous batching (vsg-01) | Embedding/rerank server, CPU ONNX path, metrics, tracing (tei-01) | Portable CPU inference library with quantisation (ort-01, -02) | `models/port.py`, `ModelAdapter`, `LLMTelemetry`, task router, circuit breakers (01a NB-10) |
| CPU viability | Works but memory-bandwidth-bound; embedding models (nomic-embed-text, 274 MB, 2K context) are CPU-feasible; 7B+ chat models are not sized here (ollama-08, dive) | CPU instruction-set builds exist; throughput far below GPU serving (llcpp-01, dive) | **Not the design centre**; single-node CPU use possible but unoptimised (vsg dive) | CPU image (ARM and x86) exists; throughput bounded by cores and ONNX/Candle kernels (tei-01) | Depends on model, quantisation, instruction set; INT8 accuracy loss must be measured per model (ort dive) | `neural/*` cannot import without `torch` (01a BL-44, BL-57); `RealSemanticProvider` is a SHA-256 simulation, not a model (01a, cohort 10 cross-ref) |
| Security | **CVE-2026-103663**: unauthenticated path traversal via `/api/pull` digests, CVSS v4 9.4, affected 0.34.2 to below 0.35.0, fixed in 0.35.0 (ollama-07); no auth, no tenant concept, process-global model cache (ollama dive) | Flat API keys, no TLS discussion found, `/slots` exposes state unless disabled (llcpp dive) | No verified multi-tenant isolation (vsg dive) | Auth and multi-tenancy not documented in sources read (tei dive) | n/a (library, not a service) | Egress gateway wraps model calls (BL-45); Ollama pinned at **0.12.3** in `deploy/docker-compose.yml`, which **predates the 0.34.2-0.35.0 CVE range** (01-SYSTEM-BASELINE.md section 3) |
| Air-gap | Partial-yes: staged model import, `OLLAMA_NO_CLOUD=1`, firewall egress deny, no `/api/pull`; no air-gap guide in the docs read (ollama dive) | Yes; CPU-only builds fit offline bundles (llcpp dive) | Viable only if the customer mirrors images and weights; not one-node-first (vsg dive) | Viable if weights are pre-staged, to verify; Hugging Face hub dependence by default otherwise (tei dive) | Yes; CPU wheel fits the CPU-only policy (ort dive) | Compose ships Ollama; default sharing level S0 = none (BL-45) |
| Licence | Repository MIT; **model licences pass through** and were not displayed on the pages fetched, so each must be read individually (ollama-08) | MIT engine; model weights carry their own licences (llcpp-02, -04) | Apache-2.0 with patent grant, but Docker/wheel distributions bundle NVIDIA CUDA/PyTorch components not verified here, which EOIP has already declined under ADR-H16 (vsg dive) | Apache-2.0 since 2024-04-08; **HFOILv1.0 at v0.1.0 (2023-10-13)** is a diligence item for any old pinned tag (tei-02, -03) | MIT (ort-01) | n/a |

### 2.3 Local embedding and reranker models (CAP-53, cross-ref cohort 10)

| Model | Licence | Bundle-eligible | Note |
|---|---|---|---|
| bge-m3 | MIT (emb-01) | Yes | 1,024-dim, 8,192 context, dense+sparse+multi-vector, 100+ languages |
| bge-reranker-v2-m3 | Apache-2.0 (emb-02) | Yes | 0.6B |
| multilingual-e5-large-instruct | MIT (emb-03) | Yes | Prefix-convention misuse risk |
| gte-modernbert-base | Apache-2.0 (emb-04) | Yes | about 149M, 768-dim |
| nomic-embed-text-v2-moe | Apache-2.0 (emb-05) | Yes | Truncates at 512 tokens |
| jina-embeddings-v2-base-en | Apache-2.0 (emb-06) | Yes | about 137M |
| jina v3, v5-text, colbert-v2 | CC-BY-NC-4.0 (emb-07, -09) | **No** | Non-commercial |
| jina-embeddings-v4 | Qwen Research License (emb-08) | Legal review | Card corrects an earlier mislabel as cc-by-nc |
| ColBERTv2 | MIT (emb-10) | Yes | Multi-vector storage blow-up |
| sentence-transformers | per PyPI metadata (emb-11) | n/a | Not installed in EOIP's lock |
| TEI | n/a (server) | n/a | Serves Qwen3-Embedding, Gemma3, Nomic, GTE, E5, BGE rerankers (emb-12) |

### 2.4 Guardrails (CAP-46/CAP-49)

| Item | Role | Licence | CPU feasibility |
|---|---|---|---|
| NeMo Guardrails | Rails at input, retrieval, execution, output, configured per point (grd-02) | Apache-2.0 | Embeddable; each LLM-based rail adds a model call (dive) |
| Llama Guard 4 (12B) | Text+image safety classifier (grd-03) | Llama 4 Community License: gated, not OSI, AUP incorporated, about 700M MAU threshold per a secondary summary (grd-05) | A 12B guard on CPU is expensive, not measured (dive) |
| Llama Prompt Guard 2 (86M) | Benign/malicious injection classifier, 8 languages (grd-04) | Same Llama 4 licence family | 86M backbone is CPU-feasible (dive) |
| EOIP `KnowledgeFirewall` | Regex-pattern injection defence (self-inversion, INV-grd-01) | n/a | Already CPU-native, but the dive calls the pattern list brittle by reading the file |

## 3. Operational and licensing comparison

| Member | Licence class | Redistribution / OEM trigger | One-node footprint | Air-gap | Maintenance |
|---|---|---|---|---|---|
| MCP | Spec and Python SDK licence **not examined** | Verify before redistribution; do not bundle third-party graph servers (TigerGraph licence unclear, mcp-13) | In-process | Yes; stdio and Streamable HTTP need no cloud (mcp-05) | 2026-07-28 revision is breaking; SDK 1.30.0 does not document support for it (mcp-07) |
| Ollama | MIT (server) | Model licences pass through; ship no weights by default, keep a model-licence register (ollama dive) | Light; CPU memory-bandwidth-bound | Partial-yes; no air-gap guide found | 0.x, weekly-or-faster releases, mutable tags; **unpatched CVE range 0.34.2 to below 0.35.0 in the field generally**, though EOIP's pin (0.12.3) predates it |
| A2A | Apache-2.0, patent grant | None identified | Pure HTTP | Yes between in-perimeter agents; webhooks need inbound reachability, awkward in air-gapped single-node deployments (a2a dive) | v1.0.1 (2026-05-28); governance steady-state undecided for 18 months (a2a-02, -03) |
| Agent frameworks | MIT/Apache-2.0 per metadata | Claude Agent SDK terms need verification against service terms; CrewAI commercial-tier boundaries to check (agfw dive) | Large, unmeasured transitive trees against the 9-package core | Viable only with a local model endpoint | AutoGen archived; vendor gravity to Azure/Foundry, Gemini/Vertex, Claude (agfw dive) |
| DSPy | MIT | None found | Pure Python | Viable with a local endpoint | Compile needs many LM calls, slow on CPU-only reference hardware unless a customer provides a GPU endpoint (dspy dive) |
| llama.cpp | MIT | None for the engine; model weights carry their own licences | Dependency-free, CPU-only builds fit offline bundles | Yes | Build-numbered releases (b11889), no stability promise (llcpp-01, -03) |
| vLLM / SGLang | Apache-2.0, patent grant | **Distributions bundle NVIDIA CUDA/PyTorch components EOIP has already declined (ADR-H16)**; document as customer-provisioned only | Not one-node-first | Viable if the customer mirrors images and weights | Fast-moving 0.x APIs (vsg dive) |
| HF TEI | Apache-2.0 from 2024-04-08 | **HFOILv1.0 at v0.1.0 is a diligence item for old pinned tags** (tei-02) | Small CPU image, ARM and x86 | Viable if weights are pre-staged, to verify | v1.9.4 (2026-09-15) |
| ONNX Runtime | MIT | None for the runtime; check transitive native libraries in the wheel, not audited | CPU wheel fits the policy | Yes | v1.31.0 (2026-10-09) |
| Guardrails (NeMo) | Apache-2.0 | None | Embeddable | Yes with local checker models | v0.24.1 (2026-09-16) |
| Llama Guard / Prompt Guard | **Llama 4 Community License**, gated, non-OSI | **Weights cannot be silently bundled**; customer downloads under Meta's terms | n/a (model weights) | Requires gated download | n/a |

## 4. Performance evidence

No independent or vendor benchmark was collected for any member in this cohort. The only hard figure is a security one:

| Figure | Source | Class |
|---|---|---|
| CVE-2026-103663: unauthenticated path traversal via `/api/pull` digests, CVSS v4 9.4 (6.9 without write access to `/usr/lib/ollama`), affected 0.34.2 to below 0.35.0, published 2026-10-08, fixed in 0.35.0 | ollama-07 | Officially documented (CVE record) |
| nomic-embed-text: 274 MB, 2K context (as a sizing data point for CPU embedding feasibility) | ollama-08 | Officially documented (model library page) |

No throughput, latency, or token-cost figure exists for MCP overhead, A2A overhead, any agent framework, DSPy compilation, llama.cpp, vLLM/SGLang, TEI, or ONNX Runtime on CPU reference hardware. No comparison can declare a winner.

## 5. Findings

1. **EOIP's MCP surface fails two of the specification's own security rules.** The spec requires audience validation and forbids token passthrough (mcp-06, -08); EOIP's server authenticates one static shared secret with no principal, so every caller is indistinguishable and the confused-deputy problem applies directly (mcp-17, INV-mcp-02).
2. **The better-designed MCP contract already exists in the codebase and is not live.** `tools_contract/mcp_server.py` has identity-spoof checks but is not mounted, and it separately constructs an `ActionEngine` with `write_back_enabled=True` (01a NB-03), which would reverse ADR-007's read-only-MCP-by-design decision if ever wired up without review.
3. **Reference MCP servers for graph databases are themselves insecure by default.** mcp-neo4j runs read/write Cypher (mcp-09); the Neptune server executes arbitrary queries, not read-only, scoped only by IAM (mcp-12); FalkorDB's is read-only by default but overridable (mcp-10). EOIP's own QueryPlan-template design (ADR-006) is confirmed as the right inversion (INV-mcp-03) and should not be weakened to match these examples.
4. **A2A has no authorization story at the protocol level at all** ("future work", a2a-01); any A2A adapter must map the external agent's identity to an EOIP tenant principal and enforce BL-18 inside the executor, not trust the protocol.
5. **No agent framework in the cohort ships tenant isolation or egress control**, and adopting one adds a dependency without closing a gap (agfw dive). AutoGen's archival within about a year of wide adoption (agfw-01) is a concrete churn risk for betting on any single framework; EOIP's own typed `contracts/agent.py` plus resumable run state is the safer base (STR-agfw-01).
6. **EOIP's prediction and generation stack cannot run a real local model today.** `neural/*` cannot import without `torch`, which is absent from every lock (BL-44, BL-57, cross-ref cohort 13), and `RealSemanticProvider` in the retrieval path is a SHA-256 hash simulation, not an embedding model (01a). The gap is not model choice; it is that nothing has been wired to a real CPU-capable serving engine yet.
7. **Ollama's compose pin (0.12.3) happens to predate the only confirmed CVE range found (0.34.2 to below 0.35.0), but this is not evidence of safety, only of non-exposure to that specific flaw.** Ollama has no auth and no tenant concept by design (ollama dive); any upgrade must re-check the CVE list, and the deployment must keep the engine off any externally reachable interface regardless of version.
8. **Model-licence pass-through is unmanaged.** Ollama's library pages did not display licence text for the models fetched (ollama-08); EOIP has no model-licence register today despite NB-10's model catalog existing. Four embedding-model variants in the local-embeddings dive are non-commercial or research-licensed (emb-07, -08, -09) and must never be silently bundled.
9. **llama.cpp and ONNX Runtime are the cleanest CPU-only, licence-clean serving candidates; vLLM/SGLang and gated Llama Guard models are explicitly non-bundleable.** llama.cpp and ORT are MIT with no redistribution trigger for the engine itself (llcpp dive, ort dive); vLLM/SGLang distributions carry NVIDIA-licensed components already declined under ADR-H16 (vsg dive); Llama Guard and Prompt Guard require a gated, customer-performed download under Meta's non-OSI terms (grd-03, -04, -05).
10. **The agent surface's own threat (tool poisoning, confused deputy) has no reconciled severity estimate.** Reported attack-success rates for MCP tool poisoning conflict by source (36.5% vs over 60%, mcp-16) and are not reconciled in the dive; treat the threat as real and unquantified, not as a solved or a negligible risk.

## 6. Implications for EOIP

| CAP | Parity needed (STR-IDs) | Exploitable weakness (INV-IDs) | Decision | Candidate gap statement |
|---|---|---|---|---|
| CAP-59 MCP hardening | STR-mcp-02 (OAuth audience binding, scope step-up), STR-mcp-03 (annotate all 18 tools) | INV-mcp-02 (confused deputy via single shared token), INV-mcp-01 (tool poisoning), INV-mcp-03 (raw-query servers as the inversion to avoid) | **BUILD, P0** | Move MCP to resource-server mode with per-user tokens and tool annotations; decide whether to mount or retire `tools_contract/mcp_server.py` (U-14) before any write-back path is enabled. |
| CAP-46/CAP-47 via agent paths | STR-a2a-01 (principal mapping in the executor) | INV-a2a-01 (no authorization at protocol level) | **BUILD, P0** | `agents/governed.py:250` must pass `scope` and `allow`; any A2A adapter maps external identity to a tenant principal before touching retrieval. |
| CAP-48/agent runtime | STR-agfw-01 (typed `AgentResult`, resumable run state) | INV-agfw-01 (no policy plane across frameworks; AutoGen archival) | **BUILD** in-house thin loop with swappable adapters; **REFERENCE** framework patterns only | Do not adopt a full third-party framework as a dependency; borrow typed-output and checkpoint patterns. |
| CAP-61 local serving | STR-llcpp-01 (`LlamaCppProvider` implementing `EmbeddingProvider`), STR-tei-01 (`TeiEmbeddingProvider`/`TeiReranker`), STR-ort-01 (`OnnxEmbeddingProvider` with export manifest), STR-ollama-01/-02 (digest-pinned provider adapter, signed bundle import) | INV-ollama-01 (unauthenticated API in some versions), INV-vsg-01 (CUDA-coupled distribution vs CPU-only policy) | **BUILD, P0**: wire one real CPU-capable provider behind `ModelPort`; **REJECT** bundling vLLM/SGLang; **INTEGRATE** llama.cpp or TEI as the first real embedding path | This closes the gap found in finding 6: no real local model currently executes in any EOIP path. |
| CAP-53 embeddings, licence | STR-emb-01 (bge-m3 as the single default) | INV-emb-01 (mixed Jina licences), INV-emb-02 (hashing embedder has no semantics) | **BUILD** a licence allow-list in the model catalog; **REUSE** bge-m3/gte-modernbert/e5/nomic as defaults | No model-licence register exists despite NB-10's catalog; build it before shipping any real embedding default. |
| CAP-49 injection defence | STR-grd-01 (rails at five points), STR-grd-02 (small local injection classifier, customer-supplied weights) | INV-grd-01 (regex firewall brittle), INV-grd-02 (Llama licence non-OSI, gated) | **BUILD, P1**: layered defence, regex first, optional classifier second; never bundle Llama Guard/Prompt Guard weights | Firewall hooks should map to NeMo's five rail points even without adopting NeMo itself. |
| CAP-58 NL-to-query | STR-dspy-01 (metric-driven compilation, versioned artefacts) | INV-dspy-01 (compile cost, metric dependence; slow on CPU without a GPU endpoint) | **EXPERIMENT, P2** | Keep the deterministic template tier (BL-11) primary; DSPy only as an optional path when an LLM is already enabled and a labelled dev set of useful size exists. |
| CAP-79 model supply chain | STR-ollama-02 (signed model bundle format) | INV-ollama-02 (model-licence pass-through), INV-tei-01 (HFOIL-era tags) | **BUILD, P2** | SBOM entries per bundled model weight; pin TEI tags to post-2024-04-08 and verify LICENSE in the image. |

## 7. Open questions

1. Who decides whether `tools_contract/mcp_server.py` is mounted, and under what review does its `ActionEngine(write_back_enabled=True)` get approved or stripped (U-14)?
2. Which single local-serving engine (llama.cpp, TEI, ONNX Runtime, or Ollama with a verified post-fix version) becomes the first real `ModelPort` provider, and on what CPU hardware is it qualified under ADR-H15?
3. Is the Ollama version in compose (0.12.3) ever intended to move forward, and if so, what version gate excludes the 0.34.2-to-below-0.35.0 CVE range going forward?
4. Has Claude Agent SDK's repository LICENSE been reconciled against its service terms, and does CrewAI's commercial-tier boundary affect anything EOIP would adopt (agfw dive, both unverified)?
5. What is the real, reconciled attack-success rate for MCP tool poisoning against EOIP's own tool set, once `security/redteam` (cohort 12, INV-lt-02) exists?
6. Does any A2A adoption plan exist, or is it purely a future-reach capability with no current customer demand?
