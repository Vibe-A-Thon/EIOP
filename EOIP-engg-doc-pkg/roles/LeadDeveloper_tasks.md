# Lead Developer — Implementation Leadership & Code Quality

> **Role**: Lead Developer / Tech Lead
> **Scope**: Code architecture, reviews, mentoring, implementation decisions, refactoring, quality standards

---

## SDLC Phase Responsibilities

### 1. Implementation Leadership
- **TASK-LD-001**: Implement Token Format Engines (CORE-001) — 7 serialization strategies + auto-selection + benchmarks
  - Status: Not Started | Priority: P0
  - File: `packages/eoip/token_formats/engine.py`
  - Acceptance: All 7 formats serialize/deserialize, round-trip fidelity, 30%+ token reduction, brain_os + router wiring, unit tests

- **TASK-LD-002**: Implement Verification & Guardrail Engine (CORE-002) — VerifierRegistry, 7+ rules, DynamicGuardrailInjector
  - Status: Not Started | Priority: P0
  - File: `packages/eoip/verification/engine.py`
  - Acceptance: Rule composition, loop boundary integration, audit trail, tests

- **TASK-LD-003**: Implement Intent Router (CORE-003) — classifier, routing table, feedback loop, cost integration
  - Status: Not Started | Priority: P0
  - File: `packages/eoip/routing/engine.py`
  - Depends: CORE-001

- **TASK-LD-004**: Implement Graph-over-Graph (CORE-004) — layers, cross-layer queries, merge, diff, constraint propagation
  - Status: Not Started | Priority: P0
  - File: `packages/eoip/graph_graph/engine.py`

- **TASK-LD-005**: Implement Loop-over-Loop (CORE-005) — SupervisoryLoop, LoopMonitor, strategy switching
  - Status: Not Started | Priority: P1
  - File: `packages/eoip/intelligence_eng/engine.py` (extend)
  - Depends: CORE-002

- **TASK-LD-006**: Implement Token Budget Engineering (CORE-006) — allocation strategies, tracking, reallocation
  - Status: Not Started | Priority: P1
  - File: `packages/eoip/token_budget/engine.py`
  - Depends: CORE-001

### 2. Code Quality & Standards
- **TASK-LD-007**: Establish code review checklist for AI-generated code
  - Status: Not Started | Priority: P0
  - Deliverable: Review checklist covering: thread safety, Pydantic module-level models, singleton pattern, brain_os wiring, router endpoints, test coverage
  - Risk: AI agents produce code that silently fails or has subtle bugs
  - Mitigation: Mandatory human review, automated linting, type checking

- **TASK-LD-008**: Enforce consistent engine pattern across all 21+ discipline engines
  - Status: Not Started | Priority: P0
  - Deliverable: Engine template/archetype document
  - Pattern: `__init__.py` exports, `engine.py` with class + `get_*_engine()` singleton, `stats()` method, brain_os telemetry, router endpoints

- **TASK-LD-009**: Define Pydantic model standards for API request/response schemas
  - Status: Not Started | Priority: P1
  - Deliverable: Pydantic conventions document (module-level models, Field validators, ConfigDict)

- **TASK-LD-010**: Establish Git branching strategy — feature branches, PR reviews, squash merge to dev_local
  - Status: Not Started | Priority: P1
  - Deliverable: Git workflow document

### 3. Phase 2+ Implementation Oversight
- **TASK-LD-011**: Implement/oversee Phase 2 engines: extraction, federation, temporal retrieval, causal inference
  - Status: Not Started | Priority: P1
  - Files: `packages/eoip/extraction/`, `packages/eoip/federation/`, `packages/eoip/retrieval/temporal.py`, `packages/eoip/causal/`

- **TASK-LD-012**: Implement/oversee Phase 3 engines: XAI, NLP pipeline, relation extraction, MLOps
  - Status: Not Started | Priority: P1
  - Files: `packages/eoip/xai/`, `packages/eoip/nlp/`, `packages/eoip/mlops/`

- **TASK-LD-013**: Review and approve all Phase 4-7 implementations before merge
  - Status: Not Started | Priority: P0
  - KPI: 100% code review coverage, < 24h review turnaround

### 4. Technical Debt & Refactoring
- **TASK-LD-014**: Fix pre-existing test failures (test_deployed_route_surface, test_intelligent_query latency)
  - Status: Not Started | Priority: P1
  - Files: `tests/unit/test_product_intelligence.py`, `tests/unit/test_graph_intelligence.py`

- **TASK-LD-015**: Evaluate engine import chain performance — current pytest collection takes 60-120s due to 500+ module imports
  - Status: Not Started | Priority: P2
  - Risk: Slow test feedback loop reduces developer productivity
  - Mitigation: Lazy imports, import profiling, test isolation

- **TASK-LD-016**: Standardize error handling across all engines — consistent exception hierarchy, error codes
  - Status: Not Started | Priority: P2
  - Deliverable: Exception hierarchy document

---

## Handoffs

| From Lead Dev | To Role | What |
|---|---|---|
| Implemented engines | QA Engineer | Test execution |
| Code review feedback | Developer / AI Agent | Revision requests |
| Technical blockers | Architect | Design decisions |
| Implementation estimates | Delivery Manager | Sprint planning |
| Performance findings | QA Lead | Load test baseline |
