# EOIP Context

The extension reads context from a local EOIP deployment and never edits source
files. Run **EOIP: Set Access Token** and enter `EOIP_API_TOKEN` from
`deploy/.env`; the token is stored in VS Code SecretStorage. Set
`eoip.repositoryRoot` to the local checkout matching the ingested repository.

## What is implemented

The extension is a read-only IDE surface over the EOIP API and MCP server. It
supports active-file context, symbol lookup, Jira/source-to-code tracing,
impact, lineage/provenance, GraphRAG retrieval, knowledge graph search,
natural-language query, and approved MCP tool invocation. It uses the same
Bearer token as the web/API stack, stores it in VS Code SecretStorage, and
rejects write/admin tools.

Source navigation is intentionally constrained. Links returned by EOIP must
resolve under `eoip.repositoryRoot`; absolute paths, traversal, and symlinks
escaping the workspace are refused. The extension can show prior successful
context when the API is temporarily unavailable, but it does not mutate files or
silently fabricate graph results.

The **EOIP Context** view appears in Explorer. Place the caret within an indexed
symbol and run **EOIP: Context for Active File**, or move the caret between
symbols to refresh the view. It shows the current symbol and source range,
related graph entities grouped by type, traversal relationships, provenance, and
evidence returned by EOIP. If the API is unavailable or the symbol is not
indexed, the view reports that state and retains the last successful context
when available.

Use **EOIP: Trace Requirement to Code** to select a Jira/source entity and show
both the bounded path to the active symbol and its impact. **Explore Impact**,
**Trace Provenance / Lineage**, **GraphRAG Retrieval**, and **Search Knowledge
Graph** remain available from the command palette. Selecting an indexed code
entity in the view opens its workspace-relative source range; navigation rejects
absolute paths, path traversal, and symlinks escaping `eoip.repositoryRoot`.

Build the VSIX with `docker compose --profile tools run --build --rm
extension-build` from the `deploy/` directory. Install
`dist/eoip-context-0.1.0.vsix` using VS Code's **Extensions: Install from VSIX**
command. The extension runs in VS Code; Docker packages it and hosts the API.

Run the extension-host acceptance checks from this directory with `npm test`.
The runner downloads a compatible VS Code build unless `VSCODE_EXECUTABLE` points
to an installed VS Code executable.

For an installed Windows host, run:

```powershell
$env:VSCODE_EXECUTABLE = 'C:\Program Files\Microsoft VS Code\Code.exe'
npm.cmd test
```

Each run uses a unique disposable user-data/extensions profile; it does not
change your regular settings, token or installed extensions. A JSON receipt is
saved under the repository's ignored `test-results/` directory. A nonzero host
exit or missing/incomplete receipt fails the gate.

Five multi-step journeys exercise all ten commands: NLQ/MCP protocol and refusals; context/path/source
navigation and offline handling; search/impact/lineage/retrieval; nested and flat
document-symbol providers with the cursor inside a function body; authentication
and unsafe-path refusals. Source text remains unchanged. The tests use real
VS Code commands, editors, ranges, SecretStorage and document-symbol registration,
but automate input/quick-pick selection and use a loopback HTTP contract fixture.
They do not certify live HugeGraph integration, manual prompt behavior or visual
TreeView layout.

**EOIP: Natural Language Query** submits a read-only question to
`/api/v1/query/nl` and displays the interpreted plan, answer, warnings and graph
results. **EOIP: Read-only MCP Tool** discovers and invokes approved read-only
tools through an actual initialization/tools-list/tools-call exchange.
Set `eoip.mcpUrl` (default `http://localhost:8001/mcp`) for EOIP's stateless JSON
Streamable HTTP transport. Arbitrary agent/admin/write tools are refused.
Both commands use the same SecretStorage token as other EOIP commands.

Full auto-demo uses a disposable visible development host with the updated
0.1.0 source extension. See [demo instructions](../../demo/autodemo/README.md).
The existing VSIX is not rebuilt or installed by this demo. `npm test` also runs
native Node protocol tests before the five real-host fixture journeys.

To run the separate live NLQ/MCP presentation on Windows, double-click
`demo/autodemo/run-demo-vscode.bat` or run it from a terminal. It starts the
local Docker services, waits up to 60 seconds for API/MCP health, then checks
that the `intent-to-runtime` and `knowledge-provenance` graph scenarios are
already ready. It does not seed or preload the graph. Ingest the approved demo
scenario pack first if either prerequisite is missing. Provide
`EOIP_API_TOKEN` in the environment or `deploy/.env`.

The presentation runs 17 live steps: NLQ `SEARCH`, `PATH`, `IMPACT`,
`NEIGHBORHOOD`, `LINEAGE`, and `TRACEABILITY`, followed by all 11 read-only MCP
tools supported by the extension. Each step is checked and recorded in a JSON
receipt under `test-results/`; successful runs hold the visible result between
steps and wait for **Close Demo** at the end. The default result hold is
2500 ms; use `--delay MS` (0 through 60000) to change it. `--no-pause`
disables the hold and final confirmation for unattended runs. Use `--dry-run`
to inspect coverage, pacing, and prerequisites without starting services.
This demonstrates the workspace source extension in an isolated
visible VS Code development host; it does not install or certify a VSIX.
