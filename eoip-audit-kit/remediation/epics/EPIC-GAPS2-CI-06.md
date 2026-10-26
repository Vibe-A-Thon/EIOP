# EPIC-GAPS2-CI-06: EOIP-engg-doc-pkg/gaps2-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 37 tasks, ~18.5 h, priorities {'P2': 35, 'P3': 2}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-G2-TIME-007 [P2] G2-TIME-007: G2-TIME-007

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1060-1064` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TIME-007
Evidence viewed in historical mode SHALL reflect what was known/valid for that time.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Evidence viewed in historical mode SHALL reflect what was known/valid for that time.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:224`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L224-L224)
- tests: `tests/unit/test_temporal_model_family.py:156`, `tests/unit/test_temporal_model_family.py::test_historical_mode_evidence_reflects_valid_time`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TWIN-001 [P2] G2-TWIN-001: G2-TWIN-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1005-1007` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TWIN-001
EOIP SHALL present the enterprise as a continuously synchronized semantic twin.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] EOIP SHALL present the enterprise as a continuously synchronized semantic twin.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:55`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L55-L55), [`packages/eoip/graph/twin.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/twin.py#L1-L1)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:52`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TWIN-002 [P2] G2-TWIN-002: G2-TWIN-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1008-1024` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TWIN-002
The twin SHALL include:
- business intent,
- requirements,
- architecture,
- code,
- APIs,
- tests,
- CI/CD,
- deployments,
- runtime,
- telemetry semantics,
- incidents,
- knowledge/docs,
- people/ownership,
- decisions.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] The twin SHALL include: - business intent, - requirements, - architecture, - code, - APIs, - tests, - CI/CD, - deployments, - runtime, - telemetry semantics, - incidents, - knowledge/docs, - people/ownership, - decisions.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_check_wp62.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp62.py#L12-L12), [`scripts/_find_specs.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_find_specs.py#L7-L7), [`scripts/_mark_wp62_done.py:116`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp62_done.py#L116-L116)
- tests: `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:31`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py::test_g2_twin_002_twin_comprehensive_ontology_coverage`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TWIN-003 [P2] G2-TWIN-003: G2-TWIN-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1025-1027` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TWIN-003
The twin SHALL expose current state and historical revisions.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] The twin SHALL expose current state and historical revisions.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/twin.py:173`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/twin.py#L173-L173), [`scripts/_check_wp62.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp62.py#L12-L12), [`scripts/_mark_wp62_done.py:120`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp62_done.py#L120-L120)
- tests: `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:32`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py::test_g2_twin_003_twin_historical_revisions_and_state`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TWIN-004 [P2] G2-TWIN-004: G2-TWIN-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1028-1030` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TWIN-004
Every derived twin relationship SHALL be evidence-addressable.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Every derived twin relationship SHALL be evidence-addressable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/twin.py:197`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/twin.py#L197-L197), [`scripts/_check_wp62.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp62.py#L12-L12), [`scripts/_mark_wp62_done.py:124`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp62_done.py#L124-L124)
- tests: `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:33`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py::test_g2_twin_004_derived_relationships_evidence_addressable`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-TWIN-005 [P2] G2-TWIN-005: G2-TWIN-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1031-1039` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-TWIN-005
The twin SHALL distinguish:
- intended,
- implemented,
- observed runtime,
- inferred.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] The twin SHALL distinguish: - intended, - implemented, - observed runtime, - inferred.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_check_wp62.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp62.py#L12-L12), [`scripts/_mark_wp62_done.py:128`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp62_done.py#L128-L128)
- tests: `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:34`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py::test_g2_twin_005_distinguish_intended_implemented_observed_inferred`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-GRAPH-001 [P2] G2-UX-GRAPH-001: G2-UX-GRAPH-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1474-1476` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-GRAPH-001
Semantic zoom.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Semantic zoom.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:56`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L56-L56)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:53`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-GRAPH-002 [P2] G2-UX-GRAPH-002: G2-UX-GRAPH-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1477-1479` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-GRAPH-002
Clustering/grouping.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Behaviour stated in EOIP-engg-doc-pkg/gaps2-requirements.md:1477 ('G2-UX-GRAPH-002') is demonstrably met. Requirement text gives no testable criteria: discovery step: refine with the requirement owner (UNKNOWN).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/kgr/rendering/WebGLGraphRenderer.js:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/kgr/rendering/WebGLGraphRenderer.js#L2-L2), [`scripts/_mark_wp53_done.py:164`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L164-L164)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:7`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_graph_002_clustering_grouping`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-GRAPH-003 [P2] G2-UX-GRAPH-003: G2-UX-GRAPH-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1480-1482` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-GRAPH-003
Graph folding/collapse.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Graph folding/collapse.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:170`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L170-L170)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:236`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_graph_003_folding_collapse_layouts`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-GRAPH-004 [P2] G2-UX-GRAPH-004: G2-UX-GRAPH-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1483-1485` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-GRAPH-004
Progressive expansion rather than rendering huge neighborhoods.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Progressive expansion rather than rendering huge neighborhoods.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:176`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L176-L176)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:241`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_graph_004_progressive_expansion`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-GRAPH-005 [P2] G2-UX-GRAPH-005: G2-UX-GRAPH-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1486-1488` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-GRAPH-005
Time slider.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Time slider.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:182`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L182-L182)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:246`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_graph_005_time_slider`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-GRAPH-006 [P2] G2-UX-GRAPH-006: G2-UX-GRAPH-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1489-1491` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-GRAPH-006
Current/historical toggle.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Current/historical toggle.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:188`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L188-L188)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:251`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_graph_006_current_historical_toggle`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-GRAPH-007 [P2] G2-UX-GRAPH-007: G2-UX-GRAPH-007

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1492-1494` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-GRAPH-007
Relationship/trust/source filters.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Relationship/trust/source filters.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:194`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L194-L194)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:256`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_graph_007_filters`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-GRAPH-008 [P2] G2-UX-GRAPH-008: G2-UX-GRAPH-008

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1495-1497` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-GRAPH-008
Edge confidence/evidence indicators.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Edge confidence/evidence indicators.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:200`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L200-L200)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:261`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_graph_008_edge_confidence_indicators`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-GRAPH-009 [P2] G2-UX-GRAPH-009: G2-UX-GRAPH-009

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1498-1500` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-GRAPH-009
Path storytelling mode.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Path storytelling mode.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:206`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L206-L206)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:266`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_graph_009_path_storytelling`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-GRAPH-010 [P2] G2-UX-GRAPH-010: G2-UX-GRAPH-010

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1501-1503` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-GRAPH-010
Architecture boundary overlays.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Architecture boundary overlays.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:212`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L212-L212)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:271`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_graph_010_architecture_overlay`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-GRAPH-011 [P2] G2-UX-GRAPH-011: G2-UX-GRAPH-011

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1504-1506` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-GRAPH-011
Runtime topology overlay.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Runtime topology overlay.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:218`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L218-L218)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:276`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_graph_011_runtime_topology_overlay`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-GRAPH-012 [P2] G2-UX-GRAPH-012: G2-UX-GRAPH-012

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1507-1509` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-GRAPH-012
Release comparison overlay.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Release comparison overlay.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:224`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L224-L224)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:281`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_graph_012_release_comparison_overlay`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-GRAPH-013 [P2] G2-UX-GRAPH-013: G2-UX-GRAPH-013

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1510-1512` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-GRAPH-013
Blast-radius highlighting.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Blast-radius highlighting.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:230`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L230-L230)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:286`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_graph_013_blast_radius_highlighting`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-GRAPH-014 [P2] G2-UX-GRAPH-014: G2-UX-GRAPH-014

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1513-1515` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-GRAPH-014
Click relationship → “Why does this edge exist?”
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Click relationship → “Why does this edge exist?”
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:236`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L236-L236)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:291`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_graph_014_why_edge_exists`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-GRAPH-015 [P2] G2-UX-GRAPH-015: G2-UX-GRAPH-015

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1516-1518` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-GRAPH-015
Click node → “Where did this entity come from?”
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Click node → “Where did this entity come from?”
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:242`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L242-L242)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:296`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_graph_015_where_entity_came_from`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-LENS-001 [P2] G2-UX-LENS-001: G2-UX-LENS-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1438-1440` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-UX-LENS-001
Implement a pluggable lens framework where all lenses operate on the same graph/query services.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Implement a pluggable lens framework where all lenses operate on the same graph/query services.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:57`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L57-L57), [`packages/eoip/graph/lens.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/lens.py#L1-L1)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:54`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-LENS-002 [P2] G2-UX-LENS-002: G2-UX-LENS-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1464-1466` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-UX-LENS-002
Lens state SHALL preserve current scope/entity/time/filter context when switching.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Lens state SHALL preserve current scope/entity/time/filter context when switching.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:254`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L254-L254), [`scripts/check_wp53_registry.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/check_wp53_registry.py#L11-L11)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:8`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_lens_002_context_preservation`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-LENS-003 [P2] G2-UX-LENS-003: G2-UX-LENS-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1467-1471` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-UX-LENS-003
Lenses SHALL support shareable/exportable local query definitions where permitted.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Lenses SHALL support shareable/exportable local query definitions where permitted.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:260`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L260-L260), [`scripts/check_wp53_registry.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/check_wp53_registry.py#L11-L11)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:326`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_lens_003_shareable_query_definitions`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-PLAY-001 [P2] G2-UX-PLAY-001: G2-UX-PLAY-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1526-1528` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-PLAY-001
Replay selected incident/release/change as temporal graph events.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Replay selected incident/release/change as temporal graph events.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:58`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L58-L58)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:55`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-PLAY-003 [P2] G2-UX-PLAY-003: G2-UX-PLAY-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1538-1540` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-PLAY-003
Allow pause/step/scrub.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Allow pause/step/scrub.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:272`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L272-L272)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:341`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_play_003_pause_step_scrub`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-PLAY-004 [P2] G2-UX-PLAY-004: G2-UX-PLAY-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1541-1543` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-PLAY-004
Every playback event SHALL link to source evidence.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Every playback event SHALL link to source evidence.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:278`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L278-L278)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:346`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_play_004_event_source_evidence_links`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-UX-PLAY-005 [P2] G2-UX-PLAY-005: G2-UX-PLAY-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1544-1548` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-UX-PLAY-005
Support export of an incident timeline evidence package.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Support export of an incident timeline evidence package.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:284`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L284-L284)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:351`, `tests/unit/test_web_ux_and_admin_wp53.py::test_g2_ux_play_005_export_timeline_package`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-VSC-001 [P2] G2-VSC-001: G2-VSC-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1606-1608` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-VSC-001
Display API contract relationships for current symbol.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Display API contract relationships for current symbol.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:59`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L59-L59)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:56`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-VSC-002 [P2] G2-VSC-002: G2-VSC-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1609-1611` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-VSC-002
Display runtime services/deployments connected to current code.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Display runtime services/deployments connected to current code.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_find_vsc_specs.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_find_vsc_specs.py#L14-L14), [`scripts/_inspect_vsc_reqs.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_inspect_vsc_reqs.py#L6-L6), [`scripts/_mark_wp54_and_wp55_done.py:29`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp54_and_wp55_done.py#L29-L29)
- tests: `tests/unit/test_vscode_extension_wp54.py:6`, `tests/unit/test_vscode_extension_wp54.py::test_g2_vsc_002_runtime_services`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-VSC-003 [P2] G2-VSC-003: G2-VSC-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1612-1614` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-VSC-003
Display architecture conformance findings inline/panel.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Display architecture conformance findings inline/panel.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_find_vsc_specs.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_find_vsc_specs.py#L14-L14), [`scripts/_inspect_vsc_reqs.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_inspect_vsc_reqs.py#L6-L6), [`scripts/_mark_wp54_and_wp55_done.py:33`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp54_and_wp55_done.py#L33-L33)
- tests: `tests/unit/test_vscode_extension_wp54.py:7`, `tests/unit/test_vscode_extension_wp54.py::test_g2_vsc_003_architecture_conformance`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-VSC-004 [P2] G2-VSC-004: G2-VSC-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1615-1617` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-VSC-004
Display impacted tests for current change.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Display impacted tests for current change.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_find_vsc_specs.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_find_vsc_specs.py#L14-L14), [`scripts/_inspect_vsc_reqs.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_inspect_vsc_reqs.py#L6-L6), [`scripts/_mark_wp54_and_wp55_done.py:37`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp54_and_wp55_done.py#L37-L37)
- tests: `tests/unit/test_vscode_extension_wp54.py:8`, `tests/unit/test_vscode_extension_wp54.py::test_g2_vsc_004_impacted_tests`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-VSC-006 [P2] G2-VSC-006: G2-VSC-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1621-1623` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-VSC-006
Display decision/ADR rationale.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Display decision/ADR rationale.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_find_vsc_specs.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_find_vsc_specs.py#L14-L14), [`scripts/_inspect_vsc_reqs.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_inspect_vsc_reqs.py#L6-L6), [`scripts/_mark_wp54_and_wp55_done.py:45`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp54_and_wp55_done.py#L45-L45)
- tests: `tests/unit/test_vscode_extension_wp54.py:10`, `tests/unit/test_vscode_extension_wp54.py::test_g2_vsc_006_adr_rationale`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-VSC-007 [P2] G2-VSC-007: G2-VSC-007

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1624-1626` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-VSC-007
Support `WHY`, `WHAT CHANGED`, `IMPACT`, `WHERE USED` quick actions.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Support WHY, WHAT CHANGED, IMPACT, WHERE USED quick actions.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_find_vsc_specs.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_find_vsc_specs.py#L14-L14), [`scripts/_inspect_vsc_reqs.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_inspect_vsc_reqs.py#L6-L6), [`scripts/_mark_wp54_and_wp55_done.py:49`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp54_and_wp55_done.py#L49-L49)
- tests: `tests/unit/test_vscode_extension_wp54.py:11`, `tests/unit/test_vscode_extension_wp54.py::test_g2_vsc_007_quick_actions`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-VSC-008 [P2] G2-VSC-008: G2-VSC-008

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1627-1631` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-VSC-008
Never require unrestricted raw telemetry access in editor.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Never require unrestricted raw telemetry access in editor.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_find_vsc_specs.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_find_vsc_specs.py#L14-L14), [`scripts/_inspect_vsc_reqs.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_inspect_vsc_reqs.py#L6-L6), [`scripts/_mark_wp54_and_wp55_done.py:53`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp54_and_wp55_done.py#L53-L53)
- tests: `tests/unit/test_vscode_extension_wp54.py:12`, `tests/unit/test_vscode_extension_wp54.py::test_g2_vsc_008_bounded_telemetry_semantics`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-CAP-006 [P3] G2-CAP-006: G2-CAP-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1308-1312` (heading) · **Type:** Functional · **Severity:** Low
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-CAP-006
Capsules MAY be exportable in an approved local package format.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Capsules MAY be exportable in an approved local package format.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/capsules.py:227`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/capsules.py#L227-L227), [`scripts/_mark_wp44_done.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L14-L14)
- tests: `tests/unit/test_capsules.py:118`, `tests/unit/test_capsules.py::test_capsule_export_package_format_g2_cap_006`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVENT-004 [P3] G2-EVENT-004: G2-EVENT-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:841-843` (heading) · **Type:** Functional · **Severity:** Low
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EVENT-004
Support local in-process implementation initially; broker abstraction MAY be added later.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Support local in-process implementation initially; broker abstraction MAY be added later.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L7-L7), [`scripts/update_wp22_registry.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L24-L24)
- tests: `tests/unit/test_semantic_consumers_reconciliation.py:29`, `tests/unit/test_semantic_consumers_reconciliation.py::test_default_semantic_consumers_process_each_cursor_once`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

