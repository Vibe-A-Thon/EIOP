# EPIC-REVA-NOTEST-01: reva-requirements.md · code_no_test

*Code references the ID but no test is mapped.* 60 tasks, ~150.0 h, priorities {'P0': 11, 'P1': 24, 'P2': 25}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-REVA-AS-003 [P0] REVA-AS-003: Redaction (before anything is stored): remove values of Authorization, Proxy-Authorization, Cookie, Set-Cookie, X-Api-Key, X-Auth-Token and configurable headers; query parameters whose names match `(?

- **Source:** `reva-requirements.md:899-899` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AS-003 | Redaction (before anything is stored): remove values of `Authorization`, `Proxy-Authorization`, `Cookie`, `Set-Cookie`, `X-Api-Key`, `X-Auth-Token` and configurable headers; query parameters whose names match `(?i)(token\|secret\|password\|passwd\|pwd\|key\|sig\|signature\|code\|session\|auth)`; any value matching JWT, AWS access key, private-key PEM or generic high-entropy (≥ 4.0 bits/char over ≥ 32 chars) patterns. Bodies are **not** stored by default; only JSON key-shape summaries are kept. Every redaction is recorded with an RFC 6901 pointer and a reason. | Fixture with secrets in headers, query, body and URL path: no secret value appears in any warrant, blob, log or projection (byte search over the whole data volume). | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/core/redact.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-AS-003') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Fixture with secrets in headers, query, body and URL path: no secret value appears in any warrant, blob, log or projection (byte search over the whole data volume)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/core/redact.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/core/redact.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-DI-001 [P0] REVA-DI-001: Enterprise dual-key cryptographic authorization protocol. Dynamic execution of any target binary or debugger requires an authorization token signed by both an authenticated analyst and an authorized t

- **Source:** `reva-requirements.md:1136-1136` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-DI-001 | Enterprise dual-key cryptographic authorization protocol. Dynamic execution of any target binary or debugger requires an authorization token signed by both an authenticated analyst and an authorized tenant security administrator (`Authority.CONTROLLED_EXECUTION`). | Controlled execution rejects single-signature or unsigned requests with `REVA_ERR_UNAUTHORIZED_EXECUTION`; validates dual Ed25519 signatures before spawning any process. | component
```
</details>

**Next steps**
1. Read the referenced code: reva/dynamic/auth_gate.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-DI-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Controlled execution rejects single-signature or unsigned requests with REVAERRUNAUTHORIZEDEXECUTION; validates dual Ed25519 signatures before spawning any process
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/dynamic/auth_gate.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/dynamic/auth_gate.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-FM-003 [P0] REVA-FM-003: Embedded configuration, key, and credential harvester. Scans carved filesystems for private keys (RSA, ECC, OpenSSH), X.509 certificates, hardcoded passwords, default credentials, API tokens, and /etc

- **Source:** `reva-requirements.md:1121-1121` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-FM-003 | Embedded configuration, key, and credential harvester. Scans carved filesystems for private keys (RSA, ECC, OpenSSH), X.509 certificates, hardcoded passwords, default credentials, API tokens, and `/etc/shadow` entries. | Discovers embedded certificates and keys; redacts sensitive secrets in public output; projects `reva_Resource(secret)` with SHA-256 fingerprint warrants. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/extract/firmware/wasm_decoder.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-FM-003') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Discovers embedded certificates and keys; redacts sensitive secrets in public output; projects revaResource(secret) with SHA-256 fingerprint warrants
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/firmware/wasm_decoder.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/firmware/wasm_decoder.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-RO-002 [P0] REVA-RO-002: CDP network capture with real-time RFC 6901 PII & credential redaction. Hooks Network.requestWillBeSent and Network.responseReceived; streams HTTP requests/responses into structured HAR; automatically

- **Source:** `reva-requirements.md:1154-1154` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-RO-002 | CDP network capture with real-time RFC 6901 PII & credential redaction. Hooks `Network.requestWillBeSent` and `Network.responseReceived`; streams HTTP requests/responses into structured HAR; automatically redacts cookies, Authorization headers, tokens, and PII. | Captures network exchanges; verifies all Authorization headers and session cookies are replaced with `[REDACTED]`; no plaintext credentials stored in warrants. | component
```
</details>

**Next steps**
1. Read the referenced code: reva/obs/dom_harvester.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-RO-002') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Captures network exchanges; verifies all Authorization headers and session cookies are replaced with [REDACTED]; no plaintext credentials stored in warrants
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/obs/dom_harvester.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/obs/dom_harvester.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SEC-001 [P0] REVA-SEC-001: Tenant scoping: every REVA table has tenant_id; every query filters by the authenticated tenant at the data-access layer (repository base class), never only in routers. Blob paths include the tenant n

- **Source:** `reva-requirements.md:1022-1022` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SEC-001 | Tenant scoping: every REVA table has `tenant_id`; every query filters by the authenticated tenant at the data-access layer (repository base class), never only in routers. Blob paths include the tenant namespace; signing keys are per tenant. | Cross-tenant test suite: every endpoint and tool is called with tenant A credentials against tenant B IDs → 404, and nothing leaks in errors, timings beyond noise, or counts. | acceptance
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/store.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-SEC-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Cross-tenant test suite: every endpoint and tool is called with tenant A credentials against tenant B IDs → 404, and nothing leaks in errors, timings beyond noise, or counts
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/store.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/store.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SEC-002 [P0] REVA-SEC-002: ACL inheritance: source-record warrants carry source_acl_refs from connectors (e.g. Confluence space permissions, Jira project roles, Git repo access). Effective visibility = source ACL ∩ envelope all

- **Source:** `reva-requirements.md:1023-1023` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SEC-002 | ACL inheritance: source-record warrants carry `source_acl_refs` from connectors (e.g. Confluence space permissions, Jira project roles, Git repo access). Effective visibility = source ACL ∩ envelope allow − deny. Derived warrants and workflow results inherit the **intersection** of the ACLs of all inputs (most restrictive). | A trace combining a restricted Confluence fact with public code facts is invisible to a user without Confluence access, and the trace reports `ACL_HIDDEN` frontier counts to users who lack access. | acceptance
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/acl.py:1, reva/kernel/query.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-SEC-002') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] A trace combining a restricted Confluence fact with public code facts is invisible to a user without Confluence access, and the trace reports ACLHIDDEN frontier counts to users who lack access
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/acl.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/acl.py#L1-L1), [`reva/kernel/query.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/query.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SEC-005 [P0] REVA-SEC-005: Redaction library shared by AS, VS (logs), MC (errors) and exports (§7.11 REVA-AS-003 patterns + configurable). · Secret-scan test over all REVA outputs in the acceptance run finds nothing. · acceptan

- **Source:** `reva-requirements.md:1026-1026` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SEC-005 | Redaction library shared by AS, VS (logs), MC (errors) and exports (§7.11 REVA-AS-003 patterns + configurable). | Secret-scan test over all REVA outputs in the acceptance run finds nothing. | acceptance
```
</details>

**Next steps**
1. Read the referenced code: reva/core/redact.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-SEC-005') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Secret-scan test over all REVA outputs in the acceptance run finds nothing
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/core/redact.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/core/redact.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SEC-007 [P0] REVA-SEC-007: Keys: KEK-encrypted private keys; rotation and revocation (REVA-WK-010); public keys exportable; no private key ever in logs, errors, bundles or API responses. · Log and response scans in tests. · int

- **Source:** `reva-requirements.md:1028-1028` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SEC-007 | Keys: KEK-encrypted private keys; rotation and revocation (REVA-WK-010); public keys exportable; no private key ever in logs, errors, bundles or API responses. | Log and response scans in tests. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/keys.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-SEC-007') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Log and response scans in tests
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/keys.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/keys.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-VS-005 [P0] REVA-VS-005: Environment hygiene: only env_allow variables pass through; secrets are never injected unless an obligation explicitly requires a named secret from the KGF secret store; HOME and TMP point into the ru

- **Source:** `reva-requirements.md:829-829` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-VS-005 | Environment hygiene: only `env_allow` variables pass through; secrets are never injected unless an obligation explicitly requires a named secret from the KGF secret store; HOME and TMP point into the run root. | Env dump fixture shows only allowed variables. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/sandbox/runner.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-VS-005') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Env dump fixture shows only allowed variables
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/sandbox/runner.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/sandbox/runner.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-WK-009 [P0] REVA-WK-009: Retrieval by ID, by subject, by predicate, by producer, by link (in/out), by time window, with ACL filtering (§7.21) and paging (§7.17). IDs and signatures are verified on every read. A failed verific

- **Source:** `reva-requirements.md:680-680` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-WK-009 | Retrieval by ID, by subject, by predicate, by producer, by link (in/out), by time window, with ACL filtering (§7.21) and paging (§7.17). IDs and signatures are verified on every read. A failed verification raises `REVA_E_INTEGRITY` and quarantines the record. | Corrupting one stored byte makes the read fail and records a `reva.pred.integrity_violation` warrant; unauthorized principals receive 404 (not 403) to avoid existence leaks. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/core/errors.py:1, reva/kernel/query.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-WK-009') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Corrupting one stored byte makes the read fail and records a reva.pred.integrityviolation warrant; unauthorized principals receive 404 (not 403) to avoid existence leaks
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/core/errors.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/core/errors.py#L1-L1), [`reva/kernel/query.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/query.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-WK-010 [P0] REVA-WK-010: Signing: each producer has ≥ 1 Ed25519 key (key1_ ID). Private keys are encrypted at rest with a KEK (REVA_KEK from the KGF secret store or env) using AES-256-GCM. Support rotation (new key active, ol

- **Source:** `reva-requirements.md:681-681` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-WK-010 | Signing: each producer has ≥ 1 Ed25519 key (`key1_` ID). Private keys are encrypted at rest with a KEK (`REVA_KEK` from the KGF secret store or env) using AES-256-GCM. Support rotation (new key active, old key verify-only) and revocation (revoked keys fail verification for warrants recorded after `revoked_at`). | Rotation test: warrants by old and new keys both verify; revocation test: a warrant recorded after revocation fails; private key files are never readable by other OS users (0600) and never logged. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/keys.py:1, reva/kernel/signing.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-WK-010') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Rotation test: warrants by old and new keys both verify; revocation test: a warrant recorded after revocation fails; private key files are never readable by other OS users (0600) and never logged
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/keys.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/keys.py#L1-L1), [`reva/kernel/signing.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/signing.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-C-03 [P1] C-03: Multi-backend graph neutrality. REVA writes to the authoritative graph only through KGF's graph abstraction / governed mutation gateway. It must work with HugeGraph, Neo4j and Neptune, and declare per

- **Source:** `reva-requirements.md:273-273` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
C-03 | **Multi-backend graph neutrality.** REVA writes to the authoritative graph only through KGF's graph abstraction / governed mutation gateway. It must work with HugeGraph, Neo4j and Neptune, and declare per-backend capability gaps rather than silently degrading.
```
</details>

**Next steps**
1. Read the referenced code: reva/graph/ontology.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('C-03') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «C-03 | Multi-backend graph neutrality. REVA writes to the authoritative graph only through KGF's graph abstraction / governed mutation gateway. It must work with HugeGraph, Neo4j and Neptune, and declare per-backend capability gaps rather than silently degrading.»
- [ ] Multi-backend graph neutrality. REVA writes to the authoritative graph only through KGF's graph abstraction / governed mutation gateway. It must work with HugeGraph, Neo4j and Neptune, and declare per-backend capability gaps rather than silently degrading.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/graph/ontology.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/graph/ontology.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-BD-004 [P1] REVA-BD-004: Binary symbol and export delta engine. Detects added, removed, and modified functions, exported APIs, and symbol table entries; classifies breaking changes (removed exports, signature alterations). · 

- **Source:** `reva-requirements.md:1173-1173` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-BD-004 | Binary symbol and export delta engine. Detects added, removed, and modified functions, exported APIs, and symbol table entries; classifies breaking changes (removed exports, signature alterations). | Outputs structured delta containing `added`, `removed`, `modified`, and `renamed` functions; verifies breaking API removals are flagged with high severity. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/diff/impact_classifier.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-BD-004') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Outputs structured delta containing added, removed, modified, and renamed functions; verifies breaking API removals are flagged with high severity
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/diff/impact_classifier.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/diff/impact_classifier.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-CV-002 [P1] REVA-CV-002: Every REVA workflow and extractor returning a set MUST attach Coverage. A static check in CI fails if a registered predicate with requires_coverage=True is issued without coverage. · CI check reva-lin

- **Source:** `reva-requirements.md:707-707` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-CV-002 | Every REVA workflow and extractor returning a set MUST attach Coverage. A static check in CI fails if a registered predicate with `requires_coverage=True` is issued without coverage. | CI check `reva-lint coverage` passes; a deliberately broken extractor fails it. | static
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/gaps.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-CV-002') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] CI check reva-lint coverage passes; a deliberately broken extractor fails it
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/gaps.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/gaps.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-FM-001 [P1] REVA-FM-001: Multi-format firmware header parser and signature carver. Detects and parses headers for SquashFS, CramFS, JFFS2, YAFFS2, Ext2/3/4, U-Boot images, Device Tree Blobs (DTB), and UEFI capsule containers.

- **Source:** `reva-requirements.md:1119-1119` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-FM-001 | Multi-format firmware header parser and signature carver. Detects and parses headers for SquashFS, CramFS, JFFS2, YAFFS2, Ext2/3/4, U-Boot images, Device Tree Blobs (DTB), and UEFI capsule containers. | Detects and extracts file systems from raw flash dump fixtures; accurately calculates partition offsets, lengths, and magic bytes. | component
```
</details>

**Next steps**
1. Read the referenced code: reva/extract/firmware/carver.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-FM-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Detects and extracts file systems from raw flash dump fixtures; accurately calculates partition offsets, lengths, and magic bytes
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/firmware/carver.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/firmware/carver.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-FM-002 [P1] REVA-FM-002: Sandboxed carving pipeline with recursion and decompression limits. Enforces strict maximum recursion depth ($\le 6$), maximum decompression ratio ($200:1$), and overall size budget ($10\text{ GiB}$) 

- **Source:** `reva-requirements.md:1120-1120` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-FM-002 | Sandboxed carving pipeline with recursion and decompression limits. Enforces strict maximum recursion depth ($\le 6$), maximum decompression ratio ($200:1$), and overall size budget ($10\text{ GiB}$) to prevent decompression bombs. | Recursively unpacks nested firmware images up to depth 6; halts safely when recursion depth or quota exceeded with `REVA_ERR_CARVE_LIMIT_EXCEEDED` and issues limitation warrant. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/extract/firmware/secret_harvester.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-FM-002') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Recursively unpacks nested firmware images up to depth 6; halts safely when recursion depth or quota exceeded with REVAERRCARVELIMITEXCEEDED and issues limitation warrant
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/firmware/secret_harvester.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/firmware/secret_harvester.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-MB-002 [P1] REVA-MB-002: DEX / Multi-DEX bytecode parser. Parses DEX headers, class definitions, method prototypes, annotations, and string tables across classes.dex, classes2.dex, etc., without running Dalvik VM. · Ingests m

- **Source:** `reva-requirements.md:1102-1102` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-MB-002 | DEX / Multi-DEX bytecode parser. Parses DEX headers, class definitions, method prototypes, annotations, and string tables across `classes.dex`, `classes2.dex`, etc., without running Dalvik VM. | Ingests multi-DEX APKs; indexes all class names, method names, and method signatures; extracts hardcoded string literals and backend API URLs. | component
```
</details>

**Next steps**
1. Read the referenced code: reva/extract/mobile/dex_parser.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-MB-002') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Ingests multi-DEX APKs; indexes all class names, method names, and method signatures; extracts hardcoded string literals and backend API URLs
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/mobile/dex_parser.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/mobile/dex_parser.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NB-001 [P1] REVA-NB-001: Multi-format binary loader (ELF, PE32/PE32+, Mach-O, Fat Mach-O, COFF) with architecture detection (x86_64, aarch64, armv7, riscv64). Parse file headers, section tables, segment permissions (R, W, X),

- **Source:** `reva-requirements.md:1081-1081` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NB-001 | Multi-format binary loader (ELF, PE32/PE32+, Mach-O, Fat Mach-O, COFF) with architecture detection (x86_64, aarch64, armv7, riscv64). Parse file headers, section tables, segment permissions (`R`, `W`, `X`), entry points, and image base addresses. | Fixtures for ELF (Linux), PE (Windows), and Mach-O (macOS x86_64 and arm64 universal) are parsed correctly; executable segments and section headers match ground truth without executing untrusted code on the host. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/extract/native/loader.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-NB-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Fixtures for ELF (Linux), PE (Windows), and Mach-O (macOS x8664 and arm64 universal) are parsed correctly; executable segments and section headers match ground truth without executing untrusted code on the host
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/native/loader.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/native/loader.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NB-002 [P1] REVA-NB-002: Sandboxed headless disassembler engine using Capstone/Keystone and Radare2/Rizin worker under strict rlimits (CPU $\le 600\text{s}$, RAM $\le 4\text{ GiB}$, network: "none"). Disassembles target funct

- **Source:** `reva-requirements.md:1082-1082` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NB-002 | Sandboxed headless disassembler engine using Capstone/Keystone and Radare2/Rizin worker under strict rlimits (CPU $\le 600\text{s}$, RAM $\le 4\text{ GiB}$, `network: "none"`). Disassembles target functions into instruction streams (mnemonic, operands, instruction size, prefix, jump target). | Disassembly of standard test functions produces instruction streams matching reference objdump; timeout and memory limit violations terminate worker safely with `REVA_ERR_SANDBOX_TIMEOUT` and issue a warrant limitation. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/extract/native/disasm.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-NB-002') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Disassembly of standard test functions produces instruction streams matching reference objdump; timeout and memory limit violations terminate worker safely with REVAERRSANDBOXTIMEOUT and issue a warrant limitation
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/native/disasm.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/native/disasm.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-PD-002 [P1] REVA-PD-002: Owner digest per §7.6.3 for Python, TypeScript/TSX, JavaScript and Java; whole-file mode for others. · Golden digests for fixture symbols; reformatting trailing whitespace does not change the digest; 

- **Source:** `reva-requirements.md:785-785` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-PD-002 | Owner digest per §7.6.3 for Python, TypeScript/TSX, JavaScript and Java; whole-file mode for others. | Golden digests for fixture symbols; reformatting trailing whitespace does not change the digest; changing one token does. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/pd/owner_digest.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-PD-002') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Golden digests for fixture symbols; reformatting trailing whitespace does not change the digest; changing one token does
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/pd/owner_digest.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/pd/owner_digest.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-PD-003 [P1] REVA-PD-003: Closure evaluation (deterministic, pure function) with these ordered checks, each producing reason codes (§10.6): (1) obligation active and reviewed; (2) dependencies closed; (3) no blocking gap open;

- **Source:** `reva-requirements.md:786-786` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-PD-003 | Closure evaluation (deterministic, pure function) with these ordered checks, each producing reason codes (§10.6): (1) obligation active and reviewed; (2) dependencies closed; (3) no blocking gap open; (4) no open contradiction on linked warrants; (5) binding valid, owners resolvable, owner digests current; (6) ≥ 1 verifier run for the binding's verifier at the current commit, with a valid attestation; (7) run depth ≥ required depth and authority acceptable (§6.7); (8) anti-gaming checks AG-01…AG-14 (REVA-PD-004) pass; (9) every required case kind has ≥ 1 passing test tagged with it; (10) nondeterminism and performance budgets satisfied; (11) for acceptance-depth obligations, each listed journey has a passing journey run with runtime artifacts. Outcome ∈ `closed, open, failed, blocked, stale, flaky, unknown`. | Table-driven tests: one fixture per reason code; outcome is never `closed` if any check is non-pass; `unknown`/`truncated`/`skipped` never aggregate to `closed`. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/pd/closure.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-PD-003') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Table-driven tests: one fixture per reason code; outcome is never closed if any check is non-pass; unknown/truncated/skipped never aggregate to closed
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/pd/closure.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/pd/closure.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-PD-005 [P1] REVA-PD-005: Mutation probe (REVA's own implementation for Python): AST mutation operators restricted to owner spans: comparison operator swap (<↔<=, ==↔!=), boolean operator swap, not insertion/removal, arithmeti

- **Source:** `reva-requirements.md:788-788` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-PD-005 | **Mutation probe** (REVA's own implementation for Python): AST mutation operators restricted to owner spans: comparison operator swap (`<`↔`<=`, `==`↔`!=`), boolean operator swap, `not` insertion/removal, arithmetic operator swap, numeric constant ±1, string constant replacement, `return X` → `return None`, removal of a call statement, `if` condition forced True/False. Each mutant runs only the obligation's tests in the sandbox with a per-mutant timeout; equivalent mutants surviving can be suppressed only by a human-attested waiver warrant. | On a fixture module with a strong and a weak test suite, the strong suite reaches ≥ 0.9 and the weak one ≤ 0.4; results are deterministic for a fixed seed. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/pd/mutation.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-PD-005') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] On a fixture module with a strong and a weak test suite, the strong suite reaches ≥ 0.9 and the weak one ≤ 0.4; results are deterministic for a fixed seed
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/pd/mutation.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/pd/mutation.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-PD-006 [P1] REVA-PD-006: Ledger generation for a scope: the canonical set of closure decisions, summary counts by outcome, complete = (all required obligations closed), ldg1_ ID, signed by the tenant PD key and logged. · Re-r

- **Source:** `reva-requirements.md:789-789` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-PD-006 | Ledger generation for a scope: the canonical set of closure decisions, summary counts by outcome, `complete = (all required obligations closed)`, `ldg1_` ID, signed by the tenant PD key and logged. | Re-running on unchanged inputs yields the identical ledger ID; changing one owner line flips the affected obligation to `stale`. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/pd/ledger.py:1, scripts/reva/build_reva_ledger.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-PD-006') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Re-running on unchanged inputs yields the identical ledger ID; changing one owner line flips the affected obligation to stale
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/pd/ledger.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/pd/ledger.py#L1-L1), [`scripts/reva/build_reva_ledger.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/reva/build_reva_ledger.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SEC-010 [P1] REVA-SEC-010: Export control: bundles and ledger exports exclude warrants the exporting principal cannot see, and restricted warrants unless the policy allows; exports are logged as warrants. · Export by a limited 

- **Source:** `reva-requirements.md:1031-1031` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SEC-010 | Export control: bundles and ledger exports exclude warrants the exporting principal cannot see, and `restricted` warrants unless the policy allows; exports are logged as warrants. | Export by a limited user omits restricted items. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/bundles.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-SEC-010') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Export by a limited user omits restricted items
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/bundles.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/bundles.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-TL-002 [P1] REVA-TL-002: Signed Tree Heads issued every REVA_STH_INTERVAL_S when the tree grew, and on demand; stored and served. · STH signatures verify with the tenant log public key; STHs are monotonic in tree_size. · comp

- **Source:** `reva-requirements.md:695-695` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-TL-002 | Signed Tree Heads issued every `REVA_STH_INTERVAL_S` when the tree grew, and on demand; stored and served. | STH signatures verify with the tenant log public key; STHs are monotonic in `tree_size`. | component
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/sth.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-TL-002') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] STH signatures verify with the tenant log public key; STHs are monotonic in treesize
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/sth.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/sth.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-TL-004 [P1] REVA-TL-004: Background auditor: re-verifies log consistency between the last audited STH and the current one, and verifies a random sample (REVA_AUDIT_SAMPLE, default 1%) of stored warrants against their leaves. 

- **Source:** `reva-requirements.md:697-697` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-TL-004 | Background auditor: re-verifies log consistency between the last audited STH and the current one, and verifies a random sample (`REVA_AUDIT_SAMPLE`, default 1%) of stored warrants against their leaves. Failures raise a critical alert and an integrity warrant. | Deleting a leaf row or editing a stored warrant is detected within one audit cycle. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/auditor.py:1, reva/kernel/sth.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-TL-004') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Deleting a leaf row or editing a stored warrant is detected within one audit cycle
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/auditor.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/auditor.py#L1-L1), [`reva/kernel/sth.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/sth.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-VS-003 [P1] REVA-VS-003: Resource limits per profile (defaults): CPU seconds 900, address space 4 GiB, file size 1 GiB, open files 4,096, processes 512, wall timeout 1,800 s; output capture capped at 16 MiB per stream, with o

- **Source:** `reva-requirements.md:827-827` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-VS-003 | Resource limits per profile (defaults): CPU seconds 900, address space 4 GiB, file size 1 GiB, open files 4,096, processes 512, wall timeout 1,800 s; output capture capped at 16 MiB per stream, with overflow recorded as truncation (never silently cut). | A fork bomb fixture is contained; an infinite-output fixture is truncated with a recorded limit. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/sandbox/limits.py:1, reva/sandbox/runner.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-VS-003') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] A fork bomb fixture is contained; an infinite-output fixture is truncated with a recorded limit
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/sandbox/limits.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/sandbox/limits.py#L1-L1), [`reva/sandbox/runner.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/sandbox/runner.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-VS-004 [P1] REVA-VS-004: Process lineage: new session and process group; descendants tracked by /proc polling (Linux) or psutil; on timeout or cancellation, the whole group receives SIGTERM, then SIGKILL after a 10 s grace; c

- **Source:** `reva-requirements.md:828-828` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-VS-004 | Process lineage: new session and process group; descendants tracked by `/proc` polling (Linux) or psutil; on timeout or cancellation, the whole group receives SIGTERM, then SIGKILL after a 10 s grace; cleanup outcome recorded. No REVA-owned process survives a run. | Orphan-detection test: after cancellation, no process with the run's pgid remains. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/sandbox/lineage.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-VS-004') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Orphan-detection test: after cancellation, no process with the run's pgid remains
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/sandbox/lineage.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/sandbox/lineage.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-VS-008 [P1] REVA-VS-008: Attestation creation and signing (§7.6.6); verification utility kgf reva verify-attestation <file>. · Tampering with any predicate field fails verification. · integration

- **Source:** `reva-requirements.md:832-832` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-VS-008 | Attestation creation and signing (§7.6.6); verification utility `kgf reva verify-attestation <file>`. | Tampering with any predicate field fails verification. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/sandbox/attest.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-VS-008') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Tampering with any predicate field fails verification
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/sandbox/attest.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/sandbox/attest.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-WK-003 [P1] REVA-WK-003: Implement Pydantic v2 models for the warrant body, envelope, Subject, Location, Coverage, Authority, epistemic state and confidence exactly as in §6.3–§6.6, strict and extra="forbid". · JSON Schema is

- **Source:** `reva-requirements.md:674-674` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-WK-003 | Implement Pydantic v2 models for the warrant body, envelope, Subject, Location, Coverage, Authority, epistemic state and confidence exactly as in §6.3–§6.6, strict and `extra="forbid"`. | JSON Schema is generated to `docs/reva/schemas/warrant.schema.json`; unknown fields are rejected; every enum value round-trips. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/warrant.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-WK-003') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] JSON Schema is generated to docs/reva/schemas/warrant.schema.json; unknown fields are rejected; every enum value round-trips
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/warrant.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/warrant.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-WK-007 [P1] REVA-WK-007: issue(draft) -> SealedWarrant: validate → normalize sets → store raw payload as blob → canonicalize body → compute ID → sign → persist (idempotent on ID) → append to transparency log → emit reva.warra

- **Source:** `reva-requirements.md:678-678` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-WK-007 | `issue(draft) -> SealedWarrant`: validate → normalize sets → store raw payload as blob → canonicalize body → compute ID → sign → persist (idempotent on ID) → append to transparency log → emit `reva.warrant.issued` event. The whole operation is atomic: no stored warrant without a log entry, and no log entry without a stored warrant. | Killing the process at each of 6 injected fault points leaves either nothing or a complete warrant+log entry (recovery job reconciles); re-issuing the same draft returns the same ID without duplicates. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/blobs.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-WK-007') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Killing the process at each of 6 injected fault points leaves either nothing or a complete warrant+log entry (recovery job reconciles); re-issuing the same draft returns the same ID without duplicates
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/blobs.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/blobs.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-WK-012 [P1] REVA-WK-012: Warrant bundles: export a set of warrants (plus their link closure to a configurable depth, required blobs, producer public keys, STH and inclusion proofs) as a .revabundle (zip with manifest.json, wa

- **Source:** `reva-requirements.md:683-683` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-WK-012 | Warrant bundles: export a set of warrants (plus their link closure to a configurable depth, required blobs, producer public keys, STH and inclusion proofs) as a `.revabundle` (zip with `manifest.json`, `warrants.jsonl`, `blobs/`, `keys.json`, `proofs.json`). Import verifies every ID, signature and inclusion proof before accepting anything (all-or-nothing). | Round-trip export/import into a second tenant preserves IDs; any tampered byte rejects the whole import with a precise error list; import never partially mutates state. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/bundles.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-WK-012') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Round-trip export/import into a second tenant preserves IDs; any tampered byte rejects the whole import with a precise error list; import never partially mutates state
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/bundles.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/bundles.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-WK-015 [P1] REVA-WK-015: Emit domain events (reva.warrant.issued, .superseded, .retracted, .integrity_violation) on the KGF event bus if present, else on REVA's internal outbox table, with at-least-once delivery and consumer 

- **Source:** `reva-requirements.md:686-686` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-WK-015 | Emit domain events (`reva.warrant.issued`, `.superseded`, `.retracted`, `.integrity_violation`) on the KGF event bus if present, else on REVA's internal outbox table, with at-least-once delivery and consumer idempotency keys = warrant ID. | Consumer receives every event exactly once after deduplication in a crash-restart test. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/events.py:1, reva/worker.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-WK-015') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Consumer receives every event exactly once after deduplication in a crash-restart test
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/events.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/events.py#L1-L1), [`reva/worker.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/worker.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RJ-01 [P1] RJ-01: Warrant lifecycle and tamper evidence. Ingest a Git repo and a Jira project with REVAINGESTWARRANTS=true; open a KGF entity; open its warrants in the WarrantDrawer; verify signature and inclusion proo

- **Source:** `reva-requirements.md:1410-1410` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RJ-01 | **Warrant lifecycle and tamper evidence.** Ingest a Git repo and a Jira project with `REVA_INGEST_WARRANTS=true`; open a KGF entity; open its warrants in the WarrantDrawer; verify signature and inclusion proof in the UI; corrupt one stored warrant row directly in the DB; run the auditor. | Warrants visible with correct authority/epistemic badges; proof verifies; corruption is detected within one audit cycle, the record is quarantined, and an alert and integrity warrant appear.
```
</details>

**Next steps**
1. Read the referenced code: scripts/reva/gen_ci.py:9
2. Write one test per acceptance criterion; mark with @pytest.mark.req('RJ-01') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RJ-01 | Warrant lifecycle and tamper evidence. Ingest a Git repo and a Jira project with REVA_INGEST_WARRANTS=true; open a KGF entity; open its warrants in the WarrantDrawer; verify signature and inclusion proof in the UI; corrupt one stored warrant row directly in the DB; run the auditor. | Warrants visible with correct authority/epistemic badges; proof verifies; corruption is»
- [ ] Warrant lifecycle and tamper evidence. Ingest a Git repo and a Jira project with REVA_INGEST_WARRANTS=true; open a KGF entity; open its warrants in the WarrantDrawer; verify signature and inclusion proof in the UI; corrupt one stored warrant row directly in the DB; run the auditor.
- [ ] Warrants visible with correct authority/epistemic badges; proof verifies; corruption is detected within one audit cycle, the record is quarantined, and an alert and integrity warrant appear.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/reva/gen_ci.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/reva/gen_ci.py#L9-L9)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RJ-12 [P1] RJ-12: Operations. Run doctor (all pass); rotate a producer key; back up; destroy the volume; restore; verify the log; reproject into an empty Neo4j; disable REVA and confirm KGF core still works

- **Source:** `reva-requirements.md:1421-1421` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RJ-12 | **Operations.** Run doctor (all pass); rotate a producer key; back up; destroy the volume; restore; verify the log; reproject into an empty Neo4j; disable REVA and confirm KGF core still works. | Every step passes; post-restore verification checks all IDs and log consistency; reprojection counts match; KGF core journeys pass with REVA disabled.
```
</details>

**Next steps**
1. Read the referenced code: scripts/reva/gen_ci.py:9
2. Write one test per acceptance criterion; mark with @pytest.mark.req('RJ-12') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RJ-12 | Operations. Run doctor (all pass); rotate a producer key; back up; destroy the volume; restore; verify the log; reproject into an empty Neo4j; disable REVA and confirm KGF core still works. | Every step passes; post-restore verification checks all IDs and log consistency; reprojection counts match; KGF core journeys pass with REVA disabled.»
- [ ] Operations. Run doctor (all pass); rotate a producer key; back up; destroy the volume; restore; verify the log; reproject into an empty Neo4j; disable REVA and confirm KGF core still works.
- [ ] Every step passes; post-restore verification checks all IDs and log consistency; reprojection counts match; KGF core journeys pass with REVA disabled.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/reva/gen_ci.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/reva/gen_ci.py#L9-L9)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-C-04 [P2] C-04: Governed mutation. Extractors and connectors produce warrants and proposed graph mutations. They never write directly to the graph

- **Source:** `reva-requirements.md:274-274` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
C-04 | **Governed mutation.** Extractors and connectors produce warrants and *proposed* graph mutations. They never write directly to the graph.
```
</details>

**Next steps**
1. Read the referenced code: reva/graph/ontology.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('C-04') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «C-04 | Governed mutation. Extractors and connectors produce warrants and proposed graph mutations. They never write directly to the graph.»
- [ ] Governed mutation. Extractors and connectors produce warrants and proposed graph mutations. They never write directly to the graph.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/graph/ontology.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/graph/ontology.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AB-001 [P2] REVA-AB-001: Parsing with tree-sitter (JavaScript, TypeScript, TSX, Java, Python). Parse errors are localized (error nodes counted per file); files with errors are still processed for unaffected subtrees, and cove

- **Source:** `reva-requirements.md:875-875` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AB-001 | Parsing with tree-sitter (JavaScript, TypeScript, TSX, Java, Python). Parse errors are localized (error nodes counted per file); files with errors are still processed for unaffected subtrees, and coverage records the error count. | Fixture with a syntax error in one function still yields boundaries from the rest, with a limitation. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/extract/boundaries/extractor.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-AB-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Fixture with a syntax error in one function still yields boundaries from the rest, with a limitation
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/boundaries/extractor.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/boundaries/extractor.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AB-008 [P2] REVA-AB-008: Logical identities: boundaries bnd:<service>/<kind>:<METHOD> <template> (or topic/channel/operation), resources res:<kind>:<canonical_name>; version identity = digest of the defining source span. Thes

- **Source:** `reva-requirements.md:882-882` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AB-008 | **Logical identities**: boundaries `bnd:<service>/<kind>:<METHOD> <template>` (or topic/channel/operation), resources `res:<kind>:<canonical_name>`; version identity = digest of the defining source span. These identities are stable across commits when the defining facts are unchanged, even if files move (W-04). | Moving a controller file between packages keeps the boundary's logical identity; editing the handler body changes only its version identity. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/graph/entity_registry.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-AB-008') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Moving a controller file between packages keeps the boundary's logical identity; editing the handler body changes only its version identity
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/graph/entity_registry.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/graph/entity_registry.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AB-009 [P2] REVA-AB-009: Client↔server matching (endpoint_match.py): for each outbound call, resolve the target service from base URL/config mapping (REVA_SERVICE_URL_MAP + discovered config keys), then match (method, canonic

- **Source:** `reva-requirements.md:883-883` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AB-009 | **Client↔server matching** (`endpoint_match.py`): for each outbound call, resolve the target service from base URL/config mapping (`REVA_SERVICE_URL_MAP` + discovered config keys), then match `(method, canonical template)` against that service's inbound routes. Scoring: exact template = 0.95; same segment count with parameter positions aligned = 0.75; prefix-only = 0.4 (never projected; becomes candidates in a gap). Ties produce `ambiguous` (no edge, gap with candidates). Matched pairs are projected as `reva_CALLS` with `inferred` epistemic state and the score as confidence. | Two-repo fixture (client JS + server Spring) produces the expected calls; an ambiguous fixture yields a gap with both candidates. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/extract/boundaries/extractor.py:208
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-AB-009') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Two-repo fixture (client JS + server Spring) produces the expected calls; an ambiguous fixture yields a gap with both candidates
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/boundaries/extractor.py:208`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/boundaries/extractor.py#L208-L208)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AB-015 [P2] REVA-AB-015: Wisdom Graph Precedent & Decision Extractor: Ingest and extract Architectural Decision Records (ADRs from docs/adr/, doc/decisions/, RFC/), Conventional Commit semantics (feat, fix, refactor, breaking

- **Source:** `reva-requirements.md:889-889` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AB-015 | **Wisdom Graph Precedent & Decision Extractor**: Ingest and extract Architectural Decision Records (ADRs from `docs/adr/`, `doc/decisions/`, `RFC/`), Conventional Commit semantics (`feat`, `fix`, `refactor`, `breaking`, `Fixes #`, `Ref:`), and PR discussion notes into Wisdom Graph entities (`wg_Decision`, `wg_Precedent`, `wg_Lesson`). Links architectural rationale to corresponding `reva_Service` and `reva_Boundary` vertices via `reva_JUSTIFIED_BY` edges. | ADR fixtures in markdown format are parsed into structured decision nodes with context, decision, and consequence; links to affected code routes verified in graph. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/extract/wisdom/wisdom_miner.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-AB-015') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] ADR fixtures in markdown format are parsed into structured decision nodes with context, decision, and consequence; links to affected code routes verified in graph
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/wisdom/wisdom_miner.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/wisdom/wisdom_miner.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AI-001 [P2] REVA-AI-001: Supported containers: ZIP (incl. JAR/WAR/EAR/APK-as-zip/whl/nupkg), TAR (+gzip/bzip2/xz), npm .tgz, Electron ASAR (header JSON + offsets), OCI image layout directories and docker save tarballs (manife

- **Source:** `reva-requirements.md:842-842` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AI-001 | Supported containers: ZIP (incl. JAR/WAR/EAR/APK-as-zip/whl/nupkg), TAR (+gzip/bzip2/xz), npm `.tgz`, Electron ASAR (header JSON + offsets), OCI image layout directories and `docker save` tarballs (manifest + layers), plain files and directories. Format detection uses magic bytes first, extension second; disagreements are recorded as limitations. | Fixture of each format inventories completely; a `.zip`-named TAR is detected as TAR with a limitation. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/extract/artifacts/inventory.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-AI-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Fixture of each format inventories completely; a .zip-named TAR is detected as TAR with a limitation
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/artifacts/inventory.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/artifacts/inventory.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AS-001 [P2] REVA-AS-001: Inputs: HAR 1.2; OTLP/JSON trace exports (resource + scope spans) using OpenTelemetry semantic conventions (http.request.method, http.route, url.full, url.path, server.address, server.port, http.respo

- **Source:** `reva-requirements.md:897-897` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AS-001 | Inputs: HAR 1.2; OTLP/JSON trace exports (resource + scope spans) using OpenTelemetry semantic conventions (`http.request.method`, `http.route`, `url.full`, `url.path`, `server.address`, `server.port`, `http.response.status_code`, `messaging.system`, `messaging.destination.name`, `db.system`, `db.collection.name`/`db.sql.table`, `peer.service`, `service.name`); NGINX/Apache combined log format; JSON-lines logs with a configurable field mapping (`REVA_AS_LOG_MAPPINGS`). | Fixture per input type parses with exact record counts; malformed lines are counted and reported, not dropped silently. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/extract/apisurface/miner.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-AS-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Fixture per input type parses with exact record counts; malformed lines are counted and reported, not dropped silently
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/apisurface/miner.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/apisurface/miner.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-BD-001 [P2] REVA-BD-001: Dual-identity binary comparison engine. Separates logical function identity (service:binary:symbol_name) from version identity (content hash and offset); prevents false-positive churn caused by code r

- **Source:** `reva-requirements.md:1170-1170` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-BD-001 | Dual-identity binary comparison engine. Separates logical function identity (`service:binary:symbol_name`) from version identity (content hash and offset); prevents false-positive churn caused by code relocation. | Compares two versions of a binary where code was reordered or recompiled with different base address; correctly matches unchanged functions despite address changes. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/diff/binary_identity.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-BD-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Compares two versions of a binary where code was reordered or recompiled with different base address; correctly matches unchanged functions despite address changes
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/diff/binary_identity.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/diff/binary_identity.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-BD-003 [P2] REVA-BD-003: Instruction-level normalized fuzzy hashing. Generates normalized instruction hashes (SSDEEP, TLSH) by abstracting immediate constants, register reassignments, and jump offsets; detects refactored func

- **Source:** `reva-requirements.md:1172-1172` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-BD-003 | Instruction-level normalized fuzzy hashing. Generates normalized instruction hashes (SSDEEP, TLSH) by abstracting immediate constants, register reassignments, and jump offsets; detects refactored functions across compiler optimization flags (`-O2` vs `-O3`). | Normalized fuzzy hash matches functions compiled across optimization flags; flags only genuine logic mutations. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/diff/fuzzy_hash.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-BD-003') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Normalized fuzzy hash matches functions compiled across optimization flags; flags only genuine logic mutations
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/diff/fuzzy_hash.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/diff/fuzzy_hash.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-CV-001 [P2] REVA-CV-001: Implement the Coverage model (§6.5) and compose(*coverages) -> Coverage with min-status, union of limits/reasons, summed examined counts and null-propagating omitted counts. · Property tests: composit

- **Source:** `reva-requirements.md:706-706` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-CV-001 | Implement the Coverage model (§6.5) and `compose(*coverages) -> Coverage` with min-status, union of limits/reasons, summed examined counts and null-propagating omitted counts. | Property tests: composition is associative and commutative; complete only if all inputs are complete. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/coverage.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-CV-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Property tests: composition is associative and commutative; complete only if all inputs are complete
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/coverage.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/coverage.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-CX-001 [P2] REVA-CX-001: Conflict keys: each predicate declares its functional aspects (JSON pointers into statement that must be single-valued per subject at a given valid time). Detection runs on issue for warrants sharing 

- **Source:** `reva-requirements.md:733-733` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-CX-001 | Conflict keys: each predicate declares its functional aspects (JSON pointers into `statement` that must be single-valued per subject at a given valid time). Detection runs on issue for warrants sharing `(tenant, subject_key, predicate, aspect)` with overlapping valid time and different values. | Two warrants giving different owners for the same service in overlapping intervals create one `value_conflict`. | component
```
</details>

**Next steps**
1. Read the referenced code: reva/api/routes_contradictions.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-CX-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Two warrants giving different owners for the same service in overlapping intervals create one valueconflict
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/api/routes_contradictions.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/api/routes_contradictions.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-DB-001 [P2] REVA-DB-001: SQLite: open with URI file:<path>?mode=ro&immutable=1, inventory tables, columns, PKs, FKs, indexes, views (SQL), triggers; record the DB file and -wal sibling digests; warn that a live DB/WAL copy ma

- **Source:** `reva-requirements.md:912-912` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-DB-001 | SQLite: open with URI `file:<path>?mode=ro&immutable=1`, inventory tables, columns, PKs, FKs, indexes, views (SQL), triggers; record the DB file and `-wal` sibling digests; warn that a live DB/WAL copy may be non-atomic. | Fixture DB inventories exactly; the DB file's digest is unchanged after inspection. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/extract/dbschema/introspect.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-DB-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Fixture DB inventories exactly; the DB file's digest is unchanged after inspection
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/dbschema/introspect.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/dbschema/introspect.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-DI-003 [P2] REVA-DI-003: Breakpoint, watchpoint, and bounded memory inspection controller. Sets software and hardware breakpoints on virtual addresses and exported symbols; reads memory slices with strict size bounds ($\le 64

- **Source:** `reva-requirements.md:1138-1138` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-DI-003 | Breakpoint, watchpoint, and bounded memory inspection controller. Sets software and hardware breakpoints on virtual addresses and exported symbols; reads memory slices with strict size bounds ($\le 64\text{ KiB}$) and register values. | Hits breakpoint in fixture binary; inspects registers and stack memory; rejects memory reads exceeding limit with `REVA_ERR_INSPECTION_LIMIT`. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/dynamic/mem_redactor.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-DI-003') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Hits breakpoint in fixture binary; inspects registers and stack memory; rejects memory reads exceeding limit with REVAERRINSPECTIONLIMIT
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/dynamic/mem_redactor.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/dynamic/mem_redactor.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-DI-004 [P2] REVA-DI-004: Instruction and call-path execution tracer. Records executed basic blocks, function calls, and branch decisions into a bounded ring-buffer (max 100,000 events); prevents log exhaustion. · Captures exa

- **Source:** `reva-requirements.md:1139-1139` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-DI-004 | Instruction and call-path execution tracer. Records executed basic blocks, function calls, and branch decisions into a bounded ring-buffer (max 100,000 events); prevents log exhaustion. | Captures exact execution trace of target function; produces `reva_RuntimeTrace` entity with instruction count and branch decisions; ring-buffer overflow handled gracefully with truncation limitation. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/dynamic/crash_triage.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-DI-004') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Captures exact execution trace of target function; produces revaRuntimeTrace entity with instruction count and branch decisions; ring-buffer overflow handled gracefully with truncation limitation
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/dynamic/crash_triage.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/dynamic/crash_triage.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-001 [P2] REVA-IF-001: POST /warrants · Issue warrant from draft (system/human producers; extractors use internal API) · analyst+

- **Source:** `reva-requirements.md:1222-1222` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-001 | `POST /warrants` | Issue warrant from draft (system/human producers; extractors use internal API) | analyst+
```
</details>

**Next steps**
1. Read the referenced code: reva/api/routes_warrants.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-IF-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-001 | POST /warrants | Issue warrant from draft (system/human producers; extractors use internal API) | analyst+»
- [ ] Issue warrant from draft (system/human producers; extractors use internal API)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/api/routes_warrants.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/api/routes_warrants.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-020 [P2] REVA-IF-020: GET /obligations, POST /obligations/sync (load YAML), POST /obligations/propose-from-jira/{issue_key}, POST /obligations/{key}/review, GET /obligations/{key} · Obligations · viewer / reviewer

- **Source:** `reva-requirements.md:1232-1232` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-020 | `GET /obligations`, `POST /obligations/sync` (load YAML), `POST /obligations/propose-from-jira/{issue_key}`, `POST /obligations/{key}/review`, `GET /obligations/{key}` | Obligations | viewer / reviewer
```
</details>

**Next steps**
1. Read the referenced code: reva/api/routes_pd.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-IF-020') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-020 | GET /obligations, POST /obligations/sync (load YAML), POST /obligations/propose-from-jira/{issue_key}, POST /obligations/{key}/review, GET /obligations/{key} | Obligations | viewer / reviewer»
- [ ] GET /obligations, POST /obligations/sync (load YAML), POST /obligations/propose-from-jira/{issue_key}, POST /obligations/{key}/review, GET /obligations/{key}
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/api/routes_pd.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/api/routes_pd.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-030 [P2] REVA-IF-030: GET /logs/{log_id}/sth, GET /logs/{log_id}/sth/history · Tree heads · viewer

- **Source:** `reva-requirements.md:1239-1239` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-030 | `GET /logs/{log_id}/sth`, `GET /logs/{log_id}/sth/history` | Tree heads | viewer
```
</details>

**Next steps**
1. Read the referenced code: reva/api/routes_logs.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-IF-030') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-030 | GET /logs/{log_id}/sth, GET /logs/{log_id}/sth/history | Tree heads | viewer»
- [ ] GET /logs/{log_id}/sth, GET /logs/{log_id}/sth/history
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/api/routes_logs.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/api/routes_logs.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-KG-001 [P2] REVA-KG-001: Implement the gap model (§6.8.1) with stable gap1_ identity and a hash-chained revision history; every revision is itself recorded by a warrant (reva.pred.gap_revision). · Editing a stored revision br

- **Source:** `reva-requirements.md:718-718` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-KG-001 | Implement the gap model (§6.8.1) with stable `gap1_` identity and a hash-chained revision history; every revision is itself recorded by a warrant (`reva.pred.gap_revision`). | Editing a stored revision breaks chain verification; recording the same question twice returns the existing gap. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/api/routes_gaps.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-KG-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Editing a stored revision breaks chain verification; recording the same question twice returns the existing gap
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/api/routes_gaps.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/api/routes_gaps.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-MB-001 [P2] REVA-MB-001: APK & AAB container unbundler with ZIP bomb protection and binary XML decoder. Safely extracts and parses AndroidManifest.xml (decoding binary AXML into standard XML DOM), app package name, version co

- **Source:** `reva-requirements.md:1101-1101` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-MB-001 | APK & AAB container unbundler with ZIP bomb protection and binary XML decoder. Safely extracts and parses `AndroidManifest.xml` (decoding binary AXML into standard XML DOM), app package name, version code, version name, min/target SDK, and debuggable status. | Parses standard and obfuscated AXML manifests; enforces 200:1 maximum decompression ratio; correctly detects debuggable flag and exported components. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/extract/mobile/apk_parser.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-MB-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Parses standard and obfuscated AXML manifests; enforces 200:1 maximum decompression ratio; correctly detects debuggable flag and exported components
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/mobile/apk_parser.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/mobile/apk_parser.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-MB-004 [P2] REVA-MB-004: iOS IPA bundle analyzer. Unpacks .ipa archive, parses Info.plist, embedded mobile provisioning profiles (embedded.mobileprovision), app entitlements, URL schemes (CFBundleURLTypes), and Fat Mach-O bin

- **Source:** `reva-requirements.md:1104-1104` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-MB-004 | iOS IPA bundle analyzer. Unpacks `.ipa` archive, parses `Info.plist`, embedded mobile provisioning profiles (`embedded.mobileprovision`), app entitlements, URL schemes (`CFBundleURLTypes`), and Fat Mach-O binary architecture slices. | Extracts bundle ID, version, minimum iOS version, registered custom URL schemes, and declared app entitlements; verifies code sign metadata without macOS host dependency. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/extract/mobile/jni_mapper.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-MB-004') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Extracts bundle ID, version, minimum iOS version, registered custom URL schemes, and declared app entitlements; verifies code sign metadata without macOS host dependency
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/mobile/jni_mapper.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/mobile/jni_mapper.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-MC-002 [P2] REVA-MC-002: MCP server tools exactly as in §9.2, with JSON Schemas generated from Pydantic models; input schemas strict; output schemas describe successful results; errors use the error contract (§10.1). Tools ar

- **Source:** `reva-requirements.md:986-986` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-MC-002 | MCP server tools exactly as in §9.2, with JSON Schemas generated from Pydantic models; input schemas strict; output schemas describe successful results; errors use the error contract (§10.1). Tools are registered in KGF's MCP server when it exists (IP-06); otherwise REVA starts its own stdio and streamable-HTTP MCP server. | MCP conformance test: list tools, call each tool with valid and invalid input, check schemas and error shape. | acceptance
```
</details>

**Next steps**
1. Read the referenced code: reva/mcp/server.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-MC-002') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] MCP conformance test: list tools, call each tool with valid and invalid input, check schemas and error shape
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/mcp/server.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/mcp/server.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-MC-007 [P2] REVA-MC-007: CLI kgf reva <command> (or a standalone reva entry point if KGF has no CLI) covering §9.3, with --json, --tenant, exit codes (§10.2) consistent with the REST/MCP errors. · CLI acceptance tests per com

- **Source:** `reva-requirements.md:991-991` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-MC-007 | CLI `kgf reva <command>` (or a standalone `reva` entry point if KGF has no CLI) covering §9.3, with `--json`, `--tenant`, exit codes (§10.2) consistent with the REST/MCP errors. | CLI acceptance tests per command. | acceptance
```
</details>

**Next steps**
1. Read the referenced code: reva/cli/main.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-MC-007') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] CLI acceptance tests per command
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/cli/main.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/cli/main.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NB-003 [P2] REVA-NB-003: Headless Ghidra decompilation batch worker with Python bridge generating structured C pseudocode AST without GUI dependency. Worker executes inside an ephemeral container, reads binary bytes, and emit

- **Source:** `reva-requirements.md:1083-1083` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NB-003 | Headless Ghidra decompilation batch worker with Python bridge generating structured C pseudocode AST without GUI dependency. Worker executes inside an ephemeral container, reads binary bytes, and emits JSON AST containing AST function nodes, expressions, control flow statements, and variable scopes. | Decompiles stripped C binaries into structured C AST; recovers function argument count, return type, and local stack variable allocations; runs headless with zero GUI or display server. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/extract/native/cfg.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-NB-003') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Decompiles stripped C binaries into structured C AST; recovers function argument count, return type, and local stack variable allocations; runs headless with zero GUI or display server
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/native/cfg.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/native/cfg.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-NB-007 [P2] REVA-NB-007: Native import/export and dynamic symbol table parser (PLT/GOT, IAT/EAT). Resolves dynamic library dependencies, imported APIs, and exported symbols; matches calls to known standard library and system 

- **Source:** `reva-requirements.md:1087-1087` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-NB-007 | Native import/export and dynamic symbol table parser (PLT/GOT, IAT/EAT). Resolves dynamic library dependencies, imported APIs, and exported symbols; matches calls to known standard library and system runtime APIs. | Identifies all imported DLL/SO functions with calling conventions; maps unresolved externals to library dependencies in SBOM. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/extract/native/vuln_scanner.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-NB-007') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Identifies all imported DLL/SO functions with calling conventions; maps unresolved externals to library dependencies in SBOM
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/native/vuln_scanner.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/native/vuln_scanner.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-PD-001 [P2] REVA-PD-001: Load and validate obligation YAML and bindings (schema, unique keys, acyclic dependencies, case-kind coverage of fixtures, journey presence rules). Validation errors list every violation with file:lin

- **Source:** `reva-requirements.md:784-784` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-PD-001 | Load and validate obligation YAML and bindings (schema, unique keys, acyclic dependencies, case-kind coverage of fixtures, journey presence rules). Validation errors list every violation with file:line. | Invalid fixtures produce precise errors; valid set loads; dependency cycle detected. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/pd/bindings.py:1, reva/pd/obligations.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-PD-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Invalid fixtures produce precise errors; valid set loads; dependency cycle detected
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/pd/bindings.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/pd/bindings.py#L1-L1), [`reva/pd/obligations.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/pd/obligations.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

