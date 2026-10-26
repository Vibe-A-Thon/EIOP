# EPIC-IP-UNTR-02: EOIP-engg-doc-pkg/ip-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 60 tasks, ~390.0 h, priorities {'P1': 12, 'P2': 48}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-REQ-SHB-002 [P1] REQ-SHB-002: Simulated tools: every registered tool of class ≥ INTERNALWRITE MUST declare a simulate implementation that, given the call, returns the assertions it would change (no external side effects). Tools wi

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:781-781` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-SHB-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-SHB-002 | Simulated tools: every registered tool of class ≥ `INTERNAL_WRITE` MUST declare a `simulate` implementation that, given the call, returns the assertions it would change (no external side effects). Tools without `simulate` cannot be rehearsed and are listed as such.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-SHB-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-SHB-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-SHB-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-SHB-002 | Simulated tools: every registered tool of class ≥ INTERNAL_WRITE MUST declare a simulate implementation that, given the call, returns the assertions it would change (no external side effects). Tools without simulate cannot be rehearsed and are listed as such.»
- [ ] Simulated tools: every registered tool of class ≥ INTERNAL_WRITE MUST declare a simulate implementation that, given the call, returns the assertions it would change (no external side effects). Tools without simulate cannot be rehearsed and are listed as such.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-SHB-004 [P1] REQ-SHB-004: POST /branches/{id}/merge requires an approval when κ > the agent's budget or any SHACL violation exists; merge replays the plan against the authoritative graph through the normal commit checkpoint (l

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:783-783` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-SHB-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-SHB-004 | `POST /branches/{id}/merge` requires an approval when κ > the agent's budget or any SHACL violation exists; merge replays the plan against the authoritative graph through the normal commit checkpoint (leases re-validated). `POST /branches/{id}/discard`. Branches expire after `ttl` (default 24 h).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-SHB-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-SHB-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-SHB-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-SHB-004 | POST /branches/{id}/merge requires an approval when κ > the agent's budget or any SHACL violation exists; merge replays the plan against the authoritative graph through the normal commit checkpoint (leases re-validated). POST /branches/{id}/discard. Branches expire after ttl (default 24 h).»
- [ ] POST /branches/{id}/merge requires an approval when κ > the agent's budget or any SHACL violation exists; merge replays the plan against the authoritative graph through the normal commit checkpoint (leases re-validated). POST /branches/{id}/discard. Branches expire after ttl (default 24 h).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-SHB-005 [P1] REQ-SHB-005: Branch isolation test: no read of the authoritative graph by any other principal can observe branch deltas

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:784-784` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-SHB-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-SHB-005 | Branch isolation test: no read of the authoritative graph by any other principal can observe branch deltas.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-SHB-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-SHB-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-SHB-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-SHB-005 | Branch isolation test: no read of the authoritative graph by any other principal can observe branch deltas.»
- [ ] Branch isolation test: no read of the authoritative graph by any other principal can observe branch deltas.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-VER-002 [P1] REQ-VER-002: Resolution by observer call creates a new OBSERVED warrant with new grounds; resolution by a person with authority creates an ATTESTED warrant. Refutation marks the original assertion validto = now an

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:499-499` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-VER-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-VER-002 | Resolution by observer call creates a new `OBSERVED` warrant with new grounds; resolution by a person with authority creates an `ATTESTED` warrant. Refutation marks the original assertion `valid_to = now` and creates a `refuted_by` link.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-VER-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-VER-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-VER-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-VER-002 | Resolution by observer call creates a new OBSERVED warrant with new grounds; resolution by a person with authority creates an ATTESTED warrant. Refutation marks the original assertion valid_to = now and creates a refuted_by link.»
- [ ] Resolution by observer call creates a new OBSERVED warrant with new grounds; resolution by a person with authority creates an ATTESTED warrant. Refutation marks the original assertion valid_to = now and creates a refuted_by link.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-WAR-010 [P1] REQ-WAR-010: warrant-service MUST validate every warrant against the schema on write and reject invalid ones with WARSCHEMAINVALID and the JSON-pointer of the first failure

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:343-343` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-WAR-010; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-WAR-010 | `warrant-service` MUST validate every warrant against the schema on write and reject invalid ones with `WAR_SCHEMA_INVALID` and the JSON-pointer of the first failure.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-WAR-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-WAR-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-WAR-010

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-WAR-010 | warrant-service MUST validate every warrant against the schema on write and reject invalid ones with WAR_SCHEMA_INVALID and the JSON-pointer of the first failure.»
- [ ] warrant-service MUST validate every warrant against the schema on write and reject invalid ones with WAR_SCHEMA_INVALID and the JSON-pointer of the first failure.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-WAR-012 [P1] REQ-WAR-012: Canonical JSON for hashing and signing MUST follow RFC 8785 (JSON Canonicalization Scheme)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:345-345` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-WAR-012; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-WAR-012 | Canonical JSON for hashing and signing MUST follow RFC 8785 (JSON Canonicalization Scheme).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-WAR-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-WAR-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-WAR-012

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-WAR-012 | Canonical JSON for hashing and signing MUST follow RFC 8785 (JSON Canonicalization Scheme).»
- [ ] Canonical JSON for hashing and signing MUST follow RFC 8785 (JSON Canonicalization Scheme).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-WAR-013 [P1] REQ-WAR-013: Warrants for stored assertions MUST be persisted in the graph through the graph abstraction layer as a Warrant node linked (:Warrant)-[:JUSTIFIES]->(assertion) and (:Warrant)-[:DERIVEDFROM]->(:Warrant

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:346-346` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-WAR-013; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-WAR-013 | Warrants for stored assertions MUST be persisted in the graph through the graph abstraction layer as a `Warrant` node linked `(:Warrant)-[:JUSTIFIES]->(assertion)` and `(:Warrant)-[:DERIVED_FROM]->(:Warrant)` for parents. Runtime-only warrants (propositions not stored as assertions) MUST be persisted in a warrant store with tenant-configurable retention `warrant.runtime_retention_days` (default 30).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-WAR-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-WAR-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-WAR-013

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-WAR-013 | Warrants for stored assertions MUST be persisted in the graph through the graph abstraction layer as a Warrant node linked (:Warrant)-[:JUSTIFIES]->(assertion) and (:Warrant)-[:DERIVED_FROM]->(:Warrant) for parents. Runtime-only warrants (propositions not stored as assertions) MUST be persisted in a warrant store with tenant-configurable retention warrant.runtime_»
- [ ] Warrants for stored assertions MUST be persisted in the graph through the graph abstraction layer as a Warrant node linked (:Warrant)-[:JUSTIFIES]->(assertion) and (:Warrant)-[:DERIVED_FROM]->(:Warrant) for parents. Runtime-only warrants (propositions not stored as assertions) MUST be persisted in a warrant store with tenant-configurable retention warrant.runtime_retention_days (default 30).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-WAR-014 [P1] REQ-WAR-014: GET /warrants/{id}/lineage?depth=N MUST return the parent DAG to depth N (default 5, max 20) in under 300 ms p95 for depth 5 on a lineage of up to 1,000 warrants

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:347-347` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-WAR-014; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-WAR-014 | `GET /warrants/{id}/lineage?depth=N` MUST return the parent DAG to depth N (default 5, max 20) in under 300 ms p95 for depth 5 on a lineage of up to 1,000 warrants.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-WAR-014' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-WAR-014') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-WAR-014

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-WAR-014 | GET /warrants/{id}/lineage?depth=N MUST return the parent DAG to depth N (default 5, max 20) in under 300 ms p95 for depth 5 on a lineage of up to 1,000 warrants.»
- [ ] GET /warrants/{id}/lineage?depth=N MUST return the parent DAG to depth N (default 5, max 20) in under 300 ms p95 for depth 5 on a lineage of up to 1,000 warrants.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-WAR-020 [P1] REQ-WAR-020: The ingestion write path MUST create a warrant (operator class OBSERVER when kgf:observerSource=true for the source, else HEARSAY) for every new or changed assertion, in the same transaction or outbox

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:376-376` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-WAR-020; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-WAR-020 | The ingestion write path MUST create a warrant (operator class `OBSERVER` when `kgf:observerSource=true` for the source, else `HEARSAY`) for every new or changed assertion, in the same transaction or outbox batch as the assertion.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-WAR-020' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-WAR-020') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-WAR-020

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-WAR-020 | The ingestion write path MUST create a warrant (operator class OBSERVER when kgf:observerSource=true for the source, else HEARSAY) for every new or changed assertion, in the same transaction or outbox batch as the assertion.»
- [ ] The ingestion write path MUST create a warrant (operator class OBSERVER when kgf:observerSource=true for the source, else HEARSAY) for every new or changed assertion, in the same transaction or outbox batch as the assertion.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-WAR-021 [P1] REQ-WAR-021: A one-time migration MUST create warrants for all existing assertions: existing OBSERVED → OBSERVED with grounds sourcerecord; existing PREDICTED/inferred → PREDICTED with grounds modelrun (model id l

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:377-377` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-WAR-021; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-WAR-021 | A one-time migration MUST create warrants for all existing assertions: existing `OBSERVED` → `OBSERVED` with grounds `source_record`; existing `PREDICTED`/inferred → `PREDICTED` with grounds `model_run` (model id `legacy` if unknown); anything else → `UNKNOWN`. The migration is idempotent and resumable, logs counts per status, and has a dry-run mode.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-WAR-021' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-WAR-021') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-WAR-021

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-WAR-021 | A one-time migration MUST create warrants for all existing assertions: existing OBSERVED → OBSERVED with grounds source_record; existing PREDICTED/inferred → PREDICTED with grounds model_run (model id legacy if unknown); anything else → UNKNOWN. The migration is idempotent and resumable, logs counts per status, and has a dry-run mode.»
- [ ] A one-time migration MUST create warrants for all existing assertions: existing OBSERVED → OBSERVED with grounds source_record; existing PREDICTED/inferred → PREDICTED with grounds model_run (model id legacy if unknown); anything else → UNKNOWN. The migration is idempotent and resumable, logs counts per status, and has a dry-run mode.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-WAR-022 [P1] REQ-WAR-022: An assertion with status PREDICTED, GENERATED, HEARSAY or UNKNOWN MUST NOT overwrite or delete an assertion with status OBSERVED or ATTESTED for the same subject. It is stored alongside, and queries r

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:378-378` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-WAR-022; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-WAR-022 | An assertion with status `PREDICTED`, `GENERATED`, `HEARSAY` or `UNKNOWN` MUST NOT overwrite or delete an assertion with status `OBSERVED` or `ATTESTED` for the same subject. It is stored alongside, and queries return both with their statuses unless the caller filters. Attempted overwrite returns `WAR_STATUS_DOWNGRADE_WRITE`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-WAR-022' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-WAR-022') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-WAR-022

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-WAR-022 | An assertion with status PREDICTED, GENERATED, HEARSAY or UNKNOWN MUST NOT overwrite or delete an assertion with status OBSERVED or ATTESTED for the same subject. It is stored alongside, and queries return both with their statuses unless the caller filters. Attempted overwrite returns WAR_STATUS_DOWNGRADE_WRITE.»
- [ ] An assertion with status PREDICTED, GENERATED, HEARSAY or UNKNOWN MUST NOT overwrite or delete an assertion with status OBSERVED or ATTESTED for the same subject. It is stored alongside, and queries return both with their statuses unless the caller filters. Attempted overwrite returns WAR_STATUS_DOWNGRADE_WRITE.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-WAR-023 [P1] REQ-WAR-023: Bitemporal reconstruction: GET /graph/as-of?validat=…&recordedat=… MUST return the assertion set as it was valid and recorded at those times, with their warrants

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:379-379` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-WAR-023; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-WAR-023 | Bitemporal reconstruction: `GET /graph/as-of?valid_at=…&recorded_at=…` MUST return the assertion set as it was valid and recorded at those times, with their warrants.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-WAR-023' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-WAR-023') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-WAR-023

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-WAR-023 | Bitemporal reconstruction: GET /graph/as-of?valid_at=…&recorded_at=… MUST return the assertion set as it was valid and recorded at those times, with their warrants.»
- [ ] Bitemporal reconstruction: GET /graph/as-of?valid_at=…&recorded_at=… MUST return the assertion set as it was valid and recorded at those times, with their warrants.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-BRB-003 [P2] REQ-BRB-003: Escalations: GET /escalations, POST /escalations/{id}/decide with `{decision: APPROVE · REJECT · APPROVE_WITH_SCOPE, scope?, note}. Approval creates an ATTESTED warrant for the action by the approver,

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:660-660` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-BRB-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-BRB-003 | Escalations: `GET /escalations`, `POST /escalations/{id}/decide` with `{decision: APPROVE | REJECT | APPROVE_WITH_SCOPE, scope?, note}`. Approval creates an `ATTESTED` warrant for the action by the approver, then the action proceeds without debiting the agent budget beyond its current balance (approved κ is logged as `kappa_approved`).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-BRB-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-BRB-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-BRB-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-BRB-003 | Escalations: GET /escalations, POST /escalations/{id}/decide with `{decision: APPROVE | REJECT | APPROVE_WITH_SCOPE, scope?, note}. Approval creates an ATTESTED warrant for the action by the approver, then the action proceeds without debiting the agent budget beyond its current balance (approved κ is logged as kappa_approved`).»
- [ ] Escalations: GET /escalations, POST /escalations/{id}/decide with `{decision: APPROVE
- [ ] APPROVE_WITH_SCOPE, scope?, note}. Approval creates an ATTESTED warrant for the action by the approver, then the action proceeds without debiting the agent budget beyond its current balance (approved κ is logged as kappa_approved`).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-BRB-005 [P2] REQ-BRB-005: Metric kgfipbudgetoverruntotal{tenant,agentclass} counts escalations caused by κ > B

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:662-662` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-BRB-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-BRB-005 | Metric `kgf_ip_budget_overrun_total{tenant,agent_class}` counts escalations caused by κ > B.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-BRB-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-BRB-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-BRB-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-BRB-005 | Metric kgf_ip_budget_overrun_total{tenant,agent_class} counts escalations caused by κ > B.»
- [ ] Metric kgf_ip_budget_overrun_total{tenant,agent_class} counts escalations caused by κ > B.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-BRB-006 [P2] REQ-BRB-006: Demonstration scenario: a STANDARDAGENT requests an action on a criticality-5 service with κ > 10 → escalated; approver sees the impact subgraph and approves; action executes; budget unchanged; a seco

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:663-663` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-BRB-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-BRB-006 | Demonstration scenario: a STANDARD_AGENT requests an action on a criticality-5 service with κ > 10 → escalated; approver sees the impact subgraph and approves; action executes; budget unchanged; a second, low-κ action is allowed and debited.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-BRB-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-BRB-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-BRB-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-BRB-006 | Demonstration scenario: a STANDARD_AGENT requests an action on a criticality-5 service with κ > 10 → escalated; approver sees the impact subgraph and approves; action executes; budget unchanged; a second, low-κ action is allowed and debited.»
- [ ] Demonstration scenario: a STANDARD_AGENT requests an action on a criticality-5 service with κ > 10 → escalated; approver sees the impact subgraph and approves; action executes; budget unchanged; a second, low-κ action is allowed and debited.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CHK-003 [P2] REQ-CHK-003: POST /checkpoints/{checkpoint}/evaluate (request: checkpoint, subject, warrant_ids[], action_class, plan_id?, principal_id) returns `{decision: ALLOW · BLOCK · ESCALATE

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:480-480` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CHK-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CHK-003 | `POST /checkpoints/{checkpoint}/evaluate` (request: `checkpoint`, `subject`, `warrant_ids[]`, `action_class`, `plan_id?`, `principal_id`) returns `{decision: ALLOW | BLOCK | ESCALATE | ALLOW_WITH_DOWNGRADE, reasons[], warrant_out, required_tasks[]}`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CHK-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CHK-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CHK-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CHK-003 | POST /checkpoints/{checkpoint}/evaluate (request: checkpoint, subject, warrant_ids[], action_class, plan_id?, principal_id) returns `{decision: ALLOW | BLOCK | ESCALATE | ALLOW_WITH_DOWNGRADE, reasons[], warrant_out, required_tasks[]}`.»
- [ ] POST /checkpoints/{checkpoint}/evaluate (request: checkpoint, subject, warrant_ids[], action_class, plan_id?, principal_id) returns `{decision: ALLOW
- [ ] ALLOW_WITH_DOWNGRADE, reasons[], warrant_out, required_tasks[]}`.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CHK-004 [P2] REQ-CHK-004: Every checkpoint evaluation writes a checkpointevaluated event (§19.2) with decision and reasons, and increments metrics in §16

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:481-481` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CHK-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CHK-004 | Every checkpoint evaluation writes a `checkpoint_evaluated` event (§19.2) with decision and reasons, and increments metrics in §16.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CHK-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CHK-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CHK-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CHK-004 | Every checkpoint evaluation writes a checkpoint_evaluated event (§19.2) with decision and reasons, and increments metrics in §16.»
- [ ] Every checkpoint evaluation writes a checkpoint_evaluated event (§19.2) with decision and reasons, and increments metrics in §16.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CHK-005 [P2] REQ-CHK-005: p95 latency of evaluate excluding SASI, lease validation and κ: < 20 ms

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:482-482` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CHK-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CHK-005 | p95 latency of `evaluate` excluding SASI, lease validation and κ: < 20 ms.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CHK-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CHK-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CHK-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CHK-005 | p95 latency of evaluate excluding SASI, lease validation and κ: < 20 ms.»
- [ ] p95 latency of evaluate excluding SASI, lease validation and κ: < 20 ms.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CMT-001 [P2] REQ-CMT-001: Explicit capture: SDK method committo(promisees, statement, kind, dueat, about[], condition?) and POST /commitments create a commitment in state ACTIVE with a warrant composed by A1 from the calling c

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1334-1334` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CMT-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CMT-001 | Explicit capture: SDK method `commit_to(promisees, statement, kind, due_at, about[], condition?)` and `POST /commitments` create a commitment in state `ACTIVE` with a warrant composed by A1 from the calling context (status of the commitment warrant = `ATTESTED` when made by a person, `GENERATED` when made by an agent; this records that the promise exists, not that it will be kept).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CMT-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CMT-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CMT-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CMT-001 | Explicit capture: SDK method commit_to(promisees, statement, kind, due_at, about[], condition?) and POST /commitments create a commitment in state ACTIVE with a warrant composed by A1 from the calling context (status of the commitment warrant = ATTESTED when made by a person, GENERATED when made by an agent; this records that the promise exists, not that it will b»
- [ ] Explicit capture: SDK method commit_to(promisees, statement, kind, due_at, about[], condition?) and POST /commitments create a commitment in state ACTIVE with a warrant composed by A1 from the calling context (status of the commitment warrant = ATTESTED when made by a person, GENERATED when made by an agent; this records that the promise exists, not that it will be kept).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CMT-002 [P2] REQ-CMT-002: Implicit detection: at the answer and handoff checkpoints, agent outputs pass through the extractor (POST /commitments/extract; prompt template commitment.extract.v1, a registered GENERATOR operator, 

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1335-1335` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CMT-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CMT-002 | Implicit detection: at the `answer` and `handoff` checkpoints, agent outputs pass through the extractor (`POST /commitments/extract`; prompt template `commitment.extract.v1`, a registered GENERATOR operator, local model `commitment.extract_model`). Each detected promissory statement creates a `PROPOSED` commitment with its source span. The promisor agent's runtime must call `confirm` or `retract` within `commitment.confirm_window`; unconfirmed proposals become `ACTIVE` and a notice goes to the agent's owner.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CMT-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CMT-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CMT-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CMT-002 | Implicit detection: at the answer and handoff checkpoints, agent outputs pass through the extractor (POST /commitments/extract; prompt template commitment.extract.v1, a registered GENERATOR operator, local model commitment.extract_model). Each detected promissory statement creates a PROPOSED commitment with its source span. The promisor agent's runtime must call c»
- [ ] Implicit detection: at the answer and handoff checkpoints, agent outputs pass through the extractor (POST /commitments/extract; prompt template commitment.extract.v1, a registered GENERATOR operator, local model commitment.extract_model). Each detected promissory statement creates a PROPOSED commitment with its source span. The promisor agent's runtime must call confirm or retract within commitmen
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CMT-003 [P2] REQ-CMT-003: Extraction benchmark evals/commitment/extract-v1 with ≥ 200 labelled agent outputs (promises with and without dates, conditional promises, non-promises such as "you could…", reported speech). Acceptan

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1336-1336` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CMT-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CMT-003 | Extraction benchmark `evals/commitment/extract-v1` with ≥ 200 labelled agent outputs (promises with and without dates, conditional promises, non-promises such as "you could…", reported speech). Acceptance: precision ≥ 0.90 and recall ≥ 0.85 for detecting promises; due-date extraction exact-match ≥ 0.85 on promises that state a date.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CMT-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CMT-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CMT-003

**Acceptance criteria**
- [ ] precision ≥ 0.90 and recall ≥ 0.85 for detecting promises; due-date extraction exact-match ≥ 0.85 on promises that state a date
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CMT-005 [P2] REQ-CMT-005: Feasibility at creation: if dueat − now < commitment.minleadtime, or the promisor already holds ≥ commitment.maxopen open commitments, the commitment is created in state ATRISK and the promisor and it

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1338-1338` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CMT-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CMT-005 | Feasibility at creation: if `due_at − now < commitment.min_lead_time`, or the promisor already holds ≥ `commitment.max_open` open commitments, the commitment is created in state `AT_RISK` and the promisor and its owner are notified.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CMT-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CMT-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CMT-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CMT-005 | Feasibility at creation: if due_at − now < commitment.min_lead_time, or the promisor already holds ≥ commitment.max_open open commitments, the commitment is created in state AT_RISK and the promisor and its owner are notified.»
- [ ] Feasibility at creation: if due_at − now < commitment.min_lead_time, or the promisor already holds ≥ commitment.max_open open commitments, the commitment is created in state AT_RISK and the promisor and its owner are notified.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CMT-006 [P2] REQ-CMT-006: Lifecycle scheduler (runs every minute): ACTIVE → ATRISK when remaining time < commitment.atriskfraction × (dueat − createdat) and no progress entry exists in the last quarter of the window; ACTIVE

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1339-1339` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CMT-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CMT-006 | Lifecycle scheduler (runs every minute): `ACTIVE → AT_RISK` when remaining time < `commitment.at_risk_fraction` × (due_at − created_at) and no progress entry exists in the last quarter of the window; `ACTIVE | AT_RISK → BROKEN` when `due_at` passes without fulfilment; `CONDITIONAL` commitments become due only when their condition first matches the graph (evaluated on `kgf.graph.changed`). Every transition writes `kgf.ip.commitment.changed` and notifies promisees.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CMT-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CMT-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CMT-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CMT-006 | Lifecycle scheduler (runs every minute): ACTIVE → AT_RISK when remaining time < commitment.at_risk_fraction × (due_at − created_at) and no progress entry exists in the last quarter of the window; `ACTIVE | AT_RISK → BROKEN when due_at passes without fulfilment; CONDITIONAL commitments become due only when their condition first matches the graph (evaluated on kgf.g»
- [ ] Lifecycle scheduler (runs every minute): ACTIVE → AT_RISK when remaining time < commitment.at_risk_fraction × (due_at − created_at) and no progress entry exists in the last quarter of the window; `ACTIVE
- [ ] AT_RISK → BROKEN when due_at passes without fulfilment; CONDITIONAL commitments become due only when their condition first matches the graph (evaluated on kgf.graph.changed). Every transition writes kgf.ip.commitment.changed` and notifies promisees.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CMT-007 [P2] REQ-CMT-007: Evidence-based fulfilment: POST /commitments/{id}/fulfil {warrantid} succeeds only if the referenced warrant has status ≥ commitment.fulfilminstatus and its grounds reference at least one entity in ab

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1340-1340` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CMT-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CMT-007 | Evidence-based fulfilment: `POST /commitments/{id}/fulfil {warrant_id}` succeeds only if the referenced warrant has status ≥ `commitment.fulfil_min_status` and its grounds reference at least one entity in `about` (or, for `FOLLOW_UP`, a delivered message to every promisee recorded as an `OBSERVED` tool receipt). Otherwise `CMT_FULFILMENT_UNWARRANTED`. An agent saying "done" (a GENERATED proposition) never fulfils a commitment.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CMT-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CMT-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CMT-007

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CMT-007 | Evidence-based fulfilment: POST /commitments/{id}/fulfil {warrant_id} succeeds only if the referenced warrant has status ≥ commitment.fulfil_min_status and its grounds reference at least one entity in about (or, for FOLLOW_UP, a delivered message to every promisee recorded as an OBSERVED tool receipt). Otherwise CMT_FULFILMENT_UNWARRANTED. An agent saying "done" (»
- [ ] Evidence-based fulfilment: POST /commitments/{id}/fulfil {warrant_id} succeeds only if the referenced warrant has status ≥ commitment.fulfil_min_status and its grounds reference at least one entity in about (or, for FOLLOW_UP, a delivered message to every promisee recorded as an OBSERVED tool receipt). Otherwise CMT_FULFILMENT_UNWARRANTED. An agent saying "done" (a GENERATED proposition) never ful
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CMT-008 [P2] REQ-CMT-008: Commit-time conflict check: at the commit checkpoint, if an action modifies or deletes an entity that an ACTIVE, ATRISK or due CONDITIONAL commitment is ABOUT, and the action's plan does not reference

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1341-1341` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CMT-008; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CMT-008 | Commit-time conflict check: at the `commit` checkpoint, if an action modifies or deletes an entity that an `ACTIVE`, `AT_RISK` or due `CONDITIONAL` commitment is `ABOUT`, and the action's plan does not reference that commitment id, the checkpoint returns `ESCALATE` with `CMT_CONFLICT`, listing the commitments and their promisees.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CMT-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CMT-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CMT-008

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CMT-008 | Commit-time conflict check: at the commit checkpoint, if an action modifies or deletes an entity that an ACTIVE, AT_RISK or due CONDITIONAL commitment is ABOUT, and the action's plan does not reference that commitment id, the checkpoint returns ESCALATE with CMT_CONFLICT, listing the commitments and their promisees.»
- [ ] Commit-time conflict check: at the commit checkpoint, if an action modifies or deletes an entity that an ACTIVE, AT_RISK or due CONDITIONAL commitment is ABOUT, and the action's plan does not reference that commitment id, the checkpoint returns ESCALATE with CMT_CONFLICT, listing the commitments and their promisees.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CMT-009 [P2] REQ-CMT-009: Retrieval: when an agent works in a warrantcontext whose task touches entities with open commitments by that agent, the retrieval checkpoint adds those commitments (statement, due date, state, warrant

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1342-1342` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CMT-009; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CMT-009 | Retrieval: when an agent works in a `warrant_context` whose task touches entities with open commitments by that agent, the `retrieval` checkpoint adds those commitments (statement, due date, state, warrant) to the context so the agent does not contradict them.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CMT-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CMT-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CMT-009

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CMT-009 | Retrieval: when an agent works in a warrant_context whose task touches entities with open commitments by that agent, the retrieval checkpoint adds those commitments (statement, due date, state, warrant) to the context so the agent does not contradict them.»
- [ ] Retrieval: when an agent works in a warrant_context whose task touches entities with open commitments by that agent, the retrieval checkpoint adds those commitments (statement, due date, state, warrant) to the context so the agent does not contradict them.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CMT-011 [P2] REQ-CMT-011: RELEASED requires every promisee (or a principal with ip.commitment.manage on their behalf) to release the promisor, recorded with an ATTESTED warrant

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1344-1344` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CMT-011; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CMT-011 | `RELEASED` requires every promisee (or a principal with `ip.commitment.manage` on their behalf) to release the promisor, recorded with an `ATTESTED` warrant.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CMT-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CMT-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CMT-011

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CMT-011 | RELEASED requires every promisee (or a principal with ip.commitment.manage on their behalf) to release the promisor, recorded with an ATTESTED warrant.»
- [ ] RELEASED requires every promisee (or a principal with ip.commitment.manage on their behalf) to release the promisor, recorded with an ATTESTED warrant.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CMT-012 [P2] REQ-CMT-012: APIs per §19.7, cursor-paginated, filterable by state, promisor, promisee, about-entity, kind, due range

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1345-1345` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CMT-012; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CMT-012 | APIs per §19.7, cursor-paginated, filterable by state, promisor, promisee, about-entity, kind, due range.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CMT-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CMT-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CMT-012

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CMT-012 | APIs per §19.7, cursor-paginated, filterable by state, promisor, promisee, about-entity, kind, due range.»
- [ ] APIs per §19.7, cursor-paginated, filterable by state, promisor, promisee, about-entity, kind, due range.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-CMT-013 [P2] REQ-CMT-013: UI 18.20 and metrics kgfipcommitmentkeptratio, kgfipcommitmentsoverdue, kgfipcommitmentsorphaned

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1346-1346` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-CMT-013; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-CMT-013 | UI 18.20 and metrics `kgf_ip_commitment_kept_ratio`, `kgf_ip_commitments_overdue`, `kgf_ip_commitments_orphaned`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-CMT-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-CMT-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-CMT-013

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-CMT-013 | UI 18.20 and metrics kgf_ip_commitment_kept_ratio, kgf_ip_commitments_overdue, kgf_ip_commitments_orphaned.»
- [ ] UI 18.20 and metrics kgf_ip_commitment_kept_ratio, kgf_ip_commitments_overdue, kgf_ip_commitments_orphaned.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DCG-001 [P2] REQ-DCG-001: Protected-fact registry entries: {protectedid, tenantid, pattern, appliestoprincipals (role/group/user selectors), exceptprincipals, reason, owner, createdat}. pattern is a graph pattern in KGF's cano

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:673-673` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DCG-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DCG-001 | Protected-fact registry entries: `{protected_id, tenant_id, pattern, applies_to_principals (role/group/user selectors), except_principals, reason, owner, created_at}`. `pattern` is a graph pattern in KGF's canonical pattern syntax over types, relations and property predicates (e.g., `(p:Person)-[:SUBJECT_OF]->(:LayoffPlan)`), or a single assertion id. Entities, properties or relations annotated `kgf:protected=true` generate registry entries automatically.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DCG-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DCG-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DCG-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DCG-001 | Protected-fact registry entries: {protected_id, tenant_id, pattern, applies_to_principals (role/group/user selectors), except_principals, reason, owner, created_at}. pattern is a graph pattern in KGF's canonical pattern syntax over types, relations and property predicates (e.g., (p:Person)-[:SUBJECT_OF]->(:LayoffPlan)), or a single assertion id. Entities, properti»
- [ ] Protected-fact registry entries: {protected_id, tenant_id, pattern, applies_to_principals (role/group/user selectors), except_principals, reason, owner, created_at}. pattern is a graph pattern in KGF's canonical pattern syntax over types, relations and property predicates (e.g., (p:Person)-[:SUBJECT_OF]->(:LayoffPlan)), or a single assertion id. Entities, properties or relations annotated kgf:prot
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DCG-011 [P2] REQ-DCG-011: Absent-capability rule: if KGF has no rule engine, embed one that runs locally (e.g., an OWL 2 RL / Datalog engine), loading the tenant ontology's rules; record DR

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:699-699` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DCG-011; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DCG-011 | Absent-capability rule: if KGF has no rule engine, embed one that runs locally (e.g., an OWL 2 RL / Datalog engine), loading the tenant ontology's rules; record DR.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DCG-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DCG-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DCG-011

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DCG-011 | Absent-capability rule: if KGF has no rule engine, embed one that runs locally (e.g., an OWL 2 RL / Datalog engine), loading the tenant ontology's rules; record DR.»
- [ ] Absent-capability rule: if KGF has no rule engine, embed one that runs locally (e.g., an OWL 2 RL / Datalog engine), loading the tenant ontology's rules; record DR.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DCG-012 [P2] REQ-DCG-012: POST /derivation/check (request: principalid, sessionid, candidateassertionids[]) returns per candidate {decision, protectedids[], derivationids[]}. GET /derivation/blocks lists blocks with filters

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:700-700` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DCG-012; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DCG-012 | `POST /derivation/check` (request: `principal_id`, `session_id`, `candidate_assertion_ids[]`) returns per candidate `{decision, protected_ids[], derivation_ids[]}`. `GET /derivation/blocks` lists blocks with filters.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DCG-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DCG-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DCG-012

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DCG-012 | POST /derivation/check (request: principal_id, session_id, candidate_assertion_ids[]) returns per candidate {decision, protected_ids[], derivation_ids[]}. GET /derivation/blocks lists blocks with filters.»
- [ ] POST /derivation/check (request: principal_id, session_id, candidate_assertion_ids[]) returns per candidate {decision, protected_ids[], derivation_ids[]}. GET /derivation/blocks lists blocks with filters.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DCG-014 [P2] REQ-DCG-014: Performance: p95 < 200 ms with · K · ≤ 2,000 and ≤ 500 rules.

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:702-702` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DCG-014; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DCG-014 | Performance: p95 < 200 ms with | K | ≤ 2,000 and ≤ 500 rules.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DCG-014' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DCG-014') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DCG-014

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DCG-014 | Performance: p95 < 200 ms with | K | ≤ 2,000 and ≤ 500 rules.»
- [ ] Performance: p95 < 200 ms with
- [ ] ≤ 2,000 and ≤ 500 rules.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DIS-003 [P2] REQ-DIS-003: Diversity: deliberations whose actionclass ≥ dissent.requiredfromactionclass require ≥ dissent.minindependent participants with distinct values of dissent.diversitykey (model family, context source, o

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1384-1384` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DIS-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DIS-003 | Diversity: deliberations whose `action_class` ≥ `dissent.required_from_action_class` require ≥ `dissent.min_independent` participants with distinct values of `dissent.diversity_key` (model family, context source, or principal). Otherwise `DIS_INSUFFICIENT_DIVERSITY`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DIS-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DIS-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DIS-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DIS-003 | Diversity: deliberations whose action_class ≥ dissent.required_from_action_class require ≥ dissent.min_independent participants with distinct values of dissent.diversity_key (model family, context source, or principal). Otherwise DIS_INSUFFICIENT_DIVERSITY.»
- [ ] Diversity: deliberations whose action_class ≥ dissent.required_from_action_class require ≥ dissent.min_independent participants with distinct values of dissent.diversity_key (model family, context source, or principal). Otherwise DIS_INSUFFICIENT_DIVERSITY.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DIS-004 [P2] REQ-DIS-004: Grounded stance changes: when a participant's option differs from its previous round, the change is GROUNDEDSHIFT only if its new rationale contains at least one proposition whose warrant grounds incl

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1385-1385` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DIS-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DIS-004 | Grounded stance changes: when a participant's option differs from its previous round, the change is `GROUNDED_SHIFT` only if its new rationale contains at least one proposition whose warrant grounds include a ground id that the participant had not cited or been shown in any earlier round and whose status is ≥ `PREDICTED`; otherwise `UNGROUNDED_SHIFT`. Restating another participant's rationale is not a new ground.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DIS-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DIS-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DIS-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DIS-004 | Grounded stance changes: when a participant's option differs from its previous round, the change is GROUNDED_SHIFT only if its new rationale contains at least one proposition whose warrant grounds include a ground id that the participant had not cited or been shown in any earlier round and whose status is ≥ PREDICTED; otherwise UNGROUNDED_SHIFT. Restating another »
- [ ] Grounded stance changes: when a participant's option differs from its previous round, the change is GROUNDED_SHIFT only if its new rationale contains at least one proposition whose warrant grounds include a ground id that the participant had not cited or been shown in any earlier round and whose status is ≥ PREDICTED; otherwise UNGROUNDED_SHIFT. Restating another participant's rationale is not a n
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DIS-005 [P2] REQ-DIS-005: Minority report: on decide, if round-0 positions were not unanimous, a minority report is mandatory. It contains every round-0 position whose option differs from the decided option (even if the partic

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1386-1386` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DIS-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DIS-005 | Minority report: on `decide`, if round-0 positions were not unanimous, a minority report is mandatory. It contains every round-0 position whose option differs from the decided option (even if the participant later shifted), plus any final-round dissent; a summary generated through the SDK (its propositions keep SASI statuses); and revisit triggers derived automatically from the entities in the dissenting positions' grounds (graph-change triggers) plus an optional date set by the decision owner. A decision without a required minority report is rejected.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DIS-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DIS-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DIS-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DIS-005 | Minority report: on decide, if round-0 positions were not unanimous, a minority report is mandatory. It contains every round-0 position whose option differs from the decided option (even if the participant later shifted), plus any final-round dissent; a summary generated through the SDK (its propositions keep SASI statuses); and revisit triggers derived automatica»
- [ ] Minority report: on decide, if round-0 positions were not unanimous, a minority report is mandatory. It contains every round-0 position whose option differs from the decided option (even if the participant later shifted), plus any final-round dissent; a summary generated through the SDK (its propositions keep SASI statuses); and revisit triggers derived automatically from the entities in the disse
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DIS-006 [P2] REQ-DIS-006: Human approval view: when a decision feeds an escalation or approval (§9.2), the approver sees the minority report and the ungrounded shifts before deciding

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1387-1387` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DIS-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DIS-006 | Human approval view: when a decision feeds an escalation or approval (§9.2), the approver sees the minority report and the ungrounded shifts before deciding.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DIS-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DIS-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DIS-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DIS-006 | Human approval view: when a decision feeds an escalation or approval (§9.2), the approver sees the minority report and the ungrounded shifts before deciding.»
- [ ] Human approval view: when a decision feeds an escalation or approval (§9.2), the approver sees the minority report and the ungrounded shifts before deciding.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DIS-007 [P2] REQ-DIS-007: Revisit triggers: on a matching kgf.graph.changed event or date, emit kgf.ip.minority.revisit and notify the decision owner with the changed facts. The owner can record POST /decisions/{id}/vindicatio

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1388-1388` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DIS-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DIS-007 | Revisit triggers: on a matching `kgf.graph.changed` event or date, emit `kgf.ip.minority.revisit` and notify the decision owner with the changed facts. The owner can record `POST /decisions/{id}/vindication {vindicated: true | false, note}` with an `ATTESTED` warrant.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DIS-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DIS-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DIS-007

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DIS-007 | Revisit triggers: on a matching kgf.graph.changed event or date, emit kgf.ip.minority.revisit and notify the decision owner with the changed facts. The owner can record `POST /decisions/{id}/vindication {vindicated: true | false, note} with an ATTESTED` warrant.»
- [ ] Revisit triggers: on a matching kgf.graph.changed event or date, emit kgf.ip.minority.revisit and notify the decision owner with the changed facts. The owner can record `POST /decisions/{id}/vindication {vindicated: true
- [ ] false, note} with an ATTESTED` warrant.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DIS-008 [P2] REQ-DIS-008: Metrics per §16: dissent preservation ratio, homogenization index, ungrounded shift ratio, minority vindicated total; per agent and per model family

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1389-1389` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DIS-008; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DIS-008 | Metrics per §16: dissent preservation ratio, homogenization index, ungrounded shift ratio, minority vindicated total; per agent and per model family.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DIS-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DIS-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DIS-008

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DIS-008 | Metrics per §16: dissent preservation ratio, homogenization index, ungrounded shift ratio, minority vindicated total; per agent and per model family.»
- [ ] Metrics per §16: dissent preservation ratio, homogenization index, ungrounded shift ratio, minority vindicated total; per agent and per model family.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DIS-009 [P2] REQ-DIS-009: Benchmark evals/dissent/minority-v1: ≥ 100 synthetic deliberation tasks over the demo tenant where the correct answer is held by a minority of round-0 positions (planted by giving one participant a de

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1390-1390` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DIS-009; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DIS-009 | Benchmark `evals/dissent/minority-v1`: ≥ 100 synthetic deliberation tasks over the demo tenant where the correct answer is held by a minority of round-0 positions (planted by giving one participant a decisive fact). Acceptance: the correct minority position appears in the minority report in ≥ 95% of tasks where it appeared in round 0; ungrounded-shift detection precision ≥ 0.9 against hand labels on 100 stance changes.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DIS-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DIS-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DIS-009

**Acceptance criteria**
- [ ] the correct minority position appears in the minority report in ≥ 95% of tasks where it appeared in round 0; ungrounded-shift detection precision ≥ 0.9 against hand labels on 100 stance changes
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DIS-010 [P2] REQ-DIS-010: UI 18.21 and APIs per §19.7

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1391-1391` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DIS-010; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DIS-010 | UI 18.21 and APIs per §19.7.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DIS-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DIS-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DIS-010

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DIS-010 | UI 18.21 and APIs per §19.7.»
- [ ] UI 18.21 and APIs per §19.7.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DIS-011 [P2] REQ-DIS-011: Demonstration scenario: three participants (two model families plus bob) decide whether to restart customer-db. One agent's round-0 position cites an observed replication-lag fact and says "do not res

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1392-1392` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DIS-011; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DIS-011 | Demonstration scenario: three participants (two model families plus `bob`) decide whether to restart customer-db. One agent's round-0 position cites an observed replication-lag fact and says "do not restart". In round 1 it switches to "restart" without new grounds → `UNGROUNDED_SHIFT`. The decision is "restart"; the minority report keeps the replication-lag position; the approver sees it; a later change to the replication-lag fact fires a revisit notice.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DIS-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DIS-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DIS-011

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DIS-011 | Demonstration scenario: three participants (two model families plus bob) decide whether to restart customer-db. One agent's round-0 position cites an observed replication-lag fact and says "do not restart". In round 1 it switches to "restart" without new grounds → UNGROUNDED_SHIFT. The decision is "restart"; the minority report keeps the replication-lag position; »
- [ ] Demonstration scenario: three participants (two model families plus bob) decide whether to restart customer-db. One agent's round-0 position cites an observed replication-lag fact and says "do not restart". In round 1 it switches to "restart" without new grounds → UNGROUNDED_SHIFT. The decision is "restart"; the minority report keeps the replication-lag position; the approver sees it; a later chan
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DSC-002 [P2] REQ-DSC-002: GET /disciplines/{id}/metrics?from&to returns the discipline's metrics as time series at daily granularity for the requested window (max 400 days)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1288-1288` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DSC-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DSC-002 | `GET /disciplines/{id}/metrics?from&to` returns the discipline's metrics as time series at daily granularity for the requested window (max 400 days).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DSC-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DSC-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DSC-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DSC-002 | GET /disciplines/{id}/metrics?from&to returns the discipline's metrics as time series at daily granularity for the requested window (max 400 days).»
- [ ] GET /disciplines/{id}/metrics?from&to returns the discipline's metrics as time series at daily granularity for the requested window (max 400 days).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DSC-004 [P2] REQ-DSC-004: GET /disciplines/warrant/maturity returns {level, criteria: [{level, criterion, met, value, threshold}]}; screen 18.23 shows unmet criteria with links to the screen or setting that fixes each

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1290-1290` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DSC-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DSC-004 | `GET /disciplines/warrant/maturity` returns `{level, criteria: [{level, criterion, met, value, threshold}]}`; screen 18.23 shows unmet criteria with links to the screen or setting that fixes each.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DSC-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DSC-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DSC-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DSC-004 | GET /disciplines/warrant/maturity returns {level, criteria: [{level, criterion, met, value, threshold}]}; screen 18.23 shows unmet criteria with links to the screen or setting that fixes each.»
- [ ] GET /disciplines/warrant/maturity returns {level, criteria: [{level, criterion, met, value, threshold}]}; screen 18.23 shows unmet criteria with links to the screen or setting that fixes each.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-DSC-005 [P2] REQ-DSC-005: Discipline catalogue entries, definitions and maturity are visible to principals with ip.disciplines.view; no tenant data beyond aggregates is shown

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:1291-1291` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-DSC-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-DSC-005 | Discipline catalogue entries, definitions and maturity are visible to principals with `ip.disciplines.view`; no tenant data beyond aggregates is shown.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-DSC-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-DSC-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-DSC-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-DSC-005 | Discipline catalogue entries, definitions and maturity are visible to principals with ip.disciplines.view; no tenant data beyond aggregates is shown.»
- [ ] Discipline catalogue entries, definitions and maturity are visible to principals with ip.disciplines.view; no tenant data beyond aggregates is shown.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-EXP-004 [P2] REQ-EXP-004: Exports never include data the requesting principal could not read at export time; the derivation guard runs on the bundle contents

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:516-516` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-EXP-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-EXP-004 | Exports never include data the requesting principal could not read at export time; the derivation guard runs on the bundle contents.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-EXP-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-EXP-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-EXP-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-EXP-004 | Exports never include data the requesting principal could not read at export time; the derivation guard runs on the bundle contents.»
- [ ] Exports never include data the requesting principal could not read at export time; the derivation guard runs on the bundle contents.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-HLF-002 [P2] REQ-HLF-002: When freshness of an assertion of a type with kgf:criticality ≥ halflife.mincriticalityfortasks (default 3) falls below halflife.phi (default 0.5), create a verification task with reason HALFLIFEDUE. 

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:599-599` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-HLF-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-HLF-002 | When freshness of an assertion of a type with `kgf:criticality ≥ halflife.min_criticality_for_tasks` (default 3) falls below `halflife.phi` (default 0.5), create a verification task with reason `HALF_LIFE_DUE`. Rate-limit to `halflife.max_tasks_per_day` (default 200) per tenant, highest criticality first.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-HLF-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-HLF-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-HLF-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-HLF-002 | When freshness of an assertion of a type with kgf:criticality ≥ halflife.min_criticality_for_tasks (default 3) falls below halflife.phi (default 0.5), create a verification task with reason HALF_LIFE_DUE. Rate-limit to halflife.max_tasks_per_day (default 200) per tenant, highest criticality first.»
- [ ] When freshness of an assertion of a type with kgf:criticality ≥ halflife.min_criticality_for_tasks (default 3) falls below halflife.phi (default 0.5), create a verification task with reason HALF_LIFE_DUE. Rate-limit to halflife.max_tasks_per_day (default 200) per tenant, highest criticality first.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-IMP-002 [P2] REQ-IMP-002: POST /impact/propagate (request: changes[]{entityid, changetype, properties[]}, maxhops?, includepaths: bool) returns impactrunid, entities[]{entityid, type, probability, hop, criticality, paths[]}, t

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:634-634` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-IMP-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-IMP-002 | `POST /impact/propagate` (request: `changes[]{entity_id, change_type, properties[]}`, `max_hops?`, `include_paths: bool`) returns `impact_run_id`, `entities[]{entity_id, type, probability, hop, criticality, paths[]}`, `test_checklist[]` (entities of types annotated as tests or with `TESTS`/`VERIFIES` relations to impacted entities, ranked by probability × criticality), `summary_text` (generated through SDK, therefore warranted), `mode` (`prior` or `learned`), `model_version`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-IMP-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-IMP-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-IMP-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-IMP-002 | POST /impact/propagate (request: changes[]{entity_id, change_type, properties[]}, max_hops?, include_paths: bool) returns impact_run_id, entities[]{entity_id, type, probability, hop, criticality, paths[]}, test_checklist[] (entities of types annotated as tests or with TESTS/VERIFIES relations to impacted entities, ranked by probability × criticality), summary_text»
- [ ] POST /impact/propagate (request: changes[]{entity_id, change_type, properties[]}, max_hops?, include_paths: bool) returns impact_run_id, entities[]{entity_id, type, probability, hop, criticality, paths[]}, test_checklist[] (entities of types annotated as tests or with TESTS/VERIFIES relations to impacted entities, ranked by probability × criticality), summary_text (generated through SDK, therefore
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-IMP-003 [P2] REQ-IMP-003: Each response is stored as an impact run with its parameters and is reproducible: re-running with the same snapshot and model version returns identical probabilities (deterministic inference)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:635-635` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-IMP-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-IMP-003 | Each response is stored as an impact run with its parameters and is reproducible: re-running with the same snapshot and model version returns identical probabilities (deterministic inference).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-IMP-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-IMP-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-IMP-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-IMP-003 | Each response is stored as an impact run with its parameters and is reproducible: re-running with the same snapshot and model version returns identical probabilities (deterministic inference).»
- [ ] Each response is stored as an impact run with its parameters and is reproducible: re-running with the same snapshot and model version returns identical probabilities (deterministic inference).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-IMP-004 [P2] REQ-IMP-004: Learned mode is enabled per tenant only when the trained model beats prior mode on the chronological test split by ≥ 5 percentage points AUPRC and has calibration error (ECE) ≤ 0.1; otherwise the tena

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:636-636` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-IMP-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-IMP-004 | Learned mode is enabled per tenant only when the trained model beats prior mode on the chronological test split by ≥ 5 percentage points AUPRC and has calibration error (ECE) ≤ 0.1; otherwise the tenant stays in prior mode and the UI says so.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-IMP-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-IMP-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-IMP-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-IMP-004 | Learned mode is enabled per tenant only when the trained model beats prior mode on the chronological test split by ≥ 5 percentage points AUPRC and has calibration error (ECE) ≤ 0.1; otherwise the tenant stays in prior mode and the UI says so.»
- [ ] Learned mode is enabled per tenant only when the trained model beats prior mode on the chronological test split by ≥ 5 percentage points AUPRC and has calibration error (ECE) ≤ 0.1; otherwise the tenant stays in prior mode and the UI says so.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-IMP-005 [P2] REQ-IMP-005: Performance: p95 < 2 s for · S · ≤ 10, H = 4, on a graph of 1,000,000 nodes / 5,000,000 edges (neighbourhood loaded through the abstraction layer with batched hop expansion).

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:637-637` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-IMP-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-IMP-005 | Performance: p95 < 2 s for | S | ≤ 10, H = 4, on a graph of 1,000,000 nodes / 5,000,000 edges (neighbourhood loaded through the abstraction layer with batched hop expansion).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-IMP-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-IMP-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-IMP-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-IMP-005 | Performance: p95 < 2 s for | S | ≤ 10, H = 4, on a graph of 1,000,000 nodes / 5,000,000 edges (neighbourhood loaded through the abstraction layer with batched hop expansion).»
- [ ] Performance: p95 < 2 s for
- [ ] ≤ 10, H = 4, on a graph of 1,000,000 nodes / 5,000,000 edges (neighbourhood loaded through the abstraction layer with batched hop expansion).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV1-001 [P2] REQ-INV1-001: Compute embeddings for all three levels at each snapshot (instance: heterogeneous GNN self-supervised link prediction; meta-graph: types and relation types with instance-count features; ontology: conc

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:829-829` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV1-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV1-001 | Compute embeddings for all three levels at each snapshot (instance: heterogeneous GNN self-supervised link prediction; meta-graph: types and relation types with instance-count features; ontology: concept graph with axiom edges).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV1-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV1-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV1-001

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV1-001 | Compute embeddings for all three levels at each snapshot (instance: heterogeneous GNN self-supervised link prediction; meta-graph: types and relation types with instance-count features; ontology: concept graph with axiom edges).»
- [ ] Compute embeddings for all three levels at each snapshot (instance: heterogeneous GNN self-supervised link prediction; meta-graph: types and relation types with instance-count features; ontology: concept graph with axiom edges).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV1-002 [P2] REQ-INV1-002: Drift score per entity/type/relation-type: dv = 1 − cos(R·zv^(t−1), zv^(t)) with Procrustes matrix R (REQ-NEU-021)

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:830-830` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV1-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV1-002 | Drift score per entity/type/relation-type: `d_v = 1 − cos(R·z_v^(t−1), z_v^(t))` with Procrustes matrix R (REQ-NEU-021).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV1-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV1-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV1-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV1-002 | Drift score per entity/type/relation-type: d_v = 1 − cos(R·z_v^(t−1), z_v^(t)) with Procrustes matrix R (REQ-NEU-021).»
- [ ] Drift score per entity/type/relation-type: d_v = 1 − cos(R·z_v^(t−1), z_v^(t)) with Procrustes matrix R (REQ-NEU-021).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV1-003 [P2] REQ-INV1-003: Adaptive threshold per type: flag when dv > μT + drift.sigma × σT (default 3) over the trailing drift.window (default 30 snapshots); minimum 5 snapshots before flagging

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:831-831` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV1-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV1-003 | Adaptive threshold per type: flag when `d_v > μ_T + drift.sigma × σ_T` (default 3) over the trailing `drift.window` (default 30 snapshots); minimum 5 snapshots before flagging.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV1-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV1-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV1-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV1-003 | Adaptive threshold per type: flag when d_v > μ_T + drift.sigma × σ_T (default 3) over the trailing drift.window (default 30 snapshots); minimum 5 snapshots before flagging.»
- [ ] Adaptive threshold per type: flag when d_v > μ_T + drift.sigma × σ_T (default 3) over the trailing drift.window (default 30 snapshots); minimum 5 snapshots before flagging.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV1-004 [P2] REQ-INV1-004: Drift classification into exactly these classes: SCHEMADATAMISALIGNMENT, INGESTIONCONTAMINATION, USAGEMEANINGDIVERGENCE, DEPRECATEDRESURRECTION, RELATIONOVERLOADING, OTHER. Phase 1: deterministic rule

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:832-832` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV1-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV1-004 | Drift classification into exactly these classes: `SCHEMA_DATA_MISALIGNMENT`, `INGESTION_CONTAMINATION`, `USAGE_MEANING_DIVERGENCE`, `DEPRECATED_RESURRECTION`, `RELATION_OVERLOADING`, `OTHER`. Phase 1: deterministic rules (documented per class with the signals they use: SHACL violation rate change, share of assertions from a single new source, query-context shift, writes to deprecated types, relation-pair embedding multimodality). Phase 2: a trained classifier replaces rules when ≥ `drift.min_labels` (default 200) steward-labelled events exist and it beats rules on macro-F1 by ≥ 5 points.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV1-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV1-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV1-004

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV1-004 | Drift classification into exactly these classes: SCHEMA_DATA_MISALIGNMENT, INGESTION_CONTAMINATION, USAGE_MEANING_DIVERGENCE, DEPRECATED_RESURRECTION, RELATION_OVERLOADING, OTHER. Phase 1: deterministic rules (documented per class with the signals they use: SHACL violation rate change, share of assertions from a single new source, query-context shift, writes to d»
- [ ] Drift classification into exactly these classes: SCHEMA_DATA_MISALIGNMENT, INGESTION_CONTAMINATION, USAGE_MEANING_DIVERGENCE, DEPRECATED_RESURRECTION, RELATION_OVERLOADING, OTHER. Phase 1: deterministic rules (documented per class with the signals they use: SHACL violation rate change, share of assertions from a single new source, query-context shift, writes to deprecated types, relation-pair embe
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV1-005 [P2] REQ-INV1-005: Cross-level correlation: a drift event links to co-occurring drift at other levels (same type at meta/ontology level) and is scored higher when it appears on ≥ 2 levels

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:833-833` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV1-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV1-005 | Cross-level correlation: a drift event links to co-occurring drift at other levels (same type at meta/ontology level) and is scored higher when it appears on ≥ 2 levels.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV1-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV1-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV1-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV1-005 | Cross-level correlation: a drift event links to co-occurring drift at other levels (same type at meta/ontology level) and is scored higher when it appears on ≥ 2 levels.»
- [ ] Cross-level correlation: a drift event links to co-occurring drift at other levels (same type at meta/ontology level) and is scored higher when it appears on ≥ 2 levels.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV1-006 [P2] REQ-INV1-006: Self-healing proposals per class (at least): constraint tightening (SHACL shape change), entity split, relation re-typing, ingestion rule amendment (mapping change or source quarantine), deprecation e

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:834-834` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV1-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV1-006 | Self-healing proposals per class (at least): constraint tightening (SHACL shape change), entity split, relation re-typing, ingestion rule amendment (mapping change or source quarantine), deprecation enforcement. Each proposal includes simulated impact: affected entities (Invention 2), queries whose results change (replay of saved queries on a shadow branch, §13), constraint violations before/after.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV1-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV1-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV1-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV1-006 | Self-healing proposals per class (at least): constraint tightening (SHACL shape change), entity split, relation re-typing, ingestion rule amendment (mapping change or source quarantine), deprecation enforcement. Each proposal includes simulated impact: affected entities (Invention 2), queries whose results change (replay of saved queries on a shadow branch, §13),»
- [ ] Self-healing proposals per class (at least): constraint tightening (SHACL shape change), entity split, relation re-typing, ingestion rule amendment (mapping change or source quarantine), deprecation enforcement. Each proposal includes simulated impact: affected entities (Invention 2), queries whose results change (replay of saved queries on a shadow branch, §13), constraint violations before/after
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV1-007 [P2] REQ-INV1-007: Auto-apply only when drift.autoapply=true (default false) AND severity = low AND classifier confidence ≥ 0.9 AND simulated impact touches ≤ 10 entities; everything else goes to the steward queue

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:835-835` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV1-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV1-007 | Auto-apply only when `drift.auto_apply=true` (default false) AND severity = low AND classifier confidence ≥ 0.9 AND simulated impact touches ≤ 10 entities; everything else goes to the steward queue.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV1-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV1-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV1-007

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV1-007 | Auto-apply only when drift.auto_apply=true (default false) AND severity = low AND classifier confidence ≥ 0.9 AND simulated impact touches ≤ 10 entities; everything else goes to the steward queue.»
- [ ] Auto-apply only when drift.auto_apply=true (default false) AND severity = low AND classifier confidence ≥ 0.9 AND simulated impact touches ≤ 10 entities; everything else goes to the steward queue.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV1-008 [P2] REQ-INV1-008: APIs: GET /drift/events, GET /drift/events/{id}, POST /drift/events/{id}/label, GET /drift/events/{id}/proposals, POST /drift/proposals/{pid}/apply

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:836-836` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV1-008; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV1-008 | APIs: `GET /drift/events`, `GET /drift/events/{id}`, `POST /drift/events/{id}/label`, `GET /drift/events/{id}/proposals`, `POST /drift/proposals/{pid}/apply | reject`. Events feed Brain Health (REQ-MET-012).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV1-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV1-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV1-008

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV1-008 | APIs: GET /drift/events, GET /drift/events/{id}, POST /drift/events/{id}/label, GET /drift/events/{id}/proposals, `POST /drift/proposals/{pid}/apply | reject`. Events feed Brain Health (REQ-MET-012).»
- [ ] APIs: GET /drift/events, GET /drift/events/{id}, POST /drift/events/{id}/label, GET /drift/events/{id}/proposals, `POST /drift/proposals/{pid}/apply
- [ ] reject`. Events feed Brain Health (REQ-MET-012).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REQ-INV1-009 [P2] REQ-INV1-009: Demonstration scenario: inject 300 assertions from a new source that systematically uses Server for containers; heartbeat flags INGESTIONCONTAMINATION on Server within one snapshot cycle, proposes an 

- **Source:** `EOIP-engg-doc-pkg/ip-requirements.md:837-837` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-REQ-INV1-009; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REQ-INV1-009 | Demonstration scenario: inject 300 assertions from a new source that systematically uses `Server` for containers; heartbeat flags `INGESTION_CONTAMINATION` on `Server` within one snapshot cycle, proposes an ingestion rule amendment with simulated impact; steward applies; next cycle clears the hotspot.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REQ-INV1-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REQ-INV1-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-REQ-INV1-009

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REQ-INV1-009 | Demonstration scenario: inject 300 assertions from a new source that systematically uses Server for containers; heartbeat flags INGESTION_CONTAMINATION on Server within one snapshot cycle, proposes an ingestion rule amendment with simulated impact; steward applies; next cycle clears the hotspot.»
- [ ] Demonstration scenario: inject 300 assertions from a new source that systematically uses Server for containers; heartbeat flags INGESTION_CONTAMINATION on Server within one snapshot cycle, proposes an ingestion rule amendment with simulated impact; steward applies; next cycle clears the hotspot.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

