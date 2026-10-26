# EPIC-SUPER-NOTRUN-04: EOIP-engg-doc-pkg/super-requirements.md · tests_not_executed

*Tests are mapped/referenced but none ran in the audit (excluded or not collected).* 60 tasks, ~60.0 h, priorities {'P1': 49, 'P2': 11}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-SR-DEP-002 [P1] SR-DEP-002: Helm charts/operators for Kubernetes (HA, autoscaling, network policies, pod security, PDBs) for DP-1…DP-4

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:923-923` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-DEP-002 | **Helm charts/operators** for Kubernetes (HA, autoscaling, network policies, pod security, PDBs) for DP-1…DP-4. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-DEP-002 | Helm charts/operators for Kubernetes (HA, autoscaling, network policies, pod security, PDBs) for DP-1…DP-4. | P1»
- [ ] Helm charts/operators for Kubernetes (HA, autoscaling, network policies, pod security, PDBs) for DP-1…DP-4.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-EXT-013 [P1] SR-EXT-013: Plugin test kit and scaffolding CLI; contract tests mandatory for marketplace listing

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:789-789` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-EXT-013 | **Plugin test kit** and scaffolding CLI; contract tests mandatory for marketplace listing. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-EXT-013 | Plugin test kit and scaffolding CLI; contract tests mandatory for marketplace listing. | P1»
- [ ] Plugin test kit and scaffolding CLI; contract tests mandatory for marketplace listing.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-EXT-014 [P1] SR-EXT-014: Marketplace (online catalog for connected profiles; offline catalog bundles for air-gapped): ratings, security scan results, certification badges, revenue-share support

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:790-790` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-EXT-014 | **Marketplace** (online catalog for connected profiles; **offline catalog bundles** for air-gapped): ratings, security scan results, certification badges, revenue-share support. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-EXT-014 | Marketplace (online catalog for connected profiles; offline catalog bundles for air-gapped): ratings, security scan results, certification badges, revenue-share support. | P1»
- [ ] Marketplace (online catalog for connected profiles; offline catalog bundles for air-gapped): ratings, security scan results, certification badges, revenue-share support.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-EXT-015 [P1] SR-EXT-015: Low-code Studio: visual pipeline, mapping, rule, agent and report builders that emit the same versioned artifacts as code

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:791-791` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-EXT-015 | **Low-code Studio:** visual pipeline, mapping, rule, agent and report builders that emit the same versioned artifacts as code. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-EXT-015 | Low-code Studio: visual pipeline, mapping, rule, agent and report builders that emit the same versioned artifacts as code. | P1»
- [ ] Low-code Studio: visual pipeline, mapping, rule, agent and report builders that emit the same versioned artifacts as code.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-GDB-005 [P1] SR-GDB-005: Polyglot persistence: each logical graph domain (e.g., org, code, incident, lineage, meta) MAY bind to a different backend and tier (hot/warm/cold); cross-domain bridge edges are resolved by the feder

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:187-187` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GDB-005 | **Polyglot persistence:** each logical graph domain (e.g., org, code, incident, lineage, meta) MAY bind to a different backend and tier (hot/warm/cold); cross-domain **bridge edges** are resolved by the federation layer. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GDB-005 | Polyglot persistence: each logical graph domain (e.g., org, code, incident, lineage, meta) MAY bind to a different backend and tier (hot/warm/cold); cross-domain bridge edges are resolved by the federation layer. | P1»
- [ ] Polyglot persistence: each logical graph domain (e.g., org, code, incident, lineage, meta) MAY bind to a different backend and tier (hot/warm/cold); cross-domain bridge edges are resolved by the federation layer.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-GDB-006 [P1] SR-GDB-006: Online migration between backends (export → verify counts/checksums/golden queries → dual-write or cutover → rollback) MUST be supported for Tier A pairs

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:188-188` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GDB-006 | **Online migration** between backends (export → verify counts/checksums/golden queries → dual-write or cutover → rollback) MUST be supported for Tier A pairs. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GDB-006 | Online migration between backends (export → verify counts/checksums/golden queries → dual-write or cutover → rollback) MUST be supported for Tier A pairs. | P1»
- [ ] Online migration between backends (export → verify counts/checksums/golden queries → dual-write or cutover → rollback) MUST be supported for Tier A pairs.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-GDB-008 [P1] SR-GDB-008: Multi-model graph support: property graph (LPG) and RDF are both first-class; RDF-star/reification patterns and LPG↔RDF round-trip mappings MUST be defined and tested

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:190-190` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GDB-008 | **Multi-model graph support:** property graph (LPG) and RDF are both first-class; RDF-star/reification patterns and LPG↔RDF round-trip mappings MUST be defined and tested. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GDB-008 | Multi-model graph support: property graph (LPG) and RDF are both first-class; RDF-star/reification patterns and LPG↔RDF round-trip mappings MUST be defined and tested. | P1»
- [ ] Multi-model graph support: property graph (LPG) and RDF are both first-class; RDF-star/reification patterns and LPG↔RDF round-trip mappings MUST be defined and tested.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-GDB-009 [P1] SR-GDB-009: Graph versioning: every mutation produces an EntityRevision; point-in-time ("as-of") reads and diffs between revisions MUST be supported (full snapshot/diff at P1)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:191-191` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GDB-009 | **Graph versioning:** every mutation produces an `EntityRevision`; point-in-time ("as-of") reads and diffs between revisions MUST be supported (full snapshot/diff at P1). | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GDB-009 | Graph versioning: every mutation produces an EntityRevision; point-in-time ("as-of") reads and diffs between revisions MUST be supported (full snapshot/diff at P1). | P1»
- [ ] Graph versioning: every mutation produces an EntityRevision; point-in-time ("as-of") reads and diffs between revisions MUST be supported (full snapshot/diff at P1).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-GDB-015 [P1] SR-GDB-015: Durable workflow engine built in (retry, timers, human-approval steps, sagas); optional adapters for Temporal/Airflow/Dagster/Prefect-class orchestrators

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:220-220` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GDB-015 | **Durable workflow engine** built in (retry, timers, human-approval steps, sagas); optional adapters for Temporal/Airflow/Dagster/Prefect-class orchestrators. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GDB-015 | Durable workflow engine built in (retry, timers, human-approval steps, sagas); optional adapters for Temporal/Airflow/Dagster/Prefect-class orchestrators. | P1»
- [ ] Durable workflow engine built in (retry, timers, human-approval steps, sagas); optional adapters for Temporal/Airflow/Dagster/Prefect-class orchestrators.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-005 [P1] SR-ING-005: Connector marketplace-ready packaging: signed manifest, version, compatibility range, data-flow manifest, test fixtures, health contract

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:349-349` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-005 | **Connector marketplace-ready packaging:** signed manifest, version, compatibility range, data-flow manifest, test fixtures, health contract. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-005 | Connector marketplace-ready packaging: signed manifest, version, compatibility range, data-flow manifest, test fixtures, health contract. | P1»
- [ ] Connector marketplace-ready packaging: signed manifest, version, compatibility range, data-flow manifest, test fixtures, health contract.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-017 [P1] SR-ING-017: Ontology induction: propose classes, properties, relation types and hierarchies from data; present for steward approval in the Mapping Studio; support ontology-first, data-first and hybrid modes

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:386-386` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-017 | **Ontology induction:** propose classes, properties, relation types and hierarchies from data; present for steward approval in the Mapping Studio; support *ontology-first*, *data-first* and *hybrid* modes. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-017 | Ontology induction: propose classes, properties, relation types and hierarchies from data; present for steward approval in the Mapping Studio; support ontology-first, data-first and hybrid modes. | P1»
- [ ] Ontology induction: propose classes, properties, relation types and hierarchies from data; present for steward approval in the Mapping Studio; support ontology-first, data-first and hybrid modes.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-031 [P1] SR-ING-031: Collective resolution using graph context (shared neighbors, co-authorship, same repo/team) and transitive clustering with constraints; survivorship rules produce golden records with per-attribute sou

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:415-415` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-031 | **Collective resolution** using graph context (shared neighbors, co-authorship, same repo/team) and transitive clustering with constraints; **survivorship rules** produce golden records with per-attribute source precedence. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-031 | Collective resolution using graph context (shared neighbors, co-authorship, same repo/team) and transitive clustering with constraints; survivorship rules produce golden records with per-attribute source precedence. | P1»
- [ ] Collective resolution using graph context (shared neighbors, co-authorship, same repo/team) and transitive clustering with constraints; survivorship rules produce golden records with per-attribute source precedence.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-041 [P1] SR-ING-041: Graphify-class artifacts: auto-generate portable graph.json, interactive HTML, and a markdown/wiki report per graph or subgraph; support export to Obsidian/Markdown vaults; support post-commit/post-me

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:441-441` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-041 | **Graphify-class artifacts:** auto-generate portable `graph.json`, interactive HTML, and a markdown/wiki report per graph or subgraph; support export to Obsidian/Markdown vaults; support post-commit/post-merge hooks and PR-impact triage (rank open change requests by graph impact; flag overlapping-community conflicts). | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-041 | Graphify-class artifacts: auto-generate portable graph.json, interactive HTML, and a markdown/wiki report per graph or subgraph; support export to Obsidian/Markdown vaults; support post-commit/post-merge hooks and PR-impact triage (rank open change requests by graph impact; flag overlapping-community conflicts). | P1»
- [ ] Graphify-class artifacts: auto-generate portable graph.json, interactive HTML, and a markdown/wiki report per graph or subgraph; support export to Obsidian/Markdown vaults; support post-commit/post-merge hooks and PR-impact triage (rank open change requests by graph impact; flag overlapping-community conflicts).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-043 [P1] SR-ING-043: Pre-aggregation: per-type degree/centrality, per-edge-class reachability, and domain-to-domain bridge statistics are maintained to answer overview and impact questions within latency targets

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:443-443` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-043 | **Pre-aggregation:** per-type degree/centrality, per-edge-class reachability, and domain-to-domain bridge statistics are maintained to answer overview and impact questions within latency targets. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-043 | Pre-aggregation: per-type degree/centrality, per-edge-class reachability, and domain-to-domain bridge statistics are maintained to answer overview and impact questions within latency targets. | P1»
- [ ] Pre-aggregation: per-type degree/centrality, per-edge-class reachability, and domain-to-domain bridge statistics are maintained to answer overview and impact questions within latency targets.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-071 [P1] SR-ING-071: BI/analytics access: read-only JDBC/ODBC SQL views, OData, GraphQL, Arrow Flight-class bulk endpoint, notebook (Jupyter) client libraries

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:475-475` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-071 | BI/analytics access: read-only JDBC/ODBC SQL views, OData, GraphQL, Arrow Flight-class bulk endpoint, notebook (Jupyter) client libraries. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-071 | BI/analytics access: read-only JDBC/ODBC SQL views, OData, GraphQL, Arrow Flight-class bulk endpoint, notebook (Jupyter) client libraries. | P1»
- [ ] BI/analytics access: read-only JDBC/ODBC SQL views, OData, GraphQL, Arrow Flight-class bulk endpoint, notebook (Jupyter) client libraries.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-LLM-020 [P1] SR-LLM-020: Region and sovereignty pinning: endpoints and processing regions are constrained per tenant/jurisdiction

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:671-671` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-020 | **Region and sovereignty pinning:** endpoints and processing regions are constrained per tenant/jurisdiction. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-020 | Region and sovereignty pinning: endpoints and processing regions are constrained per tenant/jurisdiction. | P1»
- [ ] Region and sovereignty pinning: endpoints and processing regions are constrained per tenant/jurisdiction.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/egress/gateway.py:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/gateway.py#L17-L17)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NFR-002 [P1] SR-NFR-002: Data scaling patterns: graph partitioning/sharding per backend capability, read replicas, tenant-based partitioning, hot/warm/cold tiering, archive to object storage with rehydration, vector index sha

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:897-897` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NFR-002 | **Data scaling patterns:** graph partitioning/sharding per backend capability, read replicas, tenant-based partitioning, hot/warm/cold tiering, archive to object storage with rehydration, vector index sharding, search index lifecycle management. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NFR-002 | Data scaling patterns: graph partitioning/sharding per backend capability, read replicas, tenant-based partitioning, hot/warm/cold tiering, archive to object storage with rehydration, vector index sharding, search index lifecycle management. | P1»
- [ ] Data scaling patterns: graph partitioning/sharding per backend capability, read replicas, tenant-based partitioning, hot/warm/cold tiering, archive to object storage with rehydration, vector index sharding, search index lifecycle management.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NFR-007 [P1] SR-NFR-007: Chaos and soak testing: node/zone failure, partition, slow disk, clock skew, backend restart mid-ingest; 7-day soak per release

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:902-902` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NFR-007 | **Chaos and soak testing:** node/zone failure, partition, slow disk, clock skew, backend restart mid-ingest; 7-day soak per release. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NFR-007 | Chaos and soak testing: node/zone failure, partition, slow disk, clock skew, backend restart mid-ingest; 7-day soak per release. | P1»
- [ ] Chaos and soak testing: node/zone failure, partition, slow disk, clock skew, backend restart mid-ingest; 7-day soak per release.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NFR-008 [P1] SR-NFR-008: Capacity planning tools: sizing calculator and in-product forecasts (graph growth, index size, GPU needs) with reference architectures per tier

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:903-903` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NFR-008 | **Capacity planning tools:** sizing calculator and in-product forecasts (graph growth, index size, GPU needs) with reference architectures per tier. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NFR-008 | Capacity planning tools: sizing calculator and in-product forecasts (graph growth, index size, GPU needs) with reference architectures per tier. | P1»
- [ ] Capacity planning tools: sizing calculator and in-product forecasts (graph growth, index size, GPU needs) with reference architectures per tier.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NLQ-012 [P1] SR-NLQ-012: Feedback loop: thumbs/corrections/"this edge is wrong" feed a curation queue that improves mappings, aliases, intent templates and ranking, with steward approval

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:591-591` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NLQ-012 | **Feedback loop:** thumbs/corrections/"this edge is wrong" feed a curation queue that improves mappings, aliases, intent templates and ranking, with steward approval. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NLQ-012 | Feedback loop: thumbs/corrections/"this edge is wrong" feed a curation queue that improves mappings, aliases, intent templates and ranking, with steward approval. | P1»
- [ ] Feedback loop: thumbs/corrections/"this edge is wrong" feed a curation queue that improves mappings, aliases, intent templates and ranking, with steward approval.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NLQ-014 [P1] SR-NLQ-014: What-if simulation: sandboxed copy-on-write overlay graph where users propose changes (delete service, rotate account, add dependency) and see propagated impact before acting; overlay never alters pro

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:593-593` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NLQ-014 | **What-if simulation:** sandboxed copy-on-write overlay graph where users propose changes (delete service, rotate account, add dependency) and see propagated impact before acting; overlay never alters production truth. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NLQ-014 | What-if simulation: sandboxed copy-on-write overlay graph where users propose changes (delete service, rotate account, add dependency) and see propagated impact before acting; overlay never alters production truth. | P1»
- [ ] What-if simulation: sandboxed copy-on-write overlay graph where users propose changes (delete service, rotate account, add dependency) and see propagated impact before acting; overlay never alters production truth.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NLQ-015 [P1] SR-NLQ-015: Proactive suggestions: based on role, current entity and usage graph, the UI proposes "questions you might ask next" (e.g., owners to notify, tests to run)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:594-594` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NLQ-015 | **Proactive suggestions:** based on role, current entity and usage graph, the UI proposes "questions you might ask next" (e.g., owners to notify, tests to run). | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NLQ-015 | Proactive suggestions: based on role, current entity and usage graph, the UI proposes "questions you might ask next" (e.g., owners to notify, tests to run). | P1»
- [ ] Proactive suggestions: based on role, current entity and usage graph, the UI proposes "questions you might ask next" (e.g., owners to notify, tests to run).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ONT-006 [P1] SR-ONT-006: Ontology alignment/matching: lexical, structural, embedding-assisted mapping between a customer's vocabulary and an industry standard, with confidence and steward review

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:500-500` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ONT-006 | **Ontology alignment/matching:** lexical, structural, embedding-assisted mapping between a customer's vocabulary and an industry standard, with confidence and steward review. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ONT-006 | Ontology alignment/matching: lexical, structural, embedding-assisted mapping between a customer's vocabulary and an industry standard, with confidence and steward review. | P1»
- [ ] Ontology alignment/matching: lexical, structural, embedding-assisted mapping between a customer's vocabulary and an industry standard, with confidence and steward review.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ONT-008 [P1] SR-ONT-008: Ontology-driven generation: GraphQL schema, REST resources, form UIs, validation, and docs generated from the ontology

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:502-502` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ONT-008 | **Ontology-driven generation:** GraphQL schema, REST resources, form UIs, validation, and docs generated from the ontology. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ONT-008 | Ontology-driven generation: GraphQL schema, REST resources, form UIs, validation, and docs generated from the ontology. | P1»
- [ ] Ontology-driven generation: GraphQL schema, REST resources, form UIs, validation, and docs generated from the ontology.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ONT-010 [P1] SR-ONT-010: Catalog interoperability: import/sync with data catalogs and glossaries (DataHub, OpenMetadata, Atlas, Collibra-class), CMDBs, enterprise-architecture repositories (ArchiMate/TOGAF models), and API re

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:504-504` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ONT-010 | **Catalog interoperability:** import/sync with data catalogs and glossaries (DataHub, OpenMetadata, Atlas, Collibra-class), CMDBs, enterprise-architecture repositories (ArchiMate/TOGAF models), and API registries. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ONT-010 | Catalog interoperability: import/sync with data catalogs and glossaries (DataHub, OpenMetadata, Atlas, Collibra-class), CMDBs, enterprise-architecture repositories (ArchiMate/TOGAF models), and API registries. | P1»
- [ ] Catalog interoperability: import/sync with data catalogs and glossaries (DataHub, OpenMetadata, Atlas, Collibra-class), CMDBs, enterprise-architecture repositories (ArchiMate/TOGAF models), and API registries.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ONT-020 [P1] SR-ONT-020: Inference tiers: (a) graph-native derivations (transitive, inverse, symmetric, property chains), (b) rule-based (Datalog/SWRL-class) materialization with provenance, (c) OWL-RL/EL profile reasoning wh

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:522-522` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ONT-020 | **Inference tiers:** (a) graph-native derivations (transitive, inverse, symmetric, property chains), (b) rule-based (Datalog/SWRL-class) materialization with provenance, (c) OWL-RL/EL profile reasoning where RDF back-ends support it, (d) probabilistic/ML inference proposals. Every inferred fact is labeled `DERIVED` or `INFERRED` and explainable ("why is this true?" returns the rule and premises). | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ONT-020 | Inference tiers: (a) graph-native derivations (transitive, inverse, symmetric, property chains), (b) rule-based (Datalog/SWRL-class) materialization with provenance, (c) OWL-RL/EL profile reasoning where RDF back-ends support it, (d) probabilistic/ML inference proposals. Every inferred fact is labeled DERIVED or INFERRED and explainable ("why is this true?" returns»
- [ ] Inference tiers: (a) graph-native derivations (transitive, inverse, symmetric, property chains), (b) rule-based (Datalog/SWRL-class) materialization with provenance, (c) OWL-RL/EL profile reasoning where RDF back-ends support it, (d) probabilistic/ML inference proposals. Every inferred fact is labeled DERIVED or INFERRED and explainable ("why is this true?" returns the rule and premises).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ONT-021 [P1] SR-ONT-021: Truth maintenance: retraction of premises retracts conclusions; contradictions are surfaced as validation findings, never silently resolved

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:523-523` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ONT-021 | **Truth maintenance:** retraction of premises retracts conclusions; contradictions are surfaced as validation findings, never silently resolved. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ONT-021 | Truth maintenance: retraction of premises retracts conclusions; contradictions are surfaced as validation findings, never silently resolved. | P1»
- [ ] Truth maintenance: retraction of premises retracts conclusions; contradictions are surfaced as validation findings, never silently resolved.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ONT-022 [P1] SR-ONT-022: Temporal and defeasible semantics for roles/ownership that change over time (valid-time intervals on edges)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:524-524` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ONT-022 | **Temporal and defeasible semantics** for roles/ownership that change over time (valid-time intervals on edges). | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ONT-022 | Temporal and defeasible semantics for roles/ownership that change over time (valid-time intervals on edges). | P1»
- [ ] Temporal and defeasible semantics for roles/ownership that change over time (valid-time intervals on edges).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-OPS-006 [P1] SR-OPS-006: Cost/FinOps views for cloud profiles (storage, compute, LLM tokens) and capacity views for on-prem

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:914-914` (table_row) · **Type:** Infra · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-OPS-006 | **Cost/FinOps views** for cloud profiles (storage, compute, LLM tokens) and capacity views for on-prem. | P2
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-OPS-006 | Cost/FinOps views for cloud profiles (storage, compute, LLM tokens) and capacity views for on-prem. | P2»
- [ ] Cost/FinOps views for cloud profiles (storage, compute, LLM tokens) and capacity views for on-prem.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-PRV-004 [P1] SR-PRV-004: Purpose and consent tracking where applicable; purpose limitation enforced in policy

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:851-851` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-PRV-004 | **Purpose and consent tracking** where applicable; purpose limitation enforced in policy. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-PRV-004 | Purpose and consent tracking where applicable; purpose limitation enforced in policy. | P1»
- [ ] Purpose and consent tracking where applicable; purpose limitation enforced in policy.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/privacy/consent.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/privacy/consent.py#L1-L1)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-PRV-005 [P1] SR-PRV-005: Compliance from the graph: auto-generate records of processing, data maps, data-flow diagrams, system-to-data-class inventories, cross-border transfer views and DPIA starter reports from the graph its

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:852-852` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-PRV-005 | **Compliance from the graph:** auto-generate records of processing, data maps, data-flow diagrams, system-to-data-class inventories, cross-border transfer views and DPIA starter reports from the graph itself. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-PRV-005 | Compliance from the graph: auto-generate records of processing, data maps, data-flow diagrams, system-to-data-class inventories, cross-border transfer views and DPIA starter reports from the graph itself. | P1»
- [ ] Compliance from the graph: auto-generate records of processing, data maps, data-flow diagrams, system-to-data-class inventories, cross-border transfer views and DPIA starter reports from the graph itself.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/privacy/consent.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/privacy/consent.py#L11-L11)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-PRV-007 [P1] SR-PRV-007: Pseudonymization/anonymization services (tokenization, k-anonymity checks, optional differential-privacy aggregates)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:854-854` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-PRV-007 | **Pseudonymization/anonymization services** (tokenization, k-anonymity checks, optional differential-privacy aggregates). | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-PRV-007 | Pseudonymization/anonymization services (tokenization, k-anonymity checks, optional differential-privacy aggregates). | P1»
- [ ] Pseudonymization/anonymization services (tokenization, k-anonymity checks, optional differential-privacy aggregates).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-QRY-008 [P1] SR-QRY-008: Graph algorithm library callable from plans (≥ 60 algorithms by P1): shortest/k-shortest/all-simple paths, reachability, SCC/WCC, topological order and cycle detection, dominators/critical path, PageR

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:319-319` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QRY-008 | **Graph algorithm library** callable from plans (≥ 60 algorithms by P1): shortest/k-shortest/all-simple paths, reachability, SCC/WCC, topological order and cycle detection, dominators/critical path, PageRank/personalized PageRank, betweenness/closeness/degree/eigenvector centrality, community detection (Leiden/Louvain/label propagation), triangle/clustering/k-core, similarity (Jaccard/cosine/Adamic-Adar), node embeddings (node2vec/GraphSAGE-class), link prediction, motif matching, temporal paths, flow/cut, subgraph isomorphism/pattern matching. Each declares complexity and sampling/approximation modes. | P0 (core 30) / P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QRY-008 | Graph algorithm library callable from plans (≥ 60 algorithms by P1): shortest/k-shortest/all-simple paths, reachability, SCC/WCC, topological order and cycle detection, dominators/critical path, PageRank/personalized PageRank, betweenness/closeness/degree/eigenvector centrality, community detection (Leiden/Louvain/label propagation), triangle/clustering/k-core, sim»
- [ ] Graph algorithm library callable from plans (≥ 60 algorithms by P1): shortest/k-shortest/all-simple paths, reachability, SCC/WCC, topological order and cycle detection, dominators/critical path, PageRank/personalized PageRank, betweenness/closeness/degree/eigenvector centrality, community detection (Leiden/Louvain/label propagation), triangle/clustering/k-core, similarity (Jaccard/cosine/Adamic-Ad
- [ ] P0 (core 30) / P1
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-QRY-009 [P1] SR-QRY-009: Incremental / precomputed accelerators: transitive-closure or reachability indexes for impact queries, materialized views per persona, summary edges, and top-k caches, all invalidated by graph-revisio

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:320-320` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QRY-009 | **Incremental / precomputed accelerators:** transitive-closure or reachability indexes for impact queries, materialized views per persona, summary edges, and top-k caches, all invalidated by graph-revision events. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QRY-009 | Incremental / precomputed accelerators: transitive-closure or reachability indexes for impact queries, materialized views per persona, summary edges, and top-k caches, all invalidated by graph-revision events. | P1»
- [ ] Incremental / precomputed accelerators: transitive-closure or reachability indexes for impact queries, materialized views per persona, summary edges, and top-k caches, all invalidated by graph-revision events.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-QRY-011 [P1] SR-QRY-011: Time travel: AS OF, BETWEEN, DIFF over revisions for every query class where backends or the revision store allow

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:322-322` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QRY-011 | **Time travel:** `AS OF`, `BETWEEN`, `DIFF` over revisions for every query class where backends or the revision store allow. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QRY-011 | Time travel: AS OF, BETWEEN, DIFF over revisions for every query class where backends or the revision store allow. | P1»
- [ ] Time travel: AS OF, BETWEEN, DIFF over revisions for every query class where backends or the revision store allow.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-QRY-012 [P1] SR-QRY-012: Multilingual query front-ends (NL, EOQL) with locale-aware date/number handling

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:323-323` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QRY-012 | **Multilingual query front-ends** (NL, EOQL) with locale-aware date/number handling. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QRY-012 | Multilingual query front-ends (NL, EOQL) with locale-aware date/number handling. | P1»
- [ ] Multilingual query front-ends (NL, EOQL) with locale-aware date/number handling.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-RAG-004 [P1] SR-RAG-004: Advanced strategies as plugins: HyDE, query decomposition, step-back, RAG-Fusion, parent-child chunking, sentence-window, self-RAG/corrective-RAG, agentic RAG loops, long-context packing with budget m

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:566-566` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-RAG-004 | **Advanced strategies as plugins:** HyDE, query decomposition, step-back, RAG-Fusion, parent-child chunking, sentence-window, self-RAG/corrective-RAG, agentic RAG loops, long-context packing with budget manager. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-RAG-004 | Advanced strategies as plugins: HyDE, query decomposition, step-back, RAG-Fusion, parent-child chunking, sentence-window, self-RAG/corrective-RAG, agentic RAG loops, long-context packing with budget manager. | P1»
- [ ] Advanced strategies as plugins: HyDE, query decomposition, step-back, RAG-Fusion, parent-child chunking, sentence-window, self-RAG/corrective-RAG, agentic RAG loops, long-context packing with budget manager.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-RAG-009 [P1] SR-RAG-009: Caching: semantic and exact caches keyed by tenant, policy version, graph revision and model version; invalidated by revision events

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:571-571` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-RAG-009 | **Caching:** semantic and exact caches keyed by tenant, policy version, graph revision and model version; invalidated by revision events. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-RAG-009 | Caching: semantic and exact caches keyed by tenant, policy version, graph revision and model version; invalidated by revision events. | P1»
- [ ] Caching: semantic and exact caches keyed by tenant, policy version, graph revision and model version; invalidated by revision events.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-SEC-005 [P1] SR-SEC-005: Access governance: access reviews/certification campaigns, privileged-access workflows, break-glass with mandatory post-hoc review

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:828-828` (table_row) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-SEC-005 | **Access governance:** access reviews/certification campaigns, privileged-access workflows, break-glass with mandatory post-hoc review. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-SEC-005 | Access governance: access reviews/certification campaigns, privileged-access workflows, break-glass with mandatory post-hoc review. | P1»
- [ ] Access governance: access reviews/certification campaigns, privileged-access workflows, break-glass with mandatory post-hoc review.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-TEN-010 [P1] SR-TEN-010: Cross-tenant sharing (opt-in): controlled sharing of ontologies, mappings, templates and anonymized benchmarks; never raw data; always explicit and auditable

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:727-727` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-TEN-010 | **Cross-tenant sharing (opt-in):** controlled sharing of ontologies, mappings, templates and anonymized benchmarks; never raw data; always explicit and auditable. | P2
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-TEN-010 | Cross-tenant sharing (opt-in): controlled sharing of ontologies, mappings, templates and anonymized benchmarks; never raw data; always explicit and auditable. | P2»
- [ ] Cross-tenant sharing (opt-in): controlled sharing of ontologies, mappings, templates and anonymized benchmarks; never raw data; always explicit and auditable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/tenancy/__init__.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/__init__.py#L15-L15)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-UX-003 [P1] SR-UX-003: Alternate views: table, matrix (dependency/DSM), tree/hierarchy, Sankey/flow, timeline/scrubber (temporal), geo-map, diff view between revisions

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:805-805` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-UX-003 | **Alternate views:** table, matrix (dependency/DSM), tree/hierarchy, Sankey/flow, timeline/scrubber (temporal), geo-map, diff view between revisions. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-UX-003 | Alternate views: table, matrix (dependency/DSM), tree/hierarchy, Sankey/flow, timeline/scrubber (temporal), geo-map, diff view between revisions. | P1»
- [ ] Alternate views: table, matrix (dependency/DSM), tree/hierarchy, Sankey/flow, timeline/scrubber (temporal), geo-map, diff view between revisions.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-UX-006 [P1] SR-UX-006: Persona-based homes and role-aware navigation (executive, architect, engineer, steward, auditor, admin), fully configurable

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:808-808` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-UX-006 | **Persona-based homes** and role-aware navigation (executive, architect, engineer, steward, auditor, admin), fully configurable. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-UX-006 | Persona-based homes and role-aware navigation (executive, architect, engineer, steward, auditor, admin), fully configurable. | P1»
- [ ] Persona-based homes and role-aware navigation (executive, architect, engineer, steward, auditor, admin), fully configurable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-UX-007 [P1] SR-UX-007: Collaboration: comments, annotations, @mentions, shared investigations/views, review of proposed ontology/mapping changes, activity feed

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:809-809` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-UX-007 | **Collaboration:** comments, annotations, @mentions, shared investigations/views, review of proposed ontology/mapping changes, activity feed. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-UX-007 | Collaboration: comments, annotations, @mentions, shared investigations/views, review of proposed ontology/mapping changes, activity feed. | P1»
- [ ] Collaboration: comments, annotations, @mentions, shared investigations/views, review of proposed ontology/mapping changes, activity feed.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-UX-009 [P1] SR-UX-009: Responsive and mobile read: tablet/phone views for answers, alerts and approvals

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:811-811` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-UX-009 | **Responsive and mobile read:** tablet/phone views for answers, alerts and approvals. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-UX-009 | Responsive and mobile read: tablet/phone views for answers, alerts and approvals. | P1»
- [ ] Responsive and mobile read: tablet/phone views for answers, alerts and approvals.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-UX-012 [P1] SR-UX-012: Performance budget: initial load ≤ 3 s on reference hardware over LAN; interactions ≤ 200 ms for local operations

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:814-814` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-UX-012 | **Performance budget:** initial load ≤ 3 s on reference hardware over LAN; interactions ≤ 200 ms for local operations. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-UX-012 | Performance budget: initial load ≤ 3 s on reference hardware over LAN; interactions ≤ 200 ms for local operations. | P1»
- [ ] Performance budget: initial load ≤ 3 s on reference hardware over LAN; interactions ≤ 200 ms for local operations.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-VDB-003 [P1] SR-VDB-003: Index strategies configurable: HNSW, IVF-PQ, DiskANN-class disk indexes, scalar/product/binary quantization, filtered-search strategies, per-collection recall/latency targets

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:229-229` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-VDB-003 | **Index strategies configurable:** HNSW, IVF-PQ, DiskANN-class disk indexes, scalar/product/binary quantization, filtered-search strategies, per-collection recall/latency targets. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-VDB-003 | Index strategies configurable: HNSW, IVF-PQ, DiskANN-class disk indexes, scalar/product/binary quantization, filtered-search strategies, per-collection recall/latency targets. | P1»
- [ ] Index strategies configurable: HNSW, IVF-PQ, DiskANN-class disk indexes, scalar/product/binary quantization, filtered-search strategies, per-collection recall/latency targets.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-WL-005 [P1] SR-WL-005: OEM rebuild pipeline: partners can produce rebranded, re-signed bundles/appliance images from a documented pipeline; partner-owned update channel and docs portal

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:737-737` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-WL-005 | **OEM rebuild pipeline:** partners can produce rebranded, re-signed bundles/appliance images from a documented pipeline; partner-owned update channel and docs portal. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-WL-005 | OEM rebuild pipeline: partners can produce rebranded, re-signed bundles/appliance images from a documented pipeline; partner-owned update channel and docs portal. | P1»
- [ ] OEM rebuild pipeline: partners can produce rebranded, re-signed bundles/appliance images from a documented pipeline; partner-owned update channel and docs portal.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-WL-008 [P1] SR-WL-008: Partner console: create/branding/configure tenants, view fleet health and usage, apply partner policy floors, issue licenses, manage support entitlements

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:740-740` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-WL-008 | **Partner console:** create/branding/configure tenants, view fleet health and usage, apply partner policy floors, issue licenses, manage support entitlements. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-WL-008 | Partner console: create/branding/configure tenants, view fleet health and usage, apply partner policy floors, issue licenses, manage support entitlements. | P1»
- [ ] Partner console: create/branding/configure tenants, view fleet health and usage, apply partner policy floors, issue licenses, manage support entitlements.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-WL-009 [P1] SR-WL-009: Embeddable components: iframe/web-component widgets (NL console, graph viewer, impact panel) with token-based auth for embedding in customer or partner portals

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:741-741` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-WL-009 | **Embeddable components:** iframe/web-component widgets (NL console, graph viewer, impact panel) with token-based auth for embedding in customer or partner portals. | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-WL-009 | Embeddable components: iframe/web-component widgets (NL console, graph viewer, impact panel) with token-based auth for embedding in customer or partner portals. | P1»
- [ ] Embeddable components: iframe/web-component widgets (NL console, graph viewer, impact panel) with token-based auth for embedding in customer or partner portals.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-026 [P2] SR-AGT-026: Anomaly detection on graph structure, ingestion patterns and access behavior

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:703-703` (table_row) · **Type:** AI · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-026 | **Anomaly detection** on graph structure, ingestion patterns and access behavior. | P2
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-026 | Anomaly detection on graph structure, ingestion patterns and access behavior. | P2»
- [ ] Anomaly detection on graph structure, ingestion patterns and access behavior.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-028 [P2] SR-AGT-028: Onboarding and tours: auto-generated "map of this domain" guides for newcomers from the graph

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:705-705` (table_row) · **Type:** AI · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-028 | **Onboarding and tours:** auto-generated "map of this domain" guides for newcomers from the graph. | P2
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-028 | Onboarding and tours: auto-generated "map of this domain" guides for newcomers from the graph. | P2»
- [ ] Onboarding and tours: auto-generated "map of this domain" guides for newcomers from the graph.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ARC-009 [P2] SR-ARC-009: Federation: queries MAY span multiple graph backends and multiple sites (hub-and-spoke or mesh) with partial-result semantics, per-site policy enforcement and no raw-data movement unless permitted

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:170-170` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ARC-009 | **Federation:** queries MAY span multiple graph backends and multiple sites (hub-and-spoke or mesh) with partial-result semantics, per-site policy enforcement and no raw-data movement unless permitted. | P2
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ARC-009 | Federation: queries MAY span multiple graph backends and multiple sites (hub-and-spoke or mesh) with partial-result semantics, per-site policy enforcement and no raw-data movement unless permitted. | P2»
- [ ] Federation: queries MAY span multiple graph backends and multiple sites (hub-and-spoke or mesh) with partial-result semantics, per-site policy enforcement and no raw-data movement unless permitted.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-CON-014 [P2] SR-CON-014: A tenant MUST be able to switch a capability between local and cloud providers via migration tooling (e.g., local object store → cloud bucket) with verification and rollback

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:128-128` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CON-014 | A tenant MUST be able to switch a capability between local and cloud providers via migration tooling (e.g., local object store → cloud bucket) with verification and rollback. | P2
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CON-014 | A tenant MUST be able to switch a capability between local and cloud providers via migration tooling (e.g., local object store → cloud bucket) with verification and rollback. | P2»
- [ ] A tenant MUST be able to switch a capability between local and cloud providers via migration tooling (e.g., local object store → cloud bucket) with verification and rollback.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-DEP-004 [P2] SR-DEP-004: Appliance image (hardware + software; CPU and GPU variants) with hardened OS, first-boot wizard, lifecycle updates

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:925-925` (table_row) · **Type:** Infra · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-DEP-004 | **Appliance image** (hardware + software; CPU and GPU variants) with hardened OS, first-boot wizard, lifecycle updates. | P2
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-DEP-004 | Appliance image (hardware + software; CPU and GPU variants) with hardened OS, first-boot wizard, lifecycle updates. | P2»
- [ ] Appliance image (hardware + software; CPU and GPU variants) with hardened OS, first-boot wizard, lifecycle updates.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-DEP-005 [P2] SR-DEP-005: Native packages (RPM/DEB) and VM images for customers without containers

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:926-926` (table_row) · **Type:** Infra · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-DEP-005 | **Native packages** (RPM/DEB) and VM images for customers without containers. | P2
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-DEP-005 | Native packages (RPM/DEB) and VM images for customers without containers. | P2»
- [ ] Native packages (RPM/DEB) and VM images for customers without containers.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-DEP-008 [P2] SR-DEP-008: Edge/federation package for DP-6: small footprint, offline-first, delta/summary sync with conflict policies and bandwidth limits

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:929-929` (table_row) · **Type:** Infra · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-DEP-008 | **Edge/federation package** for DP-6: small footprint, offline-first, delta/summary sync with conflict policies and bandwidth limits. | P2
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-DEP-008 | Edge/federation package for DP-6: small footprint, offline-first, delta/summary sync with conflict policies and bandwidth limits. | P2»
- [ ] Edge/federation package for DP-6: small footprint, offline-first, delta/summary sync with conflict policies and bandwidth limits.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-GDB-007 [P2] SR-GDB-007: Virtual/zero-ETL graph mode: optionally expose existing relational/lakehouse data as a graph view through declarative mappings (OBDA/virtual-graph style) without copying data

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:189-189` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GDB-007 | **Virtual/zero-ETL graph mode:** optionally expose existing relational/lakehouse data as a graph view through declarative mappings (OBDA/virtual-graph style) without copying data. | P2
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GDB-007 | Virtual/zero-ETL graph mode: optionally expose existing relational/lakehouse data as a graph view through declarative mappings (OBDA/virtual-graph style) without copying data. | P2»
- [ ] Virtual/zero-ETL graph mode: optionally expose existing relational/lakehouse data as a graph view through declarative mappings (OBDA/virtual-graph style) without copying data.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-GDB-011 [P2] SR-GDB-011: Relational metadata/config store: PostgreSQL as the clustered default, SQLite for single-node DP-0; ports allow customer-standard engines (SQL Server, Oracle, MySQL/MariaDB) at P2

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:216-216` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GDB-011 | **Relational metadata/config store:** PostgreSQL as the clustered default, SQLite for single-node DP-0; ports allow customer-standard engines (SQL Server, Oracle, MySQL/MariaDB) at P2. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GDB-011 | Relational metadata/config store: PostgreSQL as the clustered default, SQLite for single-node DP-0; ports allow customer-standard engines (SQL Server, Oracle, MySQL/MariaDB) at P2. | P0»
- [ ] Relational metadata/config store: PostgreSQL as the clustered default, SQLite for single-node DP-0; ports allow customer-standard engines (SQL Server, Oracle, MySQL/MariaDB) at P2.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-018 [P2] SR-ING-018: Link prediction / graph completion (heuristic and learned, e.g., translational and GNN-class models) proposes missing edges into a review queue; auto-assertion only above a tenant-configured threshold

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:387-387` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-018 | **Link prediction / graph completion** (heuristic and learned, e.g., translational and GNN-class models) proposes missing edges into a review queue; auto-assertion only above a tenant-configured threshold. | P2
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-018 | Link prediction / graph completion (heuristic and learned, e.g., translational and GNN-class models) proposes missing edges into a review queue; auto-assertion only above a tenant-configured threshold. | P2»
- [ ] Link prediction / graph completion (heuristic and learned, e.g., translational and GNN-class models) proposes missing edges into a review queue; auto-assertion only above a tenant-configured threshold.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-NLQ-013 [P2] SR-NLQ-013: Voice and chat surfaces: same pipeline via chat apps (Teams/Slack-class), IDE chat, CLI, and optional speech I/O

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:592-592` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NLQ-013 | **Voice and chat surfaces:** same pipeline via chat apps (Teams/Slack-class), IDE chat, CLI, and optional speech I/O. | P2
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NLQ-013 | Voice and chat surfaces: same pipeline via chat apps (Teams/Slack-class), IDE chat, CLI, and optional speech I/O. | P2»
- [ ] Voice and chat surfaces: same pipeline via chat apps (Teams/Slack-class), IDE chat, CLI, and optional speech I/O.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

