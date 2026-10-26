# EPIC-03FUNCTIONAL-NOTEST: EOIP-engg-doc-pkg/03-functional-requirements.md · code_no_test

*Code references the ID but no test is mapped.* 2 tasks, ~5.0 h, priorities {'P1': 2}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-FR-GRAPH-004 [P1] FR-GRAPH-004: Canonical identifiers

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:181-190` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-GRAPH-004 — Canonical identifiers
**WHAT:** Define deterministic IDs independent of HugeGraph internal IDs where possible.  
**WHY:** Traceability and replay cannot depend on unstable database identifiers.  
**HOW:** canonical_id is the platform identity; source aliases map to it; ambiguous identities stay separate.  
**DATA / INTERFACES:** canonical_id/source_id/source_system  
**FAILURE:** Collision is a blocking validation error.  
**TEST:** Collision/idempotency tests.  
**COMPLETE WHEN:** Every canonical entity has unique stable canonical_id.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Read the referenced code: scripts/tick_phase0_phase1.py:15
2. Write one test per acceptance criterion; mark with @pytest.mark.req('FR-GRAPH-004') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Delivers: Define deterministic IDs independent of HugeGraph internal IDs where possible.
- [ ] Failure behaviour: Collision is a blocking validation error.
- [ ] Verified by: Collision/idempotency tests.
- [ ] Complete when: Every canonical entity has unique stable canonical_id.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L15-L15)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-TEMP-001 [P1] FR-TEMP-001: Bitemporal-ready fields

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:315-324` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-TEMP-001 — Bitemporal-ready fields
**WHAT:** Store created/modified/deleted, first/last seen, valid_from/valid_to and source_version where available.  
**WHY:** Enterprise topology changes over time.  
**HOW:** MVP writes fields and current-state queries; historical reconstruction/diff is P5.  
**DATA / INTERFACES:** temporal properties  
**FAILURE:** Invalid intervals generate validation findings.  
**TEST:** Temporal validation tests.  
**COMPLETE WHEN:** MVP schema is ready for P5 without ID rewrite.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Read the referenced code: scripts/tick_phase0_phase1.py:16
2. Write one test per acceptance criterion; mark with @pytest.mark.req('FR-TEMP-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Delivers: Store created/modified/deleted, first/last seen, valid_from/valid_to and source_version where available.
- [ ] Interfaces: temporal properties
- [ ] Failure behaviour: Invalid intervals generate validation findings.
- [ ] Verified by: Temporal validation tests.
- [ ] Complete when: MVP schema is ready for P5 without ID rewrite.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase0_phase1.py:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase0_phase1.py#L16-L16)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

