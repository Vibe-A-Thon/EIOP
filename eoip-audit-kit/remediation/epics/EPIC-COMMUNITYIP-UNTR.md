# EPIC-COMMUNITYIP-UNTR: EOIP-engg-doc-pkg/community-ip-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 34 tasks, ~224.0 h, priorities {'P0': 26, 'P1': 8}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-CIP-E2E-01 [P0] CIP-E2E-01: Correction With Independent Support

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:335-338` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-E2E-01; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-E2E-01: Correction With Independent Support

Create two independent evidence sources supporting an agent result. Correct one. Verify impact and descendants, invalidated path, surviving path, pinned evaluation, and `CURRENT` only if all gates pass. Historical version is available only under authorized historical access.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-E2E-01' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-E2E-01') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-E2E-01

**Acceptance criteria**
- [ ] Create two independent evidence sources supporting an agent result.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-E2E-02 [P0] CIP-E2E-02: Revocation Before Worker Processing

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:339-342` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-E2E-02; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-E2E-02: Revocation Before Worker Processing

Create answer, cache, citation and memory from restricted source. Downgrade access, then request through API/UI/MCP/export/cache before worker processing. Each path denies or safely redacts. After processing, verify lifecycle/audit and no redisclosure.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-E2E-02' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-E2E-02') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-E2E-02

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Revocation Before Worker Processing Create answer, cache, citation and memory from restricted source. Downgrade access, then request through API/UI/MCP/export/cache before worker processing. Each path denies or safely redacts. After processing, verify lifecycle/audit and no redisclosure.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-001 [P0] CIP-RQ-001: Source and Scope Inventory

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:121-126` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-001: Source and Scope Inventory

Inventory existing event, provenance, memory, agent trace, proposal, policy, evaluation, graph revision, authorization, storage, worker, API, UI, and deployment contracts. For each candidate integration, record observed request/response/schema, durability, tenant scope, auth path, and tests actually executed. Assign `REUSE_VERIFIED`, `EXTEND`, `REPLACE_WITH_APPROVAL`, or `NOT_PRESENT`; gaps have owners and tasks.

**Acceptance:** `AC-001.1` all domains inventoried; `AC-001.2` every reused boundary has runtime contract evidence; `AC-001.3` all gaps have owner/task; `AC-001.4` unrelated user worktree changes are preserved.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-001

**Acceptance criteria**
- [ ] AC-001.1 all domains inventoried; AC-001.2 every reused boundary has runtime contract evidence; AC-001.3 all gaps have owner/task; AC-001.4 unrelated user worktree changes are preserved.
- [ ] AC-001.1 all domains inventoried; AC-001.2 every reused boundary has runtime contract evidence; AC-001.3 all gaps have owner/task; AC-001.4 unrelated user worktree changes are preserved
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-002 [P0] CIP-RQ-002: Typed Dependency Contract

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:127-132` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-002: Typed Dependency Contract

Implement versioned artifact and dependency schemas from Section 3. Validate IDs, kinds, revision references, tenant consistency, semantics, timestamps, and graph-size bounds. Reject empty IDs, cross-tenant edges, missing revisions, malformed times, unsupported schema versions, and invalid self-dependencies. Unknown semantic fields are never ignored.

**Acceptance:** `AC-002.1` contract tests cover valid round-trip and every invalid input/rejection. `AC-002.2` migration, unsupported-version rejection, deterministic canonical digest, and cross-tenant rejection pass through the persistence boundary.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-002

**Acceptance criteria**
- [ ] AC-002.1 contract tests cover valid round-trip and every invalid input/rejection. AC-002.2 migration, unsupported-version rejection, deterministic canonical digest, and cross-tenant rejection pass through the persistence boundary.
- [ ] AC-002.1 contract tests cover valid round-trip and every invalid input/rejection. AC-002.2 migration, unsupported-version rejection, deterministic canonical digest, and cross-tenant rejection pass through the persistence boundary
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-004 [P0] CIP-RQ-004: Durable Mutation/Event Processing

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:139-144` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-004: Durable Mutation/Event Processing

Use verified transaction/outbox or equivalent durable event semantics. A committed mutation cannot be lost if the process crashes before consumption. Duplicates are idempotent. Cursors and impact records recover after API/worker restart. If mutation and event cannot share a transaction, implement an explicit recoverable reconciliation protocol and pending state; do not claim atomicity or exactly-once delivery without proof.

**Acceptance:** `AC-004.1` crash injection at every listed mutation/publication/cursor boundary recovers without losing a committed change. `AC-004.2` duplicate delivery/replay converges to one logical impact and action.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-004

**Acceptance criteria**
- [ ] AC-004.1 crash injection at every listed mutation/publication/cursor boundary recovers without losing a committed change. AC-004.2 duplicate delivery/replay converges to one logical impact and action.
- [ ] AC-004.1 crash injection at every listed mutation/publication/cursor boundary recovers without losing a committed change. AC-004.2 duplicate delivery/replay converges to one logical impact and action
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-005 [P0] CIP-RQ-005: Change Classification and Provenance

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:145-150` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-005: Change Classification and Provenance

Preserve source/event IDs, revisions, change kind, tenant, actor, policy context, valid/recorded times, causal correlation, and redacted digest metadata. Apply temporal ordering to late events; do not mutate current state from a late event without that policy. Reject/quarantine duplicate, malformed, or untrusted events; never permissively mark current.

**Acceptance:** `AC-005.1` tests verify change classification, ordering, duplicate handling, actor binding, and temporal semantics. `AC-005.2` stored event metadata contains no source payload, credential, or secret canary.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-005

**Acceptance criteria**
- [ ] AC-005.1 tests verify change classification, ordering, duplicate handling, actor binding, and temporal semantics. AC-005.2 stored event metadata contains no source payload, credential, or secret canary.
- [ ] AC-005.1 tests verify change classification, ordering, duplicate handling, actor binding, and temporal semantics. AC-005.2 stored event metadata contains no source payload, credential, or secret canary
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-006 [P0] CIP-RQ-006: Bounded Impact Computation

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:151-156` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-006: Bounded Impact Computation

Compute transitive reverse dependency closure for authorized changed artifacts at an explicit temporal coordinate. Return direct/indirect paths, roots, revisions, states, and completeness/truncation metadata. Traversal is cycle-safe and deterministic, bounded by depth, nodes, fan-out, time, and tenant scope. Limits yield `complete=false` and reason, never a false complete result.

**Acceptance:** `AC-006.1` tests cover chains, diamonds, multiple roots, cycles, disconnected graphs, duplicate edges, and removed dependencies. `AC-006.2` property-based cases match a reference closure; limit/timeout cases report incomplete status and deterministic ordering.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-006

**Acceptance criteria**
- [ ] AC-006.1 tests cover chains, diamonds, multiple roots, cycles, disconnected graphs, duplicate edges, and removed dependencies. AC-006.2 property-based cases match a reference closure; limit/timeout cases report incomplete status and deterministic ordering.
- [ ] AC-006.1 tests cover chains, diamonds, multiple roots, cycles, disconnected graphs, duplicate edges, and removed dependencies. AC-006.2 property-based cases match a reference closure; limit/timeout cases report incomplete status and deterministic ordering
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-007 [P0] CIP-RQ-007: Independent-Support Analysis

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:157-162` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-007: Independent-Support Analysis

For multi-source derived artifacts, determine whether a valid, authorized, non-retracted support path remains. Enumerate valid/invalid paths and assumptions. Do not keep an output current just because text/confidence is unchanged; do not invalidate independent support because one redundant source changed. Incomplete/uncertain dependencies yield `UNKNOWN` or `QUARANTINED` under risk policy.

**Acceptance:** `AC-007.1` cases cover one-of-many invalidation, all evidence invalid, contradictory surviving evidence, duplicate-content sources, and inaccessible evidence. `AC-007.2` incomplete dependency capture yields the required conservative state and cannot be marked current.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-007

**Acceptance criteria**
- [ ] AC-007.1 cases cover one-of-many invalidation, all evidence invalid, contradictory surviving evidence, duplicate-content sources, and inaccessible evidence. AC-007.2 incomplete dependency capture yields the required conservative state and cannot be marked current.
- [ ] AC-007.1 cases cover one-of-many invalidation, all evidence invalid, contradictory surviving evidence, duplicate-content sources, and inaccessible evidence. AC-007.2 incomplete dependency capture yields the required conservative state and cannot be marked current
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-008 [P0] CIP-RQ-008: Temporal and Historical Views

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:163-168` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-008; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-008: Temporal and Historical Views

Evaluate explicit `valid_at` and `known_at`/recorded-time coordinates compatible with EOIP bitemporal behavior. Distinguish current belief from historical knowledge. Historical views still obey current authorization, retention, hold, and deletion policy. API/UI label coordinates and historical/current/partial/reconstructed status.

**Acceptance:** `AC-008.1` backdated correction, late arrival, retraction, and historical/current queries return the correct valid-time and known-time views. `AC-008.2` post-creation access downgrade and retention expiry remain enforced in historical views.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-008

**Acceptance criteria**
- [ ] AC-008.1 backdated correction, late arrival, retraction, and historical/current queries return the correct valid-time and known-time views. AC-008.2 post-creation access downgrade and retention expiry remain enforced in historical views.
- [ ] AC-008.1 backdated correction, late arrival, retraction, and historical/current queries return the correct valid-time and known-time views. AC-008.2 post-creation access downgrade and retention expiry remain enforced in historical views
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-009 [P0] CIP-RQ-009: Authorization Revocation Fast Path

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:169-174` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-009; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-009: Authorization Revocation Fast Path

Access reduction, revocation, tenant change, or policy update must deny affected reads synchronously at authoritative boundaries; background processing is not required to stop disclosure. Re-key/invalidate caches by principal, tenant, and policy revision. Prevent stale websocket, MCP, export, and browser state from serving restricted evidence. Avoid existence/count/timing leaks beyond policy.

**Acceptance:** `AC-009.1` downgrade blocks the next authoritative read before worker processing. `AC-009.2` REST, UI, MCP, export, cache, websocket/event stream all deny or safely redact before and after asynchronous processing without existence leakage.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-009

**Acceptance criteria**
- [ ] AC-009.1 downgrade blocks the next authoritative read before worker processing. AC-009.2 REST, UI, MCP, export, cache, websocket/event stream all deny or safely redact before and after asynchronous processing without existence leakage.
- [ ] AC-009.1 downgrade blocks the next authoritative read before worker processing. AC-009.2 REST, UI, MCP, export, cache, websocket/event stream all deny or safely redact before and after asynchronous processing without existence leakage
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-011 [P0] CIP-RQ-011: Dry-Run Immutable Plan

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:181-186` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-011; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-011: Dry-Run Immutable Plan

Plan includes tenant, actor, event IDs, input/dependency snapshot, policy revision, affected artifacts, ordered actions, expected revisions, bounds, digest, creation/expiry, and completeness. Reject/recompute if revisions or policy change before approval/execution. Dry run cannot mutate source, graph, artifact content, or external systems; only an auditable plan record may be persisted.

**Acceptance:** `AC-011.1` persisted plan contains all required snapshot, scope, action, time, completeness, and digest fields. `AC-011.2` dry run has no prohibited side effects; stale snapshot, tampering, expiry, duplicate submission, and digest determinism are tested.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-011

**Acceptance criteria**
- [ ] AC-011.1 persisted plan contains all required snapshot, scope, action, time, completeness, and digest fields. AC-011.2 dry run has no prohibited side effects; stale snapshot, tampering, expiry, duplicate submission, and digest determinism are tested.
- [ ] AC-011.1 persisted plan contains all required snapshot, scope, action, time, completeness, and digest fields. AC-011.2 dry run has no prohibited side effects; stale snapshot, tampering, expiry, duplicate submission, and digest determinism are tested
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-012 [P0] CIP-RQ-012: Approval and Execution Safety

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:187-192` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-012; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-012: Approval and Execution Safety

Reuse proposal/approval only if runtime tests prove actor, tenant, role, plan digest, policy revision, expiry, and single-use binding. Human approval is mandatory for purge, consequential retraction, evaluation baseline change, and external reconciliation. Automatic in-platform re-evaluation/quarantine requires explicit versioned policy. No unapproved write tool; approval cannot authorize another tenant or plan revision.

**Acceptance:** `AC-012.1` deny self-approval where prohibited, wrong tenant/role, altered/expired/replayed approval, and changed policy. `AC-012.2` runtime/tool registration cannot bypass governed approval or execute an unapproved write.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-012

**Acceptance criteria**
- [ ] AC-012.1 deny self-approval where prohibited, wrong tenant/role, altered/expired/replayed approval, and changed policy. AC-012.2 runtime/tool registration cannot bypass governed approval or execute an unapproved write.
- [ ] AC-012.1 deny self-approval where prohibited, wrong tenant/role, altered/expired/replayed approval, and changed policy. AC-012.2 runtime/tool registration cannot bypass governed approval or execute an unapproved write
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-014 [P0] CIP-RQ-014: Evaluation Before Reinstatement

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:199-204` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-014; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-014: Evaluation Before Reinstatement

Pin evaluator, dataset, prompt, model, tool schema, policy, and graph/source snapshot. Compare candidate/baseline on correctness, evidence coverage/groundedness, policy violations, abstention, safety, latency, cost where available, and domain metrics. Missing metrics are `UNKNOWN`. Reinstate only if all mandatory quality/security gates pass and evidence remains authorized. Model judges cannot be sole oracle for deterministic invariants.

**Acceptance:** `AC-014.1` evaluation pins all required candidate/baseline inputs and verifies exact deterministic golden outcomes. `AC-014.2` probabilistic metrics declare paired method, sampling config, seed, and minimum sample count; missing/insufficient evidence blocks reinstatement.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-014' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-014') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-014

**Acceptance criteria**
- [ ] AC-014.1 evaluation pins all required candidate/baseline inputs and verifies exact deterministic golden outcomes. AC-014.2 probabilistic metrics declare paired method, sampling config, seed, and minimum sample count; missing/insufficient evidence blocks reinstatement.
- [ ] AC-014.1 evaluation pins all required candidate/baseline inputs and verifies exact deterministic golden outcomes. AC-014.2 probabilistic metrics declare paired method, sampling config, seed, and minimum sample count; missing/insufficient evidence blocks reinstatement
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-015 [P0] CIP-RQ-015: Evaluation Threshold Governance

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:205-210` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-015; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-015: Evaluation Threshold Governance

Version, freeze, and assign owners to gates before candidate evaluation. Unauthorized disclosure, cross-tenant data, missing required dependency, integrity error, or unapproved side effect always fails. Domain thresholds may vary only within governed bounds. Baseline changes require actor/approval and dataset/evaluator digests. Never tune thresholds after seeing candidate results.

**Acceptance:** `AC-015.1` version binding, governed policy range, and approved baseline are enforced. `AC-015.2` candidate comparisons are immutable; threshold changes after result inspection and attempts to erase failed gates are rejected/audited.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-015' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-015') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-015

**Acceptance criteria**
- [ ] AC-015.1 version binding, governed policy range, and approved baseline are enforced. AC-015.2 candidate comparisons are immutable; threshold changes after result inspection and attempts to erase failed gates are rejected/audited.
- [ ] AC-015.1 version binding, governed policy range, and approved baseline are enforced. AC-015.2 candidate comparisons are immutable; threshold changes after result inspection and attempts to erase failed gates are rejected/audited
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-016 [P0] CIP-RQ-016: Read-Time Lifecycle Gate

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:211-216` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-016; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-016: Read-Time Lifecycle Gate

Every API/UI/MCP/export retrieval rechecks tenant, authorization, state, retention, and policy. `STALE`, `REVOKED`, `QUARANTINED`, and `UNKNOWN` artifacts cannot silently appear current or enter new agent context. Provide safe state and authorized remediation details. Apply freshness to new runs and memory recall.

**Acceptance:** `AC-016.1` route/browser tests cover stale memory, citations, partial results, and export lifecycle behavior. `AC-016.2` hidden metadata is denied, and stale/revoked/unknown artifacts cannot enter a new context or be shown as current.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-016' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-016') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-016

**Acceptance criteria**
- [ ] AC-016.1 route/browser tests cover stale memory, citations, partial results, and export lifecycle behavior. AC-016.2 hidden metadata is denied, and stale/revoked/unknown artifacts cannot enter a new context or be shown as current.
- [ ] AC-016.1 route/browser tests cover stale memory, citations, partial results, and export lifecycle behavior. AC-016.2 hidden metadata is denied, and stale/revoked/unknown artifacts cannot enter a new context or be shown as current
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-017 [P0] CIP-RQ-017: Retention, Deletion, and Legal Hold

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:217-222` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-017; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-017: Retention, Deletion, and Legal Hold

Purge only under approved retention policy and authorized role, after legal-hold checks. Remove/cryptographically erase content and content-bearing caches as required; check graph, files, logs, indexes, exports, browser caches, backups, replicas. Keep only minimum non-sensitive audit tombstone allowed by policy. Unavailable store means purge incomplete.

**Acceptance:** `AC-017.1` unauthorized purge and purge under legal hold are denied and audited. `AC-017.2` synthetic canaries are searched across every declared store/derivative and documented backup behavior; residual content or unavailable store makes purge incomplete.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-017' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-017') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-017

**Acceptance criteria**
- [ ] AC-017.1 unauthorized purge and purge under legal hold are denied and audited. AC-017.2 synthetic canaries are searched across every declared store/derivative and documented backup behavior; residual content or unavailable store makes purge incomplete.
- [ ] AC-017.1 unauthorized purge and purge under legal hold are denied and audited. AC-017.2 synthetic canaries are searched across every declared store/derivative and documented backup behavior; residual content or unavailable store makes purge incomplete
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-018 [P0] CIP-RQ-018: Tenant and Principal Isolation

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:223-228` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-018; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-018: Tenant and Principal Isolation

Tenant-scope all records, edges, cursors, plans, receipts, queues, caches, exports, metrics with identifiers, and UI/API. Derive tenant from authenticated principal; caller selector requires authorized membership. Revalidate jobs at execution. Cross-tenant admin requires explicit scope/audit.

**Acceptance:** `AC-018.1` IDOR, guessed IDs, omitted filters, pagination mixing, cross-tenant edges, and cache collisions deny without leakage. `AC-018.2` event replay and worker payload tampering cannot cross tenant or principal scope.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-018' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-018') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-018

**Acceptance criteria**
- [ ] AC-018.1 IDOR, guessed IDs, omitted filters, pagination mixing, cross-tenant edges, and cache collisions deny without leakage. AC-018.2 event replay and worker payload tampering cannot cross tenant or principal scope.
- [ ] AC-018.1 IDOR, guessed IDs, omitted filters, pagination mixing, cross-tenant edges, and cache collisions deny without leakage. AC-018.2 event replay and worker payload tampering cannot cross tenant or principal scope
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-019 [P0] CIP-RQ-019: API Contract

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:229-234` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-019; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-019: API Contract

Provide authenticated, versioned operations for artifact freshness; bounded impact preview; dry-run plan create/read; approve/execute/cancel/recover; paginated impact/repair history; and isolated non-production benchmark run/report. Routes may follow local conventions but cannot weaken observable behavior. OpenAPI documents scopes, tenant binding, limits, idempotency, errors, partial results, and states. MCP remains read-only unless an existing proposal-only boundary explicitly applies; never expose repair execution as a read-only tool.

**Acceptance:** `AC-019.1` OpenAPI schemas describe all required operations, auth scopes, limits, partial results, and errors. `AC-019.2` authenticated real API tests verify tenant scope, pagination, idempotency, and error behavior; MCP exposes no ungoverned write.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-019' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-019') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-019

**Acceptance criteria**
- [ ] AC-019.1 OpenAPI schemas describe all required operations, auth scopes, limits, partial results, and errors. AC-019.2 authenticated real API tests verify tenant scope, pagination, idempotency, and error behavior; MCP exposes no ungoverned write.
- [ ] AC-019.1 OpenAPI schemas describe all required operations, auth scopes, limits, partial results, and errors. AC-019.2 authenticated real API tests verify tenant scope, pagination, idempotency, and error behavior; MCP exposes no ungoverned write
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-020 [P0] CIP-RQ-020: Operational UI

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:235-240` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-020; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-020: Operational UI

Show change/version, impact completeness/bounds, artifact counts by state/action, valid/invalid evidence paths, temporal coordinate, policy/tenant context, reversibility, approvals, execution progress/errors, and receipts. Provide filtering, detail, pagination, authorized recovery controls, and truthful empty/loading/partial/error/denied states. No fabricated success or operational values.

**Acceptance:** `AC-020.1` real API browser journeys cover correction/repair, downgrade denial, partial impact, approval, execution, worker restart, and evidence. `AC-020.2` keyboard operation, responsive viewports, and truthful loading/empty/error/denied states pass.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-020' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-020') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-020

**Acceptance criteria**
- [ ] AC-020.1 real API browser journeys cover correction/repair, downgrade denial, partial impact, approval, execution, worker restart, and evidence. AC-020.2 keyboard operation, responsive viewports, and truthful loading/empty/error/denied states pass.
- [ ] AC-020.1 real API browser journeys cover correction/repair, downgrade denial, partial impact, approval, execution, worker restart, and evidence. AC-020.2 keyboard operation, responsive viewports, and truthful loading/empty/error/denied states pass
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-021 [P0] CIP-RQ-021: Performance and Bounds

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:241-246` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-021; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-021: Performance and Bounds

All work is bounded and validated; caller limits cannot exceed server maxima. Initial profile: 10,000 dependency edges per tenant, 100 changed roots, closure capped at 10,000 artifacts, impact-preview p95 <= 5 seconds on declared reference environment. Access revocation blocks the next authoritative API read immediately without queue dependency. Record environment, graph shape, warm/cold state, concurrency, percentiles, and memory. Missing profile data invalidates measurement.

**Acceptance:** `AC-021.1` repeatable load test at the frozen profile meets closure and p95 targets and records p50/p95/p99, memory, queue age, errors, and truncation. `AC-021.2` timeout/oversize paths fail explicitly; revocation is immediate at read boundary; target changes require prior approved ADR.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-021' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-021') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-021

**Acceptance criteria**
- [ ] AC-021.1 repeatable load test at the frozen profile meets closure and p95 targets and records p50/p95/p99, memory, queue age, errors, and truncation. AC-021.2 timeout/oversize paths fail explicitly; revocation is immediate at read boundary; target changes require prior approved ADR.
- [ ] AC-021.1 repeatable load test at the frozen profile meets closure and p95 targets and records p50/p95/p99, memory, queue age, errors, and truncation. AC-021.2 timeout/oversize paths fail explicitly; revocation is immediate at read boundary; target changes require prior approved ADR
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-022 [P0] CIP-RQ-022: Observability and Audit

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:247-252` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-022; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-022: Observability and Audit

Emit redacted metrics/logs/traces for event lag, impact size/completeness, repair outcomes/retries, gate failures, denied stale/revoked reads, queue age and purge completeness. Correlate with non-secret IDs and tenant-safe pseudonyms. Audit plan/approval/execution/cancel/retry/purge/baseline actions. Observability must not create cross-tenant leakage.

**Acceptance:** `AC-022.1` emitted audit/log/metric records contain required correlation fields and redact secret/PII canaries. `AC-022.2` tenant isolation is verified and alerting/operator runbook is present and exercised.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-022' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-022') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-022

**Acceptance criteria**
- [ ] AC-022.1 emitted audit/log/metric records contain required correlation fields and redact secret/PII canaries. AC-022.2 tenant isolation is verified and alerting/operator runbook is present and exercised.
- [ ] AC-022.1 emitted audit/log/metric records contain required correlation fields and redact secret/PII canaries. AC-022.2 tenant isolation is verified and alerting/operator runbook is present and exercised
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-023 [P0] CIP-RQ-023: Failure and Recovery Semantics

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:253-258` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-023; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-023: Failure and Recovery Semantics

Define behavior for corrupt journal, unavailable graph/dependency/policy store, worker crash, duplicate/late event, clock skew, partial traversal, provider outage, invalid benchmark, and failed evaluation. Uncertain safety-critical impact denies/quarantines. Health distinguishes degraded/ready. Replay is bounded and cannot duplicate external actions.

**Acceptance:** `AC-023.1` fault injection covers each listed dependency/event/agent failure and health reflects degraded versus ready. `AC-023.2` recovery converges safely or records a non-recoverable state with actionable operator steps.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-023' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-023') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-023

**Acceptance criteria**
- [ ] AC-023.1 fault injection covers each listed dependency/event/agent failure and health reflects degraded versus ready. AC-023.2 recovery converges safely or records a non-recoverable state with actionable operator steps.
- [ ] AC-023.1 fault injection covers each listed dependency/event/agent failure and health reflects degraded versus ready. AC-023.2 recovery converges safely or records a non-recoverable state with actionable operator steps
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-024 [P0] CIP-RQ-024: AMRB Dataset and Scenario Contract

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:259-283` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-024; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-024' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-024') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-024

**Acceptance criteria**
- [ ] AC-024.1 validator rejects missing fields, duplicate IDs, secret-shaped data, invalid refs, underspecified oracle, and unsupported schema. AC-024.2 all 16 scenario families execute through real service/API integration with deterministic oracles, not mocks alone.
- [ ] AC-024.1 validator rejects missing fields, duplicate IDs, secret-shaped data, invalid refs, underspecified oracle, and unsupported schema. AC-024.2 all 16 scenario families execute through real service/API integration with deterministic oracles, not mocks alone
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-026 [P0] CIP-RQ-026: AMRB CLI and Reproducibility

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:290-295` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-026; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-026: AMRB CLI and Reproducibility

Provide documented validate/run/compare/export commands using EOIP CLI conventions. Support fixed seed, explicit profile, bounded concurrency, no implicit egress, JSON and human output. Record benchmark/evaluator digest, source revision, redacted config fingerprint, exact command/environment, per-case outcomes, raw metrics, summary and receipt digest. Never connect to or mutate production by default.

**Acceptance:** `AC-026.1` clean-checkout runs reproduce deterministic outcomes/counts and schema-valid export receipts. `AC-026.2` malformed input, egress, and production-store selection fail; results are independently recomputable.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-026' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-026') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-026

**Acceptance criteria**
- [ ] AC-026.1 clean-checkout runs reproduce deterministic outcomes/counts and schema-valid export receipts. AC-026.2 malformed input, egress, and production-store selection fail; results are independently recomputable.
- [ ] AC-026.1 clean-checkout runs reproduce deterministic outcomes/counts and schema-valid export receipts. AC-026.2 malformed input, egress, and production-store selection fail; results are independently recomputable
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-027 [P0] CIP-RQ-027: Community Artifact Safety

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:296-301` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-027; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-027: Community Artifact Safety

Prepare benchmark schema, synthetic fixtures, validator, runner interface, expected-result docs, contribution/security policy. Do not publish automatically. Before release, authorized owner selects compatible license, reviews dependencies/assets, privacy/secrets and IP disclosure timing, approves destination. Contributions must be reproducible and pass validation/security checks. Results are not product certification.

**Acceptance:** `AC-027.1` exact package digest has owner, privacy/security, license, and destination approvals. `AC-027.2` missing approval blocks publication while local validation remains runnable; benchmark is not represented as certification.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-027' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-027') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-027

**Acceptance criteria**
- [ ] AC-027.1 exact package digest has owner, privacy/security, license, and destination approvals. AC-027.2 missing approval blocks publication while local validation remains runnable; benchmark is not represented as certification.
- [ ] AC-027.1 exact package digest has owner, privacy/security, license, and destination approvals. AC-027.2 missing approval blocks publication while local validation remains runnable; benchmark is not represented as certification
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-028 [P0] CIP-RQ-028: IP and Invention-Record Hygiene

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:302-307` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-028; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-028: IP and Invention-Record Hygiene

Maintain a private access-controlled engineering record of dated human-authored problem statements, diagrams, algorithm versions, decisions, contributors, experiments, commands/results and digests. No secrets/customer data. Distinguish human contributions from model drafts. Do not send confidential details to external models/repos/issues without authorization. Do not make claims about AI inventorship or ownership based on tool ownership. Counsel/rightsholder owns patentability, inventorship, assignment, filing, defensive publication, licensing and FTO decisions. Agents may prepare a marked technical draft only when requested; never file/publish or claim patentability.

**Acceptance:** `AC-028.1` access control/redaction tests pass and contribution records distinguish human work from generated drafts. `AC-028.2` publication remains blocked absent authorized IP decision; no code or report automatically claims patent status.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-028' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-028') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-028

**Acceptance criteria**
- [ ] AC-028.1 access control/redaction tests pass and contribution records distinguish human work from generated drafts. AC-028.2 publication remains blocked absent authorized IP decision; no code or report automatically claims patent status.
- [ ] AC-028.1 access control/redaction tests pass and contribution records distinguish human work from generated drafts. AC-028.2 publication remains blocked absent authorized IP decision; no code or report automatically claims patent status
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-E2E-03 [P1] CIP-E2E-03: Restart and Duplicate Recovery

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:343-346` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-E2E-03; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-E2E-03: Restart and Duplicate Recovery

Crash between mutation and consumption, restart API/worker, replay event twice. Verify one logical impact/action, correct cursor, deterministic plan, full descendants, and no fabricated success.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-E2E-03' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-E2E-03') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-E2E-03

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Restart and Duplicate Recovery Crash between mutation and consumption, restart API/worker, replay event twice. Verify one logical impact/action, correct cursor, deterministic plan, full descendants, and no fabricated success.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-E2E-04 [P1] CIP-E2E-04: External Action Reconciliation

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:347-350` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-E2E-04; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-E2E-04: External Action Reconciliation

Invalidate evidence for a proposal referencing an external deployment/notification. Mark for reconciliation and require human proposal. No reversal API call; no claimed rollback success.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-E2E-04' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-E2E-04') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-E2E-04

**Acceptance criteria**
- [ ] Mark for reconciliation and require human proposal.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-E2E-05 [P1] CIP-E2E-05: Full AMRB Run

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:351-354` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-E2E-05; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-E2E-05: Full AMRB Run

From clean checkout, validate/run all scenarios, recompute metrics, bind source/environment, verify zero unauthorized disclosure/forbidden actions, export receipt. Skip/unavailable integration blocks full-pass label.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-E2E-05' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-E2E-05') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-E2E-05

**Acceptance criteria**
- [ ] From clean checkout, validate/run all scenarios, recompute metrics, bind source/environment, verify zero unauthorized disclosure/forbidden actions, export receipt.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-003 [P1] CIP-RQ-003: Dependency Capture

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:133-138` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-003: Dependency Capture

Capture direct dependencies when EOIP creates each supported retrieval, agent run, memory record, evaluation, and proposal. Include source/graph revisions, evidence manifest refs, prompt/contract/model/tool/policy/ontology versions, evaluator/dataset version, and tenant/principal context as applicable. Capture inputs actually read, not inferred from query text. Incomplete capture marks the artifact `UNKNOWN` with reason.

**Acceptance:** `AC-003.1` request-level tests cover retrieval, agent run, tool call, empty evidence, partial/budget-exhausted run, memory write, evaluation, and proposal. `AC-003.2` captured versions equal those consumed by runtime; incomplete capture persists `UNKNOWN` and cannot be presented as current.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-003

**Acceptance criteria**
- [ ] AC-003.1 request-level tests cover retrieval, agent run, tool call, empty evidence, partial/budget-exhausted run, memory write, evaluation, and proposal. AC-003.2 captured versions equal those consumed by runtime; incomplete capture persists UNKNOWN and cannot be presented as current.
- [ ] AC-003.1 request-level tests cover retrieval, agent run, tool call, empty evidence, partial/budget-exhausted run, memory write, evaluation, and proposal. AC-003.2 captured versions equal those consumed by runtime; incomplete capture persists UNKNOWN and cannot be presented as current
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-010 [P1] CIP-RQ-010: Repair Decision Matrix

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:175-180` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-010; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-010: Repair Decision Matrix

Each impacted artifact gets a deterministic decision: `KEEP_WITH_PROOF`, `RE_EVALUATE`, `RETRACT`, `QUARANTINE`, `PURGE_IF_AUTHORIZED`, `RECONCILIATION_REQUIRED`, or `MANUAL_REVIEW`. Record changes, invalid/current dependencies, surviving support, policy revision, decision-rule IDs, uncertainty, reversibility, required role, and side effects. Keep requires persisted proof; unknown never defaults to keep.

**Acceptance:** `AC-010.1` table-driven tests cover every action and input class, including missing/unknown dependencies and surviving evidence. `AC-010.2` deterministic inputs produce identical decisions/digests regardless of input ordering; `KEEP_WITH_PROOF` requires persisted proof.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-010

**Acceptance criteria**
- [ ] AC-010.1 table-driven tests cover every action and input class, including missing/unknown dependencies and surviving evidence. AC-010.2 deterministic inputs produce identical decisions/digests regardless of input ordering; KEEP_WITH_PROOF requires persisted proof.
- [ ] AC-010.1 table-driven tests cover every action and input class, including missing/unknown dependencies and surviving evidence. AC-010.2 deterministic inputs produce identical decisions/digests regardless of input ordering; KEEPWITHPROOF requires persisted proof
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-013 [P1] CIP-RQ-013: Idempotent and Recoverable Execution

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:193-198` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-013; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-013: Idempotent and Recoverable Execution

Use stable action IDs and expected revisions. Replays do not duplicate logical memory/evaluations/audit/proposals. Persist states `PLANNED`, `APPROVED`, `RUNNING`, `SUCCEEDED`, `FAILED_RETRYABLE`, `FAILED_FINAL`, `CANCELLED`, `NEEDS_REVIEW`; define bounded retries. Preserve prior state until mutation commits, support operator recovery, honor cancellation at safe checkpoints, and audit all attempts.

**Acceptance:** `AC-013.1` concurrent workers and duplicate retries produce one logical mutation/action. `AC-013.2` restart/cancellation/failure recovery never reports partial work as success and stays within retry policy.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-013

**Acceptance criteria**
- [ ] AC-013.1 concurrent workers and duplicate retries produce one logical mutation/action. AC-013.2 restart/cancellation/failure recovery never reports partial work as success and stays within retry policy.
- [ ] AC-013.1 concurrent workers and duplicate retries produce one logical mutation/action. AC-013.2 restart/cancellation/failure recovery never reports partial work as success and stays within retry policy
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-025 [P1] CIP-RQ-025: AMRB Metrics

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:284-289` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-025; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-025: AMRB Metrics

Report per-case and aggregate stale/revoked detection precision/recall; unauthorized disclosures (required zero); closure precision/recall; false-keep/invalidation; independent-support accuracy; action correctness/idempotency; crash convergence; truncation errors; latency/memory/retries/queue lag/cost; and unknown-dependency quarantine accuracy. Include numerators, denominators, confidence intervals, scenario strata, exclusions, and every failure. Never average away security failures or hide skips. Compare only matching benchmark/evaluator versions and environment declarations.

**Acceptance:** `AC-025.1` tests independently recompute every aggregate/confidence interval from raw outcomes and verify denominators/exclusions. `AC-025.2` any unauthorized disclosure or deterministic invariant failure fails the suite regardless of aggregate score.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-025' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-025') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-025

**Acceptance criteria**
- [ ] AC-025.1 tests independently recompute every aggregate/confidence interval from raw outcomes and verify denominators/exclusions. AC-025.2 any unauthorized disclosure or deterministic invariant failure fails the suite regardless of aggregate score.
- [ ] AC-025.1 tests independently recompute every aggregate/confidence interval from raw outcomes and verify denominators/exclusions. AC-025.2 any unauthorized disclosure or deterministic invariant failure fails the suite regardless of aggregate score
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CIP-RQ-029 [P1] CIP-RQ-029: Documentation and Migration

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:308-313` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-029; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-029: Documentation and Migration

Document architecture, state machine, schema, APIs, controls, operator procedures, deployment, retention/purge, backup/restore, replay/recovery, benchmark, limits and troubleshooting. Persistent changes require forward migration, compatibility, rollback or forward-repair, backup/restore and upgrade/downgrade tests. No migration required for optional ephemeral benchmark data unless selected persistence needs it.

**Acceptance:** `AC-029.1` architecture/API/operator/benchmark docs match the tested implementation in a clean walkthrough. `AC-029.2` migration from every supported prior schema and documented rollback/forward-repair are exercised.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CIP-RQ-029' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CIP-RQ-029') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-CIP-RQ-029

**Acceptance criteria**
- [ ] AC-029.1 architecture/API/operator/benchmark docs match the tested implementation in a clean walkthrough. AC-029.2 migration from every supported prior schema and documented rollback/forward-repair are exercised.
- [ ] AC-029.1 architecture/API/operator/benchmark docs match the tested implementation in a clean walkthrough. AC-029.2 migration from every supported prior schema and documented rollback/forward-repair are exercised
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

