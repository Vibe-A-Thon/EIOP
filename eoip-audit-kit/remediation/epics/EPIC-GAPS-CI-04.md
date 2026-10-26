# EPIC-GAPS-CI-04: EOIP-engg-doc-pkg/gaps-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 60 tasks, ~30.5 h, priorities {'P2': 60}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-GAP-LIN-001 [P2] GAP-LIN-001: Map internal lineage to OpenLineage concepts where applicable

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:791-791` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-LIN-001:** Map internal lineage to OpenLineage concepts where applicable.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Map internal lineage to OpenLineage concepts where applicable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/future_scope.py:60`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/future_scope.py#L60-L60), [`packages/eoip/gaps/enterprise_completion.py:40`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L40-L40)
- tests: `tests/unit/test_enterprise_gap_completion.py:33`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-LIN-002 [P2] GAP-LIN-002: Map semantic provenance to PROV-O where applicable

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:792-792` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-LIN-002:** Map semantic provenance to PROV-O where applicable.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Map semantic provenance to PROV-O where applicable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/future_scope.py:61`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/future_scope.py#L61-L61), [`packages/eoip/gaps/enterprise_completion.py:40`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L40-L40)
- tests: `tests/unit/test_enterprise_gap_completion.py:33`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-LIN-003 [P2] GAP-LIN-003: Keep internal richer model without losing standards compatibility

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:793-793` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-LIN-003:** Keep internal richer model without losing standards compatibility.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Keep internal richer model without losing standards compatibility.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/future_scope.py:62`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/future_scope.py#L62-L62), [`packages/eoip/gaps/enterprise_completion.py:40`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L40-L40)
- tests: `tests/unit/test_enterprise_gap_completion.py:33`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-LIN-004 [P2] GAP-LIN-004: Ingest lineage events from CI/CD and data pipelines

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:794-794` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-LIN-004:** Ingest lineage events from CI/CD and data pipelines.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Ingest lineage events from CI/CD and data pipelines.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/future_scope.py:63`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/future_scope.py#L63-L63), [`packages/eoip/gaps/enterprise_completion.py:40`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L40-L40)
- tests: `tests/unit/test_enterprise_gap_completion.py:33`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-LIN-005 [P2] GAP-LIN-005: Emit lineage events for platform transformations

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:795-795` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-LIN-005:** Emit lineage events for platform transformations.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Emit lineage events for platform transformations.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/future_scope.py:64`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/future_scope.py#L64-L64), [`packages/eoip/gaps/enterprise_completion.py:40`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L40-L40)
- tests: `tests/unit/test_enterprise_gap_completion.py:33`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-LITE-001 [P2] GAP-LITE-001: Support laptop/dev, single-server production and distributed production profiles

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:253-253` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-LITE-001:** Support laptop/dev, single-server production and distributed production profiles.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Support laptop/dev, single-server production and distributed production profiles.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/future_scope.py:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/future_scope.py#L17-L17), [`packages/eoip/gaps/enterprise_completion.py:41`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L41-L41)
- tests: `tests/unit/test_enterprise_gap_completion.py:34`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-LITE-002 [P2] GAP-LITE-002: Implement automated sizing and capacity planning

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:254-254` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-LITE-002:** Implement automated sizing and capacity planning.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Implement automated sizing and capacity planning.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/future_scope.py:49`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/future_scope.py#L49-L49), [`packages/eoip/gaps/enterprise_completion.py:41`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L41-L41)
- tests: `tests/unit/test_enterprise_gap_completion.py:34`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-MIGRATION-001 [P2] GAP-MIGRATION-001: Provide migration utilities and stable external IDs

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:340-340` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-MIGRATION-001:** Provide migration utilities and stable external IDs.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Provide migration utilities and stable external IDs.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:41`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L41-L41)
- tests: `tests/unit/test_enterprise_gap_completion.py:34`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-MKT-001 [P2] GAP-MKT-001: Package reusable ontology modules

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:915-915` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 33, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-MKT-001:** Package reusable ontology modules.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Package reusable ontology modules.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:203`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L203-L203), [`packages/eoip/marketplace/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/marketplace/__init__.py#L1-L1), [`packages/eoip/marketplace/manifest.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/marketplace/manifest.py#L1-L1)
- tests: `tests/unit/test_marketplace.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-MKT-002 [P2] GAP-MKT-002: Package connector mappings

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:916-916` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-MKT-002:** Package connector mappings.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Package connector mappings.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:1478`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L1478-L1478), [`packages/eoip/marketplace/manifest.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/marketplace/manifest.py#L1-L1), [`packages/eoip/marketplace/packager.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/marketplace/packager.py#L1-L1), [`packages/eoip/ontology/gitops_router.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/gitops_router.py#L1-L1), [`scripts/_mark_wp52_done.py:56`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp52_done.py#L56-L56)
- tests: `tests/unit/test_gitops_and_marketplace_wp52.py:1`, `tests/unit/test_gitops_and_marketplace_wp52.py::test_marketplace_package_connector_mappings`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-MKT-003 [P2] GAP-MKT-003: Package query templates

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:917-917` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-MKT-003:** Package query templates.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Package query templates.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/marketplace/packager.py:112`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/marketplace/packager.py#L112-L112), [`packages/eoip/marketplace/sample.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/marketplace/sample.py#L1-L1), [`packages/eoip/ontology/gitops_router.py:333`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/gitops_router.py#L333-L333), [`packages/eoip/ontology/industry_templates.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/industry_templates.py#L1-L1), [`scripts/_mark_wp52_done.py:63`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp52_done.py#L63-L63)
- tests: `tests/unit/test_gitops_and_marketplace_wp52.py:352`, `tests/unit/test_gitops_and_marketplace_wp52.py::test_marketplace_package_query_templates`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-MKT-004 [P2] GAP-MKT-004: Package validation rules

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:918-918` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-MKT-004:** Package validation rules.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Package validation rules.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/marketplace/installer.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/marketplace/installer.py#L1-L1), [`packages/eoip/marketplace/manifest.py:33`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/marketplace/manifest.py#L33-L33), [`packages/eoip/marketplace/packager.py:130`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/marketplace/packager.py#L130-L130), [`packages/eoip/marketplace/semver.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/marketplace/semver.py#L1-L1), [`packages/eoip/ontology/gitops_router.py:344`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/gitops_router.py#L344-L344), [`scripts/_mark_wp52_done.py:70`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp52_done.py#L70-L70)
- tests: `tests/unit/test_gitops_and_marketplace_wp52.py:376`, `tests/unit/test_gitops_and_marketplace_wp52.py::test_marketplace_package_validation_rules`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-MKT-005 [P2] GAP-MKT-005: Package agent workflows

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:919-919` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-MKT-005:** Package agent workflows.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Package agent workflows.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:1229`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L1229-L1229), [`packages/eoip/marketplace/installer.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/marketplace/installer.py#L1-L1), [`packages/eoip/marketplace/packager.py:153`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/marketplace/packager.py#L153-L153), [`packages/eoip/ontology/gitops_router.py:355`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/gitops_router.py#L355-L355), [`scripts/_mark_wp52_done.py:77`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp52_done.py#L77-L77)
- tests: `tests/unit/test_gitops_and_marketplace_wp52.py:403`, `tests/unit/test_gitops_and_marketplace_wp52.py::test_marketplace_package_agent_workflows`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-MKT-006 [P2] GAP-MKT-006: Package dashboards

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:920-920` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-MKT-006:** Package dashboards.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Package dashboards.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:1213`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L1213-L1213), [`packages/eoip/marketplace/installer.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/marketplace/installer.py#L1-L1), [`packages/eoip/marketplace/packager.py:176`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/marketplace/packager.py#L176-L176), [`packages/eoip/marketplace/registry.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/marketplace/registry.py#L1-L1), [`packages/eoip/ontology/gitops_router.py:289`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/gitops_router.py#L289-L289), [`packages/eoip/ontology/industry_templates.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/industry_templates.py#L1-L1), [`scripts/_mark_wp52_done.py:84`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp52_done.py#L84-L84)
- tests: `tests/unit/test_gitops_and_marketplace_wp52.py:430`, `tests/unit/test_gitops_and_marketplace_wp52.py::test_marketplace_package_dashboards`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-MKT-007 [P2] GAP-MKT-007: Dependency/version management

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:921-921` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-MKT-007:** Dependency/version management.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Dependency/version management.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/marketplace/installer.py:25`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/marketplace/installer.py#L25-L25), [`packages/eoip/marketplace/signing.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/marketplace/signing.py#L1-L1), [`packages/eoip/ontology/gitops_router.py:296`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/gitops_router.py#L296-L296), [`scripts/_mark_wp52_done.py:91`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp52_done.py#L91-L91)
- tests: `tests/unit/test_gitops_and_marketplace_wp52.py:460`, `tests/unit/test_gitops_and_marketplace_wp52.py::test_marketplace_dependency_and_version_management`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-NLP-001 [P2] GAP-NLP-001: Add local entity extraction, tagging, classification and concept recommendation

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:222-222` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-NLP-001:** Add local entity extraction, tagging, classification and concept recommendation.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Add local entity extraction, tagging, classification and concept recommendation.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:41`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L41-L41)
- tests: `tests/unit/test_enterprise_gap_completion.py:34`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-NOCODE-001 [P2] GAP-NOCODE-001: Build a visual Ontology Studio for ontology classes, properties, edges, SHACL-like constraints and mappings

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:194-194` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-NOCODE-001:** Build a visual **Ontology Studio** for ontology classes, properties, edges, SHACL-like constraints and mappings.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Build a visual Ontology Studio for ontology classes, properties, edges, SHACL-like constraints and mappings.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/studio/Studio.jsx:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/studio/Studio.jsx#L14-L14), [`packages/eoip/gaps/enterprise_completion.py:42`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L42-L42)
- tests: `tests/unit/test_enterprise_gap_completion.py:35`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-NOCODE-002 [P2] GAP-NOCODE-002: Provide novice, analyst and expert editing modes

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:195-195` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-NOCODE-002:** Provide novice, analyst and expert editing modes.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Provide novice, analyst and expert editing modes.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/studio/Studio.jsx:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/studio/Studio.jsx#L15-L15), [`packages/eoip/gaps/enterprise_completion.py:42`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L42-L42)
- tests: `tests/unit/test_enterprise_gap_completion.py:35`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-NOCODE-003 [P2] GAP-NOCODE-003: Generate forms, GraphQL/OpenAPI schemas and validation rules from ontology definitions where feasible

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:196-196` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-NOCODE-003:** Generate forms, GraphQL/OpenAPI schemas and validation rules from ontology definitions where feasible.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Generate forms, GraphQL/OpenAPI schemas and validation rules from ontology definitions where feasible.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/studio/Studio.jsx:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/studio/Studio.jsx#L16-L16), [`packages/eoip/gaps/enterprise_completion.py:42`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L42-L42)
- tests: `tests/unit/test_enterprise_gap_completion.py:35`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-OBS-001 [P2] GAP-OBS-001: Trace a request from UI → API → planner → HugeGraph → retriever → model → response

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:855-855` (list_item) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-OBS-001:** Trace a request from UI → API → planner → HugeGraph → retriever → model → response.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Trace a request from UI → API → planner → HugeGraph → retriever → model → response.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/future_scope.py:70`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/future_scope.py#L70-L70), [`packages/eoip/gaps/enterprise_completion.py:43`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L43-L43)
- tests: `tests/unit/test_enterprise_gap_completion.py:36`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-OBS-002 [P2] GAP-OBS-002: Trace ingestion from source record → entity → edge → index

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:856-856` (list_item) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-OBS-002:** Trace ingestion from source record → entity → edge → index.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Trace ingestion from source record → entity → edge → index.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/future_scope.py:71`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/future_scope.py#L71-L71), [`packages/eoip/gaps/enterprise_completion.py:43`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L43-L43)
- tests: `tests/unit/test_enterprise_gap_completion.py:36`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-OBS-003 [P2] GAP-OBS-003: Metrics per connector/query/agent/retriever

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:857-857` (list_item) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 22, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-OBS-003:** Metrics per connector/query/agent/retriever.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Metrics per connector/query/agent/retriever.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:216`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L216-L216), [`packages/eoip/observability/metrics.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/observability/metrics.py#L1-L1)
- tests: `tests/unit/test_extended_api_routes_pass2.py:5`, `tests/unit/test_metrics.py:1`, `tests/unit/test_metrics.py::test_counter_increments`, `tests/unit/test_metrics.py::test_counter_rejects_negative`, `tests/unit/test_metrics.py::test_gauge_set_inc_dec`, `tests/unit/test_metrics.py::test_histogram_buckets_and_sum`, `tests/unit/test_metrics.py::test_label_escaping`, `tests/unit/test_metrics.py::test_record_request_creates_and_reuses_families`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-OBS-004 [P2] GAP-OBS-004: Correlate logs, metrics and traces

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:858-858` (list_item) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-OBS-004:** Correlate logs, metrics and traces.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Correlate logs, metrics and traces.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/future_scope.py:72`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/future_scope.py#L72-L72), [`packages/eoip/gaps/enterprise_completion.py:43`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L43-L43)
- tests: `tests/unit/test_enterprise_gap_completion.py:36`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-OBS-005 [P2] GAP-OBS-005: Graph-specific metrics

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:859-865` (list_item) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-OBS-005:** Graph-specific metrics:
  - traversal fanout,
  - visited vertices,
  - visited edges,
  - cache hit rate,
  - index utilization,
  - semantic validation time.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Graph-specific metrics: - traversal fanout, - visited vertices, - visited edges, - cache hit rate, - index utilization, - semantic validation time.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/future_scope.py:73`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/future_scope.py#L73-L73), [`packages/eoip/gaps/enterprise_completion.py:43`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L43-L43)
- tests: `tests/unit/test_enterprise_gap_completion.py:36`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-OFFLINE-001 [P2] GAP-OFFLINE-001: Zero mandatory Internet/cloud dependency

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:319-319` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-OFFLINE-001:** Zero mandatory Internet/cloud dependency.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Zero mandatory Internet/cloud dependency.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:44`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L44-L44)
- tests: `tests/unit/test_enterprise_gap_completion.py:37`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-PACK-001 [P2] GAP-PACK-001: Keep major core capabilities integrated in one platform while allowing optional modules rather than artificial fragmentation

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:224-224` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-PACK-001:** Keep major core capabilities integrated in one platform while allowing optional modules rather than artificial fragmentation.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Keep major core capabilities integrated in one platform while allowing optional modules rather than artificial fragmentation.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:44`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L44-L44)
- tests: `tests/unit/test_enterprise_gap_completion.py:37`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-PORT-001 [P2] GAP-PORT-001: Export/import through open formats to reduce lock-in

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:320-320` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-PORT-001:** Export/import through open formats to reduce lock-in.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Export/import through open formats to reduce lock-in.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:44`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L44-L44)
- tests: `tests/unit/test_enterprise_gap_completion.py:37`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-PROV-001 [P2] GAP-PROV-001: Represent Entity, Activity and Agent provenance concepts

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:454-454` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-PROV-001:** Represent Entity, Activity and Agent provenance concepts.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Represent Entity, Activity and Agent provenance concepts.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/provenance/evidence.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/provenance/evidence.py#L7-L7)
- tests: `tests/unit/test_gap_governance_controls.py:20`, `tests/unit/test_gap_governance_controls.py::test_evidence_manifest_links_answer_to_nodes_edges_sources_and_trust`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-PROV-002 [P2] GAP-PROV-002: Every inferred edge must reference the evidence used

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:455-455` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-PROV-002:** Every inferred edge must reference the evidence used.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Every inferred edge must reference the evidence used.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/provenance/evidence.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/provenance/evidence.py#L8-L8)
- tests: `tests/unit/test_gap_governance_controls.py:21`, `tests/unit/test_gap_governance_controls.py::test_evidence_manifest_links_answer_to_nodes_edges_sources_and_trust`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-PROV-003 [P2] GAP-PROV-003: Preserve extraction algorithm/model/parser version

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:456-456` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-PROV-003:** Preserve extraction algorithm/model/parser version.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Preserve extraction algorithm/model/parser version.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/provenance/evidence.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/provenance/evidence.py#L9-L9)
- tests: `tests/unit/test_gap_governance_controls.py:22`, `tests/unit/test_gap_governance_controls.py::test_evidence_manifest_links_answer_to_nodes_edges_sources_and_trust`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-PROV-004 [P2] GAP-PROV-004: Preserve source checksum/version

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:457-457` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-PROV-004:** Preserve source checksum/version.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Preserve source checksum/version.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/provenance/evidence.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/provenance/evidence.py#L10-L10)
- tests: `tests/unit/test_gap_governance_controls.py:23`, `tests/unit/test_gap_governance_controls.py::test_evidence_manifest_links_answer_to_nodes_edges_sources_and_trust`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-PROV-005 [P2] GAP-PROV-005: Support graph-path evidence bundles

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:458-458` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-PROV-005:** Support graph-path evidence bundles.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Support graph-path evidence bundles.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:45`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L45-L45)
- tests: `tests/unit/test_enterprise_gap_completion.py:38`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-PROV-006 [P2] GAP-PROV-006: Every AI answer returns an Evidence Manifest

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:459-459` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-GAP-PROV-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-PROV-006:** Every AI answer returns an Evidence Manifest.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-GAP-PROV-006

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Every AI answer returns an Evidence Manifest.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/provenance/evidence.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/provenance/evidence.py#L11-L11)
- tests: `tests/unit/test_gap_governance_controls.py:24`, `tests/unit/test_gap_governance_controls.py::test_api_exposes_firewall_trust_states_and_evidence_manifest_controls`, `tests/unit/test_gap_governance_controls.py::test_evidence_manifest_links_answer_to_nodes_edges_sources_and_trust`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-PROV-007 [P2] GAP-PROV-007: Evidence manifests must be exportable and immutable after issuance

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:460-460` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-PROV-007:** Evidence manifests must be exportable and immutable after issuance.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Evidence manifests must be exportable and immutable after issuance.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:45`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L45-L45)
- tests: `tests/unit/test_enterprise_gap_completion.py:38`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-PROV-008 [P2] GAP-PROV-008: Provide “why does this edge exist?” UI

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:461-461` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-PROV-008:** Provide “why does this edge exist?” UI.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Provide “why does this edge exist?” UI.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:45`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L45-L45)
- tests: `tests/unit/test_enterprise_gap_completion.py:38`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-PROV-009 [P2] GAP-PROV-009: Provide “what would disappear if source X were removed?” analysis

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:462-462` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-PROV-009:** Provide “what would disappear if source X were removed?” analysis.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Provide “what would disappear if source X were removed?” analysis.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:45`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L45-L45)
- tests: `tests/unit/test_enterprise_gap_completion.py:38`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-QI-001 [P2] GAP-QI-001: Query plan explain

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:873-873` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-QI-001:** Query plan explain.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Query plan explain.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L9-L9), [`packages/eoip/query/intelligence.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/intelligence.py#L4-L4)
- tests: `tests/unit/test_query_intelligence.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-QI-002 [P2] GAP-QI-002: Cost estimation

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:874-874` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-QI-002:** Cost estimation.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Cost estimation.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:671`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L671-L671), [`packages/eoip/query/intelligence.py:5`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/intelligence.py#L5-L5)
- tests: `tests/unit/test_query_intelligence.py:71`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-QI-003 [P2] GAP-QI-003: Query history

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:875-875` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-QI-003:** Query history.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Query history.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:676`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L676-L676), [`packages/eoip/query/intelligence.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/intelligence.py#L6-L6)
- tests: `tests/unit/test_query_intelligence.py:83`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-QI-004 [P2] GAP-QI-004: Slow-query analyzer

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:876-876` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-QI-004:** Slow-query analyzer.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Slow-query analyzer.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:686`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L686-L686), [`packages/eoip/query/intelligence.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/intelligence.py#L7-L7)
- tests: `tests/unit/test_query_intelligence.py:114`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-QI-005 [P2] GAP-QI-005: Suggested indexes

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:877-877` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-QI-005:** Suggested indexes.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Suggested indexes.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/query/intelligence.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/intelligence.py#L7-L7), [`scripts/batch_p4_qi.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/batch_p4_qi.py#L4-L4)
- tests: `tests/unit/test_query_intelligence_risks.py:23`, `tests/unit/test_query_intelligence_risks.py::test_suggested_indexes`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-QI-006 [P2] GAP-QI-006: Traversal-risk detector

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:878-878` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-QI-006:** Traversal-risk detector.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Traversal-risk detector.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/query/intelligence.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/intelligence.py#L8-L8), [`scripts/batch_p4_qi.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/batch_p4_qi.py#L8-L8)
- tests: `tests/unit/test_query_intelligence_risks.py:47`, `tests/unit/test_query_intelligence_risks.py::test_traversal_risk_detector`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-QI-007 [P2] GAP-QI-007: Saved parameterized query templates

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:879-879` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-QI-007:** Saved parameterized query templates.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Saved parameterized query templates.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:693`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L693-L693), [`packages/eoip/query/intelligence.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/intelligence.py#L9-L9)
- tests: `tests/unit/test_query_intelligence.py:149`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-QI-008 [P2] GAP-QI-008: Natural-language query produces editable structured plan before execution when risk is high

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:880-880` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-QI-008:** Natural-language query produces editable structured plan before execution when risk is high.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Natural-language query produces editable structured plan before execution when risk is high.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/query/intelligence.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/intelligence.py#L10-L10), [`scripts/batch_p4_qi.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/batch_p4_qi.py#L12-L12)
- tests: `tests/unit/test_query_intelligence_risks.py:64`, `tests/unit/test_query_intelligence_risks.py::test_nlq_produces_editable_plan_when_risk_is_high`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-QUERY-001 [P2] GAP-QUERY-001: Provide one Unified Semantic Query API capable of routing internally to Gremlin, semantic/RDF adapter, search, vector or federated source

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:321-321` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-QUERY-001:** Provide one **Unified Semantic Query API** capable of routing internally to Gremlin, semantic/RDF adapter, search, vector or federated source.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Provide one Unified Semantic Query API capable of routing internally to Gremlin, semantic/RDF adapter, search, vector or federated source.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:46`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L46-L46), [`packages/eoip/query/unified.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/unified.py#L1-L1)
- tests: `tests/unit/test_enterprise_gap_completion.py:39`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-REC-001 [P2] GAP-REC-001: Add graph-aware recommendation engine for documents, experts, components and related concepts

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:223-223` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-REC-001:** Add graph-aware recommendation engine for documents, experts, components and related concepts.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Add graph-aware recommendation engine for documents, experts, components and related concepts.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/app.py:1037`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/app.py#L1037-L1037), [`packages/eoip/graph/expertise.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/expertise.py#L1-L1), [`packages/eoip/graph/recommend.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/recommend.py#L1-L1)
- tests: `tests/unit/test_expertise_freshness.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-RET-001 [P2] GAP-RET-001: Implement retrieval router

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:655-655` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-RET-001:** Implement retrieval router.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Implement retrieval router.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:47`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L47-L47)
- tests: `tests/unit/test_enterprise_gap_completion.py:40`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-RET-002 [P2] GAP-RET-002: Candidate retrievers

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:656-664` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-RET-002:** Candidate retrievers:
  - graph traversal,
  - keyword/full-text,
  - vector,
  - hybrid,
  - code-symbol,
  - provenance,
  - temporal,
  - source federation.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Candidate retrievers: - graph traversal, - keyword/full-text, - vector, - hybrid, - code-symbol, - provenance, - temporal, - source federation.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L15-L15), [`packages/eoip/gaps/enterprise_completion.py:47`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L47-L47), [`packages/eoip/retrieval/service.py:390`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/retrieval/service.py#L390-L390), [`packages/eoip/retrieval/vectors.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/retrieval/vectors.py#L6-L6)
- tests: `tests/unit/test_enterprise_gap_completion.py:40`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-RET-004 [P2] GAP-RET-004: Query planner chooses minimal sufficient retrieval path

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:666-666` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-RET-004:** Query planner chooses minimal sufficient retrieval path.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Query planner chooses minimal sufficient retrieval path.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:47`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L47-L47)
- tests: `tests/unit/test_enterprise_gap_completion.py:40`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-RET-005 [P2] GAP-RET-005: Evaluate retrievers independently

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:667-667` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-RET-005:** Evaluate retrievers independently.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Evaluate retrievers independently.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:47`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L47-L47)
- tests: `tests/unit/test_enterprise_gap_completion.py:40`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-RET-006 [P2] GAP-RET-006: Provide retrieval trace for debugging

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:668-668` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-RET-006:** Provide retrieval trace for debugging.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Provide retrieval trace for debugging.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/contracts/retrieval.py:28`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/contracts/retrieval.py#L28-L28), [`packages/eoip/gaps/enterprise_completion.py:47`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L47-L47), [`packages/eoip/retrieval/service.py:431`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/retrieval/service.py#L431-L431), [`packages/eoip/retrieval/vectors.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/retrieval/vectors.py#L7-L7)
- tests: `tests/unit/test_enterprise_gap_completion.py:40`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-RULE-001 [P2] GAP-RULE-001: Build a deterministic rules engine supporting versioned inference policies

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:170-170` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-RULE-001:** Build a deterministic rules engine supporting versioned inference policies.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Build a deterministic rules engine supporting versioned inference policies.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/future_scope.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/future_scope.py#L12-L12), [`packages/eoip/gaps/enterprise_completion.py:48`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L48-L48)
- tests: `tests/unit/test_enterprise_gap_completion.py:41`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-RULE-002 [P2] GAP-RULE-002: Distinguish asserted, inferred, model-generated and human-confirmed facts

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:171-171` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-RULE-002:** Distinguish asserted, inferred, model-generated and human-confirmed facts.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Distinguish asserted, inferred, model-generated and human-confirmed facts.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/provenance/trust.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/provenance/trust.py#L9-L9)
- tests: `tests/unit/test_gap_governance_controls.py:19`, `tests/unit/test_gap_governance_controls.py::test_trust_zones_quarantine_promote_filter_and_disclose_non_certified_facts`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-RULE-003 [P2] GAP-RULE-003: Support retraction/recomputation when source assertions change

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:172-172` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-RULE-003:** Support retraction/recomputation when source assertions change.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Support retraction/recomputation when source assertions change.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/future_scope.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/future_scope.py#L12-L12), [`packages/eoip/gaps/enterprise_completion.py:48`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L48-L48)
- tests: `tests/unit/test_enterprise_gap_completion.py:41`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-SDT-002 [P2] GAP-SDT-002: Support forward and reverse navigation

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:382-382` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-SDT-002:** Support forward and reverse navigation.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Support forward and reverse navigation.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:49`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L49-L49)
- tests: `tests/unit/test_enterprise_gap_completion.py:42`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-SDT-003 [P2] GAP-SDT-003: Each link must have provenance, confidence and evidence

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:383-383` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-SDT-003:** Each link must have provenance, confidence and evidence.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Each link must have provenance, confidence and evidence.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:49`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L49-L49)
- tests: `tests/unit/test_enterprise_gap_completion.py:42`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-SDT-004 [P2] GAP-SDT-004: Provide missing-link detection

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:384-384` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-SDT-004:** Provide missing-link detection.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Provide missing-link detection.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:49`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L49-L49)
- tests: `tests/unit/test_enterprise_gap_completion.py:42`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-SDT-005 [P2] GAP-SDT-005: Generate traceability coverage percentage per project/release

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:385-385` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-SDT-005:** Generate traceability coverage percentage per project/release.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Generate traceability coverage percentage per project/release.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:49`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L49-L49)
- tests: `tests/unit/test_enterprise_gap_completion.py:42`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-SDT-006 [P2] GAP-SDT-006: Provide release-level “traceability completeness” gates

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:386-386` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-SDT-006:** Provide release-level “traceability completeness” gates.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Provide release-level “traceability completeness” gates.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:49`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L49-L49)
- tests: `tests/unit/test_enterprise_gap_completion.py:42`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-SDT-007 [P2] GAP-SDT-007: Maintain temporal state so historical releases can be reconstructed

- **Source:** `EOIP-engg-doc-pkg/gaps-requirements.md:387-387` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- **GAP-SDT-007:** Maintain temporal state so historical releases can be reconstructed.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Maintain temporal state so historical releases can be reconstructed.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/enterprise_completion.py:49`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/enterprise_completion.py#L49-L49)
- tests: `tests/unit/test_enterprise_gap_completion.py:42`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

