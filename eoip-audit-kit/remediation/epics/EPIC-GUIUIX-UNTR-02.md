# EPIC-GUIUIX-UNTR-02: GUI-UIX-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 60 tasks, ~360.0 h, priorities {'P1': 49, 'P2': 11}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-INT-150 [P1] INT-150: REST · POST /api/v1/egress/endpoints/{endpoint_id}/disable · Disable Endpoint

- **Source:** `GUI-UIX-requirements.md:669-669` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-150` | REST | `POST /api/v1/egress/endpoints/{endpoint_id}/disable` | Disable Endpoint | `KillRequest`; params: endpoint_id | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/egress/router.py:118` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-150' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-150') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-150 | REST | POST /api/v1/egress/endpoints/{endpoint_id}/disable | Disable Endpoint | KillRequest; params: endpoint_id | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/egress/router.py:118 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-151 [P1] INT-151: REST · POST /api/v1/egress/endpoints/{endpoint_id}/enable · Enable Endpoint

- **Source:** `GUI-UIX-requirements.md:670-670` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-151` | REST | `POST /api/v1/egress/endpoints/{endpoint_id}/enable` | Enable Endpoint | `EnableEndpointRequest`; params: endpoint_id | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/egress/router.py:96` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-151' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-151') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-151 | REST | POST /api/v1/egress/endpoints/{endpoint_id}/enable | Enable Endpoint | EnableEndpointRequest; params: endpoint_id | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/egress/router.py:96 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-152 [P1] INT-152: REST · POST /api/v1/egress/kill · Kill

- **Source:** `GUI-UIX-requirements.md:671-671` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-152` | REST | `POST /api/v1/egress/kill` | Kill | `KillRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/egress/router.py:172` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-152' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-152') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-152 | REST | POST /api/v1/egress/kill | Kill | KillRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/egress/router.py:172 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-153 [P1] INT-153: REST · GET /api/v1/egress/manifests · Manifests

- **Source:** `GUI-UIX-requirements.md:672-672` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-153` | REST | `GET /api/v1/egress/manifests` | Manifests | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/egress/router.py:180` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-153' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-153') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-153 | REST | GET /api/v1/egress/manifests | Manifests | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/egress/router.py:180 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-154 [P1] INT-154: REST · GET /api/v1/egress/plugins · List Plugins

- **Source:** `GUI-UIX-requirements.md:673-673` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-154` | REST | `GET /api/v1/egress/plugins` | List Plugins | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/egress/router.py:204` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-154' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-154') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-154 | REST | GET /api/v1/egress/plugins | List Plugins | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/egress/router.py:204 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-155 [P1] INT-155: REST · POST /api/v1/egress/plugins/install · Install Plugin

- **Source:** `GUI-UIX-requirements.md:674-674` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-155` | REST | `POST /api/v1/egress/plugins/install` | Install Plugin | `InstallPluginRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/egress/router.py:193` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-155' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-155') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-155 | REST | POST /api/v1/egress/plugins/install | Install Plugin | InstallPluginRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/egress/router.py:193 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-156 [P1] INT-156: REST · POST /api/v1/egress/plugins/submit · Submit Plugin

- **Source:** `GUI-UIX-requirements.md:675-675` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-156` | REST | `POST /api/v1/egress/plugins/submit` | Submit Plugin | `SubmitPluginRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/egress/router.py:188` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-156' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-156') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-156 | REST | POST /api/v1/egress/plugins/submit | Submit Plugin | SubmitPluginRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/egress/router.py:188 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-157 [P1] INT-157: REST · GET /api/v1/egress/policy/rules · List Rules

- **Source:** `GUI-UIX-requirements.md:676-676` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-157` | REST | `GET /api/v1/egress/policy/rules` | List Rules | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/egress/router.py:167` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-157' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-157') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-157 | REST | GET /api/v1/egress/policy/rules | List Rules | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/egress/router.py:167 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-158 [P1] INT-158: REST · POST /api/v1/egress/policy/rules · Add Rule

- **Source:** `GUI-UIX-requirements.md:677-677` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-158` | REST | `POST /api/v1/egress/policy/rules` | Add Rule | `AddRuleRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/egress/router.py:162` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-158' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-158') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-158 | REST | POST /api/v1/egress/policy/rules | Add Rule | AddRuleRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/egress/router.py:162 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-159 [P1] INT-159: REST · GET /api/v1/egress/report · Report

- **Source:** `GUI-UIX-requirements.md:678-678` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-159` | REST | `GET /api/v1/egress/report` | Report | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/egress/router.py:184` | SCR-019
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-159' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-159') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-159 | REST | GET /api/v1/egress/report | Report | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/egress/router.py:184 | SCR-019»
- [ ] 200; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-168 [P1] INT-168: REST · GET /api/v1/enterprise/audit/stats · Audit log statistics

- **Source:** `GUI-UIX-requirements.md:687-687` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-168` | REST | `GET /api/v1/enterprise/audit/stats` | Audit log statistics | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/enterprise/router.py:561` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-168' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-168') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-168 | REST | GET /api/v1/enterprise/audit/stats | Audit log statistics | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/enterprise/router.py:561 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-169 [P1] INT-169: REST · GET /api/v1/enterprise/audit/verify · Verify audit chain integrity

- **Source:** `GUI-UIX-requirements.md:688-688` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-169` | REST | `GET /api/v1/enterprise/audit/verify` | Verify audit chain integrity | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/enterprise/router.py:567` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-169' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-169') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-169 | REST | GET /api/v1/enterprise/audit/verify | Verify audit chain integrity | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/enterprise/router.py:567 | No primary screen assigned»
- [ ] Verify audit chain integrity
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-202 [P1] INT-202: REST · GET /api/v1/enterprise/lifecycle/status · Application lifecycle status

- **Source:** `GUI-UIX-requirements.md:721-721` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-202` | REST | `GET /api/v1/enterprise/lifecycle/status` | Application lifecycle status | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/authz/security_router.py:122` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-202' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-202') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-202 | REST | GET /api/v1/enterprise/lifecycle/status | Application lifecycle status | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/authz/security_router.py:122 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-207 [P1] INT-207: REST · POST /api/v1/enterprise/migrations/{migration_id}/rollback · Rollback migration

- **Source:** `GUI-UIX-requirements.md:726-726` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-207` | REST | `POST /api/v1/enterprise/migrations/{migration_id}/rollback` | Rollback migration | `none`; params: migration_id | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/config/router.py:125` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-207' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-207') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-207 | REST | POST /api/v1/enterprise/migrations/{migration_id}/rollback | Rollback migration | none; params: migration_id | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/config/router.py:125 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-211 [P1] INT-211: REST · GET /api/v1/enterprise/plugins · List plugins

- **Source:** `GUI-UIX-requirements.md:730-730` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-211` | REST | `GET /api/v1/enterprise/plugins` | List plugins | `none`; params: none | `array` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/egress/router.py:204` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-211' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-211') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-211 | REST | GET /api/v1/enterprise/plugins | List plugins | none; params: none | array | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/egress/router.py:204 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-218 [P1] INT-218: REST · POST /api/v1/enterprise/snapshots/restore · Restore from snapshot

- **Source:** `GUI-UIX-requirements.md:737-737` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-218` | REST | `POST /api/v1/enterprise/snapshots/restore` | Restore from snapshot | `RestoreRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/enterprise/router.py:198` | SCR-010
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-218' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-218') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-218 | REST | POST /api/v1/enterprise/snapshots/restore | Restore from snapshot | RestoreRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/enterprise/router.py:198 | SCR-010»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-316 [P1] INT-316: REST · GET /api/v1/licensing/status · Status

- **Source:** `GUI-UIX-requirements.md:835-835` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-316` | REST | `GET /api/v1/licensing/status` | Status | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/authz/security_router.py:122` | SCR-026
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-316' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-316') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-316 | REST | GET /api/v1/licensing/status | Status | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/authz/security_router.py:122 | SCR-026»
- [ ] 200; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-359 [P1] INT-359: REST · POST /api/v1/ontology/gitops/rollback · Rollback Version

- **Source:** `GUI-UIX-requirements.md:878-878` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-359` | REST | `POST /api/v1/ontology/gitops/rollback` | Rollback Version | `RollbackRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/config/router.py:125` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-359' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-359') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-359 | REST | POST /api/v1/ontology/gitops/rollback | Rollback Version | RollbackRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/config/router.py:125 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-384 [P1] INT-384: REST · POST /api/v1/platform/aiml/tokens/budget · Create token budget

- **Source:** `GUI-UIX-requirements.md:903-903` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-384` | REST | `POST /api/v1/platform/aiml/tokens/budget` | Create token budget | `TokenBudgetRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-384' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-384') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-384 | REST | POST /api/v1/platform/aiml/tokens/budget | Create token budget | TokenBudgetRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-385 [P1] INT-385: REST · POST /api/v1/platform/aiml/tokens/consume · Consume token budget

- **Source:** `GUI-UIX-requirements.md:904-904` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-385` | REST | `POST /api/v1/platform/aiml/tokens/consume` | Consume token budget | `TokenConsumeRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-385' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-385') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-385 | REST | POST /api/v1/platform/aiml/tokens/consume | Consume token budget | TokenConsumeRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-432 [P1] INT-432: REST · POST /api/v1/platform/guardrails/reflection-sandbox · Execute agent action inside formal invariance sandbox

- **Source:** `GUI-UIX-requirements.md:951-951` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-432` | REST | `POST /api/v1/platform/guardrails/reflection-sandbox` | Execute agent action inside formal invariance sandbox | `ReflectionSandboxRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-432' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-432') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-432 | REST | POST /api/v1/platform/guardrails/reflection-sandbox | Execute agent action inside formal invariance sandbox | ReflectionSandboxRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assign»
- [ ] Execute agent action inside formal invariance sandbox
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-483 [P1] INT-483: REST · POST /api/v1/platform/recovery/restore/{point_id} · Restore to checkpoint

- **Source:** `GUI-UIX-requirements.md:1002-1002` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-483` | REST | `POST /api/v1/platform/recovery/restore/{point_id}` | Restore to checkpoint | `none`; params: point_id | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-483' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-483') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-483 | REST | POST /api/v1/platform/recovery/restore/{point_id} | Restore to checkpoint | none; params: point_id | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-510 [P1] INT-510: REST · POST /api/v1/platform/state/restore · Restore stream state from snapshot

- **Source:** `GUI-UIX-requirements.md:1029-1029` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-510` | REST | `POST /api/v1/platform/state/restore` | Restore stream state from snapshot | `StateRestoreRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `PARTIAL` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-510' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-510') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-510 | REST | POST /api/v1/platform/state/restore | Restore stream state from snapshot | StateRestoreRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | PARTIAL | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] Restore stream state from snapshot
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-511 [P1] INT-511: REST · POST /api/v1/platform/state/snapshot · Create durable snapshot of stream state

- **Source:** `GUI-UIX-requirements.md:1030-1030` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-511` | REST | `POST /api/v1/platform/state/snapshot` | Create durable snapshot of stream state | `StateSnapshotRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `PARTIAL` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-511' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-511') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-511 | REST | POST /api/v1/platform/state/snapshot | Create durable snapshot of stream state | StateSnapshotRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | PARTIAL | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] Create durable snapshot of stream state
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-522 [P1] INT-522: REST · POST /api/v1/platform/token-budget/allocate · Allocate dynamic token budget across stages

- **Source:** `GUI-UIX-requirements.md:1041-1041` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-522` | REST | `POST /api/v1/platform/token-budget/allocate` | Allocate dynamic token budget across stages | `TokenBudgetAllocateRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-522' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-522') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-522 | REST | POST /api/v1/platform/token-budget/allocate | Allocate dynamic token budget across stages | TokenBudgetAllocateRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] Allocate dynamic token budget across stages
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-523 [P1] INT-523: REST · POST /api/v1/platform/token-budget/consume · Record token consumption and check compression triggers

- **Source:** `GUI-UIX-requirements.md:1042-1042` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-523` | REST | `POST /api/v1/platform/token-budget/consume` | Record token consumption and check compression triggers | `TokenBudgetConsumeRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-523' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-523') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-523 | REST | POST /api/v1/platform/token-budget/consume | Record token consumption and check compression triggers | TokenBudgetConsumeRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] Record token consumption and check compression triggers
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-524 [P1] INT-524: REST · GET /api/v1/platform/token-budget/stats · Get token budget engine global stats

- **Source:** `GUI-UIX-requirements.md:1043-1043` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-524` | REST | `GET /api/v1/platform/token-budget/stats` | Get token budget engine global stats | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:1938` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-524' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-524') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-524 | REST | GET /api/v1/platform/token-budget/stats | Get token budget engine global stats | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:1938 | No primary screen assigned»
- [ ] Get token budget engine global stats
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-525 [P1] INT-525: REST · POST /api/v1/platform/token-formats/benchmark · Benchmark token reduction across all 7 formats vs JSON

- **Source:** `GUI-UIX-requirements.md:1044-1044` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-525` | REST | `POST /api/v1/platform/token-formats/benchmark` | Benchmark token reduction across all 7 formats vs JSON | `TokenFormatSerializeRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-525' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-525') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-525 | REST | POST /api/v1/platform/token-formats/benchmark | Benchmark token reduction across all 7 formats vs JSON | TokenFormatSerializeRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] Benchmark token reduction across all 7 formats vs JSON
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-526 [P1] INT-526: REST · POST /api/v1/platform/token-formats/deserialize · Deserialize payload from token format

- **Source:** `GUI-UIX-requirements.md:1045-1045` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-526` | REST | `POST /api/v1/platform/token-formats/deserialize` | Deserialize payload from token format | `TokenFormatDeserializeRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-526' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-526') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-526 | REST | POST /api/v1/platform/token-formats/deserialize | Deserialize payload from token format | TokenFormatDeserializeRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] Deserialize payload from token format
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-527 [P1] INT-527: REST · POST /api/v1/platform/token-formats/serialize · Serialize payload to token-efficient format

- **Source:** `GUI-UIX-requirements.md:1046-1046` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-527` | REST | `POST /api/v1/platform/token-formats/serialize` | Serialize payload to token-efficient format | `TokenFormatSerializeRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-527' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-527') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-527 | REST | POST /api/v1/platform/token-formats/serialize | Serialize payload to token-efficient format | TokenFormatSerializeRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] Serialize payload to token-efficient format
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-535 [P1] INT-535: REST · POST /api/v1/platform/tools/verify-attestation · Verify HMAC-SHA256 signature of tool attestation certificate

- **Source:** `GUI-UIX-requirements.md:1054-1054` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-535` | REST | `POST /api/v1/platform/tools/verify-attestation` | Verify HMAC-SHA256 signature of tool attestation certificate | `ToolVerifyAttestationRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-535' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-535') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-535 | REST | POST /api/v1/platform/tools/verify-attestation | Verify HMAC-SHA256 signature of tool attestation certificate | ToolVerifyAttestationRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen »
- [ ] Verify HMAC-SHA256 signature of tool attestation certificate
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-536 [P1] INT-536: REST · GET /api/v1/platform/verification/audit-trail · Retrieve tamper-evident verification audit trail

- **Source:** `GUI-UIX-requirements.md:1055-1055` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-536` | REST | `GET /api/v1/platform/verification/audit-trail` | Retrieve tamper-evident verification audit trail | `none`; params: limit | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:1866` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-536' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-536') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-536 | REST | GET /api/v1/platform/verification/audit-trail | Retrieve tamper-evident verification audit trail | none; params: limit | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:1866 | No primary screen assigned»
- [ ] Retrieve tamper-evident verification audit trail
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-544 [P1] INT-544: REST · POST /api/v1/privacy/classify · Classify

- **Source:** `GUI-UIX-requirements.md:1063-1063` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-544` | REST | `POST /api/v1/privacy/classify` | Classify | `ClassifyRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-544' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-544') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-544 | REST | POST /api/v1/privacy/classify | Classify | ClassifyRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-545 [P1] INT-545: REST · POST /api/v1/privacy/consents · Record Consent

- **Source:** `GUI-UIX-requirements.md:1064-1064` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-545` | REST | `POST /api/v1/privacy/consents` | Record Consent | `ConsentRecord`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-545' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-545') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-545 | REST | POST /api/v1/privacy/consents | Record Consent | ConsentRecord; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-546 [P1] INT-546: REST · GET /api/v1/privacy/consents/allowed · Consents Allowed

- **Source:** `GUI-UIX-requirements.md:1065-1065` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-546` | REST | `GET /api/v1/privacy/consents/allowed` | Consents Allowed | `none`; params: subject_id, purpose, tenant_id, source | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/privacy/router.py:106` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-546' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-546') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-546 | REST | GET /api/v1/privacy/consents/allowed | Consents Allowed | none; params: subject_id, purpose, tenant_id, source | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/privacy/router.py:106 | No primary screen assigned»
- [ ] none; params: subject_id, purpose, tenant_id, source
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-547 [P1] INT-547: REST · POST /api/v1/privacy/dsar/erase · Dsar Erase

- **Source:** `GUI-UIX-requirements.md:1066-1066` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-547` | REST | `POST /api/v1/privacy/dsar/erase` | Dsar Erase | `LocateRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-547' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-547') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-547 | REST | POST /api/v1/privacy/dsar/erase | Dsar Erase | LocateRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-548 [P1] INT-548: REST · POST /api/v1/privacy/dsar/locate · Dsar Locate

- **Source:** `GUI-UIX-requirements.md:1067-1067` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-548` | REST | `POST /api/v1/privacy/dsar/locate` | Dsar Locate | `LocateRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-548' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-548') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-548 | REST | POST /api/v1/privacy/dsar/locate | Dsar Locate | LocateRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-549 [P1] INT-549: REST · POST /api/v1/privacy/residency/validate · Residency Validate

- **Source:** `GUI-UIX-requirements.md:1068-1068` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-549` | REST | `POST /api/v1/privacy/residency/validate` | Residency Validate | `ResidencyRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-549' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-549') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-549 | REST | POST /api/v1/privacy/residency/validate | Residency Validate | ResidencyRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-550 [P1] INT-550: REST · POST /api/v1/privacy/retention/evaluate · Retention Evaluate

- **Source:** `GUI-UIX-requirements.md:1069-1069` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-550` | REST | `POST /api/v1/privacy/retention/evaluate` | Retention Evaluate | `RetentionRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-550' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-550') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-550 | REST | POST /api/v1/privacy/retention/evaluate | Retention Evaluate | RetentionRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-607 [P1] INT-607: REST · GET /api/v1/security/policy-matrix · Policy Matrix

- **Source:** `GUI-UIX-requirements.md:1126-1126` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-607` | REST | `GET /api/v1/security/policy-matrix` | Policy Matrix | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/authz/security_router.py:137` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-607' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-607') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-607 | REST | GET /api/v1/security/policy-matrix | Policy Matrix | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/authz/security_router.py:137 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-608 [P1] INT-608: REST · GET /api/v1/security/status · Security Status

- **Source:** `GUI-UIX-requirements.md:1127-1127` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-608` | REST | `GET /api/v1/security/status` | Security Status | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/authz/security_router.py:122` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-608' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-608') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-608 | REST | GET /api/v1/security/status | Security Status | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/authz/security_router.py:122 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-609 [P1] INT-609: REST · POST /api/v1/security/tokens/issue · Issue Token

- **Source:** `GUI-UIX-requirements.md:1128-1128` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-609` | REST | `POST /api/v1/security/tokens/issue` | Issue Token | `IssueTokenRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/authz/security_router.py:63` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-609' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-609') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-609 | REST | POST /api/v1/security/tokens/issue | Issue Token | IssueTokenRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/authz/security_router.py:63 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-610 [P1] INT-610: REST · POST /api/v1/security/tokens/revoke · Revoke Token

- **Source:** `GUI-UIX-requirements.md:1129-1129` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-610` | REST | `POST /api/v1/security/tokens/revoke` | Revoke Token | `RevokeTokenRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/authz/security_router.py:107` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-610' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-610') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-610 | REST | POST /api/v1/security/tokens/revoke | Revoke Token | RevokeTokenRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/authz/security_router.py:107 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-611 [P1] INT-611: REST · POST /api/v1/security/tokens/verify · Verify Token

- **Source:** `GUI-UIX-requirements.md:1130-1130` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-611` | REST | `POST /api/v1/security/tokens/verify` | Verify Token | `VerifyTokenRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/authz/security_router.py:85` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-611' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-611') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-611 | REST | POST /api/v1/security/tokens/verify | Verify Token | VerifyTokenRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/authz/security_router.py:85 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-665 [P1] INT-665: REST · GET /api/v1/tenancy/isolation/models · Isolation Models

- **Source:** `GUI-UIX-requirements.md:1184-1184` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-665` | REST | `GET /api/v1/tenancy/isolation/models` | Isolation Models | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:685` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-665' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-665') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-665 | REST | GET /api/v1/tenancy/isolation/models | Isolation Models | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:685 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-666 [P1] INT-666: REST · GET /api/v1/tenancy/isolation/placement · Get Placement

- **Source:** `GUI-UIX-requirements.md:1185-1185` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-666` | REST | `GET /api/v1/tenancy/isolation/placement` | Get Placement | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/reports/router.py:52` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-666' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-666') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-666 | REST | GET /api/v1/tenancy/isolation/placement | Get Placement | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/reports/router.py:52 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-667 [P1] INT-667: REST · POST /api/v1/tenancy/isolation/placement · Set Placement

- **Source:** `GUI-UIX-requirements.md:1186-1186` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-667` | REST | `POST /api/v1/tenancy/isolation/placement` | Set Placement | `object`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-667' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-667') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-667 | REST | POST /api/v1/tenancy/isolation/placement | Set Placement | object; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-718 [P1] INT-718: REST · GET /brain/learning/status · Get Learning Status

- **Source:** `GUI-UIX-requirements.md:1237-1237` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-718` | REST | `GET /brain/learning/status` | Get Learning Status | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/authz/security_router.py:122` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-718' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-718') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-718 | REST | GET /brain/learning/status | Get Learning Status | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/authz/security_router.py:122 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-725 [P1] INT-725: REST · POST /brain/llm/tokenize · Tokenize Text

- **Source:** `GUI-UIX-requirements.md:1244-1244` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-725` | REST | `POST /brain/llm/tokenize` | Tokenize Text | `LLMTokenizeRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:452` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-725' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-725') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-725 | REST | POST /brain/llm/tokenize | Tokenize Text | LLMTokenizeRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:452 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-002 [P2] INT-002: REST · POST /api/v1/admin/demo · Demo

- **Source:** `GUI-UIX-requirements.md:521-521` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-002` | REST | `POST /api/v1/admin/demo` | Demo | `none`; params: none | `none` | 202; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:1106` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-002 | REST | POST /api/v1/admin/demo | Demo | none; params: none | none | 202; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/main.py:1106 | No primary screen assigned»
- [ ] 202; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-003 [P2] INT-003: REST · GET /api/v1/admin/dlq · Dlq List

- **Source:** `GUI-UIX-requirements.md:522-522` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-003` | REST | `GET /api/v1/admin/dlq` | Dlq List | `none`; params: limit | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:1365` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-003 | REST | GET /api/v1/admin/dlq | Dlq List | none; params: limit | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/main.py:1365 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-004 [P2] INT-004: REST · POST /api/v1/admin/dlq/{event_id}/replay · Replay Dlq

- **Source:** `GUI-UIX-requirements.md:523-523` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-004` | REST | `POST /api/v1/admin/dlq/{event_id}/replay` | Replay Dlq | `none`; params: event_id | `none` | 202,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:1379` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-004 | REST | POST /api/v1/admin/dlq/{event_id}/replay | Replay Dlq | none; params: event_id | none | 202,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/main.py:1379 | No primary screen assigned»
- [ ] 202,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-005 [P2] INT-005: REST · POST /api/v1/admin/entities/{canonical_id}/delete · Delete Entity

- **Source:** `GUI-UIX-requirements.md:524-524` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-005` | REST | `POST /api/v1/admin/entities/{canonical_id}/delete` | Delete Entity | `none`; params: canonical_id | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | SCR-006
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-005 | REST | POST /api/v1/admin/entities/{canonical_id}/delete | Delete Entity | none; params: canonical_id | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | SCR-006»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-006 [P2] INT-006: REST · GET /api/v1/admin/event-consumers · Event Consumers

- **Source:** `GUI-UIX-requirements.md:525-525` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-006` | REST | `GET /api/v1/admin/event-consumers` | Event Consumers | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:597` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-006 | REST | GET /api/v1/admin/event-consumers | Event Consumers | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/main.py:597 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-007 [P2] INT-007: REST · POST /api/v1/admin/event-consumers/run · Run Event Consumers

- **Source:** `GUI-UIX-requirements.md:526-526` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-007` | REST | `POST /api/v1/admin/event-consumers/run` | Run Event Consumers | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:607` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-007 | REST | POST /api/v1/admin/event-consumers/run | Run Event Consumers | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/main.py:607 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-008 [P2] INT-008: REST · POST /api/v1/admin/gremlin · Admin Gremlin

- **Source:** `GUI-UIX-requirements.md:527-527` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-008` | REST | `POST /api/v1/admin/gremlin` | Admin Gremlin | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:1116` | SCR-011
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-008 | REST | POST /api/v1/admin/gremlin | Admin Gremlin | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/main.py:1116 | SCR-011»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-009 [P2] INT-009: REST · POST /api/v1/admin/ingestion/confluence · Ingest Confluence

- **Source:** `GUI-UIX-requirements.md:528-528` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-009` | REST | `POST /api/v1/admin/ingestion/confluence` | Ingest Confluence | `IncrementalSyncRequest`; params: none | `none` | 202,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:1090` | SCR-002, SCR-015
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-009 | REST | POST /api/v1/admin/ingestion/confluence | Ingest Confluence | IncrementalSyncRequest; params: none | none | 202,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/main.py:1090 | SCR-002, SCR-015»
- [ ] 202,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-010 [P2] INT-010: REST · POST /api/v1/admin/ingestion/files · Ingest File

- **Source:** `GUI-UIX-requirements.md:529-529` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-010` | REST | `POST /api/v1/admin/ingestion/files` | Ingest File | `none`; params: filename, source_id, ocr, dry_run | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/fileparse/api.py:69` | SCR-002, SCR-015
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-010 | REST | POST /api/v1/admin/ingestion/files | Ingest File | none; params: filename, source_id, ocr, dry_run | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/fileparse/api.py:69 | SCR-002, SCR-015»
- [ ] none; params: filename, source_id, ocr, dry_run
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-011 [P2] INT-011: REST · GET /api/v1/admin/ingestion/files/bundles/{bundle_id}/{artifact} · Download

- **Source:** `GUI-UIX-requirements.md:530-530` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-011` | REST | `GET /api/v1/admin/ingestion/files/bundles/{bundle_id}/{artifact}` | Download | `none`; params: bundle_id, artifact | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/fileparse/api.py:77` | SCR-002, SCR-015
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-011 | REST | GET /api/v1/admin/ingestion/files/bundles/{bundle_id}/{artifact} | Download | none; params: bundle_id, artifact | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/fileparse/api.py:77 | SCR-002, SCR-015»
- [ ] none; params: bundle_id, artifact
- [ ] 200,422; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-012 [P2] INT-012: REST · POST /api/v1/admin/ingestion/files/parse · Parse File

- **Source:** `GUI-UIX-requirements.md:531-531` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-012` | REST | `POST /api/v1/admin/ingestion/files/parse` | Parse File | `none`; params: filename, source_id, ocr | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/fileparse/api.py:62` | SCR-002, SCR-015
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-012 | REST | POST /api/v1/admin/ingestion/files/parse | Parse File | none; params: filename, source_id, ocr | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/fileparse/api.py:62 | SCR-002, SCR-015»
- [ ] none; params: filename, source_id, ocr
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

