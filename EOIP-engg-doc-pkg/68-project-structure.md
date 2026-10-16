# Project Structure

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define repository/module layout and dependency rules

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

Loop engineering designs bounded iterative execution; graph engineering designs semantic state and traversals; harness engineering supplies deterministic wrappers, tools, policies, observability and evaluation; context engineering constructs minimal evidence packages; memory engineering governs persistence. Graph-over-loop records loop state/outcomes as graph facts; loop-over-graph iteratively traverses/evaluates graph neighborhoods under explicit termination conditions.

Tests are traceability assets. Unit/parser/connector/schema/integrity/ontology/identity/relationship/provenance/idempotency/recovery/query-limit/RAG/agent/MCP/UI/VS Code/security/Docker/backup/E2E/performance suites map to requirement IDs. A feature is done only when its requirement, implementation task, tests and acceptance evidence are linked.


```text
eoip/
├─ apps/
│  ├─ api/                 # FastAPI composition root
│  ├─ worker/              # ingestion/parse job entry point
│  ├─ mcp/                 # MCP façade
│  ├─ web/                 # React/TypeScript SPA
│  └─ vscode-extension/    # VS Code extension
├─ packages/
│  ├─ contracts/           # Pydantic/versioned JSON contracts
│  ├─ connectors/          # SDK + jira/git/gitlab/file adapters
│  ├─ ingestion/           # capture/canonicalize/checkpoint/DLQ
│  ├─ ontology/            # ontology vocabulary + schema manifest
│  ├─ graph/               # HugeGraph client/schema/mutations
│  ├─ codegraph/           # parser plugins + symbol graph
│  ├─ identity/            # resolution policies
│  ├─ provenance/          # evidence/lineage
│  ├─ validation/          # rule engine + quality metrics
│  ├─ query/               # QueryPlan, policy, Gremlin templates
│  ├─ retrieval/           # RAG router/context builder
│  ├─ models/              # local model abstraction
│  ├─ agents/              # registry/runtime/TraceImpact agent
│  ├─ audit/               # audit event sink/redaction
│  └─ observability/       # logs/metrics/tracing helpers
├─ config/
│  ├─ ontology/
│  ├─ mappings/
│  ├─ query-policies/
│  └─ agents/
├─ deploy/
│  ├─ docker-compose.yml
│  ├─ docker-compose.observability.yml
│  └─ secrets.example/
├─ examples/
│  ├─ jira/
│  ├─ gitlab/
│  └─ demo-repo/
├─ tests/
│  ├─ unit/ contract/ integration/ e2e/ security/ performance/
├─ scripts/
│  ├─ bootstrap_schema.py
│  ├─ backup.py
│  ├─ restore.py
│  └─ demo_reset.py
└─ docs/
```

## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| NFR-MAINT-001 | Modular monolith boundary | P1-MVP | Core can later split without changing external contracts. |
| FR-CONN-001 | Connector SDK | P1-MVP | A new connector can be added without editing ingestion core. |
| FR-QUERY-001 | Structured QueryPlan | P1-MVP | All NL and structured requests compile to validated QueryPlan. |

## Engineering rules

- Configuration is versioned; secrets are references, never committed values.
- Every persistent fact carries canonical identity and provenance where applicable.
- Every failure path returns a stable error category, logs a correlation ID, and avoids partial silent success.
- MVP behavior must remain functional without an external network and, for graph features, without a local LLM.
- New implementation work must add/adjust automated tests and traceability entries.

## Validation / definition of done

- Normative interfaces are implemented and documented.
- Automated tests mapped to the listed requirement IDs pass.
- Error, security, logging and configuration paths are exercised.
- Acceptance evidence is reproducible from a clean documented environment.
- Deferred capabilities remain behind stable interfaces and are not represented as already implemented.
