# EIOP

Enterprise Ontology & Intelligence Platform. The implementation lives at the
repository root; the requirements and architecture handoff are in
`EOIP-engg-doc-pkg/`.

Start the local Docker deployment from this directory: From the repository root, with Docker Desktop running in Linux-container mode:

```powershell
.\scripts\docker.ps1 up
.\scripts\docker.ps1 test
```
The startup script finds Docker Desktop even when its CLI is missing from PATH,
generates local credentials, builds the services, and waits for readiness.
No host Python or Node installation is required.


Open [the explorer](http://localhost:8080/app) or
[administration](http://localhost:8080/admin). Enter `EOIP_API_TOKEN` from the
generated, Git-ignored `deploy/.env`. API documentation is at
[localhost:8000/docs](http://localhost:8000/docs).

The demo worker loads Jira fixtures, a real Git repository, Python/TypeScript
symbols, documentation, merge-request metadata, and pipeline metadata.

See [the Docker runbook](docs/docker-local.md) for Full instructions and current scope, services, tests,
backup/restore, the VS Code extension, optional profiles, and implementation limits.
