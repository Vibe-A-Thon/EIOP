# EPIC-GAPS2-CI-05: EOIP-engg-doc-pkg/gaps2-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 60 tasks, ~30.0 h, priorities {'P2': 60}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-G2-SRC-JIRA-002 [P2] G2-SRC-JIRA-002: G2-SRC-JIRA-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:353-355` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-JIRA-002
Preserve issue key and immutable source ID separately.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Preserve issue key and immutable source ID separately.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:22`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L22-L22)
- tests: `tests/unit/test_jira_connector.py:86`, `tests/unit/test_jira_connector.py::test_jira_issue_extraction_with_fields`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-JIRA-003 [P2] G2-SRC-JIRA-003: G2-SRC-JIRA-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:356-358` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-JIRA-003
Map link types into explicit graph relationships.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Map link types into explicit graph relationships.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:23`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L23-L23)
- tests: `tests/unit/test_jira_connector.py:106`, `tests/unit/test_jira_connector.py::test_jira_changelog_streaming_and_history`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-JIRA-004 [P2] G2-SRC-JIRA-004: G2-SRC-JIRA-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:359-361` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-JIRA-004
Incrementally process new/changed issues and changelog updates.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Incrementally process new/changed issues and changelog updates.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L24-L24)
- tests: `tests/unit/test_jira_connector.py:127`, `tests/unit/test_jira_connector.py::test_jira_project_version_and_metadata_hierarchy`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-JIRA-005 [P2] G2-SRC-JIRA-005: G2-SRC-JIRA-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:362-364` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-JIRA-005
Link Jira to commits/branches/MRs using deterministic references before semantic inference.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Link Jira to commits/branches/MRs using deterministic references before semantic inference.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:25`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L25-L25)
- tests: `tests/unit/test_jira_connector.py:149`, `tests/unit/test_jira_connector.py::test_jira_sprints_and_agile_metadata`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-KIB-002 [P2] G2-SRC-KIB-002: G2-SRC-KIB-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:503-505` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-KIB-002
Capture alert/rule metadata where available and configured.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Capture alert/rule metadata where available and configured.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:18`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L18-L18)
- tests: `tests/unit/test_connectors_new.py:97`, `tests/unit/test_connectors_new.py::TestKibanaConnector::test_map_event`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-KIB-003 [P2] G2-SRC-KIB-003: G2-SRC-KIB-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:506-508` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-KIB-003
Do not ingest full raw log history into HugeGraph.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Do not ingest full raw log history into HugeGraph.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:18`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L18-L18)
- tests: `tests/unit/test_connectors_new.py:97`, `tests/unit/test_connectors_new.py::TestKibanaConnector::test_map_event`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-KIB-004 [P2] G2-SRC-KIB-004: G2-SRC-KIB-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:509-518` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-KIB-004
Create semantic objects:
- LogPattern,
- ErrorSignature,
- SavedQuery,
- Dashboard,
- Panel,
- AlertDefinition,
- EvidenceWindow.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Create semantic objects: - LogPattern, - ErrorSignature, - SavedQuery, - Dashboard, - Panel, - AlertDefinition, - EvidenceWindow.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:18`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L18-L18)
- tests: `tests/unit/test_connectors_new.py:97`, `tests/unit/test_connectors_new.py::TestKibanaConnector::test_map_event`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-KIB-005 [P2] G2-SRC-KIB-005: G2-SRC-KIB-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:519-523` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-KIB-005
Retain source query/time-range pointers for reproducibility.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Retain source query/time-range pointers for reproducibility.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:18`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L18-L18)
- tests: `tests/unit/test_connectors_new.py:97`, `tests/unit/test_connectors_new.py::TestKibanaConnector::test_map_event`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-OTEL-001 [P2] G2-SRC-OTEL-001: G2-SRC-OTEL-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:556-558` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-OTEL-001
Support OTLP-compatible semantic ingestion or an adapter for normalized traces/metrics/log metadata.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Support OTLP-compatible semantic ingestion or an adapter for normalized traces/metrics/log metadata.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/connectors/otel.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/otel.py#L1-L1), [`packages/eoip/gaps/g2_readiness.py:46`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L46-L46)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:43`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-OTEL-002 [P2] G2-SRC-OTEL-002: G2-SRC-OTEL-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:559-561` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-OTEL-002
Map resource/service attributes into canonical Service, Instance, Environment and Deployment entities.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Map resource/service attributes into canonical Service, Instance, Environment and Deployment entities.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:27`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L27-L27)
- tests: `tests/unit/test_otel_connector.py:6`, `tests/unit/test_otel_connector.py::test_otel_trace_span_extraction`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-OTEL-003 [P2] G2-SRC-OTEL-003: G2-SRC-OTEL-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:562-564` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-OTEL-003
Derive bounded runtime call relationships from traces.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Derive bounded runtime call relationships from traces.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:28`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L28-L28)
- tests: `tests/unit/test_otel_connector.py:30`, `tests/unit/test_otel_connector.py::test_otel_metric_descriptor_and_datapoint_ingestion`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-OTEL-004 [P2] G2-SRC-OTEL-004: G2-SRC-OTEL-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:565-567` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-OTEL-004
Store trace exemplars/evidence references rather than all spans unless explicitly configured for a small environment.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Store trace exemplars/evidence references rather than all spans unless explicitly configured for a small environment.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:29`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L29-L29)
- tests: `tests/unit/test_otel_connector.py:52`, `tests/unit/test_otel_connector.py::test_otel_graceful_handling_when_sdk_missing`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-OTEL-005 [P2] G2-SRC-OTEL-005: G2-SRC-OTEL-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:568-572` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-OTEL-005
Use telemetry windows and confidence for runtime relationships.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Use telemetry windows and confidence for runtime relationships.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:30`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L30-L30)
- tests: `tests/unit/test_otel_connector.py:65`, `tests/unit/test_otel_connector.py::test_otel_checkpoint_and_healthy_status`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-RUNTIME-002 [P2] G2-SRC-RUNTIME-002: G2-SRC-RUNTIME-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:595-597` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 2, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-RUNTIME-002
Link image digest to build/artifact/commit where possible.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Link image digest to build/artifact/commit where possible.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:31`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L31-L31)
- tests: `tests/unit/test_runtime_connector.py:6`, `tests/unit/test_runtime_connector.py::test_runtime_infra_resource_discovery_and_extraction`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-RUNTIME-003 [P2] G2-SRC-RUNTIME-003: G2-SRC-RUNTIME-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:598-602` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 2, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-RUNTIME-003
Maintain current and historical workload/service topology.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Maintain current and historical workload/service topology.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:32`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L32-L32)
- tests: `tests/unit/test_runtime_connector.py:46`, `tests/unit/test_runtime_connector.py::test_runtime_infra_dependency_handling_and_health`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-SBOM-001 [P2] G2-SRC-SBOM-001: G2-SRC-SBOM-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:605-607` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-SBOM-001
Ingest SPDX/CycloneDX or equivalent supported SBOM formats.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Ingest SPDX/CycloneDX or equivalent supported SBOM formats.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/connectors/sbom.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/sbom.py#L1-L1), [`packages/eoip/gaps/g2_readiness.py:48`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L48-L48)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:45`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-SBOM-002 [P2] G2-SRC-SBOM-002: G2-SRC-SBOM-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:608-611` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-SBOM-002
Build:
`Repository/Artifact → Package → Version → Dependency`.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Build: Repository/Artifact → Package → Version → Dependency.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:33`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L33-L33)
- tests: `tests/unit/test_sbom_connector.py:6`, `tests/unit/test_sbom_connector.py::test_sbom_spdx_package_extraction`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-SBOM-003 [P2] G2-SRC-SBOM-003: G2-SRC-SBOM-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:612-614` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-SBOM-003
Link vulnerabilities/CVEs to affected package versions when data is provided by configured scanners/feeds.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Link vulnerabilities/CVEs to affected package versions when data is provided by configured scanners/feeds.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:34`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L34-L34)
- tests: `tests/unit/test_sbom_connector.py:36`, `tests/unit/test_sbom_connector.py::test_sbom_cyclonedx_component_extraction`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-SBOM-004 [P2] G2-SRC-SBOM-004: G2-SRC-SBOM-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:615-620` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-SBOM-004
Support query:
“Which production services contain package/version X?”

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Support query: “Which production services contain package/version X?”
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:35`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L35-L35)
- tests: `tests/unit/test_g2_readiness.py:101`, `tests/unit/test_sbom_connector.py:66`, `tests/unit/test_sbom_connector.py::test_sbom_vulnerability_extraction_and_health`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-SNKB-001 [P2] G2-SRC-SNKB-001: G2-SRC-SNKB-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:391-393` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-SNKB-001
Capture KB articles, KBs/categories, article versions, ownership, state, validity and related records.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Capture KB articles, KBs/categories, article versions, ownership, state, validity and related records.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:49`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L49-L49)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:46`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-SNKB-002 [P2] G2-SRC-SNKB-002: G2-SRC-SNKB-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:394-396` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-SNKB-002
Link KB articles to incidents, problems, services, CIs and change records when source relationships/evidence exist.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Link KB articles to incidents, problems, services, CIs and change records when source relationships/evidence exist.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:36`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L36-L36)
- tests: `tests/unit/test_servicenow_connector.py:111`, `tests/unit/test_servicenow_connector.py::test_servicenow_kb_article_extraction`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-SNKB-003 [P2] G2-SRC-SNKB-003: G2-SRC-SNKB-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:397-401` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-SNKB-003
Retain article revision lineage.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Retain article revision lineage.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:37`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L37-L37)
- tests: `tests/unit/test_servicenow_connector.py:129`, `tests/unit/test_servicenow_connector.py::test_servicenow_kb_metadata_and_version`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-SNOW-001 [P2] G2-SRC-SNOW-001: G2-SRC-SNOW-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:404-406` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-SNOW-001
Capture incident records and their affected services/CIs, assignment, severity, state, timestamps and linked records.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Capture incident records and their affected services/CIs, assignment, severity, state, timestamps and linked records.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:50`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L50-L50)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:47`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-SNOW-002 [P2] G2-SRC-SNOW-002: G2-SRC-SNOW-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:407-409` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-SNOW-002
Capture problem/RCA records and relationships to incidents and known errors.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Capture problem/RCA records and relationships to incidents and known errors.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:38`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L38-L38)
- tests: `tests/unit/test_servicenow_connector.py:26`, `tests/unit/test_servicenow_connector.py::test_servicenow_incident_extraction`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-SNOW-003 [P2] G2-SRC-SNOW-003: G2-SRC-SNOW-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:410-412` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-SNOW-003
Capture change requests, approvals, windows, implementation/backout plans and affected CIs/services.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Capture change requests, approvals, windows, implementation/backout plans and affected CIs/services.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:39`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L39-L39)
- tests: `tests/unit/test_servicenow_connector.py:45`, `tests/unit/test_servicenow_connector.py::test_servicenow_problem_extraction`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-SNOW-005 [P2] G2-SRC-SNOW-005: G2-SRC-SNOW-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:416-418` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-SNOW-005
Preserve state transitions as temporal events rather than only current status.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Preserve state transitions as temporal events rather than only current status.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:41`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L41-L41)
- tests: `tests/unit/test_servicenow_connector.py:81`, `tests/unit/test_servicenow_connector.py::test_servicenow_pagination_and_watermarks`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-SNOW-006 [P2] G2-SRC-SNOW-006: G2-SRC-SNOW-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:419-423` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-SNOW-006
Link changes/deployments/incidents using explicit source relationships and bounded temporal correlation.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Link changes/deployments/incidents using explicit source relationships and bounded temporal correlation.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:42`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L42-L42)
- tests: `tests/unit/test_servicenow_connector.py:99`, `tests/unit/test_servicenow_connector.py::test_servicenow_schema_drift`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-WEB-001 [P2] G2-SRC-WEB-001: G2-SRC-WEB-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:623-625` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-WEB-001
Support Markdown, text, HTML, JSON, YAML, XML, PDF and configured office/document formats when a safe parser exists.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Support Markdown, text, HTML, JSON, YAML, XML, PDF and configured office/document formats when a safe parser exists.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:51`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L51-L51)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:48`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-WEB-002 [P2] G2-SRC-WEB-002: G2-SRC-WEB-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:626-628` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-WEB-002
Implement controlled internal web crawling with explicit allowlists and bounds.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Implement controlled internal web crawling with explicit allowlists and bounds.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/inspect_tested_p2.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_tested_p2.py#L4-L4), [`scripts/update_phase2_wp23.py:43`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L43-L43)
- tests: `tests/unit/test_acquisition_fabric.py:181`, `tests/unit/test_acquisition_fabric.py::test_controlled_crawler_can_authorize_private_intranet_targets_explicitly`, `tests/unit/test_web_crawler_connector.py:13`, `tests/unit/test_web_crawler_connector.py::test_web_crawler_scope_and_allowlist_boundaries`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-WEB-003 [P2] G2-SRC-WEB-003: G2-SRC-WEB-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:629-631` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-WEB-003
Detect duplicate content by hash/canonical URL.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Detect duplicate content by hash/canonical URL.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:44`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L44-L44)
- tests: `tests/unit/test_web_crawler_connector.py:30`, `tests/unit/test_web_crawler_connector.py::test_web_crawler_html_structure_parsing`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-WEB-004 [P2] G2-SRC-WEB-004: G2-SRC-WEB-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:632-634` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-WEB-004
Retain link graph and document hierarchy.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Retain link graph and document hierarchy.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:45`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L45-L45)
- tests: `tests/unit/test_web_crawler_connector.py:66`, `tests/unit/test_web_crawler_connector.py::test_web_crawler_politeness_delay_and_rate_limiting`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-WEB-005 [P2] G2-SRC-WEB-005: G2-SRC-WEB-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:635-639` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-WEB-005
Never follow unconfigured external domains automatically.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Never follow unconfigured external domains automatically.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:46`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L46-L46)
- tests: `tests/unit/test_web_crawler_connector.py:101`, `tests/unit/test_web_crawler_connector.py::test_web_crawler_content_hashing_and_event_version`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SYNC-001 [P2] G2-SYNC-001: Baseline state

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:642-644` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SYNC-001 — Baseline state
Every source SHALL have a recorded baseline completion marker.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Every source SHALL have a recorded baseline completion marker.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:52`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L52-L52)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:49`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SYNC-002 [P2] G2-SYNC-002: Baseline snapshot

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:645-654` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SYNC-002 — Baseline snapshot
Baseline SHALL record:
- source scope,
- source version/cursor,
- started/finished times,
- counts,
- failures,
- mapping/parser versions,
- graph mutation counts.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Baseline SHALL record: - source scope, - source version/cursor, - started/finished times, - counts, - failures, - mapping/parser versions, - graph mutation counts.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L8-L8), [`scripts/update_wp22_registry.py:52`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L52-L52)
- tests: `tests/unit/test_acquisition_fabric.py:68`, `tests/unit/test_acquisition_fabric.py::test_baseline_controller_persists_ordered_restart_manifest`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SYNC-003 [P2] G2-SYNC-003: Delta processing

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:655-657` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SYNC-003 — Delta processing
Only changed records SHALL be reprocessed after baseline unless reconciliation requests otherwise.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Only changed records SHALL be reprocessed after baseline unless reconciliation requests otherwise.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L8-L8), [`scripts/update_wp22_registry.py:59`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L59-L59)
- tests: `tests/unit/test_semantic_consumers_reconciliation.py:104`, `tests/unit/test_semantic_consumers_reconciliation.py::test_reconciler_detects_and_repairs_missing_stale_and_orphaned_records`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SYNC-004 [P2] G2-SYNC-004: Delete/retire

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:658-660` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 13, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SYNC-004 — Delete/retire
Source deletion SHALL expire current graph assertions; historical revisions remain queryable.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Source deletion SHALL expire current graph assertions;
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L8-L8), [`scripts/update_wp22_registry.py:66`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L66-L66)
- tests: `tests/unit/test_graph_evolution.py:167`, `tests/unit/test_graph_evolution.py::test_deletion_is_a_temporal_barrier_for_entity_and_relationship_replay`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SYNC-005 [P2] G2-SYNC-005: Missed-event recovery

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:661-663` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SYNC-005 — Missed-event recovery
Reconciliation SHALL repair missed webhooks/events.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Missed-event recovery Reconciliation SHALL repair missed webhooks/events.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L8-L8), [`scripts/update_wp22_registry.py:73`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L73-L73)
- tests: `tests/unit/test_semantic_consumers_reconciliation.py:104`, `tests/unit/test_semantic_consumers_reconciliation.py::test_reconciler_detects_and_repairs_missing_stale_and_orphaned_records`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SYNC-006 [P2] G2-SYNC-006: Duplicate-event handling

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:664-666` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 13, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SYNC-006 — Duplicate-event handling
Duplicate events SHALL be safe.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Duplicate-event handling Duplicate events SHALL be safe.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L8-L8), [`scripts/update_wp22_registry.py:80`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L80-L80)
- tests: `tests/unit/test_graph_evolution.py:30`, `tests/unit/test_graph_evolution.py::test_entity_evolution_is_idempotent_temporal_and_late_event_safe`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SYNC-007 [P2] G2-SYNC-007: Late event handling

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:667-669` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 13, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SYNC-007 — Late event handling
Late events SHALL not incorrectly overwrite newer source versions.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Late events SHALL not incorrectly overwrite newer source versions.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L8-L8), [`scripts/update_wp22_registry.py:87`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L87-L87)
- tests: `tests/unit/test_graph_evolution.py:30`, `tests/unit/test_graph_evolution.py::test_entity_evolution_is_idempotent_temporal_and_late_event_safe`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SYNC-008 [P2] G2-SYNC-008: Dependency-aware update

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:670-672` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SYNC-008 — Dependency-aware update
When source A changes, only dependent derived relationships/retrieval indexes/summaries SHALL be invalidated/recomputed.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] When source A changes, only dependent derived relationships/retrieval indexes/summaries SHALL be invalidated/recomputed.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L9-L9), [`scripts/update_wp22_registry.py:94`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L94-L94)
- tests: `tests/unit/test_semantic_consumers_reconciliation.py:29`, `tests/unit/test_semantic_consumers_reconciliation.py::test_default_semantic_consumers_process_each_cursor_once`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SYNC-009 [P2] G2-SYNC-009: Consistency watermark

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:673-675` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 2, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SYNC-009 — Consistency watermark
Expose source consistency/freshness watermarks.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Consistency watermark Expose source consistency/freshness watermarks.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L9-L9), [`scripts/update_wp22_registry.py:101`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L101-L101)
- tests: `tests/unit/test_phase2_api.py:8`, `tests/unit/test_phase2_api.py::test_source_sync_admin_routes_enqueue_only_safe_sync_options`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SYNC-010 [P2] G2-SYNC-010: Full rebuild is exceptional

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:676-678` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SYNC-010 — Full rebuild is exceptional
Full rebuild SHALL be an explicit maintenance action, not normal sync behavior.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Full rebuild SHALL be an explicit maintenance action, not normal sync behavior.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L9-L9), [`scripts/update_wp22_registry.py:112`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L112-L112)
- tests: `tests/unit/test_acquisition_sync_semantics.py:26`, `tests/unit/test_acquisition_sync_semantics.py::test_full_rebuild_requires_explicit_maintenance_authorization`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SYNC-011 [P2] G2-SYNC-011: Rebuild equivalence test

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:679-681` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SYNC-011 — Rebuild equivalence test
For supported deterministic domains, replay/rebuild output SHALL be logically equivalent to incrementally maintained graph state.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] For supported deterministic domains, replay/rebuild output SHALL be logically equivalent to incrementally maintained graph state.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L9-L9), [`scripts/update_wp22_registry.py:119`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L119-L119)
- tests: `tests/unit/test_file_ingestion.py:39`, `tests/unit/test_file_ingestion.py::test_capture_graph_retrieval_and_idempotent_replay`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SYNC-012 [P2] G2-SYNC-012: Connector pause/resume

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:682-684` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SYNC-012 — Connector pause/resume
Operators SHALL pause a source without losing checkpoint.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Operators SHALL pause a source without losing checkpoint.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L9-L9), [`scripts/update_wp22_registry.py:126`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L126-L126)
- tests: `tests/unit/test_acquisition_fabric.py:34`, `tests/unit/test_acquisition_fabric.py::test_scheduler_admits_all_operation_types_and_enforces_controls`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SYNC-013 [P2] G2-SYNC-013: Backfill

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:685-687` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SYNC-013 — Backfill
A newly added mapping/entity type SHALL support bounded historical backfill without re-ingesting unrelated data.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] A newly added mapping/entity type SHALL support bounded historical backfill without re-ingesting unrelated data.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L9-L9), [`scripts/update_wp22_registry.py:133`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L133-L133)
- tests: `tests/unit/test_acquisition_sync_semantics.py:44`, `tests/unit/test_acquisition_sync_semantics.py::test_bounded_historical_backfill_submits_bounded_specification`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SYNC-014 [P2] G2-SYNC-014: Selective rescan

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:688-698` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SYNC-014 — Selective rescan
Support rescan by:
- entity type,
- path,
- repository,
- project,
- time range,
- source ID.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Support rescan by: - entity type, - path, - repository, - project, - time range, - source ID.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L9-L9), [`scripts/update_wp22_registry.py:140`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L140-L140)
- tests: `tests/unit/test_acquisition_sync_semantics.py:71`, `tests/unit/test_acquisition_sync_semantics.py::test_selective_rescan_submits_filters_by_criteria`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TEL-001 [P2] G2-TEL-001: G2-TEL-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1634-1636` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TEL-001
HugeGraph SHALL store semantic telemetry objects, not unlimited raw measurements.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] HugeGraph SHALL store semantic telemetry objects, not unlimited raw measurements.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:53`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L53-L53)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:50`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TEL-002 [P2] G2-TEL-002: G2-TEL-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1637-1639` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TEL-002
Every telemetry-derived relationship SHALL have observation window.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Every telemetry-derived relationship SHALL have observation window.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/telemetry/adapter.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/telemetry/adapter.py#L1-L1), [`scripts/_check_wp72.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L13-L13), [`scripts/_mark_wp72_done.py:84`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L84-L84)
- tests: `tests/unit/test_performance_reliability_and_operations_wp72.py:23`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_g2_tel_002_telemetry_derived_relationship_has_observation_window`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TEL-003 [P2] G2-TEL-003: G2-TEL-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1640-1642` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TEL-003
Every telemetry-derived relationship SHALL include source/evidence reference.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Every telemetry-derived relationship SHALL include source/evidence reference.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/telemetry/adapter.py:5`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/telemetry/adapter.py#L5-L5), [`scripts/_check_wp72.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L13-L13), [`scripts/_mark_wp72_done.py:88`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L88-L88)
- tests: `tests/unit/test_performance_reliability_and_operations_wp72.py:24`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_g2_tel_003_telemetry_relationship_includes_source_evidence_ref`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TEL-004 [P2] G2-TEL-004: G2-TEL-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1643-1645` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TEL-004
Use aggregation/fingerprints for repeated log patterns.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Use aggregation/fingerprints for repeated log patterns.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/telemetry/adapter.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/telemetry/adapter.py#L6-L6), [`scripts/_check_wp72.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L13-L13), [`scripts/_mark_wp72_done.py:92`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L92-L92)
- tests: `tests/unit/test_performance_reliability_and_operations_wp72.py:25`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_g2_tel_004_aggregation_fingerprints_for_repeated_logs`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TEL-005 [P2] G2-TEL-005: G2-TEL-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1646-1648` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TEL-005
Preserve bounded exemplar IDs/trace IDs where permitted.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Preserve bounded exemplar IDs/trace IDs where permitted.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/telemetry/adapter.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/telemetry/adapter.py#L7-L7), [`scripts/_check_wp72.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L13-L13), [`scripts/_mark_wp72_done.py:96`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L96-L96)
- tests: `tests/unit/test_performance_reliability_and_operations_wp72.py:26`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_g2_tel_005_preserve_bounded_exemplar_trace_ids`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TEL-006 [P2] G2-TEL-006: G2-TEL-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1649-1651` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TEL-006
Support configurable retention for derived telemetry facts.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Support configurable retention for derived telemetry facts.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/telemetry/adapter.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/telemetry/adapter.py#L8-L8), [`scripts/_check_wp72.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L13-L13), [`scripts/_mark_wp72_done.py:100`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L100-L100)
- tests: `tests/unit/test_performance_reliability_and_operations_wp72.py:27`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_g2_tel_006_configurable_retention_for_derived_facts`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TEL-007 [P2] G2-TEL-007: G2-TEL-007

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1652-1654` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TEL-007
A runtime edge SHALL expire when no longer observed under configured policy.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] A runtime edge SHALL expire when no longer observed under configured policy.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/telemetry/adapter.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/telemetry/adapter.py#L8-L8), [`scripts/_check_wp72.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L13-L13), [`scripts/_mark_wp72_done.py:104`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L104-L104)
- tests: `tests/unit/test_performance_reliability_and_operations_wp72.py:28`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_g2_tel_007_runtime_edge_expires_under_policy`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TEL-008 [P2] G2-TEL-008: G2-TEL-008

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1655-1659` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TEL-008
Do not confuse “not observed” with “does not exist”; confidence/coverage SHALL be explicit.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Do not confuse “not observed” with “does not exist”; confidence/coverage SHALL be explicit.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/telemetry/adapter.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/telemetry/adapter.py#L9-L9), [`scripts/_check_wp72.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L13-L13), [`scripts/_mark_wp72_done.py:108`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L108-L108)
- tests: `tests/unit/test_performance_reliability_and_operations_wp72.py:29`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_g2_tel_008_explicit_confidence_coverage_status`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TIME-001 [P2] G2-TIME-001: G2-TIME-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1042-1044` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TIME-001
GUI SHALL provide a temporal state selector for supported domains.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] GUI SHALL provide a temporal state selector for supported domains.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:54`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L54-L54)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:51`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TIME-002 [P2] G2-TIME-002: G2-TIME-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1045-1047` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TIME-002
Support “state as of T”.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Support “state as of T”.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:194`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L194-L194)
- tests: `tests/unit/test_temporal_model_family.py:93`, `tests/unit/test_temporal_model_family.py::test_time_machine_state_as_of_t`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TIME-003 [P2] G2-TIME-003: G2-TIME-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1048-1050` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TIME-003
Support compare T1 vs T2.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Support compare T1 vs T2.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:200`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L200-L200)
- tests: `tests/unit/test_temporal_model_family.py:110`, `tests/unit/test_temporal_model_family.py::test_time_machine_compare_t1_vs_t2`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TIME-004 [P2] G2-TIME-004: G2-TIME-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1051-1053` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TIME-004
Highlight semantic additions/removals/changes.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Highlight semantic additions/removals/changes.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:206`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L206-L206)
- tests: `tests/unit/test_temporal_model_family.py:121`, `tests/unit/test_temporal_model_family.py::test_time_machine_highlights_semantic_changes`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TIME-005 [P2] G2-TIME-005: G2-TIME-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1054-1056` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TIME-005
Support release-based snapshots.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Support release-based snapshots.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:212`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L212-L212)
- tests: `tests/unit/test_temporal_model_family.py:134`, `tests/unit/test_temporal_model_family.py::test_release_based_snapshots`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TIME-006 [P2] G2-TIME-006: G2-TIME-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1057-1059` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TIME-006
Time travel SHALL include ontology/schema version context.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Time travel SHALL include ontology/schema version context.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:218`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L218-L218)
- tests: `tests/unit/test_temporal_model_family.py:143`, `tests/unit/test_temporal_model_family.py::test_time_travel_schema_version_context`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

