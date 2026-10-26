# EPIC-MVP-NOTEST: EOIP-engg-doc-pkg/MVP-requirements.md · code_no_test

*Code references the ID but no test is mapped.* 1 tasks, ~2.5 h, priorities {'P1': 1}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-MVP-FR-012 [P1] MVP-FR-012: Graph validation

- **Source:** `EOIP-engg-doc-pkg/MVP-requirements.md:134-139` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### MVP-FR-012 — Graph validation
**Parent requirements:** FR-VALID-001, FR-VALID-002  
**Requirement:** Deliver this capability as an integrated part of the P1 architecture.  
**Acceptance:** Seeded invalid data produces expected validation findings and hard invalid edges are prevented/quarantined.  
**Failure behavior:** Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
```
</details>

**Next steps**
1. Read the referenced code: packages/eoip/validation/gate.py:8
2. Write one test per acceptance criterion; mark with @pytest.mark.req('MVP-FR-012') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Deliver this capability as an integrated part of the P1 architecture.
- [ ] Seeded invalid data produces expected validation findings and hard invalid edges are prevented/quarantined.
- [ ] Failure behaviour: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data.
- [ ] Seeded invalid data produces expected validation findings and hard invalid edges are prevented/quarantined
- [ ] Failure behavior: Failure is explicit, logged/audited where applicable, and must not silently substitute hardcoded data
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/validation/gate.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/validation/gate.py#L8-L8)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

