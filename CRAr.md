# Competitive Research Derived Requirements for EOIP

Version: 1.0. Date: 2026-10-16, Asia/Calcutta. Status: **development specification; no requirement accepted by this document's creation**.

Research source: [competitive-research-analysis.md](competitive-research-analysis.md). Comparison data: [competitive-research-matrix.csv](competitive-research-matrix.csv). Local baseline: `ccf9e2891070b9b10eb05791ef8cf4cd1ca08731`.

### Navigation

- [Objective](#1-objective-and-authority)
- [Completion and evidence rules](#2-mandatory-completion-contract)
- [Agent execution protocol](#3-agent-execution-protocol)
- [Chosen defaults](#4-chosen-defaults-and-configuration-rules)
- [Shared contracts](#5-canonical-cross-module-contracts)
- [All 40 detailed requirements](#6-detailed-requirements)
- [Implementation order](#7-dependency-ordered-implementation-programme)
- [End-to-end scenarios](#8-required-end-to-end-scenarios)
- [Release handoff](#9-release-checklist-and-handoff)

## 1. Objective and Authority

Develop a commercially distributed, modular enterprise knowledge graph and ontology platform that can acquire enterprise information through qualified push, polling, crawl and data-access adapters; preserve source permissions/provenance; support deterministic semantics plus probabilistic AI; and expose usable, accessible and governed operational workflows.

The owner delegated design decisions and requested coverage of every named tool and extensible connectivity without a fixed preferred stack/scale. This specification therefore chooses explicit engineering defaults. It does not invent actual customer environments, budgets, staff, source credentials, licenses or contracted SLAs. Missing environment-specific inputs must cause actionable configuration/qualification states, not guessed defaults or silent feature substitution.

This is not an instruction to copy competitors or reimplement their proprietary internals. Build independent designs, use licensed existing domain engines and preserve ownership boundaries. Existing EOIP-owned code remains proprietary commercial software; third-party components retain their own terms. SaaS and customer-installed profiles both matter.

## 2. Mandatory Completion Contract

### 2.1 Atomic Clauses and States

Each numbered clause within CRA-001..040 is an independently tracked acceptance obligation. Stable clause identifiers are formed as `CRA-020.3`, for example. Never close a parent while any required child is open, blocked, failed, unqualified or stale.

Allowed lifecycle: `OPEN -> DESIGNED -> IMPLEMENTED -> VERIFIED -> ACCEPTED`; use `BLOCKED` with dependency/owner/remediation, and `FAILED` for attempted unsuccessful acceptance. `DEFERRED` and `WAIVED` remain visible and do not count as implemented completion. A feature flag, demo-only substitute, mock, test path or interface stub is not VERIFIED.

An ACCEPTED clause requires all applicable evidence: reviewed contract/design; real implementation; positive/negative behavior; actual integration and persistence; authorization; failure/recovery; user workflow; performance/profile limits; deployment compatibility; and independent review. Record nonapplicable evidence categories with a precise reviewed reason, not a generic exemption.

No agent may claim 100% completion by counting files, functions, routes, markers, test names, screenshots or registry entries. No agent may silently reduce scope, replace a real provider with hashing/fake output, mark skipped tests passed, or call unavailable behavior complete. If an external dependency prevents verification, finish safe local work and leave the affected clauses BLOCKED or UNQUALIFIED with exact instructions.

### 2.2 Evidence Record

Maintain an artifact-addressable acceptance ledger. The example is a proposed schema, not a preaccepted result:

```json
{
  "requirement_clause": "CRA-020.3",
  "state": "OPEN",
  "profile": "P1",
  "source_commit": "exact-commit",
  "source_fingerprint": "sha256-of-actual-source-inventory",
  "source_unchanged_during_run": false,
  "artifact_digest": "sha256-of-built-artifact",
  "runtime": {"backend": "configured-real-backend", "engine_version": "pinned", "config_digest": "sha256"},
  "fixture": {"id": "independent-cardinality-corpus", "digest": "sha256", "license": "reviewed"},
  "execution": {"command": "credential-free-argument-vector", "exit_code": null, "started_at": null, "completed_at": null},
  "evidence": [],
  "negative_cases": [],
  "limitations": [],
  "reviewer": null
}
```

Evidence files must exist, parse, match hashes and be produced by the recorded run. Required skipped/xfailed/error/timeout tests fail their gate. A stale artifact cannot qualify a new run. Detect source edits during execution; such a run may report test-process success but cannot claim stable-source acceptance. Distinguish a content-bound dirty worktree from an immutable revision-bound release. Do not store secrets, raw restricted documents or unredacted customer prompts in ordinary receipts.

## 3. Agent Execution Protocol

1. Read this entire file, the research and the relevant existing CP/GUI plans before editing. Capture current Git status/HEAD and preserve concurrent work. Re-read affected modules; do not infer completion from earlier audit labels.
2. Enumerate existing composed routes, contracts, stores, connectors, validators, model providers, frontend screens and real tests. Identify one canonical owner for each capability. Update an existing implementation before creating a duplicate system.
3. Create a clause-level ledger, dependency map and decision records. Implement the P0 correctness/security/data-durability foundations first, then one complete source -> evidence -> accepted graph -> query -> UI journey.
4. For each change, define inputs/outputs, source/tenant boundary, persistence, cancellation, compatibility, resource limits and negative cases before writing production code. Use existing Pydantic, transport, GraphStore, job, policy and UI conventions where valid.
5. Add focused tests, execute them, then execute real integration and workflow tests appropriate to the changed behavior. Rebuild and exercise the exact release artifact for release acceptance. Keep mock/component tests explicitly separate.
6. Update the evidence ledger and affected documentation with actual outcomes. Explain open dependencies and failures. Do not change unrelated business behavior or licensing to make tests green.
7. Re-evaluate the dependency graph after each accepted slice. Continue through feasible work; do not claim a blocked external item prevents unrelated implementation.

No production crawling, customer-data export, source-system write-back, paid cloud provisioning or publication is authorized merely by this specification. Such execution requires the appropriate environment access, business authorization and operational safeguards.

## 4. Chosen Defaults and Configuration Rules

| Concern | Required default / decision | Configurability and validation |
|---|---|---|
| Application structure | Existing Python/FastAPI and React/Vite; modular application with isolated heavy/untrusted workers | Replace providers behind contracts; no blanket rewrite or mandatory microservice split |
| Standards | RDF 1.1, JSON-LD 1.1, SPARQL 1.1, OWL 2 profile-specific behavior, SHACL Core 2017 baseline | New standards/extensions are named profiles with conformance tests, not silent upgrades |
| Reasoning | Qualified RDFS/RL and EL/QL/DL adapters appropriate to the requested task | Profile mismatch rejected; do not hand-roll and advertise complete standards engines |
| Source data ownership | Source-authoritative ACL and revision; metadata-only discovery first | Broader data/profiling/write scopes explicitly configured and separately authorized |
| AI | Provider-disabled/no-egress until an approved local or external provider is configured | Explicit provider/model revision and disclosure of any approved fallback |
| Publishing | Stage, validate, review when required, then publish an exact revision | Policy may allow automatic low-risk publication only through an audited rule |
| Query | 30-s online deadline; bounded rows/expansion; longer work is a job | Tenant quotas and lower source limits take precedence |
| Acquisition | 2 concurrent operations per source initially; bounded queues and retry | Provider-specific limits, Retry-After and customer budgets may lower this |
| Plugins | Disabled/untrusted until signature, contract and permission validation | No arbitrary main-process execution or unreviewed dynamic dependency installation |
| Storage | Durable canonical/control storage for real deployments | Explicit memory fixtures only; no automatic fallback from failed durable storage |
| Presentation | Existing design system; compact task screens, semantic states, reduce-motion, accessible alternatives | Theme/density/locale/workspace preferences versioned and scoped |
| Connectivity | Versioned factories for REST, GraphQL, SOAP, JDBC/ODBC, files/object stores, events/CDC and custom providers | Generic protocol support is not per-product certification |
| Licensing | Proprietary first-party; upstream component terms preserved | Per-artifact/per-deployment SBOM, notices, reviewed obligations |

P0/P1/P2 performance datasets, reference hardware and targets are defined in research section 4 and must be copied into versioned benchmark manifests, not hardcoded into algorithms. These are selected targets, not measured capacity. P1 is the initial enterprise release gate; P2 remains open until independently qualified. Selecting a smaller release must not erase P2 obligations from the overall programme.

Initial quality gates are selected explicitly in research section 14: supported structured/RDF round-trip fidelity 100%; reviewed linking precision >=0.99 and recall >=0.80; answer evidence precision >=0.98, coverage >=0.95 and unanswerable abstention >=0.95; clean printed OCR CER <=0.05; clean-speech WER <=0.15; visual-diagram candidate relation precision >=0.95 and recall >=0.85. Qualify the enabled domain/language/task using the prescribed held-out corpus and confidence reporting. These are target thresholds, not measured quality or permission for automatic high-impact publication. Profile changes require review and requalification.

Customer-specific required inputs: source product/edition/API version, source identity and scopes, URLs/network policy, principal/IdP, residence/retention, secret references, enabled plugins/providers, data-license grants and source ACL model. Reject incomplete configuration with field-specific diagnostics. `Fortuna` and `API Portal` have no uniquely identified product contract; keep those adapters unqualified until identified, while developing the generic protocol framework.

## 5. Canonical Cross-Module Contracts

| Contract | Mandatory fields/behavior |
|---|---|
| TrustedScope | Authenticated subject, tenant, workspace, memberships/grants, policy epoch, delegation and expiry; derive server-side |
| ConnectorManifest | Stable provider ID/version, supported product/API versions, auth modes/scopes, configuration schema, capability flags, limits, license and qualification receipts |
| SourceEvent | Source instance, stable event identity, operation including delete/ACL change, resource ID/revision, observed/source times, payload/checksum reference, cursor and correlation |
| ExtractedDocument | Raw content hash/reference, MIME and detected format, parser/version/config, sections and locators, parent/attachment chain, warnings/errors/budgets and source ACL |
| Assertion | RDF terms or mapped identity, assertion ID/graph, evidence, knowledge state, source/model/rule revisions, temporal fields, policy dependencies and derivations |
| OntologyPackage | Ontology/version IRIs, profile, exact imports/checksums, axioms/shapes/mappings, license, change/reviewer/validation/release manifest |
| SemanticRun | Authorized revision inputs, engine/version/profile, budget, status, unsupported coverage, result/report hash, partial/truncation and cancellation |
| Publication | Expected base revision, proposed mutation digest, validation/approval/policy bindings, idempotency, durable outcome and outbox sequence |
| QueryResult | Declared dialect/profile/plan, authorized scope, revision/freshness, pagination/partial state, evidence and actual execution metrics |
| ActionIntent | Target/type, exact arguments digest, delegated principal, preconditions, source/base/policy revisions, approval/expiry, idempotency and compensation/read-back |

Reuse existing `packages/eoip/contracts/` models through reviewed compatible extensions. Never derive trusted scope from connector payload claims, an LLM response, browser-selected tenant text or a raw user-supplied graph name. Durable identifiers must be stable across retries; canonical RDF terms are not lowercased or rewritten by display preferences.

## 6. Detailed Requirements

All requirements below start OPEN. Existing code paths are **investigation/reuse locations only**, not proof of acceptance. Dependency references are order constraints, not permission to block independent work indefinitely.

### CRA-001. Baseline, Decisions and Acceptance Ledger

Priority P0. Depends on none. Source gaps G06/G18 and all unqualified comparison dimensions. Reuse verification and requirements-registry tooling.

1. Inventory the actual runtime composition and all advertised features, including provider/backend/profile, license, deployment and integration status. Separate implemented, configured, exercised and accepted states.
2. Create decision records for profiles, semantic engines, storage authority, event durability, identity, plugin execution, retention and model policies. State tradeoffs and replacement path. Pin artifact versions/checksums for actual execution; a latest tag is invalid release evidence.
3. Create one ledger entry per numbered CRA clause, with dependency, owner and required evidence categories. Preserve open historical CP/GUI requirements and link overlaps without claiming this specification replaces them.
4. Expose capability discovery based on configuration and runtime readiness. Unsupported, unlicensed, unavailable and unqualified are distinct states; a source name or exported string is not a supported capability.
5. Adopt the selected P0/P1/P2 target profiles as versioned manifests. Record measured outcomes separately. Reject capability declarations not backed by contract tests and appropriate qualification.

Acceptance: inspect an actual instance where a provider is disabled, unavailable and healthy; the UI/API must accurately distinguish all three. Corrupt a receipt or change source during verification and demonstrate that acceptance is rejected. Ledger coverage must reconcile all 40 requirements and their children without treating coverage as completion.

### CRA-002. Modularity and Safe Plugin Runtime

Priority P0. Depends on CRA-001. Sources INV-05/08/10/21/23/29/39/44/45/55.

1. Define versioned interfaces for connector, parser, mapper, graph store, semantic engine, search/vector index, model provider, workflow/action and UI contribution. Declare compatibility ranges and capability negotiation.
2. Keep heavy parsers, JVM reasoners, native codecs, model/GPU work and untrusted extensions outside the request process. Enforce CPU/memory/time/output/file/network budgets and terminate safely.
3. Require signed plugin manifests, publisher identity, digest, dependency inventory, permissions, configuration schema and migration/uninstall behavior. Verify signatures/digests before activation and after retrieval.
4. Provide declarative configuration for ordinary customization. A configuration field must not become arbitrary import/eval/shell execution. Custom code uses a separately authorized isolated execution path.
5. Persist plugin state through owned repositories, scope it by tenant/workspace and version schema migrations. Disable/uninstall must revoke permissions, stop jobs and preserve or safely migrate owned data.
6. Qualify replacement of one engine/plugin without altering domain APIs or corrupting canonical state. Separate licensing entitlements from authorization; neither grants the other's privileges.

Acceptance: run a benign plugin then malicious timeout/memory/network/path-escape cases. Reject a modified signature and incompatible contract. Crash/restart a worker, disable its plugin while work is pending and verify no orphan side effects or leaked tenant state. No plugin marketplace listing alone qualifies execution safety.

### CRA-003. Identity, Scope and Derived-Data Authorization

Priority P0. Depends on CRA-001/002. Source G15/G16 and INV-19/20/24/39/43.

1. Implement trusted principal/session/IdP integration, memberships and tenant/workspace grants, preserving existing approved authentication contracts. Distinguish deployment-token access from a production user session.
2. Enforce deny-by-default authorization at every canonical read/write, traversal, count, search/vector candidate, semantic job, event, report/export, raw download, administration and action boundary.
3. Compose source ACLs and classifications on every derivative. Derived facts and evidence cannot be visible merely because their final subject is visible. Support alternate permitted proofs explicitly; never reveal a restricted proof.
4. Bind caches, drafts, saved views, cursors and local state to authorized scope and policy epoch. Scope switching/disconnect aborts pending work and discards late results. Migrate ambiguous legacy browser data without inferring ownership.
5. Propagate revocation/ACL changes through every index, cache, inference, job and stream; deny unsafe stale access while projections lag. Reauthorize long-running downloads/jobs/actions before sensitive delivery/commit.
6. Test same-backend tenants with identical external IDs, malicious tenant fields, unauthorized graph names and cross-workspace membership changes. Audit defaults such as global/system scopes; do not assume names exempt isolation safely.

Acceptance: two real principals/tenants exercise every boundary, including hidden intermediate nodes, aggregate counts, inferred links, vector neighbors and raw artifacts. Revoke source access during a job and active UI session; previously visible data must not reappear through late results or exports. Review actual persistence/cache/event backends, not one in-memory store.

### CRA-004. Connection Factory and Conformance SDK

Priority P0. Depends on CRA-002/003. Source G07/G08 and INV-27/31/42/43/45. Investigate existing `connectors/factory.py`, base, registry and source contracts.

1. Extend the existing factory with explicit per-capability descriptors: discover, baseline, poll, webhook, CDC, ACL, deletion, attachment, lineage, write-back, resume and health. State supported resource and API versions.
2. Validate configuration/secret references before instantiation. Do not swallow specialization failures and silently switch to a generic endpoint. Fallback requires an explicit configured policy and visible capability downgrade.
3. Provide generic protocol adapters for REST/OpenAPI, GraphQL, SOAP, JDBC/ODBC, SFTP/files/object storage and event/CDC sources through isolated qualified drivers. Unsupported protocols return actionable unavailable states.
4. Implement conformance fixtures and a sandbox runner covering auth, pagination, rate limits, retry, rename/delete, ACL change, ordering, duplicate events, cursor durability, attachment and resource budgets.
5. Store provider version/config digest and qualification receipts with each source instance. Successful connection/authentication is not baseline sync certification, and sync is not write-back approval.
6. Provide authoring templates, contract validation and mock fixtures for a new custom source, followed by separate real-system qualification. Unknown business products must not be advertised as fully supported via `api/entities` defaults.

Acceptance: add a synthetic custom provider without core changes, then a real permitted vendor adapter. Demonstrate invalid credential, incompatible version, unsupported capability and specialization error with no fabricated fallback data. Resume after worker restart without duplicates or skipped resources.

### CRA-005. Work-Tracking and Test-System Adapters

Priority P1. Depends on CRA-004/010/011. Sources Jira, Rally and qTest; source requirement attachment line 123.

1. Qualify Jira Cloud and separately selected Data Center versions for projects, issues, links, comments, custom fields and attachments. Retrieve permission context with authorized scopes and preserve issue/source revision identity.
2. Qualify Rally workspace/project resource types and hierarchy. Preserve artifact relationships and version/cursor semantics; configuration must select actual API version and resource scope.
3. Qualify qTest projects, tests, runs/results and defect associations. Distinguish test definitions from execution results and preserve updates/deletes and project authorization.
4. Research the official API/version/auth/scopes and acquire licensed test access for each product. Store a compatibility manifest and vendor-response fixtures with secrets removed.
5. Demonstrate bounded baseline and incremental acquisition, pagination, rate limits, ACL-only change, deleted/renamed items, attachments and replay. A generic Agile profile cannot substitute for actual vendor semantics.

Acceptance: one live/sandbox end-to-end journey per product and selected edition, followed by restart/replay and access revocation. If a sandbox is unavailable, contract code and mock tests may be IMPLEMENTED, but that product's integration clauses remain BLOCKED/UNQUALIFIED.

### CRA-006. Wiki, Content, Chat and Document Repositories

Priority P1. Depends on CRA-004/010/011/012/013. Sources wiki, Confluence, Slack and Documentum.

1. Provide generic wiki acquisition plus Confluence-specific spaces, pages, versions, links, comments and attachments with inherited/restricted-page permissions and body/macro fidelity diagnostics.
2. Qualify Slack through approved application scopes/events/history APIs. Preserve conversation membership, message/file edits/deletes, threads, pagination and rate limits. Private/direct messages are excluded by default unless explicitly authorized and legally permitted.
3. Qualify Documentum's licensed selected API for object IDs, versions/renditions, folders, relationships, ACL inheritance, checkout and retention/legal holds. Do not reduce document identity to filename or URL.
4. Preserve message/document part and attachment provenance through nested parsing. Redact restricted content before indexing or invoking external providers. Synchronize permissions independently of content changes.
5. Display unsupported macros/renditions, inaccessible content and partial crawl honestly; do not fabricate plain-text equivalents or claim all wiki products share a single API.

Acceptance: restricted page/channel/document cannot appear through raw downloads, graph neighbors, counts or answers. Modify/delete/rename a source and change its ACL; verify all derivatives and historical access rules after restart.

### CRA-007. Code, Build, Artifact and API-Portal Adapters

Priority P1. Depends on CRA-004/010/011. Sources GitHub, GitLab, Artifactory and API Portal.

1. Qualify GitHub/GitLab selected editions for repository/project identity, commits/branches, pull/merge requests, issues, CI metadata and permitted artifacts. Preserve immutable commit references and moving-branch observations separately.
2. Support source-native app/project/repository authorization, installation scope, signed webhook verification, cursor/rate-limit behavior and rename/delete/fork semantics.
3. Qualify Artifactory repository/build/artifact metadata, checksum identity and authorized content, including promotion/deletion and repository ACLs. Never extract/store credentials from build metadata.
4. Treat API Portal as a configurable provider family until its product/API is identified. Support governed OpenAPI/schema/documentation ingestion, API/version relationships and approved discovery without pretending a universal portal endpoint exists.
5. Integrate code/document/schema parsing with provenance to commit/artifact/version and explicit language/format capability. Reject unsupported binaries and untrusted executable content.

Acceptance: show a source change linked to an API/artifact/business entity with exact revision evidence. Revoke private-repository access and prove it disappears from retrieval and exports. Verify signed webhook replay protection and real vendor sandbox data, not only local JSON fixtures.

### CRA-008. Observability and Operational-System Adapters

Priority P1. Depends on CRA-004/010/011/040. Sources ServiceNow, Splunk, Kibana and Grafana.

1. Qualify ServiceNow table/CMDB/incident/change/knowledge profiles with actual row/field ACLs and domain separation. Avoid broad table-service-account rights in default profiles.
2. Qualify Splunk searches/knowledge objects and permitted event metadata under query/time/result budgets. Sensitive log content is separately authorized; credentials and PII must not enter normal graph labels or telemetry.
3. Qualify Kibana saved objects/spaces separately from Elasticsearch/OpenSearch data authority. An authenticated dashboard connection does not authorize every backing index.
4. Qualify Grafana organizations/folders/dashboards and authorized data-source metadata/query results. Never retrieve or expose stored data-source secrets as ordinary metadata.
5. Keep observed telemetry separate from inferred incident causality. Preserve timestamps, source sampling, staleness, missing data and uncertainty. Any write-back/provisioning uses CRA-027.

Acceptance: build an incident -> service -> deployment -> dashboard/log evidence journey. Exercise data-source denial, partial/stale telemetry, truncation and ACL revocation; no made-up operational status or causal conclusion is permitted.

### CRA-009. Warehouses, Catalog Federation and Custom Systems

Priority P1. Depends on CRA-004/024/029. Sources Snowflake, Fortuna and other enterprise systems.

1. Qualify Snowflake metadata and separately authorized data/query-history access with role/warehouse scope, masking/row policies, identifiers, costs and selected SQL/API versions.
2. Provide metadata-only, sampled-data and virtual-query modes with separate permissions, retention and provider readiness. Sampling/query history must be opt-in and redacted before downstream use.
3. Require a real product identity, interface/schema and network/auth contract for Fortuna. Until supplied, expose the configured custom-system adapter and missing-input reason, not an invented Fortuna API.
4. Integrate external catalogs such as OpenMetadata/DataHub/Atlas or commercial platforms through documented public interfaces and explicit ownership/precedence mappings. Do not duplicate their internal metadata model blindly.
5. Certify custom REST/GraphQL/SOAP/database/file/event providers using CRA-004 and scope-aware source fixtures. A signed plugin plus connectivity does not imply complete domain mappings or authorization fidelity.

Acceptance: virtual and materialized queries over the same approved source yield equivalent declared results under masking/null/join cases. Demonstrate source denial, source drift and cost cancellation. Mark product-specific missing access as blocked without blocking the generic factory.

### CRA-010. Durable Source Events and Incremental Synchronization

Priority P0. Depends on CRA-003/004/031. Sources INV-31/39/40/44.

1. Version the SourceEvent contract for upsert, delete, ACL-only change, rename/move and reconciliation. Include source instance, stable event identity, source/resource revision, observed time, payload hash/reference and cursor.
2. Preserve event order guarantees exactly as supplied; use stable deduplication and explicit conflict handling when revisions are opaque or incomparable. A content hash cannot hide ACL changes or repeated temporal events.
3. Implement durable checkpoints/leases and at-least-once acquisition with idempotent published effects. Acknowledge only after the declared durable boundary; reconcile crash windows instead of claiming distributed exactly-once.
4. Handle source absence, partial pages, invalid cursors and expired history with visible reconciliation/backfill states. Do not treat partial baseline absence as deletion.
5. Bind accepted assertions and projections to source/ontology/policy revisions and expose freshness/watermarks. Replay must preserve deletion and policy epochs without resurrecting data.

Acceptance: inject crashes before/after raw persistence, graph publication, outbox delivery and cursor acknowledgement. Replay duplicate/reordered/ACL/delete events and compare canonical graph and projections with independently computed expected state.

### CRA-011. Safe Push, Crawl and Network Access

Priority P0. Depends on CRA-003/004. Sources source-acquisition objective and INV-07/49/52.

1. Authenticate push/webhook sources, validate signature/timestamp/body limits and prevent replay. Apply backpressure and never enqueue unbounded payloads.
2. Restrict crawler schemes, hosts, ports, credentials, depth, pages, bytes, time and request concurrency. Respect authorized source policies and prefer source APIs where available.
3. Revalidate destination/DNS/redirect policy for every request and attachment URL, including IPv6, private/loopback/link-local/cloud metadata and proxy behavior. Never forward credentials to another origin by default.
4. Disable browser scripting and arbitrary resource fetching unless an isolated, explicitly permitted adapter requires it. Keep robots/terms/authorization decisions separate; robots permission is not access authorization.
5. Record crawl coverage, denied/skipped/failed resources and observation times. Partial results cannot become a clean/successful full-source statement.

Acceptance: hostile webhook/replay, redirect/DNS rebinding, zip attachment and credential-forwarding cases are rejected under real network-policy tests. Verify a paused/cancelled crawl releases leases and does not restart itself after cleanup.

### CRA-012. Safe Text, Structured Data and Office Parsing

Priority P0. Depends on CRA-002/010/011. Sources G09/G11 and INV-30/47/49.

1. Extend the existing format engine rather than creating duplicate parsers. Support TXT/CSV/JSON/XML/HTML/RTF, DOC/DOCX, PPT/PPTX and XLS/XLSX through qualified adapters, with explicit dependency readiness and format detection.
2. Preserve paragraph/table/row/column/sheet/slide locators, source encoding and parse/config versions. Distinguish spreadsheet formulas from cached/evaluated values; do not execute macros or embedded code.
3. Apply global input/expanded/member/depth/text/row/section/time budgets across nesting. Use safe XML/HTML parsing and prevent external-entity/remote-resource execution.
4. Repair and test chunking progress/termination. Validate `0 <= overlap < chunk_size`; the final chunk exits; empty, boundary, Unicode and long-unbroken inputs terminate without duplicate infinite suffixes.
5. Model partial extraction and unsupported content explicitly. Preserve raw bytes and warnings so a parser upgrade can rebuild results. A converter exit zero does not certify semantic fidelity.

Acceptance: independently authored golden files for every format plus corrupted, encrypted, malformed and oversized inputs. Run the suspected long-input loop reproduction in a timeout-isolated process, then prove bounded termination and complete intended text coverage. Missing optional tools must yield UNAVAILABLE, not empty successful documents.

### CRA-013. Email, Containers and Nested Provenance

Priority P0. Depends on CRA-012/035/040. Sources attachment format requirements and G17.

1. Parse EML/MIME and approved mailbox protocols with stable message/thread/header/body-part identity. Support MSG only through an explicitly licensed and qualified adapter; do not silently clear existing dependency concerns.
2. Preserve parent message/archive/document relationships, attachment content hashes, original names, source locators and inherited ACL/retention/legal-hold metadata.
3. Enforce combined archive/container expansion, depth, member count and path-safety limits, including duplicate names, symlinks and format confusion. Do not extract untrusted paths into the application filesystem.
4. Handle encrypted/unreadable attachments, malformed MIME, embedded messages and converter failure with per-item diagnostics and aggregate partial/failed status.
5. Prevent automatic remote-image loading, active HTML/script execution and credential extraction from messages. Every attachment download rechecks source authorization.

Acceptance: nested email/archive bombs, traversal, duplicate members, malformed encodings and restricted attachments fail safely. Demonstrate source email deletion/hold behavior across every nested derivative and artifact; preserve separately licensed component obligations.

### CRA-014. Images, Audio and Video

Priority P1. Depends on CRA-002/012/026/035/040. Sources INV-51/52.

1. Provide capability-specific image metadata, OCR, audio transcription, video decode/frame sampling and optional visual extraction adapters. Report exactly which tasks/providers are configured, rather than one multimodal flag.
2. Retain coordinates/page/frame/time spans, language, confidence, provider/model/config revisions and raw evidence references. Transcript/visual outputs remain proposed unless approved by applicable publication policy.
3. Isolate codecs/OCR/ML execution, enforce duration/resolution/frame/sample/output budgets and prohibit unapproved model downloads/network calls. Required model assets must be available in offline bundles.
4. Support cancellation/progress based on actual work and explicit partial output. Preserve unsupported or low-quality segments; never fabricate text, timestamps or diagram topology.
5. Evaluate WER/CER, entity/fact precision/recall and visual task accuracy on licensed domain/language corpora with held-out splits. Apply section 4's selected thresholds through per-task/profile manifests, not as an unsupported universal quality claim.

Acceptance: real permitted media files, degraded scans/noise/unsupported codecs and large/hostile inputs. Verify no external call in no-egress mode, correct evidence locators, timeout cleanup and dependency-unavailable states. File metadata alone does not satisfy OCR/transcription/understanding.

### CRA-015. Engineering Diagram Semantics

Priority P1. Depends on CRA-012/014/016/017. Sources G10 and INV-07/32.

1. Support notation-specific structured diagrams, initially diagrams.net/Chowlk-compatible conceptual diagrams plus declared Mermaid/PlantUML subsets; retain the exact source and parser coverage.
2. Parse components, ports, containment, directions, cardinalities, sequence/event meaning and labels only where supported. Never silently coerce every box to Service or unknown relation to CALLS.
3. Visual extraction from images/video creates candidates with bounding regions, uncertainty and reviewer controls. Distinguish inferred visual interpretation from formal notation semantics.
4. Show a source-versus-graph diff and loss ledger. Unsupported constructs block claims of lossless conversion; the reviewer may explicitly accept a limited projection without altering the source.
5. Round-trip supported models to editable diagrams or maintain a documented non-round-trippable status. Escape/sanitize all generated markup and labels.

Acceptance: independently specified gold diagrams with parallel/directed edges, labels/metacharacters, nesting and intentionally unsupported constructs. Compare formal axioms and business meaning, not just vertex counts or rendered screenshots. Verify correction/rejection propagates to graph/provenance/indexes.

### CRA-016. RDF Terms, Parsing and Standards Fidelity

Priority P0. Depends on CRA-002/003. Sources G03/G05 and INV-01/23/26/55.

1. Use a proven standards parser for the selected RDF/JSON-LD serializations and validate exact supported syntax/profile. Do not describe the EOIP-specific compact JSON-LD importer as a general implementation.
2. Preserve IRI lexical identity, case, blank-node scope, language tags, datatype and literal lexical/value distinctions, RDF lists, named graph identity and annotations. Normalized display labels never mutate canonical IDs.
3. Restrict JSON-LD contexts and ontology imports by the approved resolver policy, hash-pin approved external resources and support disconnected resolution. Block SSRF and remote context changes.
4. Distinguish syntax validity, ontology profile membership, logical consistency and instance-shape validity with separate outcomes.
5. Qualify export/import using independent parsers and canonical/isomorphic dataset comparisons plus semantic competency queries. Report bounds, truncation, unsupported constructs and loss counts explicitly.

Acceptance: case-distinct IRIs remain distinct; equivalent blank-node relabellings compare correctly; datatype/language/named graph round trips preserve meaning. Hostile/cyclic/remote contexts and malformed literals fail safely. A standards-shaped JSON object is not conformance evidence.

### CRA-017. Mapping IR, RDF/LPG Projection and OBDA Inputs

Priority P0. Depends on CRA-010/016. Sources G05/G10/G13 and INV-03/16/26/27/28/30/31/35.

1. Define a versioned, engine-neutral mapping representation for source schema/records to ontology terms, including stable identity, joins, nulls, datatypes, language, provenance and graph policy.
2. Support qualified R2RML/RML adapters and explicit source-dialect/config compatibility. User-defined functions run through CRA-002 with approved capabilities.
3. Preserve multigraph/relationship assertion IDs, edge properties and evidence when projecting to/from property graphs. Record every unsupported construct and lossy coercion; block lossless claims when any loss exists.
4. Separate virtual mappings from materialized ingestion, including source access policy, transaction/snapshot/freshness semantics and resource costs. Do not pretend source rows are copied when queries are virtualized, or vice versa.
5. Provide mapping test cases, dry-run/sample preview, field diagnostics and source-drift analysis. Bind approval/publication to source schema and ontology/mapping revisions.

Acceptance: nulls, multi-value joins, language/datatype literals, blank nodes, duplicate/parallel edges and restricted fields are compared against independent expected RDF and query results. Same approved mapping executes through two qualified adapters with documented equivalence or explicit differences.

### CRA-018. Durable Ontology Registry and Packages

Priority P0. Depends on CRA-016/031/035. Sources INV-02/15/25/46/50/55.

1. Persist ontology/version IRIs, imports/checksums, axioms, annotations, shapes, rules, mappings, namespace ownership, profile and license metadata in a canonical registry.
2. Package immutable releases with full import closure, engine/profile/config references, provenance, validation/reasoning reports and publication signatures/manifests.
3. Keep drafts, accepted releases and source/derived graph revisions separate. No mutable global singleton or browser localStorage may be the sole authority.
4. Support domain packs and optional pinned upper ontologies such as gist, preserving upstream terms, namespaces, attribution and migration notes. Do not imply importing an upper ontology models the entire enterprise.
5. Resolve and install packages atomically with compatibility and signature checks, approved repositories and offline availability. Reject missing/tampered/unlicensed dependencies with explicit diagnostics.

Acceptance: clean restart and fresh-node restore retrieve the same package/release by hash; missing import, changed remote document or incompatible engine cannot silently publish. Compare independently opened package contents and release metadata, not only a database row.

### CRA-019. Profile-Correct Reasoning and Explanations

Priority P0. Depends on CRA-002/016/018. Sources G03/G04 and INV-01/04/17/18/19/20/22/46/48/53/55.

1. Replace or clearly scope the custom helper; do not advertise it as complete OWL DL. Use qualified engines for RDFS, OWL 2 RL/EL/QL/DL tasks with explicit supported profiles and limits.
2. Preserve exact identifiers, load pinned import closure, check profile membership and distinguish consistency, unsatisfiable classes, classification and entailment tasks.
3. Return engine/version/profile, asserted versus inferred statements, explanations/support dependencies, revision and unsupported/error/timeout/cancel status. Timeouts cannot become negative entailment or a clean consistency result.
4. Keep inferred graphs separate and implement dependency-aware invalidation/retraction after source, ontology, identity or ACL changes. Handle multiple justifications correctly.
5. Offer materialized/query-time modes only where supported and measured. Expose resulting plan, amplification and freshness rather than hiding expensive work.
6. Enforce CRA-003 on inference inputs/outputs/explanations. Prevent restricted supporting facts from leaking through an otherwise visible conclusion.

Acceptance: independent gold entailments, non-entailments, incoherence, profile violations, chains/cycles, duplicate support and retraction. The observed case-folding probe must no longer conflate distinct IRIs. Compare a qualified independent engine on the common profile and retain exact differing cases; never replace disagreement with a blanket pass.

### CRA-020. Transactional Shape Validation

Priority P0. Depends on CRA-002/016/018/031. Sources G01/G02 and INV-22/47/48/49.

1. Use a proven validator for declared SHACL Core 2017 coverage; keep extensions/profile versions explicit. A custom Python property checker must be labelled as such until replaced/qualified.
2. Enforce min/max cardinality, datatype/node kind, class, value sets, language/length/pattern/numeric bounds, logical and property-path constraints for the declared profile. Unsupported constraints must produce an explicit unsupported result, never `conforms=true`.
3. Produce standards-compatible reports with focus node, result path/value, source shape/constraint, severity and message, plus revision/engine/config and explicit truncation. Unknown datatype names fail validation setup.
4. Validate the candidate against required existing data and shape/ontology revision. Publication requires revision recheck or transactional isolation so concurrent individually valid writes cannot jointly violate a constraint.
5. Revalidate affected data on shape changes; clearly distinguish incremental supported validation from a full check. Timeout, runtime failure, cancellation and unavailable validator block required publication.
6. Bound CPU/memory/report size and restrict remote imports/SPARQL/JS/UDF execution. Required advanced profiles receive separate qualification rather than implicit enabling.

Acceptance: independently authored min/max counts including zero/multivalues, invalid datatypes, paths, shape updates and concurrent conflicts. Reproduce G01/G02 separately, then demonstrate rejection and unchanged canonical graph after failure. Compare results against an independent validator for the common declared profile.

### CRA-021. Vocabulary, Taxonomy and Multilingual Stewardship

Priority P1. Depends on CRA-018/020/022. Sources INV-06/09/10/11/12/13/14/15/54.

1. Support SKOS concepts/schemes, broader/narrower/related, polyhierarchy, preferred/alternative/hidden labels with language tags, mappings, deprecation/replacement and explicit concept-versus-label identity.
2. Provide SKOS-XL and OntoLex-Lemon through qualified optional profiles where required; reject unsupported export/import rather than flattening silently.
3. Support candidate terms, definitions, synonyms, crosswalk proposals, provenance, domain ownership and review. Model suggestions must not auto-create equivalence or upstream namespace terms.
4. Version vocabularies with classifier/embedding/index dependencies and publication receipts. Record consumer acknowledgement and stale projection state after change.
5. Provide language-aware search/editing and Unicode/RTL-safe presentation, label uniqueness policies and stable IDs independent of translated labels.

Acceptance: multilingual import/edit/export, same-label distinct concepts, cyclic taxonomy policy, polyhierarchy, retired terms and concurrent edits. Change a vocabulary and verify dependent classifier/search output, rollback and evidence preservation. Evaluate domain-specific vocabularies separately from software license rights.

### CRA-022. Ontology and Mapping Change Governance

Priority P1. Depends on CRA-003/018/019/020/031. Sources INV-02/08/12/15/16/25/34/40/46.

1. Implement durable draft -> validation -> review -> approval -> publication -> superseded/rollback lifecycle with explicit roles, separation of duties and audited decisions.
2. Diff semantic statements, imports, shapes, mappings, labels and policy implications rather than only text files. Display impacted data, queries, indexes, sources and actions with bounded analysis.
3. Bind approval to exact candidate, base, ontology, shapes, mapping and policy revisions. Concurrent edits produce conflict/precondition errors; stale approval cannot authorize changed content.
4. Support scheduled/atomic publication and compatible rollback with immutable manifests, consumer acknowledgement, explicit partial failure and repair. Retain history and tenant isolation through restart.
5. Run competency questions, profile/consistency/shapes checks, domain review and migration dry-runs as release gates. No generated or agent-written ontology bypasses these gates.

Acceptance: two editors conflict, reviewer denies, approval expires, policy changes, publication crashes and consumer fails. Prove old/new versions remain reproducible and rollback restores business queries without falsely undoing external actions. A save button or append-only policy call is not governed publication.

### CRA-023. Canonical Identity, Alignment and Reversible Resolution

Priority P1. Depends on CRA-003/010/016/019/022. Sources INV-13/37/52/53/54.

1. Define scoped source identity and canonical-ID mapping with deterministic idempotency, aliases and source-instance boundaries. Same textual ID in two systems/tenants is not one entity.
2. Generate alignment/merge candidates with lexical/structural/model evidence, uncertainty, domain rules and NIL/no-match outcomes. Never infer `owl:sameAs` or merge solely from label or vector similarity.
3. Require approval for high-impact identity/schema changes and run consistency/constraint checks on proposed mappings. Preserve conflicting source claims instead of overwriting them silently.
4. Support reversible merge/split with relationship assertion/evidence/provenance preservation, temporal history and retraction/rebuild of dependent inferences and indexes.
5. Evaluate candidate precision/recall/calibration by tenant/domain/language and adverse ambiguity, with held-out gold data. Model changes require reevaluation and versioned review results.

Acceptance: ambiguous abbreviations, same-name entities, conflicting identifiers and wrong high-confidence matches. Merge then split across restart and compare every edge/evidence/reference with the original. Denied/rejected candidates must never appear as accepted facts.

### CRA-024. Typed Query, Federation and Semantic Planning

Priority P1. Depends on CRA-003/016/017/019/031. Sources G06/G13 and INV-18/19/21/23/27/28/29/35.

1. Publish an exact grammar/capability manifest per dialect/backend: supported EQL/EOQL/OSQL subsets, qualified SPARQL and optional SQL/Cypher/Gremlin/GQL adapters. A language name or exported template is not an executable implementation.
2. Use typed parsed plans and parameterization; reject unsupported constructs and unauthorized operations. No concatenated raw user strings enter privileged backend code.
3. Provide validate/explain/cost/profile/execute/cancel with actual execution information, bounded depth/rows/time and source budgets. Explain output must correspond to the actual plan and reasoning mode.
4. Implement qualified OBDA/federation with source auth delegation, null/bag/set/type semantics, join pushdown, partial-source outcomes, snapshot/freshness and schema-drift handling.
5. Scope templates/history/results and caches; redact sensitive literals. Prevent unauthorized source or graph selection and export of hidden intermediate facts.
6. Separate warmed endpoint benchmarks from CLI startup/setup. Compare materialized and virtual results on declared semantics, not only query syntax.

Acceptance: independent result corpus covering optional/join/null/cardinality/path/aggregate/order/limit cases, source failures and injection. Run against real qualified backends; unsupported dialect constructs must fail clearly. Exercise cost limit and cancellation with backend resource release.

### CRA-025. Search, Embeddings and Projection Fidelity

Priority P1. Depends on CRA-003/010/018/023/031. Sources G12 and INV-10/39/44/54.

1. Version keyword/vector indexes by scope, source/ontology/policy revision, provider/model/tokenizer, dimension, normalization and distance metric.
2. Distinguish deterministic hashing fixtures from real semantic providers. Provider-disabled/unavailable or dimension mismatch cannot silently populate a production semantic index with hashing or zeros.
3. Enforce permission filtering at candidate generation and final delivery, with scoped caches and policy-epoch revocation. Do not retrieve unrestricted candidates into externally visible prompts or diagnostics.
4. Support resumable indexing, deletion, model re-embedding, shadow index evaluation and atomic cutover/rollback. Keep watermarks and explicit stale/unavailable states; projections rebuild from authoritative records.
5. Evaluate recall@k/nDCG/latency by domain/language and ACL selectivity using a labelled corpus. Record corpus splits and model/config changes; do not use graph proximity as relevance gold automatically.

Acceptance: real configured provider, missing provider, vector shape errors, source delete/ACL change, re-embedding crash and rollback. Demonstrate no cross-tenant vector neighbor/count/answer leakage and correct read-back after restart/rebuild.

### CRA-026. Evidence-Bound AI and Ontology Learning

Priority P1. Depends on CRA-003/014/019/020/023/025/040. Sources INV-04/11/14/16/49/51/52/53/54.

1. Keep extraction/classification/alignment/answer suggestions distinct from asserted facts and logical entailments. Record provider/model/prompt/tool/config revisions, evidence spans and policy context.
2. Build bounded authorized context with token budgets, evidence prioritization, freshness and conflicts. Emit clause-level evidence links to actual permitted source revisions; unknown/insufficient evidence produces abstention or explicit uncertainty.
3. Support true streaming/cancellation where configured with cleanup and accurate lifecycle. A graph event feed or simulated token timer is not answer streaming. Prevent partial cancelled output from being saved as an accepted complete answer.
4. Apply independent egress/DLP policy before provider calls. No unapproved endpoint/model downloads or external linting services in no-egress mode; record provider usage/cost without leaking raw data.
5. Treat retrieved documents and tool outputs as untrusted data. Prompt instructions cannot grant tools, alter trusted scope or bypass publication/action approval.
6. Evaluate factual/evidence correctness, abstention, prompt-injection resistance, calibration, domain/language coverage and quality drift against held-out data. Do not call a raw classifier score a probability without calibration evidence.

Acceptance: real local or approved external model traces with actual responses, malicious documents, missing evidence, contradictory sources, unavailable provider and cancellation. Verify the cited span supports the claim and is visible to the current principal at delivery. No scripted canned answers qualify provider integration.

### CRA-027. Governed Actions and Write-Back

Priority P1. Depends on CRA-003/004/022/031/040. Sources INV-33/36/41/43.

1. Define declarative action types, target source/capability, allowed argument schema, preconditions, risk class, execution scope, approval rules and compensation/read-back semantics.
2. Default all sources to read-only. Write-back and source-policy provisioning require explicit configuration, separate permissions and qualified vendor integration.
3. Bind approval to exact intent/arguments digest, source/base/policy revisions, principal/delegation, expiry and nonce. Reauthorize immediately before execution; reject modified/replayed/expired intents.
4. Persist intent/execution/outcome/compensation journals, enforce idempotency and expose honest partial/unknown state for uncertain remote outcomes. Read back the source-system effect before reporting confirmed success.
5. Provide dry-run/impact preview, cancellation before commit, irreversible-action warnings and authorized operator recovery. A graph transaction cannot compensate an external change by itself.

Acceptance: changed arguments, denied permission, revoked credential, stale source, duplicate request, remote timeout after commit and compensation failure. Demonstrate exactly one intended effect through vendor read-back and complete audit, not a returned 200 alone.

### CRA-028. Temporal Knowledge, Impact and Simulation

Priority P1. Depends on CRA-010/019/023/031. Sources G14 and INV-25/36/37/38/40.

1. Model valid time, transaction/observation time, corrections, retractions, source revision and lineage explicitly. Timestamp fields alone do not establish bitemporal query behavior.
2. Support authorized as-of queries, version diffs, provenance and bounded historical snapshots. Retention/hold/deletion rules constrain what history may be served.
3. Separate observed relationships, deterministic graph impact, heuristic paths, stochastic estimates and domain simulation outputs in both API and GUI.
4. Simulations require versioned model/assumptions/inputs, seed, uncertainty and validation protocol. Random-walk frequency is not a calibrated failure probability or a causal intervention estimate.
5. Preserve actual path/hop evidence and cost semantics; do not summarize a multi-hop result as a fabricated two-node explanation. Approval/execution of operational action remains CRA-027.

Acceptance: late events, corrections, clock skew, merges/splits, permission changes and retention across historical reads. Repeat seeded runs, compare sensitivity/gold scenarios, cancel expensive work and ensure simulated facts cannot enter asserted production knowledge without review.

### CRA-029. Catalog, Lineage and Enterprise Context

Priority P1. Depends on CRA-003/010/017/018/024/031. Sources INV-24/28/38/39/40/42/43/44/45.

1. Maintain technical assets, business terms, owners, classifications, quality observations and lineage as typed linked entities with source/freshness and allowed scope.
2. Distinguish observed/base metadata, human curation and effective merged view; define field-level precedence, conflict and reset-to-source behavior. A human override cannot silently hide changed source truth indefinitely.
3. Parse lineage only for supported source/query semantics. Unknown/dynamic statements yield uncertainty and diagnostics, not guessed source-target edges.
4. Expose data-graph versus schema/meta-graph versus provenance/security graph views with stable links and correct object types. Do not relabel the same graph as different capabilities.
5. Federate external catalogs through public versioned APIs with authoritative ownership rules, mappings, duplicate prevention and deletion/ACL propagation.

Acceptance: source rename after human override, stale owner, conflicting glossary, denied lineage source and failed projection. Show the effective value's supporting layer and revision, repair after replay and demonstrate permitted query results through real API/UI/MCP.

### CRA-030. Modular, Accessible and Truthful GUI

Priority P1. Depends on CRA-001/003 and the domain requirement exposed by each screen. Preserve [GUI-UIX-implementation-plan.md](GUI-UIX-implementation-plan.md) and later approved GUI requirements.

1. Deliver complete task routes for source discovery/configuration/runs, ingestion review, ontology/vocabulary authoring, validation/reasoning, graph/entity/evidence, query/answer, changes/impact, actions/jobs, governance, reports, settings and support. Reconcile all existing 27-screen obligations; no duplicate marketing shell.
2. Use shared typed API contracts, authorization/capability-aware navigation, route boundaries, cancellable requests and explicit loading/empty/partial/stale/denied/error/success states. Never populate unavailable administration panels with examples presented as real records.
3. Provide simple task forms plus expert model/query views over the same server state. Display exact revisions, consequences, validation and approval status; preserve unsupported model constructs instead of rewriting them through a simplified editor.
4. Keep graph/table/tree alternatives equivalent for inspection and supported actions. Bound graph scenes; support keyboard navigation, focus/selection identity, screen-reader naming, reflow and readable theme/contrast.
5. Target WCAG 2.2 AA across the supported product, with automated checks plus manual AT and usability qualification. Localize resources/formats, test pseudo-expansion/RTL, and honor reduced motion in CSS and JS/graph animation.
6. Version and scope theme/density/locale/white-label/plugin preferences. Safely validate brand assets and contrast, support preview/rollback and show only real controls backed by supported operations.

Acceptance: real browser against real services and built artifacts across desktop/mobile, four supported themes, reduced motion, keyboard and manual AT. Complete source -> review -> publish -> ask -> evidence -> authorized export/action journeys with failure/restart cases. Screenshots alone do not qualify semantics, persistence, accessibility or usability.

### CRA-031. Durable Jobs, Publication and Event Delivery

Priority P0. Depends on CRA-002/003. Sources G16 and INV-12/25/29/30/31/36/39/41/44/45.

1. Reuse and qualify the existing job/control plane for durable queueing, scope, leases, heartbeats, deadlines, retries, cancellation and terminal status. No process-local state as the only job authority in real deployments.
2. Persist publication intent/mutation/outbox identity consistently. Use a real transaction where available; otherwise implement documented idempotency/reconciliation and expose incomplete states.
3. Define replay/resume/retention/gap semantics for events and consumers, bounded buffers and per-principal authorization. Never put durable bearer credentials in URLs.
4. Enforce retry policy by operation safety; do not blindly retry mutations. Preserve poison events in a governed DLQ with reason, redaction, requeue authority and audit.
5. Fence expired leases/workers and prevent cancelled/revoked jobs from committing later. API/worker restarts and multi-instance claims must be tested on the selected real durable backend.

Acceptance: kill process/network/storage at each commit boundary; race two workers; replay a DLQ item; cancel and revoke scope mid-job. Demonstrate expected published effects, event sequence, cursor and restored job state using independent read-back.

### CRA-032. Observability and Operational Truth

Priority P0. Depends on CRA-001/003/031. Sources INV-39/44/45 and all D16 gaps.

1. Integrate existing structured logging, OpenTelemetry and metrics with source event/job/semantic/publication/projection/query/action correlation and stage timings.
2. Record latency/throughput/error/cancel/denied/unsupported/timeout, queue age, source freshness, projection/policy lag, resource usage, inference amplification and model cost/quality. Unknown/stale telemetry is distinct from zero/healthy.
3. Restrict metrics-label cardinality and sensitive content; protect tenant-specific diagnostics, traces and support bundles. Redact credentials/query literals/raw prompts unless explicitly authorized under retention policy.
4. Provide dashboards and alerts tied to actual measured service behavior, thresholds and runbooks. Avoid initialized example metrics or always-success health endpoints.
5. Test collector absence/backpressure without corrupting critical data flows. Audit and publication durability must not depend on best-effort telemetry alone.

Acceptance: trigger a real failed connector, timeout validator, stuck lease and policy-stale index. Confirm trace correlation, correct alert/state and no secrets in logs/metrics/bundles. Validate observed metric values against independent counters/workload timestamps.

### CRA-033. Backup, Restore and Failure Recovery

Priority P0. Depends on CRA-018/031/032/040. Sources INV-12/20/23/25/37/45 and D18 gaps.

1. Inventory authoritative state: canonical graph, control database, ontology/import/release packages, raw references, identity/policy, outbox/cursors, secrets/KMS recovery metadata and rebuild watermarks.
2. Define consistent encrypted backups/snapshots and retention for each supported deployment/backend, with access controls, immutability where appropriate and off-site failure separation.
3. Implement restore into a clean environment with revision/checksum/query/ACL consistency checks and projection rebuild. Restore secrets through the approved process, not by copying plaintext into bundles.
4. Measure P1 RPO <=15 min and RTO <=4 h for the declared tested failure model; document observed values, exceptions and exact data loss. Do not infer P2/region HA from a local restore.
5. Rehearse partial backup failure, corrupt snapshot, lost key, concurrent writes, API/worker restart and failed upgrade. Fence old writers and prevent event replay from resurrecting deleted/revoked records.

Acceptance: timed independent restore with business queries, ontology revisions, source cursors and adversarial authorization checked after recovery. An archive file or successful backup API response alone is not acceptance.

### CRA-034. Migration, Portability and Rollback

Priority P1. Depends on CRA-016/017/018/022/033/035. Sources INV-01/15/16/25/26/32/34/35/40.

1. Implement documented export/convert/validate/compare/replay/cutover/rollback tooling using the existing CLI conventions, with dry-run and explicit source/target scope. Do not document nonexistent executable commands as available.
2. Preserve source IDs/IRIs, blank-node semantics, literals/languages/datatypes, named graphs, edge assertions, provenance, ACL/retention and ontology history to the declared fidelity profile.
3. Generate a feature/loss/unsupported ledger and source-target reconciliation counts plus independent semantic/query comparisons. Never declare migration lossless when required constructs are dropped/coerced.
4. Stage and shadow-read from a pinned source watermark; replay deltas including ACL/delete events. Bind cutover approval to exact source, mapping, target and policy revision.
5. Support rollback of routing and compatible data/projections, with separately governed external-action compensation. Retain source until qualified restore/query/ACL checks pass.

Acceptance: migrate a standards ontology and a named property-graph corpus through two qualified stores; compare independent output. Inject mapping failure, drift, denied record, partial cutover and rollback. Run on isolated synthetic/licensed data, never customer production by default.

### CRA-035. Commercial Packaging and Supply-Chain Compliance

Priority P0. Depends on CRA-001/002. Sources G17 and INV-02/05/13/15/21/32/35/46/49/50/54/55.

1. Preserve proprietary EOIP-owned licensing and upstream component rights. Do not relabel third-party files or assume all files in an owned directory are owned.
2. Produce exact shipped SBOMs and license/notices/source-obligation records for Python, npm/browser bundles, VSIX, OS/container packages, JVM/WASM/native engines, plugins, models, datasets, vocabularies and assets.
3. Resolve GPL/AGPL/LGPL/OEM/embedding/redistribution and data/model terms for the actual integration and both SaaS/installed profiles. Existing `extract-msg` and ownership/contract questions require explicit resolution, not automated green status.
4. Sign/hash release artifacts and plugin packages, retain build provenance and dependency locks, and make notices available online and offline as appropriate. An installed dependency list is not proof of notices shipped to customers.
5. Qualify installation/upgrade/uninstall and air-gap operation with no unapproved runtime downloads. Entitlements must disable unavailable modules truthfully without granting data access.

Acceptance: inspect actual wheel/image/browser/VSIX/air-gap artifacts and compare embedded inventories/notices with SBOM. Tamper with a plugin/artifact and reject activation. Obtain documented legal/owner approvals; agent-written licensing documents alone cannot clear distribution rights.

### CRA-036. Correctness, Performance and Scale Qualification

Priority P0. Depends on the feature under qualification and CRA-001/032/037. Sources G18 and all D06/D14/D22 gaps.

1. Implement a reproducible workload harness with pinned dataset/generator/license, seed, expected answers, hardware/OS/runtime, engine/config and built-artifact identity.
2. Qualify P0 then P1 then P2 separately using the research profiles. Count asserted/inferred triples, raw/index/vector/history bytes, replicas and cold/hot residency independently.
3. Measure p50/p95/p99, successful/failed/cancelled operations, throughput, source/index lag, peak resources, amplification and cost units. Include cold/warm trials, concurrency, skew, ACL selectivity, updates/deletes and failure/restart.
4. Enforce the selected profile's point-read, bounded graph and approved-query targets without suppressing errors or weakening semantics/security/durability. Do not extrapolate a 1M memory fixture to 500M production capacity.
5. Run independent oracle/differential semantic checks before timing and retain at least three repeated measured trials with variability. Competitive published claims require equivalent semantics/features/hardware and license/publication review.
6. Evaluate parser/OCR/linking/RAG/simulation quality with declared labelled corpora and task-specific thresholds. Use section 4's selected defaults for listed tasks; new simulation/domain/language profiles require explicit additional thresholds before qualification, not arbitrary universal accuracy promises.

Acceptance: raw machine-readable results and independent expected-answer checks bound to manifests. Any wrong answer, leakage, required timeout or missing artifact fails the corresponding gate even when median latency is fast. Vendor benchmark PDFs are comparison evidence, not EOIP execution results.

### CRA-037. Independent QA and Evidence Verification

Priority P0. Depends on CRA-001 and each changed feature. Sources all INV IDs and explicit attachment completion instruction.

1. Maintain unit/property/fuzz, differential semantics, contract, real-backend/vendor integration, security/tenancy, real browser, migration/restore, chaos and performance suites with scope labels.
2. Separate mock tests from actual integration; independently author gold fixtures/oracles so implementation and expected output do not share the same faulty helper. A code change that only alters expected values is not proof of correctness.
3. Build once and verify the exact promoted artifact in each supported deployment/backend/profile, with actual persistence and negative cases. Development-server checks are not release-artifact acceptance.
4. Validate source stability, artifact freshness/hashes, exit codes, skip/error counts, fixtures/environment and review records. Missing/invalid/stale/contradictory evidence fails closed.
5. Perform manual domain, security, accessibility/AT, usability, operations and legal reviews where automated evidence is insufficient. Record reviewer/date/scope, defects and remediation, not a blanket approval checkbox.
6. On concurrent source changes, preserve edits and report the run as unbound; restart affected services and rerun relevant qualification on a stable revision. Historical passes remain historical.

Acceptance: deliberately tamper with a result, reuse stale artifacts, skip a required test, run against memory instead of production backend, edit source mid-run and fail a negative case. The gate must refuse acceptance each time. Verify every claimed ACCEPTED clause can be independently reproduced/read back.

### CRA-038. Support, Service Objectives and Operator Readiness

Priority P1. Depends on CRA-032/033/035/037. Sources D21 gaps and research playbooks.

1. Define supported versions/deployments, lifecycle/deprecation, service ownership, incident severity, escalation and customer versus vendor responsibility.
2. Implement documented incident, scaling, upgrade, backup/restore, credential compromise, poisoned data/model and projection-lag playbooks with diagnostic prerequisites and stop/rollback conditions.
3. Treat 99.9% monthly availability and initial response objectives as engineering proposals until staffing, measurement, exclusions and signed contracts support them. Response is not resolution, and installed customer infrastructure is a separate responsibility boundary.
4. Produce redacted support bundles with authorization, consent, retention and no secrets/customer raw data by default. Provide offline documentation for disconnected customers.
5. Rehearse operational incidents and restore with someone other than the implementer where feasible, recording actual observations and unresolved failures. Agent role-playing is not operator sign-off.

Acceptance: real drill of a source credential compromise, stuck publication and lost store. An authorized operator follows the runbook and proves recovery/denial targets from raw observations. Commercial/counsel approval of SLA and support schedules remains a human external gate.

### CRA-039. Public APIs, SDKs and Developer Ecosystem

Priority P1. Depends on CRA-001/002/003/035/037. Sources INV-08/10/33/39/41/44/50/55.

1. Generate published OpenAPI/JSON schemas and Python/TypeScript SDKs from the composed real application contract. Version public APIs, errors, events and compatibility/deprecation independently from internal endpoints.
2. Expose authorized MCP tools with typed inputs/outputs, provenance and budgets. Tools cannot change trusted identity or obtain broader rights through natural-language arguments.
3. Provide plugin/connector templates, synthetic fixtures, conformance runner, supported-version tables and a documented qualification process. Uncertified community modules remain visibly unqualified.
4. Generate ontology/API/help documentation from exact signed release artifacts, sanitize authored content and support offline/no-egress generation. Follow LODE/WIDOCO version/license transitions explicitly if adopted.
5. Define contribution, vulnerability disclosure, ownership and marketplace policies consistent with proprietary core licensing and upstream obligations. Do not publish customer models/content as examples.

Acceptance: independently build a client and sample plugin from released schemas/templates, run a real scoped task and reject deprecated/incompatible/unauthorized calls. Compare generated docs/SDKs with actual runtime and artifact digest; a static schema file alone is insufficient.

### CRA-040. Privacy, Retention, Deletion and No-Egress Guarantees

Priority P0. Depends on CRA-003/010/018/031. Sources INV-13/24/25/37/42/43/49/51/52/54.

1. Classify source data and derivatives, record lawful/contractual handling policy, residence, retention, consent where applicable and legal holds. Code/model/dataset/content licenses are distinct.
2. Enforce egress policy for connectors, parsers/imports, model calls, linting, telemetry, docs and support bundles. No-egress mode must be measured at the network boundary, not inferred from configuration.
3. Track all copies/derivatives including graph assertions/inferences, raw objects, indexes/vectors, caches, answers, exports, jobs, traces and backups. A deletion workflow must locate and process each according to retention/hold policy.
4. Prevent replay, restore, re-embedding or resynchronization from resurrecting deleted/revoked content. Immutable history requires documented retention/access treatment; it is not an excuse to ignore erasure obligations.
5. Support data-subject/administrative access and deletion workflows with authorization, audit, scoped reports and explicit conflict/escalation for legal hold. Do not claim regulatory certification from a policy module name.

Acceptance: delete and revoke a subject/source while jobs and streams are active, restore/replay older state, then inspect every derivative and network log. Demonstrate retained held material is restricted and reported accurately, with reviewed retention/backup exceptions.

## 7. Dependency-Ordered Implementation Programme

| Gate | Implement | Required exit evidence |
|---|---|---|
| A: truthful baseline | CRA-001; current contract inventory | Complete open ledger; real capability discovery; agreed design defaults |
| B: safe platform | CRA-002/003/031/032/035/040 | Principal/scope, isolated worker, durable state, supply-chain and privacy negative tests |
| C: first acquisition slice | CRA-004/010/011/012/013 plus one real source | Push/pull -> raw -> parse -> staged evidence -> replay after crash |
| D: semantic core | CRA-016/017/018/019/020 | Independent syntax/term/entailment/shape correctness; no invalid publication |
| E: governed knowledge | CRA-021/022/023/028/029 | Reviewed release, source conflict, identity undo and historical authorization |
| F: usable value | CRA-024/025/026/030 | Real query/answer/evidence/save/export with denial and restart |
| G: complete named sources/actions | CRA-005..009/014/015/027 | Every named adapter/media task qualified or explicitly still blocked |
| H: deploy and migrate | CRA-033/034/035/039 | Actual artifact install, migration, rollback, restore and SDK task |
| I: independent acceptance | CRA-036/037/038; remaining GUI/CP obligations | Stable-revision, real-profile evidence; manual reviews; support readiness |

Dependencies with cycles are engineering iteration boundaries, not deadlocks: CRA-031 provides the initial durable substrate for CRA-010, while source-specific event semantics are then qualified through both. CRA-021/022 share a registry/governance foundation; implement the common contracts before integrated acceptance. CRA-037 evolves from Gate A and verifies each slice, not only the final stage.

Do not spend the first phase implementing every optional advanced model or rewriting every screen. First close observed semantic defects and one trustworthy vertical slice. Continue across all named sources and remaining modules with the same acceptance discipline; nothing disappears from the programme because it is deferred.

## 8. Required End-to-End Scenarios

| Scenario | Steps | Independent checks |
|---|---|---|
| E01 source-to-answer | Configure permitted source, discover/select, baseline, parse, review, validate, publish, index, ask and inspect source evidence | Exact source revision, accepted assertions, real model/provider and source ACL |
| E02 live change | Edit source content then ACL, ingest incrementally and query again | Correct cursor/watermark, no duplicate or stale forbidden answer |
| E03 bad semantics | Invalid cardinality/datatype/profile and inconsistent ontology | Explicit failed/unsupported report; unchanged accepted graph |
| E04 model release | Concurrent draft edits, impact, review, signed publish, failed consumer and rollback | Exact revision approval, conflict, no partial hidden state |
| E05 identity correction | Ambiguous entities, reviewed merge, source updates, split | Every relationship/evidence/history restored correctly |
| E06 action | Dry-run, review, approval, source mutation, timeout/retry and read-back | Exact approved arguments, one effect, compensation/unknown outcome truth |
| E07 isolation | Colliding IDs and hidden intermediate facts across tenants/workspaces | No API/UI/search/vector/inference/count/event/export/raw leakage |
| E08 recovery | Kill API/worker/store during acquisition/publication; restore clean node | Durable job/cursor/outbox/revision/ACL consistency and measured RPO/RTO |
| E09 migration | Export different model/store, stage/compare, catch up, cutover and rollback | Declared fidelity, loss ledger, gold queries, no action side effects |
| E10 media | Office/email/archives/images/audio/video/diagram processing | Bounds, locators, dependency readiness, reviewed candidates and no covert egress |
| E11 deletion | Delete/revoke while jobs run, rebuild indexes and restore old backup | No resurrection, reviewed hold policy and complete derivative accounting |
| E12 customization | Install qualified connector/parser/UI/provider plugin and change theme/locale | No core edit required, compatible contracts, sandbox, accessibility and rollback |

Use real permitted backends and source/model integrations for final acceptance; maintain smaller synthetic fixtures for fast tests. Do not substitute E01's API return values for E07/E08 security/recovery evidence.

## 9. Release Checklist and Handoff

The release candidate is not complete until all required clauses for the declared supported profiles and the complete agreed release scope have accepted evidence. Overall programme completion additionally requires all remaining P2 and external/manual obligations; do not describe a scoped P1 release as 100% of the whole programme.

Required final handoff: exact commit/source inventory, reproducible build and artifact digests; supported profile/backend/source/model versions; migration/rollback/restore instructions; SBOM/notices; raw correctness/security/performance/browser results; manual review records; operational playbooks; acceptance ledger; known limitations and blocked/deferred work with owners.

Mandatory refusal conditions: fabricated examples presented as live results; invalid data accepted as conformant; unsupported features treated as pass; cross-tenant leak; uncontrolled egress; unbounded parser/plugin execution; unauthorized/replayed action; unqualified durable-store fallback; missing/stale/source-changed receipts; required test skip; unsigned/tampered release; unresolved required license or regulatory approval.

No plan can make unknown customer systems or proprietary vendor internals assumption-free in advance. This specification makes uncertainty actionable: missing contracts fail configuration or remain explicit blocked qualification, while independently implementable platform work proceeds. The standard of completion is observable, reproducible and authorized behavior in the actual supported deployment, not the volume of code or documentation produced.
