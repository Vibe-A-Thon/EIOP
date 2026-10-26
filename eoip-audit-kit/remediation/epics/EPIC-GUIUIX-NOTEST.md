# EPIC-GUIUIX-NOTEST: GUI-UIX-requirements.md · code_no_test

*Code references the ID but no test is mapped.* 4 tasks, ~13.4 h, priorities {'P0': 2, 'P1': 2}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-SCR-010 [P0] SCR-010: Temporal and time travel

- **Source:** `GUI-UIX-requirements.md:243-255` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 3 other site(s): see duplicate task DUP-SCR-010; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 4.2 h (M, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-010 - Temporal and time travel

- **Route / personas / purpose:** `/t/:tenant/w/:workspace/time`; Analyst, steward; Compare snapshots and play graph evolution.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `INT-029`, `INT-083`, `INT-180`, `INT-196`, `INT-215`, `INT-216`, `INT-217`, `INT-218`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_010.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Read the referenced code: frontend/src/screens/Temporal.tsx:180
2. Write one test per acceptance criterion; mark with @pytest.mark.req('SCR-010') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-SCR-010

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: IMPLEMENTED-UNVERIFIED. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`frontend/src/screens/Temporal.tsx:180`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/frontend/src/screens/Temporal.tsx#L180-L180)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SCR-020 [P0] SCR-020: Collaboration

- **Source:** `GUI-UIX-requirements.md:373-385` (heading) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 3 other site(s): see duplicate task DUP-SCR-020; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 4.2 h (M, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### SCR-020 - Collaboration

- **Route / personas / purpose:** `/t/:tenant/w/:workspace/collaboration`; All collaborators; Comment, mention, share views and see presence.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** `BACKEND-MISSING-016`. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `scr_020.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidation a
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Read the referenced code: frontend/src/screens/Collaboration.tsx:8
2. Write one test per acceptance criterion; mark with @pytest.mark.req('SCR-020') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-SCR-020

**Acceptance criteria**
- [ ] Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidati
- [ ] Backend readiness: PARTIAL. Use MSW only for BACKEND-MISSING-; show a development-only “mock contract” marker and block production builds if any required mock remains enabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`frontend/src/screens/Collaboration.tsx:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/frontend/src/screens/Collaboration.tsx#L8-L8)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-016 [P1] BACKEND-MISSING-016: WS /api/v1/collaboration/{workspace} · Principal-bound presence, comments and optional Yjs update relay with tenant ACL. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for m

- **Source:** `GUI-UIX-requirements.md:1275-1275` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-016` | `WS /api/v1/collaboration/{workspace}` | Principal-bound presence, comments and optional Yjs update relay with tenant ACL. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-020
```
</details>

**Next steps**
1. Read the referenced code: frontend/src/screens/Collaboration.tsx:8
2. Write one test per acceptance criterion; mark with @pytest.mark.req('BACKEND-MISSING-016') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-016 | WS /api/v1/collaboration/{workspace} | Principal-bound presence, comments and optional Yjs update relay with tenant ACL. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-020»
- [ ] Principal-bound presence, comments and optional Yjs update relay with tenant ACL. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`frontend/src/screens/Collaboration.tsx:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/frontend/src/screens/Collaboration.tsx#L8-L8)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-BACKEND-MISSING-018 [P1] BACKEND-MISSING-018: POST /api/v1/tenants/{id}/brand/publish · Draft asset upload, contrast validation, preview token and atomic publish/rollback. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency 

- **Source:** `GUI-UIX-requirements.md:1277-1277` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`BACKEND-MISSING-018` | `POST /api/v1/tenants/{id}/brand/publish` | Draft asset upload, contrast validation, preview token and atomic publish/rollback. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-023
```
</details>

**Next steps**
1. Read the referenced code: frontend/src/screens/Brand.tsx:148
2. Write one test per acceptance criterion; mark with @pytest.mark.req('BACKEND-MISSING-018') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «BACKEND-MISSING-018 | POST /api/v1/tenants/{id}/brand/publish | Draft asset upload, contrast validation, preview token and atomic publish/rollback. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | SCR-023»
- [ ] Draft asset upload, contrast validation, preview token and atomic publish/rollback. Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`frontend/src/screens/Brand.tsx:148`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/frontend/src/screens/Brand.tsx#L148-L148)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

