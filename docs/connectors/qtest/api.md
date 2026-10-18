# qTest Manager API Research & Qualification Specification

*Researched per CRA-005.3, CRA-005.4, CRA-005.8. Complies with ADR-004 and ONT-005.*

## Official API Specifications & Pinned Versions
- **qTest REST API**: Version 3.0 (`https://api.qasymphony.com/`)
  - Endpoints:
    - `/api/v3/projects` (Projects)
    - `/api/v3/projects/{projectId}/test-cases` (Test Definitions)
    - `/api/v3/projects/{projectId}/test-runs` (Test Execution Runs)
    - `/api/v3/projects/{projectId}/test-suites` (Test Suites)
    - `/api/v3/projects/{projectId}/test-cycles` (Test Cycles)
    - `/api/v3/projects/{projectId}/test-runs/{testRunId}/auto-test-logs` (Execution Results)

## Authentication & Scopes
- **Authentication**: Bearer Token via header `Authorization: Bearer <qtest_token>`.
- **Project Isolation**: All operations scoped strictly by `projectId`.

## Semantic Distinction: Definitions vs Executions
- Test Definitions (`TestCase`): Authoritative definitions of test specifications, steps, expected results, and requirement links.
- Test Executions (`TestRun`): Timestamped execution runs carrying passed/failed counts, duration, environment, and logs.
- Cross-System Traceability: `qtest:verifiesRequirement` links to external Jira issues ONLY when the Jira issue exists in the graph.
