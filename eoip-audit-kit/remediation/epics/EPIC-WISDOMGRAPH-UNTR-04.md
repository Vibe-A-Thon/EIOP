# EPIC-WISDOMGRAPH-UNTR-04: wisdom-graph-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 52 tasks, ~314.5 h, priorities {'P2': 52}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-WG-PLT-005 [P2] WG-PLT-005: No tenant data is sent to an external model endpoint unless the tenant's data-sharing policy explicitly permits that data class for that endpoint (REQ-PLT-005). All Wisdom models default to local mode

- **Source:** `wisdom-graph-requirements.md:172-172` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-PLT-005 | No tenant data is sent to an external model endpoint unless the tenant's data-sharing policy explicitly permits that data class for that endpoint (`REQ-PLT-005`). All Wisdom models default to local models through `ModelPort`. Decision rationales and transcripts are classified at least `internal`; off-system transcripts are `confidential` by default.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-PLT-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-PLT-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-PLT-005 | No tenant data is sent to an external model endpoint unless the tenant's data-sharing policy explicitly permits that data class for that endpoint (REQ-PLT-005). All Wisdom models default to local models through ModelPort. Decision rationales and transcripts are classified at least internal; off-system transcripts are confidential by default.»
- [ ] No tenant data is sent to an external model endpoint unless the tenant's data-sharing policy explicitly permits that data class for that endpoint (REQ-PLT-005). All Wisdom models default to local models through ModelPort. Decision rationales and transcripts are classified at least internal; off-system transcripts are confidential by default.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-PLT-008 [P2] WG-PLT-008: All timestamps are UTC ISO-8601 with milliseconds. All ids are UUIDv7 unless stated otherwise

- **Source:** `wisdom-graph-requirements.md:175-175` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-PLT-008 | All timestamps are UTC ISO-8601 with milliseconds. All ids are UUIDv7 unless stated otherwise.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-PLT-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-PLT-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-PLT-008 | All timestamps are UTC ISO-8601 with milliseconds. All ids are UUIDv7 unless stated otherwise.»
- [ ] All timestamps are UTC ISO-8601 with milliseconds. All ids are UUIDv7 unless stated otherwise.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-PLT-012 [P2] WG-PLT-012: Counsel can only add caution. No Wisdom output may convert a BLOCK or ESCALATE from any existing checkpoint, budget, lease, derivation guard or approval into ALLOW (see WG-CNS-006)

- **Source:** `wisdom-graph-requirements.md:179-179` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-PLT-012 | Counsel can only add caution. No Wisdom output may convert a `BLOCK` or `ESCALATE` from any existing checkpoint, budget, lease, derivation guard or approval into `ALLOW` (see WG-CNS-006).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-PLT-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-PLT-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-PLT-012 | Counsel can only add caution. No Wisdom output may convert a BLOCK or ESCALATE from any existing checkpoint, budget, lease, derivation guard or approval into ALLOW (see WG-CNS-006).»
- [ ] Counsel can only add caution. No Wisdom output may convert a BLOCK or ESCALATE from any existing checkpoint, budget, lease, derivation guard or approval into ALLOW (see WG-CNS-006).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-POL-002 [P2] WG-POL-002: An exception is a first-class record linked to the decision, the policy version and its justification warrant. An exception without a justification warrant is rejected (WSDEXCEPTIONUNJUSTIFIED)

- **Source:** `wisdom-graph-requirements.md:751-751` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-POL-002 | An exception is a first-class record linked to the decision, the policy version and its justification warrant. An exception without a justification warrant is rejected (`WSD_EXCEPTION_UNJUSTIFIED`).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-POL-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-POL-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-POL-002 | An exception is a first-class record linked to the decision, the policy version and its justification warrant. An exception without a justification warrant is rejected (WSD_EXCEPTION_UNJUSTIFIED).»
- [ ] An exception is a first-class record linked to the decision, the policy version and its justification warrant. An exception without a justification warrant is rejected (WSD_EXCEPTION_UNJUSTIFIED).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-POL-003 [P2] WG-POL-003: Exception routing: when a checkpoint finds that a planned action fails a policy that permits exceptions, counsel includes the exception precedents for that policy (WG-PRE-007) and the approver role co

- **Source:** `wisdom-graph-requirements.md:752-752` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-POL-003 | Exception routing: when a checkpoint finds that a planned action fails a policy that permits exceptions, counsel includes the exception precedents for that policy (WG-PRE-007) and the approver role configured for the policy (`policy.exception_approver_role`); the escalation created by the existing flow is addressed to that role.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-POL-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-POL-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-POL-003 | Exception routing: when a checkpoint finds that a planned action fails a policy that permits exceptions, counsel includes the exception precedents for that policy (WG-PRE-007) and the approver role configured for the policy (policy.exception_approver_role); the escalation created by the existing flow is addressed to that role.»
- [ ] Exception routing: when a checkpoint finds that a planned action fails a policy that permits exceptions, counsel includes the exception precedents for that policy (WG-PRE-007) and the approver role configured for the policy (policy.exception_approver_role); the escalation created by the existing flow is addressed to that role.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-POL-006 [P2] WG-POL-006: Conflict resolution records: when two policies or two definitions conflicted for a decision, the trace stores which prevailed and why (policies[].result = OVERRIDDENBY:<policyid> with a rationale warr

- **Source:** `wisdom-graph-requirements.md:755-755` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-POL-006 | Conflict resolution records: when two policies or two definitions conflicted for a decision, the trace stores which prevailed and why (`policies[].result = OVERRIDDEN_BY:<policy_id>` with a rationale warrant), so precedent searches can find how a conflict was resolved before.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-POL-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-POL-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-POL-006 | Conflict resolution records: when two policies or two definitions conflicted for a decision, the trace stores which prevailed and why (policies[].result = OVERRIDDEN_BY:<policy_id> with a rationale warrant), so precedent searches can find how a conflict was resolved before.»
- [ ] Conflict resolution records: when two policies or two definitions conflicted for a decision, the trace stores which prevailed and why (policies[].result = OVERRIDDEN_BY:<policy_id> with a rationale warrant), so precedent searches can find how a conflict was resolved before.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-POL-007 [P2] WG-POL-007: Acceptance on the seeded tenant: the planted recurring exception (plan §4.3, "renewal discount above cap when an open sev-1 incident exists") produces exactly one amendment proposal with the correct c

- **Source:** `wisdom-graph-requirements.md:756-756` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-WG-POL-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-POL-007 | Acceptance on the seeded tenant: the planted recurring exception (plan §4.3, "renewal discount above cap when an open sev-1 incident exists") produces exactly one amendment proposal with the correct condition; the planted random exceptions produce none.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-POL-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-POL-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-WG-POL-007

**Acceptance criteria**
- [ ] on the seeded tenant: the planted recurring exception (plan §4.3, "renewal discount above cap when an open sev-1 incident exists") produces exactly one amendment proposal with the correct condition; the planted random exceptions produce none
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-PRC-001 [P2] WG-PRC-001: Lesson Review · Weekly (wisdom.lesson_review_cron) · Queue of CANDIDATE, STALE, LESSON_CONFLICT lessons with statistics, supporting/contradicting decisions, proposed exclusions; approve/reject/depreca

- **Source:** `wisdom-graph-requirements.md:1037-1037` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-PRC-001 | Lesson Review | Weekly (`wisdom.lesson_review_cron`) | Queue of `CANDIDATE`, `STALE`, `LESSON_CONFLICT` lessons with statistics, supporting/contradicting decisions, proposed exclusions; approve/reject/deprecate with reason; sign-off
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-PRC-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-PRC-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-PRC-001 | Lesson Review | Weekly (wisdom.lesson_review_cron) | Queue of CANDIDATE, STALE, LESSON_CONFLICT lessons with statistics, supporting/contradicting decisions, proposed exclusions; approve/reject/deprecate with reason; sign-off»
- [ ] Queue of CANDIDATE, STALE, LESSON_CONFLICT lessons with statistics, supporting/contradicting decisions, proposed exclusions; approve/reject/deprecate with reason; sign-off
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-PRC-002 [P2] WG-PRC-002: Precedent Quality Review · Monthly · Sample of 50 counsel events with the precedents shown; reviewer marks relevant/irrelevant (labels feed evals/wisdom/precedent-v1 refresh); trace conflicts; sign-of

- **Source:** `wisdom-graph-requirements.md:1038-1038` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-PRC-002 | Precedent Quality Review | Monthly | Sample of 50 counsel events with the precedents shown; reviewer marks relevant/irrelevant (labels feed `evals/wisdom/precedent-v1` refresh); trace conflicts; sign-off
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-PRC-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-PRC-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-PRC-002 | Precedent Quality Review | Monthly | Sample of 50 counsel events with the precedents shown; reviewer marks relevant/irrelevant (labels feed evals/wisdom/precedent-v1 refresh); trace conflicts; sign-off»
- [ ] Sample of 50 counsel events with the precedents shown; reviewer marks relevant/irrelevant (labels feed evals/wisdom/precedent-v1 refresh); trace conflicts; sign-off
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-PRC-003 [P2] WG-PRC-003: Exception-to-Policy Review · Monthly · Policy amendment proposals (W10), exception patterns, approver concentration; decide; sign-off

- **Source:** `wisdom-graph-requirements.md:1039-1039` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-PRC-003 | Exception-to-Policy Review | Monthly | Policy amendment proposals (W10), exception patterns, approver concentration; decide; sign-off
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-PRC-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-PRC-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-PRC-003 | Exception-to-Policy Review | Monthly | Policy amendment proposals (W10), exception patterns, approver concentration; decide; sign-off»
- [ ] Policy amendment proposals (W10), exception patterns, approver concentration; decide; sign-off
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-PRC-004 [P2] WG-PRC-004: Values and Trade-off Review · Quarterly · Value registry diff, value-conflict counsel counts, value outcome shares; re-approve; sign-off

- **Source:** `wisdom-graph-requirements.md:1040-1040` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-PRC-004 | Values and Trade-off Review | Quarterly | Value registry diff, value-conflict counsel counts, value outcome shares; re-approve; sign-off
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-PRC-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-PRC-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-PRC-004 | Values and Trade-off Review | Quarterly | Value registry diff, value-conflict counsel counts, value outcome shares; re-approve; sign-off»
- [ ] Values and Trade-off Review
- [ ] Value registry diff, value-conflict counsel counts, value outcome shares; re-approve; sign-off
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-PRE-002 [P2] WG-PRE-002: POST /wisdom/precedents/search with exactly one of situation, decisionid or freetext, plus optional decisiontype, k and filters{from, to, outcome, actor, policyid, exceptiononly}, returns ranked prece

- **Source:** `wisdom-graph-requirements.md:618-618` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-PRE-002 | `POST /wisdom/precedents/search` with exactly one of `situation`, `decision_id` or `free_text`, plus optional `decision_type`, `k` and `filters{from, to, outcome, actor, policy_id, exception_only}`, returns ranked precedents with scores, outcomes, why_similar, and `novelty`; or `NO_PRECEDENT`. Free text is converted to a situation by the Ask Wisdom parser (§21) and labelled `situation_source = TEXT`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-PRE-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-PRE-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-PRE-002 | POST /wisdom/precedents/search with exactly one of situation, decision_id or free_text, plus optional decision_type, k and filters{from, to, outcome, actor, policy_id, exception_only}, returns ranked precedents with scores, outcomes, why_similar, and novelty; or NO_PRECEDENT. Free text is converted to a situation by the Ask Wisdom parser (§21) and labelled situatio»
- [ ] POST /wisdom/precedents/search with exactly one of situation, decision_id or free_text, plus optional decision_type, k and filters{from, to, outcome, actor, policy_id, exception_only}, returns ranked precedents with scores, outcomes, why_similar, and novelty; or NO_PRECEDENT. Free text is converted to a situation by the Ask Wisdom parser (§21) and labelled situation_source = TEXT.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-PRE-004 [P2] WG-PRE-004: Cited precedent: when a decision-maker cites a precedent (UI action or SDK citeprecedent(decisionid)), a CITEDPRECEDENT edge is stored; computed links are stored as PRECEDENTFOR with score and run id.

- **Source:** `wisdom-graph-requirements.md:620-620` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-PRE-004 | Cited precedent: when a decision-maker cites a precedent (UI action or SDK `cite_precedent(decision_id)`), a `CITED_PRECEDENT` edge is stored; computed links are stored as `PRECEDENT_FOR` with score and run id. Both are visible in the trace.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-PRE-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-PRE-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-PRE-004 | Cited precedent: when a decision-maker cites a precedent (UI action or SDK cite_precedent(decision_id)), a CITED_PRECEDENT edge is stored; computed links are stored as PRECEDENT_FOR with score and run id. Both are visible in the trace.»
- [ ] Cited precedent: when a decision-maker cites a precedent (UI action or SDK cite_precedent(decision_id)), a CITED_PRECEDENT edge is stored; computed links are stored as PRECEDENT_FOR with score and run id. Both are visible in the trace.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-PRE-005 [P2] WG-PRE-005: Decision communities: nightly Louvain over the graph of PRECEDENTFOR (score ≥ 0.6), CITEDPRECEDENT, CAUSED and INFLUENCED edges, per tenant and decision domain; DecisionCommunity nodes with MEMBEROF e

- **Source:** `wisdom-graph-requirements.md:621-621` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-PRE-005 | Decision communities: nightly Louvain over the graph of `PRECEDENT_FOR` (score ≥ 0.6), `CITED_PRECEDENT`, `CAUSED` and `INFLUENCED` edges, per tenant and decision domain; `DecisionCommunity` nodes with `MEMBER_OF` edges; community ids stable across runs by maximum-overlap matching. `GET /wisdom/communities` and `/wisdom/communities/{id}`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-PRE-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-PRE-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-PRE-005 | Decision communities: nightly Louvain over the graph of PRECEDENT_FOR (score ≥ 0.6), CITED_PRECEDENT, CAUSED and INFLUENCED edges, per tenant and decision domain; DecisionCommunity nodes with MEMBER_OF edges; community ids stable across runs by maximum-overlap matching. GET /wisdom/communities and /wisdom/communities/{id}.»
- [ ] Decision communities: nightly Louvain over the graph of PRECEDENT_FOR (score ≥ 0.6), CITED_PRECEDENT, CAUSED and INFLUENCED edges, per tenant and decision domain; DecisionCommunity nodes with MEMBER_OF edges; community ids stable across runs by maximum-overlap matching. GET /wisdom/communities and /wisdom/communities/{id}.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-PRE-006 [P2] WG-PRE-006: Decision-to-decision causal chains: CAUSED edges are created when decision B's read set includes an assertion written by decision A's action within wisdom.causalchainwindow (default 30 days); INFLUENC

- **Source:** `wisdom-graph-requirements.md:622-622` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-PRE-006 | Decision-to-decision causal chains: `CAUSED` edges are created when decision B's read set includes an assertion written by decision A's action within `wisdom.causal_chain_window` (default 30 days); `INFLUENCED` when B cited A or A was a precedent shown to B. `GET /wisdom/decisions/{id}/chain?direction=up` (or `down`) `&depth=N` (N ≤ 10) returns the chain.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-PRE-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-PRE-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-PRE-006 | Decision-to-decision causal chains: CAUSED edges are created when decision B's read set includes an assertion written by decision A's action within wisdom.causal_chain_window (default 30 days); INFLUENCED when B cited A or A was a precedent shown to B. GET /wisdom/decisions/{id}/chain?direction=up (or down) &depth=N (N ≤ 10) returns the chain.»
- [ ] Decision-to-decision causal chains: CAUSED edges are created when decision B's read set includes an assertion written by decision A's action within wisdom.causal_chain_window (default 30 days); INFLUENCED when B cited A or A was a precedent shown to B. GET /wisdom/decisions/{id}/chain?direction=up (or down) &depth=N (N ≤ 10) returns the chain.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-PRE-007 [P2] WG-PRE-007: Exception precedent: filters.exceptiononly = true returns only decisions that granted an exception to the given policy, with approver and justification, so "how were exceptions to policy X granted bef

- **Source:** `wisdom-graph-requirements.md:623-623` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-PRE-007 | Exception precedent: `filters.exception_only = true` returns only decisions that granted an exception to the given policy, with approver and justification, so "how were exceptions to policy X granted before" is answerable in one call.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-PRE-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-PRE-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-PRE-007 | Exception precedent: filters.exception_only = true returns only decisions that granted an exception to the given policy, with approver and justification, so "how were exceptions to policy X granted before" is answerable in one call.»
- [ ] Exception precedent: filters.exception_only = true returns only decisions that granted an exception to the given policy, with approver and justification, so "how were exceptions to policy X granted before" is answerable in one call.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-PRE-008 [P2] WG-PRE-008: Benchmark evals/wisdom/precedent-v1: ≥ 200 query situations on the seeded tenant with steward-labelled relevant precedents. Acceptance: nDCG@10 ≥ 0.75, recall@10 ≥ 0.85, and the planted failed precede

- **Source:** `wisdom-graph-requirements.md:624-624` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-WG-PRE-008; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-PRE-008 | Benchmark `evals/wisdom/precedent-v1`: ≥ 200 query situations on the seeded tenant with steward-labelled relevant precedents. Acceptance: nDCG@10 ≥ 0.75, recall@10 ≥ 0.85, and the planted failed precedent appears in the top 10 for ≥ 90% of queries that have one. Report each similarity component's ablation.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-PRE-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-PRE-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-WG-PRE-008

**Acceptance criteria**
- [ ] nDCG@10 ≥ 0.75, recall@10 ≥ 0.85, and the planted failed precedent appears in the top 10 for ≥ 90% of queries that have one. Report each similarity component's ablation
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-PRE-009 [P2] WG-PRE-009: Performance: precedent search p95 < 500 ms at 1,000,000 decisions per tenant on the reference hardware; fingerprint computation p95 < 100 ms per decision

- **Source:** `wisdom-graph-requirements.md:625-625` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-PRE-009 | Performance: precedent search p95 < 500 ms at 1,000,000 decisions per tenant on the reference hardware; fingerprint computation p95 < 100 ms per decision.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-PRE-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-PRE-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-PRE-009 | Performance: precedent search p95 < 500 ms at 1,000,000 decisions per tenant on the reference hardware; fingerprint computation p95 < 100 ms per decision.»
- [ ] Performance: precedent search p95 < 500 ms at 1,000,000 decisions per tenant on the reference hardware; fingerprint computation p95 < 100 ms per decision.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-PRE-010 [P2] WG-PRE-010: Precedent results carry a warrant composed by A1 with operator wg.precedent.v1 (class COMPUTATION); the "similar" claim is a computation, and the precedent's outcome keeps its own status

- **Source:** `wisdom-graph-requirements.md:626-626` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-PRE-010 | Precedent results carry a warrant composed by A1 with operator `wg.precedent.v1` (class COMPUTATION); the "similar" claim is a computation, and the precedent's outcome keeps its own status.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-PRE-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-PRE-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-PRE-010 | Precedent results carry a warrant composed by A1 with operator wg.precedent.v1 (class COMPUTATION); the "similar" claim is a computation, and the precedent's outcome keeps its own status.»
- [ ] Precedent results carry a warrant composed by A1 with operator wg.precedent.v1 (class COMPUTATION); the "similar" claim is a computation, and the precedent's outcome keeps its own status.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-TLS-002 [P2] WG-TLS-002: The MCP wrapper (REQ-SDK-004) exposes the read tools above as MCP tools with warrants on every result. recorddecision and recordoutcome are write tools that run the commit checkpoint and require warra

- **Source:** `wisdom-graph-requirements.md:984-984` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-WG-TLS-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-TLS-002 | The MCP wrapper (`REQ-SDK-004`) exposes the read tools above as MCP tools with warrants on every result. `record_decision` and `record_outcome` are write tools that run the commit checkpoint and require warrants. No MCP tool can approve a lesson, change a value, accept a policy proposal or acknowledge counsel on behalf of a person.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-TLS-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-TLS-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-WG-TLS-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-TLS-002 | The MCP wrapper (REQ-SDK-004) exposes the read tools above as MCP tools with warrants on every result. record_decision and record_outcome are write tools that run the commit checkpoint and require warrants. No MCP tool can approve a lesson, change a value, accept a policy proposal or acknowledge counsel on behalf of a person.»
- [ ] The MCP wrapper (REQ-SDK-004) exposes the read tools above as MCP tools with warrants on every result. record_decision and record_outcome are write tools that run the commit checkpoint and require warrants. No MCP tool can approve a lesson, change a value, accept a policy proposal or acknowledge counsel on behalf of a person.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-TLS-003 [P2] WG-TLS-003: Tool schemas are generated from the OpenAPI definitions (§27.7) and validated in a contract test against a real MCP session (stdio and HTTP)

- **Source:** `wisdom-graph-requirements.md:985-985` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-TLS-003 | Tool schemas are generated from the OpenAPI definitions (§27.7) and validated in a contract test against a real MCP session (stdio and HTTP).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-TLS-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-TLS-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-TLS-003 | Tool schemas are generated from the OpenAPI definitions (§27.7) and validated in a contract test against a real MCP session (stdio and HTTP).»
- [ ] Tool schemas are generated from the OpenAPI definitions (§27.7) and validated in a contract test against a real MCP session (stdio and HTTP).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-TLS-005 [P2] WG-TLS-005: KGF's own agents call getcounsel implicitly through the checkpoint (WG-CNS-001); explicit calls are for planning before a plan exists

- **Source:** `wisdom-graph-requirements.md:987-987` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-TLS-005 | KGF's own agents call `get_counsel` implicitly through the checkpoint (WG-CNS-001); explicit calls are for planning before a plan exists.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-TLS-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-TLS-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-TLS-005 | KGF's own agents call get_counsel implicitly through the checkpoint (WG-CNS-001); explicit calls are for planning before a plan exists.»
- [ ] KGF's own agents call get_counsel implicitly through the checkpoint (WG-CNS-001); explicit calls are for planning before a plan exists.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-TLS-006 [P2] WG-TLS-006: Demonstration: an external MCP client asks for precedents for a discount decision, receives them with warrants, records a decision with a rationale, and later records an attested outcome; the trace, o

- **Source:** `wisdom-graph-requirements.md:988-988` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-TLS-006 | Demonstration: an external MCP client asks for precedents for a discount decision, receives them with warrants, records a decision with a rationale, and later records an attested outcome; the trace, outcome and lesson update are visible in the UI.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-TLS-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-TLS-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-TLS-006 | Demonstration: an external MCP client asks for precedents for a discount decision, receives them with warrants, records a decision with a rationale, and later records an attested outcome; the trace, outcome and lesson update are visible in the UI.»
- [ ] Demonstration: an external MCP client asks for precedents for a discount decision, receives them with warrants, records a decision with a rationale, and later records an attested outcome; the trace, outcome and lesson update are visible in the UI.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-UI-001 [P2] WG-UI-001: Decision Inbox · /wisdom/inbox · Off-system extractions pending verification with source span highlighted; confirm/edit/reject with reason; bulk actions limited to 20 items with per-item review

- **Source:** `wisdom-graph-requirements.md:1064-1064` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-UI-001 | Decision Inbox | `/wisdom/inbox` | Off-system extractions pending verification with source span highlighted; confirm/edit/reject with reason; bulk actions limited to 20 items with per-item review
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-UI-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-UI-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-UI-001 | Decision Inbox | /wisdom/inbox | Off-system extractions pending verification with source span highlighted; confirm/edit/reject with reason; bulk actions limited to 20 items with per-item review»
- [ ] Off-system extractions pending verification with source span highlighted; confirm/edit/reject with reason; bulk actions limited to 20 items with per-item review
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-UI-002 [P2] WG-UI-002: Decision view ("Why") · /wisdom/decisions/:id · Everything in WG-OBS-001; status labels by icon + text; replay and reconsider buttons with results; export/verify; audit tab

- **Source:** `wisdom-graph-requirements.md:1065-1065` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-UI-002 | Decision view ("Why") | `/wisdom/decisions/:id` | Everything in WG-OBS-001; status labels by icon + text; replay and reconsider buttons with results; export/verify; audit tab
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-UI-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-UI-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-UI-002 | Decision view ("Why") | /wisdom/decisions/:id | Everything in WG-OBS-001; status labels by icon + text; replay and reconsider buttons with results; export/verify; audit tab»
- [ ] Everything in WG-OBS-001; status labels by icon + text; replay and reconsider buttons with results; export/verify; audit tab
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-UI-003 [P2] WG-UI-003: Precedent Explorer · /wisdom/precedents · Search by situation, decision id or text; ranked results with outcome badges (success, failure, pending), why-similar chips, archetype grouping toggle, "no pr

- **Source:** `wisdom-graph-requirements.md:1066-1066` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-UI-003 | Precedent Explorer | `/wisdom/precedents` | Search by situation, decision id or text; ranked results with outcome badges (success, failure, pending), why-similar chips, archetype grouping toggle, "no precedent" state; exception-only filter
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-UI-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-UI-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-UI-003 | Precedent Explorer | /wisdom/precedents | Search by situation, decision id or text; ranked results with outcome badges (success, failure, pending), why-similar chips, archetype grouping toggle, "no precedent" state; exception-only filter»
- [ ] Search by situation, decision id or text; ranked results with outcome badges (success, failure, pending), why-similar chips, archetype grouping toggle, "no precedent" state; exception-only filter
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-UI-004 [P2] WG-UI-004: Counsel panel · inside plan/commit views, escalations, deliberations · Precedents, applicable/excluded/near-boundary lessons, values at stake, judge calibration, world-model predictions with abstentio

- **Source:** `wisdom-graph-requirements.md:1067-1067` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-UI-004 | Counsel panel | inside plan/commit views, escalations, deliberations | Precedents, applicable/excluded/near-boundary lessons, values at stake, judge calibration, world-model predictions with abstentions, effect and κ multiplier; acknowledge with note
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-UI-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-UI-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-UI-004 | Counsel panel | inside plan/commit views, escalations, deliberations | Precedents, applicable/excluded/near-boundary lessons, values at stake, judge calibration, world-model predictions with abstentions, effect and κ multiplier; acknowledge with note»
- [ ] inside plan/commit views, escalations, deliberations
- [ ] Precedents, applicable/excluded/near-boundary lessons, values at stake, judge calibration, world-model predictions with abstentions, effect and κ multiplier; acknowledge with note
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-UI-006 [P2] WG-UI-006: Outcomes · /wisdom/outcomes · Outcome specs (create/version/approve), outcome timeline per decision, attribution with confounding flags and steward override

- **Source:** `wisdom-graph-requirements.md:1069-1069` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-UI-006 | Outcomes | `/wisdom/outcomes` | Outcome specs (create/version/approve), outcome timeline per decision, attribution with confounding flags and steward override
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-UI-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-UI-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-UI-006 | Outcomes | /wisdom/outcomes | Outcome specs (create/version/approve), outcome timeline per decision, attribution with confounding flags and steward override»
- [ ] Outcome specs (create/version/approve), outcome timeline per decision, attribution with confounding flags and steward override
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-UI-007 [P2] WG-UI-007: Policies and Exceptions · /wisdom/policies · Policy versions, exception history with approvers and outcomes, amendment proposals and decisions

- **Source:** `wisdom-graph-requirements.md:1070-1070` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-UI-007 | Policies and Exceptions | `/wisdom/policies` | Policy versions, exception history with approvers and outcomes, amendment proposals and decisions
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-UI-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-UI-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-UI-007 | Policies and Exceptions | /wisdom/policies | Policy versions, exception history with approvers and outcomes, amendment proposals and decisions»
- [ ] Policy versions, exception history with approvers and outcomes, amendment proposals and decisions
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-UI-008 [P2] WG-UI-008: Values and Trade-offs · /wisdom/values · Value registry with canonical definitions, ranks by domain, trade-off rules with conditions, cycle validation errors, value outcome shares

- **Source:** `wisdom-graph-requirements.md:1071-1071` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-UI-008 | Values and Trade-offs | `/wisdom/values` | Value registry with canonical definitions, ranks by domain, trade-off rules with conditions, cycle validation errors, value outcome shares
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-UI-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-UI-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-UI-008 | Values and Trade-offs | /wisdom/values | Value registry with canonical definitions, ranks by domain, trade-off rules with conditions, cycle validation errors, value outcome shares»
- [ ] Value registry with canonical definitions, ranks by domain, trade-off rules with conditions, cycle validation errors, value outcome shares
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-UI-009 [P2] WG-UI-009: Calibration · /wisdom/calibration · Agent judges with reliability diagrams and Brier/ECE; person records only per WG-CAL-002 with the WG-SEC-004 notice

- **Source:** `wisdom-graph-requirements.md:1072-1072` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-UI-009 | Calibration | `/wisdom/calibration` | Agent judges with reliability diagrams and Brier/ECE; person records only per WG-CAL-002 with the WG-SEC-004 notice
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-UI-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-UI-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-UI-009 | Calibration | /wisdom/calibration | Agent judges with reliability diagrams and Brier/ECE; person records only per WG-CAL-002 with the WG-SEC-004 notice»
- [ ] Agent judges with reliability diagrams and Brier/ECE; person records only per WG-CAL-002 with the WG-SEC-004 notice
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-UI-010 [P2] WG-UI-010: What-if Studio · /wisdom/whatif · Pick situation or past decision and option; predicted success with calibration note, abstention state, shadow-branch diff, impact and κ; every number labelled predict

- **Source:** `wisdom-graph-requirements.md:1073-1073` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-UI-010 | What-if Studio | `/wisdom/whatif` | Pick situation or past decision and option; predicted success with calibration note, abstention state, shadow-branch diff, impact and κ; every number labelled predicted
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-UI-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-UI-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-UI-010 | What-if Studio | /wisdom/whatif | Pick situation or past decision and option; predicted success with calibration note, abstention state, shadow-branch diff, impact and κ; every number labelled predicted»
- [ ] Pick situation or past decision and option; predicted success with calibration note, abstention state, shadow-branch diff, impact and κ; every number labelled predicted
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-UI-011 [P2] WG-UI-011: Timeline · /wisdom/entities/:id/timeline · Event clock for an entity with decisions, checkpoint events, changes and outcomes in order; temporal-join filters; as-of view at any decision

- **Source:** `wisdom-graph-requirements.md:1074-1074` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-UI-011 | Timeline | `/wisdom/entities/:id/timeline` | Event clock for an entity with decisions, checkpoint events, changes and outcomes in order; temporal-join filters; as-of view at any decision
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-UI-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-UI-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-UI-011 | Timeline | /wisdom/entities/:id/timeline | Event clock for an entity with decisions, checkpoint events, changes and outcomes in order; temporal-join filters; as-of view at any decision»
- [ ] Event clock for an entity with decisions, checkpoint events, changes and outcomes in order; temporal-join filters; as-of view at any decision
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-UI-012 [P2] WG-UI-012: Emergence · /wisdom/emergence · Situation-kind, feature and unwritten-rule proposals with evidence; send to Ontology Advisor; decide

- **Source:** `wisdom-graph-requirements.md:1075-1075` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-UI-012 | Emergence | `/wisdom/emergence` | Situation-kind, feature and unwritten-rule proposals with evidence; send to Ontology Advisor; decide
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-UI-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-UI-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-UI-012 | Emergence | /wisdom/emergence | Situation-kind, feature and unwritten-rule proposals with evidence; send to Ontology Advisor; decide»
- [ ] Situation-kind, feature and unwritten-rule proposals with evidence; send to Ontology Advisor; decide
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-UI-013 [P2] WG-UI-013: Curator · /wisdom/curator · Critic runs with Q values and guarded metrics; archetypes; pruning reports; derived-layer rebuild status

- **Source:** `wisdom-graph-requirements.md:1076-1076` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-UI-013 | Curator | `/wisdom/curator` | Critic runs with Q values and guarded metrics; archetypes; pruning reports; derived-layer rebuild status
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-UI-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-UI-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-UI-013 | Curator | /wisdom/curator | Critic runs with Q values and guarded metrics; archetypes; pruning reports; derived-layer rebuild status»
- [ ] Critic runs with Q values and guarded metrics; archetypes; pruning reports; derived-layer rebuild status
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-UI-014 [P2] WG-UI-014: Wisdom Dashboard · /wisdom/metrics · Metrics of §23 over time, Wisdom Index with criteria, governance process status

- **Source:** `wisdom-graph-requirements.md:1077-1077` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-UI-014 | Wisdom Dashboard | `/wisdom/metrics` | Metrics of §23 over time, Wisdom Index with criteria, governance process status
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-UI-014' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-UI-014') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-UI-014 | Wisdom Dashboard | /wisdom/metrics | Metrics of §23 over time, Wisdom Index with criteria, governance process status»
- [ ] Metrics of §23 over time, Wisdom Index with criteria, governance process status
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-UI-015 [P2] WG-UI-015: Ask Wisdom · inside Ask the Brain · Intent chip, generated queries, precedents and lessons cards, "no precedent" and "predicted" labels, warrants on hover

- **Source:** `wisdom-graph-requirements.md:1078-1078` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-UI-015 | Ask Wisdom | inside Ask the Brain | Intent chip, generated queries, precedents and lessons cards, "no precedent" and "predicted" labels, warrants on hover
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-UI-015' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-UI-015') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-UI-015 | Ask Wisdom | inside Ask the Brain | Intent chip, generated queries, precedents and lessons cards, "no precedent" and "predicted" labels, warrants on hover»
- [ ] inside Ask the Brain
- [ ] Intent chip, generated queries, precedents and lessons cards, "no precedent" and "predicted" labels, warrants on hover
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-VAL-001 [P2] WG-VAL-001: values-service stores the value registry (§5.5): name, canonical definition (verbatim in UI), owner, rank per domain, version, approval. Values are tenant configuration; changing them requires wg.valu

- **Source:** `wisdom-graph-requirements.md:764-764` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-VAL-001 | `values-service` stores the value registry (§5.5): name, canonical definition (verbatim in UI), owner, rank per domain, version, approval. Values are tenant configuration; changing them requires `wg.values.manage` and creates a new version.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-VAL-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-VAL-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-VAL-001 | values-service stores the value registry (§5.5): name, canonical definition (verbatim in UI), owner, rank per domain, version, approval. Values are tenant configuration; changing them requires wg.values.manage and creates a new version.»
- [ ] values-service stores the value registry (§5.5): name, canonical definition (verbatim in UI), owner, rank per domain, version, approval. Values are tenant configuration; changing them requires wg.values.manage and creates a new version.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-VAL-002 [P2] WG-VAL-002: Trade-off rules (§5.5) state which value is preferred over which in a domain, with optional unless conditions over situation features. A rule set is validated for cycles within a domain (A over B, B o

- **Source:** `wisdom-graph-requirements.md:765-765` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-VAL-002 | Trade-off rules (§5.5) state which value is preferred over which in a domain, with optional `unless` conditions over situation features. A rule set is validated for cycles within a domain (A over B, B over C, C over A without disjoint conditions) and rejected with `WSD_VALUE_CYCLE`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-VAL-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-VAL-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-VAL-002 | Trade-off rules (§5.5) state which value is preferred over which in a domain, with optional unless conditions over situation features. A rule set is validated for cycles within a domain (A over B, B over C, C over A without disjoint conditions) and rejected with WSD_VALUE_CYCLE.»
- [ ] Trade-off rules (§5.5) state which value is preferred over which in a domain, with optional unless conditions over situation features. A rule set is validated for cycles within a domain (A over B, B over C, C over A without disjoint conditions) and rejected with WSD_VALUE_CYCLE.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-VAL-003 [P2] WG-VAL-003: Each decision type declares which values its options typically protect or risk (valuesatstake defaults); the decision-maker can add or remove values at decision time

- **Source:** `wisdom-graph-requirements.md:766-766` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-VAL-003 | Each decision type declares which values its options typically protect or risk (`values_at_stake` defaults); the decision-maker can add or remove values at decision time.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-VAL-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-VAL-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-VAL-003 | Each decision type declares which values its options typically protect or risk (values_at_stake defaults); the decision-maker can add or remove values at decision time.»
- [ ] Each decision type declares which values its options typically protect or risk (values_at_stake defaults); the decision-maker can add or remove values at decision time.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-VAL-004 [P2] WG-VAL-004: Value conflict detection: at a checkpoint, if the chosen option risks a value ranked higher in the domain than every value it protects, and no trade-off rule with matching conditions permits it, couns

- **Source:** `wisdom-graph-requirements.md:767-767` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-VAL-004 | Value conflict detection: at a checkpoint, if the chosen option risks a value ranked higher in the domain than every value it protects, and no trade-off rule with matching conditions permits it, counsel reports `WSD_VALUE_CONFLICT` with the rule set consulted.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-VAL-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-VAL-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-VAL-004 | Value conflict detection: at a checkpoint, if the chosen option risks a value ranked higher in the domain than every value it protects, and no trade-off rule with matching conditions permits it, counsel reports WSD_VALUE_CONFLICT with the rule set consulted.»
- [ ] Value conflict detection: at a checkpoint, if the chosen option risks a value ranked higher in the domain than every value it protects, and no trade-off rule with matching conditions permits it, counsel reports WSD_VALUE_CONFLICT with the rule set consulted.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-VAL-005 [P2] WG-VAL-005: Value outcomes: outcome specs may be tagged with the value they measure; the Wisdom Index (§23) reports, per value, the share of decisions whose outcomes protected it

- **Source:** `wisdom-graph-requirements.md:768-768` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-VAL-005 | Value outcomes: outcome specs may be tagged with the value they measure; the Wisdom Index (§23) reports, per value, the share of decisions whose outcomes protected it.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-VAL-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-VAL-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-VAL-005 | Value outcomes: outcome specs may be tagged with the value they measure; the Wisdom Index (§23) reports, per value, the share of decisions whose outcomes protected it.»
- [ ] Value outcomes: outcome specs may be tagged with the value they measure; the Wisdom Index (§23) reports, per value, the share of decisions whose outcomes protected it.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-VAL-006 [P2] WG-VAL-006: APIs: GET/POST/PUT /wisdom/values, GET/POST/PUT /wisdom/trade-off-rules, POST /wisdom/values/check {situation, option}

- **Source:** `wisdom-graph-requirements.md:769-769` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-VAL-006 | APIs: `GET/POST/PUT /wisdom/values`, `GET/POST/PUT /wisdom/trade-off-rules`, `POST /wisdom/values/check {situation, option}`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-VAL-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-VAL-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-VAL-006 | APIs: GET/POST/PUT /wisdom/values, GET/POST/PUT /wisdom/trade-off-rules, POST /wisdom/values/check {situation, option}.»
- [ ] APIs: GET/POST/PUT /wisdom/values, GET/POST/PUT /wisdom/trade-off-rules, POST /wisdom/values/check {situation, option}.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-WLD-001 [P2] WG-WLD-001: world-model-service implements W11 training exactly, registers every model in the model registry (GN-007/REQ-NEU-030) with seed, environment (GN-012), data window and gate report, and promotes only th

- **Source:** `wisdom-graph-requirements.md:873-873` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-WLD-001 | `world-model-service` implements W11 training exactly, registers every model in the model registry (GN-007/REQ-NEU-030) with seed, environment (GN-012), data window and gate report, and promotes only through the gate.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-WLD-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-WLD-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-WLD-001 | world-model-service implements W11 training exactly, registers every model in the model registry (GN-007/REQ-NEU-030) with seed, environment (GN-012), data window and gate report, and promotes only through the gate.»
- [ ] world-model-service implements W11 training exactly, registers every model in the model registry (GN-007/REQ-NEU-030) with seed, environment (GN-012), data window and gate report, and promotes only through the gate.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-WLD-002 [P2] WG-WLD-002: POST /wisdom/predict {situation, options[]} returns calibrated psuccess per option with the model version and abstentions; counsel uses it when wisdom.worldmodelincounsel = true (default true when a m

- **Source:** `wisdom-graph-requirements.md:874-874` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-WLD-002 | `POST /wisdom/predict {situation, options[]}` returns calibrated `p_success` per option with the model version and abstentions; counsel uses it when `wisdom.world_model_in_counsel = true` (default true when a model is ACTIVE for the decision type).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-WLD-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-WLD-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-WLD-002 | POST /wisdom/predict {situation, options[]} returns calibrated p_success per option with the model version and abstentions; counsel uses it when wisdom.world_model_in_counsel = true (default true when a model is ACTIVE for the decision type).»
- [ ] POST /wisdom/predict {situation, options[]} returns calibrated p_success per option with the model version and abstentions; counsel uses it when wisdom.world_model_in_counsel = true (default true when a model is ACTIVE for the decision type).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-WLD-003 [P2] WG-WLD-003: POST /wisdom/whatif implements W11 steps 6–9; POST /wisdom/decisions/{id}/counterfactual {option} answers "what if we had chosen B" for a past decision using its decision-time context, never present-d

- **Source:** `wisdom-graph-requirements.md:875-875` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-WG-WLD-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-WLD-003 | `POST /wisdom/whatif` implements W11 steps 6–9; `POST /wisdom/decisions/{id}/counterfactual {option}` answers "what if we had chosen B" for a past decision using its decision-time context, never present-day state.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-WLD-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-WLD-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-WG-WLD-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-WLD-003 | POST /wisdom/whatif implements W11 steps 6–9; POST /wisdom/decisions/{id}/counterfactual {option} answers "what if we had chosen B" for a past decision using its decision-time context, never present-day state.»
- [ ] POST /wisdom/whatif implements W11 steps 6–9; POST /wisdom/decisions/{id}/counterfactual {option} answers "what if we had chosen B" for a past decision using its decision-time context, never present-day state.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-WLD-004 [P2] WG-WLD-004: Abstention is mandatory outside the training distribution (step 6). A test with 50 synthetic out-of-distribution situations asserts 50 abstentions

- **Source:** `wisdom-graph-requirements.md:876-876` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-WLD-004 | Abstention is mandatory outside the training distribution (step 6). A test with 50 synthetic out-of-distribution situations asserts 50 abstentions.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-WLD-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-WLD-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-WLD-004 | Abstention is mandatory outside the training distribution (step 6). A test with 50 synthetic out-of-distribution situations asserts 50 abstentions.»
- [ ] Abstention is mandatory outside the training distribution (step 6). A test with 50 synthetic out-of-distribution situations asserts 50 abstentions.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-WLD-005 [P2] WG-WLD-005: The world model never writes to the knowledge layer and never changes a decision; its outputs are PREDICTED and expire with the model version

- **Source:** `wisdom-graph-requirements.md:877-877` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-WLD-005 | The world model never writes to the knowledge layer and never changes a decision; its outputs are `PREDICTED` and expire with the model version.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-WLD-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-WLD-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-WLD-005 | The world model never writes to the knowledge layer and never changes a decision; its outputs are PREDICTED and expire with the model version.»
- [ ] The world model never writes to the knowledge layer and never changes a decision; its outputs are PREDICTED and expire with the model version.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-WLD-006 [P2] WG-WLD-006: Simulation fidelity check: for 100 seeded past decisions with recorded actual effects, the shadow-branch diff of the chosen option matches the recorded actual assertion changes (set equality on assert

- **Source:** `wisdom-graph-requirements.md:878-878` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-WLD-006 | Simulation fidelity check: for 100 seeded past decisions with recorded actual effects, the shadow-branch diff of the chosen option matches the recorded actual assertion changes (set equality on assertion ids and change kinds) in ≥ 95% of cases; mismatches list the tools whose `simulate` is incomplete.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-WLD-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-WLD-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-WLD-006 | Simulation fidelity check: for 100 seeded past decisions with recorded actual effects, the shadow-branch diff of the chosen option matches the recorded actual assertion changes (set equality on assertion ids and change kinds) in ≥ 95% of cases; mismatches list the tools whose simulate is incomplete.»
- [ ] Simulation fidelity check: for 100 seeded past decisions with recorded actual effects, the shadow-branch diff of the chosen option matches the recorded actual assertion changes (set equality on assertion ids and change kinds) in ≥ 95% of cases; mismatches list the tools whose simulate is incomplete.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-WLD-007 [P2] WG-WLD-007: Acceptance on the seeded tenant: the gradient-boosted predictor beats every baseline of step 4 by ≥ 0.03 AUPRC on at least 4 of the 6 seeded decision types, with ECE ≤ 0.10; decision types where it do

- **Source:** `wisdom-graph-requirements.md:879-879` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-WG-WLD-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-WLD-007 | Acceptance on the seeded tenant: the gradient-boosted predictor beats every baseline of step 4 by ≥ 0.03 AUPRC on at least 4 of the 6 seeded decision types, with ECE ≤ 0.10; decision types where it does not are reported as "no world model — baselines sufficient" (an accepted outcome, not a failure of this requirement).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-WLD-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-WLD-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-WG-WLD-007

**Acceptance criteria**
- [ ] on the seeded tenant: the gradient-boosted predictor beats every baseline of step 4 by ≥ 0.03 AUPRC on at least 4 of the 6 seeded decision types, with ECE ≤ 0.10; decision types where it does not are reported as "no world model — baselines sufficient" (an accepted outcome, not a failure of this requirement)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-WLD-008 [P2] WG-WLD-008: The anti-stub probes of GN-003 (loss descent, weight delta where applicable, label-permutation gap ≥ 0.10, structural coherence for the neural candidate) are run for every trained world model and stor

- **Source:** `wisdom-graph-requirements.md:880-880` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-WLD-008 | The anti-stub probes of GN-003 (loss descent, weight delta where applicable, label-permutation gap ≥ 0.10, structural coherence for the neural candidate) are run for every trained world model and stored in its gate report.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-WLD-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-WLD-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-WLD-008 | The anti-stub probes of GN-003 (loss descent, weight delta where applicable, label-permutation gap ≥ 0.10, structural coherence for the neural candidate) are run for every trained world model and stored in its gate report.»
- [ ] The anti-stub probes of GN-003 (loss descent, weight delta where applicable, label-permutation gap ≥ 0.10, structural coherence for the neural candidate) are run for every trained world model and stored in its gate report.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-WLD-009 [P2] WG-WLD-009: Performance: predict p95 < 50 ms per option; whatif including shadow-branch simulation p95 < 5 s for plans with ≤ 20 tool calls

- **Source:** `wisdom-graph-requirements.md:881-881` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-WLD-009 | Performance: `predict` p95 < 50 ms per option; `whatif` including shadow-branch simulation p95 < 5 s for plans with ≤ 20 tool calls.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-WLD-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-WLD-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-WLD-009 | Performance: predict p95 < 50 ms per option; whatif including shadow-branch simulation p95 < 5 s for plans with ≤ 20 tool calls.»
- [ ] Performance: predict p95 < 50 ms per option; whatif including shadow-branch simulation p95 < 5 s for plans with ≤ 20 tool calls.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

