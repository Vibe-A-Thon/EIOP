# Enterprise Ontology & Intelligence Platform (EOIP) — Engineering Documentation Package

**Baseline:** 0.1.0-architecture-baseline  
**Generated:** 2026-10-01

**Current master backlog:** [../KGF-MASTER-BACKLOG.md](../KGF-MASTER-BACKLOG.md) is the active master completion backlog synthesizing [Audit-GAPS-CG-dev.md](Audit-GAPS-CG-dev.md) and the KnowGridFlow Conquest Plan. Current implementation status and phase tasks are governed by this backlog.

This package converts the governing master prompt into an implementation-ready, local-first architecture and phased engineering plan. It preserves the prompt's mandatory output set and adds an audit, research/verification basis, traceability matrix, architecture diagram catalog, versioned data contracts, machine-readable schemas and domain implementation plans.

## Start here

1. `00-specification-audit-and-enhancements.md` — ambiguity/gap resolutions.
2. `01-project-vision.md` and `02-scope-and-objectives.md` — product boundary.
3. `06-architecture.md`, `11-graph-schema.md`, `18-ingestion-architecture.md`, `25-query-engine-requirements.md`, `29-rag-architecture.md`, `30-agent-architecture.md`, `46-security-architecture.md` — architecture core.
4. `MVP-requirements.md` — the exact integrated P1 slice.
5. `MVP-implementation-plan.md` — 28 ordered build tasks.
6. `61-demo-playbook.md` — repeatable demo outcome.
7. `66-phase-roadmap.md` — P0→P8+ evolution.
8. `72-requirement-traceability.md` and `traceability/*.csv` — requirement→implementation→test→acceptance.
9. `73-architecture-diagrams.md` — all 17 requested Mermaid diagrams.
10. `74-data-contracts.md` + `schemas/*.schema.json` — versioned interface contracts.

## MVP architecture in one sentence

One local Docker Compose deployment uses Apache HugeGraph/RocksDB as the authoritative graph, a modular FastAPI application/worker, one React SPA with `/app` and `/admin` modes, a read-only MCP façade, a read-only VS Code context extension and an optional local model adapter; source events/checkpoints/DLQ/backups use mounted local volumes, and all business answers come from persisted graph evidence.

## Important scope truth

No actual Jira JSON beyond the master prompt was supplied to this generation. The included Jira and GitLab files are explicitly synthetic fixtures. The importer is mapping-driven so a real enterprise export can replace the fixture without changing graph-core logic.

## Directories

- `implementation/` — work-package implementation plans.
- `schemas/` — JSON Schemas for platform contracts.
- `openapi/` — API starter contract.
- `traceability/` — machine-readable requirement catalog and matrices.
- `diagrams/` — individual Mermaid diagram files.
- `examples/` — synthetic demonstration inputs only.

## Architecture invariants

- No cloud/SaaS runtime dependency.
- External LLM endpoints disabled in MVP.
- HugeGraph is graph/ontology source of truth.
- URL separation is not authorization.
- Deterministic parsing/linking before probabilistic inference.
- No unrestricted model-generated Gremlin.
- Read-only agent/MCP MVP.
- Inferred facts are labeled and evidence-backed.
- Core graph/search/path/impact works without an LLM.
- Performance targets remain targets until benchmarked on declared hardware/data.
