# Local deployment verification

> Current overlay, 2026-10-11: this page is a retained local deployment receipt
> from 2026-10-02. For current project status, use
> [../available-status.md](../available-status.md) and
> [../../KGF-MASTER-BACKLOG.md](../../KGF-MASTER-BACKLOG.md). The current
> working tree shows 167/516 backlog tasks ticked; Phase 8 release receipts are
> still required before production claims.

Verified on 2026-10-02 using the user's Docker Desktop Linux engine on Windows.
Docker Engine: 29.8.1. Compose: v5.5.1. Database: HugeGraph 1.7.0 / RocksDB.

| Check | Result |
|---|---|
| Build and start default Compose services | Passed; graph/API/worker/web/MCP healthy |
| Idempotent schema bootstrap | Passed; subsequent initialization returns created=false |
| Python tests in Linux container | 123 passed |
| Chromium UI tests in Docker | 2 passed |
| Authentication and excessive query limits | Passed |
| Durable worker demo replay | Passed; business entity counts preserved |
| Jira → Commit → File → CodeSymbol traversal | Passed; source evidence returned |
| Impact, TraceImpact, model-unavailable graph retrieval | Passed |
| Schema/endpoint/evidence validation on demo data | Passed |
| Real MCP initialization, tool listing, search/path calls | Passed |
| Logical backup and isolated HugeGraph restore | Passed; 39 vertices, 61 edges, 9 raw evidence files restored |
| Main graph/API/worker restart persistence | Passed; 41 vertices, 64 edges and evidence path retained |
| Prometheus scraping of live API metrics | Passed |
| VS Code extension packaging in Docker | Passed; eoip-context-0.1.0.vsix generated |
| Frontend and extension dependency audit | No reported vulnerabilities in the installed locks |
| Basic Python syntax/import/unused-name lint | Passed |
| Generated credentials and artifacts ignored by Git | Passed |

Graph counts differ between snapshot and restart checks because replay records
new ingestion runs. Screenshots from UI tests are in `test-results/`.
The VS Code extension was packaged and its JavaScript syntax checked; its commands
were not executed inside the user's VS Code extension host. Optional Ollama
generation with a staged model has not been tested. Production-scale performance,
native database backup, and the remaining roadmap requirements have not been
certified. See [the runbook](docker-local.md) for the supported deployment scope.

The core deployment and Prometheus were left running. The disposable restore
graph and test runners were removed. No Git commit was created.
