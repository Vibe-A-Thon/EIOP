# EPIC-25QUERYENGINE-UNTR: EOIP-engg-doc-pkg/25-query-engine-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 1 tasks, ~6.0 h, priorities {'P1': 1}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-FR-QUERY-009 [P1] FR-QUERY-009: Natural-language query processor · P1-MVP · NLQ routes graph facts, query operators, QueryPlan execution and safe search fallback while returning answer text, confidence, highlights and follow-ups.

- **Source:** `EOIP-engg-doc-pkg/25-query-engine-requirements.md:30-30` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
FR-QUERY-009 | Natural-language query processor | P1-MVP | NLQ routes graph facts, query operators, QueryPlan execution and safe search fallback while returning answer text, confidence, highlights and follow-ups.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-QUERY-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-QUERY-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «FR-QUERY-009 | Natural-language query processor | P1-MVP | NLQ routes graph facts, query operators, QueryPlan execution and safe search fallback while returning answer text, confidence, highlights and follow-ups.»
- [ ] NLQ routes graph facts, query operators, QueryPlan execution and safe search fallback while returning answer text, confidence, highlights and follow-ups.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

