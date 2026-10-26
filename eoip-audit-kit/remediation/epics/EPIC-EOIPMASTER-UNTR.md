# EPIC-EOIPMASTER-UNTR: EOIP-master-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 60 tasks, ~362.0 h, priorities {'P0': 44, 'P1': 16}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-CAP-04 [P0] CAP-04: Embedded/single-node footprint · D01 Storage · P0

- **Source:** `EOIP-master-requirements.md:42-42` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-04` | **Embedded/single-node footprint** | D01 Storage | `P0` | 100% Implemented (Implemented (BL-01)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-04' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-04') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-04 | Embedded/single-node footprint | D01 Storage | P0 | 100% Implemented (Implemented (BL-01)) | VERIFIED»
- [ ] 100% Implemented (Implemented (BL-01))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-08 [P0] CAP-08: Schema, typing and constraint enforcement · D01 Storage · P0

- **Source:** `EOIP-master-requirements.md:46-46` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-08` | **Schema, typing and constraint enforcement** | D01 Storage | `P0` | 100% Implemented (Implemented (BL-28)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-08' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-08') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-08 | Schema, typing and constraint enforcement | D01 Storage | P0 | 100% Implemented (Implemented (BL-28)) | VERIFIED»
- [ ] Schema, typing and constraint enforcement
- [ ] 100% Implemented (Implemented (BL-28))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-11 [P0] CAP-11: Edge properties and reification (RDF-star / LPG) · D02 Schema · P0

- **Source:** `EOIP-master-requirements.md:49-49` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-11` | **Edge properties and reification (RDF-star / LPG)** | D02 Schema | `P0` | 100% Implemented (Implemented (BL-01)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-11' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-11') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-11 | Edge properties and reification (RDF-star / LPG) | D02 Schema | P0 | 100% Implemented (Implemented (BL-01)) | VERIFIED»
- [ ] Edge properties and reification (RDF-star / LPG)
- [ ] 100% Implemented (Implemented (BL-01))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-13 [P0] CAP-13: Apache TinkerPop Gremlin query execution · D02 Schema · P0

- **Source:** `EOIP-master-requirements.md:51-51` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-13` | **Apache TinkerPop Gremlin query execution** | D02 Schema | `P0` | 100% Implemented (Implemented (BL-02, BL-04)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-13' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-13') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-13 | Apache TinkerPop Gremlin query execution | D02 Schema | P0 | 100% Implemented (Implemented (BL-02, BL-04)) | VERIFIED»
- [ ] Apache TinkerPop Gremlin query execution
- [ ] 100% Implemented (Implemented (BL-02, BL-04))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-14 [P0] CAP-14: Cypher / openCypher / ISO GQL execution · D02 Schema · P0

- **Source:** `EOIP-master-requirements.md:52-52` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-14` | **Cypher / openCypher / ISO GQL execution** | D02 Schema | `P0` | 100% Implemented (Implemented (BL-03, BL-04)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-14' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-14') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-14 | Cypher / openCypher / ISO GQL execution | D02 Schema | P0 | 100% Implemented (Implemented (BL-03, BL-04)) | VERIFIED»
- [ ] Cypher / openCypher / ISO GQL execution
- [ ] 100% Implemented (Implemented (BL-03, BL-04))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-19 [P0] CAP-19: Multi-hop, shortest-path and recursive queries · D03 Query · P0

- **Source:** `EOIP-master-requirements.md:57-57` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-19` | **Multi-hop, shortest-path and recursive queries** | D03 Query | `P0` | 100% Implemented (Implemented (BL-43)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-19' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-19') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-19 | Multi-hop, shortest-path and recursive queries | D03 Query | P0 | 100% Implemented (Implemented (BL-43)) | VERIFIED»
- [ ] Multi-hop, shortest-path and recursive queries
- [ ] 100% Implemented (Implemented (BL-43))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-24 [P0] CAP-24: Explanation and proof traces · D03 Query · P0

- **Source:** `EOIP-master-requirements.md:62-62` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-24` | **Explanation and proof traces** | D03 Query | `P0` | 100% Implemented (Implemented (BL-41, BL-48)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-24' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-24') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-24 | Explanation and proof traces | D03 Query | P0 | 100% Implemented (Implemented (BL-41, BL-48)) | VERIFIED»
- [ ] Explanation and proof traces
- [ ] 100% Implemented (Implemented (BL-41, BL-48))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-25 [P0] CAP-25: Inconsistency and contradiction handling · D04 Reasoning · P0

- **Source:** `EOIP-master-requirements.md:63-63` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-25` | **Inconsistency and contradiction handling** | D04 Reasoning | `P0` | 100% Implemented (Implemented (BL-39)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-25' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-25') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-25 | Inconsistency and contradiction handling | D04 Reasoning | P0 | 100% Implemented (Implemented (BL-39)) | VERIFIED»
- [ ] Inconsistency and contradiction handling
- [ ] 100% Implemented (Implemented (BL-39))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-26 [P0] CAP-26: Enterprise connectors and CDC streaming · D04 Reasoning · P0

- **Source:** `EOIP-master-requirements.md:64-64` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-26` | **Enterprise connectors and CDC streaming** | D04 Reasoning | `P0` | 100% Implemented (Implemented (BL-23)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-26' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-26') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-26 | Enterprise connectors and CDC streaming | D04 Reasoning | P0 | 100% Implemented (Implemented (BL-23)) | VERIFIED»
- [ ] Enterprise connectors and CDC streaming
- [ ] 100% Implemented (Implemented (BL-23))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-27 [P0] CAP-27: Idempotent event log, replay and DLQ · D04 Reasoning · P0

- **Source:** `EOIP-master-requirements.md:65-65` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-27` | **Idempotent event log, replay and DLQ** | D04 Reasoning | `P0` | 100% Implemented (Implemented (BL-24)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-27' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-27') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-27 | Idempotent event log, replay and DLQ | D04 Reasoning | P0 | 100% Implemented (Implemented (BL-24)) | VERIFIED»
- [ ] Idempotent event log, replay and DLQ
- [ ] 100% Implemented (Implemented (BL-24))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-28 [P0] CAP-28: Schema inference from arbitrary JSON · D04 Reasoning · P0

- **Source:** `EOIP-master-requirements.md:66-66` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-28` | **Schema inference from arbitrary JSON** | D04 Reasoning | `P0` | 100% Implemented (Implemented (BL-26)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-28' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-28') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-28 | Schema inference from arbitrary JSON | D04 Reasoning | P0 | 100% Implemented (Implemented (BL-26)) | VERIFIED»
- [ ] Schema inference from arbitrary JSON
- [ ] 100% Implemented (Implemented (BL-26))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-30 [P0] CAP-30: Deterministic identity keys · D04 Reasoning · P0

- **Source:** `EOIP-master-requirements.md:68-68` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-30` | **Deterministic identity keys** | D04 Reasoning | `P0` | 100% Implemented (Implemented (BL-34)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-30' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-30') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-30 | Deterministic identity keys | D04 Reasoning | P0 | 100% Implemented (Implemented (BL-34)) | VERIFIED»
- [ ] 100% Implemented (Implemented (BL-34))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-32 [P0] CAP-32: Unstructured extraction (Parsing, NER, RE) · D05 Identity · P0

- **Source:** `EOIP-master-requirements.md:70-70` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-32` | **Unstructured extraction (Parsing, NER, RE)** | D05 Identity | `P0` | 100% Implemented (Implemented (BL-42, C05)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-32' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-32') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-32 | Unstructured extraction (Parsing, NER, RE) | D05 Identity | P0 | 100% Implemented (Implemented (BL-42, C05)) | VERIFIED»
- [ ] Unstructured extraction (Parsing, NER, RE)
- [ ] 100% Implemented (Implemented (BL-42, C05))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-33 [P0] CAP-33: PII and secret detection at ingest · D05 Identity · P0

- **Source:** `EOIP-master-requirements.md:71-71` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 7.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-33` | **PII and secret detection at ingest** | D05 Identity | `P0` | 100% Implemented (Implemented (BL-45, BL-46)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-33' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-33') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-33 | PII and secret detection at ingest | D05 Identity | P0 | 100% Implemented (Implemented (BL-45, BL-46)) | VERIFIED»
- [ ] PII and secret detection at ingest
- [ ] 100% Implemented (Implemented (BL-45, BL-46))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-CAP-34 [P0] CAP-34: Bitemporal queries (Valid Time + Transaction Time) · D05 Identity · P0

- **Source:** `EOIP-master-requirements.md:72-72` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-34` | **Bitemporal queries (Valid Time + Transaction Time)** | D05 Identity | `P0` | 100% Implemented (Implemented (BL-37)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-34' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-34') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-34 | Bitemporal queries (Valid Time + Transaction Time) | D05 Identity | P0 | 100% Implemented (Implemented (BL-37)) | VERIFIED»
- [ ] Bitemporal queries (Valid Time + Transaction Time)
- [ ] 100% Implemented (Implemented (BL-37))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-36 [P0] CAP-36: Event sourcing and complete audit history · D05 Identity · P0

- **Source:** `EOIP-master-requirements.md:74-74` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-36` | **Event sourcing and complete audit history** | D05 Identity | `P0` | 100% Implemented (Implemented (BL-24, BL-37)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-36' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-36') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-36 | Event sourcing and complete audit history | D05 Identity | P0 | 100% Implemented (Implemented (BL-24, BL-37)) | VERIFIED»
- [ ] Event sourcing and complete audit history
- [ ] 100% Implemented (Implemented (BL-24, BL-37))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-38 [P0] CAP-38: Provenance, evidence spans, and claim attribution · D05 Identity · P0

- **Source:** `EOIP-master-requirements.md:76-76` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-38` | **Provenance, evidence spans, and claim attribution** | D05 Identity | `P0` | 100% Implemented (Implemented (BL-41)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-38' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-38') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-38 | Provenance, evidence spans, and claim attribution | D05 Identity | P0 | 100% Implemented (Implemented (BL-41)) | VERIFIED»
- [ ] Provenance, evidence spans, and claim attribution
- [ ] 100% Implemented (Implemented (BL-41))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-39 [P0] CAP-39: Contradiction handling and truth maintenance · D05 Identity · P0

- **Source:** `EOIP-master-requirements.md:77-77` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-39` | **Contradiction handling and truth maintenance** | D05 Identity | `P0` | 100% Implemented (Implemented (BL-39)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-39' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-39') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-39 | Contradiction handling and truth maintenance | D05 Identity | P0 | 100% Implemented (Implemented (BL-39)) | VERIFIED»
- [ ] Contradiction handling and truth maintenance
- [ ] 100% Implemented (Implemented (BL-39))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-43 [P0] CAP-43: Epistemic separation (Facts vs. Predictions) · D06 Ingestion · P0

- **Source:** `EOIP-master-requirements.md:81-81` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-43` | **Epistemic separation (Facts vs. Predictions)** | D06 Ingestion | `P0` | 100% Implemented (Implemented (BL-40)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-43' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-43') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-43 | Epistemic separation (Facts vs. Predictions) | D06 Ingestion | P0 | 100% Implemented (Implemented (BL-40)) | VERIFIED»
- [ ] Epistemic separation (Facts vs. Predictions)
- [ ] 100% Implemented (Implemented (BL-40))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-44 [P0] CAP-44: Enterprise authentication and SSO (OIDC/SAML) · D06 Ingestion · P0

- **Source:** `EOIP-master-requirements.md:82-82` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 7.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-44` | **Enterprise authentication and SSO (OIDC/SAML)** | D06 Ingestion | `P0` | 100% Implemented (Implemented (BL-19)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-44' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-44') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-44 | Enterprise authentication and SSO (OIDC/SAML) | D06 Ingestion | P0 | 100% Implemented (Implemented (BL-19)) | VERIFIED»
- [ ] Enterprise authentication and SSO (OIDC/SAML)
- [ ] 100% Implemented (Implemented (BL-19))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-CAP-45 [P0] CAP-45: Role-Based and Attribute-Based Access Control · D06 Ingestion · P0

- **Source:** `EOIP-master-requirements.md:83-83` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-45` | **Role-Based and Attribute-Based Access Control** | D06 Ingestion | `P0` | 100% Implemented (Implemented (BL-19)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-45' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-45') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-45 | Role-Based and Attribute-Based Access Control | D06 Ingestion | P0 | 100% Implemented (Implemented (BL-19)) | VERIFIED»
- [ ] Role-Based and Attribute-Based Access Control
- [ ] 100% Implemented (Implemented (BL-19))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-48 [P0] CAP-48: Audit integrity and cryptographic tamper resistance · D06 Ingestion · P0

- **Source:** `EOIP-master-requirements.md:86-86` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-48` | **Audit integrity and cryptographic tamper resistance** | D06 Ingestion | `P0` | 100% Implemented (Implemented (BL-36, REVA Warrants)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-48' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-48') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-48 | Audit integrity and cryptographic tamper resistance | D06 Ingestion | P0 | 100% Implemented (Implemented (BL-36, REVA Warrants)) | VERIFIED»
- [ ] Audit integrity and cryptographic tamper resistance
- [ ] 100% Implemented (Implemented (BL-36, REVA Warrants))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-49 [P0] CAP-49: Query and prompt-injection defense · D07 Security · P0

- **Source:** `EOIP-master-requirements.md:87-87` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-49` | **Query and prompt-injection defense** | D07 Security | `P0` | 100% Implemented (Implemented (BL-45, REVA Gate)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-49' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-49') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-49 | Query and prompt-injection defense | D07 Security | P0 | 100% Implemented (Implemented (BL-45, REVA Gate)) | VERIFIED»
- [ ] Query and prompt-injection defense
- [ ] 100% Implemented (Implemented (BL-45, REVA Gate))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-50 [P0] CAP-50: Air-gapped and local-first operation · D07 Security · P0

- **Source:** `EOIP-master-requirements.md:88-88` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-50` | **Air-gapped and local-first operation** | D07 Security | `P0` | 100% Implemented (Implemented (BL-102)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-50' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-50') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-50 | Air-gapped and local-first operation | D07 Security | P0 | 100% Implemented (Implemented (BL-102)) | VERIFIED»
- [ ] Air-gapped and local-first operation
- [ ] 100% Implemented (Implemented (BL-102))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-51 [P0] CAP-51: Zero-data-leak LLM egress control · D07 Security · P0

- **Source:** `EOIP-master-requirements.md:89-89` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-51` | **Zero-data-leak LLM egress control** | D07 Security | `P0` | 100% Implemented (Implemented (BL-45)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-51' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-51') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-51 | Zero-data-leak LLM egress control | D07 Security | P0 | 100% Implemented (Implemented (BL-45)) | VERIFIED»
- [ ] Zero-data-leak LLM egress control
- [ ] 100% Implemented (Implemented (BL-45))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-52 [P0] CAP-52: White-label and OEM packaging · D07 Security · P0

- **Source:** `EOIP-master-requirements.md:90-90` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-52` | **White-label and OEM packaging** | D07 Security | `P0` | 100% Implemented (Implemented (BL-21, BL-22)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-52' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-52') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-52 | White-label and OEM packaging | D07 Security | P0 | 100% Implemented (Implemented (BL-21, BL-22)) | VERIFIED»
- [ ] White-label and OEM packaging
- [ ] 100% Implemented (Implemented (BL-21, BL-22))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-54 [P0] CAP-54: Full-text keyword search (BM25) · D07 Security · P0

- **Source:** `EOIP-master-requirements.md:92-92` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-54` | **Full-text keyword search (BM25)** | D07 Security | `P0` | 100% Implemented (Implemented (BL-13)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-54' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-54') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-54 | Full-text keyword search (BM25) | D07 Security | P0 | 100% Implemented (Implemented (BL-13)) | VERIFIED»
- [ ] Full-text keyword search (BM25)
- [ ] 100% Implemented (Implemented (BL-13))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-55 [P0] CAP-55: Hybrid retrieval and Reciprocal Rank Fusion (RRF) · D07 Security · P0

- **Source:** `EOIP-master-requirements.md:93-93` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-55` | **Hybrid retrieval and Reciprocal Rank Fusion (RRF)** | D07 Security | `P0` | 100% Implemented (Implemented (BL-15)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-55' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-55') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-55 | Hybrid retrieval and Reciprocal Rank Fusion (RRF) | D07 Security | P0 | 100% Implemented (Implemented (BL-15)) | VERIFIED»
- [ ] Hybrid retrieval and Reciprocal Rank Fusion (RRF)
- [ ] 100% Implemented (Implemented (BL-15))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-58 [P0] CAP-58: Natural language query with ranked suggestions · D08 Graph ML · P0

- **Source:** `EOIP-master-requirements.md:96-96` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-58` | **Natural language query with ranked suggestions** | D08 Graph ML | `P0` | 100% Implemented (Implemented (BL-11, BL-12)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-58' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-58') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-58 | Natural language query with ranked suggestions | D08 Graph ML | P0 | 100% Implemented (Implemented (BL-11, BL-12)) | VERIFIED»
- [ ] Natural language query with ranked suggestions
- [ ] 100% Implemented (Implemented (BL-11, BL-12))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-59 [P0] CAP-59: Model Context Protocol (MCP) tool server · D08 Graph ML · P0

- **Source:** `EOIP-master-requirements.md:97-97` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-59` | **Model Context Protocol (MCP) tool server** | D08 Graph ML | `P0` | 100% Implemented (Implemented (BL-47)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-59' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-59') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-59 | Model Context Protocol (MCP) tool server | D08 Graph ML | P0 | 100% Implemented (Implemented (BL-47)) | VERIFIED»
- [ ] Model Context Protocol (MCP) tool server
- [ ] 100% Implemented (Implemented (BL-47))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-60 [P0] CAP-60: Grounded answers with citations and abstention · D08 Graph ML · P0

- **Source:** `EOIP-master-requirements.md:98-98` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-60` | **Grounded answers with citations and abstention** | D08 Graph ML | `P0` | 100% Implemented (Implemented (BL-16, BL-40)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-60' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-60') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-60 | Grounded answers with citations and abstention | D08 Graph ML | P0 | 100% Implemented (Implemented (BL-16, BL-40)) | VERIFIED»
- [ ] Grounded answers with citations and abstention
- [ ] 100% Implemented (Implemented (BL-16, BL-40))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-61 [P0] CAP-61: Local model serving and execution · D08 Graph ML · P0

- **Source:** `EOIP-master-requirements.md:99-99` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-61` | **Local model serving and execution** | D08 Graph ML | `P0` | 100% Implemented (Implemented (BL-102)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-61' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-61') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-61 | Local model serving and execution | D08 Graph ML | P0 | 100% Implemented (Implemented (BL-102)) | VERIFIED»
- [ ] Local model serving and execution
- [ ] 100% Implemented (Implemented (BL-102))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-66 [P0] CAP-66: Precise code graph (Symbols, Definitions, AST) · D09 Agents · P0

- **Source:** `EOIP-master-requirements.md:104-104` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-66` | **Precise code graph (Symbols, Definitions, AST)** | D09 Agents | `P0` | 100% Implemented (Implemented (BL-42)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-66' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-66') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-66 | Precise code graph (Symbols, Definitions, AST) | D09 Agents | P0 | 100% Implemented (Implemented (BL-42)) | VERIFIED»
- [ ] Precise code graph (Symbols, Definitions, AST)
- [ ] 100% Implemented (Implemented (BL-42))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-69 [P0] CAP-69: Change-impact digital thread · D09 Agents · P0

- **Source:** `EOIP-master-requirements.md:107-107` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-69` | **Change-impact digital thread** | D09 Agents | `P0` | 100% Implemented (Implemented (BL-42, Journey J1)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-69' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-69') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-69 | Change-impact digital thread | D09 Agents | P0 | 100% Implemented (Implemented (BL-42, Journey J1)) | VERIFIED»
- [ ] 100% Implemented (Implemented (BL-42, Journey J1))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-71 [P0] CAP-71: Investigation workbench and visual query builder · D09 Agents · P0

- **Source:** `EOIP-master-requirements.md:109-109` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-71` | **Investigation workbench and visual query builder** | D09 Agents | `P0` | 100% Implemented (Implemented (BL-54)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-71' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-71') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-71 | Investigation workbench and visual query builder | D09 Agents | P0 | 100% Implemented (Implemented (BL-54)) | VERIFIED»
- [ ] Investigation workbench and visual query builder
- [ ] 100% Implemented (Implemented (BL-54))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-74 [P0] CAP-74: Online backup, point-in-time restore, and WAL · D10 UI/UX · P0

- **Source:** `EOIP-master-requirements.md:112-112` (table_row) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-74` | **Online backup, point-in-time restore, and WAL** | D10 UI/UX | `P0` | 100% Implemented (Implemented (BL-50)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-74' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-74') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-74 | Online backup, point-in-time restore, and WAL | D10 UI/UX | P0 | 100% Implemented (Implemented (BL-50)) | VERIFIED»
- [ ] Online backup, point-in-time restore, and WAL
- [ ] 100% Implemented (Implemented (BL-50))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-75 [P0] CAP-75: Enterprise observability (OpenTelemetry / Prometheus) · D10 UI/UX · P0

- **Source:** `EOIP-master-requirements.md:113-113` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-75` | **Enterprise observability (OpenTelemetry / Prometheus)** | D10 UI/UX | `P0` | 100% Implemented (Implemented (BL-49)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-75' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-75') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-75 | Enterprise observability (OpenTelemetry / Prometheus) | D10 UI/UX | P0 | 100% Implemented (Implemented (BL-49)) | VERIFIED»
- [ ] Enterprise observability (OpenTelemetry / Prometheus)
- [ ] 100% Implemented (Implemented (BL-49))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-77 [P0] CAP-77: Licensing economics and low Total Cost of Ownership · D10 UI/UX · P0

- **Source:** `EOIP-master-requirements.md:115-115` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-77` | **Licensing economics and low Total Cost of Ownership** | D10 UI/UX | `P0` | 100% Implemented (Implemented (BL-22)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-77' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-77') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-77 | Licensing economics and low Total Cost of Ownership | D10 UI/UX | P0 | 100% Implemented (Implemented (BL-22)) | VERIFIED»
- [ ] Licensing economics and low Total Cost of Ownership
- [ ] 100% Implemented (Implemented (BL-22))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-78 [P0] CAP-78: Independent evaluation and benchmark harness · D10 UI/UX · P0

- **Source:** `EOIP-master-requirements.md:116-116` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-78` | **Independent evaluation and benchmark harness** | D10 UI/UX | `P0` | 100% Implemented (Implemented (BL-07, scripts/benchmark.py)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-78' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-78') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-78 | Independent evaluation and benchmark harness | D10 UI/UX | P0 | 100% Implemented (Implemented (BL-07, scripts/benchmark.py)) | VERIFIED»
- [ ] Independent evaluation and benchmark harness
- [ ] 100% Implemented (Implemented (BL-07, scripts/benchmark.py))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-79 [P0] CAP-79: Supply-chain security (SBOM, signing, provenance) · D10 UI/UX · P0

- **Source:** `EOIP-master-requirements.md:117-117` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-79` | **Supply-chain security (SBOM, signing, provenance)** | D10 UI/UX | `P0` | 100% Implemented (Implemented (BL-48, REVA Warrants)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-79' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-79') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-79 | Supply-chain security (SBOM, signing, provenance) | D10 UI/UX | P0 | 100% Implemented (Implemented (BL-48, REVA Warrants)) | VERIFIED»
- [ ] Supply-chain security (SBOM, signing, provenance)
- [ ] 100% Implemented (Implemented (BL-48, REVA Warrants))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INV-03 [P0] INV-03: TopBraid EDG · Monolithic server appliance requiring months of configuration and specialized training · GitOps-native ontology-as-code (Turtle/LinkML/YAML) with instant CLI linting, diff, and automate

- **Source:** `EOIP-master-requirements.md:2666-2666` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INV-03` | **TopBraid EDG** | Monolithic server appliance requiring months of configuration and specialized training | **GitOps-native ontology-as-code (Turtle/LinkML/YAML) with instant CLI linting, diff, and automated rollback** | ``ADOPT (P0)``
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INV-03' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INV-03') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INV-03 | TopBraid EDG | Monolithic server appliance requiring months of configuration and specialized training | GitOps-native ontology-as-code (Turtle/LinkML/YAML) with instant CLI linting, diff, and automated rollback | ADOPT (P0)»
- [ ] Monolithic server appliance requiring months of configuration and specialized training
- [ ] GitOps-native ontology-as-code (Turtle/LinkML/YAML) with instant CLI linting, diff, and automated rollback
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INV-04 [P0] INV-04: Ontop / Timbr.ai · OBDA strictly translates SQL; completely blind to PDFs, docs, diagrams, and logs · Universal Connection Factory + Multimodal Grounding Pipeline: virtualize SQL, extract unstructured

- **Source:** `EOIP-master-requirements.md:2667-2667` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INV-04` | **Ontop / Timbr.ai** | OBDA strictly translates SQL; completely blind to PDFs, docs, diagrams, and logs | **Universal Connection Factory + Multimodal Grounding Pipeline: virtualize SQL, extract unstructured dark data** | ``ADOPT (P0)``
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INV-04' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INV-04') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INV-04 | Ontop / Timbr.ai | OBDA strictly translates SQL; completely blind to PDFs, docs, diagrams, and logs | Universal Connection Factory + Multimodal Grounding Pipeline: virtualize SQL, extract unstructured dark data | ADOPT (P0)»
- [ ] OBDA strictly translates SQL; completely blind to PDFs, docs, diagrams, and logs
- [ ] Universal Connection Factory + Multimodal Grounding Pipeline: virtualize SQL, extract unstructured dark data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INV-07 [P0] INV-07: Senzing / Commercial ER · Per-record pricing creates severe cost barriers for large enterprise data lakes · Integrate open-source Splink (Fellegi-Sunter model) with DuckDB acceleration; 100% free of p

- **Source:** `EOIP-master-requirements.md:2670-2670` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INV-07` | **Senzing / Commercial ER** | Per-record pricing creates severe cost barriers for large enterprise data lakes | **Integrate open-source Splink (Fellegi-Sunter model) with DuckDB acceleration; 100% free of per-record fees** | ``ADOPT (P0)``
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INV-07' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INV-07') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INV-07 | Senzing / Commercial ER | Per-record pricing creates severe cost barriers for large enterprise data lakes | Integrate open-source Splink (Fellegi-Sunter model) with DuckDB acceleration; 100% free of per-record fees | ADOPT (P0)»
- [ ] Senzing / Commercial ER
- [ ] Per-record pricing creates severe cost barriers for large enterprise data lakes
- [ ] Integrate open-source Splink (Fellegi-Sunter model) with DuckDB acceleration; 100% free of per-record fees
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INV-SELF-05 [P0] INV-SELF-05: KnowGridFlow Baseline (BL-29) · Differential SHACL test fails due to missing dependency · Pin pyshacl in requirements-neural.lock and provide pure-Python SHACL-Core fallback

- **Source:** `EOIP-master-requirements.md:2678-2678` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INV-SELF-05` | **KnowGridFlow Baseline (BL-29)** | Differential SHACL test fails due to missing dependency | **Pin pyshacl in requirements-neural.lock and provide pure-Python SHACL-Core fallback** | ``ADOPT (P0)``
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INV-SELF-05' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INV-SELF-05') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INV-SELF-05 | KnowGridFlow Baseline (BL-29) | Differential SHACL test fails due to missing dependency | Pin pyshacl in requirements-neural.lock and provide pure-Python SHACL-Core fallback | ADOPT (P0)»
- [ ] Differential SHACL test fails due to missing dependency
- [ ] Pin pyshacl in requirements-neural.lock and provide pure-Python SHACL-Core fallback
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-03 [P1] CAP-03: Multi-model and document graph storage · D01 Storage · P1

- **Source:** `EOIP-master-requirements.md:41-41` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-03` | **Multi-model and document graph storage** | D01 Storage | `P1` | 100% Implemented (Implemented (BL-26)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-03' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-03') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-03 | Multi-model and document graph storage | D01 Storage | P1 | 100% Implemented (Implemented (BL-26)) | VERIFIED»
- [ ] Multi-model and document graph storage
- [ ] 100% Implemented (Implemented (BL-26))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-06 [P1] CAP-06: Bulk load and high-throughput ingestion · D01 Storage · P1

- **Source:** `EOIP-master-requirements.md:44-44` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-06` | **Bulk load and high-throughput ingestion** | D01 Storage | `P1` | 100% Implemented (Implemented (BL-24)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-06' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-06') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-06 | Bulk load and high-throughput ingestion | D01 Storage | P1 | 100% Implemented (Implemented (BL-24)) | VERIFIED»
- [ ] Bulk load and high-throughput ingestion
- [ ] 100% Implemented (Implemented (BL-24))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-29 [P1] CAP-29: Declarative mapping (R2RML / RML) · D04 Reasoning · P1

- **Source:** `EOIP-master-requirements.md:67-67` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-29` | **Declarative mapping (R2RML / RML)** | D04 Reasoning | `P1` | 100% Implemented (Implemented (BL-33)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-29' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-29') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-29 | Declarative mapping (R2RML / RML) | D04 Reasoning | P1 | 100% Implemented (Implemented (BL-33)) | VERIFIED»
- [ ] Declarative mapping (R2RML / RML)
- [ ] 100% Implemented (Implemented (BL-33))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-35 [P1] CAP-35: Branching, diff, merge, and rollback · D05 Identity · P1

- **Source:** `EOIP-master-requirements.md:73-73` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-35` | **Branching, diff, merge, and rollback** | D05 Identity | `P1` | 100% Implemented (Implemented (BL-38)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-35' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-35') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-35 | Branching, diff, merge, and rollback | D05 Identity | P1 | 100% Implemented (Implemented (BL-38)) | VERIFIED»
- [ ] Branching, diff, merge, and rollback
- [ ] 100% Implemented (Implemented (BL-38))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-40 [P1] CAP-40: End-to-end data lineage (OpenLineage) · D05 Identity · P1

- **Source:** `EOIP-master-requirements.md:78-78` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-40` | **End-to-end data lineage (OpenLineage)** | D05 Identity | `P1` | 100% Implemented (Implemented (BL-41)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-40' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-40') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-40 | End-to-end data lineage (OpenLineage) | D05 Identity | P1 | 100% Implemented (Implemented (BL-41)) | VERIFIED»
- [ ] End-to-end data lineage (OpenLineage)
- [ ] 100% Implemented (Implemented (BL-41))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-42 [P1] CAP-42: Metadata catalog and data dictionary · D06 Ingestion · P1

- **Source:** `EOIP-master-requirements.md:80-80` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-42` | **Metadata catalog and data dictionary** | D06 Ingestion | `P1` | 100% Implemented (Implemented (BL-21, BL-42)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-42' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-42') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-42 | Metadata catalog and data dictionary | D06 Ingestion | P1 | 100% Implemented (Implemented (BL-21, BL-42)) | VERIFIED»
- [ ] Metadata catalog and data dictionary
- [ ] 100% Implemented (Implemented (BL-21, BL-42))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-57 [P1] CAP-57: Episodic and semantic agent memory · D08 Graph ML · P1

- **Source:** `EOIP-master-requirements.md:95-95` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-57` | **Episodic and semantic agent memory** | D08 Graph ML | `P1` | 100% Implemented (Implemented (BL-48, Graphiti DeepDive)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-57' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-57') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-57 | Episodic and semantic agent memory | D08 Graph ML | P1 | 100% Implemented (Implemented (BL-48, Graphiti DeepDive)) | VERIFIED»
- [ ] Episodic and semantic agent memory
- [ ] 100% Implemented (Implemented (BL-48, Graphiti DeepDive))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-62 [P1] CAP-62: In-database graph algorithm library · D08 Graph ML · P1

- **Source:** `EOIP-master-requirements.md:100-100` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-62` | **In-database graph algorithm library** | D08 Graph ML | `P1` | 100% Implemented (Implemented (BL-43)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-62' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-62') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-62 | In-database graph algorithm library | D08 Graph ML | P1 | 100% Implemented (Implemented (BL-43)) | VERIFIED»
- [ ] In-database graph algorithm library
- [ ] 100% Implemented (Implemented (BL-43))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-65 [P1] CAP-65: Temporal graph analytics · D09 Agents · P1

- **Source:** `EOIP-master-requirements.md:103-103` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-65` | **Temporal graph analytics** | D09 Agents | `P1` | 100% Implemented (Implemented (BL-37, BL-38)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-65' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-65') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-65 | Temporal graph analytics | D09 Agents | P1 | 100% Implemented (Implemented (BL-37, BL-38)) | VERIFIED»
- [ ] 100% Implemented (Implemented (BL-37, BL-38))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-67 [P1] CAP-67: Incremental code re-indexing on commit · D09 Agents · P1

- **Source:** `EOIP-master-requirements.md:105-105` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-67` | **Incremental code re-indexing on commit** | D09 Agents | `P1` | 100% Implemented (Implemented (BL-42)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-67' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-67') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-67 | Incremental code re-indexing on commit | D09 Agents | P1 | 100% Implemented (Implemented (BL-42)) | VERIFIED»
- [ ] Incremental code re-indexing on commit
- [ ] 100% Implemented (Implemented (BL-42))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-68 [P1] CAP-68: Software bill of materials (SBOM) and dependency risk · D09 Agents · P1

- **Source:** `EOIP-master-requirements.md:106-106` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-68` | **Software bill of materials (SBOM) and dependency risk** | D09 Agents | `P1` | 100% Implemented (Implemented (BL-42)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-68' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-68') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-68 | Software bill of materials (SBOM) and dependency risk | D09 Agents | P1 | 100% Implemented (Implemented (BL-42)) | VERIFIED»
- [ ] Software bill of materials (SBOM) and dependency risk
- [ ] 100% Implemented (Implemented (BL-42))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-72 [P1] CAP-72: Visual ontology authoring and Schema Studio · D09 Agents · P1

- **Source:** `EOIP-master-requirements.md:110-110` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-72` | **Visual ontology authoring and Schema Studio** | D09 Agents | `P1` | 100% Implemented (Implemented (BL-54)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-72' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-72') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-72 | Visual ontology authoring and Schema Studio | D09 Agents | P1 | 100% Implemented (Implemented (BL-54)) | VERIFIED»
- [ ] Visual ontology authoring and Schema Studio
- [ ] 100% Implemented (Implemented (BL-54))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-73 [P1] CAP-73: Time-machine playback and visual graph diff · D10 UI/UX · P1

- **Source:** `EOIP-master-requirements.md:111-111` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-73` | **Time-machine playback and visual graph diff** | D10 UI/UX | `P1` | 100% Implemented (Implemented (BL-54)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-73' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-73') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-73 | Time-machine playback and visual graph diff | D10 UI/UX | P1 | 100% Implemented (Implemented (BL-54)) | VERIFIED»
- [ ] Time-machine playback and visual graph diff
- [ ] 100% Implemented (Implemented (BL-54))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-76 [P1] CAP-76: High availability and active-passive disaster recovery · D10 UI/UX · P1

- **Source:** `EOIP-master-requirements.md:114-114` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-76` | **High availability and active-passive disaster recovery** | D10 UI/UX | `P1` | 100% Implemented (Implemented (BL-102)) | **VERIFIED**
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'CAP-76' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('CAP-76') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-76 | High availability and active-passive disaster recovery | D10 UI/UX | P1 | 100% Implemented (Implemented (BL-102)) | VERIFIED»
- [ ] High availability and active-passive disaster recovery
- [ ] 100% Implemented (Implemented (BL-102))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INV-08 [P1] INV-08: TerminusDB · Custom Prolog/Rust query language creates steep learning curves and vendor lock-in · Standard Cypher/GQL query interface over bitemporal revision vertices (EntityRevision, RelationshipRev

- **Source:** `EOIP-master-requirements.md:2671-2671` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INV-08` | **TerminusDB** | Custom Prolog/Rust query language creates steep learning curves and vendor lock-in | **Standard Cypher/GQL query interface over bitemporal revision vertices (EntityRevision, RelationshipRevision)** | ``ADOPT (P1)``
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INV-08' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INV-08') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INV-08 | TerminusDB | Custom Prolog/Rust query language creates steep learning curves and vendor lock-in | Standard Cypher/GQL query interface over bitemporal revision vertices (EntityRevision, RelationshipRevision) | ADOPT (P1)»
- [ ] Custom Prolog/Rust query language creates steep learning curves and vendor lock-in
- [ ] Standard Cypher/GQL query interface over bitemporal revision vertices (EntityRevision, RelationshipRevision)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INV-SELF-04 [P1] INV-SELF-04: KnowGridFlow Baseline (BL-10) · Custom query languages force users to learn proprietary syntax · Standardize user-facing query interfaces on openCypher / ISO GQL and natural language with query sugges

- **Source:** `EOIP-master-requirements.md:2677-2677` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INV-SELF-04` | **KnowGridFlow Baseline (BL-10)** | Custom query languages force users to learn proprietary syntax | **Standardize user-facing query interfaces on openCypher / ISO GQL and natural language with query suggestions** | ``ADOPT (P1)``
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INV-SELF-04' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INV-SELF-04') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INV-SELF-04 | KnowGridFlow Baseline (BL-10) | Custom query languages force users to learn proprietary syntax | Standardize user-facing query interfaces on openCypher / ISO GQL and natural language with query suggestions | ADOPT (P1)»
- [ ] Custom query languages force users to learn proprietary syntax
- [ ] Standardize user-facing query interfaces on openCypher / ISO GQL and natural language with query suggestions
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

