# EPIC-IP-UNTR-03: EOIP-engg-doc-pkg/ip-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 60 tasks, ~390.0 h, priorities {'P2': 60}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-REQ-INV11-002 [P2] REQ-INV11-002: Merge simulation on a shadow branch: merged entity = union of relations, property conflicts resolved by the type's merge policy (most recent observed value by default), then: replay of saved queries a

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:923-923` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV11-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV11-002 | Merge simulation on a shadow branch: merged entity = union of relations, property conflicts resolved by the type's merge policy (most recent observed value by default), then: replay of saved queries and dashboards touching either entity (result diffs), SHACL validation (new violations), impact of the merge (Invention 2).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV11-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV11-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV11-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV11-002 | Merge simulation on a shadow branch: merged entity = union of relations, property conflicts resolved by the type's merge policy (most recent observed value by default), then: replay of saved queries and dashboards touching either entity (result diffs), SHACL validation (new violations), impact of the merge (Invention 2).»
- [ ] Merge simulation on a shadow branch: merged entity = union of relations, property conflicts resolved by the type's merge policy (most recent observed value by default), then: replay of saved queries and dashboards touching either entity (result diffs), SHACL validation (new violations), impact of the merge (Invention 2).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV11-003 [P2] REQ-INV11-003: Merge preview in the UI shows the before/after entity, changed query results, violations and impacted entities; steward approves or rejects. Approved merges commit through the normal checkpoint; merge

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:924-924` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV11-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV11-003 | Merge preview in the UI shows the before/after entity, changed query results, violations and impacted entities; steward approves or rejects. Approved merges commit through the normal checkpoint; merges are reversible (split back) within `dedup.undo_days` (default 30).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV11-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV11-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV11-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV11-003 | Merge preview in the UI shows the before/after entity, changed query results, violations and impacted entities; steward approves or rejects. Approved merges commit through the normal checkpoint; merges are reversible (split back) within dedup.undo_days (default 30).»
- [ ] Merge preview in the UI shows the before/after entity, changed query results, violations and impacted entities; steward approves or rejects. Approved merges commit through the normal checkpoint; merges are reversible (split back) within dedup.undo_days (default 30).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV11-004 [P2] REQ-INV11-004: Learning: per type, logistic calibration of τT from approve/reject decisions once ≥ 50 decisions exist for that type

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:925-925` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV11-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV11-004 | Learning: per type, logistic calibration of τ_T from approve/reject decisions once ≥ 50 decisions exist for that type.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV11-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV11-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV11-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV11-004 | Learning: per type, logistic calibration of τ_T from approve/reject decisions once ≥ 50 decisions exist for that type.»
- [ ] Learning: per type, logistic calibration of τ_T from approve/reject decisions once ≥ 50 decisions exist for that type.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV11-005 [P2] REQ-INV11-005: APIs: GET /dedup/candidates, POST /dedup/simulate {a, b}, POST /dedup/merge {simulationid}, POST /dedup/unmerge {mergeid}

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:926-926` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV11-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV11-005 | APIs: `GET /dedup/candidates`, `POST /dedup/simulate {a, b}`, `POST /dedup/merge {simulation_id}`, `POST /dedup/unmerge {merge_id}`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV11-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV11-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV11-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV11-005 | APIs: GET /dedup/candidates, POST /dedup/simulate {a, b}, POST /dedup/merge {simulation_id}, POST /dedup/unmerge {merge_id}.»
- [ ] APIs: GET /dedup/candidates, POST /dedup/simulate {a, b}, POST /dedup/merge {simulation_id}, POST /dedup/unmerge {merge_id}.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV11-006 [P2] REQ-INV11-006: Acceptance on the seeded set (200 planted duplicate pairs, 200 near-miss non-duplicates) at default τ: precision ≥ 0.95 and recall ≥ 0.85. Unmerge restores the pre-merge state exactly (state hashes ma

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:927-927` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV11-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV11-006 | Acceptance on the seeded set (200 planted duplicate pairs, 200 near-miss non-duplicates) at default τ: precision ≥ 0.95 and recall ≥ 0.85. Unmerge restores the pre-merge state exactly (state hashes match).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV11-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV11-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV11-006

**Acceptance criteria**
- [ ] on the seeded set (200 planted duplicate pairs, 200 near-miss non-duplicates) at default τ: precision ≥ 0.95 and recall ≥ 0.85. Unmerge restores the pre-merge state exactly (state hashes match)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV12-001 [P2] REQ-INV12-001: Abstraction pyramid per tenant: L0 full graph; L1 entities grouped by type within Louvain communities; L2 groups of types (by kgf:domain); L3 domain summary nodes. Meta-edges between groups carry coun

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:933-933` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV12-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV12-001 | Abstraction pyramid per tenant: L0 full graph; L1 entities grouped by type within Louvain communities; L2 groups of types (by `kgf:domain`); L3 domain summary nodes. Meta-edges between groups carry counts and relation-type breakdowns. Rebuilt after each snapshot.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV12-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV12-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV12-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV12-001 | Abstraction pyramid per tenant: L0 full graph; L1 entities grouped by type within Louvain communities; L2 groups of types (by kgf:domain); L3 domain summary nodes. Meta-edges between groups carry counts and relation-type breakdowns. Rebuilt after each snapshot.»
- [ ] Abstraction pyramid per tenant: L0 full graph; L1 entities grouped by type within Louvain communities; L2 groups of types (by kgf:domain); L3 domain summary nodes. Meta-edges between groups carry counts and relation-type breakdowns. Rebuilt after each snapshot.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV12-002 [P2] REQ-INV12-002: Per-level embeddings trained with an alignment loss so that the mean of an L1 group's L0 member embeddings and the group's L1 embedding have cosine ≥ 0.8 (and likewise L1→L2, L2→L3). Report the achiev

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:934-934` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV12-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV12-002 | Per-level embeddings trained with an alignment loss so that the mean of an L1 group's L0 member embeddings and the group's L1 embedding have cosine ≥ 0.8 (and likewise L1→L2, L2→L3). Report the achieved alignment per level.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV12-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV12-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV12-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV12-002 | Per-level embeddings trained with an alignment loss so that the mean of an L1 group's L0 member embeddings and the group's L1 embedding have cosine ≥ 0.8 (and likewise L1→L2, L2→L3). Report the achieved alignment per level.»
- [ ] Per-level embeddings trained with an alignment loss so that the mean of an L1 group's L0 member embeddings and the group's L1 embedding have cosine ≥ 0.8 (and likewise L1→L2, L2→L3). Report the achieved alignment per level.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV12-003 [P2] REQ-INV12-003: Cross-level query: POST /abstraction/query {level, question

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:935-935` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV12-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV12-003 | Cross-level query: `POST /abstraction/query {level, question | pattern}` answers at that level (e.g., count of services depending on a database cluster at L2) and returns drill-down handles to L0 entities.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV12-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV12-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV12-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV12-003 | Cross-level query: `POST /abstraction/query {level, question | pattern}` answers at that level (e.g., count of services depending on a database cluster at L2) and returns drill-down handles to L0 entities.»
- [ ] Cross-level query: `POST /abstraction/query {level, question
- [ ] pattern}` answers at that level (e.g., count of services depending on a database cluster at L2) and returns drill-down handles to L0 entities.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV12-004 [P2] REQ-INV12-004: The explorer switches level by zoom thresholds with animated morphing between summary nodes and members (positions interpolated, never teleported), honouring reduced-motion settings

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:936-936` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV12-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV12-004 | The explorer switches level by zoom thresholds with animated morphing between summary nodes and members (positions interpolated, never teleported), honouring reduced-motion settings.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV12-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV12-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV12-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV12-004 | The explorer switches level by zoom thresholds with animated morphing between summary nodes and members (positions interpolated, never teleported), honouring reduced-motion settings.»
- [ ] The explorer switches level by zoom thresholds with animated morphing between summary nodes and members (positions interpolated, never teleported), honouring reduced-motion settings.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV12-005 [P2] REQ-INV12-005: APIs: GET /abstraction/levels, GET /abstraction/{level}/graph?viewport=…

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:937-937` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV12-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV12-005 | APIs: `GET /abstraction/levels`, `GET /abstraction/{level}/graph?viewport=…`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV12-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV12-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV12-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV12-005 | APIs: GET /abstraction/levels, GET /abstraction/{level}/graph?viewport=….»
- [ ] APIs: GET /abstraction/levels, GET /abstraction/{level}/graph?viewport=….
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV3-001 [P2] REQ-INV3-001: Question decomposition into sub-questions, each tagged with ontology concepts (entity linking to types and instances), via local LLM through the SDK (warranted)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:843-843` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV3-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV3-001 | Question decomposition into sub-questions, each tagged with ontology concepts (entity linking to types and instances), via local LLM through the SDK (warranted).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV3-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV3-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV3-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV3-001 | Question decomposition into sub-questions, each tagged with ontology concepts (entity linking to types and instances), via local LLM through the SDK (warranted).»
- [ ] Question decomposition into sub-questions, each tagged with ontology concepts (entity linking to types and instances), via local LLM through the SDK (warranted).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV3-002 [P2] REQ-INV3-002: Metapath enumeration from the meta-graph up to length ask.maxmetapathlen (default 4) between tagged types

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:844-844` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV3-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV3-002 | Metapath enumeration from the meta-graph up to length `ask.max_metapath_len` (default 4) between tagged types.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV3-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV3-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV3-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV3-002 | Metapath enumeration from the meta-graph up to length ask.max_metapath_len (default 4) between tagged types.»
- [ ] Metapath enumeration from the meta-graph up to length ask.max_metapath_len (default 4) between tagged types.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV3-003 [P2] REQ-INV3-003: Metapath scoring: semantic-level attention between the sub-question embedding and each metapath embedding (metapath embedding = attention-pooled relation and type embeddings), with hierarchical attent

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:845-845` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV3-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV3-003 | Metapath scoring: semantic-level attention between the sub-question embedding and each metapath embedding (metapath embedding = attention-pooled relation and type embeddings), with hierarchical attention over metapaths sharing prefixes. Select top `ask.top_metapaths` (default 5). Phase 1 may use a training-free scorer (cosine of embeddings + path-length prior) until a trained scorer beats it on the QA eval set (REQ-INV3-008); record the active scorer in each answer.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV3-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV3-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV3-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV3-003 | Metapath scoring: semantic-level attention between the sub-question embedding and each metapath embedding (metapath embedding = attention-pooled relation and type embeddings), with hierarchical attention over metapaths sharing prefixes. Select top ask.top_metapaths (default 5). Phase 1 may use a training-free scorer (cosine of embeddings + path-length prior) unti»
- [ ] Metapath scoring: semantic-level attention between the sub-question embedding and each metapath embedding (metapath embedding = attention-pooled relation and type embeddings), with hierarchical attention over metapaths sharing prefixes. Select top ask.top_metapaths (default 5). Phase 1 may use a training-free scorer (cosine of embeddings + path-length prior) until a trained scorer beats it on the 
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV3-004 [P2] REQ-INV3-004: Subgraph extraction restricted to instances reachable through selected metapaths, passed through the derivation guard

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:846-846` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV3-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV3-004 | Subgraph extraction restricted to instances reachable through selected metapaths, passed through the derivation guard.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV3-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV3-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV3-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV3-004 | Subgraph extraction restricted to instances reachable through selected metapaths, passed through the derivation guard.»
- [ ] Subgraph extraction restricted to instances reachable through selected metapaths, passed through the derivation guard.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV3-005 [P2] REQ-INV3-005: Dual path: (a) deterministic: generate a query in the tenant's configured query language (Cypher, Gremlin, SPARQL, GQL, SQL as supported by KGF) constrained to the selected metapaths, show it to the u

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:847-847` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV3-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV3-005 | Dual path: (a) deterministic: generate a query in the tenant's configured query language (Cypher, Gremlin, SPARQL, GQL, SQL as supported by KGF) constrained to the selected metapaths, show it to the user, execute; (b) neural: GNN over the subgraph + answer generation through the SDK.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV3-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV3-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV3-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV3-005 | Dual path: (a) deterministic: generate a query in the tenant's configured query language (Cypher, Gremlin, SPARQL, GQL, SQL as supported by KGF) constrained to the selected metapaths, show it to the user, execute; (b) neural: GNN over the subgraph + answer generation through the SDK.»
- [ ] Dual path: (a) deterministic: generate a query in the tenant's configured query language (Cypher, Gremlin, SPARQL, GQL, SQL as supported by KGF) constrained to the selected metapaths, show it to the user, execute; (b) neural: GNN over the subgraph + answer generation through the SDK.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV3-006 [P2] REQ-INV3-006: Fusion: answer claims carry warrants; claims from the deterministic path inherit statuses from the data (A1 COMPUTATION); neural claims are PREDICTED; disagreement between paths is shown explicitly ("

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:848-848` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV3-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV3-006 | Fusion: answer claims carry warrants; claims from the deterministic path inherit statuses from the data (A1 COMPUTATION); neural claims are `PREDICTED`; disagreement between paths is shown explicitly ("the query returned X; the model suggests Y").
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV3-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV3-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV3-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV3-006 | Fusion: answer claims carry warrants; claims from the deterministic path inherit statuses from the data (A1 COMPUTATION); neural claims are PREDICTED; disagreement between paths is shown explicitly ("the query returned X; the model suggests Y").»
- [ ] Fusion: answer claims carry warrants; claims from the deterministic path inherit statuses from the data (A1 COMPUTATION); neural claims are PREDICTED; disagreement between paths is shown explicitly ("the query returned X; the model suggests Y").
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV3-007 [P2] REQ-INV3-007: Ontology validation of the fused answer against SHACL/axioms; violations are flagged in the answer with the violated constraint

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:849-849` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV3-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV3-007 | Ontology validation of the fused answer against SHACL/axioms; violations are flagged in the answer with the violated constraint.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV3-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV3-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV3-007

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV3-007 | Ontology validation of the fused answer against SHACL/axioms; violations are flagged in the answer with the violated constraint.»
- [ ] Ontology validation of the fused answer against SHACL/axioms; violations are flagged in the answer with the violated constraint.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV3-008 [P2] REQ-INV3-008: Eval set evals/ask/kgf-qa-v1 with ≥ 150 questions over a seeded demo tenant, covering the five documented question types (impact of changing a service account, who changed a class, systems changed by 

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:850-850` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV3-008; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV3-008 | Eval set `evals/ask/kgf-qa-v1` with ≥ 150 questions over a seeded demo tenant, covering the five documented question types (impact of changing a service account, who changed a class, systems changed by a feature, what to test for a rule change, incident cause). Acceptance: exact-match or steward-accepted answers ≥ 80% on deterministic-answerable questions; 100% of answers carry warrants; 0 answers present a `PREDICTED` claim as observed.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV3-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV3-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV3-008

**Acceptance criteria**
- [ ] exact-match or steward-accepted answers ≥ 80% on deterministic-answerable questions; 100% of answers carry warrants; 0 answers present a PREDICTED claim as observed
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV3-009 [P2] REQ-INV3-009: API: `POST /ask {question, mode: auto · deterministic · neural} streams {suggested_queries[], selected_metapaths[], deterministic_result, neural_result, fused_answer, warrant_id, violations[]}; GET /a

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:851-851` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV3-009; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV3-009 | API: `POST /ask {question, mode: auto | deterministic | neural}` streams `{suggested_queries[], selected_metapaths[], deterministic_result, neural_result, fused_answer, warrant_id, violations[]}`; `GET /ask/{id}`. Suggested queries (existing KGF feature) are now generated from selected metapaths.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV3-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV3-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV3-009

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV3-009 | API: `POST /ask {question, mode: auto | deterministic | neural} streams {suggested_queries[], selected_metapaths[], deterministic_result, neural_result, fused_answer, warrant_id, violations[]}; GET /ask/{id}`. Suggested queries (existing KGF feature) are now generated from selected metapaths.»
- [ ] API: `POST /ask {question, mode: auto
- [ ] neural} streams {suggested_queries[], selected_metapaths[], deterministic_result, neural_result, fused_answer, warrant_id, violations[]}; GET /ask/{id}`. Suggested queries (existing KGF feature) are now generated from selected metapaths.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV4-001 [P2] REQ-INV4-001: Usage mining: record traversed metapaths from queries and Ask the Brain; propose a new relation type when a metapath of length 2–3 not defined as a direct relation is traversed by ≥ advisor.minsupport

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:857-857` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV4-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV4-001 | Usage mining: record traversed metapaths from queries and Ask the Brain; propose a new relation type when a metapath of length 2–3 not defined as a direct relation is traversed by ≥ `advisor.min_support` (default 20) distinct queries in 30 days.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV4-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV4-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV4-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV4-001 | Usage mining: record traversed metapaths from queries and Ask the Brain; propose a new relation type when a metapath of length 2–3 not defined as a direct relation is traversed by ≥ advisor.min_support (default 20) distinct queries in 30 days.»
- [ ] Usage mining: record traversed metapaths from queries and Ask the Brain; propose a new relation type when a metapath of length 2–3 not defined as a direct relation is traversed by ≥ advisor.min_support (default 20) distinct queries in 30 days.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV4-002 [P2] REQ-INV4-002: New-type proposal: cluster untyped or generically typed entities in embedding space (HDBSCAN, minclustersize default 10); propose a type when a cluster is stable across 3 snapshots, with suggested pro

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:858-858` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV4-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV4-002 | New-type proposal: cluster untyped or generically typed entities in embedding space (HDBSCAN, `min_cluster_size` default 10); propose a type when a cluster is stable across 3 snapshots, with suggested properties = properties present in ≥ 80% of members and suggested parent = nearest existing type centroid.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV4-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV4-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV4-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV4-002 | New-type proposal: cluster untyped or generically typed entities in embedding space (HDBSCAN, min_cluster_size default 10); propose a type when a cluster is stable across 3 snapshots, with suggested properties = properties present in ≥ 80% of members and suggested parent = nearest existing type centroid.»
- [ ] New-type proposal: cluster untyped or generically typed entities in embedding space (HDBSCAN, min_cluster_size default 10); propose a type when a cluster is stable across 3 snapshots, with suggested properties = properties present in ≥ 80% of members and suggested parent = nearest existing type centroid.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV4-003 [P2] REQ-INV4-003: Relation-type splitting: for each relation type with ≥ 40 edges, cluster edge embeddings (concatenation of source, relation and target embeddings); propose a split when ≥ 2 clusters each have ≥ 20 edg

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:859-859` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV4-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV4-003 | Relation-type splitting: for each relation type with ≥ 40 edges, cluster edge embeddings (concatenation of source, relation and target embeddings); propose a split when ≥ 2 clusters each have ≥ 20 edges and silhouette ≥ 0.35; suggested names generated through the SDK and marked `GENERATED`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV4-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV4-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV4-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV4-003 | Relation-type splitting: for each relation type with ≥ 40 edges, cluster edge embeddings (concatenation of source, relation and target embeddings); propose a split when ≥ 2 clusters each have ≥ 20 edges and silhouette ≥ 0.35; suggested names generated through the SDK and marked GENERATED.»
- [ ] Relation-type splitting: for each relation type with ≥ 40 edges, cluster edge embeddings (concatenation of source, relation and target embeddings); propose a split when ≥ 2 clusters each have ≥ 20 edges and silhouette ≥ 0.35; suggested names generated through the SDK and marked GENERATED.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV4-004 [P2] REQ-INV4-004: Type refinement: propose subtypes when intra-type dispersion > 2× the median dispersion across types; propose merge when two sibling types have centroid cosine distance < 0.1 and property overlap ≥ 0.

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:860-860` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV4-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV4-004 | Type refinement: propose subtypes when intra-type dispersion > 2× the median dispersion across types; propose merge when two sibling types have centroid cosine distance < 0.1 and property overlap ≥ 0.8.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV4-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV4-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV4-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV4-004 | Type refinement: propose subtypes when intra-type dispersion > 2× the median dispersion across types; propose merge when two sibling types have centroid cosine distance < 0.1 and property overlap ≥ 0.8.»
- [ ] Type refinement: propose subtypes when intra-type dispersion > 2× the median dispersion across types; propose merge when two sibling types have centroid cosine distance < 0.1 and property overlap ≥ 0.8.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV4-005 [P2] REQ-INV4-005: Every proposal runs impact simulation on a shadow branch: entities reclassified, queries and artifacts affected (via Meaning Migration A6), constraint changes; then enters the steward queue. Approved 

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:861-861` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV4-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV4-005 | Every proposal runs impact simulation on a shadow branch: entities reclassified, queries and artifacts affected (via Meaning Migration A6), constraint changes; then enters the steward queue. Approved proposals become a meaning release draft (§11), never a direct ontology edit.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV4-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV4-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV4-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV4-005 | Every proposal runs impact simulation on a shadow branch: entities reclassified, queries and artifacts affected (via Meaning Migration A6), constraint changes; then enters the steward queue. Approved proposals become a meaning release draft (§11), never a direct ontology edit.»
- [ ] Every proposal runs impact simulation on a shadow branch: entities reclassified, queries and artifacts affected (via Meaning Migration A6), constraint changes; then enters the steward queue. Approved proposals become a meaning release draft (§11), never a direct ontology edit.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV4-006 [P2] REQ-INV4-006: APIs: GET /ontology/proposals, GET /ontology/proposals/{id}, `POST /ontology/proposals/{id}/approve · reject · defer` with reason (reasons are training labels).

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:862-862` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV4-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV4-006 | APIs: `GET /ontology/proposals`, `GET /ontology/proposals/{id}`, `POST /ontology/proposals/{id}/approve | reject | defer` with reason (reasons are training labels).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV4-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV4-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV4-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV4-006 | APIs: GET /ontology/proposals, GET /ontology/proposals/{id}, `POST /ontology/proposals/{id}/approve | reject | defer` with reason (reasons are training labels).»
- [ ] APIs: GET /ontology/proposals, GET /ontology/proposals/{id}, `POST /ontology/proposals/{id}/approve
- [ ] defer` with reason (reasons are training labels).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV5-001 [P2] REQ-INV5-001: Fingerprint of an incident at time t: (a) ontology-typed topology diff in window [t − Δ, t] (forensics.window, default 2 h): counts of change events per (entity type, relation type, change kind) norma

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:868-868` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV5-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV5-001 | Fingerprint of an incident at time t: (a) ontology-typed topology diff in window `[t − Δ, t]` (`forensics.window`, default 2 h): counts of change events per `(entity type, relation type, change kind)` normalized; (b) embedding of the changed subgraph (TGN-style temporal encoder, or mean-pooled GNN embeddings of changed entities in Phase 1).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV5-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV5-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV5-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV5-001 | Fingerprint of an incident at time t: (a) ontology-typed topology diff in window [t − Δ, t] (forensics.window, default 2 h): counts of change events per (entity type, relation type, change kind) normalized; (b) embedding of the changed subgraph (TGN-style temporal encoder, or mean-pooled GNN embeddings of changed entities in Phase 1).»
- [ ] Fingerprint of an incident at time t: (a) ontology-typed topology diff in window [t − Δ, t] (forensics.window, default 2 h): counts of change events per (entity type, relation type, change kind) normalized; (b) embedding of the changed subgraph (TGN-style temporal encoder, or mean-pooled GNN embeddings of changed entities in Phase 1).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV5-002 [P2] REQ-INV5-002: Library of fingerprints for resolved incidents with their recorded root cause (entity ids and change ids)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:869-869` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV5-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV5-002 | Library of fingerprints for resolved incidents with their recorded root cause (entity ids and change ids).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV5-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV5-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV5-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV5-002 | Library of fingerprints for resolved incidents with their recorded root cause (entity ids and change ids).»
- [ ] Library of fingerprints for resolved incidents with their recorded root cause (entity ids and change ids).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV5-003 [P2] REQ-INV5-003: Matching: weighted similarity 0.5 × cosine(typed diff vectors) + 0.5 × cosine(embeddings); return top 5 with score and a graph-diff explanation: which typed changes match, which differ

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:870-870` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV5-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV5-003 | Matching: weighted similarity `0.5 × cosine(typed diff vectors) + 0.5 × cosine(embeddings)`; return top 5 with score and a graph-diff explanation: which typed changes match, which differ.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV5-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV5-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV5-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV5-003 | Matching: weighted similarity 0.5 × cosine(typed diff vectors) + 0.5 × cosine(embeddings); return top 5 with score and a graph-diff explanation: which typed changes match, which differ.»
- [ ] Matching: weighted similarity 0.5 × cosine(typed diff vectors) + 0.5 × cosine(embeddings); return top 5 with score and a graph-diff explanation: which typed changes match, which differ.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV5-004 [P2] REQ-INV5-004: APIs: POST /incidents/{id}/fingerprint, GET /incidents/{id}/matches, POST /incidents/{id}/root-cause (records the confirmed cause; becomes a library entry)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:871-871` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV5-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV5-004 | APIs: `POST /incidents/{id}/fingerprint`, `GET /incidents/{id}/matches`, `POST /incidents/{id}/root-cause` (records the confirmed cause; becomes a library entry).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV5-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV5-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV5-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV5-004 | APIs: POST /incidents/{id}/fingerprint, GET /incidents/{id}/matches, POST /incidents/{id}/root-cause (records the confirmed cause; becomes a library entry).»
- [ ] APIs: POST /incidents/{id}/fingerprint, GET /incidents/{id}/matches, POST /incidents/{id}/root-cause (records the confirmed cause; becomes a library entry).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV5-006 [P2] REQ-INV5-006: Acceptance: on 20 held-out seeded incidents, the top-5 matches include an incident with the same root-cause type for ≥ 14 of the 20

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:873-873` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV5-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV5-006 | Acceptance: on 20 held-out seeded incidents, the top-5 matches include an incident with the same root-cause type for ≥ 14 of the 20.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV5-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV5-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV5-006

**Acceptance criteria**
- [ ] on 20 held-out seeded incidents, the top-5 matches include an incident with the same root-cause type for ≥ 14 of the 20
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV6-001 [P2] REQ-INV6-001: Opt-in per tenant (federation.enabled, default false) and per data class: a tenant chooses which data classes may contribute gradients. restricted can never contribute

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:879-879` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV6-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV6-001 | Opt-in per tenant (`federation.enabled`, default false) and per data class: a tenant chooses which data classes may contribute gradients. `restricted` can never contribute.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV6-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV6-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV6-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV6-001 | Opt-in per tenant (federation.enabled, default false) and per data class: a tenant chooses which data classes may contribute gradients. restricted can never contribute.»
- [ ] Opt-in per tenant (federation.enabled, default false) and per data class: a tenant chooses which data classes may contribute gradients. restricted can never contribute.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV6-002 [P2] REQ-INV6-002: Task: link prediction and entity-resolution scoring models. Each participating tenant trains locally on its own snapshot; only clipped, noised gradients/updates leave the tenant

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:880-880` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV6-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV6-002 | Task: link prediction and entity-resolution scoring models. Each participating tenant trains locally on its own snapshot; only clipped, noised gradients/updates leave the tenant.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV6-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV6-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV6-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV6-002 | Task: link prediction and entity-resolution scoring models. Each participating tenant trains locally on its own snapshot; only clipped, noised gradients/updates leave the tenant.»
- [ ] Task: link prediction and entity-resolution scoring models. Each participating tenant trains locally on its own snapshot; only clipped, noised gradients/updates leave the tenant.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV6-004 [P2] REQ-INV6-004: Secure aggregation so the coordinator sees only the sum of updates. The coordinator is self-hosted inside the KGF deployment of the platform operator; no third-party service

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:882-882` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV6-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV6-004 | Secure aggregation so the coordinator sees only the sum of updates. The coordinator is self-hosted inside the KGF deployment of the platform operator; no third-party service.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV6-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV6-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV6-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV6-004 | Secure aggregation so the coordinator sees only the sum of updates. The coordinator is self-hosted inside the KGF deployment of the platform operator; no third-party service.»
- [ ] Secure aggregation so the coordinator sees only the sum of updates. The coordinator is self-hosted inside the KGF deployment of the platform operator; no third-party service.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV6-005 [P2] REQ-INV6-005: The federated model is offered to each tenant as a CANDIDATE and promoted only if it beats the tenant's local model on the tenant's own validation split

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:883-883` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV6-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV6-005 | The federated model is offered to each tenant as a CANDIDATE and promoted only if it beats the tenant's local model on the tenant's own validation split.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV6-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV6-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV6-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV6-005 | The federated model is offered to each tenant as a CANDIDATE and promoted only if it beats the tenant's local model on the tenant's own validation split.»
- [ ] The federated model is offered to each tenant as a CANDIDATE and promoted only if it beats the tenant's local model on the tenant's own validation split.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV6-006 [P2] REQ-INV6-006: Audit: every round logs participating tenants (pseudonymous ids), classes, ε spent; tenants can view their own ledger

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:884-884` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV6-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV6-006 | Audit: every round logs participating tenants (pseudonymous ids), classes, ε spent; tenants can view their own ledger.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV6-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV6-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV6-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV6-006 | Audit: every round logs participating tenants (pseudonymous ids), classes, ε spent; tenants can view their own ledger.»
- [ ] Audit: every round logs participating tenants (pseudonymous ids), classes, ε spent; tenants can view their own ledger.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV7-001 [P2] REQ-INV7-001: Vitality vector per entity, recomputed daily: recency of updates, update frequency (30/90 days), query touches (30/90 days), degree and PageRank centrality, neighbourhood change rate, embedding drift 

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:890-890` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV7-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV7-001 | Vitality vector per entity, recomputed daily: recency of updates, update frequency (30/90 days), query touches (30/90 days), degree and PageRank centrality, neighbourhood change rate, embedding drift rate (from Invention 1), freshness (A7).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV7-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV7-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV7-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV7-001 | Vitality vector per entity, recomputed daily: recency of updates, update frequency (30/90 days), query touches (30/90 days), degree and PageRank centrality, neighbourhood change rate, embedding drift rate (from Invention 1), freshness (A7).»
- [ ] Vitality vector per entity, recomputed daily: recency of updates, update frequency (30/90 days), query touches (30/90 days), degree and PageRank centrality, neighbourhood change rate, embedding drift rate (from Invention 1), freshness (A7).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV7-002 [P2] REQ-INV7-002: Events: DEPRECATED, ARCHIVED, STALE (no update and no query for health.staledays, default 180), GOVERNANCERISK (steward-flagged). Model: Cox proportional hazards in Phase 1; switch to a neural surviva

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:891-891` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV7-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV7-002 | Events: `DEPRECATED`, `ARCHIVED`, `STALE` (no update and no query for `health.stale_days`, default 180), `GOVERNANCE_RISK` (steward-flagged). Model: Cox proportional hazards in Phase 1; switch to a neural survival model only if concordance index improves by ≥ 0.03 on a chronological split.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV7-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV7-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV7-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV7-002 | Events: DEPRECATED, ARCHIVED, STALE (no update and no query for health.stale_days, default 180), GOVERNANCE_RISK (steward-flagged). Model: Cox proportional hazards in Phase 1; switch to a neural survival model only if concordance index improves by ≥ 0.03 on a chronological split.»
- [ ] Events: DEPRECATED, ARCHIVED, STALE (no update and no query for health.stale_days, default 180), GOVERNANCE_RISK (steward-flagged). Model: Cox proportional hazards in Phase 1; switch to a neural survival model only if concordance index improves by ≥ 0.03 on a chronological split.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV7-003 [P2] REQ-INV7-003: Output per entity: predicted median remaining useful life, survival curve at 30/90/180 days, top contributing features. Entities with median < health.alertdays (default 30) and criticality ≥ 3 appear 

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:892-892` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV7-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV7-003 | Output per entity: predicted median remaining useful life, survival curve at 30/90/180 days, top contributing features. Entities with median < `health.alert_days` (default 30) and criticality ≥ 3 appear in the steward review queue with suggested action (archive, refresh, merge, deprecate).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV7-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV7-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV7-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV7-003 | Output per entity: predicted median remaining useful life, survival curve at 30/90/180 days, top contributing features. Entities with median < health.alert_days (default 30) and criticality ≥ 3 appear in the steward review queue with suggested action (archive, refresh, merge, deprecate).»
- [ ] Output per entity: predicted median remaining useful life, survival curve at 30/90/180 days, top contributing features. Entities with median < health.alert_days (default 30) and criticality ≥ 3 appear in the steward review queue with suggested action (archive, refresh, merge, deprecate).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV7-004 [P2] REQ-INV7-004: Steward decisions are stored as labels and used in the next training cycle

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:893-893` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV7-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV7-004 | Steward decisions are stored as labels and used in the next training cycle.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV7-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV7-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV7-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV7-004 | Steward decisions are stored as labels and used in the next training cycle.»
- [ ] Steward decisions are stored as labels and used in the next training cycle.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV7-005 [P2] REQ-INV7-005: APIs: GET /entities/{id}/vitality, GET /entity-health/queue, POST /entity-health/queue/{id}/decide

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:894-894` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV7-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV7-005 | APIs: `GET /entities/{id}/vitality`, `GET /entity-health/queue`, `POST /entity-health/queue/{id}/decide`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV7-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV7-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV7-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV7-005 | APIs: GET /entities/{id}/vitality, GET /entity-health/queue, POST /entity-health/queue/{id}/decide.»
- [ ] APIs: GET /entities/{id}/vitality, GET /entity-health/queue, POST /entity-health/queue/{id}/decide.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV7-006 [P2] REQ-INV7-006: Acceptance: concordance index ≥ 0.70 on the chronological test split of the demo tenant; the evidence includes the evaluation report

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:895-895` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV7-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV7-006 | Acceptance: concordance index ≥ 0.70 on the chronological test split of the demo tenant; the evidence includes the evaluation report.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV7-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV7-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV7-006

**Acceptance criteria**
- [ ] concordance index ≥ 0.70 on the chronological test split of the demo tenant; the evidence includes the evaluation report
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV8-001 [P2] REQ-INV8-001: Candidate pairs: entities A, B connected within 2 hops, both with ≥ causal.minsnapshots (default 20) snapshots of embedding change magnitudes

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:901-901` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV8-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV8-001 | Candidate pairs: entities A, B connected within 2 hops, both with ≥ `causal.min_snapshots` (default 20) snapshots of embedding change magnitudes.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV8-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV8-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV8-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV8-001 | Candidate pairs: entities A, B connected within 2 hops, both with ≥ causal.min_snapshots (default 20) snapshots of embedding change magnitudes.»
- [ ] Candidate pairs: entities A, B connected within 2 hops, both with ≥ causal.min_snapshots (default 20) snapshots of embedding change magnitudes.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV8-002 [P2] REQ-INV8-002: Granger test: VAR on the change-magnitude series with lag 1–3 (selected by AIC); F-test; Benjamini–Hochberg correction at q = 0.01 across all tested pairs per run

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:902-902` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV8-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV8-002 | Granger test: VAR on the change-magnitude series with lag 1–3 (selected by AIC); F-test; Benjamini–Hochberg correction at q = 0.01 across all tested pairs per run.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV8-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV8-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV8-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV8-002 | Granger test: VAR on the change-magnitude series with lag 1–3 (selected by AIC); F-test; Benjamini–Hochberg correction at q = 0.01 across all tested pairs per run.»
- [ ] Granger test: VAR on the change-magnitude series with lag 1–3 (selected by AIC); F-test; Benjamini–Hochberg correction at q = 0.01 across all tested pairs per run.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV8-003 [P2] REQ-INV8-003: Counterfactual check on a shadow branch: remove the A→B connecting paths, re-run the temporal predictor for B's next change; keep the candidate only if predicted change magnitude of B drops by ≥ causa

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:903-903` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV8-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV8-003 | Counterfactual check on a shadow branch: remove the A→B connecting paths, re-run the temporal predictor for B's next change; keep the candidate only if predicted change magnitude of B drops by ≥ `causal.min_effect` (default 50%).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV8-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV8-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV8-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV8-003 | Counterfactual check on a shadow branch: remove the A→B connecting paths, re-run the temporal predictor for B's next change; keep the candidate only if predicted change magnitude of B drops by ≥ causal.min_effect (default 50%).»
- [ ] Counterfactual check on a shadow branch: remove the A→B connecting paths, re-run the temporal predictor for B's next change; keep the candidate only if predicted change magnitude of B drops by ≥ causal.min_effect (default 50%).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV8-004 [P2] REQ-INV8-004: Accepted pairs are stored as (:Entity)-[:CAUSES {strength, lag, pvalue, runid}]->(:Entity) in a separate causal layer (distinct label or named graph), status PREDICTED, never mixed with observed relat

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:904-904` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV8-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV8-004 | Accepted pairs are stored as `(:Entity)-[:CAUSES {strength, lag, p_value, run_id}]->(:Entity)` in a separate causal layer (distinct label or named graph), status `PREDICTED`, never mixed with observed relations.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV8-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV8-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV8-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV8-004 | Accepted pairs are stored as (:Entity)-[:CAUSES {strength, lag, p_value, run_id}]->(:Entity) in a separate causal layer (distinct label or named graph), status PREDICTED, never mixed with observed relations.»
- [ ] Accepted pairs are stored as (:Entity)-[:CAUSES {strength, lag, p_value, run_id}]->(:Entity) in a separate causal layer (distinct label or named graph), status PREDICTED, never mixed with observed relations.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV8-005 [P2] REQ-INV8-005: POST /causal/discover (job), GET /causal/edges, POST /causal/whatif {changes[]} returns propagated effects using only CAUSES edges, clearly labelled as predicted. The graph explorer offers a "Causal l

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:905-905` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV8-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV8-005 | `POST /causal/discover` (job), `GET /causal/edges`, `POST /causal/whatif {changes[]}` returns propagated effects using only CAUSES edges, clearly labelled as predicted. The graph explorer offers a "Causal lens" toggle (§18.10).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV8-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV8-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV8-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV8-005 | POST /causal/discover (job), GET /causal/edges, POST /causal/whatif {changes[]} returns propagated effects using only CAUSES edges, clearly labelled as predicted. The graph explorer offers a "Causal lens" toggle (§18.10).»
- [ ] POST /causal/discover (job), GET /causal/edges, POST /causal/whatif {changes[]} returns propagated effects using only CAUSES edges, clearly labelled as predicted. The graph explorer offers a "Causal lens" toggle (§18.10).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV8-006 [P2] REQ-INV8-006: Synthetic validation: on a generated temporal graph with 20 planted causal links and 200 non-causal correlated pairs, recall ≥ 0.7 and precision ≥ 0.8

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:906-906` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV8-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV8-006 | Synthetic validation: on a generated temporal graph with 20 planted causal links and 200 non-causal correlated pairs, recall ≥ 0.7 and precision ≥ 0.8.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV8-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV8-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV8-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV8-006 | Synthetic validation: on a generated temporal graph with 20 planted causal links and 200 non-causal correlated pairs, recall ≥ 0.7 and precision ≥ 0.8.»
- [ ] Synthetic validation: on a generated temporal graph with 20 planted causal links and 200 non-causal correlated pairs, recall ≥ 0.7 and precision ≥ 0.8.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV9-001 [P2] REQ-INV9-001: Features of the visible subgraph: node and edge counts, density, type distribution entropy, hierarchy depth (longest path in DAG part), number of components, presence of a time property

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:912-912` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV9-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV9-001 | Features of the visible subgraph: node and edge counts, density, type distribution entropy, hierarchy depth (longest path in DAG part), number of components, presence of a time property.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV9-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV9-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV9-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV9-001 | Features of the visible subgraph: node and edge counts, density, type distribution entropy, hierarchy depth (longest path in DAG part), number of components, presence of a time property.»
- [ ] Features of the visible subgraph: node and edge counts, density, type distribution entropy, hierarchy depth (longest path in DAG part), number of components, presence of a time property.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV9-002 [P2] REQ-INV9-002: Candidate layouts: force-directed, hierarchical/layered, radial/ego, concentric, circular, grid, timeline (the layouts KGF's front-end supports)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:913-913` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV9-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV9-002 | Candidate layouts: force-directed, hierarchical/layered, radial/ego, concentric, circular, grid, timeline (the layouts KGF's front-end supports).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV9-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV9-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV9-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV9-002 | Candidate layouts: force-directed, hierarchical/layered, radial/ego, concentric, circular, grid, timeline (the layouts KGF's front-end supports).»
- [ ] Candidate layouts: force-directed, hierarchical/layered, radial/ego, concentric, circular, grid, timeline (the layouts KGF's front-end supports).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV9-003 [P2] REQ-INV9-003: Phase 1 scorer: weighted sum of normalized stress, edge crossings, node overlap, label overlap and type-cluster cohesion, computed in a Web Worker on a fast preview layout. Phase 2: a learned scorer t

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:914-914` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV9-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV9-003 | Phase 1 scorer: weighted sum of normalized stress, edge crossings, node overlap, label overlap and type-cluster cohesion, computed in a Web Worker on a fast preview layout. Phase 2: a learned scorer trained on user ratings (thumbs up/down and layout switches) once ≥ 300 rated layouts exist and it beats Phase 1 on held-out ratings.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV9-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV9-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV9-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV9-003 | Phase 1 scorer: weighted sum of normalized stress, edge crossings, node overlap, label overlap and type-cluster cohesion, computed in a Web Worker on a fast preview layout. Phase 2: a learned scorer trained on user ratings (thumbs up/down and layout switches) once ≥ 300 rated layouts exist and it beats Phase 1 on held-out ratings.»
- [ ] Phase 1 scorer: weighted sum of normalized stress, edge crossings, node overlap, label overlap and type-cluster cohesion, computed in a Web Worker on a fast preview layout. Phase 2: a learned scorer trained on user ratings (thumbs up/down and layout switches) once ≥ 300 rated layouts exist and it beats Phase 1 on held-out ratings.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV9-004 [P2] REQ-INV9-004: POST /layout/recommend returns ranked layouts with parameters; the explorer applies the top one by default ("Smart layout" toggle)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:915-915` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV9-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV9-004 | `POST /layout/recommend` returns ranked layouts with parameters; the explorer applies the top one by default ("Smart layout" toggle).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV9-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV9-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV9-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV9-004 | POST /layout/recommend returns ranked layouts with parameters; the explorer applies the top one by default ("Smart layout" toggle).»
- [ ] POST /layout/recommend returns ranked layouts with parameters; the explorer applies the top one by default ("Smart layout" toggle).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV9-005 [P2] REQ-INV9-005: Learned weights stored in the model registry only (REQ-IPH-003)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:916-916` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV9-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV9-005 | Learned weights stored in the model registry only (REQ-IPH-003).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV9-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV9-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV9-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV9-005 | Learned weights stored in the model registry only (REQ-IPH-003).»
- [ ] Learned weights stored in the model registry only (REQ-IPH-003).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-LIN-001 [P2] REQ-LIN-001: A laundering event is any attempted warrant whose status exceeds what A1 allows. The service rejects it and writes launderingdetected with the offending operator and inputs

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:506-506` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-LIN-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-LIN-001 | A **laundering event** is any attempted warrant whose status exceeds what A1 allows. The service rejects it and writes `laundering_detected` with the offending operator and inputs.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-LIN-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-LIN-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-LIN-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-LIN-001 | A laundering event is any attempted warrant whose status exceeds what A1 allows. The service rejects it and writes laundering_detected with the offending operator and inputs.»
- [ ] A laundering event is any attempted warrant whose status exceeds what A1 allows. The service rejects it and writes laundering_detected with the offending operator and inputs.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-LIN-002 [P2] REQ-LIN-002: The laundering audit job (§15.3) samples audit.samplesize (default 200) memory writes and handoffs per tenant per month and re-runs A1/A2 from stored inputs; mismatches are reported

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:507-507` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-LIN-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-LIN-002 | The laundering audit job (§15.3) samples `audit.sample_size` (default 200) memory writes and handoffs per tenant per month and re-runs A1/A2 from stored inputs; mismatches are reported.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-LIN-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-LIN-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-LIN-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-LIN-002 | The laundering audit job (§15.3) samples audit.sample_size (default 200) memory writes and handoffs per tenant per month and re-runs A1/A2 from stored inputs; mismatches are reported.»
- [ ] The laundering audit job (§15.3) samples audit.sample_size (default 200) memory writes and handoffs per tenant per month and re-runs A1/A2 from stored inputs; mismatches are reported.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-LSE-003 [P2] REQ-LSE-003: Event delivery: at-least-once, ordered per subjectid, end-to-end lag p95 < 2 s at 1,000 changes/s per tenant

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:528-528` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-LSE-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-LSE-003 | Event delivery: at-least-once, ordered per `subject_id`, end-to-end lag p95 < 2 s at 1,000 changes/s per tenant.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-LSE-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-LSE-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-LSE-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-LSE-003 | Event delivery: at-least-once, ordered per subject_id, end-to-end lag p95 < 2 s at 1,000 changes/s per tenant.»
- [ ] Event delivery: at-least-once, ordered per subject_id, end-to-end lag p95 < 2 s at 1,000 changes/s per tenant.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-LSE-010 [P2] REQ-LSE-010: A lease is issued at the retrieval checkpoint for every assertion read inside a warrantcontext that has a planid. Expiry = issuedat + min(kgf:halfLifeDays of the assertion's type × lease.halflifefract

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:550-550` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-LSE-010; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-LSE-010 | A lease is issued at the `retrieval` checkpoint for every assertion read inside a `warrant_context` that has a `plan_id`. Expiry = `issued_at + min(kgf:halfLifeDays of the assertion's type × lease.halflife_fraction, lease.max_ttl)`; defaults `lease.halflife_fraction = 0.5`, `lease.max_ttl = 24h`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-LSE-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-LSE-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-LSE-010

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-LSE-010 | A lease is issued at the retrieval checkpoint for every assertion read inside a warrant_context that has a plan_id. Expiry = issued_at + min(kgf:halfLifeDays of the assertion's type × lease.halflife_fraction, lease.max_ttl); defaults lease.halflife_fraction = 0.5, lease.max_ttl = 24h.»
- [ ] A lease is issued at the retrieval checkpoint for every assertion read inside a warrant_context that has a plan_id. Expiry = issued_at + min(kgf:halfLifeDays of the assertion's type × lease.halflife_fraction, lease.max_ttl); defaults lease.halflife_fraction = 0.5, lease.max_ttl = 24h.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-LSE-011 [P2] REQ-LSE-011: On kgf.graph.changed for a subject, all ACTIVE leases on that subject with version ≠ newversion become REVOKED within 2 s p95

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:551-551` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-LSE-011; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-LSE-011 | On `kgf.graph.changed` for a subject, all `ACTIVE` leases on that subject with `version ≠ new_version` become `REVOKED` within 2 s p95.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-LSE-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-LSE-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-LSE-011

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-LSE-011 | On kgf.graph.changed for a subject, all ACTIVE leases on that subject with version ≠ new_version become REVOKED within 2 s p95.»
- [ ] On kgf.graph.changed for a subject, all ACTIVE leases on that subject with version ≠ new_version become REVOKED within 2 s p95.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-LSE-012 [P2] REQ-LSE-012: Leases are stored in a fast store indexed by (tenantid, subjectid) and (tenantid, planid). Expired leases are swept every lease.sweepinterval (default 60 s)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:552-552` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-LSE-012; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-LSE-012 | Leases are stored in a fast store indexed by `(tenant_id, subject_id)` and `(tenant_id, plan_id)`. Expired leases are swept every `lease.sweep_interval` (default 60 s).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-LSE-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-LSE-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-LSE-012

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-LSE-012 | Leases are stored in a fast store indexed by (tenant_id, subject_id) and (tenant_id, plan_id). Expired leases are swept every lease.sweep_interval (default 60 s).»
- [ ] Leases are stored in a fast store indexed by (tenant_id, subject_id) and (tenant_id, plan_id). Expired leases are swept every lease.sweep_interval (default 60 s).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-LVC-001 [P2] REQ-LVC-001: POST /commits/validate (request: action, warrantid, plangraph) returns ALLOW, REPLAN {affectedsteps[], refreshedassertions[]} or ESCALATE

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:571-571` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-LVC-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-LVC-001 | `POST /commits/validate` (request: `action`, `warrant_id`, `plan_graph`) returns `ALLOW`, `REPLAN {affected_steps[], refreshed_assertions[]}` or `ESCALATE`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-LVC-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-LVC-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-LVC-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-LVC-001 | POST /commits/validate (request: action, warrant_id, plan_graph) returns ALLOW, REPLAN {affected_steps[], refreshed_assertions[]} or ESCALATE.»
- [ ] POST /commits/validate (request: action, warrant_id, plan_graph) returns ALLOW, REPLAN {affected_steps[], refreshed_assertions[]} or ESCALATE.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-LVC-003 [P2] REQ-LVC-003: p95 validation < 50 ms for ≤ 500 leases

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:573-573` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-LVC-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-LVC-003 | p95 validation < 50 ms for ≤ 500 leases.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-LVC-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-LVC-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-LVC-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-LVC-003 | p95 validation < 50 ms for ≤ 500 leases.»
- [ ] p95 validation < 50 ms for ≤ 500 leases.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

