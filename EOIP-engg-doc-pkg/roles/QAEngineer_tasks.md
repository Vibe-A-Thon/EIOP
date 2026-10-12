# QA Engineer — Test Execution & Bug Reporting

> **Role**: QA Engineer
> **Scope**: Test execution, bug reporting, test automation, regression testing, test data management

---

## Test Execution Tasks

### Phase 1 Tests
- **TASK-QA-001**: Execute unit tests for Token Format Engines (CORE-001)
  - Tests: Round-trip fidelity (7 formats x 10 payload types), auto-selection accuracy, token count estimation, compression ratio validation
  - Status: Not Started | Priority: P0

- **TASK-QA-002**: Execute unit tests for Verification Engine (CORE-002)
  - Tests: Each rule type independently, rule composition/chaining, short-circuit on failure, audit trail completeness
  - Status: Not Started | Priority: P0

- **TASK-QA-003**: Execute unit tests for Intent Router (CORE-003)
  - Tests: Classification accuracy per intent, sub-10ms latency validation, feedback loop recording, cost estimate accuracy
  - Status: Not Started | Priority: P0

- **TASK-QA-004**: Execute unit tests for Graph-over-Graph (CORE-004)
  - Tests: Layer creation, cross-layer query correctness, merge/diff operations, constraint propagation
  - Status: Not Started | Priority: P0

- **TASK-QA-005**: Regression test full suite after Phase 1 integration
  - Tests: All 239+ existing test files, 52 engineering discipline tests, 2 pre-existing failures documented
  - Status: Not Started | Priority: P0
  - KPI: Zero new test failures

### Phase 2-7 Tests
- **TASK-QA-006** through **TASK-QA-015**: Execute test plans for Phases 2-7 (per QA Lead test plans)

### Integration Tests
- **TASK-QA-016**: Brain OS telemetry integration — verify all engines report stats via `get_system_telemetry()`
  - Status: Not Started | Priority: P1
  - Verify: 21+ existing + new engines all return valid stats dicts

- **TASK-QA-017**: Platform Router API integration — verify all endpoints respond with correct schemas
  - Status: Not Started | Priority: P1
  - Method: OpenAPI schema validation, request/response contract checks

- **TASK-QA-018**: Cross-engine integration — verify Intelligence Engine can orchestrate new engines (token formats, verification, intent routing)
  - Status: Not Started | Priority: P1

### Automation Tasks
- **TASK-QA-019**: Write Hypothesis property-based tests for token format round-trips (TEST-003)
  - Status: Not Started | Priority: P2
  - File: `tests/property/test_token_formats.py`

- **TASK-QA-020**: Write k6 load test scripts for critical API endpoints (TEST-002)
  - Status: Not Started | Priority: P1
  - File: `tests/load/`

- **TASK-QA-021**: Write Playwright e2e tests for new dashboard lenses (UI-007)
  - Status: Not Started | Priority: P2
  - File: `apps/web/e2e/`

### Bug Reporting Standards
- Bug template: Title, Steps to Reproduce, Expected Result, Actual Result, Severity, Screenshots/Logs
- Severity levels: P0 (system down), P1 (major feature broken), P2 (minor issue), P3 (cosmetic)
- File: GitHub Issues with `bug` label

---

## Handoffs

| From QA Engineer | To Role | What |
|---|---|---|
| Bug reports | Developer | Fix implementation |
| Test results | QA Lead | Quality metrics |
| Regression results | Delivery Manager | Release readiness |
| Automation scripts | CI pipeline | Automated execution |
