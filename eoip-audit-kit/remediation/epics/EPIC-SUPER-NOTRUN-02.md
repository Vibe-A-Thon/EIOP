# EPIC-SUPER-NOTRUN-02: EOIP-engg-doc-pkg/super-requirements.md · tests_not_executed

*Tests are mapped/referenced but none ran in the audit (excluded or not collected).* 60 tasks, ~61.0 h, priorities {'P0': 60}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-SR-ING-006 [P0] SR-ING-006: Streaming and batch share one pipeline: the same stages and mapping specs serve both; back-pressure and priority lanes per tenant

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:350-350` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-006 | **Streaming and batch share one pipeline:** the same stages and mapping specs serve both; back-pressure and priority lanes per tenant. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-006 | Streaming and batch share one pipeline: the same stages and mapping specs serve both; back-pressure and priority lanes per tenant. | P0»
- [ ] Streaming and batch share one pipeline: the same stages and mapping specs serve both; back-pressure and priority lanes per tenant.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-007 [P0] SR-ING-007: Large-JSON handling: streaming parse (never load whole file), gz/zstd/archive support, malformed-record quarantine with line/offset pointers, numeric precision and Unicode/timezone normalization, bina

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:351-351` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-007 | **Large-JSON handling:** streaming parse (never load whole file), gz/zstd/archive support, malformed-record quarantine with line/offset pointers, numeric precision and Unicode/timezone normalization, binary blob offload. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-007 | Large-JSON handling: streaming parse (never load whole file), gz/zstd/archive support, malformed-record quarantine with line/offset pointers, numeric precision and Unicode/timezone normalization, binary blob offload. | P0»
- [ ] Large-JSON handling: streaming parse (never load whole file), gz/zstd/archive support, malformed-record quarantine with line/offset pointers, numeric precision and Unicode/timezone normalization, binary blob offload.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-011 [P0] SR-ING-011: Entity detection: record types from top-level arrays/envelopes/discriminator fields; nested objects classified as embedded value, child entity, or reference using a scored heuristic (key presence, siz

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:380-380` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-011 | **Entity detection:** record types from top-level arrays/envelopes/discriminator fields; nested objects classified as *embedded value*, *child entity*, or *reference* using a scored heuristic (key presence, size, reuse across parents, naming, user override). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-011 | Entity detection: record types from top-level arrays/envelopes/discriminator fields; nested objects classified as embedded value, child entity, or reference using a scored heuristic (key presence, size, reuse across parents, naming, user override). | P0»
- [ ] Entity detection: record types from top-level arrays/envelopes/discriminator fields; nested objects classified as embedded value, child entity, or reference using a scored heuristic (key presence, size, reuse across parents, naming, user override).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-014 [P0] SR-ING-014: Relationship discovery — statistical: inclusion-dependency and value-overlap discovery across datasets (MinHash/LSH containment for scale), name and embedding-based schema matching, co-occurrence, tem

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:383-383` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-014 | **Relationship discovery — statistical:** inclusion-dependency and value-overlap discovery across datasets (MinHash/LSH containment for scale), name and embedding-based schema matching, co-occurrence, temporal proximity, co-change coupling, mention extraction in text (entity linking). | P0 (value overlap) / P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-014 | Relationship discovery — statistical: inclusion-dependency and value-overlap discovery across datasets (MinHash/LSH containment for scale), name and embedding-based schema matching, co-occurrence, temporal proximity, co-change coupling, mention extraction in text (entity linking). | P0 (value overlap) / P1»
- [ ] Relationship discovery — statistical: inclusion-dependency and value-overlap discovery across datasets (MinHash/LSH containment for scale), name and embedding-based schema matching, co-occurrence, temporal proximity, co-change coupling, mention extraction in text (entity linking).
- [ ] P0 (value overlap) / P1
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ingest/profile.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ingest/profile.py#L24-L24)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-015 [P0] SR-ING-015: Relationship discovery — operational: service-call edges from traces/logs, config references (env var → secret → account), IaC dependency edges, build/runtime dependencies from SBOM and lockfiles, cod

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:384-384` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-015 | **Relationship discovery — operational:** service-call edges from traces/logs, config references (env var → secret → account), IaC dependency edges, build/runtime dependencies from SBOM and lockfiles, code call/import graphs (tree-sitter and SCIP/LSIF-class indexers), SQL lineage parsing, access-log derived usage edges. | P0 (engineering set) / P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-015 | Relationship discovery — operational: service-call edges from traces/logs, config references (env var → secret → account), IaC dependency edges, build/runtime dependencies from SBOM and lockfiles, code call/import graphs (tree-sitter and SCIP/LSIF-class indexers), SQL lineage parsing, access-log derived usage edges. | P0 (engineering set) / P1»
- [ ] Relationship discovery — operational: service-call edges from traces/logs, config references (env var → secret → account), IaC dependency edges, build/runtime dependencies from SBOM and lockfiles, code call/import graphs (tree-sitter and SCIP/LSIF-class indexers), SQL lineage parsing, access-log derived usage edges.
- [ ] P0 (engineering set) / P1
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-ING-019 [P0] SR-ING-019: Mapping DSL: declarative, versioned, diff-able mappings (YAML/JSON) with RML/R2RML and JSON-LD @context import/export; generated by inference, editable by humans, testable on samples

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:388-388` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-019 | **Mapping DSL:** declarative, versioned, diff-able mappings (YAML/JSON) with RML/R2RML and JSON-LD `@context` import/export; generated by inference, editable by humans, testable on samples. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-019 | Mapping DSL: declarative, versioned, diff-able mappings (YAML/JSON) with RML/R2RML and JSON-LD @context import/export; generated by inference, editable by humans, testable on samples. | P0»
- [ ] Mapping DSL: declarative, versioned, diff-able mappings (YAML/JSON) with RML/R2RML and JSON-LD @context import/export; generated by inference, editable by humans, testable on samples.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-020 [P0] SR-ING-020: Schema drift handling: new/changed/removed fields trigger drift events, auto-compatible mapping updates when safe, and steward review when not; mappings are pinned per run for reproducibility

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:389-389` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-020 | **Schema drift handling:** new/changed/removed fields trigger drift events, auto-compatible mapping updates when safe, and steward review when not; mappings are pinned per run for reproducibility. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-020 | Schema drift handling: new/changed/removed fields trigger drift events, auto-compatible mapping updates when safe, and steward review when not; mappings are pinned per run for reproducibility. | P0»
- [ ] Schema drift handling: new/changed/removed fields trigger drift events, auto-compatible mapping updates when safe, and steward review when not; mappings are pinned per run for reproducibility.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ingest/profile.py:128`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ingest/profile.py#L128-L128)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-030 [P0] SR-ING-030: Deterministic rules first (exact keys, normalized emails/IDs), then probabilistic (blocking via sorted-neighborhood/canopy/LSH; pairwise similarity with string/phonetic/numeric/date/embedding features

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:414-414` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-030 | Deterministic rules first (exact keys, normalized emails/IDs), then probabilistic (blocking via sorted-neighborhood/canopy/LSH; pairwise similarity with string/phonetic/numeric/date/embedding features; Fellegi–Sunter-class scoring and/or trained classifiers). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-030 | Deterministic rules first (exact keys, normalized emails/IDs), then probabilistic (blocking via sorted-neighborhood/canopy/LSH; pairwise similarity with string/phonetic/numeric/date/embedding features; Fellegi–Sunter-class scoring and/or trained classifiers). | P0»
- [ ] Deterministic rules first (exact keys, normalized emails/IDs), then probabilistic (blocking via sorted-neighborhood/canopy/LSH; pairwise similarity with string/phonetic/numeric/date/embedding features; Fellegi–Sunter-class scoring and/or trained classifiers).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-032 [P0] SR-ING-032: Every merge is explainable, reversible (unmerge), audited; three bands (auto-merge / human review / reject) with tenant-set thresholds and an active-learning review queue

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:416-416` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-032 | Every merge is **explainable, reversible (unmerge), audited**; three bands (auto-merge / human review / reject) with tenant-set thresholds and an active-learning review queue. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-032 | Every merge is explainable, reversible (unmerge), audited; three bands (auto-merge / human review / reject) with tenant-set thresholds and an active-learning review queue. | P0»
- [ ] Every merge is explainable, reversible (unmerge), audited; three bands (auto-merge / human review / reject) with tenant-set thresholds and an active-learning review queue.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-033 [P0] SR-ING-033: Cross-source ID crosswalk persisted as first-class graph structure (SAMEAS with confidence and evidence) so aliases resolve at query time

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:417-417` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-033 | **Cross-source ID crosswalk** persisted as first-class graph structure (`SAME_AS` with confidence and evidence) so aliases resolve at query time. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-033 | Cross-source ID crosswalk persisted as first-class graph structure (SAME_AS with confidence and evidence) so aliases resolve at query time. | P0»
- [ ] Cross-source ID crosswalk persisted as first-class graph structure (SAME_AS with confidence and evidence) so aliases resolve at query time.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-040 [P0] SR-ING-040: Derived graphs are computed incrementally from mutation events; full rebuild MUST be possible and verified equivalent to the incremental result

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:440-440` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-040 | Derived graphs are computed **incrementally** from mutation events; full rebuild MUST be possible and verified equivalent to the incremental result. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-040 | Derived graphs are computed incrementally from mutation events; full rebuild MUST be possible and verified equivalent to the incremental result. | P0»
- [ ] Derived graphs are computed incrementally from mutation events; full rebuild MUST be possible and verified equivalent to the incremental result.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-042 [P0] SR-ING-042: Traversal-first retrieval (no embeddings required) is the baseline retrieval mode; embeddings enhance recall but are never prerequisite (consistent with SR-CON-005)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:442-442` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-042 | **Traversal-first retrieval** (no embeddings required) is the baseline retrieval mode; embeddings enhance recall but are never prerequisite (consistent with SR-CON-005). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-042 | Traversal-first retrieval (no embeddings required) is the baseline retrieval mode; embeddings enhance recall but are never prerequisite (consistent with SR-CON-005). | P0»
- [ ] Traversal-first retrieval (no embeddings required) is the baseline retrieval mode; embeddings enhance recall but are never prerequisite (consistent with SR-CON-005).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-050 [P0] SR-ING-050: Validation rules with severities (INFO/WARN/ERROR/BLOCKER), remediation suggestions, quarantine with replay, and a data-quality scorecard (completeness, freshness, uniqueness, consistency, confidence 

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:449-449` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-050 | Validation rules with severities (`INFO/WARN/ERROR/BLOCKER`), remediation suggestions, quarantine with replay, and a data-quality scorecard (completeness, freshness, uniqueness, consistency, confidence distribution) per source and per domain. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-050 | Validation rules with severities (INFO/WARN/ERROR/BLOCKER), remediation suggestions, quarantine with replay, and a data-quality scorecard (completeness, freshness, uniqueness, consistency, confidence distribution) per source and per domain. | P0»
- [ ] Validation rules with severities (INFO/WARN/ERROR/BLOCKER), remediation suggestions, quarantine with replay, and a data-quality scorecard (completeness, freshness, uniqueness, consistency, confidence distribution) per source and per domain.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-051 [P0] SR-ING-051: Freshness SLOs per connector with alerting and a user-visible "knowledge age" on every answer

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:450-450` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-051 | **Freshness SLOs** per connector with alerting and a user-visible "knowledge age" on every answer. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-051 | Freshness SLOs per connector with alerting and a user-visible "knowledge age" on every answer. | P0»
- [ ] Freshness SLOs per connector with alerting and a user-visible "knowledge age" on every answer.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-052 [P0] SR-ING-052: Idempotency tests: re-running an ingestion produces zero net graph change; interrupted runs resume without duplicates (restart-safe)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:451-451` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-052 | **Idempotency tests:** re-running an ingestion produces zero net graph change; interrupted runs resume without duplicates (restart-safe). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-052 | Idempotency tests: re-running an ingestion produces zero net graph change; interrupted runs resume without duplicates (restart-safe). | P0»
- [ ] Idempotency tests: re-running an ingestion produces zero net graph change; interrupted runs resume without duplicates (restart-safe).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-053 [P0] SR-ING-053: Reconciliation reports (source counts vs graph counts, orphan edges, dangling references) on schedule

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:452-452` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-053 | **Reconciliation reports** (source counts vs graph counts, orphan edges, dangling references) on schedule. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-053 | Reconciliation reports (source counts vs graph counts, orphan edges, dangling references) on schedule. | P0»
- [ ] Reconciliation reports (source counts vs graph counts, orphan edges, dangling references) on schedule.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-060 [P0] SR-ING-060: Hostile-input posture: parsers sandboxed; zip-bomb/path-traversal/XXE/deserialization defenses; file-type verification; size/time limits

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:467-467` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-060 | **Hostile-input posture:** parsers sandboxed; zip-bomb/path-traversal/XXE/deserialization defenses; file-type verification; size/time limits. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-060 | Hostile-input posture: parsers sandboxed; zip-bomb/path-traversal/XXE/deserialization defenses; file-type verification; size/time limits. | P0»
- [ ] Hostile-input posture: parsers sandboxed; zip-bomb/path-traversal/XXE/deserialization defenses; file-type verification; size/time limits.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-061 [P0] SR-ING-061: Indirect prompt injection defense: ingested text is data, never instructions; extracted passages are fenced, scanned and flagged before any LLM sees them

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:468-468` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-061 | **Indirect prompt injection defense:** ingested text is data, never instructions; extracted passages are fenced, scanned and flagged before any LLM sees them. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-061 | Indirect prompt injection defense: ingested text is data, never instructions; extracted passages are fenced, scanned and flagged before any LLM sees them. | P0»
- [ ] Indirect prompt injection defense: ingested text is data, never instructions; extracted passages are fenced, scanned and flagged before any LLM sees them.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-070 [P0] SR-ING-070: Export formats: JSON/NDJSON, CSV, Parquet, GraphML, GEXF, GraphSON, openCypher bulk CSV, RDF (Turtle, N-Quads, JSON-LD, RDF-star), DOT/Mermaid, Markdown vault, interactive HTML; full-tenant export bun

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:474-474` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-070 | Export formats: JSON/NDJSON, CSV, Parquet, GraphML, GEXF, GraphSON, openCypher bulk CSV, RDF (Turtle, N-Quads, JSON-LD, RDF-star), DOT/Mermaid, Markdown vault, interactive HTML; full-tenant export bundle (data + ontology + mappings + config + audit). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-070 | Export formats: JSON/NDJSON, CSV, Parquet, GraphML, GEXF, GraphSON, openCypher bulk CSV, RDF (Turtle, N-Quads, JSON-LD, RDF-star), DOT/Mermaid, Markdown vault, interactive HTML; full-tenant export bundle (data + ontology + mappings + config + audit). | P0»
- [ ] Export formats: JSON/NDJSON, CSV, Parquet, GraphML, GEXF, GraphSON, openCypher bulk CSV, RDF (Turtle, N-Quads, JSON-LD, RDF-star), DOT/Mermaid, Markdown vault, interactive HTML; full-tenant export bundle (data + ontology + mappings + config + audit).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-LLM-001 [P0] SR-LLM-001: Model Provider Port for chat/completion, structured output (grammar/JSON-schema constrained), tool calling, embeddings, reranking, vision/OCR, speech; capability negotiation (context length, modalitie

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:604-604` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-001 | **Model Provider Port** for chat/completion, structured output (grammar/JSON-schema constrained), tool calling, embeddings, reranking, vision/OCR, speech; capability negotiation (context length, modalities, tools, determinism). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-001 | Model Provider Port for chat/completion, structured output (grammar/JSON-schema constrained), tool calling, embeddings, reranking, vision/OCR, speech; capability negotiation (context length, modalities, tools, determinism). | P0»
- [ ] Model Provider Port for chat/completion, structured output (grammar/JSON-schema constrained), tool calling, embeddings, reranking, vision/OCR, speech; capability negotiation (context length, modalities, tools, determinism).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-LLM-002 [P0] SR-LLM-002: Local/self-hosted by default. Adapters for local runtimes (vLLM-, SGLang-, llama.cpp-, Ollama-, TGI-, ONNX Runtime-, OpenVINO-, TensorRT-LLM-class). No external provider adapter is active until explic

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:605-605` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-002 | **Local/self-hosted by default.** Adapters for local runtimes (vLLM-, SGLang-, llama.cpp-, Ollama-, TGI-, ONNX Runtime-, OpenVINO-, TensorRT-LLM-class). **No external provider adapter is active until explicitly enabled by an authorized tenant administrator** (§10.2). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-002 | Local/self-hosted by default. Adapters for local runtimes (vLLM-, SGLang-, llama.cpp-, Ollama-, TGI-, ONNX Runtime-, OpenVINO-, TensorRT-LLM-class). No external provider adapter is active until explicitly enabled by an authorized tenant administrator (§10.2). | P0»
- [ ] Local/self-hosted by default. Adapters for local runtimes (vLLM-, SGLang-, llama.cpp-, Ollama-, TGI-, ONNX Runtime-, OpenVINO-, TensorRT-LLM-class). No external provider adapter is active until explicitly enabled by an authorized tenant administrator (§10.2).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-LLM-003 [P0] SR-LLM-003: Model registry: per model — source, hash, license terms (open-weight licenses differ and some restrict commercial redistribution), intended tasks, hardware profile, evaluation scores, approval status;

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:606-606` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-003 | **Model registry:** per model — source, hash, license terms (open-weight licenses differ and some restrict commercial redistribution), intended tasks, hardware profile, evaluation scores, approval status; offline model bundles with signature verification. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-003 | Model registry: per model — source, hash, license terms (open-weight licenses differ and some restrict commercial redistribution), intended tasks, hardware profile, evaluation scores, approval status; offline model bundles with signature verification. | P0»
- [ ] Model registry: per model — source, hash, license terms (open-weight licenses differ and some restrict commercial redistribution), intended tasks, hardware profile, evaluation scores, approval status; offline model bundles with signature verification.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-LLM-004 [P0] SR-LLM-004: Task-based routing: small/fast models for classification, extraction and routing; larger models for synthesis; fallbacks and circuit breakers; per-tenant model allowlists

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:607-607` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-004 | **Task-based routing:** small/fast models for classification, extraction and routing; larger models for synthesis; fallbacks and circuit breakers; per-tenant model allowlists. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-004 | Task-based routing: small/fast models for classification, extraction and routing; larger models for synthesis; fallbacks and circuit breakers; per-tenant model allowlists. | P0»
- [ ] Task-based routing: small/fast models for classification, extraction and routing; larger models for synthesis; fallbacks and circuit breakers; per-tenant model allowlists.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-LLM-005 [P0] SR-LLM-005: Hardware reference configurations (CPU-only small model; single-GPU; multi-GPU; air-gapped appliance) with sizing guidance, quantization options, throughput/latency benchmarks per release

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:608-608` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-005 | **Hardware reference configurations** (CPU-only small model; single-GPU; multi-GPU; air-gapped appliance) with sizing guidance, quantization options, throughput/latency benchmarks per release. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-005 | Hardware reference configurations (CPU-only small model; single-GPU; multi-GPU; air-gapped appliance) with sizing guidance, quantization options, throughput/latency benchmarks per release. | P0»
- [ ] Hardware reference configurations (CPU-only small model; single-GPU; multi-GPU; air-gapped appliance) with sizing guidance, quantization options, throughput/latency benchmarks per release.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-LLM-006 [P0] SR-LLM-006: Prompt/skill registry: versioned prompts, schemas, few-shot sets; A/B and regression-evaluated; tenant overrides; prompt content never contains raw sensitive data unless policy allows

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:609-609` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-006 | **Prompt/skill registry:** versioned prompts, schemas, few-shot sets; A/B and regression-evaluated; tenant overrides; prompt content never contains raw sensitive data unless policy allows. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-006 | Prompt/skill registry: versioned prompts, schemas, few-shot sets; A/B and regression-evaluated; tenant overrides; prompt content never contains raw sensitive data unless policy allows. | P0»
- [ ] Prompt/skill registry: versioned prompts, schemas, few-shot sets; A/B and regression-evaluated; tenant overrides; prompt content never contains raw sensitive data unless policy allows.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-LLM-007 [P0] SR-LLM-007: Embedding service with model versioning, batch/online modes, multilingual and code models, and re-embedding jobs (SR-VDB-005)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:610-610` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-007 | **Embedding service** with model versioning, batch/online modes, multilingual and code models, and re-embedding jobs (SR-VDB-005). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-007 | Embedding service with model versioning, batch/online modes, multilingual and code models, and re-embedding jobs (SR-VDB-005). | P0»
- [ ] Embedding service with model versioning, batch/online modes, multilingual and code models, and re-embedding jobs (SR-VDB-005).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-LLM-008 [P0] SR-LLM-008: LLM observability: per-call latency, tokens, cost, cache hits, refusals, guardrail triggers, quality scores — local telemetry only unless the tenant exports it

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:611-611` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-008 | **LLM observability:** per-call latency, tokens, cost, cache hits, refusals, guardrail triggers, quality scores — local telemetry only unless the tenant exports it. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-008 | LLM observability: per-call latency, tokens, cost, cache hits, refusals, guardrail triggers, quality scores — local telemetry only unless the tenant exports it. | P0»
- [ ] LLM observability: per-call latency, tokens, cost, cache hits, refusals, guardrail triggers, quality scores — local telemetry only unless the tenant exports it.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-LLM-009 [P0] SR-LLM-009: Guardrails: input/output scanners (PII, secrets, injection patterns), tool allowlists, output schema validation, jailbreak/prompt-injection test corpus in CI (aligned with the OWASP LLM Top-10 categor

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:612-612` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-009 | **Guardrails:** input/output scanners (PII, secrets, injection patterns), tool allowlists, output schema validation, jailbreak/prompt-injection test corpus in CI (aligned with the OWASP LLM Top-10 categories). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-009 | Guardrails: input/output scanners (PII, secrets, injection patterns), tool allowlists, output schema validation, jailbreak/prompt-injection test corpus in CI (aligned with the OWASP LLM Top-10 categories). | P0»
- [ ] Guardrails: input/output scanners (PII, secrets, injection patterns), tool allowlists, output schema validation, jailbreak/prompt-injection test corpus in CI (aligned with the OWASP LLM Top-10 categories).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-LLM-017 [P0] SR-LLM-017: Consent and contract records: enabling an endpoint records the signer, date, DPA reference, data-residency region and scope; changes require re-approval

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:668-668` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-017 | **Consent and contract records:** enabling an endpoint records the signer, date, DPA reference, data-residency region and scope; changes require re-approval. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-017 | Consent and contract records: enabling an endpoint records the signer, date, DPA reference, data-residency region and scope; changes require re-approval. | P0»
- [ ] Consent and contract records: enabling an endpoint records the signer, date, DPA reference, data-residency region and scope; changes require re-approval.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/egress/gateway.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/gateway.py#L9-L9), [`packages/eoip/egress/policy.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/policy.py#L9-L9), [`packages/eoip/egress/provider.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/provider.py#L12-L12)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-LLM-019 [P0] SR-LLM-019: Local fallback: on denial or outage, tasks fall back to local models or deterministic modes with a visible notice

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:670-670` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-019 | **Local fallback:** on denial or outage, tasks fall back to local models or deterministic modes with a visible notice. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-019 | Local fallback: on denial or outage, tasks fall back to local models or deterministic modes with a visible notice. | P0»
- [ ] Local fallback: on denial or outage, tasks fall back to local models or deterministic modes with a visible notice.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/egress/gateway.py:26`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/gateway.py#L26-L26)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NFR-001 [P0] SR-NFR-001: Horizontal scale for API, query, ingestion workers, agent runners, embedding and model-serving tiers; autoscaling policies (K8s) and manual sizing for appliances

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:896-896` (table_row) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NFR-001 | **Horizontal scale** for API, query, ingestion workers, agent runners, embedding and model-serving tiers; autoscaling policies (K8s) and manual sizing for appliances. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NFR-001 | Horizontal scale for API, query, ingestion workers, agent runners, embedding and model-serving tiers; autoscaling policies (K8s) and manual sizing for appliances. | P0»
- [ ] Horizontal scale for API, query, ingestion workers, agent runners, embedding and model-serving tiers; autoscaling policies (K8s) and manual sizing for appliances.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NFR-003 [P0] SR-NFR-003: Query protection: admission control, per-tenant concurrency, cost-based throttling, kill-runaway-query, result streaming and spill, plan caching

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:898-898` (table_row) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NFR-003 | **Query protection:** admission control, per-tenant concurrency, cost-based throttling, kill-runaway-query, result streaming and spill, plan caching. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NFR-003 | Query protection: admission control, per-tenant concurrency, cost-based throttling, kill-runaway-query, result streaming and spill, plan caching. | P0»
- [ ] Query protection: admission control, per-tenant concurrency, cost-based throttling, kill-runaway-query, result streaming and spill, plan caching.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NFR-004 [P0] SR-NFR-004: Graceful degradation matrix (documented and tested): vector down → text/graph retrieval; model down → deterministic + evidence (SR-RAG-008); search down → graph-only; bus lag → stale-flag; one backend

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:899-899` (table_row) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NFR-004 | **Graceful degradation matrix** (documented and tested): vector down → text/graph retrieval; model down → deterministic + evidence (SR-RAG-008); search down → graph-only; bus lag → stale-flag; one backend down → federated partial results with notice. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NFR-004 | Graceful degradation matrix (documented and tested): vector down → text/graph retrieval; model down → deterministic + evidence (SR-RAG-008); search down → graph-only; bus lag → stale-flag; one backend down → federated partial results with notice. | P0»
- [ ] Graceful degradation matrix (documented and tested): vector down → text/graph retrieval; model down → deterministic + evidence (SR-RAG-008); search down → graph-only; bus lag → stale-flag; one backend down → federated partial results with notice.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NFR-005 [P0] SR-NFR-005: Backup/restore: native backend backups and logical checksummed archives; consistent multi-store snapshots (graph + vector + search + relational + object + event log) with crash-atomic recovery; point-

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:900-900` (table_row) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NFR-005 | **Backup/restore:** native backend backups and logical checksummed archives; consistent multi-store snapshots (graph + vector + search + relational + object + event log) with crash-atomic recovery; point-in-time recovery via event log + revisions; restore drills automated with golden-query verification. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NFR-005 | Backup/restore: native backend backups and logical checksummed archives; consistent multi-store snapshots (graph + vector + search + relational + object + event log) with crash-atomic recovery; point-in-time recovery via event log + revisions; restore drills automated with golden-query verification. | P0»
- [ ] Backup/restore: native backend backups and logical checksummed archives; consistent multi-store snapshots (graph + vector + search + relational + object + event log) with crash-atomic recovery; point-in-time recovery via event log + revisions; restore drills automated with golden-query verification.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NFR-006 [P0] SR-NFR-006: Upgrades: rolling and blue/green for clustered; offline signed upgrade bundles for air-gapped; versioned idempotent schema/ontology migrations; tested downgrade/rollback; compatibility matrix; LTS and

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:901-901` (table_row) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NFR-006 | **Upgrades:** rolling and blue/green for clustered; offline signed upgrade bundles for air-gapped; versioned idempotent schema/ontology migrations; tested downgrade/rollback; compatibility matrix; LTS and stable channels (LTS ≥ 24 months). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NFR-006 | Upgrades: rolling and blue/green for clustered; offline signed upgrade bundles for air-gapped; versioned idempotent schema/ontology migrations; tested downgrade/rollback; compatibility matrix; LTS and stable channels (LTS ≥ 24 months). | P0»
- [ ] Upgrades: rolling and blue/green for clustered; offline signed upgrade bundles for air-gapped; versioned idempotent schema/ontology migrations; tested downgrade/rollback; compatibility matrix; LTS and stable channels (LTS ≥ 24 months).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NLQ-004 [P0] SR-NLQ-004: Answer modes: (1) Deterministic — computed from the graph, exact, no LLM; (2) Narrated — deterministic facts + LLM wording; (3) Exploratory investigation — multi-step agent with visible plan and evide

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:583-583` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NLQ-004 | **Answer modes:** (1) *Deterministic* — computed from the graph, exact, no LLM; (2) *Narrated* — deterministic facts + LLM wording; (3) *Exploratory investigation* — multi-step agent with visible plan and evidence trail; (4) *Report* — long-form, multi-section, charts/tables/citations, exportable. The UI states which mode produced the answer. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NLQ-004 | Answer modes: (1) Deterministic — computed from the graph, exact, no LLM; (2) Narrated — deterministic facts + LLM wording; (3) Exploratory investigation — multi-step agent with visible plan and evidence trail; (4) Report — long-form, multi-section, charts/tables/citations, exportable. The UI states which mode produced the answer. | P0»
- [ ] Answer modes: (1) Deterministic — computed from the graph, exact, no LLM; (2) Narrated — deterministic facts + LLM wording; (3) Exploratory investigation — multi-step agent with visible plan and evidence trail; (4) Report — long-form, multi-section, charts/tables/citations, exportable. The UI states which mode produced the answer.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/suggest/models.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/suggest/models.py#L1-L1)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NLQ-005 [P0] SR-NLQ-005: Depth bar ("no shortness"): answers MUST include, as relevant: direct answer, supporting evidence and paths, assumptions, confidence and uncertainty, alternatives considered, recommended next actions,

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:584-584` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NLQ-005 | **Depth bar ("no shortness"):** answers MUST include, as relevant: direct answer, supporting evidence and paths, assumptions, confidence and uncertainty, alternatives considered, recommended next actions, coverage gaps ("sources not ingested that could change this"), and suggested follow-up questions. Minimum answer-quality gates are enforced by the evaluation suite (SR-NLQ-010). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NLQ-005 | Depth bar ("no shortness"): answers MUST include, as relevant: direct answer, supporting evidence and paths, assumptions, confidence and uncertainty, alternatives considered, recommended next actions, coverage gaps ("sources not ingested that could change this"), and suggested follow-up questions. Minimum answer-quality gates are enforced by the evaluation suite (S»
- [ ] Depth bar ("no shortness"): answers MUST include, as relevant: direct answer, supporting evidence and paths, assumptions, confidence and uncertainty, alternatives considered, recommended next actions, coverage gaps ("sources not ingested that could change this"), and suggested follow-up questions. Minimum answer-quality gates are enforced by the evaluation suite (SR-NLQ-010).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NLQ-006 [P0] SR-NLQ-006: Explainability (XAI): "why?" on any result returns the paths/rules/premises; counterfactuals ("what would change the answer?"); confidence decomposition (edge confidence, source freshness, coverage). 

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:585-585` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NLQ-006 | **Explainability (XAI):** "why?" on any result returns the paths/rules/premises; counterfactuals ("what would change the answer?"); confidence decomposition (edge confidence, source freshness, coverage). Do not depend on exposing hidden model chain-of-thought. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NLQ-006 | Explainability (XAI): "why?" on any result returns the paths/rules/premises; counterfactuals ("what would change the answer?"); confidence decomposition (edge confidence, source freshness, coverage). Do not depend on exposing hidden model chain-of-thought. | P0»
- [ ] Explainability (XAI): "why?" on any result returns the paths/rules/premises; counterfactuals ("what would change the answer?"); confidence decomposition (edge confidence, source freshness, coverage). Do not depend on exposing hidden model chain-of-thought.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NLQ-007 [P0] SR-NLQ-007: Conversation context: follow-ups, pronoun/ellipsis resolution, session and saved-investigation memory, pinned entities, branching ("explore alternative"), shareable investigation links respecting each

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:586-586` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NLQ-007 | **Conversation context:** follow-ups, pronoun/ellipsis resolution, session and saved-investigation memory, pinned entities, branching ("explore alternative"), shareable investigation links respecting each viewer's permissions. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NLQ-007 | Conversation context: follow-ups, pronoun/ellipsis resolution, session and saved-investigation memory, pinned entities, branching ("explore alternative"), shareable investigation links respecting each viewer's permissions. | P0»
- [ ] Conversation context: follow-ups, pronoun/ellipsis resolution, session and saved-investigation memory, pinned entities, branching ("explore alternative"), shareable investigation links respecting each viewer's permissions.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NLQ-009 [P0] SR-NLQ-009: Languages: English at P0; multilingual NL (major European, Indic and East-Asian languages) via local multilingual models at P1, with glossary-term translation

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:588-588` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NLQ-009 | **Languages:** English at P0; multilingual NL (major European, Indic and East-Asian languages) via local multilingual models at P1, with glossary-term translation. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NLQ-009 | Languages: English at P0; multilingual NL (major European, Indic and East-Asian languages) via local multilingual models at P1, with glossary-term translation. | P1»
- [ ] Languages: English at P0; multilingual NL (major European, Indic and East-Asian languages) via local multilingual models at P1, with glossary-term translation.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NLQ-010 [P0] SR-NLQ-010: NL evaluation suite: golden question sets per intent and per industry pack; metrics — intent accuracy, entity-link accuracy, plan validity rate, execution accuracy (result-set equality), groundedness,

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:589-589` (table_row) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NLQ-010 | **NL evaluation suite:** golden question sets per intent and per industry pack; metrics — intent accuracy, entity-link accuracy, plan validity rate, **execution accuracy** (result-set equality), groundedness, hallucination rate, refusal correctness, clarification precision, latency, tokens. Proposal gates: ≥ 95 % execution accuracy on Tier-1 deterministic intents; ≥ 0.95 groundedness on narrated answers; 0 policy-violating results in the adversarial set. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NLQ-010 | NL evaluation suite: golden question sets per intent and per industry pack; metrics — intent accuracy, entity-link accuracy, plan validity rate, execution accuracy (result-set equality), groundedness, hallucination rate, refusal correctness, clarification precision, latency, tokens. Proposal gates: ≥ 95 % execution accuracy on Tier-1 deterministic intents; ≥ 0.95 g»
- [ ] NL evaluation suite: golden question sets per intent and per industry pack; metrics — intent accuracy, entity-link accuracy, plan validity rate, execution accuracy (result-set equality), groundedness, hallucination rate, refusal correctness, clarification precision, latency, tokens. Proposal gates: ≥ 95 % execution accuracy on Tier-1 deterministic intents; ≥ 0.95 groundedness on narrated answers; 
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NLQ-011 [P0] SR-NLQ-011: Safety: refuse or constrain questions the user is not entitled to; never reveal existence of hidden entities ("redaction notice" lists the fact that filters applied, not the content)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:590-590` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NLQ-011 | **Safety:** refuse or constrain questions the user is not entitled to; never reveal existence of hidden entities ("redaction notice" lists the *fact* that filters applied, not the content). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NLQ-011 | Safety: refuse or constrain questions the user is not entitled to; never reveal existence of hidden entities ("redaction notice" lists the fact that filters applied, not the content). | P0»
- [ ] Safety: refuse or constrain questions the user is not entitled to; never reveal existence of hidden entities ("redaction notice" lists the fact that filters applied, not the content).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ONT-001 [P0] SR-ONT-001: Ontology service stores ontologies as versioned artifacts (semantic versioning, diff, migration plans, deprecation lifecycle). Every graph element pins ontologyversion

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:495-495` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ONT-001 | **Ontology service** stores ontologies as versioned artifacts (semantic versioning, diff, migration plans, deprecation lifecycle). Every graph element pins `ontology_version`. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ONT-001 | Ontology service stores ontologies as versioned artifacts (semantic versioning, diff, migration plans, deprecation lifecycle). Every graph element pins ontology_version. | P0»
- [ ] Ontology service stores ontologies as versioned artifacts (semantic versioning, diff, migration plans, deprecation lifecycle). Every graph element pins ontology_version.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ONT-002 [P0] SR-ONT-002: Import/export: OWL 2 (RDF/XML, Turtle, Manchester), RDFS, SKOS, JSON Schema, JSON-LD contexts, LinkML-style schemas, Protégé project interop, CSV glossaries; export of the active ontology to OWL and S

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:496-496` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ONT-002 | **Import/export:** OWL 2 (RDF/XML, Turtle, Manchester), RDFS, SKOS, JSON Schema, JSON-LD contexts, LinkML-style schemas, Protégé project interop, CSV glossaries; export of the active ontology to OWL and SHACL shapes. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ONT-002 | Import/export: OWL 2 (RDF/XML, Turtle, Manchester), RDFS, SKOS, JSON Schema, JSON-LD contexts, LinkML-style schemas, Protégé project interop, CSV glossaries; export of the active ontology to OWL and SHACL shapes. | P0»
- [ ] Import/export: OWL 2 (RDF/XML, Turtle, Manchester), RDFS, SKOS, JSON Schema, JSON-LD contexts, LinkML-style schemas, Protégé project interop, CSV glossaries; export of the active ontology to OWL and SHACL shapes.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ONT-003 [P0] SR-ONT-003: Ontology Studio (UI): visual class/property editor, relationship canvas, constraint editor, glossary/taxonomy manager, mapping designer, diff/merge, impact preview ("what existing data breaks if I cha

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:497-497` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ONT-003 | **Ontology Studio** (UI): visual class/property editor, relationship canvas, constraint editor, glossary/taxonomy manager, mapping designer, diff/merge, impact preview ("what existing data breaks if I change this?"), review-and-approve workflow with roles. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ONT-003 | Ontology Studio (UI): visual class/property editor, relationship canvas, constraint editor, glossary/taxonomy manager, mapping designer, diff/merge, impact preview ("what existing data breaks if I change this?"), review-and-approve workflow with roles. | P0»
- [ ] Ontology Studio (UI): visual class/property editor, relationship canvas, constraint editor, glossary/taxonomy manager, mapping designer, diff/merge, impact preview ("what existing data breaks if I change this?"), review-and-approve workflow with roles.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ONT-004 [P0] SR-ONT-004: Constraint validation via SHACL-class shapes plus native rules; severity-based gates in ingestion; constraint violations visible as a graph-quality dashboard

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:498-498` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ONT-004 | **Constraint validation** via SHACL-class shapes plus native rules; severity-based gates in ingestion; constraint violations visible as a graph-quality dashboard. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ONT-004 | Constraint validation via SHACL-class shapes plus native rules; severity-based gates in ingestion; constraint violations visible as a graph-quality dashboard. | P0»
- [ ] Constraint validation via SHACL-class shapes plus native rules; severity-based gates in ingestion; constraint violations visible as a graph-quality dashboard.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ONT-005 [P0] SR-ONT-005: Business glossary and taxonomy (SKOS-compatible): terms, synonyms, multilingual labels, definitions, owners, approved-status; terms link to ontology concepts and to physical fields; NL layer uses the 

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:499-499` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ONT-005 | **Business glossary and taxonomy** (SKOS-compatible): terms, synonyms, multilingual labels, definitions, owners, approved-status; terms link to ontology concepts and to physical fields; NL layer uses the glossary for grounding. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ONT-005 | Business glossary and taxonomy (SKOS-compatible): terms, synonyms, multilingual labels, definitions, owners, approved-status; terms link to ontology concepts and to physical fields; NL layer uses the glossary for grounding. | P0»
- [ ] Business glossary and taxonomy (SKOS-compatible): terms, synonyms, multilingual labels, definitions, owners, approved-status; terms link to ontology concepts and to physical fields; NL layer uses the glossary for grounding.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ONT-009 [P0] SR-ONT-009: Governed evolution: proposals, review, approval, scheduled rollout, backward-compat checks, automatic data migration jobs, rollback

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:503-503` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ONT-009 | **Governed evolution:** proposals, review, approval, scheduled rollout, backward-compat checks, automatic data migration jobs, rollback. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ONT-009 | Governed evolution: proposals, review, approval, scheduled rollout, backward-compat checks, automatic data migration jobs, rollback. | P0»
- [ ] Governed evolution: proposals, review, approval, scheduled rollout, backward-compat checks, automatic data migration jobs, rollback.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-OPS-001 [P0] SR-OPS-001: OpenTelemetry metrics, logs and traces end-to-end (ingestion → mutation → query → answer); local sinks (Prometheus/Grafana/Loki/Tempo-class) bundled; customer sinks pluggable. Structured JSON logs wit

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:909-909` (table_row) · **Type:** Infra · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-OPS-001 | **OpenTelemetry** metrics, logs and traces end-to-end (ingestion → mutation → query → answer); local sinks (Prometheus/Grafana/Loki/Tempo-class) bundled; customer sinks pluggable. Structured JSON logs with correlation IDs, no secrets, no raw sensitive values. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-OPS-001 | OpenTelemetry metrics, logs and traces end-to-end (ingestion → mutation → query → answer); local sinks (Prometheus/Grafana/Loki/Tempo-class) bundled; customer sinks pluggable. Structured JSON logs with correlation IDs, no secrets, no raw sensitive values. | P0»
- [ ] OpenTelemetry metrics, logs and traces end-to-end (ingestion → mutation → query → answer); local sinks (Prometheus/Grafana/Loki/Tempo-class) bundled; customer sinks pluggable. Structured JSON logs with correlation IDs, no secrets, no raw sensitive values.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-OPS-002 [P0] SR-OPS-002: Health and readiness endpoints per service; dependency health roll-up; SLO dashboards and alert rules shipped as code

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:910-910` (table_row) · **Type:** Infra · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-OPS-002 | **Health and readiness** endpoints per service; dependency health roll-up; SLO dashboards and alert rules shipped as code. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-OPS-002 | Health and readiness endpoints per service; dependency health roll-up; SLO dashboards and alert rules shipped as code. | P0»
- [ ] Health and readiness endpoints per service; dependency health roll-up; SLO dashboards and alert rules shipped as code.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-OPS-003 [P0] SR-OPS-003: Support bundle: one command/UI action produces a redacted diagnostic archive; customer reviews before sharing

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:911-911` (table_row) · **Type:** Infra · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-OPS-003 | **Support bundle:** one command/UI action produces a redacted diagnostic archive; customer reviews before sharing. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-OPS-003 | Support bundle: one command/UI action produces a redacted diagnostic archive; customer reviews before sharing. | P0»
- [ ] Support bundle: one command/UI action produces a redacted diagnostic archive; customer reviews before sharing.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-OPS-004 [P0] SR-OPS-004: Telemetry to vendor is OFF by default; optional, opt-in, content-free usage statistics with a visible schema

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:912-912` (table_row) · **Type:** Infra · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-OPS-004 | **Telemetry to vendor is OFF by default;** optional, opt-in, content-free usage statistics with a visible schema. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-OPS-004 | Telemetry to vendor is OFF by default; optional, opt-in, content-free usage statistics with a visible schema. | P0»
- [ ] Telemetry to vendor is OFF by default; optional, opt-in, content-free usage statistics with a visible schema.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-OPS-005 [P0] SR-OPS-005: Runbooks for connector failure, DLQ drain, graph restore, schema/ontology migration rollback, model outage, egress incident, tenant isolation incident, key rotation, DR failover

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:913-913` (table_row) · **Type:** Infra · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-OPS-005 | **Runbooks** for connector failure, DLQ drain, graph restore, schema/ontology migration rollback, model outage, egress incident, tenant isolation incident, key rotation, DR failover. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-OPS-005 | Runbooks for connector failure, DLQ drain, graph restore, schema/ontology migration rollback, model outage, egress incident, tenant isolation incident, key rotation, DR failover. | P0»
- [ ] Runbooks for connector failure, DLQ drain, graph restore, schema/ontology migration rollback, model outage, egress incident, tenant isolation incident, key rotation, DR failover.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-PRV-002 [P0] SR-PRV-002: Data-subject requests: locate a subject across graph, raw captures, vector/search indexes, caches, derived graphs, exports and backups (flagged); execute access/export, rectification and erasure with 

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:849-849` (table_row) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-PRV-002 | **Data-subject requests:** locate a subject across graph, raw captures, vector/search indexes, caches, derived graphs, exports and backups (flagged); execute access/export, rectification and **erasure with propagation** (including embeddings and summaries) and produce proof. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-PRV-002 | Data-subject requests: locate a subject across graph, raw captures, vector/search indexes, caches, derived graphs, exports and backups (flagged); execute access/export, rectification and erasure with propagation (including embeddings and summaries) and produce proof. | P0»
- [ ] Data-subject requests: locate a subject across graph, raw captures, vector/search indexes, caches, derived graphs, exports and backups (flagged); execute access/export, rectification and erasure with propagation (including embeddings and summaries) and produce proof.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/privacy/dsar.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/privacy/dsar.py#L1-L1)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-PRV-003 [P0] SR-PRV-003: Retention and legal hold per class/tenant/source; automated expiry with crypto-shred option

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:850-850` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-PRV-003 | **Retention and legal hold** per class/tenant/source; automated expiry with crypto-shred option. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-PRV-003 | Retention and legal hold per class/tenant/source; automated expiry with crypto-shred option. | P0»
- [ ] Retention and legal hold per class/tenant/source; automated expiry with crypto-shred option.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/privacy/dsar.py:174`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/privacy/dsar.py#L174-L174), [`packages/eoip/privacy/retention.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/privacy/retention.py#L1-L1)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-QA-001 [P0] SR-QA-001: Provide synthetic dataset generators per industry pack (referentially consistent, with planted ground-truth relationships, duplicates, drift, PII canaries and adversarial prompt-injection documents). 

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:955-955` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QA-001 | Provide **synthetic dataset generators** per industry pack (referentially consistent, with planted ground-truth relationships, duplicates, drift, PII canaries and adversarial prompt-injection documents). No real customer data in test assets. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QA-001 | Provide synthetic dataset generators per industry pack (referentially consistent, with planted ground-truth relationships, duplicates, drift, PII canaries and adversarial prompt-injection documents). No real customer data in test assets. | P0»
- [ ] Provide synthetic dataset generators per industry pack (referentially consistent, with planted ground-truth relationships, duplicates, drift, PII canaries and adversarial prompt-injection documents). No real customer data in test assets.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-QA-002 [P0] SR-QA-002: Each generator exposes scale knobs (S/M/L/XL) and ground-truth answers for the golden question sets

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:956-956` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QA-002 | Each generator exposes scale knobs (S/M/L/XL) and ground-truth answers for the golden question sets. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QA-002 | Each generator exposes scale knobs (S/M/L/XL) and ground-truth answers for the golden question sets. | P0»
- [ ] Each generator exposes scale knobs (S/M/L/XL) and ground-truth answers for the golden question sets.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-QRY-001 [P0] SR-QRY-001: The compiler MUST accept EOQL, Gremlin, openCypher, GQL (subset first), SPARQL, SQL (analytics) and NL-produced plans, validate them against the ontology and the caller's policy, and lower them per th

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:312-312` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QRY-001 | The compiler MUST accept EOQL, Gremlin, openCypher, GQL (subset first), SPARQL, SQL (analytics) and NL-produced plans, validate them against the ontology and the caller's policy, and lower them per the Capability Manifest. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QRY-001 | The compiler MUST accept EOQL, Gremlin, openCypher, GQL (subset first), SPARQL, SQL (analytics) and NL-produced plans, validate them against the ontology and the caller's policy, and lower them per the Capability Manifest. | P0»
- [ ] The compiler MUST accept EOQL, Gremlin, openCypher, GQL (subset first), SPARQL, SQL (analytics) and NL-produced plans, validate them against the ontology and the caller's policy, and lower them per the Capability Manifest.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-QRY-002 [P0] SR-QRY-002: Never execute raw model- or user-generated graph queries without schema-aware validation, policy rewrite, depth/timeout/expansion/cost limits and expensive-pattern detection. Raw dialect access is an 

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:313-313` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QRY-002 | **Never execute raw model- or user-generated graph queries** without schema-aware validation, policy rewrite, depth/timeout/expansion/cost limits and expensive-pattern detection. Raw dialect access is an admin-gated, audited feature. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QRY-002 | Never execute raw model- or user-generated graph queries without schema-aware validation, policy rewrite, depth/timeout/expansion/cost limits and expensive-pattern detection. Raw dialect access is an admin-gated, audited feature. | P0»
- [ ] Never execute raw model- or user-generated graph queries without schema-aware validation, policy rewrite, depth/timeout/expansion/cost limits and expensive-pattern detection. Raw dialect access is an admin-gated, audited feature.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-QRY-003 [P0] SR-QRY-003: Query Explain: every query returns (on request) the plan, chosen backend(s), pushdowns, estimated vs actual cost, and the generated dialect text

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:314-314` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QRY-003 | **Query Explain:** every query returns (on request) the plan, chosen backend(s), pushdowns, estimated vs actual cost, and the generated dialect text. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QRY-003 | Query Explain: every query returns (on request) the plan, chosen backend(s), pushdowns, estimated vs actual cost, and the generated dialect text. | P0»
- [ ] Query Explain: every query returns (on request) the plan, chosen backend(s), pushdowns, estimated vs actual cost, and the generated dialect text.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

