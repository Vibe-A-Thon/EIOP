# Phased Roadmap

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Phase 0 through Phase 8+ with migration preparation

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## PHASE 0 — Architecture, schemas, development foundation

**Scope:** Contracts, schema manifest, repo boundaries, threat model, Compose skeleton, CI/test harness.  
**Migration effect / dependency:** No product breadth; prepare canonical IDs, connector SDK, QueryPlan and versioned contracts.

## PHASE 1 — Fully functional demonstrable MVP

**Scope:** Jira/Git/code/docs vertical slice, HugeGraph, provenance, validation, query/impact/path, web/admin, VS Code, GraphRAG, TraceImpactAgent, MCP, observability, backup/restore.  
**Migration effect / dependency:** One physical graph; read-only AI/MCP; no mandatory vector DB.

## PHASE 2 — Enterprise connectors and ontology depth

**Scope:** Confluence, ServiceNow, richer file/intranet parsers, RDF/OWL export, broader domain ontology.  
**Migration effect / dependency:** Reuse Connector SDK/canonical contracts; additive schema migrations.

## PHASE 3 — Advanced GraphRAG and retrieval routing

**Scope:** Local embeddings/vector index if benchmarks justify; CRAG/Self-RAG/adaptive/multi-hop strategy plugins; reranking/evaluation.  
**Migration effect / dependency:** RetrievalResult contract exists in P1; HugeGraph remains source of truth.

## PHASE 4 — Advanced agents and multi-agent workflows

**Scope:** Supervisor/worker, DAG, planner/executor, critic/reviewer, consensus where useful.  
**Migration effect / dependency:** Bounded runtime/tool contracts from P1; still governed write boundary.

## PHASE 5 — Temporal intelligence and graph analytics

**Scope:** Graph diffs, point-in-time/release views, deeper blast radius, analytics/community/path algorithms.  
**Migration effect / dependency:** P1 canonical IDs + temporal/version fields avoid identity migration.

## PHASE 6 — Human-control policies and automation

**Scope:** Concrete HCTL/HITL/HOTL/etc policy engine, approvals, deterministic RPA and selected write workflows.  
**Migration effect / dependency:** P1 separates read/write tools and already audits actions.

## PHASE 7 — Enterprise hardening, scaling and operational maturity

**Scope:** RBAC/SSO if required, HA, distributed HugeGraph/HStore if measured, quotas, multi-tenancy/isolation, DR/SLO operations.  
**Migration effect / dependency:** P1 versioned APIs, domain boundaries and canonical IDs insulate clients.

## PHASE 8+ — Advanced/self-improving capabilities

**Scope:** Controlled proposal/sandbox/evaluation workflows for self-learning/evolving/writing; never direct unreviewed production mutation.  
**Migration effect / dependency:** Requires mature governance, approvals, regression evaluation, rollback and policy enforcement.

## Deferred-requirement mapping

| Requirement | Target | Dependency / preparation in MVP |
|---|---|---|
| FR-CONF-001 — Confluence connector | P2 | Stable canonical contracts, connector/query/agent ports and additive schema/versioning established in P1. |
| FR-SNOW-001 — ServiceNow connector | P2 | Stable canonical contracts, connector/query/agent ports and additive schema/versioning established in P1. |
| FR-GRAPH-010 — RDF/OWL interoperability | P2 | Stable canonical contracts, connector/query/agent ports and additive schema/versioning established in P1. |
| FR-RAG-006 — Adaptive RAG strategy framework | P3 | Stable canonical contracts, connector/query/agent ports and additive schema/versioning established in P1. |
| FR-AGENT-005 — Controlled self-modification | P8+ | Stable canonical contracts, connector/query/agent ports and additive schema/versioning established in P1. |
