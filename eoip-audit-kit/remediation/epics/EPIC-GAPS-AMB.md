# EPIC-GAPS-AMB: EOIP-engg-doc-pkg/gaps-requirements.md · ambiguous_tests

*Mapped tests both pass and fail on the audited commit.* 5 tasks, ~10.5 h, priorities {'P1': 5}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-GAP-CP-009 [P1] GAP-CP-009: Semantic contracts are machine-readable and testable

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:407-407` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-CP-009:** Semantic contracts are machine-readable and testable.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Semantic contracts are machine-readable and testable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/coverage.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/coverage.py#L8-L8)
- tests: `tests/unit/test_gap_coverage.py:4`, `tests/unit/test_gap_coverage.py::test_g2_docs_are_loaded_from_heading_requirements`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_docs_are_loaded_as_machine_readable_contracts`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GAP-KGCI-001 [P1] GAP-KGCI-001: CLI runnable in CI

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:820-820` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 24, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-KGCI-001:** CLI runnable in CI.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): CLI runnable in CI.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:213`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L213-L213), [`packages/eoip/ci/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ci/__init__.py#L1-L1), [`packages/eoip/ci/pipeline.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ci/pipeline.py#L1-L1), [`packages/eoip/gaps/coverage.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/coverage.py#L9-L9), [`scripts/gap_coverage.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/gap_coverage.py#L4-L4)
- tests: `tests/unit/test_gap_coverage.py:5`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_kgci_pipeline.py:1`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GAP-KGCI-002 [P1] GAP-KGCI-002: Machine-readable report

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:821-821` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-KGCI-002:** Machine-readable report.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Machine-readable report.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ci/pipeline.py:112`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ci/pipeline.py#L112-L112), [`packages/eoip/gaps/coverage.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/coverage.py#L10-L10), [`scripts/gap_coverage.py:5`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/gap_coverage.py#L5-L5)
- tests: `tests/unit/test_gap_coverage.py:6`, `tests/unit/test_gap_coverage.py::test_g2_coverage_report_uses_selected_document_set`, `tests/unit/test_gap_coverage.py::test_g2_docs_are_loaded_from_heading_requirements`, `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`, `tests/unit/test_gap_coverage.py::test_gap_docs_are_loaded_as_machine_readable_contracts`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GAP-KGCI-003 [P1] GAP-KGCI-003: Fail build on configured semantic regression

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:822-822` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-KGCI-003:** Fail build on configured semantic regression.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Fail build on configured semantic regression.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ci/pipeline.py:74`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ci/pipeline.py#L74-L74), [`packages/eoip/gaps/coverage.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/coverage.py#L11-L11), [`scripts/gap_coverage.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/gap_coverage.py#L6-L6)
- tests: `tests/unit/test_gap_coverage.py:7`, `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GAP-SDT-001 [P1] GAP-SDT-001: Every requirement must be linkable to design, story, commit, code symbol, test, build, deployment, service and incident

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:381-381` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 11, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; ID defined at 1 other site(s): see duplicate task DUP-GAP-SDT-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04, FT-F09 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-SDT-001:** Every requirement must be linkable to design, story, commit, code symbol, test, build, deployment, service and incident.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)
4. Resolve duplicate definition first: DUP-GAP-SDT-001

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Every requirement must be linkable to design, story, commit, code symbol, test, build, deployment, service and incident.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:49`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L49-L49)
- tests: `tests/unit/test_enterprise_gap_completion.py:42`, `tests/unit/test_gap_coverage.py:43`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

