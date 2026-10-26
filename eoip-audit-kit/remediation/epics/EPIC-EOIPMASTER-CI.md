# EPIC-EOIPMASTER-CI: EOIP-master-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 12 tasks, ~8.0 h, priorities {'P0': 11, 'P1': 1}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-CAP-20 [P0] CAP-20: Portable typed query IR and compiler · D03 Query · P0

- **Source:** `EOIP-master-requirements.md:58-58` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-20` | **Portable typed query IR and compiler** | D03 Query | `P0` | 100% Implemented & Verified (WP-KG3-03, CRA-009.1 Verified; Deterministic compiler to openCypher, Gremlin, SPARQL) | **VERIFIED**
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-20 | Portable typed query IR and compiler | D03 Query | P0 | 100% Implemented & Verified (WP-KG3-03, CRA-009.1 Verified; Deterministic compiler to openCypher, Gremlin, SPARQL) | VERIFIED»
- [ ] Portable typed query IR and compiler
- [ ] 100% Implemented & Verified (WP-KG3-03, CRA-009.1 Verified; Deterministic compiler to openCypher, Gremlin, SPARQL)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/query/ast_compiler.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/ast_compiler.py#L1-L1), [`scripts/build_master_suite.py:200`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L200-L200), [`scripts/enhance_master_suite.py:170`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L170-L170), [`scripts/investigate_caps.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L11-L11), [`scripts/patch_suite_and_dashboard.py:36`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L36-L36), [`scripts/update_matrix_caps.py:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L17-L17), [`scripts/verify_22_caps.py:80`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L80-L80)
- tests: `scripts/test_cap_enrichment.py:69`, `scripts/test_master_caps_enrichment.py:83`, `tests/query/test_ast_compiler.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CAP-31 [P0] CAP-31: Probabilistic entity resolution (ER) · D05 Identity · P0

- **Source:** `EOIP-master-requirements.md:69-69` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-31` | **Probabilistic entity resolution (ER)** | D05 Identity | `P0` | 100% Implemented & Verified (WP-KG3-04, CRA-023.2 Verified; Fellegi-Sunter model in DuckDB with 95%+ precision/recall) | **VERIFIED**
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-31 | Probabilistic entity resolution (ER) | D05 Identity | P0 | 100% Implemented & Verified (WP-KG3-04, CRA-023.2 Verified; Fellegi-Sunter model in DuckDB with 95%+ precision/recall) | VERIFIED»
- [ ] Probabilistic entity resolution (ER)
- [ ] 100% Implemented & Verified (WP-KG3-04, CRA-023.2 Verified; Fellegi-Sunter model in DuckDB with 95%+ precision/recall)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/er/splink_engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/er/splink_engine.py#L1-L1), [`scripts/build_master_suite.py:224`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L224-L224), [`scripts/enhance_master_suite.py:172`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L172-L172), [`scripts/investigate_caps.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L10-L10), [`scripts/patch_suite_and_dashboard.py:38`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L38-L38), [`scripts/update_matrix_caps.py:21`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L21-L21), [`scripts/verify_22_caps.py:108`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L108-L108)
- tests: `scripts/test_cap_enrichment.py:93`, `scripts/test_master_caps_enrichment.py:107`, `tests/unit/test_splink_er_engine.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CAP-46 [P0] CAP-46: Derivation-aware source-ACL enforcement in retrieval · D06 Ingestion · P0

- **Source:** `EOIP-master-requirements.md:84-84` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-46` | **Derivation-aware source-ACL enforcement in retrieval** | D06 Ingestion | `P0` | 100% Implemented & Verified (WP-KG3-01, CRA-003.8 Verified; Zero restricted triple leakage under multi-hop inference) | **VERIFIED**
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-46 | Derivation-aware source-ACL enforcement in retrieval | D06 Ingestion | P0 | 100% Implemented & Verified (WP-KG3-01, CRA-003.8 Verified; Zero restricted triple leakage under multi-hop inference) | VERIFIED»
- [ ] Derivation-aware source-ACL enforcement in retrieval
- [ ] 100% Implemented & Verified (WP-KG3-01, CRA-003.8 Verified; Zero restricted triple leakage under multi-hop inference)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/authz/derivation_acl.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/authz/derivation_acl.py#L1-L1), [`scripts/build_master_suite.py:242`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L242-L242), [`scripts/enhance_master_suite.py:166`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L166-L166), [`scripts/investigate_caps.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L11-L11), [`scripts/patch_suite_and_dashboard.py:32`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L32-L32), [`scripts/update_matrix_caps.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L24-L24), [`scripts/verify_22_caps.py:129`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L129-L129)
- tests: `scripts/test_cap_enrichment.py:111`, `scripts/test_master_caps_enrichment.py:125`, `tests/security/test_derivation_acl_pipeline.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CAP-47 [P0] CAP-47: Multi-tenant isolation (SILO / BRIDGE / POOL) · D06 Ingestion · P0

- **Source:** `EOIP-master-requirements.md:85-85` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-47` | **Multi-tenant isolation (SILO / BRIDGE / POOL)** | D06 Ingestion | `P0` | 100% Implemented & Verified (WP-KG3-02, CRA-003.6 Verified; 100% namespace prefixing & cross-tenant barrier verification) | **VERIFIED**
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-47 | Multi-tenant isolation (SILO / BRIDGE / POOL) | D06 Ingestion | P0 | 100% Implemented & Verified (WP-KG3-02, CRA-003.6 Verified; 100% namespace prefixing & cross-tenant barrier verification) | VERIFIED»
- [ ] Multi-tenant isolation (SILO / BRIDGE / POOL)
- [ ] 100% Implemented & Verified (WP-KG3-02, CRA-003.6 Verified; 100% namespace prefixing & cross-tenant barrier verification)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/tenancy/isolation_hardened.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/isolation_hardened.py#L1-L1), [`scripts/build_master_suite.py:248`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L248-L248), [`scripts/enhance_master_suite.py:168`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L168-L168), [`scripts/investigate_caps.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L12-L12), [`scripts/patch_suite_and_dashboard.py:34`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L34-L34), [`scripts/update_matrix_caps.py:25`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L25-L25), [`scripts/verify_22_caps.py:136`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L136-L136)
- tests: `scripts/test_cap_enrichment.py:117`, `scripts/test_master_caps_enrichment.py:131`, `tests/security/test_multi_tenant_isolation_hardened.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-CAP-56 [P0] CAP-56: GraphRAG (Local, Global, and Path Traversal) · D07 Security · P0

- **Source:** `EOIP-master-requirements.md:94-94` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-56` | **GraphRAG (Local, Global, and Path Traversal)** | D07 Security | `P0` | 100% Implemented & Verified (WP-KG3-07, CRA-026.1 Verified; Dual-level LightRAG + HippoRAG PPR diffusion) | **VERIFIED**
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-56 | GraphRAG (Local, Global, and Path Traversal) | D07 Security | P0 | 100% Implemented & Verified (WP-KG3-07, CRA-026.1 Verified; Dual-level LightRAG + HippoRAG PPR diffusion) | VERIFIED»
- [ ] GraphRAG (Local, Global, and Path Traversal)
- [ ] 100% Implemented & Verified (WP-KG3-07, CRA-026.1 Verified; Dual-level LightRAG + HippoRAG PPR diffusion)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/rag/dual_level_diffusion.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/rag/dual_level_diffusion.py#L1-L1), [`scripts/build_master_suite.py:260`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L260-L260), [`scripts/enhance_master_suite.py:174`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L174-L174), [`scripts/patch_suite_and_dashboard.py:40`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L40-L40)
- tests: `scripts/test_master_caps_enrichment.py:143`, `tests/ai/test_dual_level_hipporag.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-01 [P0] GAP-01: CAP-46 / BL-18 · CLOSED · Triplestores, vector stores, and KnowGridFlow's existing retrieval service treat graph facts as globally readable once indexed. Evaluating traversals over mixed-permission da

- **Source:** `EOIP-master-requirements.md:2650-2650` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GAP-01` | **`CAP-46 / BL-18`** | `CLOSED` | `Triplestores, vector stores, and KnowGridFlow's existing retrieval service treat graph facts as globally readable once indexed. Evaluating traversals over mixed-permission data leaks private facts to unauthorized users.` | **P0**
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GAP-01 | CAP-46 / BL-18 | CLOSED | Triplestores, vector stores, and KnowGridFlow's existing retrieval service treat graph facts as globally readable once indexed. Evaluating traversals over mixed-permission data leaks private facts to unauthorized users. | P0»
- [ ] Triplestores, vector stores, and KnowGridFlow's existing retrieval service treat graph facts as globally readable once indexed. Evaluating traversals over mixed-permission data leaks private facts to unauthorized users.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/authz/derivation_acl.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/authz/derivation_acl.py#L1-L1), [`packages/eoip/ontology/manifest.py:283`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/manifest.py#L283-L283), [`scripts/build_master_suite.py:345`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L345-L345), [`scripts/enhance_master_suite.py:198`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L198-L198)
- tests: `tests/security/test_derivation_acl_pipeline.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-GAP-04 [P0] GAP-04: CAP-20 / BL-09 · CLOSED · Moonshot universal transpiler uses regex substitution, which breaks on nested sub-queries and variable-length path predicates.

- **Source:** `EOIP-master-requirements.md:2652-2652` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GAP-04` | **`CAP-20 / BL-09`** | `CLOSED` | `Moonshot universal transpiler uses regex substitution, which breaks on nested sub-queries and variable-length path predicates.` | **P0**
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GAP-04 | CAP-20 / BL-09 | CLOSED | Moonshot universal transpiler uses regex substitution, which breaks on nested sub-queries and variable-length path predicates. | P0»
- [ ] Moonshot universal transpiler uses regex substitution, which breaks on nested sub-queries and variable-length path predicates.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/query/ast_compiler.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/ast_compiler.py#L1-L1), [`scripts/build_master_suite.py:382`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L382-L382), [`scripts/enhance_master_suite.py:235`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L235-L235)
- tests: `tests/query/test_ast_compiler.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-07 [P0] GAP-07: CAP-47 / BL-20 · CLOSED · Graph backend adapters contain 0 references to tenant scoping; physical isolation is labeled 'External gate'.

- **Source:** `EOIP-master-requirements.md:2655-2655` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GAP-07` | **`CAP-47 / BL-20`** | `CLOSED` | `Graph backend adapters contain 0 references to tenant scoping; physical isolation is labeled 'External gate'.` | **P0**
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GAP-07 | CAP-47 / BL-20 | CLOSED | Graph backend adapters contain 0 references to tenant scoping; physical isolation is labeled 'External gate'. | P0»
- [ ] Graph backend adapters contain 0 references to tenant scoping; physical isolation is labeled 'External gate'.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ontology/manifest.py:283`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/manifest.py#L283-L283), [`packages/eoip/tenancy/isolation_hardened.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/isolation_hardened.py#L1-L1), [`scripts/build_master_suite.py:381`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L381-L381), [`scripts/enhance_master_suite.py:234`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L234-L234)
- tests: `tests/security/test_multi_tenant_isolation_hardened.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-INV-01 [P0] INV-01: GraphDB / Stardog / Palantir · Derived facts and vector embeddings are treated as globally visible, surfacing restricted data · Derivation-Aware ACL Composition: Cryptographically compose premise ACLs

- **Source:** `EOIP-master-requirements.md:2664-2664` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INV-01` | **GraphDB / Stardog / Palantir** | Derived facts and vector embeddings are treated as globally visible, surfacing restricted data | **Derivation-Aware ACL Composition: Cryptographically compose premise ACLs onto derived facts; policy epoch invalidation on revocation** | ``ADOPT (P0)``
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INV-01 | GraphDB / Stardog / Palantir | Derived facts and vector embeddings are treated as globally visible, surfacing restricted data | Derivation-Aware ACL Composition: Cryptographically compose premise ACLs onto derived facts; policy epoch invalidation on revocation | ADOPT (P0)»
- [ ] GraphDB / Stardog / Palantir
- [ ] Derived facts and vector embeddings are treated as globally visible, surfacing restricted data
- [ ] Derivation-Aware ACL Composition: Cryptographically compose premise ACLs onto derived facts; policy epoch invalidation on revocation
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/authz/derivation_acl.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/authz/derivation_acl.py#L1-L1), [`scripts/build_master_suite.py:380`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L380-L380), [`scripts/enhance_master_suite.py:233`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L233-L233)
- tests: `tests/security/test_derivation_acl_pipeline.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-INV-SELF-02 [P0] INV-SELF-02: KnowGridFlow Baseline (BL-20) · Graph backend adapters contain zero tenant scoping parameters, risking multi-tenant cross-talk · Enforce tenant prefixing and logical partition isolation in GraphStore 

- **Source:** `EOIP-master-requirements.md:2675-2675` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INV-SELF-02` | **KnowGridFlow Baseline (BL-20)** | Graph backend adapters contain zero tenant scoping parameters, risking multi-tenant cross-talk | **Enforce tenant prefixing and logical partition isolation in GraphStore protocol across all backends** | ``ADOPT (P0)``
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INV-SELF-02 | KnowGridFlow Baseline (BL-20) | Graph backend adapters contain zero tenant scoping parameters, risking multi-tenant cross-talk | Enforce tenant prefixing and logical partition isolation in GraphStore protocol across all backends | ADOPT (P0)»
- [ ] Graph backend adapters contain zero tenant scoping parameters, risking multi-tenant cross-talk
- [ ] Enforce tenant prefixing and logical partition isolation in GraphStore protocol across all backends
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/tenancy/isolation_hardened.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/isolation_hardened.py#L1-L1), [`scripts/build_master_suite.py:381`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L381-L381), [`scripts/enhance_master_suite.py:234`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L234-L234)
- tests: `tests/security/test_multi_tenant_isolation_hardened.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-INV-SELF-03 [P0] INV-SELF-03: KnowGridFlow Baseline (BL-09) · Regex string substitution cannot parse nested subqueries, aggregations, or GQL path expressions · Build typed AST query compiler (QueryPlan -> Backend AST) with formal 

- **Source:** `EOIP-master-requirements.md:2676-2676` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INV-SELF-03` | **KnowGridFlow Baseline (BL-09)** | Regex string substitution cannot parse nested subqueries, aggregations, or GQL path expressions | **Build typed AST query compiler (QueryPlan -> Backend AST) with formal dialect conformance tests** | ``ADOPT (P0)``
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INV-SELF-03 | KnowGridFlow Baseline (BL-09) | Regex string substitution cannot parse nested subqueries, aggregations, or GQL path expressions | Build typed AST query compiler (QueryPlan -> Backend AST) with formal dialect conformance tests | ADOPT (P0)»
- [ ] Regex string substitution cannot parse nested subqueries, aggregations, or GQL path expressions
- [ ] Build typed AST query compiler (QueryPlan -> Backend AST) with formal dialect conformance tests
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/query/ast_compiler.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/ast_compiler.py#L1-L1), [`scripts/build_master_suite.py:382`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L382-L382), [`scripts/enhance_master_suite.py:235`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L235-L235)
- tests: `tests/query/test_ast_compiler.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-GAP-05 [P1] GAP-05: CAP-56 / BL-16 · CLOSED · Existing GraphRAG handles 1-2 hop neighborhood retrieval but cannot answer corpus-wide thematic questions ('What are the major systemic risks across all services?').

- **Source:** `EOIP-master-requirements.md:2653-2653` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GAP-05` | **`CAP-56 / BL-16`** | `CLOSED` | `Existing GraphRAG handles 1-2 hop neighborhood retrieval but cannot answer corpus-wide thematic questions ('What are the major systemic risks across all services?').` | **P1**
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GAP-05 | CAP-56 / BL-16 | CLOSED | Existing GraphRAG handles 1-2 hop neighborhood retrieval but cannot answer corpus-wide thematic questions ('What are the major systemic risks across all services?'). | P1»
- [ ] Existing GraphRAG handles 1-2 hop neighborhood retrieval but cannot answer corpus-wide thematic questions ('What are the major systemic risks across all services?').
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/rag/dual_level_diffusion.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/rag/dual_level_diffusion.py#L1-L1), [`scripts/build_master_suite.py:386`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L386-L386), [`scripts/enhance_master_suite.py:239`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L239-L239)
- tests: `tests/ai/test_dual_level_hipporag.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

