# Governed Deep Agents and XAI

EOIP Deep Agents are bounded reasoning services over the authoritative knowledge graph. They do not silently mutate graph state. Read agents may inspect allowlisted graph capabilities; writing agents can only emit inert change proposals for a separate human decision.

## Implemented agent catalog

The runtime registers specialists for trace and change impact, graph investigation, incident investigation and correlation, data quality, ontology review, connector diagnosis, documentation freshness, evidence verification, architecture conformance, query optimization, anomaly detection, blast radius, community analysis, similarity, test coverage, and knowledge curation. `GraphInvestigator` can optionally use the configured local model for evidence-grounded synthesis and degrades to deterministic retrieval when the model is unavailable.

`KnowledgeCurator` is risk R2 and `PROPOSE_ONLY`. Its output can be approved or rejected, but approval does not apply the proposed graph mutation. A separately authorized platform workflow would be required to apply it.

## Execution lifecycle

Every accepted run records these safe lifecycle events:

`RECEIVE -> CONTEXT -> PLAN -> VALIDATE -> EXECUTE -> OBSERVE -> EVALUATE -> EXPLAIN -> AUDIT -> FINISH`

`OBSERVE` is emitted for context-aware tool calls and may be absent for legacy deterministic agents that execute through the compatibility adapter. Contracts enforce maximum steps, tool calls, retries, recursion, elapsed time, model tokens, and context items. The runtime also has a consecutive-failure circuit breaker.

Source content crosses a knowledge firewall before execution. Secret-like text is redacted, prompt-injection patterns are flagged, and all retrieved content remains untrusted data rather than executable instructions.

## Explainability contract

Each result contains an `explanation` with:

- decision summary;
- observed facts and explicitly marked inferences;
- stable evidence references and graph paths;
- policy and rule decisions;
- confidence and the inputs used to compute it;
- uncertainty and rejected alternatives;
- tool-call summaries with argument digests rather than raw sensitive input.

Private chain-of-thought is never stored or returned. The fixed `chain_of_thought_disclosed: false` field makes that boundary machine-verifiable.

## APIs

- `GET /api/v1/agents` - list versioned contracts, capabilities, risks, and budgets.
- `POST /api/v1/agents/{agent_id}/runs` - execute a governed agent.
- `GET /api/v1/agents/runs/{run_id}` - retrieve the current result and durable trace.
- `GET /api/v1/agents/runs/{run_id}/explanation` - retrieve the safe XAI envelope.
- `GET /api/v1/agents/proposals` - list pending or decided proposals.
- `POST /api/v1/agents/proposals/{proposal_id}/approve` - record human approval only.
- `POST /api/v1/agents/proposals/{proposal_id}/reject` - record human rejection.

The MCP facade exposes agent discovery, execution, and explanation through the same authenticated API. It does not expose proposal approval or graph mutation.

## Orchestration and release evaluation

`AgentOrchestrator` supports bounded sequential supervisor workflows. Child count, recursion, per-agent time, and stop-on-failure behavior are explicit. It does not permit uncontrolled peer loops or recursive swarms.

`evaluate_agents` runs golden cases and reports pass rate, evidence rate, invalid status or tool use, and an evaluation gate. New or changed agent contracts should not be enabled until their golden cases pass the configured threshold.

## Operational controls

Set `enabled: false` in a deployed agent contract to stop new runs. The runtime fails closed for unknown or disabled agents, unregistered tools, exhausted budgets, open circuit breakers, and missing approvals. Trace files are written atomically under `${EOIP_DATA_DIR}/agent-traces`; audit events and the graph `AgentRun` record retain actor and correlation identifiers without source payloads or hidden reasoning.
