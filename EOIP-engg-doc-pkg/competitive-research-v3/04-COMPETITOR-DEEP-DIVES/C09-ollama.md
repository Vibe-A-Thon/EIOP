| Field | Value |
|---|---|
| Registry ID | T-C09-ollama |
| Tier | A (local model runtime already in EOIP compose; default-local LLM and embedding path) |
| Versions examined | Ollama v0.40.11 (2026-10-24, latest); v0.12.3 (2025-09-26, EOIP pin); v0.35.0 (CVE fix) |
| Verified on | 2026-10-26 |
| Worker | V06 |

## 1. Identity, current status, tier, sources

Ollama (github.com/ollama/ollama, owner Ollama, Inc.; Go server wrapping llama.cpp-family engines) is a local LLM/embedding runtime with a REST API (`/api/generate`, `/api/chat`, `/api/embed`, `/api/pull`, `/api/create`), a model registry at ollama.com, a Modelfile format, desktop apps and optional "cloud models". Licence of the repository: **MIT** (GitHub licence API) [CLAIM-ollama-01]. Release cadence is extreme: v0.40.8 to v0.40.11 shipped within ~3.5 days (2026-10-21 to 2026-10-24) [CLAIM-ollama-02]. EOIP pins `ollama/ollama:0.12.3` (`deploy/docker-compose.yml:192`, profile `ai`): 2025-09-26, i.e. ~13 months and ~28 minor versions behind latest. Status: active, early-production by semantic-version standard (0.x, no stability promise; unverified statement - no compatibility policy found).

## 2. Problem, workloads, workflows

Problem: run open-weight models locally with one-command pull/serve and a stable HTTP API. EOIP workloads: (a) embeddings for retrieval replacing the hashing embedder (BL-14, `models/embeddings.py:44`); (b) local LLM for NL suggestion LLM-assist (BL-12), entity extraction, summarisation, agent runs (BL-48), under egress policy S0 (BL-45). Workflow: operator imports GGUF on a connected staging host -> `ollama create` -> exports model store volume -> loads on air-gapped host -> `POST /api/embed` batch of chunks -> vectors to store.

## 3. Feature inventory

| Feature | Status | Note |
|---|---|---|
| REST chat/generate/embed, batch `input` array, `truncate` (default true), `dimensions`, `keep_alive` | present | `/api/embed` returns `prompt_eval_count`, durations [CLAIM-ollama-05] |
| Model import from local GGUF / safetensors via Modelfile | present | Ollama does not quantise GGUF on import [CLAIM-ollama-04] |
| Concurrency controls | present | `OLLAMA_NUM_PARALLEL` (default 1), `OLLAMA_MAX_LOADED_MODELS` (3 on CPU), `OLLAMA_MAX_QUEUE` 512 -> 503, `OLLAMA_KEEP_ALIVE` 5 min [CLAIM-ollama-03] |
| Authentication | **absent** in server; reverse proxy advised | FAQ shows nginx/ngrok/Cloudflare tunnels, no built-in auth [CLAIM-ollama-03] |
| Disable cloud | present | `OLLAMA_NO_CLOUD=1` or `disable_ollama_cloud` in `~/.ollama/server.json`; removes cloud models and web search [CLAIM-ollama-03] |
| Air-gap guide | **absent** | no dedicated doc; proxies via `HTTPS_PROXY` [CLAIM-ollama-03] |
| Structured outputs, tool calling, vision, speech | present (newer builds) | v0.40.x notes list vision/speech models; not individually verified |
| GPU | optional | NVIDIA container toolkit; none on Docker Desktop macOS [CLAIM-ollama-06] |
| Multi-tenancy, per-user quotas, audit | absent | unknown/none documented |
| SDKs | Python/JS official clients (not examined) | UNVERIFIED here |

## 4. Architecture

```
 client --HTTP 11434--> ollama serve (Go) --scheduler (queue<=512, parallel slots, model LRU, keep_alive)
                                |-- runner subprocess per loaded model (llama.cpp-family backend, CPU or GPU)
                                |-- model store: blobs (sha256 layers) + manifests under OLLAMA_MODELS
                                `-- registry client: /api/pull (OCI-like manifests+layers) --> ollama.com (egress!)
 optional: signin key (id_ed25519) --> cloud models / web search (disabled by OLLAMA_NO_CLOUD)
```
Default bind 127.0.0.1:11434 per FAQ; the official container image is reported by Rapid7 to run as root bound to 0.0.0.0 [CLAIM-ollama-07].

## 5. Under-the-hood reconstruction

- **Model store**: content-addressed layers (weights GGUF, template, params, licence text, adapters) with a manifest per tag; `/api/pull` resolves manifest -> downloads layers by digest. The path-traversal CVEs stem from unvalidated digests mapping to file paths (`digestToPath`) [CLAIM-ollama-07] - hence an air-gapped build must never expose `/api/pull` to untrusted callers.
- **Scheduler**: per-model runner process; admission checks required memory (`RAM ~ NUM_PARALLEL x CONTEXT_LENGTH` scaling) against free memory/VRAM; evicts idle models after `keep_alive`; queue beyond `MAX_QUEUE` returns 503 [CLAIM-ollama-03]. CPU concurrent model load is permitted without the VRAM-fit rule.
- **Embedding path**: `/api/embed` batches an input array into one runner call; truncation silently shortens over-context inputs unless `truncate:false` -> EOIP must set `truncate:false` and chunk itself to avoid silent recall loss (design inference).
- **Modelfile**: `FROM`, `PARAMETER`, `TEMPLATE`, `SYSTEM`, `ADAPTER`, `LICENSE` directives (page examined covered only FROM; others from general knowledge, UNVERIFIED here).
- Concurrency/transactions/partitioning: none beyond process-local scheduling. Security: none native; trust boundary is the network. Versioning: model tags are mutable, digests immutable - pin digests in EOIP config.
- Hypothesis (not proven): the engine rewrite in recent versions changes CPU kernels between releases, so embedding vectors may drift across versions; **EOIP must store model digest + runtime version with every vector** and re-embed on change.

## 6. Inferred requirements for EOIP

FR: embed endpoint behind `models/provider.py` abstraction; model digest allowlist; offline import pipeline; startup check that `/api/pull` is unreachable from tenants. NFR: bind to backend network only (compose `networks: [backend]`, already so), non-root container with read-only root FS, `OLLAMA_NO_CLOUD=1`, per-call manifest (BL-45) recording model digest; CPU-only sizing per ADR-H15..H17 (no CUDA redistribution, GPU unknown).

## 7. Performance and resource model

No vendor benchmark used; none verified. Known scaling rules from docs: RAM scales with parallel x context; default 1 parallel request per model; CPU inference keeps models in system memory. Throughput on CPU is bounded by memory bandwidth and core count; embedding models like `nomic-embed-text` are 274 MB with 2K context (library page) [CLAIM-ollama-08], so a CPU embedding service is feasible, whereas 7B+ chat models on CPU have interactive-latency risk (no measured number; EOIP must measure: BM-AI). Failure modes: 503 under queue pressure, silent truncation, cold-load latency after `keep_alive` expiry, model eviction thrash when `MAX_LOADED_MODELS` exceeded.

## 8. Strengths and how to match/exceed

| Strength | Match/exceed |
|---|---|
| One-binary local serving, MIT, wide model catalogue | INTEGRATE as one of several providers (llama.cpp direct, TEI, ONNX are Tier B siblings) |
| Simple `/api/embed` batching | match through provider abstraction |
| Offline GGUF import | wrap in signed, digest-pinned model bundles (exceed) |
| Fast release cadence | pin by digest, update through staging |

## 9. Limitations with root causes

| Class | Item |
|---|---|
| Security (verified) | CVE-2026-103663: unauthenticated path traversal via `/api/pull` digests, affected 0.34.2 to <0.35.0, CVSS v4 9.4 (6.9 without write to `/usr/lib/ollama`), published 2026-10-08, fixed 0.35.0 [CLAIM-ollama-07]. Earlier: CVE-2024-37032 (<0.1.34, public Metasploit module), CVE-2024-39722 (<0.1.46). Aggregator reports of CVE-2026-7482 "Bleeding Llama" (memory leak) and Windows updater CVEs: affected ranges NOT verified. Whether 0.12.3 is affected by them: UNKNOWN |
| Architectural | No auth, no tenant concept; process-global model cache |
| Operational | 0.x churn; weekly-or-faster releases; mutable tags |
| Licensing | Repository MIT, but **model licences pass through**: Ollama library pages did not display licence text in what I fetched (llama3.2, nomic-embed-text pages stated none) [CLAIM-ollama-08], so the redistributor must read each model's own licence (e.g. community/acceptable-use licences, field-of-use or user-count limits - general knowledge, per-model UNVERIFIED). White-label bundles that ship weights trigger legal review |
| CPU caveat | CPU-only works but memory-bandwidth-bound; AVX/instruction-set requirements not documented in FAQ (UNVERIFIED) |
| Docs | No air-gap guide; telemetry/account metadata collected for cloud features [CLAIM-ollama-03] |

## 10. Deployment, licensing, redistribution

Self-hosted, docker, desktop, managed none (cloud models optional). Air-gap: **partial-yes** - requires staged model import, `OLLAMA_NO_CLOUD=1`, firewall egress deny, no `/api/pull`. Redistribution: server MIT permissive; model weights bring their own terms; EOIP should ship **no weights** by default and keep a model-licence register with SBOM entries (CAP-79). Legal review trigger: yes (model-licence pass-through, not Ollama's own). Compose: update pin from 0.12.3, run non-root, no published host port.

## 11. Competitive delta against EOIP baseline

| Item | Baseline | Delta |
|---|---|---|
| Runtime in compose | `ollama/ollama:0.12.3`, volume `model-data:/root/.ollama`, backend network, profile `ai`; live-unverified | version 13 months old; runs as root (volume path `/root/.ollama`) |
| Provider abstraction | `models/provider.py`, `models/embeddings.py:44,115` Ollama + sentence-transformers (BL-14, BL-57) | good: Ollama is replaceable |
| Egress | gateway default S0 (BL-45) | Ollama's own egress (pull, cloud) is outside the gateway; needs network policy |
| Vectors | hashing embedder default | switch default only after offline-embedding POC |
| numpy absent (BL-57) | N0 tier not installed | Ollama embeddings are an alternative that avoids numpy for dense vectors |

## 12. Cards

STR-ollama-01 | Ollama | trivial local serving + batch embeddings | [ollama-04,05] | air-gapped semantic retrieval w/o GPU | integrate | provider adapter with digest pinning | 10k chunks embedded offline, vectors reproducible within tolerance across two restarts.
STR-ollama-02 | Ollama | MIT runtime + offline import | [ollama-01,04] | redistribution-safe runtime | integrate | signed model bundle format | bundle imports with network blocked.

**INV-ollama-01 (unauthenticated, traversal-prone API).** Target Ollama 0.34.2-<0.35.0 and earlier CVEs. Root cause: *proven* (digest-to-path flaw; no auth). Options: (1) quick - bump pin >=0.35.0, non-root, internal network only; (2) native - EOIP egress sidecar proxy that allows only `/api/embed`, `/api/chat` with tenant+model allowlist and disables `/api/pull`,`/api/create`; (3) long-term - provider-neutral inference gateway with signed model catalogue so Ollama is swappable for llama.cpp server. Selected: 1 now, 2 next. Test: ZAP/Nuclei scan of sidecar; attempt traversal pull must fail; success = 0 reachable mutating endpoints. Failure case: sidecar breaks streaming. Defensibility: ties to EOIP model-licence register and egress manifests. Decision: ADOPT.
**INV-ollama-02 (model-licence pass-through).** Root cause: licensing, *proven* as structure (weights have own licences). Options: allowlist of permissive models (Apache/MIT) only by default; per-model licence acceptance recorded in licence file (BL-22); customer-supplied weights. Decision: ADOPT. Test: CI fails if a model digest lacks a register entry.
**INV-ollama-03 (silent truncation / version-dependent vectors).** Hypothesis for drift; truncation proven by API docs. Decision: EXPERIMENT (store digest+version per vector; re-embed job).

## 13. Per-capability decisions

| Capability | Decision |
|---|---|
| CAP-61 local model serving | INTEGRATE Ollama as default dev/one-node provider; EXPERIMENT llama.cpp/TEI/ONNX for CPU efficiency (Tier B) |
| CAP-53 embeddings for vector search | INTEGRATE via provider; REJECT keeping hashing embedder as production default |
| CAP-51 egress control | BUILD sidecar/network policy around Ollama |
| CAP-50 air-gap | BUILD model-bundle import procedure |
| CAP-79 supply chain | BUILD model digests + licences in SBOM |

## 14. Tests and acceptance

1. Pin >=0.35.0 (latest tested 0.40.x); container scan; non-root start. 2. Network-deny test: with egress blocked, `/api/embed` works, `/api/pull` fails closed. 3. Reproducibility: embed fixed corpus twice and across two Ollama versions; cosine drift report. 4. CPU sizing run: `nomic-embed-text` batch throughput and a 3B chat model latency on target one-node CPU (record hardware). 5. `truncate:false` enforced; over-length input errors instead of truncating. 6. Model-licence register check.

## 15. Risks and open questions

Which CVEs affect 0.12.3 (unverified); 0.x API breaks between pin bumps; model-licence terms of default models; CPU latency for agent runs; whether Ollama telemetry exists beyond cloud account metadata (unverified); desktop/Windows updater CVEs (aggregator-only).

## Appendix A. Dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | MIT, cadence, owner |
| D2 | 2 | local serving |
| D3 | 4 | scheduler, runner, store |
| D4 | 5 | content-addressed blobs; no index |
| D5 | N/A | no schema |
| D6 | N/A | not a query engine |
| D7 | N/A | |
| D8 | 5,7 | process-local scheduling; no HA |
| D9 | N/A | |
| D10 | N/A | |
| D11 | 5 | tag vs digest versions |
| D12 | N/A | embeddings only |
| D13 | 2,5 | embed/chat provider |
| D14 | 2 | LLM-assist host only |
| D15 | N/A | |
| D16 | 3 | desktop app, CLI |
| D17 | 3 | API, Modelfile |
| D18 | 9,12 | CVEs, no auth, root container |
| D19 | 9 | none |
| D20 | 7 | no figures; EOIP must measure |
| D21 | 10 | MIT; cloud paid features not examined |
| D22 | 5 | GGUF import/export |
| D23 | N/A | not examined |
| D24 | 9 | aggregator CVE data flagged |

## Appendix B. Capability mapping

| CAP | This tech | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-61 | native | ollama-03,04 | BL-57/BL-14 Partial | INTEGRATE | P1 |
| CAP-53 | partial (embedding provider) | ollama-05 | BL-14 Partial | INTEGRATE | P1 |
| CAP-50 | partial | ollama-03 | compose files | BUILD procedure | P1 |
| CAP-51 | absent | ollama-03 | BL-45 Implemented | BUILD | P1 |
| CAP-79 | absent | ollama-08 | none | BUILD | P2 |

## Appendix C. Evidence records (accessed 2026-10-26)

| CLAIM | product/version/date | claim | class | source | pub/access | conf | contradictory |
|---|---|---|---|---|---|---|---|
| ollama-01 | repo main | Licence MIT | Officially documented | GitHub licence API https://api.github.com/repos/ollama/ollama/license | /2026-10-26 | 0.95 | none |
| ollama-02 | v0.40.8-0.40.11; v0.12.3 | Latest v0.40.11 published 2026-10-24T00:30Z; v0.40.8 2026-10-21; v0.12.3 published 2025-09-26T05:08Z | Officially documented | GitHub releases https://github.com/ollama/ollama/releases | /2026-10-26 | 0.95 | none |
| ollama-03 | docs 2026-10 | Default bind 127.0.0.1:11434; OLLAMA_MODELS, NUM_PARALLEL=1, MAX_LOADED_MODELS=3 CPU, MAX_QUEUE=512, KEEP_ALIVE=5m, NO_CLOUD; no built-in auth; no air-gap guide; cloud signin key | Officially documented | Ollama FAQ https://docs.ollama.com/faq | /2026-10-26 | 0.85 (summarised) | none |
| ollama-04 | docs | GGUF/safetensors import via Modelfile; no quantisation on import | Officially documented | https://docs.ollama.com/import | /2026-10-26 | 0.85 | none |
| ollama-05 | docs | `/api/embed`: input string or array, truncate default true, dimensions, keep_alive | Officially documented | https://docs.ollama.com/api/embed | /2026-10-26 | 0.85 | none |
| ollama-06 | docs | GPU in Docker needs nvidia toolkit; none on macOS Docker Desktop; CPU memory scales parallel x context | Officially documented | Ollama FAQ (repo docs/faq.mdx) https://github.com/ollama/ollama | /2026-10-26 | 0.8 | none |
| ollama-07 | 0.34.2-<0.35.0 | CVE-2026-103663 path traversal in /api/pull, fixed 0.35.0, CVSS v4 9.4/6.9, published 2026-10-08; earlier CVE-2024-37032, -39722; default image root/0.0.0.0 (Rapid7) | Third-party report (CVE database) | OpenCVE https://app.opencve.io/cve/CVE-2026-103663 ; Rapid7 https://www.rapid7.com/db/modules/exploit/linux/http/ollama_rce_cve_2024_37032/ | 2026-10-08 / 2026-10-26 | 0.7: one search aggregator earlier cited v0.14.0-rc1 as lower bound; used OpenCVE | affected-range conflict |
| ollama-08 | library pages | llama3.2 sizes 1.3-2.0 GB, 128K ctx; nomic-embed-text 274 MB, 2K ctx; licence not shown in fetched text | Officially documented | https://ollama.com/library/nomic-embed-text ; /llama3.2 | /2026-10-26 | 0.6 (licence absence may be extraction artefact) | none |
| ollama-09 | EOIP repo | compose pins ollama/ollama:0.12.3, profile ai, volume /root/.ollama | Observed in source code | deploy/docker-compose.yml:192-196 | /2026-10-26 | 0.95 | none |

## Appendix D. Assumptions

Verified date is 2026-10-26. Model-licence content of specific models not read (pass-through risk stated structurally). Ollama internals described are from docs plus general architecture knowledge; engine-level claims beyond docs marked hypothesis. No live run.
