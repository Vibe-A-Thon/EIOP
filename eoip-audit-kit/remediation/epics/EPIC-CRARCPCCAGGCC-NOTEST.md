# EPIC-CRARCPCCAGGCC-NOTEST: CRAr_cpccaggcc-requirements.md · code_no_test

*Code references the ID but no test is mapped.* 7 tasks, ~21.0 h, priorities {'P0': 1, 'P1': 2, 'P2': 4}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-ONT-009 [P0] ONT-009: Governed Action layer (write-back) · P0 · L

- **Source:** `CRAr_cpccaggcc-requirements.md:2628-2628` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 1 other site(s): see duplicate task DUP-ONT-009; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-009 | Governed Action layer (write-back) | P0 | L | Tier 1 — Differentiators | ONT-005 | CRA-027 | CRA-027.7
```
</details>

**Next steps**
1. Read the referenced code: packages/eoip/actions/contracts.py:75
2. Write one test per acceptance criterion; mark with @pytest.mark.req('ONT-009') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-ONT-009

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-009 | Governed Action layer (write-back) | P0 | L | Tier 1 — Differentiators | ONT-005 | CRA-027 | CRA-027.7»
- [ ] Governed Action layer (write-back)
- [ ] Tier 1 — Differentiators
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/actions/contracts.py:75`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/actions/contracts.py#L75-L75)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ONT-003 [P1] ONT-003: RDF backend port (Fuseki reference) · P1 · M

- **Source:** `CRAr_cpccaggcc-requirements.md:2622-2622` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 1 other site(s): see duplicate task DUP-ONT-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-003 | RDF backend port (Fuseki reference) | P1 | M | Tier 1 — Differentiators | ONT-001 | CRA-024 (+CRA-002) | CRA-002.10, CRA-024.11
```
</details>

**Next steps**
1. Read the referenced code: packages/eoip/graph/backends.py:345, packages/eoip/graph/rdf_backend.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('ONT-003') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-ONT-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-003 | RDF backend port (Fuseki reference) | P1 | M | Tier 1 — Differentiators | ONT-001 | CRA-024 (+CRA-002) | CRA-002.10, CRA-024.11»
- [ ] RDF backend port (Fuseki reference)
- [ ] Tier 1 — Differentiators
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/backends.py:345`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/backends.py#L345-L345), [`packages/eoip/graph/rdf_backend.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/rdf_backend.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ONT-006 [P1] ONT-006: AI-suggested CML mappings · P1 · M

- **Source:** `CRAr_cpccaggcc-requirements.md:2625-2625` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 1 other site(s): see duplicate task DUP-ONT-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-006 | AI-suggested CML mappings | P1 | M | Tier 1 — Differentiators | ONT-005 | CRA-017 (+CRA-026) | CRA-017.10
```
</details>

**Next steps**
1. Read the referenced code: packages/eoip/mapping/diagnostics.py:10
2. Write one test per acceptance criterion; mark with @pytest.mark.req('ONT-006') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-ONT-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-006 | AI-suggested CML mappings | P1 | M | Tier 1 — Differentiators | ONT-005 | CRA-017 (+CRA-026) | CRA-017.10»
- [ ] Tier 1 — Differentiators
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/mapping/diagnostics.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/mapping/diagnostics.py#L10-L10)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-002 [P2] GN-002: Assertion contract (prediction is not fact) · CRA-044.12, CRA-045.2 · X-34

- **Source:** `CRAr_cpccaggcc-requirements.md:2785-2785` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 10 other site(s): see duplicate task DUP-GN-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-002 | Assertion contract (prediction is not fact) | CRA-044.12, CRA-045.2 | X-34
```
</details>

**Next steps**
1. Read the referenced code: packages/eoip/neural/lifecycle.py:13
2. Write one test per acceptance criterion; mark with @pytest.mark.req('GN-002') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-GN-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-002 | Assertion contract (prediction is not fact) | CRA-044.12, CRA-045.2 | X-34»
- [ ] Assertion contract (prediction is not fact)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/neural/lifecycle.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/neural/lifecycle.py#L13-L13)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-012 [P2] GN-012: Determinism and reproducibility · CRA-043.6 · Cross-process 1e-4 gate (section 5.3)

- **Source:** `CRAr_cpccaggcc-requirements.md:2779-2779` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 9 other site(s): see duplicate task DUP-GN-012; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-012 | Determinism and reproducibility | CRA-043.6 | Cross-process 1e-4 gate (section 5.3)
```
</details>

**Next steps**
1. Read the referenced code: programme_rules.js:236
2. Write one test per acceptance criterion; mark with @pytest.mark.req('GN-012') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-GN-012

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-012 | Determinism and reproducibility | CRA-043.6 | Cross-process 1e-4 gate (section 5.3)»
- [ ] Cross-process 1e-4 gate (section 5.3)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`programme_rules.js:236`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/programme_rules.js#L236-L236)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ONT-015 [P2] ONT-015: DeepOnto alignment for pack merging · P2 · L

- **Source:** `CRAr_cpccaggcc-requirements.md:2634-2634` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 1 other site(s): see duplicate task DUP-ONT-015; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-015 | DeepOnto alignment for pack merging | P2 | L | Tier 2 — Completeness | ONT-007 | CRA-023 | CRA-023.7
```
</details>

**Next steps**
1. Read the referenced code: packages/eoip/identity/alignment.py:192
2. Write one test per acceptance criterion; mark with @pytest.mark.req('ONT-015') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-ONT-015

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-015 | DeepOnto alignment for pack merging | P2 | L | Tier 2 — Completeness | ONT-007 | CRA-023 | CRA-023.7»
- [ ] DeepOnto alignment for pack merging
- [ ] Tier 2 — Completeness
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/identity/alignment.py:192`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/identity/alignment.py#L192-L192)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ONT-017 [P2] ONT-017: R2RML / RML import to CML · P2 · M

- **Source:** `CRAr_cpccaggcc-requirements.md:2636-2636` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 1 other site(s): see duplicate task DUP-ONT-017; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-017 | R2RML / RML import to CML | P2 | M | Tier 2 — Completeness | ONT-005 | CRA-034 (+CRA-017) | CRA-017.7, CRA-034.8
```
</details>

**Next steps**
1. Read the referenced code: packages/eoip/migration/r2rml_importer.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('ONT-017') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-ONT-017

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-017 | R2RML / RML import to CML | P2 | M | Tier 2 — Completeness | ONT-005 | CRA-034 (+CRA-017) | CRA-017.7, CRA-034.8»
- [ ] R2RML / RML import to CML
- [ ] Tier 2 — Completeness
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/migration/r2rml_importer.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/migration/r2rml_importer.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

