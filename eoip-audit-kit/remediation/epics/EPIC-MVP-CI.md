# EPIC-MVP-CI: EOIP-engg-doc-pkg/MVP-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 11 tasks, ~5.5 h, priorities {'P0': 1, 'P1': 10}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-MVP-FR-023 [P0] MVP-FR-023: Logging

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:200-205` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-023 — Logging
**Parent requirements:** NFR-OPS-001  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Correlation-aware structured logs cover startup, ingestion, query, validation, RAG/agent and failures without secrets.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Correlation-aware structured logs cover startup, ingestion, query, validation, RAG/agent and failures without secrets.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Correlation-aware structured logs cover startup, ingestion, query, validation, RAG/agent and failures without secrets
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_check_wp72.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L14-L14), [`scripts/_mark_wp72_done.py:112`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L112-L112), [`scripts/build_master_suite.py:513`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L513-L513)
- tests: `scripts/test_unified_triage.py:119`, `tests/unit/test_performance_reliability_and_operations_wp72.py:30`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_mvp_fr_023_logging`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-MVP-FR-001 [P1] MVP-FR-001: Apache HugeGraph local Docker

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:68-73` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-001 — Apache HugeGraph local Docker
**Parent requirements:** FR-GRAPH-001  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** HugeGraph starts from Compose, persists through restart, and is reachable only through the internal network by default.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] HugeGraph starts from Compose, persists through restart, and is reachable only through the internal network by default.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] HugeGraph starts from Compose, persists through restart, and is reachable only through the internal network by default
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/verify_requirement_evidence.py:159`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_requirement_evidence.py#L159-L159)
- tests: `tests/unit/test_requirement_evidence.py:73`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-MVP-FR-019 [P1] MVP-FR-019: VS Code extension

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:176-181` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-019 — VS Code extension
**Parent requirements:** FR-VSCODE-001, FR-VSCODE-002  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Opening the demo symbol retrieves Jira/commit/dependency/doc/evidence context and exact source range.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Opening the demo symbol retrieves Jira/commit/dependency/doc/evidence context and exact source range.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Opening the demo symbol retrieves Jira/commit/dependency/doc/evidence context and exact source range
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_find_vsc_specs.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_find_vsc_specs.py#L15-L15), [`scripts/_inspect_vsc_reqs.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_inspect_vsc_reqs.py#L7-L7), [`scripts/_mark_wp54_and_wp55_done.py:57`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp54_and_wp55_done.py#L57-L57), [`scripts/build_master_suite.py:505`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L505-L505)
- tests: `scripts/test_unified_triage.py:111`, `tests/unit/test_vscode_extension_wp54.py:13`, `tests/unit/test_vscode_extension_wp54.py::test_mvp_fr_019_extension_delivery`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-MVP-FR-020 [P1] MVP-FR-020: Local GraphRAG

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:182-187` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-020 — Local GraphRAG
**Parent requirements:** FR-RAG-001, FR-RAG-002, FR-RAG-003  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** GraphRAG retrieves real graph/doc evidence and returns citations; with model down it returns structured evidence/fallback.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] GraphRAG retrieves real graph/doc evidence and returns citations; with model down it returns structured evidence/fallback.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] GraphRAG retrieves real graph/doc evidence and returns citations; with model down it returns structured evidence/fallback
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:22`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L22-L22)
- tests: `tests/unit/test_retrieval.py:48`, `tests/unit/test_retrieval.py::test_code_context_preserves_relationship_evidence`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-MVP-FR-021 [P1] MVP-FR-021: Useful read-only agent workflow

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:188-193` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-021 — Useful read-only agent workflow
**Parent requirements:** FR-AGENT-003  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** TraceImpactAgent answers the demo trace/impact request using allowlisted read tools and remains within execution budgets.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] TraceImpactAgent answers the demo trace/impact request using allowlisted read tools and remains within execution budgets.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] TraceImpactAgent answers the demo trace/impact request using allowlisted read tools and remains within execution budgets
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:262`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L262-L262)
- tests: `tests/unit/test_governed_agents.py:121`, `tests/unit/test_governed_agents.py::test_useful_read_only_agent_workflow`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-MVP-FR-022 [P1] MVP-FR-022: MCP core graph access

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:194-199` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-022 — MCP core graph access
**Parent requirements:** FR-MCP-001, FR-MCP-002  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** MCP client obtains the same entity/path/impact/evidence semantics as REST; no write tool is advertised.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] MCP client obtains the same entity/path/impact/evidence semantics as REST; no write tool is advertised.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] MCP client obtains the same entity/path/impact/evidence semantics as REST; no write tool is advertised
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:22`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L22-L22)
- tests: `tests/security/test_verification_suite.py:168`, `tests/security/test_verification_suite.py::test_mcp_tool_surface_is_read_only`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-MVP-FR-024 [P1] MVP-FR-024: Metrics

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:206-211` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-024 — Metrics
**Parent requirements:** NFR-OPS-002  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Machine-readable metrics expose ingestion/query/model/agent/failure counters/latencies locally.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Machine-readable metrics expose ingestion/query/model/agent/failure counters/latencies locally.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Machine-readable metrics expose ingestion/query/model/agent/failure counters/latencies locally
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_check_wp72.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L14-L14), [`scripts/_mark_wp72_done.py:116`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L116-L116), [`scripts/build_master_suite.py:513`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L513-L513)
- tests: `scripts/test_unified_triage.py:119`, `tests/unit/test_performance_reliability_and_operations_wp72.py:31`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_mvp_fr_024_metrics`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-MVP-FR-025 [P1] MVP-FR-025: Backup

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:212-217` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-025 — Backup
**Parent requirements:** NFR-REL-002  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** A checksummed graph/application backup artifact is generated from the demo environment.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] A checksummed graph/application backup artifact is generated from the demo environment.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] A checksummed graph/application backup artifact is generated from the demo environment
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_check_wp72.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L14-L14), [`scripts/_mark_wp72_done.py:120`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L120-L120), [`scripts/build_master_suite.py:513`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L513-L513)
- tests: `scripts/test_unified_triage.py:119`, `tests/unit/test_performance_reliability_and_operations_wp72.py:32`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_mvp_fr_025_backup`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-MVP-FR-026 [P1] MVP-FR-026: Restore

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:218-223` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-026 — Restore
**Parent requirements:** NFR-REL-002  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Restore into a clean graph reproduces expected counts and golden path/impact queries.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Restore into a clean graph reproduces expected counts and golden path/impact queries.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Restore into a clean graph reproduces expected counts and golden path/impact queries
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_check_wp72.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L14-L14), [`scripts/_mark_wp72_done.py:124`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L124-L124), [`scripts/build_master_suite.py:513`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L513-L513)
- tests: `scripts/test_unified_triage.py:119`, `tests/unit/test_performance_reliability_and_operations_wp72.py:33`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_mvp_fr_026_restore`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-MVP-FR-027 [P1] MVP-FR-027: Automated tests

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:224-229` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 29, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-027 — Automated tests
**Parent requirements:** NFR-MAINT-001  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Unit, contract, integration, security and E2E suites execute locally and produce a report.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Unit, contract, integration, security and E2E suites execute locally and produce a report.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Unit, contract, integration, security and E2E suites execute locally and produce a report
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L7-L7)
- tests: `tests/unit/test_validation_source_binding.py:32`, `tests/unit/test_validation_source_binding.py::test_executes_command_and_persists_source_bound_fresh_artifact`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-MVP-FR-028 [P1] MVP-FR-028: End-to-end demo

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:230-235` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 25, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-028 — End-to-end demo
**Parent requirements:** FR-GRAPH-006, FR-AGENT-003  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** A documented clean-reset demo executes ingestion→graph→query→UI→VS Code→GraphRAG→MCP→backup/restore from persisted data.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] A documented clean-reset demo executes ingestion→graph→query→UI→VS Code→GraphRAG→MCP→backup/restore from persisted data.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] A documented clean-reset demo executes ingestion→graph→query→UI→VS Code→GraphRAG→MCP→backup/restore from persisted data
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/verification/release_gate.py:106`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/verification/release_gate.py#L106-L106), [`scripts/_mark_wp8_done.py:72`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp8_done.py#L72-L72), [`scripts/build_master_suite.py:509`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L509-L509), [`scripts/verify_requirement_evidence.py:159`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_requirement_evidence.py#L159-L159)
- tests: `scripts/test_unified_triage.py:115`, `tests/e2e/test_demo_flow.py:1`, `tests/unit/test_production_release_gate_wp8.py:20`, `tests/unit/test_production_release_gate_wp8.py::test_mvp_fr_028_cross_domain_traceability_evidence`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

