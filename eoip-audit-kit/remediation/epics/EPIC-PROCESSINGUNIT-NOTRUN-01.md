# EPIC-PROCESSINGUNIT-NOTRUN-01: processing-units-requirements.md · tests_not_executed

*Tests are mapped/referenced but none ran in the audit (excluded or not collected).* 60 tasks, ~60.0 h, priorities {'P0': 24, 'P1': 21, 'P2': 15}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-PUR-CON-007 [P0] PUR-CON-007: Make plan-only execution side-effect free except authorized planning/audit records

- **Source:** `processing-units-requirements.md:138-138` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-CON-007 | Make plan-only execution side-effect free except authorized planning/audit records. | Instrumented dry run launches no model/kernel, changes no graph and performs no network acquisition.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Instrumented dry run launches no model/kernel, changes no graph and performs no network acquisition
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-CPU-005 [P0] PUR-CPU-005: graph.boundedtraverse: reuse graph traversal over an authorized snapshot with depth/result limits and truncation markers

- **Source:** `processing-units-requirements.md:299-299` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-CPU-005 | `graph.bounded_traverse`: reuse graph traversal over an authorized snapshot with depth/result limits and truncation markers. | Expected paths, cycles, missing nodes, unauthorized edges and truncation are independently reconciled.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Expected paths, cycles, missing nodes, unauthorized edges and truncation are independently reconciled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-DAT-001 [P0] PUR-DAT-001: Use immutable, tenant-scoped artifacts with atomic staging/finalization and authorized resolution

- **Source:** `processing-units-requirements.md:274-274` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-DAT-001 | Use immutable, tenant-scoped artifacts with atomic staging/finalization and authorized resolution. | Partial writes, traversal paths, symlinks/reparse points and cross-tenant IDs cannot become valid inputs.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Partial writes, traversal paths, symlinks/reparse points and cross-tenant IDs cannot become valid inputs
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-DAT-002 [P0] PUR-DAT-002: Record graph/data snapshot and input/model/operator/policy digests for every derived result

- **Source:** `processing-units-requirements.md:275-275` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-DAT-002 | Record graph/data snapshot and input/model/operator/policy digests for every derived result. | A verifier reconstructs the authorized inputs and detects modified content or a changed model.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] A verifier reconstructs the authorized inputs and detects modified content or a changed model
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-DAT-006 [P0] PUR-DAT-006: Apply retention, deletion and legal-hold rules to inputs, outputs, temporary files, vectors and evidence

- **Source:** `processing-units-requirements.md:279-279` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-DAT-006 | Apply retention, deletion and legal-hold rules to inputs, outputs, temporary files, vectors and evidence. | Expiry/purge/restart drills remove eligible derived data and preserve authorized holds without misleading deletion claims.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Expiry/purge/restart drills remove eligible derived data and preserve authorized holds without misleading deletion claims
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-INT-001 [P0] PUR-INT-001: Implement the versioned API in section 5 using existing auth/tenant middleware; no unauthenticated diagnostic bypass

- **Source:** `processing-units-requirements.md:398-398` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-INT-001 | Implement the versioned API in section 5 using existing auth/tenant middleware; no unauthenticated diagnostic bypass. | Browser/API jobs use the actual worker and persisted artifacts with authorized results and negative access tests.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Browser/API jobs use the actual worker and persisted artifacts with authorized results and negative access tests
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-INT-004 [P0] PUR-INT-004: Integrate vector/IPU results into authorized query/explorer/report workflows using immutable snapshot references

- **Source:** `processing-units-requirements.md:401-401` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-INT-004 | Integrate vector/IPU results into authorized query/explorer/report workflows using immutable snapshot references. | End-to-end user workflow shows derived evidence and unchanged source facts; revoked access remains denied.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] End-to-end user workflow shows derived evidence and unchanged source facts; revoked access remains denied
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-INT-006 [P0] PUR-INT-006: MCP and VS Code clients consume the same policy-checked API; do not grant an external AI client raw source data by default

- **Source:** `processing-units-requirements.md:403-403` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-INT-006 | MCP and VS Code clients consume the same policy-checked API; do not grant an external AI client raw source data by default. | Read capability/status metadata safely; sensitive results require explicit existing authorization and channel policy.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Read capability/status metadata safely; sensitive results require explicit existing authorization and channel policy
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-INT-008 [P0] PUR-INT-008: Add Configuration/Model Lab controls for profiles, artifact import/promotion and quotas using existing design/auth patterns

- **Source:** `processing-units-requirements.md:405-405` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-INT-008 | Add Configuration/Model Lab controls for profiles, artifact import/promotion and quotas using existing design/auth patterns. | Invalid/unauthorized changes fail server-side; effective revision, validation and rollback are visible.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Invalid/unauthorized changes fail server-side; effective revision, validation and rollback are visible
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-INT-009 [P0] PUR-INT-009: Add Governance evidence/provenance views and workflow-specific actions in Integration/Query/Reports rather than ten unrelated dashboards

- **Source:** `processing-units-requirements.md:406-406` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-INT-009 | Add Governance evidence/provenance views and workflow-specific actions in Integration/Query/Reports rather than ten unrelated dashboards. | A user follows input -> plan -> job -> result -> receipt -> source without copying secrets between apps.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] A user follows input -> plan -> job -> result -> receipt -> source without copying secrets between apps
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-IPU-004 [P0] PUR-IPU-004: graph.clusterfeatures: approved sklearn baseline over authorized features with seed, algorithm/version and quality diagnostics; clusters are hypotheses

- **Source:** `processing-units-requirements.md:380-380` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-IPU-004 | `graph.cluster_features`: approved sklearn baseline over authorized features with seed, algorithm/version and quality diagnostics; clusters are hypotheses. | Known fixture grouping plus stability/quality report; no semantic certainty from cluster IDs.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Known fixture grouping plus stability/quality report; no semantic certainty from cluster IDs
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/graph_intel.py:131`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/graph_intel.py#L131-L131)
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-LPU-004 [P0] PUR-LPU-004: text.summarizegrounded: approved local model, bounded retrieved context, resolvable citations, uncertainty and no automatic fact promotion

- **Source:** `processing-units-requirements.md:369-369` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-LPU-004 | `text.summarize_grounded`: approved local model, bounded retrieved context, resolvable citations, uncertainty and no automatic fact promotion. | Every cited source exists and is authorized; independently judged supported-claim/abstention thresholds pass.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Every cited source exists and is authorized; independently judged supported-claim/abstention thresholds pass
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/text_local.py:129`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/text_local.py#L129-L129)
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-LPU-005 [P0] PUR-LPU-005: query.propose: generate only a structured read-query proposal validated by the existing parser/planner; do not execute generated text automatically

- **Source:** `processing-units-requirements.md:370-370` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-LPU-005 | `query.propose`: generate only a structured read-query proposal validated by the existing parser/planner; do not execute generated text automatically. | Mutation/injection/unbounded-query attempts fail; a separate authorized user action runs an accepted read plan.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Mutation/injection/unbounded-query attempts fail; a separate authorized user action runs an accepted read plan
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/text_local.py:189`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/text_local.py#L189-L189)
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-NPU-004 [P0] PUR-NPU-004: model.batchinfer: bounded microbatching preserving per-input IDs, errors and cancellation; no unauthorized cross-tenant batching

- **Source:** `processing-units-requirements.md:328-328` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-NPU-004 | `model.batch_infer`: bounded microbatching preserving per-input IDs, errors and cancellation; no unauthorized cross-tenant batching. | Split/reordered/error batches reconcile to original items; memory remains within admission.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Split/reordered/error batches reconcile to original items; memory remains within admission
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-SEC-002 [P0] PUR-SEC-002: Deny all model/embedding/OCR runtime internet egress, including library downloads, license callbacks and telemetry

- **Source:** `processing-units-requirements.md:233-233` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-SEC-002 | Deny all model/embedding/OCR runtime internet egress, including library downloads, license callbacks and telemetry. | Independent network observation detects no permitted external connections during normal and adversarial runs.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Independent network observation detects no permitted external connections during normal and adversarial runs
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-SEC-003 [P0] PUR-SEC-003: Enforce worker network isolation with deployment controls, not monkey-patched sockets, regexes or a self-reported byte counter

- **Source:** `processing-units-requirements.md:234-234` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-SEC-003 | Enforce worker network isolation with deployment controls, not monkey-patched sockets, regexes or a self-reported byte counter. | Raw sockets, DNS/UDP, IPv6, proxies, subprocesses and redirect attempts cannot bypass the approved boundary.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Raw sockets, DNS/UDP, IPv6, proxies, subprocesses and redirect attempts cannot bypass the approved boundary
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-SEC-005 [P0] PUR-SEC-005: Authorize and minimize input before passing it to any model; secrets/credentials never enter a prompt

- **Source:** `processing-units-requirements.md:236-236` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-SEC-005 | Authorize and minimize input before passing it to any model; secrets/credentials never enter a prompt. | Seeded nested secrets and unnecessary fields are blocked/removed before the observed inference boundary.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Seeded nested secrets and unnecessary fields are blocked/removed before the observed inference boundary
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-SEC-008 [P0] PUR-SEC-008: Treat retrieved content, OCR and prompts as untrusted; prohibit instruction-driven tool, URL, file or policy escalation

- **Source:** `processing-units-requirements.md:239-239` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-SEC-008 | Treat retrieved content, OCR and prompts as untrusted; prohibit instruction-driven tool, URL, file or policy escalation. | Injected instructions produce no tool/network/mutation effect and cannot alter execution permissions.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Injected instructions produce no tool/network/mutation effect and cannot alter execution permissions
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-SEC-009 [P0] PUR-SEC-009: Allow only approved immutable model/parser artifacts; no pickle, remote code, dynamic plugin installation or unreviewed ONNX custom ops

- **Source:** `processing-units-requirements.md:240-240` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-SEC-009 | Allow only approved immutable model/parser artifacts; no pickle, remote code, dynamic plugin installation or unreviewed ONNX custom ops. | Tampered weights, path-traversing external tensor data and executable model bundles are rejected in isolation.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Tampered weights, path-traversing external tensor data and executable model bundles are rejected in isolation
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-SEC-010 [P0] PUR-SEC-010: Isolate process credentials, filesystem mounts, IPC, temporary files and caches by tenant/job

- **Source:** `processing-units-requirements.md:241-241` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-SEC-010 | Isolate process credentials, filesystem mounts, IPC, temporary files and caches by tenant/job. | Worker probes cannot read home directories, connector secrets, another job's files or another tenant's cache.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Worker probes cannot read home directories, connector secrets, another job's files or another tenant's cache
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-SEC-012 [P0] PUR-SEC-012: Exclude raw prompts, documents, vectors, images and secret-bearing exceptions from ordinary logs, traces and metrics

- **Source:** `processing-units-requirements.md:243-243` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-SEC-012 | Exclude raw prompts, documents, vectors, images and secret-bearing exceptions from ordinary logs, traces and metrics. | Canary scans across stdout/stderr, traces, errors, crash bundles and UI show no protected content.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Canary scans across stdout/stderr, traces, errors, crash bundles and UI show no protected content
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-SEC-013 [P0] PUR-SEC-013: Use approved cryptographic/storage services for encryption, signatures and secret references. A hash alone is not confidentiality or authenticity

- **Source:** `processing-units-requirements.md:244-244` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-SEC-013 | Use approved cryptographic/storage services for encryption, signatures and secret references. A hash alone is not confidentiality or authenticity. | Unauthorized readers cannot retrieve artifacts; forged evidence/digests fail verification and no hard-coded shared key is accepted.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Unauthorized readers cannot retrieve artifacts; forged evidence/digests fail verification and no hard-coded shared key is accepted
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-SEC-014 [P0] PUR-SEC-014: Local LLM outputs cannot authorize actions, resolve access policy or automatically become verified knowledge

- **Source:** `processing-units-requirements.md:245-245` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-SEC-014 | Local LLM outputs cannot authorize actions, resolve access policy or automatically become verified knowledge. | Malicious/incorrect generated SQL or graph updates remain proposals and cannot execute without the existing governed path.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Malicious/incorrect generated SQL or graph updates remain proposals and cannot execute without the existing governed path
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-SEC-015 [P0] PUR-SEC-015: Provide global/tenant/profile kill switches that stop new admission and revoke running publish authority

- **Source:** `processing-units-requirements.md:246-246` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-SEC-015 | Provide global/tenant/profile kill switches that stop new admission and revoke running publish authority. | Revocation is observed across processes; a stale local cache cannot continue privileged execution.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Revocation is observed across processes; a stale local cache cannot continue privileged execution
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-DAT-003 [P1] PUR-DAT-003: Preserve row/node IDs and stable order through batch/tensor conversion, filtering and graph features

- **Source:** `processing-units-requirements.md:276-276` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-DAT-003 | Preserve row/node IDs and stable order through batch/tensor conversion, filtering and graph features. | Results map exactly back to source IDs; unauthorized/filtered nodes do not reappear by array index.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Results map exactly back to source IDs; unauthorized/filtered nodes do not reappear by array index
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-DAT-008 [P1] PUR-DAT-008: Make result schemas portable and bounded; binary tensors use safe numeric formats, not arbitrary Python objects

- **Source:** `processing-units-requirements.md:281-281` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-DAT-008 | Make result schemas portable and bounded; binary tensors use safe numeric formats, not arbitrary Python objects. | Installed clients on supported OSes read results and reject tampered metadata/payload mismatches.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Installed clients on supported OSes read results and reject tampered metadata/payload mismatches
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-FND-007 [P1] PUR-FND-007: Keep configuration schema-versioned, validated, auditable and reversible. Unknown fields and unsafe combinations fail closed

- **Source:** `processing-units-requirements.md:106-106` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-FND-007 | Keep configuration schema-versioned, validated, auditable and reversible. Unknown fields and unsafe combinations fail closed. | Invalid configuration cannot enable external inference or elevate a capability; rollback restores the previous effective revision.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Invalid configuration cannot enable external inference or elevate a capability; rollback restores the previous effective revision
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-INT-005 [P1] PUR-INT-005: Register processing agent tools with typed contracts, delegated scope, budgets and cancellation; never direct arbitrary code execution

- **Source:** `processing-units-requirements.md:402-402` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-INT-005 | Register processing agent tools with typed contracts, delegated scope, budgets and cancellation; never direct arbitrary code execution. | A real agent invocation cannot exceed operator/tenant/action permissions; result/receipt links are resolvable.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] A real agent invocation cannot exceed operator/tenant/action permissions; result/receipt links are resolvable
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-LPU-006 [P1] PUR-LPU-006: Enforce token/time/memory limits, tenant-isolated KV caches, model identity and local-only execution; cancelled generation cannot publish

- **Source:** `processing-units-requirements.md:371-371` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-LPU-006 | Enforce token/time/memory limits, tenant-isolated KV caches, model identity and local-only execution; cancelled generation cannot publish. | Real local inference and no-egress measurements pass with missing-model, overflow and cancellation negatives.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Real local inference and no-egress measurements pass with missing-model, overflow and cancellation negatives
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-NPU-002 [P1] PUR-NPU-002: text.embed: approved local embedding artifact/tokenizer, deterministic batching, normalization declaration and model-space version

- **Source:** `processing-units-requirements.md:326-326` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-NPU-002 | `text.embed`: approved local embedding artifact/tokenizer, deterministic batching, normalization declaration and model-space version. | Same text/model yields comparable vectors; incompatible embedding spaces cannot be mixed.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Same text/model yields comparable vectors; incompatible embedding spaces cannot be mixed
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-OPS-003 [P1] PUR-OPS-003: Provide secure model/data import, quarantine, evaluation, promotion and rollback workflows

- **Source:** `processing-units-requirements.md:421-421` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-OPS-003 | Provide secure model/data import, quarantine, evaluation, promotion and rollback workflows. | Tampered/incompatible models never become active; rollback restores previous version with reproducible receipts.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Tampered/incompatible models never become active; rollback restores previous version with reproducible receipts
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-OPS-004 [P1] PUR-OPS-004: Expose safe metrics for queue age, throughput, errors, memory, stage latency, provider placement and fallback

- **Source:** `processing-units-requirements.md:422-422` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-OPS-004 | Expose safe metrics for queue age, throughput, errors, memory, stage latency, provider placement and fallback. | Metrics reconcile with job records without high-cardinality secret-bearing labels.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Metrics reconcile with job records without high-cardinality secret-bearing labels
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-OPS-005 [P1] PUR-OPS-005: Document customer-installed Windows/Linux single-host deployment separately from SaaS/multi-worker deployment

- **Source:** `processing-units-requirements.md:423-423` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-OPS-005 | Document customer-installed Windows/Linux single-host deployment separately from SaaS/multi-worker deployment. | Each advertised profile has its own recovery/isolation/capacity evidence; unsupported topology is rejected.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Each advertised profile has its own recovery/isolation/capacity evidence; unsupported topology is rejected
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-OPS-006 [P1] PUR-OPS-006: Maintain migration/backup/restore contracts for job state, configuration, model manifests and evidence

- **Source:** `processing-units-requirements.md:424-424` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-OPS-006 | Maintain migration/backup/restore contracts for job state, configuration, model manifests and evidence. | Old/new version compatibility and downgrade/restore drills preserve references and authorization.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Old/new version compatibility and downgrade/restore drills preserve references and authorization
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-OPS-007 [P1] PUR-OPS-007: Fail safely under disk full, dependency corruption, model/device loss, queue saturation and broker outage

- **Source:** `processing-units-requirements.md:425-425` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-OPS-007 | Fail safely under disk full, dependency corruption, model/device loss, queue saturation and broker outage. | Fault injection yields bounded failure/recovery with no silent precision downgrade or data loss claims.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Fault injection yields bounded failure/recovery with no silent precision downgrade or data loss claims
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-RUN-003 [P1] PUR-RUN-003: Implement leases, expiry, monotonically increasing fencing tokens and atomic result publication

- **Source:** `processing-units-requirements.md:189-189` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-RUN-003 | Implement leases, expiry, monotonically increasing fencing tokens and atomic result publication. | Expired/stale workers cannot heartbeat back into authority or publish after cancellation/reclaim.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Expired/stale workers cannot heartbeat back into authority or publish after cancellation/reclaim
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-SEC-004 [P1] PUR-SEC-004: Explicitly identify the local model trust boundary. Private IPs, .local, .internal and loopback are not automatically trusted services

- **Source:** `processing-units-requirements.md:235-235` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-SEC-004 | Explicitly identify the local model trust boundary. Private IPs, `.local`, `.internal` and loopback are not automatically trusted services. | A malicious local listener or reassigned destination is rejected; IPC/service identity is verified.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] A malicious local listener or reassigned destination is rejected; IPC/service identity is verified
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-SEC-006 [P1] PUR-SEC-006: Preserve existing sensitivity labels and D0-D4 policy mapping without inventing equivalences. Derived features/embeddings inherit source restrictions

- **Source:** `processing-units-requirements.md:237-237` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-SEC-006 | Preserve existing sensitivity labels and D0-D4 policy mapping without inventing equivalences. Derived features/embeddings inherit source restrictions. | A restricted source cannot become an unrestricted summary/vector/result through transformation.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] A restricted source cannot become an unrestricted summary/vector/result through transformation
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-SEC-007 [P1] PUR-SEC-007: Validate structured payloads recursively with depth/size bounds; DLP failure or unknown classification fails closed for model input

- **Source:** `processing-units-requirements.md:238-238` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-SEC-007 | Validate structured payloads recursively with depth/size bounds; DLP failure or unknown classification fails closed for model input. | Nested lists/maps, encoded-content cases, scanner errors and pathological inputs do not bypass admission.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Nested lists/maps, encoded-content cases, scanner errors and pathological inputs do not bypass admission
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-SEC-011 [P1] PUR-SEC-011: Reauthorize before dispatch, result download, report inclusion and graph publication; support revocation mid-job

- **Source:** `processing-units-requirements.md:242-242` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-SEC-011 | Reauthorize before dispatch, result download, report inclusion and graph publication; support revocation mid-job. | Revoked users cannot obtain new outputs or publish results from already queued work.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Revoked users cannot obtain new outputs or publish results from already queued work
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-SEC-016 [P1] PUR-SEC-016: Document and test residual risks: privileged-host compromise, native-library vulnerabilities, inference leakage and hardware side channels

- **Source:** `processing-units-requirements.md:247-247` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-SEC-016 | Document and test residual risks: privileged-host compromise, native-library vulnerabilities, inference leakage and hardware side channels. | Release security report names tested boundaries and unmitigated risks; it makes no absolute zero-leak guarantee.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Release security report names tested boundaries and unmitigated risks; it makes no absolute zero-leak guarantee
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-VER-002 [P1] PUR-VER-002: Run real API -> auth -> job -> worker -> library/model -> artifact -> UI/client journeys

- **Source:** `processing-units-requirements.md:448-448` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VER-002 | Run real API -> auth -> job -> worker -> library/model -> artifact -> UI/client journeys. | No mocks stand in for the component claimed qualified; captured outputs and state are independently reconciled.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] No mocks stand in for the component claimed qualified; captured outputs and state are independently reconciled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-VER-005 [P1] PUR-VER-005: Prove no-egress and data minimization at an independently observed worker/model boundary

- **Source:** `processing-units-requirements.md:451-451` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VER-005 | Prove no-egress and data minimization at an independently observed worker/model boundary. | Blocked attack attempts plus normal inference are captured outside the model process; self-reported zero bytes is insufficient.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Blocked attack attempts plus normal inference are captured outside the model process; self-reported zero bytes is insufficient
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-VER-006 [P1] PUR-VER-006: Test tenant isolation, grants, cache scope, output access, revocation and channel permissions under concurrency

- **Source:** `processing-units-requirements.md:452-452` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VER-006 | Test tenant isolation, grants, cache scope, output access, revocation and channel permissions under concurrency. | Adversarial cross-tenant runs reveal no unauthorized output or execution.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Adversarial cross-tenant runs reveal no unauthorized output or execution
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-VER-012 [P1] PUR-VER-012: Independent acceptance validates evidence content, environment binding, signatures/digests and negative-case coverage before capability promotion

- **Source:** `processing-units-requirements.md:458-458` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VER-012 | Independent acceptance validates evidence content, environment binding, signatures/digests and negative-case coverage before capability promotion. | Missing/tampered/stale/self-declared receipts cannot produce `SUPPORTED_QUALIFIED`.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Missing/tampered/stale/self-declared receipts cannot produce SUPPORTEDQUALIFIED
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-APU-002 [P2] PUR-APU-002: workflow.run: execute approved plan via shared jobs; checkpoint completed immutable stages and report per-stage results

- **Source:** `processing-units-requirements.md:357-357` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-APU-002 | `workflow.run`: execute approved plan via shared jobs; checkpoint completed immutable stages and report per-stage results. | Restart resumes eligible stages without duplicated effects or loss of provenance.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Restart resumes eligible stages without duplicated effects or loss of provenance
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-APU-003 [P2] PUR-APU-003: Select devices by policy/qualification/resources, then measured end-to-end cost including transfers; CPU default when no useful evidence exists

- **Source:** `processing-units-requirements.md:358-358` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-APU-003 | Select devices by policy/qualification/resources, then measured end-to-end cost including transfers; CPU default when no useful evidence exists. | Controlled selection fixtures show why a device was chosen; fake benchmark/configuration cannot grant qualification.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Controlled selection fixtures show why a device was chosen; fake benchmark/configuration cannot grant qualification
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-APU-004 [P2] PUR-APU-004: Reserve/release resources atomically across competing jobs; isolate tenant queues and provider/session state

- **Source:** `processing-units-requirements.md:359-359` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-APU-004 | Reserve/release resources atomically across competing jobs; isolate tenant queues and provider/session state. | Concurrency stress never oversubscribes configured reservations or leaks results between tenants.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Concurrency stress never oversubscribes configured reservations or leaks results between tenants
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-APU-005 [P2] PUR-APU-005: Enforce explicit fallback/cancellation semantics per stage and for the entire plan; never change precision/model to conceal failure

- **Source:** `processing-units-requirements.md:360-360` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-APU-005 | Enforce explicit fallback/cancellation semantics per stage and for the entire plan; never change precision/model to conceal failure. | Device loss either yields documented equivalent CPU fallback or fails; receipt records all attempted and actual providers.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Device loss either yields documented equivalent CPU fallback or fails; receipt records all attempted and actual providers
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-CON-006 [P2] PUR-CON-006: Define dtype, layout, shape and null/NaN/Inf/overflow handling per operator

- **Source:** `processing-units-requirements.md:137-137` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-CON-006 | Define dtype, layout, shape and null/NaN/Inf/overflow handling per operator. | Boundary fixtures produce documented errors or results; implicit lossy conversion does not occur.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Boundary fixtures produce documented errors or results; implicit lossy conversion does not occur
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-CON-009 [P2] PUR-CON-009: Use typed errors with safe messages and retry semantics; never return empty results to represent missing backends

- **Source:** `processing-units-requirements.md:140-140` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-CON-009 | Use typed errors with safe messages and retry semantics; never return empty results to represent missing backends. | Missing dependencies, model absence, bad shapes, denied access and genuine empty results are distinguishable.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Missing dependencies, model absence, bad shapes, denied access and genuine empty results are distinguishable
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-CPU-002 [P2] PUR-CPU-002: records.transform: declarative select/rename/filter/cast with an allowlisted expression AST, no eval; casts fail explicitly

- **Source:** `processing-units-requirements.md:296-296` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-CPU-002 | `records.transform`: declarative select/rename/filter/cast with an allowlisted expression AST, no eval; casts fail explicitly. | Golden records including nulls and invalid casts produce exact outputs and row-level provenance.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Golden records including nulls and invalid casts produce exact outputs and row-level provenance
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-CPU-003 [P2] PUR-CPU-003: records.aggregate: count/sum/min/max/mean grouped by declared fields; explicit missing/overflow and stable ordering

- **Source:** `processing-units-requirements.md:297-297` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-CPU-003 | `records.aggregate`: count/sum/min/max/mean grouped by declared fields; explicit missing/overflow and stable ordering. | Exact integer fixtures and tolerance-checked floating fixtures; bounded high-cardinality groups fail before exhaustion.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Exact integer fixtures and tolerance-checked floating fixtures; bounded high-cardinality groups fail before exhaustion
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-CPU-004 [P2] PUR-CPU-004: records.sortdeduplicate: stable key sort and exact-key deduplication with a declared first/last/error policy

- **Source:** `processing-units-requirements.md:298-298` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-CPU-004 | `records.sort_deduplicate`: stable key sort and exact-key deduplication with a declared first/last/error policy. | Same inputs yield same surviving source IDs; no approximate semantic merge.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Same inputs yield same surviving source IDs; no approximate semantic merge
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-DAT-004 [P2] PUR-DAT-004: Validate numeric shape/dtype before allocation; disallow object arrays and unsafe serialization

- **Source:** `processing-units-requirements.md:277-277` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-DAT-004 | Validate numeric shape/dtype before allocation; disallow object arrays and unsafe serialization. | Ragged, overflow, malformed compressed and huge declared-shape inputs fail safely.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Ragged, overflow, malformed compressed and huge declared-shape inputs fail safely
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-DAT-005 [P2] PUR-DAT-005: Partition caches by tenant, scope, data/policy/model/operator version and precision; invalidate on revocation

- **Source:** `processing-units-requirements.md:278-278` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-DAT-005 | Partition caches by tenant, scope, data/policy/model/operator version and precision; invalidate on revocation. | Identical text in two tenants does not share confidential KV/result caches or access grants.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Identical text in two tenants does not share confidential KV/result caches or access grants
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-DAT-007 [P2] PUR-DAT-007: Distinguish observed facts, calculated features, OCR text, model predictions and simulations in provenance

- **Source:** `processing-units-requirements.md:280-280` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-DAT-007 | Distinguish observed facts, calculated features, OCR text, model predictions and simulations in provenance. | Neither a high similarity score nor a model's confidence silently changes a graph claim into verified fact.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Neither a high similarity score nor a model's confidence silently changes a graph claim into verified fact
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-DPU-005 [P2] PUR-DPU-005: data.ingestionenvelope: produce typed source-event/provenance handoff with quality/rejection counts; publication uses existing ingestion owner

- **Source:** `processing-units-requirements.md:339-339` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-DPU-005 | `data.ingestion_envelope`: produce typed source-event/provenance handoff with quality/rejection counts; publication uses existing ingestion owner. | Source counts reconcile to accepted/rejected/duplicate records and graph results through the real ingestion path.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Source counts reconcile to accepted/rejected/duplicate records and graph results through the real ingestion path
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/data_prep.py:174`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/data_prep.py#L174-L174)
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-FND-002 [P2] PUR-FND-002: Use one shared processing domain, operator catalog and adapter protocol

- **Source:** `processing-units-requirements.md:101-101` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-FND-002 | Use one shared processing domain, operator catalog and adapter protocol. | A tensor operation invoked through two applicable profiles uses the same versioned implementation and produces equivalent outputs.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] A tensor operation invoked through two applicable profiles uses the same versioned implementation and produces equivalent outputs
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-FND-003 [P2] PUR-FND-003: Core graph/query startup must not import or require optional compute libraries

- **Source:** `processing-units-requirements.md:102-102` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-FND-003 | Core graph/query startup must not import or require optional compute libraries. | A clean core-only environment starts and performs a real graph read while all optional packages are absent.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] A clean core-only environment starts and performs a real graph read while all optional packages are absent
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

