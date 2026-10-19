# EOIP / KGF Processing Units Implementation Plan

Version: 1.0 proposed delivery plan. Date: 2026-10-19.

Status: Planning artifact. **No processing operator, accelerator, security boundary or completion claim is established by this file.**

Normative companion: [processing-units-requirements.md](processing-units-requirements.md). Rationale, primary research and targeted source findings: [processing-units-research.md](processing-units-research.md).

## 1. Instructions to the Implementing Agent

Read all three processing documents before editing code. Then inspect the current branch and the relevant existing owners. The source observations in the research are a starting point, not a substitute for re-reading changing code.

Implement the finite functional scope for all ten aliases: CPU, GPU, TPU, NPU, DPU, QPU, APU, LPU, IPU and VPU. Do not interpret this as permission to create ten hardware emulators, rewrite EOIP, upload tenant data to an LLM or declare performance equivalence with physical chips.

Use Python for orchestration, adapters, configuration, qualification scripts and evidence verification. Use established libraries for their mathematical/domain engines. Do not ask an LLM to perform numeric calculations, policy decisions, evidence acceptance or scheduling when code can do them deterministically.

For every change:

1. Read the owning code and adjacent tests; record the required behavior and failure case.
2. Add a regression or executable acceptance scenario that would fail without the change.
3. Implement the smallest owned change; preserve unrelated user work and backward compatibility.
4. Run unit/contract tests, then the real runtime journey for the claim being made.
5. Collect independently observed outputs, failures, resource/network evidence and state reconciliation.
6. Have a separate verifier validate the bundle. Only then request acceptance/promotion.

Do not mark a requirement complete because a file, class, route, mocked test, test name, screenshot or ledger entry exists. Never edit an acceptance status to compensate for missing hardware, models, deployment access or failed measurements.

## 2. Dependency Order and Ownership

All new paths below are **proposed implementation targets** unless linked as existing files. Check for collisions before creation. Reuse an existing owner when it already provides the required behavior; do not create duplicate stores, registries or policy engines.

| Area | Target ownership |
|---|---|
| Public processing objects and adapter protocols | `packages/eoip/processing/contracts.py`, `interfaces.py` |
| Operator metadata and dispatch | `packages/eoip/processing/catalog.py`, `service.py` |
| Planning, budgets and device selection | `packages/eoip/processing/planner.py`, `resources.py`, `devices.py` |
| CPU/numerical/ONNX/local-text/vision/quantum adapters | `packages/eoip/processing/backends/` |
| Pure operator adapters | `packages/eoip/processing/operators/` grouped by domain, not duplicated for each chip name |
| Authorization, artifact and job integration | Existing owners via narrow adapters in `packages/eoip/processing/` |
| API router and CLI integration | `packages/eoip/processing/router.py`; extend [API composition](apps/api/main.py) and [CLI](packages/eoip/cli.py) |
| Worker isolation and execution | Extend [worker](apps/worker/main.py); isolated processing entry point only where required |
| Evidence collection/checks | `scripts/processing/` using existing evidence/artifact authority |
| Contract schemas and manifests | `schemas/processing/`, `config/processing/`, `docs/processing/` |
| Tests | `tests/processing/unit/`, `contract/`, `integration/`, `security/`, `acceptance/` and existing owner tests |
| UI | Selected existing frontend's owned Operations/Configuration/Model Lab/Governance modules |
| Future suite repository | Platform-owned package in the `AvyukthiAI` organization; portals consume versioned API/client contracts |

Do not put runtime data, models, credentials, tenant documents or large evidence captures into Git. Put versioned schemas, small synthetic fixtures, scripts, locks and sanitized release manifests into Git. Keep working evidence in configured local storage or `.audit-scratch`; retain accepted evidence in the protected artifact store.

### 2.1 Work package dependency table

| Package | Deliverable | Depends on | Closure gates |
|---|---|---|---|
| PU-W00 | Baseline, decisions, traceability and threat model | None | G01 |
| PU-W01 | Typed contracts, catalog and validation | W00 | G02 |
| PU-W02 | Tenant/artifact/privacy integration | W01 | G03 |
| PU-W03 | Durable jobs, results, cancellation and recovery | W01, W02 | G04 |
| PU-W04 | Sandboxed worker and no-egress boundary | W02, W03 | G05, G23 |
| PU-W05 | Discovery, runtime profiles and verified capability admission | W01, W04 | G06 |
| PU-W06 | CPU and DPU operators | W02-W05 | G07 |
| PU-W07 | Shared CPU vector/sparse backend | W01, W04-W06 | G08 |
| PU-W08 | Tensor/ONNX graph execution | W05, W07 | G09 |
| PU-W09 | Model lifecycle, embeddings and neural inference | W02, W04, W08 | G10 |
| PU-W10 | Graph intelligence and graph-model integration | W06-W09 | G11 |
| PU-W11 | Vision/OCR/keyframe integration | W04, W06, W09 | G12 |
| PU-W12 | Deterministic text and private local LLM | W04, W06, W09 | G13 |
| PU-W13 | Bounded quantum simulation/research | W04, W05, W07 | G14 |
| PU-W14 | Heterogeneous DAG planning/execution | W03, W05-W13 | G15 |
| PU-W15 | API/CLI and real ingestion/query/report integration | W03; incrementally W06-W14 | G16 |
| PU-W16 | Suite UI integration and accessibility | W15 | G17 |
| PU-W17 | Agent/MCP/VS Code integration | W15, existing channel identity gates | G18 |
| PU-W18 | Optional GPU and NPU physical-device qualification | W05, W08, W09, W14; policy/hardware available | G19 |
| PU-W19 | Packaging, migration, deployment and runbooks | W06-W18 for selected release profiles | G20, G21 |
| PU-W20 | Independent full acceptance and release promotion | All packages applicable to release scope | G22, G24; all other applicable gates |

An incremental CPU release is allowed only with an explicit reduced release manifest and honest outstanding requirements. It is not "100% of this programme." W18 cannot be counted complete with mock devices or skipped hardware tests.

## 3. Work Packages

### PU-W00: Establish the Baseline

**Requirements:** PUR-FND-001 through PUR-FND-008; PUR-VER-001; all normative scope/decision sections.

Actions:

1. Record source revision, dirty files without exposing secrets, Python version, supported deployment entry points and the actual worker/queue composition. Do not overwrite parallel development.
2. Read [pyproject](pyproject.toml), [neural installation](docs/install-neural.md), [neural runtime](packages/eoip/neural/runtime.py), [CPU compliance](tests/compliance/test_no_cuda_packages.py), [suite plan](docs/EOIP-suite-architecture-plan.md) and [multi-repository setup](eopisuite/multi/docs/README.md).
3. Create a machine-readable requirement registry from every normative `PUR-*` row. Add contract/default/security-section obligations, operator IDs, owner, package, gate, profile applicability and initial `NOT_STARTED` status.
4. Record ADRs for functional-profile naming, CPU reference behavior, optional hardware distribution policy, supported platform matrix, sandbox boundaries and evidence authority. A proposal is not an approval.
5. Produce a threat model covering malicious tenants, imported models/documents, native parsers, compromised worker, confused deputy, stale grants, cached data, outbound network, artifact substitution and evidence forgery.
6. Capture a baseline of relevant existing tests. Read failures before changing expectations. Inventory implemented behavior separately from qualification evidence.

**Acceptance:** G01 requires reviewed decisions, a complete parseable registry, recorded unknowns and explicit supported/non-supported topology. No installation or performance claim is made at this stage.

### PU-W01: Freeze Contracts Before Implementing Backends

**Requirements:** PUR-CON-001 through PUR-CON-010; PUR-DAT-003, PUR-DAT-004, PUR-DAT-008; PUR-FND-002, PUR-FND-007.

Actions:

1. Implement the common objects from requirements section 5 and JSON Schemas. Separate public input from trusted `ExecutionContext` and measured receipt fields.
2. Define all operator schemas, with parameter names, units, bounds, defaults, shape rules, error codes and result schemas. Register all ten aliases even when implementations are unavailable.
3. Implement canonical nested request/plan hashing using the existing canonicalization dependency. Reject nonfinite JSON numbers and ambiguous datetime/decimal serialization.
4. Add adapter methods: `describe()`, bounded `probe(context)`, `estimate(spec, inputs, params)`, `execute(plan, artifact_reader, artifact_writer, cancellation)` and `close()`. These are protocol contracts; never expose module loading or arbitrary callables to API clients.
5. Add plan expiry and binding to exact policy/input/model/operator revisions. A job submission reauthorizes and compares the plan binding; stale plans return `STALE_PLAN`.
6. Implement error mapping and distinguish unsupported/unavailable/disabled/unlicensed/unqualified from valid empty output.

Contract details that must not be left implicit:

| Domain | Required parameter decisions |
|---|---|
| Records | Schema ID/version; case-sensitive field paths; null/missing distinction; stable order; cast failure policy; exact-key dedup survivor |
| Vectors | Floating dtype; row IDs; normalization declaration; `k`; stable tie order; zero-vector policy; no NaN/Inf |
| Tensors | Layout/axes; batch broadcasting; shape bounds; pads/stride/dilation; groups=1; epsilon; output byte estimate |
| Sparse graph | CSR sorted indices and duplicate-edge policy; node-ID map; direction; edge weighting; missing-feature policy |
| Models | Model/tokenizer/preprocessor versions; input/output names; label map; batch/shape limits; abstention/score semantics |
| Text | UTF-8/source character offsets; pinned tokenizer; chunk size/overlap units; source-span citation schema |
| Vision | Allowed media types; decoded pixels; EXIF orientation; transform matrices; box coordinate system; OCR languages; frame timestamps |
| Quantum | Gate schema; qubit order and displayed bitstring endianness; seed; shots; method; noise; observable schema and resource estimate |
| DAG | Named input/output ports; immutable dependency references; ordering; cancellation/failure propagation; aggregate budgets |

**Acceptance:** G02 runs schema fuzzing and installed-client/API conformance. Hand-written DTO files with no request validation do not close this package.

### PU-W02: Secure Context and Artifact Handoff

**Requirements:** PUR-SEC-001, PUR-SEC-005 through PUR-SEC-007, PUR-SEC-010 through PUR-SEC-014; PUR-DAT-001 through PUR-DAT-008; PUR-CON-003.

Actions:

1. Reuse existing principal/tenant resolution; require a trusted non-empty context. No request field, query string or `X-Tenant` value may grant scope without existing authorization.
2. Implement an artifact-owner adapter for immutable input/result staging. Validate digest/media type/size and authorization before worker access; avoid a duplicate blob store.
3. Use per-job restricted directories or equivalent object-store scope. Reject path traversal, absolute paths, symlink/reparse-point escapes and ONNX external-data references outside the approved bundle.
4. Propagate source labels and classifications through tensors, embeddings, images, summaries and receipts. Resolve the existing D0-D4/tag mapping explicitly; do not infer that an absent tag means public.
5. Recursively minimize model input from registered schemas. Secret-bearing/unknown fields fail closed or are removed by approved deterministic policy; retain only safe audit descriptions of the transformation.
6. Define cache keys and retention/hold/purge behavior, including abandoned staging files. Reauthorize downloads and report projections after grant changes.

**Acceptance:** G03 uses two real tenant contexts, nested secret fixtures, revoked grants and malformed artifacts. Independent artifact enumeration confirms no cross-tenant read, write, cache reuse or orphaned publicly accessible result.

### PU-W03: Harden the Owned Job Engine

**Requirements:** PUR-RUN-001 through PUR-RUN-003, PUR-RUN-008, PUR-RUN-009, PUR-RUN-012; PUR-CON-008; PUR-OPS-006.

Inspect [jobs](packages/eoip/jobs.py), [durable job tests](tests/integration/test_durable_jobs.py) and the actual [worker](apps/worker/main.py) before editing. Do not assume the API currently uses `DurableJobStore` merely because the class exists.

Actions:

1. Add a failing regression: submit tenant A's pending job, then claim using tenant B's scope. Fix the whole eligible-state predicate to be grouped before tenant filtering. Test both `PENDING` and expired `RUNNING` branches.
2. Audit get/list/claim/checkpoint/heartbeat/fail/cancel/replay/outbox paths for non-null tenant requirements, authorized worker identity, job kind, lease expiry, fence and terminal state. Reject an expired lease even before another worker reclaims it.
3. Add versioned persistence for result/receipt references. The current `commit_job(result=...)` signature is not proof of persistence. Use transactional metadata/outbox plus staged artifacts and reconciliation; do not assert cross-store atomicity without a protocol.
4. Preserve old queue consumers while adding processing state mappings. Avoid silently changing legacy DLQ replay behavior; processing replay creates a separately linked job through the new contract.
5. Implement idempotency storage/unique constraints, bounded retries, cancellation races and immediate fence revocation. `cancel(SUCCEEDED)` returns terminal status unchanged.
6. Close database connections explicitly and validate Windows file-handle cleanup. A context-managed SQLite transaction is not automatically connection closure.
7. Test concurrent separate processes, not just sequential calls named "race." Kill workers after claim, before/after artifact finalization, before/after commit and during outbox publication.

**Acceptance:** G04 independently reads persisted jobs/artifacts/effects after restart. A stale worker cannot publish; every successful processing job has a readable matching result/receipt; abandoned artifacts are reconciled. SaaS/multi-host qualification remains blocked until its shared-authority profile passes equivalent tests.

### PU-W04: Worker Isolation and No-Egress Enforcement

**Requirements:** PUR-SEC-002 through PUR-SEC-004, PUR-SEC-008 through PUR-SEC-010, PUR-SEC-012, PUR-SEC-013, PUR-SEC-015, PUR-SEC-016; PUR-RUN-004, PUR-RUN-005; PUR-VER-005.

Actions:

1. Implement a broker/worker split: broker resolves authorized inputs and job authority; isolated worker receives scoped input/output handles and no connector/cloud credentials.
2. Provide one verifiable secure deployment profile before accepting confidential-data jobs. Linux container/network-namespace controls or Windows restricted identity/firewall/job-object controls must be effective, not merely configured in a sample file.
3. Enforce process-tree memory/CPU/disk/deadline limits, read-only runtime/model mounts, bounded output, restricted temporary storage and sanitized environment variables. Clear proxy/cloud/token variables.
4. Disable runtime downloads, update checks and telemetry. Network-deny controls remain mandatory even if libraries expose offline flags.
5. Implement model input inspection at the broker boundary and independent network observation outside the model process. Do not treat `NetworkSocketMonitor` self-reports, REVA delimiters or a scanner's "clean" verdict as complete isolation.
6. Test malicious document/model bundles and a controlled hostile fixture executable in a separate security test harness. Production operator APIs must never expose this harness or arbitrary executable upload.
7. Add kill-switch propagation and audit. On policy revocation, revoke publish authority first, stop/kill the worker next and retain only permitted diagnostics.

**Acceptance:** G05 and G23 include normal inference plus direct sockets, DNS/UDP, IPv6, proxy, subprocess, localhost impersonation and file/cache exfiltration attempts. A fake "zero bytes" counter is insufficient. Document the exact boundary and residual risk.

### PU-W05: Discover Providers and Admit Only Qualified Execution

**Requirements:** PUR-FND-001, PUR-FND-003, PUR-FND-004, PUR-FND-006; PUR-RUN-010, PUR-RUN-011; PUR-CON-005; PUR-VER-007, PUR-VER-012.

Actions:

1. Extend the existing capability registry rather than creating a competing production truth source. Keep its six existing capability states; store execution health, qualification and authorization as distinct facts.
2. Correct the qualification path so a mutable `ACCEPTED` string or missing receipt cannot establish production qualification. Require an independently verified artifact bound to the exact profile/operator/model/platform tuple.
3. Ensure production processing admission rejects supported-but-unqualified providers. An explicitly marked synthetic developer profile may run tests; it cannot serve confidential customer jobs or grant production status.
4. Implement bounded out-of-process discovery/probes. A `timeout_s` argument without timeout enforcement is not sufficient. Do not enumerate model paths or hardware serials into ordinary tenant responses.
5. Detect CPU resources and optional devices without importing every optional package at application startup. Separate "package installed," "device found," "execution succeeded," "task quality accepted" and "production enabled."
6. Requalify on runtime/driver/model/operator/policy changes and failed health probes. Never let refreshed evidence override an explicit disabled/unlicensed state.

**Acceptance:** G06 intentionally edits ledger statuses, removes evidence, changes a model hash, hangs a probe and simulates device loss. Each produces the correct unqualified/unavailable state and admission decision, with unchanged core graph startup.

### PU-W06: Deterministic CPU and Data Preparation

**Requirements:** PUR-CPU-001 through PUR-CPU-005; PUR-DPU-001 through PUR-DPU-005.

Actions:

1. Implement records validation/transform/aggregate/sort/dedup and bounded traversal using existing validators/graph services. Allowlisted expressions are a typed AST, not Python `eval` or string-built SQL.
2. Implement streaming batch preparation from acquired artifacts. Bound row size, batch bytes, total accepted bytes and group cardinality; apply backpressure rather than retaining the full stream.
3. Use standard hashing and gzip with decompressed limits. Verify duplicate candidates by content/keys, not an unchecked hash match alone.
4. Connect classification/redaction and source-event envelopes to existing ingestion. Return per-row safe error codes, accepted/rejected/duplicate counts and stable offsets.
5. Run an ingestion journey with valid/invalid/duplicate/classified synthetic records. Reconcile source totals, queued batches, graph records and rejected artifacts.

**Acceptance:** G07 requires exact expected results, bounded memory under a generated large stream, compressed-bomb denial, tenant isolation and independently reconciled ingestion effects. None of these operators needs an LLM.

### PU-W07: Shared CPU Numerical Backend

**Requirements:** PUR-GPU-001 through PUR-GPU-004; PUR-DAT-003, PUR-DAT-004; numerical semantics in requirements section 8.

Actions:

1. Reuse the existing `numerics` extra and qualification approach. Implement typed dense/CSR readers that reject object arrays and unsafe loads.
2. Implement cosine top-k, shared matmul, reductions and sparse-dense multiplication through NumPy/SciPy. Bound temporary/output allocation before invoking native routines.
3. Define deterministic tie/order behavior and zero-vector handling. Preserve source IDs, dtype and policy labels through batch splits.
4. Set thread budgets before native runtime initialization; measure worker count times native thread count to prevent oversubscription.
5. Build analytic fixtures and a second small scalar reference oracle for tests, plus randomized property cases. Do not duplicate optimized production algorithms in Python.

**Acceptance:** G08 executes real kernels on CPU, independently compares results and records process peak memory. Sparse cases must not densify unexpectedly. Hardware acceleration is not needed to close the CPU subset; PUR-GPU-005 remains W18.

### PU-W08: Tensor and ONNX Graph Execution

**Requirements:** PUR-TPU-001 through PUR-TPU-005; PUR-CON-006; PUR-SEC-009.

Actions:

1. Add a reviewed optional ONNX/ONNX Runtime CPU environment with exact package/native dependency locks. Keep core imports clean.
2. Implement the declared tensor kernels; reuse matmul/reductions from W07. Use ONNX CPU for convolution/model graph operations rather than designing a neural compiler.
3. Construct tiny known-answer ONNX models in test fixtures using the supported ONNX APIs. These qualify runtime mechanics only, not business intelligence.
4. Restrict opsets, operators, shape expansion and external tensor data. Inspect models inside quarantine before execution; runtime format validation does not prevent resource abuse.
5. Implement quantization evaluation over separately approved reference/quantized artifacts. Store both identities, held-out metrics and full end-to-end costs; no automatic promotion.

**Acceptance:** G09 includes known-answer graph execution, invalid/custom-op models, malicious external paths, oversized shapes, numerical parity and quantization rejection when quality degrades. No TPU hardware claim is permitted.

### PU-W09: Model Lifecycle and Neural Tasks

**Requirements:** PUR-NPU-001 through PUR-NPU-004; PUR-OPS-003; PUR-VER-004; model requirements shared with IPU/VPU/LPU.

Actions:

1. Implement immutable model manifests and quarantine/import/promote/rollback commands through existing artifact and authority owners. Never make a runtime network download the installation path.
2. Select at least one real CPU-capable artifact for each required embedding, classifier, graph-model and vision task. Record exact upstream revision, file hashes, license, tokenizer/preprocessor, training/evaluation provenance and intended domain. Do not invent hashes in documentation.
3. Separate fixture-generated model smoke tests from task-quality evaluation. Freeze held-out data and metric code before selecting/passing candidates.
4. Implement inference, embeddings, classifier abstention and microbatching using shared ONNX execution. Make provider/session state tenant-safe and bounded.
5. Update existing model/embedding callers to the common policy and lifecycle without silently changing their public results. Replace configuration-only "available" claims with the appropriate discovered/healthy/qualified state.
6. Validate rollback and incompatible embedding-space migrations. Never compare or reuse embeddings from different models as if they shared a space.

**Acceptance:** G10 needs actual model outputs and the requirements' held-out quality gates. Model selection/license/evaluation failures block only affected tasks; they are not replaced by random/zero vectors or fabricated classifiers. PUR-NPU-005 remains W18.

### PU-W10: Graph Intelligence

**Requirements:** PUR-IPU-001 through PUR-IPU-005; PUR-CPU-005; PUR-DAT-007.

Actions:

1. Export a bounded authorized graph snapshot into validated CSR, retaining canonical IDs, direction and weight semantics. Empty and isolated-node cases are legitimate.
2. Use SciPy components/shortest-path operations with bounded source sets. Reject negative-weight configurations that violate the selected algorithm's contract.
3. Add feature aggregation through sparse kernels; specify self-loops, normalization, missing features and hop count.
4. Use a selected existing sklearn clustering baseline, pinned seed and manifest parameters. Report diagnostics and uncertainty rather than "discovered truth."
5. Execute a real approved graph-model artifact through the shared neural backend; present results as derived predictions with held-out evaluation and source references.

**Acceptance:** G11 verifies graph/array round-trip counts and exact small graphs, then real task evaluation. A tool called `community` or `similarity` that only reads graph entities does not satisfy this package.

### PU-W11: Vision and Documents

**Requirements:** PUR-VPU-001 through PUR-VPU-006; PUR-INT-003.

Actions:

1. Package approved headless OpenCV, Tesseract executable/language data and supported codecs. Resolve binary licenses and platform availability; avoid unreviewed PDF/codec dependencies.
2. Implement decoded-pixel/page/frame bounds before expensive processing, with isolated parsers. Preserve orientation/resize/deskew transforms and source artifact identity.
3. Run actual OCR to a structured intermediate representation, then map boxes/text/confidence to source coordinates. Missing OCR is `unavailable`, not an empty document.
4. Implement deterministic layout grouping and exact/perceptual duplicate scoring. Table/chart semantics outside tested capability are uncertain/unsupported.
5. Decode only uploaded approved video artifacts; enforce duration/frame/pixel limits. Never accept a camera/HTTP URL as a worker input.
6. Integrate an approved vision model via W09 and the existing ingestion/review workflow. Keep OCR/model predictions distinct from reviewed facts.

**Acceptance:** G12 uses real images/documents/video, OCR character-error metrics, box-coordinate oracles, malformed media and missing-language cases, plus actual downstream provenance navigation.

### PU-W12: Deterministic Text and Local Language Models

**Requirements:** PUR-LPU-001 through PUR-LPU-006; PUR-SEC-005, PUR-SEC-008, PUR-SEC-014.

Actions:

1. Build deterministic Unicode-aware chunking/tokenization and authorized retrieval first. Confirm useful behavior with the LLM package and model absent.
2. Select a small, legally usable, CPU-capable local GGUF model and pinned tokenizer/template. The exact artifact is an implementation selection with recorded evidence, not a guessed universal model recommendation.
3. Run llama-cpp-python with the local artifact in the W04 isolated worker. CPU profile sets GPU offload off explicitly. Any existing local HTTP service must pass equivalent endpoint identity and no-egress controls before it becomes an alternative adapter.
4. Implement structured extraction, citation-bearing summaries and read-query proposals. Constrain schema, source span references and token limits; validate output outside the model process.
5. Reuse the existing read-query parser/planner. Generated query text has no execution authority; run only after a separately authorized action.
6. Add contextual injection, unknown-answer, malformed JSON, secret-bearing prompt, cancellation, over-context and cache-scope cases. Clear per-tenant generation state according to policy.

**Acceptance:** G13 needs real local generation, independently judged held-out quality, correct abstention, prompt minimization and external no-egress observations. No cloud fallback, no same-model self-grading, no claim that a hash fence prevents prompt injection.

### PU-W13: Quantum Simulation

**Requirements:** PUR-QPU-001 through PUR-QPU-006.

Actions:

1. Install Qiskit Aer CPU into the optional research profile with reviewed dependencies. Do not add CUDA transitively or depend on cloud quantum accounts.
2. Validate JSON circuit/observable schemas and compile via Qiskit APIs. Implement only the allowlisted gates, methods, noise and measurements from the requirements.
3. Estimate state, workspace and process overhead before execution. Set explicit Aer memory/thread limits and external process limits; never use unlimited or "all host memory" settings.
4. Implement simulation, sampling and expectation with declared seed and endianness. Preserve simulation labels through every API, UI and report serializer.
5. Implement the bounded MaxCut experiment using established circuit primitives and an approved standard optimizer. Compare with exhaustive enumeration for <=12 nodes and preserve both solutions/objectives/timings.
6. Use analytic Bell/GHZ/rotation/noise fixtures and a frozen statistical rule for shot results. For a Bell fixture with 4,096 shots, require only `00`/`11`, sum=4,096 and `abs(count_00-2048) <= 160`; also compare the underlying probabilities analytically. Record the seed and do not rerun until lucky.

**Acceptance:** G14 proves bounded simulation and rejection of oversized circuits. Research usefulness does not imply quantum advantage; physical QPU status remains false.

### PU-W14: Heterogeneous Workflow Scheduler

**Requirements:** PUR-APU-001 through PUR-APU-005; PUR-RUN-005 through PUR-RUN-011.

Actions:

1. Implement DAG validation and stable topological planning over the actual operator catalog. Resolve all artifact/model/policy versions before execution.
2. Add resource estimation/reservations with synchronized accounting across local workers. No stage may schedule work beyond the job/tenant/deployment envelope.
3. Use CPU when no qualified comparative measurement exists. Device selection considers queue/load, compilation, transfer and model memory, not just nominal TOPS.
4. Checkpoint immutable completed stages via the owned job store. Validate cached stage authorization, input identity and policy freshness before reuse.
5. Implement equivalent CPU fallback only for allowed modes and supported operations. Strict accelerator modes fail before or during dispatch when placement cannot be assured.
6. Observe fair progress under two-tenant contention, cancel a parent DAG mid-stage and simulate device loss. Verify descendants stop and stale outputs cannot publish.

**Acceptance:** G15 runs an actual DPU -> VPU/text -> embedding -> graph/report pipeline on CPU and later on qualified mixed hardware. A plan diagram alone is not integration.

### PU-W15: API, CLI and Business Workflows

**Requirements:** PUR-INT-001 through PUR-INT-004; PUR-CON-001 through PUR-CON-010 as public contracts.

Actions:

1. Add the section 5 API with existing auth/tenancy middleware, request limits and typed errors. Keep an explicit feature flag disabled until foundational gates pass.
2. Implement the existing `eoip` CLI subcommands as authenticated clients of the same service. Secure token storage/configuration must follow existing conventions; no token in command history by default.
3. Connect actual worker dispatch; an accepted job ID is not success until an output/receipt is persisted and retrievable.
4. Integrate data preparation/OCR with real ingestion, graph/vector features with query/explorer, and snapshot-based outputs with reports. Use existing mutation approval when publication changes knowledge.
5. Generate/export API schemas and client types. Test compatibility and correct error/status mapping across server, CLI and browser client.

**Acceptance:** G16 performs submit -> observe -> cancel/retry -> result -> receipt through a packaged service and independently reads artifacts/graph effects. It includes two tenants, expired grants and idempotency conflicts.

### PU-W16: Suite UI and Usability

**Requirements:** PUR-INT-007 through PUR-INT-010; PUR-VER-010.

Actions:

1. Follow the existing two-frontend reconciliation decision; select actual deployed routes/components before adding screens. No third frontend or ten artificial chip dashboards.
2. Operations: inventory split into logical capabilities and physical devices; jobs table, limits, progress/cancel, errors and expandable actual-provider evidence.
3. Configuration/Model Lab: approved profile settings, immutable model imports, task evaluation, promotion/rollback and effective policy versions. Sensitive administration remains permission-gated.
4. Governance: navigable result provenance, qualification details, denied execution reasons and redacted evidence links. Ingestion/query/report screens provide contextual task actions.
5. Keep advanced knobs behind progressive disclosure. Use existing icons/tokens, bounded layouts, meaningful focus order, restrained transitions and reduced-motion support.
6. Verify real loading, no-data, denied, unavailable, stale, failed, partial, cancelled and successful states at 390x844 and 1440x900, and with keyboard-only navigation. Test another narrow viewport when a layout contains wide tables.

**Acceptance:** G17 combines Playwright interactions/screenshots/accessibility checks with API/job/worker evidence. UI mocks do not close runtime requirements. A truthful CPU-only experience must be complete without a model or accelerator installed.

### PU-W17: Agents, MCP and VS Code

**Requirements:** PUR-INT-005, PUR-INT-006; PUR-SEC-001, PUR-SEC-011, PUR-SEC-014.

Actions:

1. Register narrowly scoped processing tools, initially capability/status/plan and approved bounded jobs. Reuse existing tool-contract identity and budgets.
2. Carry delegated principal/tenant/scope to the API. A deployment token or tool annotation is not proof of end-user SaaS delegation.
3. Add MCP metadata/result filtering: external AI clients must not automatically receive sensitive source data, embeddings, prompts or evidence. Channel authorization is separate from the local worker's no-egress property.
4. Add VS Code task/status/result deep links using existing extension authentication/secure storage. Do not expose worker filesystem paths or make the extension a second compute engine.
5. Verify scope attenuation, cancellation, missing model and approval-required publication through real clients. Preserve read-only behavior until action-safety gates authorize effects.

**Acceptance:** G18 uses a real tool call and API path, denies scope escalation and captures sanitized client-visible results. Agent labels or MCP tool-list output alone are insufficient.

### PU-W18: Optional Physical GPU/NPU Qualification

**Requirements:** PUR-GPU-005; PUR-NPU-005; PUR-CON-005; PUR-FND-006; PUR-VER-007, PUR-VER-009.

Actions:

1. Obtain the reviewed policy decision and actual eligible hardware. Record OS, device model, runtime build, driver and provider dependencies. Do not install drivers or change host security settings without the deployment owner's authority.
2. Build separate DirectML and OpenVINO worker environments. Follow the pinned provider's documented constraints, including DirectML session restrictions; do not infer compatibility from an import.
3. For GPU, execute the declared dense tensor/vector ONNX subset. Unsupported sparse kernels stay CPU-only and are explicitly reported.
4. For NPU, compile/run at least one approved bounded model on the physical Intel device. Inspect actual placement/fallback, not just `get_available_providers()`.
5. Compare CPU and accelerated outputs at identical input/model/precision/quality where possible. Report changes in precision and evaluate them separately rather than disguising them as speedup.
6. Test strict modes, preferred modes, unsupported operators/shapes, driver absence, exhausted memory and device loss. Verify no silent provider/model substitution.
7. Record cold start, compile/load, transfer, compute and total times with raw samples. Qualify only the tested tuple and limits.

**Acceptance:** G19 requires real-device evidence. When hardware is absent, adapter code can be `IMPLEMENTED_UNVERIFIED`; hardware requirements are `BLOCKED`. Do not mark them `ACCEPTED` to reach a percentage target.

### PU-W19: Distribution, Migration and Operations

**Requirements:** PUR-OPS-001 through PUR-OPS-008; PUR-FND-005; PUR-VER-011.

Actions:

1. Produce profile-specific dependency locks, native/model asset manifests, SBOM and third-party notices. CPU-only core tests must inspect actual distributable artifacts, not merely a limited set of filename patterns.
2. Build an offline wheelhouse/artifact bundle in a clean staging environment with no tenant data. Installation/run phases must succeed with external networking blocked.
3. Package customer-installed Windows/Linux single-host profiles separately from any qualified multi-worker SaaS topology. A shared SQLite/network volume is not multi-host qualification.
4. Add health/readiness checks that distinguish degraded optional profiles from core outage. Record safe metrics for queue age, resource use, provider fallback, failures and job durations.
5. Implement versioned job/config/model/evidence migrations with backup/restore and rollback instructions. Validate old records before migration; never destructively rewrite a user's database as a test.
6. Publish setup, support matrix, operator catalog, model cards, privacy boundary, threat model, capacity guidance, recovery and troubleshooting guides under `docs/processing/` and link them from the appropriate existing READMEs after implementation.
7. Test disk full, corrupt/missing model, broker outage, migration failure and rollback from the shipped artifact.

**Acceptance:** G20/G21 install and operate actual release artifacts in clean/offline environments and recover them. A Dockerfile, lock file or runbook path alone proves nothing about its successful use.

### PU-W20: Independent Acceptance and Promotion

**Requirements:** PUR-VER-001 through PUR-VER-012 and all unclosed requirements.

Actions:

1. Freeze release scope, source/distribution/model/profile identities, fixture versions and acceptance thresholds before the final run.
2. Run the complete scenario matrix below with real components, preserving failures. Do not auto-mark skipped/excluded cases passed.
3. Collect evidence through a runner that observes worker processes, network controls and persisted output independently. Scan bundles for protected data before publication.
4. Verify digests/signatures, actual output correctness, negative-case outcomes, installed artifact identities and profile applicability. Deliberately tamper with a bundle to test rejection.
5. Produce a release acceptance report with accepted/failed/blocked counts and denominators by CPU functionality, integration/security, task model and physical accelerator tuple.
6. Promote only accepted exact capabilities; release manifest and UI must show remaining unsupported/unqualified options truthfully. Record reviewer identity and requalification triggers.

**Acceptance:** G22/G24 and every applicable gate pass with independent evidence. No universal "100% all hardware" claim is allowed; the report names the exact accepted v1 scope.

## 4. Requirement-to-Work Mapping

Ranges are inclusive and must be expanded into individual IDs by the registry builder. Shared requirements are cross-cutting; their listed package is the accountable lead, not an exemption for other packages.

| Requirement group | IDs | Accountable packages |
|---|---|---|
| Foundation | PUR-FND-001 through PUR-FND-008 | W00, W05, W19 |
| Contracts | PUR-CON-001 through PUR-CON-010 | W01, W03, W15 |
| Runtime | PUR-RUN-001 through PUR-RUN-012 | W03, W04, W05, W14 |
| Security | PUR-SEC-001 through PUR-SEC-016 | W02, W04, W12, W17 |
| Data | PUR-DAT-001 through PUR-DAT-008 | W02, W07, W10 |
| CPU | PUR-CPU-001 through PUR-CPU-005 | W06 |
| GPU | PUR-GPU-001 through PUR-GPU-005 | W07; W18 owns 005 |
| TPU | PUR-TPU-001 through PUR-TPU-005 | W08 |
| NPU | PUR-NPU-001 through PUR-NPU-005 | W09; W18 owns 005 |
| DPU | PUR-DPU-001 through PUR-DPU-005 | W06 |
| QPU | PUR-QPU-001 through PUR-QPU-006 | W13 |
| APU | PUR-APU-001 through PUR-APU-005 | W14 |
| LPU | PUR-LPU-001 through PUR-LPU-006 | W12 |
| IPU | PUR-IPU-001 through PUR-IPU-005 | W10 |
| VPU | PUR-VPU-001 through PUR-VPU-006 | W11 |
| Integration | PUR-INT-001 through PUR-INT-010 | W15, W16, W17 |
| Operations | PUR-OPS-001 through PUR-OPS-008 | W09, W19 |
| Verification | PUR-VER-001 through PUR-VER-012 | W20; specialist packages supply observations |

Every operator inherits context, artifact, job, sandbox, evidence and applicable API requirements. An operator unit test cannot waive those inherited obligations.

## 5. Verification Gates

| Gate | Required observed result | Evidence that is insufficient |
|---|---|---|
| G01 Baseline | Reviewed decisions, actual source/dependency/platform inventory and complete registry | Architecture prose alone |
| G02 Contracts | Positive/negative schema and real client/API compatibility | Models exist in source |
| G03 Data boundary | Authorized artifacts and rejected cross-tenant/revoked/secret-bearing inputs | Tenant ID present in JSON |
| G04 Jobs | Real process races, stale-fence denial, durable results and restart reconciliation | Sequential methods named concurrency tests |
| G05 Isolation | Effective OS/container limits and denied worker file/process/network actions | `ProcessPoolExecutor` or sample firewall YAML |
| G06 Capability truth | Tampered/stale/missing evidence never qualifies execution; bounded probes | Import success or editable ledger status |
| G07 CPU/DPU | Exact record outcomes and reconciled real ingestion under bounded memory | Empty pipeline or placeholder records |
| G08 Vectors | Real numerical results, source-ID parity and memory observations | NumPy installed |
| G09 Tensors | Known-answer tensor/model graphs and unsafe-model rejection | ONNX session object created |
| G10 Neural tasks | Real local inference, held-out metrics and promotion/rollback | Constant/random embeddings or toy smoke model alone |
| G11 Graph | Independent graph/array reconciliation and task-model quality | Graph tool name or plausible score |
| G12 Vision | Real OCR/video/model output, metrics and source coordinates | Image thumbnail or mocked OCR text |
| G13 Language | Real private inference, grounded/abstaining outputs and validated query proposals | Same LLM grades itself correct |
| G14 Quantum | Analytic and statistical checks, resource rejection and classical comparison | A simulator import or "quantum" label |
| G15 APU workflow | Actual multi-stage jobs, resource/fairness/cancel/fallback evidence | Static DAG visualization |
| G16 API/CLI | Authenticated packaged end-to-end journey and persisted outputs | Route count or generated OpenAPI alone |
| G17 UI | Interactive real-backend journeys, truthful states and accessibility | Screenshots of mocked data alone |
| G18 Channels | Delegated agent/MCP/VS Code calls and scope-denial observations | Tool registration or extension compilation |
| G19 Hardware | Actual GPU/NPU placement, result parity and failure/fallback tests | Provider list, device name or mock hardware |
| G20 Distribution | Clean/offline install of shipped profile with dependency/model/license integrity | Dependency lock without installation |
| G21 Recovery | Migration/restore/downgrade/fault drills preserve owned state and scope | Backup command exits zero without restore |
| G22 Performance | Reproducible raw samples and equal-work comparisons with limits | Guessed throughput or vendor marketing numbers |
| G23 No-egress | External observation of blocked hostile attempts and normal local inference | Worker reports zero bytes |
| G24 Acceptance | Independent profile-bound signed/verified bundle and truthful release manifest | Developer says complete or edits ledger |

## 6. Executable Acceptance Scenarios

Each scenario must be implemented as a real runner/fixture set, with machine-readable expected results and safe raw observations. A mock may test an error branch but cannot replace the actual component in the acceptance run.

| Scenario | Steps and expected observations | Gates |
|---|---|---|
| PU-S01 Core only | Install core without NumPy/ONNX/LLM/OCR/Aer; start API; create/read authorized fixture graph; inspect all ten logical catalog entries and explicit unavailable reasons. | G01, G06, G16, G20 |
| PU-S02 Complete CPU catalog | Install all CPU profiles/assets offline; run every declared operator on known inputs; compare outputs and receipts; assert physical GPU/NPU/QPU not claimed. | G07-G15, G20 |
| PU-S03 Cross-tenant job claim | Create A/B jobs in pending/expired/retry/cancelled states; race scoped workers in separate processes; inspect every claimed/completed artifact and fence. | G03, G04 |
| PU-S04 Idempotency and publish | Submit duplicate/conflicting keys; crash at each artifact/commit point; replay outbox delivery; assert one valid result and no duplicate graph publication. | G04, G16, G21 |
| PU-S05 Cancellation/revocation | Cancel during native kernel/model execution and revoke grants before download; inspect process exit, terminal-state race and no late publication. | G04, G05, G16 |
| PU-S06 Numeric oracle | Run cosine/tensor/sparse edge cases and randomized bounded inputs; compare independent expected outputs and source IDs; observe peak memory and thread count. | G08, G09 |
| PU-S07 Malicious model/artifact | Import altered hashes, external tensor traversal, object arrays, unsafe code bundles and huge shapes; assert quarantine/denial and no file/network effects. | G03, G05, G09, G10 |
| PU-S08 Document to knowledge | Import licensed synthetic document, preprocess/OCR, preserve boxes, review derived claims, ingest through real owner, query provenance and generate authorized report. | G07, G12, G16, G17 |
| PU-S09 Graph intelligence | Authorized graph snapshot -> CSR -> components/features/model -> query/report; reconcile entities, edges, metrics and derived-claim types. | G10, G11, G16 |
| PU-S10 Private language task | Seed unnecessary secrets and prompt injection into source fixtures; run retrieval/minimization/local inference; validate schema/citations/abstention and no privileged actions. | G03, G13, G23 |
| PU-S11 Hostile egress | Attempt raw network, DNS, UDP, IPv6, proxy, subprocess, local listener and redirects from controlled worker fixtures; observe denial outside the worker. | G05, G23 |
| PU-S12 Cache and retention | Same input in different tenants/scopes; revoke one, expire artifacts, apply legal hold; independently inspect eligible purge and denied reuse/download. | G03, G21, G23 |
| PU-S13 Quantum reference | Bell/GHZ/rotation/noise/expectation fixtures; bounded MaxCut vs exact classical optimum; excessive qubits/shots/gates rejected preallocation. | G14 |
| PU-S14 DAG contention | Run mixed-unit DAGs for two tenants with concurrent reservations; enforce fairness, peak limits and cancel/restore checkpoints; inspect all stage receipts. | G04, G15, G22 |
| PU-S15 GPU | Execute declared dense operators on actual GPU; force unsupported operator/device loss; compare CPU outputs and inspect placement/timings/strict-mode denial. | G19, G22 |
| PU-S16 NPU | Execute approved model on actual NPU; test unsupported shape/op and missing driver; inspect actual placement and strict/preferred behavior. | G19, G22 |
| PU-S17 UI and channels | Use real browser, CLI, agent, MCP and VS Code clients; run permitted tasks, navigate evidence and deny scope escalation/sensitive external-client result access. | G16-G18 |
| PU-S18 Clean offline release | Install packaged locks/wheels/binaries/models with network blocked and empty caches; exercise each advertised profile and license inventory. | G20, G23 |
| PU-S19 Recovery/upgrade | Backup, migrate, restore and rollback a populated synthetic deployment; inject disk full/model corruption/broker outage; reconcile results/grants/evidence. | G21 |
| PU-S20 Evidence attack | Alter source/model/profile digest, output, raw metric, signature and accepted status; attempt promotion with missing/expired receipts; verifier rejects every forged case. | G06, G24 |

## 7. Python Automation to Build

All scripts below are proposed deliverables, not commands that exist today. Use the repository's existing scripts and registries where suitable; these names identify responsibilities, not permission to duplicate them.

| Script / installed equivalent | Responsibilities | Required failure behavior |
|---|---|---|
| `scripts/processing/build_registry.py` | Parse all normative requirements/operators; validate mappings, counts and gate/profile applicability | Nonzero on duplicate/orphan IDs or unknown status; never auto-accept |
| `scripts/processing/discover_host.py` | Redacted CPU/device/runtime/isolation facts with exact versions | Unknown fields remain unknown; no fabricated hardware/capacity |
| `scripts/processing/build_offline_bundle.py` | Resolve approved locks/assets in a clean staging environment, verify hashes/notices and build a manifest | No tenant data; fail on missing license/hash or unresolved artifact |
| `scripts/processing/import_model.py` | Quarantine and validate already-acquired local artifacts | No implicit download, unsafe deserialize or automatic promotion |
| `scripts/processing/run_profile.py` | Run selected real acceptance scenarios with isolated synthetic tenants and safe observations | Failed/skipped/blocked cases remain distinct; nonzero when requested qualification incomplete |
| `scripts/processing/benchmark.py` | Equal-work CPU/provider comparisons, raw samples and resource/quality checks | Refuse incomparable precision/workload claims and missing hardware |
| `scripts/processing/verify_evidence.py` | Independently recompute checks, validate identity/digests/signatures, artifacts and applicability | Reject tampered/missing/stale/untrusted evidence; never trust a `passed: true` field alone |
| `scripts/processing/report_coverage.py` | Produce human/machine-readable accepted/failed/blocked report by requirement and profile | Preserve denominator; excluded work is visible, not counted passed |

Script inputs use JSON/TOML/YAML schemas through structured parsers, not string substitution or shell-built commands. Scripts must support Windows/Linux paths, deterministic exit codes, bounded runtime and redacted output. No script may push code, publish packages, change host firewall/driver policy or grant acceptance automatically without the appropriate workflow authority.

### 7.1 Suggested command interface after implementation

These commands are a target interface to implement and test, not instructions to run against the current checkout immediately:

```text
eoip processing capabilities --json
eoip processing devices --json
eoip processing plan --request fixtures/processing/vector-request.json
eoip processing submit --request fixtures/processing/vector-request.json --plan PLAN_ID --idempotency-key KEY
eoip processing status JOB_ID
eoip processing cancel JOB_ID
eoip processing receipt JOB_ID --output receipt.json
eoip processing verify-evidence --bundle BUNDLE_PATH
```

`PLAN_ID`, `KEY`, `JOB_ID` and `BUNDLE_PATH` are runtime values from the fixture/authority flow, not hard-coded production identifiers. Authentication/tenant scope comes from the secured client session. Direct worker execution is restricted to an explicitly synthetic developer/qualification harness, never a shortcut around production policy.

## 8. Baseline Tests and New Test Layout

Existing relevant tests to inspect and retain include:

- [Durable jobs](tests/integration/test_durable_jobs.py) and [durable state](tests/unit/test_durable_state_persistence.py).
- [Capability registry](tests/unit/test_capability_registry.py) and [capability route](tests/integration/test_capabilities_route.py).
- [Model runtime truthfulness](tests/unit/test_model_runtime_truthfulness.py) and [neural tiers](tests/neural/test_runtime_tiers.py).
- [CPU-only package compliance](tests/compliance/test_no_cuda_packages.py).
- [Privacy](tests/unit/test_privacy.py), [egress gateway](tests/unit/test_egress_gateway.py), [REVA egress](tests/reva/unit/core/test_egress_gate.py).
- [Privacy governance integration](tests/integration/test_privacy_governance_and_no_egress.py) and [no-egress security](tests/security/test_no_egress.py).

Their presence is not a passing result. Inspect assertions, fixtures, skip conditions, monkeypatching and actual deployment coverage. The demonstrated pending-claim issue shows why a test suite with a tenant-isolation description can still miss a critical predicate case.

New processing tests must separate:

1. Pure unit tests for schema/estimation/operator edge cases.
2. Contract tests for adapters, API and SDK serialization/error behavior.
3. Integration tests with actual job/artifact/model libraries and real persistence.
4. Security tests with real isolated workers and externally observed effects.
5. Acceptance journeys from actual installed clients/UI to real workers.
6. Hardware tests marked by exact required provider/device and treated as blocked when unavailable.

Do not blanket-skip optional profiles and still claim the full catalog passed. Core-only CI and full CPU-profile CI are different jobs with different acceptance scopes.

## 9. Performance and Capacity Protocol

Performance targets are not inferred from the user's machine, vendor marketing or the word "accelerator." First establish a reproducible benchmark manifest, then agree and version any service-level target for the intended deployment.

For each representative operator/workflow:

1. Freeze input sizes, tensor/model precision, outputs, seed, quality threshold, concurrency and resource budgets.
2. Record cold-start/model-load/compile cost separately. Run at least five warm-ups and thirty measured warm samples for short tasks; for long model/workflow jobs use at least ten measured runs and disclose the lower sample count.
3. Measure queue delay, transfer, preprocessing, kernel/inference, postprocessing, artifact write and total client-observed duration. Report median/p95 only with sample count and quantile method.
4. Record RSS/process-tree peak, allocated device memory when observable, thread/process count, failures and output quality. Unknown energy or device-memory metrics stay unknown.
5. Compare against the same CPU reference. An accelerator is usable even when slower, but automatic selection must not prefer it without justified measured benefit or an explicit policy reason.
6. Freeze the baseline report. For a fixed qualification host/profile, fail a subsequent median or p95 regression above 20% until investigated/approved; do not call this a universal customer SLA.
7. Run contention and over-limit denial cases. Tail behavior and safe failure matter as much as a single fast kernel.

Do not convert software workload throughput into fabricated hardware TOPS. No requirement permits claiming "software QPU acceleration" without equal-task evidence; simulation remains classical regardless of speed.

## 10. Rollout and Rollback

| Stage | Entry gate | Allowed use | Rollback |
|---|---|---|---|
| Development | Contracts and synthetic fixtures | Synthetic data only, unqualified label | Disable processing flag; leave core unchanged |
| CPU foundation | G01-G08 plus required privacy/job gates | Declared deterministic CPU/DPU/numeric tasks | Disable operator/profile; preserve existing graph/query |
| CPU intelligent tasks | G09-G14 plus task models, no-egress and packaging | Only accepted local model/vision/research tasks | Revoke promotion, restore prior artifact manifest, invalidate derived caches |
| Integrated pilot | G15-G18 and relevant recovery gates | Approved tenant pilot, bounded quotas, observed workflows | Stop admission, fence workers, preserve/read accepted artifacts |
| Optional acceleration | G19 and provider-specific packaging/privacy/performance | Only exact accepted hardware tuples | Explicit equivalent CPU fallback when allowed; strict modes fail |
| Production scope | All applicable gates including G20-G24 | Advertised release manifest only | Restore compatible code/config/state and revalidate capability evidence |

No migration deletes original source artifacts merely because a derived representation exists. No rollback silently changes model version, embedding space, precision or security policy. Track and reconcile in-flight work across deployment changes.

## 11. Stop Conditions and Reporting

Stop the affected operation and report a concrete blocker when:

- A required secure sandbox cannot enforce the declared boundary.
- Hardware/provider/driver evidence is unavailable for a hardware claim.
- A model has unresolved redistribution rights, unverifiable bytes or failed quality gates.
- Tenant/job authority, artifact ownership or approval semantics are unresolved.
- The current source contradicts the documented integration point and no compatible migration is defined.
- A required independent verifier or protected evidence store is unavailable.

Continue independent CPU/contracts/documentation work where safe. Do not turn a scoped blocker into a reason to fabricate implementation, disable tests or rewrite unrelated architecture.

Every progress report must state: requirements changed; files changed as navigation only; commands actually run; observed outcomes; retained evidence IDs; failed/blocked work; and next dependency-ready tasks. The final acceptance report includes exact versions, profile/device/model scope and separate completion fractions. Only verified and accepted outcomes count toward completion.

## 12. Final Completion Checklist

- All normative requirements and inherited contract/default/security obligations are mapped with no orphan IDs.
- Every v1 operator executes useful real work on CPU in its declared optional environment.
- Optional GPU/NPU claims have physical-device evidence; unsupported platforms remain explicitly unsupported.
- Actual ingestion, graph/query, reporting, UI, CLI, agent, MCP and VS Code paths use the same governed runtime.
- Tenant isolation, durable results, cancellation, recovery and revocation hold under real concurrency/faults.
- Model tasks meet their independently evaluated quality gates and remain local within the verified boundary.
- Quantum results remain bounded simulations and are compared with classical baselines.
- Clean/offline distribution, license notices, migrations, restore drills and runbooks match shipped artifacts.
- Independent evidence verification rejects tampered/missing/stale claims and controls capability promotion.
- The release report makes no universal hardware, security, performance or "100%" claim beyond its accepted finite scope.

Until these conditions are met, report the work as partial with explicit accepted, failed and blocked requirements. This plan makes completion testable; it does not substitute documentation for implementation.
