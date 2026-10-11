# EOIP / KnowGridFlow Current Available Status

**Document ID:** EOIP-STATUS-CURRENT-2026-10-11
**Status:** Current evidence-bound status, superseding older production-complete claims
**Source Audit:** [../Audit-GAPS-CG-dev.md](../Audit-GAPS-CG-dev.md)

## Current Evidence

| Evidence | Result |
|---|---|
| Markdown audit | 192 current `.md` files / 38,121 lines mechanically read; documentation audit scanned 194 Markdown/text documents / 46,685 lines |
| Full pytest run | `2843 passed`, `34 skipped`, `2 warnings`, `0 failures` in 709.87s |
| GAP coverage gate | 296/296 done; P0 gate passed |
| G2 coverage gate | 364/364 done; P0 gate passed |
| Deployment route scan | 502 routes |
| Product capability scanner | Score `0.9857`; first-choice gate blocked only by `PIC-002` route evidence |
| Web build | `npm run build` passed in `apps/web` |

## Implemented Areas

- FastAPI API services under `apps/api`.
- Graph store/backends, traversal, algorithms, query, bitemporal, simulation, and analytics modules under `packages/eoip/graph` and `packages/eoip/query`.
- Retrieval and GraphRAG modules under `packages/eoip/retrieval`, plus `ragx`.
- Source connector and ingestion modules under `packages/eoip/connectors` and `packages/eoip/ingestion`.
- MCP facade under `apps/mcp`.
- VS Code extension under `apps/vscode-extension`.
- Vite + React web app under `apps/web`.
- Enterprise/security/privacy/compliance/config/licensing/egress/tenancy/brain/moonshot modules.

## Current Gaps

- `PIC-002`: `/api/v1/loops/catalog` is expected by the product scanner but is not mounted in the deployment app.
- `PIC-010`: `/api/v1/reports` root route is expected by the scanner; report subroutes are implemented.
- Documentation audit still has 1,199 conservative candidate records without literal implementation/test leads.
- Older/historical docs still include stale paths, old counts, and current-vs-roadmap ambiguity.
- Live connector, Hubble/runtime, browser E2E, and VS Code extension host acceptance were not rerun in this audit pass.

Use [../Audit-GAPS-CG-dev.md](../Audit-GAPS-CG-dev.md) as the active closure backlog.
