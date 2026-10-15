# CP Implementation Changes: Audit, Gap Analysis, and Handoff

Audit date: 2026-10-14, Asia/Calcutta.

Requirements baseline: [gaps-audit-cp.md](gaps-audit-cp.md).
Execution contract: [gaps-audit-cp-implementation-plan.md](gaps-audit-cp-implementation-plan.md).
Comparison base: working-tree changes relative to `df8223b`.

Licensing follow-up, 2026-10-14: the project owner selected proprietary commercial terms for owned code, named Avyukthi AI and Murthy Ravinder kumar, and selected both SaaS and customer-installed delivery. The root Apache notice has been replaced by a scoped proprietary notice; see [LICENSING.md](LICENSING.md) for the commercial drafts, third-party boundary, ownership register and release checklist. This resolves the intended licensing direction, not legal ownership verification or dependency clearance. The default API image includes the GPL-identified `extract-msg` dependency and is not cleared for proprietary distribution. OPEN-14 remains partially unresolved. Earlier test receipts below describe their original source snapshot, not subsequent packaging or unrelated implementation changes.

Licensing packaging verification: six focused tests passed (`test-results/licensing/documents.xml`); focused Ruff and diff-whitespace checks passed. An isolated Python wheel build succeeded, its metadata declares `LicenseRef-EOIP-Proprietary`, and all nine included license/policy documents were checked byte-for-byte against the repository. The web production build succeeded and `dist/legal/LICENSE` matches the module notice; `dist/legal/NOTICE` is present. `vsce ls` includes the extension's LICENSE. The complete VSIX archive, Docker images, full application suite, and exhaustive third-party notices/source obligations were not verified in this licensing follow-up. These packaging checks do not approve commercial distribution.

## 1. Executive Result

**The new changes are a useful partial implementation, not a completed platform or a production-ready multi-tenant release.** This audit found and repaired defects in requirement importing, authentication validation, event isolation, disconnect cleanup, CORS, report configuration, and test execution evidence. Important shared-storage, identity lifecycle, authorization, streaming, persistence, and release-evidence gaps remain open.

The implementation preserves all 2,603 audit records and the 944 pre-migration registry records. No requirement has been promoted to `VERIFIED`. Current registry states remain `UNTRIAGED` until individual source definitions, dispositions, acceptance clauses, and owners are reconciled. This status does not mean no code exists; it means the new closure contract has not yet been satisfied.

The historical audit is deliberately unchanged. Its statuses, dates, counts, source locations, and hash are historical evidence. This document records the newer behavior and supersedes neither the requirement definitions nor the original audit findings wholesale.

### Audit Scope and Limits

1. Parsed every one of the 2,603 audit matrix records, preserving all 15 columns and checking exact coverage against the implementation plan's execution index.
2. Compared the changed registry, evidence tooling, authentication, HTTP/WebSocket/event paths, tenancy wiring, CORS, HTML export, report generation, and CI with their applicable CP work packages.
3. Read the changed implementation paths and their relevant existing callers, tests, and requirement excerpts. Ran focused unit, security, integration, browser, build, and collection checks.
4. Included additional changes already present in the workspace, including report renderers, SSE framing, `LICENSE`, and `NOTICE`. Their presence is not evidence that they were authorized or complete.
5. Did not re-read and semantically re-audit every unchanged Markdown file or every unchanged application module in this pass. Parsing the complete matrix is not equivalent to resolving every normative source block.
6. Did not run live identity-provider, real graph-backend, reverse-proxy, cloud connector, multi-replica, restore, performance, desktop, or third-party acceptance environments.

## 2. Baseline and Traceability

| Measure | Observed result | Interpretation |
|---|---|---|
| Audit records | 2,603 unique original/audit ID pairs | Exact matrix coverage, not 2,603 independent features |
| Audit columns | 15 per record | Escaped Markdown pipes preserved |
| Legacy registry | 944 records retained | Historical status/evidence retained under `legacy_claims` |
| Current registry | 2,603 records | No legacy-only records in the migration |
| Current closure state | 2,603 `UNTRIAGED` | No unsupported completion promotion |
| Audit SHA-256 | `affc9247d2383b02a4e9257e9bb85b9d20e81593f28c3e4d40d29323f17ed602` | LF-normalized immutable audit |
| Historical registry SHA-256 | `55917afdef287ee9c167c4f164b90b7ff74217423e89ef378f6783c5bb58df94` | LF-normalized pre-migration source snapshot |
| Registry validation | Passed | IDs, baseline equality, routing import, schema and guarded states |
| Full test collection | 3,585 tests at the final collection run | Collection only; these tests were not all executed |
| Requirement marker IDs | 677 | Includes unresolved/noncanonical markers |
| Registry IDs with markers | 670 | A marker alone does not establish relevant assertions |
| Registry IDs without markers | 1,933 | Requires semantic test mapping, not bulk automatic tagging |
| Unique marked test nodes | 874 | Some tests carry multiple requirement markers |
| Unknown marker IDs | 7 | `NFR-REL-003`, `REQ-001` through `REQ-005`, and a malformed section-47 marker |

Collection numbers above describe that run. Subsequent additions require regenerating the map; the current generated file is authoritative for collected node names, not historical counts in this table.

### Historical Registry Self-Reference

Some audit rows cite lines in `requirements-registry.json`. Once that registry is migrated, reading its current contents as an immutable source recursively embeds generated output and invalidates the baseline. An intermediate generated file grew beyond the loader's 16 MiB bound.

The repair uses `config/verification/cp-registry-baseline.json`, copied byte-for-byte from the audit commit's registry (`54e31304fd089e471cef83fbc4a5e89660a36195`). Its pinned digest is checked before use. Missing or altered snapshots fail closed. Runtime importing no longer depends on `git show`, so a shallow checkout or source archive does not silently select a different source. The generated registry is approximately 6.1 MB rather than the earlier oversized output.

Source hashing normalizes CRLF to LF for audit documents and the snapshot. Execution receipts intentionally hash actual checked-out code/configuration bytes; they are tied to that execution environment.

## 3. Findings Repaired in This Batch

### FIX-01: Circular and Unreliable Completion Evidence

Priority: P0. Packages: CP-00, CP-02, CP-36.

- Replaced automatic completion inference from file/test references with an explicit implementation schema and conservative migration.
- Preserved legacy metadata and status claims without treating them as current proof.
- Added bounded parsing, exact audit/plan ID coverage, duplicate detection, source-location checks, project-relative path checks, baseline digests, alias-cycle checks, and clause-ID validation.
- Added the pinned historical registry snapshot and a real-repository save/read/idempotence regression.
- `INTEGRATION_VERIFIED` and `VERIFIED` remain rejected because the full acceptance/sign-off verifier is not implemented. This is an explicit fail-closed limitation, not an implemented release gate.

Files: `packages/eoip/verification/cp_registry.py`, `scripts/build_requirements_registry.py`, `requirements-registry.json`, `config/verification/cp-registry-baseline.json`.

### FIX-02: Stale Test Maps and Unsupported Passing Claims

Priority: P0. Packages: CP-00, CP-02.

- Ordinary pytest runs no longer rewrite the repository test map.
- `--requirements-map` explicitly replaces a map from the current collection; deleted tests are not merged back from stale entries.
- Incomplete/erroring collection does not overwrite a useful earlier map.
- `--run-evidence` records selected node IDs, markers, actual setup/call/teardown outcomes, exit status, collection errors, timestamps, revision, invocation arguments, and source hashes before/after execution.
- Receipt checks reject collect-only runs, failed/skipped/xfail/incomplete execution, changed source, missing cases, count mismatch, and altered receipt content.
- Current evidence collection deliberately rejects distributed pytest execution rather than creating an incomplete combined receipt.

Files: `packages/eoip/verification/pytest_evidence.py`, `packages/eoip/verification/test_receipts.py`, `tests/conftest.py`.

Limits: local hashes prove content integrity, not independent authenticity. Source manifests cover declared code/configuration trees and root inputs, not model weights, runtime services, all data, or every repository file. A collection map is an inventory, never a passing test receipt.

### FIX-03: Arbitrary Tokens Accepted as Authenticated Identity

Priority: P0. Packages: CP-04, CP-09.

- `TokenValidator` delegates to the canonical HMAC `TokenService`; sufficiently long opaque strings are no longer accepted.
- Removed the implicit validator signing secret and the nonstandard token-signature path.
- Validates object/header shape, HS256 algorithm, signature, issuer, audience, subject, finite bounded expiry/not-before values, role list shape, identity claim shape, and conflicting tenant claims.
- Handles oversized numeric dates without overflowing float conversion.
- HTTP and WebSocket paths now share principal construction; actual identities replace fixed `local-user` audit attribution on the changed HTTP path.

Files: `packages/eoip/authn/__init__.py`, `packages/eoip/authn/oauth_sso.py`, `apps/api/main.py`.

Limits: bootstrap shared-token access remains; signed tokens do not establish a complete login/session system. See OPEN-03 and OPEN-04.

### FIX-04: Tenant Spoofing and Unscoped Event Disclosure

Priority: P0. Packages: CP-04, CP-06, CP-11.

- Added a common tenant selection rule based on the authenticated principal.
- Tenant-bound administrators cannot use their role to select an unrelated tenant.
- Unbound nonadministrative users cannot invent a tenant through headers or query parameters.
- The tenancy dependency uses authenticated principal identity instead of a forged `X-Principal` header when a principal is present. Production header-only context is rejected.
- WebSocket and polling paths use the same event visibility rule, including the tenant named `default`.
- Tenant-scoped consumers reject events with no usable ownership metadata and events with conflicting tenant/canonical-ID metadata.
- Polling applies scope filtering before its result limit, preventing unrelated events from filling the requested page.
- Tenancy service construction now receives the graph store instead of an unconnected constructor.

Files: `packages/eoip/tenancy/context.py`, `packages/eoip/enterprise/middleware.py`, `packages/eoip/events/emitter.py`, `apps/api/main.py`, `apps/api/extended.py`.

Limits: correct context selection and event filtering do not make every domain repository tenant-safe. Global/platform administrative scope remains a distinct privileged path. Domain-wide isolation remains release-blocking.

### FIX-05: WebSocket Cleanup and Cross-Thread Delivery

Priority: P1. Packages: CP-10, CP-11.

- Register the subscriber's owning event loop at subscription time instead of inspecting private queue state after its first read.
- Schedule delivery on that loop when events originate in synchronous worker threads.
- Catch bounded queue overflow inside the scheduled callback, where the exception actually occurs.
- Snapshot subscriber/ring-buffer state under a lock for concurrent access.
- Wait for disconnect concurrently with incoming events; idle connections do not wait indefinitely for another graph event before cleanup.
- Remove subscriptions before awaited task cleanup so cancellation cannot skip removal.
- Close authenticated WebSockets when the local token expires.

Limits: queues and replay buffers remain process-local; event IDs, durable replay, revocation notifications, heartbeats, drop notifications, and cross-replica delivery are not completed.

### FIX-06: Administrative Mutations Lacked a Role Check

Priority: P0. Package: CP-05.

- The composed API now rejects nonadministrative mutation requests under the current admin/source/authz/security/tenancy prefix guard before execution.
- Tests cover viewer rejection on admin, role-management, security token issuance, and source endpoints.
- Webhook requests remain outside this coarse guard and must satisfy their separate webhook authentication contract.

Limits: this is an interim prefix-level guard, not exhaustive resource authorization. Some read-like POST operations may require a more precise policy classification. It does not prove that tenant-bound administrators are correctly limited inside every administrative service.

### FIX-07: CORS Defaults and Preflight Integration

Priority: P0. Packages: CP-07, CP-08.

- Removed wildcard credentialed CORS defaults.
- Validates explicit HTTP(S) origins; rejects wildcards, credentials, paths, query strings, fragments, whitespace, and invalid ports.
- Local development retains explicit localhost origins. Production without configured origins does not implicitly permit localhost.
- Genuine browser preflight requests reach CORS middleware without requiring a bearer token. This exemption does not authenticate subsequent data requests.
- Tests exercise allowed and denied preflights through the composed API, malformed configuration, and production defaults.

Configuration: `EOIP_CORS_ORIGINS=https://web.example.test` or comma-separated explicit origins. Do not include trailing paths. Production profile detection uses `EOIP_ENV` with `APP_ENV` fallback.

### FIX-08: Interactive HTML Export Injection

Priority: P0. Packages: CP-08, CP-23, CP-25.

- Escapes exported document titles and script-embedded JSON delimiters.
- Replaced property inspector `innerHTML` interpolation with DOM creation and `textContent`.
- Uses a null-prototype node-position map so a node ID such as `__proto__` does not alter object behavior.
- Browser tests exercise hostile titles, closing-script strings, property keys/values, canvas rendering, inspector selection, and search.

Files: `apps/web/src/kgr/export/InteractiveExport.js`, `apps/web/tests/interactive-export-security.spec.js`.

Limits: this tests the standalone export surface, not every application rendering sink, SVG/CSV export, URL-opening path, or CSP configuration.

### FIX-09: Report Format Gate and Artifact Contract

Priority: P1. Package: CP-25.

- Retained the newly added PDF/DOCX/PPTX byte renderers and stored-artifact download path.
- Added an installable `reports` optional dependency group and CI installation for renderer tests.
- Removed the HTTP query-parameter bypass of disabled binary rendering. Deployment configuration controls `EOIP_ENABLE_EXTERNAL_REPORT_FORMATS`.
- Missing renderer dependencies return 503 rather than an uncontrolled import failure.
- Export returns the stored artifact's actual format; an explicitly different requested format returns 409 instead of being ignored.
- Invalid stored binary encoding fails explicitly instead of returning textual bytes labeled as a document.
- `render_bytes` shares required-parameter and format-gate validation with `render`.
- Tests check PDF magic bytes and DOCX/PPTX ZIP package structure, not merely nonempty output.

Limits: binary document structure is not visual fidelity. Persistence, resource ownership, retention, schedules, approvals, white-label layouts, long-content pagination, table fidelity, and rendered visual QA remain incomplete. PDF remains disabled unless configured, so the source's P0 PDF requirement is not generally closed.

### FIX-10: Logging Module Import Order Broke Composed Startup

Priority: P1. Packages: CP-02, CP-30.

Importing `eoip.observability.logging` replaced the package's `logging` attribute, causing `configure_json_logging()` to call `getLogger` on the child module instead of the standard library. The combined regression suite exposed this even though the MCP tests passed in isolation.

The package now aliases the standard-library import. A regression imports the child module first, then configures logging twice and checks idempotent handler creation.

## 4. Remaining Findings and Required Closure

| ID | Priority | Observation and evidence | Required implementation and acceptance |
|---|---|---|---|
| OPEN-01 | P0 | Most domain routes still capture a global `store`; `ontology_export()` calls `export_jsonld(store)` without a principal-scoped repository. | CP-03/05/06: inject scope-enforcing repositories into every data consumer. Prove two tenants with identical logical IDs in one real backend cannot read/write/export each other's data. |
| OPEN-02 | P0 | `reports/router.py` keeps artifacts in `rendered_store`, a router-local dictionary with no artifact owner. The schedule store is not comprehensively tenant-scoped. | CP-03/06/25: durable artifact metadata/content, tenant and creator ownership, authorized downloads, bounded size/retention, restart and cross-tenant negative tests. |
| OPEN-03 | P0 | Bootstrap tokens remain accepted; local HMAC token service and enterprise `TokenSigner` have separate issuance/verification/revocation paths. | CP-04: one supported identity/session contract, explicit production mode, secure key management/rotation, durable revocation, logout, and public endpoint integration tests. |
| OPEN-04 | P0 | `SAMLAdapter` still parses simulated assertions; break-glass/federation helpers contain permissive behavior. | CP-04: real signature/issuer/audience/replay verification or fail-closed unsupported behavior. Require configured identity-provider tests; do not advertise helper parsing as federation. |
| OPEN-05 | P0 | Prefix-level administrative checks do not inventory all actions, ownership decisions, policy edits, raw queries, jobs, or MCP operations. | CP-05/07: explicit operation/action/resource policy matrix, deny-by-default service checks, role revocation, field filtering, and no-self-escalation tests. |
| OPEN-06 | P0 | Browser `useGraphEvents.js` opens an unauthenticated WebSocket and unauthenticated replay fetch. Durable tokens in query parameters are still accepted by the server. | CP-04/08/11/24: secure session or short-lived one-use handshake credentials, authenticated replay client, logout/tenant-switch cleanup, and reconnect tests. Do not put durable tokens in browser URLs. |
| OPEN-07 | P0 | New SSE response framing does not make the provider incremental. `SelfLLMEngine.generate_stream()` first calls `generate()` to completion, then splits words. | CP-11/19: connect a real incremental provider, propagate cancellation, measure first chunk before completion through the deployed proxy, and preserve nonstreaming compatibility. The ASGI framing test does not prove latency. |
| OPEN-08 | P0 | Full normative source recovery, alias classification, profile applicability, per-clause acceptance, and accountable owners are not populated across the registry. | CP-00/01: recover complete source blocks and references in small batches; record engineering/alias/metadata/external-owner dispositions with rationale. Resolve all definitions before claiming the batch's G0 gate. |
| OPEN-09 | P0 | 1,933 registry records lacked a marker in the recorded collection; seven collected marker IDs were unresolved. Existing broad markers may be semantically weak. | CP-00/02: investigate each unmatched marker; map actual assertions to atomic requirements, repair encoding errors, and distinguish fixture IDs from product IDs. Never mass-tag unrelated tests to inflate coverage. |
| OPEN-10 | P0 | Integration/acceptance receipt promotion is deliberately unavailable. Existing older gate helpers are not all migrated to this contract. | CP-02/36: implement authoritative receipt schema/trust validation, profile/clauses/environment binding, integration evidence, owner decisions, and negative gate tests. Reconcile all completion consumers. |
| OPEN-11 | P0 | Events, subscriptions, and replay remain process-local. Buffer overflow drops events and IDs do not form a durable cross-replica sequence. | CP-03/10/11: scoped durable outbox/broker, replay cursor contract, gap signaling, idempotent consumption, backpressure policy, restart/reconnect/multi-replica tests. |
| OPEN-12 | P1 | PPTX section rendering does not carry section tables. PDF/DOCX/PPTX layout and long-content overflow were not visually verified. | CP-25: preserve every section/table/evidence item, add readable wrapping/pagination, render golden artifacts, and inspect long and Unicode fixtures. |
| OPEN-13 | P1 | Report scheduling is not demonstrated as durable, tenant-authorized, single-execution worker delivery; approvals and branding are not integrated. | CP-10/25/28: schedules with timezone/missed-run rules, worker claims, retry/cancel, versioned approvals, branding and downloadable artifacts. |
| OPEN-14 | P0 | Added root `LICENSE`/`NOTICE` files do not establish owner approval, accurate dependency terms, model rights, or a complete SBOM. | CP-01/33: authorized owner decision, exact dependency/asset/model inventory, notices and redistribution evidence. Existing files were preserved, not treated as legal approval. |
| OPEN-15 | P1 | The new snapshot importer requires explicit reconciliation when normative sources change; an approved rebaseline workflow is not implemented. | CP-00/35: versioned baseline migration command with reviewable before/after mappings, preserved history, and explicit ownership. Never silently recalculate historical claims. |
| OPEN-16 | P0 | CORS and HTML export fixes do not establish session CSRF protection, deployment CSP, safe rich rendering everywhere, or protected docs/metrics policy. | CP-04/08: threat-model each browser surface, add policy headers and cookie rules, and run hostile-input browser tests across supported flows. |
| OPEN-17 | P0 | No fresh real-backend, proxy timing, live connector, HA/DR, performance or independent release acceptance receipts were produced. | CP-13/16/29/31/32/36: configured environments, reproducible fixtures, teardown, versions, timings and immutable run artifacts. Keep each unavailable prerequisite explicit. |

## 5. Package-Level Status

These are change-audit statuses, not declarations that untouched packages have no implementation.

| Package | Current assessment from this batch |
|---|---|
| CP-00 | Partial: exact import/migration and guarded schema; semantic triage and clause-level completeness remain open. |
| CP-01 | Open: decisions, external prerequisite owners, license authority and acceptance scope not closed. |
| CP-02 | Partial: opt-in run receipts, current maps, focused tests and CI retention; full gate integration and broader execution remain open. |
| CP-03 | Not completed: no shared durable domain repository migration in this batch. |
| CP-04 | Partial: local token validation and principal propagation repaired; complete sessions/federation/revocation remain open. |
| CP-05 | Partial: coarse administrative mutation guard; exhaustive service/resource policies remain open. |
| CP-06 | Partial: identity-based context and event scoping; domain-wide storage isolation remains open. |
| CP-07 | Partial: CORS preflight and selected report error contracts; full operation/client inventory remains open. |
| CP-08 | Partial: safe standalone HTML export and explicit CORS; full browser security remains open. |
| CP-09 | Narrow contribution: rejects malformed local authentication inputs; egress/privacy/injection governance not completed. |
| CP-10 | Narrow contribution: bounded event delivery mechanics; durable jobs/events/schedules not completed. |
| CP-11 | Partial: SSE framing and scoped WebSocket/polling; real provider streaming, client integration and durable replay remain open. |
| CP-12 | No new completion evidence for ontology governance. |
| CP-13 | No new real-backend conformance evidence. |
| CP-14 | No new query/federation completion evidence. |
| CP-15 | No new ingestion pipeline completion evidence. |
| CP-16 | No new live connector acceptance evidence. |
| CP-17 | No new entity-resolution/provenance completion evidence. |
| CP-18 | No new temporal/impact workflow completion evidence. |
| CP-19 | Not completed: the examined model stream remains buffered/simulated. |
| CP-20 | No new retrieval/index completion evidence. |
| CP-21 | No new grounded RAG/NLQ completion evidence. |
| CP-22 | No new agent/workflow authorization completion evidence. |
| CP-23 | Narrow contribution: interactive-export injection fix, not graph explorer feature closure. |
| CP-24 | Not completed: realtime browser authentication remains disconnected from the new server contract. |
| CP-25 | Partial: binary rendering/download and safer gating; durability, scope, fidelity and workflow remain open. |
| CP-26 | No new shared collaboration completion evidence. |
| CP-27 | No new offline/desktop/synchronization acceptance evidence. |
| CP-28 | No new administration/branding/localization completion evidence. |
| CP-29 | MCP transport regression tested; live host/SDK/plugin acceptance remains open. |
| CP-30 | Narrow contribution: logging import-order/startup repair, not operational SLO completion. |
| CP-31 | No new migration/restore/HA/DR acceptance evidence. |
| CP-32 | No new performance/capacity/cost acceptance evidence. |
| CP-33 | Files present, but authorized licensing and supply-chain acceptance remain open. |
| CP-34 | No new research acceptance evidence; do not infer capability from names or synthetic output. |
| CP-35 | This dated audit and plan status note added; historical documents deliberately preserved. |
| CP-36 | No release gate declared passed; unsupported verified states fail closed. |
| CP-37 | No new code-graph/domain catalog completion evidence. |

## 6. Verification Record

| Check | Result and scope |
|---|---|
| Registry `--check` | Passed: 2,603 records; no closure promotion. |
| First combined Python regression | 235 passed, 0 failed, 0 skipped; `test-results/cp-audit-regression.xml`. |
| Expanded final regression | 299 passed, 0 failed, 0 skipped, 0 errors; includes tenancy and SR-wave API regressions. Receipt validated against unchanged final source. |
| Interactive export browser tests | 2 passed in Chromium. Standalone artifact rendering and hostile-input behavior, not the full application UI. |
| Web production build | Passed. Existing large JavaScript bundle remains a performance follow-up, not a build failure. |
| Focused Ruff check | Passed on new verification/security tests, evidence modules, emitter, logging helper and registry script. Not a claim of repository-wide lint compliance. |
| Full collection | Completed; one collection warning for the helper dataclass `TestRunSummary`, which has a constructor. No full-suite execution claim. |

Final evidence targets: `test-results/cp-final-regression.xml` and `test-results/cp-final-regression-receipt.json`. A passing test count is usable only when the receipt reports successful execution and unchanged tested sources. Files under `test-results/` are local run artifacts, not implicitly committed release receipts.

Final execution window: `2026-10-14T13:11:09.794881+00:00` to `2026-10-14T13:13:40.808880+00:00`. Exit code: 0. `source_unchanged`: true. Receipt payload integrity digest: `b2b96dc6a99541795a7daeb1b26f30b0d87ee45f7cba2a3ea20a91cf158310bb`. This is the receipt's canonical payload digest, not a signature from an independent authority.

Earlier failed runs were diagnostic: one exposed the logging import collision; a later event test exposed cancellation-sensitive subscriber cleanup; the expanded tenancy test exposed an endpoint that bypassed the shared context resolver. All three were repaired before the final passing run. Failed or superseded receipts must not be used as acceptance evidence.

### Reproduction Commands

From the repository root in PowerShell:

```powershell
$env:PYTHONPATH = '.;packages'
python -m scripts.build_requirements_registry --check
python -m pytest --collect-only -q --requirements-map=requirements-test-map.json
python -m pip install -e '.[dev,reports]'
python -m pytest tests/unit/test_cp_registry.py tests/unit/test_pytest_execution_evidence.py tests/unit/test_requirement_evidence.py tests/unit/test_authn.py tests/unit/test_authz.py tests/unit/test_phase4_phase4_engines.py tests/unit/test_phase4_preflight.py tests/unit/test_kgr_events.py tests/unit/test_observability_import_order.py tests/unit/test_reports.py tests/unit/test_tenancy.py tests/unit/test_sr_wave_api_routes.py tests/security/test_token_validation_contract.py tests/security/test_http_and_realtime_contract.py tests/security/test_cors_contract.py tests/integration/test_mcp_transport.py -q --timeout=60 --junitxml=test-results/cp-final-regression.xml --run-evidence=test-results/cp-final-regression-receipt.json
```

For a configured local report-rendering profile:

```powershell
$env:EOIP_ENABLE_EXTERNAL_REPORT_FORMATS = 'true'
```

Do not treat this flag as approval to expose the currently process-local/unscoped report store to untrusted multi-tenant users.

From `apps/web`:

```powershell
npm run build
npx --no-install playwright test tests/interactive-export-security.spec.js --config=playwright.config.js
```

CI now validates the registry, captures unit/security execution receipts and JUnit, retains Python evidence, installs report renderers, builds the web app, and runs the export browser tests. This change does not prove that the complete remote CI workflow has already passed.

## 7. Next Implementation Batches

### Batch A: Recover Definitions and Establish a Trustworthy Work Queue

1. Start with BASE-01..04, INFRA-002, SR-TEN-001, SR-NLQ-008 and their linked original sources. Recover complete definitions instead of promoting the audit's shortened or derived acceptance text.
2. Record accountable owner, classification, scope/profile, dependencies, and independently testable acceptance clauses.
3. Resolve the seven unknown marker IDs and audit whether existing broad markers actually assert their claimed behavior.
4. Add source-block/alias/marker integrity validation and an explicit rebaseline workflow. Preserve all historical audit fields.
5. Implement a real integration/sign-off evidence verifier before permitting verified statuses. Independently review the trust model and negative promotion cases.

Exit: the selected batch has no unresolved engineering definition, no unowned acceptance clause, and no unsupported closure claim.

### Batch B: Identity, Resource Policy, and Storage Scope

1. Choose the supported production identity/session model and centralize token issuance, verification, revocation, key rotation, tenant membership and actor propagation.
2. Inventory actual composed routes and non-HTTP entrypoints, including mutation-like POSTs, raw queries, reports, jobs, security administration and MCP.
3. Add service-level resource authorization and tenant-enforcing repository interfaces. Eliminate global-store access for tenant operations.
4. Persist policy/session/domain state with migration and concurrency behavior appropriate to the selected deployment profile.
5. Test two tenants in one API and one actual backend, including exports, counts, traversals, cursors, reports, caches, queued work, and role revocation.

Exit: no cross-tenant observations or unauthorized mutations through any tested public or worker boundary. Header filtering alone is insufficient.

### Batch C: Realtime Integration

1. Replace credential-bearing WebSocket URLs with secure session or one-use scoped handshake tickets.
2. Integrate the web client with authentication, authorized replay, tenant changes, logout, retry cleanup and bounded buffering.
3. Persist ordered scoped event records and define reconnect, cursor expiry, dropped-event and slow-consumer behavior.
4. Connect a genuinely incremental provider; cancellation must stop computation rather than merely stop writing output.
5. Run a deployed proxy test with controlled delays: first chunk must arrive before provider completion; disconnect and token revocation must stop delivery.

Exit: authenticated end-to-end client/provider delivery, not just an SSE content type or an in-process generator.

### Batch D: Reports as Durable Authorized Artifacts

1. Replace `rendered_store` with a scoped durable artifact repository and store content digest, MIME type, format, creator, tenant, template version and evidence provenance.
2. Enforce ownership on render/list/download/delete and schedules; add byte limits, retention and worker recovery.
3. Preserve tables and evidence in every output format. Add pagination, fonts/Unicode support and golden render inspection for long content.
4. Integrate approval transitions, versioned white-label templates and actual recurring worker delivery.
5. Verify artifacts after restart and through the UI with two tenants. Test dependency absence, corruption, format mismatch, cancellation and schedule retries.

Exit: SR-NLQ-008 closes only when all its required formats and workflows meet their acceptance clauses; adding binary serializers is not enough.

## 8. Handoff Rules

- Preserve existing workspace changes; do not revert them to reproduce an earlier audit snapshot.
- Keep `gaps-audit-cp.md` immutable unless performing an explicit reviewed baseline migration.
- Do not regenerate completion percentages from file existence, checkboxes, marker counts or collection output.
- Never attach a failed, skipped, collect-only, source-stale or untrusted receipt as passing release evidence.
- A passing focused suite does not establish full application completion, production readiness, legal approval or research capability.
- Continue the implementation plan from the open dependency gates, using this audit as a dated change assessment rather than a replacement requirements specification.
