# EOIP / KnowGridFlow Current Available Status

**Document ID:** EOIP-STATUS-CURRENT-2026-10-11
**Status:** Current evidence-bound status, superseding older production-complete claims
**Master Backlog:** [../KGF-MASTER-BACKLOG.md](../KGF-MASTER-BACKLOG.md)
**Source Audits:** [Audit-GAPS-CG-dev.md](Audit-GAPS-CG-dev.md)

## Current Evidence

| Evidence | Result |
|---|---|
| Master Backlog | 167/516 tasks ticked in the current working tree: Phase 0 13/13, Phase 1 65/65, Phase 2 88/130, Phase 8 1/17; remaining phases have no ticked rows yet. Source: [../KGF-MASTER-BACKLOG.md](../KGF-MASTER-BACKLOG.md), which is not edited by this status overlay. |
| Requirement Registry | 893 items mapped with code/test paths in `requirements-registry.json` (BASE-01) |
| Requirement Test Map | 539 requirements mapped to automated tests in `requirements-test-map.json` (BASE-02) |
| Markdown documentation sweep | 231 first-party Markdown files / 47,000 lines read mechanically, excluding `KGF-MASTER-BACKLOG.md`, `.git`, `.venv`, `.pytest_cache`, and `node_modules` |
| Full pytest run | `2843 passed`, `34 skipped`, `2 warnings`, `0 failures` in 709.87s |
| GAP coverage gate | 296/296 done; P0 gate passed |
| G2 coverage gate | 364/364 done; P0 gate passed |
| Deployment route scan | 502+ routes active; `/api/v1/loops/catalog` and `/api/v1/reports` mounted |
| Product capability scanner | Enterprise grade score `1.0` (10/10 capabilities `advanced_ready`), First-Choice Gate PASSED |
| Web build | `npm run build` passed in `apps/web` (175 modules, 0 errors) |

## Implemented Areas

- FastAPI API services under `apps/api`.
- Graph store/backends, traversal, algorithms, query, bitemporal, simulation, and analytics modules under `packages/eoip/graph` and `packages/eoip/query`.
- Retrieval and GraphRAG modules under `packages/eoip/retrieval`, plus `ragx`.
- Source connector and ingestion modules under `packages/eoip/connectors` and `packages/eoip/ingestion`.
- Phase 2 acquisition/sync work now includes SourceEvent v2 envelope coverage, ordered baseline manifests, semantic event consumers, DLQ/replay, tombstone/delete semantics, permission metadata, content fingerprinting, attachment metadata, incremental enrichment, pause/resume, backfill, selective rescan, and crawler-security controls.
- MCP facade under `apps/mcp`.
- VS Code extension under `apps/vscode-extension`.
- Vite + React web app under `apps/web` with responsive Cytoscape canvas and 6-panel Cognitive Engineering Studio.
- Enterprise/security/privacy/compliance/config/licensing/egress/tenancy/brain/moonshot modules.

## Active Closure Roadmap

All remaining items and live acceptance tests are tracked in [../KGF-MASTER-BACKLOG.md](../KGF-MASTER-BACKLOG.md).

