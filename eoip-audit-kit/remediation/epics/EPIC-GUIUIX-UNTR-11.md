# EPIC-GUIUIX-UNTR-11: GUI-UIX-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 60 tasks, ~360.0 h, priorities {'P2': 60}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-INT-542 [P2] INT-542: REST · POST /api/v1/playback/export · Playback Export

- **Source:** `GUI-UIX-requirements.md:1061-1061` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-542` | REST | `POST /api/v1/playback/export` | Playback Export | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `PARTIAL` | `apps/api/app.py:1327` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-542' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-542') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-542 | REST | POST /api/v1/playback/export | Playback Export | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | PARTIAL | apps/api/app.py:1327 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-543 [P2] INT-543: REST · POST /api/v1/playback/stream · Playback Stream

- **Source:** `GUI-UIX-requirements.md:1062-1062` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-543` | REST | `POST /api/v1/playback/stream` | Playback Stream | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `PARTIAL` | `apps/api/app.py:1311` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-543' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-543') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-543 | REST | POST /api/v1/playback/stream | Playback Stream | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | PARTIAL | apps/api/app.py:1311 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-551 [P2] INT-551: REST · GET /api/v1/process/cases · Process Cases

- **Source:** `GUI-UIX-requirements.md:1070-1070` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-551` | REST | `GET /api/v1/process/cases` | Process Cases | `none`; params: source_label | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1043` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-551' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-551') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-551 | REST | GET /api/v1/process/cases | Process Cases | none; params: source_label | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1043 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-552 [P2] INT-552: REST · POST /api/v1/process/deviations · Process Deviations

- **Source:** `GUI-UIX-requirements.md:1071-1071` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-552` | REST | `POST /api/v1/process/deviations` | Process Deviations | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1055` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-552' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-552') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-552 | REST | POST /api/v1/process/deviations | Process Deviations | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1055 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-553 [P2] INT-553: REST · GET /api/v1/process/paths · Process Paths

- **Source:** `GUI-UIX-requirements.md:1072-1072` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-553` | REST | `GET /api/v1/process/paths` | Process Paths | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1049` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-553' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-553') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-553 | REST | GET /api/v1/process/paths | Process Paths | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1049 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-554 [P2] INT-554: REST · GET /api/v1/product/capabilities · Product Capabilities

- **Source:** `GUI-UIX-requirements.md:1073-1073` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-554` | REST | `GET /api/v1/product/capabilities` | Product Capabilities | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1521` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-554' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-554') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-554 | REST | GET /api/v1/product/capabilities | Product Capabilities | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1521 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-555 [P2] INT-555: REST · POST /api/v1/product/capabilities/materialize · Materialize Product Capabilities

- **Source:** `GUI-UIX-requirements.md:1074-1074` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-555` | REST | `POST /api/v1/product/capabilities/materialize` | Materialize Product Capabilities | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1552` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-555' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-555') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-555 | REST | POST /api/v1/product/capabilities/materialize | Materialize Product Capabilities | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1552 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-556 [P2] INT-556: REST · GET /api/v1/product/first-choice-gate · Product First Choice Gate

- **Source:** `GUI-UIX-requirements.md:1075-1075` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-556` | REST | `GET /api/v1/product/first-choice-gate` | Product First Choice Gate | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1534` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-556' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-556') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-556 | REST | GET /api/v1/product/first-choice-gate | Product First Choice Gate | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1534 | No primary screen assigned»
- [ ] Product First Choice Gate
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-557 [P2] INT-557: REST · GET /api/v1/qa/dashboard · Dashboard Report

- **Source:** `GUI-UIX-requirements.md:1076-1076` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-557` | REST | `GET /api/v1/qa/dashboard` | Dashboard Report | `none`; params: requirement_ids | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/qa/router.py:102` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-557' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-557') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-557 | REST | GET /api/v1/qa/dashboard | Dashboard Report | none; params: requirement_ids | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/qa/router.py:102 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-558 [P2] INT-558: REST · POST /api/v1/qa/dashboard/external-gates · Record Gate

- **Source:** `GUI-UIX-requirements.md:1077-1077` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-558` | REST | `POST /api/v1/qa/dashboard/external-gates` | Record Gate | `ExternalGateRecord`; params: none | `object` | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-558' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-558') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-558 | REST | POST /api/v1/qa/dashboard/external-gates | Record Gate | ExternalGateRecord; params: none | object | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 201,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-559 [P2] INT-559: REST · POST /api/v1/qa/dashboard/test-runs · Record Run

- **Source:** `GUI-UIX-requirements.md:1078-1078` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-559` | REST | `POST /api/v1/qa/dashboard/test-runs` | Record Run | `TestRunSummary`; params: none | `object` | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-559' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-559') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-559 | REST | POST /api/v1/qa/dashboard/test-runs | Record Run | TestRunSummary; params: none | object | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 201,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-560 [P2] INT-560: REST · GET /api/v1/qa/evidence/coverage · Coverage

- **Source:** `GUI-UIX-requirements.md:1079-1079` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-560` | REST | `GET /api/v1/qa/evidence/coverage` | Coverage | `none`; params: requirement_ids | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/qa/router.py:61` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-560' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-560') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-560 | REST | GET /api/v1/qa/evidence/coverage | Coverage | none; params: requirement_ids | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/qa/router.py:61 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-561 [P2] INT-561: REST · GET /api/v1/qa/evidence/coverage/{requirement_id} · Requirement Coverage

- **Source:** `GUI-UIX-requirements.md:1080-1080` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-561` | REST | `GET /api/v1/qa/evidence/coverage/{requirement_id}` | Requirement Coverage | `none`; params: requirement_id | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/qa/router.py:73` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-561' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-561') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-561 | REST | GET /api/v1/qa/evidence/coverage/{requirement_id} | Requirement Coverage | none; params: requirement_id | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/qa/router.py:73 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-562 [P2] INT-562: REST · POST /api/v1/qa/evidence/register · Register

- **Source:** `GUI-UIX-requirements.md:1081-1081` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-562` | REST | `POST /api/v1/qa/evidence/register` | Register | `EvidenceEntry`; params: none | `object` | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-562' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-562') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-562 | REST | POST /api/v1/qa/evidence/register | Register | EvidenceEntry; params: none | object | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 201,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-563 [P2] INT-563: REST · GET /api/v1/qa/inventory · Inventory

- **Source:** `GUI-UIX-requirements.md:1082-1082` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-563` | REST | `GET /api/v1/qa/inventory` | Inventory | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/qa/router.py:116` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-563' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-563') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-563 | REST | GET /api/v1/qa/inventory | Inventory | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/qa/router.py:116 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-564 [P2] INT-564: REST · POST /api/v1/qa/inventory/validate · Validate Inventory

- **Source:** `GUI-UIX-requirements.md:1083-1083` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-564` | REST | `POST /api/v1/qa/inventory/validate` | Validate Inventory | `InventorySnapshot`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-564' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-564') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-564 | REST | POST /api/v1/qa/inventory/validate | Validate Inventory | InventorySnapshot; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-565 [P2] INT-565: REST · GET /api/v1/qa/mutation-checks · List Checks

- **Source:** `GUI-UIX-requirements.md:1084-1084` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-565` | REST | `GET /api/v1/qa/mutation-checks` | List Checks | `none`; params: none | `array` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/qa/router.py:93` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-565' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-565') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-565 | REST | GET /api/v1/qa/mutation-checks | List Checks | none; params: none | array | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/qa/router.py:93 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-566 [P2] INT-566: REST · POST /api/v1/qa/mutation-checks · Run Check

- **Source:** `GUI-UIX-requirements.md:1085-1085` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-566` | REST | `POST /api/v1/qa/mutation-checks` | Run Check | `object`; params: none | `object` | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-566' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-566') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-566 | REST | POST /api/v1/qa/mutation-checks | Run Check | object; params: none | object | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 201,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-567 [P2] INT-567: REST · GET /api/v1/qa/mutation-checks/release/{release} · Release Summary

- **Source:** `GUI-UIX-requirements.md:1086-1086` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-567` | REST | `GET /api/v1/qa/mutation-checks/release/{release}` | Release Summary | `none`; params: release | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/qa/router.py:97` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-567' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-567') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-567 | REST | GET /api/v1/qa/mutation-checks/release/{release} | Release Summary | none; params: release | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/qa/router.py:97 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-568 [P2] INT-568: REST · GET /api/v1/qa/policy-gate/latest · Latest Policy Gate

- **Source:** `GUI-UIX-requirements.md:1087-1087` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-568` | REST | `GET /api/v1/qa/policy-gate/latest` | Latest Policy Gate | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/qa/router.py:129` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-568' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-568') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-568 | REST | GET /api/v1/qa/policy-gate/latest | Latest Policy Gate | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/qa/router.py:129 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-569 [P2] INT-569: REST · POST /api/v1/qa/policy-gate/run · Run Policy Gate

- **Source:** `GUI-UIX-requirements.md:1088-1088` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-569` | REST | `POST /api/v1/qa/policy-gate/run` | Run Policy Gate | `none`; params: none | `object` | 201; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-569' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-569') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-569 | REST | POST /api/v1/qa/policy-gate/run | Run Policy Gate | none; params: none | object | 201; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 201; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-570 [P2] INT-570: REST · POST /api/v1/query · Query Plan

- **Source:** `GUI-UIX-requirements.md:1089-1089` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-570` | REST | `POST /api/v1/query` | Query Plan | `QueryPlan`; params: none | `GraphResult` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:499` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-570' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-570') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-570 | REST | POST /api/v1/query | Query Plan | QueryPlan; params: none | GraphResult | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:499 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-571 [P2] INT-571: REST · GET /api/v1/query/cache/stats · Query Cache Stats

- **Source:** `GUI-UIX-requirements.md:1090-1090` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-571` | REST | `GET /api/v1/query/cache/stats` | Query Cache Stats | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1034` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-571' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-571') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-571 | REST | GET /api/v1/query/cache/stats | Query Cache Stats | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1034 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-572 [P2] INT-572: REST · GET /api/v1/query/context/{entity_cid} · Query Context Endpoint

- **Source:** `GUI-UIX-requirements.md:1091-1091` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-572` | REST | `GET /api/v1/query/context/{entity_cid}` | Query Context Endpoint | `none`; params: entity_cid | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/reports/router.py:52` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-572' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-572') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-572 | REST | GET /api/v1/query/context/{entity_cid} | Query Context Endpoint | none; params: entity_cid | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/reports/router.py:52 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-573 [P2] INT-573: REST · POST /api/v1/query/cost · Query Cost

- **Source:** `GUI-UIX-requirements.md:1092-1092` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-573` | REST | `POST /api/v1/query/cost` | Query Cost | `QueryPlan`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:662` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-573' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-573') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-573 | REST | POST /api/v1/query/cost | Query Cost | QueryPlan; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:662 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-574 [P2] INT-574: REST · POST /api/v1/query/eql · Eql Query

- **Source:** `GUI-UIX-requirements.md:1093-1093` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-574` | REST | `POST /api/v1/query/eql` | Eql Query | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1573` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-574' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-574') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-574 | REST | POST /api/v1/query/eql | Eql Query | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1573 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-575 [P2] INT-575: REST · POST /api/v1/query/explain · Query Explain

- **Source:** `GUI-UIX-requirements.md:1094-1094` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-575` | REST | `POST /api/v1/query/explain` | Query Explain | `QueryPlan`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:657` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-575' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-575') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-575 | REST | POST /api/v1/query/explain | Query Explain | QueryPlan; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:657 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-576 [P2] INT-576: REST · GET /api/v1/query/history · Query History

- **Source:** `GUI-UIX-requirements.md:1095-1095` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-576` | REST | `GET /api/v1/query/history` | Query History | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:667` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-576' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-576') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-576 | REST | GET /api/v1/query/history | Query History | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:667 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-577 [P2] INT-577: REST · POST /api/v1/query/language · Query Language

- **Source:** `GUI-UIX-requirements.md:1096-1096` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-577` | REST | `POST /api/v1/query/language` | Query Language | `QueryLanguageRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:912` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-577' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-577') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-577 | REST | POST /api/v1/query/language | Query Language | QueryLanguageRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:912 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-578 [P2] INT-578: REST · POST /api/v1/query/multi-paradigm · Multi Paradigm Query

- **Source:** `GUI-UIX-requirements.md:1097-1097` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-578` | REST | `POST /api/v1/query/multi-paradigm` | Multi Paradigm Query | `MultiParadigmQueryRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/enterprise/advanced_router.py:97` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-578' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-578') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-578 | REST | POST /api/v1/query/multi-paradigm | Multi Paradigm Query | MultiParadigmQueryRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/enterprise/advanced_router.py:97 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-579 [P2] INT-579: REST · POST /api/v1/query/nl · Query Nl

- **Source:** `GUI-UIX-requirements.md:1098-1098` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-579` | REST | `POST /api/v1/query/nl` | Query Nl | `NLQueryRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:506` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-579' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-579') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-579 | REST | POST /api/v1/query/nl | Query Nl | NLQueryRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:506 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-580 [P2] INT-580: REST · GET /api/v1/query/slow · Query Slow

- **Source:** `GUI-UIX-requirements.md:1099-1099` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-580` | REST | `GET /api/v1/query/slow` | Query Slow | `none`; params: threshold_ms, top_n | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:674` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-580' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-580') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-580 | REST | GET /api/v1/query/slow | Query Slow | none; params: threshold_ms, top_n | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:674 | No primary screen assigned»
- [ ] none; params: threshold_ms, top_n
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-581 [P2] INT-581: REST · GET /api/v1/query/templates · Query List Templates

- **Source:** `GUI-UIX-requirements.md:1100-1100` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-581` | REST | `GET /api/v1/query/templates` | Query List Templates | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:684` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-581' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-581') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-581 | REST | GET /api/v1/query/templates | Query List Templates | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:684 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-582 [P2] INT-582: REST · POST /api/v1/query/templates · Query Save Template

- **Source:** `GUI-UIX-requirements.md:1101-1101` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-582` | REST | `POST /api/v1/query/templates` | Query Save Template | `TemplateSaveRequest`; params: none | `object` | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:691` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-582' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-582') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-582 | REST | POST /api/v1/query/templates | Query Save Template | TemplateSaveRequest; params: none | object | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:691 | No primary screen assigned»
- [ ] 201,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-583 [P2] INT-583: REST · GET /api/v1/query/templates/{template_id} · Query Get Template

- **Source:** `GUI-UIX-requirements.md:1102-1102` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-583` | REST | `GET /api/v1/query/templates/{template_id}` | Query Get Template | `none`; params: template_id | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:712` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-583' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-583') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-583 | REST | GET /api/v1/query/templates/{template_id} | Query Get Template | none; params: template_id | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:712 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-584 [P2] INT-584: REST · DELETE /api/v1/query/templates/{template_id} · Query Delete Template

- **Source:** `GUI-UIX-requirements.md:1103-1103` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-584` | REST | `DELETE /api/v1/query/templates/{template_id}` | Query Delete Template | `none`; params: template_id | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:720` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-584' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-584') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-584 | REST | DELETE /api/v1/query/templates/{template_id} | Query Delete Template | none; params: template_id | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:720 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-585 [P2] INT-585: REST · POST /api/v1/query/templates/{template_id}/bind · Query Bind Template

- **Source:** `GUI-UIX-requirements.md:1104-1104` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-585` | REST | `POST /api/v1/query/templates/{template_id}/bind` | Query Bind Template | `TemplateBindRequest`; params: template_id | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:728` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-585' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-585') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-585 | REST | POST /api/v1/query/templates/{template_id}/bind | Query Bind Template | TemplateBindRequest; params: template_id | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:728 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-586 [P2] INT-586: REST · POST /api/v1/query/what-changed · Query What Changed Required Alias

- **Source:** `GUI-UIX-requirements.md:1105-1105` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-586` | REST | `POST /api/v1/query/what-changed` | Query What Changed Required Alias | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1137` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-586' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-586') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-586 | REST | POST /api/v1/query/what-changed | Query What Changed Required Alias | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1137 | No primary screen assigned»
- [ ] Query What Changed Required Alias
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-587 [P2] INT-587: REST · GET /api/v1/query/what-changed/{entity_cid} · Query What Changed Endpoint

- **Source:** `GUI-UIX-requirements.md:1106-1106` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-587` | REST | `GET /api/v1/query/what-changed/{entity_cid}` | Query What Changed Endpoint | `none`; params: entity_cid | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/reports/router.py:52` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-587' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-587') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-587 | REST | GET /api/v1/query/what-changed/{entity_cid} | Query What Changed Endpoint | none; params: entity_cid | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/reports/router.py:52 | No primary screen assigned»
- [ ] Query What Changed Endpoint
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-588 [P2] INT-588: REST · POST /api/v1/query/what-if · Query What If Required Alias

- **Source:** `GUI-UIX-requirements.md:1107-1107` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-588` | REST | `POST /api/v1/query/what-if` | Query What If Required Alias | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1146` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-588' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-588') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-588 | REST | POST /api/v1/query/what-if | Query What If Required Alias | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1146 | No primary screen assigned»
- [ ] Query What If Required Alias
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-589 [P2] INT-589: REST · POST /api/v1/query/why · Query Why Required Alias

- **Source:** `GUI-UIX-requirements.md:1108-1108` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-589` | REST | `POST /api/v1/query/why` | Query Why Required Alias | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1114` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-589' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-589') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-589 | REST | POST /api/v1/query/why | Query Why Required Alias | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1114 | No primary screen assigned»
- [ ] Query Why Required Alias
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-590 [P2] INT-590: REST · POST /api/v1/query/why-not · Query Why Not Endpoint

- **Source:** `GUI-UIX-requirements.md:1109-1109` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-590` | REST | `POST /api/v1/query/why-not` | Query Why Not Endpoint | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1123` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-590' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-590') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-590 | REST | POST /api/v1/query/why-not | Query Why Not Endpoint | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1123 | No primary screen assigned»
- [ ] Query Why Not Endpoint
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-591 [P2] INT-591: REST · GET /api/v1/query/why/{entity_cid} · Query Why Endpoint

- **Source:** `GUI-UIX-requirements.md:1110-1110` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-591` | REST | `GET /api/v1/query/why/{entity_cid}` | Query Why Endpoint | `none`; params: entity_cid | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/reports/router.py:52` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-591' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-591') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-591 | REST | GET /api/v1/query/why/{entity_cid} | Query Why Endpoint | none; params: entity_cid | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/reports/router.py:52 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-592 [P2] INT-592: REST · POST /api/v1/rag · Rag

- **Source:** `GUI-UIX-requirements.md:1111-1111` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-592` | REST | `POST /api/v1/rag` | Rag | `RetrievalRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:1356` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-592' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-592') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-592 | REST | POST /api/v1/rag | Rag | RetrievalRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/main.py:1356 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-593 [P2] INT-593: REST · GET /api/v1/rag/patterns · Rag Patterns

- **Source:** `GUI-UIX-requirements.md:1112-1112` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-593` | REST | `GET /api/v1/rag/patterns` | Rag Patterns | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1643` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-593' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-593') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-593 | REST | GET /api/v1/rag/patterns | Rag Patterns | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1643 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-594 [P2] INT-594: REST · POST /api/v1/rag/query · Rag Query

- **Source:** `GUI-UIX-requirements.md:1113-1113` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-594` | REST | `POST /api/v1/rag/query` | Rag Query | `RAGQueryRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1637` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-594' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-594') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-594 | REST | POST /api/v1/rag/query | Rag Query | RAGQueryRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1637 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-595 [P2] INT-595: REST · GET /api/v1/reports · Reports Capability

- **Source:** `GUI-UIX-requirements.md:1114-1114` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-595` | REST | `GET /api/v1/reports` | Reports Capability | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/reports/router.py:52` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-595' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-595') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-595 | REST | GET /api/v1/reports | Reports Capability | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/reports/router.py:52 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-596 [P2] INT-596: REST · GET /api/v1/reports/export/{report_id} · Export Placeholder

- **Source:** `GUI-UIX-requirements.md:1115-1115` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-596` | REST | `GET /api/v1/reports/export/{report_id}` | Export Placeholder | `none`; params: report_id, report_format | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `PARTIAL` | `packages/eoip/reports/router.py:52` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-596' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-596') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-596 | REST | GET /api/v1/reports/export/{report_id} | Export Placeholder | none; params: report_id, report_format | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | PARTIAL | packages/eoip/reports/router.py:52 | No primary screen assigned»
- [ ] none; params: report_id, report_format
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-597 [P2] INT-597: REST · POST /api/v1/reports/render · Render Report

- **Source:** `GUI-UIX-requirements.md:1116-1116` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-597` | REST | `POST /api/v1/reports/render` | Render Report | `ReportContext`; params: template_id, report_format, generated_at | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-597' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-597') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-597 | REST | POST /api/v1/reports/render | Render Report | ReportContext; params: template_id, report_format, generated_at | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] ReportContext; params: template_id, report_format, generated_at
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-598 [P2] INT-598: REST · GET /api/v1/reports/schedules · List Schedules

- **Source:** `GUI-UIX-requirements.md:1117-1117` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-598` | REST | `GET /api/v1/reports/schedules` | List Schedules | `none`; params: none | `array` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/reports/router.py:52` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-598' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-598') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-598 | REST | GET /api/v1/reports/schedules | List Schedules | none; params: none | array | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/reports/router.py:52 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-599 [P2] INT-599: REST · POST /api/v1/reports/schedules · Create Schedule

- **Source:** `GUI-UIX-requirements.md:1118-1118` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-599` | REST | `POST /api/v1/reports/schedules` | Create Schedule | `inline`; params: template_id, name, recurrence, report_format | `object` | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-599' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-599') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-599 | REST | POST /api/v1/reports/schedules | Create Schedule | inline; params: template_id, name, recurrence, report_format | object | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] inline; params: template_id, name, recurrence, report_format
- [ ] 201,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-600 [P2] INT-600: REST · GET /api/v1/reports/schedules/due · Due Schedules

- **Source:** `GUI-UIX-requirements.md:1119-1119` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-600` | REST | `GET /api/v1/reports/schedules/due` | Due Schedules | `none`; params: none | `array` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/reports/router.py:52` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-600' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-600') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-600 | REST | GET /api/v1/reports/schedules/due | Due Schedules | none; params: none | array | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/reports/router.py:52 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-601 [P2] INT-601: REST · DELETE /api/v1/reports/schedules/{schedule_id} · Delete Schedule

- **Source:** `GUI-UIX-requirements.md:1120-1120` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-601` | REST | `DELETE /api/v1/reports/schedules/{schedule_id}` | Delete Schedule | `none`; params: schedule_id | `HTTPValidationError` | 204,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/reports/router.py:158` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-601' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-601') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-601 | REST | DELETE /api/v1/reports/schedules/{schedule_id} | Delete Schedule | none; params: schedule_id | HTTPValidationError | 204,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/reports/router.py:158 | No primary screen assigned»
- [ ] 204,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-602 [P2] INT-602: REST · POST /api/v1/reports/schedules/{schedule_id}/mark-run · Mark Run

- **Source:** `GUI-UIX-requirements.md:1121-1121` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-602` | REST | `POST /api/v1/reports/schedules/{schedule_id}/mark-run` | Mark Run | `none`; params: schedule_id, at | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-602' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-602') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-602 | REST | POST /api/v1/reports/schedules/{schedule_id}/mark-run | Mark Run | none; params: schedule_id, at | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] none; params: schedule_id, at
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-603 [P2] INT-603: REST · GET /api/v1/reports/templates · List Templates

- **Source:** `GUI-UIX-requirements.md:1122-1122` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-603` | REST | `GET /api/v1/reports/templates` | List Templates | `none`; params: none | `array` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/reports/router.py:52` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-603' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-603') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-603 | REST | GET /api/v1/reports/templates | List Templates | none; params: none | array | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/reports/router.py:52 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-604 [P2] INT-604: REST · POST /api/v1/retrieval/search · Retrieval Search

- **Source:** `GUI-UIX-requirements.md:1123-1123` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-604` | REST | `POST /api/v1/retrieval/search` | Retrieval Search | `RetrievalSearchRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:850` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-604' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-604') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-604 | REST | POST /api/v1/retrieval/search | Retrieval Search | RetrievalSearchRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:850 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-605 [P2] INT-605: REST · GET /api/v1/search · Search

- **Source:** `GUI-UIX-requirements.md:1124-1124` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-605` | REST | `GET /api/v1/search` | Search | `none`; params: q, label, limit, include_deleted | `GraphResult` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:386` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-605' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-605') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-605 | REST | GET /api/v1/search | Search | none; params: q, label, limit, include_deleted | GraphResult | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:386 | No primary screen assigned»
- [ ] none; params: q, label, limit, include_deleted
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-606 [P2] INT-606: REST · POST /api/v1/search/faceted · Search Faceted

- **Source:** `GUI-UIX-requirements.md:1125-1125` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-606` | REST | `POST /api/v1/search/faceted` | Search Faceted | `SearchRequest`; params: none | `SearchResponse` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:742` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-606' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-606') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-606 | REST | POST /api/v1/search/faceted | Search Faceted | SearchRequest; params: none | SearchResponse | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:742 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-612 [P2] INT-612: REST · POST /api/v1/simulation/create · Simulation Create

- **Source:** `GUI-UIX-requirements.md:1131-1131` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-612` | REST | `POST /api/v1/simulation/create` | Simulation Create | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1168` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-612' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-612') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-612 | REST | POST /api/v1/simulation/create | Simulation Create | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1168 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-613 [P2] INT-613: REST · GET /api/v1/simulation/list · Simulation List

- **Source:** `GUI-UIX-requirements.md:1132-1132` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-613` | REST | `GET /api/v1/simulation/list` | Simulation List | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1201` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-613' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-613') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-613 | REST | GET /api/v1/simulation/list | Simulation List | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1201 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

