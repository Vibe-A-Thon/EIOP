# Glossary

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Normative platform terminology

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Core terms

- **Canonical Entity:** source-independent platform representation identified by a stable `canonical_id`.
- **Source Event:** immutable captured source record/envelope before normalization.
- **Evidence:** reference describing why a graph fact exists, including source/method/version/confidence.
- **DETERMINISTIC / INFERRED / HUMAN_CONFIRMED:** creation status of a fact; inferred facts are never displayed as unqualified deterministic truth.
- **Logical Graph Domain:** semantic partition inside the EOIP graph, not necessarily a separate physical database.
- **Meta Graph:** graph records describing sources, domains, versions, runs, validation and quality.
- **QueryPlan:** validated typed representation of intent and graph bounds used before Gremlin execution.
- **GraphRAG:** retrieval grounded primarily in graph entities/edges/paths/provenance plus linked artifacts.
- **Loop Engineering:** design of bounded iterative execution with explicit state, termination, retry and evaluation.
- **Graph Engineering:** design of graph schema, identity, semantics, mutations, indexes, traversals, quality and lifecycle.
- **Harness Engineering:** deterministic runtime/tool/policy/observability/evaluation infrastructure surrounding probabilistic components.
- **Memory Engineering:** lifecycle/security/scoping design for persisted agent/context memory.
- **Context Engineering:** selection, ordering, compression and provenance of evidence supplied to a model/agent.
- **Graph-over-Loop:** representing loop state/transitions/outcomes as graph entities/relationships for inspection and learning.
- **Loop-over-Graph:** bounded iterative traversal/evaluation/replanning over graph state.

## Human-control policy vocabulary

These labels are **platform-defined semantics unless separately linked to a recognized external standard**:

| Label | EOIP semantic definition |
|---|---|
| HCTL — Human-Commanded-the-Loop | Human initiates and sets objective/constraints; machine executes permitted substeps. |
| HITL-FE — Human-in-the-Loop-for-Exceptions | Automation proceeds within policy; human approval/intervention is required on exception/risk threshold. |
| HBTL — Human-Beside-the-Loop | Human observes and can intervene, while normal execution can continue. |
| HATL — Human-Above-the-Loop | Human defines/approves policy and reviews system-level outcomes rather than each action. |
| HITD — Human-in-the-Design | Human controls design-time goals, tools, policies, evaluations and release gates. |
| EITL — Environment-in-the-Loop | Environment observations feed the control loop and may change plan/termination. |
| HITL — Human-in-the-Loop | A defined decision/action step requires human participation before continuation. |
| HOTL — Human-on-the-Loop | Automation acts while human supervises and can override/stop. |
| HOOTL — Human-out-of-the-Loop | No human intervention in the runtime loop; prohibited for high-risk/write MVP actions. |
| HITA — Human-in-the-Action | Human explicitly authorizes or performs the concrete action. |
| HITC — Human-in-the-Control-Loop | Human participates in feedback/control decisions affecting execution state. |
| HITI — Human-in-the-Institution | Organizational governance/policy/accountability surrounds the technical loop. |
| MITL — Machine-in-the-Loop | Machine contributes analysis/decision support inside a human-governed process. |
| HITP — Human-in-the-Process | Human participation occurs at defined business-process stages. |

Every policy is implemented using explicit dimensions: initiator, approver, supervisor, intervention trigger, action risk, reversibility, timeout behavior, exception path and evidence requirement.
