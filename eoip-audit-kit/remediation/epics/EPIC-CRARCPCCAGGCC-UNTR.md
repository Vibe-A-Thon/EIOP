# EPIC-CRARCPCCAGGCC-UNTR: CRAr_cpccaggcc-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 30 tasks, ~195.0 h, priorities {'P0': 4, 'P1': 8, 'P2': 18}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-ONT-001 [P0] ONT-001: W3C serialization bridge (rdflib) · P0 · M

- **Source:** `CRAr_cpccaggcc-requirements.md:2620-2620` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ONT-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-001 | W3C serialization bridge (rdflib) | P0 | M | Tier 0 — Credibility | none | CRA-016 (+CRA-034) | CRA-016.9
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ONT-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ONT-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ONT-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-001 | W3C serialization bridge (rdflib) | P0 | M | Tier 0 — Credibility | none | CRA-016 (+CRA-034) | CRA-016.9»
- [ ] W3C serialization bridge (rdflib)
- [ ] Tier 0 — Credibility
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ONT-004 [P0] ONT-004: Conformant SHACL via pySHACL · P0 · S

- **Source:** `CRAr_cpccaggcc-requirements.md:2623-2623` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ONT-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-004 | Conformant SHACL via pySHACL | P0 | S | Tier 0 — Credibility | ONT-001 | CRA-020 | requirement-level
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ONT-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ONT-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ONT-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-004 | Conformant SHACL via pySHACL | P0 | S | Tier 0 — Credibility | ONT-001 | CRA-020 | requirement-level»
- [ ] Conformant SHACL via pySHACL
- [ ] Tier 0 — Credibility
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ONT-005 [P0] ONT-005: Connector Mapping Language (CML) · P0 · L

- **Source:** `CRAr_cpccaggcc-requirements.md:2624-2624` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ONT-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-005 | Connector Mapping Language (CML) | P0 | L | Tier 1 — Differentiators | ONT-001 | CRA-017 (+CRA-004/005) | requirement-level
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ONT-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ONT-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ONT-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-005 | Connector Mapping Language (CML) | P0 | L | Tier 1 — Differentiators | ONT-001 | CRA-017 (+CRA-004/005) | requirement-level»
- [ ] Connector Mapping Language (CML)
- [ ] Tier 1 — Differentiators
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ONT-007 [P0] ONT-007: Pluggable reasoner port (ELK default) · P0 · M

- **Source:** `CRAr_cpccaggcc-requirements.md:2626-2626` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ONT-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-007 | Pluggable reasoner port (ELK default) | P0 | M | Tier 0 — Credibility | ONT-001 | CRA-019 | requirement-level
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ONT-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ONT-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ONT-007

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-007 | Pluggable reasoner port (ELK default) | P0 | M | Tier 0 — Credibility | ONT-001 | CRA-019 | requirement-level»
- [ ] Pluggable reasoner port (ELK default)
- [ ] Tier 0 — Credibility
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-007 [P1] GN-007: Model registry, promotion, rollback · CRA-044.9

- **Source:** `CRAr_cpccaggcc-requirements.md:2790-2790` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 7 other site(s): see duplicate task DUP-GN-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-007 | Model registry, promotion, rollback | CRA-044.9 | —
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-007

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-007 | Model registry, promotion, rollback | CRA-044.9 | —»
- [ ] Model registry, promotion, rollback
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-014 [P1] GN-014: Air-gapped installation · CRA-043.3 · Wheel bundle + hash lock

- **Source:** `CRAr_cpccaggcc-requirements.md:2781-2781` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 9 other site(s): see duplicate task DUP-GN-014; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-014 | Air-gapped installation | CRA-043.3 | Wheel bundle + hash lock
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-014' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-014') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-014

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-014 | Air-gapped installation | CRA-043.3 | Wheel bundle + hash lock»
- [ ] Wheel bundle + hash lock
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ONT-002 [P1] ONT-002: SPARQL 1.1 endpoint over the LPG store · P1 · L

- **Source:** `CRAr_cpccaggcc-requirements.md:2621-2621` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ONT-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-002 | SPARQL 1.1 endpoint over the LPG store | P1 | L | Tier 1 — Differentiators | ONT-001 | CRA-024 | requirement-level
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ONT-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ONT-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ONT-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-002 | SPARQL 1.1 endpoint over the LPG store | P1 | L | Tier 1 — Differentiators | ONT-001 | CRA-024 | requirement-level»
- [ ] SPARQL 1.1 endpoint over the LPG store
- [ ] Tier 1 — Differentiators
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ONT-008 [P1] ONT-008: Hybrid materialize / virtualize reasoning · P1 · M

- **Source:** `CRAr_cpccaggcc-requirements.md:2627-2627` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ONT-008; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-008 | Hybrid materialize / virtualize reasoning | P1 | M | Tier 1 — Differentiators | ONT-007 | CRA-019 | CRA-019.10
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ONT-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ONT-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ONT-008

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-008 | Hybrid materialize / virtualize reasoning | P1 | M | Tier 1 — Differentiators | ONT-007 | CRA-019 | CRA-019.10»
- [ ] Hybrid materialize / virtualize reasoning
- [ ] Tier 1 — Differentiators
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ONT-010 [P1] ONT-010: Ship gist, FIBO and schema.org as domain packs · P1 · S

- **Source:** `CRAr_cpccaggcc-requirements.md:2629-2629` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ONT-010; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-010 | Ship gist, FIBO and schema.org as domain packs | P1 | S | Tier 2 — Completeness | ONT-001 | CRA-018 | CRA-018.8
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ONT-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ONT-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ONT-010

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-010 | Ship gist, FIBO and schema.org as domain packs | P1 | S | Tier 2 — Completeness | ONT-001 | CRA-018 | CRA-018.8»
- [ ] Ship gist, FIBO and schema.org as domain packs
- [ ] Tier 2 — Completeness
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ONT-016 [P1] ONT-016: SKOS RDF import / export · P1 · S

- **Source:** `CRAr_cpccaggcc-requirements.md:2635-2635` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ONT-016; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-016 | SKOS RDF import / export | P1 | S | Tier 2 — Completeness | ONT-001 | CRA-021 | CRA-021.6
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ONT-016' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ONT-016') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ONT-016

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-016 | SKOS RDF import / export | P1 | S | Tier 2 — Completeness | ONT-001 | CRA-021 | CRA-021.6»
- [ ] SKOS RDF import / export
- [ ] Tier 2 — Completeness
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ONT-018 [P1] ONT-018: PROV-O provenance on every mined triple · P1 · M

- **Source:** `CRAr_cpccaggcc-requirements.md:2637-2637` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ONT-018; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-018 | PROV-O provenance on every mined triple | P1 | M | Tier 2 — Completeness | ONT-005 | CRA-017 | CRA-017.9
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ONT-018' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ONT-018') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ONT-018

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-018 | PROV-O provenance on every mined triple | P1 | M | Tier 2 — Completeness | ONT-005 | CRA-017 | CRA-017.9»
- [ ] PROV-O provenance on every mined triple
- [ ] Tier 2 — Completeness
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-ONT-019 [P1] ONT-019: OWL round-trip certification CI gate · P1 · S

- **Source:** `CRAr_cpccaggcc-requirements.md:2638-2638` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-ONT-019; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-019 | OWL round-trip certification CI gate | P1 | S | Tier 2 — Completeness | ONT-001 | CRA-016 (+CRA-037/041) | CRA-016.9, CRA-016.10, CRA-041.2
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'ONT-019' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('ONT-019') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-ONT-019

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-019 | OWL round-trip certification CI gate | P1 | S | Tier 2 — Completeness | ONT-001 | CRA-016 (+CRA-037/041) | CRA-016.9, CRA-016.10, CRA-041.2»
- [ ] OWL round-trip certification CI gate
- [ ] Tier 2 — Completeness
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-001 [P2] GN-001: Neural runtime and degradation contract · CRA-043.4 · X-39

- **Source:** `CRAr_cpccaggcc-requirements.md:2784-2784` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 11 other site(s): see duplicate task DUP-GN-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-001 | Neural runtime and degradation contract | CRA-043.4 | X-39
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-001 | Neural runtime and degradation contract | CRA-043.4 | X-39»
- [ ] Neural runtime and degradation contract
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-003 [P2] GN-003: Anti-stub harness · CRA-044.3, CRA-037.11 · Must fail the hash stub

- **Source:** `CRAr_cpccaggcc-requirements.md:2786-2786` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 7 other site(s): see duplicate task DUP-GN-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-003 | Anti-stub harness | CRA-044.3, CRA-037.11 | Must fail the hash stub
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-003 | Anti-stub harness | CRA-044.3, CRA-037.11 | Must fail the hash stub»
- [ ] Must fail the hash stub
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-004 [P2] GN-004: Versioned feature and embedding store · CRA-044.9, CRA-025.8 · X-41

- **Source:** `CRAr_cpccaggcc-requirements.md:2787-2787` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 9 other site(s): see duplicate task DUP-GN-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-004 | Versioned feature and embedding store | CRA-044.9, CRA-025.8 | X-41
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-004 | Versioned feature and embedding store | CRA-044.9, CRA-025.8 | X-41»
- [ ] Versioned feature and embedding store
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-005 [P2] GN-005: Snapshots, temporal splits, negative sampling · CRA-044.4

- **Source:** `CRAr_cpccaggcc-requirements.md:2788-2788` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 8 other site(s): see duplicate task DUP-GN-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-005 | Snapshots, temporal splits, negative sampling | CRA-044.4 | —
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-005 | Snapshots, temporal splits, negative sampling | CRA-044.4 | —»
- [ ] Snapshots, temporal splits, negative sampling
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-006 [P2] GN-006: Evaluation harness and calibration · CRA-044.5, CRA-036.10 · X-37

- **Source:** `CRAr_cpccaggcc-requirements.md:2789-2789` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 8 other site(s): see duplicate task DUP-GN-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-006 | Evaluation harness and calibration | CRA-044.5, CRA-036.10 | X-37
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-006 | Evaluation harness and calibration | CRA-044.5, CRA-036.10 | X-37»
- [ ] Evaluation harness and calibration
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-010 [P2] GN-010: Numerical stack provisioning and platform matrix · CRA-043.1, 043.2, 043.3, 043.10, 043.11 · Tiers N0-N3, CPU-only distribution (H-16)

- **Source:** `CRAr_cpccaggcc-requirements.md:2777-2777` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 10 other site(s): see duplicate task DUP-GN-010; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-010 | Numerical stack provisioning and platform matrix | CRA-043.1, 043.2, 043.3, 043.10, 043.11 | Tiers N0-N3, CPU-only distribution (H-16)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-010

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-010 | Numerical stack provisioning and platform matrix | CRA-043.1, 043.2, 043.3, 043.10, 043.11 | Tiers N0-N3, CPU-only distribution (H-16)»
- [ ] Numerical stack provisioning and platform matrix
- [ ] CRA-043.1, 043.2, 043.3, 043.10, 043.11
- [ ] Tiers N0-N3, CPU-only distribution (H-16)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-011 [P2] GN-011: Array backend and dtype discipline · CRA-043.5 · float32 storage, no Python loops

- **Source:** `CRAr_cpccaggcc-requirements.md:2778-2778` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 9 other site(s): see duplicate task DUP-GN-011; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-011 | Array backend and dtype discipline | CRA-043.5 | float32 storage, no Python loops
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-011

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-011 | Array backend and dtype discipline | CRA-043.5 | float32 storage, no Python loops»
- [ ] Array backend and dtype discipline
- [ ] float32 storage, no Python loops
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-013 [P2] GN-013: BLAS thread governance · CRA-043.7 · Set before numpy import

- **Source:** `CRAr_cpccaggcc-requirements.md:2780-2780` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 9 other site(s): see duplicate task DUP-GN-013; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-013 | BLAS thread governance | CRA-043.7 | Set before numpy import
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-013

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-013 | BLAS thread governance | CRA-043.7 | Set before numpy import»
- [ ] Set before numpy import
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-015 [P2] GN-015: Numerical correctness and stability · CRA-043.8

- **Source:** `CRAr_cpccaggcc-requirements.md:2782-2782` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 9 other site(s): see duplicate task DUP-GN-015; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-015 | Numerical correctness and stability | CRA-043.8 | —
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-015' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-015') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-015

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-015 | Numerical correctness and stability | CRA-043.8 | —»
- [ ] Numerical correctness and stability
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-016 [P2] GN-016: Memory and tensor lifecycle · CRA-043.9 · Refuse before allocation

- **Source:** `CRAr_cpccaggcc-requirements.md:2783-2783` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 8 other site(s): see duplicate task DUP-GN-016; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-016 | Memory and tensor lifecycle | CRA-043.9 | Refuse before allocation
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-016' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-016') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-016

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-016 | Memory and tensor lifecycle | CRA-043.9 | Refuse before allocation»
- [ ] Memory and tensor lifecycle
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-203 [P2] GN-203: Natural-language bridge · CRA-026, CRA-045.3 · Grounded, cited, dual path

- **Source:** `CRAr_cpccaggcc-requirements.md:2793-2793` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 8 other site(s): see duplicate task DUP-GN-203; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-203 | Natural-language bridge | CRA-026, CRA-045.3 | Grounded, cited, dual path
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-203' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-203') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-203

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-203 | Natural-language bridge | CRA-026, CRA-045.3 | Grounded, cited, dual path»
- [ ] Grounded, cited, dual path
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-501 [P2] GN-501: Adversarial quality discriminator · CRA-044.8 · After CRA-044.6

- **Source:** `CRAr_cpccaggcc-requirements.md:2796-2796` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 8 other site(s): see duplicate task DUP-GN-501; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-501 | Adversarial quality discriminator | CRA-044.8 | After CRA-044.6
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-501' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-501') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-501

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-501 | Adversarial quality discriminator | CRA-044.8 | After CRA-044.6»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-701 [P2] GN-701: Explainability · CRA-044.10 · Faithfulness probe

- **Source:** `CRAr_cpccaggcc-requirements.md:2798-2798` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 7 other site(s): see duplicate task DUP-GN-701; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-701 | Explainability | CRA-044.10 | Faithfulness probe
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-701' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-701') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-701

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-701 | Explainability | CRA-044.10 | Faithfulness probe»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-702 [P2] GN-702: Fusion and arbitration · CRA-045.3 · DISPUTED surfaced

- **Source:** `CRAr_cpccaggcc-requirements.md:2799-2799` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 7 other site(s): see duplicate task DUP-GN-702; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-702 | Fusion and arbitration | CRA-045.3 | DISPUTED surfaced
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-702' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-702') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-702

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-702 | Fusion and arbitration | CRA-045.3 | DISPUTED surfaced»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-703 [P2] GN-703: Security and entitlements · CRA-003, CRA-044.A · Membership-inference probe

- **Source:** `CRAr_cpccaggcc-requirements.md:2800-2800` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 8 other site(s): see duplicate task DUP-GN-703; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-703 | Security and entitlements | CRA-003, CRA-044.A | Membership-inference probe
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-703' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-703') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-703

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-703 | Security and entitlements | CRA-003, CRA-044.A | Membership-inference probe»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-704 [P2] GN-704: API surface · Section 11 · X-38

- **Source:** `CRAr_cpccaggcc-requirements.md:2801-2801` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 8 other site(s): see duplicate task DUP-GN-704; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-704 | API surface | Section 11 | X-38
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-704' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-704') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-704

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-704 | API surface | Section 11 | X-38»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-705 [P2] GN-705: Performance budgets · CRA-036 · Manifest targets

- **Source:** `CRAr_cpccaggcc-requirements.md:2802-2802` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 4 other site(s): see duplicate task DUP-GN-705; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-705 | Performance budgets | CRA-036 | Manifest targets
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-705' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-705') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-705

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-705 | Performance budgets | CRA-036 | Manifest targets»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-706 [P2] GN-706: Known failure-mode guards · CRA-044.11

- **Source:** `CRAr_cpccaggcc-requirements.md:2803-2803` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 4 other site(s): see duplicate task DUP-GN-706; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GN-706 | Known failure-mode guards | CRA-044.11 | —
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-706' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-706') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-706

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GN-706 | Known failure-mode guards | CRA-044.11 | —»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

