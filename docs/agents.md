# EOIP Agent Framework

EOIP provides 20 bounded agents with a governed runtime, circuit breaker, and strict read-only tool enforcement.

---

## Agent Runtime (`packages/eoip/agents/runtime.py`)

All agents run through `AgentRuntime` which enforces:

| Constraint | Value |
|-----------|-------|
| Max steps | Configurable (default 20) |
| Max seconds | Configurable (default 60) |
| Max tool calls | Configurable (default 50) |
| Max recursion | Configurable (default 3) |
| Tool access | `READ_TOOLS` frozenset only |
| Write tools | Rejected at registration |

The runtime uses a `ThreadPoolExecutor` with timeout, exponential backoff, and a circuit breaker that opens after N consecutive failures.

### Agent Contract (`packages/eoip/contracts/agent.py`)

```python
class AgentContract:
    agent_type: AgentType      # 22 types
    risk_level: RiskLevel      # R0-R4
    budget: AgentBudget        # max_steps, max_seconds, max_tool_calls
    policy: AgentPolicy        # allowed_intents, blocked_labels
    dry_run: bool              # simulate without side effects
```

---

## Agent Catalog

### Core Agents

#### TraceImpactAgent (`agents/trace_impact.py`)
The primary user-facing agent. Given a question or entity, traces downstream impact across the graph.

- **Input**: Question (NL) or canonical_id
- **Output**: `ExplanationEnvelope` with evidence_refs, calibrated confidence, step-by-step rationale
- **Tools**: search_entities, find_path, impact_analysis, get_evidence
- **Risk**: R0 (read-only)
- Tests: `tests/e2e/test_demo_flow.py::test_trace_impact_agent_on_demo`

#### BlastRadiusAgent (`agents/blast_radius.py`)
Computes downstream impact for infrastructure or service changes.

- **Input**: Anchor entity + direction (UPSTREAM/DOWNSTREAM)
- **Output**: Ranked entity list with impact scores and rationale
- **Risk**: R0 (read-only)

#### AnomalyDetectionAgent (`agents/anomaly.py`)
Detects structural and temporal anomalies in the graph.

- **Algorithms used**: degree centrality outliers, temporal gap detection, orphan detection
- **Output**: `AnomalyReport` with anomaly list, severity, and context

#### CommunityDetectionAgent (`agents/community.py`)
Discovers community structure across graph domains.

- **Algorithms used**: Louvain modularity, label propagation
- **Output**: Community assignments with modularity score

#### SimilarityAgent (`agents/similarity.py`)
Ranks entities by structural similarity.

- **Algorithms used**: Jaccard, Adamic-Adar, common neighbors
- **Output**: Ranked similarity list with scores

#### TestCoverageAgent (`agents/test_coverage.py`)
Traces code symbols to their test files and computes coverage gaps.

- **Output**: Coverage map (CodeSymbol → test files), uncovered symbols list

#### IncidentCorrelationAgent (`agents/incident_correlation.py`)
Correlates incidents with root causes and related code changes.

- **Input**: Incident canonical_id
- **Output**: Correlated MRs, commits, symbols, and deployment events

#### CatalogAgent (`agents/catalog.py`)
Manages the knowledge catalog — discovers, categorizes, and links knowledge artifacts.

- **Output**: Catalog entries with domain classifications and cross-references

#### FirewallAgent (`agents/firewall.py`)
Enforces knowledge firewall rules — prevents sensitive information from crossing domain boundaries.

- **Output**: Policy violations, trust state assessments

#### EvaluationAgent (`agents/evaluation.py`)
Runs RAG evaluation harness against a question set.

- **Metrics**: Precision, recall, evidence_coverage, groundedness, latency
- **Output**: `EvaluationReport`

#### GovernedAgent (`agents/governed.py`)
Handles operations that require human approval before execution.

- **ALL actions require explicit human approval**
- Self-modification is disabled permanently
- `governed.py` is the only agent that can propose write operations

#### OrchestratorAgent (`agents/orchestration.py`)
Coordinates multi-agent workflows.

- Dispatches sub-agents based on intent
- Aggregates results into unified response
- Respects per-sub-agent budgets

#### ProposalAgent (`agents/proposals.py`)
Creates and manages change proposals.

- All proposals require human review before execution
- Proposals are stored as graph vertices pending approval

### Analytics Agents

#### GraphAnalyticsAgent (`agents/graph_analytics.py`)
Runs any of 30+ graph algorithms as bounded agent workflows.

**Single algorithm mode**:
```json
{"goal": "ring_detection", "context_refs": ["urn:domain:CODE"]}
```

**Swarm mode** (runs 5-9 algorithms in parallel):
```json
{"goal": "swarm"}
```
Swarm executes: ring_detection, k_core, community_detection, anomaly_detection, blast_radius, + domain-specific algorithms.

- **ALGORITHM_REGISTRY**: 30 algorithms mapped to dispatch methods
- **Output**: Per-algorithm results + aggregated swarm report
- API: `POST /api/v1/agents/analytics`
- Tests: `tests/unit/test_agent_analytics.py`

#### SemanticIndexAgent (`agents/semantic_index.py`)
Runs the semantic indexing pipeline with stage filtering.

```json
{"stages": ["bridge_edges", "search_index"], "scope": "CODE"}
```

- **Stages**: bridge_edges, metadata_enrichment, search_index, analytics, validation, event_publish
- Triggered automatically by graph evolution events
- API: `POST /api/v1/agents/semantic-index`
- Tests: `tests/unit/test_agent_analytics.py`

### Support Agents

#### MemoryAgent (`agents/memory.py`)
Manages scoped agent memory records (TTL, provenance, classification).

#### AgentRouter (`agents/agent_router.py`)
Intent-based routing to the appropriate agent.

#### TraceAgent (`agents/trace.py`)
Traces code lineage: symbol → commits → MRs → issues → deployments.

#### KnowledgeDebtAgent (`agents/knowledge_debt.py`)
Assesses knowledge debt: undocumented symbols, orphaned documents, stale links.

---

## Tool Access Policy

Only tools in `READ_TOOLS` frozenset can be registered:

```
search_entities, get_entity, get_neighbors, find_path, impact_analysis,
trace_lineage, get_evidence, list_domains, get_code_symbol, get_file_symbols,
list_commits, get_merge_request, get_dependencies, query_graph, get_quality,
run_algorithm, get_memory, get_community
```

Any attempt to register a write tool raises `ToolRegistrationError` at agent initialization.

`KnowledgeCurator` and `ProposalAgent` are `PROPOSE_ONLY` — they generate proposals that must be approved before execution.

---

## Multi-Agent Orchestration

The `OrchestratorAgent` can spawn sub-agents with independent budgets. The total budget is not shared — each sub-agent has its own step/time limits.

For complex queries, the typical orchestration is:

1. `TraceImpactAgent` → identifies anchor entities
2. `BlastRadiusAgent` → computes impact set
3. `TestCoverageAgent` → checks test coverage of affected symbols
4. `IncidentCorrelationAgent` → correlates with recent incidents

Each sub-agent returns an `ExplanationEnvelope` that the orchestrator aggregates into a unified answer.

---

## ExplanationEnvelope

All user-facing agents return `ExplanationEnvelope`:

```python
class ExplanationEnvelope:
    answer: str                    # natural language answer
    confidence: float              # 0.0-1.0, calibrated (never 1.0 without full evidence)
    evidence_refs: list[str]       # stable canonical_id URNs
    reasoning_steps: list[str]     # step-by-step trace
    partial: bool                  # True if budget was exhausted
    agent_type: str
    duration_ms: int
```
