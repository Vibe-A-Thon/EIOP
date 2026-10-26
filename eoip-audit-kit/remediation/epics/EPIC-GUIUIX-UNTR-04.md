# EPIC-GUIUIX-UNTR-04: GUI-UIX-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 60 tasks, ~360.0 h, priorities {'P2': 60}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-INT-087 [P2] INT-087: REST · POST /api/v1/branding/terminology/canonicalize · Canonicalize

- **Source:** `GUI-UIX-requirements.md:606-606` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-087` | REST | `POST /api/v1/branding/terminology/canonicalize` | Canonicalize | `CanonicalizeRequest`; params: tenant_id | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/branding/router.py:56` | SCR-023
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-087' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-087') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-087 | REST | POST /api/v1/branding/terminology/canonicalize | Canonicalize | CanonicalizeRequest; params: tenant_id | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/branding/router.py:56 | SCR-023»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-088 [P2] INT-088: REST · POST /api/v1/branding/terminology/rename · Rename

- **Source:** `GUI-UIX-requirements.md:607-607` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-088` | REST | `POST /api/v1/branding/terminology/rename` | Rename | `RenameRequest`; params: tenant_id | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/branding/router.py:52` | SCR-023
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-088' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-088') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-088 | REST | POST /api/v1/branding/terminology/rename | Rename | RenameRequest; params: tenant_id | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/branding/router.py:52 | SCR-023»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-089 [P2] INT-089: REST · GET /api/v1/branding/theme · Theme View

- **Source:** `GUI-UIX-requirements.md:608-608` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-089` | REST | `GET /api/v1/branding/theme` | Theme View | `none`; params: tenant_id, mode | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/branding/router.py:48` | SCR-023
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-089' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-089') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-089 | REST | GET /api/v1/branding/theme | Theme View | none; params: tenant_id, mode | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/branding/router.py:48 | SCR-023»
- [ ] none; params: tenant_id, mode
- [ ] 200,422; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-090 [P2] INT-090: REST · GET /api/v1/capsules · List Capsules

- **Source:** `GUI-UIX-requirements.md:609-609` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-090` | REST | `GET /api/v1/capsules` | List Capsules | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:737` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-090' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-090') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-090 | REST | GET /api/v1/capsules | List Capsules | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/main.py:737 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-091 [P2] INT-091: REST · POST /api/v1/capsules · Build Capsule

- **Source:** `GUI-UIX-requirements.md:610-610` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-091` | REST | `POST /api/v1/capsules` | Build Capsule | `CapsuleRequest`; params: none | `none` | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:708` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-091' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-091') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-091 | REST | POST /api/v1/capsules | Build Capsule | CapsuleRequest; params: none | none | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/main.py:708 | No primary screen assigned»
- [ ] 201,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-092 [P2] INT-092: REST · GET /api/v1/capsules/{name} · Get Capsule

- **Source:** `GUI-UIX-requirements.md:611-611` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-092` | REST | `GET /api/v1/capsules/{name}` | Get Capsule | `none`; params: name | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:743` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-092' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-092') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-092 | REST | GET /api/v1/capsules/{name} | Get Capsule | none; params: name | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/main.py:743 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-093 [P2] INT-093: REST · GET /api/v1/catalog/products · Catalog List Products

- **Source:** `GUI-UIX-requirements.md:612-612` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-093` | REST | `GET /api/v1/catalog/products` | Catalog List Products | `none`; params: owner, domain, state, access_policy, consumer | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:561` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-093' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-093') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-093 | REST | GET /api/v1/catalog/products | Catalog List Products | none; params: owner, domain, state, access_policy, consumer | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:561 | No primary screen assigned»
- [ ] none; params: owner, domain, state, access_policy, consumer
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-094 [P2] INT-094: REST · POST /api/v1/catalog/products · Catalog Create Product

- **Source:** `GUI-UIX-requirements.md:613-613` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-094` | REST | `POST /api/v1/catalog/products` | Catalog Create Product | `KnowledgeProduct`; params: none | `KnowledgeProduct` | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:582` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-094' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-094') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-094 | REST | POST /api/v1/catalog/products | Catalog Create Product | KnowledgeProduct; params: none | KnowledgeProduct | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:582 | No primary screen assigned»
- [ ] 201,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-095 [P2] INT-095: REST · POST /api/v1/catalog/products/import · Catalog Import Product

- **Source:** `GUI-UIX-requirements.md:614-614` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-095` | REST | `POST /api/v1/catalog/products/import` | Catalog Import Product | `KnowledgeProduct`; params: none | `KnowledgeProduct` | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:647` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-095' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-095') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-095 | REST | POST /api/v1/catalog/products/import | Catalog Import Product | KnowledgeProduct; params: none | KnowledgeProduct | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:647 | No primary screen assigned»
- [ ] 201,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-096 [P2] INT-096: REST · GET /api/v1/catalog/products/{product_id} · Catalog Get Product

- **Source:** `GUI-UIX-requirements.md:615-615` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-096` | REST | `GET /api/v1/catalog/products/{product_id}` | Catalog Get Product | `none`; params: product_id | `KnowledgeProduct` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:590` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-096' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-096') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-096 | REST | GET /api/v1/catalog/products/{product_id} | Catalog Get Product | none; params: product_id | KnowledgeProduct | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:590 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-097 [P2] INT-097: REST · PUT /api/v1/catalog/products/{product_id} · Catalog Update Product

- **Source:** `GUI-UIX-requirements.md:616-616` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-097` | REST | `PUT /api/v1/catalog/products/{product_id}` | Catalog Update Product | `KnowledgeProduct`; params: product_id | `KnowledgeProduct` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:598` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-097' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-097') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-097 | REST | PUT /api/v1/catalog/products/{product_id} | Catalog Update Product | KnowledgeProduct; params: product_id | KnowledgeProduct | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:598 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-098 [P2] INT-098: REST · DELETE /api/v1/catalog/products/{product_id} · Catalog Delete Product

- **Source:** `GUI-UIX-requirements.md:617-617` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-098` | REST | `DELETE /api/v1/catalog/products/{product_id}` | Catalog Delete Product | `none`; params: product_id | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:609` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-098' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-098') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-098 | REST | DELETE /api/v1/catalog/products/{product_id} | Catalog Delete Product | none; params: product_id | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:609 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-099 [P2] INT-099: REST · GET /api/v1/catalog/products/{product_id}/export · Catalog Export Product

- **Source:** `GUI-UIX-requirements.md:618-618` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-099` | REST | `GET /api/v1/catalog/products/{product_id}/export` | Catalog Export Product | `none`; params: product_id | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `PARTIAL` | `apps/api/extended.py:638` | SCR-019
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-099' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-099') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-099 | REST | GET /api/v1/catalog/products/{product_id}/export | Catalog Export Product | none; params: product_id | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | PARTIAL | apps/api/extended.py:638 | SCR-019»
- [ ] 200,422; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-100 [P2] INT-100: REST · GET /api/v1/catalog/products/{product_id}/lineage · Catalog Product Lineage

- **Source:** `GUI-UIX-requirements.md:619-619` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-100` | REST | `GET /api/v1/catalog/products/{product_id}/lineage` | Catalog Product Lineage | `none`; params: product_id | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:630` | SCR-006
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-100' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-100') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-100 | REST | GET /api/v1/catalog/products/{product_id}/lineage | Catalog Product Lineage | none; params: product_id | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:630 | SCR-006»
- [ ] 200,422; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-101 [P2] INT-101: REST · POST /api/v1/catalog/products/{product_id}/transition · Catalog Transition Product

- **Source:** `GUI-UIX-requirements.md:620-620` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-101` | REST | `POST /api/v1/catalog/products/{product_id}/transition` | Catalog Transition Product | `CatalogTransitionRequest`; params: product_id | `KnowledgeProduct` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/extended.py:618` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-101' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-101') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-101 | REST | POST /api/v1/catalog/products/{product_id}/transition | Catalog Transition Product | CatalogTransitionRequest; params: product_id | KnowledgeProduct | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/extended.py:618 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-102 [P2] INT-102: REST · POST /api/v1/causal/correlations/{entity_cid} · Causal Correlations

- **Source:** `GUI-UIX-requirements.md:621-621` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-102` | REST | `POST /api/v1/causal/correlations/{entity_cid}` | Causal Correlations | `inline`; params: entity_cid | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | SCR-006
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-102' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-102') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-102 | REST | POST /api/v1/causal/correlations/{entity_cid} | Causal Correlations | inline; params: entity_cid | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | SCR-006»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-103 [P2] INT-103: REST · POST /api/v1/causal/counterfactual-intervention · Counterfactual Intervention

- **Source:** `GUI-UIX-requirements.md:622-622` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-103` | REST | `POST /api/v1/causal/counterfactual-intervention` | Counterfactual Intervention | `CounterfactualInterventionRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/enterprise/advanced_router.py:86` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-103' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-103') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-103 | REST | POST /api/v1/causal/counterfactual-intervention | Counterfactual Intervention | CounterfactualInterventionRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/enterprise/advanced_router.py:86 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-104 [P2] INT-104: REST · POST /api/v1/causal/hypotheses/{incident_cid} · Causal Hypotheses

- **Source:** `GUI-UIX-requirements.md:623-623` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-104` | REST | `POST /api/v1/causal/hypotheses/{incident_cid}` | Causal Hypotheses | `inline`; params: incident_cid | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/ingest/profile.py:982` | SCR-009
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-104' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-104') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-104 | REST | POST /api/v1/causal/hypotheses/{incident_cid} | Causal Hypotheses | inline; params: incident_cid | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/ingest/profile.py:982 | SCR-009»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-105 [P2] INT-105: REST · POST /api/v1/causal/live-blast-radius · Live Blast Radius

- **Source:** `GUI-UIX-requirements.md:624-624` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-105` | REST | `POST /api/v1/causal/live-blast-radius` | Live Blast Radius | `LiveBlastRadiusRequest`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/enterprise/advanced_router.py:77` | SCR-007
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-105' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-105') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-105 | REST | POST /api/v1/causal/live-blast-radius | Live Blast Radius | LiveBlastRadiusRequest; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/enterprise/advanced_router.py:77 | SCR-007»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-106 [P2] INT-106: REST · POST /api/v1/causal/prerequisites · Causal Prerequisites

- **Source:** `GUI-UIX-requirements.md:625-625` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-106` | REST | `POST /api/v1/causal/prerequisites` | Causal Prerequisites | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1281` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-106' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-106') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-106 | REST | POST /api/v1/causal/prerequisites | Causal Prerequisites | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1281 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-107 [P2] INT-107: REST · GET /api/v1/change-journal · Semantic Change Journal

- **Source:** `GUI-UIX-requirements.md:626-626` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-107` | REST | `GET /api/v1/change-journal` | Semantic Change Journal | `none`; params: after, limit | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:702` | SCR-008
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-107' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-107') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-107 | REST | GET /api/v1/change-journal | Semantic Change Journal | none; params: after, limit | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/main.py:702 | SCR-008»
- [ ] none; params: after, limit
- [ ] 200,422; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-108 [P2] INT-108: REST · GET /api/v1/compliance/ai/evaluations · List Evaluations

- **Source:** `GUI-UIX-requirements.md:627-627` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-108` | REST | `GET /api/v1/compliance/ai/evaluations` | List Evaluations | `none`; params: model_card_id | `array<EvaluationRecord>` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:86` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-108' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-108') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-108 | REST | GET /api/v1/compliance/ai/evaluations | List Evaluations | none; params: model_card_id | array<EvaluationRecord> | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:86 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-109 [P2] INT-109: REST · POST /api/v1/compliance/ai/evaluations · Record Evaluation

- **Source:** `GUI-UIX-requirements.md:628-628` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-109` | REST | `POST /api/v1/compliance/ai/evaluations` | Record Evaluation | `EvaluationRecord`; params: none | `EvaluationRecord` | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:90` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-109' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-109') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-109 | REST | POST /api/v1/compliance/ai/evaluations | Record Evaluation | EvaluationRecord; params: none | EvaluationRecord | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:90 | No primary screen assigned»
- [ ] 201,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-110 [P2] INT-110: REST · GET /api/v1/compliance/ai/model-cards · List Model Cards

- **Source:** `GUI-UIX-requirements.md:629-629` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-110` | REST | `GET /api/v1/compliance/ai/model-cards` | List Model Cards | `none`; params: none | `array<ModelCard>` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:74` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-110' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-110') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-110 | REST | GET /api/v1/compliance/ai/model-cards | List Model Cards | none; params: none | array<ModelCard> | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:74 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-111 [P2] INT-111: REST · POST /api/v1/compliance/ai/model-cards · Register Model Card

- **Source:** `GUI-UIX-requirements.md:630-630` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-111` | REST | `POST /api/v1/compliance/ai/model-cards` | Register Model Card | `ModelCard`; params: none | `ModelCard` | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:78` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-111' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-111') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-111 | REST | POST /api/v1/compliance/ai/model-cards | Register Model Card | ModelCard; params: none | ModelCard | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:78 | No primary screen assigned»
- [ ] 201,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-112 [P2] INT-112: REST · GET /api/v1/compliance/ai/model-cards/{model_card_id}/label · Ai Label

- **Source:** `GUI-UIX-requirements.md:631-631` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-112` | REST | `GET /api/v1/compliance/ai/model-cards/{model_card_id}/label` | Ai Label | `none`; params: model_card_id | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:82` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-112' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-112') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-112 | REST | GET /api/v1/compliance/ai/model-cards/{model_card_id}/label | Ai Label | none; params: model_card_id | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:82 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-113 [P2] INT-113: REST · POST /api/v1/compliance/ai/oversight · Configure Oversight

- **Source:** `GUI-UIX-requirements.md:632-632` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-113` | REST | `POST /api/v1/compliance/ai/oversight` | Configure Oversight | `HumanOversightConfig`; params: none | `HumanOversightConfig` | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:94` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-113' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-113') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-113 | REST | POST /api/v1/compliance/ai/oversight | Configure Oversight | HumanOversightConfig; params: none | HumanOversightConfig | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:94 | No primary screen assigned»
- [ ] 201,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-114 [P2] INT-114: REST · GET /api/v1/compliance/changes · List Changes

- **Source:** `GUI-UIX-requirements.md:633-633` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-114` | REST | `GET /api/v1/compliance/changes` | List Changes | `none`; params: state, kind | `array` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:99` | SCR-008
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-114' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-114') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-114 | REST | GET /api/v1/compliance/changes | List Changes | none; params: state, kind | array | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:99 | SCR-008»
- [ ] none; params: state, kind
- [ ] 200,422; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-115 [P2] INT-115: REST · POST /api/v1/compliance/changes · Create Change

- **Source:** `GUI-UIX-requirements.md:634-634` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-115` | REST | `POST /api/v1/compliance/changes` | Create Change | `none`; params: kind, title, description, requested_by, created_at | `object` | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:106` | SCR-008
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-115' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-115') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-115 | REST | POST /api/v1/compliance/changes | Create Change | none; params: kind, title, description, requested_by, created_at | object | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:106 | SCR-008»
- [ ] none; params: kind, title, description, requested_by, created_at
- [ ] 201,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-116 [P2] INT-116: REST · POST /api/v1/compliance/changes/{proposal_id}/transition · Transition Change

- **Source:** `GUI-UIX-requirements.md:635-635` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-116` | REST | `POST /api/v1/compliance/changes/{proposal_id}/transition` | Transition Change | `none`; params: proposal_id, to_state, actor, at, reason | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:118` | SCR-008
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-116' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-116') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-116 | REST | POST /api/v1/compliance/changes/{proposal_id}/transition | Transition Change | none; params: proposal_id, to_state, actor, at, reason | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:118 | SCR-008»
- [ ] none; params: proposal_id, to_state, actor, at, reason
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-117 [P2] INT-117: REST · GET /api/v1/compliance/exceptions · List Exceptions

- **Source:** `GUI-UIX-requirements.md:636-636` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-117` | REST | `GET /api/v1/compliance/exceptions` | List Exceptions | `none`; params: active_only | `array` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:152` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-117' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-117') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-117 | REST | GET /api/v1/compliance/exceptions | List Exceptions | none; params: active_only | array | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:152 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-118 [P2] INT-118: REST · POST /api/v1/compliance/exceptions · Create Exception

- **Source:** `GUI-UIX-requirements.md:637-637` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-118` | REST | `POST /api/v1/compliance/exceptions` | Create Exception | `none`; params: policy_ref, subject, justification, approved_by, expires_at | `object` | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:156` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-118' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-118') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-118 | REST | POST /api/v1/compliance/exceptions | Create Exception | none; params: policy_ref, subject, justification, approved_by, expires_at | object | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:156 | No primary screen assigned»
- [ ] none; params: policy_ref, subject, justification, approved_by, expires_at
- [ ] 201,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-119 [P2] INT-119: REST · POST /api/v1/compliance/exceptions/{exception_id}/revoke · Revoke Exception

- **Source:** `GUI-UIX-requirements.md:638-638` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-119` | REST | `POST /api/v1/compliance/exceptions/{exception_id}/revoke` | Revoke Exception | `none`; params: exception_id, actor | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:168` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-119' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-119') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-119 | REST | POST /api/v1/compliance/exceptions/{exception_id}/revoke | Revoke Exception | none; params: exception_id, actor | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:168 | No primary screen assigned»
- [ ] none; params: exception_id, actor
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-120 [P2] INT-120: REST · GET /api/v1/compliance/packs · List Packs

- **Source:** `GUI-UIX-requirements.md:639-639` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-120` | REST | `GET /api/v1/compliance/packs` | List Packs | `none`; params: none | `array<CompliancePack>` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:53` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-120' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-120') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-120 | REST | GET /api/v1/compliance/packs | List Packs | none; params: none | array<CompliancePack> | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:53 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-121 [P2] INT-121: REST · GET /api/v1/compliance/packs/{framework} · Get Pack

- **Source:** `GUI-UIX-requirements.md:640-640` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-121` | REST | `GET /api/v1/compliance/packs/{framework}` | Get Pack | `none`; params: framework | `CompliancePack` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:57` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-121' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-121') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-121 | REST | GET /api/v1/compliance/packs/{framework} | Get Pack | none; params: framework | CompliancePack | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:57 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-122 [P2] INT-122: REST · POST /api/v1/compliance/packs/{framework}/gap-analysis · Gap Analysis

- **Source:** `GUI-UIX-requirements.md:641-641` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-122` | REST | `POST /api/v1/compliance/packs/{framework}/gap-analysis` | Gap Analysis | `none`; params: framework | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:64` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-122' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-122') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-122 | REST | POST /api/v1/compliance/packs/{framework}/gap-analysis | Gap Analysis | none; params: framework | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:64 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-123 [P2] INT-123: REST · GET /api/v1/compliance/roles · List Roles

- **Source:** `GUI-UIX-requirements.md:642-642` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-123` | REST | `GET /api/v1/compliance/roles` | List Roles | `none`; params: none | `array` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:136` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-123' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-123') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-123 | REST | GET /api/v1/compliance/roles | List Roles | none; params: none | array | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:136 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-124 [P2] INT-124: REST · GET /api/v1/compliance/roles/auditor-view · Auditor View

- **Source:** `GUI-UIX-requirements.md:643-643` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-124` | REST | `GET /api/v1/compliance/roles/auditor-view` | Auditor View | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:140` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-124' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-124') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-124 | REST | GET /api/v1/compliance/roles/auditor-view | Auditor View | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:140 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-125 [P2] INT-125: REST · GET /api/v1/compliance/roles/{role} · Get Role

- **Source:** `GUI-UIX-requirements.md:644-644` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-125` | REST | `GET /api/v1/compliance/roles/{role}` | Get Role | `none`; params: role | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/compliance/router.py:144` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-125' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-125') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-125 | REST | GET /api/v1/compliance/roles/{role} | Get Role | none; params: role | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/compliance/router.py:144 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-126 [P2] INT-126: REST · GET /api/v1/config/audit · Audit

- **Source:** `GUI-UIX-requirements.md:645-645` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-126` | REST | `GET /api/v1/config/audit` | Audit | `none`; params: key | `array<ConfigChangeRecord>` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/config/router.py:118` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-126' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-126') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-126 | REST | GET /api/v1/config/audit | Audit | none; params: key | array<ConfigChangeRecord> | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/config/router.py:118 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-127 [P2] INT-127: REST · POST /api/v1/config/bounds · Bounds

- **Source:** `GUI-UIX-requirements.md:646-646` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-127` | REST | `POST /api/v1/config/bounds` | Bounds | `object`; params: none | `ConfigChangeRecord` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/config/router.py:105` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-127' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-127') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-127 | REST | POST /api/v1/config/bounds | Bounds | object; params: none | ConfigChangeRecord | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/config/router.py:105 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-128 [P2] INT-128: REST · GET /api/v1/config/definitions · Definitions

- **Source:** `GUI-UIX-requirements.md:647-647` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-128` | REST | `GET /api/v1/config/definitions` | Definitions | `none`; params: none | `array<SettingDef>` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/config/router.py:58` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-128' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-128') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-128 | REST | GET /api/v1/config/definitions | Definitions | none; params: none | array<SettingDef> | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/config/router.py:58 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-129 [P2] INT-129: REST · POST /api/v1/config/diff · Diff

- **Source:** `GUI-UIX-requirements.md:648-648` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-129` | REST | `POST /api/v1/config/diff` | Diff | `object`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/config/router.py:168` | SCR-008
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-129' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-129') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-129 | REST | POST /api/v1/config/diff | Diff | object; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/config/router.py:168 | SCR-008»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-130 [P2] INT-130: REST · GET /api/v1/config/effective · Effective

- **Source:** `GUI-UIX-requirements.md:649-649` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-130` | REST | `GET /api/v1/config/effective` | Effective | `none`; params: key, tenant, business_unit, workspace, user_id | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/config/router.py:62` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-130' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-130') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-130 | REST | GET /api/v1/config/effective | Effective | none; params: key, tenant, business_unit, workspace, user_id | object | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/config/router.py:62 | No primary screen assigned»
- [ ] none; params: key, tenant, business_unit, workspace, user_id
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-131 [P2] INT-131: REST · GET /api/v1/config/explain · Explain

- **Source:** `GUI-UIX-requirements.md:650-650` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-131` | REST | `GET /api/v1/config/explain` | Explain | `none`; params: key, tenant, business_unit, workspace, user_id | `ExplainResult` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/config/router.py:76` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-131' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-131') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-131 | REST | GET /api/v1/config/explain | Explain | none; params: key, tenant, business_unit, workspace, user_id | ExplainResult | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/config/router.py:76 | No primary screen assigned»
- [ ] none; params: key, tenant, business_unit, workspace, user_id
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-132 [P2] INT-132: REST · POST /api/v1/config/export · Export

- **Source:** `GUI-UIX-requirements.md:651-651` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-132` | REST | `POST /api/v1/config/export` | Export | `object`; params: none | `ConfigArchive` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `PARTIAL` | `packages/eoip/config/router.py:140` | SCR-019
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-132' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-132') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-132 | REST | POST /api/v1/config/export | Export | object; params: none | ConfigArchive | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | PARTIAL | packages/eoip/config/router.py:140 | SCR-019»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-133 [P2] INT-133: REST · GET /api/v1/config/flags · List Flags

- **Source:** `GUI-UIX-requirements.md:652-652` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-133` | REST | `GET /api/v1/config/flags` | List Flags | `none`; params: none | `array<FeatureFlag>` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/config/router.py:177` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-133' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-133') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-133 | REST | GET /api/v1/config/flags | List Flags | none; params: none | array<FeatureFlag> | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/config/router.py:177 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-134 [P2] INT-134: REST · POST /api/v1/config/flags · Set Flag

- **Source:** `GUI-UIX-requirements.md:653-653` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-134` | REST | `POST /api/v1/config/flags` | Set Flag | `object`; params: none | `FeatureFlag` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/config/router.py:181` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-134' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-134') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-134 | REST | POST /api/v1/config/flags | Set Flag | object; params: none | FeatureFlag | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/config/router.py:181 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-135 [P2] INT-135: REST · POST /api/v1/config/import · Import

- **Source:** `GUI-UIX-requirements.md:654-654` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-135` | REST | `POST /api/v1/config/import` | Import | `object`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/config/router.py:147` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-135' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-135') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-135 | REST | POST /api/v1/config/import | Import | object; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/config/router.py:147 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-136 [P2] INT-136: REST · POST /api/v1/config/reload-subscribe · Reload Subscribe

- **Source:** `GUI-UIX-requirements.md:655-655` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-136` | REST | `POST /api/v1/config/reload-subscribe` | Reload Subscribe | `object`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/config/router.py:188` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-136' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-136') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-136 | REST | POST /api/v1/config/reload-subscribe | Reload Subscribe | object; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/config/router.py:188 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-138 [P2] INT-138: REST · POST /api/v1/config/set · Set

- **Source:** `GUI-UIX-requirements.md:657-657` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-138` | REST | `POST /api/v1/config/set` | Set | `object`; params: none | `ConfigChangeRecord` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/config/router.py:90` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-138' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-138') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-138 | REST | POST /api/v1/config/set | Set | object; params: none | ConfigChangeRecord | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/config/router.py:90 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-139 [P2] INT-139: REST · POST /api/v1/conformance/check · Conformance Check

- **Source:** `GUI-UIX-requirements.md:658-658` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-139` | REST | `POST /api/v1/conformance/check` | Conformance Check | `object`; params: none | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:975` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-139' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-139') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-139 | REST | POST /api/v1/conformance/check | Conformance Check | object; params: none | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | apps/api/app.py:975 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-140 [P2] INT-140: REST · GET /api/v1/conformance/rules · Conformance Rule Sets

- **Source:** `GUI-UIX-requirements.md:659-659` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-140` | REST | `GET /api/v1/conformance/rules` | Conformance Rule Sets | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1001` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-140' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-140') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-140 | REST | GET /api/v1/conformance/rules | Conformance Rule Sets | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1001 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-141 [P2] INT-141: REST · PUT /api/v1/conformance/rules/{name} · Save Conformance Rule Set

- **Source:** `GUI-UIX-requirements.md:660-660` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-141` | REST | `PUT /api/v1/conformance/rules/{name}` | Save Conformance Rule Set | `object`; params: name | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1007` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-141' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-141') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-141 | REST | PUT /api/v1/conformance/rules/{name} | Save Conformance Rule Set | object; params: name | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1007 | No primary screen assigned»
- [ ] Save Conformance Rule Set
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-142 [P2] INT-142: REST · GET /api/v1/connectors/catalog · Connectors Catalog

- **Source:** `GUI-UIX-requirements.md:661-661` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-142` | REST | `GET /api/v1/connectors/catalog` | Connectors Catalog | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:1583` | SCR-014
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-142' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-142') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-142 | REST | GET /api/v1/connectors/catalog | Connectors Catalog | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:1583 | SCR-014»
- [ ] 200; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-143 [P2] INT-143: REST · GET /api/v1/connectors/files/formats · Formats

- **Source:** `GUI-UIX-requirements.md:662-662` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-143` | REST | `GET /api/v1/connectors/files/formats` | Formats | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/fileparse/api.py:24` | SCR-014
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-143' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-143') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-143 | REST | GET /api/v1/connectors/files/formats | Formats | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/fileparse/api.py:24 | SCR-014»
- [ ] 200; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-144 [P2] INT-144: REST · GET /api/v1/demo/scenarios · Demo Scenarios

- **Source:** `GUI-UIX-requirements.md:663-663` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-144` | REST | `GET /api/v1/demo/scenarios` | Demo Scenarios | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/app.py:355` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-144' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-144') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-144 | REST | GET /api/v1/demo/scenarios | Demo Scenarios | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/app.py:355 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-145 [P2] INT-145: REST · GET /api/v1/domain-packs · List Domain Packs

- **Source:** `GUI-UIX-requirements.md:664-664` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-145` | REST | `GET /api/v1/domain-packs` | List Domain Packs | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/enterprise/advanced_router.py:119` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-145' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-145') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-145 | REST | GET /api/v1/domain-packs | List Domain Packs | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/enterprise/advanced_router.py:119 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-146 [P2] INT-146: REST · GET /api/v1/domain-packs/{pack_name} · Get Domain Pack

- **Source:** `GUI-UIX-requirements.md:665-665` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-146` | REST | `GET /api/v1/domain-packs/{pack_name}` | Get Domain Pack | `none`; params: pack_name | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/enterprise/advanced_router.py:123` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-146' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-146') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-146 | REST | GET /api/v1/domain-packs/{pack_name} | Get Domain Pack | none; params: pack_name | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/enterprise/advanced_router.py:123 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-147 [P2] INT-147: REST · POST /api/v1/domain-packs/{pack_name}/activate · Activate Domain Pack

- **Source:** `GUI-UIX-requirements.md:666-666` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-147` | REST | `POST /api/v1/domain-packs/{pack_name}/activate` | Activate Domain Pack | `ActivateDomainPackRequest`; params: pack_name | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/enterprise/advanced_router.py:130` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-147' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-147') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-147 | REST | POST /api/v1/domain-packs/{pack_name}/activate | Activate Domain Pack | ActivateDomainPackRequest; params: pack_name | none | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/enterprise/advanced_router.py:130 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

