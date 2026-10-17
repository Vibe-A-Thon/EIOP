# EOIP Community and IP Requirements

Document ID: `CIP-REQ-2026-10-16`  
Prepared: 2026-10-16  
Status: normative engineering requirements; not an implementation or completion receipt  
Audience: coding agents, maintainers, QA, security, operations, community maintainers, and IP counsel  
Companion plan: [community-ip-implementation-plan.md](community-ip-implementation-plan.md)
Revision: 2026-10-17 — section 8 (tracker integration) appended; sections 1–7 unchanged.  

## 1. Purpose and Scope

This specification defines an EOIP capability for determining what agent-derived information becomes unsafe, unsupported, inaccessible, or stale after its inputs or operating conditions change, and for producing a bounded, auditable remediation plan. It also defines a reusable synthetic benchmark for measuring that behavior across agent systems.

The engineering name used here is **Change-Triggered Agent Repair (CTAR)**. The community benchmark is **Agent Mutation Resilience Benchmark (AMRB)**. These are project identifiers, not claims of novelty, ownership, patentability, or priority.

The deliverable is an integrated EOIP feature, not just a library, paper, demo, test files, or patent disclosure. Reuse existing graph, provenance, temporal, agent, policy, evaluation, API, worker, UI, and evidence facilities only after their actual runtime behavior is verified. A source path, symbol, documentation statement, or passing unit test alone is not proof that this specification is met.

### 1.1 Required Outcomes

1. Represent versioned dependencies from source facts and operating configuration to retrievals, agent runs, memories, evaluations, proposals, and other supported derived artifacts.
2. Detect relevant changes and compute a tenant-scoped, permission-aware downstream impact set.
3. Distinguish stale, revoked, quarantined, unknown, and still-supported outputs; do not collapse these into one confidence value.
4. Generate an explainable, deterministic repair plan, and execute only authorized, approved, reversible or explicitly irreversible in-platform actions.
5. Preserve temporal history without disclosing data that a principal is no longer authorized to access.
6. Demonstrate correctness, security, resilience, and performance through repeatable runtime receipts and a versioned synthetic benchmark.
7. Prepare a community benchmark without exposing tenant data, credentials, proprietary code, or unreviewed invention disclosures.

### 1.2 Out of Scope

- Automatically undoing payments, deployments, emails, external API calls, or other external side effects. CTAR may identify these, quarantine related EOIP artifacts, and create a human-reviewed reconciliation proposal.
- Replacing EOIP's source connectors, graph store, bitemporal model, authorization service, agent runtime, evaluation engine, or proposal/approval mechanism.
- Claiming that all historical answers must always be retained or deleted. Retention, legal hold, privacy, and access policies govern preservation and purge.
- Claiming novelty, patentability, patent eligibility, non-obviousness, freedom to operate, or a priority date. These require qualified legal review and claim-level searches in relevant jurisdictions.
- Publishing code, fixtures, papers, invention disclosures, or APIs as an open standard until the authorized owner approves the exact artifacts, license, and disclosure timing.
- Treating synthetic benchmark results as proof of production readiness or general agent safety.

## 2. Evidence and Completion Rules

### 2.1 Research and Prior-Art Caution

The motivating research found extensive existing work in graph-grounded answers, provenance, agent evaluation, stateful tool environments, temporal agent memory, evidence-gated execution, and graph-traversal feedback. Selected references include [US20250390491A1](https://patents.google.com/patent/US20250390491A1/en), [US10681061B2](https://patents.google.com/patent/US10681061B2/en), [EviBound](https://arxiv.org/abs/2511.05524), [tau-bench](https://arxiv.org/abs/2406.12045), [ToolSandbox](https://arxiv.org/abs/2408.04682), and [Zep](https://arxiv.org/abs/2501.13956). These are search leads, not an exhaustive prior-art analysis. An exact-phrase miss is not novelty evidence.

The engineering hypothesis worth investigating is an integrated, temporal, tenant-scoped change-impact and repair lifecycle, especially its handling of access revocation, evidence correction/retraction, independent surviving support, and downstream agent artifacts. This is not an assertion that the mechanism is new or patentable.

### 2.2 Definition of Done

An acceptance clause is complete only when all applicable conditions pass on the release candidate:

1. Real behavior is exercised through its public or trusted service boundary, including persistence and worker behavior where applicable.
2. Positive, negative, authorization, concurrency, restart/replay, and failure scenarios pass.
3. API, worker, persistence, agent, UI, and deployment integration are tested against the actual supported profile. In-memory unit tests alone are insufficient.
4. A machine-readable receipt is bound to source revision, clean/dirty worktree state, artifact hashes, environment, exact commands, exit codes, test identities/outcomes, benchmark data version, and runtime configuration.
5. A reviewer can reproduce the receipt, or an external prerequisite is clearly recorded as a blocker. Skipped/blocked required gates are not passes.
6. Assertions verify observable behavior rather than implementation details or self-reported success fields.
7. Documentation, OpenAPI, configuration, migrations, and runbooks match tested behavior.

Paths, symbols, test names, requirement markers, screenshots, checkboxes, coverage, green builds, and historical test reports are supporting evidence only. Report **engineering completion**, **evidence coverage**, and **release readiness** separately. Never report 100% while a mandatory clause is missing, skipped, blocked, stale, or source-referenced only.

## 3. Domain Model and Required Semantics

### 3.1 Dependency Direction

Represent dependencies as `dependent_artifact DEPENDS_ON input_artifact`. Impact starts at a changed input and traverses the reverse index to find dependents. Storage, API representations, UI arrows, and benchmark fixtures must use this direction consistently.

Each dependency edge is tenant-scoped and contains a stable edge ID, tenant ID, dependent artifact ID/revision, input artifact ID/revision, dependency kind, required/optional flag, creation time, schema version, and provenance for how it was observed. Do not copy source payload into dependency metadata.

### 3.2 Artifact Kinds

The first release supports these kinds or an explicitly versioned mapping to existing EOIP records:

| Kind | Meaning |
| --- | --- |
| `SOURCE_REVISION` | Versioned source record/evidence, graph fact, or source deletion/retraction marker. |
| `GRAPH_REVISION` | Entity, relationship, schema snapshot, or graph version used by a derivation. |
| `RETRIEVAL_RESULT` | Evidence manifest, retrieved subgraph, or retrieval snapshot used as model context. |
| `AGENT_RUN` | One execution identified by stable run ID and immutable run revision. |
| `MEMORY_RECORD` | Persisted agent memory, including scope, owner, TTL, and provenance. |
| `PROMPT_VERSION` | Exact prompt/template version and rendered-input digest where permitted. |
| `AGENT_CONTRACT_VERSION` | Agent configuration, tool allowlist, budgets, policy, and contract revision. |
| `MODEL_VERSION` | Provider/model/deployment ID and immutable version/digest when available. |
| `TOOL_SCHEMA_VERSION` | Tool implementation/schema/version, excluding secret configuration. |
| `POLICY_VERSION` | Authorization, retrieval, privacy, retention, or egress policy revision. |
| `ONTOLOGY_VERSION` | Ontology/schema mapping revision affecting interpretation. |
| `EVALUATION_RESULT` | Evaluation case/run/baseline and exact dataset/evaluator versions. |
| `PROPOSAL` | In-platform proposed action linked to run and justification evidence. |
| `EXTERNAL_ACTION_REFERENCE` | External-side-effect reference; EOIP cannot claim it can reverse it. |

Unknown kinds or dependency semantics fail conservatively; they are not silently treated as unaffected.

### 3.3 Artifact Identity and Content

Each artifact has stable ID, tenant, kind, revision, lifecycle state, created/recorded time, optional valid-time interval, actor/owner, classification, retention/deletion policy, and versioned dependency set. Separate immutable identity from revisioned lifecycle state.

Record digests of exact relevant inputs/configuration when possible. Canonicalization specifies UTF-8, key ordering, numeric serialization, null handling, Unicode normalization, and schema version. A digest proves equality under that canonicalization; it does not prove truth, authorization, authorship, or safety.

Never copy raw secrets, credentials, unrestricted source content, or unnecessary personal data into dependency metadata, traces, fixtures, or receipts. Store stable references and redacted metadata. Re-check authorization at read time; a citation/cache does not grant access.

### 3.4 Change Kinds

Recognize separately: `SOURCE_CREATED`, `SOURCE_CORRECTED`, `SOURCE_RETRACTED`, `SOURCE_DELETED`, `SOURCE_ACCESS_REDUCED`, `SOURCE_ACCESS_REVOKED`, `TENANT_SCOPE_CHANGED`, `POLICY_CHANGED`, `RETENTION_POLICY_CHANGED`, `ONTOLOGY_CHANGED`, `PROMPT_CHANGED`, `AGENT_CONTRACT_CHANGED`, `MODEL_CHANGED`, `TOOL_SCHEMA_CHANGED`, `EVALUATION_DATASET_CHANGED`, `EVALUATOR_CHANGED`, `LATE_EVENT`, `DUPLICATE_EVENT`, and `UNKNOWN_CHANGE`.

Changes originate only from authenticated, authorized internal mutations or validated events from approved connectors. Simulation is isolated to a test sandbox and cannot mutate production history.

### 3.5 Lifecycle States

| State | Required interpretation |
| --- | --- |
| `CURRENT` | Dependencies are verified current for declared view and caller is currently authorized. |
| `STALE` | A dependency changed; impact is known, but repair or proof of unaffected status is incomplete. |
| `REVOKED` | A source, permission, consent, or policy change makes use/disclosure impermissible. |
| `QUARANTINED` | Blocked from normal retrieval/display/use pending review or repair. |
| `UNKNOWN` | Dependency history is incomplete, corrupt, or not understood; fails closed for consequential use. |
| `SUPERSEDED` | Replaced by newer derived artifact; retained only under policy. |
| `PURGED` | Content removed under authorized deletion; minimal non-sensitive audit facts may remain only if policy allows. |

`CURRENT` is relative to tenant, principal, policy revision, temporal coordinate, and dependency snapshot. It is not permanent or a model confidence score. State changes record event, actor/service, reason, revisions, timestamp, and plan/decision reference.

## 4. Functional Requirements

All requirements are mandatory for the first integrated release. Each `AC` is independently verifiable; no requirement closes until every child clause passes.

### CIP-RQ-001: Source and Scope Inventory

Inventory existing event, provenance, memory, agent trace, proposal, policy, evaluation, graph revision, authorization, storage, worker, API, UI, and deployment contracts. For each candidate integration, record observed request/response/schema, durability, tenant scope, auth path, and tests actually executed. Assign `REUSE_VERIFIED`, `EXTEND`, `REPLACE_WITH_APPROVAL`, or `NOT_PRESENT`; gaps have owners and tasks.

**Acceptance:** `AC-001.1` all domains inventoried; `AC-001.2` every reused boundary has runtime contract evidence; `AC-001.3` all gaps have owner/task; `AC-001.4` unrelated user worktree changes are preserved.

### CIP-RQ-002: Typed Dependency Contract

Implement versioned artifact and dependency schemas from Section 3. Validate IDs, kinds, revision references, tenant consistency, semantics, timestamps, and graph-size bounds. Reject empty IDs, cross-tenant edges, missing revisions, malformed times, unsupported schema versions, and invalid self-dependencies. Unknown semantic fields are never ignored.

**Acceptance:** `AC-002.1` contract tests cover valid round-trip and every invalid input/rejection. `AC-002.2` migration, unsupported-version rejection, deterministic canonical digest, and cross-tenant rejection pass through the persistence boundary.

### CIP-RQ-003: Dependency Capture

Capture direct dependencies when EOIP creates each supported retrieval, agent run, memory record, evaluation, and proposal. Include source/graph revisions, evidence manifest refs, prompt/contract/model/tool/policy/ontology versions, evaluator/dataset version, and tenant/principal context as applicable. Capture inputs actually read, not inferred from query text. Incomplete capture marks the artifact `UNKNOWN` with reason.

**Acceptance:** `AC-003.1` request-level tests cover retrieval, agent run, tool call, empty evidence, partial/budget-exhausted run, memory write, evaluation, and proposal. `AC-003.2` captured versions equal those consumed by runtime; incomplete capture persists `UNKNOWN` and cannot be presented as current.

### CIP-RQ-004: Durable Mutation/Event Processing

Use verified transaction/outbox or equivalent durable event semantics. A committed mutation cannot be lost if the process crashes before consumption. Duplicates are idempotent. Cursors and impact records recover after API/worker restart. If mutation and event cannot share a transaction, implement an explicit recoverable reconciliation protocol and pending state; do not claim atomicity or exactly-once delivery without proof.

**Acceptance:** `AC-004.1` crash injection at every listed mutation/publication/cursor boundary recovers without losing a committed change. `AC-004.2` duplicate delivery/replay converges to one logical impact and action.

### CIP-RQ-005: Change Classification and Provenance

Preserve source/event IDs, revisions, change kind, tenant, actor, policy context, valid/recorded times, causal correlation, and redacted digest metadata. Apply temporal ordering to late events; do not mutate current state from a late event without that policy. Reject/quarantine duplicate, malformed, or untrusted events; never permissively mark current.

**Acceptance:** `AC-005.1` tests verify change classification, ordering, duplicate handling, actor binding, and temporal semantics. `AC-005.2` stored event metadata contains no source payload, credential, or secret canary.

### CIP-RQ-006: Bounded Impact Computation

Compute transitive reverse dependency closure for authorized changed artifacts at an explicit temporal coordinate. Return direct/indirect paths, roots, revisions, states, and completeness/truncation metadata. Traversal is cycle-safe and deterministic, bounded by depth, nodes, fan-out, time, and tenant scope. Limits yield `complete=false` and reason, never a false complete result.

**Acceptance:** `AC-006.1` tests cover chains, diamonds, multiple roots, cycles, disconnected graphs, duplicate edges, and removed dependencies. `AC-006.2` property-based cases match a reference closure; limit/timeout cases report incomplete status and deterministic ordering.

### CIP-RQ-007: Independent-Support Analysis

For multi-source derived artifacts, determine whether a valid, authorized, non-retracted support path remains. Enumerate valid/invalid paths and assumptions. Do not keep an output current just because text/confidence is unchanged; do not invalidate independent support because one redundant source changed. Incomplete/uncertain dependencies yield `UNKNOWN` or `QUARANTINED` under risk policy.

**Acceptance:** `AC-007.1` cases cover one-of-many invalidation, all evidence invalid, contradictory surviving evidence, duplicate-content sources, and inaccessible evidence. `AC-007.2` incomplete dependency capture yields the required conservative state and cannot be marked current.

### CIP-RQ-008: Temporal and Historical Views

Evaluate explicit `valid_at` and `known_at`/recorded-time coordinates compatible with EOIP bitemporal behavior. Distinguish current belief from historical knowledge. Historical views still obey current authorization, retention, hold, and deletion policy. API/UI label coordinates and historical/current/partial/reconstructed status.

**Acceptance:** `AC-008.1` backdated correction, late arrival, retraction, and historical/current queries return the correct valid-time and known-time views. `AC-008.2` post-creation access downgrade and retention expiry remain enforced in historical views.

### CIP-RQ-009: Authorization Revocation Fast Path

Access reduction, revocation, tenant change, or policy update must deny affected reads synchronously at authoritative boundaries; background processing is not required to stop disclosure. Re-key/invalidate caches by principal, tenant, and policy revision. Prevent stale websocket, MCP, export, and browser state from serving restricted evidence. Avoid existence/count/timing leaks beyond policy.

**Acceptance:** `AC-009.1` downgrade blocks the next authoritative read before worker processing. `AC-009.2` REST, UI, MCP, export, cache, websocket/event stream all deny or safely redact before and after asynchronous processing without existence leakage.

### CIP-RQ-010: Repair Decision Matrix

Each impacted artifact gets a deterministic decision: `KEEP_WITH_PROOF`, `RE_EVALUATE`, `RETRACT`, `QUARANTINE`, `PURGE_IF_AUTHORIZED`, `RECONCILIATION_REQUIRED`, or `MANUAL_REVIEW`. Record changes, invalid/current dependencies, surviving support, policy revision, decision-rule IDs, uncertainty, reversibility, required role, and side effects. Keep requires persisted proof; unknown never defaults to keep.

**Acceptance:** `AC-010.1` table-driven tests cover every action and input class, including missing/unknown dependencies and surviving evidence. `AC-010.2` deterministic inputs produce identical decisions/digests regardless of input ordering; `KEEP_WITH_PROOF` requires persisted proof.

### CIP-RQ-011: Dry-Run Immutable Plan

Plan includes tenant, actor, event IDs, input/dependency snapshot, policy revision, affected artifacts, ordered actions, expected revisions, bounds, digest, creation/expiry, and completeness. Reject/recompute if revisions or policy change before approval/execution. Dry run cannot mutate source, graph, artifact content, or external systems; only an auditable plan record may be persisted.

**Acceptance:** `AC-011.1` persisted plan contains all required snapshot, scope, action, time, completeness, and digest fields. `AC-011.2` dry run has no prohibited side effects; stale snapshot, tampering, expiry, duplicate submission, and digest determinism are tested.

### CIP-RQ-012: Approval and Execution Safety

Reuse proposal/approval only if runtime tests prove actor, tenant, role, plan digest, policy revision, expiry, and single-use binding. Human approval is mandatory for purge, consequential retraction, evaluation baseline change, and external reconciliation. Automatic in-platform re-evaluation/quarantine requires explicit versioned policy. No unapproved write tool; approval cannot authorize another tenant or plan revision.

**Acceptance:** `AC-012.1` deny self-approval where prohibited, wrong tenant/role, altered/expired/replayed approval, and changed policy. `AC-012.2` runtime/tool registration cannot bypass governed approval or execute an unapproved write.

### CIP-RQ-013: Idempotent and Recoverable Execution

Use stable action IDs and expected revisions. Replays do not duplicate logical memory/evaluations/audit/proposals. Persist states `PLANNED`, `APPROVED`, `RUNNING`, `SUCCEEDED`, `FAILED_RETRYABLE`, `FAILED_FINAL`, `CANCELLED`, `NEEDS_REVIEW`; define bounded retries. Preserve prior state until mutation commits, support operator recovery, honor cancellation at safe checkpoints, and audit all attempts.

**Acceptance:** `AC-013.1` concurrent workers and duplicate retries produce one logical mutation/action. `AC-013.2` restart/cancellation/failure recovery never reports partial work as success and stays within retry policy.

### CIP-RQ-014: Evaluation Before Reinstatement

Pin evaluator, dataset, prompt, model, tool schema, policy, and graph/source snapshot. Compare candidate/baseline on correctness, evidence coverage/groundedness, policy violations, abstention, safety, latency, cost where available, and domain metrics. Missing metrics are `UNKNOWN`. Reinstate only if all mandatory quality/security gates pass and evidence remains authorized. Model judges cannot be sole oracle for deterministic invariants.

**Acceptance:** `AC-014.1` evaluation pins all required candidate/baseline inputs and verifies exact deterministic golden outcomes. `AC-014.2` probabilistic metrics declare paired method, sampling config, seed, and minimum sample count; missing/insufficient evidence blocks reinstatement.

### CIP-RQ-015: Evaluation Threshold Governance

Version, freeze, and assign owners to gates before candidate evaluation. Unauthorized disclosure, cross-tenant data, missing required dependency, integrity error, or unapproved side effect always fails. Domain thresholds may vary only within governed bounds. Baseline changes require actor/approval and dataset/evaluator digests. Never tune thresholds after seeing candidate results.

**Acceptance:** `AC-015.1` version binding, governed policy range, and approved baseline are enforced. `AC-015.2` candidate comparisons are immutable; threshold changes after result inspection and attempts to erase failed gates are rejected/audited.

### CIP-RQ-016: Read-Time Lifecycle Gate

Every API/UI/MCP/export retrieval rechecks tenant, authorization, state, retention, and policy. `STALE`, `REVOKED`, `QUARANTINED`, and `UNKNOWN` artifacts cannot silently appear current or enter new agent context. Provide safe state and authorized remediation details. Apply freshness to new runs and memory recall.

**Acceptance:** `AC-016.1` route/browser tests cover stale memory, citations, partial results, and export lifecycle behavior. `AC-016.2` hidden metadata is denied, and stale/revoked/unknown artifacts cannot enter a new context or be shown as current.

### CIP-RQ-017: Retention, Deletion, and Legal Hold

Purge only under approved retention policy and authorized role, after legal-hold checks. Remove/cryptographically erase content and content-bearing caches as required; check graph, files, logs, indexes, exports, browser caches, backups, replicas. Keep only minimum non-sensitive audit tombstone allowed by policy. Unavailable store means purge incomplete.

**Acceptance:** `AC-017.1` unauthorized purge and purge under legal hold are denied and audited. `AC-017.2` synthetic canaries are searched across every declared store/derivative and documented backup behavior; residual content or unavailable store makes purge incomplete.

### CIP-RQ-018: Tenant and Principal Isolation

Tenant-scope all records, edges, cursors, plans, receipts, queues, caches, exports, metrics with identifiers, and UI/API. Derive tenant from authenticated principal; caller selector requires authorized membership. Revalidate jobs at execution. Cross-tenant admin requires explicit scope/audit.

**Acceptance:** `AC-018.1` IDOR, guessed IDs, omitted filters, pagination mixing, cross-tenant edges, and cache collisions deny without leakage. `AC-018.2` event replay and worker payload tampering cannot cross tenant or principal scope.

### CIP-RQ-019: API Contract

Provide authenticated, versioned operations for artifact freshness; bounded impact preview; dry-run plan create/read; approve/execute/cancel/recover; paginated impact/repair history; and isolated non-production benchmark run/report. Routes may follow local conventions but cannot weaken observable behavior. OpenAPI documents scopes, tenant binding, limits, idempotency, errors, partial results, and states. MCP remains read-only unless an existing proposal-only boundary explicitly applies; never expose repair execution as a read-only tool.

**Acceptance:** `AC-019.1` OpenAPI schemas describe all required operations, auth scopes, limits, partial results, and errors. `AC-019.2` authenticated real API tests verify tenant scope, pagination, idempotency, and error behavior; MCP exposes no ungoverned write.

### CIP-RQ-020: Operational UI

Show change/version, impact completeness/bounds, artifact counts by state/action, valid/invalid evidence paths, temporal coordinate, policy/tenant context, reversibility, approvals, execution progress/errors, and receipts. Provide filtering, detail, pagination, authorized recovery controls, and truthful empty/loading/partial/error/denied states. No fabricated success or operational values.

**Acceptance:** `AC-020.1` real API browser journeys cover correction/repair, downgrade denial, partial impact, approval, execution, worker restart, and evidence. `AC-020.2` keyboard operation, responsive viewports, and truthful loading/empty/error/denied states pass.

### CIP-RQ-021: Performance and Bounds

All work is bounded and validated; caller limits cannot exceed server maxima. Initial profile: 10,000 dependency edges per tenant, 100 changed roots, closure capped at 10,000 artifacts, impact-preview p95 <= 5 seconds on declared reference environment. Access revocation blocks the next authoritative API read immediately without queue dependency. Record environment, graph shape, warm/cold state, concurrency, percentiles, and memory. Missing profile data invalidates measurement.

**Acceptance:** `AC-021.1` repeatable load test at the frozen profile meets closure and p95 targets and records p50/p95/p99, memory, queue age, errors, and truncation. `AC-021.2` timeout/oversize paths fail explicitly; revocation is immediate at read boundary; target changes require prior approved ADR.

### CIP-RQ-022: Observability and Audit

Emit redacted metrics/logs/traces for event lag, impact size/completeness, repair outcomes/retries, gate failures, denied stale/revoked reads, queue age and purge completeness. Correlate with non-secret IDs and tenant-safe pseudonyms. Audit plan/approval/execution/cancel/retry/purge/baseline actions. Observability must not create cross-tenant leakage.

**Acceptance:** `AC-022.1` emitted audit/log/metric records contain required correlation fields and redact secret/PII canaries. `AC-022.2` tenant isolation is verified and alerting/operator runbook is present and exercised.

### CIP-RQ-023: Failure and Recovery Semantics

Define behavior for corrupt journal, unavailable graph/dependency/policy store, worker crash, duplicate/late event, clock skew, partial traversal, provider outage, invalid benchmark, and failed evaluation. Uncertain safety-critical impact denies/quarantines. Health distinguishes degraded/ready. Replay is bounded and cannot duplicate external actions.

**Acceptance:** `AC-023.1` fault injection covers each listed dependency/event/agent failure and health reflects degraded versus ready. `AC-023.2` recovery converges safely or records a non-recoverable state with actionable operator steps.

### CIP-RQ-024: AMRB Dataset and Scenario Contract

Build a versioned, synthetic, license-pending package with schema, validator, deterministic seed, expected outcomes, threat model, and no customer/source data. Minimum scenario families:

1. One source corrected while independent support survives.
2. All supporting evidence retracted.
3. Source deleted with answer and memory descendants.
4. Permission downgrade after answer/cache creation.
5. Tenant isolation under colliding IDs.
6. Policy revision changes retrieval eligibility.
7. Ontology/schema change alters interpretation.
8. Prompt, agent contract, model, and tool schema changes.
9. Evaluator/dataset change does not mutate old result.
10. Backdated and late events.
11. Duplicate event and repeated repair.
12. Crash at each durable mutation/consumer checkpoint.
13. Cycle, fan-out/depth cap, missing edge, corrupted digest.
14. Legal hold/retention conflict during purge.
15. External action requires human reconciliation, never automatic rollback.
16. Policy/evaluation service unavailable; conservative state required.

Each case specifies initial graph/artifacts, tenant/principal, mutation, expected direct/transitive closure, state/action, forbidden disclosure/action, and deterministic oracle. No expected outcome depends solely on an LLM judge.

**Acceptance:** `AC-024.1` validator rejects missing fields, duplicate IDs, secret-shaped data, invalid refs, underspecified oracle, and unsupported schema. `AC-024.2` all 16 scenario families execute through real service/API integration with deterministic oracles, not mocks alone.

### CIP-RQ-025: AMRB Metrics

Report per-case and aggregate stale/revoked detection precision/recall; unauthorized disclosures (required zero); closure precision/recall; false-keep/invalidation; independent-support accuracy; action correctness/idempotency; crash convergence; truncation errors; latency/memory/retries/queue lag/cost; and unknown-dependency quarantine accuracy. Include numerators, denominators, confidence intervals, scenario strata, exclusions, and every failure. Never average away security failures or hide skips. Compare only matching benchmark/evaluator versions and environment declarations.

**Acceptance:** `AC-025.1` tests independently recompute every aggregate/confidence interval from raw outcomes and verify denominators/exclusions. `AC-025.2` any unauthorized disclosure or deterministic invariant failure fails the suite regardless of aggregate score.

### CIP-RQ-026: AMRB CLI and Reproducibility

Provide documented validate/run/compare/export commands using EOIP CLI conventions. Support fixed seed, explicit profile, bounded concurrency, no implicit egress, JSON and human output. Record benchmark/evaluator digest, source revision, redacted config fingerprint, exact command/environment, per-case outcomes, raw metrics, summary and receipt digest. Never connect to or mutate production by default.

**Acceptance:** `AC-026.1` clean-checkout runs reproduce deterministic outcomes/counts and schema-valid export receipts. `AC-026.2` malformed input, egress, and production-store selection fail; results are independently recomputable.

### CIP-RQ-027: Community Artifact Safety

Prepare benchmark schema, synthetic fixtures, validator, runner interface, expected-result docs, contribution/security policy. Do not publish automatically. Before release, authorized owner selects compatible license, reviews dependencies/assets, privacy/secrets and IP disclosure timing, approves destination. Contributions must be reproducible and pass validation/security checks. Results are not product certification.

**Acceptance:** `AC-027.1` exact package digest has owner, privacy/security, license, and destination approvals. `AC-027.2` missing approval blocks publication while local validation remains runnable; benchmark is not represented as certification.

### CIP-RQ-028: IP and Invention-Record Hygiene

Maintain a private access-controlled engineering record of dated human-authored problem statements, diagrams, algorithm versions, decisions, contributors, experiments, commands/results and digests. No secrets/customer data. Distinguish human contributions from model drafts. Do not send confidential details to external models/repos/issues without authorization. Do not make claims about AI inventorship or ownership based on tool ownership. Counsel/rightsholder owns patentability, inventorship, assignment, filing, defensive publication, licensing and FTO decisions. Agents may prepare a marked technical draft only when requested; never file/publish or claim patentability.

**Acceptance:** `AC-028.1` access control/redaction tests pass and contribution records distinguish human work from generated drafts. `AC-028.2` publication remains blocked absent authorized IP decision; no code or report automatically claims patent status.

### CIP-RQ-029: Documentation and Migration

Document architecture, state machine, schema, APIs, controls, operator procedures, deployment, retention/purge, backup/restore, replay/recovery, benchmark, limits and troubleshooting. Persistent changes require forward migration, compatibility, rollback or forward-repair, backup/restore and upgrade/downgrade tests. No migration required for optional ephemeral benchmark data unless selected persistence needs it.

**Acceptance:** `AC-029.1` architecture/API/operator/benchmark docs match the tested implementation in a clean walkthrough. `AC-029.2` migration from every supported prior schema and documented rollback/forward-repair are exercised.

### CIP-RQ-030: Traceability and Release Gate

Map every requirement/acceptance clause to executable scenario, observable, receipt and accountable package. Verifier rejects duplicate/missing IDs/clauses, absent JUnit cases, failed/skipped/blocked results, stale source hashes, benchmark mismatch, absent integration, and wrong scenario counts. A marker, test file, generated receipt or checkbox is not proof absent successful execution and revision/environment binding.

Report `NOT_RUN`, `FAIL`, `BLOCKED`, `PASS_WITH_EVIDENCE`. Engineering completion is 100% only when all mandatory clauses pass; release readiness is separate. Denominator changes require versioned owner approval and history.

**Acceptance:** `AC-030.1` verifier mutation tests remove requirement, clause, JUnit case, integration receipt, source hash, or benchmark case and prove 100% is denied. `AC-030.2` unit-only success never closes the feature; engineering, evidence, and release states remain separate.

## 5. Cross-Cutting Security and Privacy

1. Enforce least privilege and fail-closed authorization across API, MCP, UI, worker and CLI.
2. Keep credentials in approved secret injection; never place them in events, fixtures, logs, URLs, benchmark output or evidence.
3. Treat source text, agent output, tool arguments, imported benchmark data and graph fields as untrusted; injection cannot become repair instruction or evaluator oracle.
4. Propagate deletion/access changes to caches, memories, indexes, exports, websocket sessions and backups under policy.
5. Use synthetic fixtures and adversarial canaries; run secret/privacy scans before release.
6. Do not use production traces in an open benchmark without explicit authorization and privacy review.
7. Contribution templates never solicit credentials or confidential invention details.
8. Public claims describe limits and do not guarantee elimination of hallucination or data leakage.

## 6. Required End-to-End Scenarios

### CIP-E2E-01: Correction With Independent Support

Create two independent evidence sources supporting an agent result. Correct one. Verify impact and descendants, invalidated path, surviving path, pinned evaluation, and `CURRENT` only if all gates pass. Historical version is available only under authorized historical access.

### CIP-E2E-02: Revocation Before Worker Processing

Create answer, cache, citation and memory from restricted source. Downgrade access, then request through API/UI/MCP/export/cache before worker processing. Each path denies or safely redacts. After processing, verify lifecycle/audit and no redisclosure.

### CIP-E2E-03: Restart and Duplicate Recovery

Crash between mutation and consumption, restart API/worker, replay event twice. Verify one logical impact/action, correct cursor, deterministic plan, full descendants, and no fabricated success.

### CIP-E2E-04: External Action Reconciliation

Invalidate evidence for a proposal referencing an external deployment/notification. Mark for reconciliation and require human proposal. No reversal API call; no claimed rollback success.

### CIP-E2E-05: Full AMRB Run

From clean checkout, validate/run all scenarios, recompute metrics, bind source/environment, verify zero unauthorized disclosure/forbidden actions, export receipt. Skip/unavailable integration blocks full-pass label.

## 7. Requirement Map and Research

| Requirements | Concern | Evidence type |
| --- | --- | --- |
| `CIP-RQ-001..005` | Inventory, schemas, capture, durable events | Runtime contracts, storage and crash/replay tests |
| `CIP-RQ-006..010` | Impact, surviving support, time, authorization, decisions | Reference-oracle and security integration tests |
| `CIP-RQ-011..017` | Plans, approval, execution, evaluation, lifecycle, purge | API/worker E2E, restart, deletion, gate receipts |
| `CIP-RQ-018..023` | Tenant/security, API/UI, performance, observability, resilience | Cross-boundary E2E, load/fault-injection receipts |
| `CIP-RQ-024..027` | Synthetic benchmark and community package | Validator, reproducibility, owner/release approval |
| `CIP-RQ-028..030` | IP hygiene, docs/migrations, completion evidence | Restricted review, walkthrough, verifier mutation tests |

Starting references: [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [NIST GenAI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf), [OWASP GenAI Security Project](https://genai.owasp.org/llm-top-10/), [MCP specification](https://modelcontextprotocol.io/specification/2025-11-25), [USPTO Patent Public Search](https://ppubs.uspto.gov/pubwebapp/), [WIPO PATENTSCOPE](https://patentscope.wipo.int/search/en/search.jsf), and [EPO Espacenet](https://worldwide.espacenet.com/). Standards guide controls; they are not certification. Selected research/patent results are not exhaustive. Counsel/rightsholder must determine filing, ownership, jurisdiction, publication/license and FTO before external disclosure.

Implementation status: this document defines requirements only; it is not implementation or completion evidence.

<!-- tracker-integration -->

## 8. Tracker Integration

This section adds identifiers and reporting rules for the EOIP programme tracker; sections 1–7 are unchanged and nothing below is a requirement.

### 8.1 Tracked Identifiers

| Item | Identifier | Count |
| --- | --- | --- |
| Acceptance clause | `CIP-RQ-NNN.AC-NNN.n` (the requirement id joined to the native `AC` id, so receipts stay unambiguous) | 62 |
| End-to-end scenario | `CIP-E2E-01` … `CIP-E2E-05` | 5 |
| Plan task, phase gate, negative test, release item | see plan §12 | 76 |

Evidence manifests keep the native `requirement_id` and `acceptance_id` fields (plan §7); the tracker id is their concatenation.

### 8.2 Status Reporting and the Three Measures

| Tracker canonical state | Status written in this programme's own ledger |
|---|---|
| OPEN, IN_PROGRESS, CODE_COMPLETE, EVIDENCED, STALE | `NOT_RUN` |
| VERIFIED | `PASS_WITH_EVIDENCE` |
| BLOCKED | `BLOCKED` |
| FAILED | `FAIL` |

The tracker reports engineering completion (`AC` clauses PASS_WITH_EVIDENCE out of 62), engineering integration (phase gates P0–P7, CIP-E2E and the 13 mandatory negative categories) and community/release readiness (P8 gate and the release checklist) as three separate numbers, as §2.2 and plan §1.1 require. They are never averaged.

### 8.3 What Moves a Clause

A file path, class or function name, test-file name, test count, commit hash, green CI badge, screenshot or an agent's statement is never proof of completion on its own. The tracker and the verifier refuse EVIDENCED unless an executed run is recorded (command, exit code 0, environment, evidence path and its SHA-256, bound to the current requirement text), and refuse VERIFIED unless a reviewer who is not the producer re-ran it and recorded the verification reference.

| Target state | Required evidence (checked by the tracker and by `verify_programme_ledger.mjs`) |
|---|---|
| IN_PROGRESS | Owner and work reference (task card, branch, ledger draft or DR id). |
| CODE_COMPLETE | 40-hex commit and the changed paths. The paths are navigation only and are never proof. |
| EVIDENCED (reported NOT_RUN) | Commit; evidence path in the repository test-results convention found in P0 and its SHA-256; producer; exact command; exit code 0; environment and store/worker profile; the exact JUnit case ids that executed (clauses, scenarios, negatives); the executable scenario and observable (clauses); attestation of a real run with no skip. |
| VERIFIED | Everything above plus independent reviewer, review date, verification reference and re-run attestation; the previous phase gate VERIFIED (phases close in order). |
| FAILED | Failure note with the observed numbers or error, and a reference to the failing run. |
| BLOCKED | The blocking dependency, decision id or missing input. |
| STALE | What changed (source, artifact, environment or requirement text). |

### 8.4 Cross-Programme Decisions Holding CIP Items

| Decision | Subject | Items held below VERIFIED until DECIDED | Record as |
|---|---|---|---|
| XP-11 | One change stream for leases, CTAR and revocation | `CIP-RQ-004.AC-004.1` | DR-IP (REQ-LSE-002) + CIP ADR (P0.3) |
| XP-21 | Branching and commits: CIP forbids without authorisation, IP prescribes | `CIP-P0.GATE` | Owner authorisation record |

- **XP-11 One change stream for leases, CTAR and revocation.** One transactional outbox publishes `kgf.graph.changed` (REQ-LSE-001). CIP adds the non-graph change kinds (access, policy, prompt, model, tool, evaluator) to the same outbox with the CIP-RQ-005 metadata. Lease revocation, CTAR intake and ASPEII admission invalidation are consumers of that one stream. Synchronous read denial on revocation (CIP-RQ-009) does not wait for any consumer.
- **XP-21 Branching and commits: CIP forbids without authorisation, IP prescribes.** Before CIP code work starts, the owner records whether CIP work may branch and commit (and the naming scheme, e.g. `cip/P<n>-<name>`). Until then CIP work stays in Phase 0 (documentation and inventory).

CTAR is owned here; ASPEII-RQ-030 integrates it and its WP13 gate waits for `CIP-P4.GATE`.
