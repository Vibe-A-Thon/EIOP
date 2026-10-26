# EPIC-GAPS2-CI-03: EOIP-engg-doc-pkg/gaps2-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 60 tasks, ~30.0 h, priorities {'P2': 60}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-G2-GRAPH-BIZ-001 [P2] G2-GRAPH-BIZ-001: G2-GRAPH-BIZ-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:984-993` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-BIZ-001
Represent:
- BusinessObjective,
- BusinessCapability,
- Requirement,
- Product,
- Application,
- Service,
- Owner.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Represent: - BusinessObjective, - BusinessCapability, - Requirement, - Product, - Application, - Service, - Owner.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L16-L16), [`packages/eoip/graph/business_intent.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/business_intent.py#L1-L1)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:13`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-BIZ-002 [P2] G2-GRAPH-BIZ-002: G2-GRAPH-BIZ-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:994-996` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-BIZ-002
Link business intent through technical implementation and runtime.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Link business intent through technical implementation and runtime.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp44_done.py:32`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L32-L32)
- tests: `tests/unit/test_g2_domain_graphs.py:88`, `tests/unit/test_g2_domain_graphs.py::test_g2_graph_biz_002_intent_to_technical`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-BIZ-003 [P2] G2-GRAPH-BIZ-003: G2-GRAPH-BIZ-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:997-1002` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-BIZ-003
Support reverse query:
“Which business capabilities are affected if Service X fails?”

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Support reverse query: “Which business capabilities are affected if Service X fails?”
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp44_done.py:33`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L33-L33)
- tests: `tests/unit/test_g2_domain_graphs.py:104`, `tests/unit/test_g2_domain_graphs.py::test_g2_graph_biz_003_reverse_query`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-DEC-001 [P2] G2-GRAPH-DEC-001: G2-GRAPH-DEC-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:949-960` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-DEC-001
Represent:
- Decision,
- Alternative,
- Constraint,
- Rationale,
- Evidence,
- Approver,
- Affected Architecture,
- Implementation,
- Outcome.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Represent: - Decision, - Alternative, - Constraint, - Rationale, - Evidence, - Approver, - Affected Architecture, - Implementation, - Outcome.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L17-L17), [`packages/eoip/graph/decisions.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/decisions.py#L1-L1)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:14`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-DEC-002 [P2] G2-GRAPH-DEC-002: G2-GRAPH-DEC-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:961-963` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-DEC-002
Link ADRs/design decisions to code/architecture/releases.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Link ADRs/design decisions to code/architecture/releases.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp44_done.py:34`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L34-L34)
- tests: `tests/unit/test_g2_domain_graphs.py:119`, `tests/unit/test_g2_domain_graphs.py::test_g2_graph_dec_002_adr_links`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-DEC-003 [P2] G2-GRAPH-DEC-003: G2-GRAPH-DEC-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:964-968` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-DEC-003
Support “Why was this architecture chosen?” queries.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Support “Why was this architecture chosen?” queries.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp44_done.py:35`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L35-L35)
- tests: `tests/unit/test_g2_domain_graphs.py:139`, `tests/unit/test_g2_domain_graphs.py::test_g2_graph_dec_003_why_architecture`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-OBS-001 [P2] G2-GRAPH-OBS-001: G2-GRAPH-OBS-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:886-898` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-OBS-001
Model:
- Dashboard,
- Panel,
- Metric,
- LogPattern,
- ErrorSignature,
- Monitor,
- Alert,
- TraceEvidence,
- SLO,
- Service.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Model: - Dashboard, - Panel, - Metric, - LogPattern, - ErrorSignature, - Monitor, - Alert, - TraceEvidence, - SLO, - Service.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:18`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L18-L18)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:15`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-OBS-002 [P2] G2-GRAPH-OBS-002: G2-GRAPH-OBS-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:899-901` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-OBS-002
Link runtime evidence to deployments/incidents/services.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Link runtime evidence to deployments/incidents/services.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_observability.py:97`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_observability.py#L97-L97), [`scripts/_mark_wp44_done.py:36`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L36-L36)
- tests: `tests/unit/test_g2_domain_graphs.py:159`, `tests/unit/test_g2_domain_graphs.py::test_g2_graph_obs_002_link_runtime_evidence`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-OBS-003 [P2] G2-GRAPH-OBS-003: G2-GRAPH-OBS-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:902-906` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-OBS-003
Relationships SHALL have bounded observation windows and evidence.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Relationships SHALL have bounded observation windows and evidence.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp44_done.py:37`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L37-L37)
- tests: `tests/unit/test_g2_domain_graphs.py:180`, `tests/unit/test_g2_domain_graphs.py::test_g2_graph_obs_003_bounded_observation_window`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-PROC-001 [P2] G2-GRAPH-PROC-001: G2-GRAPH-PROC-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:971-973` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-PROC-001
Derive process events from Jira/ServiceNow/CI/CD where configured.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Derive process events from Jira/ServiceNow/CI/CD where configured.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:19`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L19-L19)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:16`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-PROC-002 [P2] G2-GRAPH-PROC-002: G2-GRAPH-PROC-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:974-976` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-PROC-002
Represent designed and observed process flows separately.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Represent designed and observed process flows separately.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp44_done.py:38`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L38-L38)
- tests: `tests/unit/test_g2_domain_graphs.py:200`, `tests/unit/test_g2_domain_graphs.py::test_g2_graph_proc_002_designed_vs_observed`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-PROC-003 [P2] G2-GRAPH-PROC-003: G2-GRAPH-PROC-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:977-981` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-PROC-003
Identify skipped steps, loops, bottlenecks and deviations.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Identify skipped steps, loops, bottlenecks and deviations.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp44_done.py:39`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L39-L39)
- tests: `tests/unit/test_g2_domain_graphs.py:225`, `tests/unit/test_g2_domain_graphs.py::test_g2_graph_proc_003_deviations_and_bottlenecks`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-RUNTIME-001 [P2] G2-GRAPH-RUNTIME-001: G2-GRAPH-RUNTIME-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:909-911` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-RUNTIME-001
Represent implemented runtime topology independently from intended architecture.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Represent implemented runtime topology independently from intended architecture.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:20`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L20-L20), [`packages/eoip/graph/runtime_topology.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/runtime_topology.py#L1-L1)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:17`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-RUNTIME-002 [P2] G2-GRAPH-RUNTIME-002: G2-GRAPH-RUNTIME-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:912-914` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-RUNTIME-002
Support temporal service-to-service relationships.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Support temporal service-to-service relationships.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/runtime_topology.py:23`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/runtime_topology.py#L23-L23), [`scripts/_mark_wp44_done.py:40`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L40-L40)
- tests: `tests/unit/test_g2_domain_graphs.py:248`, `tests/unit/test_g2_domain_graphs.py::test_g2_graph_runtime_002_temporal_service_calls`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-RUNTIME-003 [P2] G2-GRAPH-RUNTIME-003: G2-GRAPH-RUNTIME-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:915-919` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-RUNTIME-003
Compare runtime relationships with static code dependencies.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Compare runtime relationships with static code dependencies.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/runtime_topology.py:50`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/runtime_topology.py#L50-L50), [`scripts/_mark_wp44_done.py:41`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L41-L41)
- tests: `tests/unit/test_g2_domain_graphs.py:269`, `tests/unit/test_g2_domain_graphs.py::test_g2_graph_runtime_003_compare_runtime_vs_static`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-TEST-001 [P2] G2-GRAPH-TEST-001: G2-GRAPH-TEST-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:935-938` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-TEST-001
Represent:
`Requirement → Code Symbol → Test → TestRun → Build → Release`.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Represent: Requirement → Code Symbol → Test → TestRun → Build → Release.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:22`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L22-L22)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:19`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-TEST-002 [P2] G2-GRAPH-TEST-002: G2-GRAPH-TEST-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:939-941` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-TEST-002
Support change-based test impact analysis.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Support change-based test impact analysis.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp44_done.py:44`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L44-L44)
- tests: `tests/unit/test_g2_domain_graphs.py:326`, `tests/unit/test_g2_domain_graphs.py::test_g2_graph_test_002_change_impact_analysis`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-GRAPH-TEST-003 [P2] G2-GRAPH-TEST-003: G2-GRAPH-TEST-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:942-946` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-GRAPH-TEST-003
Track test coverage relationship confidence/source.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Track test coverage relationship confidence/source.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp44_done.py:45`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L45-L45)
- tests: `tests/unit/test_g2_domain_graphs.py:343`, `tests/unit/test_g2_domain_graphs.py::test_g2_graph_test_003_test_coverage_confidence_provenance`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-I2R-001 [P2] G2-I2R-001: G2-I2R-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1348-1351` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-I2R-001
Support the chain:
`Business Objective → Capability → Requirement → Decision → Jira → Code → API → Test → Build → Deployment → Runtime → Telemetry → Incident/Outcome`.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Support the chain: Business Objective → Capability → Requirement → Decision → Jira → Code → API → Test → Build → Deployment → Runtime → Telemetry → Incident/Outcome.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:23`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L23-L23)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:20`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-I2R-002 [P2] G2-I2R-002: G2-I2R-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1352-1354` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-I2R-002
Support reverse traversal.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Support reverse traversal.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp44_done.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L24-L24)
- tests: `tests/unit/test_i2r_intelligence.py:1`, `tests/unit/test_i2r_intelligence.py::test_reverse_traversal_g2_i2r_002`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-I2R-003 [P2] G2-I2R-003: G2-I2R-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1355-1357` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-I2R-003
Compute coverage for missing links.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Compute coverage for missing links.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp44_done.py:25`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L25-L25)
- tests: `tests/unit/test_i2r_intelligence.py:33`, `tests/unit/test_i2r_intelligence.py::test_compute_coverage_for_missing_links_g2_i2r_003`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-I2R-004 [P2] G2-I2R-004: G2-I2R-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1358-1360` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-I2R-004
Flag critical production assets without business/requirement ownership.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Flag critical production assets without business/requirement ownership.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/business_intent.py:232`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/business_intent.py#L232-L232), [`scripts/_mark_wp44_done.py:26`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L26-L26)
- tests: `tests/unit/test_i2r_intelligence.py:52`, `tests/unit/test_i2r_intelligence.py::test_flag_unowned_production_assets_g2_i2r_004`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-I2R-005 [P2] G2-I2R-005: G2-I2R-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1361-1365` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-I2R-005
Flag business-critical requirements without runtime traceability.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Flag business-critical requirements without runtime traceability.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/business_intent.py:253`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/business_intent.py#L253-L253), [`scripts/_mark_wp44_done.py:27`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L27-L27)
- tests: `tests/unit/test_i2r_intelligence.py:77`, `tests/unit/test_i2r_intelligence.py::test_flag_untraced_critical_requirements_g2_i2r_005`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-IMMUNE-001 [P2] G2-IMMUNE-001: G2-IMMUNE-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1180-1182` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-IMMUNE-001
Detect orphan nodes.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Detect orphan nodes.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L24-L24), [`packages/eoip/graph/immune_system.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/immune_system.py#L1-L1)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:21`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-IMMUNE-002 [P2] G2-IMMUNE-002: G2-IMMUNE-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1183-1185` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-IMMUNE-002
Detect missing mandatory relationships.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Detect missing mandatory relationships.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/immune_system.py:5`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/immune_system.py#L5-L5), [`scripts/_check_wp62.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp62.py#L8-L8), [`scripts/_find_specs.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_find_specs.py#L7-L7), [`scripts/_mark_wp62_done.py:44`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp62_done.py#L44-L44)
- tests: `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:13`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py::test_g2_immune_002_missing_mandatory_relationships`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-IMMUNE-003 [P2] G2-IMMUNE-003: G2-IMMUNE-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1186-1188` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-IMMUNE-003
Detect contradictory claims.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Detect contradictory claims.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/immune_system.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/immune_system.py#L6-L6), [`scripts/_check_wp62.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp62.py#L8-L8), [`scripts/_mark_wp62_done.py:48`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp62_done.py#L48-L48)
- tests: `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:14`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py::test_g2_immune_003_contradictory_claims`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-IMMUNE-004 [P2] G2-IMMUNE-004: G2-IMMUNE-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1189-1191` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-IMMUNE-004
Detect stale documentation.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Detect stale documentation.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/immune_system.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/immune_system.py#L7-L7), [`scripts/_check_wp62.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp62.py#L8-L8), [`scripts/_mark_wp62_done.py:52`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp62_done.py#L52-L52)
- tests: `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:15`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py::test_g2_immune_004_stale_documentation`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-IMMUNE-005 [P2] G2-IMMUNE-005: G2-IMMUNE-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1192-1194` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-IMMUNE-005
Detect source/schema/mapping drift.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Detect source/schema/mapping drift.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/immune_system.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/immune_system.py#L8-L8), [`scripts/_check_wp62.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp62.py#L8-L8), [`scripts/_mark_wp62_done.py:56`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp62_done.py#L56-L56)
- tests: `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:16`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py::test_g2_immune_005_schema_drift`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-IMMUNE-006 [P2] G2-IMMUNE-006: G2-IMMUNE-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1195-1197` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-IMMUNE-006
Detect unexpected architecture edges.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Detect unexpected architecture edges.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/immune_system.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/immune_system.py#L9-L9), [`scripts/_check_wp62.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp62.py#L8-L8), [`scripts/_mark_wp62_done.py:60`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp62_done.py#L60-L60)
- tests: `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:17`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py::test_g2_immune_006_unexpected_architecture_edges`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-IMMUNE-007 [P2] G2-IMMUNE-007: G2-IMMUNE-007

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1198-1200` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-IMMUNE-007
Detect missing ownership.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Detect missing ownership.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/immune_system.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/immune_system.py#L10-L10), [`scripts/_check_wp62.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp62.py#L9-L9), [`scripts/_mark_wp62_done.py:64`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp62_done.py#L64-L64)
- tests: `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:18`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py::test_g2_immune_007_missing_ownership`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-IMMUNE-008 [P2] G2-IMMUNE-008: G2-IMMUNE-008

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1201-1203` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-IMMUNE-008
Detect broken provenance/evidence references.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Detect broken provenance/evidence references.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/immune_system.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/immune_system.py#L11-L11), [`scripts/_check_wp62.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp62.py#L9-L9), [`scripts/_mark_wp62_done.py:68`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp62_done.py#L68-L68)
- tests: `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:19`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py::test_g2_immune_008_broken_provenance`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-IMMUNE-009 [P2] G2-IMMUNE-009: G2-IMMUNE-009

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1204-1206` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-IMMUNE-009
Detect suspicious/low-confidence AI-inferred relationships.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Detect suspicious/low-confidence AI-inferred relationships.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/immune_system.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/immune_system.py#L12-L12), [`scripts/_check_wp62.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp62.py#L9-L9), [`scripts/_mark_wp62_done.py:72`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp62_done.py#L72-L72)
- tests: `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:20`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py::test_g2_immune_009_suspicious_ai_relationships`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-IMMUNE-010 [P2] G2-IMMUNE-010: G2-IMMUNE-010

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1207-1209` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-IMMUNE-010
Detect graph poisoning patterns/untrusted source anomalies.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Detect graph poisoning patterns/untrusted source anomalies.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/immune_system.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/immune_system.py#L13-L13), [`scripts/_check_wp62.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp62.py#L9-L9), [`scripts/_mark_wp62_done.py:76`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp62_done.py#L76-L76)
- tests: `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:21`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py::test_g2_immune_010_graph_poisoning_anomalies`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-IMMUNE-011 [P2] G2-IMMUNE-011: G2-IMMUNE-011

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1210-1212` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-IMMUNE-011
Recommend repair, quarantine, re-ingestion or human review.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Recommend repair, quarantine, re-ingestion or human review.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/immune_system.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/immune_system.py#L14-L14), [`scripts/_check_wp62.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp62.py#L9-L9), [`scripts/_mark_wp62_done.py:80`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp62_done.py#L80-L80)
- tests: `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:22`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py::test_g2_immune_011_quarantine_and_action_recommendation`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-IMMUNE-012 [P2] G2-IMMUNE-012: G2-IMMUNE-012

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1213-1215` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-IMMUNE-012
Trusted knowledge SHALL NOT be silently rewritten by the immune system.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Trusted knowledge SHALL NOT be silently rewritten by the immune system.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/immune_system.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/immune_system.py#L15-L15), [`scripts/_check_wp62.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp62.py#L10-L10), [`scripts/_mark_wp62_done.py:84`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp62_done.py#L84-L84)
- tests: `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:23`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py::test_g2_immune_012_non_silent_rewrite_policy`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-IMMUNE-013 [P2] G2-IMMUNE-013: G2-IMMUNE-013

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1216-1220` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-IMMUNE-013
Every recommendation SHALL explain why it was generated.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Every recommendation SHALL explain why it was generated.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/immune_system.py:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/immune_system.py#L16-L16), [`scripts/_check_wp62.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp62.py#L10-L10), [`scripts/_mark_wp62_done.py:88`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp62_done.py#L88-L88)
- tests: `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:24`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py::test_g2_immune_013_verifiable_explanatory_rationale`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-JOURNAL-001 [P2] G2-JOURNAL-001: G2-JOURNAL-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:773-775` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-JOURNAL-001
Maintain an append-oriented local change journal for source and graph changes.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Maintain an append-oriented local change journal for source and graph changes.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:25`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L25-L25)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:22`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-JOURNAL-002 [P2] G2-JOURNAL-002: G2-JOURNAL-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:776-788` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-JOURNAL-002
Record:
- event ID,
- source,
- canonical entity,
- before hash,
- after hash,
- mutation type,
- changed fields/edges,
- timestamps,
- causal source event,
- graph version.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Record: - event ID, - source, - canonical entity, - before hash, - after hash, - mutation type, - changed fields/edges, - timestamps, - causal source event, - graph version.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:130`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L130-L130)
- tests: `tests/unit/test_change_journal_family.py:12`, `tests/unit/test_change_journal_family.py::test_journal_record_schema_and_integrity`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-JOURNAL-003 [P2] G2-JOURNAL-003: G2-JOURNAL-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:789-796` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-JOURNAL-003
Support query by:
- source,
- entity,
- time,
- release,
- ingestion run.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Support query by: - source, - entity, - time, - release, - ingestion run.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:136`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L136-L136)
- tests: `tests/unit/test_change_journal_family.py:46`, `tests/unit/test_change_journal_family.py::test_journal_query_by_entity_time_and_run`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-JOURNAL-004 [P2] G2-JOURNAL-004: G2-JOURNAL-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:797-799` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-JOURNAL-004
Journal SHALL support replay into derived indexes/services.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Journal SHALL support replay into derived indexes/services.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:142`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L142-L142)
- tests: `tests/unit/test_change_journal_family.py:77`, `tests/unit/test_change_journal_family.py::test_journal_replay_into_derived_indices`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-JOURNAL-005 [P2] G2-JOURNAL-005: G2-JOURNAL-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:800-802` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-JOURNAL-005
Journal retention SHALL be configurable.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Journal retention SHALL be configurable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:148`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L148-L148)
- tests: `tests/unit/test_change_journal_family.py:105`, `tests/unit/test_change_journal_family.py::test_journal_configurable_retention`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-JOURNAL-006 [P2] G2-JOURNAL-006: G2-JOURNAL-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:803-807` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-JOURNAL-006
Journal data SHALL be included in audit/incident troubleshooting.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Journal data SHALL be included in audit/incident troubleshooting.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:154`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L154-L154)
- tests: `tests/unit/test_change_journal_family.py:127`, `tests/unit/test_change_journal_family.py::test_journal_audit_incident_troubleshooting`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-KD-001 [P2] G2-KD-001: G2-KD-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1368-1370` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-KD-001
Represent Knowledge Debt Finding as a first-class record.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Represent Knowledge Debt Finding as a first-class record.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:26`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L26-L26), [`packages/eoip/graph/knowledge_debt.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/knowledge_debt.py#L1-L1)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:23`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-KD-002 [P2] G2-KD-002: G2-KD-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1371-1385` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 21, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-KD-002
Categories:
- unowned component,
- undocumented API,
- unlinked requirement,
- unlinked implementation,
- stale document,
- unresolved identity,
- broken provenance,
- low-confidence critical inference,
- missing test,
- missing architecture mapping,
- unknown production owner,
- stale runbook.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Categories: - unowned component, - undocumented API, - unlinked requirement, - unlinked implementation, - stale document, - unresolved identity, - broken provenance, - low-confidence critical inference, - missing test, - missing architecture mapping, - unknown production owner, - stale runbook.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp44_done.py:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L17-L17)
- tests: `tests/unit/test_knowledge_debt.py:89`, `tests/unit/test_knowledge_debt.py::test_all_twelve_debt_categories_detected_g2_kd_002`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-KD-003 [P2] G2-KD-003: G2-KD-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1386-1394` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 21, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-KD-003
Compute debt by:
- project,
- team,
- service,
- application,
- domain,
- release.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Compute debt by: - project, - team, - service, - application, - domain, - release.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/knowledge_debt.py:94`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/knowledge_debt.py#L94-L94), [`scripts/_mark_wp44_done.py:18`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L18-L18)
- tests: `tests/unit/test_knowledge_debt.py:124`, `tests/unit/test_knowledge_debt.py::test_debt_computed_by_dimensions_g2_kd_003`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-KD-004 [P2] G2-KD-004: G2-KD-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1395-1397` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 21, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-KD-004
Avoid one opaque debt score; expose contributing dimensions.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Avoid one opaque debt score; expose contributing dimensions.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/knowledge_debt.py:105`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/knowledge_debt.py#L105-L105), [`scripts/_mark_wp44_done.py:19`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L19-L19)
- tests: `tests/unit/test_knowledge_debt.py:154`, `tests/unit/test_knowledge_debt.py::test_multidimensional_debt_facets_g2_kd_004`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-KD-005 [P2] G2-KD-005: G2-KD-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1398-1400` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 21, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-KD-005
Support debt trend over time.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Support debt trend over time.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/knowledge_debt.py:131`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/knowledge_debt.py#L131-L131), [`scripts/_mark_wp44_done.py:20`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L20-L20)
- tests: `tests/unit/test_knowledge_debt.py:171`, `tests/unit/test_knowledge_debt.py::test_debt_trend_tracking_g2_kd_005`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-KD-006 [P2] G2-KD-006: G2-KD-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1401-1405` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 21, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-KD-006
Link every finding to remediation action/evidence.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Link every finding to remediation action/evidence.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp44_done.py:21`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp44_done.py#L21-L21)
- tests: `tests/unit/test_knowledge_debt.py:188`, `tests/unit/test_knowledge_debt.py::test_findings_link_remediation_and_evidence_g2_kd_006`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-OEVO-001 [P2] G2-OEVO-001: G2-OEVO-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1223-1225` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-OEVO-001
Detect recurring unmapped entity/relationship patterns.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Detect recurring unmapped entity/relationship patterns.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:28`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L28-L28), [`packages/eoip/ontology/drift.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/drift.py#L1-L1)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:25`, `tests/unit/test_ontology_drift_review.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-OEVO-002 [P2] G2-OEVO-002: G2-OEVO-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1226-1228` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-OEVO-002
Propose new class/property/relationship definitions.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Propose new class/property/relationship definitions.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:162`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L162-L162)
- tests: `tests/unit/test_ontology_evolution_family.py:17`, `tests/unit/test_ontology_evolution_family.py::test_propose_new_ontology_definitions`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-OEVO-003 [P2] G2-OEVO-003: G2-OEVO-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1229-1237` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-OEVO-003
Proposals SHALL include:
- evidence count,
- examples,
- candidate parent/class,
- proposed constraints,
- impact analysis,
- migration/backfill requirement.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Proposals SHALL include: - evidence count, - examples, - candidate parent/class, - proposed constraints, - impact analysis, - migration/backfill requirement.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:168`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L168-L168)
- tests: `tests/unit/test_ontology_evolution_family.py:42`, `tests/unit/test_ontology_evolution_family.py::test_proposal_contents_and_impact_analysis`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-OEVO-004 [P2] G2-OEVO-004: G2-OEVO-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1238-1240` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-OEVO-004
Ontology changes require configured human review/approval.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Ontology changes require configured human review/approval.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:174`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L174-L174)
- tests: `tests/unit/test_ontology_evolution_family.py:61`, `tests/unit/test_ontology_evolution_family.py::test_ontology_changes_require_human_review_and_governance`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-OEVO-005 [P2] G2-OEVO-005: G2-OEVO-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1241-1243` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-OEVO-005
Approved ontology changes SHALL enter existing Ontology GitOps workflow.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Approved ontology changes SHALL enter existing Ontology GitOps workflow.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:180`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L180-L180)
- tests: `tests/unit/test_ontology_evolution_family.py:94`, `tests/unit/test_ontology_evolution_family.py::test_approved_ontology_changes_enter_gitops_workflow`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-OEVO-006 [P2] G2-OEVO-006: G2-OEVO-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1244-1248` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-OEVO-006
Rejected suggestions SHALL remain available as training/evaluation feedback without becoming facts.

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Rejected suggestions SHALL remain available as training/evaluation feedback without becoming facts.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:186`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L186-L186)
- tests: `tests/unit/test_ontology_evolution_family.py:122`, `tests/unit/test_ontology_evolution_family.py::test_rejected_suggestions_preserved_as_feedback`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-PERF-001 [P2] G2-PERF-001: G2-PERF-001

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1735-1737` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-PERF-001
Baseline ingestion throughput SHALL be measured per source type.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Baseline ingestion throughput SHALL be measured per source type.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gaps/g2_readiness.py:29`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gaps/g2_readiness.py#L29-L29)
- tests: `tests/unit/test_g2_readiness.py`, `tests/unit/test_g2_readiness.py:26`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-PERF-002 [P2] G2-PERF-002: G2-PERF-002

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1738-1740` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-PERF-002
Incremental update latency SHALL be measured separately.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Incremental update latency SHALL be measured separately.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/benchmark.py:227`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/benchmark.py#L227-L227), [`scripts/_check_wp72.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L10-L10), [`scripts/_mark_wp72_done.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L12-L12)
- tests: `tests/unit/test_performance_reliability_and_operations_wp72.py:5`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_g2_perf_002_incremental_update_latency_measured`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-PERF-003 [P2] G2-PERF-003: G2-PERF-003

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1741-1743` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-PERF-003
Graph mutation throughput SHALL be benchmarked.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Graph mutation throughput SHALL be benchmarked.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_check_wp72.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L10-L10), [`scripts/_mark_wp72_done.py:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L16-L16)
- tests: `tests/unit/test_performance_reliability_and_operations_wp72.py:6`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_g2_perf_003_graph_mutation_throughput_benchmarked`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-PERF-004 [P2] G2-PERF-004: G2-PERF-004

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1744-1746` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-PERF-004
Historical-state reconstruction latency SHALL be benchmarked.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Historical-state reconstruction latency SHALL be benchmarked.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_check_wp72.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L10-L10), [`scripts/_mark_wp72_done.py:20`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L20-L20)
- tests: `tests/unit/test_performance_reliability_and_operations_wp72.py:7`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_g2_perf_004_historical_state_reconstruction_latency`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-PERF-005 [P2] G2-PERF-005: G2-PERF-005

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1747-1749` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-PERF-005
Graph diff latency SHALL be benchmarked.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Graph diff latency SHALL be benchmarked.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_check_wp72.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L10-L10), [`scripts/_mark_wp72_done.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L24-L24)
- tests: `tests/unit/test_performance_reliability_and_operations_wp72.py:8`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_g2_perf_005_graph_diff_latency_benchmarked`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-G2-PERF-006 [P2] G2-PERF-006: G2-PERF-006

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:1750-1752` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
## G2-PERF-006
Crawler concurrency SHALL be source-configurable.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Crawler concurrency SHALL be source-configurable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ingest/incremental_crawler.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ingest/incremental_crawler.py#L1-L1), [`scripts/_check_wp72.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L10-L10), [`scripts/_mark_wp72_done.py:28`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L28-L28)
- tests: `tests/unit/test_performance_reliability_and_operations_wp72.py:9`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_g2_perf_006_crawler_concurrency_source_configurable`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

