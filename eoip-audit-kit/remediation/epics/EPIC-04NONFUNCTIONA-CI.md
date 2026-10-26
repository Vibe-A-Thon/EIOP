# EPIC-04NONFUNCTIONA-CI: EOIP-engg-doc-pkg/04-non-functional-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 13 tasks, ~8.8 h, priorities {'P0': 5, 'P1': 8}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-NFR-PRIV-001 [P0] NFR-PRIV-001: Data minimization and classification

- **Source:** `EOIP-engg-doc-pkg/04-non-functional-requirements.md:141-152` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 36, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-PRIV-001 — Data minimization and classification
**WHAT:** Capture only required source fields and classify sensitive content.  
**WHY:** Local operation still requires privacy discipline.  
**HOW:** Connector mappings define allow/deny/redaction; logs never copy document bodies by default.  
**DATA / INTERFACES:** Source mapping/classification  
**FAILURE:** Unknown sensitive field defaults to protected handling.  
**TEST:** Redaction fixtures.  
**COMPLETE WHEN:** Audit/log exports contain no prohibited content.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Capture only required source fields and classify sensitive content.
- [ ] Interfaces: Source mapping/classification
- [ ] Failure behaviour: Unknown sensitive field defaults to protected handling.
- [ ] Verified by: Redaction fixtures.
- [ ] Complete when: Audit/log exports contain no prohibited content.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L24-L24)
- tests: `tests/unit/test_agent_memory.py:1`, `tests/unit/test_agent_memory.py::test_scope_and_owner_are_exact_and_export_keeps_classification`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-NFR-SEC-001 [P0] NFR-SEC-001: No outbound enterprise-data egress

- **Source:** `EOIP-engg-doc-pkg/04-non-functional-requirements.md:11-20` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 42, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-NFR-SEC-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-SEC-001 — No outbound enterprise-data egress
**WHAT:** Disable external LLM/API egress by default and document firewall/Docker network controls.  
**WHY:** Enterprise data must remain local.  
**HOW:** MVP services need no internet at runtime after images/models are staged.  
**DATA / INTERFACES:** Network policy/config  
**FAILURE:** Blocked egress fails closed; audit safe error.  
**TEST:** Egress test with deny network.  
**COMPLETE WHEN:** Demo succeeds with external network disabled.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-NFR-SEC-001

**Acceptance criteria**
- [ ] Delivers: Disable external LLM/API egress by default and document firewall/Docker network controls.
- [ ] Interfaces: Network policy/config
- [ ] Failure behaviour: Blocked egress fails closed; audit safe error.
- [ ] Verified by: Egress test with deny network.
- [ ] Complete when: Demo succeeds with external network disabled.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/moonshot/federated_graph.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/moonshot/federated_graph.py#L6-L6), [`scripts/tick_phase0_phase1.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L24-L24)
- tests: `tests/security/test_no_egress.py:1`, `tests/security/test_no_egress.py::test_backend_network_is_internal`, `tests/security/test_verification_suite.py:1`, `tests/security/test_verification_suite.py::test_mcp_tool_surface_is_read_only`, `tests/security/test_verification_suite.py::test_prompt_injection_is_ingested_as_data_and_never_executed`, `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py:536`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-NFR-SEC-002 [P0] NFR-SEC-002: Secret isolation

- **Source:** `EOIP-engg-doc-pkg/04-non-functional-requirements.md:21-30` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-SEC-002 — Secret isolation
**WHAT:** Credentials are never hardcoded/logged and use mounted secret files/env references.  
**WHY:** Connector/model/admin secrets require protection.  
**HOW:** Secret loader resolves file references; redaction filter protects logs.  
**DATA / INTERFACES:** SecretRef  
**FAILURE:** Missing secret fails connector without exposing value.  
**TEST:** Secret scan/log redaction tests.  
**COMPLETE WHEN:** Repository and logs contain no test secret plaintext.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Credentials are never hardcoded/logged and use mounted secret files/env references.
- [ ] Failure behaviour: Missing secret fails connector without exposing value.
- [ ] Verified by: Secret scan/log redaction tests.
- [ ] Complete when: Repository and logs contain no test secret plaintext.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L24-L24)
- tests: `tests/security/test_verification_suite.py:103`, `tests/security/test_verification_suite.py::test_audit_sink_redacts_canary_secrets_from_jsonl`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-NFR-SEC-004 [P0] NFR-SEC-004: Prompt/tool injection defenses

- **Source:** `EOIP-engg-doc-pkg/04-non-functional-requirements.md:41-50` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-SEC-004 — Prompt/tool injection defenses
**WHAT:** Treat retrieved content as data, not instructions, and validate all tool plans.  
**WHY:** Malicious docs/code can manipulate agents.  
**HOW:** Context delimiters, instruction hierarchy, tool allowlists, QueryPlan schema/policy and output validation.  
**DATA / INTERFACES:** Agent/QueryPlan  
**FAILURE:** Injection attempt cannot add tool or exceed query policy.  
**TEST:** Adversarial evals.  
**COMPLETE WHEN:** Known injection cases remain read-only/bounded.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Treat retrieved content as data, not instructions, and validate all tool plans.
- [ ] Failure behaviour: Injection attempt cannot add tool or exceed query policy.
- [ ] Verified by: Adversarial evals.
- [ ] Complete when: Known injection cases remain read-only/bounded.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L24-L24)
- tests: `tests/security/test_verification_suite.py:63`, `tests/security/test_verification_suite.py::test_mcp_tool_surface_is_read_only`, `tests/security/test_verification_suite.py::test_over_depth_request_is_rejected_with_422`, `tests/security/test_verification_suite.py::test_prompt_injection_is_ingested_as_data_and_never_executed`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-NFR-SEC-007 [P0] NFR-SEC-007: Audit events

- **Source:** `EOIP-engg-doc-pkg/04-non-functional-requirements.md:71-80` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-SEC-007 — Audit events
**WHAT:** Record auth, ingestion, query, agent/tool, admin mutation, backup/restore and policy-denial events.  
**WHY:** Operational accountability is required.  
**HOW:** Structured append-only local audit stream plus selected graph meta references; never private chain-of-thought.  
**DATA / INTERFACES:** AuditEvent v1  
**FAILURE:** Audit write failure blocks high-risk action and alerts; read query may degrade per policy.  
**TEST:** Audit coverage tests.  
**COMPLETE WHEN:** Sensitive operation has traceable audit ID.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Record auth, ingestion, query, agent/tool, admin mutation, backup/restore and policy-denial events.
- [ ] Interfaces: AuditEvent v1
- [ ] Failure behaviour: Audit write failure blocks high-risk action and alerts; read query may degrade per policy.
- [ ] Verified by: Audit coverage tests.
- [ ] Complete when: Sensitive operation has traceable audit ID.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/audit/sink.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/audit/sink.py#L1-L1), [`scripts/tick_phase0_phase1.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L24-L24)
- tests: `tests/security/test_verification_suite.py:103`, `tests/security/test_verification_suite.py::test_audit_sink_redacts_canary_secrets_from_jsonl`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-NFR-MAINT-001 [P1] NFR-MAINT-001: Modular monolith boundary

- **Source:** `EOIP-engg-doc-pkg/04-non-functional-requirements.md:131-140` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-MAINT-001 — Modular monolith boundary
**WHAT:** Use modular monolith services in Phase 1; split only on evidence.  
**WHY:** Avoid premature distributed complexity.  
**HOW:** Domain packages expose typed ports; API/worker/MCP reuse application services.  
**DATA / INTERFACES:** Python package boundaries  
**FAILURE:** Cross-module direct DB access rejected by architecture tests/convention.  
**TEST:** Dependency/lint tests.  
**COMPLETE WHEN:** Core can later split without changing external contracts.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Use modular monolith services in Phase 1; split only on evidence.
- [ ] Interfaces: Python package boundaries
- [ ] Failure behaviour: Cross-module direct DB access rejected by architecture tests/convention.
- [ ] Verified by: Dependency/lint tests.
- [ ] Complete when: Core can later split without changing external contracts.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/store.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/store.py#L1-L1)
- tests: `tests/contract/test_graph_store_contract.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-NFR-OPS-001 [P1] NFR-OPS-001: Structured logging and health

- **Source:** `EOIP-engg-doc-pkg/04-non-functional-requirements.md:101-110` (heading) · **Type:** Infra · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 36, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-NFR-OPS-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-OPS-001 — Structured logging and health
**WHAT:** Expose structured logs, liveness/readiness and correlation IDs locally.  
**WHY:** Troubleshooting must not depend on cloud observability.  
**HOW:** JSON logs to stdout/file, /health/live, /health/ready; correlation spans ingestion/query/agent.  
**DATA / INTERFACES:** LogEvent  
**FAILURE:** Dependency failure makes readiness false.  
**TEST:** Health/log tests.  
**COMPLETE WHEN:** Failure can be followed by correlation ID.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-NFR-OPS-001

**Acceptance criteria**
- [ ] Delivers: Expose structured logs, liveness/readiness and correlation IDs locally.
- [ ] Failure behaviour: Dependency failure makes readiness false.
- [ ] Verified by: Health/log tests.
- [ ] Complete when: Failure can be followed by correlation ID.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/audit/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/audit/__init__.py#L1-L1), [`packages/eoip/audit/redaction.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/audit/redaction.py#L1-L1), [`packages/eoip/audit/sink.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/audit/sink.py#L1-L1), [`packages/eoip/authn/__init__.py:18`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/authn/__init__.py#L18-L18), [`scripts/_check_wp72.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L15-L15), [`scripts/_mark_wp72_done.py:128`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L128-L128)
- tests: `tests/unit/test_observability_import_order.py:8`, `tests/unit/test_observability_import_order.py::test_configure_logging_after_child_module_import`, `tests/unit/test_performance_reliability_and_operations_wp72.py:34`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_nfr_ops_001_structured_logging_and_health`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-NFR-OPS-002 [P1] NFR-OPS-002: Local metrics

- **Source:** `EOIP-engg-doc-pkg/04-non-functional-requirements.md:111-120` (heading) · **Type:** Infra · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 35, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-OPS-002 — Local metrics
**WHAT:** Expose Prometheus-format metrics for ingestion, graph queries, RAG/model, agents, tools and errors.  
**WHY:** Performance/quality claims require measurement.  
**HOW:** App /metrics; Prometheus/Grafana optional profile, not mandatory core.  
**DATA / INTERFACES:** Metric series  
**FAILURE:** Metrics failure does not break core request path.  
**TEST:** Metric scrape tests.  
**COMPLETE WHEN:** Key MVP metrics are machine-readable.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Expose Prometheus-format metrics for ingestion, graph queries, RAG/model, agents, tools and errors.
- [ ] Interfaces: Metric series
- [ ] Failure behaviour: Metrics failure does not break core request path.
- [ ] Verified by: Metric scrape tests.
- [ ] Complete when: Key MVP metrics are machine-readable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_check_wp72.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L15-L15), [`scripts/_mark_wp72_done.py:132`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L132-L132)
- tests: `tests/unit/test_performance_reliability_and_operations_wp72.py:35`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_nfr_ops_002_local_metrics`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-NFR-PERF-001 [P1] NFR-PERF-001: Benchmark-defined objectives

- **Source:** `EOIP-engg-doc-pkg/04-non-functional-requirements.md:121-130` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 47, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-PERF-001 — Benchmark-defined objectives
**WHAT:** Define and run a representative local benchmark before claiming throughput/latency.  
**WHY:** Arbitrary performance claims are prohibited.  
**HOW:** Baseline dataset and hardware profile are versioned; report p50/p95/p99 and resource use.  
**DATA / INTERFACES:** Benchmark manifest/results  
**FAILURE:** Missed targets create tuning issue, not hidden result.  
**TEST:** Automated benchmark smoke + manual full run.  
**COMPLETE WHEN:** Published numbers identify dataset/hardware/version.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Define and run a representative local benchmark before claiming throughput/latency.
- [ ] Interfaces: Benchmark manifest/results
- [ ] Failure behaviour: Missed targets create tuning issue, not hidden result.
- [ ] Verified by: Automated benchmark smoke + manual full run.
- [ ] Complete when: Published numbers identify dataset/hardware/version.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/benchmark.py:194`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/benchmark.py#L194-L194), [`scripts/_check_wp72.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L15-L15), [`scripts/_mark_wp72_done.py:136`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L136-L136), [`scripts/benchmark.py:460`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/benchmark.py#L460-L460), [`scripts/benchmark_data.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/benchmark_data.py#L1-L1)
- tests: `tests/performance/test_benchmark_publication.py:1`, `tests/performance/test_benchmarks.py:76`, `tests/unit/test_performance_reliability_and_operations_wp72.py:36`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_nfr_perf_001_benchmark_defined_objectives`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-NFR-REL-001 [P1] NFR-REL-001: Restart-safe processing

- **Source:** `EOIP-engg-doc-pkg/04-non-functional-requirements.md:81-90` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 39, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-NFR-REL-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-REL-001 — Restart-safe processing
**WHAT:** Workers recover from crash using checkpoints and idempotent graph mutations.  
**WHY:** Local containers will restart.  
**HOW:** Run state persists to mounted state volume/meta graph.  
**DATA / INTERFACES:** Checkpoint/IngestionRun  
**FAILURE:** Unclean shutdown detected and resumed/reconciled.  
**TEST:** Kill/restart E2E.  
**COMPLETE WHEN:** No duplicates or silent skipped records after restart.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-NFR-REL-001

**Acceptance criteria**
- [ ] Delivers: Workers recover from crash using checkpoints and idempotent graph mutations.
- [ ] Failure behaviour: Unclean shutdown detected and resumed/reconciled.
- [ ] Verified by: Kill/restart E2E.
- [ ] Complete when: No duplicates or silent skipped records after restart.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_check_wp72.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L15-L15), [`scripts/_mark_wp72_done.py:140`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L140-L140)
- tests: `tests/e2e/test_restart_safe.py:1`, `tests/unit/test_performance_reliability_and_operations_wp72.py:37`, `tests/unit/test_performance_reliability_and_operations_wp72.py::test_nfr_rel_001_restart_safe_processing`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-NFR-REL-002 [P1] NFR-REL-002: Backup and restore

- **Source:** `EOIP-engg-doc-pkg/04-non-functional-requirements.md:91-100` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 99, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.8 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-REL-002 — Backup and restore
**WHAT:** Provide repeatable graph schema+data backup and restore plus config/raw-state backup guidance.  
**WHY:** MVP acceptance explicitly requires recovery.  
**HOW:** Use HugeGraph-supported tooling for graph export/restore and checksummed archive; run scripted verification query.  
**DATA / INTERFACES:** Backup manifest  
**FAILURE:** Failed backup never marked successful; restore uses clean target/test mode.  
**TEST:** Backup/restore E2E.  
**COMPLETE WHEN:** Restored demo reproduces expected counts/path queries.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Provide repeatable graph schema+data backup and restore plus config/raw-state backup guidance.
- [ ] Interfaces: Backup manifest
- [ ] Failure behaviour: Failed backup never marked successful; restore uses clean target/test mode.
- [ ] Verified by: Backup/restore E2E.
- [ ] Complete when: Restored demo reproduces expected counts/path queries.
- [ ] DATA / INTERFACES: Backup manifest
- [ ] FAILURE: Failed backup never marked successful; restore uses clean target/test mode
- [ ] COMPLETE WHEN: Restored demo reproduces expected counts/path queries
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_check_wp72.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_check_wp72.py#L15-L15), [`scripts/_mark_wp72_done.py:144`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp72_done.py#L144-L144)
- tests: `tests/unit/test_graph_evolution.py:91`, `tests/unit/test_graph_evolution.py::test_restored_legacy_relationship_expires_without_creating_duplicate_history[False-delete]`, `tests/unit/test_graph_evolution.py::test_restored_legacy_relationship_expires_without_creating_duplicate_history[False-replace]`, `tests/unit/test_graph_evolution.py::test_restored_legacy_relationship_expires_without_creating_duplicate_history[False-revert]`, `tests/unit/test_graph_evolution.py::test_restored_legacy_relationship_expires_without_creating_duplicate_history[True-delete]`, `tests/unit/test_graph_evolution.py::test_restored_legacy_relationship_expires_without_creating_duplicate_history[True-replace]`, `tests/unit/test_graph_evolution.py::test_restored_legacy_relationship_expires_without_creating_duplicate_history[True-revert]`, `tests/unit/test_operational_recovery.py:36`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-NFR-SEC-003 [P1] NFR-SEC-003: Input/file safety

- **Source:** `EOIP-engg-doc-pkg/04-non-functional-requirements.md:31-40` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-SEC-003 — Input/file safety
**WHAT:** Validate paths, sizes, MIME/extension expectations, archive behavior and URL endpoints.  
**WHY:** Ingestion handles untrusted enterprise artifacts.  
**HOW:** Restrict to configured roots; reject traversal/symlink escape; bound files and parsers.  
**DATA / INTERFACES:** Upload/connector config  
**FAILURE:** Unsafe input quarantined.  
**TEST:** Traversal/zip-bomb/oversize tests.  
**COMPLETE WHEN:** Security suite rejects malicious fixtures.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Validate paths, sizes, MIME/extension expectations, archive behavior and URL endpoints.
- [ ] Interfaces: Upload/connector config
- [ ] Failure behaviour: Unsafe input quarantined.
- [ ] Verified by: Traversal/zip-bomb/oversize tests.
- [ ] Complete when: Security suite rejects malicious fixtures.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L24-L24)
- tests: `tests/security/test_verification_suite.py:136`, `tests/security/test_verification_suite.py::test_over_depth_request_is_rejected_with_422`, `tests/security/test_verification_suite.py::test_oversized_body_is_rejected_with_413`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-NFR-SEC-006 [P1] NFR-SEC-006: Container hardening

- **Source:** `EOIP-engg-doc-pkg/04-non-functional-requirements.md:61-70` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-NFR-SEC-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-SEC-006 — Container hardening
**WHAT:** Use non-root where practical, read-only FS where practical, dropped capabilities, healthchecks and private networks.  
**WHY:** Reduces local attack surface.  
**HOW:** Compose separates public app edge from internal graph/model networks.  
**DATA / INTERFACES:** Compose/security profile  
**FAILURE:** Hardening exception documented.  
**TEST:** Container inspection tests.  
**COMPLETE WHEN:** HugeGraph/model not exposed externally by default.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-NFR-SEC-006

**Acceptance criteria**
- [ ] Delivers: Use non-root where practical, read-only FS where practical, dropped capabilities, healthchecks and private networks.
- [ ] Interfaces: Compose/security profile
- [ ] Failure behaviour: Hardening exception documented.
- [ ] Verified by: Container inspection tests.
- [ ] Complete when: HugeGraph/model not exposed externally by default.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L24-L24)
- tests: `tests/security/test_container_hardening.py:1`, `tests/security/test_container_hardening.py::test_application_anchor_drops_all_capabilities`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

