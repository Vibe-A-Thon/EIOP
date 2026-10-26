# Chapter 6 — Agents, Loops, and Orchestration

This chapter covers every way EOIP runs agentic work: the governed agent runtime
(`packages/eoip/agents/runtime.py`), the 17+ specialist agents in the production
catalog, the agent-architecture playground (`/api/v1/agentarch/*`), agent-to-agent
(A2A) messaging, the deterministic loops library (`/api/v1/loops/*`), the reasoning
strategy layer (`/api/v1/reasoning/*`), durable execution workflows
(`/api/v1/execution/*`), and the MCP server (`apps/mcp/main.py`) that exposes all of
this to AI clients.

Everything below is grounded in the source. Where a behavior is defined in code but
was not exercised against a live server while writing this chapter, it is marked
**[not runtime-verified]**.

## Index

1. [The governed agent runtime](#1-the-governed-agent-runtime)
2. [Running agents via the API (`/api/v1/agents/*`)](#2-running-agents-via-the-api)
3. [Proposals: approve / reject](#3-proposals-approve--reject)
4. [Trace-impact shortcut](#4-trace-impact-shortcut)
5. [Analytics and semantic-index agents](#5-analytics-and-semantic-index-agents)
6. [The specialist agent catalog](#6-the-specialist-agent-catalog)
7. [Agent architectures (`/api/v1/agentarch/*`)](#7-agent-architectures-apiv1agentarch)
8. [A2A messaging](#8-a2a-messaging)
9. [The loops library (`/api/v1/loops/*`)](#9-the-loops-library-apiv1loops)
10. [Loop approvals: park / decide](#10-loop-approvals-park--decide)
11. [Reasoning strategies and working memory](#11-reasoning-strategies-and-working-memory)
12. [Execution workflows (`/api/v1/execution/*`)](#12-execution-workflows-apiv1execution)
13. [The MCP server](#13-the-mcp-server)
14. [Human approval patterns — where approvals appear](#14-human-approval-patterns)

---

## 1. The governed agent runtime

**What it does.** Every agent in EOIP runs inside `AgentRuntime`
(`packages/eoip/agents/runtime.py`), which enforces contracts, budgets, read-only
tool access, a knowledge firewall, a per-agent circuit breaker, and produces a
replayable XAI trace plus an evidence-linked explanation for every run.

**Key mechanics (from the source):**

- **READ_TOOLS allowlist** — `runtime.py:42` defines the only tools an agent may
  register: `search, entity, path, impact, lineage, quality, ontology,
  connector_status, evidence, similarity, community, anomaly, test_coverage,
  incident_correlation`. `AgentRegistry.register` raises `ValueError` if an agent
  declares anything outside this set. Note: the tool *registry* also carries three
  PR tools (`list_prs`, `get_pr_impact`, `triage_prs` — `tools.py:162-167`), but
  agents cannot be registered with them.
- **Budgets** — each contract carries `AgentBudgets` (`max_steps`, `max_seconds`,
  plus `max_tool_calls`, `max_recursion`, `max_context_items` from
  `eoip.contracts.agent`). Budgets you send in a request are **clamped down** to the
  contract maximum (`_clamped_budgets`, `runtime.py:523`) — you can only ever ask
  for *less*.
- **Circuit breaker** — after 3 consecutive `FAILED`/`CANCELLED` runs for the same
  agent (`failure_threshold=3`, `runtime.py:221`), further runs return
  `status="DENIED"` with summary `"Circuit breaker is open for <agent_id>"` until a
  run succeeds.
- **Dry-run** — `AgentRunRequest.dry_run` is forwarded into every `ToolRequest`
  (`runtime.py:164`); read tools are unaffected (they never mutate anyway).
- **Knowledge firewall** — the goal text is scanned before execution
  (`firewall.py`): secrets are replaced with `[REDACTED]`, PII with
  `[REDACTED-PII]`, and rule decisions (`KFW-SECRET-REDACTION`, `KFW-PII-REDACTION`,
  `KFW-RESTRICTED-DATA`, `KFW-PROMPT-INJECTION`, `KFW-UNTRUSTED-DATA`) are recorded
  in the trace's `CONTEXT` phase.
- **Trace phases** — every run emits events in phases `RECEIVE → CONTEXT → PLAN →
  VALIDATE → EXECUTE → EVALUATE → EXPLAIN → AUDIT → FINISH`, persisted via
  `AgentTraceStore`, and the run itself is upserted as an `AgentRun` graph vertex.

**Errors and recovery.** A run never throws at the API layer for agent-level
problems; it returns `status` one of `SUCCEEDED | PARTIAL | FAILED | DENIED |
CANCELLED` with `warnings` and an `explanation` envelope. `DENIED` means unknown /
disabled agent, open circuit breaker, or budget violation. `CANCELLED` means the
time budget was hit (`"Agent execution stopped at its time budget."`).

---

## 2. Running agents via the API

Routes live in `apps/api/main.py:1512-1634`. All require an authenticated principal
(`Authorization: Bearer <token>`).

### List agents

**What it does.** Returns every registered agent contract.

**How to access.** `GET /api/v1/agents`

**Step by step.**

```bash
curl -s http://localhost:8000/api/v1/agents \
  -H "Authorization: Bearer $EOIP_TOKEN"
```

**Response.** `{"agents": [AgentContract, ...]}` — each contract includes
`agent_id`, `version`, `agent_type`, `purpose`, `allowed_tools`,
`prohibited_tools` (`["write_graph", "delete_graph", "deploy", "send_message"]`),
`model_policy`, `memory_policy`, `risk_level`, `human_control`, `budgets`.

### Run an agent

**What it does.** Executes one governed agent run.

**How to access.** `POST /api/v1/agents/{agent_id}/runs`

**Step by step.**

```bash
curl -s -X POST http://localhost:8000/api/v1/agents/DataQuality/runs \
  -H "Authorization: Bearer $EOIP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Check provenance coverage for tenant t-001",
    "context_refs": ["urn:eoip:service:checkout"],
    "budgets": {"max_steps": 8, "max_seconds": 20},
    "dry_run": true,
    "synthesize": false
  }'
```

Request model (`AgentRunRequest`, `main.py:162`): `goal` (1–4096 chars),
`context_refs` (≤100), `budgets` (dict), `dry_run` (bool), `synthesize` (bool,
GraphInvestigator only), `memory_ttl_seconds` (≤ `MAX_TTL_SECONDS = 30*86400`, i.e.
30 days — `memory.py:22`).

**Response.** An `AgentResult`: `request_id`, `run_id`, `status`, `summary`,
`evidence_refs`, `tool_calls` (each with `tool_call_id`, `tool_name`, `status`,
`risk_level`, `duration_ms`, `arguments_digest`), `proposals`, `warnings`,
`explanation` (`decision_summary`, `evidence_refs`, `rule_decisions`,
`confidence`, `uncertainty`).

**Errors and recovery.**
- `404 "Agent not found"` — bad `agent_id` (also returned when the runtime denies
  with `Unknown agent`). List agents first.
- `401` — no authenticated principal.
- `422 "Task memory TTL exceeds the configured maximum"` — lower
  `memory_ttl_seconds`.
- `status="DENIED"` with `"Circuit breaker is open for DataQuality"` — wait for a
  successful run or restart the API process (failure counters are in-memory).

### Inspect a run

- `GET /api/v1/agents/runs/{run_id}` → `{"result": ..., "trace": ...}` (404 `"Agent
  run not found"`).
- `GET /api/v1/agents/runs/{run_id}/memory` → scoped task-memory record; only
  exists for contracts with `memory_policy="APPROVED"` (currently only
  `TraceImpact` — `catalog.py:47`). 404 `"Agent task memory not found"` otherwise;
  503 if memory storage is unavailable.
- `GET /api/v1/agents/runs/{run_id}/explanation` → the `ExplanationEnvelope`
  (404 `"Agent explanation not found"`).

---

## 3. Proposals: approve / reject

**What it does.** Agents never write to the graph. The one `WRITING`-type agent,
`KnowledgeCurator`, emits inert `ChangeProposal` objects (`"Approval changes
proposal state only; applying a mutation remains a separate, explicitly authorised
platform operation."` — `proposals.py:1-5`). Proposals persist to
`$EOIP_DATA_DIR/state/agent-proposals.json` (default `.data/state/agent-proposals.json`).

**How to access.**
- `GET /api/v1/agents/proposals?status=PENDING`
- `POST /api/v1/agents/proposals/{proposal_id}/approve`
- `POST /api/v1/agents/proposals/{proposal_id}/reject`

**Step by step.**

```bash
# 1. Run the curator to generate proposals
curl -s -X POST http://localhost:8000/api/v1/agents/KnowledgeCurator/runs \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{"goal": "Find provenance gaps in tenant t-001"}'

# 2. List pending proposals
curl -s "http://localhost:8000/api/v1/agents/proposals?status=PENDING" \
  -H "Authorization: Bearer $EOIP_TOKEN"

# 3. Approve one
curl -s -X POST http://localhost:8000/api/v1/agents/proposals/<proposal_id>/approve \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{"actor_id": "sindhuja.reviewer"}'
```

**Response.** The updated proposal: `status` flips to `APPROVED`/`REJECTED`, plus
`approved_by` and `decided_at`. Proposal fields: `proposal_id`, `run_id`,
`proposed_by`, `operation` (e.g. `REVIEW_PROVENANCE`), `target_ref`, `patch`,
`rationale`, `evidence_refs`, `risk_level`.

**Errors and recovery.** Approving requires the authorization decision
`agents:approve` (`main.py:1596-1607`): `401` without a principal, `403 "Proposal
review permission required"` if the policy enforcer denies, `503` if the policy
service is unavailable. `404 "Proposal not found"` for a bad id; `409 "Proposal has
already been decided"` on a second decision — decisions are final. `GET` with an
invalid `status` gives `422 "Invalid proposal status"` (valid: `PENDING`,
`APPROVED`, `REJECTED`, `EXPIRED`).

---

## 4. Trace-impact shortcut

**What it does.** Runs the deterministic `TraceImpact` agent over one canonical
entity without constructing a full agent request.

**How to access.** `POST /api/v1/agents/trace-impact`

**Step by step.**

```bash
curl -s -X POST http://localhost:8000/api/v1/agents/trace-impact \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{"canonical_id": "urn:eoip:service:checkout", "max_depth": 4}'
```

`max_depth` is clamped to 1–8 (`TraceRequest`, `main.py:157`).

**Response.** `{agent_id, run_id, status, summary, evidence_refs, tool_calls,
explanation, generation: "deterministic", partial}` (`main.py:1752`).

**Errors and recovery.** `404 "Entity not found"` when the summary reports the
entity is missing. `status="PARTIAL"` with warning `"Traversal stopped before
source resolution"` means the traversal time budget expired — retry with a smaller
`max_depth`.

---

## 5. Analytics and semantic-index agents

**What it does.** Two direct-execution endpoints in `apps/api/extended.py:1008-1034`
that run `GraphAnalyticsAgent` / `SemanticIndexAgent` **outside** the governed
runtime (no trace, no firewall — they call `agent.execute(request, store)`
directly). Treat their output as diagnostic, not audited.

**How to access.**
- `POST /api/v1/agents/analytics`
- `POST /api/v1/agents/semantic-index`

**Step by step.**

```bash
curl -s -X POST http://localhost:8000/api/v1/agents/analytics \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{"algorithm": "all", "context_refs": ["urn:eoip:service:checkout"], "budgets": {"max_steps": 10}}'
```

Request model (`AgentAnalyticsRequest`, `extended.py:427`): `algorithm` (default
`"all"`), `context_refs`, `budgets`.

**Response.** The agent's result model dump (or `{status, summary, data}`).
**[not runtime-verified]** which algorithms `GraphAnalyticsAgent` accepts; pass
`"all"` for the swarm behavior described by the field description.

---

## 6. The specialist agent catalog

Built by `build_agent_registry()` in `packages/eoip/agents/catalog.py`. The task
brief mentions "11 specialist agents"; the code actually registers **18**. All are
deterministic (`model_policy="deterministic"`) except `GraphInvestigator`
(`optional_local_grounded`). All are `risk_level="R0"` / `human_control="READ_ONLY"`
except where noted.

| `agent_id` | Type | What it does (from the source) |
|---|---|---|
| `TraceImpact` | GOAL_BASED | Bounded impact traversal with evidence paths (`trace_impact.py`); the only agent with `memory_policy="APPROVED"` |
| `ChangeImpact` | GOAL_BASED | Blast radius of a proposed/observed change (subclasses TraceImpact) |
| `IncidentInvestigation` | MODEL_BASED | Correlate incidents with changes, deployments, evidence |
| `IncidentCorrelation` | MODEL_BASED | Find incident correlation chains |
| `DataQuality` | VALIDATOR | Find records missing canonical ids or provenance edges |
| `OntologyReview` | REVIEWER | Check labels/edge endpoints against the ontology manifest |
| `ConnectorDiagnosis` | MODEL_BASED | Summarize failed/partial `IngestionRun`s by source system |
| `DocumentationFreshness` | VALIDATOR | Find stale/disconnected `Document` vertices |
| `EvidenceVerification` | VALIDATOR | Find edges lacking `source_ref`/`evidence_key` |
| `GraphInvestigator` | RAG | Answer a graph question for one `context_refs[0]` entity; optional local-model synthesis via `synthesize=true` |
| `ArchitectureConformance` | REVIEWER | Find `Dependency` vertices with no ownership/evidence edges |
| `QueryOptimization` | UTILITY_BASED | Report largest vertex populations for bounded query planning |
| `AnomalyDetection` | MODEL_BASED | Structural graph anomalies (`anomaly.py`) |
| `BlastRadius` | GOAL_BASED | Rank downstream blast radius of an entity |
| `CommunityAnalysis` | MODEL_BASED | Identify graph communities and boundaries |
| `Similarity` | MODEL_BASED | Find structurally similar entities |
| `TestCoverage` | VALIDATOR | Requirements/work items without test coverage |
| `KnowledgeCurator` | WRITING, **R2**, `human_control="PROPOSE_ONLY"` | Runs DataQuality then emits up to 20 inert `REVIEW_PROVENANCE` proposals |

**Errors and recovery.** `GraphInvestigator` fails with `"GraphInvestigator
requires a canonical entity context."` if you don't pass `context_refs`. Agents
returning `PARTIAL` with findings is normal — it means "issues found, human review
required", not a crash.

There is also a higher-level natural-language router, `POST /api/v1/agents/query`
and `GET /api/v1/agents/types` (`apps/api/app.py:1668-1677`, backed by
`eoip.graph.agent_router.AgentRouter`), which maps a free-text query onto an agent
type. **[not runtime-verified]** for this chapter.

---

## 7. Agent architectures (`/api/v1/agentarch/*`)

Router: `packages/eoip/agentarch/router.py`, wired in `apps/api/extended.py:1501`.

### Catalog

**What it does.** Lists every architecture *class* the package implements —
18 classical, 15 reasoning, 27 enterprise capability classes, plus the 16 org
patterns.

**How to access.** `GET /api/v1/agentarch/catalog`

```bash
curl -s http://localhost:8000/api/v1/agentarch/catalog -H "Authorization: Bearer $EOIP_TOKEN"
```

**Response.** `{"classical": [...], "reasoning": [...], "enterprise": [...],
"patterns": [...]}`. Reasoning entries include `"react"`, `"plan-execute"`,
`"tree-of-thought"`, `"hypothesis-testing"`, `"verification"`, etc.
(`architecture_catalog()`, `router.py:23-76`).

### Run one architecture

**What it does.** `POST /api/v1/agentarch/run` executes an architecture through the
governed runtime. **Honesty note:** the default runtime registered by
`build_agentarch_router(store)` (`router.py:79-92`) contains only **four** agents:
`urn:eoip:agentarch:reactive`, `urn:eoip:agentarch:react`,
`urn:eoip:agentarch:discovery`, `urn:eoip:agentarch:ontology`. Any other catalog
entry returns a governed `DENIED` result with `"Unknown agent: ..."` — the catalog
is a class inventory, not a runnable registry. **[not runtime-verified]** beyond
reading the wiring.

**Step by step — three concrete examples.**

```bash
# 1. ReActAgent — registered, works end to end
curl -s -X POST http://localhost:8000/api/v1/agentarch/run \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{"agent_id": "urn:eoip:agentarch:react",
       "goal": "Reason about the checkout service dependencies",
       "actor_id": "sindhuja", "metadata": {}}'

# 2. HypothesisTestingAgent — in the catalog but NOT registered in the default
#    runtime; this returns status DENIED ("Unknown agent") via the API today.
#    Run it in-process instead:
.venv/Scripts/python - <<'PY'
from eoip.agentarch.reasoning import HypothesisTestingAgent
print(HypothesisTestingAgent.architecture)   # "hypothesis-testing"
PY

# 3. VerificationAgent — same situation (architecture = "verification").
```

Request model (`ArchRunRequest`): `agent_id`, `goal`, `actor_id` (default `"api"`),
`metadata`. Extra fields are rejected (`extra="forbid"` → HTTP 422).

**Response.** A full governed `AgentResult` dump (same shape as §2).

### Coordinate an org pattern

**What it does.** `POST /api/v1/agentarch/coordinate` runs one of the 16
coordination patterns from `org.py` over participant agent ids.

**Step by step.**

```bash
curl -s -X POST http://localhost:8000/api/v1/agentarch/coordinate \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{"pattern": "supervisor-worker",
       "participants": ["urn:eoip:agentarch:react", "urn:eoip:agentarch:discovery"],
       "goal": "Investigate incident EOIP-123 affecting checkout"}'
```

Patterns (`PATTERNS`, `org.py:480`): `supervisor-worker`, `manager-specialist`,
`leader-follower`, `blackboard`, `hierarchical-teams`, `federated`, `market-based`,
`contract-net`, `negotiation`, `voting`, `ensemble`, `mesh`, `event-driven`,
`pipeline`, `handoff`, `mixture-of-agents` (exact keys are the `pattern` class
attributes; see the catalog's `patterns` list).

**Response.** Pattern-specific dict, always with `pattern`, `status`
(`SUCCEEDED|PARTIAL|FAILED`), and `child_results`; `supervisor-worker` adds
`assignments`, `blackboard` adds the shared `blackboard` state.

**Errors and recovery.** `404 "Unknown pattern: <name>"` — use a key from the
catalog. Participants are capped at 12 (`CoordinateRequest`, `router.py:104`).

---

## 8. A2A messaging

**What it does.** Agent-to-agent envelopes (`a2a.py`) with W3C-style `traceparent`
propagation (`00-<trace-id>-<parent-id>-01`) and capability discovery cards.

**How to access.**
- `POST /api/v1/agentarch/a2a/send`
- `GET /api/v1/agentarch/a2a/capabilities/{agent_id}`

**Step by step.**

```bash
# Discover capabilities
curl -s http://localhost:8000/api/v1/agentarch/a2a/capabilities/urn:eoip:agentarch:react \
  -H "Authorization: Bearer $EOIP_TOKEN"

# Send a TASK message
curl -s -X POST http://localhost:8000/api/v1/agentarch/a2a/send \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{"sender_id": "urn:eoip:agentarch:react",
       "recipient_id": "urn:eoip:agentarch:discovery",
       "message_type": "TASK",
       "content": {"goal": "Discover services related to checkout"},
       "traceparent": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"}'
```

`message_type` is one of `TASK | RESPONSE | CANCEL | CAPABILITY_QUERY | HEARTBEAT`.
The bus dispatches `TASK` to the runtime, answers `CAPABILITY_QUERY` from the
registered `CapabilityCard`s, and returns a `RESPONSE` envelope.

**Errors and recovery.** `404` if the recipient is unknown. `422` if
`traceparent` is missing (required field) or you send extra fields.

---

## 9. The loops library (`/api/v1/loops/*`)

Router: `packages/eoip/loops/router.py`. Execution is in-process and
deterministic — **you supply the step script**; no LLM is involved.

### Catalog

**How to access.** `GET /api/v1/loops/catalog`

```bash
curl -s http://localhost:8000/api/v1/loops/catalog -H "Authorization: Bearer $EOIP_TOKEN"
```

**Response.** `{loops: [{loop_name, phases, runner}], human_patterns: [...]}` —
23 loops (`LOOP_PHASES`, `drivers.py:42-65`), e.g. `ooda`
(`observe/orient/decide/act`), `react` (`reason/act`), `plan_execute_verify`,
`hypothesis_experiment_evaluate`, `graph_traversal`, `safety_validation`,
`retry_backoff_recovery`, `consensus_reconciliation`. `runner` names the Python
function (e.g. `run_ooda_loop`).

### Run a loop script

**What it does.** Executes one bounded run of a named loop. Each script step
mutates state and emits a signal; the driver enforces iteration/time/token/cost
budgets, cycle detection, and JSON checkpoints (`.data/loops` by default).

**How to access.** `POST /api/v1/loops/run/{loop_name}`

**Step by step.**

```bash
curl -s -X POST http://localhost:8000/api/v1/loops/run/react \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "config": {"max_iterations": 8, "time_budget_seconds": 30,
               "token_budget": 5000, "cost_budget": 1.0},
    "initial_state": {"issue": "EOIP-123", "service": "checkout"},
    "script": [
      {"set_state": {"thought": "inspect checkout latency"}, "increment": "n",
       "signal": "continue", "tokens_used": 120, "note": "reason step 1"},
      {"set_state": {"action": "query graph"}, "signal": "continue", "tokens_used": 80},
      {"set_state": {"conclusion": "db connection pool saturated"},
       "signal": "complete", "note": "done"}
    ]
  }'
```

`ScriptStep` fields (`router.py:55`): `set_state`, `increment`, `signal`
(`continue|complete|...`, see `StepSignal` in `core.py:118`), `tokens_used`,
`cost_used`, `note`, `goto_phase`, `await_approval`. `LoopConfig` fields
(`core.py`): `max_iterations` (default 32), `time_budget_seconds` (60),
`token_budget` (100 000), `cost_budget` (100.0), `idempotency_key`,
`checkpoint_dir`, `detect_cycles`, `checkpoint_every`, plus `resume_run_id` /
`resume_approved` on the request envelope for resuming parked runs.

**Response.** A `LoopResult`: `run_id`, `loop_name`, `status`
(`completed|converged|failed|awaiting_approval|...`), final `state`, `metrics`
(iterations, tokens, cost, error category), and the termination outcome.

**Errors and recovery.** `404 {"detail": "unknown loop: <name>"}`; `409` with the
error category when the loop fails (e.g. budget exhausted, cycle detected);
`404 "no checkpoint for <run_id>"` when resuming an unknown run.

---

## 10. Loop approvals: park / decide

**What it does.** A step can return `await_approval` (a dict describing the gate).
The driver then parks the run with status `awaiting_approval` and checkpoints it;
a human decision resumes or kills it. Decisions use the 15 human-participation
patterns (`HumanPattern`, `approval.py:35`: `human_before_execution`,
`human_at_checkpoint`, `human_at_decision`, `human_at_commit`, `human_at_handoff`,
`human_in_review`, `human_in_verification`, `human_in_validation`,
`human_in_active_learning`, `human_in_feedback`, `human_in_escalation`,
`human_in_override`, `human_in_recovery`, `human_in_adversarial_review`,
`multi_human_approval`).

**How to access.**
- `GET /api/v1/loops/approvals/pending`
- `POST /api/v1/loops/approvals/decide`

**Step by step (park then decide).**

```bash
# 1. Run a loop whose step 2 parks for approval
curl -s -X POST http://localhost:8000/api/v1/loops/run/safety_validation \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{"script": [
        {"signal": "continue", "note": "propose change for EOIP-123"},
        {"signal": "continue",
         "await_approval": {"action": "agents:approve", "pattern": "human_at_decision"}}
      ]}'
# -> status: "awaiting_approval", note the run_id

# 2. Record the human decision
curl -s -X POST http://localhost:8000/api/v1/loops/approvals/decide \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{"request_id": "<request_id from the parked run>",
       "approver": "sindhuja.reviewer", "roles": ["release-manager"],
       "decision": "approve",
       "evidence": {"ticket": "EOIP-123"},
       "reason": "Change reviewed in CAB"}'
# -> {"recorded": true, "request_id": "...", "decision": "approve"}

# 3. Resume the parked run from its checkpoint
curl -s -X POST http://localhost:8000/api/v1/loops/run/safety_validation \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{"resume_run_id": "<run_id>", "resume_approved": true, "script": []}'
```

`decision` is a `GateDecision`: `approve | deny | escalate`.

**Errors and recovery.** The default approval queue is `InMemoryApprovalQueue` —
pending gates **do not survive an API restart** unless the deployment wires a
persistent queue (check `apps/api/extended.py:1500`; a checkpoint store is wired,
the queue is in-memory). Denying resumes the run with the deny path
(`resume_approved: false`).

---

## 11. Reasoning strategies and working memory

Router: `packages/eoip/reasoning/router.py`, prefix `/api/v1/reasoning`.

### List and run strategies

**How to access.**
- `GET /api/v1/reasoning/strategies`
- `POST /api/v1/reasoning/strategies/{name}/run`
- `POST /api/v1/reasoning/select` (meta-reasoning: pick the best strategy, then run it)

**Step by step.**

```bash
curl -s http://localhost:8000/api/v1/reasoning/strategies -H "Authorization: Bearer $EOIP_TOKEN"
# {"strategies": ["react", "tot", "got", "best-first", "beam", "htn",
#                 "world-model", "neuro-symbolic", "causal", "probabilistic", "meta"]}

curl -s -X POST http://localhost:8000/api/v1/reasoning/strategies/react/run \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{"prompt": "Why is checkout latency elevated during EOIP-123?",
       "context": {"tenant_id": "t-001"},
       "max_steps": 8,
       "candidate_actions": ["query_graph", "read_logs"]}'

curl -s -X POST http://localhost:8000/api/v1/reasoning/select \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{"prompt": "Plan the migration of checkout to the new schema"}'
```

`ReasoningProblem` fields (`strategies.py:55`): `problem_id?`, `prompt`,
`context`, `max_steps` (default 16), `candidate_actions`, `causal_model`.

**Response.** A `ReasoningResult`: `result_id`, `strategy`, `status`
(`SUCCEEDED | MAX_STEPS | FAILED`), `answer`, `steps[]` (each with `step_index`,
`kind` — thought/action/observation/expansion/rollout/rule-check — `content`,
`score`, `parent`), `iterations`. These strategies are symbolic/simulated — they
do not call an LLM.

**Errors and recovery.** `404` for an unknown strategy name; `422` for a malformed
problem (`extra="forbid"`).

### Working memory, costs, evaluation references

- `POST /api/v1/reasoning/memory/working` — body `{"content": "...", "priority":
  0.8}`; returns `{item, evicted, used_tokens, token_budget}`. Token-budgeted:
  low-priority items are evicted when the budget is exceeded.
- `GET /api/v1/reasoning/memory/working` — snapshot of current items and usage.
- `GET /api/v1/reasoning/agentops/costs` — cost-ledger totals (`CostLedger`).
- `GET /api/v1/reasoning/evaluation/references` — trajectory-scorer reference
  data (`references`, `golden_tools`).

Note: this `WorkingMemory` is a per-router-instance in-memory store — contents are
lost on restart and are not shared with agent task memory (§2).

---

## 12. Execution workflows (`/api/v1/execution/*`)

Router: `packages/eoip/execution/router.py`; engine in `workflows.py`. Durable-ish
(event-sourced via an in-process `EventStore`), synchronous runner supporting
DAG dependencies, retries with backoff, long-running timers, human approval gates,
and saga compensation. **The engine and event store are in-process** — workflow
definitions and state do not survive an API restart **[not runtime-verified for
persistence]**.

**How to access (all under `/api/v1/execution`).**

| Method & path | Purpose |
|---|---|
| `POST /workflows` | register/validate a `WorkflowDefinition` (DAG checked) |
| `GET /workflows/{id}/state` | replayed instance state |
| `POST /workflows/{id}/run` | execute to completion |
| `POST /workflows/{id}/cancel` | cancel + skip pending steps |
| `POST /workflows/{id}/compensate` | saga compensation, reverse order |
| `POST /workflows/{id}/approve` | human-approval decision for a step |
| `GET /workflows/{id}/timers` | steps whose fire-at timer is due |
| `POST /queue/items` | enqueue prioritized work |
| `POST /queue/claim` | lease-based claim |
| `POST /queue/items/{id}/complete` | complete a leased item |
| `GET /streams/{id}/reconcile` | event-stream consistency report |

### Worked example — a checkout deploy with approval and compensation

```bash
# 1. Define the workflow
curl -s -X POST http://localhost:8000/api/v1/execution/workflows \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "wf-checkout-deploy-001",
    "name": "Checkout deploy for EOIP-123",
    "steps": [
      {"name": "build", "action": "build",
       "retry": {"max_attempts": 3, "backoff_seconds": 2.0},
       "compensation": "cleanup_build"},
      {"name": "approve_release", "action": "noop",
       "depends_on": ["build"], "requires_approval": true},
      {"name": "deploy", "action": "deploy",
       "depends_on": ["approve_release"], "timer_seconds": 0.0,
       "compensation": "rollback_deploy"}
    ]
  }'
# -> {"workflow_id": "wf-checkout-deploy-001", "steps": 3, "valid": true}

# 2. Run it — it will stop at the approval gate
curl -s -X POST http://localhost:8000/api/v1/execution/workflows/wf-checkout-deploy-001/run \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{"tenant_id": "t-001"}'

# 3. Grant the gate
curl -s -X POST http://localhost:8000/api/v1/execution/workflows/wf-checkout-deploy-001/approve \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{"step": "approve_release", "approved": true}'

# 4. Inspect state / due timers
curl -s http://localhost:8000/api/v1/execution/workflows/wf-checkout-deploy-001/state \
  -H "Authorization: Bearer $EOIP_TOKEN"
curl -s http://localhost:8000/api/v1/execution/workflows/wf-checkout-deploy-001/timers \
  -H "Authorization: Bearer $EOIP_TOKEN"

# 5. If something went wrong: compensate (runs cleanup_build / rollback_deploy)
curl -s -X POST http://localhost:8000/api/v1/execution/workflows/wf-checkout-deploy-001/compensate \
  -H "Authorization: Bearer $EOIP_TOKEN"

# 6. Queue a follow-up task and let a worker claim/complete it
curl -s -X POST http://localhost:8000/api/v1/execution/queue/items \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{"kind": "post-deploy-verify", "payload": {"service": "checkout"}, "priority": 5}'
curl -s -X POST http://localhost:8000/api/v1/execution/queue/claim \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{"owner": "worker-1"}'
curl -s -X POST http://localhost:8000/api/v1/execution/queue/items/<item_id>/complete \
  -H "Authorization: Bearer $EOIP_TOKEN" -H "Content-Type: application/json" \
  -d '{"owner": "worker-1"}'
```

**Response shapes.** Workflow endpoints return a `WorkflowState`: `workflow_id`,
plus per-step `StepState` (`name`, `status` — `PENDING|WAITING_TIMER|
WAITING_APPROVAL|RUNNING|SUCCEEDED|FAILED|COMPENSATED|SKIPPED`, `attempts`,
`approved`, `timer_fire_at`, `error`).

**Errors and recovery.**
- `422` at registration — duplicate step names, unknown `depends_on`, or a
  dependency cycle (`validate_dag`).
- `404 "unknown workflow <id>"` — definitions live in memory; re-register after
  restart.
- `409` on `cancel` of a terminal workflow, on `approve` for a step not in
  `WAITING_APPROVAL` (`"step X is not awaiting approval"`), or on completing a
  queue item leased by another owner.
- Steps with `timer_seconds > 0` enter `WAITING_TIMER`; they fire when due
  (`GET .../timers`) and the next `run` call picks them up.

---

## 13. The MCP server

**What it does.** `apps/mcp/main.py` exposes a read-only
[Model Context Protocol](https://modelcontextprotocol.io) facade over the same
REST API, so AI assistants (Claude Desktop, IDEs) can query the graph and run
agents. Every tool response is annotated with the calibrated uncertainty envelope
(`annotate_mcp_payload`, `main.py:56-58`).

**How to connect a client.**

1. Run the MCP app (e.g. `uvicorn apps.mcp.main:create_app --factory`, or the
   `eoip-mcp` container in `deploy/`). It proxies to `EOIP_API_URL`
   (default `http://eoip-api:8000`).
2. Every request except `/health/live` needs `Authorization: Bearer <token>` —
   the same token the API uses (`api_token()` from `eoip.runtime`); the server
   forwards it downstream.
3. Health check: `GET /health/live` → `{"status": "ok"}` (unauthenticated).
4. Transport security pins allowed hosts to `localhost:*`, `127.0.0.1:*`,
   `eoip-mcp:*` (`main.py:21-24`) — remote hostnames are refused.

**The 18 tools** (name — signature → underlying REST call):

| Tool | Signature | Calls |
|---|---|---|
| `search` | `(q: str, limit: int = 25)` | `GET /api/v1/search` |
| `entity` | `(canonical_id: str)` | `GET /api/v1/entities/{id}` |
| `path` | `(source_id, target_id, max_depth=8)` | `POST /api/v1/path` |
| `impact` | `(canonical_id, max_depth=4)` | `POST /api/v1/impact` |
| `lineage` | `(canonical_id, max_depth=4, result_limit=100)` | `POST /api/v1/lineage` |
| `trace_impact` | `(canonical_id, max_depth=4)` | `POST /api/v1/agents/trace-impact` |
| `list_agents` | `()` | `GET /api/v1/agents` |
| `run_agent` | `(agent_id, goal, context_refs=None, dry_run=False, synthesize=False)` | `POST /api/v1/agents/{id}/runs` |
| `agent_explanation` | `(run_id)` | `GET /api/v1/agents/runs/{id}/explanation` |
| `blast_radius` | `(canonical_id, max_depth=4)` | `POST /api/v1/graph/blast-radius` |
| `graph_surprises` | `(limit=20)` | `POST /api/v1/graph/surprises` |
| `validate_ontology` | `()` | `POST /api/v1/admin/validation` |
| `neighbors` | `(canonical_id, max_depth=1, result_limit=50)` | `POST /api/v1/neighborhood` |
| `document` | `(canonical_id)` | `GET /api/v1/entities/{id}` |
| `code_symbol` | `(qualified_name)` | `GET /api/v1/search` (limit 5) |
| `jira_issue` | `(issue_key)` | `GET /api/v1/search` (limit 5) |
| `evidence` | `(canonical_id)` | `POST /api/v1/lineage` (depth 2) |
| `query` | `(plan: dict)` | `POST /api/v1/query` |

**Errors and recovery.** Downstream HTTP errors surface as MCP errors with the API
status code and detail (`"EOIP API error 404: ..."`); connection failures surface
as code 503 `"EOIP API unavailable"`. A missing/wrong Bearer token yields HTTP 401
`"A valid Bearer token is required"`.

---

## 14. Human approval patterns

Approvals surface in **four** distinct places — do not confuse them:

1. **Agent change proposals** — `GET /api/v1/agents/proposals?status=PENDING`,
   decided via `/approve` / `/reject` (§3). Requires the `agents:approve` policy
   decision; every decision is written to the authorization decision log.
2. **Loop approval gates** — a script step with `await_approval` parks the run
   (`awaiting_approval`); `GET /api/v1/loops/approvals/pending`,
   `POST /api/v1/loops/approvals/decide`, then resume with `resume_run_id` +
   `resume_approved` (§10).
3. **Workflow step gates** — a `StepDefinition` with `requires_approval: true`
   enters `WAITING_APPROVAL`; grant it with
   `POST /api/v1/execution/workflows/{id}/approve` (§12).
4. **Ontology / identity review queues** — `POST /api/v1/ontology/proposals`
   turns drift findings into `ChangeProposal`s that land in the *same* agent
   proposal store as §3, and `/api/v1/identity/candidates/{id}/decide|reject`
   handles entity-merge review (outside this chapter's scope).

In the web UI, approvals appear wherever the frontend surfaces these endpoints;
the authoritative record is always the proposal store
(`.data/state/agent-proposals.json`) and the workflow event stream — check the
API, not the screen, when auditing. **[UI navigation paths not runtime-verified
for this chapter.]**

---

*Chapter 6 ends. Next: operations and administration.*
