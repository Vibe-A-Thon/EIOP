# EPIC-GUIUIX-UNTR-13: GUI-UIX-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 56 tasks, ~336.0 h, priorities {'P2': 56}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-INT-677 [P2] INT-677: REST · GET /api/v1/tenancy/metering/verify · Meter Verify

- **Source:** `GUI-UIX-requirements.md:1196-1196` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-677` | REST | `GET /api/v1/tenancy/metering/verify` | Meter Verify | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/reports/router.py:52` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-677' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-677') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-677 | REST | GET /api/v1/tenancy/metering/verify | Meter Verify | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/reports/router.py:52 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-678 [P2] INT-678: REST · GET /api/v1/tenancy/quotas · Get Quotas

- **Source:** `GUI-UIX-requirements.md:1197-1197` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-678` | REST | `GET /api/v1/tenancy/quotas` | Get Quotas | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/reports/router.py:52` | SCR-022
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-678' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-678') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-678 | REST | GET /api/v1/tenancy/quotas | Get Quotas | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/reports/router.py:52 | SCR-022»
- [ ] 200; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-679 [P2] INT-679: REST · POST /api/v1/tenancy/quotas/check · Quota Check

- **Source:** `GUI-UIX-requirements.md:1198-1198` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-679` | REST | `POST /api/v1/tenancy/quotas/check` | Quota Check | `object`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | SCR-022
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-679' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-679') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-679 | REST | POST /api/v1/tenancy/quotas/check | Quota Check | object; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | SCR-022»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-680 [P2] INT-680: REST · POST /api/v1/tenancy/quotas/consume · Quota Consume

- **Source:** `GUI-UIX-requirements.md:1199-1199` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-680` | REST | `POST /api/v1/tenancy/quotas/consume` | Quota Consume | `object`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | SCR-022
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-680' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-680') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-680 | REST | POST /api/v1/tenancy/quotas/consume | Quota Consume | object; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | SCR-022»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-681 [P2] INT-681: REST · POST /api/v1/tenancy/quotas/refund · Quota Refund

- **Source:** `GUI-UIX-requirements.md:1200-1200` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-681` | REST | `POST /api/v1/tenancy/quotas/refund` | Quota Refund | `object`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | SCR-022
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-681' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-681') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-681 | REST | POST /api/v1/tenancy/quotas/refund | Quota Refund | object; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | SCR-022»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-682 [P2] INT-682: REST · POST /api/v1/traceability · Traceability

- **Source:** `GUI-UIX-requirements.md:1201-1201` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-682` | REST | `POST /api/v1/traceability` | Traceability | `TraceabilityRequest`; params: none | `GraphResult` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:482` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-682' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-682') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-682 | REST | POST /api/v1/traceability | Traceability | TraceabilityRequest; params: none | GraphResult | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:482 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-683 [P2] INT-683: REST · GET /api/v1/truth/assertions/{subject_id}/{predicate} · Truth Assertion

- **Source:** `GUI-UIX-requirements.md:1202-1202` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-683` | REST | `GET /api/v1/truth/assertions/{subject_id}/{predicate}` | Truth Assertion | `none`; params: subject_id, predicate | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:535` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-683' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-683') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-683 | REST | GET /api/v1/truth/assertions/{subject_id}/{predicate} | Truth Assertion | none; params: subject_id, predicate | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:535 | No primary screen assigned»
- [ ] none; params: subject_id, predicate
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-684 [P2] INT-684: REST · POST /api/v1/truth/claims · Truth Add Claim

- **Source:** `GUI-UIX-requirements.md:1203-1203` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-684` | REST | `POST /api/v1/truth/claims` | Truth Add Claim | `Claim`; params: none | `Claim` | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:496` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-684' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-684') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-684 | REST | POST /api/v1/truth/claims | Truth Add Claim | Claim; params: none | Claim | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:496 | No primary screen assigned»
- [ ] 201,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-685 [P2] INT-685: REST · GET /api/v1/truth/contradictions · Truth Contradictions

- **Source:** `GUI-UIX-requirements.md:1204-1204` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-685` | REST | `GET /api/v1/truth/contradictions` | Truth Contradictions | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:504` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-685' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-685') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-685 | REST | GET /api/v1/truth/contradictions | Truth Contradictions | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:504 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-686 [P2] INT-686: REST · GET /api/v1/truth/explain/{subject_id}/{predicate} · Truth Explain

- **Source:** `GUI-UIX-requirements.md:1205-1205` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-686` | REST | `GET /api/v1/truth/explain/{subject_id}/{predicate}` | Truth Explain | `none`; params: subject_id, predicate | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:546` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-686' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-686') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-686 | REST | GET /api/v1/truth/explain/{subject_id}/{predicate} | Truth Explain | none; params: subject_id, predicate | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:546 | No primary screen assigned»
- [ ] none; params: subject_id, predicate
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-687 [P2] INT-687: REST · GET /api/v1/truth/export · Truth Export

- **Source:** `GUI-UIX-requirements.md:1206-1206` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-687` | REST | `GET /api/v1/truth/export` | Truth Export | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `PARTIAL` | `apps/api/extended.py:551` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-687' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-687') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-687 | REST | GET /api/v1/truth/export | Truth Export | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | PARTIAL | apps/api/extended.py:551 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-688 [P2] INT-688: REST · POST /api/v1/truth/resolve · Truth Resolve

- **Source:** `GUI-UIX-requirements.md:1207-1207` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-688` | REST | `POST /api/v1/truth/resolve` | Truth Resolve | `TruthResolveRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:519` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-688' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-688') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-688 | REST | POST /api/v1/truth/resolve | Truth Resolve | TruthResolveRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:519 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-689 [P2] INT-689: REST · POST /api/v1/twin/business/capabilities · Create Capability

- **Source:** `GUI-UIX-requirements.md:1208-1208` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-689` | REST | `POST /api/v1/twin/business/capabilities` | Create Capability | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:920` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-689' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-689') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-689 | REST | POST /api/v1/twin/business/capabilities | Create Capability | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:920 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-690 [P2] INT-690: REST · GET /api/v1/twin/business/chain/{objective_cid} · Intent Chain

- **Source:** `GUI-UIX-requirements.md:1209-1209` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-690` | REST | `GET /api/v1/twin/business/chain/{objective_cid}` | Intent Chain | `none`; params: objective_cid | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/reports/router.py:52` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-690' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-690') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-690 | REST | GET /api/v1/twin/business/chain/{objective_cid} | Intent Chain | none; params: objective_cid | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/reports/router.py:52 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-691 [P2] INT-691: REST · POST /api/v1/twin/business/link · Link Entity To Capability

- **Source:** `GUI-UIX-requirements.md:1210-1210` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-691` | REST | `POST /api/v1/twin/business/link` | Link Entity To Capability | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:936` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-691' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-691') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-691 | REST | POST /api/v1/twin/business/link | Link Entity To Capability | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:936 | No primary screen assigned»
- [ ] Link Entity To Capability
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-692 [P2] INT-692: REST · POST /api/v1/twin/business/objectives · Create Objective

- **Source:** `GUI-UIX-requirements.md:1211-1211` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-692` | REST | `POST /api/v1/twin/business/objectives` | Create Objective | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:904` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-692' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-692') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-692 | REST | POST /api/v1/twin/business/objectives | Create Objective | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:904 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-693 [P2] INT-693: REST · GET /api/v1/twin/business/reverse-impact/{service_cid} · Business Reverse Impact

- **Source:** `GUI-UIX-requirements.md:1212-1212` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-693` | REST | `GET /api/v1/twin/business/reverse-impact/{service_cid}` | Business Reverse Impact | `none`; params: service_cid | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/reports/router.py:52` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-693' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-693') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-693 | REST | GET /api/v1/twin/business/reverse-impact/{service_cid} | Business Reverse Impact | none; params: service_cid | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/reports/router.py:52 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-694 [P2] INT-694: REST · GET /api/v1/twin/classify · Twin Classify

- **Source:** `GUI-UIX-requirements.md:1213-1213` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-694` | REST | `GET /api/v1/twin/classify` | Twin Classify | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:958` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-694' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-694') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-694 | REST | GET /api/v1/twin/classify | Twin Classify | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:958 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-695 [P2] INT-695: REST · GET /api/v1/twin/coverage · Twin Coverage

- **Source:** `GUI-UIX-requirements.md:1214-1214` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-695` | REST | `GET /api/v1/twin/coverage` | Twin Coverage | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:963` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-695' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-695') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-695 | REST | GET /api/v1/twin/coverage | Twin Coverage | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:963 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-696 [P2] INT-696: REST · POST /api/v1/twin/decisions/extract · Extract Decisions

- **Source:** `GUI-UIX-requirements.md:1215-1215` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-696` | REST | `POST /api/v1/twin/decisions/extract` | Extract Decisions | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:896` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-696' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-696') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-696 | REST | POST /api/v1/twin/decisions/extract | Extract Decisions | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:896 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-697 [P2] INT-697: REST · POST /api/v1/twin/decisions/ingest · Ingest Decision Endpoint

- **Source:** `GUI-UIX-requirements.md:1216-1216` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-697` | REST | `POST /api/v1/twin/decisions/ingest` | Ingest Decision Endpoint | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:876` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-697' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-697') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-697 | REST | POST /api/v1/twin/decisions/ingest | Ingest Decision Endpoint | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:876 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-698 [P2] INT-698: REST · GET /api/v1/twin/decisions/{entity_cid} · Decisions For Entity

- **Source:** `GUI-UIX-requirements.md:1217-1217` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-698` | REST | `GET /api/v1/twin/decisions/{entity_cid}` | Decisions For Entity | `none`; params: entity_cid | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/reports/router.py:52` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-698' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-698') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-698 | REST | GET /api/v1/twin/decisions/{entity_cid} | Decisions For Entity | none; params: entity_cid | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/reports/router.py:52 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-699 [P2] INT-699: REST · GET /api/v1/twin/missing-links · Twin Missing Links

- **Source:** `GUI-UIX-requirements.md:1218-1218` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-699` | REST | `GET /api/v1/twin/missing-links` | Twin Missing Links | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:968` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-699' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-699') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-699 | REST | GET /api/v1/twin/missing-links | Twin Missing Links | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:968 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-700 [P2] INT-700: REST · GET /api/v1/twin/test-intelligence/mappings · Test Code Mappings

- **Source:** `GUI-UIX-requirements.md:1219-1219` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-700` | REST | `GET /api/v1/twin/test-intelligence/mappings` | Test Code Mappings | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:858` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-700' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-700') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-700 | REST | GET /api/v1/twin/test-intelligence/mappings | Test Code Mappings | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:858 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-701 [P2] INT-701: REST · GET /api/v1/twin/test-intelligence/runs · Test Run Builds

- **Source:** `GUI-UIX-requirements.md:1220-1220` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-701` | REST | `GET /api/v1/twin/test-intelligence/runs` | Test Run Builds | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:863` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-701' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-701') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-701 | REST | GET /api/v1/twin/test-intelligence/runs | Test Run Builds | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:863 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-702 [P2] INT-702: REST · POST /api/v1/twin/test-intelligence/select · Select Tests

- **Source:** `GUI-UIX-requirements.md:1221-1221` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-702` | REST | `POST /api/v1/twin/test-intelligence/select` | Select Tests | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:868` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-702' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-702') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-702 | REST | POST /api/v1/twin/test-intelligence/select | Select Tests | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:868 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-703 [P2] INT-703: REST · GET /api/v1/validation/runs · Validation Runs

- **Source:** `GUI-UIX-requirements.md:1222-1222` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-703` | REST | `GET /api/v1/validation/runs` | Validation Runs | `none`; params: limit | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:1463` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-703' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-703') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-703 | REST | GET /api/v1/validation/runs | Validation Runs | none; params: limit | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/main.py:1463 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-704 [P2] INT-704: REST · POST /api/v1/whatif/execute · Whatif Execute

- **Source:** `GUI-UIX-requirements.md:1223-1223` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-704` | REST | `POST /api/v1/whatif/execute` | Whatif Execute | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1263` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-704' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-704') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-704 | REST | POST /api/v1/whatif/execute | Whatif Execute | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1263 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-705 [P2] INT-705: REST · POST /api/v1/whatif/plan · Whatif Plan

- **Source:** `GUI-UIX-requirements.md:1224-1224` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-705` | REST | `POST /api/v1/whatif/plan` | Whatif Plan | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1254` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-705' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-705') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-705 | REST | POST /api/v1/whatif/plan | Whatif Plan | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1254 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-706 [P2] INT-706: REST · POST /api/v1/xai/certify-decision · Certify Decision

- **Source:** `GUI-UIX-requirements.md:1225-1225` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-706` | REST | `POST /api/v1/xai/certify-decision` | Certify Decision | `CertifyDecisionRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/enterprise/advanced_router.py:140` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-706' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-706') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-706 | REST | POST /api/v1/xai/certify-decision | Certify Decision | CertifyDecisionRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/enterprise/advanced_router.py:140 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-707 [P2] INT-707: REST · POST /api/v1/xai/verify-certificate · Verify Certificate

- **Source:** `GUI-UIX-requirements.md:1226-1226` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-707` | REST | `POST /api/v1/xai/verify-certificate` | Verify Certificate | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/enterprise/advanced_router.py:151` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-707' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-707') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-707 | REST | POST /api/v1/xai/verify-certificate | Verify Certificate | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/enterprise/advanced_router.py:151 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-708 [P2] INT-708: REST · GET /brain/agents · List Agents

- **Source:** `GUI-UIX-requirements.md:1227-1227` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-708` | REST | `GET /brain/agents` | List Agents | `none`; params: none | `array` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:290` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-708' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-708') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-708 | REST | GET /brain/agents | List Agents | none; params: none | array | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:290 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-709 [P2] INT-709: REST · GET /brain/approaches · List Query Approaches

- **Source:** `GUI-UIX-requirements.md:1228-1228` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-709` | REST | `GET /brain/approaches` | List Query Approaches | `none`; params: none | `array` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:193` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-709' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-709') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-709 | REST | GET /brain/approaches | List Query Approaches | none; params: none | array | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:193 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-710 [P2] INT-710: REST · POST /brain/ask · Ask Brain

- **Source:** `GUI-UIX-requirements.md:1229-1229` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-710` | REST | `POST /brain/ask` | Ask Brain | `BrainAskRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:117` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-710' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-710') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-710 | REST | POST /brain/ask | Ask Brain | BrainAskRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:117 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-711 [P2] INT-711: REST · GET /brain/databases · List Databases

- **Source:** `GUI-UIX-requirements.md:1230-1230` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-711` | REST | `GET /brain/databases` | List Databases | `none`; params: none | `array` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:307` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-711' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-711') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-711 | REST | GET /brain/databases | List Databases | none; params: none | array | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:307 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-712 [P2] INT-712: REST · GET /brain/dialects · List Dialects

- **Source:** `GUI-UIX-requirements.md:1231-1231` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-712` | REST | `GET /brain/dialects` | List Dialects | `none`; params: none | `array` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:301` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-712' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-712') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-712 | REST | GET /brain/dialects | List Dialects | none; params: none | array | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:301 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-713 [P2] INT-713: REST · POST /brain/induce · Induce Ontology

- **Source:** `GUI-UIX-requirements.md:1232-1232` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-713` | REST | `POST /brain/induce` | Induce Ontology | `InduceRequest`; params: none | `array` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:312` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-713' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-713') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-713 | REST | POST /brain/induce | Induce Ontology | InduceRequest; params: none | array | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:312 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-714 [P2] INT-714: REST · POST /brain/intelligent-query · Intelligent Query

- **Source:** `GUI-UIX-requirements.md:1233-1233` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-714` | REST | `POST /brain/intelligent-query` | Intelligent Query | `IntelligentQueryRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:100` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-714' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-714') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-714 | REST | POST /brain/intelligent-query | Intelligent Query | IntelligentQueryRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:100 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-715 [P2] INT-715: REST · POST /brain/learning/load · Load Learning State

- **Source:** `GUI-UIX-requirements.md:1234-1234` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-715` | REST | `POST /brain/learning/load` | Load Learning State | `none`; params: directory | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:211` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-715' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-715') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-715 | REST | POST /brain/learning/load | Load Learning State | none; params: directory | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:211 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-716 [P2] INT-716: REST · GET /brain/learning/policy · Get Learned Policy

- **Source:** `GUI-UIX-requirements.md:1235-1235` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-716` | REST | `GET /brain/learning/policy` | Get Learned Policy | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:218` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-716' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-716') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-716 | REST | GET /brain/learning/policy | Get Learned Policy | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:218 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-717 [P2] INT-717: REST · POST /brain/learning/save · Save Learning State

- **Source:** `GUI-UIX-requirements.md:1236-1236` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-717` | REST | `POST /brain/learning/save` | Save Learning State | `none`; params: directory | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:204` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-717' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-717') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-717 | REST | POST /brain/learning/save | Save Learning State | none; params: directory | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:204 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-719 [P2] INT-719: REST · POST /brain/learning/train · Train Learning Engine

- **Source:** `GUI-UIX-requirements.md:1238-1238` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-719` | REST | `POST /brain/learning/train` | Train Learning Engine | `LearningTrainRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:224` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-719' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-719') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-719 | REST | POST /brain/learning/train | Train Learning Engine | LearningTrainRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:224 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-720 [P2] INT-720: REST · POST /brain/llm/embed · Embed Text

- **Source:** `GUI-UIX-requirements.md:1239-1239` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-720` | REST | `POST /brain/llm/embed` | Embed Text | `LLMEmbedRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:461` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-720' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-720') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-720 | REST | POST /brain/llm/embed | Embed Text | LLMEmbedRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:461 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-721 [P2] INT-721: REST · POST /brain/llm/explain · Explain Llm

- **Source:** `GUI-UIX-requirements.md:1240-1240` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-721` | REST | `POST /brain/llm/explain` | Explain Llm | `LLMGenerateRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:440` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-721' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-721') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-721 | REST | POST /brain/llm/explain | Explain Llm | LLMGenerateRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:440 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-722 [P2] INT-722: REST · POST /brain/llm/generate · Generate Llm

- **Source:** `GUI-UIX-requirements.md:1241-1241` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-722` | REST | `POST /brain/llm/generate` | Generate Llm | `LLMGenerateRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:363` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-722' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-722') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-722 | REST | POST /brain/llm/generate | Generate Llm | LLMGenerateRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:363 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-723 [P2] INT-723: REST · GET /brain/llm/models · List Llm Models

- **Source:** `GUI-UIX-requirements.md:1242-1242` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-723` | REST | `GET /brain/llm/models` | List Llm Models | `none`; params: none | `array` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:343` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-723' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-723') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-723 | REST | GET /brain/llm/models | List Llm Models | none; params: none | array | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:343 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-724 [P2] INT-724: REST · POST /brain/llm/stream · Stream Llm

- **Source:** `GUI-UIX-requirements.md:1243-1243` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-724` | REST | `POST /brain/llm/stream` | Stream Llm | `LLMGenerateRequest`; params: none | `array` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `PARTIAL` | `packages/eoip/brain/router.py:418` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-724' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-724') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-724 | REST | POST /brain/llm/stream | Stream Llm | LLMGenerateRequest; params: none | array | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | PARTIAL | packages/eoip/brain/router.py:418 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-726 [P2] INT-726: REST · GET /brain/loops · List Loops

- **Source:** `GUI-UIX-requirements.md:1245-1245` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-726` | REST | `GET /brain/loops` | List Loops | `none`; params: none | `array` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:285` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-726' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-726') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-726 | REST | GET /brain/loops | List Loops | none; params: none | array | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:285 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-727 [P2] INT-727: REST · POST /brain/narrate · Narrate Brain Inquiry

- **Source:** `GUI-UIX-requirements.md:1246-1246` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-727` | REST | `POST /brain/narrate` | Narrate Brain Inquiry | `CognitiveNarrateRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:178` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-727' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-727') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-727 | REST | POST /brain/narrate | Narrate Brain Inquiry | CognitiveNarrateRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:178 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-728 [P2] INT-728: REST · POST /brain/query · Query Brain Report

- **Source:** `GUI-UIX-requirements.md:1247-1247` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-728` | REST | `POST /brain/query` | Query Brain Report | `BrainQueryReportRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:157` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-728' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-728') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-728 | REST | POST /brain/query | Query Brain Report | BrainQueryReportRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:157 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-729 [P2] INT-729: REST · GET /brain/rag-modes · List Rag Modes

- **Source:** `GUI-UIX-requirements.md:1248-1248` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-729` | REST | `GET /brain/rag-modes` | List Rag Modes | `none`; params: none | `array` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:296` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-729' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-729') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-729 | REST | GET /brain/rag-modes | List Rag Modes | none; params: none | array | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:296 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-730 [P2] INT-730: REST · GET /brain/snapshot · Get Brain Snapshot

- **Source:** `GUI-UIX-requirements.md:1249-1249` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-730` | REST | `GET /brain/snapshot` | Get Brain Snapshot | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:329` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-730' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-730') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-730 | REST | GET /brain/snapshot | Get Brain Snapshot | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:329 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-731 [P2] INT-731: REST · GET /brain/telemetry · Get Telemetry

- **Source:** `GUI-UIX-requirements.md:1250-1250` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-731` | REST | `GET /brain/telemetry` | Get Telemetry | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:279` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-731' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-731') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-731 | REST | GET /brain/telemetry | Get Telemetry | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:279 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-732 [P2] INT-732: REST · GET /health/live · Live

- **Source:** `GUI-UIX-requirements.md:1251-1251` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-732` | REST | `GET /health/live` | Live | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:318` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-732' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-732') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-732 | REST | GET /health/live | Live | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:318 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-733 [P2] INT-733: REST · GET /health/ready · Ready

- **Source:** `GUI-UIX-requirements.md:1252-1252` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-733` | REST | `GET /health/ready` | Ready | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:322` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-733' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-733') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-733 | REST | GET /health/ready | Ready | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:322 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-734 [P2] INT-734: REST · GET /metrics · Metrics Render

- **Source:** `GUI-UIX-requirements.md:1253-1253` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-734` | REST | `GET /metrics` | Metrics Render | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:1358` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-734' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-734') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-734 | REST | GET /metrics | Metrics Render | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:1358 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

