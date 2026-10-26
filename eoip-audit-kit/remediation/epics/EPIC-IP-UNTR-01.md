# EPIC-IP-UNTR-01: EOIP-engg-doc-pkg/ip-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 60 tasks, ~390.0 h, priorities {'P0': 6, 'P1': 54}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-REQ-BRB-002 [P0] REQ-BRB-002: POST /actions/authorize (request: action, warrantid, agentid, planid?) returns {decision, kappa, budgetbefore, budgetafter?, impactrunid, escalationid?}. Budget debit and decision are atomic (no doubl

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:659-659` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-BRB-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-BRB-002 | `POST /actions/authorize` (request: `action`, `warrant_id`, `agent_id`, `plan_id?`) returns `{decision, kappa, budget_before, budget_after?, impact_run_id, escalation_id?}`. Budget debit and decision are atomic (no double spend under concurrency; test with 100 concurrent requests).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-BRB-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-BRB-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-BRB-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-BRB-002 | POST /actions/authorize (request: action, warrant_id, agent_id, plan_id?) returns {decision, kappa, budget_before, budget_after?, impact_run_id, escalation_id?}. Budget debit and decision are atomic (no double spend under concurrency; test with 100 concurrent requests).»
- [ ] POST /actions/authorize (request: action, warrant_id, agent_id, plan_id?) returns {decision, kappa, budget_before, budget_after?, impact_run_id, escalation_id?}. Budget debit and decision are atomic (no double spend under concurrency; test with 100 concurrent requests).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CMT-004 [P0] REQ-CMT-004: Authority: the promisor's authority scopes (A1) MUST include action commit:<kind> on the ontology types of every about entity. Otherwise the commitment is rejected with CMTUNAUTHORIZED and an escalati

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1337-1337` (table_row) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CMT-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CMT-004 | Authority: the promisor's authority scopes (A1) MUST include action `commit:<kind>` on the ontology types of every `about` entity. Otherwise the commitment is rejected with `CMT_UNAUTHORIZED` and an escalation is created for a principal who holds that scope.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CMT-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CMT-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CMT-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CMT-004 | Authority: the promisor's authority scopes (A1) MUST include action commit:<kind> on the ontology types of every about entity. Otherwise the commitment is rejected with CMT_UNAUTHORIZED and an escalation is created for a principal who holds that scope.»
- [ ] Authority: the promisor's authority scopes (A1) MUST include action commit:<kind> on the ontology types of every about entity. Otherwise the commitment is rejected with CMT_UNAUTHORIZED and an escalation is created for a principal who holds that scope.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-EXP-001 [P0] REQ-EXP-001: Each tenant has an Ed25519 signing key pair stored in KGF's secret store; rotation supported; public keys published at GET /warrants/keys

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:513-513` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-EXP-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-EXP-001 | Each tenant has an Ed25519 signing key pair stored in KGF's secret store; rotation supported; public keys published at `GET /warrants/keys`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-EXP-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-EXP-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-EXP-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-EXP-001 | Each tenant has an Ed25519 signing key pair stored in KGF's secret store; rotation supported; public keys published at GET /warrants/keys.»
- [ ] Each tenant has an Ed25519 signing key pair stored in KGF's secret store; rotation supported; public keys published at GET /warrants/keys.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV5-005 [P0] REQ-INV5-005: Thresholds, weights and the trained encoder are trade secrets (REQ-IPH-003)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:872-872` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV5-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV5-005 | Thresholds, weights and the trained encoder are trade secrets (REQ-IPH-003).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV5-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV5-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV5-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV5-005 | Thresholds, weights and the trained encoder are trade secrets (REQ-IPH-003).»
- [ ] Thresholds, weights and the trained encoder are trade secrets (REQ-IPH-003).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-IPH-003 [P0] REQ-IPH-003: Trade-secret material for Inventions 5, 6 and 9, and all tuned thresholds and trained weights for every invention, MUST NOT be committed to the source repository. Store them in the model registry (§14

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:161-161` (table_row) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-IPH-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-IPH-003 | Trade-secret material for Inventions 5, 6 and 9, and all tuned thresholds and trained weights for every invention, MUST NOT be committed to the source repository. Store them in the model registry (§14.0.4) with encryption at rest, and load them by reference. Repository files contain only default values from this document.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-IPH-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-IPH-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-IPH-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-IPH-003 | Trade-secret material for Inventions 5, 6 and 9, and all tuned thresholds and trained weights for every invention, MUST NOT be committed to the source repository. Store them in the model registry (§14.0.4) with encryption at rest, and load them by reference. Repository files contain only default values from this document.»
- [ ] Trade-secret material for Inventions 5, 6 and 9, and all tuned thresholds and trained weights for every invention, MUST NOT be committed to the source repository. Store them in the model registry (§14.0.4) with encryption at rest, and load them by reference. Repository files contain only default values from this document.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PLT-007 [P0] REQ-PLT-007: Every API MUST enforce KGF's existing authentication and RBAC. New permissions are listed in §19.3

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:148-148` (table_row) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PLT-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PLT-007 | Every API MUST enforce KGF's existing authentication and RBAC. New permissions are listed in §19.3.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PLT-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PLT-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PLT-007

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PLT-007 | Every API MUST enforce KGF's existing authentication and RBAC. New permissions are listed in §19.3.»
- [ ] Every API MUST enforce KGF's existing authentication and RBAC. New permissions are listed in §19.3.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-BRB-004 [P1] REQ-BRB-004: GET /budgets, PUT /budgets/{agentclassorid} (permission ip.budget.admin), budget history per agent

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:661-661` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-BRB-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-BRB-004 | `GET /budgets`, `PUT /budgets/{agent_class_or_id}` (permission `ip.budget.admin`), budget history per agent.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-BRB-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-BRB-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-BRB-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-BRB-004 | GET /budgets, PUT /budgets/{agent_class_or_id} (permission ip.budget.admin), budget history per agent.»
- [ ] GET /budgets, PUT /budgets/{agent_class_or_id} (permission ip.budget.admin), budget history per agent.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CHK-001 [P1] REQ-CHK-001: The table above MUST be tenant configuration warrant.minstatusbyactionclass. Changing it requires ip.policy.admin

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:464-464` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CHK-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CHK-001 | The table above MUST be tenant configuration `warrant.min_status_by_action_class`. Changing it requires `ip.policy.admin`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CHK-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CHK-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CHK-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CHK-001 | The table above MUST be tenant configuration warrant.min_status_by_action_class. Changing it requires ip.policy.admin.»
- [ ] The table above MUST be tenant configuration warrant.min_status_by_action_class. Changing it requires ip.policy.admin.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CHK-002 [P1] REQ-CHK-002: Every tool/operator that performs an action MUST declare its action class in the registry. Undeclared → treated as IRREVERSIBLE

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:465-465` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CHK-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CHK-002 | Every tool/operator that performs an action MUST declare its action class in the registry. Undeclared → treated as `IRREVERSIBLE`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CHK-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CHK-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CHK-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CHK-002 | Every tool/operator that performs an action MUST declare its action class in the registry. Undeclared → treated as IRREVERSIBLE.»
- [ ] Every tool/operator that performs an action MUST declare its action class in the registry. Undeclared → treated as IRREVERSIBLE.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CHK-006 [P1] REQ-CHK-006: Every answer produced by KGF (NL answers, reports, exports) MUST carry an answer warrant whose grounds list every proposition warrant used, and the UI shows the warrant (§18.2)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:483-483` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CHK-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CHK-006 | Every answer produced by KGF (NL answers, reports, exports) MUST carry an answer warrant whose grounds list every proposition warrant used, and the UI shows the warrant (§18.2).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CHK-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CHK-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CHK-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CHK-006 | Every answer produced by KGF (NL answers, reports, exports) MUST carry an answer warrant whose grounds list every proposition warrant used, and the UI shows the warrant (§18.2).»
- [ ] Every answer produced by KGF (NL answers, reports, exports) MUST carry an answer warrant whose grounds list every proposition warrant used, and the UI shows the warrant (§18.2).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CMT-014 [P1] REQ-CMT-014: Demonstration scenario: agent-std-1 tells bob "I will rotate the svc-payments credentials by tomorrow 18:00" → PROPOSED commitment with the source span, confirmed → ACTIVE. agent-elev-1 plans to delet

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1347-1347` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CMT-014; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CMT-014 | Demonstration scenario: `agent-std-1` tells `bob` "I will rotate the svc-payments credentials by tomorrow 18:00" → `PROPOSED` commitment with the source span, confirmed → `ACTIVE`. `agent-elev-1` plans to delete svc-payments without referencing the commitment → `CMT_CONFLICT`. `agent-std-1` reports "done" in text → fulfilment refused. A credential-rotation tool receipt (`OBSERVED`) is submitted → `FULFILLED`. A second commitment by `agent-std-1` exists when the agent is retired → refused without successor, then transferred to `agent-elev-1`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CMT-014' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CMT-014') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CMT-014

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CMT-014 | Demonstration scenario: agent-std-1 tells bob "I will rotate the svc-payments credentials by tomorrow 18:00" → PROPOSED commitment with the source span, confirmed → ACTIVE. agent-elev-1 plans to delete svc-payments without referencing the commitment → CMT_CONFLICT. agent-std-1 reports "done" in text → fulfilment refused. A credential-rotation tool receipt (OBSERVE»
- [ ] Demonstration scenario: agent-std-1 tells bob "I will rotate the svc-payments credentials by tomorrow 18:00" → PROPOSED commitment with the source span, confirmed → ACTIVE. agent-elev-1 plans to delete svc-payments without referencing the commitment → CMT_CONFLICT. agent-std-1 reports "done" in text → fulfilment refused. A credential-rotation tool receipt (OBSERVED) is submitted → FULFILLED. A sec
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DCG-002 [P1] REQ-DCG-002: GET/POST/PUT/DELETE /protected-facts with permission ip.protected.admin; every change audited

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:674-674` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DCG-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DCG-002 | `GET/POST/PUT/DELETE /protected-facts` with permission `ip.protected.admin`; every change audited.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DCG-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DCG-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DCG-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DCG-002 | GET/POST/PUT/DELETE /protected-facts with permission ip.protected.admin; every change audited.»
- [ ] GET/POST/PUT/DELETE /protected-facts with permission ip.protected.admin; every change audited.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DCG-010 [P1] REQ-DCG-010: derivation-guard MUST implement A5 and be invoked at the retrieval checkpoint for all agent and LLM reads, and for user-facing NL answers. Direct UI graph browsing by humans MAY bypass it when dcg.app

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:698-698` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DCG-010; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DCG-010 | `derivation-guard` MUST implement A5 and be invoked at the `retrieval` checkpoint for all agent and LLM reads, and for user-facing NL answers. Direct UI graph browsing by humans MAY bypass it when `dcg.apply_to_human_browse=false` (default true).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DCG-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DCG-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DCG-010

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DCG-010 | derivation-guard MUST implement A5 and be invoked at the retrieval checkpoint for all agent and LLM reads, and for user-facing NL answers. Direct UI graph browsing by humans MAY bypass it when dcg.apply_to_human_browse=false (default true).»
- [ ] derivation-guard MUST implement A5 and be invoked at the retrieval checkpoint for all agent and LLM reads, and for user-facing NL answers. Direct UI graph browsing by humans MAY bypass it when dcg.apply_to_human_browse=false (default true).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DCG-013 [P1] REQ-DCG-013: Benchmark evals/dcg/inference-leak-v1 MUST contain ≥ 50 constructed scenarios where a protected fact is derivable from 2–4 individually permitted facts, and ≥ 50 benign scenarios. Acceptance: 100% of 

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:701-701` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DCG-013; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DCG-013 | Benchmark `evals/dcg/inference-leak-v1` MUST contain ≥ 50 constructed scenarios where a protected fact is derivable from 2–4 individually permitted facts, and ≥ 50 benign scenarios. Acceptance: 100% of leak scenarios blocked within depth 3; ≤ 5% false blocks on benign scenarios.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DCG-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DCG-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DCG-013

**Acceptance criteria**
- [ ] 100% of leak scenarios blocked within depth 3; ≤ 5% false blocks on benign scenarios
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DIS-001 [P1] REQ-DIS-001: SDK deliberate(question, options, participants, actionclass, maxrounds?) and POST /deliberations run the protocol: round 0, each participant produces a position in isolation; rounds 1..dissent.maxroun

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1382-1382` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DIS-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DIS-001 | SDK `deliberate(question, options, participants, action_class, max_rounds?)` and `POST /deliberations` run the protocol: round 0, each participant produces a position in isolation; rounds 1..`dissent.max_rounds`, participants see all previous positions and may revise. Positions are produced through the checkpoint SDK, so every rationale proposition carries a warrant (SASI applies).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DIS-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DIS-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DIS-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DIS-001 | SDK deliberate(question, options, participants, action_class, max_rounds?) and POST /deliberations run the protocol: round 0, each participant produces a position in isolation; rounds 1..dissent.max_rounds, participants see all previous positions and may revise. Positions are produced through the checkpoint SDK, so every rationale proposition carries a warrant (SA»
- [ ] SDK deliberate(question, options, participants, action_class, max_rounds?) and POST /deliberations run the protocol: round 0, each participant produces a position in isolation; rounds 1..dissent.max_rounds, participants see all previous positions and may revise. Positions are produced through the checkpoint SDK, so every rationale proposition carries a warrant (SASI applies).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DIS-002 [P1] REQ-DIS-002: Isolation: in round 0 the runtime MUST NOT include any other participant's position, rationale or the deliberation's later state in a participant's context; the position records seenpositionids = [] a

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1383-1383` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DIS-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DIS-002 | Isolation: in round 0 the runtime MUST NOT include any other participant's position, rationale or the deliberation's later state in a participant's context; the position records `seen_position_ids = []` and `isolated = true`. A detected breach (any other position id or its text hash present in the context sent to the model) voids the position with `DIS_ISOLATION_BREACH`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DIS-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DIS-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DIS-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DIS-002 | Isolation: in round 0 the runtime MUST NOT include any other participant's position, rationale or the deliberation's later state in a participant's context; the position records seen_position_ids = [] and isolated = true. A detected breach (any other position id or its text hash present in the context sent to the model) voids the position with DIS_ISOLATION_BREACH»
- [ ] Isolation: in round 0 the runtime MUST NOT include any other participant's position, rationale or the deliberation's later state in a participant's context; the position records seen_position_ids = [] and isolated = true. A detected breach (any other position id or its text hash present in the context sent to the model) voids the position with DIS_ISOLATION_BREACH.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DSC-001 [P1] REQ-DSC-001: discipline-registry MUST serve the table above from GET /disciplines (id, name, definition, requirement groups, metric names with current values, process ids with last run date, screen routes). Defini

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1287-1287` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DSC-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DSC-001 | `discipline-registry` MUST serve the table above from `GET /disciplines` (id, name, definition, requirement groups, metric names with current values, process ids with last run date, screen routes). Definitions are stored as configuration so the owner can update the wording without a code change.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DSC-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DSC-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DSC-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DSC-001 | discipline-registry MUST serve the table above from GET /disciplines (id, name, definition, requirement groups, metric names with current values, process ids with last run date, screen routes). Definitions are stored as configuration so the owner can update the wording without a code change.»
- [ ] discipline-registry MUST serve the table above from GET /disciplines (id, name, definition, requirement groups, metric names with current values, process ids with last run date, screen routes). Definitions are stored as configuration so the owner can update the wording without a code change.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DSC-003 [P1] REQ-DSC-003: Warrant Engineering maturity MUST be computed per tenant from live data over the trailing disciplines.maturitywindowdays, using exactly these criteria (a level requires all criteria of that level and 

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1289-1289` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DSC-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DSC-003 | Warrant Engineering maturity MUST be computed per tenant from live data over the trailing `disciplines.maturity_window_days`, using exactly these criteria (a level requires all criteria of that level and every level below): **L1 Labelled** — ≥ 99% of stored assertions have a warrant and ≥ 99% of answers carry an answer warrant. **L2 Enforced at commit** — `ip.warrant.enabled`, minimum-status checks active for `EXTERNAL_WRITE` and `IRREVERSIBLE`, and zero commits of those classes executed without a checkpoint evaluation in the window. **L3 End to end** — all six checkpoints evaluated at least once per day on ≥ 90% of days; `ip.lease.enabled`, `ip.budget.enabled`, `ip.dcg.enabled`, `ip.sasi.enabled` on; warrant coverage ≥ 0.99. **L4 Self-measuring** — every process REQ-PRC-001..009 that applies to enabled features ran on schedule with sign-off in the window, and `ip.export.enabled` with at least one verified export. Level 0 otherwise.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DSC-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DSC-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DSC-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DSC-003 | Warrant Engineering maturity MUST be computed per tenant from live data over the trailing disciplines.maturity_window_days, using exactly these criteria (a level requires all criteria of that level and every level below): L1 Labelled — ≥ 99% of stored assertions have a warrant and ≥ 99% of answers carry an answer warrant. L2 Enforced at commit — ip.warrant.enabled»
- [ ] Warrant Engineering maturity MUST be computed per tenant from live data over the trailing disciplines.maturity_window_days, using exactly these criteria (a level requires all criteria of that level and every level below): L1 Labelled — ≥ 99% of stored assertions have a warrant and ≥ 99% of answers carry an answer warrant. L2 Enforced at commit — ip.warrant.enabled, minimum-status checks active for
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-EXP-002 [P1] REQ-EXP-002: POST /warrants/{id}/export returns a bundle: the answer or action, its warrant, the full lineage DAG, the graph snapshot version, model versions, data classes touched, the requesting principal's permi

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:514-514` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-EXP-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-EXP-002 | `POST /warrants/{id}/export` returns a bundle: the answer or action, its warrant, the full lineage DAG, the graph snapshot version, model versions, data classes touched, the requesting principal's permissions at the time, and an Ed25519 signature over the RFC 8785 canonical bundle. Formats: JSON, and PDF with the bundle embedded as an attachment and a visible footer showing bundle id and verification URL path.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-EXP-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-EXP-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-EXP-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-EXP-002 | POST /warrants/{id}/export returns a bundle: the answer or action, its warrant, the full lineage DAG, the graph snapshot version, model versions, data classes touched, the requesting principal's permissions at the time, and an Ed25519 signature over the RFC 8785 canonical bundle. Formats: JSON, and PDF with the bundle embedded as an attachment and a visible footer»
- [ ] POST /warrants/{id}/export returns a bundle: the answer or action, its warrant, the full lineage DAG, the graph snapshot version, model versions, data classes touched, the requesting principal's permissions at the time, and an Ed25519 signature over the RFC 8785 canonical bundle. Formats: JSON, and PDF with the bundle embedded as an attachment and a visible footer showing bundle id and verificatio
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-EXP-003 [P1] REQ-EXP-003: POST /warrants/verify accepts a bundle, verifies the signature, and optionally replays: re-runs the recorded queries against the recorded as-of snapshot (REQ-WAR-023) and reports MATCH, MISMATCH (with

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:515-515` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-EXP-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-EXP-003 | `POST /warrants/verify` accepts a bundle, verifies the signature, and optionally replays: re-runs the recorded queries against the recorded `as-of` snapshot (REQ-WAR-023) and reports `MATCH`, `MISMATCH` (with diff) or `NOT_REPLAYABLE` (with reason).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-EXP-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-EXP-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-EXP-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-EXP-003 | POST /warrants/verify accepts a bundle, verifies the signature, and optionally replays: re-runs the recorded queries against the recorded as-of snapshot (REQ-WAR-023) and reports MATCH, MISMATCH (with diff) or NOT_REPLAYABLE (with reason).»
- [ ] POST /warrants/verify accepts a bundle, verifies the signature, and optionally replays: re-runs the recorded queries against the recorded as-of snapshot (REQ-WAR-023) and reports MATCH, MISMATCH (with diff) or NOT_REPLAYABLE (with reason).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-HLF-001 [P1] REQ-HLF-001: halflife-service MUST implement A7, refit nightly (halflife.refitcron, default 0 2 tenant local time), and store (tenantid, type, property?, model, params, hdays, nevents, fittedat) history

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:598-598` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-HLF-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-HLF-001 | `halflife-service` MUST implement A7, refit nightly (`halflife.refit_cron`, default `0 2 * * *` tenant local time), and store `(tenant_id, type, property?, model, params, h_days, n_events, fitted_at)` history.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-HLF-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-HLF-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-HLF-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-HLF-001 | halflife-service MUST implement A7, refit nightly (halflife.refit_cron, default 0 2 * tenant local time), and store (tenant_id, type, property?, model, params, h_days, n_events, fitted_at) history.»
- [ ] halflife-service MUST implement A7, refit nightly (halflife.refit_cron, default 0 2 * tenant local time), and store (tenant_id, type, property?, model, params, h_days, n_events, fitted_at) history.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-HLF-003 [P1] REQ-HLF-003: GET /half-lives lists current values with sample sizes and fit model; POST /half-lives/refit triggers a refit (permission ip.halflife.admin)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:600-600` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-HLF-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-HLF-003 | `GET /half-lives` lists current values with sample sizes and fit model; `POST /half-lives/refit` triggers a refit (permission `ip.halflife.admin`).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-HLF-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-HLF-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-HLF-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-HLF-003 | GET /half-lives lists current values with sample sizes and fit model; POST /half-lives/refit triggers a refit (permission ip.halflife.admin).»
- [ ] GET /half-lives lists current values with sample sizes and fit model; POST /half-lives/refit triggers a refit (permission ip.halflife.admin).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-HLF-004 [P1] REQ-HLF-004: Unit tests with synthetic exponential and Weibull data MUST recover the true half-life within 10% at n = 500. On the seeded demo tenant, fitted half-lives MUST be within 15% of the planted values for 

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:601-601` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-HLF-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-HLF-004 | Unit tests with synthetic exponential and Weibull data MUST recover the true half-life within 10% at n = 500. On the seeded demo tenant, fitted half-lives MUST be within 15% of the planted values for every type with ≥ 100 change events.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-HLF-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-HLF-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-HLF-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-HLF-004 | Unit tests with synthetic exponential and Weibull data MUST recover the true half-life within 10% at n = 500. On the seeded demo tenant, fitted half-lives MUST be within 15% of the planted values for every type with ≥ 100 change events.»
- [ ] Unit tests with synthetic exponential and Weibull data MUST recover the true half-life within 10% at n = 500. On the seeded demo tenant, fitted half-lives MUST be within 15% of the planted values for every type with ≥ 100 change events.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-IMP-001 [P1] REQ-IMP-001: impact-engine MUST implement the propagation exactly as specified, in prior mode from day one and in learned mode once a model passes its gate (REQ-IMP-004)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:633-633` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-IMP-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-IMP-001 | `impact-engine` MUST implement the propagation exactly as specified, in prior mode from day one and in learned mode once a model passes its gate (REQ-IMP-004).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-IMP-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-IMP-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-IMP-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-IMP-001 | impact-engine MUST implement the propagation exactly as specified, in prior mode from day one and in learned mode once a model passes its gate (REQ-IMP-004).»
- [ ] impact-engine MUST implement the propagation exactly as specified, in prior mode from day one and in learned mode once a model passes its gate (REQ-IMP-004).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-IMP-006 [P1] REQ-IMP-006: Blast barriers and tenant boundaries are absolute: a test MUST prove zero probability mass crosses them

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:638-638` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-IMP-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-IMP-006 | Blast barriers and tenant boundaries are absolute: a test MUST prove zero probability mass crosses them.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-IMP-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-IMP-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-IMP-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-IMP-006 | Blast barriers and tenant boundaries are absolute: a test MUST prove zero probability mass crosses them.»
- [ ] Blast barriers and tenant boundaries are absolute: a test MUST prove zero probability mass crosses them.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV11-001 [P1] REQ-INV11-001: Candidates: within each type, blocking by normalized name/key tokens and by approximate nearest neighbours in embedding space; pairs with cosine ≥ τT (dedup.tau per type, default 0.92)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:922-922` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV11-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV11-001 | Candidates: within each type, blocking by normalized name/key tokens and by approximate nearest neighbours in embedding space; pairs with cosine ≥ τ_T (`dedup.tau` per type, default 0.92).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV11-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV11-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV11-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV11-001 | Candidates: within each type, blocking by normalized name/key tokens and by approximate nearest neighbours in embedding space; pairs with cosine ≥ τ_T (dedup.tau per type, default 0.92).»
- [ ] Candidates: within each type, blocking by normalized name/key tokens and by approximate nearest neighbours in embedding space; pairs with cosine ≥ τ_T (dedup.tau per type, default 0.92).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV6-003 [P1] REQ-INV6-003: Differential privacy with DP-SGD per data class: per-class ε budgets (defaults public: 8, internal: 4, confidential: 1, δ = 1e-5) tracked with a privacy accountant; a tenant stops contributing a class

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:881-881` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV6-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV6-003 | Differential privacy with DP-SGD per data class: per-class ε budgets (defaults `public: 8`, `internal: 4`, `confidential: 1`, δ = 1e-5) tracked with a privacy accountant; a tenant stops contributing a class once its budget is exhausted for the period (`federation.period`, default 90 days).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV6-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV6-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV6-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV6-003 | Differential privacy with DP-SGD per data class: per-class ε budgets (defaults public: 8, internal: 4, confidential: 1, δ = 1e-5) tracked with a privacy accountant; a tenant stops contributing a class once its budget is exhausted for the period (federation.period, default 90 days).»
- [ ] Differential privacy with DP-SGD per data class: per-class ε budgets (defaults public: 8, internal: 4, confidential: 1, δ = 1e-5) tracked with a privacy accountant; a tenant stops contributing a class once its budget is exhausted for the period (federation.period, default 90 days).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-IPH-001 [P1] REQ-IPH-001: Configuration key ip.publicreleaseallowed (platform-level, default false). While false, CI MUST fail any job that publishes packages to a public registry, pushes to a remote whose visibility is public

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:159-159` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-IPH-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-IPH-001 | Configuration key `ip.public_release_allowed` (platform-level, default `false`). While `false`, CI MUST fail any job that publishes packages to a public registry, pushes to a remote whose visibility is public, or deploys public documentation that contains files under the IP module paths (§4.3).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-IPH-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-IPH-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-IPH-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-IPH-001 | Configuration key ip.public_release_allowed (platform-level, default false). While false, CI MUST fail any job that publishes packages to a public registry, pushes to a remote whose visibility is public, or deploys public documentation that contains files under the IP module paths (§4.3).»
- [ ] Configuration key ip.public_release_allowed (platform-level, default false). While false, CI MUST fail any job that publishes packages to a public registry, pushes to a remote whose visibility is public, or deploys public documentation that contains files under the IP module paths (§4.3).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-IPH-002 [P1] REQ-IPH-002: Source files implementing Inventions 1–20 MUST carry the repository's existing licence header. If the repository has no licence header convention, add Proprietary and confidential. All rights reserved

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:160-160` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-IPH-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-IPH-002 | Source files implementing Inventions 1–20 MUST carry the repository's existing licence header. If the repository has no licence header convention, add `Proprietary and confidential. All rights reserved by the rights holder named in LICENSE.` and record a DR.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-IPH-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-IPH-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-IPH-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-IPH-002 | Source files implementing Inventions 1–20 MUST carry the repository's existing licence header. If the repository has no licence header convention, add Proprietary and confidential. All rights reserved by the rights holder named in LICENSE. and record a DR.»
- [ ] Source files implementing Inventions 1–20 MUST carry the repository's existing licence header. If the repository has no licence header convention, add Proprietary and confidential. All rights reserved by the rights holder named in LICENSE. and record a DR.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-IPH-004 [P1] REQ-IPH-004: Code comments, READMEs and API descriptions MUST describe behaviour, not claim novelty. Do not write "patented", "patent pending" or "novel" anywhere until the owner sets ip.publicreleaseallowed=true

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:162-162` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-IPH-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-IPH-004 | Code comments, READMEs and API descriptions MUST describe behaviour, not claim novelty. Do not write "patented", "patent pending" or "novel" anywhere until the owner sets `ip.public_release_allowed=true`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-IPH-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-IPH-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-IPH-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-IPH-004 | Code comments, READMEs and API descriptions MUST describe behaviour, not claim novelty. Do not write "patented", "patent pending" or "novel" anywhere until the owner sets ip.public_release_allowed=true.»
- [ ] Code comments, READMEs and API descriptions MUST describe behaviour, not claim novelty. Do not write "patented", "patent pending" or "novel" anywhere until the owner sets ip.public_release_allowed=true.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-IPH-005 [P1] REQ-IPH-005: Each invention module MUST include an INVENTION.md file (internal, not published) listing: invention number, requirement IDs implemented, algorithm IDs, the date the first working version produced an 

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:163-163` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-IPH-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-IPH-005 | Each invention module MUST include an `INVENTION.md` file (internal, not published) listing: invention number, requirement IDs implemented, algorithm IDs, the date the first working version produced an Evidence Pack, and the name of the person who directed the work. This supports the owner's dated invention records.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-IPH-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-IPH-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-IPH-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-IPH-005 | Each invention module MUST include an INVENTION.md file (internal, not published) listing: invention number, requirement IDs implemented, algorithm IDs, the date the first working version produced an Evidence Pack, and the name of the person who directed the work. This supports the owner's dated invention records.»
- [ ] Each invention module MUST include an INVENTION.md file (internal, not published) listing: invention number, requirement IDs implemented, algorithm IDs, the date the first working version produced an Evidence Pack, and the name of the person who directed the work. This supports the owner's dated invention records.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-LSE-001 [P1] REQ-LSE-001: KGF MUST publish kgf.graph.changed events for every committed assertion create/update/delete: {tenantid, assertionid, subjectid, changekind, oldversion, newversion, recordedat, warrantid}

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:526-526` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-LSE-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-LSE-001 | KGF MUST publish `kgf.graph.changed` events for every committed assertion create/update/delete: `{tenant_id, assertion_id, subject_id, change_kind, old_version, new_version, recorded_at, warrant_id}`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-LSE-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-LSE-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-LSE-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-LSE-001 | KGF MUST publish kgf.graph.changed events for every committed assertion create/update/delete: {tenant_id, assertion_id, subject_id, change_kind, old_version, new_version, recorded_at, warrant_id}.»
- [ ] KGF MUST publish kgf.graph.changed events for every committed assertion create/update/delete: {tenant_id, assertion_id, subject_id, change_kind, old_version, new_version, recorded_at, warrant_id}.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-LVC-002 [P1] REQ-LVC-002: The SDK commit() MUST call A3 for every action of class ≥ INTERNALWRITE and implement step 7 (partial re-planning) for KGF's own agents

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:572-572` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-LVC-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-LVC-002 | The SDK `commit()` MUST call A3 for every action of class ≥ `INTERNAL_WRITE` and implement step 7 (partial re-planning) for KGF's own agents.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-LVC-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-LVC-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-LVC-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-LVC-002 | The SDK commit() MUST call A3 for every action of class ≥ INTERNAL_WRITE and implement step 7 (partial re-planning) for KGF's own agents.»
- [ ] The SDK commit() MUST call A3 for every action of class ≥ INTERNAL_WRITE and implement step 7 (partial re-planning) for KGF's own agents.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-LVC-005 [P1] REQ-LVC-005: Demonstration scenario (part of the Evidence Pack): an agent plans a change using fact F; F is changed by another user before commit; the commit returns REPLAN naming only the steps that used F; after

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:575-575` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-LVC-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-LVC-005 | Demonstration scenario (part of the Evidence Pack): an agent plans a change using fact F; F is changed by another user before commit; the commit returns `REPLAN` naming only the steps that used F; after re-planning the commit succeeds; the audit log shows the full sequence.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-LVC-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-LVC-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-LVC-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-LVC-005 | Demonstration scenario (part of the Evidence Pack): an agent plans a change using fact F; F is changed by another user before commit; the commit returns REPLAN naming only the steps that used F; after re-planning the commit succeeds; the audit log shows the full sequence.»
- [ ] Demonstration scenario (part of the Evidence Pack): an agent plans a change using fact F; F is changed by another user before commit; the commit returns REPLAN naming only the steps that used F; after re-planning the commit succeeds; the audit log shows the full sequence.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-MET-001 [P1] REQ-MET-001: Any consolidation (summarizing, deduplicating or compressing agent memory or KGF notes) MUST go through POST /memory/consolidate (or the SDK equivalent) which: (a) groups input propositions by status;

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:753-753` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-MET-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-MET-001 | Any consolidation (summarizing, deduplicating or compressing agent memory or KGF notes) MUST go through `POST /memory/consolidate` (or the SDK equivalent) which: (a) groups input propositions by status; (b) never produces a single output statement that combines propositions of different status; (c) produces output propositions each with a warrant composed by A1 from only the inputs it summarizes; (d) runs SASI on generated output; (e) creates verification tasks for any output proposition that became `GENERATED` while all its inputs were `OBSERVED`/`ATTESTED` (lost support).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-MET-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-MET-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-MET-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-MET-001 | Any consolidation (summarizing, deduplicating or compressing agent memory or KGF notes) MUST go through POST /memory/consolidate (or the SDK equivalent) which: (a) groups input propositions by status; (b) never produces a single output statement that combines propositions of different status; (c) produces output propositions each with a warrant composed by A1 from»
- [ ] Any consolidation (summarizing, deduplicating or compressing agent memory or KGF notes) MUST go through POST /memory/consolidate (or the SDK equivalent) which: (a) groups input propositions by status; (b) never produces a single output statement that combines propositions of different status; (c) produces output propositions each with a warrant composed by A1 from only the inputs it summarizes; (d
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-MMG-010 [P1] REQ-MMG-010: meaning-service MUST implement A6. Meaning release lifecycle: DRAFT → IMPACTANALYZED → REWRITESPROPOSED → EVALSRUN → APPROVED → PUBLISHED (or REJECTED)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:738-738` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-MMG-010; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-MMG-010 | `meaning-service` MUST implement A6. Meaning release lifecycle: `DRAFT → IMPACT_ANALYZED → REWRITES_PROPOSED → EVALS_RUN → APPROVED → PUBLISHED` (or `REJECTED`).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-MMG-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-MMG-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-MMG-010

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-MMG-010 | meaning-service MUST implement A6. Meaning release lifecycle: DRAFT → IMPACT_ANALYZED → REWRITES_PROPOSED → EVALS_RUN → APPROVED → PUBLISHED (or REJECTED).»
- [ ] meaning-service MUST implement A6. Meaning release lifecycle: DRAFT → IMPACT_ANALYZED → REWRITES_PROPOSED → EVALS_RUN → APPROVED → PUBLISHED (or REJECTED).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-MMG-011 [P1] REQ-MMG-011: APIs: POST /meaning/releases (from ontology version pair), GET /meaning/releases/{id}, GET …/impact, POST …/rewrites/{artifactid}/decide, POST …/evals/run, POST …/publish, POST …/rollback

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:739-739` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-MMG-011; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-MMG-011 | APIs: `POST /meaning/releases` (from ontology version pair), `GET /meaning/releases/{id}`, `GET …/impact`, `POST …/rewrites/{artifact_id}/decide`, `POST …/evals/run`, `POST …/publish`, `POST …/rollback`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-MMG-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-MMG-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-MMG-011

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-MMG-011 | APIs: POST /meaning/releases (from ontology version pair), GET /meaning/releases/{id}, GET …/impact, POST …/rewrites/{artifact_id}/decide, POST …/evals/run, POST …/publish, POST …/rollback.»
- [ ] APIs: POST /meaning/releases (from ontology version pair), GET /meaning/releases/{id}, GET …/impact, POST …/rewrites/{artifact_id}/decide, POST …/evals/run, POST …/publish, POST …/rollback.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-MMG-013 [P1] REQ-MMG-013: Rollback restores artifacts and ontology to v within 5 minutes for ≤ 10,000 artifacts

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:741-741` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-MMG-013; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-MMG-013 | Rollback restores artifacts and ontology to v within 5 minutes for ≤ 10,000 artifacts.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-MMG-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-MMG-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-MMG-013

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-MMG-013 | Rollback restores artifacts and ontology to v within 5 minutes for ≤ 10,000 artifacts.»
- [ ] Rollback restores artifacts and ontology to v within 5 minutes for ≤ 10,000 artifacts.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-NEU-030 [P1] REQ-NEU-030: Registry records {modelid, tenantid (or 'global'), task, version, training snapshot, feature version, hyperparameters, metrics, status (CANDIDATE, ACTIVE, RETIRED), artifact URI (encrypted at rest), c

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:821-821` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-NEU-030; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-NEU-030 | Registry records `{model_id, tenant_id (or 'global'), task, version, training snapshot, feature version, hyperparameters, metrics, status (CANDIDATE, ACTIVE, RETIRED), artifact URI (encrypted at rest), created_by, approved_by}`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-NEU-030' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-NEU-030') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-NEU-030

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-NEU-030 | Registry records {model_id, tenant_id (or 'global'), task, version, training snapshot, feature version, hyperparameters, metrics, status (CANDIDATE, ACTIVE, RETIRED), artifact URI (encrypted at rest), created_by, approved_by}.»
- [ ] Registry records {model_id, tenant_id (or 'global'), task, version, training snapshot, feature version, hyperparameters, metrics, status (CANDIDATE, ACTIVE, RETIRED), artifact URI (encrypted at rest), created_by, approved_by}.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-NEU-031 [P1] REQ-NEU-031: Promotion CANDIDATE → ACTIVE only through the gate defined for each task, recorded as an approval. Rollback to the previous ACTIVE version in < 1 minute

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:822-822` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-NEU-031; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-NEU-031 | Promotion `CANDIDATE → ACTIVE` only through the gate defined for each task, recorded as an approval. Rollback to the previous ACTIVE version in < 1 minute.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-NEU-031' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-NEU-031') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-NEU-031

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-NEU-031 | Promotion CANDIDATE → ACTIVE only through the gate defined for each task, recorded as an approval. Rollback to the previous ACTIVE version in < 1 minute.»
- [ ] Promotion CANDIDATE → ACTIVE only through the gate defined for each task, recorded as an approval. Rollback to the previous ACTIVE version in < 1 minute.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-OPR-001 [P1] REQ-OPR-001: Every operator (tool, query template, rule, model, LLM prompt, human approval step) used by KGF features or agents MUST be registered with operatorid, class (OBSERVER, COMPUTATION, MODEL, GENERATOR, H

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:389-389` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-OPR-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-OPR-001 | Every operator (tool, query template, rule, model, LLM prompt, human approval step) used by KGF features or agents MUST be registered with `operator_id`, `class` (`OBSERVER`, `COMPUTATION`, `MODEL`, `GENERATOR`, `HUMAN`), `version`, `owner`, `description`, `action_class` it can perform, and `approved_by`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-OPR-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-OPR-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-OPR-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-OPR-001 | Every operator (tool, query template, rule, model, LLM prompt, human approval step) used by KGF features or agents MUST be registered with operator_id, class (OBSERVER, COMPUTATION, MODEL, GENERATOR, HUMAN), version, owner, description, action_class it can perform, and approved_by.»
- [ ] Every operator (tool, query template, rule, model, LLM prompt, human approval step) used by KGF features or agents MUST be registered with operator_id, class (OBSERVER, COMPUTATION, MODEL, GENERATOR, HUMAN), version, owner, description, action_class it can perform, and approved_by.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-OPR-002 [P1] REQ-OPR-002: An unregistered operator invoked through the checkpoint SDK MUST be treated as class GENERATOR and its output status capped at GENERATED; an OPRUNREGISTERED audit event is written

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:390-390` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-OPR-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-OPR-002 | An unregistered operator invoked through the checkpoint SDK MUST be treated as class `GENERATOR` and its output status capped at `GENERATED`; an `OPR_UNREGISTERED` audit event is written.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-OPR-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-OPR-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-OPR-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-OPR-002 | An unregistered operator invoked through the checkpoint SDK MUST be treated as class GENERATOR and its output status capped at GENERATED; an OPR_UNREGISTERED audit event is written.»
- [ ] An unregistered operator invoked through the checkpoint SDK MUST be treated as class GENERATOR and its output status capped at GENERATED; an OPR_UNREGISTERED audit event is written.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-OPR-003 [P1] REQ-OPR-003: Registering or changing an operator's class requires permission ip.operator.approve and creates an entry in the Warrant Review process (§15.1)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:391-391` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-OPR-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-OPR-003 | Registering or changing an operator's class requires permission `ip.operator.approve` and creates an entry in the Warrant Review process (§15.1).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-OPR-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-OPR-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-OPR-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-OPR-003 | Registering or changing an operator's class requires permission ip.operator.approve and creates an entry in the Warrant Review process (§15.1).»
- [ ] Registering or changing an operator's class requires permission ip.operator.approve and creates an entry in the Warrant Review process (§15.1).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PLT-002 [P1] REQ-PLT-002: Every feature in this document MUST be behind a tenant-scoped feature flag named in §19.1, default off, switchable at runtime without restart

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:143-143` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PLT-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PLT-002 | Every feature in this document MUST be behind a tenant-scoped feature flag named in §19.1, default **off**, switchable at runtime without restart.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PLT-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PLT-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PLT-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PLT-002 | Every feature in this document MUST be behind a tenant-scoped feature flag named in §19.1, default off, switchable at runtime without restart.»
- [ ] Every feature in this document MUST be behind a tenant-scoped feature flag named in §19.1, default off, switchable at runtime without restart.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PLT-003 [P1] REQ-PLT-003: Every feature MUST work with no internet access (local-first). Model files, rule engines and libraries are installed with KGF

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:144-144` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PLT-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PLT-003 | Every feature MUST work with no internet access (local-first). Model files, rule engines and libraries are installed with KGF.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PLT-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PLT-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PLT-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PLT-003 | Every feature MUST work with no internet access (local-first). Model files, rule engines and libraries are installed with KGF.»
- [ ] Every feature MUST work with no internet access (local-first). Model files, rule engines and libraries are installed with KGF.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PLT-004 [P1] REQ-PLT-004: Every feature MUST work on each graph database KGF supports, through KGF's graph abstraction layer. Database-specific code is allowed only inside adapters

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:145-145` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PLT-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PLT-004 | Every feature MUST work on each graph database KGF supports, through KGF's graph abstraction layer. Database-specific code is allowed only inside adapters.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PLT-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PLT-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PLT-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PLT-004 | Every feature MUST work on each graph database KGF supports, through KGF's graph abstraction layer. Database-specific code is allowed only inside adapters.»
- [ ] Every feature MUST work on each graph database KGF supports, through KGF's graph abstraction layer. Database-specific code is allowed only inside adapters.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PLT-005 [P1] REQ-PLT-005: No feature may send tenant data to an external model endpoint unless the tenant's existing data-sharing policy explicitly permits that data class for that endpoint. The warrant, SASI, derivation-guard

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:146-146` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PLT-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PLT-005 | No feature may send tenant data to an external model endpoint unless the tenant's existing data-sharing policy explicitly permits that data class for that endpoint. The warrant, SASI, derivation-guard and neural components MUST default to local models.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PLT-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PLT-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PLT-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PLT-005 | No feature may send tenant data to an external model endpoint unless the tenant's existing data-sharing policy explicitly permits that data class for that endpoint. The warrant, SASI, derivation-guard and neural components MUST default to local models.»
- [ ] No feature may send tenant data to an external model endpoint unless the tenant's existing data-sharing policy explicitly permits that data class for that endpoint. The warrant, SASI, derivation-guard and neural components MUST default to local models.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PLT-006 [P1] REQ-PLT-006: Every state-changing API MUST write an audit event (§19.4) with actor, tenant, action, target, warrant id (when applicable) and outcome

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:147-147` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PLT-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PLT-006 | Every state-changing API MUST write an audit event (§19.4) with actor, tenant, action, target, warrant id (when applicable) and outcome.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PLT-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PLT-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PLT-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PLT-006 | Every state-changing API MUST write an audit event (§19.4) with actor, tenant, action, target, warrant id (when applicable) and outcome.»
- [ ] Every state-changing API MUST write an audit event (§19.4) with actor, tenant, action, target, warrant id (when applicable) and outcome.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PLT-009 [P1] REQ-PLT-009: All new services MUST expose health (/healthz), readiness (/readyz) and Prometheus-format metrics (/metrics), and propagate OpenTelemetry trace context

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:150-150` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PLT-009; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PLT-009 | All new services MUST expose health (`/healthz`), readiness (`/readyz`) and Prometheus-format metrics (`/metrics`), and propagate OpenTelemetry trace context.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PLT-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PLT-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PLT-009

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PLT-009 | All new services MUST expose health (/healthz), readiness (/readyz) and Prometheus-format metrics (/metrics), and propagate OpenTelemetry trace context.»
- [ ] All new services MUST expose health (/healthz), readiness (/readyz) and Prometheus-format metrics (/metrics), and propagate OpenTelemetry trace context.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PLT-010 [P1] REQ-PLT-010: Turning a feature flag off MUST restore the pre-feature behaviour of KGF exactly (no data loss, no errors). This is tested by the kill-switch control in §17.3

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:151-151` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PLT-010; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PLT-010 | Turning a feature flag off MUST restore the pre-feature behaviour of KGF exactly (no data loss, no errors). This is tested by the kill-switch control in §17.3.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PLT-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PLT-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PLT-010

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PLT-010 | Turning a feature flag off MUST restore the pre-feature behaviour of KGF exactly (no data loss, no errors). This is tested by the kill-switch control in §17.3.»
- [ ] Turning a feature flag off MUST restore the pre-feature behaviour of KGF exactly (no data loss, no errors). This is tested by the kill-switch control in §17.3.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-RFX-002 [P1] REQ-RFX-002: Validation: the action's tool and every operator in the condition MUST be registered with class OBSERVER, COMPUTATION or a tool whose action class is declared; any GENERATOR or MODEL operator is rejec

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1403-1403` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-RFX-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-RFX-002 | Validation: the action's tool and every operator in the condition MUST be registered with class `OBSERVER`, `COMPUTATION` or a tool whose action class is declared; any `GENERATOR` or `MODEL` operator is rejected with `RFX_GENERATOR_FORBIDDEN`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-RFX-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-RFX-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-RFX-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-RFX-002 | Validation: the action's tool and every operator in the condition MUST be registered with class OBSERVER, COMPUTATION or a tool whose action class is declared; any GENERATOR or MODEL operator is rejected with RFX_GENERATOR_FORBIDDEN.»
- [ ] Validation: the action's tool and every operator in the condition MUST be registered with class OBSERVER, COMPUTATION or a tool whose action class is declared; any GENERATOR or MODEL operator is rejected with RFX_GENERATOR_FORBIDDEN.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-RFX-003 [P1] REQ-RFX-003: A rule can be enabled only after a dry run on a shadow branch over the last 7 days of matching events (§13) has been reviewed and the rule approved by a principal with ip.reflex.approve; approval crea

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1404-1404` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-RFX-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-RFX-003 | A rule can be enabled only after a dry run on a shadow branch over the last 7 days of matching events (§13) has been reviewed and the rule approved by a principal with `ip.reflex.approve`; approval creates an `ATTESTED` warrant that becomes the authority of every fire.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-RFX-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-RFX-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-RFX-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-RFX-003 | A rule can be enabled only after a dry run on a shadow branch over the last 7 days of matching events (§13) has been reviewed and the rule approved by a principal with ip.reflex.approve; approval creates an ATTESTED warrant that becomes the authority of every fire.»
- [ ] A rule can be enabled only after a dry run on a shadow branch over the last 7 days of matching events (§13) has been reviewed and the rule approved by a principal with ip.reflex.approve; approval creates an ATTESTED warrant that becomes the authority of every fire.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-RFX-008 [P1] REQ-RFX-008: Demonstration scenario: a rule "when a ServiceAccount gets property compromised=true, disable its tokens and notify its owner" is dry-run, approved and enabled; setting the property fires it within 50

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1409-1409` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-RFX-008; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-RFX-008 | Demonstration scenario: a rule "when a ServiceAccount gets property `compromised=true`, disable its tokens and notify its owner" is dry-run, approved and enabled; setting the property fires it within 500 ms; the warrant shows the approver's authority; a burst of 25 matching events in an hour opens the circuit.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-RFX-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-RFX-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-RFX-008

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-RFX-008 | Demonstration scenario: a rule "when a ServiceAccount gets property compromised=true, disable its tokens and notify its owner" is dry-run, approved and enabled; setting the property fires it within 500 ms; the warrant shows the approver's authority; a burst of 25 matching events in an hour opens the circuit.»
- [ ] Demonstration scenario: a rule "when a ServiceAccount gets property compromised=true, disable its tokens and notify its owner" is dry-run, approved and enabled; setting the property fires it within 500 ms; the warrant shows the approver's authority; a burst of 25 matching events in an hour opens the circuit.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-SAS-001 [P1] REQ-SAS-001: sasi-engine MUST implement A2 exactly, using only local models by default. Model ids are configuration (sasi.extractmodel, sasi.embedmodel, sasi.nlimodel)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:445-445` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-SAS-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-SAS-001 | `sasi-engine` MUST implement A2 exactly, using only local models by default. Model ids are configuration (`sasi.extract_model`, `sasi.embed_model`, `sasi.nli_model`).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-SAS-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-SAS-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-SAS-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-SAS-001 | sasi-engine MUST implement A2 exactly, using only local models by default. Model ids are configuration (sasi.extract_model, sasi.embed_model, sasi.nli_model).»
- [ ] sasi-engine MUST implement A2 exactly, using only local models by default. Model ids are configuration (sasi.extract_model, sasi.embed_model, sasi.nli_model).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-SAS-002 [P1] REQ-SAS-002: Every generator call made through the checkpoint SDK MUST pass through SASI before its output leaves the rewrite checkpoint

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:446-446` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-SAS-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-SAS-002 | Every generator call made through the checkpoint SDK MUST pass through SASI before its output leaves the rewrite checkpoint.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-SAS-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-SAS-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-SAS-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-SAS-002 | Every generator call made through the checkpoint SDK MUST pass through SASI before its output leaves the rewrite checkpoint.»
- [ ] Every generator call made through the checkpoint SDK MUST pass through SASI before its output leaves the rewrite checkpoint.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-SAS-004 [P1] REQ-SAS-004: Benchmark dataset evals/sasi/laundering-v1.jsonl MUST be created with ≥ 300 hand-checked items: supported paraphrases, unsupported additions, altered numbers, altered names, merged hearsay. Acceptance

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:448-448` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-SAS-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-SAS-004 | Benchmark dataset `evals/sasi/laundering-v1.jsonl` MUST be created with ≥ 300 hand-checked items: supported paraphrases, unsupported additions, altered numbers, altered names, merged hearsay. Acceptance: on this set, precision of status inheritance ≥ 0.95 (an inherited status is correct) and recall of laundering detection ≥ 0.90 (unsupported propositions marked `GENERATED`). Report both on every model change.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-SAS-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-SAS-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-SAS-004

**Acceptance criteria**
- [ ] on this set, precision of status inheritance ≥ 0.95 (an inherited status is correct) and recall of laundering detection ≥ 0.90 (unsupported propositions marked GENERATED). Report both on every model change
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-SAS-006 [P1] REQ-SAS-006: If the NLI model is unavailable, SASI MUST fail closed: all propositions GENERATED, notice SASIDEGRADED, alert raised

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:450-450` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-SAS-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-SAS-006 | If the NLI model is unavailable, SASI MUST fail closed: all propositions `GENERATED`, notice `SASI_DEGRADED`, alert raised.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-SAS-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-SAS-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-SAS-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-SAS-006 | If the NLI model is unavailable, SASI MUST fail closed: all propositions GENERATED, notice SASI_DEGRADED, alert raised.»
- [ ] If the NLI model is unavailable, SASI MUST fail closed: all propositions GENERATED, notice SASI_DEGRADED, alert raised.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-SDK-002 [P1] REQ-SDK-002: The SDK MUST call checkpoints automatically; callers cannot bypass them except through ip.warrant.enabled=false (feature flag)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:490-490` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-SDK-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-SDK-002 | The SDK MUST call checkpoints automatically; callers cannot bypass them except through `ip.warrant.enabled=false` (feature flag).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-SDK-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-SDK-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-SDK-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-SDK-002 | The SDK MUST call checkpoints automatically; callers cannot bypass them except through ip.warrant.enabled=false (feature flag).»
- [ ] The SDK MUST call checkpoints automatically; callers cannot bypass them except through ip.warrant.enabled=false (feature flag).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-SDK-003 [P1] REQ-SDK-003: All existing KGF LLM features (NL query, query suggestion, report generation, entity auto-detection from JSON) MUST be migrated to the SDK. List each migrated feature in the binding map

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:491-491` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-SDK-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-SDK-003 | All existing KGF LLM features (NL query, query suggestion, report generation, entity auto-detection from JSON) MUST be migrated to the SDK. List each migrated feature in the binding map.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-SDK-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-SDK-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-SDK-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-SDK-003 | All existing KGF LLM features (NL query, query suggestion, report generation, entity auto-detection from JSON) MUST be migrated to the SDK. List each migrated feature in the binding map.»
- [ ] All existing KGF LLM features (NL query, query suggestion, report generation, entity auto-detection from JSON) MUST be migrated to the SDK. List each migrated feature in the binding map.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-SHB-001 [P1] REQ-SHB-001: branch-service creates copy-on-write branches of a tenant's authoritative graph: POST /branches {baseversion, purpose, ttl}. Reads on a branch see base + branch deltas; writes go only to branch deltas

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:780-780` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-SHB-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-SHB-001 | `branch-service` creates copy-on-write branches of a tenant's authoritative graph: `POST /branches {base_version, purpose, ttl}`. Reads on a branch see base + branch deltas; writes go only to branch deltas. Absent-capability rule: implement copy-on-write at the abstraction layer with a delta overlay store keyed by `(branch_id, assertion_id)` when the database has no native branching; record DR.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-SHB-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-SHB-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-SHB-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-SHB-001 | branch-service creates copy-on-write branches of a tenant's authoritative graph: POST /branches {base_version, purpose, ttl}. Reads on a branch see base + branch deltas; writes go only to branch deltas. Absent-capability rule: implement copy-on-write at the abstraction layer with a delta overlay store keyed by (branch_id, assertion_id) when the database has no nat»
- [ ] branch-service creates copy-on-write branches of a tenant's authoritative graph: POST /branches {base_version, purpose, ttl}. Reads on a branch see base + branch deltas; writes go only to branch deltas. Absent-capability rule: implement copy-on-write at the abstraction layer with a delta overlay store keyed by (branch_id, assertion_id) when the database has no native branching; record DR.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

