| Field | Value |
|---|---|
| Registry ID | T-C09-onnx-runtime |
| Tier | B (CPU inference runtime; engine behind several embedding servers) |
| Versions examined | onnxruntime 1.31.0 (2026-10-09, PyPI) |
| Verified on | 2026-10-26 |
| Worker | V22 |

## 1. Identity, current status, tier, sources

ONNX Runtime (ORT), `microsoft/onnxruntime`, a cross-platform inference and training accelerator for models in the ONNX format. Licence **MIT** (PyPI metadata; copyright holder Microsoft) [CLAIM-ort-01]. Latest PyPI release 1.31.0, 2026-10-09 [CLAIM-ort-01]. Docs list execution providers (EPs) for NVIDIA CUDA and TensorRT, Intel OpenVINO and oneDNN, Windows DirectML, Qualcomm QNN, Android NNAPI, Apple CoreML, XNNPACK, AMD ROCm and MIGraphX, WebGPU, plus community EPs; language bindings Python, C++, C, C#, Java, JavaScript, Objective-C, with Julia, Ruby, Rust via community projects [CLAIM-ort-02]. The CPU path uses core ORT kernels rather than a listed EP [CLAIM-ort-02]. ONNX format governance (LF AI & Data) is general knowledge, UNVERIFIED here. Status: active, 1.x, production.

## 2. Problem, workloads, workflows

Problem: run one exported model graph portably and quickly across hardware. EOIP workloads: CPU embeddings and cross-encoder reranking (BL-14 replacement), small classifiers (PII/injection detectors), OCR/ASR components (CRA-014). Workflow: export model to ONNX, optionally quantise to INT8, ship with the customer's offline bundle, load via `onnxruntime.InferenceSession(providers=["CPUExecutionProvider"])`.

## 3. Feature inventory

| Feature | Status | Note |
|---|---|---|
| CPU execution, graph optimisation | present | [CLAIM-ort-02] |
| Quantisation tooling (INT8, float16, mixed precision) | present | docs section "Quantize ONNX models" [CLAIM-ort-02] |
| Many hardware EPs | optional | [CLAIM-ort-02] |
| Generate API / GenAI extension for LLMs | present, labelled Preview | Phi-3, DeepSeek-R1-Distill tutorials; LoRA adapters [CLAIM-ort-02] |
| Language bindings (listed above) | present | [CLAIM-ort-02] |
| Model hub / server | absent | library only; TEI embeds ORT (`ort`) for CPU [CLAIM-ort-03 via C09-hf-tei] |
| Tenancy / policy | N/A | library |

## 4. Architecture

```
 model.onnx --load--> InferenceSession --graph optimisation (fusions, constant folding)--> partition by EP
     --> CPU kernels (MLAS) | accelerator EP(s) --> outputs ; session options: threads, memory arena
```
Partitioning/kernel names (MLAS etc.) are general knowledge: UNVERIFIED in sources read.

## 5. Under-the-hood reconstruction

Load graph, run optimisation passes, assign nodes to EPs by capability with CPU as fallback, execute with a thread pool. Quantised operators (QDQ or QOperator) run in INT8 kernels on CPU (hypothesis). No source read at a pinned tag; file-level claims withheld.

## 6. Requirements inferred

FR: reproducible export recipe per model (opset, dynamic axes, tokenizer artefacts); parity test against the reference PyTorch output. NFR: pinned wheel with hash (ADR-H15 hash-locked file); CPU-only wheel (`onnxruntime`, not `onnxruntime-gpu`, since GPU wheels pull CUDA, see ADR-H16); thread limits for noisy neighbours.

## 7. Performance and resource model

No benchmark collected. Performance depends on model, quantisation, CPU instruction set; INT8 accuracy loss must be measured per model. Failure modes: unsupported operators in exported graphs, tokenizer mismatches (tokenization is outside ORT), dynamic-shape slowdowns.

## 8. Strengths

MIT, mature, small CPU footprint relative to torch, wide bindings (Python and also non-Python hosts). Match: use as the CPU numeric engine for embeddings/rerankers/classifiers in optional `neural-text` extra, instead of torch where models export cleanly. Exceed: EOIP-side parity and drift tests.

## 9. Limitations

Friction: export pipelines and tokenizer handling are the integrator's job; GenAI API in preview; INT8 quality drift; ONNX export of new architectures lags. Operational: separate wheels per accelerator. Licensing: MIT runtime, models carry their own licences.

## 10. Deployment, licensing, viability

MIT, redistributable; CPU wheel fits CPU-only policy; air-gap viable; one-node friendly. No legal trigger for the runtime. Check transitive native libraries in the wheel (not audited).

## 11. Competitive delta vs EOIP baseline

EOIP's planned stack is torch-based N1/N2 (BL-57, ADR-H15) with numpy absent from the lock today. ORT is a lighter inference-only alternative for N2 tasks; no ORT usage exists in EOIP (absent, not code-grepped here; treat as Unknown).

## 12. Cards

STR-ort-01 | ONNX Runtime | portable CPU inference with quantisation | CLAIM-ort-01,02 | smaller install than torch for embedding/rerank/classifier in air-gapped bundles | integrate | `OnnxEmbeddingProvider` with export manifest (model hash, opset, tokenizer hash) | cosine parity >= agreed threshold vs reference on 1k texts; wheel size and cold start recorded vs torch.
INV-ort-01 | ORT 1.31.0 | export/tokenizer burden (hypothesis) | root cause UX/maturity, hypothesis | ship pre-exported artefacts in the offline bundle; worse if customers bring custom models | options: (1) use TEI/llama.cpp which hide it; (2) export recipes + parity tests; (3) automatic exporter service | select 1 for default, 2 for custom models | POC: export 3 models, measure parity failures | defensibility: low | decision EXPERIMENT.

## 13. Per-capability decisions

| Capability | Decision |
|---|---|
| CAP-61 CPU model execution (small models) | INTEGRATE (optional) |
| CAP-33/CAP-49 small classifier models | EXPERIMENT |
| GenAI API for LLMs | DEFER (llama.cpp/Ollama cover it) |
| GPU wheels | REJECT for distribution (ADR-H16) |

## 14. Tests

Parity and latency of one embedding model and one reranker in torch vs ORT FP32 vs ORT INT8; wheel hash lock; no network at runtime; session thread caps.

## 15. Risks and open questions

Transitive licences in wheel; GenAI API stability; ORT version compatibility with TEI's `ort` crate; tokenizer packaging.

## Appendix A. Research-dimension coverage

| Dimension | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | MIT, active |
| D2 | 2 | CPU inference |
| D3 | 4 | Session/EP model |
| D4-D7 | N/A | Library |
| D8 | 7 | Thread pool only |
| D9-D12 | N/A | none |
| D13 | 2 | Retrieval models |
| D14-D16 | N/A | none |
| D17 | 3 | Bindings |
| D18 | 6 | Supply chain |
| D19 | N/A | none |
| D20 | 7 | No numbers |
| D21 | 10 | MIT |
| D22 | 8 | ONNX portability |
| D23 | N/A | none found |
| D24 | App. C | docs + PyPI |

## Appendix B. Capability mapping

| CAP-ID | This technology | CLAIM | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-61 | native (library) | ort-02 | BL-57 | INTEGRATE | P2 |
| CAP-53 | partial | ort-02 | BL-14 | EXPERIMENT | P2 |
| CAP-79 | n/a | ort-01 | none | BUILD (hash-lock) | P2 |

## Appendix C. Evidence records

| CLAIM-ID | product/version/date | claim | class | source | dates | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-ort-01 | onnxruntime 1.31.0 | MIT; released 2026-10-09 | Officially documented | https://pypi.org/project/onnxruntime/ | 2026-10-09 / 2026-10-26 | 0.9 | none |
| CLAIM-ort-02 | ORT docs | EP list, bindings, quantisation guide, Generate API (Preview) | Officially documented | https://onnxruntime.ai/docs/ | undated / 2026-10-26 | 0.85 | none |
| CLAIM-ort-03 | TEI README | ONNX backend recommended for x86 CPU | Officially documented | https://github.com/huggingface/text-embeddings-inference | undated / 2026-10-26 | 0.8 | none |

## Appendix D. Assumptions

Licence taken from PyPI metadata; repo LICENSE and third-party notices not read.
