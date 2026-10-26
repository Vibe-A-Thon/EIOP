# EPIC-REVA-UNTR-01: reva-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 60 tasks, ~366.0 h, priorities {'P0': 18, 'P1': 42}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-C-07 [P0] C-07: Tenant isolation. Data, keys, logs, caches, blobs and indexes are tenant-scoped; cross-tenant leakage is a P0 defect

- **Source:** `reva-requirements.md:277-277` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 7.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
C-07 | **Tenant isolation.** Data, keys, logs, caches, blobs and indexes are tenant-scoped; cross-tenant leakage is a P0 defect.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'C-07' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('C-07') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «C-07 | Tenant isolation. Data, keys, logs, caches, blobs and indexes are tenant-scoped; cross-tenant leakage is a P0 defect.»
- [ ] Tenant isolation. Data, keys, logs, caches, blobs and indexes are tenant-scoped; cross-tenant leakage is a P0 defect.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-REVA-AB-006 [P0] REVA-AB-006: Resources (W-05): detect and model as reva_Resource with access mode: files (fs., open(), java.nio.file.Files.), DB tables (SQL string literals parsed with a lightweight SQL tokenizer for FROM/JOIN/IN

- **Source:** `reva-requirements.md:880-880` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AB-006 | **Resources (W-05)**: detect and model as `reva_Resource` with access mode: files (`fs.*`, `open()`, `java.nio.file.Files.*`), DB tables (SQL string literals parsed with a lightweight SQL tokenizer for `FROM/JOIN/INTO/UPDATE/DELETE` table names; JPA `@Entity/@Table(name)`; SQLAlchemy `__tablename__`; Prisma model calls; Mongoose model names), cache keys (Redis client `get/set/del` with literal or templated keys), queues/topics (from AB-004), secrets and env vars (`process.env`, `os.getenv`, `System.getenv`, Spring placeholders), service accounts (identifiers matching configured patterns `REVA_SERVICE_ACCOUNT_PATTERNS`, plus Kubernetes `serviceAccountName`, IAM role ARNs and connection-string user names in config files), buckets (S3/GCS SDK calls with literal names). | E-02 regression: the fixture's `fs.writeFileSync` becomes a `file` resource with `write` mode; each resource kind has a fixture. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AB-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AB-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] E-02 regression: the fixture's fs.writeFileSync becomes a file resource with write mode; each resource kind has a fixture
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-DV-004 [P0] REVA-DV-004: Configuration drift: compare deployed config files found in artifacts/images with repo config at the commit (key-level diff, values hashed when classified sensitive). · Fixture with one changed key re

- **Source:** `reva-requirements.md:966-966` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-DV-004 | Configuration drift: compare deployed config files found in artifacts/images with repo config at the commit (key-level diff, values hashed when classified sensitive). | Fixture with one changed key reports it with hashed values for a secret key. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-DV-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-DV-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture with one changed key reports it with hashed values for a secret key
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-048 [P0] REVA-IF-048: POST /firmware/carve (image upload), GET /firmware/{digest}/partitions, GET /firmware/{digest}/secrets · Firmware partition carving & secrets · analyst

- **Source:** `reva-requirements.md:1249-1249` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-048 | `POST /firmware/carve` (image upload), `GET /firmware/{digest}/partitions`, `GET /firmware/{digest}/secrets` | Firmware partition carving & secrets | analyst
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-048' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-048') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-048 | POST /firmware/carve (image upload), GET /firmware/{digest}/partitions, GET /firmware/{digest}/secrets | Firmware partition carving & secrets | analyst»
- [ ] POST /firmware/carve (image upload), GET /firmware/{digest}/partitions, GET /firmware/{digest}/secrets
- [ ] Firmware partition carving & secrets
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-MC-001 [P0] REVA-MC-001: REST API under /api/reva/v1 implementing every endpoint in §9.1, authenticated and tenant-scoped through KGF's auth middleware (AuthPort). OpenAPI 3.1 is generated and published at /api/reva/v1/openap

- **Source:** `reva-requirements.md:985-985` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-MC-001 | REST API under `/api/reva/v1` implementing every endpoint in §9.1, authenticated and tenant-scoped through KGF's auth middleware (AuthPort). OpenAPI 3.1 is generated and published at `/api/reva/v1/openapi.json`. | Contract tests for every endpoint (success, validation error, unauthorized, not found, budget overflow). | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-MC-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-MC-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Contract tests for every endpoint (success, validation error, unauthorized, not found, budget overflow)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-OB-002 [P0] REVA-OB-002: Structured JSON logs with tenant_id, correlation_id, principal, operation, no secrets (redaction filter). · Log scan test. · integration

- **Source:** `reva-requirements.md:1063-1063` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-OB-002 | Structured JSON logs with `tenant_id`, `correlation_id`, `principal`, `operation`, no secrets (redaction filter). | Log scan test. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-OB-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-OB-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-OB-002 | Structured JSON logs with tenant_id, correlation_id, principal, operation, no secrets (redaction filter). | Log scan test. | integration»
- [ ] Structured JSON logs with tenant_id, correlation_id, principal, operation, no secrets (redaction filter).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-OB-005 [P0] REVA-OB-005: Backup/restore: relational store dump + blob store + keys (encrypted) + logs; restore verifies every warrant ID and log consistency before serving. · Restore drill in RJ-12. · acceptance

- **Source:** `reva-requirements.md:1066-1066` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-OB-005 | Backup/restore: relational store dump + blob store + keys (encrypted) + logs; restore verifies every warrant ID and log consistency before serving. | Restore drill in RJ-12. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-OB-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-OB-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Restore drill in RJ-12
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SEC-003 [P0] REVA-SEC-003: ACL revocation: when a connector reports revoked access, affected warrants, cached views, continuation tokens and trace results become invisible to the revoked principals within REVA_ACL_PROPAGATION_S

- **Source:** `reva-requirements.md:1024-1024` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SEC-003 | ACL revocation: when a connector reports revoked access, affected warrants, cached views, continuation tokens and trace results become invisible to the revoked principals within `REVA_ACL_PROPAGATION_S` (default 60 s). | Revocation journey (part of RJ-07). | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SEC-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SEC-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Revocation journey (part of RJ-07)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SEC-004 [P0] REVA-SEC-004: Classification: warrants inherit classification from sources; statements of restricted warrants storing PII values use salted commitments (HMAC-SHA256 with a tenant secret) instead of raw values where

- **Source:** `reva-requirements.md:1025-1025` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SEC-004 | Classification: warrants inherit classification from sources; statements of `restricted` warrants storing PII values use salted commitments (HMAC-SHA256 with a tenant secret) instead of raw values where the predicate declares `pii_fields`. | Fixture PII fields are stored as commitments; equality search via commitment works; raw values are absent from storage. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SEC-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SEC-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture PII fields are stored as commitments; equality search via commitment works; raw values are absent from storage
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SEC-006 [P0] REVA-SEC-006: Untrusted input handling: all parsers run in sandboxed workers (REVA-VS-010); REVA never fetches URLs found in content (no SSRF); archive extraction rules (REVA-AI-003). · Static check: no HTTP client

- **Source:** `reva-requirements.md:1027-1027` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SEC-006 | Untrusted input handling: all parsers run in sandboxed workers (REVA-VS-010); REVA never fetches URLs found in content (no SSRF); archive extraction rules (REVA-AI-003). | Static check: no HTTP client usage in extractor modules; SSRF fixture with URLs in content triggers no network call (network namespace audit). | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SEC-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SEC-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Static check: no HTTP client usage in extractor modules; SSRF fixture with URLs in content triggers no network call (network namespace audit)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SEC-008 [P0] REVA-SEC-008: Authorization roles (mapped to KGF roles): reva.viewer (read warrants/results within ACL), reva.analyst (run workflows, record gaps), reva.reviewer (review obligations, resolve contradictions, waivers

- **Source:** `reva-requirements.md:1029-1029` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SEC-008 | Authorization roles (mapped to KGF roles): `reva.viewer` (read warrants/results within ACL), `reva.analyst` (run workflows, record gaps), `reva.reviewer` (review obligations, resolve contradictions, waivers), `reva.verifier` (start verifier runs), `reva.admin` (keys, policies, doctor). | Role matrix test across endpoints/tools. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SEC-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SEC-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Role matrix test across endpoints/tools
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SEC-009 [P0] REVA-SEC-009: Audit: every mutating action (record gap, resolve contradiction, waive, start run, change policy, rotate key) is itself a warrant by the acting human/system producer. · Audit view lists actions with v

- **Source:** `reva-requirements.md:1030-1030` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SEC-009 | Audit: every mutating action (record gap, resolve contradiction, waive, start run, change policy, rotate key) is itself a warrant by the acting human/system producer. | Audit view lists actions with verifiable signatures. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SEC-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SEC-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Audit view lists actions with verifiable signatures
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SEC-011 [P0] REVA-SEC-011: Sandbox hardening: verifier containers run as non-root, read-only root filesystem except the work dir, no Docker socket, no-new-privileges, dropped capabilities, seccomp default profile. · Container i

- **Source:** `reva-requirements.md:1032-1032` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SEC-011 | Sandbox hardening: verifier containers run as non-root, read-only root filesystem except the work dir, no Docker socket, `no-new-privileges`, dropped capabilities, seccomp default profile. | Container inspect test asserts each setting. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SEC-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SEC-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Container inspect test asserts each setting
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-TST-006 [P0] REVA-TST-006: Conformance suites: (a) GraphPort conformance for each backend (HugeGraph, Neo4j; Neptune via a Gremlin-compatible lane or named skip); (b) sandbox profile conformance; (c) MCP contract conformance; (

- **Source:** `reva-requirements.md:1399-1399` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-TST-006 | Conformance suites: (a) GraphPort conformance for each backend (HugeGraph, Neo4j; Neptune via a Gremlin-compatible lane or named skip); (b) sandbox profile conformance; (c) MCP contract conformance; (d) cross-tenant isolation conformance.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-TST-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-TST-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-TST-006 | Conformance suites: (a) GraphPort conformance for each backend (HugeGraph, Neo4j; Neptune via a Gremlin-compatible lane or named skip); (b) sandbox profile conformance; (c) MCP contract conformance; (d) cross-tenant isolation conformance.»
- [ ] Conformance suites: (a) GraphPort conformance for each backend (HugeGraph, Neo4j; Neptune via a Gremlin-compatible lane or named skip); (b) sandbox profile conformance; (c) MCP contract conformance; (d) cross-tenant isolation conformance.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-TST-010 [P0] REVA-TST-010: Security tests: secret-scan of all outputs, cross-tenant suite, ACL propagation, prompt-injection fixtures, zip-bomb/path-traversal fixtures, SSRF network audit

- **Source:** `reva-requirements.md:1403-1403` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-TST-010 | Security tests: secret-scan of all outputs, cross-tenant suite, ACL propagation, prompt-injection fixtures, zip-bomb/path-traversal fixtures, SSRF network audit.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-TST-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-TST-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-TST-010 | Security tests: secret-scan of all outputs, cross-tenant suite, ACL propagation, prompt-injection fixtures, zip-bomb/path-traversal fixtures, SSRF network audit.»
- [ ] Security tests: secret-scan of all outputs, cross-tenant suite, ACL propagation, prompt-injection fixtures, zip-bomb/path-traversal fixtures, SSRF network audit.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-XP-001 [P0] REVA-XP-001: External commercial decompiler RPC bridge (IDA Pro / Hopper daemon). Connects over authenticated TLS socket to a tenant-hosted commercial decompiler daemon. · Enabled with REVA_XP_COMMERCIAL_DECOMPILE

- **Source:** `reva-requirements.md:1181-1181` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-XP-001 | External commercial decompiler RPC bridge (IDA Pro / Hopper daemon). Connects over authenticated TLS socket to a tenant-hosted commercial decompiler daemon. | Enabled with `REVA_XP_COMMERCIAL_DECOMPILER=true`; requires tenant-provided license; strictly optional. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-XP-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-XP-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-XP-001 | External commercial decompiler RPC bridge (IDA Pro / Hopper daemon). Connects over authenticated TLS socket to a tenant-hosted commercial decompiler daemon. | Enabled with REVA_XP_COMMERCIAL_DECOMPILER=true; requires tenant-provided license; strictly optional. | integration»
- [ ] External commercial decompiler RPC bridge (IDA Pro / Hopper daemon). Connects over authenticated TLS socket to a tenant-hosted commercial decompiler daemon.
- [ ] Enabled with REVA_XP_COMMERCIAL_DECOMPILER=true; requires tenant-provided license; strictly optional.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RJ-10 [P0] RJ-10: API surface and reconciliation. Ingest HAR + OTel + NGINX logs for the fixture estate; reconcile with static boundaries

- **Source:** `reva-requirements.md:1419-1419` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RJ-10 | **API surface and reconciliation.** Ingest HAR + OTel + NGINX logs for the fixture estate; reconcile with static boundaries. | Templating collapses slug IDs (E-07 regression); secrets never stored (byte scan); OpenAPI alignment categories correct; matched/static-only/runtime-only/ambiguous counts equal golden; no "dead" claim under sampled coverage.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RJ-10' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RJ-10') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RJ-10 | API surface and reconciliation. Ingest HAR + OTel + NGINX logs for the fixture estate; reconcile with static boundaries. | Templating collapses slug IDs (E-07 regression); secrets never stored (byte scan); OpenAPI alignment categories correct; matched/static-only/runtime-only/ambiguous counts equal golden; no "dead" claim under sampled coverage.»
- [ ] API surface and reconciliation. Ingest HAR + OTel + NGINX logs for the fixture estate; reconcile with static boundaries.
- [ ] Templating collapses slug IDs (E-07 regression); secrets never stored (byte scan); OpenAPI alignment categories correct; matched/static-only/runtime-only/ambiguous counts equal golden; no "dead" claim under sampled coverage.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RJ-15 [P0] RJ-15: Controlled Dynamic Tracing, Headless Browser CDP Observation, and Cross-Version Binary Diff. Issue a dual-key signed authorization token; trigger ephemeral containerized GDB tracing for a test binary;

- **Source:** `reva-requirements.md:1424-1424` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RJ-15 | **Controlled Dynamic Tracing, Headless Browser CDP Observation, and Cross-Version Binary Diff.** Issue a dual-key signed authorization token; trigger ephemeral containerized GDB tracing for a test binary; observe instruction stream into bounded ring-buffer; trigger supervised headless browser scenario against fixture SPA web app; verify real-time RFC 6901 redaction on Authorization headers and cookies; upload binary v1 and v2 with reordered functions and reallocated addresses; run binary diff (`POST /api/reva/v1/diff/binaries`). | Dynamic tracer halts at designated breakpoint and enforces 64 KiB read bound; headless browser records video and screenshot attestation with 100% credential redaction; binary diff correctly identifies unchanged, modified, and added functions using CFG isomorphism and GED $\ge 0.90$ without false-positive AST churn.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RJ-15' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RJ-15') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RJ-15 | Controlled Dynamic Tracing, Headless Browser CDP Observation, and Cross-Version Binary Diff. Issue a dual-key signed authorization token; trigger ephemeral containerized GDB tracing for a test binary; observe instruction stream into bounded ring-buffer; trigger supervised headless browser scenario against fixture SPA web app; verify real-time RFC 6901 redaction on Autho»
- [ ] Controlled Dynamic Tracing, Headless Browser CDP Observation, and Cross-Version Binary Diff. Issue a dual-key signed authorization token; trigger ephemeral containerized GDB tracing for a test binary; observe instruction stream into bounded ring-buffer; trigger supervised headless browser scenario against fixture SPA web app; verify real-time RFC 6901 redaction on Authorization headers and cookies
- [ ] Dynamic tracer halts at designated breakpoint and enforces 64 KiB read bound; headless browser records video and screenshot attestation with 100% credential redaction; binary diff correctly identifies unchanged, modified, and added functions using CFG isomorphism and GED $\ge 0.90$ without false-positive AST churn.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-C-01 [P1] C-01: Local-first, air-gap capable. Every REVA capability works with no internet access. No mandatory SaaS, cloud service or external LLM

- **Source:** `reva-requirements.md:271-271` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
C-01 | **Local-first, air-gap capable.** Every REVA capability works with no internet access. No mandatory SaaS, cloud service or external LLM.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'C-01' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('C-01') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «C-01 | Local-first, air-gap capable. Every REVA capability works with no internet access. No mandatory SaaS, cloud service or external LLM.»
- [ ] Local-first, air-gap capable. Every REVA capability works with no internet access. No mandatory SaaS, cloud service or external LLM.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-C-02 [P1] C-02: External-LLM egress policy. REVA never sends raw enterprise content to an external model unless the tenant's egress policy explicitly allows that data class. The default is local models only

- **Source:** `reva-requirements.md:272-272` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
C-02 | **External-LLM egress policy.** REVA never sends raw enterprise content to an external model unless the tenant's egress policy explicitly allows that data class. The default is local models only.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'C-02' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('C-02') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «C-02 | External-LLM egress policy. REVA never sends raw enterprise content to an external model unless the tenant's egress policy explicitly allows that data class. The default is local models only.»
- [ ] External-LLM egress policy. REVA never sends raw enterprise content to an external model unless the tenant's egress policy explicitly allows that data class. The default is local models only.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-C-06 [P1] C-06: Permissions survive everything. Source ACLs are preserved through warrants, graph projection, search, traces, views, caches, exports and answers

- **Source:** `reva-requirements.md:276-276` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
C-06 | **Permissions survive everything.** Source ACLs are preserved through warrants, graph projection, search, traces, views, caches, exports and answers.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'C-06' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('C-06') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «C-06 | Permissions survive everything. Source ACLs are preserved through warrants, graph projection, search, traces, views, caches, exports and answers.»
- [ ] Permissions survive everything. Source ACLs are preserved through warrants, graph projection, search, traces, views, caches, exports and answers.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-IP-01 [P1] IP-01: Mount REVA FastAPI routers under /api/reva/v1

- **Source:** `reva-requirements.md:386-386` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
IP-01 | Mount REVA FastAPI routers under `/api/reva/v1` | `REVA_ENABLED` (false until P1 is complete, then true)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'IP-01' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('IP-01') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «IP-01 | Mount REVA FastAPI routers under /api/reva/v1 | REVA_ENABLED (false until P1 is complete, then true)»
- [ ] Mount REVA FastAPI routers under /api/reva/v1
- [ ] REVA_ENABLED (false until P1 is complete, then true)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-IP-02 [P1] IP-02: Register REVA DB migrations with KGF's migration runner

- **Source:** `reva-requirements.md:387-387` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
IP-02 | Register REVA DB migrations with KGF's migration runner | —
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'IP-02' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('IP-02') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «IP-02 | Register REVA DB migrations with KGF's migration runner | —»
- [ ] Register REVA DB migrations with KGF's migration runner
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-IP-03 [P1] IP-03: GraphPort adapter onto KGF's graph abstraction and mutation gateway

- **Source:** `reva-requirements.md:388-388` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
IP-03 | `GraphPort` adapter onto KGF's graph abstraction and mutation gateway | `REVA_GRAPH_PROJECTION` (true)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'IP-03' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('IP-03') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «IP-03 | GraphPort adapter onto KGF's graph abstraction and mutation gateway | REVA_GRAPH_PROJECTION (true)»
- [ ] GraphPort adapter onto KGF's graph abstraction and mutation gateway
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-IP-04 [P1] IP-04: Hook into KGF's ingestion pipeline after normalization, so connectors can attach source-record warrants

- **Source:** `reva-requirements.md:389-389` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
IP-04 | Hook into KGF's ingestion pipeline after normalization, so connectors can attach source-record warrants | `REVA_INGEST_WARRANTS` (false → true after RJ-01 passes)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'IP-04' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('IP-04') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «IP-04 | Hook into KGF's ingestion pipeline after normalization, so connectors can attach source-record warrants | REVA_INGEST_WARRANTS (false → true after RJ-01 passes)»
- [ ] Hook into KGF's ingestion pipeline after normalization, so connectors can attach source-record warrants
- [ ] REVA_INGEST_WARRANTS (false → true after RJ-01 passes)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-IP-05 [P1] IP-05: Hook into KGF's answer/NL-query pipeline to enforce the grounded-answer contract

- **Source:** `reva-requirements.md:390-390` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
IP-05 | Hook into KGF's answer/NL-query pipeline to enforce the grounded-answer contract | `REVA_ANSWER_CONTRACT` (false → true after RJ-08 passes)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'IP-05' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('IP-05') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «IP-05 | Hook into KGF's answer/NL-query pipeline to enforce the grounded-answer contract | REVA_ANSWER_CONTRACT (false → true after RJ-08 passes)»
- [ ] Hook into KGF's answer/NL-query pipeline to enforce the grounded-answer contract
- [ ] REVA_ANSWER_CONTRACT (false → true after RJ-08 passes)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-IP-06 [P1] IP-06: Register REVA MCP tools with KGF's MCP server, or start REVA's own MCP server if KGF has none

- **Source:** `reva-requirements.md:391-391` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
IP-06 | Register REVA MCP tools with KGF's MCP server, or start REVA's own MCP server if KGF has none | `REVA_MCP` (true)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'IP-06' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('IP-06') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «IP-06 | Register REVA MCP tools with KGF's MCP server, or start REVA's own MCP server if KGF has none | REVA_MCP (true)»
- [ ] Register REVA MCP tools with KGF's MCP server, or start REVA's own MCP server if KGF has none
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-IP-07 [P1] IP-07: Add REVA screens and navigation entries to the KGF frontend

- **Source:** `reva-requirements.md:392-392` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
IP-07 | Add REVA screens and navigation entries to the KGF frontend | `REVA_UI` (true)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'IP-07' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('IP-07') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «IP-07 | Add REVA screens and navigation entries to the KGF frontend | REVA_UI (true)»
- [ ] Add REVA screens and navigation entries to the KGF frontend
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-IP-08 [P1] IP-08: Wire REVA's Proof-of-Done into KGF's completion boards (KGF completion board, Phase 4 board) as the source of done-status

- **Source:** `reva-requirements.md:393-393` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
IP-08 | Wire REVA's Proof-of-Done into KGF's completion boards (KGF completion board, Phase 4 board) as the source of done-status | `REVA_PD_BOARDS` (true)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'IP-08' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('IP-08') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «IP-08 | Wire REVA's Proof-of-Done into KGF's completion boards (KGF completion board, Phase 4 board) as the source of done-status | REVA_PD_BOARDS (true)»
- [ ] Wire REVA's Proof-of-Done into KGF's completion boards (KGF completion board, Phase 4 board) as the source of done-status
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-IP-09 [P1] IP-09: Add reva services and volumes to the KGF Docker Compose file

- **Source:** `reva-requirements.md:394-394` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
IP-09 | Add `reva` services and volumes to the KGF Docker Compose file | —
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'IP-09' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('IP-09') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «IP-09 | Add reva services and volumes to the KGF Docker Compose file | —»
- [ ] Add reva services and volumes to the KGF Docker Compose file
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-IP-10 [P1] IP-10: Add REVA health checks to KGF's health endpoint

- **Source:** `reva-requirements.md:395-395` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
IP-10 | Add REVA health checks to KGF's health endpoint | —
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'IP-10' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('IP-10') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «IP-10 | Add REVA health checks to KGF's health endpoint | —»
- [ ] Add REVA health checks to KGF's health endpoint
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-01 [P1] RC-01: Content-addressed Evidence record (subject digest, provider, analysis profile, operation, parameters, raw/normalized result, confidence, authority, environment, limitations, relationship coverage, loc

- **Source:** `reva-requirements.md:113-113` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-01; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-01 | Content-addressed Evidence record (subject digest, provider, analysis profile, operation, parameters, raw/normalized result, confidence, authority, environment, limitations, relationship coverage, locations, evidence links) | `src/domain/evidence.ts`, `src/domain/canonicalDigest.ts`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-01' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-01') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-01

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-01 | Content-addressed Evidence record (subject digest, provider, analysis profile, operation, parameters, raw/normalized result, confidence, authority, environment, limitations, relationship coverage, locations, evidence links) | src/domain/evidence.ts, src/domain/canonicalDigest.ts»
- [ ] Content-addressed Evidence record (subject digest, provider, analysis profile, operation, parameters, raw/normalized result, confidence, authority, environment, limitations, relationship coverage, locations, evidence links)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-04 [P1] RC-04: Residual unknowns (stable IDs from question+domain+scope; hash-chained revisions; status; severity; required authority/confidence/environment; recommended probes; depends-on/related/contradicts links;

- **Source:** `reva-requirements.md:116-116` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-04; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-04 | Residual unknowns (stable IDs from question+domain+scope; hash-chained revisions; status; severity; required authority/confidence/environment; recommended probes; depends-on/related/contradicts links; verified resolution) | `src/domain/residualUnknown.ts`, `src/application/investigation/*`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-04' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-04') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-04

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-04 | Residual unknowns (stable IDs from question+domain+scope; hash-chained revisions; status; severity; required authority/confidence/environment; recommended probes; depends-on/related/contradicts links; verified resolution) | src/domain/residualUnknown.ts, src/application/investigation/*»
- [ ] Residual unknowns (stable IDs from question+domain+scope; hash-chained revisions; status; severity; required authority/confidence/environment; recommended probes; depends-on/related/contradicts links; verified resolution)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-05 [P1] RC-05: Reconstruction obligation ledger (reviewed obligations, case kinds, required original/fixture/verifier authority, manifest bindings with owner digest, verifier enumerating obligation IDs, closure dige

- **Source:** `reva-requirements.md:117-117` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-05; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-05 | Reconstruction obligation ledger (reviewed obligations, case kinds, required original/fixture/verifier authority, manifest bindings with owner digest, verifier enumerating obligation IDs, closure digest) | `docs/reconstruction-obligation-ledgers.md`, `src/application/ReconstructionObligation*`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-05' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-05') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-05

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-05 | Reconstruction obligation ledger (reviewed obligations, case kinds, required original/fixture/verifier authority, manifest bindings with owner digest, verifier enumerating obligation IDs, closure digest) | docs/reconstruction-obligation-ledgers.md, src/application/ReconstructionObligation*»
- [ ] Reconstruction obligation ledger (reviewed obligations, case kinds, required original/fixture/verifier authority, manifest bindings with owner digest, verifier enumerating obligation IDs, closure digest)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-06 [P1] RC-06: Reconstruction coverage evaluator (verifier authority must match contract authority; inference cannot be promoted)

- **Source:** `reva-requirements.md:118-118` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-06; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-06 | Reconstruction coverage evaluator (verifier authority must match contract authority; inference cannot be promoted) | `docs/reconstruction-coverage.md`, `src/domain/reconstructionCoverage*.ts`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-06' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-06') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-06

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-06 | Reconstruction coverage evaluator (verifier authority must match contract authority; inference cannot be promoted) | docs/reconstruction-coverage.md, src/domain/reconstructionCoverage*.ts»
- [ ] Reconstruction coverage evaluator (verifier authority must match contract authority; inference cannot be promoted)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-10 [P1] RC-10: JavaScript Application Graph (provider-neutral nodes/edges, observations separated from entity identity, 7 identity strategies with stability scopes, authority vs epistemic state vs confidence, explic

- **Source:** `reva-requirements.md:122-122` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-10; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-10 | JavaScript Application Graph (provider-neutral nodes/edges, observations separated from entity identity, 7 identity strategies with stability scopes, authority vs epistemic state vs confidence, explicit unavailable values, coverage) | `docs/javascript-application-graph.md`, `src/domain/javascript/javascriptApplicationGraph*.ts`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-10' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-10') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-10

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-10 | JavaScript Application Graph (provider-neutral nodes/edges, observations separated from entity identity, 7 identity strategies with stability scopes, authority vs epistemic state vs confidence, explicit unavailable values, coverage) | docs/javascript-application-graph.md, src/domain/javascript/javascriptApplicationGraph*.ts»
- [ ] JavaScript Application Graph (provider-neutral nodes/edges, observations separated from entity identity, 7 identity strategies with stability scopes, authority vs epistemic state vs confidence, explicit unavailable values, coverage)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-12 [P1] RC-12: Feature trace from typed seeds (node-id, route, string, channel, module, native-export, API) with paths, authorities, containsinference, native hand-offs and recommended tools

- **Source:** `reva-requirements.md:124-124` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-12; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-12 | Feature trace from typed seeds (node-id, route, string, channel, module, native-export, API) with paths, authorities, `contains_inference`, native hand-offs and recommended tools | `src/domain/javascript/javascriptFeatureTrace*.ts`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-12' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-12') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-12

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-12 | Feature trace from typed seeds (node-id, route, string, channel, module, native-export, API) with paths, authorities, contains_inference, native hand-offs and recommended tools | src/domain/javascript/javascriptFeatureTrace*.ts»
- [ ] Feature trace from typed seeds (node-id, route, string, channel, module, native-export, API) with paths, authorities, contains_inference, native hand-offs and recommended tools
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-16 [P1] RC-16: Web network capture inspection (HAR/SAZ/mitmproxy/qlog) with credential redaction by RFC 6901 pointer and API-surface grouping (method, origin, path template with numeric/uuid/hex/iso-date rules)

- **Source:** `reva-requirements.md:128-128` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-16; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-16 | Web network capture inspection (HAR/SAZ/mitmproxy/qlog) with credential redaction by RFC 6901 pointer and API-surface grouping (method, origin, path template with numeric/uuid/hex/iso-date rules) | `src/domain/webNetworkCapture.ts`, `src/domain/analysisView/WebNetworkApiSurfaceAccumulator.ts`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-16' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-16') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-16

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-16 | Web network capture inspection (HAR/SAZ/mitmproxy/qlog) with credential redaction by RFC 6901 pointer and API-surface grouping (method, origin, path template with numeric/uuid/hex/iso-date rules) | src/domain/webNetworkCapture.ts, src/domain/analysisView/WebNetworkApiSurfaceAccumulator.ts»
- [ ] Web network capture inspection (HAR/SAZ/mitmproxy/qlog) with credential redaction by RFC 6901 pointer and API-surface grouping (method, origin, path template with numeric/uuid/hex/iso-date rules)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-19 [P1] RC-19: Artifact inventory graph (containers, occurrences, digests, extraction boundaries, decompression budgets, integrity contradictions, record-and-continue policy)

- **Source:** `reva-requirements.md:131-131` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-19; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-19 | Artifact inventory graph (containers, occurrences, digests, extraction boundaries, decompression budgets, integrity contradictions, record-and-continue policy) | `src/domain/artifactGraph.ts`, `artifactDecompressionBudget.ts`, `artifactIntegrityPolicy.ts`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-19' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-19') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-19

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-19 | Artifact inventory graph (containers, occurrences, digests, extraction boundaries, decompression budgets, integrity contradictions, record-and-continue policy) | src/domain/artifactGraph.ts, artifactDecompressionBudget.ts, artifactIntegrityPolicy.ts»
- [ ] Artifact inventory graph (containers, occurrences, digests, extraction boundaries, decompression budgets, integrity contradictions, record-and-continue policy)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-24 [P1] RC-24: Untrusted target content marking (meta.provenance.untrustedcontent) and prompt-injection discipline

- **Source:** `reva-requirements.md:136-136` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-24; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-24 | Untrusted target content marking (`_meta.provenance.untrusted_content`) and prompt-injection discipline | `docs/mcp-contracts.md` § Untrusted target content
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-24' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-24') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-24

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-24 | Untrusted target content marking (_meta.provenance.untrusted_content) and prompt-injection discipline | docs/mcp-contracts.md § Untrusted target content»
- [ ] Untrusted target content marking (_meta.provenance.untrusted_content) and prompt-injection discipline
- [ ] docs/mcp-contracts.md § Untrusted target content
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-26 [P1] RC-26: Known-answer agent evaluation (claims checked against delivered evidence: value, authority, confidence, subject, parameters, links)

- **Source:** `reva-requirements.md:138-138` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-26; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-26 | Known-answer agent evaluation (claims checked against delivered evidence: value, authority, confidence, subject, parameters, links) | `src/evaluation/KnownAnswerEvaluation.ts`, `AgentEvaluationReport.ts`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-26' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-26') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-26

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-26 | Known-answer agent evaluation (claims checked against delivered evidence: value, authority, confidence, subject, parameters, links) | src/evaluation/KnownAnswerEvaluation.ts, AgentEvaluationReport.ts»
- [ ] Known-answer agent evaluation (claims checked against delivered evidence: value, authority, confidence, subject, parameters, links)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AB-002 [P1] REVA-AB-002: Inbound HTTP routes — JS/TS: Express/Router (`app\ · router.<method>(path, …), .route(path).<method>()), Fastify (fastify.<method>, route({method,url})), Koa-router, NestJS (@Controller(base) + @Get/@

- **Source:** `reva-requirements.md:876-876` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AB-002 | **Inbound HTTP routes** — JS/TS: Express/Router (`app\|router.<method>(path, …)`, `.route(path).<method>()`), Fastify (`fastify.<method>`, `route({method,url})`), Koa-router, NestJS (`@Controller(base)` + `@Get/@Post/...(path)`), Next.js (`pages/api/**` files, `app/**/route.(ts\|js)` exported `GET/POST/...`). Java: Spring `@RestController`/`@Controller` with class-level `@RequestMapping` combined with method-level `@GetMapping/@PostMapping/@PutMapping/@DeleteMapping/@PatchMapping/@RequestMapping(method=…)`, `value`/`path` arrays, JAX-RS `@Path` + `@GET/...`. Python: FastAPI `@app\|router.<method>(path)` with `APIRouter(prefix=…)` and `include_router(prefix=…)` composition, Flask `@app\|bp.route(path, methods=[…])` with blueprint `url_prefix`, Django `path()/re_path()` in `urls.py` with `include()` prefixes. | Fixture repos per framework (authored for REVA) yield the exact expected route sets (golden files), including composed prefixes. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AB-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AB-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture repos per framework (authored for REVA) yield the exact expected route sets (golden files), including composed prefixes
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AB-010 [P1] REVA-AB-010: Electron specifics: BrowserWindow creation and webPreferences (contextIsolation, nodeIntegration, sandbox, preload path), preload discovery, exposed API members, renderer → preload → main IPC chains (

- **Source:** `reva-requirements.md:884-884` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AB-010 | **Electron specifics**: BrowserWindow creation and `webPreferences` (contextIsolation, nodeIntegration, sandbox, preload path), preload discovery, exposed API members, renderer → preload → main IPC chains (cf. E-01, E-03). | E-01 fixture reproduces the chain renderer→contextBridge→`invokes`→handler→channel and the endpoint call. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AB-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AB-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] E-01 fixture reproduces the chain renderer→contextBridge→invokes→handler→channel and the endpoint call
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AI-005 [P1] REVA-AI-005: Integrity: when a container declares member digests (JAR signature digests in META-INF/*.SF/MANIFEST.MF, wheel RECORD, npm integrity in lockfiles, OCI layer digests, ASAR integrity blocks), REVA verif

- **Source:** `reva-requirements.md:846-846` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AI-005 | Integrity: when a container declares member digests (JAR signature digests in `META-INF/*.SF`/`MANIFEST.MF`, wheel `RECORD`, npm `integrity` in lockfiles, OCI layer digests, ASAR integrity blocks), REVA verifies them and creates `integrity_mismatch` contradictions on mismatch, honouring the integrity policy (REVA-CX-005). | Fixtures with one tampered member for each declaring format raise exactly one contradiction each. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AI-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AI-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixtures with one tampered member for each declaring format raise exactly one contradiction each
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AS-004 [P1] REVA-AS-004: Templating, highest authority first: (1) OpenAPI/AsyncAPI specs ingested in KGF for that origin → exact template (observed for the match, source_system_record for the template); (2) OTel http.route → 

- **Source:** `reva-requirements.md:900-900` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AS-004 | Templating, highest authority first: (1) OpenAPI/AsyncAPI specs ingested in KGF for that origin → exact template (`observed` for the match, `source_system_record` for the template); (2) OTel `http.route` → template as observed; (3) value-class rules per segment (integer, UUID, hex ≥ 8, ISO date, ULID, email, base64url ≥ 16); (4) cardinality inference: in a segment trie per `(method, origin)`, a position becomes `{param}` when ≥ `K` (default 3) distinct sibling values share the same prefix and suffix structure and each value's request volume share is < 50%. Each template records its basis and confidence. | E-07 regression: the three `svc-*` rotate calls collapse into `/api/v2/service-accounts/{param}/rotate` (basis `cardinality`); an OpenAPI fixture overrides with the named parameter `{accountId}`. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AS-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AS-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] E-07 regression: the three svc- rotate calls collapse into /api/v2/service-accounts/{param}/rotate (basis cardinality); an OpenAPI fixture overrides with the named parameter {accountId}
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-BD-005 [P1] REVA-BD-005: Binary change impact propagation warrant. Traverses KGF knowledge graph from mutated binary functions to higher-level API routes, background jobs, and user-facing features; emits signed impact warrant

- **Source:** `reva-requirements.md:1174-1174` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-BD-005 | Binary change impact propagation warrant. Traverses KGF knowledge graph from mutated binary functions to higher-level API routes, background jobs, and user-facing features; emits signed impact warrant citing changed function digests. | Trace from changed native function resolves impacted HTTP boundaries and Jira stories; generates comprehensive binary impact diff report. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-BD-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-BD-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Trace from changed native function resolves impacted HTTP boundaries and Jira stories; generates comprehensive binary impact diff report
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-CX-002 [P1] REVA-CX-002: Integrity contradictions: declared digest ≠ observed digest (archives, manifests, SBOM entries, commit claims) create integrity_mismatch. · Fixture with a tampered JAR member produces an integrity con

- **Source:** `reva-requirements.md:734-734` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-CX-002 | Integrity contradictions: declared digest ≠ observed digest (archives, manifests, SBOM entries, commit claims) create `integrity_mismatch`. | Fixture with a tampered JAR member produces an integrity contradiction; the member is quarantined from nested expansion. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-CX-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-CX-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture with a tampered JAR member produces an integrity contradiction; the member is quarantined from nested expansion
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-CX-003 [P1] REVA-CX-003: Resolution rules, in order of configuration: valid_time_split (both true in different intervals) → authority_precedence (configurable per predicate, default: human_attested > controlled_execution > ru

- **Source:** `reva-requirements.md:735-735` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-CX-003 | Resolution rules, in order of configuration: `valid_time_split` (both true in different intervals) → `authority_precedence` (configurable per predicate, default: `human_attested > controlled_execution > runtime_observed > source_system_record > shipped_artifact > source_code_static > rule_derived > historical_reference > model_inferred`) → `recency` (only if enabled for the predicate) → `human_decision`. Automatic rules never discard members; they mark a winner and keep all members visible. | Each rule has a fixture; resolution is recorded as a decision warrant. | component
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-CX-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-CX-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Each rule has a fixture; resolution is recorded as a decision warrant
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-DB-002 [P1] REVA-DB-002: PostgreSQL, MySQL/MariaDB, SQL Server and Oracle via SQLAlchemy 2.x inspector: schemas, tables, columns (type, nullable, default), PKs, FKs, unique constraints, indexes, views (+ definition where the 

- **Source:** `reva-requirements.md:913-913` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-DB-002 | PostgreSQL, MySQL/MariaDB, SQL Server and Oracle via SQLAlchemy 2.x inspector: schemas, tables, columns (type, nullable, default), PKs, FKs, unique constraints, indexes, views (+ definition where the dialect exposes it), comments; optional row-count estimates from catalog statistics. Connections use KGF-stored credentials and are verified read-only before introspection (`SET TRANSACTION READ ONLY` / equivalent; refuse when the role can write, unless `REVA_DB_ALLOW_WRITABLE_ROLE=true`). | Integration tests against PostgreSQL and MySQL containers in CI; SQL Server and Oracle via optional CI lane (named skip when unavailable). | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-DB-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-DB-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Integration tests against PostgreSQL and MySQL containers in CI; SQL Server and Oracle via optional CI lane (named skip when unavailable)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-DB-003 [P1] REVA-DB-003: Row sampling is disabled by default. When enabled per connection by tenant policy, sample ≤ REVA_DB_SAMPLE_ROWS (default 20) rows per table with PII masking (column-name heuristics + classification ru

- **Source:** `reva-requirements.md:914-914` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-DB-003 | Row sampling is disabled by default. When enabled per connection by tenant policy, sample ≤ `REVA_DB_SAMPLE_ROWS` (default 20) rows per table with PII masking (column-name heuristics + classification rules); samples are stored as restricted blobs. | Sampling off: no `SELECT` on user tables appears in the DB audit log of the test container. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-DB-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-DB-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Sampling off: no SELECT on user tables appears in the DB audit log of the test container
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-DI-002 [P1] REVA-DI-002: Containerized ephemeral debugger bridge. Spawns GDB/MI2 or LLDB in an ephemeral Linux container with drop-all Linux capabilities (--cap-drop=ALL, --security-opt=no-new-privileges:true), private PID na

- **Source:** `reva-requirements.md:1137-1137` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-DI-002 | Containerized ephemeral debugger bridge. Spawns GDB/MI2 or LLDB in an ephemeral Linux container with drop-all Linux capabilities (`--cap-drop=ALL`, `--security-opt=no-new-privileges:true`), private PID namespace, `network: "none"`, and strict CPU/memory rlimits. | Controller establishes MI2 protocol communication with debugger; enforces automatic container termination upon session completion or timeout. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-DI-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-DI-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Controller establishes MI2 protocol communication with debugger; enforces automatic container termination upon session completion or timeout
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-DR-001 [P1] REVA-DR-001: `kgf reva doctor [--json] [--scope all\ · kernel\ · sandbox\

- **Source:** `reva-requirements.md:1015-1015` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-DR-001 | `kgf reva doctor [--json] [--scope all\|kernel\|sandbox\|graph\|extractors\|connectors\|models]` checks: Python version; REVA migrations applied; relational store connectivity and write test; blob store writable with free space ≥ `REVA_MIN_FREE_GB`; KEK present; producer and log keys present, decryptable, file mode 0600; latest STH verifies and log consistency since the last audit; graph backend reachable with a capability probe per backend (traversal, property filters, batch writes, transactions); tree-sitter grammars load; sandbox capabilities (namespaces, cgroup v2, docker/podman availability, prlimit); git available; connectors healthy (SourcePort); LLMPort local model reachable when GA synthesis is enabled; clock skew vs NTP reference (if reachable, else unknown); feature flags state. | Each check has pass/fail/unknown fixtures; JSON output validates against its schema. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-DR-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-DR-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Each check has pass/fail/unknown fixtures; JSON output validates against its schema
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-DR-002 [P1] REVA-DR-002: Each finding: `{check_id, status: pass\ · fail\ · warn\

- **Source:** `reva-requirements.md:1016-1016` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-DR-002 | Each finding: `{check_id, status: pass\|fail\|warn\|unknown, category: environment\|configuration\|integrity\|capability, message, remediation, evidence}`. Exit code 0 only if no `fail`. | Exit code tests. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-DR-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-DR-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-DR-002 | Each finding: `{check_id, status: pass\ | fail\ | warn\ | unknown, category: environment\ | configuration\ | integrity\ | capability, message, remediation, evidence}. Exit code 0 only if no fail`. | Exit code tests. | integration»
- [ ] Each finding: `{check_id, status: pass\
- [ ] capability, message, remediation, evidence}. Exit code 0 only if no fail`.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-DV-002 [P1] REVA-DV-002: Checks (each a warrant): (a) embedded revision equals expected (SP-010); (b) not dirty (SP-011); (c) JS bundles: source-map sourcesContent digests equal the repo files at the commit (per file, with co

- **Source:** `reva-requirements.md:964-964` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-DV-002 | Checks (each a warrant): (a) embedded revision equals expected (SP-010); (b) not dirty (SP-011); (c) **JS bundles**: source-map `sourcesContent` digests equal the repo files at the commit (per file, with coverage); (d) **JVM**: class list/packages in the JAR equal the compiled output of the commit when a CI build artifact for that commit is registered in KGF; otherwise `unknown` with gap `GAP_NO_REFERENCE_BUILD`; (e) **Python/npm**: RECORD/lockfile digests equal the commit's lockfile resolution; (f) **reproducible-build mode** (optional): if a build recipe is registered (`reva-build.yaml`), rebuild in the sandbox and compare digests. | Fixture matrix covers match, mismatch and unknown for each check. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-DV-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-DV-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture matrix covers match, mismatch and unknown for each check
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-DV-003 [P1] REVA-DV-003: Verdict: verified_match (all applicable checks pass at observed authority), mismatch (any check fails → contradiction), unverifiable_dirty, unknown (insufficient evidence; gaps created). Never verifie

- **Source:** `reva-requirements.md:965-965` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-DV-003 | Verdict: `verified_match` (all applicable checks pass at observed authority), `mismatch` (any check fails → contradiction), `unverifiable_dirty`, `unknown` (insufficient evidence; gaps created). Never `verified_match` from revision labels alone; labels give at most `claimed_match`. | Verdict table tests. | unit
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-DV-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-DV-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-DV-003 | Verdict: verified_match (all applicable checks pass at observed authority), mismatch (any check fails → contradiction), unverifiable_dirty, unknown (insufficient evidence; gaps created). Never verified_match from revision labels alone; labels give at most claimed_match. | Verdict table tests. | unit»
- [ ] Verdict: verified_match (all applicable checks pass at observed authority), mismatch (any check fails → contradiction), unverifiable_dirty, unknown (insufficient evidence; gaps created). Never verified_match from revision labels alone; labels give at most claimed_match.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-FM-004 [P1] REVA-FM-004: WASM & EVM bytecode decoder. Parses WebAssembly module sections (type, import, function, table, memory, export, code, custom), validates section offsets, and decodes instruction opcodes; parses EVM by

- **Source:** `reva-requirements.md:1122-1122` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-FM-004 | WASM & EVM bytecode decoder. Parses WebAssembly module sections (type, import, function, table, memory, export, code, custom), validates section offsets, and decodes instruction opcodes; parses EVM bytecode contract selectors and function dispatchers. | Emits structured WASM and EVM interface inventories with function signatures and exported methods; verifies pure-Python decoding without running VM. | unit
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-FM-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-FM-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Emits structured WASM and EVM interface inventories with function signatures and exported methods; verifies pure-Python decoding without running VM
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-FM-005 [P1] REVA-FM-005: Firmware artifact warrant bundle generation. Computes Merkle tree of all carved partitions, filesystems, and embedded binaries; issues signed warrant bundle binding master firmware image digest to all

- **Source:** `reva-requirements.md:1123-1123` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-FM-005 | Firmware artifact warrant bundle generation. Computes Merkle tree of all carved partitions, filesystems, and embedded binaries; issues signed warrant bundle binding master firmware image digest to all child artifact warrants. | Generates valid warrant bundle with inclusion proofs; proves full provenance from root firmware image to individual configuration files. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-FM-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-FM-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Generates valid warrant bundle with inclusion proofs; proves full provenance from root firmware image to individual configuration files
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-FT-003 [P1] REVA-FT-003: Bounds: max_depth (default 6), max_frontier (default 5,000 nodes per hop), max_paths (default 200 returned; all counted). Hitting a bound records it in coverage and lists the unexpanded frontier with 

- **Source:** `reva-requirements.md:937-937` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-FT-003 | Bounds: `max_depth` (default 6), `max_frontier` (default 5,000 nodes per hop), `max_paths` (default 200 returned; all counted). Hitting a bound records it in coverage and lists the unexpanded frontier with reasons (`DEPTH_LIMIT`, `FRONTIER_LIMIT`, `ACL_HIDDEN`, `EDGE_COVERAGE_UNKNOWN`). | A deep fixture reports exact frontier counts; ACL-hidden nodes are counted but never named. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-FT-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-FT-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] A deep fixture reports exact frontier counts; ACL-hidden nodes are counted but never named
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-FT-004 [P1] REVA-FT-004: Path strength: per edge (authority, epistemic, confidence_bp) from the edge's warrant summary; path epistemic = weakest; path confidence = product of edge confidences (bp arithmetic, floor); path auth

- **Source:** `reva-requirements.md:938-938` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-FT-004 | Path strength: per edge `(authority, epistemic, confidence_bp)` from the edge's warrant summary; path epistemic = weakest; path confidence = product of edge confidences (bp arithmetic, floor); path authority set = union. `contains_inference = true` if any edge is inferred. Results sort by confidence desc, then length asc. | Golden ordering on fixture. | unit
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-FT-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-FT-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Golden ordering on fixture
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-GA-002 [P1] REVA-GA-002: Deterministic-first: when a question matches a trace template or typed query, the answer is built deterministically from workflow results (no LLM). LLM synthesis is used only to phrase or to answer no

- **Source:** `reva-requirements.md:1002-1002` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-GA-002 | Deterministic-first: when a question matches a trace template or typed query, the answer is built deterministically from workflow results (no LLM). LLM synthesis is used only to phrase or to answer non-template questions, and only through KGF's LLMPort under the egress policy (C-02). | Template questions produce `mode=deterministic` with zero LLM calls (call counter). | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-GA-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-GA-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Template questions produce mode=deterministic with zero LLM calls (call counter)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

