# Application Entry Points

EOIP already has multiple process/client entry points sharing `packages/eoip`. Run commands from the repository root. A separate entry point does not imply independently qualified persistence or authorization.

| Component | Start/build boundary | Guide |
|---|---|---|
| API | `python -m uvicorn apps.api.main:create_app --factory` with explicit environment | [API](api/README.md) |
| Worker | `python -m apps.worker.main` with the same persistent backend/data configuration | [Worker](worker/README.md) |
| MCP | `python -m uvicorn apps.mcp.main:create_app --factory` with API URL and token | [MCP](mcp/README.md) |
| Web | `npm --prefix apps/web run dev` or `run build` | [Web](web/README.md) |
| VS Code | Host extension or packaged VSIX | [Extension](vscode-extension/README.md) |

The default [Compose profile](../deploy/docker-compose.yml) wires API, worker, MCP and web to HugeGraph and application volumes. The [alternate frontend](../frontend/README.md) and [backend preview shim](../backend/README.md) sit outside this folder and have different launch assumptions. Inspect both before migration.

Use [Getting Started](../docs/getting-started.md) for full safe commands, [architecture](../docs/architecture-guide.md) for trust/data boundaries and [suite plan](../docs/EOIP-suite-architecture-plan.md) for the proposed future packaging. The suite catalog is not the current app list.
