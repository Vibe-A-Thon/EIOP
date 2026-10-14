# EOIP / KnowGridFlow: Complete Gap Closure Implementation Plan

Document ID: `CP-IMPLEMENTATION-2026-10-14`  
Prepared: 2026-10-14, Asia/Calcutta  
Audience: coding AI agents, maintainers, QA, operations, product and legal owners  
Source audit: [gaps-audit-cp.md](gaps-audit-cp.md)  
Source audit date: 2026-10-13  
Source audit commit: `54e31304fd089e471cef83fbc4a5e89660a36195`  
Repository inspected for this plan: `192e9a0a9e61a22a652930b5ad3684622e25e508`  
Source audit SHA-256: `affc9247d2383b02a4e9257e9bb85b9d20e81593f28c3e4d40d29323f17ed602`  
Status: implementation instructions; no gap is closed merely by inclusion here.

Execution update, 2026-10-14: partial implementation and a change audit are recorded in [Audit-GAPS-G-dev.md](Audit-GAPS-G-dev.md). The registry now preserves all 2,603 baseline records, with current statuses kept `UNTRIAGED` pending semantic reconciliation. Evidence tooling, selected security/tenant/event boundaries, safe HTML export, report format handling and regression coverage have progressed. No complete CP package or release gate is declared closed; the linked audit lists repaired defects, remaining blockers, verification scope and next implementation batches.

Navigation: [Completion contract](#1-mission-and-completion-contract), [Baseline](#2-verified-planning-baseline), [Agent instructions](#3-agent-operating-instructions), [Shared contracts](#4-architecture-and-shared-contracts), [Phases](#5-phases-dependencies-and-exit-gates), [Work packages](#6-detailed-work-packages), [Validation](#7-validation-evidence-and-agent-handoff), [Finding crosswalk](#8-audit-finding-crosswalk), [Closeout](#9-release-closeout-checklist), [All requirement records](#appendix-a-complete-requirement-execution-index).

## 1. Mission and Completion Contract

Implement, integrate, and verify every applicable behavior represented by the source audit, including requirements initially classified as implemented but unverified. Deliver usable application workflows, durable operational behavior, and reproducible evidence. Existing code is the starting point: inspect, exercise, repair, and integrate it before adding a replacement.

This plan preserves all **2,603 audit records** in Appendix A. These are records, not necessarily 2,603 independent product features. Some are acceptance tests, implementation subtasks, document identifiers, repeated descriptions, role responsibilities, or references to requirements defined elsewhere. Every record must receive a documented disposition; none may disappear during normalization.

The target is **100% verified engineering implementation within an explicitly recorded scope**, followed by **100% required integration and release evidence**. A plan cannot guarantee frontier research outcomes, third-party credentials, legal decisions, hiring, or certification. Those requirements remain visible with their own owners and closure conditions. Do not describe engineering completion as completion of all audit records while non-engineering obligations remain open.

### 1.1 Three Separate Completion Measures

| Measure | Numerator | Denominator | Rule |
|---|---|---|---|
| Audit reconciliation | Records with a source definition, accountable owner, execution package, and explicit disposition | All 2,603 baseline records plus subsequently discovered records | An alias is reconciled only with a trace to its canonical requirement; reconciliation is not implementation. |
| Verified engineering completion | Canonical engineering requirements whose applicable acceptance clauses all pass | All canonical engineering requirements in the accepted scope | Partial implementation, skipped tests, missing infrastructure, and unsupported required adapters contribute zero closure. |
| Release readiness | Required gates with valid passing receipts for the release candidate | Every required gate for every advertised deployment profile | An unavailable external gate blocks the readiness claim. |

Report the count of unresolved, duplicate/alias, metadata-only, superseded, external-owner, and engineering records separately. Never silently reduce the denominator, delete an inconvenient requirement, lower an acceptance threshold after seeing results, or turn a required feature into an optional one to reach 100%.

### 1.2 Mandatory Definition of Done for Each Engineering Requirement

1. Recover the complete normative source, including adjacent bullets, tables, constraints, and referenced acceptance criteria. An abbreviated audit title is insufficient.
2. Establish the current behavior with a failing or missing acceptance scenario. If it already works, demonstrate it through the real public boundary and avoid redundant code.
3. Implement the domain behavior and its storage, API/tool, UI, worker, configuration, and deployment integrations wherever applicable.
4. Apply authenticated principal, tenant scope, authorization, validation, privacy, quotas, and audit behavior at every public and asynchronous boundary.
5. Handle empty input, invalid input, denied access, cancellation, timeout, dependency failure, retry, concurrent writes, restart, and partial results as relevant.
6. Add meaningful assertions for each acceptance clause. Record exact test node IDs; a file path or requirement marker alone is not proof.
7. Run the required tests on the current implementation. Capture output, exit status, environment, source/artifact hashes, and any infrastructure versions.
8. Exercise migrations and rollback/forward-repair when persistent state changes. Prove compatibility or document and test the versioned transition.
9. Update current API, configuration, operator, and user documentation. Preserve historical audit statements as dated evidence.
10. Attach evidence and change the canonical status only when all applicable checks pass. Every dependent alias points to the same evidence plus any additional assertions it requires.

## 2. Verified Planning Baseline

The audit file contains 18,505 content lines, 2,603 matrix rows with 15 columns each, and references 59 source documents. All 59 source paths existed when this plan was prepared. The complete matrix was parsed; its IDs are unique. The detailed findings repeat the matrix records by area. The closing audit sections contribute additional cross-cutting findings that are explicitly mapped in Section 8.

### 2.1 Audit Status and Priority Counts

| Audit status | Records | Required execution treatment |
|---|---:|---|
| IMPLEMENTED-UNVERIFIED | 966 | Trace and prove existing behavior; repair missing wiring or inadequate assertions. |
| PARTIAL | 60 | Enumerate missing acceptance clauses, then implement and verify those clauses. |
| STUBBED | 7 | Replace the stub with real behavior and test the delivered result. |
| MISSED | 1,567 | Search for equivalent existing behavior; build only after the missing behavior is established. |
| BLOCKED | 3 | Prepare code and acceptance harness; obtain the named prerequisite and run the gate. |
| IMPLEMENTED-VERIFIED | 0 | This is the audit's evidence assessment, not a claim that all existing code is broken. |

| Priority | Records |
|---|---:|
| P0 | 526 |
| P1 | 229 |
| P2 | 531 |
| P3 | 7 |
| UNSTATED | 1,310 |
| Total | 2,603 |

The audit's displayed priority table omits the seven P3 records. Preserve them. Some priority values may have been inferred from phase identifiers: for example, a source-wave label containing `P3` is not automatically a product priority. Resolve against the original requirement and retain both the audit value and the normalized value.

There are 175 audit titles containing `...`. Several `FRD-*` records point to an inventory line saying "Requirement IDs seen"; that is a reference requiring source recovery, not a sufficient acceptance definition. Some area assignments are misleading: graph export is classified as ONT, usage/billing as VEC, and rendering performance as CON. Appendix A therefore supplies **initial routing**, which CP-00 must validate against complete source text before code is changed.

### 2.2 Evidence Boundaries

The audit reports 110 focused tests passed, a successful web build, dependency scans, 3,492 tests collected, and a live specification with 734 operations. Its full pytest run did not complete successfully. These are historical observations. This planning task did not rerun the application test suite, production infrastructure, browser acceptance, or dependency scans and does not promote those observations to current release receipts.

Targeted source inspection for this plan confirmed these starting points:

| Current source | Observed behavior / implication |
|---|---|
| `apps/api/main.py` | Shared-token HTTP boundary and `local-user` audit actor; inspect WebSocket and webhook paths separately. |
| `apps/api/app.py` | Application factory mounts broad routers; default CORS allows all origins with credentials. |
| `apps/api/extended.py` | Process-local identity/config/model/branding holders; `TenancyService()` is initialized without the graph store. |
| `packages/eoip/reports/router.py` | PDF/DOCX/PPTX and stored-report download return 501. |
| `packages/eoip/brain/router.py` | LLM stream handler materializes `list(generate_stream(...))`. |
| `packages/eoip/models/provider.py` | An actual local model adapter already exists; extend the provider boundary instead of inventing another. |
| `packages/eoip/jobs.py` | Disk-backed queue explicitly described as single-worker; do not confuse file durability with multi-worker concurrency. |
| `tests/conftest.py` | Requirement map merges historical collection entries; stale entries require reconciliation. |
| `scripts/verify_requirement_evidence.py` | Existing conservative JUnit-based verifier can be extended; its current expected requirement set is MVP-specific. |
| `packages/eoip/verification/release_gate.py` | Existing release-receipt types and required gates; inspect actual validation before relying on them. |
| `apps/web/package.json` | Vite/React with JavaScript, Cytoscape, Graphology, Sigma, and Playwright; only `dev` and `build` npm scripts. |
| `apps/web/playwright.config.js` | Existing tests default to `http://eoip-web:8080`; local runs need the correct base URL. |
| `.github/workflows/ci.yml` | Current CI runs unit tests and web build; broaden it to the required acceptance layers. |
| `requirements-registry.json` | 944 records at inspection time; migrate/extend this registry without overwriting its existing IDs. |

## 3. Agent Operating Instructions

### 3.1 Start of Every Work Session

1. Read applicable repository instructions and inspect `git status`. Preserve unrelated changes and user-owned work.
2. Read this plan, the selected CP package, its dependency exits, and the full sources for the selected IDs in Appendix A.
3. Compare the current revision with this plan's inspected revision. Revalidate changed routes, symbols, test names, and schemas; line numbers are navigation hints, not immutable truth.
4. Choose a small coherent batch from the earliest unblocked phase. Security prerequisites outrank nominal product priority.
5. Search by original ID, behavior, current symbol, route, and tests. Search `apps/`, `packages/eoip/`, `tests/`, `scripts/`, and deployment configuration.
6. Produce a concrete task card before coding. Scope the write set, accepted behavior, test cases, migrations, and rollback.
7. Implement the smallest complete vertical workflow. Run focused checks, then the dependency and public-boundary integration checks.
8. Update the requirement record, receipts, and handoff in the same change. Continue with another unblocked package when a credential or owner decision blocks one package.

### 3.2 Required Task Card

```yaml
task_id: CP-06.001
audit_ids: [REQ-TEN-001] # illustrative; recover the actual definition first
original_ids: []
canonical_id: null
source_refs: []
source_hashes: {}
classification: engineering # or alias, metadata, external-owner, unresolved
normalized_priority: P0
owner_role: backend-tenancy
depends_on: [CP-03, CP-04, CP-05]
current_behavior: "Observed result and exact reproduction"
required_behavior: "Complete source outcome, without ellipsis"
acceptance_clauses: []
public_entrypoints: []
code_paths: []
storage_and_migration: []
api_and_client_changes: []
positive_tests: []
negative_tests: []
restart_concurrency_tests: []
operational_tests: []
rollback_or_forward_repair: "Required for state changes"
status: READY
blocker: null
receipt_paths: []
```

Split conjunctive requirements into child acceptance clauses such as `REQ-TEN-001.AC01`; preserve the parent audit ID. Parent closure requires all children. A module-level marker covering dozens of IDs does not substitute for this mapping.

### 3.3 Execution States

Use `UNTRIAGED -> READY -> IN_PROGRESS -> IMPLEMENTED -> INTEGRATION_VERIFIED -> VERIFIED`. Allow `BLOCKED` with a reason and resumption condition. Keep the original audit status immutable as a baseline field.

Use a separate disposition for `ALIAS`, `METADATA_ONLY`, `SUPERSEDED`, and `EXTERNAL_OWNER`. An alias must reference a canonical ID and justified equivalence. A superseded requirement needs an explicit source of supersession. Unclear requirements remain unresolved; do not invent a passing implementation from the title.

### 3.4 Prohibited Shortcuts

- Do not replace implementation with success-shaped dictionaries, canned model answers, placeholder artifacts, fake infrastructure receipts, or static UI data.
- Do not close requirements from file existence, a regex match, a checked Markdown box, aggregate coverage percentages, or a green build alone.
- Do not remove security checks to make existing tests pass. Repair fixtures so they authenticate through supported paths.
- Do not label every dictionary a persistence bug. Classify authoritative records, transient request state, bounded caches, and test doubles separately.
- Do not claim a generic backend adapter supports a vendor until the vendor's real protocol and required semantics pass acceptance.
- Do not launch paid infrastructure, publish artifacts, select a legal license, or send external messages merely because this plan describes the eventual workflow. Prepare concrete artifacts within the authorized implementation scope and obtain missing authority where required.

## 4. Architecture and Shared Contracts

These are target contracts to implement or reconcile with existing types, not assertions that the named types already exist. Keep the modular Python application and the existing web stack. Add services or storage products only when a required deployment profile needs them.

### 4.1 Identity, Tenant, and Authorization Context

One trusted `PrincipalContext` must carry subject, issuer, authenticated session/service identity, selected authorized tenant, memberships, roles/scopes, policy version, and request correlation. It must be created by a verified authentication path, not assembled from arbitrary headers.

Tenant selection must validate membership. A supplied tenant selector can select only a tenant the principal is authorized to use; missing/invalid context fails closed. Background jobs and event consumers receive a serialized scope created by a trusted producer and revalidate permissions before sensitive work. Prevent context leakage between concurrent asynchronous requests.

Authorize both action and resource at the service boundary. Transport middleware authenticates; domain authorization protects direct calls from HTTP, MCP, workers, CLI, and scheduled tasks. Cross-tenant administration requires an explicit policy path and audit record.

### 4.2 Persistent Records and Events

For each authoritative record define `tenant_id`, stable ID, schema version, revision, created/updated timestamps, creator, classification, retention, and deletion semantics where applicable. Use composite uniqueness and scoped foreign references. Use optimistic concurrency for editable resources and transactional claims/leases for jobs.

Inventory existing storage ports first. Reuse a compliant transactional adapter; if none exists, add an embedded transactional profile and a server-backed transactional profile appropriate to multi-replica deployment. Select the actual engine in an ADR before implementation. A JSON file with a process-local lock is not the clustered profile.

Persist a domain mutation and its outbox event together. Consumers must deduplicate event IDs and checkpoint progress. Define an event envelope with event ID, type/version, tenant, aggregate ID/revision, actor, correlation/causation IDs, occurred/recorded times, classification, and payload. The target is replay-safe effects under at-least-once delivery; do not claim universal exactly-once transport.

### 4.3 Public API and Client Contract

Each operation must have a unique stable operation ID, owner/tag, version/stability, principal policy, input/output schemas, error schemas, limits, and audit classification. List operations need stable ordering and pagination. Mutation operations need explicit idempotency and concurrency behavior; read-only operations must not acquire unrelated mutation requirements.

Adopt the audit's structured problem-details contract with type, title, status, detail, instance/correlation identifier, and stable application error code. Scrub secrets and internal paths. Use ETag/If-Match where revision conflicts matter. Scope idempotency records to principal/tenant, operation, request digest, and expiration; a reused key with a different payload must conflict.

Generate or validate frontend clients from the canonical specification. Preserve old callers through explicit compatibility adapters or a versioned migration. Do not create a second nearly identical route just to satisfy an audit ID.

### 4.4 Jobs and Streaming

Define job transitions `QUEUED -> RUNNING -> SUCCEEDED | FAILED | CANCELLED`, with retry/held states when required and documented transitions. Include attempt count, lease owner/expiry, progress, cancellability, error code, result reference, tenant scope, and timestamps. Worker death must not permanently strand jobs.

Stream events need a request/run ID, monotonic sequence, event kind, payload schema, and one terminal success/error/cancel event. Support disconnect cleanup, slow consumers, bounded buffers, token/session expiry, and reconnect/replay where promised. Do not measure time-to-first-token from a fully buffered response.

### 4.5 Model, Retrieval, and Evidence Truth

Separate deterministic graph results, model narration, and simulation. Real inference must expose the actual provider/model/version and observed usage when available; unknown metrics stay unknown. Citations identify authorized source evidence, revision, and location. They must resolve at response time and obey later access revocation on retrieval.

Model output is untrusted data. Validate query plans and tool arguments; do not execute generated text directly. Explanations expose evidence, decisions, and bounded rationale, not fabricated internal reasoning or a false mathematical proof of model correctness.

### 4.6 Deployment Profiles

Enumerate the profiles named by source requirements, including local/offline, single-node durable, clustered, and any required managed-cloud/OEM profiles. Each gets a capability matrix, dependency inventory, config schema, startup validation, supported backends, migration path, and acceptance suite.

Use the canonical `GraphStore` contract with HugeGraph as the current reference deployment. Memory is suitable for tests and explicitly labeled transient development use. Other required adapters remain open until real backend conformance passes. Profile-specific optional features cannot silently satisfy mandatory requirements in another profile.

## 5. Phases, Dependencies, and Exit Gates

Package numbers identify ownership, not a strict total ordering. The phase table and explicit prerequisites determine execution order.

| Phase | Work packages | Required exit |
|---|---|---|
| A. Reconcile and stabilize | CP-00, CP-01, CP-02 | All records accounted for; acceptance definitions recovered; reproducible tests and blockers recorded. |
| B. Trusted durable foundation | CP-03 through CP-10 | Real principal, authorization, isolation, safe browser/API boundaries, durable state/jobs, and policy-gated egress pass integration. |
| C. Data and intelligence core | CP-11 through CP-22, CP-37 | Streaming, ontology, graph, ingestion, connectors, temporal/query/retrieval/model/agent behavior passes real service tests. |
| D. Complete product workflows | CP-23 through CP-29 | All required UI, exports, collaboration, offline, branding, and developer workflows use live scoped services. |
| E. Operations and advanced scope | CP-30 through CP-34 | Observability, HA/recovery, performance, packaging/governance, and defined advanced features meet their own measurable gates. |
| F. Release reconciliation | CP-35, CP-36 | Current docs match evidence; final candidate passes all required gates; every open item is disclosed. |

CP-33 license/infrastructure inventory and CP-34 research-definition work begin in Phase A because they have external lead time. Their implementation exits remain in Phase E. CP-30 instrumentation starts with Phase B so later acceptance is observable. UI contract design can begin early, but a UI workflow cannot close before its backend dependencies pass.

Critical dependency paths:

- CP-00 -> CP-02 -> CP-03 -> CP-04 -> CP-05 -> CP-06 -> tenant-safe domain integration.
- CP-07 + CP-10 -> CP-11 -> CP-19/CP-21/CP-22 -> CP-24.
- CP-12 + CP-13 -> CP-15/CP-16 -> CP-17 -> CP-18/CP-20/CP-37.
- CP-03 + CP-06 + CP-10 -> CP-25/CP-26 -> CP-27.
- CP-30 + CP-31 + CP-32 + CP-33 + completed domain packages -> CP-35 -> CP-36.

For parallel execution, isolate package ownership and coordinate changes to `apps/api/main.py`, `apps/api/app.py`, `apps/api/extended.py`, contracts, registry schemas, and CI through one integration owner. Do not have concurrent agents independently redesign shared authentication, tenant context, or database schemas.

## 6. Detailed Work Packages

Each package inherits Section 1.2. Steps below define the implementation order within the package. Existing paths are entry points to inspect, not instructions to rewrite entire files. New types, harnesses, or artifacts named below are proposed deliverables unless explicitly identified as existing.

<a id="cp-00"></a>

### CP-00. Requirement Recovery and Evidence Registry

Priority: P0. Prerequisites: none. Owner: traceability/integration maintainer.

Start in `gaps-audit-cp.md`, `requirements-registry.json`, `requirements-test-map.json`, `scripts/build_requirements_registry.py`, `scripts/verify_requirement_evidence.py`, and `tests/conftest.py`.

1. Parse the Markdown matrix using a table parser or an escape-aware reader. Assert 2,603 unique IDs and 15 columns per baseline row; do not split escaped pipes as new cells.
2. Preserve the source file digest and immutable audit fields. Join existing registry IDs by exact original identifier and separately recover aliases, acceptance IDs, test IDs, phase labels, and role tasks.
3. Resolve each source location to the complete requirement block. Follow references until normative text is found. For `FRD-*` inventory records and undefined moonshot labels, record the missing definition instead of manufacturing one.
4. Decompose compound requirements into measurable clauses, identify applicable profiles, and assign primary/secondary CP owners. Reclassify misleading area/priority labels with a recorded reason.
5. Add schema-versioned fields for source hashes, canonical relationships, public boundaries, applicability, acceptance clauses, test node IDs, evidence hashes, blocker owners, and audit/current statuses. Migrate the existing 944-record registry; do not replace it with an incompatible new list.
6. Remove automatic completion promotion based solely on file/test presence. A verification result must consume real test outcomes and clause-level evidence.
7. Rebuild the current test map from current collection instead of retaining deleted test nodes indefinitely. Keep historical maps as separate run artifacts.
8. Add a coverage validator that fails on orphan audit IDs, duplicate canonical mappings without justification, unresolved source truncation, invalid references, unowned clauses, and unsupported `VERIFIED` status.

Acceptance: exact baseline set equality with Appendix A; every record has a disposition and owner; deleting a required receipt or altering tested source invalidates closure; a skipped/failed test cannot promote a requirement. Gate G0 requires no unresolved engineering definition in the batch entering implementation.

<a id="cp-01"></a>

### CP-01. Decisions, External Prerequisites, and Non-Code Obligations

Priority: P0 for blockers. Prerequisites: CP-00 initial inventory. Owner: integration maintainer with named product, operations, and legal owners.

Read the role documents under `EOIP-engg-doc-pkg/roles/`, `KGF-MASTER-BACKLOG.md`, `super-requirements.md`, and the complete moonshot definitions.

| Decision/prerequisite | Required concrete preparation | Closure authority / evidence |
|---|---|---|
| Supported deployment profiles and adapter matrix | List every required backend, source, auth mode, desktop/offline mode, edition, and environment | Product/architecture scope record; required options retain open tasks until proven. |
| Transactional persistence and event transport | Compare existing ports against concurrency, backup, and offline requirements; prepare schema/ADR and migration plan | Architecture decision plus implemented conformance tests. |
| Identity provider and tenant model | Document issuer/audience, login/session lifecycle, service identities, tenant selection, and role ownership | Configured test identity provider plus signed-principal acceptance. |
| License, notices, redistribution, and OEM rights | Inventory code, dependencies, fonts/assets, model weights, connectors, and commercial restrictions | Authorized owner selects terms; appropriate legal review and approved files. |
| Live SaaS/Hubble/VS Code/cloud acceptance | Build fixtures, accounts/permission matrix, cleanup procedure, resource estimate, and exact test command | Authorized sandbox access and actual passing receipts. |
| Hardware and service targets | Recover latency/throughput/availability/RPO/RTO targets from source; define dataset and workload | Accepted benchmark contract before execution. |
| Undefined or research-grade features | Recover MS-1..10 definitions and measurable targets for LOM/GNN/federated/quantum-inspired/process features | Product/research acceptance charter; absence blocks that feature's closure. |
| Business role tasks | Produce reviewable supporting artifacts where useful; identify actual hiring, partnership, market, or financial decisions | Named business owner confirms the real-world action; code cannot substitute. |

For each unresolved item store the affected audit IDs, exact missing input, prepared artifact path, owner, next action, and resumption test. Continue independent engineering work. Preparing a decision packet is not approving it. Gate: no engineering task relies on an unrecorded decision, and no external obligation is falsely counted as code completion.

<a id="cp-02"></a>

### CP-02. Reliable Test Execution and Evidence Collection

Priority: P0. Prerequisites: CP-00 initial mapping. Owner: QA/infrastructure.

Start in `pyproject.toml`, `tests/conftest.py`, `tests/unit/`, `tests/security/`, `tests/e2e/`, `tests/runtime_hubble/`, `tests/runtime_dlq/`, `.github/workflows/ci.yml`, and `apps/web/playwright.config.js`.

1. Reproduce incomplete full-suite behavior with per-test durations, JUnit, worker/process logs, and bounded diagnostic timeouts. Isolate the reported MCP/subprocess hang and clean up child processes, sockets, and async tasks.
2. Separate pure unit tests from tests requiring databases, model servers, browser, Hubble, external credentials, or extension host. Mark their prerequisites accurately; required release jobs must fail or report blocked when infrastructure is absent.
3. Prevent global environment, singleton, event-loop, and port leakage across tests. Use isolated temporary data directories and explicit dependency teardown.
4. Add acceptance fixtures with at least two tenants, multiple roles, overlapping canonical IDs, real persistence, expired/revoked sessions, and authorized/forbidden resources.
5. Capture immutable run manifests containing collected/executed/passed/failed/skipped counts, test node IDs, timeouts, source revision, dirty-diff digest, dependency versions, and raw artifact hashes.
6. Extend existing CI with contract, security, integration, browser, deployment, and release profiles. Make expensive infrastructure jobs explicit required checks for their release scope.
7. Preserve requirements such as greater than 80% coverage for new components separately from the repository's current Python coverage floor of 70%. Measure meaningful branches and workflows, not just a global number.

Acceptance: a full required suite completes with no unexplained omissions; a deliberately hung subprocess produces a bounded failure and teardown; a failed or skipped required scenario fails the gate; stale requirement map entries cannot count as executed tests. Gate G1 supplies a trustworthy baseline even when it reports existing failures.

<a id="cp-03"></a>

### CP-03. Durable State and Multi-Replica Repositories

Priority: P0. Prerequisites: CP-00, CP-01 persistence decision, CP-02 fixtures. Owner: backend/storage.

Start in `apps/api/extended.py`, `packages/eoip/state/`, `packages/eoip/jobs.py`, and the identity, config, model management, branding, collaboration, reports, graph snapshots, and scheduling packages.

1. Inventory authoritative records separately from caches. For each holder record lifecycle, owner, tenant key, consistency, concurrency, encryption, retention, backup, and current storage.
2. Introduce or extend repository ports for identities/sessions, memberships/policies, settings/flags, model/prompt registries, workspaces/annotations, report metadata/schedules/artifacts, jobs/checkpoints, and saved graph views/snapshots.
3. Implement the selected embedded and clustered adapters with transactions, migrations, unique constraints, compare-and-swap revisions, and bounded queries. Inject repositories through existing factories and application lifespan.
4. Move mutable process-global service instances behind scoped service dependencies. Publish config/policy changes across replicas and invalidate scoped caches by version.
5. Import existing on-disk state through idempotent migration commands with dry-run, validation, backups, and explicit legacy tenant ownership. Never assign ambiguous customer data to a default tenant automatically.
6. Add outbox/inbox persistence needed by CP-10. Define backup consistency across graph, relational metadata, object storage, and derived indexes.

Acceptance: create through API A, read through API B, restart both, and read the same authorized state; concurrent updates either serialize correctly or return a revision conflict; worker crash and migration replay do not duplicate records. Migration failure leaves a recoverable state and an actionable error. Gate G2-storage rejects production profiles using transient authoritative stores.

<a id="cp-04"></a>

### CP-04. Authentication, Sessions, and Principal Propagation

Priority: P0. Prerequisites: CP-02, CP-03 identity/session persistence. Owner: security/backend.

Start in `apps/api/main.py`, `packages/eoip/authn/__init__.py`, `packages/eoip/authn/oauth_sso.py`, and identity-related routers.

1. Consolidate local, OIDC, SAML where required, service-token, and API-key authentication into a trusted principal contract. Use maintained authentication libraries rather than custom signature/protocol implementations.
2. Remove acceptance of arbitrary long opaque strings. Validate issuer, audience, allowed signing algorithms, signature, expiry, not-before, session revocation, and tenant memberships. Handle key rotation with bounded cache behavior.
3. Complete browser login/logout, session renewal, revocation, profile, password/reset/MFA flows where required by the recovered source. For OIDC browser login enforce state, nonce, and PKCE; protect cookie mutations against CSRF.
4. Store secrets/refresh credentials securely and keep long-lived bearer tokens out of browser URLs and insecure persistent storage. Distinguish development bootstrap from production login.
5. Apply the same principal service to HTTP, WebSocket, SSE, MCP, CLI/service access, and scheduled work. Keep truly public health endpoints minimal; restrict metrics/docs/spec according to the deployment policy.
6. Validate webhook signatures, freshness, replay identifiers, and source registration independently of browser login; remove any broad unauthenticated webhook bypass.
7. Replace `local-user` audit attribution with the actual principal and authentication result.

Acceptance: invalid/expired/revoked/wrong-issuer/wrong-audience tokens fail; forged tenant claims fail; logout invalidates protected sessions; key rotation works; WebSocket and MCP use the same identity; webhook replay is rejected. Missing production identity configuration prevents insecure startup.

<a id="cp-05"></a>

### CP-05. Resource Authorization and Administrative Policy

Priority: P0. Prerequisites: CP-04 and CP-03 policy storage. Owner: security/domain maintainers.

Start in `packages/eoip/authz/core.py`, `packages/eoip/authz/security_router.py`, `apps/api/main.py`, and every mounted router/service entry point.

1. Enumerate all operations from the composed runtime app and all non-HTTP tools. Map each to action, resource type, scope, role/attribute policy, and audit event.
2. Enforce deny-by-default policies at the service boundary. Apply resource ownership/classification as well as route-level roles, including raw graph queries, exports, snapshots, model tools, and admin surfaces.
3. Protect role/policy changes against self-escalation; enforce separation of duties and dual control where required. Persist policy versions and invalidate cached grants.
4. Implement field-level filtering/masking consistently for list, detail, search, graph traversal, export, and event payloads. Avoid existence/count leakage for forbidden resources.
5. Audit denials and privileged mutations without exposing credential contents or sensitive object bodies.

Acceptance: table-driven role/action/resource tests plus real route tests cover allowed and denied access; adding an unclassified operation fails CI; worker/MCP calls cannot bypass the policy; a grant revoked on one replica stops access on another.

<a id="cp-06"></a>

### CP-06. Tenant Isolation Across Every Store and Transport

Priority: P0. Prerequisites: CP-03, CP-04, CP-05. Owner: backend/tenancy.

Start in `packages/eoip/enterprise/middleware.py`, `packages/eoip/tenancy/`, `packages/eoip/graph/named_graph.py`, `apps/api/extended.py`, and cache/vector/job/event adapters.

1. Derive the active tenant from a trusted principal and authorized membership; remove caller-controlled fallback to `default` in production requests.
2. Inject the graph/storage dependencies into `TenancyService` and domain services. Prevent unscoped constructors or global stores from serving tenant data.
3. Scope graph vertices/edges/traversals, vector/full-text indexes, file/object paths, caches, jobs, events, exports, report schedules, memories, logs, audit readers, and usage counters.
4. Validate tenant membership at mutation time and again on deferred work execution. Bind job IDs, cursors, download references, and subscription channels to scope.
5. Implement tenant provisioning, suspension, quotas, placement, migration, deletion, retention/legal-hold interaction, and allowed ontology/template sharing. Make raw cross-tenant data sharing impossible through template sharing APIs.
6. Migrate legacy data only with explicit ownership evidence. Record ambiguous data as blocked migration input.

Acceptance: use two tenants in the same API deployment and same real backend, with identical logical IDs. Attempt cross-tenant read/write/search/traversal/export/stream/cache/job/restore access, forged headers, concurrent requests, and role revocation. Separate in-memory test objects are insufficient. Gate G2-isolation requires zero unauthorized cross-tenant observations.

<a id="cp-07"></a>

### CP-07. API Consistency, Metadata, and Client Contracts

Priority: P0. Prerequisites: CP-04..CP-06 contracts agreed; CP-02 harness. Owner: API integration.

Start in `apps/api/main.py`, `apps/api/app.py`, `apps/api/extended.py`, `packages/eoip/contracts/`, and existing SDK/client code.

1. Inventory the actual mounted runtime operations, duplicate routes, unreachable routers, schema conflicts, sync blocking calls, and ambiguous operation IDs. Recheck `platform_router`, reasoning, and collaboration mounting instead of relying on historical counts.
2. Assign owner/tags/stability/security metadata. Add a canonical error handler and typed response models; distinguish unsupported capability, invalid input, unavailable backend, and forbidden access.
3. Apply bounded pagination, deterministic ordering, signed/scoped cursor semantics, filter limits, and maximum expansion sizes to applicable lists/graph APIs.
4. Add idempotency, ETags/revision preconditions, rate-limit scope/headers, cache validators, and retry hints where semantically appropriate. Ensure cache keys include principal/tenant/policy-sensitive variants.
5. Generate/validate one client contract consumed by the web app, SDK, and extension. Register compatibility changes and deprecations with migration tests.
6. Add OpenAPI validation against live startup composition and prevent newly unowned/untagged/unprotected operations in CI.

Acceptance: every public operation has an owner and security classification; malformed, denied, conflict, rate-limit, and backend-failure responses match schemas; clients consume real responses; duplicate operation IDs/routes fail validation.

<a id="cp-08"></a>

### CP-08. Browser Security and Safe Rendering

Priority: P0. Prerequisites: CP-04 browser-session design, CP-07 errors. Owner: frontend/security.

Start in `apps/api/app.py`, `apps/web/src/kgr/export/InteractiveExport.js`, web source rendering paths, and web-server/deployment configuration.

1. Replace wildcard credentialed CORS defaults with explicit validated origins. Test permitted and denied preflights and origin handling on live requests.
2. Replace graph-key/value interpolation through `innerHTML` with safe DOM/text construction. For intentional rich content use a maintained sanitizer with a documented allowlist, safe links, and no active script/event-handler content.
3. Apply CSP with an explicit asset/script policy, frame/embed policy, secure cookie behavior, and Trusted Types where supported and applicable. Handle exported standalone HTML separately so it remains both usable and safe.
4. Inspect Markdown, tooltips, error text, labels, CSV formulas, SVG exports, URL opening, file previews, and code panels for injection and unsafe navigation.
5. Remove credential-bearing URLs and sensitive client logging; bound local storage and clear protected cached state on logout/tenant switch.

Acceptance: graph labels/properties containing HTML/script/URL payloads render inertly in the app and exported artifact; cross-origin credential requests fail as configured; CSP does not break required graph workers; embed mode grants only its intended scope.

<a id="cp-09"></a>

### CP-09. Egress, Secrets, Privacy, and Injection Boundaries

Priority: P0. Prerequisites: CP-04..CP-06. Owner: security/data governance.

Start in `packages/eoip/egress/`, `packages/eoip/privacy/`, `packages/eoip/security/`, `packages/eoip/query/policy.py`, and `tests/security/`.

1. Inventory every outbound network path: connectors, model providers, package installs, report renderers, webhooks, telemetry, browser resources, and redirect-following clients.
2. Require a central policy decision for endpoint, tenant, purpose, classification, consent, and byte budget. Internal/private network sources need explicit configured authorization; cloud metadata and unrelated loopback/private addresses remain denied.
3. Validate destinations after DNS resolution and at every redirect; account for rebinding, alternate IP encodings, proxy environment variables, and user-controlled URLs. Apply connection/read deadlines and response limits.
4. Connect the secret provider to source/model credentials, redact logs/errors, implement rotation and scoped access, and prevent secrets appearing in registry exports or support bundles.
5. Propagate classification into chunks, embeddings, caches, answers, evidence, reports, and notifications. Implement masked responses, audited reveal, retention, erasure, and derived-data cleanup.
6. Parameterize/validate generated queries and tool arguments. Treat documents, graph labels, retrieved text, and model content as data; test prompt injection at the tool/action boundary.

Acceptance: offline mode produces no disallowed egress; prohibited payloads cannot exit through any adapter; secret rotation invalidates old access; deletion removes derived searchable data; malicious redirect/prompt/query payloads fail without unrelated side effects.

<a id="cp-10"></a>

### CP-10. Durable Jobs, Events, Schedules, and Recovery

Priority: P0. Prerequisites: CP-03, CP-06, CP-07. Owner: backend/workers.

Start in `packages/eoip/jobs.py`, `packages/eoip/events/`, `packages/eoip/scheduling/`, ingestion pipelines, and report scheduling.

1. Preserve the existing job API while adding the required state transitions, result references, cancellation, deadlines, retries, and operator-readable failure reasons.
2. Implement transactional job claims, leases, heartbeats, retry backoff/jitter, deduplication, and dead-letter handling for the clustered profile. Define single-worker behavior explicitly for the local profile.
3. Persist mutation/outbox and consumer/inbox state; replay events without duplicate domain effects. Include tenant, actor, policy context, correlation, and schema version.
4. Make long operations checkpointable. Interruptions must resume from a documented point or fail with a safe restart procedure.
5. Implement schedules with explicit timezone, recurrence, missed-run/coalescing policy, and single-execution coordination. Surface status and cancellation through APIs and UI.

Acceptance: kill a worker before/after commit, duplicate a message, replay a checkpoint, race two workers, expire a lease, cancel a running task, and restart the service. Assert no duplicate published record and no permanent orphan job; retries preserve scope and authorization.

<a id="cp-11"></a>

### CP-11. True SSE and WebSocket Delivery

Priority: P0. Prerequisites: CP-04..CP-07, CP-10. Owner: API/realtime.

Start in `packages/eoip/brain/router.py`, `apps/api/main.py`, `packages/eoip/streaming/`, and `apps/web/src/kgr/hooks/useGraphEvents.js`.

1. Replace list-buffered model streaming with incremental transport from the actual provider. Preserve a separate nonstreaming response contract for existing callers.
2. Validate principal/tenant before WebSocket acceptance. Use secure supported session or short-lived handshake credentials; do not put durable tokens in query logs.
3. Publish typed job, graph, agent, collaboration, and model events through the authorized tenant channel. Implement heartbeat, sequence, terminal events, bounded buffers, and reconnect rules.
4. Propagate client cancellation/disconnect to model/query/worker execution. Handle expiry/revocation during a live connection and avoid leaking partial forbidden output.
5. Configure reverse-proxy buffering/timeouts correctly and test through the deployed proxy, not just direct ASGI calls.

Acceptance: a client receives the first chunk before generation completes; delayed later chunks are observable; unauthenticated handshake fails cleanly without 500; slow consumers stay bounded; reconnect cannot replay another tenant's events.

<a id="cp-12"></a>

### CP-12. Ontology, Schemas, Validation, and Governed Publishing

Priority: P0/P1 by source. Prerequisites: CP-03, CP-05..CP-07, CP-10. Owner: ontology/backend.

Start in `packages/eoip/ontology/`, `packages/eoip/graph/schema_migration.py`, `packages/eoip/validation/`, and `apps/web/src/studio/SchemaCanvas.jsx`.

1. Recover entity/edge/schema requirements and reconcile the canonical manifest with all adapters and contracts. Define schema version and compatibility rules.
2. Implement draft -> validate -> review/approve -> publish -> migrate -> active lifecycle, including permissions, immutable published versions, diffs, and rollback/forward repair.
3. Enforce property constraints, cardinality, referential integrity, required provenance, controlled vocabulary, mapping validation, and SHACL/RDF/OWL behavior where specified.
4. Isolate tenant overrides and terminology from canonical identity. Support domain packs and GitOps import/export with deterministic serialization and signed/reviewed changes where required.
5. Wire UI editors to validation diagnostics and real publish jobs. Prevent client-only changes from masquerading as published schemas.

Acceptance: invalid schema/data is rejected with useful field diagnostics; concurrent edits conflict; migration updates data and indexes consistently; failed publish leaves the previous version usable; unauthorized tenants cannot change shared ontology definitions.

<a id="cp-13"></a>

### CP-13. Graph Stores, Algorithms, and Backend Conformance

Priority: P0/P1. Prerequisites: CP-06, CP-07, CP-12 contracts. Owner: graph/backend.

Start in `packages/eoip/graph/store.py`, `backends.py`, `hugegraph.py`, `neo4j.py`, `neptune.py`, `database_adapters.py`, `algorithms.py`, and `community.py` under `packages/eoip/graph/`.

1. Enumerate required backend operations and capability differences: writes, transactions, traversal, path/impact, indexes, schema, query languages, snapshots, tenant namespaces, and bulk loading.
2. Build a backend conformance suite with the same graph fixtures and expected results. Implement missing adapters using their real transport; report unsupported features explicitly.
3. Enforce scoped IDs and traversal boundaries in storage operations; tenant filtering after unrestricted traversal is insufficient.
4. Verify centrality, community detection, similarity, components, k-core, link prediction, anomaly, and path algorithms against known graphs and independently computed expected results. An algorithm label must select that algorithm.
5. Add bounded/cancellable execution, deterministic seeds where applicable, resource limits, progressive subgraph/LOD APIs, and explicit approximation metadata.
6. Reconcile reference HugeGraph behavior with optional backend claims and document tested consistency/transaction limits.

Acceptance: the same tenant-aware contract suite passes on each required actual backend; cycle/disconnected/high-degree graphs terminate within limits; algorithm results meet source tolerances; partial/approximate results are labeled.

<a id="cp-14"></a>

### CP-14. Query Languages, Planning, Federation, and Workbench

Priority: P0/P1. Prerequisites: CP-05..CP-07, CP-12, CP-13. Owner: query/backend.

Start in `packages/eoip/query/`, `packages/eoip/qlang/`, `packages/eoip/federation/`, query contracts, and `apps/web/src/studio/QueryConsole.jsx`.

1. Inventory each documented language and supported grammar. Map parse -> validate -> authorize -> plan -> execute -> explain/profile/cancel, with one typed QueryPlan boundary.
2. Use existing parsers and ASTs; implement allowlists and parameter binding. Enforce depth, expansion, rows, memory, time, read/write mode, and resource access before execution.
3. Unify query status, explain/profile output, warnings, partial-result semantics, and cancellation across endpoints and providers.
4. Implement federation capability negotiation, scoped pushdown, per-site policy, deadlines, circuit breaking, consistent result identities, and explicit unavailable-site diagnostics. Do not silently drop a failed source.
5. Persist saved queries, parameters, history, permissions, and revisions. Wire visual query builders and the workbench to validated backend plans.

Acceptance: malformed/injected/forbidden plans never execute; validate/explain agree with actual execution; cancellation releases backend resources; federated partial failure is visible; saved query sharing does not share credentials or bypass resource policy.

<a id="cp-15"></a>

### CP-15. File Ingestion, Uploads, and Publication Pipelines

Priority: P0/P1. Prerequisites: CP-03, CP-06, CP-09, CP-10, CP-12, CP-13. Owner: ingestion.

Start in `packages/eoip/fileparse/`, `packages/eoip/ingest/`, `packages/eoip/ingestion/`, `packages/eoip/imports/`, and the pipeline/mapping studio.

1. Enumerate required formats, extraction metadata, size limits, parser dependencies, and fidelity expectations. A recognized extension without correct extraction is not support.
2. Add tenant-scoped resumable upload sessions with chunk order/offset, checksums, expiration, quota enforcement, finalization, and cleanup. Stream payloads without unbounded memory buffering.
3. Validate MIME/signature, archive depth/compression ratios, traversal paths, external references, malformed documents, and parser time/memory. Sandbox risky parsers where required.
4. Implement profile -> map -> validate -> preview -> approve -> publish with versioned mappings, provenance, deduplication, rejected-record diagnostics, and replay-safe jobs.
5. Support incremental updates, source deletion/tombstones, checkpoints, schema drift, quarantine/dead-letter review, and rollback of incomplete publication.
6. Connect the UI to live upload/job/progress/review APIs. Report per-file/per-record outcomes rather than a success count disconnected from graph state.

Acceptance: interrupt/resume an upload, restart a parser job, duplicate a file, delete a source, reject hostile archives, and cancel publication. Assert correct graph records and exact source evidence locations for representative required formats.

<a id="cp-16"></a>

### CP-16. Real Connectors, Synchronization, and Source Registry

Priority: P0/P1. Prerequisites: CP-06, CP-09, CP-10, CP-15. Owner: connectors/integrations.

Start in `packages/eoip/connectors/`, `packages/eoip/adapters/`, `packages/eoip/integrations/`, `packages/eoip/ingestion/source_sync.py`, and `apps/web/src/admin/ConnectorSetupWizard.jsx`.

1. Create a source-by-source checklist from all FR-CONN, G2-SRC, SR-CON, and related records: Jira, Git/GitHub/GitLab, Confluence, ServiceNow/knowledge, API catalogs, CI/CD, SBOM, web crawling, databases/files, OpenTelemetry/runtime, Datadog, Grafana, and Kibana where specified.
2. For each source implement authentication/secret references, connectivity checks, pagination, rate limits, retries, checkpoints, incremental cursor/watermark, deletion, schema mapping, and source permissions.
3. Preserve upstream ACLs/classification and stable source identities; propagate scope into the graph and retrieval indexes.
4. Validate webhooks/signatures and scheduled sync. Handle out-of-order events, duplicate delivery, expired credentials, cursor invalidation, and resynchronization without data loss.
5. Add contract tests against controlled fixtures and live sandbox acceptance against each required source. Publish a capability matrix distinguishing fixture-tested from live-verified support.

Acceptance per connector: initial sync, incremental change, deletion, outage/retry, token rotation, permissions change, and restart produce correct graph/provenance state. No connector closes solely because it can parse a sample JSON file. Live receipts remain blocked until actual access is available.

<a id="cp-17"></a>

### CP-17. Entity Resolution, Provenance, Lineage, and Data Quality

Priority: P0/P1. Prerequisites: CP-12..CP-16. Owner: data/identity resolution.

Start in `packages/eoip/identity/`, `packages/eoip/provenance/`, `packages/eoip/quality/`, graph lineage consumers, and ingestion review components.

1. Keep user authentication identity distinct from source entity resolution. Define stable canonical IDs, source aliases, matching rules, and versioned merge/split decisions.
2. Record deterministic/inferred/manual/ambiguous evidence and confidence inputs. Do not collapse ambiguous matches silently or fabricate certainty.
3. Persist provenance for nodes, edges, transformations, model-derived assertions, and changes, including source location/version and extraction method.
4. Implement steward review queues, merge previews, conflict resolution, reversible splits where possible, and downstream index/lineage updates.
5. Add freshness, decay, completeness, duplication, contradiction, trust, and ownership quality rules with explainable diagnostics and remediation jobs.

Acceptance: overlapping names across tenants never merge; late source corrections and deletion propagate through lineage; an evidence link resolves to the actual permitted source; ambiguous matches remain visible until reviewed; repeated ingestion is idempotent.

<a id="cp-18"></a>

### CP-18. Temporal Graphs, Snapshots, Impact, and Incident Workflows

Priority: P0/P1. Prerequisites: CP-10, CP-13, CP-17. Owner: graph/incident analysis.

Start in `packages/eoip/graph/bitemporal.py`, `snapshots.py`, `diff_engine.py`, `playback.py`, `simulation.py`, `packages/eoip/incidents/`, and temporal/change dashboards.

1. Define valid time versus transaction time, timezone normalization, event ordering, late arrivals, revisions, and correction semantics. Keep queryable historical state durable.
2. Implement tenant-scoped snapshots with source/schema versions, retention, checksums, consistent capture, compare/diff, and restore prerequisites.
3. Complete impact/blast radius with depth/type breakdown, bounded traversal, evidence paths, risk inputs, affected owners/tests/services, and uncertainty indicators.
4. Persist investigations and incident workspaces linking alerts, topology, code changes, relevant evidence, and action history. Distinguish causal hypotheses from proven relationships.
5. Implement what-if branches/simulations as isolated state; publishing a change requires normal approval and mutation policy. Wire playback/diff UI to actual versioned data.

Acceptance: as-of queries return correct historical state across late corrections; snapshot diffs are reproducible; simulations never mutate the live graph implicitly; impact calculations stop at tenant/policy boundaries; restart preserves an investigation.

<a id="cp-19"></a>

### CP-19. Real Model Inference, Embeddings, and Model Governance

Priority: P0 for truthful behavior; feature priorities follow sources. Prerequisites: CP-03, CP-06, CP-09, CP-11. Owner: AI/runtime.

Start in `packages/eoip/models/self_llm.py`, `packages/eoip/models/provider.py`, `packages/eoip/brain/`, `packages/eoip/model_management/`, `packages/eoip/mlops/`, and `packages/eoip/evaluation/`.

1. Inventory all routes claiming tokenization, embeddings, inference, confidence, citations, XAI, cognitive tiers, and speculative decoding. Trace each to the executing provider.
2. Confine deterministic simulators to explicitly labeled development/test use. Remove production capability claims until backed by the required runtime. Renaming the simulator is containment, not closure of the real-inference requirement.
3. Extend the existing provider abstraction with model discovery, health, generation, incremental streaming, tokenizer/embedding access, cancellation, usage, limits, and structured failure. Use the actual model's tokenizer and compatible embedding model.
4. Implement model registry persistence, version/artifact digests, licensing references, deployment profiles, resource checks, routing, fallback policy, kill switches, and rollback. Model absence must produce an explicit deterministic/degraded mode or an unavailable error according to the operation contract.
5. Derive citations from authorized retrieval evidence and confidence from defined/calibrated signals; do not synthesize evidence identifiers or claim unmeasured confidence. Explain observable evidence and decisions honestly.
6. For required speculative decoding, implement a real compatible draft/target runtime and measure correctness, accepted-token ratio, latency, and resource usage; never close it with a simulated counter.
7. Evaluate real inference on held-out tasks with evidence correctness, refusal/abstention, injection resistance, latency, cost, and no-egress assertions. Bind results to model/runtime/data versions.

Acceptance: a real configured local runtime generates non-template output; embeddings/token counts match the runtime contract; citations resolve; cancellation stops computation; model downtime is visible; changing the model changes the evidence version. Research-grade quality adjectives require CP-01/CP-34 measurable targets.

<a id="cp-20"></a>

### CP-20. Vector, Full-Text, Hybrid Retrieval, and Search

Priority: P0/P1. Prerequisites: CP-06, CP-09, CP-13, CP-17, CP-19 embedding contract. Owner: retrieval/data.

Start in `packages/eoip/embeddings/`, `packages/eoip/retrieval/`, `packages/eoip/search/`, graph vector adapters, and the SR-VDB source requirements.

1. Implement the canonical vector/search ports: scoped upsert/delete, metadata filters, namespace isolation, kNN, BM25/sparse/hybrid retrieval, facets/highlights, snapshots, rebuild, and model-version tracking.
2. Enumerate every mandated backend separately from optional examples. Complete actual adapters and their authentication/configuration; share conformance fixtures across embedded and remote stores.
3. Enforce authorization during candidate generation/ranking, not merely after returning forbidden top-k matches. Verify index metadata cannot be forged to escape scope.
4. Add chunk/version strategy, embedding model migration, shadow index rebuild, atomic activation, stale-index signaling, source deletion, and erasure propagation.
5. Implement multi-vector/multimodal, configurable indexes/quantization, reranking, and language analyzers where required. Expose approximation/recall tradeoffs as tested capabilities.
6. Preserve graph plus full-text operation without a vector store, with clear degraded semantic capability and no fake vectors.

Acceptance: known relevant results rank correctly on a held-out corpus; denied/deleted documents never surface; rebuild and model switch preserve availability; no-vector mode passes its core acceptance suite; each advertised adapter meets actual recall/latency targets.

<a id="cp-21"></a>

### CP-21. Grounded RAG, Natural-Language Query, and Explanation

Priority: P0/P1. Prerequisites: CP-14, CP-17, CP-19, CP-20. Owner: AI/query.

Start in `packages/eoip/ragx/`, `packages/eoip/query/nlq.py`, `packages/eoip/graph/rag_router.py`, `packages/eoip/truth/`, `packages/eoip/xai/`, and Ask Brain clients.

1. Recover all required RAG/NLQ modes and distinguish distinct algorithms from aliases. Implement the required routing, retrieval, graph expansion, evidence selection, reranking, context budgeting, and output contracts.
2. Translate natural language through a validated query/intent representation. Expose ambiguity clarification, authorized suggestions, query preview, and deterministic versus narrated/exploratory/report modes.
3. Attach sentence/claim-level citations with source revisions and access checks. Detect missing, conflicting, stale, or insufficient evidence and abstain or qualify appropriately.
4. Persist question/run/evidence manifests, safe explanations, feedback, and reproducible configuration. Feedback must not automatically change production policy or training data.
5. Test adversarial retrieved instructions, numeric calculations, multi-hop questions, unsupported questions, multilingual inputs where required, and model/vector outage.

Acceptance: each required mode demonstrates a distinct documented behavior; claims are supported by accessible evidence; a no-evidence question does not get fabricated citations; query budgets and authorization survive generated plans; UI and MCP expose the same evidence semantics.

<a id="cp-22"></a>

### CP-22. Agents, Tools, Memory, Workflows, and Approvals

Priority: P0/P1. Prerequisites: CP-05..CP-11, CP-14, CP-21. Owner: agent platform.

Start in `packages/eoip/agents/`, `packages/eoip/agentarch/`, `packages/eoip/workflows/`, `packages/eoip/memory_eng/`, `packages/eoip/tools_contract/`, and agent routers.

1. Implement a versioned agent contract with input/output schemas, purpose, capabilities, budgets, autonomy mode, risk class, memory scope, approval rules, and evaluation hooks.
2. Enforce tool allowlists, read/write separation, argument validation, tenant/resource authorization, step/token/time limits, loop detection, circuit breaking, and cancellation inside the runtime.
3. Persist run state, events, tool results, approval requests, reviewer decisions, and replay checkpoints. Re-check authorization when executing a delayed approval; bind approval to the exact action/payload/version.
4. Support specified HITL/HOTL/HIC modes and multi-agent coordination through bounded events and evidence. Do not grant peer agents implicit authority from another agent's output.
5. Implement scoped memory lifetimes, inspection, erasure, poisoning defenses, provenance, and consolidation. Prevent memory/search leakage across user/workspace/tenant boundaries.
6. Complete required specialist agents and workflow/RPA hooks through real services. Self-improvement remains proposal/review driven unless explicitly allowed by policy.
7. Connect run timelines, budgets, intervention, retry, and approval UI to the durable runtime.

Acceptance: denied tools never execute; a stale approval cannot authorize a changed payload; worker restart resumes safely; budget exhaustion and cancellation stop further actions; replay does not repeat irreversible actions; memories honor access revocation and erasure.

<a id="cp-23"></a>

### CP-23. Graph Explorer and Visualization Feature Completion

Priority: P0/P1/P2 according to recovered KGR requirements. Prerequisites: CP-07, CP-08, CP-11, CP-13, CP-18. Owner: graph/frontend.

Start in `apps/web/src/kgr/`, `apps/web/src/GraphCanvas.jsx`, graph API contracts, and KGR requirement/implementation documents.

1. Inventory and exercise the required graph types, lenses, layouts, inspectors, filters, and export controls. Preserve shared selection/filter state across graph-type switches and history navigation.
2. Complete the eight inspector views required by the source: properties, relationships, impact, evidence, similarity, history, annotations, and raw data, applying field policy consistently.
3. Verify the specified layout algorithms, centrality radar, blast-radius rings, community hulls/labels, edge bundling, minimap, fisheye, semantic zoom, lasso, hub exclusion, surprise/dead-code indicators, and code navigation against real graph data.
4. Integrate bounded server subgraphs, progressive loading, LOD, cancellation, worker layouts, and stable element identities. Required large-graph scenarios must avoid downloading an unbounded graph to the browser.
5. Complete table/matrix/tree/timeline/Sankey/geo/diff and 2D/3D views only where mandated. Use existing proven renderers and a proper 3D engine for any required 3D surface.
6. Add keyboard/screen-reader alternatives, reduced motion, color-blind/high-contrast modes, responsive controls, clear empty/error/partial/loading states, and persistent saved views.
7. Exercise all controls with browser tests and actual backend calls; inspect desktop/mobile screenshots and nonblank canvas output.

Acceptance: every recovered KGR clause has a working control and observable result; graph changes arrive safely in real time; source thresholds such as 1,000 nodes under two seconds and 50,000/100,000-node scenarios are measured under their separate specified conditions. No visual or performance claim closes from a component name alone.

<a id="cp-24"></a>

### CP-24. Complete Application Screens and End-to-End Navigation

Priority: P0/P1. Prerequisites: CP-04..CP-08 and each screen's domain package. Owner: product/frontend.

Start in `apps/web/src/App.jsx`, `admin/`, `studio/`, `dashboards/`, `cognitive/`, and existing `apps/web/tests/`.

1. Build a screen-to-operation-to-requirement inventory for auth/settings, home/health/jobs, Ask Brain, graph/entity/impact/change, incidents/temporal, query workbench, ontology, sources/ingestion/resolution, agents, reports, collaboration, governance/tenancy/branding, and platform health.
2. Complete shared authenticated client behavior, tenant switching, role-aware navigation, routing/deep links, loading/error/empty/denied/partial states, and recoverable forms.
3. Connect each command to real typed endpoints and durable state. Remove hardcoded success/results from production paths; explicit demo mode must never satisfy production acceptance.
4. Provide consistent job progress/cancellation, conflict resolution, evidence inspection, destructive-action preview/approval, and notification navigation across screens.
5. Implement persona homes, onboarding, settings, mobile answers/alerts/approvals, and accessibility requirements with source-specific assertions.
6. Test navigation into and out of every view, direct deep links after restart, expired sessions mid-action, tenant changes, and real backend outages.

Acceptance: screen coverage has no required orphan feature; each primary workflow succeeds against a real scoped backend; denied roles cannot invoke hidden actions directly; no UI displays completion while the backend job failed or remains pending.

<a id="cp-25"></a>

### CP-25. Reports, Stored Artifacts, and Graph Export Formats

Priority: P0/P1. Prerequisites: CP-03, CP-06..CP-10, CP-17, CP-18. Owner: reporting/frontend.

Start in `packages/eoip/reports/generator.py`, `router.py`, `schedule.py`, `packages/eoip/exporters/`, graph format conversion, and `apps/web/src/kgr/export/`.

1. Replace 501 report export paths with durable report records and actual renderers. Persist template/version, parameters, source revision, generator version, actor/tenant, status, checksum, content type, artifact reference, and expiry.
2. Implement HTML, Markdown, JSON, PDF, DOCX, and PPTX for the required report templates. Use existing maintained document libraries where available, add explicit optional dependencies/runtime packaging as needed, and generate actual valid binary documents.
3. Return usable download/stream responses with correct content type, filename, size, integrity, authorization, and missing/expired-artifact errors. Prevent path traversal and unauthorized shared links.
4. Complete recurring generation through CP-10, including timezone, missed runs, concurrency, failure alerts, parameters, and authorized delivery.
5. Implement each specified graph format separately: PNG, SVG, PDF, JSON-LD, GraphML, CSV, GEXF, Obsidian, Mermaid, Cypher, clipboard, and interactive HTML as required. Preserve IDs, types, direction, evidence, Unicode, and classification according to the format contract.
6. Enforce privacy/masking on the server's export dataset and safe rendering in interactive artifacts. Branding must use the authorized tenant's versioned theme.

Acceptance: open every document with an independent parser/renderer and inspect representative rendered pages/slides; validate graph exports by parsing/round-trip where possible; stored reports survive restart; tenant B cannot download tenant A's report; no required format returns 501 or contains a placeholder instead of the requested content.

<a id="cp-26"></a>

### CP-26. Collaboration, Notifications, and Shared Investigations

Priority: P1/P2, with P0 scope/privacy dependencies. Prerequisites: CP-03, CP-05..CP-08, CP-10, CP-11. Owner: collaboration.

Start in `packages/eoip/collaboration/`, `packages/eoip/notifications/`, `packages/eoip/moonshot/collaborative_crdt.py`, and annotation/workspace UI.

1. Persist workspaces, memberships, comments, annotations, mentions, saved/shared queries, views, activity, and notification preferences with revision control.
2. Enforce sharing scope, object-level permissions, revocation, and classification. Notifications must not reveal a resource to a recipient who cannot read it.
3. Implement real-time presence and updates with bounded ephemeral presence state and durable changes. Reconnect replays authorized events only.
4. Where concurrent editing is required, specify convergent operations and adopt a proven CRDT/OT implementation as appropriate; distinguish supported collaborative fields from exclusive-edit fields.
5. Implement in-app read/unread, subscriptions, digest scheduling, delivery retries/deduplication, and approved email/webhook integrations. External messages require configured recipient policy and credentials.

Acceptance: concurrent edits converge or produce a documented conflict; restart preserves shared work; lost connections recover without duplication; revoking membership stops future events and downloads; mentions do not leak private content.

<a id="cp-27"></a>

### CP-27. Offline, Desktop, Synchronization, and Edge Profiles

Priority: source-defined. Prerequisites: CP-03, CP-06, CP-09, CP-10, CP-24, CP-26 where shared edits apply. Owner: local/edge platform.

Start in `packages/eoip/edge/`, synchronization adapters, local deployment scripts, web persistence, and the source's offline/desktop requirements.

1. Distinguish a locally hosted server from browser offline support and a packaged desktop application. Implement each only under its explicit contract; none substitutes for another.
2. Define allowed offline reads/mutations, encrypted/scoped cache, authenticated unlock, data expiry, queued operations, base revision, idempotency, and local quota.
3. Implement reconnect handshake, server authorization revalidation, ordered replay, conflict detection/resolution, tombstones, and index refresh. Reject a queued mutation whose authority was revoked while offline.
4. Support documented conflict behavior for graph edits, annotations, and settings. Never merge security policy changes automatically.
5. For required desktop/edge distribution, implement installation, isolated data roots, safe update/rollback, model/dependency availability, and platform-specific smoke tests.

Acceptance: disconnect, perform allowed work, restart the client, reconnect, and reconcile against concurrent remote edits without data loss or scope leakage. Offline mode emits no forbidden requests; logout/tenant switch clears protected cached access.

<a id="cp-28"></a>

### CP-28. Administration, Configuration, Branding, Localization, and OEM

Priority: P0/P1 by source. Prerequisites: CP-03..CP-09, CP-24. Owner: platform/frontend.

Start in `packages/eoip/config/`, `packages/eoip/branding/`, `packages/eoip/tenancy/`, `packages/eoip/licensing/`, billing/metering, and admin UI.

1. Complete typed layered configuration, secret references, validated import/export, audited revisions, effective-value provenance, feature flags, policy floors, and cross-replica propagation.
2. Implement durable tenant/user/role lifecycle, quotas, entitlements, partner administration, metering, and support access. Prevent an unlicensed or misconfigured production install from silently using permissive development entitlement keys.
3. Apply versioned theme tokens, assets, terminology, persona labels, assistant branding, legal/help content, and domain-specific visual styles consistently across UI, login, errors, reports, and notifications.
4. Implement required custom-domain ownership verification, certificate lifecycle, SSO routing, email templates, and embedding token scope. Reject host/header tricks that select another tenant.
5. Externalize UI strings and implement language packs, pluralization, dates/numbers, RTL, glossary translation, accessibility, and fallback behavior.
6. Prepare the OEM rebuild/re-sign/update pipeline, removable vendor identifiers where legally permitted, partner fleet console, and embedded widgets. Coordinate legal/commercial choices with CP-33.

Acceptance: a second tenant's theme/config does not bleed into the first; updates survive restart and appear on another replica; a locale/RTL run has no clipped controls or untranslated required strings; custom-domain traffic resolves to the correct authorized tenant; entitlement enforcement matches approved product policy.

<a id="cp-29"></a>

### CP-29. MCP, VS Code, SDK, CLI, Plugins, and Developer Experience

Priority: P0/P1 by source. Prerequisites: CP-04..CP-07, CP-14, CP-17, CP-22, CP-37 as applicable. Owner: developer tools.

Start in `apps/vscode-extension/`, the actual MCP app discovered under `apps/`, `packages/eoip/sdk/`, `packages/eoip/cli.py`, `packages/eoip/plugins/`, and `packages/eoip/marketplace/`.

1. Generate tool/command inventories from registered code and package manifests. Reconcile all required search, context, impact, path, lineage, retrieval, source navigation, change, conformance, tests, incident, ADR, and telemetry commands.
2. Apply the same principal/tenant/policy contract to MCP and SDK/CLI requests. Keep read-only discovery/query tools separate from approved action tools; preserve budgets and typed errors.
3. Complete cancellation, pagination, evidence/resource links, streaming, reconnect, and version compatibility. Fix subprocess lifecycle defects contributing to test hangs.
4. Validate source URI/path mapping, workspace boundaries, line ranges, and missing files in the VS Code extension. Store credentials in the host's secure mechanism.
5. Run extension-host tests with an actual backend, not just JavaScript unit imports. Package/install the extension and exercise contributed commands.
6. Implement required plugin manifest/version/signature, permissions, sandbox, install/upgrade/uninstall rollback, and certification lifecycle. A package signature establishes origin, not safe execution.
7. Publish runnable SDK/CLI examples and contract tests generated from the current supported surface.

Acceptance: each required command/tool produces the same authorized domain result as the web/API path; malformed tool calls and workspace-escape links fail safely; real extension-host tests pass; a denied plugin capability cannot reach network/filesystem/graph operations.

<a id="cp-30"></a>

### CP-30. Observability, Runtime Topology, SLOs, and Support

Priority: P0/P1. Prerequisites: CP-04, CP-06, CP-10; instrument other packages as they are built. Owner: operations/observability.

Start in `packages/eoip/observability/`, `packages/eoip/telemetry/`, `packages/eoip/audit/`, `packages/eoip/health/`, `packages/eoip/graph/runtime_topology.py`, and `tests/runtime_hubble/`.

1. Propagate trace/correlation/run IDs across API, jobs, connectors, model providers, graph, and exports; preserve principal/tenant attribution without leaking sensitive values into telemetry labels.
2. Add golden-signal metrics, saturation/queue depth, connector lag, graph/index freshness, model latency, policy denials, job failures, and SLO burn alerts with bounded cardinality.
3. Consolidate readiness/liveness/dependency health and platform topology. A downstream failure must produce accurate degraded status and operational diagnostics.
4. Implement required Hubble/runtime ingestion and source-bound topology-to-code links using live runtime data. Distinguish observed dependencies from inferred mappings.
5. Provide redacted support bundles, audit querying/export, retention, tamper evidence, dashboards, and tested runbooks.

Acceptance: a real browser/connector request can be followed through its workers and stores; injected backend failure triggers the intended alert; secrets are absent from logs/traces/bundles; live Hubble records map to the correct source revision and tenant.

<a id="cp-31"></a>

### CP-31. Deployment, Migrations, Backup, Restore, HA, and DR

Priority: P0 for production claims. Prerequisites: CP-03, CP-06, CP-10, CP-30. Owner: operations/storage.

Start in `deploy/`, container scripts, `scripts/backup.py`, `scripts/restore.py`, `scripts/verify_restore.py`, `scripts/verify_recovery_bundle.py`, and recovery modules.

1. Define reproducible local, durable single-node, clustered, and required cloud profiles with pinned artifacts, config validation, secret injection, readiness, resource limits, and non-root hardening.
2. Refuse production startup with transient stores, default vendor keys, missing identity settings, unsafe CORS, or unsupported required capabilities. Keep developer setup explicit and separate.
3. Implement ordered versioned migrations for graph/schema, metadata, job/event, config, model registry, and index changes. Use expand/contract compatibility and rehearse N-1 to N upgrade.
4. Implement consistent encrypted backups with manifest, checksums, key handling, tenant ownership, object/graph/config/model dependencies, and restore verification into an empty isolated target.
5. Exercise API/worker/backend node failure, lease loss, rolling upgrade, network partition, storage outage, and restart. Document actual topology limits and prevent split-brain writes.
6. Automate restore and DR drills with measured RPO/RTO, integrity checks, source/evidence resolution, tenant access, job state, and index rebuilding.
7. Prepare rollback or forward-repair procedures and test them with representative persistent data. Never perform a destructive restore against a user's working deployment as an acceptance shortcut.

Acceptance: a clean target recovers a usable authorized application within source targets; no acknowledged committed data is lost beyond the agreed RPO; final topology survives required failures; rolling upgrade and repair retain client compatibility. Simulated dictionaries do not satisfy HA/DR gates.

<a id="cp-32"></a>

### CP-32. Performance, Scalability, Capacity, and Cost

Priority: P0/P1 by profile. Prerequisites: CP-13..CP-24, CP-30, CP-31 reference topology. Owner: performance/QA.

Start in `packages/eoip/graph/benchmark.py`, `scripts/benchmark.py`, `scripts/benchmark_data.py`, `tests/performance/`, web rendering code, and non-functional source requirements.

1. Create a target table linking each latency, throughput, concurrency, graph-size, memory, availability, and cost requirement to hardware, dataset, topology, warm/cold state, and measuring method.
2. Cover skewed/high-degree graphs, large uploads, incremental ingestion, vector rebuild, concurrent queries, long streams, export jobs, tenant quotas, and slow consumers.
3. Measure p50/p95/p99, failures/timeouts, throughput, CPU/RAM/GPU/disk/network, queue growth, time-to-first-token, cancellation latency, and browser responsiveness under defined load.
4. Optimize evidenced bottlenecks: indexes, query plans, bulk writes, bounded caching, LOD, worker layout, batching, backpressure, concurrency limits, and streaming. Re-run the relevant workload after each change.
5. Add soak tests and resource-leak checks. Verify fairness so one tenant cannot consume every worker, query slot, or memory budget.
6. Publish reproducible reports and regression budgets; preserve separate thresholds from different requirements instead of averaging them into a passing score.

Acceptance: every applicable source target passes on its declared profile; runs include raw measurements and dataset hashes; memory remains bounded during a soak; cancellation and overloaded-system behavior are measured; unavailable hardware leaves the corresponding claim unverified.

<a id="cp-33"></a>

### CP-33. Licensing, Compliance Evidence, Supply Chain, and Distribution

Priority: P0 for redistribution; source-defined elsewhere. Prerequisites: CP-01 decisions; CP-09 and CP-31 controls for technical evidence. Owner: packaging/security with legal/commercial owners.

Start in `packages/eoip/licensing/`, `packages/eoip/compliance/`, `packages/eoip/billing/`, package manifests, lockfiles, deployment images, and `EOIP-engg-doc-pkg/69-dependency-license-sbom.md`.

1. Inventory first-party ownership, third-party dependencies/assets, transitive packages, containers, parsers, graph/vector engines, plugins, and model weights. Record versions, licenses, source URLs, provenance, and redistribution constraints.
2. Prepare root LICENSE/NOTICE and package metadata only after the authorized rights holder selects terms. Do not infer an open-source license from dependency licenses or a pricing requirement.
3. Generate SBOMs for actual distributable artifacts; scan dependency vulnerabilities, secrets, and license policy; sign/provenance-bind releases where required.
4. Implement approved entitlement, edition, offline-license, usage-metering, billing-export, and OEM rules with tamper detection and clear error/recovery behavior. Do not equate technical entitlement enforcement with legal approval.
5. Produce controls/evidence for privacy, retention, audit, residency, access reviews, disaster recovery, and applicable assurance programs. Maintain an obligation-to-control-to-test matrix.
6. Route patent/trademark/contracts/privacy notices/certification and business commitments to qualified owners with prepared evidence. Certification requires the actual authorized external assessment, not a passing internal test.

Acceptance: artifacts have approved license/notice/provenance, reproducible SBOMs, and required scans; enforcement is tested across editions and offline profiles; outstanding legal/certification obligations remain explicitly open until owner evidence exists.

<a id="cp-34"></a>

### CP-34. Advanced Intelligence, Learning, and Research Features

Priority: source-defined; definition work starts in Phase A. Prerequisites: CP-01 acceptance charter, CP-13, CP-17..CP-22, CP-30, CP-32. Owner: AI/research/domain specialists.

Start in `packages/eoip/moonshot/`, `gnn/`, `causal/`, `distillation/`, `intelligence_eng/`, `graph_loop/`, `graph_graph/`, `loops/`, and the full MS/AI/AIDLC/SDLC requirements.

1. Build a family-by-family charter rather than treating all advanced modules as one capability. Recover any missing MS-1..10 definitions and preserve all existing IDs.
2. For LOM/foundation/GNN training and inference define datasets, licensing, train/validation/test splits, baseline, metrics, hardware, artifact versioning, reproducibility, inference API, and regression gates.
3. For federated/privacy-preserving learning define the threat model, participant identity, allowed data movement, aggregation, privacy accounting where promised, failure/dropout behavior, and measurable leakage/quality criteria.
4. For quantum-inspired optimization use actual defined algorithms and compare solution quality/runtime to classical baselines. The name is not proof of improvement or quantum capability.
5. For digital twins, causal reasoning, process intelligence and OCEL requirements define event semantics, ground-truth fixtures, uncertainty, scenario isolation, replay, and action approval.
6. For memory immune systems, autonomous maintenance, integrity sentinels, knowledge debt, distillation, self-improvement, and reflective workflows define threat/failure corpora, bounded proposals, review, rollback, and false-positive/quality metrics.
7. For verifiable reasoning chains distinguish cryptographic integrity of evidence/tool traces from correctness of a model's reasoning. Implement and test only the guarantee actually specified.
8. Connect each accepted capability to durable jobs, versioned model/data artifacts, tenant policy, API/tool/UI contracts, and live evaluations. A heuristic scaffold cannot close a learned-model requirement.

Acceptance: every advanced feature has a recovered definition, real implementation, application integration, held-out evaluation, failure cases, and reproducible receipts. Failed experiments remain open findings. Do not turn an unbounded claim such as "frontier-grade" into a passing string-comparison test.

<a id="cp-35"></a>

### CP-35. Documentation, Current Status, and Maintainability

Priority: P0 for accurate release claims. Prerequisites: CP-00 registry, package evidence. Owner: documentation/integration.

Start in `README.md`, root/package status pages, `KGF-MASTER-BACKLOG.md`, engineering guides, API/SDK docs, and current requirements generators.

1. Generate counts, route/tool/command inventories, supported backends, tested profiles, and status summaries from one validated registry plus real receipts. Show audit baseline and current status separately.
2. Update current architecture, configuration, authentication, tenant, API, ingestion, model, report, offline, plugin, deployment, recovery, and troubleshooting guides as packages close.
3. Resolve all six source-audit document conflicts with dated decisions. Keep historical audits intact and label their snapshot context; correct current claims and links.
4. Document previously under-described polyglot query semantics, broad completion-module ownership, process-state lifetime, and API ownership. Split modules only where it improves actual maintenance boundaries.
5. Validate local Markdown links, anchors, commands, environment variables, code paths, generated schemas, and public examples. Reconcile root and engineering-package copies atomically.
6. Apply architecture fitness checks, code ownership, typed interfaces, dependency layering, change notes, and support/deprecation policy according to the recovered maintenance/SDLC requirements.

Acceptance: current docs make no unsupported completion claim; generated numbers agree; required commands execute in their stated environment; links resolve; obsolete module names and historical test counts are not presented as current capabilities.

<a id="cp-36"></a>

### CP-36. Final Acceptance, Independent Re-Audit, and Release Evidence

Priority: P0. Prerequisites: all applicable package exits; CP-35 current docs. Owner: release integration/QA.

1. Freeze a release candidate identified by code commit/tree digest, dependency locks, container/package/model artifacts, schema version, configuration profile, and dataset versions. Receipt-only documentation commits must still identify the exact tested code artifact.
2. Execute every required test layer and external acceptance gate. Use the real composed application, production-equivalent persistence, browser client, tools/extension, connectors, model runtime, and operational topology.
3. Run the source audit's REL-01..REL-15 gates and any recovered additional gates. An aggregate GAP/G2 scanner pass is supplemental traceability evidence only.
4. Verify receipts independently: check exit status, artifact hashes, test identity, required assertions, infrastructure/profile, timestamps, source compatibility, and absence of unexplained skips or fabricated defaults.
5. Re-audit requirement-by-requirement. Ensure baseline IDs are all reconciled, canonical engineering requirements are all verified, aliases have valid evidence, and new findings are registered and resolved.
6. Publish a closeout report separating engineering completion, integration readiness, externally owned obligations, supported profiles, measured limits, migrations, and rollback.
7. Prepare release notes/packages. Publishing, deployment, and tagging require the authority applicable to the actual requested release action; preparing this plan does not itself authorize a production rollout.

Acceptance: exact scope/evidence reconciliation with no unresolved required engineering clauses; all required candidate gates pass; externally blocked items prevent an overall completion claim unless their scope was explicitly and transparently changed by its owner. Never issue an unconditional "100% production-ready" verdict from this plan alone.

<a id="cp-37"></a>

### CP-37. Code Graph, Engineering Domains, Runtime Semantics, and Catalogs

Priority: P0/P1 by source. Prerequisites: CP-12..CP-18; CP-30 runtime ingestion for live correlation. Owner: graph/domain engineering.

Start in `packages/eoip/codegraph/`, `packages/eoip/graph/engineering.py`, `conformance.py`, `test_intelligence.py`, `business_intent.py`, `api_contracts.py`, `process_mining.py`, `packages/eoip/catalog/`, and `packages/eoip/systems/`.

1. Enumerate required code languages, symbol/AST relationships, repository/version metadata, and source location fidelity. Test actual parsers on language-specific fixtures; string matching does not establish semantic parser coverage.
2. Connect requirements, decisions, source symbols, tests, builds, deployments, runtime services, incidents, owners, and business processes through evidence-backed edges.
3. Implement required architecture conformance, dependency drift, impacted-test selection, dead-code/orphan discovery, knowledge debt, bus-factor/expertise, release/change risk, and domain-specific graph analyses.
4. Complete the documented engineering disciplines, graph families, metadata/catalog discovery, domain packs, and system registry contracts. For each analysis define inputs, algorithm, provenance, confidence/limits, output schema, and UI/tool consumers.
5. Reconcile static code with observed runtime/API/security/process graphs and explain mismatches. Preserve source revision and avoid presenting inferred relationships as observed facts.
6. Propagate incremental repository changes, rename/delete, deployment version changes, and evidence erasure without stale links or duplicated canonical entities.

Acceptance: a source change can be traced through its requirement/test/build/deployment/incident chain with correct locations; language fixtures produce expected semantic edges; conformance findings are reproducible; live runtime correlation uses the deployed revision; every required domain result is accessible through its public API and intended client.

### Specialized Engine and SDLC Instructions

The following instructions supplement the owning CP packages. They prevent the phase-4 engine families from being treated as generic AI work. Read the original acceptance block for each parent and every `.1`, `.2`, or `.A1` child; early references in the audit sometimes contain only an overlap-table summary.

| Source family | Owner / supporting packages | Concrete implementation and acceptance |
|---|---|---|
| CORE-001 token formats | CP-19, CP-07, CP-32 | Implement all required serializers/deserializers through the established token-format port; preserve types, escaping, Unicode, nulls, nested values and schema versions. Fuzz round trips, bound recursive/decompression inputs, reject unsupported types explicitly, and measure claimed token reductions with actual target tokenizers on representative payloads. |
| CORE-002 guardrails | CP-09, CP-22 | Wire static/dynamic verification before and after model/tool/loop boundaries; policy failures must stop the action. Test bypass attempts, conflicting rules, safe diagnostics and exact downstream effects. |
| CORE-003 intent routing | CP-19, CP-21, CP-32 | Route from a typed intent to real supported engines/providers with policy and budget constraints. Implement shadow evaluation, deterministic fallback and versioned routing decisions; measure routing quality, latency and cost claims against a fixed baseline. |
| CORE-004 graph-over-graph | CP-13, CP-14, CP-37 | Implement the defined graph composition/meta relationships, identity mapping, scoped traversal and provenance across graphs. Test overlapping IDs, missing graphs, cycles and updates through public APIs. |
| CORE-005 loop-over-loop | CP-22, CP-10 | Persist nested loop state, parent/child budgets, approvals, convergence/stall criteria and cancellation. Replay cannot re-execute committed actions; child loops cannot exceed parent authority or budget. |
| CORE-006 token budgeting | CP-22, CP-19, CP-33 | Use one versioned token/cost model for reservations, observed usage, release/refund, limits and metering. Test concurrent reservations, unknown provider usage, partial streams, retries and tenant fairness; keep currency/price assumptions explicit. |
| AGENT-001 boundary telemetry | CP-30, CP-22 | Instrument actual boundary transitions with trace identity, redacted metadata and measurable cognitive/task signals. Validate event provenance, missing events, detection quality, overhead and privacy. |
| AGENT-002 / AI-002 / AI-003 extraction | CP-15, CP-17, CP-20 | Establish one owned NLP -> relation/triple -> entity/community pipeline, preserving source offsets and confidence. Test language detection, NER, coreference/relations where required, topic models, schema validation and entity resolution using labeled corpora and precision/recall targets. |
| AGENT-003 / AGENT-004 messaging and fan-out | CP-22, CP-10 | Implement correlated typed messages, bounded parallelism, cancellation, deadlines, aggregation and partial failures. Duplicate/out-of-order messages and worker loss must not lose results or duplicate effects. |
| AI-001 explanations | CP-21, CP-34 | Connect actual model/graph features to explanation outputs; test factor attribution, uncertainty, calibration and human-readable evidence. Explanation fidelity needs evaluated behavior, not a constant importance dictionary. |
| AI-004 / AI-005 experiments | CP-19, CP-03, CP-09 | Persist experiment parameters, datasets, prompts, metrics, artifacts and lineage. Implement reproducible splits, A/B assignment, canary/shadow deployment, promotion thresholds and rollback; prevent test-set leakage and scope data by tenant. |
| AI-006 embeddings | CP-20 | Pin model/dimension/version metadata, invalidate incompatible indexes, re-embed safely and validate recall after activation. Remove vectors and caches when source data is erased. |
| AI-007 probabilistic reasoning | CP-34 | Implement the specified probabilistic model, evidence updates and uncertainty propagation; compare to known distributions and held-out calibration, including missing/conflicting evidence. |
| GRAPH-001 federation | CP-14 | Exercise real multi-source planning, capability negotiation, authorization, joins, identities, timeout and partial results; an adapter registry alone is insufficient. |
| GRAPH-002..004 causal/distillation/GNN | CP-34, CP-19 | Define data, model/algorithm, baseline, training or inference path, output contract and quality thresholds separately. Produce versioned artifacts and public integration rather than treating all three as heuristic graph traversal. |
| GRAPH-005 temporal/hybrid retrieval | CP-20, CP-18 | Combine time constraints and hybrid ranking without returning inaccessible or temporally invalid evidence; evaluate retrieval relevance and historical correctness together. |
| GRAPH-006 OWL/SHACL | CP-12 | Use suitable reasoning/validation libraries for the declared subset, expose unsupported constructs, bound inference, detect inconsistency and test standards fixtures at the stated scope. |
| MULTI-001 multimodal | CP-34, CP-15, CP-23 | Implement actual supported diagram/image/document inputs and graph-to-image outputs. Measure extracted structure/location fidelity on labeled inputs; bound parsers and inspect rendered artifacts. |
| MULTI-002 memory graphs | CP-22, CP-17, CP-18 | Persist scoped episodic/semantic graph memory, consolidation and retention with provenance; test temporal recall, poisoning, deletion, access revocation and restart. |
| INFRA-001 caches | CP-03, CP-06, CP-32 | Implement the required cache tiers, scoped keys, consistency/TTL, invalidation, stampede control and failover. Never serve a result after access revocation or from another tenant's cached query. |
| INFRA-002..007 infrastructure | CP-04, CP-07, CP-10, CP-29..CP-31 | Complete SSO, GitOps delivery, log aggregation, distributed scheduling, versioned API/SDK and automated recovery as real deployments; require their respective package receipts. |
| UI-001..009 interface systems | CP-23..CP-26, CP-28 | Integrate shared design components, i18n, data grids, charting, exports, workflow builder, missing lenses, search analytics and collaboration with the actual backend. Test component states, virtualization, filters/sort, live data, accessibility and real workflows. |
| SDLC-001..009 architecture/governance | CP-00, CP-01, CP-06..CP-10, CP-22, CP-28, CP-31 | Deliver traceability gates, ADRs, threat cases, typed engine registration, tenant scope, kill switches, ordered migrations, human work queues with SLA/escalation, and bounded resilience. Assert each mechanism at the composed app boundary. |
| SDLC-010..019 quality | CP-02, CP-24, CP-32, CP-35 | Add the required lint/type/layering checks, changed-code coverage, realistic synthetic datasets, deterministic fixtures, mutation testing for critical logic, coding-agent rules, platform dogfooding, SDK contracts, browser regression and leak tests. Set explicit baselines and fail on real regressions. |
| SDLC-020..031 operations | CP-06, CP-09, CP-27, CP-30..CP-33 | Maintain compatibility matrix, continuous security checks, signed/SBOM releases, production cluster profile, air-gapped bundles, telemetry/SLOs, measured cost claims, encryption/retention/erasure, tenant isolation and hardware-specific benchmarks. |
| SDLC-032..034 documentation/procurement | CP-29, CP-33, CP-35 | Build docs-as-code checks, tested developer bootstrap, versioned CLI/setup material, and procurement evidence including accessibility results. Procurement/legal acceptance remains an external-owner obligation when required. |
| AIDLC-001..016 governance and evaluation | CP-00, CP-01, CP-04, CP-09, CP-19..CP-22, CP-33, CP-34 | Recover actual definitions before coding; implement shared evaluations, red-team/quality gates, prompt/model promotion and rollback, unified cost accounting, feedback, fine-tuning, sandbox enforcement, agent/workload identity and SCIM where specified, governance and evidence UX. Test provisioning/deprovisioning, sandbox escape/exhaustion, blocked promotion, and rollback through live services. |

Do not treat a parent family mapping as automatic closure for its children. If a child adds a UI, persistence, privacy, performance, or external acceptance obligation, add the relevant secondary CP package and its assertions.

## 7. Validation, Evidence, and Agent Handoff

### 7.1 Acceptance Test Matrix

The paths below distinguish existing test locations from proposed suites. Proposed suites must be implemented before their commands are added to required CI. Reuse an existing meaningful test when it already asserts the complete behavior.

| Layer | Location / target | Minimum assertions | Required receipt |
|---|---|---|---|
| Registry and source integrity | Existing registry scripts, plus proposed CP schema/index validator | Exact audit ID coverage; recovered complete clauses; valid aliases; no stale-test closure | Source/index digest, validation report, canonical counts |
| Unit | Existing `tests/unit/` | Algorithms, state transitions, validation, deterministic edge cases, error handling | JUnit, exact node IDs, relevant coverage |
| API contract | Proposed composed-app contract suite | Every mounted operation has metadata/security/error contracts; real serialized responses match | OpenAPI digest, client contract results |
| Security | Existing `tests/security/`, expanded integration fixtures | Principal validation, RBAC/ABAC, tenant attacks, SSRF, XSS, query/prompt injection, secret redaction | Threat-case results, negative assertions, configuration |
| Storage/backend conformance | Proposed shared adapter conformance suite | Scoped CRUD/query, transactions, concurrency, restart, capabilities, migration | Backend versions, fixture hashes, result logs |
| Domain integration | Extend existing integration tests | Actual route/tool -> service -> store -> worker -> result behavior | Input/output evidence and persisted state checks |
| Browser | Existing `apps/web/tests/` with additional workflows | Live network calls, actual data changes, role/tenant behavior, error/retry/cancel, keyboard/mobile states | Playwright report, traces, screenshots, console/network failures |
| Artifacts | Proposed report/export acceptance suite | Valid files opened by independent consumers; content/evidence/branding/masking correct | File checksums, parser checks, rendered page/slide review |
| Model/evaluation | Existing evaluation modules with real runtime harness | Real generation/embeddings, grounding, abstention, latency, injection resistance | Model/data/runtime hashes, metrics and failure examples |
| Tools and extension | MCP transport tests; actual VS Code host suite | Authentication, command/tool results, cancellation, source navigation, secure tokens | Tool transcript, host logs, packaged extension digest |
| Live sources/runtime | Existing Hubble/DLQ suites; per-connector sandbox harness | Initial/incremental/delete/retry/restart/permission behavior | Redacted live receipt, upstream version, source-to-graph evidence |
| Recovery/HA | Existing isolated acceptance deployment and recovery scripts | Restore, rolling migration, failover, partition, backup integrity, scoped access | Topology, fault timeline, measured RPO/RTO |
| Performance | Existing `tests/performance/` and benchmarks | Individual source targets, tails, throughput, resource bounds, fairness, soak | Raw results, workload/hardware/dataset profiles |
| Distribution | Built packages/images/model bundles | SBOM/license/scan/signature/config correctness, install and upgrade | Artifact digests and policy report |

Use both happy-path and adversarial assertions. For stateful requirements, include restart and multi-replica tests. For UI requirements, backend tests alone are insufficient. For hardware, live connectors, certification, or disaster recovery, a unit-test simulation is only a prerequisite.

### 7.2 Existing Commands and Their Limits

Run commands from the repository root unless otherwise stated. These are inspected entry points, not a claim that they have passed during plan creation. Install the repository's locked/supported development dependencies in the project's selected environment before running them. Capture nonzero exit codes; do not replace failing commands with a success message.

```powershell
git status --short
git rev-parse HEAD
python -m pytest --collect-only -q
python -m pytest tests/unit -q
python -m pytest tests/security -q
python -m pytest -q --junitxml=test-results/cp-full.xml
npm --prefix apps/web ci
npm --prefix apps/web run build
```

Create the evidence output directory before invoking reporters that require it. Current collection writes a requirement map only when explicitly passed `--requirements-map=requirements-test-map.json`; ordinary runs no longer update it. Use `--run-evidence=test-results/run-receipt.json` for source-bound execution outcomes. A collection map is not passing evidence. See the dated change audit for the remaining CP-00/CP-02 verification limitations.

For browser execution, use the existing project configuration from `apps/web` and a real running application. Replace the example local port with the actual isolated test deployment; the existing config's default is a container hostname.

```powershell
# Working directory: apps/web
$env:PLAYWRIGHT_BASE_URL = 'http://127.0.0.1:8080'
npx --no-install playwright test --config=playwright.config.js
```

Do not invent `npm test`, `test:e2e`, or a release CLI that is not registered. Add new scripts only when implementing their harnesses and document their exact arguments. Dependency setup and browser installation may require network access; use the approved offline artifact process for an offline profile.

Existing recovery scripts use real graph/data/config/model state. Read their arguments and isolate the target before running them. Existing GAP/G2 scanners, registry generators, and `ProductionReleaseGate` remain useful tools but must be checked for semantic evidence validation; a JSON field saying `PASSED` is not independently sufficient.

### 7.3 Receipt Schema and Trust Rules

Extend the existing receipt types instead of creating an unrelated incompatible evidence system. A completed receipt must contain at least:

```json
{
  "schema_version": "cp-receipt-v1",
  "task_id": "CP-06.001",
  "requirement_ids": ["REQ-TEN-001"],
  "acceptance_clause_ids": ["REQ-TEN-001.AC01"],
  "code_commit": "resolved-full-commit-sha",
  "working_tree_digest": "sha256-of-tested-source-manifest",
  "artifact_digests": {},
  "profile": "named-test-profile",
  "dependency_versions": {},
  "dataset_digest": "sha256-of-fixture-manifest",
  "started_at": "ISO-8601 timestamp with offset",
  "finished_at": "ISO-8601 timestamp with offset",
  "command": "exact executed command without secrets",
  "exit_code": 0,
  "test_node_ids": [],
  "counts": {"collected": 0, "executed": 0, "passed": 0, "failed": 0, "skipped": 0},
  "asserted_outcomes": [],
  "artifacts": [],
  "limitations": [],
  "verdict": "BLOCKED"
}
```

This is a schema illustration, not an execution receipt. Keep verdict blocked until actual execution supplies valid data. Store receipts under a consistent run directory, for example `test-results/cp/<run-id>/`, and define durable CI artifact retention. Hash raw outputs; reject missing artifacts, missing required assertions, altered source, default `HEAD` strings instead of resolved revisions, contradictory counts, and untrusted manually asserted success.

A test may support several requirements only when its assertions cover every mapped clause. Require reviewers to explain shared coverage. Code changes after a receipt invalidate affected evidence; a final candidate suite re-establishes integration across all packages.

### 7.4 Example Fully Specified Acceptance Cases

| Case | Setup and action | Required observation | Packages |
|---|---|---|---|
| Cross-tenant graph access | Create the same logical node ID in tenants A/B in one deployed backend; authenticate as A; try B's header, node ID, cursor, export ID, and stream channel | No B data, counts, evidence, or event leaks; denial is audited with A's actual principal | CP-04..CP-06, CP-11 |
| Durable settings conflict | Read revision R on clients A/B; A saves R+1; B submits stale R; restart both APIs | B receives a conflict; A's state persists; client can reload/reconcile | CP-03, CP-07, CP-28 |
| Streaming cancellation | Use a real provider with delayed chunks; read the first event, then cancel | First event precedes completion; no full buffering; provider work stops; one documented terminal outcome | CP-11, CP-19 |
| Stored report download | Generate a PDF/DOCX/PPTX from scoped graph data; restart API; download as owner and then another tenant | Valid parseable artifact, correct type/contents/checksum/branding, durable download, denied other tenant | CP-25, CP-28 |
| Connector replay | Sync a real sandbox source, kill worker after commit before checkpoint, restart, replay, then delete source record | One canonical result, consistent provenance/checkpoint, correct tombstone and retrieval removal | CP-10, CP-15..CP-17 |
| Grounded answer | Ask a supported question, then an unanswerable one; include malicious instructions in a retrieved document | First answer cites authorized source spans; second abstains/qualifies; retrieved instructions cannot trigger tools | CP-09, CP-19..CP-22 |
| Offline revoked authority | Queue an allowed edit while offline; revoke membership on server; reconnect | Server rejects replay; client explains conflict and removes forbidden cached access | CP-05, CP-06, CP-27 |
| Clean-target restore | Back up graph, metadata, objects, config, and index manifests; restore to an empty isolated stack | Checksums, authorized workflows, evidence links, job recovery, and measured RPO/RTO meet target | CP-03, CP-31 |

Expand these examples into exact fixture data, expected values, endpoint/tool names, and test node IDs once CP-00 recovers the individual source requirement. Do not copy illustrative requirement IDs onto unrelated tests.

### 7.5 Session Handoff and Resumption

For each completed work session record: revision/dirty diff, selected audit/canonical IDs, implementation paths, migrations/config changes, exact commands and results, receipt paths, unverified clauses, blockers with owners, next unblocked package, and rollback notes. A new agent reads this handoff and the registry before starting; it must not infer completion from a previous assistant's prose.

The reusable execution instruction is:

> Implement the earliest unblocked batch in `gaps-audit-cp-implementation-plan.md`. Read each complete source requirement and current code first. Reuse existing behavior where proven; complete missing domain, storage, API/tool, UI, worker, and deployment integration. Follow the shared security and persistence contracts. Verify every applicable acceptance clause with real execution and attach receipts. Preserve unrelated changes and historical evidence. Record unresolved external inputs, continue independent work, and report exact verified scope without claiming unsupported completion.

## 8. Audit Finding Crosswalk

The matrix does not exhaust the audit's prose findings. The following mappings make Sections 1 and 5 through 10 of the audit explicit work, even when a finding has no standalone normalized REQ ID.

### 8.1 Top Ten Findings

| Audit finding | Execution packages | Closure proof |
|---|---|---|
| Shared token / no enterprise principal | CP-04, CP-05 | Real sessions/identities and consistent resource decisions across all transports |
| Caller-controlled tenant / ineffective isolation | CP-03, CP-06 | Adversarial multi-tenant acceptance in one deployment/store |
| Simulator presented as Self-LLM | CP-19, CP-21, CP-34 | Real runtime, truthful semantics, validated evidence and quality evaluation |
| Process-local enterprise state | CP-03, CP-10, CP-26, CP-28 | Restart/concurrency/replica consistency across authoritative records |
| Broad inconsistent API | CP-07, CP-29 | Complete operation inventory, contracts, clients, and policy checks |
| Report/export 501 paths | CP-25 | Independently parseable stored artifacts and authorized downloads |
| Buffered streaming / unsafe WebSocket | CP-04, CP-06, CP-11 | Incremental deployed transport, auth, scope, cancellation and reconnect |
| CORS/CSP/HTML rendering weaknesses | CP-08, CP-09 | Browser security tests and inert hostile exported content |
| Missing operational/live evidence | CP-02, CP-16, CP-29..CP-32, CP-36 | Actual live connector/browser/host/HA/performance receipts |
| Missing root license / redistribution clarity | CP-01, CP-33 | Authorized license choice and complete artifact notices/SBOM |

### 8.2 Non-Functional Domains

| Audit domain | Primary closure packages |
|---|---|
| Authentication and authorization | CP-04, CP-05 |
| Tenant isolation | CP-06 with CP-03 and every data consumer |
| Secrets, SSRF, query/prompt injection, LLM data sharing | CP-09, CP-14, CP-19, CP-22 |
| Local-first and offline | CP-27, CP-31 |
| Distribution and HA | CP-03, CP-10, CP-31 |
| Scalability | CP-13, CP-20, CP-23, CP-32 |
| Observability | CP-30 |
| Privacy | CP-09, CP-17, CP-20, CP-25, CP-26 |
| Backup/restore | CP-31 |
| Upgrade/migration | CP-03, CP-12, CP-31 |
| Licensing | CP-01, CP-33 |

### 8.3 Conflicts, Undocumented Features, and Technical Debt

| Audit identifier / observation | Required resolution | Owner packages |
|---|---|---|
| CONFLICT-001: completion headline vs missing release receipts | Show verified scope and separate blocked release gates; regenerate headline only from validated evidence | CP-00, CP-35, CP-36 |
| CONFLICT-002: 944/826/893 registry counts | Preserve baseline counts and generate current counts from the migrated canonical registry | CP-00, CP-35 |
| CONFLICT-003: 167/516 vs 516/516 status | Date historical snapshots; atomically update current status from one data source | CP-35 |
| CONFLICT-004: mandatory HugeGraph vs multi-backend claims | Canonical GraphStore plus reference profile and per-backend conformance/capabilities | CP-01, CP-13, CP-31 |
| CONFLICT-005: report support vs 501 | Real render/store/download implementation and artifact tests | CP-25 |
| CONFLICT-006: frontier-grade Self-LLM vs deterministic simulation | Accurate capability labeling, real runtime, required evaluations | CP-19, CP-34, CP-35 |
| UNDOCUMENTED-001: polyglot query semantics | Supported grammars, planning/security/partial-result guarantees, public API documentation | CP-14, CP-35 |
| UNDOCUMENTED-002: broad enterprise completion module | Capability ownership, support tier, durable lifecycle and actual public integration | CP-00, owning domain packages, CP-35 |
| UNDOCUMENTED-003: process-local registry lifetimes | Explicit repository/lifetime contracts and durable production adapters | CP-03, CP-35 |
| UNDOCUMENTED-004: blank operation tags | Owner/tag/stability/security metadata and CI enforcement | CP-07 |
| Circular completion machinery | Requirement/acceptance/receipt validation rather than file existence | CP-00, CP-02, CP-36 |
| 452 in-memory assignments | Classify actual authoritative state before changing it | CP-03 |
| Inconsistent pagination/errors/rates/cache/idempotency | Apply operation-specific canonical contracts | CP-07 |
| Buffered streaming | Incremental transport with deployed timing evidence | CP-11 |
| Unsafe HTML composition | Safe rendering and export injection tests | CP-08, CP-25 |
| Tests assert fabricated intelligence | Tests of real runtime, source evidence, calibration, and held-out quality | CP-19, CP-21, CP-34 |

### 8.4 GUI Readiness Crosswalk

| Audit screen area | Required packages before workflow closure |
|---|---|
| Auth and settings | CP-03..CP-08, CP-24, CP-28 |
| Home, health, jobs | CP-10, CP-24, CP-30 |
| Ask Brain | CP-11, CP-14, CP-19..CP-21, CP-24 |
| Graph Explorer, Entity 360, Impact, Change | CP-13, CP-17, CP-18, CP-23, CP-24 |
| Incidents and temporal | CP-18, CP-24, CP-30, CP-37 |
| Query Workbench | CP-14, CP-24 |
| Ontology and meta graph | CP-12, CP-13, CP-24 |
| Sources, ingestion, resolution | CP-15..CP-17, CP-24 |
| Agents | CP-10, CP-11, CP-22, CP-24 |
| Reports | CP-24, CP-25 |
| Collaboration and notifications | CP-11, CP-24, CP-26 |
| Governance, tenants, white-label | CP-04..CP-09, CP-24, CP-28, CP-33 |
| Platform health | CP-24, CP-30, CP-31 |

### 8.5 Explicit Stubbed and Blocked Records

| Audit ID | Original ID | Required treatment |
|---|---|---|
| REQ-ONT-001 | AC-09 | CP-25: validate every named graph export format; this is not solely ontology work. |
| REQ-ONT-002 | AC-27 | CP-25: prove the exact required export coverage and clipboard behavior. |
| REQ-LLM-005 | DERIVED-LLM-SELF-001 | CP-19 + CP-34: real inference, defined XAI/speculative behavior and accepted quality target. |
| REQ-NLQ-009 | SR-NLQ-008 | CP-25 + CP-10: all report templates, parameters, schedules, stored downloads and formats. |
| REQ-SEC-125 | SR-WL-002 | CP-28 + CP-04 + CP-25: domain/TLS/login/email/report branding; exporter alone cannot close it. |
| REQ-UI-075 | UI-005 | CP-25 + CP-24: functioning PDF/CSV user workflow. |
| REQ-UI-076 | UI-005.1 | CP-25: actual PDF graph report and rendered-content checks. |
| REQ-NFR-078 | CG-GAP-008 | CP-36 plus all external gate owners: collect actual live receipts. |
| REQ-UI-011 | G2-P10 | CP-23 + CP-24 + CP-31 + CP-32: full phase requirements and operational evidence; phase label needs decomposition. |
| REQ-OPS-027 | REL-10 | CP-31 + CP-36: real production-profile HA, backup/restore and disaster-recovery evidence. |

## 9. Release Closeout Checklist

- [ ] Baseline audit digest is preserved and every one of its 2,603 IDs remains accounted for.
- [ ] All truncated/inventory-only definitions are recovered or explicitly unresolved; unresolved required behavior prevents full closure.
- [ ] Original/current priorities, aliases, parent-child clauses, profile applicability, and external-owner records are explicit.
- [ ] Every canonical engineering requirement passes all applicable acceptance clauses through its public application boundary.
- [ ] No required real capability is implemented only as a simulator, stub, sample loader, unmounted router, or static UI.
- [ ] Authentication, authorization, tenant isolation, secrets, privacy, browser security, and egress protections are integrated across all transports.
- [ ] Authoritative state survives restart; multi-replica claims have concurrency and shared-storage proof.
- [ ] Streaming, exports, connectors, model inference, agent actions, offline sync, and developer tools have actual integration receipts.
- [ ] Full required Python tests, browser tests, security checks, adapter tests, and artifact checks pass on the release candidate.
- [ ] Required external connectors, Hubble, VS Code host, production HA/restore/DR, and performance targets have actual receipts.
- [ ] Migrations and recovery are rehearsed, and supported deployment/backend/profile matrices match measured behavior.
- [ ] Current docs, generated counts, API/tool inventories, links, examples, and support limits match the evidence.
- [ ] License/notice, supply-chain artifacts, and required non-code approvals are complete or explicitly block the broader readiness claim.
- [ ] Independent final reconciliation finds no missing audit IDs, unsupported completion states, hidden skips, or unregistered newly found gaps.
- [ ] Closeout states engineering completion, release readiness, and external obligations separately, with links to reproducible receipts.

Only after these checks pass for the accepted scope may an agent report 100% verified implementation. A narrower milestone can be reported earlier, with its exact denominator and remaining work.

## Appendix A. Complete Requirement Execution Index

This index is mechanically derived from all 2,603 matrix rows in the source audit. It preserves normalized ID, original ID/title, source location, baseline priority/status, an initial CP owner, and a starting action. The audit title is reproduced as recorded, including existing abbreviations. Read the complete cited source before implementing.

The CP assignment is a triage aid based on the ID family, recorded subject, and audit area, not a claim that semantic classification is complete. CP-00 must confirm it and add secondary packages wherever a requirement spans services. No row is closed by its routing assignment. All rows also inherit CP-00 traceability, CP-02 verification, CP-35 documentation, and CP-36 final reconciliation.

Action key: `PROVE` = demonstrate or repair existing implementation; `COMPLETE` = close missing clauses; `REPLACE` = replace stub; `TRACE/BUILD` = find equivalent behavior before building; `UNBLOCK` = finish the acceptance harness and resolve the external prerequisite. Non-engineering or ambiguous source records must first receive the CP-00/CP-01 disposition regardless of this baseline action.

<!-- BEGIN REQUIREMENT INDEX -->

### A.1 Coverage and Routing Summary

| Audit area | Records | Initial CP owners (record counts) |
|---|---:|---|
| ADM | 43 | CP-01: 2; CP-02: 2; CP-06: 1; CP-16: 1; CP-23: 1; CP-25: 5; CP-28: 24; CP-33: 7 |
| AGT | 120 | CP-00: 1; CP-01: 2; CP-06: 2; CP-09: 1; CP-15: 9; CP-17: 2; CP-18: 2; CP-22: 77; CP-23: 4; CP-29: 7; CP-30: 7; CP-32: 1; CP-33: 2; CP-34: 2; CP-35: 1 |
| API | 22 | CP-00: 1; CP-01: 2; CP-02: 2; CP-07: 8; CP-16: 6; CP-22: 1; CP-29: 1; CP-31: 1 |
| CON | 122 | CP-05: 2; CP-07: 1; CP-09: 4; CP-12: 4; CP-13: 1; CP-14: 5; CP-15: 1; CP-16: 62; CP-17: 4; CP-20: 1; CP-21: 2; CP-22: 1; CP-23: 1; CP-27: 1; CP-29: 3; CP-30: 1; CP-31: 1; CP-32: 4; CP-33: 7; CP-34: 13; CP-36: 2; CP-37: 1 |
| DEV | 143 | CP-00: 10; CP-01: 6; CP-02: 17; CP-07: 3; CP-09: 8; CP-10: 3; CP-12: 2; CP-13: 2; CP-14: 1; CP-15: 2; CP-16: 2; CP-17: 11; CP-18: 2; CP-22: 4; CP-23: 1; CP-24: 5; CP-27: 1; CP-29: 10; CP-30: 2; CP-31: 2; CP-32: 9; CP-33: 2; CP-34: 1; CP-35: 31; CP-37: 6 |
| GRA | 307 | CP-01: 6; CP-02: 3; CP-03: 2; CP-07: 2; CP-09: 10; CP-10: 1; CP-11: 1; CP-12: 6; CP-13: 67; CP-14: 13; CP-15: 5; CP-16: 4; CP-17: 6; CP-18: 5; CP-19: 1; CP-20: 15; CP-21: 6; CP-22: 8; CP-23: 40; CP-24: 1; CP-25: 2; CP-26: 2; CP-27: 2; CP-28: 1; CP-29: 7; CP-30: 3; CP-31: 3; CP-32: 4; CP-33: 7; CP-34: 36; CP-35: 3; CP-37: 35 |
| IMP | 9 | CP-01: 1; CP-02: 1; CP-18: 4; CP-29: 2; CP-35: 1 |
| ING | 117 | CP-00: 2; CP-02: 1; CP-09: 1; CP-10: 4; CP-13: 3; CP-15: 80; CP-16: 3; CP-17: 2; CP-18: 1; CP-21: 1; CP-23: 1; CP-25: 1; CP-29: 3; CP-30: 1; CP-31: 1; CP-32: 3; CP-33: 4; CP-34: 3; CP-35: 1; CP-37: 1 |
| LIN | 41 | CP-09: 1; CP-15: 1; CP-17: 27; CP-20: 1; CP-21: 4; CP-22: 1; CP-25: 2; CP-32: 1; CP-33: 2; CP-35: 1 |
| LLM | 38 | CP-09: 2; CP-18: 1; CP-19: 28; CP-21: 1; CP-22: 1; CP-25: 1; CP-32: 1; CP-33: 2; CP-34: 1 |
| LOC | 12 | CP-03: 1; CP-10: 2; CP-13: 1; CP-16: 1; CP-27: 6; CP-31: 1 |
| NFR | 919 | CP-00: 328; CP-01: 32; CP-02: 20; CP-03: 3; CP-04: 3; CP-06: 5; CP-07: 3; CP-09: 27; CP-10: 12; CP-12: 11; CP-13: 10; CP-14: 13; CP-15: 17; CP-16: 56; CP-17: 18; CP-18: 15; CP-19: 20; CP-20: 5; CP-21: 12; CP-22: 26; CP-23: 25; CP-24: 6; CP-25: 6; CP-27: 4; CP-28: 7; CP-29: 21; CP-30: 27; CP-31: 17; CP-32: 22; CP-33: 22; CP-34: 76; CP-35: 6; CP-36: 7; CP-37: 37 |
| NLQ | 16 | CP-14: 1; CP-21: 14; CP-25: 1 |
| OBS | 44 | CP-00: 1; CP-01: 1; CP-02: 2; CP-16: 1; CP-19: 3; CP-22: 1; CP-29: 1; CP-30: 29; CP-31: 2; CP-33: 2; CP-35: 1 |
| ONT | 96 | CP-02: 1; CP-07: 4; CP-12: 51; CP-13: 4; CP-16: 1; CP-17: 7; CP-18: 3; CP-21: 1; CP-22: 1; CP-23: 2; CP-25: 5; CP-27: 1; CP-28: 3; CP-29: 6; CP-30: 1; CP-31: 1; CP-32: 2; CP-34: 2 |
| OPS | 47 | CP-01: 2; CP-06: 1; CP-10: 1; CP-13: 1; CP-18: 6; CP-19: 2; CP-28: 1; CP-30: 8; CP-31: 22; CP-33: 2; CP-36: 1 |
| QRY | 74 | CP-07: 2; CP-11: 1; CP-13: 3; CP-14: 57; CP-18: 3; CP-19: 1; CP-22: 1; CP-23: 2; CP-29: 1; CP-32: 1; CP-34: 1; CP-35: 1 |
| RAG | 48 | CP-00: 1; CP-09: 1; CP-20: 4; CP-21: 37; CP-23: 1; CP-25: 1; CP-32: 3 |
| SCL | 31 | CP-02: 1; CP-03: 2; CP-19: 2; CP-20: 1; CP-30: 1; CP-32: 22; CP-34: 1; CP-36: 1 |
| SEC | 169 | CP-00: 1; CP-01: 2; CP-02: 1; CP-04: 7; CP-05: 5; CP-06: 1; CP-07: 1; CP-08: 2; CP-09: 112; CP-10: 2; CP-18: 2; CP-20: 1; CP-22: 3; CP-23: 1; CP-28: 3; CP-29: 1; CP-31: 6; CP-32: 2; CP-33: 7; CP-34: 1; CP-35: 2; CP-36: 3; CP-37: 3 |
| TEN | 23 | CP-06: 15; CP-09: 1; CP-16: 2; CP-28: 2; CP-31: 1; CP-32: 1; CP-33: 1 |
| TMP | 39 | CP-01: 2; CP-02: 1; CP-07: 3; CP-12: 1; CP-13: 2; CP-15: 1; CP-16: 1; CP-18: 11; CP-19: 1; CP-21: 1; CP-22: 1; CP-23: 1; CP-24: 1; CP-25: 1; CP-28: 1; CP-29: 4; CP-31: 1; CP-32: 1; CP-33: 3; CP-37: 1 |
| UI | 104 | CP-02: 1; CP-12: 3; CP-14: 1; CP-16: 5; CP-17: 1; CP-18: 8; CP-20: 5; CP-22: 7; CP-23: 8; CP-24: 37; CP-25: 6; CP-26: 6; CP-28: 7; CP-29: 2; CP-32: 2; CP-33: 1; CP-35: 2; CP-36: 1; CP-37: 1 |
| VEC | 17 | CP-10: 2; CP-13: 1; CP-15: 1; CP-16: 1; CP-20: 9; CP-33: 3 |
| WLB | 2 | CP-28: 2 |
| Total | 2,603 | Every record has exactly one initial owner; add secondary owners during CP-00. |

### A.2 ADM: 43 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-ADM-001` | `AC-20`: &#124; AC-20 &#124; Annotations on nodes/edges persist and export with reports &#124; No free competitor has this &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1051`; audit line 118 | UNSTATED | MISSED | [CP-25](#cp-25) | subject triage | TRACE/BUILD |
| `REQ-ADM-002` | `AC-FR-ADMIN-001`: &#124; FR-ADMIN-001 &#124; Admin UI &#124; WP-EXPERIENCE &#124; TEST-FR-ADMIN-001 &#124; AC-FR-ADMIN-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:78`; audit line 147 | UNSTATED | MISSED | [CP-28](#cp-28) | ID family | TRACE/BUILD |
| `REQ-ADM-003` | `AC-FR-ADMIN-002`: &#124; FR-ADMIN-002 &#124; Admin UI &#124; WP-EXPERIENCE &#124; TEST-FR-ADMIN-002 &#124; AC-FR-ADMIN-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:79`; audit line 148 | UNSTATED | MISSED | [CP-28](#cp-28) | ID family | TRACE/BUILD |
| `REQ-ADM-004` | `AIDLC-002.3`: - [ ] `AIDLC-002.3` Quality comparison report before cutover | `eoip-phase4-2-requirements.md:2072`; audit line 307 | UNSTATED | MISSED | [CP-25](#cp-25) | subject triage | TRACE/BUILD |
| `REQ-ADM-005` | `AIDLC-003.2`: - [ ] `AIDLC-003.2` Resolution quality reported | `eoip-phase4-2-requirements.md:2090`; audit line 311 | UNSTATED | MISSED | [CP-25](#cp-25) | subject triage | TRACE/BUILD |
| `REQ-ADM-006` | `CG-GAP-002`: Add the reports root route (PIC-010) | `EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:63`; audit line 388 | P1 | PARTIAL | [CP-25](#cp-25) | subject triage | COMPLETE |
| `REQ-ADM-007` | `COMPLY-001.3`: - [x] `COMPLY-001.3` Violation reporting with remediation | `eoip-phase4-2-requirements.md:1168`; audit line 399 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-ADM-008` | `FR-ADMIN-001`: Admin ingestion UI | `EOIP-engg-doc-pkg/03-functional-requirements.md:645`; audit line 504 | P0 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-009` | `FR-ADMIN-002`: Admin graph quality UI | `EOIP-engg-doc-pkg/03-functional-requirements.md:655`; audit line 505 | P0 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-010` | `FR-KGR-008`: ### FR-KGR-008: Annotation & Collaboration | `EOIP-engg-doc-pkg/KGR-requirements.md:373`; audit line 550 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-ADM-011` | `G2-ADMIN-001`: G2-ADMIN-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1090`; audit line 623 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-012` | `G2-ADMIN-002`: G2-ADMIN-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1554`; audit line 624 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-013` | `G2-ADMIN-003`: G2-ADMIN-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1557`; audit line 625 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-014` | `G2-ADMIN-004`: G2-ADMIN-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1560`; audit line 626 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-015` | `G2-ADMIN-005`: G2-ADMIN-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1563`; audit line 627 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-016` | `G2-ADMIN-006`: G2-ADMIN-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1566`; audit line 628 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-017` | `G2-ADMIN-007`: G2-ADMIN-007 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1569`; audit line 629 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-018` | `G2-ADMIN-008`: G2-ADMIN-008 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1572`; audit line 630 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-019` | `G2-ADMIN-009`: G2-ADMIN-009 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1575`; audit line 631 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-020` | `G2-ADMIN-010`: G2-ADMIN-010 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1578`; audit line 632 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-021` | `G2-ADMIN-011`: G2-ADMIN-011 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1581`; audit line 633 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-022` | `G2-ADMIN-012`: G2-ADMIN-012 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1584`; audit line 634 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-023` | `G2-ADMIN-013`: G2-ADMIN-013 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1587`; audit line 635 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-024` | `G2-ADMIN-014`: G2-ADMIN-014 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1590`; audit line 636 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-025` | `G2-ADMIN-015`: G2-ADMIN-015 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1593`; audit line 637 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-026` | `G2-ADMIN-016`: G2-ADMIN-016 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1596`; audit line 638 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-027` | `G2-ADMIN-017`: G2-ADMIN-017 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1599`; audit line 639 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-028` | `GAP-KGCI-002`: GAP-KGCI-002: Machine-readable report | `EOIP-engg-doc-pkg/gaps-requirements.md:821`; audit line 1366 | P0 | IMPLEMENTED-UNVERIFIED | [CP-25](#cp-25) | subject triage | PROVE |
| `REQ-ADM-029` | `SDLC-011.1`: - [ ] `SDLC-011.1` Coverage report in CI | `eoip-phase4-2-requirements.md:1602`; audit line 1835 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-ADM-030` | `SDLC-014.3`: - [ ] `SDLC-014.3` Survivor report | `eoip-phase4-2-requirements.md:1659`; audit line 1852 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-ADM-031` | `SDLC-022.2`: - [ ] `SDLC-022.2` SBOM and license report per release | `eoip-phase4-2-requirements.md:1806`; audit line 1891 | UNSTATED | MISSED | [CP-33](#cp-33) | engine family | TRACE/BUILD |
| `REQ-ADM-032` | `SDLC-030.4`: - [ ] `SDLC-030.4` Reports per engine | `eoip-phase4-2-requirements.md:1958`; audit line 1933 | UNSTATED | MISSED | [CP-06](#cp-06) | engine family | TRACE/BUILD |
| `REQ-ADM-033` | `SDLC-034`: - [x] `TEST-005.A2` Accessibility conformance report output for procurement (SDLC-034). *(added by review)* | `eoip-phase4-2-requirements.md:1316`; audit line 1949 | UNSTATED | MISSED | [CP-33](#cp-33) | engine family | TRACE/BUILD |
| `REQ-ADM-034` | `SDLC-034.4`: - [ ] `SDLC-034.4` Accessibility conformance report | `eoip-phase4-2-requirements.md:2032`; audit line 1953 | UNSTATED | MISSED | [CP-33](#cp-33) | engine family | TRACE/BUILD |
| `REQ-ADM-035` | `SR-CON-007`: &#124; SR-CON-007 &#124; **Clean-room and license-clean:** study external products and papers for ideas only; produce an independent implementation, SBOM and license report per release. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:104`; audit line 2011 | P0 | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-ADM-036` | `SR-WL-004`: &#124; SR-WL-004 &#124; **De-vendoring:** vendor identifiers removable from UI, docs, CLI binary names, container/image names, package names, API hostnames, error pages and installers; "powered by" is a licensed toggle. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:736`; audit line 2238 | P0 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ADM-037` | `TASK-CEO-002`: - **TASK-CEO-002**: Validate $14.4B TAM with market research and analyst reports | `EOIP-engg-doc-pkg/roles/CEO_tasks.md:18`; audit line 2275 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-ADM-038` | `TASK-DM-008`: - **TASK-DM-008**: Weekly status reports to CEO/CTO with burndown, risks, blockers | `EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:52`; audit line 2328 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-ADM-039` | `TASK-LEGAL-007`: - **TASK-LEGAL-007**: Draft Enterprise License Agreement (ELA) for Professional/Enterprise/OEM tiers | `EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:48`; audit line 2373 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-ADM-040` | `TASK-LIC-002`: - **TASK-LIC-002**: Implement license enforcement for Phase 4 features in code | `EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:17`; audit line 2383 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-ADM-041` | `TASK-LIC-012`: - **TASK-LIC-012**: Maintain dependency license inventory — track all third-party licenses and renewal dates | `EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:64`; audit line 2393 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-ADM-042` | `TEST-FR-ADMIN-001`: &#124; FR-ADMIN-001 &#124; Admin UI &#124; WP-EXPERIENCE &#124; TEST-FR-ADMIN-001 &#124; AC-FR-ADMIN-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:78`; audit line 2488 | UNSTATED | MISSED | [CP-28](#cp-28) | ID family | TRACE/BUILD |
| `REQ-ADM-043` | `TEST-FR-ADMIN-002`: &#124; FR-ADMIN-002 &#124; Admin UI &#124; WP-EXPERIENCE &#124; TEST-FR-ADMIN-002 &#124; AC-FR-ADMIN-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:79`; audit line 2489 | UNSTATED | MISSED | [CP-28](#cp-28) | ID family | TRACE/BUILD |

### A.3 AGT: 120 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-AGT-001` | `AC-FR-AGENT-001`: &#124; FR-AGENT-001 &#124; Agent Runtime &#124; WP-AGENT-MEMORY &#124; TEST-FR-AGENT-001 &#124; AC-FR-AGENT-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:68`; audit line 149 | UNSTATED | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-002` | `AC-FR-AGENT-002`: &#124; FR-AGENT-002 &#124; Agent Runtime &#124; WP-AGENT-MEMORY &#124; TEST-FR-AGENT-002 &#124; AC-FR-AGENT-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:69`; audit line 150 | UNSTATED | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-003` | `AC-FR-AGENT-003`: &#124; FR-AGENT-003 &#124; Agent Runtime &#124; WP-AGENT-MEMORY &#124; TEST-FR-AGENT-003 &#124; AC-FR-AGENT-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:70`; audit line 151 | UNSTATED | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-004` | `AC-FR-AGENT-004`: &#124; FR-AGENT-004 &#124; Agent Runtime &#124; WP-AGENT-MEMORY &#124; TEST-FR-AGENT-004 &#124; AC-FR-AGENT-004 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:71`; audit line 152 | UNSTATED | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-005` | `AC-FR-AGENT-005`: &#124; FR-AGENT-005 &#124; Agent Runtime &#124; WP-AGENT-MEMORY &#124; TEST-FR-AGENT-005 &#124; AC-FR-AGENT-005 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:72`; audit line 153 | UNSTATED | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-006` | `AC-FR-MCP-001`: &#124; FR-MCP-001 &#124; MCP &#124; WP-MCP &#124; TEST-FR-MCP-001 &#124; AC-FR-MCP-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:74`; audit line 184 | UNSTATED | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-AGT-007` | `AC-FR-MCP-002`: &#124; FR-MCP-002 &#124; MCP &#124; WP-MCP &#124; TEST-FR-MCP-002 &#124; AC-FR-MCP-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:75`; audit line 185 | UNSTATED | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-AGT-008` | `AC-FR-MEM-001`: &#124; FR-MEM-001 &#124; Memory &#124; WP-AGENT-MEMORY &#124; TEST-FR-MEM-001 &#124; AC-FR-MEM-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:73`; audit line 186 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-AGT-009` | `AGENT-001`: Cognitive Boundary Telemetry | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:175`; audit line 228 | P1 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | engine family | PROVE |
| `REQ-AGT-010` | `AGENT-001.1`: - [x] `AGENT-001.1` 7+ boundary signal detectors | `eoip-phase4-2-requirements.md:406`; audit line 229 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-AGT-011` | `AGENT-001.2`: - [x] `AGENT-001.2` HandoffDecision with target selection | `eoip-phase4-2-requirements.md:407`; audit line 230 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-AGT-012` | `AGENT-001.3`: - [x] `AGENT-001.3` Integration with control loop autonomy levels | `eoip-phase4-2-requirements.md:408`; audit line 231 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-AGT-013` | `AGENT-001.4`: - [x] `AGENT-001.4` Telemetry event emission on boundary detection | `eoip-phase4-2-requirements.md:409`; audit line 232 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-AGT-014` | `AGENT-001.5`: - [x] `AGENT-001.5` Unit tests for each signal type | `eoip-phase4-2-requirements.md:410`; audit line 233 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-AGT-015` | `AGENT-002`: Dynamic Entity & Community Extraction Pipeline | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:194`; audit line 234 | P1 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | engine family | PROVE |
| `REQ-AGT-016` | `AGENT-002.1`: - [x] `AGENT-002.1` Configurable chunking strategies | `eoip-phase4-2-requirements.md:432`; audit line 235 | UNSTATED | MISSED | [CP-15](#cp-15) | engine family | TRACE/BUILD |
| `REQ-AGT-017` | `AGENT-002.2`: - [x] `AGENT-002.2` Entity extraction with type classification | `eoip-phase4-2-requirements.md:433`; audit line 236 | UNSTATED | MISSED | [CP-15](#cp-15) | engine family | TRACE/BUILD |
| `REQ-AGT-018` | `AGENT-002.3`: - [x] `AGENT-002.3` Relation extraction producing triples | `eoip-phase4-2-requirements.md:434`; audit line 237 | UNSTATED | MISSED | [CP-15](#cp-15) | engine family | TRACE/BUILD |
| `REQ-AGT-019` | `AGENT-002.4`: - [x] `AGENT-002.4` Community detection integration | `eoip-phase4-2-requirements.md:435`; audit line 238 | UNSTATED | MISSED | [CP-15](#cp-15) | engine family | TRACE/BUILD |
| `REQ-AGT-020` | `AGENT-002.5`: - [x] `AGENT-002.5` Streaming mode for continuous operation | `eoip-phase4-2-requirements.md:436`; audit line 239 | UNSTATED | MISSED | [CP-15](#cp-15) | engine family | TRACE/BUILD |
| `REQ-AGT-021` | `AGENT-002.6`: - [x] `AGENT-002.6` Thread-safe singleton | `eoip-phase4-2-requirements.md:437`; audit line 240 | UNSTATED | MISSED | [CP-15](#cp-15) | engine family | TRACE/BUILD |
| `REQ-AGT-022` | `AGENT-002.7`: - [x] `AGENT-002.7` Wired into brain_os.py and platform_router.py | `eoip-phase4-2-requirements.md:438`; audit line 241 | UNSTATED | MISSED | [CP-15](#cp-15) | engine family | TRACE/BUILD |
| `REQ-AGT-023` | `AGENT-002.8`: - [x] `AGENT-002.8` Unit tests | `eoip-phase4-2-requirements.md:439`; audit line 242 | UNSTATED | MISSED | [CP-15](#cp-15) | engine family | TRACE/BUILD |
| `REQ-AGT-024` | `AGENT-003`: Agent Communication Bus | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:220`; audit line 243 | P2 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | engine family | PROVE |
| `REQ-AGT-025` | `AGENT-003.1`: - [x] `AGENT-003.1` Typed message schemas with versioning | `eoip-phase4-2-requirements.md:460`; audit line 244 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-AGT-026` | `AGENT-003.2`: - [x] `AGENT-003.2` Capability negotiation protocol | `eoip-phase4-2-requirements.md:461`; audit line 245 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-AGT-027` | `AGENT-003.3`: - [x] `AGENT-003.3` Persistent message queue with DLQ | `eoip-phase4-2-requirements.md:462`; audit line 246 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-AGT-028` | `AGENT-003.4`: - [x] `AGENT-003.4` Pub/sub broadcast channels | `eoip-phase4-2-requirements.md:463`; audit line 247 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-AGT-029` | `AGENT-003.5`: - [x] `AGENT-003.5` Unit tests | `eoip-phase4-2-requirements.md:464`; audit line 248 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-AGT-030` | `AGENT-004`: Parallel Fan-Out/Fan-In (MapReduce) | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:241`; audit line 249 | P1 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | engine family | PROVE |
| `REQ-AGT-031` | `AGENT-004.1`: - [x] `AGENT-004.1` FanOutStage splitting work into parallel shards | `eoip-phase4-2-requirements.md:481`; audit line 250 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-AGT-032` | `AGENT-004.2`: - [x] `AGENT-004.2` FanInStage merging results with conflict detection | `eoip-phase4-2-requirements.md:482`; audit line 251 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-AGT-033` | `AGENT-004.3`: - [x] `AGENT-004.3` Configurable parallelism and timeouts | `eoip-phase4-2-requirements.md:483`; audit line 252 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-AGT-034` | `AGENT-004.4`: - [x] `AGENT-004.4` Integration with existing harness engine | `eoip-phase4-2-requirements.md:484`; audit line 253 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-AGT-035` | `AGENT-004.5`: - [x] `AGENT-004.5` Unit tests with race condition scenarios | `eoip-phase4-2-requirements.md:485`; audit line 254 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-AGT-036` | `AIDLC-003.1`: - [ ] `AIDLC-003.1` Benchmarks and targets recorded for AGENT-002, AI-002, AI-003 | `eoip-phase4-2-requirements.md:2089`; audit line 310 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-AGT-037` | `AIDLC-005.2`: - [ ] `AIDLC-005.2` Replay-based regression test for two agents | `eoip-phase4-2-requirements.md:2184`; audit line 321 | UNSTATED | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-AGT-038` | `AIDLC-012.3`: - [ ] `AIDLC-012.3` Per-agent allowlists | `eoip-phase4-2-requirements.md:2241`; audit line 357 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-AGT-039` | `AIDLC-013`: ###### AIDLC-013: Agent and workload identity, plus SCIM | `eoip-phase4-2-requirements.md:2244`; audit line 359 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-AGT-040` | `AIDLC-013.1`: - [ ] `AIDLC-013.1` Agent credentials are scoped and expire | `eoip-phase4-2-requirements.md:2257`; audit line 360 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-AGT-041` | `AIDLC-013.2`: - [ ] `AIDLC-013.2` Audit shows agent and delegating user | `eoip-phase4-2-requirements.md:2258`; audit line 361 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-AGT-042` | `AIDLC-014.1`: - [ ] `AIDLC-014.1` Inventory and risk classes for all engines and agents | `eoip-phase4-2-requirements.md:2276`; audit line 365 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-AGT-043` | `AIDLC-014.2`: - [ ] `AIDLC-014.2` Model and agent card template filled for core models | `eoip-phase4-2-requirements.md:2277`; audit line 366 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-AGT-044` | `FR-AGENT-001`: Agent contract | `EOIP-engg-doc-pkg/03-functional-requirements.md:545`; audit line 506 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | ID family | PROVE |
| `REQ-AGT-045` | `FR-AGENT-002`: Bounded agent runtime | `EOIP-engg-doc-pkg/03-functional-requirements.md:555`; audit line 507 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | ID family | PROVE |
| `REQ-AGT-046` | `FR-AGENT-003`: TraceImpact agent | `EOIP-engg-doc-pkg/02-scope-and-objectives.md:26`; audit line 508 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | ID family | PROVE |
| `REQ-AGT-047` | `FR-AGENT-004`: Write/action approval boundary | `EOIP-engg-doc-pkg/03-functional-requirements.md:575`; audit line 509 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | ID family | PROVE |
| `REQ-AGT-048` | `FR-AGENT-005`: Controlled self-modification | `EOIP-engg-doc-pkg/03-functional-requirements.md:585`; audit line 510 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | ID family | PROVE |
| `REQ-AGT-049` | `FR-MCP-001`: MCP read server | `EOIP-engg-doc-pkg/03-functional-requirements.md:605`; audit line 573 | P0 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-AGT-050` | `FR-MCP-002`: MCP action separation | `EOIP-engg-doc-pkg/03-functional-requirements.md:615`; audit line 574 | P0 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-AGT-051` | `GAP-AGOV-003`: GAP-AGOV-003: Capability tokens or equivalent scoped tool authorization in future enterprise phases | `EOIP-engg-doc-pkg/gaps-requirements.md:716`; audit line 1209 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | ID family | PROVE |
| `REQ-AGT-052` | `GAP-AGOV-005`: GAP-AGOV-005: Per-agent time/step/tool/model budgets | `EOIP-engg-doc-pkg/gaps-requirements.md:718`; audit line 1211 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | ID family | PROVE |
| `REQ-AGT-053` | `GAP-AGOV-007`: GAP-AGOV-007: Tool-output sanitization | `EOIP-engg-doc-pkg/gaps-requirements.md:720`; audit line 1213 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | ID family | PROVE |
| `REQ-AGT-054` | `GAP-AGOV-008`: GAP-AGOV-008: MCP server allowlist | `EOIP-engg-doc-pkg/gaps-requirements.md:721`; audit line 1214 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | ID family | PROVE |
| `REQ-AGT-055` | `GAP-AGOV-010`: GAP-AGOV-010: Replayable agent execution traces excluding private chain-of-thought | `EOIP-engg-doc-pkg/gaps-requirements.md:723`; audit line 1216 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | ID family | PROVE |
| `REQ-AGT-056` | `GAP-AGOV-012`: GAP-AGOV-012: Agent evaluation gates before promotion | `EOIP-engg-doc-pkg/gaps-requirements.md:725`; audit line 1218 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | ID family | PROVE |
| `REQ-AGT-057` | `GAP-AKO-001`: GAP-AKO-001: Knowledge Curator Agent | `EOIP-engg-doc-pkg/gaps-implementation.md:601`; audit line 1221 | P2 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | subject triage | PROVE |
| `REQ-AGT-058` | `GAP-AKO-003`: GAP-AKO-003: Data Quality Agent | `EOIP-engg-doc-pkg/gaps-requirements.md:697`; audit line 1223 | P2 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | subject triage | PROVE |
| `REQ-AGT-059` | `GAP-AKO-005`: GAP-AKO-005: Change Impact Agent | `EOIP-engg-doc-pkg/gaps-requirements.md:699`; audit line 1225 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | subject triage | PROVE |
| `REQ-AGT-060` | `GAP-AKO-006`: GAP-AKO-006: Architecture Conformance Agent | `EOIP-engg-doc-pkg/gaps-requirements.md:700`; audit line 1226 | P2 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | subject triage | PROVE |
| `REQ-AGT-061` | `GAP-AKO-007`: GAP-AKO-007: Incident Investigation Agent | `EOIP-engg-doc-pkg/gaps-requirements.md:701`; audit line 1227 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | subject triage | PROVE |
| `REQ-AGT-062` | `GAP-AKO-008`: GAP-AKO-008: Documentation Freshness Agent | `EOIP-engg-doc-pkg/gaps-requirements.md:702`; audit line 1228 | P2 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | subject triage | PROVE |
| `REQ-AGT-063` | `GAP-AKO-009`: GAP-AKO-009: Evidence Verification Agent | `EOIP-engg-doc-pkg/gaps-requirements.md:703`; audit line 1229 | P2 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | subject triage | PROVE |
| `REQ-AGT-064` | `GAP-LIFE-003`: GAP-LIFE-003: Expire transient agent memory separately from enterprise facts | `EOIP-engg-doc-pkg/gaps-requirements.md:902`; audit line 1394 | P2 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | subject triage | PROVE |
| `REQ-AGT-065` | `GAP-MKT-005`: GAP-MKT-005: Package agent workflows | `EOIP-engg-doc-pkg/gaps-requirements.md:919`; audit line 1410 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-AGT-066` | `KGR-G-009`: Neuro-Symbolic Agent Memory (AGAM) & IDE MCP Server | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:44`; audit line 1618 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-AGT-067` | `KGR-G-014`: Streaming Temporal Agent Memory (Dual-Timeline Incremental Updates) | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:314`; audit line 1623 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-AGT-068` | `KGR-G-019`: Calibrated Uncertainty & Honest Abstain MCP Response Protocol | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:314`; audit line 1628 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-AGT-069` | `KGR-G-022`: Multi-Archetype Agent Factory & A2A Protocol (76+ Archetypes & Swarms) | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:226`; audit line 1631 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-AGT-070` | `MS-16`: Agentic Process Intelligence & Digital Process Twin | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:183`; audit line 1646 | P1 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-AGT-071` | `MS-19`: Agent Memory Immune System (AMIS) — Anti-Poisoning Defense | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:25`; audit line 1649 | P1 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-AGT-072` | `MVP-FR-021`: Useful read-only agent workflow | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:119`; audit line 1700 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | subject triage | PROVE |
| `REQ-AGT-073` | `PRE-001.4`: - [x] `PRE-001.4` Decide the load tool (conflict B5, DEC-P4-03) and the overlap handling (DEC-P4-02). | `eoip-phase4-2-requirements.md:199`; audit line 1756 | UNSTATED | MISSED | [CP-00](#cp-00) | ID family | TRACE/BUILD |
| `REQ-AGT-074` | `SDLC-005`: &#124; Tenant isolation &#124; INFRA-001, AGENT-003, CORE-006, AI-005, MULTI-002 and the "thread-safe singleton" pattern in 8 requirements &#124; Process-wide singletons holding tenant state conflict with KGR-G-013 and MS-26. See SD... | `eoip-phase4-2-requirements.md:144`; audit line 1804 | UNSTATED | MISSED | [CP-06](#cp-06) | engine family | TRACE/BUILD |
| `REQ-AGT-075` | `SDLC-008`: &#124; Humans in the loop &#124; AGENT-001, COMPLY-001, KGF GAP-TRUTH-008, GAP-GOV, loop approval gates &#124; Five places hand work to people; none defines the queue, SLA, escalation or notification. See SDLC-008. &#124; | `eoip-phase4-2-requirements.md:141`; audit line 1819 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-AGT-076` | `SDLC-008.2`: - [ ] `SDLC-008.2` AGENT-001, COMPLY-001, GAP-TRUTH-008 and low-confidence triples (AI-003) create work items | `eoip-phase4-2-requirements.md:1545`; audit line 1821 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-AGT-077` | `SDLC-010`: &#124; SDLC: build and code quality &#124; KGF S-03 CI &#124; No type or layering gates, no coverage, no synthetic data, no mutation testing, no rules for the coding agent &#124; SDLC-010..016 &#124; | `eoip-phase4-2-requirements.md:1371`; audit line 1829 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-AGT-078` | `SDLC-025.1`: - [ ] `SDLC-025.1` Traces cover a full agent request | `eoip-phase4-2-requirements.md:1863`; audit line 1905 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-AGT-079` | `SDLC-030`: &#124; Tenant isolation &#124; INFRA-001, AGENT-003, CORE-006, AI-005, MULTI-002 and the "thread-safe singleton" pattern in 8 requirements &#124; Process-wide singletons holding tenant state conflict with KGR-G-013 and MS-26. See SD... | `eoip-phase4-2-requirements.md:144`; audit line 1929 | UNSTATED | MISSED | [CP-06](#cp-06) | engine family | TRACE/BUILD |
| `REQ-AGT-080` | `SR-AGT-001`: &#124; SR-AGT-001 &#124; **Agent contract** (JSON schema): identity, purpose, allowed tools, input/output schemas, budgets (steps, tokens, time, expansions), risk class, approval mode, memory scope, evaluation hooks. Agents are ... | `EOIP-engg-doc-pkg/super-requirements.md:681`; audit line 1954 | P0 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-081` | `SR-AGT-002`: &#124; SR-AGT-002 &#124; **Bounded runtime:** tool allowlist, budget enforcement, circuit breaker, loop/stall detection, deterministic replay from traces. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:682`; audit line 1955 | P0 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-082` | `SR-AGT-003`: &#124; SR-AGT-003 &#124; **Autonomy modes:** HITL (human approves each action), HOTL (human monitors, can intervene), HIC (human in command; autonomy scoped by policy). Mode is a policy per agent × action risk class × tenant. &#124;... | `EOIP-engg-doc-pkg/super-requirements.md:683`; audit line 1956 | P0 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-083` | `SR-AGT-004`: &#124; SR-AGT-004 &#124; **Read/write separation:** default agents are read-only; any write/action tool requires an explicit approval boundary, audit and (where configured) dual control. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:684`; audit line 1957 | P0 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-084` | `SR-AGT-005`: &#124; SR-AGT-005 &#124; **MCP servers:** a read-only MCP server exposing graph, query, evidence and lineage tools; a separately governed action server; inventories generated from code; per-tenant auth and rate limits. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:685`; audit line 1958 | P0 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-085` | `SR-AGT-006`: &#124; SR-AGT-006 &#124; **Memory:** scoped (turn/session/user/workspace/tenant), policy-governed, expiring, inspectable and erasable; no cross-tenant memory. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:686`; audit line 1959 | P0 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-086` | `SR-AGT-007`: &#124; SR-AGT-007 &#124; **Agent registry & marketplace:** discover, install, evaluate and certify agents; signed packages; capability declarations. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:687`; audit line 1960 | P1 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-087` | `SR-AGT-008`: &#124; SR-AGT-008 &#124; **Multi-agent orchestration:** planner/critic/worker patterns, event-driven coordination, shared evidence blackboard, XAI trace per run. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:688`; audit line 1961 | P1 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-088` | `SR-AGT-009`: &#124; SR-AGT-009 &#124; **Controlled self-improvement is OFF by default;** proposals (prompt, mapping, ontology, rule changes) are generated as reviewable change requests, never self-applied. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:689`; audit line 1962 | P0 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-089` | `SR-AGT-010`: &#124; SR-AGT-010 &#124; **Specialist agent catalog** (starting set inherited from the codebase, plus new): DataQuality, OntologyReview, ConnectorDiagnosis, DocumentationFreshness, EvidenceVerification, ArchitectureConformance, ... | `EOIP-engg-doc-pkg/super-requirements.md:690`; audit line 1963 | P1 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-090` | `SR-AGT-011`: &#124; SR-AGT-011 &#124; **RPA/workflow hooks:** approved agent outputs may trigger tickets, PR comments, notifications or runbook steps through connectors, always with human approval unless policy allows. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:691`; audit line 1964 | P1 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-091` | `SR-AGT-020`: &#124; SR-AGT-020 &#124; **Continuous sync and change detection:** the brain updates on source change; users can **watch** an entity, pattern or question and get alerts when answers change ("continuous queries"). &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:697`; audit line 1965 | P1 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-092` | `SR-AGT-021`: &#124; SR-AGT-021 &#124; **Drift and conformance detection:** docs vs code, architecture vs deployment, ontology vs data, policy vs access, declared vs observed dependencies. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:698`; audit line 1966 | P1 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-093` | `SR-AGT-022`: &#124; SR-AGT-022 &#124; **Freshness and knowledge-decay scoring:** per node/edge/source; stale knowledge is visibly flagged and down-ranked. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:699`; audit line 1967 | P0 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-094` | `SR-AGT-023`: &#124; SR-AGT-023 &#124; **Knowledge-debt and bus-factor analysis:** single-owner components, orphaned systems, undocumented critical dependencies. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:700`; audit line 1968 | P1 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-095` | `SR-AGT-024`: &#124; SR-AGT-024 &#124; **Expert finder and routing:** who knows/owns/changed what, with identity-resolved evidence; "who should I ask?". &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:701`; audit line 1969 | P1 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-096` | `SR-AGT-025`: &#124; SR-AGT-025 &#124; **Risk scoring:** change risk = blast radius × fragility × test coverage × recent-incident correlation; surfaced in PR/change-request bots. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:702`; audit line 1970 | P1 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-097` | `SR-AGT-026`: &#124; SR-AGT-026 &#124; **Anomaly detection** on graph structure, ingestion patterns and access behavior. &#124; P2 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:703`; audit line 1971 | P2 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-098` | `SR-AGT-027`: &#124; SR-AGT-027 &#124; **Digest and briefing:** scheduled personalized briefings (what changed, what's at risk, open items) per role. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:704`; audit line 1972 | P1 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-099` | `SR-AGT-028`: &#124; SR-AGT-028 &#124; **Onboarding and tours:** auto-generated "map of this domain" guides for newcomers from the graph. &#124; P2 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:705`; audit line 1973 | P2 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-100` | `SR-AGT-029`: &#124; SR-AGT-029 &#124; **Digital-twin mode:** model processes/assets/organizations as simulatable graphs for scenario planning (links to SR-NLQ-014). &#124; P3 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:706`; audit line 1974 | P3 | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-101` | `SR-COM-002`: &#124; SR-COM-002 &#124; **PoC kit:** 30-day evaluation license, per-industry demo datasets, scripted demo flows, sizing tool, ROI calculator, 10-question "prove it on your data" workshop template. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:1001`; audit line 1994 | P0 | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-AGT-102` | `TASK-AIE-002`: - **TASK-AIE-002**: Implement Cognitive Boundary Detection (AGENT-001) — signal algorithms | `EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:18`; audit line 2245 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-AGT-103` | `TASK-ARCH-014`: - **TASK-ARCH-014**: Design Fan-Out/Fan-In (AGENT-004) state merge protocol — conflict detection, merge strategies, idempotency | `EOIP-engg-doc-pkg/roles/Architect_tasks.md:69`; audit line 2270 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-AGT-104` | `TASK-DM-004`: - **TASK-DM-004**: Manage AI Agent coding workflow — task assignment, verification, code review pipeline | `EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:28`; audit line 2324 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-AGT-105` | `TASK-DM-013`: - **TASK-DM-013**: Capacity planning: map 47 requirements to available dev capacity (AI agents + human) | `EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:79`; audit line 2333 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-AGT-106` | `TASK-LAI-008`: - **TASK-LAI-008**: Design cognitive boundary detection algorithms (AGENT-001) | `EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:46`; audit line 2342 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-AGT-107` | `TASK-LEGAL-013`: - **TASK-LEGAL-013**: Review AI agent actions for liability — who is responsible when an agent makes a harmful decision? | `EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:75`; audit line 2379 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-AGT-108` | `TEST-FR-AGENT-001`: &#124; FR-AGENT-001 &#124; Agent Runtime &#124; WP-AGENT-MEMORY &#124; TEST-FR-AGENT-001 &#124; AC-FR-AGENT-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:68`; audit line 2490 | UNSTATED | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-109` | `TEST-FR-AGENT-002`: &#124; FR-AGENT-002 &#124; Agent Runtime &#124; WP-AGENT-MEMORY &#124; TEST-FR-AGENT-002 &#124; AC-FR-AGENT-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:69`; audit line 2491 | UNSTATED | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-110` | `TEST-FR-AGENT-003`: &#124; FR-AGENT-003 &#124; Agent Runtime &#124; WP-AGENT-MEMORY &#124; TEST-FR-AGENT-003 &#124; AC-FR-AGENT-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:70`; audit line 2492 | UNSTATED | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-111` | `TEST-FR-AGENT-004`: &#124; FR-AGENT-004 &#124; Agent Runtime &#124; WP-AGENT-MEMORY &#124; TEST-FR-AGENT-004 &#124; AC-FR-AGENT-004 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:71`; audit line 2493 | UNSTATED | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-112` | `TEST-FR-AGENT-005`: &#124; FR-AGENT-005 &#124; Agent Runtime &#124; WP-AGENT-MEMORY &#124; TEST-FR-AGENT-005 &#124; AC-FR-AGENT-005 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:72`; audit line 2494 | UNSTATED | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-113` | `WP-AGENT-MEMORY-01`: ### WP-AGENT-MEMORY-01 — Agent contract | `EOIP-engg-doc-pkg/implementation/wp-agent-memory.md:24`; audit line 2620 | UNSTATED | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-114` | `WP-AGENT-MEMORY-02`: ### WP-AGENT-MEMORY-02 — Bounded agent runtime | `EOIP-engg-doc-pkg/implementation/wp-agent-memory.md:33`; audit line 2621 | UNSTATED | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-115` | `WP-AGENT-MEMORY-03`: ### WP-AGENT-MEMORY-03 — TraceImpact agent | `EOIP-engg-doc-pkg/implementation/wp-agent-memory.md:42`; audit line 2622 | UNSTATED | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-116` | `WP-AGENT-MEMORY-04`: ### WP-AGENT-MEMORY-04 — Write/action approval boundary | `EOIP-engg-doc-pkg/implementation/wp-agent-memory.md:51`; audit line 2623 | UNSTATED | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-117` | `WP-AGENT-MEMORY-05`: ### WP-AGENT-MEMORY-05 — Controlled self-modification | `EOIP-engg-doc-pkg/implementation/wp-agent-memory.md:60`; audit line 2624 | UNSTATED | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-118` | `WP-AGENT-MEMORY-06`: ### WP-AGENT-MEMORY-06 — Scoped memory records | `EOIP-engg-doc-pkg/implementation/wp-agent-memory.md:69`; audit line 2625 | UNSTATED | MISSED | [CP-22](#cp-22) | ID family | TRACE/BUILD |
| `REQ-AGT-119` | `WP-MCP-01`: ### WP-MCP-01 — MCP read server | `EOIP-engg-doc-pkg/implementation/wp-mcp.md:20`; audit line 2656 | UNSTATED | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-AGT-120` | `WP-MCP-02`: ### WP-MCP-02 — MCP action separation | `EOIP-engg-doc-pkg/implementation/wp-mcp.md:29`; audit line 2657 | UNSTATED | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |

### A.4 API: 22 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-API-001` | `G2-ARCH-002`: G2-ARCH-002 — API/event first | `EOIP-engg-doc-pkg/gaps2-requirements.md:56`; audit line 641 | P0 | IMPLEMENTED-UNVERIFIED | [CP-07](#cp-07) | subject triage | PROVE |
| `REQ-API-002` | `G2-SRC-API-001`: G2-SRC-API-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:523`; audit line 863 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-API-003` | `G2-SRC-API-002`: G2-SRC-API-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:480`; audit line 864 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-API-004` | `G2-SRC-API-003`: G2-SRC-API-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:483`; audit line 865 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-API-005` | `G2-SRC-API-004`: G2-SRC-API-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:487`; audit line 866 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-API-006` | `G2-SRC-API-005`: G2-SRC-API-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:490`; audit line 867 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-API-007` | `G2-SRC-API-006`: G2-SRC-API-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:493`; audit line 868 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-API-008` | `INFRA-006.3`: - [x] `INFRA-006.3` Generated Python SDK | `eoip-phase4-2-requirements.md:927`; audit line 1601 | UNSTATED | MISSED | [CP-07](#cp-07) | engine family | TRACE/BUILD |
| `REQ-API-009` | `INFRA-006.4`: - [x] `INFRA-006.4` Generated JavaScript SDK | `eoip-phase4-2-requirements.md:928`; audit line 1602 | UNSTATED | MISSED | [CP-07](#cp-07) | engine family | TRACE/BUILD |
| `REQ-API-010` | `INFRA-006.5`: - [x] `INFRA-006.5` SDK packaging | `eoip-phase4-2-requirements.md:929`; audit line 1603 | UNSTATED | MISSED | [CP-07](#cp-07) | engine family | TRACE/BUILD |
| `REQ-API-011` | `INFRA-007.4`: - [x] `INFRA-007.4` Encryption at rest | `eoip-phase4-2-requirements.md:951`; audit line 1608 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-API-012` | `PRE-001.5`: - [x] `PRE-001.5` List every Phase 4 engine that exposes an API and state how it will be mounted (engine registry SDLC-004 if accepted, otherwise the manual wiring in brain_os.py and platform_router.py). | `eoip-phase4-2-requirements.md:200`; audit line 1757 | UNSTATED | MISSED | [CP-00](#cp-00) | ID family | TRACE/BUILD |
| `REQ-API-013` | `SDLC-008.1`: - [ ] `SDLC-008.1` Work-item API and inbox UI | `eoip-phase4-2-requirements.md:1544`; audit line 1820 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-API-014` | `SDLC-017.3`: - [ ] `SDLC-017.3` SDK and web client use the same contracts | `eoip-phase4-2-requirements.md:1716`; audit line 1867 | UNSTATED | MISSED | [CP-29](#cp-29) | engine family | TRACE/BUILD |
| `REQ-API-015` | `SR-QA-013`: &#124; SR-QA-013 &#124; Generated inventories (API routes, tools, labels, algorithms, commands) come from code introspection; hand-written counts fail the docs build. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:965`; audit line 2168 | P0 | IMPLEMENTED-UNVERIFIED | [CP-07](#cp-07) | subject triage | PROVE |
| `REQ-API-016` | `TASK-ARCH-006`: - **TASK-ARCH-006**: Define API contract standards for new Phase 4 endpoints (47 features → ~100+ new endpoints) | `EOIP-engg-doc-pkg/roles/Architect_tasks.md:34`; audit line 2262 | UNSTATED | MISSED | [CP-07](#cp-07) | subject triage | TRACE/BUILD |
| `REQ-API-017` | `TASK-CTO-006`: - **TASK-CTO-006**: Define and enforce API design standards across 133+ API paths | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:44`; audit line 2292 | UNSTATED | MISSED | [CP-07](#cp-07) | subject triage | TRACE/BUILD |
| `REQ-API-018` | `TASK-DM-006`: - **TASK-DM-006**: Establish release checklist: all tests pass, OpenAPI validates, no P0 bugs, docs updated | `EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:41`; audit line 2326 | P0 | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-API-019` | `TASK-LD-016`: - **TASK-LD-016**: Standardize error handling across all engines — consistent exception hierarchy, error codes | `EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:83`; audit line 2366 | UNSTATED | MISSED | [CP-07](#cp-07) | area fallback | TRACE/BUILD |
| `REQ-API-020` | `TASK-MKE-005`: - **TASK-MKE-005**: Write product documentation site content — getting started, tutorials, API reference | `EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:29`; audit line 2399 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-API-021` | `TASK-QA-020`: - **TASK-QA-020**: Write k6 load test scripts for critical API endpoints (TEST-002) | `EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:52`; audit line 2432 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-API-022` | `TASK-QAL-011`: - **TASK-QAL-011**: Establish API contract testing for 133+ endpoints | `EOIP-engg-doc-pkg/roles/QALead_tasks.md:61`; audit line 2444 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |

### A.5 CON: 122 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-CON-001` | `AC-06`: &#124; AC-06 &#124; Graph renders 1,000 nodes in < 2 seconds &#124; Sourcetrail: crashes, code2flow: cluttered &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1037`; audit line 104 | UNSTATED | MISSED | [CP-32](#cp-32) | explicit | TRACE/BUILD |
| `REQ-CON-002` | `AC-15`: &#124; AC-15 &#124; No external network requests in production &#124; Fixes Sourcegraph, CodeSee, Graphistry &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1046`; audit line 113 | UNSTATED | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-CON-003` | `AC-22`: &#124; AC-22 &#124; Code + graph side-by-side view with synchronized navigation &#124; Sourcetrail (discontinued, desktop, 4 langs) — KGR is browser-based, all languages &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1053`; audit line 120 | UNSTATED | MISSED | [CP-27](#cp-27) | subject triage | TRACE/BUILD |
| `REQ-CON-004` | `AC-FR-CONF-001`: &#124; FR-CONF-001 &#124; Platform &#124; WP-CONNECTORS &#124; TEST-FR-CONF-001 &#124; AC-FR-CONF-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:22`; audit line 159 | UNSTATED | MISSED | [CP-16](#cp-16) | subject triage | TRACE/BUILD |
| `REQ-CON-005` | `AC-FR-CONN-001`: &#124; FR-CONN-001 &#124; Connector SDK &#124; WP-CONNECTORS &#124; TEST-FR-CONN-001 &#124; AC-FR-CONN-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:15`; audit line 160 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-006` | `AC-FR-CONN-002`: &#124; FR-CONN-002 &#124; Connector SDK &#124; WP-CONNECTORS &#124; TEST-FR-CONN-002 &#124; AC-FR-CONN-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:16`; audit line 161 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-007` | `AC-FR-CONN-003`: &#124; FR-CONN-003 &#124; Connector SDK &#124; WP-CONNECTORS &#124; TEST-FR-CONN-003 &#124; AC-FR-CONN-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:17`; audit line 162 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-008` | `AC-FR-CONN-004`: &#124; FR-CONN-004 &#124; Connector SDK &#124; WP-CONNECTORS &#124; TEST-FR-CONN-004 &#124; AC-FR-CONN-004 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:18`; audit line 163 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-009` | `AC-FR-CONN-005`: &#124; FR-CONN-005 &#124; Connector SDK &#124; WP-CONNECTORS &#124; TEST-FR-CONN-005 &#124; AC-FR-CONN-005 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:19`; audit line 164 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-010` | `AC-FR-CONN-006`: &#124; FR-CONN-006 &#124; Connector SDK &#124; WP-CONNECTORS &#124; TEST-FR-CONN-006 &#124; AC-FR-CONN-006 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:20`; audit line 165 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-011` | `AC-FR-CONN-007`: &#124; FR-CONN-007 &#124; Connector SDK &#124; WP-CONNECTORS &#124; TEST-FR-CONN-007 &#124; AC-FR-CONN-007 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:21`; audit line 166 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-012` | `AC-FR-SNOW-001`: &#124; FR-SNOW-001 &#124; Platform &#124; WP-CONNECTORS &#124; TEST-FR-SNOW-001 &#124; AC-FR-SNOW-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:23`; audit line 205 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-013` | `AIDLC-001.2`: - [ ] `AIDLC-001.2` Lineage queryable from an answer back to source | `eoip-phase4-2-requirements.md:2053`; audit line 301 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-CON-014` | `AIDLC-003.3`: - [ ] `AIDLC-003.3` Source reliability scores | `eoip-phase4-2-requirements.md:2091`; audit line 312 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-CON-015` | `CONN-01`: Confluence offline fixtures and live-connector test | `KGF-MASTER-BACKLOG.md:493`; audit line 413 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-CON-016` | `CONN-02`: ServiceNow offline fixtures and live-connector test | `KGF-MASTER-BACKLOG.md:496`; audit line 414 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-CON-017` | `CONN-03`: Jira changelog streaming connector and fixtures | `KGF-MASTER-BACKLOG.md:499`; audit line 415 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-CON-018` | `FR-06`: &#124; FR-06 &#124; User experience &#124; Web UI, admin UI, Hubble/local graph exploration, VS Code extension, demo walkthroughs, dashboards, source views, lineage views, and operational controls. &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1085`; audit line 500 | UNSTATED | MISSED | [CP-29](#cp-29) | subject triage | TRACE/BUILD |
| `REQ-CON-019` | `FR-CODE-005`: Source navigation | `EOIP-engg-doc-pkg/03-functional-requirements.md:365`; audit line 515 | P0 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-CON-020` | `FR-CONF-001`: Confluence connector | `EOIP-engg-doc-pkg/03-functional-requirements.md:81`; audit line 516 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | subject triage | PROVE |
| `REQ-CON-021` | `FR-CONN-001`: Connector SDK | `EOIP-engg-doc-pkg/03-functional-requirements.md:11`; audit line 517 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-CON-022` | `FR-CONN-002`: Jira JSON connector | `EOIP-engg-doc-pkg/02-scope-and-objectives.md:22`; audit line 518 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-CON-023` | `FR-CONN-003`: Git repository connector | `EOIP-engg-doc-pkg/02-scope-and-objectives.md:23`; audit line 519 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-CON-024` | `FR-CONN-004`: GitLab metadata adapter | `EOIP-engg-doc-pkg/03-functional-requirements.md:41`; audit line 520 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-CON-025` | `FR-CONN-005`: Connector resiliency | `EOIP-engg-doc-pkg/03-functional-requirements.md:51`; audit line 521 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-CON-026` | `FR-CONN-006`: Dry run and replay | `EOIP-engg-doc-pkg/03-functional-requirements.md:61`; audit line 522 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-CON-027` | `FR-CONN-007`: Source deletion semantics | `EOIP-engg-doc-pkg/03-functional-requirements.md:71`; audit line 523 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-CON-028` | `FR-KGR-012`: Implements FR-KGR-012. Inspired by Sourcetrail's defining feature. No free browser-based tool offers this. | `EOIP-engg-doc-pkg/KGR-implementation-plan.md:1329`; audit line 554 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-CON-029` | `FR-SNOW-001`: ServiceNow connector | `EOIP-engg-doc-pkg/03-functional-requirements.md:91`; audit line 595 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-CON-030` | `G2-ARCH-004`: G2-ARCH-004 — Preserve source fidelity | `EOIP-engg-doc-pkg/gaps2-requirements.md:72`; audit line 643 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | area fallback | PROVE |
| `REQ-CON-031` | `G2-ARCH-011`: G2-ARCH-011 — AI is not the source of truth | `EOIP-engg-doc-pkg/gaps2-requirements.md:100`; audit line 650 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | area fallback | PROVE |
| `REQ-CON-032` | `G2-ARCH-014`: G2-ARCH-014 — Source permissions respected | `EOIP-engg-doc-pkg/gaps2-requirements.md:112`; audit line 653 | P0 | IMPLEMENTED-UNVERIFIED | [CP-05](#cp-05) | subject triage | PROVE |
| `REQ-CON-033` | `G2-EKAF-001`: G2-EKAF-001 — Source Registry | `EOIP-engg-doc-pkg/gaps2-implementation.md:139`; audit line 676 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-CON-034` | `G2-EKAF-002`: G2-EKAF-002 — Connector SDK | `EOIP-engg-doc-pkg/gaps2-requirements.md:175`; audit line 677 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-CON-035` | `G2-EKAF-003`: G2-EKAF-003 — SourceEvent envelope | `EOIP-engg-doc-pkg/gaps2-implementation.md:58`; audit line 678 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-CON-036` | `G2-EKAF-004`: G2-EKAF-004 — Baseline crawl | `EOIP-engg-doc-pkg/gaps2-requirements.md:204`; audit line 679 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-CON-037` | `G2-EKAF-008`: G2-EKAF-008 — Reconciliation crawl | `EOIP-engg-doc-pkg/gaps2-requirements.md:221`; audit line 683 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-CON-038` | `G2-EKAF-016`: G2-EKAF-016 — Source deletion semantics | `EOIP-engg-doc-pkg/gaps2-requirements.md:262`; audit line 691 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-CON-039` | `G2-EKAF-019`: G2-EKAF-019 — Crawl boundaries | `EOIP-engg-doc-pkg/gaps2-requirements.md:275`; audit line 694 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-CON-040` | `G2-EKAF-021`: G2-EKAF-021 — Connector health | `EOIP-engg-doc-pkg/gaps2-requirements.md:290`; audit line 696 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-CON-041` | `G2-EKAF-022`: G2-EKAF-022 — Source priority | `EOIP-engg-doc-pkg/gaps2-requirements.md:301`; audit line 697 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-CON-042` | `G2-EKAF-027`: G2-EKAF-027 — Source capability introspection | `EOIP-engg-doc-pkg/gaps2-requirements.md:322`; audit line 702 | P2 | PARTIAL | [CP-34](#cp-34) | ID family | COMPLETE |
| `REQ-CON-043` | `G2-EKAF-028`: G2-EKAF-028 — Connector compatibility matrix | `EOIP-engg-doc-pkg/gaps2-requirements.md:334`; audit line 703 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-CON-044` | `G2-EKAF-029`: G2-EKAF-029 — Offline source fixture mode | `EOIP-engg-doc-pkg/gaps2-requirements.md:337`; audit line 704 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-CON-045` | `G2-EKAF-030`: G2-EKAF-030 — Source onboarding wizard | `EOIP-engg-doc-pkg/gaps2-requirements.md:340`; audit line 705 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-CON-046` | `G2-P1`: &#124; G2-P1 &#124; EKAF core &#124; Source registry + connector/crawler framework &#124; | `EOIP-engg-doc-pkg/gaps2-implementation.md:36`; audit line 797 | P1 | MISSED | [CP-16](#cp-16) | subject triage | TRACE/BUILD |
| `REQ-CON-047` | `G2-P3`: &#124; G2-P3 &#124; Source Wave 1 &#124; Jira + Git/GitLab/GitHub + source + files &#124; | `EOIP-engg-doc-pkg/gaps2-implementation.md:38`; audit line 801 | P3 | MISSED | [CP-16](#cp-16) | subject triage | TRACE/BUILD |
| `REQ-CON-048` | `G2-P4`: &#124; G2-P4 &#124; Source Wave 2 &#124; Confluence + ServiceNow + API portals &#124; | `EOIP-engg-doc-pkg/gaps2-implementation.md:39`; audit line 802 | UNSTATED | MISSED | [CP-16](#cp-16) | subject triage | TRACE/BUILD |
| `REQ-CON-049` | `G2-P5`: &#124; G2-P5 &#124; Source Wave 3 &#124; CI/CD + observability + runtime + SBOM &#124; | `EOIP-engg-doc-pkg/gaps2-implementation.md:40`; audit line 803 | UNSTATED | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-CON-050` | `G2-SRC-JIRA-001`: G2-SRC-JIRA-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:416`; audit line 898 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-CON-051` | `G2-SRC-JIRA-002`: G2-SRC-JIRA-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:353`; audit line 899 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-CON-052` | `G2-SRC-JIRA-003`: G2-SRC-JIRA-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:356`; audit line 900 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-CON-053` | `G2-SRC-JIRA-004`: G2-SRC-JIRA-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:359`; audit line 901 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-CON-054` | `G2-SRC-JIRA-005`: G2-SRC-JIRA-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:362`; audit line 902 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-CON-055` | `G2-SRC-JIRA-006`: G2-SRC-JIRA-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:365`; audit line 903 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-CON-056` | `G2-SYNC-012`: G2-SYNC-012 — Connector pause/resume | `EOIP-engg-doc-pkg/gaps2-requirements.md:682`; audit line 946 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-CON-057` | `G2-T0002`: ### G2-T0002 — SourceEvent v2 | `EOIP-engg-doc-pkg/gaps2-implementation.md:78`; audit line 950 | UNSTATED | MISSED | [CP-16](#cp-16) | area fallback | TRACE/BUILD |
| `REQ-CON-058` | `G2-T0004`: ### G2-T0004 — Source Registry schema | `EOIP-engg-doc-pkg/gaps2-implementation.md:102`; audit line 952 | UNSTATED | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-CON-059` | `GAP-AI-001`: GAP-AI-001: Make every GraphRAG/agent answer evidence-addressable to graph nodes, paths and source records | `EOIP-engg-doc-pkg/gaps-requirements.md:147`; audit line 1220 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | subject triage | PROVE |
| `REQ-CON-060` | `GAP-AKO-004`: GAP-AKO-004: Connector Diagnosis Agent | `EOIP-engg-doc-pkg/gaps-requirements.md:698`; audit line 1224 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | subject triage | PROVE |
| `REQ-CON-061` | `GAP-CACHE-002`: GAP-CACHE-002: Cache dependencies reference graph versions/source freshness | `EOIP-engg-doc-pkg/gaps-requirements.md:889`; audit line 1241 | P2 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | subject triage | PROVE |
| `REQ-CON-062` | `GAP-CONTRACT-002`: GAP-CONTRACT-002: Detect connector schema drift | `EOIP-engg-doc-pkg/gaps-requirements.md:440`; audit line 1264 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | subject triage | PROVE |
| `REQ-CON-063` | `GAP-CP-005`: GAP-CP-005: Every connector maps into canonical contracts | `EOIP-engg-doc-pkg/gaps-requirements.md:403`; audit line 1273 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | subject triage | PROVE |
| `REQ-CON-064` | `GAP-CP-006`: GAP-CP-006: Source-specific fields remain accessible without polluting the canonical ontology | `EOIP-engg-doc-pkg/gaps-requirements.md:404`; audit line 1274 | P2 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-CON-065` | `GAP-DRIFT-001`: GAP-DRIFT-001: Detect source schema drift | `EOIP-engg-doc-pkg/gaps-requirements.md:513`; audit line 1280 | P1 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-CON-066` | `GAP-ER-008`: GAP-ER-008: Source aliases | `EOIP-engg-doc-pkg/gaps-requirements.md:628`; audit line 1298 | P1 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-CON-067` | `GAP-FABRIC-001`: GAP-FABRIC-001: Query materialized HugeGraph data and selected external sources in one plan | `EOIP-engg-doc-pkg/06-architecture.md:125`; audit line 1303 | P1 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | subject triage | PROVE |
| `REQ-CON-068` | `GAP-FABRIC-002`: GAP-FABRIC-002: Source capability registry | `EOIP-engg-doc-pkg/gaps-requirements.md:639`; audit line 1304 | P1 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | area fallback | PROVE |
| `REQ-CON-069` | `GAP-FABRIC-004`: GAP-FABRIC-004: Push filters/projections to source where possible | `EOIP-engg-doc-pkg/gaps-requirements.md:641`; audit line 1306 | P1 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | area fallback | PROVE |
| `REQ-CON-070` | `GAP-FABRIC-008`: GAP-FABRIC-008: Enforce source-level data policies | `EOIP-engg-doc-pkg/gaps-requirements.md:645`; audit line 1310 | P1 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | area fallback | PROVE |
| `REQ-CON-071` | `GAP-FED-001`: GAP-FED-001: Build a first-class Semantic Federation & Virtualization Layer for external sources without forcing materialization | `EOIP-engg-doc-pkg/gaps-implementation.md:536`; audit line 1312 | P1 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-CON-072` | `GAP-FED-002`: GAP-FED-002: Support policy-controlled choice between VIRTUAL, CACHE, MATERIALIZE, and HYBRID per source/entity type | `EOIP-engg-doc-pkg/gaps-requirements.md:118`; audit line 1313 | P1 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-CON-073` | `GAP-FED-003`: GAP-FED-003: Maintain explainable query plans showing which results came from HugeGraph versus live sources | `EOIP-engg-doc-pkg/gaps-requirements.md:119`; audit line 1314 | P1 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-CON-074` | `GAP-FED-004`: GAP-FED-004: Build federation adapters independently of HugeGraph so the product can query JDBC/REST/file sources while keeping HugeGraph as semantic control pl | `EOIP-engg-doc-pkg/gaps-requirements.md:120`; audit line 1315 | P1 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-CON-075` | `GAP-GITOPS-001`: GAP-GITOPS-001: Store ontology/schema source definitions in Git-compatible text formats | `EOIP-engg-doc-pkg/gaps-implementation.md:291`; audit line 1324 | P0 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | ID family | PROVE |
| `REQ-CON-076` | `GAP-GRAG-002`: GAP-GRAG-002: Use deterministic source-system relations first; model-generated relations second | `EOIP-engg-doc-pkg/gaps-requirements.md:359`; audit line 1337 | P2 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-CON-077` | `GAP-KFW-004`: GAP-KFW-004: Prevent source text from becoming executable agent instructions | `EOIP-engg-doc-pkg/gaps-requirements.md:738`; audit line 1360 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-CON-078` | `GAP-KFW-005`: GAP-KFW-005: Tag untrusted/externally sourced graph content | `EOIP-engg-doc-pkg/gaps-requirements.md:739`; audit line 1361 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-CON-079` | `GAP-KP-001`: GAP-KP-001: Catalog every graph, ontology, data source, connector, model, query, agent and knowledge product | `EOIP-engg-doc-pkg/gaps-implementation.md:539`; audit line 1369 | P1 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | subject triage | PROVE |
| `REQ-CON-080` | `GAP-KQ-005`: GAP-KQ-005: Quality must be measurable by source, project, graph, domain and release | `EOIP-engg-doc-pkg/gaps-requirements.md:504`; audit line 1378 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-CON-081` | `GAP-RULE-003`: GAP-RULE-003: Support retraction/recomputation when source assertions change | `EOIP-engg-doc-pkg/gaps-requirements.md:172`; audit line 1461 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | area fallback | PROVE |
| `REQ-CON-082` | `GAP-STUDIO-002`: GAP-STUDIO-002: Text source view for experts | `EOIP-engg-doc-pkg/gaps-requirements.md:604`; audit line 1486 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | area fallback | PROVE |
| `REQ-CON-083` | `GAP-TCO-001`: GAP-TCO-001: Provide transparent resource consumption, sizing calculator and offline license/deployment model | `EOIP-engg-doc-pkg/gaps-requirements.md:225`; audit line 1497 | P2 | IMPLEMENTED-UNVERIFIED | [CP-33](#cp-33) | subject triage | PROVE |
| `REQ-CON-084` | `GAP-TRUTH-003`: GAP-TRUTH-003: Store source authority score | `EOIP-engg-doc-pkg/gaps-requirements.md:472`; audit line 1513 | P1 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | area fallback | PROVE |
| `REQ-CON-085` | `MVP-FR-007`: Jira graph | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:105`; audit line 1685 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | subject triage | PROVE |
| `REQ-CON-086` | `MVP-P0`: &#124; MVP-P0 &#124; Reconstruction Baseline And Evidence Lock &#124; Freeze the source corpus, recreate repository structure, install dependencies, validate config files, preserve generated audit JSONs, and regenerate this requirem... | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md:44`; audit line 1709 | P0 | MISSED | [CP-16](#cp-16) | area fallback | TRACE/BUILD |
| `REQ-CON-087` | `MVP-P1`: &#124; MVP-P1 &#124; Contracts, Ontology, And Graph Core &#124; Implement source-event contracts, ontology manifest, graph store interface, memory backend, HugeGraph backend, graph schema bootstrap, identity resolution, provenance, ... | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md:45`; audit line 1710 | P1 | MISSED | [CP-17](#cp-17) | subject triage | TRACE/BUILD |
| `REQ-CON-088` | `NFR-02`: &#124; NFR-02 &#124; Security and governance &#124; Secrets, tokens, RBAC, destructive operations, audit logs, privacy controls, connector scopes, and deployment hardening must be explicit and testable. &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1094`; audit line 1726 | UNSTATED | MISSED | [CP-05](#cp-05) | subject triage | TRACE/BUILD |
| `REQ-CON-089` | `REL-06`: Live connector acceptance with real credentials | `KGF-MASTER-BACKLOG.md:175`; audit line 1768 | P0 | IMPLEMENTED-UNVERIFIED | [CP-36](#cp-36) | ID family | PROVE |
| `REQ-CON-090` | `REL-07`: Live Hubble/runtime validation, including source-bound code graph | `KGF-MASTER-BACKLOG.md:175`; audit line 1769 | P0 | IMPLEMENTED-UNVERIFIED | [CP-36](#cp-36) | ID family | PROVE |
| `REQ-CON-091` | `REQ-USER-IMPORT-001`: &#124; User-import proposal (former REQ-USER-IMPORT-001 is unverified) &#124; Original proposal retained in [ticket](ticket-20261004-001.md); no approved source exists &#124; No verified EOIP endpoint/stub/test for this proposed wor... | `EOIP-engg-doc-pkg/tickets/requirements-map.md:15`; audit line 1778 | UNSTATED | MISSED | [CP-07](#cp-07) | subject triage | TRACE/BUILD |
| `REQ-CON-092` | `SDLC-019.2`: - [ ] `SDLC-019.2` Resource-growth assertions | `eoip-phase4-2-requirements.md:1750`; audit line 1876 | UNSTATED | MISSED | [CP-32](#cp-32) | engine family | TRACE/BUILD |
| `REQ-CON-093` | `SDLC-031.2`: - [ ] `SDLC-031.2` Resource manager with queueing | `eoip-phase4-2-requirements.md:1975`; audit line 1936 | UNSTATED | MISSED | [CP-32](#cp-32) | engine family | TRACE/BUILD |
| `REQ-CON-094` | `SR-COM-005`: &#124; SR-COM-005 &#124; **Services:** onboarding, connector development, ontology engineering, NL tuning, training, compliance-pack onboarding, managed operations. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:1004`; audit line 1997 | P0 | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-CON-095` | `SR-COM-006`: &#124; SR-COM-006 &#124; **Partner program:** certification tracks (implementer, connector developer, ontology engineer), partner portal, deal registration, co-marketing assets. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:1005`; audit line 1998 | P1 | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-CON-096` | `SR-COM-010`: &#124; SR-COM-010 &#124; **Strategy decisions to record as ADRs:** open-core vs source-available vs closed; trademark and white-label rights; third-party component redistribution rights; IP assignment for plugins and marketplace... | `EOIP-engg-doc-pkg/super-requirements.md:1009`; audit line 2002 | P0 | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-CON-097` | `SR-CON-006`: &#124; SR-CON-006 &#124; **Evidence-first:** every returned fact carries source, method (asserted/derived/inferred/curated), confidence, freshness and policy-filter notice. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:103`; audit line 2010 | P0 | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-098` | `SR-DEP-003`: &#124; SR-DEP-003 &#124; **Offline delivery:** signed OCI image archives, model bundles, ontology/industry packs, connector catalog, docs, license file, checksum manifest; verified by an installer **preflight checker** (OS, kern... | `EOIP-engg-doc-pkg/super-requirements.md:924`; audit line 2021 | P0 | MISSED | [CP-31](#cp-31) | ID family | TRACE/BUILD |
| `REQ-CON-099` | `SR-EXT-003`: &#124; SR-EXT-003 &#124; **Admin APIs** cover tenants, users, config, branding, licenses, connectors, policies — enabling partner automation. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:778`; audit line 2030 | P0 | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-CON-100` | `SR-EXT-005`: &#124; SR-EXT-005 &#124; **Integration surface:** Slack/Teams-class ChatOps, ITSM (ServiceNow/Jira), CI/CD bots (PR impact comments, merge-risk gates), SIEM, email, calendar, BI tools (SR-ING-071), IDE extensions (VS Code at P0;... | `EOIP-engg-doc-pkg/super-requirements.md:780`; audit line 2032 | P0 | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-CON-101` | `SR-GDB-016`: &#124; SR-GDB-016 &#124; **Component license matrix:** every bundled and optional component is classified (permissive / weak copyleft / strong copyleft or network-copyleft / source-available / commercial). Anything other than pe... | `EOIP-engg-doc-pkg/super-requirements.md:221`; audit line 2054 | P0 | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-CON-102` | `SR-PRV-003`: &#124; SR-PRV-003 &#124; **Retention and legal hold** per class/tenant/source; automated expiry with crypto-shred option. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:850`; audit line 2158 | P0 | PARTIAL | [CP-09](#cp-09) | ID family | COMPLETE |
| `REQ-CON-103` | `SR-VDB-005`: &#124; SR-VDB-005 &#124; **Embedding governance:** embeddings are derived data; they inherit the classification and access policy of their source, are deleted when the source is erased (§14.3), and are re-generated on model chan... | `EOIP-engg-doc-pkg/super-requirements.md:231`; audit line 2232 | P0 | MISSED | [CP-20](#cp-20) | ID family | TRACE/BUILD |
| `REQ-CON-104` | `TASK-LEGAL-005`: - **TASK-LEGAL-005**: Define open-source contribution policy — what can be open-sourced (Community edition) vs. proprietary | `EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:38`; audit line 2371 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-CON-105` | `TASK-LEGAL-006`: - **TASK-LEGAL-006**: Review license implications of graph database connectors (Neo4j Community GPL, TigerGraph proprietary) | `EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:42`; audit line 2372 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-CON-106` | `TASK-LIC-005`: - **TASK-LIC-005**: Evaluate LLM provider options — OpenAI, Anthropic, open-source (Llama, Mistral) — cost vs quality | `EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:32`; audit line 2386 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-CON-107` | `TEST-FR-CONN-001`: &#124; FR-CONN-001 &#124; Connector SDK &#124; WP-CONNECTORS &#124; TEST-FR-CONN-001 &#124; AC-FR-CONN-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:15`; audit line 2501 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-108` | `TEST-FR-CONN-002`: &#124; FR-CONN-002 &#124; Connector SDK &#124; WP-CONNECTORS &#124; TEST-FR-CONN-002 &#124; AC-FR-CONN-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:16`; audit line 2502 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-109` | `TEST-FR-CONN-003`: &#124; FR-CONN-003 &#124; Connector SDK &#124; WP-CONNECTORS &#124; TEST-FR-CONN-003 &#124; AC-FR-CONN-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:17`; audit line 2503 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-110` | `TEST-FR-CONN-004`: &#124; FR-CONN-004 &#124; Connector SDK &#124; WP-CONNECTORS &#124; TEST-FR-CONN-004 &#124; AC-FR-CONN-004 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:18`; audit line 2504 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-111` | `TEST-FR-CONN-005`: &#124; FR-CONN-005 &#124; Connector SDK &#124; WP-CONNECTORS &#124; TEST-FR-CONN-005 &#124; AC-FR-CONN-005 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:19`; audit line 2505 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-112` | `TEST-FR-CONN-006`: &#124; FR-CONN-006 &#124; Connector SDK &#124; WP-CONNECTORS &#124; TEST-FR-CONN-006 &#124; AC-FR-CONN-006 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:20`; audit line 2506 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-113` | `TEST-FR-CONN-007`: &#124; FR-CONN-007 &#124; Connector SDK &#124; WP-CONNECTORS &#124; TEST-FR-CONN-007 &#124; AC-FR-CONN-007 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:21`; audit line 2507 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-114` | `WP-CONNECTORS-01`: ### WP-CONNECTORS-01 — Connector SDK | `EOIP-engg-doc-pkg/implementation/wp-connectors.md:27`; audit line 2631 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-115` | `WP-CONNECTORS-02`: ### WP-CONNECTORS-02 — Jira JSON connector | `EOIP-engg-doc-pkg/implementation/wp-connectors.md:36`; audit line 2632 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-116` | `WP-CONNECTORS-03`: ### WP-CONNECTORS-03 — Git repository connector | `EOIP-engg-doc-pkg/implementation/wp-connectors.md:45`; audit line 2633 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-117` | `WP-CONNECTORS-04`: ### WP-CONNECTORS-04 — GitLab metadata adapter | `EOIP-engg-doc-pkg/implementation/wp-connectors.md:54`; audit line 2634 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-118` | `WP-CONNECTORS-05`: ### WP-CONNECTORS-05 — Connector resiliency | `EOIP-engg-doc-pkg/implementation/wp-connectors.md:63`; audit line 2635 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-119` | `WP-CONNECTORS-06`: ### WP-CONNECTORS-06 — Dry run and replay | `EOIP-engg-doc-pkg/implementation/wp-connectors.md:72`; audit line 2636 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-120` | `WP-CONNECTORS-07`: ### WP-CONNECTORS-07 — Source deletion semantics | `EOIP-engg-doc-pkg/implementation/wp-connectors.md:81`; audit line 2637 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-121` | `WP-CONNECTORS-08`: ### WP-CONNECTORS-08 — Confluence connector | `EOIP-engg-doc-pkg/implementation/wp-connectors.md:90`; audit line 2638 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-CON-122` | `WP-CONNECTORS-09`: ### WP-CONNECTORS-09 — ServiceNow connector | `EOIP-engg-doc-pkg/implementation/wp-connectors.md:99`; audit line 2639 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |

### A.6 DEV: 143 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-DEV-001` | `AC-14`: &#124; AC-14 &#124; New components have > 80% test coverage &#124; N/A &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1045`; audit line 112 | UNSTATED | MISSED | [CP-02](#cp-02) | explicit | TRACE/BUILD |
| `REQ-DEV-002` | `AC-FR-VALID-001`: &#124; FR-VALID-001 &#124; Validation &#124; WP-VALIDATION &#124; TEST-FR-VALID-001 &#124; AC-FR-VALID-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:59`; audit line 209 | UNSTATED | MISSED | [CP-17](#cp-17) | ID family | TRACE/BUILD |
| `REQ-DEV-003` | `AC-FR-VALID-002`: &#124; FR-VALID-002 &#124; Validation &#124; WP-VALIDATION &#124; TEST-FR-VALID-002 &#124; AC-FR-VALID-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:60`; audit line 210 | UNSTATED | MISSED | [CP-17](#cp-17) | ID family | TRACE/BUILD |
| `REQ-DEV-004` | `AC-FR-VALID-003`: &#124; FR-VALID-003 &#124; Validation &#124; WP-VALIDATION &#124; TEST-FR-VALID-003 &#124; AC-FR-VALID-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:61`; audit line 211 | UNSTATED | MISSED | [CP-17](#cp-17) | ID family | TRACE/BUILD |
| `REQ-DEV-005` | `AC-FR-VSCODE-001`: &#124; FR-VSCODE-001 &#124; VS Code &#124; WP-EXPERIENCE &#124; TEST-FR-VSCODE-001 &#124; AC-FR-VSCODE-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:80`; audit line 212 | UNSTATED | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-DEV-006` | `AC-FR-VSCODE-002`: &#124; FR-VSCODE-002 &#124; VS Code &#124; WP-EXPERIENCE &#124; TEST-FR-VSCODE-002 &#124; AC-FR-VSCODE-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:81`; audit line 213 | UNSTATED | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-DEV-007` | `AC-NFR-MAINT-001`: &#124; NFR-MAINT-001 &#124; Architecture &#124; WP-FOUNDATION &#124; TEST-NFR-MAINT-001 &#124; AC-NFR-MAINT-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:94`; audit line 214 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-008` | `AIDLC-001.4`: - [ ] `AIDLC-001.4` Reproduce a past answer in a test | `eoip-phase4-2-requirements.md:2055`; audit line 303 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-DEV-009` | `AIDLC-004.3`: - [ ] `AIDLC-004.3` CI gate with thresholds | `eoip-phase4-2-requirements.md:2167`; audit line 317 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-DEV-010` | `AIDLC-009.3`: - [ ] `AIDLC-009.3` Quality drift alert | `eoip-phase4-2-requirements.md:2316`; audit line 342 | UNSTATED | MISSED | [CP-10](#cp-10) | subject triage | TRACE/BUILD |
| `REQ-DEV-011` | `AIDLC-010.1`: - [ ] `AIDLC-010.1` Pipeline from dataset to registry | `eoip-phase4-2-requirements.md:2144`; audit line 345 | UNSTATED | MISSED | [CP-34](#cp-34) | subject triage | TRACE/BUILD |
| `REQ-DEV-012` | `AIDLC-011.3`: - [ ] `AIDLC-011.3` Nightly CI run | `eoip-phase4-2-requirements.md:2222`; audit line 352 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-DEV-013` | `AIDLC-016.2`: - [ ] `AIDLC-016.2` Enforcement test: a loop cannot exceed its tier | `eoip-phase4-2-requirements.md:2295`; audit line 376 | UNSTATED | MISSED | [CP-10](#cp-10) | subject triage | TRACE/BUILD |
| `REQ-DEV-014` | `BASE-01`: Create the requirement registry | `KGF-MASTER-BACKLOG.md:33`; audit line 379 | P0 | PARTIAL | [CP-00](#cp-00) | ID family | COMPLETE |
| `REQ-DEV-015` | `BASE-02`: Add the @pytest.mark.req marker and a requirement-to-test map | `KGF-MASTER-BACKLOG.md:215`; audit line 380 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | ID family | PROVE |
| `REQ-DEV-016` | `BASE-03`: Retro-tag existing tests with requirement IDs | `KGF-MASTER-BACKLOG.md:218`; audit line 381 | P0 | PARTIAL | [CP-00](#cp-00) | ID family | COMPLETE |
| `REQ-DEV-017` | `BASE-04`: Verification sweep of all 434 audit-gap IDs | `KGF-MASTER-BACKLOG.md:160`; audit line 382 | P0 | PARTIAL | [CP-00](#cp-00) | ID family | COMPLETE |
| `REQ-DEV-018` | `CG-DEV-2026-10-11`: **Document ID:** AUDIT-GAPS-CG-DEV-2026-10-11 | `EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:3`; audit line 385 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-019` | `CG-GAP-003`: Reconcile documentation drift | `EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:64`; audit line 389 | P0 | PARTIAL | [CP-35](#cp-35) | subject triage | COMPLETE |
| `REQ-DEV-020` | `CORE-002.1`: - [x] `CORE-002.1` VerifierRegistry with register/unregister/compose operations | `eoip-phase4-2-requirements.md:265`; audit line 425 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-DEV-021` | `G2-P0-001`: - **G2 Phased Enterprise Registry:** 364 requirements across P0–P10 (`G2-P0-001` through `G2-P10-040`) — *100% Implemented & Verified* | `EOIP-engg-doc-pkg/KGR-g-requirements.md:74`; audit line 796 | P0 | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-022` | `G2-P10-040`: - **G2 Phased Enterprise Registry:** 364 requirements across P0–P10 (`G2-P0-001` through `G2-P10-040`) — *100% Implemented & Verified* | `EOIP-engg-doc-pkg/KGR-g-requirements.md:74`; audit line 799 | P0 | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-023` | `G2-SYNC-011`: G2-SYNC-011 — Rebuild equivalence test | `EOIP-engg-doc-pkg/gaps2-requirements.md:679`; audit line 945 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-DEV-024` | `GAP-001`: - **Original Gap Registry:** 296 requirements (`GAP-001` through `GAP-296`) — *100% Implemented & Verified* | `EOIP-engg-doc-pkg/KGR-g-requirements.md:73`; audit line 1197 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-025` | `GAP-296`: - **Original Gap Registry:** 296 requirements (`GAP-001` through `GAP-296`) — *100% Implemented & Verified* | `EOIP-engg-doc-pkg/KGR-g-requirements.md:73`; audit line 1206 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-026` | `GAP-ARCH-004`: GAP-ARCH-004: Support CI gate mode | `EOIP-engg-doc-pkg/gaps-requirements.md:537`; audit line 1237 | P0 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-DEV-027` | `GAP-CONTRACT-006`: GAP-CONTRACT-006: Expose contract tests to CI/CD | `EOIP-engg-doc-pkg/gaps-requirements.md:444`; audit line 1268 | P2 | IMPLEMENTED-UNVERIFIED | [CP-02](#cp-02) | subject triage | PROVE |
| `REQ-DEV-028` | `GAP-CP-002`: GAP-CP-002: Maintain a canonical entity registry | `EOIP-engg-doc-pkg/gaps-requirements.md:400`; audit line 1270 | P2 | IMPLEMENTED-UNVERIFIED | [CP-35](#cp-35) | area fallback | PROVE |
| `REQ-DEV-029` | `GAP-CP-003`: GAP-CP-003: Maintain canonical relationship registry | `EOIP-engg-doc-pkg/gaps-requirements.md:401`; audit line 1271 | P2 | IMPLEMENTED-UNVERIFIED | [CP-35](#cp-35) | area fallback | PROVE |
| `REQ-DEV-030` | `GAP-KGCI-001`: GAP-KGCI-001: CLI runnable in CI | `EOIP-engg-doc-pkg/gaps-requirements.md:820`; audit line 1365 | P0 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | subject triage | PROVE |
| `REQ-DEV-031` | `GAP-KQ-001`: GAP-KQ-001: Define per-domain quality SLOs | `EOIP-engg-doc-pkg/gaps-implementation.md:293`; audit line 1374 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-DEV-032` | `GAP-KQ-003`: GAP-KQ-003: Quality SLO violations generate actionable findings | `EOIP-engg-doc-pkg/gaps-requirements.md:502`; audit line 1376 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-DEV-033` | `GAP-KQ-004`: GAP-KQ-004: Quality score is not one opaque number; show component dimensions | `EOIP-engg-doc-pkg/gaps-requirements.md:503`; audit line 1377 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-DEV-034` | `H-03`: Integration test suite | `KGF-MASTER-BACKLOG.md:272`; audit line 1562 | P0 | IMPLEMENTED-UNVERIFIED | [CP-02](#cp-02) | subject triage | PROVE |
| `REQ-DEV-035` | `INFRA-003.3`: - [x] `INFRA-003.3` CD workflow stages in GitHub Actions | `eoip-phase4-2-requirements.md:860`; audit line 1583 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-DEV-036` | `KGR-G-025`: Universal 55-Database Registry & Adapter SPI | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:229`; audit line 1634 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-DEV-037` | `PRE-002`: Pre-flight: register Phase 4 in the KGF registry and adopt the Universal Definition of Done | `eoip-phase4-2-requirements.md:18`; audit line 1758 | P0 | MISSED | [CP-00](#cp-00) | ID family | TRACE/BUILD |
| `REQ-DEV-038` | `PRE-002.1`: - [x] `PRE-002.1` All Phase 4 IDs (and accepted suggestions) are rows in requirements-registry.json (KGF BASE-01) with the cross-IDs from the overlap map. | `eoip-phase4-2-requirements.md:209`; audit line 1759 | UNSTATED | MISSED | [CP-00](#cp-00) | ID family | TRACE/BUILD |
| `REQ-DEV-039` | `PRE-002.2`: - [x] `PRE-002.2` Tests for Phase 4 carry @pytest.mark.req("<ID>") and commits use [ID] (KGF BASE-02). | `eoip-phase4-2-requirements.md:210`; audit line 1760 | UNSTATED | MISSED | [CP-00](#cp-00) | ID family | TRACE/BUILD |
| `REQ-DEV-040` | `S-03`: CI/CD pipeline | `requirements-registry.json:1`; audit line 1781 | P1 | IMPLEMENTED-UNVERIFIED | [CP-02](#cp-02) | subject triage | PROVE |
| `REQ-DEV-041` | `S-04`: Developer documentation | `requirements-registry.json:1`; audit line 1782 | P1 | IMPLEMENTED-UNVERIFIED | [CP-35](#cp-35) | subject triage | PROVE |
| `REQ-DEV-042` | `SDLC-001.1`: - [ ] `SDLC-001.1` CI fails a PR with no valid requirement ID | `eoip-phase4-2-requirements.md:1409`; audit line 1785 | UNSTATED | MISSED | [CP-00](#cp-00) | engine family | TRACE/BUILD |
| `REQ-DEV-043` | `SDLC-001.2`: - [ ] `SDLC-001.2` CI fails when a done requirement has no tagged test | `eoip-phase4-2-requirements.md:1410`; audit line 1786 | UNSTATED | MISSED | [CP-00](#cp-00) | engine family | TRACE/BUILD |
| `REQ-DEV-044` | `SDLC-001.3`: - [ ] `SDLC-001.3` Registry and Markdown checkbox state are reconciled by a script | `eoip-phase4-2-requirements.md:1411`; audit line 1787 | UNSTATED | MISSED | [CP-00](#cp-00) | engine family | TRACE/BUILD |
| `REQ-DEV-045` | `SDLC-002.3`: - [ ] `SDLC-002.3` Requirement registry rows link to ADRs | `eoip-phase4-2-requirements.md:1430`; audit line 1792 | UNSTATED | MISSED | [CP-01](#cp-01) | engine family | TRACE/BUILD |
| `REQ-DEV-046` | `SDLC-002.4`: - [ ] `SDLC-002.4` ADR numbering is checked in CI | `eoip-phase4-2-requirements.md:1431`; audit line 1793 | UNSTATED | MISSED | [CP-01](#cp-01) | engine family | TRACE/BUILD |
| `REQ-DEV-047` | `SDLC-004.1`: - [ ] `SDLC-004.1` Descriptor and registry implemented | `eoip-phase4-2-requirements.md:1468`; audit line 1800 | UNSTATED | MISSED | [CP-07](#cp-07) | engine family | TRACE/BUILD |
| `REQ-DEV-048` | `SDLC-004.3`: - [ ] `SDLC-004.3` Startup test fails on an unmounted router (would have caught CG-GAP-001) | `eoip-phase4-2-requirements.md:1470`; audit line 1802 | UNSTATED | MISSED | [CP-07](#cp-07) | engine family | TRACE/BUILD |
| `REQ-DEV-049` | `SDLC-009.3`: - [ ] `SDLC-009.3` TEST-001 scenarios prove graceful degradation | `eoip-phase4-2-requirements.md:1565`; audit line 1827 | UNSTATED | MISSED | [CP-10](#cp-10) | engine family | TRACE/BUILD |
| `REQ-DEV-050` | `SDLC-010.1`: - [ ] `SDLC-010.1` Linters and type checker in CI | `eoip-phase4-2-requirements.md:1584`; audit line 1830 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-DEV-051` | `SDLC-012.3`: - [ ] `SDLC-012.3` Used by TEST-002, TEST-001 and COMPLY-002 tests | `eoip-phase4-2-requirements.md:1623`; audit line 1842 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-DEV-052` | `SDLC-013`: ###### SDLC-013: Test hygiene and CI speed | `eoip-phase4-2-requirements.md:1626`; audit line 1844 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-DEV-053` | `SDLC-017.1`: - [ ] `SDLC-017.1` Contract suite runs in CI | `eoip-phase4-2-requirements.md:1714`; audit line 1865 | UNSTATED | MISSED | [CP-29](#cp-29) | engine family | TRACE/BUILD |
| `REQ-DEV-054` | `SDLC-018.1`: - [ ] `SDLC-018.1` E2E suite in CI | `eoip-phase4-2-requirements.md:1732`; audit line 1870 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-DEV-055` | `SDLC-020.1`: - [ ] `SDLC-020.1` Upgrade test with seeded data | `eoip-phase4-2-requirements.md:1766`; audit line 1880 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-DEV-056` | `SDLC-022.3`: - [ ] `SDLC-022.3` Signed artifacts verified in CI | `eoip-phase4-2-requirements.md:1807`; audit line 1892 | UNSTATED | MISSED | [CP-33](#cp-33) | engine family | TRACE/BUILD |
| `REQ-DEV-057` | `SDLC-024.1`: - [ ] `SDLC-024.1` Bundle build in CI | `eoip-phase4-2-requirements.md:1842`; audit line 1900 | UNSTATED | MISSED | [CP-27](#cp-27) | engine family | TRACE/BUILD |
| `REQ-DEV-058` | `SDLC-026`: - [x] `TEST-001.A2` Results feed SLOs and runbooks (SDLC-026). Unit tests for the fault injector itself. *(added by review)* | `eoip-phase4-2-requirements.md:1238`; audit line 1909 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-DEV-059` | `SDLC-029.2`: - [ ] `SDLC-029.2` Rotation test with no downtime | `eoip-phase4-2-requirements.md:1938`; audit line 1926 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-DEV-060` | `SDLC-031`: - [x] `TEST-004.A2` Baselines are tied to a hardware profile (SDLC-031). Unit tests for the comparison logic. *(added by review)* | `eoip-phase4-2-requirements.md:1297`; audit line 1934 | UNSTATED | MISSED | [CP-32](#cp-32) | engine family | TRACE/BUILD |
| `REQ-DEV-061` | `SDLC-032.2`: - [ ] `SDLC-032.2` Snippets executed in CI | `eoip-phase4-2-requirements.md:1995`; audit line 1941 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-DEV-062` | `SDLC-032.4`: - [ ] `SDLC-032.4` Facts (route counts, test counts) injected from generated files | `eoip-phase4-2-requirements.md:1997`; audit line 1943 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-DEV-063` | `SDLC-033`: ###### SDLC-033: Developer experience: one-command bootstrap, CLI, sample data and first-run | `eoip-phase4-2-requirements.md:1999`; audit line 1944 | UNSTATED | MISSED | [CP-29](#cp-29) | engine family | TRACE/BUILD |
| `REQ-DEV-064` | `SR-EXT-013`: &#124; SR-EXT-013 &#124; **Plugin test kit** and scaffolding CLI; contract tests mandatory for marketplace listing. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:789`; audit line 2036 | P1 | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-DEV-065` | `TASK-CTO-005`: - **TASK-CTO-005**: Establish code review standards, PR process, and quality gates | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:37`; audit line 2291 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-066` | `TASK-DEV-001`: - **TASK-DEV-001**: Token Format Engines (CORE-001) | `EOIP-engg-doc-pkg/roles/Developer_tasks.md:21`; audit line 2305 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-067` | `TASK-DEV-002`: - **TASK-DEV-002**: Verification Engine (CORE-002) | `EOIP-engg-doc-pkg/roles/Developer_tasks.md:27`; audit line 2306 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-068` | `TASK-DEV-003`: - **TASK-DEV-003**: Intent Router (CORE-003) | `EOIP-engg-doc-pkg/roles/Developer_tasks.md:32`; audit line 2307 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-069` | `TASK-DEV-004`: - **TASK-DEV-004**: Graph-over-Graph (CORE-004) | `EOIP-engg-doc-pkg/roles/Developer_tasks.md:37`; audit line 2308 | UNSTATED | MISSED | [CP-13](#cp-13) | subject triage | TRACE/BUILD |
| `REQ-DEV-070` | `TASK-DEV-005`: - **TASK-DEV-005**: Loop-over-Loop (CORE-005) | `EOIP-engg-doc-pkg/roles/Developer_tasks.md:42`; audit line 2309 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-071` | `TASK-DEV-006`: - **TASK-DEV-006**: Token Budget (CORE-006) | `EOIP-engg-doc-pkg/roles/Developer_tasks.md:46`; audit line 2310 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-072` | `TASK-DEV-007`: - **TASK-DEV-007**: Cognitive Boundary Telemetry (AGENT-001) | `EOIP-engg-doc-pkg/roles/Developer_tasks.md:52`; audit line 2311 | UNSTATED | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-DEV-073` | `TASK-DEV-008`: - **TASK-DEV-008**: Entity Extraction Pipeline (AGENT-002) | `EOIP-engg-doc-pkg/roles/Developer_tasks.md:56`; audit line 2312 | UNSTATED | MISSED | [CP-15](#cp-15) | subject triage | TRACE/BUILD |
| `REQ-DEV-074` | `TASK-DEV-009`: - **TASK-DEV-009**: Agent Message Bus (AGENT-003) | `EOIP-engg-doc-pkg/roles/Developer_tasks.md:60`; audit line 2313 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-DEV-075` | `TASK-DEV-010`: - **TASK-DEV-010**: Fan-Out/Fan-In Stages (AGENT-004) | `EOIP-engg-doc-pkg/roles/Developer_tasks.md:63`; audit line 2314 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-DEV-076` | `TASK-DEV-011`: - **TASK-DEV-011**: Federated Graph Engine (GRAPH-001) | `EOIP-engg-doc-pkg/roles/Developer_tasks.md:66`; audit line 2315 | UNSTATED | MISSED | [CP-13](#cp-13) | subject triage | TRACE/BUILD |
| `REQ-DEV-077` | `TASK-DEV-012`: - **TASK-DEV-012**: Temporal Retrieval (GRAPH-005) | `EOIP-engg-doc-pkg/roles/Developer_tasks.md:69`; audit line 2316 | UNSTATED | MISSED | [CP-18](#cp-18) | subject triage | TRACE/BUILD |
| `REQ-DEV-078` | `TASK-DEV-013`: - **TASK-DEV-013** through **TASK-DEV-030**: Remaining 18 engine implementations (see eoip-phase4-requirements.md for full specs) | `EOIP-engg-doc-pkg/roles/Developer_tasks.md:73`; audit line 2317 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-079` | `TASK-DEV-030`: - **TASK-DEV-013** through **TASK-DEV-030**: Remaining 18 engine implementations (see eoip-phase4-requirements.md for full specs) | `EOIP-engg-doc-pkg/roles/Developer_tasks.md:73`; audit line 2318 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-080` | `TASK-DEV-031`: - **TASK-DEV-031**: Fix `test_deployed_route_surface_contains_product_gate_routes` — wire `/api/v1/loops/catalog` endpoint | `EOIP-engg-doc-pkg/roles/Developer_tasks.md:76`; audit line 2319 | UNSTATED | MISSED | [CP-07](#cp-07) | subject triage | TRACE/BUILD |
| `REQ-DEV-081` | `TASK-DEV-032`: - **TASK-DEV-032**: Fix `test_intelligent_query_with_store` — assert `latency_ms >= 0` instead of `> 0` or add timing floor | `EOIP-engg-doc-pkg/roles/Developer_tasks.md:80`; audit line 2320 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-DEV-082` | `TASK-DM-003`: - **TASK-DM-003**: Track dependency chains across phases (e.g., CORE-001 blocks CORE-003, CORE-006, TEST-003) | `EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:23`; audit line 2323 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-DEV-083` | `TASK-LD-002`: - **TASK-LD-002**: Implement Verification & Guardrail Engine (CORE-002) — VerifierRegistry, 7+ rules, DynamicGuardrailInjector | `EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:16`; audit line 2352 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-084` | `TASK-LEGAL-011`: - **TASK-LEGAL-011**: EU AI Act compliance assessment — classify system risk level, documentation requirements | `EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:66`; audit line 2377 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-DEV-085` | `TASK-MKE-009`: - **TASK-MKE-009**: Set up and manage developer community (Discord or Slack) | `EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:46`; audit line 2403 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-DEV-086` | `TASK-MKT-009`: - **TASK-MKT-009**: Launch developer community — Discord/Slack, documentation site, tutorial content | `EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:54`; audit line 2415 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-DEV-087` | `TASK-MKT-014`: - **TASK-MKT-014**: Launch marketing website with product pages, pricing, documentation | `EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:78`; audit line 2420 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-DEV-088` | `TASK-QA-005`: - **TASK-QA-005**: Regression test full suite after Phase 1 integration | `EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:27`; audit line 2425 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-DEV-089` | `TASK-QA-006`: - **TASK-QA-006** through **TASK-QA-015**: Execute test plans for Phases 2-7 (per QA Lead test plans) | `EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:33`; audit line 2426 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-DEV-090` | `TASK-QA-015`: - **TASK-QA-006** through **TASK-QA-015**: Execute test plans for Phases 2-7 (per QA Lead test plans) | `EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:33`; audit line 2427 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-DEV-091` | `TASK-QA-019`: - **TASK-QA-019**: Write Hypothesis property-based tests for token format round-trips (TEST-003) | `EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:48`; audit line 2431 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-DEV-092` | `TASK-QAL-001`: - **TASK-QAL-001**: Define test pyramid for EOIP — unit (70%), integration (20%), e2e (10%) | `EOIP-engg-doc-pkg/roles/QALead_tasks.md:11`; audit line 2434 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-DEV-093` | `TASK-QAL-002`: - **TASK-QAL-002**: Define quality gates for each Phase 4 requirement | `EOIP-engg-doc-pkg/roles/QALead_tasks.md:17`; audit line 2435 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-DEV-094` | `TASK-QAL-004`: - **TASK-QAL-004**: Define regression test suite covering critical paths across 21+ engines | `EOIP-engg-doc-pkg/roles/QALead_tasks.md:28`; audit line 2437 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-DEV-095` | `TASK-QAL-007`: - **TASK-QAL-007**: Phase 6 test infrastructure — chaos tests (TEST-001), load tests (TEST-002), property-based (TEST-003), perf regression (TEST-004), a11y (TEST-005) | `EOIP-engg-doc-pkg/roles/QALead_tasks.md:41`; audit line 2440 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-DEV-096` | `TEST-001`: Chaos Engineering Framework | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:888`; audit line 2464 | P2 | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-097` | `TEST-001.1`: - [x] `TEST-001.1` Fault injection framework | `eoip-phase4-2-requirements.md:1233`; audit line 2465 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-098` | `TEST-001.2`: - [x] `TEST-001.2` 5+ chaos scenarios | `eoip-phase4-2-requirements.md:1234`; audit line 2466 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-099` | `TEST-001.3`: - [x] `TEST-001.3` Recovery verification | `eoip-phase4-2-requirements.md:1235`; audit line 2467 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-100` | `TEST-001.4`: - [x] `TEST-001.4` CI integration (optional runs) | `eoip-phase4-2-requirements.md:1236`; audit line 2468 | UNSTATED | MISSED | [CP-02](#cp-02) | subject triage | TRACE/BUILD |
| `REQ-DEV-101` | `TEST-002`: Load Testing Framework | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:904`; audit line 2469 | P1 | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-DEV-102` | `TEST-002.1`: - [x] `TEST-002.1` Load test scripts | `eoip-phase4-2-requirements.md:1253`; audit line 2470 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-DEV-103` | `TEST-002.2`: - [x] `TEST-002.2` 4+ load scenarios | `eoip-phase4-2-requirements.md:1254`; audit line 2471 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-DEV-104` | `TEST-002.3`: - [x] `TEST-002.3` Latency and throughput targets | `eoip-phase4-2-requirements.md:1255`; audit line 2472 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-DEV-105` | `TEST-002.4`: - [x] `TEST-002.4` CI-runnable (optional) | `eoip-phase4-2-requirements.md:1256`; audit line 2473 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-DEV-106` | `TEST-003`: Property-Based & Fuzz Testing | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:920`; audit line 2474 | P2 | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-107` | `TEST-003.1`: - [x] `TEST-003.1` Hypothesis test suite | `eoip-phase4-2-requirements.md:1272`; audit line 2475 | UNSTATED | MISSED | [CP-02](#cp-02) | subject triage | TRACE/BUILD |
| `REQ-DEV-108` | `TEST-003.2`: - [x] `TEST-003.2` Fuzz tests for serialization | `eoip-phase4-2-requirements.md:1273`; audit line 2476 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-109` | `TEST-003.3`: - [x] `TEST-003.3` Property tests for query engine | `eoip-phase4-2-requirements.md:1274`; audit line 2477 | UNSTATED | MISSED | [CP-14](#cp-14) | subject triage | TRACE/BUILD |
| `REQ-DEV-110` | `TEST-003.4`: - [x] `TEST-003.4` CI integration | `eoip-phase4-2-requirements.md:1275`; audit line 2478 | UNSTATED | MISSED | [CP-02](#cp-02) | subject triage | TRACE/BUILD |
| `REQ-DEV-111` | `TEST-004`: Performance Regression Detection in CI | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:935`; audit line 2479 | P1 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | subject triage | PROVE |
| `REQ-DEV-112` | `TEST-004.1`: - [x] `TEST-004.1` Benchmark runner in CI workflow | `eoip-phase4-2-requirements.md:1292`; audit line 2480 | UNSTATED | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-DEV-113` | `TEST-004.2`: - [x] `TEST-004.2` Baseline comparison | `eoip-phase4-2-requirements.md:1293`; audit line 2481 | UNSTATED | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-DEV-114` | `TEST-004.3`: - [x] `TEST-004.3` Configurable regression thresholds | `eoip-phase4-2-requirements.md:1294`; audit line 2482 | UNSTATED | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-DEV-115` | `TEST-004.4`: - [x] `TEST-004.4` PR performance report | `eoip-phase4-2-requirements.md:1295`; audit line 2483 | UNSTATED | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-DEV-116` | `TEST-005`: Accessibility Testing | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:951`; audit line 2484 | P2 | IMPLEMENTED-UNVERIFIED | [CP-24](#cp-24) | subject triage | PROVE |
| `REQ-DEV-117` | `TEST-005.1`: - [x] `TEST-005.1` axe-core test integration | `eoip-phase4-2-requirements.md:1312`; audit line 2485 | UNSTATED | MISSED | [CP-24](#cp-24) | subject triage | TRACE/BUILD |
| `REQ-DEV-118` | `TEST-005.2`: - [x] `TEST-005.2` WCAG 2.1 AA compliance | `eoip-phase4-2-requirements.md:1313`; audit line 2486 | UNSTATED | MISSED | [CP-24](#cp-24) | subject triage | TRACE/BUILD |
| `REQ-DEV-119` | `TEST-005.3`: - [x] `TEST-005.3` CI gate for a11y violations | `eoip-phase4-2-requirements.md:1314`; audit line 2487 | UNSTATED | MISSED | [CP-24](#cp-24) | subject triage | TRACE/BUILD |
| `REQ-DEV-120` | `TEST-FR-CODE-001`: &#124; FR-CODE-001 &#124; Code Graph &#124; WP-CODEGRAPH &#124; TEST-FR-CODE-001 &#124; AC-FR-CODE-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:46`; audit line 2495 | UNSTATED | MISSED | [CP-37](#cp-37) | ID family | TRACE/BUILD |
| `REQ-DEV-121` | `TEST-FR-CODE-002`: &#124; FR-CODE-002 &#124; Code Graph &#124; WP-CODEGRAPH &#124; TEST-FR-CODE-002 &#124; AC-FR-CODE-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:47`; audit line 2496 | UNSTATED | MISSED | [CP-37](#cp-37) | ID family | TRACE/BUILD |
| `REQ-DEV-122` | `TEST-FR-CODE-003`: &#124; FR-CODE-003 &#124; Code Graph &#124; WP-CODEGRAPH &#124; TEST-FR-CODE-003 &#124; AC-FR-CODE-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:48`; audit line 2497 | UNSTATED | MISSED | [CP-37](#cp-37) | ID family | TRACE/BUILD |
| `REQ-DEV-123` | `TEST-FR-CODE-004`: &#124; FR-CODE-004 &#124; Code Graph &#124; WP-CODEGRAPH &#124; TEST-FR-CODE-004 &#124; AC-FR-CODE-004 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:49`; audit line 2498 | UNSTATED | MISSED | [CP-37](#cp-37) | ID family | TRACE/BUILD |
| `REQ-DEV-124` | `TEST-FR-CODE-005`: &#124; FR-CODE-005 &#124; Code Graph &#124; WP-CODEGRAPH &#124; TEST-FR-CODE-005 &#124; AC-FR-CODE-005 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:50`; audit line 2499 | UNSTATED | MISSED | [CP-37](#cp-37) | ID family | TRACE/BUILD |
| `REQ-DEV-125` | `TEST-FR-CONF-001`: &#124; FR-CONF-001 &#124; Platform &#124; WP-CONNECTORS &#124; TEST-FR-CONF-001 &#124; AC-FR-CONF-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:22`; audit line 2500 | UNSTATED | MISSED | [CP-16](#cp-16) | subject triage | TRACE/BUILD |
| `REQ-DEV-126` | `TEST-FR-ID-001`: &#124; FR-ID-001 &#124; Identity &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-ID-001 &#124; AC-FR-ID-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:43`; audit line 2518 | UNSTATED | MISSED | [CP-17](#cp-17) | ID family | TRACE/BUILD |
| `REQ-DEV-127` | `TEST-FR-ID-002`: &#124; FR-ID-002 &#124; Identity &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-ID-002 &#124; AC-FR-ID-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:44`; audit line 2519 | UNSTATED | MISSED | [CP-17](#cp-17) | ID family | TRACE/BUILD |
| `REQ-DEV-128` | `TEST-FR-MCP-001`: &#124; FR-MCP-001 &#124; MCP &#124; WP-MCP &#124; TEST-FR-MCP-001 &#124; AC-FR-MCP-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:74`; audit line 2525 | UNSTATED | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-DEV-129` | `TEST-FR-MCP-002`: &#124; FR-MCP-002 &#124; MCP &#124; WP-MCP &#124; TEST-FR-MCP-002 &#124; AC-FR-MCP-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:75`; audit line 2526 | UNSTATED | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-DEV-130` | `TEST-FR-MEM-001`: &#124; FR-MEM-001 &#124; Memory &#124; WP-AGENT-MEMORY &#124; TEST-FR-MEM-001 &#124; AC-FR-MEM-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:73`; audit line 2527 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-DEV-131` | `TEST-FR-ONTO-001`: &#124; FR-ONTO-001 &#124; Ontology &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-ONTO-001 &#124; AC-FR-ONTO-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:39`; audit line 2528 | UNSTATED | MISSED | [CP-12](#cp-12) | ID family | TRACE/BUILD |
| `REQ-DEV-132` | `TEST-FR-ONTO-002`: &#124; FR-ONTO-002 &#124; Ontology &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-ONTO-002 &#124; AC-FR-ONTO-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:40`; audit line 2529 | UNSTATED | MISSED | [CP-12](#cp-12) | ID family | TRACE/BUILD |
| `REQ-DEV-133` | `TEST-FR-SNOW-001`: &#124; FR-SNOW-001 &#124; Platform &#124; WP-CONNECTORS &#124; TEST-FR-SNOW-001 &#124; AC-FR-SNOW-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:23`; audit line 2546 | UNSTATED | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-DEV-134` | `TEST-FR-TEMP-001`: &#124; FR-TEMP-001 &#124; Temporal &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-TEMP-001 &#124; AC-FR-TEMP-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:45`; audit line 2547 | UNSTATED | MISSED | [CP-18](#cp-18) | ID family | TRACE/BUILD |
| `REQ-DEV-135` | `TEST-FR-VALID-001`: &#124; FR-VALID-001 &#124; Validation &#124; WP-VALIDATION &#124; TEST-FR-VALID-001 &#124; AC-FR-VALID-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:59`; audit line 2550 | UNSTATED | MISSED | [CP-17](#cp-17) | ID family | TRACE/BUILD |
| `REQ-DEV-136` | `TEST-FR-VALID-002`: &#124; FR-VALID-002 &#124; Validation &#124; WP-VALIDATION &#124; TEST-FR-VALID-002 &#124; AC-FR-VALID-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:60`; audit line 2551 | UNSTATED | MISSED | [CP-17](#cp-17) | ID family | TRACE/BUILD |
| `REQ-DEV-137` | `TEST-FR-VALID-003`: &#124; FR-VALID-003 &#124; Validation &#124; WP-VALIDATION &#124; TEST-FR-VALID-003 &#124; AC-FR-VALID-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:61`; audit line 2552 | UNSTATED | MISSED | [CP-17](#cp-17) | ID family | TRACE/BUILD |
| `REQ-DEV-138` | `TEST-FR-VSCODE-001`: &#124; FR-VSCODE-001 &#124; VS Code &#124; WP-EXPERIENCE &#124; TEST-FR-VSCODE-001 &#124; AC-FR-VSCODE-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:80`; audit line 2553 | UNSTATED | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-DEV-139` | `TEST-FR-VSCODE-002`: &#124; FR-VSCODE-002 &#124; VS Code &#124; WP-EXPERIENCE &#124; TEST-FR-VSCODE-002 &#124; AC-FR-VSCODE-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:81`; audit line 2554 | UNSTATED | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-DEV-140` | `TEST-NFR-MAINT-001`: &#124; NFR-MAINT-001 &#124; Architecture &#124; WP-FOUNDATION &#124; TEST-NFR-MAINT-001 &#124; AC-NFR-MAINT-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:94`; audit line 2555 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-141` | `TEST-NFR-PRIV-001`: &#124; NFR-PRIV-001 &#124; Privacy &#124; WP-SECURITY-OPS &#124; TEST-NFR-PRIV-001 &#124; AC-NFR-PRIV-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:95`; audit line 2559 | UNSTATED | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-DEV-142` | `TEST-NFR-REL-001`: &#124; NFR-REL-001 &#124; Reliability &#124; WP-SECURITY-OPS &#124; TEST-NFR-REL-001 &#124; AC-NFR-REL-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:89`; audit line 2560 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |
| `REQ-DEV-143` | `TEST-NFR-REL-002`: &#124; NFR-REL-002 &#124; Reliability &#124; WP-SECURITY-OPS &#124; TEST-NFR-REL-002 &#124; AC-NFR-REL-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:90`; audit line 2561 | UNSTATED | MISSED | [CP-35](#cp-35) | area fallback | TRACE/BUILD |

### A.7 GRA: 307 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-GRA-001` | `AC-01`: &#124; AC-01 &#124; User can switch between 10 graph types with appropriate visualization &#124; Graphify: 1 type, Bloom: 1, Gephi: 1 &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1032`; audit line 99 | UNSTATED | MISSED | [CP-23](#cp-23) | subject triage | TRACE/BUILD |
| `REQ-GRA-002` | `AC-02`: &#124; AC-02 &#124; 8-tab inspector shows properties, relationships, impact, evidence, similarity, history, annotations, raw &#124; Graphify: properties only &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1033`; audit line 100 | UNSTATED | MISSED | [CP-26](#cp-26) | subject triage | TRACE/BUILD |
| `REQ-GRA-003` | `AC-04`: &#124; AC-04 &#124; Centrality metrics computed and displayed as radar chart &#124; Gephi: desktop only, Bloom: GDS required &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1035`; audit line 102 | UNSTATED | MISSED | [CP-27](#cp-27) | subject triage | TRACE/BUILD |
| `REQ-GRA-004` | `AC-05`: &#124; AC-05 &#124; 12 layout algorithms available and switchable without data loss &#124; Graphify: 1, code2flow: 1 &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1036`; audit line 103 | UNSTATED | MISSED | [CP-23](#cp-23) | subject triage | TRACE/BUILD |
| `REQ-GRA-005` | `AC-07`: &#124; AC-07 &#124; Progressive WebGL rendering handles 50,000 nodes &#124; Graphify: 5K limit &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1038`; audit line 105 | UNSTATED | MISSED | [CP-23](#cp-23) | explicit | TRACE/BUILD |
| `REQ-GRA-006` | `AC-10`: &#124; AC-10 &#124; 10-dimensional filter state persists across graph type switches &#124; Graphify: label only &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1041`; audit line 108 | UNSTATED | MISSED | [CP-03](#cp-03) | subject triage | TRACE/BUILD |
| `REQ-GRA-007` | `AC-17`: &#124; AC-17 &#124; WebSocket real-time updates with fade-in animation &#124; Graphify: git hooks only &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1048`; audit line 115 | UNSTATED | MISSED | [CP-11](#cp-11) | subject triage | TRACE/BUILD |
| `REQ-GRA-008` | `AC-18`: &#124; AC-18 &#124; Graph diff shows added/removed/modified entities &#124; No free competitor has this &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1049`; audit line 116 | UNSTATED | MISSED | [CP-18](#cp-18) | subject triage | TRACE/BUILD |
| `REQ-GRA-009` | `AC-25`: &#124; AC-25 &#124; Community auto-labeling with user override and summary cards &#124; Graphify (basic labeling only, no override) &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1056`; audit line 123 | UNSTATED | MISSED | [CP-13](#cp-13) | subject triage | TRACE/BUILD |
| `REQ-GRA-010` | `AC-26`: &#124; AC-26 &#124; PR/change impact dashboard with community overlap detection &#124; Graphify (list only, no visual overlap) &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1057`; audit line 124 | UNSTATED | MISSED | [CP-18](#cp-18) | subject triage | TRACE/BUILD |
| `REQ-GRA-011` | `AC-32`: &#124; AC-32 &#124; Force-directed edge bundling declutters high-degree nodes &#124; yFiles (€9.2K) — KGR does it free &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1063`; audit line 130 | UNSTATED | MISSED | [CP-13](#cp-13) | area fallback | TRACE/BUILD |
| `REQ-GRA-012` | `AC-34`: &#124; AC-34 &#124; Self-contained interactive HTML export with search/filter/inspect &#124; Graphify (basic zoom only) — KGR adds full interaction &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1065`; audit line 132 | UNSTATED | MISSED | [CP-25](#cp-25) | subject triage | TRACE/BUILD |
| `REQ-GRA-013` | `AC-35`: &#124; AC-35 &#124; Automated graph report with 7 analysis sections &#124; Graphify (basic topology) — KGR adds centrality, health, recommendations &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1066`; audit line 133 | UNSTATED | MISSED | [CP-25](#cp-25) | subject triage | TRACE/BUILD |
| `REQ-GRA-014` | `AC-36`: &#124; AC-36 &#124; Hub exclusion filter with visual indicator of excluded nodes &#124; Graphify (flag only, no visual) &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1067`; audit line 134 | UNSTATED | MISSED | [CP-13](#cp-13) | subject triage | TRACE/BUILD |
| `REQ-GRA-015` | `AC-37`: &#124; AC-37 &#124; Surprising connection detection with cross-domain and absence analysis &#124; Graphify (basic ranking only) &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1068`; audit line 135 | UNSTATED | MISSED | [CP-13](#cp-13) | subject triage | TRACE/BUILD |
| `REQ-GRA-016` | `AC-38`: &#124; AC-38 &#124; Rule-based conditional styling with composable IF/THEN rules &#124; Neo4j Bloom, Linkurious (both commercial) — KGR does it free &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1069`; audit line 136 | UNSTATED | MISSED | [CP-13](#cp-13) | area fallback | TRACE/BUILD |
| `REQ-GRA-017` | `AC-39`: &#124; AC-39 &#124; Lasso and rectangle multi-selection for large graphs &#124; KeyLines, yFiles (commercial) — KGR does it free &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1070`; audit line 137 | UNSTATED | MISSED | [CP-13](#cp-13) | subject triage | TRACE/BUILD |
| `REQ-GRA-018` | `AC-40`: &#124; AC-40 &#124; URL deep linking encodes full graph state (filters, zoom, selection, layout) &#124; Neo4j Bloom (selection only) — KGR encodes full state &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1071`; audit line 138 | UNSTATED | MISSED | [CP-23](#cp-23) | subject triage | TRACE/BUILD |
| `REQ-GRA-019` | `AC-42`: &#124; AC-42 &#124; Investigation playbooks guide multi-step analysis workflows &#124; Graphistry (GPU-only, commercial) — KGR does it free &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1073`; audit line 140 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-GRA-020` | `AC-43`: &#124; AC-43 &#124; Cross-project graph merge with preview and undo &#124; Graphify (multi-repo, no preview) &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1074`; audit line 141 | UNSTATED | MISSED | [CP-13](#cp-13) | subject triage | TRACE/BUILD |
| `REQ-GRA-021` | `AC-44`: &#124; AC-44 &#124; 17 RAG patterns route queries to optimal retrieval strategy &#124; No graph viz tool has RAG &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1075`; audit line 142 | UNSTATED | MISSED | [CP-21](#cp-21) | subject triage | TRACE/BUILD |
| `REQ-GRA-022` | `AC-45`: &#124; AC-45 &#124; 40+ agent types with perceive-decide-act lifecycle &#124; No graph viz tool has agents &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1076`; audit line 143 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-GRA-023` | `AC-47`: &#124; AC-47 &#124; AI Explorer panel provides chat-based graph exploration with LLM-optional fallback &#124; Neo4j Bloom (NL, cloud-only) — KGR is local-first + multi-RAG &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1078`; audit line 145 | UNSTATED | MISSED | [CP-27](#cp-27) | subject triage | TRACE/BUILD |
| `REQ-GRA-024` | `AC-48`: &#124; AC-48 &#124; MCP tools expose RAG/agent/engineering capabilities to external clients &#124; Graphify (basic MCP) — KGR has full RAG+agent MCP &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1079`; audit line 146 | UNSTATED | MISSED | [CP-29](#cp-29) | subject triage | TRACE/BUILD |
| `REQ-GRA-025` | `AC-FR-CODE-001`: &#124; FR-CODE-001 &#124; Code Graph &#124; WP-CODEGRAPH &#124; TEST-FR-CODE-001 &#124; AC-FR-CODE-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:46`; audit line 154 | UNSTATED | MISSED | [CP-37](#cp-37) | ID family | TRACE/BUILD |
| `REQ-GRA-026` | `AC-FR-CODE-002`: &#124; FR-CODE-002 &#124; Code Graph &#124; WP-CODEGRAPH &#124; TEST-FR-CODE-002 &#124; AC-FR-CODE-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:47`; audit line 155 | UNSTATED | MISSED | [CP-37](#cp-37) | ID family | TRACE/BUILD |
| `REQ-GRA-027` | `AC-FR-CODE-003`: &#124; FR-CODE-003 &#124; Code Graph &#124; WP-CODEGRAPH &#124; TEST-FR-CODE-003 &#124; AC-FR-CODE-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:48`; audit line 156 | UNSTATED | MISSED | [CP-37](#cp-37) | ID family | TRACE/BUILD |
| `REQ-GRA-028` | `AC-FR-CODE-004`: &#124; FR-CODE-004 &#124; Code Graph &#124; WP-CODEGRAPH &#124; TEST-FR-CODE-004 &#124; AC-FR-CODE-004 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:49`; audit line 157 | UNSTATED | MISSED | [CP-37](#cp-37) | ID family | TRACE/BUILD |
| `REQ-GRA-029` | `AC-FR-CODE-005`: &#124; FR-CODE-005 &#124; Code Graph &#124; WP-CODEGRAPH &#124; TEST-FR-CODE-005 &#124; AC-FR-CODE-005 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:50`; audit line 158 | UNSTATED | MISSED | [CP-37](#cp-37) | ID family | TRACE/BUILD |
| `REQ-GRA-030` | `AC-FR-GRAPH-001`: &#124; FR-GRAPH-001 &#124; Graph Core &#124; WP-FOUNDATION &#124; TEST-FR-GRAPH-001 &#124; AC-FR-GRAPH-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:29`; audit line 167 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-031` | `AC-FR-GRAPH-002`: &#124; FR-GRAPH-002 &#124; Graph Core &#124; WP-FOUNDATION &#124; TEST-FR-GRAPH-002 &#124; AC-FR-GRAPH-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:30`; audit line 168 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-032` | `AC-FR-GRAPH-003`: &#124; FR-GRAPH-003 &#124; Graph Core &#124; WP-FOUNDATION &#124; TEST-FR-GRAPH-003 &#124; AC-FR-GRAPH-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:31`; audit line 169 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-033` | `AC-FR-GRAPH-004`: &#124; FR-GRAPH-004 &#124; Graph Core &#124; WP-FOUNDATION &#124; TEST-FR-GRAPH-004 &#124; AC-FR-GRAPH-004 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:32`; audit line 170 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-034` | `AC-FR-GRAPH-005`: &#124; FR-GRAPH-005 &#124; Graph Core &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-GRAPH-005 &#124; AC-FR-GRAPH-005 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:33`; audit line 171 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-035` | `AC-FR-GRAPH-006`: &#124; FR-GRAPH-006 &#124; Graph Core &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-GRAPH-006 &#124; AC-FR-GRAPH-006 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:34`; audit line 172 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-036` | `AC-FR-GRAPH-007`: &#124; FR-GRAPH-007 &#124; Graph Core &#124; WP-QUERY &#124; TEST-FR-GRAPH-007 &#124; AC-FR-GRAPH-007 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:35`; audit line 173 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-037` | `AC-FR-GRAPH-008`: &#124; FR-GRAPH-008 &#124; Graph Core &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-GRAPH-008 &#124; AC-FR-GRAPH-008 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:36`; audit line 174 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-038` | `AC-FR-GRAPH-009`: &#124; FR-GRAPH-009 &#124; Graph Core &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-GRAPH-009 &#124; AC-FR-GRAPH-009 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:37`; audit line 175 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-039` | `AC-FR-GRAPH-010`: &#124; FR-GRAPH-010 &#124; Graph Core &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-GRAPH-010 &#124; AC-FR-GRAPH-010 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:38`; audit line 176 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-040` | `AI-001.2`: - [x] `AI-001.2` Decision trace graph generation | `eoip-phase4-2-requirements.md:651`; audit line 257 | UNSTATED | MISSED | [CP-21](#cp-21) | engine family | TRACE/BUILD |
| `REQ-GRA-041` | `AI-007.1`: - [x] `AI-007.1` Bayesian inference over graph structures | `eoip-phase4-2-requirements.md:784`; audit line 294 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-042` | `AIDLC-003`: &#124; Measured quality targets &#124; AGENT-001, AGENT-002, GRAPH-004, AI-001, AI-002, AI-003, AI-007, COMPLY-002, MULTI-001 &#124; These are statistical components with no precision/recall, MRR/AUC, calibration or fidelity target.... | `eoip-phase4-2-requirements.md:139`; audit line 309 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-GRA-043` | `AIDLC-004`: &#124; Measured quality targets &#124; AGENT-001, AGENT-002, GRAPH-004, AI-001, AI-002, AI-003, AI-007, COMPLY-002, MULTI-001 &#124; These are statistical components with no precision/recall, MRR/AUC, calibration or fidelity target.... | `eoip-phase4-2-requirements.md:139`; audit line 314 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-GRA-044` | `AIDLC-004.1`: - [ ] `AIDLC-004.1` Golden datasets for at least RAG, graph Q and A and one agent workflow | `eoip-phase4-2-requirements.md:2165`; audit line 315 | UNSTATED | MISSED | [CP-21](#cp-21) | subject triage | TRACE/BUILD |
| `REQ-GRA-045` | `AIDLC-006`: - **Step 2. Cost and trust path.** Router with shadow mode, token budgets, supervisory loops, logging and tracing, the distributed cache with the GAP-CACHE items, and the model gateway. Items: `CORE-003`, `AIDLC-006`, `C... | `eoip-phase4-2-requirements.md:176`; audit line 324 | UNSTATED | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-GRA-046` | `AIDLC-008.1`: - [ ] `AIDLC-008.1` One call path for all model use | `eoip-phase4-2-requirements.md:2127`; audit line 335 | UNSTATED | MISSED | [CP-13](#cp-13) | area fallback | TRACE/BUILD |
| `REQ-GRA-047` | `AIDLC-010`: - **Step 7. Deferred.** Probabilistic reasoning, multi-modal, memory graphs, fine-tuning pipeline, knowledge distillation. Items: `AI-007`, `MULTI-001`, `MULTI-002`, `AIDLC-010`, `GRAPH-003`. | `eoip-phase4-2-requirements.md:181`; audit line 344 | UNSTATED | MISSED | [CP-34](#cp-34) | subject triage | TRACE/BUILD |
| `REQ-GRA-048` | `CG-CODE-01`: Align code-graph docs to the real modules | `EOIP-engg-doc-pkg/17-code-graph.md:18`; audit line 383 | P1 | PARTIAL | [CP-37](#cp-37) | subject triage | COMPLETE |
| `REQ-GRA-049` | `COMPLY-001`: Compliance-as-Code Graph Constraints | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:836`; audit line 396 | P1 | IMPLEMENTED-UNVERIFIED | [CP-33](#cp-33) | ID family | PROVE |
| `REQ-GRA-050` | `COMPLY-001.1`: - [x] `COMPLY-001.1` Graph-pattern compliance rules | `eoip-phase4-2-requirements.md:1166`; audit line 397 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-GRA-051` | `COMPLY-001.2`: - [x] `COMPLY-001.2` Continuous monitoring on graph mutations | `eoip-phase4-2-requirements.md:1167`; audit line 398 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-GRA-052` | `COMPLY-002.1`: - [x] `COMPLY-002.1` PII detection across graph properties | `eoip-phase4-2-requirements.md:1190`; audit line 403 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-GRA-053` | `CORE-001.7`: - [x] `CORE-001.7` Unit tests covering all 7 formats with edge cases | `eoip-phase4-2-requirements.md:241`; audit line 423 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-GRA-054` | `CORE-004`: Graph-over-Graph Engineering | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:99`; audit line 442 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | engine family | PROVE |
| `REQ-GRA-055` | `CORE-004.1`: - [x] `CORE-004.1` GraphLayer abstraction with 7+ built-in types | `eoip-phase4-2-requirements.md:327`; audit line 443 | UNSTATED | MISSED | [CP-13](#cp-13) | engine family | TRACE/BUILD |
| `REQ-GRA-056` | `CORE-004.6`: - [x] `CORE-004.6` Thread-safe singleton `get_graph_graph_engine()` | `eoip-phase4-2-requirements.md:332`; audit line 448 | UNSTATED | MISSED | [CP-13](#cp-13) | engine family | TRACE/BUILD |
| `REQ-GRA-057` | `FR-04`: &#124; FR-04 &#124; Query and retrieval &#124; EOQL/query engine, graph traversal, evidence-backed GraphRAG, explainable retrieval, citations, ranking, filters, and consistent API/UI/MCP access. &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1083`; audit line 498 | UNSTATED | MISSED | [CP-29](#cp-29) | subject triage | TRACE/BUILD |
| `REQ-GRA-058` | `FR-05`: &#124; FR-05 &#124; Agentic operations &#124; Tool registry, MCP governance, agent memory, human approval controls, audit trails, risk classification, and governed automation over graph-backed knowledge. &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1084`; audit line 499 | UNSTATED | MISSED | [CP-29](#cp-29) | subject triage | TRACE/BUILD |
| `REQ-GRA-059` | `FR-07`: &#124; FR-07 &#124; Deployment and operations &#124; Docker local deployment, HA deployment path, backup/restore, observability, performance, security, privacy, DevSecOps, runbooks, validation evidence, and acceptance testing. &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1086`; audit line 501 | UNSTATED | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-GRA-060` | `FR-GRAPH-001`: HugeGraph authoritative store | `EOIP-engg-doc-pkg/01-project-vision.md:22`; audit line 524 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-GRA-061` | `FR-GRAPH-002`: Logical graph domains | `EOIP-engg-doc-pkg/03-functional-requirements.md:161`; audit line 525 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-GRA-062` | `FR-GRAPH-003`: Schema bootstrap | `EOIP-engg-doc-pkg/03-functional-requirements.md:171`; audit line 526 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-GRA-063` | `FR-GRAPH-004`: Canonical identifiers | `EOIP-engg-doc-pkg/03-functional-requirements.md:181`; audit line 527 | P0 | PARTIAL | [CP-13](#cp-13) | ID family | COMPLETE |
| `REQ-GRA-064` | `FR-GRAPH-005`: Meta graph | `EOIP-engg-doc-pkg/03-functional-requirements.md:191`; audit line 528 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-GRA-065` | `FR-GRAPH-006`: Cross-domain bridge edges | `EOIP-engg-doc-pkg/01-project-vision.md:23`; audit line 529 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-GRA-066` | `FR-GRAPH-007`: Gremlin repository | `EOIP-engg-doc-pkg/03-functional-requirements.md:211`; audit line 530 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-GRA-067` | `FR-GRAPH-008`: Index strategy | `EOIP-engg-doc-pkg/03-functional-requirements.md:221`; audit line 531 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-GRA-068` | `FR-GRAPH-009`: Graph version journal | `EOIP-engg-doc-pkg/03-functional-requirements.md:231`; audit line 532 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-GRA-069` | `FR-GRAPH-010`: RDF/OWL interoperability | `EOIP-engg-doc-pkg/03-functional-requirements.md:241`; audit line 533 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-GRA-070` | `FR-GRAPH-011`: &#124; FR-GRAPH-011 &#124; Multi-backend GraphStore registry &#124; P2 &#124; HugeGraph, Neptune, Memory backends all pass GraphStore protocol tests. &#124; | `EOIP-engg-doc-pkg/06-architecture.md:307`; audit line 534 | P2 | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-071` | `FR-GRAPH-012`: &#124; FR-GRAPH-012 &#124; **[Pass 5]** Amazon Neptune adapter &#124; P2 &#124; **Done** &#124; `packages/eoip/graph/neptune.py` â€” openCypher HTTPS, full GraphStore contract &#124; | `docs/audit-2026-10-06/assessed-gap-report.md:171`; audit line 535 | P2 | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-072` | `FR-KGR-001`: ### FR-KGR-001: Multi-Graph Type Rendering | `EOIP-engg-doc-pkg/KGR-requirements.md:99`; audit line 543 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-GRA-073` | `FR-KGR-003`: ### FR-KGR-003: Edge Intelligence | `EOIP-engg-doc-pkg/KGR-requirements.md:232`; audit line 545 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-GRA-074` | `FR-KGR-004`: ### FR-KGR-004: Interactive Graph Exploration | `EOIP-engg-doc-pkg/KGR-requirements.md:244`; audit line 546 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-GRA-075` | `FR-KGR-006`: ### FR-KGR-006: Graph Comparison & Diff | `EOIP-engg-doc-pkg/KGR-requirements.md:344`; audit line 548 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-GRA-076` | `FR-KGR-010`: Implements FR-KGR-010. Addresses a gap in Graphify, Gephi, and code2flow. Matches yFiles (€9.2K), KeyLines (commercial), Linkurious (commercial) — all of which charge for this feature. | `EOIP-engg-doc-pkg/KGR-implementation-plan.md:1298`; audit line 552 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-GRA-077` | `FR-KGR-016`: Implements FR-KGR-016. Inspired by Graphify's `graphify prs` with community-based conflict detection. | `EOIP-engg-doc-pkg/KGR-implementation-plan.md:1520`; audit line 558 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-GRA-078` | `FR-KGR-018`: ### FR-KGR-018: Automated Graph Intelligence Report | `EOIP-engg-doc-pkg/KGR-requirements.md:504`; audit line 560 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-GRA-079` | `FR-KGR-023`: ### FR-KGR-023: URL Deep Linking / Graph State Sharing | `EOIP-engg-doc-pkg/KGR-requirements.md:564`; audit line 565 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-GRA-080` | `FR-KGR-026`: ### FR-KGR-026: Cross-Project Graph Merge | `EOIP-engg-doc-pkg/KGR-requirements.md:600`; audit line 568 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-GRA-081` | `FR-KGR-027`: ### FR-KGR-027: RAG-Powered Graph Intelligence (17 Patterns) | `EOIP-engg-doc-pkg/KGR-requirements.md:611`; audit line 569 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-GRA-082` | `FR-KGR-028`: ### FR-KGR-028: Agentic AI Graph Intelligence (40+ Agent Types) | `EOIP-engg-doc-pkg/KGR-requirements.md:642`; audit line 570 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-GRA-083` | `FR-VALID-001`: Graph validation rules | `EOIP-engg-doc-pkg/03-functional-requirements.md:455`; audit line 599 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-GRA-084` | `FR-VALID-003`: Graph quality metrics | `EOIP-engg-doc-pkg/03-functional-requirements.md:475`; audit line 601 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-GRA-085` | `G2-ARCH-005`: G2-ARCH-005 — HugeGraph is semantic operational truth | `EOIP-engg-doc-pkg/gaps2-requirements.md:76`; audit line 644 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | subject triage | PROVE |
| `REQ-GRA-086` | `G2-ARCH-006`: G2-ARCH-006 — No raw telemetry lake in HugeGraph | `EOIP-engg-doc-pkg/gaps2-requirements.md:80`; audit line 645 | P0 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | subject triage | PROVE |
| `REQ-GRA-087` | `G2-EKAF-026`: G2-EKAF-026 — Incremental graph enrichment | `EOIP-engg-doc-pkg/gaps2-requirements.md:319`; audit line 701 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-GRA-088` | `G2-GRAPH-API-001`: G2-GRAPH-API-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:524`; audit line 729 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-089` | `G2-GRAPH-API-002`: G2-GRAPH-API-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:870`; audit line 730 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-090` | `G2-GRAPH-API-003`: G2-GRAPH-API-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:879`; audit line 731 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-091` | `G2-GRAPH-BIZ-001`: G2-GRAPH-BIZ-001 | `EOIP-engg-doc-pkg/gaps2-requirements.md:984`; audit line 732 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-092` | `G2-GRAPH-BIZ-002`: G2-GRAPH-BIZ-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:994`; audit line 733 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-093` | `G2-GRAPH-BIZ-003`: G2-GRAPH-BIZ-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:997`; audit line 734 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-094` | `G2-GRAPH-DEC-001`: G2-GRAPH-DEC-001 | `EOIP-engg-doc-pkg/gaps2-requirements.md:949`; audit line 735 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-095` | `G2-GRAPH-DEC-002`: G2-GRAPH-DEC-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:961`; audit line 736 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-096` | `G2-GRAPH-DEC-003`: G2-GRAPH-DEC-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:964`; audit line 737 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-097` | `G2-GRAPH-OBS-001`: G2-GRAPH-OBS-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:618`; audit line 738 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-098` | `G2-GRAPH-OBS-002`: G2-GRAPH-OBS-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:899`; audit line 739 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-099` | `G2-GRAPH-OBS-003`: G2-GRAPH-OBS-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:902`; audit line 740 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-100` | `G2-GRAPH-PROC-001`: G2-GRAPH-PROC-001 | `EOIP-engg-doc-pkg/gaps2-requirements.md:971`; audit line 741 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-101` | `G2-GRAPH-PROC-002`: G2-GRAPH-PROC-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:974`; audit line 742 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-102` | `G2-GRAPH-PROC-003`: G2-GRAPH-PROC-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:977`; audit line 743 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-103` | `G2-GRAPH-RUNTIME-001`: G2-GRAPH-RUNTIME-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:619`; audit line 744 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-104` | `G2-GRAPH-RUNTIME-002`: G2-GRAPH-RUNTIME-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:912`; audit line 745 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-105` | `G2-GRAPH-RUNTIME-003`: G2-GRAPH-RUNTIME-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:915`; audit line 746 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-106` | `G2-GRAPH-TEST-001`: G2-GRAPH-TEST-001 | `EOIP-engg-doc-pkg/gaps2-requirements.md:935`; audit line 750 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-107` | `G2-GRAPH-TEST-002`: G2-GRAPH-TEST-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:939`; audit line 751 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-108` | `G2-GRAPH-TEST-003`: G2-GRAPH-TEST-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:942`; audit line 752 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-109` | `G2-P2`: &#124; G2-P2 &#124; Baseline + incremental graph evolution &#124; Safe continuous sync/versioning &#124; | `EOIP-engg-doc-pkg/gaps2-implementation.md:37`; audit line 800 | P2 | PARTIAL | [CP-13](#cp-13) | subject triage | COMPLETE |
| `REQ-GRA-110` | `G2-P6`: &#124; G2-P6 &#124; Expanded semantic digital twin &#124; New graph domains + intent-to-runtime &#124; | `EOIP-engg-doc-pkg/gaps2-implementation.md:41`; audit line 804 | UNSTATED | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | subject triage | PROVE |
| `REQ-GRA-111` | `G2-UX-GRAPH-001`: G2-UX-GRAPH-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1088`; audit line 1165 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-112` | `G2-UX-GRAPH-002`: G2-UX-GRAPH-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1477`; audit line 1166 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-113` | `G2-UX-GRAPH-003`: G2-UX-GRAPH-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1480`; audit line 1167 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-114` | `G2-UX-GRAPH-004`: G2-UX-GRAPH-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1483`; audit line 1168 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-115` | `G2-UX-GRAPH-005`: G2-UX-GRAPH-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1486`; audit line 1169 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-116` | `G2-UX-GRAPH-006`: G2-UX-GRAPH-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1489`; audit line 1170 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-117` | `G2-UX-GRAPH-007`: G2-UX-GRAPH-007 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1492`; audit line 1171 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-118` | `G2-UX-GRAPH-008`: G2-UX-GRAPH-008 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1495`; audit line 1172 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-119` | `G2-UX-GRAPH-009`: G2-UX-GRAPH-009 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1498`; audit line 1173 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-120` | `G2-UX-GRAPH-010`: G2-UX-GRAPH-010 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1501`; audit line 1174 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-121` | `G2-UX-GRAPH-011`: G2-UX-GRAPH-011 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1504`; audit line 1175 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-122` | `G2-UX-GRAPH-012`: G2-UX-GRAPH-012 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1507`; audit line 1176 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-123` | `G2-UX-GRAPH-013`: G2-UX-GRAPH-013 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1510`; audit line 1177 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-124` | `G2-UX-GRAPH-014`: G2-UX-GRAPH-014 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1513`; audit line 1178 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-125` | `G2-UX-GRAPH-015`: G2-UX-GRAPH-015 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1516`; audit line 1179 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-126` | `G2-UX-GRAPH-016`: G2-UX-GRAPH-016 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1519`; audit line 1180 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-127` | `GAP-APP-001`: GAP-APP-001: Build a Knowledge App Builder that can compose query, table, graph, timeline, KPI and evidence panels from saved semantic queries | `EOIP-engg-doc-pkg/gaps-implementation.md:783`; audit line 1232 | P2 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | subject triage | PROVE |
| `REQ-GRA-128` | `GAP-ARCH-002`: GAP-ARCH-002: Evaluate actual code/deployment graph against intended architecture | `EOIP-engg-doc-pkg/gaps-requirements.md:535`; audit line 1235 | P0 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-GRA-129` | `GAP-CACHE-003`: GAP-CACHE-003: Invalidate using graph CDC | `EOIP-engg-doc-pkg/gaps-requirements.md:890`; audit line 1242 | P2 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | subject triage | PROVE |
| `REQ-GRA-130` | `GAP-CATALOG-001`: GAP-CATALOG-001: Add an enterprise Knowledge Catalog over all graph assets | `EOIP-engg-doc-pkg/gaps-implementation.md:538`; audit line 1246 | P0 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | subject triage | PROVE |
| `REQ-GRA-131` | `GAP-CATALOG-005`: GAP-CATALOG-005: Provide lineage-impact navigation from catalog to underlying graph path | `EOIP-engg-doc-pkg/gaps-requirements.md:300`; audit line 1250 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | subject triage | PROVE |
| `REQ-GRA-132` | `GAP-CDC-001`: GAP-CDC-001: Every graph mutation emits an internal event | `EOIP-engg-doc-pkg/gaps-requirements.md:803`; audit line 1251 | P1 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-GRA-133` | `GAP-CDC-003`: GAP-CDC-003: Consumers can subscribe to entity/edge/domain changes | `EOIP-engg-doc-pkg/gaps-requirements.md:805`; audit line 1253 | P1 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-GRA-134` | `GAP-CDC-005`: GAP-CDC-005: Support incremental GraphRAG summary update | `EOIP-engg-doc-pkg/gaps-requirements.md:807`; audit line 1255 | P1 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-GRA-135` | `GAP-GDS`: Local graph analytics service | `requirements-registry.json:1`; audit line 1321 | P1 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | subject triage | PROVE |
| `REQ-GRA-136` | `GAP-GDS-001`: GAP-GDS-001: Create a local graph-analytics service with pluggable algorithms without requiring the authoritative graph to be copied permanently into another da | `EOIP-engg-doc-pkg/gaps-implementation.md:731`; audit line 1322 | P1 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-GRA-137` | `GAP-GDS-002`: GAP-GDS-002: Provide algorithms for PageRank, centrality, connected components, community detection, similarity, shortest path and dependency risk | `EOIP-engg-doc-pkg/gaps-requirements.md:145`; audit line 1323 | P1 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-GRA-138` | `GAP-GRAG-005`: GAP-GRAG-005: Benchmark GraphRAG against direct graph query, vector RAG, hybrid RAG and no-RAG baselines | `EOIP-engg-doc-pkg/gaps-requirements.md:362`; audit line 1340 | P2 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-GRA-139` | `GAP-GRAPHTEST-001`: &#124; GAP-GRAPHTEST-001..011 graph assertion framework &#124; `graphtest/framework.py` loads declarative suites and validates paths, cardinality, ownership, provenance, temporal validity, boundaries and traceability coverage &#124;... | `EOIP-engg-doc-pkg/reference/g2-traceability.md:74`; audit line 1342 | UNSTATED | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | subject triage | PROVE |
| `REQ-GRA-140` | `GAP-HG-001`: GAP-HG-001: Abstract HugeGraph client behind repository interface | `EOIP-engg-doc-pkg/gaps-implementation.md:51`; audit line 1345 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-GRA-141` | `GAP-HG-004`: GAP-HG-004: Bulk-loader path | `EOIP-engg-doc-pkg/gaps-requirements.md:1077`; audit line 1348 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-GRA-142` | `GAP-KFW-006`: GAP-KFW-006: Defend against graph poisoning and semantic prompt injection | `EOIP-engg-doc-pkg/gaps-requirements.md:740`; audit line 1362 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-GRA-143` | `GAP-KRAG-002`: GAP-KRAG-002: Favor authoritative graph facts over generated summaries | `EOIP-engg-doc-pkg/gaps-requirements.md:677`; audit line 1381 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-GRA-144` | `GAP-LAYER-001`: GAP-LAYER-001: Introduce Graph Views / Knowledge Products comparable conceptually to curated graph subsets: | `EOIP-engg-doc-pkg/gaps-implementation.md:540`; audit line 1390 | P2 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | subject triage | PROVE |
| `REQ-GRA-145` | `GAP-LIFE-001`: GAP-LIFE-001: Tier hot/warm/archive graph information | `EOIP-engg-doc-pkg/gaps-requirements.md:900`; audit line 1392 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | subject triage | PROVE |
| `REQ-GRA-146` | `GAP-REC`: Graph-aware recommendation engine | `requirements-registry.json:1`; audit line 1450 | P1 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | subject triage | PROVE |
| `REQ-GRA-147` | `GAP-REC-001`: GAP-REC-001: Add graph-aware recommendation engine for documents, experts, components and related concepts | `EOIP-engg-doc-pkg/gaps-requirements.md:223`; audit line 1451 | P2 | IMPLEMENTED-UNVERIFIED | [CP-31](#cp-31) | ID family | PROVE |
| `REQ-GRA-148` | `GAP-RET-004`: GAP-RET-004: Query planner chooses minimal sufficient retrieval path | `EOIP-engg-doc-pkg/gaps-requirements.md:666`; audit line 1455 | P0 | IMPLEMENTED-UNVERIFIED | [CP-20](#cp-20) | ID family | PROVE |
| `REQ-GRA-149` | `GAP-SEARCH-001`: GAP-SEARCH-001: Add synchronized full-text + vector + graph hybrid search with freshness guarantees | `EOIP-engg-doc-pkg/gaps-implementation.md:459`; audit line 1470 | P1 | IMPLEMENTED-UNVERIFIED | [CP-20](#cp-20) | ID family | PROVE |
| `REQ-GRA-150` | `GAP-SEARCH-002`: GAP-SEARCH-002: Search results must preserve graph identity and provenance | `EOIP-engg-doc-pkg/gaps-requirements.md:169`; audit line 1471 | P1 | IMPLEMENTED-UNVERIFIED | [CP-20](#cp-20) | ID family | PROVE |
| `REQ-GRA-151` | `GAP-TEMP-006`: GAP-TEMP-006: Graph diffs must be first-class objects | `EOIP-engg-doc-pkg/gaps-requirements.md:573`; audit line 1503 | P1 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-GRA-152` | `GRAPH-001`: Federated Graph Engineering | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:260`; audit line 1522 | P1 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | engine family | PROVE |
| `REQ-GRA-153` | `GRAPH-001.1`: - [x] `GRAPH-001.1` Virtual graph spanning 2+ backends | `eoip-phase4-2-requirements.md:505`; audit line 1523 | UNSTATED | MISSED | [CP-14](#cp-14) | engine family | TRACE/BUILD |
| `REQ-GRA-154` | `GRAPH-001.2`: - [x] `GRAPH-001.2` Query decomposition and result merging | `eoip-phase4-2-requirements.md:506`; audit line 1524 | UNSTATED | MISSED | [CP-14](#cp-14) | engine family | TRACE/BUILD |
| `REQ-GRA-155` | `GRAPH-001.3`: - [x] `GRAPH-001.3` Entity mapping across backends | `eoip-phase4-2-requirements.md:507`; audit line 1525 | UNSTATED | MISSED | [CP-14](#cp-14) | engine family | TRACE/BUILD |
| `REQ-GRA-156` | `GRAPH-001.4`: - [x] `GRAPH-001.4` Query pushdown optimization | `eoip-phase4-2-requirements.md:508`; audit line 1526 | UNSTATED | MISSED | [CP-14](#cp-14) | engine family | TRACE/BUILD |
| `REQ-GRA-157` | `GRAPH-001.5`: - [x] `GRAPH-001.5` Thread-safe singleton | `eoip-phase4-2-requirements.md:509`; audit line 1527 | UNSTATED | MISSED | [CP-14](#cp-14) | engine family | TRACE/BUILD |
| `REQ-GRA-158` | `GRAPH-001.6`: - [x] `GRAPH-001.6` Wired into brain_os.py and platform_router.py | `eoip-phase4-2-requirements.md:510`; audit line 1528 | UNSTATED | MISSED | [CP-14](#cp-14) | engine family | TRACE/BUILD |
| `REQ-GRA-159` | `GRAPH-001.7`: - [x] `GRAPH-001.7` Unit tests | `eoip-phase4-2-requirements.md:511`; audit line 1529 | UNSTATED | MISSED | [CP-14](#cp-14) | engine family | TRACE/BUILD |
| `REQ-GRA-160` | `GRAPH-002`: Causal Inference over Graphs | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:284`; audit line 1530 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | engine family | PROVE |
| `REQ-GRA-161` | `GRAPH-002.1`: - [x] `GRAPH-002.1` do-calculus intervention on graph entities | `eoip-phase4-2-requirements.md:532`; audit line 1531 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-162` | `GRAPH-002.2`: - [x] `GRAPH-002.2` Counterfactual query execution | `eoip-phase4-2-requirements.md:533`; audit line 1532 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-163` | `GRAPH-002.3`: - [x] `GRAPH-002.3` Blast radius analysis | `eoip-phase4-2-requirements.md:534`; audit line 1533 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-164` | `GRAPH-002.4`: - [x] `GRAPH-002.4` Integration with existing causal reasoning | `eoip-phase4-2-requirements.md:535`; audit line 1534 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-165` | `GRAPH-002.5`: - [x] `GRAPH-002.5` Unit tests | `eoip-phase4-2-requirements.md:536`; audit line 1535 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-166` | `GRAPH-003`: Knowledge Distillation Engineering | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:305`; audit line 1536 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | engine family | PROVE |
| `REQ-GRA-167` | `GRAPH-003.1`: - [x] `GRAPH-003.1` Graph distillation with configurable strategies | `eoip-phase4-2-requirements.md:555`; audit line 1537 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-168` | `GRAPH-003.2`: - [x] `GRAPH-003.2` Portable knowledge packages | `eoip-phase4-2-requirements.md:556`; audit line 1538 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-169` | `GRAPH-003.3`: - [x] `GRAPH-003.3` Edge deployment integration | `eoip-phase4-2-requirements.md:557`; audit line 1539 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-170` | `GRAPH-003.4`: - [x] `GRAPH-003.4` Fidelity metrics (information loss measurement) | `eoip-phase4-2-requirements.md:558`; audit line 1540 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-171` | `GRAPH-003.5`: - [x] `GRAPH-003.5` Unit tests | `eoip-phase4-2-requirements.md:559`; audit line 1541 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-172` | `GRAPH-004`: Graph Neural Network Integration | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:325`; audit line 1542 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | engine family | PROVE |
| `REQ-GRA-173` | `GRAPH-004.1`: - [x] `GRAPH-004.1` Graph embedding generation (node2vec, TransE) | `eoip-phase4-2-requirements.md:578`; audit line 1543 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-174` | `GRAPH-004.2`: - [x] `GRAPH-004.2` Link prediction with confidence scores | `eoip-phase4-2-requirements.md:579`; audit line 1544 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-175` | `GRAPH-004.3`: - [x] `GRAPH-004.3` Node classification | `eoip-phase4-2-requirements.md:580`; audit line 1545 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-176` | `GRAPH-004.4`: - [x] `GRAPH-004.4` Integration with existing graph store | `eoip-phase4-2-requirements.md:581`; audit line 1546 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-177` | `GRAPH-004.5`: - [x] `GRAPH-004.5` Unit tests | `eoip-phase4-2-requirements.md:582`; audit line 1547 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-178` | `GRAPH-005`: Temporal & Hybrid Retrieval Engineering | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:346`; audit line 1548 | P1 | IMPLEMENTED-UNVERIFIED | [CP-20](#cp-20) | engine family | PROVE |
| `REQ-GRA-179` | `GRAPH-005.1`: - [x] `GRAPH-005.1` TemporalIndex with validity windows | `eoip-phase4-2-requirements.md:600`; audit line 1549 | UNSTATED | MISSED | [CP-20](#cp-20) | engine family | TRACE/BUILD |
| `REQ-GRA-180` | `GRAPH-005.2`: - [x] `GRAPH-005.2` As-of and range queries | `eoip-phase4-2-requirements.md:601`; audit line 1550 | UNSTATED | MISSED | [CP-20](#cp-20) | engine family | TRACE/BUILD |
| `REQ-GRA-181` | `GRAPH-005.3`: - [x] `GRAPH-005.3` Integration with state time-travel | `eoip-phase4-2-requirements.md:602`; audit line 1551 | UNSTATED | MISSED | [CP-20](#cp-20) | engine family | TRACE/BUILD |
| `REQ-GRA-182` | `GRAPH-005.4`: - [x] `GRAPH-005.4` Integration with hybrid search | `eoip-phase4-2-requirements.md:603`; audit line 1552 | UNSTATED | MISSED | [CP-20](#cp-20) | engine family | TRACE/BUILD |
| `REQ-GRA-183` | `GRAPH-005.5`: - [x] `GRAPH-005.5` Unit tests | `eoip-phase4-2-requirements.md:604`; audit line 1553 | UNSTATED | MISSED | [CP-20](#cp-20) | engine family | TRACE/BUILD |
| `REQ-GRA-184` | `GRAPH-006`: OWL Reasoning & SHACL Runtime Validation | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:366`; audit line 1554 | P2 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | engine family | PROVE |
| `REQ-GRA-185` | `GRAPH-006.1`: - [x] `GRAPH-006.1` OWL subsumption and inference | `eoip-phase4-2-requirements.md:622`; audit line 1555 | UNSTATED | MISSED | [CP-12](#cp-12) | engine family | TRACE/BUILD |
| `REQ-GRA-186` | `GRAPH-006.2`: - [x] `GRAPH-006.2` SHACL shape validation | `eoip-phase4-2-requirements.md:623`; audit line 1556 | UNSTATED | MISSED | [CP-12](#cp-12) | engine family | TRACE/BUILD |
| `REQ-GRA-187` | `GRAPH-006.3`: - [x] `GRAPH-006.3` Violation report with severity levels | `eoip-phase4-2-requirements.md:624`; audit line 1557 | UNSTATED | MISSED | [CP-12](#cp-12) | engine family | TRACE/BUILD |
| `REQ-GRA-188` | `GRAPH-006.4`: - [x] `GRAPH-006.4` Integration with ontology management | `eoip-phase4-2-requirements.md:625`; audit line 1558 | UNSTATED | MISSED | [CP-12](#cp-12) | engine family | TRACE/BUILD |
| `REQ-GRA-189` | `GRAPH-006.5`: - [x] `GRAPH-006.5` Unit tests | `eoip-phase4-2-requirements.md:626`; audit line 1559 | UNSTATED | MISSED | [CP-12](#cp-12) | engine family | TRACE/BUILD |
| `REQ-GRA-190` | `H-01`: HugeGraph adapter wiring | `KGF-MASTER-BACKLOG.md:267`; audit line 1560 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | subject triage | PROVE |
| `REQ-GRA-191` | `KGR-G-004`: In-Memory High-Performance Graph Algorithm Engine | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:33`; audit line 1613 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-192` | `KGR-G-005`: Universal Zero-ETL Virtual Relational Graph Adapter | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:34`; audit line 1614 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-193` | `KGR-G-008`: Zero-Trust Confidential Graph & Egress DLP Gateway | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:39`; audit line 1617 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-194` | `KGR-G-013`: Native Per-Tenant Named-Graph Isolation Protocol | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:283`; audit line 1622 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-195` | `KGR-G-016`: Co-Located HNSW Vector + Graph Index (VectorGraph Adapter) | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:283`; audit line 1625 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-196` | `KGR-G-017`: PR-Level Cross-Repository Graph Impact Triage MCP Tools | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:251`; audit line 1626 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-197` | `KGR-G-020`: Real-Time Graph Mutation Streaming & Webhook Notification | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:283`; audit line 1629 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-GRA-198` | `MS-12`: Live Collaborative Graph Studio (Figma for Knowledge Graphs) | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:68`; audit line 1642 | P1 | IMPLEMENTED-UNVERIFIED | [CP-26](#cp-26) | explicit | PROVE |
| `REQ-GRA-199` | `MS-17`: Graph-Grounded Multi-Agent Orchestration Fabric (A2A + MCP) | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:210`; audit line 1647 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-GRA-200` | `MS-18`: Federated Cross-Organizational Privacy-Preserving Graph Learning | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:151`; audit line 1648 | P1 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-GRA-201` | `MS-20`: Verifiable AI Reasoning Chains (Cryptographic Proof of Thought) | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:300`; audit line 1651 | P1 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-GRA-202` | `MS-21`: Knowledge Graph Integrity Sentinel (Continuous Structural Integrity Monitor) | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:267`; audit line 1652 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-GRA-203` | `MS-22`: Quantum-Inspired Graph Optimization Engine | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:26`; audit line 1653 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-GRA-204` | `MS-24`: Continuous Graph Health Intelligence Dashboard | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:353`; audit line 1655 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-GRA-205` | `MS-28`: Autonomous Graph Maintenance & Self-Organization Engine | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:28`; audit line 1659 | P1 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-GRA-206` | `MS-29`: Graph-Native Foundation Model Runtime (Structural Reasoning Host) | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:551`; audit line 1660 | P1 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-GRA-207` | `MS-30`: Object-Centric Process Intelligence Graph (OCEL 2.0 + Knowledge Graph Fusion) | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:8`; audit line 1662 | P1 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-GRA-208` | `MULTI-001.1`: - [x] `MULTI-001.1` Diagram parsing to graph nodes | `eoip-phase4-2-requirements.md:1334`; audit line 1671 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-209` | `MULTI-001.2`: - [x] `MULTI-001.2` Graph-to-image rendering | `eoip-phase4-2-requirements.md:1335`; audit line 1672 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-GRA-210` | `MULTI-002`: Knowledge & Memory Graph Engineering | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:984`; audit line 1674 | P2 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | engine family | PROVE |
| `REQ-GRA-211` | `MULTI-002.1`: - [x] `MULTI-002.1` Graph-native memory storage | `eoip-phase4-2-requirements.md:1353`; audit line 1675 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-GRA-212` | `MULTI-002.2`: - [x] `MULTI-002.2` Episodic memory graphs | `eoip-phase4-2-requirements.md:1354`; audit line 1676 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-GRA-213` | `MULTI-002.3`: - [x] `MULTI-002.3` Graph-based consolidation | `eoip-phase4-2-requirements.md:1355`; audit line 1677 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-GRA-214` | `MVP-FR-001`: Apache HugeGraph local Docker | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:99`; audit line 1679 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | subject triage | PROVE |
| `REQ-GRA-215` | `MVP-FR-008`: Code graph | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:106`; audit line 1686 | P0 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | subject triage | PROVE |
| `REQ-GRA-216` | `MVP-FR-010`: Cross-graph linking | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:108`; audit line 1689 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | subject triage | PROVE |
| `REQ-GRA-217` | `MVP-FR-012`: Graph validation | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:110`; audit line 1691 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | subject triage | PROVE |
| `REQ-GRA-218` | `MVP-FR-015`: Path query | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:113`; audit line 1694 | P0 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | subject triage | PROVE |
| `REQ-GRA-219` | `MVP-FR-017`: Graph visualizer | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:115`; audit line 1696 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | subject triage | PROVE |
| `REQ-GRA-220` | `MVP-FR-020`: Local GraphRAG | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:118`; audit line 1699 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | subject triage | PROVE |
| `REQ-GRA-221` | `MVP-FR-022`: MCP core graph access | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:120`; audit line 1701 | P0 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | subject triage | PROVE |
| `REQ-GRA-222` | `MVP-P3`: &#124; MVP-P3 &#124; Query, Retrieval, RAG, And Explanation &#124; Implement EOQL/query APIs, traversal controls, evidence-backed RAG, citation handling, explainability artifacts, graph algorithms, and API documentation. &#124; EOIP-eng... | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md:47`; audit line 1712 | P3 | MISSED | [CP-07](#cp-07) | subject triage | TRACE/BUILD |
| `REQ-GRA-223` | `MVP-P4`: &#124; MVP-P4 &#124; Agent, MCP, And Human Control &#124; Implement MCP server, tool registry, agent runtime contracts, human-in-the-loop approval, memory governance, graph-over-loop and loop-over-graph behaviors, and audit traces. ... | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md:48`; audit line 1713 | UNSTATED | MISSED | [CP-29](#cp-29) | subject triage | TRACE/BUILD |
| `REQ-GRA-224` | `MVP-P5`: &#124; MVP-P5 &#124; User Interfaces And Developer Experience &#124; Build the usable web app, admin views, VS Code extension path, Hubble/local graph explorer integration, demo walkthroughs, and dashboards. &#124; EOIP-engg-doc-pkg/42-... | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md:49`; audit line 1714 | UNSTATED | MISSED | [CP-29](#cp-29) | subject triage | TRACE/BUILD |
| `REQ-GRA-225` | `NFR-03`: &#124; NFR-03 &#124; Portability &#124; The graph persistence layer must preserve the EOIP graph contract while allowing client-selected graph systems through adapters and configuration. &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1095`; audit line 1727 | UNSTATED | MISSED | [CP-03](#cp-03) | subject triage | TRACE/BUILD |
| `REQ-GRA-226` | `SDLC-003.2`: - [ ] `SDLC-003.2` Threat models exist for CORE-002, CORE-003, GRAPH-001, AGENT-003, INFRA-002, COMPLY-002 | `eoip-phase4-2-requirements.md:1448`; audit line 1796 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-GRA-227` | `SDLC-004`: &#124; Wiring &#124; Only 8 of 49 require wiring into brain_os.py and platform_router.py (CORE-001, 002, 003, 004, 006, AGENT-002, GRAPH-001, AI-001). The other engine requirements have no API-exposure criterion, which is the fa... | `eoip-phase4-2-requirements.md:35`; audit line 1799 | UNSTATED | MISSED | [CP-07](#cp-07) | engine family | TRACE/BUILD |
| `REQ-GRA-228` | `SDLC-015.1`: - [ ] `SDLC-015.1` Protected-path rules enforced in CI | `eoip-phase4-2-requirements.md:1676`; audit line 1855 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-GRA-229` | `SDLC-016.2`: - [ ] `SDLC-016.2` Requirement-code-test graph queryable | `eoip-phase4-2-requirements.md:1695`; audit line 1861 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-GRA-230` | `SDLC-025`: - **Step 2. Cost and trust path.** Router with shadow mode, token budgets, supervisory loops, logging and tracing, the distributed cache with the GAP-CACHE items, and the model gateway. Items: `CORE-003`, `AIDLC-006`, `C... | `eoip-phase4-2-requirements.md:176`; audit line 1904 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-GRA-231` | `SDLC-028`: &#124; Derived data copies &#124; INFRA-001 L2 cache, AI-006 embeddings, GRAPH-003 packages, AGENT-003 persisted messages, AI-005 artifacts, MULTI-002 memory graphs, COMPLY-002 pseudonym vault, INFRA-007 backups, INFRA-004 logs ... | `eoip-phase4-2-requirements.md:142`; audit line 1919 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-GRA-232` | `SDLC-028.2`: - [ ] `SDLC-028.2` Erasure test removes a subject from graph, caches, vector index, packages, logs and backups | `eoip-phase4-2-requirements.md:1920`; audit line 1921 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-GRA-233` | `SDLC-029`: &#124; Derived data copies &#124; INFRA-001 L2 cache, AI-006 embeddings, GRAPH-003 packages, AGENT-003 persisted messages, AI-005 artifacts, MULTI-002 memory graphs, COMPLY-002 pseudonym vault, INFRA-007 backups, INFRA-004 logs ... | `eoip-phase4-2-requirements.md:142`; audit line 1924 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-GRA-234` | `SDLC-031.3`: - [ ] `SDLC-031.3` CPU-only path works | `eoip-phase4-2-requirements.md:1976`; audit line 1937 | UNSTATED | MISSED | [CP-32](#cp-32) | engine family | TRACE/BUILD |
| `REQ-GRA-235` | `SDLC-032.1`: - [ ] `SDLC-032.1` Link and path checks fail the build | `eoip-phase4-2-requirements.md:1994`; audit line 1940 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-GRA-236` | `SR-ARC-002`: &#124; SR-ARC-002 &#124; **Ports-and-adapters:** Graph Store, Vector Store, Search, Object Store, Relational Store, Event Bus, Model Provider, Identity Provider, Secret/KMS, Scheduler and Notification are ports with versioned co... | `EOIP-engg-doc-pkg/super-requirements.md:163`; audit line 1976 | P0 | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-GRA-237` | `SR-ARC-005`: &#124; SR-ARC-005 &#124; **Distributed by design:** stateless API/query/worker tiers scale horizontally; stateful tiers (graph, vector, search, relational, object, log) support replication and partitioning per backend capability... | `EOIP-engg-doc-pkg/super-requirements.md:166`; audit line 1979 | P0 | MISSED | [CP-10](#cp-10) | subject triage | TRACE/BUILD |
| `REQ-GRA-238` | `SR-ARC-006`: &#124; SR-ARC-006 &#124; **Consistency model documented and tested:** strong consistency within a graph partition for writes and read-your-writes for the writer; eventual consistency for derived indexes (vector, search, material... | `EOIP-engg-doc-pkg/super-requirements.md:167`; audit line 1980 | P0 | MISSED | [CP-20](#cp-20) | subject triage | TRACE/BUILD |
| `REQ-GRA-239` | `SR-ARC-009`: &#124; SR-ARC-009 &#124; **Federation:** queries MAY span multiple graph backends and multiple sites (hub-and-spoke or mesh) with partial-result semantics, per-site policy enforcement and no raw-data movement unless permitted. \... | `EOIP-engg-doc-pkg/super-requirements.md:170`; audit line 1983 | P2 | MISSED | [CP-14](#cp-14) | subject triage | TRACE/BUILD |
| `REQ-GRA-240` | `SR-CON-008`: &#124; SR-CON-008 &#124; **Adapters over lock-in:** no component outside an adapter may import a vendor-specific graph, vector, model, bus or storage SDK. Enforced by architecture tests. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:105`; audit line 2012 | P0 | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-GRA-241` | `SR-CON-010`: &#124; SR-CON-010 &#124; Cloud capabilities MUST be delivered as **Service Provider plugins** (e.g., object storage, managed graph DB, managed search, KMS/HSM, IdP, queue, LLM endpoint, monitoring sink) selectable per capability... | `EOIP-engg-doc-pkg/super-requirements.md:124`; audit line 2014 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-GRA-242` | `SR-CON-012`: &#124; SR-CON-012 &#124; Provide reference adapters for the three hyperscalers' object storage, KMS, identity federation and managed graph/search where available (e.g., Amazon Neptune/OpenSearch/S3/KMS, Azure Blob/Key Vault/Entr... | `EOIP-engg-doc-pkg/super-requirements.md:126`; audit line 2016 | P1 | PARTIAL | [CP-16](#cp-16) | ID family | COMPLETE |
| `REQ-GRA-243` | `SR-CON-013`: **Research basis:** Terraform/OpenTofu IaC model; dbt for data transformation; GitOps principles (Weaveworks); Graphify git hook incremental indexing; super-requirements SR-CON-013 (Terraform/Helm IaC modules, P1). | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:99`; audit line 2017 | P1 | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-GRA-244` | `SR-DEP-008`: &#124; SR-DEP-008 &#124; **Edge/federation package** for DP-6: small footprint, offline-first, delta/summary sync with conflict policies and bandwidth limits. &#124; P2 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:929`; audit line 2026 | P2 | MISSED | [CP-31](#cp-31) | ID family | TRACE/BUILD |
| `REQ-GRA-245` | `SR-EXT-011`: &#124; SR-EXT-011 &#124; **Isolation:** each plugin runs in a container or WASM sandbox with declared capabilities (network, filesystem, secrets, graph read/write scopes), CPU/memory/time limits, health checks and no ambient aut... | `EOIP-engg-doc-pkg/super-requirements.md:787`; audit line 2034 | P0 | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-GRA-246` | `SR-GDB-003`: &#124; SR-GDB-003 &#124; A **backend-neutral conformance suite** (contract tests + golden queries + performance probes + failure injection) MUST gate every adapter. Backend-specific behavior (e.g., HugeGraph 1.7 not honoring UNI... | `EOIP-engg-doc-pkg/super-requirements.md:185`; audit line 2041 | P0 | PARTIAL | [CP-13](#cp-13) | ID family | COMPLETE |
| `REQ-GRA-247` | `SR-GDB-005`: &#124; SR-GDB-005 &#124; **Polyglot persistence:** each logical graph domain (e.g., org, code, incident, lineage, meta) MAY bind to a different backend and tier (hot/warm/cold); cross-domain **bridge edges** are resolved by the ... | `EOIP-engg-doc-pkg/super-requirements.md:187`; audit line 2043 | P1 | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-248` | `SR-GDB-009`: &#124; SR-GDB-009 &#124; **Graph versioning:** every mutation produces an `EntityRevision`; point-in-time ("as-of") reads and diffs between revisions MUST be supported (full snapshot/diff at P1). &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:191`; audit line 2047 | P1 | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-249` | `SR-GDB-010`: &#124; SR-GDB-010 &#124; **Embedded engine option** for DP-0/edge nodes with no server process, and an in-memory engine for tests only (selection is explicit configuration, never a silent fallback). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:192`; audit line 2048 | P0 | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-250` | `SR-GDB-014`: &#124; SR-GDB-014 &#124; **Cache:** in-process plus a Redis-protocol-compatible adapter; every cache key MUST include tenant, policy-version and graph-revision. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:219`; audit line 2052 | P0 | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-251` | `SR-NFR-002`: &#124; SR-NFR-002 &#124; **Data scaling patterns:** graph partitioning/sharding per backend capability, read replicas, tenant-based partitioning, hot/warm/cold tiering, archive to object storage with rehydration, vector index sh... | `EOIP-engg-doc-pkg/super-requirements.md:897`; audit line 2115 | P1 | MISSED | [CP-15](#cp-15) | subject triage | TRACE/BUILD |
| `REQ-GRA-252` | `SR-NFR-004`: &#124; SR-NFR-004 &#124; **Graceful degradation matrix** (documented and tested): vector down → text/graph retrieval; model down → deterministic + evidence (SR-RAG-008); search down → graph-only; bus lag → stale-flag; one backen... | `EOIP-engg-doc-pkg/super-requirements.md:899`; audit line 2117 | P0 | MISSED | [CP-20](#cp-20) | subject triage | TRACE/BUILD |
| `REQ-GRA-253` | `SR-NFR-005`: &#124; SR-NFR-005 &#124; **Backup/restore:** native backend backups and logical checksummed archives; consistent multi-store snapshots (graph + vector + search + relational + object + event log) with crash-atomic recovery; point... | `EOIP-engg-doc-pkg/super-requirements.md:900`; audit line 2118 | P0 | MISSED | [CP-31](#cp-31) | subject triage | TRACE/BUILD |
| `REQ-GRA-254` | `SR-NFR-008`: &#124; SR-NFR-008 &#124; **Capacity planning tools:** sizing calculator and in-product forecasts (graph growth, index size, GPU needs) with reference architectures per tier. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:903`; audit line 2121 | P1 | MISSED | [CP-13](#cp-13) | subject triage | TRACE/BUILD |
| `REQ-GRA-255` | `SR-PRV-002`: &#124; SR-PRV-002 &#124; **Data-subject requests:** locate a subject across graph, raw captures, vector/search indexes, caches, derived graphs, exports and backups (flagged); execute access/export, rectification and **erasure wi... | `EOIP-engg-doc-pkg/super-requirements.md:849`; audit line 2157 | P0 | PARTIAL | [CP-09](#cp-09) | ID family | COMPLETE |
| `REQ-GRA-256` | `SR-PRV-005`: &#124; SR-PRV-005 &#124; **Compliance from the graph:** auto-generate records of processing, data maps, data-flow diagrams, system-to-data-class inventories, cross-border transfer views and DPIA starter reports from the graph it... | `EOIP-engg-doc-pkg/super-requirements.md:852`; audit line 2160 | P1 | PARTIAL | [CP-09](#cp-09) | ID family | COMPLETE |
| `REQ-GRA-257` | `SR-VDB-002`: &#124; SR-VDB-002 &#124; **Adapters:** embedded (FAISS/hnswlib/USearch/LanceDB-class), PostgreSQL pgvector, Qdrant, Milvus, Weaviate, Chroma, OpenSearch/Elasticsearch k-NN, Redis-compatible vector, Vespa, graph-native vector ind... | `EOIP-engg-doc-pkg/super-requirements.md:228`; audit line 2229 | P0 | MISSED | [CP-20](#cp-20) | ID family | TRACE/BUILD |
| `REQ-GRA-258` | `SR-VDB-004`: &#124; SR-VDB-004 &#124; **Multi-vector and multimodal:** text, code, table, image, audio-transcript, and node/graph embeddings; late-interaction (ColBERT-style) and sparse-learned (SPLADE-style) as optional retrievers. &#124; P2 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:230`; audit line 2231 | P2 | MISSED | [CP-20](#cp-20) | ID family | TRACE/BUILD |
| `REQ-GRA-259` | `SR-VDB-007`: &#124; SR-VDB-007 &#124; A deployment with **no vector store** MUST still pass the core NL acceptance suite using graph + full-text retrieval (degraded semantic recall is acceptable and MUST be signalled). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:233`; audit line 2234 | P0 | MISSED | [CP-20](#cp-20) | ID family | TRACE/BUILD |
| `REQ-GRA-260` | `SR-WL-009`: &#124; SR-WL-009 &#124; **Embeddable components:** iframe/web-component widgets (NL console, graph viewer, impact panel) with token-based auth for embedding in customer or partner portals. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:741`; audit line 2243 | P1 | MISSED | [CP-28](#cp-28) | ID family | TRACE/BUILD |
| `REQ-GRA-261` | `TASK-AIE-004`: - **TASK-AIE-004**: Implement GNN embeddings (GRAPH-004) — node2vec, TransE implementations | `EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:28`; audit line 2247 | UNSTATED | MISSED | [CP-34](#cp-34) | subject triage | TRACE/BUILD |
| `REQ-GRA-262` | `TASK-AIE-005`: - **TASK-AIE-005**: Implement Temporal Retrieval (GRAPH-005) — TemporalIndex with validity windows | `EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:32`; audit line 2248 | UNSTATED | MISSED | [CP-18](#cp-18) | subject triage | TRACE/BUILD |
| `REQ-GRA-263` | `TASK-AIE-013`: - **TASK-AIE-013**: Build golden evaluation dataset — 100+ test cases across retrieval, reasoning, graph queries | `EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:66`; audit line 2256 | UNSTATED | MISSED | [CP-13](#cp-13) | subject triage | TRACE/BUILD |
| `REQ-GRA-264` | `TASK-ARCH-001`: - **TASK-ARCH-001**: Design Graph-over-Graph (CORE-004) layer architecture — define GraphLayer abstraction, cross-layer query semantics, constraint propagation model | `EOIP-engg-doc-pkg/roles/Architect_tasks.md:11`; audit line 2257 | UNSTATED | MISSED | [CP-14](#cp-14) | subject triage | TRACE/BUILD |
| `REQ-GRA-265` | `TASK-ARCH-005`: - **TASK-ARCH-005**: Design Federated Graph (GRAPH-001) query decomposition — plan generation, backend dispatch, result merge, conflict resolution | `EOIP-engg-doc-pkg/roles/Architect_tasks.md:29`; audit line 2261 | UNSTATED | MISSED | [CP-14](#cp-14) | subject triage | TRACE/BUILD |
| `REQ-GRA-266` | `TASK-CEO-003`: - **TASK-CEO-003**: Competitive positioning against Palantir, Databricks, Neo4j, DataStax | `EOIP-engg-doc-pkg/roles/CEO_tasks.md:25`; audit line 2276 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-GRA-267` | `TASK-CEO-007`: - **TASK-CEO-007**: Establish advisory board with enterprise AI, knowledge graph, and compliance domain experts | `EOIP-engg-doc-pkg/roles/CEO_tasks.md:53`; audit line 2280 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-GRA-268` | `TASK-CTO-002`: - **TASK-CTO-002**: Define scalability targets: 10K concurrent users, 100M graph nodes, sub-second query latency | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:17`; audit line 2288 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-GRA-269` | `TASK-CTO-003`: - **TASK-CTO-003**: Evaluate and approve technology stack decisions (graph databases, vector stores, LLM providers) | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:24`; audit line 2289 | UNSTATED | MISSED | [CP-20](#cp-20) | subject triage | TRACE/BUILD |
| `REQ-GRA-270` | `TASK-CTO-009`: - **TASK-CTO-009**: Evaluate Graph-over-Graph (CORE-004) architectural feasibility and performance implications | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:63`; audit line 2295 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-GRA-271` | `TASK-CTO-012`: - **TASK-CTO-012**: Evaluate GNN integration (GRAPH-004) feasibility — library selection, training pipeline, inference latency | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:80`; audit line 2298 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-GRA-272` | `TASK-CTO-014`: - **TASK-CTO-014**: Establish data classification framework for graph entities (public/internal/confidential/restricted) | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:94`; audit line 2300 | UNSTATED | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-GRA-273` | `TASK-LAI-002`: - **TASK-LAI-002**: Design GNN Integration (GRAPH-004) architecture — embedding strategy, inference pipeline | `EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:16`; audit line 2336 | UNSTATED | MISSED | [CP-34](#cp-34) | subject triage | TRACE/BUILD |
| `REQ-GRA-274` | `TASK-LAI-006`: - **TASK-LAI-006**: Design Temporal Retrieval (GRAPH-005) integration with existing RAG suite | `EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:37`; audit line 2340 | UNSTATED | MISSED | [CP-18](#cp-18) | subject triage | TRACE/BUILD |
| `REQ-GRA-275` | `TASK-LAI-016`: - **TASK-LAI-016**: Design Causal Inference (GRAPH-002) algorithms — do-calculus, counterfactual queries | `EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:83`; audit line 2350 | UNSTATED | MISSED | [CP-34](#cp-34) | subject triage | TRACE/BUILD |
| `REQ-GRA-276` | `TASK-LD-004`: - **TASK-LD-004**: Implement Graph-over-Graph (CORE-004) — layers, cross-layer queries, merge, diff, constraint propagation | `EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:26`; audit line 2354 | UNSTATED | MISSED | [CP-13](#cp-13) | subject triage | TRACE/BUILD |
| `REQ-GRA-277` | `TASK-LIC-003`: - **TASK-LIC-003**: Define metering model — what usage metrics drive billing (API calls, graph nodes, agents, tokens) | `EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:22`; audit line 2384 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-GRA-278` | `TASK-LIC-006`: - **TASK-LIC-006**: Evaluate graph database licensing costs for supported backends (Neo4j Enterprise, TigerGraph, Amazon Neptune) | `EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:38`; audit line 2387 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-GRA-279` | `TASK-LIC-013`: - **TASK-LIC-013**: Ensure license compliance for all deployment scenarios (single-tenant, multi-tenant, edge) | `EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:68`; audit line 2394 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-GRA-280` | `TASK-MKE-010`: - **TASK-MKE-010**: Create tutorial video series — installation, first graph, first query, first agent | `EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:49`; audit line 2404 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-GRA-281` | `TASK-MKT-002`: - **TASK-MKT-002**: Define positioning statement against competitors (Palantir, Neo4j Aura, DataStax, Databricks) | `EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:17`; audit line 2408 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-GRA-282` | `TASK-MKT-010`: - **TASK-MKT-010**: Conference and event strategy — identify 3-5 target conferences (KGC, AI Summit, GraphConnect) | `EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:58`; audit line 2416 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-GRA-283` | `TASK-MKT-013`: - **TASK-MKT-013**: Develop brand guidelines — logo, color palette, typography, voice | `EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:73`; audit line 2419 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-GRA-284` | `TASK-QA-004`: - **TASK-QA-004**: Execute unit tests for Graph-over-Graph (CORE-004) | `EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:23`; audit line 2424 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-GRA-285` | `TASK-QAL-003`: - **TASK-QAL-003**: Establish test data management strategy for graph stores, RAG, and agent tests | `EOIP-engg-doc-pkg/roles/QALead_tasks.md:22`; audit line 2436 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-GRA-286` | `TASK-QAL-005`: - **TASK-QAL-005**: Phase 1 test plan — Token formats (round-trip fuzz), Verification (rule composition), Intent Router (classification accuracy), Graph-over-Graph (cross-layer queries) | `EOIP-engg-doc-pkg/roles/QALead_tasks.md:34`; audit line 2438 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-GRA-287` | `TEST-FR-GRAPH-001`: &#124; FR-GRAPH-001 &#124; Graph Core &#124; WP-FOUNDATION &#124; TEST-FR-GRAPH-001 &#124; AC-FR-GRAPH-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:29`; audit line 2508 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-288` | `TEST-FR-GRAPH-002`: &#124; FR-GRAPH-002 &#124; Graph Core &#124; WP-FOUNDATION &#124; TEST-FR-GRAPH-002 &#124; AC-FR-GRAPH-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:30`; audit line 2509 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-289` | `TEST-FR-GRAPH-003`: &#124; FR-GRAPH-003 &#124; Graph Core &#124; WP-FOUNDATION &#124; TEST-FR-GRAPH-003 &#124; AC-FR-GRAPH-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:31`; audit line 2510 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-290` | `TEST-FR-GRAPH-004`: &#124; FR-GRAPH-004 &#124; Graph Core &#124; WP-FOUNDATION &#124; TEST-FR-GRAPH-004 &#124; AC-FR-GRAPH-004 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:32`; audit line 2511 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-291` | `TEST-FR-GRAPH-005`: &#124; FR-GRAPH-005 &#124; Graph Core &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-GRAPH-005 &#124; AC-FR-GRAPH-005 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:33`; audit line 2512 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-292` | `TEST-FR-GRAPH-006`: &#124; FR-GRAPH-006 &#124; Graph Core &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-GRAPH-006 &#124; AC-FR-GRAPH-006 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:34`; audit line 2513 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-293` | `TEST-FR-GRAPH-007`: &#124; FR-GRAPH-007 &#124; Graph Core &#124; WP-QUERY &#124; TEST-FR-GRAPH-007 &#124; AC-FR-GRAPH-007 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:35`; audit line 2514 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-294` | `TEST-FR-GRAPH-008`: &#124; FR-GRAPH-008 &#124; Graph Core &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-GRAPH-008 &#124; AC-FR-GRAPH-008 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:36`; audit line 2515 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-295` | `TEST-FR-GRAPH-009`: &#124; FR-GRAPH-009 &#124; Graph Core &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-GRAPH-009 &#124; AC-FR-GRAPH-009 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:37`; audit line 2516 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-296` | `TEST-FR-GRAPH-010`: &#124; FR-GRAPH-010 &#124; Graph Core &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-GRAPH-010 &#124; AC-FR-GRAPH-010 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:38`; audit line 2517 | UNSTATED | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-GRA-297` | `WP-CODEGRAPH-01`: ### WP-CODEGRAPH-01 — Deterministic code parser | `EOIP-engg-doc-pkg/implementation/wp-codegraph.md:23`; audit line 2626 | UNSTATED | MISSED | [CP-37](#cp-37) | ID family | TRACE/BUILD |
| `REQ-GRA-298` | `WP-CODEGRAPH-02`: ### WP-CODEGRAPH-02 — Python and TypeScript MVP parsing | `EOIP-engg-doc-pkg/implementation/wp-codegraph.md:32`; audit line 2627 | UNSTATED | MISSED | [CP-37](#cp-37) | ID family | TRACE/BUILD |
| `REQ-GRA-299` | `WP-CODEGRAPH-03`: ### WP-CODEGRAPH-03 — Commit-to-symbol linking | `EOIP-engg-doc-pkg/implementation/wp-codegraph.md:41`; audit line 2628 | UNSTATED | MISSED | [CP-37](#cp-37) | ID family | TRACE/BUILD |
| `REQ-GRA-300` | `WP-CODEGRAPH-04`: ### WP-CODEGRAPH-04 — Call/import/dependency edges | `EOIP-engg-doc-pkg/implementation/wp-codegraph.md:50`; audit line 2629 | UNSTATED | MISSED | [CP-37](#cp-37) | ID family | TRACE/BUILD |
| `REQ-GRA-301` | `WP-CODEGRAPH-05`: ### WP-CODEGRAPH-05 — Source navigation | `EOIP-engg-doc-pkg/implementation/wp-codegraph.md:59`; audit line 2630 | UNSTATED | MISSED | [CP-37](#cp-37) | ID family | TRACE/BUILD |
| `REQ-GRA-302` | `WP-EXPERIENCE-02`: ### WP-EXPERIENCE-02 — Graph explorer | `EOIP-engg-doc-pkg/implementation/wp-experience.md:33`; audit line 2641 | UNSTATED | MISSED | [CP-23](#cp-23) | subject triage | TRACE/BUILD |
| `REQ-GRA-303` | `WP-EXPERIENCE-04`: ### WP-EXPERIENCE-04 — Admin graph quality UI | `EOIP-engg-doc-pkg/implementation/wp-experience.md:51`; audit line 2643 | UNSTATED | MISSED | [CP-24](#cp-24) | subject triage | TRACE/BUILD |
| `REQ-GRA-304` | `WP-FOUNDATION-01`: ### WP-FOUNDATION-01 — HugeGraph authoritative store | `EOIP-engg-doc-pkg/implementation/wp-foundation.md:23`; audit line 2646 | UNSTATED | MISSED | [CP-13](#cp-13) | subject triage | TRACE/BUILD |
| `REQ-GRA-305` | `WP-FOUNDATION-02`: ### WP-FOUNDATION-02 — Logical graph domains | `EOIP-engg-doc-pkg/implementation/wp-foundation.md:32`; audit line 2647 | UNSTATED | MISSED | [CP-13](#cp-13) | subject triage | TRACE/BUILD |
| `REQ-GRA-306` | `WP-VALIDATION-01`: ### WP-VALIDATION-01 — Graph validation rules | `EOIP-engg-doc-pkg/implementation/wp-validation.md:21`; audit line 2699 | UNSTATED | MISSED | [CP-17](#cp-17) | ID family | TRACE/BUILD |
| `REQ-GRA-307` | `WP-VALIDATION-03`: ### WP-VALIDATION-03 — Graph quality metrics | `EOIP-engg-doc-pkg/implementation/wp-validation.md:39`; audit line 2701 | UNSTATED | MISSED | [CP-17](#cp-17) | ID family | TRACE/BUILD |

### A.8 IMP: 9 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-IMP-001` | `AC-03`: &#124; AC-03 &#124; Blast radius renders concentric rings with depth/type breakdown and risk &#124; No competitor has this &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1034`; audit line 101 | UNSTATED | MISSED | [CP-18](#cp-18) | subject triage | TRACE/BUILD |
| `REQ-IMP-002` | `AC-19`: &#124; AC-19 &#124; What-if simulation shows impact of entity removal &#124; No competitor has this &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1050`; audit line 117 | UNSTATED | MISSED | [CP-18](#cp-18) | subject triage | TRACE/BUILD |
| `REQ-IMP-003` | `AIDLC-014.4`: - [ ] `AIDLC-014.4` Impact assessment template | `eoip-phase4-2-requirements.md:2279`; audit line 368 | UNSTATED | MISSED | [CP-18](#cp-18) | subject triage | TRACE/BUILD |
| `REQ-IMP-004` | `FR-VSCODE-002`: VS Code trace/impact commands | `EOIP-engg-doc-pkg/03-functional-requirements.md:675`; audit line 603 | P0 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-IMP-005` | `GAP-STUDIO-010`: GAP-STUDIO-010: Impact preview before publish | `EOIP-engg-doc-pkg/gaps-requirements.md:612`; audit line 1494 | P0 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | subject triage | PROVE |
| `REQ-IMP-006` | `SDLC-014.4`: - [ ] `SDLC-014.4` No impact on PR latency | `eoip-phase4-2-requirements.md:1660`; audit line 1853 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-IMP-007` | `SDLC-016.3`: - [ ] `SDLC-016.3` PR impact comment on internal PRs | `eoip-phase4-2-requirements.md:1696`; audit line 1862 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-IMP-008` | `TASK-DM-010`: - **TASK-DM-010**: Maintain project risk register with probability, impact, and mitigation plans | `EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:63`; audit line 2330 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-IMP-009` | `WP-EXPERIENCE-06`: ### WP-EXPERIENCE-06 — VS Code trace/impact commands | `EOIP-engg-doc-pkg/implementation/wp-experience.md:69`; audit line 2645 | UNSTATED | MISSED | [CP-29](#cp-29) | subject triage | TRACE/BUILD |

### A.9 ING: 117 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-ING-001` | `AC-28`: &#124; AC-28 &#124; AMBIGUOUS evidence status supported alongside DETERMINISTIC/INFERRED/MANUAL &#124; Matches Graphify's 3-tier evidence (EXTRACTED/INFERRED/AMBIGUOUS) &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1059`; audit line 126 | UNSTATED | MISSED | [CP-15](#cp-15) | subject triage | TRACE/BUILD |
| `REQ-ING-002` | `AC-FR-INGEST-001`: &#124; FR-INGEST-001 &#124; Ingestion &#124; WP-INGESTION &#124; TEST-FR-INGEST-001 &#124; AC-FR-INGEST-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:24`; audit line 179 | UNSTATED | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-003` | `AC-FR-INGEST-002`: &#124; FR-INGEST-002 &#124; Ingestion &#124; WP-INGESTION &#124; TEST-FR-INGEST-002 &#124; AC-FR-INGEST-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:25`; audit line 180 | UNSTATED | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-004` | `AC-FR-INGEST-003`: &#124; FR-INGEST-003 &#124; Ingestion &#124; WP-INGESTION &#124; TEST-FR-INGEST-003 &#124; AC-FR-INGEST-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:26`; audit line 181 | UNSTATED | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-005` | `AC-FR-INGEST-004`: &#124; FR-INGEST-004 &#124; Ingestion &#124; WP-INGESTION &#124; TEST-FR-INGEST-004 &#124; AC-FR-INGEST-004 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:27`; audit line 182 | UNSTATED | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-006` | `AC-FR-INGEST-005`: &#124; FR-INGEST-005 &#124; Ingestion &#124; WP-INGESTION &#124; TEST-FR-INGEST-005 &#124; AC-FR-INGEST-005 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:28`; audit line 183 | UNSTATED | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-007` | `AI-002.2`: - [x] `AI-002.2` Sentiment analysis with aspect extraction | `eoip-phase4-2-requirements.md:676`; audit line 265 | UNSTATED | MISSED | [CP-15](#cp-15) | engine family | TRACE/BUILD |
| `REQ-ING-008` | `AI-003`: Relation Extraction & Triple Generation | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:435`; audit line 269 | P1 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | engine family | PROVE |
| `REQ-ING-009` | `AI-003.1`: - [x] `AI-003.1` Pattern-based relation extraction | `eoip-phase4-2-requirements.md:698`; audit line 270 | UNSTATED | MISSED | [CP-17](#cp-17) | engine family | TRACE/BUILD |
| `REQ-ING-010` | `AIDLC-014.3`: - [ ] `AIDLC-014.3` Mapping to EU AI Act, NIST AI RMF, ISO/IEC 42001 | `eoip-phase4-2-requirements.md:2278`; audit line 367 | UNSTATED | MISSED | [CP-15](#cp-15) | subject triage | TRACE/BUILD |
| `REQ-ING-011` | `CG-CODE-02`: Publish the exact polyglot parser language matrix | `EOIP-engg-doc-pkg/17-code-graph.md:28`; audit line 384 | P1 | PARTIAL | [CP-15](#cp-15) | area fallback | COMPLETE |
| `REQ-ING-012` | `COMPLY-002.3`: - [x] `COMPLY-002.3` Pseudonymization with token mapping | `eoip-phase4-2-requirements.md:1192`; audit line 405 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-ING-013` | `FR-03`: &#124; FR-03 &#124; Code and engineering intelligence &#124; Repository/code graph extraction, commits, services, APIs, ownership, SBOM, CI/CD/runtime/observability evidence, architecture links, and engineering risk reasoning. &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1082`; audit line 497 | UNSTATED | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-ING-014` | `FR-CODE-001`: Deterministic code parser | `EOIP-engg-doc-pkg/03-functional-requirements.md:325`; audit line 511 | P0 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-ING-015` | `FR-INGEST-001`: Raw capture | `EOIP-engg-doc-pkg/03-functional-requirements.md:101`; audit line 538 | P0 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-ING-016` | `FR-INGEST-002`: Canonicalization | `EOIP-engg-doc-pkg/03-functional-requirements.md:111`; audit line 539 | P0 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-ING-017` | `FR-INGEST-003`: Idempotent mutation | `EOIP-engg-doc-pkg/03-functional-requirements.md:121`; audit line 540 | P0 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-ING-018` | `FR-INGEST-004`: Ingestion job lifecycle | `EOIP-engg-doc-pkg/03-functional-requirements.md:131`; audit line 541 | P0 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-ING-019` | `FR-INGEST-005`: Dead-letter processing | `EOIP-engg-doc-pkg/03-functional-requirements.md:141`; audit line 542 | P0 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-ING-020` | `G2-EKAF-006`: G2-EKAF-006 — Webhook/event ingestion | `EOIP-engg-doc-pkg/gaps2-requirements.md:215`; audit line 681 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-ING-021` | `G2-EKAF-012`: G2-EKAF-012 — Checkpointing | `EOIP-engg-doc-pkg/gaps2-requirements.md:238`; audit line 687 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-ING-022` | `G2-EKAF-018`: G2-EKAF-018 — Mapping drift | `EOIP-engg-doc-pkg/gaps2-requirements.md:272`; audit line 693 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-ING-023` | `GAP-CDC-006`: GAP-CDC-006: Replay from checkpoint | `EOIP-engg-doc-pkg/gaps-requirements.md:808`; audit line 1256 | P1 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-ING-024` | `GAP-CONTRACT-001`: GAP-CONTRACT-001: Define contracts between source systems and ontology mappings | `EOIP-engg-doc-pkg/gaps-implementation.md:292`; audit line 1263 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | subject triage | PROVE |
| `REQ-ING-025` | `GAP-CONTRACT-003`: GAP-CONTRACT-003: Fail or quarantine ingestion when required semantic invariants are violated | `EOIP-engg-doc-pkg/gaps-requirements.md:441`; audit line 1265 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | subject triage | PROVE |
| `REQ-ING-026` | `GAP-CONTRACT-005`: GAP-CONTRACT-005: Maintain producer/consumer mapping contracts | `EOIP-engg-doc-pkg/gaps-requirements.md:443`; audit line 1267 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | subject triage | PROVE |
| `REQ-ING-027` | `GAP-CP-004`: GAP-CP-004: Maintain policy, validation, provenance and mapping metadata | `EOIP-engg-doc-pkg/gaps-requirements.md:402`; audit line 1272 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | subject triage | PROVE |
| `REQ-ING-028` | `GAP-DUAL-002`: GAP-DUAL-002: Guarantee round-trip mappings for supported ontology constructs | `EOIP-engg-doc-pkg/gaps-requirements.md:143`; audit line 1289 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | subject triage | PROVE |
| `REQ-ING-029` | `GAP-GRAG-001`: GAP-GRAG-001: Do not make LLM extraction the only path to graph construction | `EOIP-engg-doc-pkg/gaps-implementation.md:461`; audit line 1336 | P2 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-ING-030` | `GAP-HG-005`: GAP-HG-005: Online ingestion path | `EOIP-engg-doc-pkg/gaps-requirements.md:1078`; audit line 1349 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-ING-031` | `GAP-MKT-002`: GAP-MKT-002: Package connector mappings | `EOIP-engg-doc-pkg/gaps-requirements.md:916`; audit line 1407 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-ING-032` | `GAP-NLP-001`: GAP-NLP-001: Add local entity extraction, tagging, classification and concept recommendation | `EOIP-engg-doc-pkg/gaps-requirements.md:222`; audit line 1415 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | subject triage | PROVE |
| `REQ-ING-033` | `GAP-NOCODE-001`: GAP-NOCODE-001: Build a visual Ontology Studio for ontology classes, properties, edges, SHACL-like constraints and mappings | `EOIP-engg-doc-pkg/gaps-requirements.md:194`; audit line 1417 | P0 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | subject triage | PROVE |
| `REQ-ING-034` | `GAP-STUDIO-009`: GAP-STUDIO-009: Crosswalk/mapping designer | `EOIP-engg-doc-pkg/gaps-requirements.md:611`; audit line 1493 | P0 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | subject triage | PROVE |
| `REQ-ING-035` | `GAP-TEMP-001`: GAP-TEMP-001: Support event time and system/ingestion time | `EOIP-engg-doc-pkg/gaps-requirements.md:568`; audit line 1498 | P1 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-ING-036` | `GAP-TRUTH-004`: GAP-TRUTH-004: Store extraction confidence | `EOIP-engg-doc-pkg/gaps-requirements.md:473`; audit line 1514 | P1 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | subject triage | PROVE |
| `REQ-ING-037` | `KGR-G-002`: Local Multimodal Audio & Document Ingestion Pipeline | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:28`; audit line 1611 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-ING-038` | `MVP-FR-003`: Jira JSON ingestion | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:101`; audit line 1681 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | subject triage | PROVE |
| `REQ-ING-039` | `MVP-FR-004`: Git repository/GitLab ingestion | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:102`; audit line 1682 | P0 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | subject triage | PROVE |
| `REQ-ING-040` | `MVP-FR-018`: Admin ingestion/validation UI | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:116`; audit line 1697 | P0 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | subject triage | PROVE |
| `REQ-ING-041` | `MVP-P2`: &#124; MVP-P2 &#124; Ingestion MVP &#124; Build the core ingestion engine with demo/manual/file/git/code inputs, connector framework, retry/dead-letter behavior, cursoring, and deterministic demo data loading. &#124; EOIP-engg-doc-pkg/1... | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md:46`; audit line 1711 | P2 | MISSED | [CP-10](#cp-10) | subject triage | TRACE/BUILD |
| `REQ-ING-042` | `NFR-04`: &#124; NFR-04 &#124; Reliability &#124; Local Docker startup must complete with healthy services; ingestion must tolerate retries and partial source failures; backup/restore must be documented and verifiable. &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1096`; audit line 1728 | UNSTATED | MISSED | [CP-31](#cp-31) | subject triage | TRACE/BUILD |
| `REQ-ING-043` | `NFR-05`: &#124; NFR-05 &#124; Performance and scale &#124; Batch ingestion, traversal budgets, retrieval latency, indexing strategy, and benchmark evidence must be maintained as product acceptance criteria. &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1097`; audit line 1729 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-ING-044` | `PRE-001.1`: - [x] `PRE-001.1` Check each package this roadmap creates against the repo (verification/, federation/, causal/, xai/, extraction/, observability/, embeddings/, routing/, token_formats/, token_budget/, graph_graph/, dist... | `eoip-phase4-2-requirements.md:196`; audit line 1753 | UNSTATED | MISSED | [CP-00](#cp-00) | ID family | TRACE/BUILD |
| `REQ-ING-045` | `PRE-001.3`: - [x] `PRE-001.3` Decide module ownership for the duplicated extractor work (AGENT-002, AI-002, AI-003) and record it (conflict B6). | `eoip-phase4-2-requirements.md:198`; audit line 1755 | UNSTATED | MISSED | [CP-00](#cp-00) | ID family | TRACE/BUILD |
| `REQ-ING-046` | `SDLC-009.2`: - [ ] `SDLC-009.2` Used by at least ingestion, agent fan-out and RAG paths | `eoip-phase4-2-requirements.md:1564`; audit line 1826 | UNSTATED | MISSED | [CP-10](#cp-10) | engine family | TRACE/BUILD |
| `REQ-ING-047` | `SDLC-016.1`: - [ ] `SDLC-016.1` Self-ingestion job | `eoip-phase4-2-requirements.md:1694`; audit line 1860 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-ING-048` | `SDLC-034.1`: - [ ] `SDLC-034.1` Control mapping document with evidence links | `eoip-phase4-2-requirements.md:2029`; audit line 1950 | UNSTATED | MISSED | [CP-33](#cp-33) | engine family | TRACE/BUILD |
| `REQ-ING-049` | `SR-ARC-001`: &#124; SR-ARC-001 &#124; **Modular monolith first, service-extractable:** modules communicate through typed interfaces/events and MUST be separable into independently scalable services without code rewrite (preserves the prior `... | `EOIP-engg-doc-pkg/super-requirements.md:162`; audit line 1975 | P0 | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-ING-050` | `SR-ARC-003`: &#124; SR-ARC-003 &#124; **Event backbone:** an append-only event log (pluggable: embedded log for DP-0; NATS JetStream/Kafka-class for clustered) carries ingestion, mutation, policy and audit events; consumers are idempotent (o... | `EOIP-engg-doc-pkg/super-requirements.md:164`; audit line 1977 | P0 | MISSED | [CP-10](#cp-10) | subject triage | TRACE/BUILD |
| `REQ-ING-051` | `SR-COM-007`: &#124; SR-COM-007 &#124; **Documentation set:** admin, user, API/SDK, connector developer, ontology guide, security whitepaper, architecture, reference deployments, runbooks, compliance mappings, release notes, upgrade guides, t... | `EOIP-engg-doc-pkg/super-requirements.md:1006`; audit line 1999 | P0 | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-ING-052` | `SR-COM-020`: &#124; SR-COM-020 &#124; Pack SDK and signed distribution format: ontology layer, mapping templates, connector bundles, validation/policy rules, glossary, sample dataset generator, golden questions, report templates, compliance ... | `EOIP-engg-doc-pkg/super-requirements.md:1034`; audit line 2003 | P0 | IMPLEMENTED-UNVERIFIED | [CP-33](#cp-33) | ID family | PROVE |
| `REQ-ING-053` | `SR-CON-005`: &#124; SR-CON-005 &#124; **LLM-optional:** ingestion, graph construction, validation, deterministic query, impact analysis, lineage and reporting MUST work with no LLM present. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:102`; audit line 2009 | P0 | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-ING-054` | `SR-EXT-010`: &#124; SR-EXT-010 &#124; **Extension points:** connectors, parsers/extractors, relationship-discovery methods, identity-resolution matchers, graph algorithms, store adapters, query-dialect adapters, model providers, agents/skill... | `EOIP-engg-doc-pkg/super-requirements.md:786`; audit line 2033 | P0 | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-ING-055` | `SR-EXT-015`: &#124; SR-EXT-015 &#124; **Low-code Studio:** visual pipeline, mapping, rule, agent and report builders that emit the same versioned artifacts as code. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:791`; audit line 2038 | P1 | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-ING-056` | `SR-GDB-007`: &#124; SR-GDB-007 &#124; **Virtual/zero-ETL graph mode:** optionally expose existing relational/lakehouse data as a graph view through declarative mappings (OBDA/virtual-graph style) without copying data. &#124; P2 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:189`; audit line 2045 | P2 | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-ING-057` | `SR-GDB-008`: &#124; SR-GDB-008 &#124; **Multi-model graph support:** property graph (LPG) and RDF are both first-class; RDF-star/reification patterns and LPG↔RDF round-trip mappings MUST be defined and tested. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:190`; audit line 2046 | P1 | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-ING-058` | `SR-GOV-001`: &#124; SR-GOV-001 &#124; **Compliance Pack format:** control catalog, mapping to platform capabilities, automated evidence queries over the graph/audit, report templates, gap analysis. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:868`; audit line 2055 | P1 | IMPLEMENTED-UNVERIFIED | [CP-25](#cp-25) | subject triage | PROVE |
| `REQ-ING-059` | `SR-GOV-003`: &#124; SR-GOV-003 &#124; **Change governance:** ontology, mapping, policy, model and agent changes use proposal → review → approval → rollout with audit and rollback. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:870`; audit line 2057 | P0 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | subject triage | PROVE |
| `REQ-ING-060` | `SR-ING-001`: &#124; SR-ING-001 &#124; **Connector SDK** (Python and TypeScript at P0; Go/Java at P1) with a stable contract: `discover`, `authenticate`, `fetch(cursor)`, `schema`, `health`, `metrics`, `capabilities`, `deletion_semantics`; co... | `EOIP-engg-doc-pkg/super-requirements.md:345`; audit line 2060 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-061` | `SR-ING-002`: &#124; SR-ING-002 &#124; Resiliency: pagination, rate-limit adaptation, retry with jitter, circuit breaker, checkpoint/cursor, partial-failure isolation, DLQ, replay, dry-run, backfill and incremental sync. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:346`; audit line 2061 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-062` | `SR-ING-003`: &#124; SR-ING-003 &#124; **Change capture:** polling, webhooks, CDC (log-based where the source supports it), file watchers, stream consumers; deletes handled by tombstones with configurable semantics (soft delete, retire edge, ... | `EOIP-engg-doc-pkg/super-requirements.md:347`; audit line 2062 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-063` | `SR-ING-004`: &#124; SR-ING-004 &#124; **Credential isolation:** connector secrets live only in the secret store, scoped per tenant/connector, rotated, never logged, never visible to plugins other than the owning connector. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:348`; audit line 2063 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-064` | `SR-ING-005`: &#124; SR-ING-005 &#124; **Connector marketplace-ready packaging:** signed manifest, version, compatibility range, data-flow manifest, test fixtures, health contract. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:349`; audit line 2064 | P1 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-065` | `SR-ING-006`: &#124; SR-ING-006 &#124; **Streaming and batch share one pipeline:** the same stages and mapping specs serve both; back-pressure and priority lanes per tenant. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:350`; audit line 2065 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-066` | `SR-ING-007`: &#124; SR-ING-007 &#124; **Large-JSON handling:** streaming parse (never load whole file), gz/zstd/archive support, malformed-record quarantine with line/offset pointers, numeric precision and Unicode/timezone normalization, bin... | `EOIP-engg-doc-pkg/super-requirements.md:351`; audit line 2066 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-067` | `SR-ING-010`: &#124; SR-ING-010 &#124; The **Schema Profiler** MUST infer types, nullability, cardinality, uniqueness, enumerations, formats (email, UUID, URL, IP/CIDR, ISO date/time, currency, phone, IBAN, ARN/URN, git SHA, ticket keys like ... | `EOIP-engg-doc-pkg/super-requirements.md:379`; audit line 2067 | P0 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-ING-068` | `SR-ING-011`: &#124; SR-ING-011 &#124; **Entity detection:** record types from top-level arrays/envelopes/discriminator fields; nested objects classified as *embedded value*, *child entity*, or *reference* using a scored heuristic (key presen... | `EOIP-engg-doc-pkg/super-requirements.md:380`; audit line 2068 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-069` | `SR-ING-012`: &#124; SR-ING-012 &#124; **Key detection:** natural/surrogate key candidates; composite keys; stability scoring across runs; canonical ID minting strategy per type (deterministic, namespaced, collision-safe). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:381`; audit line 2069 | P0 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-ING-070` | `SR-ING-013`: &#124; SR-ING-013 &#124; **Relationship discovery — explicit:** foreign-key-like fields, `$ref`/JSON Pointer, URLs to known entities, `*_id`/`parent`/`owner` conventions, join-table detection (junction → edge with properties), p... | `EOIP-engg-doc-pkg/super-requirements.md:382`; audit line 2070 | P0 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-ING-071` | `SR-ING-014`: &#124; SR-ING-014 &#124; **Relationship discovery — statistical:** inclusion-dependency and value-overlap discovery across datasets (MinHash/LSH containment for scale), name and embedding-based schema matching, co-occurrence, te... | `EOIP-engg-doc-pkg/super-requirements.md:383`; audit line 2071 | P0 | PARTIAL | [CP-15](#cp-15) | ID family | COMPLETE |
| `REQ-ING-072` | `SR-ING-015`: &#124; SR-ING-015 &#124; **Relationship discovery — operational:** service-call edges from traces/logs, config references (env var → secret → account), IaC dependency edges, build/runtime dependencies from SBOM and lockfiles, co... | `EOIP-engg-doc-pkg/super-requirements.md:384`; audit line 2072 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-073` | `SR-ING-016`: &#124; SR-ING-016 &#124; **Edge classes and honesty:** every edge is `ASSERTED` (source says so), `DERIVED` (deterministic rule), `INFERRED` (statistical/ML/LLM), or `CURATED` (human-approved), with confidence and method. Inferr... | `EOIP-engg-doc-pkg/super-requirements.md:385`; audit line 2073 | P0 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-ING-074` | `SR-ING-017`: &#124; SR-ING-017 &#124; **Ontology induction:** propose classes, properties, relation types and hierarchies from data; present for steward approval in the Mapping Studio; support *ontology-first*, *data-first* and *hybrid* mode... | `EOIP-engg-doc-pkg/super-requirements.md:386`; audit line 2074 | P1 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-075` | `SR-ING-018`: &#124; SR-ING-018 &#124; **Link prediction / graph completion** (heuristic and learned, e.g., translational and GNN-class models) proposes missing edges into a review queue; auto-assertion only above a tenant-configured threshol... | `EOIP-engg-doc-pkg/super-requirements.md:387`; audit line 2075 | P2 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-076` | `SR-ING-019`: &#124; SR-ING-019 &#124; **Mapping DSL:** declarative, versioned, diff-able mappings (YAML/JSON) with RML/R2RML and JSON-LD `@context` import/export; generated by inference, editable by humans, testable on samples. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:388`; audit line 2076 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-077` | `SR-ING-020`: &#124; SR-ING-020 &#124; **Schema drift handling:** new/changed/removed fields trigger drift events, auto-compatible mapping updates when safe, and steward review when not; mappings are pinned per run for reproducibility. &#124; P0 ... | `EOIP-engg-doc-pkg/super-requirements.md:389`; audit line 2077 | P0 | PARTIAL | [CP-15](#cp-15) | ID family | COMPLETE |
| `REQ-ING-078` | `SR-ING-030`: &#124; SR-ING-030 &#124; Deterministic rules first (exact keys, normalized emails/IDs), then probabilistic (blocking via sorted-neighborhood/canopy/LSH; pairwise similarity with string/phonetic/numeric/date/embedding features; F... | `EOIP-engg-doc-pkg/super-requirements.md:414`; audit line 2078 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-079` | `SR-ING-031`: &#124; SR-ING-031 &#124; **Collective resolution** using graph context (shared neighbors, co-authorship, same repo/team) and transitive clustering with constraints; **survivorship rules** produce golden records with per-attribut... | `EOIP-engg-doc-pkg/super-requirements.md:415`; audit line 2079 | P1 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-080` | `SR-ING-032`: &#124; SR-ING-032 &#124; Every merge is **explainable, reversible (unmerge), audited**; three bands (auto-merge / human review / reject) with tenant-set thresholds and an active-learning review queue. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:416`; audit line 2080 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-081` | `SR-ING-033`: &#124; SR-ING-033 &#124; **Cross-source ID crosswalk** persisted as first-class graph structure (`SAME_AS` with confidence and evidence) so aliases resolve at query time. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:417`; audit line 2081 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-082` | `SR-ING-040`: &#124; SR-ING-040 &#124; Derived graphs are computed **incrementally** from mutation events; full rebuild MUST be possible and verified equivalent to the incremental result. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:440`; audit line 2082 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-083` | `SR-ING-041`: &#124; SR-ING-041 &#124; **Graphify-class artifacts:** auto-generate portable `graph.json`, interactive HTML, and a markdown/wiki report per graph or subgraph; support export to Obsidian/Markdown vaults; support post-commit/post... | `EOIP-engg-doc-pkg/super-requirements.md:441`; audit line 2083 | P1 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-084` | `SR-ING-042`: &#124; SR-ING-042 &#124; **Traversal-first retrieval** (no embeddings required) is the baseline retrieval mode; embeddings enhance recall but are never prerequisite (consistent with SR-CON-005). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:442`; audit line 2084 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-085` | `SR-ING-043`: &#124; SR-ING-043 &#124; **Pre-aggregation:** per-type degree/centrality, per-edge-class reachability, and domain-to-domain bridge statistics are maintained to answer overview and impact questions within latency targets. &#124; P1 \... | `EOIP-engg-doc-pkg/super-requirements.md:443`; audit line 2085 | P1 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-086` | `SR-ING-050`: &#124; SR-ING-050 &#124; Validation rules with severities (`INFO/WARN/ERROR/BLOCKER`), remediation suggestions, quarantine with replay, and a data-quality scorecard (completeness, freshness, uniqueness, consistency, confidence d... | `EOIP-engg-doc-pkg/super-requirements.md:449`; audit line 2086 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-087` | `SR-ING-051`: &#124; SR-ING-051 &#124; **Freshness SLOs** per connector with alerting and a user-visible "knowledge age" on every answer. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:450`; audit line 2087 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-088` | `SR-ING-052`: &#124; SR-ING-052 &#124; **Idempotency tests:** re-running an ingestion produces zero net graph change; interrupted runs resume without duplicates (restart-safe). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:451`; audit line 2088 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-089` | `SR-ING-053`: &#124; SR-ING-053 &#124; **Reconciliation reports** (source counts vs graph counts, orphan edges, dangling references) on schedule. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:452`; audit line 2089 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-090` | `SR-ING-060`: &#124; SR-ING-060 &#124; **Hostile-input posture:** parsers sandboxed; zip-bomb/path-traversal/XXE/deserialization defenses; file-type verification; size/time limits. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:467`; audit line 2090 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-091` | `SR-ING-061`: &#124; SR-ING-061 &#124; **Indirect prompt injection defense:** ingested text is data, never instructions; extracted passages are fenced, scanned and flagged before any LLM sees them. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:468`; audit line 2091 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-092` | `SR-ING-070`: &#124; SR-ING-070 &#124; Export formats: JSON/NDJSON, CSV, Parquet, GraphML, GEXF, GraphSON, openCypher bulk CSV, RDF (Turtle, N-Quads, JSON-LD, RDF-star), DOT/Mermaid, Markdown vault, interactive HTML; full-tenant export bundle... | `EOIP-engg-doc-pkg/super-requirements.md:474`; audit line 2092 | P0 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-093` | `SR-ING-071`: &#124; SR-ING-071 &#124; BI/analytics access: read-only JDBC/ODBC SQL views, OData, GraphQL, Arrow Flight-class bulk endpoint, notebook (Jupyter) client libraries. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:475`; audit line 2093 | P1 | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-094` | `SR-NFR-001`: &#124; SR-NFR-001 &#124; **Horizontal scale** for API, query, ingestion workers, agent runners, embedding and model-serving tiers; autoscaling policies (K8s) and manual sizing for appliances. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:896`; audit line 2114 | P0 | MISSED | [CP-10](#cp-10) | subject triage | TRACE/BUILD |
| `REQ-ING-095` | `SR-NFR-007`: &#124; SR-NFR-007 &#124; **Chaos and soak testing:** node/zone failure, partition, slow disk, clock skew, backend restart mid-ingest; 7-day soak per release. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:902`; audit line 2120 | P1 | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-ING-096` | `SR-PRV-001`: &#124; SR-PRV-001 &#124; **Classification engine** at ingest (patterns, dictionaries, NER, ML; customer-extensible) labels PII/PHI/PCI/secrets/IP/legal-privileged/export-controlled; labels propagate to derived data. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:848`; audit line 2156 | P0 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-ING-097` | `SR-QA-010`: &#124; SR-QA-010 &#124; Every `SR-` requirement maps to ≥ 1 executable acceptance test; the mapping is stored as structured data (test-ID → requirement-ID), **and references in comments or docstrings never count as evidence.** \... | `EOIP-engg-doc-pkg/super-requirements.md:962`; audit line 2165 | P0 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | subject triage | PROVE |
| `REQ-ING-098` | `TASK-AIE-001`: - **TASK-AIE-001**: Implement Intent Router classifier (CORE-003) — TF-IDF feature extraction, lightweight classification model | `EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:11`; audit line 2244 | UNSTATED | MISSED | [CP-15](#cp-15) | subject triage | TRACE/BUILD |
| `REQ-ING-099` | `TASK-AIE-003`: - **TASK-AIE-003**: Implement Entity Extraction pipeline (AGENT-002) — document chunker + entity extractor | `EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:23`; audit line 2246 | UNSTATED | MISSED | [CP-15](#cp-15) | subject triage | TRACE/BUILD |
| `REQ-ING-100` | `TASK-AIE-008`: - **TASK-AIE-008**: Implement Relation Extraction (AI-003) — pattern-based triple generation | `EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:45`; audit line 2251 | UNSTATED | MISSED | [CP-15](#cp-15) | subject triage | TRACE/BUILD |
| `REQ-ING-101` | `TASK-ARCH-004`: - **TASK-ARCH-004**: Design Intent Router (CORE-003) classification architecture — feature extraction, classifier model, routing table, feedback loop | `EOIP-engg-doc-pkg/roles/Architect_tasks.md:25`; audit line 2260 | UNSTATED | MISSED | [CP-15](#cp-15) | subject triage | TRACE/BUILD |
| `REQ-ING-102` | `TASK-LAI-014`: - **TASK-LAI-014**: Design Entity Extraction pipeline (AGENT-002) — chunking strategies, extraction accuracy targets | `EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:74`; audit line 2348 | UNSTATED | MISSED | [CP-15](#cp-15) | subject triage | TRACE/BUILD |
| `REQ-ING-103` | `TASK-LAI-015`: - **TASK-LAI-015**: Design Relation Extraction (AI-003) — pattern templates, confidence scoring | `EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:79`; audit line 2349 | UNSTATED | MISSED | [CP-15](#cp-15) | subject triage | TRACE/BUILD |
| `REQ-ING-104` | `TASK-LD-011`: - **TASK-LD-011**: Implement/oversee Phase 2 engines: extraction, federation, temporal retrieval, causal inference | `EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:61`; audit line 2361 | UNSTATED | MISSED | [CP-15](#cp-15) | subject triage | TRACE/BUILD |
| `REQ-ING-105` | `TASK-LD-012`: - **TASK-LD-012**: Implement/oversee Phase 3 engines: XAI, NLP pipeline, relation extraction, MLOps | `EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:65`; audit line 2362 | UNSTATED | MISSED | [CP-15](#cp-15) | subject triage | TRACE/BUILD |
| `REQ-ING-106` | `TASK-QAL-006`: - **TASK-QAL-006**: Phase 2 test plan — Extraction pipeline (entity accuracy), Federation (multi-backend), Temporal (as-of correctness) | `EOIP-engg-doc-pkg/roles/QALead_tasks.md:38`; audit line 2439 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-ING-107` | `TEST-FR-INGEST-001`: &#124; FR-INGEST-001 &#124; Ingestion &#124; WP-INGESTION &#124; TEST-FR-INGEST-001 &#124; AC-FR-INGEST-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:24`; audit line 2520 | UNSTATED | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-108` | `TEST-FR-INGEST-002`: &#124; FR-INGEST-002 &#124; Ingestion &#124; WP-INGESTION &#124; TEST-FR-INGEST-002 &#124; AC-FR-INGEST-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:25`; audit line 2521 | UNSTATED | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-109` | `TEST-FR-INGEST-003`: &#124; FR-INGEST-003 &#124; Ingestion &#124; WP-INGESTION &#124; TEST-FR-INGEST-003 &#124; AC-FR-INGEST-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:26`; audit line 2522 | UNSTATED | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-110` | `TEST-FR-INGEST-004`: &#124; FR-INGEST-004 &#124; Ingestion &#124; WP-INGESTION &#124; TEST-FR-INGEST-004 &#124; AC-FR-INGEST-004 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:27`; audit line 2523 | UNSTATED | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-111` | `TEST-FR-INGEST-005`: &#124; FR-INGEST-005 &#124; Ingestion &#124; WP-INGESTION &#124; TEST-FR-INGEST-005 &#124; AC-FR-INGEST-005 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:28`; audit line 2524 | UNSTATED | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-112` | `WP-EXPERIENCE-03`: ### WP-EXPERIENCE-03 — Admin ingestion UI | `EOIP-engg-doc-pkg/implementation/wp-experience.md:42`; audit line 2642 | UNSTATED | MISSED | [CP-15](#cp-15) | subject triage | TRACE/BUILD |
| `REQ-ING-113` | `WP-INGESTION-01`: ### WP-INGESTION-01 — Raw capture | `EOIP-engg-doc-pkg/implementation/wp-ingestion.md:23`; audit line 2651 | UNSTATED | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-114` | `WP-INGESTION-02`: ### WP-INGESTION-02 — Canonicalization | `EOIP-engg-doc-pkg/implementation/wp-ingestion.md:32`; audit line 2652 | UNSTATED | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-115` | `WP-INGESTION-03`: ### WP-INGESTION-03 — Idempotent mutation | `EOIP-engg-doc-pkg/implementation/wp-ingestion.md:41`; audit line 2653 | UNSTATED | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-116` | `WP-INGESTION-04`: ### WP-INGESTION-04 — Ingestion job lifecycle | `EOIP-engg-doc-pkg/implementation/wp-ingestion.md:50`; audit line 2654 | UNSTATED | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |
| `REQ-ING-117` | `WP-INGESTION-05`: ### WP-INGESTION-05 — Dead-letter processing | `EOIP-engg-doc-pkg/implementation/wp-ingestion.md:59`; audit line 2655 | UNSTATED | MISSED | [CP-15](#cp-15) | ID family | TRACE/BUILD |

### A.10 LIN: 41 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-LIN-001` | `AC-FR-PROV-001`: &#124; FR-PROV-001 &#124; Provenance &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-PROV-001 &#124; AC-FR-PROV-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:41`; audit line 189 | UNSTATED | MISSED | [CP-17](#cp-17) | ID family | TRACE/BUILD |
| `REQ-LIN-002` | `AC-FR-PROV-002`: &#124; FR-PROV-002 &#124; Provenance &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-PROV-002 &#124; AC-FR-PROV-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:42`; audit line 190 | UNSTATED | MISSED | [CP-17](#cp-17) | ID family | TRACE/BUILD |
| `REQ-LIN-003` | `AIDLC-001.3`: - [ ] `AIDLC-001.3` OpenLineage events emitted | `eoip-phase4-2-requirements.md:2054`; audit line 302 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-LIN-004` | `AIDLC-015`: - **Step 6. Interface.** Design system first, then i18n, grid, charts, export, lenses, search analytics and the evidence UX. Workflow builder and collaboration last (collaboration is MS-12). Items: `UI-001`, `UI-002`, `U... | `eoip-phase4-2-requirements.md:180`; audit line 369 | UNSTATED | MISSED | [CP-25](#cp-25) | subject triage | TRACE/BUILD |
| `REQ-LIN-005` | `COMPLY-003.2`: - [x] `COMPLY-003.2` Evidence collection | `eoip-phase4-2-requirements.md:1213`; audit line 410 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-LIN-006` | `FR-PROV-001`: Evidence model | `EOIP-engg-doc-pkg/01-project-vision.md:24`; audit line 578 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-LIN-007` | `FR-PROV-002`: Provenance traversal | `EOIP-engg-doc-pkg/03-functional-requirements.md:285`; audit line 579 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-LIN-008` | `G2-ARCH-010`: G2-ARCH-010 — Evidence is mandatory | `EOIP-engg-doc-pkg/gaps2-requirements.md:96`; audit line 649 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | area fallback | PROVE |
| `REQ-LIN-009` | `GAP-AGOV-009`: GAP-AGOV-009: Complete action provenance | `EOIP-engg-doc-pkg/gaps-requirements.md:722`; audit line 1215 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | ID family | PROVE |
| `REQ-LIN-010` | `GAP-DATAOPS-001`: GAP-DATAOPS-001: Capture every transformation as lineage metadata | `EOIP-engg-doc-pkg/gaps-implementation.md:542`; audit line 1278 | P2 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | subject triage | PROVE |
| `REQ-LIN-011` | `GAP-FABRIC-005`: GAP-FABRIC-005: Local result cache with provenance/freshness | `EOIP-engg-doc-pkg/gaps-requirements.md:642`; audit line 1307 | P1 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | subject triage | PROVE |
| `REQ-LIN-012` | `GAP-GRAG-006`: GAP-GRAG-006: Persist evidence chains for every answer | `EOIP-engg-doc-pkg/gaps-requirements.md:363`; audit line 1341 | P2 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-LIN-013` | `GAP-KFW-007`: GAP-KFW-007: Maintain security provenance | `EOIP-engg-doc-pkg/gaps-requirements.md:741`; audit line 1363 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-LIN-014` | `GAP-KP-004`: GAP-KP-004: Product lineage must be navigable | `EOIP-engg-doc-pkg/gaps-requirements.md:594`; audit line 1372 | P1 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | subject triage | PROVE |
| `REQ-LIN-015` | `GAP-KRAG-007`: GAP-KRAG-007: Answer abstention when evidence is insufficient | `EOIP-engg-doc-pkg/gaps-requirements.md:682`; audit line 1386 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-LIN-016` | `GAP-KRAG-008`: GAP-KRAG-008: Confidence calibrated from evidence—not model self-confidence | `EOIP-engg-doc-pkg/gaps-requirements.md:683`; audit line 1387 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-LIN-017` | `GAP-KRAG-009`: GAP-KRAG-009: Every response includes evidence manifest | `EOIP-engg-doc-pkg/gaps-requirements.md:684`; audit line 1388 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-LIN-018` | `GAP-LIFE-002`: GAP-LIFE-002: Archive historical facts without losing lineage | `EOIP-engg-doc-pkg/gaps-requirements.md:901`; audit line 1393 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | subject triage | PROVE |
| `REQ-LIN-019` | `GAP-LIFE-005`: GAP-LIFE-005: Purge with provenance record where legally allowed | `EOIP-engg-doc-pkg/gaps-requirements.md:904`; audit line 1396 | P2 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | subject triage | PROVE |
| `REQ-LIN-020` | `GAP-LIN-001`: GAP-LIN-001: Map internal lineage to OpenLineage concepts where applicable | `EOIP-engg-doc-pkg/gaps-implementation.md:541`; audit line 1398 | P2 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-LIN-021` | `GAP-LIN-002`: GAP-LIN-002: Map semantic provenance to PROV-O where applicable | `EOIP-engg-doc-pkg/gaps-requirements.md:792`; audit line 1399 | P2 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-LIN-022` | `GAP-LIN-003`: GAP-LIN-003: Keep internal richer model without losing standards compatibility | `EOIP-engg-doc-pkg/gaps-requirements.md:793`; audit line 1400 | P2 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-LIN-023` | `GAP-LIN-004`: GAP-LIN-004: Ingest lineage events from CI/CD and data pipelines | `EOIP-engg-doc-pkg/gaps-requirements.md:794`; audit line 1401 | P2 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-LIN-024` | `GAP-LIN-005`: GAP-LIN-005: Emit lineage events for platform transformations | `EOIP-engg-doc-pkg/gaps-requirements.md:795`; audit line 1402 | P2 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-LIN-025` | `GAP-PROV-001`: GAP-PROV-001: Represent Entity, Activity and Agent provenance concepts | `EOIP-engg-doc-pkg/gaps-implementation.md:167`; audit line 1431 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-LIN-026` | `GAP-PROV-002`: GAP-PROV-002: Every inferred edge must reference the evidence used | `EOIP-engg-doc-pkg/gaps-requirements.md:455`; audit line 1432 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-LIN-027` | `GAP-PROV-003`: GAP-PROV-003: Preserve extraction algorithm/model/parser version | `EOIP-engg-doc-pkg/gaps-requirements.md:456`; audit line 1433 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-LIN-028` | `GAP-PROV-004`: GAP-PROV-004: Preserve source checksum/version | `EOIP-engg-doc-pkg/gaps-requirements.md:457`; audit line 1434 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-LIN-029` | `GAP-PROV-005`: GAP-PROV-005: Support graph-path evidence bundles | `EOIP-engg-doc-pkg/gaps-requirements.md:458`; audit line 1435 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-LIN-030` | `GAP-PROV-006`: GAP-PROV-006: Every AI answer returns an Evidence Manifest | `EOIP-engg-doc-pkg/gaps-requirements.md:459`; audit line 1436 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-LIN-031` | `GAP-PROV-007`: GAP-PROV-007: Evidence manifests must be exportable and immutable after issuance | `EOIP-engg-doc-pkg/gaps-requirements.md:460`; audit line 1437 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-LIN-032` | `GAP-PROV-008`: GAP-PROV-008: Provide “why does this edge exist?” UI | `EOIP-engg-doc-pkg/gaps-requirements.md:461`; audit line 1438 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-LIN-033` | `GAP-PROV-009`: GAP-PROV-009: Provide “what would disappear if source X were removed?” analysis | `EOIP-engg-doc-pkg/gaps-requirements.md:462`; audit line 1439 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-LIN-034` | `GAP-RET-003`: GAP-RET-003: Rank using evidence quality, recency, authority and relevance | `EOIP-engg-doc-pkg/gaps-requirements.md:665`; audit line 1454 | P0 | IMPLEMENTED-UNVERIFIED | [CP-20](#cp-20) | ID family | PROVE |
| `REQ-LIN-035` | `GAP-SDT-003`: GAP-SDT-003: Each link must have provenance, confidence and evidence | `EOIP-engg-doc-pkg/gaps-requirements.md:383`; audit line 1464 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | subject triage | PROVE |
| `REQ-LIN-036` | `MVP-FR-011`: Provenance | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:109`; audit line 1690 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | subject triage | PROVE |
| `REQ-LIN-037` | `SDLC-015.2`: - [ ] `SDLC-015.2` PR template with evidence checklist | `eoip-phase4-2-requirements.md:1677`; audit line 1856 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-LIN-038` | `SR-ARC-012`: &#124; SR-ARC-012 &#124; **Mandatory ADR process:** every decision that changes a port, a default component or a supported-backend tier needs an ADR with alternatives, license review and benchmark evidence. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:173`; audit line 1986 | P0 | MISSED | [CP-33](#cp-33) | subject triage | TRACE/BUILD |
| `REQ-LIN-039` | `SR-QA-012`: &#124; SR-QA-012 &#124; Status dashboards MUST report three numbers separately: *tests passing*, *requirements with behavioral evidence*, *requirements with external-gate evidence*; a single "% complete" is prohibited. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:964`; audit line 2167 | P0 | IMPLEMENTED-UNVERIFIED | [CP-25](#cp-25) | subject triage | PROVE |
| `REQ-LIN-040` | `TEST-FR-PROV-001`: &#124; FR-PROV-001 &#124; Provenance &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-PROV-001 &#124; AC-FR-PROV-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:41`; audit line 2530 | UNSTATED | MISSED | [CP-17](#cp-17) | ID family | TRACE/BUILD |
| `REQ-LIN-041` | `TEST-FR-PROV-002`: &#124; FR-PROV-002 &#124; Provenance &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-PROV-002 &#124; AC-FR-PROV-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:42`; audit line 2531 | UNSTATED | MISSED | [CP-17](#cp-17) | ID family | TRACE/BUILD |

### A.11 LLM: 38 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-LLM-001` | `AI-004`: Model A/B Testing & Canary Deployment | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:456`; audit line 275 | P2 | IMPLEMENTED-UNVERIFIED | [CP-19](#cp-19) | engine family | PROVE |
| `REQ-LLM-002` | `AIDLC-007.4`: - [ ] `AIDLC-007.4` Prompts and policies loaded from the registry | `eoip-phase4-2-requirements.md:2112`; audit line 333 | UNSTATED | MISSED | [CP-19](#cp-19) | area fallback | TRACE/BUILD |
| `REQ-LLM-003` | `AIDLC-008`: &#124; `CORE-006` &#124; merge &#124; MS-27, K-03 &#124; Token accounting in MS-27 and budgets here share one cost model. Build the model once (see AIDLC-008). &#124; | `eoip-phase4-2-requirements.md:79`; audit line 334 | UNSTATED | MISSED | [CP-19](#cp-19) | area fallback | TRACE/BUILD |
| `REQ-LLM-004` | `AIDLC-010.3`: - [ ] `AIDLC-010.3` Model card generated | `eoip-phase4-2-requirements.md:2146`; audit line 347 | UNSTATED | MISSED | [CP-34](#cp-34) | subject triage | TRACE/BUILD |
| `REQ-LLM-005` | `DERIVED-LLM-SELF-001`: Frontier-grade Self-LLM engine with real inference, XAI and speculative decoding | `EOIP-engg-doc-pkg/todo-status.md:20`; audit line 466 | P0 | STUBBED | [CP-19](#cp-19) | explicit | REPLACE |
| `REQ-LLM-006` | `G2-T0003`: ### G2-T0003 — Canonical revision model | `EOIP-engg-doc-pkg/gaps2-implementation.md:90`; audit line 951 | UNSTATED | IMPLEMENTED-UNVERIFIED | [CP-19](#cp-19) | area fallback | PROVE |
| `REQ-LLM-007` | `GAP-AGOV-006`: GAP-AGOV-006: Prompt-injection detection | `EOIP-engg-doc-pkg/gaps-requirements.md:719`; audit line 1212 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | ID family | PROVE |
| `REQ-LLM-008` | `GAP-KRAG-010`: GAP-KRAG-010: Local model routing by task complexity | `EOIP-engg-doc-pkg/gaps-requirements.md:685`; audit line 1389 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-LLM-009` | `GAP-RULE-002`: GAP-RULE-002: Distinguish asserted, inferred, model-generated and human-confirmed facts | `EOIP-engg-doc-pkg/gaps-requirements.md:171`; audit line 1460 | P2 | IMPLEMENTED-UNVERIFIED | [CP-19](#cp-19) | area fallback | PROVE |
| `REQ-LLM-010` | `SDLC-003`: ###### SDLC-003: Threat model and abuse-case library per engine | `eoip-phase4-2-requirements.md:1433`; audit line 1794 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-LLM-011` | `SR-ARC-010`: **Research basis:** SR-ARC-010 (Sandboxed extension runtime, already specified but not productized); Salesforce AppExchange model; VS Code 40,000+ extension ecosystem; Futurum Platform Ecosystem Report 2026. | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:43`; audit line 1984 | UNSTATED | MISSED | [CP-25](#cp-25) | subject triage | TRACE/BUILD |
| `REQ-LLM-012` | `SR-GOV-002`: &#124; SR-GOV-002 &#124; **AI governance:** model cards, AI-BOM, evaluation records, intended-use and prohibited-use settings, human-oversight configuration, user-visible AI labeling, AI incident workflow. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:869`; audit line 2056 | P0 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | subject triage | PROVE |
| `REQ-LLM-013` | `SR-LLM-001`: &#124; SR-LLM-001 &#124; **Model Provider Port** for chat/completion, structured output (grammar/JSON-schema constrained), tool calling, embeddings, reranking, vision/OCR, speech; capability negotiation (context length, modaliti... | `EOIP-engg-doc-pkg/super-requirements.md:604`; audit line 2094 | P0 | MISSED | [CP-19](#cp-19) | ID family | TRACE/BUILD |
| `REQ-LLM-014` | `SR-LLM-002`: &#124; SR-LLM-002 &#124; **Local/self-hosted by default.** Adapters for local runtimes (vLLM-, SGLang-, llama.cpp-, Ollama-, TGI-, ONNX Runtime-, OpenVINO-, TensorRT-LLM-class). **No external provider adapter is active until exp... | `EOIP-engg-doc-pkg/super-requirements.md:605`; audit line 2095 | P0 | MISSED | [CP-19](#cp-19) | ID family | TRACE/BUILD |
| `REQ-LLM-015` | `SR-LLM-003`: &#124; SR-LLM-003 &#124; **Model registry:** per model — source, hash, license terms (open-weight licenses differ and some restrict commercial redistribution), intended tasks, hardware profile, evaluation scores, approval status... | `EOIP-engg-doc-pkg/super-requirements.md:606`; audit line 2096 | P0 | MISSED | [CP-19](#cp-19) | ID family | TRACE/BUILD |
| `REQ-LLM-016` | `SR-LLM-004`: &#124; SR-LLM-004 &#124; **Task-based routing:** small/fast models for classification, extraction and routing; larger models for synthesis; fallbacks and circuit breakers; per-tenant model allowlists. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:607`; audit line 2097 | P0 | MISSED | [CP-19](#cp-19) | ID family | TRACE/BUILD |
| `REQ-LLM-017` | `SR-LLM-005`: &#124; SR-LLM-005 &#124; **Hardware reference configurations** (CPU-only small model; single-GPU; multi-GPU; air-gapped appliance) with sizing guidance, quantization options, throughput/latency benchmarks per release. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:608`; audit line 2098 | P0 | MISSED | [CP-19](#cp-19) | ID family | TRACE/BUILD |
| `REQ-LLM-018` | `SR-LLM-006`: &#124; SR-LLM-006 &#124; **Prompt/skill registry:** versioned prompts, schemas, few-shot sets; A/B and regression-evaluated; tenant overrides; prompt content never contains raw sensitive data unless policy allows. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:609`; audit line 2099 | P0 | MISSED | [CP-19](#cp-19) | ID family | TRACE/BUILD |
| `REQ-LLM-019` | `SR-LLM-007`: &#124; SR-LLM-007 &#124; **Embedding service** with model versioning, batch/online modes, multilingual and code models, and re-embedding jobs (SR-VDB-005). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:610`; audit line 2100 | P0 | MISSED | [CP-19](#cp-19) | ID family | TRACE/BUILD |
| `REQ-LLM-020` | `SR-LLM-008`: &#124; SR-LLM-008 &#124; **LLM observability:** per-call latency, tokens, cost, cache hits, refusals, guardrail triggers, quality scores — local telemetry only unless the tenant exports it. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:611`; audit line 2101 | P0 | MISSED | [CP-19](#cp-19) | ID family | TRACE/BUILD |
| `REQ-LLM-021` | `SR-LLM-009`: &#124; SR-LLM-009 &#124; **Guardrails:** input/output scanners (PII, secrets, injection patterns), tool allowlists, output schema validation, jailbreak/prompt-injection test corpus in CI (aligned with the OWASP LLM Top-10 catego... | `EOIP-engg-doc-pkg/super-requirements.md:612`; audit line 2102 | P0 | MISSED | [CP-19](#cp-19) | ID family | TRACE/BUILD |
| `REQ-LLM-022` | `SR-LLM-010`: &#124; SR-LLM-010 &#124; **Egress Gateway** is the *only* path to any external model; enforced by network policy so bypass is technically impossible. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:661`; audit line 2103 | P0 | IMPLEMENTED-UNVERIFIED | [CP-19](#cp-19) | ID family | PROVE |
| `REQ-LLM-023` | `SR-LLM-011`: &#124; SR-LLM-011 &#124; **Policy engine** evaluates every outbound call against the matrix, transforms the payload to the permitted level (schema-strip, aggregate, synthesize, tokenize, redact), and blocks on failure. Default i... | `EOIP-engg-doc-pkg/super-requirements.md:662`; audit line 2104 | P0 | IMPLEMENTED-UNVERIFIED | [CP-19](#cp-19) | ID family | PROVE |
| `REQ-LLM-024` | `SR-LLM-012`: &#124; SR-LLM-012 &#124; **Dry-run preview:** administrators and (for S6) requesters see the *exact* payload that would be sent before approval. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:663`; audit line 2105 | P0 | IMPLEMENTED-UNVERIFIED | [CP-19](#cp-19) | ID family | PROVE |
| `REQ-LLM-025` | `SR-LLM-013`: &#124; SR-LLM-013 &#124; **Per-call Egress Manifest** (immutable): who, what data classes, which level, which fields/tokens, endpoint, region, byte counts, approval id, response hash. A "what left the building" report is exporta... | `EOIP-engg-doc-pkg/super-requirements.md:664`; audit line 2106 | P0 | IMPLEMENTED-UNVERIFIED | [CP-19](#cp-19) | ID family | PROVE |
| `REQ-LLM-026` | `SR-LLM-014`: &#124; SR-LLM-014 &#124; **DLP and canary testing:** outbound payloads are scanned (PII/secret/PHI patterns, entropy, customer-defined dictionaries); CI plants canary values in test tenants and fails the build if any canary appe... | `EOIP-engg-doc-pkg/super-requirements.md:665`; audit line 2107 | P0 | IMPLEMENTED-UNVERIFIED | [CP-19](#cp-19) | ID family | PROVE |
| `REQ-LLM-027` | `SR-LLM-015`: &#124; SR-LLM-015 &#124; **Reversible tokenization vault** (local, per-tenant keys) re-identifies model responses locally; responses are also scanned before display. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:666`; audit line 2108 | P0 | IMPLEMENTED-UNVERIFIED | [CP-19](#cp-19) | ID family | PROVE |
| `REQ-LLM-028` | `SR-LLM-016`: &#124; SR-LLM-016 &#124; **Kill switch and budgets:** global/tenant/endpoint disable, rate and cost budgets, anomaly alerts on egress volume. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:667`; audit line 2109 | P0 | IMPLEMENTED-UNVERIFIED | [CP-19](#cp-19) | ID family | PROVE |
| `REQ-LLM-029` | `SR-LLM-017`: &#124; SR-LLM-017 &#124; **Consent and contract records:** enabling an endpoint records the signer, date, DPA reference, data-residency region and scope; changes require re-approval. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:668`; audit line 2110 | P0 | PARTIAL | [CP-19](#cp-19) | ID family | COMPLETE |
| `REQ-LLM-030` | `SR-LLM-018`: &#124; SR-LLM-018 &#124; **Same policy applies to embeddings, OCR, speech, reranking and telemetry** — not only chat models. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:669`; audit line 2111 | P0 | IMPLEMENTED-UNVERIFIED | [CP-19](#cp-19) | ID family | PROVE |
| `REQ-LLM-031` | `SR-LLM-019`: &#124; SR-LLM-019 &#124; **Local fallback:** on denial or outage, tasks fall back to local models or deterministic modes with a visible notice. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:670`; audit line 2112 | P0 | PARTIAL | [CP-19](#cp-19) | ID family | COMPLETE |
| `REQ-LLM-032` | `SR-LLM-020`: &#124; SR-LLM-020 &#124; **Region and sovereignty pinning:** endpoints and processing regions are constrained per tenant/jurisdiction. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:671`; audit line 2113 | P1 | PARTIAL | [CP-19](#cp-19) | ID family | COMPLETE |
| `REQ-LLM-033` | `SR-PRV-006`: &#124; SR-PRV-006 &#124; **Residency enforcement:** region pinning for storage, processing and model endpoints; cross-border transfer controls. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:853`; audit line 2161 | P0 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-LLM-034` | `TASK-AIE-012`: - **TASK-AIE-012**: Optimize prompt templates for top 5 most-used operations — reduce token usage, improve quality | `EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:62`; audit line 2255 | UNSTATED | MISSED | [CP-19](#cp-19) | area fallback | TRACE/BUILD |
| `REQ-LLM-035` | `TASK-LAI-004`: - **TASK-LAI-004**: Define AI model evaluation framework — benchmark suites, golden datasets, quality metrics | `EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:26`; audit line 2338 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-LLM-036` | `TASK-LAI-013`: - **TASK-LAI-013**: Define model drift monitoring strategy — when to retrain, what to measure | `EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:69`; audit line 2347 | UNSTATED | MISSED | [CP-19](#cp-19) | area fallback | TRACE/BUILD |
| `REQ-LLM-037` | `TASK-LIC-009`: - **TASK-LIC-009**: Analyze total cost of ownership (TCO) per deployment model — self-hosted vs cloud vs hybrid | `EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:50`; audit line 2390 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-LLM-038` | `TASK-LIC-010`: - **TASK-LIC-010**: Define token cost model — what does each token format save per 1M API calls? | `EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:54`; audit line 2391 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |

### A.12 LOC: 12 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-LOC-001` | `AC-16`: &#124; AC-16 &#124; Community detection clusters visible as hull overlays &#124; Gephi: desktop only &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1047`; audit line 114 | UNSTATED | MISSED | [CP-27](#cp-27) | subject triage | TRACE/BUILD |
| `REQ-LOC-002` | `GAP-DRIFT-004`: GAP-DRIFT-004: Detect relationship distribution shifts | `EOIP-engg-doc-pkg/gaps-requirements.md:516`; audit line 1283 | P1 | IMPLEMENTED-UNVERIFIED | [CP-27](#cp-27) | area fallback | PROVE |
| `REQ-LOC-003` | `GAP-FABRIC-006`: GAP-FABRIC-006: Offline degradation strategy | `EOIP-engg-doc-pkg/gaps-requirements.md:643`; audit line 1308 | P1 | IMPLEMENTED-UNVERIFIED | [CP-27](#cp-27) | subject triage | PROVE |
| `REQ-LOC-004` | `GAP-HG-006`: GAP-HG-006: standalone → distributed migration playbook | `EOIP-engg-doc-pkg/gaps-requirements.md:1079`; audit line 1350 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-LOC-005` | `GAP-LITE-001`: GAP-LITE-001: Support laptop/dev, single-server production and distributed production profiles | `EOIP-engg-doc-pkg/gaps-implementation.md:665`; audit line 1403 | P2 | IMPLEMENTED-UNVERIFIED | [CP-27](#cp-27) | ID family | PROVE |
| `REQ-LOC-006` | `GAP-OFFLINE-001`: GAP-OFFLINE-001: Zero mandatory Internet/cloud dependency | `EOIP-engg-doc-pkg/gaps-implementation.md:172`; audit line 1425 | P0 | IMPLEMENTED-UNVERIFIED | [CP-27](#cp-27) | ID family | PROVE |
| `REQ-LOC-007` | `INFRA-001.3`: - [x] `INFRA-001.3` Distributed invalidation | `eoip-phase4-2-requirements.md:812`; audit line 1571 | UNSTATED | MISSED | [CP-03](#cp-03) | engine family | TRACE/BUILD |
| `REQ-LOC-008` | `INFRA-005`: Distributed Scheduling | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:619`; audit line 1592 | P2 | IMPLEMENTED-UNVERIFIED | [CP-10](#cp-10) | engine family | PROVE |
| `REQ-LOC-009` | `INFRA-005.2`: - [x] `INFRA-005.2` Distributed task locking | `eoip-phase4-2-requirements.md:905`; audit line 1594 | UNSTATED | MISSED | [CP-10](#cp-10) | engine family | TRACE/BUILD |
| `REQ-LOC-010` | `SDLC-024`: ###### SDLC-024: Air-gapped installation bundle and offline update channel | `eoip-phase4-2-requirements.md:1829`; audit line 1899 | UNSTATED | MISSED | [CP-27](#cp-27) | engine family | TRACE/BUILD |
| `REQ-LOC-011` | `SR-CON-001`: &#124; SR-CON-001 &#124; **Self-contained:** the default distribution MUST run with zero external network dependencies (no SaaS, no cloud API, no phone-home, no CDN assets, no package fetch at runtime). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:98`; audit line 2005 | P0 | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-LOC-012` | `SR-DEP-001`: &#124; SR-DEP-001 &#124; **Docker Compose** distribution for DP-0 with healthy-start verification and one-command clean-reset demo including backup/restore (inherited `MVP-FR-028`). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:922`; audit line 2019 | P0 | MISSED | [CP-31](#cp-31) | ID family | TRACE/BUILD |

### A.13 NFR: 919 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-NFR-001` | `AC-08`: &#124; AC-08 &#124; All existing EOIP lenses continue unchanged &#124; N/A &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1039`; audit line 106 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-002` | `AC-11`: &#124; AC-11 &#124; Minimap, fisheye, semantic zoom all function &#124; No competitor bundles all three &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1042`; audit line 109 | UNSTATED | MISSED | [CP-23](#cp-23) | subject triage | TRACE/BUILD |
| `REQ-NFR-003` | `AC-12`: &#124; AC-12 &#124; Full keyboard navigation without mouse &#124; No competitor achieves full keyboard nav &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1043`; audit line 110 | UNSTATED | MISSED | [CP-24](#cp-24) | subject triage | TRACE/BUILD |
| `REQ-NFR-004` | `AC-13`: &#124; AC-13 &#124; 166+ existing tests continue to pass &#124; N/A &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1044`; audit line 111 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-005` | `AC-21`: &#124; AC-21 &#124; Node group collapsing works with domain/type/community/custom grouping &#124; yFiles (€9.2K), KeyLines (commercial), Linkurious (commercial) — KGR does it free &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1052`; audit line 119 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-006` | `AC-24`: &#124; AC-24 &#124; Dead code / orphaned entity detection with visual indicators &#124; code2flow (4 langs, CLI only) — KGR covers all entity types &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1055`; audit line 122 | UNSTATED | MISSED | [CP-29](#cp-29) | subject triage | TRACE/BUILD |
| `REQ-NFR-007` | `AC-29`: &#124; AC-29 &#124; Geo-mode positions entities on map when location metadata available &#124; Linkurious, Ogma (commercial) — KGR does it free &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1060`; audit line 127 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-008` | `AC-30`: &#124; AC-30 &#124; Semantic zoom shows 3 levels (cluster/entity/detail) with smooth transitions &#124; No free competitor has this &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1061`; audit line 128 | UNSTATED | MISSED | [CP-23](#cp-23) | subject triage | TRACE/BUILD |
| `REQ-NFR-009` | `AC-31`: &#124; AC-31 &#124; Fisheye distortion provides 2x magnification at cursor with gradual falloff &#124; yFiles (€9.2K) — KGR does it free &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1062`; audit line 129 | UNSTATED | MISSED | [CP-23](#cp-23) | subject triage | TRACE/BUILD |
| `REQ-NFR-010` | `AC-33`: &#124; AC-33 &#124; Color-blind safe palette with 3 modes (deuteranopia/tritanopia/high-contrast) &#124; No competitor has 3 palette modes &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1064`; audit line 131 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-011` | `AI-001`: Advanced XAI Engine | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:390`; audit line 255 | P1 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | engine family | PROVE |
| `REQ-NFR-012` | `AI-001.1`: - [x] `AI-001.1` Feature importance analysis | `eoip-phase4-2-requirements.md:650`; audit line 256 | UNSTATED | MISSED | [CP-21](#cp-21) | engine family | TRACE/BUILD |
| `REQ-NFR-013` | `AI-001.3`: - [x] `AI-001.3` Confidence calibration | `eoip-phase4-2-requirements.md:652`; audit line 258 | UNSTATED | MISSED | [CP-21](#cp-21) | engine family | TRACE/BUILD |
| `REQ-NFR-014` | `AI-001.4`: - [x] `AI-001.4` Human-readable explanation rendering | `eoip-phase4-2-requirements.md:653`; audit line 259 | UNSTATED | MISSED | [CP-21](#cp-21) | engine family | TRACE/BUILD |
| `REQ-NFR-015` | `AI-001.5`: - [x] `AI-001.5` Thread-safe singleton | `eoip-phase4-2-requirements.md:654`; audit line 260 | UNSTATED | MISSED | [CP-21](#cp-21) | engine family | TRACE/BUILD |
| `REQ-NFR-016` | `AI-001.6`: - [x] `AI-001.6` Wired into brain_os.py and platform_router.py | `eoip-phase4-2-requirements.md:655`; audit line 261 | UNSTATED | MISSED | [CP-21](#cp-21) | engine family | TRACE/BUILD |
| `REQ-NFR-017` | `AI-001.7`: - [x] `AI-001.7` Unit tests | `eoip-phase4-2-requirements.md:656`; audit line 262 | UNSTATED | MISSED | [CP-21](#cp-21) | engine family | TRACE/BUILD |
| `REQ-NFR-018` | `AI-002`: Deep NLP Pipeline | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:414`; audit line 263 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | engine family | PROVE |
| `REQ-NFR-019` | `AI-002.1`: - [x] `AI-002.1` Deep NER with configurable backends | `eoip-phase4-2-requirements.md:675`; audit line 264 | UNSTATED | MISSED | [CP-15](#cp-15) | engine family | TRACE/BUILD |
| `REQ-NFR-020` | `AI-002.3`: - [x] `AI-002.3` Topic modeling | `eoip-phase4-2-requirements.md:677`; audit line 266 | UNSTATED | MISSED | [CP-15](#cp-15) | engine family | TRACE/BUILD |
| `REQ-NFR-021` | `AI-002.4`: - [x] `AI-002.4` Language detection | `eoip-phase4-2-requirements.md:678`; audit line 267 | UNSTATED | MISSED | [CP-15](#cp-15) | engine family | TRACE/BUILD |
| `REQ-NFR-022` | `AI-002.5`: - [x] `AI-002.5` Unit tests | `eoip-phase4-2-requirements.md:679`; audit line 268 | UNSTATED | MISSED | [CP-15](#cp-15) | engine family | TRACE/BUILD |
| `REQ-NFR-023` | `AI-003.2`: - [x] `AI-003.2` Triple generation with confidence scores | `eoip-phase4-2-requirements.md:699`; audit line 271 | UNSTATED | MISSED | [CP-17](#cp-17) | engine family | TRACE/BUILD |
| `REQ-NFR-024` | `AI-003.4`: - [x] `AI-003.4` Deduplication | `eoip-phase4-2-requirements.md:701`; audit line 273 | UNSTATED | MISSED | [CP-17](#cp-17) | engine family | TRACE/BUILD |
| `REQ-NFR-025` | `AI-003.5`: - [x] `AI-003.5` Unit tests | `eoip-phase4-2-requirements.md:702`; audit line 274 | UNSTATED | MISSED | [CP-17](#cp-17) | engine family | TRACE/BUILD |
| `REQ-NFR-026` | `AI-004.1`: - [x] `AI-004.1` A/B experiment creation and traffic splitting | `eoip-phase4-2-requirements.md:719`; audit line 276 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-NFR-027` | `AI-004.2`: - [x] `AI-004.2` Statistical significance testing | `eoip-phase4-2-requirements.md:720`; audit line 277 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-NFR-028` | `AI-004.5`: - [x] `AI-004.5` Unit tests | `eoip-phase4-2-requirements.md:723`; audit line 280 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-NFR-029` | `AI-005`: MLOps Experiment Tracking | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:475`; audit line 281 | P2 | IMPLEMENTED-UNVERIFIED | [CP-19](#cp-19) | engine family | PROVE |
| `REQ-NFR-030` | `AI-005.1`: - [x] `AI-005.1` Experiment creation and run tracking | `eoip-phase4-2-requirements.md:741`; audit line 282 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-NFR-031` | `AI-005.3`: - [x] `AI-005.3` Artifact storage | `eoip-phase4-2-requirements.md:743`; audit line 284 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-NFR-032` | `AI-005.4`: - [x] `AI-005.4` Cross-run comparison | `eoip-phase4-2-requirements.md:744`; audit line 285 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-NFR-033` | `AI-005.5`: - [x] `AI-005.5` Unit tests | `eoip-phase4-2-requirements.md:745`; audit line 286 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-NFR-034` | `AI-006.2`: - [x] `AI-006.2` Drift detection | `eoip-phase4-2-requirements.md:764`; audit line 289 | UNSTATED | MISSED | [CP-20](#cp-20) | engine family | TRACE/BUILD |
| `REQ-NFR-035` | `AI-006.3`: - [x] `AI-006.3` Multi-modal fusion | `eoip-phase4-2-requirements.md:765`; audit line 290 | UNSTATED | MISSED | [CP-20](#cp-20) | engine family | TRACE/BUILD |
| `REQ-NFR-036` | `AI-006.4`: - [x] `AI-006.4` Dimension reduction | `eoip-phase4-2-requirements.md:766`; audit line 291 | UNSTATED | MISSED | [CP-20](#cp-20) | engine family | TRACE/BUILD |
| `REQ-NFR-037` | `AI-006.5`: - [x] `AI-006.5` Unit tests | `eoip-phase4-2-requirements.md:767`; audit line 292 | UNSTATED | MISSED | [CP-20](#cp-20) | engine family | TRACE/BUILD |
| `REQ-NFR-038` | `AI-007`: Probabilistic Reasoning Integration | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:515`; audit line 293 | P3 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | engine family | PROVE |
| `REQ-NFR-039` | `AI-007.2`: - [x] `AI-007.2` Uncertainty propagation | `eoip-phase4-2-requirements.md:785`; audit line 295 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-NFR-040` | `AI-007.4`: - [x] `AI-007.4` Unit tests | `eoip-phase4-2-requirements.md:787`; audit line 297 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-NFR-041` | `AI-ACT-ART-13`: &#124; 3 &#124; `compliance_twin.py` &#124; `_check_control` method: missing keys cause FAIL (not default True). Expanded to 6 frameworks (added ISO 42001, HIPAA, GDPR). Added controls EU-AI-ACT-ART-13, SOC2-CC7.2, SOC2-CC8.1, GOV-G... | `docs/audit-2026-10-06/assessed-gap-report.md:750`; audit line 298 | UNSTATED | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-042` | `AIDLC-002.1`: - [ ] `AIDLC-002.1` Blue/green index switch | `eoip-phase4-2-requirements.md:2070`; audit line 305 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-NFR-043` | `AIDLC-002.2`: - [ ] `AIDLC-002.2` Backfill resumable | `eoip-phase4-2-requirements.md:2071`; audit line 306 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-NFR-044` | `AIDLC-002.4`: - [ ] `AIDLC-002.4` Rollback tested | `eoip-phase4-2-requirements.md:2073`; audit line 308 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-NFR-045` | `AIDLC-004.2`: - [ ] `AIDLC-004.2` Deterministic scorers implemented | `eoip-phase4-2-requirements.md:2166`; audit line 316 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-NFR-046` | `AIDLC-005.1`: - [ ] `AIDLC-005.1` Recorder and replayer | `eoip-phase4-2-requirements.md:2183`; audit line 320 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-NFR-047` | `AIDLC-005.4`: - [ ] `AIDLC-005.4` Recordings follow retention and erasure policy | `eoip-phase4-2-requirements.md:2186`; audit line 323 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-NFR-048` | `AIDLC-006.1`: - [ ] `AIDLC-006.1` Labelled sets and confusion matrices | `eoip-phase4-2-requirements.md:2200`; audit line 325 | UNSTATED | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-NFR-049` | `AIDLC-006.2`: - [ ] `AIDLC-006.2` Shadow mode in both engines | `eoip-phase4-2-requirements.md:2201`; audit line 326 | UNSTATED | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-NFR-050` | `AIDLC-006.3`: - [ ] `AIDLC-006.3` Promotion threshold documented | `eoip-phase4-2-requirements.md:2202`; audit line 327 | UNSTATED | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-NFR-051` | `AIDLC-006.4`: - [ ] `AIDLC-006.4` Drift alerts after promotion | `eoip-phase4-2-requirements.md:2203`; audit line 328 | UNSTATED | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-NFR-052` | `AIDLC-007.2`: - [ ] `AIDLC-007.2` Promotion blocked unless evaluation passes | `eoip-phase4-2-requirements.md:2110`; audit line 331 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-053` | `AIDLC-007.3`: - [ ] `AIDLC-007.3` Rollback tested | `eoip-phase4-2-requirements.md:2111`; audit line 332 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-054` | `AIDLC-008.4`: - [ ] `AIDLC-008.4` Usage metering feeds CORE-006 and MS-27 | `eoip-phase4-2-requirements.md:2130`; audit line 338 | UNSTATED | MISSED | [CP-33](#cp-33) | subject triage | TRACE/BUILD |
| `REQ-NFR-055` | `AIDLC-009.1`: - [ ] `AIDLC-009.1` Feedback capture end to end | `eoip-phase4-2-requirements.md:2314`; audit line 340 | UNSTATED | MISSED | [CP-10](#cp-10) | subject triage | TRACE/BUILD |
| `REQ-NFR-056` | `AIDLC-009.2`: - [ ] `AIDLC-009.2` Online sampled evaluation | `eoip-phase4-2-requirements.md:2315`; audit line 341 | UNSTATED | MISSED | [CP-10](#cp-10) | subject triage | TRACE/BUILD |
| `REQ-NFR-057` | `AIDLC-009.4`: - [ ] `AIDLC-009.4` Feedback converts to eval cases | `eoip-phase4-2-requirements.md:2317`; audit line 343 | UNSTATED | MISSED | [CP-10](#cp-10) | subject triage | TRACE/BUILD |
| `REQ-NFR-058` | `AIDLC-010.2`: - [ ] `AIDLC-010.2` Evaluation gate blocks regressions | `eoip-phase4-2-requirements.md:2145`; audit line 346 | UNSTATED | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-NFR-059` | `AIDLC-010.4`: - [ ] `AIDLC-010.4` Rollback tested | `eoip-phase4-2-requirements.md:2147`; audit line 348 | UNSTATED | MISSED | [CP-34](#cp-34) | subject triage | TRACE/BUILD |
| `REQ-NFR-060` | `AIDLC-011.1`: - [ ] `AIDLC-011.1` Attack corpus and runner | `eoip-phase4-2-requirements.md:2220`; audit line 350 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-NFR-061` | `AIDLC-011.2`: - [ ] `AIDLC-011.2` Mapped to OWASP categories | `eoip-phase4-2-requirements.md:2221`; audit line 351 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-NFR-062` | `AIDLC-011.4`: - [ ] `AIDLC-011.4` Failing attack creates a tracked finding | `eoip-phase4-2-requirements.md:2223`; audit line 353 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-NFR-063` | `AIDLC-012.1`: - [ ] `AIDLC-012.1` Sandbox runtime with enforced limits | `eoip-phase4-2-requirements.md:2239`; audit line 355 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-064` | `AIDLC-012.2`: - [ ] `AIDLC-012.2` Escape and exhaustion tests | `eoip-phase4-2-requirements.md:2240`; audit line 356 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-065` | `AIDLC-012.4`: - [ ] `AIDLC-012.4` Plugin loader uses the same runtime | `eoip-phase4-2-requirements.md:2242`; audit line 358 | UNSTATED | MISSED | [CP-29](#cp-29) | subject triage | TRACE/BUILD |
| `REQ-NFR-066` | `AIDLC-013.3`: - [ ] `AIDLC-013.3` SCIM create/update/deactivate tested | `eoip-phase4-2-requirements.md:2259`; audit line 362 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-NFR-067` | `AIDLC-013.4`: - [ ] `AIDLC-013.4` Revocation takes effect immediately | `eoip-phase4-2-requirements.md:2260`; audit line 363 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-NFR-068` | `AIDLC-014`: ###### AIDLC-014: AI governance pack | `eoip-phase4-2-requirements.md:2262`; audit line 364 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-069` | `AIDLC-015.2`: - [ ] `AIDLC-015.2` Confidence and abstain states | `eoip-phase4-2-requirements.md:2335`; audit line 371 | UNSTATED | MISSED | [CP-25](#cp-25) | subject triage | TRACE/BUILD |
| `REQ-NFR-070` | `AIDLC-015.3`: - [ ] `AIDLC-015.3` Why-this-answer panel | `eoip-phase4-2-requirements.md:2336`; audit line 372 | UNSTATED | MISSED | [CP-25](#cp-25) | subject triage | TRACE/BUILD |
| `REQ-NFR-071` | `AIDLC-015.4`: - [ ] `AIDLC-015.4` Accessibility checks pass | `eoip-phase4-2-requirements.md:2337`; audit line 373 | UNSTATED | MISSED | [CP-25](#cp-25) | subject triage | TRACE/BUILD |
| `REQ-NFR-072` | `AIDLC-016.1`: - [ ] `AIDLC-016.1` Catalog covers all loops | `eoip-phase4-2-requirements.md:2294`; audit line 375 | UNSTATED | MISSED | [CP-10](#cp-10) | subject triage | TRACE/BUILD |
| `REQ-NFR-073` | `AIDLC-016.4`: - [ ] `AIDLC-016.4` Linked from governance pack | `eoip-phase4-2-requirements.md:2297`; audit line 378 | UNSTATED | MISSED | [CP-10](#cp-10) | subject triage | TRACE/BUILD |
| `REQ-NFR-074` | `CG-DOC-01`: Point the live docs at this backlog | `KGF-MASTER-BACKLOG.md:238`; audit line 386 | P0 | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-075` | `CG-GAP-001`: Mount the loops catalog route (PIC-002) | `EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:62`; audit line 387 | P0 | PARTIAL | [CP-37](#cp-37) | subject triage | COMPLETE |
| `REQ-NFR-076` | `CG-GAP-005`: Markdown link-check pass (non-historical docs first) | `EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:66`; audit line 391 | P1 | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-077` | `CG-GAP-006`: Decide and close the apps/console question | `EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:67`; audit line 392 | P1 | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-078` | `CG-GAP-008`: Live and external acceptance receipts (delivered in Phase 8) | `EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:69`; audit line 394 | P1 | BLOCKED | [CP-36](#cp-36) | explicit | UNBLOCK |
| `REQ-NFR-079` | `COMPLY-001.4`: - [x] `COMPLY-001.4` GDPR, SOX, HIPAA rule templates | `eoip-phase4-2-requirements.md:1169`; audit line 400 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-080` | `COMPLY-001.5`: - [x] `COMPLY-001.5` Unit tests | `eoip-phase4-2-requirements.md:1170`; audit line 401 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-081` | `COMPLY-002.2`: - [x] `COMPLY-002.2` k-anonymity implementation | `eoip-phase4-2-requirements.md:1191`; audit line 404 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-082` | `COMPLY-002.4`: - [x] `COMPLY-002.4` Scheduled scanning | `eoip-phase4-2-requirements.md:1193`; audit line 406 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-083` | `COMPLY-002.5`: - [x] `COMPLY-002.5` Unit tests | `eoip-phase4-2-requirements.md:1194`; audit line 407 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-084` | `COMPLY-003.1`: - [x] `COMPLY-003.1` Per-framework compliance scores | `eoip-phase4-2-requirements.md:1212`; audit line 409 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-085` | `COMPLY-003.3`: - [x] `COMPLY-003.3` Attestation tracking | `eoip-phase4-2-requirements.md:1214`; audit line 411 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-086` | `CORE-001`: Token Format Serialization Engines | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:20`; audit line 416 | P0 | IMPLEMENTED-UNVERIFIED | [CP-19](#cp-19) | engine family | PROVE |
| `REQ-NFR-087` | `CORE-001.1`: - [x] `CORE-001.1` All 7 format strategies implemented with serialize/deserialize | `eoip-phase4-2-requirements.md:235`; audit line 417 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-NFR-088` | `CORE-001.2`: - [x] `CORE-001.2` Auto-format selection based on payload characteristics | `eoip-phase4-2-requirements.md:236`; audit line 418 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-NFR-089` | `CORE-001.3`: - [x] `CORE-001.3` Round-trip fidelity: `deserialize(serialize(obj)) == obj` for all supported types | `eoip-phase4-2-requirements.md:237`; audit line 419 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-NFR-090` | `CORE-001.4`: - [x] `CORE-001.4` Token reduction benchmarks showing 30%+ savings vs JSON | `eoip-phase4-2-requirements.md:238`; audit line 420 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-NFR-091` | `CORE-001.5`: - [x] `CORE-001.5` Thread-safe singleton `get_token_format_engine()` | `eoip-phase4-2-requirements.md:239`; audit line 421 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-NFR-092` | `CORE-002`: Verification & Guardrail Engineering | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:45`; audit line 424 | P0 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | engine family | PROVE |
| `REQ-NFR-093` | `CORE-002.2`: - [x] `CORE-002.2` 7+ built-in verification rules | `eoip-phase4-2-requirements.md:266`; audit line 426 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-NFR-094` | `CORE-002.3`: - [x] `CORE-002.3` DynamicGuardrailInjector with real-time intent checking | `eoip-phase4-2-requirements.md:267`; audit line 427 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-NFR-095` | `CORE-002.4`: - [x] `CORE-002.4` Integration hooks at loop boundaries | `eoip-phase4-2-requirements.md:268`; audit line 428 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-NFR-096` | `CORE-002.6`: - [x] `CORE-002.6` Thread-safe singleton `get_verification_engine()` | `eoip-phase4-2-requirements.md:270`; audit line 430 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-NFR-097` | `CORE-002.7`: - [x] `CORE-002.7` Wired into brain_os.py and platform_router.py | `eoip-phase4-2-requirements.md:271`; audit line 431 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-NFR-098` | `CORE-002.8`: - [x] `CORE-002.8` Unit tests for each rule type and composition | `eoip-phase4-2-requirements.md:272`; audit line 432 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-NFR-099` | `CORE-003`: Intent Router Engineering | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:72`; audit line 433 | P0 | IMPLEMENTED-UNVERIFIED | [CP-19](#cp-19) | engine family | PROVE |
| `REQ-NFR-100` | `CORE-003.1`: - [x] `CORE-003.1` IntentClassifier with 8+ intent categories | `eoip-phase4-2-requirements.md:296`; audit line 434 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-NFR-101` | `CORE-003.4`: - [x] `CORE-003.4` Feedback loop for classifier accuracy tracking | `eoip-phase4-2-requirements.md:299`; audit line 437 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-NFR-102` | `CORE-003.5`: - [x] `CORE-003.5` Integration with cost_optimization engine | `eoip-phase4-2-requirements.md:300`; audit line 438 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-NFR-103` | `CORE-003.6`: - [x] `CORE-003.6` Thread-safe singleton `get_router_engine()` | `eoip-phase4-2-requirements.md:301`; audit line 439 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-NFR-104` | `CORE-003.7`: - [x] `CORE-003.7` Wired into brain_os.py and platform_router.py | `eoip-phase4-2-requirements.md:302`; audit line 440 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-NFR-105` | `CORE-004.3`: - [x] `CORE-004.3` Layer projection and merging | `eoip-phase4-2-requirements.md:329`; audit line 445 | UNSTATED | MISSED | [CP-13](#cp-13) | engine family | TRACE/BUILD |
| `REQ-NFR-106` | `CORE-004.5`: - [x] `CORE-004.5` Constraint propagation across layers | `eoip-phase4-2-requirements.md:331`; audit line 447 | UNSTATED | MISSED | [CP-13](#cp-13) | engine family | TRACE/BUILD |
| `REQ-NFR-107` | `CORE-004.7`: - [x] `CORE-004.7` Wired into brain_os.py and platform_router.py | `eoip-phase4-2-requirements.md:333`; audit line 449 | UNSTATED | MISSED | [CP-13](#cp-13) | engine family | TRACE/BUILD |
| `REQ-NFR-108` | `CORE-004.8`: - [x] `CORE-004.8` Unit tests for cross-layer operations | `eoip-phase4-2-requirements.md:334`; audit line 450 | UNSTATED | MISSED | [CP-13](#cp-13) | engine family | TRACE/BUILD |
| `REQ-NFR-109` | `CORE-005`: Loop-over-Loop Engineering | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:126`; audit line 451 | P1 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | engine family | PROVE |
| `REQ-NFR-110` | `CORE-005.1`: - [x] `CORE-005.1` SupervisoryLoop wrapping and monitoring inner loops | `eoip-phase4-2-requirements.md:352`; audit line 452 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-NFR-111` | `CORE-005.3`: - [x] `CORE-005.3` Dynamic strategy switching | `eoip-phase4-2-requirements.md:354`; audit line 454 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-NFR-112` | `CORE-005.4`: - [x] `CORE-005.4` Circuit-breaker integration | `eoip-phase4-2-requirements.md:355`; audit line 455 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-NFR-113` | `CORE-005.5`: - [x] `CORE-005.5` Unit tests for composition patterns | `eoip-phase4-2-requirements.md:356`; audit line 456 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-NFR-114` | `CORE-006`: Token Budget Engineering | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:146`; audit line 457 | P1 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | engine family | PROVE |
| `REQ-NFR-115` | `CORE-006.1`: - [x] `CORE-006.1` TokenBudget with 4 allocation strategies | `eoip-phase4-2-requirements.md:377`; audit line 458 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-NFR-116` | `CORE-006.2`: - [x] `CORE-006.2` Real-time consumption tracking per pipeline stage | `eoip-phase4-2-requirements.md:378`; audit line 459 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-NFR-117` | `CORE-006.3`: - [x] `CORE-006.3` Dynamic reallocation when stages under/over-consume | `eoip-phase4-2-requirements.md:379`; audit line 460 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-NFR-118` | `CORE-006.4`: - [x] `CORE-006.4` Context compression triggers on budget exceed | `eoip-phase4-2-requirements.md:380`; audit line 461 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-NFR-119` | `CORE-006.5`: - [x] `CORE-006.5` Integration with intelligence_eng and cost_optimization | `eoip-phase4-2-requirements.md:381`; audit line 462 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-NFR-120` | `CORE-006.6`: - [x] `CORE-006.6` Thread-safe singleton | `eoip-phase4-2-requirements.md:382`; audit line 463 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-NFR-121` | `CORE-006.7`: - [x] `CORE-006.7` Wired into brain_os.py and platform_router.py | `eoip-phase4-2-requirements.md:383`; audit line 464 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-NFR-122` | `CORE-006.8`: - [x] `CORE-006.8` Unit tests | `eoip-phase4-2-requirements.md:384`; audit line 465 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-NFR-123` | `FR-01`: - **Core Functional Requirements:** 67 requirements (`FR-01` through `FR-67`) — *100% Implemented & Verified* | `EOIP-engg-doc-pkg/KGR-g-requirements.md:70`; audit line 476 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-124` | `FR-67`: - **Core Functional Requirements:** 67 requirements (`FR-01` through `FR-67`) — *100% Implemented & Verified* | `EOIP-engg-doc-pkg/KGR-g-requirements.md:70`; audit line 503 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-125` | `FR-CODE-002`: Python and TypeScript MVP parsing | `EOIP-engg-doc-pkg/02-scope-and-objectives.md:24`; audit line 512 | P0 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-126` | `FR-CODE-003`: Commit-to-symbol linking | `EOIP-engg-doc-pkg/03-functional-requirements.md:345`; audit line 513 | P0 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-127` | `FR-CODE-004`: Call/import/dependency edges | `EOIP-engg-doc-pkg/03-functional-requirements.md:355`; audit line 514 | P0 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-128` | `FR-ID-001`: Deterministic identity resolution | `EOIP-engg-doc-pkg/03-functional-requirements.md:295`; audit line 536 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-NFR-129` | `FR-ID-002`: Ambiguous identity candidates | `EOIP-engg-doc-pkg/03-functional-requirements.md:305`; audit line 537 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-NFR-130` | `FR-KGR-002`: ### FR-KGR-002: Node Intelligence (8-Tab Inspector) | `EOIP-engg-doc-pkg/KGR-requirements.md:171`; audit line 544 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-NFR-131` | `FR-KGR-005`: ### FR-KGR-005: Data Feed Integration | `EOIP-engg-doc-pkg/KGR-requirements.md:306`; audit line 547 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-NFR-132` | `FR-KGR-007`: ### FR-KGR-007: Export & Sharing (11+ Formats) | `EOIP-engg-doc-pkg/KGR-requirements.md:354`; audit line 549 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-NFR-133` | `FR-KGR-009`: ### FR-KGR-009: AI-Assisted Exploration (Future-Ready) | `EOIP-engg-doc-pkg/KGR-requirements.md:384`; audit line 551 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-NFR-134` | `FR-KGR-011`: Implements FR-KGR-011. Matches Linkurious and Ogma (both commercial). | `EOIP-engg-doc-pkg/KGR-implementation-plan.md:1495`; audit line 553 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-NFR-135` | `FR-KGR-014`: Implements FR-KGR-014. Matches code2flow's orphaned function detection. Extended to cover all entity types. | `EOIP-engg-doc-pkg/KGR-implementation-plan.md:1434`; audit line 556 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-NFR-136` | `FR-KGR-015`: Implements FR-KGR-015. | `EOIP-engg-doc-pkg/KGR-implementation-plan.md:1464`; audit line 557 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-NFR-137` | `FR-KGR-017`: ### FR-KGR-017: Self-Contained Interactive HTML Export | `EOIP-engg-doc-pkg/KGR-requirements.md:492`; audit line 559 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-NFR-138` | `FR-KGR-019`: ### FR-KGR-019: Hub Exclusion Filter | `EOIP-engg-doc-pkg/KGR-requirements.md:519`; audit line 561 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-NFR-139` | `FR-KGR-020`: ### FR-KGR-020: Surprising/Unexpected Connection Detection | `EOIP-engg-doc-pkg/KGR-requirements.md:530`; audit line 562 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-NFR-140` | `FR-KGR-021`: ### FR-KGR-021: Rule-Based Conditional Visual Styling | `EOIP-engg-doc-pkg/KGR-requirements.md:542`; audit line 563 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-NFR-141` | `FR-KGR-025`: ### FR-KGR-025: Investigation Playbooks | `EOIP-engg-doc-pkg/KGR-requirements.md:589`; audit line 567 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-NFR-142` | `FR-KGR-029`: ### FR-KGR-029: Engineering Disciplines (8 Patterns) | `EOIP-engg-doc-pkg/KGR-requirements.md:666`; audit line 571 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-NFR-143` | `FR-MEM-001`: Scoped memory records | `EOIP-engg-doc-pkg/03-functional-requirements.md:595`; audit line 575 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | subject triage | PROVE |
| `REQ-NFR-144` | `FR-ONTO-002`: Relationship semantics | `EOIP-engg-doc-pkg/03-functional-requirements.md:265`; audit line 577 | P0 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | ID family | PROVE |
| `REQ-NFR-145` | `FR-VALID-002`: Validation gates | `EOIP-engg-doc-pkg/03-functional-requirements.md:465`; audit line 600 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-NFR-146` | `FR-VSCODE-001`: VS Code context extension | `EOIP-engg-doc-pkg/03-functional-requirements.md:665`; audit line 602 | P0 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-NFR-147` | `FRD-001`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 604 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-148` | `FRD-001-008`: &#124; Requirement IDs seen &#124; FRD-001-008, FRD-100, FRD-200, FRD-300, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2078`; audit line 605 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-149` | `FRD-002`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 606 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-150` | `FRD-003`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 607 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-151` | `FRD-004`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 608 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-152` | `FRD-005`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 609 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-153` | `FRD-006`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 610 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-154` | `FRD-007`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 611 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-155` | `FRD-100`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 612 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-156` | `FRD-101`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 613 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-157` | `FRD-102`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 614 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-158` | `FRD-103`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 615 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-159` | `FRD-200`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 616 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-160` | `FRD-201`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 617 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-161` | `FRD-202`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 618 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-162` | `FRD-300`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 619 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-163` | `FRD-301`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 620 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-164` | `FRD-302`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 621 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-165` | `FRD-321`: &#124; Requirement IDs seen &#124; FRD-001, FRD-002, FRD-003, FRD-004, FRD-005, FRD-006, FRD-007, FRD-100, FRD-101, FRD-102, FRD-103, FRD-200, FRD-201, FRD-202, FRD-300, FRD-301, FRD-302, FRD-321 &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054`; audit line 622 | UNSTATED | MISSED | [CP-00](#cp-00) | source recovery | TRACE/BUILD |
| `REQ-NFR-166` | `G2-ARCH-001`: G2-ARCH-001 — One acquisition contract | `EOIP-engg-doc-pkg/gaps2-implementation.md:57`; audit line 640 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-167` | `G2-ARCH-003`: G2-ARCH-003 — Deterministic first | `EOIP-engg-doc-pkg/gaps2-requirements.md:68`; audit line 642 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-168` | `G2-ARCH-008`: G2-ARCH-008 — Current and historical views | `EOIP-engg-doc-pkg/gaps2-requirements.md:88`; audit line 647 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-169` | `G2-ARCH-009`: G2-ARCH-009 — One semantic identity system | `EOIP-engg-doc-pkg/gaps2-requirements.md:92`; audit line 648 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-170` | `G2-ARCH-012`: G2-ARCH-012 — Incremental by default after baseline | `EOIP-engg-doc-pkg/gaps2-requirements.md:104`; audit line 651 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-171` | `G2-ARCH-013`: G2-ARCH-013 — Replayability | `EOIP-engg-doc-pkg/gaps2-requirements.md:108`; audit line 652 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-172` | `G2-ARCH-015`: G2-ARCH-015 — Progressive complexity | `EOIP-engg-doc-pkg/gaps2-requirements.md:116`; audit line 654 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-173` | `G2-ARCHC-001`: G2-ARCHC-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:821`; audit line 655 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-174` | `G2-ARCHC-002`: G2-ARCHC-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1113`; audit line 656 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-175` | `G2-ARCHC-003`: G2-ARCHC-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1116`; audit line 657 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-176` | `G2-ARCHC-004`: G2-ARCHC-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1123`; audit line 658 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-177` | `G2-ARCHC-005`: G2-ARCHC-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1126`; audit line 659 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-178` | `G2-ARCHC-006`: G2-ARCHC-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1129`; audit line 660 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-179` | `G2-ARCHC-007`: G2-ARCHC-007 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1132`; audit line 661 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-180` | `G2-ARCHC-008`: G2-ARCHC-008 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1135`; audit line 662 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-181` | `G2-ARCHC-009`: G2-ARCHC-009 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1138`; audit line 663 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-182` | `G2-CAP-001`: G2-CAP-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:944`; audit line 664 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-183` | `G2-CAP-002`: G2-CAP-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1289`; audit line 665 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-184` | `G2-CAP-003`: G2-CAP-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1292`; audit line 666 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-185` | `G2-CAP-004`: G2-CAP-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1295`; audit line 667 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-186` | `G2-CAP-005`: G2-CAP-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1298`; audit line 668 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-187` | `G2-CAP-006`: G2-CAP-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1308`; audit line 669 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-188` | `G2-CAUSE-001`: G2-CAUSE-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1017`; audit line 670 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-189` | `G2-CAUSE-002`: G2-CAUSE-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1150`; audit line 671 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-190` | `G2-CAUSE-003`: G2-CAUSE-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1157`; audit line 672 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-191` | `G2-CAUSE-004`: G2-CAUSE-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1160`; audit line 673 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-192` | `G2-CAUSE-005`: G2-CAUSE-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1168`; audit line 674 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-193` | `G2-CAUSE-006`: G2-CAUSE-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1171`; audit line 675 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-194` | `G2-EKAF-005`: G2-EKAF-005 — Incremental sync | `EOIP-engg-doc-pkg/gaps2-requirements.md:207`; audit line 680 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-195` | `G2-EKAF-007`: G2-EKAF-007 — Poll fallback | `EOIP-engg-doc-pkg/gaps2-requirements.md:218`; audit line 682 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-196` | `G2-EKAF-009`: G2-EKAF-009 — Idempotency | `EOIP-engg-doc-pkg/gaps2-requirements.md:224`; audit line 684 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-197` | `G2-EKAF-010`: G2-EKAF-010 — Ordering tolerance | `EOIP-engg-doc-pkg/gaps2-requirements.md:227`; audit line 685 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-198` | `G2-EKAF-013`: G2-EKAF-013 — Replay | `EOIP-engg-doc-pkg/gaps2-requirements.md:241`; audit line 688 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-199` | `G2-EKAF-014`: G2-EKAF-014 — Dead-letter handling | `EOIP-engg-doc-pkg/gaps2-requirements.md:250`; audit line 689 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-200` | `G2-EKAF-015`: G2-EKAF-015 — Dry run | `EOIP-engg-doc-pkg/gaps2-requirements.md:259`; audit line 690 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-201` | `G2-EKAF-023`: G2-EKAF-023 — Permission-aware metadata | `EOIP-engg-doc-pkg/gaps2-requirements.md:304`; audit line 698 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-202` | `G2-EKAF-024`: G2-EKAF-024 — Content fingerprinting | `EOIP-engg-doc-pkg/gaps2-requirements.md:307`; audit line 699 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-203` | `G2-EKAF-025`: G2-EKAF-025 — Attachment handling | `EOIP-engg-doc-pkg/gaps2-requirements.md:310`; audit line 700 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-204` | `G2-EVENT-001`: G2-EVENT-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:60`; audit line 706 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-205` | `G2-EVENT-002`: G2-EVENT-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:835`; audit line 707 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-206` | `G2-EVENT-003`: G2-EVENT-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:838`; audit line 708 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-207` | `G2-EVENT-004`: G2-EVENT-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:841`; audit line 709 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-208` | `G2-EVENT-005`: G2-EVENT-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:844`; audit line 710 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-209` | `G2-EVENT-006`: G2-EVENT-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:855`; audit line 711 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-210` | `G2-EVENT-007`: G2-EVENT-007 | `EOIP-engg-doc-pkg/gaps2-requirements.md:858`; audit line 712 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-211` | `G2-EVOL-001`: G2-EVOL-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:268`; audit line 713 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-212` | `G2-EVOL-002`: G2-EVOL-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:706`; audit line 714 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-213` | `G2-EVOL-003`: G2-EVOL-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:711`; audit line 715 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-214` | `G2-EVOL-004`: G2-EVOL-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:714`; audit line 716 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-215` | `G2-EVOL-005`: G2-EVOL-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:717`; audit line 717 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-216` | `G2-EVOL-006`: G2-EVOL-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:720`; audit line 718 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-217` | `G2-EVOL-007`: G2-EVOL-007 | `EOIP-engg-doc-pkg/gaps2-requirements.md:723`; audit line 719 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-218` | `G2-EVOL-008`: G2-EVOL-008 | `EOIP-engg-doc-pkg/gaps2-requirements.md:726`; audit line 720 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-219` | `G2-EVOL-009`: G2-EVOL-009 | `EOIP-engg-doc-pkg/gaps2-implementation.md:59`; audit line 721 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-220` | `G2-EVOL-010`: G2-EVOL-010 | `EOIP-engg-doc-pkg/gaps2-requirements.md:743`; audit line 722 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-221` | `G2-EVOL-011`: G2-EVOL-011 | `EOIP-engg-doc-pkg/gaps2-requirements.md:746`; audit line 723 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-222` | `G2-EVOL-012`: G2-EVOL-012 | `EOIP-engg-doc-pkg/gaps2-requirements.md:749`; audit line 724 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-223` | `G2-EVOL-013`: G2-EVOL-013 | `EOIP-engg-doc-pkg/gaps2-requirements.md:752`; audit line 725 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-224` | `G2-EVOL-014`: G2-EVOL-014 | `EOIP-engg-doc-pkg/gaps2-requirements.md:755`; audit line 726 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-225` | `G2-EVOL-015`: G2-EVOL-015 | `EOIP-engg-doc-pkg/gaps2-requirements.md:758`; audit line 727 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-226` | `G2-EVOL-016`: G2-EVOL-016 | `EOIP-engg-doc-pkg/gaps2-requirements.md:761`; audit line 728 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-227` | `G2-I2R-001`: G2-I2R-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:748`; audit line 753 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-228` | `G2-I2R-002`: G2-I2R-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1352`; audit line 754 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-229` | `G2-I2R-003`: G2-I2R-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1355`; audit line 755 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-230` | `G2-I2R-004`: G2-I2R-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1358`; audit line 756 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-231` | `G2-I2R-005`: G2-I2R-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1361`; audit line 757 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-232` | `G2-IMMUNE-001`: G2-IMMUNE-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:942`; audit line 758 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-233` | `G2-IMMUNE-002`: G2-IMMUNE-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1183`; audit line 759 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-234` | `G2-IMMUNE-003`: G2-IMMUNE-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1186`; audit line 760 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-235` | `G2-IMMUNE-004`: G2-IMMUNE-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1189`; audit line 761 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-236` | `G2-IMMUNE-005`: G2-IMMUNE-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1192`; audit line 762 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-237` | `G2-IMMUNE-006`: G2-IMMUNE-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1195`; audit line 763 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-238` | `G2-IMMUNE-007`: G2-IMMUNE-007 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1198`; audit line 764 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-239` | `G2-IMMUNE-008`: G2-IMMUNE-008 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1201`; audit line 765 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-240` | `G2-IMMUNE-009`: G2-IMMUNE-009 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1204`; audit line 766 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-241` | `G2-IMMUNE-010`: G2-IMMUNE-010 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1207`; audit line 767 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-242` | `G2-IMMUNE-011`: G2-IMMUNE-011 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1210`; audit line 768 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-243` | `G2-IMMUNE-012`: G2-IMMUNE-012 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1213`; audit line 769 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-244` | `G2-IMMUNE-013`: G2-IMMUNE-013 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1216`; audit line 770 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-245` | `G2-JOURNAL-001`: G2-JOURNAL-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:269`; audit line 771 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-NFR-246` | `G2-JOURNAL-002`: G2-JOURNAL-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:776`; audit line 772 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-NFR-247` | `G2-JOURNAL-003`: G2-JOURNAL-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:789`; audit line 773 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-NFR-248` | `G2-JOURNAL-004`: G2-JOURNAL-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:797`; audit line 774 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-NFR-249` | `G2-JOURNAL-005`: G2-JOURNAL-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:800`; audit line 775 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-NFR-250` | `G2-JOURNAL-006`: G2-JOURNAL-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:803`; audit line 776 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-NFR-251` | `G2-KD-001`: G2-KD-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:823`; audit line 777 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-252` | `G2-KD-002`: G2-KD-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1371`; audit line 778 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-253` | `G2-KD-003`: G2-KD-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1386`; audit line 779 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-254` | `G2-KD-004`: G2-KD-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1395`; audit line 780 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-255` | `G2-KD-005`: G2-KD-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1398`; audit line 781 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-256` | `G2-KD-006`: G2-KD-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1401`; audit line 782 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-257` | `G2-OEVO-001`: G2-OEVO-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:943`; audit line 789 | P2 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | ID family | PROVE |
| `REQ-NFR-258` | `G2-OEVO-002`: G2-OEVO-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1226`; audit line 790 | P2 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | ID family | PROVE |
| `REQ-NFR-259` | `G2-OEVO-003`: G2-OEVO-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1229`; audit line 791 | P2 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | ID family | PROVE |
| `REQ-NFR-260` | `G2-OEVO-004`: G2-OEVO-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1238`; audit line 792 | P2 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | ID family | PROVE |
| `REQ-NFR-261` | `G2-OEVO-005`: G2-OEVO-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1241`; audit line 793 | P2 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | ID family | PROVE |
| `REQ-NFR-262` | `G2-OEVO-006`: G2-OEVO-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1244`; audit line 794 | P2 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | ID family | PROVE |
| `REQ-NFR-263` | `G2-P0`: &#124; G2-P0 &#124; Contract & architecture alignment &#124; G2 additions fit current EOIP core &#124; | `EOIP-engg-doc-pkg/gaps2-implementation.md:35`; audit line 795 | P0 | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-264` | `G2-P9`: &#124; G2-P9 &#124; Simulation & causal intelligence &#124; counterfactual twin + causal hypotheses &#124; | `EOIP-engg-doc-pkg/gaps2-implementation.md:44`; audit line 807 | UNSTATED | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | subject triage | PROVE |
| `REQ-NFR-265` | `G2-PM-001`: G2-PM-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:822`; audit line 816 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-266` | `G2-PM-002`: G2-PM-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1254`; audit line 817 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-267` | `G2-PM-003`: G2-PM-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1257`; audit line 818 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-268` | `G2-PM-004`: G2-PM-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1266`; audit line 819 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-269` | `G2-PM-005`: G2-PM-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1269`; audit line 820 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-270` | `G2-QOP-001`: G2-QOP-001 — WHY | `EOIP-engg-doc-pkg/gaps2-implementation.md:825`; audit line 821 | P2 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-NFR-271` | `G2-QOP-002`: G2-QOP-002 — WHY NOT | `EOIP-engg-doc-pkg/gaps2-requirements.md:1320`; audit line 822 | P2 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-NFR-272` | `G2-QOP-003`: G2-QOP-003 — WHAT IF | `EOIP-engg-doc-pkg/gaps2-implementation.md:1018`; audit line 823 | P2 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-NFR-273` | `G2-QOP-004`: G2-QOP-004 — WHAT CHANGED | `EOIP-engg-doc-pkg/gaps2-requirements.md:1326`; audit line 824 | P2 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-NFR-274` | `G2-QOP-005`: G2-QOP-005 — WHEN | `EOIP-engg-doc-pkg/gaps2-requirements.md:1329`; audit line 825 | P2 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-NFR-275` | `G2-QOP-006`: G2-QOP-006 — WHO | `EOIP-engg-doc-pkg/gaps2-requirements.md:1332`; audit line 826 | P2 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-NFR-276` | `G2-QOP-007`: G2-QOP-007 — WHERE | `EOIP-engg-doc-pkg/gaps2-requirements.md:1335`; audit line 827 | P2 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-NFR-277` | `G2-QOP-008`: G2-QOP-008 — HOW | `EOIP-engg-doc-pkg/gaps2-requirements.md:1338`; audit line 828 | P2 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-NFR-278` | `G2-QOP-009`: G2-QOP-009 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1341`; audit line 829 | P2 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-NFR-279` | `G2-REL-001`: G2-REL-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:271`; audit line 830 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-280` | `G2-REL-002`: G2-REL-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1766`; audit line 831 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-281` | `G2-REL-003`: G2-REL-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1769`; audit line 832 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-282` | `G2-REL-004`: G2-REL-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1772`; audit line 833 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-283` | `G2-REL-005`: G2-REL-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1775`; audit line 834 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-284` | `G2-REL-006`: G2-REL-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1778`; audit line 835 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-285` | `G2-REL-007`: G2-REL-007 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1781`; audit line 836 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-286` | `G2-REL-008`: G2-REL-008 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1784`; audit line 837 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-287` | `G2-SIM-001`: G2-SIM-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1016`; audit line 851 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-288` | `G2-SIM-002`: G2-SIM-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1070`; audit line 852 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-289` | `G2-SIM-003`: G2-SIM-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1073`; audit line 853 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-290` | `G2-SIM-004`: G2-SIM-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1083`; audit line 854 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-291` | `G2-SIM-005`: G2-SIM-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1091`; audit line 855 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-292` | `G2-SIM-006`: G2-SIM-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1094`; audit line 856 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-293` | `G2-SIM-007`: G2-SIM-007 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1097`; audit line 857 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-294` | `G2-SLO-001`: G2-SLO-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:824`; audit line 858 | P2 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-NFR-295` | `G2-SLO-002`: G2-SLO-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1418`; audit line 859 | P2 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-NFR-296` | `G2-SLO-003`: G2-SLO-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1421`; audit line 860 | P2 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-NFR-297` | `G2-SLO-004`: G2-SLO-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1424`; audit line 861 | P2 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-NFR-298` | `G2-SLO-005`: G2-SLO-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1427`; audit line 862 | P2 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-NFR-299` | `G2-SRC-CICD-001`: G2-SRC-CICD-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:611`; audit line 869 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-300` | `G2-SRC-CICD-002`: G2-SRC-CICD-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:578`; audit line 870 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-301` | `G2-SRC-CICD-003`: G2-SRC-CICD-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:582`; audit line 871 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-302` | `G2-SRC-CICD-004`: G2-SRC-CICD-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:585`; audit line 872 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-303` | `G2-SRC-CODE-001`: G2-SRC-CODE-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:419`; audit line 873 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-304` | `G2-SRC-CODE-002`: G2-SRC-CODE-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:461`; audit line 874 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-305` | `G2-SRC-CODE-003`: G2-SRC-CODE-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:464`; audit line 875 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-306` | `G2-SRC-CODE-004`: G2-SRC-CODE-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:467`; audit line 876 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-307` | `G2-SRC-CODE-005`: G2-SRC-CODE-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:470`; audit line 877 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-308` | `G2-SRC-CONF-001`: G2-SRC-CONF-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:520`; audit line 878 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-309` | `G2-SRC-CONF-002`: G2-SRC-CONF-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:375`; audit line 879 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-310` | `G2-SRC-CONF-003`: G2-SRC-CONF-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:378`; audit line 880 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-311` | `G2-SRC-CONF-004`: G2-SRC-CONF-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:381`; audit line 881 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-312` | `G2-SRC-CONF-005`: G2-SRC-CONF-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:384`; audit line 882 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-313` | `G2-SRC-DD-001`: G2-SRC-DD-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:613`; audit line 883 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-314` | `G2-SRC-DD-002`: G2-SRC-DD-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:529`; audit line 884 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-315` | `G2-SRC-DD-003`: G2-SRC-DD-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:532`; audit line 885 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-316` | `G2-SRC-DD-004`: G2-SRC-DD-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:535`; audit line 886 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-317` | `G2-SRC-GH-001`: G2-SRC-GH-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:418`; audit line 887 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-318` | `G2-SRC-GH-002`: G2-SRC-GH-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:429`; audit line 888 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-319` | `G2-SRC-GH-003`: G2-SRC-GH-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:432`; audit line 889 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-320` | `G2-SRC-GH-004`: G2-SRC-GH-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:435`; audit line 890 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-321` | `G2-SRC-GL-001`: G2-SRC-GL-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:417`; audit line 891 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-322` | `G2-SRC-GL-002`: G2-SRC-GL-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:445`; audit line 892 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-323` | `G2-SRC-GL-003`: G2-SRC-GL-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:448`; audit line 893 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-324` | `G2-SRC-GL-004`: G2-SRC-GL-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:451`; audit line 894 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-325` | `G2-SRC-GRAF-001`: G2-SRC-GRAF-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:614`; audit line 895 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-326` | `G2-SRC-GRAF-002`: G2-SRC-GRAF-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:545`; audit line 896 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-327` | `G2-SRC-GRAF-003`: G2-SRC-GRAF-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:549`; audit line 897 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-328` | `G2-SRC-KIB-001`: G2-SRC-KIB-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:612`; audit line 904 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-329` | `G2-SRC-KIB-002`: G2-SRC-KIB-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:503`; audit line 905 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-330` | `G2-SRC-KIB-003`: G2-SRC-KIB-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:506`; audit line 906 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-331` | `G2-SRC-KIB-004`: G2-SRC-KIB-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:509`; audit line 907 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-332` | `G2-SRC-KIB-005`: G2-SRC-KIB-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:519`; audit line 908 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-333` | `G2-SRC-OTEL-001`: G2-SRC-OTEL-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:615`; audit line 909 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-334` | `G2-SRC-OTEL-002`: G2-SRC-OTEL-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:559`; audit line 910 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-335` | `G2-SRC-OTEL-003`: G2-SRC-OTEL-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:562`; audit line 911 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-336` | `G2-SRC-OTEL-004`: G2-SRC-OTEL-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:565`; audit line 912 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-337` | `G2-SRC-OTEL-005`: G2-SRC-OTEL-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:568`; audit line 913 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-338` | `G2-SRC-RUNTIME-001`: G2-SRC-RUNTIME-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:616`; audit line 914 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-339` | `G2-SRC-RUNTIME-002`: G2-SRC-RUNTIME-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:595`; audit line 915 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-340` | `G2-SRC-RUNTIME-003`: G2-SRC-RUNTIME-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:598`; audit line 916 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-341` | `G2-SRC-SBOM-001`: G2-SRC-SBOM-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:617`; audit line 917 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-342` | `G2-SRC-SBOM-002`: G2-SRC-SBOM-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:608`; audit line 918 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-343` | `G2-SRC-SBOM-003`: G2-SRC-SBOM-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:612`; audit line 919 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-344` | `G2-SRC-SBOM-004`: G2-SRC-SBOM-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:615`; audit line 920 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-345` | `G2-SRC-SNKB-001`: G2-SRC-SNKB-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:521`; audit line 921 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-346` | `G2-SRC-SNKB-002`: G2-SRC-SNKB-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:394`; audit line 922 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-347` | `G2-SRC-SNKB-003`: G2-SRC-SNKB-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:397`; audit line 923 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-348` | `G2-SRC-SNOW-001`: G2-SRC-SNOW-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:522`; audit line 924 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-349` | `G2-SRC-SNOW-002`: G2-SRC-SNOW-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:407`; audit line 925 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-350` | `G2-SRC-SNOW-003`: G2-SRC-SNOW-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:410`; audit line 926 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-351` | `G2-SRC-SNOW-004`: G2-SRC-SNOW-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:413`; audit line 927 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-352` | `G2-SRC-SNOW-005`: G2-SRC-SNOW-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:416`; audit line 928 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-353` | `G2-SRC-SNOW-006`: G2-SRC-SNOW-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:419`; audit line 929 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-NFR-354` | `G2-SYNC-001`: G2-SYNC-001 — Baseline state | `EOIP-engg-doc-pkg/gaps2-implementation.md:267`; audit line 935 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-NFR-355` | `G2-SYNC-003`: G2-SYNC-003 — Delta processing | `EOIP-engg-doc-pkg/gaps2-requirements.md:655`; audit line 937 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-NFR-356` | `G2-SYNC-004`: G2-SYNC-004 — Delete/retire | `EOIP-engg-doc-pkg/gaps2-requirements.md:658`; audit line 938 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-NFR-357` | `G2-SYNC-005`: G2-SYNC-005 — Missed-event recovery | `EOIP-engg-doc-pkg/gaps2-requirements.md:661`; audit line 939 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-NFR-358` | `G2-SYNC-006`: G2-SYNC-006 — Duplicate-event handling | `EOIP-engg-doc-pkg/gaps2-requirements.md:664`; audit line 940 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-NFR-359` | `G2-SYNC-007`: G2-SYNC-007 — Late event handling | `EOIP-engg-doc-pkg/gaps2-requirements.md:667`; audit line 941 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-NFR-360` | `G2-SYNC-008`: G2-SYNC-008 — Dependency-aware update | `EOIP-engg-doc-pkg/gaps2-requirements.md:670`; audit line 942 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-NFR-361` | `G2-SYNC-009`: G2-SYNC-009 — Consistency watermark | `EOIP-engg-doc-pkg/gaps2-requirements.md:673`; audit line 943 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-NFR-362` | `G2-SYNC-010`: G2-SYNC-010 — Full rebuild is exceptional | `EOIP-engg-doc-pkg/gaps2-requirements.md:676`; audit line 944 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-NFR-363` | `G2-SYNC-013`: G2-SYNC-013 — Backfill | `EOIP-engg-doc-pkg/gaps2-requirements.md:685`; audit line 947 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-NFR-364` | `G2-SYNC-014`: G2-SYNC-014 — Selective rescan | `EOIP-engg-doc-pkg/gaps2-requirements.md:688`; audit line 948 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-NFR-365` | `G2-T0005`: ### G2-T0005 — Capability interfaces | `EOIP-engg-doc-pkg/gaps2-implementation.md:105`; audit line 953 | UNSTATED | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-366` | `G2-T0101`: ### G2-T0101 | `EOIP-engg-doc-pkg/gaps2-implementation.md:145`; audit line 955 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-367` | `G2-T0102`: ### G2-T0102 | `EOIP-engg-doc-pkg/gaps2-implementation.md:148`; audit line 956 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-368` | `G2-T0103`: ### G2-T0103 | `EOIP-engg-doc-pkg/gaps2-implementation.md:151`; audit line 957 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-369` | `G2-T0104`: ### G2-T0104 | `EOIP-engg-doc-pkg/gaps2-implementation.md:154`; audit line 958 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-370` | `G2-T0110`: ### G2-T0110 | `EOIP-engg-doc-pkg/gaps2-implementation.md:161`; audit line 959 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-371` | `G2-T0111`: ### G2-T0111 | `EOIP-engg-doc-pkg/gaps2-implementation.md:170`; audit line 960 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-372` | `G2-T0112`: ### G2-T0112 | `EOIP-engg-doc-pkg/gaps2-implementation.md:173`; audit line 961 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-373` | `G2-T0120`: ### G2-T0120 | `EOIP-engg-doc-pkg/gaps2-implementation.md:180`; audit line 962 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-374` | `G2-T0121`: ### G2-T0121 | `EOIP-engg-doc-pkg/gaps2-implementation.md:183`; audit line 963 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-375` | `G2-T0122`: ### G2-T0122 | `EOIP-engg-doc-pkg/gaps2-implementation.md:186`; audit line 964 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-376` | `G2-T0123`: ### G2-T0123 | `EOIP-engg-doc-pkg/gaps2-implementation.md:189`; audit line 965 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-377` | `G2-T0130`: ### G2-T0130 | `EOIP-engg-doc-pkg/gaps2-implementation.md:196`; audit line 966 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-378` | `G2-T0131`: ### G2-T0131 | `EOIP-engg-doc-pkg/gaps2-implementation.md:205`; audit line 967 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-379` | `G2-T0132`: ### G2-T0132 | `EOIP-engg-doc-pkg/gaps2-implementation.md:208`; audit line 968 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-380` | `G2-T0133`: ### G2-T0133 | `EOIP-engg-doc-pkg/gaps2-implementation.md:216`; audit line 969 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-381` | `G2-T0134`: ### G2-T0134 | `EOIP-engg-doc-pkg/gaps2-implementation.md:219`; audit line 970 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-382` | `G2-T0135`: ### G2-T0135 | `EOIP-engg-doc-pkg/gaps2-implementation.md:222`; audit line 971 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-383` | `G2-T0140`: ### G2-T0140 | `EOIP-engg-doc-pkg/gaps2-implementation.md:229`; audit line 972 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-384` | `G2-T0141`: ### G2-T0141 | `EOIP-engg-doc-pkg/gaps2-implementation.md:232`; audit line 973 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-385` | `G2-T0142`: ### G2-T0142 | `EOIP-engg-doc-pkg/gaps2-implementation.md:235`; audit line 974 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-386` | `G2-T0150`: ### G2-T0150 | `EOIP-engg-doc-pkg/gaps2-implementation.md:242`; audit line 975 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-387` | `G2-T0151`: ### G2-T0151 | `EOIP-engg-doc-pkg/gaps2-implementation.md:245`; audit line 976 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-388` | `G2-T0152`: ### G2-T0152 | `EOIP-engg-doc-pkg/gaps2-implementation.md:248`; audit line 977 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-389` | `G2-T0153`: ### G2-T0153 | `EOIP-engg-doc-pkg/gaps2-implementation.md:251`; audit line 978 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-390` | `G2-T0201`: ### G2-T0201 | `EOIP-engg-doc-pkg/gaps2-implementation.md:277`; audit line 979 | UNSTATED | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-391` | `G2-T0202`: ### G2-T0202 | `EOIP-engg-doc-pkg/gaps2-implementation.md:282`; audit line 980 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-392` | `G2-T0203`: ### G2-T0203 | `EOIP-engg-doc-pkg/gaps2-implementation.md:291`; audit line 981 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-393` | `G2-T0210`: ### G2-T0210 | `EOIP-engg-doc-pkg/gaps2-implementation.md:298`; audit line 982 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-394` | `G2-T0211`: ### G2-T0211 | `EOIP-engg-doc-pkg/gaps2-implementation.md:301`; audit line 983 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-395` | `G2-T0212`: ### G2-T0212 | `EOIP-engg-doc-pkg/gaps2-implementation.md:304`; audit line 984 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-396` | `G2-T0213`: ### G2-T0213 | `EOIP-engg-doc-pkg/gaps2-implementation.md:312`; audit line 985 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-397` | `G2-T0220`: ### G2-T0220 | `EOIP-engg-doc-pkg/gaps2-implementation.md:319`; audit line 986 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-398` | `G2-T0221`: ### G2-T0221 | `EOIP-engg-doc-pkg/gaps2-implementation.md:322`; audit line 987 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-399` | `G2-T0222`: ### G2-T0222 | `EOIP-engg-doc-pkg/gaps2-implementation.md:330`; audit line 988 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-400` | `G2-T0223`: ### G2-T0223 | `EOIP-engg-doc-pkg/gaps2-implementation.md:333`; audit line 989 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-401` | `G2-T0224`: ### G2-T0224 | `EOIP-engg-doc-pkg/gaps2-implementation.md:336`; audit line 990 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-402` | `G2-T0225`: ### G2-T0225 | `EOIP-engg-doc-pkg/gaps2-implementation.md:339`; audit line 991 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-403` | `G2-T0230`: ### G2-T0230 | `EOIP-engg-doc-pkg/gaps2-implementation.md:346`; audit line 992 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-404` | `G2-T0231`: ### G2-T0231 | `EOIP-engg-doc-pkg/gaps2-implementation.md:349`; audit line 993 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-405` | `G2-T0232`: ### G2-T0232 | `EOIP-engg-doc-pkg/gaps2-implementation.md:352`; audit line 994 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-406` | `G2-T0240`: ### G2-T0240 | `EOIP-engg-doc-pkg/gaps2-implementation.md:359`; audit line 995 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-407` | `G2-T0241`: ### G2-T0241 | `EOIP-engg-doc-pkg/gaps2-implementation.md:362`; audit line 996 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-408` | `G2-T0242`: ### G2-T0242 | `EOIP-engg-doc-pkg/gaps2-implementation.md:365`; audit line 997 | UNSTATED | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-409` | `G2-T0243`: ### G2-T0243 | `EOIP-engg-doc-pkg/gaps2-implementation.md:371`; audit line 998 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-410` | `G2-T0250`: ### G2-T0250 | `EOIP-engg-doc-pkg/gaps2-implementation.md:378`; audit line 999 | UNSTATED | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-411` | `G2-T0251`: ### G2-T0251 | `EOIP-engg-doc-pkg/gaps2-implementation.md:381`; audit line 1000 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-412` | `G2-T0252`: ### G2-T0252 | `EOIP-engg-doc-pkg/gaps2-implementation.md:384`; audit line 1001 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-413` | `G2-T0253`: ### G2-T0253 | `EOIP-engg-doc-pkg/gaps2-implementation.md:387`; audit line 1002 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-414` | `G2-T0301`: ### G2-T0301 | `EOIP-engg-doc-pkg/gaps2-implementation.md:426`; audit line 1003 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-415` | `G2-T0302`: ### G2-T0302 | `EOIP-engg-doc-pkg/gaps2-implementation.md:433`; audit line 1004 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-416` | `G2-T0303`: ### G2-T0303 | `EOIP-engg-doc-pkg/gaps2-implementation.md:436`; audit line 1005 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-417` | `G2-T0304`: ### G2-T0304 | `EOIP-engg-doc-pkg/gaps2-implementation.md:439`; audit line 1006 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-418` | `G2-T0310`: ### G2-T0310 | `EOIP-engg-doc-pkg/gaps2-implementation.md:446`; audit line 1007 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-419` | `G2-T0311`: ### G2-T0311 | `EOIP-engg-doc-pkg/gaps2-implementation.md:449`; audit line 1008 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-420` | `G2-T0312`: ### G2-T0312 | `EOIP-engg-doc-pkg/gaps2-implementation.md:452`; audit line 1009 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-421` | `G2-T0313`: ### G2-T0313 | `EOIP-engg-doc-pkg/gaps2-implementation.md:455`; audit line 1010 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-422` | `G2-T0320`: ### G2-T0320 | `EOIP-engg-doc-pkg/gaps2-implementation.md:462`; audit line 1011 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-423` | `G2-T0321`: ### G2-T0321 | `EOIP-engg-doc-pkg/gaps2-implementation.md:465`; audit line 1012 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-424` | `G2-T0322`: ### G2-T0322 | `EOIP-engg-doc-pkg/gaps2-implementation.md:468`; audit line 1013 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-425` | `G2-T0323`: ### G2-T0323 | `EOIP-engg-doc-pkg/gaps2-implementation.md:471`; audit line 1014 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-426` | `G2-T0330`: ### G2-T0330 | `EOIP-engg-doc-pkg/gaps2-implementation.md:478`; audit line 1015 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-427` | `G2-T0331`: ### G2-T0331 | `EOIP-engg-doc-pkg/gaps2-implementation.md:481`; audit line 1016 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-428` | `G2-T0332`: ### G2-T0332 | `EOIP-engg-doc-pkg/gaps2-implementation.md:484`; audit line 1017 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-429` | `G2-T0333`: ### G2-T0333 | `EOIP-engg-doc-pkg/gaps2-implementation.md:487`; audit line 1018 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-430` | `G2-T0340`: ### G2-T0340 | `EOIP-engg-doc-pkg/gaps2-implementation.md:494`; audit line 1019 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-431` | `G2-T0341`: ### G2-T0341 | `EOIP-engg-doc-pkg/gaps2-implementation.md:497`; audit line 1020 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-432` | `G2-T0342`: ### G2-T0342 | `EOIP-engg-doc-pkg/gaps2-implementation.md:500`; audit line 1021 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-433` | `G2-T0401`: ### G2-T0401 | `EOIP-engg-doc-pkg/gaps2-implementation.md:530`; audit line 1022 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-434` | `G2-T0402`: ### G2-T0402 | `EOIP-engg-doc-pkg/gaps2-implementation.md:533`; audit line 1023 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-435` | `G2-T0403`: ### G2-T0403 | `EOIP-engg-doc-pkg/gaps2-implementation.md:536`; audit line 1024 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-436` | `G2-T0404`: ### G2-T0404 | `EOIP-engg-doc-pkg/gaps2-implementation.md:539`; audit line 1025 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-437` | `G2-T0405`: ### G2-T0405 | `EOIP-engg-doc-pkg/gaps2-implementation.md:542`; audit line 1026 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-438` | `G2-T0410`: ### G2-T0410 — KB | `EOIP-engg-doc-pkg/gaps2-implementation.md:551`; audit line 1027 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-439` | `G2-T0411`: ### G2-T0411 — Incident | `EOIP-engg-doc-pkg/gaps2-implementation.md:554`; audit line 1028 | UNSTATED | MISSED | [CP-18](#cp-18) | subject triage | TRACE/BUILD |
| `REQ-NFR-440` | `G2-T0412`: ### G2-T0412 — Problem | `EOIP-engg-doc-pkg/gaps2-implementation.md:557`; audit line 1029 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-441` | `G2-T0413`: ### G2-T0413 — Change | `EOIP-engg-doc-pkg/gaps2-implementation.md:560`; audit line 1030 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-442` | `G2-T0414`: ### G2-T0414 — CMDB | `EOIP-engg-doc-pkg/gaps2-implementation.md:563`; audit line 1031 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-443` | `G2-T0415`: ### G2-T0415 | `EOIP-engg-doc-pkg/gaps2-implementation.md:566`; audit line 1032 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-444` | `G2-T0416`: ### G2-T0416 | `EOIP-engg-doc-pkg/gaps2-implementation.md:569`; audit line 1033 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-445` | `G2-T0420`: ### G2-T0420 | `EOIP-engg-doc-pkg/gaps2-implementation.md:576`; audit line 1034 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-446` | `G2-T0421`: ### G2-T0421 | `EOIP-engg-doc-pkg/gaps2-implementation.md:579`; audit line 1035 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-447` | `G2-T0422`: ### G2-T0422 | `EOIP-engg-doc-pkg/gaps2-implementation.md:582`; audit line 1036 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-448` | `G2-T0423`: ### G2-T0423 | `EOIP-engg-doc-pkg/gaps2-implementation.md:585`; audit line 1037 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-449` | `G2-T0424`: ### G2-T0424 | `EOIP-engg-doc-pkg/gaps2-implementation.md:588`; audit line 1038 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-450` | `G2-T0425`: ### G2-T0425 | `EOIP-engg-doc-pkg/gaps2-implementation.md:591`; audit line 1039 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-451` | `G2-T0426`: ### G2-T0426 | `EOIP-engg-doc-pkg/gaps2-implementation.md:594`; audit line 1040 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-452` | `G2-T0501`: ### G2-T0501 | `EOIP-engg-doc-pkg/gaps2-implementation.md:627`; audit line 1041 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-453` | `G2-T0502`: ### G2-T0502 | `EOIP-engg-doc-pkg/gaps2-implementation.md:630`; audit line 1042 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-454` | `G2-T0503`: ### G2-T0503 | `EOIP-engg-doc-pkg/gaps2-implementation.md:633`; audit line 1043 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-455` | `G2-T0504`: ### G2-T0504 | `EOIP-engg-doc-pkg/gaps2-implementation.md:636`; audit line 1044 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-456` | `G2-T0510`: ### G2-T0510 | `EOIP-engg-doc-pkg/gaps2-implementation.md:643`; audit line 1045 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-457` | `G2-T0511`: ### G2-T0511 | `EOIP-engg-doc-pkg/gaps2-implementation.md:646`; audit line 1046 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-458` | `G2-T0512`: ### G2-T0512 | `EOIP-engg-doc-pkg/gaps2-implementation.md:649`; audit line 1047 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-459` | `G2-T0513`: ### G2-T0513 | `EOIP-engg-doc-pkg/gaps2-implementation.md:652`; audit line 1048 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-460` | `G2-T0520`: ### G2-T0520 | `EOIP-engg-doc-pkg/gaps2-implementation.md:659`; audit line 1049 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-461` | `G2-T0521`: ### G2-T0521 | `EOIP-engg-doc-pkg/gaps2-implementation.md:662`; audit line 1050 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-462` | `G2-T0522`: ### G2-T0522 | `EOIP-engg-doc-pkg/gaps2-implementation.md:665`; audit line 1051 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-463` | `G2-T0523`: ### G2-T0523 | `EOIP-engg-doc-pkg/gaps2-implementation.md:668`; audit line 1052 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-464` | `G2-T0530`: ### G2-T0530 | `EOIP-engg-doc-pkg/gaps2-implementation.md:675`; audit line 1053 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-465` | `G2-T0531`: ### G2-T0531 | `EOIP-engg-doc-pkg/gaps2-implementation.md:678`; audit line 1054 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-466` | `G2-T0532`: ### G2-T0532 | `EOIP-engg-doc-pkg/gaps2-implementation.md:681`; audit line 1055 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-467` | `G2-T0540`: ### G2-T0540 | `EOIP-engg-doc-pkg/gaps2-implementation.md:688`; audit line 1056 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-468` | `G2-T0541`: ### G2-T0541 | `EOIP-engg-doc-pkg/gaps2-implementation.md:691`; audit line 1057 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-469` | `G2-T0542`: ### G2-T0542 | `EOIP-engg-doc-pkg/gaps2-implementation.md:694`; audit line 1058 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-470` | `G2-T0543`: ### G2-T0543 | `EOIP-engg-doc-pkg/gaps2-implementation.md:697`; audit line 1059 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-471` | `G2-T0550`: ### G2-T0550 | `EOIP-engg-doc-pkg/gaps2-implementation.md:704`; audit line 1060 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-472` | `G2-T0551`: ### G2-T0551 | `EOIP-engg-doc-pkg/gaps2-implementation.md:707`; audit line 1061 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-473` | `G2-T0560`: ### G2-T0560 | `EOIP-engg-doc-pkg/gaps2-implementation.md:714`; audit line 1062 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-474` | `G2-T0561`: ### G2-T0561 | `EOIP-engg-doc-pkg/gaps2-implementation.md:717`; audit line 1063 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-475` | `G2-T0562`: ### G2-T0562 | `EOIP-engg-doc-pkg/gaps2-implementation.md:720`; audit line 1064 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-476` | `G2-T0563`: ### G2-T0563 | `EOIP-engg-doc-pkg/gaps2-implementation.md:723`; audit line 1065 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-477` | `G2-T0601`: ### G2-T0601 | `EOIP-engg-doc-pkg/gaps2-implementation.md:754`; audit line 1066 | UNSTATED | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-478` | `G2-T0602`: ### G2-T0602 | `EOIP-engg-doc-pkg/gaps2-implementation.md:757`; audit line 1067 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-479` | `G2-T0603`: ### G2-T0603 | `EOIP-engg-doc-pkg/gaps2-implementation.md:760`; audit line 1068 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-480` | `G2-T0610`: ### G2-T0610 | `EOIP-engg-doc-pkg/gaps2-implementation.md:767`; audit line 1069 | UNSTATED | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-481` | `G2-T0611`: ### G2-T0611 | `EOIP-engg-doc-pkg/gaps2-implementation.md:770`; audit line 1070 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-482` | `G2-T0612`: ### G2-T0612 | `EOIP-engg-doc-pkg/gaps2-implementation.md:773`; audit line 1071 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-483` | `G2-T0620`: ### G2-T0620 | `EOIP-engg-doc-pkg/gaps2-implementation.md:780`; audit line 1072 | UNSTATED | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-484` | `G2-T0621`: ### G2-T0621 | `EOIP-engg-doc-pkg/gaps2-implementation.md:783`; audit line 1073 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-485` | `G2-T0622`: ### G2-T0622 | `EOIP-engg-doc-pkg/gaps2-implementation.md:786`; audit line 1074 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-486` | `G2-T0630`: ### G2-T0630 | `EOIP-engg-doc-pkg/gaps2-implementation.md:793`; audit line 1075 | UNSTATED | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-487` | `G2-T0631`: ### G2-T0631 | `EOIP-engg-doc-pkg/gaps2-implementation.md:800`; audit line 1076 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-488` | `G2-T0632`: ### G2-T0632 | `EOIP-engg-doc-pkg/gaps2-implementation.md:803`; audit line 1077 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-489` | `G2-T0701`: ### G2-T0701 | `EOIP-engg-doc-pkg/gaps2-implementation.md:831`; audit line 1078 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-490` | `G2-T0702`: ### G2-T0702 | `EOIP-engg-doc-pkg/gaps2-implementation.md:834`; audit line 1079 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-491` | `G2-T0703`: ### G2-T0703 | `EOIP-engg-doc-pkg/gaps2-implementation.md:837`; audit line 1080 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-492` | `G2-T0704`: ### G2-T0704 | `EOIP-engg-doc-pkg/gaps2-implementation.md:840`; audit line 1081 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-493` | `G2-T0705`: ### G2-T0705 | `EOIP-engg-doc-pkg/gaps2-implementation.md:843`; audit line 1082 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-494` | `G2-T0710`: ### G2-T0710 | `EOIP-engg-doc-pkg/gaps2-implementation.md:850`; audit line 1083 | UNSTATED | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-495` | `G2-T0711`: ### G2-T0711 | `EOIP-engg-doc-pkg/gaps2-implementation.md:853`; audit line 1084 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-496` | `G2-T0712`: ### G2-T0712 | `EOIP-engg-doc-pkg/gaps2-implementation.md:856`; audit line 1085 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-497` | `G2-T0713`: ### G2-T0713 | `EOIP-engg-doc-pkg/gaps2-implementation.md:859`; audit line 1086 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-498` | `G2-T0714`: ### G2-T0714 | `EOIP-engg-doc-pkg/gaps2-implementation.md:862`; audit line 1087 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-499` | `G2-T0715`: ### G2-T0715 | `EOIP-engg-doc-pkg/gaps2-implementation.md:865`; audit line 1088 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-500` | `G2-T0720`: ### G2-T0720 | `EOIP-engg-doc-pkg/gaps2-implementation.md:872`; audit line 1089 | UNSTATED | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-501` | `G2-T0721`: ### G2-T0721 | `EOIP-engg-doc-pkg/gaps2-implementation.md:875`; audit line 1090 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-502` | `G2-T0722`: ### G2-T0722 | `EOIP-engg-doc-pkg/gaps2-implementation.md:878`; audit line 1091 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-503` | `G2-T0723`: ### G2-T0723 | `EOIP-engg-doc-pkg/gaps2-implementation.md:881`; audit line 1092 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-504` | `G2-T0730`: ### G2-T0730 | `EOIP-engg-doc-pkg/gaps2-implementation.md:888`; audit line 1093 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-505` | `G2-T0731`: ### G2-T0731 | `EOIP-engg-doc-pkg/gaps2-implementation.md:891`; audit line 1094 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-506` | `G2-T0732`: ### G2-T0732 | `EOIP-engg-doc-pkg/gaps2-implementation.md:894`; audit line 1095 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-507` | `G2-T0733`: ### G2-T0733 | `EOIP-engg-doc-pkg/gaps2-implementation.md:897`; audit line 1096 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-508` | `G2-T0740`: ### G2-T0740 | `EOIP-engg-doc-pkg/gaps2-implementation.md:904`; audit line 1097 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-509` | `G2-T0741`: ### G2-T0741 | `EOIP-engg-doc-pkg/gaps2-implementation.md:907`; audit line 1098 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-510` | `G2-T0742`: ### G2-T0742 | `EOIP-engg-doc-pkg/gaps2-implementation.md:910`; audit line 1099 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-511` | `G2-T0743`: ### G2-T0743 | `EOIP-engg-doc-pkg/gaps2-implementation.md:913`; audit line 1100 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-512` | `G2-T0750`: ### G2-T0750 | `EOIP-engg-doc-pkg/gaps2-implementation.md:920`; audit line 1101 | UNSTATED | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-513` | `G2-T0751`: ### G2-T0751 | `EOIP-engg-doc-pkg/gaps2-implementation.md:923`; audit line 1102 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-514` | `G2-T0752`: ### G2-T0752 | `EOIP-engg-doc-pkg/gaps2-implementation.md:926`; audit line 1103 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-515` | `G2-T0753`: ### G2-T0753 | `EOIP-engg-doc-pkg/gaps2-implementation.md:929`; audit line 1104 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-516` | `G2-T0801`: ### G2-T0801 | `EOIP-engg-doc-pkg/gaps2-implementation.md:950`; audit line 1105 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-517` | `G2-T0802`: ### G2-T0802 | `EOIP-engg-doc-pkg/gaps2-implementation.md:953`; audit line 1106 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-518` | `G2-T0803`: ### G2-T0803 | `EOIP-engg-doc-pkg/gaps2-implementation.md:956`; audit line 1107 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-519` | `G2-T0804`: ### G2-T0804 | `EOIP-engg-doc-pkg/gaps2-implementation.md:959`; audit line 1108 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-520` | `G2-T0805`: ### G2-T0805 | `EOIP-engg-doc-pkg/gaps2-implementation.md:962`; audit line 1109 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-521` | `G2-T0810`: ### G2-T0810 | `EOIP-engg-doc-pkg/gaps2-implementation.md:969`; audit line 1110 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-522` | `G2-T0811`: ### G2-T0811 | `EOIP-engg-doc-pkg/gaps2-implementation.md:972`; audit line 1111 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-523` | `G2-T0812`: ### G2-T0812 | `EOIP-engg-doc-pkg/gaps2-implementation.md:975`; audit line 1112 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-524` | `G2-T0813`: ### G2-T0813 | `EOIP-engg-doc-pkg/gaps2-implementation.md:978`; audit line 1113 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-525` | `G2-T0814`: ### G2-T0814 | `EOIP-engg-doc-pkg/gaps2-implementation.md:981`; audit line 1114 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-526` | `G2-T0820`: ### G2-T0820 | `EOIP-engg-doc-pkg/gaps2-implementation.md:988`; audit line 1115 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-527` | `G2-T0821`: ### G2-T0821 | `EOIP-engg-doc-pkg/gaps2-implementation.md:991`; audit line 1116 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-528` | `G2-T0822`: ### G2-T0822 | `EOIP-engg-doc-pkg/gaps2-implementation.md:994`; audit line 1117 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-529` | `G2-T0823`: ### G2-T0823 | `EOIP-engg-doc-pkg/gaps2-implementation.md:997`; audit line 1118 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-530` | `G2-T0824`: ### G2-T0824 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1000`; audit line 1119 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-531` | `G2-T0901`: ### G2-T0901 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1024`; audit line 1120 | UNSTATED | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-532` | `G2-T0902`: ### G2-T0902 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1027`; audit line 1121 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-533` | `G2-T0903`: ### G2-T0903 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1030`; audit line 1122 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-534` | `G2-T0904`: ### G2-T0904 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1033`; audit line 1123 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-535` | `G2-T0905`: ### G2-T0905 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1036`; audit line 1124 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-536` | `G2-T0906`: ### G2-T0906 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1039`; audit line 1125 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-537` | `G2-T0910`: ### G2-T0910 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1046`; audit line 1126 | UNSTATED | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-538` | `G2-T0911`: ### G2-T0911 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1049`; audit line 1127 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-539` | `G2-T0912`: ### G2-T0912 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1052`; audit line 1128 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-540` | `G2-T0920`: ### G2-T0920 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1059`; audit line 1129 | UNSTATED | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-541` | `G2-T0921`: ### G2-T0921 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1062`; audit line 1130 | UNSTATED | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-542` | `G2-T0922`: ### G2-T0922 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1065`; audit line 1131 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-543` | `G2-T0923`: ### G2-T0923 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1068`; audit line 1132 | UNSTATED | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-544` | `G2-T0924`: ### G2-T0924 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1071`; audit line 1133 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-545` | `G2-T1030`: ### G2-T1030 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1154`; audit line 1134 | UNSTATED | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-546` | `G2-T1031`: ### G2-T1031 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1157`; audit line 1135 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-547` | `G2-T1032`: ### G2-T1032 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1160`; audit line 1136 | UNSTATED | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-548` | `G2-T1033`: ### G2-T1033 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1163`; audit line 1137 | UNSTATED | PARTIAL | [CP-00](#cp-00) | area fallback | COMPLETE |
| `REQ-NFR-549` | `G2-T1040`: ### G2-T1040 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1170`; audit line 1138 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-550` | `G2-T1041`: ### G2-T1041 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1173`; audit line 1139 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-551` | `G2-T1042`: ### G2-T1042 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1176`; audit line 1140 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-552` | `G2-T1043`: ### G2-T1043 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1179`; audit line 1141 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-553` | `G2-T1044`: ### G2-T1044 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1182`; audit line 1142 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-554` | `G2-T1045`: ### G2-T1045 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1185`; audit line 1143 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-555` | `G2-T1046`: ### G2-T1046 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1188`; audit line 1144 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-556` | `G2-TEL-001`: G2-TEL-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:621`; audit line 1145 | P2 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-NFR-557` | `G2-TEL-002`: G2-TEL-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1637`; audit line 1146 | P2 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-NFR-558` | `G2-TEL-003`: G2-TEL-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1640`; audit line 1147 | P2 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-NFR-559` | `G2-TEL-004`: G2-TEL-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1643`; audit line 1148 | P2 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-NFR-560` | `G2-TEL-005`: G2-TEL-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1646`; audit line 1149 | P2 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-NFR-561` | `G2-TEL-006`: G2-TEL-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1649`; audit line 1150 | P2 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-NFR-562` | `G2-TEL-007`: G2-TEL-007 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1652`; audit line 1151 | P2 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-NFR-563` | `G2-TEL-008`: G2-TEL-008 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1655`; audit line 1152 | P2 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-NFR-564` | `G2-TIME-001`: G2-TIME-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:820`; audit line 1153 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-NFR-565` | `G2-TIME-002`: G2-TIME-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1045`; audit line 1154 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-NFR-566` | `G2-TIME-003`: G2-TIME-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1048`; audit line 1155 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-NFR-567` | `G2-TIME-004`: G2-TIME-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1051`; audit line 1156 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-NFR-568` | `G2-TIME-005`: G2-TIME-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1054`; audit line 1157 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-NFR-569` | `G2-TIME-006`: G2-TIME-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1057`; audit line 1158 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-NFR-570` | `G2-TIME-007`: G2-TIME-007 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1060`; audit line 1159 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-NFR-571` | `G2-TWIN-001`: G2-TWIN-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:747`; audit line 1160 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-572` | `G2-TWIN-002`: G2-TWIN-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1008`; audit line 1161 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-573` | `G2-TWIN-003`: G2-TWIN-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1025`; audit line 1162 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-574` | `G2-TWIN-004`: G2-TWIN-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1028`; audit line 1163 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-575` | `G2-TWIN-005`: G2-TWIN-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1031`; audit line 1164 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-576` | `G2-VSC-001`: G2-VSC-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1091`; audit line 1189 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-NFR-577` | `G2-VSC-002`: G2-VSC-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1609`; audit line 1190 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-NFR-578` | `G2-VSC-003`: G2-VSC-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1612`; audit line 1191 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-NFR-579` | `G2-VSC-004`: G2-VSC-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1615`; audit line 1192 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-NFR-580` | `G2-VSC-005`: G2-VSC-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1618`; audit line 1193 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-NFR-581` | `G2-VSC-006`: G2-VSC-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1621`; audit line 1194 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-NFR-582` | `G2-VSC-007`: G2-VSC-007 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1624`; audit line 1195 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-NFR-583` | `G2-VSC-008`: G2-VSC-008 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1627`; audit line 1196 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-NFR-584` | `GAP-AGOV-002`: GAP-AGOV-002: Read/write/destructive risk classification | `EOIP-engg-doc-pkg/gaps-requirements.md:715`; audit line 1208 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | ID family | PROVE |
| `REQ-NFR-585` | `GAP-AGOV-004`: GAP-AGOV-004: Human approval policy by risk | `EOIP-engg-doc-pkg/gaps-requirements.md:717`; audit line 1210 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | ID family | PROVE |
| `REQ-NFR-586` | `GAP-AGOV-011`: GAP-AGOV-011: Deterministic dry-run mode | `EOIP-engg-doc-pkg/gaps-requirements.md:724`; audit line 1217 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | ID family | PROVE |
| `REQ-NFR-587` | `GAP-APP`: Knowledge app builder | `requirements-registry.json:1`; audit line 1231 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-588` | `GAP-APP-002`: GAP-APP-002: App definitions must be configuration-as-code and exportable | `EOIP-engg-doc-pkg/gaps-requirements.md:274`; audit line 1233 | P2 | IMPLEMENTED-UNVERIFIED | [CP-25](#cp-25) | subject triage | PROVE |
| `REQ-NFR-589` | `GAP-ARCH-001`: GAP-ARCH-001: Allow architecture rules such as: | `EOIP-engg-doc-pkg/gaps-implementation.md:382`; audit line 1234 | P0 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-590` | `GAP-ARCH-005`: GAP-ARCH-005: Link violation to exact code symbols/commits | `EOIP-engg-doc-pkg/gaps-requirements.md:538`; audit line 1238 | P0 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-NFR-591` | `GAP-CATALOG`: Knowledge catalog | `requirements-registry.json:1`; audit line 1245 | P1 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | subject triage | PROVE |
| `REQ-NFR-592` | `GAP-CATALOG-002`: GAP-CATALOG-002: Support asset certification states: Draft, Candidate, Trusted, Certified, Deprecated, Quarantined | `EOIP-engg-doc-pkg/gaps-requirements.md:297`; audit line 1247 | P0 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | subject triage | PROVE |
| `REQ-NFR-593` | `GAP-CATALOG-003`: GAP-CATALOG-003: Create stewardship assignments and data/knowledge ownership | `EOIP-engg-doc-pkg/gaps-requirements.md:298`; audit line 1248 | P0 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | subject triage | PROVE |
| `REQ-NFR-594` | `GAP-CATALOG-004`: GAP-CATALOG-004: Add domain collections / knowledge products | `EOIP-engg-doc-pkg/gaps-requirements.md:299`; audit line 1249 | P0 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | subject triage | PROVE |
| `REQ-NFR-595` | `GAP-CDC-002`: GAP-CDC-002: Event includes before/after semantic identity | `EOIP-engg-doc-pkg/gaps-requirements.md:804`; audit line 1252 | P1 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-NFR-596` | `GAP-CP-009`: GAP-CP-009: Semantic contracts are machine-readable and testable | `EOIP-engg-doc-pkg/gaps-requirements.md:407`; audit line 1277 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-597` | `GAP-DRIFT-003`: GAP-DRIFT-003: Detect vocabulary usage drift | `EOIP-engg-doc-pkg/gaps-requirements.md:515`; audit line 1282 | P1 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-NFR-598` | `GAP-DRIFT-007`: GAP-DRIFT-007: Generate drift explanations and affected assets | `EOIP-engg-doc-pkg/gaps-requirements.md:519`; audit line 1286 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-599` | `GAP-ER-001`: GAP-ER-001: Deterministic match rules | `EOIP-engg-doc-pkg/gaps-requirements.md:621`; audit line 1291 | P1 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-NFR-600` | `GAP-ER-002`: GAP-ER-002: Probabilistic/fuzzy match | `EOIP-engg-doc-pkg/gaps-requirements.md:622`; audit line 1292 | P1 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-NFR-601` | `GAP-ER-003`: GAP-ER-003: Configurable match features | `EOIP-engg-doc-pkg/gaps-requirements.md:623`; audit line 1293 | P1 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-NFR-602` | `GAP-ER-004`: GAP-ER-004: Explain match score | `EOIP-engg-doc-pkg/gaps-requirements.md:624`; audit line 1294 | P1 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-NFR-603` | `GAP-ER-005`: GAP-ER-005: Candidate queue for human review | `EOIP-engg-doc-pkg/gaps-requirements.md:625`; audit line 1295 | P1 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-NFR-604` | `GAP-ER-006`: GAP-ER-006: Merge/unmerge | `EOIP-engg-doc-pkg/gaps-requirements.md:626`; audit line 1296 | P1 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-NFR-605` | `GAP-ER-007`: GAP-ER-007: Golden entity record | `EOIP-engg-doc-pkg/gaps-requirements.md:627`; audit line 1297 | P1 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-NFR-606` | `GAP-ER-009`: GAP-ER-009: Historical identity evolution | `EOIP-engg-doc-pkg/gaps-requirements.md:629`; audit line 1299 | P1 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-NFR-607` | `GAP-ER-010`: GAP-ER-010: No irreversible automatic merge below confidence threshold | `EOIP-engg-doc-pkg/gaps-requirements.md:630`; audit line 1300 | P1 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-NFR-608` | `GAP-EXT-001`: GAP-EXT-001: Support extension SDKs rather than requiring modification of the core platform | `EOIP-engg-doc-pkg/gaps-implementation.md:785`; audit line 1302 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-609` | `GAP-FED`: Semantic federation layer | `requirements-registry.json:1`; audit line 1311 | P1 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | subject triage | PROVE |
| `REQ-NFR-610` | `GAP-FRESH-001`: GAP-FRESH-001: Detect stale documents | `EOIP-engg-doc-pkg/gaps-implementation.md:384`; audit line 1316 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-611` | `GAP-FRESH-002`: GAP-FRESH-002: Detect docs contradicted by code/config/runtime | `EOIP-engg-doc-pkg/gaps-requirements.md:1002`; audit line 1317 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-612` | `GAP-FRESH-003`: GAP-FRESH-003: Detect ownership changes | `EOIP-engg-doc-pkg/gaps-requirements.md:1003`; audit line 1318 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-613` | `GAP-FRESH-004`: GAP-FRESH-004: Detect deprecated APIs still referenced in docs | `EOIP-engg-doc-pkg/gaps-requirements.md:1004`; audit line 1319 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-614` | `GAP-FRESH-005`: GAP-FRESH-005: Recommend review—not silently rewrite authoritative docs | `EOIP-engg-doc-pkg/gaps-requirements.md:1005`; audit line 1320 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-615` | `GAP-GITOPS-003`: GAP-GITOPS-003: Generate semantic diffs: | `EOIP-engg-doc-pkg/gaps-requirements.md:419`; audit line 1326 | P0 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | ID family | PROVE |
| `REQ-NFR-616` | `GAP-GITOPS-006`: GAP-GITOPS-006: Generate migration scripts | `EOIP-engg-doc-pkg/gaps-requirements.md:429`; audit line 1329 | P0 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | ID family | PROVE |
| `REQ-NFR-617` | `GAP-GOV`: Semantic stewardship workflow | `requirements-registry.json:1`; audit line 1332 | P1 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | subject triage | PROVE |
| `REQ-NFR-618` | `GAP-GOV-001`: GAP-GOV-001: Add semantic stewardship workflow: draft → review → approve → publish → deprecate | `EOIP-engg-doc-pkg/gaps-implementation.md:298`; audit line 1333 | P2 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | subject triage | PROVE |
| `REQ-NFR-619` | `GAP-GRAG-003`: GAP-GRAG-003: Add community detection and hierarchical semantic summaries, but regenerate summaries incrementally rather than rebuilding the whole corpus | `EOIP-engg-doc-pkg/gaps-requirements.md:360`; audit line 1338 | P2 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-NFR-620` | `GAP-GRAG-004`: GAP-GRAG-004: Maintain cost/compute budgets even for local models | `EOIP-engg-doc-pkg/gaps-requirements.md:361`; audit line 1339 | P2 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-NFR-621` | `GAP-HG-003`: GAP-HG-003: Index advisor | `EOIP-engg-doc-pkg/gaps-requirements.md:1076`; audit line 1347 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-NFR-622` | `GAP-HG-008`: GAP-HG-008: capacity benchmark before production | `EOIP-engg-doc-pkg/gaps-requirements.md:1081`; audit line 1352 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-NFR-623` | `GAP-IDE`: VS Code extension completion | `requirements-registry.json:1`; audit line 1355 | P1 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | subject triage | PROVE |
| `REQ-NFR-624` | `GAP-KFW-001`: GAP-KFW-001: Inspect all context leaving a knowledge boundary | `EOIP-engg-doc-pkg/gaps-implementation.md:603`; audit line 1357 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-NFR-625` | `GAP-KFW-003`: GAP-KFW-003: Block or redact based on policy | `EOIP-engg-doc-pkg/gaps-requirements.md:737`; audit line 1359 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-NFR-626` | `GAP-KFW-008`: GAP-KFW-008: Provide “why blocked/redacted?” explanation | `EOIP-engg-doc-pkg/gaps-requirements.md:742`; audit line 1364 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-NFR-627` | `GAP-KGCI-003`: GAP-KGCI-003: Fail build on configured semantic regression | `EOIP-engg-doc-pkg/gaps-requirements.md:822`; audit line 1367 | P0 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | subject triage | PROVE |
| `REQ-NFR-628` | `GAP-KP-002`: GAP-KP-002: A Knowledge Product defines: | `EOIP-engg-doc-pkg/gaps-requirements.md:582`; audit line 1370 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-629` | `GAP-KP-003`: GAP-KP-003: Product states: Draft, Experimental, Trusted, Certified, Deprecated | `EOIP-engg-doc-pkg/gaps-requirements.md:593`; audit line 1371 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-630` | `GAP-KP-005`: GAP-KP-005: Export/import product definitions | `EOIP-engg-doc-pkg/gaps-requirements.md:595`; audit line 1373 | P1 | IMPLEMENTED-UNVERIFIED | [CP-25](#cp-25) | subject triage | PROVE |
| `REQ-NFR-631` | `GAP-KQ-002`: GAP-KQ-002: Compute: | `EOIP-engg-doc-pkg/gaps-requirements.md:490`; audit line 1375 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-NFR-632` | `GAP-KQ-006`: GAP-KQ-006: Support trend charts and regression gates | `EOIP-engg-doc-pkg/gaps-requirements.md:505`; audit line 1379 | P0 | IMPLEMENTED-UNVERIFIED | [CP-17](#cp-17) | ID family | PROVE |
| `REQ-NFR-633` | `GAP-KRAG-003`: GAP-KRAG-003: Community summaries must link to underlying nodes/edges | `EOIP-engg-doc-pkg/gaps-requirements.md:678`; audit line 1382 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-NFR-634` | `GAP-KRAG-004`: GAP-KRAG-004: Incremental community update | `EOIP-engg-doc-pkg/gaps-requirements.md:679`; audit line 1383 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-NFR-635` | `GAP-KRAG-006`: GAP-KRAG-006: Contradiction-aware context assembly | `EOIP-engg-doc-pkg/gaps-requirements.md:681`; audit line 1385 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-NFR-636` | `GAP-LIFE-004`: GAP-LIFE-004: Retention policies per domain/classification | `EOIP-engg-doc-pkg/gaps-requirements.md:903`; audit line 1395 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-637` | `GAP-LIFE-006`: GAP-LIFE-006: Rebuild derived data from authoritative inputs | `EOIP-engg-doc-pkg/gaps-requirements.md:905`; audit line 1397 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-638` | `GAP-LITE-002`: GAP-LITE-002: Implement automated sizing and capacity planning | `EOIP-engg-doc-pkg/gaps-requirements.md:254`; audit line 1404 | P2 | IMPLEMENTED-UNVERIFIED | [CP-27](#cp-27) | ID family | PROVE |
| `REQ-NFR-639` | `GAP-MIGRATION-001`: GAP-MIGRATION-001: Provide migration utilities and stable external IDs | `EOIP-engg-doc-pkg/gaps-requirements.md:340`; audit line 1405 | P2 | IMPLEMENTED-UNVERIFIED | [CP-31](#cp-31) | ID family | PROVE |
| `REQ-NFR-640` | `GAP-MKT-004`: GAP-MKT-004: Package validation rules | `EOIP-engg-doc-pkg/gaps-requirements.md:918`; audit line 1409 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-NFR-641` | `GAP-MKT-008`: GAP-MKT-008: Signed packages in later phases | `EOIP-engg-doc-pkg/gaps-requirements.md:922`; audit line 1413 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-NFR-642` | `GAP-NLP`: Local NLP pipeline | `requirements-registry.json:1`; audit line 1414 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-643` | `GAP-NOCODE-002`: GAP-NOCODE-002: Provide novice, analyst and expert editing modes | `EOIP-engg-doc-pkg/gaps-requirements.md:195`; audit line 1418 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-644` | `GAP-PACK-001`: GAP-PACK-001: Keep major core capabilities integrated in one platform while allowing optional modules rather than artificial fragmentation | `EOIP-engg-doc-pkg/gaps-requirements.md:224`; audit line 1427 | P2 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-645` | `GAP-PORT-001`: GAP-PORT-001: Export/import through open formats to reduce lock-in | `EOIP-engg-doc-pkg/gaps-implementation.md:52`; audit line 1430 | P2 | IMPLEMENTED-UNVERIFIED | [CP-25](#cp-25) | subject triage | PROVE |
| `REQ-NFR-646` | `GAP-QI-002`: GAP-QI-002: Cost estimation | `EOIP-engg-doc-pkg/gaps-requirements.md:874`; audit line 1441 | P1 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-NFR-647` | `GAP-QI-005`: GAP-QI-005: Suggested indexes | `EOIP-engg-doc-pkg/gaps-requirements.md:877`; audit line 1444 | P1 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-NFR-648` | `GAP-QI-006`: GAP-QI-006: Traversal-risk detector | `EOIP-engg-doc-pkg/gaps-requirements.md:878`; audit line 1445 | P1 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-NFR-649` | `GAP-RULE`: Deterministic rules engine | `requirements-registry.json:1`; audit line 1458 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-650` | `GAP-SDT-002`: GAP-SDT-002: Support forward and reverse navigation | `EOIP-engg-doc-pkg/gaps-requirements.md:382`; audit line 1463 | P0 | IMPLEMENTED-UNVERIFIED | [CP-24](#cp-24) | subject triage | PROVE |
| `REQ-NFR-651` | `GAP-SDT-004`: GAP-SDT-004: Provide missing-link detection | `EOIP-engg-doc-pkg/gaps-requirements.md:384`; audit line 1465 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-652` | `GAP-TAX-001`: GAP-TAX-001: Add enterprise taxonomy/thesaurus management using SKOS-compatible concepts | `EOIP-engg-doc-pkg/gaps-implementation.md:297`; audit line 1496 | P1 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-NFR-653` | `GAP-TEMP-004`: GAP-TEMP-004: Support historical topology reconstruction | `EOIP-engg-doc-pkg/gaps-requirements.md:571`; audit line 1501 | P1 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-NFR-654` | `GAP-TEMPLATE`: Industry templates | `requirements-registry.json:1`; audit line 1504 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-655` | `GAP-TRUST-001`: GAP-TRUST-001: New/inferred/untrusted knowledge enters a quarantine zone | `EOIP-engg-doc-pkg/gaps-implementation.md:295`; audit line 1506 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-656` | `GAP-TRUST-002`: GAP-TRUST-002: Promotion requires rules, confidence or approval | `EOIP-engg-doc-pkg/gaps-requirements.md:751`; audit line 1507 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-657` | `GAP-TRUST-003`: GAP-TRUST-003: Trust states: | `EOIP-engg-doc-pkg/gaps-requirements.md:752`; audit line 1508 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-658` | `GAP-TRUST-004`: GAP-TRUST-004: Queries may specify minimum trust level | `EOIP-engg-doc-pkg/gaps-requirements.md:760`; audit line 1509 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-659` | `GAP-TRUST-005`: GAP-TRUST-005: AI answers must disclose use of non-certified knowledge | `EOIP-engg-doc-pkg/gaps-requirements.md:761`; audit line 1510 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-660` | `GAP-TRUTH-001`: GAP-TRUTH-001: Do not overwrite conflicting claims | `EOIP-engg-doc-pkg/gaps-implementation.md:294`; audit line 1511 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-661` | `GAP-TRUTH-002`: GAP-TRUTH-002: Represent claims separately from resolved canonical facts | `EOIP-engg-doc-pkg/gaps-requirements.md:471`; audit line 1512 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-662` | `GAP-TRUTH-005`: GAP-TRUTH-005: Store validation confidence | `EOIP-engg-doc-pkg/gaps-requirements.md:474`; audit line 1515 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-663` | `GAP-TRUTH-006`: GAP-TRUTH-006: Detect contradictory claims | `EOIP-engg-doc-pkg/gaps-requirements.md:475`; audit line 1516 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-664` | `GAP-TRUTH-007`: GAP-TRUTH-007: Support configurable truth-resolution policy | `EOIP-engg-doc-pkg/gaps-requirements.md:476`; audit line 1517 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-665` | `GAP-TRUTH-008`: GAP-TRUTH-008: Permit human adjudication | `EOIP-engg-doc-pkg/gaps-requirements.md:477`; audit line 1518 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-666` | `GAP-TRUTH-010`: GAP-TRUTH-010: Explain why a canonical fact was selected | `EOIP-engg-doc-pkg/gaps-requirements.md:479`; audit line 1520 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-667` | `H-05`: Configuration validation | `KGF-MASTER-BACKLOG.md:277`; audit line 1564 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-668` | `INFRA-001`: Multi-Level Caching | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:537`; audit line 1568 | P1 | IMPLEMENTED-UNVERIFIED | [CP-03](#cp-03) | engine family | PROVE |
| `REQ-NFR-669` | `INFRA-001.2`: - [x] `INFRA-001.2` Read-through and write-through strategies | `eoip-phase4-2-requirements.md:811`; audit line 1570 | UNSTATED | MISSED | [CP-03](#cp-03) | engine family | TRACE/BUILD |
| `REQ-NFR-670` | `INFRA-001.5`: - [x] `INFRA-001.5` Unit tests | `eoip-phase4-2-requirements.md:814`; audit line 1573 | UNSTATED | MISSED | [CP-03](#cp-03) | engine family | TRACE/BUILD |
| `REQ-NFR-671` | `INFRA-002.4`: - [x] `INFRA-002.4` JWT token validation | `eoip-phase4-2-requirements.md:837`; audit line 1578 | UNSTATED | MISSED | [CP-04](#cp-04) | engine family | TRACE/BUILD |
| `REQ-NFR-672` | `INFRA-002.5`: - [x] `INFRA-002.5` Unit tests | `eoip-phase4-2-requirements.md:838`; audit line 1579 | UNSTATED | MISSED | [CP-04](#cp-04) | engine family | TRACE/BUILD |
| `REQ-NFR-673` | `INFRA-003.1`: - [x] `INFRA-003.1` ArgoCD Application manifests | `eoip-phase4-2-requirements.md:858`; audit line 1581 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-NFR-674` | `INFRA-003.2`: - [x] `INFRA-003.2` Staging and production environment configs | `eoip-phase4-2-requirements.md:859`; audit line 1582 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-NFR-675` | `INFRA-003.5`: - [x] `INFRA-003.5` Automated rollback | `eoip-phase4-2-requirements.md:862`; audit line 1585 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-NFR-676` | `INFRA-004`: Log Aggregation | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:599`; audit line 1586 | P2 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | engine family | PROVE |
| `REQ-NFR-677` | `INFRA-004.2`: - [x] `INFRA-004.2` Correlation ID propagation | `eoip-phase4-2-requirements.md:882`; audit line 1588 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-NFR-678` | `INFRA-004.3`: - [x] `INFRA-004.3` Per-module log level control | `eoip-phase4-2-requirements.md:883`; audit line 1589 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-NFR-679` | `INFRA-004.4`: - [x] `INFRA-004.4` Loki-compatible format | `eoip-phase4-2-requirements.md:884`; audit line 1590 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-NFR-680` | `INFRA-004.5`: - [x] `INFRA-004.5` Unit tests | `eoip-phase4-2-requirements.md:885`; audit line 1591 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-NFR-681` | `INFRA-005.1`: - [x] `INFRA-005.1` Leader election mechanism | `eoip-phase4-2-requirements.md:904`; audit line 1593 | UNSTATED | MISSED | [CP-10](#cp-10) | engine family | TRACE/BUILD |
| `REQ-NFR-682` | `INFRA-005.3`: - [x] `INFRA-005.3` Task dependency DAGs | `eoip-phase4-2-requirements.md:906`; audit line 1595 | UNSTATED | MISSED | [CP-10](#cp-10) | engine family | TRACE/BUILD |
| `REQ-NFR-683` | `INFRA-005.5`: - [x] `INFRA-005.5` Unit tests | `eoip-phase4-2-requirements.md:908`; audit line 1597 | UNSTATED | MISSED | [CP-10](#cp-10) | engine family | TRACE/BUILD |
| `REQ-NFR-684` | `INFRA-006.2`: - [x] `INFRA-006.2` Deprecation headers | `eoip-phase4-2-requirements.md:926`; audit line 1600 | UNSTATED | MISSED | [CP-07](#cp-07) | engine family | TRACE/BUILD |
| `REQ-NFR-685` | `INFRA-007.5`: - [x] `INFRA-007.5` Unit tests | `eoip-phase4-2-requirements.md:952`; audit line 1609 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-NFR-686` | `KGR-G-001`: Polyglot Cross-Repository AST Linker | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:27`; audit line 1610 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-NFR-687` | `KGR-G-003`: Obsidian Vault & Interactive Knowledge Artifact Generator | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:29`; audit line 1612 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-NFR-688` | `KGR-G-007`: Autonomous Self-Healing Active Fabric & Governance Approvals | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:43`; audit line 1616 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-NFR-689` | `KGR-G-010`: Continuous Compliance Twin & AI-BOM Synthesizer | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:48`; audit line 1619 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-NFR-690` | `KGR-G-011`: Formal Behavioral Verification at Merge Gate | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:251`; audit line 1620 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-NFR-691` | `KGR-G-012`: Incremental Differential AST Re-Index (Git Hook Integration) | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:251`; audit line 1621 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-NFR-692` | `KGR-G-018`: Massively Parallel Deep Multi-Hop Analytics Engine (5+ Hops) | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:314`; audit line 1627 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-NFR-693` | `KGR-G-021`: Enterprise Control Loops Governance Engine | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:169`; audit line 1630 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-NFR-694` | `KGR-G-027`: Brain OS Kernel Dual-Route Answering Engine | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:169`; audit line 1636 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-NFR-695` | `KGR-G-PLAN-V1.0`: **Document ID:** EOIP-ENGG-KGR-G-PLAN-V1.0 | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:3`; audit line 1637 | UNSTATED | MISSED | [CP-00](#cp-00) | ID family | TRACE/BUILD |
| `REQ-NFR-696` | `KGR-G-REQ-V2.0`: **Document ID:** EOIP-ENGG-KGR-G-REQ-V2.0 | `EOIP-engg-doc-pkg/KGR-g-requirements.md:3`; audit line 1638 | UNSTATED | MISSED | [CP-00](#cp-00) | ID family | TRACE/BUILD |
| `REQ-NFR-697` | `MS-1`: Diamond Moonshot Baseline #1 | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:377`; audit line 1639 | P0 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-698` | `MS-10`: Diamond Moonshot Baseline #10 | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:325`; audit line 1640 | P0 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-699` | `MS-11`: Universal Plugin & Extension Marketplace | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:8`; audit line 1641 | P1 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | explicit | PROVE |
| `REQ-NFR-700` | `MS-14`: Zero-Friction Self-Service Onboarding AI Wizard | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:33`; audit line 1644 | P1 | IMPLEMENTED-UNVERIFIED | [CP-24](#cp-24) | explicit | PROVE |
| `REQ-NFR-701` | `MS-2`: Diamond Moonshot Baseline #2 | `EOIP-engg-doc-pkg/KGR-g-requirements.md:66`; audit line 1650 | P0 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-702` | `MS-23`: Living Operational Digital Twin of the Enterprise | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:384`; audit line 1654 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-703` | `MS-25`: Industry Intelligence Domain Packs | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:27`; audit line 1656 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-704` | `MS-3`: Diamond Moonshot Baseline #3 | `EOIP-engg-doc-pkg/KGR-g-requirements.md:66`; audit line 1661 | P0 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-705` | `MS-4`: Diamond Moonshot Baseline #4 | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:383`; audit line 1663 | P0 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-706` | `MS-5`: Diamond Moonshot Baseline #5 | `EOIP-engg-doc-pkg/KGR-g-requirements.md:66`; audit line 1664 | P0 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-707` | `MS-6`: Diamond Moonshot Baseline #6 | `EOIP-engg-doc-pkg/KGR-g-requirements.md:174`; audit line 1665 | P0 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-708` | `MS-7`: Diamond Moonshot Baseline #7 | `EOIP-engg-doc-pkg/KGR-g-requirements.md:175`; audit line 1666 | P0 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-709` | `MS-8`: Diamond Moonshot Baseline #8 | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:317`; audit line 1667 | P0 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-710` | `MS-9`: Diamond Moonshot Baseline #9 | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:383`; audit line 1668 | P0 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-NFR-711` | `MULTI-001`: Scoped Multi-Modal Engineering | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:970`; audit line 1670 | P3 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | engine family | PROVE |
| `REQ-NFR-712` | `MULTI-001.3`: - [x] `MULTI-001.3` Integration with fileparse engine | `eoip-phase4-2-requirements.md:1336`; audit line 1673 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-NFR-713` | `MULTI-002.4`: - [x] `MULTI-002.4` Unit tests | `eoip-phase4-2-requirements.md:1356`; audit line 1678 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-NFR-714` | `MVP-FR-005`: Code parsing | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:103`; audit line 1683 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-715` | `MVP-FR-006`: Canonical entity generation | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:104`; audit line 1684 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-716` | `MVP-FR-01`: - **MVP Functional Requirements:** 28 requirements (`MVP-FR-01` through `MVP-FR-28`) — *100% Implemented & Verified* | `EOIP-engg-doc-pkg/KGR-g-requirements.md:72`; audit line 1688 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-717` | `MVP-FR-019`: VS Code extension | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:117`; audit line 1698 | P0 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | subject triage | PROVE |
| `REQ-NFR-718` | `MVP-FR-027`: Automated tests | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:125`; audit line 1706 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-719` | `MVP-FR-028`: End-to-end demo | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:126`; audit line 1707 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-720` | `MVP-FR-28`: - **MVP Functional Requirements:** 28 requirements (`MVP-FR-01` through `MVP-FR-28`) — *100% Implemented & Verified* | `EOIP-engg-doc-pkg/KGR-g-requirements.md:72`; audit line 1708 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-721` | `NFR-01`: - **Non-Functional Requirements:** 14 requirements (`NFR-01` through `NFR-14`) — *100% Implemented & Verified* | `EOIP-engg-doc-pkg/KGR-g-requirements.md:71`; audit line 1725 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-722` | `NFR-06`: &#124; NFR-06 &#124; Usability &#124; MVP workflows must be directly usable without relying on marketing pages or unsupported manual steps. &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1098`; audit line 1730 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-NFR-723` | `NFR-14`: - **Non-Functional Requirements:** 14 requirements (`NFR-01` through `NFR-14`) — *100% Implemented & Verified* | `EOIP-engg-doc-pkg/KGR-g-requirements.md:71`; audit line 1731 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-724` | `NFR-KGR-002`: ### NFR-KGR-002: Responsiveness | `EOIP-engg-doc-pkg/KGR-requirements.md:713`; audit line 1733 | UNSTATED | MISSED | [CP-32](#cp-32) | ID family | TRACE/BUILD |
| `REQ-NFR-725` | `NFR-KGR-003`: ### NFR-KGR-003: Accessibility | `EOIP-engg-doc-pkg/KGR-requirements.md:718`; audit line 1734 | UNSTATED | MISSED | [CP-32](#cp-32) | ID family | TRACE/BUILD |
| `REQ-NFR-726` | `NFR-KGR-004`: ### NFR-KGR-004: Browser Support | `EOIP-engg-doc-pkg/KGR-requirements.md:726`; audit line 1735 | UNSTATED | MISSED | [CP-32](#cp-32) | ID family | TRACE/BUILD |
| `REQ-NFR-727` | `NFR-MAINT-001`: Modular monolith boundary | `EOIP-engg-doc-pkg/04-non-functional-requirements.md:131`; audit line 1737 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-728` | `NFR-OPS-001`: Structured logging and health | `EOIP-engg-doc-pkg/04-non-functional-requirements.md:101`; audit line 1738 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-729` | `NFR-OPS-002`: Local metrics | `EOIP-engg-doc-pkg/04-non-functional-requirements.md:111`; audit line 1739 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-730` | `NFR-PERF-001`: Benchmark-defined objectives | `EOIP-engg-doc-pkg/04-non-functional-requirements.md:121`; audit line 1740 | P0 | IMPLEMENTED-UNVERIFIED | [CP-32](#cp-32) | ID family | PROVE |
| `REQ-NFR-731` | `NFR-PRIV-001`: Data minimization and classification | `EOIP-engg-doc-pkg/04-non-functional-requirements.md:141`; audit line 1741 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-732` | `NFR-REL-001`: Restart-safe processing | `EOIP-engg-doc-pkg/04-non-functional-requirements.md:81`; audit line 1742 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-733` | `NFR-REL-002`: Backup and restore | `EOIP-engg-doc-pkg/04-non-functional-requirements.md:91`; audit line 1743 | P0 | IMPLEMENTED-UNVERIFIED | [CP-31](#cp-31) | subject triage | PROVE |
| `REQ-NFR-734` | `NFR-SEC-001`: No outbound enterprise-data egress | `EOIP-engg-doc-pkg/04-non-functional-requirements.md:11`; audit line 1744 | P0 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | subject triage | PROVE |
| `REQ-NFR-735` | `NFR-SEC-002`: Secret isolation | `EOIP-engg-doc-pkg/04-non-functional-requirements.md:21`; audit line 1745 | P0 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | subject triage | PROVE |
| `REQ-NFR-736` | `NFR-SEC-003`: Input/file safety | `EOIP-engg-doc-pkg/04-non-functional-requirements.md:31`; audit line 1746 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-737` | `NFR-SEC-004`: Prompt/tool injection defenses | `EOIP-engg-doc-pkg/04-non-functional-requirements.md:41`; audit line 1747 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-738` | `NFR-SEC-005`: Authentication without MVP RBAC | `EOIP-engg-doc-pkg/04-non-functional-requirements.md:51`; audit line 1748 | P0 | IMPLEMENTED-UNVERIFIED | [CP-04](#cp-04) | subject triage | PROVE |
| `REQ-NFR-739` | `NFR-SEC-006`: Container hardening | `EOIP-engg-doc-pkg/04-non-functional-requirements.md:61`; audit line 1749 | P0 | IMPLEMENTED-UNVERIFIED | [CP-31](#cp-31) | subject triage | PROVE |
| `REQ-NFR-740` | `NFR-SEC-007`: Audit events | `EOIP-engg-doc-pkg/04-non-functional-requirements.md:71`; audit line 1750 | P0 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-741` | `PRE-001`: Pre-flight: package-collision and baseline reconciliation | `eoip-phase4-2-requirements.md:18`; audit line 1752 | P0 | MISSED | [CP-00](#cp-00) | ID family | TRACE/BUILD |
| `REQ-NFR-742` | `PRE-002.3`: - [x] `PRE-002.3` The Universal Definition of Done (section 4) is copied into the pull-request template. | `eoip-phase4-2-requirements.md:211`; audit line 1761 | UNSTATED | MISSED | [CP-00](#cp-00) | ID family | TRACE/BUILD |
| `REQ-NFR-743` | `PRE-002.4`: - [x] `PRE-002.4` For each "merge" overlap, the owning ID is recorded; the other ID is closed by reference when the shared implementation passes. | `eoip-phase4-2-requirements.md:212`; audit line 1762 | UNSTATED | MISSED | [CP-00](#cp-00) | ID family | TRACE/BUILD |
| `REQ-NFR-744` | `REL-02`: Full regression green on the final tree | `KGF-MASTER-BACKLOG.md:1216`; audit line 1764 | P0 | IMPLEMENTED-UNVERIFIED | [CP-36](#cp-36) | ID family | PROVE |
| `REQ-NFR-745` | `REL-03`: GAP and G2 P0 coverage gates pass | `KGF-MASTER-BACKLOG.md:1218`; audit line 1765 | P0 | IMPLEMENTED-UNVERIFIED | [CP-36](#cp-36) | ID family | PROVE |
| `REQ-NFR-746` | `REL-04`: Product capability scanner first-choice gate passes | `KGF-MASTER-BACKLOG.md:292`; audit line 1766 | P0 | IMPLEMENTED-UNVERIFIED | [CP-36](#cp-36) | ID family | PROVE |
| `REQ-NFR-747` | `REL-09`: VS Code extension-host verification against the current backend | `KGF-MASTER-BACKLOG.md:161`; audit line 1771 | P0 | IMPLEMENTED-UNVERIFIED | [CP-36](#cp-36) | ID family | PROVE |
| `REQ-NFR-748` | `REL-13`: Link-check pass on all non-historical docs | `KGF-MASTER-BACKLOG.md:247`; audit line 1775 | P0 | IMPLEMENTED-UNVERIFIED | [CP-36](#cp-36) | ID family | PROVE |
| `REQ-NFR-749` | `REL-14`: End-to-end demo on the final build | `KGF-MASTER-BACKLOG.md:1249`; audit line 1776 | P0 | IMPLEMENTED-UNVERIFIED | [CP-36](#cp-36) | ID family | PROVE |
| `REQ-NFR-750` | `S-01`: Frontend KGR completion | `requirements-registry.json:1`; audit line 1779 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-751` | `SDLC-001.4`: - [ ] `SDLC-001.4` Check runs in under 30 seconds | `eoip-phase4-2-requirements.md:1412`; audit line 1788 | UNSTATED | MISSED | [CP-00](#cp-00) | engine family | TRACE/BUILD |
| `REQ-NFR-752` | `SDLC-002`: ###### SDLC-002: Architecture decision records and decision register | `eoip-phase4-2-requirements.md:1414`; audit line 1789 | UNSTATED | MISSED | [CP-01](#cp-01) | engine family | TRACE/BUILD |
| `REQ-NFR-753` | `SDLC-002.1`: - [ ] `SDLC-002.1` ADR template and index exist | `eoip-phase4-2-requirements.md:1428`; audit line 1790 | UNSTATED | MISSED | [CP-01](#cp-01) | engine family | TRACE/BUILD |
| `REQ-NFR-754` | `SDLC-002.2`: - [ ] `SDLC-002.2` Every decided DEC item has an ADR | `eoip-phase4-2-requirements.md:1429`; audit line 1791 | UNSTATED | MISSED | [CP-01](#cp-01) | engine family | TRACE/BUILD |
| `REQ-NFR-755` | `SDLC-003.1`: - [ ] `SDLC-003.1` Template and review checklist | `eoip-phase4-2-requirements.md:1447`; audit line 1795 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-NFR-756` | `SDLC-003.3`: - [ ] `SDLC-003.3` Each threat has a mitigation requirement or an accepted-risk entry | `eoip-phase4-2-requirements.md:1449`; audit line 1797 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-NFR-757` | `SDLC-003.4`: - [ ] `SDLC-003.4` Abuse-case tests exist for the top threats | `eoip-phase4-2-requirements.md:1450`; audit line 1798 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-NFR-758` | `SDLC-004.2`: - [ ] `SDLC-004.2` Existing engines migrated or explicitly exempted | `eoip-phase4-2-requirements.md:1469`; audit line 1801 | UNSTATED | MISSED | [CP-07](#cp-07) | engine family | TRACE/BUILD |
| `REQ-NFR-759` | `SDLC-004.4`: - [ ] `SDLC-004.4` New engines add zero lines to brain_os.py/platform_router.py | `eoip-phase4-2-requirements.md:1471`; audit line 1803 | UNSTATED | MISSED | [CP-07](#cp-07) | engine family | TRACE/BUILD |
| `REQ-NFR-760` | `SDLC-005.1`: - [ ] `SDLC-005.1` Container and factory pattern exist | `eoip-phase4-2-requirements.md:1487`; audit line 1805 | UNSTATED | MISSED | [CP-06](#cp-06) | engine family | TRACE/BUILD |
| `REQ-NFR-761` | `SDLC-005.4`: - [ ] `SDLC-005.4` Migration notes for existing singletons | `eoip-phase4-2-requirements.md:1490`; audit line 1808 | UNSTATED | MISSED | [CP-06](#cp-06) | engine family | TRACE/BUILD |
| `REQ-NFR-762` | `SDLC-006`: ###### SDLC-006: Feature flags and kill switches | `eoip-phase4-2-requirements.md:1492`; audit line 1809 | UNSTATED | MISSED | [CP-28](#cp-28) | engine family | TRACE/BUILD |
| `REQ-NFR-763` | `SDLC-006.2`: - [ ] `SDLC-006.2` Kill switch tested for CORE-002, CORE-003 and INFRA-001 | `eoip-phase4-2-requirements.md:1507`; audit line 1811 | UNSTATED | MISSED | [CP-28](#cp-28) | engine family | TRACE/BUILD |
| `REQ-NFR-764` | `SDLC-006.3`: - [ ] `SDLC-006.3` Flags evaluated in under 1 ms | `eoip-phase4-2-requirements.md:1508`; audit line 1812 | UNSTATED | MISSED | [CP-28](#cp-28) | engine family | TRACE/BUILD |
| `REQ-NFR-765` | `SDLC-007.1`: - [ ] `SDLC-007.1` Migration runner with dry-run and rollback | `eoip-phase4-2-requirements.md:1525`; audit line 1815 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-NFR-766` | `SDLC-007.2`: - [ ] `SDLC-007.2` Each new durable store ships with a migration | `eoip-phase4-2-requirements.md:1526`; audit line 1816 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-NFR-767` | `SDLC-008.3`: - [ ] `SDLC-008.3` SLA breach escalates | `eoip-phase4-2-requirements.md:1546`; audit line 1822 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-NFR-768` | `SDLC-009`: ###### SDLC-009: Resilience patterns library: backpressure, load shedding, bulkheads | `eoip-phase4-2-requirements.md:1549`; audit line 1824 | UNSTATED | MISSED | [CP-10](#cp-10) | engine family | TRACE/BUILD |
| `REQ-NFR-769` | `SDLC-009.1`: - [ ] `SDLC-009.1` Library with unit tests | `eoip-phase4-2-requirements.md:1563`; audit line 1825 | UNSTATED | MISSED | [CP-10](#cp-10) | engine family | TRACE/BUILD |
| `REQ-NFR-770` | `SDLC-009.4`: - [ ] `SDLC-009.4` Shedding preserves P0 traffic classes | `eoip-phase4-2-requirements.md:1566`; audit line 1828 | P0 | MISSED | [CP-10](#cp-10) | engine family | TRACE/BUILD |
| `REQ-NFR-771` | `SDLC-010.2`: - [ ] `SDLC-010.2` New packages pass strict typing | `eoip-phase4-2-requirements.md:1585`; audit line 1831 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-NFR-772` | `SDLC-010.3`: - [ ] `SDLC-010.3` Layering contract file exists and is enforced | `eoip-phase4-2-requirements.md:1586`; audit line 1832 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-NFR-773` | `SDLC-010.4`: - [ ] `SDLC-010.4` Pre-commit config documented | `eoip-phase4-2-requirements.md:1587`; audit line 1833 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-NFR-774` | `SDLC-011`: ###### SDLC-011: Coverage measurement and changed-lines gate | `eoip-phase4-2-requirements.md:1589`; audit line 1834 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-NFR-775` | `SDLC-011.2`: - [ ] `SDLC-011.2` Changed-lines gate enforced | `eoip-phase4-2-requirements.md:1603`; audit line 1836 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-NFR-776` | `SDLC-011.3`: - [ ] `SDLC-011.3` Critical engines have thresholds | `eoip-phase4-2-requirements.md:1604`; audit line 1837 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-NFR-777` | `SDLC-011.4`: - [ ] `SDLC-011.4` Baseline recorded | `eoip-phase4-2-requirements.md:1605`; audit line 1838 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-NFR-778` | `SDLC-012.1`: - [ ] `SDLC-012.1` Generator with seeds and size presets | `eoip-phase4-2-requirements.md:1621`; audit line 1840 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-NFR-779` | `SDLC-012.4`: - [ ] `SDLC-012.4` Documented data shapes | `eoip-phase4-2-requirements.md:1624`; audit line 1843 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-NFR-780` | `SDLC-013.1`: - [ ] `SDLC-013.1` Zero unexplained skips | `eoip-phase4-2-requirements.md:1640`; audit line 1845 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-NFR-781` | `SDLC-013.2`: - [ ] `SDLC-013.2` PR run under a set time budget | `eoip-phase4-2-requirements.md:1641`; audit line 1846 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-NFR-782` | `SDLC-013.3`: - [ ] `SDLC-013.3` Flaky tests tracked | `eoip-phase4-2-requirements.md:1642`; audit line 1847 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-NFR-783` | `SDLC-013.4`: - [ ] `SDLC-013.4` Warnings fixed or whitelisted with reason | `eoip-phase4-2-requirements.md:1643`; audit line 1848 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-NFR-784` | `SDLC-014`: ###### SDLC-014: Mutation testing for correctness-critical engines | `eoip-phase4-2-requirements.md:1645`; audit line 1849 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-NFR-785` | `SDLC-014.1`: - [ ] `SDLC-014.1` Nightly job on named packages | `eoip-phase4-2-requirements.md:1657`; audit line 1850 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-NFR-786` | `SDLC-014.2`: - [ ] `SDLC-014.2` Score threshold per package | `eoip-phase4-2-requirements.md:1658`; audit line 1851 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-NFR-787` | `SDLC-016`: ###### SDLC-016: Dogfood: manage the platform with the platform | `eoip-phase4-2-requirements.md:1681`; audit line 1859 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-NFR-788` | `SDLC-017.4`: - [ ] `SDLC-017.4` Breaking change fails the build | `eoip-phase4-2-requirements.md:1717`; audit line 1868 | UNSTATED | MISSED | [CP-29](#cp-29) | engine family | TRACE/BUILD |
| `REQ-NFR-789` | `SDLC-018`: ###### SDLC-018: Continuous browser E2E and visual regression | `eoip-phase4-2-requirements.md:1719`; audit line 1869 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-NFR-790` | `SDLC-018.3`: - [ ] `SDLC-018.3` Flake budget defined | `eoip-phase4-2-requirements.md:1734`; audit line 1872 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-NFR-791` | `SDLC-018.4`: - [ ] `SDLC-018.4` Runs against the compose stack | `eoip-phase4-2-requirements.md:1735`; audit line 1873 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-NFR-792` | `SDLC-019`: ###### SDLC-019: Soak, endurance and leak testing | `eoip-phase4-2-requirements.md:1737`; audit line 1874 | UNSTATED | MISSED | [CP-32](#cp-32) | engine family | TRACE/BUILD |
| `REQ-NFR-793` | `SDLC-019.1`: - [ ] `SDLC-019.1` Soak scenarios for loops, scheduler and bus | `eoip-phase4-2-requirements.md:1749`; audit line 1875 | UNSTATED | MISSED | [CP-32](#cp-32) | engine family | TRACE/BUILD |
| `REQ-NFR-794` | `SDLC-019.3`: - [ ] `SDLC-019.3` Run nightly or weekly | `eoip-phase4-2-requirements.md:1751`; audit line 1877 | UNSTATED | MISSED | [CP-32](#cp-32) | engine family | TRACE/BUILD |
| `REQ-NFR-795` | `SDLC-019.4`: - [ ] `SDLC-019.4` Results feed SLOs | `eoip-phase4-2-requirements.md:1752`; audit line 1878 | UNSTATED | MISSED | [CP-32](#cp-32) | engine family | TRACE/BUILD |
| `REQ-NFR-796` | `SDLC-020`: ###### SDLC-020: Upgrade and compatibility matrix | `eoip-phase4-2-requirements.md:1754`; audit line 1879 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-NFR-797` | `SDLC-020.3`: - [ ] `SDLC-020.3` Backward-compat tests for formats and packages | `eoip-phase4-2-requirements.md:1768`; audit line 1882 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-NFR-798` | `SDLC-020.4`: - [ ] `SDLC-020.4` Policy documented | `eoip-phase4-2-requirements.md:1769`; audit line 1883 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-NFR-799` | `SDLC-021.2`: - [ ] `SDLC-021.2` Nightly DAST | `eoip-phase4-2-requirements.md:1785`; audit line 1886 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-NFR-800` | `SDLC-021.3`: - [ ] `SDLC-021.3` Severity-based SLA | `eoip-phase4-2-requirements.md:1786`; audit line 1887 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-NFR-801` | `SDLC-021.4`: - [ ] `SDLC-021.4` Zero critical findings gate | `eoip-phase4-2-requirements.md:1787`; audit line 1888 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-NFR-802` | `SDLC-022.4`: - [ ] `SDLC-022.4` Rollback runbook tested | `eoip-phase4-2-requirements.md:1808`; audit line 1893 | UNSTATED | MISSED | [CP-33](#cp-33) | engine family | TRACE/BUILD |
| `REQ-NFR-803` | `SDLC-023.2`: - [ ] `SDLC-023.2` NetworkPolicies default-deny | `eoip-phase4-2-requirements.md:1825`; audit line 1896 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-NFR-804` | `SDLC-023.4`: - [ ] `SDLC-023.4` HA run documented | `eoip-phase4-2-requirements.md:1827`; audit line 1898 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-NFR-805` | `SDLC-024.2`: - [ ] `SDLC-024.2` Install on a host with no network egress | `eoip-phase4-2-requirements.md:1843`; audit line 1901 | UNSTATED | MISSED | [CP-27](#cp-27) | engine family | TRACE/BUILD |
| `REQ-NFR-806` | `SDLC-024.3`: - [ ] `SDLC-024.3` Signature and checksum verification | `eoip-phase4-2-requirements.md:1844`; audit line 1902 | UNSTATED | MISSED | [CP-27](#cp-27) | engine family | TRACE/BUILD |
| `REQ-NFR-807` | `SDLC-024.4`: - [ ] `SDLC-024.4` Update from bundle N to N+1 | `eoip-phase4-2-requirements.md:1845`; audit line 1903 | UNSTATED | MISSED | [CP-27](#cp-27) | engine family | TRACE/BUILD |
| `REQ-NFR-808` | `SDLC-025.4`: - [ ] `SDLC-025.4` Works with no external backend | `eoip-phase4-2-requirements.md:1866`; audit line 1908 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-NFR-809` | `SDLC-026.1`: - [ ] `SDLC-026.1` SLOs defined for core engines | `eoip-phase4-2-requirements.md:1881`; audit line 1910 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-NFR-810` | `SDLC-026.2`: - [ ] `SDLC-026.2` Runbooks exist and are linked from alerts | `eoip-phase4-2-requirements.md:1882`; audit line 1911 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-NFR-811` | `SDLC-026.3`: - [ ] `SDLC-026.3` Postmortem template | `eoip-phase4-2-requirements.md:1883`; audit line 1912 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-NFR-812` | `SDLC-026.4`: - [ ] `SDLC-026.4` One game day completed | `eoip-phase4-2-requirements.md:1884`; audit line 1913 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-NFR-813` | `SDLC-027`: &#124; Unproven benefits &#124; CORE-001 (30-70% token reduction), CORE-003 (40-60% cost cut, 60-70% of queries cheap, sub-10ms), CORE-006 &#124; Claims in the rationale have no measurement plan in the acceptance criteria. See SDLC-... | `eoip-phase4-2-requirements.md:140`; audit line 1914 | UNSTATED | MISSED | [CP-32](#cp-32) | engine family | TRACE/BUILD |
| `REQ-NFR-814` | `SDLC-027.2`: - [ ] `SDLC-027.2` Budget alerts | `eoip-phase4-2-requirements.md:1901`; audit line 1916 | UNSTATED | MISSED | [CP-32](#cp-32) | engine family | TRACE/BUILD |
| `REQ-NFR-815` | `SDLC-027.4`: - [ ] `SDLC-027.4` Monthly showback export | `eoip-phase4-2-requirements.md:1903`; audit line 1918 | UNSTATED | MISSED | [CP-32](#cp-32) | engine family | TRACE/BUILD |
| `REQ-NFR-816` | `SDLC-028.1`: - [ ] `SDLC-028.1` Data map covers all stores | `eoip-phase4-2-requirements.md:1919`; audit line 1920 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-NFR-817` | `SDLC-028.3`: - [ ] `SDLC-028.3` Retention policy engine | `eoip-phase4-2-requirements.md:1921`; audit line 1922 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-NFR-818` | `SDLC-028.4`: - [ ] `SDLC-028.4` Legal-hold override | `eoip-phase4-2-requirements.md:1922`; audit line 1923 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-NFR-819` | `SDLC-029.1`: - [ ] `SDLC-029.1` Interface with local backend and one external adapter | `eoip-phase4-2-requirements.md:1937`; audit line 1925 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-NFR-820` | `SDLC-029.4`: - [ ] `SDLC-029.4` Consumers migrated | `eoip-phase4-2-requirements.md:1940`; audit line 1928 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-NFR-821` | `SDLC-030.1`: - [ ] `SDLC-030.1` Suite runs for all Phase 4 stateful engines | `eoip-phase4-2-requirements.md:1955`; audit line 1930 | UNSTATED | MISSED | [CP-06](#cp-06) | engine family | TRACE/BUILD |
| `REQ-NFR-822` | `SDLC-030.2`: - [ ] `SDLC-030.2` Fails on a deliberately leaky fixture | `eoip-phase4-2-requirements.md:1956`; audit line 1931 | UNSTATED | MISSED | [CP-06](#cp-06) | engine family | TRACE/BUILD |
| `REQ-NFR-823` | `SDLC-030.3`: - [ ] `SDLC-030.3` Part of the Definition of Done | `eoip-phase4-2-requirements.md:1957`; audit line 1932 | UNSTATED | MISSED | [CP-06](#cp-06) | engine family | TRACE/BUILD |
| `REQ-NFR-824` | `SDLC-031.1`: - [ ] `SDLC-031.1` Profiles measured and published | `eoip-phase4-2-requirements.md:1974`; audit line 1935 | UNSTATED | MISSED | [CP-32](#cp-32) | engine family | TRACE/BUILD |
| `REQ-NFR-825` | `SDLC-031.4`: - [ ] `SDLC-031.4` Sizing guide | `eoip-phase4-2-requirements.md:1977`; audit line 1938 | UNSTATED | MISSED | [CP-32](#cp-32) | engine family | TRACE/BUILD |
| `REQ-NFR-826` | `SDLC-032.3`: - [ ] `SDLC-032.3` Docs site builds from the repo | `eoip-phase4-2-requirements.md:1996`; audit line 1942 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-NFR-827` | `SDLC-033.1`: - [ ] `SDLC-033.1` Fresh clone to running stack in one command | `eoip-phase4-2-requirements.md:2012`; audit line 1945 | UNSTATED | MISSED | [CP-29](#cp-29) | engine family | TRACE/BUILD |
| `REQ-NFR-828` | `SDLC-033.3`: - [ ] `SDLC-033.3` Sample data pack | `eoip-phase4-2-requirements.md:2014`; audit line 1947 | UNSTATED | MISSED | [CP-29](#cp-29) | engine family | TRACE/BUILD |
| `REQ-NFR-829` | `SDLC-034.2`: - [ ] `SDLC-034.2` Whitepaper and data-flow diagrams | `eoip-phase4-2-requirements.md:2030`; audit line 1951 | UNSTATED | MISSED | [CP-33](#cp-33) | engine family | TRACE/BUILD |
| `REQ-NFR-830` | `SDLC-034.3`: - [ ] `SDLC-034.3` DPIA template | `eoip-phase4-2-requirements.md:2031`; audit line 1952 | UNSTATED | MISSED | [CP-33](#cp-33) | engine family | TRACE/BUILD |
| `REQ-NFR-831` | `SR-ARC-007`: &#124; SR-ARC-007 &#124; **Exactly-once effects** via idempotency keys, deterministic IDs and replay-safe mutations; at-least-once delivery acceptable at transport level. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:168`; audit line 1981 | P0 | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-832` | `SR-CFG-003`: &#124; SR-CFG-003 &#124; **Effective-config explain:** "why does this setting have this value?" shows the layer chain and last change. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:749`; audit line 1989 | P0 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-NFR-833` | `SR-CFG-005`: &#124; SR-CFG-005 &#124; **Feature flags and entitlements** distinct from configuration; flags never bypass policy. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:751`; audit line 1991 | P0 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-NFR-834` | `SR-COM-004`: &#124; SR-COM-004 &#124; **Support:** Standard / Priority / Enterprise / Mission-critical tiers with response targets, escalation paths, named technical account managers, support-bundle workflow. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:1003`; audit line 1996 | P0 | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-835` | `SR-COM-008`: &#124; SR-COM-008 &#124; **Sales artifacts:** datasheets per module and industry, battlecards, demo environments, reference architectures, case-study templates. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:1007`; audit line 2000 | P1 | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-836` | `SR-COM-021`: &#124; SR-COM-021 &#124; Ship the Software/IT pack and **two non-IT packs** at GA to prove horizontal applicability; remaining packs on the roadmap (§20). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:1035`; audit line 2004 | P0 | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-837` | `SR-CON-003`: &#124; SR-CON-003 &#124; **No egress by default:** outbound traffic MUST be denied by default via network policy and application-level egress gateway; any permitted egress is allowlisted, logged and attributable. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:100`; audit line 2007 | P0 | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-NFR-838` | `SR-DEP-004`: &#124; SR-DEP-004 &#124; **Appliance image** (hardware + software; CPU and GPU variants) with hardened OS, first-boot wizard, lifecycle updates. &#124; P2 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:925`; audit line 2022 | P2 | MISSED | [CP-31](#cp-31) | ID family | TRACE/BUILD |
| `REQ-NFR-839` | `SR-DEP-005`: &#124; SR-DEP-005 &#124; **Native packages** (RPM/DEB) and VM images for customers without containers. &#124; P2 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:926`; audit line 2023 | P2 | MISSED | [CP-31](#cp-31) | ID family | TRACE/BUILD |
| `REQ-NFR-840` | `SR-DEP-009`: &#124; SR-DEP-009 &#124; **Reference architectures and hardening guides** per profile and tier, including network diagrams for air-gapped and connected variants. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:930`; audit line 2027 | P0 | MISSED | [CP-31](#cp-31) | ID family | TRACE/BUILD |
| `REQ-NFR-841` | `SR-EXT-004`: &#124; SR-EXT-004 &#124; Official SDKs: Python, TypeScript at P0; Java/Kotlin, Go, .NET at P1; Jupyter/notebook integrations. &#124; P0/P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:779`; audit line 2031 | P0 | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-NFR-842` | `SR-GDB-002`: &#124; SR-GDB-002 &#124; Each adapter MUST publish a **Capability Manifest** (example in §5.6). The planner uses it to choose pushdown vs in-engine execution and to refuse or degrade unsupported plans *explicitly* (never silentl... | `EOIP-engg-doc-pkg/super-requirements.md:184`; audit line 2040 | P0 | PARTIAL | [CP-13](#cp-13) | ID family | COMPLETE |
| `REQ-NFR-843` | `SR-GDB-004`: &#124; SR-GDB-004 &#124; **Certification tiers:** Tier A *Certified* (full conformance, benchmarked, HA validated, supported under SLA); Tier B *Compatible* (documented capability gaps); Tier C *Community/Experimental*. Marketin... | `EOIP-engg-doc-pkg/super-requirements.md:186`; audit line 2042 | P0 | PARTIAL | [CP-13](#cp-13) | ID family | COMPLETE |
| `REQ-NFR-844` | `SR-GDB-006`: &#124; SR-GDB-006 &#124; **Online migration** between backends (export → verify counts/checksums/golden queries → dual-write or cutover → rollback) MUST be supported for Tier A pairs. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:188`; audit line 2044 | P1 | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-NFR-845` | `SR-GDB-012`: &#124; SR-GDB-012 &#124; **Object/raw store:** filesystem (DP-0), S3-compatible (clustered), and cloud blob adapters. Raw captures are immutable, content-addressed (SHA-256), encrypted, and retention-managed. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:217`; audit line 2050 | P0 | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-NFR-846` | `SR-GOV-005`: &#124; SR-GOV-005 &#124; **Policy exceptions** are time-boxed, approved, visible and auto-expiring. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:872`; audit line 2059 | P1 | IMPLEMENTED-UNVERIFIED | [CP-00](#cp-00) | area fallback | PROVE |
| `REQ-NFR-847` | `SR-PRV-004`: &#124; SR-PRV-004 &#124; **Purpose and consent tracking** where applicable; purpose limitation enforced in policy. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:851`; audit line 2159 | P1 | PARTIAL | [CP-09](#cp-09) | ID family | COMPLETE |
| `REQ-NFR-848` | `SR-PRV-007`: &#124; SR-PRV-007 &#124; **Pseudonymization/anonymization services** (tokenization, k-anonymity checks, optional differential-privacy aggregates). &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:854`; audit line 2162 | P1 | MISSED | [CP-09](#cp-09) | ID family | TRACE/BUILD |
| `REQ-NFR-849` | `SR-WL-007`: &#124; SR-WL-007 &#124; **Custom legal and onboarding content:** terms, privacy notices, welcome tours, help links. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:739`; audit line 2241 | P0 | PARTIAL | [CP-28](#cp-28) | ID family | COMPLETE |
| `REQ-NFR-850` | `TASK-AIE-007`: - **TASK-AIE-007**: Implement Deep NLP pipeline (AI-002) — extend existing pipeline with sentiment, topic modeling | `EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:41`; audit line 2250 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-851` | `TASK-AIE-009`: - **TASK-AIE-009**: Implement MLOps Experiment Tracker (AI-005) | `EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:49`; audit line 2252 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-852` | `TASK-ARCH-002`: - **TASK-ARCH-002**: Design Token Format Engine (CORE-001) architecture — pluggable format strategy pattern, auto-selection algorithm, round-trip fidelity validation | `EOIP-engg-doc-pkg/roles/Architect_tasks.md:17`; audit line 2258 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-853` | `TASK-ARCH-012`: - **TASK-ARCH-012**: Define engine-to-engine integration patterns (direct call, event bus, shared state) | `EOIP-engg-doc-pkg/roles/Architect_tasks.md:60`; audit line 2268 | UNSTATED | MISSED | [CP-10](#cp-10) | subject triage | TRACE/BUILD |
| `REQ-NFR-854` | `TASK-CEO-001`: - **TASK-CEO-001**: Define and maintain product vision — "Enterprise Cognitive Intelligence Platform" positioning | `EOIP-engg-doc-pkg/roles/CEO_tasks.md:12`; audit line 2274 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-855` | `TASK-CEO-004`: - **TASK-CEO-004**: Define pricing strategy across edition tiers (Community/Professional/Enterprise/OEM) | `EOIP-engg-doc-pkg/roles/CEO_tasks.md:31`; audit line 2277 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-856` | `TASK-CEO-005`: - **TASK-CEO-005**: Prepare Series A/B pitch incorporating 47 Phase 4 features as product moat | `EOIP-engg-doc-pkg/roles/CEO_tasks.md:40`; audit line 2278 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-857` | `TASK-CEO-006`: - **TASK-CEO-006**: Identify and pursue strategic partnerships (cloud providers, system integrators) | `EOIP-engg-doc-pkg/roles/CEO_tasks.md:47`; audit line 2279 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-858` | `TASK-CEO-008`: - **TASK-CEO-008**: Approve go-to-market strategy and launch timeline | `EOIP-engg-doc-pkg/roles/CEO_tasks.md:59`; audit line 2281 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-859` | `TASK-CEO-010`: - **TASK-CEO-010**: Establish customer advisory program for design partners | `EOIP-engg-doc-pkg/roles/CEO_tasks.md:70`; audit line 2283 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-860` | `TASK-CEO-011`: - **TASK-CEO-011**: Hire/contract key roles: VP Engineering, VP Sales, Head of AI | `EOIP-engg-doc-pkg/roles/CEO_tasks.md:76`; audit line 2284 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-861` | `TASK-CEO-012`: - **TASK-CEO-012**: Establish IP protection strategy | `EOIP-engg-doc-pkg/roles/CEO_tasks.md:82`; audit line 2285 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-862` | `TASK-CEO-013`: - **TASK-CEO-013**: Define data residency and sovereignty policy for global enterprise customers | `EOIP-engg-doc-pkg/roles/CEO_tasks.md:90`; audit line 2286 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-863` | `TASK-CTO-001`: - **TASK-CTO-001**: Own and maintain system architecture across 21+ engineering disciplines | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:11`; audit line 2287 | UNSTATED | MISSED | [CP-37](#cp-37) | subject triage | TRACE/BUILD |
| `REQ-NFR-864` | `TASK-CTO-007`: - **TASK-CTO-007**: Technical debt management — prioritize refactoring vs. feature development | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:50`; audit line 2293 | UNSTATED | MISSED | [CP-35](#cp-35) | subject triage | TRACE/BUILD |
| `REQ-NFR-865` | `TASK-CTO-010`: - **TASK-CTO-010**: Validate token format engines (CORE-001) compression ratios against production payloads | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:70`; audit line 2296 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-866` | `TASK-CTO-018`: - **TASK-CTO-018**: Establish feature flag strategy for gradual rollout and experimentation | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:117`; audit line 2304 | UNSTATED | MISSED | [CP-28](#cp-28) | subject triage | TRACE/BUILD |
| `REQ-NFR-867` | `TASK-DM-001`: - **TASK-DM-001**: Create sprint plans for 7 phases of Phase 4 roadmap (47 requirements) | `EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:11`; audit line 2321 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-868` | `TASK-DM-002`: - **TASK-DM-002**: Define Definition of Done (DoD) for each requirement type | `EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:18`; audit line 2322 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-869` | `TASK-DM-011`: - **TASK-DM-011**: Define escalation paths: blocked task → Lead Dev (4h) → CTO (1d) → CEO (2d) | `EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:68`; audit line 2331 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-870` | `TASK-DM-012`: - **TASK-DM-012**: Track phase completion against milestones — flag when behind by >1 sprint | `EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:73`; audit line 2332 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-871` | `TASK-LAI-001`: - **TASK-LAI-001**: Design XAI Engine (AI-001) architecture — explainability framework without SHAP/LIME dependencies | `EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:11`; audit line 2335 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-872` | `TASK-LAI-007`: - **TASK-LAI-007**: Evaluate and optimize hybrid search engine (7 modalities) — relevance tuning, RRF weights | `EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:41`; audit line 2341 | UNSTATED | MISSED | [CP-20](#cp-20) | subject triage | TRACE/BUILD |
| `REQ-NFR-873` | `TASK-LAI-009`: - **TASK-LAI-009**: Design Intent Router classifier (CORE-003) — feature engineering, training data strategy | `EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:51`; audit line 2343 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-874` | `TASK-LAI-010`: - **TASK-LAI-010**: Evaluate reasoning strategy effectiveness (9 strategies) — which strategies perform best for which task types | `EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:56`; audit line 2344 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-875` | `TASK-LAI-011`: - **TASK-LAI-011**: Design A/B testing framework for models (AI-004) | `EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:61`; audit line 2345 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-876` | `TASK-LAI-012`: - **TASK-LAI-012**: Design experiment tracking system (AI-005) — lightweight, no external deps | `EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:65`; audit line 2346 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-877` | `TASK-LD-001`: - **TASK-LD-001**: Implement Token Format Engines (CORE-001) — 7 serialization strategies + auto-selection + benchmarks | `EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:11`; audit line 2351 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-NFR-878` | `TASK-LD-003`: - **TASK-LD-003**: Implement Intent Router (CORE-003) — classifier, routing table, feedback loop, cost integration | `EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:21`; audit line 2353 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-879` | `TASK-LD-005`: - **TASK-LD-005**: Implement Loop-over-Loop (CORE-005) — SupervisoryLoop, LoopMonitor, strategy switching | `EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:30`; audit line 2355 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-880` | `TASK-LD-006`: - **TASK-LD-006**: Implement Token Budget Engineering (CORE-006) — allocation strategies, tracking, reallocation | `EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:35`; audit line 2356 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-881` | `TASK-LD-007`: - **TASK-LD-007**: Establish code review checklist for AI-generated code | `EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:41`; audit line 2357 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-882` | `TASK-LD-008`: - **TASK-LD-008**: Enforce consistent engine pattern across all 21+ discipline engines | `EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:47`; audit line 2358 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-883` | `TASK-LD-010`: - **TASK-LD-010**: Establish Git branching strategy — feature branches, PR reviews, squash merge to dev_local | `EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:56`; audit line 2360 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-884` | `TASK-LD-013`: - **TASK-LD-013**: Review and approve all Phase 4-7 implementations before merge | `EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:69`; audit line 2363 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-885` | `TASK-LEGAL-001`: - **TASK-LEGAL-001**: Patent strategy — identify patentable innovations and file provisional patents | `EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:11`; audit line 2367 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-886` | `TASK-LEGAL-002`: - **TASK-LEGAL-002**: Trademark registration — "EOIP", "KnowGridFlow", "Enterprise Cognitive Intelligence Platform" | `EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:22`; audit line 2368 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-887` | `TASK-LEGAL-008`: - **TASK-LEGAL-008**: Draft Terms of Service for Community edition (SaaS) | `EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:53`; audit line 2374 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-888` | `TASK-LEGAL-009`: - **TASK-LEGAL-009**: Draft Data Processing Agreement (DPA) for GDPR compliance | `EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:57`; audit line 2375 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-889` | `TASK-LEGAL-012`: - **TASK-LEGAL-012**: India DPDP Act compliance — data localization requirements, consent management | `EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:71`; audit line 2378 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-890` | `TASK-LEGAL-014`: - **TASK-LEGAL-014**: Draft partnership agreement template for system integrators and cloud providers | `EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:82`; audit line 2380 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-891` | `TASK-LEGAL-015`: - **TASK-LEGAL-015**: Employee/contractor IP assignment agreements | `EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:86`; audit line 2381 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-892` | `TASK-LIC-001`: - **TASK-LIC-001**: Define feature matrix per edition: Community (free) vs Professional vs Enterprise vs OEM | `EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:11`; audit line 2382 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-NFR-893` | `TASK-MKE-001`: - **TASK-MKE-001**: Write blog series (4-6 posts) on platform differentiators | `EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:11`; audit line 2395 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-894` | `TASK-MKE-002`: - **TASK-MKE-002**: Create product one-pager / datasheet for each edition tier | `EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:17`; audit line 2396 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-895` | `TASK-MKE-003`: - **TASK-MKE-003**: Create technical whitepaper: "Token Economics in Enterprise AI" | `EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:21`; audit line 2397 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-896` | `TASK-MKE-004`: - **TASK-MKE-004**: Create sales deck / presentation template | `EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:25`; audit line 2398 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-897` | `TASK-MKE-006`: - **TASK-MKE-006**: Execute launch campaign — email sequences, social posts, PR outreach | `EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:34`; audit line 2400 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-898` | `TASK-MKE-007`: - **TASK-MKE-007**: Set up marketing automation — email nurture flows, lead scoring, CRM integration | `EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:38`; audit line 2401 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-899` | `TASK-MKE-008`: - **TASK-MKE-008**: Manage social media presence — LinkedIn, Twitter/X, YouTube | `EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:41`; audit line 2402 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-900` | `TASK-MKE-011`: - **TASK-MKE-011**: Prepare conference presentation materials for target events | `EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:53`; audit line 2405 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-901` | `TASK-MKT-001`: - **TASK-MKT-001**: Define GTM strategy — target segments, buyer personas, value propositions per segment | `EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:11`; audit line 2407 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-902` | `TASK-MKT-003`: - **TASK-MKT-003**: Create competitive battlecards for sales enablement | `EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:22`; audit line 2409 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-903` | `TASK-MKT-004`: - **TASK-MKT-004**: Define product-led growth (PLG) strategy for Community edition | `EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:26`; audit line 2410 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-904` | `TASK-MKT-005`: - **TASK-MKT-005**: Create thought leadership content plan — blog series, whitepapers, case studies | `EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:32`; audit line 2411 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-905` | `TASK-MKT-006`: - **TASK-MKT-006**: Create product demo video showcasing key differentiators | `EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:40`; audit line 2412 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-906` | `TASK-MKT-007`: - **TASK-MKT-007**: Develop customer success stories / design partner case studies | `EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:45`; audit line 2413 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-907` | `TASK-MKT-008`: - **TASK-MKT-008**: Define marketing qualified lead (MQL) criteria and nurture workflow | `EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:50`; audit line 2414 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-908` | `TASK-MKT-011`: - **TASK-MKT-011**: Engage industry analysts (Gartner, Forrester) for category validation | `EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:63`; audit line 2417 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-NFR-909` | `TASK-QA-001`: - **TASK-QA-001**: Execute unit tests for Token Format Engines (CORE-001) | `EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:11`; audit line 2421 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-NFR-910` | `TASK-QA-002`: - **TASK-QA-002**: Execute unit tests for Verification Engine (CORE-002) | `EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:15`; audit line 2422 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-NFR-911` | `TASK-QA-003`: - **TASK-QA-003**: Execute unit tests for Intent Router (CORE-003) | `EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:19`; audit line 2423 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-NFR-912` | `TASK-QA-018`: - **TASK-QA-018**: Cross-engine integration — verify Intelligence Engine can orchestrate new engines (token formats, verification, intent routing) | `EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:44`; audit line 2430 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-NFR-913` | `TASK-QAL-008`: - **TASK-QAL-008**: Establish load testing framework (k6 or Locust) with production-realistic scenarios | `EOIP-engg-doc-pkg/roles/QALead_tasks.md:46`; audit line 2441 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-NFR-914` | `TASK-QAL-009`: - **TASK-QAL-009**: Establish chaos engineering framework for fault injection | `EOIP-engg-doc-pkg/roles/QALead_tasks.md:51`; audit line 2442 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-NFR-915` | `TASK-QAL-013`: - **TASK-QAL-013**: Defect triage process — severity classification, fix SLA, root cause analysis | `EOIP-engg-doc-pkg/roles/QALead_tasks.md:71`; audit line 2446 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-NFR-916` | `WP-EXPERIENCE-05`: ### WP-EXPERIENCE-05 — VS Code context extension | `EOIP-engg-doc-pkg/implementation/wp-experience.md:60`; audit line 2644 | UNSTATED | MISSED | [CP-29](#cp-29) | subject triage | TRACE/BUILD |
| `REQ-NFR-917` | `WP-FOUNDATION-04`: ### WP-FOUNDATION-04 — Canonical identifiers | `EOIP-engg-doc-pkg/implementation/wp-foundation.md:50`; audit line 2649 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-918` | `WP-FOUNDATION-05`: ### WP-FOUNDATION-05 — Modular monolith boundary | `EOIP-engg-doc-pkg/implementation/wp-foundation.md:59`; audit line 2650 | UNSTATED | MISSED | [CP-00](#cp-00) | area fallback | TRACE/BUILD |
| `REQ-NFR-919` | `WP-VALIDATION-02`: ### WP-VALIDATION-02 — Validation gates | `EOIP-engg-doc-pkg/implementation/wp-validation.md:30`; audit line 2700 | UNSTATED | MISSED | [CP-17](#cp-17) | ID family | TRACE/BUILD |

### A.14 NLQ: 16 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-NLQ-001` | `GAP-QI-008`: GAP-QI-008: Natural-language query produces editable structured plan before execution when risk is high | `EOIP-engg-doc-pkg/gaps-requirements.md:880`; audit line 1447 | P1 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-NLQ-002` | `SR-NLQ-001`: &#124; SR-NLQ-001 &#124; **Template/semantic-parser tier first:** common intents (§1.2) compile deterministically without an LLM; an LLM-assisted tier handles open-ended phrasing using constrained decoding against the ontology s... | `EOIP-engg-doc-pkg/super-requirements.md:580`; audit line 2122 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-NLQ-003` | `SR-NLQ-002`: &#124; SR-NLQ-002 &#124; **Intelligent suggestion engine (core differentiator):** when a question is ambiguous, under-specified, too broad, or maps to multiple plans, the system MUST present a ranked set of **candidate questions... | `EOIP-engg-doc-pkg/super-requirements.md:581`; audit line 2123 | UNSTATED | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-NLQ-004` | `SR-NLQ-003`: &#124; SR-NLQ-003 &#124; **Entity disambiguation UX:** "service account `abc`" resolving to several entities (dev/prod, duplicates across systems) shows candidates with context and lets the user pin one for the session. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:582`; audit line 2124 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-NLQ-005` | `SR-NLQ-004`: &#124; SR-NLQ-004 &#124; **Answer modes:** (1) *Deterministic* — computed from the graph, exact, no LLM; (2) *Narrated* — deterministic facts + LLM wording; (3) *Exploratory investigation* — multi-step agent with visible plan an... | `EOIP-engg-doc-pkg/super-requirements.md:583`; audit line 2125 | P0 | PARTIAL | [CP-21](#cp-21) | ID family | COMPLETE |
| `REQ-NLQ-006` | `SR-NLQ-005`: &#124; SR-NLQ-005 &#124; **Depth bar ("no shortness"):** answers MUST include, as relevant: direct answer, supporting evidence and paths, assumptions, confidence and uncertainty, alternatives considered, recommended next actions... | `EOIP-engg-doc-pkg/super-requirements.md:584`; audit line 2126 | P0 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-NLQ-007` | `SR-NLQ-006`: &#124; SR-NLQ-006 &#124; **Explainability (XAI):** "why?" on any result returns the paths/rules/premises; counterfactuals ("what would change the answer?"); confidence decomposition (edge confidence, source freshness, coverage).... | `EOIP-engg-doc-pkg/super-requirements.md:585`; audit line 2127 | P0 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-NLQ-008` | `SR-NLQ-007`: &#124; SR-NLQ-007 &#124; **Conversation context:** follow-ups, pronoun/ellipsis resolution, session and saved-investigation memory, pinned entities, branching ("explore alternative"), shareable investigation links respecting eac... | `EOIP-engg-doc-pkg/super-requirements.md:586`; audit line 2128 | P0 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-NLQ-009` | `SR-NLQ-008`: &#124; SR-NLQ-008 &#124; **Reports:** templates (impact assessment, incident RCA, change-risk review, compliance evidence, executive brief), scheduled/recurring, parameterized, multi-format export (HTML, PDF, DOCX, PPTX, Markdow... | `EOIP-engg-doc-pkg/super-requirements.md:587`; audit line 2129 | P0 | STUBBED | [CP-25](#cp-25) | explicit | REPLACE |
| `REQ-NLQ-010` | `SR-NLQ-009`: &#124; SR-NLQ-009 &#124; **Languages:** English at P0; multilingual NL (major European, Indic and East-Asian languages) via local multilingual models at P1, with glossary-term translation. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:588`; audit line 2130 | P0 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-NLQ-011` | `SR-NLQ-010`: &#124; SR-NLQ-005 &#124; **Depth bar ("no shortness"):** answers MUST include, as relevant: direct answer, supporting evidence and paths, assumptions, confidence and uncertainty, alternatives considered, recommended next actions... | `EOIP-engg-doc-pkg/super-requirements.md:584`; audit line 2131 | P0 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-NLQ-012` | `SR-NLQ-011`: &#124; SR-NLQ-011 &#124; **Safety:** refuse or constrain questions the user is not entitled to; never reveal existence of hidden entities ("redaction notice" lists the *fact* that filters applied, not the content). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:590`; audit line 2132 | P0 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-NLQ-013` | `SR-NLQ-012`: &#124; SR-NLQ-012 &#124; **Feedback loop:** thumbs/corrections/"this edge is wrong" feed a curation queue that improves mappings, aliases, intent templates and ranking, with steward approval. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:591`; audit line 2133 | P1 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-NLQ-014` | `SR-NLQ-013`: &#124; SR-NLQ-013 &#124; **Voice and chat surfaces:** same pipeline via chat apps (Teams/Slack-class), IDE chat, CLI, and optional speech I/O. &#124; P2 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:592`; audit line 2134 | P2 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-NLQ-015` | `SR-NLQ-014`: &#124; SR-NLQ-014 &#124; **What-if simulation:** sandboxed copy-on-write overlay graph where users propose changes (delete service, rotate account, add dependency) and see propagated impact before acting; overlay never alters pr... | `EOIP-engg-doc-pkg/super-requirements.md:593`; audit line 2135 | P1 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-NLQ-016` | `SR-NLQ-015`: &#124; SR-NLQ-015 &#124; **Proactive suggestions:** based on role, current entity and usage graph, the UI proposes "questions you might ask next" (e.g., owners to notify, tests to run). &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:594`; audit line 2136 | P1 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |

### A.15 OBS: 44 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-OBS-001` | `AI-004.4`: - [x] `AI-004.4` Comparison metrics | `eoip-phase4-2-requirements.md:722`; audit line 279 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-OBS-002` | `AI-005.2`: - [x] `AI-005.2` Parameter and metric logging | `eoip-phase4-2-requirements.md:742`; audit line 283 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-OBS-003` | `CORE-001.6`: - [x] `CORE-001.6` Wired into `brain_os.py` telemetry and `platform_router.py` endpoints | `eoip-phase4-2-requirements.md:240`; audit line 422 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-OBS-004` | `CORE-005.2`: - [x] `CORE-005.2` LoopMonitor with real-time metrics | `eoip-phase4-2-requirements.md:353`; audit line 453 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-OBS-005` | `FR-08`: &#124; FR-08 &#124; Product packaging &#124; Documentation index, traceability, decisions/ADRs, assumptions, risk register, license/SBOM awareness, demo readiness, and reconstruction instructions. &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1087`; audit line 502 | UNSTATED | MISSED | [CP-33](#cp-33) | subject triage | TRACE/BUILD |
| `REQ-OBS-006` | `G2-OBS-001`: G2-OBS-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:141`; audit line 783 | P1 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-OBS-007` | `G2-OBS-002`: G2-OBS-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1705`; audit line 784 | P1 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-OBS-008` | `G2-OBS-003`: G2-OBS-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1714`; audit line 785 | P1 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-OBS-009` | `G2-OBS-004`: G2-OBS-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1720`; audit line 786 | P1 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-OBS-010` | `G2-OBS-005`: G2-OBS-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1723`; audit line 787 | P1 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-OBS-011` | `G2-OBS-006`: G2-OBS-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1726`; audit line 788 | P1 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-OBS-012` | `G2-T0006`: ### G2-T0006 — Traceability | `EOIP-engg-doc-pkg/gaps2-implementation.md:119`; audit line 954 | UNSTATED | MISSED | [CP-30](#cp-30) | area fallback | TRACE/BUILD |
| `REQ-OBS-013` | `GAP-ENG-001`: GAP-ENG-001: Make requirement-to-code-to-runtime traceability a native differentiator rather than an external integration | `EOIP-engg-doc-pkg/gaps-requirements.md:121`; audit line 1290 | P2 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | area fallback | PROVE |
| `REQ-OBS-014` | `GAP-OBS-001`: GAP-OBS-001: Trace a request from UI → API → planner → HugeGraph → retriever → model → response | `EOIP-engg-doc-pkg/gaps-implementation.md:54`; audit line 1420 | P1 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-OBS-015` | `GAP-OBS-002`: GAP-OBS-002: Trace ingestion from source record → entity → edge → index | `EOIP-engg-doc-pkg/gaps-requirements.md:856`; audit line 1421 | P1 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-OBS-016` | `GAP-OBS-003`: GAP-OBS-003: Metrics per connector/query/agent/retriever | `EOIP-engg-doc-pkg/gaps-requirements.md:857`; audit line 1422 | P1 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-OBS-017` | `GAP-OBS-004`: GAP-OBS-004: Correlate logs, metrics and traces | `EOIP-engg-doc-pkg/gaps-requirements.md:858`; audit line 1423 | P1 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-OBS-018` | `GAP-OBS-005`: GAP-OBS-005: Graph-specific metrics: | `EOIP-engg-doc-pkg/gaps-requirements.md:859`; audit line 1424 | P1 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | ID family | PROVE |
| `REQ-OBS-019` | `GAP-SDT-005`: GAP-SDT-005: Generate traceability coverage percentage per project/release | `EOIP-engg-doc-pkg/gaps-implementation.md:381`; audit line 1466 | P0 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | area fallback | PROVE |
| `REQ-OBS-020` | `GAP-SDT-006`: GAP-SDT-006: Provide release-level “traceability completeness” gates | `EOIP-engg-doc-pkg/gaps-requirements.md:386`; audit line 1467 | P0 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | area fallback | PROVE |
| `REQ-OBS-021` | `INFRA-003.4`: - [x] `INFRA-003.4` Health check verification | `eoip-phase4-2-requirements.md:861`; audit line 1584 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-OBS-022` | `INFRA-004.1`: - [x] `INFRA-004.1` Structured JSON logging | `eoip-phase4-2-requirements.md:881`; audit line 1587 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-OBS-023` | `MS-KGR-020`: - **Health SLA Alerting:** Define health SLAs per entity type (e.g., "ServiceCatalog entities must be ≤ 24h stale") and receive alerts when SLAs are breached. Integrated with PagerDuty, Slack, and custom webhooks (from M... | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:424`; audit line 1669 | UNSTATED | MISSED | [CP-16](#cp-16) | subject triage | TRACE/BUILD |
| `REQ-OBS-024` | `MVP-FR-023`: Logging | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:121`; audit line 1702 | P0 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | area fallback | PROVE |
| `REQ-OBS-025` | `MVP-FR-024`: Metrics | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:122`; audit line 1703 | P0 | IMPLEMENTED-UNVERIFIED | [CP-30](#cp-30) | area fallback | PROVE |
| `REQ-OBS-026` | `MVP-P7`: &#124; MVP-P7 &#124; Acceptance, Traceability, And Productization &#124; Close acceptance criteria, traceability, dependency/license/SBOM review, ADRs, risk register, demo playbook, multi-backend product positioning, and release han... | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md:51`; audit line 1716 | UNSTATED | MISSED | [CP-33](#cp-33) | subject triage | TRACE/BUILD |
| `REQ-OBS-027` | `NFR-002`: &#124; NFR-002 &#124; Missing &#124; unassessed / P1 &#124; EOIP-engg-doc-pkg/super-requirements.md:897 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish acceptance criteria and phase dependencies. &#124; | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1680`; audit line 1718 | P1 | MISSED | [CP-30](#cp-30) | area fallback | TRACE/BUILD |
| `REQ-OBS-028` | `NFR-003`: &#124; NFR-003 &#124; Missing &#124; unassessed / P1 &#124; EOIP-engg-doc-pkg/super-requirements.md:898 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish acceptance criteria and phase dependencies. &#124; | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1681`; audit line 1719 | P1 | MISSED | [CP-30](#cp-30) | area fallback | TRACE/BUILD |
| `REQ-OBS-029` | `NFR-004`: &#124; NFR-004 &#124; Missing &#124; unassessed / P1 &#124; EOIP-engg-doc-pkg/super-requirements.md:899 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish acceptance criteria and phase dependencies. &#124; | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1682`; audit line 1720 | P1 | MISSED | [CP-30](#cp-30) | area fallback | TRACE/BUILD |
| `REQ-OBS-030` | `NFR-005`: &#124; NFR-005 &#124; Missing &#124; unassessed / P1 &#124; EOIP-engg-doc-pkg/super-requirements.md:900 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish acceptance criteria and phase dependencies. &#124; | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1683`; audit line 1721 | P1 | MISSED | [CP-30](#cp-30) | area fallback | TRACE/BUILD |
| `REQ-OBS-031` | `NFR-006`: &#124; NFR-006 &#124; Missing &#124; unassessed / P1 &#124; EOIP-engg-doc-pkg/super-requirements.md:901 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish acceptance criteria and phase dependencies. &#124; | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1684`; audit line 1722 | P1 | MISSED | [CP-30](#cp-30) | area fallback | TRACE/BUILD |
| `REQ-OBS-032` | `NFR-007`: &#124; NFR-007 &#124; Missing &#124; unassessed / P1 &#124; EOIP-engg-doc-pkg/super-requirements.md:902 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish acceptance criteria and phase dependencies. &#124; | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1685`; audit line 1723 | P1 | MISSED | [CP-30](#cp-30) | area fallback | TRACE/BUILD |
| `REQ-OBS-033` | `NFR-008`: &#124; NFR-008 &#124; Missing &#124; unassessed / P1 &#124; EOIP-engg-doc-pkg/super-requirements.md:903 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish acceptance criteria and phase dependencies. &#124; | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1686`; audit line 1724 | P1 | MISSED | [CP-30](#cp-30) | area fallback | TRACE/BUILD |
| `REQ-OBS-034` | `SDLC-001`: - **Step 0. Pre-flight.** Run PRE-001 and PRE-002. Decide DEC-P4-01 to 05. If accepted, start the three cheap de-risking proposals: SDLC-001 (traceability gate), SDLC-004 (engine registry), SDLC-015 (rules for the coding... | `eoip-phase4-2-requirements.md:174`; audit line 1784 | UNSTATED | MISSED | [CP-00](#cp-00) | engine family | TRACE/BUILD |
| `REQ-OBS-035` | `SDLC-015`: - **Step 0. Pre-flight.** Run PRE-001 and PRE-002. Decide DEC-P4-01 to 05. If accepted, start the three cheap de-risking proposals: SDLC-001 (traceability gate), SDLC-004 (engine registry), SDLC-015 (rules for the coding... | `eoip-phase4-2-requirements.md:174`; audit line 1854 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-OBS-036` | `SDLC-025.2`: - [ ] `SDLC-025.2` Trace ID present in logs and decision records | `eoip-phase4-2-requirements.md:1864`; audit line 1906 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-OBS-037` | `SDLC-033.2`: - [ ] `SDLC-033.2` CLI covers health, migrate, flags | `eoip-phase4-2-requirements.md:2013`; audit line 1946 | UNSTATED | MISSED | [CP-29](#cp-29) | engine family | TRACE/BUILD |
| `REQ-OBS-038` | `TASK-AIE-006`: - **TASK-AIE-006**: Implement XAI Engine (AI-001) — feature importance, decision trace, confidence calibration | `EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:37`; audit line 2249 | UNSTATED | MISSED | [CP-30](#cp-30) | area fallback | TRACE/BUILD |
| `REQ-OBS-039` | `TASK-ARCH-017`: - **TASK-ARCH-017**: Define observability requirements per engine — what to trace, what to meter, what to log | `EOIP-engg-doc-pkg/roles/Architect_tasks.md:82`; audit line 2273 | UNSTATED | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-OBS-040` | `TASK-CEO-009`: - **TASK-CEO-009**: Define success metrics: ARR targets, customer acquisition, NPS, churn | `EOIP-engg-doc-pkg/roles/CEO_tasks.md:65`; audit line 2282 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-OBS-041` | `TASK-CTO-008`: - **TASK-CTO-008**: Establish engineering metrics: deployment frequency, lead time, MTTR, change failure rate | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:56`; audit line 2294 | UNSTATED | MISSED | [CP-31](#cp-31) | subject triage | TRACE/BUILD |
| `REQ-OBS-042` | `TASK-CTO-016`: - **TASK-CTO-016**: Design observability stack: metrics (Prometheus), logs (Loki), traces (OTel), dashboards (Grafana) | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:106`; audit line 2302 | UNSTATED | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-OBS-043` | `TASK-QA-016`: - **TASK-QA-016**: Brain OS telemetry integration — verify all engines report stats via `get_system_telemetry()` | `EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:36`; audit line 2428 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-OBS-044` | `TASK-QAL-012`: - **TASK-QAL-012**: Establish quality metrics dashboard: test coverage, pass rate, defect density, escape rate | `EOIP-engg-doc-pkg/roles/QALead_tasks.md:66`; audit line 2445 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |

### A.16 ONT: 96 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-ONT-001` | `AC-09`: &#124; AC-09 &#124; Export produces valid PNG, SVG, PDF, JSON-LD, GraphML, CSV, GEXF, Obsidian, Mermaid, Cypher &#124; Graphify: HTML/JSON/GraphML/SVG/Obsidian/Mermaid/Cypher — KGR matches all + adds PDF/JSON-LD/GEXF &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1040`; audit line 107 | UNSTATED | STUBBED | [CP-25](#cp-25) | explicit | REPLACE |
| `REQ-ONT-002` | `AC-27`: &#124; AC-27 &#124; 11+ export formats covering every competitor's export capability &#124; Surpasses all: matches Graphify's 7 + adds PDF/JSON-LD/GEXF/clipboard &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1058`; audit line 125 | UNSTATED | STUBBED | [CP-25](#cp-25) | explicit | REPLACE |
| `REQ-ONT-003` | `AC-FR-ID-001`: &#124; FR-ID-001 &#124; Identity &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-ID-001 &#124; AC-FR-ID-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:43`; audit line 177 | UNSTATED | MISSED | [CP-17](#cp-17) | ID family | TRACE/BUILD |
| `REQ-ONT-004` | `AC-FR-ID-002`: &#124; FR-ID-002 &#124; Identity &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-ID-002 &#124; AC-FR-ID-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:44`; audit line 178 | UNSTATED | MISSED | [CP-17](#cp-17) | ID family | TRACE/BUILD |
| `REQ-ONT-005` | `AC-FR-ONTO-001`: &#124; FR-ONTO-001 &#124; Ontology &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-ONTO-001 &#124; AC-FR-ONTO-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:39`; audit line 187 | UNSTATED | MISSED | [CP-12](#cp-12) | ID family | TRACE/BUILD |
| `REQ-ONT-006` | `AC-FR-ONTO-002`: &#124; FR-ONTO-002 &#124; Ontology &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-ONTO-002 &#124; AC-FR-ONTO-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:40`; audit line 188 | UNSTATED | MISSED | [CP-12](#cp-12) | ID family | TRACE/BUILD |
| `REQ-ONT-007` | `AC-FR-TEMP-001`: &#124; FR-TEMP-001 &#124; Temporal &#124; WP-ONTOLOGY-GRAPH &#124; TEST-FR-TEMP-001 &#124; AC-FR-TEMP-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:45`; audit line 206 | UNSTATED | MISSED | [CP-18](#cp-18) | ID family | TRACE/BUILD |
| `REQ-ONT-008` | `AI-003.3`: - [x] `AI-003.3` Ontology-aware validation | `eoip-phase4-2-requirements.md:700`; audit line 272 | UNSTATED | MISSED | [CP-17](#cp-17) | engine family | TRACE/BUILD |
| `REQ-ONT-009` | `AIDLC-001`: - **Step 3. Knowledge pipeline.** AI-002, then AI-003, then AGENT-002 (settles conflict B6), then temporal retrieval, OWL/SHACL and federation, with quality benchmarks, lineage and re-embedding. Items: `AI-002`, `AI-003`... | `eoip-phase4-2-requirements.md:177`; audit line 299 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-ONT-010` | `AIDLC-002`: - **Step 3. Knowledge pipeline.** AI-002, then AI-003, then AGENT-002 (settles conflict B6), then temporal retrieval, OWL/SHACL and federation, with quality benchmarks, lineage and re-embedding. Items: `AI-002`, `AI-003`... | `eoip-phase4-2-requirements.md:177`; audit line 304 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-ONT-011` | `FR-02`: &#124; FR-02 &#124; Ontology and graph &#124; Enterprise ontology, schema generation, semantic validation, identity resolution, provenance, lineage, temporal graph, relationship model, graph quality, and graph algorithms. &#124; | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1081`; audit line 487 | UNSTATED | MISSED | [CP-17](#cp-17) | subject triage | TRACE/BUILD |
| `REQ-ONT-012` | `FR-ONTO-001`: Enterprise ontology vocabulary | `EOIP-engg-doc-pkg/03-functional-requirements.md:255`; audit line 576 | P0 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | ID family | PROVE |
| `REQ-ONT-013` | `G2-EKAF-017`: G2-EKAF-017 — Schema drift | `EOIP-engg-doc-pkg/gaps2-requirements.md:265`; audit line 692 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-ONT-014` | `G2-P8`: &#124; G2-P8 &#124; Knowledge health & governed AI &#124; immune system + ontology proposals + capsules &#124; | `EOIP-engg-doc-pkg/gaps2-implementation.md:43`; audit line 806 | UNSTATED | MISSED | [CP-12](#cp-12) | subject triage | TRACE/BUILD |
| `REQ-ONT-015` | `G2-REQ-34`: &#124; G2-REQ-34 required data contracts &#124; Required G2 schema files exist under `schemas/`, including telemetry, API contract, capsule, simulation, debt/SLO, ontology proposal, causal hypothesis and process event contracts ... | `EOIP-engg-doc-pkg/reference/g2-traceability.md:63`; audit line 838 | UNSTATED | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-ONT-016` | `GAP-AGOV-001`: GAP-AGOV-001: Tool registry with versioned schemas | `EOIP-engg-doc-pkg/gaps-implementation.md:55`; audit line 1207 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | ID family | PROVE |
| `REQ-ONT-017` | `GAP-AKO-002`: GAP-AKO-002: Ontology Reviewer Agent | `EOIP-engg-doc-pkg/gaps-requirements.md:696`; audit line 1222 | P2 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-ONT-018` | `GAP-CONTRACT-004`: GAP-CONTRACT-004: Generate compatibility reports before deploying ontology changes | `EOIP-engg-doc-pkg/gaps-requirements.md:442`; audit line 1266 | P2 | IMPLEMENTED-UNVERIFIED | [CP-25](#cp-25) | subject triage | PROVE |
| `REQ-ONT-019` | `GAP-CP-001`: GAP-CP-001: Ontology is the semantic control plane, not merely another graph | `EOIP-engg-doc-pkg/gaps-implementation.md:50`; audit line 1269 | P2 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-ONT-020` | `GAP-CP-007`: GAP-CP-007: Every schema/ontology change is versioned and diffable | `EOIP-engg-doc-pkg/gaps-requirements.md:405`; audit line 1275 | P2 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-ONT-021` | `GAP-CP-008`: GAP-CP-008: Breaking schema changes require migration plans | `EOIP-engg-doc-pkg/gaps-requirements.md:406`; audit line 1276 | P2 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-ONT-022` | `GAP-DBAGNOSTIC-001`: GAP-DBAGNOSTIC-001: Keep ontology/domain contracts independent of any single graph database implementation | `EOIP-engg-doc-pkg/gaps-implementation.md:53`; audit line 1279 | P2 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-ONT-023` | `GAP-DRIFT-002`: GAP-DRIFT-002: Detect ontology drift | `EOIP-engg-doc-pkg/gaps-requirements.md:514`; audit line 1281 | P1 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-ONT-024` | `GAP-DRIFT-006`: GAP-DRIFT-006: Detect code architecture drift from intended ontology/architecture | `EOIP-engg-doc-pkg/gaps-requirements.md:518`; audit line 1285 | P1 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-ONT-025` | `GAP-DUAL`: Dual semantic model (RDF/OWL ↔ property graph) | `requirements-registry.json:1`; audit line 1287 | P1 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-ONT-026` | `GAP-DUAL-001`: GAP-DUAL-001: Implement a Dual Semantic Model: native HugeGraph property graph + canonical RDF/OWL/SHACL semantic representation | `EOIP-engg-doc-pkg/gaps-requirements.md:142`; audit line 1288 | P2 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-ONT-027` | `GAP-EXPORT-001`: GAP-EXPORT-001: Support RDF, JSON-LD, GraphML/CSV and canonical JSON exports | `EOIP-engg-doc-pkg/gaps-requirements.md:339`; audit line 1301 | P2 | IMPLEMENTED-UNVERIFIED | [CP-25](#cp-25) | ID family | PROVE |
| `REQ-ONT-028` | `GAP-GITOPS-002`: GAP-GITOPS-002: Provide ontology branch, pull-request/review and merge workflows | `EOIP-engg-doc-pkg/gaps-requirements.md:418`; audit line 1325 | P0 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | ID family | PROVE |
| `REQ-ONT-029` | `GAP-GITOPS-004`: GAP-GITOPS-004: CI validates ontology before publishing | `EOIP-engg-doc-pkg/gaps-requirements.md:427`; audit line 1327 | P0 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | ID family | PROVE |
| `REQ-ONT-030` | `GAP-GITOPS-005`: GAP-GITOPS-005: Run impact analysis for ontology changes | `EOIP-engg-doc-pkg/gaps-requirements.md:428`; audit line 1328 | P0 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | ID family | PROVE |
| `REQ-ONT-031` | `GAP-GITOPS-008`: GAP-GITOPS-008: Package ontology releases using SemVer-like policy | `EOIP-engg-doc-pkg/gaps-requirements.md:431`; audit line 1331 | P0 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | ID family | PROVE |
| `REQ-ONT-032` | `GAP-GOV-002`: GAP-GOV-002: Support ontology branches, diffs, merge conflict detection and semantic merge | `EOIP-engg-doc-pkg/gaps-requirements.md:198`; audit line 1334 | P2 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-ONT-033` | `GAP-GOV-003`: GAP-GOV-003: Add business glossary, taxonomy, reference-data and ontology crosswalks | `EOIP-engg-doc-pkg/gaps-requirements.md:199`; audit line 1335 | P2 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-ONT-034` | `GAP-HG-002`: GAP-HG-002: Automated schema migration | `EOIP-engg-doc-pkg/gaps-implementation.md:168`; audit line 1346 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-ONT-035` | `GAP-HG-010`: GAP-HG-010: avoid pretending SPARQL/RDF is native; use explicit semantic adapter | `EOIP-engg-doc-pkg/gaps-requirements.md:1083`; audit line 1354 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-ONT-036` | `GAP-IDE-001`: GAP-IDE-001: Expose ontology and lineage directly within VS Code | `EOIP-engg-doc-pkg/gaps-requirements.md:173`; audit line 1356 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-ONT-037` | `GAP-KGCI-004`: GAP-KGCI-004: Generate versioned ontology artifact | `EOIP-engg-doc-pkg/gaps-requirements.md:823`; audit line 1368 | P0 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-ONT-038` | `GAP-KRAG-001`: GAP-KRAG-001: Retrieval must be ontology-aware | `EOIP-engg-doc-pkg/gaps-implementation.md:170`; audit line 1380 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-ONT-039` | `GAP-MKT-001`: GAP-MKT-001: Package reusable ontology modules | `EOIP-engg-doc-pkg/gaps-implementation.md:782`; audit line 1406 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-ONT-040` | `GAP-NOCODE`: Visual ontology studio | `requirements-registry.json:1`; audit line 1416 | P1 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-ONT-041` | `GAP-NOCODE-003`: GAP-NOCODE-003: Generate forms, GraphQL/OpenAPI schemas and validation rules from ontology definitions where feasible | `EOIP-engg-doc-pkg/gaps-requirements.md:196`; audit line 1419 | P0 | IMPLEMENTED-UNVERIFIED | [CP-07](#cp-07) | subject triage | PROVE |
| `REQ-ONT-042` | `GAP-SEM-001`: GAP-SEM-001: Treat ontology/schema/governance as first-class, not a plugin | `EOIP-engg-doc-pkg/gaps-requirements.md:146`; audit line 1484 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | subject triage | PROVE |
| `REQ-ONT-043` | `GAP-STUDIO-004`: GAP-STUDIO-004: RDFS/OWL export | `EOIP-engg-doc-pkg/gaps-requirements.md:606`; audit line 1488 | P0 | IMPLEMENTED-UNVERIFIED | [CP-25](#cp-25) | subject triage | PROVE |
| `REQ-ONT-044` | `GAP-STUDIO-008`: GAP-STUDIO-008: Reusable ontology modules | `EOIP-engg-doc-pkg/gaps-requirements.md:610`; audit line 1492 | P0 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-ONT-045` | `GAP-STUDIO-011`: GAP-STUDIO-011: Generate forms and API schemas from ontology where practical | `EOIP-engg-doc-pkg/gaps-requirements.md:613`; audit line 1495 | P0 | IMPLEMENTED-UNVERIFIED | [CP-07](#cp-07) | subject triage | PROVE |
| `REQ-ONT-046` | `H-08`: OpenAPI schema publication | `KGF-MASTER-BACKLOG.md:283`; audit line 1567 | P0 | IMPLEMENTED-UNVERIFIED | [CP-07](#cp-07) | subject triage | PROVE |
| `REQ-ONT-047` | `KGR-G-015`: LLM-Assisted Dynamic Ontology Induction with Anti-Drift Guards | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:314`; audit line 1624 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-ONT-048` | `KGR-G-026`: Dynamic Living Brain Ontology Induction & Consolidation | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:230`; audit line 1635 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-ONT-049` | `MS-13`: Graph-as-Code & GitOps for Ontology, Data, and Policy | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:96`; audit line 1643 | P1 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | explicit | PROVE |
| `REQ-ONT-050` | `MS-15`: Enterprise Large Ontology Model (LOM) Fine-Tuning Runtime | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:24`; audit line 1645 | P1 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-ONT-051` | `MVP-FR-002`: Automatic graph schema initialization | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:100`; audit line 1680 | P0 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-ONT-052` | `MVP-FR-009`: Meta graph | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:107`; audit line 1687 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | subject triage | PROVE |
| `REQ-ONT-053` | `SDLC-007`: - [x] `INFRA-003.A2` Schema migrations (SDLC-007) run in order with deploys; promotion gates reference evaluation and load results (AIDLC-004, TEST-004). *(added by review)* | `eoip-phase4-2-requirements.md:864`; audit line 1814 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-ONT-054` | `SDLC-017.2`: - [ ] `SDLC-017.2` MCP tool schemas covered | `eoip-phase4-2-requirements.md:1715`; audit line 1866 | UNSTATED | MISSED | [CP-29](#cp-29) | engine family | TRACE/BUILD |
| `REQ-ONT-055` | `SR-ARC-004`: &#124; SR-ARC-004 &#124; **Single canonical contract per concept:** one versioned schema registry for entities, edges, events, QueryPlan, agent contract, config and plugin manifest; all APIs and UIs derive from it (generated, no... | `EOIP-engg-doc-pkg/super-requirements.md:165`; audit line 1978 | P0 | MISSED | [CP-29](#cp-29) | subject triage | TRACE/BUILD |
| `REQ-ONT-056` | `SR-CFG-001`: &#124; SR-CFG-001 &#124; **Layered configuration:** product default → edition → partner → tenant → business unit → workspace → user. Each setting is typed (JSON Schema), documented, validated, versioned and audited. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:747`; audit line 1987 | P0 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ONT-057` | `SR-CFG-006`: &#124; SR-CFG-006 &#124; **Hot reload** for non-structural settings; structural changes (backend bindings, ontology major versions) go through migration plans. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:752`; audit line 1992 | P1 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ONT-058` | `SR-CON-009`: &#124; SR-CON-009 &#124; **Vendor-neutral data ownership:** customers can export all data, ontology, config and audit trails in open formats at any time (§7.9). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:106`; audit line 2013 | P0 | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-ONT-059` | `SR-EXT-001`: &#124; SR-EXT-001 &#124; **Headless first:** every UI capability is available through public, versioned APIs — REST (OpenAPI 3.1), GraphQL (ontology-generated), gRPC (high-volume), WebSocket/SSE (streaming answers, subscriptions... | `EOIP-engg-doc-pkg/super-requirements.md:776`; audit line 2028 | P0 | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-ONT-060` | `SR-GDB-001`: &#124; SR-GDB-001 &#124; All graph access MUST go through the **Graph Store Port** exposing: schema ops, bulk load, transactional upsert (idempotent by canonical ID), traversal, path, neighborhood, aggregation, full-scan with cu... | `EOIP-engg-doc-pkg/super-requirements.md:183`; audit line 2039 | P0 | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-ONT-061` | `SR-GOV-004`: &#124; SR-GOV-004 &#124; **Roles:** data owners, stewards, custodians, ontology curators, security admins, auditors (read-only, tamper-evident views). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:871`; audit line 2058 | P0 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-ONT-062` | `SR-NFR-006`: &#124; SR-NFR-006 &#124; **Upgrades:** rolling and blue/green for clustered; offline signed upgrade bundles for air-gapped; versioned idempotent schema/ontology migrations; tested downgrade/rollback; compatibility matrix; LTS an... | `EOIP-engg-doc-pkg/super-requirements.md:901`; audit line 2119 | P0 | MISSED | [CP-27](#cp-27) | subject triage | TRACE/BUILD |
| `REQ-ONT-063` | `SR-ONT-001`: &#124; SR-ONT-001 &#124; **Ontology service** stores ontologies as versioned artifacts (semantic versioning, diff, migration plans, deprecation lifecycle). Every graph element pins `ontology_version`. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:495`; audit line 2137 | P0 | MISSED | [CP-12](#cp-12) | ID family | TRACE/BUILD |
| `REQ-ONT-064` | `SR-ONT-002`: &#124; SR-ONT-002 &#124; **Import/export:** OWL 2 (RDF/XML, Turtle, Manchester), RDFS, SKOS, JSON Schema, JSON-LD contexts, LinkML-style schemas, Protégé project interop, CSV glossaries; export of the active ontology to OWL and ... | `EOIP-engg-doc-pkg/super-requirements.md:496`; audit line 2138 | P0 | MISSED | [CP-12](#cp-12) | ID family | TRACE/BUILD |
| `REQ-ONT-065` | `SR-ONT-003`: &#124; SR-ONT-003 &#124; **Ontology Studio** (UI): visual class/property editor, relationship canvas, constraint editor, glossary/taxonomy manager, mapping designer, diff/merge, impact preview ("what existing data breaks if I ch... | `EOIP-engg-doc-pkg/super-requirements.md:497`; audit line 2139 | P0 | MISSED | [CP-12](#cp-12) | ID family | TRACE/BUILD |
| `REQ-ONT-066` | `SR-ONT-004`: &#124; SR-ONT-004 &#124; **Constraint validation** via SHACL-class shapes plus native rules; severity-based gates in ingestion; constraint violations visible as a graph-quality dashboard. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:498`; audit line 2140 | P0 | MISSED | [CP-12](#cp-12) | ID family | TRACE/BUILD |
| `REQ-ONT-067` | `SR-ONT-005`: &#124; SR-ONT-005 &#124; **Business glossary and taxonomy** (SKOS-compatible): terms, synonyms, multilingual labels, definitions, owners, approved-status; terms link to ontology concepts and to physical fields; NL layer uses the... | `EOIP-engg-doc-pkg/super-requirements.md:499`; audit line 2141 | P0 | MISSED | [CP-12](#cp-12) | ID family | TRACE/BUILD |
| `REQ-ONT-068` | `SR-ONT-006`: &#124; SR-ONT-006 &#124; **Ontology alignment/matching:** lexical, structural, embedding-assisted mapping between a customer's vocabulary and an industry standard, with confidence and steward review. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:500`; audit line 2142 | P1 | MISSED | [CP-12](#cp-12) | ID family | TRACE/BUILD |
| `REQ-ONT-069` | `SR-ONT-007`: &#124; SR-ONT-007 &#124; **Tenant-renamable terminology (white-label semantics):** a tenant may rename "Service" → "Application", "Incident" → "Case", etc., without changing the underlying canonical type. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:501`; audit line 2143 | P0 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | ID family | PROVE |
| `REQ-ONT-070` | `SR-ONT-008`: &#124; SR-ONT-008 &#124; **Ontology-driven generation:** GraphQL schema, REST resources, form UIs, validation, and docs generated from the ontology. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:502`; audit line 2144 | P1 | MISSED | [CP-12](#cp-12) | ID family | TRACE/BUILD |
| `REQ-ONT-071` | `SR-ONT-009`: &#124; SR-ONT-009 &#124; **Governed evolution:** proposals, review, approval, scheduled rollout, backward-compat checks, automatic data migration jobs, rollback. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:503`; audit line 2145 | P0 | MISSED | [CP-12](#cp-12) | ID family | TRACE/BUILD |
| `REQ-ONT-072` | `SR-ONT-010`: &#124; SR-ONT-010 &#124; **Catalog interoperability:** import/sync with data catalogs and glossaries (DataHub, OpenMetadata, Atlas, Collibra-class), CMDBs, enterprise-architecture repositories (ArchiMate/TOGAF models), and API r... | `EOIP-engg-doc-pkg/super-requirements.md:504`; audit line 2146 | P1 | MISSED | [CP-12](#cp-12) | ID family | TRACE/BUILD |
| `REQ-ONT-073` | `SR-ONT-020`: &#124; SR-ONT-020 &#124; **Inference tiers:** (a) graph-native derivations (transitive, inverse, symmetric, property chains), (b) rule-based (Datalog/SWRL-class) materialization with provenance, (c) OWL-RL/EL profile reasoning w... | `EOIP-engg-doc-pkg/super-requirements.md:522`; audit line 2147 | P1 | MISSED | [CP-12](#cp-12) | ID family | TRACE/BUILD |
| `REQ-ONT-074` | `SR-ONT-021`: &#124; SR-ONT-021 &#124; **Truth maintenance:** retraction of premises retracts conclusions; contradictions are surfaced as validation findings, never silently resolved. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:523`; audit line 2148 | P1 | MISSED | [CP-12](#cp-12) | ID family | TRACE/BUILD |
| `REQ-ONT-075` | `SR-ONT-022`: &#124; SR-ONT-022 &#124; **Temporal and defeasible semantics** for roles/ownership that change over time (valid-time intervals on edges). &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:524`; audit line 2149 | P1 | MISSED | [CP-12](#cp-12) | ID family | TRACE/BUILD |
| `REQ-ONT-076` | `SR-WL-001`: &#124; SR-WL-001 &#124; **Brand tokens:** logo(s), favicon, app name, colors, typography, spacing, icon sets, node/edge visual styles per ontology type, light/dark themes — all via theme packages, no code change. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:733`; audit line 2235 | P0 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-ONT-077` | `TASK-ARCH-003`: - **TASK-ARCH-003**: Design Verification Engine (CORE-002) pipeline — VerifierRegistry composition model, loop boundary integration points, audit trail schema | `EOIP-engg-doc-pkg/roles/Architect_tasks.md:21`; audit line 2259 | UNSTATED | MISSED | [CP-12](#cp-12) | subject triage | TRACE/BUILD |
| `REQ-ONT-078` | `TASK-ARCH-008`: - **TASK-ARCH-008**: Define event schema standards for inter-engine communication | `EOIP-engg-doc-pkg/roles/Architect_tasks.md:42`; audit line 2264 | UNSTATED | MISSED | [CP-12](#cp-12) | subject triage | TRACE/BUILD |
| `REQ-ONT-079` | `TASK-ARCH-009`: - **TASK-ARCH-009**: Design temporal index schema for GRAPH-005 (fact validity windows, as-of queries) | `EOIP-engg-doc-pkg/roles/Architect_tasks.md:47`; audit line 2265 | UNSTATED | MISSED | [CP-18](#cp-18) | subject triage | TRACE/BUILD |
| `REQ-ONT-080` | `TASK-ARCH-011`: - **TASK-ARCH-011**: Design embedding versioning schema for AI-006 (version lineage, drift detection triggers) | `EOIP-engg-doc-pkg/roles/Architect_tasks.md:55`; audit line 2267 | UNSTATED | MISSED | [CP-17](#cp-17) | subject triage | TRACE/BUILD |
| `REQ-ONT-081` | `TASK-ARCH-013`: - **TASK-ARCH-013**: Design Agent Communication Bus (AGENT-003) message schema and routing topology | `EOIP-engg-doc-pkg/roles/Architect_tasks.md:65`; audit line 2269 | UNSTATED | MISSED | [CP-12](#cp-12) | subject triage | TRACE/BUILD |
| `REQ-ONT-082` | `TASK-LD-009`: - **TASK-LD-009**: Define Pydantic model standards for API request/response schemas | `EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:52`; audit line 2359 | UNSTATED | MISSED | [CP-07](#cp-07) | subject triage | TRACE/BUILD |
| `REQ-ONT-083` | `TASK-QA-017`: - **TASK-QA-017**: Platform Router API integration — verify all endpoints respond with correct schemas | `EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:40`; audit line 2429 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-ONT-084` | `WP-FOUNDATION-03`: ### WP-FOUNDATION-03 — Schema bootstrap | `EOIP-engg-doc-pkg/implementation/wp-foundation.md:41`; audit line 2648 | UNSTATED | MISSED | [CP-12](#cp-12) | subject triage | TRACE/BUILD |
| `REQ-ONT-085` | `WP-ONTOLOGY-GRAPH-01`: ### WP-ONTOLOGY-GRAPH-01 — Meta graph | `EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:30`; audit line 2658 | UNSTATED | MISSED | [CP-12](#cp-12) | subject triage | TRACE/BUILD |
| `REQ-ONT-086` | `WP-ONTOLOGY-GRAPH-02`: ### WP-ONTOLOGY-GRAPH-02 — Cross-domain bridge edges | `EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:39`; audit line 2659 | UNSTATED | MISSED | [CP-12](#cp-12) | subject triage | TRACE/BUILD |
| `REQ-ONT-087` | `WP-ONTOLOGY-GRAPH-03`: ### WP-ONTOLOGY-GRAPH-03 — Index strategy | `EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:48`; audit line 2660 | UNSTATED | MISSED | [CP-12](#cp-12) | subject triage | TRACE/BUILD |
| `REQ-ONT-088` | `WP-ONTOLOGY-GRAPH-04`: ### WP-ONTOLOGY-GRAPH-04 — Graph version journal | `EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:57`; audit line 2661 | UNSTATED | MISSED | [CP-12](#cp-12) | subject triage | TRACE/BUILD |
| `REQ-ONT-089` | `WP-ONTOLOGY-GRAPH-05`: ### WP-ONTOLOGY-GRAPH-05 — RDF/OWL interoperability | `EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:66`; audit line 2662 | UNSTATED | MISSED | [CP-12](#cp-12) | subject triage | TRACE/BUILD |
| `REQ-ONT-090` | `WP-ONTOLOGY-GRAPH-06`: ### WP-ONTOLOGY-GRAPH-06 — Enterprise ontology vocabulary | `EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:75`; audit line 2663 | UNSTATED | MISSED | [CP-12](#cp-12) | subject triage | TRACE/BUILD |
| `REQ-ONT-091` | `WP-ONTOLOGY-GRAPH-07`: ### WP-ONTOLOGY-GRAPH-07 — Relationship semantics | `EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:84`; audit line 2664 | UNSTATED | MISSED | [CP-12](#cp-12) | subject triage | TRACE/BUILD |
| `REQ-ONT-092` | `WP-ONTOLOGY-GRAPH-08`: ### WP-ONTOLOGY-GRAPH-08 — Evidence model | `EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:93`; audit line 2665 | UNSTATED | MISSED | [CP-12](#cp-12) | subject triage | TRACE/BUILD |
| `REQ-ONT-093` | `WP-ONTOLOGY-GRAPH-09`: ### WP-ONTOLOGY-GRAPH-09 — Provenance traversal | `EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:102`; audit line 2666 | UNSTATED | MISSED | [CP-17](#cp-17) | subject triage | TRACE/BUILD |
| `REQ-ONT-094` | `WP-ONTOLOGY-GRAPH-10`: ### WP-ONTOLOGY-GRAPH-10 — Deterministic identity resolution | `EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:111`; audit line 2667 | UNSTATED | MISSED | [CP-17](#cp-17) | subject triage | TRACE/BUILD |
| `REQ-ONT-095` | `WP-ONTOLOGY-GRAPH-11`: ### WP-ONTOLOGY-GRAPH-11 — Ambiguous identity candidates | `EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:120`; audit line 2668 | UNSTATED | MISSED | [CP-12](#cp-12) | subject triage | TRACE/BUILD |
| `REQ-ONT-096` | `WP-ONTOLOGY-GRAPH-12`: ### WP-ONTOLOGY-GRAPH-12 — Bitemporal-ready fields | `EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:129`; audit line 2669 | UNSTATED | MISSED | [CP-18](#cp-18) | subject triage | TRACE/BUILD |

### A.17 OPS: 47 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-OPS-001` | `AC-NFR-OPS-001`: &#124; NFR-OPS-001 &#124; Observability &#124; WP-SECURITY-OPS &#124; TEST-NFR-OPS-001 &#124; AC-NFR-OPS-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:91`; audit line 215 | UNSTATED | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-OPS-002` | `AC-NFR-OPS-002`: &#124; NFR-OPS-002 &#124; Observability &#124; WP-SECURITY-OPS &#124; TEST-NFR-OPS-002 &#124; AC-NFR-OPS-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:92`; audit line 216 | UNSTATED | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-OPS-003` | `AI-004.3`: - [x] `AI-004.3` Canary deployment with auto-rollback | `eoip-phase4-2-requirements.md:721`; audit line 278 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-OPS-004` | `AIDLC-008.2`: - [ ] `AIDLC-008.2` Failover test | `eoip-phase4-2-requirements.md:2128`; audit line 336 | UNSTATED | MISSED | [CP-31](#cp-31) | subject triage | TRACE/BUILD |
| `REQ-OPS-005` | `GAP-CHANGE-001`: GAP-CHANGE-001: Analyze a proposed code change before merge | `EOIP-engg-doc-pkg/gaps-implementation.md:383`; audit line 1257 | P0 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-OPS-006` | `GAP-CHANGE-002`: GAP-CHANGE-002: Analyze a Jira/change request before implementation | `EOIP-engg-doc-pkg/gaps-requirements.md:548`; audit line 1258 | P0 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-OPS-007` | `GAP-CHANGE-003`: GAP-CHANGE-003: Traverse code, service, test, deployment, ownership and incident relationships | `EOIP-engg-doc-pkg/gaps-requirements.md:549`; audit line 1259 | P0 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-OPS-008` | `GAP-CHANGE-004`: GAP-CHANGE-004: Categorize impact: | `EOIP-engg-doc-pkg/gaps-requirements.md:550`; audit line 1260 | P0 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-OPS-009` | `GAP-CHANGE-005`: GAP-CHANGE-005: Provide confidence and supporting paths | `EOIP-engg-doc-pkg/gaps-requirements.md:559`; audit line 1261 | P0 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-OPS-010` | `GAP-CHANGE-006`: GAP-CHANGE-006: Compare predicted impact with actual post-deployment incidents to calibrate the model | `EOIP-engg-doc-pkg/gaps-requirements.md:560`; audit line 1262 | P0 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-OPS-011` | `GAP-HA`: High availability patterns | `requirements-registry.json:1`; audit line 1343 | P1 | IMPLEMENTED-UNVERIFIED | [CP-31](#cp-31) | subject triage | PROVE |
| `REQ-OPS-012` | `GAP-HA-001`: GAP-HA-001: Provide self-managed HA patterns for HugeGraph distributed mode | `EOIP-engg-doc-pkg/gaps-implementation.md:664`; audit line 1344 | P1 | IMPLEMENTED-UNVERIFIED | [CP-31](#cp-31) | ID family | PROVE |
| `REQ-OPS-013` | `GAP-HG-007`: GAP-HG-007: backup/restore verification | `EOIP-engg-doc-pkg/gaps-requirements.md:1080`; audit line 1351 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-OPS-014` | `GAP-OPS-001`: &#124; `ops/` &#124; 2 &#124; Preflight checks, ops bundle (GAP-OPS-001) &#124; | `EOIP-engg-doc-pkg/06-architecture.md:126`; audit line 1426 | UNSTATED | PARTIAL | [CP-31](#cp-31) | area fallback | COMPLETE |
| `REQ-OPS-015` | `GAP-SDT-001`: GAP-SDT-001: Every requirement must be linkable to design, story, commit, code symbol, test, build, deployment, service and incident | `EOIP-engg-doc-pkg/gaps-implementation.md:166`; audit line 1462 | P0 | IMPLEMENTED-UNVERIFIED | [CP-31](#cp-31) | subject triage | PROVE |
| `REQ-OPS-016` | `GAP-SDT-008`: GAP-SDT-008: Support semantic digital-thread comparison between releases | `EOIP-engg-doc-pkg/gaps-requirements.md:388`; audit line 1469 | P0 | IMPLEMENTED-UNVERIFIED | [CP-31](#cp-31) | area fallback | PROVE |
| `REQ-OPS-017` | `H-06`: Docker Compose smoke test | `KGF-MASTER-BACKLOG.md:279`; audit line 1565 | P0 | IMPLEMENTED-UNVERIFIED | [CP-31](#cp-31) | area fallback | PROVE |
| `REQ-OPS-018` | `INFRA-003`: CD Pipeline & GitOps Deployment | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:579`; audit line 1580 | P2 | IMPLEMENTED-UNVERIFIED | [CP-31](#cp-31) | engine family | PROVE |
| `REQ-OPS-019` | `INFRA-005.4`: - [x] `INFRA-005.4` Failover handling | `eoip-phase4-2-requirements.md:907`; audit line 1596 | UNSTATED | MISSED | [CP-10](#cp-10) | engine family | TRACE/BUILD |
| `REQ-OPS-020` | `INFRA-007`: Automated Backup & Restore Testing | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:658`; audit line 1604 | P2 | IMPLEMENTED-UNVERIFIED | [CP-31](#cp-31) | engine family | PROVE |
| `REQ-OPS-021` | `INFRA-007.1`: - [x] `INFRA-007.1` Automated backup scheduling | `eoip-phase4-2-requirements.md:948`; audit line 1605 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-OPS-022` | `INFRA-007.2`: - [x] `INFRA-007.2` Backup integrity verification | `eoip-phase4-2-requirements.md:949`; audit line 1606 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-OPS-023` | `INFRA-007.3`: - [x] `INFRA-007.3` Automated restore testing | `eoip-phase4-2-requirements.md:950`; audit line 1607 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-OPS-024` | `MVP-FR-025`: Backup | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:123`; audit line 1704 | P0 | IMPLEMENTED-UNVERIFIED | [CP-31](#cp-31) | subject triage | PROVE |
| `REQ-OPS-025` | `MVP-FR-026`: Restore | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:124`; audit line 1705 | P0 | IMPLEMENTED-UNVERIFIED | [CP-31](#cp-31) | subject triage | PROVE |
| `REQ-OPS-026` | `REL-01`: Author the release checklist that requires live receipts | `KGF-MASTER-BACKLOG.md:1212`; audit line 1763 | P0 | IMPLEMENTED-UNVERIFIED | [CP-36](#cp-36) | ID family | PROVE |
| `REQ-OPS-027` | `REL-10`: Production HA, backup/restore and disaster-recovery receipts | `KGF-MASTER-BACKLOG.md:175`; audit line 1772 | P0 | BLOCKED | [CP-31](#cp-31) | explicit | UNBLOCK |
| `REQ-OPS-028` | `SDLC-006.4`: - [ ] `SDLC-006.4` Flag state is exported in backups | `eoip-phase4-2-requirements.md:1509`; audit line 1813 | UNSTATED | MISSED | [CP-28](#cp-28) | engine family | TRACE/BUILD |
| `REQ-OPS-029` | `SDLC-007.3`: - [ ] `SDLC-007.3` Upgrade test from the previous tagged release passes | `eoip-phase4-2-requirements.md:1527`; audit line 1817 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-OPS-030` | `SDLC-007.4`: - [ ] `SDLC-007.4` Migrations run in INFRA-003 deploy ordering | `eoip-phase4-2-requirements.md:1528`; audit line 1818 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-OPS-031` | `SDLC-022`: &#124; SDLC: release and deploy &#124; INFRA-003, INFRA-006 &#124; No SemVer/SBOM/signing, no production Kubernetes profile, no air-gapped bundle &#124; SDLC-022..024 &#124; | `eoip-phase4-2-requirements.md:1373`; audit line 1889 | UNSTATED | MISSED | [CP-33](#cp-33) | engine family | TRACE/BUILD |
| `REQ-OPS-032` | `SDLC-023.1`: - [ ] `SDLC-023.1` Hardened chart values with tests (helm lint, policy checks) | `eoip-phase4-2-requirements.md:1824`; audit line 1895 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-OPS-033` | `SR-DEP-006`: &#124; SR-DEP-006 &#124; **Supported-platform matrix** (OS, kernel, Kubernetes, container runtime, browsers, GPUs) maintained and tested per release. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:927`; audit line 2024 | P0 | MISSED | [CP-31](#cp-31) | ID family | TRACE/BUILD |
| `REQ-OPS-034` | `SR-OPS-001`: &#124; SR-OPS-001 &#124; **OpenTelemetry** metrics, logs and traces end-to-end (ingestion → mutation → query → answer); local sinks (Prometheus/Grafana/Loki/Tempo-class) bundled; customer sinks pluggable. Structured JSON logs wi... | `EOIP-engg-doc-pkg/super-requirements.md:909`; audit line 2150 | P0 | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-OPS-035` | `SR-OPS-002`: &#124; SR-OPS-002 &#124; **Health and readiness** endpoints per service; dependency health roll-up; SLO dashboards and alert rules shipped as code. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:910`; audit line 2151 | P0 | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-OPS-036` | `SR-OPS-003`: &#124; SR-OPS-003 &#124; **Support bundle:** one command/UI action produces a redacted diagnostic archive; customer reviews before sharing. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:911`; audit line 2152 | P0 | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-OPS-037` | `SR-OPS-004`: &#124; SR-OPS-004 &#124; **Telemetry to vendor is OFF by default;** optional, opt-in, content-free usage statistics with a visible schema. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:912`; audit line 2153 | P0 | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-OPS-038` | `SR-OPS-005`: &#124; SR-OPS-005 &#124; **Runbooks** for connector failure, DLQ drain, graph restore, schema/ontology migration rollback, model outage, egress incident, tenant isolation incident, key rotation, DR failover. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:913`; audit line 2154 | P0 | MISSED | [CP-06](#cp-06) | subject triage | TRACE/BUILD |
| `REQ-OPS-039` | `SR-OPS-006`: &#124; SR-OPS-006 &#124; **Cost/FinOps views** for cloud profiles (storage, compute, LLM tokens) and capacity views for on-prem. &#124; P2 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:914`; audit line 2155 | P2 | MISSED | [CP-19](#cp-19) | subject triage | TRACE/BUILD |
| `REQ-OPS-040` | `SR-QA-011`: &#124; SR-QA-011 &#124; A requirement is `Done` only if its mapped tests pass **and** a mutation/negative check proves the test fails when the behavior is broken (sampled per release). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:963`; audit line 2166 | P0 | IMPLEMENTED-UNVERIFIED | [CP-31](#cp-31) | area fallback | PROVE |
| `REQ-OPS-041` | `TASK-CTO-004`: - **TASK-CTO-004**: Design multi-region deployment architecture for global enterprise customers | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:30`; audit line 2290 | UNSTATED | MISSED | [CP-31](#cp-31) | subject triage | TRACE/BUILD |
| `REQ-OPS-042` | `TASK-CTO-015`: - **TASK-CTO-015**: Define disaster recovery architecture: RPO < 1 hour, RTO < 4 hours | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:99`; audit line 2301 | UNSTATED | MISSED | [CP-31](#cp-31) | subject triage | TRACE/BUILD |
| `REQ-OPS-043` | `TASK-DM-005`: - **TASK-DM-005**: Define release cadence: bi-weekly feature releases, monthly stable releases | `EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:36`; audit line 2325 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-OPS-044` | `TASK-LIC-008`: - **TASK-LIC-008**: Negotiate cloud provider agreements (AWS, Azure, GCP) for deployment | `EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:46`; audit line 2389 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-OPS-045` | `TASK-MKT-012`: - **TASK-MKT-012**: PR strategy for product launch — press release, media outreach | `EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:68`; audit line 2418 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-OPS-046` | `TEST-NFR-OPS-001`: &#124; NFR-OPS-001 &#124; Observability &#124; WP-SECURITY-OPS &#124; TEST-NFR-OPS-001 &#124; AC-NFR-OPS-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:91`; audit line 2556 | UNSTATED | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |
| `REQ-OPS-047` | `TEST-NFR-OPS-002`: &#124; NFR-OPS-002 &#124; Observability &#124; WP-SECURITY-OPS &#124; TEST-NFR-OPS-002 &#124; AC-NFR-OPS-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:92`; audit line 2557 | UNSTATED | MISSED | [CP-30](#cp-30) | subject triage | TRACE/BUILD |

### A.18 QRY: 74 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-QRY-001` | `AC-23`: &#124; AC-23 &#124; Visual query builder produces valid QueryPlans without writing code &#124; Linkurious (commercial) — KGR does it free &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1054`; audit line 121 | UNSTATED | MISSED | [CP-14](#cp-14) | subject triage | TRACE/BUILD |
| `REQ-QRY-002` | `AC-FR-QUERY-001`: &#124; FR-QUERY-001 &#124; Query Engine &#124; WP-QUERY &#124; TEST-FR-QUERY-001 &#124; AC-FR-QUERY-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:51`; audit line 191 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-003` | `AC-FR-QUERY-002`: &#124; FR-QUERY-002 &#124; Query Engine &#124; WP-QUERY &#124; TEST-FR-QUERY-002 &#124; AC-FR-QUERY-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:52`; audit line 192 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-004` | `AC-FR-QUERY-003`: &#124; FR-QUERY-003 &#124; Query Engine &#124; WP-QUERY &#124; TEST-FR-QUERY-003 &#124; AC-FR-QUERY-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:53`; audit line 193 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-005` | `AC-FR-QUERY-004`: &#124; FR-QUERY-004 &#124; Query Engine &#124; WP-QUERY &#124; TEST-FR-QUERY-004 &#124; AC-FR-QUERY-004 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:54`; audit line 194 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-006` | `AC-FR-QUERY-005`: &#124; FR-QUERY-005 &#124; Query Engine &#124; WP-QUERY &#124; TEST-FR-QUERY-005 &#124; AC-FR-QUERY-005 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:55`; audit line 195 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-007` | `AC-FR-QUERY-006`: &#124; FR-QUERY-006 &#124; Query Engine &#124; WP-QUERY &#124; TEST-FR-QUERY-006 &#124; AC-FR-QUERY-006 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:56`; audit line 196 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-008` | `AC-FR-QUERY-007`: &#124; FR-QUERY-007 &#124; Query Engine &#124; WP-QUERY &#124; TEST-FR-QUERY-007 &#124; AC-FR-QUERY-007 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:57`; audit line 197 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-009` | `AC-FR-QUERY-008`: &#124; FR-QUERY-008 &#124; Query Engine &#124; WP-QUERY &#124; TEST-FR-QUERY-008 &#124; AC-FR-QUERY-008 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:58`; audit line 198 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-010` | `AI-007.3`: - [x] `AI-007.3` Probabilistic query answering with confidence intervals | `eoip-phase4-2-requirements.md:786`; audit line 296 | UNSTATED | MISSED | [CP-34](#cp-34) | engine family | TRACE/BUILD |
| `REQ-QRY-011` | `CORE-003.8`: - [x] `CORE-003.8` Unit tests with diverse query types | `eoip-phase4-2-requirements.md:303`; audit line 441 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-QRY-012` | `CORE-004.2`: - [x] `CORE-004.2` Cross-layer query execution | `eoip-phase4-2-requirements.md:328`; audit line 444 | UNSTATED | MISSED | [CP-13](#cp-13) | engine family | TRACE/BUILD |
| `REQ-QRY-013` | `FR-KGR-013`: Implements FR-KGR-013. Matches Linkurious's no-code Query Builder (commercial). | `EOIP-engg-doc-pkg/KGR-implementation-plan.md:1403`; audit line 555 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-QRY-014` | `FR-QUERY-001`: Structured QueryPlan | `EOIP-engg-doc-pkg/03-functional-requirements.md:375`; audit line 580 | P0 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-QRY-015` | `FR-QUERY-002`: Path query | `EOIP-engg-doc-pkg/03-functional-requirements.md:385`; audit line 581 | P0 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-QRY-016` | `FR-QUERY-003`: Impact analysis | `EOIP-engg-doc-pkg/01-project-vision.md:25`; audit line 582 | P0 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-QRY-017` | `FR-QUERY-004`: Entity search | `EOIP-engg-doc-pkg/03-functional-requirements.md:405`; audit line 583 | P0 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-QRY-018` | `FR-QUERY-005`: Natural-language query interpretation | `EOIP-engg-doc-pkg/03-functional-requirements.md:415`; audit line 584 | P0 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-QRY-019` | `FR-QUERY-006`: Query safety policy | `EOIP-engg-doc-pkg/03-functional-requirements.md:425`; audit line 585 | P0 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-QRY-020` | `FR-QUERY-007`: Query evidence envelope | `EOIP-engg-doc-pkg/03-functional-requirements.md:435`; audit line 586 | P0 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-QRY-021` | `FR-QUERY-008`: Raw Gremlin admin boundary | `EOIP-engg-doc-pkg/03-functional-requirements.md:445`; audit line 587 | P0 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-QRY-022` | `FR-QUERY-009`: &#124; FR-QUERY-009 &#124; Natural-language query processor &#124; P1-MVP &#124; NLQ routes graph facts, query operators, QueryPlan execution and safe search fallback while returning answer text, confidence, highlights and follow-ups. \... | `EOIP-engg-doc-pkg/25-query-engine-requirements.md:30`; audit line 588 | P1 | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-023` | `GAP-AKO-010`: GAP-AKO-010: Query Optimization Agent | `EOIP-engg-doc-pkg/gaps-requirements.md:704`; audit line 1230 | P2 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | subject triage | PROVE |
| `REQ-QRY-024` | `GAP-CACHE-001`: GAP-CACHE-001: Cache by normalized semantic intent/query plan rather than raw prompt only | `EOIP-engg-doc-pkg/gaps-implementation.md:462`; audit line 1240 | P2 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | subject triage | PROVE |
| `REQ-QRY-025` | `GAP-CACHE-004`: GAP-CACHE-004: Separate deterministic query cache from AI response cache | `EOIP-engg-doc-pkg/gaps-requirements.md:891`; audit line 1243 | P2 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | subject triage | PROVE |
| `REQ-QRY-026` | `GAP-FABRIC-003`: GAP-FABRIC-003: Cost-aware query routing | `EOIP-engg-doc-pkg/gaps-requirements.md:640`; audit line 1305 | P1 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | subject triage | PROVE |
| `REQ-QRY-027` | `GAP-FABRIC-007`: GAP-FABRIC-007: Explain query routing | `EOIP-engg-doc-pkg/gaps-requirements.md:644`; audit line 1309 | P1 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | subject triage | PROVE |
| `REQ-QRY-028` | `GAP-HG-009`: GAP-HG-009: Gremlin query safety | `EOIP-engg-doc-pkg/gaps-requirements.md:1082`; audit line 1353 | P0 | IMPLEMENTED-UNVERIFIED | [CP-13](#cp-13) | ID family | PROVE |
| `REQ-QRY-029` | `GAP-MKT-003`: GAP-MKT-003: Package query templates | `EOIP-engg-doc-pkg/gaps-requirements.md:917`; audit line 1408 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-QRY-030` | `GAP-QI-001`: GAP-QI-001: Query plan explain | `EOIP-engg-doc-pkg/gaps-implementation.md:463`; audit line 1440 | P1 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-QRY-031` | `GAP-QI-003`: GAP-QI-003: Query history | `EOIP-engg-doc-pkg/gaps-requirements.md:875`; audit line 1442 | P1 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-QRY-032` | `GAP-QI-004`: GAP-QI-004: Slow-query analyzer | `EOIP-engg-doc-pkg/gaps-requirements.md:876`; audit line 1443 | P1 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-QRY-033` | `GAP-QI-007`: GAP-QI-007: Saved parameterized query templates | `EOIP-engg-doc-pkg/gaps-implementation.md:169`; audit line 1446 | P1 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-QRY-034` | `GAP-QUERY`: Unified semantic query API | `requirements-registry.json:1`; audit line 1448 | P1 | IMPLEMENTED-UNVERIFIED | [CP-07](#cp-07) | subject triage | PROVE |
| `REQ-QRY-035` | `GAP-QUERY-001`: GAP-QUERY-001: Provide one Unified Semantic Query API capable of routing internally to Gremlin, semantic/RDF adapter, search, vector or federated source | `EOIP-engg-doc-pkg/gaps-requirements.md:321`; audit line 1449 | P2 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | ID family | PROVE |
| `REQ-QRY-036` | `GAP-TEMP-002`: GAP-TEMP-002: Query “what was known at time T?” | `EOIP-engg-doc-pkg/gaps-requirements.md:569`; audit line 1499 | P1 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-QRY-037` | `GAP-TEMP-003`: GAP-TEMP-003: Query “what was actually valid at time T?” | `EOIP-engg-doc-pkg/gaps-requirements.md:570`; audit line 1500 | P1 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-QRY-038` | `KGR-G-024`: Polyglot Query Transpiler & NL2* Router | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:228`; audit line 1633 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-QRY-039` | `MVP-FR-013`: Query API | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:111`; audit line 1692 | P0 | IMPLEMENTED-UNVERIFIED | [CP-07](#cp-07) | subject triage | PROVE |
| `REQ-QRY-040` | `MVP-FR-014`: Impact analysis query | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:112`; audit line 1693 | P0 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | subject triage | PROVE |
| `REQ-QRY-041` | `MVP-FR-016`: Search/query UI | `EOIP-engg-doc-pkg/70-acceptance-criteria.md:114`; audit line 1695 | P0 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | subject triage | PROVE |
| `REQ-QRY-042` | `SDLC-015.4`: - [ ] `SDLC-015.4` Agent change log stored and queryable | `eoip-phase4-2-requirements.md:1679`; audit line 1858 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-QRY-043` | `SR-GDB-011`: &#124; SR-GDB-011 &#124; **Relational metadata/config store:** PostgreSQL as the clustered default, SQLite for single-node DP-0; ports allow customer-standard engines (SQL Server, Oracle, MySQL/MariaDB) at P2. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:216`; audit line 2049 | P2 | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-QRY-044` | `SR-NFR-003`: &#124; SR-NFR-003 &#124; **Query protection:** admission control, per-tenant concurrency, cost-based throttling, kill-runaway-query, result streaming and spill, plan caching. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:898`; audit line 2116 | P0 | MISSED | [CP-11](#cp-11) | subject triage | TRACE/BUILD |
| `REQ-QRY-045` | `SR-QRY-001`: &#124; SR-QRY-001 &#124; The compiler MUST accept EOQL, Gremlin, openCypher, GQL (subset first), SPARQL, SQL (analytics) and NL-produced plans, validate them against the ontology and the caller's policy, and lower them per the C... | `EOIP-engg-doc-pkg/super-requirements.md:312`; audit line 2170 | P0 | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-046` | `SR-QRY-002`: &#124; SR-QRY-002 &#124; **Never execute raw model- or user-generated graph queries** without schema-aware validation, policy rewrite, depth/timeout/expansion/cost limits and expensive-pattern detection. Raw dialect access is an... | `EOIP-engg-doc-pkg/super-requirements.md:313`; audit line 2171 | P0 | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-047` | `SR-QRY-003`: &#124; SR-QRY-003 &#124; **Query Explain:** every query returns (on request) the plan, chosen backend(s), pushdowns, estimated vs actual cost, and the generated dialect text. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:314`; audit line 2172 | P0 | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-048` | `SR-QRY-004`: &#124; SR-QRY-004 &#124; **Dialect round-trip tests:** a golden corpus (≥ 500 queries per Tier A backend, growing) MUST prove IR → dialect semantic equivalence by result comparison on shared fixtures. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:315`; audit line 2173 | P0 | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-049` | `SR-QRY-005`: &#124; SR-QRY-005 &#124; **Parameterization everywhere;** string-built queries are forbidden (injection defense). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:316`; audit line 2174 | P0 | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-050` | `SR-QRY-006`: &#124; SR-QRY-006 &#124; **Saved queries, query libraries, templates and versioned "question catalog"** per tenant/workspace, shareable and permission-aware. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:317`; audit line 2175 | P0 | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-051` | `SR-QRY-007`: &#124; SR-QRY-007 &#124; **Result envelope:** rows/graph/table/report + evidence IDs + method flags + freshness (as-of, lag) + coverage notes + policy filters applied. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:318`; audit line 2176 | P0 | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-052` | `SR-QRY-008`: &#124; SR-QRY-008 &#124; **Graph algorithm library** callable from plans (≥ 60 algorithms by P1): shortest/k-shortest/all-simple paths, reachability, SCC/WCC, topological order and cycle detection, dominators/critical path, Page... | `EOIP-engg-doc-pkg/super-requirements.md:319`; audit line 2177 | P1 | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-053` | `SR-QRY-009`: &#124; SR-QRY-009 &#124; **Incremental / precomputed accelerators:** transitive-closure or reachability indexes for impact queries, materialized views per persona, summary edges, and top-k caches, all invalidated by graph-revisi... | `EOIP-engg-doc-pkg/super-requirements.md:320`; audit line 2178 | P1 | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-054` | `SR-QRY-010`: &#124; SR-QRY-010 &#124; **Federated query** across backends and sites with per-source policy enforcement and partial results. &#124; P2 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:321`; audit line 2179 | P2 | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-055` | `SR-QRY-011`: &#124; SR-QRY-011 &#124; **Time travel:** `AS OF`, `BETWEEN`, `DIFF` over revisions for every query class where backends or the revision store allow. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:322`; audit line 2180 | P1 | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-056` | `SR-QRY-012`: &#124; SR-QRY-012 &#124; **Multilingual query front-ends** (NL, EOQL) with locale-aware date/number handling. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:323`; audit line 2181 | P1 | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-057` | `TASK-LD-014`: - **TASK-LD-014**: Fix pre-existing test failures (test_deployed_route_surface, test_intelligent_query latency) | `EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:74`; audit line 2364 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-QRY-058` | `TEST-FR-QUERY-001`: &#124; FR-QUERY-001 &#124; Query Engine &#124; WP-QUERY &#124; TEST-FR-QUERY-001 &#124; AC-FR-QUERY-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:51`; audit line 2532 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-059` | `TEST-FR-QUERY-002`: &#124; FR-QUERY-002 &#124; Query Engine &#124; WP-QUERY &#124; TEST-FR-QUERY-002 &#124; AC-FR-QUERY-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:52`; audit line 2533 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-060` | `TEST-FR-QUERY-003`: &#124; FR-QUERY-003 &#124; Query Engine &#124; WP-QUERY &#124; TEST-FR-QUERY-003 &#124; AC-FR-QUERY-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:53`; audit line 2534 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-061` | `TEST-FR-QUERY-004`: &#124; FR-QUERY-004 &#124; Query Engine &#124; WP-QUERY &#124; TEST-FR-QUERY-004 &#124; AC-FR-QUERY-004 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:54`; audit line 2535 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-062` | `TEST-FR-QUERY-005`: &#124; FR-QUERY-005 &#124; Query Engine &#124; WP-QUERY &#124; TEST-FR-QUERY-005 &#124; AC-FR-QUERY-005 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:55`; audit line 2536 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-063` | `TEST-FR-QUERY-006`: &#124; FR-QUERY-006 &#124; Query Engine &#124; WP-QUERY &#124; TEST-FR-QUERY-006 &#124; AC-FR-QUERY-006 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:56`; audit line 2537 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-064` | `TEST-FR-QUERY-007`: &#124; FR-QUERY-007 &#124; Query Engine &#124; WP-QUERY &#124; TEST-FR-QUERY-007 &#124; AC-FR-QUERY-007 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:57`; audit line 2538 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-065` | `TEST-FR-QUERY-008`: &#124; FR-QUERY-008 &#124; Query Engine &#124; WP-QUERY &#124; TEST-FR-QUERY-008 &#124; AC-FR-QUERY-008 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:58`; audit line 2539 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-066` | `WP-QUERY-01`: ### WP-QUERY-01 — Structured QueryPlan | `EOIP-engg-doc-pkg/implementation/wp-query.md:27`; audit line 2670 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-067` | `WP-QUERY-02`: ### WP-QUERY-02 — Path query | `EOIP-engg-doc-pkg/implementation/wp-query.md:36`; audit line 2671 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-068` | `WP-QUERY-03`: ### WP-QUERY-03 — Impact analysis | `EOIP-engg-doc-pkg/implementation/wp-query.md:45`; audit line 2672 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-069` | `WP-QUERY-04`: ### WP-QUERY-04 — Entity search | `EOIP-engg-doc-pkg/implementation/wp-query.md:54`; audit line 2673 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-070` | `WP-QUERY-05`: ### WP-QUERY-05 — Natural-language query interpretation | `EOIP-engg-doc-pkg/implementation/wp-query.md:63`; audit line 2674 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-071` | `WP-QUERY-06`: ### WP-QUERY-06 — Query safety policy | `EOIP-engg-doc-pkg/implementation/wp-query.md:72`; audit line 2675 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-072` | `WP-QUERY-07`: ### WP-QUERY-07 — Query evidence envelope | `EOIP-engg-doc-pkg/implementation/wp-query.md:81`; audit line 2676 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-073` | `WP-QUERY-08`: ### WP-QUERY-08 — Raw Gremlin admin boundary | `EOIP-engg-doc-pkg/implementation/wp-query.md:90`; audit line 2677 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |
| `REQ-QRY-074` | `WP-QUERY-09`: ### WP-QUERY-09 — Gremlin repository | `EOIP-engg-doc-pkg/implementation/wp-query.md:99`; audit line 2678 | UNSTATED | MISSED | [CP-14](#cp-14) | ID family | TRACE/BUILD |

### A.19 RAG: 48 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-RAG-001` | `AC-46`: &#124; AC-46 &#124; 8 engineering disciplines compose RAG + agents into higher-order intelligence &#124; Unique to KGR &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1077`; audit line 144 | UNSTATED | MISSED | [CP-21](#cp-21) | subject triage | TRACE/BUILD |
| `REQ-RAG-002` | `AC-FR-RAG-001`: &#124; FR-RAG-001 &#124; Retrieval/RAG &#124; WP-RAG &#124; TEST-FR-RAG-001 &#124; AC-FR-RAG-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:62`; audit line 199 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-003` | `AC-FR-RAG-002`: &#124; FR-RAG-002 &#124; Retrieval/RAG &#124; WP-RAG &#124; TEST-FR-RAG-002 &#124; AC-FR-RAG-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:63`; audit line 200 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-004` | `AC-FR-RAG-003`: &#124; FR-RAG-003 &#124; Retrieval/RAG &#124; WP-RAG &#124; TEST-FR-RAG-003 &#124; AC-FR-RAG-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:64`; audit line 201 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-005` | `AC-FR-RAG-004`: &#124; FR-RAG-004 &#124; Retrieval/RAG &#124; WP-RAG &#124; TEST-FR-RAG-004 &#124; AC-FR-RAG-004 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:65`; audit line 202 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-006` | `AC-FR-RAG-005`: &#124; FR-RAG-005 &#124; Retrieval/RAG &#124; WP-RAG &#124; TEST-FR-RAG-005 &#124; AC-FR-RAG-005 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:66`; audit line 203 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-007` | `AC-FR-RAG-006`: &#124; FR-RAG-006 &#124; Retrieval/RAG &#124; WP-RAG &#124; TEST-FR-RAG-006 &#124; AC-FR-RAG-006 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:67`; audit line 204 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-008` | `AIDLC-005`: &#124; Untested AI quality &#124; TEST-001..005 cover chaos, load, fuzz, performance and accessibility &#124; No requirement tests answer quality, groundedness, agent task success or injection resistance. See AIDLC-004, AIDLC-005, A... | `eoip-phase4-2-requirements.md:143`; audit line 319 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-RAG-009` | `AIDLC-011`: &#124; Untested AI quality &#124; TEST-001..005 cover chaos, load, fuzz, performance and accessibility &#124; No requirement tests answer quality, groundedness, agent task success or injection resistance. See AIDLC-004, AIDLC-005, A... | `eoip-phase4-2-requirements.md:143`; audit line 349 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-RAG-010` | `AIDLC-015.1`: - [ ] `AIDLC-015.1` Citation drill-down component | `eoip-phase4-2-requirements.md:2334`; audit line 370 | UNSTATED | MISSED | [CP-25](#cp-25) | subject triage | TRACE/BUILD |
| `REQ-RAG-011` | `FR-RAG-001`: Retrieval router | `EOIP-engg-doc-pkg/03-functional-requirements.md:485`; audit line 589 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-RAG-012` | `FR-RAG-002`: GraphRAG evidence retrieval | `EOIP-engg-doc-pkg/01-project-vision.md:26`; audit line 590 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-RAG-013` | `FR-RAG-003`: Local model abstraction | `EOIP-engg-doc-pkg/03-functional-requirements.md:505`; audit line 591 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-RAG-014` | `FR-RAG-004`: No mandatory vector DB in MVP | `EOIP-engg-doc-pkg/02-scope-and-objectives.md:25`; audit line 592 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-RAG-015` | `FR-RAG-005`: RAG evaluation harness | `EOIP-engg-doc-pkg/03-functional-requirements.md:525`; audit line 593 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-RAG-016` | `FR-RAG-006`: Adaptive RAG strategy framework | `EOIP-engg-doc-pkg/03-functional-requirements.md:535`; audit line 594 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-RAG-017` | `GAP-AI`: Evidence-addressable RAG | `requirements-registry.json:1`; audit line 1219 | P1 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | subject triage | PROVE |
| `REQ-RAG-018` | `GAP-RET-001`: GAP-RET-001: Implement retrieval router | `EOIP-engg-doc-pkg/gaps-implementation.md:458`; audit line 1452 | P0 | IMPLEMENTED-UNVERIFIED | [CP-20](#cp-20) | ID family | PROVE |
| `REQ-RAG-019` | `GAP-RET-002`: GAP-RET-002: Candidate retrievers: | `EOIP-engg-doc-pkg/gaps-requirements.md:656`; audit line 1453 | P0 | IMPLEMENTED-UNVERIFIED | [CP-20](#cp-20) | ID family | PROVE |
| `REQ-RAG-020` | `GAP-RET-005`: GAP-RET-005: Evaluate retrievers independently | `EOIP-engg-doc-pkg/gaps-requirements.md:667`; audit line 1456 | P0 | IMPLEMENTED-UNVERIFIED | [CP-20](#cp-20) | ID family | PROVE |
| `REQ-RAG-021` | `GAP-RET-006`: GAP-RET-006: Provide retrieval trace for debugging | `EOIP-engg-doc-pkg/gaps-requirements.md:668`; audit line 1457 | P0 | IMPLEMENTED-UNVERIFIED | [CP-20](#cp-20) | ID family | PROVE |
| `REQ-RAG-022` | `KGR-G-023`: 45+ Modality Unified Enterprise RAG Suite | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:227`; audit line 1632 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-RAG-023` | `PRE-001.2`: - [x] `PRE-001.2` Resolve baseline conflicts B1 to B3 against the code (database adapters 17+ vs 55, RAG modes 64 vs 45+, UI components 90+ vs 55) and correct the numbers in this file. | `eoip-phase4-2-requirements.md:197`; audit line 1754 | UNSTATED | MISSED | [CP-00](#cp-00) | ID family | TRACE/BUILD |
| `REQ-RAG-024` | `SR-QA-001`: &#124; SR-QA-001 &#124; Provide **synthetic dataset generators** per industry pack (referentially consistent, with planted ground-truth relationships, duplicates, drift, PII canaries and adversarial prompt-injection documents). ... | `EOIP-engg-doc-pkg/super-requirements.md:955`; audit line 2163 | P0 | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-RAG-025` | `SR-QA-002`: &#124; SR-QA-002 &#124; Each generator exposes scale knobs (S/M/L/XL) and ground-truth answers for the golden question sets. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:956`; audit line 2164 | P0 | MISSED | [CP-21](#cp-21) | area fallback | TRACE/BUILD |
| `REQ-RAG-026` | `SR-RAG-001`: &#124; SR-RAG-001 &#124; **Router** chooses strategy per query class with a logged rationale; operators can override per tenant/workspace; unknown classes degrade to hybrid retrieval with a visible notice. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:563`; audit line 2182 | P0 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-027` | `SR-RAG-002`: &#124; SR-RAG-002 &#124; **GraphRAG patterns:** local (entity-neighborhood + attached documents), global (community-summary map-reduce), path-based, subgraph-as-context, and temporal. &#124; P0 (local) / P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:564`; audit line 2183 | P0 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-028` | `SR-RAG-003`: &#124; SR-RAG-003 &#124; **Hybrid retrieval:** BM25 + dense (+ optional sparse-learned) with reciprocal-rank fusion, cross-encoder reranking (local models), metadata/policy filtering *before* ranking. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:565`; audit line 2184 | P0 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-029` | `SR-RAG-004`: &#124; SR-RAG-004 &#124; **Advanced strategies as plugins:** HyDE, query decomposition, step-back, RAG-Fusion, parent-child chunking, sentence-window, self-RAG/corrective-RAG, agentic RAG loops, long-context packing with budget ... | `EOIP-engg-doc-pkg/super-requirements.md:566`; audit line 2185 | P1 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-030` | `SR-RAG-005`: &#124; SR-RAG-005 &#124; **Graph-aware chunking:** chunk boundaries follow document structure and link to graph entities; every chunk carries `raw_id`, section path, classification, ontology links. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:567`; audit line 2186 | P0 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-031` | `SR-RAG-006`: &#124; SR-RAG-006 &#124; **Corrective verification:** before returning any LLM-generated assertion, verify entity/relationship claims against deterministic graph facts; unverifiable claims are removed or labeled. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:568`; audit line 2187 | P0 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-032` | `SR-RAG-007`: &#124; SR-RAG-007 &#124; **Context budget manager:** token-aware assembly, deduplication, evidence prioritization, and per-model context-window adaptation. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:569`; audit line 2188 | P0 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-033` | `SR-RAG-008`: &#124; SR-RAG-008 &#124; **Model-down fallback:** if no model is reachable, return deterministic results, retrieved evidence and templated narration with clear labeling (inherited `MVP-FR-020`). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:570`; audit line 2189 | P0 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-034` | `SR-RAG-009`: &#124; SR-RAG-009 &#124; **Caching:** semantic and exact caches keyed by tenant, policy version, graph revision and model version; invalidated by revision events. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:571`; audit line 2190 | P1 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-035` | `SR-RAG-010`: &#124; SR-RAG-010 &#124; **RAG evaluation harness** built in: retrieval precision/recall@k, MRR/nDCG, groundedness/faithfulness, citation precision, answer relevance, hallucination rate, latency, token cost; regression gates in ... | `EOIP-engg-doc-pkg/super-requirements.md:572`; audit line 2191 | P0 | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-036` | `TASK-LAI-005`: - **TASK-LAI-005**: Optimize RAG retrieval quality across 64 modes — identify top 10 most-used modes, benchmark accuracy | `EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:32`; audit line 2339 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-RAG-037` | `TEST-FR-RAG-001`: &#124; FR-RAG-001 &#124; Retrieval/RAG &#124; WP-RAG &#124; TEST-FR-RAG-001 &#124; AC-FR-RAG-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:62`; audit line 2540 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-038` | `TEST-FR-RAG-002`: &#124; FR-RAG-002 &#124; Retrieval/RAG &#124; WP-RAG &#124; TEST-FR-RAG-002 &#124; AC-FR-RAG-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:63`; audit line 2541 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-039` | `TEST-FR-RAG-003`: &#124; FR-RAG-003 &#124; Retrieval/RAG &#124; WP-RAG &#124; TEST-FR-RAG-003 &#124; AC-FR-RAG-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:64`; audit line 2542 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-040` | `TEST-FR-RAG-004`: &#124; FR-RAG-004 &#124; Retrieval/RAG &#124; WP-RAG &#124; TEST-FR-RAG-004 &#124; AC-FR-RAG-004 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:65`; audit line 2543 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-041` | `TEST-FR-RAG-005`: &#124; FR-RAG-005 &#124; Retrieval/RAG &#124; WP-RAG &#124; TEST-FR-RAG-005 &#124; AC-FR-RAG-005 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:66`; audit line 2544 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-042` | `TEST-FR-RAG-006`: &#124; FR-RAG-006 &#124; Retrieval/RAG &#124; WP-RAG &#124; TEST-FR-RAG-006 &#124; AC-FR-RAG-006 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:67`; audit line 2545 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-043` | `WP-RAG-01`: ### WP-RAG-01 — Retrieval router | `EOIP-engg-doc-pkg/implementation/wp-rag.md:24`; audit line 2679 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-044` | `WP-RAG-02`: ### WP-RAG-02 — GraphRAG evidence retrieval | `EOIP-engg-doc-pkg/implementation/wp-rag.md:33`; audit line 2680 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-045` | `WP-RAG-03`: ### WP-RAG-03 — Local model abstraction | `EOIP-engg-doc-pkg/implementation/wp-rag.md:42`; audit line 2681 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-046` | `WP-RAG-04`: ### WP-RAG-04 — No mandatory vector DB in MVP | `EOIP-engg-doc-pkg/implementation/wp-rag.md:51`; audit line 2682 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-047` | `WP-RAG-05`: ### WP-RAG-05 — RAG evaluation harness | `EOIP-engg-doc-pkg/implementation/wp-rag.md:60`; audit line 2683 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |
| `REQ-RAG-048` | `WP-RAG-06`: ### WP-RAG-06 — Adaptive RAG strategy framework | `EOIP-engg-doc-pkg/implementation/wp-rag.md:69`; audit line 2684 | UNSTATED | MISSED | [CP-21](#cp-21) | ID family | TRACE/BUILD |

### A.20 SCL: 31 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-SCL-001` | `AC-NFR-PERF-001`: &#124; NFR-PERF-001 &#124; Performance &#124; WP-SECURITY-OPS &#124; TEST-NFR-PERF-001 &#124; AC-NFR-PERF-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:93`; audit line 217 | UNSTATED | MISSED | [CP-32](#cp-32) | ID family | TRACE/BUILD |
| `REQ-SCL-002` | `CORE-003.2`: - [x] `CORE-003.2` Sub-10ms classification latency | `eoip-phase4-2-requirements.md:297`; audit line 435 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-SCL-003` | `CORE-003.3`: - [x] `CORE-003.3` RoutingDecision with cost/latency estimates | `eoip-phase4-2-requirements.md:298`; audit line 436 | UNSTATED | MISSED | [CP-19](#cp-19) | engine family | TRACE/BUILD |
| `REQ-SCL-004` | `G2-EKAF-011`: G2-EKAF-011 — Rate limiting | `EOIP-engg-doc-pkg/gaps2-requirements.md:230`; audit line 686 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-SCL-005` | `G2-PERF-001`: G2-PERF-001 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1735`; audit line 808 | P2 | IMPLEMENTED-UNVERIFIED | [CP-32](#cp-32) | ID family | PROVE |
| `REQ-SCL-006` | `G2-PERF-002`: G2-PERF-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1738`; audit line 809 | P2 | IMPLEMENTED-UNVERIFIED | [CP-32](#cp-32) | ID family | PROVE |
| `REQ-SCL-007` | `G2-PERF-003`: G2-PERF-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1741`; audit line 810 | P2 | IMPLEMENTED-UNVERIFIED | [CP-32](#cp-32) | ID family | PROVE |
| `REQ-SCL-008` | `G2-PERF-004`: G2-PERF-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1744`; audit line 811 | P2 | IMPLEMENTED-UNVERIFIED | [CP-32](#cp-32) | ID family | PROVE |
| `REQ-SCL-009` | `G2-PERF-005`: G2-PERF-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1747`; audit line 812 | P2 | IMPLEMENTED-UNVERIFIED | [CP-32](#cp-32) | ID family | PROVE |
| `REQ-SCL-010` | `G2-PERF-006`: G2-PERF-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1750`; audit line 813 | P2 | IMPLEMENTED-UNVERIFIED | [CP-32](#cp-32) | ID family | PROVE |
| `REQ-SCL-011` | `G2-PERF-007`: G2-PERF-007 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1753`; audit line 814 | P2 | IMPLEMENTED-UNVERIFIED | [CP-32](#cp-32) | ID family | PROVE |
| `REQ-SCL-012` | `G2-PERF-008`: G2-PERF-008 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1756`; audit line 815 | P2 | IMPLEMENTED-UNVERIFIED | [CP-32](#cp-32) | ID family | PROVE |
| `REQ-SCL-013` | `GAP-CACHE-005`: GAP-CACHE-005: Do not serve stale results beyond policy | `EOIP-engg-doc-pkg/gaps-requirements.md:892`; audit line 1244 | P2 | IMPLEMENTED-UNVERIFIED | [CP-32](#cp-32) | area fallback | PROVE |
| `REQ-SCL-014` | `GAP-PERF-001`: ## HugeGraph cluster / sharding notes (GAP-PERF-001/002, G2-SCALE-SHARD) | `EOIP-engg-doc-pkg/reference/deployment-ha.md:126`; audit line 1428 | UNSTATED | PARTIAL | [CP-32](#cp-32) | ID family | COMPLETE |
| `REQ-SCL-015` | `GAP-PERF-002`: &#124; GAP-PERF-002 &#124; HugeGraph distributed storage backend &#124; **Done** &#124; `EOIP_GRAPH_CLUSTER_MODE`, HA Compose HugeGraph PD/Store profiles, `build_shard_plan()`, `/api/v1/ops/shard-plan` &#124; | `docs/audit-2026-10-06/assessed-gap-report.md:452`; audit line 1429 | UNSTATED | MISSED | [CP-32](#cp-32) | ID family | TRACE/BUILD |
| `REQ-SCL-016` | `INFRA-001.1`: - [x] `INFRA-001.1` L1 + L2 cache hierarchy | `eoip-phase4-2-requirements.md:810`; audit line 1569 | UNSTATED | MISSED | [CP-03](#cp-03) | engine family | TRACE/BUILD |
| `REQ-SCL-017` | `INFRA-001.4`: - [x] `INFRA-001.4` Cache warming | `eoip-phase4-2-requirements.md:813`; audit line 1572 | UNSTATED | MISSED | [CP-03](#cp-03) | engine family | TRACE/BUILD |
| `REQ-SCL-018` | `NFR-KGR-001`: ### NFR-KGR-001: Performance | `EOIP-engg-doc-pkg/KGR-requirements.md:704`; audit line 1732 | UNSTATED | MISSED | [CP-32](#cp-32) | ID family | TRACE/BUILD |
| `REQ-SCL-019` | `PERF-01`: Formal NFR benchmark suite (Locust / pytest-benchmark) | `KGF-MASTER-BACKLOG.md:177`; audit line 1751 | P2 | IMPLEMENTED-UNVERIFIED | [CP-32](#cp-32) | ID family | PROVE |
| `REQ-SCL-020` | `REL-12`: Performance benchmark receipts | `KGF-MASTER-BACKLOG.md:162`; audit line 1774 | P0 | IMPLEMENTED-UNVERIFIED | [CP-36](#cp-36) | ID family | PROVE |
| `REQ-SCL-021` | `S-02`: Performance benchmarks | `requirements-registry.json:1`; audit line 1780 | P1 | IMPLEMENTED-UNVERIFIED | [CP-32](#cp-32) | subject triage | PROVE |
| `REQ-SCL-022` | `SDLC-025.3`: - [ ] `SDLC-025.3` Dashboards for latency and cost by span | `eoip-phase4-2-requirements.md:1865`; audit line 1907 | UNSTATED | MISSED | [CP-30](#cp-30) | engine family | TRACE/BUILD |
| `REQ-SCL-023` | `SR-VDB-003`: &#124; SR-VDB-003 &#124; **Index strategies configurable:** HNSW, IVF-PQ, DiskANN-class disk indexes, scalar/product/binary quantization, filtered-search strategies, per-collection recall/latency targets. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:229`; audit line 2230 | P1 | MISSED | [CP-20](#cp-20) | ID family | TRACE/BUILD |
| `REQ-SCL-024` | `TASK-ARCH-010`: - **TASK-ARCH-010**: Design multi-level cache topology for INFRA-001 (L1 in-process, L2 Redis, invalidation protocol) | `EOIP-engg-doc-pkg/roles/Architect_tasks.md:51`; audit line 2266 | UNSTATED | MISSED | [CP-32](#cp-32) | area fallback | TRACE/BUILD |
| `REQ-SCL-025` | `TASK-ARCH-015`: - **TASK-ARCH-015**: Define performance budgets per engine: max latency, max memory, max CPU per request | `EOIP-engg-doc-pkg/roles/Architect_tasks.md:74`; audit line 2271 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-SCL-026` | `TASK-ARCH-016`: - **TASK-ARCH-016**: Design for horizontal scalability — stateless engines, shared-nothing where possible | `EOIP-engg-doc-pkg/roles/Architect_tasks.md:78`; audit line 2272 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-SCL-027` | `TASK-CTO-011`: - **TASK-CTO-011**: Design Intent Router (CORE-003) classifier architecture for production-grade sub-10ms latency | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:75`; audit line 2297 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-SCL-028` | `TASK-CTO-017`: - **TASK-CTO-017**: Define SLA targets for API endpoints: p99 latency, availability, error budget | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:112`; audit line 2303 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-SCL-029` | `TASK-LD-015`: - **TASK-LD-015**: Evaluate engine import chain performance — current pytest collection takes 60-120s due to 500+ module imports | `EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:78`; audit line 2365 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-SCL-030` | `TASK-QAL-010`: - **TASK-QAL-010**: Set up performance regression detection in CI (TEST-004) | `EOIP-engg-doc-pkg/roles/QALead_tasks.md:56`; audit line 2443 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-SCL-031` | `TEST-NFR-PERF-001`: &#124; NFR-PERF-001 &#124; Performance &#124; WP-SECURITY-OPS &#124; TEST-NFR-PERF-001 &#124; AC-NFR-PERF-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:93`; audit line 2558 | UNSTATED | MISSED | [CP-32](#cp-32) | ID family | TRACE/BUILD |

### A.21 SEC: 169 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-SEC-001` | `AC-NFR-PRIV-001`: &#124; NFR-PRIV-001 &#124; Privacy &#124; WP-SECURITY-OPS &#124; TEST-NFR-PRIV-001 &#124; AC-NFR-PRIV-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:95`; audit line 218 | UNSTATED | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-SEC-002` | `AC-NFR-REL-001`: &#124; NFR-REL-001 &#124; Reliability &#124; WP-SECURITY-OPS &#124; TEST-NFR-REL-001 &#124; AC-NFR-REL-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:89`; audit line 219 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-003` | `AC-NFR-REL-002`: &#124; NFR-REL-002 &#124; Reliability &#124; WP-SECURITY-OPS &#124; TEST-NFR-REL-002 &#124; AC-NFR-REL-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:90`; audit line 220 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-004` | `AC-NFR-SEC-001`: &#124; NFR-SEC-001 &#124; Security &#124; WP-SECURITY-OPS &#124; TEST-NFR-SEC-001 &#124; AC-NFR-SEC-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:82`; audit line 221 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-005` | `AC-NFR-SEC-002`: &#124; NFR-SEC-002 &#124; Security &#124; WP-SECURITY-OPS &#124; TEST-NFR-SEC-002 &#124; AC-NFR-SEC-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:83`; audit line 222 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-006` | `AC-NFR-SEC-003`: &#124; NFR-SEC-003 &#124; Security &#124; WP-SECURITY-OPS &#124; TEST-NFR-SEC-003 &#124; AC-NFR-SEC-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:84`; audit line 223 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-007` | `AC-NFR-SEC-004`: &#124; NFR-SEC-004 &#124; Security &#124; WP-SECURITY-OPS &#124; TEST-NFR-SEC-004 &#124; AC-NFR-SEC-004 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:85`; audit line 224 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-008` | `AC-NFR-SEC-005`: &#124; NFR-SEC-005 &#124; Security &#124; WP-SECURITY-OPS &#124; TEST-NFR-SEC-005 &#124; AC-NFR-SEC-005 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:86`; audit line 225 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-009` | `AC-NFR-SEC-006`: &#124; NFR-SEC-006 &#124; Security &#124; WP-SECURITY-OPS &#124; TEST-NFR-SEC-006 &#124; AC-NFR-SEC-006 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:87`; audit line 226 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-010` | `AC-NFR-SEC-007`: &#124; NFR-SEC-007 &#124; Security &#124; WP-SECURITY-OPS &#124; TEST-NFR-SEC-007 &#124; AC-NFR-SEC-007 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:88`; audit line 227 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-011` | `AIDLC-016.3`: - [ ] `AIDLC-016.3` Tenant override audited | `eoip-phase4-2-requirements.md:2296`; audit line 377 | UNSTATED | MISSED | [CP-10](#cp-10) | subject triage | TRACE/BUILD |
| `REQ-SEC-012` | `CG-GAP-004`: Triage the 1,199 unmapped documentation-audit records | `EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:65`; audit line 390 | P0 | PARTIAL | [CP-00](#cp-00) | ID family | COMPLETE |
| `REQ-SEC-013` | `CG-GAP-009`: Generated audit artifacts policy | `EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:70`; audit line 395 | P2 | PARTIAL | [CP-09](#cp-09) | area fallback | COMPLETE |
| `REQ-SEC-014` | `COMPLY-002`: Automated PII Detection & Anonymization | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:854`; audit line 402 | P1 | IMPLEMENTED-UNVERIFIED | [CP-33](#cp-33) | ID family | PROVE |
| `REQ-SEC-015` | `COMPLY-003.4`: - [x] `COMPLY-003.4` Audit export | `eoip-phase4-2-requirements.md:1215`; audit line 412 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-SEC-016` | `CORE-002.5`: - [x] `CORE-002.5` Verification audit trail | `eoip-phase4-2-requirements.md:269`; audit line 429 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-SEC-017` | `FR-001`: &#124; FR-001 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:847`; audit line 467 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-018` | `FR-002`: &#124; FR-002 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:848`; audit line 468 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-019` | `FR-003`: &#124; FR-003 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:849`; audit line 469 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-020` | `FR-004`: &#124; FR-004 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:850`; audit line 470 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-021` | `FR-005`: &#124; FR-005 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:851`; audit line 471 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-022` | `FR-006`: &#124; FR-006 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:852`; audit line 472 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-023` | `FR-007`: &#124; FR-007 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:853`; audit line 473 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-024` | `FR-008`: &#124; FR-008 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:854`; audit line 474 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-025` | `FR-009`: &#124; FR-009 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:855`; audit line 475 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-026` | `FR-010`: &#124; FR-010 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:856`; audit line 477 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-027` | `FR-011`: &#124; FR-011 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:857`; audit line 478 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-028` | `FR-012`: &#124; FR-012 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:858`; audit line 479 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-029` | `FR-013`: &#124; FR-013 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:859`; audit line 480 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-030` | `FR-014`: &#124; FR-014 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:860`; audit line 481 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-031` | `FR-015`: &#124; FR-015 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:861`; audit line 482 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-032` | `FR-016`: &#124; FR-016 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:862`; audit line 483 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-033` | `FR-017`: &#124; FR-017 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:863`; audit line 484 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-034` | `FR-018`: &#124; FR-018 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:864`; audit line 485 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-035` | `FR-019`: &#124; FR-019 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:865`; audit line 486 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-036` | `FR-020`: &#124; FR-020 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:866`; audit line 488 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-037` | `FR-021`: &#124; FR-021 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:867`; audit line 489 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-038` | `FR-022`: &#124; FR-022 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:868`; audit line 490 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-039` | `FR-023`: &#124; FR-023 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:869`; audit line 491 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-040` | `FR-024`: &#124; FR-024 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:870`; audit line 492 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-041` | `FR-025`: &#124; FR-025 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:871`; audit line 493 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-042` | `FR-026`: &#124; FR-026 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:872`; audit line 494 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-043` | `FR-027`: &#124; FR-027 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:873`; audit line 495 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-044` | `FR-028`: &#124; FR-028 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2365 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish ac... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:874`; audit line 496 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-045` | `FR-KGR-022`: ### FR-KGR-022: Lasso/Rectangle Multi-Selection | `EOIP-engg-doc-pkg/KGR-requirements.md:553`; audit line 564 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-SEC-046` | `G2-EKAF-020`: G2-EKAF-020 — Authentication isolation | `EOIP-engg-doc-pkg/gaps2-requirements.md:287`; audit line 695 | P2 | IMPLEMENTED-UNVERIFIED | [CP-34](#cp-34) | ID family | PROVE |
| `REQ-SEC-047` | `G2-GRAPH-SEC-001`: G2-GRAPH-SEC-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:620`; audit line 747 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-SEC-048` | `G2-GRAPH-SEC-002`: G2-GRAPH-SEC-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:925`; audit line 748 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-SEC-049` | `G2-GRAPH-SEC-003`: G2-GRAPH-SEC-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:928`; audit line 749 | P2 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-SEC-050` | `G2-SEC-CRAWL-001`: G2-SEC-CRAWL-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:140`; audit line 839 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-SEC-051` | `G2-SEC-CRAWL-002`: G2-SEC-CRAWL-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1665`; audit line 840 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-SEC-052` | `G2-SEC-CRAWL-003`: G2-SEC-CRAWL-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1668`; audit line 841 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-SEC-053` | `G2-SEC-CRAWL-004`: G2-SEC-CRAWL-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1671`; audit line 842 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-SEC-054` | `G2-SEC-CRAWL-005`: G2-SEC-CRAWL-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1674`; audit line 843 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-SEC-055` | `G2-SEC-CRAWL-006`: G2-SEC-CRAWL-006 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1677`; audit line 844 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-SEC-056` | `G2-SEC-CRAWL-007`: G2-SEC-CRAWL-007 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1680`; audit line 845 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-SEC-057` | `G2-SEC-CRAWL-008`: G2-SEC-CRAWL-008 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1683`; audit line 846 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-SEC-058` | `G2-SEC-CRAWL-009`: G2-SEC-CRAWL-009 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1686`; audit line 847 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-SEC-059` | `G2-SEC-CRAWL-010`: G2-SEC-CRAWL-010 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1689`; audit line 848 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-SEC-060` | `G2-SEC-CRAWL-011`: G2-SEC-CRAWL-011 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1692`; audit line 849 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-SEC-061` | `G2-SEC-CRAWL-012`: G2-SEC-CRAWL-012 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1695`; audit line 850 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-SEC-062` | `G2-T0001`: ### G2-T0001 — Audit current contracts | `EOIP-engg-doc-pkg/gaps2-implementation.md:64`; audit line 949 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-063` | `GAP-002`: &#124; GAP-002 &#124; Partial &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:63 &#124; scripts/tick_phase0_phase1.py:13 &#124; Inspect cited code/tests and derive atomic acceptance checks; bind fresh results before complet... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1342`; audit line 1198 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-064` | `GAP-003`: &#124; GAP-003 &#124; Partial &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:64 &#124; scripts/tick_phase0_phase1.py:9 &#124; Inspect cited code/tests and derive atomic acceptance checks; bind fresh results before completi... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1343`; audit line 1199 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-065` | `GAP-004`: &#124; GAP-004 &#124; Partial &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:65 &#124; scripts/tick_phase0_phase1.py:9 &#124; Inspect cited code/tests and derive atomic acceptance checks; bind fresh results before completi... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1344`; audit line 1200 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-066` | `GAP-005`: &#124; GAP-005 &#124; Partial &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:66 &#124; scripts/check_markdown_links.py:1; scripts/tick_phase0_phase1.py:9 &#124; Inspect cited code/tests and derive atomic acceptance checks;... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1345`; audit line 1201 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-067` | `GAP-006`: &#124; GAP-006 &#124; Partial &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:67 &#124; scripts/tick_phase0_phase1.py:13 &#124; Inspect cited code/tests and derive atomic acceptance checks; bind fresh results before complet... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1346`; audit line 1202 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-068` | `GAP-007`: &#124; GAP-007 &#124; Partial &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:68 &#124; scripts/tick_phase0_phase1.py:9 &#124; Inspect cited code/tests and derive atomic acceptance checks; bind fresh results before completi... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1347`; audit line 1203 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-069` | `GAP-008`: &#124; GAP-008 &#124; Missing &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:69 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish acceptance criteria and phase dependencies. &#124; | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1348`; audit line 1204 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-070` | `GAP-009`: &#124; GAP-009 &#124; Partial &#124; unassessed / P2 &#124; EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:70 &#124; scripts/tick_phase0_phase1.py:9 &#124; Inspect cited code/tests and derive atomic acceptance checks; bind fresh results before completi... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1349`; audit line 1205 | P2 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-071` | `GAP-KFW-002`: GAP-KFW-002: Detect secrets, PII, credentials, regulated data and restricted classifications | `EOIP-engg-doc-pkg/gaps-requirements.md:736`; audit line 1358 | P2 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | ID family | PROVE |
| `REQ-SEC-072` | `GAP-SEC-001`: GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | `EOIP-engg-doc-pkg/gaps-requirements.md:783`; audit line 1472 | P1 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | area fallback | PROVE |
| `REQ-SEC-073` | `GAP-SEC-002`: GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1603`; audit line 1473 | P1 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | area fallback | PROVE |
| `REQ-SEC-074` | `GAP-SEC-003`: GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1604`; audit line 1474 | P1 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | area fallback | PROVE |
| `REQ-SEC-075` | `GAP-SEC-004`: GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1605`; audit line 1475 | P1 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | area fallback | PROVE |
| `REQ-SEC-076` | `GAP-SEC-005`: GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1606`; audit line 1476 | P1 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | area fallback | PROVE |
| `REQ-SEC-077` | `GAP-SEC-006`: GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1607`; audit line 1477 | P1 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | area fallback | PROVE |
| `REQ-SEC-078` | `GAP-SEC-007`: GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1608`; audit line 1478 | P1 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | area fallback | PROVE |
| `REQ-SEC-079` | `GAP-SEC-008`: GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | `KGF-MASTER-BACKLOG.md:997`; audit line 1479 | P1 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | area fallback | PROVE |
| `REQ-SEC-080` | `GAP-SEC-009`: GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | `KGF-MASTER-BACKLOG.md:1008`; audit line 1480 | P1 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | area fallback | PROVE |
| `REQ-SEC-081` | `GAP-SEC-010`: GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | `KGF-MASTER-BACKLOG.md:1009`; audit line 1481 | P1 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | area fallback | PROVE |
| `REQ-SEC-082` | `GAP-SEC-011`: GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | `KGF-MASTER-BACKLOG.md:1010`; audit line 1482 | P1 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | area fallback | PROVE |
| `REQ-SEC-083` | `GAP-SEC-012`: GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | `EOIP-engg-doc-pkg/gaps-requirements.md:783`; audit line 1483 | P1 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | area fallback | PROVE |
| `REQ-SEC-084` | `GAP-TEMPLATE-001`: GAP-TEMPLATE-001: Provide packaged templates for engineering, audit, risk, incident, architecture and compliance use cases | `EOIP-engg-doc-pkg/gaps-implementation.md:784`; audit line 1505 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | subject triage | PROVE |
| `REQ-SEC-085` | `H-04`: Auth/RBAC enforcement | `KGF-MASTER-BACKLOG.md:274`; audit line 1563 | P0 | IMPLEMENTED-UNVERIFIED | [CP-05](#cp-05) | subject triage | PROVE |
| `REQ-SEC-086` | `H-07`: Error handling audit | `KGF-MASTER-BACKLOG.md:281`; audit line 1566 | P0 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | area fallback | PROVE |
| `REQ-SEC-087` | `INFRA-002`: OAuth2/OIDC/SSO Integration | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:558`; audit line 1574 | P1 | IMPLEMENTED-UNVERIFIED | [CP-04](#cp-04) | engine family | PROVE |
| `REQ-SEC-088` | `INFRA-002.1`: - [x] `INFRA-002.1` OAuth2 authorization code flow | `eoip-phase4-2-requirements.md:834`; audit line 1575 | UNSTATED | MISSED | [CP-04](#cp-04) | engine family | TRACE/BUILD |
| `REQ-SEC-089` | `INFRA-002.2`: - [x] `INFRA-002.2` OIDC discovery and verification | `eoip-phase4-2-requirements.md:835`; audit line 1576 | UNSTATED | MISSED | [CP-04](#cp-04) | engine family | TRACE/BUILD |
| `REQ-SEC-090` | `INFRA-002.3`: - [x] `INFRA-002.3` SAML adapter | `eoip-phase4-2-requirements.md:836`; audit line 1577 | UNSTATED | MISSED | [CP-04](#cp-04) | engine family | TRACE/BUILD |
| `REQ-SEC-091` | `MVP-P6`: &#124; MVP-P6 &#124; Security, Operations, Deployment, And Validation &#124; Implement Docker local deployment, secrets examples, health checks, observability, backup/restore, security/privacy controls, test strategy, benchmarking, ... | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md:50`; audit line 1715 | UNSTATED | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-SEC-092` | `NFR-001`: &#124; NFR-001 &#124; Missing &#124; unassessed / P1 &#124; EOIP-engg-doc-pkg/audits/historical/eoip-development-audit-2026-10-03.md:106 &#124; No literal-ID lead &#124; Trace behavior semantically before implementing; establish acceptance crit... | `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1679`; audit line 1717 | P1 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-093` | `NFR-KGR-005`: ### NFR-KGR-005: Security | `EOIP-engg-doc-pkg/KGR-requirements.md:732`; audit line 1736 | UNSTATED | MISSED | [CP-32](#cp-32) | ID family | TRACE/BUILD |
| `REQ-SEC-094` | `REL-05`: Documentation audit re-run and regenerated | `KGF-MASTER-BACKLOG.md:245`; audit line 1767 | P0 | IMPLEMENTED-UNVERIFIED | [CP-36](#cp-36) | ID family | PROVE |
| `REQ-SEC-095` | `REL-11`: Security certification receipts | `KGF-MASTER-BACKLOG.md:1213`; audit line 1773 | P0 | IMPLEMENTED-UNVERIFIED | [CP-36](#cp-36) | ID family | PROVE |
| `REQ-SEC-096` | `REL-15`: Close-out re-audit, registry reconciliation and release tag | `KGF-MASTER-BACKLOG.md:1252`; audit line 1777 | P0 | IMPLEMENTED-UNVERIFIED | [CP-36](#cp-36) | ID family | PROVE |
| `REQ-SEC-097` | `S-05`: Security hardening | `requirements-registry.json:1`; audit line 1783 | P1 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | area fallback | PROVE |
| `REQ-SEC-098` | `SDLC-006.1`: - [ ] `SDLC-006.1` Flag service with audit trail | `eoip-phase4-2-requirements.md:1506`; audit line 1810 | UNSTATED | MISSED | [CP-28](#cp-28) | engine family | TRACE/BUILD |
| `REQ-SEC-099` | `SDLC-008.4`: - [ ] `SDLC-008.4` Decisions are in the audit ledger | `eoip-phase4-2-requirements.md:1547`; audit line 1823 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-SEC-100` | `SDLC-012.2`: - [ ] `SDLC-012.2` Planted-PII and contradiction modes | `eoip-phase4-2-requirements.md:1622`; audit line 1841 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-SEC-101` | `SDLC-015.3`: - [ ] `SDLC-015.3` Second-review rule for P0/security paths | `eoip-phase4-2-requirements.md:1678`; audit line 1857 | P0 | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-SEC-102` | `SDLC-021`: ###### SDLC-021: Continuous security testing pipeline | `eoip-phase4-2-requirements.md:1771`; audit line 1884 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-SEC-103` | `SDLC-021.1`: - [ ] `SDLC-021.1` SAST, dependency, container and secrets scans in CI | `eoip-phase4-2-requirements.md:1784`; audit line 1885 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-SEC-104` | `SDLC-023`: ###### SDLC-023: Kubernetes production profile and secrets management | `eoip-phase4-2-requirements.md:1810`; audit line 1894 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-SEC-105` | `SDLC-023.3`: - [ ] `SDLC-023.3` Secrets never in plain values | `eoip-phase4-2-requirements.md:1826`; audit line 1897 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-SEC-106` | `SR-CFG-002`: &#124; SR-CFG-002 &#124; **Floors and ceilings:** upper layers may set security/compliance *floors* and *ceilings* lower layers cannot loosen (e.g., tenant cannot enable external LLMs beyond partner-allowed levels). Most-restric... | `EOIP-engg-doc-pkg/super-requirements.md:748`; audit line 1988 | P0 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-SEC-107` | `SR-COM-003`: &#124; SR-COM-003 &#124; **Legal and procurement kit:** EULA, MSA, DPA, SLA, OEM and partner agreements, BAA template, security questionnaire answers (SIG/CAIQ-style), SBOM and third-party notices, export-control classification,... | `EOIP-engg-doc-pkg/super-requirements.md:1002`; audit line 1995 | P0 | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-SEC-108` | `SR-DEP-002`: &#124; SR-DEP-002 &#124; **Helm charts/operators** for Kubernetes (HA, autoscaling, network policies, pod security, PDBs) for DP-1…DP-4. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:923`; audit line 2020 | P1 | MISSED | [CP-31](#cp-31) | ID family | TRACE/BUILD |
| `REQ-SEC-109` | `SR-EXT-014`: &#124; SR-EXT-014 &#124; **Marketplace** (online catalog for connected profiles; **offline catalog bundles** for air-gapped): ratings, security scan results, certification badges, revenue-share support. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:790`; audit line 2037 | P1 | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-SEC-110` | `SR-QA-014`: &#124; SR-QA-014 &#124; Linters/type-checkers/security scanners run at zero-error policy on main (the prior baseline carried 165 lint errors, mostly mechanical). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:966`; audit line 2169 | P0 | IMPLEMENTED-UNVERIFIED | [CP-09](#cp-09) | area fallback | PROVE |
| `REQ-SEC-111` | `SR-SEC-001`: &#124; SR-SEC-001 &#124; **Authentication:** OIDC, SAML 2.0, LDAP/AD, SCIM 2.0 provisioning, local break-glass accounts, MFA (TOTP, WebAuthn/FIDO2), scoped API keys, OAuth2 client credentials, mTLS service identities, short-live... | `EOIP-engg-doc-pkg/super-requirements.md:824`; audit line 2192 | P0 | MISSED | [CP-04](#cp-04) | subject triage | TRACE/BUILD |
| `REQ-SEC-112` | `SR-SEC-002`: &#124; SR-SEC-002 &#124; **Authorization:** RBAC + ABAC + relationship-based (Zanzibar-style) checks + classification-based mandatory access; evaluated by a policy engine (policy-as-code, OPA/Cedar-class) with a test and **"what... | `EOIP-engg-doc-pkg/super-requirements.md:825`; audit line 2193 | P0 | MISSED | [CP-05](#cp-05) | subject triage | TRACE/BUILD |
| `REQ-SEC-113` | `SR-SEC-003`: &#124; SR-SEC-003 &#124; **Element-level security:** policies apply to vertices, edges, properties and derived structures (embeddings, summaries, communities, caches); query-time policy rewriting and result filtering; field mask... | `EOIP-engg-doc-pkg/super-requirements.md:826`; audit line 2194 | P0 | MISSED | [CP-20](#cp-20) | subject triage | TRACE/BUILD |
| `REQ-SEC-114` | `SR-SEC-004`: &#124; SR-SEC-004 &#124; **Permission-aware ingestion and retrieval:** where the source provides ACLs/permissions, the connector ingests and maps them so answers include only what the asking user could access in the source syste... | `EOIP-engg-doc-pkg/super-requirements.md:827`; audit line 2195 | P0 | MISSED | [CP-05](#cp-05) | subject triage | TRACE/BUILD |
| `REQ-SEC-115` | `SR-SEC-005`: &#124; SR-SEC-005 &#124; **Access governance:** access reviews/certification campaigns, privileged-access workflows, break-glass with mandatory post-hoc review. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:828`; audit line 2196 | P1 | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-SEC-116` | `SR-SEC-006`: &#124; SR-SEC-006 &#124; **Agent identities** are first-class principals with least-privilege roles and budgets; agents never inherit a human's full rights implicitly. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:829`; audit line 2197 | P0 | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-SEC-117` | `SR-SEC-010`: &#124; SR-SEC-010 &#124; **Encryption:** TLS 1.3 externally, mTLS internally; at-rest encryption for all stores; field-level encryption for sensitive properties; KMS/HSM integration (PKCS#11, KMIP, cloud KMS adapters); rotation;... | `EOIP-engg-doc-pkg/super-requirements.md:835`; audit line 2198 | P0 | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-118` | `SR-SEC-011`: &#124; SR-SEC-011 &#124; **Secrets:** mounted files/secret store only; no secrets in environment variables, images, logs, graph or embeddings; automated secret scanning on ingested content with quarantine. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:836`; audit line 2199 | P0 | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-SEC-119` | `SR-SEC-012`: &#124; SR-SEC-012 &#124; **Audit:** immutable, hash-chained, signed, exportable (WORM option, SIEM formats); covers authN/Z decisions, config, data access (detail configurable), policy decisions, egress manifests, admin and agen... | `EOIP-engg-doc-pkg/super-requirements.md:837`; audit line 2200 | P0 | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-SEC-120` | `SR-SEC-013`: &#124; SR-SEC-013 &#124; **Hardening:** non-root containers, read-only root FS, dropped capabilities, seccomp/AppArmor profiles, minimal signed base images, network segmentation, CIS-aligned benchmarks. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:838`; audit line 2201 | P0 | MISSED | [CP-31](#cp-31) | subject triage | TRACE/BUILD |
| `REQ-SEC-121` | `SR-SEC-014`: &#124; SR-SEC-014 &#124; **Supply chain:** SBOM (CycloneDX/SPDX) per image and release, VEX, signed images/artifacts (Sigstore/cosign-class), SLSA-aligned provenance, pinned and reproducible builds, license scanning, dependency ... | `EOIP-engg-doc-pkg/super-requirements.md:839`; audit line 2202 | P0 | MISSED | [CP-33](#cp-33) | subject triage | TRACE/BUILD |
| `REQ-SEC-122` | `SR-SEC-015`: &#124; SR-SEC-015 &#124; **Secure SDLC:** threat models (STRIDE + LLM-specific + multi-tenant), SAST/DAST/SCA/fuzzing in CI, annual independent penetration test, vulnerability disclosure program, patch SLAs, security advisories ... | `EOIP-engg-doc-pkg/super-requirements.md:840`; audit line 2203 | P0 | MISSED | [CP-06](#cp-06) | subject triage | TRACE/BUILD |
| `REQ-SEC-123` | `SR-SEC-016`: &#124; SR-SEC-016 &#124; **Web and API defenses:** CSP, CSRF/XSS protections, SSRF guards for connectors and model endpoints, input validation, request size/time limits, DoS and abuse controls. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:841`; audit line 2204 | P0 | MISSED | [CP-08](#cp-08) | subject triage | TRACE/BUILD |
| `REQ-SEC-124` | `SR-SEC-017`: &#124; SR-SEC-017 &#124; **LLM-specific security:** prompt-injection and data-exfiltration test corpus, output filtering, tool-permission enforcement, context isolation per tenant/user (aligned with OWASP LLM Top-10 categories).... | `EOIP-engg-doc-pkg/super-requirements.md:842`; audit line 2205 | P0 | MISSED | [CP-05](#cp-05) | subject triage | TRACE/BUILD |
| `REQ-SEC-125` | `SR-WL-002`: &#124; SR-WL-002 &#124; **Domain and identity:** custom domains/CNAMEs, tenant-supplied TLS certs, branded login/SSO pages, branded transactional email, branded PDF/DOCX/PPTX/HTML reports. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:734`; audit line 2236 | P0 | STUBBED | [CP-28](#cp-28) | explicit | REPLACE |
| `REQ-SEC-126` | `TASK-CTO-013`: - **TASK-CTO-013**: Approve security architecture: auth flow, encryption at rest/transit, key management | `EOIP-engg-doc-pkg/roles/CTO_tasks.md:88`; audit line 2299 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-127` | `TASK-DM-009`: - **TASK-DM-009**: Sprint retrospectives documenting lessons learned and process improvements | `EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:57`; audit line 2329 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-SEC-128` | `TASK-DM-014`: - **TASK-DM-014**: Coordinate cross-role handoffs (QA ↔ Dev, Security ↔ Dev, Legal ↔ Marketing) | `EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:86`; audit line 2334 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-SEC-129` | `TASK-LEGAL-003`: - **TASK-LEGAL-003**: Trade secret identification — classify proprietary algorithms not suitable for patenting | `EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:26`; audit line 2369 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-SEC-130` | `TASK-LEGAL-004`: - **TASK-LEGAL-004**: Audit all dependencies for license compatibility (GPL, LGPL, Apache, MIT, BSD) | `EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:31`; audit line 2370 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-SEC-131` | `TASK-LEGAL-010`: - **TASK-LEGAL-010**: Draft Business Associate Agreement (BAA) for HIPAA-regulated customers | `EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:61`; audit line 2376 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-SEC-132` | `TASK-SEC-001`: - **TASK-SEC-001**: Conduct threat model (STRIDE) for EOIP platform — identify attack surfaces across 21+ engines, 133+ API endpoints | `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:11`; audit line 2447 | UNSTATED | MISSED | [CP-07](#cp-07) | subject triage | TRACE/BUILD |
| `REQ-SEC-133` | `TASK-SEC-002`: - **TASK-SEC-002**: Define security policy for agent tool execution — what agents can call, permission boundaries | `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:16`; audit line 2448 | UNSTATED | MISSED | [CP-05](#cp-05) | subject triage | TRACE/BUILD |
| `REQ-SEC-134` | `TASK-SEC-003`: - **TASK-SEC-003**: Define encryption standards — AES-256 at rest, TLS 1.3 in transit, key rotation policy | `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:22`; audit line 2449 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-135` | `TASK-SEC-004`: - **TASK-SEC-004**: Approve OAuth2/OIDC/SSO implementation (INFRA-002) — review provider integration security | `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:26`; audit line 2450 | UNSTATED | MISSED | [CP-04](#cp-04) | subject triage | TRACE/BUILD |
| `REQ-SEC-136` | `TASK-SEC-005`: - **TASK-SEC-005**: Define API security controls — rate limiting, input validation, output sanitization, CORS policy | `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:30`; audit line 2451 | UNSTATED | MISSED | [CP-08](#cp-08) | subject triage | TRACE/BUILD |
| `REQ-SEC-137` | `TASK-SEC-006`: - **TASK-SEC-006**: SOC 2 Type II readiness assessment — identify control gaps, remediation plan | `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:35`; audit line 2452 | UNSTATED | MISSED | [CP-35](#cp-35) | subject triage | TRACE/BUILD |
| `REQ-SEC-138` | `TASK-SEC-007`: - **TASK-SEC-007**: GDPR compliance review — data subject rights, consent management, data portability | `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:41`; audit line 2453 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-139` | `TASK-SEC-008`: - **TASK-SEC-008**: HIPAA compliance assessment — PHI handling controls, BAA templates | `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:46`; audit line 2454 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-140` | `TASK-SEC-009`: - **TASK-SEC-009**: Design Compliance-as-Code (COMPLY-001) rule templates for GDPR, SOX, HIPAA | `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:50`; audit line 2455 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-141` | `TASK-SEC-010`: - **TASK-SEC-010**: Establish continuous compliance monitoring (COMPLY-003) — automated evidence collection | `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:54`; audit line 2456 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-142` | `TASK-SEC-011`: - **TASK-SEC-011**: Establish vulnerability management program — scanning schedule, remediation SLAs | `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:59`; audit line 2457 | UNSTATED | MISSED | [CP-10](#cp-10) | subject triage | TRACE/BUILD |
| `REQ-SEC-143` | `TASK-SEC-012`: - **TASK-SEC-012**: Define incident response plan — detection, containment, eradication, recovery, lessons learned | `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:64`; audit line 2458 | UNSTATED | MISSED | [CP-18](#cp-18) | subject triage | TRACE/BUILD |
| `REQ-SEC-144` | `TASK-SEC-013`: - **TASK-SEC-013**: Conduct security review of token format deserialization (CORE-001) — prevent deserialization attacks | `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:68`; audit line 2459 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-145` | `TASK-SEC-014`: - **TASK-SEC-014**: Review PII Detection & Anonymization (COMPLY-002) implementation for correctness | `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:73`; audit line 2460 | UNSTATED | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-SEC-146` | `TASK-SEC-015`: - **TASK-SEC-015**: Define data classification policy — public, internal, confidential, restricted | `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:77`; audit line 2461 | UNSTATED | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-SEC-147` | `TASK-SEC-016`: - **TASK-SEC-016**: Review multi-tenancy isolation controls — ensure tenant data separation | `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:81`; audit line 2462 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-148` | `TASK-SEC-017`: - **TASK-SEC-017**: Define data retention and destruction policies per compliance framework | `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:85`; audit line 2463 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-149` | `TEST-NFR-SEC-001`: &#124; NFR-SEC-001 &#124; Security &#124; WP-SECURITY-OPS &#124; TEST-NFR-SEC-001 &#124; AC-NFR-SEC-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:82`; audit line 2562 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-150` | `TEST-NFR-SEC-002`: &#124; NFR-SEC-002 &#124; Security &#124; WP-SECURITY-OPS &#124; TEST-NFR-SEC-002 &#124; AC-NFR-SEC-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:83`; audit line 2563 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-151` | `TEST-NFR-SEC-003`: &#124; NFR-SEC-003 &#124; Security &#124; WP-SECURITY-OPS &#124; TEST-NFR-SEC-003 &#124; AC-NFR-SEC-003 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:84`; audit line 2564 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-152` | `TEST-NFR-SEC-004`: &#124; NFR-SEC-004 &#124; Security &#124; WP-SECURITY-OPS &#124; TEST-NFR-SEC-004 &#124; AC-NFR-SEC-004 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:85`; audit line 2565 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-153` | `TEST-NFR-SEC-005`: &#124; NFR-SEC-005 &#124; Security &#124; WP-SECURITY-OPS &#124; TEST-NFR-SEC-005 &#124; AC-NFR-SEC-005 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:86`; audit line 2566 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-154` | `TEST-NFR-SEC-006`: &#124; NFR-SEC-006 &#124; Security &#124; WP-SECURITY-OPS &#124; TEST-NFR-SEC-006 &#124; AC-NFR-SEC-006 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:87`; audit line 2567 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-155` | `TEST-NFR-SEC-007`: &#124; NFR-SEC-007 &#124; Security &#124; WP-SECURITY-OPS &#124; TEST-NFR-SEC-007 &#124; AC-NFR-SEC-007 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:88`; audit line 2568 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-156` | `WP-SECURITY-OPS-01`: ### WP-SECURITY-OPS-01 — No outbound enterprise-data egress | `EOIP-engg-doc-pkg/implementation/wp-security-ops.md:32`; audit line 2685 | UNSTATED | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-SEC-157` | `WP-SECURITY-OPS-02`: ### WP-SECURITY-OPS-02 — Secret isolation | `EOIP-engg-doc-pkg/implementation/wp-security-ops.md:41`; audit line 2686 | UNSTATED | MISSED | [CP-09](#cp-09) | subject triage | TRACE/BUILD |
| `REQ-SEC-158` | `WP-SECURITY-OPS-03`: ### WP-SECURITY-OPS-03 — Input/file safety | `EOIP-engg-doc-pkg/implementation/wp-security-ops.md:50`; audit line 2687 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-159` | `WP-SECURITY-OPS-04`: ### WP-SECURITY-OPS-04 — Prompt/tool injection defenses | `EOIP-engg-doc-pkg/implementation/wp-security-ops.md:59`; audit line 2688 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-160` | `WP-SECURITY-OPS-05`: ### WP-SECURITY-OPS-05 — Authentication without MVP RBAC | `EOIP-engg-doc-pkg/implementation/wp-security-ops.md:68`; audit line 2689 | UNSTATED | MISSED | [CP-04](#cp-04) | subject triage | TRACE/BUILD |
| `REQ-SEC-161` | `WP-SECURITY-OPS-06`: ### WP-SECURITY-OPS-06 — Container hardening | `EOIP-engg-doc-pkg/implementation/wp-security-ops.md:77`; audit line 2690 | UNSTATED | MISSED | [CP-31](#cp-31) | subject triage | TRACE/BUILD |
| `REQ-SEC-162` | `WP-SECURITY-OPS-07`: ### WP-SECURITY-OPS-07 — Audit events | `EOIP-engg-doc-pkg/implementation/wp-security-ops.md:86`; audit line 2691 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-163` | `WP-SECURITY-OPS-08`: ### WP-SECURITY-OPS-08 — Restart-safe processing | `EOIP-engg-doc-pkg/implementation/wp-security-ops.md:95`; audit line 2692 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-164` | `WP-SECURITY-OPS-09`: ### WP-SECURITY-OPS-09 — Backup and restore | `EOIP-engg-doc-pkg/implementation/wp-security-ops.md:104`; audit line 2693 | UNSTATED | MISSED | [CP-31](#cp-31) | subject triage | TRACE/BUILD |
| `REQ-SEC-165` | `WP-SECURITY-OPS-10`: ### WP-SECURITY-OPS-10 — Structured logging and health | `EOIP-engg-doc-pkg/implementation/wp-security-ops.md:113`; audit line 2694 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-166` | `WP-SECURITY-OPS-11`: ### WP-SECURITY-OPS-11 — Local metrics | `EOIP-engg-doc-pkg/implementation/wp-security-ops.md:122`; audit line 2695 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-167` | `WP-SECURITY-OPS-12`: ### WP-SECURITY-OPS-12 — Benchmark-defined objectives | `EOIP-engg-doc-pkg/implementation/wp-security-ops.md:131`; audit line 2696 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-SEC-168` | `WP-SECURITY-OPS-13`: ### WP-SECURITY-OPS-13 — Modular monolith boundary | `EOIP-engg-doc-pkg/implementation/wp-security-ops.md:140`; audit line 2697 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |
| `REQ-SEC-169` | `WP-SECURITY-OPS-14`: ### WP-SECURITY-OPS-14 — Data minimization and classification | `EOIP-engg-doc-pkg/implementation/wp-security-ops.md:149`; audit line 2698 | UNSTATED | MISSED | [CP-09](#cp-09) | area fallback | TRACE/BUILD |

### A.22 TEN: 23 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-TEN-001` | `AIDLC-008.3`: - [ ] `AIDLC-008.3` Per-tenant quotas enforced | `eoip-phase4-2-requirements.md:2129`; audit line 337 | UNSTATED | MISSED | [CP-06](#cp-06) | subject triage | TRACE/BUILD |
| `REQ-TEN-002` | `AIDLC-012`: - **Step 1. Independent foundations.** CORE-001 unblocks CORE-003, CORE-006 and TEST-003; CORE-002 unblocks CORE-005; CORE-004 stands alone. Alongside, if accepted: the evaluation skeleton, the sandbox, the tenant-isolat... | `eoip-phase4-2-requirements.md:175`; audit line 354 | UNSTATED | MISSED | [CP-06](#cp-06) | area fallback | TRACE/BUILD |
| `REQ-TEN-003` | `SDLC-005.2`: - [ ] `SDLC-005.2` Stateful Phase 4 engines are tenant-keyed | `eoip-phase4-2-requirements.md:1488`; audit line 1806 | UNSTATED | MISSED | [CP-06](#cp-06) | engine family | TRACE/BUILD |
| `REQ-TEN-004` | `SDLC-005.3`: - [ ] `SDLC-005.3` Concurrency test: two tenants cannot observe each other | `eoip-phase4-2-requirements.md:1489`; audit line 1807 | UNSTATED | MISSED | [CP-06](#cp-06) | engine family | TRACE/BUILD |
| `REQ-TEN-005` | `SDLC-027.1`: - [ ] `SDLC-027.1` Cost attribution per tenant and route | `eoip-phase4-2-requirements.md:1900`; audit line 1915 | UNSTATED | MISSED | [CP-32](#cp-32) | engine family | TRACE/BUILD |
| `REQ-TEN-006` | `SDLC-029.3`: - [ ] `SDLC-029.3` Per-tenant keys | `eoip-phase4-2-requirements.md:1939`; audit line 1927 | UNSTATED | MISSED | [CP-09](#cp-09) | engine family | TRACE/BUILD |
| `REQ-TEN-007` | `SR-ARC-011`: &#124; SR-ARC-011 &#124; **Architecture fitness tests** in CI: forbidden imports, layering rules, adapter-only vendor SDK usage, no hand-maintained inventories, no cross-tenant code paths without tenant context. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:172`; audit line 1985 | P0 | MISSED | [CP-06](#cp-06) | subject triage | TRACE/BUILD |
| `REQ-TEN-008` | `SR-COM-001`: &#124; SR-COM-001 &#124; **Licensing models** supported by the entitlement system: perpetual + annual support, annual subscription, size-tier/usage-based, per-tenant (OEM/managed), seat-based add-ons, revenue-share/royalty for O... | `EOIP-engg-doc-pkg/super-requirements.md:1000`; audit line 1993 | P0 | IMPLEMENTED-UNVERIFIED | [CP-33](#cp-33) | ID family | PROVE |
| `REQ-TEN-009` | `SR-CON-011`: &#124; SR-CON-011 &#124; Every plugin MUST ship a **Data-Flow Manifest** declaring data classes sent/received, destinations, regions, retention and whether data can leave the tenant boundary. Installation MUST display it and req... | `EOIP-engg-doc-pkg/super-requirements.md:125`; audit line 2015 | P0 | PARTIAL | [CP-16](#cp-16) | ID family | COMPLETE |
| `REQ-TEN-010` | `SR-CON-014`: &#124; SR-CON-014 &#124; A tenant MUST be able to switch a capability between local and cloud providers via migration tooling (e.g., local object store → cloud bucket) with verification and rollback. &#124; P2 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:128`; audit line 2018 | P2 | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-TEN-011` | `SR-DEP-007`: &#124; SR-DEP-007 &#124; **Offline licensing:** signed license files encoding edition, modules, size tier, tenants, seats, expiry; grace periods; **no license check may ever delete or lock customer data** (read-only degrade only... | `EOIP-engg-doc-pkg/super-requirements.md:928`; audit line 2025 | P0 | IMPLEMENTED-UNVERIFIED | [CP-31](#cp-31) | ID family | PROVE |
| `REQ-TEN-012` | `SR-TEN-001`: &#124; SR-TEN-001 &#124; **Tenant context is mandatory** in every API, query, job, event, cache key, log line, metric label, agent call and plugin invocation; code paths without tenant context fail closed. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:718`; audit line 2206 | P0 | IMPLEMENTED-UNVERIFIED | [CP-06](#cp-06) | ID family | PROVE |
| `REQ-TEN-013` | `SR-TEN-002`: &#124; SR-TEN-002 &#124; **Three isolation models**, selectable per tenant/edition: *Silo* (dedicated stack), *Bridge* (shared compute, dedicated data stores/namespaces), *Pool* (shared everything, logical isolation). &#124; P0 (Sil... | `EOIP-engg-doc-pkg/super-requirements.md:719`; audit line 2207 | P0 | IMPLEMENTED-UNVERIFIED | [CP-06](#cp-06) | ID family | PROVE |
| `REQ-TEN-014` | `SR-TEN-003`: &#124; SR-TEN-003 &#124; Isolation is enforced at **every layer:** graph (database/graph-space/namespace per tenant), vector (collection), search (index), relational (schema + row-level security), object (bucket/prefix), event t... | `EOIP-engg-doc-pkg/super-requirements.md:720`; audit line 2208 | P0 | PARTIAL | [CP-06](#cp-06) | ID family | COMPLETE |
| `REQ-TEN-015` | `SR-TEN-004`: &#124; SR-TEN-004 &#124; **Automated cross-tenant penetration suite** (every endpoint, job type and plugin hook attempts cross-tenant reads/writes/side-channels) MUST pass in CI and before each release. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:721`; audit line 2209 | P0 | PARTIAL | [CP-06](#cp-06) | ID family | COMPLETE |
| `REQ-TEN-016` | `SR-TEN-005`: &#124; SR-TEN-005 &#124; **Per-tenant keys** (envelope encryption; BYOK and hold-your-own-key options), **crypto-shredding** on tenant deletion. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:722`; audit line 2210 | P0 | PARTIAL | [CP-06](#cp-06) | ID family | COMPLETE |
| `REQ-TEN-017` | `SR-TEN-006`: &#124; SR-TEN-006 &#124; **Noisy-neighbor control:** quotas (graph size, ingestion rate, concurrent queries, LLM tokens, storage), fair scheduling, priority lanes, per-tenant rate limits and circuit breakers. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:723`; audit line 2211 | P0 | IMPLEMENTED-UNVERIFIED | [CP-06](#cp-06) | ID family | PROVE |
| `REQ-TEN-018` | `SR-TEN-007`: &#124; SR-TEN-007 &#124; **Tenant lifecycle:** provision (API + console + IaC), configure, suspend, resume, clone (staging), migrate (cluster/region), export, delete (verified, certificate of destruction). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:724`; audit line 2212 | P0 | IMPLEMENTED-UNVERIFIED | [CP-06](#cp-06) | ID family | PROVE |
| `REQ-TEN-019` | `SR-TEN-008`: &#124; SR-TEN-008 &#124; **Per-tenant everything:** ontology extensions, connectors, mappings, model allowlist, egress policy, retention, region, SSO, branding, SLA tier, feature entitlements. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:725`; audit line 2213 | P0 | PARTIAL | [CP-06](#cp-06) | ID family | COMPLETE |
| `REQ-TEN-020` | `SR-TEN-009`: &#124; SR-TEN-009 &#124; **Metering and entitlements:** local, tamper-evident usage meters (records ingested, graph size, queries, LLM tokens, storage, seats, connectors) with export for billing; entitlements enforce edition/mod... | `EOIP-engg-doc-pkg/super-requirements.md:726`; audit line 2214 | P0 | IMPLEMENTED-UNVERIFIED | [CP-06](#cp-06) | ID family | PROVE |
| `REQ-TEN-021` | `SR-TEN-010`: &#124; SR-TEN-010 &#124; **Cross-tenant sharing (opt-in):** controlled sharing of ontologies, mappings, templates and anonymized benchmarks; never raw data; always explicit and auditable. &#124; P2 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:727`; audit line 2215 | P2 | PARTIAL | [CP-06](#cp-06) | ID family | COMPLETE |
| `REQ-TEN-022` | `SR-WL-003`: &#124; SR-WL-003 &#124; **Terminology and persona white-labelling:** tenant renames concepts (SR-ONT-007) and names/styles the AI assistant (name, tone, avatar, greeting) without altering safety behavior. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:735`; audit line 2237 | P0 | PARTIAL | [CP-28](#cp-28) | ID family | COMPLETE |
| `REQ-TEN-023` | `SR-WL-008`: &#124; SR-WL-008 &#124; **Partner console:** create/branding/configure tenants, view fleet health and usage, apply partner policy floors, issue licenses, manage support entitlements. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:740`; audit line 2242 | P1 | MISSED | [CP-28](#cp-28) | ID family | TRACE/BUILD |

### A.23 TMP: 39 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-TMP-001` | `AIDLC-001.1`: - [ ] `AIDLC-001.1` Corpus snapshots with hashes | `eoip-phase4-2-requirements.md:2052`; audit line 300 | UNSTATED | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-TMP-002` | `AIDLC-004.4`: - [ ] `AIDLC-004.4` Results history and dashboard | `eoip-phase4-2-requirements.md:2168`; audit line 318 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-TMP-003` | `AIDLC-005.3`: - [ ] `AIDLC-005.3` Counterfactual diff report | `eoip-phase4-2-requirements.md:2185`; audit line 322 | UNSTATED | MISSED | [CP-25](#cp-25) | subject triage | TRACE/BUILD |
| `REQ-TMP-004` | `AIDLC-007`: - [x] `AI-005.A2` Artifacts follow encryption and retention policy (SDLC-028, SDLC-029); prompt versions link to the prompt registry (AIDLC-007). *(added by review)* | `eoip-phase4-2-requirements.md:747`; audit line 329 | UNSTATED | MISSED | [CP-18](#cp-18) | area fallback | TRACE/BUILD |
| `REQ-TMP-005` | `AIDLC-007.1`: - [ ] `AIDLC-007.1` Registry with versions and promotion | `eoip-phase4-2-requirements.md:2109`; audit line 330 | UNSTATED | MISSED | [CP-18](#cp-18) | area fallback | TRACE/BUILD |
| `REQ-TMP-006` | `CORE-004.4`: - [x] `CORE-004.4` Layer diff for change detection | `eoip-phase4-2-requirements.md:330`; audit line 446 | UNSTATED | MISSED | [CP-13](#cp-13) | engine family | TRACE/BUILD |
| `REQ-TMP-007` | `FR-TEMP-001`: Bitemporal-ready fields | `EOIP-engg-doc-pkg/03-functional-requirements.md:315`; audit line 596 | P0 | PARTIAL | [CP-18](#cp-18) | ID family | COMPLETE |
| `REQ-TMP-008` | `G2-ARCH-007`: G2-ARCH-007 — No destructive history overwrite | `EOIP-engg-doc-pkg/gaps2-requirements.md:84`; audit line 646 | P0 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | area fallback | PROVE |
| `REQ-TMP-009` | `G2-P7`: &#124; G2-P7 &#124; Temporal/architecture/process intelligence &#124; Time Machine + conformance + process mining &#124; | `EOIP-engg-doc-pkg/gaps2-implementation.md:42`; audit line 805 | UNSTATED | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | subject triage | PROVE |
| `REQ-TMP-010` | `G2-SYNC-002`: G2-SYNC-002 — Baseline snapshot | `EOIP-engg-doc-pkg/gaps2-requirements.md:645`; audit line 936 | P2 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-TMP-011` | `GAP-ARCH-006`: GAP-ARCH-006: Provide trend and technical-debt history | `EOIP-engg-doc-pkg/gaps-requirements.md:539`; audit line 1239 | P0 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-TMP-012` | `GAP-GITOPS-007`: GAP-GITOPS-007: Allow rollback to previous semantic version | `EOIP-engg-doc-pkg/gaps-requirements.md:430`; audit line 1330 | P0 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | ID family | PROVE |
| `REQ-TMP-013` | `GAP-KRAG-005`: GAP-KRAG-005: Temporal filtering | `EOIP-engg-doc-pkg/gaps-requirements.md:680`; audit line 1384 | P0 | IMPLEMENTED-UNVERIFIED | [CP-21](#cp-21) | ID family | PROVE |
| `REQ-TMP-014` | `GAP-LAYER-002`: GAP-LAYER-002: Views must be declarative, versioned and reproducible | `EOIP-engg-doc-pkg/gaps-requirements.md:252`; audit line 1391 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | area fallback | PROVE |
| `REQ-TMP-015` | `GAP-MKT-007`: GAP-MKT-007: Dependency/version management | `EOIP-engg-doc-pkg/gaps-requirements.md:921`; audit line 1412 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-TMP-016` | `GAP-RULE-001`: GAP-RULE-001: Build a deterministic rules engine supporting versioned inference policies | `EOIP-engg-doc-pkg/gaps-requirements.md:170`; audit line 1459 | P2 | IMPLEMENTED-UNVERIFIED | [CP-19](#cp-19) | subject triage | PROVE |
| `REQ-TMP-017` | `GAP-SDT-007`: GAP-SDT-007: Maintain temporal state so historical releases can be reconstructed | `EOIP-engg-doc-pkg/gaps-requirements.md:387`; audit line 1468 | P0 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | subject triage | PROVE |
| `REQ-TMP-018` | `GAP-STUDIO-006`: GAP-STUDIO-006: Diff/merge | `EOIP-engg-doc-pkg/gaps-requirements.md:608`; audit line 1490 | P0 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | area fallback | PROVE |
| `REQ-TMP-019` | `GAP-TEMP-005`: GAP-TEMP-005: Retain semantic changes without overwriting history | `EOIP-engg-doc-pkg/gaps-requirements.md:572`; audit line 1502 | P1 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-TMP-020` | `GAP-TRUTH-009`: GAP-TRUTH-009: Retain rejected/obsolete claims for history | `EOIP-engg-doc-pkg/gaps-requirements.md:478`; audit line 1519 | P1 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | area fallback | PROVE |
| `REQ-TMP-021` | `INFRA-006`: API Versioning & Client SDK Generation | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:639`; audit line 1598 | P2 | IMPLEMENTED-UNVERIFIED | [CP-07](#cp-07) | engine family | PROVE |
| `REQ-TMP-022` | `INFRA-006.1`: - [x] `INFRA-006.1` API version coexistence (v1 + v2) | `eoip-phase4-2-requirements.md:925`; audit line 1599 | UNSTATED | MISSED | [CP-07](#cp-07) | engine family | TRACE/BUILD |
| `REQ-TMP-023` | `KGR-G-006`: 2D Bitemporal CRDT Branch Engine & Merkle Audit Trail | `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:38`; audit line 1615 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-TMP-024` | `SDLC-012`: - [x] `TEST-002.A2` Runs on generated realistic data (SDLC-012); results and baselines are stored as versioned artifacts. *(added by review)* | `eoip-phase4-2-requirements.md:1258`; audit line 1839 | UNSTATED | MISSED | [CP-02](#cp-02) | engine family | TRACE/BUILD |
| `REQ-TMP-025` | `SDLC-017`: - [x] `INFRA-006.A2` Breaking-change detection (OpenAPI diff) runs in CI; SDK contract tests (SDLC-017). *(added by review)* | `eoip-phase4-2-requirements.md:931`; audit line 1864 | UNSTATED | MISSED | [CP-29](#cp-29) | engine family | TRACE/BUILD |
| `REQ-TMP-026` | `SDLC-018.2`: - [ ] `SDLC-018.2` Visual snapshots for shared components | `eoip-phase4-2-requirements.md:1733`; audit line 1871 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-TMP-027` | `SDLC-020.2`: - [ ] `SDLC-020.2` Version matrix in CI (scheduled) | `eoip-phase4-2-requirements.md:1767`; audit line 1881 | UNSTATED | MISSED | [CP-31](#cp-31) | engine family | TRACE/BUILD |
| `REQ-TMP-028` | `SDLC-022.1`: - [ ] `SDLC-022.1` Automated changelog and version bump | `eoip-phase4-2-requirements.md:1805`; audit line 1890 | UNSTATED | MISSED | [CP-33](#cp-33) | engine family | TRACE/BUILD |
| `REQ-TMP-029` | `SR-ARC-008`: &#124; SR-ARC-008 &#124; **Hybrid logical clocks / bitemporal fields** on all mutations (valid time, transaction time) so federated and replayed data order deterministically. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:169`; audit line 1982 | P1 | MISSED | [CP-18](#cp-18) | subject triage | TRACE/BUILD |
| `REQ-TMP-030` | `SR-CFG-004`: &#124; SR-CFG-004 &#124; **Config as code:** export/import (YAML/JSON), GitOps promotion dev → stage → prod, diff, dry-run, rollback, change approval workflow. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:750`; audit line 1990 | P0 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | ID family | PROVE |
| `REQ-TMP-031` | `SR-COM-009`: &#124; SR-COM-009 &#124; **Lifecycle policy:** versioning, LTS, end-of-support, security-patch commitments published. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:1008`; audit line 2001 | P0 | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-TMP-032` | `SR-CON-004`: &#124; SR-CON-004 &#124; **Everything configurable, safely:** every behavior in this document that says "configurable" MUST be a typed, versioned, validated, auditable setting with a safe default (§12.3). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:101`; audit line 2008 | P0 | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-TMP-033` | `SR-EXT-002`: &#124; SR-EXT-002 &#124; API standards: semantic versioning, ≥ 12-month deprecation window, idempotency keys, cursor pagination, async job pattern, consistent error model, rate-limit headers, generated reference and SDKs. &#124; P0 ... | `EOIP-engg-doc-pkg/super-requirements.md:777`; audit line 2029 | P0 | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-TMP-034` | `SR-EXT-012`: &#124; SR-EXT-012 &#124; **Signed, versioned packages** with manifest, compatibility range, Data-Flow Manifest, SBOM and test fixtures; trust levels (first-party / certified partner / community / private). &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:788`; audit line 2035 | P0 | MISSED | [CP-29](#cp-29) | ID family | TRACE/BUILD |
| `REQ-TMP-035` | `SR-GDB-015`: &#124; SR-GDB-015 &#124; **Durable workflow engine** built in (retry, timers, human-approval steps, sagas); optional adapters for Temporal/Airflow/Dagster/Prefect-class orchestrators. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:220`; audit line 2053 | P1 | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-TMP-036` | `TASK-ARCH-007`: - **TASK-ARCH-007**: Design API versioning strategy (v1 stable, v2 experimental) with deprecation policy | `EOIP-engg-doc-pkg/roles/Architect_tasks.md:38`; audit line 2263 | UNSTATED | MISSED | [CP-07](#cp-07) | subject triage | TRACE/BUILD |
| `REQ-TMP-037` | `TASK-DM-007`: - **TASK-DM-007**: Manage changelog and release notes for each version | `EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:46`; audit line 2327 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |
| `REQ-TMP-038` | `TASK-LIC-004`: - **TASK-LIC-004**: Design trial/freemium conversion funnel — Community → Professional upgrade triggers | `EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:27`; audit line 2385 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-TMP-039` | `TASK-MKE-012`: - **TASK-MKE-012**: Set up marketing analytics — website traffic, conversion rates, content performance | `EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:58`; audit line 2406 | UNSTATED | MISSED | [CP-01](#cp-01) | ID family | TRACE/BUILD |

### A.24 UI: 104 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-UI-001` | `AC-41`: &#124; AC-41 &#124; Alternative table view provides WCAG-accessible data browsing &#124; No competitor has this &#124; | `EOIP-engg-doc-pkg/KGR-requirements.md:1072`; audit line 139 | UNSTATED | MISSED | [CP-24](#cp-24) | subject triage | TRACE/BUILD |
| `REQ-UI-002` | `AC-FR-UI-001`: &#124; FR-UI-001 &#124; Web UI &#124; WP-EXPERIENCE &#124; TEST-FR-UI-001 &#124; AC-FR-UI-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:76`; audit line 207 | UNSTATED | MISSED | [CP-24](#cp-24) | subject triage | TRACE/BUILD |
| `REQ-UI-003` | `AC-FR-UI-002`: &#124; FR-UI-002 &#124; Web UI &#124; WP-EXPERIENCE &#124; TEST-FR-UI-002 &#124; AC-FR-UI-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:77`; audit line 208 | UNSTATED | MISSED | [CP-24](#cp-24) | subject triage | TRACE/BUILD |
| `REQ-UI-004` | `AIDLC-003.4`: - [ ] `AIDLC-003.4` Dashboard | `eoip-phase4-2-requirements.md:2092`; audit line 313 | UNSTATED | MISSED | [CP-22](#cp-22) | subject triage | TRACE/BUILD |
| `REQ-UI-005` | `CG-GAP-007`: Update web UX docs to the real stack | `EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:68`; audit line 393 | P1 | PARTIAL | [CP-24](#cp-24) | subject triage | COMPLETE |
| `REQ-UI-006` | `COMPLY-003`: Continuous Compliance Monitoring Dashboard | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:872`; audit line 408 | P2 | IMPLEMENTED-UNVERIFIED | [CP-33](#cp-33) | ID family | PROVE |
| `REQ-UI-007` | `FR-KGR-024`: ### FR-KGR-024: Alternative Table/List View (Accessibility) | `EOIP-engg-doc-pkg/KGR-requirements.md:575`; audit line 566 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-UI-008` | `FR-KGR-030`: ### FR-KGR-030: AI Explorer Panel | `EOIP-engg-doc-pkg/KGR-requirements.md:685`; audit line 572 | UNSTATED | MISSED | [CP-23](#cp-23) | ID family | TRACE/BUILD |
| `REQ-UI-009` | `FR-UI-001`: User web application | `EOIP-engg-doc-pkg/03-functional-requirements.md:625`; audit line 597 | P0 | IMPLEMENTED-UNVERIFIED | [CP-24](#cp-24) | subject triage | PROVE |
| `REQ-UI-010` | `FR-UI-002`: Graph explorer | `EOIP-engg-doc-pkg/03-functional-requirements.md:635`; audit line 598 | P0 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | subject triage | PROVE |
| `REQ-UI-011` | `G2-P10`: &#124; G2-P10 &#124; Diamond-standard UX & production hardening &#124; lenses, playback, scale, operational maturity &#124; | `EOIP-engg-doc-pkg/gaps2-implementation.md:45`; audit line 798 | UNSTATED | BLOCKED | [CP-23](#cp-23) | explicit | UNBLOCK |
| `REQ-UI-012` | `G2-SRC-WEB-001`: G2-SRC-WEB-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:420`; audit line 930 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-UI-013` | `G2-SRC-WEB-002`: G2-SRC-WEB-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:626`; audit line 931 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-UI-014` | `G2-SRC-WEB-003`: G2-SRC-WEB-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:629`; audit line 932 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-UI-015` | `G2-SRC-WEB-004`: G2-SRC-WEB-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:632`; audit line 933 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-UI-016` | `G2-SRC-WEB-005`: G2-SRC-WEB-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:635`; audit line 934 | P2 | IMPLEMENTED-UNVERIFIED | [CP-16](#cp-16) | ID family | PROVE |
| `REQ-UI-017` | `G2-UX-LENS-001`: G2-UX-LENS-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1087`; audit line 1181 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-UI-018` | `G2-UX-LENS-002`: G2-UX-LENS-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1464`; audit line 1182 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-UI-019` | `G2-UX-LENS-003`: G2-UX-LENS-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1467`; audit line 1183 | P2 | IMPLEMENTED-UNVERIFIED | [CP-23](#cp-23) | ID family | PROVE |
| `REQ-UI-020` | `G2-UX-PLAY-001`: G2-UX-PLAY-001 | `EOIP-engg-doc-pkg/gaps2-implementation.md:1089`; audit line 1184 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-UI-021` | `G2-UX-PLAY-002`: G2-UX-PLAY-002 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1529`; audit line 1185 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-UI-022` | `G2-UX-PLAY-003`: G2-UX-PLAY-003 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1538`; audit line 1186 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-UI-023` | `G2-UX-PLAY-004`: G2-UX-PLAY-004 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1541`; audit line 1187 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-UI-024` | `G2-UX-PLAY-005`: G2-UX-PLAY-005 | `EOIP-engg-doc-pkg/gaps2-requirements.md:1544`; audit line 1188 | P2 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | ID family | PROVE |
| `REQ-UI-025` | `GAP-ARCH-003`: GAP-ARCH-003: Show violations in Web UI and VS Code | `EOIP-engg-doc-pkg/gaps-requirements.md:536`; audit line 1236 | P0 | IMPLEMENTED-UNVERIFIED | [CP-37](#cp-37) | ID family | PROVE |
| `REQ-UI-026` | `GAP-MKT-006`: GAP-MKT-006: Package dashboards | `EOIP-engg-doc-pkg/gaps-requirements.md:920`; audit line 1411 | P2 | IMPLEMENTED-UNVERIFIED | [CP-29](#cp-29) | ID family | PROVE |
| `REQ-UI-027` | `GAP-STUDIO-001`: GAP-STUDIO-001: Visual class/property/relationship editor | `EOIP-engg-doc-pkg/gaps-implementation.md:296`; audit line 1485 | P0 | IMPLEMENTED-UNVERIFIED | [CP-24](#cp-24) | area fallback | PROVE |
| `REQ-UI-028` | `GAP-STUDIO-003`: GAP-STUDIO-003: SHACL-style validation rules | `EOIP-engg-doc-pkg/gaps-requirements.md:605`; audit line 1487 | P0 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-UI-029` | `GAP-STUDIO-005`: GAP-STUDIO-005: SKOS taxonomy support | `EOIP-engg-doc-pkg/gaps-requirements.md:607`; audit line 1489 | P0 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-UI-030` | `GAP-STUDIO-007`: GAP-STUDIO-007: Comments and review workflow | `EOIP-engg-doc-pkg/gaps-requirements.md:609`; audit line 1491 | P0 | IMPLEMENTED-UNVERIFIED | [CP-22](#cp-22) | subject triage | PROVE |
| `REQ-UI-031` | `GAP-UX-001`: GAP-UX-001: Hide RDF/SHACL complexity from non-semantic users while preserving standards internally | `EOIP-engg-doc-pkg/gaps-requirements.md:200`; audit line 1521 | P2 | IMPLEMENTED-UNVERIFIED | [CP-12](#cp-12) | subject triage | PROVE |
| `REQ-UI-032` | `REL-08`: Browser-level web E2E after the Vite build | `KGF-MASTER-BACKLOG.md:1213`; audit line 1770 | P0 | IMPLEMENTED-UNVERIFIED | [CP-36](#cp-36) | ID family | PROVE |
| `REQ-UI-033` | `SDLC-016.4`: - [ ] `SDLC-016.4` Dashboard shows progress from the registry | `eoip-phase4-2-requirements.md:1697`; audit line 1863 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-UI-034` | `SDLC-027.3`: - [ ] `SDLC-027.3` Benefit dashboard for CORE-001/003/006 claims | `eoip-phase4-2-requirements.md:1902`; audit line 1917 | UNSTATED | MISSED | [CP-32](#cp-32) | engine family | TRACE/BUILD |
| `REQ-UI-035` | `SDLC-032`: &#124; SDLC: docs, DX, go-to-market &#124; UI-001 Storybook, KGF S-04 &#124; No docs-as-code CI, no bootstrap experience, no procurement pack &#124; SDLC-032..034 &#124; | `eoip-phase4-2-requirements.md:1375`; audit line 1939 | UNSTATED | MISSED | [CP-35](#cp-35) | engine family | TRACE/BUILD |
| `REQ-UI-036` | `SDLC-033.4`: - [ ] `SDLC-033.4` First-run guide in the UI | `eoip-phase4-2-requirements.md:2015`; audit line 1948 | UNSTATED | MISSED | [CP-29](#cp-29) | engine family | TRACE/BUILD |
| `REQ-UI-037` | `SR-UX-001`: &#124; SR-UX-001 &#124; **No mock UI:** every screen reads live APIs; hardcoded demo data is allowed only in an explicit, labeled Demo Mode. UI acceptance tests assert real backend calls. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:803`; audit line 2216 | P0 | MISSED | [CP-24](#cp-24) | subject triage | TRACE/BUILD |
| `REQ-UI-038` | `SR-UX-002`: &#124; SR-UX-002 &#124; **Graph visualization at scale:** WebGL rendering, level-of-detail and semantic zoom, bounded subgraph fetch, clustering/community collapse, multiple layouts (force, hierarchical, radial, geo), 2D/3D, min... | `EOIP-engg-doc-pkg/super-requirements.md:804`; audit line 2217 | P0 | MISSED | [CP-23](#cp-23) | subject triage | TRACE/BUILD |
| `REQ-UI-039` | `SR-UX-003`: &#124; SR-UX-003 &#124; **Alternate views:** table, matrix (dependency/DSM), tree/hierarchy, Sankey/flow, timeline/scrubber (temporal), geo-map, diff view between revisions. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:805`; audit line 2218 | P1 | MISSED | [CP-18](#cp-18) | subject triage | TRACE/BUILD |
| `REQ-UI-040` | `SR-UX-004`: &#124; SR-UX-004 &#124; **Honest visual encoding:** edge style encodes class and confidence (asserted/derived/inferred/curated); freshness shading; provenance drawer ("show evidence") one click from any element or answer sentenc... | `EOIP-engg-doc-pkg/super-requirements.md:806`; audit line 2219 | P0 | MISSED | [CP-17](#cp-17) | subject triage | TRACE/BUILD |
| `REQ-UI-041` | `SR-UX-005`: &#124; SR-UX-005 &#124; **NL console:** suggestion cards (SR-NLQ-002), query preview (EOQL + dialect), evidence panel, mode badge (deterministic/narrated/exploratory/report), follow-up chips, investigation canvas that pins entit... | `EOIP-engg-doc-pkg/super-requirements.md:807`; audit line 2220 | P0 | MISSED | [CP-25](#cp-25) | subject triage | TRACE/BUILD |
| `REQ-UI-042` | `SR-UX-006`: &#124; SR-UX-006 &#124; **Persona-based homes** and role-aware navigation (executive, architect, engineer, steward, auditor, admin), fully configurable. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:808`; audit line 2221 | P1 | MISSED | [CP-24](#cp-24) | subject triage | TRACE/BUILD |
| `REQ-UI-043` | `SR-UX-007`: &#124; SR-UX-007 &#124; **Collaboration:** comments, annotations, @mentions, shared investigations/views, review of proposed ontology/mapping changes, activity feed. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:809`; audit line 2222 | P1 | MISSED | [CP-26](#cp-26) | subject triage | TRACE/BUILD |
| `REQ-UI-044` | `SR-UX-008`: &#124; SR-UX-008 &#124; **Accessibility:** WCAG 2.2 AA, keyboard-first, screen-reader semantics for graph (alt text paths, tabular fallback), reduced-motion, color-blind-safe palettes. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:810`; audit line 2223 | P0 | MISSED | [CP-24](#cp-24) | subject triage | TRACE/BUILD |
| `REQ-UI-045` | `SR-UX-009`: &#124; SR-UX-009 &#124; **Responsive and mobile read:** tablet/phone views for answers, alerts and approvals. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:811`; audit line 2224 | P1 | MISSED | [CP-24](#cp-24) | subject triage | TRACE/BUILD |
| `REQ-UI-046` | `SR-UX-010`: &#124; SR-UX-010 &#124; **Onboarding:** guided setup wizard (connect → profile → map → validate → ask), sample-data sandbox, in-product help, "what can I ask?" explorer driven by the meta-graph. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:812`; audit line 2225 | P0 | MISSED | [CP-24](#cp-24) | subject triage | TRACE/BUILD |
| `REQ-UI-047` | `SR-UX-011`: &#124; SR-UX-011 &#124; **Destructive-action safety:** confirmations with impact preview, undo where possible, dual control for configured classes. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:813`; audit line 2226 | P0 | MISSED | [CP-18](#cp-18) | subject triage | TRACE/BUILD |
| `REQ-UI-048` | `SR-UX-012`: &#124; SR-UX-012 &#124; **Performance budget:** initial load ≤ 3 s on reference hardware over LAN; interactions ≤ 200 ms for local operations. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:814`; audit line 2227 | P1 | MISSED | [CP-32](#cp-32) | subject triage | TRACE/BUILD |
| `REQ-UI-049` | `SR-WL-006`: &#124; SR-WL-006 &#124; **Localization packs:** UI strings, date/number formats, RTL, glossary translation; partner-supplied language packs. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:738`; audit line 2240 | P0 | PARTIAL | [CP-28](#cp-28) | ID family | COMPLETE |
| `REQ-UI-050` | `TASK-QA-021`: - **TASK-QA-021**: Write Playwright e2e tests for new dashboard lenses (UI-007) | `EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:56`; audit line 2433 | UNSTATED | MISSED | [CP-02](#cp-02) | ID family | TRACE/BUILD |
| `REQ-UI-051` | `TEST-FR-UI-001`: &#124; FR-UI-001 &#124; Web UI &#124; WP-EXPERIENCE &#124; TEST-FR-UI-001 &#124; AC-FR-UI-001 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:76`; audit line 2548 | UNSTATED | MISSED | [CP-24](#cp-24) | subject triage | TRACE/BUILD |
| `REQ-UI-052` | `TEST-FR-UI-002`: &#124; FR-UI-002 &#124; Web UI &#124; WP-EXPERIENCE &#124; TEST-FR-UI-002 &#124; AC-FR-UI-002 &#124; | `EOIP-engg-doc-pkg/72-requirement-traceability.md:77`; audit line 2549 | UNSTATED | MISSED | [CP-24](#cp-24) | subject triage | TRACE/BUILD |
| `REQ-UI-053` | `UI-001`: Component Library & Design System | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:682`; audit line 2569 | P1 | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-054` | `UI-001.1`: - [x] `UI-001.1` 10+ shared UI components | `eoip-phase4-2-requirements.md:976`; audit line 2570 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-055` | `UI-001.2`: - [x] `UI-001.2` Storybook setup with stories for each component | `eoip-phase4-2-requirements.md:977`; audit line 2571 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-056` | `UI-001.3`: - [x] `UI-001.3` Design tokens file | `eoip-phase4-2-requirements.md:978`; audit line 2572 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-057` | `UI-001.4`: - [x] `UI-001.4` Theme-aware components | `eoip-phase4-2-requirements.md:979`; audit line 2573 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-058` | `UI-001.5`: - [x] `UI-001.5` Component documentation | `eoip-phase4-2-requirements.md:980`; audit line 2574 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-059` | `UI-002`: Internationalization (i18n/l10n) | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:700`; audit line 2575 | P2 | MISSED | [CP-28](#cp-28) | engine family | TRACE/BUILD |
| `REQ-UI-060` | `UI-002.1`: - [x] `UI-002.1` i18n framework integrated | `eoip-phase4-2-requirements.md:999`; audit line 2576 | UNSTATED | MISSED | [CP-28](#cp-28) | engine family | TRACE/BUILD |
| `REQ-UI-061` | `UI-002.2`: - [x] `UI-002.2` English locale file with all strings | `eoip-phase4-2-requirements.md:1000`; audit line 2577 | UNSTATED | MISSED | [CP-28](#cp-28) | engine family | TRACE/BUILD |
| `REQ-UI-062` | `UI-002.3`: - [x] `UI-002.3` Language selector | `eoip-phase4-2-requirements.md:1001`; audit line 2578 | UNSTATED | MISSED | [CP-28](#cp-28) | engine family | TRACE/BUILD |
| `REQ-UI-063` | `UI-002.4`: - [x] `UI-002.4` Date/number locale formatting | `eoip-phase4-2-requirements.md:1002`; audit line 2579 | UNSTATED | MISSED | [CP-28](#cp-28) | engine family | TRACE/BUILD |
| `REQ-UI-064` | `UI-002.5`: - [x] `UI-002.5` At least 2 locale files | `eoip-phase4-2-requirements.md:1003`; audit line 2580 | UNSTATED | MISSED | [CP-28](#cp-28) | engine family | TRACE/BUILD |
| `REQ-UI-065` | `UI-003`: Advanced Data Grid | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:718`; audit line 2581 | P2 | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-066` | `UI-003.1`: - [x] `UI-003.1` Grid component with sort/filter/paginate | `eoip-phase4-2-requirements.md:1020`; audit line 2582 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-067` | `UI-003.2`: - [x] `UI-003.2` Virtual scrolling for 10K+ rows | `eoip-phase4-2-requirements.md:1021`; audit line 2583 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-068` | `UI-003.3`: - [x] `UI-003.3` Column resize and reorder | `eoip-phase4-2-requirements.md:1022`; audit line 2584 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-069` | `UI-003.4`: - [x] `UI-003.4` Applied to 3+ existing tables | `eoip-phase4-2-requirements.md:1023`; audit line 2585 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-070` | `UI-004`: Charting Library Integration | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:734`; audit line 2586 | P2 | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-071` | `UI-004.1`: - [x] `UI-004.1` Charting library integrated | `eoip-phase4-2-requirements.md:1040`; audit line 2587 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-072` | `UI-004.2`: - [x] `UI-004.2` 6+ chart types available | `eoip-phase4-2-requirements.md:1041`; audit line 2588 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-073` | `UI-004.3`: - [x] `UI-004.3` Theme-aware | `eoip-phase4-2-requirements.md:1042`; audit line 2589 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-074` | `UI-004.4`: - [x] `UI-004.4` Applied to existing metric displays | `eoip-phase4-2-requirements.md:1043`; audit line 2590 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-075` | `UI-005`: PDF/CSV Export | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:750`; audit line 2591 | P2 | STUBBED | [CP-25](#cp-25) | explicit | REPLACE |
| `REQ-UI-076` | `UI-005.1`: - [x] `UI-005.1` PDF export for graph reports | `eoip-phase4-2-requirements.md:1059`; audit line 2592 | UNSTATED | STUBBED | [CP-25](#cp-25) | explicit | REPLACE |
| `REQ-UI-077` | `UI-005.2`: - [x] `UI-005.2` CSV export for tabular data | `eoip-phase4-2-requirements.md:1060`; audit line 2593 | UNSTATED | MISSED | [CP-25](#cp-25) | engine family | TRACE/BUILD |
| `REQ-UI-078` | `UI-005.3`: - [x] `UI-005.3` Export buttons on data views | `eoip-phase4-2-requirements.md:1061`; audit line 2594 | UNSTATED | MISSED | [CP-25](#cp-25) | engine family | TRACE/BUILD |
| `REQ-UI-079` | `UI-005.4`: - [x] `UI-005.4` Report templates | `eoip-phase4-2-requirements.md:1062`; audit line 2595 | UNSTATED | MISSED | [CP-25](#cp-25) | engine family | TRACE/BUILD |
| `REQ-UI-080` | `UI-006`: Visual Workflow Builder | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:766`; audit line 2596 | P3 | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-UI-081` | `UI-006.1`: - [x] `UI-006.1` Drag-and-drop canvas | `eoip-phase4-2-requirements.md:1079`; audit line 2597 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-UI-082` | `UI-006.2`: - [x] `UI-006.2` Node palette with 10+ node types | `eoip-phase4-2-requirements.md:1080`; audit line 2598 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-UI-083` | `UI-006.3`: - [x] `UI-006.3` Connection validation | `eoip-phase4-2-requirements.md:1081`; audit line 2599 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-UI-084` | `UI-006.4`: - [x] `UI-006.4` Export to pipeline config | `eoip-phase4-2-requirements.md:1082`; audit line 2600 | UNSTATED | MISSED | [CP-22](#cp-22) | engine family | TRACE/BUILD |
| `REQ-UI-085` | `UI-007`: Missing Dashboard Lenses | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:782`; audit line 2601 | P2 | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-086` | `UI-007.1`: - [x] `UI-007.1` All 6 lenses implemented | `eoip-phase4-2-requirements.md:1101`; audit line 2602 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-087` | `UI-007.2`: - [x] `UI-007.2` Navigation integration | `eoip-phase4-2-requirements.md:1102`; audit line 2603 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-088` | `UI-007.3`: - [x] `UI-007.3` Data connected to backend APIs | `eoip-phase4-2-requirements.md:1103`; audit line 2604 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-089` | `UI-007.4`: - [x] `UI-007.4` Theme-aware | `eoip-phase4-2-requirements.md:1104`; audit line 2605 | UNSTATED | MISSED | [CP-24](#cp-24) | engine family | TRACE/BUILD |
| `REQ-UI-090` | `UI-008`: Search Analytics & Relevance Dashboard | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:800`; audit line 2606 | P2 | IMPLEMENTED-UNVERIFIED | [CP-20](#cp-20) | engine family | PROVE |
| `REQ-UI-091` | `UI-008.1`: - [x] `UI-008.1` Search event logging | `eoip-phase4-2-requirements.md:1121`; audit line 2607 | UNSTATED | MISSED | [CP-20](#cp-20) | engine family | TRACE/BUILD |
| `REQ-UI-092` | `UI-008.2`: - [x] `UI-008.2` Analytics dashboard | `eoip-phase4-2-requirements.md:1122`; audit line 2608 | UNSTATED | MISSED | [CP-20](#cp-20) | engine family | TRACE/BUILD |
| `REQ-UI-093` | `UI-008.3`: - [x] `UI-008.3` Relevance tuning controls | `eoip-phase4-2-requirements.md:1123`; audit line 2609 | UNSTATED | MISSED | [CP-20](#cp-20) | engine family | TRACE/BUILD |
| `REQ-UI-094` | `UI-008.4`: - [x] `UI-008.4` A/B testing for ranking | `eoip-phase4-2-requirements.md:1124`; audit line 2610 | UNSTATED | MISSED | [CP-20](#cp-20) | engine family | TRACE/BUILD |
| `REQ-UI-095` | `UI-009`: Real-time Collaboration | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:816`; audit line 2611 | P3 | MISSED | [CP-26](#cp-26) | engine family | TRACE/BUILD |
| `REQ-UI-096` | `UI-009.1`: - [x] `UI-009.1` Real-time state sync between users | `eoip-phase4-2-requirements.md:1141`; audit line 2612 | UNSTATED | MISSED | [CP-26](#cp-26) | engine family | TRACE/BUILD |
| `REQ-UI-097` | `UI-009.2`: - [x] `UI-009.2` Presence indicators | `eoip-phase4-2-requirements.md:1142`; audit line 2613 | UNSTATED | MISSED | [CP-26](#cp-26) | engine family | TRACE/BUILD |
| `REQ-UI-098` | `UI-009.3`: - [x] `UI-009.3` Shared graph exploration | `eoip-phase4-2-requirements.md:1143`; audit line 2614 | UNSTATED | MISSED | [CP-26](#cp-26) | engine family | TRACE/BUILD |
| `REQ-UI-099` | `UI-009.4`: - [x] `UI-009.4` Annotation sync | `eoip-phase4-2-requirements.md:1144`; audit line 2615 | UNSTATED | MISSED | [CP-26](#cp-26) | engine family | TRACE/BUILD |
| `REQ-UI-100` | `UI-01`: Dashboard: causal blast radius | `KGF-MASTER-BACKLOG.md:917`; audit line 2616 | P0 | IMPLEMENTED-UNVERIFIED | [CP-18](#cp-18) | subject triage | PROVE |
| `REQ-UI-101` | `UI-02`: Dashboard: multi-paradigm querying | `KGF-MASTER-BACKLOG.md:919`; audit line 2617 | P0 | IMPLEMENTED-UNVERIFIED | [CP-14](#cp-14) | subject triage | PROVE |
| `REQ-UI-102` | `UI-03`: Dashboard: domain pack activation | `KGF-MASTER-BACKLOG.md:921`; audit line 2618 | P0 | IMPLEMENTED-UNVERIFIED | [CP-24](#cp-24) | subject triage | PROVE |
| `REQ-UI-103` | `UI-04`: Dashboard: XAI factor verification | `KGF-MASTER-BACKLOG.md:923`; audit line 2619 | P0 | IMPLEMENTED-UNVERIFIED | [CP-24](#cp-24) | subject triage | PROVE |
| `REQ-UI-104` | `WP-EXPERIENCE-01`: ### WP-EXPERIENCE-01 — User web application | `EOIP-engg-doc-pkg/implementation/wp-experience.md:24`; audit line 2640 | UNSTATED | MISSED | [CP-24](#cp-24) | area fallback | TRACE/BUILD |

### A.25 VEC: 17 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-VEC-001` | `AI-006`: Embedding Management & Versioning | `EOIP-engg-doc-pkg/eoip-phase4-requirements.md:495`; audit line 287 | P2 | IMPLEMENTED-UNVERIFIED | [CP-20](#cp-20) | engine family | PROVE |
| `REQ-VEC-002` | `AI-006.1`: - [x] `AI-006.1` Embedding versioning and registry | `eoip-phase4-2-requirements.md:763`; audit line 288 | UNSTATED | MISSED | [CP-20](#cp-20) | engine family | TRACE/BUILD |
| `REQ-VEC-003` | `AIDLC-009`: - **Step 4. Agents and AI services.** Boundary telemetry, message bus, fan-out/fan-in, XAI, MLOps, embeddings, causal and GNN, with the human work queue, feedback loop and autonomy catalog. Items: `AGENT-001`, `AGENT-003... | `eoip-phase4-2-requirements.md:178`; audit line 339 | UNSTATED | MISSED | [CP-10](#cp-10) | subject triage | TRACE/BUILD |
| `REQ-VEC-004` | `AIDLC-016`: - **Step 4. Agents and AI services.** Boundary telemetry, message bus, fan-out/fan-in, XAI, MLOps, embeddings, causal and GNN, with the human work queue, feedback loop and autonomy catalog. Items: `AGENT-001`, `AGENT-003... | `eoip-phase4-2-requirements.md:178`; audit line 374 | UNSTATED | MISSED | [CP-10](#cp-10) | subject triage | TRACE/BUILD |
| `REQ-VEC-005` | `GAP-CDC-004`: GAP-CDC-004: Support incremental search/vector/index synchronization | `EOIP-engg-doc-pkg/gaps-requirements.md:806`; audit line 1254 | P1 | IMPLEMENTED-UNVERIFIED | [CP-15](#cp-15) | ID family | PROVE |
| `REQ-VEC-006` | `GAP-DRIFT-005`: GAP-DRIFT-005: Detect embedding-space drift if vector retrieval is used | `EOIP-engg-doc-pkg/gaps-requirements.md:517`; audit line 1284 | P1 | IMPLEMENTED-UNVERIFIED | [CP-20](#cp-20) | subject triage | PROVE |
| `REQ-VEC-007` | `H-02`: Real embedding integration | `KGF-MASTER-BACKLOG.md:270`; audit line 1561 | P0 | PARTIAL | [CP-20](#cp-20) | subject triage | COMPLETE |
| `REQ-VEC-008` | `MS-27`: Usage Intelligence & Embedded Billing Metering Engine | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:436`; audit line 1658 | P2 | IMPLEMENTED-UNVERIFIED | [CP-33](#cp-33) | explicit | PROVE |
| `REQ-VEC-009` | `SR-CON-002`: &#124; SR-CON-002 &#124; **Local-first:** all processing, storage, indexing, embedding, inference and UI serving happen inside the customer-controlled boundary by default; the system MUST function fully offline. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:99`; audit line 2006 | P0 | MISSED | [CP-16](#cp-16) | ID family | TRACE/BUILD |
| `REQ-VEC-010` | `SR-GDB-013`: &#124; SR-GDB-013 &#124; **Event bus adapters:** embedded log, NATS JetStream-class, Kafka/Redpanda-class, RabbitMQ, cloud queues. &#124; P0/P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:218`; audit line 2051 | P0 | MISSED | [CP-13](#cp-13) | ID family | TRACE/BUILD |
| `REQ-VEC-011` | `SR-VDB-001`: &#124; SR-VDB-001 &#124; **Vector Store Port:** upsert/delete by ID with metadata, filtered kNN, hybrid (dense + sparse/BM25), namespace-per-tenant, snapshot/restore, index rebuild, embedding-model version tracking. &#124; P0 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:227`; audit line 2228 | P0 | MISSED | [CP-20](#cp-20) | ID family | TRACE/BUILD |
| `REQ-VEC-012` | `SR-VDB-006`: &#124; SR-VDB-006 &#124; **Full-text/search port:** BM25 keyword, phrase, fuzzy, facets, highlighting, multilingual analyzers; adapters for embedded engine (Tantivy/SQLite-FTS class), PostgreSQL FTS, OpenSearch/Elasticsearch cla... | `EOIP-engg-doc-pkg/super-requirements.md:232`; audit line 2233 | P0 | MISSED | [CP-20](#cp-20) | ID family | TRACE/BUILD |
| `REQ-VEC-013` | `TASK-AIE-010`: - **TASK-AIE-010**: Implement Embedding Management (AI-006) — registry, drift detection, fusion | `EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:53`; audit line 2253 | UNSTATED | MISSED | [CP-20](#cp-20) | subject triage | TRACE/BUILD |
| `REQ-VEC-014` | `TASK-AIE-011`: - **TASK-AIE-011**: Optimize RAG retrieval precision — tune BM25 weights, RRF parameters, reranking thresholds | `EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:58`; audit line 2254 | UNSTATED | MISSED | [CP-20](#cp-20) | subject triage | TRACE/BUILD |
| `REQ-VEC-015` | `TASK-LAI-003`: - **TASK-LAI-003**: Design Embedding Management (AI-006) lifecycle — versioning, drift detection, fusion | `EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:22`; audit line 2337 | UNSTATED | MISSED | [CP-20](#cp-20) | subject triage | TRACE/BUILD |
| `REQ-VEC-016` | `TASK-LIC-007`: - **TASK-LIC-007**: Evaluate vector database options — Milvus (Apache), Weaviate (BSD), Qdrant (Apache) vs managed services | `EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:42`; audit line 2388 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |
| `REQ-VEC-017` | `TASK-LIC-011`: - **TASK-LIC-011**: Track and optimize third-party API costs (LLM inference, embedding generation, cloud compute) | `EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:59`; audit line 2392 | UNSTATED | MISSED | [CP-33](#cp-33) | ID family | TRACE/BUILD |

### A.26 WLB: 2 Records

| Audit ID | Original requirement (audit wording) | Source / audit line | Priority | Audit status | Initial package | Routing basis | Starting action |
|---|---|---|---|---|---|---|---|
| `REQ-WLB-001` | `MS-26`: White-Label Partner Ecosystem & OEM Framework | `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:472`; audit line 1657 | P2 | IMPLEMENTED-UNVERIFIED | [CP-28](#cp-28) | explicit | PROVE |
| `REQ-WLB-002` | `SR-WL-005`: &#124; SR-WL-005 &#124; **OEM rebuild pipeline:** partners can produce rebranded, re-signed bundles/appliance images from a documented pipeline; partner-owned update channel and docs portal. &#124; P1 &#124; | `EOIP-engg-doc-pkg/super-requirements.md:737`; audit line 2239 | P1 | MISSED | [CP-28](#cp-28) | ID family | TRACE/BUILD |

<!-- END REQUIREMENT INDEX -->
