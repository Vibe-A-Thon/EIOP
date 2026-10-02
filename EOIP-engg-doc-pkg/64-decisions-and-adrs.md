# Architecture Decisions and ADRs

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Baseline decisions that coding agents must not silently overturn

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## ADR-001 — Logical domains in one physical HugeGraph graph for MVP
**Status:** Accepted. **Decision:** graph-domain metadata separates Jira/code/docs/CI/provenance/meta while keeping cross-domain paths native. **Revisit when:** measured size/HA/isolation requires physical partitioning.

## ADR-002 — RocksDB standalone HugeGraph for MVP
**Status:** Accepted. **Decision:** choose simplest supported local topology. **Consequence:** no HA; backup/rebuild is required. **Revisit:** P7 capacity/SLO review.

## ADR-003 — Modular monolith application core
**Status:** Accepted. **Decision:** one Python domain codebase with API/worker/MCP entry points and strict ports. **Rejected:** premature microservices. **Revisit:** independently scalable/deployable/security boundary proven by metrics.

## ADR-004 — Raw capture on local filesystem, HugeGraph as authoritative graph
**Status:** Accepted. **Decision:** immutable SourceEvent/DLQ/checkpoints are files/volumes; canonical graph truth resides in HugeGraph. **Reason:** replay without adding a second database.

## ADR-005 — No mandatory vector database in P1
**Status:** Accepted. **Decision:** graph-first/linked-text retrieval. **Revisit:** P3 evaluation demonstrates semantic retrieval gap worth added infrastructure.

## ADR-006 — QueryPlan compilation, no unrestricted NL→Gremlin
**Status:** Accepted. **Decision:** models/rules produce typed plans; policy selects bounded templates. **Reason:** safety, repeatability and cost control.

## ADR-007 — Read-only MCP/agent MVP
**Status:** Accepted. **Decision:** analysis/context only. **Reason:** write governance/human approval is not yet mature.

## ADR-008 — Deterministic code and cross-domain linking first
**Status:** Accepted. **Decision:** AST/Git/keys/hashes before probabilistic/LLM links. Inferred links remain labeled/evidenced.

## ADR-009 — Local model abstraction and model-down degradation
**Status:** Accepted. **Decision:** local model enriches, never owns graph truth. External providers disabled. Core platform works without the model.

## ADR-010 — Versioned external contracts and canonical IDs
**Status:** Accepted. **Decision:** clients never depend on HugeGraph internal IDs; storage topology/schema implementation can evolve behind stable contracts.
