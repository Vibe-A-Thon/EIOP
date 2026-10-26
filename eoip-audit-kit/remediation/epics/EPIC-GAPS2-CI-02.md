# EPIC-GAPS2-CI-02: EOIP-engg-doc-pkg/gaps2-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 60 tasks, ~30.0 h, priorities {'P2': 60}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-G2-ARCHC-001 [P2] G2-ARCHC-001: G2-ARCHC-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1107-1112` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCHC-001
Maintain separate views for:
- intended architecture,
- implemented/static architecture,
- observed runtime architecture.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Maintain separate views for: - intended architecture, - implemented/static architecture, - observed runtime architecture.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L9-L9), [`packages/eoip/graph/conformance.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/conformance.py#L1-L1)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:6`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ARCHC-002 [P2] G2-ARCHC-002: G2-ARCHC-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1113-1115` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCHC-002
Define architecture policy DSL or declarative rules.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Define architecture policy DSL or declarative rules.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/rule_catalog.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/rule_catalog.py#L1-L1), [`scripts/tick_phase0_phase1.py:19`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L19-L19)
- tests: `tests/unit/test_conformance.py:9`, `tests/unit/test_conformance.py::test_parse_rules_basic`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ARCHC-004 [P2] G2-ARCHC-004: G2-ARCHC-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1123-1125` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCHC-004
Compile rules into bounded graph validations.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Compile rules into bounded graph validations.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:19`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L19-L19)
- tests: `tests/unit/test_conformance.py:87`, `tests/unit/test_conformance.py::test_check_conformance_all_pass`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ARCHC-005 [P2] G2-ARCHC-005: G2-ARCHC-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1126-1128` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCHC-005
Report exact violating graph path.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Report exact violating graph path.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:19`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L19-L19)
- tests: `tests/unit/test_conformance.py:97`, `tests/unit/test_conformance.py::test_check_conformance_with_failure`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ARCHC-006 [P2] G2-ARCHC-006: G2-ARCHC-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1129-1131` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCHC-006
Map violations to source files/symbols/commits where possible.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Map violations to source files/symbols/commits where possible.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:19`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L19-L19)
- tests: `tests/unit/test_conformance.py:97`, `tests/unit/test_conformance.py::test_check_conformance_with_failure`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ARCHC-007 [P2] G2-ARCHC-007: G2-ARCHC-007

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1132-1134` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCHC-007
Expose violations in Web UI and VS Code.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Expose violations in Web UI and VS Code.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:19`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L19-L19)
- tests: `tests/unit/test_conformance.py:109`, `tests/unit/test_conformance.py::test_api_conformance_check_dsl`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ARCHC-008 [P2] G2-ARCHC-008: G2-ARCHC-008

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1135-1137` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCHC-008
Support CI gate mode.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Support CI gate mode.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:19`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L19-L19)
- tests: `tests/unit/test_conformance.py:167`, `tests/unit/test_conformance.py::test_api_conformance_ruleset_and_catalog`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-ARCHC-009 [P2] G2-ARCHC-009: G2-ARCHC-009

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1138-1142` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-ARCHC-009
Track architecture debt trend.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Track architecture debt trend.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:19`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L19-L19)
- tests: `tests/unit/test_conformance.py:167`, `tests/unit/test_conformance.py::test_api_conformance_ruleset_and_catalog`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-CAP-001 [P2] G2-CAP-001: G2-CAP-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1278-1288` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-CAP-001
Capsule definition SHALL specify:
- root entities,
- traversal rules,
- max depth,
- domains,
- time window,
- trust threshold,
- evidence inclusion,
- security policy.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Capsule definition SHALL specify: - root entities, - traversal rules, - max depth, - domains, - time window, - trust threshold, - evidence inclusion, - security policy.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/main.py:925`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/main.py#L925-L925), [`packages/eoip/gaps/g2_readiness.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L10-L10), [`packages/eoip/graph/capsules.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/capsules.py#L1-L1)
- tests: `tests/unit/test_capsules.py:1`, `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:7`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-CAP-002 [P2] G2-CAP-002: G2-CAP-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1289-1291` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-CAP-002
Capsules SHALL be reproducible against a graph version.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Capsules SHALL be reproducible against a graph version.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp44_done.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L10-L10)
- tests: `tests/unit/test_capsules.py:63`, `tests/unit/test_capsules.py::test_capsule_is_reproducible_g2_cap_002`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-CAP-003 [P2] G2-CAP-003: G2-CAP-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1292-1294` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-CAP-003
Capsules SHALL reduce unnecessary context exposure to AI agents.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Capsules SHALL reduce unnecessary context exposure to AI agents.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp44_done.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L11-L11)
- tests: `tests/unit/test_capsules.py:73`, `tests/unit/test_capsules.py::test_capsule_reduces_context_exposure_g2_cap_003`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-CAP-004 [P2] G2-CAP-004: G2-CAP-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1295-1297` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-CAP-004
Capsules SHALL include manifest and evidence references.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Capsules SHALL include manifest and evidence references.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp44_done.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L12-L12)
- tests: `tests/unit/test_capsules.py:90`, `tests/unit/test_capsules.py::test_capsule_includes_manifest_and_evidence_g2_cap_004`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-CAP-005 [P2] G2-CAP-005: G2-CAP-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1298-1307` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-CAP-005
Example capsules:
- release,
- incident,
- service,
- application,
- change request,
- architecture review,
- audit evidence.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Example capsules: - release, - incident, - service, - application, - change request, - architecture review, - audit evidence.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/capsules.py:271`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/capsules.py#L271-L271), [`scripts/_mark_wp44_done.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L13-L13)
- tests: `tests/unit/test_capsules.py:102`, `tests/unit/test_capsules.py::test_capsule_example_types_g2_cap_005`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-CAUSE-001 [P2] G2-CAUSE-001: G2-CAUSE-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1147-1149` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-CAUSE-001
Represent correlation separately from causal hypotheses.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Represent correlation separately from causal hypotheses.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L11-L11), [`packages/eoip/graph/causal.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/causal.py#L1-L1)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:8`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-CAUSE-002 [P2] G2-CAUSE-002: G2-CAUSE-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1150-1156` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-CAUSE-002
Relationship classes:
- `CORRELATED_WITH`
- `POSSIBLY_CAUSED`
- `EVIDENCE_SUPPORTS_CAUSE`
- `HUMAN_CONFIRMED_CAUSE`
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Relationship classes: - CORRELATED_WITH - POSSIBLY_CAUSED - EVIDENCE_SUPPORTS_CAUSE - HUMAN_CONFIRMED_CAUSE
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L6-L6)
- tests: `tests/unit/test_causal_reasoning.py:45`, `tests/unit/test_causal_reasoning.py::test_causal_relationship_classes_and_hypotheses`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-CAUSE-003 [P2] G2-CAUSE-003: G2-CAUSE-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1157-1159` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-CAUSE-003
AI SHALL NOT silently promote correlation into confirmed causality.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] AI SHALL NOT silently promote correlation into confirmed causality.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L12-L12)
- tests: `tests/unit/test_causal_reasoning.py:54`, `tests/unit/test_causal_reasoning.py::test_causal_hypotheses_no_silent_promotion_to_confirmed`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-CAUSE-004 [P2] G2-CAUSE-004: G2-CAUSE-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1160-1167` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-CAUSE-004
Causal hypotheses SHALL include:
- evidence,
- time ordering,
- alternative explanations,
- confidence,
- review status.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Causal hypotheses SHALL include: - evidence, - time ordering, - alternative explanations, - confidence, - review status.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:18`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L18-L18)
- tests: `tests/unit/test_causal_reasoning.py:66`, `tests/unit/test_causal_reasoning.py::test_causal_hypothesis_structure_and_alternatives`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-CAUSE-005 [P2] G2-CAUSE-005: G2-CAUSE-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1168-1170` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-CAUSE-005
Use deployment/telemetry/incident relationships to propose bounded hypotheses.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Use deployment/telemetry/incident relationships to propose bounded hypotheses.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L24-L24)
- tests: `tests/unit/test_causal_reasoning.py:78`, `tests/unit/test_causal_reasoning.py::test_temporal_correlations_and_time_ordering`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-CAUSE-006 [P2] G2-CAUSE-006: G2-CAUSE-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1171-1175` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-CAUSE-006
Human confirmation/rejection SHALL be preserved.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Human confirmation/rejection SHALL be preserved.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:30`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L30-L30)
- tests: `tests/unit/test_causal_reasoning.py:88`, `tests/unit/test_causal_reasoning.py::test_human_confirmation_and_rejection_preserved`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-002 [P2] G2-EKAF-002: Connector SDK

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:175-186` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-002 — Connector SDK
Provide a stable SDK with:
- `discover()`,
- `baseline()`,
- `poll_changes()`,
- `handle_event()`,
- `fetch_record()`,
- `fetch_children()`,
- `checkpoint()`,
- `health()`,
- `capabilities()`.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Provide a stable SDK with: - discover(), - baseline(), - poll_changes(), - handle_event(), - fetch_record(), - fetch_children(), - checkpoint(), - health(), - capabilities().
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/patch_contracts_tags.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_contracts_tags.py#L7-L7), [`scripts/tick_phase2_batch1.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L9-L9)
- tests: `tests/contract/test_g2_contracts.py:144`, `tests/contract/test_g2_contracts.py::test_fake_connector_satisfies_runtime_connector_protocol`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-007 [P2] G2-EKAF-007: Poll fallback

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:218-220` (heading) · **Type:** Functional · **Severity:** Low
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-007 — Poll fallback
Every event-driven connector SHOULD support incremental polling as reconciliation/fallback where the source permits it.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Every event-driven connector SHOULD support incremental polling as reconciliation/fallback where the source permits it.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L9-L9)
- tests: `tests/unit/test_acquisition_fabric.py:34`, `tests/unit/test_acquisition_fabric.py::test_scheduler_admits_all_operation_types_and_enforces_controls`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-008 [P2] G2-EKAF-008: Reconciliation crawl

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:221-223` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-008 — Reconciliation crawl
Periodic reconciliation SHALL compare source state/checksums/cursors with EOIP state and repair missed events.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Periodic reconciliation SHALL compare source state/checksums/cursors with EOIP state and repair missed events.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L10-L10)
- tests: `tests/unit/test_acquisition_fabric.py:34`, `tests/unit/test_acquisition_fabric.py::test_scheduler_admits_all_operation_types_and_enforces_controls`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-010 [P2] G2-EKAF-010: Ordering tolerance

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:227-229` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 13, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-010 — Ordering tolerance
Connectors SHALL tolerate delayed/out-of-order events using source versions/event timestamps where available.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Connectors SHALL tolerate delayed/out-of-order events using source versions/event timestamps where available.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/inspect_wp21_reqs.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_reqs.py#L9-L9), [`scripts/inspect_wp21_tasks.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_tasks.py#L6-L6), [`scripts/read_g2_specs.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_g2_specs.py#L7-L7), [`scripts/update_wp21_registry.py:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp21_registry.py#L17-L17)
- tests: `tests/unit/test_graph_evolution.py:30`, `tests/unit/test_graph_evolution.py::test_entity_evolution_is_idempotent_temporal_and_late_event_safe`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-011 [P2] G2-EKAF-011: Rate limiting

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:230-237` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-011 — Rate limiting
Connector framework SHALL support:
- source rate limits,
- adaptive backoff,
- retry-after,
- concurrency limits,
- per-source budgets.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Connector framework SHALL support: - source rate limits, - adaptive backoff, - retry-after, - concurrency limits, - per-source budgets.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L10-L10)
- tests: `tests/unit/test_acquisition_fabric.py:34`, `tests/unit/test_acquisition_fabric.py::test_scheduler_admits_all_operation_types_and_enforces_controls`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-012 [P2] G2-EKAF-012: Checkpointing

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:238-240` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-012 — Checkpointing
Checkpoints SHALL advance only after downstream graph mutation commits.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Checkpoints SHALL advance only after downstream graph mutation commits.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L10-L10)
- tests: `tests/unit/test_acquisition_fabric.py:68`, `tests/unit/test_acquisition_fabric.py::test_baseline_controller_persists_ordered_restart_manifest`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-013 [P2] G2-EKAF-013: Replay

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:241-249` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-013 — Replay
An operator SHALL be able to replay:
- one event,
- one record,
- one time window,
- one ingestion run,
- one source,
without requiring a full graph rebuild.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] An operator SHALL be able to replay: - one event, - one record, - one time window, - one ingestion run, - one source, without requiring a full graph rebuild.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L10-L10)
- tests: `tests/unit/test_acquisition_fabric.py:34`, `tests/unit/test_acquisition_fabric.py::test_scheduler_admits_all_operation_types_and_enforces_controls`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-014 [P2] G2-EKAF-014: Dead-letter handling

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:250-258` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-014 — Dead-letter handling
Failed events SHALL enter a local DLQ with:
- failure category,
- source event,
- mapping/parser version,
- stack/correlation ID,
- retry state,
- remediation note.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Failed events SHALL enter a local DLQ with: - failure category, - source event, - mapping/parser version, - stack/correlation ID, - retry state, - remediation note.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/inspect_wp21_reqs.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_reqs.py#L9-L9), [`scripts/inspect_wp21_tasks.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_tasks.py#L6-L6), [`scripts/read_g2_specs.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_g2_specs.py#L7-L7), [`scripts/update_wp21_registry.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp21_registry.py#L24-L24)
- tests: `tests/unit/test_phase2_ingestion.py:315`, `tests/unit/test_phase2_ingestion.py::test_dead_letter_handling_contract`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-015 [P2] G2-EKAF-015: Dry run

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:259-261` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-015 — Dry run
Every connector/mapping SHALL support a dry-run mode that produces proposed canonical mutations without modifying the graph.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Every connector/mapping SHALL support a dry-run mode that produces proposed canonical mutations without modifying the graph.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L11-L11)
- tests: `tests/unit/test_acquisition_fabric.py:325`, `tests/unit/test_acquisition_fabric.py::test_source_operation_api_queues_registry_scoped_job`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-016 [P2] G2-EKAF-016: Source deletion semantics

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:262-264` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 13, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-016 — Source deletion semantics
Deletion/archival SHALL expire current facts while retaining historical provenance.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Deletion/archival SHALL expire current facts while retaining historical provenance.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/inspect_wp21_reqs.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_reqs.py#L9-L9), [`scripts/inspect_wp21_tasks.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_tasks.py#L6-L6), [`scripts/read_g2_specs.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_g2_specs.py#L7-L7), [`scripts/update_wp21_registry.py:31`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp21_registry.py#L31-L31)
- tests: `tests/unit/test_graph_evolution.py:167`, `tests/unit/test_graph_evolution.py::test_deletion_is_a_temporal_barrier_for_entity_and_relationship_replay`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-017 [P2] G2-EKAF-017: Schema drift

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:265-271` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-017 — Schema drift
EKAF SHALL detect source payload/schema changes and classify:
- additive,
- compatible,
- potentially breaking,
- breaking.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] EKAF SHALL detect source payload/schema changes and classify: - additive, - compatible, - potentially breaking, - breaking.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/connectors/drift.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/drift.py#L1-L1)
- tests: `tests/unit/test_ekaf_drift.py:13`, `tests/unit/test_ekaf_drift.py::test_payload_schema_is_stable_and_escapes_path_separators`, `tests/unit/test_ekaf_drift.py::test_schema_drift_classifies_compatible_and_additive_payloads`, `tests/unit/test_ekaf_drift.py::test_schema_drift_classifies_removed_or_container_changes_as_breaking`, `tests/unit/test_ekaf_drift.py::test_schema_drift_classifies_scalar_changes_as_potentially_breaking`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-018 [P2] G2-EKAF-018: Mapping drift

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:272-274` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-018 — Mapping drift
A mapping version change SHALL be traceable and replayable.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] A mapping version change SHALL be traceable and replayable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/connectors/drift.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/drift.py#L1-L1)
- tests: `tests/unit/test_ekaf_drift.py:72`, `tests/unit/test_ekaf_drift.py::test_mapping_drift_ledger_records_version_changes_and_builds_replay_plan`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-019 [P2] G2-EKAF-019: Crawl boundaries

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:275-286` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-019 — Crawl boundaries
Controlled web crawling SHALL enforce:
- allowed hosts,
- allowed path prefixes,
- excluded path patterns,
- maximum depth,
- maximum pages,
- content type limits,
- size limits,
- concurrency,
- politeness/rate limits.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Controlled web crawling SHALL enforce: - allowed hosts, - allowed path prefixes, - excluded path patterns, - maximum depth, - maximum pages, - content type limits, - size limits, - concurrency, - politeness/rate limits.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L11-L11)
- tests: `tests/unit/test_acquisition_fabric.py:209`, `tests/unit/test_acquisition_fabric.py::test_controlled_crawler_enforces_rate_and_politeness_controls`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-021 [P2] G2-EKAF-021: Connector health

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:290-300` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-021 — Connector health
Expose:
- last success,
- last failure,
- lag,
- freshness,
- error rate,
- throughput,
- checkpoint,
- rate-limit status.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Expose: - last success, - last failure, - lag, - freshness, - error rate, - throughput, - checkpoint, - rate-limit status.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L11-L11)
- tests: `tests/unit/test_source_registry.py:52`, `tests/unit/test_source_registry.py::test_registry_entry_carries_g2_operational_metadata_without_secrets`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-022 [P2] G2-EKAF-022: Source priority

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:301-303` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 2, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-022 — Source priority
When two sources assert conflicting facts, the acquisition layer SHALL preserve both claims and defer truth resolution to the trust layer.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] When two sources assert conflicting facts, the acquisition layer SHALL preserve both claims and defer truth resolution to the trust layer.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/connectors/conflicts.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/conflicts.py#L1-L1)
- tests: `tests/unit/test_ekaf_conflicts.py:8`, `tests/unit/test_ekaf_conflicts.py::test_acquisition_marks_non_conflicting_claim_sets_as_preserved_not_conflicting`, `tests/unit/test_ekaf_conflicts.py::test_acquisition_preserves_conflicting_source_claims_without_resolution`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-024 [P2] G2-EKAF-024: Content fingerprinting

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:307-309` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 13, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-024 — Content fingerprinting
Use stable hashing to skip unchanged content.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Content fingerprinting Use stable hashing to skip unchanged content.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/inspect_wp21_reqs.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_reqs.py#L10-L10), [`scripts/inspect_wp21_tasks.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_tasks.py#L6-L6), [`scripts/read_g2_specs.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_g2_specs.py#L8-L8), [`scripts/update_wp21_registry.py:45`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp21_registry.py#L45-L45)
- tests: `tests/unit/test_graph_evolution.py:30`, `tests/unit/test_graph_evolution.py::test_entity_evolution_is_idempotent_temporal_and_late_event_safe`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-025 [P2] G2-EKAF-025: Attachment handling

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:310-318` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-025 — Attachment handling
Attachments SHALL be:
- classified,
- size-limited,
- hashed,
- safely parsed,
- linked to parent records,
- quarantined when unsafe/unparseable.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Attachments SHALL be: - classified, - size-limited, - hashed, - safely parsed, - linked to parent records, - quarantined when unsafe/unparseable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/inspect_wp21_reqs.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_reqs.py#L10-L10), [`scripts/inspect_wp21_tasks.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_tasks.py#L6-L6), [`scripts/read_g2_specs.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_g2_specs.py#L8-L8), [`scripts/update_wp21_registry.py:52`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp21_registry.py#L52-L52)
- tests: `tests/unit/test_file_ingestion.py:18`, `tests/unit/test_file_ingestion.py::test_binary_connector_scope_and_limits`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-026 [P2] G2-EKAF-026: Incremental graph enrichment

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:319-321` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-026 — Incremental graph enrichment
A new source connection SHALL enrich existing canonical entities rather than create a disconnected duplicate domain.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] A new source connection SHALL enrich existing canonical entities rather than create a disconnected duplicate domain.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/inspect_wp21_reqs.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_reqs.py#L10-L10), [`scripts/inspect_wp21_tasks.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_tasks.py#L6-L6), [`scripts/read_g2_specs.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_g2_specs.py#L8-L8), [`scripts/update_wp21_registry.py:59`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp21_registry.py#L59-L59)
- tests: `tests/unit/test_identity_resolver.py:28`, `tests/unit/test_identity_resolver.py::test_same_person_by_email`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-028 [P2] G2-EKAF-028: Connector compatibility matrix

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:334-336` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-028 — Connector compatibility matrix
Maintain tested source-product/API versions.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Connector compatibility matrix Maintain tested source-product/API versions.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L12-L12)
- tests: `tests/unit/test_source_registry.py:52`, `tests/unit/test_source_registry.py::test_registry_entry_carries_g2_operational_metadata_without_secrets`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EKAF-029 [P2] G2-EKAF-029: Offline source fixture mode

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:337-339` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-029 — Offline source fixture mode
Every production connector SHALL have fixture/synthetic mode for local deterministic testing.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Every production connector SHALL have fixture/synthetic mode for local deterministic testing.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L12-L12)
- tests: `tests/unit/test_acquisition_fabric.py:325`, `tests/unit/test_acquisition_fabric.py::test_source_operation_api_queues_registry_scoped_job`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVENT-001 [P2] G2-EVENT-001: G2-EVENT-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:832-834` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EVENT-001
Events SHALL have stable versioned schemas.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Events SHALL have stable versioned schemas.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L13-L13)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:10`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVENT-005 [P2] G2-EVENT-005: G2-EVENT-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:844-854` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EVENT-005
Consumers may include:
- search index,
- vector index,
- GraphRAG community summaries,
- semantic cache,
- dashboards,
- quality metrics,
- agents,
- alerts.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Consumers may include: - search index, - vector index, - GraphRAG community summaries, - semantic cache, - dashboards, - quality metrics, - agents, - alerts.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L7-L7), [`scripts/update_wp22_registry.py:31`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L31-L31)
- tests: `tests/unit/test_semantic_consumers_reconciliation.py:29`, `tests/unit/test_semantic_consumers_reconciliation.py::test_default_semantic_consumers_process_each_cursor_once`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVENT-007 [P2] G2-EVENT-007: G2-EVENT-007

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:858-862` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EVENT-007
Support replay from journal/checkpoint.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Support replay from journal/checkpoint.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/read_wp22_specs.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/read_wp22_specs.py#L7-L7), [`scripts/update_wp22_registry.py:45`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_wp22_registry.py#L45-L45)
- tests: `tests/unit/test_semantic_consumers_reconciliation.py:29`, `tests/unit/test_semantic_consumers_reconciliation.py::test_default_semantic_consumers_process_each_cursor_once`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVOL-001 [P2] G2-EVOL-001: G2-EVOL-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:703-705` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-EVOL-001
Every mutable canonical entity SHALL support revision metadata.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Every mutable canonical entity SHALL support revision metadata.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L14-L14)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:11`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVOL-002 [P2] G2-EVOL-002: G2-EVOL-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:706-710` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-EVOL-002
Every mutable relationship SHALL support validity interval:
- `valid_from`,
- `valid_to`.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Every mutable relationship SHALL support validity interval: - valid_from, - valid_to.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:38`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L38-L38)
- tests: `tests/unit/test_graph_evolution_family.py:35`, `tests/unit/test_graph_evolution_family.py::test_evolve_relationship_validity_interval`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVOL-003 [P2] G2-EVOL-003: G2-EVOL-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:711-713` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-EVOL-003
Store observation/system time separately from business/event-valid time where meaningful.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Store observation/system time separately from business/event-valid time where meaningful.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:44`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L44-L44)
- tests: `tests/unit/test_graph_evolution_family.py:52`, `tests/unit/test_graph_evolution_family.py::test_observation_time_separated_from_event_time`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVOL-004 [P2] G2-EVOL-004: G2-EVOL-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:714-716` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-EVOL-004
A relationship removal SHALL expire the previous assertion rather than erase history.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] A relationship removal SHALL expire the previous assertion rather than erase history.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:50`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L50-L50)
- tests: `tests/unit/test_graph_evolution_family.py:72`, `tests/unit/test_graph_evolution_family.py::test_relationship_removal_expires_assertion_without_erasing_history`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVOL-005 [P2] G2-EVOL-005: G2-EVOL-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:717-719` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-EVOL-005
A relationship update SHALL be represented as a new revision/assertion.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] A relationship update SHALL be represented as a new revision/assertion.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:56`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L56-L56)
- tests: `tests/unit/test_graph_evolution_family.py:93`, `tests/unit/test_graph_evolution_family.py::test_relationship_update_represented_as_new_revision`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVOL-006 [P2] G2-EVOL-006: G2-EVOL-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:720-722` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-EVOL-006
Current views SHALL exclude expired facts unless explicitly requested.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Current views SHALL exclude expired facts unless explicitly requested.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:62`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L62-L62)
- tests: `tests/unit/test_graph_evolution_family.py:110`, `tests/unit/test_graph_evolution_family.py::test_current_views_exclude_expired_facts`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVOL-007 [P2] G2-EVOL-007: G2-EVOL-007

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:723-725` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-EVOL-007
Historical queries SHALL reconstruct state at time T.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Historical queries SHALL reconstruct state at time T.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:68`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L68-L68)
- tests: `tests/unit/test_graph_evolution_family.py:123`, `tests/unit/test_graph_evolution_family.py::test_historical_as_of_reconstruction`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVOL-008 [P2] G2-EVOL-008: G2-EVOL-008

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:726-735` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-EVOL-008
Provide graph diff:
- added entities,
- changed entities,
- removed/retired entities,
- added edges,
- expired edges,
- changed properties,
- trust changes.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Provide graph diff: - added entities, - changed entities, - removed/retired entities, - added edges, - expired edges, - changed properties, - trust changes.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:74`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L74-L74)
- tests: `tests/unit/test_graph_evolution_family.py:137`, `tests/unit/test_graph_evolution_family.py::test_graph_diff_between_timestamps`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVOL-009 [P2] G2-EVOL-009: G2-EVOL-009

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:736-742` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-EVOL-009
Every graph mutation SHALL reference:
- SourceEvent,
- ingestion run,
- mapping/parser version,
- ontology version.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Every graph mutation SHALL reference: - SourceEvent, - ingestion run, - mapping/parser version, - ontology version.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/contracts/revision.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/contracts/revision.py#L1-L1), [`scripts/update_phase3_wp32_wp33.py:80`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L80-L80)
- tests: `tests/unit/test_graph_evolution_family.py:149`, `tests/unit/test_graph_evolution_family.py::test_graph_mutation_source_references`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVOL-010 [P2] G2-EVOL-010: G2-EVOL-010

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:743-745` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 21, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-EVOL-010
Graph mutation batches SHALL be atomic at an appropriate bounded unit.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Graph mutation batches SHALL be atomic at an appropriate bounded unit.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:86`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L86-L86)
- tests: `tests/unit/test_bulk_load.py:1`, `tests/unit/test_bulk_load.py::test_hugegraph_bulk_load_uses_bounded_native_batches`, `tests/unit/test_bulk_load.py::test_memory_bulk_load_validates_then_commits_atomically`, `tests/unit/test_graph_evolution_family.py:161`, `tests/unit/test_graph_evolution_family.py::test_atomic_batch_isolation`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVOL-011 [P2] G2-EVOL-011: G2-EVOL-011

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:746-748` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-EVOL-011
Failed mutation batch SHALL not advance source checkpoint.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Failed mutation batch SHALL not advance source checkpoint.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:92`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L92-L92)
- tests: `tests/unit/test_graph_evolution_family.py:171`, `tests/unit/test_graph_evolution_family.py::test_failed_batch_does_not_advance_checkpoint`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVOL-012 [P2] G2-EVOL-012: G2-EVOL-012

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:749-751` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-EVOL-012
Relationship preservation SHALL mean “preserve history,” not “keep stale edges active.”
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Relationship preservation SHALL mean “preserve history,” not “keep stale edges active.”
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:98`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L98-L98)
- tests: `tests/unit/test_graph_evolution_family.py:182`, `tests/unit/test_graph_evolution_family.py::test_relationship_preservation_means_history_not_stale_edges`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVOL-013 [P2] G2-EVOL-013: G2-EVOL-013

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:752-754` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-EVOL-013
Support previous-revision links or revision identifiers.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Support previous-revision links or revision identifiers.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:104`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L104-L104)
- tests: `tests/unit/test_graph_evolution_family.py:197`, `tests/unit/test_graph_evolution_family.py::test_previous_revision_links`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVOL-014 [P2] G2-EVOL-014: G2-EVOL-014

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:755-757` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-EVOL-014
Support tombstone/retired status for source objects no longer current.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Support tombstone/retired status for source objects no longer current.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:110`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L110-L110)
- tests: `tests/unit/test_graph_evolution_family.py:211`, `tests/unit/test_graph_evolution_family.py::test_tombstone_retired_status`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-EVOL-016 [P2] G2-EVOL-016: G2-EVOL-016

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:761-770` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-EVOL-016
Schema/ontology migration SHALL explicitly declare whether existing facts require:
- no migration,
- lazy migration,
- online backfill,
- offline migration,
- source replay.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Schema/ontology migration SHALL explicitly declare whether existing facts require: - no migration, - lazy migration, - online backfill, - offline migration, - source replay.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:122`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L122-L122)
- tests: `tests/unit/test_graph_evolution_family.py:241`, `tests/unit/test_graph_evolution_family.py::test_schema_ontology_migration_strategy`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-API-001 [P2] G2-GRAPH-API-001: G2-GRAPH-API-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:867-869` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-API-001
Model APIs, versions, endpoints/operations, schemas, owners, providers, consumers and compatibility.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Model APIs, versions, endpoints/operations, schemas, owners, providers, consumers and compatibility.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L15-L15), [`packages/eoip/graph/api_contracts.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/api_contracts.py#L1-L1)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:12`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-API-002 [P2] G2-GRAPH-API-002: G2-GRAPH-API-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:870-878` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-API-002
Link contracts to:
- source symbols,
- services,
- docs,
- tests,
- deployments,
- consumers.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Link contracts to: - source symbols, - services, - docs, - tests, - deployments, - consumers.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/api_contracts.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/api_contracts.py#L24-L24), [`scripts/_mark_wp44_done.py:30`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L30-L30)
- tests: `tests/unit/test_g2_domain_graphs.py:24`, `tests/unit/test_g2_domain_graphs.py::test_g2_graph_api_002_contract_linking`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-API-003 [P2] G2-GRAPH-API-003: G2-GRAPH-API-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:879-883` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-API-003
Track breaking/non-breaking contract changes.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Track breaking/non-breaking contract changes.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/api_contracts.py:108`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/api_contracts.py#L108-L108), [`scripts/_mark_wp44_done.py:31`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L31-L31)
- tests: `tests/unit/test_g2_domain_graphs.py:55`, `tests/unit/test_g2_domain_graphs.py::test_g2_graph_api_003_breaking_changes`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

