# EPIC-EOIPPHASE42-UNTR: EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 50 tasks, ~313.0 h, priorities {'P0': 11, 'P1': 32, 'P2': 7}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-AIDLC-004 [P0] AIDLC-004: AI evaluation harness and regression gates

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:2151-2169` (heading) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### AIDLC-004: AI evaluation harness and regression gates

- [ ] `AIDLC-004` **AI evaluation harness and regression gates**
- **Priority**: P0 | **Category**: Evaluate and validate | **Complexity**: High
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: GAP-AI, retrieval evaluation (existing), AI-004
- **Why (evidence from the documents)**: The platform has 64 RAG modes, 35 agent types and 71 query dialects, and CORE-003 must choose among paths, but no requirement measures answer quality. TEST-001..005 cover chaos, load, fuzz, performance and accessibility only. Router, A/B tests and fine-tuning all need an offline quality signal first.
- **Implementation**:
  - Versioned golden datasets; deterministic scorers first (citation accuracy, groundedness against retrieved evidence, exact graph answers), calibrated model-judged scoring only where needed.
  - Metrics: faithfulness, context precision/recall, answer relevance, agent task success, cost and latency.
  - CI gate with thresholds; results stored per commit and per prompt/model version.
- **Suggested paths**: `tests/evals/`, `packages/eoip/evals/`
- **Acceptance criteria**:
  - [ ] `AIDLC-004.1` Golden datasets for at least RAG, graph Q and A and one agent workflow
  - [ ] `AIDLC-004.2` Deterministic scorers implemented
  - [ ] `AIDLC-004.3` CI gate with thresholds
  - [ ] `AIDLC-004.4` Results history and dashboard
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AIDLC-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AIDLC-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] AIDLC-004.1 Golden datasets for at least RAG, graph Q and A and one agent workflow
- [ ] [ ] AIDLC-004.2 Deterministic scorers implemented
- [ ] [ ] AIDLC-004.3 CI gate with thresholds
- [ ] [ ] AIDLC-004.4 Results history and dashboard
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AIDLC-012 [P0] AIDLC-012: Agent tool sandbox and least-privilege capability policy

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:2225-2243` (heading) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### AIDLC-012: Agent tool sandbox and least-privilege capability policy

- [ ] `AIDLC-012` **Agent tool sandbox and least-privilege capability policy**
- **Priority**: P0 | **Category**: Secure and govern | **Complexity**: High
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `CORE-002`
- **Related existing items**: MS-11, NFR-SEC-001, FR-AGENT-004
- **Why (evidence from the documents)**: CORE-002 names "unverified code execution" as a top production failure mode. 35 agent archetypes call tools, and MS-11 needs a sandboxed plugin loader. These should share one sandbox runtime and one capability policy.
- **Implementation**:
  - Sandboxed execution (WASM or container) with CPU, memory, time, filesystem and network limits and an egress allowlist.
  - Per-agent tool allowlists and approval tiers; capability tokens; audit of every call.
  - Shared by plugins (MS-11).
- **Suggested paths**: `packages/eoip/sandbox/`
- **Acceptance criteria**:
  - [ ] `AIDLC-012.1` Sandbox runtime with enforced limits
  - [ ] `AIDLC-012.2` Escape and exhaustion tests
  - [ ] `AIDLC-012.3` Per-agent allowlists
  - [ ] `AIDLC-012.4` Plugin loader uses the same runtime
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AIDLC-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AIDLC-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] AIDLC-012.1 Sandbox runtime with enforced limits
- [ ] [ ] AIDLC-012.2 Escape and exhaustion tests
- [ ] [ ] AIDLC-012.3 Per-agent allowlists
- [ ] [ ] AIDLC-012.4 Plugin loader uses the same runtime
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-001 [P0] SDLC-001: Requirement traceability gate in CI

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1395-1413` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-001: Requirement traceability gate in CI

- [ ] `SDLC-001` **Requirement traceability gate in CI**
- **Priority**: P0 | **Category**: Plan and requirements | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `PRE-001`
- **Related existing items**: KGF BASE-01, BASE-02, BASE-03, CG-GAP-004
- **Why (evidence from the documents)**: The CG audit found 1,199 documentation records with no code or test lead and five documentation-drift gaps; the G-dev audit found most tests untagged. Without an enforced link between requirement, commit and test the drift returns. This programme adds 49 more requirements.
- **Implementation**:
  - Adopt the commit prefix [ID] and the @pytest.mark.req("ID") marker (KGF BASE-02).
  - CI check: every PR names at least one existing requirement ID; every requirement marked done has at least one tagged test; no orphan tests.
  - Emit requirements-test-map.json as a CI artifact and fail on unknown IDs.
- **Suggested paths**: `scripts/traceability_check.py`, `.github/workflows/traceability.yml`
- **Acceptance criteria**:
  - [ ] `SDLC-001.1` CI fails a PR with no valid requirement ID
  - [ ] `SDLC-001.2` CI fails when a done requirement has no tagged test
  - [ ] `SDLC-001.3` Registry and Markdown checkbox state are reconciled by a script
  - [ ] `SDLC-001.4` Check runs in under 30 seconds
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-001.1 CI fails a PR with no valid requirement ID
- [ ] [ ] SDLC-001.2 CI fails when a done requirement has no tagged test
- [ ] [ ] SDLC-001.3 Registry and Markdown checkbox state are reconciled by a script
- [ ] [ ] SDLC-001.4 Check runs in under 30 seconds
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-004 [P0] SDLC-004: Engine auto-registration and wiring contract

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1454-1472` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-004: Engine auto-registration and wiring contract

- [ ] `SDLC-004` **Engine auto-registration and wiring contract**
- **Priority**: P0 | **Category**: Architecture and design | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: CG-GAP-001, KGF H-03
- **Why (evidence from the documents)**: Eight requirements each edit brain_os.py and platform_router.py by hand, and CG-GAP-001 shows the consequence: a router that exists but is not mounted. Hand wiring also makes those two files merge hot spots when several agents or branches work in parallel.
- **Implementation**:
  - An Engine descriptor (name, version, router, health check, telemetry hooks, tenant scope, feature flag) registered by decorator or entry point.
  - The app builds routes, health and telemetry from the registry; no manual edits to brain_os.py or platform_router.py for new engines.
  - Startup self-check lists every router module under packages/eoip and fails if one is neither mounted nor explicitly excluded.
- **Suggested paths**: `packages/eoip/platform/registry.py`
- **Acceptance criteria**:
  - [ ] `SDLC-004.1` Descriptor and registry implemented
  - [ ] `SDLC-004.2` Existing engines migrated or explicitly exempted
  - [ ] `SDLC-004.3` Startup test fails on an unmounted router (would have caught CG-GAP-001)
  - [ ] `SDLC-004.4` New engines add zero lines to brain_os.py/platform_router.py
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-004.1 Descriptor and registry implemented
- [ ] [ ] SDLC-004.2 Existing engines migrated or explicitly exempted
- [ ] [ ] SDLC-004.3 Startup test fails on an unmounted router (would have caught CG-GAP-001)
- [ ] [ ] SDLC-004.4 New engines add zero lines to brainos.py/platformrouter.py
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-005 [P0] SDLC-005: Tenant-scoped engine instances instead of process-wide singletons

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1473-1491` (heading) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-005: Tenant-scoped engine instances instead of process-wide singletons

- [ ] `SDLC-005` **Tenant-scoped engine instances instead of process-wide singletons**
- **Priority**: P1 | **Category**: Architecture and design | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-030`
- **Related existing items**: KGR-G-013, MS-26, tenancy/
- **Why (evidence from the documents)**: Eight requirements mandate a thread-safe singleton get_*_engine(). Budgets, caches, queues, experiments and memory are tenant data. KGR-G-013 and MS-26 require tenant isolation; a singleton holding state across tenants defeats it.
- **Implementation**:
  - Keep singletons for stateless services; give stateful engines a tenant-keyed factory behind a small dependency-injection container.
  - get_*_engine(tenant) signature with a default-tenant shim for existing callers.
  - Document which engines are stateless and which are tenant-scoped.
- **Suggested paths**: `packages/eoip/platform/container.py`
- **Acceptance criteria**:
  - [ ] `SDLC-005.1` Container and factory pattern exist
  - [ ] `SDLC-005.2` Stateful Phase 4 engines are tenant-keyed
  - [ ] `SDLC-005.3` Concurrency test: two tenants cannot observe each other
  - [ ] `SDLC-005.4` Migration notes for existing singletons
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-005.1 Container and factory pattern exist
- [ ] [ ] SDLC-005.2 Stateful Phase 4 engines are tenant-keyed
- [ ] [ ] SDLC-005.3 Concurrency test: two tenants cannot observe each other
- [ ] [ ] SDLC-005.4 Migration notes for existing singletons
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-015 [P0] SDLC-015: Governance for the AI coding agent itself

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1662-1680` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 7.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-015: Governance for the AI coding agent itself

- [ ] `SDLC-015` **Governance for the AI coding agent itself**
- **Priority**: P0 | **Category**: Build and code quality | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-001`
- **Related existing items**: KGF Section 4.5 rules
- **Why (evidence from the documents)**: Around 565 tasks will be executed by an AI developer agent. The backlog states rules in prose (never rewrite historical audits, never lower a gate) but nothing enforces them, and an agent can quietly weaken tests or thresholds to turn a box green.
- **Implementation**:
  - CODEOWNERS and protected paths (gate thresholds, audit/ history, security tests, CI config) requiring human review.
  - PR policy: size limit, linked requirement ID, evidence, passing suite; a second agent or human reviews P0 and security-sensitive changes.
  - Budgets per task (time, tokens), a change log of agent actions, secrets scan, and a kill switch.
- **Suggested paths**: `.github/CODEOWNERS`, `.github/pull_request_template.md`
- **Acceptance criteria**:
  - [ ] `SDLC-015.1` Protected-path rules enforced in CI
  - [ ] `SDLC-015.2` PR template with evidence checklist
  - [ ] `SDLC-015.3` Second-review rule for P0/security paths
  - [ ] `SDLC-015.4` Agent change log stored and queryable
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-015' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-015') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-015.1 Protected-path rules enforced in CI
- [ ] [ ] SDLC-015.2 PR template with evidence checklist
- [ ] [ ] SDLC-015.3 Second-review rule for P0/security paths
- [ ] [ ] SDLC-015.4 Agent change log stored and queryable
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SDLC-021 [P0] SDLC-021: Continuous security testing pipeline

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1771-1788` (heading) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-021: Continuous security testing pipeline

- [ ] `SDLC-021` **Continuous security testing pipeline**
- **Priority**: P1 | **Category**: Verify and test | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: KGF S-05, REL-11, NFR-SEC-*
- **Why (evidence from the documents)**: KGF S-05 is a single OWASP audit with dependency and secrets scanning. TEST-003 fuzzes only serialization and queries. Security regressions need to be caught per PR and nightly.
- **Implementation**:
  - SAST on every PR; dependency and container scanning; secrets detection; DAST against the compose stack nightly.
  - Findings feed the registry with severity and SLA.
- **Suggested paths**: `.github/workflows/security.yml`
- **Acceptance criteria**:
  - [ ] `SDLC-021.1` SAST, dependency, container and secrets scans in CI
  - [ ] `SDLC-021.2` Nightly DAST
  - [ ] `SDLC-021.3` Severity-based SLA
  - [ ] `SDLC-021.4` Zero critical findings gate
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-021' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-021') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-021.1 SAST, dependency, container and secrets scans in CI
- [ ] [ ] SDLC-021.2 Nightly DAST
- [ ] [ ] SDLC-021.3 Severity-based SLA
- [ ] [ ] SDLC-021.4 Zero critical findings gate
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-023 [P0] SDLC-023: Kubernetes production profile and secrets management

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1810-1828` (heading) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-023: Kubernetes production profile and secrets management

- [ ] `SDLC-023` **Kubernetes production profile and secrets management**
- **Priority**: P1 | **Category**: Release and deploy | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `INFRA-003`
- **Related existing items**: NFR-SEC-006, GAP-HA, REL-10
- **Why (evidence from the documents)**: A Helm chart exists, Redis is in it but unwired, container hardening is partial (NFR-SEC-006) and the release gate needs a real HA environment (REL-10). Production defaults are not specified.
- **Implementation**:
  - Resource requests/limits, HPA, PodDisruptionBudgets, NetworkPolicies, probes, security contexts.
  - Secrets via an external store or sealed secrets; no secrets in values files.
  - Environment overlays for staging and production.
- **Suggested paths**: `deploy/helm/`
- **Acceptance criteria**:
  - [ ] `SDLC-023.1` Hardened chart values with tests (helm lint, policy checks)
  - [ ] `SDLC-023.2` NetworkPolicies default-deny
  - [ ] `SDLC-023.3` Secrets never in plain values
  - [ ] `SDLC-023.4` HA run documented
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-023' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-023') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-023.1 Hardened chart values with tests (helm lint, policy checks)
- [ ] [ ] SDLC-023.2 NetworkPolicies default-deny
- [ ] [ ] SDLC-023.3 Secrets never in plain values
- [ ] [ ] SDLC-023.4 HA run documented
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-028 [P0] SDLC-028: Data lifecycle: retention and right-to-erasure across all derived stores

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1905-1923` (heading) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-028: Data lifecycle: retention and right-to-erasure across all derived stores

- [ ] `SDLC-028` **Data lifecycle: retention and right-to-erasure across all derived stores**
- **Priority**: P0 | **Category**: Operate and maintain | **Complexity**: High
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-029`
- **Related existing items**: NFR-PRIV-001, COMPLY-002, privacy/
- **Why (evidence from the documents)**: Phase 4 adds at least nine places personal data can be copied (L2 cache, embeddings, distilled packages, persisted messages, experiment artifacts, memory graphs, pseudonym vault, backups, logs). The privacy module handles DSAR only, COMPLY-001 promises GDPR, and immutable ledgers (G2-JOURNAL, XAI Merkle tree) conflict with erasure.
- **Implementation**:
  - Data-map of every derived store; erasure orchestrator that cascades from the graph to each store.
  - Crypto-shredding with per-subject or per-tenant keys for immutable logs and backups; erasure re-applied after restore.
  - Retention policies, archival tiers, legal hold.
- **Suggested paths**: `packages/eoip/privacy/lifecycle.py`
- **Acceptance criteria**:
  - [ ] `SDLC-028.1` Data map covers all stores
  - [ ] `SDLC-028.2` Erasure test removes a subject from graph, caches, vector index, packages, logs and backups
  - [ ] `SDLC-028.3` Retention policy engine
  - [ ] `SDLC-028.4` Legal-hold override
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-028' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-028') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-028.1 Data map covers all stores
- [ ] [ ] SDLC-028.2 Erasure test removes a subject from graph, caches, vector index, packages, logs and backups
- [ ] [ ] SDLC-028.3 Retention policy engine
- [ ] [ ] SDLC-028.4 Legal-hold override
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-029 [P0] SDLC-029: Key management and envelope encryption layer

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1924-1941` (heading) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-029: Key management and envelope encryption layer

- [ ] `SDLC-029` **Key management and envelope encryption layer**
- **Priority**: P1 | **Category**: Operate and maintain | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: INFRA-007, COMPLY-002, NFR-SEC-002
- **Why (evidence from the documents)**: INFRA-007 (encryption at rest), COMPLY-002 (reversible tokens), AI-005 (artifacts), MULTI-002 and audit chains each need keys and would otherwise invent their own cryptography.
- **Implementation**:
  - KMS abstraction with local and external backends (including HSM); envelope encryption; rotation; per-tenant keys.
  - Used by backups, vault, caches, artifacts and ledgers.
- **Suggested paths**: `packages/eoip/kms/`
- **Acceptance criteria**:
  - [ ] `SDLC-029.1` Interface with local backend and one external adapter
  - [ ] `SDLC-029.2` Rotation test with no downtime
  - [ ] `SDLC-029.3` Per-tenant keys
  - [ ] `SDLC-029.4` Consumers migrated
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-029' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-029') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-029.1 Interface with local backend and one external adapter
- [ ] [ ] SDLC-029.2 Rotation test with no downtime
- [ ] [ ] SDLC-029.3 Per-tenant keys
- [ ] [ ] SDLC-029.4 Consumers migrated
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-030 [P0] SDLC-030: Tenant-isolation conformance suite

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1942-1959` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-030: Tenant-isolation conformance suite

- [ ] `SDLC-030` **Tenant-isolation conformance suite**
- **Priority**: P0 | **Category**: Operate and maintain | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-005`
- **Related existing items**: KGR-G-013, MS-26
- **Why (evidence from the documents)**: KGR-G-013 and MS-26 require isolation, and Phase 4 adds many stateful components (cache keys, bus topics, budgets, experiments, memory, vector indexes, logs). Isolation must be proven by tests that every new engine passes.
- **Implementation**:
  - Reusable suite: two tenants, same inputs, assert no cross-visibility in data, caches, queues, logs, metrics, vector search and exports.
  - Mandatory for every engine descriptor (SDLC-004).
- **Suggested paths**: `tests/tenancy/`
- **Acceptance criteria**:
  - [ ] `SDLC-030.1` Suite runs for all Phase 4 stateful engines
  - [ ] `SDLC-030.2` Fails on a deliberately leaky fixture
  - [ ] `SDLC-030.3` Part of the Definition of Done
  - [ ] `SDLC-030.4` Reports per engine
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-030' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-030') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-030.1 Suite runs for all Phase 4 stateful engines
- [ ] [ ] SDLC-030.2 Fails on a deliberately leaky fixture
- [ ] [ ] SDLC-030.4 Reports per engine
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AIDLC-001 [P1] AIDLC-001: Dataset and knowledge-base versioning with lineage

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:2038-2056` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### AIDLC-001: Dataset and knowledge-base versioning with lineage

- [ ] `AIDLC-001` **Dataset and knowledge-base versioning with lineage**
- **Priority**: P1 | **Category**: Data and knowledge | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AI-006`, `AGENT-002`
- **Related existing items**: GAP-AI, G2-ARCH-013, AI-006
- **Why (evidence from the documents)**: AI-006 versions embeddings, but not the chunks, corpora or extraction runs they came from. Evidence-addressable answers (GAP-AI) and replayability (G2-ARCH-013) need lineage from source to chunk to embedding to answer.
- **Implementation**:
  - Content-addressed corpus snapshots; lineage records source, chunk, extractor version, embedding model and index.
  - Emit OpenLineage-compatible events from ingestion and extraction.
  - Restore a snapshot and reproduce an answer.
- **Suggested paths**: `packages/eoip/lineage/`
- **Acceptance criteria**:
  - [ ] `AIDLC-001.1` Corpus snapshots with hashes
  - [ ] `AIDLC-001.2` Lineage queryable from an answer back to source
  - [ ] `AIDLC-001.3` OpenLineage events emitted
  - [ ] `AIDLC-001.4` Reproduce a past answer in a test
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AIDLC-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AIDLC-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] AIDLC-001.1 Corpus snapshots with hashes
- [ ] [ ] AIDLC-001.2 Lineage queryable from an answer back to source
- [ ] [ ] AIDLC-001.3 OpenLineage events emitted
- [ ] [ ] AIDLC-001.4 Reproduce a past answer in a test
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AIDLC-002 [P1] AIDLC-002: Re-embedding and blue/green vector index migration

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:2057-2074` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### AIDLC-002: Re-embedding and blue/green vector index migration

- [ ] `AIDLC-002` **Re-embedding and blue/green vector index migration**
- **Priority**: P1 | **Category**: Data and knowledge | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AI-006`, `AIDLC-004`
- **Related existing items**: KGF H-02, K-09, AI-006
- **Why (evidence from the documents)**: H-02 replaces hash embeddings with real ones and AI-006 detects drift, but nothing says how to move an existing vector index to a new embedding model without downtime or quality loss.
- **Implementation**:
  - Dual-write and dual-read, backfill workers, quality comparison before cutover, rollback.
  - Embedding version required on every query path.
- **Suggested paths**: `packages/eoip/embeddings/migration.py`
- **Acceptance criteria**:
  - [ ] `AIDLC-002.1` Blue/green index switch
  - [ ] `AIDLC-002.2` Backfill resumable
  - [ ] `AIDLC-002.3` Quality comparison report before cutover
  - [ ] `AIDLC-002.4` Rollback tested
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AIDLC-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AIDLC-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] AIDLC-002.1 Blue/green index switch
- [ ] [ ] AIDLC-002.2 Backfill resumable
- [ ] [ ] AIDLC-002.3 Quality comparison report before cutover
- [ ] [ ] AIDLC-002.4 Rollback tested
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AIDLC-003 [P1] AIDLC-003: Knowledge quality scoring and extraction accuracy benchmarks

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:2075-2093` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### AIDLC-003: Knowledge quality scoring and extraction accuracy benchmarks

- [ ] `AIDLC-003` **Knowledge quality scoring and extraction accuracy benchmarks**
- **Priority**: P1 | **Category**: Data and knowledge | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AGENT-002`, `AI-003`
- **Related existing items**: KGF MS-24, GAP-TRUTH-*
- **Why (evidence from the documents)**: AGENT-002, AI-002 and AI-003 have no precision/recall target; MS-24 will show graph health but not extraction accuracy; entity resolution quality is unmeasured; NLP is multilingual in scope (AI-002, UI-002).
- **Implementation**:
  - Labelled benchmark corpora per language and domain pack; metrics for entity, relation and resolution quality.
  - Per-source reliability scores feeding truth resolution.
  - Quality dashboard in the health view.
- **Suggested paths**: `tests/benchmarks/extraction/`
- **Acceptance criteria**:
  - [ ] `AIDLC-003.1` Benchmarks and targets recorded for AGENT-002, AI-002, AI-003
  - [ ] `AIDLC-003.2` Resolution quality reported
  - [ ] `AIDLC-003.3` Source reliability scores
  - [ ] `AIDLC-003.4` Dashboard
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AIDLC-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AIDLC-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] AIDLC-003.1 Benchmarks and targets recorded for AGENT-002, AI-002, AI-003
- [ ] [ ] AIDLC-003.2 Resolution quality reported
- [ ] [ ] AIDLC-003.3 Source reliability scores
- [ ] [ ] AIDLC-003.4 Dashboard
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AIDLC-005 [P1] AIDLC-005: Agent trajectory recording and deterministic replay

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:2170-2187` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 9.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### AIDLC-005: Agent trajectory recording and deterministic replay

- [ ] `AIDLC-005` **Agent trajectory recording and deterministic replay**
- **Priority**: P1 | **Category**: Evaluate and validate | **Complexity**: High
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AIDLC-004`, `SDLC-028`
- **Related existing items**: G2-ARCH-013, G2-EKAF-013, AGENT-001
- **Why (evidence from the documents)**: Replayability is a stated principle (G2-ARCH-013). Recorded trajectories enable regression tests for agents, counterfactual replay under new policies (verification, router) and evidence for audits.
- **Implementation**:
  - Record tool calls, retrieved evidence and model outputs per step; replay with recorded outputs in CI.
  - Counterfactual replay: re-run with a different policy and diff outcomes.
- **Suggested paths**: `packages/eoip/agents/replay.py`
- **Acceptance criteria**:
  - [ ] `AIDLC-005.1` Recorder and replayer
  - [ ] `AIDLC-005.2` Replay-based regression test for two agents
  - [ ] `AIDLC-005.3` Counterfactual diff report
  - [ ] `AIDLC-005.4` Recordings follow retention and erasure policy
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AIDLC-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AIDLC-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Record tool calls, retrieved evidence and model outputs per step; replay with recorded outputs in CI
- [ ] Counterfactual replay: re-run with a different policy and diff outcomes
- [ ] [ ] AIDLC-005.1 Recorder and replayer
- [ ] [ ] AIDLC-005.2 Replay-based regression test for two agents
- [ ] [ ] AIDLC-005.3 Counterfactual diff report
- [ ] [ ] AIDLC-005.4 Recordings follow retention and erasure policy
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AIDLC-006 [P1] AIDLC-006: Router and guardrail calibration with shadow mode

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:2188-2204` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### AIDLC-006: Router and guardrail calibration with shadow mode

- [ ] `AIDLC-006` **Router and guardrail calibration with shadow mode**
- **Priority**: P1 | **Category**: Evaluate and validate | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `CORE-002`, `CORE-003`, `AIDLC-004`
- **Why (evidence from the documents)**: A router that sends hard questions down cheap paths, or a guardrail that blocks valid output, degrades quality silently. Both CORE-002 and CORE-003 need calibration before enforcement.
- **Implementation**:
  - Labelled intent and verification sets; confusion matrices; cost-of-error weighting.
  - Shadow mode logs decisions without acting; promote to enforce when thresholds hold.
- **Suggested paths**: `tests/evals/routing/`
- **Acceptance criteria**:
  - [ ] `AIDLC-006.1` Labelled sets and confusion matrices
  - [ ] `AIDLC-006.2` Shadow mode in both engines
  - [ ] `AIDLC-006.3` Promotion threshold documented
  - [ ] `AIDLC-006.4` Drift alerts after promotion
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AIDLC-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AIDLC-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Shadow mode logs decisions without acting; promote to enforce when thresholds hold
- [ ] [ ] AIDLC-006.1 Labelled sets and confusion matrices
- [ ] [ ] AIDLC-006.2 Shadow mode in both engines
- [ ] [ ] AIDLC-006.3 Promotion threshold documented
- [ ] [ ] AIDLC-006.4 Drift alerts after promotion
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AIDLC-007 [P1] AIDLC-007: Prompt, policy and template registry

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:2096-2113` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 9.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### AIDLC-007: Prompt, policy and template registry

- [ ] `AIDLC-007` **Prompt, policy and template registry**
- **Priority**: P1 | **Category**: Model, prompt and agent development | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AIDLC-004`, `SDLC-006`
- **Related existing items**: AI-005, GAP-RULE
- **Why (evidence from the documents)**: AI-005 tracks prompt iterations as experiments, and verification rules, routing policies and GAP-RULE inference policies are all versioned text. None is a deployable, tested, promotable artifact.
- **Implementation**:
  - Versioned registry with diffs, owners, evaluation results, environment promotion (dev, staging, prod) and rollback.
  - Signed artifacts; flag-controlled rollout.
- **Suggested paths**: `packages/eoip/registry/prompts.py`
- **Acceptance criteria**:
  - [ ] `AIDLC-007.1` Registry with versions and promotion
  - [ ] `AIDLC-007.2` Promotion blocked unless evaluation passes
  - [ ] `AIDLC-007.3` Rollback tested
  - [ ] `AIDLC-007.4` Prompts and policies loaded from the registry
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AIDLC-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AIDLC-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Versioned registry with diffs, owners, evaluation results, environment promotion (dev, staging, prod) and rollback
- [ ] Signed artifacts; flag-controlled rollout
- [ ] [ ] AIDLC-007.1 Registry with versions and promotion
- [ ] [ ] AIDLC-007.2 Promotion blocked unless evaluation passes
- [ ] [ ] AIDLC-007.3 Rollback tested
- [ ] [ ] AIDLC-007.4 Prompts and policies loaded from the registry
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AIDLC-008 [P1] AIDLC-008: Model gateway consolidation

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:2114-2131` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### AIDLC-008: Model gateway consolidation

- [ ] `AIDLC-008` **Model gateway consolidation**
- **Priority**: P1 | **Category**: Model, prompt and agent development | **Complexity**: High
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `CORE-006`, `CORE-003`
- **Related existing items**: models/provider.py, model_management/, cost_optimization/, MS-27
- **Why (evidence from the documents)**: Model access is spread across models/provider.py, model_management, cost_optimization and the new routing, budget and A/B work (CORE-003, CORE-006, AI-004). Failover, rate limits, semantic response caching, prompt redaction and per-tenant quotas belong in one place.
- **Implementation**:
  - A single gateway: provider abstraction, failover, retries, rate limits, semantic cache, PII redaction on prompts, per-tenant keys and quotas, usage metering.
  - Consolidate; do not add a fourth path.
- **Suggested paths**: `packages/eoip/gateway/`
- **Acceptance criteria**:
  - [ ] `AIDLC-008.1` One call path for all model use
  - [ ] `AIDLC-008.2` Failover test
  - [ ] `AIDLC-008.3` Per-tenant quotas enforced
  - [ ] `AIDLC-008.4` Usage metering feeds CORE-006 and MS-27
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AIDLC-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AIDLC-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] AIDLC-008.1 One call path for all model use
- [ ] [ ] AIDLC-008.2 Failover test
- [ ] [ ] AIDLC-008.3 Per-tenant quotas enforced
- [ ] [ ] AIDLC-008.4 Usage metering feeds CORE-006 and MS-27
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AIDLC-009 [P1] AIDLC-009: AI quality monitoring and user feedback loop

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:2301-2318` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### AIDLC-009: AI quality monitoring and user feedback loop

- [ ] `AIDLC-009` **AI quality monitoring and user feedback loop**
- **Priority**: P1 | **Category**: Deploy and monitor AI | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AIDLC-004`, `SDLC-008`
- **Related existing items**: brain/learning_engine.py, AI-004, CORE-003
- **Why (evidence from the documents)**: The learning engine and drift detectors exist, but no requirement captures user corrections or monitors answer quality in production. Without feedback, A/B tests (AI-004) and routing feedback (CORE-003) lack ground truth.
- **Implementation**:
  - Feedback API and UI (helpful, wrong, citation disputed, correction); sampled online evaluation; drift and quality monitors.
  - Low-quality cases open work items (SDLC-008) and become evaluation cases (AIDLC-004).
- **Suggested paths**: `packages/eoip/feedback/`
- **Acceptance criteria**:
  - [ ] `AIDLC-009.1` Feedback capture end to end
  - [ ] `AIDLC-009.2` Online sampled evaluation
  - [ ] `AIDLC-009.3` Quality drift alert
  - [ ] `AIDLC-009.4` Feedback converts to eval cases
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AIDLC-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AIDLC-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] AIDLC-009.1 Feedback capture end to end
- [ ] [ ] AIDLC-009.2 Online sampled evaluation
- [ ] [ ] AIDLC-009.3 Quality drift alert
- [ ] [ ] AIDLC-009.4 Feedback converts to eval cases
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AIDLC-010 [P1] AIDLC-010: Model fine-tuning lifecycle pipeline

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:2132-2148` (heading) · **Type:** AI · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### AIDLC-010: Model fine-tuning lifecycle pipeline

- [ ] `AIDLC-010` **Model fine-tuning lifecycle pipeline**
- **Priority**: P2 | **Category**: Model, prompt and agent development | **Complexity**: High
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AIDLC-004`, `AI-005`
- **Related existing items**: MS-15, AI-004, AI-005
- **Why (evidence from the documents)**: MS-15 (LOM fine-tuning), self_llm and AI-004/005 will train and ship own models. Dataset consent and licensing, PII scrubbing, run tracking, evaluation gates, promotion and model cards must be one controlled path.
- **Implementation**:
  - Curated dataset with consent/license checks and PII scrub; training runs tracked (AI-005); evaluation gate; registry promotion and rollback; model card.
- **Suggested paths**: `packages/eoip/mlops/finetune.py`
- **Acceptance criteria**:
  - [ ] `AIDLC-010.1` Pipeline from dataset to registry
  - [ ] `AIDLC-010.2` Evaluation gate blocks regressions
  - [ ] `AIDLC-010.3` Model card generated
  - [ ] `AIDLC-010.4` Rollback tested
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AIDLC-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AIDLC-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] AIDLC-010.1 Pipeline from dataset to registry
- [ ] [ ] AIDLC-010.2 Evaluation gate blocks regressions
- [ ] [ ] AIDLC-010.3 Model card generated
- [ ] [ ] AIDLC-010.4 Rollback tested
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AIDLC-011 [P1] AIDLC-011: Continuous AI red-teaming harness

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:2207-2224` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### AIDLC-011: Continuous AI red-teaming harness

- [ ] `AIDLC-011` **Continuous AI red-teaming harness**
- **Priority**: P1 | **Category**: Secure and govern | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `CORE-002`, `SDLC-003`
- **Related existing items**: NFR-SEC-004, G2-IMMUNE-*, MS-19, MS-21
- **Why (evidence from the documents)**: The platform ingests untrusted content from Jira, Confluence, the web and files (G2-SEC-CRAWL, G2-SRC-WEB), which makes indirect prompt injection a first-order risk. NFR-SEC-004 is partial and G2-IMMUNE has 12 open gaps.
- **Implementation**:
  - Attack corpora: direct and indirect injection, tool abuse, exfiltration via retrieval, memory poisoning, jailbreak and multi-turn attacks; mapped to OWASP LLM and Agentic lists.
  - Nightly run against the verification and guardrail stack; regressions block release.
- **Suggested paths**: `tests/redteam/`
- **Acceptance criteria**:
  - [ ] `AIDLC-011.1` Attack corpus and runner
  - [ ] `AIDLC-011.2` Mapped to OWASP categories
  - [ ] `AIDLC-011.3` Nightly CI run
  - [ ] `AIDLC-011.4` Failing attack creates a tracked finding
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AIDLC-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AIDLC-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] AIDLC-011.1 Attack corpus and runner
- [ ] [ ] AIDLC-011.2 Mapped to OWASP categories
- [ ] [ ] AIDLC-011.3 Nightly CI run
- [ ] [ ] AIDLC-011.4 Failing attack creates a tracked finding
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AIDLC-013 [P1] AIDLC-013: Agent and workload identity, plus SCIM

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:2244-2261` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### AIDLC-013: Agent and workload identity, plus SCIM

- [ ] `AIDLC-013` **Agent and workload identity, plus SCIM**
- **Priority**: P1 | **Category**: Secure and govern | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `INFRA-002`
- **Related existing items**: INFRA-002, H-04, GAP-SEC-008..012
- **Why (evidence from the documents)**: INFRA-002 covers human SSO only. Agents and services act on behalf of users and need their own scoped, short-lived identities and an audit trail that says which agent acted for whom.
- **Implementation**:
  - Workload identities with short-lived scoped credentials; on-behalf-of delegation; per-agent audit principal.
  - SCIM provisioning for human lifecycle.
- **Suggested paths**: `packages/eoip/authz/workload.py`
- **Acceptance criteria**:
  - [ ] `AIDLC-013.1` Agent credentials are scoped and expire
  - [ ] `AIDLC-013.2` Audit shows agent and delegating user
  - [ ] `AIDLC-013.3` SCIM create/update/deactivate tested
  - [ ] `AIDLC-013.4` Revocation takes effect immediately
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AIDLC-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AIDLC-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] AIDLC-013.1 Agent credentials are scoped and expire
- [ ] [ ] AIDLC-013.2 Audit shows agent and delegating user
- [ ] [ ] AIDLC-013.3 SCIM create/update/deactivate tested
- [ ] [ ] AIDLC-013.4 Revocation takes effect immediately
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AIDLC-014 [P1] AIDLC-014: AI governance pack

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:2262-2280` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### AIDLC-014: AI governance pack

- [ ] `AIDLC-014` **AI governance pack**
- **Priority**: P1 | **Category**: Secure and govern | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `COMPLY-003`, `AIDLC-016`
- **Related existing items**: COMPLY-001, COMPLY-003, audit/xai_ledger.py
- **Why (evidence from the documents)**: COMPLY-001 covers GDPR, SOX and HIPAA. Customers in BFSI and healthcare (two of the eight domain packs) also face AI-specific rules and standards such as the EU AI Act, NIST AI RMF and ISO/IEC 42001.
- **Implementation**:
  - AI system inventory and risk classification; model and agent cards; impact assessments; human-oversight records.
  - Control mapping to the named frameworks feeding COMPLY-003.
  - Autonomy policy catalog (see AIDLC-016).
- **Suggested paths**: `docs/ai-governance/`
- **Acceptance criteria**:
  - [ ] `AIDLC-014.1` Inventory and risk classes for all engines and agents
  - [ ] `AIDLC-014.2` Model and agent card template filled for core models
  - [ ] `AIDLC-014.3` Mapping to EU AI Act, NIST AI RMF, ISO/IEC 42001
  - [ ] `AIDLC-014.4` Impact assessment template
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AIDLC-014' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AIDLC-014') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] AIDLC-014.1 Inventory and risk classes for all engines and agents
- [ ] [ ] AIDLC-014.2 Model and agent card template filled for core models
- [ ] [ ] AIDLC-014.3 Mapping to EU AI Act, NIST AI RMF, ISO/IEC 42001
- [ ] [ ] AIDLC-014.4 Impact assessment template
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AIDLC-015 [P1] AIDLC-015: Evidence and explanation UX

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:2321-2338` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### AIDLC-015: Evidence and explanation UX

- [ ] `AIDLC-015` **Evidence and explanation UX**
- **Priority**: P1 | **Category**: Human experience | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `UI-001`, `AI-001`
- **Related existing items**: GAP-AI, KGR-G-019, UI-04
- **Why (evidence from the documents)**: The backend promises evidence-addressable answers (GAP-AI), calibrated abstention (KGR-G-019), XAI (AI-001, the XAI ledger) and uncertainty (AI-007), but the UI requirements list none of the screens users need to see them.
- **Implementation**:
  - Citation drill-down to graph nodes, paths and source records; confidence and uncertainty display; why-this-answer view; clear abstain state; feedback controls.
  - Shared component set (UI-001), accessible by default.
- **Suggested paths**: `apps/web/src/evidence/`
- **Acceptance criteria**:
  - [ ] `AIDLC-015.1` Citation drill-down component
  - [ ] `AIDLC-015.2` Confidence and abstain states
  - [ ] `AIDLC-015.3` Why-this-answer panel
  - [ ] `AIDLC-015.4` Accessibility checks pass
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AIDLC-015' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AIDLC-015') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] AIDLC-015.1 Citation drill-down component
- [ ] [ ] AIDLC-015.2 Confidence and abstain states
- [ ] [ ] AIDLC-015.3 Why-this-answer panel
- [ ] [ ] AIDLC-015.4 Accessibility checks pass
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AIDLC-016 [P1] AIDLC-016: Autonomy policy catalog

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:2281-2298` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### AIDLC-016: Autonomy policy catalog

- [ ] `AIDLC-016` **Autonomy policy catalog**
- **Priority**: P1 | **Category**: Secure and govern | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AGENT-001`, `CORE-002`
- **Related existing items**: AGENT-001, FR-AGENT-004
- **Why (evidence from the documents)**: AGENT-001 escalates between autonomy levels across 14 control loops and 23 execution loops, but the allowed level per loop, risk tier and tenant is nowhere defined. Human-oversight rules also require it.
- **Implementation**:
  - Autonomy ladder (for example advise, act with approval, act and report, autonomous) per loop and risk tier.
  - Tenant-level policy overrides; enforced by the loop runtime and verification gate.
- **Suggested paths**: `packages/eoip/loops/autonomy.py`
- **Acceptance criteria**:
  - [ ] `AIDLC-016.1` Catalog covers all loops
  - [ ] `AIDLC-016.2` Enforcement test: a loop cannot exceed its tier
  - [ ] `AIDLC-016.3` Tenant override audited
  - [ ] `AIDLC-016.4` Linked from governance pack
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AIDLC-016' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AIDLC-016') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] AIDLC-016.1 Catalog covers all loops
- [ ] [ ] AIDLC-016.2 Enforcement test: a loop cannot exceed its tier
- [ ] [ ] AIDLC-016.3 Tenant override audited
- [ ] [ ] AIDLC-016.4 Linked from governance pack
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-003 [P1] SDLC-003: Threat model and abuse-case library per engine

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1433-1451` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 9.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-003: Threat model and abuse-case library per engine

- [ ] `SDLC-003` **Threat model and abuse-case library per engine**
- **Priority**: P1 | **Category**: Plan and requirements | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AIDLC-011`
- **Related existing items**: KGF NFR-SEC-*, G2-IMMUNE-*
- **Why (evidence from the documents)**: Many new surfaces: a message bus (AGENT-003), federated pushdown to external databases (GRAPH-001), SSO (INFRA-002), a pseudonym vault (COMPLY-002), cache keys (INFRA-001), a router that can skip checks (CORE-003). Security items in the KGF backlog are mostly verification after the fact.
- **Implementation**:
  - One threat model per new engine using STRIDE plus the OWASP LLM and Agentic top-10 lists; stored under docs/threat-models/.
  - Design gate: an engine is not started until its threat model is reviewed.
  - Abuse-case tests are derived from each threat model.
- **Suggested paths**: `docs/threat-models/`
- **Acceptance criteria**:
  - [ ] `SDLC-003.1` Template and review checklist
  - [ ] `SDLC-003.2` Threat models exist for CORE-002, CORE-003, GRAPH-001, AGENT-003, INFRA-002, COMPLY-002
  - [ ] `SDLC-003.3` Each threat has a mitigation requirement or an accepted-risk entry
  - [ ] `SDLC-003.4` Abuse-case tests exist for the top threats
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] One threat model per new engine using STRIDE plus the OWASP LLM and Agentic top-10 lists; stored under docs/threat-models/
- [ ] Design gate: an engine is not started until its threat model is reviewed
- [ ] Abuse-case tests are derived from each threat model
- [ ] [ ] SDLC-003.1 Template and review checklist
- [ ] [ ] SDLC-003.2 Threat models exist for CORE-002, CORE-003, GRAPH-001, AGENT-003, INFRA-002, COMPLY-002
- [ ] [ ] SDLC-003.3 Each threat has a mitigation requirement or an accepted-risk entry
- [ ] [ ] SDLC-003.4 Abuse-case tests exist for the top threats
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-006 [P1] SDLC-006: Feature flags and kill switches

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1492-1510` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-006: Feature flags and kill switches

- [ ] `SDLC-006` **Feature flags and kill switches**
- **Priority**: P1 | **Category**: Architecture and design | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-004`
- **Related existing items**: INFRA-003, AI-004
- **Why (evidence from the documents)**: CORE-003 can short-circuit 60-70% of queries, CORE-002 can block outputs, and AI-004 canaries models. INFRA-003 only covers deploy-level canaries. A runtime switch is needed to turn an engine off or to enable it per tenant without redeploying, including in air-gapped sites.
- **Implementation**:
  - Local, signed flag store with per-engine, per-tenant and percentage rollout; no external SaaS.
  - Every engine descriptor (SDLC-004) declares its kill switch; flag changes are audited.
  - Default-off for behaviour-changing engines until shadow evaluation passes.
- **Suggested paths**: `packages/eoip/flags/`
- **Acceptance criteria**:
  - [ ] `SDLC-006.1` Flag service with audit trail
  - [ ] `SDLC-006.2` Kill switch tested for CORE-002, CORE-003 and INFRA-001
  - [ ] `SDLC-006.3` Flags evaluated in under 1 ms
  - [ ] `SDLC-006.4` Flag state is exported in backups
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-006.1 Flag service with audit trail
- [ ] [ ] SDLC-006.2 Kill switch tested for CORE-002, CORE-003 and INFRA-001
- [ ] [ ] SDLC-006.3 Flags evaluated in under 1 ms
- [ ] [ ] SDLC-006.4 Flag state is exported in backups
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-007 [P1] SDLC-007: Schema and data migration framework

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1511-1529` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-007: Schema and data migration framework

- [ ] `SDLC-007` **Schema and data migration framework**
- **Priority**: P1 | **Category**: Architecture and design | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `INFRA-003`
- **Related existing items**: KGF GAP-GITOPS-006, GAP-GITOPS-007
- **Why (evidence from the documents)**: KGF GAP-GITOPS-006/007 plan ontology migrations only. Phase 4 adds durable formats: message bus (AGENT-003), experiment store (AI-005), embedding registry (AI-006), knowledge packages (GRAPH-003), temporal index (GRAPH-005), L2 cache, and the CORE-001 wire formats.
- **Implementation**:
  - Versioned, ordered, reversible migrations with dry-run, for graph schema, vector index metadata, queues and registries.
  - Compatibility windows: N and N-1 readers; format version headers.
  - Migration status endpoint and CI test that upgrades from the previous release.
- **Suggested paths**: `packages/eoip/migrations/`
- **Acceptance criteria**:
  - [ ] `SDLC-007.1` Migration runner with dry-run and rollback
  - [ ] `SDLC-007.2` Each new durable store ships with a migration
  - [ ] `SDLC-007.3` Upgrade test from the previous tagged release passes
  - [ ] `SDLC-007.4` Migrations run in INFRA-003 deploy ordering
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-007.1 Migration runner with dry-run and rollback
- [ ] [ ] SDLC-007.2 Each new durable store ships with a migration
- [ ] [ ] SDLC-007.3 Upgrade test from the previous tagged release passes
- [ ] [ ] SDLC-007.4 Migrations run in INFRA-003 deploy ordering
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-008 [P1] SDLC-008: Human-in-the-loop work queue and approvals inbox

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1530-1548` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-008: Human-in-the-loop work queue and approvals inbox

- [ ] `SDLC-008` **Human-in-the-loop work queue and approvals inbox**
- **Priority**: P1 | **Category**: Architecture and design | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: AGENT-001, COMPLY-001, KGF GAP-TRUTH-008, GAP-GOV
- **Why (evidence from the documents)**: AGENT-001 hands off to humans, COMPLY-001 produces remediation, KGF GAP-TRUTH-008 needs human adjudication, GAP-GOV needs stewardship review, and loops have approval gates. Each mentions people; none defines the queue, assignment, SLA, escalation or notification.
- **Implementation**:
  - One work-item model (type, subject, evidence links, assignee/role, SLA, status, decision) with an inbox UI and API.
  - Escalation and delegation rules; notification channels (email, Slack/Teams webhook).
  - Every decision is audited and fed back to the producing engine.
- **Suggested paths**: `packages/eoip/workqueue/`, `apps/web/src/inbox/`
- **Acceptance criteria**:
  - [ ] `SDLC-008.1` Work-item API and inbox UI
  - [ ] `SDLC-008.2` AGENT-001, COMPLY-001, GAP-TRUTH-008 and low-confidence triples (AI-003) create work items
  - [ ] `SDLC-008.3` SLA breach escalates
  - [ ] `SDLC-008.4` Decisions are in the audit ledger
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-008.1 Work-item API and inbox UI
- [ ] [ ] SDLC-008.2 AGENT-001, COMPLY-001, GAP-TRUTH-008 and low-confidence triples (AI-003) create work items
- [ ] [ ] SDLC-008.3 SLA breach escalates
- [ ] [ ] SDLC-008.4 Decisions are in the audit ledger
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-009 [P1] SDLC-009: Resilience patterns library: backpressure, load shedding, bulkheads

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1549-1567` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-009: Resilience patterns library: backpressure, load shedding, bulkheads

- [ ] `SDLC-009` **Resilience patterns library: backpressure, load shedding, bulkheads**
- **Priority**: P1 | **Category**: Architecture and design | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `TEST-001`
- **Related existing items**: G2-REL-*, G2-EKAF-011
- **Why (evidence from the documents)**: TEST-001 tests failures and CORE-005 mentions a circuit breaker, but no requirement builds shared resilience behaviour. Ingestion bursts (G2-EKAF rate limiting), agent swarms and RAG under load (TEST-002) will otherwise be handled engine by engine.
- **Implementation**:
  - Shared timeouts, retries with jitter, circuit breakers, bulkhead pools and load-shedding policy with priority classes.
  - Adopt in ingestion, agent swarm, RAG and the router.
  - Metrics for shed, retried and tripped calls.
- **Suggested paths**: `packages/eoip/resilience/`
- **Acceptance criteria**:
  - [ ] `SDLC-009.1` Library with unit tests
  - [ ] `SDLC-009.2` Used by at least ingestion, agent fan-out and RAG paths
  - [ ] `SDLC-009.3` TEST-001 scenarios prove graceful degradation
  - [ ] `SDLC-009.4` Shedding preserves P0 traffic classes
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-009.1 Library with unit tests
- [ ] [ ] SDLC-009.2 Used by at least ingestion, agent fan-out and RAG paths
- [ ] [ ] SDLC-009.3 TEST-001 scenarios prove graceful degradation
- [ ] [ ] SDLC-009.4 Shedding preserves P0 traffic classes
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-010 [P1] SDLC-010: Static analysis, typing and layering gates

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1570-1588` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-010: Static analysis, typing and layering gates

- [ ] `SDLC-010` **Static analysis, typing and layering gates**
- **Priority**: P1 | **Category**: Build and code quality | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: KGF S-03
- **Why (evidence from the documents)**: KGF S-03 mentions lint but no type, security-lint or dependency-direction checks. Phase 4 adds about 14 new or extended packages that must not form import cycles (for example graph_graph must not import agents).
- **Implementation**:
  - ruff and a security linter (bandit or semgrep rules) in CI; mypy or pyright strict on new packages, baseline on old ones.
  - import-linter contracts for package layering; ESLint for apps/web.
  - Pre-commit hooks mirror CI.
- **Suggested paths**: `pyproject.toml`, `.importlinter`, `.pre-commit-config.yaml`
- **Acceptance criteria**:
  - [ ] `SDLC-010.1` Linters and type checker in CI
  - [ ] `SDLC-010.2` New packages pass strict typing
  - [ ] `SDLC-010.3` Layering contract file exists and is enforced
  - [ ] `SDLC-010.4` Pre-commit config documented
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-010.1 Linters and type checker in CI
- [ ] [ ] SDLC-010.2 New packages pass strict typing
- [ ] [ ] SDLC-010.3 Layering contract file exists and is enforced
- [ ] [ ] SDLC-010.4 Pre-commit config documented
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-011 [P1] SDLC-011: Coverage measurement and changed-lines gate

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1589-1606` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 9.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-011: Coverage measurement and changed-lines gate

- [ ] `SDLC-011` **Coverage measurement and changed-lines gate**
- **Priority**: P1 | **Category**: Build and code quality | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Why (evidence from the documents)**: Both audits count tests (2,843) but never report coverage. Many acceptance criteria say only "unit tests". A pass count says nothing about which behaviour is exercised.
- **Implementation**:
  - Measure line and branch coverage in CI; publish trend.
  - Gate on changed-lines coverage for PRs rather than a global number.
  - Per-package thresholds for critical engines.
- **Suggested paths**: `.coveragerc`
- **Acceptance criteria**:
  - [ ] `SDLC-011.1` Coverage report in CI
  - [ ] `SDLC-011.2` Changed-lines gate enforced
  - [ ] `SDLC-011.3` Critical engines have thresholds
  - [ ] `SDLC-011.4` Baseline recorded
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] say only "unit tests". A pass count says nothing about which behaviour is exercised
- [ ] Measure line and branch coverage in CI; publish trend
- [ ] Gate on changed-lines coverage for PRs rather than a global number
- [ ] Per-package thresholds for critical engines
- [ ] [ ] SDLC-011.1 Coverage report in CI
- [ ] [ ] SDLC-011.2 Changed-lines gate enforced
- [ ] [ ] SDLC-011.3 Critical engines have thresholds
- [ ] [ ] SDLC-011.4 Baseline recorded
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-012 [P1] SDLC-012: Synthetic enterprise graph and corpus generator

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1607-1625` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-012: Synthetic enterprise graph and corpus generator

- [ ] `SDLC-012` **Synthetic enterprise graph and corpus generator**
- **Priority**: P1 | **Category**: Build and code quality | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: TEST-002, KGF S-02, PERF-01
- **Why (evidence from the documents)**: TEST-002, the 50K-node latency KPI, chaos tests, COMPLY-002 and truth-resolution tests all need realistic data, and the performance tests today use in-memory stores only.
- **Implementation**:
  - Seeded generator for graphs (1K to 10M nodes, skewed degree, multiple domains), documents, planted PII, contradictory claims and temporal histories.
  - Deterministic: the same seed produces the same data and hashes.
  - Loaders for HugeGraph and the memory store.
- **Suggested paths**: `packages/eoip/testing/synthetic/`
- **Acceptance criteria**:
  - [ ] `SDLC-012.1` Generator with seeds and size presets
  - [ ] `SDLC-012.2` Planted-PII and contradiction modes
  - [ ] `SDLC-012.3` Used by TEST-002, TEST-001 and COMPLY-002 tests
  - [ ] `SDLC-012.4` Documented data shapes
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-012.1 Generator with seeds and size presets
- [ ] [ ] SDLC-012.2 Planted-PII and contradiction modes
- [ ] [ ] SDLC-012.3 Used by TEST-002, TEST-001 and COMPLY-002 tests
- [ ] [ ] SDLC-012.4 Documented data shapes
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-014 [P1] SDLC-014: Mutation testing for correctness-critical engines

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1645-1661` (heading) · **Type:** Non-Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-014: Mutation testing for correctness-critical engines

- [ ] `SDLC-014` **Mutation testing for correctness-critical engines**
- **Priority**: P2 | **Category**: Build and code quality | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-011`
- **Why (evidence from the documents)**: Verification rules, token-format round trips, routing, budgets and compliance constraints fail silently if tests are weak. Mutation scores show whether tests would notice a regression.
- **Implementation**:
  - Run mutation testing nightly on verification, token_formats, routing, token_budget and compliance packages.
  - Track mutation score trend; surviving mutants become test tasks.
- **Suggested paths**: `.github/workflows/mutation.yml`
- **Acceptance criteria**:
  - [ ] `SDLC-014.1` Nightly job on named packages
  - [ ] `SDLC-014.2` Score threshold per package
  - [ ] `SDLC-014.3` Survivor report
  - [ ] `SDLC-014.4` No impact on PR latency
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-014' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-014') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Track mutation score trend; surviving mutants become test tasks
- [ ] [ ] SDLC-014.1 Nightly job on named packages
- [ ] [ ] SDLC-014.2 Score threshold per package
- [ ] [ ] SDLC-014.3 Survivor report
- [ ] [ ] SDLC-014.4 No impact on PR latency
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-017 [P1] SDLC-017: Contract tests across API, SDKs, MCP, web client and VS Code extension

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1701-1718` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-017: Contract tests across API, SDKs, MCP, web client and VS Code extension

- [ ] `SDLC-017` **Contract tests across API, SDKs, MCP, web client and VS Code extension**
- **Priority**: P1 | **Category**: Verify and test | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `INFRA-006`
- **Related existing items**: KGF H-03, H-08
- **Why (evidence from the documents)**: 502 routes, an MCP app, a VS Code extension, generated SDKs (INFRA-006) and a web client all consume the same API. CG-GAP-001/002 already show scanner-vs-route drift. Per-surface unit tests do not catch it.
- **Implementation**:
  - Generate contract tests from the OpenAPI schema; consumer-driven contracts for MCP tools, SDKs, web and extension.
  - Breaking-change detection in CI.
- **Suggested paths**: `tests/contract/`
- **Acceptance criteria**:
  - [ ] `SDLC-017.1` Contract suite runs in CI
  - [ ] `SDLC-017.2` MCP tool schemas covered
  - [ ] `SDLC-017.3` SDK and web client use the same contracts
  - [ ] `SDLC-017.4` Breaking change fails the build
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-017' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-017') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-017.1 Contract suite runs in CI
- [ ] [ ] SDLC-017.2 MCP tool schemas covered
- [ ] [ ] SDLC-017.3 SDK and web client use the same contracts
- [ ] [ ] SDLC-017.4 Breaking change fails the build
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-020 [P1] SDLC-020: Upgrade and compatibility matrix

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1754-1770` (heading) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-020: Upgrade and compatibility matrix

- [ ] `SDLC-020` **Upgrade and compatibility matrix**
- **Priority**: P2 | **Category**: Verify and test | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-007`
- **Why (evidence from the documents)**: Token formats, knowledge packages, durable queues and registries must survive upgrades. Python, Node, HugeGraph, Redis and browser versions also vary on customer sites.
- **Implementation**:
  - N-1 to N upgrade tests with data; version matrix for Python, Node, HugeGraph, Redis, browsers.
  - Deprecation policy aligned with INFRA-006.
- **Suggested paths**: `tests/compat/`
- **Acceptance criteria**:
  - [ ] `SDLC-020.1` Upgrade test with seeded data
  - [ ] `SDLC-020.2` Version matrix in CI (scheduled)
  - [ ] `SDLC-020.3` Backward-compat tests for formats and packages
  - [ ] `SDLC-020.4` Policy documented
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-020' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-020') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-020.1 Upgrade test with seeded data
- [ ] [ ] SDLC-020.2 Version matrix in CI (scheduled)
- [ ] [ ] SDLC-020.3 Backward-compat tests for formats and packages
- [ ] [ ] SDLC-020.4 Policy documented
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-022 [P1] SDLC-022: Release engineering: SemVer, changelog, SBOM and signed artifacts

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1791-1809` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-022: Release engineering: SemVer, changelog, SBOM and signed artifacts

- [ ] `SDLC-022` **Release engineering: SemVer, changelog, SBOM and signed artifacts**
- **Priority**: P1 | **Category**: Release and deploy | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `INFRA-003`
- **Related existing items**: KGF GAP-GITOPS-008, G2-SRC-SBOM
- **Why (evidence from the documents)**: GAP-GITOPS-008 versions ontology releases only. Enterprise buyers ask for SBOMs and signed builds; the platform already ingests SBOMs (G2-SRC-SBOM) but does not publish its own.
- **Implementation**:
  - SemVer, conventional commits and automated changelog; release candidate and promotion flow.
  - Generate CycloneDX or SPDX SBOMs and license report; sign images and wheels; record build provenance.
  - Rollback runbook per release.
- **Suggested paths**: `.github/workflows/release.yml`
- **Acceptance criteria**:
  - [ ] `SDLC-022.1` Automated changelog and version bump
  - [ ] `SDLC-022.2` SBOM and license report per release
  - [ ] `SDLC-022.3` Signed artifacts verified in CI
  - [ ] `SDLC-022.4` Rollback runbook tested
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-022' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-022') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-022.1 Automated changelog and version bump
- [ ] [ ] SDLC-022.2 SBOM and license report per release
- [ ] [ ] SDLC-022.3 Signed artifacts verified in CI
- [ ] [ ] SDLC-022.4 Rollback runbook tested
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-024 [P1] SDLC-024: Air-gapped installation bundle and offline update channel

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1829-1846` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-024: Air-gapped installation bundle and offline update channel

- [ ] `SDLC-024` **Air-gapped installation bundle and offline update channel**
- **Priority**: P1 | **Category**: Release and deploy | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-022`
- **Related existing items**: KGF principle: air-gap deployable, NFR-SEC-001
- **Why (evidence from the documents)**: The principles say "air-gap deployable", yet no task builds an offline installer. Local models and embeddings (H-02) need weights, images, wheels, npm packages and docs delivered without internet.
- **Implementation**:
  - Reproducible bundle: images, wheels, npm packages, model weights, docs, checksums and signatures.
  - Offline update procedure and verification script.
- **Suggested paths**: `deploy/airgap/`
- **Acceptance criteria**:
  - [ ] `SDLC-024.1` Bundle build in CI
  - [ ] `SDLC-024.2` Install on a host with no network egress
  - [ ] `SDLC-024.3` Signature and checksum verification
  - [ ] `SDLC-024.4` Update from bundle N to N+1
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-024' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-024') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-024.1 Bundle build in CI
- [ ] [ ] SDLC-024.2 Install on a host with no network egress
- [ ] [ ] SDLC-024.4 Update from bundle N to N+1
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-025 [P1] SDLC-025: Unified observability: traces, metrics and logs with GenAI conventions

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1849-1867` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-025: Unified observability: traces, metrics and logs with GenAI conventions

- [ ] `SDLC-025` **Unified observability: traces, metrics and logs with GenAI conventions**
- **Priority**: P1 | **Category**: Operate and maintain | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `INFRA-004`
- **Related existing items**: NFR-OPS-001, NFR-OPS-002, G2-TEL-*
- **Why (evidence from the documents)**: INFRA-004 adds logs and OpenTelemetry is optional. CORE-002, CORE-003 and CORE-006 each make decisions (blocked, routed, over budget) that must be reconstructable end to end.
- **Implementation**:
  - Trace context through API, loops, agents, retrieval and model calls; spans for LLM calls, tool calls and retrievals.
  - Trace ID attached to logs, verification results, routing and budget decisions.
  - Local-first collector configuration.
- **Suggested paths**: `packages/eoip/observability/`
- **Acceptance criteria**:
  - [ ] `SDLC-025.1` Traces cover a full agent request
  - [ ] `SDLC-025.2` Trace ID present in logs and decision records
  - [ ] `SDLC-025.3` Dashboards for latency and cost by span
  - [ ] `SDLC-025.4` Works with no external backend
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-025' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-025') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-025.1 Traces cover a full agent request
- [ ] [ ] SDLC-025.2 Trace ID present in logs and decision records
- [ ] [ ] SDLC-025.3 Dashboards for latency and cost by span
- [ ] [ ] SDLC-025.4 Works with no external backend
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-026 [P1] SDLC-026: SLOs, alert catalog, runbooks and incident process

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1868-1885` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-026: SLOs, alert catalog, runbooks and incident process

- [ ] `SDLC-026` **SLOs, alert catalog, runbooks and incident process**
- **Priority**: P1 | **Category**: Operate and maintain | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `TEST-001`
- **Related existing items**: G2-SLO-*, REL-10
- **Why (evidence from the documents)**: The G2-SLO family has four untitled gaps and REL-10 needs a DR runbook. There is no incident, on-call or postmortem process anywhere in the three backlogs.
- **Implementation**:
  - SLOs and error budgets per engine; alert catalog with actionable thresholds.
  - Runbook per engine and per failure scenario; incident and postmortem templates; game days using TEST-001.
- **Suggested paths**: `docs/runbooks/`
- **Acceptance criteria**:
  - [ ] `SDLC-026.1` SLOs defined for core engines
  - [ ] `SDLC-026.2` Runbooks exist and are linked from alerts
  - [ ] `SDLC-026.3` Postmortem template
  - [ ] `SDLC-026.4` One game day completed
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-026' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-026') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-026.1 SLOs defined for core engines
- [ ] [ ] SDLC-026.2 Runbooks exist and are linked from alerts
- [ ] [ ] SDLC-026.3 Postmortem template
- [ ] [ ] SDLC-026.4 One game day completed
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-027 [P1] SDLC-027: FinOps and benefit realization

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1886-1904` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-027: FinOps and benefit realization

- [ ] `SDLC-027` **FinOps and benefit realization**
- **Priority**: P1 | **Category**: Operate and maintain | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `CORE-006`, `CORE-003`
- **Related existing items**: MS-27, CORE-006
- **Why (evidence from the documents)**: Token economics is called the number one cost concern, and CORE-001/003 claim 30-70% token savings and 40-60% cost reduction. Nothing measures whether the savings occur.
- **Implementation**:
  - Attribute cost (tokens, compute, storage) per tenant, agent, route and feature; budgets and anomaly alerts.
  - Before/after benefit dashboard that checks each claim against measured data.
  - Showback report.
- **Suggested paths**: `packages/eoip/finops/`
- **Acceptance criteria**:
  - [ ] `SDLC-027.1` Cost attribution per tenant and route
  - [ ] `SDLC-027.2` Budget alerts
  - [ ] `SDLC-027.3` Benefit dashboard for CORE-001/003/006 claims
  - [ ] `SDLC-027.4` Monthly showback export
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-027' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-027') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-027.1 Cost attribution per tenant and route
- [ ] [ ] SDLC-027.2 Budget alerts
- [ ] [ ] SDLC-027.3 Benefit dashboard for CORE-001/003/006 claims
- [ ] [ ] SDLC-027.4 Monthly showback export
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-031 [P1] SDLC-031: Capacity planning, hardware profiles and local model resource manager

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1960-1978` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-031: Capacity planning, hardware profiles and local model resource manager

- [ ] `SDLC-031` **Capacity planning, hardware profiles and local model resource manager**
- **Priority**: P1 | **Category**: Operate and maintain | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `TEST-002`
- **Related existing items**: KGF KPI p95 at 50K nodes, MS-15, GRAPH-004
- **Why (evidence from the documents)**: Local-first means customers run self_llm (5 tiers), embeddings, GNN training (GRAPH-004) and fine-tuning (MS-15) on their own hardware. No sizing guide exists and the latency KPI names no hardware.
- **Implementation**:
  - Reference hardware profiles (CPU-only, single GPU, multi-GPU) with measured throughput and latency.
  - Resource manager: model loading, batching, queueing, quantization profiles and a CPU fallback.
  - Sizing guide and calculator.
- **Suggested paths**: `packages/eoip/runtime/resources.py`
- **Acceptance criteria**:
  - [ ] `SDLC-031.1` Profiles measured and published
  - [ ] `SDLC-031.2` Resource manager with queueing
  - [ ] `SDLC-031.3` CPU-only path works
  - [ ] `SDLC-031.4` Sizing guide
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-031' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-031') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-031.1 Profiles measured and published
- [ ] [ ] SDLC-031.2 Resource manager with queueing
- [ ] [ ] SDLC-031.3 CPU-only path works
- [ ] [ ] SDLC-031.4 Sizing guide
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-032 [P1] SDLC-032: Docs-as-code CI and documentation site

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1981-1998` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-032: Docs-as-code CI and documentation site

- [ ] `SDLC-032` **Docs-as-code CI and documentation site**
- **Priority**: P1 | **Category**: Docs, DX and go-to-market | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: KGF CG-GAP-003, CG-GAP-005, S-04
- **Why (evidence from the documents)**: Five of the nine CG gaps are documentation drift (stale paths, stale stack claims, a missing console, broken links, historical counts). The same will happen to 49 new requirements without automation.
- **Implementation**:
  - CI checks: link check, referenced-path existence, executable code snippets, stale-count detector against generated facts.
  - Versioned documentation site with API reference generated from OpenAPI and a glossary.
- **Suggested paths**: `docs/`, `mkdocs.yml`
- **Acceptance criteria**:
  - [ ] `SDLC-032.1` Link and path checks fail the build
  - [ ] `SDLC-032.2` Snippets executed in CI
  - [ ] `SDLC-032.3` Docs site builds from the repo
  - [ ] `SDLC-032.4` Facts (route counts, test counts) injected from generated files
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-032' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-032') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-032.1 Link and path checks fail the build
- [ ] [ ] SDLC-032.2 Snippets executed in CI
- [ ] [ ] SDLC-032.3 Docs site builds from the repo
- [ ] [ ] SDLC-032.4 Facts (route counts, test counts) injected from generated files
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-002 [P2] SDLC-002: Architecture decision records and decision register

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1414-1432` (heading) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-002: Architecture decision records and decision register

- [ ] `SDLC-002` **Architecture decision records and decision register**
- **Priority**: P2 | **Category**: Plan and requirements | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: KGF DEC-01..DEC-10
- **Why (evidence from the documents)**: The two backlogs already hold 10 open decisions (DEC-01..10), 12 source conflicts and now 6 more baseline conflicts. Decisions recorded only in chat or a table get re-opened.
- **Implementation**:
  - docs/adr/ with a short template (context, decision, consequences, status, linked requirement IDs).
  - Migrate DEC-xx and C-xx/B-xx entries into ADRs as they are decided.
  - Link ADR IDs from the requirement registry.
- **Suggested paths**: `docs/adr/`
- **Acceptance criteria**:
  - [ ] `SDLC-002.1` ADR template and index exist
  - [ ] `SDLC-002.2` Every decided DEC item has an ADR
  - [ ] `SDLC-002.3` Requirement registry rows link to ADRs
  - [ ] `SDLC-002.4` ADR numbering is checked in CI
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-002.1 ADR template and index exist
- [ ] [ ] SDLC-002.2 Every decided DEC item has an ADR
- [ ] [ ] SDLC-002.3 Requirement registry rows link to ADRs
- [ ] [ ] SDLC-002.4 ADR numbering is checked in CI
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-013 [P2] SDLC-013: Test hygiene and CI speed

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1626-1644` (heading) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-013: Test hygiene and CI speed

- [ ] `SDLC-013` **Test hygiene and CI speed**
- **Priority**: P2 | **Category**: Build and code quality | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: CG baseline
- **Why (evidence from the documents)**: The CG audit records 34 skipped tests, 2 warnings and a 709.87 s full run. Phase 4 adds dozens of modules; a slow suite slows every agent iteration.
- **Implementation**:
  - Triage each skipped test: fix, delete or document with an expiry.
  - Parallel execution and sharding; test-impact selection for PRs, full suite nightly.
  - Flaky-test detection and quarantine with an owner.
- **Suggested paths**: `pytest.ini`
- **Acceptance criteria**:
  - [ ] `SDLC-013.1` Zero unexplained skips
  - [ ] `SDLC-013.2` PR run under a set time budget
  - [ ] `SDLC-013.3` Flaky tests tracked
  - [ ] `SDLC-013.4` Warnings fixed or whitelisted with reason
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-013.1 Zero unexplained skips
- [ ] [ ] SDLC-013.2 PR run under a set time budget
- [ ] [ ] SDLC-013.3 Flaky tests tracked
- [ ] [ ] SDLC-013.4 Warnings fixed or whitelisted with reason
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-016 [P2] SDLC-016: Dogfood: manage the platform with the platform

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1681-1698` (heading) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-016: Dogfood: manage the platform with the platform

- [ ] `SDLC-016` **Dogfood: manage the platform with the platform**
- **Priority**: P2 | **Category**: Build and code quality | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-001`
- **Related existing items**: KGR-G-017, code-graph traceability
- **Why (evidence from the documents)**: EOIP already ingests code, Jira, GitLab and documents and offers PR impact triage (KGR-G-017). Ingesting its own repository, requirement registry, tests, ADRs and CI results gives live traceability and impact analysis for this very programme.
- **Implementation**:
  - Ingest the repo, registry, tests and CI results into a tenant of EOIP; model requirement-to-code-to-test edges.
  - Use PR impact triage on its own PRs; dashboard of open requirements by phase.
- **Suggested paths**: `scripts/self_ingest.py`
- **Acceptance criteria**:
  - [ ] `SDLC-016.1` Self-ingestion job
  - [ ] `SDLC-016.2` Requirement-code-test graph queryable
  - [ ] `SDLC-016.3` PR impact comment on internal PRs
  - [ ] `SDLC-016.4` Dashboard shows progress from the registry
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-016' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-016') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-016.1 Self-ingestion job
- [ ] [ ] SDLC-016.2 Requirement-code-test graph queryable
- [ ] [ ] SDLC-016.3 PR impact comment on internal PRs
- [ ] [ ] SDLC-016.4 Dashboard shows progress from the registry
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-018 [P2] SDLC-018: Continuous browser E2E and visual regression

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1719-1736` (heading) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-018: Continuous browser E2E and visual regression

- [ ] `SDLC-018` **Continuous browser E2E and visual regression**
- **Priority**: P2 | **Category**: Verify and test | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `UI-001`
- **Related existing items**: REL-08
- **Why (evidence from the documents)**: KGF REL-08 is a one-time browser run before release. A 90+ component UI changing under UI-001 to UI-009 needs continuous checks.
- **Implementation**:
  - Playwright flows for graph explorer, admin, reports and the new lenses; visual snapshots from Storybook.
  - Runs on PRs touching apps/web; artifacts retained.
- **Suggested paths**: `apps/web/e2e/`
- **Acceptance criteria**:
  - [ ] `SDLC-018.1` E2E suite in CI
  - [ ] `SDLC-018.2` Visual snapshots for shared components
  - [ ] `SDLC-018.3` Flake budget defined
  - [ ] `SDLC-018.4` Runs against the compose stack
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-018' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-018') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-018.1 E2E suite in CI
- [ ] [ ] SDLC-018.2 Visual snapshots for shared components
- [ ] [ ] SDLC-018.3 Flake budget defined
- [ ] [ ] SDLC-018.4 Runs against the compose stack
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-019 [P2] SDLC-019: Soak, endurance and leak testing

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1737-1753` (heading) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-019: Soak, endurance and leak testing

- [ ] `SDLC-019` **Soak, endurance and leak testing**
- **Priority**: P2 | **Category**: Verify and test | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `TEST-002`
- **Why (evidence from the documents)**: There are 14 control loops, 23 autonomous execution loops, a scheduler (INFRA-005) and a durable bus (AGENT-003) that run for days. Unit and load tests do not reveal slow leaks, handle exhaustion or queue growth.
- **Implementation**:
  - Multi-hour soak scenarios with memory, file-handle, thread and queue-depth tracking.
  - Fail on monotonic growth beyond tolerance.
- **Suggested paths**: `tests/soak/`
- **Acceptance criteria**:
  - [ ] `SDLC-019.1` Soak scenarios for loops, scheduler and bus
  - [ ] `SDLC-019.2` Resource-growth assertions
  - [ ] `SDLC-019.3` Run nightly or weekly
  - [ ] `SDLC-019.4` Results feed SLOs
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-019' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-019') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-019.1 Soak scenarios for loops, scheduler and bus
- [ ] [ ] SDLC-019.2 Resource-growth assertions
- [ ] [ ] SDLC-019.3 Run nightly or weekly
- [ ] [ ] SDLC-019.4 Results feed SLOs
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-033 [P2] SDLC-033: Developer experience: one-command bootstrap, CLI, sample data and first-run

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:1999-2016` (heading) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-033: Developer experience: one-command bootstrap, CLI, sample data and first-run

- [ ] `SDLC-033` **Developer experience: one-command bootstrap, CLI, sample data and first-run**
- **Priority**: P2 | **Category**: Docs, DX and go-to-market | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: KGF S-04, G2-EKAF-030
- **Why (evidence from the documents)**: Onboarding for developers and for first-time operators (G2-EKAF-030 onboarding wizard) is not covered. Fast local setup also speeds the AI agent.
- **Implementation**:
  - Dev container and make dev; pre-commit; a small CLI for health, migrations, flags and sample data load.
  - Sample dataset and guided first-run in the web app.
- **Suggested paths**: `Makefile`, `.devcontainer/`
- **Acceptance criteria**:
  - [ ] `SDLC-033.1` Fresh clone to running stack in one command
  - [ ] `SDLC-033.2` CLI covers health, migrate, flags
  - [ ] `SDLC-033.3` Sample data pack
  - [ ] `SDLC-033.4` First-run guide in the UI
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-033' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-033') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-033.1 Fresh clone to running stack in one command
- [ ] [ ] SDLC-033.2 CLI covers health, migrate, flags
- [ ] [ ] SDLC-033.3 Sample data pack
- [ ] [ ] SDLC-033.4 First-run guide in the UI
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SDLC-034 [P2] SDLC-034: Enterprise procurement and GRC pack

- **Source:** `EOIP-engg-doc-pkg/eoip-phase4-2-requirements.md:2017-2033` (heading) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
###### SDLC-034: Enterprise procurement and GRC pack

- [ ] `SDLC-034` **Enterprise procurement and GRC pack**
- **Priority**: P2 | **Category**: Docs, DX and go-to-market | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `COMPLY-003`, `TEST-005`
- **Why (evidence from the documents)**: The TAM is enterprise (regulated industries are among the eight domain packs). Buyers ask for SOC 2 and ISO 27001 mappings, a security whitepaper, data-flow diagrams, DPIA templates, an accessibility conformance report and SLAs.
- **Implementation**:
  - Control mapping and evidence automation driven by COMPLY-003.
  - Security whitepaper, data-flow diagrams, DPIA/ROPA templates, accessibility report, SLA and support model.
- **Suggested paths**: `docs/trust/`
- **Acceptance criteria**:
  - [ ] `SDLC-034.1` Control mapping document with evidence links
  - [ ] `SDLC-034.2` Whitepaper and data-flow diagrams
  - [ ] `SDLC-034.3` DPIA template
  - [ ] `SDLC-034.4` Accessibility conformance report
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'SDLC-034' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('SDLC-034') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] [ ] SDLC-034.1 Control mapping document with evidence links
- [ ] [ ] SDLC-034.2 Whitepaper and data-flow diagrams
- [ ] [ ] SDLC-034.3 DPIA template
- [ ] [ ] SDLC-034.4 Accessibility conformance report
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

