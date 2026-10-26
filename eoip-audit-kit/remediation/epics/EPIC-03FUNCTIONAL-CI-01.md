# EPIC-03FUNCTIONAL-CI-01: EOIP-engg-doc-pkg/03-functional-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 60 tasks, ~36.5 h, priorities {'P0': 3, 'P1': 57}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-FR-ADMIN-001 [P0] FR-ADMIN-001: Admin ingestion UI

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:645-654` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-ADMIN-001 — Admin ingestion UI
**WHAT:** Show connectors, runs, status, counts, errors, replay/dry-run controls.  
**WHY:** Operations must reflect real system state.  
**HOW:** Admin routes call ingestion APIs; URL separation is not authorization.  
**DATA / INTERFACES:** IngestionRun  
**FAILURE:** Actions validate local auth/confirmation.  
**TEST:** Admin E2E.  
**COMPLETE WHEN:** Run state reconciles with backend/meta graph.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Show connectors, runs, status, counts, errors, replay/dry-run controls.
- [ ] Failure behaviour: Actions validate local auth/confirmation.
- [ ] Verified by: Admin E2E.
- [ ] Complete when: Run state reconciles with backend/meta graph.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/admin/ConnectorSetupWizard.jsx:60`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/ConnectorSetupWizard.jsx#L60-L60), [`apps/web/src/admin/IngestionReconciliationPanel.jsx:51`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/IngestionReconciliationPanel.jsx#L51-L51), [`apps/web/src/admin/index.jsx:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/index.jsx#L17-L17), [`scripts/_mark_wp53_done.py:40`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L40-L40), [`scripts/check_wp53_registry.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/check_wp53_registry.py#L8-L8)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:5`, `tests/unit/test_web_ux_and_admin_wp53.py::test_fr_admin_001_ingestion_ui`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-GRAPH-010 [P0] FR-GRAPH-010: RDF/OWL interoperability

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:241-254` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-GRAPH-010 — RDF/OWL interoperability
**WHAT:** Export platform ontology/data through explicit adapters rather than claiming native RDF/SPARQL.  
**WHY:** Interoperability is useful but HugeGraph is a property graph.  
**HOW:** The authenticated `GET /api/v1/ontology/export` adapter emits JSON-LD 1.1. Graph labels map to OWL classes, edge labels to OWL object properties, scalar properties to datatype properties, and relationship instances to direct triples plus reified assertions so edge attributes remain available. The export includes ontology version/domain/required-property metadata, is bounded by a caller-selected limit, and reports truncation and mapping losses. HugeGraph remains a property graph; SPARQL, if added, targets an adapter, not raw HugeGraph.

**DATA / INTERFACES:** JSON-LD 1.1 mapping document and machine-readable export metadata

**FAILURE:** Unsupported labels and edges without included endpoints are retained where possible and reported in `export.mapping_losses`; over-limit results set `export.partial` and identify which record kinds were truncated.

**TEST:** Fixtures verify vocabulary, entity and relationship mapping, preservation of relationship attributes, nested JSON properties, authentication, and bounded/truncated output.

**COMPLETE WHEN:** No documentation claims native SPARQL support.
**TARGET PHASE:** P2
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Export platform ontology/data through explicit adapters rather than claiming native RDF/SPARQL.
- [ ] Interfaces: JSON-LD 1.1 mapping document and machine-readable export metadata
- [ ] Failure behaviour: Unsupported labels and edges without included endpoints are retained where possible and reported in export.mapping_losses; over-limit results set export.partial and identify which record kinds were truncated.
- [ ] Verified by: Fixtures verify vocabulary, entity and relationship mapping, preservation of relationship attributes, nested JSON properties, authentication, and bounded/truncated output.
- [ ] Complete when: No documentation claims native SPARQL support.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L16-L16)
- tests: `tests/unit/test_dual_semantic_model.py:44`, `tests/unit/test_dual_semantic_model.py::test_jsonld_import_reconstructs_supported_property_graph_records`, `tests/unit/test_phase2_rdf_export.py:28`, `tests/unit/test_phase2_rdf_export.py::test_jsonld_export_maps_ontology_vertices_and_reified_relationships`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-INGEST-005 [P0] FR-INGEST-005: Dead-letter processing

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:141-150` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-INGEST-005 — Dead-letter processing
**WHAT:** Store rejected events locally with reason/evidence and replay controls.  
**WHY:** Bad records must not block whole imports.  
**HOW:** DLQ files contain event hash, stage, error code, safe message, run ID.  
**DATA / INTERFACES:** DLQ envelope  
**FAILURE:** Secrets/PII are not duplicated beyond allowed capture.  
**TEST:** Malformed fixtures.  
**COMPLETE WHEN:** Rejected records are inspectable and replayable.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Store rejected events locally with reason/evidence and replay controls.
- [ ] Interfaces: DLQ envelope
- [ ] Failure behaviour: Secrets/PII are not duplicated beyond allowed capture.
- [ ] Verified by: Malformed fixtures.
- [ ] Complete when: Rejected records are inspectable and replayable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ingestion/dlq.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ingestion/dlq.py#L1-L1)
- tests: `tests/unit/test_jira_ingestion.py:147`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-ADMIN-002 [P1] FR-ADMIN-002: Admin graph quality UI

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:655-664` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-ADMIN-002 — Admin graph quality UI
**WHAT:** Show graph stats, validation findings, quality metrics, schema/ontology versions and backup state.  
**WHY:** Demonstrates maintainability and trust.  
**HOW:** All values queried from APIs/meta graph.  
**DATA / INTERFACES:** QualitySnapshot  
**FAILURE:** Missing metric displayed as unavailable.  
**TEST:** Fixture reconciliation tests.  
**COMPLETE WHEN:** No dashboard KPI is hardcoded.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Show graph stats, validation findings, quality metrics, schema/ontology versions and backup state.
- [ ] Failure behaviour: Missing metric displayed as unavailable.
- [ ] Verified by: Fixture reconciliation tests.
- [ ] Complete when: No dashboard KPI is hardcoded.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/admin/KnowledgeGovernanceAndSLOPanel.jsx:39`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/KnowledgeGovernanceAndSLOPanel.jsx#L39-L39), [`apps/web/src/admin/index.jsx:23`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/admin/index.jsx#L23-L23), [`scripts/_mark_wp53_done.py:47`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L47-L47), [`scripts/check_wp53_registry.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/check_wp53_registry.py#L8-L8)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:124`, `tests/unit/test_web_ux_and_admin_wp53.py::test_fr_admin_002_graph_quality_ui`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-AGENT-001 [P1] FR-AGENT-001: Agent contract

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:545-554` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-AGENT-001 — Agent contract
**WHAT:** Define ID/type/purpose/input/output/capabilities/tools/model/memory/policies/time/budget/retry/failure/evidence/audit fields.  
**WHY:** Agents require enforceable runtime contracts.  
**HOW:** Registry loads versioned YAML/JSON definitions and validates before execution.  
**DATA / INTERFACES:** AgentContract  
**FAILURE:** Invalid contract cannot register.  
**TEST:** Schema tests.  
**COMPLETE WHEN:** Every enabled agent has a validated contract.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Define ID/type/purpose/input/output/capabilities/tools/model/memory/policies/time/budget/retry/failure/evidence/audit fields.
- [ ] Failure behaviour: Invalid contract cannot register.
- [ ] Verified by: Schema tests.
- [ ] Complete when: Every enabled agent has a validated contract.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:232`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L232-L232)
- tests: `tests/unit/test_governed_agents.py:32`, `tests/unit/test_governed_agents.py::test_agent_contract_validation`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-AGENT-002 [P1] FR-AGENT-002: Bounded agent runtime

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:555-564` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-AGENT-002 — Bounded agent runtime
**WHAT:** Enforce maximum steps/retries/recursion/time/model/tool budgets and circuit breaker.  
**WHY:** Prevents unbounded loops and resource use.  
**HOW:** Runtime state machine records route/context/plan/tool/observation/evaluation/result/audit.  
**DATA / INTERFACES:** AgentRun  
**FAILURE:** Budget exhaustion terminates with partial evidence.  
**TEST:** Loop/budget tests.  
**COMPLETE WHEN:** Agent cannot exceed configured execution envelope.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Enforce maximum steps/retries/recursion/time/model/tool budgets and circuit breaker.
- [ ] Failure behaviour: Budget exhaustion terminates with partial evidence.
- [ ] Verified by: Loop/budget tests.
- [ ] Complete when: Agent cannot exceed configured execution envelope.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/loops/core.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/loops/core.py#L1-L1), [`scripts/update_phase3_wp32_wp33.py:238`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L238-L238)
- tests: `tests/unit/test_governed_agents.py:66`, `tests/unit/test_governed_agents.py::test_bounded_agent_runtime`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-AGENT-003 [P1] FR-AGENT-003: TraceImpact agent

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:565-574` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-AGENT-003 — TraceImpact agent
**WHAT:** Provide one useful read-only MVP workflow that answers requirement/code trace and impact questions.  
**WHY:** MVP requires a real agent without unsafe write autonomy.  
**HOW:** Agent composes search/path/impact/retrieval tools and returns evidence summary.  
**DATA / INTERFACES:** AgentRequest/AgentResult  
**FAILURE:** Tool/model failures are surfaced with partial structured result.  
**TEST:** Golden E2E agent tests.  
**COMPLETE WHEN:** Same demo question works via UI/API/MCP context.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Provide one useful read-only MVP workflow that answers requirement/code trace and impact questions.
- [ ] Failure behaviour: Tool/model failures are surfaced with partial structured result.
- [ ] Verified by: Golden E2E agent tests.
- [ ] Complete when: Same demo question works via UI/API/MCP context.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/agents/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/agents/__init__.py#L1-L1), [`packages/eoip/agents/anomaly.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/agents/anomaly.py#L1-L1), [`packages/eoip/agents/blast_radius.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/agents/blast_radius.py#L1-L1), [`packages/eoip/agents/community.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/agents/community.py#L1-L1), [`packages/eoip/agents/incident_correlation.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/agents/incident_correlation.py#L1-L1), [`packages/eoip/agents/similarity.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/agents/similarity.py#L1-L1), [`packages/eoip/agents/trace_impact.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/agents/trace_impact.py#L1-L1), [`scripts/update_phase3_wp32_wp33.py:244`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L244-L244)
- tests: `packages/eoip/agents/test_coverage.py:1`, `tests/unit/test_governed_agents.py:85`, `tests/unit/test_governed_agents.py::test_trace_impact_agent`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-AGENT-004 [P1] FR-AGENT-004: Write/action approval boundary

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:575-584` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-AGENT-004 — Write/action approval boundary
**WHAT:** Separate read tools from write/destructive tools and require explicit confirmation for future write actions.  
**WHY:** Agent autonomy must not bypass human control.  
**HOW:** MVP registers read tools only; future action registry includes risk/reversibility/approval policy.  
**DATA / INTERFACES:** ToolContract  
**FAILURE:** Unapproved write invocation denied/audited.  
**TEST:** Negative policy tests.  
**COMPLETE WHEN:** No MVP agent can mutate source systems or code.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Separate read tools from write/destructive tools and require explicit confirmation for future write actions.
- [ ] Failure behaviour: Unapproved write invocation denied/audited.
- [ ] Verified by: Negative policy tests.
- [ ] Complete when: No MVP agent can mutate source systems or code.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:250`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L250-L250)
- tests: `tests/unit/test_governed_agents.py:100`, `tests/unit/test_governed_agents.py::test_write_action_approval_boundary`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-AGENT-005 [P1] FR-AGENT-005: Controlled self-modification

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:585-594` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-AGENT-005 — Controlled self-modification
**WHAT:** Self-learning/evolving/writing capabilities remain disabled until governance, sandboxing, tests and approval exist.  
**WHY:** Autonomous self-change is high risk.  
**HOW:** Architecture reserves versioned proposal/sandbox interfaces only; implementation is P8+.  
**DATA / INTERFACES:** ChangeProposal  
**FAILURE:** Any runtime self-edit request denied in earlier phases.  
**TEST:** Policy tests.  
**COMPLETE WHEN:** No production self-modification path exists before P8+.  
**TARGET PHASE:** P8+
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Self-learning/evolving/writing capabilities remain disabled until governance, sandboxing, tests and approval exist.
- [ ] Failure behaviour: Any runtime self-edit request denied in earlier phases.
- [ ] Verified by: Policy tests.
- [ ] Complete when: No production self-modification path exists before P8+.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/update_phase3_wp32_wp33.py:256`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp32_wp33.py#L256-L256)
- tests: `tests/unit/test_governed_agents.py:110`, `tests/unit/test_governed_agents.py::test_controlled_self_modification`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-CODE-001 [P1] FR-CODE-001: Deterministic code parser

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:325-334` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 19, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-CODE-001 — Deterministic code parser
**WHAT:** Parse source using Tree-sitter/language-specific AST tooling, never LLM as primary parser.  
**WHY:** Code relationships must be reproducible.  
**HOW:** Parser plugins emit File and CodeSymbol records with ranges, qualified names and structural relationships.  
**DATA / INTERFACES:** Repository checkout, parser contracts  
**FAILURE:** Parse errors become file-level findings and do not abort repository.  
**TEST:** Golden parser fixtures.  
**COMPLETE WHEN:** Supported files yield stable symbol graph and exact source ranges.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Parse source using Tree-sitter/language-specific AST tooling, never LLM as primary parser.
- [ ] Interfaces: Repository checkout, parser contracts
- [ ] Failure behaviour: Parse errors become file-level findings and do not abort repository.
- [ ] Verified by: Golden parser fixtures.
- [ ] Complete when: Supported files yield stable symbol graph and exact source ranges.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:20`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L20-L20)
- tests: `tests/unit/test_code_parser.py:6`, `tests/unit/test_code_parser.py::test_python_parser_returns_stable_symbols_ranges_imports_and_static_calls`, `tests/unit/test_requirement_evidence.py:60`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-CODE-002 [P1] FR-CODE-002: Python and TypeScript MVP parsing

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:335-344` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-CODE-002 — Python and TypeScript MVP parsing
**WHAT:** Support Python and TypeScript/JavaScript in Phase 1.  
**WHY:** Two common languages prove parser extensibility without over-scoping.  
**HOW:** Tree-sitter grammars/plugins extract modules/classes/functions/methods/imports/calls where statically resolvable.  
**DATA / INTERFACES:** Source files  
**FAILURE:** Unsupported syntax is partial with confidence/status.  
**TEST:** Language-specific fixtures.  
**COMPLETE WHEN:** Demo repo symbols and imports/calls are queryable.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Support Python and TypeScript/JavaScript in Phase 1.
- [ ] Interfaces: Source files
- [ ] Failure behaviour: Unsupported syntax is partial with confidence/status.
- [ ] Verified by: Language-specific fixtures.
- [ ] Complete when: Demo repo symbols and imports/calls are queryable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:20`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L20-L20)
- tests: `tests/unit/test_code_parser.py:7`, `tests/unit/test_code_parser.py::test_python_parser_returns_stable_symbols_ranges_imports_and_static_calls`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-CODE-003 [P1] FR-CODE-003: Commit-to-symbol linking

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:345-354` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-FR-CODE-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-CODE-003 — Commit-to-symbol linking
**WHAT:** Relate commits to files and affected symbols using changed ranges/versions where available.  
**WHY:** Requirements must trace below file level.  
**HOW:** MVP maps changed files deterministically and intersects diff hunks with symbol ranges when possible.  
**DATA / INTERFACES:** Git diff metadata, symbols  
**FAILURE:** Ambiguous deleted/renamed symbols produce evidence-backed partial link.  
**TEST:** Rename/diff tests.  
**COMPLETE WHEN:** Demo commit connects to relevant function(s).  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-FR-CODE-003

**Acceptance criteria**
- [ ] Delivers: Relate commits to files and affected symbols using changed ranges/versions where available.
- [ ] Interfaces: Git diff metadata, symbols
- [ ] Failure behaviour: Ambiguous deleted/renamed symbols produce evidence-backed partial link.
- [ ] Verified by: Rename/diff tests.
- [ ] Complete when: Demo commit connects to relevant function(s).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/codegraph/diff_hunk.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/codegraph/diff_hunk.py#L1-L1)
- tests: `tests/unit/test_diff_hunk.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-CODE-004 [P1] FR-CODE-004: Call/import/dependency edges

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:355-364` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-CODE-004 — Call/import/dependency edges
**WHAT:** Represent calls, imports and package/module dependencies with provenance.  
**WHY:** Impact analysis needs dependency structure.  
**HOW:** Static extractor emits typed edges and marks unresolved/external targets explicitly.  
**DATA / INTERFACES:** AST, manifests  
**FAILURE:** Dynamic calls are not fabricated.  
**TEST:** Static-call fixtures.  
**COMPLETE WHEN:** Blast radius traverses only validated edge classes.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Represent calls, imports and package/module dependencies with provenance.
- [ ] Interfaces: AST, manifests
- [ ] Failure behaviour: Dynamic calls are not fabricated.
- [ ] Verified by: Static-call fixtures.
- [ ] Complete when: Blast radius traverses only validated edge classes.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:20`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L20-L20)
- tests: `tests/unit/test_code_parser.py:8`, `tests/unit/test_code_parser.py::test_python_parser_returns_stable_symbols_ranges_imports_and_static_calls`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-CODE-005 [P1] FR-CODE-005: Source navigation

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:365-374` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-CODE-005 — Source navigation
**WHAT:** Preserve repo, revision, path and line/column ranges.  
**WHY:** VS Code must open exact context.  
**HOW:** API returns workspace-relative path plus range and commit/revision evidence.  
**DATA / INTERFACES:** CodeSymbol  
**FAILURE:** Missing local checkout returns context without unsafe file access.  
**TEST:** Navigation contract tests.  
**COMPLETE WHEN:** Extension opens demo symbol at correct range.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Preserve repo, revision, path and line/column ranges.
- [ ] Failure behaviour: Missing local checkout returns context without unsafe file access.
- [ ] Verified by: Navigation contract tests.
- [ ] Complete when: Extension opens demo symbol at correct range.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:20`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L20-L20)
- tests: `tests/unit/test_code_parser.py:9`, `tests/unit/test_code_parser.py::test_python_parser_returns_stable_symbols_ranges_imports_and_static_calls`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-CONN-001 [P1] FR-CONN-001: Connector SDK

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:11-20` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-CONN-001 — Connector SDK
**WHAT:** Provide a versioned connector interface for discover, extract, checkpoint, health and replay.  
**WHY:** New sources must not change graph-core logic.  
**HOW:** Each connector emits SourceEvent records and owns source-specific auth/pagination only.  
**DATA / INTERFACES:** ConnectorConfig, SourceEvent, Checkpoint  
**FAILURE:** Connector isolation; retryable failures checkpoint; poison records to DLQ.  
**TEST:** Contract tests against a fake source.  
**COMPLETE WHEN:** A new connector can be added without editing ingestion core.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Provide a versioned connector interface for discover, extract, checkpoint, health and replay.
- [ ] Interfaces: ConnectorConfig, SourceEvent, Checkpoint
- [ ] Failure behaviour: Connector isolation; retryable failures checkpoint; poison records to DLQ.
- [ ] Verified by: Contract tests against a fake source.
- [ ] Complete when: A new connector can be added without editing ingestion core.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/connectors/base.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/base.py#L1-L1), [`scripts/patch_contracts_tags.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_contracts_tags.py#L7-L7), [`scripts/tick_phase2_batch1.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L7-L7)
- tests: `tests/contract/test_g2_contracts.py:144`, `tests/contract/test_g2_contracts.py::test_fake_connector_satisfies_runtime_connector_protocol`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-CONN-002 [P1] FR-CONN-002: Jira JSON connector

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:21-30` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-FR-CONN-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-CONN-002 — Jira JSON connector
**WHAT:** Import configurable Jira JSON plus the synthetic MVP fixture.  
**WHY:** Jira is the primary work-management seed for traceability.  
**HOW:** Map source fields through configuration into canonical WorkItem/Project/Person entities.  
**DATA / INTERFACES:** JSON file, mapping YAML, SourceEvent  
**FAILURE:** Malformed records rejected individually with evidence; run continues.  
**TEST:** Fixture, malformed, duplicate, resume tests.  
**COMPLETE WHEN:** Repeat import is idempotent and creates expected graph.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-FR-CONN-002

**Acceptance criteria**
- [ ] Delivers: Import configurable Jira JSON plus the synthetic MVP fixture.
- [ ] Interfaces: JSON file, mapping YAML, SourceEvent
- [ ] Failure behaviour: Malformed records rejected individually with evidence; run continues.
- [ ] Verified by: Fixture, malformed, duplicate, resume tests.
- [ ] Complete when: Repeat import is idempotent and creates expected graph.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_jira_ingestion.py:11`, `tests/unit/test_jira_ingestion.py::test_dlq_record_uses_the_unified_envelope`, `tests/unit/test_jira_ingestion.py::test_dry_run_validates_without_capture_or_graph_writes`, `tests/unit/test_jira_ingestion.py::test_jira_import_accepts_configured_mapping_and_local_fixture`, `tests/unit/test_jira_ingestion.py::test_jira_import_captures_evidence_and_is_idempotent`, `tests/unit/test_jira_ingestion.py::test_jira_ingestion_creates_belongs_to_domain_edges`, `tests/unit/test_jira_ingestion.py::test_jira_parent_relationship_is_created_even_when_parent_record_follows_child`, `tests/unit/test_jira_ingestion.py::test_jira_resume_replays_captured_events_without_regenerating_identity`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-CONN-004 [P1] FR-CONN-004: GitLab metadata adapter

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:41-50` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-FR-CONN-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-CONN-004 — GitLab metadata adapter
**WHAT:** Support GitLab-style MR/pipeline metadata from configurable API or local JSON fixture.  
**WHY:** The E2E story includes merge requests and pipelines.  
**HOW:** MVP supports fixture/offline mode; live on-prem GitLab adapter uses endpoint/token abstraction.  
**DATA / INTERFACES:** MR/pipeline JSON, endpoint config  
**FAILURE:** Rate limits/retries/checkpoints; no hard-coded credential.  
**TEST:** Mock API and fixture contract tests.  
**COMPLETE WHEN:** MR and pipeline records link to commits and work items.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-FR-CONN-004

**Acceptance criteria**
- [ ] Delivers: Support GitLab-style MR/pipeline metadata from configurable API or local JSON fixture.
- [ ] Interfaces: MR/pipeline JSON, endpoint config
- [ ] Failure behaviour: Rate limits/retries/checkpoints; no hard-coded credential.
- [ ] Verified by: Mock API and fixture contract tests.
- [ ] Complete when: MR and pipeline records link to commits and work items.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L7-L7)
- tests: `tests/unit/test_gitlab_connector.py:25`, `tests/unit/test_gitlab_connector.py::test_gitlab_baseline_emits_repository_delivery_and_knowledge_events`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-CONN-006 [P1] FR-CONN-006: Dry run and replay

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:61-70` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 54, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-CONN-006 — Dry run and replay
**WHAT:** Allow validation-only dry run and deterministic replay of captured source events.  
**WHY:** Safe mapping evolution and debugging need reproducibility.  
**HOW:** Dry run performs parse/map/validation without graph mutation; replay reads raw-capture events.  
**DATA / INTERFACES:** SourceEvent archive  
**FAILURE:** Invalid replay schema/version is quarantined.  
**TEST:** Golden-event replay tests.  
**COMPLETE WHEN:** Same input/version produces same canonical mutations.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Allow validation-only dry run and deterministic replay of captured source events.
- [ ] Interfaces: SourceEvent archive
- [ ] Failure behaviour: Invalid replay schema/version is quarantined.
- [ ] Verified by: Golden-event replay tests.
- [ ] Complete when: Same input/version produces same canonical mutations.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ingestion/replay.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ingestion/replay.py#L1-L1), [`scripts/replay.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/replay.py#L1-L1)
- tests: `tests/unit/test_confluence_history.py:140`, `tests/unit/test_confluence_history.py::test_old_captures_report_partial_history_and_invalid_complete_history_enters_dlq`, `tests/unit/test_confluence_metadata.py:92`, `tests/unit/test_confluence_metadata.py::test_metadata_persists_in_revisions_clears_on_update_and_is_replay_stable`, `tests/unit/test_document_references.py:101`, `tests/unit/test_document_references.py::test_fact_changes_not_observations_trigger_staleness_and_replay_cannot_rebase`, `tests/unit/test_phase2_ingestion.py:13`, `tests/unit/test_phase2_ingestion.py::test_rest_refetch_preserves_capture_provenance_and_replay_freshness[confluence]`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-CONN-007 [P1] FR-CONN-007: Source deletion semantics

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:71-80` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-CONN-007 — Source deletion semantics
**WHAT:** Represent source disappearance/deletion without silent hard delete.  
**WHY:** Historical provenance must not be destroyed.  
**HOW:** Mark tombstone/deleted_at; hard delete is separate administrative operation.  
**DATA / INTERFACES:** Source version/tombstone  
**FAILURE:** Conflicting source state becomes validation finding.  
**TEST:** Deletion/reappearance tests.  
**COMPLETE WHEN:** Deleted source is queryable historically and excluded from current views.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Represent source disappearance/deletion without silent hard delete.
- [ ] Interfaces: Source version/tombstone
- [ ] Failure behaviour: Conflicting source state becomes validation finding.
- [ ] Verified by: Deletion/reappearance tests.
- [ ] Complete when: Deleted source is queryable historically and excluded from current views.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_jira_ingestion.py:101`, `tests/unit/test_jira_ingestion.py::test_jira_source_deletion_tombstones_without_hard_delete`, `tests/unit/test_jira_ingestion.py::test_jira_source_reappearance_restores_current_view`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-GRAPH-001 [P1] FR-GRAPH-001: HugeGraph authoritative store

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:151-160` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-FR-GRAPH-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-GRAPH-001 — HugeGraph authoritative store
**WHAT:** Use Apache HugeGraph as the authoritative property graph and ontology operational store.  
**WHY:** This is a non-negotiable platform constraint.  
**HOW:** All user-visible entity/relationship truth is resolved from HugeGraph; raw files are evidence, not alternative truth DB.  
**DATA / INTERFACES:** HugeGraph schema/Gremlin  
**FAILURE:** Graph unavailable returns degraded/readiness failure; no shadow DB fallback.  
**TEST:** Startup and persistence tests.  
**COMPLETE WHEN:** All demo graph paths survive service restart.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-FR-GRAPH-001

**Acceptance criteria**
- [ ] Delivers: Use Apache HugeGraph as the authoritative property graph and ontology operational store.
- [ ] Interfaces: HugeGraph schema/Gremlin
- [ ] Failure behaviour: Graph unavailable returns degraded/readiness failure; no shadow DB fallback.
- [ ] Verified by: Startup and persistence tests.
- [ ] Complete when: All demo graph paths survive service restart.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/catalog/products.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/catalog/products.py#L6-L6), [`packages/eoip/graph/memory.py:5`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/memory.py#L5-L5)
- tests: `tests/unit/test_requirement_evidence.py:10`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-GRAPH-002 [P1] FR-GRAPH-002: Logical graph domains

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:161-170` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-GRAPH-002 — Logical graph domains
**WHAT:** Represent Jira, Code, Docs, CI, Provenance, Meta and other domains explicitly within the graph.  
**WHY:** Avoid one undifferentiated graph while preserving native cross-domain traversal.  
**HOW:** MVP uses one physical graph with graph_domain property and domain meta nodes; later physical isolation only by measured need.  
**DATA / INTERFACES:** graph_domain, GraphDomain node  
**FAILURE:** Unknown domain is rejected by schema policy.  
**TEST:** Domain integrity tests.  
**COMPLETE WHEN:** Every business vertex/edge belongs to a valid domain.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Represent Jira, Code, Docs, CI, Provenance, Meta and other domains explicitly within the graph.
- [ ] Interfaces: graph_domain, GraphDomain node
- [ ] Failure behaviour: Unknown domain is rejected by schema policy.
- [ ] Verified by: Domain integrity tests.
- [ ] Complete when: Every business vertex/edge belongs to a valid domain.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/meta.py:33`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/meta.py#L33-L33), [`scripts/tick_phase0_phase1.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L15-L15)
- tests: `tests/unit/test_meta_graph.py:9`, `tests/unit/test_meta_graph.py::test_bootstrap_creates_domain_vertices`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-GRAPH-003 [P1] FR-GRAPH-003: Schema bootstrap

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:171-180` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 29, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-GRAPH-003 — Schema bootstrap
**WHAT:** Initialize property keys, vertex labels, edge labels and indexes idempotently.  
**WHY:** `docker compose up` must create a usable environment.  
**HOW:** Schema bootstrap compares expected schema version before applying additive changes.  
**DATA / INTERFACES:** Schema manifest  
**FAILURE:** Incompatible migration fails startup of app mutation path but preserves DB.  
**TEST:** Fresh/repeat/incompatible schema tests.  
**COMPLETE WHEN:** Fresh stack auto-initializes and second run is no-op.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Initialize property keys, vertex labels, edge labels and indexes idempotently.
- [ ] Interfaces: Schema manifest
- [ ] Failure behaviour: Incompatible migration fails startup of app mutation path but preserves DB.
- [ ] Verified by: Fresh/repeat/incompatible schema tests.
- [ ] Complete when: Fresh stack auto-initializes and second run is no-op.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L15-L15)
- tests: `tests/unit/test_phase2_hugegraph_schema.py:26`, `tests/unit/test_phase2_hugegraph_schema.py::test_schema_bootstrap_appends_new_properties_to_existing_labels`, `tests/unit/test_phase2_hugegraph_schema.py::test_schema_bootstrap_is_read_only_when_compatible`, `tests/unit/test_phase2_hugegraph_schema.py::test_schema_bootstrap_refuses_missing_compatibility_metadata[edgelabels-nullable_keys]`, `tests/unit/test_phase2_hugegraph_schema.py::test_schema_bootstrap_refuses_missing_compatibility_metadata[propertykeys-data_type]`, `tests/unit/test_phase2_hugegraph_schema.py::test_schema_bootstrap_refuses_missing_compatibility_metadata[vertexlabels-properties]`, `tests/unit/test_phase2_hugegraph_schema.py::test_schema_bootstrap_rejects_new_required_property_on_existing_label`, `tests/unit/test_phase2_hugegraph_schema.py::test_schema_incompatibility_blocks_all_mutations[edgelabels-enable_label_index-False]`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-GRAPH-005 [P1] FR-GRAPH-005: Meta graph

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:191-200` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-GRAPH-005 — Meta graph
**WHAT:** Model datasets, sources, graph domains, schema/ontology versions, ingestion runs, quality and lineage metadata.  
**WHY:** The query router and admin UI need graph self-description.  
**HOW:** Meta nodes are queryable and link to domain data via INGESTED_IN/BELONGS_TO_DOMAIN/EVIDENCED_BY.  
**DATA / INTERFACES:** Meta entities/edges  
**FAILURE:** Stale meta state is validation finding.  
**TEST:** Meta traversal tests.  
**COMPLETE WHEN:** Admin statistics are derived from graph/meta records.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Model datasets, sources, graph domains, schema/ontology versions, ingestion runs, quality and lineage metadata.
- [ ] Interfaces: Meta entities/edges
- [ ] Failure behaviour: Stale meta state is validation finding.
- [ ] Verified by: Meta traversal tests.
- [ ] Complete when: Admin statistics are derived from graph/meta records.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/meta.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/meta.py#L1-L1), [`scripts/tick_phase0_phase1.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L15-L15)
- tests: `tests/unit/test_meta_graph.py:9`, `tests/unit/test_meta_graph.py::test_bootstrap_creates_domain_vertices`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-GRAPH-006 [P1] FR-GRAPH-006: Cross-domain bridge edges

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:201-210` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-GRAPH-006 — Cross-domain bridge edges
**WHAT:** Create explicit, evidence-backed edges between work, code, CI and documents.  
**WHY:** The value proposition is end-to-end enterprise traceability.  
**HOW:** Link deterministic identifiers first (issue keys, commit SHA, paths); inferred links are labeled and scored.  
**DATA / INTERFACES:** IMPLEMENTS, MODIFIES, REFERENCES, DOCUMENTS, PRODUCED_BY  
**FAILURE:** Low-confidence inference never becomes deterministic truth.  
**TEST:** Synthetic E2E path assertions.  
**COMPLETE WHEN:** Jira→MR→Commit→File→Function→Dependency→Pipeline→Doc path is traversable.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Create explicit, evidence-backed edges between work, code, CI and documents.
- [ ] Interfaces: IMPLEMENTS, MODIFIES, REFERENCES, DOCUMENTS, PRODUCED_BY
- [ ] Failure behaviour: Low-confidence inference never becomes deterministic truth.
- [ ] Verified by: Synthetic E2E path assertions.
- [ ] Complete when: Jira→MR→Commit→File→Function→Dependency→Pipeline→Doc path is traversable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L15-L15)
- tests: `tests/unit/test_graph_traversal.py:10`, `tests/unit/test_graph_traversal.py::test_find_path_returns_shortest_ordered_path_in_both_directions`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-GRAPH-007 [P1] FR-GRAPH-007: Gremlin repository

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:211-220` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-GRAPH-007 — Gremlin repository
**WHAT:** Centralize parameterized/bounded Gremlin templates.  
**WHY:** Unrestricted model-generated graph queries are unsafe.  
**HOW:** Only named templates and validated QueryPlans reach the graph client in MVP.  
**DATA / INTERFACES:** QueryPlan v1  
**FAILURE:** Unknown template or over-limit request rejected.  
**TEST:** Policy and traversal-bound tests.  
**COMPLETE WHEN:** No UI/agent endpoint can execute arbitrary mutation Gremlin.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Centralize parameterized/bounded Gremlin templates.
- [ ] Interfaces: QueryPlan v1
- [ ] Failure behaviour: Unknown template or over-limit request rejected.
- [ ] Verified by: Policy and traversal-bound tests.
- [ ] Complete when: No UI/agent endpoint can execute arbitrary mutation Gremlin.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L15-L15)
- tests: `tests/unit/test_query_intelligence.py:161`, `tests/unit/test_query_intelligence.py::test_template_binding_builds_plan`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-GRAPH-008 [P1] FR-GRAPH-008: Index strategy

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:221-230` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 29, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-GRAPH-008 — Index strategy
**WHAT:** Create indexes only for measured access patterns.  
**WHY:** Over-indexing increases write/storage cost.  
**HOW:** MVP indexes canonical/source IDs, issue keys, commit SHA, qualified symbol name, path/domain/type and selected timestamps.  
**DATA / INTERFACES:** HugeGraph IndexLabels  
**FAILURE:** Index bootstrap mismatch blocks incompatible mutation.  
**TEST:** Query-plan benchmark tests.  
**COMPLETE WHEN:** Benchmark-critical lookup paths use planned indexes.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Create indexes only for measured access patterns.
- [ ] Interfaces: HugeGraph IndexLabels
- [ ] Failure behaviour: Index bootstrap mismatch blocks incompatible mutation.
- [ ] Verified by: Query-plan benchmark tests.
- [ ] Complete when: Benchmark-critical lookup paths use planned indexes.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ontology/manifest.py:458`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/manifest.py#L458-L458), [`scripts/tick_phase0_phase1.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L15-L15)
- tests: `tests/unit/test_phase2_hugegraph_schema.py:12`, `tests/unit/test_phase2_hugegraph_schema.py::test_document_reference_lookups_have_single_property_secondary_indexes`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-GRAPH-009 [P1] FR-GRAPH-009: Graph version journal

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:231-240` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 13, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-GRAPH-009 — Graph version journal
**WHAT:** Record mutation run, schema/ontology version, first/last seen and validity metadata.  
**WHY:** Reproducibility needs temporal/version context.  
**HOW:** MVP stores revisions/change journal metadata; full snapshots/diffs are P5.  
**DATA / INTERFACES:** revision fields, IngestionRun  
**FAILURE:** Missing version metadata is validation error.  
**TEST:** Replay/version tests.  
**COMPLETE WHEN:** Each changed fact can be attributed to a run/version.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Record mutation run, schema/ontology version, first/last seen and validity metadata.
- [ ] Interfaces: revision fields, IngestionRun
- [ ] Failure behaviour: Missing version metadata is validation error.
- [ ] Verified by: Replay/version tests.
- [ ] Complete when: Each changed fact can be attributed to a run/version.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L16-L16)
- tests: `tests/unit/test_graph_evolution.py:30`, `tests/unit/test_graph_evolution.py::test_entity_evolution_is_idempotent_temporal_and_late_event_safe`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-ID-001 [P1] FR-ID-001: Deterministic identity resolution

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:295-304` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 2, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-ID-001 — Deterministic identity resolution
**WHAT:** Resolve exact emails, canonical source IDs and configured aliases before fuzzy methods.  
**WHY:** Avoid accidental person/service merging.  
**HOW:** Generate candidate set and auto-merge only deterministic rules.  
**DATA / INTERFACES:** IdentityCandidate  
**FAILURE:** Conflict preserved as separate nodes.  
**TEST:** Alias/conflict tests.  
**COMPLETE WHEN:** Exact aliases merge predictably and retain source aliases.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Resolve exact emails, canonical source IDs and configured aliases before fuzzy methods.
- [ ] Failure behaviour: Conflict preserved as separate nodes.
- [ ] Verified by: Alias/conflict tests.
- [ ] Complete when: Exact aliases merge predictably and retain source aliases.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/identity/resolver.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/identity/resolver.py#L15-L15)
- tests: `tests/unit/test_identity_ingestion.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-ID-002 [P1] FR-ID-002: Ambiguous identity candidates

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:305-314` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-ID-002 — Ambiguous identity candidates
**WHAT:** Never silently merge low-confidence fuzzy matches.  
**WHY:** False identity merges contaminate the enterprise graph.  
**HOW:** Store candidate relationship/confidence for review; human-confirmed merge is future UI.  
**DATA / INTERFACES:** IdentityCandidate  
**FAILURE:** Ambiguous candidates remain separate.  
**TEST:** Fuzzy boundary tests.  
**COMPLETE WHEN:** No fuzzy-only match produces same canonical_id automatically.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Never silently merge low-confidence fuzzy matches.
- [ ] Failure behaviour: Ambiguous candidates remain separate.
- [ ] Verified by: Fuzzy boundary tests.
- [ ] Complete when: No fuzzy-only match produces same canonical_id automatically.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/identity/candidates.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/identity/candidates.py#L1-L1)
- tests: `tests/unit/test_identity_candidates.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-INGEST-001 [P1] FR-INGEST-001: Raw capture

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:101-110` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-INGEST-001 — Raw capture
**WHAT:** Persist immutable local SourceEvent envelopes before normalization.  
**WHY:** Replay, provenance and audit require source fidelity.  
**HOW:** Write newline-delimited JSON by source/run/date with hashes and restrictive permissions.  
**DATA / INTERFACES:** SourceEvent v1  
**FAILURE:** Disk-full fails job before graph mutation of uncaptured record.  
**TEST:** Hash/replay/restart tests.  
**COMPLETE WHEN:** Every graph mutation references a captured event.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Persist immutable local SourceEvent envelopes before normalization.
- [ ] Interfaces: SourceEvent v1
- [ ] Failure behaviour: Disk-full fails job before graph mutation of uncaptured record.
- [ ] Verified by: Hash/replay/restart tests.
- [ ] Complete when: Every graph mutation references a captured event.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/contracts/graph_mutation.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/contracts/graph_mutation.py#L4-L4), [`packages/eoip/contracts/source_event.py:5`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/contracts/source_event.py#L5-L5)
- tests: `tests/unit/test_jira_ingestion.py:21`, `tests/unit/test_jira_ingestion.py::test_jira_import_captures_evidence_and_is_idempotent`, `tests/unit/test_jira_ingestion.py::test_malformed_record_is_captured_and_quarantined_without_graph_mutation`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-INGEST-002 [P1] FR-INGEST-002: Canonicalization

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:111-120` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-FR-INGEST-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-INGEST-002 — Canonicalization
**WHAT:** Normalize source events into typed canonical entities/relationships.  
**WHY:** Cross-source graph logic requires stable contracts.  
**HOW:** Pure/config-driven mappers emit versioned NormalizedEntity/Relationship records.  
**DATA / INTERFACES:** Canonical JSON contracts  
**FAILURE:** Mapper errors are per-record findings/DLQ.  
**TEST:** Golden mapping tests.  
**COMPLETE WHEN:** Same source record maps deterministically for same mapper version.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-FR-INGEST-002

**Acceptance criteria**
- [ ] Delivers: Normalize source events into typed canonical entities/relationships.
- [ ] Interfaces: Canonical JSON contracts
- [ ] Failure behaviour: Mapper errors are per-record findings/DLQ.
- [ ] Verified by: Golden mapping tests.
- [ ] Complete when: Same source record maps deterministically for same mapper version.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/identity/resolver.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/identity/resolver.py#L1-L1), [`scripts/tick_phase2_batch1.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L8-L8)
- tests: `tests/unit/test_identity_resolver.py:5`, `tests/unit/test_identity_resolver.py::test_email_resolution`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-INGEST-003 [P1] FR-INGEST-003: Idempotent mutation

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:121-130` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 34, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-INGEST-003 — Idempotent mutation
**WHAT:** Use deterministic canonical IDs and mutation upserts.  
**WHY:** Repeated sync must not duplicate graph facts.  
**HOW:** Canonical IDs hash namespace/type/source identity; edges use deterministic semantic key.  
**DATA / INTERFACES:** GraphMutation v1  
**FAILURE:** Conflict surfaces validation finding; no blind merge.  
**TEST:** Double-ingest E2E.  
**COMPLETE WHEN:** Second identical run does not increase logical entity/edge counts.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Use deterministic canonical IDs and mutation upserts.
- [ ] Interfaces: GraphMutation v1
- [ ] Failure behaviour: Conflict surfaces validation finding; no blind merge.
- [ ] Verified by: Double-ingest E2E.
- [ ] Complete when: Second identical run does not increase logical entity/edge counts.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ontology/manifest.py:471`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/manifest.py#L471-L471)
- tests: `tests/unit/test_edge_dedup.py:1`, `tests/unit/test_phase2_hugegraph_schema.py:359`, `tests/unit/test_phase2_hugegraph_schema.py::test_hugegraph_edge_upsert_updates_matching_edge_key_instead_of_duplicating`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-INGEST-004 [P1] FR-INGEST-004: Ingestion job lifecycle

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:131-140` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-INGEST-004 — Ingestion job lifecycle
**WHAT:** Track queued/running/succeeded/partial/failed/cancelled states.  
**WHY:** Admin UI and recovery need truthful state.  
**HOW:** Each run records counts, checkpoint, timings, versions and errors in meta graph and local logs.  
**DATA / INTERFACES:** IngestionRun  
**FAILURE:** Worker crash leaves resumable state.  
**TEST:** State-transition tests.  
**COMPLETE WHEN:** Admin UI reflects actual backend run state.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Track queued/running/succeeded/partial/failed/cancelled states.
- [ ] Failure behaviour: Worker crash leaves resumable state.
- [ ] Verified by: State-transition tests.
- [ ] Complete when: Admin UI reflects actual backend run state.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L8-L8)
- tests: `tests/unit/test_acquisition_fabric.py:68`, `tests/unit/test_acquisition_fabric.py::test_baseline_controller_persists_ordered_restart_manifest`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-MCP-001 [P1] FR-MCP-001: MCP read server

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:605-614` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-MCP-001 — MCP read server
**WHAT:** Expose search_entity/get_entity/neighbors/path/query/impact/code/jira/document/lineage/evidence as local MCP tools/resources.  
**WHY:** Developer and agent clients need standard context access.  
**HOW:** Thin adapter calls same application services and policy layer as REST.  
**DATA / INTERFACES:** MCP tool schemas  
**FAILURE:** Backend/policy errors map to structured MCP errors.  
**TEST:** MCP contract/E2E tests.  
**COMPLETE WHEN:** MCP returns same graph evidence as REST for demo case.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Expose search_entity/get_entity/neighbors/path/query/impact/code/jira/document/lineage/evidence as local MCP tools/resources.
- [ ] Interfaces: MCP tool schemas
- [ ] Failure behaviour: Backend/policy errors map to structured MCP errors.
- [ ] Verified by: MCP contract/E2E tests.
- [ ] Complete when: MCP returns same graph evidence as REST for demo case.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/mcp/main.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/mcp/main.py#L1-L1), [`scripts/tick_phase0_phase1.py:21`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L21-L21)
- tests: `tests/security/test_verification_suite.py:168`, `tests/security/test_verification_suite.py::test_mcp_tool_surface_is_read_only`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-MCP-002 [P1] FR-MCP-002: MCP action separation

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:615-624` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-MCP-002 — MCP action separation
**WHAT:** Keep write/action tools in separate registry and disabled in MVP.  
**WHY:** Protocol access must not expand authority.  
**HOW:** Action tools require explicit config, risk policy and confirmation in later phases.  
**DATA / INTERFACES:** ToolRegistry  
**FAILURE:** Disabled writes are not advertised.  
**TEST:** Capability-list tests.  
**COMPLETE WHEN:** MVP MCP surface is read-only.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Keep write/action tools in separate registry and disabled in MVP.
- [ ] Failure behaviour: Disabled writes are not advertised.
- [ ] Verified by: Capability-list tests.
- [ ] Complete when: MVP MCP surface is read-only.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/mcp/main.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/mcp/main.py#L1-L1), [`scripts/tick_phase0_phase1.py:21`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L21-L21)
- tests: `tests/security/test_verification_suite.py:168`, `tests/security/test_verification_suite.py::test_mcp_tool_surface_is_read_only`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-MEM-001 [P1] FR-MEM-001: Scoped memory records

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:595-604` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 36, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-MEM-001 — Scoped memory records
**WHAT:** Model working/task/conversation/semantic/episodic/procedural memory with scope/source/TTL/provenance/confidence/classification/deletion policy.  
**WHY:** Agent memory must be governable.  
**HOW:** MVP persists only task/audit evidence needed for TraceImpact; broad long-term memory is later.  
**DATA / INTERFACES:** MemoryRecord  
**FAILURE:** Expired/forbidden memory excluded.  
**TEST:** TTL/scope tests.  
**COMPLETE WHEN:** No uncontrolled accumulation in MVP.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Model working/task/conversation/semantic/episodic/procedural memory with scope/source/TTL/provenance/confidence/classification/deletion policy.
- [ ] Failure behaviour: Expired/forbidden memory excluded.
- [ ] Verified by: TTL/scope tests.
- [ ] Complete when: No uncontrolled accumulation in MVP.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/contracts/memory.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/contracts/memory.py#L4-L4)
- tests: `tests/unit/test_agent_memory.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-ONTO-001 [P1] FR-ONTO-001: Enterprise ontology vocabulary

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:255-264` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-ONTO-001 — Enterprise ontology vocabulary
**WHAT:** Version organization, work, code, CI/CD, operations, knowledge and AI/agent concepts.  
**WHY:** Cross-source semantics require a controlled vocabulary.  
**HOW:** Terms have URI/name, definition, domain/range, cardinality and lifecycle status.  
**DATA / INTERFACES:** Ontology manifest  
**FAILURE:** Unknown/deprecated term creates validation error/warning.  
**TEST:** Ontology conformance tests.  
**COMPLETE WHEN:** MVP entities/edges reference ontology version and valid terms.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Version organization, work, code, CI/CD, operations, knowledge and AI/agent concepts.
- [ ] Interfaces: Ontology manifest
- [ ] Failure behaviour: Unknown/deprecated term creates validation error/warning.
- [ ] Verified by: Ontology conformance tests.
- [ ] Complete when: MVP entities/edges reference ontology version and valid terms.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ontology/manifest.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/manifest.py#L1-L1), [`scripts/tick_phase0_phase1.py:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L16-L16)
- tests: `tests/unit/test_manifest_integrity.py:15`, `tests/unit/test_manifest_integrity.py::test_every_edge_endpoint_is_a_known_vertex_label`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-ONTO-002 [P1] FR-ONTO-002: Relationship semantics

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:265-274` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-ONTO-002 — Relationship semantics
**WHAT:** Distinguish containment, identity, dependency, implementation, authorship, provenance, temporal and cross-domain semantics.  
**WHY:** Generic RELATED_TO edges destroy explainability.  
**HOW:** Every edge label has explicit domain/range, direction, inverse semantics where relevant and evidence policy.  
**DATA / INTERFACES:** Edge manifest  
**FAILURE:** Invalid endpoints rejected or quarantined.  
**TEST:** Edge domain/range tests.  
**COMPLETE WHEN:** No MVP business relationship relies on untyped generic edge.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Distinguish containment, identity, dependency, implementation, authorship, provenance, temporal and cross-domain semantics.
- [ ] Interfaces: Edge manifest
- [ ] Failure behaviour: Invalid endpoints rejected or quarantined.
- [ ] Verified by: Edge domain/range tests.
- [ ] Complete when: No MVP business relationship relies on untyped generic edge.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ontology/manifest.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/manifest.py#L1-L1), [`scripts/tick_phase0_phase1.py:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L16-L16)
- tests: `tests/unit/test_manifest_integrity.py:15`, `tests/unit/test_manifest_integrity.py::test_every_edge_endpoint_is_a_known_vertex_label`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-PROV-001 [P1] FR-PROV-001: Evidence model

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:275-284` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-PROV-001 — Evidence model
**WHAT:** Attach source reference, event hash, extraction time, mapper/parser version, confidence and creation status.  
**WHY:** Answers and inferred links must be defensible.  
**HOW:** Evidence nodes/records link to entities and relationships; DETERMINISTIC/INFERRED/HUMAN_CONFIRMED status is mandatory.  
**DATA / INTERFACES:** Evidence v1  
**FAILURE:** Missing evidence makes inferred fact invalid.  
**TEST:** Provenance coverage tests.  
**COMPLETE WHEN:** MVP evidence coverage is 100% for cross-domain bridge edges.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Attach source reference, event hash, extraction time, mapper/parser version, confidence and creation status.
- [ ] Interfaces: Evidence v1
- [ ] Failure behaviour: Missing evidence makes inferred fact invalid.
- [ ] Verified by: Provenance coverage tests.
- [ ] Complete when: MVP evidence coverage is 100% for cross-domain bridge edges.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/provenance/evidence.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/provenance/evidence.py#L1-L1), [`scripts/tick_phase0_phase1.py:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L16-L16)
- tests: `tests/unit/test_gap_governance_controls.py:119`, `tests/unit/test_gap_governance_controls.py::test_evidence_manifest_links_answer_to_nodes_edges_sources_and_trust`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-PROV-002 [P1] FR-PROV-002: Provenance traversal

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:285-294` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 2, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-PROV-002 — Provenance traversal
**WHAT:** Support reverse traversal from graph fact to source event and ingestion run.  
**WHY:** Audit/debugging needs chain of custody.  
**HOW:** API exposes evidence references and lineage path.  
**DATA / INTERFACES:** Evidence, SourceEvent, IngestionRun  
**FAILURE:** Missing source artifact is reported, not hidden.  
**TEST:** Lineage API E2E.  
**COMPLETE WHEN:** User can trace demo answer to source fixture/commit metadata.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Support reverse traversal from graph fact to source event and ingestion run.
- [ ] Interfaces: Evidence, SourceEvent, IngestionRun
- [ ] Failure behaviour: Missing source artifact is reported, not hidden.
- [ ] Verified by: Lineage API E2E.
- [ ] Complete when: User can trace demo answer to source fixture/commit metadata.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/provenance/lineage.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/provenance/lineage.py#L1-L1), [`scripts/tick_phase0_phase1.py:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L16-L16)
- tests: `tests/unit/test_provenance.py:31`, `tests/unit/test_provenance.py::test_lineage_traces_to_source`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-QUERY-001 [P1] FR-QUERY-001: Structured QueryPlan

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:375-384` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-FR-QUERY-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-QUERY-001 — Structured QueryPlan
**WHAT:** Represent user/agent query intent as a typed plan before Gremlin.  
**WHY:** Separates interpretation from execution and enables policy.  
**HOW:** QueryPlan contains intent, anchors, relationship allowlist, depth, filters, limits and evidence mode.  
**DATA / INTERFACES:** QueryPlan v1  
**FAILURE:** Invalid/oversized plans rejected before graph call.  
**TEST:** Schema/property-based tests.  
**COMPLETE WHEN:** All NL and structured requests compile to validated QueryPlan.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-FR-QUERY-001

**Acceptance criteria**
- [ ] Delivers: Represent user/agent query intent as a typed plan before Gremlin.
- [ ] Interfaces: QueryPlan v1
- [ ] Failure behaviour: Invalid/oversized plans rejected before graph call.
- [ ] Verified by: Schema/property-based tests.
- [ ] Complete when: All NL and structured requests compile to validated QueryPlan.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/contracts/query_plan.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/contracts/query_plan.py#L6-L6), [`scripts/tick_phase0_phase1.py:21`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L21-L21)
- tests: `tests/unit/test_query_executor.py:25`, `tests/unit/test_query_executor.py::test_impact_via_executor`, `tests/unit/test_query_executor.py::test_path_via_executor`, `tests/unit/test_query_executor.py::test_search_via_executor`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-QUERY-002 [P1] FR-QUERY-002: Path query

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:385-394` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-FR-QUERY-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-QUERY-002 — Path query
**WHAT:** Find bounded paths between known entities.  
**WHY:** Core traceability questions are path questions.  
**HOW:** Use template with max depth, relationship allowlist, timeout and result cap.  
**DATA / INTERFACES:** Entity IDs, QueryPlan  
**FAILURE:** No path returns empty evidence-backed result; timeout is explicit.  
**TEST:** Known/unknown/over-depth tests.  
**COMPLETE WHEN:** Demo Jira-to-function path returns expected ordered edges.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-FR-QUERY-002

**Acceptance criteria**
- [ ] Delivers: Find bounded paths between known entities.
- [ ] Interfaces: Entity IDs, QueryPlan
- [ ] Failure behaviour: No path returns empty evidence-backed result; timeout is explicit.
- [ ] Verified by: Known/unknown/over-depth tests.
- [ ] Complete when: Demo Jira-to-function path returns expected ordered edges.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/contracts/graph_result.py:27`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/contracts/graph_result.py#L27-L27), [`scripts/tick_phase0_phase1.py:21`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L21-L21)
- tests: `tests/unit/test_query_executor.py:35`, `tests/unit/test_query_executor.py::test_path_via_executor`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-QUERY-003 [P1] FR-QUERY-003: Impact analysis

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:395-404` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 22, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-FR-QUERY-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-QUERY-003 — Impact analysis
**WHAT:** Compute directional bounded blast radius using configured impact edge semantics.  
**WHY:** Users need change consequences, not generic neighborhoods.  
**HOW:** Traverse allowlisted dependency/call/implementation edges, dedupe, rank by path length/evidence and report why each node is included.  
**DATA / INTERFACES:** Anchor entity, impact policy  
**FAILURE:** Cycles bounded; partial results marked on timeout.  
**TEST:** Cyclic graph and golden blast-radius tests.  
**COMPLETE WHEN:** Demo function change returns expected dependents with paths.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-FR-QUERY-003

**Acceptance criteria**
- [ ] Delivers: Compute directional bounded blast radius using configured impact edge semantics.
- [ ] Interfaces: Anchor entity, impact policy
- [ ] Failure behaviour: Cycles bounded; partial results marked on timeout.
- [ ] Verified by: Cyclic graph and golden blast-radius tests.
- [ ] Complete when: Demo function change returns expected dependents with paths.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/contracts/graph_result.py:48`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/contracts/graph_result.py#L48-L48), [`scripts/tick_phase0_phase1.py:21`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L21-L21)
- tests: `tests/unit/test_graph_traversal.py:32`, `tests/unit/test_graph_traversal.py::test_impact_is_bounded_and_excludes_non_allowlisted_edges`, `tests/unit/test_query_executor.py:48`, `tests/unit/test_query_executor.py::test_impact_via_executor`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-QUERY-004 [P1] FR-QUERY-004: Entity search

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:405-414` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-FR-QUERY-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-QUERY-004 — Entity search
**WHAT:** Search by canonical/source IDs, issue key, commit SHA, symbol/path and names.  
**WHY:** Users need reliable anchors before traversal.  
**HOW:** Exact/indexed identifiers first; bounded text/name match second.  
**DATA / INTERFACES:** SearchRequest  
**FAILURE:** Broad queries require minimum term and result cap.  
**TEST:** Search relevance/limit tests.  
**COMPLETE WHEN:** Demo Jira issue, commit and symbol are discoverable.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-FR-QUERY-004

**Acceptance criteria**
- [ ] Delivers: Search by canonical/source IDs, issue key, commit SHA, symbol/path and names.
- [ ] Failure behaviour: Broad queries require minimum term and result cap.
- [ ] Verified by: Search relevance/limit tests.
- [ ] Complete when: Demo Jira issue, commit and symbol are discoverable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:21`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L21-L21)
- tests: `tests/unit/test_query_executor.py:25`, `tests/unit/test_query_executor.py::test_search_via_executor`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-QUERY-005 [P1] FR-QUERY-005: Natural-language query interpretation

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:415-424` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-FR-QUERY-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-QUERY-005 — Natural-language query interpretation
**WHAT:** Interpret supported NL intents locally and safely.  
**WHY:** Natural interaction improves usability without sacrificing graph safety.  
**HOW:** Rule/regex fast path handles canonical questions; local LLM may produce QueryPlan JSON only, never executable Gremlin.  
**DATA / INTERFACES:** NL text, schema snapshot  
**FAILURE:** Model failure falls back to deterministic intents or requests structured refinement.  
**TEST:** Adversarial prompt/query tests.  
**COMPLETE WHEN:** Prompt injection cannot bypass QueryPlan policy.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-FR-QUERY-005

**Acceptance criteria**
- [ ] Delivers: Interpret supported NL intents locally and safely.
- [ ] Interfaces: NL text, schema snapshot
- [ ] Failure behaviour: Model failure falls back to deterministic intents or requests structured refinement.
- [ ] Verified by: Adversarial prompt/query tests.
- [ ] Complete when: Prompt injection cannot bypass QueryPlan policy.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/contracts/query_plan.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/contracts/query_plan.py#L6-L6), [`packages/eoip/query/nl.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/nl.py#L1-L1)
- tests: `tests/unit/test_query_nl.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-QUERY-006 [P1] FR-QUERY-006: Query safety policy

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:425-434` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-FR-QUERY-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-QUERY-006 — Query safety policy
**WHAT:** Enforce traversal depth, result count, timeout, relationship/property allowlists and read-only mode.  
**WHY:** Graph queries can be computationally expensive or destructive.  
**HOW:** Policy validates plans and server-side execution wrapper cancels/limits work where supported.  
**DATA / INTERFACES:** QueryPolicy  
**FAILURE:** Violation returns stable error code and audit event.  
**TEST:** Boundary/fuzz tests.  
**COMPLETE WHEN:** All exposed query endpoints pass policy conformance suite.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-FR-QUERY-006

**Acceptance criteria**
- [ ] Delivers: Enforce traversal depth, result count, timeout, relationship/property allowlists and read-only mode.
- [ ] Failure behaviour: Violation returns stable error code and audit event.
- [ ] Verified by: Boundary/fuzz tests.
- [ ] Complete when: All exposed query endpoints pass policy conformance suite.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/query/policy.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/policy.py#L1-L1)
- tests: `tests/unit/test_query_policy.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-QUERY-007 [P1] FR-QUERY-007: Query evidence envelope

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:435-444` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-FR-QUERY-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-QUERY-007 — Query evidence envelope
**WHAT:** Every derived result can include paths, fact IDs and evidence references.  
**WHY:** Explainability requires more than answer text.  
**HOW:** API returns answer-independent GraphResult/Evidence objects.  
**DATA / INTERFACES:** GraphResult v1  
**FAILURE:** Missing evidence is visible in result quality.  
**TEST:** Evidence completeness tests.  
**COMPLETE WHEN:** GraphRAG/UI/MCP consume same evidence format.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-FR-QUERY-007

**Acceptance criteria**
- [ ] Delivers: Every derived result can include paths, fact IDs and evidence references.
- [ ] Interfaces: GraphResult v1
- [ ] Failure behaviour: Missing evidence is visible in result quality.
- [ ] Verified by: Evidence completeness tests.
- [ ] Complete when: GraphRAG/UI/MCP consume same evidence format.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/contracts/graph_result.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/contracts/graph_result.py#L4-L4), [`scripts/tick_phase0_phase1.py:21`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L21-L21)
- tests: `tests/unit/test_query_executor.py:35`, `tests/unit/test_query_executor.py::test_impact_via_executor`, `tests/unit/test_query_executor.py::test_path_via_executor`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-QUERY-008 [P1] FR-QUERY-008: Raw Gremlin admin boundary

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:445-454` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-FR-QUERY-008; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-QUERY-008 — Raw Gremlin admin boundary
**WHAT:** Do not expose unrestricted Gremlin to user app, agent or MCP.  
**WHY:** Prevents arbitrary traversal/mutation and injection.  
**HOW:** Developer-only local diagnostic path is disabled by default and never used by normal flows.  
**DATA / INTERFACES:** Admin configuration  
**FAILURE:** Disabled path returns 404/403-like policy response.  
**TEST:** Endpoint exposure tests.  
**COMPLETE WHEN:** No public OpenAPI/MCP tool accepts free-form Gremlin in MVP.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-FR-QUERY-008

**Acceptance criteria**
- [ ] Delivers: Do not expose unrestricted Gremlin to user app, agent or MCP.
- [ ] Interfaces: Admin configuration
- [ ] Failure behaviour: Disabled path returns 404/403-like policy response.
- [ ] Verified by: Endpoint exposure tests.
- [ ] Complete when: No public OpenAPI/MCP tool accepts free-form Gremlin in MVP.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/contracts/query_plan.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/contracts/query_plan.py#L6-L6), [`packages/eoip/query/policy.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/policy.py#L1-L1)
- tests: `tests/unit/test_admin_gremlin.py:1`, `tests/unit/test_query_policy.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-RAG-001 [P1] FR-RAG-001: Retrieval router

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:485-494` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-RAG-001 — Retrieval router
**WHAT:** Choose direct graph, linked documents, code context, graph+text hybrid or no retrieval.  
**WHY:** Avoid unnecessary LLM/vector infrastructure and token use.  
**HOW:** Deterministic intent rules first; pluggable local classifier later.  
**DATA / INTERFACES:** RetrievalRequest  
**FAILURE:** Unknown intent chooses conservative graph/search path.  
**TEST:** Router table tests.  
**COMPLETE WHEN:** Known MVP questions route without external service.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Choose direct graph, linked documents, code context, graph+text hybrid or no retrieval.
- [ ] Failure behaviour: Unknown intent chooses conservative graph/search path.
- [ ] Verified by: Router table tests.
- [ ] Complete when: Known MVP questions route without external service.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/retrieval/service.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/retrieval/service.py#L3-L3), [`scripts/tick_phase0_phase1.py:22`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L22-L22)
- tests: `tests/unit/test_retrieval.py:23`, `tests/unit/test_retrieval.py::test_retrieval_router_selects_code_context_for_code_question`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-RAG-002 [P1] FR-RAG-002: GraphRAG evidence retrieval

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:495-504` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-RAG-002 — GraphRAG evidence retrieval
**WHAT:** Retrieve entities, relationships, paths, neighborhoods, provenance and linked documents.  
**WHY:** Answers must be grounded in authoritative graph context.  
**HOW:** Convert bounded GraphResult into context blocks with stable citations.  
**DATA / INTERFACES:** GraphResult/Evidence  
**FAILURE:** Insufficient evidence yields explicit insufficiency, not invention.  
**TEST:** Golden question/evidence tests.  
**COMPLETE WHEN:** Demo GraphRAG answer cites graph/source references.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Retrieve entities, relationships, paths, neighborhoods, provenance and linked documents.
- [ ] Failure behaviour: Insufficient evidence yields explicit insufficiency, not invention.
- [ ] Verified by: Golden question/evidence tests.
- [ ] Complete when: Demo GraphRAG answer cites graph/source references.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/models/provider.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/models/provider.py#L1-L1), [`packages/eoip/retrieval/service.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/retrieval/service.py#L3-L3), [`scripts/tick_phase0_phase1.py:22`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L22-L22)
- tests: `tests/unit/test_retrieval.py:48`, `tests/unit/test_retrieval.py::test_code_context_preserves_relationship_evidence`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-RAG-003 [P1] FR-RAG-003: Local model abstraction

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:505-514` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-RAG-003 — Local model abstraction
**WHAT:** Provide model interface for chat/generation and optional embeddings with all external providers disabled in MVP.  
**WHY:** Local-first is non-negotiable and future providers must not leak enterprise data.  
**HOW:** Configuration supports a local OpenAI-compatible/Ollama-style adapter; external adapter code is disabled by policy.  
**DATA / INTERFACES:** ModelRequest/Response  
**FAILURE:** Model-down degrades to graph results and deterministic summaries.  
**TEST:** No-egress/model-down tests.  
**COMPLETE WHEN:** Core search/path/impact remains usable with model service stopped.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Provide model interface for chat/generation and optional embeddings with all external providers disabled in MVP.
- [ ] Failure behaviour: Model-down degrades to graph results and deterministic summaries.
- [ ] Verified by: No-egress/model-down tests.
- [ ] Complete when: Core search/path/impact remains usable with model service stopped.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/retrieval/service.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/retrieval/service.py#L4-L4), [`scripts/tick_phase0_phase1.py:22`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L22-L22)
- tests: `tests/unit/test_retrieval.py:6`, `tests/unit/test_retrieval.py::test_model_unavailable_retains_independent_graph_evidence`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-RAG-004 [P1] FR-RAG-004: No mandatory vector DB in MVP

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:515-524` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-RAG-004 — No mandatory vector DB in MVP
**WHAT:** Do not require a second database for semantic retrieval in Phase 1.  
**WHY:** Infrastructure must stay minimal.  
**HOW:** Use graph, metadata, document sections and local lexical retrieval; optional embeddings may be evaluated in-process/file-indexed.  
**DATA / INTERFACES:** DocumentSection  
**FAILURE:** Semantic-only request reports reduced capability if embeddings disabled.  
**TEST:** Model-off tests.  
**COMPLETE WHEN:** MVP starts and demos without vector database.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Do not require a second database for semantic retrieval in Phase 1.
- [ ] Failure behaviour: Semantic-only request reports reduced capability if embeddings disabled.
- [ ] Verified by: Model-off tests.
- [ ] Complete when: MVP starts and demos without vector database.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:22`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L22-L22)
- tests: `tests/unit/test_retrieval.py:6`, `tests/unit/test_retrieval.py::test_model_unavailable_retains_independent_graph_evidence`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-RAG-005 [P1] FR-RAG-005: RAG evaluation harness

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:525-534` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-RAG-005 — RAG evaluation harness
**WHAT:** Measure retrieval precision/recall, context relevance, evidence coverage, groundedness, answer correctness, latency and token usage.  
**WHY:** RAG quality must be testable.  
**HOW:** Golden QA dataset includes expected entities/paths/evidence.  
**DATA / INTERFACES:** EvalCase/EvalResult  
**FAILURE:** Failed generation does not erase retrieval metrics.  
**TEST:** Automated evaluation tests.  
**COMPLETE WHEN:** Baseline report is reproducible locally.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Measure retrieval precision/recall, context relevance, evidence coverage, groundedness, answer correctness, latency and token usage.
- [ ] Failure behaviour: Failed generation does not erase retrieval metrics.
- [ ] Verified by: Automated evaluation tests.
- [ ] Complete when: Baseline report is reproducible locally.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/retrieval/eval.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/retrieval/eval.py#L1-L1), [`scripts/rag_eval.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/rag_eval.py#L1-L1)
- tests: `tests/unit/test_retrieval_eval.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-UI-001 [P1] FR-UI-001: User web application

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:625-634` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-UI-001 — User web application
**WHAT:** Provide search/NL query, graph visualization, details/evidence, path and impact views backed by real APIs.  
**WHY:** MVP must demonstrate value interactively.  
**HOW:** React/TypeScript app uses /api/v1; no hardcoded domain responses.  
**DATA / INTERFACES:** REST/SSE  
**FAILURE:** API failure shows explicit degraded/error state.  
**TEST:** Component + Playwright E2E.  
**COMPLETE WHEN:** Demo flow works from persisted data.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Provide search/NL query, graph visualization, details/evidence, path and impact views backed by real APIs.
- [ ] Failure behaviour: API failure shows explicit degraded/error state.
- [ ] Verified by: Component + Playwright E2E.
- [ ] Complete when: Demo flow works from persisted data.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:54`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L54-L54), [`scripts/check_wp53_registry.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/check_wp53_registry.py#L8-L8)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:5`, `tests/unit/test_web_ux_and_admin_wp53.py::test_fr_ui_001_user_web_application`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-UI-002 [P1] FR-UI-002: Graph explorer

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:635-644` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 45, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-UI-002 — Graph explorer
**WHAT:** Visualize typed nodes/edges with filters, expansion, path highlighting and provenance.  
**WHY:** Users need interpretable graph navigation.  
**HOW:** Cytoscape.js loaded locally; server returns bounded subgraphs.  
**DATA / INTERFACES:** GraphResult  
**FAILURE:** Large result prompts/refuses expansion beyond cap.  
**TEST:** Visual E2E + API bounds.  
**COMPLETE WHEN:** Demo path is highlighted with evidence access.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Visualize typed nodes/edges with filters, expansion, path highlighting and provenance.
- [ ] Failure behaviour: Large result prompts/refuses expansion beyond cap.
- [ ] Verified by: Visual E2E + API bounds.
- [ ] Complete when: Demo path is highlighted with evidence access.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_mark_wp53_done.py:61`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp53_done.py#L61-L61), [`scripts/check_wp53_registry.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/check_wp53_registry.py#L8-L8)
- tests: `tests/unit/test_web_ux_and_admin_wp53.py:136`, `tests/unit/test_web_ux_and_admin_wp53.py::test_fr_ui_002_graph_explorer`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-VALID-001 [P1] FR-VALID-001: Graph validation rules

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:455-464` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-VALID-001 — Graph validation rules
**WHAT:** Execute rule packs for orphan, endpoint/domain-range, duplicate, provenance, mandatory edge, type and dangling reference checks.  
**WHY:** Graph correctness must be measurable.  
**HOW:** Rules produce ValidationFinding with rule, severity, entity/edge refs, evidence and remediation.  
**DATA / INTERFACES:** ValidationRun/Finding  
**FAILURE:** Rule failure isolated and reported.  
**TEST:** Seeded-invalid-graph tests.  
**COMPLETE WHEN:** Admin UI shows real findings from demo data.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Execute rule packs for orphan, endpoint/domain-range, duplicate, provenance, mandatory edge, type and dangling reference checks.
- [ ] Failure behaviour: Rule failure isolated and reported.
- [ ] Verified by: Seeded-invalid-graph tests.
- [ ] Complete when: Admin UI shows real findings from demo data.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/validation/engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/validation/engine.py#L1-L1), [`scripts/tick_phase0_phase1.py:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L17-L17)
- tests: `tests/unit/test_validation_engine.py:24`, `tests/unit/test_validation_engine.py::test_valid_graph_passes_validation`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-VALID-002 [P1] FR-VALID-002: Validation gates

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:465-474` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-VALID-002 — Validation gates
**WHAT:** Block or quarantine mutations that violate hard invariants; soft rules run post-ingestion.  
**WHY:** Not all quality defects have equal risk.  
**HOW:** ERROR invariants prevent commit; WARN/INFO findings persist.  
**DATA / INTERFACES:** Rule policy  
**FAILURE:** Partial batches are rolled back or safely marked by mutation strategy.  
**TEST:** Hard/soft rule tests.  
**COMPLETE WHEN:** Invalid endpoint edge cannot silently enter graph.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Block or quarantine mutations that violate hard invariants; soft rules run post-ingestion.
- [ ] Interfaces: Rule policy
- [ ] Failure behaviour: Partial batches are rolled back or safely marked by mutation strategy.
- [ ] Verified by: Hard/soft rule tests.
- [ ] Complete when: Invalid endpoint edge cannot silently enter graph.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ontology/manifest.py:379`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/manifest.py#L379-L379), [`packages/eoip/validation/engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/validation/engine.py#L1-L1), [`packages/eoip/validation/gate.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/validation/gate.py#L1-L1), [`packages/eoip/validation/quality.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/validation/quality.py#L1-L1), [`scripts/tick_phase0_phase1.py:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L17-L17)
- tests: `tests/unit/test_validation_engine.py:24`, `tests/unit/test_validation_engine.py::test_valid_graph_passes_validation`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-VALID-003 [P1] FR-VALID-003: Graph quality metrics

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:475-484` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-VALID-003 — Graph quality metrics
**WHAT:** Compute completeness, freshness, orphan rate, duplicate rate, provenance/evidence coverage and schema compliance.  
**WHY:** Admin users need trendable graph health.  
**HOW:** Metrics derive from validation and graph stats; MVP computes per run/domain.  
**DATA / INTERFACES:** QualitySnapshot  
**FAILURE:** Unknown denominator reported as N/A, not false zero/100%.  
**TEST:** Metric fixture tests.  
**COMPLETE WHEN:** Dashboard values reconcile with fixture counts.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Compute completeness, freshness, orphan rate, duplicate rate, provenance/evidence coverage and schema compliance.
- [ ] Failure behaviour: Unknown denominator reported as N/A, not false zero/100%.
- [ ] Verified by: Metric fixture tests.
- [ ] Complete when: Dashboard values reconcile with fixture counts.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/App.jsx:79`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/App.jsx#L79-L79), [`packages/eoip/ci/pipeline.py:64`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ci/pipeline.py#L64-L64), [`packages/eoip/validation/quality.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/validation/quality.py#L1-L1)
- tests: `tests/unit/test_quality.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-VSCODE-001 [P1] FR-VSCODE-001: VS Code context extension

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:665-674` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-VSCODE-001 — VS Code context extension
**WHAT:** Provide sidebar/webview showing current file/symbol, Jira, commits, dependencies, docs and provenance.  
**WHY:** Developer workflow is a required product surface.  
**HOW:** Extension resolves local workspace path/symbol and calls platform API over configured local endpoint.  
**DATA / INTERFACES:** Extension API contract  
**FAILURE:** Unavailable platform shows offline state; no source modification.  
**TEST:** Extension host tests.  
**COMPLETE WHEN:** Opening demo function retrieves correct graph context.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Provide sidebar/webview showing current file/symbol, Jira, commits, dependencies, docs and provenance.
- [ ] Interfaces: Extension API contract
- [ ] Failure behaviour: Unavailable platform shows offline state; no source modification.
- [ ] Verified by: Extension host tests.
- [ ] Complete when: Opening demo function retrieves correct graph context.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/vscode-extension/extension.js:395`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/vscode-extension/extension.js#L395-L395), [`scripts/_find_vsc_specs.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_find_vsc_specs.py#L13-L13), [`scripts/_inspect_vsc_reqs.py:5`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_inspect_vsc_reqs.py#L5-L5), [`scripts/_mark_wp54_and_wp55_done.py:21`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp54_and_wp55_done.py#L21-L21)
- tests: `tests/unit/test_vscode_extension_wp54.py:4`, `tests/unit/test_vscode_extension_wp54.py::test_fr_vscode_001_context_extension`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-FR-VSCODE-002 [P1] FR-VSCODE-002: VS Code trace/impact commands

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:675-683` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-VSCODE-002 — VS Code trace/impact commands
**WHAT:** Commands answer why code exists and what change may affect.  
**WHY:** Makes enterprise graph actionable in editor.  
**HOW:** Commands invoke path/impact services and render evidence.  
**DATA / INTERFACES:** Query API  
**FAILURE:** No unrestricted Gremlin/tool execution.  
**TEST:** Command E2E.  
**COMPLETE WHEN:** Demo command returns Jira→code path and impact.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Commands answer why code exists and what change may affect.
- [ ] Interfaces: Query API
- [ ] Failure behaviour: No unrestricted Gremlin/tool execution.
- [ ] Verified by: Command E2E.
- [ ] Complete when: Demo command returns Jira→code path and impact.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/_find_vsc_specs.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_find_vsc_specs.py#L13-L13), [`scripts/_inspect_vsc_reqs.py:5`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_inspect_vsc_reqs.py#L5-L5), [`scripts/_mark_wp54_and_wp55_done.py:25`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/_mark_wp54_and_wp55_done.py#L25-L25)
- tests: `tests/unit/test_vscode_extension_wp54.py:5`, `tests/unit/test_vscode_extension_wp54.py::test_fr_vscode_002_trace_impact_commands`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

