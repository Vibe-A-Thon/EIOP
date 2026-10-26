# EPIC-SUPER-NOTRUN-03: EOIP-engg-doc-pkg/super-requirements.md · tests_not_executed

*Tests are mapped/referenced but none ran in the audit (excluded or not collected).* 60 tasks, ~75.0 h, priorities {'P0': 45, 'P1': 15}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-SR-QRY-004 [P0] SR-QRY-004: Dialect round-trip tests: a golden corpus (≥ 500 queries per Tier A backend, growing) MUST prove IR → dialect semantic equivalence by result comparison on shared fixtures

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:315-315` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QRY-004 | **Dialect round-trip tests:** a golden corpus (≥ 500 queries per Tier A backend, growing) MUST prove IR → dialect semantic equivalence by result comparison on shared fixtures. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QRY-004 | Dialect round-trip tests: a golden corpus (≥ 500 queries per Tier A backend, growing) MUST prove IR → dialect semantic equivalence by result comparison on shared fixtures. | P0»
- [ ] Dialect round-trip tests: a golden corpus (≥ 500 queries per Tier A backend, growing) MUST prove IR → dialect semantic equivalence by result comparison on shared fixtures.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-QRY-005 [P0] SR-QRY-005: Parameterization everywhere; string-built queries are forbidden (injection defense)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:316-316` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QRY-005 | **Parameterization everywhere;** string-built queries are forbidden (injection defense). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QRY-005 | Parameterization everywhere; string-built queries are forbidden (injection defense). | P0»
- [ ] Parameterization everywhere; string-built queries are forbidden (injection defense).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-QRY-006 [P0] SR-QRY-006: Saved queries, query libraries, templates and versioned "question catalog" per tenant/workspace, shareable and permission-aware

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:317-317` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QRY-006 | **Saved queries, query libraries, templates and versioned "question catalog"** per tenant/workspace, shareable and permission-aware. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QRY-006 | Saved queries, query libraries, templates and versioned "question catalog" per tenant/workspace, shareable and permission-aware. | P0»
- [ ] Saved queries, query libraries, templates and versioned "question catalog" per tenant/workspace, shareable and permission-aware.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-QRY-007 [P0] SR-QRY-007: Result envelope: rows/graph/table/report + evidence IDs + method flags + freshness (as-of, lag) + coverage notes + policy filters applied

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:318-318` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QRY-007 | **Result envelope:** rows/graph/table/report + evidence IDs + method flags + freshness (as-of, lag) + coverage notes + policy filters applied. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QRY-007 | Result envelope: rows/graph/table/report + evidence IDs + method flags + freshness (as-of, lag) + coverage notes + policy filters applied. | P0»
- [ ] Result envelope: rows/graph/table/report + evidence IDs + method flags + freshness (as-of, lag) + coverage notes + policy filters applied.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-RAG-001 [P0] SR-RAG-001: Router chooses strategy per query class with a logged rationale; operators can override per tenant/workspace; unknown classes degrade to hybrid retrieval with a visible notice

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:563-563` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-RAG-001 | **Router** chooses strategy per query class with a logged rationale; operators can override per tenant/workspace; unknown classes degrade to hybrid retrieval with a visible notice. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-RAG-001 | Router chooses strategy per query class with a logged rationale; operators can override per tenant/workspace; unknown classes degrade to hybrid retrieval with a visible notice. | P0»
- [ ] Router chooses strategy per query class with a logged rationale; operators can override per tenant/workspace; unknown classes degrade to hybrid retrieval with a visible notice.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-RAG-002 [P0] SR-RAG-002: GraphRAG patterns: local (entity-neighborhood + attached documents), global (community-summary map-reduce), path-based, subgraph-as-context, and temporal

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:564-564` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-RAG-002 | **GraphRAG patterns:** local (entity-neighborhood + attached documents), global (community-summary map-reduce), path-based, subgraph-as-context, and temporal. | P0 (local) / P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-RAG-002 | GraphRAG patterns: local (entity-neighborhood + attached documents), global (community-summary map-reduce), path-based, subgraph-as-context, and temporal. | P0 (local) / P1»
- [ ] GraphRAG patterns: local (entity-neighborhood + attached documents), global (community-summary map-reduce), path-based, subgraph-as-context, and temporal.
- [ ] P0 (local) / P1
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-RAG-003 [P0] SR-RAG-003: Hybrid retrieval: BM25 + dense (+ optional sparse-learned) with reciprocal-rank fusion, cross-encoder reranking (local models), metadata/policy filtering before ranking

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:565-565` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-RAG-003 | **Hybrid retrieval:** BM25 + dense (+ optional sparse-learned) with reciprocal-rank fusion, cross-encoder reranking (local models), metadata/policy filtering *before* ranking. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-RAG-003 | Hybrid retrieval: BM25 + dense (+ optional sparse-learned) with reciprocal-rank fusion, cross-encoder reranking (local models), metadata/policy filtering before ranking. | P0»
- [ ] Hybrid retrieval: BM25 + dense (+ optional sparse-learned) with reciprocal-rank fusion, cross-encoder reranking (local models), metadata/policy filtering before ranking.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-RAG-005 [P0] SR-RAG-005: Graph-aware chunking: chunk boundaries follow document structure and link to graph entities; every chunk carries rawid, section path, classification, ontology links

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:567-567` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-RAG-005 | **Graph-aware chunking:** chunk boundaries follow document structure and link to graph entities; every chunk carries `raw_id`, section path, classification, ontology links. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-RAG-005 | Graph-aware chunking: chunk boundaries follow document structure and link to graph entities; every chunk carries raw_id, section path, classification, ontology links. | P0»
- [ ] Graph-aware chunking: chunk boundaries follow document structure and link to graph entities; every chunk carries raw_id, section path, classification, ontology links.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-RAG-006 [P0] SR-RAG-006: Corrective verification: before returning any LLM-generated assertion, verify entity/relationship claims against deterministic graph facts; unverifiable claims are removed or labeled

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:568-568` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-RAG-006 | **Corrective verification:** before returning any LLM-generated assertion, verify entity/relationship claims against deterministic graph facts; unverifiable claims are removed or labeled. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-RAG-006 | Corrective verification: before returning any LLM-generated assertion, verify entity/relationship claims against deterministic graph facts; unverifiable claims are removed or labeled. | P0»
- [ ] Corrective verification: before returning any LLM-generated assertion, verify entity/relationship claims against deterministic graph facts; unverifiable claims are removed or labeled.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-RAG-007 [P0] SR-RAG-007: Context budget manager: token-aware assembly, deduplication, evidence prioritization, and per-model context-window adaptation

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:569-569` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-RAG-007 | **Context budget manager:** token-aware assembly, deduplication, evidence prioritization, and per-model context-window adaptation. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-RAG-007 | Context budget manager: token-aware assembly, deduplication, evidence prioritization, and per-model context-window adaptation. | P0»
- [ ] Context budget manager: token-aware assembly, deduplication, evidence prioritization, and per-model context-window adaptation.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-RAG-008 [P0] SR-RAG-008: Model-down fallback: if no model is reachable, return deterministic results, retrieved evidence and templated narration with clear labeling (inherited MVP-FR-020)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:570-570` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-RAG-008 | **Model-down fallback:** if no model is reachable, return deterministic results, retrieved evidence and templated narration with clear labeling (inherited `MVP-FR-020`). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-RAG-008 | Model-down fallback: if no model is reachable, return deterministic results, retrieved evidence and templated narration with clear labeling (inherited MVP-FR-020). | P0»
- [ ] Model-down fallback: if no model is reachable, return deterministic results, retrieved evidence and templated narration with clear labeling (inherited MVP-FR-020).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-RAG-010 [P0] SR-RAG-010: RAG evaluation harness built in: retrieval precision/recall@k, MRR/nDCG, groundedness/faithfulness, citation precision, answer relevance, hallucination rate, latency, token cost; regression gates in C

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:572-572` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-RAG-010 | **RAG evaluation harness** built in: retrieval precision/recall@k, MRR/nDCG, groundedness/faithfulness, citation precision, answer relevance, hallucination rate, latency, token cost; regression gates in CI. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-RAG-010 | RAG evaluation harness built in: retrieval precision/recall@k, MRR/nDCG, groundedness/faithfulness, citation precision, answer relevance, hallucination rate, latency, token cost; regression gates in CI. | P0»
- [ ] RAG evaluation harness built in: retrieval precision/recall@k, MRR/nDCG, groundedness/faithfulness, citation precision, answer relevance, hallucination rate, latency, token cost; regression gates in CI.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-SEC-001 [P0] SR-SEC-001: Authentication: OIDC, SAML 2.0, LDAP/AD, SCIM 2.0 provisioning, local break-glass accounts, MFA (TOTP, WebAuthn/FIDO2), scoped API keys, OAuth2 client credentials, mTLS service identities, short-lived

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:824-824` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-SEC-001 | **Authentication:** OIDC, SAML 2.0, LDAP/AD, SCIM 2.0 provisioning, local break-glass accounts, MFA (TOTP, WebAuthn/FIDO2), scoped API keys, OAuth2 client credentials, mTLS service identities, short-lived tokens, session controls. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-SEC-001 | Authentication: OIDC, SAML 2.0, LDAP/AD, SCIM 2.0 provisioning, local break-glass accounts, MFA (TOTP, WebAuthn/FIDO2), scoped API keys, OAuth2 client credentials, mTLS service identities, short-lived tokens, session controls. | P0»
- [ ] Authentication: OIDC, SAML 2.0, LDAP/AD, SCIM 2.0 provisioning, local break-glass accounts, MFA (TOTP, WebAuthn/FIDO2), scoped API keys, OAuth2 client credentials, mTLS service identities, short-lived tokens, session controls.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-SEC-002 [P0] SR-SEC-002: Authorization: RBAC + ABAC + relationship-based (Zanzibar-style) checks + classification-based mandatory access; evaluated by a policy engine (policy-as-code, OPA/Cedar-class) with a test and "what ca

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:825-825` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-SEC-002 | **Authorization:** RBAC + ABAC + relationship-based (Zanzibar-style) checks + classification-based mandatory access; evaluated by a policy engine (policy-as-code, OPA/Cedar-class) with a test and **"what can this user see?" simulation** tool. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-SEC-002 | Authorization: RBAC + ABAC + relationship-based (Zanzibar-style) checks + classification-based mandatory access; evaluated by a policy engine (policy-as-code, OPA/Cedar-class) with a test and "what can this user see?" simulation tool. | P0»
- [ ] Authorization: RBAC + ABAC + relationship-based (Zanzibar-style) checks + classification-based mandatory access; evaluated by a policy engine (policy-as-code, OPA/Cedar-class) with a test and "what can this user see?" simulation tool.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-SEC-003 [P0] SR-SEC-003: Element-level security: policies apply to vertices, edges, properties and derived structures (embeddings, summaries, communities, caches); query-time policy rewriting and result filtering; field maski

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:826-826` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-SEC-003 | **Element-level security:** policies apply to vertices, edges, properties and derived structures (embeddings, summaries, communities, caches); query-time policy rewriting and result filtering; field masking; purpose-based and time-bound (JIT) access; segregation of duties. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-SEC-003 | Element-level security: policies apply to vertices, edges, properties and derived structures (embeddings, summaries, communities, caches); query-time policy rewriting and result filtering; field masking; purpose-based and time-bound (JIT) access; segregation of duties. | P0»
- [ ] Element-level security: policies apply to vertices, edges, properties and derived structures (embeddings, summaries, communities, caches); query-time policy rewriting and result filtering; field masking; purpose-based and time-bound (JIT) access; segregation of duties.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-SEC-004 [P0] SR-SEC-004: Permission-aware ingestion and retrieval: where the source provides ACLs/permissions, the connector ingests and maps them so answers include only what the asking user could access in the source system

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:827-827` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-SEC-004 | **Permission-aware ingestion and retrieval:** where the source provides ACLs/permissions, the connector ingests and maps them so answers include only what the asking user could access in the source system; unmapped ACLs default to deny. This MUST also govern RAG context assembly and community summaries (summaries of restricted content are themselves restricted). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-SEC-004 | Permission-aware ingestion and retrieval: where the source provides ACLs/permissions, the connector ingests and maps them so answers include only what the asking user could access in the source system; unmapped ACLs default to deny. This MUST also govern RAG context assembly and community summaries (summaries of restricted content are themselves restricted). | P0»
- [ ] Permission-aware ingestion and retrieval: where the source provides ACLs/permissions, the connector ingests and maps them so answers include only what the asking user could access in the source system; unmapped ACLs default to deny. This MUST also govern RAG context assembly and community summaries (summaries of restricted content are themselves restricted).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-SEC-006 [P0] SR-SEC-006: Agent identities are first-class principals with least-privilege roles and budgets; agents never inherit a human's full rights implicitly

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:829-829` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-SEC-006 | **Agent identities** are first-class principals with least-privilege roles and budgets; agents never inherit a human's full rights implicitly. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-SEC-006 | Agent identities are first-class principals with least-privilege roles and budgets; agents never inherit a human's full rights implicitly. | P0»
- [ ] Agent identities are first-class principals with least-privilege roles and budgets; agents never inherit a human's full rights implicitly.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-SEC-010 [P0] SR-SEC-010: Encryption: TLS 1.3 externally, mTLS internally; at-rest encryption for all stores; field-level encryption for sensitive properties; KMS/HSM integration (PKCS#11, KMIP, cloud KMS adapters); rotation; 

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:835-835` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-SEC-010 | **Encryption:** TLS 1.3 externally, mTLS internally; at-rest encryption for all stores; field-level encryption for sensitive properties; KMS/HSM integration (PKCS#11, KMIP, cloud KMS adapters); rotation; optional FIPS 140-validated crypto modules. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-SEC-010 | Encryption: TLS 1.3 externally, mTLS internally; at-rest encryption for all stores; field-level encryption for sensitive properties; KMS/HSM integration (PKCS#11, KMIP, cloud KMS adapters); rotation; optional FIPS 140-validated crypto modules. | P0»
- [ ] Encryption: TLS 1.3 externally, mTLS internally; at-rest encryption for all stores; field-level encryption for sensitive properties; KMS/HSM integration (PKCS#11, KMIP, cloud KMS adapters); rotation; optional FIPS 140-validated crypto modules.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-SEC-011 [P0] SR-SEC-011: Secrets: mounted files/secret store only; no secrets in environment variables, images, logs, graph or embeddings; automated secret scanning on ingested content with quarantine

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:836-836` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-SEC-011 | **Secrets:** mounted files/secret store only; no secrets in environment variables, images, logs, graph or embeddings; automated secret scanning on ingested content with quarantine. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-SEC-011 | Secrets: mounted files/secret store only; no secrets in environment variables, images, logs, graph or embeddings; automated secret scanning on ingested content with quarantine. | P0»
- [ ] Secrets: mounted files/secret store only; no secrets in environment variables, images, logs, graph or embeddings; automated secret scanning on ingested content with quarantine.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-SEC-012 [P0] SR-SEC-012: Audit: immutable, hash-chained, signed, exportable (WORM option, SIEM formats); covers authN/Z decisions, config, data access (detail configurable), policy decisions, egress manifests, admin and agent

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:837-837` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-SEC-012 | **Audit:** immutable, hash-chained, signed, exportable (WORM option, SIEM formats); covers authN/Z decisions, config, data access (detail configurable), policy decisions, egress manifests, admin and agent actions; retention configurable. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-SEC-012 | Audit: immutable, hash-chained, signed, exportable (WORM option, SIEM formats); covers authN/Z decisions, config, data access (detail configurable), policy decisions, egress manifests, admin and agent actions; retention configurable. | P0»
- [ ] Audit: immutable, hash-chained, signed, exportable (WORM option, SIEM formats); covers authN/Z decisions, config, data access (detail configurable), policy decisions, egress manifests, admin and agent actions; retention configurable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-SEC-013 [P0] SR-SEC-013: Hardening: non-root containers, read-only root FS, dropped capabilities, seccomp/AppArmor profiles, minimal signed base images, network segmentation, CIS-aligned benchmarks

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:838-838` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-SEC-013 | **Hardening:** non-root containers, read-only root FS, dropped capabilities, seccomp/AppArmor profiles, minimal signed base images, network segmentation, CIS-aligned benchmarks. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-SEC-013 | Hardening: non-root containers, read-only root FS, dropped capabilities, seccomp/AppArmor profiles, minimal signed base images, network segmentation, CIS-aligned benchmarks. | P0»
- [ ] Hardening: non-root containers, read-only root FS, dropped capabilities, seccomp/AppArmor profiles, minimal signed base images, network segmentation, CIS-aligned benchmarks.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-SEC-014 [P0] SR-SEC-014: Supply chain: SBOM (CycloneDX/SPDX) per image and release, VEX, signed images/artifacts (Sigstore/cosign-class), SLSA-aligned provenance, pinned and reproducible builds, license scanning, dependency r

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:839-839` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-SEC-014 | **Supply chain:** SBOM (CycloneDX/SPDX) per image and release, VEX, signed images/artifacts (Sigstore/cosign-class), SLSA-aligned provenance, pinned and reproducible builds, license scanning, dependency review. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-SEC-014 | Supply chain: SBOM (CycloneDX/SPDX) per image and release, VEX, signed images/artifacts (Sigstore/cosign-class), SLSA-aligned provenance, pinned and reproducible builds, license scanning, dependency review. | P0»
- [ ] Supply chain: SBOM (CycloneDX/SPDX) per image and release, VEX, signed images/artifacts (Sigstore/cosign-class), SLSA-aligned provenance, pinned and reproducible builds, license scanning, dependency review.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-SEC-015 [P0] SR-SEC-015: Secure SDLC: threat models (STRIDE + LLM-specific + multi-tenant), SAST/DAST/SCA/fuzzing in CI, annual independent penetration test, vulnerability disclosure program, patch SLAs, security advisories c

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:840-840` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-SEC-015 | **Secure SDLC:** threat models (STRIDE + LLM-specific + multi-tenant), SAST/DAST/SCA/fuzzing in CI, annual independent penetration test, vulnerability disclosure program, patch SLAs, security advisories channel. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-SEC-015 | Secure SDLC: threat models (STRIDE + LLM-specific + multi-tenant), SAST/DAST/SCA/fuzzing in CI, annual independent penetration test, vulnerability disclosure program, patch SLAs, security advisories channel. | P0»
- [ ] Secure SDLC: threat models (STRIDE + LLM-specific + multi-tenant), SAST/DAST/SCA/fuzzing in CI, annual independent penetration test, vulnerability disclosure program, patch SLAs, security advisories channel.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-SEC-016 [P0] SR-SEC-016: Web and API defenses: CSP, CSRF/XSS protections, SSRF guards for connectors and model endpoints, input validation, request size/time limits, DoS and abuse controls

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:841-841` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-SEC-016 | **Web and API defenses:** CSP, CSRF/XSS protections, SSRF guards for connectors and model endpoints, input validation, request size/time limits, DoS and abuse controls. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-SEC-016 | Web and API defenses: CSP, CSRF/XSS protections, SSRF guards for connectors and model endpoints, input validation, request size/time limits, DoS and abuse controls. | P0»
- [ ] Web and API defenses: CSP, CSRF/XSS protections, SSRF guards for connectors and model endpoints, input validation, request size/time limits, DoS and abuse controls.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-SEC-017 [P0] SR-SEC-017: LLM-specific security: prompt-injection and data-exfiltration test corpus, output filtering, tool-permission enforcement, context isolation per tenant/user (aligned with OWASP LLM Top-10 categories)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:842-842` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-SEC-017 | **LLM-specific security:** prompt-injection and data-exfiltration test corpus, output filtering, tool-permission enforcement, context isolation per tenant/user (aligned with OWASP LLM Top-10 categories). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-SEC-017 | LLM-specific security: prompt-injection and data-exfiltration test corpus, output filtering, tool-permission enforcement, context isolation per tenant/user (aligned with OWASP LLM Top-10 categories). | P0»
- [ ] LLM-specific security: prompt-injection and data-exfiltration test corpus, output filtering, tool-permission enforcement, context isolation per tenant/user (aligned with OWASP LLM Top-10 categories).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-TEN-003 [P0] SR-TEN-003: Isolation is enforced at every layer: graph (database/graph-space/namespace per tenant), vector (collection), search (index), relational (schema + row-level security), object (bucket/prefix), event to

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:720-720` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-TEN-003 | Isolation is enforced at **every layer:** graph (database/graph-space/namespace per tenant), vector (collection), search (index), relational (schema + row-level security), object (bucket/prefix), event topics, secrets, KMS keys, caches, logs, backups, exports. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-TEN-003 | Isolation is enforced at every layer: graph (database/graph-space/namespace per tenant), vector (collection), search (index), relational (schema + row-level security), object (bucket/prefix), event topics, secrets, KMS keys, caches, logs, backups, exports. | P0»
- [ ] Isolation is enforced at every layer: graph (database/graph-space/namespace per tenant), vector (collection), search (index), relational (schema + row-level security), object (bucket/prefix), event topics, secrets, KMS keys, caches, logs, backups, exports.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/tenancy/context.py:71`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/context.py#L71-L71), [`packages/eoip/tenancy/isolation.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/isolation.py#L1-L1), [`packages/eoip/tenancy/lifecycle.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/lifecycle.py#L13-L13)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-TEN-004 [P0] SR-TEN-004: Automated cross-tenant penetration suite (every endpoint, job type and plugin hook attempts cross-tenant reads/writes/side-channels) MUST pass in CI and before each release

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:721-721` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-TEN-004 | **Automated cross-tenant penetration suite** (every endpoint, job type and plugin hook attempts cross-tenant reads/writes/side-channels) MUST pass in CI and before each release. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-TEN-004 | Automated cross-tenant penetration suite (every endpoint, job type and plugin hook attempts cross-tenant reads/writes/side-channels) MUST pass in CI and before each release. | P0»
- [ ] Automated cross-tenant penetration suite (every endpoint, job type and plugin hook attempts cross-tenant reads/writes/side-channels) MUST pass in CI and before each release.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/tenancy/__init__.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/__init__.py#L13-L13)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-TEN-005 [P0] SR-TEN-005: Per-tenant keys (envelope encryption; BYOK and hold-your-own-key options), crypto-shredding on tenant deletion

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:722-722` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-TEN-005 | **Per-tenant keys** (envelope encryption; BYOK and hold-your-own-key options), **crypto-shredding** on tenant deletion. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-TEN-005 | Per-tenant keys (envelope encryption; BYOK and hold-your-own-key options), crypto-shredding on tenant deletion. | P0»
- [ ] Per-tenant keys (envelope encryption; BYOK and hold-your-own-key options), crypto-shredding on tenant deletion.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/tenancy/__init__.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/__init__.py#L13-L13), [`packages/eoip/tenancy/isolation.py:38`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/isolation.py#L38-L38), [`packages/eoip/tenancy/lifecycle.py:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/lifecycle.py#L16-L16)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-TEN-008 [P0] SR-TEN-008: Per-tenant everything: ontology extensions, connectors, mappings, model allowlist, egress policy, retention, region, SSO, branding, SLA tier, feature entitlements

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:725-725` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-TEN-008 | **Per-tenant everything:** ontology extensions, connectors, mappings, model allowlist, egress policy, retention, region, SSO, branding, SLA tier, feature entitlements. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-TEN-008 | Per-tenant everything: ontology extensions, connectors, mappings, model allowlist, egress policy, retention, region, SSO, branding, SLA tier, feature entitlements. | P0»
- [ ] Per-tenant everything: ontology extensions, connectors, mappings, model allowlist, egress policy, retention, region, SSO, branding, SLA tier, feature entitlements.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/tenancy/__init__.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/__init__.py#L14-L14)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-UX-001 [P0] SR-UX-001: No mock UI: every screen reads live APIs; hardcoded demo data is allowed only in an explicit, labeled Demo Mode. UI acceptance tests assert real backend calls

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:803-803` (table_row) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-UX-001 | **No mock UI:** every screen reads live APIs; hardcoded demo data is allowed only in an explicit, labeled Demo Mode. UI acceptance tests assert real backend calls. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] tests assert real backend calls. | P0
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-UX-002 [P0] SR-UX-002: Graph visualization at scale: WebGL rendering, level-of-detail and semantic zoom, bounded subgraph fetch, clustering/community collapse, multiple layouts (force, hierarchical, radial, geo), 2D/3D, min

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:804-804` (table_row) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-UX-002 | **Graph visualization at scale:** WebGL rendering, level-of-detail and semantic zoom, bounded subgraph fetch, clustering/community collapse, multiple layouts (force, hierarchical, radial, geo), 2D/3D, minimap, path highlighting, blast-radius overlay; interactive at ≥ 50 k visible elements with LOD, ≥ 5 k fully detailed. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-UX-002 | Graph visualization at scale: WebGL rendering, level-of-detail and semantic zoom, bounded subgraph fetch, clustering/community collapse, multiple layouts (force, hierarchical, radial, geo), 2D/3D, minimap, path highlighting, blast-radius overlay; interactive at ≥ 50 k visible elements with LOD, ≥ 5 k fully detailed. | P0»
- [ ] Graph visualization at scale: WebGL rendering, level-of-detail and semantic zoom, bounded subgraph fetch, clustering/community collapse, multiple layouts (force, hierarchical, radial, geo), 2D/3D, minimap, path highlighting, blast-radius overlay; interactive at ≥ 50 k visible elements with LOD, ≥ 5 k fully detailed.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-UX-004 [P0] SR-UX-004: Honest visual encoding: edge style encodes class and confidence (asserted/derived/inferred/curated); freshness shading; provenance drawer ("show evidence") one click from any element or answer sentenc

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:806-806` (table_row) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-UX-004 | **Honest visual encoding:** edge style encodes class and confidence (asserted/derived/inferred/curated); freshness shading; provenance drawer ("show evidence") one click from any element or answer sentence. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-UX-004 | Honest visual encoding: edge style encodes class and confidence (asserted/derived/inferred/curated); freshness shading; provenance drawer ("show evidence") one click from any element or answer sentence. | P0»
- [ ] Honest visual encoding: edge style encodes class and confidence (asserted/derived/inferred/curated); freshness shading; provenance drawer ("show evidence") one click from any element or answer sentence.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-UX-005 [P0] SR-UX-005: NL console: suggestion cards (SR-NLQ-002), query preview (EOQL + dialect), evidence panel, mode badge (deterministic/narrated/exploratory/report), follow-up chips, investigation canvas that pins entit

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:807-807` (table_row) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-UX-005 | **NL console:** suggestion cards (SR-NLQ-002), query preview (EOQL + dialect), evidence panel, mode badge (deterministic/narrated/exploratory/report), follow-up chips, investigation canvas that pins entities, paths and findings. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-UX-005 | NL console: suggestion cards (SR-NLQ-002), query preview (EOQL + dialect), evidence panel, mode badge (deterministic/narrated/exploratory/report), follow-up chips, investigation canvas that pins entities, paths and findings. | P0»
- [ ] NL console: suggestion cards (SR-NLQ-002), query preview (EOQL + dialect), evidence panel, mode badge (deterministic/narrated/exploratory/report), follow-up chips, investigation canvas that pins entities, paths and findings.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-UX-008 [P0] SR-UX-008: Accessibility: WCAG 2.2 AA, keyboard-first, screen-reader semantics for graph (alt text paths, tabular fallback), reduced-motion, color-blind-safe palettes

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:810-810` (table_row) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-UX-008 | **Accessibility:** WCAG 2.2 AA, keyboard-first, screen-reader semantics for graph (alt text paths, tabular fallback), reduced-motion, color-blind-safe palettes. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-UX-008 | Accessibility: WCAG 2.2 AA, keyboard-first, screen-reader semantics for graph (alt text paths, tabular fallback), reduced-motion, color-blind-safe palettes. | P0»
- [ ] Accessibility: WCAG 2.2 AA, keyboard-first, screen-reader semantics for graph (alt text paths, tabular fallback), reduced-motion, color-blind-safe palettes.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-UX-010 [P0] SR-UX-010: Onboarding: guided setup wizard (connect → profile → map → validate → ask), sample-data sandbox, in-product help, "what can I ask?" explorer driven by the meta-graph

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:812-812` (table_row) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-UX-010 | **Onboarding:** guided setup wizard (connect → profile → map → validate → ask), sample-data sandbox, in-product help, "what can I ask?" explorer driven by the meta-graph. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-UX-010 | Onboarding: guided setup wizard (connect → profile → map → validate → ask), sample-data sandbox, in-product help, "what can I ask?" explorer driven by the meta-graph. | P0»
- [ ] Onboarding: guided setup wizard (connect → profile → map → validate → ask), sample-data sandbox, in-product help, "what can I ask?" explorer driven by the meta-graph.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-UX-011 [P0] SR-UX-011: Destructive-action safety: confirmations with impact preview, undo where possible, dual control for configured classes

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:813-813` (table_row) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-UX-011 | **Destructive-action safety:** confirmations with impact preview, undo where possible, dual control for configured classes. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-UX-011 | Destructive-action safety: confirmations with impact preview, undo where possible, dual control for configured classes. | P0»
- [ ] Destructive-action safety: confirmations with impact preview, undo where possible, dual control for configured classes.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-VDB-001 [P0] SR-VDB-001: Vector Store Port: upsert/delete by ID with metadata, filtered kNN, hybrid (dense + sparse/BM25), namespace-per-tenant, snapshot/restore, index rebuild, embedding-model version tracking

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:227-227` (table_row) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-VDB-001 | **Vector Store Port:** upsert/delete by ID with metadata, filtered kNN, hybrid (dense + sparse/BM25), namespace-per-tenant, snapshot/restore, index rebuild, embedding-model version tracking. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-VDB-001 | Vector Store Port: upsert/delete by ID with metadata, filtered kNN, hybrid (dense + sparse/BM25), namespace-per-tenant, snapshot/restore, index rebuild, embedding-model version tracking. | P0»
- [ ] Vector Store Port: upsert/delete by ID with metadata, filtered kNN, hybrid (dense + sparse/BM25), namespace-per-tenant, snapshot/restore, index rebuild, embedding-model version tracking.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-VDB-002 [P0] SR-VDB-002: Adapters: embedded (FAISS/hnswlib/USearch/LanceDB-class), PostgreSQL pgvector, Qdrant, Milvus, Weaviate, Chroma, OpenSearch/Elasticsearch k-NN, Redis-compatible vector, Vespa, graph-native vector inde

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:228-228` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-VDB-002 | **Adapters:** embedded (FAISS/hnswlib/USearch/LanceDB-class), PostgreSQL pgvector, Qdrant, Milvus, Weaviate, Chroma, OpenSearch/Elasticsearch k-NN, Redis-compatible vector, Vespa, graph-native vector indexes (e.g., Neo4j), plus cloud-managed (Pinecone, Azure AI Search, Vertex AI Vector Search, Atlas Vector Search) under DP-3/4 only. | P0 (embedded, pgvector) / P1 (rest)
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-VDB-002 | Adapters: embedded (FAISS/hnswlib/USearch/LanceDB-class), PostgreSQL pgvector, Qdrant, Milvus, Weaviate, Chroma, OpenSearch/Elasticsearch k-NN, Redis-compatible vector, Vespa, graph-native vector indexes (e.g., Neo4j), plus cloud-managed (Pinecone, Azure AI Search, Vertex AI Vector Search, Atlas Vector Search) under DP-3/4 only. | P0 (embedded, pgvector) / P1 (rest»
- [ ] Adapters: embedded (FAISS/hnswlib/USearch/LanceDB-class), PostgreSQL pgvector, Qdrant, Milvus, Weaviate, Chroma, OpenSearch/Elasticsearch k-NN, Redis-compatible vector, Vespa, graph-native vector indexes (e.g., Neo4j), plus cloud-managed (Pinecone, Azure AI Search, Vertex AI Vector Search, Atlas Vector Search) under DP-3/4 only.
- [ ] P0 (embedded, pgvector) / P1 (rest)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-VDB-005 [P0] SR-VDB-005: Embedding governance: embeddings are derived data; they inherit the classification and access policy of their source, are deleted when the source is erased (§14.3), and are re-generated on model chang

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:231-231` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-VDB-005 | **Embedding governance:** embeddings are derived data; they inherit the classification and access policy of their source, are deleted when the source is erased (§14.3), and are re-generated on model change with versioned side-by-side indexes and cut-over. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-VDB-005 | Embedding governance: embeddings are derived data; they inherit the classification and access policy of their source, are deleted when the source is erased (§14.3), and are re-generated on model change with versioned side-by-side indexes and cut-over. | P0»
- [ ] Embedding governance: embeddings are derived data; they inherit the classification and access policy of their source, are deleted when the source is erased (§14.3), and are re-generated on model change with versioned side-by-side indexes and cut-over.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-VDB-006 [P0] SR-VDB-006: Full-text/search port: BM25 keyword, phrase, fuzzy, facets, highlighting, multilingual analyzers; adapters for embedded engine (Tantivy/SQLite-FTS class), PostgreSQL FTS, OpenSearch/Elasticsearch clas

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:232-232` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-VDB-006 | **Full-text/search port:** BM25 keyword, phrase, fuzzy, facets, highlighting, multilingual analyzers; adapters for embedded engine (Tantivy/SQLite-FTS class), PostgreSQL FTS, OpenSearch/Elasticsearch class. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-VDB-006 | Full-text/search port: BM25 keyword, phrase, fuzzy, facets, highlighting, multilingual analyzers; adapters for embedded engine (Tantivy/SQLite-FTS class), PostgreSQL FTS, OpenSearch/Elasticsearch class. | P0»
- [ ] Full-text/search port: BM25 keyword, phrase, fuzzy, facets, highlighting, multilingual analyzers; adapters for embedded engine (Tantivy/SQLite-FTS class), PostgreSQL FTS, OpenSearch/Elasticsearch class.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-VDB-007 [P0] SR-VDB-007: A deployment with no vector store MUST still pass the core NL acceptance suite using graph + full-text retrieval (degraded semantic recall is acceptable and MUST be signalled)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:233-233` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-VDB-007 | A deployment with **no vector store** MUST still pass the core NL acceptance suite using graph + full-text retrieval (degraded semantic recall is acceptable and MUST be signalled). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-VDB-007 | A deployment with no vector store MUST still pass the core NL acceptance suite using graph + full-text retrieval (degraded semantic recall is acceptable and MUST be signalled). | P0»
- [ ] A deployment with no vector store MUST still pass the core NL acceptance suite using graph + full-text retrieval (degraded semantic recall is acceptable and MUST be signalled).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-WL-002 [P0] SR-WL-002: Domain and identity: custom domains/CNAMEs, tenant-supplied TLS certs, branded login/SSO pages, branded transactional email, branded PDF/DOCX/PPTX/HTML reports

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:734-734` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-WL-002 | **Domain and identity:** custom domains/CNAMEs, tenant-supplied TLS certs, branded login/SSO pages, branded transactional email, branded PDF/DOCX/PPTX/HTML reports. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-WL-002 | Domain and identity: custom domains/CNAMEs, tenant-supplied TLS certs, branded login/SSO pages, branded transactional email, branded PDF/DOCX/PPTX/HTML reports. | P0»
- [ ] Domain and identity: custom domains/CNAMEs, tenant-supplied TLS certs, branded login/SSO pages, branded transactional email, branded PDF/DOCX/PPTX/HTML reports.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-WL-003 [P0] SR-WL-003: Terminology and persona white-labelling: tenant renames concepts (SR-ONT-007) and names/styles the AI assistant (name, tone, avatar, greeting) without altering safety behavior

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:735-735` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-WL-003 | **Terminology and persona white-labelling:** tenant renames concepts (SR-ONT-007) and names/styles the AI assistant (name, tone, avatar, greeting) without altering safety behavior. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-WL-003 | Terminology and persona white-labelling: tenant renames concepts (SR-ONT-007) and names/styles the AI assistant (name, tone, avatar, greeting) without altering safety behavior. | P0»
- [ ] Terminology and persona white-labelling: tenant renames concepts (SR-ONT-007) and names/styles the AI assistant (name, tone, avatar, greeting) without altering safety behavior.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/branding/terminology.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/branding/terminology.py#L1-L1), [`packages/eoip/branding/theme.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/branding/theme.py#L10-L10)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-WL-006 [P0] SR-WL-006: Localization packs: UI strings, date/number formats, RTL, glossary translation; partner-supplied language packs

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:738-738` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-WL-006 | **Localization packs:** UI strings, date/number formats, RTL, glossary translation; partner-supplied language packs. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-WL-006 | Localization packs: UI strings, date/number formats, RTL, glossary translation; partner-supplied language packs. | P0»
- [ ] Localization packs: UI strings, date/number formats, RTL, glossary translation; partner-supplied language packs.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/branding/localization.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/branding/localization.py#L1-L1)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-WL-007 [P0] SR-WL-007: Custom legal and onboarding content: terms, privacy notices, welcome tours, help links

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:739-739` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-WL-007 | **Custom legal and onboarding content:** terms, privacy notices, welcome tours, help links. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-WL-007 | Custom legal and onboarding content: terms, privacy notices, welcome tours, help links. | P0»
- [ ] Custom legal and onboarding content: terms, privacy notices, welcome tours, help links.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/branding/content.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/branding/content.py#L1-L1)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-007 [P1] SR-AGT-007: Agent registry & marketplace: discover, install, evaluate and certify agents; signed packages; capability declarations

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:687-687` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-007 | **Agent registry & marketplace:** discover, install, evaluate and certify agents; signed packages; capability declarations. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-007 | Agent registry & marketplace: discover, install, evaluate and certify agents; signed packages; capability declarations. | P1»
- [ ] Agent registry & marketplace: discover, install, evaluate and certify agents; signed packages; capability declarations.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-008 [P1] SR-AGT-008: Multi-agent orchestration: planner/critic/worker patterns, event-driven coordination, shared evidence blackboard, XAI trace per run

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:688-688` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-008 | **Multi-agent orchestration:** planner/critic/worker patterns, event-driven coordination, shared evidence blackboard, XAI trace per run. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-008 | Multi-agent orchestration: planner/critic/worker patterns, event-driven coordination, shared evidence blackboard, XAI trace per run. | P1»
- [ ] Multi-agent orchestration: planner/critic/worker patterns, event-driven coordination, shared evidence blackboard, XAI trace per run.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-010 [P1] SR-AGT-010: Specialist agent catalog (starting set inherited from the codebase, plus new): DataQuality, OntologyReview, ConnectorDiagnosis, DocumentationFreshness, EvidenceVerification, ArchitectureConformance, Q

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:690-690` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-010 | **Specialist agent catalog** (starting set inherited from the codebase, plus new): DataQuality, OntologyReview, ConnectorDiagnosis, DocumentationFreshness, EvidenceVerification, ArchitectureConformance, QueryOptimization, GraphInvestigator, KnowledgeCurator, ChangeImpact, IncidentInvestigation; new: ComplianceMapper, ImpactSimulator, ExpertFinder, KnowledgeDebt, ReportWriter, OntologyInduction, ThreatPathAnalyst. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-010 | Specialist agent catalog (starting set inherited from the codebase, plus new): DataQuality, OntologyReview, ConnectorDiagnosis, DocumentationFreshness, EvidenceVerification, ArchitectureConformance, QueryOptimization, GraphInvestigator, KnowledgeCurator, ChangeImpact, IncidentInvestigation; new: ComplianceMapper, ImpactSimulator, ExpertFinder, KnowledgeDebt, Report»
- [ ] Specialist agent catalog (starting set inherited from the codebase, plus new): DataQuality, OntologyReview, ConnectorDiagnosis, DocumentationFreshness, EvidenceVerification, ArchitectureConformance, QueryOptimization, GraphInvestigator, KnowledgeCurator, ChangeImpact, IncidentInvestigation; new: ComplianceMapper, ImpactSimulator, ExpertFinder, KnowledgeDebt, ReportWriter, OntologyInduction, Threat
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-011 [P1] SR-AGT-011: RPA/workflow hooks: approved agent outputs may trigger tickets, PR comments, notifications or runbook steps through connectors, always with human approval unless policy allows

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:691-691` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-011 | **RPA/workflow hooks:** approved agent outputs may trigger tickets, PR comments, notifications or runbook steps through connectors, always with human approval unless policy allows. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-011 | RPA/workflow hooks: approved agent outputs may trigger tickets, PR comments, notifications or runbook steps through connectors, always with human approval unless policy allows. | P1»
- [ ] RPA/workflow hooks: approved agent outputs may trigger tickets, PR comments, notifications or runbook steps through connectors, always with human approval unless policy allows.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-020 [P1] SR-AGT-020: Continuous sync and change detection: the brain updates on source change; users can watch an entity, pattern or question and get alerts when answers change ("continuous queries")

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:697-697` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-020 | **Continuous sync and change detection:** the brain updates on source change; users can **watch** an entity, pattern or question and get alerts when answers change ("continuous queries"). | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-020 | Continuous sync and change detection: the brain updates on source change; users can watch an entity, pattern or question and get alerts when answers change ("continuous queries"). | P1»
- [ ] Continuous sync and change detection: the brain updates on source change; users can watch an entity, pattern or question and get alerts when answers change ("continuous queries").
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-021 [P1] SR-AGT-021: Drift and conformance detection: docs vs code, architecture vs deployment, ontology vs data, policy vs access, declared vs observed dependencies

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:698-698` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-021 | **Drift and conformance detection:** docs vs code, architecture vs deployment, ontology vs data, policy vs access, declared vs observed dependencies. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-021 | Drift and conformance detection: docs vs code, architecture vs deployment, ontology vs data, policy vs access, declared vs observed dependencies. | P1»
- [ ] Drift and conformance detection: docs vs code, architecture vs deployment, ontology vs data, policy vs access, declared vs observed dependencies.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-023 [P1] SR-AGT-023: Knowledge-debt and bus-factor analysis: single-owner components, orphaned systems, undocumented critical dependencies

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:700-700` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-023 | **Knowledge-debt and bus-factor analysis:** single-owner components, orphaned systems, undocumented critical dependencies. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-023 | Knowledge-debt and bus-factor analysis: single-owner components, orphaned systems, undocumented critical dependencies. | P1»
- [ ] Knowledge-debt and bus-factor analysis: single-owner components, orphaned systems, undocumented critical dependencies.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-024 [P1] SR-AGT-024: Expert finder and routing: who knows/owns/changed what, with identity-resolved evidence; "who should I ask?"

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:701-701` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-024 | **Expert finder and routing:** who knows/owns/changed what, with identity-resolved evidence; "who should I ask?". | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-024 | Expert finder and routing: who knows/owns/changed what, with identity-resolved evidence; "who should I ask?". | P1»
- [ ] Expert finder and routing: who knows/owns/changed what, with identity-resolved evidence; "who should I ask?".
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-025 [P1] SR-AGT-025: Risk scoring: change risk = blast radius × fragility × test coverage × recent-incident correlation; surfaced in PR/change-request bots

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:702-702` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-025 | **Risk scoring:** change risk = blast radius × fragility × test coverage × recent-incident correlation; surfaced in PR/change-request bots. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-025 | Risk scoring: change risk = blast radius × fragility × test coverage × recent-incident correlation; surfaced in PR/change-request bots. | P1»
- [ ] Risk scoring: change risk = blast radius × fragility × test coverage × recent-incident correlation; surfaced in PR/change-request bots.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-027 [P1] SR-AGT-027: Digest and briefing: scheduled personalized briefings (what changed, what's at risk, open items) per role

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:704-704` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-027 | **Digest and briefing:** scheduled personalized briefings (what changed, what's at risk, open items) per role. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-027 | Digest and briefing: scheduled personalized briefings (what changed, what's at risk, open items) per role. | P1»
- [ ] Digest and briefing: scheduled personalized briefings (what changed, what's at risk, open items) per role.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ARC-008 [P1] SR-ARC-008: Hybrid logical clocks / bitemporal fields on all mutations (valid time, transaction time) so federated and replayed data order deterministically

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:169-169` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ARC-008 | **Hybrid logical clocks / bitemporal fields** on all mutations (valid time, transaction time) so federated and replayed data order deterministically. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ARC-008 | Hybrid logical clocks / bitemporal fields on all mutations (valid time, transaction time) so federated and replayed data order deterministically. | P1»
- [ ] Hybrid logical clocks / bitemporal fields on all mutations (valid time, transaction time) so federated and replayed data order deterministically.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-COM-006 [P1] SR-COM-006: Partner program: certification tracks (implementer, connector developer, ontology engineer), partner portal, deal registration, co-marketing assets

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:1005-1005` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-COM-006 | **Partner program:** certification tracks (implementer, connector developer, ontology engineer), partner portal, deal registration, co-marketing assets. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-COM-006 | Partner program: certification tracks (implementer, connector developer, ontology engineer), partner portal, deal registration, co-marketing assets. | P1»
- [ ] Partner program: certification tracks (implementer, connector developer, ontology engineer), partner portal, deal registration, co-marketing assets.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-COM-008 [P1] SR-COM-008: Sales artifacts: datasheets per module and industry, battlecards, demo environments, reference architectures, case-study templates

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:1007-1007` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-COM-008 | **Sales artifacts:** datasheets per module and industry, battlecards, demo environments, reference architectures, case-study templates. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-COM-008 | Sales artifacts: datasheets per module and industry, battlecards, demo environments, reference architectures, case-study templates. | P1»
- [ ] Sales artifacts: datasheets per module and industry, battlecards, demo environments, reference architectures, case-study templates.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-CON-012 [P1] SR-CON-012: Provide reference adapters for the three hyperscalers' object storage, KMS, identity federation and managed graph/search where available (e.g., Amazon Neptune/OpenSearch/S3/KMS, Azure Blob/Key Vault/E

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:126-126` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CON-012 | Provide reference adapters for the three hyperscalers' object storage, KMS, identity federation and managed graph/search where available (e.g., Amazon Neptune/OpenSearch/S3/KMS, Azure Blob/Key Vault/Entra ID/Cosmos Gremlin, GCP GCS/KMS/Cloud Identity). | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CON-012 | Provide reference adapters for the three hyperscalers' object storage, KMS, identity federation and managed graph/search where available (e.g., Amazon Neptune/OpenSearch/S3/KMS, Azure Blob/Key Vault/Entra ID/Cosmos Gremlin, GCP GCS/KMS/Cloud Identity). | P1»
- [ ] Provide reference adapters for the three hyperscalers' object storage, KMS, identity federation and managed graph/search where available (e.g., Amazon Neptune/OpenSearch/S3/KMS, Azure Blob/Key Vault/Entra ID/Cosmos Gremlin, GCP GCS/KMS/Cloud Identity).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/egress/provider.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/provider.py#L15-L15), [`packages/eoip/egress/vault.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/vault.py#L9-L9)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-CON-013 [P1] SR-CON-013: Provide infrastructure-as-code modules (Terraform/OpenTofu, Helm) for DP-3/DP-4 with security-hardened defaults, private networking, and no public endpoints by default

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:127-127` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CON-013 | Provide infrastructure-as-code modules (Terraform/OpenTofu, Helm) for DP-3/DP-4 with security-hardened defaults, private networking, and no public endpoints by default. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CON-013 | Provide infrastructure-as-code modules (Terraform/OpenTofu, Helm) for DP-3/DP-4 with security-hardened defaults, private networking, and no public endpoints by default. | P1»
- [ ] Provide infrastructure-as-code modules (Terraform/OpenTofu, Helm) for DP-3/DP-4 with security-hardened defaults, private networking, and no public endpoints by default.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

