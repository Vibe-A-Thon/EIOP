# EOIP Context

Read-only context from your local Docker deployment. Run **EOIP: Set Access Token**
and enter `EOIP_API_TOKEN` from `deploy/.env`. The token is kept in VS Code
SecretStorage. Then use **Search Knowledge Graph**, **Context for Active File**,
**Explore Impact**, **Trace Requirement to Code**, **Trace Provenance / Lineage**,
or **GraphRAG Retrieval** from the command palette.

For **Open Symbol Source**, set `eoip.repositoryRoot` to the local ingested
repository, for example `F:\code\EOIP\EIOP\examples\demo-repo`.

Build with `docker compose --profile tools run --build --rm extension-build`
from the `deploy/` directory. Install `dist/eoip-context-0.1.0.vsix` using VS Code's
**Extensions: Install from VSIX** command. The extension runs inside VS Code;
Docker packages it and hosts its API.
