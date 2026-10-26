# EPIC-ASPEII-NOTEST: EOIP-engg-doc-pkg/aspeii-reqirements.md · code_no_test

*Code references the ID but no test is mapped.* 2 tasks, ~6.0 h, priorities {'P0': 2}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-ASPEII-RQ-001 [P0] ASPEII-RQ-001: Baseline, Scope, and Decision Ledger

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:188-200` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-001: Baseline, Scope, and Decision Ledger

Priority P0. Dependencies: none.

1. Capture current commit, dirty-file hashes, runtime entrypoints, supported configurations, actual registered routes, and feature flags before implementation.
2. Reproduce AS-G01, AS-G02, and AS-G03 safely and preserve raw outputs; inventory other research gaps as source observations pending verification.
3. Create a clause registry containing every normative requirement, shared-contract allocation, scenario mapping, owner, dependency, status, and missing evidence.
4. Record each changed design default, rejected alternative, migration implication, and acceptance revision in a decision ledger.
5. Preserve concurrent user changes and existing requirement identities; reconcile overlapping CTAR, CRAr, Graph Neurons, and GUI contracts explicitly.
6. Report unsupported integrations and unresolved customer configuration as BLOCKED scoped items; never invent credentials, authorities, licenses, or passing results.

Acceptance: a clean checkout and a dirty checkout produce distinguishable manifests; deletion of one clause or an unknown requirement reference fails registry validation.
```
</details>

**Next steps**
1. Read the referenced code: packages/eoip/aspeii/admission.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('ASPEII-RQ-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-ASPEII-RQ-001

**Acceptance criteria**
- [ ] a clean checkout and a dirty checkout produce distinguishable manifests; deletion of one clause or an unknown requirement reference fails registry validation
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/aspeii/admission.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/aspeii/admission.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ASPEII-RQ-021 [P0] ASPEII-RQ-021: Execution Gateway and Reconciliation

- **Source:** `EOIP-engg-doc-pkg/aspeii-reqirements.md:448-460` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 1 other site(s): see duplicate task DUP-ASPEII-RQ-021; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### ASPEII-RQ-021: Execution Gateway and Reconciliation

Priority P0. Dependencies: 003, 009, 020.

1. Route all consequential paths through one gateway, including API, workers, MCP, retries, scheduled loops, legacy tools, and ontology publication.
2. Enforce certificate freshness, action digest, worker fence, current grants, and risk-specific dispatch conditions at the last controllable boundary.
3. Use provider idempotency and conditional updates where supported; persist attempt state before dispatch and observed external IDs afterward.
4. On uncertain external result, enter UNKNOWN_OUTCOME, reconcile through an independent read/status endpoint, and forbid blind resubmission.
5. Verify postconditions independently before declaring success; distinguish accepted, dispatched, observed effect, and verified outcome.
6. Implement rollback/compensation only for qualified effects; compensation is a new governed action and cannot erase an external effect's history.

Acceptance: timeout after remote commit does not duplicate a write; HTTP 200 with unmet postcondition is not SUCCEEDED; restart resumes reconciliation.
```
</details>

**Next steps**
1. Read the referenced code: packages/eoip/aspeii/dispatcher.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('ASPEII-RQ-021') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-ASPEII-RQ-021

**Acceptance criteria**
- [ ] timeout after remote commit does not duplicate a write; HTTP 200 with unmet postcondition is not SUCCEEDED; restart resumes reconciliation
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/aspeii/dispatcher.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/aspeii/dispatcher.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

