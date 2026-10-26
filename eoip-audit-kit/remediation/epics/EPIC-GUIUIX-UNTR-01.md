# EPIC-GUIUIX-UNTR-01: GUI-UIX-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 60 tasks, ~447.5 h, priorities {'P0': 27, 'P1': 33}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-BACKEND-MISSING-005 [P0] BACKEND-MISSING-005: GET /api/v1/brain/answers/{id}/events · Authenticated SSE stream for tokens/evidence/status with Last-Event-ID and cancel. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for

- **Source:** `GUI-UIX-requirements.md:1264-1264` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-005` | `GET /api/v1/brain/answers/{id}/events` | Authenticated SSE stream for tokens/evidence/status with Last-Event-ID and cancel. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-004
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-005 | GET /api/v1/brain/answers/{id}/events | Authenticated SSE stream for tokens/evidence/status with Last-Event-ID and cancel. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-004»
- [ ] Authenticated SSE stream for tokens/evidence/status with Last-Event-ID and cancel. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-014 [P0] BACKEND-MISSING-014: GET /api/v1/agents/runs/{id}/events · Authenticated run trace/approval SSE with sequence, redaction and resume. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation a

- **Source:** `GUI-UIX-requirements.md:1273-1273` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-014` | `GET /api/v1/agents/runs/{id}/events` | Authenticated run trace/approval SSE with sequence, redaction and resume. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-018
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-014' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-014') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-014 | GET /api/v1/agents/runs/{id}/events | Authenticated run trace/approval SSE with sequence, redaction and resume. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-018»
- [ ] Authenticated run trace/approval SSE with sequence, redaction and resume. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-001 [P0] SCR-001: Authentication and tenant entry

- **Source:** `GUI-UIX-requirements.md:126-138` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-001 - Authentication and tenant entry

- **Route / personas / purpose:** `/auth/*`; All users; Establish identity, MFA, session and tenant context.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-049`, `INT-050`, `INT-051`, `INT-052`, `INT-053`, `INT-054`, `INT-055`, `INT-056`, `BACKEND-MISSING-001`, `BACKEND-MISSING-002`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_001.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. G
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-001

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-002 [P0] SCR-002: First-run onboarding

- **Source:** `GUI-UIX-requirements.md:139-151` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-002 - First-run onboarding

- **Route / personas / purpose:** `/t/:tenant/onboarding`; Tenant admin, data engineer; Configure workspace, source, ingestion review and first question.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-009`, `INT-010`, `INT-011`, `INT-012`, `INT-013`, `INT-014`, `INT-015`, `INT-016`, `BACKEND-MISSING-003`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_002.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader 
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-002

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-003 [P0] SCR-003: Brain overview

- **Source:** `GUI-UIX-requirements.md:152-164` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-003 - Brain overview

- **Route / personas / purpose:** `/t/:tenant/w/:workspace`; All users; Summarize graph health, changes, jobs, alerts and saved work.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-020`, `INT-021`, `INT-022`, `INT-023`, `INT-049`, `INT-161`, `INT-162`, `INT-163`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_003.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or 
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-003

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: IMPLEMENTED-UNVERIFIED. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-004 [P0] SCR-004: Ask the Brain

- **Source:** `GUI-UIX-requirements.md:165-177` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-004 - Ask the Brain

- **Route / personas / purpose:** `/t/:tenant/w/:workspace/ask`; Executive, analyst; Ask, compare deterministic suggestions, inspect evidence and export.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-039`, `INT-061`, `INT-062`, `INT-063`, `INT-064`, `INT-065`, `INT-066`, `INT-067`, `BACKEND-MISSING-005`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_004.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operabl
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-004

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-005 [P0] SCR-005: Graph Explorer

- **Source:** `GUI-UIX-requirements.md:178-190` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-005 - Graph Explorer

- **Route / personas / purpose:** `/t/:tenant/w/:workspace/graph`; Analyst, engineer, steward; Explore, filter, path-find, cluster and save ontology-driven graphs.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-178`, `INT-216`, `INT-232`, `INT-252`, `INT-253`, `INT-254`, `INT-255`, `INT-256`, `BACKEND-MISSING-004`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_005.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-rea
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-005

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-006 [P0] SCR-006: Entity 360

- **Source:** `GUI-UIX-requirements.md:191-203` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-006 - Entity 360

- **Route / personas / purpose:** `/t/:tenant/w/:workspace/entity/:id`; All knowledge users; Inspect properties, relations, provenance, timeline and work.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-005`, `INT-100`, `INT-102`, `INT-180`, `INT-226`, `INT-289`, `INT-290`, `INT-291`, `BACKEND-MISSING-006`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_006.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable.
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-006

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-007 [P0] SCR-007: Impact Analysis studio

- **Source:** `GUI-UIX-requirements.md:204-216` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-007 - Impact Analysis studio

- **Route / personas / purpose:** `/t/:tenant/w/:workspace/impact`; Engineer, analyst; Model a change, inspect blast radius and produce a test checklist.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-044`, `INT-105`, `INT-252`, `INT-262`, `INT-277`, `INT-278`, `INT-280`, `INT-292`, `BACKEND-MISSING-007`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_007.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reade
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-007

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-008 [P0] SCR-008: Change history

- **Source:** `GUI-UIX-requirements.md:217-229` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-008; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-008 - Change history

- **Route / personas / purpose:** `/t/:tenant/w/:workspace/changes`; Engineer, compliance; Trace who changed what and compare versions.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-107`, `INT-114`, `INT-115`, `INT-116`, `INT-129`, `INT-178`, `INT-179`, `INT-180`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_008.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes o
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-008

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: IMPLEMENTED-UNVERIFIED. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-009 [P0] SCR-009: Incident root-cause workspace

- **Source:** `GUI-UIX-requirements.md:230-242` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-009; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-009 - Incident root-cause workspace

- **Route / personas / purpose:** `/t/:tenant/w/:workspace/incidents/:id`; IT user, responder; Rank causes and walk evidence-backed troubleshooting paths.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-104`, `INT-175`, `INT-242`, `INT-439`, `INT-440`, `INT-441`, `INT-442`, `INT-443`, `BACKEND-MISSING-008`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_009.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and scre
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-009

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-011 [P0] SCR-011: Query Workbench

- **Source:** `GUI-UIX-requirements.md:256-268` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-011; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-011 - Query Workbench

- **Route / personas / purpose:** `/t/:tenant/w/:workspace/query`; Analyst, data engineer; Author, validate, explain, run and save polyglot queries.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-008`, `INT-039`, `INT-062`, `INT-067`, `INT-081`, `INT-167`, `INT-230`, `INT-326`, `BACKEND-MISSING-009`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_011.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. 
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-011

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-012 [P0] SCR-012: Ontology Designer

- **Source:** `GUI-UIX-requirements.md:269-281` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-012; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-012 - Ontology Designer

- **Route / personas / purpose:** `/t/:tenant/w/:workspace/ontology`; Ontology steward; Edit, validate, diff, approve and publish schema.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-024`, `INT-066`, `INT-204`, `INT-279`, `INT-345`, `INT-346`, `INT-347`, `INT-348`, `BACKEND-MISSING-010`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_012.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a m
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-012

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-013 [P0] SCR-013: Meta-graph

- **Source:** `GUI-UIX-requirements.md:282-294` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-013; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-013 - Meta-graph

- **Route / personas / purpose:** `/t/:tenant/w/:workspace/meta-graph`; Steward, analyst; Explore type relationships and instance counts.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-066`, `INT-345`, `INT-346`, `INT-347`, `INT-348`, `INT-349`, `INT-350`, `INT-351`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_013.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or 
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-013

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: IMPLEMENTED-UNVERIFIED. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-014 [P0] SCR-014: Sources and connectors

- **Source:** `GUI-UIX-requirements.md:295-307` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-014; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-014 - Sources and connectors

- **Route / personas / purpose:** `/t/:tenant/w/:workspace/sources`; Integration engineer; Configure, test and monitor source connections.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-142`, `INT-143`, `INT-231`, `INT-444`, `INT-446`, `INT-447`, `INT-448`, `INT-620`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_014.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it 
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-014' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-014') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-014

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: IMPLEMENTED-UNVERIFIED. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-015 [P0] SCR-015: Ingestion and Mapping studio

- **Source:** `GUI-UIX-requirements.md:308-320` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-015; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-015 - Ingestion and Mapping studio

- **Route / personas / purpose:** `/t/:tenant/w/:workspace/ingestion`; Data engineer, steward; Infer, review, map, dry-run and publish source data.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-009`, `INT-010`, `INT-011`, `INT-012`, `INT-013`, `INT-014`, `INT-015`, `INT-016`, `BACKEND-MISSING-011`, `BACKEND-MISSING-012`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_015.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is ke
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-015' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-015') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-015

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-016 [P0] SCR-016: Entity resolution and quality

- **Source:** `GUI-UIX-requirements.md:321-333` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-016; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-016 - Entity resolution and quality

- **Route / personas / purpose:** `/t/:tenant/w/:workspace/quality`; Data steward; Resolve duplicates and manage quality issues/rules.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-388`, `INT-414`, `BACKEND-MISSING-013`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_016.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit fe
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-016' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-016') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-016

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-017 [P0] SCR-017: Pipelines and Jobs

- **Source:** `GUI-UIX-requirements.md:334-346` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-017; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-017 - Pipelines and Jobs

- **Route / personas / purpose:** `/t/:tenant/w/:workspace/jobs`; Data engineer, operator; Monitor throughput, logs, retries, cancellation and reruns.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-020`, `INT-021`, `INT-022`, `INT-023`, `INT-025`, `INT-026`, `INT-374`, `INT-433`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_017.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, 
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-017' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-017') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-017

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: IMPLEMENTED-UNVERIFIED. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-018 [P0] SCR-018: Agents

- **Source:** `GUI-UIX-requirements.md:347-359` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-018; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-018 - Agents

- **Route / personas / purpose:** `/t/:tenant/w/:workspace/agents`; Analyst, admin; Configure agents, inspect traces and approve actions.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-032`, `INT-033`, `INT-034`, `INT-035`, `INT-036`, `INT-037`, `INT-038`, `INT-039`, `BACKEND-MISSING-014`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_018.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, wh
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-018' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-018') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-018

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-019 [P0] SCR-019: Reports and dashboards

- **Source:** `GUI-UIX-requirements.md:360-372` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-019; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-019 - Reports and dashboards

- **Route / personas / purpose:** `/t/:tenant/w/:workspace/reports`; Executive, analyst; Build, schedule, share and export governed reports.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-057`, `INT-060`, `INT-081`, `INT-099`, `INT-132`, `INT-159`, `INT-163`, `INT-194`, `BACKEND-MISSING-015`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_019.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. G
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-019' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-019') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-019

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-021 [P0] SCR-021: Governance and security

- **Source:** `GUI-UIX-requirements.md:386-398` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-021; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-021 - Governance and security

- **Route / personas / purpose:** `/t/:tenant/admin/governance`; Security officer; Manage access, classifications, model egress and audit.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-001`, `INT-051`, `INT-052`, `INT-053`, `INT-054`, `INT-055`, `INT-056`, `INT-057`, `BACKEND-MISSING-017`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_021.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Gi
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-021' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-021') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-021

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-022 [P0] SCR-022: Tenant administration

- **Source:** `GUI-UIX-requirements.md:399-411` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-022; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-022 - Tenant administration

- **Route / personas / purpose:** `/platform/tenants/:tenant`; Tenant/platform admin; Manage lifecycle, quotas, storage, licences and backups.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-188`, `INT-678`, `INT-679`, `INT-680`, `INT-681`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_022.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-022' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-022') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-022

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: IMPLEMENTED-UNVERIFIED. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-023 [P0] SCR-023: White-label studio

- **Source:** `GUI-UIX-requirements.md:412-424` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-023; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-023 - White-label studio

- **Route / personas / purpose:** `/t/:tenant/admin/brand`; Partner, tenant admin; Edit and safely publish a tenant brand pack.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-085`, `INT-086`, `INT-087`, `INT-088`, `INT-089`, `BACKEND-MISSING-018`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_023.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then 
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-023' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-023') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-023

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-024 [P0] SCR-024: Platform health

- **Source:** `GUI-UIX-requirements.md:425-437` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-024; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-024 - Platform health

- **Route / personas / purpose:** `/platform/health`; Platform admin, operator; Inspect services, queues, stores, models and nodes.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-049`, `INT-161`, `INT-162`, `INT-163`, `INT-164`, `INT-165`, `INT-166`, `INT-190`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_024.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or f
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-024' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-024') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-024

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: IMPLEMENTED-UNVERIFIED. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-025 [P0] SCR-025: User settings

- **Source:** `GUI-UIX-requirements.md:438-450` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-025; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-025 - User settings

- **Route / personas / purpose:** `/settings`; All users; Manage profile, appearance, locale, shortcuts and tokens.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-058`, `INT-059`, `INT-060`, `INT-078`, `INT-236`, `INT-293`, `INT-294`, `INT-295`, `BACKEND-MISSING-019`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_025.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-025' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-025') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-025

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-026 [P0] SCR-026: Notifications, help and licences

- **Source:** `GUI-UIX-requirements.md:451-463` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-026; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-026 - Notifications, help and licences

- **Route / personas / purpose:** `/notifications`; All users; Review events, help, shortcuts and legal notices.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-312`, `INT-313`, `INT-314`, `INT-315`, `INT-316`, `INT-317`, `INT-468`, `INT-469`, `BACKEND-MISSING-020`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_026.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, w
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-026' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-026') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-026

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-027 [P0] SCR-027: Global errors

- **Source:** `GUI-UIX-requirements.md:464-477` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-SCR-027; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-027 - Global errors

- **Route / personas / purpose:** `/errors/:code`; All users; Recover from forbidden, missing, failed, offline and mismatched states.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-049`, `INT-190`, `INT-191`, `INT-192`, `INT-193`, `INT-194`, `INT-195`, `INT-196`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_027.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or f
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SCR-027' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SCR-027') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-SCR-027

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: IMPLEMENTED-UNVERIFIED. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-001 [P1] BACKEND-MISSING-001: POST /api/v1/session/exchange · OIDC/SAML/local credential exchange -> secure session + principal + allowed tenants; emits session.expiring/revoked. Standard RFC 7807 errors, principal-derived tenant,

- **Source:** `GUI-UIX-requirements.md:1260-1260` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-001` | `POST /api/v1/session/exchange` | OIDC/SAML/local credential exchange -> secure session + principal + allowed tenants; emits session.expiring/revoked. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-001
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-001 | POST /api/v1/session/exchange | OIDC/SAML/local credential exchange -> secure session + principal + allowed tenants; emits session.expiring/revoked. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-001»
- [ ] OIDC/SAML/local credential exchange -> secure session + principal + allowed tenants; emits session.expiring/revoked. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-002 [P1] BACKEND-MISSING-002: GET /api/v1/me · Current principal, roles, effective permissions, tenant/workspace grants and preferences. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and au

- **Source:** `GUI-UIX-requirements.md:1261-1261` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-002` | `GET /api/v1/me` | Current principal, roles, effective permissions, tenant/workspace grants and preferences. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-001
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-002 | GET /api/v1/me | Current principal, roles, effective permissions, tenant/workspace grants and preferences. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-001»
- [ ] Current principal, roles, effective permissions, tenant/workspace grants and preferences. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-003 [P1] BACKEND-MISSING-003: GET/PUT /api/v1/onboarding · Durable per-tenant onboarding state, completed steps and resumable wizard draft. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and

- **Source:** `GUI-UIX-requirements.md:1262-1262` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-003` | `GET/PUT /api/v1/onboarding` | Durable per-tenant onboarding state, completed steps and resumable wizard draft. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-002
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-003 | GET/PUT /api/v1/onboarding | Durable per-tenant onboarding state, completed steps and resumable wizard draft. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-002»
- [ ] Durable per-tenant onboarding state, completed steps and resumable wizard draft. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-004 [P1] BACKEND-MISSING-004: POST /api/v1/workspaces/{w}/graph/views · Persist viewport, layout, filters, pins, lens and ACL with optimistic version. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for m

- **Source:** `GUI-UIX-requirements.md:1263-1263` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-004` | `POST /api/v1/workspaces/{w}/graph/views` | Persist viewport, layout, filters, pins, lens and ACL with optimistic version. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-005
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-004 | POST /api/v1/workspaces/{w}/graph/views | Persist viewport, layout, filters, pins, lens and ACL with optimistic version. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-005»
- [ ] Persist viewport, layout, filters, pins, lens and ACL with optimistic version. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-006 [P1] BACKEND-MISSING-006: GET /api/v1/entities/{id}/360 · Tenant-scoped aggregate of properties, grouped relations, provenance, timeline and issues. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for

- **Source:** `GUI-UIX-requirements.md:1265-1265` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-006` | `GET /api/v1/entities/{id}/360` | Tenant-scoped aggregate of properties, grouped relations, provenance, timeline and issues. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-006
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-006 | GET /api/v1/entities/{id}/360 | Tenant-scoped aggregate of properties, grouped relations, provenance, timeline and issues. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-006»
- [ ] Tenant-scoped aggregate of properties, grouped relations, provenance, timeline and issues. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-007 [P1] BACKEND-MISSING-007: POST /api/v1/impact/plans · Persist proposed change, blast radius, severity and generated test checklist; export job link. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for

- **Source:** `GUI-UIX-requirements.md:1266-1266` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-007` | `POST /api/v1/impact/plans` | Persist proposed change, blast radius, severity and generated test checklist; export job link. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-007
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-007 | POST /api/v1/impact/plans | Persist proposed change, blast radius, severity and generated test checklist; export job link. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-007»
- [ ] Persist proposed change, blast radius, severity and generated test checklist; export job link. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-008 [P1] BACKEND-MISSING-008: POST /api/v1/incidents/{id}/workspaces · Durable RCA candidates, evidence, troubleshooting steps, comments and decisions. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for 

- **Source:** `GUI-UIX-requirements.md:1267-1267` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-008` | `POST /api/v1/incidents/{id}/workspaces` | Durable RCA candidates, evidence, troubleshooting steps, comments and decisions. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-009
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-008 | POST /api/v1/incidents/{id}/workspaces | Durable RCA candidates, evidence, troubleshooting steps, comments and decisions. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-009»
- [ ] Durable RCA candidates, evidence, troubleshooting steps, comments and decisions. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-009 [P1] BACKEND-MISSING-009: `POST /api/v1/query/validate · explain · profile

- **Source:** `GUI-UIX-requirements.md:1268-1268` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-009` | `POST /api/v1/query/validate | explain | profile | cancel` | Uniform polyglot query lifecycle with cost guard, cancellation and typed result frames. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-011
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-009 | `POST /api/v1/query/validate | explain | profile | cancel` | Uniform polyglot query lifecycle with cost guard, cancellation and typed result frames. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-011»
- [ ] Uniform polyglot query lifecycle with cost guard, cancellation and typed result frames. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-010 [P1] BACKEND-MISSING-010: POST /api/v1/ontology/drafts/{id}/publish · Draft/diff/validation/approval/migration plan with publish and rollback events. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency fo

- **Source:** `GUI-UIX-requirements.md:1269-1269` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-010` | `POST /api/v1/ontology/drafts/{id}/publish` | Draft/diff/validation/approval/migration plan with publish and rollback events. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-012
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-010 | POST /api/v1/ontology/drafts/{id}/publish | Draft/diff/validation/approval/migration plan with publish and rollback events. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-012»
- [ ] Draft/diff/validation/approval/migration plan with publish and rollback events. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-011 [P1] BACKEND-MISSING-011: POST/PATCH /api/v1/uploads · Chunked resumable upload with checksum, offset, expiry, scan status and abort. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and a

- **Source:** `GUI-UIX-requirements.md:1270-1270` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-011` | `POST/PATCH /api/v1/uploads` | Chunked resumable upload with checksum, offset, expiry, scan status and abort. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-015
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-011 | POST/PATCH /api/v1/uploads | Chunked resumable upload with checksum, offset, expiry, scan status and abort. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-015»
- [ ] Chunked resumable upload with checksum, offset, expiry, scan status and abort. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-012 [P1] BACKEND-MISSING-012: POST /api/v1/mappings/{id}/review · Accept/reject/edit/merge inferred entities and relationships with reviewer audit. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for muta

- **Source:** `GUI-UIX-requirements.md:1271-1271` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-012` | `POST /api/v1/mappings/{id}/review` | Accept/reject/edit/merge inferred entities and relationships with reviewer audit. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-015
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-012 | POST /api/v1/mappings/{id}/review | Accept/reject/edit/merge inferred entities and relationships with reviewer audit. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-015»
- [ ] Accept/reject/edit/merge inferred entities and relationships with reviewer audit. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-013 [P1] BACKEND-MISSING-013: POST /api/v1/resolution/actions · Merge/split/undo entity resolution with impact preview and idempotency key. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and

- **Source:** `GUI-UIX-requirements.md:1272-1272` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-013` | `POST /api/v1/resolution/actions` | Merge/split/undo entity resolution with impact preview and idempotency key. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-016
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-013 | POST /api/v1/resolution/actions | Merge/split/undo entity resolution with impact preview and idempotency key. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-016»
- [ ] Merge/split/undo entity resolution with impact preview and idempotency key. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-015 [P1] BACKEND-MISSING-015: POST /api/v1/reports/{id}/exports · Durable PDF/DOCX/PPTX/CSV/PNG/SVG job and signed policy-checked download manifest. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mut

- **Source:** `GUI-UIX-requirements.md:1274-1274` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-015` | `POST /api/v1/reports/{id}/exports` | Durable PDF/DOCX/PPTX/CSV/PNG/SVG job and signed policy-checked download manifest. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-019
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-015' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-015') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-015 | POST /api/v1/reports/{id}/exports | Durable PDF/DOCX/PPTX/CSV/PNG/SVG job and signed policy-checked download manifest. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-019»
- [ ] Durable PDF/DOCX/PPTX/CSV/PNG/SVG job and signed policy-checked download manifest. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-017 [P1] BACKEND-MISSING-017: PUT /api/v1/tenants/{id}/model-data-policy · Per-classification/model endpoint sharing rules plus redaction preview and approval. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempote

- **Source:** `GUI-UIX-requirements.md:1276-1276` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-017` | `PUT /api/v1/tenants/{id}/model-data-policy` | Per-classification/model endpoint sharing rules plus redaction preview and approval. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-021
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-017' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-017') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-017 | PUT /api/v1/tenants/{id}/model-data-policy | Per-classification/model endpoint sharing rules plus redaction preview and approval. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-021»
- [ ] Per-classification/model endpoint sharing rules plus redaction preview and approval. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-019 [P1] BACKEND-MISSING-019: GET/PUT /api/v1/me/preferences · Theme, density, locale, shortcuts and notification channels with sync version. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation a

- **Source:** `GUI-UIX-requirements.md:1278-1278` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-019` | `GET/PUT /api/v1/me/preferences` | Theme, density, locale, shortcuts and notification channels with sync version. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-025
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-019' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-019') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-019 | GET/PUT /api/v1/me/preferences | Theme, density, locale, shortcuts and notification channels with sync version. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-025»
- [ ] Theme, density, locale, shortcuts and notification channels with sync version. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-020 [P1] BACKEND-MISSING-020: GET /api/v1/about/licenses · Project/dependency licences, notices, version/build and SBOM download. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit eve

- **Source:** `GUI-UIX-requirements.md:1279-1279` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-020` | `GET /api/v1/about/licenses` | Project/dependency licences, notices, version/build and SBOM download. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-026
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'BACKEND-MISSING-020' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('BACKEND-MISSING-020') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-020 | GET /api/v1/about/licenses | Project/dependency licences, notices, version/build and SBOM download. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-026»
- [ ] Project/dependency licences, notices, version/build and SBOM download. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-049 [P1] INT-049: REST · GET /api/v1/auth/health · Auth Health

- **Source:** `GUI-UIX-requirements.md:568-568` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-049` | REST | `GET /api/v1/auth/health` | Auth Health | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `PARTIAL` | `apps/api/extended.py:1006` | SCR-001, SCR-003, SCR-024, SCR-027
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-049' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-049') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-049 | REST | GET /api/v1/auth/health | Auth Health | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | PARTIAL | apps/api/extended.py:1006 | SCR-001, SCR-003, SCR-024, SCR-027»
- [ ] 200; body not uniform
- [ ] SCR-001, SCR-003, SCR-024, SCR-027
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-050 [P1] INT-050: REST · POST /api/v1/auth/login · Auth Login

- **Source:** `GUI-UIX-requirements.md:569-569` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-050` | REST | `POST /api/v1/auth/login` | Auth Login | `LoginRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `PARTIAL` | `apps/api/extended.py:993` | SCR-001
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-050' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-050') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-050 | REST | POST /api/v1/auth/login | Auth Login | LoginRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | PARTIAL | apps/api/extended.py:993 | SCR-001»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-051 [P1] INT-051: REST · GET /api/v1/authz/decisions · Authz Decisions

- **Source:** `GUI-UIX-requirements.md:570-570` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-051` | REST | `GET /api/v1/authz/decisions` | Authz Decisions | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `PARTIAL` | `apps/api/extended.py:1083` | SCR-001, SCR-021
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-051' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-051') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-051 | REST | GET /api/v1/authz/decisions | Authz Decisions | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | PARTIAL | apps/api/extended.py:1083 | SCR-001, SCR-021»
- [ ] 200; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-052 [P1] INT-052: REST · POST /api/v1/authz/evaluate · Authz Evaluate

- **Source:** `GUI-UIX-requirements.md:571-571` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-052` | REST | `POST /api/v1/authz/evaluate` | Authz Evaluate | `AuthzEvaluateRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `PARTIAL` | `apps/api/extended.py:1088` | SCR-001, SCR-021
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-052' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-052') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-052 | REST | POST /api/v1/authz/evaluate | Authz Evaluate | AuthzEvaluateRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | PARTIAL | apps/api/extended.py:1088 | SCR-001, SCR-021»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-053 [P1] INT-053: REST · GET /api/v1/authz/policies · Authz List Policies

- **Source:** `GUI-UIX-requirements.md:572-572` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-053` | REST | `GET /api/v1/authz/policies` | Authz List Policies | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `PARTIAL` | `apps/api/extended.py:1065` | SCR-001, SCR-021
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-053' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-053') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-053 | REST | GET /api/v1/authz/policies | Authz List Policies | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | PARTIAL | apps/api/extended.py:1065 | SCR-001, SCR-021»
- [ ] 200; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-054 [P1] INT-054: REST · POST /api/v1/authz/policies/reload · Authz Reload Policies

- **Source:** `GUI-UIX-requirements.md:573-573` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-054` | REST | `POST /api/v1/authz/policies/reload` | Authz Reload Policies | `none`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `PARTIAL` | `apps/api/extended.py:1072` | SCR-001, SCR-021
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-054' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-054') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-054 | REST | POST /api/v1/authz/policies/reload | Authz Reload Policies | none; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | PARTIAL | apps/api/extended.py:1072 | SCR-001, SCR-021»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-055 [P1] INT-055: REST · GET /api/v1/authz/roles · Authz List Roles

- **Source:** `GUI-UIX-requirements.md:574-574` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-055` | REST | `GET /api/v1/authz/roles` | Authz List Roles | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `PARTIAL` | `apps/api/extended.py:1040` | SCR-001, SCR-021
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-055' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-055') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-055 | REST | GET /api/v1/authz/roles | Authz List Roles | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | PARTIAL | apps/api/extended.py:1040 | SCR-001, SCR-021»
- [ ] 200; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-056 [P1] INT-056: REST · POST /api/v1/authz/roles · Authz Create Role

- **Source:** `GUI-UIX-requirements.md:575-575` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-056` | REST | `POST /api/v1/authz/roles` | Authz Create Role | `AuthzRoleRequest`; params: none | `object` | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `PARTIAL` | `apps/api/extended.py:1045` | SCR-001, SCR-021
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-056' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-056') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-056 | REST | POST /api/v1/authz/roles | Authz Create Role | AuthzRoleRequest; params: none | object | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | PARTIAL | apps/api/extended.py:1045 | SCR-001, SCR-021»
- [ ] 201,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-057 [P1] INT-057: REST · GET /api/v1/authz/roles/export · Authz Export Roles

- **Source:** `GUI-UIX-requirements.md:576-576` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-057` | REST | `GET /api/v1/authz/roles/export` | Authz Export Roles | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `PARTIAL` | `apps/api/extended.py:1058` | SCR-019, SCR-021
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-057' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-057') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-057 | REST | GET /api/v1/authz/roles/export | Authz Export Roles | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | PARTIAL | apps/api/extended.py:1058 | SCR-019, SCR-021»
- [ ] 200; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-058 [P1] INT-058: REST · GET /api/v1/authz/users · Authz List Users

- **Source:** `GUI-UIX-requirements.md:577-577` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-058` | REST | `GET /api/v1/authz/users` | Authz List Users | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `PARTIAL` | `apps/api/extended.py:1015` | SCR-025
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-058' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-058') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-058 | REST | GET /api/v1/authz/users | Authz List Users | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | PARTIAL | apps/api/extended.py:1015 | SCR-025»
- [ ] 200; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-059 [P1] INT-059: REST · POST /api/v1/authz/users · Authz Create User

- **Source:** `GUI-UIX-requirements.md:578-578` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-059` | REST | `POST /api/v1/authz/users` | Authz Create User | `AuthzUserRequest`; params: none | `object` | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `PARTIAL` | `apps/api/extended.py:1022` | SCR-025
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-059' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-059') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-059 | REST | POST /api/v1/authz/users | Authz Create User | AuthzUserRequest; params: none | object | 201,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | PARTIAL | apps/api/extended.py:1022 | SCR-025»
- [ ] 201,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-060 [P1] INT-060: REST · GET /api/v1/authz/users/export · Authz Export Users

- **Source:** `GUI-UIX-requirements.md:579-579` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-060` | REST | `GET /api/v1/authz/users/export` | Authz Export Users | `none`; params: none | `none` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `PARTIAL` | `apps/api/extended.py:1033` | SCR-019, SCR-025
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-060' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-060') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-060 | REST | GET /api/v1/authz/users/export | Authz Export Users | none; params: none | none | 200; body not uniform | Endpoint-specific; inspect params | no declared event | PARTIAL | apps/api/extended.py:1033 | SCR-019, SCR-025»
- [ ] 200; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-071 [P1] INT-071: REST · GET /api/v1/brain/learning/status · Get Learning Status

- **Source:** `GUI-UIX-requirements.md:590-590` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-071` | REST | `GET /api/v1/brain/learning/status` | Get Learning Status | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/authz/security_router.py:122` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-071' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-071') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-071 | REST | GET /api/v1/brain/learning/status | Get Learning Status | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/authz/security_router.py:122 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-078 [P1] INT-078: REST · POST /api/v1/brain/llm/tokenize · Tokenize Text

- **Source:** `GUI-UIX-requirements.md:597-597` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-078` | REST | `POST /api/v1/brain/llm/tokenize` | Tokenize Text | `LLMTokenizeRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/brain/router.py:452` | SCR-025
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-078' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-078') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-078 | REST | POST /api/v1/brain/llm/tokenize | Tokenize Text | LLMTokenizeRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/brain/router.py:452 | SCR-025»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-137 [P1] INT-137: REST · POST /api/v1/config/rollback · Rollback

- **Source:** `GUI-UIX-requirements.md:656-656` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-137` | REST | `POST /api/v1/config/rollback` | Rollback | `object`; params: none | `ConfigChangeRecord` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/config/router.py:125` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-137' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-137') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-137 | REST | POST /api/v1/config/rollback | Rollback | object; params: none | ConfigChangeRecord | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/config/router.py:125 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-148 [P1] INT-148: REST · POST /api/v1/egress/call · Call

- **Source:** `GUI-UIX-requirements.md:667-667` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-148` | REST | `POST /api/v1/egress/call` | Call | `CallRequest`; params: none | `object` | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/egress/router.py:140` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-148' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-148') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-148 | REST | POST /api/v1/egress/call | Call | CallRequest; params: none | object | 200,422; body not uniform | Endpoint-specific; inspect params | job/poll if response says so; no uniform protocol | IMPLEMENTED-UNVERIFIED | packages/eoip/egress/router.py:140 | No primary screen assigned»
- [ ] 200,422; body not uniform
- [ ] job/poll if response says so; no uniform protocol
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-149 [P1] INT-149: REST · GET /api/v1/egress/endpoints · List Endpoints

- **Source:** `GUI-UIX-requirements.md:668-668` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-149` | REST | `GET /api/v1/egress/endpoints` | List Endpoints | `none`; params: none | `object` | 200; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `packages/eoip/egress/router.py:126` | No primary screen assigned
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'INT-149' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('INT-149') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-149 | REST | GET /api/v1/egress/endpoints | List Endpoints | none; params: none | object | 200; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | packages/eoip/egress/router.py:126 | No primary screen assigned»
- [ ] 200; body not uniform
- [ ] No primary screen assigned
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

