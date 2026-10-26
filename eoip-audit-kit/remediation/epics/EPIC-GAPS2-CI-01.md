# EPIC-GAPS2-CI-01: EOIP-engg-doc-pkg/gaps2-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 60 tasks, ~30.0 h, priorities {'P0': 14, 'P1': 28, 'P2': 18}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-G2-EKAF-004 [P0] G2-EKAF-004: Baseline crawl

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:204-206` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-004 — Baseline crawl
A source SHALL support an initial full authorized baseline extraction where technically possible.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] A source SHALL support an initial full authorized baseline extraction where technically possible.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L9-L9)
- tests: `tests/unit/test_acquisition_fabric.py:68`, `tests/unit/test_acquisition_fabric.py::test_baseline_controller_persists_ordered_restart_manifest`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-020 [P0] G2-EKAF-020: Authentication isolation

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:287-289` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-020 — Authentication isolation
Secrets SHALL never be embedded in connector configuration artifacts.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Secrets SHALL never be embedded in connector configuration artifacts.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L11-L11)
- tests: `tests/unit/test_acquisition_fabric.py:87`, `tests/unit/test_acquisition_fabric.py::test_webhook_gateway_authenticates_persists_and_deduplicates_before_processing`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-030 [P0] G2-EKAF-030: Source onboarding wizard

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:340-345` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-030 — Source onboarding wizard
Admin GUI SHALL guide:
`connect → authenticate → scope → discover → preview → map → dry run → validate → baseline`.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Admin GUI SHALL guide: connect → authenticate → scope → discover → preview → map → dry run → validate → baseline.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L12-L12)
- tests: `tests/unit/test_acquisition_fabric.py:325`, `tests/unit/test_acquisition_fabric.py::test_source_operation_api_queues_registry_scoped_job`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SEC-CRAWL-001 [P0] G2-SEC-CRAWL-001: G2-SEC-CRAWL-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1662-1664` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SEC-CRAWL-001
SSRF protection for crawlers/connectors.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): SSRF protection for crawlers/connectors.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:33`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L33-L33)
- tests: `tests/unit/test_acquisition_fabric.py:165`, `tests/unit/test_acquisition_fabric.py::test_controlled_crawler_rejects_private_dns_resolution`, `tests/unit/test_g2_readiness.py:30`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SEC-CRAWL-004 [P0] G2-SEC-CRAWL-004: G2-SEC-CRAWL-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1671-1673` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SEC-CRAWL-004
Secret/credential redaction in logs.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Secret/credential redaction in logs.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/security/test_crawler_security.py:53`, `tests/security/test_crawler_security.py::test_crawler_secret_redaction_in_logs`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SEC-CRAWL-006 [P0] G2-SEC-CRAWL-006: G2-SEC-CRAWL-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1677-1679` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SEC-CRAWL-006
Untrusted document parsing SHALL be sandboxed/isolated where practical.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Untrusted document parsing SHALL be sandboxed/isolated where practical.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/security/test_crawler_security.py:78`, `tests/security/test_crawler_security.py::test_untrusted_document_parsing_is_quarantined_and_isolated`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SEC-CRAWL-009 [P0] G2-SEC-CRAWL-009: G2-SEC-CRAWL-009

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1686-1688` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SEC-CRAWL-009
Prompt-injection content SHALL be tagged as data, not instructions to agents.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Prompt-injection content SHALL be tagged as data, not instructions to agents.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/security/test_crawler_security.py:122`, `tests/security/test_crawler_security.py::test_prompt_injection_tagged_as_data_not_instruction`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SEC-CRAWL-011 [P0] G2-SEC-CRAWL-011: G2-SEC-CRAWL-011

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1692-1694` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SEC-CRAWL-011
Source credentials SHALL use minimum required permissions.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Source credentials SHALL use minimum required permissions.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/security/test_crawler_security.py:153`, `tests/security/test_crawler_security.py::test_source_credentials_use_minimum_permissions`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-DD-001 [P0] G2-SRC-DD-001: G2-SRC-DD-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:526-528` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-DD-001
Capture configured services, service dependencies, dashboards, monitors, SLO metadata, APM/service catalog metadata and bounded log/trace evidence where authorized.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Capture configured services, service dependencies, dashboards, monitors, SLO metadata, APM/service catalog metadata and bounded log/trace evidence where authorized.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:40`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L40-L40)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:37`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-GL-001 [P0] G2-SRC-GL-001: G2-SRC-GL-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:442-444` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-GL-001
Capture groups/projects, repositories, branches, tags, commits, merge requests, issues/work items, pipelines, jobs, artifacts metadata, releases and wiki/pages metadata where authorized.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Capture groups/projects, repositories, branches, tags, commits, merge requests, issues/work items, pipelines, jobs, artifacts metadata, releases and wiki/pages metadata where authorized.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:42`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L42-L42), [`packages/eoip/ingestion/gitlab_rest.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ingestion/gitlab_rest.py#L1-L1), [`scripts/tick_phase2_batch1.py:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L16-L16)
- tests: `tests/unit/test_g2_readiness.py:39`, `tests/unit/test_gitlab_connector.py:25`, `tests/unit/test_gitlab_connector.py::test_gitlab_baseline_emits_repository_delivery_and_knowledge_events`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-JIRA-001 [P0] G2-SRC-JIRA-001: G2-SRC-JIRA-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:350-352` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-JIRA-001
Capture projects, issue types, epics, stories, tasks, bugs, subtasks, sprints, statuses, labels, links, users, comments and changelog where authorized.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Capture projects, issue types, epics, stories, tasks, bugs, subtasks, sprints, statuses, labels, links, users, comments and changelog where authorized.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:44`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L44-L44), [`packages/eoip/ingestion/jira_rest.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ingestion/jira_rest.py#L1-L1)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:41`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-KIB-001 [P0] G2-SRC-KIB-001: G2-SRC-KIB-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:500-502` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-KIB-001
Capture configured dashboard/saved-object/data-view metadata through supported APIs/export mechanisms where authorized.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Capture configured dashboard/saved-object/data-view metadata through supported APIs/export mechanisms where authorized.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:45`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L45-L45)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:42`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-RUNTIME-001 [P0] G2-SRC-RUNTIME-001: G2-SRC-RUNTIME-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:592-594` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-RUNTIME-001
Capture images, containers/workloads, namespaces, deployments, services, config references and environment metadata where authorized.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Capture images, containers/workloads, namespaces, deployments, services, config references and environment metadata where authorized.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/connectors/runtime_infra.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/runtime_infra.py#L1-L1), [`packages/eoip/gaps/g2_readiness.py:47`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L47-L47)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:44`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-SNOW-004 [P0] G2-SRC-SNOW-004: G2-SRC-SNOW-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:413-415` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-SNOW-004
Capture authorized CMDB CIs and relationships for topology enrichment.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Capture authorized CMDB CIs and relationships for topology enrichment.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase2_wp23.py:40`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L40-L40)
- tests: `tests/unit/test_servicenow_connector.py:63`, `tests/unit/test_servicenow_connector.py::test_servicenow_change_request_extraction`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ARCHC-003 [P1] G2-ARCHC-003: G2-ARCHC-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1116-1122` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCHC-003
Rule examples:
- UI MUST_NOT_ACCESS database directly.
- Domain A MUST_NOT_DEPEND_ON Domain B.
- Critical API MUST have owner and tests.
- Regulated data MUST_NOT cross boundary X.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Critical API MUST have owner and tests.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:19`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L19-L19)
- tests: `tests/unit/test_conformance.py:18`, `tests/unit/test_conformance.py::test_parse_rules_with_severity_and_depth`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-001 [P1] G2-EKAF-001: Source Registry

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:155-174` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-001 — Source Registry
Maintain a registry containing:
- source ID,
- source type,
- base endpoint,
- acquisition modes,
- credentials reference,
- allowed scopes,
- excluded scopes,
- polling frequency,
- webhook status,
- mapping version,
- parser version,
- checkpoint,
- last successful baseline,
- last incremental run,
- reconciliation schedule,
- health,
- freshness SLO.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Source Registry Maintain a registry containing: - source ID, - source type, - base endpoint, - acquisition modes, - credentials reference, - allowed scopes, - excluded scopes, - polling frequency, - webhook status, - mapping version, - parser version, - checkpoint, - last successful baseline, - last incremental run, - reconciliation schedule, - health, - freshness SLO.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L12-L12)
- tests: `tests/unit/test_acquisition_fabric.py:284`, `tests/unit/test_acquisition_fabric.py::test_generic_web_and_file_connectors_share_source_connector_semantics`, `tests/unit/test_g2_readiness.py:9`, `tests/unit/test_source_registry.py:52`, `tests/unit/test_source_registry.py::test_registry_entry_carries_g2_operational_metadata_without_secrets`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-003 [P1] G2-EKAF-003: SourceEvent envelope

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:187-203` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-003 — SourceEvent envelope
Every acquired unit SHALL be emitted as a versioned `SourceEvent` with:
- event_id,
- source_id,
- source_type,
- source_record_id,
- source_record_type,
- operation,
- event_time,
- observed_time,
- cursor/checkpoint,
- content_hash,
- source_version,
- payload/evidence reference,
- permissions metadata when applicable,
- correlation/run ID.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Every acquired unit SHALL be emitted as a versioned SourceEvent with: - event_id, - source_id, - source_type, - source_record_id, - source_record_type, - operation, - event_time, - observed_time, - cursor/checkpoint, - content_hash, - source_version, - payload/evidence reference, - permissions metadata when applicable, - correlation/run ID.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/inspect_tested_p2.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_tested_p2.py#L4-L4), [`scripts/inspect_wp21_reqs.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_reqs.py#L9-L9), [`scripts/inspect_wp21_tasks.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_tasks.py#L6-L6), [`scripts/read_g2_specs.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_g2_specs.py#L7-L7), [`scripts/update_wp21_registry.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp21_registry.py#L10-L10)
- tests: `tests/contract/test_g2_contracts.py:47`, `tests/contract/test_g2_contracts.py::test_v2_event_exposes_g2_envelope_aliases`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-005 [P1] G2-EKAF-005: Incremental sync

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:207-214` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-005 — Incremental sync
After baseline, EOIP SHALL ingest only:
- newly created records,
- changed records,
- deleted/archived records,
- relationship changes,
- permission changes where supported.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] After baseline, EOIP SHALL ingest only: - newly created records, - changed records, - deleted/archived records, - relationship changes, - permission changes where supported.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L9-L9)
- tests: `tests/unit/test_acquisition_fabric.py:34`, `tests/unit/test_acquisition_fabric.py::test_scheduler_admits_all_operation_types_and_enforces_controls`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-006 [P1] G2-EKAF-006: Webhook/event ingestion

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:215-217` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-006 — Webhook/event ingestion
Connectors that support events SHALL ingest them through a durable local event endpoint.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Connectors that support events SHALL ingest them through a durable local event endpoint.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L9-L9)
- tests: `tests/unit/test_acquisition_fabric.py:87`, `tests/unit/test_acquisition_fabric.py::test_webhook_gateway_authenticates_persists_and_deduplicates_before_processing`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-009 [P1] G2-EKAF-009: Idempotency

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:224-226` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-009 — Idempotency
Repeated delivery of the same source event SHALL NOT create duplicate canonical facts.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Repeated delivery of the same source event SHALL NOT create duplicate canonical facts.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L10-L10)
- tests: `tests/unit/test_acquisition_fabric.py:87`, `tests/unit/test_acquisition_fabric.py::test_webhook_gateway_authenticates_persists_and_deduplicates_before_processing`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-023 [P1] G2-EKAF-023: Permission-aware metadata

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:304-306` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-023 — Permission-aware metadata
Where supported, preserve source visibility/security metadata for future enforcement.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Where supported, preserve source visibility/security metadata for future enforcement.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/inspect_wp21_reqs.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_reqs.py#L10-L10), [`scripts/inspect_wp21_tasks.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_tasks.py#L6-L6), [`scripts/read_g2_specs.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_g2_specs.py#L8-L8), [`scripts/update_wp21_registry.py:38`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp21_registry.py#L38-L38)
- tests: `tests/contract/test_g2_contracts.py:14`, `tests/contract/test_g2_contracts.py::test_v1_source_event_upgrade_preserves_identity_and_hash`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVENT-002 [P1] G2-EVENT-002: G2-EVENT-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:835-837` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EVENT-002
Events SHALL be emitted only after durable graph mutation state is known.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Events SHALL be emitted only after durable graph mutation state is known.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L7-L7), [`scripts/update_wp22_registry.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L10-L10)
- tests: `tests/unit/test_semantic_consumers_reconciliation.py:29`, `tests/unit/test_semantic_consumers_reconciliation.py::test_default_semantic_consumers_process_each_cursor_once`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVENT-003 [P1] G2-EVENT-003: G2-EVENT-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:838-840` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EVENT-003
Consumers SHALL be idempotent.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Consumers SHALL be idempotent.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L7-L7), [`scripts/update_wp22_registry.py:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L17-L17)
- tests: `tests/unit/test_semantic_consumers_reconciliation.py:29`, `tests/unit/test_semantic_consumers_reconciliation.py::test_default_semantic_consumers_process_each_cursor_once`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVENT-006 [P1] G2-EVENT-006: G2-EVENT-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:855-857` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EVENT-006
Consumer failures SHALL not corrupt authoritative graph state.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Consumer failures SHALL not corrupt authoritative graph state.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L7-L7), [`scripts/update_wp22_registry.py:38`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L38-L38)
- tests: `tests/unit/test_semantic_consumers_reconciliation.py:67`, `tests/unit/test_semantic_consumers_reconciliation.py::test_consumer_failure_does_not_corrupt_graph_state`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVOL-015 [P1] G2-EVOL-015: G2-EVOL-015

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:758-760` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-EVOL-015
Provide rollback/replay strategy for mapping defects.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Provide rollback/replay strategy for mapping defects.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:116`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L116-L116)
- tests: `tests/unit/test_graph_evolution_family.py:224`, `tests/unit/test_graph_evolution_family.py::test_rollback_and_replay_strategy`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-SEC-001 [P1] G2-GRAPH-SEC-001: G2-GRAPH-SEC-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:922-924` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-SEC-001
Represent package/version/dependency/SBOM/vulnerability/artifact/service relationships.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Represent package/version/dependency/SBOM/vulnerability/artifact/service relationships.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:21`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L21-L21), [`packages/eoip/graph/security_graph.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/security_graph.py#L1-L1)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:18`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-SEC-002 [P1] G2-GRAPH-SEC-002: G2-GRAPH-SEC-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:925-927` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-SEC-002
Support blast radius from package/CVE to deployed services.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Support blast radius from package/CVE to deployed services.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/security_graph.py:19`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/security_graph.py#L19-L19), [`scripts/_mark_wp44_done.py:42`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L42-L42)
- tests: `tests/unit/test_g2_domain_graphs.py:288`, `tests/unit/test_g2_domain_graphs.py::test_g2_graph_sec_002_vulnerability_blast_radius`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-SEC-003 [P1] G2-GRAPH-SEC-003: G2-GRAPH-SEC-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:928-932` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-SEC-003
Preserve scanner/evidence provenance.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Preserve scanner/evidence provenance.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/security_graph.py:21`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/security_graph.py#L21-L21), [`scripts/_mark_wp44_done.py:43`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L43-L43)
- tests: `tests/unit/test_g2_domain_graphs.py:308`, `tests/unit/test_g2_domain_graphs.py::test_g2_graph_sec_003_preserve_scanner_provenance`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-REL-006 [P1] G2-REL-006: G2-REL-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1778-1780` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-REL-006
Backup SHALL include graph state plus metadata required for synchronization continuity.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Backup SHALL include graph state plus metadata required for synchronization continuity.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_check_wp72.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L11-L11), [`scripts/_mark_wp72_done.py:56`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L56-L56)
- tests: `tests/unit/test_performance_reliability_and_operations_wp72.py:16`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_g2_rel_006_backup_includes_graph_and_sync_metadata`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-REL-007 [P1] G2-REL-007: G2-REL-007

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1781-1783` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 86, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-REL-007
Restore SHALL preserve/restore connector checkpoints consistently.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Restore SHALL preserve/restore connector checkpoints consistently.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_check_wp72.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L11-L11), [`scripts/_mark_wp72_done.py:60`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L60-L60)
- tests: `tests/unit/test_operational_recovery.py:36`, `tests/unit/test_operational_recovery.py::test_operational_recovery_preserves_state_and_holds_active_jobs`, `tests/unit/test_performance_reliability_and_operations_wp72.py:17`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_g2_rel_007_restore_preserves_checkpoints`, `tests/unit/test_recovery_bundle.py:48`, `tests/unit/test_recovery_bundle.py::test_bundle_restores_actual_weights_configuration_and_graph`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-REL-008 [P1] G2-REL-008: G2-REL-008

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1784-1788` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-REL-008
A restore procedure SHALL document whether events after backup must be replayed.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] A restore procedure SHALL document whether events after backup must be replayed.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/recovery/webhook_reliability.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/recovery/webhook_reliability.py#L1-L1), [`scripts/_check_wp72.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L11-L11), [`scripts/_mark_wp72_done.py:64`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L64-L64)
- tests: `tests/unit/test_performance_reliability_and_operations_wp72.py:18`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_g2_rel_008_restore_procedure_documents_event_replay`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SEC-CRAWL-002 [P1] G2-SEC-CRAWL-002: G2-SEC-CRAWL-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1665-1667` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 23, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SEC-CRAWL-002
Strict target allowlist.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Strict target allowlist.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/inspect_tested_p2.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_tested_p2.py#L4-L4)
- tests: `tests/security/test_crawler_security.py:1`, `tests/security/test_crawler_security.py::test_crawler_strict_target_allowlist`, `tests/unit/test_acquisition_fabric.py:165`, `tests/unit/test_acquisition_fabric.py::test_controlled_crawler_can_authorize_private_intranet_targets_explicitly`, `tests/unit/test_acquisition_fabric.py::test_controlled_crawler_rejects_private_dns_resolution`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SEC-CRAWL-003 [P1] G2-SEC-CRAWL-003: G2-SEC-CRAWL-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1668-1670` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SEC-CRAWL-003
No automatic Internet traversal.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): No automatic Internet traversal.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/security/test_crawler_security.py:35`, `tests/security/test_crawler_security.py::test_crawler_blocks_automatic_internet_traversal`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SEC-CRAWL-005 [P1] G2-SEC-CRAWL-005: G2-SEC-CRAWL-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1674-1676` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SEC-CRAWL-005
TLS validation configurable but secure by default.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): TLS validation configurable but secure by default.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/security/test_crawler_security.py:67`, `tests/security/test_crawler_security.py::test_crawler_tls_validation_secure_by_default`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SEC-CRAWL-007 [P1] G2-SEC-CRAWL-007: G2-SEC-CRAWL-007

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1680-1682` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SEC-CRAWL-007
Content-size/decompression limits.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Content-size/decompression limits.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/security/test_crawler_security.py:91`, `tests/security/test_crawler_security.py::test_crawler_content_size_limits`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SEC-CRAWL-008 [P1] G2-SEC-CRAWL-008: G2-SEC-CRAWL-008

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1683-1685` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SEC-CRAWL-008
Archive/bomb protection.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Archive/bomb protection.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/security/test_crawler_security.py:112`, `tests/security/test_crawler_security.py::test_crawler_archive_bomb_protection`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SEC-CRAWL-010 [P1] G2-SEC-CRAWL-010: G2-SEC-CRAWL-010

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1689-1691` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SEC-CRAWL-010
Crawler actions SHALL be read-only unless a separate explicitly approved action connector exists.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Crawler actions SHALL be read-only unless a separate explicitly approved action connector exists.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/security/test_crawler_security.py:138`, `tests/security/test_crawler_security.py::test_crawler_actions_are_read_only`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SEC-CRAWL-012 [P1] G2-SEC-CRAWL-012: G2-SEC-CRAWL-012

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1695-1699` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SEC-CRAWL-012
All outbound source access SHALL be auditable.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] All outbound source access SHALL be auditable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/security/test_crawler_security.py:167`, `tests/security/test_crawler_security.py::test_all_outbound_source_access_is_auditable`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SIM-002 [P1] G2-SIM-002: G2-SIM-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1070-1072` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SIM-002
Apply hypothetical mutations without touching authoritative graph.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Apply hypothetical mutations without touching authoritative graph.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_check_wp62.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp62.py#L11-L11), [`scripts/_find_specs.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_find_specs.py#L7-L7), [`scripts/_mark_wp62_done.py:92`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp62_done.py#L92-L92)
- tests: `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:25`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py::test_g2_sim_002_hypothetical_mutations_without_base_mutation`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-SRC-CONF-001 [P1] G2-SRC-CONF-001: G2-SRC-CONF-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:372-374` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 23, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-SRC-CONF-001
Capture spaces, pages, page hierarchy, versions, labels, links, attachments, authors/editors and timestamps.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Capture spaces, pages, page hierarchy, versions, labels, links, attachments, authors/editors and timestamps.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:39`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L39-L39)
- tests: `tests/runtime_dlq/test_confluence_acquisition.py:8`, `tests/unit/test_confluence_metadata.py:45`, `tests/unit/test_confluence_metadata.py::test_acquisition_completes_truncated_labels_without_following_remote_links`, `tests/unit/test_confluence_metadata.py::test_invalid_page_metadata_is_captured_and_rejected_before_document_writes[history-value6]`, `tests/unit/test_confluence_metadata.py::test_invalid_page_metadata_is_captured_and_rejected_before_document_writes[history-value7]`, `tests/unit/test_confluence_metadata.py::test_invalid_page_metadata_is_captured_and_rejected_before_document_writes[history-value8]`, `tests/unit/test_confluence_metadata.py::test_invalid_page_metadata_is_captured_and_rejected_before_document_writes[metadata-value0]`, `tests/unit/test_confluence_metadata.py::test_invalid_page_metadata_is_captured_and_rejected_before_document_writes[metadata-value1]`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-PLAY-002 [P1] G2-UX-PLAY-002: G2-UX-PLAY-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1529-1537` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-PLAY-002
Playback SHALL synchronize:
- deployment,
- topology,
- alerts,
- error signatures,
- incidents,
- rollback/recovery.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Playback SHALL synchronize: - deployment, - topology, - alerts, - error signatures, - incidents, - rollback/recovery.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:266`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L266-L266)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:9`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_play_002_playback_synchronization`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-VSC-005 [P1] G2-VSC-005: G2-VSC-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1618-1620` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-VSC-005
Display relevant incidents/error signatures.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Display relevant incidents/error signatures.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_find_vsc_specs.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_find_vsc_specs.py#L14-L14), [`scripts/_inspect_vsc_reqs.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_inspect_vsc_reqs.py#L6-L6), [`scripts/_mark_wp54_and_wp55_done.py:41`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp54_and_wp55_done.py#L41-L41)
- tests: `tests/unit/test_vscode_extension_wp54.py:9`, `tests/unit/test_vscode_extension_wp54.py::test_g2_vsc_005_relevant_incidents`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ADMIN-001 [P2] G2-ADMIN-001: G2-ADMIN-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1551-1553` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ADMIN-001
Source Registry management.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Source Registry management.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/admin/index.jsx:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/index.jsx#L16-L16), [`packages/eoip/gaps/g2_readiness.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L7-L7)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:4`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ADMIN-002 [P2] G2-ADMIN-002: G2-ADMIN-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1554-1556` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ADMIN-002
Connector setup wizard.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Connector setup wizard.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/admin/ConnectorSetupWizard.jsx:60`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/ConnectorSetupWizard.jsx#L60-L60), [`apps/web/src/admin/index.jsx:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/index.jsx#L17-L17), [`scripts/_mark_wp53_done.py:68`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L68-L68)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:6`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_admin_002_connector_wizard`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ADMIN-003 [P2] G2-ADMIN-003: G2-ADMIN-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1557-1559` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ADMIN-003
Baseline/incremental/reconciliation status.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Baseline/incremental/reconciliation status.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/admin/IngestionReconciliationPanel.jsx:51`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/IngestionReconciliationPanel.jsx#L51-L51), [`apps/web/src/admin/index.jsx:18`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/index.jsx#L18-L18), [`scripts/_mark_wp53_done.py:74`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L74-L74)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:151`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_admin_003_reconciliation_status`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ADMIN-004 [P2] G2-ADMIN-004: G2-ADMIN-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1560-1562` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ADMIN-004
Checkpoint viewer.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Checkpoint viewer.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/admin/CheckpointAndRecoveryPanel.jsx:64`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/CheckpointAndRecoveryPanel.jsx#L64-L64), [`apps/web/src/admin/index.jsx:19`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/index.jsx#L19-L19), [`scripts/_mark_wp53_done.py:80`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L80-L80)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:156`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_admin_004_checkpoint_viewer`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ADMIN-005 [P2] G2-ADMIN-005: G2-ADMIN-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1563-1565` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ADMIN-005
DLQ/replay console.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): DLQ/replay console.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/admin/CheckpointAndRecoveryPanel.jsx:64`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/CheckpointAndRecoveryPanel.jsx#L64-L64), [`apps/web/src/admin/index.jsx:19`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/index.jsx#L19-L19), [`scripts/_mark_wp53_done.py:86`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L86-L86)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:161`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_admin_005_dlq_replay_console`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ADMIN-006 [P2] G2-ADMIN-006: G2-ADMIN-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1566-1568` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ADMIN-006
Schema/mapping drift console.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Schema/mapping drift console.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/admin/SchemaDriftAndFreshnessPanel.jsx:32`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/SchemaDriftAndFreshnessPanel.jsx#L32-L32), [`apps/web/src/admin/index.jsx:20`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/index.jsx#L20-L20), [`scripts/_mark_wp53_done.py:92`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L92-L92)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:166`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_admin_006_schema_drift_console`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ADMIN-007 [P2] G2-ADMIN-007: G2-ADMIN-007

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1569-1571` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ADMIN-007
Source freshness/lag dashboard.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Source freshness/lag dashboard.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/admin/SchemaDriftAndFreshnessPanel.jsx:32`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/SchemaDriftAndFreshnessPanel.jsx#L32-L32), [`apps/web/src/admin/index.jsx:20`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/index.jsx#L20-L20), [`scripts/_mark_wp53_done.py:98`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L98-L98)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:171`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_admin_007_source_freshness_dashboard`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ADMIN-008 [P2] G2-ADMIN-008: G2-ADMIN-008

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1572-1574` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ADMIN-008
Graph version timeline.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Graph version timeline.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/admin/GraphTimelineAndJournalPanel.jsx:35`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/GraphTimelineAndJournalPanel.jsx#L35-L35), [`apps/web/src/admin/index.jsx:21`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/index.jsx#L21-L21), [`scripts/_mark_wp53_done.py:104`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L104-L104)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:176`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_admin_008_graph_version_timeline`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ADMIN-009 [P2] G2-ADMIN-009: G2-ADMIN-009

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1575-1577` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ADMIN-009
Semantic Change Journal viewer.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Semantic Change Journal viewer.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/admin/GraphTimelineAndJournalPanel.jsx:68`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/GraphTimelineAndJournalPanel.jsx#L68-L68), [`scripts/_mark_wp53_done.py:110`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L110-L110)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:181`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_admin_009_semantic_change_journal`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ADMIN-010 [P2] G2-ADMIN-010: G2-ADMIN-010

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1578-1580` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ADMIN-010
Semantic event consumer health.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Semantic event consumer health.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/admin/GraphTimelineAndJournalPanel.jsx:82`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/GraphTimelineAndJournalPanel.jsx#L82-L82), [`scripts/_mark_wp53_done.py:116`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L116-L116)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:186`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_admin_010_event_consumer_health`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ADMIN-011 [P2] G2-ADMIN-011: G2-ADMIN-011

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1581-1583` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ADMIN-011
Source-to-ontology mapping preview.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Source-to-ontology mapping preview.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/admin/index.jsx:22`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/index.jsx#L22-L22), [`scripts/_mark_wp53_done.py:122`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L122-L122)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:191`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_admin_011_mapping_preview`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ADMIN-012 [P2] G2-ADMIN-012: G2-ADMIN-012

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1584-1586` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ADMIN-012
Crawl-scope safety preview.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Crawl-scope safety preview.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:128`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L128-L128)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:196`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_admin_012_crawl_safety_preview`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ADMIN-013 [P2] G2-ADMIN-013: G2-ADMIN-013

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1587-1589` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ADMIN-013
Telemetry semantic extraction controls.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Telemetry semantic extraction controls.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:134`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L134-L134)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:201`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_admin_013_telemetry_extraction_controls`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ADMIN-014 [P2] G2-ADMIN-014: G2-ADMIN-014

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1590-1592` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ADMIN-014
Knowledge SLO management.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Knowledge SLO management.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/admin/KnowledgeGovernanceAndSLOPanel.jsx:39`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/KnowledgeGovernanceAndSLOPanel.jsx#L39-L39), [`apps/web/src/admin/index.jsx:23`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/index.jsx#L23-L23), [`scripts/_mark_wp53_done.py:140`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L140-L140)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:206`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_admin_014_knowledge_slo_management`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ADMIN-015 [P2] G2-ADMIN-015: G2-ADMIN-015

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1593-1595` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ADMIN-015
Knowledge Debt dashboard.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Knowledge Debt dashboard.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/admin/KnowledgeGovernanceAndSLOPanel.jsx:86`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/KnowledgeGovernanceAndSLOPanel.jsx#L86-L86), [`scripts/_mark_wp53_done.py:146`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L146-L146)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:211`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_admin_015_knowledge_debt_dashboard`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ADMIN-016 [P2] G2-ADMIN-016: G2-ADMIN-016

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1596-1598` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ADMIN-016
Ontology evolution proposal review.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Ontology evolution proposal review.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/admin/KnowledgeGovernanceAndSLOPanel.jsx:100`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/KnowledgeGovernanceAndSLOPanel.jsx#L100-L100), [`scripts/_mark_wp53_done.py:152`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L152-L152)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:216`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_admin_016_ontology_evolution_proposals`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ADMIN-017 [P2] G2-ADMIN-017: G2-ADMIN-017

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1599-1603` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 48, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ADMIN-017
Simulation workspace manager.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Simulation workspace manager.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/admin/KnowledgeGovernanceAndSLOPanel.jsx:114`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/KnowledgeGovernanceAndSLOPanel.jsx#L114-L114), [`scripts/_mark_wp53_done.py:158`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L158-L158)
- tests: `tests/unit/test_g2_readiness.py:100`, `tests/unit/test_web_ux_and_admin_wp53.py:221`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_admin_017_simulation_workspace_manager`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ARCH-007 [P2] G2-ARCH-007: No destructive history overwrite

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:84-87` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 32, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCH-007 — No destructive history overwrite

Changes SHALL close/expire old facts and create new revisions rather than silently destroying historical enterprise knowledge.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Changes SHALL close/expire old facts and create new revisions rather than silently destroying historical enterprise knowledge.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_architecture.py:77`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_architecture.py#L77-L77)
- tests: `tests/unit/test_confluence_body.py:138`, `tests/unit/test_confluence_body.py::test_body_removal_clears_current_structure_without_destroying_history`, `tests/unit/test_confluence_metadata.py:92`, `tests/unit/test_confluence_metadata.py::test_metadata_persists_in_revisions_clears_on_update_and_is_replay_stable`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

