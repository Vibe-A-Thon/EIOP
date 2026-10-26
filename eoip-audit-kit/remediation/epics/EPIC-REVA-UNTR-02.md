# EPIC-REVA-UNTR-02: reva-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 60 tasks, ~368.5 h, priorities {'P1': 39, 'P2': 21}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-REVA-GA-003 [P1] REVA-GA-003: Context assembly for LLM synthesis: each context item carries its warrant ID, epistemic state, authority and an untrusted-content fence; system instructions forbid following instructions inside fenced

- **Source:** `reva-requirements.md:1003-1003` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-GA-003 | Context assembly for LLM synthesis: each context item carries its warrant ID, epistemic state, authority and an untrusted-content fence; system instructions forbid following instructions inside fenced content and require citing warrant IDs per claim. | Prompt-injection fixture (ingested Confluence page containing "ignore previous instructions and …") does not change behaviour; the incident is recorded as a `reva.pred.injection_attempt` warrant. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-GA-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-GA-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Prompt-injection fixture (ingested Confluence page containing "ignore previous instructions and …") does not change behaviour; the incident is recorded as a reva.pred.injectionattempt warrant
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-GA-006 [P1] REVA-GA-006: Known-answer evaluation suites (YAML under tests/reva/evaluation/suites/): question, expected claims (value matchers, required kind, required authority set, required predicate), forbidden claims, max 

- **Source:** `reva-requirements.md:1006-1006` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-GA-006 | Known-answer evaluation suites (YAML under `tests/reva/evaluation/suites/`): question, expected claims (value matchers, required kind, required authority set, required predicate), forbidden claims, max LLM calls. Metrics: claim precision/recall, citation validity rate, mis-graded claim rate, absence-overclaim rate, contradiction surfacing rate, latency. | `kgf reva eval run --suite reference` produces a report; CI gate thresholds: citation validity ≥ 0.98, absence-overclaim = 0, mis-graded ≤ 0.02. | evaluation
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-GA-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-GA-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] kgf reva eval run --suite reference produces a report; CI gate thresholds: citation validity ≥ 0.98, absence-overclaim = 0, mis-graded ≤ 0.02
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-GA-007 [P1] REVA-GA-007: Agent transcript evaluation: given an MCP transcript of an agent using REVA tools, check that each final-answer claim is supported by a warrant actually delivered in that transcript, with matching aut

- **Source:** `reva-requirements.md:1007-1007` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-GA-007 | Agent transcript evaluation: given an MCP transcript of an agent using REVA tools, check that each final-answer claim is supported by a warrant actually delivered in that transcript, with matching authority/epistemic state. | Fixture transcripts (supported, unsupported, wrong authority) score correctly. | evaluation
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-GA-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-GA-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture transcripts (supported, unsupported, wrong authority) score correctly
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-GD-002 [P1] REVA-GD-002: Matching tiers, in order: (1) equal logical identity; (2) equal version identity (moved/renamed); (3) git rename/copy detection (git diff -M50% -C) mapping old→new paths; (4) structural fingerprint (i

- **Source:** `reva-requirements.md:952-952` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-GD-002 | Matching tiers, in order: (1) equal logical identity; (2) equal version identity (moved/renamed); (3) git rename/copy detection (`git diff -M50% -C`) mapping old→new paths; (4) structural fingerprint (identifier-insensitive normalized AST token hash, plus a MinHash similarity ≥ 0.8 for near matches); (5) semantic key (kind + sorted neighbour signature). Unresolved one-to-many matches are `ambiguous` with candidates (gap). | Each tier has a fixture where only that tier can match. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-GD-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-GD-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Each tier has a fixture where only that tier can match
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-003 [P1] REVA-IF-003: GET /warrants · Query by subject, predicate, producer, authority, epistemic, time, as-of · viewer

- **Source:** `reva-requirements.md:1224-1224` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-003 | `GET /warrants` | Query by subject, predicate, producer, authority, epistemic, time, as-of | viewer
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-003 | GET /warrants | Query by subject, predicate, producer, authority, epistemic, time, as-of | viewer»
- [ ] Query by subject, predicate, producer, authority, epistemic, time, as-of
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-049 [P1] REVA-IF-049: POST /tracing/sessions (start trace session with dual-key token), GET /tracing/sessions/{id}, POST /tracing/sessions/{id}/stop, POST /tracing/crash-dump · Controlled dynamic tracing & crash triage · s

- **Source:** `reva-requirements.md:1250-1250` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-049 | `POST /tracing/sessions` (start trace session with dual-key token), `GET /tracing/sessions/{id}`, `POST /tracing/sessions/{id}/stop`, `POST /tracing/crash-dump` | Controlled dynamic tracing & crash triage | security_analyst
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-049' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-049') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-049 | POST /tracing/sessions (start trace session with dual-key token), GET /tracing/sessions/{id}, POST /tracing/sessions/{id}/stop, POST /tracing/crash-dump | Controlled dynamic tracing & crash triage | security_analyst»
- [ ] POST /tracing/sessions (start trace session with dual-key token), GET /tracing/sessions/{id}, POST /tracing/sessions/{id}/stop, POST /tracing/crash-dump
- [ ] Controlled dynamic tracing & crash triage
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-050 [P1] REVA-IF-050: POST /trace (seed, template, bounds, as-of), GET /trace/templates, GET /trace/{trace_id} · Feature/impact trace · viewer (results ACL-filtered)

- **Source:** `reva-requirements.md:1251-1251` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-050 | `POST /trace` (seed, template, bounds, as-of), `GET /trace/templates`, `GET /trace/{trace_id}` | Feature/impact trace | viewer (results ACL-filtered)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-050' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-050') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-050 | POST /trace (seed, template, bounds, as-of), GET /trace/templates, GET /trace/{trace_id} | Feature/impact trace | viewer (results ACL-filtered)»
- [ ] POST /trace (seed, template, bounds, as-of), GET /trace/templates, GET /trace/{trace_id}
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-KG-004 [P1] REVA-KG-004: Resolution check: resolved requires ≥ 1 warrant meeting required_authority, required_depth and required_band, with no open contradiction on those warrants. The check result is stored in resolution.che

- **Source:** `reva-requirements.md:721-721` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-KG-004 | Resolution check: `resolved` requires ≥ 1 warrant meeting `required_authority`, `required_depth` and `required_band`, with no open contradiction on those warrants. The check result is stored in `resolution.check_result`. | A resolution citing only inferred warrants for an authority-`runtime_observed` gap is rejected with reason `GAP_AUTHORITY_INSUFFICIENT`. | component
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-KG-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-KG-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] A resolution citing only inferred warrants for an authority-runtimeobserved gap is rejected with reason GAPAUTHORITYINSUFFICIENT
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-MB-003 [P1] REVA-MB-003: Android component topology and intent filter miner. Identifies all Activities, Services, BroadcastReceivers, and ContentProviders; extracts intent filters (actions, categories, data schemes, mime type

- **Source:** `reva-requirements.md:1103-1103` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-MB-003 | Android component topology and intent filter miner. Identifies all Activities, Services, BroadcastReceivers, and ContentProviders; extracts intent filters (actions, categories, data schemes, mime types), deep links, and permission requirements (`android:permission`, `android:exported`). | Builds complete component topology graph; marks all exported components; identifies attack surface and deep-link routing schemes into `reva_MobileComponent` vertices. | unit
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-MB-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-MB-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Builds complete component topology graph; marks all exported components; identifies attack surface and deep-link routing schemes into revaMobileComponent vertices
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-MC-004 [P1] REVA-MC-004: Effect declarations: each tool/endpoint declares effects ∈ {read_only, records_warrants, runs_sandbox, mutates_graph_via_gateway, external_io} and MCP annotations (readOnlyHint, destructiveHint, idemp

- **Source:** `reva-requirements.md:988-988` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-MC-004 | Effect declarations: each tool/endpoint declares `effects ∈ {read_only, records_warrants, runs_sandbox, mutates_graph_via_gateway, external_io}` and MCP annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`) consistent with them. | Metadata test. | unit
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-MC-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-MC-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-MC-004 | Effect declarations: each tool/endpoint declares effects ∈ {read_only, records_warrants, runs_sandbox, mutates_graph_via_gateway, external_io} and MCP annotations (readOnlyHint, destructiveHint, idempotentHint, openWorldHint) consistent with them. | Metadata test. | unit»
- [ ] Effect declarations: each tool/endpoint declares effects ∈ {read_only, records_warrants, runs_sandbox, mutates_graph_via_gateway, external_io} and MCP annotations (readOnlyHint, destructiveHint, idempotentHint, openWorldHint) consistent with them.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-MC-006 [P1] REVA-MC-006: Progress and cancellation: long workflows emit progress notifications (MCP progress tokens; REST server-sent events at /jobs/{id}/events) and honour cancellation; cancellation results keep partial obs

- **Source:** `reva-requirements.md:990-990` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-MC-006 | Progress and cancellation: long workflows emit progress notifications (MCP progress tokens; REST server-sent events at `/jobs/{id}/events`) and honour cancellation; cancellation results keep partial observations and report cleanup status. | Cancel mid-trace and mid-run; partial results and cleanup status are returned. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-MC-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-MC-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Cancel mid-trace and mid-run; partial results and cleanup status are returned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NB-008 [P1] REVA-NB-008: Native binary warrant projection into KGF Knowledge Graph (GL0/GL1). Projects reva_BinaryFunction, reva_BasicBlock, and reva_NativeExport nodes and reva_CALLS_NATIVE, reva_CONTAINS_BLOCK, and reva_BRA

- **Source:** `reva-requirements.md:1088-1088` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NB-008 | Native binary warrant projection into KGF Knowledge Graph (GL0/GL1). Projects `reva_BinaryFunction`, `reva_BasicBlock`, and `reva_NativeExport` nodes and `reva_CALLS_NATIVE`, `reva_CONTAINS_BLOCK`, and `reva_BRANCHES_TO` edges with signed warrants, epistemic state `derived`, and content-addressed IDs. | Graph projection test confirms all functions, basic blocks, and native calls are queryable via `GraphPort`; idempotency test confirms re-projection yields identical nodes without duplication. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NB-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NB-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Graph projection test confirms all functions, basic blocks, and native calls are queryable via GraphPort; idempotency test confirms re-projection yields identical nodes without duplication
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-003 [P1] REVA-NFR-003: Warrant read by ID with signature + ID verification p95 ≤ 10 ms

- **Source:** `reva-requirements.md:1193-1193` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-003 | Warrant read by ID with signature + ID verification p95 ≤ 10 ms. | Perf harness
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-003 | Warrant read by ID with signature + ID verification p95 ≤ 10 ms. | Perf harness»
- [ ] Warrant read by ID with signature + ID verification p95 ≤ 10 ms.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-011 [P1] REVA-NFR-011: Durability: no acknowledged warrant is lost on process crash (fsync/transaction commit before acknowledgement)

- **Source:** `reva-requirements.md:1201-1201` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-011 | Durability: no acknowledged warrant is lost on process crash (fsync/transaction commit before acknowledgement). | Crash-injection test (REVA-WK-007)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-011 | Durability: no acknowledged warrant is lost on process crash (fsync/transaction commit before acknowledgement). | Crash-injection test (REVA-WK-007)»
- [ ] Durability: no acknowledged warrant is lost on process crash (fsync/transaction commit before acknowledgement).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-013 [P1] REVA-NFR-013: Portability: Linux x86-64 and arm64 containers; extractors pure Python except tree-sitter wheels; sandbox degrades to subprocess+rlimits when containers/cgroups are unavailable (recorded as environmen

- **Source:** `reva-requirements.md:1203-1203` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-013 | Portability: Linux x86-64 and arm64 containers; extractors pure Python except tree-sitter wheels; sandbox degrades to subprocess+rlimits when containers/cgroups are unavailable (recorded as environment limitation). | CI matrix
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-013 | Portability: Linux x86-64 and arm64 containers; extractors pure Python except tree-sitter wheels; sandbox degrades to subprocess+rlimits when containers/cgroups are unavailable (recorded as environment limitation). | CI matrix»
- [ ] Portability: Linux x86-64 and arm64 containers; extractors pure Python except tree-sitter wheels; sandbox degrades to subprocess+rlimits when containers/cgroups are unavailable (recorded as environment limitation).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NFR-014 [P1] REVA-NFR-014: Air-gap: full test suite passes with network disabled (except container image pulls pre-cached)

- **Source:** `reva-requirements.md:1204-1204` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NFR-014 | Air-gap: full test suite passes with network disabled (except container image pulls pre-cached). | CI job with `--network none`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-NFR-014' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-NFR-014') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-NFR-014 | Air-gap: full test suite passes with network disabled (except container image pulls pre-cached). | CI job with --network none»
- [ ] Air-gap: full test suite passes with network disabled (except container image pulls pre-cached).
- [ ] CI job with --network none
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-OB-004 [P1] REVA-OB-004: Runbook docs/reva/RUNBOOK.md: key rotation, log audit failure response, restore from backup with log consistency verification, sandbox troubleshooting, re-projection of the graph from warrants (kgf re

- **Source:** `reva-requirements.md:1065-1065` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-OB-004 | Runbook `docs/reva/RUNBOOK.md`: key rotation, log audit failure response, restore from backup with log consistency verification, sandbox troubleshooting, re-projection of the graph from warrants (`kgf reva reproject`). | Each runbook procedure is executed in the acceptance environment at least once (RJ-12). | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-OB-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-OB-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Each runbook procedure is executed in the acceptance environment at least once (RJ-12)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-OB-006 [P1] REVA-OB-006: Re-projection: kgf reva reproject [--backend X] rebuilds all REVA graph elements from warrants (idempotent), enabling backend migration without data loss. · Reprojection into an empty backend yields t

- **Source:** `reva-requirements.md:1067-1067` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-OB-006 | Re-projection: `kgf reva reproject [--backend X]` rebuilds all REVA graph elements from warrants (idempotent), enabling backend migration without data loss. | Reprojection into an empty backend yields the same element counts and properties. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-OB-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-OB-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Reprojection into an empty backend yields the same element counts and properties
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-RO-005 [P1] REVA-RO-005: Deterministic scenario driver and journey attestation. Executes scripted UI interaction journeys (click, fill, navigate); captures timestamped screenshots and video recordings; packages execution logs

- **Source:** `reva-requirements.md:1157-1157` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-RO-005 | Deterministic scenario driver and journey attestation. Executes scripted UI interaction journeys (click, fill, navigate); captures timestamped screenshots and video recordings; packages execution logs and video into signed attestation warrant. | Drives multi-step UI login and form submission scenario; records video and screenshots; generates cryptographic attestation proving journey completion. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-RO-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-RO-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Drives multi-step UI login and form submission scenario; records video and screenshots; generates cryptographic attestation proving journey completion
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SEC-012 [P1] REVA-SEC-012: Retention: per-tenant policies (by predicate/classification) expire warrant envelopes and blobs while keeping the log leaf and a tombstone (retracted_by_retention); legal hold prevents expiry. Log pro

- **Source:** `reva-requirements.md:1033-1033` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SEC-012 | Retention: per-tenant policies (by predicate/classification) expire warrant envelopes and blobs while keeping the log leaf and a tombstone (`retracted_by_retention`); legal hold prevents expiry. Log proofs still verify after expiry. | Retention job fixture; proofs verify; expired content is unreadable. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SEC-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SEC-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Retention job fixture; proofs verify; expired content is unreadable
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SP-003 [P1] REVA-SP-003: .NET: via dnfile, read assembly identity (name, version, culture, public key token), referenced assemblies, TargetFrameworkAttribute, informational version (often containing +<commit>), embedded resou

- **Source:** `reva-requirements.md:858-858` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SP-003 | **.NET**: via `dnfile`, read assembly identity (name, version, culture, public key token), referenced assemblies, `TargetFrameworkAttribute`, informational version (often containing `+<commit>`), embedded resource names; read sibling `*.deps.json` for NuGet package graphs when present. | Fixture assembly and deps.json produce the expected package graph; a commit suffix in the informational version yields a `built_from_commit` warrant with `derived` epistemic state. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SP-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SP-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture assembly and deps.json produce the expected package graph; a commit suffix in the informational version yields a builtfromcommit warrant with derived epistemic state
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SP-005 [P1] REVA-SP-005: Python distributions: wheel/sdist/installed dist-info: METADATA (name, version, requires-dist), RECORD (with digest verification), direct_url.json (PEP 610 vcs_info.commit_id, requested_revision), top

- **Source:** `reva-requirements.md:860-860` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SP-005 | **Python distributions**: wheel/sdist/installed dist-info: `METADATA` (name, version, requires-dist), `RECORD` (with digest verification), `direct_url.json` (PEP 610 `vcs_info.commit_id`, `requested_revision`), `top_level.txt`; virtualenv/site-packages scans. | Fixture venv with a VCS-installed package yields its commit; RECORD mismatch raises an integrity contradiction. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SP-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SP-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture venv with a VCS-installed package yields its commit; RECORD mismatch raises an integrity contradiction
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SP-006 [P1] REVA-SP-006: npm: package.json (name, version, gitHead, repository), package-lock.json v2/v3 packages map (resolved, integrity, dev/optional flags), node_modules/.package-lock.json; integrity verification for tarb

- **Source:** `reva-requirements.md:861-861` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SP-006 | **npm**: `package.json` (`name`, `version`, `gitHead`, `repository`), `package-lock.json` v2/v3 `packages` map (resolved, integrity, dev/optional flags), `node_modules/.package-lock.json`; integrity verification for tarballs present in the inventory. | Fixture app with lockfile v3 yields the full dependency graph; dev dependencies are flagged. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SP-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SP-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture app with lockfile v3 yields the full dependency graph; dev dependencies are flagged
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-TST-001 [P1] REVA-TST-001: Test depth taxonomy mirrors §6.7. Directories: tests/reva/unit, component, integration, acceptance, conformance (per graph backend and per sandbox profile), evaluation, perf. A test's directory must m

- **Source:** `reva-requirements.md:1394-1394` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-TST-001 | Test depth taxonomy mirrors §6.7. Directories: `tests/reva/unit`, `component`, `integration`, `acceptance`, `conformance` (per graph backend and per sandbox profile), `evaluation`, `perf`. A test's directory must match its declared depth marker (`@pytest.mark.reva_depth("unit")`); CI enforces the match.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-TST-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-TST-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] , conformance (per graph backend and per sandbox profile), evaluation, perf. A test's directory must match its declared depth marker (@pytest.mark.revadepth("unit")); CI enforces the match
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-TST-003 [P1] REVA-TST-003: All fixtures are authored for REVA (synthetic) or built in CI from tiny source programs (Go, Rust, Java/Spring Boot, .NET, Python, Node). No third-party application binaries, no REA fixtures. Fixture 

- **Source:** `reva-requirements.md:1396-1396` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-TST-003 | All fixtures are authored for REVA (synthetic) or built in CI from tiny source programs (Go, Rust, Java/Spring Boot, .NET, Python, Node). No third-party application binaries, no REA fixtures. Fixture build scripts live in `tests/reva/fixtures/build/` with pinned toolchain images.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-TST-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-TST-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-TST-003 | All fixtures are authored for REVA (synthetic) or built in CI from tiny source programs (Go, Rust, Java/Spring Boot, .NET, Python, Node). No third-party application binaries, no REA fixtures. Fixture build scripts live in tests/reva/fixtures/build/ with pinned toolchain images.»
- [ ] All fixtures are authored for REVA (synthetic) or built in CI from tiny source programs (Go, Rust, Java/Spring Boot, .NET, Python, Node). No third-party application binaries, no REA fixtures. Fixture build scripts live in tests/reva/fixtures/build/ with pinned toolchain images.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-UI-001 [P1] REVA-UI-001: Shared components: EpistemicBadge (Observed/Derived/Inferred/Unknown/Unavailable, with colour and icon + text), AuthorityChip, ConfidenceMeter (band + %), CoverageMeter (status, examined/omitted, limi

- **Source:** `reva-requirements.md:1041-1041` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-UI-001 | Shared components: `EpistemicBadge` (Observed/Derived/Inferred/Unknown/Unavailable, with colour **and** icon + text), `AuthorityChip`, `ConfidenceMeter` (band + %), `CoverageMeter` (status, examined/omitted, limits, "Unknown — not proven empty" rule), `WarrantDrawer` (body, envelope, signature status, log inclusion proof verification, links graph), `GapCallout`, `ContradictionBanner`. | Storybook stories plus Playwright visual tests; axe accessibility checks pass. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-UI-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-UI-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-UI-001 | Shared components: EpistemicBadge (Observed/Derived/Inferred/Unknown/Unavailable, with colour and icon + text), AuthorityChip, ConfidenceMeter (band + %), CoverageMeter (status, examined/omitted, limits, "Unknown — not proven empty" rule), WarrantDrawer (body, envelope, signature status, log inclusion proof verification, links graph), GapCallout, ContradictionBann»
- [ ] Shared components: EpistemicBadge (Observed/Derived/Inferred/Unknown/Unavailable, with colour and icon + text), AuthorityChip, ConfidenceMeter (band + %), CoverageMeter (status, examined/omitted, limits, "Unknown — not proven empty" rule), WarrantDrawer (body, envelope, signature status, log inclusion proof verification, links graph), GapCallout, ContradictionBanner.
- [ ] Storybook stories plus Playwright visual tests; axe accessibility checks pass.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-UI-002 [P1] REVA-UI-002: Warrant Explorer: search/filter warrants (subject, predicate, producer, authority, epistemic, time, classification); open WarrantDrawer; verify signature/proof client-side (WebCrypto Ed25519 where ava

- **Source:** `reva-requirements.md:1042-1042` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-UI-002 | **Warrant Explorer**: search/filter warrants (subject, predicate, producer, authority, epistemic, time, classification); open WarrantDrawer; verify signature/proof client-side (WebCrypto Ed25519 where available, else server verify endpoint). | Journey RJ-01 steps. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-UI-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-UI-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-UI-002 | Warrant Explorer: search/filter warrants (subject, predicate, producer, authority, epistemic, time, classification); open WarrantDrawer; verify signature/proof client-side (WebCrypto Ed25519 where available, else server verify endpoint). | Journey RJ-01 steps. | acceptance»
- [ ] Warrant Explorer: search/filter warrants (subject, predicate, producer, authority, epistemic, time, classification); open WarrantDrawer; verify signature/proof client-side (WebCrypto Ed25519 where available, else server verify endpoint).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-UI-007 [P1] REVA-UI-007: Contradiction Center: open conflicts with members side by side (values, authority, valid time), suggested rule outcome, resolve with rationale (human decision), affected items list. · RJ-02. · accepta

- **Source:** `reva-requirements.md:1047-1047` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-UI-007 | **Contradiction Center**: open conflicts with members side by side (values, authority, valid time), suggested rule outcome, resolve with rationale (human decision), affected items list. | RJ-02. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-UI-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-UI-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-UI-007 | Contradiction Center: open conflicts with members side by side (values, authority, valid time), suggested rule outcome, resolve with rationale (human decision), affected items list. | RJ-02. | acceptance»
- [ ] Contradiction Center: open conflicts with members side by side (values, authority, valid time), suggested rule outcome, resolve with rationale (human decision), affected items list.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-UI-008 [P1] REVA-UI-008: Artifact & SBOM Explorer: inventory tree (paged), integrity status, components table, commit linkage (with gap if missing), dirty flag, CycloneDX/SPDX download. · RJ-09. · acceptance

- **Source:** `reva-requirements.md:1048-1048` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-UI-008 | **Artifact & SBOM Explorer**: inventory tree (paged), integrity status, components table, commit linkage (with gap if missing), dirty flag, CycloneDX/SPDX download. | RJ-09. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-UI-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-UI-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-UI-008 | Artifact & SBOM Explorer: inventory tree (paged), integrity status, components table, commit linkage (with gap if missing), dirty flag, CycloneDX/SPDX download. | RJ-09. | acceptance»
- [ ] Artifact & SBOM Explorer: inventory tree (paged), integrity status, components table, commit linkage (with gap if missing), dirty flag, CycloneDX/SPDX download.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-UI-014 [P1] REVA-UI-014: Drift Verification: verdict, check list with authority, evidence links, gaps. · RJ-09. · acceptance

- **Source:** `reva-requirements.md:1054-1054` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-UI-014 | **Drift Verification**: verdict, check list with authority, evidence links, gaps. | RJ-09. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-UI-014' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-UI-014') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-UI-014 | Drift Verification: verdict, check list with authority, evidence links, gaps. | RJ-09. | acceptance»
- [ ] Drift Verification: verdict, check list with authority, evidence links, gaps.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-UI-017 [P1] REVA-UI-017: Doctor & Settings (admin): doctor results with remediation; policies (egress, integrity, budgets, auto-probes, retention, mutation threshold), key management (rotate, revoke, export public keys). · Ad

- **Source:** `reva-requirements.md:1057-1057` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-UI-017 | **Doctor & Settings** (admin): doctor results with remediation; policies (egress, integrity, budgets, auto-probes, retention, mutation threshold), key management (rotate, revoke, export public keys). | Admin journey within RJ-12. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-UI-017' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-UI-017') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-UI-017 | Doctor & Settings (admin): doctor results with remediation; policies (egress, integrity, budgets, auto-probes, retention, mutation threshold), key management (rotate, revoke, export public keys). | Admin journey within RJ-12. | acceptance»
- [ ] Doctor & Settings (admin): doctor results with remediation; policies (egress, integrity, budgets, auto-probes, retention, mutation threshold), key management (rotate, revoke, export public keys).
- [ ] Admin journey within RJ-12.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-VS-010 [P1] REVA-VS-010: Extractor isolation: extractors that parse untrusted bytes (archives, binaries, HAR, logs) run in the unit profile as worker subprocesses with memory limits, so parser crashes or zip bombs cannot affe

- **Source:** `reva-requirements.md:834-834` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-VS-010 | Extractor isolation: extractors that parse untrusted bytes (archives, binaries, HAR, logs) run in the `unit` profile as worker subprocesses with memory limits, so parser crashes or zip bombs cannot affect the API process. | Malicious fixtures (zip bomb, deeply nested JSON, gigantic line) are contained and reported. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-VS-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-VS-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Malicious fixtures (zip bomb, deeply nested JSON, gigantic line) are contained and reported
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-VW-002 [P1] REVA-VW-002: Budgets: every REST/MCP response has a byte budget (REVA_RESPONSE_MAX_BYTES, default 262,144) and an approximate token budget (REVA_RESPONSE_MAX_TOKENS, default 32,000; estimator ceil(utf8_bytes/4)). 

- **Source:** `reva-requirements.md:975-975` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-VW-002 | Budgets: every REST/MCP response has a byte budget (`REVA_RESPONSE_MAX_BYTES`, default 262,144) and an approximate token budget (`REVA_RESPONSE_MAX_TOKENS`, default 32,000; estimator `ceil(utf8_bytes/4)`). Workflows default to `summary` and include a ready-to-call continuation (`{tool\|endpoint, arguments}`) for the next page or facet. Over-budget results are never truncated mid-structure; the full result is retained and referenced. | Over-budget workflow returns summary + continuation; following continuations reconstructs the full result (digest equality). | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-VW-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-VW-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Over-budget workflow returns summary + continuation; following continuations reconstructs the full result (digest equality)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-VW-003 [P1] REVA-VW-003: Continuation tokens are opaque, HMAC-SHA256-signed with a tenant key, bound to (tenant, principal, parent_id, view request, offset) and expire after REVA_CONTINUATION_TTL_S (default 3,600). · A token 

- **Source:** `reva-requirements.md:976-976` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-VW-003 | Continuation tokens are opaque, HMAC-SHA256-signed with a tenant key, bound to `(tenant, principal, parent_id, view request, offset)` and expire after `REVA_CONTINUATION_TTL_S` (default 3,600). | A token used by another principal or after expiry is rejected. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-VW-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-VW-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] A token used by another principal or after expiry is rejected
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RJ-05 [P1] RJ-05: Knowledge-gap workflow. A runtime-only API call (no static source) creates a gap; assign owner; run the connector-sync probe; ingest the missing repo; resolve

- **Source:** `reva-requirements.md:1414-1414` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RJ-05 | **Knowledge-gap workflow.** A runtime-only API call (no static source) creates a gap; assign owner; run the connector-sync probe; ingest the missing repo; resolve. | Gap auto-created once; probe result warrants linked; resolution passes the authority check; revision chain verifies; board ordering by impact is correct.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RJ-05' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RJ-05') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RJ-05 | Knowledge-gap workflow. A runtime-only API call (no static source) creates a gap; assign owner; run the connector-sync probe; ingest the missing repo; resolve. | Gap auto-created once; probe result warrants linked; resolution passes the authority check; revision chain verifies; board ordering by impact is correct.»
- [ ] Knowledge-gap workflow. A runtime-only API call (no static source) creates a gap; assign owner; run the connector-sync probe; ingest the missing repo; resolve.
- [ ] Gap auto-created once; probe result warrants linked; resolution passes the authority check; revision chain verifies; board ordering by impact is correct.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RJ-07 [P1] RJ-07: Permission-aware tracing and revocation. Two users with different Confluence permissions run the same trace; then revoke user 2's access

- **Source:** `reva-requirements.md:1416-1416` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RJ-07 | **Permission-aware tracing and revocation.** Two users with different Confluence permissions run the same trace; then revoke user 2's access. | User 2 never sees restricted nodes and gets `ACL_HIDDEN` counts; after revocation, cached views and continuations stop working for user 2 within 60 s.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RJ-07' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RJ-07') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RJ-07 | Permission-aware tracing and revocation. Two users with different Confluence permissions run the same trace; then revoke user 2's access. | User 2 never sees restricted nodes and gets ACL_HIDDEN counts; after revocation, cached views and continuations stop working for user 2 within 60 s.»
- [ ] Permission-aware tracing and revocation. Two users with different Confluence permissions run the same trace; then revoke user 2's access.
- [ ] User 2 never sees restricted nodes and gets ACL_HIDDEN counts; after revocation, cached views and continuations stop working for user 2 within 60 s.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RJ-08 [P1] RJ-08: Grounded answers and evaluation. Ask template and free-form questions, including an absence question under partial coverage and a prompt-injection document. Run the reference evaluation suite

- **Source:** `reva-requirements.md:1417-1417` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RJ-08 | **Grounded answers and evaluation.** Ask template and free-form questions, including an absence question under partial coverage and a prompt-injection document. Run the reference evaluation suite. | Template answers are deterministic (0 LLM calls); claims are grouped by kind with valid citations; the absence answer says "Unknown — not proven"; injection is ignored and recorded; suite metrics meet REVA-GA-006 thresholds.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RJ-08' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RJ-08') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RJ-08 | Grounded answers and evaluation. Ask template and free-form questions, including an absence question under partial coverage and a prompt-injection document. Run the reference evaluation suite. | Template answers are deterministic (0 LLM calls); claims are grouped by kind with valid citations; the absence answer says "Unknown — not proven"; injection is ignored and recor»
- [ ] Grounded answers and evaluation. Ask template and free-form questions, including an absence question under partial coverage and a prompt-injection document. Run the reference evaluation suite.
- [ ] Template answers are deterministic (0 LLM calls); claims are grouped by kind with valid citations; the absence answer says "Unknown — not proven"; injection is ignored and recorded; suite metrics meet REVA-GA-006 thresholds.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RJ-13 [P1] RJ-13: Native Binary Decompilation, CFG Reconstruction, and Graph Projection. Upload a stripped Linux ELF x8664 binary and Windows PE32+ executable; trigger analysis via POST /api/reva/v1/binaries/analyze; v

- **Source:** `reva-requirements.md:1422-1422` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RJ-13 | **Native Binary Decompilation, CFG Reconstruction, and Graph Projection.** Upload a stripped Linux ELF x86_64 binary and Windows PE32+ executable; trigger analysis via `POST /api/reva/v1/binaries/analyze`; verify extracted `reva_BinaryFunction` and `reva_BasicBlock` vertices; check cyclomatic complexity; inspect decompiled C AST via `GET /api/reva/v1/binaries/{digest}/functions/{offset}/decompiled`; verify string cross-reference warrants (`reva_Resource`) and `reva_CALLS_NATIVE` edges; verify Ed25519 signatures and Merkle inclusion proofs. | All functions and basic blocks match golden CFG; decompiled C pseudocode reproduces control flow structures (if/else, while, switch); signed warrants appear in transparency log; re-projection test preserves exact identities.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RJ-13' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RJ-13') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RJ-13 | Native Binary Decompilation, CFG Reconstruction, and Graph Projection. Upload a stripped Linux ELF x86_64 binary and Windows PE32+ executable; trigger analysis via POST /api/reva/v1/binaries/analyze; verify extracted reva_BinaryFunction and reva_BasicBlock vertices; check cyclomatic complexity; inspect decompiled C AST via GET /api/reva/v1/binaries/{digest}/functions/{o»
- [ ] Native Binary Decompilation, CFG Reconstruction, and Graph Projection. Upload a stripped Linux ELF x86_64 binary and Windows PE32+ executable; trigger analysis via POST /api/reva/v1/binaries/analyze; verify extracted reva_BinaryFunction and reva_BasicBlock vertices; check cyclomatic complexity; inspect decompiled C AST via GET /api/reva/v1/binaries/{digest}/functions/{offset}/decompiled; verify st
- [ ] All functions and basic blocks match golden CFG; decompiled C pseudocode reproduces control flow structures (if/else, while, switch); signed warrants appear in transparency log; re-projection test preserves exact identities.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RJ-14 [P1] RJ-14: Mobile Package (APK/IPA) Component Triage and JNI Bridge Mapping. Upload an Android APK (.apk) and iOS IPA (.ipa) containing both compiled UI components and native .so / Mach-O libraries; run kgf reva

- **Source:** `reva-requirements.md:1423-1423` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RJ-14 | **Mobile Package (APK/IPA) Component Triage and JNI Bridge Mapping.** Upload an Android APK (`.apk`) and iOS IPA (`.ipa`) containing both compiled UI components and native `.so` / Mach-O libraries; run `kgf reva mobile triage`; inspect discovered `reva_MobileComponent` entities (Activities, Services, Receivers), deep links, and declared permissions. Verify cross-layer mapping: Java native method in Dalvik DEX correctly resolves to C function in embedded ARM64 `.so` via `reva_CALLS_NATIVE` edge. | Manifest binary XML and `Info.plist` parsed with zero decompression bomb vulnerability; all exported activities flagged; JNI bridge edge links Android Activity to native decompiler function; signed warrants issued for mobile package topology.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RJ-14' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RJ-14') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RJ-14 | Mobile Package (APK/IPA) Component Triage and JNI Bridge Mapping. Upload an Android APK (.apk) and iOS IPA (.ipa) containing both compiled UI components and native .so / Mach-O libraries; run kgf reva mobile triage; inspect discovered reva_MobileComponent entities (Activities, Services, Receivers), deep links, and declared permissions. Verify cross-layer mapping: Java n»
- [ ] Mobile Package (APK/IPA) Component Triage and JNI Bridge Mapping. Upload an Android APK (.apk) and iOS IPA (.ipa) containing both compiled UI components and native .so / Mach-O libraries; run kgf reva mobile triage; inspect discovered reva_MobileComponent entities (Activities, Services, Receivers), deep links, and declared permissions. Verify cross-layer mapping: Java native method in Dalvik DEX c
- [ ] Manifest binary XML and Info.plist parsed with zero decompression bomb vulnerability; all exported activities flagged; JNI bridge edge links Android Activity to native decompiler function; signed warrants issued for mobile package topology.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-C-05 [P2] C-05: Epistemic separation. Observed, derived, inferred, predicted and human-approved facts stay distinct end to end (storage, API, UI, LLM context)

- **Source:** `reva-requirements.md:275-275` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
C-05 | **Epistemic separation.** Observed, derived, inferred, predicted and human-approved facts stay distinct end to end (storage, API, UI, LLM context).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'C-05' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('C-05') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «C-05 | Epistemic separation. Observed, derived, inferred, predicted and human-approved facts stay distinct end to end (storage, API, UI, LLM context).»
- [ ] Epistemic separation. Observed, derived, inferred, predicted and human-approved facts stay distinct end to end (storage, API, UI, LLM context).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-C-08 [P2] C-08: White-label. All user-visible strings are localizable resources; product name, logo and colours come from tenant branding configuration

- **Source:** `reva-requirements.md:278-278` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
C-08 | **White-label.** All user-visible strings are localizable resources; product name, logo and colours come from tenant branding configuration.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'C-08' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('C-08') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «C-08 | White-label. All user-visible strings are localizable resources; product name, logo and colours come from tenant branding configuration.»
- [ ] White-label. All user-visible strings are localizable resources; product name, logo and colours come from tenant branding configuration.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-C-09 [P2] C-09: Single node first. All of REVA runs on one node via Docker Compose; scale-out is optional

- **Source:** `reva-requirements.md:279-279` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
C-09 | **Single node first.** All of REVA runs on one node via Docker Compose; scale-out is optional.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'C-09' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('C-09') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «C-09 | Single node first. All of REVA runs on one node via Docker Compose; scale-out is optional.»
- [ ] Single node first. All of REVA runs on one node via Docker Compose; scale-out is optional.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-C-10 [P2] C-10: Preserve working functionality. REVA is additive. Changes to existing KGF modules are limited to the integration points in §5.4, each behind a feature flag defaulting to the pre-REVA behaviour until e

- **Source:** `reva-requirements.md:280-280` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
C-10 | **Preserve working functionality.** REVA is additive. Changes to existing KGF modules are limited to the integration points in §5.4, each behind a feature flag defaulting to the pre-REVA behaviour until enabled.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'C-10' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('C-10') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «C-10 | Preserve working functionality. REVA is additive. Changes to existing KGF modules are limited to the integration points in §5.4, each behind a feature flag defaulting to the pre-REVA behaviour until enabled.»
- [ ] Preserve working functionality. REVA is additive. Changes to existing KGF modules are limited to the integration points in §5.4, each behind a feature flag defaulting to the pre-REVA behaviour until enabled.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-02 [P2] RC-02: Evidence bundles (deterministic manifests of artifacts, providers, environments, scenarios, captures, unknowns, records; canonical ordering; duplicate rejection; target filtering)

- **Source:** `reva-requirements.md:114-114` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-02; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-02 | Evidence bundles (deterministic manifests of artifacts, providers, environments, scenarios, captures, unknowns, records; canonical ordering; duplicate rejection; target filtering) | `src/domain/evidenceBundle.ts`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-02' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-02') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-02

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-02 | Evidence bundles (deterministic manifests of artifacts, providers, environments, scenarios, captures, unknowns, records; canonical ordering; duplicate rejection; target filtering) | src/domain/evidenceBundle.ts»
- [ ] Evidence bundles (deterministic manifests of artifacts, providers, environments, scenarios, captures, unknowns, records; canonical ordering; duplicate rejection; target filtering)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-03 [P2] RC-03: Relationship coverage (complete / partial / unknown; empty set ≠ no relationships)

- **Source:** `reva-requirements.md:115-115` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-03; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-03 | Relationship coverage (`complete` / `partial` / `unknown`; empty set ≠ no relationships) | `src/domain/relationshipCoverage.ts`, `docs/mcp-contracts.md`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-03' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-03') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-03

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-03 | Relationship coverage (complete / partial / unknown; empty set ≠ no relationships) | src/domain/relationshipCoverage.ts, docs/mcp-contracts.md»
- [ ] Relationship coverage (complete / partial / unknown; empty set ≠ no relationships)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-07 [P2] RC-07: Readiness conformance (9 stages, fail-closed aggregation: fail/unknown/unsupported/truncated/skipped never become pass)

- **Source:** `reva-requirements.md:119-119` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-07; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-07 | Readiness conformance (9 stages, fail-closed aggregation: fail/unknown/unsupported/truncated/skipped never become pass) | `docs/reconstruction-readiness.md`, `src/domain/reconstructionReadiness*.ts`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-07' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-07') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-07

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-07 | Readiness conformance (9 stages, fail-closed aggregation: fail/unknown/unsupported/truncated/skipped never become pass) | docs/reconstruction-readiness.md, src/domain/reconstructionReadiness*.ts»
- [ ] Readiness conformance (9 stages, fail-closed aggregation: fail/unknown/unsupported/truncated/skipped never become pass)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-08 [P2] RC-08: Completion ledger and verifier report with process lineage (run ID, PIDs, process group, descendants)

- **Source:** `reva-requirements.md:120-120` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-08; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-08 | Completion ledger and verifier report with process lineage (run ID, PIDs, process group, descendants) | `src/domain/evidenceCompletionLedger.ts`, `src/domain/completionLedgerGeneration.ts`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-08' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-08') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-08

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-08 | Completion ledger and verifier report with process lineage (run ID, PIDs, process group, descendants) | src/domain/evidenceCompletionLedger.ts, src/domain/completionLedgerGeneration.ts»
- [ ] Completion ledger and verifier report with process lineage (run ID, PIDs, process group, descendants)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-09 [P2] RC-09: Conformance trust gate (per-dimension match/mismatch/unknown/truncated, volatile dimensions ignored, first divergence)

- **Source:** `reva-requirements.md:121-121` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-09; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-09 | Conformance trust gate (per-dimension match/mismatch/unknown/truncated, volatile dimensions ignored, first divergence) | `src/domain/conformanceTrustGate.ts`, `conformancePackage.ts`, `conformanceReplay.ts`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-09' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-09') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-09

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-09 | Conformance trust gate (per-dimension match/mismatch/unknown/truncated, volatile dimensions ignored, first divergence) | src/domain/conformanceTrustGate.ts, conformancePackage.ts, conformanceReplay.ts»
- [ ] Conformance trust gate (per-dimension match/mismatch/unknown/truncated, volatile dimensions ignored, first divergence)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-11 [P2] RC-11: JavaScript/Electron static reconstruction (directory/ASAR, BrowserWindow, preload, contextBridge, IPC pairing, utility processes, native bindings, endpoints incl. partial templates, GraphQL/tRPC opera

- **Source:** `reva-requirements.md:123-123` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-11; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-11 | JavaScript/Electron static reconstruction (directory/ASAR, BrowserWindow, preload, contextBridge, IPC pairing, utility processes, native bindings, endpoints incl. partial templates, GraphQL/tRPC operations, source maps) | `src/application/javascript/*`, `src/domain/javascript/*`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-11' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-11') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-11

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-11 | JavaScript/Electron static reconstruction (directory/ASAR, BrowserWindow, preload, contextBridge, IPC pairing, utility processes, native bindings, endpoints incl. partial templates, GraphQL/tRPC operations, source maps) | src/application/javascript/, src/domain/javascript/»
- [ ] JavaScript/Electron static reconstruction (directory/ASAR, BrowserWindow, preload, contextBridge, IPC pairing, utility processes, native bindings, endpoints incl. partial templates, GraphQL/tRPC operations, source maps)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-13 [P2] RC-13: Application version comparison (tiered matching: exact identity → content digest → module source digest → source-map identity → structural fingerprint → semantic key; ambiguous kept with candidates) a

- **Source:** `reva-requirements.md:125-125` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-13; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-13 | Application version comparison (tiered matching: exact identity → content digest → module source digest → source-map identity → structural fingerprint → semantic key; ambiguous kept with candidates) and change graph (`changed_from`) | `src/domain/javascript/javascriptApplicationVersion*.ts`, `javascriptApplicationChangeGraph.ts`, `javascriptAstFingerprint.ts`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-13' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-13') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-13

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-13 | Application version comparison (tiered matching: exact identity → content digest → module source digest → source-map identity → structural fingerprint → semantic key; ambiguous kept with candidates) and change graph (changed_from) | src/domain/javascript/javascriptApplicationVersion*.ts, javascriptApplicationChangeGraph.ts, javascriptAstFingerprint.ts»
- [ ] Application version comparison (tiered matching: exact identity → content digest → module source digest → source-map identity → structural fingerprint → semantic key; ambiguous kept with candidates) and change graph (changed_from)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-14 [P2] RC-14: Static/runtime reconciliation (observedas edges as cross-layer inference linking static and runtime evidence)

- **Source:** `reva-requirements.md:126-126` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-14; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-14 | Static/runtime reconciliation (`observed_as` edges as cross-layer inference linking static and runtime evidence) | `docs/javascript-runtime-reconciliation.md`, `src/domain/javascript/javascriptRuntimeReconciliation.ts`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-14' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-14') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-14

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-14 | Static/runtime reconciliation (observed_as edges as cross-layer inference linking static and runtime evidence) | docs/javascript-runtime-reconciliation.md, src/domain/javascript/javascriptRuntimeReconciliation.ts»
- [ ] Static/runtime reconciliation (observed_as edges as cross-layer inference linking static and runtime evidence)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-15 [P2] RC-15: Source-to-bundle comparison (historical source tree vs shipped bundle) and reference-source import

- **Source:** `reva-requirements.md:127-127` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-15; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-15 | Source-to-bundle comparison (historical source tree vs shipped bundle) and reference-source import | `src/server/registerApplicationTools/compareSourceToBundle.ts`, `src/domain/referenceSource*.ts`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-15' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-15') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-15

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-15 | Source-to-bundle comparison (historical source tree vs shipped bundle) and reference-source import | src/server/registerApplicationTools/compareSourceToBundle.ts, src/domain/referenceSource*.ts»
- [ ] Source-to-bundle comparison (historical source tree vs shipped bundle) and reference-source import
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-17 [P2] RC-17: SQLite schema and row-sample inspection (DB + WAL identity)

- **Source:** `reva-requirements.md:129-129` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-17; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-17 | SQLite schema and row-sample inspection (DB + WAL identity) | `src/domain/sqlite/sqliteDatabase.ts`, `docs/sqlite-databases.md`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-17' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-17') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-17

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-17 | SQLite schema and row-sample inspection (DB + WAL identity) | src/domain/sqlite/sqliteDatabase.ts, docs/sqlite-databases.md»
- [ ] SQLite schema and row-sample inspection (DB + WAL identity)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-18 [P2] RC-18: Embedded build metadata: Go buildinfo (modules, settings), Rust cargo-auditable dependency list, .NET PE/CLI metadata, Flutter build identity

- **Source:** `reva-requirements.md:130-130` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-18; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-18 | Embedded build metadata: Go buildinfo (modules, settings), Rust cargo-auditable dependency list, .NET PE/CLI metadata, Flutter build identity | `src/go/*`, `src/rust/*`, `src/dotnet/*`, `src/flutter/*`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-18' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-18') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-18

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-18 | Embedded build metadata: Go buildinfo (modules, settings), Rust cargo-auditable dependency list, .NET PE/CLI metadata, Flutter build identity | src/go/, src/rust/, src/dotnet/, src/flutter/»
- [ ] Embedded build metadata: Go buildinfo (modules, settings), Rust cargo-auditable dependency list, .NET PE/CLI metadata, Flutter build identity
- [ ] src/go/, src/rust/, src/dotnet/, src/flutter/
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-20 [P2] RC-20: Analysis views and paging over retained evidence (summary/facet/item/page; coverage with nextoffset; view digest bound to parent evidence)

- **Source:** `reva-requirements.md:132-132` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-RC-20; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-20 | Analysis views and paging over retained evidence (summary/facet/item/page; coverage with `next_offset`; view digest bound to parent evidence) | `src/domain/analysisView/*`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-20' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-20') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-20

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-20 | Analysis views and paging over retained evidence (summary/facet/item/page; coverage with next_offset; view digest bound to parent evidence) | src/domain/analysisView/*»
- [ ] Analysis views and paging over retained evidence (summary/facet/item/page; coverage with next_offset; view digest bound to parent evidence)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-21 [P2] RC-21: MCP response budget (10 MiB), oversized-result retention with continuation, summary-mode bundle discovery, filters

- **Source:** `reva-requirements.md:133-133` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-RC-21; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-21 | MCP response budget (10 MiB), oversized-result retention with continuation, summary-mode bundle discovery, filters | `src/config/mcpResponseBudget.ts`, `docs/mcp-contracts.md`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-21' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-21') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-21

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-21 | MCP response budget (10 MiB), oversized-result retention with continuation, summary-mode bundle discovery, filters | src/config/mcpResponseBudget.ts, docs/mcp-contracts.md»
- [ ] MCP response budget (10 MiB), oversized-result retention with continuation, summary-mode bundle discovery, filters
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-22 [P2] RC-22: MCP tool design discipline (inspect/search/trace/compare/workflow/observe shapes; strict schemas; truthful effects; lifecycle ownership; cancellation semantics)

- **Source:** `reva-requirements.md:134-134` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-RC-22; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-22 | MCP tool design discipline (inspect/search/trace/compare/workflow/observe shapes; strict schemas; truthful effects; lifecycle ownership; cancellation semantics) | `docs/tool-design.md`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-22' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-22') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-22

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-22 | MCP tool design discipline (inspect/search/trace/compare/workflow/observe shapes; strict schemas; truthful effects; lifecycle ownership; cancellation semantics) | docs/tool-design.md»
- [ ] MCP tool design discipline (inspect/search/trace/compare/workflow/observe shapes; strict schemas; truthful effects; lifecycle ownership; cancellation semantics)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-23 [P2] RC-23: Error contract (typed codes, categories, retryable flag, remediation, partial observations; user-visible error catalog with harm ranking)

- **Source:** `reva-requirements.md:135-135` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-RC-23; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-23 | Error contract (typed codes, categories, retryable flag, remediation, partial observations; user-visible error catalog with harm ranking) | `docs/error-contract.schema.json`, `docs/user-visible-errors.csv`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-23' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-23') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-23

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-23 | Error contract (typed codes, categories, retryable flag, remediation, partial observations; user-visible error catalog with harm ranking) | docs/error-contract.schema.json, docs/user-visible-errors.csv»
- [ ] Error contract (typed codes, categories, retryable flag, remediation, partial observations; user-visible error catalog with harm ranking)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-25 [P2] RC-25: Guided prompts with evidence discipline (Observation / Inference / Unknown; absence ≠ equivalence)

- **Source:** `reva-requirements.md:137-137` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-25; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-25 | Guided prompts with evidence discipline (Observation / Inference / Unknown; absence ≠ equivalence) | `src/contracts/promptContracts.ts`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-25' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-25') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-25

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-25 | Guided prompts with evidence discipline (Observation / Inference / Unknown; absence ≠ equivalence) | src/contracts/promptContracts.ts»
- [ ] Guided prompts with evidence discipline (Observation / Inference / Unknown; absence ≠ equivalence)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-27 [P2] RC-27: Owned process supervision (process groups, deadlines, bounded stdout/stderr, Linux prlimit AS/FSIZE/CPU/core, private runtime roots, cleanup retention)

- **Source:** `reva-requirements.md:139-139` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-27; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-27 | Owned process supervision (process groups, deadlines, bounded stdout/stderr, Linux prlimit AS/FSIZE/CPU/core, private runtime roots, cleanup retention) | `src/process/*`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-27' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-27') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-27

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-27 | Owned process supervision (process groups, deadlines, bounded stdout/stderr, Linux prlimit AS/FSIZE/CPU/core, private runtime roots, cleanup retention) | src/process/*»
- [ ] Owned process supervision (process groups, deadlines, bounded stdout/stderr, Linux prlimit AS/FSIZE/CPU/core, private runtime roots, cleanup retention)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

