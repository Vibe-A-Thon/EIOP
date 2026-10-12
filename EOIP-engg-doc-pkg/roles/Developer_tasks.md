# Developer — Feature Implementation & Unit Testing

> **Role**: Software Developer (+ AI Agent Developer)
> **Scope**: Feature coding, unit tests, bug fixes, documentation, engine implementation

---

## Implementation Task Queue

### Phase 1 — Core Engines (AI Agent Executable)

Each task follows the standard engine pattern:
1. Create `packages/eoip/<module>/__init__.py` with exports
2. Create `packages/eoip/<module>/engine.py` with engine class + `get_*_engine()` singleton
3. Implement `stats()` method returning `{"engine": "<name>", ...}`
4. Wire into `packages/eoip/brain/brain_os.py` — import + telemetry entry
5. Add Pydantic request models at module level in `packages/eoip/platform_router.py`
6. Add API endpoints in `platform_router.py`
7. Write unit tests in `tests/unit/`

- **TASK-DEV-001**: Token Format Engines (CORE-001)
  - File: `packages/eoip/token_formats/engine.py`
  - Classes: `FormatStrategy` (ABC), `TOONFormat`, `TRONFormat`, `LEANFormat`, `ASONFormat`, `ZONFormat`, `ZOONFormat`, `TSONFormat`, `TokenFormatEngine`
  - Methods: `serialize(obj, format)`, `deserialize(data, format)`, `auto_select(obj, budget)`, `estimate_tokens(obj, format)`, `benchmark(obj)`
  - Tests: Round-trip fidelity per format, auto-selection, token counting, compression ratios

- **TASK-DEV-002**: Verification Engine (CORE-002)
  - File: `packages/eoip/verification/engine.py`
  - Classes: `VerificationRule` (ABC), `SchemaConformanceRule`, `PolicyComplianceRule`, `ConfidenceThresholdRule`, `HallucinationDetectionRule`, `CognitiveDriftRule`, `FactConsistencyRule`, `OutputFormatRule`, `VerifierRegistry`, `DynamicGuardrailInjector`, `VerificationEngine`
  - Methods: `verify(output, rules)`, `register_rule()`, `compose_chain()`, `inject_guardrail()`, `audit_trail()`

- **TASK-DEV-003**: Intent Router (CORE-003)
  - File: `packages/eoip/routing/engine.py`
  - Classes: `IntentClassifier`, `RoutingDecision`, `RoutingTable`, `FeedbackTracker`, `RouterEngine`
  - Methods: `classify(query)`, `route(query)`, `record_feedback()`, `accuracy_report()`

- **TASK-DEV-004**: Graph-over-Graph (CORE-004)
  - File: `packages/eoip/graph_graph/engine.py`
  - Classes: `GraphLayer`, `LayerRelation`, `CrossLayerQuery`, `GraphOverGraphEngine`
  - Methods: `add_layer()`, `project(query, layers)`, `cross_query()`, `merge_layers()`, `diff_layers()`

- **TASK-DEV-005**: Loop-over-Loop (CORE-005)
  - File: `packages/eoip/intelligence_eng/engine.py` (extend)
  - Classes: `SupervisoryLoop`, `LoopMonitor`, `LoopSwitcher`

- **TASK-DEV-006**: Token Budget (CORE-006)
  - File: `packages/eoip/token_budget/engine.py`
  - Classes: `TokenBudget`, `BudgetPolicy`, `BudgetTracker`, `TokenBudgetEngine`

### Phase 2 — Agentic AI & Graph

- **TASK-DEV-007**: Cognitive Boundary Telemetry (AGENT-001)
  - File: `packages/eoip/telemetry/adapter.py` (extend)
  - Classes: `CognitiveBoundaryDetector`, `HandoffDecision`

- **TASK-DEV-008**: Entity Extraction Pipeline (AGENT-002)
  - File: `packages/eoip/extraction/engine.py`
  - Classes: `DocumentChunker`, `EntityExtractor`, `RelationExtractor`, `CommunityDetector`, `ExtractionPipeline`

- **TASK-DEV-009**: Agent Message Bus (AGENT-003)
  - File: `packages/eoip/agents/message_bus.py`

- **TASK-DEV-010**: Fan-Out/Fan-In Stages (AGENT-004)
  - File: `packages/eoip/harness/engine.py` (extend)

- **TASK-DEV-011**: Federated Graph Engine (GRAPH-001)
  - File: `packages/eoip/federation/engine.py`

- **TASK-DEV-012**: Temporal Retrieval (GRAPH-005)
  - File: `packages/eoip/retrieval/temporal.py`

### Phase 3-7 Tasks
- **TASK-DEV-013** through **TASK-DEV-030**: Remaining 18 engine implementations (see eoip-phase4-requirements.md for full specs)

### Bug Fixes
- **TASK-DEV-031**: Fix `test_deployed_route_surface_contains_product_gate_routes` — wire `/api/v1/loops/catalog` endpoint
  - File: `packages/eoip/platform_router.py` or loops router
  - Priority: P1

- **TASK-DEV-032**: Fix `test_intelligent_query_with_store` — assert `latency_ms >= 0` instead of `> 0` or add timing floor
  - File: `tests/unit/test_graph_intelligence.py`
  - Priority: P2

---

## Coding Standards

- Thread-safe singleton: double-checked locking with `threading.Lock()`
- Pydantic `BaseModel` defined at module level (not inside functions) for OpenAPI schema resolution
- `from __future__ import annotations` at top of every module
- Type hints on all public methods
- `stats()` method on every engine returning `{"engine": "<name>", ...}`
- No comments unless explaining non-obvious WHY

## Handoffs

| From Developer | To Role | What |
|---|---|---|
| Implemented code | Lead Developer | Code review |
| Unit tests | QA Engineer | Integration test validation |
| API endpoints | QA Lead | API contract testing |
| Bug reports | Delivery Manager | Sprint backlog |
