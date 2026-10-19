# EOIP / KGF Processing Units: Research and Feasibility

Research date: 2026-10-19.

Status: Research and proposed architecture, not implemented functionality or a production certification. Repository baseline: `cc03ea9436df67a900280d9dfbb69036cc3c3242`, plus the working-tree files inspected during this task. Other work may change those files; revalidate before implementation.

Companions: [Requirements](processing-units-requirements.md), [Implementation plan](processing-units-implementation-plan.md), [Suite architecture](docs/EOIP-suite-architecture-plan.md), [Multi-repository suite](eopisuite/multi/docs/README.md).

## 1. Direct Answer

**Yes, software on a regular CPU can perform useful workloads associated with all ten categories. No, this does not manufacture ten physical processors or reproduce all their properties.** GPU and NPU hardware can optionally accelerate supported workloads; they are not prerequisites for the defined software baseline.

There are three different projects one might mean:

| Interpretation | What it delivers | Recommendation for EOIP |
|---|---|---|
| Functional software implementation | Performs a defined calculation or workflow using existing CPU/GPU/NPU libraries | Build this for all ten logical profiles |
| Instruction/device emulation | Models a specified instruction set, device interface or circuit behavior | Use existing tools only for a justified compatibility or research need |
| Hardware-equivalent replacement | Same silicon throughput, memory bandwidth, electrical isolation, power use or physical quantum behavior | Not achievable merely by adding Python code |

The practical product is **EOIP Processing Runtime**, a governed execution layer. CPU, GPU, TPU, NPU, DPU, QPU, APU, LPU, IPU and VPU are workload profiles and discovery aliases. They are not ten new hardware devices, ten proprietary instruction sets, or ten independently deployed services.

The names overlap. Tensor, neural, vision and language workloads share numerical kernels. A GPU can perform tensor inference; an NPU may support only a subset of a model; an APU is a physical integration category, not a separate mathematical operation. IPU and LPU also have vendor-specific meanings. EOIP must use descriptive UI labels and avoid implied vendor affiliation or binary compatibility.

## 2. Findings for Each Unit

### 2.1 CPU: General execution

QEMU demonstrates that instruction-set emulation is possible through its Tiny Code Generator. That is distinct from running Python and native numerical libraries on the host CPU. EOIP normally needs the latter, not a virtual machine inside its graph engine. [QEMU emulation](https://www.qemu.org/docs/master/about/emulation.html)

**EOIP use:** deterministic transformations, validation, bounded graph operations, reductions, scheduling and policy checks. Use standard Python orchestration, processes for CPU-bound Python work, and existing compiled libraries for numerical kernels. Threads are suitable where the actual implementation releases the GIL or performs I/O; adding threads does not automatically accelerate Python bytecode.

**Boundary:** no x86/ARM emulator, guest operating system, cycle-accurate model, arbitrary customer Python execution or privileged device access in the initial scope.

### 2.2 GPU: Parallel numerical work and graphics

Mesa's llvmpipe is a concrete example of CPU software rasterization. It does not establish universal CUDA binary compatibility. Separately, NumPy matrix multiplication can use optimized BLAS on a CPU. Both demonstrate functional software alternatives for particular operations, not GPU-equivalent performance. [Mesa llvmpipe](https://docs.mesa3d.org/drivers/llvmpipe.html), [NumPy matmul](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html)

**EOIP use:** vector similarity, batched matrix multiplication, sparse feature operations and analytics. CPU reference execution is mandatory. A qualified provider may accelerate the same versioned operators on a physical GPU. Browser graph rendering remains with the existing frontend renderer, not a new server-side graphics stack.

**Boundary:** arbitrary GPU kernels, CUDA/PTX compatibility, game rendering, VRAM virtualization and claimed GPU TOPS on CPU are not included. Small jobs can be slower on an accelerator after transfer and compilation costs; measure end-to-end time.

### 2.3 TPU: Tensor execution

Google documents a TPU as specialized hardware with matrix, vector and scalar compute components. Tensor mathematics can execute on other processors, but the TPU's physical matrix units and interconnect do not appear when a CPU library is installed. [Cloud TPU architecture](https://docs.cloud.google.com/tpu/docs/system-architecture-tpu-vm?hl=en), [Original TPU evaluation paper](https://arxiv.org/abs/1704.04760)

**EOIP use:** a portable tensor profile: matrix operations, convolution, activations, reductions, normalization, quantized inference evaluation and bounded ONNX graph execution. Reuse the same numerical/model backends as NPU rather than writing another neural framework.

**Boundary:** no TPU ISA emulator, Google runtime compatibility claim, systolic-array timing promise or cloud TPU dependency. Training foundation models is not required for EOIP's knowledge workflows.

### 2.4 NPU: Neural inference

ONNX Runtime execution providers assign supported parts of a model to available backends. A provider being installed does not prove that a particular model ran on its accelerator. OpenVINO and QNN documentation describe device-specific support and fallback behavior; qualification must cover the actual model, shapes, precision, runtime and driver. [ONNX execution providers](https://onnxruntime.ai/docs/execution-providers/), [OpenVINO provider](https://onnxruntime.ai/docs/execution-providers/OpenVINO-ExecutionProvider.html), [QNN provider](https://onnxruntime.ai/docs/execution-providers/QNN-ExecutionProvider.html)

**EOIP use:** local embeddings, small classification and scoring models, optional vision models and inference for approved graph models. CPU ONNX execution is the functional baseline. Intel NPU is the first optional NPU qualification target, not a claim of universal NPU compatibility.

**Boundary:** an NPU cannot generally execute arbitrary Python, a graph database, every ONNX operator or every LLM. Do not silently report CPU fallback as NPU execution. Vendor SDKs, operating systems, architectures, licenses and drivers require separate qualification.

### 2.5 DPU: Data-plane processing

NVIDIA describes BlueField/DOCA in terms of network, storage and security offload onto separate hardware. Software on the host can perform analogous data-processing functions, but it does not acquire that separate hardware trust boundary or free the host from doing the work. [DOCA overview](https://developer.nvidia.com/networking/doca/overview)

**EOIP use:** bounded ingestion batches, schema checks, checksums, compression, deduplication, rate limiting, redaction, provenance envelopes and backpressure. Reuse the existing connector and ingestion paths; deterministic scripts do these tasks without an LLM.

**Boundary:** no line-rate networking promise, SmartNIC emulation, kernel-bypass framework, custom encryption, host-independent firewall or storage controller. TLS and encryption remain the responsibility of approved existing libraries and deployment services.

### 2.6 QPU: Classical simulation only

Qiskit Aer supplies CPU simulation methods including statevector, density matrix and stabilizer simulation. Some methods have optional GPU support, with separate build and hardware constraints. A simulator is not a physical QPU and does not establish quantum advantage. [AerSimulator reference](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html)

**EOIP use:** optional, bounded research on small graph partitioning/optimization examples, with classical comparisons and a visible `SIMULATED` label. It is not required for normal ingestion, query, decisions or security.

For a dense complex128 statevector, raw state storage is `16 * 2^n` bytes. Thus 20 qubits require 16 MiB, 30 require 16 GiB and 40 require 16 TiB before additional workspace and runtime overhead. A dense density matrix uses `16 * 4^n` bytes. This arithmetic follows the simulator's representation; it is not a benchmark. Resource estimates must include intermediates, copies and concurrent jobs. [Aer memory options and implementation](https://github.com/Qiskit/qiskit-aer/blob/main/qiskit_aer/backends/aer_simulator.py)

Specialized methods can exploit structure, but they do not remove worst-case complexity for arbitrary circuits. The first EOIP profile therefore caps statevector circuits at 20 qubits, density-matrix circuits at 10, and rejects oversized work before allocation.

**Boundary:** no quantum randomness, physical entanglement, quantum-secure key distribution, general cryptanalytic service, hardware noise calibration claim, or automatic quantum improvement claim.

### 2.7 APU: Heterogeneous orchestration

An AMD APU integrates CPU and graphics/accelerator resources; the MI300A documentation illustrates a particular coherent-memory implementation. A software scheduler can coordinate existing resources but cannot create an on-package coherent memory fabric on unrelated hardware. [AMD MI300A architecture](https://instinct.docs.amd.com/projects/amdgpu-docs/en/docs-30.10.2/gpu-partitioning/mi300a/overview.html)

**EOIP use:** choose CPU/GPU/NPU for each supported DAG stage, account for transfers, reserve memory, batch work, bound queues and fall back only when permitted. CPU-only hosts still run the scheduler and workflows.

**Boundary:** no fabricated unified memory, automatic multi-host distribution, bandwidth guarantees, or assumption that the fastest individual kernel gives the fastest complete workflow.

### 2.8 LPU: Local language processing

Groq's LPU is a vendor-specific chip/compiler architecture. Local language-model inference is available through software such as llama.cpp; its Python bindings support local model paths and multiple build backends. This does not reproduce Groq's hardware characteristics. [Groq LPU explanation](https://groq.com/blog/the-groq-lpu-explained), [llama.cpp](https://github.com/ggml-org/llama.cpp), [llama-cpp-python](https://llama-cpp-python.readthedocs.io/en/latest/)

**EOIP use:** deterministic tokenization/chunking/retrieval first; approved local-model extraction, grounded summaries and query proposals only when a task needs them. Maintain useful graph and query functionality with no LLM installed.

**Boundary:** no Groq-compatible binaries, cloud inference requirement, universal language understanding, guaranteed determinism of generated text, unrestricted tool execution or autonomous database changes.

### 2.9 IPU: Graph intelligence

Graphcore's Poplar documentation distinguishes physical IPUs, an IPU model and host-CPU execution. It explicitly describes limitations of the model, including numerical and random-number behavior. Those facilities are not a general substitute for hardware validation. [Poplar programs and targets](https://docs.graphcore.ai/projects/poplar-user-guide/en/latest/poplar_programs.html), [IPUModel reference](https://docs.graphcore.ai/projects/poplar-api/en/latest/poplar/profiling/IPUModel.html)

**EOIP use:** sparse graph features, connected components, bounded neighborhood aggregation, graph embeddings and optional approved graph-model inference. SciPy already provides graph algorithms; preserve source node IDs and authorization while translating graph snapshots to arrays. [SciPy connected components](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.connected_components.html)

**Boundary:** no Poplar SDK dependency or Graphcore binary compatibility by default. "Intelligence" is not evidence of factual correctness; similarity, cluster membership and model scores remain derived claims.

### 2.10 VPU: Vision/document processing

Here VPU means the user's visual-processing category, implemented as **vision and document processing**. The abbreviation can also mean video-processing hardware in other contexts. Intel's Movidius materials describe specialized vision hardware; historical examples are not a recommendation to purchase or support those devices today. [Intel VPU overview](https://www.intel.com/content/www/us/en/developer/topic-technology/edge-5g/hardware/vision-accelerator-movidius-vpu.html)

OpenCV exposes Python image/video operations, and Tesseract can emit text and positional OCR formats. These provide practical local building blocks. [OpenCV Python tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html), [Tesseract output formats](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html)

**EOIP use:** document image preprocessing, OCR, layout evidence, image duplicate detection and bounded uploaded-video keyframes. Preserve page, bounding-box, transform and timestamp provenance; OCR is fallible and does not create verified graph facts automatically.

**Boundary:** no surveillance platform, face identification, real-time camera requirement, universal codec support, inferred identity or compulsory visual-language model.

## 3. Recommended Technical Choices

These are engineering decisions inferred from the research and repository, not claims made by the cited vendors.

| Concern | Baseline decision | Optional extension / restriction |
|---|---|---|
| Public contracts and orchestration | Python 3.11+, existing Pydantic/FastAPI/CLI conventions | Native libraries behind typed adapters; no custom hardware compiler |
| Array/sparse work | Existing `numerics` extra: NumPy/SciPy; sklearn where already appropriate | Explicit dtype, shape, memory and thread budgets |
| Portable inference | ONNX Runtime CPU, installed as an optional processing extra | Separate provider environments prevent conflicting ONNX runtime distributions |
| GPU qualification | First candidate: ONNX DirectML on an eligible Windows GPU | Restricted supported ONNX operator subset; additional CUDA/MIGraphX profiles require separate policy and qualification |
| NPU qualification | First candidate: OpenVINO on a supported Intel NPU | QNN/other vendors later through the same adapter contract, never inferred from device marketing names |
| Local LLM | Approved local GGUF artifact through llama-cpp-python in an isolated worker | Existing local-model service can be adapted after endpoint and isolation hardening; not an alternate ungoverned path |
| Vision/OCR | Headless OpenCV plus approved local Tesseract executable and language data | PDF rasterization only through the existing qualified parser, or a separately reviewed dependency |
| Quantum | Qiskit Aer CPU in an optional isolated research environment | No cloud QPU connector in this scope |
| Job authority | Reuse and harden owned job/authority abstractions | Local SQLite profile is not multi-host SaaS qualification |
| Models/data | Offline imports, immutable digests, license inventory, model cards and task evaluation | No runtime download, training on tenant data or model telemetry |

DirectML's documented restrictions include sequential execution and disabled memory-pattern optimization for its ONNX sessions. Follow the exact pinned release's constraints rather than copying CPU session settings. The documentation also discusses Windows ML as the Windows distribution direction; that deserves a separate compatibility decision, not a hidden switch in the first Python adapter. [DirectML provider](https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html)

OpenVINO's supported-device matrix is version-specific. Installation, compilation, permitted shapes and actual execution must be tested on the target device. Unknown hardware remains unqualified. [OpenVINO supported devices](https://docs.openvino.ai/2026/documentation/compatibility-and-support/supported-devices.html)

## 4. Security and LLM Data Exposure

"Local model" is not a complete security property. The process can still read excess files, write prompts to logs, reuse another tenant's cache, execute unsafe loaders or make outbound connections.

ONNX explicitly warns that models can exhaust compute/memory even when their format is valid. Transformers documentation separates offline loading from remote-code and unsafe-serialization risks. These are reasons for process isolation and artifact qualification, not reasons to trust any local model file automatically. [ONNX model validation](https://onnxruntime.ai/docs/), [Transformers security policy](https://github.com/huggingface/transformers/blob/main/SECURITY.md), [Offline loading](https://huggingface.co/docs/transformers/main/installation)

Required design:

1. No outbound model, embedding, OCR or telemetry calls in this programme's initial execution profiles.
2. Offline artifact acquisition is a separate, administrator-operated workflow with no tenant data in the staging environment.
3. The control plane authorizes and minimizes data before dispatch. Workers receive only approved input artifacts, not the whole database or repository.
4. Model processes have no connector credentials, cloud credentials, broad home-directory mounts, arbitrary tools or writable model files.
5. Enforce isolation outside Python, then verify it with observed deny tests for TCP, UDP, DNS, IPv4/IPv6, proxies, child processes and malicious model/parser behavior.
6. Preserve classification, tenant, provenance and access restrictions on embeddings, features, caches, logs and outputs.
7. Treat prompts, retrieved text and model outputs as untrusted data. Hashes and delimiters do not grant authority or prove resistance to prompt injection.
8. Never claim mathematically guaranteed zero leakage or perfect detection. State the measured boundary, tested threats, deployment prerequisites and residual risks.

## 5. EOIP Source Alignment and Prerequisites

This is targeted integration inspection, not a claim to have audited the entire repository or every route. Source findings below must be rechecked against the implementation branch.

| Finding | Evidence inspected | Required response |
|---|---|---|
| CPU numerical dependencies already exist; advanced tiers are not declared/qualified by the install guide | [Project configuration](pyproject.toml), [Neural installation](docs/install-neural.md), [Runtime](packages/eoip/neural/runtime.py) | Extend optional profiles; keep the graph core usable without numerical/model packages |
| Current compliance policy rejects CUDA/NVIDIA distribution dependencies | [CPU-only compliance](tests/compliance/test_no_cuda_packages.py) | Resolve ADR-H16 explicitly before any CUDA-bearing artifact; do not delete the gate or conceal dependencies in a new lock-file location |
| Capability states exist, but registration qualification reads mutable local ledger statuses; `require` permits supported-unqualified entries | [Capability registry](packages/eoip/capabilities/registry.py) | Add independently verified, profile-bound evidence promotion and production admission; do not treat an edited ledger as proof |
| Probe timeout parameter does not itself impose a timeout on synchronous probe functions | [Capability registry](packages/eoip/capabilities/registry.py) | Run bounded probes outside request paths and contain hangs |
| Local model availability is based on model configuration; generation dispatches to a configurable HTTP URL | [Local model provider](packages/eoip/models/provider.py) | A configured name is not successful execution or trusted locality; validate endpoint identity/isolation or use the isolated in-process adapter |
| Network monitor records calls supplied to it and considers broad private-name/address patterns internal | [Privacy governance](packages/eoip/privacy/governance.py) | Do not treat it as a socket firewall or independent packet observation |
| REVA scrubbing is shallow and fencing is a delimited hash wrapper | [REVA egress](reva/core/egress_gate.py) | Structured recursive minimization plus external containment; delimiters are not an enforcement boundary |
| Gateway records DLP findings, while the inspected call path specifically denies canary hits; approvals are supplied identifiers and transport is injectable | [Egress gateway](packages/eoip/egress/gateway.py) | Do not assume all findings block, approvals are verified, or every call is routed through the gateway; qualify effective behavior and deny compute-worker egress regardless |
| Durable job code exists alongside the original file queue | [Jobs](packages/eoip/jobs.py), [Worker](apps/worker/main.py) | Select the actual supported execution path explicitly; reconcile state/result contracts rather than build a third unrelated queue |
| Tenant-filtered pending claim can return another tenant's job | [Durable claim implementation](packages/eoip/jobs.py) | Security prerequisite: parenthesize the whole eligible-state predicate before tenant filtering; enforce non-null trusted tenant scope and test other queue operations |
| Commit accepts a `result` argument but the inspected method does not persist it; lease checks need further expiry review | [Durable commit](packages/eoip/jobs.py) | Persist result/receipt references transactionally; qualify fencing, expiry, cancellation and recovery, not just method signatures |
| Tool names such as similarity/community currently include bounded graph-read handlers | [Agent tool registry](packages/eoip/agents/tools.py) | Register actual compute contracts separately; do not claim algorithm implementation from the presence of a similarly named tool |
| Two frontends and a suite extraction plan exist | [Suite plan](docs/EOIP-suite-architecture-plan.md) | Use the selected deployed frontend and shared client; no third frontend or ten new portals |

### 5.1 Isolated queue observation

A temporary SQLite database was created using the current `DurableJobStore`. A pending job for `tenant-a` was submitted; `claim_job(..., tenant_id="tenant-b")` returned that job. The successful repeat probe printed:

```json
{
  "probe": "tenant-scoped-pending-claim",
  "requested_tenant": "tenant-b",
  "claimed_tenant": "tenant-a",
  "cross_tenant_claim_observed": true
}
```

The SQL construction places `AND tenant_id = ?` after an ungrouped `OR`, so it does not constrain the first `PENDING` branch. This is a demonstrated method-level issue, not a claim that an external API exploit was demonstrated. The probe used disposable synthetic data, changed no project source, and the temporary database was removed. It is a planning observation, not a retained release-qualification evidence bundle. The implementation plan requires a reproducible regression and broader queue audit.

## 6. Fit to Application Intent

| EOIP workflow | Useful profiles | Why this is worth building |
|---|---|---|
| Connector ingestion and schema validation | DPU, CPU | Deterministic processing, provenance and bounded resource use |
| Entity resolution and similarity | GPU, TPU, NPU, IPU | CPU-capable numerical scoring with optional measured acceleration |
| Graph impact, clustering and recommendations | CPU, IPU | Authorized graph features, explainable baselines and derived results |
| Document ingestion | VPU, DPU, NPU | Local OCR with page-level evidence and optional evaluated models |
| Grounded answers and query assistance | LPU, CPU | Deterministic retrieval first; optional constrained local generation |
| Reports and analytics | CPU, GPU, APU | Reproducible snapshots, aggregation and fair scheduling |
| Agent workflows | APU plus authorized operators | Typed bounded tools using existing approvals and budgets |
| Optimization research | QPU plus classical CPU baseline | Controlled experiments, explicitly not a production dependency |

The highest practical value is likely CPU/DPU orchestration, privacy, numerical inference and document handling. That is an engineering prioritization, not a measured ROI claim. Build all ten scoped profiles, but deliver quantum research last and keep it disabled by default.

## 7. What Remains Unverified

- No GPU, NPU, quantum simulator, local LLM or vision benchmark was executed for this research.
- No dependency set, wheelhouse, model artifact or driver combination was installed or qualified.
- Hardware availability, customer deployment OS, model licenses and representative customer workloads are not established.
- Vendor documentation describes possibilities and constraints, not EOIP performance or security certification.
- No existing module is upgraded to "complete" by this document. A source reference is navigation; only independently checked runtime evidence can close a requirement.

The requirements turn these unknowns into explicit discovery, selection and qualification tasks. A coding agent must report blocked evidence honestly rather than invent hardware, hashes, measurements or user approvals.
