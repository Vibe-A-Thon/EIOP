# EPIC-ASPEII-CI: EOIP-engg-doc-pkg/aspeii-reqirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 4 tasks, ~7.2 h, priorities {'P0': 4}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-ASPEII-RQ-018 [P0] ASPEII-RQ-018: Canonical Action Identity

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:409-421` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Partially Implemented / L2 (tests passed 20, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-018; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-018: Canonical Action Identity

Priority P0. Dependencies: 002, 012.

1. Implement the complete canonical projection and digest rules in section 3.5 using a qualified canonical JSON implementation.
2. Bind resolved identity, account, destination, arguments, tool/adapter/policy versions, obligations, pre-state, grant, and expiry.
3. Test cross-language equivalence, nested-key ordering, Unicode, null/absent distinctions, exact numeric bounds, arrays, and invalid JSON values.
4. Create a new digest for any material change; do not reuse approvals across wrappers, retries with changed effects, or normalized arguments unless equivalence is proven by the contract.
5. Store immutable canonical payloads behind authorized reads and display their digest in review/audit details.
6. Reject unknown canonicalization versions and parsing discrepancies; never fall back to unstable string representations.

Acceptance: changing account, tenant, nested argument, or destination changes identity; reordering JSON object keys alone does not; array order remains significant.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-ASPEII-RQ-018

**Acceptance criteria**
- [ ] changing account, tenant, nested argument, or destination changes identity; reordering JSON object keys alone does not; array order remains significant
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_aspeii_action.py:66`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-ASPEII-RQ-019 [P0] ASPEII-RQ-019: Independent Obligation Checker

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:422-434` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 20, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-019; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-019: Independent Obligation Checker

Priority P0. Dependencies: 004, 012, 014, 015, 018.

1. Derive obligations from trusted tool contracts and current policy, never from the planner's requested subset.
2. Check each required predicate against current scoped evidence and pre-state using a registered versioned verifier.
3. Return per-obligation PASS/FAIL/UNKNOWN plus evidence, rule, boundary, and reason; unknown mandatory predicates deny.
4. Keep the checker independent of planner generation and prevent it from modifying source facts, policy, or evaluation expectations.
5. Explicitly model the trusted base, including adapters, clocks, identity, state reads, verifier code, and key material; publish limitations in qualification records.
6. Support optional formal checker plugins only with bounded proof language, trusted-axiom manifest, timeout and independent proof replay; unsupported proofs remain unusable.

Acceptance: omitted precondition, contradictory premises, risk downgrade, stale state, or forged verifier output prevents the actual adapter call, regardless of persuasive model text.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-ASPEII-RQ-019

**Acceptance criteria**
- [ ] omitted precondition, contradictory premises, risk downgrade, stale state, or forged verifier output prevents the actual adapter call, regardless of persuasive model text
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_aspeii_action.py:137`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-ASPEII-RQ-020 [P0] ASPEII-RQ-020: Approval Binding and Admission

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:435-447` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Partially Implemented / L2 (tests passed 20, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-020; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-020: Approval Binding and Admission

Priority P0. Dependencies: 003, 004, 018, 019.

1. Record review decisions bound to the exact action digest, approver identity/permission, policy revision, expiry, and separation-of-duties result.
2. Resolve approval IDs server-side and reject nonexistent, cross-tenant, expired, revoked, already-consumed, or mismatched decisions.
3. Atomically reserve admission for a logical effect and issue a certificate only after all required obligations and approvals pass.
4. Distinguish human approval from scoped standing policy authority; show the actual authority in receipts and UI.
5. Recheck state and authority immediately before dispatch; changed preconditions require renewed checking and, where action identity changes, new approval.
6. Reject observer-only approval-required execution and preserve all denials/expirations as auditable outcomes.

Acceptance: `approval_id='nonexistent-approval'` cannot trigger even an in-memory effect handler; one genuine approval cannot authorize a second logical action.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-ASPEII-RQ-020

**Acceptance criteria**
- [ ] approvalid='nonexistent-approval' cannot trigger even an in-memory effect handler; one genuine approval cannot authorize a second logical action
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_aspeii_action.py:174`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-ASPEII-RQ-022 [P0] ASPEII-RQ-022: Integrity, Receipts, and Offline Verification

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:461-473` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Partially Implemented / L2 (tests passed 25, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-022; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 2.2 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-022: Integrity, Receipts, and Offline Verification

Priority P0. Dependencies: 003, 018, 020, 021.

1. Persist certificates, approvals, attempts, denial outcomes, and closure receipts with complete digest bindings and ordered audit events.
2. Use managed or protected private keys, key IDs, rotation/revocation, signed checkpoints, and authenticated export manifests; no default production signing secret.
3. Provide offline verification of payload hashes, signatures, chain continuity, schema versions, and record bindings with a supplied trusted-key set.
4. Label integrity/authenticity/authorization/obligation/outcome results separately; verification of one must not imply the others.
5. Detect deletion, truncation, reordering, replacement, and stale checkpoint attacks to the declared assurance level; a local hash chain alone cannot detect total-history replacement without a trusted anchor.
6. Export privacy-filtered bundles with redaction manifests and access checks; missing protected payload may produce LIMITED_VERIFICATION, never fabricated full verification.

Acceptance: modify an action, outcome, metadata field, or predecessor link and verification fails; a valid signature on an unsupported claim does not pass factual checking.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-ASPEII-RQ-022

**Acceptance criteria**
- [ ] Priority P0. Dependencies: 003, 018, 020, 021
- [ ] Persist certificates, approvals, attempts, denial outcomes, and closure receipts with complete digest bindings and ordered audit events
- [ ] Use managed or protected private keys, key IDs, rotation/revocation, signed checkpoints, and authenticated export manifests; no default production signing secret
- [ ] Provide offline verification of payload hashes, signatures, chain continuity, schema versions, and record bindings with a supplied trusted-key set
- [ ] Label integrity/authenticity/authorization/obligation/outcome results separately; verification of one must not imply the others
- [ ] Detect deletion, truncation, reordering, replacement, and stale checkpoint attacks to the declared assurance level; a local hash chain alone cannot detect total-history replacement without a trusted anchor
- [ ] Export privacy-filtered bundles with redaction manifests and access checks; missing protected payload may produce LIMITEDVERIFICATION, never fabricated full verification
- [ ] modify an action, outcome, metadata field, or predecessor link and verification fails; a valid signature on an unsupported claim does not pass factual checking
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_aspeii_action.py:137`, `tests/unit/test_aspeii_receipts.py:77`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

