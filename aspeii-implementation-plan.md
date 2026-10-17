# ASPEII Implementation Plan for EOIP / KnowGridFlow

Plan: `ASPEII-PLAN-1.0`. Prepared: 2026-10-17 (Asia/Calcutta).
Normative specification: [aspeii-reqirements.md](aspeii-reqirements.md).
Research, sources, current gaps and probes: [aspeii-research-analysis.md](aspeii-research-analysis.md).
Inspected baseline: `00f18804ca2c7a5d12855c4763973fdfe892deac`.
Status: implementation instructions; no ASPEII feature is declared complete by this plan.
Revision: 1.0.1 (2026-10-17) — section 13 (tracker procedure) appended; sections 1–12 unchanged.

Navigation: [agent instructions](#1-instructions-to-the-implementing-agent), [repository baseline](#2-repository-reconnaissance), [architecture](#3-selected-architecture), [18 work packages](#4-work-packages-and-gates), [requirement allocation](#5-requirement-to-package-allocation), [verification](#6-verification-design), [evidence bundles](#7-evidence-bundle-and-completion-algorithm), [commands](#8-commands-and-execution-discipline), [migration](#9-migration-and-rollout), [release matrix](#11-release-matrix-and-missing-inputs), [handoff](#12-fresh-agent-handoff-and-final-acceptance).

## 1. Instructions to the Implementing Agent

Read the complete requirements and this plan before changing code. Then inspect the current checkout: the recorded baseline may have advanced. Preserve existing changes, including the untracked community and Graph Neurons documents present during research. Reconcile real implementations instead of recreating features solely because this plan names a proposed file.

The intended result is an integrated feature in the active EOIP app and frontend. Implement each work package through its real public/service boundary, run its meaningful checks, retain the observations, and update clause status only after independent verification. Source/test paths below are navigation and proposed ownership, never proof of completion.

Use a bounded vertical slice at each stage. Keep incomplete consequential features unavailable through explicit capability flags. A flag that disables an incomplete feature does not complete that feature. A synthetic service can support unit tests but cannot qualify a production adapter. Do not add fake successes, constant scores, self-attested PASS fields, or approval bypasses to get a green suite.

Do not change acceptance thresholds, remove failed cases, replace a real backend with memory, or narrow the release scope silently. Record the design decision, affected clauses, reason, and resulting incomplete status. Continue independent work when a customer environment is unavailable, and leave the actual integration BLOCKED.

### 1.1 Completion Levels

| Level | Evidence | What it establishes |
| --- | --- | --- |
| L0 | Design and source references | Planned or inspected only |
| L1 | Schema/static checks | Structure/type correctness within the check |
| L2 | Executed isolated behavior | Component behavior on declared fixtures |
| L3 | Real service/API/storage integration | Actual runtime contract and persistence |
| L4 | Worker/concurrency/recovery/security observations | Correctness across relevant failure boundaries |
| L5 | Browser/CLI/MCP user journey | Integrated user-visible behavior |
| L6 | Packaged deployment, real adapters, restore, release verifier | Qualified release profile |

Every requirement receives the applicable levels, specified in the traceability registry. Inapplicable levels require a concrete rationale; merely difficult or unavailable checks are BLOCKED, not inapplicable. Requirement completion is clause-based, not the maximum level of one test.

## 2. Repository Reconnaissance

Run these read-only commands from the repository root. PowerShell examples avoid changing the worktree.

```powershell
git status --short
git rev-parse HEAD
rg --files --hidden -g AGENTS.md -g '!node_modules' -g '!.git' -g '!.venv'
rg --files packages/eoip apps/api apps/mcp frontend/src tests scripts
rg -n 'promote_fact|ToolRegistry|ExternalMCPClient|ToolExecutionAttestor' packages apps tests
rg -n 'proposal_store|AgentOrchestrator|create_app|include_router' apps/api backend packages/eoip
```

Read `pyproject.toml`, dependency locks if present, `frontend/package.json`, active app factory, auth middleware, request principal handling, route registration, workers, state storage, feature flags, model providers, and frontend navigation. Use structured OpenAPI/route inspection in an isolated application fixture to identify the actual mounted routes; a function found by search may not be reachable.

Record exactly which storage backends and deployment modes exist. The research found a file-backed single-worker queue and an in-memory state engine. Do not describe them as distributed persistence. Inspect current `community-ip-implementation-plan.md` and CTAR implementation status, plus Graph Neurons interfaces; names in draft documents do not mean code exists.

Also read [ip-requirements.md](ip-requirements.md) and [ip-requirements-implementation-plan.md](ip-requirements-implementation-plan.md), which appeared concurrently while this plan was prepared. Apply requirements section 2.1 before choosing warrant, checkpoint, lease, signer, consequence-budget or publication ownership. Preserve their public schemas/configuration keys. Record unresolved semantic conflicts against both requirement IDs; do not add a parallel warrant-service or mistake an IP fact lease for a worker fence.

### 2.1 Initial Behavior Probes

Convert the three recorded probes into meaningful failing regression cases. Use only in-memory handlers and isolated test data:

1. `promote_fact({}, 'CERTIFIED', confidence=0.8)` must no longer be enough to create a usable certified fact.
2. A registered approval-required tool invoked with a nonexistent approval ID must produce no handler call.
3. An external MCP client pointed at a reserved `.invalid` host must not report a connected session or successful tool execution.

Also inspect authenticated proposal routes, current `ChangeProposal` serialization, and the Agents screen. The recorded UI expects `p.id` while the DTO defines `proposal_id`, and its mutation error is swallowed. Test the actual response through the browser before choosing a fix, because the checkout may now contain an adapter.

Do not run production connectors, install external research plugins, or open network egress as part of these initial probes. Repository research authorization does not substitute for configured tenant credentials and action authority in the product.

## 3. Selected Architecture

### 3.1 Ownership and Proposed File Layout

Paths marked NEW are proposed; they do not currently prove implementation. Use the existing owner when the same responsibility is already implemented correctly. New modules are small cohesive services, not a replacement agent framework.

| Responsibility | Preferred ownership / proposed files |
| --- | --- |
| Public domain schemas | NEW `packages/eoip/contracts/aspeii.py`; split into smaller contract modules only if size warrants |
| Scope/decision records | NEW `docs/aspeii/decisions.md`, `docs/aspeii/traceability.json` |
| Transactional authority repository | NEW `packages/eoip/aspeii/repository.py`, `sqlite_repository.py`, `postgres_repository.py`, migrations |
| Claim support and lifecycle | Extend `provenance/`; NEW `packages/eoip/aspeii/claims.py`, `support.py` as needed |
| Intent and task service | NEW `packages/eoip/aspeii/intents.py`, `delegation.py`; integrate existing agent runtime/orchestrator |
| Grants and reservations | NEW `packages/eoip/aspeii/grants.py`; reuse current authentication/authorization principals |
| Action identity and checker | NEW `packages/eoip/aspeii/actions.py`, `canonical.py`, `verification.py` |
| Approvals and executor | Extend proposal service; NEW `packages/eoip/aspeii/execution.py`; single dispatch boundary |
| Receipt signing/verification | NEW `packages/eoip/aspeii/receipts.py`; reconcile existing attestor rather than retaining its default secret |
| Semantic view and builder | Extend `ontology/`; NEW `packages/eoip/aspeii/semantics.py`, `evolution.py` |
| Evaluations and challenges | Extend `agents/evaluation.py` where suitable; NEW bounded experiment services |
| Runtime adapters | Extend `tools_contract/mcp_bridge.py`, `agents/tools.py`, `apps/mcp/main.py` with shared contracts |
| API router | NEW `packages/eoip/aspeii/router.py`, registered by `apps/api/main.py` |
| CLI | Extend actual `eoip.cli` command tree after inspecting it; commands listed later are target contracts |
| Current GUI | `frontend/src/screens/Agents.tsx`, `Ask.tsx`; NEW screens/components/hooks under existing conventions |
| Evidence tooling | NEW `scripts/verify_aspeii_evidence.py` using qualified shared verifier utilities; preserve MVP verifier |
| Tests | New focused files under `tests/unit`, `tests/integration`, security/recovery suites and the actual browser-test location |

Application policy, scopes, source connectors, model routing, and graph stores remain shared services. Reconcile duplicate tool registries through an explicit adapter and one authority record. No unaudited singleton can become a second execution gateway.

### 3.2 Persistence Contract

Choose a narrow SQL repository for ASPEII authority. Default implementation is standard-library SQLite for one-host local deployment and a reviewed pinned PostgreSQL driver for multi-worker deployment. Do not add an ORM merely to follow this document; use the repository's existing transactional abstraction if it meets these semantics. Record the selected driver/version/license in the dependency decision. PostgreSQL profile is required for the full SaaS qualification matrix.

Minimum tables (names may receive a project-standard prefix):

| Table | Keys / transaction role |
| --- | --- |
| `artifact_revisions` | PK tenant, artifact ID, revision; kind, workspace, schema, canonical digest, immutable typed payload; unique content revision |
| `artifact_heads` | PK tenant, artifact ID; current revision/state; optimistic concurrency counter |
| `dependency_edges` | Tenant, dependent ref, input ref, support-set ID, kind; reverse index on input ref |
| `task_leases` | Tenant, task ID; owner, expiry, monotonically increasing fence; single current lease |
| `grants` | Tenant, grant ID; parent, subject, audience, scope, expiry, revocation epoch, token hash |
| `budget_reservations` | Root/task/attempt, units/currency, reserved/used/released; guarded aggregate counters |
| `action_admissions` | Tenant, action ID/digest, policy/state refs, status and revision; exact immutable effect |
| `approval_decisions` | Tenant, decision ID, action digest, principal, expiry, decision and consumption/revocation state |
| `execution_attempts` | Tenant, logical action ID, attempt number, worker fence, provider key, dispatch/reconciliation state |
| `idempotency_records` | Unique tenant, actor, route, key; request digest and stable response/operation ref |
| `outbox_events` | Unique event ID and tenant sequence; committed payload refs, delivery attempts, watermark |
| `receipt_records` | Immutable receipt/certificate refs, digests, key IDs/signatures, chain/checkpoint refs |
| `semantic_heads` | Tenant, workspace, model/view profile; active version and revision |
| `evaluation_cases` | Evaluation ID, case ID, repetition, parent/candidate refs; scores, failures, usage and artifacts |

SQL payload storage does not exempt schemas from validation or indexing. Tenant-scoped foreign keys or equivalent application checks must prevent cross-tenant references. Use transaction isolation or row locking sufficient for budget reservation, decision consumption, and head updates. Demonstrate correctness with races; do not rely on process-local locks for PostgreSQL.

Object blobs are immutable content-addressed data behind existing authorized storage. Store digests/references in SQL, not unlimited evidence bodies. Graph data is a rebuildable projection except existing domain/source graph records, which retain their owner. A missing/lagging graph projection must not grant permission or hide an authoritative denial.

### 3.3 Service Ports

Implement typed interfaces and shared exceptions for these boundaries:

```text
IntentService: create, revise, validate, activate, cancel, evaluate_outcome
TaskService: create_dag, assign, claim_lease, heartbeat, handoff, complete, reconcile
GrantService: issue, attenuate, resolve_effective_scope, reserve, settle, revoke
ClaimService: record, resolve, support, challenge, invalidate
ActionService: propose, canonicalize, check, decide, admit, dispatch, reconcile
ReceiptService: close, sign, export, verify
SemanticService: manifest, browse, resolve, build_candidate, compare, publish, rollback
QualificationService: import_run, validate_bundle, clause_status, release_verdict
```

Services receive an authenticated execution context, never an untrusted identity dictionary. Put meaningful invariants in services/repositories so HTTP, CLI, workers and MCP cannot bypass them. Model-provider implementations return proposals/typed output; they do not receive repository write access to approvals, verifiers or published version heads.

## 4. Work Packages and Gates

All packages are mandatory for the defined scope. P0/P1 determines sequencing, not whether a clause may be omitted. Adjacent packages can be implemented in separate changes only when their shared schemas are frozen and tests demonstrate compatibility.

### WP01: Baseline and Traceability

Covers ASPEII-RQ-001 and establishes ASPEII-RQ-035 infrastructure. Depends on none.

1. Run section 2 reconnaissance and read the research findings against current source.
2. Create a machine-readable registry of 36 requirements, 216 clauses, shared-contract obligations, and 16 scenarios. Capture requirement-document digest.
3. Assign each clause to work package, integration layers, test scenario and evidence type. Separate observed current behavior from proposed behavior.
4. Save the initial helper probe outputs and route/schema inventories under an ignored run-specific evidence directory.
5. Inventory source-revision, auth, proposal, CTAR, model and ontology contracts; record exact adapters to extend and conflicts to resolve.
6. Add registry validation for duplicates, omissions, unknown refs and false VERIFIED statuses.

Gate: the registry reports all clauses OPEN; baseline manifest is reproducible; the three unsafe helper behaviors are either reproduced or superseded by new runtime evidence. No implementation credit from test names.

### WP02: Contracts and Transactional Storage

Covers ASPEII-RQ-002 and ASPEII-RQ-003. Depends on WP01.

1. Implement strict records from requirements section 3, lifecycle transition validators, typed references and stable sanitized errors.
2. Write JSON Schema/OpenAPI components and generated frontend DTOs; keep schema conversion in one toolchain.
3. Implement repository transactions, idempotency records, revisions, leases, reservations and outbox before services can mutate state.
4. Add SQLite migration and PostgreSQL migration with exactly equivalent invariants; include startup schema compatibility checks.
5. Store immutable payloads plus mutable heads through explicit transition commands. Keep projection consumers idempotent.
6. Test persistence by terminating/restarting processes and exercising separate DB connections, not by reusing one in-memory object.

Gate: round-trip validation, invalid-input refusal, duplicate submit, two-worker CAS race, crash recovery, and projection replay pass on both required storage profiles. Add a clear partial local-only status while PostgreSQL is unavailable.

### WP03: Identity and Epistemic Foundation

Covers ASPEII-RQ-004, ASPEII-RQ-012, ASPEII-RQ-013, ASPEII-RQ-014 and ASPEII-RQ-015. Depends on WP02.

1. Resolve tenant/principal from current auth middleware. Verify proposal and agent route behavior at HTTP boundaries; remove body identity authority.
2. Extend tool contracts with production/effect classes, evidence semantics and qualified implementation identity. Reconcile both registries.
3. Implement claim/evidence records, immutable source locators, origin groups, support sets, conflicts and four separate status dimensions.
4. Implement support evaluation with grounded leaves, AND/OR support groups, cycle detection and bounded graph traversal. A traversal limit yields UNKNOWN.
5. Replace trust promotion with verified transition service; compatibility helper must call that service or return a legacy unqualified result, not silently certify.
6. Enforce current authorization and freshness before returning claims, derivative content or evidence. Wire invalidation by revision.
7. Add typed outputs to actual RAG/agent/memory paths, including a generator wrapped as a remote tool and a generated assertion stored in a database.

Gate: confidence-only promotion fails; copied evidence is not independent; circular support is rejected; real sources can independently support a hypothesis; permission revocation blocks reads and actions immediately. Preserve existing graph fact semantics during migration.

### WP04: Canonical Actions, Checker and Approvals

Covers ASPEII-RQ-018, ASPEII-RQ-019 and ASPEII-RQ-020. Depends on WP03.

1. Select a vetted RFC 8785 implementation and produce cross-language vectors. Record its exact version and license; never approximate with sorted `repr`.
2. Implement canonical projection from trusted resolved action fields. Store immutable action content and reject semantic mutation after review.
3. Register independent deterministic obligation verifiers and their schemas; use trusted adapter contracts to derive required checks and risk.
4. Integrate approvals with existing proposal storage/service through bound decisions. Do not make approval automatically execute a mutation.
5. Implement admission transaction: verify authority and obligations, bind decision, reserve logical effect, issue certificate and append audit event.
6. Update approval-required `ToolRegistry.invoke` paths to resolve real admission; a nonempty approval string must not suffice.
7. Add negative tests for changed tenant/account/destination, nested args, stale state, omitted obligation, self-approval, expiry and duplicate consumption.

Gate: ASPEII-E2E-05 passes with independent zero-handler-call evidence. Cross-language vectors agree. A successful adversarial model narrative cannot alter the checker decision. Formal proof support is an optional plugin contract, not a requirement to invent a prover.

### WP05: Gateway, Actual Effects and Receipts

Covers ASPEII-RQ-021 and ASPEII-RQ-022. Depends on WP04.

1. Implement one final dispatch boundary and inventory every consequential route/call site. Prevent legacy direct invocation from bypassing it.
2. Qualify a reversible EOIP graph correction adapter with expected-revision checks and independent postcondition read.
3. Add attempt persistence, fences, provider idempotency and independent reconciliation. Place a fault-injection point immediately before/after dispatch and before receipt closure.
4. Implement signing with a vetted Ed25519 library/provider, trusted public-key manifests, rotation, revocation and export verification.
5. Replace the default-secret in-memory attestor path with the shared receipt service; label legacy HMAC artifacts accurately.
6. Verify partial failure semantics, unknown outcomes, duplicates and compensation as a separately authorized action.

Gate: graph correction changes exactly the approved record once; altered/expired certificates never dispatch; crash after external commit does not duplicate effect; offline verifier detects changed metadata/outcome/chain. Restore cannot resurrect a consumed approval.

### WP06: Real MCP and Connector Qualification

Covers ASPEII-RQ-023 and the external-effect portion of ASPEII-RQ-021. Depends on WP05.

1. Inventory the installed MCP SDK and active `apps/mcp/main.py` behavior. Pin a supported protocol/version before implementation.
2. Replace constructed connection/success responses with actual initialize/list/call transport. Add explicit unsupported and disconnected states.
3. Implement stdio and HTTP clients with credential audience isolation, allowlists, response bounds, timeouts and schema-drift handling.
4. Start a separate actual MCP test server process for each transport. Its own append-only call log and state are independent observations; do not patch the client's transport to return fixtures for qualification.
5. Select the first real sandbox-capable write adapter from current supported connectors using this order: existing qualified issue/ticket update adapter, existing qualified document draft adapter, then a new narrowly scoped issue/ticket adapter. Prefer a configured disposable GitHub/GitLab/Jira sandbox; record the exact selected provider and supported action. No credentials -> BLOCKED external profile, while local transport work continues.
6. Exercise one authorized sandbox write, read its actual state independently, and remove/revert only through the provider's authorized cleanup workflow. Track test artifacts and quota/cost.
7. Classify external observation-only integrations honestly; they may import receipts but cannot enable mandatory-gate write actions.

Gate: both MCP transports prove actual server interaction; unreachable endpoint fails; malicious redirect/schema change is blocked; selected real connector has an observed effect plus reconciliation receipt. A local HTTP mock is transport test evidence, not the selected vendor integration result.

### WP07: Intent and Outcome Contracts

Covers ASPEII-RQ-005 and ASPEII-RQ-006. Depends on WP04; runtime execution integrates after WP08.

1. Add intent schemas and services with explicit default configuration from requirements section 1.3.
2. Map existing business objectives/capabilities to intent references without turning all objectives into runnable tasks.
3. Implement deterministic validation of unresolved fields, acceptance predicates, non-goals, effect boundaries and aggregate budgets.
4. Provide a manual/deterministic plan path first. Add a model planner behind the existing configured provider interface, treating output as untrusted candidate data.
5. Compile task DAGs and allocate every mandatory outcome predicate to a registered verifier or explicit human acceptance task.
6. Implement immutable revisions, active-intent changes, dependent action invalidation and truthful partial outcomes.

Gate: ambiguous intent remains draft; read-only investigation cannot become write remediation; passing child status cannot bypass a failed outcome predicate. Compare actual runtime result to frozen acceptance through a separate verifier.

### WP08: Delegation, Grants and Recoverable Scheduling

Covers ASPEII-RQ-007, ASPEII-RQ-008, ASPEII-RQ-009 and ASPEII-RQ-010. Depends on WP05 and WP07; capability evidence harness from WP01/WP16 is built incrementally.

1. Implement assignment and handoff contracts for agent and human participants; preserve accountable owner and parent intent.
2. Implement qualified capability lookup and deterministic constrained ranking. Start with internal agents; external federation remains unavailable until its adapter qualifies.
3. Add opaque attenuated grants, ancestor revocation checks, aggregate reservations and reconciliation of usage. Total model budget includes billed input/output/reasoning categories available from the provider; do not count only displayed output tokens.
4. Implement DAG scheduler, task dependencies, leases/heartbeats/fences, backpressure, cancellation and bounded retries.
5. On reassignment, reconcile previous attempts before transferring authority. A stale worker cannot write through the gateway.
6. Capture observable task events and safe explanation data through the existing trace store or a compatible adapter.
7. Test no-provider, unavailable human reviewer, all delegates ineligible, budget exhaustion, duplicate events and root revocation.

Gate: ASPEII-E2E-01, 02 and 06 pass on real workers; partial/blocked tasks are visible; all child usage stays within root budgets. No unrestricted recursive execution or silent delegation escalation.

### WP09: Human Review and Epistemic Challenges

Covers ASPEII-RQ-011, ASPEII-RQ-016 and ASPEII-RQ-017. Depends on WP04 and WP08.

1. Implement human task responses, review ownership, expiry, decline/escalation and revision-aware decisions.
2. Add belief/requirement artifacts and structured falsification specifications; import existing requirement IDs without renumbering them.
3. Implement deterministic contradiction rules over structured predicates and boundary-aware dependencies; keep language-model suggestions advisory.
4. Persist challenge results and counterexamples; generate scoped repair proposals through the action/proposal service.
5. Enforce finite challenge budgets and preserve failed requirements/previous runs after reconstruction.
6. Integrate independent receipt verification before any requirement claim becomes VERIFIED.

Gate: a review timeout never becomes approval; false support cycles and conflicting constraints remain unresolved; finite stress testing reports only the tested scope. Existing test-file links alone do not advance a requirement.

### WP10: Semantic Access and Grounded Builder

Covers ASPEII-RQ-024 and ASPEII-RQ-025. Depends on WP03, WP06 and WP07.

For this dependency, WP06's qualified MCP read transports are sufficient to start semantic access. Missing credentials for its separate real vendor write qualification do not block independent WP10 work; the external-write release profile remains BLOCKED.

1. Create explicit adapters from ontology manifest/source mappings/provenance to typed semantic views.
2. Implement bounded browse/resolve and manifest operations over real storage with current authorization and snapshot pinning.
3. Add ambiguity, truncation, unavailable evidence and stale-version results. Preserve relation semantics; no arbitrary fallback edges.
4. Implement a deterministic/manual builder and a model-assisted proposal adapter. Both use the same bounded source probe interface.
5. Use actual authorized table metadata and document spans for the initial fixture; record column/units/join-path observations separately from business-rule assertions.
6. Route version-zero publication through the same validation/approval/publication authority as subsequent versions; until WP13 exists, persist drafts only.

Gate: a real source probe detects an invented column; ambiguous concepts remain alternatives; browse/resolve returns only authorized records; draft initialization cannot silently set the active ontology.

### WP11: Trajectories and Candidate Isolation

Covers ASPEII-RQ-026 and ASPEII-RQ-027. Depends on WP08 and WP10.

1. Instrument tool boundaries with safe trajectory records, exact versions, usage and independent outcome predicates.
2. Store trace artifacts in authorized storage; redact secret/data content and exclude chain-of-thought.
3. Implement frozen workload selection with origin deduplication and construction/validation separation.
4. Add attribution hypotheses and typed patches for content, schema, and tool view; record one primary causal hypothesis per candidate.
5. Sandboxed candidate workers receive read-only approved source snapshots and no production credentials, signing keys, policy write access or evaluator labels.
6. Reject executable tool generation, permission expansion, evaluator changes and active-head mutation. Exhausted rounds produce an explicit incomplete result.

Gate: candidate evaluation cannot mutate the live semantic version; poisoned trajectories cannot change policy; duplicated traces do not inflate evidence or measured improvement.

### WP12: Paired Evaluation

Covers ASPEII-RQ-028. Depends on WP11 and evaluation foundations from WP16.

1. Build `EvaluationSpec` before proposing a candidate: case IDs, origin/time grouping, splits, task metric, model/tool versions, budgets, seeds, thresholds and hard constraints.
2. Run baseline without semantic views, parent static view and candidate view on matched tasks. Only parent/candidate paired results decide the promotion delta; the raw baseline supplies context.
3. Record per-case outputs, expected outcomes, actual assertions, duration/tokens/errors and all failure cases.
4. Use equal conditions, randomized parent/candidate execution order, at least three repetitions for nondeterministic providers, and isolated caches or a documented matched-cache policy.
5. Compute case-level mean deltas with a paired bootstrap over origin groups using 10,000 resamples and a recorded seed. Use the percentile 95% interval; include repetitions within each case rather than treating them as independent cases. Document exceptions for a preapproved task-specific test.
6. Enforce improvement, resource and no-regression gates; any mandatory security case failure rejects. Critical-stratum task-score decrease below zero rejects even if the global mean improves.
7. Limit candidate rounds to three. A new search run must use a refreshed validation reserve or a documented unchanged-reserve risk assessment; final qualification set stays sealed until selection finishes. Opening final labels for tuning invalidates that qualification split.
8. Model-judge scores remain advisory for factual/security gates. Human-scored subjective cases use a frozen rubric, blinded pair order, and recorded disagreement/adjudication.

Gate: deliberately bad candidate fails; constant evaluator is caught; missing case produces incomplete evaluation; gains reported for each qualified model/domain rather than generalized globally. A new candidate can legitimately remain rejected; do not fabricate a passing example.

### WP13: Publication, CTAR and Rollback

Covers ASPEII-RQ-029 and ASPEII-RQ-030. Depends on WP05, WP12 and the actual CTAR implementation.

1. Reconcile ASPEII artifact kinds with community CTAR schemas. If CTAR is still only a plan, implement the shared required dependency/event/lifecycle capability under its existing ownership before claiming integration.
2. Record every derivation's source/model/prompt/policy/tool/evaluator/ontology revisions with `dependent DEPENDS_ON input` edges.
3. Implement active-head CAS and a single publication transaction with approved action, evaluation record and outbox.
4. Invalidate affected caches, certificates, mappings, agent qualifications and predictions. Enforce immediate authority/read checks independent of graph projection lag.
5. Add progressive read-only exposure and rollback thresholds in versioned rollout configuration. Start at one explicit nonproduction workspace.
6. Implement governed rollback with impact/compatibility analysis and new lineage events. Do not claim rollback reverses external effects.
7. Exercise duplicate/out-of-order events, late corrections, revocation before worker processing, two-candidate races, and publish crash/restore.

Gate: ASPEII-E2E-08, 10 and 11 pass, including independent surviving support and model-specific qualification. Neural predictions never become facts through publication alone.

### WP14: HTTP, CLI and Event Integration

Covers ASPEII-RQ-031. Depends on service packages above; expose read/draft endpoints incrementally.

1. Register the router in the active factory and confirm endpoints through actual OpenAPI and HTTP calls.
2. Implement request/response DTOs, standard errors, idempotency, conditional revisions and object-level access checks.
3. Expose resumable tenant-filtered events from the durable outbox; expired cursor returns a defined gap/reset instruction.
4. Add CLI command group through the existing parser: `aspeii inspect`, `aspeii evaluate`, `aspeii receipts verify`, `aspeii qualification`, and governed submission commands. Define flags and JSON output in generated help before documenting them as available.
5. Reconcile old proposal routes: preserve safe reads, reject unsafe direct execution, and return explicit deprecation/action-admission requirements.
6. Add reverse-proxy, local/offline, real MCP, and packaged CLI contract checks.

Gate: actual HTTP/CLI/MCP paths agree on scope and outcomes; changed-payload idempotency conflicts; no public path can dispatch with arbitrary approval strings.

### WP15: Integrated GUI Workflows

Covers ASPEII-RQ-032 and user-facing portions of ASPEII-RQ-011. Depends on WP14; prototype with real draft/read APIs early.

1. Extend current navigation with Intents and Assurance, plus appropriate Agents/Ontology subviews; use nested routes with durable deep links and breadcrumbs.
2. Implement intent list/editor/detail, task graph/table, evidence inspector, action review, candidate diff/evaluation and publication history.
3. Use generated DTOs and tenant-scoped TanStack Query keys. Fix proposal ID and swallowed-error behavior against actual APIs.
4. Use existing lucide icons, buttons, segmented controls/tabs, numeric inputs and filters. Keep short operational labels, visible status, bounded typography and progressive advanced settings.
5. Make approval review display exact payload effects and stale revision. Prevent duplicate submissions while showing retryable errors. Approval and execution are distinct states/commands.
6. Build accessible dialogs, focus restoration, keyboard navigation, table equivalents for graphs, reduced-motion support and consistent empty/error/denied states.
7. Run browser workflows with real backend, worker and storage on all required viewports. Include full-page and relevant-state screenshots plus DOM/network assertions and trace artifacts.

Gate: no hidden approval error, wrong proposal ID, overflow, inaccessible essential control or false completion badge. Screenshots alone are insufficient: show real state changes and denied effects through independent backend observations.

### WP16: Independent Evaluation and Adversarial Harness

Covers ASPEII-RQ-034 and ASPEII-RQ-035. Starts at WP01; finishes after WP15.

1. Build shared fixture and receipt infrastructure early, adding behavior cases alongside each package.
2. Create deterministic synthetic source corpora, known-support/contradiction graphs, restricted twins, grant trees, effect servers and candidate datasets.
3. Instrument independent effect observations, such as a separately running MCP server log, database audit snapshot, connector readback, and browser network trace.
4. Add anti-stub controls: fake MCP success, constant claim verifier, constant evaluator, fabricated approval, static result page and hard-coded canned corpus response must be detected.
5. Exercise actual boundaries for injection, SSRF, cross-tenant access, token audience confusion, poisoned semantic data, self-validation cycles and replay/race attacks.
6. Keep evaluation credentials, labels and outputs out of builder access. Pin external dataset/model licenses and retention when adding non-synthetic data.
7. Link all outcomes to atomic clauses; explicitly allocate shared-contract requirements and all API/screen states.

Gate: harness fails when a meaningful invariant is intentionally violated; all applicable 16 scenarios have reproducible results. Security failures cannot be hidden by passing average scores.

### WP17: Operations, Deployment and Migration

Covers ASPEII-RQ-033 and deployment portions of ASPEII-RQ-003/034. Depends on WP13-WP16.

1. Package required storage, signing and adapter dependencies for Windows/Linux customer installations and the chosen Linux SaaS container profile; record supported versions.
2. Implement configuration validation, health/readiness, sanitized metrics and operator controls.
3. Execute the migration sequence in section 9 on a realistic legacy fixture and a restored copy, checking data counts and digests.
4. Measure specified performance on declared hardware; include warm-up, case counts, errors/timeouts and resource curves.
5. Exercise operator runbooks with real dependency failures and independent recovery observations.
6. Verify no-egress behavior with model disabled and a configured local provider; hosted model tests are separately cost-authorized, versioned profiles.
7. Assemble operator and user documentation from the behavior that actually qualified, including unavailable modes.

Gate: actual install/upgrade/restore works; consumed approvals remain consumed; no secret/default development key in packages; resource/latency targets met or explicitly FAILED/BLOCKED for that release profile.

### WP18: Final Release Evidence and Handoff

Covers ASPEII-RQ-036. Depends on all prior required packages.

1. Freeze release candidate and full source/dependency/configuration manifests; capture all concurrent changes.
2. Run the scoped release suite from packaged artifacts in isolated supported environments. Reuse valid receipts only when their complete dependency manifest still matches.
3. Independently verify clauses, profiles, raw artifact integrity, scenario observations, migrations, real adapters, browser behavior and operational restore.
4. Generate a completion report with 216-clause denominator plus mandatory shared/scenario gate status and separate deployment matrix.
5. Attempt verifier negative controls: delete one artifact, change covered code/config, swap tenant, forge a PASS, omit one clause, reuse a stale receipt. Every case must prevent full completion.
6. Update release notes, requirement ledger and remaining-gap handoff. Do not commit, publish or deploy externally unless the user requests that action.

Gate: every required clause and cross-cutting gate VERIFIED on the actual release profile. Any gap yields a truthful partial release report, not a redefined 100% score.

## 5. Requirement-to-Package Allocation

All six clauses of each row are assigned. Implementing agents must add finer test/evidence mappings without deleting this coverage.

| Requirement | Primary package | Required integration emphasis |
| --- | --- | --- |
| ASPEII-RQ-001 | WP01 | Current checkout, registry, baseline probes |
| ASPEII-RQ-002 | WP02 | Python/TS schemas and legacy adapters |
| ASPEII-RQ-003 | WP02, WP17 | Both SQL profiles, workers, restore |
| ASPEII-RQ-004 | WP03 | HTTP/MCP/UI/export tenancy |
| ASPEII-RQ-005 | WP07 | Intent GUI/API/runtime |
| ASPEII-RQ-006 | WP07 | Independent outcome verifier |
| ASPEII-RQ-007 | WP08 | Real task DAG and handoffs |
| ASPEII-RQ-008 | WP08 | Measured capability registry |
| ASPEII-RQ-009 | WP08 | Atomic budgets, grant chain, revocation |
| ASPEII-RQ-010 | WP08 | Worker fencing and reconciliation |
| ASPEII-RQ-011 | WP09, WP15 | Human queue and exact review |
| ASPEII-RQ-012 | WP03 | Both tool registries and typed outputs |
| ASPEII-RQ-013 | WP03 | Claims/evidence storage and permissions |
| ASPEII-RQ-014 | WP03 | RAG/memory/tool anti-laundering |
| ASPEII-RQ-015 | WP03, WP13 | Read-time validity and CTAR |
| ASPEII-RQ-016 | WP09 | Requirement/claim lifecycle |
| ASPEII-RQ-017 | WP09 | Executed challenges and repair |
| ASPEII-RQ-018 | WP04 | Cross-runtime canonical action vectors |
| ASPEII-RQ-019 | WP04 | Independent trusted checker |
| ASPEII-RQ-020 | WP04 | Approval, admission, concurrent consumption |
| ASPEII-RQ-021 | WP05, WP06 | Actual local/external effects |
| ASPEII-RQ-022 | WP05 | Signed receipts and independent verification |
| ASPEII-RQ-023 | WP06 | Real stdio/HTTP MCP |
| ASPEII-RQ-024 | WP10 | Semantic browse/resolve/manifests |
| ASPEII-RQ-025 | WP10 | Actual source probes and version zero |
| ASPEII-RQ-026 | WP11 | Trace capture and attribution |
| ASPEII-RQ-027 | WP11 | Isolated typed candidates |
| ASPEII-RQ-028 | WP12 | Held-out paired evaluation |
| ASPEII-RQ-029 | WP13 | Atomic publish, conflict and rollback |
| ASPEII-RQ-030 | WP13 | CTAR/AMRB and neural prediction semantics |
| ASPEII-RQ-031 | WP14 | Active HTTP/CLI/events/MCP surfaces |
| ASPEII-RQ-032 | WP15 | Current frontend real browser workflows |
| ASPEII-RQ-033 | WP17 | Install, metrics, restore and performance |
| ASPEII-RQ-034 | WP16 | Adversarial and supply-chain qualification |
| ASPEII-RQ-035 | WP01, WP16 | Independent observed behavior |
| ASPEII-RQ-036 | WP18 | Artifact-bound release evidence |

## 6. Verification Design

### 6.1 Fixture Contract

Create a small deterministic corpus with two tenants and two workspaces each. Include:

- A service, incident, owning team and source revision with a known factual relation.
- One corrected relation, one revoked source, one stale observation and one independently corroborated alternative.
- A mirrored source and a generator-produced copy sharing the same origin group.
- A pair of contradictory structured constraints and a pair of merely different natural-language claims.
- A table/document mapping with an invented column, ambiguous term, mixed units and a valid grounded mapping.
- A reversible graph mutation, a remote idempotent update, and a remote write with deliberately uncertain response.
- A valid/expired/revoked/fake approval and old/new worker fences.
- Parent/candidate semantic versions where one improves task performance and another breaks a mandatory invariant.

Fixtures have explicit expected outputs, IDs, creation seed, source license, content hash and labels. Test-server effects are independently recorded. Fixtures never include production personal data or tokens. Builders can access construction data only; evaluator ground truth lives behind a distinct capability or process boundary.

### 6.2 Scenario Evidence Allocation

| Scenario | Minimum observations | Core packages |
| --- | --- | --- |
| ASPEII-E2E-01 | HTTP intent, actual task events, graph reads, outcome predicates, browser, restart | WP07-WP09, WP14-WP15 |
| ASPEII-E2E-02 | Validation response, unresolved fields, zero dispatch count, GUI draft | WP07, WP15 |
| ASPEII-E2E-03 | Cross-tool claim lineage, circular support rejection, no certified output | WP03, WP06, WP16 |
| ASPEII-E2E-04 | Approved digest, actual graph before/after, independent verifier, receipt | WP04-WP05 |
| ASPEII-E2E-05 | Denial reasons and independent effect counter zero for every variant | WP04-WP05, WP16 |
| ASPEII-E2E-06 | Concurrent workers, lease/fence history, aggregate reservation ledger | WP08 |
| ASPEII-E2E-07 | Server commit, client timeout, stored UNKNOWN_OUTCOME, reconciled readback | WP05-WP06 |
| ASPEII-E2E-08 | Revocation commit, blocked read/action before worker, CTAR repair | WP03, WP13 |
| ASPEII-E2E-09 | Real probe output, typed mapping, source locator, approved initial version | WP10, WP13 |
| ASPEII-E2E-10 | Matched per-case scores and security failure, unchanged active digest | WP11-WP12 |
| ASPEII-E2E-11 | Publish CAS, invalidation events, rollback receipt and restored read result | WP13 |
| ASPEII-E2E-12 | Executed counterexample, unresolved conflict, budget-limited termination | WP09 |
| ASPEII-E2E-13 | Separate stdio/HTTP server logs, auth/schema failure records | WP06 |
| ASPEII-E2E-14 | Offline verify outputs, tampered failures, rotation/restore replay refusal | WP05, WP17 |
| ASPEII-E2E-15 | Network deny logs, model-disabled behavior, local-provider results | WP17 |
| ASPEII-E2E-16 | Browser traces plus independent clause verifier refusing missing evidence | WP15-WP18 |

### 6.3 Suggested Test Ownership

These names are proposed starting points, not files assumed to exist. Prefer extending a relevant existing test where it produces independent behavior coverage.

| Proposed suite | Behavior it must demonstrate |
| --- | --- |
| `tests/unit/test_aspeii_contracts.py` | Strict schemas, legacy mapping, illegal transitions, boundary values |
| `tests/unit/test_aspeii_support.py` | AND/OR support, cyclic/duplicate origins, conflicts, unknown limits |
| `tests/unit/test_aspeii_canonical.py` | Shared canonical vectors and semantic separation |
| `tests/integration/test_aspeii_action_gateway.py` | Real admission/dispatch/postcondition and denial no-effects |
| `tests/integration/test_aspeii_repository.py` | SQLite/PostgreSQL CAS, outbox, budgets, restore |
| `tests/integration/test_aspeii_delegation.py` | Actual worker leases, root budget, reassignment and cancellation |
| `tests/integration/test_aspeii_mcp.py` | Separate processes and actual transports; not patched client success |
| `tests/integration/test_aspeii_semantic_evolution.py` | Real snapshots, paired evaluation, conflict/publish/rollback |
| `tests/integration/test_aspeii_ctar.py` | Source/policy/model invalidation through actual CTAR services |
| `tests/unit/test_aspeii_evidence_verifier.py` | Malformed, stale, forged, omitted and mismatched bundle refusal |
| Existing frontend/browser suite | Real intent/evidence/review/evolution journeys with traces |

Do not rely on tests that only assert a method exists, DTO keys match the implementation, or a mock returned its configured value. Unit schema tests are useful structure checks but are insufficient to qualify the workflow.

## 7. Evidence Bundle and Completion Algorithm

Use ignored runtime output such as `.audit-scratch/aspeii/<run-id>/`; add small curated fixture manifests to version control. Never place secrets in the bundle. A portable bundle contains:

```text
manifest.json
requirements.json
environment.json
source-manifest.json
dependency-manifest.json
configuration-redacted.json
cases.jsonl
api/
worker/
database/
adapters/
browser/
performance/
recovery/
verifier-result.json
signatures/
```

Required manifest fields: schema version, run ID, requirement/plan digests, release artifact digest, Git commit, dirty-tree manifest, environment, profile, adapter/model/database versions, start/end UTC times, random seeds, expected case and clause counts, all artifact paths/digests, omissions, signer/trust profile where used. Relative artifact paths must resolve within bundle root; reject traversal, symlink escape, oversized content and untrusted executable attachments.

Required per-case fields: stable case ID, clause IDs, scenario ID, input/expected-output refs, test runner and verifier versions, start/end, actual observed values, outcome, raw artifacts, backend/transport mode, independent effect observation, error/skipped reason, fixture/build/config digests. Screenshots attach to a case but cannot replace its effect assertions.

Algorithm:

```text
load frozen registry and expected profile matrix
validate schema, counts, identifiers, reference integrity and bundle bounds
verify source/build/dependency/configuration identities against release candidate
verify artifact digests and signatures according to the declared trust profile
for each clause:
    find required behavior cases and integration levels
    reject missing, skipped, flaky, stale, inconclusive or mismatched observations
    verify actual expected assertions and independent effect evidence
    mark VERIFIED only when every required case for this profile passes
verify shared-contract and all mandatory end-to-end gates
compute verified_clauses / 216 without dropping deferred or blocked clauses
emit per-profile verdict and all unresolved reasons
full_completion = all clauses VERIFIED and all required gates/profiles PASS
```

The verifier checks outcomes independently of the application component. It cannot prove arbitrary logs are honest without a trusted runner and protected collection boundary; record that trusted base. Signing the bundle adds integrity, not truth. Where raw protected content is intentionally omitted, classify the affected result as limited verification unless authorized independent verification supplies the required evidence.

### 7.1 Example Receipt Skeleton

This is a schema illustration, not a passing receipt. `NOT_RUN` is an illustrative case status that the final verifier must reject as completion evidence.

```json
{
  "schema_version": "aspeii-evidence/1",
  "run_id": "example-not-executed",
  "profile": "local-sqlite",
  "release_artifact_digest": null,
  "requirements_digest": null,
  "cases": [
    {
      "case_id": "approval-missing-no-dispatch",
      "clause_ids": ["ASPEII-RQ-020.C02", "ASPEII-RQ-035.C03"],
      "scenario_id": "ASPEII-E2E-05",
      "status": "NOT_RUN",
      "expected": {"handler_calls": 0},
      "observed": null,
      "artifacts": []
    }
  ],
  "completion": {"verified": 0, "required": 216, "verdict": "INCOMPLETE"}
}
```

## 8. Commands and Execution Discipline

These existing commands are suitable only after checking installed dependencies and project conventions. They do not implement ASPEII by themselves.

```powershell
python -m pytest tests/unit/test_agent_runtime.py tests/unit/test_governed_agents.py tests/unit/test_provenance.py
python -m pytest tests/integration/test_mcp_transport.py
npm --prefix frontend run typecheck
npm --prefix frontend run build
```

Add scoped ASPEII test commands once those suites exist. Capture JUnit/JSON case outputs and the structured evidence collectors. Use pytest strict markers as configured; tests must execute, not merely collect. Browser tooling must be discovered from the existing repo and dependencies before choosing a runner; a new Playwright integration is appropriate if no equivalent supported harness exists.

Target future commands, to implement and verify before presenting as working:

```text
eoip aspeii inspect --intent <id> --json
eoip aspeii evaluate --spec <authorized-evaluation-spec> --json
eoip aspeii receipts verify --bundle <path> --trust <trusted-key-manifest> --json
eoip aspeii qualification --profile <profile> --json
python scripts/verify_aspeii_evidence.py --registry <path> --bundle <path> --release-manifest <path>
```

The evidence verifier exits 0 only for PASS of the requested scope/profile, 1 for failed/incomplete evidence, and 2 for malformed inputs/internal verification failure. It must never skip a requested profile because dependencies are unavailable. Hosted-provider calls require configured budget and test credentials; record actual usage. No new production secrets should appear in command-line arguments or logs.

ASPEII ledger statuses and the IP plan's statuses are separate reporting contracts. Map IP `NOT-STARTED` to ASPEII `OPEN`, `IN-PROGRESS`/`CODE-COMPLETE`/`EVIDENCED` to `IN_PROGRESS` until the required evidence verifies, and IP `VERIFIED` to ASPEII `VERIFIED` only for the overlapping clauses and matching artifact/profile. Preserve original status values in their own ledgers. A failed ASPEII integration cannot inherit completion merely because an IP component is verified in isolation.

During frontend implementation, run the local dev server on a free port and provide its actual URL. During documentation-only work no server is needed. Completion of this plan eventually requires testing the packaged frontend/API configuration, not just the Vite development proxy.

## 9. Migration and Rollout

### 9.1 Legacy Data Classification

| Legacy data | Migration behavior |
| --- | --- |
| `CERTIFIED` from confidence or unresolvable strings | Preserve legacy value for history; new assurance UNKNOWN until independently verified |
| Existing approved proposal | Preserve historical decision; no new execution authority until bound canonical action and current checks exist |
| HMAC attestation | Import as legacy integrity record with known key/format limits; do not re-sign as if original public-key proof existed |
| Untyped tool output / source reference | Store origin and original content; new epistemic support UNKNOWN until qualified |
| In-memory state | Export only through an explicit verified snapshot while process is live; no invented historical events after loss |
| Existing ontology version | Import immutable snapshot and observed provenance; establish governed active head after validation, not a fabricated paired-evaluation receipt |
| Graph Neurons prediction | Map to HYPOTHESIS with model/version provenance; preserve separation from asserted graph facts |

### 9.2 Deployment Sequence

1. Back up and verify restoration of existing state; inventory legacy records and non-migratable artifacts.
2. Install additive schemas and read adapters with features disabled for consequential actions.
3. Backfill typed references and provenance; label unknown states conservatively and report counts.
4. Run shadow checking on read-only and proposed actions. Capture discrepancies; shadow mode cannot claim prevention.
5. Qualify one nonproduction workspace with enforced local graph correction and real MCP reads.
6. Enable enforced actions for explicitly qualified adapters and tenants after end-to-end acceptance.
7. Enable semantic candidate evaluation in isolated environments; publication remains separately approval-gated.
8. Expand supported profiles only with new evidence. Retire unsafe legacy mutation paths after compatibility migration.
9. Verify rollback to the prior compatible application/schema state without re-enabling insecure execution paths.

A migration must be resumable/idempotent, record processed/failed counts, and detect modified source revisions during backfill. Current read/admission controls must not wait for a long backfill to finish. Missing evidence remains UNKNOWN rather than being bulk-promoted.

### 9.3 Required Runbooks

| Incident | Required operator procedure and check |
| --- | --- |
| Checker unavailable | Fail consequential admission; retain readable authorized records; recover verifier and recheck pending actions |
| Authority DB unavailable | Stop dispatch and publication; show degraded readiness; reconcile after recovery |
| Signing key suspected compromised | Revoke key, stop affected issuance, rotate trusted manifest, retain historical compromise status; reverify dependent trust policy |
| Worker lost during dispatch | Fence worker, preserve UNKNOWN_OUTCOME, inspect external operation status, resolve once |
| Source/policy revoked | Commit immediate access/admission denial, enqueue CTAR propagation, measure affected cache/derivative cleanup |
| Bad semantic candidate published | Freeze further publication, governed rollback/compatibility check, invalidate dependent artifacts and requalify |
| Evidence corruption | Quarantine affected receipts/claims, refuse completion, restore or reacquire legitimate evidence |
| Restore from backup | Isolate network/effects, restore authority first, verify consumed approvals/fences/heads, rebuild projections, reopen after reconciliation |

## 10. Performance and Experiment Reproduction

Use the exact requirements section 7 workload, hardware description and timing exclusions. Report actual environment differences and do not claim the reference target passed on a smaller substitute. Collect percentiles from raw samples; record queueing, storage, checker and adapter times separately as well as end-to-end latency.

Required experiment comparisons:

| Experiment | Baseline | Treatment | Decision |
| --- | --- | --- | --- |
| Semantic utility | Raw access and static parent view | Evaluated candidate view | Paired measured gain with frozen gates |
| Delegation usefulness | Same task with one qualified agent | Bounded delegated workflow | Report task success, cost, time and reviewer burden; no mandatory claim that delegation always wins |
| Evidence discipline | Legacy provenance-presence/confidence paths | Typed support and independent checking | Detect planted laundering cases without losing valid supported claims |
| Action governance | Existing presence-only approval test fixture | Bound approval plus final dispatch checks | Zero forbidden effects in mandatory corpus |
| Recovery | Normal execution | Crash/retry/revocation/restore | Same authorized final state or explicit unknown outcome, never duplicate unapproved effect |

Report failures and uncertainty. A feature can be correctly implemented yet fail to improve a workload; retain the parent semantic version and present the research result honestly. Performance/quality claims are per tested profile, not transferred from published PCAA or EvoOntology numbers.

## 11. Release Matrix and Missing Inputs

| Profile / prerequisite | Required qualification | Missing input behavior |
| --- | --- | --- |
| Customer-installed local SQLite, Windows | Actual installation, one-worker recovery, no-egress mode, browser/CLI | BLOCKED profile if environment unavailable |
| Customer-installed local SQLite, Linux | Same behaviors in Linux package | Separate evidence, not inferred from Windows |
| Multi-worker PostgreSQL/SaaS Linux | Concurrency, tenant isolation, keys, backups, workers, packaged frontend/API | No SaaS readiness claim without this run |
| MCP stdio | Real process and output limits | Explicit unsupported/unavailable state |
| MCP HTTP | Real authenticated session, audience, redirect and schema tests | Explicit unsupported/unavailable state |
| Configured local model | Actual model identity, usage, typed outputs and evaluated workload | Core still works; model-specific profile BLOCKED |
| Configured hosted model | Approved test budget/egress, exact deployment/version, evaluation | No paid calls or provider qualification invented |
| Real sandbox write connector | Valid test account/resources, least privilege, observed write/readback and cleanup | External-effect qualification BLOCKED |
| Production retention/destinations/owners | Explicit deployment configuration | Dependent production capability unavailable |

The engineering defaults are already selected in the requirements. Do not repeatedly ask for routine implementation choices. Record genuinely external facts only when they are available, and continue all independent work while those profiles remain blocked.

## 12. Fresh-Agent Handoff and Final Acceptance

At each completed work package, update the registry with exact code revision, changed paths, migrations, observed cases, evidence bundle location, dependencies and next runnable task. Record uncommitted changes with hashes. Never label an entire package complete when one assigned clause lacks required evidence.

Handoff format:

```text
Current source/build identity:
Supported and tested profiles:
Work packages completed with evidence:
Clause totals: VERIFIED / OPEN / BLOCKED / FAILED / STALE / DEFERRED:
Shared-contract and E2E gate status:
Changed files and migrations:
Actual commands executed and outcomes:
Evidence bundle and independent verification result:
Known failures, residual risks and unavailable integrations:
Next exact package/task and prerequisites:
Concurrent user changes to preserve:
```

Final acceptance requires a reviewer or independent verifier to reproduce the declared behavior from the release artifact, fixture manifests and instructions. A clean repository, attractive GUI, generated tests, passing schema checks, or a signed report alone is insufficient. Report full completion only when all 216 clauses, mandatory shared contracts, end-to-end scenarios and supported release profiles have current qualifying evidence.

<!-- tracker-integration -->

## 13. Tracker Procedure for the Implementing Agent

This section tells an agent exactly how to record ASPEII progress in the EOIP programme tracker. It adds no new scope. The clause registry built in WP01 stays the authoritative ASPEII registry; the programme ledger mirrors it item for item so the owner can follow all four programmes in one place.

### 13.1 Files

| File (copy into the repository) | Purpose |
|---|---|
| `tools/tracker/EOIP-programme-tracker.html` | Interactive tracker for ASPEII, CIP, IP and Graph Neurons (open in a browser; state is kept in the browser and exported as JSON) |
| `tools/tracker/EOIP-programme-registry.json` | Every tracked item: id, programme, kind, parent, work package or phase, source `file:line`, normative text and its SHA-256 |
| `tools/tracker/programme_rules.js` | The single rules engine used by the tracker page and the verifier |
| `tools/tracker/verify_programme_ledger.mjs` | Command-line verifier; exit 0 only when the requested scope is complete with no problem |
| `docs/programme/programme-ledger.json` | The committed consolidated ledger (`eoip-programme-ledger-v1`), exported from the tracker or written by agents |

### 13.2 Release Profile Identifiers

| Tracker item | Profile id used in evidence | Plan §11 row |
| --- | --- | --- |
| `ASPEII-PROF-01` | `local-sqlite-windows` | Customer-installed local SQLite, Windows |
| `ASPEII-PROF-02` | `local-sqlite-linux` | Customer-installed local SQLite, Linux |
| `ASPEII-PROF-03` | `postgres-saas-linux` | Multi-worker PostgreSQL/SaaS Linux |
| `ASPEII-PROF-04` | `mcp-stdio` | MCP stdio |
| `ASPEII-PROF-05` | `mcp-http` | MCP HTTP |
| `ASPEII-PROF-06` | `local-model` | Configured local model |
| `ASPEII-PROF-07` | `hosted-model` | Configured hosted model |
| `ASPEII-PROF-08` | `sandbox-write-connector` | Real sandbox write connector |
| `ASPEII-PROF-09` | `production-config` | Production retention/destinations/owners |

A profile whose environment is unavailable is recorded `BLOCKED` with the missing input named (§11). It is never inferred from another profile.

### 13.3 Gate Order Used by the Tracker

The "Depends on" sentences in §4 mix hard prerequisites with incremental notes. The tracker orders gates by the hard prerequisites below; incremental notes (WP07 runtime integration after WP08, WP08 harness from WP01/WP16, WP12 foundations from WP16) do not block a gate. ASPEII gates are not start-blocking: the tracker warns when a gate closes before its prerequisites, and ASPEII-WP18 requires every ASPEII item.

| Gate | Package | Closes after | Covers |
| --- | --- | --- | --- |
| `ASPEII-WP01.GATE` | Baseline and Traceability | — | ASPEII-RQ-001, ASPEII-RQ-035 |
| `ASPEII-WP02.GATE` | Contracts and Transactional Storage | WP01 | ASPEII-RQ-002, ASPEII-RQ-003 |
| `ASPEII-WP03.GATE` | Identity and Epistemic Foundation | WP02 | ASPEII-RQ-004, ASPEII-RQ-012, ASPEII-RQ-013, ASPEII-RQ-014, ASPEII-RQ-015 |
| `ASPEII-WP04.GATE` | Canonical Actions, Checker and Approvals | WP03 | ASPEII-RQ-018, ASPEII-RQ-019, ASPEII-RQ-020 |
| `ASPEII-WP05.GATE` | Gateway, Actual Effects and Receipts | WP04 | ASPEII-RQ-021, ASPEII-RQ-022 |
| `ASPEII-WP06.GATE` | Real MCP and Connector Qualification | WP05 | ASPEII-RQ-023, ASPEII-RQ-021 |
| `ASPEII-WP07.GATE` | Intent and Outcome Contracts | WP04 | ASPEII-RQ-005, ASPEII-RQ-006 |
| `ASPEII-WP08.GATE` | Delegation, Grants and Recoverable Scheduling | WP05, WP07 | ASPEII-RQ-007, ASPEII-RQ-008, ASPEII-RQ-009, ASPEII-RQ-010 |
| `ASPEII-WP09.GATE` | Human Review and Epistemic Challenges | WP04, WP08 | ASPEII-RQ-011, ASPEII-RQ-016, ASPEII-RQ-017 |
| `ASPEII-WP10.GATE` | Semantic Access and Grounded Builder | WP03, WP06, WP07 | ASPEII-RQ-024, ASPEII-RQ-025 |
| `ASPEII-WP11.GATE` | Trajectories and Candidate Isolation | WP08, WP10 | ASPEII-RQ-026, ASPEII-RQ-027 |
| `ASPEII-WP12.GATE` | Paired Evaluation | WP11 | ASPEII-RQ-028 |
| `ASPEII-WP13.GATE` | Publication, CTAR and Rollback | WP05, WP12 + `CIP-P4.GATE` (CTAR implemented) | ASPEII-RQ-029, ASPEII-RQ-030 |
| `ASPEII-WP14.GATE` | HTTP, CLI and Event Integration | WP03, WP04, WP05, WP06, WP07, WP08, WP09, WP10, WP11, WP12, WP13 | ASPEII-RQ-031 |
| `ASPEII-WP15.GATE` | Integrated GUI Workflows | WP14 | ASPEII-RQ-032, ASPEII-RQ-011 |
| `ASPEII-WP16.GATE` | Independent Evaluation and Adversarial Harness | WP15 | ASPEII-RQ-034, ASPEII-RQ-035 |
| `ASPEII-WP17.GATE` | Operations, Deployment and Migration | WP13, WP14, WP15, WP16 | ASPEII-RQ-033, ASPEII-RQ-003 |
| `ASPEII-WP18.GATE` | Final Release Evidence and Handoff | WP01, WP02, WP03, WP04, WP05, WP06, WP07, WP08, WP09, WP10, WP11, WP12, WP13, WP14, WP15, WP16, WP17 | ASPEII-RQ-036 |

### 13.4 Per-Case Update Loop

1. Before work, set the clause to `IN_PROGRESS` with your owner id and work reference.
2. Implement through the real public or service boundary (§1). Commit. Optionally record `CODE_COMPLETE` with the commit and changed paths; this still reports `IN_PROGRESS` and earns no credit.
3. Execute the case through the evidence collector into `.audit-scratch/aspeii/<run-id>/`. Record `EVIDENCED` with the fields in §13.5.
4. Run `scripts/verify_aspeii_evidence.py` as a separate process or reviewer. Only its exit 0 for the clause's profile lets the reviewer record `VERIFIED` with `verifier-result.json` as the verification reference. The reviewer must not be the producer.
5. When any source, configuration, dependency or requirement text changes, record `STALE` and re-run. The verifier also reports a changed digest as stale.
6. Export the ledger (or write it directly) to `docs/programme/programme-ledger.json` and run:

```bash
# create an empty ledger once
node tools/tracker/verify_programme_ledger.mjs --init > docs/programme/programme-ledger.json
# check the ledger and recompute every evidence digest in the working tree
node tools/tracker/verify_programme_ledger.mjs --ledger docs/programme/programme-ledger.json --repo . --programme ASPEII
```

### 13.5 Evidence Required per Transition

A file path, class or function name, test-file name, test count, commit hash, green CI badge, screenshot or an agent's statement is never proof of completion on its own. The tracker and the verifier refuse EVIDENCED unless an executed run is recorded (command, exit code 0, environment, evidence path and its SHA-256, bound to the current requirement text), and refuse VERIFIED unless a reviewer who is not the producer re-ran it and recorded the verification reference.

| Target state | Required evidence (checked by the tracker and by `verify_programme_ledger.mjs`) |
|---|---|
| IN_PROGRESS | Owner and work reference (task card, branch, ledger draft or DR id). |
| CODE_COMPLETE | 40-hex commit and the changed paths. The paths are navigation only and are never proof. |
| EVIDENCED (reported IN_PROGRESS) | Commit; evidence path inside `.audit-scratch/aspeii/<run-id>/`; its SHA-256; producer; exact command; exit code 0; environment; release profile id (§13.2 of the plan); completion level L2–L6 (L0 design/source references and L1 static checks are not evidence, plan §1.1); executed case ids from `cases.jsonl`; attestation that it ran against the real boundary with no skipped, flaky, stale, inconclusive or mismatched case. |
| VERIFIED | Everything above plus: reviewer different from the producer, review date, verification reference `.audit-scratch/aspeii/<run-id>/verifier-result.json` produced by `scripts/verify_aspeii_evidence.py` with exit 0, and the reviewer's re-run attestation. `.ACC` items additionally need all six clauses VERIFIED. |
| FAILED | Failure note with the observed numbers or error, and a reference to the failing run. |
| BLOCKED | The blocking dependency, decision id or missing input. |
| STALE | What changed (source, artifact, environment or requirement text). |

Evidence digest: for a file, the SHA-256 of its bytes; for a directory, the SHA-256 of the UTF-8 text made of one line `<path relative to the directory>\t<sha256 of that file>\n` per file, sorted by path. `--repo` recomputes it and reports any mismatch as STALE.

### 13.6 Handoff Additions

Add to the §12 handoff: the verifier output for `--programme ASPEII`, the counts of tracker problems and open cross-programme decisions, and the next item ids. Decisions XP-02, XP-11, XP-22 and XP-24 hold ASPEII items; XP-10, XP-12, XP-13, XP-14, XP-23, XP-25, XP-26 and XP-27 are settled by requirements §2.1 and need only the owner's confirmation in the tracker.
