# EPIC-EOIPMASTER-NOTRUN: EOIP-master-requirements.md · tests_not_executed

*Tests are mapped/referenced but none ran in the audit (excluded or not collected).* 18 tasks, ~18.0 h, priorities {'P0': 2, 'P1': 11, 'P2': 5}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-CAP-07 [P0] CAP-07: Supernode handling and degree skew · D01 Storage · P0

- **Source:** `EOIP-master-requirements.md:45-45` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-07` | **Supernode handling and degree skew** | D01 Storage | `P0` | 100% Implemented & Verified (Parallel CSR fan-out throttling & streaming batch iterators; zero OOM on high degree) | **VERIFIED**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:21, scripts/test_master_caps_enrichment.py:35
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-07 | Supernode handling and degree skew | D01 Storage | P0 | 100% Implemented & Verified (Parallel CSR fan-out throttling & streaming batch iterators; zero OOM on high degree) | VERIFIED»
- [ ] Supernode handling and degree skew
- [ ] 100% Implemented & Verified (Parallel CSR fan-out throttling & streaming batch iterators; zero OOM on high degree)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:152`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L152-L152), [`scripts/investigate_caps.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L10-L10), [`scripts/patch_suite_and_dashboard.py:73`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L73-L73), [`scripts/update_matrix_caps.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L9-L9), [`scripts/verify_22_caps.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L24-L24)
- tests: `scripts/test_cap_enrichment.py:21`, `scripts/test_master_caps_enrichment.py:35`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-10 [P0] CAP-10: SHACL shape validation · D02 Schema · P0

- **Source:** `EOIP-master-requirements.md:48-48` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-10` | **SHACL shape validation** | D02 Schema | `P0` | 100% Implemented & Verified (WP-KG3-05, CRA-020.1 Verified; 100% pass on W3C SHACL Core constraints) | **VERIFIED**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:33, scripts/test_master_caps_enrichment.py:47
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-10 | SHACL shape validation | D02 Schema | P0 | 100% Implemented & Verified (WP-KG3-05, CRA-020.1 Verified; 100% pass on W3C SHACL Core constraints) | VERIFIED»
- [ ] 100% Implemented & Verified (WP-KG3-05, CRA-020.1 Verified; 100% pass on W3C SHACL Core constraints)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:164`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L164-L164), [`scripts/enhance_master_suite.py:176`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L176-L176), [`scripts/investigate_caps.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L10-L10), [`scripts/patch_suite_and_dashboard.py:42`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L42-L42), [`scripts/update_matrix_caps.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L11-L11), [`scripts/verify_22_caps.py:38`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L38-L38)
- tests: `scripts/test_cap_enrichment.py:33`, `scripts/test_master_caps_enrichment.py:47`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-02 [P1] CAP-02: RDF/quad storage and named graphs · D01 Storage · P1

- **Source:** `EOIP-master-requirements.md:40-40` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-02` | **RDF/quad storage and named graphs** | D01 Storage | `P1` | 100% Implemented & Verified (W3C N-Quads, Trig serialization, tenant-scoped named graph isolation) | **VERIFIED**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:7, scripts/test_master_caps_enrichment.py:21
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-02 | RDF/quad storage and named graphs | D01 Storage | P1 | 100% Implemented & Verified (W3C N-Quads, Trig serialization, tenant-scoped named graph isolation) | VERIFIED»
- [ ] RDF/quad storage and named graphs
- [ ] 100% Implemented & Verified (W3C N-Quads, Trig serialization, tenant-scoped named graph isolation)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:138`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L138-L138), [`scripts/investigate_caps.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L10-L10), [`scripts/patch_suite_and_dashboard.py:59`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L59-L59), [`scripts/update_matrix_caps.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L7-L7), [`scripts/verify_22_caps.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L10-L10)
- tests: `scripts/test_cap_enrichment.py:7`, `scripts/test_master_caps_enrichment.py:21`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-09 [P1] CAP-09: Ontology modeling (RDFS/OWL 2) · D02 Schema · P1

- **Source:** `EOIP-master-requirements.md:47-47` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-09` | **Ontology modeling (RDFS/OWL 2)** | D02 Schema | `P1` | 100% Implemented & Verified (LinkML metamodel + OWL 2 Class, ObjectProperty, DatatypeProperty, SubClassOf, DisjointClasses) | **VERIFIED**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:27, scripts/test_master_caps_enrichment.py:41
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-09 | Ontology modeling (RDFS/OWL 2) | D02 Schema | P1 | 100% Implemented & Verified (LinkML metamodel + OWL 2 Class, ObjectProperty, DatatypeProperty, SubClassOf, DisjointClasses) | VERIFIED»
- [ ] Ontology modeling (RDFS/OWL 2)
- [ ] 100% Implemented & Verified (LinkML metamodel + OWL 2 Class, ObjectProperty, DatatypeProperty, SubClassOf, DisjointClasses)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:158`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L158-L158), [`scripts/investigate_caps.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L12-L12), [`scripts/patch_suite_and_dashboard.py:79`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L79-L79), [`scripts/update_matrix_caps.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L10-L10), [`scripts/verify_22_caps.py:31`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L31-L31)
- tests: `scripts/test_cap_enrichment.py:27`, `scripts/test_master_caps_enrichment.py:41`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-12 [P1] CAP-12: Taxonomy and SKOS concept management · D02 Schema · P1

- **Source:** `EOIP-master-requirements.md:50-50` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-12` | **Taxonomy and SKOS concept management** | D02 Schema | `P1` | 100% Implemented & Verified (SKOS ConceptScheme, broader/narrower/related, multilingual prefLabel/altLabel) | **VERIFIED**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:39, scripts/test_master_caps_enrichment.py:53
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-12 | Taxonomy and SKOS concept management | D02 Schema | P1 | 100% Implemented & Verified (SKOS ConceptScheme, broader/narrower/related, multilingual prefLabel/altLabel) | VERIFIED»
- [ ] Taxonomy and SKOS concept management
- [ ] 100% Implemented & Verified (SKOS ConceptScheme, broader/narrower/related, multilingual prefLabel/altLabel)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:170`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L170-L170), [`scripts/investigate_caps.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L12-L12), [`scripts/patch_suite_and_dashboard.py:91`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L91-L91), [`scripts/update_matrix_caps.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L12-L12), [`scripts/verify_22_caps.py:45`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L45-L45)
- tests: `scripts/test_cap_enrichment.py:39`, `scripts/test_master_caps_enrichment.py:53`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-15 [P1] CAP-15: W3C SPARQL 1.1 query execution · D02 Schema · P1

- **Source:** `EOIP-master-requirements.md:53-53` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-15` | **W3C SPARQL 1.1 query execution** | D02 Schema | `P1` | 100% Implemented & Verified (Federated SELECT, ASK, CONSTRUCT, DESCRIBE with SPARQL 1.1 protocol translation) | **VERIFIED**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:45, scripts/test_master_caps_enrichment.py:59
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-15 | W3C SPARQL 1.1 query execution | D02 Schema | P1 | 100% Implemented & Verified (Federated SELECT, ASK, CONSTRUCT, DESCRIBE with SPARQL 1.1 protocol translation) | VERIFIED»
- [ ] W3C SPARQL 1.1 query execution
- [ ] 100% Implemented & Verified (Federated SELECT, ASK, CONSTRUCT, DESCRIBE with SPARQL 1.1 protocol translation)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:176`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L176-L176), [`scripts/investigate_caps.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L12-L12), [`scripts/patch_suite_and_dashboard.py:97`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L97-L97), [`scripts/update_matrix_caps.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L13-L13), [`scripts/verify_22_caps.py:52`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L52-L52)
- tests: `scripts/test_cap_enrichment.py:45`, `scripts/test_master_caps_enrichment.py:59`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-18 [P1] CAP-18: Cost-based query optimization & WCOJ · D03 Query · P1

- **Source:** `EOIP-master-requirements.md:56-56` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-18` | **Cost-based query optimization & WCOJ** | D03 Query | `P1` | 100% Implemented & Verified (Cardinality estimation, selectivity scoring, push-down predicates in QueryPlan) | **VERIFIED**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:63, scripts/test_master_caps_enrichment.py:77
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-18 | Cost-based query optimization & WCOJ | D03 Query | P1 | 100% Implemented & Verified (Cardinality estimation, selectivity scoring, push-down predicates in QueryPlan) | VERIFIED»
- [ ] Cost-based query optimization & WCOJ
- [ ] 100% Implemented & Verified (Cardinality estimation, selectivity scoring, push-down predicates in QueryPlan)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:194`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L194-L194), [`scripts/investigate_caps.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L12-L12), [`scripts/patch_suite_and_dashboard.py:115`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L115-L115), [`scripts/update_matrix_caps.py:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L16-L16), [`scripts/verify_22_caps.py:73`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L73-L73)
- tests: `scripts/test_cap_enrichment.py:63`, `scripts/test_master_caps_enrichment.py:77`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-21 [P1] CAP-21: Federation and virtualization (OBDA) · D03 Query · P1

- **Source:** `EOIP-master-requirements.md:59-59` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-21` | **Federation and virtualization (OBDA)** | D03 Query | `P1` | 100% Implemented & Verified (R2RML-compatible virtual relational-to-graph mapping with phantom graph views without ETL) | **VERIFIED**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:75, scripts/test_master_caps_enrichment.py:89
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-21 | Federation and virtualization (OBDA) | D03 Query | P1 | 100% Implemented & Verified (R2RML-compatible virtual relational-to-graph mapping with phantom graph views without ETL) | VERIFIED»
- [ ] Federation and virtualization (OBDA)
- [ ] 100% Implemented & Verified (R2RML-compatible virtual relational-to-graph mapping with phantom graph views without ETL)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:206`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L206-L206), [`scripts/investigate_caps.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L12-L12), [`scripts/patch_suite_and_dashboard.py:127`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L127-L127), [`scripts/update_matrix_caps.py:18`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L18-L18), [`scripts/verify_22_caps.py:87`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L87-L87)
- tests: `scripts/test_cap_enrichment.py:75`, `scripts/test_master_caps_enrichment.py:89`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-22 [P1] CAP-22: Incremental rule / Datalog materialization · D03 Query · P1

- **Source:** `EOIP-master-requirements.md:60-60` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-22` | **Incremental rule / Datalog materialization** | D03 Query | `P1` | 100% Implemented & Verified (WP-KG3-10, CRA-019.1 Verified; Bitemporal delta CRDT with O(1) state-machine transaction retractions) | **VERIFIED**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:81, scripts/test_master_caps_enrichment.py:95
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-22 | Incremental rule / Datalog materialization | D03 Query | P1 | 100% Implemented & Verified (WP-KG3-10, CRA-019.1 Verified; Bitemporal delta CRDT with O(1) state-machine transaction retractions) | VERIFIED»
- [ ] Incremental rule / Datalog materialization
- [ ] 100% Implemented & Verified (WP-KG3-10, CRA-019.1 Verified; Bitemporal delta CRDT with O(1) state-machine transaction retractions)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:212`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L212-L212), [`scripts/investigate_caps.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L10-L10), [`scripts/patch_suite_and_dashboard.py:133`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L133-L133), [`scripts/update_matrix_caps.py:19`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L19-L19), [`scripts/verify_22_caps.py:94`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L94-L94)
- tests: `scripts/test_cap_enrichment.py:81`, `scripts/test_master_caps_enrichment.py:95`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-23 [P1] CAP-23: OWL 2 profile reasoning (RL/QL/EL) · D03 Query · P1

- **Source:** `EOIP-master-requirements.md:61-61` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-23` | **OWL 2 profile reasoning (RL/QL/EL)** | D03 Query | `P1` | 100% Implemented & Verified (Subclass subsumption, disjointness checking, and transitive property chain inference) | **VERIFIED**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:87, scripts/test_master_caps_enrichment.py:101
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-23 | OWL 2 profile reasoning (RL/QL/EL) | D03 Query | P1 | 100% Implemented & Verified (Subclass subsumption, disjointness checking, and transitive property chain inference) | VERIFIED»
- [ ] OWL 2 profile reasoning (RL/QL/EL)
- [ ] 100% Implemented & Verified (Subclass subsumption, disjointness checking, and transitive property chain inference)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:218`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L218-L218), [`scripts/investigate_caps.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L11-L11), [`scripts/patch_suite_and_dashboard.py:139`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L139-L139), [`scripts/update_matrix_caps.py:20`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L20-L20), [`scripts/verify_22_caps.py:101`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L101-L101)
- tests: `scripts/test_cap_enrichment.py:87`, `scripts/test_master_caps_enrichment.py:101`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-37 [P1] CAP-37: Schema and ontology evolution with migrations · D05 Identity · P1

- **Source:** `EOIP-master-requirements.md:75-75` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-37` | **Schema and ontology evolution with migrations** | D05 Identity | `P1` | 100% Implemented & Verified (WP-KG3-06, CRA-022.1 Verified; GitOps ontology-as-code with LinkML CI linting & schema diff) | **VERIFIED**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:99, scripts/test_master_caps_enrichment.py:113
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-37 | Schema and ontology evolution with migrations | D05 Identity | P1 | 100% Implemented & Verified (WP-KG3-06, CRA-022.1 Verified; GitOps ontology-as-code with LinkML CI linting & schema diff) | VERIFIED»
- [ ] Schema and ontology evolution with migrations
- [ ] 100% Implemented & Verified (WP-KG3-06, CRA-022.1 Verified; GitOps ontology-as-code with LinkML CI linting & schema diff)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:230`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L230-L230), [`scripts/investigate_caps.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L11-L11), [`scripts/patch_suite_and_dashboard.py:151`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L151-L151), [`scripts/update_matrix_caps.py:22`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L22-L22), [`scripts/verify_22_caps.py:115`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L115-L115)
- tests: `scripts/test_cap_enrichment.py:99`, `scripts/test_master_caps_enrichment.py:113`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-41 [P1] CAP-41: Ontology governance workflow · D06 Ingestion · P1

- **Source:** `EOIP-master-requirements.md:79-79` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-41` | **Ontology governance workflow** | D06 Ingestion | `P1` | 100% Implemented & Verified (WP-KG3-08, CRA-027.1 Verified; Multi-stage review gates, stewardship queues & approval-gated mutations) | **VERIFIED**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:105, scripts/test_master_caps_enrichment.py:119
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-41 | Ontology governance workflow | D06 Ingestion | P1 | 100% Implemented & Verified (WP-KG3-08, CRA-027.1 Verified; Multi-stage review gates, stewardship queues & approval-gated mutations) | VERIFIED»
- [ ] 100% Implemented & Verified (WP-KG3-08, CRA-027.1 Verified; Multi-stage review gates, stewardship queues & approval-gated mutations)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:236`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L236-L236), [`scripts/investigate_caps.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L11-L11), [`scripts/patch_suite_and_dashboard.py:157`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L157-L157), [`scripts/update_matrix_caps.py:23`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L23-L23), [`scripts/verify_22_caps.py:122`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L122-L122)
- tests: `scripts/test_cap_enrichment.py:105`, `scripts/test_master_caps_enrichment.py:119`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-53 [P1] CAP-53: Dense vector similarity search · D07 Security · P1

- **Source:** `EOIP-master-requirements.md:91-91` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-53` | **Dense vector similarity search** | D07 Security | `P1` | 100% Implemented & Verified (WP-KG3-07 / Tier 8; Pure-Python & NumPy dense vector similarity, HNSW indexing, Matryoshka embeddings) | **VERIFIED**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:123, scripts/test_master_caps_enrichment.py:137
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-53 | Dense vector similarity search | D07 Security | P1 | 100% Implemented & Verified (WP-KG3-07 / Tier 8; Pure-Python & NumPy dense vector similarity, HNSW indexing, Matryoshka embeddings) | VERIFIED»
- [ ] Dense vector similarity search
- [ ] 100% Implemented & Verified (WP-KG3-07 / Tier 8; Pure-Python & NumPy dense vector similarity, HNSW indexing, Matryoshka embeddings)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:254`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L254-L254), [`scripts/investigate_caps.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L12-L12), [`scripts/patch_suite_and_dashboard.py:175`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L175-L175), [`scripts/update_matrix_caps.py:26`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L26-L26), [`scripts/verify_22_caps.py:143`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L143-L143)
- tests: `scripts/test_cap_enrichment.py:123`, `scripts/test_master_caps_enrichment.py:137`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-05 [P2] CAP-05: Distributed scale-out and sharding · D01 Storage · P2

- **Source:** `EOIP-master-requirements.md:43-43` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-05` | **Distributed scale-out and sharding** | D01 Storage | `P2` | Architectural Sharding Implemented — Multi-Node Physical Cluster Roadmap (WP-KG3-12) | **ROADMAP**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:13, scripts/test_master_caps_enrichment.py:27
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-05 | Distributed scale-out and sharding | D01 Storage | P2 | Architectural Sharding Implemented — Multi-Node Physical Cluster Roadmap (WP-KG3-12) | ROADMAP»
- [ ] Distributed scale-out and sharding
- [ ] Architectural Sharding Implemented — Multi-Node Physical Cluster Roadmap (WP-KG3-12)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:144`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L144-L144), [`scripts/investigate_caps.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L10-L10), [`scripts/patch_suite_and_dashboard.py:65`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L65-L65), [`scripts/update_matrix_caps.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L8-L8), [`scripts/verify_22_caps.py:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L17-L17)
- tests: `scripts/test_cap_enrichment.py:13`, `scripts/test_master_caps_enrichment.py:27`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-16 [P2] CAP-16: SQL/PGQ and relational SQL bridges · D02 Schema · P2

- **Source:** `EOIP-master-requirements.md:54-54` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-16` | **SQL/PGQ and relational SQL bridges** | D02 Schema | `P2` | 100% Implemented & Verified (UniversalAST SQL MATCH and relational join transpilation to QueryPlan IR) | **VERIFIED**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:51, scripts/test_master_caps_enrichment.py:65
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-16 | SQL/PGQ and relational SQL bridges | D02 Schema | P2 | 100% Implemented & Verified (UniversalAST SQL MATCH and relational join transpilation to QueryPlan IR) | VERIFIED»
- [ ] SQL/PGQ and relational SQL bridges
- [ ] 100% Implemented & Verified (UniversalAST SQL MATCH and relational join transpilation to QueryPlan IR)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:182`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L182-L182), [`scripts/investigate_caps.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L10-L10), [`scripts/patch_suite_and_dashboard.py:103`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L103-L103), [`scripts/update_matrix_caps.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L14-L14), [`scripts/verify_22_caps.py:59`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L59-L59)
- tests: `scripts/test_cap_enrichment.py:51`, `scripts/test_master_caps_enrichment.py:65`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-17 [P2] CAP-17: GraphQL query and mutation API · D03 Query · P2

- **Source:** `EOIP-master-requirements.md:55-55` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-17` | **GraphQL query and mutation API** | D03 Query | `P2` | 100% Implemented & Verified (Typed schema exposition, queries, mutations at /api/v1/graphql) | **VERIFIED**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:57, scripts/test_master_caps_enrichment.py:71
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-17 | GraphQL query and mutation API | D03 Query | P2 | 100% Implemented & Verified (Typed schema exposition, queries, mutations at /api/v1/graphql) | VERIFIED»
- [ ] GraphQL query and mutation API
- [ ] 100% Implemented & Verified (Typed schema exposition, queries, mutations at /api/v1/graphql)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:188`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L188-L188), [`scripts/investigate_caps.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L11-L11), [`scripts/patch_suite_and_dashboard.py:109`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L109-L109), [`scripts/update_matrix_caps.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L15-L15), [`scripts/verify_22_caps.py:66`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L66-L66)
- tests: `scripts/test_cap_enrichment.py:57`, `scripts/test_master_caps_enrichment.py:71`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-63 [P2] CAP-63: Knowledge graph embeddings (KGE) · D08 Graph ML · P2

- **Source:** `EOIP-master-requirements.md:101-101` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-63` | **Knowledge graph embeddings (KGE)** | D08 Graph ML | `P2` | 100% Implemented & Verified (TransE / RotatE loss functions, low-dimensional vector projections, fusion, and drift detection) | **VERIFIED**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:129, scripts/test_master_caps_enrichment.py:149
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-63 | Knowledge graph embeddings (KGE) | D08 Graph ML | P2 | 100% Implemented & Verified (TransE / RotatE loss functions, low-dimensional vector projections, fusion, and drift detection) | VERIFIED»
- [ ] Knowledge graph embeddings (KGE)
- [ ] 100% Implemented & Verified (TransE / RotatE loss functions, low-dimensional vector projections, fusion, and drift detection)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:266`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L266-L266), [`scripts/investigate_caps.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L12-L12), [`scripts/patch_suite_and_dashboard.py:187`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L187-L187), [`scripts/update_matrix_caps.py:27`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L27-L27), [`scripts/verify_22_caps.py:150`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L150-L150)
- tests: `scripts/test_cap_enrichment.py:129`, `scripts/test_master_caps_enrichment.py:149`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-64 [P2] CAP-64: Graph Neural Networks (GNN) and link prediction · D08 Graph ML · P2

- **Source:** `EOIP-master-requirements.md:102-102` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-64` | **Graph Neural Networks (GNN) and link prediction** | D08 Graph ML | `P2` | 100% Implemented & Verified (Topology-aware GNN message passing, link prediction, anomaly detection, autonomous self-healing) | **VERIFIED**
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): scripts/test_cap_enrichment.py:135, scripts/test_master_caps_enrichment.py:155
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-64 | Graph Neural Networks (GNN) and link prediction | D08 Graph ML | P2 | 100% Implemented & Verified (Topology-aware GNN message passing, link prediction, anomaly detection, autonomous self-healing) | VERIFIED»
- [ ] Graph Neural Networks (GNN) and link prediction
- [ ] 100% Implemented & Verified (Topology-aware GNN message passing, link prediction, anomaly detection, autonomous self-healing)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:272`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L272-L272), [`scripts/investigate_caps.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/investigate_caps.py#L11-L11), [`scripts/patch_suite_and_dashboard.py:193`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L193-L193), [`scripts/update_matrix_caps.py:28`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L28-L28), [`scripts/verify_22_caps.py:157`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L157-L157)
- tests: `scripts/test_cap_enrichment.py:135`, `scripts/test_master_caps_enrichment.py:155`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

