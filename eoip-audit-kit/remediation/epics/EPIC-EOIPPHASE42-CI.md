# EPIC-EOIPPHASE42-CI: EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 51 tasks, ~50.0 h, priorities {'P0': 2, 'P1': 5, 'P2': 44}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-PRE-001 [P0] PRE-001: Pre-flight: package-collision and baseline reconciliation

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:189-201` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 2, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### PRE-001: Pre-flight: package-collision and baseline reconciliation

- [x] `PRE-001` **Pre-flight: package-collision and baseline reconciliation**
- **Priority**: P0 | **Category**: Pre-flight | **Complexity**: Low
- **Depends on**: none | **Coordinate with**: none
- **Description**: Before any engine is created, verify what already exists. The source document says "Create ... __init__.py" for packages that other documents say exist, and its baseline counts differ from the audits.
- **Acceptance criteria**:
  - [x] `PRE-001.1` Check each package this roadmap creates against the repo (verification/, federation/, causal/, xai/, extraction/, observability/, embeddings/, routing/, token_formats/, token_budget/, graph_graph/, distillation/, gnn/, mlops/); for each, record extend or create in the registry.
  - [x] `PRE-001.2` Resolve baseline conflicts B1 to B3 against the code (database adapters 17+ vs 55, RAG modes 64 vs 45+, UI components 90+ vs 55) and correct the numbers in this file.
  - [x] `PRE-001.3` Decide module ownership for the duplicated extractor work (AGENT-002, AI-002, AI-003) and record it (conflict B6).
  - [x] `PRE-001.4` Decide the load tool (conflict B5, DEC-P4-03) and the overlap handling (DEC-P4-02).
  - [x] `PRE-001.5` List every Phase 4 engine that exposes an API and state how it will be mounted (engine registry SDLC-004 if accepted, otherwise the manual wiring in brain_os.py and platform_router.py).
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Before any engine is created, verify what already exists. The source document says "Create ... __init__.py" for packages that other documents say exist, and its baseline counts differ from the audits.
- [ ] [x] PRE-001.2 Resolve baseline conflicts B1 to B3 against the code (database adapters 17+ vs 55, RAG modes 64 vs 45+, UI components 90+ vs 55) and correct the numbers in this file
- [ ] [x] PRE-001.3 Decide module ownership for the duplicated extractor work (AGENT-002, AI-002, AI-003) and record it (conflict B6)
- [ ] [x] PRE-001.4 Decide the load tool (conflict B5, DEC-P4-03) and the overlap handling (DEC-P4-02)
- [ ] [x] PRE-001.5 List every Phase 4 engine that exposes an API and state how it will be mounted (engine registry SDLC-004 if accepted, otherwise the manual wiring in brainos.py and platformrouter.py)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_phase4_preflight.py:1`, `tests/unit/test_phase4_preflight.py::test_preflight_package_collision_and_baselines`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PRE-002 [P0] PRE-002: Pre-flight: register Phase 4 in the KGF registry and adopt the Universal Definition of Done

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:202-213` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 2, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### PRE-002: Pre-flight: register Phase 4 in the KGF registry and adopt the Universal Definition of Done

- [x] `PRE-002` **Pre-flight: register Phase 4 in the KGF registry and adopt the Universal Definition of Done**
- **Priority**: P0 | **Category**: Pre-flight | **Complexity**: Low
- **Depends on**: none | **Coordinate with**: none
- **Description**: Phase 4 shares the KGF programme's evidence rules. Register the IDs and agree the single definition of done so closing a Phase 4 item also closes the overlapping KGF item.
- **Acceptance criteria**:
  - [x] `PRE-002.1` All Phase 4 IDs (and accepted suggestions) are rows in requirements-registry.json (KGF BASE-01) with the cross-IDs from the overlap map.
  - [x] `PRE-002.2` Tests for Phase 4 carry @pytest.mark.req("<ID>") and commits use [ID] (KGF BASE-02).
  - [x] `PRE-002.3` The Universal Definition of Done (section 4) is copied into the pull-request template.
  - [x] `PRE-002.4` For each "merge" overlap, the owning ID is recorded; the other ID is closed by reference when the shared implementation passes.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Phase 4 shares the KGF programme's evidence rules. Register the IDs and agree the single definition of done so closing a Phase 4 item also closes the overlapping KGF item.
- [ ] Depends on: none | Coordinate with: none
- [ ] [x] PRE-002.1 All Phase 4 IDs (and accepted suggestions) are rows in requirements-registry.json (KGF BASE-01) with the cross-IDs from the overlap map
- [ ] [x] PRE-002.2 Tests for Phase 4 carry @pytest.mark.req("<ID>") and commits use [ID] (KGF BASE-02)
- [ ] [x] PRE-002.4 For each "merge" overlap, the owning ID is recorded; the other ID is closed by reference when the shared implementation passes
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_phase4_preflight.py:1`, `tests/unit/test_phase4_preflight.py::test_preflight_requirements_registry_registered`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-AGENT-003 [P1] AGENT-003: merge · MS-17, agents/orchestration.py · Durable bus underlies A2A orchestration. Implement once.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:82-82` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-AGENT-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`AGENT-003` | merge | MS-17, agents/orchestration.py | Durable bus underlies A2A orchestration. Implement once.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-AGENT-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AGENT-003 | merge | MS-17, agents/orchestration.py | Durable bus underlies A2A orchestration. Implement once.»
- [ ] Durable bus underlies A2A orchestration. Implement once.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/agents/message_bus.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/agents/message_bus.py#L1-L1)
- tests: `tests/unit/test_phase4_phase2_engines.py:4`, `tests/unit/test_phase4_phase2_engines.py::TestAgent003MessageBus::test_broadcast_channel`, `tests/unit/test_phase4_phase2_engines.py::TestAgent003MessageBus::test_capability_negotiation`, `tests/unit/test_phase4_phase2_engines.py::TestAgent003MessageBus::test_queue_and_dlq_expiration`, `tests/unit/test_phase4_preflight.py:54`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-COMPLY-002 [P1] COMPLY-002: extend · NFR-PRIV-001, privacy/

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:114-114` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 6 other site(s): see duplicate task DUP-COMPLY-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`COMPLY-002` | extend | NFR-PRIV-001, privacy/ | -
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-COMPLY-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMPLY-002 | extend | NFR-PRIV-001, privacy/ | -»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/privacy/scanner.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/privacy/scanner.py#L1-L1)
- tests: `tests/unit/test_phase4_phase6_7_engines.py:5`, `tests/unit/test_phase4_phase6_7_engines.py::TestComply002PIIDetectionAndAnonymization::test_anonymizer_and_pseudonymizer`, `tests/unit/test_phase4_phase6_7_engines.py::TestComply002PIIDetectionAndAnonymization::test_pii_scanner`, `tests/unit/test_phase4_preflight.py:59`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CORE-006 [P1] CORE-006: merge · MS-27, K-03 · Token accounting in MS-27 and budgets here share one cost model. Build the model once (see AIDLC-008).

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:79-79` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 6 other site(s): see duplicate task DUP-CORE-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CORE-006` | merge | MS-27, K-03 | Token accounting in MS-27 and budgets here share one cost model. Build the model once (see AIDLC-008).
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CORE-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CORE-006 | merge | MS-27, K-03 | Token accounting in MS-27 and budgets here share one cost model. Build the model once (see AIDLC-008).»
- [ ] Token accounting in MS-27 and budgets here share one cost model. Build the model once (see AIDLC-008).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/platform_router.py:424`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/platform_router.py#L424-L424), [`packages/eoip/token_budget/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/token_budget/__init__.py#L1-L1), [`packages/eoip/token_budget/engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/token_budget/engine.py#L1-L1)
- tests: `tests/unit/test_phase4_core_engines.py:1`, `tests/unit/test_phase4_core_engines.py::TestCore006TokenBudget::test_context_compression_on_budget_exceed`, `tests/unit/test_phase4_core_engines.py::TestCore006TokenBudget::test_token_budget_allocation_and_reallocation`, `tests/unit/test_phase4_preflight.py:53`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-INFRA-002 [P1] INFRA-002: merge · H-04, NFR-SEC-005, GAP-SEC-008..012 · Authentication enforcement (H-04) and SSO overlap. Build SSO as the provider side of H-04.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:98-98` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 42, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 7 other site(s): see duplicate task DUP-INFRA-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INFRA-002` | merge | H-04, NFR-SEC-005, GAP-SEC-008..012 | Authentication enforcement (H-04) and SSO overlap. Build SSO as the provider side of H-04.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-INFRA-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INFRA-002 | merge | H-04, NFR-SEC-005, GAP-SEC-008..012 | Authentication enforcement (H-04) and SSO overlap. Build SSO as the provider side of H-04.»
- [ ] Authentication enforcement (H-04) and SSO overlap. Build SSO as the provider side of H-04.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/authn/oauth_sso.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/authn/oauth_sso.py#L1-L1)
- tests: `tests/security/test_token_validation_contract.py:13`, `tests/security/test_token_validation_contract.py::test_arbitrary_malformed_or_unbounded_tokens_are_rejected[None]`, `tests/security/test_token_validation_contract.py::test_arbitrary_malformed_or_unbounded_tokens_are_rejected[]`, `tests/security/test_token_validation_contract.py::test_arbitrary_malformed_or_unbounded_tokens_are_rejected[a.b.c]`, `tests/security/test_token_validation_contract.py::test_arbitrary_malformed_or_unbounded_tokens_are_rejected[arbitrary-long-token-that-used-to-authenticate]`, `tests/security/test_token_validation_contract.py::test_arbitrary_malformed_or_unbounded_tokens_are_rejected[xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx]`, `tests/security/test_token_validation_contract.py::test_conflicting_tenant_claims_are_rejected`, `tests/security/test_token_validation_contract.py::test_even_correctly_signed_invalid_claims_are_rejected[aud-another-api]`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-INFRA-007 [P1] INFRA-007: merge · MVP-FR-025, MVP-FR-026, NFR-REL-002, GAP-HA, REL-10 · Backup and restore appears in the MVP, NFR and release-gate sets.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:103-103` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 7 other site(s): see duplicate task DUP-INFRA-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INFRA-007` | merge | MVP-FR-025, MVP-FR-026, NFR-REL-002, GAP-HA, REL-10 | Backup and restore appears in the MVP, NFR and release-gate sets.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-INFRA-007

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INFRA-007 | merge | MVP-FR-025, MVP-FR-026, NFR-REL-002, GAP-HA, REL-10 | Backup and restore appears in the MVP, NFR and release-gate sets.»
- [ ] MVP-FR-025, MVP-FR-026, NFR-REL-002, GAP-HA, REL-10
- [ ] Backup and restore appears in the MVP, NFR and release-gate sets.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/recovery/backup_scheduler.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/recovery/backup_scheduler.py#L1-L1)
- tests: `tests/unit/test_phase4_phase4_engines.py:9`, `tests/unit/test_phase4_phase4_engines.py::TestInfra007BackupAndRestore::test_automated_restore_drill`, `tests/unit/test_phase4_phase4_engines.py::TestInfra007BackupAndRestore::test_backup_encryption_and_integrity`, `tests/unit/test_phase4_preflight.py:57`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-AGENT-001 [P2] AGENT-001: extend · KGR-G-019, FR-AGENT-004 · Boundary signals feed the calibrated-uncertainty protocol and the approval boundary.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:80-80` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 6 other site(s): see duplicate task DUP-AGENT-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`AGENT-001` | extend | KGR-G-019, FR-AGENT-004 | Boundary signals feed the calibrated-uncertainty protocol and the approval boundary.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-AGENT-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AGENT-001 | extend | KGR-G-019, FR-AGENT-004 | Boundary signals feed the calibrated-uncertainty protocol and the approval boundary.»
- [ ] Boundary signals feed the calibrated-uncertainty protocol and the approval boundary.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/telemetry/adapter.py:129`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/telemetry/adapter.py#L129-L129)
- tests: `tests/unit/test_phase4_phase2_engines.py:2`, `tests/unit/test_phase4_phase2_engines.py::TestAgent001CognitiveBoundaryTelemetry::test_all_seven_boundary_signals`, `tests/unit/test_phase4_preflight.py:54`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-AGENT-002 [P2] AGENT-002: merge · GAP-NLP, KGR-G-015, FR-INGEST-*, G2-EKAF-026 · Duplicates AI-002 (entity extraction) and AI-003 (relation extraction). One extractor implementation, orchestrated here.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:81-81` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 7 other site(s): see duplicate task DUP-AGENT-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`AGENT-002` | merge | GAP-NLP, KGR-G-015, FR-INGEST-*, G2-EKAF-026 | Duplicates AI-002 (entity extraction) and AI-003 (relation extraction). One extractor implementation, orchestrated here.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-AGENT-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AGENT-002 | merge | GAP-NLP, KGR-G-015, FR-INGEST-*, G2-EKAF-026 | Duplicates AI-002 (entity extraction) and AI-003 (relation extraction). One extractor implementation, orchestrated here.»
- [ ] GAP-NLP, KGR-G-015, FR-INGEST-*, G2-EKAF-026
- [ ] Duplicates AI-002 (entity extraction) and AI-003 (relation extraction). One extractor implementation, orchestrated here.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/extraction/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/extraction/__init__.py#L1-L1), [`packages/eoip/extraction/engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/extraction/engine.py#L1-L1), [`packages/eoip/extraction/relation_extractor.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/extraction/relation_extractor.py#L7-L7)
- tests: `tests/unit/test_phase4_phase2_engines.py:3`, `tests/unit/test_phase4_phase2_engines.py::TestAgent002AndAi003Extraction::test_chunker_and_entity_extractor`, `tests/unit/test_phase4_phase2_engines.py::TestAgent002AndAi003Extraction::test_full_pipeline_and_communities`, `tests/unit/test_phase4_phase2_engines.py::TestAgent002AndAi003Extraction::test_relation_extractor_triples`, `tests/unit/test_phase4_preflight.py:54`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-AGENT-004 [P2] AGENT-004: extend · KGR-G-018 · Formalizes analytics/parallel_multihop.py.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:83-83` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-AGENT-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`AGENT-004` | extend | KGR-G-018 | Formalizes analytics/parallel_multihop.py.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-AGENT-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AGENT-004 | extend | KGR-G-018 | Formalizes analytics/parallel_multihop.py.»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/harness/engine.py:188`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/harness/engine.py#L188-L188)
- tests: `tests/unit/test_phase4_phase2_engines.py:5`, `tests/unit/test_phase4_phase2_engines.py::TestAgent004ParallelFanOutFanIn::test_fan_out_fan_in_map_reduce`, `tests/unit/test_phase4_preflight.py:54`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-AI-001 [P2] AI-001: extend · audit/xai_ledger.py, UI-04 · XAI ledger (Merkle tree, HMAC) exists. This adds model-derived attribution; the packages/eoip/xai/ name should extend, not replace, it.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:90-90` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-AI-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`AI-001` | extend | audit/xai_ledger.py, UI-04 | XAI ledger (Merkle tree, HMAC) exists. This adds model-derived attribution; the packages/eoip/xai/ name should extend, not replace, it.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-AI-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AI-001 | extend | audit/xai_ledger.py, UI-04 | XAI ledger (Merkle tree, HMAC) exists. This adds model-derived attribution; the packages/eoip/xai/ name should extend, not replace, it.»
- [ ] XAI ledger (Merkle tree, HMAC) exists. This adds model-derived attribution; the packages/eoip/xai/ name should extend, not replace, it.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/xai/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/xai/__init__.py#L1-L1), [`packages/eoip/xai/engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/xai/engine.py#L1-L1)
- tests: `tests/unit/test_phase4_phase3_engines.py:4`, `tests/unit/test_phase4_phase3_engines.py::TestAI001AdvancedXAI::test_confidence_calibration`, `tests/unit/test_phase4_phase3_engines.py::TestAI001AdvancedXAI::test_decision_trace_graph_and_critical_path`, `tests/unit/test_phase4_phase3_engines.py::TestAI001AdvancedXAI::test_feature_importance_shapley`, `tests/unit/test_phase4_preflight.py:56`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-AI-002 [P2] AI-002: merge · GAP-NLP · Same local NLP pipeline. Implement once together with AGENT-002.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:91-91` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-AI-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`AI-002` | merge | GAP-NLP | Same local NLP pipeline. Implement once together with AGENT-002.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-AI-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AI-002 | merge | GAP-NLP | Same local NLP pipeline. Implement once together with AGENT-002.»
- [ ] Same local NLP pipeline. Implement once together with AGENT-002.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/nlp/pipeline.py:346`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/nlp/pipeline.py#L346-L346)
- tests: `tests/unit/test_phase4_phase3_engines.py:5`, `tests/unit/test_phase4_phase3_engines.py::TestAI002DeepNLP::test_aspect_sentiment_analyzer`, `tests/unit/test_phase4_phase3_engines.py::TestAI002DeepNLP::test_coreference_resolver`, `tests/unit/test_phase4_phase3_engines.py::TestAI002DeepNLP::test_deep_entity_extractor`, `tests/unit/test_phase4_phase3_engines.py::TestAI002DeepNLP::test_topic_modeler_and_language_detector`, `tests/unit/test_phase4_preflight.py:56`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-AI-003 [P2] AI-003: merge · GAP-NLP, KGR-G-015 · See AGENT-002.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:92-92` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-AI-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`AI-003` | merge | GAP-NLP, KGR-G-015 | See AGENT-002.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-AI-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AI-003 | merge | GAP-NLP, KGR-G-015 | See AGENT-002.»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/extraction/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/extraction/__init__.py#L1-L1), [`packages/eoip/extraction/relation_extractor.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/extraction/relation_extractor.py#L1-L1)
- tests: `tests/unit/test_phase4_phase2_engines.py:12`, `tests/unit/test_phase4_phase2_engines.py::TestAgent002AndAi003Extraction::test_chunker_and_entity_extractor`, `tests/unit/test_phase4_phase2_engines.py::TestAgent002AndAi003Extraction::test_full_pipeline_and_communities`, `tests/unit/test_phase4_phase2_engines.py::TestAgent002AndAi003Extraction::test_relation_extractor_triples`, `tests/unit/test_phase4_preflight.py:56`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-AI-004 [P2] AI-004: extend · MS-15, model_management/registry.py

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:93-93` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-AI-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`AI-004` | extend | MS-15, model_management/registry.py | -
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-AI-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AI-004 | extend | MS-15, model_management/registry.py | -»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/model_management/registry.py:359`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/model_management/registry.py#L359-L359)
- tests: `tests/unit/test_phase4_phase3_engines.py:6`, `tests/unit/test_phase4_phase3_engines.py::TestAI004ModelABTestingAndCanary::test_ab_experiment_lifecycle_and_significance`, `tests/unit/test_phase4_phase3_engines.py::TestAI004ModelABTestingAndCanary::test_canary_deployment_promotion_and_auto_rollback`, `tests/unit/test_phase4_preflight.py:56`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-AI-005 [P2] AI-005: extend · MS-15, model_management/ · Fine-tuning runs (MS-15) should log here.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:94-94` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-AI-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`AI-005` | extend | MS-15, model_management/ | Fine-tuning runs (MS-15) should log here.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-AI-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AI-005 | extend | MS-15, model_management/ | Fine-tuning runs (MS-15) should log here.»
- [ ] Fine-tuning runs (MS-15) should log here.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/mlops/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/mlops/__init__.py#L1-L1), [`packages/eoip/mlops/experiment_tracker.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/mlops/experiment_tracker.py#L1-L1)
- tests: `tests/unit/test_phase4_phase3_engines.py:7`, `tests/unit/test_phase4_phase3_engines.py::TestAI005MLOpsExperimentTracking::test_experiment_runs_and_comparison`, `tests/unit/test_phase4_preflight.py:56`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-AI-006 [P2] AI-006: merge · H-02, K-09, KGR-G-016, ontology/embedding_drift.py · H-02 replaces hash embeddings with real ones; this adds versioning and drift. Do H-02 first.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:95-95` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-AI-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`AI-006` | merge | H-02, K-09, KGR-G-016, ontology/embedding_drift.py | H-02 replaces hash embeddings with real ones; this adds versioning and drift. Do H-02 first.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-AI-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AI-006 | merge | H-02, K-09, KGR-G-016, ontology/embedding_drift.py | H-02 replaces hash embeddings with real ones; this adds versioning and drift. Do H-02 first.»
- [ ] H-02, K-09, KGR-G-016, ontology/embedding_drift.py
- [ ] H-02 replaces hash embeddings with real ones; this adds versioning and drift. Do H-02 first.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/embeddings/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/embeddings/__init__.py#L1-L1), [`packages/eoip/embeddings/engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/embeddings/engine.py#L1-L1), [`scripts/update_matrix_caps.py:27`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L27-L27), [`scripts/verify_22_caps.py:155`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L155-L155)
- tests: `tests/unit/test_phase4_phase3_engines.py:8`, `tests/unit/test_phase4_phase3_engines.py::TestAI006EmbeddingManagement::test_embedding_fusion_and_dimension_reduction`, `tests/unit/test_phase4_phase3_engines.py::TestAI006EmbeddingManagement::test_embedding_registry_and_drift_detection`, `tests/unit/test_phase4_preflight.py:56`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-AI-007 [P2] AI-007: own · KGR-G-019, GAP-TRUTH-* · Confidence propagation connects to truth resolution.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:96-96` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-AI-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`AI-007` | own | KGR-G-019, GAP-TRUTH-* | Confidence propagation connects to truth resolution.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-AI-007

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AI-007 | own | KGR-G-019, GAP-TRUTH-* | Confidence propagation connects to truth resolution.»
- [ ] Confidence propagation connects to truth resolution.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/reasoning/strategies.py:561`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/reasoning/strategies.py#L561-L561)
- tests: `tests/unit/test_phase4_phase3_engines.py:9`, `tests/unit/test_phase4_phase3_engines.py::TestAI007ProbabilisticReasoning::test_bayesian_graph_reasoning_and_strategy`, `tests/unit/test_phase4_phase3_engines.py::TestAI007ProbabilisticReasoning::test_uncertainty_propagation`, `tests/unit/test_phase4_preflight.py:56`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-COMPLY-001 [P2] COMPLY-001: extend · compliance/, moonshot/compliance_twin.py, G2-GRAPH-SEC-*, MS-25 · compliance/ package and compliance twin exist.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:113-113` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 7 other site(s): see duplicate task DUP-COMPLY-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`COMPLY-001` | extend | compliance/, moonshot/compliance_twin.py, G2-GRAPH-SEC-*, MS-25 | compliance/ package and compliance twin exist.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-COMPLY-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMPLY-001 | extend | compliance/, moonshot/compliance_twin.py, G2-GRAPH-SEC-*, MS-25 | compliance/ package and compliance twin exist.»
- [ ] compliance/, moonshot/compliance_twin.py, G2-GRAPH-SEC-*, MS-25
- [ ] compliance/ package and compliance twin exist.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/compliance/constraints.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/constraints.py#L1-L1)
- tests: `tests/unit/test_phase4_phase6_7_engines.py:4`, `tests/unit/test_phase4_phase6_7_engines.py::TestComply001ComplianceAsCode::test_compliance_rules_and_monitor`, `tests/unit/test_phase4_preflight.py:59`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-COMPLY-003 [P2] COMPLY-003: extend · MS-24, audit/

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:115-115` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 6 other site(s): see duplicate task DUP-COMPLY-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`COMPLY-003` | extend | MS-24, audit/ | -
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-COMPLY-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMPLY-003 | extend | MS-24, audit/ | -»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/compliance/dashboard.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/dashboard.py#L1-L1)
- tests: `tests/unit/test_phase4_compliance_and_search.py:1`, `tests/unit/test_phase4_compliance_and_search.py::TestContinuousComplianceDashboard::test_attestation_workflow`, `tests/unit/test_phase4_compliance_and_search.py::TestContinuousComplianceDashboard::test_framework_scoring_and_audit_export`, `tests/unit/test_phase4_preflight.py:59`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CORE-001 [P2] CORE-001: own · NFR-PERF-001, K-01 · No equivalent in the KGF backlog. Independent library; can start immediately.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:74-74` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 7 other site(s): see duplicate task DUP-CORE-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CORE-001` | own | NFR-PERF-001, K-01 | No equivalent in the KGF backlog. Independent library; can start immediately.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CORE-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CORE-001 | own | NFR-PERF-001, K-01 | No equivalent in the KGF backlog. Independent library; can start immediately.»
- [ ] No equivalent in the KGF backlog. Independent library; can start immediately.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/platform_router.py:424`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/platform_router.py#L424-L424), [`packages/eoip/token_formats/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/token_formats/__init__.py#L1-L1), [`packages/eoip/token_formats/engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/token_formats/engine.py#L1-L1)
- tests: `tests/unit/test_phase4_core_engines.py:1`, `tests/unit/test_phase4_core_engines.py::TestCore001TokenFormats::test_all_seven_strategies_roundtrip`, `tests/unit/test_phase4_core_engines.py::TestCore001TokenFormats::test_format_engine_auto_selection_and_benchmarks`, `tests/unit/test_phase4_preflight.py:53`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CORE-002 [P2] CORE-002: extend · KGR-G-011, KGR-G-019, G2-IMMUNE-*, MS-19, NFR-SEC-004, GAP-AI · The package packages/eoip/verification/ already exists (behavioral_gate.py, per the Conquest plan). Extend it; do not recreate 

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:75-75` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 7 other site(s): see duplicate task DUP-CORE-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CORE-002` | extend | KGR-G-011, KGR-G-019, G2-IMMUNE-*, MS-19, NFR-SEC-004, GAP-AI | The package packages/eoip/verification/ already exists (behavioral_gate.py, per the Conquest plan). Extend it; do not recreate __init__.py.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CORE-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CORE-002 | extend | KGR-G-011, KGR-G-019, G2-IMMUNE-*, MS-19, NFR-SEC-004, GAP-AI | The package packages/eoip/verification/ already exists (behavioral_gate.py, per the Conquest plan). Extend it; do not recreate __init__.py.»
- [ ] KGR-G-011, KGR-G-019, G2-IMMUNE-*, MS-19, NFR-SEC-004, GAP-AI
- [ ] The package packages/eoip/verification/ already exists (behavioral_gate.py, per the Conquest plan). Extend it; do not recreate __init__.py.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/verification/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/verification/__init__.py#L1-L1), [`packages/eoip/verification/engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/verification/engine.py#L1-L1)
- tests: `tests/unit/test_phase4_core_engines.py:5`, `tests/unit/test_phase4_core_engines.py::TestCore002Verification::test_builtin_rules_and_registry`, `tests/unit/test_phase4_core_engines.py::TestCore002Verification::test_dynamic_guardrail_interceptor`, `tests/unit/test_phase4_preflight.py:53`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CORE-003 [P2] CORE-003: extend · GAP-QUERY, GAP-CACHE-004, query/multi_paradigm_dispatcher.py · Place the router in front of the existing multi-paradigm dispatcher and the unified query API; reuse cost_optimization.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:76-76` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 7 other site(s): see duplicate task DUP-CORE-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CORE-003` | extend | GAP-QUERY, GAP-CACHE-004, query/multi_paradigm_dispatcher.py | Place the router in front of the existing multi-paradigm dispatcher and the unified query API; reuse cost_optimization.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CORE-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CORE-003 | extend | GAP-QUERY, GAP-CACHE-004, query/multi_paradigm_dispatcher.py | Place the router in front of the existing multi-paradigm dispatcher and the unified query API; reuse cost_optimization.»
- [ ] Place the router in front of the existing multi-paradigm dispatcher and the unified query API; reuse cost_optimization.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/routing/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/routing/__init__.py#L1-L1), [`packages/eoip/routing/engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/routing/engine.py#L1-L1)
- tests: `tests/unit/test_phase4_core_engines.py:6`, `tests/unit/test_phase4_core_engines.py::TestCore003IntentRouter::test_router_engine_and_feedback`, `tests/unit/test_phase4_core_engines.py::TestCore003IntentRouter::test_sub10ms_intent_classification`, `tests/unit/test_phase4_preflight.py:53`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CORE-004 [P2] CORE-004: extend · GAP-DUAL, FR-GRAPH-002, FR-GRAPH-005, FR-GRAPH-006, G2-GRAPH-*, KGR-G-013 · Layers formalize logical graph domains, the meta graph and bridge edges. Reuse graph/meta.py and graph/named_graph.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:77-77` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-CORE-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CORE-004` | extend | GAP-DUAL, FR-GRAPH-002, FR-GRAPH-005, FR-GRAPH-006, G2-GRAPH-*, KGR-G-013 | Layers formalize logical graph domains, the meta graph and bridge edges. Reuse graph/meta.py and graph/named_graph.py.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CORE-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CORE-004 | extend | GAP-DUAL, FR-GRAPH-002, FR-GRAPH-005, FR-GRAPH-006, G2-GRAPH-*, KGR-G-013 | Layers formalize logical graph domains, the meta graph and bridge edges. Reuse graph/meta.py and graph/named_graph.py.»
- [ ] GAP-DUAL, FR-GRAPH-002, FR-GRAPH-005, FR-GRAPH-006, G2-GRAPH-*, KGR-G-013
- [ ] Layers formalize logical graph domains, the meta graph and bridge edges. Reuse graph/meta.py and graph/named_graph.py.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph_graph/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph_graph/__init__.py#L1-L1), [`packages/eoip/graph_graph/engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph_graph/engine.py#L1-L1)
- tests: `tests/unit/test_phase4_core_engines.py:7`, `tests/unit/test_phase4_core_engines.py::TestCore004GraphOverGraph::test_cross_layer_and_diff`, `tests/unit/test_phase4_preflight.py:53`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CORE-005 [P2] CORE-005: merge · MS-17, FR-AGENT-002 · Supervisory loops are the loop-level half of MS-17 (A2A + MCP orchestration). Implement once, link from both.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:78-78` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 6 other site(s): see duplicate task DUP-CORE-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CORE-005` | merge | MS-17, FR-AGENT-002 | Supervisory loops are the loop-level half of MS-17 (A2A + MCP orchestration). Implement once, link from both.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CORE-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CORE-005 | merge | MS-17, FR-AGENT-002 | Supervisory loops are the loop-level half of MS-17 (A2A + MCP orchestration). Implement once, link from both.»
- [ ] Supervisory loops are the loop-level half of MS-17 (A2A + MCP orchestration). Implement once, link from both.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/intelligence_eng/engine.py:761`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/intelligence_eng/engine.py#L761-L761)
- tests: `tests/unit/test_phase4_core_engines.py:8`, `tests/unit/test_phase4_core_engines.py::TestCore005LoopOverLoop::test_circuit_breaker_tripping`, `tests/unit/test_phase4_core_engines.py::TestCore005LoopOverLoop::test_supervisory_loop_execution_and_fallback`, `tests/unit/test_phase4_preflight.py:53`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GRAPH-001 [P2] GRAPH-001: merge · GAP-FED, GAP-FABRIC-002..008, federation/planner.py · Same capability as the Conquest GAP-FED deliverable. packages/eoip/federation/ already exists; extend planner.py instead of creating a sec

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:84-84` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 7 other site(s): see duplicate task DUP-GRAPH-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GRAPH-001` | merge | GAP-FED, GAP-FABRIC-002..008, federation/planner.py | Same capability as the Conquest GAP-FED deliverable. packages/eoip/federation/ already exists; extend planner.py instead of creating a second engine.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-GRAPH-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GRAPH-001 | merge | GAP-FED, GAP-FABRIC-002..008, federation/planner.py | Same capability as the Conquest GAP-FED deliverable. packages/eoip/federation/ already exists; extend planner.py instead of creating a second engine.»
- [ ] Same capability as the Conquest GAP-FED deliverable. packages/eoip/federation/ already exists; extend planner.py instead of creating a second engine.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/federation/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/federation/__init__.py#L1-L1), [`packages/eoip/federation/engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/federation/engine.py#L1-L1)
- tests: `tests/unit/test_phase4_phase2_engines.py:6`, `tests/unit/test_phase4_phase2_engines.py::TestGraph001Federation::test_catalog_and_federated_query`, `tests/unit/test_phase4_preflight.py:55`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GRAPH-002 [P2] GRAPH-002: verify · G2-CAUSE-, G2-SIM-, MS-23, UI-01, moonshot/live_causal_engine.py · A live causal engine with blast radius and counterfactual intervention is already built (POST /api/v1/causal/live-blast-radi

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:85-85` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 6 other site(s): see duplicate task DUP-GRAPH-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GRAPH-002` | verify | G2-CAUSE-*, G2-SIM-*, MS-23, UI-01, moonshot/live_causal_engine.py | A live causal engine with blast radius and counterfactual intervention is already built (POST /api/v1/causal/live-blast-radius). Verify, then add do-calculus on top.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-GRAPH-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GRAPH-002 | verify | G2-CAUSE-, G2-SIM-, MS-23, UI-01, moonshot/live_causal_engine.py | A live causal engine with blast radius and counterfactual intervention is already built (POST /api/v1/causal/live-blast-radius). Verify, then add do-calculus on top.»
- [ ] G2-CAUSE-, G2-SIM-, MS-23, UI-01, moonshot/live_causal_engine.py
- [ ] A live causal engine with blast radius and counterfactual intervention is already built (POST /api/v1/causal/live-blast-radius). Verify, then add do-calculus on top.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/causal/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/causal/__init__.py#L1-L1), [`packages/eoip/causal/engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/causal/engine.py#L1-L1)
- tests: `tests/unit/test_phase4_phase2_engines.py:7`, `tests/unit/test_phase4_phase2_engines.py::TestGraph002CausalInference::test_intervention_and_blast_radius`, `tests/unit/test_phase4_preflight.py:55`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GRAPH-003 [P2] GRAPH-003: own · edge/runtime.py · No KGF equivalent.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:86-86` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-GRAPH-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GRAPH-003` | own | edge/runtime.py | No KGF equivalent.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-GRAPH-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GRAPH-003 | own | edge/runtime.py | No KGF equivalent.»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/distillation/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/distillation/__init__.py#L1-L1), [`packages/eoip/distillation/engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/distillation/engine.py#L1-L1)
- tests: `tests/unit/test_phase4_phase2_engines.py:8`, `tests/unit/test_phase4_phase2_engines.py::TestGraph003Distillation::test_distillation_package_and_deploy`, `tests/unit/test_phase4_preflight.py:55`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GRAPH-004 [P2] GRAPH-004: merge · MS-29, MS-18, KGR-G-016 · GNN embeddings and link prediction are the engine under MS-29 (graph foundation model). Build GRAPH-004 first.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:87-87` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-GRAPH-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GRAPH-004` | merge | MS-29, MS-18, KGR-G-016 | GNN embeddings and link prediction are the engine under MS-29 (graph foundation model). Build GRAPH-004 first.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-GRAPH-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GRAPH-004 | merge | MS-29, MS-18, KGR-G-016 | GNN embeddings and link prediction are the engine under MS-29 (graph foundation model). Build GRAPH-004 first.»
- [ ] GNN embeddings and link prediction are the engine under MS-29 (graph foundation model). Build GRAPH-004 first.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gnn/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gnn/__init__.py#L1-L1), [`packages/eoip/gnn/engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gnn/engine.py#L1-L1), [`scripts/update_matrix_caps.py:28`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L28-L28), [`scripts/verify_22_caps.py:162`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L162-L162)
- tests: `tests/unit/test_phase4_phase2_engines.py:9`, `tests/unit/test_phase4_phase2_engines.py::TestGraph004GNNIntegration::test_unqualified_neural_inference_fails_closed`, `tests/unit/test_phase4_preflight.py:55`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GRAPH-005 [P2] GRAPH-005: merge · FR-TEMP-001, FR-GRAPH-009, G2-TIME-, G2-JOURNAL-, G2-ARCH-008, KGR-G-014 · Overlaps the temporal and journal families. Bitemporal module exists in graph/.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:88-88` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-GRAPH-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GRAPH-005` | merge | FR-TEMP-001, FR-GRAPH-009, G2-TIME-*, G2-JOURNAL-*, G2-ARCH-008, KGR-G-014 | Overlaps the temporal and journal families. Bitemporal module exists in graph/.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-GRAPH-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GRAPH-005 | merge | FR-TEMP-001, FR-GRAPH-009, G2-TIME-, G2-JOURNAL-, G2-ARCH-008, KGR-G-014 | Overlaps the temporal and journal families. Bitemporal module exists in graph/.»
- [ ] FR-TEMP-001, FR-GRAPH-009, G2-TIME-, G2-JOURNAL-, G2-ARCH-008, KGR-G-014
- [ ] Overlaps the temporal and journal families. Bitemporal module exists in graph/.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/retrieval/temporal.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/retrieval/temporal.py#L1-L1)
- tests: `tests/unit/test_phase4_phase2_engines.py:10`, `tests/unit/test_phase4_phase2_engines.py::TestGraph005TemporalRetrieval::test_temporal_index_as_of_and_range`, `tests/unit/test_phase4_preflight.py:55`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GRAPH-006 [P2] GRAPH-006: merge · GAP-DUAL, FR-GRAPH-010, KGR-G-015, GAP-GITOPS-004 · SHACL validation and RDF/OWL work already appears three times in the KGF backlog. One implementation.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:89-89` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-GRAPH-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GRAPH-006` | merge | GAP-DUAL, FR-GRAPH-010, KGR-G-015, GAP-GITOPS-004 | SHACL validation and RDF/OWL work already appears three times in the KGF backlog. One implementation.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-GRAPH-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GRAPH-006 | merge | GAP-DUAL, FR-GRAPH-010, KGR-G-015, GAP-GITOPS-004 | SHACL validation and RDF/OWL work already appears three times in the KGF backlog. One implementation.»
- [ ] GAP-DUAL, FR-GRAPH-010, KGR-G-015, GAP-GITOPS-004
- [ ] SHACL validation and RDF/OWL work already appears three times in the KGF backlog. One implementation.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ontology/rdf.py:679`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/rdf.py#L679-L679), [`packages/eoip/ontology/shacl_validator.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/shacl_validator.py#L1-L1)
- tests: `tests/unit/test_phase4_phase2_engines.py:11`, `tests/unit/test_phase4_phase2_engines.py::TestGraph006OWLAndSHACLValidation::test_owl_reasoner`, `tests/unit/test_phase4_phase2_engines.py::TestGraph006OWLAndSHACLValidation::test_shacl_shape_validation`, `tests/unit/test_phase4_preflight.py:55`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-INFRA-001 [P2] INFRA-001: merge · GAP-CACHE-002..005, query/cache.py · GAP-CACHE items (graph-version dependencies, CDC invalidation, staleness policy) are exactly what a distributed cache needs and INFRA-001 omits them.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:97-97` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 6 other site(s): see duplicate task DUP-INFRA-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INFRA-001` | merge | GAP-CACHE-002..005, query/cache.py | GAP-CACHE items (graph-version dependencies, CDC invalidation, staleness policy) are exactly what a distributed cache needs and INFRA-001 omits them.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-INFRA-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INFRA-001 | merge | GAP-CACHE-002..005, query/cache.py | GAP-CACHE items (graph-version dependencies, CDC invalidation, staleness policy) are exactly what a distributed cache needs and INFRA-001 omits them.»
- [ ] GAP-CACHE items (graph-version dependencies, CDC invalidation, staleness policy) are exactly what a distributed cache needs and INFRA-001 omits them.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/enterprise/cache.py:139`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/enterprise/cache.py#L139-L139)
- tests: `tests/unit/test_phase4_phase4_engines.py:4`, `tests/unit/test_phase4_phase4_engines.py::TestInfra001MultiLevelCache::test_invalidation_broadcast_and_warming`, `tests/unit/test_phase4_phase4_engines.py::TestInfra001MultiLevelCache::test_l1_l2_hierarchy_and_promotion`, `tests/unit/test_phase4_preflight.py:57`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-INFRA-003 [P2] INFRA-003: merge · S-03, H-06, REL-* · CI/CD pipeline (S-03) is the same pipeline. One workflow set.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:99-99` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 2, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 6 other site(s): see duplicate task DUP-INFRA-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INFRA-003` | merge | S-03, H-06, REL-* | CI/CD pipeline (S-03) is the same pipeline. One workflow set.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-INFRA-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INFRA-003 | merge | S-03, H-06, REL-* | CI/CD pipeline (S-03) is the same pipeline. One workflow set.»
- [ ] CI/CD pipeline (S-03) is the same pipeline. One workflow set.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_phase4_preflight.py:57`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-INFRA-004 [P2] INFRA-004: merge · NFR-OPS-001, MVP-FR-023, G2-TEL-* · Structured logging and health.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:100-100` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 6 other site(s): see duplicate task DUP-INFRA-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INFRA-004` | merge | NFR-OPS-001, MVP-FR-023, G2-TEL-* | Structured logging and health.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-INFRA-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INFRA-004 | merge | NFR-OPS-001, MVP-FR-023, G2-TEL-* | Structured logging and health.»
- [ ] Structured logging and health.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/observability/logging.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/observability/logging.py#L1-L1)
- tests: `tests/unit/test_phase4_phase4_engines.py:6`, `tests/unit/test_phase4_phase4_engines.py::TestInfra004LogAggregation::test_sampling_filter`, `tests/unit/test_phase4_phase4_engines.py::TestInfra004LogAggregation::test_structured_json_logging_with_correlation`, `tests/unit/test_phase4_preflight.py:57`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-INFRA-005 [P2] INFRA-005: extend · scheduling/executor.py, G2-EKAF-* · Crawl schedules in the acquisition fabric depend on this.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:101-101` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-INFRA-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INFRA-005` | extend | scheduling/executor.py, G2-EKAF-* | Crawl schedules in the acquisition fabric depend on this.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-INFRA-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INFRA-005 | extend | scheduling/executor.py, G2-EKAF-* | Crawl schedules in the acquisition fabric depend on this.»
- [ ] Crawl schedules in the acquisition fabric depend on this.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/scheduling/executor.py:285`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/scheduling/executor.py#L285-L285)
- tests: `tests/unit/test_phase4_phase4_engines.py:7`, `tests/unit/test_phase4_phase4_engines.py::TestInfra005DistributedScheduling::test_distributed_lock_and_task_dag`, `tests/unit/test_phase4_phase4_engines.py::TestInfra005DistributedScheduling::test_leader_election`, `tests/unit/test_phase4_preflight.py:57`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-INFRA-006 [P2] INFRA-006: merge · H-08 · H-08 already plans OpenAPI publication plus Python/TypeScript SDK clients. INFRA-006 adds versioning and a Go SDK.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:102-102` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 6 other site(s): see duplicate task DUP-INFRA-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INFRA-006` | merge | H-08 | H-08 already plans OpenAPI publication plus Python/TypeScript SDK clients. INFRA-006 adds versioning and a Go SDK.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-INFRA-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INFRA-006 | merge | H-08 | H-08 already plans OpenAPI publication plus Python/TypeScript SDK clients. INFRA-006 adds versioning and a Go SDK.»
- [ ] H-08 already plans OpenAPI publication plus Python/TypeScript SDK clients. INFRA-006 adds versioning and a Go SDK.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/sdk/versioning.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/sdk/versioning.py#L1-L1)
- tests: `tests/unit/test_phase4_phase4_engines.py:8`, `tests/unit/test_phase4_phase4_engines.py::TestInfra006APIVersioning::test_api_versioning_and_headers`, `tests/unit/test_phase4_phase4_engines.py::TestInfra006APIVersioning::test_sdk_generation`, `tests/unit/test_phase4_preflight.py:57`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-MULTI-001 [P2] MULTI-001: own · FR-CODE-* · No KGF equivalent.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:121-121` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-MULTI-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`MULTI-001` | own | FR-CODE-* | No KGF equivalent.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-MULTI-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «MULTI-001 | own | FR-CODE-* | No KGF equivalent.»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/fileparse/diagram_parser.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/fileparse/diagram_parser.py#L1-L1)
- tests: `tests/unit/test_phase4_phase6_7_engines.py:7`, `tests/unit/test_phase4_phase6_7_engines.py::TestMulti001DiagramParsingAndRendering::test_graph_to_diagram_renderer`, `tests/unit/test_phase4_phase6_7_engines.py::TestMulti001DiagramParsingAndRendering::test_mermaid_parsing_and_loading`, `tests/unit/test_phase4_preflight.py:61`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-MULTI-002 [P2] MULTI-002: extend · KGR-G-014, MS-19, memory_eng/ · Memory graphs need the poisoning defenses from MS-19.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:122-122` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-MULTI-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`MULTI-002` | extend | KGR-G-014, MS-19, memory_eng/ | Memory graphs need the poisoning defenses from MS-19.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-MULTI-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «MULTI-002 | extend | KGR-G-014, MS-19, memory_eng/ | Memory graphs need the poisoning defenses from MS-19.»
- [ ] Memory graphs need the poisoning defenses from MS-19.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/memory_eng/engine.py:298`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/memory_eng/engine.py#L298-L298)
- tests: `tests/unit/test_phase4_phase6_7_engines.py:8`, `tests/unit/test_phase4_phase6_7_engines.py::TestMulti002MemoryGraph::test_episodic_graph_and_consolidation`, `tests/unit/test_phase4_preflight.py:61`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-TEST-001 [P2] TEST-001: extend · NFR-REL-001, G2-REL-*, REL-10

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:116-116` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-TEST-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`TEST-001` | extend | NFR-REL-001, G2-REL-*, REL-10 | -
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-TEST-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «TEST-001 | extend | NFR-REL-001, G2-REL-*, REL-10 | -»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/chaos/fault_injector.py:1`, `tests/unit/test_phase4_phase6_7_engines.py:6`, `tests/unit/test_phase4_phase6_7_engines.py::TestChaos001FaultInjection::test_chaos_fault_injection_and_recovery`, `tests/unit/test_phase4_preflight.py:60`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-TEST-002 [P2] TEST-002: merge · PERF-01, S-02, NFR-PERF-001, K-04, K-05, REL-12 · Choose one load tool. KGF PERF-01 says Locust/pytest-benchmark; this says k6 or Locust.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:117-117` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-TEST-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`TEST-002` | merge | PERF-01, S-02, NFR-PERF-001, K-04, K-05, REL-12 | Choose one load tool. KGF PERF-01 says Locust/pytest-benchmark; this says k6 or Locust.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-TEST-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «TEST-002 | merge | PERF-01, S-02, NFR-PERF-001, K-04, K-05, REL-12 | Choose one load tool. KGF PERF-01 says Locust/pytest-benchmark; this says k6 or Locust.»
- [ ] PERF-01, S-02, NFR-PERF-001, K-04, K-05, REL-12
- [ ] Choose one load tool. KGF PERF-01 says Locust/pytest-benchmark; this says k6 or Locust.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/load/load_runner.py:1`, `tests/load/locustfile.py:1`, `tests/unit/test_phase4_load.py:1`, `tests/unit/test_phase4_load.py::test_load_test_runner_concurrent_queries`, `tests/unit/test_phase4_preflight.py:60`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-TEST-003 [P2] TEST-003: extend · NFR-SEC-003, query/polyglot_engine.py

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:118-118` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-TEST-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`TEST-003` | extend | NFR-SEC-003, query/polyglot_engine.py | -
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-TEST-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «TEST-003 | extend | NFR-SEC-003, query/polyglot_engine.py | -»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/fuzz/test_property_fuzz.py:1`, `tests/unit/test_phase4_preflight.py:60`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-TEST-004 [P2] TEST-004: merge · S-02, S-03, NFR-PERF-001

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:119-119` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-TEST-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`TEST-004` | merge | S-02, S-03, NFR-PERF-001 | -
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-TEST-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «TEST-004 | merge | S-02, S-03, NFR-PERF-001 | -»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/testing/perf_regression.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/testing/perf_regression.py#L1-L1)
- tests: `tests/unit/test_phase4_perf_regression.py:1`, `tests/unit/test_phase4_perf_regression.py::TestPerfRegressionDetector::test_baseline_save_and_load`, `tests/unit/test_phase4_perf_regression.py::TestPerfRegressionDetector::test_detect_latency_regression`, `tests/unit/test_phase4_perf_regression.py::TestPerfRegressionDetector::test_detect_throughput_drop`, `tests/unit/test_phase4_perf_regression.py::TestPerfRegressionDetector::test_pass_within_thresholds`, `tests/unit/test_phase4_preflight.py:60`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-TEST-005 [P2] TEST-005: own · REL-08 · New capability. REL-08 is a one-time browser run.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:120-120` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-TEST-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`TEST-005` | own | REL-08 | New capability. REL-08 is a one-time browser run.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-TEST-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «TEST-005 | own | REL-08 | New capability. REL-08 is a one-time browser run.»
- [ ] New capability. REL-08 is a one-time browser run.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/testing/a11y_scanner.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/testing/a11y_scanner.py#L1-L1), [`scripts/build_master_suite.py:495`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L495-L495)
- tests: `scripts/test_unified_triage.py:101`, `tests/unit/test_phase4_accessibility.py:1`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_compliant_html_snippet`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_contrast_ratio_calculation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_empty_button_without_aria_label`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_missing_img_alt_violation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_unlabeled_input`, `tests/unit/test_phase4_preflight.py:60`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-UI-001 [P2] UI-001: extend · S-01, CG-GAP-007 · Align with the real stack (Vite + React + JavaScript) before adopting Storybook.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:104-104` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 6 other site(s): see duplicate task DUP-UI-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`UI-001` | extend | S-01, CG-GAP-007 | Align with the real stack (Vite + React + JavaScript) before adopting Storybook.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-UI-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «UI-001 | extend | S-01, CG-GAP-007 | Align with the real stack (Vite + React + JavaScript) before adopting Storybook.»
- [ ] Align with the real stack (Vite + React + JavaScript) before adopting Storybook.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/components/ui/index.jsx:5`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/components/ui/index.jsx#L5-L5), [`apps/web/src/components/ui/tokens.js:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/components/ui/tokens.js#L2-L2)
- tests: `tests/unit/test_phase4_accessibility.py:12`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_compliant_html_snippet`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_contrast_ratio_calculation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_empty_button_without_aria_label`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_missing_img_alt_violation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_unlabeled_input`, `tests/unit/test_phase4_preflight.py:58`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-UI-002 [P2] UI-002: own · No KGF equivalent.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:105-105` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-UI-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`UI-002` | own | - | No KGF equivalent.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-UI-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «UI-002 | own | - | No KGF equivalent.»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_phase4_accessibility.py:13`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_compliant_html_snippet`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_contrast_ratio_calculation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_empty_button_without_aria_label`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_missing_img_alt_violation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_unlabeled_input`, `tests/unit/test_phase4_preflight.py:58`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-UI-003 [P2] UI-003: extend · S-01, G2-UX-GRAPH-*

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:106-106` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-UI-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`UI-003` | extend | S-01, G2-UX-GRAPH-* | -
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-UI-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «UI-003 | extend | S-01, G2-UX-GRAPH-* | -»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/components/ui/index.jsx:222`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/components/ui/index.jsx#L222-L222)
- tests: `tests/unit/test_phase4_accessibility.py:14`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_compliant_html_snippet`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_contrast_ratio_calculation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_empty_button_without_aria_label`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_missing_img_alt_violation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_unlabeled_input`, `tests/unit/test_phase4_preflight.py:58`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-UI-004 [P2] UI-004: extend · S-01

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:107-107` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-UI-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`UI-004` | extend | S-01 | -
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-UI-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «UI-004 | extend | S-01 | -»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_phase4_accessibility.py:15`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_compliant_html_snippet`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_contrast_ratio_calculation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_empty_button_without_aria_label`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_missing_img_alt_violation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_unlabeled_input`, `tests/unit/test_phase4_preflight.py:58`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-UI-005 [P2] UI-005: extend · FR-UI-001, /api/v1/reports/export · Server-side report export routes already exist.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:108-108` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-UI-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`UI-005` | extend | FR-UI-001, /api/v1/reports/export | Server-side report export routes already exist.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-UI-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «UI-005 | extend | FR-UI-001, /api/v1/reports/export | Server-side report export routes already exist.»
- [ ] Server-side report export routes already exist.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_phase4_accessibility.py:16`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_compliant_html_snippet`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_contrast_ratio_calculation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_empty_button_without_aria_label`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_missing_img_alt_violation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_unlabeled_input`, `tests/unit/test_phase4_preflight.py:58`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-UI-006 [P2] UI-006: extend · GAP-NOCODE, GAP-APP · Avoid a third builder: decide whether this is the pipeline-level editor and GAP-NOCODE/GAP-APP are ontology/dashboard editors.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:109-109` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-UI-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`UI-006` | extend | GAP-NOCODE, GAP-APP | Avoid a third builder: decide whether this is the pipeline-level editor and GAP-NOCODE/GAP-APP are ontology/dashboard editors.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-UI-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «UI-006 | extend | GAP-NOCODE, GAP-APP | Avoid a third builder: decide whether this is the pipeline-level editor and GAP-NOCODE/GAP-APP are ontology/dashboard editors.»
- [ ] Avoid a third builder: decide whether this is the pipeline-level editor and GAP-NOCODE/GAP-APP are ontology/dashboard editors.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_phase4_accessibility.py:17`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_compliant_html_snippet`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_contrast_ratio_calculation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_empty_button_without_aria_label`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_missing_img_alt_violation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_unlabeled_input`, `tests/unit/test_phase4_preflight.py:58`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-UI-007 [P2] UI-007: merge · G2-UX-LENS-, UI-01..UI-04 (KGF), G2-TIME-, G2-SIM-, G2-PM- · KGF already lists blast-radius, multi-paradigm, domain-pack and XAI screens. Share the lens shell.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:110-110` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-UI-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`UI-007` | merge | G2-UX-LENS-*, UI-01..UI-04 (KGF), G2-TIME-*, G2-SIM-*, G2-PM-* | KGF already lists blast-radius, multi-paradigm, domain-pack and XAI screens. Share the lens shell.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-UI-007

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «UI-007 | merge | G2-UX-LENS-, UI-01..UI-04 (KGF), G2-TIME-, G2-SIM-, G2-PM- | KGF already lists blast-radius, multi-paradigm, domain-pack and XAI screens. Share the lens shell.»
- [ ] G2-UX-LENS-, UI-01..UI-04 (KGF), G2-TIME-, G2-SIM-, G2-PM-
- [ ] KGF already lists blast-radius, multi-paradigm, domain-pack and XAI screens. Share the lens shell.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/dashboards/EngineDashboardsHub.jsx:20`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/dashboards/EngineDashboardsHub.jsx#L20-L20)
- tests: `tests/unit/test_phase4_accessibility.py:18`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_compliant_html_snippet`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_contrast_ratio_calculation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_empty_button_without_aria_label`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_missing_img_alt_violation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_unlabeled_input`, `tests/unit/test_phase4_preflight.py:58`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-UI-008 [P2] UI-008: own · GAP-QI-*

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:111-111` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-UI-008; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`UI-008` | own | GAP-QI-* | -
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-UI-008

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «UI-008 | own | GAP-QI-* | -»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/dashboards/EngineDashboardsHub.jsx:26`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/dashboards/EngineDashboardsHub.jsx#L26-L26), [`packages/eoip/search/analytics.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/search/analytics.py#L1-L1)
- tests: `tests/unit/test_phase4_compliance_and_search.py:1`, `tests/unit/test_phase4_compliance_and_search.py::TestSearchAnalyticsEngine::test_relevance_tuning_synonyms_and_boosts`, `tests/unit/test_phase4_compliance_and_search.py::TestSearchAnalyticsEngine::test_search_event_logging_and_summary`, `tests/unit/test_phase4_preflight.py:58`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-UI-009 [P2] UI-009: merge · MS-12 · Real-time collaboration is MS-12 (live collaborative graph studio). One CRDT layer.

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:112-112` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 5 other site(s): see duplicate task DUP-UI-009; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`UI-009` | merge | MS-12 | Real-time collaboration is MS-12 (live collaborative graph studio). One CRDT layer.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-UI-009

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «UI-009 | merge | MS-12 | Real-time collaboration is MS-12 (live collaborative graph studio). One CRDT layer.»
- [ ] Real-time collaboration is MS-12 (live collaborative graph studio). One CRDT layer.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_phase4_accessibility.py:19`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_compliant_html_snippet`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_contrast_ratio_calculation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_empty_button_without_aria_label`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_missing_img_alt_violation`, `tests/unit/test_phase4_accessibility.py::TestAccessibilityScanner::test_unlabeled_input`, `tests/unit/test_phase4_preflight.py:58`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

