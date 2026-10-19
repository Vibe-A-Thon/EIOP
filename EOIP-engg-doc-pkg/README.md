# Enterprise Ontology & Intelligence Platform (EOIP) — Engineering Documentation Package

**Baseline:** 0.1.0-architecture-baseline  
**Generated:** 2026-10-01

**Status caution:** this package contains specifications, plans, audits, and historical research. A backlog checkbox or generated task count is not runtime acceptance evidence. Use the owning requirement/implementation plans and their current evidence procedures to determine what is implemented, blocked, or verified.

This package converts the governing master prompt into an implementation-ready, local-first architecture and phased engineering plan. It preserves the prompt's mandatory output set and adds an audit, research/verification basis, traceability matrix, architecture diagram catalog, versioned data contracts, machine-readable schemas and domain implementation plans.

## How to use this package

This package contains normative specifications, architecture proposals,
implementation plans, historical audits, reference material, schemas, and
traceability artifacts. Some chapters describe target behavior that is not
implemented or not yet independently qualified. A source path, test name,
generated audit, backlog count, or successful demo is not a completion receipt.

Use the repository root [README](../README.md) and [Getting Started
guide](../docs/getting-started.md) for current operator/developer entrypoints.
Use [Architecture](../docs/architecture-guide.md) for the source-described runtime
topology and storage boundaries. Use each programme's current requirements,
implementation plan, and evidence ledger for its own status. If a required
ledger or evidence bundle is absent, report that work as open or blocked.

The codebase contains a FastAPI API, web UI, worker, MCP server, VS Code
extension, graph adapters, connector and query modules, and optional numerical
experiments. Their presence does not imply that every documented endpoint,
adapter, profile, benchmark, persistence guarantee, or end-to-end scenario has
passed its owning acceptance gate.

## Start here

For maintenance, begin with the current [documentation index](../docs/README.md), [component map](../apps/README.md), [migration guide](../docs/migration-refactoring-guide.md) and [review scope](../docs/documentation-review-2026-10-18.md). This package's dated baseline remains historical; newer root-level ASPEII, Community/IP, IP, Graph Neurons and Wisdom requirements have their own decisions and evidence gates. Resolve conflicts explicitly rather than selecting whichever document claims the highest completion.

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

## Documented MVP deployment shape

The default local Compose profile is documented around HugeGraph, a FastAPI API,
a filesystem-backed worker, a React SPA with `/app` and `/admin` paths, a
read-oriented MCP facade, a VS Code context extension, and mounted volumes. This
is a deployment profile, not a claim of multi-worker durability, fully
evidence-grounded answers, or release qualification. See the Docker runbook and
current architecture guide for actual defaults and limits.

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
