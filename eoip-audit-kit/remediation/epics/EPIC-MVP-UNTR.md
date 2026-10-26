# EPIC-MVP-UNTR: EOIP-engg-doc-pkg/MVP-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 16 tasks, ~96.0 h, priorities {'P1': 16}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-MVP-FR-002 [P1] MVP-FR-002: Automatic graph schema initialization

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:74-79` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-002 — Automatic graph schema initialization
**Parent requirements:** FR-GRAPH-003  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Fresh startup creates the expected schema automatically and repeat startup is idempotent.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'MVP-FR-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('MVP-FR-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Fresh startup creates the expected schema automatically and repeat startup is idempotent.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Fresh startup creates the expected schema automatically and repeat startup is idempotent
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-MVP-FR-003 [P1] MVP-FR-003: Jira JSON ingestion

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:80-85` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-003 — Jira JSON ingestion
**Parent requirements:** FR-CONN-002  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Synthetic Jira fixture imports to Project/WorkItem/Person/evidence records with configurable mapping and per-record validation.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'MVP-FR-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('MVP-FR-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Synthetic Jira fixture imports to Project/WorkItem/Person/evidence records with configurable mapping and per-record validation.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Synthetic Jira fixture imports to Project/WorkItem/Person/evidence records with configurable mapping and per-record validation
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-MVP-FR-004 [P1] MVP-FR-004: Git repository/GitLab ingestion

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:86-91` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-004 — Git repository/GitLab ingestion
**Parent requirements:** FR-CONN-003, FR-CONN-004  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Local demo repository plus GitLab-style MR/pipeline fixture produces repository/ref/commit/MR/pipeline facts and links.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'MVP-FR-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('MVP-FR-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Local demo repository plus GitLab-style MR/pipeline fixture produces repository/ref/commit/MR/pipeline facts and links.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Local demo repository plus GitLab-style MR/pipeline fixture produces repository/ref/commit/MR/pipeline facts and links
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-MVP-FR-005 [P1] MVP-FR-005: Code parsing

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:92-97` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-005 — Code parsing
**Parent requirements:** FR-CODE-001, FR-CODE-002  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Python and TypeScript demo files produce symbols/source ranges/import or call/dependency edges without LLM parsing.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'MVP-FR-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('MVP-FR-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Python and TypeScript demo files produce symbols/source ranges/import or call/dependency edges without LLM parsing.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Python and TypeScript demo files produce symbols/source ranges/import or call/dependency edges without LLM parsing
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-MVP-FR-006 [P1] MVP-FR-006: Canonical entity generation

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:98-103` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-006 — Canonical entity generation
**Parent requirements:** FR-INGEST-002, FR-GRAPH-004  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Every imported canonical entity has stable canonical_id; identical re-ingestion creates no logical duplicate.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'MVP-FR-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('MVP-FR-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Every imported canonical entity has stable canonical_id; identical re-ingestion creates no logical duplicate.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Every imported canonical entity has stable canonicalid; identical re-ingestion creates no logical duplicate
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-MVP-FR-007 [P1] MVP-FR-007: Jira graph

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:104-109` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-007 — Jira graph
**Parent requirements:** FR-ONTO-001, FR-GRAPH-002  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Jira project/work-item subgraph is queryable with provenance.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'MVP-FR-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('MVP-FR-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Jira project/work-item subgraph is queryable with provenance.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Jira project/work-item subgraph is queryable with provenance
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-MVP-FR-008 [P1] MVP-FR-008: Code graph

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:110-115` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-008 — Code graph
**Parent requirements:** FR-CODE-001, FR-CODE-004  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Repository→file→symbol plus code dependency subgraph is queryable with exact source locations.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'MVP-FR-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('MVP-FR-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Repository→file→symbol plus code dependency subgraph is queryable with exact source locations.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Repository→file→symbol plus code dependency subgraph is queryable with exact source locations
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-MVP-FR-009 [P1] MVP-FR-009: Meta graph

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:116-121` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-009 — Meta graph
**Parent requirements:** FR-GRAPH-005  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Sources, runs, domains, schema/ontology versions and validation/quality records are queryable as meta graph.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'MVP-FR-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('MVP-FR-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Sources, runs, domains, schema/ontology versions and validation/quality records are queryable as meta graph.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Sources, runs, domains, schema/ontology versions and validation/quality records are queryable as meta graph
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-MVP-FR-010 [P1] MVP-FR-010: Cross-graph linking

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:122-127` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-010 — Cross-graph linking
**Parent requirements:** FR-GRAPH-006  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** The complete demo cross-domain path is traversable forward and reverse with evidence.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'MVP-FR-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('MVP-FR-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] The complete demo cross-domain path is traversable forward and reverse with evidence.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] The complete demo cross-domain path is traversable forward and reverse with evidence
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-MVP-FR-011 [P1] MVP-FR-011: Provenance

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:128-133` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-011 — Provenance
**Parent requirements:** FR-PROV-001, FR-PROV-002  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Cross-domain edges have evidence and creation status; lineage endpoint traces them to source capture/run.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'MVP-FR-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('MVP-FR-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Cross-domain edges have evidence and creation status; lineage endpoint traces them to source capture/run.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Cross-domain edges have evidence and creation status; lineage endpoint traces them to source capture/run
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-MVP-FR-013 [P1] MVP-FR-013: Query API

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:140-145` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-013 — Query API
**Parent requirements:** FR-QUERY-001, FR-QUERY-006  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Versioned REST APIs return real entity/search/query/evidence results and enforce query policy.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'MVP-FR-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('MVP-FR-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Versioned REST APIs return real entity/search/query/evidence results and enforce query policy.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Versioned REST APIs return real entity/search/query/evidence results and enforce query policy
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-MVP-FR-014 [P1] MVP-FR-014: Impact analysis query

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:146-151` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-014 — Impact analysis query
**Parent requirements:** FR-QUERY-003  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Changing the demo function yields the golden blast-radius set and path evidence within configured bounds.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'MVP-FR-014' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('MVP-FR-014') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Changing the demo function yields the golden blast-radius set and path evidence within configured bounds.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Changing the demo function yields the golden blast-radius set and path evidence within configured bounds
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-MVP-FR-015 [P1] MVP-FR-015: Path query

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:152-157` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-015 — Path query
**Parent requirements:** FR-QUERY-002  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Jira issue→function path matches golden ordered vertex/edge sequence.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'MVP-FR-015' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('MVP-FR-015') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Jira issue→function path matches golden ordered vertex/edge sequence.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Jira issue→function path matches golden ordered vertex/edge sequence
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-MVP-FR-016 [P1] MVP-FR-016: Search/query UI

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:158-163` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-016 — Search/query UI
**Parent requirements:** FR-UI-001  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Search/query UI uses real APIs; API shutdown produces an error state rather than demo fallback data.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'MVP-FR-016' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('MVP-FR-016') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Search/query UI uses real APIs; API shutdown produces an error state rather than demo fallback data.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Search/query UI uses real APIs; API shutdown produces an error state rather than demo fallback data
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-MVP-FR-017 [P1] MVP-FR-017: Graph visualizer

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:164-169` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-017 — Graph visualizer
**Parent requirements:** FR-UI-002  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Graph explorer renders bounded real subgraphs, edge types and highlighted paths/provenance.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'MVP-FR-017' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('MVP-FR-017') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Graph explorer renders bounded real subgraphs, edge types and highlighted paths/provenance.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Graph explorer renders bounded real subgraphs, edge types and highlighted paths/provenance
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-MVP-FR-018 [P1] MVP-FR-018: Admin ingestion/validation UI

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:170-175` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-018 — Admin ingestion/validation UI
**Parent requirements:** FR-ADMIN-001, FR-ADMIN-002  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Admin screens show actual run counts/status, graph stats, validation findings and quality values.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'MVP-FR-018' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('MVP-FR-018') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Admin screens show actual run counts/status, graph stats, validation findings and quality values.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Admin screens show actual run counts/status, graph stats, validation findings and quality values
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

