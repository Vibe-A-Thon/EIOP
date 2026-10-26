# EPIC-04NONFUNCTIONA-AMB: EOIP-engg-doc-pkg/04-non-functional-requirements.md · ambiguous_tests

*Mapped tests both pass and fail on the audited commit.* 1 tasks, ~2.0 h, priorities {'P0': 1}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-NFR-SEC-005 [P0] NFR-SEC-005: Authentication without MVP RBAC

- **Source:** `EOIP-engg-doc-pkg/04-non-functional-requirements.md:51-60` (heading) · **Type:** Security · **Severity:** High
- **Now:** Ambiguous / L2 (tests passed 9, failed 1)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D05, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-SEC-005 — Authentication without MVP RBAC
**WHAT:** Protect non-loopback deployments with single-user/local authentication while not implementing role matrices.  
**WHY:** No RBAC does not mean unauthenticated exposure.  
**HOW:** Loopback dev may use dev token; controlled demo uses configured local credential and CSRF-safe patterns.  
**DATA / INTERFACES:** Auth config  
**FAILURE:** Missing auth in non-dev profile blocks startup/exposure.  
**TEST:** Profile/auth tests.  
**COMPLETE WHEN:** /admin route presence is never claimed as authorization boundary.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_deployment_api.py::test_admin_and_read_routes_require_token_and_jobs_are_durable
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Delivers: Protect non-loopback deployments with single-user/local authentication while not implementing role matrices.
- [ ] Interfaces: Auth config
- [ ] Failure behaviour: Missing auth in non-dev profile blocks startup/exposure.
- [ ] Verified by: Profile/auth tests.
- [ ] Complete when: /admin route presence is never claimed as authorization boundary.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L24-L24)
- tests: `tests/unit/test_deployment_api.py:21`, `tests/unit/test_deployment_api.py::test_admin_and_read_routes_require_token_and_jobs_are_durable`
- failing: `tests/unit/test_deployment_api.py::test_admin_and_read_routes_require_token_and_jobs_are_durable`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

