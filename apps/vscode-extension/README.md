# EOIP Context

The extension reads context from a local EOIP deployment and never edits source
files. Run **EOIP: Set Access Token** and enter `EOIP_API_TOKEN` from
`deploy/.env`; the token is stored in VS Code SecretStorage. Set
`eoip.repositoryRoot` to the local checkout matching the ingested repository.

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
