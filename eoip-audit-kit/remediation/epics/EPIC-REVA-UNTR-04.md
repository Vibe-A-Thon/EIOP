# EPIC-REVA-UNTR-04: reva-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 60 tasks, ~360.0 h, priorities {'P2': 60}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-REVA-IF-024 [P2] REVA-IF-024: GET /gates, POST /gates/{gate_id}/evaluate · Readiness gates · viewer / verifier

- **Source:** `reva-requirements.md:1236-1236` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-024 | `GET /gates`, `POST /gates/{gate_id}/evaluate` | Readiness gates | viewer / verifier
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-024' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-024') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-024 | GET /gates, POST /gates/{gate_id}/evaluate | Readiness gates | viewer / verifier»
- [ ] GET /gates, POST /gates/{gate_id}/evaluate
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-025 [P2] REVA-IF-025: POST /waivers, GET /waivers · Waivers · reviewer

- **Source:** `reva-requirements.md:1237-1237` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-025 | `POST /waivers`, `GET /waivers` | Waivers | reviewer
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-025' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-025') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-025 | POST /waivers, GET /waivers | Waivers | reviewer»
- [ ] POST /waivers, GET /waivers
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-026 [P2] REVA-IF-026: GET /attestations/{att_id}, POST /attestations/verify · Attestations · viewer

- **Source:** `reva-requirements.md:1238-1238` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-026 | `GET /attestations/{att_id}`, `POST /attestations/verify` | Attestations | viewer
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-026' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-026') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-026 | GET /attestations/{att_id}, POST /attestations/verify | Attestations | viewer»
- [ ] GET /attestations/{att_id}, POST /attestations/verify
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-031 [P2] REVA-IF-031: GET /logs/{log_id}/proof/inclusion, GET /logs/{log_id}/proof/consistency · Proofs · viewer

- **Source:** `reva-requirements.md:1240-1240` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-031 | `GET /logs/{log_id}/proof/inclusion`, `GET /logs/{log_id}/proof/consistency` | Proofs | viewer
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-031' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-031') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-031 | GET /logs/{log_id}/proof/inclusion, GET /logs/{log_id}/proof/consistency | Proofs | viewer»
- [ ] GET /logs/{log_id}/proof/inclusion, GET /logs/{log_id}/proof/consistency
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-040 [P2] REVA-IF-040: POST /artifacts (upload, streaming) , GET /artifacts/{artifact_id}, GET /artifacts/{id}/inventory (view) · Artifacts · analyst

- **Source:** `reva-requirements.md:1241-1241` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-040 | `POST /artifacts` (upload, streaming) , `GET /artifacts/{artifact_id}`, `GET /artifacts/{id}/inventory` (view) | Artifacts | analyst
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-040' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-040') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-040 | POST /artifacts (upload, streaming) , GET /artifacts/{artifact_id}, GET /artifacts/{id}/inventory (view) | Artifacts | analyst»
- [ ] POST /artifacts (upload, streaming) , GET /artifacts/{artifact_id}, GET /artifacts/{id}/inventory (view)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-041 [P2] REVA-IF-041: POST /provenance/analyze (artifact or image), `GET /sbom/{artifact_id}?format=cyclonedx\ · spdx` · Provenance/SBOM

- **Source:** `reva-requirements.md:1242-1242` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-041 | `POST /provenance/analyze` (artifact or image), `GET /sbom/{artifact_id}?format=cyclonedx\|spdx` | Provenance/SBOM | analyst
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-041' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-041') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-041 | POST /provenance/analyze (artifact or image), `GET /sbom/{artifact_id}?format=cyclonedx\ | spdx` | Provenance/SBOM | analyst»
- [ ] POST /provenance/analyze (artifact or image), `GET /sbom/{artifact_id}?format=cyclonedx\
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-042 [P2] REVA-IF-042: POST /boundaries/extract (repo, commit, incremental), GET /services, GET /services/{id}/boundaries · Boundaries · analyst

- **Source:** `reva-requirements.md:1243-1243` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-042 | `POST /boundaries/extract` (repo, commit, incremental), `GET /services`, `GET /services/{id}/boundaries` | Boundaries | analyst
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-042' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-042') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-042 | POST /boundaries/extract (repo, commit, incremental), GET /services, GET /services/{id}/boundaries | Boundaries | analyst»
- [ ] POST /boundaries/extract (repo, commit, incremental), GET /services, GET /services/{id}/boundaries
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-043 [P2] REVA-IF-043: POST /apisurface/ingest (HAR/OTLP/log upload or connector source), GET /apisurface/operations · API surface · analyst

- **Source:** `reva-requirements.md:1244-1244` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-043 | `POST /apisurface/ingest` (HAR/OTLP/log upload or connector source), `GET /apisurface/operations` | API surface | analyst
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-043' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-043') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-043 | POST /apisurface/ingest (HAR/OTLP/log upload or connector source), GET /apisurface/operations | API surface | analyst»
- [ ] POST /apisurface/ingest (HAR/OTLP/log upload or connector source), GET /apisurface/operations
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-044 [P2] REVA-IF-044: POST /dbschema/introspect (connection id), GET /dbschema/{db_instance} · DB schema · analyst

- **Source:** `reva-requirements.md:1245-1245` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-044 | `POST /dbschema/introspect` (connection id), `GET /dbschema/{db_instance}` | DB schema | analyst
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-044' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-044') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-044 | POST /dbschema/introspect (connection id), GET /dbschema/{db_instance} | DB schema | analyst»
- [ ] POST /dbschema/introspect (connection id), GET /dbschema/{db_instance}
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-045 [P2] REVA-IF-045: POST /reconcile (service scope, window) · Reconciliation · analyst

- **Source:** `reva-requirements.md:1246-1246` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-045 | `POST /reconcile` (service scope, window) | Reconciliation | analyst
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-045' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-045') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-045 | POST /reconcile (service scope, window) | Reconciliation | analyst»
- [ ] POST /reconcile (service scope, window)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-046 [P2] REVA-IF-046: POST /binaries/analyze (upload/digest), GET /binaries/{digest}/functions, GET /binaries/{digest}/functions/{offset}/cfg, GET /binaries/{digest}/functions/{offset}/decompiled · Binary disassembly, CFG 

- **Source:** `reva-requirements.md:1247-1247` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-046 | `POST /binaries/analyze` (upload/digest), `GET /binaries/{digest}/functions`, `GET /binaries/{digest}/functions/{offset}/cfg`, `GET /binaries/{digest}/functions/{offset}/decompiled` | Binary disassembly, CFG & decompiler AST | analyst
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-046' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-046') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-046 | POST /binaries/analyze (upload/digest), GET /binaries/{digest}/functions, GET /binaries/{digest}/functions/{offset}/cfg, GET /binaries/{digest}/functions/{offset}/decompiled | Binary disassembly, CFG & decompiler AST | analyst»
- [ ] POST /binaries/analyze (upload/digest), GET /binaries/{digest}/functions, GET /binaries/{digest}/functions/{offset}/cfg, GET /binaries/{digest}/functions/{offset}/decompiled
- [ ] Binary disassembly, CFG & decompiler AST
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-047 [P2] REVA-IF-047: POST /mobile/analyze (APK/IPA upload/digest), GET /mobile/{digest}/manifest, GET /mobile/{digest}/components, GET /mobile/{digest}/jni-bridges · Mobile triage & JNI mapping · analyst

- **Source:** `reva-requirements.md:1248-1248` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-047 | `POST /mobile/analyze` (APK/IPA upload/digest), `GET /mobile/{digest}/manifest`, `GET /mobile/{digest}/components`, `GET /mobile/{digest}/jni-bridges` | Mobile triage & JNI mapping | analyst
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-047' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-047') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-047 | POST /mobile/analyze (APK/IPA upload/digest), GET /mobile/{digest}/manifest, GET /mobile/{digest}/components, GET /mobile/{digest}/jni-bridges | Mobile triage & JNI mapping | analyst»
- [ ] POST /mobile/analyze (APK/IPA upload/digest), GET /mobile/{digest}/manifest, GET /mobile/{digest}/components, GET /mobile/{digest}/jni-bridges
- [ ] Mobile triage & JNI mapping
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-051 [P2] REVA-IF-051: POST /diff (two selectors), GET /diff/{diff_id} · Graph diff · viewer

- **Source:** `reva-requirements.md:1252-1252` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-051 | `POST /diff` (two selectors), `GET /diff/{diff_id}` | Graph diff | viewer
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-051' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-051') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-051 | POST /diff (two selectors), GET /diff/{diff_id} | Graph diff | viewer»
- [ ] POST /diff (two selectors), GET /diff/{diff_id}
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-052 [P2] REVA-IF-052: POST /drift/verify (artifact, expected commit) · Drift verification · analyst

- **Source:** `reva-requirements.md:1253-1253` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-052 | `POST /drift/verify` (artifact, expected commit) | Drift verification | analyst
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-052' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-052') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-052 | POST /drift/verify (artifact, expected commit) | Drift verification | analyst»
- [ ] POST /drift/verify (artifact, expected commit)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-053 [P2] REVA-IF-053: POST /browser/observe (scenario definition), GET /browser/sessions/{id}, GET /browser/sessions/{id}/attestation · Supervised CDP observation & UI attestation · analyst

- **Source:** `reva-requirements.md:1254-1254` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-053 | `POST /browser/observe` (scenario definition), `GET /browser/sessions/{id}`, `GET /browser/sessions/{id}/attestation` | Supervised CDP observation & UI attestation | analyst
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-053' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-053') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-053 | POST /browser/observe (scenario definition), GET /browser/sessions/{id}, GET /browser/sessions/{id}/attestation | Supervised CDP observation & UI attestation | analyst»
- [ ] POST /browser/observe (scenario definition), GET /browser/sessions/{id}, GET /browser/sessions/{id}/attestation
- [ ] Supervised CDP observation & UI attestation
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-054 [P2] REVA-IF-054: POST /diff/binaries (base digest vs target digest, options), GET /diff/binaries/{id} · Binary CFG isomorphism & logic diff · viewer

- **Source:** `reva-requirements.md:1255-1255` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-054 | `POST /diff/binaries` (base digest vs target digest, options), `GET /diff/binaries/{id}` | Binary CFG isomorphism & logic diff | viewer
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-054' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-054') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-054 | POST /diff/binaries (base digest vs target digest, options), GET /diff/binaries/{id} | Binary CFG isomorphism & logic diff | viewer»
- [ ] POST /diff/binaries (base digest vs target digest, options), GET /diff/binaries/{id}
- [ ] Binary CFG isomorphism & logic diff
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-060 [P2] REVA-IF-060: POST /answers/ground (question + optional template) → answer contract · Grounded answers · viewer

- **Source:** `reva-requirements.md:1256-1256` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-060 | `POST /answers/ground` (question + optional template) → answer contract | Grounded answers | viewer
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-060' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-060') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-060 | POST /answers/ground (question + optional template) → answer contract | Grounded answers | viewer»
- [ ] POST /answers/ground (question + optional template) → answer contract
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-061 [P2] REVA-IF-061: POST /eval/runs (suite), GET /eval/runs/{id} · Evaluation · analyst

- **Source:** `reva-requirements.md:1257-1257` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-061 | `POST /eval/runs` (suite), `GET /eval/runs/{id}` | Evaluation | analyst
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-061' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-061') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-061 | POST /eval/runs (suite), GET /eval/runs/{id} | Evaluation | analyst»
- [ ] POST /eval/runs (suite), GET /eval/runs/{id}
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-070 [P2] REVA-IF-070: GET /views/{parent_id} (view request params) · Views/paging · viewer

- **Source:** `reva-requirements.md:1258-1258` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-070 | `GET /views/{parent_id}` (view request params) | Views/paging | viewer
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-070' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-070') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-070 | GET /views/{parent_id} (view request params) | Views/paging | viewer»
- [ ] GET /views/{parent_id} (view request params)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-071 [P2] REVA-IF-071: GET /jobs/{job_id}, GET /jobs/{job_id}/events (SSE), POST /jobs/{job_id}/cancel · Jobs · owner of job

- **Source:** `reva-requirements.md:1259-1259` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-071 | `GET /jobs/{job_id}`, `GET /jobs/{job_id}/events` (SSE), `POST /jobs/{job_id}/cancel` | Jobs | owner of job
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-071' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-071') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-071 | GET /jobs/{job_id}, GET /jobs/{job_id}/events (SSE), POST /jobs/{job_id}/cancel | Jobs | owner of job»
- [ ] GET /jobs/{job_id}, GET /jobs/{job_id}/events (SSE), POST /jobs/{job_id}/cancel
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-080 [P2] REVA-IF-080: GET /doctor · Readiness · admin

- **Source:** `reva-requirements.md:1260-1260` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-080 | `GET /doctor` | Readiness | admin
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-080' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-080') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-080 | GET /doctor | Readiness | admin»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-081 [P2] REVA-IF-081: GET /policies, PUT /policies/{name} · Policies · admin

- **Source:** `reva-requirements.md:1261-1261` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-081 | `GET /policies`, `PUT /policies/{name}` | Policies | admin
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-081' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-081') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-081 | GET /policies, PUT /policies/{name} | Policies | admin»
- [ ] GET /policies, PUT /policies/{name}
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-KG-002 [P2] REVA-KG-002: Optimistic concurrency: updates require expected_revision; a mismatch returns REVA_E_CONFLICT with the current head. · Two concurrent updates: one succeeds, one gets a conflict. · integration

- **Source:** `reva-requirements.md:719-719` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-KG-002 | Optimistic concurrency: updates require `expected_revision`; a mismatch returns `REVA_E_CONFLICT` with the current head. | Two concurrent updates: one succeeds, one gets a conflict. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-KG-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-KG-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Two concurrent updates: one succeeds, one gets a conflict
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-KG-003 [P2] REVA-KG-003: State machine: `open → investigating → (blocked \ · contradicted \ · resolved \

- **Source:** `reva-requirements.md:720-720` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-KG-003 | State machine: `open → investigating → (blocked \| contradicted \| resolved \| withdrawn \| out_of_scope)`, `blocked → investigating`, `contradicted → investigating`, `resolved → open` (reopen on new contradicting evidence). Invalid transitions are rejected. | Table-driven test of all allowed and disallowed transitions. | unit
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-KG-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-KG-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Table-driven test of all allowed and disallowed transitions
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-KG-005 [P2] REVA-KG-005: Impact score: impact_score_bp = severity_weight × (1 + log2(1 + downstream_entity_count)) × blocked_obligation_factor, normalized to 0–10000, recomputed on graph changes touching the scope (debounced)

- **Source:** `reva-requirements.md:722-722` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-KG-005 | Impact score: `impact_score_bp = severity_weight × (1 + log2(1 + downstream_entity_count)) × blocked_obligation_factor`, normalized to 0–10000, recomputed on graph changes touching the scope (debounced). Weights are configurable (`REVA_GAP_WEIGHTS`). | Golden test on a fixture graph; ordering of the gap board matches expected priority. | component
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-KG-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-KG-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Golden test on a fixture graph; ordering of the gap board matches expected priority
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-KG-006 [P2] REVA-KG-006: Probes: each recommended probe is executable when auto_executable=true and the tenant policy allows automatic probes (REVA_AUTO_PROBES). Execution results become warrants linked to the gap; a probe ne

- **Source:** `reva-requirements.md:723-723` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-KG-006 | Probes: each recommended probe is executable when `auto_executable=true` and the tenant policy allows automatic probes (`REVA_AUTO_PROBES`). Execution results become warrants linked to the gap; a probe never mutates source systems. | A connector-sync probe runs, issues warrants and moves the gap to `investigating`. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-KG-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-KG-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] A connector-sync probe runs, issues warrants and moves the gap to investigating
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-KG-007 [P2] REVA-KG-007: Automatic gap creation: workflows create gaps for (a) partial/unknown coverage on a material question, (b) ambiguous matches (endpoint matching, diff matching, entity resolution), (c) runtime-only obs

- **Source:** `reva-requirements.md:724-724` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-KG-007 | Automatic gap creation: workflows create gaps for (a) partial/unknown coverage on a material question, (b) ambiguous matches (endpoint matching, diff matching, entity resolution), (c) runtime-only observations without static source, (d) missing commits for shipped revisions, (e) unresolved trace frontiers. Each kind has a template (§10.5). | Each of the five triggers creates exactly one gap per scope (deduplicated by identity). | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-KG-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-KG-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Each of the five triggers creates exactly one gap per scope (deduplicated by identity)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-KG-008 [P2] REVA-KG-008: Gap board API and UI: filter by status, severity, owner, domain, entity; bulk assign; SLA breach highlighting. · Acceptance journey RJ-05. · acceptance

- **Source:** `reva-requirements.md:725-725` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-KG-008 | Gap board API and UI: filter by status, severity, owner, domain, entity; bulk assign; SLA breach highlighting. | Acceptance journey RJ-05. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-KG-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-KG-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-KG-008 | Gap board API and UI: filter by status, severity, owner, domain, entity; bulk assign; SLA breach highlighting. | Acceptance journey RJ-05. | acceptance»
- [ ] Gap board API and UI: filter by status, severity, owner, domain, entity; bulk assign; SLA breach highlighting.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-MB-005 [P2] REVA-MB-005: JNI & Native Bridge cross-layer mapper. Identifies Java/Kotlin native method declarations, loads associated .so shared objects from lib/<abi>/, and links Java native methods to C/C++ exported symbols 

- **Source:** `reva-requirements.md:1105-1105` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-MB-005 | JNI & Native Bridge cross-layer mapper. Identifies Java/Kotlin `native` method declarations, loads associated `.so` shared objects from `lib/<abi>/`, and links Java native methods to C/C++ exported symbols (`Java_com_example_...`) via `reva_CALLS_NATIVE` edges. | Successfully links Java native method call in DEX to disassembled C function in embedded ARM64 `.so`; emits cross-layer warrant binding Java boundary to native binary function. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-MB-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-MB-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Successfully links Java native method call in DEX to disassembled C function in embedded ARM64 .so; emits cross-layer warrant binding Java boundary to native binary function
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-MB-006 [P2] REVA-MB-006: Safe read-only ADB triage adapter. Connects over loopback interface to local Android emulators or tethered devices; executes non-invasive read-only commands (pm list packages, pm dump, dumpsys package

- **Source:** `reva-requirements.md:1106-1106` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-MB-006 | Safe read-only ADB triage adapter. Connects over loopback interface to local Android emulators or tethered devices; executes non-invasive read-only commands (`pm list packages`, `pm dump`, `dumpsys package`); rejects any write or modification commands. | Queries package state on emulator; rejects any `install`, `uninstall`, `shell rm`, or state-modifying ADB command with `REVA_ERR_SECURITY_VIOLATION`. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-MB-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-MB-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Queries package state on emulator; rejects any install, uninstall, shell rm, or state-modifying ADB command with REVAERRSECURITYVIOLATION
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-MC-003 [P2] REVA-MC-003: Tool shapes follow §9.2 categories (inspect, search, trace, compare, workflow, record, verify). No tool mixes discovery, execution and mutation modes. · Static review checklist in CI (tool metadata de

- **Source:** `reva-requirements.md:987-987` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-MC-003 | Tool shapes follow §9.2 categories (inspect, search, trace, compare, workflow, record, verify). No tool mixes discovery, execution and mutation modes. | Static review checklist in CI (tool metadata declares shape and effects). | static
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-MC-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-MC-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Static review checklist in CI (tool metadata declares shape and effects)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-MC-005 [P2] REVA-MC-005: Untrusted-content marking: results that can include ingested content carry _meta.reva.untrusted_content = true and the content is wrapped in delimited fields (never interpolated into instructions). · 

- **Source:** `reva-requirements.md:989-989` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-MC-005 | Untrusted-content marking: results that can include ingested content carry `_meta.reva.untrusted_content = true` and the content is wrapped in delimited fields (never interpolated into instructions). | Marker present on every content-bearing tool (test enumerates the catalogue). | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-MC-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-MC-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Marker present on every content-bearing tool (test enumerates the catalogue)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-MC-008 [P2] REVA-MC-008: API versioning: path version v1; additive changes only within v1; breaking changes require v2 plus a deprecation window documented in CONTRACTS.md. · Contract snapshot test fails on breaking changes w

- **Source:** `reva-requirements.md:992-992` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-MC-008 | API versioning: path version `v1`; additive changes only within v1; breaking changes require `v2` plus a deprecation window documented in `CONTRACTS.md`. | Contract snapshot test fails on breaking changes without a version bump. | static
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-MC-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-MC-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Contract snapshot test fails on breaking changes without a version bump
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-MC-009 [P2] REVA-MC-009: Contract documentation docs/reva/CONTRACTS.md generated from code (endpoints, tools, schemas, errors, examples) by kgf reva docs generate; CI fails if it is stale. · Docs check in CI. · static

- **Source:** `reva-requirements.md:993-993` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-MC-009 | Contract documentation `docs/reva/CONTRACTS.md` generated from code (endpoints, tools, schemas, errors, examples) by `kgf reva docs generate`; CI fails if it is stale. | Docs check in CI. | static
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-MC-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-MC-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Docs check in CI
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NB-004 [P2] REVA-NB-004: Control Flow Graph (CFG) and Basic Block extraction. Identifies leaders, basic block boundaries, branch conditions, fallthrough targets, jump tables, and cyclomatic complexity ($M = E - N + 2P$). · Ba

- **Source:** `reva-requirements.md:1084-1084` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NB-004 | Control Flow Graph (CFG) and Basic Block extraction. Identifies leaders, basic block boundaries, branch conditions, fallthrough targets, jump tables, and cyclomatic complexity ($M = E - N + 2P$). | Basic blocks and branch edges extracted for complex functions (if/else, loops, switch statements); cyclomatic complexity calculation verified against ground truth; graph matches golden CFG representation. | component
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NB-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NB-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Basic blocks and branch edges extracted for complex functions (if/else, loops, switch statements); cyclomatic complexity calculation verified against ground truth; graph matches golden CFG representation
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NB-005 [P2] REVA-NB-005: Function boundary detection and symbol resolution. Combines export tables, symbol tables (.symtab, .dynsym), exception handling unwind info (.eh_frame), and recursive descent disassembly heuristics to

- **Source:** `reva-requirements.md:1085-1085` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NB-005 | Function boundary detection and symbol resolution. Combines export tables, symbol tables (`.symtab`, `.dynsym`), exception handling unwind info (`.eh_frame`), and recursive descent disassembly heuristics to detect non-exported internal functions. | Recovers all internal non-exported function offsets in stripped and non-stripped test binaries; emits `reva_BinaryFunction` entities with unique logical keys `nb:<sha256>:func:<offset>`. | component
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NB-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NB-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Recovers all internal non-exported function offsets in stripped and non-stripped test binaries; emits revaBinaryFunction entities with unique logical keys nb:<sha256>:func:<offset>
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NB-006 [P2] REVA-NB-006: String literal and cross-reference (xref) extractor. Scans .rodata, .rdata, and text segments for ASCII/UTF-8/UTF-16 strings; traces data references from instructions to string offsets; identifies URL

- **Source:** `reva-requirements.md:1086-1086` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NB-006 | String literal and cross-reference (xref) extractor. Scans `.rodata`, `.rdata`, and text segments for ASCII/UTF-8/UTF-16 strings; traces data references from instructions to string offsets; identifies URLs, IP addresses, format strings, and cryptographic constants. | Emits string xref warrants linking referencing basic blocks to string resources; extracts all embedded URLs and SQL queries with offset locations. | unit
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NB-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NB-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Emits string xref warrants linking referencing basic blocks to string resources; extracts all embedded URLs and SQL queries with offset locations
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-001 [P2] REVA-NFR-001: Warrant issue throughput ≥ 1,000 warrants/s in batch mode (≤ 4 KiB statements, blobs ≤ 64 KiB) on PostgreSQL; ≥ 300/s on SQLite

- **Source:** `reva-requirements.md:1191-1191` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-001 | Warrant issue throughput ≥ 1,000 warrants/s in batch mode (≤ 4 KiB statements, blobs ≤ 64 KiB) on PostgreSQL; ≥ 300/s on SQLite. | `tests/reva/perf/test_issue_throughput.py`, 5 runs, median reported
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-001 | Warrant issue throughput ≥ 1,000 warrants/s in batch mode (≤ 4 KiB statements, blobs ≤ 64 KiB) on PostgreSQL; ≥ 300/s on SQLite. | tests/reva/perf/test_issue_throughput.py, 5 runs, median reported»
- [ ] Warrant issue throughput ≥ 1,000 warrants/s in batch mode (≤ 4 KiB statements, blobs ≤ 64 KiB) on PostgreSQL; ≥ 300/s on SQLite.
- [ ] tests/reva/perf/test_issue_throughput.py, 5 runs, median reported
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-002 [P2] REVA-NFR-002: Single issue() latency p95 ≤ 25 ms (excluding blobs > 1 MiB)

- **Source:** `reva-requirements.md:1192-1192` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-002 | Single `issue()` latency p95 ≤ 25 ms (excluding blobs > 1 MiB). | Same harness
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-002 | Single issue() latency p95 ≤ 25 ms (excluding blobs > 1 MiB). | Same harness»
- [ ] Single issue() latency p95 ≤ 25 ms (excluding blobs > 1 MiB).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-004 [P2] REVA-NFR-004: Impact trace p95 ≤ 3 s for depth ≤ 6 and ≤ 50,000 traversed edges on HugeGraph and Neo4j; the result includes coverage and frontier

- **Source:** `reva-requirements.md:1194-1194` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-004 | Impact trace p95 ≤ 3 s for depth ≤ 6 and ≤ 50,000 traversed edges on HugeGraph and Neo4j; the result includes coverage and frontier. | `perf/test_trace.py` on the synthetic 1M-edge enterprise fixture
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-004 | Impact trace p95 ≤ 3 s for depth ≤ 6 and ≤ 50,000 traversed edges on HugeGraph and Neo4j; the result includes coverage and frontier. | perf/test_trace.py on the synthetic 1M-edge enterprise fixture»
- [ ] Impact trace p95 ≤ 3 s for depth ≤ 6 and ≤ 50,000 traversed edges on HugeGraph and Neo4j; the result includes coverage and frontier.
- [ ] perf/test_trace.py on the synthetic 1M-edge enterprise fixture
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-005 [P2] REVA-NFR-005: Boundary extraction ≥ 1,500 source files/min per worker; incremental re-extraction of a 1-file change in a 10k-file repo ≤ 20 s

- **Source:** `reva-requirements.md:1195-1195` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-005 | Boundary extraction ≥ 1,500 source files/min per worker; incremental re-extraction of a 1-file change in a 10k-file repo ≤ 20 s. | `perf/test_ab.py`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-005 | Boundary extraction ≥ 1,500 source files/min per worker; incremental re-extraction of a 1-file change in a 10k-file repo ≤ 20 s. | perf/test_ab.py»
- [ ] Boundary extraction ≥ 1,500 source files/min per worker; incremental re-extraction of a 1-file change in a 10k-file repo ≤ 20 s.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-006 [P2] REVA-NFR-006: API surface mining ≥ 100,000 log records/s per worker for access logs; memory ≤ 512 MiB at 10M records

- **Source:** `reva-requirements.md:1196-1196` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-006 | API surface mining ≥ 100,000 log records/s per worker for access logs; memory ≤ 512 MiB at 10M records. | `perf/test_as.py`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-006 | API surface mining ≥ 100,000 log records/s per worker for access logs; memory ≤ 512 MiB at 10M records. | perf/test_as.py»
- [ ] API surface mining ≥ 100,000 log records/s per worker for access logs; memory ≤ 512 MiB at 10M records.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-007 [P2] REVA-NFR-007: Artifact inventory of a 1 GiB JAR/OCI image ≤ 90 s; memory ≤ 1 GiB

- **Source:** `reva-requirements.md:1197-1197` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-007 | Artifact inventory of a 1 GiB JAR/OCI image ≤ 90 s; memory ≤ 1 GiB. | `perf/test_ai.py`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-007 | Artifact inventory of a 1 GiB JAR/OCI image ≤ 90 s; memory ≤ 1 GiB. | perf/test_ai.py»
- [ ] Artifact inventory of a 1 GiB JAR/OCI image ≤ 90 s; memory ≤ 1 GiB.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-008 [P2] REVA-NFR-008: Transparency log append p95 ≤ 5 ms; inclusion proof generation ≤ 20 ms at 100M leaves (logarithmic node cache)

- **Source:** `reva-requirements.md:1198-1198` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-008 | Transparency log append p95 ≤ 5 ms; inclusion proof generation ≤ 20 ms at 100M leaves (logarithmic node cache). | `perf/test_tl.py` (simulated sizes)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-008 | Transparency log append p95 ≤ 5 ms; inclusion proof generation ≤ 20 ms at 100M leaves (logarithmic node cache). | perf/test_tl.py (simulated sizes)»
- [ ] Transparency log append p95 ≤ 5 ms; inclusion proof generation ≤ 20 ms at 100M leaves (logarithmic node cache).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-009 [P2] REVA-NFR-009: UI: views render first content ≤ 1.5 s, interactions p95 ≤ 200 ms for pages ≤ 500 rows; graph views ≤ 2,000 rendered elements

- **Source:** `reva-requirements.md:1199-1199` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-009 | UI: views render first content ≤ 1.5 s, interactions p95 ≤ 200 ms for pages ≤ 500 rows; graph views ≤ 2,000 rendered elements. | Playwright performance marks
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-009 | UI: views render first content ≤ 1.5 s, interactions p95 ≤ 200 ms for pages ≤ 500 rows; graph views ≤ 2,000 rendered elements. | Playwright performance marks»
- [ ] UI: views render first content ≤ 1.5 s, interactions p95 ≤ 200 ms for pages ≤ 500 rows; graph views ≤ 2,000 rendered elements.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-010 [P2] REVA-NFR-010: Availability: REVA failures degrade gracefully; KGF core keeps working with REVA disabled or down (flags), and REVA health reports degraded/down

- **Source:** `reva-requirements.md:1200-1200` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-010 | Availability: REVA failures degrade gracefully; KGF core keeps working with REVA disabled or down (flags), and REVA health reports `degraded`/`down`. | Chaos test: stop the REVA worker; KGF core journeys still pass
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-010 | Availability: REVA failures degrade gracefully; KGF core keeps working with REVA disabled or down (flags), and REVA health reports degraded/down. | Chaos test: stop the REVA worker; KGF core journeys still pass»
- [ ] Availability: REVA failures degrade gracefully; KGF core keeps working with REVA disabled or down (flags), and REVA health reports degraded/down.
- [ ] Chaos test: stop the REVA worker; KGF core journeys still pass
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-012 [P2] REVA-NFR-012: Determinism: identical inputs produce identical warrant IDs, trace IDs, diff IDs and ledger IDs across runs, machines and backends

- **Source:** `reva-requirements.md:1202-1202` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-012 | Determinism: identical inputs produce identical warrant IDs, trace IDs, diff IDs and ledger IDs across runs, machines and backends. | Determinism suite run twice on two CI runners; IDs compared
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-012 | Determinism: identical inputs produce identical warrant IDs, trace IDs, diff IDs and ledger IDs across runs, machines and backends. | Determinism suite run twice on two CI runners; IDs compared»
- [ ] Determinism: identical inputs produce identical warrant IDs, trace IDs, diff IDs and ledger IDs across runs, machines and backends.
- [ ] Determinism suite run twice on two CI runners; IDs compared
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-015 [P2] REVA-NFR-015: Scalability: warrant store tested to 100M warrants (partitioned by tenant and month on PostgreSQL); indexes on (tenantid, subjectkey), (tenantid, predicate), (tenantid, recordedat), link table indexes

- **Source:** `reva-requirements.md:1205-1205` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-015 | Scalability: warrant store tested to 100M warrants (partitioned by tenant and month on PostgreSQL); indexes on `(tenant_id, subject_key)`, `(tenant_id, predicate)`, `(tenant_id, recorded_at)`, link table indexes. | Synthetic load test (nightly lane)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-015' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-015') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-015 | Scalability: warrant store tested to 100M warrants (partitioned by tenant and month on PostgreSQL); indexes on (tenant_id, subject_key), (tenant_id, predicate), (tenant_id, recorded_at), link table indexes. | Synthetic load test (nightly lane)»
- [ ] Scalability: warrant store tested to 100M warrants (partitioned by tenant and month on PostgreSQL); indexes on (tenant_id, subject_key), (tenant_id, predicate), (tenant_id, recorded_at), link table indexes.
- [ ] Synthetic load test (nightly lane)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-016 [P2] REVA-NFR-016: Accessibility WCAG 2.2 AA; i18n: all UI strings in resource bundles (en default; structure ready for more locales); dates and numbers localized

- **Source:** `reva-requirements.md:1206-1206` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-016 | Accessibility WCAG 2.2 AA; i18n: all UI strings in resource bundles (en default; structure ready for more locales); dates and numbers localized. | axe + i18n lint
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-016' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-016') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-016 | Accessibility WCAG 2.2 AA; i18n: all UI strings in resource bundles (en default; structure ready for more locales); dates and numbers localized. | axe + i18n lint»
- [ ] Accessibility WCAG 2.2 AA; i18n: all UI strings in resource bundles (en default; structure ready for more locales); dates and numbers localized.
- [ ] axe + i18n lint
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-017 [P2] REVA-NFR-017: Code quality: type-checked (mypy strict for reva/), lint clean (ruff), no duplicated blocks > 40 lines (jscpd or ruff equivalent), no dead code (vulture with allowlist)

- **Source:** `reva-requirements.md:1207-1207` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-017 | Code quality: type-checked (mypy strict for `reva/`), lint clean (ruff), no duplicated blocks > 40 lines (jscpd or ruff equivalent), no dead code (vulture with allowlist). | CI static lane
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-017' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-017') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-017 | Code quality: type-checked (mypy strict for reva/), lint clean (ruff), no duplicated blocks > 40 lines (jscpd or ruff equivalent), no dead code (vulture with allowlist). | CI static lane»
- [ ] Code quality: type-checked (mypy strict for reva/), lint clean (ruff), no duplicated blocks > 40 lines (jscpd or ruff equivalent), no dead code (vulture with allowlist).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-018 [P2] REVA-NFR-018: Test coverage: line ≥ 90% and branch ≥ 85% for reva/core, reva/kernel, reva/pd; ≥ 80% line for other packages. Coverage is a floor, never proof of completion (§0.4)

- **Source:** `reva-requirements.md:1208-1208` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-018 | Test coverage: line ≥ 90% and branch ≥ 85% for `reva/core`, `reva/kernel`, `reva/pd`; ≥ 80% line for other packages. **Coverage is a floor, never proof of completion** (§0.4). | CI coverage lane
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-018' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-018') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-018 | Test coverage: line ≥ 90% and branch ≥ 85% for reva/core, reva/kernel, reva/pd; ≥ 80% line for other packages. Coverage is a floor, never proof of completion (§0.4). | CI coverage lane»
- [ ] Test coverage: line ≥ 90% and branch ≥ 85% for reva/core, reva/kernel, reva/pd; ≥ 80% line for other packages. Coverage is a floor, never proof of completion (§0.4).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-019 [P2] REVA-NFR-019: Mutation score (REVA's own probe, REVA-PD-005) ≥ 0.75 for reva/core, reva/kernel, reva/pd

- **Source:** `reva-requirements.md:1209-1209` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-019 | Mutation score (REVA's own probe, REVA-PD-005) ≥ 0.75 for `reva/core`, `reva/kernel`, `reva/pd`. | Nightly lane
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-019' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-019') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-019 | Mutation score (REVA's own probe, REVA-PD-005) ≥ 0.75 for reva/core, reva/kernel, reva/pd. | Nightly lane»
- [ ] Mutation score (REVA's own probe, REVA-PD-005) ≥ 0.75 for reva/core, reva/kernel, reva/pd.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-020 [P2] REVA-NFR-020: Security: dependency audit (pip-audit, npm audit) with no known high/critical vulnerabilities at release; SBOM of REVA itself generated by REVA (dogfooding SP)

- **Source:** `reva-requirements.md:1210-1210` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-020 | Security: dependency audit (pip-audit, npm audit) with no known high/critical vulnerabilities at release; SBOM of REVA itself generated by REVA (dogfooding SP). | Release lane
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-020' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-020') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-020 | Security: dependency audit (pip-audit, npm audit) with no known high/critical vulnerabilities at release; SBOM of REVA itself generated by REVA (dogfooding SP). | Release lane»
- [ ] Security: dependency audit (pip-audit, npm audit) with no known high/critical vulnerabilities at release; SBOM of REVA itself generated by REVA (dogfooding SP).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-030 [P2] REVA-NFR-030: Contract stability: semantic versioning of REST/MCP/warrant schemas; a migration tool for warrant schema versions (reva.warrant/1 → future versions) without changing existing IDs

- **Source:** `reva-requirements.md:1211-1211` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-030 | Contract stability: semantic versioning of REST/MCP/warrant schemas; a migration tool for warrant schema versions (`reva.warrant/1` → future versions) without changing existing IDs. | Contract snapshot tests
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-030' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-030') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-030 | Contract stability: semantic versioning of REST/MCP/warrant schemas; a migration tool for warrant schema versions (reva.warrant/1 → future versions) without changing existing IDs. | Contract snapshot tests»
- [ ] Contract stability: semantic versioning of REST/MCP/warrant schemas; a migration tool for warrant schema versions (reva.warrant/1 → future versions) without changing existing IDs.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-OB-001 [P2] REVA-OB-001: Prometheus metrics: reva_warrants_issued_total{predicate,producer_type}, reva_issue_seconds (histogram), reva_translog_size{log}, reva_sth_age_seconds, reva_integrity_violations_total, reva_closure_st

- **Source:** `reva-requirements.md:1062-1062` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-OB-001 | Prometheus metrics: `reva_warrants_issued_total{predicate,producer_type}`, `reva_issue_seconds` (histogram), `reva_translog_size{log}`, `reva_sth_age_seconds`, `reva_integrity_violations_total`, `reva_closure_status{status}`, `reva_verifier_run_seconds{profile}`, `reva_sandbox_failures_total{reason}`, `reva_extractor_seconds{extractor}`, `reva_coverage_partial_total{producer}`, `reva_view_budget_overflows_total`, `reva_gaps_open{severity}`, `reva_contradictions_open`. | `/metrics` scrape test lists all metrics. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-OB-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-OB-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] /metrics scrape test lists all metrics
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-OB-003 [P2] REVA-OB-003: OpenTelemetry traces for REVA workflows and extractor jobs (exported to KGF's collector if configured; no-op otherwise). · Span names present in an in-memory exporter test. · integration

- **Source:** `reva-requirements.md:1064-1064` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-OB-003 | OpenTelemetry traces for REVA workflows and extractor jobs (exported to KGF's collector if configured; no-op otherwise). | Span names present in an in-memory exporter test. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-OB-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-OB-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Span names present in an in-memory exporter test
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-PD-008 [P2] REVA-PD-008: Jira integration: (a) propose obligations from a story's acceptance criteria (one candidate per criterion, layer guessed, review empty, disposition active only after human review); (b) write back noth

- **Source:** `reva-requirements.md:791-791` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-PD-008 | Jira integration: (a) propose obligations from a story's acceptance criteria (one candidate per criterion, layer guessed, `review` empty, disposition `active` only after human review); (b) write back nothing to Jira by default (`REVA_JIRA_WRITEBACK=false`); (c) show per-story closure status in KGF. When write-back is enabled, write only a comment containing the ledger summary and a link. | Candidate obligations are created from a fixture story with 4 criteria; no Jira write occurs by default (asserted via connector call log). | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-PD-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-PD-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Candidate obligations are created from a fixture story with 4 criteria; no Jira write occurs by default (asserted via connector call log)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-PD-010 [P2] REVA-PD-010: Board integration (IP-08): KGF completion boards read done-status from REVA ledgers via REST. A board item is "Done" only if its linked obligations are closed. Manual status changes on boards are reco

- **Source:** `reva-requirements.md:793-793` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-PD-010 | Board integration (IP-08): KGF completion boards read done-status from REVA ledgers via REST. A board item is "Done" only if its linked obligations are closed. Manual status changes on boards are recorded as human-attested warrants but cannot override a non-closed ledger state (they appear as "Asserted done — unproven"). | Acceptance journey RJ-06. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-PD-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-PD-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-PD-010 | Board integration (IP-08): KGF completion boards read done-status from REVA ledgers via REST. A board item is "Done" only if its linked obligations are closed. Manual status changes on boards are recorded as human-attested warrants but cannot override a non-closed ledger state (they appear as "Asserted done — unproven"). | Acceptance journey RJ-06. | acceptance»
- [ ] Board integration (IP-08): KGF completion boards read done-status from REVA ledgers via REST. A board item is "Done" only if its linked obligations are closed. Manual status changes on boards are recorded as human-attested warrants but cannot override a non-closed ledger state (they appear as "Asserted done — unproven").
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-RO-004 [P2] REVA-RO-004: Web console log and runtime exception harvester. Subscribes to Log.entryAdded, Runtime.consoleAPICalled, and Runtime.exceptionThrown; structures console errors, warnings, unhandled promise rejections,

- **Source:** `reva-requirements.md:1156-1156` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-RO-004 | Web console log and runtime exception harvester. Subscribes to `Log.entryAdded`, `Runtime.consoleAPICalled`, and `Runtime.exceptionThrown`; structures console errors, warnings, unhandled promise rejections, and V8 stack traces. | Captures thrown JavaScript exceptions and console errors from test page; associates stack frames with extracted JavaScript source maps. | unit
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-RO-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-RO-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Captures thrown JavaScript exceptions and console errors from test page; associates stack frames with extracted JavaScript source maps
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-RR-001 [P2] REVA-RR-001: Matching rules: static http_route ↔ observed server operation (same service, method, canonical template); static http_call ↔ observed client call (caller service, target operation); static topics ↔ me

- **Source:** `reva-requirements.md:924-924` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-RR-001 | Matching rules: static `http_route` ↔ observed server operation (same service, method, canonical template); static `http_call` ↔ observed client call (caller service, target operation); static topics ↔ messaging spans; static `db_table` resources ↔ DB spans. Each match issues a `reva.pred.observed_as` warrant (`inferred`, links to both sides, V-07). | Fixture with 10 static and 10 runtime items yields the expected 7 matches. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-RR-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-RR-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture with 10 static and 10 runtime items yields the expected 7 matches
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

