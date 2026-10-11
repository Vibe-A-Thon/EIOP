# EOIP / KnowGridFlow Audit, Gaps, and Code-Graph Development Backlog

**Document ID:** AUDIT-GAPS-CG-DEV-2026-10-11  
**Date:** 2026-10-11  
**Workspace:** `F:\code\EIP\EIOP`  
**Purpose:** Full current documentation/code audit, gap analysis, and closure backlog for implementation planning.

> Current overlay, 2026-10-11: after this audit was merged into the master
> backlog, the working tree advanced to 167/516 backlog tasks ticked. Phase 0
> and Phase 1 are complete; Phase 2 is 88/130; Phase 8 is 1/17. The baseline
> evidence below remains the audit receipt for this document, while
> `KGF-MASTER-BACKLOG.md`, `requirements-registry.json`,
> `requirements-test-map.json` and `available-status.md` carry the latest
> closure/evidence state.

## Executive Summary

This audit re-read the repository Markdown corpus and compared the documented requirements, status claims, architecture notes, demo expectations, and implementation plans against the current codebase, tests, API surfaces, config, schemas, web app, worker, MCP app, and VS Code extension.

The codebase is substantially implemented and currently passes the Python regression suite and web build. The main remaining issue is not a broad absence of code. The largest gap is documentation and traceability drift: older Markdown files still mix historical claims, stale paths, aspirational roadmap text, and current implemented capabilities without enough separation.

Current hard evidence from this audit pass:

| Evidence | Current Result |
|---|---:|
| Current `.md` files mechanically read with `rg --files -g "*.md"` + `Get-Content` | 192 files / 38,121 lines |
| Conservative `scripts.documentation_audit` scan of tracked Markdown/text | 194 documents / 46,685 lines |
| Candidate requirement records indexed by documentation audit | 1,639 |
| Candidate records with literal implementation/test leads | 440 Partial |
| Candidate records without mapped literal leads | 1,199 Missing |
| GAP coverage gate | 296/296 done; P0 gate passed |
| G2 coverage gate | 364/364 done; P0 gate passed |
| Deployment app route scan | 502 routes |
| Product capability scanner score | 0.9857 |
| Product first-choice gate | Failed only because `PIC-002` is not advanced-ready |
| Full Python test suite | 2,843 passed, 34 skipped, 2 warnings, 0 failures |
| Web build | Vite build passed; 167 modules transformed; built in 8.35s |

Important interpretation: GAP/G2 coverage gates are strong local evidence, but they do not erase the conservative documentation-audit backlog. The audit backlog includes unmapped obligations, stale references, historical claims, and requirements that need semantic reconciliation before being treated as closed.

## What Is Implemented

| Area | Current implementation evidence |
|---|---|
| API runtime | `apps/api/app.py`, `apps/api/main.py`, `apps/api/extended.py`; deployment app exposes 502 routes when constructed with memory backend. |
| Graph core | `packages/eoip/graph/*` includes memory store, HugeGraph, Neptune, Neo4j, backends, algorithms, metrics, bitemporal, evolution, snapshots, simulation, causal, what-if, twin, process mining, and graph intelligence modules. |
| Query | `packages/eoip/query/*` includes executor, NL/NLQ, policy, cache, languages, intelligence, federation-related query support, and polyglot engine. |
| Retrieval/RAG | `packages/eoip/retrieval/*`, `packages/eoip/ragx/*`, and brain/RAG suite modules support deterministic retrieval, hybrid/vector/keyword search, retrieval evaluation, and multi-modal RAG catalog behavior. |
| Connectors and ingestion | `packages/eoip/connectors/*`, `packages/eoip/ingestion/*`, `packages/eoip/fileparse/*`, `packages/eoip/systems/*`; implemented connector modules include Jira, GitHub, GitLab, Confluence, ServiceNow, files, crawler, CI/CD, observability, API portal, SBOM, and related registry/acquisition support. |
| Agents, loops, memory | `packages/eoip/agents/*`, `packages/eoip/loops/*`, `packages/eoip/reasoning/*`, `packages/eoip/brain/*`; implemented bounded agent runtime, agent catalog/archetypes, loop primitives, approval gates, cognitive narrator, Brain OS, learning/report components, and self-LLM module. |
| Security and governance | `packages/eoip/authn`, `authz`, `audit`, `egress`, `privacy`, `compliance`, `licensing`, `tenancy`, `config`, `model_management`, `marketplace`, `plugins`, `qa`. |
| Web app | `apps/web` is Vite + React + JavaScript/CSS with graph explorer, admin components, KGR panels, export/report UI pieces, graph canvas, and buildable production bundle. |
| VS Code extension | `apps/vscode-extension` contains extension host code, MCP client, demo driver, tests, and README. |
| MCP app | `apps/mcp/main.py` exposes graph-facing MCP integration. |
| Deployment/ops | `deploy/*`, Helm chart, container scripts, Hubble assets, backup/restore scripts, runtime detection, smoke/recovery scripts, Prometheus config. |
| Tests | 2,843 Python tests pass locally in this audit pass; web build also passes. |

## Current High-Priority Gaps

| ID | Priority | Status | Gap | Evidence | Recommended closure |
|---|---|---|---|---|---|
| CG-GAP-001 | P0 | Partially developed | Product scanner expects `/api/v1/loops/catalog`, but deployment route table exposes `/api/v1/brain/loops` and the standalone `eoip.loops.router` is not mounted. | Route scan found `/api/v1/brain/loops`, not `/api/v1/loops/catalog`; `packages/eoip/loops/router.py` exists. | Mount `build_router()` from `eoip.loops.router` or update product scanner/docs to the supported Brain OS loops route. Add route test. |
| CG-GAP-002 | P1 | Partially developed / scanner mismatch | Product scanner expects exact `/api/v1/reports`; deployed app exposes `/api/v1/reports/templates`, `/render`, `/export/{report_id}`, and schedule routes but no root reports index. | Route scan found report subroutes but not `/api/v1/reports`. | Add `GET /api/v1/reports` summary route or update scanner expectation to a concrete report subroute. |
| CG-GAP-003 | P0 | Documentation drift | Current docs still contain stale or incorrect implementation paths and historical pass counts. | Examples: older status docs referenced `apps/console`, `packages/eoip/ontology/schema.py`, `packages/eoip/rag/engine.py`, and old pytest totals. | Treat this file and `available-status.md` as active current status; gradually reconcile older docs by section instead of rewriting historical audit records. |
| CG-GAP-004 | P0 | Traceability gap | Conservative documentation audit indexed 1,199 candidate records without literal implementation/test leads. | `python -m scripts.documentation_audit --project-root .` output: 1,639 records, 440 Partial, 1,199 Missing. | Convert candidates into atomic requirements, map semantically to code/tests, and retire false positives. |
| CG-GAP-005 | P1 | Documentation link drift | Root README guide links were corrected, but historical/engineering package links still need a dedicated link pass. | Earlier link audit found stale local Markdown links. | Run a link checker after this audit and patch non-historical docs first. |
| CG-GAP-006 | P1 | Operator console drift | Older docs mention `apps/console`; no `apps/console` directory exists. | `Test-Path apps\console` returned false. | Either implement the console, move console capability into documented scripts/API, or mark the console as not shipped. |
| CG-GAP-007 | P1 | Web stack documentation drift | Older docs claim Next.js, TypeScript, Tailwind, and 2D/3D Force-Graph in places; current app is Vite + React + JavaScript/CSS with Cytoscape-based graph UI. | `apps/web/package.json`, build output, and source tree. | Update web UX docs to current stack and planned future stack separately. |
| CG-GAP-008 | P1 | External/live acceptance not proven by this audit | Full Python and web build pass, but live Hubble, real external connectors, production HA, browser E2E, and VS Code extension host acceptance were not rerun here. | This audit ran local regression/build/gates only. | Add a release checklist that requires live infra/profile receipts before production-release claims. |
| CG-GAP-009 | P2 | Generated audit artifacts are derived evidence | `EOIP-engg-doc-pkg/audits/generated/*` is generated by the audit script and useful, but should be treated as derived evidence. | Generated in this pass. | Keep as audit evidence or add to generated-artifact policy. Do not treat generated output as source requirements. |

## Code-Graph Specific Findings

| Finding | Status | Notes |
|---|---|---|
| Code ingestion and code graph modules exist | Implemented | `packages/eoip/ingestion/code.py`, `code_graph_json.py`, `repository.py`, `local_code.py`, and `packages/eoip/codegraph/*` exist with unit coverage. |
| Code graph docs exist | Implemented with drift risk | `EOIP-engg-doc-pkg/17-code-graph.md`, `reference/code-graph.md`, and implementation work packages exist. They should be updated to point at actual modules. |
| Polyglot parser claims need exact language matrix | Partial documentation gap | Docs mention broad language coverage. Current parser/code ingestion tests should be used as the source of truth for each language. |
| Code graph API route evidence exists | Implemented | Tests include code graph JSON ingestion and runtime Hubble code graph tests. |
| Source-bound code graph acceptance | Needs release evidence | Local unit coverage passes; live runtime/Hubble acceptance was not rerun in this pass. |

## Requirement and Feature Areas Not Yet Fully Closed

- `PIC-002` Governed autonomous agent runtime: missing exact `/api/v1/loops/catalog` route evidence.
- `PIC-010` Role-based product experience and executive reporting: missing exact `/api/v1/reports` route evidence, despite implemented report subroutes.
- 1,199 conservative documentation-audit candidate records without literal code/test leads.
- Historical claims that require semantic review before they can stay in current docs.
- Live connector acceptance against real Jira/GitLab/GitHub/Confluence/ServiceNow credentials.
- Live Hubble/runtime validation receipts for this exact working tree.
- Browser-level web E2E verification after the Vite build.
- VS Code extension host verification after the current backend changes.
- Production HA, backup/restore, disaster recovery, and security certification receipts for a real deployed environment.
- Link-check cleanup for non-root docs.

## Documentation Update Policy From This Audit

Historical audit files should remain historical. They should not be silently rewritten to pretend old evidence was generated today.

Current/live docs should now point to this file:

- `README.md`
- `available-status.md`
- `todo-status.md`
- `EOIP-engg-doc-pkg/available-status.md`
- `EOIP-engg-doc-pkg/todo-status.md`
- `EOIP-engg-doc-pkg/DOCUMENTATION-INDEX.md`
- `EOIP-engg-doc-pkg/README.md`

The machine-generated evidence files from this pass live under:

- `EOIP-engg-doc-pkg/audits/generated/current-gap-report.json`
- `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md`
- `EOIP-engg-doc-pkg/audits/generated/documentation-inventory.json`

## Verification Commands Run

```powershell
$env:PYTHONPATH='packages;.'
python -m scripts.documentation_audit --project-root .
python -m scripts.gap_coverage --project-root . --output .tmp/gap-verify-current.json --fail-on-gate --gate-priority P0
python -m scripts.gap_coverage --project-root . --doc-set g2 --output .tmp/g2-verify-current.json --fail-on-gate --gate-priority P0
python -m pytest
cd apps/web
npm run build
```

Observed verification:

- `python -m pytest`: 2,843 passed, 34 skipped, 2 warnings in 709.87s.
- `npm run build`: Vite build passed in 8.35s.
- GAP and G2 P0 coverage gates passed.

## Closure Plan

1. Close `CG-GAP-001` by mounting or documenting the loops catalog route.
2. Close `CG-GAP-002` by adding a reports root route or adjusting product scanner expectations.
3. Re-run the product scanner and update this audit with a passing first-choice gate.
4. Run a local Markdown link checker over non-historical docs and patch broken links.
5. Triage the 1,199 conservative documentation-audit Missing records into true gaps, duplicate historical claims, false positives, and roadmap items.
6. Reconcile web UI docs to Vite/React/current source instead of older Next.js/Tailwind claims.
7. Decide whether `apps/console` should be implemented or removed from current status docs.
8. Run live connector, Hubble/runtime, browser E2E, and VS Code extension acceptance and attach fresh receipts.
