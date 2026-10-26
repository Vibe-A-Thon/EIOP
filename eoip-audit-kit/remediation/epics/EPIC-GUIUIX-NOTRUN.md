# EPIC-GUIUIX-NOTRUN: GUI-UIX-requirements.md · tests_not_executed

*Tests are mapped/referenced but none ran in the audit (excluded or not collected).* 2 tasks, ~2.0 h, priorities {'P1': 2}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-INT-001 [P1] INT-001: REST · GET /api/v1/admin/audit · Audit Log

- **Source:** `GUI-UIX-requirements.md:520-520` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-001` | REST | `GET /api/v1/admin/audit` | Audit Log | `none`; params: limit | `none` | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | `IMPLEMENTED-UNVERIFIED` | `apps/api/main.py:1441` | SCR-021
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): apps/web/tests/unit/gui-intake.test.mjs:19
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-001 | REST | GET /api/v1/admin/audit | Audit Log | none; params: limit | none | 200,422; body not uniform | Endpoint-specific; inspect params | no declared event | IMPLEMENTED-UNVERIFIED | apps/api/main.py:1441 | SCR-021»
- [ ] 200,422; body not uniform
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `apps/web/tests/unit/gui-intake.test.mjs:19`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INT-735 [P1] INT-735: WebSocket · WS /api/v1/ws/jobs/{job_id} · Job status subscription

- **Source:** `GUI-UIX-requirements.md:1254-1254` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INT-735` | WebSocket | `WS /api/v1/ws/jobs/{job_id}` | Job status subscription | path job_id; auth/tenant contract absent | JSON job events, schema not published | Handshake returned 500 without auth | n/a | Real-time; resume/cancel unspecified | `PARTIAL` | `apps/api/main.py:1489` | SCR-017, SCR-024
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): apps/web/tests/unit/gui-intake.test.mjs:19
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INT-735 | WebSocket | WS /api/v1/ws/jobs/{job_id} | Job status subscription | path job_id; auth/tenant contract absent | JSON job events, schema not published | Handshake returned 500 without auth | n/a | Real-time; resume/cancel unspecified | PARTIAL | apps/api/main.py:1489 | SCR-017, SCR-024»
- [ ] path job_id; auth/tenant contract absent
- [ ] JSON job events, schema not published
- [ ] Handshake returned 500 without auth
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `apps/web/tests/unit/gui-intake.test.mjs:19`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

