# Living AI Agent Worker "Graffin" — Implementation Plan & Verification Protocol

> **Document ID**: GRF-PLAN-v1  
> **Date**: 2026-10-19  
> **Status**: Approved for Implementation  
> **Product**: Enterprise Operational Intelligence Platform (EOIP) / KnowGridFlow (KGF)  
> **Companion**: `living-AI-agg-Graffin-requirements.md` (normative requirements specification)  
> **Target Package**: `reva/agents/graffin/`, `packages/eoip/agents/graffin/`  
> **Audience**: AI Coding Agents, Systems Architects, Safety Officers, and Verification Engineers  

---

## 0. Non-Negotiable Safety & Implementation Rules

### 0.1 The Evidence Ledger Rule
A file path, class declaration, test count, or green checkmark is **never** accepted as proof that Graffin or any of its capabilities are complete. A task is marked complete **only** when:
1. The implementation executes deterministically in the target runtime.
2. The verification command named in the task's Done-When specification executes with captured evidence.
3. Every numeric safety, latency, or accuracy threshold is satisfied.
4. REVA has evaluated all Proof-of-Done obligations for the task and emitted a cryptographically signed closure decision (`cls1_...`).

### 0.2 Safety Primacy & Constitution Immutability
All work must begin with Phase GRF-P0 (Safety Foundation). The constitution file (`constitution.json`) must be hashed and locked before any autonomous execution loops are written. Any test or implementation modifying the constitution must trigger an immediate fail-closed abort.

### 0.3 Zero-Placeholder Enforcement
Every production file under `reva/agents/graffin/` and related directories must pass `python scripts/reva/forbid_placeholders.py` with **0 violations**. No `pass`-only stubs, no `NotImplementedError`, and no mock fallbacks in production paths.

---

## 1. Implementation Sequencing & Phase Overview

```
+---------------------------------------------------------------------------------------------------------+
|                                  GRAFFIN IMPLEMENTATION PHASES                                          |
+---------------------------------------------------------------------------------------------------------+
|  Phase GRF-P0: Safety Foundation & Multi-Channel Kill Switch                                            |
|  - Immutable constitution hash (WORM), OS signal traps, distributed heartbeat, emergency kill token     |
+---------------------------------------------------------------------------------------------------------+
                                                     |
                                                     v
+---------------------------------------------------------------------------------------------------------+
|  Phase GRF-P1: Autonomy Framework & Consequence Budgets                                                 |
|  - L0-L5 state machine, kappa-budget tracking, dual-key cryptographic authorization for R3/R4 ops       |
+---------------------------------------------------------------------------------------------------------+
                                                     |
                                                     v
+---------------------------------------------------------------------------------------------------------+
|  Phase GRF-P2: External Tamper-Proof Evaluators                                                         |
|  - Out-of-process Calibration Judge (ECE/Brier), Regression Sentinel, Entitlement Auditor                |
+---------------------------------------------------------------------------------------------------------+
                                                     |
                                                     v
+---------------------------------------------------------------------------------------------------------+
|  Phase GRF-P3: Autonomic Maintenance & Performance Optimization Engines                                 |
|  - Self-healing Doctor daemon, graph compaction, query plan governor, vector quantization                |
+---------------------------------------------------------------------------------------------------------+
                                                     |
                                                     v
+---------------------------------------------------------------------------------------------------------+
|  Phase GRF-P4: Knowledge Curation & Schema Evolution Engines                                            |
|  - Knowledge gap hunting & probe synthesis, contradiction quarantine, neural memory consolidation       |
+---------------------------------------------------------------------------------------------------------+
                                                     |
                                                     v
+---------------------------------------------------------------------------------------------------------+
|  Phase GRF-P5: Continuous REVA Proof-of-Done Engine & Perpetual Worker Lifecycle                         |
|  - Git change watching, automated closure evaluation, canonical signed ledger emission (ldg1_...)       |
+---------------------------------------------------------------------------------------------------------+
```

---

## 2. Work Packages & Task Breakdown

### Phase GRF-P0: Safety Foundation & Multi-Channel Kill Switch

#### Task `T-GRF-001`: Immutable Constitution & WORM Cryptographic Hash Verifier
- **File**: `reva/agents/graffin/constitution.py`, `reva/agents/graffin/constitution.json`
- **Requirements**: `GRF-SEC-001`
- **Actions**:
  1. Author `constitution.json` containing the 10 invariant definitions (C01–C10).
  2. Implement `ConstitutionVerifier` computing RFC 8785 canonical hash: `con1_[0-9a-f]{64}`.
  3. Store expected hash in read-only environment / WORM register.
  4. Startup gate: Graffin verifies hash on startup; any mismatch raises `ConstitutionTamperedError` and exits with code 65.
- **Verification**: `pytest tests/reva/unit/graffin/test_constitution.py`
- **Done-When**:
  - `T-GRF-001.D01`: Startup succeeds with authentic constitution hash.
  - `T-GRF-001.D02`: Mutating a single character in `constitution.json` causes immediate exit code 65.

#### Task `T-GRF-002`: Multi-Channel Kill Switch Subsystem
- **File**: `reva/agents/graffin/kill_switch.py`
- **Requirements**: `GRF-SEC-002`
- **Actions**:
  1. Implement `KillSwitchController` with 4 independent trigger channels:
     - Channel 1: POSIX/Windows signal handler (`SIGTERM`, `SIGINT`).
     - Channel 2: File/Redis heartbeat checker (interval $100\text{ ms}$, timeout $500\text{ ms}$).
     - Channel 3: Emergency REST endpoint (`POST /api/graffin/v1/kill`) with bearer token validation.
     - Channel 4: Dead-man's watchdog timer.
  2. Implement atomic shutdown sequence:
     - Cancel all active coroutines and worker threads within $\le 100\text{ ms}$.
     - Call `store.revoke_all_leases(agent_id="graffin")`.
     - Dump forensic state snapshot to `.data/graffin_blackbox/`.
     - Terminate process with exit code 137.
- **Verification**: `pytest tests/reva/perf/test_kill_switch_latency.py`
- **Done-When**:
  - `T-GRF-002.D01`: Measured kill switch termination latency is $\le 500\text{ ms}$ across all 4 channels.
  - `T-GRF-002.D02`: Database write locks and active leases are cleanly released upon kill.

---

### Phase GRF-P1: Autonomy Framework & Consequence Budgets

#### Task `T-GRF-003`: Autonomy Level (L0–L5) State Machine
- **File**: `reva/agents/graffin/autonomy.py`
- **Requirements**: §2
- **Actions**:
  1. Implement `AutonomyLevelManager` managing transitions between L0, L1, L2, L3, L4, L5.
  2. Enforce write permissions per level: L0 (0 writes), L1 (proposals only), L2 (HITL scripts), L3 (R1 only, $\kappa \le 100$), L4 (R1/R2 with auto-rollback), L5 (full autonomous with REVA ledger).
  3. Implement automatic demotion on anomaly detection or calibration drift.
- **Verification**: `pytest tests/reva/unit/graffin/test_autonomy.py`
- **Done-When**:
  - `T-GRF-003.D01`: Attempting graph mutation under L0 raises `PermissionDeniedError`.
  - `T-GRF-003.D02`: Brier score $> 0.15$ triggers immediate automatic demotion to L1.

#### Task `T-GRF-004`: Consequence Budget ($\kappa$) & Blast Radius Calculator
- **File**: `reva/agents/graffin/consequence_budget.py`
- **Requirements**: Invariant C03
- **Actions**:
  1. Implement `ConsequenceBudgetTracker` tracking remaining budget $\kappa \in [0, 10000]$.
  2. Implement `BlastRadiusCalculator`: estimates affected vertex count and downstream dependency impact using BFS traversal.
  3. Cost function: $\text{Cost}(action) = 1 + \log_2(1 + \text{affected\_nodes}) \cdot \text{RiskMultiplier}$.
  4. If cost exceeds remaining $\kappa$, pause and request escalation.
- **Verification**: `pytest tests/reva/unit/graffin/test_consequence_budget.py`
- **Done-When**:
  - `T-GRF-004.D01`: Action sequences exceeding $\kappa$ budget are blocked and logged.
  - `T-GRF-004.D02`: Budget resets cleanly at the start of each authorized epoch.

#### Task `T-GRF-005`: Dual-Key Cryptographic Governance Engine
- **File**: `reva/agents/graffin/dual_key.py`
- **Requirements**: Invariant C04
- **Actions**:
  1. Implement dual-key gate for Risk Tier R3 and R4 operations.
  2. Verify dual signatures: Key 1 (Graffin Ed25519) + Key 2 (Human Operator Ed25519).
  3. Validate human signature against registered operator keys in `reva_keys`.
- **Verification**: `pytest tests/reva/unit/graffin/test_dual_key.py`
- **Done-When**:
  - `T-GRF-005.D01`: High-risk operation with only Graffin signature is rejected.
  - `T-GRF-005.D02`: High-risk operation with both valid signatures executes cleanly.

---

### Phase GRF-P2: External Tamper-Proof Evaluators

#### Task `T-GRF-006`: External Calibration & ECE Judge
- **File**: `reva/agents/graffin/evaluators/calibration_judge.py`
- **Requirements**: §4, Invariant C09
- **Actions**:
  1. Implement isolated `CalibrationJudge` comparing Graffin's stated confidence vs. ground truth outcomes.
  2. Compute Brier score: $\text{BS} = \frac{1}{N}\sum (f_t - o_t)^2$.
  3. Compute Expected Calibration Error (ECE) across 10 confidence bins.
  4. Write evaluation report to append-only storage.
- **Verification**: `pytest tests/reva/unit/graffin/test_calibration_judge.py`
- **Done-When**:
  - `T-GRF-006.D01`: Judge calculates exact Brier score and ECE from evaluation fixture.
  - `T-GRF-006.D02`: Brier score $> 0.15$ triggers demotion hook.

#### Task `T-GRF-007`: Regression Sentinel & In-Memory Isolation Sandbox
- **File**: `reva/agents/graffin/evaluators/regression_sentinel.py`
- **Requirements**: §4
- **Actions**:
  1. Implement `RegressionSentinel`: clones target graph state to in-memory temporary store.
  2. Applies Graffin's proposed mutation in sandbox.
  3. Executes the 100 gold-standard regression queries.
  4. Verifies $0\%$ query regression before granting commit approval.
- **Verification**: `pytest tests/reva/unit/graffin/test_regression_sentinel.py`
- **Done-When**:
  - `T-GRF-007.D01`: Proposed mutation causing query regression is rejected with detailed diff.
  - `T-GRF-007.D02`: Clean mutation passes sentinel check in $< 2.0\text{ s}$.

---

### Phase GRF-P3: Autonomic Maintenance & Performance Optimization Engines

#### Task `T-GRF-008`: Autonomic Health & Doctor Daemon
- **File**: `reva/agents/graffin/engines/doctor_daemon.py`
- **Requirements**: `GRF-OPS-001`
- **Actions**:
  1. Implement hourly diagnostic loop executing SQLite PRAGMA checks, Merkle STH audits, and CAS blob validation.
  2. Automatically heal transient stalls: restart hung outbox workers, drain stale temporary files.
- **Verification**: `pytest tests/reva/unit/graffin/test_doctor_daemon.py`
- **Done-When**:
  - `T-GRF-008.D01`: Injected SQLite foreign key violation is detected and reported.
  - `T-GRF-008.D02`: Merkle tree consistency verified without manual intervention.

#### Task `T-GRF-009`: Graph Performance Governor & Index Optimizer
- **File**: `reva/agents/graffin/engines/performance_governor.py`
- **Requirements**: `GRF-OPS-002`
- **Actions**:
  1. Monitor query execution plans and identify full-table scans.
  2. Generate SQLite `CREATE INDEX` proposals for hot predicates.
  3. Apply indexes under Autonomy L3/L4 during idle windows.
  4. Execute non-blocking graph vacuuming.
- **Verification**: `pytest tests/reva/perf/test_performance_governor.py`
- **Done-When**:
  - `T-GRF-009.D01`: Slow query detection triggers automated index creation.
  - `T-GRF-009.D02`: Query latency improves by $\ge 25\%$ post-indexing.

---

### Phase GRF-P4: Knowledge Curation & Schema Evolution Engines

#### Task `T-GRF-010`: Autonomous Knowledge Gap Hunter & Probe Synthesizer
- **File**: `reva/agents/graffin/engines/gap_hunter.py`
- **Requirements**: `GRF-OPS-003`
- **Actions**:
  1. Scan graph boundaries for partial coverage or unknown endpoints.
  2. Synthesize safe, read-only HTTP probes (`HEAD`, `OPTIONS`, `GET /health`).
  3. Execute probes and issue `reva.pred.boundary_observed` warrants upon success.
- **Verification**: `pytest tests/reva/unit/graffin/test_gap_hunter.py`
- **Done-When**:
  - `T-GRF-010.D01`: Gaps are scanned and safe probes executed without side effects.
  - `T-GRF-010.D02`: Valid probe responses resolve knowledge gaps in REVA store.

#### Task `T-GRF-011`: Contradiction Arbiter & Quarantine Manager
- **File**: `reva/agents/graffin/engines/contradiction_arbiter.py`
- **Requirements**: `GRF-OPS-004`
- **Actions**:
  1. Detect conflicting warrants sharing `(tenant_id, subject_key, predicate)`.
  2. Apply precedence: `human_attested > controlled_execution > runtime_observed > source_system_record`.
  3. Move contradicted items into quarantine and update downstream coverage metrics.
- **Verification**: `pytest tests/reva/unit/graffin/test_contradiction_arbiter.py`
- **Done-When**:
  - `T-GRF-011.D01`: Conflicting warrants are resolved or quarantined according to rules.
  - `T-GRF-011.D02`: Graph queries do not return quarantined contradicted triples.

#### Task `T-GRF-011B`: Autonomous Git Repository Ingestion & Graph Synthesis Loop
- **File**: `reva/agents/graffin/engines/repo_ingest_loop.py`
- **Requirements**: `GRF-OPS-004`, `REVA-AB-014`, `REVA-AB-015`, `REVA-SEC-013`
- **Actions**:
  1. Receive repository submission event or polling trigger with remote Git URL (GitHub, GitLab, Bitbucket).
  2. Invoke REVA `GitRepositoryCloner` (`reva/extract/repo/git_cloner.py`) inside an isolated container sandbox with `--depth 1` shallow clone and quota limits ($\le 5\text{ GiB}$, $\le 300\text{s}$).
  3. Execute deterministic pure-Python extractors for AST boundaries, native binaries (`.so`), mobile packages, and firmware partitions.
  4. Project discovered services, endpoints, and resources into the Knowledge Graph (GL0–GL3).
  5. Parse ADRs and Conventional Commits, projecting decision traces and precedents into the Wisdom Graph (GW).
  6. Route any required semantic synthesis through `EgressSecurityGate` (`reva/core/egress_gate.py`), ensuring 100% DLP redaction, structural pseudonymization, and zero raw proprietary code egress to external LLMs.
- **Verification**: `pytest tests/reva/integration/graffin/test_repo_ingest_loop.py`
- **Done-When**:
  - `T-GRF-011B.D01`: Submitting a Git URL clones the repo and populates both Knowledge Graph and Wisdom Graph.
  - `T-GRF-011B.D02`: Zero proprietary code or unredacted secrets leave the boundary to an LLM.

---

### Phase GRF-P5: Continuous REVA Proof-of-Done Engine & Perpetual Worker Lifecycle

#### Task `T-GRF-012`: Git Change Watcher & Owner Digest Staleness Monitor
- **File**: `reva/agents/graffin/engines/staleness_daemon.py`
- **Requirements**: `GRF-OPS-005`
- **Actions**:
  1. Watch local git worktree / commit hooks for modified files.
  2. Recompute owner digests across all bound obligations.
  3. Mark changed obligations `stale` in `reva_obligations`.
- **Verification**: `pytest tests/reva/unit/graffin/test_staleness_daemon.py`
- **Done-When**:
  - `T-GRF-012.D01`: Modifying an owner file automatically marks linked obligations `stale`.

#### Task `T-GRF-013`: Autonomous Verifier Runner & Proof-of-Done Ledger Issuer
- **File**: `reva/agents/graffin/engines/verifier_orchestrator.py`
- **Requirements**: `GRF-OPS-005`
- **Actions**:
  1. For all stale obligations, spawn isolated sandbox runner (`reva.sandbox.runner`).
  2. Collect JUnit XML and coverage metrics.
  3. Run pure 11-step closure evaluation (`evaluate_closure`).
  4. If all obligations close, construct and sign canonical ledger (`ldg1_...`).
  5. Update `reva-tracker.html` data block.
- **Verification**: `pytest tests/reva/unit/graffin/test_verifier_orchestrator.py`
- **Done-When**:
  - `T-GRF-013.D01`: Autonomous pipeline runs, evaluates closures, and signs canonical ledger.
  - `T-GRF-013.D02`: `reva-tracker.html` updates with verified ledger ID.

#### Task `T-GRF-014`: REST API, MCP Tools & CLI Framework
- **File**: `reva/api/routes_graffin.py`, `reva/mcp/server.py`, `reva/cli/graffin_cli.py`
- **Requirements**: §7.1, §7.2, §7.3
- **Actions**:
  1. Implement FastAPI routes for status, kill, autonomy, proposal review, and doctor.
  2. Implement FastMCP tools (`graffin_status`, `graffin_trigger_audit`, `graffin_propose_optimization`, `graffin_emergency_abort`).
  3. Implement Click CLI group `graffin` with commands `status`, `autonomy`, `heal`, `kill`.
- **Verification**: `pytest tests/reva/unit/graffin/test_graffin_interfaces.py`
- **Done-When**:
  - `T-GRF-014.D01`: REST, MCP, and CLI commands execute and report status cleanly.

#### Task `T-GRF-015`: Perpetual Worker Lifecycle Supervisor & Daemon Service
- **File**: `reva/agents/graffin/daemon.py`
- **Requirements**: `GRF-OPS-006`
- **Actions**:
  1. Implement `GraffinDaemon`: orchestrates all engines in an asynchronous, non-blocking perpetual event loop.
  2. Integrates with systemd / Windows Service / Docker container entrypoint.
  3. Emits Prometheus telemetry metrics continuously.
- **Verification**: `pytest tests/reva/unit/graffin/test_daemon_lifecycle.py`
- **Done-When**:
  - `T-GRF-015.D01`: Daemon starts, runs 3 complete audit cycles, and halts cleanly on SIGTERM.

---

## 3. Seven-Level Verification Protocol for Graffin

```
+----------------------------------------------------------------------------------------------------+
|  Level 1: Syntactic & Type Correctness                                                             |
|  - Pydantic v2 strict models, constitution schema validation, RFC 8785 canonical hashing           |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|  Level 2: Unit Contract Execution                                                                  |
|  - Deterministic tests covering all 15 tasks under tests/reva/unit/graffin/, 100% pass             |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|  Level 3: Safety & Performance Latencies                                                           |
|  - Kill switch termination <= 500ms; memory footprint <= 8 GiB; query latency improvement >= 25%   |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|  Level 4: Adversarial Red-Teaming & Anti-Gaming                                                    |
|  - Constitution tamper rejection (exit 65); prompt-injection cannot alter autonomy or evaluators   |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|  Level 5: External Evaluator Gating                                                                |
|  - Brier score <= 0.15, ECE <= 0.12, 0% regression on 100 benchmark queries                        |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|  Level 6: REVA Proof-of-Done & Closure                                                             |
|  - All 15 Graffin obligations closed, signed DSSE attestation, signed canonical ledger (ldg1_...)  |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|  Level 7: Perpetual Autonomous Worker Integration                                                  |
|  - Clean daemon execution, zero memory leaks over 24h soak, Prometheus telemetry streaming        |
+----------------------------------------------------------------------------------------------------+
```

---

## 4. Final Exit Gate Checklist

Before Graffin can be promoted to active perpetual status:
- [ ] `forbid_placeholders.py` passes with 0 violations across all Graffin modules.
- [ ] `check_depth_markers.py` passes across all `tests/reva/unit/graffin/`.
- [ ] Constitution hash verified in WORM storage.
- [ ] Kill switch latency verified $\le 500\text{ ms}$ on both Windows and Linux.
- [ ] External evaluator confirms Brier score $\le 0.15$ and 0% query regression.
- [ ] Canonical signed ledger `docs/reva/graffin-ledger.json` emitted with status `complete=True`.
