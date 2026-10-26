# EPIC-GAPS2-AMB: EOIP-engg-doc-pkg/gaps2-requirements.md · ambiguous_tests

*Mapped tests both pass and fail on the audited commit.* 26 tasks, ~52.0 h, priorities {'P0': 2, 'P1': 24}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-G2-ARCH-014 [P0] G2-ARCH-014: Source permissions respected

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:112-115` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCH-014 — Source permissions respected

Crawlers/connectors SHALL operate only against explicitly configured/authorized scopes and credentials.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Crawlers/connectors SHALL operate only against explicitly configured/authorized scopes and credentials.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_architecture.py:84`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_architecture.py#L84-L84), [`scripts/tick_phase0_phase1.py:18`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L18-L18)
- tests: `tests/unit/test_gap_coverage.py:126`, `tests/unit/test_gap_coverage.py::test_g2_architecture_guardrails_are_executable`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-SRC-GH-001 [P0] G2-SRC-GH-001: G2-SRC-GH-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:426-428` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 5, failed 1)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F07 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-GH-001
Capture repositories, organizations, branches, tags, commits, pull requests, issues, releases, workflows/actions metadata and repository ownership metadata where authorized.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_github_connector.py::test_github_webhook_delete_and_error_categories_are_safe
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Capture repositories, organizations, branches, tags, commits, pull requests, issues, releases, workflows/actions metadata and repository ownership metadata where authorized.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:41`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L41-L41), [`packages/eoip/ingestion/github.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ingestion/github.py#L1-L1), [`scripts/tick_phase2_batch1.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L15-L15)
- tests: `tests/unit/test_g2_readiness.py:38`, `tests/unit/test_github_connector.py:25`, `tests/unit/test_github_connector.py::test_github_baseline_discovers_and_emits_versioned_engineering_events`
- failing: `tests/unit/test_github_connector.py::test_github_webhook_delete_and_error_categories_are_safe`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-ARCH-001 [P1] G2-ARCH-001: One acquisition contract

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:52-55` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 10, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCH-001 — One acquisition contract

Every source integration SHALL emit the same canonical `SourceEvent` family and SHALL NOT write HugeGraph directly.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Every source integration SHALL emit the same canonical SourceEvent family and SHALL NOT write HugeGraph directly.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_architecture.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_architecture.py#L3-L3), [`packages/eoip/gaps/g2_readiness.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L8-L8)
- tests: `tests/unit/test_g2_readiness.py:5`, `tests/unit/test_gap_coverage.py:8`, `tests/unit/test_gap_coverage.py::test_g2_architecture_guardrails_are_executable`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-ARCH-002 [P1] G2-ARCH-002: API/event first

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:56-67` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCH-002 — API/event first

Source acquisition SHALL prefer:

1. webhook/event,
2. incremental/delta API,
3. REST/GraphQL/API,
4. repository protocol,
5. filesystem,
6. controlled web crawler,
7. browser automation only as a last resort.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): API/event first Source acquisition SHALL prefer: 1. webhook/event, 2. incremental/delta API, 3. REST/GraphQL/API, 4. repository protocol, 5. filesystem, 6. controlled web crawler, 7. browser automation only as a last resort.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_architecture.py:72`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_architecture.py#L72-L72), [`scripts/tick_phase0_phase1.py:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L17-L17)
- tests: `tests/unit/test_gap_coverage.py:117`, `tests/unit/test_gap_coverage.py::test_g2_architecture_guardrails_are_executable`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-ARCH-003 [P1] G2-ARCH-003: Deterministic first

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:68-71` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCH-003 — Deterministic first

Deterministic source metadata, parser output, identifiers and explicit relationships SHALL take precedence over AI-inferred relationships.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Deterministic source metadata, parser output, identifiers and explicit relationships SHALL take precedence over AI-inferred relationships.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_architecture.py:73`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_architecture.py#L73-L73), [`scripts/tick_phase0_phase1.py:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L17-L17)
- tests: `tests/unit/test_gap_coverage.py:118`, `tests/unit/test_gap_coverage.py::test_g2_architecture_guardrails_are_executable`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-ARCH-004 [P1] G2-ARCH-004: Preserve source fidelity

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:72-75` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCH-004 — Preserve source fidelity

Raw source payloads or evidence references SHALL be retained locally according to retention policy so graph facts can be replayed and audited.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Raw source payloads or evidence references SHALL be retained locally according to retention policy so graph facts can be replayed and audited.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_architecture.py:74`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_architecture.py#L74-L74), [`scripts/tick_phase0_phase1.py:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L17-L17)
- tests: `tests/unit/test_gap_coverage.py:119`, `tests/unit/test_gap_coverage.py::test_g2_architecture_guardrails_are_executable`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-ARCH-005 [P1] G2-ARCH-005: HugeGraph is semantic operational truth

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:76-79` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCH-005 — HugeGraph is semantic operational truth

Apache HugeGraph SHALL remain the authoritative canonical graph store for operational enterprise knowledge.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Apache HugeGraph SHALL remain the authoritative canonical graph store for operational enterprise knowledge.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_architecture.py:75`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_architecture.py#L75-L75), [`scripts/tick_phase0_phase1.py:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L17-L17)
- tests: `tests/unit/test_gap_coverage.py:120`, `tests/unit/test_gap_coverage.py::test_g2_architecture_guardrails_are_executable`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-ARCH-006 [P1] G2-ARCH-006: No raw telemetry lake in HugeGraph

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:80-83` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCH-006 — No raw telemetry lake in HugeGraph

High-volume logs/metrics/traces SHALL NOT be copied wholesale into HugeGraph. EOIP SHALL store semantic summaries, topology, fingerprints, events, evidence pointers and bounded samples.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] High-volume logs/metrics/traces SHALL NOT be copied wholesale into HugeGraph.
- [ ] EOIP SHALL store semantic summaries, topology, fingerprints, events, evidence pointers and bounded samples.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_architecture.py:76`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_architecture.py#L76-L76)
- tests: `tests/unit/test_gap_coverage.py:141`, `tests/unit/test_gap_coverage.py::test_g2_architecture_guardrails_report_profile_violations`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-ARCH-008 [P1] G2-ARCH-008: Current and historical views

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:88-91` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCH-008 — Current and historical views

Every time-varying domain SHALL support current-state and historical-state queries.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Every time-varying domain SHALL support current-state and historical-state queries.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_architecture.py:78`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_architecture.py#L78-L78), [`scripts/tick_phase0_phase1.py:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L17-L17)
- tests: `tests/unit/test_gap_coverage.py:121`, `tests/unit/test_gap_coverage.py::test_g2_architecture_guardrails_are_executable`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-ARCH-009 [P1] G2-ARCH-009: One semantic identity system

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:92-95` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCH-009 — One semantic identity system

All connectors SHALL resolve into canonical IDs independent of source-internal database IDs.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] All connectors SHALL resolve into canonical IDs independent of source-internal database IDs.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_architecture.py:79`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_architecture.py#L79-L79), [`scripts/tick_phase0_phase1.py:18`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L18-L18)
- tests: `tests/unit/test_gap_coverage.py:122`, `tests/unit/test_gap_coverage.py::test_g2_architecture_guardrails_are_executable`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-ARCH-010 [P1] G2-ARCH-010: Evidence is mandatory

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:96-99` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCH-010 — Evidence is mandatory

Every externally sourced or inferred graph mutation SHALL carry provenance/evidence metadata.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Every externally sourced or inferred graph mutation SHALL carry provenance/evidence metadata.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_architecture.py:80`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_architecture.py#L80-L80)
- tests: `tests/unit/test_gap_coverage.py:123`, `tests/unit/test_gap_coverage.py::test_g2_architecture_guardrails_are_executable`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-ARCH-011 [P1] G2-ARCH-011: AI is not the source of truth

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:100-103` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCH-011 — AI is not the source of truth

The system SHALL remain useful with local models disabled.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] The system SHALL remain useful with local models disabled.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_architecture.py:81`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_architecture.py#L81-L81)
- tests: `tests/unit/test_gap_coverage.py:141`, `tests/unit/test_gap_coverage.py::test_g2_architecture_guardrails_report_profile_violations`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-ARCH-012 [P1] G2-ARCH-012: Incremental by default after baseline

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:104-107` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCH-012 — Incremental by default after baseline

After a source baseline is established, normal synchronization SHALL process only new/changed/deleted source records plus periodic reconciliation.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] After a source baseline is established, normal synchronization SHALL process only new/changed/deleted source records plus periodic reconciliation.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_architecture.py:82`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_architecture.py#L82-L82), [`scripts/tick_phase0_phase1.py:18`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L18-L18)
- tests: `tests/unit/test_gap_coverage.py:124`, `tests/unit/test_gap_coverage.py::test_g2_architecture_guardrails_are_executable`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-ARCH-013 [P1] G2-ARCH-013: Replayability

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:108-111` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCH-013 — Replayability

EOIP SHALL be able to rebuild derived graph state from captured events/mappings for supported domains.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] EOIP SHALL be able to rebuild derived graph state from captured events/mappings for supported domains.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_architecture.py:83`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_architecture.py#L83-L83), [`scripts/tick_phase0_phase1.py:18`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L18-L18)
- tests: `tests/unit/test_gap_coverage.py:125`, `tests/unit/test_gap_coverage.py::test_g2_architecture_guardrails_are_executable`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-ARCH-015 [P1] G2-ARCH-015: Progressive complexity

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:116-121` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCH-015 — Progressive complexity

MVP/team deployments SHALL remain lightweight. Brokers, separate search clusters, distributed graph components and additional stores SHALL be added only when workload evidence justifies them.

---
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Brokers, separate search clusters, distributed graph components and additional stores SHALL be added only when workload evidence justifies them.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_architecture.py:85`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_architecture.py#L85-L85)
- tests: `tests/unit/test_gap_coverage.py:127`, `tests/unit/test_gap_coverage.py::test_g2_architecture_guardrails_are_executable`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-OBS-001 [P1] G2-OBS-001: G2-OBS-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1702-1704` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 10, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-OBS-001
Trace source fetch → SourceEvent → mapping → graph mutation.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Trace source fetch → SourceEvent → mapping → graph mutation.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_observability.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_observability.py#L3-L3), [`packages/eoip/gaps/g2_readiness.py:27`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L27-L27)
- tests: `tests/unit/test_g2_readiness.py:24`, `tests/unit/test_gap_coverage.py:9`, `tests/unit/test_gap_coverage.py::test_g2_observability_contract_validates_required_metrics`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-OBS-002 [P1] G2-OBS-002: G2-OBS-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1705-1713` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-OBS-002
Expose per-source:
- fetch latency,
- records/sec,
- errors,
- lag,
- retries,
- DLQ count.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Expose per-source: - fetch latency, - records/sec, - errors, - lag, - retries, - DLQ count.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_observability.py:30`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_observability.py#L30-L30)
- tests: `tests/unit/test_gap_coverage.py:181`, `tests/unit/test_gap_coverage.py::test_g2_observability_contract_reports_missing_metrics`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-OBS-003 [P1] G2-OBS-003: G2-OBS-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1714-1719` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-OBS-003
Expose graph evolution metrics:
- added/changed/expired facts,
- mutation latency,
- validation failures.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Expose graph evolution metrics: - added/changed/expired facts, - mutation latency, - validation failures.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_observability.py:36`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_observability.py#L36-L36)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_gap_coverage.py:182`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-OBS-004 [P1] G2-OBS-004: G2-OBS-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1720-1722` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-OBS-004
Expose semantic event bus consumer lag.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Expose semantic event bus consumer lag.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_observability.py:41`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_observability.py#L41-L41)
- tests: `tests/unit/test_gap_coverage.py:183`, `tests/unit/test_gap_coverage.py::test_g2_observability_contract_reports_missing_metrics`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-OBS-005 [P1] G2-OBS-005: G2-OBS-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1723-1725` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-OBS-005
Expose graph version publication time.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Expose graph version publication time.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_observability.py:42`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_observability.py#L42-L42)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_gap_coverage.py:184`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-OBS-006 [P1] G2-OBS-006: G2-OBS-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1726-1730` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 7, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-OBS-006
Expose knowledge SLO evaluation latency.

---
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Expose knowledge SLO evaluation latency.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_observability.py:43`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_observability.py#L43-L43)
- tests: `tests/unit/test_gap_coverage.py:153`, `tests/unit/test_gap_coverage.py::test_g2_observability_contract_validates_required_metrics`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-QOP-003 [P1] G2-QOP-003: WHAT IF

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1323-1325` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 15, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-QOP-003 — WHAT IF
Execute counterfactual simulation where supported.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): WHAT IF Execute counterfactual simulation where supported.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/query_operators.py:277`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/query_operators.py#L277-L277)
- tests: `tests/unit/test_gap_coverage.py:111`, `tests/unit/test_question_operators_g2.py:79`, `tests/unit/test_question_operators_g2.py::test_operator_what_if_simulation`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-SRC-GH-003 [P1] G2-SRC-GH-003: G2-SRC-GH-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:432-434` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 2, failed 1)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F07 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-GH-003
Map PR/commit/change-set relationships to code symbols after parsing.
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_github_connector.py::test_github_webhook_delete_and_error_categories_are_safe
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Map PR/commit/change-set relationships to code symbols after parsing.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L15-L15)
- tests: `tests/unit/test_github_connector.py:25`, `tests/unit/test_github_connector.py::test_github_baseline_discovers_and_emits_versioned_engineering_events`
- failing: `tests/unit/test_github_connector.py::test_github_webhook_delete_and_error_categories_are_safe`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-SRC-GH-004 [P1] G2-SRC-GH-004: G2-SRC-GH-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:435-439` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 2, failed 1)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F07 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-GH-004
Capture repository documentation and GitHub Pages sources when configured.

---
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_github_connector.py::test_github_webhook_delete_and_error_categories_are_safe
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Capture repository documentation and GitHub Pages sources when configured.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L15-L15)
- tests: `tests/unit/test_github_connector.py:25`, `tests/unit/test_github_connector.py::test_github_baseline_discovers_and_emits_versioned_engineering_events`
- failing: `tests/unit/test_github_connector.py::test_github_webhook_delete_and_error_categories_are_safe`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-SRC-JIRA-006 [P1] G2-SRC-JIRA-006: G2-SRC-JIRA-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:365-369` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 13, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-JIRA-006
Capture project/version/release relationships where available.

---
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Capture project/version/release relationships where available.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:26`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L26-L26)
- tests: `tests/unit/test_gap_coverage.py:65`, `tests/unit/test_jira_connector.py:168`, `tests/unit/test_jira_connector.py::test_jira_webhook_event_handling`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-G2-UX-GRAPH-016 [P1] G2-UX-GRAPH-016: G2-UX-GRAPH-016

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1519-1523` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 52, failed 4)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D06, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-GRAPH-016
Click path → evidence bundle for path.

---
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0 tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Click path → evidence bundle for path.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:248`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L248-L248)
- tests: `tests/unit/test_gap_coverage.py:66`, `tests/unit/test_web_ux_and_admin_wp53.py:301`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_graph_016_path_evidence_bundle`
- failing: `tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`, `tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report`, `tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`, `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

