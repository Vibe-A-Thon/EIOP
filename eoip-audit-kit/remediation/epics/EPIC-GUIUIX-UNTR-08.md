# EPIC-GUIUIX-UNTR-08: GUI-UIX-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 60 tasks, ~360.0 h, priorities {'P2': 60}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-INT-347 [P2] INT-347: REST · GET /api/v1/ontology/export · Ontology Export

- **Source:** `GUI-UIX-requirements.md:866-866` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-347` | REST | `GET /api/v1/ontology/export` | Ontology Export | `none`; params: limit | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `PARTIAL` | `apps/api/main.py:527` | SCR-012, SCR-013
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-347' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-347') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-347 | REST | GET /api/v1/ontology/export | Ontology Export | none; params: limit | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | PARTIAL | apps/api/main.py:527 | SCR-012, SCR-013»
- [ ] 200,422; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-348 [P2] INT-348: REST · GET /api/v1/ontology/gitops/branches · List Branches

- **Source:** `GUI-UIX-requirements.md:867-867` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-348` | REST | `GET /api/v1/ontology/gitops/branches` | List Branches | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ontology/gitops_router.py:162` | SCR-012, SCR-013
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-348' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-348') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-348 | REST | GET /api/v1/ontology/gitops/branches | List Branches | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/ontology/gitops_router.py:162 | SCR-012, SCR-013»
- [ ] 200; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-349 [P2] INT-349: REST · POST /api/v1/ontology/gitops/branches · Create Branch

- **Source:** `GUI-UIX-requirements.md:868-868` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-349` | REST | `POST /api/v1/ontology/gitops/branches` | Create Branch | `CreateBranchRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | SCR-013
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-349' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-349') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-349 | REST | POST /api/v1/ontology/gitops/branches | Create Branch | CreateBranchRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | SCR-013»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-350 [P2] INT-350: REST · POST /api/v1/ontology/gitops/branches/commit · Commit Branch

- **Source:** `GUI-UIX-requirements.md:869-869` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-350` | REST | `POST /api/v1/ontology/gitops/branches/commit` | Commit Branch | `CommitManifestRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | SCR-013
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-350' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-350') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-350 | REST | POST /api/v1/ontology/gitops/branches/commit | Commit Branch | CommitManifestRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | SCR-013»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-351 [P2] INT-351: REST · POST /api/v1/ontology/gitops/diff · Generate Diff

- **Source:** `GUI-UIX-requirements.md:870-870` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-351` | REST | `POST /api/v1/ontology/gitops/diff` | Generate Diff | `eoip__ontology__gitops_router__DiffRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/config/router.py:168` | SCR-013
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-351' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-351') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-351 | REST | POST /api/v1/ontology/gitops/diff | Generate Diff | eoip__ontology__gitops_router__DiffRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/config/router.py:168 | SCR-013»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-352 [P2] INT-352: REST · POST /api/v1/ontology/gitops/impact · Impact Analysis

- **Source:** `GUI-UIX-requirements.md:871-871` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-352` | REST | `POST /api/v1/ontology/gitops/impact` | Impact Analysis | `eoip__ontology__gitops_router__ImpactRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-352' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-352') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-352 | REST | POST /api/v1/ontology/gitops/impact | Impact Analysis | eoip__ontology__gitops_router__ImpactRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-353 [P2] INT-353: REST · POST /api/v1/ontology/gitops/migration · Generate Migration

- **Source:** `GUI-UIX-requirements.md:872-872` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-353` | REST | `POST /api/v1/ontology/gitops/migration` | Generate Migration | `MigrationGenRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-353' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-353') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-353 | REST | POST /api/v1/ontology/gitops/migration | Generate Migration | MigrationGenRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-354 [P2] INT-354: REST · POST /api/v1/ontology/gitops/package-release · Package Release

- **Source:** `GUI-UIX-requirements.md:873-873` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-354` | REST | `POST /api/v1/ontology/gitops/package-release` | Package Release | `PackageReleaseRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-354' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-354') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-354 | REST | POST /api/v1/ontology/gitops/package-release | Package Release | PackageReleaseRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-355 [P2] INT-355: REST · POST /api/v1/ontology/gitops/prs · Create Pr

- **Source:** `GUI-UIX-requirements.md:874-874` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-355` | REST | `POST /api/v1/ontology/gitops/prs` | Create Pr | `CreatePRRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-355' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-355') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-355 | REST | POST /api/v1/ontology/gitops/prs | Create Pr | CreatePRRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-356 [P2] INT-356: REST · GET /api/v1/ontology/gitops/prs · List Prs

- **Source:** `GUI-UIX-requirements.md:875-875` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-356` | REST | `GET /api/v1/ontology/gitops/prs` | List Prs | `none`; params: status | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ontology/gitops_router.py:187` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-356' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-356') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-356 | REST | GET /api/v1/ontology/gitops/prs | List Prs | none; params: status | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/ontology/gitops_router.py:187 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-357 [P2] INT-357: REST · POST /api/v1/ontology/gitops/prs/{pr_id}/merge · Merge Pr

- **Source:** `GUI-UIX-requirements.md:876-876` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-357` | REST | `POST /api/v1/ontology/gitops/prs/{pr_id}/merge` | Merge Pr | `MergePRRequest`; params: pr_id | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-357' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-357') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-357 | REST | POST /api/v1/ontology/gitops/prs/{pr_id}/merge | Merge Pr | MergePRRequest; params: pr_id | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-358 [P2] INT-358: REST · POST /api/v1/ontology/gitops/prs/{pr_id}/review · Review Pr

- **Source:** `GUI-UIX-requirements.md:877-877` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-358` | REST | `POST /api/v1/ontology/gitops/prs/{pr_id}/review` | Review Pr | `ReviewPRRequest`; params: pr_id | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-358' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-358') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-358 | REST | POST /api/v1/ontology/gitops/prs/{pr_id}/review | Review Pr | ReviewPRRequest; params: pr_id | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-360 [P2] INT-360: REST · POST /api/v1/ontology/gitops/validate · Validate Ontology

- **Source:** `GUI-UIX-requirements.md:879-879` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-360` | REST | `POST /api/v1/ontology/gitops/validate` | Validate Ontology | `eoip__ontology__gitops_router__DiffRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-360' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-360') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-360 | REST | POST /api/v1/ontology/gitops/validate | Validate Ontology | eoip__ontology__gitops_router__DiffRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-361 [P2] INT-361: REST · POST /api/v1/ontology/import · Ontology Import

- **Source:** `GUI-UIX-requirements.md:880-880` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-361` | REST | `POST /api/v1/ontology/import` | Ontology Import | `object`; params: clear | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:535` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-361' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-361') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-361 | REST | POST /api/v1/ontology/import | Ontology Import | object; params: clear | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/main.py:535 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-362 [P2] INT-362: REST · GET /api/v1/ontology/packs · Ontology List Packs

- **Source:** `GUI-UIX-requirements.md:881-881` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-362` | REST | `GET /api/v1/ontology/packs` | Ontology List Packs | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:1244` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-362' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-362') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-362 | REST | GET /api/v1/ontology/packs | Ontology List Packs | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:1244 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-363 [P2] INT-363: REST · GET /api/v1/ontology/packs/{name} · Ontology Pack Detail

- **Source:** `GUI-UIX-requirements.md:882-882` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-363` | REST | `GET /api/v1/ontology/packs/{name}` | Ontology Pack Detail | `none`; params: name | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:1251` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-363' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-363') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-363 | REST | GET /api/v1/ontology/packs/{name} | Ontology Pack Detail | none; params: name | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:1251 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-364 [P2] INT-364: REST · POST /api/v1/ontology/proposals · Generate Ontology Proposals

- **Source:** `GUI-UIX-requirements.md:883-883` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-364` | REST | `POST /api/v1/ontology/proposals` | Generate Ontology Proposals | `none`; params: none | `none` | 201; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:1297` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-364' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-364') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-364 | REST | POST /api/v1/ontology/proposals | Generate Ontology Proposals | none; params: none | none | 201; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/main.py:1297 | No primary screen assigned»
- [ ] 201; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-365 [P2] INT-365: REST · GET /api/v1/ontology/shacl · Ontology Shacl

- **Source:** `GUI-UIX-requirements.md:884-884` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-365` | REST | `GET /api/v1/ontology/shacl` | Ontology Shacl | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:542` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-365' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-365') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-365 | REST | GET /api/v1/ontology/shacl | Ontology Shacl | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/main.py:542 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-366 [P2] INT-366: REST · GET /api/v1/ontology/validate · Ontology Validate

- **Source:** `GUI-UIX-requirements.md:885-885` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-366` | REST | `GET /api/v1/ontology/validate` | Ontology Validate | `none`; params: limit | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:549` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-366' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-366') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-366 | REST | GET /api/v1/ontology/validate | Ontology Validate | none; params: limit | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/main.py:549 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-367 [P2] INT-367: REST · GET /api/v1/ops/ha-topology · Ops Ha Topology

- **Source:** `GUI-UIX-requirements.md:886-886` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-367` | REST | `GET /api/v1/ops/ha-topology` | Ops Ha Topology | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:1337` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-367' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-367') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-367 | REST | GET /api/v1/ops/ha-topology | Ops Ha Topology | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:1337 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-368 [P2] INT-368: REST · POST /api/v1/ops/helm-summary · Ops Helm Summary

- **Source:** `GUI-UIX-requirements.md:887-887` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-368` | REST | `POST /api/v1/ops/helm-summary` | Ops Helm Summary | `inline`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:1351` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-368' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-368') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-368 | REST | POST /api/v1/ops/helm-summary | Ops Helm Summary | inline; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:1351 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-369 [P2] INT-369: REST · GET /api/v1/ops/preflight · Ops Preflight

- **Source:** `GUI-UIX-requirements.md:888-888` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-369` | REST | `GET /api/v1/ops/preflight` | Ops Preflight | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:1305` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-369' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-369') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-369 | REST | GET /api/v1/ops/preflight | Ops Preflight | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:1305 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-370 [P2] INT-370: REST · POST /api/v1/ops/shard-plan · Ops Shard Plan

- **Source:** `GUI-UIX-requirements.md:889-889` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-370` | REST | `POST /api/v1/ops/shard-plan` | Ops Shard Plan | `ShardPlanRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:1342` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-370' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-370') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-370 | REST | POST /api/v1/ops/shard-plan | Ops Shard Plan | ShardPlanRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:1342 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-371 [P2] INT-371: REST · GET /api/v1/ops/support-bundle · Ops Support Bundle

- **Source:** `GUI-UIX-requirements.md:890-890` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-371` | REST | `GET /api/v1/ops/support-bundle` | Ops Support Bundle | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:1329` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-371' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-371') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-371 | REST | GET /api/v1/ops/support-bundle | Ops Support Bundle | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:1329 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-372 [P2] INT-372: REST · POST /api/v1/ops/upgrade-plan · Ops Upgrade Plan

- **Source:** `GUI-UIX-requirements.md:891-891` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-372` | REST | `POST /api/v1/ops/upgrade-plan` | Ops Upgrade Plan | `UpgradePlanRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:1318` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-372' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-372') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-372 | REST | POST /api/v1/ops/upgrade-plan | Ops Upgrade Plan | UpgradePlanRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:1318 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-373 [P2] INT-373: REST · POST /api/v1/path · Find Path

- **Source:** `GUI-UIX-requirements.md:892-892` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-373` | REST | `POST /api/v1/path` | Find Path | `PathRequest`; params: none | `GraphResult` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:414` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-373' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-373') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-373 | REST | POST /api/v1/path | Find Path | PathRequest; params: none | GraphResult | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:414 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-374 [P2] INT-374: REST · GET /api/v1/pipeline/status · Pipeline Status

- **Source:** `GUI-UIX-requirements.md:893-893` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-374` | REST | `GET /api/v1/pipeline/status` | Pipeline Status | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1667` | SCR-017
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-374' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-374') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-374 | REST | GET /api/v1/pipeline/status | Pipeline Status | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1667 | SCR-017»
- [ ] 200; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-375 [P2] INT-375: REST · POST /api/v1/platform/aiml/hallucination/check · Check for hallucinations

- **Source:** `GUI-UIX-requirements.md:894-894` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-375` | REST | `POST /api/v1/platform/aiml/hallucination/check` | Check for hallucinations | `HallucinationCheckRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-375' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-375') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-375 | REST | POST /api/v1/platform/aiml/hallucination/check | Check for hallucinations | HallucinationCheckRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-376 [P2] INT-376: REST · GET /api/v1/platform/aiml/hallucination/stats · Hallucination detection stats

- **Source:** `GUI-UIX-requirements.md:895-895` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-376` | REST | `GET /api/v1/platform/aiml/hallucination/stats` | Hallucination detection stats | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:1177` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-376' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-376') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-376 | REST | GET /api/v1/platform/aiml/hallucination/stats | Hallucination detection stats | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:1177 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-377 [P2] INT-377: REST · POST /api/v1/platform/aiml/rlhf/preference · Add RLHF preference pair

- **Source:** `GUI-UIX-requirements.md:896-896` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-377` | REST | `POST /api/v1/platform/aiml/rlhf/preference` | Add RLHF preference pair | `RLHFPreferenceRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-377' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-377') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-377 | REST | POST /api/v1/platform/aiml/rlhf/preference | Add RLHF preference pair | RLHFPreferenceRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] Add RLHF preference pair
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-378 [P2] INT-378: REST · POST /api/v1/platform/aiml/rlhf/reward · Compute reward score

- **Source:** `GUI-UIX-requirements.md:897-897` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-378` | REST | `POST /api/v1/platform/aiml/rlhf/reward` | Compute reward score | `RewardScoreRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-378' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-378') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-378 | REST | POST /api/v1/platform/aiml/rlhf/reward | Compute reward score | RewardScoreRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-379 [P2] INT-379: REST · GET /api/v1/platform/aiml/rlhf/stats · RLHF statistics

- **Source:** `GUI-UIX-requirements.md:898-898` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-379` | REST | `GET /api/v1/platform/aiml/rlhf/stats` | RLHF statistics | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:1162` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-379' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-379') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-379 | REST | GET /api/v1/platform/aiml/rlhf/stats | RLHF statistics | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:1162 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-380 [P2] INT-380: REST · GET /api/v1/platform/aiml/stats · AI/ML Ops unified statistics

- **Source:** `GUI-UIX-requirements.md:899-899` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-380` | REST | `GET /api/v1/platform/aiml/stats` | AI/ML Ops unified statistics | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:1234` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-380' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-380') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-380 | REST | GET /api/v1/platform/aiml/stats | AI/ML Ops unified statistics | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:1234 | No primary screen assigned»
- [ ] AI/ML Ops unified statistics
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-381 [P2] INT-381: REST · GET /api/v1/platform/aiml/temperature/best · Best sampling config

- **Source:** `GUI-UIX-requirements.md:900-900` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-381` | REST | `GET /api/v1/platform/aiml/temperature/best` | Best sampling config | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:1206` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-381' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-381') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-381 | REST | GET /api/v1/platform/aiml/temperature/best | Best sampling config | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:1206 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-382 [P2] INT-382: REST · POST /api/v1/platform/aiml/temperature/experiment · Create sampling experiment

- **Source:** `GUI-UIX-requirements.md:901-901` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-382` | REST | `POST /api/v1/platform/aiml/temperature/experiment` | Create sampling experiment | `SamplingExperimentRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-382' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-382') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-382 | REST | POST /api/v1/platform/aiml/temperature/experiment | Create sampling experiment | SamplingExperimentRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-383 [P2] INT-383: REST · POST /api/v1/platform/aiml/temperature/trial · Record experiment trial

- **Source:** `GUI-UIX-requirements.md:902-902` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-383` | REST | `POST /api/v1/platform/aiml/temperature/trial` | Record experiment trial | `TrialRecordRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-383' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-383') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-383 | REST | POST /api/v1/platform/aiml/temperature/trial | Record experiment trial | TrialRecordRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-386 [P2] INT-386: REST · GET /api/v1/platform/compliance/frameworks · List compliance frameworks

- **Source:** `GUI-UIX-requirements.md:905-905` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-386` | REST | `GET /api/v1/platform/compliance/frameworks` | List compliance frameworks | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:762` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-386' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-386') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-386 | REST | GET /api/v1/platform/compliance/frameworks | List compliance frameworks | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:762 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-387 [P2] INT-387: REST · POST /api/v1/platform/context/bitemporal-slate · Build comparative bitemporal delta context slate

- **Source:** `GUI-UIX-requirements.md:906-906` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-387` | REST | `POST /api/v1/platform/context/bitemporal-slate` | Build comparative bitemporal delta context slate | `BitemporalSlateRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-387' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-387') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-387 | REST | POST /api/v1/platform/context/bitemporal-slate | Build comparative bitemporal delta context slate | BitemporalSlateRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] Build comparative bitemporal delta context slate
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-388 [P2] INT-388: REST · POST /api/v1/platform/context/build · Build ranked & deduplicated context window

- **Source:** `GUI-UIX-requirements.md:907-907` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-388` | REST | `POST /api/v1/platform/context/build` | Build ranked & deduplicated context window | `ContextBuildRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | SCR-016
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-388' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-388') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-388 | REST | POST /api/v1/platform/context/build | Build ranked & deduplicated context window | ContextBuildRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | SCR-016»
- [ ] Build ranked & deduplicated context window
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-389 [P2] INT-389: REST · POST /api/v1/platform/context/item · Add item to context candidates

- **Source:** `GUI-UIX-requirements.md:908-908` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-389` | REST | `POST /api/v1/platform/context/item` | Add item to context candidates | `ContextItemAddRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-389' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-389') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-389 | REST | POST /api/v1/platform/context/item | Add item to context candidates | ContextItemAddRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] Add item to context candidates
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-390 [P2] INT-390: REST · GET /api/v1/platform/context/items · List registered context items

- **Source:** `GUI-UIX-requirements.md:909-909` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-390` | REST | `GET /api/v1/platform/context/items` | List registered context items | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:1471` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-390' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-390') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-390 | REST | GET /api/v1/platform/context/items | List registered context items | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:1471 | No primary screen assigned»
- [ ] List registered context items
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-391 [P2] INT-391: REST · POST /api/v1/platform/context/slice-graph · Extract attention-weighted compressed subgraph context

- **Source:** `GUI-UIX-requirements.md:910-910` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-391` | REST | `POST /api/v1/platform/context/slice-graph` | Extract attention-weighted compressed subgraph context | `GraphSliceRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-391' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-391') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-391 | REST | POST /api/v1/platform/context/slice-graph | Extract attention-weighted compressed subgraph context | GraphSliceRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] Extract attention-weighted compressed subgraph context
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-392 [P2] INT-392: REST · GET /api/v1/platform/context/stats · Context engineering stats

- **Source:** `GUI-UIX-requirements.md:911-911` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-392` | REST | `GET /api/v1/platform/context/stats` | Context engineering stats | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:1478` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-392' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-392') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-392 | REST | GET /api/v1/platform/context/stats | Context engineering stats | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:1478 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-393 [P2] INT-393: REST · POST /api/v1/platform/copilot/insights · Generate proactive insights

- **Source:** `GUI-UIX-requirements.md:912-912` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-393` | REST | `POST /api/v1/platform/copilot/insights` | Generate proactive insights | `CopilotInsightRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-393' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-393') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-393 | REST | POST /api/v1/platform/copilot/insights | Generate proactive insights | CopilotInsightRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-394 [P2] INT-394: REST · GET /api/v1/platform/copilot/insights · List active insights

- **Source:** `GUI-UIX-requirements.md:913-913` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-394` | REST | `GET /api/v1/platform/copilot/insights` | List active insights | `none`; params: limit | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:1100` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-394' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-394') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-394 | REST | GET /api/v1/platform/copilot/insights | List active insights | none; params: limit | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:1100 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-395 [P2] INT-395: REST · POST /api/v1/platform/copilot/message · Process copilot message

- **Source:** `GUI-UIX-requirements.md:914-914` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-395` | REST | `POST /api/v1/platform/copilot/message` | Process copilot message | `CopilotMessageRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-395' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-395') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-395 | REST | POST /api/v1/platform/copilot/message | Process copilot message | CopilotMessageRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-396 [P2] INT-396: REST · GET /api/v1/platform/copilot/rules · List automation rules

- **Source:** `GUI-UIX-requirements.md:915-915` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-396` | REST | `GET /api/v1/platform/copilot/rules` | List automation rules | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:1118` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-396' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-396') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-396 | REST | GET /api/v1/platform/copilot/rules | List automation rules | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:1118 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-397 [P2] INT-397: REST · POST /api/v1/platform/copilot/rules · Add automation rule

- **Source:** `GUI-UIX-requirements.md:916-916` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-397` | REST | `POST /api/v1/platform/copilot/rules` | Add automation rule | `CopilotRuleRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-397' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-397') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-397 | REST | POST /api/v1/platform/copilot/rules | Add automation rule | CopilotRuleRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-398 [P2] INT-398: REST · GET /api/v1/platform/copilot/sessions · List copilot sessions

- **Source:** `GUI-UIX-requirements.md:917-917` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-398` | REST | `GET /api/v1/platform/copilot/sessions` | List copilot sessions | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:1125` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-398' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-398') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-398 | REST | GET /api/v1/platform/copilot/sessions | List copilot sessions | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:1125 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-399 [P2] INT-399: REST · GET /api/v1/platform/copilot/stats · Copilot statistics

- **Source:** `GUI-UIX-requirements.md:918-918` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-399` | REST | `GET /api/v1/platform/copilot/stats` | Copilot statistics | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:1132` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-399' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-399') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-399 | REST | GET /api/v1/platform/copilot/stats | Copilot statistics | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:1132 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-400 [P2] INT-400: REST · GET /api/v1/platform/copilot/suggest/{session_id} · Get suggested questions

- **Source:** `GUI-UIX-requirements.md:919-919` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-400` | REST | `GET /api/v1/platform/copilot/suggest/{session_id}` | Get suggested questions | `none`; params: session_id, limit | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:1081` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-400' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-400') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-400 | REST | GET /api/v1/platform/copilot/suggest/{session_id} | Get suggested questions | none; params: session_id, limit | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:1081 | No primary screen assigned»
- [ ] none; params: session_id, limit
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-401 [P2] INT-401: REST · GET /api/v1/platform/cost/recommendations · Get optimization recommendations

- **Source:** `GUI-UIX-requirements.md:920-920` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-401` | REST | `GET /api/v1/platform/cost/recommendations` | Get optimization recommendations | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:1428` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-401' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-401') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-401 | REST | GET /api/v1/platform/cost/recommendations | Get optimization recommendations | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:1428 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-402 [P2] INT-402: REST · POST /api/v1/platform/cost/record · Record cost event

- **Source:** `GUI-UIX-requirements.md:921-921` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-402` | REST | `POST /api/v1/platform/cost/record` | Record cost event | `CostRecordRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-402' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-402') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-402 | REST | POST /api/v1/platform/cost/record | Record cost event | CostRecordRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-403 [P2] INT-403: REST · GET /api/v1/platform/cost/stats · Cost optimization stats

- **Source:** `GUI-UIX-requirements.md:922-922` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-403` | REST | `GET /api/v1/platform/cost/stats` | Cost optimization stats | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:1438` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-403' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-403') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-403 | REST | GET /api/v1/platform/cost/stats | Cost optimization stats | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:1438 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-404 [P2] INT-404: REST · POST /api/v1/platform/edge/nodes · Register edge node

- **Source:** `GUI-UIX-requirements.md:923-923` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-404` | REST | `POST /api/v1/platform/edge/nodes` | Register edge node | `EdgeNodeRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-404' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-404') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-404 | REST | POST /api/v1/platform/edge/nodes | Register edge node | EdgeNodeRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-405 [P2] INT-405: REST · GET /api/v1/platform/edge/nodes · List edge nodes

- **Source:** `GUI-UIX-requirements.md:924-924` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-405` | REST | `GET /api/v1/platform/edge/nodes` | List edge nodes | `none`; params: region, status | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:851` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-405' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-405') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-405 | REST | GET /api/v1/platform/edge/nodes | List edge nodes | none; params: region, status | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:851 | No primary screen assigned»
- [ ] none; params: region, status
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-406 [P2] INT-406: REST · GET /api/v1/platform/edge/nodes/{node_id}/query · Offline query

- **Source:** `GUI-UIX-requirements.md:925-925` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-406` | REST | `GET /api/v1/platform/edge/nodes/{node_id}/query` | Offline query | `none`; params: node_id, entity_type, limit | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:874` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-406' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-406') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-406 | REST | GET /api/v1/platform/edge/nodes/{node_id}/query | Offline query | none; params: node_id, entity_type, limit | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:874 | No primary screen assigned»
- [ ] none; params: node_id, entity_type, limit
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-407 [P2] INT-407: REST · POST /api/v1/platform/edge/promote · Promote edge entities to cloud

- **Source:** `GUI-UIX-requirements.md:926-926` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-407` | REST | `POST /api/v1/platform/edge/promote` | Promote edge entities to cloud | `EdgePromoteRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-407' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-407') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-407 | REST | POST /api/v1/platform/edge/promote | Promote edge entities to cloud | EdgePromoteRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] Promote edge entities to cloud
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-408 [P2] INT-408: REST · GET /api/v1/platform/edge/stats · Edge runtime statistics

- **Source:** `GUI-UIX-requirements.md:927-927` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-408` | REST | `GET /api/v1/platform/edge/stats` | Edge runtime statistics | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/platform_router.py:885` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-408' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-408') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-408 | REST | GET /api/v1/platform/edge/stats | Edge runtime statistics | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/platform_router.py:885 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-409 [P2] INT-409: REST · POST /api/v1/platform/edge/sync · Sync edge node

- **Source:** `GUI-UIX-requirements.md:928-928` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-409` | REST | `POST /api/v1/platform/edge/sync` | Sync edge node | `EdgeSyncRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-409' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-409') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-409 | REST | POST /api/v1/platform/edge/sync | Sync edge node | EdgeSyncRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

