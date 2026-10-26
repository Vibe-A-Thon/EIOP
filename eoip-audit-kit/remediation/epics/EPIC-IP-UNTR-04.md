# EPIC-IP-UNTR-04: EOIP-engg-doc-pkg/ip-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 49 tasks, ~318.5 h, priorities {'P2': 47, 'P3': 2}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-REQ-LVC-004 [P2] REQ-LVC-004: Metric kgfipstalecommittotal{tenant,actionclass} counts commits that hit REPLAN or ESCALATE because of revoked or expired leases

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:574-574` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-LVC-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-LVC-004 | Metric `kgf_ip_stale_commit_total{tenant,action_class}` counts commits that hit `REPLAN` or `ESCALATE` because of revoked or expired leases.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-LVC-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-LVC-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-LVC-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-LVC-004 | Metric kgf_ip_stale_commit_total{tenant,action_class} counts commits that hit REPLAN or ESCALATE because of revoked or expired leases.»
- [ ] Metric kgf_ip_stale_commit_total{tenant,action_class} counts commits that hit REPLAN or ESCALATE because of revoked or expired leases.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-MET-002 [P2] REQ-MET-002: Consolidated memory renders status markers inline (e.g., [OBSERVED], [PREDICTED]) when exported as text for LLM context, using the template metabolism.statusmarkertemplate

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:754-754` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-MET-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-MET-002 | Consolidated memory renders status markers inline (e.g., `[OBSERVED]`, `[PREDICTED]`) when exported as text for LLM context, using the template `metabolism.status_marker_template`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-MET-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-MET-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-MET-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-MET-002 | Consolidated memory renders status markers inline (e.g., [OBSERVED], [PREDICTED]) when exported as text for LLM context, using the template metabolism.status_marker_template.»
- [ ] Consolidated memory renders status markers inline (e.g., [OBSERVED], [PREDICTED]) when exported as text for LLM context, using the template metabolism.status_marker_template.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-MET-003 [P2] REQ-MET-003: Benchmark evals/metabolism/consolidation-v1: ≥ 100 memory sets mixing observed facts, predictions and hearsay. Acceptance: 0 cases where a consolidated statement has a higher status than its lowest-st

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:755-755` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-MET-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-MET-003 | Benchmark `evals/metabolism/consolidation-v1`: ≥ 100 memory sets mixing observed facts, predictions and hearsay. Acceptance: 0 cases where a consolidated statement has a higher status than its lowest-status input; ≥ 95% of input propositions represented in output (measured by SASI entailment).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-MET-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-MET-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-MET-003

**Acceptance criteria**
- [ ] 0 cases where a consolidated statement has a higher status than its lowest-status input; ≥ 95% of input propositions represented in output (measured by SASI entailment)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-MET-010 [P2] REQ-MET-010: metabolism-service computes the metrics above hourly and stores daily snapshots for ≥ 400 days

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:770-770` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-MET-010; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-MET-010 | `metabolism-service` computes the metrics above hourly and stores daily snapshots for ≥ 400 days.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-MET-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-MET-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-MET-010

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-MET-010 | metabolism-service computes the metrics above hourly and stores daily snapshots for ≥ 400 days.»
- [ ] metabolism-service computes the metrics above hourly and stores daily snapshots for ≥ 400 days.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-MET-011 [P2] REQ-MET-011: GET /metabolism/metrics?from&to&domain&type and GET /brain-health (aggregate score and the per-region breakdown that Invention 1 contributes, §14.1)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:771-771` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-MET-011; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-MET-011 | `GET /metabolism/metrics?from&to&domain&type` and `GET /brain-health` (aggregate score and the per-region breakdown that Invention 1 contributes, §14.1).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-MET-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-MET-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-MET-011

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-MET-011 | GET /metabolism/metrics?from&to&domain&type and GET /brain-health (aggregate score and the per-region breakdown that Invention 1 contributes, §14.1).»
- [ ] GET /metabolism/metrics?from&to&domain&type and GET /brain-health (aggregate score and the per-region breakdown that Invention 1 contributes, §14.1).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-MET-012 [P2] REQ-MET-012: Brain Health score = weighted mean of normalized freshness index (0.3), 1 − normalized toxicity (0.25), 1 − normalized verification backlog (0.15), 1 − drift hotspot density from Invention 1 (0.2), di

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:772-772` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-MET-012; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-MET-012 | Brain Health score = weighted mean of normalized freshness index (0.3), 1 − normalized toxicity (0.25), 1 − normalized verification backlog (0.15), 1 − drift hotspot density from Invention 1 (0.2), digestion-latency score (0.1). Weights are configuration `brainhealth.weights`. Normalizations documented in code and in the UI tooltip.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-MET-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-MET-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-MET-012

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-MET-012 | Brain Health score = weighted mean of normalized freshness index (0.3), 1 − normalized toxicity (0.25), 1 − normalized verification backlog (0.15), 1 − drift hotspot density from Invention 1 (0.2), digestion-latency score (0.1). Weights are configuration brainhealth.weights. Normalizations documented in code and in the UI tooltip.»
- [ ] Brain Health score = weighted mean of normalized freshness index (0.3), 1 − normalized toxicity (0.25), 1 − normalized verification backlog (0.15), 1 − drift hotspot density from Invention 1 (0.2), digestion-latency score (0.1). Weights are configuration brainhealth.weights. Normalizations documented in code and in the UI tooltip.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-MMG-001 [P2] REQ-MMG-001: Register every agent artifact: prompts and prompt templates, skills, tool schemas, agent memory records, eval cases, saved queries, report templates, dashboards, cached summaries and embedding indexes

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:712-712` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-MMG-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-MMG-001 | Register every agent artifact: prompts and prompt templates, skills, tool schemas, agent memory records, eval cases, saved queries, report templates, dashboards, cached summaries and embedding indexes. Record `{artifact_id, kind, owner, version, location, content_hash}`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-MMG-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-MMG-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-MMG-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-MMG-001 | Register every agent artifact: prompts and prompt templates, skills, tool schemas, agent memory records, eval cases, saved queries, report templates, dashboards, cached summaries and embedding indexes. Record {artifact_id, kind, owner, version, location, content_hash}.»
- [ ] Register every agent artifact: prompts and prompt templates, skills, tool schemas, agent memory records, eval cases, saved queries, report templates, dashboards, cached summaries and embedding indexes. Record {artifact_id, kind, owner, version, location, content_hash}.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-MMG-002 [P2] REQ-MMG-002: Term extraction: for each artifact, extract references to ontology terms (type names, relation names, property names, enum values, synonyms/labels in every configured language) by exact and alias matc

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:713-713` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-MMG-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-MMG-002 | Term extraction: for each artifact, extract references to ontology terms (type names, relation names, property names, enum values, synonyms/labels in every configured language) by exact and alias matching against the ontology's labels, plus embedding similarity ≥ `meaning.term_sim` (default 0.9) for free text. Store edges `(:OntologyTerm)-[:USED_BY {count, spans}]->(:AgentArtifact)`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-MMG-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-MMG-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-MMG-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-MMG-002 | Term extraction: for each artifact, extract references to ontology terms (type names, relation names, property names, enum values, synonyms/labels in every configured language) by exact and alias matching against the ontology's labels, plus embedding similarity ≥ meaning.term_sim (default 0.9) for free text. Store edges (:OntologyTerm)-[:USED_BY {count, spans}]->(»
- [ ] Term extraction: for each artifact, extract references to ontology terms (type names, relation names, property names, enum values, synonyms/labels in every configured language) by exact and alias matching against the ontology's labels, plus embedding similarity ≥ meaning.term_sim (default 0.9) for free text. Store edges (:OntologyTerm)-[:USED_BY {count, spans}]->(:AgentArtifact).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-MMG-003 [P2] REQ-MMG-003: Re-extract on artifact change (event-driven) and nightly full sweep

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:714-714` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-MMG-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-MMG-003 | Re-extract on artifact change (event-driven) and nightly full sweep.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-MMG-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-MMG-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-MMG-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-MMG-003 | Re-extract on artifact change (event-driven) and nightly full sweep.»
- [ ] Re-extract on artifact change (event-driven) and nightly full sweep.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-MMG-012 [P2] REQ-MMG-012: Publishing a release applies ontology v+1 and all approved rewrites atomically from the user's point of view: either all artifacts reference v+1 or the release is rolled back

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:740-740` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-MMG-012; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-MMG-012 | Publishing a release applies ontology v+1 and all approved rewrites atomically from the user's point of view: either all artifacts reference v+1 or the release is rolled back.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-MMG-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-MMG-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-MMG-012

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-MMG-012 | Publishing a release applies ontology v+1 and all approved rewrites atomically from the user's point of view: either all artifacts reference v+1 or the release is rolled back.»
- [ ] Publishing a release applies ontology v+1 and all approved rewrites atomically from the user's point of view: either all artifacts reference v+1 or the release is rolled back.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-MMG-014 [P2] REQ-MMG-014: Metric: orphaned-term count = artifacts referencing terms absent from the active ontology version; target 0 after publish

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:742-742` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-MMG-014; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-MMG-014 | Metric: orphaned-term count = artifacts referencing terms absent from the active ontology version; target 0 after publish.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-MMG-014' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-MMG-014') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-MMG-014

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-MMG-014 | Metric: orphaned-term count = artifacts referencing terms absent from the active ontology version; target 0 after publish.»
- [ ] Metric: orphaned-term count = artifacts referencing terms absent from the active ontology version; target 0 after publish.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-MMG-015 [P2] REQ-MMG-015: Demonstration scenario: rename a relation type used by 3 prompts, 1 saved query and 5 eval cases; release shows exactly those artifacts; rewrites applied; evals pass; publish; orphaned-term count = 0.

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:743-743` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-MMG-015; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-MMG-015 | Demonstration scenario: rename a relation type used by 3 prompts, 1 saved query and 5 eval cases; release shows exactly those artifacts; rewrites applied; evals pass; publish; orphaned-term count = 0. Then split a type and show the human-review step blocks publish until approved.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-MMG-015' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-MMG-015') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-MMG-015

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-MMG-015 | Demonstration scenario: rename a relation type used by 3 prompts, 1 saved query and 5 eval cases; release shows exactly those artifacts; rewrites applied; evals pass; publish; orphaned-term count = 0. Then split a type and show the human-review step blocks publish until approved.»
- [ ] Demonstration scenario: rename a relation type used by 3 prompts, 1 saved query and 5 eval cases; release shows exactly those artifacts; rewrites applied; evals pass; publish; orphaned-term count = 0. Then split a type and show the human-review step blocks publish until approved.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-NEU-001 [P2] REQ-NEU-001: Graph snapshot export per tenant, per level (instance, meta, ontology) into a columnar format (Parquet) with node table (id, type, properties encoded), edge table (src, dst, relation, properties), and

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:797-797` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-NEU-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-NEU-001 | Graph snapshot export per tenant, per level (instance, meta, ontology) into a columnar format (Parquet) with node table (id, type, properties encoded), edge table (src, dst, relation, properties), and snapshot metadata (graph_version, recorded_at, counts). Schedule `neural.snapshot_cron` (default daily 01:00 tenant time) and on demand.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-NEU-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-NEU-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-NEU-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-NEU-001 | Graph snapshot export per tenant, per level (instance, meta, ontology) into a columnar format (Parquet) with node table (id, type, properties encoded), edge table (src, dst, relation, properties), and snapshot metadata (graph_version, recorded_at, counts). Schedule neural.snapshot_cron (default daily 01:00 tenant time) and on demand.»
- [ ] Graph snapshot export per tenant, per level (instance, meta, ontology) into a columnar format (Parquet) with node table (id, type, properties encoded), edge table (src, dst, relation, properties), and snapshot metadata (graph_version, recorded_at, counts). Schedule neural.snapshot_cron (default daily 01:00 tenant time) and on demand.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-NEU-002 [P2] REQ-NEU-002: Feature pipeline: type one-hot (or learned type embeddings), numeric properties standardized, text properties embedded with the local embedding model, degree features, recency features (days since las

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:798-798` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-NEU-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-NEU-002 | Feature pipeline: type one-hot (or learned type embeddings), numeric properties standardized, text properties embedded with the local embedding model, degree features, recency features (days since last change). Feature definitions versioned.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-NEU-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-NEU-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-NEU-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-NEU-002 | Feature pipeline: type one-hot (or learned type embeddings), numeric properties standardized, text properties embedded with the local embedding model, degree features, recency features (days since last change). Feature definitions versioned.»
- [ ] Feature pipeline: type one-hot (or learned type embeddings), numeric properties standardized, text properties embedded with the local embedding model, degree features, recency features (days since last change). Feature definitions versioned.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-NEU-003 [P2] REQ-NEU-003: Snapshots respect data classes: restricted-class properties are excluded from features unless neural.includerestricted=true for the tenant

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:799-799` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-NEU-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-NEU-003 | Snapshots respect data classes: restricted-class properties are excluded from features unless `neural.include_restricted=true` for the tenant.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-NEU-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-NEU-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-NEU-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-NEU-003 | Snapshots respect data classes: restricted-class properties are excluded from features unless neural.include_restricted=true for the tenant.»
- [ ] Snapshots respect data classes: restricted-class properties are excluded from features unless neural.include_restricted=true for the tenant.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-NEU-010 [P2] REQ-NEU-010: Use PyTorch and PyTorch Geometric (heterogeneous graph support) unless the repository already standardizes on another graph-ML library; record DR either way

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:805-805` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-NEU-010; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-NEU-010 | Use PyTorch and PyTorch Geometric (heterogeneous graph support) unless the repository already standardizes on another graph-ML library; record DR either way.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-NEU-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-NEU-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-NEU-010

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-NEU-010 | Use PyTorch and PyTorch Geometric (heterogeneous graph support) unless the repository already standardizes on another graph-ML library; record DR either way.»
- [ ] Use PyTorch and PyTorch Geometric (heterogeneous graph support) unless the repository already standardizes on another graph-ML library; record DR either way.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-NEU-011 [P2] REQ-NEU-011: Runs on CPU (mandatory) and uses a GPU when present. Training jobs declare memory needs; jobs exceeding available memory use neighbour sampling (GraphSAGE-style loaders) instead of failing

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:806-806` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-NEU-011; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-NEU-011 | Runs on CPU (mandatory) and uses a GPU when present. Training jobs declare memory needs; jobs exceeding available memory use neighbour sampling (GraphSAGE-style loaders) instead of failing.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-NEU-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-NEU-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-NEU-011

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-NEU-011 | Runs on CPU (mandatory) and uses a GPU when present. Training jobs declare memory needs; jobs exceeding available memory use neighbour sampling (GraphSAGE-style loaders) instead of failing.»
- [ ] Runs on CPU (mandatory) and uses a GPU when present. Training jobs declare memory needs; jobs exceeding available memory use neighbour sampling (GraphSAGE-style loaders) instead of failing.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-NEU-012 [P2] REQ-NEU-012: Chronological splits for every temporal task; no future information in training features (leakage test required per model)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:807-807` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-NEU-012; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-NEU-012 | Chronological splits for every temporal task; no future information in training features (leakage test required per model).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-NEU-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-NEU-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-NEU-012

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-NEU-012 | Chronological splits for every temporal task; no future information in training features (leakage test required per model).»
- [ ] Chronological splits for every temporal task; no future information in training features (leakage test required per model).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-NEU-013 [P2] REQ-NEU-013: Every model's predictions are warranted: operator class MODEL, status ≤ PREDICTED, grounds include modelrun with model id and version. Predictions never overwrite observed assertions (REQ-WAR-022)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:808-808` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-NEU-013; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-NEU-013 | Every model's predictions are warranted: operator class `MODEL`, status ≤ `PREDICTED`, grounds include `model_run` with model id and version. Predictions never overwrite observed assertions (REQ-WAR-022).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-NEU-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-NEU-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-NEU-013

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-NEU-013 | Every model's predictions are warranted: operator class MODEL, status ≤ PREDICTED, grounds include model_run with model id and version. Predictions never overwrite observed assertions (REQ-WAR-022).»
- [ ] Every model's predictions are warranted: operator class MODEL, status ≤ PREDICTED, grounds include model_run with model id and version. Predictions never overwrite observed assertions (REQ-WAR-022).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-NEU-020 [P2] REQ-NEU-020: Embeddings stored per (tenant, level, modelversion, snapshotversion) in KGF's vector store abstraction, with nearest-neighbour search

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:814-814` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-NEU-020; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-NEU-020 | Embeddings stored per `(tenant, level, model_version, snapshot_version)` in KGF's vector store abstraction, with nearest-neighbour search.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-NEU-020' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-NEU-020') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-NEU-020

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-NEU-020 | Embeddings stored per (tenant, level, model_version, snapshot_version) in KGF's vector store abstraction, with nearest-neighbour search.»
- [ ] Embeddings stored per (tenant, level, model_version, snapshot_version) in KGF's vector store abstraction, with nearest-neighbour search.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-NEU-021 [P2] REQ-NEU-021: Embedding alignment across retrains: orthogonal Procrustes alignment on anchor entities (entities unchanged between snapshots, ≥ 1,000 or all if fewer) before any cross-snapshot comparison. Alignment 

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:815-815` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-NEU-021; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-NEU-021 | Embedding alignment across retrains: orthogonal Procrustes alignment on anchor entities (entities unchanged between snapshots, ≥ 1,000 or all if fewer) before any cross-snapshot comparison. Alignment matrix stored with the snapshot.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-NEU-021' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-NEU-021') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-NEU-021

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-NEU-021 | Embedding alignment across retrains: orthogonal Procrustes alignment on anchor entities (entities unchanged between snapshots, ≥ 1,000 or all if fewer) before any cross-snapshot comparison. Alignment matrix stored with the snapshot.»
- [ ] Embedding alignment across retrains: orthogonal Procrustes alignment on anchor entities (entities unchanged between snapshots, ≥ 1,000 or all if fewer) before any cross-snapshot comparison. Alignment matrix stored with the snapshot.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-NEU-032 [P2] REQ-NEU-032: Absent-capability rule: if no registry exists, use MLflow (self-hosted) or implement the fields above in KGF's metadata store; record DR

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:823-823` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-NEU-032; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-NEU-032 | Absent-capability rule: if no registry exists, use MLflow (self-hosted) or implement the fields above in KGF's metadata store; record DR.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-NEU-032' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-NEU-032') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-NEU-032

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-NEU-032 | Absent-capability rule: if no registry exists, use MLflow (self-hosted) or implement the fields above in KGF's metadata store; record DR.»
- [ ] Absent-capability rule: if no registry exists, use MLflow (self-hosted) or implement the fields above in KGF's metadata store; record DR.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PLT-008 [P2] REQ-PLT-008: All timestamps are stored in UTC, ISO-8601 with milliseconds. All ids are UUIDv7 unless this document says otherwise

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:149-149` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PLT-008; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PLT-008 | All timestamps are stored in UTC, ISO-8601 with milliseconds. All ids are UUIDv7 unless this document says otherwise.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PLT-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PLT-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PLT-008

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PLT-008 | All timestamps are stored in UTC, ISO-8601 with milliseconds. All ids are UUIDv7 unless this document says otherwise.»
- [ ] All timestamps are stored in UTC, ISO-8601 with milliseconds. All ids are UUIDv7 unless this document says otherwise.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PRC-001 [P2] REQ-PRC-001: Warrant Review · New or changed operator registration · Queue of pending operators showing proposed class, action class, sample inputs/outputs; approve/reject with reason; approved changes take effect

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:947-947` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PRC-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PRC-001 | Warrant Review | New or changed operator registration | Queue of pending operators showing proposed class, action class, sample inputs/outputs; approve/reject with reason; approved changes take effect immediately and are audited
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PRC-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PRC-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PRC-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PRC-001 | Warrant Review | New or changed operator registration | Queue of pending operators showing proposed class, action class, sample inputs/outputs; approve/reject with reason; approved changes take effect immediately and are audited»
- [ ] New or changed operator registration
- [ ] Queue of pending operators showing proposed class, action class, sample inputs/outputs; approve/reject with reason; approved changes take effect immediately and are audited
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PRC-002 [P2] REQ-PRC-002: Meaning Release · New ontology version draft · The meaning release workflow (§11) is the tooling

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:948-948` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PRC-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PRC-002 | Meaning Release | New ontology version draft | The meaning release workflow (§11) is the tooling
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PRC-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PRC-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PRC-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PRC-002 | Meaning Release | New ontology version draft | The meaning release workflow (§11) is the tooling»
- [ ] New ontology version draft
- [ ] The meaning release workflow (§11) is the tooling
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PRC-003 [P2] REQ-PRC-003: Laundering Audit · Monthly (audit.cron) · Sample per REQ-LIN-002; report with laundering rate and offending operators; one-click creation of verification tasks

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:949-949` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PRC-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PRC-003 | Laundering Audit | Monthly (`audit.cron`) | Sample per REQ-LIN-002; report with laundering rate and offending operators; one-click creation of verification tasks
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PRC-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PRC-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PRC-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PRC-003 | Laundering Audit | Monthly (audit.cron) | Sample per REQ-LIN-002; report with laundering rate and offending operators; one-click creation of verification tasks»
- [ ] Sample per REQ-LIN-002; report with laundering rate and offending operators; one-click creation of verification tasks
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PRC-004 [P2] REQ-PRC-004: Budget Calibration · Quarterly · Report per agent class: κ distribution, escalations, approvals, incidents linked to agent actions; proposed new B_max and ρ; apply with approval

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:950-950` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PRC-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PRC-004 | Budget Calibration | Quarterly | Report per agent class: κ distribution, escalations, approvals, incidents linked to agent actions; proposed new B_max and ρ; apply with approval
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PRC-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PRC-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PRC-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PRC-004 | Budget Calibration | Quarterly | Report per agent class: κ distribution, escalations, approvals, incidents linked to agent actions; proposed new B_max and ρ; apply with approval»
- [ ] Report per agent class: κ distribution, escalations, approvals, incidents linked to agent actions; proposed new B_max and ρ; apply with approval
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PRC-005 [P2] REQ-PRC-005: Protected-Fact Review · Quarterly · Registry diff since last review, derivation-block log with top patterns, false-block reports from users; sign-off

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:951-951` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PRC-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PRC-005 | Protected-Fact Review | Quarterly | Registry diff since last review, derivation-block log with top patterns, false-block reports from users; sign-off
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PRC-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PRC-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PRC-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PRC-005 | Protected-Fact Review | Quarterly | Registry diff since last review, derivation-block log with top patterns, false-block reports from users; sign-off»
- [ ] Registry diff since last review, derivation-block log with top patterns, false-block reports from users; sign-off
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PRC-006 [P2] REQ-PRC-006: Metabolism Review · Monthly · Metabolism metrics per domain (§12.2), half-life refits, drift hotspots, verification backlog; sign-off

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:952-952` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PRC-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PRC-006 | Metabolism Review | Monthly | Metabolism metrics per domain (§12.2), half-life refits, drift hotspots, verification backlog; sign-off
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PRC-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PRC-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PRC-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PRC-006 | Metabolism Review | Monthly | Metabolism metrics per domain (§12.2), half-life refits, drift hotspots, verification backlog; sign-off»
- [ ] Metabolism metrics per domain (§12.2), half-life refits, drift hotspots, verification backlog; sign-off
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PRC-007 [P2] REQ-PRC-007: Commitment Review · Weekly (commitment.review_cron) · Commitments at risk, broken and transferred in the period per agent class; kept rate trend; one-click reassignment; sign-off

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:953-953` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PRC-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PRC-007 | Commitment Review | Weekly (`commitment.review_cron`) | Commitments at risk, broken and transferred in the period per agent class; kept rate trend; one-click reassignment; sign-off
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PRC-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PRC-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PRC-007

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PRC-007 | Commitment Review | Weekly (commitment.review_cron) | Commitments at risk, broken and transferred in the period per agent class; kept rate trend; one-click reassignment; sign-off»
- [ ] Commitments at risk, broken and transferred in the period per agent class; kept rate trend; one-click reassignment; sign-off
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PRC-008 [P2] REQ-PRC-008: Dissent Review · Monthly, and on every minority-report revisit trigger · Decisions with minority reports, triggered revisits, vindicated minorities, ungrounded-shift rate per agent; sign-off

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:954-954` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PRC-008; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PRC-008 | Dissent Review | Monthly, and on every minority-report revisit trigger | Decisions with minority reports, triggered revisits, vindicated minorities, ungrounded-shift rate per agent; sign-off
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PRC-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PRC-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PRC-008

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PRC-008 | Dissent Review | Monthly, and on every minority-report revisit trigger | Decisions with minority reports, triggered revisits, vindicated minorities, ungrounded-shift rate per agent; sign-off»
- [ ] Monthly, and on every minority-report revisit trigger
- [ ] Decisions with minority reports, triggered revisits, vindicated minorities, ungrounded-shift rate per agent; sign-off
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-PRC-009 [P2] REQ-PRC-009: Reflex Rule Review · Quarterly · Every enabled reflex rule with fire count, blocked fires, false fires reported by users, approver still valid; re-approval or disable

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:955-955` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-PRC-009; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-PRC-009 | Reflex Rule Review | Quarterly | Every enabled reflex rule with fire count, blocked fires, false fires reported by users, approver still valid; re-approval or disable
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-PRC-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-PRC-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-PRC-009

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-PRC-009 | Reflex Rule Review | Quarterly | Every enabled reflex rule with fire count, blocked fires, false fires reported by users, approver still valid; re-approval or disable»
- [ ] Every enabled reflex rule with fire count, blocked fires, false fires reported by users, approver still valid; re-approval or disable
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-RFX-001 [P2] REQ-RFX-001: Rule model: {ruleid, tenantid, name, triggertopic, condition (KGF pattern evaluated on the event's subject neighbourhood), action {toolid, parametertemplate}, approverprincipalid, approvedat, budgetcl

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1402-1402` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-RFX-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-RFX-001 | Rule model: `{rule_id, tenant_id, name, trigger_topic, condition (KGF pattern evaluated on the event's subject neighbourhood), action {tool_id, parameter_template}, approver_principal_id, approved_at, budget_class, max_fires_per_hour, enabled, dry_run_report_id}`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-RFX-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-RFX-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-RFX-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-RFX-001 | Rule model: {rule_id, tenant_id, name, trigger_topic, condition (KGF pattern evaluated on the event's subject neighbourhood), action {tool_id, parameter_template}, approver_principal_id, approved_at, budget_class, max_fires_per_hour, enabled, dry_run_report_id}.»
- [ ] Rule model: {rule_id, tenant_id, name, trigger_topic, condition (KGF pattern evaluated on the event's subject neighbourhood), action {tool_id, parameter_template}, approver_principal_id, approved_at, budget_class, max_fires_per_hour, enabled, dry_run_report_id}.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-RFX-004 [P2] REQ-RFX-004: Every fire passes the commit checkpoint (minimum status, leases on the condition's facts, κ against the rule's budget class). Fires that fail become escalations; they are never retried automatically

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1405-1405` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-RFX-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-RFX-004 | Every fire passes the `commit` checkpoint (minimum status, leases on the condition's facts, κ against the rule's budget class). Fires that fail become escalations; they are never retried automatically.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-RFX-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-RFX-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-RFX-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-RFX-004 | Every fire passes the commit checkpoint (minimum status, leases on the condition's facts, κ against the rule's budget class). Fires that fail become escalations; they are never retried automatically.»
- [ ] Every fire passes the commit checkpoint (minimum status, leases on the condition's facts, κ against the rule's budget class). Fires that fail become escalations; they are never retried automatically.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-RFX-005 [P2] REQ-RFX-005: Latency: from event publication to commit decision p95 < reflex.latencybudgetms (500 ms) at 100 matching events per second per tenant

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1406-1406` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-RFX-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-RFX-005 | Latency: from event publication to commit decision p95 < `reflex.latency_budget_ms` (500 ms) at 100 matching events per second per tenant.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-RFX-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-RFX-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-RFX-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-RFX-005 | Latency: from event publication to commit decision p95 < reflex.latency_budget_ms (500 ms) at 100 matching events per second per tenant.»
- [ ] Latency: from event publication to commit decision p95 < reflex.latency_budget_ms (500 ms) at 100 matching events per second per tenant.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-RFX-006 [P2] REQ-RFX-006: Rate limit and circuit breaker: more than maxfiresperhour fires opens the circuit (RFXRATELIMITED), disables the rule until reflex.circuitreset passes or a person re-enables it, and notifies the appro

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1407-1407` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-RFX-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-RFX-006 | Rate limit and circuit breaker: more than `max_fires_per_hour` fires opens the circuit (`RFX_RATE_LIMITED`), disables the rule until `reflex.circuit_reset` passes or a person re-enables it, and notifies the approver.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-RFX-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-RFX-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-RFX-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-RFX-006 | Rate limit and circuit breaker: more than max_fires_per_hour fires opens the circuit (RFX_RATE_LIMITED), disables the rule until reflex.circuit_reset passes or a person re-enables it, and notifies the approver.»
- [ ] Rate limit and circuit breaker: more than max_fires_per_hour fires opens the circuit (RFX_RATE_LIMITED), disables the rule until reflex.circuit_reset passes or a person re-enables it, and notifies the approver.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-RFX-007 [P2] REQ-RFX-007: APIs per §19.7, UI 18.22, metric kgfipreflexfirestotal, quarterly review REQ-PRC-009

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1408-1408` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-RFX-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-RFX-007 | APIs per §19.7, UI 18.22, metric `kgf_ip_reflex_fires_total`, quarterly review REQ-PRC-009.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-RFX-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-RFX-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-RFX-007

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-RFX-007 | APIs per §19.7, UI 18.22, metric kgf_ip_reflex_fires_total, quarterly review REQ-PRC-009.»
- [ ] APIs per §19.7, UI 18.22, metric kgf_ip_reflex_fires_total, quarterly review REQ-PRC-009.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-SAS-003 [P2] REQ-SAS-003: SASI output is a list of (proposition, span, warrant); the UI renders spans coloured by status (§18.2)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:447-447` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-SAS-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-SAS-003 | SASI output is a list of `(proposition, span, warrant)`; the UI renders spans coloured by status (§18.2).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-SAS-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-SAS-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-SAS-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-SAS-003 | SASI output is a list of (proposition, span, warrant); the UI renders spans coloured by status (§18.2).»
- [ ] SASI output is a list of (proposition, span, warrant); the UI renders spans coloured by status (§18.2).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-SAS-005 [P2] REQ-SAS-005: Latency: p95 < 1.5 s for outputs ≤ 1,500 characters on the reference hardware recorded in DR (CPU-only allowed). Batch NLI calls

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:449-449` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-SAS-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-SAS-005 | Latency: p95 < 1.5 s for outputs ≤ 1,500 characters on the reference hardware recorded in DR (CPU-only allowed). Batch NLI calls.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-SAS-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-SAS-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-SAS-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-SAS-005 | Latency: p95 < 1.5 s for outputs ≤ 1,500 characters on the reference hardware recorded in DR (CPU-only allowed). Batch NLI calls.»
- [ ] Latency: p95 < 1.5 s for outputs ≤ 1,500 characters on the reference hardware recorded in DR (CPU-only allowed). Batch NLI calls.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-SDK-001 [P2] REQ-SDK-001: Provide an SDK in every language that hosts KGF agents or LLM features (at minimum the backend language). API: with warrantcontext(principal, planid): …, observe(toolid, call), compute(operatorid, fn,

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:489-489` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-SDK-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-SDK-001 | Provide an SDK in every language that hosts KGF agents or LLM features (at minimum the backend language). API: `with warrant_context(principal, plan_id): …`, `observe(tool_id, call)`, `compute(operator_id, fn, inputs)`, `model(operator_id, fn, inputs)`, `generate(operator_id, prompt, inputs)`, `handoff(target_agent, message, warrants)`, `commit(action, warrants)`, `answer(text, warrants)`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-SDK-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-SDK-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-SDK-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-SDK-001 | Provide an SDK in every language that hosts KGF agents or LLM features (at minimum the backend language). API: with warrant_context(principal, plan_id): …, observe(tool_id, call), compute(operator_id, fn, inputs), model(operator_id, fn, inputs), generate(operator_id, prompt, inputs), handoff(target_agent, message, warrants), commit(action, warrants), answer(text, »
- [ ] Provide an SDK in every language that hosts KGF agents or LLM features (at minimum the backend language). API: with warrant_context(principal, plan_id): …, observe(tool_id, call), compute(operator_id, fn, inputs), model(operator_id, fn, inputs), generate(operator_id, prompt, inputs), handoff(target_agent, message, warrants), commit(action, warrants), answer(text, warrants).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-SDK-004 [P2] REQ-SDK-004: An MCP-compatible wrapper SHOULD be provided so external agents connected to KGF through MCP receive warrants on every tool result and must present warrants on write tools

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:492-492` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-SDK-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-SDK-004 | An MCP-compatible wrapper SHOULD be provided so external agents connected to KGF through MCP receive warrants on every tool result and must present warrants on write tools.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-SDK-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-SDK-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-SDK-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-SDK-004 | An MCP-compatible wrapper SHOULD be provided so external agents connected to KGF through MCP receive warrants on every tool result and must present warrants on write tools.»
- [ ] An MCP-compatible wrapper SHOULD be provided so external agents connected to KGF through MCP receive warrants on every tool result and must present warrants on write tools.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-SHB-003 [P2] REQ-SHB-003: POST /branches/{id}/execute-plan runs an agent plan against the branch using simulated tools, then computes GET /branches/{id}/diff (added, removed, changed assertions with warrants), impact (Inventio

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:782-782` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-SHB-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-SHB-003 | `POST /branches/{id}/execute-plan` runs an agent plan against the branch using simulated tools, then computes `GET /branches/{id}/diff` (added, removed, changed assertions with warrants), impact (Invention 2 on the diff), κ (A4) and SHACL validation results.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-SHB-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-SHB-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-SHB-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-SHB-003 | POST /branches/{id}/execute-plan runs an agent plan against the branch using simulated tools, then computes GET /branches/{id}/diff (added, removed, changed assertions with warrants), impact (Invention 2 on the diff), κ (A4) and SHACL validation results.»
- [ ] POST /branches/{id}/execute-plan runs an agent plan against the branch using simulated tools, then computes GET /branches/{id}/diff (added, removed, changed assertions with warrants), impact (Invention 2 on the diff), κ (A4) and SHACL validation results.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-SHB-006 [P2] REQ-SHB-006: Used by Invention 8 (counterfactual path removal), Invention 11 (merge simulation) and Invention 4 (impact simulation)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:785-785` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-SHB-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-SHB-006 | Used by Invention 8 (counterfactual path removal), Invention 11 (merge simulation) and Invention 4 (impact simulation).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-SHB-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-SHB-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-SHB-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-SHB-006 | Used by Invention 8 (counterfactual path removal), Invention 11 (merge simulation) and Invention 4 (impact simulation).»
- [ ] Used by Invention 8 (counterfactual path removal), Invention 11 (merge simulation) and Invention 4 (impact simulation).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-VER-001 [P2] REQ-VER-001: A verification task has: taskid, tenantid, proposition, warrantid, reason (GENERATEDPREMISE, LEASEEXPIRED, HALFLIFEDUE, DRIFT, LAUNDERINGAUDIT), suggestedobserverids[], assignee?, dueat, state (OPEN, 

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:498-498` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-VER-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-VER-001 | A verification task has: `task_id`, `tenant_id`, `proposition`, `warrant_id`, `reason` (`GENERATED_PREMISE`, `LEASE_EXPIRED`, `HALF_LIFE_DUE`, `DRIFT`, `LAUNDERING_AUDIT`), `suggested_observer_ids[]`, `assignee?`, `due_at`, `state` (`OPEN`, `IN_PROGRESS`, `RESOLVED_CONFIRMED`, `RESOLVED_REFUTED`, `EXPIRED`).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-VER-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-VER-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-VER-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-VER-001 | A verification task has: task_id, tenant_id, proposition, warrant_id, reason (GENERATED_PREMISE, LEASE_EXPIRED, HALF_LIFE_DUE, DRIFT, LAUNDERING_AUDIT), suggested_observer_ids[], assignee?, due_at, state (OPEN, IN_PROGRESS, RESOLVED_CONFIRMED, RESOLVED_REFUTED, EXPIRED).»
- [ ] A verification task has: task_id, tenant_id, proposition, warrant_id, reason (GENERATED_PREMISE, LEASE_EXPIRED, HALF_LIFE_DUE, DRIFT, LAUNDERING_AUDIT), suggested_observer_ids[], assignee?, due_at, state (OPEN, IN_PROGRESS, RESOLVED_CONFIRMED, RESOLVED_REFUTED, EXPIRED).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-VER-003 [P2] REQ-VER-003: GET /verification-tasks with filters (state, reason, type, assignee, due before), POST /verification-tasks/{id}/resolve with {outcome, observerid? , note?}

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:500-500` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-VER-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-VER-003 | `GET /verification-tasks` with filters (state, reason, type, assignee, due before), `POST /verification-tasks/{id}/resolve` with `{outcome, observer_id? , note?}`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-VER-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-VER-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-VER-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-VER-003 | GET /verification-tasks with filters (state, reason, type, assignee, due before), POST /verification-tasks/{id}/resolve with {outcome, observer_id? , note?}.»
- [ ] GET /verification-tasks with filters (state, reason, type, assignee, due before), POST /verification-tasks/{id}/resolve with {outcome, observer_id? , note?}.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-WCA-005 [P2] REQ-WCA-005: compose p95 latency < 5 ms in-process for n ≤ 50 inputs and ≤ 200 grounds

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:427-427` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-WCA-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-WCA-005 | `compose` p95 latency < 5 ms in-process for n ≤ 50 inputs and ≤ 200 grounds.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-WCA-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-WCA-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-WCA-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-WCA-005 | compose p95 latency < 5 ms in-process for n ≤ 50 inputs and ≤ 200 grounds.»
- [ ] compose p95 latency < 5 ms in-process for n ≤ 50 inputs and ≤ 200 grounds.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-WCA-006 [P2] REQ-WCA-006: POST /warrants/compose exposes A1 over HTTP for out-of-process agents (request: operatorid, inputwarrantids[], receiptgrounds[], subject; response: the stored warrant)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:428-428` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-WCA-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-WCA-006 | `POST /warrants/compose` exposes A1 over HTTP for out-of-process agents (request: `operator_id`, `input_warrant_ids[]`, `receipt_grounds[]`, `subject`; response: the stored warrant).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-WCA-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-WCA-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-WCA-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-WCA-006 | POST /warrants/compose exposes A1 over HTTP for out-of-process agents (request: operator_id, input_warrant_ids[], receipt_grounds[], subject; response: the stored warrant).»
- [ ] POST /warrants/compose exposes A1 over HTTP for out-of-process agents (request: operator_id, input_warrant_ids[], receipt_grounds[], subject; response: the stored warrant).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CMT-010 [P3] REQ-CMT-010: Transfer on retirement: disabling, deleting or replacing (new version with a different identity) an agent identity with open commitments is refused with CMTORPHANED unless a successor is named; then e

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1343-1343` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CMT-010; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CMT-010 | Transfer on retirement: disabling, deleting or replacing (new version with a different identity) an agent identity with open commitments is refused with `CMT_ORPHANED` unless a successor is named; then every open commitment is copied to a new commitment for the successor (`TRANSFERRED_TO` link, same due date, promisees notified) and the original becomes `TRANSFERRED`. Platform-level configuration MAY name a default human owner per agent class as successor.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CMT-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CMT-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CMT-010

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CMT-010 | Transfer on retirement: disabling, deleting or replacing (new version with a different identity) an agent identity with open commitments is refused with CMT_ORPHANED unless a successor is named; then every open commitment is copied to a new commitment for the successor (TRANSFERRED_TO link, same due date, promisees notified) and the original becomes TRANSFERRED. P»
- [ ] Transfer on retirement: disabling, deleting or replacing (new version with a different identity) an agent identity with open commitments is refused with CMT_ORPHANED unless a successor is named; then every open commitment is copied to a new commitment for the successor (TRANSFERRED_TO link, same due date, promisees notified) and the original becomes TRANSFERRED. Platform-level configuration MAY na
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-LSE-002 [P3] REQ-LSE-002: Absent-capability rule: if the graph write path does not emit events, implement a transactional outbox table/collection written in the same transaction as the graph write (or in a compensating step fo

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:527-527` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-LSE-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-LSE-002 | Absent-capability rule: if the graph write path does not emit events, implement a transactional outbox table/collection written in the same transaction as the graph write (or in a compensating step for databases without multi-store transactions, with at-least-once delivery and idempotent consumers). Database-native change-data-capture MAY replace the outbox per database adapter; record DR.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-LSE-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-LSE-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-LSE-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-LSE-002 | Absent-capability rule: if the graph write path does not emit events, implement a transactional outbox table/collection written in the same transaction as the graph write (or in a compensating step for databases without multi-store transactions, with at-least-once delivery and idempotent consumers). Database-native change-data-capture MAY replace the outbox per da»
- [ ] Absent-capability rule: if the graph write path does not emit events, implement a transactional outbox table/collection written in the same transaction as the graph write (or in a compensating step for databases without multi-store transactions, with at-least-once delivery and idempotent consumers). Database-native change-data-capture MAY replace the outbox per database adapter; record DR.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

