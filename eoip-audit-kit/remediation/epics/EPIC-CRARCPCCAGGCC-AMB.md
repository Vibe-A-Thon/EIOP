# EPIC-CRARCPCCAGGCC-AMB: CRAr_cpccaggcc-requirements.md · ambiguous_tests

*Mapped tests both pass and fail on the audited commit.* 5 tasks, ~23.5 h, priorities {'P0': 5}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-CRA-001 [P0] CRA-001: Baseline, Decisions and Acceptance Ledger

- **Source:** `CRAr_cpccaggcc-requirements.md:465-512` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Ambiguous / L2 (tests passed 26, failed 1)
- **Gaps:** Mapped tests both pass and fail on the audited commit; ID defined at 3 other site(s): see duplicate task DUP-CRA-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D08, FT-F04, FT-F09 · **Effort:** 4.5 h (M, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-001. Baseline, Decisions and Acceptance Ledger

*Aggregated title: Truthful Capabilities Registry, Baseline & Audit Ledger*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | none | A (Truthful baseline) | M1 | G06, G18 | — | — | INV-39 | X-04, X-26, X-33 | — |

**Base statement:** Priority P0. Depends on none. Source gaps G06/G18 and all unqualified comparison dimensions. Reuse verification and requirements-registry tooling.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-001.1** `[CRAr]` Inventory the actual runtime composition and all advertised features, including provider/backend/profile, license, deployment and integration status. Separate implemented, configured, exercised and accepted states.
- **CRA-001.2** `[CRAr]` Create decision records for profiles, semantic engines, storage authority, event durability, identity, plugin execution, retention and model policies. State tradeoffs and replacement path. Pin artifact versions/checksums for actual execution; a latest tag is invalid release evidence.
- **CRA-001.3** `[CRAr]` Create one ledger entry per numbered CRA clause, with dependency, owner and required evidence categories. Preserve open historical CP/GUI requirements and link overlaps without claiming this specification replaces them.
- **CRA-001.4** `[CRAr]` Expose capability discovery based on configuration and runtime readiness. Unsupported, unlicensed, unavailable and unqualified are distinct states; a source name or exported string is not a supported capability.
- **CRA-001.5** `[CRAr]` Adopt the selected P0/P1/P2 target profiles as versioned manifests. Record measured outcomes separately. Reject capability declarations not backed by contract tests and appropriate qualification.
- **CRA-001.6** `[AGG]` Implement a runtime `CapabilityRegistry`. Every adapter (graph backends, semantic engines, connectors, parsers, model providers) registers its declared feature matrix at startup and a health probe; the registry stores per capability: capability ID, provider ID, provider version, profile, state, last probe time and qualification receipt reference.
- **CRA-001.7** `[RES]` Capability state is exactly one of `SUPPORTED_QUALIFIED`, `SUPPORTED_UNQUALIFIED`, `DISABLED`, `UNAVAILABLE`, `UNLICENSED`, `UNSUPPORTED`. `SUPPORTED_QUALIFIED` can only be set by the ledger verifier from an ACCEPTED receipt; it can never be authored 
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/acceptance/test_cra_001_acceptance.py::test_cra_001_9_ledger_and_receipts_storage_contract
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)
4. Resolve duplicate definition first: DUP-CRA-001

**Acceptance criteria**
- [ ] Priority P0. Depends on none. Source gaps G06/G18 and all unqualified comparison dimensions. Reuse verification and requirements-registry tooling.
- [ ] CRA-001.1 [CRAr] Inventory the actual runtime composition and all advertised features, including provider/backend/profile, license, deployment and integration status. Separate implemented, configured, exercised and accepted states
- [ ] CRA-001.2 [CRAr] Create decision records for profiles, semantic engines, storage authority, event durability, identity, plugin execution, retention and model policies. State tradeoffs and replacement path. Pin artifact versions/checksums for actual execution; a latest tag is invalid release evidence
- [ ] CRA-001.3 [CRAr] Create one ledger entry per numbered CRA clause, with dependency, owner and required evidence categories. Preserve open historical CP/GUI requirements and link overlaps without claiming this specification replaces them
- [ ] CRA-001.4 [CRAr] Expose capability discovery based on configuration and runtime readiness. Unsupported, unlicensed, unavailable and unqualified are distinct states; a source name or exported string is not a supported capability
- [ ] CRA-001.5 [CRAr] Adopt the selected P0/P1/P2 target profiles as versioned manifests. Record measured outcomes separately. Reject capability declarations not backed by contract tests and appropriate qualification
- [ ] CRA-001.6 [AGG] Implement a runtime CapabilityRegistry. Every adapter (graph backends, semantic engines, connectors, parsers, model providers) registers its declared feature matrix at startup and a health probe; the registry stores per capability: capability ID, provider ID, provider version, profile, state, last probe time and qualification receipt reference
- [ ] CRA-001.7 [RES] Capability state is exactly one of SUPPORTEDQUALIFIED, SUPPORTEDUNQUALIFIED, DISABLED, UNAVAILABLE, UNLICENSED, UNSUPPORTED. SUPPORTEDQUALIFIED can only be set by the ledger verifier from an ACCEPTED receipt; it can never be authored in configuration
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/capabilities/model.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/capabilities/model.py#L1-L1), [`packages/eoip/capabilities/registry.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/capabilities/registry.py#L1-L1), [`packages/eoip/capabilities/router.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/capabilities/router.py#L1-L1), [`scripts/build_master_suite.py:685`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L685-L685), [`scripts/enhance_master_suite.py:524`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L524-L524)
- tests: `tests/acceptance/test_baseline_facts.py:1`, `tests/acceptance/test_cra_001_acceptance.py:4`, `tests/acceptance/test_verify_ledger.py:23`, `tests/integration/test_capabilities_route.py:1`, `tests/unit/test_capability_registry.py:1`
- failing: `tests/acceptance/test_cra_001_acceptance.py::test_cra_001_9_ledger_and_receipts_storage_contract`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CRA-002 [P0] CRA-002: Modularity and Safe Plugin Runtime

- **Source:** `CRAr_cpccaggcc-requirements.md:513-554` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Ambiguous / L2 (tests passed 16, failed 2)
- **Gaps:** Mapped tests both pass and fail on the audited commit; ID defined at 3 other site(s): see duplicate task DUP-CRA-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F03, FT-F04, FT-F09 · **Effort:** 5.5 h (M, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-002. Modularity and Safe Plugin Runtime

*Aggregated title: Sandboxed Micro-Worker Runtime & Resource Fencing*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-001 | B (Safe platform) | M1 | G11 | ONT-003 | — | INV-05, INV-08, INV-10, INV-21, INV-23, INV-29, INV-30, INV-34, INV-35, INV-41, INV-44, INV-45, INV-47, INV-48, INV-55 | X-27 | — |

**Base statement:** Priority P0. Depends on CRA-001. Sources INV-05/08/10/21/23/29/39/44/45/55.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-002.1** `[CRAr]` Define versioned interfaces for connector, parser, mapper, graph store, semantic engine, search/vector index, model provider, workflow/action and UI contribution. Declare compatibility ranges and capability negotiation.
- **CRA-002.2** `[CRAr]` Keep heavy parsers, JVM reasoners, native codecs, model/GPU work and untrusted extensions outside the request process. Enforce CPU/memory/time/output/file/network budgets and terminate safely.
- **CRA-002.3** `[CRAr]` Require signed plugin manifests, publisher identity, digest, dependency inventory, permissions, configuration schema and migration/uninstall behavior. Verify signatures/digests before activation and after retrieval.
- **CRA-002.4** `[CRAr]` Provide declarative configuration for ordinary customization. A configuration field must not become arbitrary import/eval/shell execution. Custom code uses a separately authorized isolated execution path.
- **CRA-002.5** `[CRAr]` Persist plugin state through owned repositories, scope it by tenant/workspace and version schema migrations. Disable/uninstall must revoke permissions, stop jobs and preserve or safely migrate owned data.
- **CRA-002.6** `[CRAr]` Qualify replacement of one engine/plugin without altering domain APIs or corrupting canonical state. Separate licensing entitlements from authorization; neither grants the other's privileges.
- **CRA-002.7** `[AGG]` Default worker resource classes: `standard` <= 2 GiB RSS, <= 2 CPU, 30 s wall clock per item; `heavy` (OCR, ASR, JVM reasoners, large office conversion) <= 8 GiB, <= 4 CPU, 600 s, always executed as a durable job. Limits are configurable per class and per tenant; the lower of tenant and class limit wins.
- **CRA-002.8** `[AGG]` On any limit breach the orchestrator terminates the whole worker process tree within 1 s of detection, releases leases, file descriptors and temp dire
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/security/test_worker_isolation.py::test_infinite_loop_timeout_killed_within_one_second tests/security/test_worker_isolation.py::test_memory_balloon_terminated_safely
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)
4. Resolve duplicate definition first: DUP-CRA-002

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-001. Sources INV-05/08/10/21/23/29/39/44/45/55.
- [ ] CRA-002.1 [CRAr] Define versioned interfaces for connector, parser, mapper, graph store, semantic engine, search/vector index, model provider, workflow/action and UI contribution. Declare compatibility ranges and capability negotiation
- [ ] CRA-002.2 [CRAr] Keep heavy parsers, JVM reasoners, native codecs, model/GPU work and untrusted extensions outside the request process. Enforce CPU/memory/time/output/file/network budgets and terminate safely
- [ ] CRA-002.3 [CRAr] Require signed plugin manifests, publisher identity, digest, dependency inventory, permissions, configuration schema and migration/uninstall behavior. Verify signatures/digests before activation and after retrieval
- [ ] CRA-002.4 [CRAr] Provide declarative configuration for ordinary customization. A configuration field must not become arbitrary import/eval/shell execution. Custom code uses a separately authorized isolated execution path
- [ ] CRA-002.5 [CRAr] Persist plugin state through owned repositories, scope it by tenant/workspace and version schema migrations. Disable/uninstall must revoke permissions, stop jobs and preserve or safely migrate owned data
- [ ] CRA-002.6 [CRAr] Qualify replacement of one engine/plugin without altering domain APIs or corrupting canonical state. Separate licensing entitlements from authorization; neither grants the other's privileges
- [ ] CRA-002.7 [AGG] Default worker resource classes: standard <= 2 GiB RSS, <= 2 CPU, 30 s wall clock per item; heavy (OCR, ASR, JVM reasoners, large office conversion) <= 8 GiB, <= 4 CPU, 600 s, always executed as a durable job. Limits are configurable per class and per tenant; the lower of tenant and class limit wins
- [ ] CRA-002.8 [AGG] On any limit breach the orchestrator terminates the whole worker process tree within 1 s of detection, releases leases, file descriptors and temp directories, records outcome TIMEOUT, OOM or LIMITEXCEEDED, returns HTTP 504 for synchronous calls or marks the job FAILED with the reason, and respawns a healthy worker. The API process keeps serving
- [ ] CRA-002.9 [AGG] Semantic micro-worker protocol (INV-55): JVM engines (OWL API, ELK, optional HermiT/Openllet, ROBOT, optional Jena/TopBraid SHACL) run only behind a versioned worker contract (gRPC or stdio JSON-RPC) carrying request ID, deadline, input artifact hashes, engine name/version/profile and resource class. No JVM runs inside the API process
- [ ] CRA-002.10 [OCA] Graph backend ports: existing adapters (in-memory, HugeGraph, Neo4j, Neptune in packages/eoip/graph/backends.py) and a new RDF-store port (Apache Jena Fuseki as reference implementation, GraphDB as certified commercial option per ONT-003) declare capabilities through the same negotiation. GPL/AGPL servers (Neo4j Community, Virtuoso OSE) are reachable only over their network protoc
- [ ] CRA-002.11 [OCA] Preserve existing conventions: Pydantic request models at module level (required for FastAPI OpenAPI schema resolution), thread-safe singleton accessors, and a stats() method on every engine wired into brainos.py telemetry
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/backends.py:345`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/backends.py#L345-L345), [`packages/eoip/graph/rdf_backend.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/rdf_backend.py#L1-L1), [`packages/eoip/plugins/contracts.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/plugins/contracts.py#L1-L1), [`packages/eoip/plugins/manifest.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/plugins/manifest.py#L1-L1), [`packages/eoip/plugins/state.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/plugins/state.py#L1-L1), [`packages/eoip/workers/protocol.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/workers/protocol.py#L1-L1), [`packages/eoip/workers/supervisor.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/workers/supervisor.py#L1-L1)
- tests: `tests/integration/test_plugin_lifecycle.py:1`, `tests/security/test_worker_isolation.py:1`, `tests/unit/test_plugin_manifest.py:1`
- failing: `tests/security/test_worker_isolation.py::test_infinite_loop_timeout_killed_within_one_second`, `tests/security/test_worker_isolation.py::test_memory_balloon_terminated_safely`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-CRA-027 [P0] CRA-027: Governed Actions and Write-Back

- **Source:** `CRAr_cpccaggcc-requirements.md:1455-1493` (heading) · **Type:** Security · **Severity:** High
- **Now:** Ambiguous / L2 (tests passed 9, failed 1)
- **Gaps:** Mapped tests both pass and fail on the audited commit; ID defined at 3 other site(s): see duplicate task DUP-CRA-027; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D15, FT-F04, FT-F09 · **Effort:** 4.5 h (M, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-027. Governed Actions and Write-Back

*Aggregated title: Two-Phase Operational Write-Back Outbox & Action Engine*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-003/004/022/031/040 | G (Named sources, media and actions) | M6 | — | ONT-009 | — | INV-05, INV-33, INV-36, INV-41, INV-43 | — | H-03 |

**Base statement:** Priority P1. Depends on CRA-003/004/022/031/040. Sources INV-33/36/41/43.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-027.1** `[CRAr]` Define declarative action types, target source/capability, allowed argument schema, preconditions, risk class, execution scope, approval rules and compensation/read-back semantics.
- **CRA-027.2** `[CRAr]` Default all sources to read-only. Write-back and source-policy provisioning require explicit configuration, separate permissions and qualified vendor integration.
- **CRA-027.3** `[CRAr]` Bind approval to exact intent/arguments digest, source/base/policy revisions, principal/delegation, expiry and nonce. Reauthorize immediately before execution; reject modified/replayed/expired intents.
- **CRA-027.4** `[CRAr]` Persist intent/execution/outcome/compensation journals, enforce idempotency and expose honest partial/unknown state for uncertain remote outcomes. Read back the source-system effect before reporting confirmed success.
- **CRA-027.5** `[CRAr]` Provide dry-run/impact preview, cancellation before commit, irreversible-action warnings and authorized operator recovery. A graph transaction cannot compensate an external change by itself.
- **CRA-027.6** `[AGG]` `ActionIntent` (section 6) lifecycle: PROPOSED -> STAGED -> APPROVED -> EXECUTING -> COMPLETED | FAILED | COMPENSATED, plus `UNKNOWN_OUTCOME` for uncertain remote results.
- **CRA-027.7** `[OCA]` Action types are declared as SHACL action shapes (`OntologyAction`, ONT-009) with SHACL preconditions, declared effects (classes/properties mutated), target connector, approval policy keyed to the existing `AutonomyLevel` ladder (destructive actions require the human-controlled level, HCTL) and an immutable audit receipt.
- **CRA-027.8** `[AGG]` `Idempotency-Key` header (16-128 chars) is mandatory; approvals carry a signature, nonce and default 5-minute expiry; replay or parameter change after approval is rejected.
- **CRA-027.9** `[RES]` Route consolidation: canonical routes `POST /api/v1/actions/execute`, `GET /api/v1/act
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/acceptance/test_governed_actions_acceptance.py::test_cra_027_9_canonical_routes_and_oca_aliases
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)
4. Resolve duplicate definition first: DUP-CRA-027

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-003/004/022/031/040. Sources INV-33/36/41/43.
- [ ] CRA-027.1 [CRAr] Define declarative action types, target source/capability, allowed argument schema, preconditions, risk class, execution scope, approval rules and compensation/read-back semantics
- [ ] CRA-027.2 [CRAr] Default all sources to read-only. Write-back and source-policy provisioning require explicit configuration, separate permissions and qualified vendor integration
- [ ] CRA-027.3 [CRAr] Bind approval to exact intent/arguments digest, source/base/policy revisions, principal/delegation, expiry and nonce. Reauthorize immediately before execution; reject modified/replayed/expired intents
- [ ] CRA-027.4 [CRAr] Persist intent/execution/outcome/compensation journals, enforce idempotency and expose honest partial/unknown state for uncertain remote outcomes. Read back the source-system effect before reporting confirmed success
- [ ] CRA-027.5 [CRAr] Provide dry-run/impact preview, cancellation before commit, irreversible-action warnings and authorized operator recovery. A graph transaction cannot compensate an external change by itself
- [ ] CRA-027.7 [OCA] Action types are declared as SHACL action shapes (OntologyAction, ONT-009) with SHACL preconditions, declared effects (classes/properties mutated), target connector, approval policy keyed to the existing AutonomyLevel ladder (destructive actions require the human-controlled level, HCTL) and an immutable audit receipt
- [ ] CRA-027.8 [AGG] Idempotency-Key header (16-128 chars) is mandatory; approvals carry a signature, nonce and default 5-minute expiry; replay or parameter change after approval is rejected
- [ ] CRA-027.9 [RES] Route consolidation: canonical routes POST /api/v1/actions/execute, GET /api/v1/actions, POST /api/v1/actions/{id}/approve; OCA aliases POST /ontology/actions/{id}/invoke and GET /ontology/actions forward to them. Write-back stays disabled until decision H-03
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/actions/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/actions/__init__.py#L1-L1), [`packages/eoip/actions/contracts.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/actions/contracts.py#L1-L1), [`packages/eoip/actions/engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/actions/engine.py#L1-L1), [`packages/eoip/actions/router.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/actions/router.py#L1-L1), [`packages/eoip/observability/telemetry_separation.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/observability/telemetry_separation.py#L7-L7), [`scripts/build_master_suite.py:238`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L238-L238), [`scripts/enhance_master_suite.py:240`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L240-L240), [`scripts/patch_suite_and_dashboard.py:159`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L159-L159)
- tests: `scripts/test_cap_enrichment.py:107`, `scripts/test_master_caps_enrichment.py:121`, `tests/acceptance/test_governed_actions_acceptance.py:1`
- failing: `tests/acceptance/test_governed_actions_acceptance.py::test_cra_027_9_canonical_routes_and_oca_aliases`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CRA-030 [P0] CRA-030: Modular, Accessible and Truthful GUI

- **Source:** `CRAr_cpccaggcc-requirements.md:1558-1589` (heading) · **Type:** Security · **Severity:** High
- **Now:** Ambiguous / L2 (tests passed 8, failed 2)
- **Gaps:** Mapped tests both pass and fail on the audited commit; ID defined at 3 other site(s): see duplicate task DUP-CRA-030; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09, FT-H01 · **Effort:** 4.5 h (M, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-030. Modular, Accessible and Truthful GUI

*Aggregated title: Accessible Multi-View Enterprise UI Workbench (WCAG 2.2 AA)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-001/003 and the domain requirement exposed by each screen | F (Usable value) | M7 | G15 | — | — | INV-01, INV-03, INV-04, INV-05, INV-06, INV-08, INV-09, INV-28, INV-32, INV-38, INV-50, INV-51 | — | — |

**Base statement:** Priority P1. Depends on CRA-001/003 and the domain requirement exposed by each screen. Preserve [GUI-UIX-implementation-plan.md](GUI-UIX-implementation-plan.md) and later approved GUI requirements.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-030.1** `[CRAr]` Deliver complete task routes for source discovery/configuration/runs, ingestion review, ontology/vocabulary authoring, validation/reasoning, graph/entity/evidence, query/answer, changes/impact, actions/jobs, governance, reports, settings and support. Reconcile all existing 27-screen obligations; no duplicate marketing shell.
- **CRA-030.2** `[CRAr]` Use shared typed API contracts, authorization/capability-aware navigation, route boundaries, cancellable requests and explicit loading/empty/partial/stale/denied/error/success states. Never populate unavailable administration panels with examples presented as real records.
- **CRA-030.3** `[CRAr]` Provide simple task forms plus expert model/query views over the same server state. Display exact revisions, consequences, validation and approval status; preserve unsupported model constructs instead of rewriting them through a simplified editor.
- **CRA-030.4** `[CRAr]` Keep graph/table/tree alternatives equivalent for inspection and supported actions. Bound graph scenes; support keyboard navigation, focus/selection identity, screen-reader naming, reflow and readable theme/contrast.
- **CRA-030.5** `[CRAr]` Target WCAG 2.2 AA across the supported product, with automated checks plus manual AT and usability qualification. Localize resources/formats, test pseudo-expansion/RTL, and honor reduced motion in CSS and JS/graph animation.
- **CRA-030.6** `[CRAr]` Version and scope theme/density/locale/white-label/plugin preferences. Safely validate brand assets and contrast, support preview/rollback and show only real controls backed by supported operations.
- **CRA-030.7** `[AGG]` Workbenches: Source Management; Ontology Modeler (bounded graph ca
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/gui/test_gui_workbench_acceptance.py::test_cra_030_2_typed_contracts_and_truthful_states tests/gui/test_gui_workbench_acceptance.py::test_cra_030_a_acceptance_gate
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)
4. Resolve duplicate definition first: DUP-CRA-030

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-001/003 and the domain requirement exposed by each screen. Preserve GUI-UIX-implementation-plan.md and later approved GUI requirements.
- [ ] CRA-030.1 [CRAr] Deliver complete task routes for source discovery/configuration/runs, ingestion review, ontology/vocabulary authoring, validation/reasoning, graph/entity/evidence, query/answer, changes/impact, actions/jobs, governance, reports, settings and support. Reconcile all existing 27-screen obligations; no duplicate marketing shell
- [ ] CRA-030.2 [CRAr] Use shared typed API contracts, authorization/capability-aware navigation, route boundaries, cancellable requests and explicit loading/empty/partial/stale/denied/error/success states. Never populate unavailable administration panels with examples presented as real records
- [ ] CRA-030.3 [CRAr] Provide simple task forms plus expert model/query views over the same server state. Display exact revisions, consequences, validation and approval status; preserve unsupported model constructs instead of rewriting them through a simplified editor
- [ ] CRA-030.4 [CRAr] Keep graph/table/tree alternatives equivalent for inspection and supported actions. Bound graph scenes; support keyboard navigation, focus/selection identity, screen-reader naming, reflow and readable theme/contrast
- [ ] CRA-030.5 [CRAr] Target WCAG 2.2 AA across the supported product, with automated checks plus manual AT and usability qualification. Localize resources/formats, test pseudo-expansion/RTL, and honor reduced motion in CSS and JS/graph animation
- [ ] CRA-030.6 [CRAr] Version and scope theme/density/locale/white-label/plugin preferences. Safely validate brand assets and contrast, support preview/rollback and show only real controls backed by supported operations
- [ ] CRA-030.7 [AGG] Workbenches: Source Management; Ontology Modeler (bounded graph canvas plus expert Manchester-syntax editor); Knowledge Explorer; Ask AI with side-by-side evidence/citation panels; Action Governance (approval queues, dry-run diffs, audit timelines)
- [ ] CRA-030.8 [OCA] Baseline audit of the existing 90+ React components and 146 ARIA attributes; add an i18n framework (currently zero i18n) with pseudo-locale and RTL tests
- [ ] CRA-030.9 [AGG] Automated checks: Playwright end-to-end and axe accessibility suites exposed as npm run test:e2e and npm run test:a11y (create the scripts if absent); no placeholder or mock records in production builds
- [ ] obligation CRA-030.A (only after every clause above is ACCEPTED)
- [ ] [CRAr] real browser against real services and built artifacts across desktop/mobile, four supported themes, reduced motion, keyboard and manual AT. Complete source -> review -> publish -> ask -> evidence -> authorized export/action journeys with failure/restart cases. Screenshots alone do not qualify semantics, persistence, accessibility or usability
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/web/src/i18n.js:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/web/src/i18n.js#L2-L2), [`packages/eoip/claims/registry.py:27`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/claims/registry.py#L27-L27)
- tests: `tests/gui/test_gui_workbench_acceptance.py:1`
- failing: `tests/gui/test_gui_workbench_acceptance.py::test_cra_030_2_typed_contracts_and_truthful_states`, `tests/gui/test_gui_workbench_acceptance.py::test_cra_030_a_acceptance_gate`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CRA-045 [P0] CRA-045: Deterministic–Probabilistic Boundary and Neuro-Symbolic Arbitration

- **Source:** `CRAr_cpccaggcc-requirements.md:2082-2119` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Ambiguous / L2 (tests passed 14, failed 1)
- **Gaps:** Mapped tests both pass and fail on the audited commit; ID defined at 4 other site(s): see duplicate task DUP-CRA-045; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D08, FT-F04, FT-F09 · **Effort:** 4.5 h (M, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-045. Deterministic–Probabilistic Boundary and Neuro-Symbolic Arbitration

*Aggregated title: (new in v3.1) Dual-Path Semantics — W3C Determinism plus Probabilistic AI*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-003/016/019/020/024/025/026/043 | F (Usable value) | M10 | G21 | — | I2, I18 | INV-19 | X-34, X-35, X-36 | — |

**Base statement:** Priority P0. Depends on CRA-003/016/019/020/024/025/026/043. Source: the closing instruction of the original attachment, `crarprompt.txt` — *"my architecture should be capable enough to handle deterministic semantics (W3C standard ontologies, schema enforcement) and probabilistic AI (vector embeddings, LLM context windows, and graph traversals)"* — and G21. Interpretation (binding): graph traversal is deterministic when executed as an exact algorithm (CRA-024, CRA-028.7) and belongs to the probabilistic pipeline when it assembles LLM context (CRA-026.7) or uses learned or sampled weights (CRA-028.4, CRA-044); the traversal result keeps its exactness label in both uses.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-045.1** `[PRM]` Classify every producer of knowledge or answers as deterministic (RDF parsing and serialization, SHACL validation, profile-qualified reasoning, exact query and traversal, deterministic mapping) or probabilistic (embeddings and similarity, LLM generation and extraction, learned graph models, OCR/ASR/vision, sampled or heuristic traversal, alignment suggestions). The class is part of each producer's capability registration (CRA-001) and appears in every result payload.
- **CRA-045.2** `[PRM]` Probabilistic output is never asserted directly. It enters as `knowledge_state=proposed` with `ModelLineage`, calibrated confidence where calibration exists, and evidence. Promotion to `asserted` requires deterministic validation — SHACL (CRA-020), profile and consistency checks (CRA-019), identity rules (CRA-023) — followed by the review policy of CRA-022. A promoted assertion keeps its probabilistic origin and its approver.
- **CRA-045.3** `[PRM]` Dual-path answering: wherever an exact deterministic path exists for a question (SPARQL/EQL query, bounded traversal, entailment check), it runs beside the probabilistic path and both results are returned with their producer class. Agreement is reported as `CORROBORATED`, disagreement as `DISPUTED` with both results and th
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/acceptance/test_cra_001_acceptance.py::test_cra_001_9_ledger_and_receipts_storage_contract
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)
4. Resolve duplicate definition first: DUP-CRA-045

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-003/016/019/020/024/025/026/043. Source: the closing instruction of the original attachment, crarprompt.txt — "my architecture should be capable enough to handle deterministic semantics (W3C standard ontologies, schema enforcement) and probabilistic AI (vector embeddings, LLM context windows, and graph traversals)" — and G21. Interpretation (binding): graph traversal is
- [ ] CRA-045.1 [PRM] Classify every producer of knowledge or answers as deterministic (RDF parsing and serialization, SHACL validation, profile-qualified reasoning, exact query and traversal, deterministic mapping) or probabilistic (embeddings and similarity, LLM generation and extraction, learned graph models, OCR/ASR/vision, sampled or heuristic traversal, alignment suggestions). The class is part of
- [ ] CRA-045.2 [PRM] Probabilistic output is never asserted directly. It enters as knowledgestate=proposed with ModelLineage, calibrated confidence where calibration exists, and evidence. Promotion to asserted requires deterministic validation — SHACL (CRA-020), profile and consistency checks (CRA-019), identity rules (CRA-023) — followed by the review policy of CRA-022. A promoted assertion keeps its 
- [ ] CRA-045.3 [PRM] Dual-path answering: wherever an exact deterministic path exists for a question (SPARQL/EQL query, bounded traversal, entailment check), it runs beside the probabilistic path and both results are returned with their producer class. Agreement is reported as CORROBORATED, disagreement as DISPUTED with both results and their evidence, and a probabilistic-only answer as UNCORROBORATED.
- [ ] CRA-045.4 [PRM] Deterministic constraints bound probabilistic proposals before display: a candidate that violates ontology domain/range, disjointness or a SHACL constraint is shown as rejected-by-constraint with the violated shape or axiom, not as a ranked suggestion
- [ ] CRA-045.5 [PRM] Separation holds in storage, query and export: asserted-only queries, the SPARQL endpoint and RDF exports exclude proposed statements unless the caller explicitly asks for them, and exported proposed statements carry their knowledge state and lineage in a named graph (urn:eoip:proposed:{tenant}) so they cannot be mistaken for facts downstream
- [ ] CRA-045.6 [PRM] Calibration honesty: a raw model output is labelled score, never probability or confidence, until a calibrator exists for that model and task with recorded calibration error (CRA-026.6, CRA-044.5)
- [ ] CRA-045.7 [PRM] Reproducibility: every probabilistic result records model or provider revision, input or prompt digest, context-manifest digest (CRA-026.12), seed where applicable and the deterministic inputs (snapshot, ontology and policy revisions), so a reviewer can rerun it; non-reproducible providers are labelled as such
- [ ] CRA-045.8 [RES] Explanations state which path produced each part of an answer and, for probabilistic parts, the evidence and calibration status. The GUI (CRA-030) shows deterministic and probabilistic results side by side with distinct text labels, not colour alone
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ai/boundary.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ai/boundary.py#L1-L1), [`packages/eoip/neural/lifecycle.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/neural/lifecycle.py#L13-L13), [`scripts/build_master_suite.py:685`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L685-L685)
- tests: `tests/acceptance/test_cra_001_acceptance.py:138`, `tests/ai/test_dual_path.py:1`, `tests/contract/test_asserted_only_queries.py:1`, `tests/semantic/test_proposal_promotion.py:1`
- failing: `tests/acceptance/test_cra_001_acceptance.py::test_cra_001_9_ledger_and_receipts_storage_contract`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

