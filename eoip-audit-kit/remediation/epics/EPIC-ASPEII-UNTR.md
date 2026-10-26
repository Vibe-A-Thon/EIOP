# EPIC-ASPEII-UNTR: EOIP-engg-doc-pkg/aspeii-reqirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 46 tasks, ~310.0 h, priorities {'P0': 23, 'P1': 13, 'P2': 10}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-ASPEII-E2E-08 [P0] ASPEII-E2E-08: Source correction, permission revocation and surviving support

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:742-742` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-E2E-08; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ASPEII-E2E-08 | Source correction, permission revocation and surviving support | Immediate access/admission denial where required; correct CTAR impact and preserved authorized support
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-E2E-08' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-E2E-08') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-E2E-08

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ASPEII-E2E-08 | Source correction, permission revocation and surviving support | Immediate access/admission denial where required; correct CTAR impact and preserved authorized support»
- [ ] Source correction, permission revocation and surviving support
- [ ] Immediate access/admission denial where required; correct CTAR impact and preserved authorized support
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-002 [P0] ASPEII-RQ-002: Versioned Shared Contracts

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:201-213` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-002: Versioned Shared Contracts

Priority P0. Dependencies: 001.

1. Implement all records and enums in section 3 with strict validation and machine-readable schemas.
2. Generate frontend types from the public contract and validate Python/TypeScript serialization equivalence on canonical vectors.
3. Reject missing identity, malformed references, unknown security fields, unsupported schema versions, invalid numerics, and over-limit input before persistence.
4. Implement explicit legacy agent/tool/proposal adapters; preserve original provenance and flag unmapped assurance as UNKNOWN.
5. Give errors stable codes, sanitized details, a correlation ID, and machine-readable retryability without revealing hidden resource existence.
6. Add schema upgrade/downstream compatibility fixtures and documented removal rules; no silent coercion of ambiguous legacy values.

Acceptance: a v2 request adapts without fabricating approval; a client-supplied tenant or risk downgrade cannot override trusted context.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-002

**Acceptance criteria**
- [ ] a v2 request adapts without fabricating approval; a client-supplied tenant or risk downgrade cannot override trusted context
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-003 [P0] ASPEII-RQ-003: Durable Authority and Transactions

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:214-226` (heading) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-003: Durable Authority and Transactions

Priority P0. Dependencies: 002.

1. Persist intent/task/action/grant/approval/receipt/evaluation/version records in a transactional repository; implement SQLite local and PostgreSQL multi-worker adapters.
2. Atomically update authoritative transitions, budget reservations, and outbox events; use compare-and-swap revisions and unique logical-effect keys.
3. Implement durable leases with fencing and expiry; workers must present the current fence when dispatching or publishing.
4. Project records to the graph asynchronously with idempotent event IDs, visible projection watermark, and rebuild support.
5. Preserve committed data across restart and recover interrupted transitions without manufacturing terminal success.
6. Supply migrations, backup/restore, corruption detection, and rollback compatibility; qualify each storage profile separately.

Acceptance: two workers race on one action and only one acquires dispatch authority; process termination after commit/before projection loses no decision and projection resumes.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-003

**Acceptance criteria**
- [ ] two workers race on one action and only one acquires dispatch authority; process termination after commit/before projection loses no decision and projection resumes
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-004 [P0] ASPEII-RQ-004: Identity, Tenant, and Permission Boundaries

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:227-239` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 7.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-004: Identity, Tenant, and Permission Boundaries

Priority P0. Dependencies: 002, 003.

1. Resolve principal, tenant, workspace, roles, and service identity from authenticated context for every operation and event consumer.
2. Enforce object/action-level authorization on lists, details, approval, execution, graph paths, evidence downloads, exports, MCP, and historical views.
3. Recheck current permissions at read, admission, dispatch, and evidence retrieval; cached grants cannot survive revocation.
4. Separate proposer, approver, verifier, publisher, and operator permissions; enforce no self-approval for R3 and configured R2 policies.
5. Minimize delegated context and credential exposure; agents receive scoped handles rather than reusable secrets.
6. Return indistinguishable unauthorized/missing object responses where appropriate; no tenant leakage via counts, cursor contents, events, errors, or caches.

Acceptance: two tenants with matching display names cannot see or approve each other's records; forged body `actor_id` is rejected or ignored in favor of authenticated identity.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-004

**Acceptance criteria**
- [ ] two tenants with matching display names cannot see or approve each other's records; forged body actorid is rejected or ignored in favor of authenticated identity
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-ASPEII-RQ-005 [P0] ASPEII-RQ-005: Intent Capture and Revision

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:240-252` (heading) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-005: Intent Capture and Revision

Priority P1. Dependencies: 002, 004.

1. Provide GUI/API creation of structured intent with all fields in section 3 and links to existing BusinessObjective/BusinessCapability objects.
2. Record ambiguous or absent required values as explicit unresolved fields; allow saving drafts but prevent activation until resolved.
3. Support non-goals, effect boundaries, per-scope data constraints, measurable acceptance predicates, aggregate budgets, and deadline.
4. Let an LLM draft a candidate interpretation; require deterministic validation and authorized acceptance of consequential scope.
5. Version edits immutably and show the changed goal/constraints; invalidate dependent actions when relevant intent fields change.
6. Distinguish user outcome satisfaction from execution status; report partial fulfillment and unavailable measurements visibly.

Acceptance: 'investigate incident without changing systems' allows evidence reads and blocks remediation writes; removing the only measurable predicate prevents activation.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-005

**Acceptance criteria**
- [ ] 'investigate incident without changing systems' allows evidence reads and blocks remediation writes; removing the only measurable predicate prevents activation
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-006 [P0] ASPEII-RQ-006: Intent Compilation and Outcome Verification

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:253-265` (heading) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-006: Intent Compilation and Outcome Verification

Priority P1. Dependencies: 005, 013, 019.

1. Compile accepted intents into typed task contracts using an allowlisted planning interface, preserving all parent constraints.
2. Validate the task graph for missing dependencies, cycles, scope expansion, incompatible outputs, and aggregate budget overflow.
3. Allocate every mandatory acceptance predicate to an independent verifier and concrete observation source.
4. For deterministic predicates, execute the registered verifier; for subjective acceptance, obtain an authorized human decision under an explicit rubric.
5. Prevent the planner from editing goal thresholds, expected results, or evaluator implementations to make its own output pass.
6. Compute intent outcome from predicate results and required tasks; unknown or skipped predicates cannot yield SUCCEEDED.

Acceptance: all children returning SUCCEEDED while a required runtime postcondition fails results in FAILED/PARTIAL intent, with the failed predicate visible.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-006

**Acceptance criteria**
- [ ] Priority P1. Dependencies: 005, 013, 019
- [ ] Compile accepted intents into typed task contracts using an allowlisted planning interface, preserving all parent constraints
- [ ] Validate the task graph for missing dependencies, cycles, scope expansion, incompatible outputs, and aggregate budget overflow
- [ ] Allocate every mandatory acceptance predicate to an independent verifier and concrete observation source
- [ ] For deterministic predicates, execute the registered verifier; for subjective acceptance, obtain an authorized human decision under an explicit rubric
- [ ] Prevent the planner from editing goal thresholds, expected results, or evaluator implementations to make its own output pass
- [ ] Compute intent outcome from predicate results and required tasks; unknown or skipped predicates cannot yield SUCCEEDED
- [ ] all children returning SUCCEEDED while a required runtime postcondition fails results in FAILED/PARTIAL intent, with the failed predicate visible
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-008 [P0] ASPEII-RQ-008: Qualified Capabilities and Assignment

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:279-291` (heading) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-008; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-008: Qualified Capabilities and Assignment

Priority P1. Dependencies: 007, 035.

1. Separate advertised capabilities from measured qualification by task type, tool/model version, deployment, and data class.
2. Select only currently authorized and qualified candidates meeting hard constraints; missing candidates yield BLOCKED.
3. Use a deterministic documented ranking of eligible candidates based on fit, measured quality, remaining capacity, and configured cost/latency priorities.
4. Record selection factors and rejected alternatives without claiming a heuristic rank is a calibrated success probability.
5. Expire capability evidence after relevant model/tool/policy changes; require requalification before consequential work resumes.
6. Keep external identities isolated by provider and tenant; no reputation pooling across tenants without explicit governed aggregate policy.

Acceptance: a stale high-scoring candidate loses eligibility to a freshly qualified candidate; an advertised unsupported tool never becomes executable by ranking alone.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-008

**Acceptance criteria**
- [ ] a stale high-scoring candidate loses eligibility to a freshly qualified candidate; an advertised unsupported tool never becomes executable by ranking alone
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-009 [P0] ASPEII-RQ-009: Attenuated Grants, Budgets, and Revocation

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:292-304` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-009; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 7.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-009: Attenuated Grants, Budgets, and Revocation

Priority P0. Dependencies: 003, 004, 007.

1. Issue scoped opaque grants whose effective permissions and resource ceilings are the intersection of parent, actor, tool, and current policy.
2. Bind grant to audience, task, tenant, expiry, parent, and revocation epoch; verify all ancestors before consequential dispatch.
3. Reserve aggregate tokens, tool calls, wall time, and configured money atomically before work; settle actual use and conservatively handle unknown cost.
4. Enforce monotonic attenuation across child depth and prohibit alias, retry, or fan-out paths from multiplying authority or budget.
5. Implement root/branch revocation and operator kill switches checked at dispatch independently of asynchronous event delivery.
6. Record denied, expired, exhausted, and revoked grants with sanitized receipts; never log raw bearer secrets.

Acceptance: simultaneous children cannot exceed a root's final available budget; revoking the parent prevents an already queued child action.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-009

**Acceptance criteria**
- [ ] simultaneous children cannot exceed a root's final available budget; revoking the parent prevents an already queued child action
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-ASPEII-RQ-012 [P0] ASPEII-RQ-012: Typed Tool Results and Registry Reconciliation

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:331-343` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-012; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 7.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-012: Typed Tool Results and Registry Reconciliation

Priority P0. Dependencies: 002, 004.

1. Register production class, effect, authoritative risk/obligations, transport, freshness, and output schema for every reachable tool.
2. Reconcile the agent tool registry and tool-contract engine through one qualification record; duplicated names cannot bypass policy.
3. Produce structured result envelopes containing content provenance, source revisions, claim refs, actual execution status, and supported assurance mode.
4. Preserve generator origin when a model output is wrapped in HTTP, MCP, a database row, an expert tool, or another agent.
5. For mixed tools, label each output field/claim's origin and reject untyped security-relevant subresults.
6. Treat schema validity as format verification only; qualification requires real execution and independently checked outputs.

Acceptance: an 'expert' MCP tool returning model text remains GENERATOR/HYPOTHESIS even when transport authentication and JSON Schema validation pass.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-012

**Acceptance criteria**
- [ ] an 'expert' MCP tool returning model text remains GENERATOR/HYPOTHESIS even when transport authentication and JSON Schema validation pass
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-ASPEII-RQ-013 [P0] ASPEII-RQ-013: Claim and Evidence Registry

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:344-356` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-013; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 7.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-013: Claim and Evidence Registry

Priority P0. Dependencies: 002, 003, 004, 012.

1. Persist scoped claim/evidence records with separate epistemic kind, truth status, lifecycle, acquisition provenance, and valid-time.
2. Resolve every evidence reference to accessible immutable content or a recorded unavailable/retracted state; arbitrary strings are not verified evidence.
3. Support field/row/document-span/page/timecode locators with original media digest and extraction/version history.
4. Track independent origin groups and deduplicate mirrored, copied, cached, or model-rephrased evidence.
5. Preserve contradictions and alternate interpretations instead of overwriting one claim with a higher confidence value.
6. Enforce retention/deletion/classification on raw evidence and derivatives; store only authorized redacted references in receipts.

Acceptance: two URLs mirroring one source count as one origin; an OCR transcription retains the image/page reference and extraction uncertainty.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-013

**Acceptance criteria**
- [ ] two URLs mirroring one source count as one origin; an OCR transcription retains the image/page reference and extraction uncertainty
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-ASPEII-RQ-014 [P0] ASPEII-RQ-014: Warrant Checking and Anti-Laundering

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:357-369` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-014; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-014: Warrant Checking and Anti-Laundering

Priority P0. Dependencies: 013.

1. Evaluate support sets under explicit rules and boundaries; require a grounded acyclic support path for claims used in consequential obligations.
2. Reject self-support and cycles whose only leaves are generated claims, including cycles distributed across agents or caches.
3. Preserve provenance and support limits through aggregation, summaries, embeddings, RAG, memory, and graph projection.
4. Allow independent observations to support a hypothesis through a new verification event; do not rewrite its original production class.
5. Label LLM judges, model confidence, citation counts, and signatures as their actual evidence types; none alone establishes factual support.
6. Replace confidence-only and string-only trust promotion; legacy `CERTIFIED` labels require an explicit scoped verification record to be used as certified evidence.

Acceptance: a fabricated statement routed through generator -> database -> search -> critic cannot become supported merely through this round trip; a genuine independent source can change its support result.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-014' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-014') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-014

**Acceptance criteria**
- [ ] a fabricated statement routed through generator -> database -> search -> critic cannot become supported merely through this round trip; a genuine independent source can change its support result
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-015 [P0] ASPEII-RQ-015: Temporal Validity and Read-Time Decisions

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:370-382` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-015; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 7.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-015: Temporal Validity and Read-Time Decisions

Priority P0. Dependencies: 004, 013, 014.

1. Enforce valid-time, source revision, observation TTL, policy revision, and CTAR lifecycle whenever claims are retrieved or used in an action.
2. Preserve historical knowledge state while applying current access permissions to historical reads.
3. Mark missing dependency history UNKNOWN and fail closed for consequential use; expose incomplete evidence honestly in read-only exploration.
4. Recompute support from surviving independent support sets after a source correction/retraction without leaking revoked content.
5. Invalidate affected caches by source/policy/ontology/model revision and provide bounded rebuild status.
6. Keep lifecycle transitions attributable and reversible only through authorized new evidence/repair, not a confidence increment.

Acceptance: revoke a source before the repair worker runs; dependent action admission and unauthorized retrieval immediately fail, while independently supported authorized content remains available.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-015' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-015') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-015

**Acceptance criteria**
- [ ] revoke a source before the repair worker runs; dependent action admission and unauthorized retrieval immediately fail, while independently supported authorized content remains available
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-ASPEII-RQ-023 [P0] ASPEII-RQ-023: Real MCP and Runtime Adapters

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:474-486` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-023; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 7.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-023: Real MCP and Runtime Adapters

Priority P0. Dependencies: 004, 012, 020, 021, 022.

1. Implement actual MCP initialization, capability negotiation, tool discovery, invocation, error handling, and disconnect behavior for supported transports.
2. Qualify stdio and HTTP transports separately; use explicit process/server allowlists, authenticated sessions, audience checks, network/egress policy, and bounded responses.
3. Remove or clearly isolate synthetic successful external calls from production paths; unavailable servers report unavailable, never connected/success.
4. Pin discovered tool schemas and implementation identity; changes invalidate dependent grants, certificates, and qualification as specified by policy.
5. Classify adapter enforcement mode and demonstrate it; imported after-the-fact logs cannot become pre-execution approvals.
6. Keep caller permissions and result provenance across EOIP MCP server and external MCP client, including malicious tool descriptions and nested calls.

Acceptance: an unreachable `.invalid` server fails connection/invocation; an actual local MCP server's independently observed call log matches the receipt; changed schema prevents reuse of old approval.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-023' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-023') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-023

**Acceptance criteria**
- [ ] an unreachable .invalid server fails connection/invocation; an actual local MCP server's independently observed call log matches the receipt; changed schema prevents reuse of old approval
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-ASPEII-RQ-025 [P0] ASPEII-RQ-025: Evidence-Grounded Semantic Builder

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:500-512` (heading) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-025; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-025: Evidence-Grounded Semantic Builder

Priority P1. Dependencies: 019, 024.

1. Generate initial semantic proposals from authorized source metadata and approved workload examples using a pluggable builder.
2. Use read-only bounded probes against actual source revisions; record query, schema, sample limitations, and result digests.
3. Treat labels, mappings, units, join paths, and business constraints as separate claims with supporting evidence.
4. Keep unsupported proposals quarantined; require domain-owner acceptance for semantic business rules that data profiling cannot establish.
5. Validate candidates through existing ontology/schema tooling and action governance before initial publication, including version zero.
6. Support deterministic/manual authoring without a model and disclose provider/model/usage for AI-assisted proposals.

Acceptance: plausible but nonexistent database columns fail grounding; a statistically common pattern does not automatically become a mandatory business constraint.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-025' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-025') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-025

**Acceptance criteria**
- [ ] plausible but nonexistent database columns fail grounding; a statistically common pattern does not automatically become a mandatory business constraint
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-026 [P0] ASPEII-RQ-026: Trajectory Capture and Attribution

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:513-525` (heading) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-026; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-026: Trajectory Capture and Attribution

Priority P1. Dependencies: 007, 013, 021, 024.

1. Capture authorized tool-level trajectories with task, semantic version, model/tool configuration, result claims, observations, failures, and outcome predicates.
2. Redact secrets and sensitive payloads; exclude private chain-of-thought while retaining reproducible inputs permitted by policy.
3. Attribute recurring failures to content, schema, tool exposure, source quality, permissions, model behavior, or infrastructure as explicit hypotheses.
4. Separate observations from inferred causes and support human correction of attribution through a new record.
5. Freeze selected trajectories before an evolution run; track origin groups and exclude test/validation feedback from construction input.
6. Support incremental ingestion, duplicate detection, missing trajectory disclosure, and CTAR invalidation on source correction.

Acceptance: a permission-denied source access is not automatically repaired by widening ontology/tool access; a repeated trace is counted once.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-026' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-026') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-026

**Acceptance criteria**
- [ ] a permission-denied source access is not automatically repaired by widening ontology/tool access; a repeated trace is counted once
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-029 [P0] ASPEII-RQ-029: Atomic Publication and Rollback

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:552-564` (heading) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-029; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-029: Atomic Publication and Rollback

Priority P0. Dependencies: 020, 021, 028, 030.

1. Publish only an accepted, approved, fully validated candidate whose parent still matches the active version.
2. Atomically commit publication reference, lineage, migration state, and outbox event; never overwrite a published snapshot.
3. Support progressive read-only exposure by configured workspace/model profile with observable error and rollback thresholds.
4. Revalidate affected mappings, queries, agent contracts, action obligations, and cached artifacts before allowing consequential use.
5. Roll back through a new governed version-selection event with compatibility checks; do not erase prior versions or imply external effects were undone.
6. Recover partial publication after restart using persisted intent and transactional state; prevent two candidates from both winning the same parent revision.

Acceptance: two accepted candidates race; one publishes and one receives CONFLICT; rollback restores the correct semantic view and triggers derivative invalidation.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-029' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-029') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-029

**Acceptance criteria**
- [ ] two accepted candidates race; one publishes and one receives CONFLICT; rollback restores the correct semantic view and triggers derivative invalidation
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-030 [P0] ASPEII-RQ-030: CTAR and Neural-Output Integration

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:565-577` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-030; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 7.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-030: CTAR and Neural-Output Integration

Priority P0. Dependencies: 003, 013, 015.

1. Add explicit CTAR artifact mappings for intent/task/grant/tool contract/claim/certificate/receipt/semantic candidate/evaluation/version records.
2. Capture dependency revisions for prompts, models, sources, policies, ontologies, evaluators, and tool schemas without copying private payloads.
3. On a relevant change, invalidate action admission immediately and schedule bounded downstream repair using the existing CTAR direction and lifecycle.
4. Treat neural predictions and similarity scores as hypotheses with model provenance; existing verified graph facts remain separately represented.
5. Preserve independently supported authorized alternatives and distinguish corrected information from revoked authorization.
6. Integrate with AMRB scenarios and explicitly reconcile external effects; no automatic historical action reversal.

Acceptance: a model update invalidates qualification for its predictions without erasing source observations; source revocation blocks a pending certificate before background repair completes.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-030' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-030') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-030

**Acceptance criteria**
- [ ] a model update invalidates qualification for its predictions without erasing source observations; source revocation blocks a pending certificate before background repair completes
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-ASPEII-RQ-031 [P0] ASPEII-RQ-031: API, Events, CLI, and Public Contracts

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:578-590` (heading) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-031; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-031: API, Events, CLI, and Public Contracts

Priority P1. Dependencies: 002, 004, 006, 010, 022, 029.

1. Implement section 5 endpoints through the active app factory and publish validated OpenAPI schemas with typed request/response examples.
2. Apply authorization, cursor pagination, idempotency, expected revisions, rate limits, and sanitized error contracts consistently.
3. Expose durable progress/audit events with resumable cursor, sequence, tenant filtering, replay bounds, and explicit gap detection.
4. Provide CLI operations for inspection, verification, evaluation, and authorized workflow submission; CLI uses the same services and never bypasses admission.
5. Maintain backward-compatible read adapters and explicit deprecation errors for unsafe legacy mutation routes.
6. Run contract tests against real HTTP/MCP transport and packaged CLI, including reverse-proxy deployment and offline evidence verification.

Acceptance: duplicate idempotent submission returns the original logical operation; same key with different payload returns 409; API and CLI cannot disagree on approval validity.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-031' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-031') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-031

**Acceptance criteria**
- [ ] duplicate idempotent submission returns the original logical operation; same key with different payload returns 409; API and CLI cannot disagree on approval validity
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-032 [P0] ASPEII-RQ-032: Integrated Operational GUI

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:591-603` (heading) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-032; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-032: Integrated Operational GUI

Priority P1. Dependencies: 011, 024, 031.

1. Extend the existing frontend with Intent workspace, Run detail, Evidence inspector, Action review, Evolution comparison, and Assurance views described in section 6.
2. Use generated types, authenticated tenant-aware query keys, current API field names, and explicit loading/empty/error/denied/stale/conflict states.
3. Display consequences, destination/account, exact revision, evidence limits, enforcement mode, and actual outcome before presenting approval or success.
4. Use accessible native controls and existing lucide icons, visible focus, keyboard operation, reduced-motion support, and responsive unclipped layouts.
5. Preserve navigation and query state, cancel/refresh safely, prevent duplicate submission, and show mutation failures instead of swallowing errors.
6. Demonstrate full user journeys in a real browser against the real API, including two tenants, revocation, stale review, worker restart, and mobile layout.

Acceptance: approve/reject uses `proposal_id` or the explicitly versioned new DTO ID; a failed mutation remains visibly failed; no mocked network response can satisfy GUI integration qualification.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-032' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-032') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-032

**Acceptance criteria**
- [ ] approve/reject uses proposalid or the explicitly versioned new DTO ID; a failed mutation remains visibly failed; no mocked network response can satisfy GUI integration qualification
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-033 [P0] ASPEII-RQ-033: Operations, Deployment, and Recovery

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:604-616` (heading) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-033; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-033: Operations, Deployment, and Recovery

Priority P1. Dependencies: 003, 009, 022, 031.

1. Package local/customer-installed and SaaS profiles with explicit storage, key, model, egress, backup, migration, and adapter configuration.
2. Expose metrics for queue age, leases, denied actions, unknown outcomes, support invalidation, evaluator failures, and projection lag without high-cardinality secrets.
3. Provide health/readiness checks that distinguish connected dependencies from synthetic/demo state; unavailable required authority storage fails readiness.
4. Document and exercise key rotation, source revocation, checker outage, storage outage, unknown external outcome, failed publish, and restore runbooks.
5. Measure section 7 performance targets on declared hardware; quotas and admission must remain correct under load/backpressure.
6. Restore backup into an isolated environment and verify authority/evidence consistency before reopening execution; restored consumed approvals must not become reusable.

Acceptance: loss of verifier/storage blocks consequential dispatch; restoration preserves consumed action identity and denies duplicate execution.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-033' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-033') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-033

**Acceptance criteria**
- [ ] loss of verifier/storage blocks consequential dispatch; restoration preserves consumed action identity and denies duplicate execution
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-034 [P0] ASPEII-RQ-034: Adversarial and Supply-Chain Boundaries

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:617-629` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-034; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 7.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-034: Adversarial and Supply-Chain Boundaries

Priority P0. Dependencies: 004, 012, 019, 023, 027.

1. Treat retrieved text, documents, media transcripts, tool descriptions, and external agent messages as untrusted data rather than policy instructions.
2. Defend adapters against SSRF, token forwarding, confused-deputy access, schema substitution, oversize payloads, subprocess injection, and unauthorized egress.
3. Verify pinned third-party artifacts, licenses, transitive dependencies, hashes, and model/data usage terms before incorporation; preserve EOIP commercial ownership boundaries.
4. Ensure builders/evaluators cannot modify each other's inputs, hidden labels, execution gateway, or signing keys through shared volumes or credentials.
5. Exercise cross-tenant, replay, race, revocation, stale-state, poisoned-knowledge, colluding-agent, and fake-receipt attacks at real boundaries.
6. Document residual threats and control scope; neither signing nor a finite red-team suite supports a universal safety claim.

Acceptance: a source instructing the agent to disable approvals has no effect on admission; a malicious MCP redirect cannot reuse a token for a different audience.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-034' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-034') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-034

**Acceptance criteria**
- [ ] a source instructing the agent to disable approvals has no effect on admission; a malicious MCP redirect cannot reuse a token for a different audience
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-ASPEII-RQ-035 [P0] ASPEII-RQ-035: Independent Behavioral Qualification

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:630-642` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-035; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-035: Independent Behavioral Qualification

Priority P0. Dependencies: 001, 002.

1. Build deterministic fixtures and independent expected results for section 8 scenarios, with source provenance and immutable fixture digests.
2. Separate unit, API, worker, storage, real-adapter, browser, adversarial, recovery, and performance outcomes; each applicable layer is required.
3. Verify absence of forbidden effects through independent adapter/server/store observations, not the action service's self-reported DENIED result alone.
4. Include deliberate negative controls that would pass a stub, such as fake approval IDs, fabricated external success, constant evaluators, and confidence-only certification; the harness must catch them.
5. Capture raw outputs, seeds, per-case results, source/build/config/dependency hashes, timestamps, integration modes, and known limitations.
6. Repeat only as justified by nondeterminism or changed artifacts; mark mismatched/stale/skipped/flaky/inconclusive evidence non-PASS and retain earlier failures.

Acceptance: replacing a real adapter with a success-returning stub makes qualification fail; changing a covered implementation file invalidates its previous receipt.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-035' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-035') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-035

**Acceptance criteria**
- [ ] replacing a real adapter with a success-returning stub makes qualification fail; changing a covered implementation file invalidates its previous receipt
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-036 [P0] ASPEII-RQ-036: Release Evidence and Honest Completion

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:643-655` (heading) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-036; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-036: Release Evidence and Honest Completion

Priority P0. Dependencies: 001, 031, 032, 033, 034, 035.

1. Implement a scope-aware evidence verifier covering all 216 numbered clauses plus allocated shared contracts and scenario obligations.
2. Require the actual deployable build, supported profiles, migrations, API/UI integration, operational restore, and real adapter evidence for release qualification.
3. Publish exact completion numerator/denominator, per-profile matrix, remaining gaps, and verifier version; do not average security failures away.
4. Fail release verification on missing artifacts, mismatched hashes, unresolved mandatory failures, orphaned clauses, unqualified adapters, or stale receipts.
5. Update operator/developer/user documentation to actual measured behavior and retain source provenance/licensing notices for imported artifacts.
6. Provide a fresh-agent handoff containing exact next steps for every incomplete clause; only declare 100% for this frozen scope when every required check is VERIFIED.

Acceptance: 215/216 verified clauses is not 100%; a perfectly formatted plan or a directory full of tests produces no implementation completion credit without qualifying observations.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-036' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-036') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-036

**Acceptance criteria**
- [ ] 215/216 verified clauses is not 100%; a perfectly formatted plan or a directory full of tests produces no implementation completion credit without qualifying observations
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-E2E-04 [P1] ASPEII-E2E-04: Reversible graph correction with genuine approval

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:738-738` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-E2E-04; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ASPEII-E2E-04 | Reversible graph correction with genuine approval | Exact action approved, single mutation observed, independent postcondition and signed receipt
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-E2E-04' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-E2E-04') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-E2E-04

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ASPEII-E2E-04 | Reversible graph correction with genuine approval | Exact action approved, single mutation observed, independent postcondition and signed receipt»
- [ ] Reversible graph correction with genuine approval
- [ ] Exact action approved, single mutation observed, independent postcondition and signed receipt
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-E2E-05 [P1] ASPEII-E2E-05: Fake/stale/cross-tenant approval and changed arguments

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:739-739` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-E2E-05; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ASPEII-E2E-05 | Fake/stale/cross-tenant approval and changed arguments | Denied with zero independent handler calls and no data mutation
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-E2E-05' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-E2E-05') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-E2E-05

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ASPEII-E2E-05 | Fake/stale/cross-tenant approval and changed arguments | Denied with zero independent handler calls and no data mutation»
- [ ] Fake/stale/cross-tenant approval and changed arguments
- [ ] Denied with zero independent handler calls and no data mutation
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-E2E-11 [P1] ASPEII-E2E-11: Qualified candidate publishes, then governed rollback

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:745-745` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-E2E-11; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ASPEII-E2E-11 | Qualified candidate publishes, then governed rollback | Atomic version change, correct invalidation, durable lineage and restored semantics
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-E2E-11' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-E2E-11') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-E2E-11

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ASPEII-E2E-11 | Qualified candidate publishes, then governed rollback | Atomic version change, correct invalidation, durable lineage and restored semantics»
- [ ] Qualified candidate publishes, then governed rollback
- [ ] Atomic version change, correct invalidation, durable lineage and restored semantics
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-E2E-14 [P1] ASPEII-E2E-14: Receipt tamper, key rotation and restore

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:748-748` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-E2E-14; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ASPEII-E2E-14 | Receipt tamper, key rotation and restore | Independent verification catches tampering; valid historical keys handled by trust policy; consumed approval not replayable
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-E2E-14' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-E2E-14') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-E2E-14

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ASPEII-E2E-14 | Receipt tamper, key rotation and restore | Independent verification catches tampering; valid historical keys handled by trust policy; consumed approval not replayable»
- [ ] Receipt tamper, key rotation and restore
- [ ] Independent verification catches tampering; valid historical keys handled by trust policy; consumed approval not replayable
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-E2E-15 [P1] ASPEII-E2E-15: No-egress installation with models disabled/local model

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:749-749` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-E2E-15; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ASPEII-E2E-15 | No-egress installation with models disabled/local model | Deterministic core usable; unavailable provider visible; no undeclared network traffic
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-E2E-15' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-E2E-15') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-E2E-15

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ASPEII-E2E-15 | No-egress installation with models disabled/local model | Deterministic core usable; unavailable provider visible; no undeclared network traffic»
- [ ] No-egress installation with models disabled/local model
- [ ] Deterministic core usable; unavailable provider visible; no undeclared network traffic
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-007 [P1] ASPEII-RQ-007: Delegated Task Contracts

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:266-278` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-007: Delegated Task Contracts

Priority P1. Dependencies: 002, 004, 005.

1. Create immutable task assignments with accountable owner, scoped inputs, output schema, verifier, grants, and resource reservation.
2. Support human-to-agent, agent-to-agent, and agent-to-human task edges with explicit assignment acceptance/decline.
3. Enforce acyclic dependencies and bounded parent depth; root accounting includes grandchildren and retries.
4. Preserve parent intent and grant lineage through every handoff; omitted constraints are a validation failure.
5. Support blocked, abstained, declined, timed-out, and cancelled outcomes without presenting them as successful delegation.
6. Record observable handoff context and result artifacts, excluding private chain-of-thought and unnecessary source payload.

Acceptance: a child cannot outsource a disallowed export to a grandchild; a human can decline without the workflow fabricating a replacement approval.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-007

**Acceptance criteria**
- [ ] a child cannot outsource a disallowed export to a grandchild; a human can decline without the workflow fabricating a replacement approval
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-010 [P1] ASPEII-RQ-010: Recoverable Scheduling and Reassignment

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:305-317` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-010; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-010: Recoverable Scheduling and Reassignment

Priority P1. Dependencies: 003, 007, 009, 021.

1. Schedule ready tasks with concurrency limits, deadlines, heartbeat leases, and fairness across tenants.
2. Reassign only after fencing the prior worker and reconciling any possibly dispatched effect.
3. Classify retryable failures using adapter contracts; non-idempotent or unknown-outcome effects enter reconciliation.
4. Permit bounded re-planning after a failure through a new plan revision preserving frozen root acceptance and remaining budget.
5. Support cancellation requests and progress events; cancellation acknowledges actual cessation or reports outstanding reconciliation.
6. Prevent oscillating reassignment with attempt limits and recorded backoff; exhausted tasks end visibly incomplete.

Acceptance: pause worker A, expire its lease, dispatch worker B, resume A; A cannot execute or publish with its old fence.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-010

**Acceptance criteria**
- [ ] pause worker A, expire its lease, dispatch worker B, resume A; A cannot execute or publish with its old fence
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-011 [P1] ASPEII-RQ-011: Human Control and Review Ergonomics

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:318-330` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-011; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-011: Human Control and Review Ergonomics

Priority P1. Dependencies: 004, 007, 020.

1. Provide a review queue with ownership, urgency, exact action, affected objects, uncertainty, and independent evidence.
2. Present explicit approve/reject/request-change/defer commands where valid; no preselected or timed-out approval.
3. Route unanswered reviews to configured escalation or expiry; never infer consent from silence.
4. Show which system can actually stop the effect and distinguish observed external actions from pending controllable actions.
5. Make reviewer workload, aged tasks, and pending irreversible operations visible without exposing private cross-tenant activity.
6. Preserve the reviewer's rationale and exact reviewed revision, with accessible keyboard navigation and audit export.

Acceptance: altering a destination after a reviewer opened the screen disables acceptance of the old digest and displays a conflict; expired review cannot dispatch.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-011

**Acceptance criteria**
- [ ] altering a destination after a reviewer opened the screen disables acceptance of the old digest and displays a conflict; expired review cannot dispatch
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-016 [P1] ASPEII-RQ-016: Epistemic Artifact and Requirement Lifecycle

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:383-395` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-016; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-016: Epistemic Artifact and Requirement Lifecycle

Priority P1. Dependencies: 013, 014.

1. Represent requirements, architectural decisions, domain hypotheses, and operating assumptions as distinct artifact kinds with explicit boundaries.
2. Link atomic propositions to dependency and falsification records, preserving original wording and revision.
3. Support draft, accepted-for-scope, challenged, revised, and superseded decisions without equating acceptance with empirical verification.
4. Show exact unsupported dependencies and conflicts; heuristic confidence is descriptive and cannot close a requirement.
5. Import existing requirement IDs through a structured parser and preserve overlapping source documents without destructive renumbering.
6. Record scope reductions and waived claims separately from passed acceptance; maintain the original completion denominator.

Acceptance: linking a test filename does not mark its claim verified; superseding a failed requirement produces a visible scope decision rather than erasing failure history.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-016' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-016') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-016

**Acceptance criteria**
- [ ] linking a test filename does not mark its claim verified; superseding a failed requirement produces a visible scope decision rather than erasing failure history
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-017 [P1] ASPEII-RQ-017: Challenges, Contradictions, and Repair Proposals

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:396-408` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-017; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-017: Challenges, Contradictions, and Repair Proposals

Priority P1. Dependencies: 016, 019.

1. Register deterministic challenge functions for missing boundaries, missing evidence, unsupported premises, stale support, and structured contradictions.
2. Treat natural-language contradiction detection as a proposal requiring structured confirmation or human adjudication.
3. Record counterexamples, challenge versions, execution outcomes, severity, and exact target revisions.
4. Generate bounded repair proposals with before/after claims, affected dependents, and revalidation obligations; never self-approve repairs.
5. Bound challenge iterations and resources; report no-new-failures only for the executed suite and scope.
6. Prevent evaluation or requirement changes from being used to retroactively pass a previously failed run.

Acceptance: contradictory structured constraints fail deterministically; an inconclusive model critique remains INCONCLUSIVE; a loop hitting its budget cannot report convergence.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-017' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-017') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-017

**Acceptance criteria**
- [ ] contradictory structured constraints fail deterministically; an inconclusive model critique remains INCONCLUSIVE; a loop hitting its budget cannot report convergence
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-024 [P1] ASPEII-RQ-024: Semantic Views and Browse/Resolve

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:487-499` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-024; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-024: Semantic Views and Browse/Resolve

Priority P1. Dependencies: 013, 015, 023.

1. Expose typed terms, mappings, constraints, evidence, and relationships as versioned views over EOIP ontology/graph records.
2. Provide bounded semantic browse and resolve APIs/MCP tools returning IDs, revisions, source locators, ambiguity, support state, and access-filtered related objects.
3. Return a compact session manifest with version/capabilities and no hidden tenant data; load detail on demand.
4. Keep source schema, business ontology, agent content view, and executable-tool catalog distinct with explicit mappings.
5. Preserve ambiguous mappings and unsupported vocabulary as reviewable records; never invent a fallback relation merely to connect nodes.
6. Pin a semantic snapshot per task while checking current permissions; report version changes and incomplete/truncated retrieval.

Acceptance: two ambiguous terms produce alternatives, not an invented unique mapping; a hidden linked record cannot leak through resolve counts, labels, or paths.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-024' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-024') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-024

**Acceptance criteria**
- [ ] two ambiguous terms produce alternatives, not an invented unique mapping; a hidden linked record cannot leak through resolve counts, labels, or paths
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-027 [P1] ASPEII-RQ-027: Isolated Evolution Candidates

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:526-538` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-027; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-027: Isolated Evolution Candidates

Priority P1. Dependencies: 025, 026.

1. Create immutable candidates against exact parents with a single declared change layer and a falsifiable improvement hypothesis.
2. Limit content/schema patches to typed operations; tool-layer patches may only configure already reviewed tool implementations within existing permissions.
3. Prevent candidates from modifying policies, grants, trusted verifiers, benchmark labels, evaluation splits, approval requirements, or active versions.
4. Validate structural consistency, scope, licensing of imported artifacts, migration effects, and reversibility before evaluation.
5. Execute candidates in isolated storage/source snapshots with denied production egress and no side effects beyond the evaluation sandbox.
6. Bound rounds/resources and persist rejection/inconclusive reasons; no synthetic passing candidate when search budget expires.

Acceptance: a patch adding an arbitrary Python tool or disabling a failed check is rejected; evaluating a candidate leaves the published semantic digest unchanged.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-027' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-027') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-027

**Acceptance criteria**
- [ ] a patch adding an arbitrary Python tool or disabling a failed check is rejected; evaluating a candidate leaves the published semantic digest unchanged
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-028 [P1] ASPEII-RQ-028: Paired Evaluation and Promotion Gate

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:539-551` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-028; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-028: Paired Evaluation and Promotion Gate

Priority P1. Dependencies: 027, 035.

1. Freeze parent, candidate, tasks, datasets, evaluator, model/tool versions, seeds, decoding, interaction budgets, and thresholds before comparison.
2. Separate construction, validation, and final qualification data; use origin/time-aware splits and prevent labels or evaluation feedback leaking to builders.
3. Evaluate identical paired tasks with comparable resource budgets and retain all cases, including timeout/error/abstention outcomes.
4. Apply section 1.3 thresholds, paired uncertainty estimates, critical-stratum checks, and hard security/schema gates; insufficient evidence is INCONCLUSIVE.
5. Use model judges only as advisory scores unless independently adjudicated to the required task rubric; no safety or factual-support gate may rely solely on a generator.
6. Qualify each target model/domain profile independently and rotate/refresh validation reserves to limit repeated-search overfitting; final qualification data remains untouched until candidate selection ends.

Acceptance: a mean gain hiding a critical-domain regression fails; changing the evaluator after seeing scores invalidates the run; an interrupted comparison cannot publish.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-RQ-028' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-RQ-028') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-RQ-028

**Acceptance criteria**
- [ ] a mean gain hiding a critical-domain regression fails; changing the evaluator after seeing scores invalidates the run; an interrupted comparison cannot publish
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-E2E-01 [P2] ASPEII-E2E-01: Read-only incident investigation from intent through delegated analysis to GUI

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:735-735` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-E2E-01; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ASPEII-E2E-01 | Read-only incident investigation from intent through delegated analysis to GUI | Typed evidence, bounded tasks, acceptance results, no mutation; restart retains run
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-E2E-01' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-E2E-01') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-E2E-01

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ASPEII-E2E-01 | Read-only incident investigation from intent through delegated analysis to GUI | Typed evidence, bounded tasks, acceptance results, no mutation; restart retains run»
- [ ] Read-only incident investigation from intent through delegated analysis to GUI
- [ ] Typed evidence, bounded tasks, acceptance results, no mutation; restart retains run
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-E2E-02 [P2] ASPEII-E2E-02: Ambiguous goal and missing budget/destination

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:736-736` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-E2E-02; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ASPEII-E2E-02 | Ambiguous goal and missing budget/destination | Draft saved; consequential activation blocked with actionable missing fields
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-E2E-02' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-E2E-02') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-E2E-02

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ASPEII-E2E-02 | Ambiguous goal and missing budget/destination | Draft saved; consequential activation blocked with actionable missing fields»
- [ ] Ambiguous goal and missing budget/destination
- [ ] Draft saved; consequential activation blocked with actionable missing fields
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-E2E-03 [P2] ASPEII-E2E-03: Evidence laundering across generator, MCP, database, RAG and critic

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:737-737` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-E2E-03; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ASPEII-E2E-03 | Evidence laundering across generator, MCP, database, RAG and critic | Origin preserved; no factual promotion or action approval from circular support
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-E2E-03' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-E2E-03') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-E2E-03

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ASPEII-E2E-03 | Evidence laundering across generator, MCP, database, RAG and critic | Origin preserved; no factual promotion or action approval from circular support»
- [ ] Evidence laundering across generator, MCP, database, RAG and critic
- [ ] Origin preserved; no factual promotion or action approval from circular support
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-E2E-06 [P2] ASPEII-E2E-06: Concurrent delegation, exhausted root budget and expired worker

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:740-740` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-E2E-06; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ASPEII-E2E-06 | Concurrent delegation, exhausted root budget and expired worker | Only eligible fenced worker acts; aggregate ceiling respected
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-E2E-06' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-E2E-06') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-E2E-06

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ASPEII-E2E-06 | Concurrent delegation, exhausted root budget and expired worker | Only eligible fenced worker acts; aggregate ceiling respected»
- [ ] Concurrent delegation, exhausted root budget and expired worker
- [ ] Only eligible fenced worker acts; aggregate ceiling respected
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-E2E-07 [P2] ASPEII-E2E-07: External write commits then times out

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:741-741` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-E2E-07; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ASPEII-E2E-07 | External write commits then times out | UNKNOWN_OUTCOME then reconciliation; no blind retry/duplicate effect
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-E2E-07' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-E2E-07') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-E2E-07

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ASPEII-E2E-07 | External write commits then times out | UNKNOWN_OUTCOME then reconciliation; no blind retry/duplicate effect»
- [ ] External write commits then times out
- [ ] UNKNOWN_OUTCOME then reconciliation; no blind retry/duplicate effect
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-E2E-09 [P2] ASPEII-E2E-09: Build initial semantic layer from table/document sources

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:743-743` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-E2E-09; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ASPEII-E2E-09 | Build initial semantic layer from table/document sources | Real read probes, typed mappings and unsupported proposals; approval-gated version zero
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-E2E-09' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-E2E-09') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-E2E-09

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ASPEII-E2E-09 | Build initial semantic layer from table/document sources | Real read probes, typed mappings and unsupported proposals; approval-gated version zero»
- [ ] Build initial semantic layer from table/document sources
- [ ] Real read probes, typed mappings and unsupported proposals; approval-gated version zero
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-E2E-10 [P2] ASPEII-E2E-10: Candidate improves held-out tasks but violates a security invariant

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:744-744` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-E2E-10; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ASPEII-E2E-10 | Candidate improves held-out tasks but violates a security invariant | Rejected; parent remains active; failure visible in GUI
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-E2E-10' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-E2E-10') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-E2E-10

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ASPEII-E2E-10 | Candidate improves held-out tasks but violates a security invariant | Rejected; parent remains active; failure visible in GUI»
- [ ] Candidate improves held-out tasks but violates a security invariant
- [ ] Rejected; parent remains active; failure visible in GUI
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-E2E-12 [P2] ASPEII-E2E-12: Conflicting requirements and finite challenge budget

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:746-746` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-E2E-12; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ASPEII-E2E-12 | Conflicting requirements and finite challenge budget | Counterexample recorded; unresolved claim stays incomplete; no universal-convergence claim
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-E2E-12' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-E2E-12') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-E2E-12

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ASPEII-E2E-12 | Conflicting requirements and finite challenge budget | Counterexample recorded; unresolved claim stays incomplete; no universal-convergence claim»
- [ ] Conflicting requirements and finite challenge budget
- [ ] Counterexample recorded; unresolved claim stays incomplete; no universal-convergence claim
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-E2E-13 [P2] ASPEII-E2E-13: Actual stdio and HTTP MCP sessions

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:747-747` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-E2E-13; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ASPEII-E2E-13 | Actual stdio and HTTP MCP sessions | Real server logs match calls; unreachable/malicious/schema-changing server fails safely
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-E2E-13' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-E2E-13') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-E2E-13

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ASPEII-E2E-13 | Actual stdio and HTTP MCP sessions | Real server logs match calls; unreachable/malicious/schema-changing server fails safely»
- [ ] Actual stdio and HTTP MCP sessions
- [ ] Real server logs match calls; unreachable/malicious/schema-changing server fails safely
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-E2E-16 [P2] ASPEII-E2E-16: Full GUI and release-verifier negative controls

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:750-750` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-E2E-16; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ASPEII-E2E-16 | Full GUI and release-verifier negative controls | Real backend workflow succeeds; removal/staleness of one mandatory receipt prevents 100% completion
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ASPEII-E2E-16' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ASPEII-E2E-16') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ASPEII-E2E-16

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ASPEII-E2E-16 | Full GUI and release-verifier negative controls | Real backend workflow succeeds; removal/staleness of one mandatory receipt prevents 100% completion»
- [ ] Full GUI and release-verifier negative controls
- [ ] Real backend workflow succeeds; removal/staleness of one mandatory receipt prevents 100% completion
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

