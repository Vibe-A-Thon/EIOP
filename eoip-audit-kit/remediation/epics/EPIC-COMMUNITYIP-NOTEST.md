# EPIC-COMMUNITYIP-NOTEST: EOIP-engg-doc-pkg/community-ip-requirements.md · code_no_test

*Code references the ID but no test is mapped.* 1 tasks, ~3.0 h, priorities {'P1': 1}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-CIP-RQ-030 [P1] CIP-RQ-030: Traceability and Release Gate

- **Source:** `EOIP-engg-doc-pkg/community-ip-requirements.md:314-321` (heading) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 1 other site(s): see duplicate task DUP-CIP-RQ-030; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### CIP-RQ-030: Traceability and Release Gate

Map every requirement/acceptance clause to executable scenario, observable, receipt and accountable package. Verifier rejects duplicate/missing IDs/clauses, absent JUnit cases, failed/skipped/blocked results, stale source hashes, benchmark mismatch, absent integration, and wrong scenario counts. A marker, test file, generated receipt or checkbox is not proof absent successful execution and revision/environment binding.

Report `NOT_RUN`, `FAIL`, `BLOCKED`, `PASS_WITH_EVIDENCE`. Engineering completion is 100% only when all mandatory clauses pass; release readiness is separate. Denominator changes require versioned owner approval and history.

**Acceptance:** `AC-030.1` verifier mutation tests remove requirement, clause, JUnit case, integration receipt, source hash, or benchmark case and prove 100% is denied. `AC-030.2` unit-only success never closes the feature; engineering, evidence, and release states remain separate.
```
</details>

**Next steps**
1. Read the referenced code: programme_rules.js:228
2. Write one test per acceptance criterion; mark with @pytest.mark.req('CIP-RQ-030') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-CIP-RQ-030

**Acceptance criteria**
- [ ] AC-030.1 verifier mutation tests remove requirement, clause, JUnit case, integration receipt, source hash, or benchmark case and prove 100% is denied. AC-030.2 unit-only success never closes the feature; engineering, evidence, and release states remain separate.
- [ ] AC-030.1 verifier mutation tests remove requirement, clause, JUnit case, integration receipt, source hash, or benchmark case and prove 100% is denied. AC-030.2 unit-only success never closes the feature; engineering, evidence, and release states remain separate
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`programme_rules.js:228`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/programme_rules.js#L228-L228)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

