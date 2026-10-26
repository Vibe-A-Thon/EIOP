# EPIC-SUPER-NOTRUN-05: EOIP-engg-doc-pkg/super-requirements.md · tests_not_executed

*Tests are mapped/referenced but none ran in the audit (excluded or not collected).* 3 tasks, ~3.0 h, priorities {'P2': 2, 'P3': 1}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-SR-QRY-010 [P2] SR-QRY-010: Federated query across backends and sites with per-source policy enforcement and partial results

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:321-321` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QRY-010 | **Federated query** across backends and sites with per-source policy enforcement and partial results. | P2
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QRY-010 | Federated query across backends and sites with per-source policy enforcement and partial results. | P2»
- [ ] Federated query across backends and sites with per-source policy enforcement and partial results.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-VDB-004 [P2] SR-VDB-004: Multi-vector and multimodal: text, code, table, image, audio-transcript, and node/graph embeddings; late-interaction (ColBERT-style) and sparse-learned (SPLADE-style) as optional retrievers

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:230-230` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-VDB-004 | **Multi-vector and multimodal:** text, code, table, image, audio-transcript, and node/graph embeddings; late-interaction (ColBERT-style) and sparse-learned (SPLADE-style) as optional retrievers. | P2
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-VDB-004 | Multi-vector and multimodal: text, code, table, image, audio-transcript, and node/graph embeddings; late-interaction (ColBERT-style) and sparse-learned (SPLADE-style) as optional retrievers. | P2»
- [ ] Multi-vector and multimodal: text, code, table, image, audio-transcript, and node/graph embeddings; late-interaction (ColBERT-style) and sparse-learned (SPLADE-style) as optional retrievers.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-029 [P3] SR-AGT-029: Digital-twin mode: model processes/assets/organizations as simulatable graphs for scenario planning (links to SR-NLQ-014)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:706-706` (table_row) · **Type:** AI · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-029 | **Digital-twin mode:** model processes/assets/organizations as simulatable graphs for scenario planning (links to SR-NLQ-014). | P3
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-029 | Digital-twin mode: model processes/assets/organizations as simulatable graphs for scenario planning (links to SR-NLQ-014). | P3»
- [ ] Digital-twin mode: model processes/assets/organizations as simulatable graphs for scenario planning (links to SR-NLQ-014).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

