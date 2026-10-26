# EPIC-IP-CI: EOIP-engg-doc-pkg/ip-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 10 tasks, ~10.0 h, priorities {'P1': 8, 'P2': 2}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-REQ-BRB-001 [P1] REQ-BRB-001: consequence-service MUST implement A4 exactly and be called from the commit checkpoint for action classes EXTERNALWRITE and IRREVERSIBLE, and for INTERNALWRITE when budget.applytointernalwrites=true (

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:658-658` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-REQ-BRB-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-BRB-001 | `consequence-service` MUST implement A4 exactly and be called from the `commit` checkpoint for action classes `EXTERNAL_WRITE` and `IRREVERSIBLE`, and for `INTERNAL_WRITE` when `budget.apply_to_internal_writes=true` (default false).
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-REQ-BRB-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-BRB-001 | consequence-service MUST implement A4 exactly and be called from the commit checkpoint for action classes EXTERNAL_WRITE and IRREVERSIBLE, and for INTERNAL_WRITE when budget.apply_to_internal_writes=true (default false).»
- [ ] consequence-service MUST implement A4 exactly and be called from the commit checkpoint for action classes EXTERNAL_WRITE and IRREVERSIBLE, and for INTERNAL_WRITE when budget.apply_to_internal_writes=true (default false).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_warrant_composition.py:280`, `tests/unit/test_warrant_composition.py::test_action_warrant_requires_trusted_action_class_and_kappa`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-REQ-PLT-001 [P1] REQ-PLT-001: Every new table, collection, node label, edge type, index, cache key, queue topic, file path, metric label and log line MUST carry tenantid. No query may run without a tenant filter applied by the pla

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:142-142` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-REQ-PLT-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PLT-001 | Every new table, collection, node label, edge type, index, cache key, queue topic, file path, metric label and log line MUST carry `tenant_id`. No query may run without a tenant filter applied by the platform layer, not by callers.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-REQ-PLT-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PLT-001 | Every new table, collection, node label, edge type, index, cache key, queue topic, file path, metric label and log line MUST carry tenant_id. No query may run without a tenant filter applied by the platform layer, not by callers.»
- [ ] Every new table, collection, node label, edge type, index, cache key, queue topic, file path, metric label and log line MUST carry tenant_id. No query may run without a tenant filter applied by the platform layer, not by callers.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_warrant_composition.py:264`, `tests/unit/test_warrant_composition.py::test_composition_rejects_cross_tenant_inputs`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-REQ-WAR-001 [P1] REQ-WAR-001: The status order MUST be a tenant configuration warrant.statusorder (array of the six values). Only swapping OBSERVED and ATTESTED is permitted; any other order is rejected with error WARINVALIDORDER

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:243-243` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-REQ-WAR-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-WAR-001 | The status order MUST be a tenant configuration `warrant.status_order` (array of the six values). Only swapping `OBSERVED` and `ATTESTED` is permitted; any other order is rejected with error `WAR_INVALID_ORDER`.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-REQ-WAR-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-WAR-001 | The status order MUST be a tenant configuration warrant.status_order (array of the six values). Only swapping OBSERVED and ATTESTED is permitted; any other order is rejected with error WAR_INVALID_ORDER.»
- [ ] The status order MUST be a tenant configuration warrant.status_order (array of the six values). Only swapping OBSERVED and ATTESTED is permitted; any other order is rejected with error WAR_INVALID_ORDER.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_warrant_composition.py:207`, `tests/unit/test_warrant_composition.py::test_model_requires_calibrated_confidence_and_uses_status_order`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-REQ-WAR-002 [P1] REQ-WAR-002: min(σ1, σ2) and comparisons MUST use the tenant's configured order

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:244-244` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-REQ-WAR-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-WAR-002 | `min(σ1, σ2)` and comparisons MUST use the tenant's configured order.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-REQ-WAR-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-WAR-002 | min(σ1, σ2) and comparisons MUST use the tenant's configured order.»
- [ ] min(σ1, σ2) and comparisons MUST use the tenant's configured order.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_warrant_composition.py:207`, `tests/unit/test_warrant_composition.py::test_model_requires_calibrated_confidence_and_uses_status_order`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-REQ-WCA-001 [P1] REQ-WCA-001: warrant-service MUST implement A1 exactly as specified, as a pure deterministic function compose(operator, inputs, receiptgrounds, principal) -> Warrant, with no I/O except reading the operator regist

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:423-423` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-REQ-WCA-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-WCA-001 | `warrant-service` MUST implement A1 exactly as specified, as a pure deterministic function `compose(operator, inputs, receipt_grounds, principal) -> Warrant`, with no I/O except reading the operator registry and ontology subtype relation (both cacheable).
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-REQ-WCA-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-WCA-001 | warrant-service MUST implement A1 exactly as specified, as a pure deterministic function compose(operator, inputs, receipt_grounds, principal) -> Warrant, with no I/O except reading the operator registry and ontology subtype relation (both cacheable).»
- [ ] warrant-service MUST implement A1 exactly as specified, as a pure deterministic function compose(operator, inputs, receipt_grounds, principal) -> Warrant, with no I/O except reading the operator registry and ontology subtype relation (both cacheable).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_warrant_composition.py:111`, `tests/unit/test_warrant_composition.py::test_action_warrant_requires_trusted_action_class_and_kappa`, `tests/unit/test_warrant_composition.py::test_composition_rejects_cross_tenant_inputs`, `tests/unit/test_warrant_composition.py::test_computation_takes_weakest_status_and_never_widens_scope_or_validity`, `tests/unit/test_warrant_composition.py::test_empty_computation_is_unknown_and_scope_intersection_cannot_widen`, `tests/unit/test_warrant_composition.py::test_generator_requires_matching_sasi_result_and_operator_must_be_approved`, `tests/unit/test_warrant_composition.py::test_model_requires_calibrated_confidence_and_uses_status_order`, `tests/unit/test_warrant_composition.py::test_observer_requires_qualification_and_human_requires_subject_authority`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-REQ-WCA-002 [P1] REQ-WCA-002: No-upgrade rule. No code path may produce a warrant whose status is higher than allowed by A1. A property-based test MUST generate ≥ 10,000 random operator/input combinations and assert the rule

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:424-424` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-REQ-WCA-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-WCA-002 | **No-upgrade rule.** No code path may produce a warrant whose status is higher than allowed by A1. A property-based test MUST generate ≥ 10,000 random operator/input combinations and assert the rule.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-REQ-WCA-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-WCA-002 | No-upgrade rule. No code path may produce a warrant whose status is higher than allowed by A1. A property-based test MUST generate ≥ 10,000 random operator/input combinations and assert the rule.»
- [ ] No-upgrade rule. No code path may produce a warrant whose status is higher than allowed by A1. A property-based test MUST generate ≥ 10,000 random operator/input combinations and assert the rule.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_warrant_composition.py:111`, `tests/unit/test_warrant_composition.py::test_a1_status_authority_and_validity_properties`, `tests/unit/test_warrant_composition.py::test_computation_takes_weakest_status_and_never_widens_scope_or_validity`, `tests/unit/test_warrant_composition.py::test_empty_computation_is_unknown_and_scope_intersection_cannot_widen`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-REQ-WCA-003 [P1] REQ-WCA-003: Authority MUST never widen: for every composition, authorityout.scopes ⊆ αf.scopes and ⊆ scopesi for each input. Property-based test as above

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:425-425` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-REQ-WCA-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-WCA-003 | Authority MUST never widen: for every composition, `authority_out.scopes ⊆ α_f.scopes` and `⊆ scopes_i` for each input. Property-based test as above.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-REQ-WCA-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-WCA-003 | Authority MUST never widen: for every composition, authority_out.scopes ⊆ α_f.scopes and ⊆ scopes_i for each input. Property-based test as above.»
- [ ] Authority MUST never widen: for every composition, authority_out.scopes ⊆ α_f.scopes and ⊆ scopes_i for each input. Property-based test as above.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_warrant_composition.py:111`, `tests/unit/test_warrant_composition.py::test_a1_status_authority_and_validity_properties`, `tests/unit/test_warrant_composition.py::test_computation_takes_weakest_status_and_never_widens_scope_or_validity`, `tests/unit/test_warrant_composition.py::test_empty_computation_is_unknown_and_scope_intersection_cannot_widen`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-REQ-WCA-004 [P1] REQ-WCA-004: Validity MUST never extend beyond any input's validto. Property-based test as above

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:426-426` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-REQ-WCA-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-WCA-004 | Validity MUST never extend beyond any input's `valid_to`. Property-based test as above.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-REQ-WCA-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-WCA-004 | Validity MUST never extend beyond any input's valid_to. Property-based test as above.»
- [ ] Validity MUST never extend beyond any input's valid_to. Property-based test as above.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_warrant_composition.py:111`, `tests/unit/test_warrant_composition.py::test_a1_status_authority_and_validity_properties`, `tests/unit/test_warrant_composition.py::test_computation_takes_weakest_status_and_never_widens_scope_or_validity`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-REQ-OPR-004 [P2] REQ-OPR-004: OBSERVER class is allowed only for operators that read from a source with kgf:observerSource=true or from the KGF graph assertions whose own status is OBSERVED. Registration validates this

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:392-392` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-REQ-OPR-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-OPR-004 | `OBSERVER` class is allowed only for operators that read from a source with `kgf:observerSource=true` or from the KGF graph assertions whose own status is `OBSERVED`. Registration validates this.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-REQ-OPR-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-OPR-004 | OBSERVER class is allowed only for operators that read from a source with kgf:observerSource=true or from the KGF graph assertions whose own status is OBSERVED. Registration validates this.»
- [ ] OBSERVER class is allowed only for operators that read from a source with kgf:observerSource=true or from the KGF graph assertions whose own status is OBSERVED. Registration validates this.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_warrant_composition.py:177`, `tests/unit/test_warrant_composition.py::test_observer_requires_qualification_and_human_requires_subject_authority`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-REQ-WAR-011 [P2] REQ-WAR-011: Warrants are immutable. A change produces a new warrant whose parents includes the old one

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:344-344` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-REQ-WAR-011; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-WAR-011 | Warrants are immutable. A change produces a new warrant whose `parents` includes the old one.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-REQ-WAR-011

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-WAR-011 | Warrants are immutable. A change produces a new warrant whose parents includes the old one.»
- [ ] Warrants are immutable. A change produces a new warrant whose parents includes the old one.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_warrant_composition.py:231`, `tests/unit/test_warrant_composition.py::test_generator_requires_matching_sasi_result_and_operator_must_be_approved`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

