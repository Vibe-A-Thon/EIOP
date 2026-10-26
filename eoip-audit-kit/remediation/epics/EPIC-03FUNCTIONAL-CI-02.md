# EPIC-03FUNCTIONAL-CI-02: EOIP-engg-doc-pkg/03-functional-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 1 tasks, ~0.5 h, priorities {'P3': 1}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-FR-RAG-006 [P3] FR-RAG-006: Adaptive RAG strategy framework

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:535-544` (heading) · **Type:** AI · **Severity:** Low
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-RAG-006 — Adaptive RAG strategy framework
**WHAT:** Expose strategy interface for simple/graph/hybrid/corrective/self/adaptive/agentic/multi-hop variants without instantiating all.  
**WHY:** Future expansion should not rewrite retrieval.  
**HOW:** Strategy selected by router and capability/config; Phase 3 adds advanced variants based on evaluation.  
**DATA / INTERFACES:** RAGStrategy  
**FAILURE:** Unsupported strategy rejected cleanly.  
**TEST:** Strategy contract tests.  
**COMPLETE WHEN:** P3 can add strategy plugin without changing callers.  
**TARGET PHASE:** P3
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Delivers: Expose strategy interface for simple/graph/hybrid/corrective/self/adaptive/agentic/multi-hop variants without instantiating all.
- [ ] Failure behaviour: Unsupported strategy rejected cleanly.
- [ ] Verified by: Strategy contract tests.
- [ ] Complete when: P3 can add strategy plugin without changing callers.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/retrieval/strategy_registry.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/retrieval/strategy_registry.py#L1-L1)
- tests: `tests/unit/test_strategy_registry.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

