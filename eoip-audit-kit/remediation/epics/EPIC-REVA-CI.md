# EPIC-REVA-CI: reva-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 2 tasks, ~1.0 h, priorities {'P0': 1, 'P1': 1}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-REVA-SEC-013 [P0] REVA-SEC-013: Zero-Data-Leak LLM Egress Gate & Deterministic Python-First Policy: 95%+ of AST/CFG parsing, symbol extraction, boundary matching, binary disassembly, and graph projection MUST be performed by determi

- **Source:** `reva-requirements.md:1034-1034` (table_row) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 1, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SEC-013 | **Zero-Data-Leak LLM Egress Gate & Deterministic Python-First Policy**: 95%+ of AST/CFG parsing, symbol extraction, boundary matching, binary disassembly, and graph projection MUST be performed by deterministic, pure-Python logic without invoking an LLM. When an LLM is required for natural language summarization or query synthesis, the request MUST pass through the LLM Egress Security Gate: (a) automated RFC 6901 pointer redaction strips all secrets, passwords, credentials, tokens, and PII; (b) proprietary source code is abstracted into structure/pseudonym tokens (`[ENTITY_1]`); (c) local offline LLMs (via Ollama/vLLM) are prioritized by default; (d) external LLM calls are blocked unless explicit tenant egress policy is configured; (e) prompt injection fencing wraps untrusted code in defensive isolation markers (`_meta.provenance.untrusted_content`). | Byte-scan of LLM egress payload asserts zero secrets, zero raw source files, and strict tokenization; offline fallback test verifies core workflows operate with LLM disabled. | acceptance
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Byte-scan of LLM egress payload asserts zero secrets, zero raw source files, and strict tokenization; offline fallback test verifies core workflows operate with LLM disabled
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/core/egress_gate.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/core/egress_gate.py#L2-L2), [`reva/core/pseudonymizer.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/core/pseudonymizer.py#L2-L2)
- tests: `tests/reva/unit/workflows/test_repo_to_graph.py:131`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-REVA-AB-014 [P1] REVA-AB-014: Repository URL Ingestion Pipeline: Ingest source code and binaries directly from GitHub, GitLab, Bitbucket, Azure Repos, raw Git HTTPS/SSH URLs, or uploaded archives (zip/tar). Sandboxed clone/fetch u

- **Source:** `reva-requirements.md:888-888` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 1, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AB-014 | **Repository URL Ingestion Pipeline**: Ingest source code and binaries directly from GitHub, GitLab, Bitbucket, Azure Repos, raw Git HTTPS/SSH URLs, or uploaded archives (zip/tar). Sandboxed clone/fetch under strict shallow depth (`--depth 1` default), timeout ($\le 300\text{s}$), and size quotas ($\le 5\text{ GiB}$); verifies commit hash, branch/tag signatures; automatically triggers pure-Python Tree-sitter boundary parsing, native binary scanning (`REVA-NB`), and Wisdom Graph extraction. | Clones fixture Git repositories from local bare git daemon; correctly extracts service boundaries and commits; detects invalid URLs and auth errors safely with `REVA_ERR_GIT_REMOTE_FAILED`. | integration
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Clones fixture Git repositories from local bare git daemon; correctly extracts service boundaries and commits; detects invalid URLs and auth errors safely with REVAERRGITREMOTEFAILED
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/repo/cloner.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/repo/cloner.py#L2-L2), [`reva/extract/repo/code_analyzer.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/repo/code_analyzer.py#L2-L2), [`reva/workflows/repo_to_graph.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/workflows/repo_to_graph.py#L2-L2)
- tests: `tests/reva/unit/workflows/test_repo_to_graph.py:2`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

