# Living AI Agent Worker "Graffin" — Architectural Specification & Aggregate Requirements

> **Document ID**: GRF-REQ-v1  
> **Date**: 2026-10-19  
> **Status**: Approved for Implementation  
> **Product**: Enterprise Operational Intelligence Platform (EOIP) / KnowGridFlow (KGF)  
> **Agent Codename**: **Graffin** (The Sovereign Guardian & Living Worker of the Enterprise Brain)  
> **Companion**: `living-AI-agg-Graffin-implementation-plan.md` (build sequencing, safety verification, proof-of-done protocol)  
> **Audience**: AI Coding Agents, Systems Architects, Safety Officers, and Verification Engineers  
> **Scope**: Eternal autonomous agent runtime, immutable safety constitution, multi-channel kill switch, autonomy levels, external evaluators, autonomic maintenance, performance optimization, and REVA Proof-of-Done integration.

---

## 0. Foundational Rules That Override Everything

### 0.1 Code and Test Files Are Not Proof of Completion
The existence of source code, test files, mock harnesses, or CI pass badges is **never** accepted as proof that Graffin or any of its sub-modules are complete. Graffin is functional and verified **only** when its execution is proven by signed REVA Warrants (`wr1_...`), active Merkle transparency log inclusion, and a valid canonical signed ledger (`ldg1_[0-9a-f]{64}`).

### 0.2 Safety-First Supremacy
If any operational requirement (performance optimization, graph compaction, schema induction, or task execution) conflicts with Graffin's **Immutable Constitution** (§1) or safety boundaries, **the safety invariant unconditionally wins**. Graffin must halt execution, roll back all transient state, and log an auditable escalation record.

### 0.3 Enhanced Original Construction — No Mere Copies
Graffin does **not** duplicate generic agent frameworks or naive reflex loops. It synthesizes and enhances the state of the art in autonomous operations: integrating bitemporal graph state clocks, consequence budgets ($\kappa$), dual-key cryptographic leases, clone-structured memory schemas, and mathematical calibration into a unified, perpetual, living enterprise worker.

---

## 1. The Immutable Constitution of Graffin

Graffin is bound by ten inviolable constitutional invariants (C01–C10). The constitution is hashed (`con1_[0-9a-f]{64}`), stored in Write-Once-Read-Many (WORM) storage, and evaluated by an independent cryptographic kernel before every state transition.

```
+----------------------------------------------------------------------------------------------------+
|                                THE IMMUTABLE CONSTITUTION (C01 - C10)                              |
+----------------------------------------------------------------------------------------------------+
|  C01: Ground Truth Inviolability      | Inferred data is NEVER labeled 'observed'.                 |
|  C02: Non-Self-Exemption               | Graffin cannot alter its constitution, evaluators, or limits|
|  C03: Consequence Budget Enforcement  | All mutations bounded by kappa-budgets & atomic rollbacks. |
|  C04: Dual-Key Governance for R3/R4    | Destructive actions require cryptographic human quorum.    |
|  C05: Bitemporal Lineage Auditing      | Every mutation records valid_time and recorded_at.        |
|  C06: REVA Proof-of-Done Gating        | Zero unverified commits; all work requires ldg1_... ledger.|
|  C07: Deterministic Kill Switch        | Immediate shutdown (< 500ms) upon hardware/signal trigger. |
|  C08: Multi-Tenant Cryptographic Fence | Zero cross-tenant data leakage or permission bypass.       |
|  C09: Epistemic Calibration            | Stated confidence must be mathematically calibrated (ECE). |
|  C10: Autonomic Resource Capping       | Strict CPU, memory, token, and API financial limits.       |
+----------------------------------------------------------------------------------------------------+
```

### Invariant C01: Ground Truth Inviolability
Graffin **SHALL NEVER** label a synthesized, inferred, or predicted datum as `observed`. Any graph entity, property, or edge created by Graffin without a direct cryptographic witness from an external source system must be tagged with `epistemic_state = "inferred"`. Violation triggers immediate self-quarantine.

### Invariant C02: Non-Self-Exemption & Self-Modification Ban
Graffin **SHALL NEVER** edit, patch, relax, or bypass its own constitution, its autonomy level bounds, its evaluator models, or its kill switch logic. Any attempt to modify these files or runtime objects raises an uncatchable security exception and trips the kill switch.

### Invariant C03: Consequence Budget Enforcement ($\kappa$-Budgets)
Every autonomous action sequence executed by Graffin is allocated a finite consequence budget $\kappa \in [0, 10000]$. Each tool call, graph mutation, or external request deducts from $\kappa$ based on its blast radius:
$$\kappa_{\text{remaining}} = \kappa_{\text{initial}} - \sum_{i=1}^{M} \text{Cost}(a_i)$$
If $\kappa_{\text{remaining}} \le 0$, execution immediately pauses and requests human escalation.

### Invariant C04: Dual-Key Governance for High-Risk Operations
Operations classified as Risk Tier R3 (e.g., dropping obsolete tables, migrating live schemas, bulk-deleting graph subgraphs) or R4 (e.g., modifying access control policies or financial triggers) **CANNOT** be executed autonomously. They require dual cryptographic authorization: Graffin's operational signature plus a human attested warrant (`Authority.HUMAN_ATTESTED`).

### Invariant C05: Bitemporal Lineage Auditing
Every state change committed by Graffin must record:
1. `valid_time`: The real-world operational interval $[t_1, t_2]$ over which the change is physically true.
2. `recorded_at`: The cryptographic timestamp when REVA sealed the transaction.

### Invariant C06: REVA Proof-of-Done Gating
Graffin **CANNOT** commit code, schemas, or graph updates directly to production branches. Every change must be wrapped as a Git PR or atomic transaction accompanied by an in-toto v1 Statement and a canonical signed REVA Ledger (`ldg1_[0-9a-f]{64}`).

### Invariant C07: Deterministic Kill Switch Compliance
Graffin must poll its kill switch registers every $\le 100\text{ ms}$. Upon receiving an abort signal, Graffin must cleanly cease execution within $\le 500\text{ ms}$, revoke all active write leases, and flush forensic state.

### Invariant C08: Multi-Tenant Cryptographic Partitioning
Graffin operates across multiple enterprise tenants but **SHALL NEVER** blend cross-tenant memory, embeddings, or graph pointers. Every tenant namespace is cryptographically partitioned using SHA-256 tenant derivations and separate CAS roots.

### Invariant C09: Epistemic Calibration
Graffin's self-reported confidence must maintain an Expected Calibration Error $\text{ECE} \le 0.12$ and Brier score $\le 0.15$ measured against historical outcomes. Overconfident hallucinations automatically throttle Graffin's operational authority.

### Invariant C10: Autonomic Resource & Financial Self-Throttling
Graffin is constrained by hard caps: max 4 CPU cores, max 8 GiB RAM, max 100,000 LLM tokens per hour, and max $50.00/day external API expenditure. Approaching $90\%$ of any budget forces graceful degradation to local deterministic algorithms.

---

## 2. Autonomy Levels Specification (L0 to L5)

Graffin operates under a dynamic, policy-governed autonomy level framework. The active level is tenant-configurable and automatically demotes upon anomaly detection.

```
+----------------------------------------------------------------------------------------------------+
|                                    AUTONOMY LEVELS (L0 - L5)                                       |
+----------------------------------------------------------------------------------------------------+
|  L0: Passive Observer       | Read-only health monitoring, audit logging, zero graph mutations.    |
|  L1: Advisory Agent         | Proposes optimization PRs and index recipes; human must execute.     |
|  L2: Supervised Executor    | Executes human-selected actions under strict Human-in-the-Loop (HITL)|
|  L3: Bounded Autonomous     | Autonomously executes low-risk R1 repairs (HOTL; kappa < 100).        |
|  L4: High Autonomy Worker   | Executes R1/R2 optimizations (HBTL); automatic snapshot rollbacks.   |
|  L5: Self-Evolving Brain    | Governed autonomic schema & loop refinement; dual-key verification.  |
+----------------------------------------------------------------------------------------------------+
```

### Level 0: Passive Observer (Read-Only)
- **Permissions**: Read-only access to GL0–GL3, system logs, metrics, and REVA store.
- **Allowed Actions**: Health checks, doctor diagnostics, gap identification, audit reports.
- **Mutations**: $0$ writes permitted.

### Level 1: Advisory Agent (Recommendations Only)
- **Permissions**: Read-only graph access + ability to post `ChangeProposal` records.
- **Allowed Actions**: Drafting index optimization recipes, recommending schema merges, identifying orphaned vertices.
- **Mutations**: Proposals stored in proposal queue; human approval required for application.

### Level 2: Supervised Executor (HITL)
- **Permissions**: Execution of pre-compiled, verified action scripts.
- **Allowed Actions**: Applying cleanups that have received explicit human sign-off via REST or CLI.
- **Human Invariant**: Human must click approve or supply signed warrant for each step.

### Level 3: Bounded Autonomous Worker (HOTL)
- **Permissions**: Autonomous execution of low-risk operational maintenance (Risk Tier R1).
- **Allowed Actions**: Index cache warming, vacuuming dead SQLite WAL files, reconciling missing bitemporal endpoints, executing non-mutating knowledge gap probes.
- **Budget**: $\kappa \le 100$ per sequence. Human is notified post-execution (Human-on-the-Loop).

### Level 4: High Autonomy Worker (HBTL)
- **Permissions**: Autonomous execution of Tier R1 and R2 operations under Human-Beside-the-Loop (HBTL).
- **Allowed Actions**: Dynamic CSCG clone splitting, episodic-to-semantic memory consolidation, query rewriting, transient service mock provisioning.
- **Safeguard**: Atomic recovery snapshot taken before mutation; automatic rollback if error rate spikes by $\ge 2\%$.

### Level 5: Governed Self-Evolving Worker
- **Permissions**: Autonomous schema tuning, agent loop optimization, and verifier orchestration.
- **Allowed Actions**: AutoSchemaKG induction, updating meta-graph templates, retiring deprecated predicates.
- **Mandatory Invariant**: Every commit must produce an in-toto attestation and pass REVA Check 12 closure evaluation.

---

## 3. Multi-Channel Kill Switch & Fail-Safe Architecture

The kill switch is a dedicated, fail-closed subsystem (`reva.agents.graffin.kill_switch`) completely independent of Graffin's cognitive loop.

```
+----------------------------------------------------------------------------------------------------+
|                                    MULTI-CHANNEL KILL SWITCH                                       |
+----------------------------------------------------------------------------------------------------+
|  Channel 1: OS Signal Trap    | SIGINT / SIGTERM / SIGKILL intercepted by C-level runtime handler. |
|  Channel 2: Distributed Heartbeat| Missing Redis/file heartbeat for > 500ms trips hardware interlock.|
|  Channel 3: Cryptographic Token | REST /kill endpoint with Ed25519 root signature revokes leases.   |
|  Channel 4: Dead-Man's Timer   | Unacknowledged watchdog timer trips if main thread hangs > 5.0s.   |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|                                  DETERMINISTIC SHUTDOWN SEQUENCE                                   |
|  1. Halt execution loop within <= 100ms.                                                           |
|  2. Revoke all active write leases (lse1_...) in GraphStore and SQLite.                            |
|  3. Roll back uncommitted atomic transaction snapshots.                                           |
|  4. Flush forensic crash dump to WORM storage (.data/graffin_blackbox/).                           |
|  5. Exit process with code 137 (SIGKILL) or 143 (SIGTERM). Total latency <= 500ms.                 |
+----------------------------------------------------------------------------------------------------+
```

### Kill Switch Specifications:
- **Maximum Termination Latency**: $\le 500\text{ ms}$ from trigger receipt to complete thread cessation.
- **Lease Invalidation**: Emits `kgf.lease.emergency_revocation` event, causing database adapters to drop uncommitted transactions.
- **Blackbox Recorder**: Captures Graffin's memory frame, last 10 tool calls, attention schema state, and exception stack trace into a WORM forensic file `blackbox_<timestamp>.json`.

---

## 4. External, Tamper-Proof Evaluators (Isolated Evaluator Framework)

Graffin cannot grade its own work. All evaluation is performed by an isolated external oracle (`GraffinExternalEvaluator`) running in a separate process space with read-only access.

```
+--------------------------+                         +-----------------------------------+
|      LIVING AGENT        |                         |    EXTERNAL TAMPER-PROOF ORACLE   |
|        GRAFFIN           |                         |        (Out-of-Process / WORM)    |
|                          |                         |                                   |
|  1. Propose Mutation     | --- ChangeProposal ---> |  1. Schema Compliance Judge       |
|  2. Execute Bounded Task |                         |  2. Regression Sentinel           |
|  3. Self-Report Confidence| -- ConfidenceScore ---> |  3. Calibration Evaluator (ECE)   |
|                          |                         |  4. Consequence Budget Auditor    |
|                          | <--- Decision & Score - |                                   |
+--------------------------+                         +-----------------------------------+
```

### Evaluator Modules:
1. **Calibration Judge**: Computes Brier Score and Expected Calibration Error (ECE) comparing Graffin's predicted outcomes with ground truth. If Brier Score $> 0.15$, autonomy is demoted from L4/L3 down to L1.
2. **Regression Sentinel**: Clones target graph into a temporary in-memory snapshot, runs the 100 gold-standard regression queries, and verifies zero performance degradation.
3. **Budget & Consequence Auditor**: Verifies that actual tool call costs did not exceed the allocated $\kappa$-budget.
4. **Security & Entitlement Arbiter**: Confirms Graffin did not touch restricted vertex labels (`Identity`, `Credential`, `TenantConfig`) without explicit authorization.

---

## 5. Core Operational Capabilities & Functional Engines

Graffin operates six autonomous engines to keep the EOIP enterprise brain optimal, healthy, and self-improving:

```
+----------------------------------------------------------------------------------------------------+
|                                   GRAFFIN OPERATIONAL ENGINES                                      |
+----------------------------------------------------------------------------------------------------+
|  1. AUTONOMIC DOCTOR & HEALER    | Continuous DB integrity, Merkle log sync, CAS corruption fix.   |
|  2. PERFORMANCE GOVERNOR         | Graph compaction, index tuning, query plan optimization.        |
|  3. GAP & CONTRADICTION HUNTER   | Detecting unproven scopes, generating executable probes.        |
|  4. COGNITIVE CONSOLIDATOR       | mPFC/hippocampal consolidation, CSCG clone state clustering.    |
|  5. PROOF-OF-DONE VERIFIER       | Continuous test runner, in-toto statements, signed ledgers.    |
|  6. DRIFT & ECOSYSTEM AUDITOR    | Dependency security, dead routes, dirty build detection.        |
+----------------------------------------------------------------------------------------------------+
```

### Engine 1: Autonomic Doctor & Self-Healing Daemon
- **Requirements**: `GRF-OPS-001`
- **Actions**:
  * Runs SQLite `PRAGMA integrity_check` and `PRAGMA foreign_key_check` every hour.
  * Verifies Merkle tree consistency between last audited STH and current tree head.
  * Sweeps CAS blob store for unreferenced orphan blobs older than 7 days and triggers safe dry-run GC.
  * Re-synchronizes outbox events if queue lag exceeds 60 seconds.

### Engine 2: Performance Governor & Compaction Engine
- **Requirements**: `GRF-OPS-002`
- **Actions**:
  * Monitors p95 and p99 query latency across all graph queries.
  * Identifies missing property indexes on frequently traversed metapaths and submits an index creation recipe.
  * Executes non-blocking graph compaction during low-traffic windows (02:00–04:00 local time).
  * Re-quantizes dense vector embeddings to INT8 if memory footprint exceeds $80\%$ of budget.

### Engine 3: Knowledge Gap Hunter & Probe Synthesizer
- **Requirements**: `GRF-OPS-003`
- **Actions**:
  * Scans active boundaries and API surfaces for unproven scopes (`not_found_unknown`).
  * Generates executable, safe, read-only probes (e.g., HTTP `HEAD` or schema `OPTIONS` requests) to resolve gaps.
  * If a probe confirms an endpoint, emits `reva.pred.boundary_observed` warrant; if it fails, marks gap `investigating`.

### Engine 4: Contradiction Arbiter & Quarantine Manager
- **Requirements**: `GRF-OPS-004`
- **Actions**:
  * Detects conflicting warrants sharing the same `(tenant_id, subject_key, predicate)` with overlapping valid times.
  * Applies deterministic precedence rules: `human_attested > controlled_execution > runtime_observed > source_system_record`.
  * Moves contradicted items into quarantine and adjusts downstream result coverage to `partial`.

### Engine 5: Continuous Proof-of-Done Verifier & Release Engine
- **Requirements**: `GRF-OPS-005`
- **Actions**:
  * Watches repository file changes and recomputes owner digests across all bound obligations.
  * Marks changed obligations `stale`.
  * Triggers isolated sandbox verifier runs (`reva.sandbox.runner`) to re-verify stale obligations.
  * Emits signed canonical ledgers (`reva-ledger.json`) and updates tracker dashboards.

### Engine 6: Cognitive Consolidator & Schema Evolution Engine
- **Requirements**: `GRF-OPS-006`
- **Actions**:
  * Runs nightly memory consolidation: clusters transient decision traces into reusable Wisdom Graph archetypes.
  * Clusters entity call graphs to identify emergent CSCG clone states.
  * Promotes candidate schemas to shadow or active status upon passing the empirical baseline gate ($p < 0.01$).

---

## 6. Functional Requirements Matrix (Area: GRF-*)

### `GRF-SEC-001`: Cryptographic Constitution Verification Engine
- **Description**: Before Graffin executes any task, the runtime **MUST** verify the cryptographic hash of its constitution against WORM storage.
- **Specification**: If `sha256(constitution.json) != EXPECTED_WORM_HASH`, Graffin enters locked state `STATE_TAMPER_DETECTED` and shuts down.
- **Done-When**:
  - `GRF-SEC-001.D01`: Tampering with any byte in `constitution.json` blocks Graffin startup with exit code 65.
  - `GRF-SEC-001.D02`: Valid constitution initializes Graffin in authorized state.

### `GRF-SEC-002`: Kill Switch Implementation & Verification
- **Description**: The platform **MUST** implement multi-channel kill switch handlers terminating Graffin within $\le 500\text{ ms}$.
- **Specification**:
  * OS Signal Handler: Traps `SIGTERM`, `SIGINT`.
  * REST API Handler: `POST /api/graffin/v1/kill` requiring bearer token.
  * Heartbeat Monitor: Checks `.data/graffin_heartbeat` every $100\text{ ms}$.
- **Done-When**:
  - `GRF-SEC-002.D01`: Triggering kill switch terminates process in $< 500\text{ ms}$ verified by timer tests.
  - `GRF-SEC-002.D02`: All uncommitted database transactions and leases are cleanly released.

### `GRF-OPS-001`: Autonomic Self-Healing Loop Execution
- **Description**: Graffin **MUST** autonomously detect and repair database inconsistencies, Merkle tree lag, and outbox stalls.
- **Specification**: Executes an hourly OODA loop (Observe DB stats, Orient vs. thresholds, Decide repair recipe, Act with rollback protection).
- **Done-When**:
  - `GRF-OPS-001.D01`: Simulated SQLite corruption triggers automatic quarantine and repair notification.
  - `GRF-OPS-001.D02`: 100% of outbox events older than 60s are processed without loss.

### `GRF-OPS-002`: Continuous Performance & Index Governor
- **Description**: Graffin **MUST** continuously optimize graph query performance.
- **Specification**: Tracks query execution plans using SQLite `EXPLAIN QUERY PLAN`. If an unindexed table scan is detected on a query executed $\ge 50$ times, Graffin creates an index proposal.
- **Done-When**:
  - `GRF-OPS-002.D01`: Slow query detection triggers automated index creation under Autonomy L3/L4.
  - `GRF-OPS-002.D02`: p95 query latency improves by $\ge 25\%$ on synthetic load tests.

### `GRF-OPS-003`: Autonomous REVA Proof-of-Done Orchestration
- **Description**: Graffin **MUST** run the REVA verifier pipeline on every code change and emit signed ledgers.
- **Specification**: Invokes `reva.pd.runs.run_verifier`, evaluates 11-step closure checks, computes `ldg1_...` ID, signs with PD key, and updates `reva-tracker.html`.
- **Done-When**:
  - `GRF-OPS-003.D01`: Git commit triggers automated closure evaluation resulting in signed `reva-ledger.json`.
  - `GRF-OPS-003.D02`: Tracker HTML progress updates to reflect closed items automatically.

### `GRF-OPS-004`: Autonomous Repository Ingestion & Continuous Knowledge/Wisdom Graph Maintenance
- **Description**: Whenever a GitHub, GitLab, Bitbucket, or Git repository URL is provided, Graffin **MUST** autonomously ingest the repository into an isolated sandbox, execute pure-Python extractors to project the codebase into the Knowledge Graph (GL0–GL3) and Wisdom Graph (GW), and strictly prevent any proprietary code or secret leaks to LLMs.
- **Specification**:
  1. Clones the remote repository using REVA's sandboxed `GitRepositoryCloner` with shallow depth (`--depth 1` default), time budget ($\le 300\text{s}$), and size quota ($\le 5\text{ GiB}$).
  2. Executes pure-Python extraction ($\ge 95\%$ deterministic Python logic using Tree-sitter, Capstone, `pyelftools`, and `axml`):
     - Maps application boundaries, services, routes, and resources into the Knowledge Graph.
     - Disassembles embedded native libraries (`.so`, `.dll`) and maps JNI native bridges (`reva_CALLS_NATIVE`).
     - Parses Architectural Decision Records (ADRs) and Conventional Commits into Wisdom Graph `wg_Decision`, `wg_Precedent`, and `wg_Lesson` nodes.
  3. Enforces the **Zero-Data-Leak LLM Egress Gate** (`REVA-SEC-013`):
     - Local offline LLMs (via Ollama/vLLM) are the mandatory default; external LLM calls are blocked unless explicitly authorized.
     - Automated RFC 6901 pointer redaction scrubs all tokens, keys, passwords, database URLs, and PII.
     - Proprietary source code is never transmitted raw; it is abstracted into pseudonymized structural tokens.
- **Done-When**:
  - `GRF-OPS-004.D01`: Submitting a repository URL triggers automated cloning, boundary extraction, and Knowledge Graph projection without manual intervention.
  - `GRF-OPS-004.D02`: ADRs and commit histories are synthesized into the Wisdom Graph with `reva_JUSTIFIED_BY` edges.
  - `GRF-OPS-004.D03`: 100% of LLM egress payloads pass DLP byte-scans with zero secret leaks and zero raw source code.

---

## 7. Interfaces (REST, MCP, CLI)

### 7.1 REST Endpoints (`/api/graffin/v1/`)

| Method | Endpoint | Request Body | Response Body | Description |
|---|---|---|---|---|
| `GET` | `/api/graffin/v1/status` | None | `GraffinStatusReport` | Get current state, autonomy level, and health |
| `POST` | `/api/graffin/v1/kill` | `KillRequest` | `KillConfirmation` | Emergency kill switch activation |
| `POST` | `/api/graffin/v1/autonomy` | `SetAutonomyRequest` | `AutonomyState` | Set autonomy level (L0–L5) with admin token |
| `POST` | `/api/graffin/v1/proposals/review` | `ProposalReview` | `ExecutionReceipt` | Approve or reject pending proposal |
| `POST` | `/api/graffin/v1/doctor/run` | None | `DoctorReport` | Force immediate autonomic health check |

### 7.2 FastMCP Tools for Graffin

1. `graffin_status() -> str`: Returns Graffin's active state, current $\kappa$-budget, and memory stats.
2. `graffin_trigger_audit() -> str`: Triggers immediate Doctor and Merkle consistency audit.
3. `graffin_propose_optimization(scope: str, details_json: str) -> str`: Submits an optimization proposal.
4. `graffin_emergency_abort(reason: str) -> str`: Cryptographic emergency abort tool.

### 7.3 CLI Commands

```bash
# Check Graffin living agent status
graffin status

# Set autonomy level
graffin autonomy set L3 --token <admin_token>

# Trigger immediate self-healing cycle
graffin heal --now

# Emergency kill switch
graffin kill --reason "Manual operator override"
```

---

## 8. Telemetry & Safety Metrics

The implementation **MUST** emit Prometheus metrics matching:

1. `graffin_autonomy_level`: Gauge representing active level (0 to 5).
2. `graffin_consequence_budget_remaining`: Gauge tracking remaining $\kappa$-budget.
3. `graffin_kill_switch_status`: Gauge (0 = armed/healthy, 1 = triggered).
4. `graffin_actions_executed_total{risk_tier, status}`: Counter of executed actions.
5. `graffin_calibration_brier_score`: Gauge tracking empirical Brier score ($\le 0.15$).
6. `graffin_evaluation_ece`: Gauge tracking Expected Calibration Error ($\le 0.12$).
7. `graffin_autonomic_repairs_total{domain, status}`: Counter of autonomous repair operations.

---

## 9. Verification & Acceptance Criteria Matrix

| Req ID | Level | Verification Command | Acceptance Threshold |
|---|---|---|---|
| `GRF-SEC-001` | L1 (Contract) | `pytest tests/reva/unit/graffin/test_constitution.py` | Hash mismatch halts Graffin immediately |
| `GRF-SEC-002` | L3 (Perf) | `pytest tests/reva/perf/test_kill_switch_latency.py` | Termination latency $\le 500\text{ ms}$ |
| `GRF-OPS-001` | L2 (Unit) | `pytest tests/reva/unit/graffin/test_autonomic_healer.py` | Self-healing recovers simulated corruptions |
| `GRF-OPS-002` | L3 (Perf) | `pytest tests/reva/perf/test_performance_governor.py` | Latency improves $\ge 25\%$ on slow queries |
| `GRF-OPS-003` | L6 (Ledger) | `python scripts/reva/verify_graffin_ledger_pass.py` | Emits valid signed `ldg1_...` ledger |
