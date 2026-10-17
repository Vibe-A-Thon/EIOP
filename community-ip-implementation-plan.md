# EOIP Community and IP Implementation Plan

Document ID: `CIP-PLAN-2026-10-16`  
Prepared: 2026-10-16  
Status: implementation plan; no task is complete by being listed here  
Normative requirements: [community-ip-requirements.md](community-ip-requirements.md)
Revision: 2026-10-17 — section 12 (tracker procedure) appended; sections 1–11 unchanged.

## 1. Mission and Completion Contract

Implement Change-Triggered Agent Repair (CTAR) in EOIP and prepare the Agent Mutation Resilience Benchmark (AMRB) as a reproducible synthetic community artifact. Do not publish automatically. Reuse existing EOIP graph/provenance/temporal/agent/policy/evaluation/worker/API/UI contracts only after runtime verification establishes they meet the requirements. Add only abstractions/storage needed to close proven gaps.

This plan does not assert novelty, patentability, freedom to operate, production certification, or a guaranteed completion date. Human/legal/ownership/environment decisions can block their release gate; report them honestly and do not mislabel them complete.

### 1.1 Independent Completion Measures

| Measure | Rule |
| --- | --- |
| Requirements | Every `CIP-RQ-*` and child `AC-*` has passing revision-bound evidence; none is missing, skipped, blocked or stale. |
| Engineering integration | API, worker, persistence, agent runtime, UI, benchmark runner and deployment profile pass integration/recovery tests. |
| Community/release readiness | Exact artifact digest has owner approval, privacy/security/license review, IP disclosure decision, destination approval and reproducible evidence. |

Do not collapse measures into one percentage. Use `NOT_RUN`, `FAIL`, `BLOCKED`, `PASS_WITH_EVIDENCE`. Engineering can be complete while publication is blocked; do not publish or claim readiness in that state.

### 1.2 Agent Operating Rules

1. Read this plan, `community-ip-requirements.md`, repository instructions and `git status` before edits; preserve unrelated work.
2. Revalidate every path, schema, route, test and command against current checkout. References below are investigation anchors only.
3. Before each package, record a task card: requirement IDs, falsifiable behavior hypothesis, cheapest falsifying check, write scope and evidence.
4. Make the smallest vertical change. Immediately run the narrowest behavior-scoped test; do not broaden before that check.
5. Run package-specific contract, security, persistence/restart and E2E checks after focused validation.
6. Never weaken auth/assertions to make tests pass; repair fixtures to use supported principal/tenant flows.
7. Do not put customer data/secrets in fixtures, traces, benchmark output, or IP records.
8. Do not publish, file, commit, create branches, launch paid infrastructure or contact external parties without authorization.

## 2. Starting Anchors and Reconciliation

The following are source-inspection anchors, not implementations accepted as complete:

| Anchor | Observed behavior | Required verification before reuse |
| --- | --- | --- |
| `packages/eoip/graph/evolution.py` | `SemanticChangeEvent`, hash-linked `ChangeJournal`, in-process `SemanticEventBus`; not durable delivery, and hash excludes before/after state. | Test journaling, integrity, atomicity, tenancy, crash windows and consumer recovery. Do not infer immutable payload integrity from chain hashes. |
| `packages/eoip/provenance/lineage.py` | `LineageService` traces `EVIDENCED_BY`/`INGESTED_IN` edges with bounded traversal. | Test coverage of agent outputs, memory, prompt/model/tool/policy versions and reverse impact. Add typed edges if absent. |
| `packages/eoip/agents/runtime.py` | Governed runtime, traces, memory, result cache, read-only tools. | Verify persistence, principal/tenant binding, consumed-version capture, cache invalidation and approvals. |
| `packages/eoip/agents/evaluation.py` | Golden cases check status/evidence/forbidden tools. | Verify it pins inputs and runs actual runtime; status-only pass is insufficient. |
| `packages/eoip/evaluation/engine.py`, `packages/eoip/platform_router.py` | Eval engine and `/eval/*` routes exist; inspected standard runner returns canned deterministic success-shaped scores. | Never use canned score as proof. Test real service outcomes; label any retained simulator explicitly. |
| `packages/eoip/graph/consumers.py` | Semantic change consumers/cursor state exist. | Verify checkpoint durability, tenant filters, idempotency, retries, corruption, multi-worker behavior. |
| `scripts/verify_requirement_evidence.py`, `tests/unit/test_requirement_evidence.py` | Conservative verifier scoped to MVP matrix; it does not claim application completion. | Preserve its current contract; add separate CIP manifest/verifier or backwards-compatible extension with independent tests. |
| `README.md`, API/agent/benchmark references | Describe current surfaces. | Update after behavior is verified; preserve dated audit history. |

Inspect actual store adapters, transactions, tenancy/authentication middleware, migrations, queue, UI, API registration, backup/restore, and test commands before choosing details. If no transactional outbox exists, use an ADR-backed recoverable protocol; do not represent a process-local lock as multi-replica-safe.

## 3. Target Architecture and Contracts

### 3.1 Logical Components

Implement/verify these components; they may be modules inside existing packages:

1. Artifact registry: tenant-scoped immutable artifact revisions and lifecycle state.
2. Dependency index: typed `dependent DEPENDS_ON input` records and reverse lookup.
3. Change intake: trusted, versioned events with durable cursor/replay.
4. Impact analyzer: bounded temporal reverse closure, authorization and surviving-support analysis.
5. Repair planner: deterministic decision rules and immutable plan digest.
6. Executor: policy-controlled approved in-platform actions with idempotency/recovery.
7. Evaluation adapter: pinned candidate/baseline comparison and mandatory security gates.
8. API/UI: authenticated workflow, state visibility, reviewer control and recovery.
9. AMRB: synthetic schema, validator, runner, metrics and result manifest.
10. CIP evidence verifier: requirement-to-runtime evidence aggregation, not source/test discovery alone.

### 3.2 Minimum Persisted Records

Map these logical records to strict versioned schemas and migrations. Names may follow local conventions, but no invariant may be omitted:

**Artifact:** `artifact_id`, `tenant_id`, `kind`, `revision`, `schema_version`, `lifecycle_state`, created/recorded time, optional valid interval, actor/owner refs, classification, retention ref, optional content digest, metadata digest, dependency snapshot.

**Dependency:** `edge_id`, tenant, dependent ID/revision, input ID/revision, dependency kind, required flag, observed-by/time, schema version.

**Change event:** `event_id`, tenant, kind, target, old/new revision, source event ref, actor, valid/recorded time, policy revision, correlation ID, redacted details, schema version and integrity digest.

**Impact result:** impact ID, tenant, event IDs, graph/dependency snapshot refs, temporal coordinate, principal/policy context, affected artifacts/paths, completeness/truncation reason, time and digest.

**Repair plan/action:** plan ID, tenant, impact, immutable action list, rule IDs, expected revisions, policy revision, digest, completeness, actor, expiry, approvals, state, attempt/idempotency IDs, error class and bounded retry data.

**Evaluation receipt:** candidate/baseline refs, evaluator/dataset/config digests, environment, raw outcomes, metric numerator/denominator, statistical method, pre-frozen thresholds, gate outcomes, source revision and digest.

Never place credentials, source content, personal data, or unrestricted model output in control records. Use references/digests and enforce read-time authorization.

### 3.3 Invariants

- Stable artifact identity; content/config change creates a revision.
- At-least-once event delivery yields one logical effect.
- `CURRENT` is relative to principal/tenant, policy revision, temporal coordinate and dependency snapshot.
- Permission reduction is enforced synchronously before async repair.
- Incomplete/corrupt dependency state cannot become current by default.
- Re-evaluation does not rewrite historic run evidence/baselines.
- Approval binds exact plan digest, tenant, principal/role, policy and expiry.
- Purge checks legal hold and all declared replicas/derivatives; unavailable store means incomplete.
- External side effects are human-reconciliation references only.
- Tenant derives from authenticated principal; selector requires membership authorization.

## 4. Phases, Work Packages, Dependencies, and Gates

Phases close in order at their gates. Parallelize only independent tasks with agreed contracts. An unverified prerequisite blocks dependent closure.

### Phase 0: Baseline and Decisions

**Requirements:** `CIP-RQ-001`, `CIP-RQ-028`, `CIP-RQ-030`  
**Tasks:** `CIP-P0.1` inventory; `.2` threat/privacy model; `.3` persistence/outbox ADR; `.4` API/UI/benchmark/evidence contracts; `.5` baseline execution.

1. Record source revision/worktree state, migrations, supported profiles and actual test/build/lint/typecheck commands/results.
2. Runtime-inspect source events, graph evolution/consumers, provenance, agent/memory/proposal, policy, evaluation, API/UI, tenancy, storage, backup/restore.
3. Map dependency directions/version semantics/tenant handling/change kinds; identify missing artifact kinds.
4. Write ADRs for persistence/index, outbox/reconciliation, ordering, schema, API ownership, deployment, and reuse decisions, with failure modes.
5. Freeze performance profile, benchmark schema/oracles, statistics, gate owners and evidence schema before candidate measurement.
6. Record rightsholder, disclosure, license, and counsel-review owners. Unknown owner is `BLOCKED`, not assumed.

**Exit:** complete runtime-qualified inventory; owner-approved ADRs; recorded baseline; no unsupported assumptions. External decisions block only their gates; internal non-disclosing work can continue.

### Phase 1: Contracts, Persistence, Migrations

**Requirements:** `CIP-RQ-002`, `CIP-RQ-003`, `CIP-RQ-018`, `CIP-RQ-029`  
**Tasks:** `CIP-P1.1` schemas; `.2` repositories; `.3` tenant query contract; `.4` migrations/adapters.

1. Add strict versioned schemas and canonical digest tests.
2. Persist artifacts, dependencies, lifecycle, plans, cursors and receipts. Include tenant in keys/predicates, enforce scoped references and uniqueness.
3. Migrate from every supported schema; test backup, rollback/forward repair, upgrade/downgrade and restart. Never silently rewrite history.
4. Test each required graph/store profile. If no atomic primitives, implement ADR recovery protocol and explicitly report unsupported profiles.
5. Bound graph sizes, fan-out, pagination, strings, metadata depth and payload size.

**Exit:** adapter contracts/migrations pass; cross-tenant/unknown-schema rejected; restart preserves data; recovery exercised.

### Phase 2: Dependency Capture and Durable Change Intake

**Requirements:** `CIP-RQ-003`, `CIP-RQ-004`, `CIP-RQ-005`, `CIP-RQ-022`, `CIP-RQ-023`  
**Tasks:** `CIP-P2.1` artifact versions; `.2` capture adapters; `.3` trusted change/outbox; `.4` replayable consumer; `.5` telemetry.

1. Instrument real retrieval, agent, memory, evaluation and proposal workflows to capture exact consumed revisions/config.
2. Incomplete capture produces `UNKNOWN` with reason and cannot look current.
3. Connect source/retraction/access/policy/ontology/prompt/model/tool/evaluator changes to durable events with tenant, actor, revision, time, correlation and redacted digest.
4. Make consumers idempotent/restart-safe; commit cursor after durable effect. Add reconciliation if mutation/event are not atomic.
5. Add lag/failure/duplicate/retry/unknown-kind telemetry and recovery runbook.

**Exit:** runtime dependency parity proven; crash, duplicate, late, corruption and restart tests pass; sandbox cannot mutate production.

### Phase 3: Impact and Freshness

**Requirements:** `CIP-RQ-006`, `CIP-RQ-007`, `CIP-RQ-008`, `CIP-RQ-009`, `CIP-RQ-016`, `CIP-RQ-021`  
**Tasks:** `CIP-P3.1` reverse closure; `.2` time/policy; `.3` independent support; `.4` read-time gate; `.5` load profile.

1. Implement deterministic cycle-safe reverse traversal from changed input.
2. Evaluate valid and recorded time separately; include temporal coordinates in identity and output.
3. Determine changed/retracted/inaccessible/incompatible/unknown dependencies; analyze surviving paths under current authorization.
4. Persist state with expected-revision/CAS semantics. Revocation blocks reads synchronously.
5. Return explicit completeness/truncation reason; store failure/timeout cannot be reported complete.
6. Measure only after target profile frozen; include environment and raw samples.

**Exit:** reference/property tests match; privacy/read-path tests pass; approved performance target passes; no cache/API bypass.

### Phase 4: Plans, Approval, Execution, Evaluation

**Requirements:** `CIP-RQ-010`, `CIP-RQ-011`, `CIP-RQ-012`, `CIP-RQ-013`, `CIP-RQ-014`, `CIP-RQ-015`, `CIP-RQ-017`, `CIP-RQ-023`  
**Tasks:** `CIP-P4.1` rules; `.2` immutable plan/digest; `.3` approval; `.4` executor; `.5` pinned evaluation; `.6` purge.

1. Implement versioned decision rules for every action/state with role, reversibility and effects.
2. Build dry-run immutable plans. Refuse stale snapshots/policy/digests.
3. Reuse approval service only after digest/tenant/actor/role/expiry/replay tests pass.
4. Execute only in-platform actions with idempotency and bounded retries. Human approval for purge, consequential retraction, baseline change and external reconciliation.
5. Evaluate pinned inputs and frozen thresholds; missing metrics/provider are not passes.
6. Purge only after retention/hold checks and store enumeration; unavailable store means incomplete.

**Exit:** exhaustive decision tests; approval/race/restart/retry tests converge safely; real evaluation used; no external side effects invoked.

### Phase 5: API, MCP, UI, Operations

**Requirements:** `CIP-RQ-009`, `CIP-RQ-016`, `CIP-RQ-018`, `CIP-RQ-019`, `CIP-RQ-020`, `CIP-RQ-021`, `CIP-RQ-022`, `CIP-RQ-023`  
**Tasks:** `CIP-P5.1` routes/schemas; `.2` authorization; `.3` UI; `.4` MCP; `.5` runbooks.

1. Inspect shared auth/error/pagination conventions before adding routes. Meet observable contract `CIP-RQ-019`; update OpenAPI.
2. Enforce principal/tenant in service methods; workers revalidate auth/policy.
3. MCP visibility is read-only. Repair actions stay proposal/approval-gated and are not exposed as read tools.
4. Build API-backed UI for impact, evidence paths, temporal view, plan, approval, execution, recovery and receipts; no fabricated success/data.
5. Test loading/empty/partial/denied/stale/error/retry/unavailable, keyboard and responsive states; clear/refetch cached state after access change.
6. Provide alert/dashboard, purge, replay/reconciliation, and safe operator recovery runbooks.

**Exit:** real API/UI journeys pass; OpenAPI/UI agree; denied data is not exposed; operator recovery rehearsed.

### Phase 6: AMRB and CIP Evidence Verifier

**Requirements:** `CIP-RQ-024`, `CIP-RQ-025`, `CIP-RQ-026`, `CIP-RQ-030`  
**Tasks:** `CIP-P6.1` schemas/fixtures; `.2` validator; `.3` runner/CLI; `.4` metrics; `.5` evidence verifier.

1. Implement all 16 scenario families from `CIP-RQ-024` with synthetic initial state, mutation, oracle, expected states/actions and forbidden outcomes.
2. Validate schema, fixed seeds, digests, input bounds and secret-shaped fixture rejection.
3. Run through integrated app/API/worker/store; test adapters may simulate providers, never bypass EOIP security/persistence/repair paths.
4. Compute metrics from raw outcomes; report denominators, intervals, exclusions, skips, environment, resources and failures. Any security failure fails suite.
5. Implement validate/run/compare/export CLI per current EOIP conventions, default no egress and no production store.
6. Create independent CIP evidence registry/verifier; do not break or repurpose MVP-only verifier. Mutation-test every evidence layer.

**Exit:** clean-checkout deterministic run; all 16 families pass; metrics recompute; no skips; revision/environment bound; verifier mutation tests deny false 100%.

### Phase 7: Release-Candidate Verification

**Requirements:** `CIP-RQ-001` through `CIP-RQ-030`; security/reliability focus: `CIP-RQ-009`, `CIP-RQ-017`, `CIP-RQ-018`, `CIP-RQ-019`, `CIP-RQ-020`, `CIP-RQ-021`, `CIP-RQ-022`, `CIP-RQ-023`, `CIP-RQ-027`, `CIP-RQ-030`  
**Tasks:** `CIP-P7.1` threat model; `.2` adversarial suite; `.3` chaos/restart; `.4` performance; `.5` evidence assembly.

1. Run IDOR, revocation, policy/cache bypass, injection, event tampering, approval replay, purge residual, secret leakage, egress and external-action prohibition.
2. Fault-inject API/worker/store restarts, duplicates, corruption, partial writes, provider/evaluator outage and concurrency.
3. Test exact frozen reference performance profile; retain samples. Target changes require prior approval.
4. Run required repository gates plus focused CIP and final-revision integration tests. Report unrelated failures; do not fix unrelated issues without scope approval.
5. Assemble revision-bound bundle: worktree state/diff digest, environment, locks, commands, node IDs/outcomes, benchmark, API/UI, migration, security, performance, artifact hashes.
6. Independent reviewer checks assertions and reproducibility. Any runtime/docs/OpenAPI/evidence mismatch blocks release.

**Exit:** all mandatory clauses `PASS_WITH_EVIDENCE`, no skipped/stale/unbound receipt, no unresolved high/critical security issue, performance passes, user work preserved.

### Phase 8: Community and IP Decision Gate

**Requirements:** `CIP-RQ-027`, `CIP-RQ-028`, `CIP-RQ-029`, `CIP-RQ-030`  
**Tasks:** `CIP-P8.1` private package; `.2` privacy/license/security review; `.3` owner/counsel decision; `.4` release authorization.

1. Assemble privately and hash exact package.
2. Run license/dependency inventory, secret scan, synthetic-data and provenance review.
3. Obtain rightsholder decisions on license, destination, contributor terms, and filing/defensive-publication/trade-secret/no-action; counsel reviews jurisdictional questions.
4. If decisions are absent, do not publish; set gate `BLOCKED`. Local development remains available.
5. Publish only approved digest and verify published bytes match; record date, owner, license, URL and integrity check.

**Exit:** release authorized and reproducible, or explicitly blocked. No agent selects a license or publishes to close a task.

## 5. Task Card and Acceptance Allocation

Every implementation task instantiates and updates this record with actual outcomes:

```yaml
task_id: CIP-P3.1
requirement_ids: [CIP-RQ-006]
acceptance_ids: [AC-006.1, AC-006.2]
source_anchors: [] # navigation only, never proof
behavioral_hypothesis: "A changed input reaches all and only dependents within declared bounds."
falsifying_check: "Compare service output to reference closure for chain, diamond, cycle and generated graphs."
write_scope: []
dependencies: [CIP-P1, CIP-P2]
positive_cases: []
negative_cases: []
authorization_cases: []
concurrency_restart_cases: []
integration_profile: "declared store + API + worker"
commands: []
receipt_ids: []
status: NOT_RUN
blockers: []
```

The acceptance registry contains exactly 62 child clauses: `CIP-RQ-001` has `AC-001.1` through `AC-001.4`; each `CIP-RQ-002` through `CIP-RQ-030` has the explicitly written `.1` and `.2` clauses (for example, `AC-002.1` and `AC-002.2`). The evidence registry must store complete IDs, not infer or abbreviate them in receipts.

Minimum evidence by phase:

| Phase | Required evidence |
| --- | --- |
| P0 | Runtime contract inventory, baseline transcript, ADRs, owner/disclosure decisions. |
| P1 | Schema positive/negative tests, migration from every supported schema, tenant and restart tests. |
| P2 | Runtime capture parity, ordering/idempotency, crash windows, replay and redaction. |
| P3 | Reference-closure/property tests, temporal, read-time revocation, bounded load receipt. |
| P4 | Complete decision matrix, digest/expiry/race, approval/role, real evaluation, purge completeness. |
| P5 | API/OpenAPI, browser journey, denied states, accessibility, MCP read-only, recovery rehearsal. |
| P6 | All scenario IDs, invalid fixture corpus, repeatable run, metric recomputation, verifier mutations. |
| P7 | Security, resilience, performance and final evidence bundle. |
| P8 | Exact digest and privacy/security/license/legal/owner publication decision. |

## 6. Validation Matrix

Discover actual commands during P0; examples below are validation categories, not assumed commands.

| Layer | Required validation |
| --- | --- |
| Domain | Focused schema/canonicalization/decision/traversal/state/metric tests; property tests against reference graph closure. |
| API | Authenticated contract, tenant, pagination, idempotency, error, OpenAPI and partial-result tests. |
| Storage | Every supported adapter, migration/recovery, concurrent writes, restart, backup/restore. |
| Worker/events | Durable intake, duplicate/late events, crash windows, replay, cursor recovery, queue/dead-letter. |
| Agent/evaluation | Exact runtime input versions, evidence/memory freshness, pinned evaluator/data/model, no canned success. |
| UI/E2E | Source mutation through impact/review/approval/execution; access downgrade across caches/exports. |
| Security | Tenant IDOR, least privilege, revocation, injection, MCP, egress, purge residual, external side-effect prohibition. |
| AMRB | Every scenario, raw outcomes, recomputed aggregates, repeatability and environment digest. |
| Performance | Frozen profile, p50/p95/p99, memory, queue age, errors, truncation, restart/fault behavior. |
| Release | Final revision, worktree inventory, dependency hashes, transcripts, receipts, docs/OpenAPI consistency, review. |

Run broad repository gates after focused checks. Report unrelated failures; if release policy requires that gate, it blocks the release claim.

## 7. Evidence Bundle Contract

Use the repository's established test-results/artifact convention discovered in P0; do not create a competing evidence store without an ADR. CIP manifest includes at least:

```json
{
  "schema_version": "cip-evidence-1.0",
  "run_id": "stable-run-id",
  "source_revision": "commit-or-explicit-uncommitted",
  "worktree_clean": false,
  "worktree_diff_sha256": "sha256-or-null",
  "created_at": "RFC3339 timestamp",
  "environment": {
    "os": "declared value",
    "python": "declared value",
    "node": "declared value or null",
    "store_profile": "adapter and version",
    "worker_profile": "declared profile",
    "configuration_sha256": "redacted config digest"
  },
  "requirements": [{
    "requirement_id": "CIP-RQ-001",
    "acceptance_id": "AC-001.1",
    "status": "PASS_WITH_EVIDENCE",
    "scenario_ids": ["CIP-E2E-01"],
    "test_case_ids": ["exact.junit.classname::test_name"],
    "commands": ["argv, exit code, duration, output digest"],
    "integration_receipts": ["artifact digest"],
    "reviewer": "authorized identity or null"
  }],
  "benchmark": {"version": "declared", "digest": "sha256", "case_count": 0},
  "security": {"critical": 0, "high": 0, "report_digest": "sha256"},
  "performance": {"profile_id": "declared", "report_digest": "sha256"},
  "release_readiness": "BLOCKED",
  "manifest_sha256": "canonical manifest hash with this field omitted"
}
```

Define actual value types, hashing, nullability, timestamps, artifact paths, size limits, and signature/attestation in schema. Do not retain placeholders literally. Verifier rejects missing/duplicate IDs or clauses, absent JUnit cases, nonzero exits, skips, stale revision, source hash mismatch, missing integration, scenario-count mismatch, invalid digest, or failed security invariants. A manifest generated by code under test is not trusted without component validation and independent digest/aggregate recomputation.

## 8. Mandatory Negative and Recovery Tests

Implement distinct cases for:

1. Invalid schema/version/canonicalization collision; cross-tenant edge, guessed ID, unauthorized principal, revoked job membership.
2. Duplicate, out-of-order, late, untrusted, unknown-kind event; event tampering and source mismatch.
3. Cycle, missing edge, corrupt digest, dangling revision, fan-out/depth cap, timeout, partial store.
4. Surviving evidence, no support, contradictory support, inaccessible evidence, incomplete capture.
5. Stale plan, changed policy/revision/digest, expired/wrong-tenant/replayed approval.
6. Concurrent workers, crash at each durable boundary, duplicate retry, cancellation, restart and dead-letter recovery.
7. Provider/evaluator/store/policy outage; partial metrics, insufficient sample, missing metric and post-result threshold tuning.
8. Access downgrade with API/browser/MCP/export/search/retrieval caches populated and before queue processing.
9. Purge under legal hold, unavailable replica, backup/export/cache residue and audit tombstone redaction.
10. External action requiring reconciliation; assert no outbound/reversal call.
11. Benchmark injection, schema/oracle alteration, duplicate case, nondeterministic seed, egress and production store selection.
12. Evidence manifest with source-only reference, marker but absent JUnit, skipped test, mismatched hash, stale benchmark or absent E2E receipt.
13. Keyboard-only UI, responsive overflow, partial/denied/stale/error/retry/recovery states.

## 9. Traceability and Change Control

Maintain canonical machine-readable rows per requirement and acceptance: ID, normative text hash/version, owner, package, dependencies, status, executable scenario, observable, receipt digest, reviewer, blocker. Preserve aliases/history. Requirement changes include rationale, impact, owner approval, old/new version, test/receipt impact, denominator, migration/compatibility, and rerun state. Changed text invalidates old evidence for that clause. Never lower thresholds or remove scenarios after seeing failures.

## 10. Release Checklist

- [ ] All mandatory requirements and clauses accounted for; no missing/skipped/blocked clause in engineering-completion claim.
- [ ] Current runtime contracts revalidated; dependencies match actual consumed revisions/configuration.
- [ ] Durable event, impact, repair, replay and revocation pass on every required store profile.
- [ ] Approval, retry, purge and external action boundaries pass adversarial tests.
- [ ] API/UI/MCP/export/worker all enforce current auth and lifecycle.
- [ ] AMRB scenarios pass; metrics independently recompute; security failures are never averaged away.
- [ ] Frozen performance profile passes; migration, backup, restore and runbooks exercised.
- [ ] Evidence is revision-bound/reproducible/reviewed; file/test references alone closed nothing.
- [ ] No community publication without owner, privacy/security, license and IP decisions.
- [ ] Final report separately states requirements, integration, and release/publication readiness.

## 11. Agent Handoff

Report completed requirement/acceptance IDs and receipt IDs; behavior and interfaces changed; exact commands/environment/exit codes; failed/skipped/blocked/unrun checks; migration/security/privacy/performance findings; changed files and preserved user changes; the three separate completion measures; and outstanding owner/legal/community decisions. Never claim 100% from a checklist. It requires verifier-confirmed passing evidence for every mandatory clause on the release candidate.

Implementation status: plan only; implementation has not been started or verified by this document.

<!-- tracker-integration -->

## 12. Tracker Procedure

This section tells an agent how to record CIP progress in the EOIP programme tracker. It adds no scope and changes no gate.

### 12.1 Files

| File (copy into the repository) | Purpose |
|---|---|
| `tools/tracker/EOIP-programme-tracker.html` | Interactive tracker for ASPEII, CIP, IP and Graph Neurons (open in a browser; state is kept in the browser and exported as JSON) |
| `tools/tracker/EOIP-programme-registry.json` | Every tracked item: id, programme, kind, parent, work package or phase, source `file:line`, normative text and its SHA-256 |
| `tools/tracker/programme_rules.js` | The single rules engine used by the tracker page and the verifier |
| `tools/tracker/verify_programme_ledger.mjs` | Command-line verifier; exit 0 only when the requested scope is complete with no problem |
| `docs/programme/programme-ledger.json` | The committed consolidated ledger (`eoip-programme-ledger-v1`), exported from the tracker or written by agents |

### 12.2 Identifiers

Tasks keep their plan ids; the shorthand `.2` in §4 means the full id `CIP-P<phase>.2`.

| Task | Phase: task |
| --- | --- |
| `CIP-P0.1` | Baseline and Decisions: inventory |
| `CIP-P0.2` | Baseline and Decisions: threat/privacy model |
| `CIP-P0.3` | Baseline and Decisions: persistence/outbox ADR |
| `CIP-P0.4` | Baseline and Decisions: API/UI/benchmark/evidence contracts |
| `CIP-P0.5` | Baseline and Decisions: baseline execution |
| `CIP-P1.1` | Contracts, Persistence, Migrations: schemas |
| `CIP-P1.2` | Contracts, Persistence, Migrations: repositories |
| `CIP-P1.3` | Contracts, Persistence, Migrations: tenant query contract |
| `CIP-P1.4` | Contracts, Persistence, Migrations: migrations/adapters |
| `CIP-P2.1` | Dependency Capture and Durable Change Intake: artifact versions |
| `CIP-P2.2` | Dependency Capture and Durable Change Intake: capture adapters |
| `CIP-P2.3` | Dependency Capture and Durable Change Intake: trusted change/outbox |
| `CIP-P2.4` | Dependency Capture and Durable Change Intake: replayable consumer |
| `CIP-P2.5` | Dependency Capture and Durable Change Intake: telemetry |
| `CIP-P3.1` | Impact and Freshness: reverse closure |
| `CIP-P3.2` | Impact and Freshness: time/policy |
| `CIP-P3.3` | Impact and Freshness: independent support |
| `CIP-P3.4` | Impact and Freshness: read-time gate |
| `CIP-P3.5` | Impact and Freshness: load profile |
| `CIP-P4.1` | Plans, Approval, Execution, Evaluation: rules |
| `CIP-P4.2` | Plans, Approval, Execution, Evaluation: immutable plan/digest |
| `CIP-P4.3` | Plans, Approval, Execution, Evaluation: approval |
| `CIP-P4.4` | Plans, Approval, Execution, Evaluation: executor |
| `CIP-P4.5` | Plans, Approval, Execution, Evaluation: pinned evaluation |
| `CIP-P4.6` | Plans, Approval, Execution, Evaluation: purge |
| `CIP-P5.1` | API, MCP, UI, Operations: routes/schemas |
| `CIP-P5.2` | API, MCP, UI, Operations: authorization |
| `CIP-P5.3` | API, MCP, UI, Operations: UI |
| `CIP-P5.4` | API, MCP, UI, Operations: MCP |
| `CIP-P5.5` | API, MCP, UI, Operations: runbooks |
| `CIP-P6.1` | AMRB and CIP Evidence Verifier: schemas/fixtures |
| `CIP-P6.2` | AMRB and CIP Evidence Verifier: validator |
| `CIP-P6.3` | AMRB and CIP Evidence Verifier: runner/CLI |
| `CIP-P6.4` | AMRB and CIP Evidence Verifier: metrics |
| `CIP-P6.5` | AMRB and CIP Evidence Verifier: evidence verifier |
| `CIP-P7.1` | Release-Candidate Verification: threat model |
| `CIP-P7.2` | Release-Candidate Verification: adversarial suite |
| `CIP-P7.3` | Release-Candidate Verification: chaos/restart |
| `CIP-P7.4` | Release-Candidate Verification: performance |
| `CIP-P7.5` | Release-Candidate Verification: evidence assembly |
| `CIP-P8.1` | Community and IP Decision Gate: private package |
| `CIP-P8.2` | Community and IP Decision Gate: privacy/license/security review |
| `CIP-P8.3` | Community and IP Decision Gate: owner/counsel decision |
| `CIP-P8.4` | Community and IP Decision Gate: release authorization |

Phase gates are `CIP-P0.GATE` … `CIP-P8.GATE`; each gate's exit text is the §4 **Exit** line. Gates close in order: a task, clause or gate of phase *n* cannot be VERIFIED before `CIP-P(n-1).GATE` is VERIFIED ("An unverified prerequisite blocks dependent closure"). `CIP-P7.GATE` also needs all 62 acceptance clauses, the five CIP-E2E scenarios and the 13 negative categories VERIFIED.

Acceptance clauses and the phases that list their requirement (the first listed phase is where the tracker groups the clause; Phase 7 re-verifies all of them):

| Requirement | Acceptance ids | Phases |
| --- | --- | --- |
| CIP-RQ-001 | AC-001.1, AC-001.2, AC-001.3, AC-001.4 | CIP-P0 |
| CIP-RQ-002 | AC-002.1, AC-002.2 | CIP-P1 |
| CIP-RQ-003 | AC-003.1, AC-003.2 | CIP-P1, CIP-P2 |
| CIP-RQ-004 | AC-004.1, AC-004.2 | CIP-P2 |
| CIP-RQ-005 | AC-005.1, AC-005.2 | CIP-P2 |
| CIP-RQ-006 | AC-006.1, AC-006.2 | CIP-P3 |
| CIP-RQ-007 | AC-007.1, AC-007.2 | CIP-P3 |
| CIP-RQ-008 | AC-008.1, AC-008.2 | CIP-P3 |
| CIP-RQ-009 | AC-009.1, AC-009.2 | CIP-P3, CIP-P5 |
| CIP-RQ-010 | AC-010.1, AC-010.2 | CIP-P4 |
| CIP-RQ-011 | AC-011.1, AC-011.2 | CIP-P4 |
| CIP-RQ-012 | AC-012.1, AC-012.2 | CIP-P4 |
| CIP-RQ-013 | AC-013.1, AC-013.2 | CIP-P4 |
| CIP-RQ-014 | AC-014.1, AC-014.2 | CIP-P4 |
| CIP-RQ-015 | AC-015.1, AC-015.2 | CIP-P4 |
| CIP-RQ-016 | AC-016.1, AC-016.2 | CIP-P3, CIP-P5 |
| CIP-RQ-017 | AC-017.1, AC-017.2 | CIP-P4 |
| CIP-RQ-018 | AC-018.1, AC-018.2 | CIP-P1, CIP-P5 |
| CIP-RQ-019 | AC-019.1, AC-019.2 | CIP-P5 |
| CIP-RQ-020 | AC-020.1, AC-020.2 | CIP-P5 |
| CIP-RQ-021 | AC-021.1, AC-021.2 | CIP-P3, CIP-P5 |
| CIP-RQ-022 | AC-022.1, AC-022.2 | CIP-P2, CIP-P5 |
| CIP-RQ-023 | AC-023.1, AC-023.2 | CIP-P2, CIP-P4, CIP-P5 |
| CIP-RQ-024 | AC-024.1, AC-024.2 | CIP-P6 |
| CIP-RQ-025 | AC-025.1, AC-025.2 | CIP-P6 |
| CIP-RQ-026 | AC-026.1, AC-026.2 | CIP-P6 |
| CIP-RQ-027 | AC-027.1, AC-027.2 | CIP-P8 |
| CIP-RQ-028 | AC-028.1, AC-028.2 | CIP-P0, CIP-P8 |
| CIP-RQ-029 | AC-029.1, AC-029.2 | CIP-P1, CIP-P8 |
| CIP-RQ-030 | AC-030.1, AC-030.2 | CIP-P0, CIP-P6, CIP-P8 |

Mandatory negative and recovery categories (§8):

| Item | Category |
| --- | --- |
| `CIP-NEG-01` | Invalid schema/version/canonicalization collision; cross-tenant edge, guessed ID, unauthorized principal, revoked job membership. |
| `CIP-NEG-02` | Duplicate, out-of-order, late, untrusted, unknown-kind event; event tampering and source mismatch. |
| `CIP-NEG-03` | Cycle, missing edge, corrupt digest, dangling revision, fan-out/depth cap, timeout, partial store. |
| `CIP-NEG-04` | Surviving evidence, no support, contradictory support, inaccessible evidence, incomplete capture. |
| `CIP-NEG-05` | Stale plan, changed policy/revision/digest, expired/wrong-tenant/replayed approval. |
| `CIP-NEG-06` | Concurrent workers, crash at each durable boundary, duplicate retry, cancellation, restart and dead-letter recovery. |
| `CIP-NEG-07` | Provider/evaluator/store/policy outage; partial metrics, insufficient sample, missing metric and post-result threshold tuning. |
| `CIP-NEG-08` | Access downgrade with API/browser/MCP/export/search/retrieval caches populated and before queue processing. |
| `CIP-NEG-09` | Purge under legal hold, unavailable replica, backup/export/cache residue and audit tombstone redaction. |
| `CIP-NEG-10` | External action requiring reconciliation; assert no outbound/reversal call. |
| `CIP-NEG-11` | Benchmark injection, schema/oracle alteration, duplicate case, nondeterministic seed, egress and production store selection. |
| `CIP-NEG-12` | Evidence manifest with source-only reference, marker but absent JUnit, skipped test, mismatched hash, stale benchmark or absent E2E receipt. |
| `CIP-NEG-13` | Keyboard-only UI, responsive overflow, partial/denied/stale/error/retry/recovery states. |

Release checklist (§10):

| Item | Check |
| --- | --- |
| `CIP-REL-01` | All mandatory requirements and clauses accounted for; no missing/skipped/blocked clause in engineering-completion claim. |
| `CIP-REL-02` | Current runtime contracts revalidated; dependencies match actual consumed revisions/configuration. |
| `CIP-REL-03` | Durable event, impact, repair, replay and revocation pass on every required store profile. |
| `CIP-REL-04` | Approval, retry, purge and external action boundaries pass adversarial tests. |
| `CIP-REL-05` | API/UI/MCP/export/worker all enforce current auth and lifecycle. |
| `CIP-REL-06` | AMRB scenarios pass; metrics independently recompute; security failures are never averaged away. |
| `CIP-REL-07` | Frozen performance profile passes; migration, backup, restore and runbooks exercised. |
| `CIP-REL-08` | Evidence is revision-bound/reproducible/reviewed; file/test references alone closed nothing. |
| `CIP-REL-09` | No community publication without owner, privacy/security, license and IP decisions. |
| `CIP-REL-10` | Final report separately states requirements, integration, and release/publication readiness. |

### 12.3 Per-Task Update Loop

1. Write the §5 task card. Set the task to `IN_PROGRESS` with the card as the work reference.
2. Branch and commit only after the owner records the authorisation decision XP-21 (§1.2 rule 8).
3. Run the narrowest behaviour test, then the package checks. Record `EVIDENCED` with the fields in §12.4; the CIP ledger value stays `NOT_RUN` until verified.
4. An independent reviewer reproduces the receipt and records `VERIFIED` (`PASS_WITH_EVIDENCE`).
5. When text, source or benchmark data changes, record `STALE`; §9 says changed text invalidates old evidence.
6. Export the ledger to `docs/programme/programme-ledger.json` and run:

```bash
# create an empty ledger once
node tools/tracker/verify_programme_ledger.mjs --init > docs/programme/programme-ledger.json
# check the ledger and recompute every evidence digest in the working tree
node tools/tracker/verify_programme_ledger.mjs --ledger docs/programme/programme-ledger.json --repo . --programme CIP
```

### 12.4 Evidence Required per Transition

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

The tracker fields map one-to-one to the `cip-evidence-1.0` manifest of §7: `commit` → `source_revision`, `evidence_sha256` → artifact digest, `junit_ids` → `test_case_ids`, `scenario_ref` → `scenario_ids`, `command` and `exit_code` → `commands`, `profile` → `environment.store_profile`, `reviewer` → `reviewer`.

Evidence digest: for a file, the SHA-256 of its bytes; for a directory, the SHA-256 of the UTF-8 text made of one line `<path relative to the directory>\t<sha256 of that file>\n` per file, sorted by path. `--repo` recomputes it and reports any mismatch as STALE.

### 12.5 Decisions Affecting CIP

- **XP-11 One change stream for leases, CTAR and revocation.** One transactional outbox publishes `kgf.graph.changed` (REQ-LSE-001). CIP adds the non-graph change kinds (access, policy, prompt, model, tool, evaluator) to the same outbox with the CIP-RQ-005 metadata. Lease revocation, CTAR intake and ASPEII admission invalidation are consumers of that one stream. Synchronous read denial on revocation (CIP-RQ-009) does not wait for any consumer.
- **XP-15 Evidence locations and one consolidated ledger.** Keep every native location. The consolidated ledger `docs/programme/programme-ledger.json` (schema eoip-programme-ledger-v1) records, per item, the native path and its SHA-256 digest. verify_programme_ledger.py recomputes the digests.
- **XP-21 Branching and commits: CIP forbids without authorisation, IP prescribes.** Before CIP code work starts, the owner records whether CIP work may branch and commit (and the naming scheme, e.g. `cip/P<n>-<name>`). Until then CIP work stays in Phase 0 (documentation and inventory).
- **XP-25 Retention settings.** Pre-resolved by aspeii-reqirements.md §2.1: reuse the IP key; production deployments acknowledge effective retention explicitly; CIP purge and legal hold apply to warrants as to any artifact.
