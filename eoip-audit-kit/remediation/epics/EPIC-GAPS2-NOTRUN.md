# EPIC-GAPS2-NOTRUN: EOIP-engg-doc-pkg/gaps2-requirements.md · tests_not_executed

*Tests are mapped/referenced but none ran in the audit (excluded or not collected).* 1 tasks, ~1.0 h, priorities {'P1': 1}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-G2-EKAF-027 [P1] G2-EKAF-027: Source capability introspection

- **Source:** `EOIP-engg-doc-pkg/gaps2-requirements.md:322-333` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### G2-EKAF-027 — Source capability introspection
Each connector SHALL report supported capabilities such as:
- baseline,
- delta,
- webhook,
- delete detection,
- version history,
- permissions,
- attachments,
- comments,
- relationships.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_g2_readiness.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Each connector SHALL report supported capabilities such as: - baseline, - delta, - webhook, - delete detection, - version history, - permissions, - attachments, - comments, - relationships.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L12-L12)
- tests: `tests/unit/test_g2_readiness.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

