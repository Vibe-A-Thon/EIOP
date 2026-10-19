# EOIP / KGF Processing Units Requirements

Version: 1.0 proposed specification. Date: 2026-10-19.

Status: **NOT IMPLEMENTED OR QUALIFIED BY THIS DOCUMENT.** These are acceptance obligations for future work, not an assertion that EOIP currently has ten software processors.

Read together: [Research and source findings](processing-units-research.md), [Implementation plan](processing-units-implementation-plan.md), [Suite architecture](docs/EOIP-suite-architecture-plan.md), [Neural installation policy](docs/install-neural.md), [Licensing](LICENSING.md).

## 1. Objective and Honest Product Boundary

Implement **EOIP Processing Runtime**, a Python-first, local-first, policy-governed execution layer for knowledge ingestion, graph analysis, numerical inference, document understanding, reporting and controlled agent tools.

All ten requested categories MUST have a functional, bounded software profile that can run on a CPU with its declared optional dependencies and artifacts. Compatible GPU/NPU hardware MAY accelerate qualified operations. This is not a requirement to simulate every instruction of every vendor's chip or to reproduce physical hardware performance.

The following meanings are binding:

| Alias | User-facing capability | What completion means |
|---|---|---|
| CPU | General processing | Deterministic, bounded Python/native-library operators |
| GPU | Vector and parallel analytics | CPU numerical reference plus optional qualified GPU execution |
| TPU | Tensor processing | Portable tensor operations and bounded model graphs, not a Google TPU clone |
| NPU | Neural inference | CPU model execution plus optional qualified physical NPU routing |
| DPU | Data preparation | Streaming/batched validation, transforms and provenance, not a SmartNIC |
| QPU | Quantum simulation | Resource-bounded classical simulation, always labelled simulated |
| APU | Heterogeneous scheduling | Coordinated execution on available devices, not fabricated shared-memory silicon |
| LPU | Local language processing | Deterministic text work plus optional approved local LLM tasks |
| IPU | Graph intelligence | Sparse graph features and approved graph-model inference, not a Graphcore emulator |
| VPU | Vision and document processing | Local image/OCR/keyframe workflows with evidence |

The research explains the feasibility and limitations using primary sources. Tensor execution can be portable through [ONNX execution providers](https://onnxruntime.ai/docs/execution-providers/); quantum simulation is classical and resource-limited through [Qiskit Aer](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html). Neither establishes EOIP qualification.

### 1.1 Explicit exclusions

No physical TPU/QPU/DPU/IPU/LPU emulation fidelity guarantee; no arbitrary CUDA/PTX/Poplar binaries; no new operating system, custom compiler or hand-written cryptography; no public compute marketplace; no customer-supplied Python/native kernels; no foundation-model training; no remote LLM/embedding/OCR service; no surveillance or biometric identity recognition; no claim of quantum advantage, real-time guarantees, zero energy cost or universal acceleration.

Exclusions are visible product boundaries, not silently waived requirements. Additional adapters can be proposed later, but their existence is not necessary to close the finite v1 scope below.

### 1.2 Completion language

The word **complete** applies only to a versioned requirement set, deployment profile, operator catalog and evidence bundle. It never means every possible hardware platform or future feature. Documentation cannot guarantee that any coding agent will achieve completion without actual execution, review, artifacts and target hardware.

`MUST` is required. `MAY` is optional and must be labelled unavailable when absent. A requirement containing a production gate cannot be closed with a stub, mock-only test, source path, screenshot alone, import probe, fabricated benchmark or developer declaration.

## 2. Decisions and Unresolved Inputs

### 2.1 Binding implementation decisions

1. Start inside the existing repository under a proposed `packages/eoip/processing/` domain. Do not create ten repositories or ten web applications.
2. Preserve the current API, graph, agent and worker contracts. Integrate through owned interfaces rather than importing `apps.api` into library modules.
3. Keep the core install independent of numerical, quantum, OCR and LLM packages. Use existing `numerics` dependencies where possible; declare additional optional profiles explicitly.
4. Python owns contracts, authorization handoff, orchestration, adapters, scripts and evidence verification. NumPy/SciPy, ONNX Runtime, OpenCV/Tesseract, Qiskit Aer and a vetted local LLM engine own their established numerical/domain algorithms.
5. Use deterministic code before an LLM. LLMs are not used for scheduling, access control, cryptography, calculations with exact answers, schema validation or deciding whether a release passed.
6. CPU execution is the reference. Initial optional hardware adapters are Windows DirectML GPU and supported Intel OpenVINO NPU. Other providers are extensions, not implicit support promises.
7. Shared arithmetic operators are implemented once and reused by GPU/TPU/NPU/IPU profiles. Aliases do not justify duplicate engines or fake chip inventories.
8. External inference is prohibited in v1, including "fallback to cloud." Missing local capacity returns a truthful error or an explicitly selected deterministic alternative.
9. Runtime operator calls are read/derive only. Publishing derived graph facts uses a separate existing governed mutation path with review where required.
10. The CPU-only ADR-H16 distribution policy remains in force until an explicit successor decision approves narrowly scoped accelerator artifacts. Never remove its test merely to make a build green.

### 2.2 Inputs that must be established, not guessed

| Input | How the implementation agent must resolve it | Behavior until resolved |
|---|---|---|
| Target OS/architecture/CPU resources | Produce a redacted discovery manifest on the actual qualification host | Do not advertise that host as supported |
| GPU/NPU model, runtime and driver | Enumerate locally, run bounded execution probes and retain provider traces | CPU baseline remains usable; accelerator stays unqualified |
| Exact dependency versions and hashes | Resolve reviewed compatible releases into per-profile locks; execute clean/offline installation | Do not invent package hashes or copy a vendor support matrix as EOIP evidence |
| LLM/embedding/vision model artifact | Select a task-appropriate artifact; record origin, immutable digest, license, tokenizer/preprocessor and evaluation | Model-dependent operators unavailable; deterministic operators still work |
| Tesseract binary/language assets and codecs | Package or approve exact executable/data digests; test on each supported OS | OCR/codec capability unavailable, never empty success |
| Tenant classification and permission mapping | Reuse actual identity/privacy contracts and record reviewed mapping | Deny unknown labels or absent trusted tenant context |
| Production evidence storage and retention | Configure the existing artifact/audit owner, encryption and signed acceptance policy | No production qualification from `.audit-scratch` alone |
| SaaS coordination/isolation | Qualify durable shared authority and tenant worker isolation | Restrict to the explicitly qualified one-host profile |

The agent has authority to propose technical selections and generate candidate lock/model manifests. It must not invent business approval, licensing rights, deployment access or hardware results. An unresolved item blocks the affected gate only; it does not justify fake completion or prevent independent CPU work.

## 3. Existing Integration Points

These are real source locations, not evidence of completed integration:

| Existing owner | Reuse and required adaptation |
|---|---|
| [Project dependencies](pyproject.toml) | Optional profile definitions, package boundaries and scripts |
| [Neural runtime](packages/eoip/neural/runtime.py) | Reconcile existing tier discovery with actual execution qualification; retain compatibility |
| [Capability model](packages/eoip/capabilities/model.py), [registry](packages/eoip/capabilities/registry.py) | Preserve capability states; add verified per-profile receipts and production admission |
| [Jobs](packages/eoip/jobs.py), [worker](apps/worker/main.py) | Harden tenant claims, result persistence, leases, cancellation and bounded processing dispatch |
| [Graph store](packages/eoip/graph/store.py), [traversal](packages/eoip/graph/traversal.py) | Authorized snapshots and provenance; no direct graph mutation from kernels |
| [Agent tools](packages/eoip/agents/tools.py), [runtime](packages/eoip/agents/runtime.py) | Typed, budgeted processing tools; actual authorization cannot depend on a tool name |
| [Local model provider](packages/eoip/models/provider.py), [embeddings](packages/eoip/models/embeddings.py) | Route existing and new processing tasks through one local-only policy and artifact lifecycle |
| [Privacy classification](packages/eoip/privacy/classification.py), [governance](packages/eoip/privacy/governance.py) | Inherited labels, access limits and independent network enforcement |
| [Egress gateway](packages/eoip/egress/gateway.py), [provider manifests](packages/eoip/egress/provider.py) | Reuse declared data-flow concepts; compute profiles remain deny-egress |
| [REVA egress](reva/core/egress_gate.py) | No bypass through shallow scrubbing or prompt delimiters |
| [API composition](apps/api/main.py), [CLI](packages/eoip/cli.py) | Add versioned commands/routes without assuming they already exist |
| [MCP](apps/mcp/main.py), [VS Code manifest](apps/vscode-extension/package.json) | Shared governed client behavior, no direct worker/model access |
| [Default web app](apps/web/package.json), [other frontend](frontend/package.json) | Select via the existing suite migration decision; no third UI |

The [research prerequisites](processing-units-research.md) include a demonstrated tenant-scoped job-claim defect. Fix and verify that before processing jobs can use the durable queue. Other listed source observations require focused regression checks, not a claim that every deployment is exploitable.

## 4. Foundation Requirements

| ID | Required behavior | Observable acceptance |
|---|---|---|
| PUR-FND-001 | Expose exactly the ten logical profile aliases above with descriptive names and explicit physical/simulated execution metadata. | A CPU-only inventory displays all ten catalog entries without claiming ten devices; unavailable extras have reasons. |
| PUR-FND-002 | Use one shared processing domain, operator catalog and adapter protocol. | A tensor operation invoked through two applicable profiles uses the same versioned implementation and produces equivalent outputs. |
| PUR-FND-003 | Core graph/query startup must not import or require optional compute libraries. | A clean core-only environment starts and performs a real graph read while all optional packages are absent. |
| PUR-FND-004 | Maintain CPU reference implementations for every v1 operator, including model/simulator operators in their optional environments. | The complete v1 operator matrix executes on CPU; absent artifacts are not counted as passes. |
| PUR-FND-005 | Preserve proprietary first-party licensing and third-party notices; inventory native runtimes, models, fonts/language data and codecs separately. | Distributable artifact scan matches SBOM and license notices; no unreviewed redistribution. |
| PUR-FND-006 | Reconcile ADR-H16 and neural-tier documentation before releasing any optional accelerator artifact. | Reviewed decision, unchanged core CPU compliance and new profile-specific distribution checks all agree. |
| PUR-FND-007 | Keep configuration schema-versioned, validated, auditable and reversible. Unknown fields and unsafe combinations fail closed. | Invalid configuration cannot enable external inference or elevate a capability; rollback restores the previous effective revision. |
| PUR-FND-008 | Keep new processing state and contracts compatible with future suite extraction into the platform owner. | Import-boundary checks and an installed-package API/worker run succeed without source-tree-only imports. |

## 5. Contracts and Data Model

### 5.1 Common typed objects

Implement Pydantic models with `extra="forbid"`. Public request fields cannot assert trusted identity, approvals, qualification or measured device use.

| Object | Required fields and invariants |
|---|---|
| `ExecutionContext` | Server-issued tenant/workspace/principal IDs, authorization snapshot/revision, correlation/causation IDs, policy revision, expiry, permitted operator IDs and output scopes; never taken on trust from request JSON |
| `ArtifactRef` | Opaque tenant-scoped ID, immutable version, media type, byte length, content digest, classification/labels, producer and provenance references; resolve via artifact owner, never arbitrary URLs/paths |
| `OperatorSpec` | Stable ID/version, accepted profiles, input/parameter/output schemas, bounds, side effects, determinism class, reference implementation, supported precision, backend constraints, dependency/model requirements |
| `ProcessingRequest` | Schema version, logical unit, operator/version, named artifact inputs, validated parameters, optional model reference, execution preference, bounded budgets and client correlation ID |
| `ExecutionPlan` | Validated operator DAG, immutable input/model/policy versions, device candidates, cost/resource estimates with estimation method, required permissions, fallback policy, plan digest and expiry |
| `DeviceDescriptor` | Physical device type/vendor/model, redacted stable local identifier, OS/driver/runtime versions, usable resources, supported profiles and last probe; do not expose hardware serials to ordinary tenants |
| `ProviderQualification` | Exact operator/model/profile/platform/version tuple, independent evidence references, verification time/expiry and supported limits; library import success is not qualification |
| `JobRecord` | Durable ID/context/plan digest, status, attempts, lease/fencing token, deadlines, cancel state, progress, result/receipt references and sanitized failure |
| `ExecutionReceipt` | Input/output digests, operator/model/policy/build/environment identities, requested/actual provider/device, placement/fallback details, seed/determinism, timing/resource observations, outcome, provenance and external verifier references |
| `ModelManifest` | Immutable weights/tokenizer/preprocessor digests, format, permitted tasks/shapes/opsets, runtime versions, license/redistribution decision, evaluation/split IDs, minimum resource estimate, owner and promotion state |

### 5.2 Contract requirements

| ID | Required behavior | Observable acceptance |
|---|---|---|
| PUR-CON-001 | Publish schemas for all objects above and version independently of internal Python classes. | Valid/invalid conformance fixtures run through both API and installed SDK; breaking schema changes fail compatibility checks. |
| PUR-CON-002 | Accept only registered operator IDs and typed parameters; prohibit module names, pickle, Python expressions, shell commands and custom executable kernels. | Malicious payload corpus is rejected before process launch or artifact reads. |
| PUR-CON-003 | Resolve inputs by authorized artifact/snapshot references; enforce tenant, workspace, revision and classification at submission and execution. | Forged references, expired grants and cross-tenant inputs produce denial with no worker data access. |
| PUR-CON-004 | Use canonical serialization for plan/request hashes and idempotency binding, including nested data and versions. | Key-order changes preserve a digest; changed nested values, policy or model invalidate it. |
| PUR-CON-005 | Distinguish `cpu_only`, `prefer_accelerator`, `require_gpu` and `require_npu`; preference never overrides policy. | Required-device jobs fail when the actual graph would fall back; preferred-device jobs disclose each fallback. |
| PUR-CON-006 | Define dtype, layout, shape and null/NaN/Inf/overflow handling per operator. | Boundary fixtures produce documented errors or results; implicit lossy conversion does not occur. |
| PUR-CON-007 | Make plan-only execution side-effect free except authorized planning/audit records. | Instrumented dry run launches no model/kernel, changes no graph and performs no network acquisition. |
| PUR-CON-008 | Persist result and receipt references atomically with successful completion and an owned publication protocol. | Killing a worker at each commit point cannot produce a successful job with missing result artifacts. |
| PUR-CON-009 | Use typed errors with safe messages and retry semantics; never return empty results to represent missing backends. | Missing dependencies, model absence, bad shapes, denied access and genuine empty results are distinguishable. |
| PUR-CON-010 | Separate job execution success, capability qualification and business-result quality. | A successful low-quality OCR/LLM result remains unqualified for its task and is not promoted into verified facts. |

### 5.3 Request example and API semantics

This is a **target contract**, not a currently callable endpoint. IDs below represent synthetic already-imported artifacts; they are not paths to create or access automatically.

```json
{
  "schema_version": "1.0",
  "logical_unit": "GPU",
  "operator_id": "vector.cosine_top_k",
  "operator_version": "1.0",
  "inputs": {
    "candidates": "artifact:fixture-candidates:v1",
    "query": "artifact:fixture-query:v1"
  },
  "parameters": {"k": 5, "zero_vector_policy": "reject"},
  "execution": {"mode": "cpu_only", "fallback": "forbid"},
  "budgets": {"deadline_seconds": 60, "memory_mib": 512, "threads": 2},
  "client_correlation_id": "qualification-vector-001"
}
```

Proposed route prefix: `/api/processing/v1`. Before implementation, verify it does not conflict with an existing route. Reuse existing authentication, CSRF/session handling and tenant resolution.

| Method and route | Behavior |
|---|---|
| `GET /capabilities` | Tenant-filtered logical units, operators, profiles, reasons and qualification references |
| `GET /devices` | Permission-filtered physical inventory; restricted device details for operators |
| `POST /plans` | Validate/estimate without executing; return plan ID/digest/expiry and applicable limits |
| `POST /jobs` | Require `Idempotency-Key`, request and matching plan digest; return `202` with durable job ID |
| `GET /jobs` | Tenant-scoped cursor pagination, bounded page size and safe status metadata |
| `GET /jobs/{job_id}` | Authorized status, progress and references; not raw input content |
| `POST /jobs/{job_id}/cancel` | Idempotent cancellation request; terminal result cannot be rewritten |
| `GET /jobs/{job_id}/result` | Reauthorize output access and issue artifact-owner response; unfinished is `409` |
| `GET /jobs/{job_id}/receipt` | Authorized redacted receipt; restricted technical evidence uses separate permission |
| `POST /profiles/{profile_id}/probes` | Privileged, bounded asynchronous probe; no arbitrary driver/runtime install |

Existing capability errors retain their established status codes: unsupported `422`, unavailable `503`, unlicensed `403`, disabled `409`. Add stable processing error codes: `INVALID_REQUEST`/`INVALID_SHAPE` (`422`), `AUTH_REQUIRED` (`401`), `POLICY_DENIED` (`403`), `NOT_FOUND` (`404`, including unauthorized artifact existence), `IDEMPOTENCY_CONFLICT`/`STALE_PLAN` (`409`), `INPUT_TOO_LARGE` (`413`), `QUOTA_EXCEEDED` (`429`), `MODEL_UNAVAILABLE`/`DEVICE_UNAVAILABLE`/`PROFILE_UNQUALIFIED` (`503`). Job outcomes additionally distinguish `DEADLINE_EXCEEDED`, `RESOURCE_EXHAUSTED`, `WORKER_LOST`, `CANCELLED`, `OUTPUT_INVALID` and `INTERNAL_ERROR`. No raw provider exception or prompt appears in a public error.

Idempotency scope is `(tenant, principal authorization scope, endpoint, key)`. Store the canonical request/plan binding and original response for at least the lifetime of the job plus 24 hours. Reuse with different input is `409`. Retries after retention expiry must be documented as new submissions, never silently represented as deduplicated.

## 6. Execution, Scheduling and Resource Safety

| ID | Required behavior | Observable acceptance |
|---|---|---|
| PUR-RUN-001 | Use the existing durable job owner with explicit processing job kinds and typed state mapping. Repair the tenant claim defect before use. | Two tenants and multiple claimers never cross scope across pending, expired, retry or cancelled states. |
| PUR-RUN-002 | Require non-null trusted tenant scope for customer jobs; privileged fleet actions use an explicit separate scope. | Missing/empty/default tenant values cannot read, claim, cancel or replay another tenant's work. |
| PUR-RUN-003 | Implement leases, expiry, monotonically increasing fencing tokens and atomic result publication. | Expired/stale workers cannot heartbeat back into authority or publish after cancellation/reclaim. |
| PUR-RUN-004 | Enforce limits outside the event loop and, for untrusted native/model workloads, outside the main API process. | A hung native operation is terminated without hanging API health or another tenant's jobs. |
| PUR-RUN-005 | Bound CPU threads, process count, RAM, disk, queue depth, input/output size and wall time before admission and during execution. | Oversized plans fail before allocation; overruns terminate and clean up without host exhaustion. |
| PUR-RUN-006 | Use deterministic topological ordering with stable node-ID tie breaks for DAGs; reject cycles and incompatible schemas. | Repeated plans have identical node order; cyclic/malformed DAGs launch no work. |
| PUR-RUN-007 | Use per-tenant fair queues and bounded concurrency; no tenant controls priority through untrusted payload fields. | Under two-tenant saturation, each eligible tenant progresses within the configured queue-age bound. |
| PUR-RUN-008 | Retry only classified transient, idempotent stages with bounded backoff; do not replay graph writes blindly. | Injected device/worker failures cause bounded attempts and one published result, not duplicate effects. |
| PUR-RUN-009 | Support cancellation for queued/running work and revoke publish authority immediately. | Cancellation wins or completion wins atomically; killed/late workers never replace a terminal result. |
| PUR-RUN-010 | Track estimates separately from measured time/memory/device placement; include model loading, transfers and compilation. | Receipts expose queue/startup/compute/transfer/end-to-end timings without claiming estimates are measurements. |
| PUR-RUN-011 | Check capability evidence freshness and runtime health again at dispatch; no sticky success after driver/model/policy changes. | Version changes or failed probes invalidate admission until requalification. |
| PUR-RUN-012 | Provide crash/restart recovery and artifact reconciliation using the owned persistence layer. | Restart tests identify abandoned work, reject stale fences and leave no successful result with missing or mismatched artifacts. |

### 6.1 Proposed initial safety defaults

These are conservative configurable product defaults, **not measured host capacity or performance promises**. Administrators may lower them; increases require policy validation and profile requalification.

| Limit | Initial default |
|---|---|
| General job wall time | 60 seconds; model/research profiles up to 300 seconds only by declared profile |
| General job memory | 512 MiB hard process budget including runtime overhead; insufficient budget rejects the job |
| Worker concurrency | One active job per tenant; two active jobs per local worker only when admission proves resources suffice |
| Thread budget | `max(1, min(2, usable_cpu_count))`; propagate to BLAS/OpenMP/provider runtimes |
| Queued jobs | 100 per tenant, 500 per local deployment; reject excess with retry information |
| DAG | 32 nodes, 64 edges; fan-out charged against aggregate resources |
| Public control JSON | 256 KiB; tensor/document contents use artifact references |
| General input/output artifact | 64 MiB input and 64 MiB output unless a reviewed operator profile sets lower/higher bounds |
| QPU | 20 statevector qubits or 10 density-matrix qubits; 4,096 shots; 1,000 gates; explicit method, no automatic method expansion |
| QPU state workspace | At least `4 * raw_state_bytes` plus measured interpreter/library overhead, all within the process limit; never treat the factor as a proof of maximum usage |
| Vision | 16 megapixels per decoded image, 50 pages per job, 60 seconds of uploaded video, at most 60 sampled frames and 4 million decoded pixels/frame |
| Local LLM | Default context 4,096 tokens including output allowance; output <=512 tokens; one generation per tenant; deadline <=300 seconds |
| Model memory | Explicit per-artifact peak estimate plus runtime/KV/cache overhead; no zero/unlimited default and no assumption a model fits in 512 MiB |
| Cancellation | Revoke commit authority immediately; cooperative stop grace 5 seconds, then terminate isolated worker; health gate blocks an unrecoverable device worker |
| Retry | At most two retries after the first attempt; exponential delays 1 and 2 seconds with bounded jitter; within original deadline |

Admission takes the minimum of operator, tenant, deployment and available-resource limits. The host must retain an administrator-configured reserve; unset reserve or unknown memory accounting blocks model/research production admission. A local developer may run synthetic fixtures under an explicitly non-production profile, not a falsely qualified secure profile.

### 6.2 Job state machine

Target public states are `QUEUED`, `RUNNING`, `CANCEL_REQUESTED`, `SUCCEEDED`, `FAILED`, `CANCELLED`, `TIMED_OUT`, `REJECTED` and `HELD_FOR_REVIEW`. Map these explicitly to existing internal queue states without changing unrelated clients silently. `REJECTED` represents failure before execution. Retries are attempts within one durable job, not new unlinked jobs. A terminal state is immutable except a separate authorized replay creates a new job with a parent reference. Do not cancel an already committed successful job by relabelling it cancelled.

## 7. Security, Privacy and LLM Controls

| ID | Required behavior | Observable acceptance |
|---|---|---|
| PUR-SEC-001 | Authenticate every API/SDK/MCP/agent invocation and derive tenant/workspace/grants from trusted context. | Cross-tenant and forged-context negative journeys fail before data or device access. |
| PUR-SEC-002 | Deny all model/embedding/OCR runtime internet egress, including library downloads, license callbacks and telemetry. | Independent network observation detects no permitted external connections during normal and adversarial runs. |
| PUR-SEC-003 | Enforce worker network isolation with deployment controls, not monkey-patched sockets, regexes or a self-reported byte counter. | Raw sockets, DNS/UDP, IPv6, proxies, subprocesses and redirect attempts cannot bypass the approved boundary. |
| PUR-SEC-004 | Explicitly identify the local model trust boundary. Private IPs, `.local`, `.internal` and loopback are not automatically trusted services. | A malicious local listener or reassigned destination is rejected; IPC/service identity is verified. |
| PUR-SEC-005 | Authorize and minimize input before passing it to any model; secrets/credentials never enter a prompt. | Seeded nested secrets and unnecessary fields are blocked/removed before the observed inference boundary. |
| PUR-SEC-006 | Preserve existing sensitivity labels and D0-D4 policy mapping without inventing equivalences. Derived features/embeddings inherit source restrictions. | A restricted source cannot become an unrestricted summary/vector/result through transformation. |
| PUR-SEC-007 | Validate structured payloads recursively with depth/size bounds; DLP failure or unknown classification fails closed for model input. | Nested lists/maps, encoded-content cases, scanner errors and pathological inputs do not bypass admission. |
| PUR-SEC-008 | Treat retrieved content, OCR and prompts as untrusted; prohibit instruction-driven tool, URL, file or policy escalation. | Injected instructions produce no tool/network/mutation effect and cannot alter execution permissions. |
| PUR-SEC-009 | Allow only approved immutable model/parser artifacts; no pickle, remote code, dynamic plugin installation or unreviewed ONNX custom ops. | Tampered weights, path-traversing external tensor data and executable model bundles are rejected in isolation. |
| PUR-SEC-010 | Isolate process credentials, filesystem mounts, IPC, temporary files and caches by tenant/job. | Worker probes cannot read home directories, connector secrets, another job's files or another tenant's cache. |
| PUR-SEC-011 | Reauthorize before dispatch, result download, report inclusion and graph publication; support revocation mid-job. | Revoked users cannot obtain new outputs or publish results from already queued work. |
| PUR-SEC-012 | Exclude raw prompts, documents, vectors, images and secret-bearing exceptions from ordinary logs, traces and metrics. | Canary scans across stdout/stderr, traces, errors, crash bundles and UI show no protected content. |
| PUR-SEC-013 | Use approved cryptographic/storage services for encryption, signatures and secret references. A hash alone is not confidentiality or authenticity. | Unauthorized readers cannot retrieve artifacts; forged evidence/digests fail verification and no hard-coded shared key is accepted. |
| PUR-SEC-014 | Local LLM outputs cannot authorize actions, resolve access policy or automatically become verified knowledge. | Malicious/incorrect generated SQL or graph updates remain proposals and cannot execute without the existing governed path. |
| PUR-SEC-015 | Provide global/tenant/profile kill switches that stop new admission and revoke running publish authority. | Revocation is observed across processes; a stale local cache cannot continue privileged execution. |
| PUR-SEC-016 | Document and test residual risks: privileged-host compromise, native-library vulnerabilities, inference leakage and hardware side channels. | Release security report names tested boundaries and unmitigated risks; it makes no absolute zero-leak guarantee. |

### 7.1 Required local execution boundary

Default secure deployment uses an isolated worker/container or equivalent OS sandbox with no network interface usable for outbound traffic, read-only approved runtime/model assets, a narrow input mount and a separate bounded output location. A broker outside the model process handles authorized artifact movement and job control. Do not give the model process the broker's network credentials.

For native Windows qualification, use a dedicated restricted worker identity, Windows Job Object or equivalent process-tree limits, narrowly permissioned directories/IPC and administrator-managed firewall policy. Verify effective restrictions. If the host cannot enforce them, mark secure confidential-data processing unsupported on that host; WSL/container isolation is an alternative only after verification. A `ProcessPoolExecutor` alone is not a sandbox. Linux resource limits alone are not a network sandbox either.

The existing source connector may need authorized network access. Keep connector acquisition outside the compute worker boundary; hand off classified immutable artifacts. Compute isolation does not promise the entire EOIP deployment is disconnected from every business system.

### 7.2 LLM decision policy

| Task | Default route | LLM eligibility |
|---|---|---|
| Math, checksums, sorting, aggregation, schemas, limits | Deterministic operator | Not eligible |
| Scheduling, authorization, egress, evidence acceptance | Deterministic policy/service | Not eligible |
| Exact entity lookup and known query templates | Existing graph/query services | Not eligible unless a separate language task is explicitly requested |
| Chunking/token counting | Deterministic tokenizer/text code | No generation |
| Summarization, ambiguous extraction, natural-language query proposal | Retrieval and deterministic baseline first | Approved local artifact, task policy, allowed source slice and task-quality gate required |
| Graph/ontology mutation | Existing governed command path | LLM may propose only; never grants approval |

Missing model => `MODEL_UNAVAILABLE` for a model-required task. A caller may explicitly choose an extractive/deterministic alternative; receipts and UI must call it that, not pretend an LLM ran. Data minimization and sandboxing apply even when the user owns the model host.

## 8. Artifacts, Provenance and Numerical Semantics

| ID | Required behavior | Observable acceptance |
|---|---|---|
| PUR-DAT-001 | Use immutable, tenant-scoped artifacts with atomic staging/finalization and authorized resolution. | Partial writes, traversal paths, symlinks/reparse points and cross-tenant IDs cannot become valid inputs. |
| PUR-DAT-002 | Record graph/data snapshot and input/model/operator/policy digests for every derived result. | A verifier reconstructs the authorized inputs and detects modified content or a changed model. |
| PUR-DAT-003 | Preserve row/node IDs and stable order through batch/tensor conversion, filtering and graph features. | Results map exactly back to source IDs; unauthorized/filtered nodes do not reappear by array index. |
| PUR-DAT-004 | Validate numeric shape/dtype before allocation; disallow object arrays and unsafe serialization. | Ragged, overflow, malformed compressed and huge declared-shape inputs fail safely. |
| PUR-DAT-005 | Partition caches by tenant, scope, data/policy/model/operator version and precision; invalidate on revocation. | Identical text in two tenants does not share confidential KV/result caches or access grants. |
| PUR-DAT-006 | Apply retention, deletion and legal-hold rules to inputs, outputs, temporary files, vectors and evidence. | Expiry/purge/restart drills remove eligible derived data and preserve authorized holds without misleading deletion claims. |
| PUR-DAT-007 | Distinguish observed facts, calculated features, OCR text, model predictions and simulations in provenance. | Neither a high similarity score nor a model's confidence silently changes a graph claim into verified fact. |
| PUR-DAT-008 | Make result schemas portable and bounded; binary tensors use safe numeric formats, not arbitrary Python objects. | Installed clients on supported OSes read results and reject tampered metadata/payload mismatches. |

For v1 numeric arrays use little-endian `.npy` without pickle for dense arrays and a versioned CSR bundle of numeric arrays plus JSON metadata for sparse inputs. Validate headers, dimensions, byte counts and indices before allocation. Use approved existing formats for graph snapshots/documents, preserving their owner contracts. A future Arrow adapter is optional, not a reason to add a mandatory new core dependency.

Floating CPU-reference gates use `abs(actual-reference) <= atol + rtol*abs(reference)` per element: float64 `atol=1e-10, rtol=1e-8`; float32 `atol=1e-5, rtol=1e-4` on bounded qualification fixtures. Integer/Boolean outputs are exact. Larger/ill-conditioned workloads need operator-specific bounds in their profile; do not silently relax a failed test. Quantized models require task-quality comparisons, not a blanket float tolerance. LLM text is evaluated semantically/structurally, not by cross-device exact string equality.

## 9. Unit-Specific Operator Catalog

Each row is a normative requirement. Listed operator IDs are stable v1 targets, not claims of current registration. Each must implement planning, CPU execution, safe error paths, resource enforcement, provenance and receipts from the shared sections. Hardware support is per operator, not inferred from its unit alias.

### 9.1 CPU: General processing

| ID | Operators and precise scope | Acceptance |
|---|---|---|
| PUR-CPU-001 | `records.validate`: bounded JSON records against a registered JSON Schema; return per-record paths/codes without echoing secret values. | Valid/invalid/missing/null/oversized records match a golden error manifest. |
| PUR-CPU-002 | `records.transform`: declarative select/rename/filter/cast with an allowlisted expression AST, no eval; casts fail explicitly. | Golden records including nulls and invalid casts produce exact outputs and row-level provenance. |
| PUR-CPU-003 | `records.aggregate`: count/sum/min/max/mean grouped by declared fields; explicit missing/overflow and stable ordering. | Exact integer fixtures and tolerance-checked floating fixtures; bounded high-cardinality groups fail before exhaustion. |
| PUR-CPU-004 | `records.sort_deduplicate`: stable key sort and exact-key deduplication with a declared first/last/error policy. | Same inputs yield same surviving source IDs; no approximate semantic merge. |
| PUR-CPU-005 | `graph.bounded_traverse`: reuse graph traversal over an authorized snapshot with depth/result limits and truncation markers. | Expected paths, cycles, missing nodes, unauthorized edges and truncation are independently reconciled. |

### 9.2 GPU: Vector and parallel analytics

| ID | Operators and precise scope | Acceptance |
|---|---|---|
| PUR-GPU-001 | `vector.cosine_top_k`: finite numeric candidate matrix/query, stable source-ID tie breaks, exact CPU baseline, explicit zero-vector reject/zero-score policy. | Known vectors give expected rank/scores; ties/zero rows/dimension mismatches behave as specified. |
| PUR-GPU-002 | `tensor.matmul`: 2D and bounded batched matmul using shared tensor backend; validate broadcast rules and output allocation. | Independent small analytic examples and randomized CPU-reference comparisons pass. |
| PUR-GPU-003 | `vector.reduce`: sum/mean/min/max and L2 norm along a declared axis; no unsupported precision promotion. | Empty-axis, extreme-value and normal fixtures follow the documented schema and tolerance. |
| PUR-GPU-004 | `sparse.matmul`: validated CSR-by-dense multiplication, stable row IDs, no implicit densification of the sparse input. | Sparse reference parity plus peak-memory observation; unsupported accelerator path explicitly uses CPU or rejects. |
| PUR-GPU-005 | Qualify optional GPU execution for the supported dense ONNX subset of the preceding operators, with actual placement and transfer accounting. | A physical eligible GPU runs real operations; CPU-forced, missing-device and strict-no-fallback cases are separately observed. |

### 9.3 TPU: Tensor processing

| ID | Operators and precise scope | Acceptance |
|---|---|---|
| PUR-TPU-001 | Reuse `tensor.matmul`; add `tensor.elementwise` for add/multiply/ReLU/sigmoid and `tensor.softmax` with explicit axis and stable computation. | Known outputs and bounded extreme inputs match CPU references; no duplicate arithmetic engine. |
| PUR-TPU-002 | `tensor.conv2d`: NCHW input/kernel, explicit pads/stride/dilation/groups; v1 groups=1; `tensor.pool2d`: max/average with explicit edge semantics. | Analytic small filters and ONNX CPU comparisons pass; unsupported layouts/groups rejected. |
| PUR-TPU-003 | `tensor.normalize`: L2 and layer normalization with declared axes/epsilon; `tensor.reshape`: validated element count/layout. | Zero-norm/constant arrays and reshape mistakes follow exact documented policy. |
| PUR-TPU-004 | `tensor.graph_infer`: execute an approved ONNX graph with fixed allowed opsets/shapes and no custom executable operations. | Real CPU execution and output comparison; unknown nodes/external data paths/oversized shapes are rejected. |
| PUR-TPU-005 | `model.quantization_evaluate`: evaluate an approved quantized artifact against its reference using local calibration/evaluation manifests. No automatic production promotion. | Report task metrics, numerical deltas, memory and latency; reject a worse model under the declared task threshold. |

### 9.4 NPU: Neural inference

| ID | Operators and precise scope | Acceptance |
|---|---|---|
| PUR-NPU-001 | `model.infer`: approved ONNX artifact with typed named inputs/outputs, CPU default, explicit precision and bounded batch/shape. | Actual inference on a known fixture; missing model/runtime and malformed input fail truthfully. |
| PUR-NPU-002 | `text.embed`: approved local embedding artifact/tokenizer, deterministic batching, normalization declaration and model-space version. | Same text/model yields comparable vectors; incompatible embedding spaces cannot be mixed. |
| PUR-NPU-003 | `model.classify`: approved small classifier with labels, score semantics and abstention threshold from its evaluated manifest. | Held-out task metrics beat/meet the declared baseline; scores are not falsely presented as calibrated probabilities. |
| PUR-NPU-004 | `model.batch_infer`: bounded microbatching preserving per-input IDs, errors and cancellation; no unauthorized cross-tenant batching. | Split/reordered/error batches reconcile to original items; memory remains within admission. |
| PUR-NPU-005 | Qualify Intel OpenVINO NPU as a separate optional provider for at least one approved bounded inference model. | Physical-device trace, CPU comparison, unsupported-op/shape handling and missing-driver failure are retained. |

### 9.5 DPU: Data preparation

| ID | Operators and precise scope | Acceptance |
|---|---|---|
| PUR-DPU-001 | `data.prepare_batches`: stream bounded records from an already acquired artifact, validate schema, batch by bytes/rows and preserve source offsets. | Large synthetic input uses bounded memory and downstream backpressure; no connector network call from the worker. |
| PUR-DPU-002 | `data.checksum`: approved SHA-256 content checks; `data.compress`/`data.decompress`: standard gzip with decompressed-byte, ratio and nesting limits. | Round-trip/digest parity and compressed-bomb rejection before resource exhaustion. |
| PUR-DPU-003 | `data.classify_redact`: reuse classification/DLP with bounded recursive structures and approved field policies; propagate labels. | Known secret/PII fixtures redact correctly; unknown/failed classification blocks model-bound delivery. |
| PUR-DPU-004 | `data.deduplicate`: content/key-based duplicate detection with collision-safe digest verification and tenant-scoped indexes. | Duplicates across batches/retries are identified without cross-tenant existence leakage. |
| PUR-DPU-005 | `data.ingestion_envelope`: produce typed source-event/provenance handoff with quality/rejection counts; publication uses existing ingestion owner. | Source counts reconcile to accepted/rejected/duplicate records and graph results through the real ingestion path. |

### 9.6 QPU: Quantum simulation

| ID | Operators and precise scope | Acceptance |
|---|---|---|
| PUR-QPU-001 | `quantum.simulate`: validated JSON circuit with H/X/Y/Z/S/T/RX/RY/RZ/CX/CZ gates, finite angles, declared qubit indices and end-of-circuit measurement. Compile to Qiskit; no executable circuit upload. | Bell/GHZ and rotation fixtures match analytic probabilities; unsupported gates/control flow fail before simulation. |
| PUR-QPU-002 | Support explicit statevector and density-matrix CPU methods; density mode may apply bounded depolarizing noise with probability in [0,1]. | Normalization, known noise-free cases and a declared noisy case pass tolerance checks; no real-hardware calibration claim. |
| PUR-QPU-003 | `quantum.sample`: bounded shots/seed and ordered bitstring counts with declared endianness; randomness is simulator pseudorandomness. | Counts sum to shots and seeded repeats on the pinned profile reproduce results; independent probability checks use a predeclared statistical rule. |
| PUR-QPU-004 | `quantum.expectation`: bounded sums of Pauli observables; no unrestricted matrix upload. | Known states/observables match analytic expectation values and validate Hermitian/shape constraints. |
| PUR-QPU-005 | `quantum.maxcut_experiment`: a bounded, seeded QAOA-style experiment on <=12 authorized graph vertices with p<=2 and <=50 objective evaluations, using Qiskit primitives and a standard optimizer. | Compare objective/time/resource use with exhaustive classical solution on the same graph; report failures and no claimed advantage without measurements. |
| PUR-QPU-006 | Estimate exponential memory before allocating; enforce method-specific caps and label every result `simulation=true`, `physical_qpu=false`. | Oversized request is rejected; UI/report/export cannot hide simulated status or turn a result into a production decision automatically. |

### 9.7 APU: Heterogeneous scheduling

| ID | Operators and precise scope | Acceptance |
|---|---|---|
| PUR-APU-001 | `workflow.plan`: validated typed DAG with compatible artifacts, stable ordering, aggregate budgets and no arbitrary code. | CPU-only mixed-unit DAG executes; cycles, unsupported operators and cumulative oversubscription reject. |
| PUR-APU-002 | `workflow.run`: execute approved plan via shared jobs; checkpoint completed immutable stages and report per-stage results. | Restart resumes eligible stages without duplicated effects or loss of provenance. |
| PUR-APU-003 | Select devices by policy/qualification/resources, then measured end-to-end cost including transfers; CPU default when no useful evidence exists. | Controlled selection fixtures show why a device was chosen; fake benchmark/configuration cannot grant qualification. |
| PUR-APU-004 | Reserve/release resources atomically across competing jobs; isolate tenant queues and provider/session state. | Concurrency stress never oversubscribes configured reservations or leaks results between tenants. |
| PUR-APU-005 | Enforce explicit fallback/cancellation semantics per stage and for the entire plan; never change precision/model to conceal failure. | Device loss either yields documented equivalent CPU fallback or fails; receipt records all attempted and actual providers. |

### 9.8 LPU: Local language processing

| ID | Operators and precise scope | Acceptance |
|---|---|---|
| PUR-LPU-001 | `text.chunk` and `text.tokenize`: deterministic Unicode-safe offsets, chunk IDs, overlap and pinned tokenizer identity; no model generation. | Non-ASCII and boundary fixtures reconstruct source spans; tokenizer mismatch is explicit. |
| PUR-LPU-002 | `text.retrieve`: reuse authorized lexical/graph retrieval and optional approved embeddings; return source spans and ranking method. | Known corpus recall and cross-tenant denial are measured; fabricated citations cannot enter the result. |
| PUR-LPU-003 | `text.extract`: local model output constrained to a registered schema, evidence spans for extracted fields and explicit abstention. | Held-out labelled examples, unsupported-field and injection cases meet the task gate; invalid JSON is failure, not parsed by eval. |
| PUR-LPU-004 | `text.summarize_grounded`: approved local model, bounded retrieved context, resolvable citations, uncertainty and no automatic fact promotion. | Every cited source exists and is authorized; independently judged supported-claim/abstention thresholds pass. |
| PUR-LPU-005 | `query.propose`: generate only a structured read-query proposal validated by the existing parser/planner; do not execute generated text automatically. | Mutation/injection/unbounded-query attempts fail; a separate authorized user action runs an accepted read plan. |
| PUR-LPU-006 | Enforce token/time/memory limits, tenant-isolated KV caches, model identity and local-only execution; cancelled generation cannot publish. | Real local inference and no-egress measurements pass with missing-model, overflow and cancellation negatives. |

### 9.9 IPU: Graph intelligence

| ID | Operators and precise scope | Acceptance |
|---|---|---|
| PUR-IPU-001 | `graph.to_csr`: export an authorized bounded immutable graph snapshot with stable node/edge IDs, direction and weight rules. | Round-trip node/edge reconciliation; no authorization bypass during graph-to-array conversion. |
| PUR-IPU-002 | `graph.components`: weak/strong components using SciPy; `graph.shortest_paths`: bounded source set and supported weight rules, not unrestricted all-pairs allocation. | Golden graphs include isolated vertices, directed cycles and invalid weights; results match independent expected sets/paths. |
| PUR-IPU-003 | `graph.aggregate_features`: one or bounded repeated sparse neighbor sum/mean steps with explicit self-loop/normalization semantics. | Small analytic graph outputs match; high-degree/memory limits and missing features are handled explicitly. |
| PUR-IPU-004 | `graph.cluster_features`: approved sklearn baseline over authorized features with seed, algorithm/version and quality diagnostics; clusters are hypotheses. | Known fixture grouping plus stability/quality report; no semantic certainty from cluster IDs. |
| PUR-IPU-005 | `graph.model_infer`: approved bounded graph-model artifact through shared CPU neural backend, preserving model-space and provenance. | Real inference, held-out task evaluation, CPU baseline and missing-model denial; never substitute random vectors or zero scores. |

### 9.10 VPU: Vision and document processing

| ID | Operators and precise scope | Acceptance |
|---|---|---|
| PUR-VPU-001 | `vision.preprocess`: allowlisted image decode, orientation, resize, grayscale/threshold and deskew through OpenCV; preserve coordinate transforms. | Known image fixtures and inverse-coordinate checks pass; decompression bombs/unsupported formats are rejected. |
| PUR-VPU-002 | `vision.ocr`: approved local Tesseract/language bundle; text plus page/box/confidence fields, engine identity and raw-source reference. | Real rendered documents produce measured CER and valid boxes; missing language/binary returns unavailable. |
| PUR-VPU-003 | `vision.layout_evidence`: deterministic grouping of OCR lines/blocks and evidence coordinates; no unsupported table/chart understanding claim. | Annotated page fixtures verify reading-order and coordinate mapping; ambiguous layouts are marked uncertain. |
| PUR-VPU-004 | `vision.duplicate_score`: exact pixel/content identity plus optional documented perceptual hash distance; near-duplicates remain candidates. | Known identical/resized/distinct images produce measured distances without automatic entity merging. |
| PUR-VPU-005 | `vision.keyframes`: bounded uploaded-video decode, explicit sampling interval/timestamps and provenance; no network camera/URL acquisition. | Known short video yields expected count/time bounds; malformed/unsupported codec and over-limit inputs fail safely. |
| PUR-VPU-006 | `vision.model_infer`: approved ONNX image classifier/detector using shared inference with explicit preprocessing/label/box schema. | Actual local model output and held-out accuracy/coordinate tests pass; acceleration only through qualified providers. |

## 10. Product and Suite Integration

| ID | Required behavior | Observable acceptance |
|---|---|---|
| PUR-INT-001 | Implement the versioned API in section 5 using existing auth/tenant middleware; no unauthenticated diagnostic bypass. | Browser/API jobs use the actual worker and persisted artifacts with authorized results and negative access tests. |
| PUR-INT-002 | Extend the existing CLI with `processing capabilities`, `devices`, `plan`, `submit`, `status`, `cancel`, `receipt` and `verify-evidence`. | Installed CLI reaches the same governed service; no alternate unrestricted local execution path. |
| PUR-INT-003 | Integrate DPU/VPU outputs with the real ingestion pipeline and preserve source/provenance/quality records. | A document/record artifact becomes reviewable knowledge through existing ingestion, with reconciled counts. |
| PUR-INT-004 | Integrate vector/IPU results into authorized query/explorer/report workflows using immutable snapshot references. | End-to-end user workflow shows derived evidence and unchanged source facts; revoked access remains denied. |
| PUR-INT-005 | Register processing agent tools with typed contracts, delegated scope, budgets and cancellation; never direct arbitrary code execution. | A real agent invocation cannot exceed operator/tenant/action permissions; result/receipt links are resolvable. |
| PUR-INT-006 | MCP and VS Code clients consume the same policy-checked API; do not grant an external AI client raw source data by default. | Read capability/status metadata safely; sensitive results require explicit existing authorization and channel policy. |
| PUR-INT-007 | Add Operations views for physical resources, logical capabilities, jobs, limits, errors and actual execution placement. | A CPU-only session and a qualified accelerated session show truthful distinct states. |
| PUR-INT-008 | Add Configuration/Model Lab controls for profiles, artifact import/promotion and quotas using existing design/auth patterns. | Invalid/unauthorized changes fail server-side; effective revision, validation and rollback are visible. |
| PUR-INT-009 | Add Governance evidence/provenance views and workflow-specific actions in Integration/Query/Reports rather than ten unrelated dashboards. | A user follows input -> plan -> job -> result -> receipt -> source without copying secrets between apps. |
| PUR-INT-010 | Preserve feature usability without LLM/GPU/NPU and expose loading/empty/denied/unavailable/stale/partial/error/cancelled states accessibly. | Keyboard, narrow desktop/mobile, reduced-motion and screen-reader journeys succeed without clipping or misleading success states. |

### 10.1 UI rules

Use existing shared tokens, icon library, API client, navigation and data-table patterns. Show "Vector analytics - CPU" or "Neural inference - Intel NPU" rather than fictional chip graphics. Distinguish actual physical devices from logical capabilities. Put detailed placement/evidence in expandable diagnostics, not the primary task form. Use concise status text, tooltips, keyboard focus, restrained transitions and reduced-motion support. Never send tensor/model data to a browser merely to draw utilization visuals.

Users choose a task, inputs and policy-permitted execution preference; advanced tuning is progressive disclosure. No manual entry of secrets, driver paths or Python code in ordinary job screens. New suite repositories remain under the existing `AvyukthiAI` organization plan; library ownership belongs to the platform, not separate CPU/GPU repositories.

## 11. Packaging and Operations

| ID | Required behavior | Observable acceptance |
|---|---|---|
| PUR-OPS-001 | Ship explicit core/numerical/ONNX/text/vision/quantum profiles with per-OS locks and offline wheel/artifact manifests. | Clean install, uninstall, missing-extra and offline reinstall execute real workload fixtures. |
| PUR-OPS-002 | Separate mutually incompatible accelerator runtimes into owned worker environments; do not install CPU/GPU variants over each other blindly. | Dependency checks and actual session creation pass in each declared profile; core environment remains CPU-only. |
| PUR-OPS-003 | Provide secure model/data import, quarantine, evaluation, promotion and rollback workflows. | Tampered/incompatible models never become active; rollback restores previous version with reproducible receipts. |
| PUR-OPS-004 | Expose safe metrics for queue age, throughput, errors, memory, stage latency, provider placement and fallback. | Metrics reconcile with job records without high-cardinality secret-bearing labels. |
| PUR-OPS-005 | Document customer-installed Windows/Linux single-host deployment separately from SaaS/multi-worker deployment. | Each advertised profile has its own recovery/isolation/capacity evidence; unsupported topology is rejected. |
| PUR-OPS-006 | Maintain migration/backup/restore contracts for job state, configuration, model manifests and evidence. | Old/new version compatibility and downgrade/restore drills preserve references and authorization. |
| PUR-OPS-007 | Fail safely under disk full, dependency corruption, model/device loss, queue saturation and broker outage. | Fault injection yields bounded failure/recovery with no silent precision downgrade or data loss claims. |
| PUR-OPS-008 | Publish operator catalog, support matrix, limits, security/runbooks, model cards and customer-facing notices with each release. | Documentation generated from the actual release manifest agrees with runtime capabilities and observed evidence. |

Target qualification profiles:

| Profile | Required scope | Default state before evidence |
|---|---|---|
| `PU-CORE` | Python control plane and deterministic records/traversal; Windows and Linux qualification separately | Unqualified |
| `PU-NUM` | NumPy/SciPy/sklearn CPU vector/tensor/graph operators | Unqualified |
| `PU-ONNX` | ONNX CPU inference plus approved embedding/classifier/graph/vision artifacts | Unqualified; each model independently gated |
| `PU-TEXT` | CPU local GGUF inference and deterministic text operators | Model operations unavailable without approved artifact |
| `PU-VISION` | CPU OpenCV/Tesseract with approved binary/language/codec set | Unqualified |
| `PU-QUANTUM` | CPU Qiskit Aer simulation | Disabled by default, research-only |
| `PU-GPU-DML` | Windows DirectML adapter for declared dense ONNX operators | Unavailable/unqualified until physical-device evidence |
| `PU-NPU-OV` | Supported Intel OpenVINO NPU adapter for declared models | Unavailable/unqualified until physical-device evidence |

Do not confuse these profiles with the existing neural tiers; publish a mapping. CPU-only installations can qualify all ten functional categories by installing the relevant optional CPU profiles. That does not qualify physical GPU or NPU claims. ARM/macOS/additional GPU or NPU vendors remain explicit future support work unless independently added and accepted.

## 12. Verification, Evidence and Definition of Done

| ID | Required behavior | Observable acceptance |
|---|---|---|
| PUR-VER-001 | Maintain a machine-readable registry of every `PUR-*` requirement, operator, task, gate and evidence reference. | A validator detects missing IDs, duplicates, unassigned requirements and unsupported completion states. |
| PUR-VER-002 | Run real API -> auth -> job -> worker -> library/model -> artifact -> UI/client journeys. | No mocks stand in for the component claimed qualified; captured outputs and state are independently reconciled. |
| PUR-VER-003 | Compare deterministic outputs against independent analytic/golden references and declared tolerances. | Deliberately broken operators are rejected by the verifier, not merely by their own health report. |
| PUR-VER-004 | Evaluate model tasks on held-out, licensed/local fixtures with baselines, split identities and failure analysis. | Toy inference smoke tests cannot close business-quality requirements; no train/evaluation leakage. |
| PUR-VER-005 | Prove no-egress and data minimization at an independently observed worker/model boundary. | Blocked attack attempts plus normal inference are captured outside the model process; self-reported zero bytes is insufficient. |
| PUR-VER-006 | Test tenant isolation, grants, cache scope, output access, revocation and channel permissions under concurrency. | Adversarial cross-tenant runs reveal no unauthorized output or execution. |
| PUR-VER-007 | Qualify actual hardware placement on each advertised accelerator tuple. | Real provider traces/counters and result parity accompany the exact driver/runtime/device; absence is BLOCKED, not PASS. |
| PUR-VER-008 | Execute crash, stale lease, duplicate submit, cancel/commit race, disk pressure and resource-overrun drills. | Persisted effects and cleanup match the state-machine contract after restart. |
| PUR-VER-009 | Benchmark reproducibly, including cold/warm/model-load/transfer costs, hardware details and raw samples. | Speedup compares equal work/precision/quality with recorded CPU baseline; no fabricated TOPS or unqualified SLA. |
| PUR-VER-010 | Verify accessibility/responsiveness and truthful states in the actual deployed frontend. | Screenshots plus interaction/accessibility results and API/worker correlation establish behavior; screenshots alone do not. |
| PUR-VER-011 | Verify packaged/offline installation and license/security inventory for every advertised release profile. | A clean machine/environment executes the shipped artifact without hidden caches or runtime downloads. |
| PUR-VER-012 | Independent acceptance validates evidence content, environment binding, signatures/digests and negative-case coverage before capability promotion. | Missing/tampered/stale/self-declared receipts cannot produce `SUPPORTED_QUALIFIED`. |

### 12.1 Required evidence bundle

Store acceptance evidence in the configured owned artifact store with access control and retention. `.audit-scratch` can hold local working material but is not a durable customer release authority and need not be committed to Git. Commit sanitized schemas, manifests, checks and approved references instead.

Each retained run must contain:

- Run ID, UTC start/end, full source revision plus dirty-diff digest if applicable, distribution/container digest and dependency lock identities.
- OS/architecture, CPU and optional device/runtime/driver information, resource limits and isolation-policy version.
- Exact selected requirement/operator/profile/model IDs; immutable input fixtures with licenses and digests.
- Commands/runner version, exit codes, safe stdout/stderr, real job/API records and independently read output artifacts.
- Expected results, actual results, numerical/task-quality metrics, tolerances and per-case verdicts.
- Network-boundary observations and data-flow/minimization evidence for confidential/model profiles.
- Fault/negative-case records, state before/after recovery and artifact/graph-effect reconciliation.
- UI screenshots/video/accessibility results when a UI claim is made, tied to the same backend/job evidence.
- Verifier identity/version, verification result and an acceptance signature or existing trusted attestation mechanism.
- Known limitations, failed/blocked cases, expiry/requalification triggers and reviewer decision.

Hashes detect changes but do not establish who produced evidence or that its observation was independent. Do not let the execution worker sign its own success into production qualification without the existing independent verifier/authority.

### 12.2 Evidence status and coverage accounting

Use `NOT_STARTED`, `IN_PROGRESS`, `IMPLEMENTED_UNVERIFIED`, `VERIFIED`, `ACCEPTED`, `BLOCKED` and `FAILED` for requirement tracking. These are not replacements for existing runtime `CapabilityState` values. Only accepted, profile-bound, current evidence can qualify production admission. A running but unqualified library is not a production pass.

Report separate fractions: CPU functional requirements accepted; integration/security requirements accepted; optional hardware tuples accepted; business-model tasks accepted. State denominators and exclusions. Do not inflate percentage completion by counting files, lines, test names, skipped tests, mocks, disabled features or a removed requirement.

### 12.3 Minimum task-quality gates

These are initial qualification thresholds for the versioned reference fixture set, not universal customer accuracy promises. A task profile may require stronger domain-specific gates before customer deployment.

| Task | Minimum gate |
|---|---|
| Deterministic records/graph/identity mappings | 100% expected outcomes across declared positive and negative fixtures |
| Numeric kernels | All declared analytic/reference cases satisfy section 8 tolerances; no nonfinite unexplained result |
| Embedding retrieval | Held-out relevance set with >=100 labelled queries; report recall@5 and nDCG@10; recall@5 >=0.80 and no regression against selected lexical baseline without reviewed justification |
| Classification/graph/image model | >=100 held-out labelled examples with represented classes; macro-F1 >=0.80 and >= deterministic/majority baseline; calibration claim requires a separate calibration evaluation |
| Structured extraction | >=100 held-out fields/examples; schema validity 100%; field-level precision >=0.95; recall >=0.80; unsupported fields abstain |
| Grounded summaries | >=50 held-out tasks; citations resolve/authorize 100%; reviewed supported-claim precision >=0.95; all fixture unanswerable cases abstain; human or separately reviewed ground truth, not self-grading by the same model |
| Read-query proposals | >=50 known schema tasks; no mutation/unbounded query admitted; >=0.90 result-equivalence on the answerable fixture subset after separately authorized execution |
| OCR | At least 20 licensed/synthetic pages across supported layouts and declared languages; CER <=0.05 for the declared clean reference subset; degraded/layout subsets reported separately, not hidden |
| Quantum | Analytic small-state comparisons at float64 tolerance; shot counts tested against a declared probability/confidence rule; optimizer objective never exceeds the independently checked exact optimum |
| Isolation/security | Zero successful bypasses in the declared threat/negative corpus; residual untested threats explicitly documented |

Freeze fixtures, metric implementations and thresholds before evaluating the candidate. A small reference corpus qualifies only that declared task domain. Customer/domain expansion needs additional evidence, not a blanket quality claim.

## 13. Change and Acceptance Authority

Existing ASPEII/action-safety, privacy, neural qualification, graph authority and suite requirements remain binding. This specification adds processing capability requirements; it does not authorize bypassing approvals, replacing existing registries or lowering another programme's gate.

Use an ADR for scope/provider changes, a versioned manifest for dependency/model changes, and fresh evidence for behavior changes. All requirement rows and normative contract/default/security sections form the acceptance surface. The implementation plan maps them to work packages, executable verification and release gates.

The intended outcome is useful, measurable EOIP functionality on ordinary hardware, with honest optional acceleration and enforceable data boundaries, not marketing names attached to empty wrappers.
